import sys
import os

from PyQt5.QtWidgets import QApplication

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    from ui.windows.main_window import MainWindow
    from utils.logger import Logger
    from core.configs.settings import Settings

    Settings.BASE_DIR = Settings.get_base_dir()
    Logger.info("main.py", "main", f"BASE_DIR: {Settings.BASE_DIR}")
except ImportError as e:
    Logger.error("main.py", "main", "ImportError: " + str(e))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.web_loader.open_website("https://ehall.xidian.edu.cn/jwapp/sys/wspjyyapp/*default/index.do", window.console_output)
    window.check_update()
    # window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
