import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QButtonGroup,
    QTextEdit,
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor
import random
import os
import subprocess
import webbrowser


class ConfigGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.start_button = None
        
        self.initUI()

        # 在初始化时打开网页
        self.open_website()

        # 开始按钮

    def open_website(self):
        url = "https://ehall.xidian.edu.cn/jwapp/sys/wspjyyapp/*default/index.do"

        browsers = [
            (
                "edge",
                "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            ),
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
                    self.console_output.append(f"使用 {browser_name} 打开网页成功")
                    return
                except Exception as e:
                    self.console_output.append(
                        f"尝试使用 {browser_name} 打开网页失败：{str(e)}"
                    )

        # 如果所有指定的浏览器都不可用，尝试使用系统默认浏览器
        try:
            webbrowser.open(url)
            self.console_output.append("使用系统默认浏览器打开网页")
        except Exception as e:
            self.console_output.append(f"无法打开网页：{str(e)}")

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle("脚本运行前参数设置")
        self.setGeometry(100, 100, 400, 400)

        # 一、是否需要自动教评选择题
        self.layout_auto_select = QHBoxLayout()
        self.radiobutton_need_option = QRadioButton("是")
        self.radiobutton_not_need_option = QRadioButton("否")
        self.radiobutton_need_option.setChecked(True)
        self.auto_select_group = QButtonGroup(self)
        self.auto_select_group.addButton(self.radiobutton_need_option)
        self.auto_select_group.addButton(self.radiobutton_not_need_option)
        self.layout_auto_select.addWidget(QLabel("是否需要自动教评选择题："))
        self.layout_auto_select.addWidget(self.radiobutton_need_option)
        self.layout_auto_select.addWidget(self.radiobutton_not_need_option)

        # 连接单选按钮的状态变化信号到槽函数
        self.radiobutton_need_option.toggled.connect(self.toggle_select_questions)
        self.radiobutton_not_need_option.toggled.connect(self.toggle_select_questions)

        # 二、选择题个数
        self.layout_number_of_select_questions = QHBoxLayout()
        self.label_number_of_select_questions = QLabel("选择题个数：")
        self.layout_number_of_select_questions.addWidget(
            self.label_number_of_select_questions
        )
        self.number_of_select_questions = QLineEdit()
        self.layout_number_of_select_questions.addWidget(
            self.number_of_select_questions
        )

        # 三、选择哪个选项
        self.layout_which_option = QVBoxLayout()
        self.label_which_option = QLabel("要批量选择的选项：")
        self.layout_which_option.addWidget(self.label_which_option)
        self.option_buttons = []
        self.option_group = QButtonGroup()
        for i in range(4):
            option_layout = QHBoxLayout()
            option_button = QRadioButton(f"选项 {chr(65+i)}")
            self.option_buttons.append(option_button)
            self.option_group.addButton(option_button)
            option_layout.addWidget(option_button)
            self.layout_which_option.addLayout(option_layout)

        # 四、是否需要文本框输入
        self.layout_auto_textbox = QHBoxLayout()
        self.layout_auto_textbox.addWidget(QLabel("是否需要文本框输入："))

        # 1. 创建选项
        self.radiobutton_need_textbox = QRadioButton("是")
        self.radiobutton_not_need_textbox = QRadioButton("否")
        self.radiobutton_not_need_textbox.setChecked(True)

        # 2. 创建选项逻辑组
        self.auto_textbox_group = QButtonGroup(self)
        self.auto_textbox_group.addButton(self.radiobutton_need_textbox)
        self.auto_textbox_group.addButton(self.radiobutton_not_need_textbox)

        # 3. 将组件添加到子布局当中
        self.layout_auto_textbox.addWidget(self.radiobutton_need_textbox)
        self.layout_auto_textbox.addWidget(self.radiobutton_not_need_textbox)

        # 连接单选按钮的状态变化信号到槽函数
        self.radiobutton_need_textbox.toggled.connect(self.toggle_textbox_count)
        self.radiobutton_not_need_textbox.toggled.connect(self.toggle_textbox_count)

        # 五、文本框个数
        self.layout_number_of_textboxes = QHBoxLayout()
        self.label_number_of_textboxes = QLabel("文本框个数：")
        self.layout_number_of_textboxes.addWidget(self.label_number_of_textboxes)
        self.number_of_textboxes = QLineEdit()
        self.layout_number_of_textboxes.addWidget(self.number_of_textboxes)

        # 六、评语选择
        self.layout_comments = QVBoxLayout()
        self.label_comments = QLabel("选择评语：")
        self.layout_comments.addWidget(self.label_comments)

        self.comment_buttons = []
        self.comment_group = QButtonGroup(self)
        comments = ["无", "很好", "还不错"]

        for comment in comments:
            comment_button = QRadioButton(comment)
            self.comment_buttons.append(comment_button)
            self.comment_group.addButton(comment_button)
            self.layout_comments.addWidget(comment_button)

        # 默认选中第一个评语
        self.comment_buttons[0].setChecked(True)

        # 七、控制台输出
        self.console_output = QTextEdit(self)
        self.console_output.setReadOnly(True)
        self.console_output.setPlaceholderText("控制台输出将显示在这里...")

        self.start_button = QPushButton("开始运行", self)
        self.start_button.clicked.connect(self.get_config)

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
        self.toggle_textbox_count()
        self.toggle_select_questions()

    def get_config(self):
        """
        获取配置
        """
        # 禁用开始按钮
        self.start_button.setEnabled(False)

        # 清空控制台并创建闪烁效果
        self.console_output.clear()
        QTimer.singleShot(100, self.show_config)  # 100毫秒后显示新内容

    def show_config(self):
        """
        显示配置
        """
        self.console_output.append("开始获取配置...")

        # 获取是否需要自动教评选择题
        self.need_auto_select = 1 if self.radiobutton_need_option.isChecked() else 0
        self.console_output.append(
            f"是否需要自动教评选择题：{'是' if self.need_auto_select == 1 else '否'}"
        )

        # 获取是否需要自动评教文本框输入
        self.need_auto_textbox = 1 if self.radiobutton_need_textbox.isChecked() else 0
        self.console_output.append(
            f"是否需要文本框输入：{'是' if self.need_auto_textbox == 1 else '否'}"
        )

        # 1. 如果两者都选择了否，直接输出运行结束
        if self.need_auto_select == 0 and self.need_auto_textbox == 0:
            self.console_output.append("\n运行结束")
            self.start_button.setEnabled(True)
            return

        # 2. 如果需要自动评教选择题，不需要自动评教文本框输入
        elif self.need_auto_select and not self.need_auto_textbox:

            # 获取选择题个数
            self.select_questions_count = self.number_of_select_questions.text()
            if self.select_questions_count:
                self.console_output.append(f"选择题个数：{self.select_questions_count}")

            # 获取选择的选项
            self.selected_option = 0
            for i, button in enumerate(self.option_buttons):
                if button.isChecked():
                    self.selected_option = i + 1
                    self.console_output.append(
                        f"选择的选项：{chr(64 + self.selected_option)}"
                    )
                    break

            # 如果有未选择的选项，不执行后续代码
            if (
                not self.number_of_select_questions.text()
                or not self.check_all_options_selected()
            ):
                self.console_output.append(
                    "警告: 请确保选择题个数已填写并确保所有选项都已选择!"
                )
                self.start_button.setEnabled(True)
                return

        # 3. 如果需要自动评教文本框输入，不需要自动评教选择题
        elif self.need_auto_textbox and not self.need_auto_select:

            # 获取文本框个数
            self.textbox_count = self.number_of_textboxes.text()
            if self.textbox_count:
                self.console_output.append(f"文本框个数：{self.textbox_count}")

            # 获取选择的评语
            self.selected_comment = ""
            for button in self.comment_buttons:
                if button.isChecked():
                    self.selected_comment = button.text()
                    self.console_output.append(f"选择的评语：{self.selected_comment}")
                    break

            # 如果有未选择的选项，不执行后续代码
            if not self.textbox_count or not any(
                button.isChecked() for button in self.comment_buttons
            ):
                self.console_output.append("警告: 请确保文本框个数已填写并选择评语!")
                self.start_button.setEnabled(True)
                return

            # 将 self.selected_comment 复制到剪切板
            if self.selected_comment:
                clipboard = QApplication.clipboard()
                clipboard.setText(self.selected_comment)
                self.console_output.append(
                    f"\n评语已复制到剪贴板：{self.selected_comment}"
                )

        # 4. 如果两者都需要
        elif self.need_auto_select and self.need_auto_textbox:

            # 获取选择题个数
            self.select_questions_count = self.number_of_select_questions.text()
            if self.select_questions_count:
                self.console_output.append(f"选择题个数：{self.select_questions_count}")

            # 获取选择的选项
            self.selected_option = 0
            for i, button in enumerate(self.option_buttons):
                if button.isChecked():
                    self.selected_option = i + 1
                    self.console_output.append(
                        f"选择的选项：{chr(64 + self.selected_option)}"
                    )
                    break

            # 获取文本框个数
            self.textbox_count = self.number_of_textboxes.text()
            if self.textbox_count:
                self.console_output.append(f"文本框个数：{self.textbox_count}")

            # 获取选择的评语
            self.selected_comment = ""
            for button in self.comment_buttons:
                if button.isChecked():
                    self.selected_comment = button.text()
                    self.console_output.append(f"选择的评语：{self.selected_comment}")
                    break

            # 如果有未选择的选项，不执行后续代码
            if (
                not self.number_of_select_questions.text()
                or not self.check_all_options_selected()
                or not self.textbox_count
                or not any(button.isChecked() for button in self.comment_buttons)
            ):
                self.console_output.append(
                    "警告: 请确保所有选项都已选择或文本框都已填写!"
                )
                self.start_button.setEnabled(True)
                return

            # 将 self.selected_comment 复制到剪切板
            if self.selected_comment:
                clipboard = QApplication.clipboard()
                clipboard.setText(self.selected_comment)
                self.console_output.append(
                    f"\n评语已复制到剪贴板：{self.selected_comment}"
                )

        # 执行初始化
        self.singal_output()

    def singal_output(self):
        """
        初始化信号
        """
        QTimer.singleShot(1000, lambda: None)
        self.console_output.append("\n开始初始化...\n")
        self.progress = 0
        self.progress_line = self.console_output.textCursor().position()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)  # 每50毫秒更新一次进度

    def update_progress(self):
        """
        更新进度
        """
        if self.progress < 94:
            self.progress += random.randint(1, 5)
        cursor = self.console_output.textCursor()
        cursor.setPosition(self.progress_line)
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(f"初始化进度：{self.progress}%")
        self.console_output.setTextCursor(cursor)

        if self.progress >= 94:
            self.progress = 100
            self.timer.stop()
            QTimer.singleShot(1000, lambda: None)
            self.done_singal()

    def done_singal(self):
        """
        初始化完成
        """
        self.console_output.append("初始化完成！")
        QTimer.singleShot(1000, self.execute_script)

    def execute_script(self):
        """
        执行脚本
        """
        self.console_output.append("\n正在启动脚本...")

        try:
            # 执行根目录下的 exe
            config_params = self.get_config_params()
            exe_path = os.path.join(os.getcwd(), "script.exe")
            result = subprocess.run(
                [exe_path] + config_params, capture_output=True, text=True
            )

            if result.returncode == 0:
                self.console_output.append("\n脚本执行成功！")
                self.console_output.append(result.stdout)
                self.start_button.setEnabled(True)
            else:
                self.console_output.append("\n脚本执行失败")
                self.console_output.append(result.stderr)
        except Exception as e:
            self.console_output.append(f"\n执行脚本时发生错误：{str(e)}")
            self.start_button.setEnabled(True)

    def get_config_params(self):
        """
        获取配置参数
        """
        params = []
        params.append(str(self.need_auto_select))
        params.append(str(self.need_auto_textbox))

        # 是否需要自动教评选择题
        if self.need_auto_select:
            params.append(self.select_questions_count)
            params.append(str(self.selected_option))

        # 是否需要自动评教文本框输入
        if self.need_auto_textbox:
            params.append(self.textbox_count)
            params.append(self.selected_comment)

        return params

    def check_all_options_selected(self):
        """
        检查是否选择了所有选项
        """
        if not (
            self.radiobutton_need_option.isChecked()
            or self.radiobutton_not_need_option.isChecked()
        ):
            return False

        # 检查选择题个数是否填写
        if not self.number_of_select_questions.text():
            return False

        # 检查是否选择了选项
        if not any(button.isChecked() for button in self.option_buttons):
            return False

        # 检查是否需要文本框输入
        if not (
            self.radiobutton_need_textbox.isChecked()
            or self.radiobutton_not_need_textbox.isChecked()
        ):
            return False

        # 如果需要文本框输入,检查文本框个数是否填写
        if (
            self.radiobutton_need_textbox.isChecked()
            and not self.number_of_textboxes.text()
        ):
            return False

        # 如果需要文本框输入,检查是否选择了评语
        if self.radiobutton_need_textbox.isChecked() and not any(
            button.isChecked() for button in self.comment_buttons
        ):
            return False

        return True

    def toggle_select_questions(self):
        """
        根据是否需要自动教评选择题来显示或隐藏选择题个数和选项组件
        """
        need_select = self.radiobutton_need_option.isChecked()
        self.number_of_select_questions.setVisible(need_select)
        self.label_number_of_select_questions.setVisible(need_select)
        self.label_which_option.setVisible(need_select)
        for button in self.option_buttons:
            button.setVisible(need_select)

    def toggle_textbox_count(self):
        """
        根据是否需要文本框输入来显示或隐藏文本框个数组件和评语组件
        """
        self.need_auto_textbox = self.radiobutton_need_textbox.isChecked()
        self.number_of_textboxes.setVisible(self.need_auto_textbox)
        self.label_number_of_textboxes.setVisible(self.need_auto_textbox)

        # 设置评语组件的可见性
        self.label_comments.setVisible(self.need_auto_textbox)
        for button in self.comment_buttons:
            button.setVisible(self.need_auto_textbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ConfigGenerator()
    ex.show()
    sys.exit(app.exec_())
