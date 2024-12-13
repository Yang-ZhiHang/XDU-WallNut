import sys
from PyQt5.QtWidgets import QApplication
from updater_window import UpdaterWindow

def main():
    """
    更新程序的主程序
    """

    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 创建更新窗口实例
    window = UpdaterWindow()

    # 显示主窗口
    window.show()

    # 开始更新
    window.start_update()
    
    # 程序结束
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()