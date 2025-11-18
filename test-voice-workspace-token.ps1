#!/usr/bin/env pwsh
# Test the alternate workspace token to find its correct host

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "🔍 Testing Voice Workspace Token" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Get the token from app.yaml (you'll need to manually extract it)
Write-Host "📝 Instructions:" -ForegroundColor Yellow
Write-Host "1. Check app.yaml for DATABRICKS_VOICE_WORKSPACE_TOKEN value"
Write-Host "2. Paste it below when prompted"
Write-Host ""

$voiceToken = Read-Host "Enter DATABRICKS_VOICE_WORKSPACE_TOKEN"

if ($voiceToken -eq "YOUR_OTHER_WORKSPACE_PAT_TOKEN_HERE" -or $voiceToken -eq "") {
    Write-Host "❌ Token not configured yet!" -ForegroundColor Red
    Write-Host ""
    Write-Host "You need to:" -ForegroundColor Yellow
    Write-Host "1. Generate PAT from the OTHER workspace (where Voice Activations Genie lives)"
    Write-Host "2. Update app.yaml with that token"
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "🔍 Testing token against different possible hosts..." -ForegroundColor Cyan
Write-Host ""

# Common Databricks workspace URL patterns
$possibleHosts = @(
    "https://dbc-4a93b454-f17b.cloud.databricks.com",  # dlk-hackathon (main workspace)
    "https://adb-XXXXXXXXX.azuredatabricks.net",       # Azure pattern (replace X with numbers)
    "https://dbc-XXXXXXXX-XXXX.cloud.databricks.com"  # AWS pattern (replace X with actual)
)

Write-Host "💡 Ask your data analyst for the workspace URL where Voice Activations Genie lives!" -ForegroundColor Yellow
Write-Host ""

$otherWorkspaceUrl = Read-Host "Enter the OTHER workspace URL (e.g., https://dbc-xxxxx.cloud.databricks.com)"

if ($otherWorkspaceUrl -eq "") {
    Write-Host "❌ No URL provided!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🧪 Testing token against: $otherWorkspaceUrl" -ForegroundColor Cyan

# Test 1: Check if token works with workspace client
Write-Host ""
Write-Host "Test 1: Workspace Info" -ForegroundColor Yellow
$env:DATABRICKS_HOST = $otherWorkspaceUrl
$env:DATABRICKS_TOKEN = $voiceToken

try {
    $result = databricks current-user me 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Token is valid for workspace: $otherWorkspaceUrl" -ForegroundColor Green
        Write-Host "User info: $result"
        
        # Test 2: Try to list Genie spaces in that workspace
        Write-Host ""
        Write-Host "Test 2: Listing Genie spaces in this workspace" -ForegroundColor Yellow
        
        # NOTE: Genie CLI commands may not exist, so we'll use API
        $headers = @{
            "Authorization" = "Bearer $voiceToken"
        }
        
        Write-Host "Checking for Genie space 01f0c3e4c6751989828598c96ee0debf..." -ForegroundColor Cyan
        
        # Try to get the specific Genie space
        $genieUrl = "$otherWorkspaceUrl/api/2.0/preview/genie/spaces/01f0c3e4c6751989828598c96ee0debf"
        
        try {
            $response = Invoke-RestMethod -Uri $genieUrl -Headers $headers -Method Get
            Write-Host "✅ Found Voice Activations Genie in this workspace!" -ForegroundColor Green
            Write-Host "Space Name: $($response.name)"
            Write-Host "Space ID: $($response.id)"
            
            Write-Host ""
            Write-Host "=====================================" -ForegroundColor Green
            Write-Host "✅ SUCCESS! Correct workspace found!" -ForegroundColor Green
            Write-Host "=====================================" -ForegroundColor Green
            Write-Host ""
            Write-Host "Update app.yaml with:" -ForegroundColor Yellow
            Write-Host "- name: DATABRICKS_VOICE_WORKSPACE_HOST" -ForegroundColor White
            Write-Host "  value: `"$otherWorkspaceUrl`"" -ForegroundColor White
            Write-Host "- name: DATABRICKS_VOICE_WORKSPACE_TOKEN" -ForegroundColor White
            Write-Host "  value: `"$voiceToken`"" -ForegroundColor White
            
        } catch {
            Write-Host "⚠️ Token is valid but couldn't find Genie 01f0c3e4c6751989828598c96ee0debf" -ForegroundColor Yellow
            Write-Host "Error: $($_.Exception.Message)"
            Write-Host ""
            Write-Host "Possible causes:" -ForegroundColor Yellow
            Write-Host "1. Genie space ID is wrong"
            Write-Host "2. Genie is in yet another workspace"
            Write-Host "3. Your user doesn't have access to that Genie"
        }
        
    } else {
        Write-Host "❌ Token is NOT valid for workspace: $otherWorkspaceUrl" -ForegroundColor Red
        Write-Host "Error: $result"
    }
} catch {
    Write-Host "❌ Error testing token: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "🔍 Summary" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To fix the cross-workspace auth, you need BOTH:" -ForegroundColor Yellow
Write-Host "1. ✅ Correct workspace URL (host)"
Write-Host "2. ✅ Valid PAT token from that workspace"
Write-Host ""
Write-Host "The code needs to be updated to support alternate HOST, not just TOKEN!" -ForegroundColor Yellow
Write-Host ""

# Cleanup
Remove-Item Env:\DATABRICKS_HOST -ErrorAction SilentlyContinue
Remove-Item Env:\DATABRICKS_TOKEN -ErrorAction SilentlyContinue

