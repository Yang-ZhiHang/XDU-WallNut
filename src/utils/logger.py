"""
该模块用于存放日志打印工具
"""

class Logger:

    @staticmethod
    def info(file_name, func_name, message, color="green"):
        if color == "green":
            print(f"\033[0;32m[{file_name}][{func_name}] {message}\033[0m")
        elif color == "yellow":
            print(f"\033[1;33m[{file_name}][{func_name}] {message}\033[0m")
        elif color == "red":
            print(f"\033[1;31m[{file_name}][{func_name}] {message}\033[0m")

    @staticmethod
    def error(file_name, func_name, message):
        print(f"\033[1;31m[{file_name}][{func_name}] {message}\033[0m")

