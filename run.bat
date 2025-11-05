@echo off
chcp 65001 >nul
title Integrated Analytics Platform - All Laboratories
echo ===================================================
echo    Starting Integrated Analytics Platform
echo    Laboratories 1, 2, 3, 4 - Complete Integration
echo ===================================================
echo.

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

:: Install/upgrade dependencies (без PySide6)
echo Installing required dependencies...
pip install -r requirements.txt

:: Run the tkinter application
echo.
echo Starting main application (Tkinter version)...
python main_gui_tkinter.py

:: If the application closes, show message
echo.
echo Application closed.
pause