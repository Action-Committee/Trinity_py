"""
Configuration management for Trinity backend services.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class BackendConfig:
    """
    Configuration manager for backend services.
    
    Handles loading, saving, and accessing configuration for all backend services.
    """
    
    DEFAULT_CONFIG = {
        'server': {
            'host': '127.0.0.1',
            'port': 5000,
            'debug': False
        },
        'rpc': {
            'host': '127.0.0.1',
            'port': 6420,
            'username': '',
            'password': ''
        },
        'block_explorer': {
            'enabled': True,
            'cache_enabled': True
        },
        'mining_pool': {
            'enabled': False,
            'pool_address': '',
            'pool_fee': 0.01,
            'difficulty': 1.0
        },
        'security': {
            'cors_enabled': True,
            'cors_origins': ['http://localhost:*'],
            'api_key_required': False
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        if config_path is None:
            # Default config location
            home = Path.home()
            config_dir = home / '.trinity_wallet' / 'backend'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_path = config_dir / 'config.json'
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                # Merge with defaults
                return self._merge_configs(self.DEFAULT_CONFIG.copy(), config)
            except Exception as e:
                print(f"Error loading config: {e}, using defaults")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save()
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merge configuration dictionaries.
        
        Args:
            base: Base configuration
            override: Override configuration
            
        Returns:
            Merged configuration
        """
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def save(self) -> bool:
        """
        Save configuration to file.
        
        Returns:
            True if saved successfully
        """
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            # Set restrictive permissions
            os.chmod(self.config_path, 0o600)
            return True
            
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'server.host')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_service_config(self, service_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Service configuration dictionary
        """
        service_config = self.config.get(service_name, {}).copy()
        
        # Include RPC config for services that need it
        if service_name in ['block_explorer', 'mining_pool']:
            rpc_config = self.config.get('rpc', {})
            service_config.update({
                'rpc_host': rpc_config.get('host'),
                'rpc_port': rpc_config.get('port'),
                'rpc_user': rpc_config.get('username'),
                'rpc_pass': rpc_config.get('password')
            })
        
        return service_config
