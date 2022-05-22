
__version__='1.0.0'
__author__='Ls_Jan'

import sys
from PyQt5.QtWidgets import QWidget,QTextEdit,QApplication
from PyQt5.QtGui import QTextCursor,QFont,QTextOption
from PyQt5.QtCore import Qt,pyqtSignal

__all__=['XJ_TextEdit']

class XJ_TextEdit(QTextEdit):
    textSent=pyqtSignal(str)#槽信号，当发送文本时发送信号
    #textChanged，为自带的槽信号，文本内容更改时触发
    def __init__(self,parent=None):
        super(XJ_TextEdit, self).__init__(parent)
        self.__oneLineMode=False
        self.__sendMsgMode=True
        self.setFont(QFont(self.font().family(),12))#简单设置下字体，初始字体的字号太小了
        self.__allowScale=False
        
    def OneLineMode(self,flag:bool):#单行模式，文本内容将只保留最后一行字串，并且窗口大小修改为单行大小，按回车将不会换行
        self.__oneLineMode=flag
        if(flag):#如果是单行模式那么就去设置下文本(多行文本将只留下最后一行
            self.__SetOneLineText()

        #对组件的模式策略进行设置
        height=self.__GetLineHeight()
        if(flag):#如果为单行模式，取消“自动换行”，并且把滚动条全隐藏
            self.setWordWrapMode(QTextOption.NoWrap)#设置换行模式为“不自动换行”
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)#隐藏行滚动条
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)#隐藏纵滚动条
            self.setMinimumHeight(height)
            self.setMaximumHeight(height)
        else:#多行模式则把“自动换行”恢复，并且显示滚动条
            self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)#设置换行模式为默认的“智能换行”
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)#显示行滚动条
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)#显示纵滚动条
            self.setMinimumHeight(height)
            self.setMaximumHeight(QApplication.desktop().screenGeometry().height())

    def keyPressEvent(self, event):#键盘某个键被按下时调用
        enter=(event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter)#回车键
        ctrl=event.modifiers()==Qt.ControlModifier#ctrl键

        if(enter):#按下回车键
            if(self.__sendMsgMode):#如果设置了信息发送模式
                if(self.__oneLineMode or ctrl):#单行模式按【回车】触发；多行模式按【ctrl+回车】触发
                    self.textSent.emit(self.toPlainText())#触发文本发送信号
                    self.setText("")#清除文本
            return
        if(self.__oneLineMode and ctrl and event.key()==Qt.Key_V):#如果是单行模式的话，在按下Ctrl+V进行文本粘贴时只会保留最后一行文本
            cursor = self.textCursor()#光标(为了插入文本
            data=QApplication.clipboard().mimeData()#剪切板内的数据
            if(data.hasHtml()):
                cursor.insertHtml(data.html())
            elif(data.hasText()):
                cursor.insertText(data.text())
            self.__SetOneLineText()#设置文本
            return
        super().keyPressEvent(event)#没有触发文本发送文本粘贴时该干啥干啥

    def Search(self,keyword):#搜索关键词，搜索成功将会高亮文本，并且返回True，否则返回False
        cursor = self.textCursor()#光标
        text=self.toPlainText()#文本内容
        L=text.find(keyword,cursor.position())#在光标位置作为起点开始寻找
        if(L==-1):
            L=text.find(keyword)#从头开始寻找
            if(L==-1):
                return False
        R=L+len(keyword)
        cursor.setPosition(L,QTextCursor.MoveAnchor)#移动光标
        cursor.setPosition(R,QTextCursor.KeepAnchor)#拖动光标
        self.setTextCursor(cursor)
        return True

    def wheelEvent(self, event):#重写滚轮事件
        if(self.__allowScale and event.modifiers()==Qt.ControlModifier):#允许缩放为真，并且按下了Ctrl键，则进行缩放
            self.zoomIn(1 if event.angleDelta().y()>0 else -1)#调用zoomIn进行缩放
            if(self.__oneLineMode):#如果是单行模式的话还得把控件高度调一下
                height=self.__GetLineHeight()
                self.setMinimumHeight(height)
                self.setMaximumHeight(height)
            return
        __wheel_V=self.verticalScrollBar()#纵滚动条
        __wheel_V.setValue(__wheel_V.value()-event.angleDelta().y())#因为默认的文本编辑框在只读模式下时按下Ctrl+滚轮是会缩放的，所以滚轮事件不能交给super().wheelEvent

    def AllowWheelScale(self,flag):#是否允许滚轮缩放。当该值为真时使用Ctrl+滚轮即可缩放
        self.__allowScale=flag
    def SendMsgMode(self,flag:bool):#文本发送模式，如果为真那么按下回车键(多行模式还得同时按下Ctrl)时将会清除文本内容并且触发textSent信号
        self.__sendMsgMode=flag
        
    def __GetLineHeight(self):#获取单行字串的最低高度
        return self.fontMetrics().lineSpacing()+10#10是魔法数字，非常恶意，是一点一点试出来的。不知道这个“10”是哪个参数设置的，一直没找到，而且在文本缩放非常极端的时候这个“10”的效果不会很好
    def __SetOneLineText(self):#设置单行文本（只保留最后一行的文本）
        text=self.toPlainText()
        sep=text.find('\n')+1#寻找回车符的后一个字符
        cursor = self.textCursor()#光标
        offset=len(text)-cursor.position()#距离文末的偏移量

        while(sep):
            if(self.__sendMsgMode):#如果可以发送文本
                self.textSent.emit(text[:sep])#连同回车符也一并发送
            text=text[sep:]#新行内容
            sep=text.find('\n')+1#寻找回车符的后一个字符
        self.setText(text)
        offset=len(text)-offset#距离文首的偏移量(此时文本仅一行
        if offset<0:
            offset=0
        cursor.setPosition(offset,QTextCursor.MoveAnchor)#移动光标
        self.setTextCursor(cursor)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)


    te=XJ_TextEdit()
    te.append('<font color="red" size=6> RRR </font>')#给文本加点料
    te.append("123456789\nABCDEFGHI\n123456789")
    te.append('<font color="green"> GGG </font>')
    te.append('<s>23333333</s>  <u>vvvvvvvvvv</u>')
    
    te.Search("456")#搜索文本
    te.Search("456")
    te.setFont(QFont('楷体',20))#设置字体
    te.SendMsgMode(True)#发送文本
    te.textSent.connect(lambda s:print("【文本发送】\n",s))#设置“发送文本”的回调函数
#    te.setReadOnly(True)#设置为只读
#    te.OneLineMode(True)#单行模式
    te.AllowWheelScale(True)#Ctrl+滚轮的文本缩放
    te.show()
    te.resize(700,400)


    sys.exit(app.exec())















