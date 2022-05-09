
from XJ_UsefulWidgets import XJ_PictCropper#图片裁剪器
from XJ_UsefulWidgets import XJ_ColorChoose#颜色选择按钮
from XJ_UsefulWidgets import XJ_Slider_Horizon#水平滑动条

import sys
from PIL import Image
from PyQt5.QtGui import QImage,QColor
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QWidget,QPushButton,QCheckBox,QFileDialog,QMessageBox,QLabel


__all__=['XJ_Cropper']

class XJ_Cropper(QWidget):#附有“透明度条”、“自由裁剪复选框”、“图片选择按钮”的裁剪器
    cropChanged=pyqtSignal()#槽信号，裁剪区发生变化时发送信号(该信号无参)
    def __init__(self,parent=None,aspectRatio=(10,16),labelText="【前】"):#aspectRatio为裁剪的宽高比
        super().__init__()

        self.__ratio=aspectRatio
        self.__img=None#PIL.Image，因为有“改变透明度”的需要，所以就临时存起来了
        self.__slider=XJ_Slider_Horizon(self)#水平滑动条，给图片设置透明度
        self.__cp=XJ_PictCropper(self,200,320)
        self.__cpSize=QLabel("0x0",self)#标签，特地用于显示图片长宽（虽然没啥用
        vbox=QVBoxLayout(self)

        cp=self.__cp
        btn=QPushButton("选图",self)#图片选择按钮
        check=QCheckBox(self)#复选框(比例裁剪
        clr=XJ_ColorChoose(self)#颜色选择按钮
        slider=self.__slider
        labelText=QLabel(labelText,self)
        cpSize=self.__cpSize



        vbox.addWidget(cp,100)

        hbox=QHBoxLayout()
        hbox.addWidget(slider,1)
        hbox.addWidget(check)
        vbox.addLayout(hbox)

        hbox=QHBoxLayout()
        hbox.addWidget(labelText)
        hbox.addWidget(cpSize)
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addWidget(clr)
        vbox.addLayout(hbox)



        check.setToolTip("比例裁剪")
        clr.setToolTip("设置为纯色")
        check.clicked.connect(self.__Click_Check)
        btn.clicked.connect(self.__Click_Button)
        clr.valueChanged.connect(self.__Click_Color)
        cp.valueChanged.connect(self.__CropChanged)
        slider.valueChanged.connect(self.__AlphaChanged)
        clr.Set_Color((192,255,255))
        slider.setMaximum(255)
        slider.setValue(255)
        slider.setPageStep(32)
        cp.Set_SmoothCrop(True)
        cp.Get_Setting().background.size=1
        cp.Get_Setting().cropper.rowCnt=1
        cp.Get_Setting().cropper.colCnt=1
        labelText.setStyleSheet("font-size:28px;  color:rgb(96,96,255);")
        cpSize.setStyleSheet("font-size:20px;  color:rgb(255,64,192);")
        btn.setStyleSheet("font-size:24px;  color:rgb(96,96,255);  border-color:#88AAAA;  border-style: solid;  border-width:3px; border-radius:10px;")

    def Get_Crop(self):#获取截图
        return self.__cp.Get_Crops(False)

    def Get_AspectRatio(self):#返回裁剪的宽高比
        return self.__ratio

    def Set_Img(self,PIL_Img):#设置图片
        self.__img=PIL_Img
        self.__cp.SetImg(PIL_Img)

    def MaximizePict(self):#图片最大化
        self.__cp.MaximizePict()

    def MaximizeCrop(self):#裁剪区最大化
        self.__cp.MaximizeCrop()

    def __CropChanged(self):
        area=self.__cp.Get_CropArea()
        self.__cpSize.setText('{}x{}'.format(*((area.width,area.height) if area else (0,0))))#设置一下标签
        self.cropChanged.emit()

    def __AlphaChanged(self,val):#透明度发生变化
        cp=self.__cp
        img=self.__img
        self.__slider.setToolTip('透明度：{}'.format(val))
        cp.valueChanged.disconnect(self.__CropChanged)#避免因为修改透明度而导致cropChanged发出信号
        area=cp.Get_CropArea()#临时记录下裁剪区，等会儿恢复
        cp.SetImg(XJ_Cropper.__GetAlphaImg(img,val/255))
        cp.valueChanged.connect(self.__CropChanged)#将信号事件恢复回来
        cp.Set_CropArea(area)#恢复裁剪区

    @staticmethod
    def __GetAlphaImg(PIL_Img, alpha = 0.7 ):#给PIL图片附上透明度：https://cloud.tencent.com/developer/article/1740547
        return Image.blend(Image.new('RGBA', PIL_Img.size, (0,0,0,0)), PIL_Img.convert('RGBA'), alpha)

    def __Click_Color(self,color):#点击了“纯色”按钮，color为三元元组
        img=Image.new('RGBA', (64,64), (*color,255))
        if(self.__img and self.__img.size!=img.size):
            self.__cp.Set_CropArea(None)
        self.__img=img
        self.__AlphaChanged(self.__slider.value())

    def __Click_Button(self,event):#点击了“选择图片”按钮
        path=QFileDialog.getOpenFileName(self,'选择图片')[0].replace('\\','/')#路径名的反斜杠全改为斜杠
        if(path):
            try:
                img=Image.open(path)
                if(self.__img.size!=img.size):
                    self.__cp.Set_CropArea(None)
                self.__img=img
                self.__AlphaChanged(self.__slider.value())
            except:
                QMessageBox.information(self,"图片读取失败","【{}】\n不是图片！".format(path))

    def __Click_Check(self,mark):#点击了“比例裁剪”复选框
        self.__cp.Set_AspectRatio(self.__ratio if mark else (0,0))
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    cp=XJ_Cropper()
    cp.show()
    cp.resize(500,300)
    sys.exit(app.exec())

