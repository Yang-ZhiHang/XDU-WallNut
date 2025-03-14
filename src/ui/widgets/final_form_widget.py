"""
该模块用于定义期末评教表单组件
"""

from typing import List
from PyQt5.QtWidgets import QVBoxLayout

from ui.widgets.select_widget import SelectWidget
from ui.widgets.single_choice_widget import SingleChoiceWidget

try:
    from utils.logger import Logger
except ImportError as e:
    Logger.error(
        "input_form_widget.py", "InputForm", "ImportError: " + str(e), color="red"
    )


class FinalForm(QVBoxLayout):
    def __init__(
        self,
        label_text: str,
        options: List[str],
        default_option: str = "yes",
        form_type: str = "choice",
    ):
        """
        输入表单组件

        Args:
            label_text: 标签文本
            options: 选项列表
            default_option: 默认选项
            form_type: 表单类型
        """
        super().__init__()
        self._init_components(label_text, options, default_option)
        self._setup_layout()
        self._connect_signals()

    def _init_components(
        self, label_text: str, options: List[str], default_option: str = "yes"
    ):
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

        # 选择组件：用于选择是否需要自动教评
        self._select_widget = SelectWidget(label_text, default_option)

        # 单选组件：用于选择要批量选择的选项
        self._layout_question_options = SingleChoiceWidget(
            "要批量选择的选项：", options
        )

    def _setup_layout(self):
        """添加所有子布局到主布局"""
        self.addLayout(self._select_widget)
        self.addLayout(self._layout_question_options)

    def _connect_signals(self):
        """连接所有信号"""
        self._select_widget.select_yes.toggled.connect(self.update_visibility)

    def update_visibility(self):
        """更新相关组件的可见性"""
        is_visible = self._select_widget.select_yes.isChecked()
        self._layout_question_options.set_visible(is_visible)

    def get_form_data(self, num_of_questions: int):
        """获取表单数据"""
        if self._select_widget.select_yes.isChecked():
            form_data = {
                "type": "choice",
                "active": True,
                "num_of_questions": num_of_questions,
                "option": next(
                    (
                        i + 1
                        for i, button in enumerate(
                            self._layout_question_options.option_buttons
                        )
                        if button.isChecked()
                    ),
                    0,
                ),
            }
        else:
            form_data = {
                "type": "choice",
                "active": False,
                "num_of_questions": 0,
                "option": None,
            }
        # Logger.info("InputForm", "get_form_data", f"表单数据: {form_data}")
        return form_data
