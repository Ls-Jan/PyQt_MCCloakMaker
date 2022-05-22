
__version__='1.0.0'
__author__='Ls_Jan'

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QSlider

__all__=['XJ_Slider_Horizon']


#滑动条的样式表。来源：https://blog.csdn.net/robertkun/article/details/20119135
#在此基础上做了一些调整
CSS_Slider_Horizon='''
    QSlider::groove:horizontal {
        border: 1px solid #4A708B;
        background: #C0C0C0;
        height: 20px;
        border-radius: 10px;
        padding-left:-1px;
        padding-right:-1px;
    }

    QSlider::sub-page:horizontal {
        background: qlineargradient(
                x1: 0, y1: 0,
                x2: 0, y2: 1, 
            stop:0 #B1B1B1, 
            stop:1 #1874CD);
        background: qlineargradient(
                x1: 0, y1: 0.5,
                x2: 1, y2: 1,
            stop: 0 #A080FF,
            stop: 1 #4080FF);
        border: 5px solid #FFFFFF;
        height: 10px;
        border-radius: 10px;
    }

    QSlider::add-page:horizontal {
        background: #575757;
        border: 5px solid #FFFFFF;
        height: 10px;
        border-radius: 10px;
    }

    QSlider::handle:horizontal 
    {
        background: qradialgradient(spread:pad, 
            cx:0.5, cy:0.5, radius:0.5, 
            fx:0.5, fy:0.5,
        stop:0.8 #45ADED, 
        stop:0.81 #FFFFFF);

        width: 25px;
        margin-top: -3px;
        margin-bottom: -3px;
        border-radius: 12px;
    }

    QSlider::handle:horizontal:hover {
        background: qradialgradient(spread:pad, 
            cx:0.5, cy:0.5, radius:0.5,
            fx:0.5, fy:0.5,
        stop:0.8 #2080FF, 
        stop:0.9 #FFFFFF);

        width: 25px;
        margin-top: -3px;
        margin-bottom: -3px;
        border-radius: 12px;
    }

'''






class XJ_Slider_Horizon(QSlider):
    def __init__(self,parent=None):
        super().__init__(Qt.Horizontal,parent)
        self.setStyleSheet(CSS_Slider_Horizon)

    def mousePressEvent(self,event):#避免滑块反复横跳而重写该方法，使滑块总能移动到鼠标附近
        min=self.minimum()#最小值
        cur=self.value()#当前值
        wid=self.maximum()-min#取值区间长度
        rate=event.pos().x()/self.size().width()#鼠标点击位置对应滑动条的位置(取值0.0~1.0)
        pos=min+int(wid*rate)#鼠标点击位置对应的值

        super().mousePressEvent(event)
        if(abs(pos-cur)<self.pageStep()):#点击位置在单步范围内时直接设置为对应值，避免反复横跳
            self.setValue(pos)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    slider=XJ_Slider_Horizon(None)
    slider.valueChanged.connect(lambda value:print(value))
    slider.setMaximum(50)
    slider.setValue(25)    
    slider.setMaximum(10)
    slider.resize(1500,50)
    slider.show()
    sys.exit(app.exec())













