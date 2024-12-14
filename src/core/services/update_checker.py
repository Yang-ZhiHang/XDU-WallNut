"""
该模块用于实现更新检查器
"""

import sys
import os
import json
import requests

try:
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "./../../"))
    )
    from utils.logger import Logger
    from core.configs.settings import Settings
except ImportError as e:
    Logger.error("update_checker.py", "update_checker", "ImportError: " + str(e))


class UpdateChecker:
    def __init__(self):
        self._version_info = {
            "current_version": None,
            "latest_version": None,
            "download_url": None,
            "release_notes": None,
            "release_date": None,
            "release_url": None,
        }
        self.error_message = ""

        self._load_current_version()
        self._get_latest_version()

    def check_update(self):
        """
        检查更新
        Returns:
            bool: 是否需要更新
            str: 错误信息
        """
        if self.version_info["current_version"] == "0.0.0":
            return False, "当前版本获取失败"

        if self.version_info["current_version"] != self.version_info["latest_version"]:
            Logger.info(
                "update_checker.py",
                "check_update",
                f"{self.version_info['current_version']} -> {self.version_info['latest_version']}",
            )
            return True, "有新版本可用: {} -> {}".format(
                self.version_info["current_version"],
                self.version_info["latest_version"],
            )
        return False, "当前版本已是最新版本: {}".format(
            self.version_info["current_version"]
        )

    def _get_latest_version(self):
        try:
            response = requests.get(Settings.GITHUB_API)
            data = response.json()

            self._version_info.update(
                {
                    "latest_version": data["tag_name"].replace(
                        "v", ""
                    ),  # 移除版本号前的'v'
                    "release_url": data["html_url"],
                    "author": data["author"]["login"],
                    "name": data["name"],
                    "published_at": data["published_at"],
                    "release_notes": data["body"],
                }
            )

            # 获取setup版本的下载链接
            for asset in data["assets"]:
                if "setup" in asset["name"].lower():
                    self._version_info["download_url"] = asset["browser_download_url"]
                    break

            # 保存到临时文件
            tmp_version_info = self._version_info.copy()
            tmp_version_info["version"] = tmp_version_info["latest_version"]
            tmp_version_info.pop("current_version")
            tmp_version_file_path = Settings.BASE_DIR + "/data/version.tmp"
            if not os.path.exists(Settings.BASE_DIR + "/data"):
                tmp_version_file_path = Settings.BASE_DIR + "/version.tmp"
            try:
                with open(tmp_version_file_path, "w", encoding="utf-8") as file:
                    json.dump(tmp_version_info, file, ensure_ascii=False, indent=4)
            except Exception as e:
                self.error_message = f"保存临时版本信息失败: {str(e)}"
                Logger.error(
                    "update_checker.py", "_get_latest_version", self.error_message
                )

        except Exception as e:
            self.error_message = f"获取最新版本信息失败: {str(e)}"
            Logger.error("update_checker.py", "_get_latest_version", self.error_message)
            self._version_info["latest_version"] = "0.0.0"

    def _load_current_version(self):
        version_file_path = Settings.BASE_DIR + "/data/version.json"
        if not os.path.exists(Settings.BASE_DIR + "/data"):
            # 获取程序路径
            if getattr(sys, "frozen", False):
                app_path = os.path.dirname(sys.executable)
            else:
                app_path = os.path.dirname(os.path.abspath(__file__))
            Logger.info(
                "update_checker.py", "_load_current_version", f"app_path: {app_path}"
            )
            version_file_path = Settings.BASE_DIR + "/version.json"
        try:
            with open(version_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self._version_info["current_version"] = data["version"]
        except Exception as e:
            self.error_message = f"读取当前版本信息失败: {str(e)}"
            Logger.error(
                "update_checker.py", "_load_current_version", self.error_message
            )
            self._version_info["current_version"] = "0.0.0"

    @property
    def version_info(self):
        return self._version_info
