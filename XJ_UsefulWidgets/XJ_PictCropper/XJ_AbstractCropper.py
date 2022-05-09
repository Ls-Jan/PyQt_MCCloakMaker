if(__package__):#如果是通过包导入该模块的话那么就用依赖导入
    from .XJ_Rect import *
    from .XJ_Pair import *
    from .XJ_Tool import *
else:
    from XJ_Rect import *
    from XJ_Pair import *
    from XJ_Tool import *
    
    
class XJ_AbstractCropper:#抽象裁剪器
    def __init__(self,L=0,T=0,Width=0,Height=0,scale=1):#Height和Width为原图宽高，scale为缩放，控制实际显示的图的大小
        if(scale<=0):#不能让它为0
            scale=0.1
        self.__area_pict=XJ_Rect(L,T,L+int(Width*scale),T+int(Height*scale))#显示的图片边界
        self.__area_crop=XJ_Rect()#显示的裁剪边界
        self.__pixelArea_crop=XJ_Rect()#实际的裁剪边界
        self.__pixelArea_crop_copy=XJ_Rect()#鼠标按下时__pixelArea_crop的复制

        self.__pictSize=XJ_Pair(Width,Height)#实际的图片大小（固定值）
        self.__scaleRatio=scale#图片缩放比（原图*scale=显示的图
        self.__aspectRatio=XJ_Pair(0,6)#裁剪的宽高比（有一个为0就为自由裁剪

        self.__pos_click=XJ_Pair(0,0)#鼠标按下时的坐标
        self.__activeLine=''#当前活跃的裁剪区的边
        self.__show=False#显示裁剪区
        self.__smoothCrop=False#当其值为真时，将会流畅裁剪，否则则会严格根据像素进行裁剪

        self.__cropChangable=False#裁剪区可修改

    def ClickPict(self,x,y):#点击图片区（准备裁剪或拖拽
        self.__pos_click=XJ_Pair(x,y)
        self.__cropChangable=True
        if(self.__area_pict.IsInside(x,y)):#在图片区内部
            if(self.__show==False):#如果裁剪区不存在
                pos=self.__GetPixelPos(x,y)
                self.__activeLine='RB'#设置活跃边
                self.__pixelArea_crop=XJ_Rect(pos.x,pos.y,pos.x,pos.y)#设置裁剪区
                self.__pixelArea_crop_copy=self.__pixelArea_crop.copy()#拷贝
