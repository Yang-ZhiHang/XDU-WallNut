from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

class ConfigHandler:
    def __init__(self, window):
        self.window = window
    
    def check_all_options_selected(self):
        """
        检查是否选择了所有选项
        """
        if not (
            self.window.radiobutton_need_option.isChecked()
            or self.window.radiobutton_not_need_option.isChecked()
        ):
            return False

        # 检查选择题个数是否填写
        if not self.window.number_of_select_questions.text():
            return False

        # 检查是否选择了选项
        if not any(button.isChecked() for button in self.window.option_buttons):
            return False

        # 检查是否需要文本框输入
        if not (
            self.window.radiobutton_need_textbox.isChecked()
            or self.window.radiobutton_not_need_textbox.isChecked()
        ):
            return False

        # 如果需要文本框输入,检查文本框个数是否填写
        if (
            self.window.radiobutton_need_textbox.isChecked()
            and not self.window.number_of_textboxes.text()
        ):
            return False

        # 如果需要文本框输入,检查是否选择了评语
        if self.window.radiobutton_need_textbox.isChecked() and not any(
            button.isChecked() for button in self.window.comment_buttons
        ):
            return False

        return True

    def show_config(self):
        """
        显示配置
        """
        self.window.console_output.append("开始获取配置...")

        # 获取是否需要自动教评选择题
        self.window.need_auto_select = 1 if self.window.radiobutton_need_option.isChecked() else 0
        self.window.console_output.append(
            f"是否需要自动教评选择题：{'是' if self.window.need_auto_select == 1 else '否'}"
        )

        # 取是否需要自动评教文本框输入
        self.window.need_auto_textbox = 1 if self.window.radiobutton_need_textbox.isChecked() else 0
        self.window.console_output.append(
            f"是否需要文本框输入：{'是' if self.window.need_auto_textbox == 1 else '否'}"
        )

        # 1. 如果两者都选择了否，直接输出运行结束
        if self.window.need_auto_select == 0 and self.window.need_auto_textbox == 0:
            self.window.console_output.append("\n运行结束")
            self.window.start_button.setEnabled(True)
            return

        # 2. 如果需要自动评教选择题，不需要自动评教文本框输入
        elif self.window.need_auto_select and not self.window.need_auto_textbox:

            # 获取选择题个数
            self.window.select_questions_count = self.window.number_of_select_questions.text()
            if self.window.select_questions_count:
                self.window.console_output.append(f"选择题个数：{self.window.select_questions_count}")

            # 获取选择的选项
            self.window.selected_option = 0
            for i, button in enumerate(self.window.option_buttons):
                if button.isChecked():
                    self.window.selected_option = i + 1
                    self.window.console_output.append(
                        f"选择的选项：{chr(64 + self.window.selected_option)}"
                    )
                    break

            # 如果有未选择的选项，不执行后续代码
            if (
                not self.window.number_of_select_questions.text()
                or not self.check_all_options_selected()
            ):
                self.window.console_output.append(
                    "警告: 请确保选择题个数已填写并确保所有选项都已选择!"
                )
                self.window.start_button.setEnabled(True)
                return

        # 3. 如果需要自动评教文本框输入，不需要自动评教择题
        elif self.window.need_auto_textbox and not self.window.need_auto_select:

            # 获取文本框个数
            self.window.textbox_count = self.window.number_of_textboxes.text()
            if self.window.textbox_count:
                self.window.console_output.append(f"文本框个数：{self.window.textbox_count}")

            # 获取选择的评语
            self.window.selected_comment = ""
            for button in self.window.comment_buttons:
                if button.isChecked():
                    self.window.selected_comment = button.text()
                    self.window.console_output.append(f"选择的评语：{self.window.selected_comment}")
                    break

            # 如果有未选择的选项，不执行后续代码
            if not self.window.textbox_count or not any(
                button.isChecked() for button in self.window.comment_buttons
            ):
                self.window.console_output.append("警告: 请确保文本框个数已填写并选择评语!")
                self.window.start_button.setEnabled(True)
                return

            # 将 self.selected_comment 复制到剪切板
            if self.window.selected_comment:
                clipboard = QApplication.clipboard()
                clipboard.setText(self.window.selected_comment)
                self.window.console_output.append(
                    f"\n评语已复制到剪贴板：{self.window.selected_comment}"
                )

        # 4. 如果两者都需要
        elif self.window.need_auto_select and self.window.need_auto_textbox:

            # 获取选择题个数
            self.window.select_questions_count = self.window.number_of_select_questions.text()
            if self.window.select_questions_count:
                self.window.console_output.append(f"选择题个数：{self.window.select_questions_count}")

            # 获取选择的选项
            self.window.selected_option = 0
            for i, button in enumerate(self.window.option_buttons):
                if button.isChecked():
                    self.window.selected_option = i + 1
                    self.window.console_output.append(
                        f"选择的选项：{chr(64 + self.window.selected_option)}"
                    )
                    break

            # 获取文本框个数
            self.window.textbox_count = self.window.number_of_textboxes.text()
            if self.window.textbox_count:
                self.window.console_output.append(f"文本框个数：{self.window.textbox_count}")

            # 获取选择的评语
            self.window.selected_comment = ""
            for button in self.window.comment_buttons:
                if button.isChecked():
                    self.window.selected_comment = button.text()
                    self.window.console_output.append(f"选择的评语：{self.window.selected_comment}")
                    break

            # 如果有未选择的选项，不执行后续代码
            if (
                not self.window.number_of_select_questions.text()
                or not self.check_all_options_selected()
                or not self.window.textbox_count
                or not any(button.isChecked() for button in self.window.comment_buttons)
            ):
                self.window.console_output.append(
                    "警告: 请确保所有选项都已选择或文本框都已填写!"
                )
                self.window.start_button.setEnabled(True)
                return

            # 将 self.selected_comment 复制到剪切板
            if self.window.selected_comment:
                clipboard = QApplication.clipboard()
                clipboard.setText(self.window.selected_comment)
                self.window.console_output.append(
                    f"\n评语已复制到剪贴板：{self.window.selected_comment}"
                )

        # 执行初始化
        self.window.progress_handler.singal_output()

    def get_config(self):
        """
        获取配置
        """
        # 禁用开始按钮
        self.window.start_button.setEnabled(False)

        # 清空控制台并创建闪烁效果
        self.window.console_output.clear()
        QTimer.singleShot(100, self.show_config)  # 100毫秒后显示新内容

    def get_config_params(self):
        """
        获取配置参数
        """
        params = []
        params.append(str(self.window.need_auto_select))
        params.append(str(self.window.need_auto_textbox))

        if self.window.need_auto_select:
            params.append(self.window.select_questions_count)
            params.append(str(self.window.selected_option))

        if self.window.need_auto_textbox:
            params.append(self.window.textbox_count)

        return params