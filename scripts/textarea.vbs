Set WshShell = CreateObject("WScript.Shell")

dim text
text = inputbox("������Ҫͳһ������ı���","����ȷ��")

dim epoch
epoch = inputbox("������Ҫ����Ĵ�����","ѭ������ȷ��")

msgbox "����Ϊ "+text+" ������ѭ�� "+ epoch +" �Σ���رձ�����, Ȼ�����ı�����ֹ�꣬5 ���ű����Զ�����",,"��ʾ"

WScript.Sleep 5000

dim i
For i = 1 To epoch
' ���»س�����ģ����
WshShell.SendKeys text 

' ��ת����һ��ѡ��
WshShell.SendKeys "{TAB}"

WScript.Sleep 50 ' ���ʱ��

Next

