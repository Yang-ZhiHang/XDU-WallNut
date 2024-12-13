"""
更新检查器
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
        self._current_version = None
        self._latest_version_info = {
            "version": None,
            "download_url": None,
            "release_notes": None,
            "release_date": None,
            "release_url": None
        }
        self.error_message = "No error occurred."
        
        self._load_current_version()
        self._get_latest_version()

    def check_update(self):
        """
        检查更新
        Returns:
            bool: 是否需要更新
            str: 错误信息
        """
        if self._current_version != self._latest_version_info["version"]:
            return True, self.error_message
        return False, self.error_message

    def _get_latest_version(self):
        """获取最新版本信息"""
        try:
            response = requests.get(Settings.UPDATE_URL)
            data = response.json()
            
            self._latest_version_info.update({
                "version": data["tag_name"].replace("v", ""),  # 移除版本号前的'v'
                "release_url": data["html_url"],
                "release_date": data["published_at"],
                "release_notes": data["body"]
            })
            
            # 获取setup版本的下载链接
            for asset in data["assets"]:
                if "setup" in asset["name"].lower():
                    self._latest_version_info["download_url"] = asset["browser_download_url"]
                    break
                    
        except Exception as e:
            self.error_message = f"获取最新版本信息失败: {str(e)}"
            Logger.error("update_checker.py", "_get_latest_version", self.error_message)
            self._latest_version_info["version"] = "0.0.0"

    def _load_current_version(self):
        """加载当前版本信息"""
        try:
            with open("data/version.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self._current_version = data["version"]
        except Exception as e:
            self.error_message = f"读取当前版本信息失败: {str(e)}"
            Logger.error("update_checker.py", "_load_current_version", self.error_message)
            self._current_version = "0.0.0"

    def update_version_file(self):
        """更新版本文件"""
        try:
            with open("data/version.json", "w", encoding="utf-8") as file:
                json.dump(self._latest_version_info, file, ensure_ascii=False, indent=4)
                
            Logger.info("update_checker.py", "update_version_file", "版本文件更新成功")
            return True
            
        except Exception as e:
            self.error_message = f"更新版本文件失败: {str(e)}"
            Logger.error("update_checker.py", "update_version_file", self.error_message)
            return False

    @property
    def version_info(self):
        """获取版本信息"""
        return self._latest_version_info

    @property
    def current_version(self):
        """获取当前版本"""
        return self._current_version


