Set WshShell = CreateObject("WScript.Shell")

dim epoch

epoch = inputbox("请输入选择题的个数：","循环次数确定")

msgbox "本程序将循环"+ epoch +"次，请关闭本窗口, 5 秒后脚本将自动运行",,"提示"

WScript.Sleep 5000

' WshShell.SendKeys "{TAB}"

dim i
For i = 1 To epoch

' 跳转到下一个选项
WshShell.SendKeys "{TAB}"

' 按下回车键，模拟点击
WshShell.SendKeys "{DOWN}" 
WshShell.SendKeys "{UP}"
WScript.Sleep 50 ' 间隔时间

Next

