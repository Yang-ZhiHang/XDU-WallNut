<div align="center">
    <h1>
        一键评教 WallNut 版
    </h1>
    本资源仅供学习交流使用，严禁用于商业与非法用途，请于24小时内删除。
    <br>
    本程序初衷仅用于学习 VBS 脚本的编写和小程序的开发。
    <br>
    如果有大佬欢迎贡献你的改进!
</div>

---

<div>
    据说西电貌似有个要求: 不评教不能查看学期考成绩。
    <br>
    But: "这么多教师，每个教师我都想选非常满意，全部评完得十几分钟。"
    <br>
    于是乎作者写了段 VBS 脚本🤔，实现了自动评教的功能，并编译为可执行程序。
</div>


---


### 🚀 更新概况 🚀

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

```bash
pip install pyinstaller
```

**2. 打包**

```bash
pyinstaller --onefile --windowed main.py
```

