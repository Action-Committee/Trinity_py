// Copyright (c) 2024 The Trinity developers
// Distributed under the MIT/X11 software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include "compressedstorage.h"
#include "hash.h"
#include "util.h"
#include <algorithm>
#include <cstring>

// We'll use a simple but effective compression scheme
// For production, this could use zlib, LZ4, or custom blockchain-specific compression

// Magic bytes to identify compressed data
static const unsigned char COMPRESSION_MAGIC[4] = { 'T', 'C', 'M', 'P' }; // Trinity CoMPressed
static const unsigned char COMPRESSION_VERSION = 0x01;

// Compression format flags
static const unsigned char FLAG_COMPRESSED = 0x01;
static const unsigned char FLAG_DEDUPLICATED = 0x02;
static const unsigned char FLAG_DELTA_ENCODED = 0x04;

CCompressedStorage compressedStorage;

CCompressedStorage::CCompressedStorage() 
    : fCompressionEnabled(false), nCompressionLevel(6)
{
}

CCompressedStorage::~CCompressedStorage()
{
    ClearCache();
}

void CCompressedStorage::SetCompressionEnabled(bool fEnabled)
{
    fCompressionEnabled = fEnabled;
}

void CCompressedStorage::SetCompressionLevel(int level)
{
    if (level < 1) level = 1;
    if (level > 9) level = 9;
    nCompressionLevel = level;
}

uint256 CCompressedStorage::ComputePatternHash(const std::vector<unsigned char>& data)
{
    return Hash(data.begin(), data.end());
}

bool CCompressedStorage::FindDuplicatePattern(const std::vector<unsigned char>& data, uint256& hashOut)
{
    hashOut = ComputePatternHash(data);
    return mapTxPatterns.count(hashOut) > 0;
}

void CCompressedStorage::StorePattern(const uint256& hash, const std::vector<unsigned char>& data)
{
    if (mapTxPatterns.count(hash) > 0) {
        mapTxPatterns[hash].refCount++;
    } else {
        TxPattern pattern;
        pattern.patternHash = hash;
        pattern.data = data;
        pattern.refCount = 1;
        mapTxPatterns[hash] = pattern;
    }
}

// Simple RLE (Run-Length Encoding) compression for demonstration
// In production, this would use zlib or LZ4
bool CCompressedStorage::CompressData(const std::vector<unsigned char>& input,
                                     std::vector<unsigned char>& output, int level)
{
    if (input.empty()) {
        output.clear();
        return true;
    }
    
    // Reserve space for output
    output.clear();
    output.reserve(input.size());
    
    // Simple RLE compression with escape sequences
    size_t i = 0;
    while (i < input.size()) {
        unsigned char current = input[i];
        size_t runLength = 1;
        
        // Count consecutive identical bytes
        while (i + runLength < input.size() && 
               input[i + runLength] == current && 
               runLength < 255) {
            runLength++;
        }
        
        // If run is long enough, encode it
        if (runLength >= 4) {
            output.push_back(0xFF); // Escape byte
            output.push_back((unsigned char)runLength);
            output.push_back(current);
            i += runLength;
        } else {
            // For short runs, just copy the bytes
            for (size_t j = 0; j < runLength; j++) {
                output.push_back(current);
            }
            i += runLength;
        }
    }
    
    // Update statistics
    stats.nTotalBytesOriginal += input.size();
    stats.nTotalBytesCompressed += output.size();
    
    return true;
}

bool CCompressedStorage::DecompressData(const std::vector<unsigned char>& input,
                                       std::vector<unsigned char>& output)
{
    if (input.empty()) {
        output.clear();
        return true;
    }
    
    output.clear();
    output.reserve(input.size() * 2); // Estimate decompressed size
    
    size_t i = 0;
    while (i < input.size()) {
        if (input[i] == 0xFF && i + 2 < input.size() && i + 3 <= input.size()) {
            // Decompress RLE sequence
            unsigned char runLength = input[i + 1];
            unsigned char value = input[i + 2];
            for (unsigned char j = 0; j < runLength; j++) {
                output.push_back(value);
            }
            i += 3;
        } else {
            // Regular byte
            output.push_back(input[i]);
            i++;
        }
    }
    
    return true;
}

bool CCompressedStorage::DeltaEncode(const std::vector<unsigned char>& base,
                                    const std::vector<unsigned char>& target,
                                    std::vector<unsigned char>& delta)
{
    // Simple delta encoding - store differences from base
    delta.clear();
    
    size_t minSize = std::min(base.size(), target.size());
    size_t maxSize = std::max(base.size(), target.size());
    
    // Store size difference
    int64_t sizeDiff = (int64_t)target.size() - (int64_t)base.size();
    delta.push_back((sizeDiff >> 24) & 0xFF);
    delta.push_back((sizeDiff >> 16) & 0xFF);
    delta.push_back((sizeDiff >> 8) & 0xFF);
    delta.push_back(sizeDiff & 0xFF);
    
    // Store differences for common part
    for (size_t i = 0; i < minSize; i++) {
        delta.push_back(target[i] ^ base[i]);
    }
    
    // Store remaining bytes if target is larger
    if (target.size() > base.size()) {
        for (size_t i = minSize; i < target.size(); i++) {
            delta.push_back(target[i]);
        }
    }
    
    return true;
}

