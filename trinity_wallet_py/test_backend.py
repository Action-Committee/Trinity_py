#!/usr/bin/env python3
"""
Test script for Trinity Backend Services.

Tests service initialization, configuration, and basic functionality.
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trinity_wallet_py.backend.config import BackendConfig
from trinity_wallet_py.backend.services.base_service import BaseService
from trinity_wallet_py.backend.services.block_explorer import BlockExplorerService
from trinity_wallet_py.backend.services.mining_pool import MiningPoolService
from trinity_wallet_py.backend.server import TrinityBackendServer


class MockService(BaseService):
    """Mock service for testing base service functionality."""
    
    def start(self):
        self._running = True
        return True
    
    def stop(self):
        self._running = False
        return True
    
    def get_status(self):
        return {'running': self._running}
    
    def get_info(self):
        return {'name': self.name, 'version': '1.0.0'}


def test_config():
    """Test configuration management."""
    print("Testing Backend Configuration...")
    
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_path = f.name
    
    try:
        # Initialize config
        config = BackendConfig(config_path)
        assert config.config is not None, "Config not initialized"
        print("  ✓ Config initialized")
        
        # Test default values
        assert config.get('server.host') == '127.0.0.1', "Default host incorrect"
        assert config.get('server.port') == 5000, "Default port incorrect"
        print("  ✓ Default values correct")
        
        # Test set and get
        config.set('server.port', 8000)
        assert config.get('server.port') == 8000, "Set/Get failed"
        print("  ✓ Set/Get works")
        
        # Test save and reload
        config.save()
        config2 = BackendConfig(config_path)
        assert config2.get('server.port') == 8000, "Save/Load failed"
        print("  ✓ Save/Load works")
        
        # Test service config
        service_config = config.get_service_config('block_explorer')
        assert 'rpc_host' in service_config, "Service config missing RPC info"
        print("  ✓ Service config generation works")
        
    finally:
        # Cleanup
        if os.path.exists(config_path):
            os.unlink(config_path)
    
    print("✓ Configuration tests passed\n")


def test_base_service():
    """Test base service functionality."""
    print("Testing Base Service...")
    
    # Create mock service
    service = MockService("test_service", {'key': 'value'})
    
    # Test initialization
    assert service.name == "test_service", "Service name incorrect"
    assert service.config['key'] == 'value', "Service config incorrect"
    assert not service.is_running(), "Service should not be running initially"
    print("  ✓ Service initialization correct")
    
    # Test start/stop
    assert service.start(), "Service start failed"
    assert service.is_running(), "Service should be running"
    print("  ✓ Service start works")
    
    assert service.stop(), "Service stop failed"
    assert not service.is_running(), "Service should not be running"
    print("  ✓ Service stop works")
    
    # Test configure
    service.configure({'new_key': 'new_value'})
    assert service.config['new_key'] == 'new_value', "Configure failed"
    print("  ✓ Service configuration update works")
    
    # Test status and info
    status = service.get_status()
    assert 'running' in status, "Status missing 'running' key"
    print("  ✓ Get status works")
    
    info = service.get_info()
    assert info['name'] == 'test_service', "Info name incorrect"
    print("  ✓ Get info works")
    
    print("✓ Base service tests passed\n")


def test_block_explorer_service():
    """Test Block Explorer service."""
    print("Testing Block Explorer Service...")
    
    # Create service with mock RPC config
    config = {
        'rpc_host': '127.0.0.1',
        'rpc_port': 6420,
        'rpc_user': 'test',
        'rpc_pass': 'test',
        'cache_enabled': True
    }
    
    service = BlockExplorerService(config)
    
    # Test initialization
    assert service.name == "block_explorer", "Service name incorrect"
    assert service.cache_enabled, "Cache should be enabled"
    print("  ✓ Block Explorer initialized")
    
    # Test info
    info = service.get_info()
    assert 'capabilities' in info, "Info missing capabilities"
    assert 'block_lookup' in info['capabilities'], "Missing block_lookup capability"
    print("  ✓ Service info correct")
    
    # Test status when not running
    status = service.get_status()
    assert not status['running'], "Service should not be running"
    print("  ✓ Status correct when not running")
    
    # Note: We can't test actual RPC calls without a running Trinity node
    print("  ℹ Skipping RPC tests (requires running Trinity node)")
    
    print("✓ Block Explorer service tests passed\n")


def test_mining_pool_service():
    """Test Mining Pool service."""
    print("Testing Mining Pool Service...")
    
    # Create service with mock config
    config = {
        'rpc_host': '127.0.0.1',
        'rpc_port': 6420,
        'rpc_user': 'test',
        'rpc_pass': 'test',
        'pool_address': 'D...',
        'pool_fee': 0.01,
        'difficulty': 1.0
    }
    
    service = MiningPoolService(config)
    
    # Test initialization
    assert service.name == "mining_pool", "Service name incorrect"
    assert service.pool_fee == 0.01, "Pool fee incorrect"
    assert service.difficulty == 1.0, "Difficulty incorrect"
    print("  ✓ Mining Pool initialized")
    
    # Test info
    info = service.get_info()
    assert 'capabilities' in info, "Info missing capabilities"
    assert 'work_distribution' in info['capabilities'], "Missing work_distribution capability"
    print("  ✓ Service info correct")
    
    # Test miner management (simulate running state for testing without RPC)
    # Note: We test the internal logic without actually starting the service
    # which would require a Trinity node connection
    
    # Manually set running state for internal logic testing
    service._running = True
    
    # Test get work
    work = service.get_work('miner_001')
    assert 'miner_001' in service.miners, "Miner not registered"
    print("  ✓ Miner registration works")
    
    # Test miner stats
    stats = service.get_miner_stats('miner_001')
    assert stats is not None, "Miner stats not returned"
    assert stats['miner_id'] == 'miner_001', "Miner ID incorrect"
    print("  ✓ Miner stats work")
    
    # Test pool stats
    pool_stats = service.get_pool_stats()
    assert 'total_miners' in pool_stats, "Pool stats missing total_miners"
    assert pool_stats['total_miners'] == 1, "Total miners incorrect"
    print("  ✓ Pool stats work")
    
    # Clean up
    service._running = False
    
    print("✓ Mining Pool service tests passed\n")


def test_server_initialization():
    """Test server initialization."""
    print("Testing Server Initialization...")
    
    # Create temporary config
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_path = f.name
    
    try:
        # Create config
        config = BackendConfig(config_path)
        
        # Test server creation
        server = TrinityBackendServer(config)
        assert server.app is not None, "Flask app not created"
        assert len(server.services) > 0, "No services initialized"
        print("  ✓ Server initialized with services")
        
        # Check that block explorer is enabled by default
        assert 'block_explorer' in server.services, "Block explorer not enabled"
        print("  ✓ Block explorer service registered")
        
        # Check that mining pool is disabled by default
        mining_pool_enabled = 'mining_pool' in server.services
        if not mining_pool_enabled:
            print("  ✓ Mining pool service disabled by default")
        
        # Test Flask app routes
        client = server.app.test_client()
        
        # Test root endpoint
        response = client.get('/')
        assert response.status_code == 200, "Root endpoint failed"
        data = json.loads(response.data)
        assert 'name' in data, "Root response missing name"
        print("  ✓ Root endpoint works")
        
        # Test health endpoint
        response = client.get('/health')
        assert response.status_code == 200, "Health endpoint failed"
        data = json.loads(response.data)
        assert 'status' in data, "Health response missing status"
        print("  ✓ Health endpoint works")
        
        # Test services list endpoint
        response = client.get('/api/services')
        assert response.status_code == 200, "Services endpoint failed"
        data = json.loads(response.data)
        assert 'services' in data, "Services response missing services"
        print("  ✓ Services list endpoint works")
        
    finally:
        # Cleanup
        if os.path.exists(config_path):
            os.unlink(config_path)
    
    print("✓ Server initialization tests passed\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Trinity Backend Services - Component Tests")
    print("=" * 60)
    print()
    
    try:
        test_config()
        test_base_service()
        test_block_explorer_service()
        test_mining_pool_service()
        test_server_initialization()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print()
        print("The Trinity Backend Services are working correctly!")
        print()
        print("To start the backend server, run:")
        print("  python -m trinity_wallet_py.backend.cli start")
        print()
        print("For more information, see:")
        print("  trinity_wallet_py/backend/README.md")
        return 0
    
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ TEST FAILED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
