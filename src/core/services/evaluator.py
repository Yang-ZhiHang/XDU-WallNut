"""
评教服务
"""

import keyboard


class Evaluator:

    @staticmethod
    def choices_script_start(num_of_choices: int, option: int | str):
        """
        选择题评教脚本

        Args:
            num_of_choices: 选择题数量
            option: 要选择的选项
        """
        key_actions = {1: ["space"], 2: ["right"], 3: ["right", "right"], 4: ["left"]}

        if option not in key_actions:
            return "选项错误"

        actions = key_actions[option]

        for _ in range(num_of_choices):
            keyboard.press_and_release("tab")
            for action in actions:
                keyboard.press_and_release(action)

    @staticmethod
    def text_script_start(num_of_text: int, text: str):
        """
        文本题评教脚本

        Args:
            num_of_text: 文本题数量
            text: 要输入的文本
        """
        for _ in range(num_of_text):
            keyboard.press_and_release("tab")
            keyboard.write(text)
