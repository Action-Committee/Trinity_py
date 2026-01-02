# Trinity Wallet - Windows Executable Build Guide

## Overview

This document describes the ultra-fast build system for creating Windows executables of the Trinity Python Wallet.

## Ultra-Fast Build Environment

We've configured a streamlined build system that can compile the Trinity Wallet into a Windows .exe file in approximately 30-90 seconds.

### Components

1. **Optimized Build Script**: `trinity_wallet_py/build_windows_fast.py`
   - Automatic dependency installation
   - Clean build process (removes caches)
   - Optimized PyInstaller settings
   - Single-file executable output
   - Automatic copy to Files/ folder

2. **GitHub Actions Workflow**: `.github/workflows/build-and-commit-exe.yml`
   - Automatic Windows .exe builds
   - Commits results to Files/ folder
   - Triggers on code changes or manual dispatch

3. **Output Location**: `Files/`
   - TrinityWallet.exe (Windows executable)
   - Documentation files
   - Build information

## Quick Start

### Option 1: Automated Build (Recommended)

The Windows .exe is automatically built by GitHub Actions whenever you:
- Push changes to `trinity_wallet_py/`
- Manually trigger the workflow from the Actions tab

**To trigger manually:**
1. Go to GitHub repository → Actions tab
2. Select "Build and Commit Windows Executable"
3. Click "Run workflow"
4. Wait 2-3 minutes
5. The .exe will be committed to the Files/ folder

### Option 2: Build on Windows

If you have access to a Windows machine:

```batch
cd trinity_wallet_py
python build_windows_fast.py
```

The executable will be created in `Files/TrinityWallet.exe`

### Option 3: Build with Wine (Linux/Mac)

For advanced users who want to cross-compile on Linux/Mac:

```bash
# Install Wine (varies by distribution)
sudo apt-get install wine wine64  # Ubuntu/Debian
brew install wine                  # macOS

# Install Windows Python under Wine
# See https://www.python.org/downloads/windows/

# Build
cd trinity_wallet_py
wine python build_windows_fast.py
```

## Build Optimizations

The build system includes several optimizations for speed:

1. **Dependency Caching**: Dependencies are only downloaded once
2. **Clean Builds**: Old artifacts are removed to prevent issues
3. **Reduced Logging**: Build output is minimal (WARN level)
4. **UPX Compression**: Smaller executable size
5. **Single-File Mode**: One .exe file, no dependencies

## Build Output

### Specifications

- **File**: TrinityWallet.exe
- **Size**: ~10-15 MB (includes Python runtime)
- **Platform**: Windows 7+ (64-bit)
- **Type**: Single-file executable
- **Mode**: Windowed (no console)

### What's Included

The .exe contains:
- Complete Python 3.11 runtime
- Trinity Wallet GUI (tkinter)
- ecdsa cryptographic library
- All wallet core modules
- Documentation

## Build Time

- **Initial build**: ~90 seconds (downloads dependencies)
- **Subsequent builds**: ~30 seconds (dependencies cached)
- **GitHub Actions**: ~2-3 minutes (includes runner setup)

## Verification

To verify the executable was built correctly:

1. Check file size (should be ~10-15 MB)
2. Run on Windows and verify GUI appears
3. Check GitHub Actions logs for build output
4. Compare with artifacts from the build-wallet.yml workflow

## Troubleshooting

### Build fails on Windows

**Issue**: PyInstaller not installed  
**Solution**: `pip install pyinstaller`

**Issue**: ecdsa not installed  
**Solution**: The script auto-installs, but you can manually run `pip install ecdsa==0.19.1`

### Executable doesn't run

**Issue**: Windows security warning  
**Solution**: Click "More info" → "Run anyway". This is normal for unsigned executables.

**Issue**: Trinity daemon not running  
**Solution**: Start trinityd with RPC enabled before running the wallet.

### Build on Linux fails

**Issue**: tkinter not found  
**Solution**: `sudo apt-get install python3-tk`

**Issue**: Cross-compilation to Windows fails  
**Solution**: Use Wine or trigger the GitHub Actions workflow instead.

## Security Notes

- Executables are built in GitHub's secure environment
- Source code is 100% open and auditable
- You can verify builds by checking workflow logs
- For maximum security, build from source yourself

## Advanced Configuration

### Customizing the Build

Edit `trinity_wallet_py/TrinityWallet.spec` to customize:
- Icon file
- Version information
- Additional files to include
- Compression settings
- Excluded modules

### Adding to Continuous Integration

The build is already integrated into CI/CD. Every push to `trinity_wallet_py/` triggers:
1. Build wallet executables (Windows/Linux/macOS)
2. Run tests
3. Upload artifacts
4. (Optional) Commit Windows .exe to Files/

## Files Created

After a successful build:

```
Files/
├── TrinityWallet.exe    # Windows executable
├── TrinityWallet        # Linux executable (if built)
├── README.md            # User documentation
├── INSTALL.md           # Installation guide
├── README.txt           # Quick start
└── BUILD_INFO.txt       # This file
```

## Next Steps

1. The Windows .exe will be automatically built when this code is pushed
2. Check the GitHub Actions tab to monitor build progress
3. Once complete, TrinityWallet.exe will appear in the Files/ folder
4. Download and test the executable on Windows

## Support

For build issues:
- Check GitHub Actions logs
- Review trinity_wallet_py/BUILD.md
- Open an issue in the repository
- Build manually using the script

---

**Build System Version**: 1.0  
**Last Updated**: 2025-12-14  
**Maintained By**: Trinity Wallet Development Team
