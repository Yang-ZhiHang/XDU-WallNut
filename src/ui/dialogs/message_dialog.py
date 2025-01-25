"""
该模块用于实现消息提示对话框
"""

from PyQt5.QtWidgets import QMessageBox, QTextBrowser
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
import sys

import markdown

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    import resources.resources_rc
    from core.icons import Icon
    from utils.logger import Logger
except ImportError as e:
    Logger.error(
        "message_dialog.py", "message_dialog", "ImportError: " + str(e), color="red"
    )


class MessageDialog:
    @staticmethod
    def show_info(
        title: str = "提示",
        message: str = "",
        ok_text: str = "确定",
        cancel_text: str = "取消",
    ) -> bool:
        """
        信息提示框

        Args:
            title: 提示框标题
            message: 提示消息内容
            ok_text: 确定按钮文本
            cancel_text: 取消按钮文本

        Returns:
            bool: 如果用户点击确定返回True，点击取消返回False
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)

        # 如果 message 是 QTextBrowser 对象
        if isinstance(message, QTextBrowser):
            # 设置 QTextBrowser 的大小策略
            message.setMinimumWidth(400)  # 最小宽度
            message.setMinimumHeight(200)  # 最小高度
            message.document().setDocumentMargin(10)  # 设置文档边距

            # 计算内容需要的大小
            doc_size = message.document().size().toSize()
            message.setFixedWidth(
                min(600, max(400, doc_size.width() + 20))
            )  # 限制最大宽度为600
            message.setFixedHeight(
                min(400, max(200, doc_size.height() + 20))
            )  # 限制最大高度为400

            msg_box.layout().addWidget(message, 1, 1, 1, msg_box.layout().columnCount())
        else:
            msg_box.setText(message)

        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowIcon(QIcon(Icon.info_ico_path))
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ok_button = msg_box.button(QMessageBox.Ok)
        ok_button.setText(ok_text)
        cancel_button = msg_box.button(QMessageBox.Cancel)
        cancel_button.setText(cancel_text)

        result = msg_box.exec_()
        return result == QMessageBox.Ok

    @staticmethod
    def show_warning(
        title: str = "警告",
        message: str = "",
        ok_text: str = "确定",
        cancel_text: str = "取消",
    ) -> bool:
        """警告提示框"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowIcon(QIcon(Icon.warning_ico_path))
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ok_button = msg_box.button(QMessageBox.Ok)
        ok_button.setText(ok_text)
        cancel_button = msg_box.button(QMessageBox.Cancel)
        cancel_button.setText(cancel_text)

        result = msg_box.exec_()
        return result == QMessageBox.Ok

    @staticmethod
    def show_error(
        title: str = "错误",
        message: str = "",
        ok_text: str = "确定",
        cancel_text: str = "取消",
    ) -> bool:
        """错误提示框"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowIcon(QIcon(Icon.error_ico_path))
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ok_button = msg_box.button(QMessageBox.Ok)
        ok_button.setText(ok_text)
        cancel_button = msg_box.button(QMessageBox.Cancel)
        cancel_button.setText(cancel_text)

        result = msg_box.exec_()
        return result == QMessageBox.Ok

    @staticmethod
    def show_update(
        title: str = "更新提示",
        version_info: dict = {},
        ok_text: str = "前往",
        cancel_text: str = "取消",
    ) -> bool:
        """更新提示框"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)

        # 创建版本信息标签
        version_text = QTextBrowser()
        version_text.setMaximumHeight(30)  # 限制高度
        version_text.setHtml(
            f'<div style="text-align: left; font-size: 14px;">有新版本可用: {version_info.get("current_version", "")} -> {version_info.get("latest_version", "")}</div>'
        )
        version_text.setFrameShape(QTextBrowser.NoFrame)  # 移除边框

        # 创建并设置更新内容的 QTextBrowser
        content = QTextBrowser()
        content.setMinimumWidth(400)  # 设置更大的最小宽度
        content.setMinimumHeight(300)  # 设置更大的最小高度
        content.document().setDocumentMargin(10)
        # 将 markdown 转换为 HTML
        content_html = markdown.markdown(version_info["release_notes"])
        content.setHtml(content_html)

        # # 设置消息框的最小尺寸
        # msg_box.setMinimumWidth(600)  # 设置消息框最小宽度
        # msg_box.setMinimumHeight(800)  # 设置消息框最小高度

        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.NoIcon)  # 不显示弹窗内图标
        msg_box.setWindowIcon(QIcon(Icon.info_ico_path))
        layout = msg_box.layout()

        # 0, 0, 1, layout.columnCount() 分别表示:
        # - 起始行: 0
        # - 起始列: 0
        # - 占用行数: 1
        # - 占用列数: layout.columnCount()layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(
            version_text, 0, 0, 1, layout.columnCount(), Qt.AlignLeft
        )  # 添加版本信息到第一行
        layout.addWidget(
            content, 1, 0, 1, layout.columnCount(), Qt.AlignCenter
        )  # 添加更新内容到第二行
        layout.setSizeConstraint(layout.SetNoConstraint)

        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.button(QMessageBox.Ok).setText(ok_text)
        msg_box.button(QMessageBox.Cancel).setText(cancel_text)
        return msg_box.exec_() == QMessageBox.Ok
