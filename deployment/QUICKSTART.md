# Quick Start - Azure Deployment

## 🚀 Deploy PulseCraft to Azure in 3 Steps

### Prerequisites
- Azure account ([Get free credits](https://azure.microsoft.com/free/))
- Azure CLI installed ([Download](https://docs.microsoft.com/cli/azure/install-azure-cli))
- Logged into Azure: `az login`

---

## Option A: Bash (Linux/macOS/Git Bash on Windows)

### Step 1: Configure

```bash
cd deployment
cp azure.config.template.sh azure.config.sh
nano azure.config.sh  # or use your preferred editor
```

Update these values in `azure.config.sh`:
- `AZURE_SUBSCRIPTION_ID` - Your Azure subscription ID
- `APP_SERVICE_NAME` - Must be globally unique (e.g., `app-pulsecraft-yourname`)
- `STATIC_WEB_APP_NAME` - Must be globally unique
- Other service names to ensure uniqueness

### Step 2: Deploy Infrastructure

```bash
chmod +x deploy-azure-infrastructure.sh
./deploy-azure-infrastructure.sh
```

⏱️ **Takes ~10-15 minutes**

### Step 3: Deploy Code

```bash
# Deploy backend
chmod +x deploy-backend.sh
./deploy-backend.sh

# Deploy frontend
chmod +x deploy-frontend.sh
./deploy-frontend.sh
```

✅ **Done!** Your app is live on Azure.

---

## Option B: PowerShell (Windows)

### Step 1: Configure

```powershell
cd deployment
Copy-Item azure.config.template.ps1 azure.config.ps1
notepad azure.config.ps1  # or use VS Code
```

Update the same values as above.

### Step 2: Deploy Infrastructure

```powershell
. .\deploy.ps1
Deploy-AzureInfrastructure
```

⏱️ **Takes ~10-15 minutes**

### Step 3: Deploy Code

```powershell
Deploy-Backend
Deploy-Frontend
```

✅ **Done!** Your app is live on Azure.

---

## 📍 Access Your Deployment

After deployment completes:

**Backend API**:
```
https://app-pulsecraft-yourname.azurewebsites.net
```

**Frontend UI**:
```
https://[your-static-web-app].azurestaticapps.net
```

**Test it**:
```bash
# Test backend
curl https://app-pulsecraft-yourname.azurewebsites.net/health

# Open frontend in browser
start https://[your-static-web-app].azurestaticapps.net
```

---

## 🔄 GitHub Actions (Optional)

For automatic deployment on every push:

### 1. Get Publish Profiles

```bash
# Backend publish profile
az webapp deployment list-publishing-profiles \
  --name app-pulsecraft-yourname \
  --resource-group rg-pulsecraft-prod \
  --xml > backend-publish-profile.xml

# Frontend deployment token
az staticwebapp secrets list \
  --name swa-pulsecraft-yourname \
  --resource-group rg-pulsecraft-prod \
  --query "properties.apiKey" -o tsv
```

### 2. Add GitHub Secrets

Go to GitHub repo → Settings → Secrets → Actions

Add these secrets:
- `AZURE_WEBAPP_PUBLISH_PROFILE` - Paste contents of backend-publish-profile.xml
- `AZURE_STATIC_WEB_APPS_API_TOKEN` - Paste the deployment token

### 3. Update Workflow

Edit `.github/workflows/azure-deploy.yml`:

```yaml
env:
  AZURE_WEBAPP_NAME: app-pulsecraft-yourname  # Update this line
```

### 4. Push to Deploy

```bash
git add .
git commit -m "Configure Azure deployment"
git push origin main
```

GitHub Actions will automatically deploy! 🎉

---

## 💰 Cost Management

**Estimated Monthly Cost**: ~$60-100

### Free Tiers Available:
- Static Web Apps: Free
- Application Insights: 5GB free
- Cosmos DB: First 1000 RU/s free (limited time)

### To Minimize Costs:
1. Use B1 tier for App Service (~$13/month)
2. Set Cosmos DB to 400 RU/s minimum
3. Delete resources after demo

### To Delete Everything:

```bash
# Delete entire resource group (WARNING: Deletes ALL resources)
az group delete --name rg-pulsecraft-prod --yes --no-wait
```

---

## 🐛 Troubleshooting

### "Name already exists"
Resource names must be globally unique. Add your name/initials to the service names.

### "Backend returns 502/503"
Wait 1-2 minutes for deployment to complete, then restart:
```bash
az webapp restart --name app-pulsecraft-yourname --resource-group rg-pulsecraft-prod
```

### "Azure OpenAI not available"
Azure OpenAI is available in limited regions. Try `eastus`, `westeurope`, or `southcentralus`.

### "Frontend can't reach backend"
Check CORS settings:
```bash
az webapp cors add \
  --name app-pulsecraft-yourname \
  --resource-group rg-pulsecraft-prod \
  --allowed-origins "*"
```

---

## 📚 More Help

- **Full Documentation**: [deployment/README.md](./README.md)
- **Azure Support**: <https://docs.microsoft.com/azure/>
- **Deployment Logs**:
  ```bash
  az webapp log tail --name app-pulsecraft-yourname --resource-group rg-pulsecraft-prod
  ```

---

## ✅ Deployment Checklist

- [ ] Azure CLI installed and logged in
- [ ] Configured `azure.config.sh` or `azure.config.ps1`
- [ ] Updated all globally unique resource names
- [ ] Ran infrastructure deployment script
- [ ] Verified deployment-info.txt created
- [ ] Deployed backend successfully
- [ ] Deployed frontend successfully
- [ ] Tested backend health endpoint
- [ ] Tested frontend in browser
- [ ] Added URLs to README.md
- [ ] (Optional) Configured GitHub Actions
- [ ] (Optional) Set up custom domain

---

**Need help?** Check the [full deployment guide](./README.md) or open an issue on GitHub.

**Good luck! 🚀**
