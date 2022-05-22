
__version__='1.0.0'
__author__='Ls_Jan'

import sys
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication,QPushButton,QColorDialog

__all__=['XJ_ColorChoose']

class XJ_ColorChoose(QPushButton):#小控件，点击弹出换色窗口。QWidget子类化时样式表不生效(也就是继承QWidget后样式表无效，或者说不能继承QWidget)，np
    valueChanged=pyqtSignal(tuple)#槽信号，值修改时发送信号
    def __init__(self,parent=None,rgb=(255,50,50),width=10):
        super().__init__(parent)
        self.setMouseTracking(True)#时刻捕捉鼠标移动
        self.__color=QColor(*rgb)
        self.__SetColor()

    def __SetColor(self):
        self.setStyleSheet("QPushButton{{background-color:rgb{0};}};".format(self.GetColor()))#设置颜色
        self.update()
        
    def mouseMoveEvent(self,event):
        self.setCursor(Qt.PointingHandCursor)#手型光标

    def mousePressEvent(self,event):#设置点击事件
        if event.button()==Qt.LeftButton:#左键点击
            col=QColorDialog.getColor()
            if(col.isValid()):
                self.__color=col
                self.__SetColor()
                self.valueChanged.emit(self.GetColor())#值修改时发送信号
                
    def SetColor(self,color):#color为三元元组，如(255,128,64)
        self.__color=QColor(*color)
        self.__SetColor()
        self.valueChanged.emit(self.GetColor())#值修改时发送信号
        
    def GetColor(self):#返回三元元组
        col=self.__color
        return (col.red(),col.green(),col.blue())




if __name__=='__main__':
    app = QApplication(sys.argv)

    test=XJ_ColorChoose()
    test.show()
    test.SetColor((128,64,32))
    test.valueChanged.connect(lambda t:print(t))
    
    sys.exit(app.exec())

    
    
    
    
    
    