# Azure Deployment Scripts - Overview

## 📁 Files Created

### Configuration Files
1. **azure.config.template.sh** - Bash configuration template
2. **azure.config.template.ps1** - PowerShell configuration template

### Deployment Scripts (Bash)
1. **deploy-azure-infrastructure.sh** - Main infrastructure deployment
2. **deploy-backend.sh** - Backend API deployment
3. **deploy-frontend.sh** - Frontend UI deployment

### Deployment Scripts (PowerShell)
1. **deploy.ps1** - Complete PowerShell deployment functions

### Documentation
1. **README.md** - Complete deployment guide
2. **QUICKSTART.md** - Quick 3-step deployment guide

### CI/CD Workflows
1. **.github/workflows/azure-deploy.yml** - GitHub Actions for automatic deployment
2. **.github/workflows/ci.yml** - Continuous Integration (build & test)

---

## 🚀 Quick Start

### For Bash Users (Linux/macOS/Git Bash)

```bash
cd deployment
cp azure.config.template.sh azure.config.sh
nano azure.config.sh  # Configure your values

./deploy-azure-infrastructure.sh
./deploy-backend.sh
./deploy-frontend.sh
```

### For PowerShell Users (Windows)

```powershell
cd deployment
Copy-Item azure.config.template.ps1 azure.config.ps1
notepad azure.config.ps1  # Configure your values

. .\deploy.ps1
Deploy-AzureInfrastructure
Deploy-Backend
Deploy-Frontend
```

---

## 📦 Azure Resources Created

The deployment scripts provision:

| Resource | Purpose | SKU/Tier |
|----------|---------|----------|
| Resource Group | Container for all resources | N/A |
| App Service Plan | Hosting plan for backend | B1 (Basic) |
| App Service | Backend Node.js API | Linux, Node 18 |
| Static Web App | Frontend hosting | Free |
| Cosmos DB | Database for sessions | 400 RU/s |
| Azure OpenAI | AI for scoring & composition | S0, GPT-4 |
| Service Bus | Agent messaging queues | Standard |
| Storage Account | Blob storage | Standard LRS |
| Key Vault | Secrets management | Standard |
| Application Insights | Monitoring & telemetry | Free tier |

---

## 💰 Estimated Costs

**Total**: ~$60-100/month

- App Service (B1): ~$13/month
- Cosmos DB (400 RU/s): ~$24/month
- Azure OpenAI: ~$10-50/month (usage-based)
- Service Bus: ~$10/month
- Storage: ~$1/month
- Other services: Free tiers available

**For Hackathon**: Most services have free trials or student credits available.

---

## 🔐 Security Features

All scripts implement security best practices:

- ✅ Secrets stored in Azure Key Vault (never in code)
- ✅ App Service Managed Identity for Key Vault access
- ✅ Environment variables via Key Vault references
- ✅ HTTPS enforced for all endpoints
- ✅ CORS configured for frontend domain
- ✅ Security headers in Static Web App config

---

## 🛠️ What Each Script Does

### deploy-azure-infrastructure.sh
- Creates all Azure resources
- Configures networking and security
- Stores secrets in Key Vault
- Grants App Service access to Key Vault
- Outputs deployment summary

### deploy-backend.sh
- Installs backend dependencies
- Creates deployment ZIP package
- Deploys to Azure App Service
- Tests health endpoint
- Displays API URLs

### deploy-frontend.sh
- Configures frontend environment
- Creates Static Web App config
- Deploys to Azure Static Web Apps
- Tests frontend accessibility
- Shows frontend URL

---

## 🔄 CI/CD with GitHub Actions

The `.github/workflows/azure-deploy.yml` workflow:

- **Triggers**: On push to `main` or pull requests
- **Backend Job**:
  - Installs Node.js dependencies
  - Runs tests (if available)
  - Creates deployment package
  - Deploys to Azure App Service
  - Tests deployment
- **Frontend Job**:
  - Builds frontend (if needed)
  - Deploys to Azure Static Web Apps
  - Waits for backend to complete

---

## 📊 Monitoring & Logs

### View Backend Logs

```bash
az webapp log tail \
  --name app-pulsecraft-yourname \
  --resource-group rg-pulsecraft-prod
```

### View Application Insights

```bash
az monitor app-insights component show \
  --app appi-pulsecraft \
  --resource-group rg-pulsecraft-prod
```

### Check Deployment Status

```bash
az webapp deployment list \
  --name app-pulsecraft-yourname \
  --resource-group rg-pulsecraft-prod
```

---

## 🧹 Cleanup

To delete all resources and stop charges:

```bash
# WARNING: This deletes EVERYTHING
az group delete --name rg-pulsecraft-prod --yes --no-wait
```

Or delete resources individually:

```bash
az webapp delete --name app-pulsecraft-yourname --resource-group rg-pulsecraft-prod
az staticwebapp delete --name swa-pulsecraft-yourname --resource-group rg-pulsecraft-prod
# etc.
```

---

## 🐛 Common Issues

### "Resource name already exists"
All service names must be globally unique. Add your username/initials to the names in `azure.config.sh`

### "Azure OpenAI not available in region"
Try these regions: `eastus`, `westeurope`, `southcentralus`

### "Backend returns 502/503"
Wait 1-2 minutes for deployment to complete, then restart the app

### "Frontend can't connect to backend"
Configure CORS to allow your Static Web App domain

### "Key Vault access denied"
Ensure App Service Managed Identity is enabled and has Key Vault permissions

---

## 📚 Further Reading

- [Full Deployment Guide](./README.md)
- [Quick Start Guide](./QUICKSTART.md)
- [Azure Documentation](https://docs.microsoft.com/azure/)
- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Static Web Apps Documentation](https://learn.microsoft.com/azure/static-web-apps/)

---

## ✅ Deployment Checklist

Before deploying:
- [ ] Azure CLI installed (`az --version`)
- [ ] Logged into Azure (`az login`)
- [ ] Subscription selected (`az account show`)
- [ ] Configured `azure.config.sh` or `azure.config.ps1`
- [ ] All resource names are globally unique
- [ ] Preferred Azure region supports all services

After deploying:
- [ ] Backend API accessible at `https://app-pulsecraft-yourname.azurewebsites.net/health`
- [ ] Frontend UI loads at Static Web App URL
- [ ] Can create sessions from frontend
- [ ] Application Insights receiving telemetry
- [ ] Secrets stored in Key Vault
- [ ] URLs added to README.md
- [ ] (Optional) GitHub Actions configured

---

**Questions?** See the [troubleshooting section](./README.md#troubleshooting) or check deployment logs.

**Good luck with your deployment! 🚀**
