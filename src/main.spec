# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [
        'D:/code/dev/XDU_WallNut/src/main.py',
        'D:/code/dev/XDU_WallNut/src/core/configs/constants.py',
        'D:/code/dev/XDU_WallNut/src/core/configs/settings.py',
        'D:/code/dev/XDU_WallNut/src/core/loaders/style_loader.py',
        'D:/code/dev/XDU_WallNut/src/core/loaders/web_loader.py',
        'D:/code/dev/XDU_WallNut/src/core/services/evaluator.py',
        'D:/code/dev/XDU_WallNut/src/core/services/file_downloader.py',
        'D:/code/dev/XDU_WallNut/src/core/icons.py',
        'D:/code/dev/XDU_WallNut/src/resources/resources_rc.py',
        'D:/code/dev/XDU_WallNut/src/ui/dialogs/message_dialog.py',
        'D:/code/dev/XDU_WallNut/src/ui/widgets/console_widget.py',
        'D:/code/dev/XDU_WallNut/src/ui/widgets/input_form_widget.py',
        'D:/code/dev/XDU_WallNut/src/ui/widgets/start_button_widget.py',
        'D:/code/dev/XDU_WallNut/src/ui/widgets/title_bar_widget.py',
        'D:/code/dev/XDU_WallNut/src/ui/windows/main_window.py',
        'D:/code/dev/XDU_WallNut/src/ui/windows/progress_window.py',
        'D:/code/dev/XDU_WallNut/src/utils/logger.py',
    ],  # 此项目中所有的 python 脚本
    pathex=['D:/code/dev/XDU_WallNut/src/main'],  # 项目绝对路径
    binaries=[],
    datas=[
        ('ui/styles/base.qss', 'styles'),
        ('data/version.json', '.')
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
    icon='D:/code/dev/XDU_WallNut/src/resources/icons/logo.png',  # 图标路径
    console=False ,
    distpath='D:/code/dev/XDU_WallNut/dist',  # 打包输出路径
)