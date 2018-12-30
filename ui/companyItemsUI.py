# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\companyItemsUI.ui'
#
# Created: Sat Nov 24 16:31:41 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_companyItem(object):
    def setupUi(self, companyItem):
        companyItem.setObjectName("companyItem")
        companyItem.resize(1694, 689)
        self.gridLayout_3 = QtGui.QGridLayout(companyItem)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.widget = Header(companyItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 100))
        self.widget.setObjectName("widget")
        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 2)
        self.inputGroupBox = QtGui.QGroupBox(companyItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputGroupBox.sizePolicy().hasHeightForWidth())
        self.inputGroupBox.setSizePolicy(sizePolicy)
        self.inputGroupBox.setCheckable(False)
        self.inputGroupBox.setObjectName("inputGroupBox")
        self.gridLayout = QtGui.QGridLayout(self.inputGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.itemCodeLabel = QtGui.QLabel(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itemCodeLabel.sizePolicy().hasHeightForWidth())
        self.itemCodeLabel.setSizePolicy(sizePolicy)
        self.itemCodeLabel.setMinimumSize(QtCore.QSize(200, 35))
        self.itemCodeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.itemCodeLabel.setObjectName("itemCodeLabel")
        self.horizontalLayout_3.addWidget(self.itemCodeLabel)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.itemCodeValue = QtGui.QLineEdit(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itemCodeValue.sizePolicy().hasHeightForWidth())
        self.itemCodeValue.setSizePolicy(sizePolicy)
        self.itemCodeValue.setMinimumSize(QtCore.QSize(200, 35))
        self.itemCodeValue.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.itemCodeValue.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.itemCodeValue.setObjectName("itemCodeValue")
        self.verticalLayout_2.addWidget(self.itemCodeValue)
        self.codeMandLabel = QtGui.QLabel(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.codeMandLabel.sizePolicy().hasHeightForWidth())
        self.codeMandLabel.setSizePolicy(sizePolicy)
        self.codeMandLabel.setMinimumSize(QtCore.QSize(200, 30))
        self.codeMandLabel.setStyleSheet("QLabel { color : red; }")
        self.codeMandLabel.setObjectName("codeMandLabel")
        self.verticalLayout_2.addWidget(self.codeMandLabel)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.itemNameLabel = QtGui.QLabel(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itemNameLabel.sizePolicy().hasHeightForWidth())
        self.itemNameLabel.setSizePolicy(sizePolicy)
        self.itemNameLabel.setMinimumSize(QtCore.QSize(200, 35))
        self.itemNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.itemNameLabel.setObjectName("itemNameLabel")
        self.horizontalLayout_4.addWidget(self.itemNameLabel)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.itemNameValue = QtGui.QLineEdit(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itemNameValue.sizePolicy().hasHeightForWidth())
        self.itemNameValue.setSizePolicy(sizePolicy)
        self.itemNameValue.setMinimumSize(QtCore.QSize(200, 35))
        self.itemNameValue.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.itemNameValue.setObjectName("itemNameValue")
        self.verticalLayout_3.addWidget(self.itemNameValue)
        self.nameMandLabel = QtGui.QLabel(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameMandLabel.sizePolicy().hasHeightForWidth())
        self.nameMandLabel.setSizePolicy(sizePolicy)
        self.nameMandLabel.setMinimumSize(QtCore.QSize(200, 30))
        self.nameMandLabel.setStyleSheet("QLabel { color : red; }")
        self.nameMandLabel.setObjectName("nameMandLabel")
        self.verticalLayout_3.addWidget(self.nameMandLabel)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.hsnCodeLabel = QtGui.QLabel(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hsnCodeLabel.sizePolicy().hasHeightForWidth())
        self.hsnCodeLabel.setSizePolicy(sizePolicy)
        self.hsnCodeLabel.setMinimumSize(QtCore.QSize(200, 35))
        self.hsnCodeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hsnCodeLabel.setObjectName("hsnCodeLabel")
        self.horizontalLayout_5.addWidget(self.hsnCodeLabel)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.hsnCodeValue = QtGui.QLineEdit(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hsnCodeValue.sizePolicy().hasHeightForWidth())
        self.hsnCodeValue.setSizePolicy(sizePolicy)
        self.hsnCodeValue.setMinimumSize(QtCore.QSize(200, 35))
        self.hsnCodeValue.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.hsnCodeValue.setObjectName("hsnCodeValue")
        self.verticalLayout_4.addWidget(self.hsnCodeValue)
        self.hsnMandLabel = QtGui.QLabel(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hsnMandLabel.sizePolicy().hasHeightForWidth())
        self.hsnMandLabel.setSizePolicy(sizePolicy)
        self.hsnMandLabel.setMinimumSize(QtCore.QSize(200, 30))
        self.hsnMandLabel.setStyleSheet("QLabel { color : red; }")
        self.hsnMandLabel.setObjectName("hsnMandLabel")
        self.verticalLayout_4.addWidget(self.hsnMandLabel)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 0, 1, 2)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.quantityLabel = QtGui.QLabel(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quantityLabel.sizePolicy().hasHeightForWidth())
        self.quantityLabel.setSizePolicy(sizePolicy)
        self.quantityLabel.setMinimumSize(QtCore.QSize(200, 35))
        self.quantityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.quantityLabel.setObjectName("quantityLabel")
        self.horizontalLayout_6.addWidget(self.quantityLabel)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.quantityValue = QtGui.QLineEdit(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quantityValue.sizePolicy().hasHeightForWidth())
        self.quantityValue.setSizePolicy(sizePolicy)
        self.quantityValue.setMinimumSize(QtCore.QSize(200, 35))
        self.quantityValue.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.quantityValue.setObjectName("quantityValue")
        self.verticalLayout_5.addWidget(self.quantityValue)
        self.quantityMandLabel = QtGui.QLabel(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quantityMandLabel.sizePolicy().hasHeightForWidth())
        self.quantityMandLabel.setSizePolicy(sizePolicy)
        self.quantityMandLabel.setMinimumSize(QtCore.QSize(200, 30))
        self.quantityMandLabel.setStyleSheet("QLabel { color : red; }")
        self.quantityMandLabel.setObjectName("quantityMandLabel")
        self.verticalLayout_5.addWidget(self.quantityMandLabel)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.gridLayout.addLayout(self.horizontalLayout_6, 3, 0, 1, 2)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.itemPriceLabel = QtGui.QLabel(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itemPriceLabel.sizePolicy().hasHeightForWidth())
        self.itemPriceLabel.setSizePolicy(sizePolicy)
        self.itemPriceLabel.setMinimumSize(QtCore.QSize(200, 35))
        self.itemPriceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.itemPriceLabel.setObjectName("itemPriceLabel")
        self.horizontalLayout_7.addWidget(self.itemPriceLabel)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.itemPriceValue = QtGui.QLineEdit(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itemPriceValue.sizePolicy().hasHeightForWidth())
        self.itemPriceValue.setSizePolicy(sizePolicy)
        self.itemPriceValue.setMinimumSize(QtCore.QSize(200, 35))
        self.itemPriceValue.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.itemPriceValue.setObjectName("itemPriceValue")
        self.verticalLayout_6.addWidget(self.itemPriceValue)
        self.priceMandLabel = QtGui.QLabel(self.inputGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.priceMandLabel.sizePolicy().hasHeightForWidth())
        self.priceMandLabel.setSizePolicy(sizePolicy)
        self.priceMandLabel.setMinimumSize(QtCore.QSize(200, 30))
        self.priceMandLabel.setStyleSheet("QLabel { color : red; }")
        self.priceMandLabel.setObjectName("priceMandLabel")
        self.verticalLayout_6.addWidget(self.priceMandLabel)
        self.horizontalLayout_7.addLayout(self.verticalLayout_6)
        self.gridLayout.addLayout(self.horizontalLayout_7, 4, 0, 1, 2)
        self.saveButton = QtGui.QPushButton(self.inputGroupBox)
        self.saveButton.setMinimumSize(QtCore.QSize(200, 35))
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 5, 0, 1, 1)
        self.discardButton = QtGui.QPushButton(self.inputGroupBox)
        self.discardButton.setMinimumSize(QtCore.QSize(200, 35))
        self.discardButton.setObjectName("discardButton")
        self.gridLayout.addWidget(self.discardButton, 5, 1, 1, 1)
        self.gridLayout_3.addWidget(self.inputGroupBox, 1, 0, 2, 1)
        self.groupBox = QtGui.QGroupBox(companyItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 100))
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.voucherNoLabel_2 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voucherNoLabel_2.sizePolicy().hasHeightForWidth())
        self.voucherNoLabel_2.setSizePolicy(sizePolicy)
        self.voucherNoLabel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.voucherNoLabel_2.setObjectName("voucherNoLabel_2")
        self.horizontalLayout.addWidget(self.voucherNoLabel_2)
        self.searchItemCodeValue = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchItemCodeValue.sizePolicy().hasHeightForWidth())
        self.searchItemCodeValue.setSizePolicy(sizePolicy)
        self.searchItemCodeValue.setMinimumSize(QtCore.QSize(450, 35))
        self.searchItemCodeValue.setMaximumSize(QtCore.QSize(400, 16777215))
        self.searchItemCodeValue.setObjectName("searchItemCodeValue")
        self.horizontalLayout.addWidget(self.searchItemCodeValue)
        self.voucherNoLabel_3 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voucherNoLabel_3.sizePolicy().hasHeightForWidth())
        self.voucherNoLabel_3.setSizePolicy(sizePolicy)
        self.voucherNoLabel_3.setAlignment(QtCore.Qt.AlignCenter)
        self.voucherNoLabel_3.setObjectName("voucherNoLabel_3")
        self.horizontalLayout.addWidget(self.voucherNoLabel_3)
        self.searchNameValue = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchNameValue.sizePolicy().hasHeightForWidth())
        self.searchNameValue.setSizePolicy(sizePolicy)
        self.searchNameValue.setMinimumSize(QtCore.QSize(450, 35))
        self.searchNameValue.setMaximumSize(QtCore.QSize(400, 16777215))
        self.searchNameValue.setObjectName("searchNameValue")
        self.horizontalLayout.addWidget(self.searchNameValue)
        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.searchButton = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMinimumSize(QtCore.QSize(400, 35))
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_2.addWidget(self.searchButton)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 1, 1, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 3)
        self.removeButton = QtGui.QPushButton(companyItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeButton.sizePolicy().hasHeightForWidth())
        self.removeButton.setSizePolicy(sizePolicy)
        self.removeButton.setMinimumSize(QtCore.QSize(0, 35))
        self.removeButton.setObjectName("removeButton")
        self.gridLayout_2.addWidget(self.removeButton, 1, 0, 1, 1)
        self.clearButton = QtGui.QPushButton(companyItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearButton.sizePolicy().hasHeightForWidth())
        self.clearButton.setSizePolicy(sizePolicy)
        self.clearButton.setMinimumSize(QtCore.QSize(0, 35))
        self.clearButton.setObjectName("clearButton")
        self.gridLayout_2.addWidget(self.clearButton, 1, 1, 1, 1)
        self.importButton = QtGui.QPushButton(companyItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importButton.sizePolicy().hasHeightForWidth())
        self.importButton.setSizePolicy(sizePolicy)
        self.importButton.setMinimumSize(QtCore.QSize(0, 35))
        self.importButton.setObjectName("importButton")
        self.gridLayout_2.addWidget(self.importButton, 1, 2, 1, 1)
        self.companyItemsTable = CompanyItemTable(companyItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.companyItemsTable.sizePolicy().hasHeightForWidth())
        self.companyItemsTable.setSizePolicy(sizePolicy)
        self.companyItemsTable.setObjectName("companyItemsTable")
        self.gridLayout_2.addWidget(self.companyItemsTable, 2, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(758, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 2)
        self.saveTableData = QtGui.QPushButton(companyItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveTableData.sizePolicy().hasHeightForWidth())
        self.saveTableData.setSizePolicy(sizePolicy)
        self.saveTableData.setMinimumSize(QtCore.QSize(300, 35))
        self.saveTableData.setObjectName("saveTableData")
        self.gridLayout_2.addWidget(self.saveTableData, 3, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 1, 1, 1)

        self.retranslateUi(companyItem)
        QtCore.QMetaObject.connectSlotsByName(companyItem)

    def retranslateUi(self, companyItem):
        companyItem.setWindowTitle(QtGui.QApplication.translate("companyItem", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.inputGroupBox.setTitle(QtGui.QApplication.translate("companyItem", "Sales Items", None, QtGui.QApplication.UnicodeUTF8))
        self.itemCodeLabel.setText(QtGui.QApplication.translate("companyItem", "Item Code", None, QtGui.QApplication.UnicodeUTF8))
        self.itemCodeValue.setPlaceholderText(QtGui.QApplication.translate("companyItem", "Enter Item Code", None, QtGui.QApplication.UnicodeUTF8))
        self.codeMandLabel.setText(QtGui.QApplication.translate("companyItem", "* Item Code is Mandatory", None, QtGui.QApplication.UnicodeUTF8))
        self.itemNameLabel.setText(QtGui.QApplication.translate("companyItem", "Item Name", None, QtGui.QApplication.UnicodeUTF8))
        self.itemNameValue.setPlaceholderText(QtGui.QApplication.translate("companyItem", "Enter Item name", None, QtGui.QApplication.UnicodeUTF8))
        self.nameMandLabel.setText(QtGui.QApplication.translate("companyItem", "* Item Name is Mandatory", None, QtGui.QApplication.UnicodeUTF8))
        self.hsnCodeLabel.setText(QtGui.QApplication.translate("companyItem", "HSN Code", None, QtGui.QApplication.UnicodeUTF8))
        self.hsnCodeValue.setPlaceholderText(QtGui.QApplication.translate("companyItem", "Enter HSN Code", None, QtGui.QApplication.UnicodeUTF8))
        self.hsnMandLabel.setText(QtGui.QApplication.translate("companyItem", "* HSN Code is Mandatory", None, QtGui.QApplication.UnicodeUTF8))
        self.quantityLabel.setText(QtGui.QApplication.translate("companyItem", "Quantity", None, QtGui.QApplication.UnicodeUTF8))
        self.quantityValue.setPlaceholderText(QtGui.QApplication.translate("companyItem", "Enter quantity", None, QtGui.QApplication.UnicodeUTF8))
        self.quantityMandLabel.setText(QtGui.QApplication.translate("companyItem", "* Quantity is Mandatory", None, QtGui.QApplication.UnicodeUTF8))
        self.itemPriceLabel.setText(QtGui.QApplication.translate("companyItem", "Item Price", None, QtGui.QApplication.UnicodeUTF8))
        self.itemPriceValue.setPlaceholderText(QtGui.QApplication.translate("companyItem", "Enter item price", None, QtGui.QApplication.UnicodeUTF8))
        self.priceMandLabel.setText(QtGui.QApplication.translate("companyItem", "* Item Price is Mandatory", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("companyItem", "Save Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.discardButton.setText(QtGui.QApplication.translate("companyItem", "Discard", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("companyItem", "Search ", None, QtGui.QApplication.UnicodeUTF8))
        self.voucherNoLabel_2.setText(QtGui.QApplication.translate("companyItem", "Enter ItemCode", None, QtGui.QApplication.UnicodeUTF8))
        self.searchItemCodeValue.setPlaceholderText(QtGui.QApplication.translate("companyItem", "Enter ItemCode", None, QtGui.QApplication.UnicodeUTF8))
        self.voucherNoLabel_3.setText(QtGui.QApplication.translate("companyItem", "Enter Item Name", None, QtGui.QApplication.UnicodeUTF8))
        self.searchNameValue.setPlaceholderText(QtGui.QApplication.translate("companyItem", "Enter Name", None, QtGui.QApplication.UnicodeUTF8))
        self.searchButton.setText(QtGui.QApplication.translate("companyItem", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("companyItem", "Remove Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setText(QtGui.QApplication.translate("companyItem", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.importButton.setText(QtGui.QApplication.translate("companyItem", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.saveTableData.setText(QtGui.QApplication.translate("companyItem", "Save Table", None, QtGui.QApplication.UnicodeUTF8))

from _views.companyItemsTableView import CompanyItemTable
from _widgets.header import Header
