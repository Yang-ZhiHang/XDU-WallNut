import sys
import os

from PyQt5.QtWidgets import QApplication
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    from ui.windows.main_window import MainWindow
    from utils.logger import Logger
except ImportError as e:
    Logger.error("main.py", "main", "ImportError: " + str(e), color="red")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.web_loader.open_website("https://ehall.xidian.edu.cn/jwapp/sys/wspjyyapp/*default/index.do", window.console_output)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()