"""
该模块用于浏览器相关操作
"""

import os
import webbrowser
from typing import List, Tuple, Optional
from PyQt5.QtWidgets import QTextEdit

class WebLoader:
    def __init__(self):
        self.browsers: List[Tuple[str, str]] = [
            ("edge", "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"),
            ("firefox", "C:\\Program Files\\Mozilla Firefox\\firefox.exe"),
            ("360", "C:\\Program Files (x86)\\360\\360se6\\Application\\360se.exe"),
        ]
    
    def open_website(self, url: str, console_output: QTextEdit) -> None:
        """
        尝试使用可用的浏览器打开网页
        
        Args:
            url: 要打开的网页地址
            console_output: 用于输出信息的控制台
        """
        if result := self._get_available_browser(console_output):
            browser, browser_name = result
            try:
                browser.open(url)
                console_output.append(f"使用 {browser_name}浏览器 打开网页成功")
                return
            except Exception as e:
                console_output.append(f"尝试使用 {browser_name}浏览器 打开网页失败：{str(e)}")
        
        self._try_default_browser(url, console_output)
    
    def _get_available_browser(self, console_output: QTextEdit) -> Optional[Tuple[webbrowser.BaseBrowser, str]]:
        """获取第一个可用的浏览器"""
        for browser_name, browser_path in self.browsers:
            if os.path.exists(browser_path):
                try:
                    webbrowser.register(
                        browser_name, None, webbrowser.BackgroundBrowser(browser_path)
                    )
                    return webbrowser.get(browser_name), browser_name
                except Exception:
                    continue
        return None
    
    def _try_default_browser(self, url: str, console_output: QTextEdit) -> None:
        """尝试使用系统默认浏览器"""
        try:
            webbrowser.open(url)
            console_output.append("使用系统默认浏览器打开网页")
        except Exception as e:
            console_output.append(f"无法打开网页：{str(e)}")