"""
Base58 encoding/decoding for Trinity addresses.
Trinity addresses start with 'D' (base58 prefix 30).
"""

import hashlib

# Base58 alphabet (Bitcoin-style)
B58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def b58encode(data):
    """Encode bytes to base58 string."""
    if not data:
        return ''
    
    # Convert bytes to integer
    num = int.from_bytes(data, 'big')
    
    # Convert to base58
    encoded = ''
    while num > 0:
        num, remainder = divmod(num, 58)
        encoded = B58_ALPHABET[remainder] + encoded
    
    # Add leading '1's for leading zero bytes
    for byte in data:
        if byte == 0:
            encoded = '1' + encoded
        else:
            break
    
    return encoded


def b58decode(s):
    """Decode base58 string to bytes."""
    if not s:
        return b''
    
    # Convert base58 to integer
    num = 0
    for char in s:
        num = num * 58 + B58_ALPHABET.index(char)
    
    # Convert integer to bytes
    combined = num.to_bytes((num.bit_length() + 7) // 8, 'big')
    
    # Add leading zero bytes for leading '1's
    for char in s:
        if char == '1':
            combined = b'\x00' + combined
        else:
            break
    
    return combined


def hash256(data):
    """Double SHA-256 hash."""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def b58encode_check(version, payload):
    """Encode with version byte and checksum."""
    data = bytes([version]) + payload
    checksum = hash256(data)[:4]
    return b58encode(data + checksum)


def b58decode_check(s):
    """Decode and verify checksum, return (version, payload)."""
    data = b58decode(s)
    if len(data) < 5:
        raise ValueError("Invalid address")
    
    version = data[0]
    payload = data[1:-4]
    checksum = data[-4:]
    
    # Verify checksum
    expected_checksum = hash256(data[:-4])[:4]
    if checksum != expected_checksum:
        raise ValueError("Invalid checksum")
    
    return version, payload
