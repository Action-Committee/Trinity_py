"""
Solo Miner for Trinity Wallet.

Adapted from contrib/pyminer/pyminer.py for Python 3 and GUI integration.
Provides simple local solo mining functionality.
"""

import hashlib
import struct
import time
import threading
from typing import Optional, Callable, Dict, Any
from .rpc_client import TrinityRPCClient


def uint32(x: int) -> int:
    """Convert to 32-bit unsigned integer."""
    return x & 0xffffffff


def bytereverse(x: int) -> int:
    """Reverse bytes in a 32-bit integer."""
    return uint32(
        ((x << 24) | ((x << 8) & 0x00ff0000) |
         ((x >> 8) & 0x0000ff00) | (x >> 24))
    )


def bufreverse(in_buf: bytes) -> bytes:
    """Reverse bytes in buffer (4-byte chunks)."""
    out_words = []
    for i in range(0, len(in_buf), 4):
        word = struct.unpack('@I', in_buf[i:i+4])[0]
        out_words.append(struct.pack('@I', bytereverse(word)))
    return b''.join(out_words)


def wordreverse(in_buf: bytes) -> bytes:
    """Reverse word order in buffer."""
    out_words = []
    for i in range(0, len(in_buf), 4):
        out_words.append(in_buf[i:i+4])
    out_words.reverse()
    return b''.join(out_words)


