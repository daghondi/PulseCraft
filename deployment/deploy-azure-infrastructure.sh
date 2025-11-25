#!/bin/bash

###############################################################################
# PulseCraft - Azure Infrastructure Deployment Script
# 
# This script provisions all Azure resources needed for PulseCraft
# 
# Prerequisites:
# 1. Azure CLI installed (az --version)
# 2. Logged into Azure (az login)
# 3. Created azure.config.sh from azure.config.template.sh
# 4. Set appropriate values in azure.config.sh
#
# Usage:
#   ./deploy-azure-infrastructure.sh
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}PulseCraft - Azure Deployment${NC}"
echo -e "${GREEN}========================================${NC}"

# Load configuration
if [ ! -f "azure.config.sh" ]; then
    echo -e "${RED}ERROR: azure.config.sh not found!${NC}"
    echo "Please copy azure.config.template.sh to azure.config.sh and configure it."
    exit 1
fi

source azure.config.sh

echo -e "${YELLOW}Configuration loaded:${NC}"
echo "  Subscription: $AZURE_SUBSCRIPTION_ID"
echo "  Location: $AZURE_LOCATION"
echo "  Resource Group: $RESOURCE_GROUP"

# Set subscription
echo -e "\n${YELLOW}Setting Azure subscription...${NC}"
az account set --subscription "$AZURE_SUBSCRIPTION_ID"

# Create Resource Group
echo -e "\n${YELLOW}Creating Resource Group...${NC}"
az group create \
    --name "$RESOURCE_GROUP" \
    --location "$AZURE_LOCATION" \
    --tags $TAGS

# Create App Service Plan
echo -e "\n${YELLOW}Creating App Service Plan...${NC}"
az appservice plan create \
    --name "$APP_SERVICE_PLAN" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$AZURE_LOCATION" \
    --sku "$APP_SERVICE_SKU" \
    --is-linux \
    --tags $TAGS

# Create App Service (Backend)
echo -e "\n${YELLOW}Creating App Service for Backend API...${NC}"
az webapp create \
    --name "$APP_SERVICE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --plan "$APP_SERVICE_PLAN" \
    --runtime "NODE:18-lts" \
    --tags $TAGS

# Configure App Service settings
echo -e "\n${YELLOW}Configuring App Service...${NC}"
az webapp config set \
    --name "$APP_SERVICE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --startup-file "server.js" \
    --always-on true

# Create Static Web App (Frontend)
echo -e "\n${YELLOW}Creating Static Web App for Frontend...${NC}"
az staticwebapp create \
    --name "$STATIC_WEB_APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$AZURE_LOCATION" \
    --sku Free \
    --tags $TAGS

echo -e "${GREEN}✓ Static Web App created${NC}"
echo -e "${YELLOW}Note: You'll need to configure GitHub integration manually or use the deployment script${NC}"

# Create Cosmos DB Account
echo -e "\n${YELLOW}Creating Cosmos DB Account...${NC}"
az cosmosdb create \
    --name "$COSMOS_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --locations regionName="$AZURE_LOCATION" failoverPriority=0 \
    --default-consistency-level Session \
    --enable-free-tier false \
    --tags $TAGS

echo -e "${YELLOW}Creating Cosmos DB Database...${NC}"
az cosmosdb sql database create \
    --account-name "$COSMOS_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --name "$COSMOS_DATABASE_NAME"

echo -e "${YELLOW}Creating Cosmos DB Container...${NC}"
az cosmosdb sql container create \
    --account-name "$COSMOS_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --database-name "$COSMOS_DATABASE_NAME" \
    --name "$COSMOS_CONTAINER_NAME" \
    --partition-key-path "/sessionId" \
    --throughput 400

# Create Azure OpenAI Service
echo -e "\n${YELLOW}Creating Azure OpenAI Service...${NC}"
az cognitiveservices account create \
    --name "$OPENAI_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$AZURE_LOCATION" \
    --kind OpenAI \
    --sku S0 \
    --tags $TAGS \
    --yes

echo -e "${YELLOW}Deploying GPT-4 model...${NC}"
az cognitiveservices account deployment create \
    --name "$OPENAI_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --deployment-name "$OPENAI_DEPLOYMENT_NAME" \
    --model-name "$OPENAI_MODEL" \
    --model-version "$OPENAI_MODEL_VERSION" \
    --model-format OpenAI \
    --sku-name "Standard" \
    --sku-capacity 10

