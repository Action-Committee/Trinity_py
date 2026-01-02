"""
Mining Pool API endpoints.
"""

from typing import Dict, Any, Tuple
from .base_api import BaseAPI


class MiningPoolAPI(BaseAPI):
    """
    API endpoints for Mining Pool service.
    """
    
    def __init__(self, service):
        """
        Initialize API with Mining Pool service.
        
        Args:
            service: MiningPoolService instance
        """
        self.service = service
    
    def get_work(self, miner_id: str) -> Tuple[str, int, Dict[str, str]]:
        """
        Get work for a miner.
        
        Args:
            miner_id: Miner identifier
            
        Returns:
            JSON response
        """
        if not miner_id:
            return self.error_response("Miner ID is required", 400)
        
        work = self.service.get_work(miner_id)
        
        if work is None:
            return self.error_response("No work available", 503)
        
        return self.success_response(work)
    
    def submit_share(self, data: Dict[str, Any]) -> Tuple[str, int, Dict[str, str]]:
        """
        Submit a share.
        
        Args:
            data: Share submission data
            
        Returns:
            JSON response
        """
        # Validate required parameters
        valid, error_msg = self.validate_required_params(data, ['miner_id', 'share_data'])
        if not valid:
            return self.error_response(error_msg, 400)
        
        result = self.service.submit_share(data['miner_id'], data['share_data'])
        
        if result['accepted']:
            return self.success_response(result)
        else:
            return self.error_response(result.get('reason', 'Share rejected'), 400)
    
    def get_pool_stats(self) -> Tuple[str, int, Dict[str, str]]:
        """
        Get pool statistics.
        
        Returns:
            JSON response
        """
        stats = self.service.get_pool_stats()
        return self.success_response(stats)
    
    def get_miner_stats(self, miner_id: str) -> Tuple[str, int, Dict[str, str]]:
        """
        Get miner statistics.
        
        Args:
            miner_id: Miner identifier
            
        Returns:
            JSON response
        """
        if not miner_id:
            return self.error_response("Miner ID is required", 400)
        
        stats = self.service.get_miner_stats(miner_id)
        
        if stats is None:
            return self.error_response(f"Miner not found: {miner_id}", 404)
        
        return self.success_response(stats)
    
    def list_miners(self) -> Tuple[str, int, Dict[str, str]]:
        """
        List all miners.
        
        Returns:
            JSON response
        """
        miners = self.service.list_miners()
        return self.success_response(miners)
