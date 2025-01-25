"""
该文件用于存放全局配置
"""

import os


class Settings:

    # 应用相关
    APP_NAME = "XDU_WallNut"

    # 窗口相关
    WINDOW_TITLE = "XDU WallNut 一键评教"
    WINDOW_SIZE = (400, 600)

    # 更新窗口相关
    UPDATE_WINDOW_TITLE = "XDU WallNut 更新程序"
    UPDATE_WINDOW_SIZE = (800, 150)

    # 更新相关
    GITHUB_APP_PAGE_URL = "https://github.com/Yang-ZhiHang/XDU-WallNut"
    GITHUB_API = "https://api.github.com/repos/Yang-ZhiHang/XDU-WallNut/releases/latest"
    GITHUB_EXE_URL = "https://github.com/Yang-ZhiHang/XDU-WallNut/releases/latest/download/XDU_WallNut.exe"

    BASE_DIR = ""

    @staticmethod
    def get_base_dir():
        """获取程序运行目录"""
        import sys

        if getattr(sys, "frozen", False):
            # 如果是打包后的可执行文件
            BASE_DIR = os.path.dirname(sys.executable)
        else:
            # 如果是源码运行
            BASE_DIR = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
        return BASE_DIR
