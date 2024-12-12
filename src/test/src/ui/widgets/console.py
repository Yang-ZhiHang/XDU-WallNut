"""
该模块用于处理控制台输出组件
"""

from PyQt5.QtWidgets import QTextEdit


class ConsoleSection(QTextEdit):
    def __init__(self):
        super().__init__()
        self._init_console()

    def _init_console(self):
        """
        控制台输出
        """
        self.console_output = QTextEdit()

        # 设置只读
        self.console_output.setReadOnly(True)

        self.console_output.setPlaceholderText("控制台输出将显示在这里...")
