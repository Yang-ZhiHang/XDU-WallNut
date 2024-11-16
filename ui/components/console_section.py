from PyQt5.QtWidgets import QTextEdit

class ConsoleSection(QTextEdit):
    def __init__(self):
        super().__init__()

        # 设置只读
        self.setReadOnly(True)

        # 设置占位符
        self.setPlaceholderText("控制台输出将显示在这里...")
    