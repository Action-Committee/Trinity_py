# Trinity Backend Services Documentation

## Overview

The Trinity Backend Services framework provides modular cryptocurrency services that can run locally or be deployed as a webserver. This framework includes:

- **Block Explorer Service**: Query blockchain data including blocks, transactions, and addresses
- **Mining Pool Service**: Manage mining operations with work distribution and share tracking
- **REST API**: Full-featured API for accessing all services
- **Local Execution**: Run services locally for development and testing

## Architecture

The backend framework is designed with a modular architecture:

```
trinity_wallet_py/backend/
├── __init__.py              # Package initialization
├── server.py                # Flask web server
├── cli.py                   # Command-line interface
├── config/                  # Configuration management
│   └── __init__.py
├── services/                # Service implementations
│   ├── __init__.py
│   ├── base_service.py      # Base service class
│   ├── block_explorer.py    # Block explorer service
│   └── mining_pool.py       # Mining pool service
└── api/                     # REST API endpoints
    ├── __init__.py
    ├── base_api.py
    ├── block_explorer_api.py
    └── mining_pool_api.py
```

## Installation

### Install Dependencies

```bash
# From the repository root
pip install -e .

# Or install directly from requirements
cd trinity_wallet_py
pip install -r requirements.txt
```

### Required Dependencies

- Python 3.10+
- Flask 2.3.0+
- Flask-CORS 4.0.0+
- Requests 2.31.0+
- ecdsa 0.19.1

## Quick Start

### 1. Initialize Configuration

```bash
python -m trinity_wallet_py.backend.cli config --init
```

This creates a default configuration file at `~/.trinity_wallet/backend/config.json`.

### 2. Start the Backend Server

```bash
python -m trinity_wallet_py.backend.cli start
```

The server will start on `http://127.0.0.1:5000` by default.

### 3. Check Server Status

```bash
python -m trinity_wallet_py.backend.cli status
```

## Configuration

### Configuration File

The configuration file is stored at `~/.trinity_wallet/backend/config.json`:

```json
{
  "server": {
    "host": "127.0.0.1",
    "port": 5000,
    "debug": false
  },
  "rpc": {
    "host": "127.0.0.1",
    "port": 6420,
    "username": "",
    "password": ""
  },
  "block_explorer": {
    "enabled": true,
    "cache_enabled": true
  },
  "mining_pool": {
    "enabled": false,
    "pool_address": "",
    "pool_fee": 0.01,
    "difficulty": 1.0
  },
  "security": {
    "cors_enabled": true,
    "cors_origins": ["http://localhost:*"],
    "api_key_required": false
  }
}
```

### Managing Configuration

```bash
# Show current configuration
python -m trinity_wallet_py.backend.cli config --show

# Set a configuration value
python -m trinity_wallet_py.backend.cli config --set server.port=8000

# Get a specific value
python -m trinity_wallet_py.backend.cli config --get server.host
```

## Services

### Block Explorer Service

The Block Explorer service provides blockchain query capabilities.

**Features:**
- Block lookup by hash
- Transaction lookup by ID
- Address validation
- Blockchain information
- Transaction search
- Response caching for improved performance

**Configuration:**
```json
{
  "block_explorer": {
    "enabled": true,
    "cache_enabled": true
  }
}
```

### Mining Pool Service

The Mining Pool service manages mining operations.

**Features:**
- Work distribution to miners
- Share submission and validation
- Miner tracking and statistics
- Pool statistics
- Configurable pool fee and difficulty

**Configuration:**
```json
{
  "mining_pool": {
    "enabled": true,
    "pool_address": "YOUR_TRINITY_ADDRESS",
    "pool_fee": 0.01,
    "difficulty": 1.0
  }
}
```

## API Endpoints

### General Endpoints

#### GET /
Returns server information.

```json
{
  "name": "Trinity Backend Server",
  "version": "1.0.0",
  "services": ["block_explorer", "mining_pool"]
}
```

#### GET /health
Health check endpoint.

```json
{
  "status": "healthy",
  "services": {
    "block_explorer": true,
    "mining_pool": false
  }
}
```

#### GET /api/services
List all services with their status.

### Block Explorer API

#### GET /api/block/<block_hash>
Get block information by hash.

**Response:**
```json
{
  "success": true,
  "data": {
    "hash": "...",
    "height": 12345,
    "transactions": [...],
    ...
  }
}
```

#### GET /api/transaction/<tx_id>
Get transaction information.

**Response:**
```json
{
  "success": true,
  "data": {
    "txid": "...",
    "amount": 10.5,
    "confirmations": 6,
    ...
  }
}
```

#### GET /api/address/<address>/validate
Validate a Trinity address.

**Response:**
```json
{
  "success": true,
  "data": {
    "valid": true,
    "address": "D...",
    ...
  }
}
```

#### GET /api/blockchain/info
Get general blockchain information.

**Response:**
```json
{
  "success": true,
  "data": {
    "blocks": 123456,
    "connections": 8,
    "difficulty": 1234.56,
    "version": "1.0.0"
  }
}
```

#### GET /api/transactions/search?address=<address>&count=<count>
Search transactions.

**Query Parameters:**
- `address` (optional): Filter by address
- `count` (optional, default=10): Number of results (1-100)

### Mining Pool API

#### GET /api/pool/work?miner_id=<miner_id>
Get work for a miner.

