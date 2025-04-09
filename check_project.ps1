# Быстрая проверка TelegramBot-папки
Write-Host "`n🔍 Запускаю аудит проекта..." -ForegroundColor Cyan

# Проверка на наличие .env (опасность)
if (Test-Path ".env") {
    Write-Host "⚠️ Найден открытый .env файл! Удали его или зашифруй." -ForegroundColor Red
} else {
    Write-Host "✅ Файл .env не найден (или зашифрован)." -ForegroundColor Green
}

# Проверка .env.enc
if (Test-Path ".env.enc") {
    Write-Host "✅ Найден .env.enc (зашифрованный файл)." -ForegroundColor Green
} else {
    Write-Host "⚠️ Файл .env.enc отсутствует!" -ForegroundColor Yellow
}

# Проверка наличия секретов в коде
Write-Host "`n🔍 Поиск подозрительных токенов и ключей в .py..."
Get-ChildItem -Recurse -Include *.py | ForEach-Object {
    $content = Get-Content $_.FullName
    if ($content -match "TOKEN=.*|SECRET=.*|API_KEY=.*|AA[A-Za-z0-9]{30,}") {
        Write-Host "❗ Возможная утечка в $($_.Name)" -ForegroundColor Red
    }
}

# Проверка на ошибки Python синтаксиса
Write-Host "`n🐍 Проверка синтаксиса Python..."
$errors = python -m py_compile (Get-ChildItem -Filter *.py).Name 2>&1
if ($errors) {
    Write-Host "❌ Синтаксическая ошибка:" -ForegroundColor Red
    Write-Host $errors
} else {
    Write-Host "✅ Синтаксис всех .py файлов в порядке." -ForegroundColor Green
}

# Проверка Git статуса
Write-Host "`n🔁 Проверка Git..."
git status

Write-Host "`n✅ Проверка завершена. Устраните предупреждения, если они есть.`n" -ForegroundColor Cyan
