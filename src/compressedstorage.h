// Copyright (c) 2024 The Trinity developers
// Distributed under the MIT/X11 software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef BITCOIN_COMPRESSED_STORAGE_H
#define BITCOIN_COMPRESSED_STORAGE_H

#include "serialize.h"
#include "uint256.h"
#include <vector>
#include <map>
#include <string>

/**
 * Compressed Block Storage Engine
 * 
 * This class implements advanced compression techniques for blockchain data:
 * 1. Redundancy reduction - Error-correcting codes and delta encoding
 * 2. Context-based compression - Pattern recognition in block structures
 * 3. Repetition elimination - Deduplication of common transaction patterns
 * 4. Mathematical optimization - Advanced entropy coding (arithmetic/range)
 * 
 * The engine provides transparent compression/decompression while maintaining
 * full backward compatibility with the network protocol.
 */

// Compression statistics for monitoring
struct CompressionStats {
    uint64_t nTotalBytesOriginal;
    uint64_t nTotalBytesCompressed;
    uint64_t nBlocksCompressed;
    uint64_t nDedupedTransactions;
    
    CompressionStats() : nTotalBytesOriginal(0), nTotalBytesCompressed(0), 
                         nBlocksCompressed(0), nDedupedTransactions(0) {}
    
    double GetCompressionRatio() const {
        return nTotalBytesOriginal > 0 ? 
            (double)nTotalBytesCompressed / nTotalBytesOriginal : 1.0;
    }
};

// Transaction pattern for deduplication
struct TxPattern {
    uint256 patternHash;
    std::vector<unsigned char> data;
    unsigned int refCount;
    
    TxPattern() : patternHash(0), refCount(0) {}
};

class CCompressedStorage
{
private:
    // Deduplication cache - stores common transaction patterns
    std::map<uint256, TxPattern> mapTxPatterns;
    
    // Compression statistics
    CompressionStats stats;
    
    // Configuration
    bool fCompressionEnabled;
    int nCompressionLevel;  // 1-9, higher = more compression but slower
    
    // Helper functions for compression
    bool CompressData(const std::vector<unsigned char>& input, 
                     std::vector<unsigned char>& output, int level);
    bool DecompressData(const std::vector<unsigned char>& input, 
                       std::vector<unsigned char>& output);
    
    // Deduplication helpers
    uint256 ComputePatternHash(const std::vector<unsigned char>& data);
    bool FindDuplicatePattern(const std::vector<unsigned char>& data, uint256& hashOut);
    void StorePattern(const uint256& hash, const std::vector<unsigned char>& data);
    
    // Delta encoding for similar blocks
    bool DeltaEncode(const std::vector<unsigned char>& base,
                    const std::vector<unsigned char>& target,
                    std::vector<unsigned char>& delta);
    bool DeltaDecode(const std::vector<unsigned char>& base,
                    const std::vector<unsigned char>& delta,
                    std::vector<unsigned char>& target);

public:
    CCompressedStorage();
    ~CCompressedStorage();
    
    // Enable/disable compression
    void SetCompressionEnabled(bool fEnabled);
    bool IsCompressionEnabled() const { return fCompressionEnabled; }
    
    // Set compression level (1-9)
    void SetCompressionLevel(int level);
    int GetCompressionLevel() const { return nCompressionLevel; }
    
    /**
     * Compress a block's serialized data
     * @param input  Original block data
     * @param output Compressed block data
     * @return true if compression succeeded
     */
    bool CompressBlock(const std::vector<unsigned char>& input,
                      std::vector<unsigned char>& output);
    
    /**
     * Decompress a block's serialized data
     * @param input  Compressed block data
     * @param output Original block data
     * @return true if decompression succeeded
     */
    bool DecompressBlock(const std::vector<unsigned char>& input,
                        std::vector<unsigned char>& output);
    
    /**
     * Compress transaction data with deduplication
     * @param input  Transaction data
     * @param output Compressed/deduplicated data
     * @return true if successful
     */
    bool CompressTransaction(const std::vector<unsigned char>& input,
                           std::vector<unsigned char>& output);
    
    /**
     * Decompress transaction data
     * @param input  Compressed/deduplicated data
     * @param output Original transaction data
     * @return true if successful
     */
    bool DecompressTransaction(const std::vector<unsigned char>& input,
                              std::vector<unsigned char>& output);
    
    // Get compression statistics
    const CompressionStats& GetStats() const { return stats; }
    void ResetStats();
    
    // Clear deduplication cache
    void ClearCache();
    
    // Get cache size in bytes
    size_t GetCacheSize() const;
};

// Global compressed storage instance
extern CCompressedStorage compressedStorage;

#endif // BITCOIN_COMPRESSED_STORAGE_H
