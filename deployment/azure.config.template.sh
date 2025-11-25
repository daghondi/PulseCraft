# Azure Deployment Configuration
# Copy this file to azure.config.sh and fill in your values

# Azure Subscription
export AZURE_SUBSCRIPTION_ID="your-subscription-id-here"
export AZURE_LOCATION="eastus"  # or your preferred region

# Resource Group
export RESOURCE_GROUP="rg-pulsecraft-prod"

# App Service (Backend)
export APP_SERVICE_PLAN="plan-pulsecraft-prod"
export APP_SERVICE_NAME="app-pulsecraft-api"  # Must be globally unique
export APP_SERVICE_SKU="B1"  # Basic tier, upgrade to S1 for production

# Static Web App (Frontend)
export STATIC_WEB_APP_NAME="swa-pulsecraft-frontend"  # Must be globally unique

# Azure OpenAI
export OPENAI_ACCOUNT_NAME="openai-pulsecraft"  # Must be globally unique
export OPENAI_DEPLOYMENT_NAME="gpt-4"
export OPENAI_MODEL="gpt-4"
export OPENAI_MODEL_VERSION="0613"

# Cosmos DB
export COSMOS_ACCOUNT_NAME="cosmos-pulsecraft"  # Must be globally unique
export COSMOS_DATABASE_NAME="pulsecraft"
export COSMOS_CONTAINER_NAME="sessions"

# Service Bus
export SERVICE_BUS_NAMESPACE="sb-pulsecraft"  # Must be globally unique
export SERVICE_BUS_QUEUE_ENRICHER="enricher-queue"
export SERVICE_BUS_QUEUE_SCORER="scorer-queue"
export SERVICE_BUS_QUEUE_COMPOSER="composer-queue"
export SERVICE_BUS_QUEUE_COMPLIANCE="compliance-queue"

# Storage Account
export STORAGE_ACCOUNT_NAME="stpulsecraft"  # Must be globally unique, lowercase, no hyphens
export STORAGE_CONTAINER_NAME="customer-data"

# Key Vault
export KEY_VAULT_NAME="kv-pulsecraft"  # Must be globally unique

# Application Insights
export APP_INSIGHTS_NAME="appi-pulsecraft"

# Container Registry (for agent deployments)
export CONTAINER_REGISTRY_NAME="crpulsecraft"  # Must be globally unique

# Tags
export TAGS="project=PulseCraft environment=production hackathon=innovation-challenge"
