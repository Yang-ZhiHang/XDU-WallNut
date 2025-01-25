"""
该模块用于文件相关操作
"""

import os
import sys

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    from utils.logger import Logger
except ImportError as e:
    Logger.error("main.py", "main", "ImportError: " + str(e))


def get_app_path():
    # 如果是打包后的 exe
    if getattr(sys, "frozen", False):
        app_path = os.path.dirname(sys.executable)
    # 如果是开发环境
    else:
        app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return app_path
