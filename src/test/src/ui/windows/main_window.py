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
    from core.configs.settings import Settings
    # from core.log.logger import logger
    from ui.widgets.input_form import InputForm
    from core.configs.constants import COMMENTS_OPTIONS, OPTION_LABELS
    from core.loaders.style_loader import StyleLoader
except ImportError as e:
    # logger.error("配置导入失败，请检查配置文件是否存在", e)
    print("配置导入失败，请检查配置文件是否存在", e)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_window()

    def init_window(self):
        """
        初始化窗口基本属性
        """
        self.setWindowTitle(Settings.WINDOW_TITLE)

        # 设置窗口大小
        self.resize(*Settings.WINDOW_SIZE)

        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建主布局
        self.main_layout = QVBoxLayout(self.central_widget)

        # 创建输入表单
        self.input_form_choices = InputForm("是否评教选择题：", OPTION_LABELS)
        self.input_form_text = InputForm("是否评教文本框：", COMMENTS_OPTIONS)
        self.main_layout.addLayout(self.input_form_choices)
        self.main_layout.addLayout(self.input_form_text)

        # 加载样式
        style_loader = StyleLoader("base.qss")
        self.setStyleSheet(style_loader.load_style())
