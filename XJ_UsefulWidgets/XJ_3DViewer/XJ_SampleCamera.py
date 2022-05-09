if(__package__):#如果是通过包导入该模块的话那么就用依赖导入
    from .XJ_AbstractCamera import *
else:
    from XJ_AbstractCamera import *

__all__=['XJ_SampleCamera','XJ_Aspect','XJ_Cube','XJ_Point']

from PIL import Image

class XJ_SampleCamera(XJ_AbstractCamera):
    def __init__(self,center=XJ_Point(0,0,0)):#center为摄像机围绕的中心坐标(三元组 x,y,z)
        super().__init__(center)
        self.__size=(100,100)
        self.__maxDist=10000
    @property
    def Canvas_Size(self):#设置投影结果的长宽
        return self.__size
    @Canvas_Size.setter
    def Canvas_Size(self,size:tuple):#设置画布长宽，如(1000,600)
        self.__size=size

    @property
    def Rendering_MaxDist(self):#设置最大渲染距离(可取负值)，与投影面的最短距离超过该值的面将不予渲染。(简单粗暴，没有做“裁剪渲染”操作，懒得搞主要是，而且效果也不好，建议别用
        return self.__maxDist
    @Rendering_MaxDist.setter
    def Rendering_MaxDist(self,dist:int):
        self.__maxDist=dist

    def GetRendering(self,pictList:list):#根据图片列表渲染图片。返回的数据类型为PIL.Image
        #图片列表格式为：[(Points,PICT),...]
        #Points指的是坐标四元组，代表着该图片在空间中的四个坐标(依次是"左上","右上","右下","左下")，坐标的数据类型是XJ_Point
        #PICT是指cv2.imread读取出来的图象，图片的数据类型是np.ndarray
        W=self.__size[0]>>1
        H=self.__size[1]>>1
        index=[]#图片列表(深度+图片+图片投影的四个二维坐标顶点)（以此决定渲染优先级
        for pst in range(len(pictList)):
            pict=pictList[pst][1]
            if(type(pict)!=type(None)):#只处理有图的
                points=[self.GetPoint(p) for p in pictList[pst][0]]
                if(len(pict[0][0])==3):#如果是rgb的那么就改成rgba格式
                    pict=np.insert(pict,3,np.ones(len(pict[0]))*255,axis=2)
                minDist=min(points,key=lambda p:p[1])[1]
                if(abs(minDist)<self.__maxDist):#在预置高度内的才参与渲染。(这做法明显不合理，但mole不想往深了研究。只不过这个的限制效果也不理想
                    index.append((minDist,pict,[p[0] for p in points]))
        index.sort(key=lambda msg:msg[0],reverse=True)#根据深度从高到低排序（越低的越后渲染

        rendering=Image.new("RGBA",(W<<1,H<<1))
        for item in index:#依次渲染
            img=item[1]#图片
            width,height = len(img[0]),len(img)#图片的宽高
            pts1 = np.float32([[0,0],[width,0],[width,height],[0,height]])#原图四顶点
            pts2 = np.float32(item[2])#透视后的四顶点
            pts1-=0.5#这个的原因不明，如果不加的话对于超小图片(长宽也就几像素的)会出现偏移问题
            pts2=pts2+0.005#加个膜法数字，防止出现各种奇怪问题(可以试着删掉这条语句看看会跑出啥问题的)。问题根源不明，只知道这条语句能解决这问题

            trans=None
            if(self.__AreTheyOnOneLine(pts2)==False):#如果透视的四顶点不处于同一条线那么该透视图有效
                mat = cv2.getPerspectiveTransform(pts1,pts2)  #使用getPerspectiveTransform()得到转换矩阵
                trans = cv2.warpPerspective(img,mat,(W<<1,H<<1),flags=cv2.INTER_NEAREST)  #使用warpPerspective()进行透视变换
            else:#图片成一条直线的话那就画个四边形把它填充
                pts=np.array([(int(p[0]),int(p[1])) for p in pts2])
                trans=np.zeros((H<<1,W<<1,4),dtype=np.uint8)
                cv2.fillConvexPoly(trans,pts,(255,255,255,255))
            rst=Image.fromarray(cv2.cvtColor(trans,cv2.COLOR_BGRA2RGBA))#转换为PIL.Image类型
            rendering.paste(rst,mask=rst.split()[3])#以透明度作为蒙版进行粘贴
        return rendering

    @staticmethod
    def __AreTheyOnOneLine(lst:np.float32,threshold=1):#判断狗日的几个点是否处于一条直线上。阈值作为其他点是否算在线上的判断依据
        if(len(lst)>1):
            p0=lst[0]
            v0=None
            lenV=0
            for p in lst[1:]:
                v=p-p0
                if((v>threshold).any() or (v<-threshold).any()):#两点不是过分靠近，进入下一步判断
                    if(type(v0)==type(None)):
                        v0=v
                    else:#v0不为空，开始判断v0和v是否足够接近
                        val=np.cross(v0,v)#计算叉乘值（几何意义：两向量组成的平行四边形的面积
                        if(val!=0):
                            d1=v0[0]*v0[0]+v0[1]*v0[1]
                            d2=v[0]*v[0]+v[1]*v[1]
                            h=val*val/max(d1,d2)#点到直线的距离(平方值
                            if(h>threshold*threshold):#如果距离够远，那说明不处于同一条线
                                return False
        return True

if __name__=='__main__':
    np.set_printoptions(suppress=True)
    camera=XJ_SampleCamera(XJ_Point(0.5,0.5,0.5))
    camera.Canvas_Scaling=100
    camera.Canvas_Size=(900,500)
    camera.Canvas_Center=(500,300)
    camera.Update()

    cube=XJ_Cube(XJ_Point(0,0,0),XJ_Point(1,1,1))
    pictList=[]
    pictList.append([cube.GetPoints(XJ_Aspect.Front),cv2.imread("Utsuho.png",cv2.IMREAD_UNCHANGED)])
    pictList.append([cube.GetPoints(XJ_Aspect.Back),cv2.imread("Utsuho.png",cv2.IMREAD_UNCHANGED)])
    pictList.append([cube.GetPoints(XJ_Aspect.Left),cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED)])
    pictList.append([cube.GetPoints(XJ_Aspect.Right),cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED)])
    pictList.append([cube.GetPoints(XJ_Aspect.Top),cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED)])
    pictList.append([cube.GetPoints(XJ_Aspect.Bottom),cv2.imread("Cube.png",cv2.IMREAD_UNCHANGED)])

    angle=0
    while(True):
        img = cv2.cvtColor(np.asarray(camera.GetRendering(pictList)),cv2.COLOR_RGBA2BGRA)
        cv2.imshow('rst',img)
        cv2.waitKey()

#        camera.Camera_VerticalAngle=angle
        camera.Camera_HorizontalAngle=angle
        print(angle)
        camera.Update()
        angle=angle+0.1












