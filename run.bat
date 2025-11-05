@echo off
chcp 65001 >nul
title Integrated Analytics Platform
echo ===================================================
echo    Starting Integrated Analytics Platform
echo ===================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Run main application
echo.
echo Starting main application...
python main_gui.py

echo.
echo Application closed.
pause