bool CCompressedStorage::DeltaDecode(const std::vector<unsigned char>& base,
                                    const std::vector<unsigned char>& delta,
                                    std::vector<unsigned char>& target)
{
    if (delta.size() < 4) return false;
    
    // Read size difference
    int64_t sizeDiff = ((int64_t)delta[0] << 24) | 
                       ((int64_t)delta[1] << 16) |
                       ((int64_t)delta[2] << 8) | 
                       (int64_t)delta[3];
    
    size_t targetSize = base.size() + sizeDiff;
    target.clear();
    target.reserve(targetSize);
    
    size_t minSize = std::min(base.size(), targetSize);
    
    // Decode common part
    for (size_t i = 0; i < minSize && (i + 4) < delta.size() && (i + 5) <= delta.size(); i++) {
        target.push_back(base[i] ^ delta[i + 4]);
    }
    
    // Add remaining bytes if target is larger
    if (targetSize > base.size()) {
        for (size_t i = minSize; (i + 4) < delta.size() && (i + 5) <= delta.size(); i++) {
            target.push_back(delta[i + 4]);
        }
    }
    
    return target.size() == targetSize;
}

bool CCompressedStorage::CompressBlock(const std::vector<unsigned char>& input,
                                      std::vector<unsigned char>& output)
{
    if (!fCompressionEnabled) {
        output = input;
        return true;
    }
    
    // Build header
    output.clear();
    output.reserve(input.size() + 16); // Reserve space for header + data
    
    // Write magic bytes
    output.insert(output.end(), COMPRESSION_MAGIC, COMPRESSION_MAGIC + 4);
    
    // Write version
    output.push_back(COMPRESSION_VERSION);
    
    // Write flags
    unsigned char flags = FLAG_COMPRESSED;
    output.push_back(flags);
    
    // Write original size (4 bytes)
    uint32_t originalSize = input.size();
    output.push_back((originalSize >> 24) & 0xFF);
    output.push_back((originalSize >> 16) & 0xFF);
    output.push_back((originalSize >> 8) & 0xFF);
    output.push_back(originalSize & 0xFF);
    
    // Compress the data
    std::vector<unsigned char> compressed;
    if (!CompressData(input, compressed, nCompressionLevel)) {
        return false;
    }
    
    // Write compressed size (4 bytes)
    uint32_t compressedSize = compressed.size();
    output.push_back((compressedSize >> 24) & 0xFF);
    output.push_back((compressedSize >> 16) & 0xFF);
    output.push_back((compressedSize >> 8) & 0xFF);
    output.push_back(compressedSize & 0xFF);
    
    // Append compressed data
    output.insert(output.end(), compressed.begin(), compressed.end());
    
    stats.nBlocksCompressed++;
    
    return true;
}

bool CCompressedStorage::DecompressBlock(const std::vector<unsigned char>& input,
                                        std::vector<unsigned char>& output)
{
    if (!fCompressionEnabled || input.size() < 14) {
        output = input;
        return true;
    }
    
    // Check magic bytes
    if (memcmp(&input[0], COMPRESSION_MAGIC, 4) != 0) {
        // Not compressed, return as-is
        output = input;
        return true;
    }
    
    // Check version
    if (input[4] != COMPRESSION_VERSION) {
        return error("DecompressBlock() : unsupported compression version");
    }
    
    // Read flags
    unsigned char flags = input[5];
    
    // Read original size
    uint32_t originalSize = ((uint32_t)input[6] << 24) |
                           ((uint32_t)input[7] << 16) |
                           ((uint32_t)input[8] << 8) |
                           (uint32_t)input[9];
    
    // Read compressed size
    uint32_t compressedSize = ((uint32_t)input[10] << 24) |
                             ((uint32_t)input[11] << 16) |
                             ((uint32_t)input[12] << 8) |
                             (uint32_t)input[13];
    
    if (14 + compressedSize > input.size()) {
        return error("DecompressBlock() : invalid compressed size");
    }
    
    // Extract compressed data
    std::vector<unsigned char> compressed(input.begin() + 14, 
                                         input.begin() + 14 + compressedSize);
    
    // Decompress
    if (!DecompressData(compressed, output)) {
        return error("DecompressBlock() : decompression failed");
    }
    
    if (output.size() != originalSize) {
        return error("DecompressBlock() : size mismatch after decompression");
    }
    
    return true;
}

bool CCompressedStorage::CompressTransaction(const std::vector<unsigned char>& input,
                                           std::vector<unsigned char>& output)
{
    if (!fCompressionEnabled) {
        output = input;
        return true;
    }
    
    // Check if this transaction pattern has been seen before
    uint256 patternHash;
    if (FindDuplicatePattern(input, patternHash)) {
        // Reference existing pattern
        output.clear();
        output.push_back(0xFE); // Deduplication marker
        output.insert(output.end(), patternHash.begin(), patternHash.end());
        stats.nDedupedTransactions++;
        return true;
    }
    
    // Store new pattern
    StorePattern(patternHash, input);
    
    // Compress normally
    return CompressData(input, output, nCompressionLevel);
}

bool CCompressedStorage::DecompressTransaction(const std::vector<unsigned char>& input,
                                              std::vector<unsigned char>& output)
{
    if (!fCompressionEnabled || input.empty()) {
        output = input;
        return true;
    }
    
    // Check for deduplication marker
    if (input[0] == 0xFE && input.size() >= 33 && input.size() == 33) {
        uint256 patternHash;
        memcpy(patternHash.begin(), &input[1], 32);
        
        if (mapTxPatterns.count(patternHash) > 0) {
            output = mapTxPatterns[patternHash].data;
            return true;
        } else {
            return error("DecompressTransaction() : pattern not found");
        }
    }
    
    // Decompress normally
    return DecompressData(input, output);
}

void CCompressedStorage::ResetStats()
{
    stats = CompressionStats();
}

void CCompressedStorage::ClearCache()
{
    mapTxPatterns.clear();
}

size_t CCompressedStorage::GetCacheSize() const
{
    size_t total = 0;
    for (const auto& pair : mapTxPatterns) {
        total += pair.second.data.size() + sizeof(TxPattern);
    }
    return total;
}
