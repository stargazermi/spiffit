# Test Voice Activations Prompt Directly with Genie API
# Uses Databricks CLI with profile authentication

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Testing Voice Activations Prompt with Genie API" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Load environment variables from .env file
if (Test-Path ".env") {
    Write-Host "✅ Loading .env file..." -ForegroundColor Green
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]*)\s*=\s*(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
            if ($name -notlike "*TOKEN*") {
                Write-Host "  $name = $value" -ForegroundColor Gray
            }
        }
    }
    Write-Host ""
} else {
    Write-Host "❌ No .env file found!" -ForegroundColor Red
    exit 1
}

$host_url = $env:DATABRICKS_HOST
$token = $env:DATABRICKS_TOKEN
$genie_space_id = $env:GENIE_VOICE_ACTIVATIONS_SPACE_ID

if (-not $token) {
    Write-Host "❌ DATABRICKS_TOKEN not found in .env file!" -ForegroundColor Red
    Write-Host "   Please add your PAT token to .env" -ForegroundColor Yellow
    exit 1
}

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Databricks Host: $host_url" -ForegroundColor Gray
Write-Host "  Token: ***$($token.Substring([Math]::Max(0, $token.Length - 4)))" -ForegroundColor Gray
Write-Host "  Genie Space ID: $genie_space_id" -ForegroundColor Gray
Write-Host ""

# The exact prompt from the app
$prompt = @"
For Voice Opportunities, sum MRR by 18 digit opportunity ID and calculate the incentive payout for that opportunity using the following rules return all applicable columns and rows (exclude opportunities where the order stage = Cancelled): Voice Activations Incentive: (Payout Min. `$250 MRR = `$300 |`$1000+ MRR = `$1000)
• Designed to encourage sellers to drive incremental VOIP sales, including both new logo customers and existing customers adding incremental VOIP MRR.
• Based on Opportunity Level (added back into qualifications)
• Applies to any NEW incremental VOIP MRR (Renewals are excluded)
o New Logo Customers
o Customers without Voice products
o Customers with existing Voice products who are adding additional, incremental VOIP lines (this is not a renewal or swap)
• Incremental VOIP sales must generate new MRR
• Migrations or upgrades to incremental VOIP services that generate new MRR are included, while renewals or product swaps without revenue gain are excluded
• Reporting: The Net MRR is specifically separated from Renewal MRR to ensure that only new or incremental VOIP sales are counted, excluding renewals or migrations with no additional revenue gain
"@

Write-Host "Prompt (first 200 chars):" -ForegroundColor Yellow
Write-Host "  $($prompt.Substring(0, [Math]::Min(200, $prompt.Length)))..." -ForegroundColor Gray
Write-Host ""

# Save prompt to temporary file (Databricks CLI needs a file input)
$tempFile = [System.IO.Path]::GetTempFileName()
$prompt | Out-File -FilePath $tempFile -Encoding UTF8 -NoNewline

Write-Host "🚀 Calling Genie API with PAT token..." -ForegroundColor Cyan
Write-Host ""

try {
    Write-Host "⏳ Sending request..." -ForegroundColor Yellow
    
    # Escape the prompt for JSON
    $escapedPrompt = $prompt -replace '\\', '\\' -replace '"', '\"' -replace "`r`n", " " -replace "`n", " " -replace "`r", " "
    
    # Build JSON body
    $jsonBody = @"
{"content": "$escapedPrompt"}
"@
    
    # Call API using REST method with PAT token
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    $api_url = "$host_url/api/2.0/genie/spaces/$genie_space_id/start-conversation"
    Write-Host "  API URL: $api_url" -ForegroundColor Gray
    Write-Host ""
    
    $result = Invoke-RestMethod -Uri $api_url -Method Post -Headers $headers -Body $jsonBody
    
    Write-Host "✅ Response received!" -ForegroundColor Green
    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "Response Details:" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    
    # Display the response
    $result | ConvertTo-Json -Depth 10 | Write-Host
    
    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "Extracting Content:" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    
    # Try to extract the actual content/text
    if ($result.message) {
        Write-Host "📄 Message:" -ForegroundColor Yellow
        Write-Host ""
        
        if ($result.message.content) {
            Write-Host $result.message.content -ForegroundColor White
        }
        
        if ($result.message.attachments) {
            Write-Host ""
            Write-Host "📎 Attachments ($($result.message.attachments.Count)):" -ForegroundColor Yellow
            $result.message.attachments | ForEach-Object {
                Write-Host "  Type: $($_.type)" -ForegroundColor Gray
                if ($_.text) {
                    Write-Host "  Text:" -ForegroundColor Gray
                    Write-Host $_.text.content -ForegroundColor White
                }
                if ($_.query) {
                    Write-Host "  Query:" -ForegroundColor Gray
                    Write-Host $_.query.query -ForegroundColor Cyan
                }
            }
        }
    }
    
    Write-Host ""
    Write-Host "✅ Test complete!" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error calling Genie API:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    if ($_.ErrorDetails) {
        Write-Host "Error details:" -ForegroundColor Yellow
        Write-Host $_.ErrorDetails.Message -ForegroundColor Gray
    }
    exit 1
} finally {
    # Clean up temp file
    if (Test-Path $tempFile) {
        Remove-Item $tempFile -Force
    }
}

