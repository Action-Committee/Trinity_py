#!/usr/bin/env python3
"""
Test script for Trinity Wallet functionality.
Tests key generation, address creation, and base58 encoding.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trinity_wallet_py.core.key import Key, generate_new_key, validate_address
from trinity_wallet_py.utils.base58 import b58encode, b58decode, b58encode_check, b58decode_check


def test_base58():
    """Test base58 encoding/decoding."""
    print("Testing Base58 encoding/decoding...")
    
    # Test encoding
    data = b"Hello World"
    encoded = b58encode(data)
    print(f"  Encoded '{data.decode()}' to: {encoded}")
    
    # Test decoding
    decoded = b58decode(encoded)
    assert decoded == data, "Base58 decode failed"
    print(f"  Decoded back to: {decoded.decode()}")
    
    # Test with checksum
    version = 30  # Trinity address version
    payload = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a" * 2
    encoded_check = b58encode_check(version, payload)
    print(f"  Encoded with checksum: {encoded_check}")
    
    decoded_version, decoded_payload = b58decode_check(encoded_check)
    assert decoded_version == version, "Version mismatch"
    assert decoded_payload == payload, "Payload mismatch"
    print(f"  Decoded successfully: version={decoded_version}")
    
    print("✓ Base58 tests passed\n")


def test_key_generation():
    """Test key generation and address creation."""
    print("Testing Key generation...")
    
    # Generate new key
    key = generate_new_key()
    print(f"  Generated new private key")
    
    # Get public key
    pubkey = key.get_public_key_bytes(compressed=False)
    print(f"  Public key length: {len(pubkey)} bytes")
    
    # Get address
    address = key.get_address()
    print(f"  Generated address: {address}")
    
    # Verify address starts with 'D'
    assert address.startswith('D'), f"Address should start with 'D', got: {address[0]}"
    print(f"  ✓ Address starts with 'D' (Trinity format)")
    
    # Validate address
    assert validate_address(address), "Address validation failed"
    print(f"  ✓ Address validation passed")
    
    # Get WIF
    wif = key.get_wif()
    print(f"  WIF format: {wif[:10]}...{wif[-10:]}")
    
    # Test WIF import/export
    key2 = Key.from_wif(wif)
    address2 = key2.get_address()
    assert address == address2, "WIF import/export failed"
    print(f"  ✓ WIF import/export works correctly")
    
    print("✓ Key generation tests passed\n")


def test_multiple_addresses():
    """Test generating multiple addresses."""
    print("Testing multiple address generation...")
    
    addresses = []
    for i in range(5):
        key = generate_new_key()
        address = key.get_address()
        addresses.append(address)
        print(f"  Address {i+1}: {address}")
    
    # Verify all addresses are unique
    assert len(addresses) == len(set(addresses)), "Duplicate addresses found"
    print(f"  ✓ All {len(addresses)} addresses are unique")
    
    # Verify all start with 'D'
    assert all(addr.startswith('D') for addr in addresses), "Not all addresses start with 'D'"
    print(f"  ✓ All addresses start with 'D'")
    
    print("✓ Multiple address tests passed\n")


def test_invalid_addresses():
    """Test address validation with invalid addresses."""
    print("Testing invalid address detection...")
    
    invalid_addresses = [
        "invalid",
        "1234567890",
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "",
        "D" * 100,
        "DInvalidAddressChecksum",
    ]
    
    for addr in invalid_addresses:
        result = validate_address(addr)
        print(f"  '{addr[:30]}...' is valid: {result}")
        assert not result, f"Invalid address {addr} was marked as valid"
    
    print("✓ Invalid address detection tests passed\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Trinity Wallet - Component Tests")
    print("=" * 60)
    print()
    
    try:
        test_base58()
        test_key_generation()
        test_multiple_addresses()
        test_invalid_addresses()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print()
        print("The Trinity Python wallet components are working correctly!")
        print("You can now run the wallet with: python3 wallet.py")
        return 0
    
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ TEST FAILED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
