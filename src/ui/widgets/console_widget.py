"""
该模块用于处理控制台输出组件
"""

from PyQt5.QtWidgets import QTextEdit


class ConsoleOutput(QTextEdit):
    def __init__(self):
        super().__init__()
        self._init_console()

    def _init_console(self):
        """
        初始化控制台输出设置
        """

        self.setReadOnly(True)
        self.setPlaceholderText("控制台输出将显示在这里...")

        # 设置固定高度
        self.setFixedHeight(150)
