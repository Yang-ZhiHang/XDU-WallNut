"""
该模块用于实现更新相关对话框
"""

import json
from PyQt5.QtWidgets import QMainWindow, QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import os
import sys

from core.services.update_checker import UpdateChecker

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from core.services.file_downloader import DownloadThread
    from utils.logger import Logger
    from core.configs.settings import Settings
    from ui.widgets.title_bar_widget import TitleBarWidget
except ImportError as e:
    Logger.error("updating_dialog.py", "updating_dialog", "ImportError: " + str(e))


class ProgressWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle(Settings.UPDATE_WINDOW_TITLE)

        # 设置窗口大小
        self.setFixedSize(*Settings.UPDATE_WINDOW_SIZE)

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
         | --------------------------------------------- |
        """

        # 状态标签
        self.status_label = QLabel("正在初始化...")

        self.progress_bar = QProgressBar()
        self.title_bar = TitleBarWidget()

    def _set_component_style(self):
        # 窗口样式
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #2b2b2b;
                border: 1px solid #404040;
                border-radius: 4px;
            }
        """
        )

        # 状态标签样式
        self.status_label.setStyleSheet(
            """
            QLabel {
                font-family: 'Segoe UI', '微软雅黑';
                font-size: 14px;
                color: #e0e0e0;
                padding: 10px;
            }
        """
        )

        # 进度条样式
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 1px solid #404040;
                border-radius: 4px;
                text-align: center;
                background-color: #363636;
                color: #e0e0e0;
                height: 20px;
            }
            
            QProgressBar::chunk {
                background-color: #5294e2;
                border-radius: 3px;
            }
        """
        )

        self.status_label.setAlignment(Qt.AlignCenter)
        self.progress_bar.setFormat("%p%")  # %p 表示进度百分比
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口无边框

    def _apply_components(self):
        self.main_layout.addWidget(self.title_bar)
        self.title_bar.min_button.clicked.connect(self.showMinimized)
        self.title_bar.close_button.clicked.connect(self.close)
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.progress_bar)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def closeEvent(self, event):
        """重写关闭事件，删除临时文件"""
        Logger.info("ProgressWindow", "closeEvent", "Handle close event.", color="white")
        event.accept()

        # 如果下载线程存在且正在运行，则停止它
        if hasattr(self, 'download_thread') and self.download_thread.isRunning():
            Logger.info("ProgressWindow", "closeEvent", "DownloadThread is running, trying to terminate...")
            self.download_thread.terminate()
            self.download_thread.wait()
            Logger.info("ProgressWindow", "closeEvent", "DownloadThread has been terminated")

        try:
            # 获取程序路径
            if getattr(sys, "frozen", False):
                # 如果是打包后的 exe
                app_path = os.path.dirname(sys.executable)
            else:
                # 如果是开发环境
                app_path = os.path.dirname(os.path.abspath(__file__))

            # 删除临时版本文件
            tmp_version_file_path = os.path.join(app_path, "data/version.tmp")
            if not os.path.exists(tmp_version_file_path):
                tmp_version_file_path = os.path.join(app_path, "version.tmp")

            if os.path.exists(tmp_version_file_path):
                os.remove(tmp_version_file_path)
                Logger.info("ProgressWindow", "closeEvent", f"Temporary file {tmp_version_file_path} deleted successfully.")
            else:
                Logger.info("ProgressWindow", "closeEvent", f"Temporary file {tmp_version_file_path} does not exist.")

            # 删除未下载完的更新包
            exe_path = os.path.join(app_path, Settings.APP_NAME + ".exe.tmp")
            Logger.info("ProgressWindow", "closeEvent", f"Delete file: {exe_path}")
            if os.path.exists(exe_path):
                os.remove(exe_path)
                Logger.info("ProgressWindow", "closeEvent", "Update package deleted successfully.")

        except Exception as e:
            Logger.error("ProgressWindow", "closeEvent", f"Failed to delete temporary files: {str(e)}")
            
        Logger.info("ProgressWindow", "closeEvent", "Close event handled.")

    def start_update(self):
        # 获取程序路径
        if getattr(sys, "frozen", False):
            app_path = os.path.dirname(sys.executable)
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))

        exe_path = os.path.join(app_path, Settings.APP_NAME + ".exe")

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
        Logger.info("ProgressWindow", "start_update", "开始下载更新包...")
        self.download_thread.start()

    def update_finished(self, success):
        """
        更新完成，保存版本信息，重启主程序，关闭更新器
        """
        if success:
            self.update_version_file()

            # 重启主程序
            os.startfile(Settings.APP_NAME + ".exe")

            # 关闭更新器
            sys.exit()
        else:
            self.close()

    def update_version_file(self):
        """更新版本文件"""
        try:
            # 读取临时文件
            tmp_version_file_path = Settings.BASE_DIR + "/data/version.tmp"
            if not os.path.exists(tmp_version_file_path):
                tmp_version_file_path = Settings.BASE_DIR + "/version.tmp"
            with open(tmp_version_file_path, "r", encoding="utf-8") as file:
                version_info = json.load(file)
                
            # 保存到正式文件
            if not os.path.exists("data"):
                os.makedirs("data", exist_ok=True)
            with open("data/version.json", "w", encoding="utf-8") as file:
                json.dump(version_info, file, ensure_ascii=False, indent=4)
                
            # 删除临时文件
            os.remove(tmp_version_file_path)
            
            Logger.info("ProgressWindow", "update_version_file", "版本文件更新成功")
            return True

        except Exception as e:
            self.error_message = f"更新版本文件失败: {str(e)}"
            Logger.error("ProgressWindow", "update_version_file", self.error_message)
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProgressWindow()
    window.show()
    sys.exit(app.exec_())
