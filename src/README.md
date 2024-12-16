## 项目结构

```bash
src/
├── core/                          # 核心业务逻辑
│   ├── config/                    # 配置相关
│   ├── loader/                    # 加载器
│   ├── services/                  # 业务逻辑
│   └── icons.py                   # 图标配置
├── data/                          # 版本信息
├── resources/                     # 资源文件
├── ui/                            # UI 相关
│   ├── dialogs/                   # 对话框
│   ├── styles/                    # 样式
│   ├── widgets/                   # 可复用组件
│   └── windows/                   # 窗口
├── utils/                         # 通用工具
├── main.py                        # 主程序
├── main.spec                      # 主程序打包配置
├── updater.py                     # 更新模块
└── updater.spec                   # 更新模块打包配置
```

## 打包

```bash
# 主程序
pyinstaller main.spec --distpath "D:/code/dev/XDU-WallNut/dist"
# 更新模块
pyinstaller updater.spec --distpath "D:/code/dev/XDU-WallNut/dist"
```
