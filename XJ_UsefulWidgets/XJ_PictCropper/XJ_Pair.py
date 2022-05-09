
class XJ_Pair:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
    @property
    def width(self):
        return self.x
    @property
    def height(self):
        return self.y
    @width.setter
    def width(self,w):
        self.x=w
    @height.setter
    def height(self,h):
        self.y=h

    def __str__(self):
        return "XJ_Pair"+str((self.x,self.y))
    def copy(self):
        return XJ_Pair(self.x,self.y)
        