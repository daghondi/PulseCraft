# Azure Deployment Configuration for PowerShell
# Copy this file to azure.config.ps1 and fill in your values

# Azure Subscription
$AZURE_SUBSCRIPTION_ID = "your-subscription-id-here"
$AZURE_LOCATION = "eastus"  # or your preferred region

# Resource Group
$RESOURCE_GROUP = "rg-pulsecraft-prod"

# App Service (Backend)
$APP_SERVICE_PLAN = "plan-pulsecraft-prod"
$APP_SERVICE_NAME = "app-pulsecraft-api"  # Must be globally unique
$APP_SERVICE_SKU = "B1"  # Basic tier, upgrade to S1 for production

# Static Web App (Frontend)
$STATIC_WEB_APP_NAME = "swa-pulsecraft-frontend"  # Must be globally unique

# Azure OpenAI
$OPENAI_ACCOUNT_NAME = "openai-pulsecraft"  # Must be globally unique
$OPENAI_DEPLOYMENT_NAME = "gpt-4"
$OPENAI_MODEL = "gpt-4"
$OPENAI_MODEL_VERSION = "0613"

# Cosmos DB
$COSMOS_ACCOUNT_NAME = "cosmos-pulsecraft"  # Must be globally unique
$COSMOS_DATABASE_NAME = "pulsecraft"
$COSMOS_CONTAINER_NAME = "sessions"

# Service Bus
$SERVICE_BUS_NAMESPACE = "sb-pulsecraft"  # Must be globally unique
$SERVICE_BUS_QUEUE_ENRICHER = "enricher-queue"
$SERVICE_BUS_QUEUE_SCORER = "scorer-queue"
$SERVICE_BUS_QUEUE_COMPOSER = "composer-queue"
$SERVICE_BUS_QUEUE_COMPLIANCE = "compliance-queue"

# Storage Account
$STORAGE_ACCOUNT_NAME = "stpulsecraft"  # Must be globally unique, lowercase, no hyphens
$STORAGE_CONTAINER_NAME = "customer-data"

# Key Vault
$KEY_VAULT_NAME = "kv-pulsecraft"  # Must be globally unique

# Application Insights
$APP_INSIGHTS_NAME = "appi-pulsecraft"

# Container Registry (for agent deployments)
$CONTAINER_REGISTRY_NAME = "crpulsecraft"  # Must be globally unique

# Tags
$TAGS = "project=PulseCraft environment=production hackathon=innovation-challenge"
