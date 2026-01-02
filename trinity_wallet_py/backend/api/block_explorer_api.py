"""
Block Explorer API endpoints.
"""

from typing import Dict, Any, Tuple
from .base_api import BaseAPI


class BlockExplorerAPI(BaseAPI):
    """
    API endpoints for Block Explorer service.
    """
    
    def __init__(self, service):
        """
        Initialize API with Block Explorer service.
        
        Args:
            service: BlockExplorerService instance
        """
        self.service = service
    
    def get_block(self, block_hash: str) -> Tuple[str, int, Dict[str, str]]:
        """
        Get block information by hash.
        
        Args:
            block_hash: Block hash
            
        Returns:
            JSON response
        """
        if not block_hash:
            return self.error_response("Block hash is required", 400)
        
        block = self.service.get_block_by_hash(block_hash)
        
        if block is None:
            return self.error_response(f"Block not found: {block_hash}", 404)
        
        return self.success_response(block)
    
    def get_transaction(self, tx_id: str) -> Tuple[str, int, Dict[str, str]]:
        """
        Get transaction information.
        
        Args:
            tx_id: Transaction ID
            
        Returns:
            JSON response
        """
        if not tx_id:
            return self.error_response("Transaction ID is required", 400)
        
        tx = self.service.get_transaction(tx_id)
        
        if tx is None:
            return self.error_response(f"Transaction not found: {tx_id}", 404)
        
        return self.success_response(tx)
    
    def validate_address(self, address: str) -> Tuple[str, int, Dict[str, str]]:
        """
        Validate an address.
        
        Args:
            address: Trinity address
            
        Returns:
            JSON response
        """
        if not address:
            return self.error_response("Address is required", 400)
        
        result = self.service.validate_address(address)
        return self.success_response(result)
    
    def get_blockchain_info(self) -> Tuple[str, int, Dict[str, str]]:
        """
        Get blockchain information.
        
        Returns:
            JSON response
        """
        info = self.service.get_blockchain_info()
        
        if info is None:
            return self.error_response("Failed to fetch blockchain info", 500)
        
        return self.success_response(info)
    
    def search_transactions(self, address: str = "", count: int = 10) -> Tuple[str, int, Dict[str, str]]:
        """
        Search transactions.
        
        Args:
            address: Optional address to filter by
            count: Maximum number of results
            
        Returns:
            JSON response
        """
        try:
            count = int(count)
            if count < 1 or count > 100:
                return self.error_response("Count must be between 1 and 100", 400)
        except ValueError:
            return self.error_response("Invalid count parameter", 400)
        
        transactions = self.service.search_transactions(address, count)
        return self.success_response(transactions)
