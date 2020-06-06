"""
    自定义电路图绘画模块
            """


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, \
    QWidget, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QPainter, QPen, QColor
import analysis

class DrawView(QWidget):

    def __init__(self, parent=None):
        super(DrawView, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mcv = myCircuitView(self)
        self.layout.addWidget(self.mcv)

class myCircuitView(QGraphicsView):


    def __init__(self, parent=None):
        super(myCircuitView, self).__init__(parent)
        self.wire_num = 0  # 记录线的个数
        self.selectedItem = None  # 记录选中的图元
        self.elementsItemList = list()  # 记录元件图元
        self.angle = list()
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0  # 画线位置缓冲
        self.obstacle = False  # 死循环阻塞

    def set_wire_num(self, tnum):
        self.wire_num = tnum

    def set_elementsItemList(self, tlist):
        self.elementsItemList = tlist

    def setScene(self, QGraphicsScene):
        """重载场景设置，并增加旋转度数列表"""
        QGraphicsView.setScene(self, QGraphicsScene)
        self.angle = [0 for i in range(len(analysis.elements))]

    def paintEvent(self, QPaintEvent):
        """重定义绘画事件"""
        if self.obstacle:  # 阻塞
            return
        QGraphicsView.paintEvent(self, QPaintEvent)  # 保留原有绘画事件
        remove_times = 0
        self.obstacle = True  # 死循环阻塞
        for obj in self.scene().items():  # 删除连线的图像元
            if remove_times >= self.wire_num:
                break
            self.scene().removeItem(obj)
            remove_times += 1
        self.drawLine()

    def mousePressEvent(self, event):
        """鼠标左键选择图元"""
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:  # 判断鼠标右键点击
            item = self.get_item_at_click(event)
            if isinstance(item, QGraphicsPixmapItem):  # 判断点击对象是否为图元的实例
                self.selectedItem = item

    def get_item_at_click(self, event):
        """获取点击位置的图元，无则返回None"""
        pos = event.pos()
        item = self.itemAt(pos)
        return item

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            if isinstance(self.selectedItem, QGraphicsPixmapItem):  # 判断点击对象是否为图元的实例
                self.rotate_item(self.selectedItem)

    def rotate_item(self, item):
        """旋转所选元件"""
        t_num = select_num = 0  # 记录所选元件
        t_items = self.scene().items()[::-1]
        for ele in t_items:
            if ele is item:
                select_num = t_num
                break
            else:
                t_num += 1
        self.angle[select_num] += 90
        self.angle[select_num] %= 360
        item.setRotation(self.angle[select_num])


    def drawLine(self):
        """绘制连线"""
        itemsPosList = list()  # 记录元件位置
        t_items = self.scene().items()[::-1]
        for item in t_items:
            if isinstance(item, QGraphicsPixmapItem):
                itemsPosList.append((int(item.x()), int(item.y())))
        for node in analysis.nodes:
            node_port = node.ports()
            for i in range(len(node_port) - 1):
                port1 = node_port[i]
                port2 = node_port[i + 1]
                ele1 = analysis.NODES.port2element(port1)
                ele2 = analysis.NODES.port2element(port2)
                if self.angle[ele1] == 0:
                    self.x1, self.y1 = itemsPosList[ele1][0] + 40, itemsPosList[ele1][1] + 16
                    if not analysis.NODES.is_positive(port1):
                        self.y1 += 200 - 25
                elif self.angle[ele1] == 90:
                    self.x1, self.y1 = itemsPosList[ele1][0] + 9 - 60, itemsPosList[ele1][1] + 40 + 60
                    if not analysis.NODES.is_positive(port1):
                        self.x1 += 200 - 25
                elif self.angle[ele1] == 180:
                    self.x1, self.y1 = itemsPosList[ele1][0] + 40, itemsPosList[ele1][1] + 9
                    if analysis.NODES.is_positive(port1):
                        self.y1 += 200 - 25
                elif self.angle[ele1] == 270:
                    self.x1, self.y1 = itemsPosList[ele1][0] + 16 - 60, itemsPosList[ele1][1] + 40 + 60
                    if analysis.NODES.is_positive(port1):
                        self.x1 += 200 - 25

                if self.angle[ele2] == 0:
                    self.x2, self.y2 = itemsPosList[ele2][0] + 40, itemsPosList[ele2][1] + 16
                    if not analysis.NODES.is_positive(port2):
                        self.y2 += 200 - 25
                elif self.angle[ele2] == 90:
                    self.x2, self.y2 = itemsPosList[ele2][0] + 9 - 60, itemsPosList[ele2][1] + 40 + 60
                    if not analysis.NODES.is_positive(port2):
                        self.x2 += 200 - 25
                elif self.angle[ele2] == 180:
                    self.x2, self.y2 = itemsPosList[ele2][0] + 40, itemsPosList[ele2][1] + 9
                    if analysis.NODES.is_positive(port2):
                        self.y2 += 200 - 25
                elif self.angle[ele2] == 270:
                    self.x2, self.y2 = itemsPosList[ele2][0] + 16 - 60, itemsPosList[ele2][1] + 40 + 60
                    if analysis.NODES.is_positive(port2):
                        self.x2 += 200 - 25

                self.scene().addLine(self.x1, self.y1, self.x2, self.y2, QColor(0, 191, 255))
                self.obstacle = False  # 阻塞解除


# if __name__ == '__main__':
#     import sys
#     app = QApplication(sys.argv)
#     myWin = DrawView()
#     myWin.setFixedSize(500, 500)
#     myWin.show()
#     sys.exit(app.exec_())