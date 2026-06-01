@echo off
cd /d "%~dp0.."
python scripts\send_telegram.py %*
if errorlevel 1 pause
