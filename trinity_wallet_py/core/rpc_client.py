"""
RPC client for communicating with Trinity daemon.
"""

import json
import base64
import http.client
from typing import Any, Dict, Optional


class TrinityRPCClient:
    """
    Client for Trinity RPC interface.
    
    SECURITY NOTE: This client uses unencrypted HTTP for RPC communication.
    This is acceptable for localhost connections (127.0.0.1) but should NOT
    be used over untrusted networks. For remote connections, use SSH tunneling
    or a VPN to secure the connection.
    """
    
    def __init__(self, host='127.0.0.1', port=6420, username='', password=''):
        """
        Initialize RPC client.
        
        Args:
            host: Trinity daemon host
            port: RPC port (default 6420)
            username: RPC username
            password: RPC password
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.obj_id = 0
    
    def _call(self, method: str, params: list = None) -> Any:
        """
        Make an RPC call.
        
        Args:
            method: RPC method name
            params: Method parameters
            
        Returns:
            Result from RPC call
        """
        if params is None:
            params = []
        
        self.obj_id += 1
        
        # Build request
        request_data = {
            'version': '1.1',
            'method': method,
            'params': params,
            'id': self.obj_id
        }
        
        # Create HTTP connection
        conn = http.client.HTTPConnection(self.host, self.port, timeout=30)
        
        try:
            # Prepare authorization header
            auth_string = f"{self.username}:{self.password}"
            auth_bytes = auth_string.encode('utf-8')
            auth_header = base64.b64encode(auth_bytes).decode('ascii')
            
            headers = {
                'Authorization': f'Basic {auth_header}',
                'Content-type': 'application/json'
            }
            
            # Make request
            conn.request('POST', '/', json.dumps(request_data), headers)
            response = conn.getresponse()
            
            if response.status != 200:
                raise Exception(f"HTTP error {response.status}: {response.reason}")
            
            # Parse response
            body = response.read().decode('utf-8')
            response_data = json.loads(body)
            
            if 'error' in response_data and response_data['error'] is not None:
                raise Exception(f"RPC error: {response_data['error']}")
            
            if 'result' not in response_data:
                raise Exception("No result in response")
            
            return response_data['result']
        
        finally:
            conn.close()
    
    # Wallet methods
    
    def getinfo(self) -> Dict:
        """Get general information about the wallet and network."""
        return self._call('getinfo')
    
    def getbalance(self, account: str = '*', minconf: int = 1) -> float:
        """Get wallet balance."""
        return self._call('getbalance', [account, minconf])
    
    def getnewaddress(self, account: str = '') -> str:
        """Generate a new address."""
        return self._call('getnewaddress', [account])
    
    def getaccountaddress(self, account: str) -> str:
        """Get address for an account."""
        return self._call('getaccountaddress', [account])
    
    def sendtoaddress(self, address: str, amount: float, comment: str = '', comment_to: str = '') -> str:
        """
        Send amount to an address.
        
        Returns:
            Transaction ID
        """
        params = [address, amount]
        if comment:
            params.append(comment)
            if comment_to:
                params.append(comment_to)
        return self._call('sendtoaddress', params)
    
    def listtransactions(self, account: str = '*', count: int = 10, skip: int = 0) -> list:
        """List transactions."""
        return self._call('listtransactions', [account, count, skip])
    
    def listunspent(self, minconf: int = 1, maxconf: int = 9999999) -> list:
        """List unspent transaction outputs."""
        return self._call('listunspent', [minconf, maxconf])
    
    def validateaddress(self, address: str) -> Dict:
        """Validate an address."""
        return self._call('validateaddress', [address])
    
    def getblock(self, block_hash: str) -> Dict:
        """Get block information."""
        return self._call('getblock', [block_hash])
    
    def getblockcount(self) -> int:
        """Get the number of blocks in the blockchain."""
        return self._call('getblockcount')
    
    def gettransaction(self, txid: str) -> Dict:
        """Get transaction details."""
        return self._call('gettransaction', [txid])
    
    def encryptwallet(self, passphrase: str) -> str:
        """Encrypt the wallet with a passphrase."""
        return self._call('encryptwallet', [passphrase])
    
    def walletpassphrase(self, passphrase: str, timeout: int) -> None:
        """Unlock the wallet."""
        self._call('walletpassphrase', [passphrase, timeout])
    
    def walletlock(self) -> None:
        """Lock the wallet."""
        self._call('walletlock')
    
    def dumpprivkey(self, address: str) -> str:
        """Dump private key for an address."""
        return self._call('dumpprivkey', [address])
    
    def importprivkey(self, privkey: str, label: str = '', rescan: bool = True) -> None:
        """Import a private key."""
        self._call('importprivkey', [privkey, label, rescan])
    
    def getpeerinfo(self) -> list:
        """Get information about connected peers."""
        return self._call('getpeerinfo')
    
    def getmininginfo(self) -> Dict:
        """Get mining information."""
        return self._call('getmininginfo')
    
    def getwork(self, data: str = None) -> Dict:
        """
        Get work for mining or submit a solution.
        
        Args:
            data: Hex-encoded block data to submit (optional)
            
        Returns:
            Work data if no data provided, or submission result
        """
        if data is None:
            return self._call('getwork')
        else:
            return self._call('getwork', [data])
    
    def getblocktemplate(self, params: Dict = None) -> Dict:
        """
        Get block template for mining.
        
        Args:
            params: Template request parameters
            
        Returns:
            Block template data
        """
        if params is None:
            params = {}
        return self._call('getblocktemplate', [params])
    
    def setgenerate(self, generate: bool, genproclimit: int = -1) -> None:
        """
        Enable/disable mining.
        
        Args:
            generate: True to enable mining, False to disable
            genproclimit: Number of processors to use (-1 for all)
        """
        self._call('setgenerate', [generate, genproclimit])
