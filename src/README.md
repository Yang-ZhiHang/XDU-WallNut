# 测试

此处进行项目重构

## 1.重构项目结构

```bash
src/
├── core/                  # 核心业务逻辑
│   ├── config/            # 配置相关
│   │   ├── settings.py    # 全局配置
│   │   └── constants.py   # 常量定义
│   └── services/          # 业务服务
│       └── evaluator.py   # 评教服务
├── ui/                    # UI 相关
│   ├── windows/           # 窗口
│   │   └── main_window.py 
│   ├── widgets/           # 可复用组件
│   │   ├── input_form.py 
│   │   └── console.py 
│   └── styles/            # 样式文件
├── utils/                 # 工具类
└── main.py                # 入口文件
```

## 2.重构代码（组件模块化）

## 3.配置集中管理

## 4.业务逻辑分离
