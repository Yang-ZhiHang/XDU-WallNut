"""
该模块用于处理样式相关操作
"""

import os
import sys


class StyleManager:
    def __init__(self, window, app):
        self.window = window
        self.app = app
        # 基准字体大小（类似于 rem 的基准值）
        self.base_font_size = 16
        self.update_scale_factor()

    def update_scale_factor(self):
        # 获取屏幕 DPI 缩放比例
        screen = self.app.primaryScreen()
        self.dpi_scale = screen.logicalDotsPerInch() / 96.0

        # 获取屏幕高度（类似于 vh）
        self.screen_height = screen.size().height()

        # 计算实际的基准大小
        self.scaled_base_size = self.base_font_size * self.dpi_scale

    def rem(self, value):
        """将 rem 值转换为实际像素值"""
        return int(value * self.scaled_base_size)

    def vh(self, value):
        """将 vh 值转换为实际像素值"""
        return int(self.screen_height * value / 100)

    def init_responsive_font_styles(self):
        # 生成响应式样式表
        style_sheet = f"""
        QLabel {{
            font-size: {self.rem(1)}px;  /* 1rem */
            min-height: {self.vh(3)}px;  /* 5vh */
        }}
        
        QPushButton {{
            font-size: {self.rem(0.875)}px;  /* 0.875rem */
            padding: {self.rem(0.5)}px {self.rem(1)}px;
        }}
        
        QTextEdit {{
            font-size: {self.rem(0.875)}px;
            min-height: {self.vh(10)}px;  /* 30vh */
        }}

        QRadioButton {{
            font-size: {self.rem(0.875)}px;
            min-height: {self.vh(3)}px;  /* 5vh */
        }}
        """
        return style_sheet

    def init_base_stylesheet(self):
        try:
            # 获取应用程序的基础路径
            if getattr(sys, "frozen", False):
                # 如果是打包后的可执行文件
                base_path = sys._MEIPASS
            else:
                # 如果是开发环境
                base_path = os.path.abspath(".")

            # 构建样式文件的完整路径
            style_file = os.path.join(base_path, "styles", "base.qss")

            with open(style_file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            self.window.console_output.append(f"样式表加载失败：{str(e)}")
            return ""

    def apply_styles(self):
        """合并并应用所有样式"""
        base_styles = self.init_base_stylesheet()
        responsive_styles = self.init_responsive_font_styles()
        combined_styles = base_styles + "\n" + responsive_styles
        self.window.setStyleSheet(combined_styles)
