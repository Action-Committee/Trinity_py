"""
Block Explorer Service for Trinity.

Provides blockchain exploration capabilities including block and transaction lookups.
"""

from typing import Dict, Any, Optional, List
from .base_service import BaseService
from ...core.rpc_client import TrinityRPCClient


class BlockExplorerService(BaseService):
    """
    Block Explorer service implementation.
    
    Provides API for querying blockchain data including blocks, transactions,
    and addresses.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Block Explorer service.
        
        Args:
            config: Service configuration with RPC connection details
        """
        super().__init__("block_explorer", config)
        
        # Initialize RPC client
        rpc_host = self.config.get('rpc_host', '127.0.0.1')
        rpc_port = self.config.get('rpc_port', 6420)
        rpc_user = self.config.get('rpc_user', '')
        rpc_pass = self.config.get('rpc_pass', '')
        
        self.rpc = TrinityRPCClient(
            host=rpc_host,
            port=rpc_port,
            username=rpc_user,
            password=rpc_pass
        )
        
        self.cache_enabled = self.config.get('cache_enabled', True)
        self._block_cache: Dict[str, Any] = {}
        self._tx_cache: Dict[str, Any] = {}
    
    def start(self) -> bool:
        """
        Start the Block Explorer service.
        
        Returns:
            True if started successfully
        """
        try:
            self.logger.info("Starting Block Explorer service...")
            
            # Test RPC connection
            info = self.rpc.getinfo()
            self.logger.info(f"Connected to Trinity node: {info}")
            
            self._running = True
            self.logger.info("Block Explorer service started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Block Explorer service: {e}")
            self._running = False
            return False
    
    def stop(self) -> bool:
        """
        Stop the Block Explorer service.
        
        Returns:
            True if stopped successfully
        """
        try:
            self.logger.info("Stopping Block Explorer service...")
            
            # Clear caches
            self._block_cache.clear()
            self._tx_cache.clear()
            
            self._running = False
            self.logger.info("Block Explorer service stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping Block Explorer service: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get Block Explorer service status.
        
        Returns:
            Status information dictionary
        """
        status = {
            'service': self.name,
            'running': self._running,
            'cache_enabled': self.cache_enabled,
            'cached_blocks': len(self._block_cache),
            'cached_transactions': len(self._tx_cache)
        }
        
        if self._running:
            try:
                info = self.rpc.getinfo()
                status['node_info'] = info
                status['block_count'] = self.rpc.getblockcount()
            except Exception as e:
                status['error'] = str(e)
        
        return status
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get Block Explorer service information.
        
        Returns:
            Service information dictionary
        """
        return {
            'name': self.name,
            'version': '1.0.0',
            'description': 'Trinity Block Explorer Service',
            'capabilities': [
                'block_lookup',
                'transaction_lookup',
                'address_validation',
                'blockchain_info'
            ],
            'endpoints': [
                '/api/block/<block_hash>',
                '/api/transaction/<tx_id>',
                '/api/address/<address>',
                '/api/blockchain/info'
            ]
        }
    
    # Block Explorer specific methods
    
    def get_block_by_hash(self, block_hash: str) -> Optional[Dict[str, Any]]:
        """
        Get block information by hash.
        
        Args:
            block_hash: Block hash
            
        Returns:
            Block data or None if not found
        """
        if not self._running:
            return None
        
        # Check cache
        if self.cache_enabled and block_hash in self._block_cache:
            return self._block_cache[block_hash]
        
        try:
            block = self.rpc.getblock(block_hash)
            
            # Cache the result
            if self.cache_enabled:
                self._block_cache[block_hash] = block
            
            return block
            
        except Exception as e:
            self.logger.error(f"Error fetching block {block_hash}: {e}")
            return None
    
    def get_transaction(self, tx_id: str) -> Optional[Dict[str, Any]]:
        """
        Get transaction information.
        
        Args:
            tx_id: Transaction ID
            
        Returns:
            Transaction data or None if not found
        """
        if not self._running:
            return None
        
        # Check cache
        if self.cache_enabled and tx_id in self._tx_cache:
            return self._tx_cache[tx_id]
        
        try:
            tx = self.rpc.gettransaction(tx_id)
            
            # Cache the result
            if self.cache_enabled:
                self._tx_cache[tx_id] = tx
            
            return tx
            
        except Exception as e:
            self.logger.error(f"Error fetching transaction {tx_id}: {e}")
            return None
    
    def validate_address(self, address: str) -> Dict[str, Any]:
        """
        Validate a Trinity address.
        
        Args:
            address: Trinity address to validate
            
        Returns:
            Validation result dictionary
        """
        if not self._running:
            return {'valid': False, 'error': 'Service not running'}
        
        try:
            result = self.rpc.validateaddress(address)
            return result
            
        except Exception as e:
            self.logger.error(f"Error validating address {address}: {e}")
            return {'valid': False, 'error': str(e)}
    
    def get_blockchain_info(self) -> Optional[Dict[str, Any]]:
        """
        Get general blockchain information.
        
        Returns:
            Blockchain info dictionary or None if error
        """
        if not self._running:
            return None
        
        try:
            info = self.rpc.getinfo()
            block_count = self.rpc.getblockcount()
            mining_info = self.rpc.getmininginfo()
            
            return {
                'blocks': block_count,
                'connections': info.get('connections', 0),
                'difficulty': mining_info.get('difficulty', 0),
                'version': info.get('version', 'unknown'),
                'protocol_version': info.get('protocolversion', 0)
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching blockchain info: {e}")
            return None
    
    def search_transactions(self, address: str, count: int = 10) -> List[Dict[str, Any]]:
        """
        Search transactions for an address.
        
        Args:
            address: Trinity address
            count: Maximum number of transactions to return
            
        Returns:
            List of transactions
        """
        if not self._running:
            return []
        
        try:
            transactions = self.rpc.listtransactions('*', count, 0)
            
            # Filter by address if provided
            if address:
                transactions = [
                    tx for tx in transactions 
                    if tx.get('address') == address
                ]
            
            return transactions
            
        except Exception as e:
            self.logger.error(f"Error searching transactions: {e}")
            return []
