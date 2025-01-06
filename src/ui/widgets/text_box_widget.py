from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QLabel


class TextBoxWidget(QHBoxLayout):
    """
    文本框组件

    init:
        label_text: 标签文本
    """

    def __init__(self, label_text):
        super().__init__()
        self._build_ui(label_text)
        self._setup_ui()

    def _build_ui(self, label_text):
        self.label_text = QLabel(label_text)
        self.textbox = QLineEdit()
        self.textbox.setFixedHeight(25)

    def _setup_ui(self):
        self.addWidget(self.label_text)
        self.addWidget(self.textbox)

    def set_visible(self, is_visible):
        self.label_text.setVisible(is_visible)
        self.textbox.setVisible(is_visible)
