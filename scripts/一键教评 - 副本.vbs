Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "https://ehall.xidian.edu.cn/jwapp/sys/wspjyyapp/*default/index.do"
WScript.Sleep 1000
msgbox "请进入教评待选项界面。",,"指引"
WScript.Sleep 6000

dim option_num
option_num = inputbox("请输入选择题的个数：","数量确定")

multiLineText = "请输入要选择的选项（1-4）：" & vbCrLf & _ 
"1. 第一个选项" & vbCrLf & _ 
"2. 第二个选项" & vbCrLf & _ 
"3. 第三个选项" & vbCrLf & _ 
"4. 第四个选项"
dim option_select
option_select = inputbox(multiLineText,"选项选择")

dim have_textarea
have_textarea = inputbox("请输入是否需要文本框输入（是/否）","确认")

If have_textarea = "是" Then
	
dim textarea_num
textarea_num = inputbox("请输入文本框的个数：","数量确定")

dim content
content = inputbox("请复制要统一输入的文本到剪切板中：","文本框")

End If

msgbox "准备好了吗！点击 确定 后点击教评网页任意位置，3秒后脚本将自动运行",,"准备出发啦！预计10秒完工！"

WScript.Sleep 3000


' -----选择题部分-----
dim i

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


' -----文本框部分-----

If have_textarea = "是" Then

For i = 1 To textarea_num

' 跳转到下一个选项
WshShell.SendKeys "{TAB}"

' 按下回车键，模拟点击
WshShell.SendKeys "^v" 

WScript.Sleep 50 ' 间隔时间

Next

End If

