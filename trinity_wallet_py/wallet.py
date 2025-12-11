#!/usr/bin/env python3
"""
Trinity Wallet - Main Entry Point
A Python-based Windows wallet for Trinity cryptocurrency.
"""

import sys
import os

# Add parent directory to path if needed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trinity_wallet_py.gui.main_window import TrinityWalletGUI


def main():
    """Main entry point for the wallet."""
    print("Starting Trinity Wallet...")
    
    # Create and run the GUI
    app = TrinityWalletGUI()
    app.run()


if __name__ == '__main__':
    main()
