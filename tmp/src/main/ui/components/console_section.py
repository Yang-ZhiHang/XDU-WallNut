"""
该模块用于处理控制台输出组件初始化
"""

from PyQt5.QtWidgets import QTextEdit


class ConsoleSection(QTextEdit):
    def __init__(self, window):
        super().__init__()

        # 初始化窗口
        self.window = window

    def init_console_output(self):
        """
        控制台输出
        """
        self.window.console_output = QTextEdit(self.window)

        # 设置只读
        self.window.console_output.setReadOnly(True)

        self.window.console_output.setPlaceholderText("控制台输出将显示在这里...")
