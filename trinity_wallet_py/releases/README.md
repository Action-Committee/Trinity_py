# Trinity Wallet - Pre-built Executables

## Download Executables

Pre-built executables for Trinity Wallet are available through GitHub Actions.

### Getting the Latest Build

**Option 1: GitHub Actions Artifacts (Recommended)**

1. Go to the [Actions tab](https://github.com/Action-Committee/Trinity_py/actions)
2. Click on the latest "Build Trinity Wallet Executables" workflow run
3. Download the artifact for your platform:
   - **Windows**: `TrinityWallet-Windows.zip`
   - **Linux**: `TrinityWallet-Linux.tar.gz`
   - **macOS**: `TrinityWallet-macOS.tar.gz`

**Option 2: Build Locally**

See [BUILD.md](../BUILD.md) for instructions on building executables on your platform.

## Platform-Specific Instructions

### Windows

1. Download `TrinityWallet-Windows.zip`
2. Extract the ZIP file
3. Run `TrinityWallet.exe`

No Python installation required!

### Linux

1. Download `TrinityWallet-Linux.tar.gz`
2. Extract: `tar -xzf TrinityWallet-Linux.tar.gz`
3. Make executable: `chmod +x TrinityWallet`
4. Run: `./TrinityWallet`

### macOS

1. Download `TrinityWallet-macOS.tar.gz`
2. Extract: `tar -xzf TrinityWallet-macOS.tar.gz`
3. Make executable: `chmod +x TrinityWallet`
4. Run: `./TrinityWallet`

## Prerequisites

Before running the wallet executable:

1. **Trinity Daemon Running**
   - Must have Trinity daemon (trinityd) running
   - Configure RPC in trinity.conf:
     ```
     server=1
     rpcuser=rpcuser
     rpcpassword=yourpassword
     rpcport=6420
     ```

2. **Network Connection**
   - Required for blockchain synchronization

## File Sizes

Approximate executable sizes:
- Windows: ~10-15 MB
- Linux: ~8-12 MB  
- macOS: ~10-14 MB

## What's Included

Each executable is a standalone package containing:
- Trinity Wallet application
- Python runtime (embedded)
- All dependencies (ecdsa, etc.)
- GUI framework (tkinter)

## Security Notes

**Antivirus Warning**: Some antivirus software may flag PyInstaller executables as suspicious. This is a false positive common with packaged Python applications.

**Verification**: 
- Download only from official GitHub repository
- Check file hashes if provided
- Scan with antivirus before running

**Source Code**: 
- Full source code available in parent directory
- Can build from source for maximum security

## Troubleshooting

**Executable won't run (Windows)**:
- Right-click → Properties → Unblock
- Add exception in antivirus software
- Run as Administrator

**"Cannot connect to node" error**:
- Ensure Trinity daemon is running
- Check RPC credentials in trinity.conf
- Verify port 6420 is not blocked

**GUI doesn't appear**:
- Check if process is running in Task Manager
- Look for error logs in console
- Try running from command line to see errors

## Alternative: Python Version

If executables don't work, you can always use the Python version:

```bash
cd trinity_wallet_py
pip install -r requirements.txt
python wallet.py
```

See [README.md](../README.md) for full Python installation instructions.

## Building Your Own

To build executables yourself:

1. See [BUILD.md](../BUILD.md) for detailed instructions
2. GitHub Actions workflow automatically builds on push
3. Windows builds must be done on Windows (or with Wine)

## Automated Builds

This repository uses GitHub Actions to automatically build executables:
- **Trigger**: Push to main or copilot/* branches
- **Platforms**: Windows, Linux, macOS
- **Output**: Artifacts available in Actions tab
- **Workflow**: `.github/workflows/build-wallet.yml`

## Support

For issues with executables:
1. Check this README
2. Review BUILD.md
3. Try Python version
4. Open GitHub issue with:
   - Platform (Windows/Linux/macOS)
   - Error messages
   - Trinity daemon status
