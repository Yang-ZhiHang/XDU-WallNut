"""
标题栏组件
"""

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import os

try:
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "./../../"))
    )
    from utils.logger import Logger
    from core.configs.settings import Settings
    from core.icons import Icon
except ImportError as e:
    Logger.error(
        "title_bar_widget.py", "title_bar_widget", "ImportError: " + str(e), color="red"
    )


class TitleBarWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._init_component()

        self._set_component_style()

        self._apply_component()

    def _init_component(self):

        self.title_bar = QHBoxLayout()

        self.icon_label = QLabel()
        icon_size = (30, 30)
        self.icon_label.setFixedSize(*icon_size)
        icon_pixmap = QIcon(Icon.logo_ico_path).pixmap(*icon_size)
        self.icon_label.setPixmap(icon_pixmap)

        self.title_label = QLabel(Settings.WINDOW_TITLE)
        self.min_button = QPushButton("－")
        self.close_button = QPushButton("×")

        self.min_button.setFixedSize(30, 30)
        self.close_button.setFixedSize(30, 30)

        self.title_bar.setContentsMargins(0, 0, 0, 0)
        self.title_bar.setSpacing(0)
        self.title_bar.addWidget(self.icon_label)
        self.title_bar.addWidget(self.title_label)
        self.title_bar.addWidget(self.min_button)
        self.title_bar.addWidget(self.close_button)

    def _set_component_style(self):

        # 设置样式
        self.setStyleSheet(
            """
            QWidget {
                background-color: #1e1e1e;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """
        )

        # 设置按钮样式
        button_style = """
            QPushButton {
                margin: 1px;
                padding: 0px;
                border: none;
                color: #ffffff;
                font-size: 16px;
                font-family: 'Microsoft YaHei';
            }
        """

        min_button_style = (
            button_style
            + """
            QPushButton:hover {
                background-color: #404040;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
        """
        )

        close_button_style = (
            button_style
            + """
            QPushButton:hover {
                background-color: #e81123;
            }
            QPushButton:pressed {
                background-color: #d31019;
            }
        """
        )

        self.min_button.setStyleSheet(min_button_style)
        self.close_button.setStyleSheet(close_button_style)
        self.title_label.setStyleSheet(
            """
            QLabel {
                color: #ffffff;
                font-size: 14px;
                padding-left: 10px;
            }
        """
        )

    def _apply_component(self):
        self.setLayout(self.title_bar)

    # ------------------------------- 窗口拖动 start
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos()
            self.window_position = self.window().pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.drag_start_position
            self.window().move(self.window_position + delta)

    # ------------------------------- 窗口拖动 end
