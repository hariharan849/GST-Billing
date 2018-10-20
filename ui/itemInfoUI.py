# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'itemInfoUI.ui'
#
# Created: Thu Sep 13 11:44:51 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_itemInfoWidget(object):
    def setupUi(self, itemInfoWidget):
        itemInfoWidget.setObjectName("itemInfoWidget")
        itemInfoWidget.resize(780, 300)
        self.gridLayout = QtGui.QGridLayout(itemInfoWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.itemNameLabel = QtGui.QLabel(itemInfoWidget)
        self.itemNameLabel.setMinimumSize(QtCore.QSize(0, 35))
        self.itemNameLabel.setObjectName("itemNameLabel")
        self.gridLayout.addWidget(self.itemNameLabel, 0, 0, 1, 1)
        self.itemNameValue = QtGui.QLineEdit(itemInfoWidget)
        self.itemNameValue.setMinimumSize(QtCore.QSize(0, 35))
        self.itemNameValue.setObjectName("itemNameValue")
        self.gridLayout.addWidget(self.itemNameValue, 0, 1, 1, 1)
        self.searchButton = QtGui.QPushButton(itemInfoWidget)
        self.searchButton.setMinimumSize(QtCore.QSize(0, 35))
        self.searchButton.setObjectName("searchButton")
        self.gridLayout.addWidget(self.searchButton, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(263, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.itemTable = ItemReportTable(itemInfoWidget)
        self.itemTable.setObjectName("itemTable")
        self.gridLayout.addWidget(self.itemTable, 1, 0, 1, 4)
        self.label = QtGui.QLabel(itemInfoWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.remarksValue = QtGui.QTextEdit(itemInfoWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.remarksValue.sizePolicy().hasHeightForWidth())
        self.remarksValue.setSizePolicy(sizePolicy)
        self.remarksValue.setMinimumSize(QtCore.QSize(0, 20))
        self.remarksValue.setMaximumSize(QtCore.QSize(16777215, 50))
        self.remarksValue.setObjectName("remarksValue")
        self.gridLayout.addWidget(self.remarksValue, 2, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(263, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 3, 1, 1)

        self.retranslateUi(itemInfoWidget)
        QtCore.QMetaObject.connectSlotsByName(itemInfoWidget)

    def retranslateUi(self, itemInfoWidget):
        itemInfoWidget.setWindowTitle(QtGui.QApplication.translate("itemInfoWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.itemNameLabel.setText(QtGui.QApplication.translate("itemInfoWidget", "Item Name", None, QtGui.QApplication.UnicodeUTF8))
        self.searchButton.setText(QtGui.QApplication.translate("itemInfoWidget", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("itemInfoWidget", "Remarks", None, QtGui.QApplication.UnicodeUTF8))

from _views.itemReportTableView import ItemReportTable
