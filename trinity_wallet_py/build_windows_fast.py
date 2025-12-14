#!/usr/bin/env python3
"""
Ultra-fast Windows .exe build script for Trinity Wallet.
Optimized PyInstaller configuration for minimal build time.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def main():
    """Build Windows executable with optimized settings."""
    
    print("=" * 60)
    print("Trinity Wallet - Ultra-Fast Windows Build")
    print("=" * 60)
    
    # Check if we're in the right directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print(f"\nWorking directory: {os.getcwd()}")
    
    # Check dependencies
    print("\n[1/5] Checking dependencies...")
    try:
        import PyInstaller
        print(f"  ✓ PyInstaller {PyInstaller.__version__} installed")
    except ImportError:
        print("  ✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("  ✓ PyInstaller installed")
    
    try:
        import ecdsa
        print(f"  ✓ ecdsa {ecdsa.__version__} installed")
    except ImportError:
        print("  ✗ ecdsa not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ecdsa==0.19.1"])
        print("  ✓ ecdsa installed")
    
    # Clean previous builds for faster compile
    print("\n[2/5] Cleaning previous builds...")
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"  ✓ Removed {dir_name}/")
    
    # Remove .spec cache files
    for cache_file in ['TrinityWallet.spec.toc', 'TrinityWallet.spec.manifest']:
        cache_path = Path(cache_file)
        if cache_path.exists():
            cache_path.unlink()
            print(f"  ✓ Removed {cache_file}")
    
    # Build with optimized settings
    print("\n[3/5] Building executable with PyInstaller...")
    print("  Using TrinityWallet.spec with optimizations:")
    print("    - Single file mode (onefile)")
    print("    - UPX compression enabled")
    print("    - No console window (windowed GUI)")
    print("    - Clean build (--clean)")
    
    build_cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "TrinityWallet.spec",
        "--clean",
        "--noconfirm",
        "--log-level", "WARN"  # Reduce output for faster builds
    ]
    
    try:
        subprocess.check_call(build_cmd)
        print("  ✓ Build completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Build failed with error: {e}")
        return 1
    
    # Verify output
    print("\n[4/5] Verifying build output...")
    
    exe_path = Path("dist/TrinityWallet.exe") if sys.platform == "win32" else Path("dist/TrinityWallet")
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"  ✓ Executable created: {exe_path}")
        print(f"  ✓ Size: {size_mb:.2f} MB")
    else:
        print(f"  ✗ Executable not found at {exe_path}")
        return 1
    
    # Copy to Files folder
    print("\n[5/5] Copying to Files folder...")
    # Use path relative to script location for robustness
    script_dir = Path(__file__).parent
    files_dir = script_dir.parent / 'Files'
    files_dir.mkdir(exist_ok=True)
    
    dest_path = files_dir / exe_path.name
    shutil.copy2(exe_path, dest_path)
    print(f"  ✓ Copied to {dest_path}")
    
    # Also copy documentation
    for doc in ['README.md', 'INSTALL.md']:
        if Path(doc).exists():
            shutil.copy2(doc, files_dir / doc)
            print(f"  ✓ Copied {doc}")
    
    print("\n" + "=" * 60)
    print("BUILD COMPLETE!")
    print("=" * 60)
    print(f"\nExecutable location: {dest_path.absolute()}")
    print(f"Size: {size_mb:.2f} MB")
    print("\nYou can now run the wallet from the Files folder.")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
