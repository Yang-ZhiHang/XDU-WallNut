import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui, QtCore
from utils.browser_utils import open_website
from utils.config_handler import ConfigHandler
from ui.base_window import BaseWindow
from ui.components.progress_handler import ProgressHandler
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

class XDUScript(BaseWindow):
    def __init__(self):
        super().__init__()

        # 初始化配置处理器
        self.config_handler = ConfigHandler(self)

        # 初始化进度处理器
        self.progress_handler = ProgressHandler(self)

        # 连接开始按钮的点击事件
        self.start_button.clicked.connect(self.config_handler.get_config)

        # 初始化时打开网页
        open_website(
            "https://ehall.xidian.edu.cn/jwapp/sys/wspjyyapp/*default/index.do",
            self.console_output,
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = XDUScript()
    ex.show()
    sys.exit(app.exec_())
