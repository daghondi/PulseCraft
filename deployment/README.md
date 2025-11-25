# Azure Deployment Guide for PulseCraft

## Overview

This guide walks you through deploying PulseCraft to Microsoft Azure using the provided deployment scripts.

## Prerequisites

### Required Tools

1. **Azure CLI** - [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
   ```bash
   # Verify installation
   az --version
   ```

2. **Node.js 18+** - [Download Node.js](https://nodejs.org/)
   ```bash
   node --version  # Should be 18.x or higher
   ```

3. **Git** - [Download Git](https://git-scm.com/)
   ```bash
   git --version
   ```

4. **Azure Static Web Apps CLI** (optional, for frontend deployment)
   ```bash
   npm install -g @azure/static-web-apps-cli
   ```

### Azure Account Setup

1. **Azure Subscription**: You need an active Azure subscription
   - Sign up at: <https://azure.microsoft.com/free/>
   - Students: <https://azure.microsoft.com/free/students/>

2. **Login to Azure**:
   ```bash
   az login
   ```

3. **Set your subscription** (if you have multiple):
   ```bash
   az account list --output table
   az account set --subscription "YOUR-SUBSCRIPTION-ID"
   ```

4. **Verify your account**:
   ```bash
   az account show
   ```

---

## Deployment Steps

### Step 1: Configure Deployment Settings

1. Navigate to the deployment directory:
   ```bash
   cd deployment
   ```

2. Copy the configuration template:
   ```bash
   cp azure.config.template.sh azure.config.sh
   ```

3. Edit `azure.config.sh` and set your values:
   ```bash
   # Required changes:
   export AZURE_SUBSCRIPTION_ID="YOUR-SUBSCRIPTION-ID"
   export AZURE_LOCATION="eastus"  # or your preferred region
   
   # Important: These must be globally unique
   export APP_SERVICE_NAME="app-pulsecraft-yourname"
   export STATIC_WEB_APP_NAME="swa-pulsecraft-yourname"
   export COSMOS_ACCOUNT_NAME="cosmos-pulsecraft-yourname"
   export OPENAI_ACCOUNT_NAME="openai-pulsecraft-yourname"
   export SERVICE_BUS_NAMESPACE="sb-pulsecraft-yourname"
   export STORAGE_ACCOUNT_NAME="stpulsecraftyourname"  # lowercase, no hyphens
   export KEY_VAULT_NAME="kv-pulsecraft-yourname"
   ```

   **Tip**: Replace `yourname` with your GitHub username or initials to ensure uniqueness.

### Step 2: Deploy Azure Infrastructure

Run the main deployment script to provision all Azure resources:

```bash
chmod +x deploy-azure-infrastructure.sh
./deploy-azure-infrastructure.sh
```

This script will create:
- ✅ Resource Group
- ✅ App Service Plan & App Service (Backend)
- ✅ Static Web App (Frontend)
- ✅ Azure Cosmos DB (Database)
- ✅ Azure OpenAI Service (AI)
- ✅ Service Bus (Messaging)
- ✅ Storage Account (Files)
- ✅ Key Vault (Secrets)
- ✅ Application Insights (Monitoring)

**Duration**: 10-15 minutes

**Output**: The script will create `deployment-info.txt` with all resource details.

### Step 3: Deploy Backend

Deploy the Node.js backend API to Azure App Service:

```bash
chmod +x deploy-backend.sh
./deploy-backend.sh
```

This will:
1. Install backend dependencies
2. Create deployment package
3. Upload to Azure App Service
4. Test the health endpoint

**Backend URL**: `https://app-pulsecraft-yourname.azurewebsites.net`

### Step 4: Deploy Frontend

Deploy the frontend UI to Azure Static Web Apps:

```bash
chmod +x deploy-frontend.sh
./deploy-frontend.sh
```

This will:
1. Configure frontend environment with backend URL
2. Create Static Web App configuration
3. Deploy to Azure Static Web Apps
4. Test the frontend

**Frontend URL**: `https://[your-app-name].azurestaticapps.net`

### Step 5: Verify Deployment

1. **Test Backend API**:
   ```bash
   curl https://app-pulsecraft-yourname.azurewebsites.net/health
   # Should return: {"status":"ok"}
   ```

2. **Test Frontend**:
   - Open `https://[your-app-name].azurestaticapps.net` in browser
   - Enter a customer name
   - Click "Run Demo"
   - Verify you get personalized results

3. **Check Logs**:
   ```bash
   # Backend logs
   az webapp log tail --name app-pulsecraft-yourname --resource-group rg-pulsecraft-prod
   
   # Application Insights
   az monitor app-insights component show --app appi-pulsecraft --resource-group rg-pulsecraft-prod
   ```

---

## GitHub Actions CI/CD (Optional)

For automatic deployment on every push to `main` branch:

### 1. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

1. **AZURE_WEBAPP_PUBLISH_PROFILE**:
   ```bash
   az webapp deployment list-publishing-profiles \
     --name app-pulsecraft-yourname \
     --resource-group rg-pulsecraft-prod \
     --xml
   ```
   Copy the entire XML output

2. **AZURE_STATIC_WEB_APPS_API_TOKEN**:
   ```bash
   az staticwebapp secrets list \
     --name swa-pulsecraft-yourname \
     --resource-group rg-pulsecraft-prod \
     --query "properties.apiKey" -o tsv
   ```

### 2. Update Workflow File

Edit `.github/workflows/azure-deploy.yml`:

```yaml
env:
  AZURE_WEBAPP_NAME: app-pulsecraft-yourname  # Update this
```

### 3. Push to Trigger Deployment

```bash
git add .
git commit -m "Configure Azure deployment"
git push origin main
```

GitHub Actions will automatically deploy both frontend and backend!

---

## Cost Estimation

Based on the configuration in the scripts:

| Service | Tier | Estimated Cost/Month |
|---------|------|---------------------|
| App Service | B1 (Basic) | ~$13 |
| Static Web App | Free | $0 |
| Cosmos DB | 400 RU/s | ~$24 |
| Azure OpenAI | Pay-per-use | ~$10-50 (varies) |
| Service Bus | Standard | ~$10 |
| Storage Account | Standard LRS | ~$1 |
| Key Vault | Standard | ~$0.03/secret |
| Application Insights | Free tier | $0 (up to 5GB) |
| **TOTAL** | | **~$60-100/month** |

**For Hackathon/Demo**:
- Most services have free tiers or trials
- You can delete resources after demo to avoid charges
- Students get $100 Azure credits

---

## Troubleshooting

### Issue: "Name already exists"

**Solution**: Resource names must be globally unique. Update these in `azure.config.sh`:
- `APP_SERVICE_NAME`
- `STATIC_WEB_APP_NAME`
- `COSMOS_ACCOUNT_NAME`
- `OPENAI_ACCOUNT_NAME`
- `SERVICE_BUS_NAMESPACE`
- `STORAGE_ACCOUNT_NAME`
- `KEY_VAULT_NAME`

### Issue: "Azure OpenAI not available in region"

**Solution**: Azure OpenAI is available in limited regions. Try:
- `eastus`
- `westeurope`
- `southcentralus`

Update `AZURE_LOCATION` in `azure.config.sh`

### Issue: "Backend returns 502/503"

**Solutions**:
1. Check if deployment completed:
   ```bash
   az webapp show --name app-pulsecraft-yourname --resource-group rg-pulsecraft-prod --query "state"
   ```

2. View logs:
   ```bash
   az webapp log tail --name app-pulsecraft-yourname --resource-group rg-pulsecraft-prod
   ```

3. Restart app:
   ```bash
   az webapp restart --name app-pulsecraft-yourname --resource-group rg-pulsecraft-prod
   ```

### Issue: "Frontend can't connect to backend"

**Solution**: Check CORS settings in backend:
```bash
az webapp cors add \
  --name app-pulsecraft-yourname \
  --resource-group rg-pulsecraft-prod \
  --allowed-origins https://[your-frontend].azurestaticapps.net
```

### Issue: "Key Vault access denied"

**Solution**: Grant App Service access:
```bash
# Get App Service principal ID
PRINCIPAL_ID=$(az webapp identity show \
  --name app-pulsecraft-yourname \
  --resource-group rg-pulsecraft-prod \
  --query principalId -o tsv)

# Grant access to Key Vault
az keyvault set-policy \
  --name kv-pulsecraft-yourname \
  --resource-group rg-pulsecraft-prod \
  --object-id $PRINCIPAL_ID \
  --secret-permissions get list
```

---

## Cleanup (After Hackathon)

To delete all resources and stop charges:

```bash
# Delete entire resource group (WARNING: This deletes EVERYTHING)
az group delete --name rg-pulsecraft-prod --yes --no-wait

# Or delete individual resources
az webapp delete --name app-pulsecraft-yourname --resource-group rg-pulsecraft-prod
az staticwebapp delete --name swa-pulsecraft-yourname --resource-group rg-pulsecraft-prod
# ... etc
```

---

## Production Checklist

Before going to production:

- [ ] Upgrade App Service to **S1** or higher
- [ ] Enable **auto-scaling** for App Service
- [ ] Configure **custom domain** and SSL
- [ ] Set up **Azure Front Door** for CDN
- [ ] Enable **Cosmos DB backup**
- [ ] Configure **monitoring alerts** in Application Insights
- [ ] Implement **rate limiting** in API
- [ ] Enable **Azure AD authentication**
- [ ] Set up **Azure DevOps** or **GitHub Actions** for CI/CD
- [ ] Configure **staging slots** for zero-downtime deployments
- [ ] Review and optimize **Cosmos DB throughput**
- [ ] Implement **API Management** for API gateway
- [ ] Set up **Azure Monitor dashboards**

---

## Useful Azure CLI Commands

```bash
# List all resources in resource group
az resource list --resource-group rg-pulsecraft-prod --output table

# Get App Service URL
az webapp show --name app-pulsecraft-yourname --resource-group rg-pulsecraft-prod --query "defaultHostName" -o tsv

# Get Cosmos DB connection string
az cosmosdb keys list --name cosmos-pulsecraft-yourname --resource-group rg-pulsecraft-prod --type connection-strings

# Get OpenAI endpoint
az cognitiveservices account show --name openai-pulsecraft-yourname --resource-group rg-pulsecraft-prod --query "properties.endpoint" -o tsv

# View Application Insights metrics
az monitor app-insights metrics show --app appi-pulsecraft --resource-group rg-pulsecraft-prod --metric requests/count

# Scale App Service
az appservice plan update --name plan-pulsecraft-prod --resource-group rg-pulsecraft-prod --sku S1

# View costs
az consumption usage list --start-date 2025-11-01 --end-date 2025-11-30
```

---

## Support & Resources

- **Azure Documentation**: <https://docs.microsoft.com/azure/>
- **Azure OpenAI**: <https://learn.microsoft.com/azure/ai-services/openai/>
- **Static Web Apps**: <https://learn.microsoft.com/azure/static-web-apps/>
- **App Service**: <https://learn.microsoft.com/azure/app-service/>
- **Azure CLI Reference**: <https://learn.microsoft.com/cli/azure/>

---

**Questions?** Check the [troubleshooting section](#troubleshooting) or refer to `deployment-info.txt` created during deployment.

**Good luck with your hackathon! 🚀**