# Create Service Bus Namespace
echo -e "\n${YELLOW}Creating Service Bus Namespace...${NC}"
az servicebus namespace create \
    --name "$SERVICE_BUS_NAMESPACE" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$AZURE_LOCATION" \
    --sku Standard \
    --tags $TAGS

# Create Service Bus Queues
echo -e "${YELLOW}Creating Service Bus Queues...${NC}"
for queue in "$SERVICE_BUS_QUEUE_ENRICHER" "$SERVICE_BUS_QUEUE_SCORER" "$SERVICE_BUS_QUEUE_COMPOSER" "$SERVICE_BUS_QUEUE_COMPLIANCE"; do
    echo "  Creating queue: $queue"
    az servicebus queue create \
        --name "$queue" \
        --namespace-name "$SERVICE_BUS_NAMESPACE" \
        --resource-group "$RESOURCE_GROUP" \
        --max-size 1024
done

# Create Storage Account
echo -e "\n${YELLOW}Creating Storage Account...${NC}"
az storage account create \
    --name "$STORAGE_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$AZURE_LOCATION" \
    --sku Standard_LRS \
    --tags $TAGS

echo -e "${YELLOW}Creating Blob Container...${NC}"
az storage container create \
    --name "$STORAGE_CONTAINER_NAME" \
    --account-name "$STORAGE_ACCOUNT_NAME" \
    --auth-mode login

# Create Key Vault
echo -e "\n${YELLOW}Creating Key Vault...${NC}"
az keyvault create \
    --name "$KEY_VAULT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$AZURE_LOCATION" \
    --enabled-for-deployment true \
    --enabled-for-template-deployment true \
    --tags $TAGS

# Create Application Insights
echo -e "\n${YELLOW}Creating Application Insights...${NC}"
az monitor app-insights component create \
    --app "$APP_INSIGHTS_NAME" \
    --location "$AZURE_LOCATION" \
    --resource-group "$RESOURCE_GROUP" \
    --tags $TAGS

# Get connection strings and keys
echo -e "\n${YELLOW}Retrieving connection strings and keys...${NC}"

