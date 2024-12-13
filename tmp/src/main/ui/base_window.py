"""
该模块用于处理主窗口相关操作
"""

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout
)
from PyQt5.QtGui import QIcon
import sys
import os
sys.path.append('utils')

from ui.components.input_section import InputSection
from ui.components.console_section import ConsoleSection

class BaseWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化组件
        self.initUI()
        
    def initUI(self):

        # 设置窗口大小
        self.setGeometry(100, 100, 600, 400)

        # 设置窗口标题
        self.setWindowTitle(f"XDU一键评教")

        # 设置窗口图标（不生效）
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = "./"
        ret_path = os.path.join(base_path, "favicon.ico")
        self.setWindowIcon(QIcon(ret_path)) 

        # 初始化组件
        self.input_section = InputSection(self)
        self.input_section.init_layout_auto_select()
        self.input_section.init_layout_number_of_select_questions()
        self.input_section.init_layout_which_option()
        self.input_section.init_layout_auto_textbox()
        self.input_section.init_layout_number_of_textboxes()
        self.input_section.init_layout_comments()
        self.input_section.init_start_button()

        # 初始化控制台输出组件
        self.console_section = ConsoleSection(self)
        self.console_section.init_console_output()

        # 创建全局布局
        global_layout = QVBoxLayout()

        # 将子布局添加到全局布局当中
        global_layout.addLayout(self.layout_auto_select)
        global_layout.addLayout(self.layout_number_of_select_questions)
        global_layout.addLayout(self.layout_which_option)
        global_layout.addLayout(self.layout_auto_textbox)
        global_layout.addLayout(self.layout_number_of_textboxes)
        global_layout.addLayout(self.layout_comments)
        global_layout.addWidget(self.start_button)
        global_layout.addWidget(self.console_output)

        # 将全局布局设置为窗口的布局
        self.setLayout(global_layout)

        # 初始化时调用一次对不必要显示的组件进行隐藏，设置正确的初始状态
        self.input_section.toggle_textbox_count()
        self.input_section.toggle_select_questions()
    