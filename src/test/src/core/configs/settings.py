"""
该文件用于存放全局配置
"""
class Settings:
    # 窗口相关
    WINDOW_TITLE = "XDU一键评教"
    WINDOW_SIZE = (800, 600)
    
    # INPUT表单相关
    INPUT_SETTINGS = {
        'choice_question': {
            'title': '是否需要自动教评选择题',
            'options': ['是', '否'],
            'default': '是'
        },
        'text_filling': {
            'title': '是否需要文本框输入',
            'options': ['是', '否'],
            'default': '否'
        }
    }
    
    # 评语
    COMMENT_OPTIONS = ['无', '很好', '还不错']