# Trinity Python Wallet

A Windows-compatible wallet for Trinity cryptocurrency, written in Python with a graphical user interface.

## Features

- **Full Trinity Network Support**: Compatible with existing Trinity network and consensus
- **Key Management**: Generate new addresses, import/export private keys
- **Transaction Management**: Send and receive TRINITY coins
- **Windows GUI**: User-friendly interface built with tkinter
- **RPC Integration**: Connects to Trinity daemon via RPC
- **Secure Storage**: Local wallet storage with restricted permissions
- **Address Labels**: Organize your addresses with custom labels
- **Multi-Algorithm Support**: Works with SHA256D, Scrypt, and Groestl mining

## Installation

### Prerequisites

- Python 3.7 or higher
- Trinity daemon (trinityd) running with RPC enabled

### Setup

1. Install Python dependencies:
```bash
cd trinity_wallet_py
pip install -r requirements.txt
```

2. Make sure Trinity daemon is running with RPC enabled. Add this to your `trinity.conf`:
```
server=1
rpcuser=rpcuser
rpcpassword=rpcpassword
rpcport=6420
```

## Usage

### Starting the Wallet

Run the wallet with:
```bash
python wallet.py
```

Or on Windows, you can double-click `wallet.py` if Python is associated with `.py` files.

### First Time Setup

1. The wallet will create a new wallet file at `~/.trinity_wallet/wallet.json`
2. Generate a new receiving address using "Wallet" → "New Address"
3. Configure RPC connection if not using default settings via "Settings" → "Connect to Node"

### Connecting to Trinity Node

The wallet attempts to connect to a local Trinity daemon by default:
- Host: 127.0.0.1
- Port: 6420
- Username: rpcuser
- Password: rpcpassword

You can change these settings in "Settings" → "Connect to Node"

### Sending TRINITY

1. Go to the "Send" tab
2. Enter the destination address
3. Enter the amount to send
4. Click "Send"
5. Confirm the transaction

### Receiving TRINITY

1. Go to the "Receive" tab
2. Select an address or create a new one
3. Copy the address and share it with the sender

### Managing Keys

**Generate New Address:**
- Go to "Wallet" → "New Address"
- Optionally enter a label for the address

**Import Private Key:**
- Go to "Wallet" → "Import Private Key"
- Enter the private key in WIF format
- Optionally enter a label

**Export Private Key:**
- Go to the "Addresses" tab
- Select an address
- Click "Export Private Key" (in Wallet menu)
- **Warning**: Keep private keys secure!

## Trinity Network Details

- **Network Port**: 62621
- **RPC Port**: 6420
- **Address Prefix**: 30 (addresses start with 'D')
- **Mining Algorithms**: SHA256D, Scrypt, Groestl
- **Genesis Block**: 000003070f466e13150a395e05856c99c5f70f9934e1d1cc0aa6dd8024de7743

## Wallet File Location

The wallet stores keys and labels in:
- **Windows**: `C:\Users\<username>\.trinity_wallet\wallet.json`
- **Linux/Mac**: `~/.trinity_wallet/wallet.json`

**Important**: Backup this file regularly! It contains your private keys.

## Security Notes

1. **Backup your wallet**: The wallet.json file contains all your private keys
2. **Secure your RPC connection**: Use strong RPC passwords
3. **Keep software updated**: Always use the latest version
4. **Verify addresses**: Always double-check addresses before sending
5. **Private key safety**: Never share your private keys

## Architecture

The wallet consists of:

- **Core Module** (`core/`):
  - `key.py`: Key generation, address creation, signing
  - `wallet.py`: Wallet management, storage
  - `rpc_client.py`: RPC communication with Trinity daemon

- **Utils Module** (`utils/`):
  - `base58.py`: Base58 encoding/decoding for addresses

- **GUI Module** (`gui/`):
  - `main_window.py`: Main Windows interface using tkinter

## Compatibility

This wallet is fully compatible with:
- Trinity Core daemon (C++ implementation)
- Trinity network protocol
- Trinity address format
- Existing Trinity wallets

## Troubleshooting

**Wallet won't connect:**
- Check Trinity daemon is running
- Verify RPC settings in trinity.conf
- Ensure firewall allows localhost connections

**Balance shows 0:**
- Check connection to daemon
- Wait for blockchain synchronization
- Click "Refresh" to update balance

**Can't send transactions:**
- Ensure wallet is unlocked (if encrypted)
- Verify sufficient balance
- Check address is valid

## Development

Built with:
- Python 3
- tkinter (GUI)
- ecdsa (cryptography)
- Standard library (networking, JSON)

## License

Released under MIT license. See COPYING file for details.

## Support

For issues and questions, please visit the Trinity repository or contact the development team.
