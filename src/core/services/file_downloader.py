"""
该模块用于实现文件下载
"""

from PyQt5.QtCore import QThread, pyqtSignal
import requests
import os
import sys

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from utils.logger import Logger
    from ui.dialogs.message_dialog import MessageDialog
except ImportError as e:
    Logger.error("file_downloader.py", "file_downloader", "ImportError: " + str(e))


class DownloadThread(QThread):
    # ------------------------------ 下载进度信号 start
    # 进度信号
    progress_signal = pyqtSignal(int)

    # 状态信号
    status_signal = pyqtSignal(str)

    # 完成信号
    finished_signal = pyqtSignal(bool)
    # ------------------------------ 下载进度信号 end

    def __init__(self, api_url, download_url, save_path):
        super().__init__()
        self.download_url = download_url
        self.save_path = save_path
        self.api_url = api_url
        self.release_info = None

    def run(self):
        try:
            self.status_signal.emit("准备更新...")

            # 获取发布信息
            response = requests.get(self.api_url)
            response.raise_for_status()

            # 开始下载
            self.status_signal.emit("准备开始下载...")

            # 下载到临时文件
            temp_path = f"{self.save_path}.tmp"

            # 开始流下载文件
            response = requests.get(self.download_url, stream=True)
            print(response)

            # 获取文件大小
            total_size = int(response.headers.get("content-length", 0))

            if total_size == 0:
                self.status_signal.emit("无法获取文件大小")
                self.finished_signal.emit(False)
                return

            # 每次下载的块大小
            block_size = 1024

            # 已下载大小
            downloaded = 0

            with open(temp_path, "wb") as f:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    f.write(data)

                    # 计算下载进度
                    progress = int((downloaded / total_size) * 100)

                    # 发送下载进度信号
                    self.progress_signal.emit(progress)

                    # 根据进度显示不同的提示语
                    progress_messages = [
                        "正在偷偷下载更新...",
                        "正在注入代码到嬉笑颠...",
                        "正在拼装代码...",
                        "正在充能...",
                        "马上就好...",
                    ]
                    message_index = min(progress // 20, len(progress_messages) - 1)
                    self.status_signal.emit(f"{progress_messages[message_index]}")

            # 下载完成后替换文件
            if os.path.exists(self.save_path):
                os.remove(self.save_path)
            os.rename(temp_path, self.save_path)

            # 发送完成状态信号
            self.status_signal.emit("更新完成!")

            # 发送完成信号
            self.finished_signal.emit(True)

        except Exception as e:
            self.status_signal.emit("更新失败，请检查网络")
            MessageDialog.show_error("出错啦", "更新失败: {}".format(str(e)))
            self.finished_signal.emit(False)
