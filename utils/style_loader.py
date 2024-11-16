import os
import sys

def load_stylesheet():
    try:
        # 获取应用程序的基础路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            base_path = sys._MEIPASS
        else:
            # 如果是开发环境
            base_path = os.path.abspath(".")

        # 构建样式文件的完整路径
        style_file = os.path.join(base_path, "styles", "style.qss")
        
        with open(style_file, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"样式表加载失败：{str(e)}")
        return ""