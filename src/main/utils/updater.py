import subprocess
import os
import sys
from typing import Optional

class Updater:
    @staticmethod
    def run_update(updater_path: str) -> Optional[str]:
        try:
            # 检查更新程序是否存在
            if not os.path.exists(updater_path):
                return "更新程序不存在"
                
            # 使用子进程运行更新程序
            subprocess.Popen([updater_path], 
                           creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            
            # 退出当前程序
            sys.exit(0)
            
        except Exception as e:
            return f"启动更新程序失败: {str(e)}"