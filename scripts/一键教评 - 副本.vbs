Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "https://ehall.xidian.edu.cn/jwapp/sys/wspjyyapp/*default/index.do"
WScript.Sleep 1000
msgbox "����������ѡ����档",,"ָ��"
WScript.Sleep 6000

dim option_num
option_num = inputbox("������ѡ����ĸ�����","����ȷ��")

multiLineText = "������Ҫѡ���ѡ�1-4����" & vbCrLf & _ 
"1. ��һ��ѡ��" & vbCrLf & _ 
"2. �ڶ���ѡ��" & vbCrLf & _ 
"3. ������ѡ��" & vbCrLf & _ 
"4. ���ĸ�ѡ��"
dim option_select
option_select = inputbox(multiLineText,"ѡ��ѡ��")

dim have_textarea
have_textarea = inputbox("�������Ƿ���Ҫ�ı������루��/��","ȷ��")

If have_textarea = "��" Then
	
dim textarea_num
textarea_num = inputbox("�������ı���ĸ�����","����ȷ��")

dim content
content = inputbox("�븴��Ҫͳһ������ı������а��У�","�ı���")

End If

msgbox "׼�������𣡵�� ȷ�� ����������ҳ����λ�ã�3���ű����Զ�����",,"׼����������Ԥ��10���깤��"

WScript.Sleep 3000


' -----ѡ���ⲿ��-----
dim i

For i = 1 To option_num

' ��ת����һ��ѡ��
WshShell.SendKeys "{TAB}"

' ͨ�����·���ģ��ѡ���ѡ��
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

WScript.Sleep 50 ' ���ʱ��

Next


' -----�ı��򲿷�-----

If have_textarea = "��" Then

For i = 1 To textarea_num

' ��ת����һ��ѡ��
WshShell.SendKeys "{TAB}"

' ���»س�����ģ����
WshShell.SendKeys "^v" 

WScript.Sleep 50 ' ���ʱ��

Next

End If

