@echo off
REM Build script for Trinity Wallet Windows executable

echo ====================================
echo Trinity Wallet - Windows Build Script
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Check if in correct directory
if not exist "wallet.py" (
    echo ERROR: wallet.py not found
    echo Please run this script from the trinity_wallet_py directory
    pause
    exit /b 1
)

echo Installing/updating PyInstaller...
pip install pyinstaller --upgrade
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)

echo.
echo Installing wallet dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Building Windows executable...
echo This may take a few minutes...
echo.

pyinstaller TrinityWallet.spec --clean
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo ====================================
echo Build Successful!
echo ====================================
echo.
echo The executable is located at:
echo   dist\TrinityWallet.exe
echo.
echo File size:
dir dist\TrinityWallet.exe | find "TrinityWallet.exe"
echo.
echo You can now distribute this executable.
echo No Python installation required on target machines.
echo.

pause
