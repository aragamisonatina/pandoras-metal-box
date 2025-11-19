@echo off
title Pandora's Metal Box
echo.
echo =============================================
echo    PANDORA'S METAL BOX - EXECUTABLE LAUNCHER
echo =============================================
echo.
echo Checking Python installation...

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again.
    pause
    exit /b 1
)

echo Python found! Installing/checking dependencies...

REM Install requirements if they don't exist
if exist requirements.txt (
    python -m pip install -r requirements.txt >nul 2>&1
    echo Dependencies verified!
) else (
    echo Installing numpy and pandas...
    python -m pip install numpy pandas >nul 2>&1
    echo Dependencies installed!
)

echo.
echo Starting Pandora's Metal Box...
echo.

REM Run the game
python main.py

echo.
echo Thanks for playing!
pause