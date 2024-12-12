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
        
        # 设置只读
        self.setReadOnly(True)

        # 设置占位符文本
        self.setPlaceholderText("控制台输出将显示在这里...")
