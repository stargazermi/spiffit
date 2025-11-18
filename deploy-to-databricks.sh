#!/bin/bash
# Databricks App Deployment Script
# Pushes latest code to Git and restarts Databricks App

# Configuration
COMMIT_MESSAGE="${1:-Update app}"
PROFILE="${2:-dlk-hackathon}"
APP_NAME="${3:-spiffit-mocking-bird}"

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

# Step 1: Git Status
echo -e "${GREEN}📊 Checking Git status...${NC}"
git status --short
echo ""

read -p "❓ Do you want to commit and push these changes? (y/n): " continue
if [ "$continue" != "y" ]; then
    echo -e "${RED}❌ Deployment cancelled${NC}"
    exit 0
fi

# Step 2: Git Add
echo -e "\n${GREEN}📦 Staging files...${NC}"
git add streamlit/spiffit-ai-calculator/

# Step 3: Git Commit
echo -e "\n${GREEN}💾 Committing changes...${NC}"
git commit -m "$COMMIT_MESSAGE"

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  No changes to commit or commit failed${NC}"
    read -p "Continue anyway? (y/n): " skip_push
    if [ "$skip_push" != "y" ]; then
        exit 1
    fi
fi

# Step 4: Git Push
echo -e "\n${GREEN}⬆️  Pushing to GitHub...${NC}"
git push origin main

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Git push failed!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"

# Step 5: Wait for GitHub sync
echo -e "\n${YELLOW}⏳ Waiting 5 seconds for GitHub to sync...${NC}"
sleep 5

# Step 6: Get App ID
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
    app_url=$(echo "$app_list" | jq -r ".apps[] | select(.name == \"$APP_NAME\") | .url")
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

# Step 7: Stop the app
echo -e "\n${GREEN}⏸️  Stopping app...${NC}"
databricks apps stop "$APP_NAME" --profile "$PROFILE"

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Stop command failed (app might already be stopped)${NC}"
fi

echo -e "${YELLOW}⏳ Waiting 3 seconds...${NC}"
sleep 3

# Step 8: Start the app
echo -e "\n${GREEN}▶️  Starting app (this will pull latest code from Git)...${NC}"
databricks apps start "$APP_NAME" --profile "$PROFILE"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to start app!${NC}"
    exit 1
fi

# Step 9: Monitor deployment
echo -e "\n${YELLOW}⏳ Monitoring deployment (this takes ~2-3 minutes)...${NC}"
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

