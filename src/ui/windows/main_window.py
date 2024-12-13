"""
该模块用于实现主窗口
"""

import os
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget

try:
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "./../../"))
    )
    from core.configs.constants import COMMENTS_OPTIONS, OPTION_LABELS
    from core.configs.settings import Settings
    from core.icons import Icon
    from core.loaders.style_loader import StyleLoader
    from core.loaders.web_loader import WebLoader
    from ui.widgets.console_widget import ConsoleOutput
    from ui.widgets.input_form_widget import InputForm
    from ui.widgets.start_button_widget import StartButton
    from utils.logger import Logger
    from ui.dialogs.message_dialog import MessageDialog
    import resources.resources_rc
except ImportError as e:
    Logger.error("main_window.py", "main_window", "ImportError: " + str(e), color="red")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle(Settings.WINDOW_TITLE)

        # 设置窗口大小
        self.resize(*Settings.WINDOW_SIZE)

        # 加载组件
        self._load_component()

        # 应用组件
        self._apply_component()


    def _load_component(self):
        """初始化组件"""

        # 创建中心部件并创建主布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # 添加标签页组件
        self.tab_widget = QTabWidget()
        self.normal_tab = QWidget()
        self.enhanced_tab = QWidget()
        self.normal_layout = QVBoxLayout(self.normal_tab)
        self.enhanced_layout = QVBoxLayout(self.enhanced_tab)

        self._app_icon = QIcon(Icon.logo_ico_path)
        self.input_form_choices = InputForm("是否评教选择题：", OPTION_LABELS, default_option="yes")
        self.input_form_text = InputForm("是否评教文本框：", COMMENTS_OPTIONS, default_option="no")
        self.style_loader = StyleLoader("base.qss")
        self.web_loader = WebLoader()
        self.start_button = StartButton()
        self.console_output = ConsoleOutput()

    def _apply_component(self):
        """应用所有初始化过的组件"""
        self.setWindowIcon(self._app_icon)
        
        # 设置标签页
        self.tab_widget.addTab(self.normal_tab, "普通模式")
        self.tab_widget.addTab(self.enhanced_tab, "增强模式")
        self.main_layout.addWidget(self.tab_widget)

        # 将现有组件添加到普通模式标签页
        self.normal_layout.addLayout(self.input_form_choices)
        self.normal_layout.addLayout(self.input_form_text)
        self.input_form_choices.update_visibility()
        self.input_form_text.update_visibility()
        self.start_button.started.connect(self._script_start)
        self.start_button.stopped.connect(self._script_stop)
        self.normal_layout.addWidget(self.start_button)
        self.normal_layout.addWidget(self.console_output)

        # 应用样式
        self.setStyleSheet(self.style_loader.load_style())

    def _script_start(self):
        """脚本开始"""
        self.console_output.append("开始一键评教...")
        MessageDialog.show_info("提示", "请进入一键评教界面，点击空白处开始执行脚本")

    def _script_stop(self):
        """脚本停止"""
        self.console_output.append("停止一键评教...")
