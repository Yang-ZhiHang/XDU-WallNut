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
    def __init__(self, web_loader=None, console_output=None):
        super().__init__()
        self.default_icon = QIcon(Icon.logo_ico_path)
        self.hover_icon = QIcon(Icon.github_ico_path)
        self.github_url = Settings.GITHUB_APP_PAGE_URL
        self.web_loader = web_loader
        self.console_output = console_output
        self._init_component()
        self._set_component_style()
        self._apply_component()

    def _init_component(self):

        # 创建一个容器 widget 来包含所有组件：以便于设置完美的 QSS 样式
        self.container = QWidget()
        self.title_bar = QHBoxLayout()
        self.main_layout = QHBoxLayout()

        self.icon_label = QLabel()
        self.icon_size = (30, 30)
        self.icon_label.setFixedSize(*self.icon_size)
        icon_pixmap = self.default_icon.pixmap(*self.icon_size)
        self.icon_label.setPixmap(icon_pixmap)

        # 设置鼠标悬停时为手型
        self.icon_label.setCursor(Qt.PointingHandCursor)

        # QLabel 接收鼠标点击事件
        self.icon_label.setMouseTracking(True)
        self.icon_label.mousePressEvent = self.icon_clicked

        self.title_label = QLabel(Settings.WINDOW_TITLE)
        self.min_button = QPushButton("－")
        self.close_button = QPushButton("×")

        self.min_button.setFixedSize(30, 30)
        self.close_button.setFixedSize(30, 30)


    def _set_component_style(self):
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # 设置外层窗口样式
        self.setStyleSheet(
            """
            QWidget {
                background-color: transparent;
            }
            """
        )
        
        # 设置内部容器样式
        self.container.setStyleSheet(
            """
            QWidget {
                background-color: #1e1e1e;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            """
        )

        self.title_bar.setContentsMargins(0, 0, 0, 0)
        self.title_bar.setSpacing(0)

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
        self.title_bar.addWidget(self.icon_label)
        self.title_bar.addWidget(self.title_label)
        self.title_bar.addWidget(self.min_button)
        self.title_bar.addWidget(self.close_button)
        self.container.setLayout(self.title_bar)
        self.main_layout.addWidget(self.container)
        self.setLayout(self.main_layout)

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

    # 添加鼠标进入事件处理
    def enterEvent(self, event):
        hover_pixmap = self.hover_icon.pixmap(*self.icon_size)
        self.icon_label.setPixmap(hover_pixmap)

    # 添加鼠标离开事件处理
    def leaveEvent(self, event):
        default_pixmap = self.default_icon.pixmap(*self.icon_size)
        self.icon_label.setPixmap(default_pixmap)

    def icon_clicked(self, event):
        Logger.info("title_bar_widget.py", "icon_clicked", "icon clicked")
        if event.button() == Qt.LeftButton and self.web_loader:
            self.web_loader.open_website(self.github_url, self.console_output)
