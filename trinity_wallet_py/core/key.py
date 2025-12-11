"""
Key management for Trinity wallet.
Handles private/public key generation and address creation.
"""

import hashlib
import secrets
from typing import Tuple
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_der, sigdecode_der
from ..utils.base58 import b58encode_check, b58decode_check

# Trinity address version (30 = 'D' prefix)
PUBKEY_ADDRESS_VERSION = 30
SCRIPT_ADDRESS_VERSION = 5
SECRET_KEY_VERSION = 177


class Key:
    """Represents a private key."""
    
    def __init__(self, private_key_bytes=None):
        """
        Initialize a key.
        If private_key_bytes is None, generate a new random key.
        """
        if private_key_bytes is None:
            # Generate new random private key
            self.private_key = SigningKey.generate(curve=SECP256k1)
        else:
            # Load from bytes
            self.private_key = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    
    def get_private_key_bytes(self) -> bytes:
        """Get private key as bytes."""
        return self.private_key.to_string()
    
    def get_public_key_bytes(self, compressed=True) -> bytes:
        """Get public key as bytes."""
        vk = self.private_key.get_verifying_key()
        if compressed:
            # Compressed public key format
            x = vk.pubkey.point.x()
            y = vk.pubkey.point.y()
            prefix = b'\x02' if y % 2 == 0 else b'\x03'
            return prefix + x.to_bytes(32, 'big')
        else:
            # Uncompressed format
            return b'\x04' + vk.to_string()
    
    def get_address(self) -> str:
        """Get Trinity address (starts with 'D')."""
        # Use uncompressed public key for compatibility
        pubkey = self.get_public_key_bytes(compressed=False)
        
        # Hash public key
        sha256_hash = hashlib.sha256(pubkey).digest()
        ripemd160 = hashlib.new('ripemd160', sha256_hash).digest()
        
        # Encode with version and checksum
        return b58encode_check(PUBKEY_ADDRESS_VERSION, ripemd160)
    
    def get_wif(self) -> str:
        """Get private key in WIF format."""
        return b58encode_check(SECRET_KEY_VERSION, self.get_private_key_bytes())
    
    @staticmethod
    def from_wif(wif: str) -> 'Key':
        """Create key from WIF format."""
        version, payload = b58decode_check(wif)
        if version != SECRET_KEY_VERSION:
            raise ValueError(f"Invalid WIF version: {version}")
        return Key(payload)
    
    def sign(self, data: bytes) -> bytes:
        """Sign data with this private key."""
        return self.private_key.sign_digest(data, sigencode=sigencode_der)


def validate_address(address: str) -> bool:
    """Validate a Trinity address."""
    try:
        version, payload = b58decode_check(address)
        return version == PUBKEY_ADDRESS_VERSION and len(payload) == 20
    except:
        return False


def generate_new_key() -> Key:
    """Generate a new random key."""
    return Key()
