#!/usr/bin/env python3
"""
Test script for solo mining functionality.
Tests the miner module without requiring a running node.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trinity_wallet_py.core.miner import (
    uint32, bytereverse, bufreverse, wordreverse, SoloMiner
)


def test_byte_operations():
    """Test byte manipulation functions."""
    print("Testing byte operations...")
    
    # Test uint32
    assert uint32(0x100000000) == 0, "uint32 overflow test failed"
    assert uint32(0x12345678) == 0x12345678, "uint32 normal value test failed"
    print("  ✓ uint32 works correctly")
    
    # Test bytereverse
    result = bytereverse(0x12345678)
    expected = 0x78563412
    assert result == expected, f"bytereverse failed: got {result:08x}, expected {expected:08x}"
    print(f"  ✓ bytereverse(0x12345678) = 0x{result:08x}")
    
    # Test bufreverse
    test_buf = b'\x01\x02\x03\x04\x05\x06\x07\x08'
    result = bufreverse(test_buf)
    print(f"  ✓ bufreverse works: {test_buf.hex()} -> {result.hex()}")
    
    # Test wordreverse
    test_buf = b'\x01\x02\x03\x04\x05\x06\x07\x08'
    result = wordreverse(test_buf)
    expected = b'\x05\x06\x07\x08\x01\x02\x03\x04'
    assert result == expected, f"wordreverse failed: got {result.hex()}, expected {expected.hex()}"
    print(f"  ✓ wordreverse works: {test_buf.hex()} -> {result.hex()}")
    
    print("✓ Byte operations tests passed\n")


def test_miner_initialization():
    """Test miner initialization without RPC."""
    print("Testing miner initialization...")
    
    # Create a mock RPC client
    class MockRPC:
        def getwork(self, data=None):
            return None
    
    mock_rpc = MockRPC()
    
    # Test miner creation
    miner = SoloMiner(mock_rpc, num_threads=2)
    assert miner.num_threads == 2, "Thread count mismatch"
    assert not miner.mining, "Miner should not be mining initially"
    assert miner.hashes_done == 0, "Initial hash count should be 0"
    assert miner.blocks_found == 0, "Initial blocks found should be 0"
    print("  ✓ Miner initialized correctly")
    
    # Test get_stats
    stats = miner.get_stats()
    assert stats['mining'] == False, "Mining status should be False"
    assert stats['threads'] == 2, "Thread count mismatch in stats"
    assert stats['hashes_done'] == 0, "Hashes done should be 0"
    assert stats['hashrate'] == 0, "Initial hashrate should be 0"
    print("  ✓ Stats retrieval works")
    
    print("✓ Miner initialization tests passed\n")


def test_callback_mechanism():
    """Test miner callback mechanism."""
    print("Testing callback mechanism...")
    
    received_notifications = []
    
    def test_callback(notification):
        received_notifications.append(notification)
    
    class MockRPC:
        def getwork(self, data=None):
            return None
    
    miner = SoloMiner(MockRPC(), num_threads=1, callback=test_callback)
    
    # Test notification
    miner._notify("Test message", {'test_data': 123})
    
    assert len(received_notifications) == 1, "Callback not invoked"
    assert received_notifications[0]['message'] == "Test message", "Message mismatch"
    assert received_notifications[0]['test_data'] == 123, "Data mismatch"
    print("  ✓ Callback mechanism works correctly")
    
    print("✓ Callback tests passed\n")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Trinity Solo Miner Tests")
    print("=" * 60)
    print()
    
    try:
        test_byte_operations()
        test_miner_initialization()
        test_callback_mechanism()
        
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
