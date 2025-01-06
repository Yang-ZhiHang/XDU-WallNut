from PyQt5.QtWidgets import QVBoxLayout, QLabel, QRadioButton, QButtonGroup

class SingleChoiceWidget(QVBoxLayout):
    """
    单选组件

    init:
        label_text: 标签文本
        options: 选项列表
    """
    def __init__(self, label_text, options):
        super().__init__()
        self._build_ui(label_text, options)
        self._setup_ui()

    def _build_ui(self, label_text, options):
        # 标签
        self.label_text = QLabel(label_text)

        # 按钮逻辑组
        self.option_buttons = []
        self.option_group = QButtonGroup()
        for option in options:
            button = QRadioButton(option)
            self.option_buttons.append(button)
            self.option_group.addButton(button)


    def _setup_ui(self):
        self.addWidget(self.label_text)
        for btn in self.option_buttons:
            self.addWidget(btn)


    def set_visible(self, is_visible):
        self.label_text.setVisible(is_visible)
        for btn in self.option_buttons:
            btn.setVisible(is_visible)


