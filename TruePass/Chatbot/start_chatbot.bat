@echo off
echo ================================
echo TruePass AI Chatbot Launcher
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "chatbot.py" (
    echo ❌ chatbot.py not found!
    echo Please run this script from the Chatbot directory
    echo.
    pause
    exit /b 1
)

REM Run the launcher
echo 🚀 Starting TruePass AI Chatbot...
echo.
python launcher.py

echo.
echo 👋 Chatbot session ended
pause
