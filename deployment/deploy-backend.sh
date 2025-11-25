#!/bin/bash

###############################################################################
# PulseCraft - Backend Deployment Script
# 
# Deploys the Node.js backend to Azure App Service
#
# Prerequisites:
# 1. Azure infrastructure deployed (run deploy-azure-infrastructure.sh first)
# 2. Azure CLI installed and logged in
# 3. azure.config.sh configured
#
# Usage:
#   ./deploy-backend.sh
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}PulseCraft - Backend Deployment${NC}"
echo -e "${GREEN}========================================${NC}"

# Load configuration
if [ ! -f "azure.config.sh" ]; then
    echo -e "${RED}ERROR: azure.config.sh not found!${NC}"
    exit 1
fi

source azure.config.sh

# Navigate to backend directory
cd ../backend

# Install dependencies
echo -e "\n${YELLOW}Installing backend dependencies...${NC}"
npm install --production

# Create deployment package
echo -e "\n${YELLOW}Creating deployment package...${NC}"
zip -r ../deployment/backend-deploy.zip . \
    -x "node_modules/*" \
    -x ".env*" \
    -x "data/*" \
    -x "*.log"

cd ../deployment

# Deploy to Azure App Service
echo -e "\n${YELLOW}Deploying to Azure App Service...${NC}"
az webapp deployment source config-zip \
    --resource-group "$RESOURCE_GROUP" \
    --name "$APP_SERVICE_NAME" \
    --src backend-deploy.zip

# Wait for deployment
echo -e "\n${YELLOW}Waiting for deployment to complete...${NC}"
sleep 10

# Test deployment
echo -e "\n${YELLOW}Testing deployment...${NC}"
BACKEND_URL="https://${APP_SERVICE_NAME}.azurewebsites.net"

echo "Testing health endpoint: ${BACKEND_URL}/health"
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "${BACKEND_URL}/health" || echo "000")
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n1)

if [ "$HTTP_CODE" == "200" ]; then
    echo -e "${GREEN}✓ Backend deployment successful!${NC}"
    echo -e "${GREEN}Backend is running at: ${BACKEND_URL}${NC}"
else
    echo -e "${RED}✗ Backend health check failed (HTTP $HTTP_CODE)${NC}"
    echo "Response: $HEALTH_RESPONSE"
    echo -e "${YELLOW}Check logs: az webapp log tail --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP${NC}"
fi

# Clean up
rm -f backend-deploy.zip

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Backend Deployment Complete${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}Backend URL:${NC} ${BACKEND_URL}"
echo -e "${YELLOW}Health Check:${NC} ${BACKEND_URL}/health"
echo -e "${YELLOW}API Endpoints:${NC}"
echo "  POST ${BACKEND_URL}/api/demo/run"
echo "  GET  ${BACKEND_URL}/api/demo/list"
echo "  GET  ${BACKEND_URL}/api/demo/replay/:id"
echo -e "\n${YELLOW}View logs:${NC}"
echo "  az webapp log tail --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP"
echo -e "\n${YELLOW}Next step:${NC} Deploy frontend with ./deploy-frontend.sh"
