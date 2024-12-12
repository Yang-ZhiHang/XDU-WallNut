import sys
import os

from PyQt5.QtWidgets import QApplication

try:
    # 导入项目根目录到 Python 路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    from ui.windows.main_window import MainWindow
except ImportError as e:
    print("路径导入失败:", e)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.web_loader.open_website("https://ehall.xidian.edu.cn/jwapp/sys/wspjyyapp/*default/index.do", window.console_output)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()