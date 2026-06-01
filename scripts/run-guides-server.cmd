@echo off
cd /d "%~dp0.."
python scripts\serve_guides.py --build --open --port 8080
