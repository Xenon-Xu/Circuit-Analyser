"""
    改编自github上的Matplotlibwidget框架，在基于Matplotlib库之上于Pytq5界面中嵌入绘图框架
    原开源代码网址：https://github.com/cxinping/PyQt5/blob/master/Chapter09/MatplotlibWidget.py """

import sys
import random
import matplotlib

matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import analysis

draw_port = 0  # 绘制的端口
draw_length_x = 100  # 横坐标长度
draw_interval = 1000  # 绘图横向步间隔（防止绘图点过密而卡死）

class MyMplCanvas(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#19232D')  # 新建一个figure
        self.axes = self.fig.add_subplot(111, facecolor='#29333D')  # 建立一个子图，如果要建立复合图，可以在这里修改
        # self.axes.hold(False)  # 每次绘图的时候不保留上一次绘图的结果(新版本取消)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    '''绘制静态图，可以在这里定义自己的绘图逻辑'''

    def start_static_plot(self):
        self.axes.clear()
        self.fig.suptitle('测试静态图')
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s, 'deepskyblue')
        self.axes.set_ylabel('静态图：Y轴')
        self.axes.set_xlabel('静态图：X轴')
        self.axes.grid(True)
        self.draw()

    '''启动绘制动态图'''

    def start_dynamic_plot(self):
        timer = QtCore.QTimer(self)
        self.axes.clear()
        timer.timeout.connect(self.update_figure)  # 每隔一段时间就会触发一次update_figure函数。
        timer.start(100)  # 触发的时间间隔为100ms

    '''动态图的绘图逻辑可以在这里修改 （已修改逻辑）'''

    def update_figure(self):
        list_y = analysis.extract_voltage_answer(draw_port, draw_length_x, draw_interval)
        if len(list_y) == 1:
            list_x = [0]
        elif len(list_y) < int(draw_length_x/draw_interval) + 1:
            list_x = [(i + analysis.lzy_times * analysis.lzy) * analysis.dt for i in range(0, analysis.temp_step, draw_interval)]
        else:
            list_x = [(i + analysis.lzy_times * analysis.lzy) * analysis.dt for i in range(analysis.temp_step-draw_length_x, analysis.temp_step, draw_interval)]

        # print(len(list_x), len(list_y))
        self.axes.clear()
        self.fig.suptitle('Voltage', color='white')
        self.axes.plot(list_x, list_y, 'deepskyblue')
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')
        self.axes.set_ylabel('Voltage / V', color='white')
        self.axes.set_xlabel('Time / s', color='white')
        self.axes.grid(True)
        self.draw()



class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=5, height=4, dpi=100)
        # self.mpl.start_static_plot() # 如果你想要初始化的时候就呈现静态图，请把这行注释去掉
        #self.mpl.start_dynamic_plot() # 如果你想要初始化的时候就呈现动态图，请把这行注释去掉
        self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar

        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    ui.mpl.start_static_plot()  # 测试静态图效果
    # ui.mpl.start_dynamic_plot() # 测试动态图效果
    ui.show()
    sys.exit(app.exec_()) 