from PyQt5.QtCore import QThread, pyqtSignal
import requests
import os


class DownloadThread(QThread):
    """下载进度信号
    --------------------------------------"""
    # 进度信号
    progress_signal = pyqtSignal(int)

    # 状态信号
    status_signal = pyqtSignal(str)

    # 完成信号
    finished_signal = pyqtSignal(bool)

    # 版本检查信号
    version_check_signal = pyqtSignal(dict)
    """ 下载进度信号 end
    -------------------------------------- """

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
            self.release_info = response.json()

            # 发送版本检查信号
            self.version_check_signal.emit(self.release_info)

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

                    # 发送状态信号
                    self.status_signal.emit(f"下载中... {progress}%")

            # 下载完成后替换文件
            if os.path.exists(self.save_path):
                os.remove(self.save_path)
            os.rename(temp_path, self.save_path)

            # 发送完成状态信号
            self.status_signal.emit("更新完成!")

            # 发送完成信号
            self.finished_signal.emit(True)

        except requests.exceptions.SSLError:
            self.status_signal.emit("下载失败，请检查网络")
            self.finished_signal.emit(False)
        except Exception as e:
            self.status_signal.emit(f"更新失败: {str(e)}")
            self.finished_signal.emit(False)
