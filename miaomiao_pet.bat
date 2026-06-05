@echo off
chcp 65001 >nul 2>&1
cd /d "%~dp0"
"D:\Config\zetero\python312\python.exe" main.py
pause