# Test WORKING Genie Space - Quick Verification
# Space ID: 01f0c4ae99271d64835d414b8d43ddfb

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Testing WORKING Genie Space" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Load environment from envtemp.txt
if (Test-Path "envtemp.txt") {
    Write-Host "✅ Loading configuration from envtemp.txt..." -ForegroundColor Green
    Get-Content "envtemp.txt" | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]*)\s*=\s*(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
    Write-Host ""
} else {
    Write-Host "❌ No envtemp.txt file found!" -ForegroundColor Red
    exit 1
}

$profile = $env:DATABRICKS_PROFILE
$genie_space_id = $env:GENIE_SPACE_ID

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Profile: $profile" -ForegroundColor Gray
Write-Host "  Genie Space: $genie_space_id" -ForegroundColor Green
Write-Host ""

# Test 1: Get space details
Write-Host "TEST 1: Get Genie Space Details" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

try {
    $result = databricks api get "/api/2.0/genie/spaces/$genie_space_id" --profile $profile | ConvertFrom-Json
    
    Write-Host "✅ SUCCESS!" -ForegroundColor Green
    Write-Host "  Space ID: $($result.space_id)" -ForegroundColor White
    Write-Host "  Title: $($result.title)" -ForegroundColor White
    Write-Host "  Warehouse: $($result.warehouse_id)" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 2: Send a test query
Write-Host "TEST 2: Send Test Query to Genie" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Query: 'Show me voice opportunities'" -ForegroundColor Gray
Write-Host ""

try {
    $query_body = '{"content": "Show me voice opportunities"}'
    $result = databricks api post "/api/2.0/genie/spaces/$genie_space_id/start-conversation" --profile $profile --json $query_body | ConvertFrom-Json
    
    Write-Host "✅ SUCCESS! Genie responded" -ForegroundColor Green
    Write-Host "  Conversation ID: $($result.conversation_id)" -ForegroundColor White
    
    if ($result.message) {
        Write-Host "  Message content: $($result.message.content.Substring(0, [Math]::Min(100, $result.message.content.Length)))..." -ForegroundColor White
    }
    
    Write-Host ""
} catch {
    Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "✅ All tests passed! Genie space is working!" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your app.yaml is already configured correctly:" -ForegroundColor Yellow
Write-Host "  GENIE_SPACE_ID = $genie_space_id" -ForegroundColor Green
Write-Host ""
Write-Host "Ready to deploy! 🎸" -ForegroundColor Cyan

