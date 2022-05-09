from XJ_Cropper import *
from XJ_UsefulWidgets import XJ_Aspect,XJ_Point,XJ_Cube#立方体以及点以及面枚举
from XJ_UsefulWidgets import XJ_3DViewer#3D显示


import sys
import cv2
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QWidget,QPushButton

__all__=['XJ_CropperGroup']

class XJ_CropperGroup_3(QWidget):#显示3个Cropper
    def __init__(self,parent,cpDict):#cpDict的键值类型为XJ_Aspect-XJ_Cropper
        super().__init__(parent)
        boxes=[]#三组裁剪区，格式为[[XJ_Aspect,QVBoxLayout],[...],[...]]

        self.__dict=cpDict
        self.__boxes=boxes

        for p in [XJ_Aspect.Front,XJ_Aspect.Left,XJ_Aspect.Top]:
            boxLayout=QVBoxLayout()
            boxLayout.addWidget(cpDict[p])
            boxes.append([p,boxLayout])
        hbox=QHBoxLayout(self)
        vbox=QVBoxLayout()
        vbox.addLayout(boxes[1][1],2)#侧面
        vbox.addLayout(boxes[2][1],1)#顶底面
        hbox.addLayout(boxes[0][1],3)#正面
        hbox.addLayout(vbox,3)

    def SwitchCropper(self,aspectSet):#根据传入的Set来切换显示
        cpDict=self.__dict
        for p in self.__boxes:
            if(p[0] not in aspectSet):
                theOther=XJ_Aspect(5-p[0].value)#另一个面
                wid_remove=cpDict[p[0]]
                wid_add=cpDict[theOther]
                p[0]=theOther#更新
                p[1].removeWidget(wid_remove)#替换组件
                p[1].addWidget(wid_add)
                wid_remove.hide()
                wid_add.show()
            else:
                p[1].addWidget(cpDict[p[0]])


class XJ_CropperGroup_2(QWidget):#显示2个Cropper
    def __init__(self,parent,cpDict):#cpDict的键值类型为XJ_Aspect-XJ_Cropper
        super().__init__(parent)
        boxes=[]#三组裁剪区，存放着3个QWidget，以及对应的XJ_Cropper(为啥还存这玩意儿呢？主要是因为一个控件至多只能归属于一个布局，在三面切二面时得重新加回去

        self.__boxes=boxes
        self.__stat=2

        for p in [(XJ_Aspect.Front,XJ_Aspect.Back),(XJ_Aspect.Left,XJ_Aspect.Right),(XJ_Aspect.Top,XJ_Aspect.Bottom)]:
            wid=QWidget(self)
            hbox=QHBoxLayout(wid)
            elem=(wid,cpDict[p[0]],cpDict[p[1]])
            boxes.append(elem)
            hbox.addWidget(elem[1])
            hbox.addWidget(elem[2])
        hbox=QHBoxLayout(self)
        hbox.addWidget(elem[0])

    def SwitchCropper(self,stat):#根据档位切换界面。前后面(0)、左右面(1)、上下面(2)
        old=self.__boxes[self.__stat]
        new=self.__boxes[stat]
        self.layout().removeWidget(old[0])
        self.layout().addWidget(new[0])
        new[0].layout().addWidget(new[1])
        new[0].layout().addWidget(new[2])
        old[0].hide()
        new[0].show()
        new[1].show()
        new[2].show()
        self.__stat=stat


