# Создаём папку dist, если она ещё не существует
if (-not (Test-Path -Path "./dist")) {
    New-Item -ItemType Directory -Path "./dist"
}

# Копируем нужные файлы
Copy-Item .\s1.webp -Destination .\dist\
Copy-Item .\intro-0.ogg -Destination .\dist\
Copy-Item .\primer_razbora.ogg -Destination .\dist\
Copy-Item .\primer_prognoz2.pdf -Destination .\dist\
Copy-Item .\Voprosi.png -Destination .\dist\

# Копируем все картинки pic*.png
Copy-Item .\pic*.png -Destination .\dist\

# Копируем все аудио x*.ogg
Copy-Item .\x*.ogg -Destination .\dist\

Write-Host "`n✅ Все файлы успешно скопированы в папку 'dist'." -ForegroundColor Green
