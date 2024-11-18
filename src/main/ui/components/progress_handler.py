"""
该模块用于处理进度相关操作
"""

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor
import random
import os
import subprocess
from utils.config_handler import ConfigHandler

class ProgressHandler:
    def __init__(self, window):
        self.window = window
        self.window.progress = 0
        self.window.timer = QTimer()
        
    def singal_output(self):
        """
        初始化信号
        """
        QTimer.singleShot(1000, lambda: None)
        self.window.console_output.append("\n开始初始化...\n")
        self.window.progress = 0
        self.window.progress_line = self.window.console_output.textCursor().position()
        self.window.timer = QTimer(self.window)
        self.window.timer.timeout.connect(self.update_progress)
        self.window.timer.start(50)  # 每50毫秒更新一次进度

    def update_progress(self):
        """
        更新进度
        """
        if self.window.progress < 94:
            self.window.progress += random.randint(1, 5)
        cursor = self.window.console_output.textCursor()
        cursor.setPosition(self.window.progress_line)
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(f"初始化进度：{self.window.progress}%")
        self.window.console_output.setTextCursor(cursor)

        if self.window.progress >= 94:
            self.window.progress = 100
            self.window.timer.stop()
            QTimer.singleShot(1000, lambda: None)
            self.done_singal()

    def done_singal(self):
        """
        初始化完成
        """
        self.window.console_output.append("初始化完成！")
        QTimer.singleShot(1000, self.execute_script)

    def execute_script(self):
        """
        执行脚本
        """
        self.window.console_output.append("\n正在启动脚本...")

        try:
            # 执行根目录下的 exe
            config_params = ConfigHandler.get_config_params(self)
            exe_path = os.path.join(os.getcwd(), "vbslauncher.exe")
            result = subprocess.run(
                [exe_path] + config_params, capture_output=True, text=True
            )

            if result.returncode == 0:
                self.window.console_output.append("\n脚本执行成功！")
                self.window.console_output.append(result.stdout)
                self.window.start_button.setEnabled(True)
            else:
                self.window.console_output.append("\n脚本执行失败")
                self.window.console_output.append(result.stderr)
        except Exception as e:
            self.window.console_output.append(f"\n执行脚本时发生错误：{str(e)}")
            self.window.start_button.setEnabled(True)