#!/usr/bin/env pwsh
<#
.SYNOPSIS
    List all available serving endpoints in Databricks workspace
.DESCRIPTION
    Uses Databricks CLI to query available serving endpoints for the orchestrator model
#>

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "🔍 Listing Databricks Serving Endpoints" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    # Check Databricks CLI is installed
    $cliVersion = databricks --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Databricks CLI not found!" -ForegroundColor Red
        Write-Host "Install: pip install databricks-cli" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✅ Databricks CLI: $cliVersion" -ForegroundColor Green
    
    # Get current profile
    $profile = $env:DATABRICKS_PROFILE
    if (-not $profile) {
        $profile = "dlk-hackathon"
        Write-Host "ℹ️  Using default profile: $profile" -ForegroundColor Yellow
    } else {
        Write-Host "ℹ️  Using profile: $profile" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "📡 Fetching serving endpoints..." -ForegroundColor Cyan
    
    # List serving endpoints
    $endpoints = databricks serving-endpoints list --profile $profile --output json 2>&1 | ConvertFrom-Json
    
    if ($endpoints -and $endpoints.Count -gt 0) {
        Write-Host ""
        Write-Host "✅ Found $($endpoints.Count) serving endpoint(s):" -ForegroundColor Green
        Write-Host ""
        
        foreach ($endpoint in $endpoints) {
            $name = $endpoint.name
            $state = if ($endpoint.state.ready) { $endpoint.state.ready } else { $endpoint.state.config_update }
            
            # Safely get model info
            $model = $null
            $workload = $null
            if ($endpoint.config.served_models -and $endpoint.config.served_models.Count -gt 0) {
                $model = $endpoint.config.served_models[0].model_name
                $workload = $endpoint.config.served_models[0].workload_size
            }
            
            Write-Host "  📦 Endpoint: $name" -ForegroundColor White
            if ($state) {
                Write-Host "     Status: $state" -ForegroundColor $(if ($state -eq "READY") { "Green" } else { "Yellow" })
            }
            if ($model) {
                Write-Host "     Model: $model" -ForegroundColor Cyan
            }
            if ($workload) {
                Write-Host "     Workload: $workload" -ForegroundColor Gray
            }
            Write-Host ""
        }
        
        # Show which are usable for orchestrator
        Write-Host "💡 Models suitable for orchestrator (smart routing):" -ForegroundColor Magenta
        $foundationModels = $endpoints | Where-Object { 
            $_.name -like "*llama*" -or 
            $_.name -like "*gpt*" -or 
            $_.name -like "*claude*" -or 
            $_.name -like "*dbrx*" -or
            $_.name -like "*mistral*" -or
            $_.name -like "*mixtral*"
        }
        
        if ($foundationModels) {
            foreach ($fm in $foundationModels) {
                Write-Host "   ✅ $($fm.name)" -ForegroundColor Green
            }
        } else {
            Write-Host "   ⚠️  No foundation models found" -ForegroundColor Yellow
            Write-Host "   Tip: Check if Foundation Model endpoints are enabled in your workspace" -ForegroundColor Gray
        }
        
    } else {
        Write-Host "⚠️  No serving endpoints found" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "💡 Possible reasons:" -ForegroundColor Cyan
        Write-Host "   1. No serving endpoints created yet" -ForegroundColor Gray
        Write-Host "   2. Permission issue - check your user permissions" -ForegroundColor Gray
        Write-Host "   3. Foundation Model API may not be enabled" -ForegroundColor Gray
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Troubleshooting:" -ForegroundColor Cyan
    Write-Host "   1. Check authentication: databricks auth login --profile dlk-hackathon" -ForegroundColor Gray
    Write-Host "   2. Verify workspace access" -ForegroundColor Gray
    Write-Host "   3. Check permissions for serving endpoints" -ForegroundColor Gray
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎸 Spiff It Good! 🎸" -ForegroundColor Magenta
Write-Host ""

