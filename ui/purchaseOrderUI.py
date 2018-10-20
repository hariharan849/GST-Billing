# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\purchaseOrderUI.ui'
#
# Created: Sat Oct 13 11:54:34 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PurchaseOrder(object):
    def setupUi(self, PurchaseOrder):
        PurchaseOrder.setObjectName("PurchaseOrder")
        PurchaseOrder.resize(1716, 734)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PurchaseOrder.sizePolicy().hasHeightForWidth())
        PurchaseOrder.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtGui.QGridLayout(PurchaseOrder)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = Header(PurchaseOrder)
        self.widget.setObjectName("widget")
        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 4)
        self.groupBox = QtGui.QGroupBox(PurchaseOrder)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.customerNameLabel = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customerNameLabel.sizePolicy().hasHeightForWidth())
        self.customerNameLabel.setSizePolicy(sizePolicy)
        self.customerNameLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.customerNameLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.customerNameLabel.setObjectName("customerNameLabel")
        self.gridLayout.addWidget(self.customerNameLabel, 0, 0, 1, 1)
        self.customerNameValue = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customerNameValue.sizePolicy().hasHeightForWidth())
        self.customerNameValue.setSizePolicy(sizePolicy)
        self.customerNameValue.setMinimumSize(QtCore.QSize(200, 35))
        self.customerNameValue.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.customerNameValue.setObjectName("customerNameValue")
        self.gridLayout.addWidget(self.customerNameValue, 0, 1, 1, 1)
        self.PONoLabel = QtGui.QLabel(self.groupBox)
        self.PONoLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.PONoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PONoLabel.setObjectName("PONoLabel")
        self.gridLayout.addWidget(self.PONoLabel, 0, 2, 1, 1)
        self.poNoValue = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.poNoValue.sizePolicy().hasHeightForWidth())
        self.poNoValue.setSizePolicy(sizePolicy)
        self.poNoValue.setMinimumSize(QtCore.QSize(250, 30))
        self.poNoValue.setReadOnly(False)
        self.poNoValue.setObjectName("poNoValue")
        self.gridLayout.addWidget(self.poNoValue, 0, 3, 1, 1)
        self.PODatelabel = QtGui.QLabel(self.groupBox)
        self.PODatelabel.setMinimumSize(QtCore.QSize(150, 30))
        self.PODatelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PODatelabel.setObjectName("PODatelabel")
        self.gridLayout.addWidget(self.PODatelabel, 0, 4, 1, 1)
        self.poDateValue = QtGui.QDateEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.poDateValue.sizePolicy().hasHeightForWidth())
        self.poDateValue.setSizePolicy(sizePolicy)
        self.poDateValue.setMinimumSize(QtCore.QSize(150, 30))
        self.poDateValue.setCalendarPopup(True)
        self.poDateValue.setObjectName("poDateValue")
        self.gridLayout.addWidget(self.poDateValue, 0, 5, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 3)
        self.addButton = QtGui.QPushButton(PurchaseOrder)
        self.addButton.setMinimumSize(QtCore.QSize(0, 35))
        self.addButton.setObjectName("addButton")
        self.gridLayout_2.addWidget(self.addButton, 2, 0, 1, 1)
        self.removeButton = QtGui.QPushButton(PurchaseOrder)
        self.removeButton.setMinimumSize(QtCore.QSize(0, 35))
        self.removeButton.setObjectName("removeButton")
        self.gridLayout_2.addWidget(self.removeButton, 2, 1, 1, 1)
        self.clearButton = QtGui.QPushButton(PurchaseOrder)
        self.clearButton.setMinimumSize(QtCore.QSize(0, 35))
        self.clearButton.setObjectName("clearButton")
        self.gridLayout_2.addWidget(self.clearButton, 2, 2, 1, 1)
        self.importButton = QtGui.QPushButton(PurchaseOrder)
        self.importButton.setMinimumSize(QtCore.QSize(0, 35))
        self.importButton.setObjectName("importButton")
        self.gridLayout_2.addWidget(self.importButton, 2, 3, 1, 1)
        self.purchaseOrderTable = PurchaseOrderTable(PurchaseOrder)
        self.purchaseOrderTable.setObjectName("purchaseOrderTable")
        self.gridLayout_2.addWidget(self.purchaseOrderTable, 3, 0, 1, 4)
        self.groupBox_3 = QtGui.QGroupBox(PurchaseOrder)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 40))
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 150))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.remarksLabel = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remarksLabel.sizePolicy().hasHeightForWidth())
        self.remarksLabel.setSizePolicy(sizePolicy)
        self.remarksLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.remarksLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.remarksLabel.setObjectName("remarksLabel")
        self.horizontalLayout.addWidget(self.remarksLabel)
        self.remarksValue = QtGui.QTextEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remarksValue.sizePolicy().hasHeightForWidth())
        self.remarksValue.setSizePolicy(sizePolicy)
        self.remarksValue.setMinimumSize(QtCore.QSize(350, 50))
        self.remarksValue.setMaximumSize(QtCore.QSize(16777215, 50))
        self.remarksValue.setObjectName("remarksValue")
        self.horizontalLayout.addWidget(self.remarksValue)
        self.saveButton = QtGui.QPushButton(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setMinimumSize(QtCore.QSize(300, 35))
        self.saveButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.discardButton = QtGui.QPushButton(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.discardButton.sizePolicy().hasHeightForWidth())
        self.discardButton.setSizePolicy(sizePolicy)
        self.discardButton.setMinimumSize(QtCore.QSize(300, 35))
        self.discardButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.discardButton.setObjectName("discardButton")
        self.horizontalLayout.addWidget(self.discardButton)
        self.gridLayout_2.addWidget(self.groupBox_3, 4, 0, 1, 4)

        self.retranslateUi(PurchaseOrder)
        QtCore.QMetaObject.connectSlotsByName(PurchaseOrder)

    def retranslateUi(self, PurchaseOrder):
        PurchaseOrder.setWindowTitle(QtGui.QApplication.translate("PurchaseOrder", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.customerNameLabel.setText(QtGui.QApplication.translate("PurchaseOrder", "Customer Name", None, QtGui.QApplication.UnicodeUTF8))
        self.PONoLabel.setText(QtGui.QApplication.translate("PurchaseOrder", "PO no", None, QtGui.QApplication.UnicodeUTF8))
        self.PODatelabel.setText(QtGui.QApplication.translate("PurchaseOrder", "PO Date", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("PurchaseOrder", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("PurchaseOrder", "Clear Selected Row", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setText(QtGui.QApplication.translate("PurchaseOrder", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.importButton.setText(QtGui.QApplication.translate("PurchaseOrder", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.remarksLabel.setText(QtGui.QApplication.translate("PurchaseOrder", "Remarks", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("PurchaseOrder", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.discardButton.setText(QtGui.QApplication.translate("PurchaseOrder", "Discard", None, QtGui.QApplication.UnicodeUTF8))

from _views.purchaseOrderTableView import PurchaseOrderTable
from _widgets.header import Header