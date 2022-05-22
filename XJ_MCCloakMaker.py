from XJ_UsefulWidgets import XJ_3DViewer#3D显示
from XJ_UsefulWidgets import XJ_Aspect,XJ_Point,XJ_Cube#立方体以及点以及面枚举

from XJ_LimitedValue import *#带有Label、数字输入框、滑动条的数值输入器
from XJ_Cropper import *#附有“透明度条”、“自由裁剪复选框”、“图片选择按钮”的裁剪器
from XJ_CropperGroup import *#裁剪器组

import sys
import cv2
import os
import numpy as np
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QWidget,QPushButton,QFileDialog,QMessageBox,QLabel


__all__=['XJ_MCCloakMaker']

class XJ_MCCloakMaker(QWidget):
    __cropperMsg=[#懒人至高境界
        (XJ_Aspect.Front,(10,16),"【前】",(1,1)),#数据依次是：面，裁剪宽高比例，裁剪器左下角文本，对应的披风文件的位置
        (XJ_Aspect.Back,(10,16),"【后】",(12,1)),
        (XJ_Aspect.Left,(1,16),"【左】",(0,1)),
        (XJ_Aspect.Right,(1,16),"【右】",(11,1)),
        (XJ_Aspect.Top,(10,1),"【上】",(1,0)),
        (XJ_Aspect.Bottom,(10,1),"【下】",(11,0))
    ]

    def __init__(self,parent=None):
        super().__init__(parent)

        cpDict={p[0]:XJ_Cropper(self,p[1],p[2]) for p in XJ_MCCloakMaker.__cropperMsg}
        viewer=XJ_3DViewer(self)
        viewer.camera.Camera_RotationCenter=XJ_Point(5,0.5,8)
        cube=XJ_Cube(XJ_Point(0,0,0),XJ_Point(10,1,16))
        resolution=XJ_LimitedValue(self,"分辨率：")
        pictSize=QPushButton("<点击刷新>",self)#获取图片大小
        cpGroup=XJ_CropperGroup(self,cpDict)

        self.__cpDict=cpDict
        self.__cpGroup=cpGroup
        self.__viewer=viewer
        self.__cube=cube
        self.__resolution=resolution
        self.__pictSize=pictSize

        viewer.camera.Canvas_Scaling=20
        viewer.camera.Canvas_Center=(200,200)
        viewer.SetMinCanvasScale(10)
        resolution.resoList=[1]*6#记录着6个面的分辨率，到时用来修改滑动条的最大值的
        resolution.valueChanged.connect(self.__ChangeResolution)
        resolution.SetMinimum(1)
        resolution.SetMaximum(1)
        cpGroup.BindViewerAndCube(viewer,cube)
        viewer.AddCube(cube)
        pictSize.clicked.connect(self.__CalcuPictSize)
        for aspect in cpDict:
            cpDict[aspect].cropChanged.connect(self.__ChangeCubePict(aspect,True))


        viewerBox=QVBoxLayout()
        viewerBox.addWidget(viewer,1)
        viewerBox.addWidget(resolution)

        hbox=QHBoxLayout()
        hbox.addWidget(QLabel("   文件大小："))
        hbox.addWidget(pictSize)
        hbox.addStretch(1)
        viewerBox.addLayout(hbox)

        hbox=QHBoxLayout()
        hbox.addLayout(viewerBox,2)
        hbox.addWidget(cpGroup,4)
        self.setLayout(hbox)

        self.__InitCropper()
        self.setFocusPolicy(Qt.StrongFocus)