class SoloMiner:
    """
    Simple solo miner for Trinity cryptocurrency.
    
    Supports SHA256d algorithm (Trinity's default).
    """
    
    def __init__(self, rpc_client: TrinityRPCClient, 
                 num_threads: int = 1,
                 callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        """
        Initialize solo miner.
        
        Args:
            rpc_client: Connected RPC client
            num_threads: Number of mining threads (default: 1)
            callback: Optional callback for status updates
        """
        self.rpc = rpc_client
        self.num_threads = num_threads
        self.callback = callback
        
        self.mining = False
        self.threads = []
        self.max_nonce = 1000000
        self.scan_time = 30
        
        # Statistics
        self.hashes_done = 0
        self.blocks_found = 0
        self.start_time = 0
        self.shares_submitted = 0
        self.shares_accepted = 0
    
    def _notify(self, message: str, data: Optional[Dict[str, Any]] = None):
        """Send notification to callback if provided."""
        if self.callback:
            notification = {'message': message, 'timestamp': time.time()}
            if data:
                notification.update(data)
            self.callback(notification)
    
    def start(self):
        """Start mining."""
        if self.mining:
            self._notify("Mining is already running")
            return
        
        self.mining = True
        self.start_time = time.time()
        self.hashes_done = 0
        self.blocks_found = 0
        
        # Start mining threads
        for i in range(self.num_threads):
            thread = threading.Thread(target=self._mine_thread, args=(i,), daemon=True)
            thread.start()
            self.threads.append(thread)
        
        self._notify(f"Mining started with {self.num_threads} thread(s)", 
                    {'threads': self.num_threads})
    
    def stop(self):
        """Stop mining."""
        if not self.mining:
            return
        
        self.mining = False
        self._notify("Mining stopped", {
            'total_hashes': self.hashes_done,
            'blocks_found': self.blocks_found,
            'runtime': time.time() - self.start_time
        })
        
        # Wait for threads to finish with reasonable timeout
        for thread in self.threads:
            thread.join(timeout=5.0)
            if thread.is_alive():
                self._notify(f"Warning: Thread {thread.name} did not stop cleanly")
        self.threads.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get mining statistics."""
        runtime = time.time() - self.start_time if self.mining else 0
        hashrate = (self.hashes_done / runtime) if runtime > 0 else 0
        
        return {
            'mining': self.mining,
            'threads': self.num_threads,
            'hashes_done': self.hashes_done,
            'hashrate': hashrate,
            'blocks_found': self.blocks_found,
            'shares_submitted': self.shares_submitted,
            'shares_accepted': self.shares_accepted,
            'runtime': runtime
        }
    
    def _mine_thread(self, thread_id: int):
        """Mining thread worker."""
        self._notify(f"Mining thread {thread_id} started")
        
        while self.mining:
            try:
                self._iterate(thread_id)
            except Exception as e:
                self._notify(f"Mining error in thread {thread_id}: {str(e)}")
                time.sleep(15)  # Error sleep
        
        self._notify(f"Mining thread {thread_id} stopped")
    
    def _iterate(self, thread_id: int):
        """Single mining iteration."""
        # Get work from node
        try:
            work = self.rpc.getwork()
        except Exception as e:
            self._notify(f"Failed to get work: {str(e)}")
            time.sleep(15)
            return
        
        if not work or 'data' not in work or 'target' not in work:
            self._notify("Invalid work data received")
            time.sleep(15)
            return
        
        time_start = time.time()
        
        # Perform proof of work
        hashes_done, nonce_bin = self._do_work(work['data'], work['target'])
        
        time_end = time.time()
        time_diff = time_end - time_start
        
        # Update max_nonce for next iteration
        if time_diff > 0:
            self.max_nonce = int((hashes_done * self.scan_time) / time_diff)
            if self.max_nonce > 0xfffffffa:
                self.max_nonce = 0xfffffffa
        
        # Update total hashes
        self.hashes_done += hashes_done
        
        # Calculate and report hashrate
        if time_diff > 0:
            hashrate = hashes_done / time_diff
            self._notify(f"Thread {thread_id}: {hashes_done} hashes, {hashrate/1000:.2f} KH/s",
                        {'thread_id': thread_id, 'hashrate': hashrate})
        
        # Submit solution if found
        if nonce_bin is not None:
            self._submit_work(work['data'], nonce_bin)
    
    def _do_work(self, datastr: str, targetstr: str) -> tuple:
        """
        Perform proof of work.
        
        Args:
            datastr: Hex-encoded work data
            targetstr: Hex-encoded target
            
        Returns:
            Tuple of (hashes_done, nonce_bin or None)
        """
        # Decode work data hex string to binary
        static_data = bytes.fromhex(datastr)
        static_data = bufreverse(static_data)
        
        # The first 76 bytes of 80 bytes do not change
        blk_hdr = static_data[:76]
        
        # Decode 256-bit target value
        targetbin = bytes.fromhex(targetstr)
        targetbin = targetbin[::-1]  # Byte-swap and dword-swap
        target = int(targetbin.hex(), 16)
        
        # Pre-hash first 76 bytes of block header
        static_hash = hashlib.sha256()
        static_hash.update(blk_hdr)
        
        # Try different nonces
        for nonce in range(self.max_nonce):
            # Check mining flag periodically for better performance
            if nonce % 1000 == 0 and not self.mining:
                return (nonce, None)
            
            # Encode 32-bit nonce value
            nonce_bin = struct.pack("<I", nonce)
            
            # Hash final 4 bytes, the nonce value
            hash1_o = static_hash.copy()
            hash1_o.update(nonce_bin)
            hash1 = hash1_o.digest()
            
            # SHA256 hash of SHA256 hash
            hash_o = hashlib.sha256()
            hash_o.update(hash1)
            hash_result = hash_o.digest()
            
            # Quick test for winning solution: high 32 bits zero?
            if hash_result[-4:] != b'\x00\x00\x00\x00':
                continue
            
            # Convert binary hash to 256-bit integer
            hash_reversed = bufreverse(hash_result)
            hash_reversed = wordreverse(hash_reversed)
            hash_int = int(hash_reversed.hex(), 16)
            
            # Proof-of-work test: hash < target
            if hash_int < target:
                self._notify(f"PROOF-OF-WORK FOUND: {hash_int:064x}",
                           {'hash': hash_int, 'nonce': nonce})
                return (nonce + 1, nonce_bin)
        
        return (self.max_nonce, None)
    
    def _submit_work(self, original_data: str, nonce_bin: bytes):
        """
        Submit found work to node.
        
        Args:
            original_data: Original work data
            nonce_bin: Binary nonce value
        """
        try:
            # Reverse nonce and encode
            nonce_bin = bufreverse(nonce_bin)
            nonce = nonce_bin.hex()
            
            # Build solution
            solution = original_data[:152] + nonce + original_data[160:256]
            
            # Submit to node
            result = self.rpc.getwork(solution)
            
            self.shares_submitted += 1
            
            if result:
                self.shares_accepted += 1
                self.blocks_found += 1
                self._notify(f"BLOCK FOUND! Result: {result}",
                           {'result': result, 'blocks_found': self.blocks_found})
            else:
                self._notify(f"Work submitted but not accepted: {result}")
                
        except Exception as e:
            self._notify(f"Error submitting work: {str(e)}")
