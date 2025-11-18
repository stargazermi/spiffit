#!/usr/bin/env pwsh
# Test if the main workspace PAT token is valid

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🔍 Testing Main Workspace PAT Token" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Get the token from app.yaml
Write-Host "Reading token from app.yaml..." -ForegroundColor Yellow
$appYamlPath = "streamlit\spiffit-ai-calculator\app.yaml"
$appYamlContent = Get-Content $appYamlPath -Raw

# Extract token (line 45)
if ($appYamlContent -match 'value: "(dapi[^"]+)"') {
    $token = $matches[1]
    Write-Host "✅ Found token in app.yaml: ***$($token.Substring($token.Length - 4))" -ForegroundColor Green
} else {
    Write-Host "❌ Could not find token in app.yaml!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Testing token against dlk-hackathon workspace..." -ForegroundColor Cyan
$host_url = "https://dbc-4a93b454-f17b.cloud.databricks.com"

# Set environment variables
$env:DATABRICKS_HOST = $host_url
$env:DATABRICKS_TOKEN = $token

Write-Host "  Host: $host_url" -ForegroundColor Gray
Write-Host "  Token: ***$($token.Substring($token.Length - 4))" -ForegroundColor Gray
Write-Host ""

# Test 1: Get current user
Write-Host "Test 1: Verify token with 'current-user me'..." -ForegroundColor Yellow
try {
    $result = databricks current-user me 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Token is VALID!" -ForegroundColor Green
        Write-Host "User: $result" -ForegroundColor Gray
        $tokenValid = $true
    } else {
        Write-Host "❌ Token is INVALID or EXPIRED!" -ForegroundColor Red
        Write-Host "Error: $result" -ForegroundColor Red
        $tokenValid = $false
    }
} catch {
    Write-Host "❌ Error testing token: $($_.Exception.Message)" -ForegroundColor Red
    $tokenValid = $false
}

Write-Host ""

if ($tokenValid) {
    # Test 2: Try to access a Genie space
    Write-Host "Test 2: Check if token can access Genie spaces..." -ForegroundColor Yellow
    $genieSpaceId = "01f0c404048613b3b494b1a64a1bca84" # Analytics Genie
    
    try {
        $headers = @{
            "Authorization" = "Bearer $token"
        }
        $genieUrl = "$host_url/api/2.0/preview/genie/spaces/$genieSpaceId"
        
        $response = Invoke-RestMethod -Uri $genieUrl -Headers $headers -Method Get -ErrorAction Stop
        
        Write-Host "✅ Token can access Genie spaces!" -ForegroundColor Green
        Write-Host "Space Name: $($response.name)" -ForegroundColor Gray
        
    } catch {
        Write-Host "❌ Token cannot access Genie spaces!" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        
        if ($_.Exception.Response.StatusCode -eq 401) {
            Write-Host ""
            Write-Host "⚠️  Token is invalid or doesn't have Genie permissions!" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Red
    Write-Host "❌ TOKEN IS INVALID!" -ForegroundColor Red
    Write-Host "=========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "The PAT token in app.yaml has expired or is invalid." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To fix:" -ForegroundColor Yellow
    Write-Host "1. Generate a new PAT token in Databricks UI:" -ForegroundColor White
    Write-Host "   User Settings → Developer → Access Tokens → Generate New Token" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Update app.yaml line 45:" -ForegroundColor White
    Write-Host "   value: `"YOUR_NEW_TOKEN`"" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Redeploy:" -ForegroundColor White
    Write-Host "   .\deploy-to-databricks.ps1" -ForegroundColor White
    Write-Host ""
}

# Cleanup
Remove-Item Env:\DATABRICKS_HOST -ErrorAction SilentlyContinue
Remove-Item Env:\DATABRICKS_TOKEN -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Test Complete" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan


