# Test if the NEW Genie space exists using the PAT token from app.yaml

$host_url = "https://dbc-4a93b454-f17b.cloud.databricks.com"
$token = "dapi5e40d9eb65d1af6c91866e0a35c4"  # From app.yaml line 46
$new_space_id = "0110c4ae99271d64835d414b8d43ddfb"
$old_space_id = "01f0c4ae99271d64835d414b8d43ddfb"

Write-Host "Testing both Genie spaces with PAT token..." -ForegroundColor Cyan
Write-Host ""

# Test OLD space
Write-Host "Testing OLD space: $old_space_id" -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
    }
    $result = Invoke-RestMethod -Uri "$host_url/api/2.0/genie/spaces/$old_space_id" -Headers $headers -Method Get
    Write-Host "✅ OLD space exists and is accessible!" -ForegroundColor Green
    Write-Host "   Title: $($result.title)" -ForegroundColor Gray
    Write-Host "   Warehouse: $($result.warehouse_id)" -ForegroundColor Gray
} catch {
    Write-Host "❌ OLD space error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test NEW space
Write-Host "Testing NEW space: $new_space_id" -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
    }
    $result = Invoke-RestMethod -Uri "$host_url/api/2.0/genie/spaces/$new_space_id" -Headers $headers -Method Get
    Write-Host "✅ NEW space exists and is accessible!" -ForegroundColor Green
    Write-Host "   Title: $($result.title)" -ForegroundColor Gray
    Write-Host "   Warehouse: $($result.warehouse_id)" -ForegroundColor Gray
} catch {
    Write-Host "❌ NEW space error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "   Details: $($_.ErrorDetails.Message)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Listing all accessible Genie spaces with this PAT token:" -ForegroundColor Cyan
try {
    $headers = @{
        "Authorization" = "Bearer $token"
    }
    $spaces = Invoke-RestMethod -Uri "$host_url/api/2.0/genie/spaces" -Headers $headers -Method Get
    $spaces.spaces | ForEach-Object {
        Write-Host "  - $($_.space_id): $($_.title)" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Error listing spaces: $($_.Exception.Message)" -ForegroundColor Red
}

