"""
该模块用于实现更新相关对话框
"""

from PyQt5.QtWidgets import QMainWindow, QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import os
import sys

from core.services.update_checker import UpdateChecker

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from core.services.file_donwloader import DownloadThread
    from utils.logger import Logger
    from core.configs.settings import Settings
except ImportError as e:
    Logger.error("updating_dialog.py", "updating_dialog", "ImportError: " + str(e))


class UpdateWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle(Settings.UPDATE_WINDOW_TITLE)

        # 设置窗口大小
        self.setFixedSize(Settings.UPDATE_WINDOW_SIZE)

        self._set_main_layout()
        self._load_components()
        self._set_component_style()
        self._apply_components()

    def _set_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()

    def _load_components(self):
        """
        初始化更新窗口的 UI
        UI 总体布局：
         | - windows title ----------------------------- |
         |               initializing...(status label)   |
         | ///////////// 50%(progress bar) ///           |
         |                                               |
         | --------------------------------------------- |
        """

        # 状态标签
        self.status_label = QLabel("正在初始化...")

        # 进度条
        self.progress_bar = QProgressBar()

    def _set_component_style(self):
        self.status_label.setAlignment(Qt.AlignCenter)

    def _apply_components(self):
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.progress_bar)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def start_update(self):
        # 获取程序路径
        if getattr(sys, "frozen", False):
            app_path = os.path.dirname(sys.executable)
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))

        exe_path = os.path.join(app_path, "XDU_WallNut.exe")

        # 创建下载线程
        self.download_thread = DownloadThread(
            Settings.GITHUB_API,
            Settings.GITHUB_EXE_URL,
            exe_path,
        )

        # 连接信号
        self.download_thread.progress_signal.connect(self.progress_bar.setValue)
        self.download_thread.status_signal.connect(self.status_label.setText)
        self.download_thread.finished_signal.connect(self.update_finished)

        # 启动下载
        self.download_thread.start()

    def update_finished(self, success, update_checker: UpdateChecker):
        """
        更新完成，保存版本信息，重启主程序，关闭更新器
        """
        if success:
            update_checker.update_version_file()

            # 重启主程序
            os.startfile("XDU_WallNut.exe")

            # 关闭更新器
            sys.exit()
