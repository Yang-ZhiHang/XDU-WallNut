Set WshShell = CreateObject("WScript.Shell")

dim text
text = inputbox("请输入要统一输入的文本：","内容确定")

dim epoch
epoch = inputbox("请输入要输入的次数：","循环次数确定")

msgbox "内容为 "+text+" 本程序将循环 "+ epoch +" 次，请关闭本窗口, 然后点击文本框出现光标，5 秒后脚本将自动运行",,"提示"

WScript.Sleep 5000

dim i
For i = 1 To epoch
' 按下回车键，模拟点击
WshShell.SendKeys text 

' 跳转到下一个选项
WshShell.SendKeys "{TAB}"

WScript.Sleep 50 ' 间隔时间

Next

