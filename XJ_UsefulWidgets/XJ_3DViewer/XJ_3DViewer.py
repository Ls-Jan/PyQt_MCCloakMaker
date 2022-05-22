
__version__='1.0.0'
__author__='Ls_Jan'

if(__package__):#如果是通过包导入该模块的话那么就用依赖导入
    from .XJ_SampleCamera import *
else:
    from XJ_SampleCamera import *
__all__=['XJ_3DViewer','XJ_Cube','XJ_Point','XJ_Aspect','XJ_SampleCamera']#在from XXX import *时限制导入的东西



import sys
import cv2
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import QLabel,QApplication

class XJ_3DViewer(QLabel):#只对立方体进行观察
    cameraMoved=pyqtSignal()#相机发生移动时(说白了就是拖拽屏幕)发送信号
    def __init__(self,parent=None,center=XJ_Point(0,0,0)):
        super(XJ_3DViewer,self).__init__(parent)
        self.camera=XJ_SampleCamera(center)#懒得保护它了，直接暴露出来

        self.__pictList=[]
        self.__cubes=set()
        self.__wheelDelta=5#滚轮滚动时的增量大小
        self.__clickPos=(0,0)#鼠标位置
        self.__minScale=1#最小缩放值，防止滚轮滚动时出现缩得过小的问题
        self.setMinimumSize(300,200)

    def mouseMoveEvent(self,event):
        x=event.pos().x()
        y=event.pos().y()
        c=self.camera
        if (event.buttons() & Qt.LeftButton):#按下左键进行拖拽
            deltaX=self.__clickPos[0]-x
            deltaY=self.__clickPos[1]-y
            self.__clickPos=(x,y)
            c.Camera_HorizontalAngle=c.Camera_HorizontalAngle-deltaX/200
            c.Camera_VerticalAngle=c.Camera_VerticalAngle-deltaY/200
            self.__UpdateCanvas()
        self.cameraMoved.emit()
    def mousePressEvent(self,event):
        x=event.pos().x()
        y=event.pos().y()
        if event.button()==Qt.LeftButton:#左键按下瞬间
            self.__clickPos=(x,y)
    def wheelEvent(self,event):
        scaling=self.camera.Canvas_Scaling
        if(event.angleDelta().y()>0):#滚轮向上滚动，增加
            self.camera.Canvas_Scaling=scaling*1.15#+self.__wheelDelta
        else:#向下滚动，减少
            if(scaling>self.__minScale):
                self.camera.Canvas_Scaling=scaling*0.85#-self.__wheelDelta
        self.__UpdateCanvas()
    def resizeEvent(self,event):
        size=event.size()
        w=size.width()
        h=size.height()
        c=self.camera

        c.Canvas_Size=(w,h)
        c.Canvas_Center=(w>>1,h>>1)
        super().resizeEvent(event)
        self.__UpdateCanvas()

    def __UpdateCanvas(self):#刷新观察结果
        self.camera.Update()
        img_PIL=self.camera.GetRendering(self.__pictList)
        self.setPixmap(img_PIL.toqpixmap())


    def UpdateCubes(self):#刷新图片列表
        self.__pictList.clear()
        for c in self.__cubes:
            for a in XJ_Aspect:
                pict=c.GetPict(a)
                if(type(pict)!=type(None)):
                    self.__pictList.append([c.GetPoints(a),pict])
        self.__UpdateCanvas()
    def AddCube(self,cube:XJ_Cube):#添加XJ_Cube
        self.__cubes.add(cube)
        self.UpdateCubes()
    def DelCube(self,cube:XJ_Cube):#将cube从集合中移除
        self.__cubes.remove(cube)
        self.UpdateCubes()
    def SetMinCanvasScale(self,minScale):#设置最小缩放值
        if(minScale>0):
            self.__minScale=minScale
    def GetNearestAspects(self,cube:XJ_Cube):#返回这个立方体的最近的3个面(这3个面不一定是观察面，因为摄像机有可能没对准这个立方体
        anchor,vector=cube.GetAnchorAndVector()
        cameraPos=self.camera.GetCameraPos()#摄像机位置

        vector['0']=XJ_Point(0,0,0)
        DistanceToCamera=lambda point:pow(cameraPos.x-point.x,2)+pow(cameraPos.y-point.y,2)+pow(cameraPos.z-point.z,2)
        dist={key:DistanceToCamera(anchor+vector[key]) for key in vector}

        aspects=set()
        aspects.add(XJ_Aspect.Left if dist['0']<dist['x'] else XJ_Aspect.Right)
        aspects.add(XJ_Aspect.Front if dist['0']<dist['y'] else XJ_Aspect.Back)
        aspects.add(XJ_Aspect.Bottom if dist['0']<dist['z'] else XJ_Aspect.Top)
        return aspects



if __name__ == '__main__':
    app = QApplication(sys.argv)

    viewer=XJ_3DViewer()
    viewer.camera.Canvas_Scaling=20
#    viewer.camera.Rendering_MaxDist=200
    viewer.camera.Canvas_Center=(50,50)
    viewer.camera.Camera_RotationCenter=XJ_Point(5,0.5,8)
    viewer.resize(1000,600)
    viewer.show()

    cube=XJ_Cube(XJ_Point(0,0,0),XJ_Point(10,1,16))
    cube.SetPict(XJ_Aspect.Back,cv2.imread("ABC.png",cv2.IMREAD_UNCHANGED))
    cube.SetPict(XJ_Aspect.Left,cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED))
    cube.SetPict(XJ_Aspect.Right,cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED))
    cube.SetPict(XJ_Aspect.Top,cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED))
    cube.SetPict(XJ_Aspect.Bottom,cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED))
    cube.SetPict(XJ_Aspect.Front,cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED))
    cube.SetPict(XJ_Aspect.Front,cv2.imread("Utsuho.png",cv2.IMREAD_UNCHANGED))
#    cube.SetVectorX(XJ_Point(30,-20,-20))
    viewer.AddCube(cube)

    subCube=XJ_Cube(XJ_Point(10,10,0),XJ_Point(16,16,16))
    subCube.SetPict(XJ_Aspect.Front,cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED))
    subCube.SetPict(XJ_Aspect.Back,cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED))
    subCube.SetPict(XJ_Aspect.Left,cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED))
    subCube.SetPict(XJ_Aspect.Right,cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED))
    subCube.SetPict(XJ_Aspect.Top,cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED))
    subCube.SetPict(XJ_Aspect.Bottom,cv2.imread("Utsuho.png",cv2.IMREAD_UNCHANGED))
    viewer.AddCube(subCube)

    viewer.cameraMoved.connect(lambda:print(viewer.GetNearestAspects(cube)))

    sys.exit(app.exec())


