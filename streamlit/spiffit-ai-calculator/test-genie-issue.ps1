# Test Genie Space Access Issue
# Demonstrates the difference between OLD (working) and NEW (broken) Genie spaces

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Genie Space Access Test - Demonstrating the Issue" -ForegroundColor Cyan
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
            if ($name -like "*TOKEN*") {
                Write-Host "  $name = ***${value.Substring([Math]::Max(0, $value.Length - 4))}" -ForegroundColor Gray
            } else {
                Write-Host "  $name = $value" -ForegroundColor Gray
            }
        }
    }
    Write-Host ""
} else {
    Write-Host "❌ No envtemp.txt file found!" -ForegroundColor Red
    Write-Host "   Please create envtemp.txt with your configuration" -ForegroundColor Yellow
    exit 1
}

$profile = $env:DATABRICKS_PROFILE
$old_space_id = $env:OLD_GENIE_SPACE_ID
$new_space_id = $env:NEW_GENIE_SPACE_ID
$host_url = $env:DATABRICKS_HOST

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Profile: $profile" -ForegroundColor Gray
Write-Host "  Host: $host_url" -ForegroundColor Gray
Write-Host "  OLD Space: $old_space_id" -ForegroundColor Green
Write-Host "  NEW Space: $new_space_id" -ForegroundColor Red
Write-Host ""

# Test 1: OLD Genie Space (should work)
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "TEST 1: OLD Genie Space (Should Work)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Space ID: $old_space_id" -ForegroundColor Green
Write-Host ""

try {
    Write-Host "⏳ Testing access..." -ForegroundColor Yellow
    $result = databricks api get "/api/2.0/genie/spaces/$old_space_id" --profile $profile | ConvertFrom-Json
    
    Write-Host "✅ SUCCESS! OLD space is accessible" -ForegroundColor Green
    Write-Host "  Title: $($result.title)" -ForegroundColor White
    Write-Host "  Warehouse: $($result.warehouse_id)" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "❌ FAILED to access OLD space" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Gray
    Write-Host ""
}

# Test 2: NEW Genie Space (should fail)
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "TEST 2: NEW Genie Space (Should Fail)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Space ID: $new_space_id" -ForegroundColor Red
Write-Host ""

try {
    Write-Host "⏳ Testing access..." -ForegroundColor Yellow
    $result = databricks api get "/api/2.0/genie/spaces/$new_space_id" --profile $profile 2>&1
    
    if ($result -match "Error:") {
        Write-Host "❌ FAILED as expected!" -ForegroundColor Red
        Write-Host "  Error: $result" -ForegroundColor Yellow
        Write-Host ""
    } else {
        $parsed = $result | ConvertFrom-Json
        Write-Host "⚠️  UNEXPECTED: NEW space is accessible!" -ForegroundColor Yellow
        Write-Host "  Title: $($parsed.title)" -ForegroundColor White
        Write-Host ""
    }
} catch {
    Write-Host "❌ FAILED as expected!" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host ""
}

# Test 3: List all accessible Genie spaces
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "TEST 3: List All Accessible Genie Spaces" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

try {
    Write-Host "⏳ Fetching list..." -ForegroundColor Yellow
    $spaces = databricks api get "/api/2.0/genie/spaces" --profile $profile | ConvertFrom-Json
    
    Write-Host "✅ Found $($spaces.spaces.Count) accessible Genie spaces:" -ForegroundColor Green
    Write-Host ""
    
    $found_old = $false
    $found_new = $false
    
    foreach ($space in $spaces.spaces) {
        $color = "Gray"
        $marker = "  "
        
        if ($space.space_id -eq $old_space_id) {
            $color = "Green"
            $marker = "✅"
            $found_old = $true
        } elseif ($space.space_id -eq $new_space_id) {
            $color = "Red"
            $marker = "❌"
            $found_new = $true
        }
        
        Write-Host "$marker $($space.space_id): $($space.title)" -ForegroundColor $color
    }
    
    Write-Host ""
    Write-Host "========================================================" -ForegroundColor Cyan
    Write-Host "Summary:" -ForegroundColor Yellow
    Write-Host "========================================================" -ForegroundColor Cyan
    
    if ($found_old) {
        Write-Host "✅ OLD space ($old_space_id) IS in the list" -ForegroundColor Green
    } else {
        Write-Host "❌ OLD space ($old_space_id) NOT in the list" -ForegroundColor Red
    }
    
    if ($found_new) {
        Write-Host "✅ NEW space ($new_space_id) IS in the list" -ForegroundColor Yellow
        Write-Host "   ^ This is unexpected! If it's in the list, why can't we access it?" -ForegroundColor Yellow
    } else {
        Write-Host "❌ NEW space ($new_space_id) NOT in the list" -ForegroundColor Red
        Write-Host "   ^ This is the problem! Your user doesn't have permission to see it" -ForegroundColor Yellow
    }
    
    Write-Host ""
    
} catch {
    Write-Host "❌ Failed to list spaces" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Conclusion:" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "The NEW Genie space needs proper permissions set for:" -ForegroundColor White
Write-Host "  User: $(databricks auth describe --profile $profile 2>&1 | Select-String 'User:' | ForEach-Object { $_.ToString().Split(':')[1].Trim() })" -ForegroundColor Cyan
Write-Host ""
Write-Host "To fix:" -ForegroundColor Yellow
Write-Host "1. Go to the NEW Genie space in Databricks UI" -ForegroundColor Gray
Write-Host "2. Click 'Share' button" -ForegroundColor Gray
Write-Host "3. Add your user with 'Can Manage' permission" -ForegroundColor Gray
Write-Host "   OR enable 'All workspace users' access" -ForegroundColor Gray
Write-Host ""

