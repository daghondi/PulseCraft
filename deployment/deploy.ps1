# Azure Deployment Scripts for PowerShell (Windows)

# This file contains PowerShell equivalents of the bash deployment scripts
# for Windows users who prefer PowerShell over Git Bash

###############################################################################
# 1. DEPLOY AZURE INFRASTRUCTURE
###############################################################################

function Deploy-AzureInfrastructure {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "PulseCraft - Azure Deployment" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green

    # Load configuration
    if (!(Test-Path "azure.config.ps1")) {
        Write-Host "ERROR: azure.config.ps1 not found!" -ForegroundColor Red
        Write-Host "Please copy azure.config.template.ps1 to azure.config.ps1 and configure it."
        return
    }

    . .\azure.config.ps1

    Write-Host "`nConfiguration loaded:" -ForegroundColor Yellow
    Write-Host "  Subscription: $AZURE_SUBSCRIPTION_ID"
    Write-Host "  Location: $AZURE_LOCATION"
    Write-Host "  Resource Group: $RESOURCE_GROUP"

    # Set subscription
    Write-Host "`nSetting Azure subscription..." -ForegroundColor Yellow
    az account set --subscription $AZURE_SUBSCRIPTION_ID

    # Create Resource Group
    Write-Host "`nCreating Resource Group..." -ForegroundColor Yellow
    az group create `
        --name $RESOURCE_GROUP `
        --location $AZURE_LOCATION `
        --tags $TAGS

    # Create App Service Plan
    Write-Host "`nCreating App Service Plan..." -ForegroundColor Yellow
    az appservice plan create `
        --name $APP_SERVICE_PLAN `
        --resource-group $RESOURCE_GROUP `
        --location $AZURE_LOCATION `
        --sku $APP_SERVICE_SKU `
        --is-linux `
        --tags $TAGS

    # Create App Service (Backend)
    Write-Host "`nCreating App Service for Backend API..." -ForegroundColor Yellow
    az webapp create `
        --name $APP_SERVICE_NAME `
        --resource-group $RESOURCE_GROUP `
        --plan $APP_SERVICE_PLAN `
        --runtime "NODE:18-lts" `
        --tags $TAGS

    # Create Static Web App (Frontend)
    Write-Host "`nCreating Static Web App for Frontend..." -ForegroundColor Yellow
    az staticwebapp create `
        --name $STATIC_WEB_APP_NAME `
        --resource-group $RESOURCE_GROUP `
        --location $AZURE_LOCATION `
        --sku Free `
        --tags $TAGS

    # Create Cosmos DB Account
    Write-Host "`nCreating Cosmos DB Account..." -ForegroundColor Yellow
    az cosmosdb create `
        --name $COSMOS_ACCOUNT_NAME `
        --resource-group $RESOURCE_GROUP `
        --locations regionName=$AZURE_LOCATION failoverPriority=0 `
        --default-consistency-level Session `
        --tags $TAGS

    Write-Host "`nCreating Cosmos DB Database..." -ForegroundColor Yellow
    az cosmosdb sql database create `
        --account-name $COSMOS_ACCOUNT_NAME `
        --resource-group $RESOURCE_GROUP `
        --name $COSMOS_DATABASE_NAME

    Write-Host "`nCreating Cosmos DB Container..." -ForegroundColor Yellow
    az cosmosdb sql container create `
        --account-name $COSMOS_ACCOUNT_NAME `
        --resource-group $RESOURCE_GROUP `
        --database-name $COSMOS_DATABASE_NAME `
        --name $COSMOS_CONTAINER_NAME `
        --partition-key-path "/sessionId" `
        --throughput 400

    # Create Azure OpenAI Service
    Write-Host "`nCreating Azure OpenAI Service..." -ForegroundColor Yellow
    az cognitiveservices account create `
        --name $OPENAI_ACCOUNT_NAME `
        --resource-group $RESOURCE_GROUP `
        --location $AZURE_LOCATION `
        --kind OpenAI `
        --sku S0 `
        --tags $TAGS `
        --yes

    # Create Service Bus Namespace
    Write-Host "`nCreating Service Bus Namespace..." -ForegroundColor Yellow
    az servicebus namespace create `
        --name $SERVICE_BUS_NAMESPACE `
        --resource-group $RESOURCE_GROUP `
        --location $AZURE_LOCATION `
        --sku Standard `
        --tags $TAGS

    # Create Service Bus Queues
    Write-Host "`nCreating Service Bus Queues..." -ForegroundColor Yellow
    $queues = @($SERVICE_BUS_QUEUE_ENRICHER, $SERVICE_BUS_QUEUE_SCORER, $SERVICE_BUS_QUEUE_COMPOSER, $SERVICE_BUS_QUEUE_COMPLIANCE)
    foreach ($queue in $queues) {
        Write-Host "  Creating queue: $queue"
        az servicebus queue create `
            --name $queue `
            --namespace-name $SERVICE_BUS_NAMESPACE `
            --resource-group $RESOURCE_GROUP `
            --max-size 1024
    }

    # Create Storage Account
    Write-Host "`nCreating Storage Account..." -ForegroundColor Yellow
    az storage account create `
        --name $STORAGE_ACCOUNT_NAME `
        --resource-group $RESOURCE_GROUP `
        --location $AZURE_LOCATION `
        --sku Standard_LRS `
        --tags $TAGS

    # Create Key Vault
    Write-Host "`nCreating Key Vault..." -ForegroundColor Yellow
    az keyvault create `
        --name $KEY_VAULT_NAME `
        --resource-group $RESOURCE_GROUP `
        --location $AZURE_LOCATION `
        --enabled-for-deployment true `
        --enabled-for-template-deployment true `
        --tags $TAGS

    # Create Application Insights
    Write-Host "`nCreating Application Insights..." -ForegroundColor Yellow
    az monitor app-insights component create `
        --app $APP_INSIGHTS_NAME `
        --location $AZURE_LOCATION `
        --resource-group $RESOURCE_GROUP `
        --tags $TAGS

    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "Deployment Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "`nBackend API will be available at:" -ForegroundColor Green
    Write-Host "  https://$APP_SERVICE_NAME.azurewebsites.net"
}

###############################################################################
# 2. DEPLOY BACKEND
###############################################################################

function Deploy-Backend {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "PulseCraft - Backend Deployment" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green

    # Load configuration
    if (!(Test-Path "azure.config.ps1")) {
        Write-Host "ERROR: azure.config.ps1 not found!" -ForegroundColor Red
        return
    }

    . .\azure.config.ps1

    # Navigate to backend directory
    Push-Location ..\backend

    # Install dependencies
    Write-Host "`nInstalling backend dependencies..." -ForegroundColor Yellow
    npm install --production

    # Create deployment package
    Write-Host "`nCreating deployment package..." -ForegroundColor Yellow
    Compress-Archive -Path .\* -DestinationPath ..\deployment\backend-deploy.zip -Force `
        -CompressionLevel Optimal `
        -Exclude "node_modules","*.env*","data","*.log"

    Pop-Location

    # Deploy to Azure App Service
    Write-Host "`nDeploying to Azure App Service..." -ForegroundColor Yellow
    az webapp deployment source config-zip `
        --resource-group $RESOURCE_GROUP `
        --name $APP_SERVICE_NAME `
        --src backend-deploy.zip

    # Wait for deployment
    Write-Host "`nWaiting for deployment to complete..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10

    # Test deployment
    Write-Host "`nTesting deployment..." -ForegroundColor Yellow
    $BACKEND_URL = "https://$APP_SERVICE_NAME.azurewebsites.net"
    
    try {
        $response = Invoke-WebRequest -Uri "$BACKEND_URL/health" -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "✓ Backend deployment successful!" -ForegroundColor Green
            Write-Host "Backend is running at: $BACKEND_URL" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "✗ Backend health check failed" -ForegroundColor Red
        Write-Host "Check logs: az webapp log tail --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP" -ForegroundColor Yellow
    }

    # Clean up
    Remove-Item backend-deploy.zip -ErrorAction SilentlyContinue

    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "Backend URL: $BACKEND_URL" -ForegroundColor Yellow
    Write-Host "API Endpoints:" -ForegroundColor Yellow
    Write-Host "  POST $BACKEND_URL/api/demo/run"
    Write-Host "  GET  $BACKEND_URL/api/demo/list"
    Write-Host "  GET  $BACKEND_URL/api/demo/replay/:id"
}

