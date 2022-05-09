import cv2.cv2 as cv2
import numpy as np
from PIL import Image

def GetMosaicImg(shape,colors,interval):#返回马赛克图片（np二维数组
    '''
        shape为二元组，（图片宽,图片高）
        colors为二元组，（方块颜色1，方块颜色2）
        interval为二元组，（单方块宽，单方块高）
    '''
    #对color的值进行处理
    clr0=list(colors[0])
    clr1=list(colors[1])
    len0=len(clr0)
    len1=len(clr1)
    if(len0<len1):
        tmp=list(clr0)
        for i in range(len0,len1):
           tmp.append(colors[1][i])
        clr0=list(tmp)
    if(len0>len1):
        tmp=list(clr1)
        for i in range(len1,len0):
           tmp.append(colors[0][i])
        clr1=list(tmp)
    #因为cv2发神经，喜欢弄成bgr，平时都是rgb的，所以得调换一下
    if(len(clr0)>=3):
        clr0[0],clr0[2]=clr0[2],clr0[0]
        clr1[0],clr1[2]=clr1[2],clr1[0]
    
    #生成马赛克图案
    h=interval[1]
    w=interval[0]
    mosaic=np.zeros((h*2,w*2,len(clr0)),dtype=np.uint8)
    cv2.rectangle(mosaic,(0,0),(w,h),clr0,-1)
    cv2.rectangle(mosaic,(w,0),(w*2,h),clr1,-1)
    cv2.rectangle(mosaic,(0,h),(w,h*2),clr1,-1)
    cv2.rectangle(mosaic,(w,h),(w*2,h*2),clr0,-1)
    while(w<shape[0]):#从行开始，生成一行的马赛克
        mosaic=np.concatenate((mosaic,mosaic), axis=1)
        w=w*2
    while(h<shape[1]):#利用一行马赛克生成一片马赛克
        mosaic=np.concatenate((mosaic,mosaic), axis=0)
        h=h*2
    
    return mosaic[0:shape[1],0:shape[0]]#把这破事忘了。图片需要裁剪才行要不然大小不对
    #【注释掉的是旧算法，利用颜色填充逐个格子填色，效率非常低】
#    img=np.zeros((shape[1],shape[0],len(clr0)),dtype=np.uint8)
#    for i in range(int(shape[0]/interval[0])+1):
#        for j in range(int(shape[1]/interval[1])+1):
#            left=i*interval[0]
#            top=j*interval[1]
#            right=left+interval[0]
#            bottom=top+interval[1]
#            color=clr0 if (i+j)&1==0 else clr1
#            cv2.rectangle(img,(left,top),(right,bottom),color,-1)
#    return img
    

def FixImgs(cvFg,cvBg):#以cvFg的透明度作为蒙版将cvBg融合进去
    Bg_b,Bg_g,Bg_r=cv2.split(cvBg)
    Fg_b,Fg_g,Fg_r,Fg_a=cv2.split(cvFg)#alpha的值越大越不透明，越小才越透明
    Bg_Mask=np.invert(Fg_a)
    bg=cv2.merge((
        np.bitwise_and(Bg_b,Bg_Mask),
        np.bitwise_and(Bg_g,Bg_Mask),
        np.bitwise_and(Bg_r,Bg_Mask)))
    fg=cv2.merge((
        np.bitwise_and(Fg_b,Fg_a),
        np.bitwise_and(Fg_g,Fg_a),
        np.bitwise_and(Fg_r,Fg_a)))
    pict=cv2.add(fg,bg)
    return pict

def GetQPixmap(cvImg):#从cv的图片类型转成QT的QPixmap类型
    cvImg=cv2.cvtColor(cvImg, cv2.COLOR_BGRA2RGBA)
    im = Image.fromarray(cvImg)
    return im.toqpixmap()

def GetAlphaQImage(qImg,alpha):#设置qImg的透明度：https://blog.csdn.net/sinat_29175427/article/details/103425812
    p=QPainter()
    p.begin(qImg)
    p.setCompositionMode(QPainter.CompositionMode_DestinationIn)
    p.fillRect(qImg.rect(),QColor(0,0,0,alpha))
    p.end()


def LimitValue(val,section):#将val的值控制在区间section内（包含边界）
    if(section[0]>section[1]):
        section=(section[1],section[0])
    return section[0] if val<section[0] else section[1] if val>section[1] else val

def InTheSection(val,section):#判断val是否在区间section内（包含边界）
    if(section[0]>section[1]):
        section=(section[1],section[0])
    return section[0]<=val<=section[1]




if __name__=='__main__':
    img=GetMosaicImg((500,500),((255,255,128),(128,128,255)),(110,110))
    cv2.imshow('',img)
    cv2.waitKey()
    
