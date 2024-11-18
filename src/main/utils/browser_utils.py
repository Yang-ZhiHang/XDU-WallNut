"""
该模块用于浏览器相关操作
"""

import os
import webbrowser

def open_website(url, console_output):
    browsers = [
        ("edge", "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"),
        ("firefox", "C:\\Program Files\\Mozilla Firefox\\firefox.exe"),
        ("360", "C:\\Program Files (x86)\\360\\360se6\\Application\\360se.exe"),
    ]

    for browser_name, browser_path in browsers:
        if os.path.exists(browser_path):
            try:
                webbrowser.register(
                    browser_name, None, webbrowser.BackgroundBrowser(browser_path)
                )
                webbrowser.get(browser_name).open(url)
                console_output.append(f"使用 {browser_name} 打开网页成功")
                return
            except Exception as e:
                console_output.append(f"尝试使用 {browser_name} 打开网页失败：{str(e)}")

    try:
        webbrowser.open(url)
        console_output.append("使用系统默认浏览器打开网页")
    except Exception as e:
        console_output.append(f"无法打开网页：{str(e)}")