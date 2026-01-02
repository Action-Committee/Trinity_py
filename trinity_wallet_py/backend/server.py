"""
Trinity Backend Web Server

Flask-based web server for Trinity backend services.
Provides REST API endpoints for block explorer and mining pool services.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from typing import Dict, Any, Optional

from .services.block_explorer import BlockExplorerService
from .services.mining_pool import MiningPoolService
from .api import BlockExplorerAPI, MiningPoolAPI
from .config import BackendConfig


class TrinityBackendServer:
    """
    Trinity backend web server.
    
    Manages service lifecycle and provides REST API endpoints.
    """
    
    def __init__(self, config: Optional[BackendConfig] = None):
        """
        Initialize the backend server.
        
        Args:
            config: Backend configuration
        """
        self.config = config or BackendConfig()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('trinity.backend.server')
        
        # Initialize Flask app
        self.app = Flask(__name__)
        
        # Configure CORS
        if self.config.get('security.cors_enabled', True):
            cors_origins = self.config.get('security.cors_origins', ['http://localhost:*'])
            CORS(self.app, origins=cors_origins)
        
        # Initialize services
        self.services: Dict[str, Any] = {}
        self.apis: Dict[str, Any] = {}
        
        self._init_services()
        self._register_routes()
    
    def _init_services(self):
        """Initialize backend services based on configuration."""
        # Block Explorer Service
        if self.config.get('block_explorer.enabled', True):
            self.logger.info("Initializing Block Explorer service...")
            explorer_config = self.config.get_service_config('block_explorer')
            self.services['block_explorer'] = BlockExplorerService(explorer_config)
            self.apis['block_explorer'] = BlockExplorerAPI(self.services['block_explorer'])
        
        # Mining Pool Service
        if self.config.get('mining_pool.enabled', False):
            self.logger.info("Initializing Mining Pool service...")
            pool_config = self.config.get_service_config('mining_pool')
            self.services['mining_pool'] = MiningPoolService(pool_config)
            self.apis['mining_pool'] = MiningPoolAPI(self.services['mining_pool'])
    
    def _register_routes(self):
        """Register API routes."""
        
        # Root endpoint
        @self.app.route('/')
        def index():
            return jsonify({
                'name': 'Trinity Backend Server',
                'version': '1.0.0',
                'services': list(self.services.keys())
            })
        
        # Health check endpoint
        @self.app.route('/health')
        def health():
            return jsonify({
                'status': 'healthy',
                'services': {
                    name: service.is_running()
                    for name, service in self.services.items()
                }
            })
        
        # Service status endpoints
        @self.app.route('/api/services')
        def list_services():
            return jsonify({
                'services': [
                    {
                        'name': name,
                        'running': service.is_running(),
                        'info': service.get_info()
                    }
                    for name, service in self.services.items()
                ]
            })
        
        @self.app.route('/api/services/<service_name>/status')
        def service_status(service_name):
            if service_name not in self.services:
                return jsonify({'error': 'Service not found'}), 404
            
            service = self.services[service_name]
            return jsonify(service.get_status())
        
        # Block Explorer API routes
        if 'block_explorer' in self.apis:
            api = self.apis['block_explorer']
            
            @self.app.route('/api/block/<block_hash>')
            def get_block(block_hash):
                return api.get_block(block_hash)
            
            @self.app.route('/api/transaction/<tx_id>')
            def get_transaction(tx_id):
                return api.get_transaction(tx_id)
            
            @self.app.route('/api/address/<address>/validate')
            def validate_address(address):
                return api.validate_address(address)
            
            @self.app.route('/api/blockchain/info')
            def blockchain_info():
                return api.get_blockchain_info()
            
            @self.app.route('/api/transactions/search')
            def search_transactions():
                address = request.args.get('address', '')
                count = request.args.get('count', 10)
                return api.search_transactions(address, count)
        
        # Mining Pool API routes
        if 'mining_pool' in self.apis:
            api = self.apis['mining_pool']
            
            @self.app.route('/api/pool/work')
            def get_work():
                miner_id = request.args.get('miner_id')
                if not miner_id:
                    return jsonify({'error': 'miner_id required'}), 400
                return api.get_work(miner_id)
            
            @self.app.route('/api/pool/submit', methods=['POST'])
            def submit_share():
                data = request.get_json()
                return api.submit_share(data)
            
            @self.app.route('/api/pool/stats')
            def pool_stats():
                return api.get_pool_stats()
            
            @self.app.route('/api/pool/miners')
            def list_miners():
                return api.list_miners()
            
            @self.app.route('/api/pool/miner/<miner_id>')
            def miner_stats(miner_id):
                return api.get_miner_stats(miner_id)
    
    def start_services(self) -> bool:
        """
        Start all enabled services.
        
        Returns:
            True if all services started successfully
        """
        self.logger.info("Starting backend services...")
        
        all_started = True
        for name, service in self.services.items():
            self.logger.info(f"Starting {name}...")
            if not service.start():
                self.logger.error(f"Failed to start {name}")
                all_started = False
        
        return all_started
    
    def stop_services(self):
        """Stop all running services."""
        self.logger.info("Stopping backend services...")
        
        for name, service in self.services.items():
            if service.is_running():
                self.logger.info(f"Stopping {name}...")
                service.stop()
    
    def run(self, host: Optional[str] = None, port: Optional[int] = None, debug: Optional[bool] = None):
        """
        Run the web server.
        
        Args:
            host: Server host (defaults to config value)
            port: Server port (defaults to config value)
            debug: Debug mode (defaults to config value)
        """
        # Start services
        self.start_services()
        
        # Get server configuration
        host = host or self.config.get('server.host', '127.0.0.1')
        port = port or self.config.get('server.port', 5000)
        debug = debug if debug is not None else self.config.get('server.debug', False)
        
        try:
            self.logger.info(f"Starting Trinity Backend Server on {host}:{port}")
            self.app.run(host=host, port=port, debug=debug)
        finally:
            self.stop_services()


def main():
    """Main entry point for the backend server."""
    import sys
    
    # Parse command line arguments
    config_path = None
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    # Load configuration
    config = BackendConfig(config_path)
    
    # Create and run server
    server = TrinityBackendServer(config)
    server.run()


if __name__ == '__main__':
    main()
