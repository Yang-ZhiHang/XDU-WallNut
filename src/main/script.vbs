Set WshShell = CreateObject("WScript.Shell")
' WshShell.Run "https://ehall.xidian.edu.cn/jwapp/sys/wspjyyapp/*default/index.do"
' WScript.Sleep 1000

dim have_option, have_textarea, option_num, option_select, textarea_num
Set objArgs = WScript.Arguments

' 获取是否需要自动评教选择题
have_option = objArgs(0)

' 获取是否需要自动评教文本框
have_textarea = objArgs(1)

' 如果需要自动评教选择题 且 不需要自动评教文本框
if have_option = 1 and have_textarea = 0 Then
    option_num = objArgs(2)
    option_select = objArgs(3)
End If

' 如果需要自动评教文本框 且 不需要自动评教选择题
If have_textarea = 1 and have_option = 0 Then
    textarea_num = objArgs(2)
End If

' 如果需要自动评教选择题 且 需要自动评教文本框
If have_option = 1 and have_textarea = 1 Then
    option_num = objArgs(2)
    option_select = objArgs(3)
    textarea_num = objArgs(4)
End If

msgbox "准备好了吗！点击 确定 后点击教评网页任意位置，3秒后脚本将自动运行",,"准备出发啦！预计10秒内完工！"

WScript.Sleep 3000


' -----选择题部分-----
dim i

If have_option = 1 Then

For i = 1 To option_num

' 跳转到下一个选项
WshShell.SendKeys "{TAB}"

' 通过上下方向模拟选项的选择
WshShell.SendKeys "{DOWN}" 

Select Case option_select
    Case 1
        WshShell.SendKeys "{UP}"
    Case 3
        WshShell.SendKeys "{DOWN}"
    Case 4
        WshShell.SendKeys "{UP}"
	WshShell.SendKeys "{UP}"
End Select

WScript.Sleep 50 ' 间隔时间

Next

End If


' -----文本框部分-----

If have_textarea = 1 Then

For i = 1 To textarea_num

' 跳转到下一个文本框
WshShell.SendKeys "{TAB}"

' 按下回车键，模拟点击
WshShell.SendKeys "^v" 

WScript.Sleep 50 ' 间隔时间

Next

End If

