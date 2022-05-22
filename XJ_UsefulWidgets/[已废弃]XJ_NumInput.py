import sys
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication,QLineEdit


__all__=['XJ_NumInput']


class XJ_NumInput(QLineEdit):
    valueChanged=pyqtSignal(int)#槽信号，值修改时发送信号
    def __init__(self,parent=None,valMin=0,valMax=100):
        super(XJ_NumInput, self).__init__(parent)
        self.__curr=valMin#__curr是用来判断当前值有无发生修改的
        self.__textFormat=lambda num:str(num)

        font=QFont()
        font.setBold(True)
        font.setPixelSize(20)

        self.setMouseTracking(True)#时刻捕捉鼠标移动
        self.setReadOnly(True)#设置只读
        self.setFont(font)#设置字体
        self.setAlignment(Qt.AlignCenter)#设置居中

        self.Set_ValueRange(valMin,valMax)

    def focusOutEvent(self,event):#脱离焦点
        curr=''.join(list(filter(lambda c:c.isdigit() or c=='+' or c=='-',self.text()))).lstrip('0')
        curr=int(eval(curr)) if len(curr) else 0
        
        self.Set_Value(curr)
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
        self.Set_Value(self.__curr+(1 if delta.y()>0 else -1))#滚轮向上滚动，增加
        self.update()
        event.accept()


    def Set_Minimum(self,valMin):
        self.Set_ValueRange(valMin,self.__val_max)
    def Set_Maximum(self,valMax):
        self.Set_ValueRange(self.__val_min,valMax)
    def Set_ValueRange(self,valMin,valMax):
        self.__val_min=valMin
        self.__val_max=valMax
        if(self.__val_max<self.__val_min):
            self.__val_max,self.__val_min=self.__val_min,self.__val_max
        self.Set_Value(self.__curr)
    def Set_Value(self,val):
        if(val<self.__val_min):
            val=self.__val_min
        if(val>self.__val_max):
            val=self.__val_max
        if(val!=self.__curr):
            self.__curr=val
            self.valueChanged.emit(val)
            self.__SetText()
            self.update()
    def Set_TextFormat(self,textFormat=lambda num:str(num)):#设置文本格式化函数
        self.__textFormat=textFormat
        self.__SetText()

    def Get_Value(self):
        return self.__curr
    def Get_ValueRange(self):#返回取值范围
        return (self.__val_min,self.__val_max)

    def __SetText(self):
        self.setText(self.__textFormat(self.__curr))

        
if __name__=='__main__':
    app = QApplication(sys.argv)

    num=XJ_NumInput()
    num.show()
    
    num.Set_Value(17)
    num.Set_Maximum(200)
    num.valueChanged.connect(lambda i:print(num.Get_Value()))
    num.Set_TextFormat(lambda num:'{}'.format(round(num/100,2)).ljust(4,'0')+'s')
#    num.Set_TextFormat(lambda num:'<font color=#FF0000>{}</font>'.format(num))

    sys.exit(app.exec())




