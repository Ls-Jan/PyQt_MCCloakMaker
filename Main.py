from XJ_MCCloakMaker import *

import sys
#from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtWidgets import QVBoxLayout,QMenuBar,QMenu,QMessageBox,QTextEdit,QDialog,QLabel

#构建菜单栏的部分参考(多半是转载+机翻的)：https://www.cnblogs.com/huaweiyun/p/15196404.html
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__cloakMaker=XJ_MCCloakMaker(self)
        self.setWindowTitle('MC披风生成器')
        self.setCentralWidget(self.__cloakMaker)
        self.resize(1400, 600)
        self.__SetMenuBar()

    def __SetMenuBar(self):
        maker=self.__cloakMaker
        maker.SwitchCropper(3)

        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)


        #【文件】
        menuA=QMenu("文件",self)
        menuA.addAction("保存披风",(lambda maker:lambda :maker.SaveCloak())(maker))#使用闭包防万一
        menuA.addAction("读取披风",(lambda maker:lambda :maker.LoadCloak())(maker))


        #【裁剪器窗口】
        actionListB=[]#真麻烦，净用些奇怪的方法来实现奇怪的功能（闭包暂时的神
        menuB=QMenu("切换裁剪窗口",self)
        actionListB.append(menuB.addAction("双面-前后",(lambda maker,lst:lambda :[lst[pst].setChecked(pst==0) for pst in range(4)] and maker.SwitchCropper(0))(maker,actionListB)))#用歪门邪道在lambda中执行循环语句
        actionListB.append(menuB.addAction("双面-左右",(lambda maker,lst:lambda :[lst[pst].setChecked(pst==1) for pst in range(4)] and maker.SwitchCropper(1))(maker,actionListB)))
        actionListB.append(menuB.addAction("双面-上下",(lambda maker,lst:lambda :[lst[pst].setChecked(pst==2) for pst in range(4)] and maker.SwitchCropper(2))(maker,actionListB)))
        menuB.addSeparator()
        actionListB.append(menuB.addAction("三面-自动",(lambda maker,lst:lambda :[lst[pst].setChecked(pst==3) for pst in range(4)] and maker.SwitchCropper(3))(maker,actionListB)))
        for a in actionListB:
            a.setCheckable(True)
        actionListB[3].setChecked(True)


        #【帮助】
        menuC=QMenu("帮助",self)
        menuC.addAction("使用帮助",self.__Help_Use)
        menuC.addAction("版本",self.__Help_Version)


        menuBar.addMenu(menuA)
        menuBar.addMenu(menuB)
        menuBar.addMenu(menuC)



    def __Help_Version(self):
        QMessageBox.information(self,'MC披风','版本：v1.0\n开发者：LsJan')

    def __Help_Use(self):
        dlg=QDialog(self)

        text=QTextEdit(dlg)
        text.setReadOnly(True)
        text.setStyleSheet("font-size:18px;")
        text.append("本软件可以方便快捷地生成MC披风文件。在此制作属于自己的披风吧。")
        text.append("下面是软件使用说明")
        text.append("")
        text.append("")
        text.append("1、左侧的是3维显示器，其下方的“分辨率”可以对披风的总分辨率进行修改。")
        text.append("")
        text.append("2、右侧的是裁剪器，用于对披风的各个面进行修改。其下方有若干组件：")
        text.append("   滑动条为图片的透明度")
        text.append("   复选框为比例裁剪")
        text.append("   选图按钮用于选择图片")
        text.append("   纯色按钮用于设置纯色图片")
        text.append("")
        text.append("")
        text.append("·3维显示器的相关操作：")
        text.append("··左键拖拽改变视角")
        text.append("··中键滚轮缩放画面")
        text.append("")
        text.append("·裁剪器的相关操作：")
        text.append("··左键拖拽选取/拖拽裁剪区域")
        text.append("··中键拖拽移动画布")
        text.append("··中键滚轮缩放画布")
        text.append("··中键双击将画布归位")
        text.append("··右键单击撤销裁剪区域")
        text.append("··右键双击将最大化选取裁剪区域")
        text.append("")

        vbox=QVBoxLayout(dlg)
        vbox.addWidget(text)

        dlg.setWindowTitle("使用帮助")
        dlg.resize(800,400)
        dlg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win=Main()
    win.show()

    sys.exit(app.exec())



