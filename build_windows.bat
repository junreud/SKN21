@echo off
echo 🃏 Building Solitaire Game for Windows...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "solitaire_env" (
    echo Creating virtual environment...
    python -m venv solitaire_env
)

REM Activate virtual environment
echo Activating virtual environment...
call solitaire_env\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install pygame==2.6.1 pyinstaller==6.16.0

REM Create executable
echo Creating Windows executable...
pyinstaller --onefile --windowed --name "Solitaire" solitaire_pygame.py

echo.
echo ✅ Build complete! 
echo 📦 Your Solitaire.exe is in the 'dist' folder
echo 📊 File size: approximately 15-20 MB
echo.
echo 🚀 To distribute:
echo 1. Copy dist\Solitaire.exe to any Windows computer
echo 2. Double-click to run (no Python installation needed!)
echo 3. The game works on Windows 7, 8, 10, and 11
echo.
pause