#                self.__LimitPixelArea()
#                self.__SetAreaCrop()#设置裁剪区
            else:#裁剪区存在
                self.__activeLine=self.__area_crop.GetNearestLines(x,y,5)#设置活跃边
                if(self.__activeLine):#在裁剪区边界上
                    self.__pixelArea_crop_copy=self.__pixelArea_crop.copy()#复制裁剪区
                elif(self.__area_crop.IsInside(x,y)==True):#在裁剪区内部
                    self.__pixelArea_crop_copy=self.__pixelArea_crop.copy()#复制裁剪区
                else:#在裁剪区外面的无效
                    self.__cropChangable=False
        else:#在图片区外面的无效
            self.__cropChangable=False

    def DragCrop(self,x,y):#左键拖拽裁剪区
        self.__pixelArea_crop=self.__pixelArea_crop_copy.copy()
        pixel=self.__pixelArea_crop
        lines=self.__activeLine
        scale=self.__scaleRatio

        if(self.__cropChangable):#如果点击坐标有效
            self.__show=True
            if(self.__activeLine):#如果活跃边有效，拖拽边
                pos=self.__GetPixelPos(x,y)
                if(lines.find('L')!=-1):
                    pixel.left=pos.x
                elif(lines.find('R')!=-1):
                    pixel.right=pos.x
                if(lines.find('T')!=-1):
                    pixel.top=pos.y
                elif(lines.find('B')!=-1):
                    pixel.bottom=pos.y
            else:#活跃边无效，拖拽裁剪区
                offsetX=int((x-self.__pos_click.x)/scale)
                offsetY=int((y-self.__pos_click.y)/scale)
                pixel.Move(offsetX,offsetY)#移动裁剪区
            self.__LimitPixelArea()#约束裁剪区
            self.__SetAreaCrop()#更新显示的裁剪区

    def ReleaseCrop(self):#左键释放裁剪区
        self.__pixelArea_crop.Neaten()
        self.__area_crop.Neaten()
        self.__pixelArea_crop_copy=self.__pixelArea_crop.copy()#拷贝

    def ClearCrop(self):#清除裁剪区
        self.__show=False

    def ScalePict(self,x,y,newScale):#缩放图片，以坐标(x,y)进行缩放
        if(newScale<=0):
            return

        scale=self.__scaleRatio
        pict=self.__area_pict
        pos=self.__GetPixelPos(x,y)

        size=self.__pictSize
        newPict=XJ_Rect(0,0,int(size.width*newScale),int(size.height*newScale))
        newPict.Move(pict.left,pict.top)
        
        self.__scaleRatio=newScale
        self.__area_pict=newPict
        self.__SetAreaCrop()

        offsetX=int(newScale*pos.x)-(x-pict.left)+1
        offsetY=int(newScale*pos.y)-(y-pict.top)+1
        self.__MovePict(-offsetX,-offsetY)
        
    def MovePict(self,x,y):#移动图片(要先调用ClickPict确定按下点
        self.__MovePict(x-self.__pos_click.x,y-self.__pos_click.y)
        self.__pos_click=XJ_Pair(x,y)

    def __MovePict(self,offsetX,offsetY):#移动图片
        self.__area_pict.Move(offsetX,offsetY)
        self.__area_crop.Move(offsetX,offsetY)

    def Get_Area_Crop(self):#获取显示裁剪区的边界（裁剪区不存在则返回None
        if(self.__show):
            return self.__area_crop
        return None

    def Get_PixelArea_Crop(self):#获取实际裁剪区的边界（裁剪区不存在则返回None
        if(self.__show):
            pixel=self.__pixelArea_crop.copy()
            pixel.Neaten()
            if(pixel.width==0):
                pixel.width=1
            if(pixel.height==0):
                pixel.height=1
            return pixel
        return None

    def Get_Area_Pict(self):#获取显示图片的边界
        return self.__area_pict

    def Get_ScaleRatio(self):#获取缩放比
        return self.__scaleRatio

    def Set_SmoothCrop(self,flag):#设置流畅裁剪
        self.__smoothCrop=flag
        if(flag==False):
            self.__LimitPixelArea()#约束裁剪区
            self.__SetAreaCrop()#更新显示的裁剪区
    
    def Set_AspectRatio(self,ratio:tuple):#设置裁剪的宽高比
        self.__aspectRatio=XJ_Pair(ratio[0],ratio[1])
        preLine=self.__activeLine
        self.__activeLine='RB'
        self.__LimitPixelArea()#约束裁剪区
        self.__SetAreaCrop()#更新显示的裁剪区
        self.__activeLine=preLine

    def Set_PixelArea_Crop(self,area):#设置裁剪区的边界
        if(type(area)==XJ_Rect):
            self.__show=True
            self.__pixelArea_crop=area
            self.__LimitPixelArea()
            self.__SetAreaCrop()
        else:
            self.__show=False
    
    def __GetPixelPos(self,posX,posY):#获取实际的像素位置
        x=int((posX-self.__area_pict.left)/self.__scaleRatio)
        y=int((posY-self.__area_pict.top)/self.__scaleRatio)
        return XJ_Pair(x,y)

    def __LimitPixelArea(self):#执行约束，控制实际裁剪区pixelArea_crop不超出范围+裁剪区长宽比受限
        pixel=self.__pixelArea_crop
        size=self.__pictSize
        aspectRatio=self.__aspectRatio
        lines=self.__activeLine
        if(lines==None):#移动裁剪区
            pass
        else:#更改裁剪区大小
            #记录一下方向，当约束后裁剪区大小为0时恢复为1像素大小
            dictX=pixel.right-pixel.left
            dictY=pixel.bottom-pixel.top
            if lines.count('L'):
                dictX=-dictX
            if lines.count('T'):
                dictY=-dictY
            dictX=1 if dictX>0 else -1
            dictY=1 if dictY>0 else -1

            #约束在图片范围内
            pixel.left=LimitValue(pixel.left,(0,size.width))
            pixel.right=LimitValue(pixel.right,(0,size.width))
            pixel.top=LimitValue(pixel.top,(0,size.height))
            pixel.bottom=LimitValue(pixel.bottom,(0,size.height))
            #如果有长宽约束就进一步处理
            if(aspectRatio.width and aspectRatio.height):
                if(len(lines)==1):
                    if(lines=='L'):
                        lines='LB'
                        pixel.bottom=size.height
                    if(lines=='R'):
                        lines='RB'
                        pixel.bottom=size.height
                    if(lines=='T'):
                        lines='TR'
                        pixel.right=size.width
                    if(lines=='B'):
                        lines='BR'
                        pixel.right=size.width

                W=pixel.right-pixel.left
                H=pixel.bottom-pixel.top
                maxW=size.width-(pixel.left if lines.count('R') else pixel.right)
                maxH=size.height-(pixel.top if lines.count('B') else pixel.bottom)
                rateW=abs(W/aspectRatio.width)
                rateH=abs(H/aspectRatio.height)
                rateMaxW=abs(maxW/aspectRatio.width)
                rateMaxH=abs(maxH/aspectRatio.height)
                
                if(self.__smoothCrop==False):
                    rateW=int(rateW)
                    rateH=int(rateH)
                    rateMaxW=int(rateMaxW)
                    rateMaxH=int(rateMaxH)
                    
                rate=min(max(rateW,rateH),min(rateMaxW,rateMaxH))#从中选取最大的裁取比(约束在图片范围内
                rate=min(rateW,rateH)
                W=int(aspectRatio.width*rate *(1 if W>0 else -1))
                H=int(aspectRatio.height*rate *(1 if H>0 else -1))

                if(lines.find('L')!=-1):
                    pixel.left=pixel.right-W
                else:
                    pixel.right=pixel.left+W
                if(lines.find('T')!=-1):
                    pixel.top=pixel.bottom-H
                else:
                    pixel.bottom=pixel.top+H
            
            if(pixel.width==0):#如果长度为0，那么就需要弄成1像素大小
                pixel.width=dictX
            if(pixel.height==0):
                pixel.height=dictY
                

        #约束在图片范围内
        pixel.Neaten()
        if(pixel.left<0):
            pixel.Move(-pixel.left,0)
        if(pixel.right>size.width):
            pixel.Move(size.width-pixel.right,0)
        if(pixel.top<0):
            pixel.Move(0,-pixel.top)
        if(pixel.bottom>size.height):
            pixel.Move(0,size.height-pixel.bottom)
            
    def __SetAreaCrop(self):#设置self.__area_crop
        pixel=self.__pixelArea_crop.copy()
        pixel.Neaten()
        pict=self.__area_pict
        scale=self.__scaleRatio
        
        L=int(scale*pixel.left)+pict.left
        T=int(scale*pixel.top)+pict.top
        R=int(scale*pixel.right)+pict.left
        B=int(scale*pixel.bottom)+pict.top
        self.__area_crop=XJ_Rect(L,T,R,B)



if __name__=='__main__':
    pass








