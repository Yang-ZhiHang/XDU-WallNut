"""
该模块用于实现主窗口
"""

import os
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QScrollArea,
    QCheckBox,
)
from PyQt5.QtCore import Qt, QTimer


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
    from ui.dialogs.message_dialog import MessageDialog
    from ui.widgets.title_bar_widget import TitleBarWidget
    from utils.logger import Logger
    from core.services.evaluator import Evaluator
    from core.services.update_checker import UpdateChecker
    from utils.file import get_app_path
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
        self.setWindowFlags(Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._set_main_layout()
        self._load_components()
        self._set_component_style()
        self._apply_components()

    def _set_main_layout(self):
        """
        设置布局框架

        中心布局 -> 标签页:
            - 普通模式布局
            - 增强模式布局
        """

        # 创建中心部件和主布局(中心部件包含主布局)
        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()

        # 创建分页
        self.tab_widget = QTabWidget()
        self.normal_tab = QWidget()
        self.enhanced_tab = QWidget()
        self.setting_tab = QWidget()

        self.layout_normal = QVBoxLayout(self.normal_tab)

        # 设置分页
        self.tab_widget.addTab(self.normal_tab, "普通模式")
        self.tab_widget.addTab(self.enhanced_tab, "增强模式")
        self.tab_widget.addTab(self.setting_tab, "设置")

    def _load_components(self):
        # ------------------------------- 普通模式 start
        self.forms_normal_mode = []
        self.forms_normal_mode.append(
            InputForm(
                "是否评教选择题：",
                OPTION_LABELS,
                default_option="yes",
                form_type="choice",
            )
        )
        self.forms_normal_mode.append(
            InputForm(
                "是否评教文本框：",
                COMMENTS_OPTIONS,
                default_option="no",
                form_type="text",
            )
        )
        # ------------------------------- 普通模式 end

        # ------------------------------- 增强模式 start
        # 添加滚动区域
        self.layout_enhanced = QVBoxLayout()
        self.enhanced_content = QWidget()
        self.enhanced_scroll = QScrollArea()
        self.enhanced_scroll.setWidgetResizable(True)
        self.enhanced_main_layout = QVBoxLayout()

        self.forms_enhanced_mode = []
        for i in range(10):
            self.forms_enhanced_mode.append(
                InputForm(
                    f"评教项目 { i + 1 }：",
                    OPTION_LABELS,
                    default_option="yes",
                    form_type="choice",
                )
            )
        # ------------------------------- 增强模式 end

        # ------------------------------- 设置 start
        self.layout_setting = QVBoxLayout()
        
        # 添加置顶复选框
        self.setting_widget = QWidget()
        self.setting_layout = QVBoxLayout()
        
        self.always_on_top = QCheckBox("窗口置顶")
        self.always_on_top.stateChanged.connect(self._toggle_always_on_top)
        self.always_on_top.setChecked(True)
        # ------------------------------- 设置 end

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.web_loader = WebLoader()
        self.console_output = ConsoleOutput()
        self.title_bar = TitleBarWidget(web_loader=self.web_loader, console_output=self.console_output)

        self._app_icon = QIcon(Icon.logo_ico_path)
        self.start_button = StartButton()

        self.style_loader = StyleLoader("base.qss")
        self.update_checker = UpdateChecker()

    def _set_component_style(self):

        # -------------------------------------- 设置 start
        self.layout_setting.setAlignment(Qt.AlignCenter)  # 居中对齐
        # -------------------------------------- 设置 end

    def _apply_components(self):

        # ------------------------------- 普通模式 start
        self.layout_normal.addLayout(self.forms_normal_mode[0])
        self.layout_normal.addLayout(self.forms_normal_mode[1])
        self.forms_normal_mode[0].update_visibility()
        self.forms_normal_mode[1].update_visibility()

        # ------------------------------- 普通模式 end

        # ------------------------------- 增强模式 start
        self.enhanced_content.setLayout(self.layout_enhanced)
        self.enhanced_scroll.setWidget(self.enhanced_content)
        self.enhanced_main_layout.addWidget(self.enhanced_scroll)
        self.enhanced_tab.setLayout(self.enhanced_main_layout)
        for form in self.forms_enhanced_mode:
            self.layout_enhanced.addLayout(form)
            form.update_visibility()
        # ------------------------------- 增强模式 end

        # ------------------------------- 设置 start
        self.setting_layout.addWidget(self.always_on_top)
        self.setting_widget.setLayout(self.setting_layout)
        self.layout_setting.addWidget(self.setting_widget)
        self.setting_tab.setLayout(self.layout_setting)
        # ------------------------------- 设置 end

        self.setWindowIcon(self._app_icon)
        self.main_layout.addWidget(self.title_bar)
        self.title_bar.min_button.clicked.connect(self.showMinimized)
        self.title_bar.close_button.clicked.connect(self.close)
        self.main_layout.addWidget(self.tab_widget)
        self.main_layout.addWidget(self.start_button)
        self.start_button.started.connect(self._script_start)
        self.start_button.stopped.connect(self._script_stop)
        self.main_layout.addWidget(self.console_output)
        self.setStyleSheet(self.style_loader.load_style())
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def _script_start(self):
        """脚本开始"""

        # 判断当前页是普通模式还是增强模式
        current_tab = self.tab_widget.currentWidget()
        if current_tab == self.normal_tab:
            self.console_output.append("当前模式: 普通模式")
        elif current_tab == self.enhanced_tab:
            self.console_output.append("当前模式: 增强模式")
        else:
            self.console_output.append("当前模式: 未知，拒绝启动")
            return

        MessageDialog.show_info("提示", "请进入一键评教界面，点击空白处开始执行脚本")

        # 创建倒计时定时器
        self.countdown = 3
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_countdown)
        self.timer.start(1000)

    def _update_countdown(self):
        """更新倒计时"""
        self.console_output.append(f"倒计时: {self.countdown}s")
        self.countdown -= 1

        if self.countdown < 0:
            self.timer.stop()
            self.console_output.append("开始执行脚本...")
            self._execute_script()

    def _execute_script(self):
        """执行脚本逻辑"""

        # 获取表单数据
        if self.tab_widget.currentWidget() == self.normal_tab:
            form_data = [form.get_form_data() for form in self.forms_normal_mode]
        elif self.tab_widget.currentWidget() == self.enhanced_tab:
            form_data = [form.get_form_data() for form in self.forms_enhanced_mode]

        try:
            for form in form_data:
                if form["active"]:
                    if form["type"] == "choice":
                        Evaluator.choices_script_start(
                            int(form["num_of_questions"]), form["option"]
                        )
                    elif form["type"] == "text":
                        Evaluator.text_script_start(
                            int(form["num_of_questions"]), form["text"]
                        )
        except Exception as e:
            self.console_output.append(f"脚本执行失败: {e}")
            self.console_output.append("请检查输入的题目数量是否为纯数字")
            Logger.error("MainWindow", "_execute_script", f"脚本执行失败: {e}")

        self.console_output.append("脚本执行完毕...")
        self.start_button.reset()

    def _script_stop(self):
        """脚本停止"""
        self.console_output.append("停止一键评教...")

    def check_update(self):
        """检查更新"""
        need_update, msg = self.update_checker.check_update()
        self.console_output.append(msg)
        
        # 删除临时文件
        def remove_temp_file():
            app_path = get_app_path()
            tmp_version_file_path = os.path.join(app_path, "data/version.tmp")
            Logger.info("MainWindow", "check_update", f"Temporary file path is {tmp_version_file_path}.")
            
            if not os.path.exists(tmp_version_file_path):
                tmp_version_file_path = os.path.join(app_path, "version.tmp")
                
            if os.path.exists(tmp_version_file_path):
                os.remove(tmp_version_file_path)
                Logger.info("MainWindow", "check_update", f"Temporary file {tmp_version_file_path} deleted successfully.")
            else:
                Logger.info("MainWindow", "check_update", f"Temporary file {tmp_version_file_path} does not exist.")

        # 处理更新逻辑
        if need_update and not self.update_checker.error_message:
            Logger.info("MainWindow", "check_update", f"need_update: {need_update}, msg: {msg}")
            
            if MessageDialog.show_update("更新提示", self.update_checker.version_info, "更新", "取消"):
                # 启动更新程序
                updater_path = os.path.join(Settings.BASE_DIR, "updater.exe")
                if os.path.exists(updater_path):
                    os.startfile(updater_path)
                    sys.exit()
                else:
                    remove_temp_file()
                    self.console_output.append("更新程序不存在.")
                    self.show()
            else:
                remove_temp_file()
        elif need_update:
            # 有错误信息
            remove_temp_file()
            Logger.error("MainWindow", "check_update", f"error_message: {self.update_checker.error_message}")
            self.console_output.append(self.update_checker.error_message)
        else:
            # 无需更新
            remove_temp_file()
            Logger.error("MainWindow", "check_update", f"no need update, msg: {msg}")
        
        # 显示窗口
        self.show()

    def _toggle_always_on_top(self, state):
        if state == Qt.Checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()  # 重新显示窗口应用更改
