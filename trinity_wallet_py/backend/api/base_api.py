"""
Base API functionality for Trinity backend services.
"""

from typing import Dict, Any, Tuple
import json


class BaseAPI:
    """
    Base class for API endpoints.
    
    Provides common response formatting and error handling.
    """
    
    @staticmethod
    def success_response(data: Any, status: int = 200) -> Tuple[str, int, Dict[str, str]]:
        """
        Create a successful JSON response.
        
        Args:
            data: Response data
            status: HTTP status code
            
        Returns:
            Tuple of (response_body, status_code, headers)
        """
        response = {
            'success': True,
            'data': data
        }
        return json.dumps(response), status, {'Content-Type': 'application/json'}
    
    @staticmethod
    def error_response(message: str, status: int = 400) -> Tuple[str, int, Dict[str, str]]:
        """
        Create an error JSON response.
        
        Args:
            message: Error message
            status: HTTP status code
            
        Returns:
            Tuple of (response_body, status_code, headers)
        """
        response = {
            'success': False,
            'error': message
        }
        return json.dumps(response), status, {'Content-Type': 'application/json'}
    
    @staticmethod
    def validate_required_params(data: Dict[str, Any], required: list) -> Tuple[bool, str]:
        """
        Validate that required parameters are present.
        
        Args:
            data: Request data dictionary
            required: List of required parameter names
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        missing = [param for param in required if param not in data]
        
        if missing:
            return False, f"Missing required parameters: {', '.join(missing)}"
        
        return True, ""
