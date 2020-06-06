# -*- coding: utf-8 -*-

import sys, math
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QMessageBox, QTableWidgetItem,\
    QAbstractItemView, QHeaderView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QPainter, QColor, QFont, QDoubleValidator, QIntValidator, QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from MainWindow import Ui_MainWindow
from AddComponentsWindow import Ui_AddComponentsDialog
from EditComponentWindow import Ui_EditComponentWin
import Matplotlibwidget
import analysis, threading, copy, cv2

time_width = 0.5  # 波形显示秒数
interval_adjust = 1  # 越大图像越精细（以1为界，>=0）
nameSet = set()  # 确保器件名字不重复

def _thread_it(func, *args):
    """多线程防卡死"""
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()

class MyMainWindow(QMainWindow, Ui_MainWindow):
    """主窗口"""

    sendToEditSignal = pyqtSignal(int, str)  # 向编辑元件值的窗口发送选中元件的序号、名称

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowState(Qt.WindowMaximized)
        self.RunButton.clicked.connect(self.RunButton_click)
        self.StopButton.clicked.connect(self.StopButton_click)
        self.AddComponentsButton.clicked.connect(self.addWindowShow)

        """变量初始化"""
        self.selectComponent = self.selectConnection = 0  # 当前鼠标选择元件行数
        self.connectionsSet = list()  # 连接的预处理列表
        self.sentMessage = 0  # 发送的显示信息数量

        """仿真运行后，不能动的控件"""
        self.criticalList = [self.AddComponentsButton, self.DeleteComponentsButton, self.ClearComponentsButton,
                                   self.AddConnectionsButton, self.DeleteConnectionsButton, self.ClearConnectionsButton,
                                   self.SwitchPushButton, self.ConstructConnectionsButton, self.GroundLineEdit,
                             self.EditComponentButton]

        self.tableWidgetComponents.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 表格设置
        self.tableWidgetComponents.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetConnentions.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidgetConnentions.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.addComponentsWin = AddComponentsWindow(self)  # 子窗口设置
        self.editComponentWin = EditComponentsWindow(self)

        self.addComponentsWin.addWinSignal.connect(self.addWindowAdjust)  # 信号绑定设置
        self.editComponentWin.editWinSignal.connect(self.editWindowAdjust)
        self.sendToEditSignal.connect(self.editComponentWin.update_unit)

        self.portValuePrecision = QIntValidator(self)  # 精度控制
        self.portValuePrecision.setRange(0, 0)

        self.Port1LineEdit.setValidator(self.portValuePrecision)
        self.Port2LineEdit.setValidator(self.portValuePrecision)
        self.GroundLineEdit.setValidator(self.portValuePrecision)

        self.scene = QGraphicsScene()  # 创建场景
        self.CircuitViewer.mcv.setScene(self.scene)  # 将场景添加至视图

        LabelUpdateTimer = QTimer(self)  # 更新计时器
        LabelUpdateTimer.timeout.connect(self.main_update)
        LabelUpdateTimer.start(100)  # 0.1秒更新一次

        self.TimeRangeLabel.setAlignment(Qt.AlignCenter)  # 示波器相关设置
        self.TimeRangeLineEdit.setAlignment(Qt.AlignCenter)

        self.lengthx_interval_upgrade()
        self.WavePlot.mpl.start_dynamic_plot()  # 开启绘图循环，横轴长度为time_width

    def main_update(self):
        """界面值显示更新的大汇总"""
        self.label_update()
        self.PortLineEdit_setValue()
        self.draw_port_update()

    def draw_port_update(self):
        """示波器绘制端口的更新"""
        if self.PortViewComboBox.count() > 0:
            Matplotlibwidget.draw_port = eval(self.PortViewComboBox.currentText())

    def lengthx_interval_upgrade(self):
        """示波器宽度和进度值更新"""
        global time_width, interval_adjust
        time_width = self.TimeRangeHorizontalSlider.value() / 1000
        interval_adjust = self.PrecisionHorizontalSlider.value() / 1000 + 0.001
        Matplotlibwidget.draw_length_x = int(time_width / analysis.dt)
        t_precise_num = int(time_width / analysis.dt / (100 ** interval_adjust))
        if t_precise_num <= 1000:
            Matplotlibwidget.draw_interval = t_precise_num
        else:
            Matplotlibwidget.draw_interval = 1000

    def label_update(self):
        """更新示波器相关值的显示值"""
        global time_width
        self.TimesLineEdit.setText('{:.4f} s'.format(analysis.timing))
        self.lengthx_interval_upgrade()
        self.TimeRangeLineEdit.setText('{} ms'.format(int(time_width * 1000)))

    def portView_update(self):
        """更新示波器可以显示的端口的 Combobox"""
        self.PortViewComboBox.clear()
        for i in range(len(analysis.elements)):
            self.PortViewComboBox.addItem(str(i * 2))
            self.PortViewComboBox.addItem(str(i * 2 + 1))

    def critialEnable(self):
        """恢复控件"""
        for obj in self.criticalList:
            obj.setEnabled(True)

    def criticalDiable(self):
        """禁用控件"""
        for obj in self.criticalList:
            obj.setEnabled(False)

    def RunButton_click(self):
        """开始分析"""
        if self.GroundLineEdit.text() == '':
            QMessageBox.critical(self, 'Fatal Error', 'Please choose a ground port!',
                                 QMessageBox.Cancel, QMessageBox.Cancel)
            return

        self.WavePlot.setVisible(True)
        self.RunButton.setEnabled(False)
        self.actionRun_Stimulation.setEnabled(False)
        self.StopButton.setEnabled(True)
        self.actionStop_Stimulation.setEnabled(True)
        self.sendMsg('>>> Running analysis...')

        try:
            analysis.restart()
            analysis.ground = eval(self.GroundLineEdit.text())
            Matplotlibwidget.draw_port = self.PortViewComboBox.currentIndex()

            analysis.main_initializing(analysis.ground)  # 分析初始化，并选取参考地端口
            _thread_it(analysis.main_analyzing)  # 开始分析
            self.criticalDiable()

        except:
            QMessageBox.critical(self, 'Fatal Error', 'Analysis Error!',
                                 QMessageBox.Cancel, QMessageBox.Cancel)
            self.StopButton_click()

    def StopButton_click(self):
        """停止分析"""
        analysis.analyzing_stop = True
        self.StopButton.setEnabled(False)
        self.actionStop_Stimulation.setEnabled(False)
        self.RunButton.setEnabled(True)
        self.actionRun_Stimulation.setEnabled(True)
        self.critialEnable()
        self.sendMsg('  Stopped.')

    def addWindowShow(self):
        """跳转到添加元件的界面"""
        self.addComponentsWin.show()

    def editWindowShow(self):
        """判断并跳转到修改元件的界面"""
        if len(analysis.elements) > 0:
            self.sendToEditSignal.emit(self.selectComponent, self.tableWidgetComponents.item(self.selectComponent, 0).text())
            self.editComponentWin.show()

    def addConnectionsButton_click(self):
        """添加连接按钮事件触发"""
        port_1 = self.Port1LineEdit.text()
        port_2 = self.Port2LineEdit.text()
        if port_1 == '' or port_2 == '':  # 输入错误的大判断
            QMessageBox.critical(self, 'Invalid Input', 'Input is empty!',
                                 QMessageBox.Cancel,QMessageBox.Cancel)
            return
        elif eval(port_1) > len(analysis.elements) * 2 - 1 or eval(port_2) > len(analysis.elements) * 2 - 1:
            QMessageBox.critical(self, 'Invalid Input', 'Port number out of range!',
                                 QMessageBox.Cancel, QMessageBox.Cancel)
            return
        elif port_1 == port_2:
            QMessageBox.critical(self, 'Invalid Input', 'Port 1 & 2 should be different!',
                                 QMessageBox.Cancel, QMessageBox.Cancel)
            return
        elif abs(eval(port_1) - eval(port_2)) == 1 and (eval(port_1) + eval(port_2) - 1) % 4 == 0:  # 自短路判断
            QMessageBox.critical(self, 'Invalid Input', 'Port 1 & 2 are short circuited!',
                                 QMessageBox.Cancel, QMessageBox.Cancel)
            return

        port_set = {eval(port_1), eval(port_2)}
        if port_set in self.connectionsSet:
            QMessageBox.critical(self, 'Invalid Input', 'Connection has already existed!',
                                 QMessageBox.Cancel, QMessageBox.Cancel)
            return
        else:
            self.RunButton.setEnabled(False)
            self.actionRun_Stimulation.setEnabled(False)
            self.connectionsSet.append(port_set)
            row = self.tableWidgetConnentions.rowCount()
            self.tableWidgetConnentions.setRowCount(row + 1)
            self.tableWidgetConnentions.setItem(row, 0, QTableWidgetItem('Wire'))
            self.tableWidgetConnentions.setItem(row, 1, QTableWidgetItem(port_1))
            self.tableWidgetConnentions.setItem(row, 2, QTableWidgetItem(port_2))
            self.tableWidgetConnentions.setItem(row, 3, QTableWidgetItem('No Policy'))
            self.Port1LineEdit.clear()
            self.Port2LineEdit.clear()

    def PortLineEdit_setValue(self):
        """port1/2LineEdit、groundEditLine定时改变输入精度"""
        self.portValuePrecision.setTop(len(analysis.elements) * 2 - 1)  # 精度限制

    def tableWidgetComponents_update(self):
        """元件列表端口值更新"""
        for i in range(self.tableWidgetComponents.rowCount()):
            self.tableWidgetComponents.setItem(i, 3, QTableWidgetItem(str(i * 2)))
            self.tableWidgetComponents.setItem(i, 4, QTableWidgetItem(str(i * 2 + 1)))

    def delButton_click(self):
        """删除所选元件"""
        if self.tableWidgetComponents.rowCount() > 0:
            justify = QMessageBox.question(self, 'Delete', 'Sure to delete?\nName: {} Type: {} Value: {}'.format(
                self.tableWidgetComponents.item(self.selectComponent, 0).text(),
                self.tableWidgetComponents.item(self.selectComponent, 1).text(),
                self.tableWidgetComponents.item(self.selectComponent, 2).text()
            ), QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
            if justify == QMessageBox.Yes:
                analysis.elements.pop(self.selectComponent)  # 从库中删除
                nameSet.discard(self.tableWidgetComponents.item(self.selectComponent, 0).text())  # 删除名字
                self.tableWidgetComponents.removeRow(self.selectComponent)  # 从表格删除
                self.tableWidgetComponents_update()  # 列表端口值更新
                if self.selectComponent - 1 >= 0:  # 防止溢出崩溃
                    self.selectComponent -= 1
                else:
                    self.selectComponent = 0
                self.RunButton.setEnabled(False)
                self.actionRun_Stimulation.setEnabled(False)

    def delConnectionsButton_click(self):
        """删除连接按钮事件触发"""
        if self.tableWidgetConnentions.rowCount() > 0:
            justify = QMessageBox.question(self, 'Delete', 'Sure to delete?\nType: {} Port1: {} Port2: {} Time Policy: {}'.format(
                self.tableWidgetConnentions.item(self.selectConnection, 0).text(),
                self.tableWidgetConnentions.item(self.selectConnection, 1).text(),
                self.tableWidgetConnentions.item(self.selectConnection, 2).text(),
                self.tableWidgetConnentions.item(self.selectConnection, 3).text()
            ), QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
            if justify == QMessageBox.Yes:
                port_set = {eval(self.tableWidgetConnentions.item(self.selectConnection, 1).text()),
                            eval(self.tableWidgetConnentions.item(self.selectConnection, 2).text())}
                for i in range(len(self.connectionsSet)):  # 删除预处理连接标记
                    if self.connectionsSet[i] == port_set:
                        self.connectionsSet.pop(i)
                        break
                self.tableWidgetConnentions.removeRow(self.selectConnection)  # 从表格删除
                if self.selectConnection - 1 >= 0:  # 防止溢出崩溃
                    self.selectConnection -= 1
                else:
                    self.selectConnection = 0
                self.RunButton.setEnabled(False)
                self.actionRun_Stimulation.setEnabled(False)

    def clearButton_click(self):
        """删除所有元件"""
        justify = QMessageBox.question(self, 'Delete', 'Clear all?', QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if justify == QMessageBox.Yes:
            analysis.elements.clear()  # 从库中删除
            nameSet.clear()  # 删除名字
            self.tableWidgetComponents.clearContents()  # 从表格删除
            self.tableWidgetComponents.setRowCount(0)
            self.selectComponent = 0
            self.RunButton.setEnabled(False)
            self.actionRun_Stimulation.setEnabled(False)

    def clearConnectionsButton_click(self):
        """清空连接按钮事件触发"""
        justify = QMessageBox.question(self, 'Delete', 'Clear all?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if justify == QMessageBox.Yes:
            self.connectionsSet.clear()  # 删除预处理标记
            self.tableWidgetConnentions.clearContents()  # 从表格删除
            self.tableWidgetConnentions.setRowCount(0)
            self.selectConnection = 0
            self.RunButton.setEnabled(False)
            self.actionRun_Stimulation.setEnabled(False)

    def addWindowAdjust(self, ele, val, frq, name):
        """添加元件确认后，对主窗口的表格进行操作，且为连接元件做初始化"""
        self.RunButton.setEnabled(False)
        self.actionRun_Stimulation.setEnabled(False)
        name_item = QTableWidgetItem(name)
        port_1_item = QTableWidgetItem('{}'.format(len(analysis.elements) * 2 - 2))
        port_2_item = QTableWidgetItem('{}'.format(len(analysis.elements) * 2 - 1))
        row = self.tableWidgetComponents.rowCount()
        self.tableWidgetComponents.setRowCount(row + 1)
        self.tableWidgetComponents.setItem(row, 0, name_item)
        if ele == 0:  # 电阻
            self.tableWidgetComponents.setItem(row, 1, QTableWidgetItem('R'))
            self.tableWidgetComponents.setItem(row, 2, QTableWidgetItem('{} Ω'.format(val)))
        elif ele == 1:  # 电容
            self.tableWidgetComponents.setItem(row, 1, QTableWidgetItem('C'))
            self.tableWidgetComponents.setItem(row, 2, QTableWidgetItem('{} F'.format(val)))
        elif ele == 2:  # 电感
            self.tableWidgetComponents.setItem(row, 1, QTableWidgetItem('L'))
            self.tableWidgetComponents.setItem(row, 2, QTableWidgetItem('{} H'.format(val)))
        elif ele == 3:  # DC_POWER
            self.tableWidgetComponents.setItem(row, 1, QTableWidgetItem('DC_Vs'))
            self.tableWidgetComponents.setItem(row, 2, QTableWidgetItem('{} V'.format(val)))
        elif ele == 4:  # DC_CURRENT
            self.tableWidgetComponents.setItem(row, 1, QTableWidgetItem('DC_Is'))
            self.tableWidgetComponents.setItem(row, 2, QTableWidgetItem('{} A'.format(val)))
        elif ele == 5:  # AC_POWER
            self.tableWidgetComponents.setItem(row, 1, QTableWidgetItem('AC_Vs'))
            self.tableWidgetComponents.setItem(row, 2, QTableWidgetItem('{} V , {} Hz'.format(val, frq)))
        elif ele == 6:  # AC_CURRENT
            self.tableWidgetComponents.setItem(row, 1, QTableWidgetItem('AC_Is'))
            self.tableWidgetComponents.setItem(row, 2, QTableWidgetItem('{} A , {} Hz'.format(val, frq)))

        self.tableWidgetComponents.setItem(row, 3, port_1_item)
        self.tableWidgetComponents.setItem(row, 4, port_2_item)

        analysis.layout_initializing(len(analysis.elements))  # 连接初始化

    def editWindowAdjust(self, ele, val, frq, name):
        """修改元件确认后，对主窗口的表格进行操作，且为连接元件做初始化"""
        analysis.modify_element(ele, val, frq)  # 从库中修改
        nameSet.discard(self.tableWidgetComponents.item(ele, 0).text())  # 删除名字
        nameSet.add(name)  # 新增名字
        self.tableWidgetComponents.setItem(ele, 0, QTableWidgetItem(name))  # 表格修改
        if analysis.elements[ele].label == 'R':  # 电阻
            self.tableWidgetComponents.setItem(ele, 2, QTableWidgetItem('{} Ω'.format(val)))
        elif analysis.elements[ele].label == 'C':  # 电容
            self.tableWidgetComponents.setItem(ele, 2, QTableWidgetItem('{} F'.format(val)))
        elif analysis.elements[ele].label == 'L':  # 电感
            self.tableWidgetComponents.setItem(ele, 2, QTableWidgetItem('{} H'.format(val)))
        elif analysis.elements[ele].label == 'DC_VS':  # DC_POWER
            self.tableWidgetComponents.setItem(ele, 2, QTableWidgetItem('{} V'.format(val)))
        elif analysis.elements[ele].label == 'DC_IS':  # DC_CURRENT
            self.tableWidgetComponents.setItem(ele, 2, QTableWidgetItem('{} A'.format(val)))
        elif analysis.elements[ele].label == 'AC_VS':  # AC_POWER
            self.tableWidgetComponents.setItem(ele, 2, QTableWidgetItem('{} V , {} Hz'.format(val, frq)))
        elif analysis.elements[ele].label == 'AC_IS':  # AC_CURRENT
            self.tableWidgetComponents.setItem(ele, 2, QTableWidgetItem('{} A , {} Hz'.format(val, frq)))
        self.RunButton.setEnabled(False)  # 禁用运行仿真按钮
        self.actionRun_Stimulation.setEnabled(False)


    def getSelectComponent(self, item):
        """选中元件读取行数"""
        self.selectComponent = item.row()  # 保存选中行

    def getSelectConnection(self, item):
        """选中连接读取行数"""
        self.selectConnection = item.row()

    def ConstructConnectionsButton_click(self):
        """重新构建连接按钮事件"""
        if len(analysis.elements) == 0:
            return
        try:
            self.construct_connections()
            self.RunButton.setEnabled(True)
            self.actionRun_Stimulation.setEnabled(True)
            self.portView_update()
            self.drawing_circuit()
        except:
            QMessageBox.critical(self, 'Fatal Error', 'Abnormal circuit connection!', QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.information(self, 'Information', 'Construct successfully!', QMessageBox.Yes, QMessageBox.Yes)
            self.sendMsg('>>> Circuit construct successfully!')

    def construct_connections(self):
        """重新构建连接核心算法"""
        analysis.reattach()  # 清空已有连接
        for port_set in self.connectionsSet:
            temp_port_set = copy.copy(port_set)
            analysis.connecting(temp_port_set.pop(), temp_port_set.pop())

    def sendMsg(self, msg):
        """outcome 窗口提示信息"""
        if self.sentMessage >= 50:
            self.textOutcomes.clear()
        self.textOutcomes.append(msg + '\n')
        self.sentMessage += 1

    def drawing_circuit(self):
        """绘制电路图"""
        self.scene = QGraphicsScene()  # 创建场景
        self.item_list = list()  # 图像元列表
        for ele in analysis.elements:
            img=cv2.imread("E:\\Documents\\code\\prj\\Circuit Analyser\\code\\images\\{}.png".format(ele.label), cv2.IMREAD_UNCHANGED)  # 读取图像，路径可以修改，不能包含中文，否则报错！
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)  # 转换图像通道
            x = img.shape[1]  # 获取图像大小
            y = img.shape[0]
            frame = QImage(img, x, y, QImage.Format_RGBA8888)
            pix = QPixmap.fromImage(frame)
            self.item_list.append(QGraphicsPixmapItem(pix))  #创建像素图元
            self.item_list[len(self.item_list) - 1].setTransformOriginPoint(40, 100)  # 中心旋转
            self.item_list[len(self.item_list) - 1].setFlag(QGraphicsItem.ItemIsMovable)  # 使图元可以拖动
            self.item_list[len(self.item_list) - 1].setFlag(QGraphicsItem.ItemIsSelectable)  # 使图元可以被选择
        for i in range(len(self.item_list)):
            self.scene.addItem(self.item_list[i])

        self.CircuitViewer.mcv.setScene(self.scene)  # 将场景添加至视图
        tnum = 0
        for node in analysis.nodes:
            tnum += len(node.port) - 1
        self.CircuitViewer.mcv.set_wire_num(tnum)  # 传递连线数
        self.CircuitViewer.mcv.set_elementsItemList(self.item_list)  # 传递元件图元
        self.CircuitViewer.mcv.drawLine()

    def SwitchPushButton_click(self):
        """Coming soon..."""
        QMessageBox.information(self, 'Info', 'Coming soon...', QMessageBox.Yes, QMessageBox.Yes)

    def closeEvent(self, QCloseEvent):
        """退出提示"""
        reply = QMessageBox.information(self, "Exit", "Sure to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        if reply == QMessageBox.No:
            QCloseEvent.ignore()

    def showAbout(self):
        """软件相关"""
        QMessageBox.information(self, "About...", """Circuit Analyser (Verson 1.0)""", QMessageBox.Yes, QMessageBox.Yes)


class AddComponentsWindow(QMainWindow, Ui_AddComponentsDialog):
    """
        增加元件的子窗口
                        """
    addWinSignal = pyqtSignal(int, float, float, str)

    def __init__(self, parent=None):
        super(AddComponentsWindow, self).__init__(parent)
        self.setupUi(self)

        self.ValuePrecision = QDoubleValidator(self)  # 精度限制
        self.ValuePrecision.setRange(0, 1e+5)
        self.ValuePrecision.setNotation(QDoubleValidator.StandardNotation)
        self.ValuePrecision.setDecimals(4)

        self.ValueLineEdit.setValidator(self.ValuePrecision)  # 精度绑定
        self.FrqLineEdit.setValidator(self.ValuePrecision)

        self.FrqLineEdit.setEnabled(False)
        self.FrqUnitLineEdit.setEnabled(False)
        self.FrqUnitLineEdit.setReadOnly(True)
        self.FrqUnitLineEdit.setText('Hz')
        self.ValueUnitLineEdit.setText('Ω')
        self.ValueUnitLineEdit.setReadOnly(True)

    def keyPressEvent(self, event):
        """键盘事件"""
        if event.key() == Qt.Key_Return:
            self.accept()

    def empty_input_msg(self):
        QMessageBox.critical(self, 'Invalid Input', 'Input is empty!', QMessageBox.Cancel, QMessageBox.Cancel)

    def accept(self):
        t_num = self.comboBox.currentIndex()
        t_val = self.ValueLineEdit.text()
        t_frq = self.FrqLineEdit.text()
        t_name = self.NameLineEdit.text()
        if t_val == '' or t_name == '':
            self.empty_input_msg()
            return
        if t_num in (5, 6):
            if t_frq == '':
                self.empty_input_msg()
                return
        if t_name in nameSet:
            QMessageBox.critical(self, 'Duplicate named', 'Please change another name!', QMessageBox.Cancel, QMessageBox.Cancel)
            self.NameLineEdit.clear()
            return
        else:
            nameSet.add(t_name)
        if t_num == 0:  # 电阻
            analysis.place_elements(R=eval(t_val))
            self.addWinSignal.emit(0, eval(t_val), 0, t_name)
        elif t_num == 1:  # 电容
            analysis.place_elements(C=eval(t_val))
            self.addWinSignal.emit(1, eval(t_val), 0, t_name)
        elif t_num == 2:  # 电感
            analysis.place_elements(L=eval(t_val))
            self.addWinSignal.emit(2, eval(t_val), 0, t_name)
        elif t_num == 3:  # DC_POWER
            analysis.place_elements(DC_VS=eval(t_val))
            self.addWinSignal.emit(3, eval(t_val), 0, t_name)
        elif t_num == 4:  # DC_CURRENT
            analysis.place_elements(DC_IS=eval(t_val))
            self.addWinSignal.emit(4, eval(t_val), 0, t_name)
        elif t_num == 5:  # AC_POWER
            analysis.place_elements(AC_VS=0, A=eval(t_val), f=eval(t_frq))
            self.addWinSignal.emit(5, eval(t_val), eval(t_frq), t_name)
        elif t_num == 6:  # AC_CURRENT
            analysis.place_elements(AC_IS=0, A=eval(t_val), f=eval(t_frq))
            self.addWinSignal.emit(6, eval(t_val), eval(t_frq), t_name)
        self.hide()

    def reject(self):
        self.hide()

    def showFreq(self):  # 显示频率输入栏（附加切换单位显示，清空表单）
        t_index = self.comboBox.currentIndex()
        if t_index in (5, 6):
            self.FrqLineEdit.setEnabled(True)
            self.FrqUnitLineEdit.setEnabled(True)
        else:
            self.FrqLineEdit.setEnabled(False)
            self.FrqUnitLineEdit.setEnabled(False)
        if t_index == 0:  # 电阻
            self.ValueUnitLineEdit.setText('Ω')
        elif t_index == 1:  # 电容
            self.ValueUnitLineEdit.setText('F')
        elif t_index == 2:  # 电感
            self.ValueUnitLineEdit.setText('H')
        elif t_index == 3 or t_index == 5:  # POWER
            self.ValueUnitLineEdit.setText('V')
        elif t_index == 4 or t_index == 6:  # CURRENT
            self.ValueUnitLineEdit.setText('A')
        self.ValueLineEdit.clear()
        self.FrqLineEdit.clear()

class EditComponentsWindow(QMainWindow, Ui_EditComponentWin):
    """
        修改元件的子窗口
                        """
    editWinSignal = pyqtSignal(int, float, float, str)

    def __init__(self, parent=None):
        super(EditComponentsWindow, self).__init__(parent)
        self.setupUi(self)
        self.update_unit(0, '')

        self.ValuePrecision = QDoubleValidator(self)  # 精度限制
        self.ValuePrecision.setRange(0, 1e+5)
        self.ValuePrecision.setNotation(QDoubleValidator.StandardNotation)
        self.ValuePrecision.setDecimals(4)

        self.NewValueLineEdit.setValidator(self.ValuePrecision)  # 精度绑定
        self.NewFreqLineEdit.setValidator(self.ValuePrecision)

        self.ele = 0  # 当前元件序号
        self.label = 'R'  # 当前元件类型
        self.name = ''  # 当前元件名字

    def keyPressEvent(self, event):
        """键盘事件"""
        if event.key() == Qt.Key_Return:
            self.accept()

    def empty_input_msg(self):
        QMessageBox.critical(self, 'Invalid Input', 'Input is empty!', QMessageBox.Cancel, QMessageBox.Cancel)

    def accept(self):
        t_val = self.NewValueLineEdit.text()
        t_frq = self.NewFreqLineEdit.text()
        t_name = self.NewNameLineEdit.text()
        if t_val == '' or t_name == '':
            self.empty_input_msg()
            return
        if self.label in analysis.AC_label:
            if t_frq == '':
                self.empty_input_msg()
                return
        if t_name in nameSet and t_name != self.name:
            QMessageBox.critical(self, 'Duplicate named', 'Please change another name!', QMessageBox.Cancel, QMessageBox.Cancel)
            self.NewNameLineEdit.clear()
            return
        if self.label == 'R':  # 电阻
            self.editWinSignal.emit(self.ele, eval(t_val), 0, t_name)
        elif self.label == 'C':  # 电容
            self.editWinSignal.emit(self.ele, eval(t_val), 0, t_name)
        elif self.label == 'L':  # 电感
            self.editWinSignal.emit(self.ele, eval(t_val), 0, t_name)
        elif self.label == 'DC_VS':  # DC_POWER
            self.editWinSignal.emit(self.ele, eval(t_val), 0, t_name)
        elif self.label == 'DC_IS':  # DC_CURRENT
            self.editWinSignal.emit(self.ele, eval(t_val), 0, t_name)
        elif self.label == 'AC_VS':  # AC_POWER
            self.editWinSignal.emit(self.ele, eval(t_val), eval(t_frq), t_name)
        elif self.label == 'AC_IS':  # AC_CURRENT
            self.editWinSignal.emit(self.ele, eval(t_val), eval(t_frq), t_name)
        self.hide()

    def update_unit(self, ele, name):  # 更新界面单位值，读取元件信号，显示
        if len(analysis.elements) == 0:  # 判断空值
            return
        self.ele = ele
        self.name = name
        self.label = analysis.elements[self.ele].label  # 更新元件信息

        self.NewNameLineEdit.setText(self.name)  # 设置文本框信息
        if self.label in analysis.AC_label:
            self.NewValueLineEdit.setText(str(analysis.elements[self.ele].amp))
        else:
            self.NewValueLineEdit.setText(str(analysis.elements[self.ele].val))

        if self.label in analysis.AC_label:
            self.NewFreqLineEdit.setPlaceholderText('New Frequency')
            self.NewFreqLineEdit.setText(str(analysis.elements[self.ele].feq))
            self.NewFreqLineEdit.setEnabled(True)
            self.NewFreqUnitLineEdit.setEnabled(True)
        else:
            self.NewFreqLineEdit.clear()
            self.NewFreqLineEdit.setPlaceholderText('')
            self.NewFreqLineEdit.setEnabled(False)
            self.NewFreqUnitLineEdit.setEnabled(False)
        if self.label == 'R':  # 电阻
            self.NewValueUnitLineEdit.setText('Ω')
        elif self.label == 'C':  # 电容
            self.NewValueUnitLineEdit.setText('F')
        elif self.label == 'L':  # 电感
            self.NewValueUnitLineEdit.setText('H')
        elif self.label in analysis.PWR_label:  # POWER
            self.NewValueUnitLineEdit.setText('V')
        elif self.label in analysis.CRT_label:  # CURRENT
            self.NewValueUnitLineEdit.setText('A')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    toolbar = myWin.findChild(QToolBar)
    toolbar.setVisible(False)
    sys.exit(app.exec_())