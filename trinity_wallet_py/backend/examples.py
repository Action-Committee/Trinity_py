#!/usr/bin/env python3
"""
Example usage of Trinity Backend Services.

This script demonstrates how to use the backend services programmatically.
"""

import time
from trinity_wallet_py.backend.config import BackendConfig
from trinity_wallet_py.backend.services.block_explorer import BlockExplorerService
from trinity_wallet_py.backend.services.mining_pool import MiningPoolService


def example_block_explorer():
    """Example: Using the Block Explorer service."""
    print("\n" + "=" * 60)
    print("Example: Block Explorer Service")
    print("=" * 60)
    
    # Create configuration
    config = {
        'rpc_host': '127.0.0.1',
        'rpc_port': 6420,
        'rpc_user': '',
        'rpc_pass': '',
        'cache_enabled': True
    }
    
    # Create service
    explorer = BlockExplorerService(config)
    
    # Get service info
    info = explorer.get_info()
    print(f"\nService: {info['name']}")
    print(f"Version: {info['version']}")
    print(f"Capabilities: {', '.join(info['capabilities'])}")
    
    # Note: Starting the service requires a running Trinity node
    print("\nNote: To use the service, you need a running Trinity node")
    print("Start Trinity daemon with: trinityd")
    print("Then the service will be able to query blockchain data")
    
    # Example API endpoints that would be available:
    print("\nAvailable API endpoints:")
    for endpoint in info['endpoints']:
        print(f"  {endpoint}")


def example_mining_pool():
    """Example: Using the Mining Pool service."""
    print("\n" + "=" * 60)
    print("Example: Mining Pool Service")
    print("=" * 60)
    
    # Create configuration
    config = {
        'rpc_host': '127.0.0.1',
        'rpc_port': 6420,
        'rpc_user': '',
        'rpc_pass': '',
        'pool_address': 'YOUR_POOL_ADDRESS',
        'pool_fee': 0.01,  # 1% fee
        'difficulty': 1.0
    }
    
    # Create service
    pool = MiningPoolService(config)
    
    # Get service info
    info = pool.get_info()
    print(f"\nService: {info['name']}")
    print(f"Version: {info['version']}")
    print(f"Capabilities: {', '.join(info['capabilities'])}")
    
    print("\nPool Configuration:")
    print(f"  Pool Fee: {config['pool_fee'] * 100}%")
    print(f"  Difficulty: {config['difficulty']}")
    
    print("\nNote: To use the mining pool, you need a running Trinity node")
    print("Configure your pool address in the config before starting")
    
    # Example mining pool workflow
    print("\nMining Pool Workflow:")
    print("  1. Miners connect and request work")
    print("  2. Pool distributes work units")
    print("  3. Miners submit shares")
    print("  4. Pool validates and tracks shares")
    print("  5. Pool calculates payouts based on shares")


def example_programmatic_server():
    """Example: Running the server programmatically."""
    print("\n" + "=" * 60)
    print("Example: Programmatic Server Usage")
    print("=" * 60)
    
    # Create custom configuration
    config = BackendConfig()
    
    # Customize settings
    config.set('server.host', '127.0.0.1')
    config.set('server.port', 5000)
    config.set('block_explorer.enabled', True)
    config.set('mining_pool.enabled', False)
    
    print("\nConfiguration:")
    print(f"  Host: {config.get('server.host')}")
    print(f"  Port: {config.get('server.port')}")
    print(f"  Block Explorer: {'Enabled' if config.get('block_explorer.enabled') else 'Disabled'}")
    print(f"  Mining Pool: {'Enabled' if config.get('mining_pool.enabled') else 'Disabled'}")
    
    # Example code to run the server (commented out)
    print("\nTo run the server programmatically:")
    print("```python")
    print("from trinity_wallet_py.backend.server import TrinityBackendServer")
    print("")
    print("server = TrinityBackendServer(config)")
    print("server.run()  # Starts on http://127.0.0.1:5000")
    print("```")


def example_api_usage():
    """Example: Using the REST API."""
    print("\n" + "=" * 60)
    print("Example: REST API Usage")
    print("=" * 60)
    
    print("\nOnce the server is running, you can access the API:")
    print("\n1. Health Check:")
    print("   curl http://127.0.0.1:5000/health")
    
    print("\n2. List Services:")
    print("   curl http://127.0.0.1:5000/api/services")
    
    print("\n3. Get Blockchain Info:")
    print("   curl http://127.0.0.1:5000/api/blockchain/info")
    
    print("\n4. Validate Address:")
    print("   curl http://127.0.0.1:5000/api/address/D.../validate")
    
    print("\n5. Get Block:")
    print("   curl http://127.0.0.1:5000/api/block/<block_hash>")
    
    print("\n6. Search Transactions:")
    print("   curl 'http://127.0.0.1:5000/api/transactions/search?address=D...&count=10'")
    
    print("\nPython Client Example:")
    print("```python")
    print("import requests")
    print("")
    print("response = requests.get('http://127.0.0.1:5000/api/blockchain/info')")
    print("data = response.json()")
    print("print(f\"Block height: {data['data']['blocks']}\")")
    print("```")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Trinity Backend Services - Usage Examples")
    print("=" * 60)
    
    example_block_explorer()
    example_mining_pool()
    example_programmatic_server()
    example_api_usage()
    
    print("\n" + "=" * 60)
    print("Getting Started")
    print("=" * 60)
    print("\n1. Install dependencies:")
    print("   pip install -e .")
    
    print("\n2. Initialize configuration:")
    print("   python -m trinity_wallet_py.backend.cli config --init")
    
    print("\n3. Start the backend server:")
    print("   python -m trinity_wallet_py.backend.cli start")
    
    print("\n4. In another terminal, check status:")
    print("   python -m trinity_wallet_py.backend.cli status")
    
    print("\n5. Access the API:")
    print("   curl http://127.0.0.1:5000/health")
    
    print("\nFor full documentation, see:")
    print("  trinity_wallet_py/backend/README.md")
    print()


if __name__ == '__main__':
    main()
