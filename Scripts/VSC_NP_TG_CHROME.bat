@echo off
echo Starting applications...

:: Запуск Chrome
start chrome

:: Запуск Notepad++
start notepad++

:: Запуск Telegram
start telegram

:: Запуск Visual Studio Code
cd /
cd "C:\Users\Administaror\AppData\Local\Programs\Microsoft VS Code"
.\Code.exe

echo All applications started!
timeout /t 3