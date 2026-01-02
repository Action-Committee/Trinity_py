Trinity
===================================


What is Trinity?
------------------

Trinity is a new crypto-currency that includes three algorithms and random rewards.

Specifications
------------------

- Proof of Work based. Mine using any of the 3 algorithms : sha256d(default), scrypt or groestl.

New Features
------------------

### Compressed Block Storage (NEW!)
Trinity now includes an advanced blockchain storage compression system that reduces storage requirements by 25-40% while maintaining full network compatibility. 

- **Enable with**: `-usecompression=1` command-line flag
- **Configurable compression level**: `-compressionlevel=<1-9>` (default: 6)
- **Features**:
  - Automatic deduplication of transaction patterns
  - RLE compression for repetitive data
  - Full backward compatibility with existing blocks
  - Transparent to network protocol
- See [COMPRESSED_STORAGE.md](COMPRESSED_STORAGE.md) for detailed documentation

Wallets & Services
------------------

Trinity now includes two wallet implementations and a backend service framework:

1. **Trinity Core (C++)** - Original Qt-based wallet
   - Full node with mining support
   - Located in `src/` directory
   - Requires compilation (see below)

2. **Trinity Python Wallet** - NEW! 🎉
   - Windows-compatible Python implementation
   - User-friendly GUI using tkinter
   - Located in `trinity_wallet_py/` directory
   - Quick setup: `cd trinity_wallet_py && pip install -r requirements.txt`
   - See [PYTHON_WALLET.md](PYTHON_WALLET.md) for full documentation

3. **Trinity Backend Services** - NEW! 🚀
   - Modular backend framework for cryptocurrency services
   - Block Explorer service for blockchain queries
   - Mining Pool service for pool operations
   - REST API with local and webserver deployment
   - Located in `trinity_wallet_py/backend/` directory
   - Quick start: `python -m trinity_wallet_py.backend.cli start`
   - See [trinity_wallet_py/backend/README.md](trinity_wallet_py/backend/README.md) for full documentation

License
-------

Trinity is released under the terms of the MIT license. See `COPYING` for more
information or see http://opensource.org/licenses/MIT.

Deps (for C++ Core)
------------------

you need libboost1.49-all-dev
[apt-get update 
[apt-get install build-essential liboost1.49-dev libssl-dev libdb4.8-dev libdb4.8++-dev libqrencode-dev libminiupnpc-dev git
