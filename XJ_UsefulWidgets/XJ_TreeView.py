
__version__='1.0.0'
__author__='Ls_Jan'

import sys
from functools import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt,QModelIndex,QItemSelectionModel,pyqtSignal,QMimeData,Qt,QPoint
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QDrag
from PyQt5.QtWidgets import *

__all__=['XJ_TreeView']


#拖拽功能浑身上下都是bug，属实是不敢恭维，爷怕了爷怕了。功能做的可真是个垃圾，大写的服，一晚上七八个小时全喂狗了
#什么？让我重写拖拽事件？当我时间很多是吧。这本身就不该用户完成的细节这苟QT为啥不做好，非得留这些破手尾，反正一晚上时间算是白糟蹋了，真的恶心
class XJ_TreeView(QTreeView):
    class XJ_Iter:
        def __init__(self,iter):
            self.__iter=iter

        def AppendRow(self,data):#添加数据(一个列表
            lst=[]
            for i in data:
                lst.append(QStandardItem(str(i)))
                lst[-1].setEditable(False)
            self.__iter.appendRow(lst)
            return XJ_TreeView.XJ_Iter(lst[0])
        
        def Copy(self):
            return XJ_TreeView.XJ_Iter(self.__iter)
            
        def Back(self):#返回上一级(返回失败则返回false
            if(type(self.__iter)==QStandardItemModel):
                return False
            if(self.__iter.parent()==None):
                self.__iter=self.__iter.model()
            else:
                self.__iter=self.__iter.parent()
            return True
            
        def Next(self,i):#进入下一级(进入失败则返回false
            if(0<=i<self.__iter.rowCount()):
                if(type(self.__iter)!=QStandardItemModel):
                    self.__iter=self.__iter.child(i,0)
                else:
                    self.__iter=self.__iter.itemFromIndex(self.__iter.index(i,0))
                return True
            else:
                return False
                
        def GetData(self):#获取数据(一个列表
            if(type(self.__iter)!=QStandardItem):
                return None
            result=[]
            model=self.__iter.model()
            index=self.__iter.index().siblingAtColumn(0)
            i=1
            while(index.isValid()):
                result.append(model.itemFromIndex(index).text())
                index=index.siblingAtColumn(i)
                i+=1
            return result
            
        def SetData(self,i,data):#设置第i个单元格的内容(设置失败则返回false
            if(type(self.__iter)==QStandardItemModel):
                return False
            model=self.__iter.model()
            index=self.__iter.index().siblingAtColumn(i)
            if(index.isValid()==False):
                return False
            item=model.itemFromIndex(index)
            item.setText(str(data))
            return True
            
        def SetFont(self,i,font):#设置第i个单元格的字体样式(设置失败则返回false
            if(type(self.__iter)==QStandardItemModel):
                return False
            model=self.__iter.model()
            index=self.__iter.index().siblingAtColumn(i)
            item=model.itemFromIndex(index)
            item.setFont(font)
            return True
        
        def SetCheckable(self,flag):#设置是否显示复选框(设置失败则返回false)。复选框为双态
            if(type(self.__iter)==QStandardItemModel):
                return False
            self.__iter.setCheckable(flag)
            if(flag==False):
                self.__iter.setCheckState(-1)
            return True
            
        def GetCheckable(self):#获取复选框状态(如果获取失败则返回false)，返回结果为：【全选：Qt.Checked(2)、部分选：Qt.PartiallyChecked(1)、不选：Qt.Unchecked(0)】
            if(type(self.__iter)==QStandardItemModel):
                return None
            return self.__iter.checkState()
        
        def SetEditable(self,i,flag):#设置第i个单元格可以双击修改(设置失败则返回false
            if(type(self.__iter)==QStandardItemModel):
                return False
            model=self.__iter.model()
            index=self.__iter.index().siblingAtColumn(i)
            item=model.itemFromIndex(index)
            item.setEditable(flag)
            return True

    doubleClicked=pyqtSignal(XJ_Iter)#槽信号，当前行双击时发送信号（如果行未发生变化则不发送
    rightClicked=pyqtSignal(list)#槽信号，右键时触发(多用于右键的自定义菜单)，发送已经选中的行（元素为XJ_Iter

    def __init__(self,parent=None):
        super(XJ_TreeView, self).__init__(parent)
        model=QStandardItemModel(self)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)#支持Shift、Ctrl多选
