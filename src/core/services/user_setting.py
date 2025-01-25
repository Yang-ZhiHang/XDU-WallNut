"""
该模块用于保存用户设置
"""

from typing import Dict, Any
import json
import os
from PyQt5.QtWidgets import QTextEdit
from utils.logger import Logger
from core.configs.settings import Settings


class UserSettings:
    _instance = None
    _settings_file = os.path.join(Settings.BASE_DIR, "data", "settings.json")
    _default_settings = {
        "auto_open_website": True,
        "website_url": "https://ehall.xidian.edu.cn/jwapp/sys/wspjyyapp/*default/index.do#/xspj",
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._settings = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        """加载设置"""
        try:
            if not os.path.exists(os.path.dirname(self._settings_file)):
                os.makedirs(os.path.dirname(self._settings_file))

            if os.path.exists(self._settings_file):
                with open(self._settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return self._default_settings.copy()
        except Exception as e:
            Logger.error("UserSettings", "_load_settings", f"加载设置失败: {str(e)}")
            return self._default_settings.copy()

    def save_settings(self):
        """保存设置"""
        try:
            with open(self._settings_file, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, ensure_ascii=False, indent=4)
            Logger.success("UserSettings", "save_settings", "设置保存成功")
        except Exception as e:
            Logger.error("UserSettings", "save_settings", f"保存设置失败: {str(e)}")

    def get(
        self, key: str, default: Any = None, console_output: QTextEdit = None
    ) -> Any:
        """获取设置值"""
        value = self._settings.get(key, default)
        if console_output:
            console_output.append(f"获取设置值: {key} = {value}")
        return value

    def set(self, key: str, value: Any):
        """设置值"""
        self._settings[key] = value
        self.save_settings()
