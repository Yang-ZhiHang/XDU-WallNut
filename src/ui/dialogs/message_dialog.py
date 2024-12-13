"""
该模块用于实现消息提示对话框
"""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
import os
import sys
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    import resources.resources_rc
    from core.icons import Icon
    from utils.logger import Logger
except ImportError as e:
    Logger.error("message_dialog.py", "message_dialog", "ImportError: " + str(e), color="red")


class MessageDialog:
    @staticmethod
    def show_info(title: str = "提示", message: str = ""):
        """
        显示信息提示框
        
        Args:
            title: 提示框标题
            message: 提示消息内容
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowIcon(QIcon(Icon.info_ico_path))
        msg_box.exec_()

    @staticmethod 
    def show_warning(title: str = "警告", message: str = ""):
        """显示警告提示框"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowIcon(QIcon(Icon.warning_ico_path))
        msg_box.exec_()

    @staticmethod
    def show_error(title: str = "错误", message: str = ""):
        """显示错误提示框"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowIcon(QIcon(Icon.error_ico_path))
        msg_box.exec_()
