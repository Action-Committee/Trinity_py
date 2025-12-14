# Trinity Python Wallet - Installation Guide

## Windows Installation

### Prerequisites
1. **Python 3.7 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Trinity Daemon (trinityd)**
   - The Python wallet needs a running Trinity daemon to connect to
   - Download and install Trinity Core from the main repository

### Installation Steps

1. **Navigate to the wallet directory:**
   ```
   cd trinity_wallet_py
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Configure Trinity daemon:**
   
   Create or edit `trinity.conf` in Trinity data directory:
   - Windows: `%APPDATA%\Trinity\trinity.conf`
   
   Add these lines:
   ```
   server=1
   rpcuser=rpcuser
   rpcpassword=your_secure_password_here
   rpcport=6420
   rpcallowip=127.0.0.1
   ```

4. **Start Trinity daemon:**
   ```
   trinityd.exe
   ```

5. **Launch the wallet:**
   - Double-click `launch_wallet.bat`, or
   - Run: `python wallet.py`

## Linux Installation

### Prerequisites
1. **Python 3.7 or higher**
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip
   ```

2. **Trinity Daemon**
   ```bash
   # Build Trinity from source or use pre-compiled binaries
   ```

### Installation Steps

1. **Navigate to the wallet directory:**
   ```bash
   cd trinity_wallet_py
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure Trinity daemon:**
   
   Edit `~/.trinity/trinity.conf`:
   ```
   server=1
   rpcuser=rpcuser
   rpcpassword=your_secure_password_here
   rpcport=6420
   rpcallowip=127.0.0.1
   ```

4. **Start Trinity daemon:**
   ```bash
   trinityd -daemon
   ```

5. **Launch the wallet:**
   ```bash
   ./launch_wallet.sh
   ```
   or
   ```bash
   python3 wallet.py
   ```

## macOS Installation

### Prerequisites
1. **Python 3.7 or higher**
   ```bash
   brew install python3
   ```

2. **Trinity Daemon**
   - Build from source or use pre-compiled binaries

### Installation Steps

Follow the same steps as Linux installation above.

## First Run

When you first run the wallet:

1. **Wallet Creation:**
   - A new wallet file will be created at `~/.trinity_wallet/wallet.json`
   - This file contains your private keys - **KEEP IT SAFE!**

2. **Generate First Address:**
   - Go to "Wallet" → "New Address"
   - Enter a label (e.g., "Main Address")
   - Your first Trinity address will be generated

3. **Verify Connection:**
   - Check the status bar at the bottom
   - Should show "Status: Connected to local node"
   - If not, go to "Settings" → "Connect to Node" and verify settings

4. **Sync Blockchain:**
   - Wait for Trinity daemon to sync with the network
   - Check sync status in Trinity daemon console

## Troubleshooting

### "Python not found" error
- Ensure Python is installed and added to PATH
- On Windows, reinstall Python and check "Add Python to PATH"

### "Module not found" error
- Run: `pip install -r requirements.txt`
- Make sure you're in the trinity_wallet_py directory

### "Cannot connect to node" error
- Check Trinity daemon is running
- Verify trinity.conf settings
- Check RPC username/password match
- Ensure port 6420 is not blocked by firewall

### Wallet shows 0 balance but you have coins
- Click "Refresh" button
- Wait for blockchain sync to complete
- Check connection status

## Security Recommendations

1. **Backup Your Wallet:**
   - Regularly backup `~/.trinity_wallet/wallet.json`
   - Store backups in multiple secure locations
   - Consider encrypting backups

2. **Strong RPC Password:**
   - Use a strong, unique password for RPC
   - Don't use the default "rpcpassword"

3. **Firewall Configuration:**
   - Only allow RPC connections from localhost (127.0.0.1)
   - Don't expose RPC port to the internet

4. **Keep Software Updated:**
   - Update Trinity daemon regularly
   - Update Python wallet when new versions are released

5. **Verify Addresses:**
   - Always double-check addresses before sending
   - Use copy-paste instead of typing manually

## Wallet File Location

The wallet stores data in:
- **Windows:** `C:\Users\<username>\.trinity_wallet\wallet.json`
- **Linux:** `~/.trinity_wallet/wallet.json`
- **macOS:** `~/.trinity_wallet/wallet.json`

This file contains:
- Private keys (encrypted in plain JSON - backup securely!)
- Address labels
- Wallet metadata

## Upgrading

To upgrade to a new version:

1. Backup your wallet file
2. Stop the wallet
3. Update the wallet files
4. Restart the wallet
5. Verify your addresses are still present

## Uninstallation

To remove the wallet:

1. **Backup wallet file first!**
2. Delete the trinity_wallet_py directory
3. Optionally delete wallet data directory:
   - Windows: `%USERPROFILE%\.trinity_wallet`
   - Linux/Mac: `~/.trinity_wallet`

## Getting Help

If you encounter issues:

1. Check this installation guide
2. Review the README.md file
3. Check Trinity daemon logs
4. Visit the Trinity repository for support

## Development Mode

For developers who want to modify the wallet:

```bash
# Clone repository
git clone https://github.com/Action-Committee/Trinity_py.git
cd Trinity_py/trinity_wallet_py

# Install in development mode
pip install -e .

# Make changes and test
python wallet.py
```

## System Requirements

- **Operating System:** Windows 7+, Linux, macOS 10.12+
- **Python:** 3.7 or higher
- **RAM:** 512 MB minimum
- **Disk Space:** 50 MB for wallet, plus blockchain size
- **Network:** Internet connection for blockchain sync
