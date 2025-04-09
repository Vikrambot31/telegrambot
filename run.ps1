[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "`n🔍 Проверка окружения..." -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python не установлен." -ForegroundColor Red
    exit
}

# Установка модулей
pip install -r requirements.txt

# Расшифровка .env
if (Test-Path ".env.enc") {
    Write-Host "🔐 Расшифровка .env.enc..." -ForegroundColor Magenta
    python decrypt_env.py
} else {
    Write-Host "⚠️ .env.enc не найден, пропускаем расшифровку." -ForegroundColor Yellow
}

# Запуск бота
Write-Host "`n🚀 Запуск бота..." -ForegroundColor Green
python bot.py
