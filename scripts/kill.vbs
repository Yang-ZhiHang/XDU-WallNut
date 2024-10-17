Set objShell = CreateObject("WScript.Shell")

' 定义要结束的进程名
strProcessName = "wscript.exe"

' 使用taskkill命令结束所有wscript.exe进程
objShell.Run "taskkill /IM " & Chr(34) & strProcessName & Chr(34) & " /F /T", 0, True

' 清理并退出
Set objShell = Nothing