#        self.setMinimumSize(1200,600)

    def __CalcuPictSize(self):#计算图片文件大小
        pict=self.__GetCloakPict()
        pathName="临时文件.png"
        pict.save(pathName)
        size=os.path.getsize(pathName)/1024#KB
        self.__pictSize.setText("{}KB".format(round(size,2)))

    def __ChangeResolution(self,value):#披风分辨率发生变化时
        self.__resolution.setToolTip("(10x16)*"+str(value))
        for aspect in self.__cpDict:
            self.__ChangeCubePict(aspect,False)()

    def __ChangeCubePict(self,aspect,changeResolution=True):#改变立方体某一个面的图片(使用闭包)。changeResolution为真时会同时修改resolution(分辨率)的值
        def inner():
            self.__pictSize.setText('<点击刷新>')
            img=self.__GetImgFromCropper(aspect,changeResolution)

            self.__cube.SetPict(aspect,img)
            self.__viewer.UpdateCubes()#方块的图片发生变化时要调用这个函数去更新缓存
        return inner

    def __GetImgFromCropper(self,aspect,changeResolution=True):#返回对应裁剪器的图片(图片经过resize)，图片类型为np.ndarray。changeResolution为真时会同时修改resolution(分辨率)的对应值
        cp=self.__cpDict[aspect]
        img_PIL=cp.Get_Crop()
        ratio=cp.Get_AspectRatio()
        reso=self.__resolution
        resoLst=reso.resoList

        img=None
        if(img_PIL):
            size=img_PIL.size
            if(changeResolution):#调整分辨率
                rateW=int(size[0]/ratio[0]+0.999)#懒得找ceil函数了
                rateH=int(size[1]/ratio[1]+0.999)
                resoLst[aspect.value]=min(max(rateW,rateH),100)#过高的分辨率只会造成浪费+卡顿
                reso.SetMaximum(max(resoLst))
            value=reso.GetValue()#对图片进行resize
            size=(ratio[0]*value,ratio[1]*value)
            img_PIL=img_PIL.resize((size[0],size[1]))
            img=np.array(img_PIL)#PIL.Image转np.ndarray：https://zhuanlan.zhihu.com/p/138962553
            img=cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)#颜色调转一下。因为cv2.imread读出来的图象的颜色通道值是BGR(而PIL转出来的是RGB)...
        else:
            resoLst[aspect.value]=1
            reso.SetMaximum(max(resoLst))
        return img

    def __GetCloakPict(self):#获取披风图
        unit=self.__resolution.GetValue()
        cube=self.__cube

        pict=Image.new("RGBA",(64*unit,32*unit))
        for msg in XJ_MCCloakMaker.__cropperMsg:
            aspect,_,_,pos=msg
            img=cube.GetPict(aspect)#转换为PIL.Image类型
            if(type(img)!=type(None)):
                img=Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))
            else:
                ratio=self.__cpDict[aspect].Get_AspectRatio()
                img=Image.new("RGBA",(ratio[0]*unit,ratio[1]*unit))
            pict.paste(img,(pos[0]*unit,pos[1]*unit))#粘贴到对应位置
        return pict

    def __InitCropper(self):#对裁剪器六面进行初始化
        cpDict=self.__cpDict
        lst=[#懒人再一次
            (XJ_Aspect.Front,"Utsuho.png"),
            (XJ_Aspect.Back,"Diana.png"),
            (XJ_Aspect.Left,(192,192,192,255)),
            (XJ_Aspect.Right,(192,192,192,255)),
            (XJ_Aspect.Top,(192,192,192,255)),
            (XJ_Aspect.Bottom,(192,192,192,255))
        ]
        for item in lst:
            cp=cpDict[item[0]]
            msg=item[1]
            if(type(msg)==str):
                try:
                    img=Image.open(msg)
                except:
                    img=Image.new('RGBA', (64,64), (255,255,255,255))
            else:
                img=Image.new('RGBA', (64,64), msg)
            cp.Set_Img(img)
            cp.MaximizeCrop()
            cp.MaximizePict()
        self.__resolution.SetValue(24)


    def SwitchCropper(self,stat):#根据档位切换界面。前后面(0)、左右面(1)、上下面(2)、三面-自动(3)
        self.__cpGroup.SwitchCropper(stat)
    def SaveCloak(self):#保存披风
        path=QFileDialog.getSaveFileName(self,"保存披风","披风","PNG(*.png)")[0].replace('\\','/')#路径名的反斜杠全改为斜杠
        if(path):
            self.__GetCloakPict().save(path)
            QMessageBox.information(self,'披风保存成功','路径为：\n{}'.format(path))
    def LoadCloak(self):#读取披风文件
        path=QFileDialog.getOpenFileName(self)[0].replace('\\','/')#路径名的反斜杠全改为斜杠
        if(len(path)>0):
            try:
                img=Image.open(path)
                size=img.size
                unitW=size[0]/64
                unitH=size[1]/32
                if((unitH!=unitW) or (unitH.is_integer()==False)):
                    QMessageBox.information(self,'格式错误','图片【{}】\n的尺寸不是64x32的整数倍，不是披风图片'.format(path))
                unit=int(min(unitW,unitH))
                for msg in XJ_MCCloakMaker.__cropperMsg:
                    aspect,size,_,pos=msg
                    L=pos[0]*unit
                    T=pos[1]*unit
                    W=size[0]*unit
                    H=size[1]*unit
                    im=img.crop((L,T,L+W,T+H))
                    cp=self.__cpDict[aspect]
                    cp.Set_Img(im)
                    cp.MaximizeCrop()
                    cp.MaximizePict()
                self.__resolution.SetValue(100)
            except:
                QMessageBox.information(self,"图片读取失败","【{}】\n不是图片！".format(path))




if __name__ == '__main__':
    app = QApplication(sys.argv)

    cm=XJ_MCCloakMaker()
    cm.show()
#    cm.SwitchCropper(3)
#    cm.LoadCloak()

    sys.exit(app.exec())






