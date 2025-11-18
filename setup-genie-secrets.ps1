# Setup Databricks Secrets for Genie Access
# This script creates a secret scope and stores your PAT token securely

$Profile = "dlk-hackathon"
$SecretScope = "spiffit-secrets"
$SecretKey = "databricks-pat-token"

Write-Host "🔐 Databricks Secrets Setup for Genie Access" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if scope exists
Write-Host "📋 Checking if secret scope exists..." -ForegroundColor Green
$scopeList = databricks secrets list-scopes --profile $Profile --output json 2>&1

if ($scopeList -match $SecretScope) {
    Write-Host "✅ Secret scope '$SecretScope' already exists" -ForegroundColor Green
} else {
    Write-Host "📦 Creating secret scope '$SecretScope'..." -ForegroundColor Yellow
    databricks secrets create-scope $SecretScope --profile $Profile
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Secret scope created!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to create secret scope" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Step 2: Prompt for PAT token
Write-Host "🔑 Personal Access Token Setup" -ForegroundColor Yellow
Write-Host ""
Write-Host "To generate a PAT token:" -ForegroundColor Gray
Write-Host "  1. Go to Databricks UI" -ForegroundColor Gray
Write-Host "  2. Settings → Developer → Access Tokens" -ForegroundColor Gray
Write-Host "  3. Generate New Token" -ForegroundColor Gray
Write-Host "  4. Copy the token" -ForegroundColor Gray
Write-Host ""

$token = Read-Host "Paste your PAT token here (hidden)" -AsSecureString
$tokenPlainText = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
)

if ([string]::IsNullOrWhiteSpace($tokenPlainText)) {
    Write-Host "❌ No token provided. Exiting." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "💾 Storing token in Databricks Secrets..." -ForegroundColor Green

# Step 3: Store the secret
$tempFile = [System.IO.Path]::GetTempFileName()
Set-Content -Path $tempFile -Value $tokenPlainText -NoNewline

databricks secrets put-secret $SecretScope $SecretKey --string-value $tokenPlainText --profile $Profile

# Clean up temp file
Remove-Item $tempFile -Force

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Token stored securely!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎯 Next steps:" -ForegroundColor Yellow
    Write-Host "  1. The app.yaml is already configured to use this secret" -ForegroundColor Gray
    Write-Host "  2. Commit and push your changes (safe - no token in Git!)" -ForegroundColor Gray
    Write-Host "     git add streamlit/spiffit-ai-calculator/app.yaml" -ForegroundColor Cyan
    Write-Host "     git commit -m 'Configure Genie auth with secrets'" -ForegroundColor Cyan
    Write-Host "     git push origin spiffit-dev" -ForegroundColor Cyan
    Write-Host "  3. Deploy the app:" -ForegroundColor Gray
    Write-Host "     .\deploy-to-databricks.ps1" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "❌ Failed to store secret" -ForegroundColor Red
    exit 1
}

