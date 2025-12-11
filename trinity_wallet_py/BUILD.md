# Building Trinity Wallet Executables

This guide explains how to build standalone executables for Trinity Wallet.

## Prerequisites

- Python 3.7 or higher
- PyInstaller: `pip install pyinstaller`
- All wallet dependencies: `pip install -r requirements.txt`

## Building on Windows (for Windows .exe)

**Recommended: Build on actual Windows machine for best compatibility**

1. Open Command Prompt or PowerShell on Windows
2. Navigate to trinity_wallet_py directory:
   ```
   cd trinity_wallet_py
   ```

3. Install build dependencies:
   ```
   pip install pyinstaller
   pip install -r requirements.txt
   ```

4. Build the executable:
   ```
   pyinstaller TrinityWallet.spec --clean
   ```

5. The executable will be in `dist/TrinityWallet.exe`

## Building on Linux (for Linux executable)

1. Navigate to trinity_wallet_py directory:
   ```bash
   cd trinity_wallet_py
   ```

2. Install build dependencies:
   ```bash
   pip3 install pyinstaller
   pip3 install -r requirements.txt
   ```

3. Build the executable:
   ```bash
   pyinstaller TrinityWallet.spec --clean
   ```

4. The executable will be in `dist/TrinityWallet`

## Cross-Compilation Notes

**Building Windows .exe on Linux:**

PyInstaller does not support true cross-compilation. To build Windows executables from Linux, you have these options:

### Option 1: Use Wine (Recommended for CI/CD)

1. Install Wine and Python for Windows:
   ```bash
   sudo apt-get install wine wine64
   wget https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
   wine python-3.11.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
   ```

2. Install dependencies in Wine Python:
   ```bash
   wine pip install pyinstaller ecdsa
   ```

3. Build with Wine:
   ```bash
   wine pyinstaller TrinityWallet.spec --clean
   ```

### Option 2: Docker with Wine

Use a Docker container with Wine and Python for Windows.

### Option 3: Use Windows VM or GitHub Actions (Easiest)

Use a Windows virtual machine or GitHub Actions with Windows runner.

## Build Outputs

After successful build:

- **dist/TrinityWallet.exe** (Windows) or **dist/TrinityWallet** (Linux)
- Single-file executable, no installation required
- Includes all dependencies (Python, ecdsa, etc.)
- Does NOT require Python to be installed on target machine

## Build Configuration

The `TrinityWallet.spec` file controls the build:

- `console=False`: No console window (GUI only)
- `onefile`: Single executable file
- Includes README and INSTALL documentation
- UPX compression enabled for smaller file size

## Distribution

To distribute the wallet:

1. Copy the executable from `dist/` folder
2. Optionally create a ZIP file with:
   - TrinityWallet.exe
   - README.md
   - INSTALL.md
   - Sample trinity.conf

## File Size

Expected executable sizes:
- Windows: ~10-15 MB (compressed with UPX)
- Linux: ~8-12 MB (compressed with UPX)

## Testing the Executable

After building, test the executable:

1. Make sure Trinity daemon is running
2. Double-click the executable (Windows) or run `./TrinityWallet` (Linux)
3. Wallet should open and connect to local node

## Troubleshooting

**"tkinter not found" error:**
- Ensure tkinter is installed: `sudo apt-get install python3-tk` (Linux)
- Reinstall Python with tkinter support (Windows)

**"Module not found" errors:**
- Install missing modules: `pip install <module>`
- Add to hiddenimports in TrinityWallet.spec

**Large file size:**
- UPX is automatically used if available
- Can exclude unnecessary modules in spec file

**Executable doesn't run:**
- Check antivirus isn't blocking
- Run from command line to see errors
- Verify all dependencies in spec file

## Automated Builds

For CI/CD pipelines, see `.github/workflows/` for automated build examples.

## Security Note

Built executables are just packaged Python applications. They still:
- Store wallet files in `~/.trinity_wallet/`
- Use same security model as Python version
- Should be distributed over secure channels
- Can be scanned by antivirus (may show false positives)
