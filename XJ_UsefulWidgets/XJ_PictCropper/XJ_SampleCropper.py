
__version__='1.0.0'
__author__='Ls_Jan'

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QRect,QPoint,pyqtSignal
from PyQt5.QtGui import QPainter,QPen,QColor,QImage
from PyQt5.QtWidgets import *
from PIL import Image

if(__package__):#如果是通过包导入该模块的话那么就用依赖导入
    from .XJ_AbstractCropper import *
else:
    from XJ_AbstractCropper import *



class XJ_SampleCropper(QWidget):#样例裁剪器，难以对其中的参数进行设置。投入使用还需进一步的封装
    valueChanged=pyqtSignal()#槽信号，裁剪区发生变化时发送信号。不发XJ_Rect是因为裁剪结果有可能是None而导致发不出去

    class Setting:#各种可控设置（因为设置太多了，所以单独列出来存着
        class Setting_Cropper:#裁剪器的设置
            def __init__(self):
                self.rowCnt=3#分割的行数
                self.colCnt=3#分割的列数

                self.color_Shadow=(0,0,0,48)#阴影颜色（裁剪区之外的颜色

                self.color_Border=(255,0,0)#边界颜色
                self.color_Inner=(0,0,255)#内线颜色
                self.thickness_Border=3#边界粗细
                self.thickness_Inner=1#内线粗细

        class Setting_MosaicBg:#马赛克背景的设置
            def __init__(self):
                self.colors=[(255,255,255,255),(190,210,210)]#马赛克颜色
                self.size=4#马赛克大小

        def __init__(self):
            self.cropper=XJ_SampleCropper.Setting.Setting_Cropper()
            self.background=XJ_SampleCropper.Setting.Setting_MosaicBg()

    def __init__(self,parent=None,width=500,height=500):
        super().__init__(parent)
        self.resize(width,height)
        self.setMouseTracking(True)#时刻捕捉鼠标移动

        self.__cropper=XJ_AbstractCropper(0,0,width,height)
        self.__setting=XJ_SampleCropper.Setting()
        self.__aspectRatio=(0,0)#记录宽高比
        self.__smoothCrop=True#记录流畅裁剪
        self.__currArea=None#用于判定裁剪区是否发生变化的，以便发送信号
        self.__fg=QImage(width,height,QImage.Format_ARGB32)
        self.__fg.fill(QColor(0,0,0,0))
        self.__img=Image.fromqimage(self.__fg)#__img的数据类型为PIL.Image.Image。采用该类型是便于和其他数据对接(减少数据转换的负担
        self.__SetMinScale()
        self.CenterPict()#居中图片
        self.UpdateMosaicBg()
        self.update()

    def SetImg(self,PIL_Img):#设置图片(如果图片无效则设置失败，返回False
        if(PIL_Img==None):
            return False
        size=PIL_Img.size
        if(size[0] and size[1]):
            scale1=self.size().width()/size[0]
            scale2=self.size().height()/size[1]
            scale=min(scale1,scale2)
            self.__cropper=XJ_AbstractCropper(0,0,size[0],size[1],scale)
            self.__img=PIL_Img
            self.__fg=PIL_Img.toqimage()        
            self.__SetMinScale()
            self.__cropper.Set_SmoothCrop(self.__smoothCrop)#设置流畅裁剪
            self.__cropper.Set_AspectRatio(self.__aspectRatio)#设置裁剪的宽高比
            self.CenterPict()#居中图片
            self.UpdateMosaicBg()
            self.__UpdateRecord_CurrArea()#更新记录

            return True
        return False

    def Set_SmoothCrop(self,flag):#设置流畅裁剪
        self.__smoothCrop=flag
        self.__cropper.Set_SmoothCrop(flag)#设置流畅裁剪
        self.__UpdateRecord_CurrArea()#更新记录

    def Set_AspectRatio(self,ratio):#设置裁剪的宽高比(二元元组
        self.__aspectRatio=ratio
        self.__cropper.Set_AspectRatio(ratio)#设置裁剪的宽高比
        self.__UpdateRecord_CurrArea()#更新记录

    def Set_CropArea(self,area):#设置裁剪区位置(XJ_Rect)
        self.__cropper.Set_PixelArea_Crop(area)
        self.__UpdateRecord_CurrArea()#更新记录

    def Get_Setting(self):
        return self.__setting

    def Get_Crops(self,split=True):#获取截图(图片类型为PIL.Image.Image)。如果分割split为真则以二维列表(行列)存放，不分割就返回整图。裁剪区不存在则返回None
        pixel=self.__cropper.Get_PixelArea_Crop()
        if(pixel==None):
            return None

        set_cpr=self.__setting.cropper
        width=pixel.width/set_cpr.colCnt
        height=pixel.height/set_cpr.rowCnt
        left=pixel.left
        top=pixel.top
        if(split==False):
            return self.__img.crop((pixel.left,pixel.top,pixel.right,pixel.bottom))

        lst=[]
        for i in range(set_cpr.rowCnt):
            row=[]
            for j in range(set_cpr.colCnt):
                row.append(self.__img.crop(left+width*j,top+height*i,width,height))
            lst.append(row)
        return lst

    def Get_CropArea(self):#获取裁剪区位置(XJ_Rect)
        return self.__cropper.Get_PixelArea_Crop()

    def UpdateMosaicBg(self):#根据self.__fg的大小以及self.__setting.background的参数设置马赛克背景图self.__bg
        set_bg=self.__setting.background
        size=self.__fg.size()
        self.__bg=GetQPixmap(GetMosaicImg((size.width(),size.height()),set_bg.colors,(set_bg.size,set_bg.size))).toImage()
        self.update()

    def MaximizePict(self):#将图片最大化显示
        cpr=self.__cropper

        #设置缩放
        pictSize=self.__fg.size()
        winSize=self.size()
        scale1=winSize.width()/pictSize.width()
        scale2=winSize.height()/pictSize.height()
        scale=min(scale1,scale2)
        cpr.ScalePict(0,0,scale)

        self.CenterPict()#居中图片
        self.update()

    def MaximizeCrop(self):#将裁剪区最大化
        cpr=self.__cropper
        size=cpr.Get_Area_Pict()
        cpr.ClickPict(size.left,size.top)
        cpr.DragCrop(size.right+1,size.bottom+1)
        cpr.ReleaseCrop()
        self.__UpdateRecord_CurrArea()

    def CenterPict(self):#让图片居中
        cpr=self.__cropper
        area=cpr.Get_Area_Pict()
        cpr.ClickPict(area.left,area.top)
        cpr.MovePict((self.width()-area.width)>>1,(self.height()-area.height)>>1)#位置居中


    def __UpdateRecord_CurrArea(self):
        currArea=self.__cropper.Get_PixelArea_Crop()#现在的裁剪结果
        if(self.__currArea!=currArea):#裁剪区发生变化
            self.__currArea=currArea
            self.valueChanged.emit()
        self.update()

    def __SetMinScale(self):#设置最小缩放比(self.__minScale)
        size=self.__fg.size()#图片大小
        self.__minScale=min(self.width()/size.width(),self.height()/size.height())/4#最小缩放比(为组件的1/4宽高)



    def paintEvent(self,event):
        painter=QPainter(self)
        cpr=self.__cropper
        set_cpr=self.__setting.cropper
        pict=cpr.Get_Area_Pict()

        #绘制图片
        qRect=QRect(pict.left,pict.top,pict.width,pict.height)
        painter.drawImage(qRect,self.__bg)
        painter.drawImage(qRect,self.__fg)

        rect=cpr.Get_Area_Crop()
        #绘制裁剪区
        if(rect):
            L=rect.left
            R=rect.right
            T=rect.top
            B=rect.bottom
            W=R-L
            H=B-T

            #画内线
            painter.setPen(QPen(QColor(*set_cpr.color_Inner),set_cpr.thickness_Inner))
            perW=W/set_cpr.colCnt
            perH=H/set_cpr.rowCnt
            for Y in [int(T+n*perH) for n in range(1,set_cpr.rowCnt)]:#画横线
                painter.drawLine(L,Y,R,Y)
            for X in [int(L+n*perW) for n in range(1,set_cpr.colCnt)]:#画纵线
                painter.drawLine(X,T,X,B)

            #画四条边界
            painter.setPen(QPen(QColor(*set_cpr.color_Border),set_cpr.thickness_Border))
            painter.drawRect(L,T,R-L,B-T)

            #绘制阴影(分4块去绘制)
            painter.fillRect(QRect(QPoint(qRect.left(),qRect.top()),QPoint(R,T)),QColor(*set_cpr.color_Shadow))
            painter.fillRect(QRect(QPoint(qRect.right(),qRect.top()),QPoint(R,B)),QColor(*set_cpr.color_Shadow))
            painter.fillRect(QRect(QPoint(qRect.right(),qRect.bottom()),QPoint(L,B)),QColor(*set_cpr.color_Shadow))
            painter.fillRect(QRect(QPoint(qRect.left(),qRect.bottom()),QPoint(L,T)),QColor(*set_cpr.color_Shadow))

    def mouseMoveEvent(self, event):
        x=event.pos().x()
        y=event.pos().y()
        cpr=self.__cropper
        rect=cpr.Get_Area_Crop()
        pict=cpr.Get_Area_Pict()

        if event.buttons() & Qt.MidButton:#按下中键进行拖拽
            cpr.MovePict(x,y)
        elif (event.buttons() & Qt.LeftButton):#按下左键进行拖拽
            cpr.DragCrop(x,y)
        elif(pict.IsInside(x,y)):#修改鼠标光标（鼠标位置要在图片范围内
            if(rect==None):#裁剪区不存在
                self.setCursor(Qt.ArrowCursor)#默认光标
            else:
                lines=rect.GetNearestLines(x,y,5)
                if(lines==None):
                    if(rect.IsInside(x,y)):
                        self.setCursor(Qt.SizeAllCursor)#十字方向箭头
                    else:
                        self.setCursor(Qt.ArrowCursor)#默认光标
                else:
                    if(len(lines)==1):
                        if(lines.count('L') or lines.count('R')):
                            self.setCursor(Qt.SizeHorCursor)#左右箭头
                        else:
                            self.setCursor(Qt.SizeVerCursor)#上下箭头
                    else:
                        if(lines.count('L')):
                            if(lines.count('T')):
                                self.setCursor(Qt.SizeFDiagCursor)#左上箭头
                            else:
                                self.setCursor(Qt.SizeBDiagCursor)#左下箭头
                        else:
                            if(lines.count('T')):
                                self.setCursor(Qt.SizeBDiagCursor)#右上箭头
                            else:
                                self.setCursor(Qt.SizeFDiagCursor)#右下箭头
        else:#鼠标在图片范围外，设置默认光标
            self.setCursor(Qt.ArrowCursor)#默认光标
        event.accept()
        self.__UpdateRecord_CurrArea()#更新记录

    def mousePressEvent(self, event):
        x=event.pos().x()
        y=event.pos().y()
        cpr=self.__cropper
        pict=cpr.Get_Area_Pict()

        if event.button()==Qt.LeftButton:#左键按下瞬间
            cpr.ClickPict(x,y)
        if event.button()==Qt.RightButton:#右键按下瞬间
            cpr.ClearCrop()#清除裁剪区
            self.update()
        if event.button()==Qt.MidButton:#中键按下瞬间
            crop=cpr.Get_Area_Crop()
            cpr.ClickPict(x,y)
            if(crop==None):
                cpr.ClearCrop()
        event.accept()

        self.__UpdateRecord_CurrArea()#更新记录

    def mouseReleaseEvent(self, event):
        if event.button()==Qt.LeftButton:#左键释放
            self.__cropper.ReleaseCrop()
        event.accept()

    def mouseDoubleClickEvent(self,event):
        cpr=self.__cropper
        if event.button()==Qt.MidButton:#中键双击将图片最大化
            crop=cpr.Get_Area_Crop()
            self.MaximizePict()
            cpr.ClickPict(event.pos().x(),event.pos().y())
            if(crop==None):
                cpr.ClearCrop()
        elif event.button()==Qt.RightButton:#右键双击将裁剪区最大化
            self.MaximizeCrop()

    def wheelEvent(self,event):
        x=event.pos().x()
        y=event.pos().y()
        cpr=self.__cropper
        scale=cpr.Get_ScaleRatio()#缩放比

        if(event.angleDelta().y()>0):
            cpr.ScalePict(x,y,scale*1.1)
        elif(scale>0.1):
            cpr.ScalePict(x,y,max(scale*0.9,self.__minScale))
        self.update()
        event.accept()

    def resizeEvent(self,event):
        self.CenterPict()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    cp=XJ_SampleCropper()
    cp.resize(1000,700)
    cp.show()

    cp.Set_AspectRatio((10,16))
    cp.Set_SmoothCrop(True)
#    cp.Set_SmoothCrop(False)
    cp.valueChanged.connect(lambda :print(cp.Get_CropArea()))
    cp.Get_Setting().background.size=1



    def GetAlphaImg_PIL(PIL_Img, alpha = 0.7 ):#给PIL图片附上透明度：https://cloud.tencent.com/developer/article/1740547
          return Image.blend(Image.new('RGBA', PIL_Img.size, (0,0,0,0)), PIL_Img.convert('RGBA'), alpha)


    def GetAlphaImg_QT(img,alpha):#返回一张带有alpha的QImage图片：https://blog.csdn.net/sinat_29175427/article/details/103425812
        img=img.copy()
        p=QPainter()
        p.begin(img)
        p.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        p.fillRect(img.rect(),QColor(0,0,0,alpha))
        p.end()
        return img
    
    
    
    img=QImage(50,108,QImage.Format_RGBA8888)
    img.fill(QColor(0,0,255))
    img=GetAlphaImg_QT(img,192)

    cp.SetImg(GetAlphaImg_PIL(Image.fromqimage(img),0.5))
#    cp.SetImg(None)
#    cp.CenterPict()
#    cp.SetImg(QImage('C:/Users/Administrator/Desktop/XXX.png'))

    sys.exit(app.exec())