#        self.setContextMenuPolicy(Qt.CustomContextMenu)#设置右键菜单策略。【说实话，没用，还不如修改鼠标单击事件】
        self.setModel(model)
        self.headerLables=[]
        self.__currIndex=None#记录双击选中的行
        self.SetDragable(True)#设置拖拽
        self.setDragDropMode(QAbstractItemView.InternalMove)#设置拖拽为移动而不是复制。默认模式是DragDrop(复制模式)
    def SetDragable(self,flag):#设置可否拖拽
        self.setDragEnabled(flag)#开启向外拖拽
        self.setAcceptDrops(flag)#开启接收拖拽
#        self.setDropIndicatorShown(flag)#显示拖拽位置【感觉这东西没用】


#    def dragEnterEvent(self, event):#【一】【拖拽进入组件内部时调用，判断该拖拽是否可accept，当accept后会进入dragMoveEvent】
#        if(event.source()==self):#仅接收控件内的拖拽，来自外部的拖拽一律禁止
#            event.accept()
    def dragMoveEvent(self, event):#【二】【成功进入到控件内部，在不停的拖拽中被反复调用直到鼠标松开。当event.ignore()时鼠标光标为禁止图标，并且释放拖拽并不会进入到dropEvent中】
        index=self.indexAt(event.pos())
        if(index.column()==0):#王八蛋个狗日东西，垃圾的要死。如果拖到非第一列的地方释放的话会出现数据丢失或者数据错位的情况，蠢得要死真的是绝了这啥破玩意儿
            event.accept()
        else:
            event.ignore()
    def dropEvent(self, event):#【三】【拖拽释放时调用】
        #个凑垃圾QTreeView，简直就是shi，做的啥玩意儿，封装一半不封装一半的，有些巴不得拿到手的功能找几十年结果是不暴露出来的是不是有病？
        super().dropEvent(event)
        
        
    
    
    def GetHead(self):#返回根部迭代器
        return XJ_TreeView.XJ_Iter(self.model())
    def GetCurrIter(self):#获取当前行的迭代器
        return XJ_TreeView.XJ_Iter(self.model().itemFromIndex(self.currentIndex()))
    def GetCursorIter(self,pos:QPoint):#获取坐标(一般传入鼠标坐标)对应行的迭代器
        XJ_TreeView.XJ_Iter(self.model().itemFromIndex(self.indexAt(pos)))
    def GetCurrIters(self):#获取当前选中行的迭代器
        d={i.row():i for i in self.selectedIndexes()}#好死不死，它是按单元格来的，不是按行，所以有了看似多此一举的操作
        return [XJ_TreeView.XJ_Iter(self.model().itemFromIndex(i)) for i in d.values()]
    def Clear(self):
        width=[]
        for i in range(self.model().columnCount()):
            width.append(self.columnWidth(i))
        self.model().clear()
        self.model().setHorizontalHeaderLabels(self.headerLables)
        for i in range(len(width)):
            self.setColumnWidth(i,width[i])
    def SetHeaderLabels(self,labels):#设置列头
        self.headerLables=labels
        self.model().setHorizontalHeaderLabels(labels)
        
    def mouseDoubleClickEvent(self,event):
        if(event.buttons() & Qt.LeftButton):#如果是左键
            currIndex=self.currentIndex()
            self.setCurrentIndex(currIndex)
            
            if(self.__currIndex!=currIndex):
                self.__currIndex=currIndex
                self.doubleClicked.emit(self.GetCurrIter())
        else:
            super().mouseDoubleClickEvent(event)
        event.accept()
        
    def mousePressEvent(self,event):
        if(event.buttons() & Qt.LeftButton):#如果是左键
            super().mousePressEvent(event)
        elif (event.buttons() & Qt.RightButton):#如果是右键
            self.rightClicked.emit(self.GetCurrIters())
        event.accept()

    


if __name__ == '__main__':
    app = QApplication(sys.argv)

    tv=XJ_TreeView()
    tv.show()
    
    iter=tv.GetHead()
    iter.AppendRow(['AAA','333']).AppendRow(['AAAAA','00000'])
    iter.AppendRow(['BBB','222'])
    iter.AppendRow(['CCC','111'])
    iter.AppendRow(['XXX','xxx'])
    iter.AppendRow(['YYY','yyy'])
    iter.AppendRow(['ZZZ','zzz'])
    
    
    tv.CurrentChanged=lambda line:print(line.GetData())
    tv.rightClicked.connect(lambda lst:[print(line.GetData()) for line in lst])
    tv.doubleClicked.connect(lambda line:print(line.GetData()))
    sys.exit(app.exec())


