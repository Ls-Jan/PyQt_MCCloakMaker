
import cv2
import numpy as np
from math import cos,sin


if(__package__):#如果是通过包导入该模块的话那么就用依赖导入
    from .XJ_Point import XJ_Point
    from .XJ_Cube import XJ_Cube
    from .XJ_Aspect import XJ_Aspect
else:
    from XJ_Point import XJ_Point
    from XJ_Cube import XJ_Cube
    from XJ_Aspect import XJ_Aspect



class XJ_AbstractCamera:#抽象摄像机，返回空间点的投影坐标（使用的是平行投影
    '''
        ↑z
        ↑
        ↑
        ↑     ↗y
        ↑   ↗
        ↑ ↗         x
        · → → → → → →
    '''

    def __init__(self,center=XJ_Point(0,0,0)):#center为摄像机围绕的中心坐标(三元组 x,y,z)
        self.__center=center.copy()#相机围绕的中心
        self.__pos=XJ_Point(0,0,100000)#相机位置。
        #__pos.x为水平方向的夹角，pos.y为垂直方向的夹角，pos.z意义为“摄像机与围绕中心的距离”(这参数在平行投影一般没啥意义)。
        #__pos.x和pos.y为0时相机到围绕中心的向量与y轴平行同向
        #__pos.x的值为z轴逆方向观察时的顺时针
        #__pos.y的值为x轴逆方向观察时的顺时针
        self.__canvas=XJ_Point(0,0,1)#投影的画面中心(x,y)以及放大倍数(z)
        self.__mat=self.__GetMatrix()#转换矩阵

    @property
    def Canvas_Center(self):#画面中心
        return (self.__canvas.x,self.__canvas.y)
    @Canvas_Center.setter
    def Canvas_Center(self,pos:tuple):#二维坐标，如(200,200)
        self.__canvas.x=int(pos[0])
        self.__canvas.y=int(pos[1])

    @property
    def Canvas_Scaling(self):#画面缩放比
        return self.__canvas.z
    @Canvas_Scaling.setter
    def Canvas_Scaling(self,scaling:float):
        if(scaling>0):
            self.__canvas.z=scaling

    @property
    def Camera_RotationCenter(self):#相机旋转中心
        return self.__center
    @Camera_RotationCenter.setter
    def Camera_RotationCenter(self,center:XJ_Point):
        self.__center=center

    @property
    def Camera_HorizontalAngle(self):#相机水平角
        return self.__pos.x
    @Camera_HorizontalAngle.setter
    def Camera_HorizontalAngle(self,angle):
        self.__pos.x=angle

    @property
    def Camera_VerticalAngle(self):#相机竖直角
        return self.__pos.y
    @Camera_VerticalAngle.setter
    def Camera_VerticalAngle(self,angle):
        self.__pos.y=angle

    def Update(self):#刷新摄像机信息
        self.__mat=self.__GetMatrix()

    def GetCameraPos(self):#返回摄像机位置(因为是平行投影，所以摄像机就取非常非常远的一个点(默认距围绕中心10w单位远)作为代表
        angleX=self.__pos.x
        angleY=self.__pos.y
        dist=self.__pos.z
        xy=dist*cos(angleY)
        z=dist*sin(angleY)
        x=-xy*sin(angleX)
        y=-xy*cos(angleX)
        return XJ_Point(x,y,z)

    def GetPoint(self,point):#获取3维空间的点在屏幕上的坐标，将返回二元元组+点到投影面的距离
        p=np.array([point.x,point.y,point.z,1]).dot(self.__mat)
        return (int(-p[0]+self.__canvas.x),int(p[2]+self.__canvas.y)),p[1]

    def __GetMatrix(self):#获取转换矩阵(投影到x0z平面上

        A=self.__pos.x
        B=self.__pos.y

        #平移旋转中心至原点
        T1=np.array([
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [-self.__center.x,-self.__center.y,-self.__center.z,1]])

        #绕z轴旋转，角度为pos.x+math.pi
        T2=np.array([
            [-cos(A),-sin(A),0,0],
            [sin(A),-cos(A),0,0],
            [0,0,1,0],
            [0,0,0,1]])

        #绕x轴旋转，角度为pos.y+math.pi
        T3=np.array([
            [1,0,0,0],
            [0,-cos(B),sin(B),0],
            [0,-sin(B),-cos(B),0],
            [0,0,0,1]])

        #对投影结果进行缩放
        return T1.dot(T2).dot(T3)*self.__canvas.z



if __name__=='__main__':
    W=400
    H=250
    center=XJ_Point(0.5,0.5,0.5)

    camera=XJ_AbstractCamera(center)
    camera.Canvas_Scaling=50
    camera.Canvas_Center=(W,H)
    camera.Update()

    cube=XJ_Cube(XJ_Point(0,0,0),XJ_Point(1,1,1))
    angle=0
    while(True):
        pict=np.zeros((H<<1,W<<1,4),dtype=np.uint8)
        points=[camera.GetPoint(p)[0] for p in cube.GetPoints(XJ_Aspect.Front)+cube.GetPoints(XJ_Aspect.Back)+[center]]
        for p in points[4:]:
            cv2.circle(pict,p,1,(255,255,255))
        for p in points[:4]:
            cv2.circle(pict,p,1,(0,0,255))

        points=[(W+p[0],H+p[1]) for p in points]

        cv2.imshow('pict',pict)
        cv2.waitKey()
        camera.Camera_VerticalAngle=angle
        camera.Camera_HorizontalAngle=angle
        camera.Update()
        angle=angle+0.1











