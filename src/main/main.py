import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from utils.browser_utils import open_website
from utils.config_handler import ConfigHandler
from ui.base_window import BaseWindow
from ui.components.progress_handler import ProgressHandler
from utils.style_handler import StyleManager
import ctypes

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

from utils.version_checker import VersionChecker
from utils.updater import Updater


class XDUScript(BaseWindow):
    def __init__(self):
        super().__init__()

        # 初始化配置处理器
        self.config_handler = ConfigHandler(self)

        # 初始化进度处理器
        self.progress_handler = ProgressHandler(self)

        # 连接开始按钮的点击事件，获取用户配置数据，并执行vbs脚本
        self.start_button.clicked.connect(self.config_handler.get_config)

        # 样式处理器属性
        self.style_handler = None

        # 初始化版本检查器
        self.version_checker = VersionChecker(self)

    def check_updates(self):
        self.console_output.append("正在检查更新...")
        has_new_version, latest_version = self.version_checker.check_for_updates()

        if has_new_version:
            self.console_output.append(f"发现新版本: {self.version_checker.current_version} -> {latest_version}")
            
            # 更新确认对话框
            reply = QMessageBox.question(
                self,
                '发现新版本',
                f'检测到新版本 {latest_version}，是否现在更新？',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                self.console_output.append("正在启动更新程序...")
                self.close()
                error = Updater.run_update("updater.exe")
                if error:
                    self.console_output.append(f"更新失败: {error}")
            else:
                self.console_output.append("用户取消更新")
        else:
            self.console_output.append(f"当前已是最新版本: {latest_version}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = XDUScript()

    # 加载样式
    ex.style_handler = StyleManager(ex, app)
    ex.style_handler.apply_styles()

    ex.console_output.append("XDU 启动！")

    ex.show()

    # 检查更新
    ex.check_updates()

    # 检测完成后打开网页
    open_website(
        "https://ehall.xidian.edu.cn/jwapp/sys/wspjyyapp/*default/index.do",
        ex.console_output,
    )

    sys.exit(app.exec_())
