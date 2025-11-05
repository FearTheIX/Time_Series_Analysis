@echo off
chcp 65001 >nul
title Integrated Analytics Platform
echo ===================================================
echo    Starting Integrated Analytics Platform
echo ===================================================
echo.

:: Check if we are in a virtual environment and if not, try to activate it
if "%VIRTUAL_ENV%"=="" (
    echo Not in a virtual environment. Checking for venv...
    if exist "venv\Scripts\activate.bat" (
        echo Activating virtual environment...
        call venv\Scripts\activate.bat
    ) else (
        echo Virtual environment not found. Using system Python.
    )
)

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Please make sure Python is installed and added to PATH
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