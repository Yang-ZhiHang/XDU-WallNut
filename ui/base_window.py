from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout
)
from PyQt5.QtGui import QIcon
import sys
import os
sys.path.append('utils')

from utils.style_loader import load_stylesheet
from ui.components.input_section import InputSection

class BaseWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化组件
        self.initUI()
        
    def initUI(self):

        # 设置窗口大小
        self.setGeometry(100, 100, 400, 400)

        # 设置窗口标题
        self.setWindowTitle("XDU一键评教")

        # 设置窗口图标（不生效）
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = "./"
        ret_path = os.path.join(base_path, "favicon.ico")
        self.setWindowIcon(QIcon(ret_path)) 

        
        
        # 加载样式表
        style = load_stylesheet()
        if style:
            self.setStyleSheet(style)

        # 初始化组件
        self.input_section = InputSection(self)
        self.input_section.init_layout_auto_select()
        self.input_section.init_layout_number_of_select_questions()
        self.input_section.init_layout_which_option()
        self.input_section.init_layout_auto_textbox()
        self.input_section.init_layout_number_of_textboxes()
        self.input_section.init_layout_comments()
        self.input_section.init_start_button()
        self.input_section.init_console_output()

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

        # 初始化时调用一次，设置正确的初始状态
        self.input_section.toggle_textbox_count()
        self.input_section.toggle_select_questions()
    