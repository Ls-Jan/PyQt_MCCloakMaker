
from XJ_UsefulWidgets import XJ_NumInput#数字输入框
from XJ_UsefulWidgets import XJ_Slider_Horizon#水平滑动条

import sys
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout,QWidget,QLabel


__all__=['XJ_LimitedVaule']

class XJ_LimitedVaule(QWidget):
    valueChanged=pyqtSignal(int)#槽信号，值发生变化时发送信号

    def __init__(self,parent=None,hint="数值："):
        super().__init__(parent)
        hbox=QHBoxLayout(self)

        label=QLabel(hint,self)
        num=XJ_NumInput(self)
        slider=XJ_Slider_Horizon(self)

        num.valueChanged.connect(self.__NumChanged)
        slider.valueChanged.connect(self.__SliderChanged)
        hbox.addWidget(label)
        hbox.addWidget(num,1)
        hbox.addWidget(slider,5)

        self.__label=label
        self.__num=num
        self.__slider=slider
        self.__change=''#相当于一个锁，改值时避免发送两次信号。并且该值不为空时说明是哪个控件的数据是新的
    def SetSheet_Label(self,sheet):
        self.__label.setStyleSheet(sheet)
    def SetSheet_Label(self,sheet):
        self.__num.setStyleSheet(sheet)
    def SetSheet_Label(self,sheet):
        self.__slider.setStyleSheet(sheet)
    def SetMinimum(self,value):
        self.__slider.setMinimum(value)
        self.__num.Set_Minimum(value)
    def SetMaximum(self,value):
        self.__slider.setMaximum(value)
        self.__num.Set_Maximum(value)
    def GetValue(self):
        if(self.__change=='N'):
            return self.__num.Get_Value()
        return self.__slider.value()
    def SetValue(self,value):
        self.__num.Set_Value(value)

    def __NumChanged(self,value):
        if(self.__change!=''):
            self.__change='N'
            self.valueChanged.emit(value)
        self.__slider.setValue(value)
        self.__change=False
    def __SliderChanged(self,value):
        if(self.__change!=''):
            self.__change='S'
            self.valueChanged.emit(value)
        self.__num.Set_Value(value)

        self.__change=False


if __name__ == '__main__':
    app = QApplication(sys.argv)

    lv=XJ_LimitedVaule()
    lv.show()
    lv.resize(500,300)

    sys.exit(app.exec())

