# Создать папку dist, если она ещё не существует
if (-not (Test-Path -Path "./dist")) {
    New-Item -ItemType Directory -Path "./dist"
}

# Список расширений для медиафайлов
$extensions = "*.png", "*.jpg", "*.jpeg", "*.ogg", "*.webp", "*.mp3", "*.pdf"

# Копировать все медиафайлы в dist
foreach ($ext in $extensions) {
    Get-ChildItem -Path . -Filter $ext | ForEach-Object {
        Copy-Item $_.FullName -Destination "./dist" -Force
    }
}

Write-Host "`n✅ Все медиафайлы успешно скопированы в папку 'dist'." -ForegroundColor Green
