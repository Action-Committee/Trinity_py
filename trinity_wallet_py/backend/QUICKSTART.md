# Trinity Backend Services - Quick Start Guide

## What are Trinity Backend Services?

Trinity Backend Services provide a modular framework for running cryptocurrency services locally or as a webserver. The framework includes:

- **Block Explorer**: Query blockchain data, blocks, and transactions
- **Mining Pool**: Manage mining operations with work distribution
- **REST API**: Full-featured API for all services
- **CLI Tools**: Easy command-line management

## Prerequisites

- Python 3.10 or higher
- Trinity daemon (trinityd) running for blockchain access
- pip (Python package manager)

## Installation

### Step 1: Install the Package

```bash
# From the repository root
pip install -e .
```

This will install all required dependencies:
- Flask (web framework)
- Flask-CORS (cross-origin support)
- Requests (HTTP client)
- ecdsa (cryptography)

### Step 2: Initialize Configuration

```bash
python -m trinity_wallet_py.backend.cli config --init
```

This creates a configuration file at `~/.trinity_wallet/backend/config.json`.

### Step 3: Start the Backend Server

```bash
python -m trinity_wallet_py.backend.cli start
```

The server will start on `http://127.0.0.1:5000`.

## Testing the Setup

### Check Server Status

In a new terminal:

```bash
python -m trinity_wallet_py.backend.cli status
```

### Test the API

```bash
# Health check
curl http://127.0.0.1:5000/health

# List services
curl http://127.0.0.1:5000/api/services
```

## Basic Usage

### Block Explorer

Query blockchain information:

```bash
# Get blockchain info
curl http://127.0.0.1:5000/api/blockchain/info

# Validate an address
curl http://127.0.0.1:5000/api/address/YOUR_ADDRESS/validate

# Search transactions
curl 'http://127.0.0.1:5000/api/transactions/search?count=10'
```

### Configuration

View and modify configuration:

```bash
# Show current config
python -m trinity_wallet_py.backend.cli config --show

# Change server port
python -m trinity_wallet_py.backend.cli config --set server.port=8000

# Enable mining pool
python -m trinity_wallet_py.backend.cli config --set mining_pool.enabled=true
```

## Running Tests

```bash
# Test backend services
python -m trinity_wallet_py.backend.cli test

# Run full test suite
python trinity_wallet_py/test_backend.py
```

## Common Tasks

### Running on a Different Port

```bash
python -m trinity_wallet_py.backend.cli start --port 8000
```

### Accessing from Other Machines

⚠️ **Security Warning**: Only expose to trusted networks!

```bash
# Listen on all interfaces
python -m trinity_wallet_py.backend.cli start --host 0.0.0.0 --port 8000
```

### Debug Mode

```bash
python -m trinity_wallet_py.backend.cli start --debug
```

## Python Client Example

```python
import requests

# Connect to backend
base_url = "http://127.0.0.1:5000"

# Get blockchain info
response = requests.get(f"{base_url}/api/blockchain/info")
data = response.json()

if data['success']:
    info = data['data']
    print(f"Block height: {info['blocks']}")
    print(f"Connections: {info['connections']}")
    print(f"Difficulty: {info['difficulty']}")
```

## Troubleshooting

### Server Won't Start

1. Check if port is already in use:
   ```bash
   netstat -tuln | grep 5000
   ```

2. Try a different port:
   ```bash
   python -m trinity_wallet_py.backend.cli start --port 8000
   ```

### Can't Connect to Trinity Node

1. Ensure Trinity daemon is running:
   ```bash
   ps aux | grep trinityd
   ```

2. Check RPC configuration in `~/.trinity_wallet/backend/config.json`

3. Test RPC connection manually:
   ```bash
   curl --user USER:PASS http://127.0.0.1:6420 -d '{"method":"getinfo"}'
   ```

### API Returns Errors

1. Check service status:
   ```bash
   python -m trinity_wallet_py.backend.cli status
   ```

2. View logs in the terminal where server is running

## Next Steps

- Read the [full documentation](README.md)
- Explore [usage examples](examples.py)
- Configure mining pool settings
- Set up custom RPC credentials
- Deploy as a systemd service

## Security Notes

- **Local Use Only**: By default, services bind to 127.0.0.1
- **No Encryption**: RPC uses HTTP - only use on localhost or via SSH tunnel
- **No Authentication**: API has no auth by default
- **Firewall**: Configure firewall rules if exposing externally

## Getting Help

- Documentation: `trinity_wallet_py/backend/README.md`
- Examples: `python trinity_wallet_py/backend/examples.py`
- Issues: Report on GitHub

## License

MIT License - See COPYING for details
