@echo off
echo Закрытие старых процессов Python (если они зависли)...
taskkill /F /IM python.exe >nul 2>&1

echo Ждём немного...
timeout /t 2 >nul

echo Запуск Telegram бота...
python bot.py

