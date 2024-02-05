# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ui_manager.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\JUANC\\00_MAESTRIA VIU\\DESARROLLO_TFM\\MapComp\\logo.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ui_manager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\JUANC\\00_MAESTRIA VIU\\DESARROLLO_TFM\\MapComp\\icono.ico'],
)