class XJ_CropperGroup(QWidget):#显示Cropper组
    def __init__(self,parent,cpDict):#cpDict的键值类型为XJ_Aspect-XJ_Cropper，viewer为XJ_3DViewer(绑定事件cameraMoved)，cube为XJ_Cube(作为viewer的参数)
        super().__init__(parent)

        self.__viewer=None
        self.__cube=None
        self.__cpDict=cpDict
        self.__gp2=XJ_CropperGroup_2(self,cpDict)
        self.__gp3=XJ_CropperGroup_3(self,cpDict)
        self.__stat=3

        hbox=QHBoxLayout(self)
        hbox.addWidget(self.__gp3)

    def __SetCropper(self):#给相机用的回调，用于三面模式的自动切换
        if(self.__stat==3):
            self.__gp3.SwitchCropper(self.__viewer.GetNearestAspects(self.__cube))
    def BindViewerAndCube(self,viewer,cube):#绑定3DViewer以及对应方块(为了让三面模式能自动切换对应的面)。将占用viewer.cameraMoved事件
        if(self.__viewer):
            self.__viewer.disconnect(self.__SetCropper)
        viewer.cameraMoved.connect(self.__SetCropper)
        self.__viewer=viewer
        self.__cube=cube
    def SwitchCropper(self,stat):#根据档位切换界面。前后面(0)、左右面(1)、上下面(2)、三面-自动(3)
        self.__stat=stat
        if(stat==3):
            self.layout().replaceWidget(self.__gp2,self.__gp3)
            self.__gp2.hide()
            self.__gp3.show()
            if(self.__viewer):
                for i in range(2):#【【【虽然觉得莫名其妙，但就先这么处理了。(代码段要执行两遍才能获得好效果)】】】
                    for s in [{XJ_Aspect.Front,XJ_Aspect.Left,XJ_Aspect.Top},{XJ_Aspect.Back,XJ_Aspect.Right,XJ_Aspect.Bottom}]:
                        self.__gp3.SwitchCropper(s)
                        for asp in s:
                            self.__cpDict[asp].MaximizePict()
                self.__gp3.SwitchCropper(self.__viewer.GetNearestAspects(self.__cube))
        else:
            self.layout().replaceWidget(self.__gp3,self.__gp2)
            self.__gp3.hide()
            self.__gp2.show()
            self.__gp2.SwitchCropper(stat)
            for asp in XJ_Aspect:
                cp=self.__cpDict[asp]
                if(cp.isVisible()):
                    cp.MaximizePict()
    def Status(self):#返回档位值
        return self.__stat

if __name__ == '__main__':
    app = QApplication(sys.argv)

    cube=XJ_Cube(XJ_Point(0,0,0),XJ_Point(10,10,10))
    for asp in XJ_Aspect:
        cube.SetPict(asp,cv2.imread("Utsuho.png",cv2.IMREAD_UNCHANGED))

    viewer=XJ_3DViewer(None,XJ_Point(5,5,5))
    viewer.camera.Canvas_Scaling=20
    viewer.AddCube(cube)
    viewer.setGeometry(200,200,800,600)

    cpDict={asp:XJ_Cropper(labelText=str(asp)) for asp in XJ_Aspect}
    cg=XJ_CropperGroup(None,cpDict)
    cg.BindViewerAndCube(viewer,cube)

    btn0=QPushButton("切换到0档")
    btn1=QPushButton("切换到1档")
    btn2=QPushButton("切换到2档")
    btn3=QPushButton("切换到3档")
    btn0.clicked.connect(lambda:cg.SwitchCropper(0))
    btn1.clicked.connect(lambda:cg.SwitchCropper(1))
    btn2.clicked.connect(lambda:cg.SwitchCropper(2))
    btn3.clicked.connect(lambda:cg.SwitchCropper(3))

    widget=QWidget()
    box=QHBoxLayout(widget)
    box.addWidget(viewer)
    box.addWidget(cg)
    box.addWidget(btn0)
    box.addWidget(btn1)
    box.addWidget(btn2)
    box.addWidget(btn3)
    widget.show()
    widget.resize(1000,600)

    # cg.SwitchCropper(2)
    # cg.SwitchCropper(1)
    
    
    # cg.SwitchCropper(2)
    # cg.SwitchCropper(1)
    # cg.SwitchCropper(0)


    sys.exit(app.exec())

