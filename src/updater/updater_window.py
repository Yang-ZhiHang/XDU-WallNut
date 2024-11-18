from PyQt5.QtWidgets import QMainWindow, QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import os
import sys
import json
from thread_utils import DownloadThread


class UpdaterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化 UI
        self.initUI()

    def initUI(self):
        """
        初始化更新窗口的 UI
        UI 总体布局：
         | - windows title ----------------------------- |
         |               status label                    |
         | ///////////// progress bar 50% ///            |
         |               version label                   |
         | ------------- error label ------------------- |
        """

        # 设置窗口标题
        self.setWindowTitle("XDU WallNut 更新程序")

        # 设置窗口大小
        self.setFixedSize(800, 150)

        # 设置中央主窗口部件 layout
        main_window = QWidget()
        self.setCentralWidget(main_window)
        layout = QVBoxLayout(main_window)

        # 状态标签
        self.status_label = QLabel("正在初始化...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # 进度条
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # 版本信息标签
        self.version_label = QLabel()
        self.version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.version_label)

    def start_update(self):
        """
        开始更新
        """
        try:
            with open("version.json", "r", encoding="utf-8") as f:
                current_version = json.load(f)["version"]
        except Exception as e:
            current_version = "未知"
            self.version_label.setText(f"获取当前版本失败: {e}")

        self.version_label.setText(f"当前版本: {current_version}")

        # 获取程序路径
        if getattr(sys, "frozen", False):
            app_path = os.path.dirname(sys.executable)
        else:
            app_path = os.path.dirname(os.path.abspath(__file__))

        exe_path = os.path.join(app_path, "XDU_WallNut.exe")

        # 创建下载线程
        self.download_thread = DownloadThread(
            "https://api.github.com/repos/Yang-ZhiHang/XDU-WallNut/releases/latest",
            "https://github.com/Yang-ZhiHang/XDU-WallNut/releases/latest/download/XDU_WallNut.exe",
            exe_path,
        )

        # 检查版本
        def check_version(release_info):
            latest_version = release_info.get("tag_name", "").replace("v", "")
            if current_version != "未知" and current_version == latest_version:
                self.status_label.setText("当前已是最新版本")
                return False
            return True

        # 连接信号
        self.download_thread.progress_signal.connect(self.progress_bar.setValue)
        self.download_thread.status_signal.connect(self.status_label.setText)
        self.download_thread.finished_signal.connect(self.update_finished)
        self.download_thread.version_check_signal.connect(check_version)

        # 启动下载
        self.download_thread.start()

    def update_finished(self, success):
        """
        更新完成，保存版本信息，重启主程序，关闭更新器
        """
        if success and hasattr(self.download_thread, "release_info"):
            # 提取并保存版本信息
            release_info = self.download_thread.release_info
            version_data = {
                "version": release_info.get("tag_name", "").replace("v", ""),
                "author": release_info.get("author", ""),
                "name": release_info.get("name", ""),
                "published_at": release_info.get("published_at", ""),
                "description": release_info.get("body", ""),
            }

            try:
                with open("version.json", "w", encoding="utf-8") as f:
                    json.dump(version_data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"保存版本信息失败: {e}")

            # 重启主程序
            os.startfile("XDU_WallNut.exe")

            # 关闭更新器
            sys.exit()
