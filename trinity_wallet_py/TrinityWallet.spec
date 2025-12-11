# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Trinity Wallet
Builds a standalone Windows executable
"""

block_cipher = None

a = Analysis(
    ['wallet.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('INSTALL.md', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.simpledialog',
        'tkinter.messagebox',
        'ecdsa',
        'ecdsa.util',
        'ecdsa.curves',
        'hashlib',
        'http.client',
        'json',
        'threading',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TrinityWallet',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path if available
)
