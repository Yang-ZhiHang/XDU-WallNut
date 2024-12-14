# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [
        'D:/code/dev/XDU-WallNut/src/updater.py',
        'D:/code/dev/XDU-WallNut/src/core/configs/settings.py',
        'D:/code/dev/XDU-WallNut/src/core/services/file_downloader.py',
        'D:/code/dev/XDU-WallNut/src/core/icons.py',
        'D:/code/dev/XDU-WallNut/src/resources/resources_rc.py',
        'D:/code/dev/XDU-WallNut/src/ui/dialogs/message_dialog.py',
        'D:/code/dev/XDU-WallNut/src/ui/widgets/title_bar_widget.py',
        'D:/code/dev/XDU-WallNut/src/ui/windows/progress_window.py',
        'D:/code/dev/XDU-WallNut/src/utils/logger.py',
    ],  # 此项目中所有的 python 脚本
    pathex=['D:/code/dev/XDU-WallNut/src'],  # 项目绝对路径
    binaries=[],
    datas=[
        ('data/version.json', 'data')
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
    name='updater',  # 打包程序的名字
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    icon='D:/code/dev/XDU-WallNut/src/resources/updater.ico',  # 图标路径
    console=False ,
    distpath='D:\\code\\dev\\XDU-WallNut\\dist',  # 打包输出路径
)