###############################################################################
# 3. DEPLOY FRONTEND
###############################################################################

function Deploy-Frontend {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "PulseCraft - Frontend Deployment" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green

    # Load configuration
    if (!(Test-Path "azure.config.ps1")) {
        Write-Host "ERROR: azure.config.ps1 not found!" -ForegroundColor Red
        return
    }

    . .\azure.config.ps1

    # Get backend URL
    $BACKEND_URL = "https://$APP_SERVICE_NAME.azurewebsites.net"
    Write-Host "`nBackend API URL: $BACKEND_URL" -ForegroundColor Yellow

    # Navigate to frontend directory
    Push-Location ..\frontend

    # Update frontend .env for production
    Write-Host "`nConfiguring frontend environment..." -ForegroundColor Yellow
    @"
VITE_API_URL=$BACKEND_URL
VITE_API_TIMEOUT=5000
"@ | Out-File -FilePath .env.production -Encoding UTF8

    Write-Host "✓ Frontend environment configured" -ForegroundColor Green

    # Get deployment token for Static Web App
    Write-Host "`nRetrieving Static Web App deployment token..." -ForegroundColor Yellow
    $DEPLOYMENT_TOKEN = az staticwebapp secrets list `
        --name $STATIC_WEB_APP_NAME `
        --resource-group $RESOURCE_GROUP `
        --query "properties.apiKey" -o tsv

    if ([string]::IsNullOrEmpty($DEPLOYMENT_TOKEN)) {
        Write-Host "ERROR: Could not retrieve deployment token" -ForegroundColor Red
        Write-Host "You may need to deploy via GitHub Actions instead" -ForegroundColor Yellow
        Pop-Location
        return
    }

    # Deploy using Azure Static Web Apps CLI
    Write-Host "`nDeploying frontend to Azure Static Web Apps..." -ForegroundColor Yellow
    swa deploy ./public `
        --deployment-token $DEPLOYMENT_TOKEN `
        --app-name $STATIC_WEB_APP_NAME `
        --env production

    # Get Static Web App URL
    Write-Host "`nRetrieving Static Web App URL..." -ForegroundColor Yellow
    $FRONTEND_HOSTNAME = az staticwebapp show `
        --name $STATIC_WEB_APP_NAME `
        --resource-group $RESOURCE_GROUP `
        --query "defaultHostname" -o tsv

    if ($FRONTEND_HOSTNAME) {
        $FRONTEND_URL = "https://$FRONTEND_HOSTNAME"
        Write-Host "✓ Frontend deployed successfully!" -ForegroundColor Green
        Write-Host "Frontend URL: $FRONTEND_URL" -ForegroundColor Green
    }

    Pop-Location

    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "Frontend URL: $FRONTEND_URL" -ForegroundColor Yellow
    Write-Host "Backend API: $BACKEND_URL" -ForegroundColor Yellow
}

###############################################################################
# USAGE
###############################################################################

Write-Host @"

PulseCraft - Azure Deployment Scripts (PowerShell)

Available Functions:
  1. Deploy-AzureInfrastructure  - Deploy all Azure resources
  2. Deploy-Backend              - Deploy backend API
  3. Deploy-Frontend             - Deploy frontend UI

Usage:
  1. Copy azure.config.template.ps1 to azure.config.ps1
  2. Edit azure.config.ps1 with your values
  3. Run: . .\deploy.ps1
  4. Run: Deploy-AzureInfrastructure
  5. Run: Deploy-Backend
  6. Run: Deploy-Frontend

Example:
  PS> . .\deploy.ps1
  PS> Deploy-AzureInfrastructure
  PS> Deploy-Backend
  PS> Deploy-Frontend

"@
