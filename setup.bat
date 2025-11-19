@echo off
echo Installing dependencies for Pandora's Metal Box...

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install requirements
echo Installing required packages...
python -m pip install -r requirements.txt

if %ERRORLEVEL% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully!
echo Running Pandora's Metal Box...
python main.py

pause