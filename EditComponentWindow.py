# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EditComponentWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditComponentWin(object):
    def setupUi(self, EditComponentWin):
        EditComponentWin.setObjectName("EditComponentWin")
        EditComponentWin.setWindowModality(QtCore.Qt.ApplicationModal)
        EditComponentWin.resize(266, 251)
        EditComponentWin.setMinimumSize(QtCore.QSize(266, 251))
        EditComponentWin.setMaximumSize(QtCore.QSize(266, 251))
        self.groupBox = QtWidgets.QGroupBox(EditComponentWin)
        self.groupBox.setGeometry(QtCore.QRect(11, 11, 244, 229))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.NewValueUnitLineEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NewValueUnitLineEdit.sizePolicy().hasHeightForWidth())
        self.NewValueUnitLineEdit.setSizePolicy(sizePolicy)
        self.NewValueUnitLineEdit.setReadOnly(True)
        self.NewValueUnitLineEdit.setObjectName("NewValueUnitLineEdit")
        self.gridLayout_2.addWidget(self.NewValueUnitLineEdit, 1, 2, 1, 1)
        self.NewFreqLineEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NewFreqLineEdit.sizePolicy().hasHeightForWidth())
        self.NewFreqLineEdit.setSizePolicy(sizePolicy)
        self.NewFreqLineEdit.setObjectName("NewFreqLineEdit")
        self.gridLayout_2.addWidget(self.NewFreqLineEdit, 2, 1, 1, 1)
        self.NewNameLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.NewNameLineEdit.setObjectName("NewNameLineEdit")
        self.gridLayout_2.addWidget(self.NewNameLineEdit, 0, 1, 1, 2)
        self.NewValueLineEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NewValueLineEdit.sizePolicy().hasHeightForWidth())
        self.NewValueLineEdit.setSizePolicy(sizePolicy)
        self.NewValueLineEdit.setObjectName("NewValueLineEdit")
        self.gridLayout_2.addWidget(self.NewValueLineEdit, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.NewFreqUnitLineEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NewFreqUnitLineEdit.sizePolicy().hasHeightForWidth())
        self.NewFreqUnitLineEdit.setSizePolicy(sizePolicy)
        self.NewFreqUnitLineEdit.setReadOnly(True)
        self.NewFreqUnitLineEdit.setObjectName("NewFreqUnitLineEdit")
        self.gridLayout_2.addWidget(self.NewFreqUnitLineEdit, 2, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setDefault(True)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 3, 1, 1, 2)

        self.retranslateUi(EditComponentWin)
        self.pushButton.clicked.connect(EditComponentWin.accept)
        QtCore.QMetaObject.connectSlotsByName(EditComponentWin)

    def retranslateUi(self, EditComponentWin):
        _translate = QtCore.QCoreApplication.translate
        EditComponentWin.setWindowTitle(_translate("EditComponentWin", "Edit..."))
        self.groupBox.setTitle(_translate("EditComponentWin", "Edit Component"))
        self.label_2.setText(_translate("EditComponentWin", "Value"))
        self.NewFreqLineEdit.setPlaceholderText(_translate("EditComponentWin", "New Frequency"))
        self.NewNameLineEdit.setPlaceholderText(_translate("EditComponentWin", "Enter a new name"))
        self.NewValueLineEdit.setPlaceholderText(_translate("EditComponentWin", "New value"))
        self.label.setText(_translate("EditComponentWin", "Name"))
        self.NewFreqUnitLineEdit.setText(_translate("EditComponentWin", "Hz"))
        self.pushButton.setText(_translate("EditComponentWin", "Modify"))
