Set WshShell = CreateObject("WScript.Shell")

dim epoch

epoch = inputbox("������ѡ����ĸ�����","ѭ������ȷ��")

msgbox "������ѭ��"+ epoch +"�Σ���رձ�����, 5 ���ű����Զ�����",,"��ʾ"

WScript.Sleep 5000

' WshShell.SendKeys "{TAB}"

dim i
For i = 1 To epoch

' ��ת����һ��ѡ��
WshShell.SendKeys "{TAB}"

' ���»س�����ģ����
WshShell.SendKeys "{DOWN}" 
WshShell.SendKeys "{UP}"
WScript.Sleep 50 ' ���ʱ��

Next

