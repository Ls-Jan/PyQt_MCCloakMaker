
__version__='1.0.0'
__author__='Ls_Jan'

if(__package__):#如果是通过包导入该模块的话那么就用依赖导入
    from .XJ_Point import *
    from .XJ_Aspect import *
else:
    from XJ_Point import *
    from XJ_Aspect import *

class XJ_Cube:#暂不打算实现立方体的旋转缩放移动操作，因为目前来说没必要
    '''
        ↑z
        ↑         
        ↑       
        ↑     ↗y
        ↑   ↗
        ↑ ↗         x
        · → → → → → → 
    '''    
    def __init__(self,pos:XJ_Point,vector:XJ_Point):#pos为立方体的前左下角锚点，vector是矢量长宽高
        self.__pos=pos.copy()
        self.__vector={'x':XJ_Point(vector.x,0,0),'y':XJ_Point(0,vector.y,0),'z':XJ_Point(0,0,vector.z)}#设置成这个结构是为了让立方体适应性更高，可以完成旋转之类的魔鬼操作，虽然并不打算做这些复杂功能
        self.__picts=dict()#面附带的图片，一般是cv2.imread读取出来的图象，数据类型是np.ndarray

    def GetPoints(self,aspect:XJ_Aspect):#获取面的坐标信息，返回[LT:XJ_Point,RT:XJ_Point,RB:XJ_Point,LB:XJ_Point]，LT为左上角，RT为右上角，RB为右下角，LB为左下角
        P=self.__pos.copy()
        V=self.__vector
        LT,RT,RB=None,None,None
        if(aspect==XJ_Aspect.Front):
            LT=P+V['z']
            RT=LT+V['x']
            RB=P+V['x']
        elif(aspect==XJ_Aspect.Back):
            RB=P+V['y']
            RT=RB+V['z']
            LT=RT+V['x']
        elif(aspect==XJ_Aspect.Left):
            RB=P
            RT=RB+V['z']
            LT=RT+V['y']
        elif(aspect==XJ_Aspect.Right):
            LT=P+V['x']+V['z']
            RT=LT+V['y']
            RB=P+V['x']+V['y']
        elif(aspect==XJ_Aspect.Top):
            LT=P+V['y']+V['z']
            RT=LT+V['x']
            RB=P+V['x']+V['z']
        elif(aspect==XJ_Aspect.Bottom):
            LT=P
            RT=LT+V['x']
            RB=RT+V['y']
        return [LT,RT,RB,LT+RB-RT]
        
    def SetPict(self,aspect:XJ_Aspect,PICT):#设置对应面的图片，一般是cv2.imread读取出来的图象，数据类型是np.ndarray
        self.__picts[aspect]=PICT
    def GetPict(self,aspect:XJ_Aspect):#获取对应面的图片
        return self.__picts.setdefault(aspect,None)

    def SetAnchor(self,anchor):#设置锚点
        self.__pos=anchor
    def SetVectorX(self,x):#设置向量x
        self.__vector['x']=x
    def SetVectorY(self,y):#设置向量y
        self.__vector['y']=y
    def SetVectorZ(self,z):#设置向量z
        self.__vector['z']=z
    def GetAnchorAndVector(self):#返回锚点以及三向量
        #锚点为XJ_Point类型
        #三向量为dict，键分别为'x'、'y'、'z'，值为XJ_Point类型
        return self.__pos.copy(),self.__vector.copy()
    
    
if __name__=='__main__':
    cube=XJ_Cube(XJ_Point(0,0,0),XJ_Point(1,2,3))
    for i in XJ_Aspect:
        print(i.name)
        for j in cube.GetPoints(i):
            print(j)
        print()
    print(cube.GetAnchorAndVector())
    