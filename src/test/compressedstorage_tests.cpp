// Copyright (c) 2024 The Trinity developers
// Distributed under the MIT/X11 software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <boost/test/unit_test.hpp>
#include "compressedstorage.h"
#include <vector>

using namespace std;

BOOST_AUTO_TEST_SUITE(compressedstorage_tests)

// Test basic compression and decompression
BOOST_AUTO_TEST_CASE(compress_decompress_roundtrip)
{
    CCompressedStorage storage;
    storage.SetCompressionEnabled(true);
    storage.SetCompressionLevel(6);
    
    // Create test data with repetitive pattern (good for RLE)
    vector<unsigned char> original;
    for (int i = 0; i < 100; i++) {
        original.push_back(0xAA); // Repeated byte
    }
    for (int i = 0; i < 50; i++) {
        original.push_back(i % 256); // Variable bytes
    }
    
    // Compress
    vector<unsigned char> compressed;
    BOOST_CHECK(storage.CompressBlock(original, compressed));
    
    // Decompress
    vector<unsigned char> decompressed;
    BOOST_CHECK(storage.DecompressBlock(compressed, decompressed));
    
    // Verify round-trip
    BOOST_CHECK_EQUAL(original.size(), decompressed.size());
    BOOST_CHECK(original == decompressed);
}

// Test compression actually reduces size for repetitive data
BOOST_AUTO_TEST_CASE(compress_reduces_size)
{
    CCompressedStorage storage;
    storage.SetCompressionEnabled(true);
    storage.SetCompressionLevel(9);
    
    // Create highly repetitive data
    vector<unsigned char> original;
    for (int i = 0; i < 1000; i++) {
        original.push_back(0xFF);
    }
    
    vector<unsigned char> compressed;
    BOOST_CHECK(storage.CompressBlock(original, compressed));
    
    // Compressed should be smaller (with header overhead considered)
    // RLE should compress 1000 identical bytes very efficiently
    BOOST_CHECK(compressed.size() < original.size());
}

// Test decompression of uncompressed data
BOOST_AUTO_TEST_CASE(decompress_uncompressed_data)
{
    CCompressedStorage storage;
    storage.SetCompressionEnabled(true);
    
    // Create data without compression magic bytes
    vector<unsigned char> original;
    for (int i = 0; i < 100; i++) {
        original.push_back(i % 256);
    }
    
    vector<unsigned char> result;
    BOOST_CHECK(storage.DecompressBlock(original, result));
    
    // Should return original data unchanged when magic bytes not found
    BOOST_CHECK(original == result);
}

// Test compression disabled mode
BOOST_AUTO_TEST_CASE(compression_disabled)
{
    CCompressedStorage storage;
    storage.SetCompressionEnabled(false);
    
    vector<unsigned char> original;
    for (int i = 0; i < 100; i++) {
        original.push_back(i % 256);
    }
    
    vector<unsigned char> result;
    BOOST_CHECK(storage.CompressBlock(original, result));
    
    // When disabled, should return original data
    BOOST_CHECK(original == result);
}

// Test transaction deduplication
BOOST_AUTO_TEST_CASE(transaction_deduplication)
{
    CCompressedStorage storage;
    storage.SetCompressionEnabled(true);
    storage.ClearCache();
    
    // Create test transaction data
    vector<unsigned char> tx1;
    for (int i = 0; i < 50; i++) {
        tx1.push_back(0x12);
    }
    
    // First compression should store the pattern
    vector<unsigned char> compressed1;
    BOOST_CHECK(storage.CompressTransaction(tx1, compressed1));
    
    // Second compression of same data should deduplicate
    vector<unsigned char> compressed2;
    BOOST_CHECK(storage.CompressTransaction(tx1, compressed2));
    
    // Second compression should be smaller (deduplicated reference)
    BOOST_CHECK(compressed2.size() < compressed1.size());
    BOOST_CHECK_EQUAL(compressed2.size(), 33); // 1 byte marker + 32 byte hash
    
    // Decompression should restore original
    vector<unsigned char> decompressed;
    BOOST_CHECK(storage.DecompressTransaction(compressed2, decompressed));
    BOOST_CHECK(tx1 == decompressed);
}

// Test compression level setting
BOOST_AUTO_TEST_CASE(compression_level_bounds)
{
    CCompressedStorage storage;
    
    // Test setting various levels
    storage.SetCompressionLevel(1);
    BOOST_CHECK_EQUAL(storage.GetCompressionLevel(), 1);
    
    storage.SetCompressionLevel(9);
    BOOST_CHECK_EQUAL(storage.GetCompressionLevel(), 9);
    
    // Test bounds checking (should clamp)
    storage.SetCompressionLevel(0);
    BOOST_CHECK_EQUAL(storage.GetCompressionLevel(), 1);
    
    storage.SetCompressionLevel(15);
    BOOST_CHECK_EQUAL(storage.GetCompressionLevel(), 9);
}

// Test statistics tracking
BOOST_AUTO_TEST_CASE(compression_statistics)
{
    CCompressedStorage storage;
    storage.SetCompressionEnabled(true);
    storage.ResetStats();
    
    const CompressionStats& stats = storage.GetStats();
    BOOST_CHECK_EQUAL(stats.nBlocksCompressed, 0);
    BOOST_CHECK_EQUAL(stats.nTotalBytesOriginal, 0);
    
    // Compress some data
    vector<unsigned char> data(100, 0xFF);
    vector<unsigned char> compressed;
    storage.CompressBlock(data, compressed);
    
    // Stats should be updated
    const CompressionStats& newStats = storage.GetStats();
    BOOST_CHECK_EQUAL(newStats.nBlocksCompressed, 1);
    BOOST_CHECK(newStats.nTotalBytesOriginal > 0);
}

BOOST_AUTO_TEST_SUITE_END()
