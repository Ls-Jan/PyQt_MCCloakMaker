class XJ_Rect:
    def __init__(self,L=0,T=0,R=0,B=0):
        self.__left=L
        self.__right=R
        self.__top=T
        self.__bottom=B

    @property
    def left(self):
        return self.__left
    @property
    def right(self):
        return self.__right
    @property
    def top(self):
        return self.__top
    @property
    def bottom(self):
        return self.__bottom
    @left.setter
    def left(self,L):
        self.__left=L
    @right.setter
    def right(self,R):
        self.__right=R
    @top.setter
    def top(self,T):
        self.__top=T
    @bottom.setter
    def bottom(self,B):
        self.__bottom=B

    @property
    def width(self):
        return self.__right-self.__left
    @property
    def height(self):
        return self.__bottom-self.__top
    @width.setter
    def width(self,W):
        self.__right=self.__left+W
    @height.setter
    def height(self,H):
        self.__bottom=self.__top+H

    def copy(self):
        return XJ_Rect(self.__left,self.__top,self.__right,self.__bottom)
    def __str__(self):
        return 'XJ_Rect'+str((self.__left,self.__top,self.__right,self.__bottom))

    def Neaten(self):
        if(self.__left>self.__right):
            self.__left,self.__right=self.__right,self.__left
        if(self.__top>self.__bottom):
            self.__top,self.__bottom=self.__bottom,self.__top
    def Move(self,x,y):
        self.__left=self.__left+x
        self.__right=self.__right+x
        self.__top=self.__top+y
        self.__bottom=self.__bottom+y
    def IsInside(self,x,y):#判断点是否在矩形内
        return self.__left<=x<=self.__right and self.__top<=y<=self.__bottom
    def GetNearestLines(self,x,y,dist=5):#返回距离点最近的边所对应的首字母，超过距离dist的将不视为“接近”
        '''
            如果边有效则返回对应的首字母，边无效返回None。
            如果位置靠近左边界则会返回'L'，其他边同理。
            如果位置靠近左上顶点则返回'LT'，其他顶点同理。
        '''

        L=abs(self.left-x)
        R=abs(self.right-x)
        T=abs(self.top-y)
        B=abs(self.bottom-y)

        rst=''#查询结果
        if(L<R and L<=dist):
            rst=rst+'L'
        elif(R<L and R<=dist):
            rst=rst+'R'
        if(T<B and T<=dist):
            rst=rst+'T'
        elif(B<T and B<=dist):
            rst=rst+'B'

        if(len(rst)==1):
            if(rst=='L' or rst=='R'):
                T=self.top-y
                B=self.bottom-y
                if(T^B>=0):
                    rst=''
            else:
                L=self.left-x
                R=self.right-x
                if(L^R>=0):
                    rst=''
        if(len(rst)==0):
            return None
        return rst

    def __eq__(self,rect):
        if(type(rect)!=XJ_Rect):
            return False
        return (
            self.left==rect.left and 
            self.right==rect.right and 
            self.top==rect.top and 
            self.bottom==rect.bottom 
        )

if __name__=='__main__':
    r=XJ_Rect(0,0,500,500)
    r.left=300
    r.left=600
    r.width=400
    print(r.copy())





