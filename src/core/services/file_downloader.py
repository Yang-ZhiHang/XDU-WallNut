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
        temp_path = f"{self.save_path}.tmp"
        try:
            self.status_signal.emit("准备更新...")
            self.status_signal.emit("准备开始下载...")

            # 设置超时时间
            response = requests.get(
                self.download_url, stream=True, timeout=10  # 添加10秒超时
            )
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            if total_size == 0:
                raise Exception("无法获取文件大小")

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
                        "正在从 Github 下载更新...",
                        "正在注入代码到西小电...",
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

        except requests.exceptions.Timeout:
            self.status_signal.emit("下载超时，请检查网络连接")
            Logger.error("file_downloader.py", "run", "下载超时")
            self.finished_signal.emit(False)

        except requests.exceptions.RequestException as e:
            self.status_signal.emit("网络连接失败")
            Logger.error("file_downloader.py", "run", f"网络连接失败: {str(e)}")
            self.finished_signal.emit(False)

        except Exception as e:
            self.status_signal.emit("更新失败，请检查网络")
            Logger.error("file_downloader.py", "run", f"下载失败: {str(e)}")
            self.finished_signal.emit(False)

        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception as e:
                    Logger.error(
                        "file_downloader.py", "run", f"清理临时文件失败: {str(e)}"
                    )

            # 确保线程正常结束
            self.quit()
            self.wait()  # 等待线程结束
