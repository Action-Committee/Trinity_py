# Trinity Wallet - Solo Mining Feature

## Overview

The Trinity Python Wallet now includes integrated solo mining functionality, allowing you to mine Trinity coins directly from the wallet interface without needing external mining software.

## Features

- **Integrated Mining**: Mine directly from the wallet GUI
- **SHA256d Algorithm**: Uses Trinity's default mining algorithm
- **Multi-threaded**: Configure 1-16 mining threads for optimal performance
- **Real-time Statistics**: Monitor hashrate, blocks found, and mining progress
- **Address Selection**: Mine directly to any wallet address
- **Mining Log**: View real-time mining events and status updates

## How It Works

The solo miner is based on the proven pyminer.py implementation, modernized for Python 3 and integrated into the wallet's GUI. It communicates with your local Trinity node via RPC to get work and submit solutions.

### Mining Process

1. The miner requests work from the Trinity node using the `getwork` RPC call
2. Multiple threads perform SHA256d proof-of-work calculations
3. When a valid solution is found, it's automatically submitted to the network
4. Mined coins are sent directly to your selected wallet address

## Usage

### Prerequisites

1. **Trinity Node Running**: You must have a Trinity daemon (trinityd) running with RPC enabled
2. **Node Configuration**: Your trinity.conf should include:
   ```
   server=1
   rpcuser=your_username
   rpcpassword=your_password
   rpcport=6420
   gen=0
   ```
   Note: Set `gen=0` to disable built-in CPU mining if desired, as the wallet miner is more efficient.

3. **Wallet Connected**: Ensure your wallet is connected to the local node (Settings → Connect to Node)

### Starting Mining

1. Open the Trinity Wallet
2. Click on the **"Mining"** tab
3. Select the number of threads (1-16)
   - More threads = higher hashrate but more CPU usage
   - Start with 1-2 threads to test
4. Select or create a mining address
   - This is where your mined coins will be sent
   - You can use any address in your wallet
5. Click **"Start Mining"**
6. Monitor the statistics and log for mining activity

### Statistics Explained

- **Status**: Shows whether mining is active or stopped
- **Hashrate**: Current mining speed (H/s = hashes per second, KH/s = kilohashes, MH/s = megahashes)
- **Hashes Done**: Total number of hashes calculated
- **Blocks Found**: Number of blocks successfully mined
- **Shares Submitted/Accepted**: Solutions submitted to the network
- **Runtime**: How long mining has been active

### Stopping Mining

Click the **"Stop Mining"** button to gracefully stop all mining threads.

## Performance Tips

1. **Thread Count**: 
   - For CPU mining, use number of CPU cores or cores - 1
   - Too many threads can slow down your system
   - Monitor system performance and adjust accordingly

2. **Mining Address**:
   - Create a dedicated mining address for easier tracking
   - Label it "Mining" in the Addresses tab

3. **Network Difficulty**:
   - Solo mining is profitable mainly on low-difficulty networks
   - Check network difficulty before mining (visible in mining info)
   - Higher difficulty = longer time to find blocks

4. **System Resources**:
   - Mining is CPU-intensive
   - Close unnecessary applications while mining
   - Ensure adequate cooling for extended mining sessions

## Technical Details

### Architecture

- **Module**: `trinity_wallet_py/core/miner.py`
- **Algorithm**: SHA256d (double SHA-256)
- **RPC Integration**: Uses `getwork` protocol
- **Threading**: Python threading with separate worker threads
- **GUI Updates**: Statistics updated every 2 seconds

### Code Components

1. **SoloMiner Class** (`core/miner.py`):
   - Manages mining threads
   - Implements SHA256d proof-of-work
   - Tracks statistics
   - Provides callback mechanism for GUI updates

2. **RPC Extensions** (`core/rpc_client.py`):
   - `getwork()`: Get mining work or submit solution
   - `getblocktemplate()`: Advanced mining template support
   - `setgenerate()`: Control built-in node mining

3. **GUI Integration** (`gui/main_window.py`):
   - Mining tab UI
   - Real-time statistics display
   - Mining log viewer
   - Thread control and address selection

### Mining Algorithm

The miner implements SHA256d (double SHA-256) mining:

```
1. Get work data from node (80-byte block header)
2. Pre-hash first 76 bytes (static part)
3. For each nonce value:
   a. Append nonce to pre-hash
   b. Calculate SHA256(SHA256(header))
   c. Check if hash < target
   d. If valid, submit solution
4. Request new work and repeat
```

## Troubleshooting

### "Not connected to Trinity node"
- Ensure trinityd is running
- Check RPC credentials in Settings → Connect to Node
- Verify node is listening on port 6420

### "Failed to get work"
- Node might not be fully synchronized
- Check node logs for errors
- Ensure RPC server is enabled (server=1 in trinity.conf)

### Low or Zero Hashrate
- Increase thread count
- Check CPU usage (should be high)
- Restart mining to refresh connection

### No Blocks Found
- This is normal for solo mining on high-difficulty networks
- Solo mining requires patience and luck
- Consider network difficulty before expecting results

### Mining Stops Unexpectedly
- Check mining log for error messages
- Node might have disconnected or stopped
- Restart both node and wallet

## Comparison to Pool Mining

### Solo Mining (This Implementation)
- ✅ Keep all block rewards (no pool fees)
- ✅ Direct to your wallet
- ✅ No external dependencies
- ❌ Irregular rewards (can be days/weeks between blocks on high-difficulty networks)
- ❌ Lower total expected rewards on high-difficulty networks

### Pool Mining
- ✅ Regular smaller payouts
- ✅ Better for high-difficulty networks
- ❌ Pool fees (typically 1-3%)
- ❌ Requires external pool software
- ❌ Trust in pool operator

**Recommendation**: Solo mining is best for:
- Low-difficulty networks
- Testing/learning purposes
- Supporting network decentralization
- When you have significant hashrate

## Security Considerations

1. **RPC Security**: The miner connects to your local node via RPC
   - Keep RPC credentials secure
   - Only allow localhost connections (default)
   - Do not expose RPC port to the internet

2. **Mining Address**: 
   - Keep your wallet encrypted
   - Backup your wallet regularly
   - Use a strong passphrase

3. **CPU Usage**:
   - Mining uses significant CPU resources
   - Monitor system temperature
   - Reduce threads if system becomes unstable

## Future Enhancements

Potential future improvements:
- [ ] Scrypt and Groestl algorithm support
- [ ] Mining pool protocol support (Stratum)
- [ ] GPU mining integration
- [ ] Profit calculator
- [ ] Temperature monitoring
- [ ] Mining profiles (save/load configurations)

## Credits

Based on the original pyminer.py from Bitcoin/Trinity contrib, adapted and modernized for Python 3 and GUI integration.

## License

MIT License - Same as Trinity Core

## Support

For issues or questions:
- Check the Trinity Wallet documentation
- Review node logs for RPC errors
- Open an issue on the Trinity GitHub repository
