#!/bin/bash

###############################################################################
# PulseCraft - Frontend Deployment Script
# 
# Deploys the frontend to Azure Static Web Apps
#
# Prerequisites:
# 1. Azure infrastructure deployed (run deploy-azure-infrastructure.sh first)
# 2. Azure CLI installed and logged in
# 3. Static Web Apps CLI installed (npm install -g @azure/static-web-apps-cli)
# 4. azure.config.sh configured
# 5. GitHub repository linked to Static Web App (or manual upload)
#
# Usage:
#   ./deploy-frontend.sh
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}PulseCraft - Frontend Deployment${NC}"
echo -e "${GREEN}========================================${NC}"

# Load configuration
if [ ! -f "azure.config.sh" ]; then
    echo -e "${RED}ERROR: azure.config.sh not found!${NC}"
    exit 1
fi

source azure.config.sh

# Get backend URL
BACKEND_URL="https://${APP_SERVICE_NAME}.azurewebsites.net"

echo -e "\n${YELLOW}Backend API URL: ${BACKEND_URL}${NC}"

# Navigate to frontend directory
cd ../frontend

# Update frontend .env for production
echo -e "\n${YELLOW}Configuring frontend environment...${NC}"
cat > .env.production << EOF
VITE_API_URL=${BACKEND_URL}
VITE_API_TIMEOUT=5000
EOF

echo -e "${GREEN}✓ Frontend environment configured${NC}"

# Get deployment token for Static Web App
echo -e "\n${YELLOW}Retrieving Static Web App deployment token...${NC}"
DEPLOYMENT_TOKEN=$(az staticwebapp secrets list \
    --name "$STATIC_WEB_APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "properties.apiKey" -o tsv)

if [ -z "$DEPLOYMENT_TOKEN" ]; then
    echo -e "${RED}ERROR: Could not retrieve deployment token${NC}"
    echo -e "${YELLOW}You may need to deploy via GitHub Actions instead${NC}"
    echo -e "${YELLOW}See: https://docs.microsoft.com/en-us/azure/static-web-apps/github-actions-workflow${NC}"
    exit 1
fi

# Create staticwebapp.config.json for routing
echo -e "\n${YELLOW}Creating Static Web App configuration...${NC}"
cat > public/staticwebapp.config.json << 'EOF'
{
  "routes": [
    {
      "route": "/api/*",
      "allowedRoles": ["anonymous"]
    },
    {
      "route": "/*",
      "serve": "/index.html",
      "statusCode": 200
    }
  ],
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/images/*.{png,jpg,gif}", "/css/*"]
  },
  "responseOverrides": {
    "404": {
      "rewrite": "/index.html",
      "statusCode": 200
    }
  },
  "globalHeaders": {
    "content-security-policy": "default-src 'self' https://*.azurestaticapps.net https://*.azurewebsites.net; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "mimeTypes": {
    ".json": "application/json",
    ".js": "text/javascript",
    ".css": "text/css",
    ".html": "text/html"
  }
}
EOF

# Deploy using Azure Static Web Apps CLI
echo -e "\n${YELLOW}Deploying frontend to Azure Static Web Apps...${NC}"

# Check if SWA CLI is installed
if ! command -v swa &> /dev/null; then
    echo -e "${YELLOW}Static Web Apps CLI not found. Installing...${NC}"
    npm install -g @azure/static-web-apps-cli
fi

# Deploy
swa deploy ./public \
    --deployment-token "$DEPLOYMENT_TOKEN" \
    --app-name "$STATIC_WEB_APP_NAME" \
    --env production

# Get Static Web App URL
echo -e "\n${YELLOW}Retrieving Static Web App URL...${NC}"
FRONTEND_URL=$(az staticwebapp show \
    --name "$STATIC_WEB_APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "defaultHostname" -o tsv)

if [ -n "$FRONTEND_URL" ]; then
    FRONTEND_URL="https://${FRONTEND_URL}"
    echo -e "${GREEN}✓ Frontend deployed successfully!${NC}"
    echo -e "${GREEN}Frontend URL: ${FRONTEND_URL}${NC}"
    
    # Test frontend
    echo -e "\n${YELLOW}Testing frontend...${NC}"
    sleep 5
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" || echo "000")
    
    if [ "$HTTP_CODE" == "200" ]; then
        echo -e "${GREEN}✓ Frontend is accessible!${NC}"
    else
        echo -e "${YELLOW}⚠ Frontend returned HTTP $HTTP_CODE${NC}"
        echo -e "${YELLOW}It may take a few minutes for deployment to propagate${NC}"
    fi
else
    echo -e "${RED}Could not retrieve frontend URL${NC}"
fi

cd ../deployment

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Frontend Deployment Complete${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}Frontend URL:${NC} ${FRONTEND_URL}"
echo -e "${YELLOW}Backend API:${NC} ${BACKEND_URL}"
echo -e "\n${YELLOW}Test the application:${NC}"
echo "  1. Open ${FRONTEND_URL} in your browser"
echo "  2. Enter a customer name and click 'Run Demo'"
echo "  3. Verify API calls to ${BACKEND_URL}"
echo -e "\n${YELLOW}GitHub Integration (Optional):${NC}"
echo "  Link your GitHub repo for automatic deployments:"
echo "  az staticwebapp update \\"
echo "    --name $STATIC_WEB_APP_NAME \\"
echo "    --resource-group $RESOURCE_GROUP \\"
echo "    --source https://github.com/YOUR_USERNAME/PulseCraft"
