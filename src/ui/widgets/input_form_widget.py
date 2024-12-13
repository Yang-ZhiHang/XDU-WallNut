from typing import List
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QLineEdit,
)


class InputForm(QVBoxLayout):
    def __init__(self, label_text: str, options: List[str], default_option: str = "yes"):
        super().__init__()
        self._init_components(label_text, options, default_option)
        self._setup_layout()
        self._connect_signals()

    def _init_components(self, label_text: str, options: List[str], default_option: str = "yes"):
        """
        初始化自动选择相关组件
        # -------------- 要实现的内容 start -------------
        # 布局的定义
        # 空行...
        # 组件的定义
        # 空行...
        # 将组件添加到布局中
        # -------------- 要实现的内容 end ---------------
        """

        # -------------- 是否需要自动教评 start --------------
        self._layout_choices_question = QHBoxLayout()

        # 标签
        self._label_whether = QLabel(label_text)
        # 按钮
        self._radio_need_option = QRadioButton("是")
        self._radio_not_need_option = QRadioButton("否")
        if default_option == "yes":
            self._radio_need_option.setChecked(True)
        else:
            self._radio_not_need_option.setChecked(True)
        self._choices_question_group = QButtonGroup(self)
        self._choices_question_group.addButton(self._radio_need_option)
        self._choices_question_group.addButton(self._radio_not_need_option)

        self._layout_choices_question.addWidget(self._label_whether)
        self._layout_choices_question.addWidget(self._radio_need_option)
        self._layout_choices_question.addWidget(self._radio_not_need_option)
        # -------------- 是否需要自动教评 end --------------

        # -------------- 题数量 start --------------
        self._layout_num_of_choices_question = QHBoxLayout()

        # 标签
        self._label_option_count = QLabel("选择题个数：")
        # 编辑框
        self._input_select_questions = QLineEdit()

        self._layout_num_of_choices_question.addWidget(self._label_option_count)
        self._layout_num_of_choices_question.addWidget(self._input_select_questions)
        # -------------- 题数量 end --------------

        # -------------- 选项相关组件 start --------------
        self._layout_choices_question_options = QVBoxLayout()

        # 标签
        self._label_which_option = QLabel("要批量选择的选项：")
        # 按钮
        self._option_buttons = []
        self._option_group = QButtonGroup()
        for label in options:
            button = QRadioButton(label)
            self._option_buttons.append(button)
            self._option_group.addButton(button)

        self._layout_choices_question_options.addWidget(self._label_which_option)
        for btn in self._option_buttons:
            self._layout_choices_question_options.addWidget(btn)
        # -------------- 选项相关组件 end --------------

    def _setup_layout(self):
        """添加所有子布局到主布局"""
        self.addLayout(self._layout_choices_question)
        self.addLayout(self._layout_num_of_choices_question)
        self.addLayout(self._layout_choices_question_options)

    def _connect_signals(self):
        """连接所有信号"""
        self._radio_need_option.toggled.connect(self.update_visibility)

    def update_visibility(self):
        """更新相关组件的可见性"""
        is_visible = self._radio_need_option.isChecked()
        self._input_select_questions.setVisible(is_visible)
        self._label_which_option.setVisible(is_visible)
        self._label_option_count.setVisible(is_visible)
        for button in self._option_buttons:
            button.setVisible(is_visible)

    def get_form_data(self):
        """获取表单数据"""
        return {
            "need_auto_select": self._radio_need_option.isChecked(),
            "select_questions_count": self._input_select_questions.text(),
            "selected_option": next(
                (
                    button.text()[-1]
                    for button in self._option_buttons
                    if button.isChecked()
                ),
                None,
            ),
        }