COSMOS_CONNECTION_STRING=$(az cosmosdb keys list \
    --name "$COSMOS_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --type connection-strings \
    --query "connectionStrings[0].connectionString" -o tsv)

OPENAI_ENDPOINT=$(az cognitiveservices account show \
    --name "$OPENAI_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "properties.endpoint" -o tsv)

OPENAI_KEY=$(az cognitiveservices account keys list \
    --name "$OPENAI_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "key1" -o tsv)

SERVICE_BUS_CONNECTION_STRING=$(az servicebus namespace authorization-rule keys list \
    --namespace-name "$SERVICE_BUS_NAMESPACE" \
    --resource-group "$RESOURCE_GROUP" \
    --name RootManageSharedAccessKey \
    --query "primaryConnectionString" -o tsv)

STORAGE_CONNECTION_STRING=$(az storage account show-connection-string \
    --name "$STORAGE_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "connectionString" -o tsv)

APP_INSIGHTS_KEY=$(az monitor app-insights component show \
    --app "$APP_INSIGHTS_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "instrumentationKey" -o tsv)

# Store secrets in Key Vault
echo -e "\n${YELLOW}Storing secrets in Key Vault...${NC}"
az keyvault secret set --vault-name "$KEY_VAULT_NAME" --name "CosmosDBConnectionString" --value "$COSMOS_CONNECTION_STRING"
az keyvault secret set --vault-name "$KEY_VAULT_NAME" --name "AzureOpenAIEndpoint" --value "$OPENAI_ENDPOINT"
az keyvault secret set --vault-name "$KEY_VAULT_NAME" --name "AzureOpenAIKey" --value "$OPENAI_KEY"
az keyvault secret set --vault-name "$KEY_VAULT_NAME" --name "ServiceBusConnectionString" --value "$SERVICE_BUS_CONNECTION_STRING"
az keyvault secret set --vault-name "$KEY_VAULT_NAME" --name "StorageConnectionString" --value "$STORAGE_CONNECTION_STRING"
az keyvault secret set --vault-name "$KEY_VAULT_NAME" --name "AppInsightsInstrumentationKey" --value "$APP_INSIGHTS_KEY"

# Configure App Service with environment variables
echo -e "\n${YELLOW}Configuring App Service environment variables...${NC}"
az webapp config appsettings set \
    --name "$APP_SERVICE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --settings \
        PORT=8080 \
        AZURE_OPENAI_ENDPOINT="$OPENAI_ENDPOINT" \
        AZURE_OPENAI_KEY="@Microsoft.KeyVault(SecretUri=https://${KEY_VAULT_NAME}.vault.azure.net/secrets/AzureOpenAIKey/)" \
        AZURE_OPENAI_DEPLOYMENT_NAME="$OPENAI_DEPLOYMENT_NAME" \
        COSMOS_DB_CONNECTION_STRING="@Microsoft.KeyVault(SecretUri=https://${KEY_VAULT_NAME}.vault.azure.net/secrets/CosmosDBConnectionString/)" \
        COSMOS_DB_DATABASE_NAME="$COSMOS_DATABASE_NAME" \
        COSMOS_DB_CONTAINER_NAME="$COSMOS_CONTAINER_NAME" \
        AZURE_SERVICE_BUS_CONNECTION_STRING="@Microsoft.KeyVault(SecretUri=https://${KEY_VAULT_NAME}.vault.azure.net/secrets/ServiceBusConnectionString/)" \
        AZURE_STORAGE_CONNECTION_STRING="@Microsoft.KeyVault(SecretUri=https://${KEY_VAULT_NAME}.vault.azure.net/secrets/StorageConnectionString/)" \
        APPINSIGHTS_INSTRUMENTATIONKEY="@Microsoft.KeyVault(SecretUri=https://${KEY_VAULT_NAME}.vault.azure.net/secrets/AppInsightsInstrumentationKey/)" \
        DEMO_MODE=false

# Grant App Service access to Key Vault
echo -e "\n${YELLOW}Configuring App Service Managed Identity...${NC}"
az webapp identity assign \
    --name "$APP_SERVICE_NAME" \
    --resource-group "$RESOURCE_GROUP"

APP_SERVICE_PRINCIPAL_ID=$(az webapp identity show \
    --name "$APP_SERVICE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query principalId -o tsv)

az keyvault set-policy \
    --name "$KEY_VAULT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --object-id "$APP_SERVICE_PRINCIPAL_ID" \
    --secret-permissions get list

# Create output summary
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"

# Save deployment info
cat > deployment-info.txt << EOF
PulseCraft - Azure Deployment Summary
Generated: $(date)

Resource Group: $RESOURCE_GROUP
Location: $AZURE_LOCATION

=== Backend API ===
App Service Name: $APP_SERVICE_NAME
App Service URL: https://${APP_SERVICE_NAME}.azurewebsites.net

=== Frontend ===
Static Web App Name: $STATIC_WEB_APP_NAME
Static Web App URL: (Configure after GitHub integration)

=== Azure Services ===
Cosmos DB Account: $COSMOS_ACCOUNT_NAME
OpenAI Endpoint: $OPENAI_ENDPOINT
OpenAI Deployment: $OPENAI_DEPLOYMENT_NAME
Service Bus Namespace: $SERVICE_BUS_NAMESPACE
Storage Account: $STORAGE_ACCOUNT_NAME
Key Vault: $KEY_VAULT_NAME
Application Insights: $APP_INSIGHTS_NAME

=== Next Steps ===
1. Deploy backend code: ./deployment/deploy-backend.sh
2. Deploy frontend code: ./deployment/deploy-frontend.sh
3. Configure Static Web App GitHub integration
4. Update frontend .env with backend API URL
5. Test the deployment: curl https://${APP_SERVICE_NAME}.azurewebsites.net/health

=== Secrets ===
All secrets are stored in Key Vault: $KEY_VAULT_NAME
Retrieve secrets using: az keyvault secret show --vault-name $KEY_VAULT_NAME --name <secret-name>

=== Cost Estimation ===
- App Service (B1): ~$13/month
- Static Web App (Free): $0
- Cosmos DB (400 RU/s): ~$24/month
- Azure OpenAI (Pay-per-use): Variable
- Service Bus (Standard): ~$10/month
- Storage (Standard LRS): ~$1/month
- Application Insights: Free tier available
TOTAL: ~$50-100/month depending on usage
EOF

echo -e "\n${GREEN}Deployment summary saved to: deployment-info.txt${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo "  1. Review deployment-info.txt"
echo "  2. Deploy backend: cd deployment && ./deploy-backend.sh"
echo "  3. Deploy frontend: cd deployment && ./deploy-frontend.sh"
echo "  4. Configure DNS (optional)"
echo "  5. Test endpoints"

echo -e "\n${GREEN}Backend API will be available at:${NC}"
echo "  https://${APP_SERVICE_NAME}.azurewebsites.net"

echo -e "\n${YELLOW}Important:${NC}"
echo "  - Keep azure.config.sh secure (contains resource names)"
echo "  - All secrets are stored in Key Vault"
echo "  - App Service has Managed Identity access to Key Vault"
