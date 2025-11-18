# Fix Genie Space ID in .env file
# Changes 0110c4ae... to 01f0c4ae...

$envFile = ".env"

if (Test-Path $envFile) {
    Write-Host "✅ Found .env file" -ForegroundColor Green
    
    $content = Get-Content $envFile -Raw
    $oldId = "0110c4ae99271d64835d414b8d43ddfb"
    $newId = "01f0c4ae99271d64835d414b8d43ddfb"
    
    if ($content -match $oldId) {
        $newContent = $content -replace $oldId, $newId
        $newContent | Set-Content $envFile -NoNewline
        Write-Host "✅ Fixed Genie Space IDs in .env" -ForegroundColor Green
        Write-Host "   Changed: $oldId" -ForegroundColor Red
        Write-Host "   To:      $newId" -ForegroundColor Green
    } else {
        Write-Host "✅ .env already has correct Genie Space ID" -ForegroundColor Green
    }
} else {
    Write-Host "❌ No .env file found!" -ForegroundColor Red
    Write-Host "   Create a .env file with the correct Genie Space ID:" -ForegroundColor Yellow
    Write-Host "   GENIE_SPACE_ID=01f0c4ae99271d64835d414b8d43ddfb" -ForegroundColor Gray
}

