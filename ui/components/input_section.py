from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QLineEdit,
    QPushButton,
    QTextEdit,
)

class InputSection(QVBoxLayout):
    def __init__(self, window):
        super().__init__()
        self.window = window
    
    def init_layout_auto_select(self):
        """
        初始化是否需要自动教评选择题
        """
        self.window.radiobutton_need_option = QRadioButton("是")
        self.window.radiobutton_not_need_option = QRadioButton("否")
        self.window.radiobutton_need_option.setChecked(True)
        self.window.auto_select_group = QButtonGroup(self)
        self.window.auto_select_group.addButton(self.window.radiobutton_need_option)
        self.window.auto_select_group.addButton(self.window.radiobutton_not_need_option)
        self.window.layout_auto_select = QHBoxLayout()
        self.window.layout_auto_select.addWidget(QLabel("是否需要自动教评选择题："))
        self.window.layout_auto_select.addWidget(self.window.radiobutton_need_option)
        self.window.layout_auto_select.addWidget(self.window.radiobutton_not_need_option)

        # 连接单选按钮的状态变化信号到槽函数
        self.window.radiobutton_need_option.toggled.connect(self.toggle_select_questions)
        self.window.radiobutton_not_need_option.toggled.connect(self.toggle_select_questions)
    
    def toggle_select_questions(self):
        """
        根据是否需要自动教评选择题来显示或隐藏选择题个数和选项组件
        """
        need_select = self.window.radiobutton_need_option.isChecked()
        self.window.number_of_select_questions.setVisible(need_select)
        self.window.label_number_of_select_questions.setVisible(need_select)
        self.window.label_which_option.setVisible(need_select)
        for button in self.window.option_buttons:
            button.setVisible(need_select)

    def toggle_textbox_count(self):
        """
        根据是否需要文本框输入来显示或隐藏文本框个数组件和评语组件
        """
        self.window.need_auto_textbox = self.window.radiobutton_need_textbox.isChecked()
        self.window.number_of_textboxes.setVisible(self.window.need_auto_textbox)
        self.window.label_number_of_textboxes.setVisible(self.window.need_auto_textbox)

        # 设置评语组件的可见性
        self.window.label_comments.setVisible(self.window.need_auto_textbox)
        for button in self.window.comment_buttons:
            button.setVisible(self.window.need_auto_textbox)

    def init_layout_number_of_select_questions(self):
        """
        初始化选择题个数
        """

        # 选择题个数
        self.window.layout_number_of_select_questions = QHBoxLayout()
        self.window.label_number_of_select_questions = QLabel("选择题个数：")
        self.window.layout_number_of_select_questions.addWidget(
            self.window.label_number_of_select_questions
        )
        self.window.number_of_select_questions = QLineEdit()
        self.window.layout_number_of_select_questions.addWidget(
            self.window.number_of_select_questions
        )
        return self.window.layout_number_of_select_questions

    def init_layout_which_option(self):
        """
        选择哪个选项
        """
        self.window.layout_which_option = QVBoxLayout()
        self.window.label_which_option = QLabel("要批量选择的选项：")
        self.window.layout_which_option.addWidget(self.window.label_which_option)
        self.window.option_buttons = []
        self.window.option_group = QButtonGroup()
        for i in range(4):
            option_layout = QHBoxLayout()
            option_button = QRadioButton(f"选项 {chr(65+i)}")
            self.window.option_buttons.append(option_button)
            self.window.option_group.addButton(option_button)
            option_layout.addWidget(option_button)
            self.window.layout_which_option.addLayout(option_layout)
        return self.window.layout_which_option

    def init_layout_auto_textbox(self):

        # 是否需要文本框输入
        self.window.layout_auto_textbox = QHBoxLayout()
        self.window.layout_auto_textbox.addWidget(QLabel("是否需要文本框输入："))

        # 创建选项
        self.window.radiobutton_need_textbox = QRadioButton("是")
        self.window.radiobutton_not_need_textbox = QRadioButton("否")
        self.window.radiobutton_not_need_textbox.setChecked(True)

        # 创建选项逻辑组
        self.window.auto_textbox_group = QButtonGroup(self)
        self.window.auto_textbox_group.addButton(self.window.radiobutton_need_textbox)
        self.window.auto_textbox_group.addButton(self.window.radiobutton_not_need_textbox)

        # 将组件添加到子布局当中
        self.window.layout_auto_textbox.addWidget(self.window.radiobutton_need_textbox)
        self.window.layout_auto_textbox.addWidget(self.window.radiobutton_not_need_textbox)

        # 连接单选按钮的状态变化信号到槽函数
        self.window.radiobutton_need_textbox.toggled.connect(self.toggle_textbox_count)
        self.window.radiobutton_not_need_textbox.toggled.connect(self.toggle_textbox_count)


    def init_layout_number_of_textboxes(self):
        """
        文本框个数
        """
        self.window.layout_number_of_textboxes = QHBoxLayout()
        self.window.label_number_of_textboxes = QLabel("文本框个数：")
        self.window.layout_number_of_textboxes.addWidget(self.window.label_number_of_textboxes)
        self.window.number_of_textboxes = QLineEdit()
        self.window.layout_number_of_textboxes.addWidget(self.window.number_of_textboxes)


    def init_layout_comments(self):
        """
        评语选择
        """
        self.window.layout_comments = QVBoxLayout()
        self.window.label_comments = QLabel("选择评语：")
        self.window.layout_comments.addWidget(self.window.label_comments)

        self.window.comment_buttons = []
        self.window.comment_group = QButtonGroup(self)
        comments = ["无", "很好", "还不错"]

        for comment in comments:
            comment_button = QRadioButton(comment)
            self.window.comment_buttons.append(comment_button)
            self.window.comment_group.addButton(comment_button)
            self.window.layout_comments.addWidget(comment_button)

        # 默认选中第一个评语
        self.window.comment_buttons[0].setChecked(True)


    def init_start_button(self):
        """
        开始运行按钮
        """
        self.window.start_button = QPushButton("开始运行", self.window)

    def init_console_output(self):
        """
        控制台输出
        """
        self.window.console_output = QTextEdit(self.window)
        self.window.console_output.setReadOnly(True)
        self.window.console_output.setPlaceholderText("控制台输出将显示在这里...")
        return self.window.console_output
