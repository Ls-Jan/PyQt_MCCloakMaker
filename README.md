# PyQt_MCCloakMaker

MC披风生成器

运行效果图：

<img src="https://github.com/Ls-Jan/PyQt_MCCloakMaker/blob/main/RunningDisplay%5BPNG%2CGIF%2CMP4%5D/0.gif"/>

</br>
</br>
</br>

***

其实怎么说呢，“就这？这都写了老半天？写几个星期？”</br>
而且在对偏大的图片时还会出现一点卡顿(产生卡顿的地方该交给其他线程去执行，也就是多线程，但mole)

</br>


然后附上我同学几个月前写的网页版披风生成器，只不过因为他不怎么想搞界面所以就看上去不太行的亚子：<a href="https://lraty-li.github.io/Minecraft-Cape-Generator/">Minecraft Crap</a></br>
不想下载exe的(只不过也不怎么建议下载就是了，毕竟做那么久就这玩意儿是有点丢人)，可以将就着用我同学的，他有心情的话估计会把界面做好。</br>
想下载使用本生成器的请点击<a href="https://github.com/Ls-Jan/PyQt_MCCloakMaker/releases/download/v1.0.0/MC_CloakMaker.zip">  XJ_MCCloakMaker  </a>，把那100M+的压缩包下载然后解压，在里头找Main.exe文件运行一下就行了。

</br>
</br>

***
本项目使用的模块：</br>
·Pyqt5</br>
·cv2</br>
·numpy</br>
·PIL</br>

即：如果你装了py3并且也装了上面模块的话，直接下载项目里的py脚本文件并运行Main.py就好了。</br>
为了减少不必要的麻烦，我把那些脚本文件归档到<a href="https://github.com/Ls-Jan/PyQt_MCCloakMaker/blob/main/MC_CloakMaker%5BPyQt%5D%E8%84%9A%E6%9C%AC.zip"> MC_CloakMaker[PyQt]脚本.zip </a> 里头了。

</br>
</br>
</br>

***
因为写的过程中，几个月前写好的Qt组件发现不好用(死了几个月的代码突然攻击我)，然后迫不得已只能改，然后心态爆炸后缓了好些天(也就是进度慢了差不多一周)。</br>
本来我这披风我预期是两星期不到就做完的(因为有之前<a href="https://github.com/Ls-Jan/PyTkinter_MC_CloakMaker"> 基于tkiner的披风编辑器 </a>的经验)，但结果却是花那么久时间是挺值得反思的。</br>
</br>

自己写的3D显示(XJ_3DViewer)说实话不好用(而且我也没啥想法去修它...)，想用该组件的请三思...</br>
因为这东西涉及到图形学，但我又只学了个皮毛都不算的东西，所以这3D显示自然好不到哪儿去，其中之一的问题是：使用本生成器时那3D显示卡在一些极特定的角度时小概率出现显示的不正确。</br>
其他组件(裁剪器XJ_PictCropper啥的)我觉得没太大使用上的问题，有需要的同学可以拷走使用。
</br>
</br>

***
最后的最后，放一下LittleSkin的传送门：<a href="https://littleskin.cn/skinlib">皮肤库-LittleSkin</a>


