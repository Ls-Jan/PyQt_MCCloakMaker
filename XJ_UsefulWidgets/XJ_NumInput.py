
__version__='1.0.0'
__author__='Ls_Jan'

import sys
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QFont,QTextCursor
from PyQt5.QtWidgets import QApplication

if(__package__):#如果是通过包导入该模块的话那么就用依赖导入
    from .XJ_TextEdit import *
else:
    from XJ_TextEdit import *

__all__=['XJ_NumInput']


class XJ_NumInput(XJ_TextEdit):#原本用的是QLineEdit，后来发现不好用(主要是因为不能加入富文本，没有setHtml函数，所以改用文本框
    valueChanged=pyqtSignal(int)#槽信号，值修改时发送信号
    def __init__(self,parent=None,valMin=0,valMax=100):
        super().__init__(parent)
        self.__curr=valMin#__curr是用来判断当前值有无发生修改的
        self.__textFormat=lambda num:str(num)
        self.__alignment=Qt.AlignCenter#对齐方式（默认居中
        self.setMouseTracking(True)#时刻捕捉鼠标移动
        self.setReadOnly(True)#设置只读
        self.OneLineMode(True)#单行模式
        self.SetValueRange(valMin,valMax)
#        self.setMaximumWidth(80)#设置宽度

    def focusOutEvent(self,event):#脱离焦点
        self.__LimitedValue()
        event.accept()    
    def mouseMoveEvent(self,event):
        if(self.isReadOnly()):
            self.viewport().setCursor(Qt.PointingHandCursor)#手型光标（不知道为什么，不能直接self.setCursor来设置光标，不管了反正能跑
        else:
            self.viewport().setCursor(Qt.IBeamCursor)#竖线光标
        event.accept()
    def mouseDoubleClickEvent(self,event):
        cursor=self.textCursor()#光标
        cursor.movePosition(QTextCursor.End)#光标移至文末
        self.setTextCursor(cursor)#设置光标

        self.setReadOnly(False)
        self.setPlainText(str(self.__curr))
        self.setAlignment(self.__alignment)#设置对齐
        event.accept()
    def wheelEvent(self,event):
        self.__LimitedValue()
        delta=event.angleDelta()
        self.SetValue(self.__curr+(1 if delta.y()>0 else -1))#滚轮向上滚动，增加
        event.accept()
    def keyPressEvent(self,event):
        self.setAlignment(self.__alignment)#设置对齐
        if(event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter):#按下回车键
            self.__LimitedValue()
        else:
            super().keyPressEvent(event)            
        event.accept()

    def SetMinimum(self,valMin):
        self.SetValueRange(valMin,self.__val_max)
    def SetMaximum(self,valMax):
        self.SetValueRange(self.__val_min,valMax)
    def SetValueRange(self,valMin,valMax):
        self.__val_min=valMin
        self.__val_max=valMax
        if(self.__val_max<self.__val_min):
            self.__val_max,self.__val_min=self.__val_min,self.__val_max
        self.SetValue(self.__curr)
    def SetValue(self,val):
        if(val<self.__val_min):
            val=self.__val_min
        if(val>self.__val_max):
            val=self.__val_max
        if(val!=self.__curr):
            self.__curr=val
            self.valueChanged.emit(val)
        self.__SetText()
        self.update()
    def SetTextFormat(self,textFormat=lambda num:str(num)):#设置文本格式化函数
        self.__textFormat=textFormat
        self.__SetText()
    def SetAlignment(self,alignment):#设置对齐方式
        self.__alignment=alignment
        self.__SetText()
    
    def GetValue(self):
        return self.__curr
    def GetValueRange(self):#返回取值范围
        return (self.__val_min,self.__val_max)


    def __SetText(self):
        self.setText(self.__textFormat(self.__curr))
        self.setAlignment(self.__alignment)#设置对齐
    def __LimitedValue(self):
        if(not self.isReadOnly()):
            self.setReadOnly(True)

            curr=''.join(list(filter(lambda c:c.isdigit() or c=='+' or c=='-',self.toPlainText()))).lstrip('0')
            curr=int(eval(curr)) if len(curr) else 0
            self.SetValue(curr)

        
if __name__=='__main__':
    app = QApplication(sys.argv)

    num=XJ_NumInput()
    num.show()
    
    num.SetValue(17)
    num.SetMaximum(200)
    num.valueChanged.connect(lambda i:print(num.GetValue()))
    num.SetTextFormat(lambda num:'{}'.format(round(num/100,2)).ljust(4,'0')+'s')
    num.SetTextFormat(lambda num:'10<sup><font color=#0088FF>{}</font><sup>'.format(num))

    sys.exit(app.exec())




