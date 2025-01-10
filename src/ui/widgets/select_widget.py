"""
该模块用于定义选择题可复用组件
"""

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QRadioButton, QButtonGroup


class SelectWidget(QHBoxLayout):
    """
    选择题可复用组件，选项为 "是" 和 "否"

    init:
        label_text: 标签文本
        default_option: 默认选项，"yes" 或 "no"
    """

    def __init__(self, label_text, default_option):
        super().__init__()
        self._build_ui(label_text, default_option)
        self._setup_ui()

    def _build_ui(self, label_text, default_option):
        self.label_text = QLabel(label_text)
        self.select_yes = QRadioButton("是")
        self.select_no = QRadioButton("否")

        self._default_option = default_option

        self._select_group = QButtonGroup(self)
        self._select_group.addButton(self.select_yes)
        self._select_group.addButton(self.select_no)

        if self._default_option == "yes":
            self.select_yes.setChecked(True)
        else:
            self.select_no.setChecked(True)

    def _setup_ui(self):
        self.addWidget(self.label_text)
        self.addWidget(self.select_yes)
        self.addWidget(self.select_no)

    def get_selected_option(self):
        return self.select_yes.isChecked()
    
    def set_visible(self, is_visible):
        self.label_text.setVisible(is_visible)
        self.select_yes.setVisible(is_visible)
        self.select_no.setVisible(is_visible)
