# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1938, 1102)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.CircuitViewer = DrawView(self.groupBox_6)
        self.CircuitViewer.setStyleSheet("background-color: rgb(80, 95, 105);")
        self.CircuitViewer.setObjectName("CircuitViewer")
        self.gridLayout_7.addWidget(self.CircuitViewer, 0, 0, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_6, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.DeleteComponentsButton = QtWidgets.QPushButton(self.groupBox_2)
        self.DeleteComponentsButton.setObjectName("DeleteComponentsButton")
        self.gridLayout_2.addWidget(self.DeleteComponentsButton, 2, 0, 1, 1)
        self.ClearComponentsButton = QtWidgets.QPushButton(self.groupBox_2)
        self.ClearComponentsButton.setObjectName("ClearComponentsButton")
        self.gridLayout_2.addWidget(self.ClearComponentsButton, 2, 1, 1, 1)
        self.tableWidgetComponents = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidgetComponents.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidgetComponents.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidgetComponents.setObjectName("tableWidgetComponents")
        self.tableWidgetComponents.setColumnCount(5)
        self.tableWidgetComponents.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetComponents.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetComponents.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetComponents.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetComponents.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetComponents.setHorizontalHeaderItem(4, item)
        self.tableWidgetComponents.verticalHeader().setStretchLastSection(False)
        self.gridLayout_2.addWidget(self.tableWidgetComponents, 0, 0, 1, 2)
        self.AddComponentsButton = QtWidgets.QPushButton(self.groupBox_2)
        self.AddComponentsButton.setObjectName("AddComponentsButton")
        self.gridLayout_2.addWidget(self.AddComponentsButton, 1, 0, 1, 1)
        self.EditComponentButton = QtWidgets.QPushButton(self.groupBox_2)
        self.EditComponentButton.setObjectName("EditComponentButton")
        self.gridLayout_2.addWidget(self.EditComponentButton, 1, 1, 1, 1)
        self.gridLayout_8.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.Port2LineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Port2LineEdit.sizePolicy().hasHeightForWidth())
        self.Port2LineEdit.setSizePolicy(sizePolicy)
        self.Port2LineEdit.setObjectName("Port2LineEdit")
        self.gridLayout_4.addWidget(self.Port2LineEdit, 1, 3, 1, 1)
        self.SwitchPushButton = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SwitchPushButton.sizePolicy().hasHeightForWidth())
        self.SwitchPushButton.setSizePolicy(sizePolicy)
        self.SwitchPushButton.setObjectName("SwitchPushButton")
        self.gridLayout_4.addWidget(self.SwitchPushButton, 1, 5, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 3, 0, 1, 1)
        self.DeleteConnectionsButton = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DeleteConnectionsButton.sizePolicy().hasHeightForWidth())
        self.DeleteConnectionsButton.setSizePolicy(sizePolicy)
        self.DeleteConnectionsButton.setObjectName("DeleteConnectionsButton")
        self.gridLayout_4.addWidget(self.DeleteConnectionsButton, 1, 6, 1, 1)
        self.ClearConnectionsButton = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ClearConnectionsButton.sizePolicy().hasHeightForWidth())
        self.ClearConnectionsButton.setSizePolicy(sizePolicy)
        self.ClearConnectionsButton.setObjectName("ClearConnectionsButton")
        self.gridLayout_4.addWidget(self.ClearConnectionsButton, 1, 7, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 1, 4, 1, 1)
        self.tableWidgetConnentions = QtWidgets.QTableWidget(self.groupBox_3)
        self.tableWidgetConnentions.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidgetConnentions.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidgetConnentions.setObjectName("tableWidgetConnentions")
        self.tableWidgetConnentions.setColumnCount(4)
        self.tableWidgetConnentions.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetConnentions.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetConnentions.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetConnentions.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetConnentions.setHorizontalHeaderItem(3, item)
        self.gridLayout_4.addWidget(self.tableWidgetConnentions, 0, 0, 1, 9)
        self.GroundLineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GroundLineEdit.sizePolicy().hasHeightForWidth())
        self.GroundLineEdit.setSizePolicy(sizePolicy)
        self.GroundLineEdit.setText("")
        self.GroundLineEdit.setObjectName("GroundLineEdit")
        self.gridLayout_4.addWidget(self.GroundLineEdit, 3, 1, 1, 1)
        self.Port1LineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Port1LineEdit.sizePolicy().hasHeightForWidth())
        self.Port1LineEdit.setSizePolicy(sizePolicy)
        self.Port1LineEdit.setObjectName("Port1LineEdit")
        self.gridLayout_4.addWidget(self.Port1LineEdit, 1, 2, 1, 1)
        self.AddConnectionsButton = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddConnectionsButton.sizePolicy().hasHeightForWidth())
        self.AddConnectionsButton.setSizePolicy(sizePolicy)
        self.AddConnectionsButton.setObjectName("AddConnectionsButton")
        self.gridLayout_4.addWidget(self.AddConnectionsButton, 1, 0, 1, 2)
        self.ConstructConnectionsButton = QtWidgets.QPushButton(self.groupBox_3)
        self.ConstructConnectionsButton.setMinimumSize(QtCore.QSize(8, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ConstructConnectionsButton.setFont(font)
        self.ConstructConnectionsButton.setObjectName("ConstructConnectionsButton")
        self.gridLayout_4.addWidget(self.ConstructConnectionsButton, 3, 2, 1, 7)
        self.gridLayout_9.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_5.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_8 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_8)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.textOutcomes = QtWidgets.QTextEdit(self.groupBox_8)
        self.textOutcomes.setReadOnly(True)
        self.textOutcomes.setObjectName("textOutcomes")
        self.gridLayout_10.addWidget(self.textOutcomes, 1, 0, 1, 1)
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_8)
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.RunButton = QtWidgets.QPushButton(self.groupBox_7)
        self.RunButton.setEnabled(False)
        self.RunButton.setObjectName("RunButton")
        self.verticalLayout.addWidget(self.RunButton)
        self.StopButton = QtWidgets.QPushButton(self.groupBox_7)
        self.StopButton.setEnabled(False)
        self.StopButton.setObjectName("StopButton")
        self.verticalLayout.addWidget(self.StopButton)
        self.gridLayout_10.addWidget(self.groupBox_7, 0, 0, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_8, 1, 1, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.WavePlot = MatplotlibWidget(self.groupBox_5)
        self.WavePlot.setObjectName("WavePlot")
        self.gridLayout_6.addWidget(self.WavePlot, 0, 1, 1, 11)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem1, 2, 5, 1, 1)
        self.PrecisionLabel = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrecisionLabel.sizePolicy().hasHeightForWidth())
        self.PrecisionLabel.setSizePolicy(sizePolicy)
        self.PrecisionLabel.setObjectName("PrecisionLabel")
        self.gridLayout_6.addWidget(self.PrecisionLabel, 2, 9, 1, 1)
        self.TimeRangeLabel = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TimeRangeLabel.sizePolicy().hasHeightForWidth())
        self.TimeRangeLabel.setSizePolicy(sizePolicy)
        self.TimeRangeLabel.setObjectName("TimeRangeLabel")
        self.gridLayout_6.addWidget(self.TimeRangeLabel, 2, 2, 1, 1)
        self.TimeRangeHorizontalSlider = QtWidgets.QSlider(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TimeRangeHorizontalSlider.sizePolicy().hasHeightForWidth())
        self.TimeRangeHorizontalSlider.setSizePolicy(sizePolicy)
        self.TimeRangeHorizontalSlider.setMinimum(500)
        self.TimeRangeHorizontalSlider.setMaximum(5000)
        self.TimeRangeHorizontalSlider.setSliderPosition(500)
        self.TimeRangeHorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.TimeRangeHorizontalSlider.setObjectName("TimeRangeHorizontalSlider")
        self.gridLayout_6.addWidget(self.TimeRangeHorizontalSlider, 2, 3, 1, 1)
        self.TimesLable = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TimesLable.sizePolicy().hasHeightForWidth())
        self.TimesLable.setSizePolicy(sizePolicy)
        self.TimesLable.setObjectName("TimesLable")
        self.gridLayout_6.addWidget(self.TimesLable, 2, 6, 1, 1)
        self.PrecisionHorizontalSlider = QtWidgets.QSlider(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrecisionHorizontalSlider.sizePolicy().hasHeightForWidth())
        self.PrecisionHorizontalSlider.setSizePolicy(sizePolicy)
        self.PrecisionHorizontalSlider.setMaximum(1651)
        self.PrecisionHorizontalSlider.setProperty("value", 1000)
        self.PrecisionHorizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.PrecisionHorizontalSlider.setObjectName("PrecisionHorizontalSlider")
        self.gridLayout_6.addWidget(self.PrecisionHorizontalSlider, 2, 10, 1, 1)
        self.PortViewComboBox = QtWidgets.QComboBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PortViewComboBox.sizePolicy().hasHeightForWidth())
        self.PortViewComboBox.setSizePolicy(sizePolicy)
        self.PortViewComboBox.setObjectName("PortViewComboBox")
        self.gridLayout_6.addWidget(self.PortViewComboBox, 2, 1, 1, 1)
        self.TimesLineEdit = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TimesLineEdit.sizePolicy().hasHeightForWidth())
        self.TimesLineEdit.setSizePolicy(sizePolicy)
        self.TimesLineEdit.setReadOnly(True)
        self.TimesLineEdit.setObjectName("TimesLineEdit")
        self.gridLayout_6.addWidget(self.TimesLineEdit, 2, 7, 1, 1)
        self.TimeRangeLineEdit = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TimeRangeLineEdit.sizePolicy().hasHeightForWidth())
        self.TimeRangeLineEdit.setSizePolicy(sizePolicy)
        self.TimeRangeLineEdit.setReadOnly(True)
        self.TimeRangeLineEdit.setObjectName("TimeRangeLineEdit")
        self.gridLayout_6.addWidget(self.TimeRangeLineEdit, 2, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout_6.addWidget(self.label_2, 2, 0, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_5, 0, 1, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1938, 26))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuComponents = QtWidgets.QMenu(self.menuMenu)
        self.menuComponents.setObjectName("menuComponents")
        self.menuConnections = QtWidgets.QMenu(self.menuMenu)
        self.menuConnections.setObjectName("menuConnections")
        self.menuStimulation = QtWidgets.QMenu(self.menuMenu)
        self.menuStimulation.setObjectName("menuStimulation")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAdd = QtWidgets.QAction(MainWindow)
        self.actionAdd.setObjectName("actionAdd")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionAdd_2 = QtWidgets.QAction(MainWindow)
        self.actionAdd_2.setObjectName("actionAdd_2")
        self.actionClear_2 = QtWidgets.QAction(MainWindow)
        self.actionClear_2.setObjectName("actionClear_2")
        self.actionEdit = QtWidgets.QAction(MainWindow)
        self.actionEdit.setObjectName("actionEdit")
        self.actionRun_Stimulation = QtWidgets.QAction(MainWindow)
        self.actionRun_Stimulation.setEnabled(False)
        self.actionRun_Stimulation.setObjectName("actionRun_Stimulation")
        self.actionStop_Stimulation = QtWidgets.QAction(MainWindow)
        self.actionStop_Stimulation.setEnabled(False)
        self.actionStop_Stimulation.setObjectName("actionStop_Stimulation")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuComponents.addAction(self.actionAdd)
        self.menuComponents.addAction(self.actionEdit)
        self.menuComponents.addSeparator()
        self.menuComponents.addAction(self.actionClear)
        self.menuConnections.addAction(self.actionAdd_2)
        self.menuConnections.addSeparator()
        self.menuConnections.addAction(self.actionClear_2)
        self.menuStimulation.addAction(self.actionRun_Stimulation)
        self.menuStimulation.addAction(self.actionStop_Stimulation)
        self.menuMenu.addAction(self.menuComponents.menuAction())
        self.menuMenu.addAction(self.menuConnections.menuAction())
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.menuStimulation.menuAction())
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tableWidgetComponents.itemClicked['QTableWidgetItem*'].connect(MainWindow.getSelectComponent)
        self.DeleteComponentsButton.clicked.connect(MainWindow.delButton_click)
        self.ClearComponentsButton.clicked.connect(MainWindow.clearButton_click)
        self.AddConnectionsButton.clicked.connect(MainWindow.addConnectionsButton_click)
        self.DeleteConnectionsButton.clicked.connect(MainWindow.delConnectionsButton_click)
        self.ClearConnectionsButton.clicked.connect(MainWindow.clearConnectionsButton_click)
        self.tableWidgetConnentions.itemClicked['QTableWidgetItem*'].connect(MainWindow.getSelectConnection)
        self.ConstructConnectionsButton.clicked.connect(MainWindow.ConstructConnectionsButton_click)
        self.SwitchPushButton.clicked.connect(MainWindow.SwitchPushButton_click)
        self.EditComponentButton.clicked.connect(MainWindow.editWindowShow)
        self.actionAdd.triggered.connect(MainWindow.addWindowShow)
        self.actionEdit.triggered.connect(MainWindow.editWindowShow)
        self.actionClear.triggered.connect(MainWindow.clearButton_click)
        self.actionAdd_2.triggered.connect(MainWindow.addConnectionsButton_click)
        self.actionClear_2.triggered.connect(MainWindow.clearConnectionsButton_click)
        self.actionRun_Stimulation.triggered.connect(MainWindow.RunButton_click)
        self.actionStop_Stimulation.triggered.connect(MainWindow.StopButton_click)
        self.actionExit.triggered.connect(MainWindow.close)
        self.actionAbout.triggered.connect(MainWindow.showAbout)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tableWidgetComponents, self.AddComponentsButton)
        MainWindow.setTabOrder(self.AddComponentsButton, self.DeleteComponentsButton)
        MainWindow.setTabOrder(self.DeleteComponentsButton, self.ClearComponentsButton)
        MainWindow.setTabOrder(self.ClearComponentsButton, self.tabWidget)
        MainWindow.setTabOrder(self.tabWidget, self.tableWidgetConnentions)
        MainWindow.setTabOrder(self.tableWidgetConnentions, self.AddConnectionsButton)
        MainWindow.setTabOrder(self.AddConnectionsButton, self.Port1LineEdit)
        MainWindow.setTabOrder(self.Port1LineEdit, self.Port2LineEdit)
        MainWindow.setTabOrder(self.Port2LineEdit, self.SwitchPushButton)
        MainWindow.setTabOrder(self.SwitchPushButton, self.DeleteConnectionsButton)
        MainWindow.setTabOrder(self.DeleteConnectionsButton, self.ClearConnectionsButton)
        MainWindow.setTabOrder(self.ClearConnectionsButton, self.GroundLineEdit)
        MainWindow.setTabOrder(self.GroundLineEdit, self.ConstructConnectionsButton)
        MainWindow.setTabOrder(self.ConstructConnectionsButton, self.PortViewComboBox)
        MainWindow.setTabOrder(self.PortViewComboBox, self.TimeRangeHorizontalSlider)
        MainWindow.setTabOrder(self.TimeRangeHorizontalSlider, self.TimeRangeLineEdit)
        MainWindow.setTabOrder(self.TimeRangeLineEdit, self.TimesLineEdit)
        MainWindow.setTabOrder(self.TimesLineEdit, self.PrecisionHorizontalSlider)
        MainWindow.setTabOrder(self.PrecisionHorizontalSlider, self.RunButton)
        MainWindow.setTabOrder(self.RunButton, self.StopButton)
        MainWindow.setTabOrder(self.StopButton, self.CircuitViewer)
        MainWindow.setTabOrder(self.CircuitViewer, self.textOutcomes)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Circuit Analyser"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Viewer (Select one component and press \'r\' to rotate)"))
        self.groupBox.setTitle(_translate("MainWindow", "Circuit Settings"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Components"))
        self.DeleteComponentsButton.setText(_translate("MainWindow", "Delete"))
        self.ClearComponentsButton.setText(_translate("MainWindow", "Clear"))
        item = self.tableWidgetComponents.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidgetComponents.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidgetComponents.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Value"))
        item = self.tableWidgetComponents.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Port (+)"))
        item = self.tableWidgetComponents.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Port (-)"))
        self.AddComponentsButton.setText(_translate("MainWindow", "Add Components"))
        self.EditComponentButton.setText(_translate("MainWindow", "Edit Component"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Components"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Connections"))
        self.Port2LineEdit.setPlaceholderText(_translate("MainWindow", "Port 2"))
        self.SwitchPushButton.setText(_translate("MainWindow", "Upgrade to Switch"))
        self.label.setText(_translate("MainWindow", "Ground"))
        self.DeleteConnectionsButton.setText(_translate("MainWindow", "Delete"))
        self.ClearConnectionsButton.setText(_translate("MainWindow", "Clear"))
        item = self.tableWidgetConnentions.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidgetConnentions.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Port_1"))
        item = self.tableWidgetConnentions.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Port_2"))
        item = self.tableWidgetConnentions.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Time Policy"))
        self.GroundLineEdit.setPlaceholderText(_translate("MainWindow", "Input Ground Port"))
        self.Port1LineEdit.setPlaceholderText(_translate("MainWindow", "Port 1"))
        self.AddConnectionsButton.setText(_translate("MainWindow", "Add Connections"))
        self.ConstructConnectionsButton.setText(_translate("MainWindow", "Construct"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Connections"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Outcomes"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Simulation"))
        self.RunButton.setText(_translate("MainWindow", "Run"))
        self.StopButton.setText(_translate("MainWindow", "Stop"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Oscilloscope"))
        self.PrecisionLabel.setText(_translate("MainWindow", "Precision"))
        self.TimeRangeLabel.setText(_translate("MainWindow", "Time Range"))
        self.TimesLable.setText(_translate("MainWindow", "Times"))
        self.label_2.setText(_translate("MainWindow", "Port View"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuComponents.setTitle(_translate("MainWindow", "Components"))
        self.menuConnections.setTitle(_translate("MainWindow", "Connections"))
        self.menuStimulation.setTitle(_translate("MainWindow", "Stimulation"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAdd.setText(_translate("MainWindow", "Add..."))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionAdd_2.setText(_translate("MainWindow", "Add"))
        self.actionClear_2.setText(_translate("MainWindow", "Clear"))
        self.actionEdit.setText(_translate("MainWindow", "Edit"))
        self.actionRun_Stimulation.setText(_translate("MainWindow", "Run Stimulation"))
        self.actionStop_Stimulation.setText(_translate("MainWindow", "Stop Stimulation"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About..."))
from DrawView import DrawView
from Matplotlibwidget import MatplotlibWidget
