#!/bin/bash
# Build script for Trinity Wallet executable

echo "===================================="
echo "Trinity Wallet - Build Script"
echo "===================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "Python found:"
python3 --version
echo

# Check if in correct directory
if [ ! -f "wallet.py" ]; then
    echo "ERROR: wallet.py not found"
    echo "Please run this script from the trinity_wallet_py directory"
    exit 1
fi

# Detect platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macOS"
else
    PLATFORM="Linux"
fi

echo "Building for: $PLATFORM"
echo

echo "Installing/updating PyInstaller..."
pip3 install pyinstaller --upgrade
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install PyInstaller"
    exit 1
fi

echo
echo "Installing wallet dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo
echo "Building executable..."
echo "This may take a few minutes..."
echo

pyinstaller TrinityWallet.spec --clean
if [ $? -ne 0 ]; then
    echo "ERROR: Build failed"
    exit 1
fi

echo
echo "===================================="
echo "Build Successful!"
echo "===================================="
echo
echo "The executable is located at:"
echo "  dist/TrinityWallet"
echo

if [ -f "dist/TrinityWallet" ]; then
    SIZE=$(du -h dist/TrinityWallet | cut -f1)
    echo "File size: $SIZE"
    echo
    
    # Make executable
    chmod +x dist/TrinityWallet
    echo "Executable permissions set"
fi

echo
echo "You can now distribute this executable."
echo "No Python installation required on target machines."
echo
