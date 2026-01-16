Trinity Mining Guide
====================

Trinity supports multiple mining algorithms (SHA256D, Scrypt, and Groestl) and can be mined using various mining software.

## Mining Software Options

### 1. Built-in CPU Miner (Trinity Core)
The Trinity Core wallet includes built-in CPU mining capabilities. While suitable for testing and small-scale mining, it's not recommended for serious mining operations.

**Usage:**
- Enable mining in `trinity.conf`:
  ```
  gen=1
  genproclimit=1
  ```
- Or use the Debug Console: `setgenerate true 1`

### 2. Python Reference Miner
Located in `contrib/pyminer/`, this is a pure Python CPU miner primarily for educational purposes.

**Features:**
- Pure Python implementation
- Getwork protocol support
- Configurable threads
- See `contrib/pyminer/README` for details

### 3. EasyMiner (GUI Mining Software)

EasyMiner is a popular GUI-based mining software that provides an easy-to-use interface for cryptocurrency mining.

**Source Code:**
- Available at: https://sourceforge.net/projects/easyminer/files/source/

**Features:**
- Graphical user interface
- Multi-pool support
- Algorithm support for SHA256D
- Suitable for beginners

**Note:** When configuring EasyMiner for Trinity:
- Use Trinity's RPC port: 6420 (default)
- Set appropriate algorithm (SHA256D, Scrypt, or Groestl)
- Configure your RPC credentials from `trinity.conf`

### 4. External Mining Software

Trinity is compatible with standard mining software that supports its algorithms:

**For SHA256D:**
- CGMiner
- BFGMiner
- Mining pools with standard stratum protocol

**For Scrypt:**
- CGMiner (with scrypt support)
- SGMiner
- Mining pools with scrypt stratum support

**For Groestl:**
- SGMiner with groestl support
- Mining pools with groestl stratum support

## Pool Mining

Trinity supports pool mining through standard protocols. Configure your mining software to connect to Trinity-compatible pools.

**RPC Configuration:**
In your `trinity.conf`:
```
server=1
rpcuser=yourusername
rpcpassword=yourpassword
rpcport=6420
rpcallowip=127.0.0.1
```

## Solo Mining

For solo mining, point your mining software to your local Trinity daemon:
- Host: 127.0.0.1
- Port: 6420
- Use getwork or stratum protocol

## Mining Pool Service

Trinity also includes a Python-based mining pool service in the backend framework:
- Located in `trinity_wallet_py/backend/services/mining_pool.py`
- REST API available via `trinity_wallet_py/backend/api/mining_pool_api.py`
- See `trinity_wallet_py/backend/README.md` for details

## Performance Considerations

- **CPU Mining**: Only practical for testing or very low difficulty
- **GPU Mining**: Recommended for serious mining
- **ASIC Mining**: Available for SHA256D algorithm
- Choose the appropriate algorithm based on available hardware

## Security Notes

- Never expose RPC ports to the internet
- Use strong RPC credentials
- Keep your mining software updated
- Use SSL/TLS when connecting to remote pools

## Additional Resources

- Trinity GitHub: https://github.com/Action-Committee/Trinity_py
- Mining Pool service documentation: `trinity_wallet_py/backend/README.md`
- Reference implementation: `contrib/pyminer/`

For more information about Trinity specifications and algorithms, see the main README.md.
