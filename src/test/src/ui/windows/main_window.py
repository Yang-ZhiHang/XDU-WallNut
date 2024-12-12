"""
该模块用于实现主窗口
"""
import os
import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
try:
    # 导入项目根目录到 Python 路径
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "./../../"))
    )
    from core.configs.constants import COMMENTS_OPTIONS, OPTION_LABELS
    from core.configs.settings import Settings
    from core.loaders.style_loader import StyleLoader
    from core.loaders.web_loader import WebLoader
    from ui.widgets.console_widget import ConsoleOutput
    from ui.widgets.input_form_widget import InputForm
except ImportError as e:
    print("配置导入失败，请检查配置文件是否存在", e)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 加载组件
        self._load_component()

        # 应用组件
        self._apply_component()

    def _load_component(self):
        """初始化窗口基本属性及组件"""
        self.setWindowTitle(Settings.WINDOW_TITLE)

        # 设置窗口大小
        self.resize(*Settings.WINDOW_SIZE)

        # 创建中心部件并创建主布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # 输入表单
        self.input_form_choices = InputForm("是否评教选择题：", OPTION_LABELS)
        self.input_form_text = InputForm("是否评教文本框：", COMMENTS_OPTIONS)

        # 样式
        self.style_loader = StyleLoader("base.qss")

        # 控制台输出
        self.console_output = ConsoleOutput()

        # 浏览器
        self.web_loader = WebLoader()

    def _apply_component(self):
        """应用所有初始化过的组件"""
        self.main_layout.addLayout(self.input_form_choices)
        self.main_layout.addLayout(self.input_form_text)
        self.main_layout.addWidget(self.console_output)
        self.setStyleSheet(self.style_loader.load_style())