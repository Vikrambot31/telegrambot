# Загружаем .env
$envPath = ".env"
if (-Not (Test-Path $envPath)) {
    Write-Host "❌ Файл .env не найден!" -ForegroundColor Red
    exit 1
}

# Читаем строки и извлекаем BOT_TOKEN
$lines = Get-Content $envPath
foreach ($line in $lines) {
    if ($line -match "^\s*BOT_TOKEN\s*=\s*(.+)$") {
        $token = $matches[1].Trim()
        break
    }
}

# Проверяем наличие токена
if ($null -eq $token -or $token -eq "") {
    Write-Host "❌ BOT_TOKEN не найден в .env!" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✅ BOT_TOKEN загружен: $token" -ForegroundColor Green
}

# Можно также экспортировать в окружение
$env:BOT_TOKEN = $token
