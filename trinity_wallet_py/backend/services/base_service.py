"""
Base service class for all Trinity backend services.
Provides common functionality and interface for service implementations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging


class BaseService(ABC):
    """
    Abstract base class for Trinity backend services.
    
    All services should inherit from this class and implement the required methods.
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the service.
        
        Args:
            name: Service name
            config: Service configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"trinity.backend.{name}")
        self._running = False
    
    @abstractmethod
    def start(self) -> bool:
        """
        Start the service.
        
        Returns:
            True if service started successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """
        Stop the service.
        
        Returns:
            True if service stopped successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        Get current service status.
        
        Returns:
            Dictionary containing service status information
        """
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """
        Get service information.
        
        Returns:
            Dictionary containing service metadata and information
        """
        pass
    
    def is_running(self) -> bool:
        """
        Check if service is running.
        
        Returns:
            True if service is running, False otherwise
        """
        return self._running
    
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Update service configuration.
        
        Args:
            config: New configuration dictionary
        """
        self.config.update(config)
        self.logger.info(f"Service {self.name} configuration updated")
