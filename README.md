<div align="center">
    <h1>
        一键评教 WallNut 版
    </h1>
    本资源仅供学习交流使用，严禁用于商业与非法用途，请于24小时内删除。
    <br>
    本程序初衷仅用于学习 VBS 脚本的编写和 Python 小程序的开发。
    <br>
    如果有大佬欢迎贡献你的想法!
</div>


---

<div>
    据说西电貌似有个要求: 不评教不能查看学期考成绩。
    <br>
    But: "这么多教师，每个教师我都想选非常满意，全部评完得花个几分钟慢慢点。"
    <br>
    于是乎作者写了段 VBS 脚本🤔，实现了自动评教的功能，并编译为可执行程序。
</div>



---

### 🚀 更新概况 🚀

- **2024 年 11 月 17 日**：优化了用户界面，增加了代码的可维护性
- **2024 年 10 月 19 日**：修复了若干 bug
- **2024 年 10 月 15 日**：更新了 UI，优化了用户体验
- **2024 年 10 月 14 日**：添加了部分功能

---

## 食用说明

**1. 下载 releases 最新版的压缩包**

<img src='./assert/1.png'>

<img src='./assert/2.png'>

**2. 解压压缩包**

这个不用我说了吧 QwQ

解压至随便哪个目录都可以，你喜欢就行

**3. 双击运行 main.exe 文件即可**

运行后自动跳转到评教页面，需要手动登录（如果你没有登录过的话）

<img src='./assert/3.png'>

## 开发者指南

> 打包 main.py 为 exe 文件（使用 PyInstaller）

**1. 安装 PyInstaller**

打开终端，安装 pyinstaller 包：

```bash
pip install pyinstaller
```

**2. 打包**

首先在根目录执行一下命令：

```
pyinstaller -F main.py
```

这将会生成 `main.spec` 文件（其他文件忽略），

根据需要配置该文件，配置完成后执行以下命令即可完成 `XDU_WallNut.exe` 的编译：

```
pyinstaller main.spec
```

作者的 `main.spec` 配置：

```
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [
        'main.py',
        'D:/dev/XDU_WallNut/ui/__init__.py',
        'D:/dev/XDU_WallNut/ui/base_window.py',
        'D:/dev/XDU_WallNut/ui/components/console_section.py',
        'D:/dev/XDU_WallNut/ui/components/input_section.py',
        'D:/dev/XDU_WallNut/ui/components/console_section.py',
        'D:/dev/XDU_WallNut/utils/__init__.py',
        'D:/dev/XDU_WallNut/utils/browser_utils.py',
        'D:/dev/XDU_WallNut/utils/config_handler.py',
        'D:/dev/XDU_WallNut/utils/style_loader.py',
    ],  # 此项目中所有的 python 脚本
    pathex=['D:\\dev\\XDU_WallNut'],  # 项目绝对路径
    binaries=[],
    datas=[
        ('styles/style.qss', 'styles'),
        ('favicon.ico', '.')
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
    icon='D:/dev/XDU_WallNut/favicon.ico',  # 图标路径
    console=False 
)
```

