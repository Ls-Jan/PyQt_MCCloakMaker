
__version__='1.0.0'
__author__='Ls_Jan'

from math import sqrt

class XJ_Point:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
        
    def copy(self):
        return XJ_Point(self.x,self.y,self.z)
        
    def __str__(self):
        return 'XJ_Point({},{},{})'.format(self.x,self.y,self.z)
        
    def __iter__(self):
        self.__cnt=0
        return self
    def __next__(self):
        num=self.x
        if(self.__cnt==1):
            num=self.y
        elif(self.__cnt==2):
            num=self.z
        elif(self.__cnt>2):
            raise StopIteration
        self.__cnt=self.__cnt+1
        return num
    
    def __add__(self,point):
        x=self.x+point.x
        y=self.y+point.y
        z=self.z+point.z
        return XJ_Point(x,y,z)
    
    def __sub__(self,point):
        x=self.x-point.x
        y=self.y-point.y
        z=self.z-point.z
        return XJ_Point(x,y,z)
    def DistanceTo(self,point,sqrtDist=False):
        d=pow(self.x-point.x,2)+pow(self.y-point.y,2)+pow(self.z-point.z,2)
        return d if sqrtDist==False else sqrt(d)
            
    
if __name__=='__main__':
    print('字串化')
    print(XJ_Point(1,2,3))
    print()

    print('列表化')
    print(list(XJ_Point('A','B','C')))
    print()

    print('加法')
    print(XJ_Point(100,200,300)+XJ_Point(1,2,3)+XJ_Point(1,2,3))
    print()

    print('减法')
    print(XJ_Point(100,200,300)-XJ_Point(1,2,3)-XJ_Point(1,2,3))
    print()
    
    print('迭代')
    for i in XJ_Point(100,200,300):
        print(i)
    print()
    
    print('迭代')    
    testA=XJ_Point('A','B','C')
    testB=XJ_Point('a','b','c')
    a=iter(testA)
    b=iter(testB)
    try:
        while True:
            print(next(a),next(b))
    except:
        pass
    print()
    
    
    