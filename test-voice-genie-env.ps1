#!/usr/bin/env pwsh
# Test Voice Activations Genie cross-workspace environment setup

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🔍 Voice Genie Environment Test" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$appName = "spiffit-mocking-bird"
$profile = "dlk-hackathon"

# Set profile
Write-Host "📋 Using profile: $profile" -ForegroundColor Yellow
$env:DATABRICKS_CONFIG_PROFILE = $profile

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 1: Check App Exists" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$appInfo = databricks apps get $appName --output json 2>&1 | ConvertFrom-Json
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ App found: $appName" -ForegroundColor Green
    Write-Host "   Status: $($appInfo.status.state)" -ForegroundColor Gray
    Write-Host "   URL: $($appInfo.url)" -ForegroundColor Gray
} else {
    Write-Host "❌ App not found: $appName" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 2: Check App Environment Variables" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Get app config
$appConfig = databricks apps get $appName --output json 2>&1 | ConvertFrom-Json

if ($appConfig.config.env) {
    Write-Host "🔍 Environment Variables in app.yaml:" -ForegroundColor Yellow
    Write-Host ""
    
    # Check for Voice Activations specific vars
    $hasVoiceHost = $false
    $hasVoiceToken = $false
    $hasVoiceSpaceId = $false
    $voiceHostValue = ""
    
    foreach ($envVar in $appConfig.config.env) {
        $name = $envVar.name
        $value = $envVar.value
        
        # Check Voice Activations variables
        if ($name -eq "DATABRICKS_VOICE_WORKSPACE_HOST") {
            $hasVoiceHost = $true
            $voiceHostValue = $value
            if ($value -like "*40f40c74-254e*") {
                Write-Host "   ✅ DATABRICKS_VOICE_WORKSPACE_HOST: $value" -ForegroundColor Green
            } elseif ($value -like "*YOUR_OTHER_WORKSPACE*" -or $value -eq "") {
                Write-Host "   ❌ DATABRICKS_VOICE_WORKSPACE_HOST: NOT CONFIGURED (placeholder)" -ForegroundColor Red
            } else {
                Write-Host "   ⚠️  DATABRICKS_VOICE_WORKSPACE_HOST: $value (unexpected workspace)" -ForegroundColor Yellow
            }
        }
        elseif ($name -eq "DATABRICKS_VOICE_WORKSPACE_TOKEN") {
            $hasVoiceToken = $true
            if ($value -like "dapi_*") {
                Write-Host "   ✅ DATABRICKS_VOICE_WORKSPACE_TOKEN: ***$($value.Substring($value.Length - 4))" -ForegroundColor Green
            } elseif ($value -like "*YOUR_OTHER_WORKSPACE*" -or $value -eq "") {
                Write-Host "   ❌ DATABRICKS_VOICE_WORKSPACE_TOKEN: NOT CONFIGURED (placeholder)" -ForegroundColor Red
            } else {
                Write-Host "   ⚠️  DATABRICKS_VOICE_WORKSPACE_TOKEN: ???" -ForegroundColor Yellow
            }
        }
        elseif ($name -eq "GENIE_VOICE_ACTIVATIONS_SPACE_ID") {
            $hasVoiceSpaceId = $true
            if ($value -eq "01f0c3e4c6751989828598c96ee0debf") {
                Write-Host "   ✅ GENIE_VOICE_ACTIVATIONS_SPACE_ID: $value" -ForegroundColor Green
            } else {
                Write-Host "   ⚠️  GENIE_VOICE_ACTIVATIONS_SPACE_ID: $value (unexpected)" -ForegroundColor Yellow
            }
        }
        elseif ($name -eq "DATABRICKS_HOST") {
            Write-Host "   📍 DATABRICKS_HOST (main): $value" -ForegroundColor Gray
        }
        elseif ($name -eq "DATABRICKS_TOKEN") {
            Write-Host "   📍 DATABRICKS_TOKEN (main): ***$($value.Substring($value.Length - 4))" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
    Write-Host "📊 Voice Activations Config Status:" -ForegroundColor Yellow
    Write-Host "   VOICE_WORKSPACE_HOST: $(if ($hasVoiceHost) { '✅' } else { '❌ MISSING' })" -ForegroundColor $(if ($hasVoiceHost) { 'Green' } else { 'Red' })
    Write-Host "   VOICE_WORKSPACE_TOKEN: $(if ($hasVoiceToken) { '✅' } else { '❌ MISSING' })" -ForegroundColor $(if ($hasVoiceToken) { 'Green' } else { 'Red' })
    Write-Host "   VOICE_ACTIVATIONS_SPACE_ID: $(if ($hasVoiceSpaceId) { '✅' } else { '❌ MISSING' })" -ForegroundColor $(if ($hasVoiceSpaceId) { 'Green' } else { 'Red' })
    
    if (!$hasVoiceHost -or !$hasVoiceToken -or !$hasVoiceSpaceId) {
        Write-Host ""
        Write-Host "❌ Voice Activations environment variables are NOT configured!" -ForegroundColor Red
        Write-Host ""
        Write-Host "To fix:" -ForegroundColor Yellow
        Write-Host "1. Edit app.yaml in Databricks Git Folder"
        Write-Host "2. Add these values:"
        Write-Host "   - DATABRICKS_VOICE_WORKSPACE_HOST: https://dbc-40f40c74-254e.cloud.databricks.com"
        Write-Host "   - DATABRICKS_VOICE_WORKSPACE_TOKEN: <your PAT token from that workspace>"
        Write-Host "   - GENIE_VOICE_ACTIVATIONS_SPACE_ID: 01f0c3e4c6751989828598c96ee0debf"
        Write-Host "3. Run: .\deploy-to-databricks.ps1"
        Write-Host ""
        exit 1
    }
    
} else {
    Write-Host "⚠️  No environment variables found in app config" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 3: Test Alternate Workspace Access" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Prompt for alternate workspace credentials to test
Write-Host "To test the alternate workspace, enter credentials:" -ForegroundColor Yellow
$altHost = Read-Host "Alternate workspace URL (or press Enter to use: https://dbc-40f40c74-254e.cloud.databricks.com)"
if ($altHost -eq "") {
    $altHost = "https://dbc-40f40c74-254e.cloud.databricks.com"
}

$altToken = Read-Host "Alternate workspace PAT token (starts with dapi_)"

if ($altToken -eq "" -or $altToken -like "*YOUR_OTHER*") {
    Write-Host ""
    Write-Host "⚠️  No token provided, skipping alternate workspace test" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "🧪 Testing alternate workspace access..." -ForegroundColor Cyan
    
    # Set alternate workspace credentials
    $env:DATABRICKS_HOST = $altHost
    $env:DATABRICKS_TOKEN = $altToken
    
    # Test 1: Get current user
    Write-Host ""
    Write-Host "Test 1: Verify token works with workspace..." -ForegroundColor Yellow
    try {
        $user = databricks current-user me 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ Token is valid for workspace: $altHost" -ForegroundColor Green
            Write-Host "   User: $user" -ForegroundColor Gray
        } else {
            Write-Host "   ❌ Token is NOT valid for workspace: $altHost" -ForegroundColor Red
            Write-Host "   Error: $user" -ForegroundColor Red
        }
    } catch {
        Write-Host "   ❌ Failed to verify token: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Test 2: Check Genie space access via API
    Write-Host ""
    Write-Host "Test 2: Check Voice Activations Genie access..." -ForegroundColor Yellow
    $genieSpaceId = "01f0c3e4c6751989828598c96ee0debf"
    
    try {
        $headers = @{
            "Authorization" = "Bearer $altToken"
        }
        $genieUrl = "$altHost/api/2.0/preview/genie/spaces/$genieSpaceId"
        
        $response = Invoke-RestMethod -Uri $genieUrl -Headers $headers -Method Get
        
        Write-Host "   ✅ Voice Activations Genie found!" -ForegroundColor Green
        Write-Host "   Space Name: $($response.name)" -ForegroundColor Gray
        Write-Host "   Space ID: $($response.id)" -ForegroundColor Gray
        Write-Host "   Description: $($response.description)" -ForegroundColor Gray
        
    } catch {
        Write-Host "   ❌ Cannot access Voice Activations Genie" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        
        if ($_.Exception.Response.StatusCode -eq 404) {
            Write-Host ""
            Write-Host "   Possible causes:" -ForegroundColor Yellow
            Write-Host "   - Genie space ID is wrong"
            Write-Host "   - Genie is in a different workspace"
            Write-Host "   - Your user doesn't have access"
        } elseif ($_.Exception.Response.StatusCode -eq 401) {
            Write-Host ""
            Write-Host "   Token is invalid or expired!" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Step 4: Compare Workspaces" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📊 Workspace Comparison:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Main Workspace (dlk-hackathon):"
Write-Host "   └─ URL: https://dbc-4a93b454-f17b.cloud.databricks.com" -ForegroundColor Gray
Write-Host "   └─ Contains: Sales, Analytics, Market Genies (mock data)"
Write-Host ""
Write-Host "   Alternate Workspace (Voice Activations):"
Write-Host "   └─ URL: https://dbc-40f40c74-254e.cloud.databricks.com" -ForegroundColor Gray
Write-Host "   └─ Contains: Voice Activations Genie (01f0c3e4...)"
Write-Host "   └─ Has VOIP/MRR data"
Write-Host ""

if ($voiceHostValue -like "*40f40c74-254e*") {
    Write-Host "✅ App is configured to use the correct alternate workspace!" -ForegroundColor Green
} elseif ($voiceHostValue -like "*4a93b454-f17b*") {
    Write-Host "❌ App is configured to use the MAIN workspace (wrong!)" -ForegroundColor Red
} else {
    Write-Host "❌ App's alternate workspace URL doesn't match expected value!" -ForegroundColor Red
    Write-Host "   Expected: https://dbc-40f40c74-254e.cloud.databricks.com" -ForegroundColor Yellow
    Write-Host "   Found: $voiceHostValue" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "✅ Environment Test Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

Write-Host "📋 Summary:" -ForegroundColor Yellow
Write-Host "1. App environment variables: $(if ($hasVoiceHost -and $hasVoiceToken) { '✅ Configured' } else { '❌ Missing' })"
Write-Host "2. Alternate workspace: $(if ($voiceHostValue -like '*40f40c74-254e*') { '✅ Correct' } else { '❌ Wrong/Missing' })"
Write-Host "3. Next step: $(if ($hasVoiceHost -and $hasVoiceToken -and $voiceHostValue -like '*40f40c74-254e*') { 'Test Voice Activations button in app!' } else { 'Update app.yaml and redeploy' })"
Write-Host ""

# Cleanup
Remove-Item Env:\DATABRICKS_HOST -ErrorAction SilentlyContinue
Remove-Item Env:\DATABRICKS_TOKEN -ErrorAction SilentlyContinue
Remove-Item Env:\DATABRICKS_CONFIG_PROFILE -ErrorAction SilentlyContinue

