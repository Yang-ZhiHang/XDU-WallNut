# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [
        'main.py',
        'D:/dev/XDU_WallNut/src/updater/updater_window.py',
        'D:/dev/XDU_WallNut/src/updater/thread_utils.py',
    ],  # 此项目中所有的 python 脚本
    pathex=['D:\\dev\\XDU_WallNut\\src\\updater'],  # 项目绝对路径
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure, a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Updater',  # 打包程序的名字
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    icon='D:/dev/XDU_WallNut/src/updater/updater.ico',  # 图标路径
    console=False ,
    distpath='D:/dev/XDU_WallNut/dist',  # 打包输出路径
)