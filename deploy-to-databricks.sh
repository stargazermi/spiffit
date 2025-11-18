#!/bin/bash
# Databricks App Deployment Script
# Restarts Databricks App (pulls latest code from Git automatically)

# Configuration
PROFILE="${1:-dlk-hackathon}"
APP_NAME="${2:-spiffit-mocking-bird}"
REPO_ID="${3:-2435542458835487}"
REPO_BRANCH="${4:-spiffit-dev}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}🚀 Databricks App Deployment Script${NC}"
echo -e "${CYAN}=====================================${NC}"
echo ""
echo -e "${YELLOW}⚠️  Make sure you've pushed your latest changes to GitHub first!${NC}"
echo ""

read -p "❓ Ready to redeploy the app? (y/n): " continue
if [ "$continue" != "y" ]; then
    echo -e "${RED}❌ Deployment cancelled${NC}"
    exit 0
fi

# Step 1: Pull latest code to Databricks Git Folder
echo -e "\n${GREEN}📥 Step 1: Updating Databricks Git Folder...${NC}"
echo -e "   ${CYAN}Repo ID: $REPO_ID${NC}"
echo -e "   ${CYAN}Branch: $REPO_BRANCH${NC}"

# Update repo to latest from GitHub
echo -e "   ${CYAN}🔄 Pulling latest from GitHub...${NC}"
databricks repos update "$REPO_ID" --branch "$REPO_BRANCH" --profile "$PROFILE"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to update Git Folder!${NC}"
    echo -e "   ${YELLOW}💡 Verify Repo ID and branch name are correct${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Git Folder updated with latest code!${NC}"

# Step 2: Get App ID
echo -e "\n${GREEN}🔍 Finding Databricks App...${NC}"
app_list=$(databricks apps list --profile "$PROFILE" --output json 2>&1)

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to list apps. Error:${NC}"
    echo "$app_list"
    echo -e "\n${YELLOW}💡 Make sure you're authenticated:${NC}"
    echo -e "   ${CYAN}databricks auth login --profile $PROFILE${NC}"
    exit 1
fi

# Parse JSON to find app (using jq if available, otherwise grep)
if command -v jq &> /dev/null; then
    app_url=$(echo "$app_list" | jq -r ".[] | select(.name == \"$APP_NAME\") | .url")
else
    # Fallback without jq
    app_url=$(echo "$app_list" | grep -A 5 "\"$APP_NAME\"" | grep "url" | cut -d'"' -f4)
fi

if [ -z "$app_url" ]; then
    echo -e "${RED}❌ App '$APP_NAME' not found!${NC}"
    echo -e "\n${YELLOW}📋 Available apps:${NC}"
    echo "$app_list" | grep "name" | cut -d'"' -f4 | sed 's/^/   - /'
    exit 1
fi

echo -e "${GREEN}✅ Found app: $APP_NAME${NC}"
echo -e "   ${CYAN}URL: $app_url${NC}"

# Step 3: Deploy the app (restart to pick up changes from Git Folder)
echo -e "\n${GREEN}🔄 Step 3: Deploying app...${NC}"
echo -e "   ${CYAN}🔄 Restarting app to pick up latest code...${NC}"

databricks apps deploy "$APP_NAME" --profile "$PROFILE"

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}❌ Deploy failed! Trying restart instead...${NC}"
    
    # Fallback: restart command
    databricks apps restart "$APP_NAME" --profile "$PROFILE"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Restart also failed!${NC}"
        exit 1
    fi
fi

# Step 4: Monitor deployment
echo -e "\n${YELLOW}⏳ Step 4: Monitoring deployment (this takes ~2-3 minutes)...${NC}"
echo -e "   ${GRAY}Press Ctrl+C to stop monitoring (app will continue deploying)${NC}"
echo ""

max_attempts=40  # ~2 minutes
attempt=0

while [ $attempt -lt $max_attempts ]; do
    attempt=$((attempt + 1))
    sleep 3
    
    app_status=$(databricks apps get "$APP_NAME" --profile "$PROFILE" --output json 2>&1)
    
    if [ $? -eq 0 ]; then
        if command -v jq &> /dev/null; then
            state=$(echo "$app_status" | jq -r '.state.value')
        else
            state=$(echo "$app_status" | grep -o '"value":"[^"]*"' | head -1 | cut -d'"' -f4)
        fi
        
        echo -e "   ${CYAN}[$attempt/$max_attempts] State: $state${NC}"
        
        if [ "$state" == "RUNNING" ]; then
            echo -e "\n${GREEN}✅ App is RUNNING!${NC}"
            echo -e "${CYAN}🌐 URL: $app_url${NC}"
            echo ""
            echo -e "${YELLOW}🔧 Verify deployment:${NC}"
            echo -e "   ${GRAY}1. Open the app in your browser${NC}"
            echo -e "   ${GRAY}2. Go to 🔧 Troubleshooting tab${NC}"
            echo -e "   ${GRAY}3. Check version (should be v1.3.2)${NC}"
            echo -e "   ${GRAY}4. Check timestamp (should be recent)${NC}"
            echo ""
            exit 0
        fi
        
        if [ "$state" == "ERROR" ] || [ "$state" == "CRASHED" ]; then
            echo -e "\n${RED}❌ App deployment failed!${NC}"
            echo -e "${YELLOW}🔍 Check logs in Databricks UI:${NC}"
            echo -e "   ${CYAN}Compute > Apps > $APP_NAME > Logs${NC}"
            exit 1
        fi
    fi
done

echo -e "\n${YELLOW}⚠️  Deployment is taking longer than expected${NC}"
echo -e "   ${GRAY}The app is still deploying in the background.${NC}"
echo -e "   ${CYAN}Check status in Databricks UI: Compute > Apps > $APP_NAME${NC}"

