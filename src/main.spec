# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [
        'main.py',
        'D:/dev/XDU_WallNut/src/main/ui/__init__.py',
        'D:/dev/XDU_WallNut/src/main/ui/base_window.py',
        'D:/dev/XDU_WallNut/src/main/ui/components/console_section.py',
        'D:/dev/XDU_WallNut/src/main/ui/components/input_section.py',
        'D:/dev/XDU_WallNut/src/main/ui/components/console_section.py',
        'D:/dev/XDU_WallNut/src/main/utils/__init__.py',
        'D:/dev/XDU_WallNut/src/main/utils/browser_utils.py',
        'D:/dev/XDU_WallNut/src/main/utils/config_handler.py',
        'D:/dev/XDU_WallNut/src/main/utils/style_handler.py',
        'D:/dev/XDU_WallNut/src/main/utils/version_checker.py',
        'D:/dev/XDU_WallNut/src/main/utils/updater.py',
    ],  # 此项目中所有的 python 脚本
    pathex=['D:\\dev\\XDU_WallNut\\src\\main'],  # 项目绝对路径
    binaries=[],
    datas=[
        ('styles/base.qss', 'styles'),
        ('favicon.ico', '.'),
        ('version.json', '.')
    ],
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
    name='XDU_WallNut',  # 打包程序的名字
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    icon='D:/dev/XDU_WallNut/src/main/favicon.ico',  # 图标路径
    console=False ,
    distpath='D:/dev/XDU_WallNut/dist',  # 打包输出路径
)