Write-Host "🔍 Проверка зависимостей..."
pip install -r requirements.txt

Write-Host "✅ Проверка .env"
if (!(Test-Path ".env")) {
    Write-Host "❌ Файл .env не найден. Остановлено."
    exit
}

$envVars = Get-Content ".env" | Where-Object { $_ -match "=" }
foreach ($line in $envVars) {
    $parts = $line -split "=", 2
    [System.Environment]::SetEnvironmentVariable($parts[0], $parts[1], "Process")
}

Write-Host "🚀 Запуск Telegram-бота..."
python bot.py
