"""
该模块用于实现控制类按钮(开始/停止)
"""

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal

class StartButton(QPushButton):
    # 定义信号
    started = pyqtSignal()  # 开始信号
    stopped = pyqtSignal()  # 停止信号
    
    def __init__(self):
        super().__init__()
        self._running = False
        self._init_ui()
        
    def _init_ui(self):
        self.setText("开始")
        self.setMinimumWidth(80)  # 设置最小宽度
        self.clicked.connect(self._on_click)
        
    def _on_click(self):
        """点击按钮时，切换按钮状态"""
        if not self._running:
            self.setText("停止")
            self._running = True
            self.started.emit()
        else:
            self.setText("开始")
            self._running = False
            self.stopped.emit()
            
    def reset(self):
        """重置按钮状态"""
        self._running = False
        self.setText("开始")

    
