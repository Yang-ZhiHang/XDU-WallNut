import requests
import json
import os
import subprocess
from typing import Tuple
from requests.exceptions import SSLError


class VersionChecker:
    def __init__(self, window):

        # 窗口对象
        self.window = window

        self.current_version = self._get_current_version()
        self.latest_version = None

        # 请求更新信息的 URL
        self.update_url = (
            "https://api.github.com/repos/Yang-ZhiHang/XDU-WallNut/releases/latest"
        )

    def _get_current_version(self) -> str:
        """
        获取当前版本
        """

        try:
            # 读取 version.json 文件，获取当前版本号
            with open("version.json", "r", encoding="utf-8") as f:
                version_info = json.load(f)
            return version_info.get("version")
        except FileNotFoundError:
            self.window.console_output.append("version.json 文件不存在")
            return "0.0.0"

    def check_for_updates(self) -> Tuple[bool, str]:
        """
        检查更新
        returns:
            Tuple[bool, str]: 是否需要更新，最新版本号
        """
        try:
            # 请求更新
            response = requests.get(self.update_url)
            if response.status_code == 200:

                # 获取最新版本信息
                release_info = response.json()

                # 获取最新版本号
                self.latest_version = release_info["tag_name"].replace("v", "")

                # 比较版本
                return self._compare_versions(), self.latest_version
            
            elif response.status_code == 404:
                self.window.console_output.append("更新信息获取失败.")
                return False, self.current_version
            elif response.status_code == 403:
                self.window.console_output.append("API 请求被拒绝.")
                return False, self.current_version
            else:
                self.window.console_output.append(f"检查更新时出错: {response.text}")
                return False, self.current_version
                
        except SSLError:
            self.window.console_output.append(f"网络连接失败，请检查网络设置.")
            return False, self.current_version
        except Exception as e:
            self.window.console_output.append(f"检查更新时出错: {str(e)}")
            return False, self.current_version

    def _compare_versions(self) -> bool:
        """
        比较版本
        """
        current = [int(x) for x in self.current_version.split(".")]
        latest = [int(x) for x in self.latest_version.split(".")]
        return latest > current
