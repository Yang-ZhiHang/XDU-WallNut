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

from ui.widgets.text_box_widget import TextBoxWidget
from core.services.user_setting import UserSettings


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
    from ui.widgets.experiment_form_widget import ExperimentForm
    from ui.widgets.final_form_widget import FinalForm
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

        self.check_update()
        self.check_settings()

    def _set_main_layout(self):
        """
        设置布局框架

        中心布局 -> 标签页:
            - 实验评教布局
            - 期末评教布局
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
        self.tab_widget.addTab(self.normal_tab, "实验评教")
        self.tab_widget.addTab(self.enhanced_tab, "期末评教")
        self.tab_widget.addTab(self.setting_tab, "设置")

    def _load_components(self):

        self.console_output = ConsoleOutput()
        self.web_loader = WebLoader()
        self.user_settings = UserSettings()

        # ------------------------------- 实验评教 start
        self.forms_normal_mode = []
        self.forms_normal_mode.append(
            ExperimentForm(
                "是否评教选择题：",
                OPTION_LABELS,
                default_option="yes",
                form_type="choice",
            )
        )
        self.forms_normal_mode.append(
            ExperimentForm(
                "是否评教文本框：",
                COMMENTS_OPTIONS,
                default_option="no",
                form_type="text",
            )
        )
        # ------------------------------- 实验评教 end

        # ------------------------------- 期末评教 start
        # 添加滚动区域
        self.layout_enhanced = QVBoxLayout()
        self.enhanced_content = QWidget()
        self.enhanced_scroll = QScrollArea()
        self.enhanced_scroll.setWidgetResizable(True)
        self.enhanced_main_layout = QVBoxLayout()

        # 题目数量
        self.layout_num_of_question = TextBoxWidget("待评教的老师个数：")

        self.forms_enhanced_mode = []
        for i in range(10):
            self.forms_enhanced_mode.append(
                FinalForm(
                    f"评教项目 { i + 1 }：",
                    OPTION_LABELS,
                    default_option="yes",
                    form_type="choice",
                )
            )
        # ------------------------------- 期末评教 end

        # ------------------------------- 设置 start
        # 添加置顶复选框
        self.setting_widget = QWidget()
        self.setting_layout = QVBoxLayout()

        self.always_on_top = QCheckBox("窗口置顶")
        self.always_on_top.stateChanged.connect(self._toggle_always_on_top)

        # 添加自动打开网站选项
        self.auto_open_website = QCheckBox("下次自动打开网站")
        self.website_url = TextBoxWidget("网站链接：")

        # 从设置中加载状态
        self.auto_open_website.setChecked(
            self.user_settings.get("auto_open_website", False, self.console_output)
        )
        self.website_url.textbox.setText(self.user_settings.get("website_url", "", self.console_output))
        # ------------------------------- 设置 end

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.title_bar = TitleBarWidget(
            web_loader=self.web_loader, console_output=self.console_output
        )

        self._app_icon = QIcon(Icon.logo_ico_path)
        self.start_button = StartButton()

        self.style_loader = StyleLoader("base.qss")
        self.update_checker = UpdateChecker()

    def _set_component_style(self):
        self.setting_layout.setAlignment(Qt.AlignTop)  # 设置垂直居上对齐

    def _apply_components(self):

        # ------------------------------- 实验评教 start
        self.layout_normal.addLayout(self.forms_normal_mode[0])
        self.layout_normal.addLayout(self.forms_normal_mode[1])
        self.forms_normal_mode[0].update_visibility()
        self.forms_normal_mode[1].update_visibility()

        # ------------------------------- 实验评教 end

        # ------------------------------- 期末评教 start
        self.layout_enhanced.addLayout(self.layout_num_of_question)
        self.enhanced_content.setLayout(self.layout_enhanced)
        self.enhanced_scroll.setWidget(self.enhanced_content)
        self.enhanced_main_layout.addWidget(self.enhanced_scroll)
        self.enhanced_tab.setLayout(self.enhanced_main_layout)

        for form in self.forms_enhanced_mode:
            self.layout_enhanced.addLayout(form)
            form.update_visibility()
        # ------------------------------- 期末评教 end

        # ------------------------------- 设置 start
        self.setting_layout.addWidget(self.always_on_top)
        self.setting_layout.addWidget(self.auto_open_website)
        self.setting_layout.addLayout(self.website_url)
        self.setting_tab.setLayout(self.setting_layout)
        self.auto_open_website.stateChanged.connect(self._toggle_website_input)
        self.website_url.textbox.textChanged.connect(self._save_website_url)
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

        # 判断当前页是实验评教还是期末评教
        current_tab = self.tab_widget.currentWidget()
        if current_tab == self.normal_tab:
            self.console_output.append("当前模式: 实验评教")
        elif current_tab == self.enhanced_tab:
            self.console_output.append("当前模式: 期末评教")
        else:
            self.console_output.append("当前模式: 未知，拒绝启动")
            return

        MessageDialog.show_info(
            "提示", "请进入一键评教界面，在3秒内选择第一道题的第一个选择题"
        )

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
            question_num = self.layout_num_of_question.textbox.text()
            form_data = [
                form.get_form_data(question_num) for form in self.forms_enhanced_mode
            ]

        try:
            first_form = True
            for form in form_data:
                if form["active"]:
                    if form["type"] == "choice":
                        if first_form:
                            Evaluator.choices_script_start(
                                int(form["num_of_questions"]) - 1, form["option"]
                            )
                            first_form = False
                        else:
                            Evaluator.choices_script_start(
                                int(form["num_of_questions"]), form["option"]
                            )
                    elif form["type"] == "text":
                        if first_form:
                            Evaluator.text_script_start(
                                int(form["num_of_questions"]) - 1, form["text"]
                            )
                            first_form = False
                        else:
                            Evaluator.text_script_start(
                                int(form["num_of_questions"]), form["text"]
                            )
            self.console_output.append("脚本执行完毕...")
        except Exception as e:
            self.console_output.append(f"脚本执行失败: {e}")
            self.console_output.append("请检查输入的题目数量是否为纯数字")
            Logger.error("MainWindow", "_execute_script", f"脚本执行失败: {e}")
            MessageDialog.show_error("错误", f"请检查输入的题目数量是否为纯数字")

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
            Logger.info(
                "MainWindow",
                "check_update",
                f"Temporary file path is {tmp_version_file_path}.",
            )

            if not os.path.exists(tmp_version_file_path):
                tmp_version_file_path = os.path.join(app_path, "version.tmp")

            if os.path.exists(tmp_version_file_path):
                os.remove(tmp_version_file_path)
                Logger.info(
                    "MainWindow",
                    "check_update",
                    f"Temporary file {tmp_version_file_path} deleted successfully.",
                )
            else:
                Logger.info(
                    "MainWindow",
                    "check_update",
                    f"Temporary file {tmp_version_file_path} does not exist.",
                )

        # 处理更新逻辑
        if need_update and not self.update_checker.error_message:
            Logger.info(
                "MainWindow", "check_update", f"need_update: {need_update}, msg: {msg}"
            )

            if MessageDialog.show_update(
                "更新提示", self.update_checker.version_info, "更新", "取消"
            ):
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
            Logger.error(
                "MainWindow",
                "check_update",
                f"error_message: {self.update_checker.error_message}",
            )
            self.console_output.append(self.update_checker.error_message)
        else:
            # 无需更新
            remove_temp_file()
            Logger.error("MainWindow", "check_update", f"no need update, msg: {msg}")

    def check_settings(self):
        """检查设置"""
        # 在初始化完成后立即检查是否需要打开网页
        if self.user_settings.get("auto_open_website", False):
            url = self.user_settings.get("website_url", "")
            if url:
                self.web_loader.open_website(url, self.console_output)

    def _toggle_always_on_top(self, state):
        """切换窗口置顶状态"""
        if state == Qt.Checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)

        # 显示窗口以应用更改
        self.show()

    def _toggle_website_input(self, state):
        """保存自动打开网站状态"""
        is_checked = state == Qt.Checked
        self.user_settings.set("auto_open_website", is_checked)

    def _save_website_url(self):
        """保存网站链接"""
        self.user_settings.set("website_url", self.website_url.textbox.text())
