# Trinity Python Wallet

## Overview

The Trinity Python Wallet is a Windows-compatible cryptocurrency wallet written in Python. It provides a graphical user interface for managing Trinity cryptocurrency, including sending, receiving, and managing addresses.

## Location

The Python wallet is located in the `trinity_wallet_py/` directory of this repository.

## Features

- ✅ **Full Network Compatibility**: Works with the existing Trinity network and consensus
- ✅ **Python Implementation**: Written entirely in Python 3.7+
- ✅ **Windows GUI**: User-friendly interface using tkinter (cross-platform compatible)
- ✅ **Key Management**: Generate new addresses, import/export private keys
- ✅ **Transaction Support**: Send and receive TRINITY coins
- ✅ **RPC Integration**: Connects to Trinity daemon via RPC
- ✅ **Address Compatibility**: Generates Trinity addresses starting with 'D' (base58 prefix 30)
- ✅ **Secure Storage**: Local wallet storage with proper file permissions
- ✅ **Multi-Algorithm Support**: Compatible with SHA256D, Scrypt, and Groestl mining

## Quick Start

### Prerequisites

1. Python 3.7 or higher
2. Trinity daemon (trinityd) running with RPC enabled

### Installation

```bash
cd trinity_wallet_py
pip install -r requirements.txt
```

### Running the Wallet

**Windows:**
```
launch_wallet.bat
```

**Linux/Mac:**
```bash
./launch_wallet.sh
```

Or directly:
```bash
python wallet.py
```

## Documentation

- **README.md** - Detailed wallet features and usage
- **INSTALL.md** - Step-by-step installation guide for all platforms
- **test_wallet.py** - Component tests for validation

## Architecture

```
trinity_wallet_py/
├── core/               # Core wallet functionality
│   ├── key.py          # Key generation and management
│   ├── wallet.py       # Wallet storage and operations
│   └── rpc_client.py   # RPC client for Trinity daemon
├── gui/                # GUI components
│   └── main_window.py  # Main tkinter interface
├── utils/              # Utility functions
│   └── base58.py       # Base58 encoding/decoding
├── wallet.py           # Main entry point
├── requirements.txt    # Python dependencies
├── README.md           # User documentation
└── INSTALL.md          # Installation guide
```

## Trinity Network Compatibility

The Python wallet is fully compatible with:

- **Network Protocol**: Uses Trinity's message start bytes (0x64, 0x72, 0xe8, 0xa6)
- **Address Format**: Trinity addresses with base58 prefix 30 ('D' prefix)
- **RPC Interface**: Standard Trinity RPC port 6420
- **Consensus Rules**: Follows Trinity blockchain consensus
- **Algorithms**: Supports SHA256D, Scrypt, and Groestl

## Security

- Private keys stored locally in `~/.trinity_wallet/wallet.json`
- Uses ECDSA SECP256k1 curve (same as Bitcoin)
- Supports wallet backup and restore
- RPC communication over localhost by default

## Testing

Run the component tests:

```bash
cd trinity_wallet_py
python test_wallet.py
```

All tests should pass:
- ✅ Base58 encoding/decoding
- ✅ Key generation
- ✅ Address creation (starting with 'D')
- ✅ Address validation
- ✅ WIF import/export

## Requirements

- Python 3.7+
- ecdsa==0.19.1 (ECDSA cryptographic signatures)
- tkinter (usually included with Python)

## Platform Support

- ✅ Windows 7+
- ✅ Linux (Ubuntu, Debian, etc.)
- ✅ macOS 10.12+

## Integration with Trinity Core

The Python wallet requires a running Trinity daemon (trinityd) for:
- Blockchain synchronization
- Transaction broadcasting
- Balance queries
- Network connectivity

Configure Trinity daemon with:
```
server=1
rpcuser=rpcuser
rpcpassword=your_password
rpcport=6420
```

## Development

The wallet is modular and extensible:

- **Core Module**: Handles cryptography and wallet operations
- **GUI Module**: Provides the user interface
- **Utils Module**: Helper functions for encoding/hashing

To contribute:
1. Fork the repository
2. Make changes in `trinity_wallet_py/`
3. Run tests: `python test_wallet.py`
4. Submit a pull request

## License

Released under MIT license. See COPYING for details.

## Support

For issues, questions, or contributions:
- Open an issue in the GitHub repository
- Check the documentation in `trinity_wallet_py/`
- Review the INSTALL.md for troubleshooting

## Changelog

### Version 1.0.0 (Initial Release)
- Full Python implementation of Trinity wallet
- Windows GUI with tkinter
- Key generation and management
- Send/receive functionality
- RPC integration with Trinity daemon
- Address book with labels
- Transaction history
- Multi-platform support
