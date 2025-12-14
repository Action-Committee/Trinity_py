@echo off
REM Ultra-Fast Windows .exe Builder for Trinity Wallet
REM Simply double-click this file to build TrinityWallet.exe

echo ============================================================
echo Trinity Wallet - Ultra-Fast Windows Builder
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or later from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

echo Building Windows executable...
echo This will take approximately 30-90 seconds.
echo.

REM Run the build script
python build_windows_fast.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo BUILD FAILED!
    echo ============================================================
    echo Check the error messages above for details.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo BUILD SUCCESSFUL!
echo ============================================================
echo.
echo The Windows executable has been created:
echo   Location: ..\Files\TrinityWallet.exe
echo.
echo You can now:
echo   1. Navigate to the Files folder
echo   2. Double-click TrinityWallet.exe to run the wallet
echo.
echo ============================================================

pause
