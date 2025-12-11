"""
Wallet manager for Trinity wallet.
Manages keys, addresses, and wallet state.
"""

import json
import os
from typing import List, Dict, Optional
from pathlib import Path
from .key import Key, generate_new_key, validate_address
from .rpc_client import TrinityRPCClient


class Wallet:
    """
    Trinity wallet implementation.
    
    SECURITY NOTE: Private keys are stored in plain JSON format in the wallet file.
    The file is protected with restrictive permissions (0o600), but is not encrypted.
    Users should:
    - Keep their system secure
    - Use full-disk encryption
    - Backup wallet files securely
    - Consider using the Trinity Core wallet for encrypted storage
    """
    
    def __init__(self, wallet_path: Optional[str] = None):
        """
        Initialize wallet.
        
        Args:
            wallet_path: Path to wallet file. If None, uses default location.
        """
        if wallet_path is None:
            # Default wallet location in user's home directory
            home = Path.home()
            wallet_dir = home / '.trinity_wallet'
            wallet_dir.mkdir(mode=0o700, exist_ok=True)
            wallet_path = wallet_dir / 'wallet.json'
        
        self.wallet_path = Path(wallet_path)
        self.keys: List[Key] = []
        self.labels: Dict[str, str] = {}  # address -> label
        self.rpc_client: Optional[TrinityRPCClient] = None
        
        # Load wallet if exists
        if self.wallet_path.exists():
            self.load()
    
    def load(self):
        """Load wallet from file."""
        try:
            with open(self.wallet_path, 'r') as f:
                data = json.load(f)
            
            # Load keys
            self.keys = []
            for key_data in data.get('keys', []):
                private_key_bytes = bytes.fromhex(key_data['private_key'])
                key = Key(private_key_bytes)
                self.keys.append(key)
            
            # Load labels
            self.labels = data.get('labels', {})
            
        except Exception as e:
            raise Exception(f"Failed to load wallet: {e}")
    
    def save(self):
        """Save wallet to file."""
        try:
            data = {
                'keys': [],
                'labels': self.labels
            }
            
            # Save keys
            for key in self.keys:
                data['keys'].append({
                    'private_key': key.get_private_key_bytes().hex(),
                    'address': key.get_address()
                })
            
            # Write to file
            with open(self.wallet_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Set restrictive permissions
            os.chmod(self.wallet_path, 0o600)
            
        except Exception as e:
            raise Exception(f"Failed to save wallet: {e}")
    
    def add_new_key(self, label: str = '') -> str:
        """
        Generate and add a new key to the wallet.
        
        Args:
            label: Optional label for the address
            
        Returns:
            New address
        """
        key = generate_new_key()
        self.keys.append(key)
        address = key.get_address()
        
        if label:
            self.labels[address] = label
        
        self.save()
        return address
    
    def import_private_key(self, wif: str, label: str = '') -> str:
        """
        Import a private key.
        
        Args:
            wif: Private key in WIF format
            label: Optional label for the address
            
        Returns:
            Address
        """
        key = Key.from_wif(wif)
        self.keys.append(key)
        address = key.get_address()
        
        if label:
            self.labels[address] = label
        
        self.save()
        return address
    
    def get_addresses(self) -> List[str]:
        """Get all addresses in the wallet."""
        return [key.get_address() for key in self.keys]
    
    def get_key_for_address(self, address: str) -> Optional[Key]:
        """Get key for a specific address."""
        for key in self.keys:
            if key.get_address() == address:
                return key
        return None
    
    def get_label(self, address: str) -> str:
        """Get label for an address."""
        return self.labels.get(address, '')
    
    def set_label(self, address: str, label: str):
        """Set label for an address."""
        self.labels[address] = label
        self.save()
    
    def export_private_key(self, address: str) -> str:
        """
        Export private key for an address.
        
        Args:
            address: Address to export
            
        Returns:
            Private key in WIF format
        """
        key = self.get_key_for_address(address)
        if key is None:
            raise ValueError(f"Address not found in wallet: {address}")
        return key.get_wif()
    
    def connect_to_node(self, host='127.0.0.1', port=6420, username='', password=''):
        """
        Connect to a Trinity node via RPC.
        
        Args:
            host: Node host
            port: RPC port
            username: RPC username
            password: RPC password
        """
        self.rpc_client = TrinityRPCClient(host, port, username, password)
    
    def get_balance(self) -> float:
        """
        Get wallet balance from connected node.
        
        Returns:
            Balance in TRINITY
        """
        if self.rpc_client is None:
            raise Exception("Not connected to a node")
        return self.rpc_client.getbalance()
    
    def send_to_address(self, to_address: str, amount: float) -> str:
        """
        Send TRINITY to an address.
        
        Args:
            to_address: Destination address
            amount: Amount to send
            
        Returns:
            Transaction ID
        """
        if self.rpc_client is None:
            raise Exception("Not connected to a node")
        
        if not validate_address(to_address):
            raise ValueError(f"Invalid address: {to_address}")
        
        return self.rpc_client.sendtoaddress(to_address, amount)
    
    def get_transactions(self, count: int = 10) -> List[Dict]:
        """
        Get recent transactions.
        
        Args:
            count: Number of transactions to retrieve
            
        Returns:
            List of transactions
        """
        if self.rpc_client is None:
            raise Exception("Not connected to a node")
        return self.rpc_client.listtransactions(count=count)
    
    def get_node_info(self) -> Dict:
        """
        Get information about the connected node.
        
        Returns:
            Node information
        """
        if self.rpc_client is None:
            raise Exception("Not connected to a node")
        return self.rpc_client.getinfo()
