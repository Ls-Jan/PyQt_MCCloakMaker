import sys
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


__all__=['XJ_NumInput']


class XJ_NumInput(QLineEdit):
    valueChanged=pyqtSignal(int)#槽信号，值修改时发送信号
    def __init__(self,parent=None,valMin=0,valMax=100):
        super(XJ_NumInput, self).__init__(parent)
        self.__curr=valMin#__curr是用来判断当前值有无发生修改的
        self.__prefix=""
        self.__postfix=""

        font=QFont()
        font.setBold(True)
        font.setPixelSize(20)

        self.setMouseTracking(True)#时刻捕捉鼠标移动
        self.setReadOnly(True)#设置只读
        self.setFont(font)#设置字体
        self.setAlignment(Qt.AlignCenter)#设置居中
        self.setMaximumWidth(80)

        self.Set_ValueRange(valMin,valMax)
        self.__SetText()

    def focusOutEvent(self,event):#脱离焦点
        curr=''.join(list(filter(lambda c:c.isdigit() or c=='+' or c=='-',self.text()))).lstrip('0')
        curr=int(eval(curr)) if len(curr) else 0
        self.__curr=curr
        self.__LimitValue()
        self.setReadOnly(True)
        event.accept()

    def mouseMoveEvent(self,event):
        self.setCursor(Qt.PointingHandCursor)#手型光标
        event.accept()

    def mouseDoubleClickEvent(self,event):
        self.setReadOnly(False)
        self.setFocus()
        self.setText(str(self.__curr))
        event.accept()

    def wheelEvent(self,event):
        delta=event.angleDelta()
        curr=self.__curr
        if(delta.y()>0):#滚轮向上滚动，增加
            if(curr<self.__val_max):
                curr=curr+1
        elif(delta.y()<0):#向下滚动，减少
            if(curr>self.__val_min):
                curr=curr-1
        self.update()
        event.accept()

        if(curr!=self.__curr):
            self.__curr=curr
            self.valueChanged.emit(curr)
        self.__SetText()


    def Set_Minimum(self,valMin):
        self.Set_ValueRange(valMin,self.__val_max)
    def Set_Maximum(self,valMax):
        self.Set_ValueRange(self.__val_min,valMax)
    def Set_ValueRange(self,valMin,valMax):
        self.__val_min=valMin
        self.__val_max=valMax
        if(self.__val_max<self.__val_min):
            self.__val_max,self.__val_min=self.__val_min,self.__val_max
        self.__LimitValue()
    def Set_Value(self,val):
        if(val<self.__val_min):
            val=self.__val_min
        if(val>self.__val_max):
            val=self.__val_max
        if(val!=self.__curr):
            self.__curr=val
            self.valueChanged.emit(val)
            self.__SetText()

    def Get_Value(self):
        return self.__curr
    def Get_ValueRange(self):#返回取值范围
        return (self.__val_min,self.__val_max)
    def SetPrefix(self,text):#设置前缀
        self.__prefix=text
        self.__SetText()
    def SetPostfix(self,text):#设置后缀
        self.__postfix=text
        self.__SetText()

    def __LimitValue(self):
        curr=self.__curr
        if(curr<self.__val_min):
            curr=self.__val_min
        if(curr>self.__val_max):
            curr=self.__val_max
        if(curr!=self.__curr):
            self.__curr=curr
            self.valueChanged.emit(curr)
            self.__SetText()

    def __SetText(self):
        self.setText(self.__prefix+str(self.__curr)+self.__postfix)


if __name__=='__main__':
    app = QApplication(sys.argv)

    tmp=XJ_NumInput()
    tmp.show()
    
    tmp.Set_Value(57)
    tmp.valueChanged.connect(lambda i:print(tmp.Get_Value()))
    tmp.SetPrefix("(16x10)*")
    sys.exit(app.exec())