**Query Parameters:**
- `miner_id` (required): Unique miner identifier

**Response:**
```json
{
  "success": true,
  "data": {
    "work_id": 123,
    "timestamp": 1234567890,
    "difficulty": 1.0
  }
}
```

#### POST /api/pool/submit
Submit a share.

**Request Body:**
```json
{
  "miner_id": "miner_123",
  "share_data": {
    "work_id": 123,
    ...
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "accepted": true,
    "reason": "Valid share"
  }
}
```

#### GET /api/pool/stats
Get pool statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_miners": 10,
    "active_miners": 5,
    "total_shares": 1000,
    "blocks_found": 5,
    "pool_fee": 0.01
  }
}
```

#### GET /api/pool/miner/<miner_id>
Get statistics for a specific miner.

#### GET /api/pool/miners
List all registered miners.

## Usage Examples

### Running the Server

#### Start with default settings:
```bash
python -m trinity_wallet_py.backend.cli start
```

#### Start on a different host/port:
```bash
python -m trinity_wallet_py.backend.cli start --host 0.0.0.0 --port 8000
```

#### Start in debug mode:
```bash
python -m trinity_wallet_py.backend.cli start --debug
```

### Using the API

#### Example: Get blockchain info
```bash
curl http://127.0.0.1:5000/api/blockchain/info
```

#### Example: Validate an address
```bash
curl http://127.0.0.1:5000/api/address/D.../validate
```

#### Example: Get mining work
```bash
curl "http://127.0.0.1:5000/api/pool/work?miner_id=miner_001"
```

### Python Client Example

```python
import requests

# Base URL
base_url = "http://127.0.0.1:5000"

# Get blockchain info
response = requests.get(f"{base_url}/api/blockchain/info")
data = response.json()
print(f"Current block height: {data['data']['blocks']}")

# Validate address
address = "D..."
response = requests.get(f"{base_url}/api/address/{address}/validate")
data = response.json()
print(f"Address valid: {data['data']['valid']}")
```

## Testing

### Test Backend Services

```bash
python -m trinity_wallet_py.backend.cli test
```

This will test:
- Configuration loading
- Service initialization
- Basic functionality

### Manual Testing

1. Start the server:
   ```bash
   python -m trinity_wallet_py.backend.cli start
   ```

2. In another terminal, check status:
   ```bash
   python -m trinity_wallet_py.backend.cli status
   ```

3. Test API endpoints:
   ```bash
   curl http://127.0.0.1:5000/health
   curl http://127.0.0.1:5000/api/services
   ```

## Security Considerations

### SECURITY NOTES

1. **Local Use**: The backend server is designed for local use (127.0.0.1) by default
2. **RPC Communication**: RPC connections use unencrypted HTTP - only use on localhost or through secure tunnels
3. **CORS**: CORS is enabled by default for localhost origins
4. **API Authentication**: No API key authentication by default - enable if exposing externally
5. **Configuration Files**: Stored with restrictive permissions (0o600)

### Best Practices

1. **Never expose to the internet** without proper security measures
2. **Use SSH tunneling** for remote access
3. **Configure firewall rules** appropriately
4. **Keep configuration files secure**
5. **Use strong RPC credentials**

## Backward Compatibility

The backend services are completely separate from the existing wallet functionality:

- **No changes to wallet code**: All wallet functionality remains unchanged
- **No consensus changes**: Backend services are read-only and don't affect blockchain consensus
- **Independent operation**: Services can be enabled/disabled independently
- **Existing tests pass**: All existing wallet tests continue to work

## Advanced Setup

### Running as a Service

For production deployment, you can run the backend as a systemd service:

```ini
[Unit]
Description=Trinity Backend Server
After=network.target

[Service]
Type=simple
User=trinity
WorkingDirectory=/home/trinity
ExecStart=/usr/bin/python3 -m trinity_wallet_py.backend.cli start
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Using a Custom Configuration

```bash
# Create custom config
cp ~/.trinity_wallet/backend/config.json /path/to/custom-config.json

# Edit as needed
nano /path/to/custom-config.json

# Run with custom config
python -m trinity_wallet_py.backend.cli start -c /path/to/custom-config.json
```

### Integrating with Existing Applications

```python
from trinity_wallet_py.backend import TrinityBackendServer
from trinity_wallet_py.backend.config import BackendConfig

# Create custom configuration
config = BackendConfig()
config.set('server.port', 8000)
config.set('block_explorer.cache_enabled', False)

# Create and run server
server = TrinityBackendServer(config)
server.run()
```

## Troubleshooting

### Server won't start

1. Check if port is already in use:
   ```bash
   netstat -tuln | grep 5000
   ```

2. Check RPC connection:
   - Ensure Trinity daemon is running
   - Verify RPC credentials in config

### Service shows as not running

1. Check logs for errors
2. Verify RPC configuration
3. Test RPC connection manually

### Cannot connect to API

1. Verify server is running:
   ```bash
   python -m trinity_wallet_py.backend.cli status
   ```

2. Check firewall settings
3. Verify host/port configuration

## Contributing

To add new services:

1. Create a new service class inheriting from `BaseService`
2. Implement required methods: `start()`, `stop()`, `get_status()`, `get_info()`
3. Create corresponding API endpoints
4. Register the service in `server.py`
5. Add configuration options
6. Update documentation

## License

Trinity is released under the MIT license. See COPYING for details.
