# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'performaInvoiceUI.ui'
#
# Created: Wed Sep 26 20:38:35 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SalesInvoice(object):
    def setupUi(self, SalesInvoice):
        SalesInvoice.setObjectName("SalesInvoice")
        SalesInvoice.resize(1716, 797)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SalesInvoice.sizePolicy().hasHeightForWidth())
        SalesInvoice.setSizePolicy(sizePolicy)
        self.gridLayout_7 = QtGui.QGridLayout(SalesInvoice)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.widget = Header(SalesInvoice)
        self.widget.setObjectName("widget")
        self.gridLayout_7.addWidget(self.widget, 0, 0, 1, 2)
        self.groupBox = QtGui.QGroupBox(SalesInvoice)
        self.groupBox.setTitle("")
        self.groupBox.setCheckable(True)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.customerNameLabel = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customerNameLabel.sizePolicy().hasHeightForWidth())
        self.customerNameLabel.setSizePolicy(sizePolicy)
        self.customerNameLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.customerNameLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.customerNameLabel.setObjectName("customerNameLabel")
        self.verticalLayout_3.addWidget(self.customerNameLabel)
        self.customerNameValue = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customerNameValue.sizePolicy().hasHeightForWidth())
        self.customerNameValue.setSizePolicy(sizePolicy)
        self.customerNameValue.setMinimumSize(QtCore.QSize(350, 35))
        self.customerNameValue.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.customerNameValue.setObjectName("customerNameValue")
        self.verticalLayout_3.addWidget(self.customerNameValue)
        self.customerAddressLabel = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customerAddressLabel.sizePolicy().hasHeightForWidth())
        self.customerAddressLabel.setSizePolicy(sizePolicy)
        self.customerAddressLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.customerAddressLabel.setObjectName("customerAddressLabel")
        self.verticalLayout_3.addWidget(self.customerAddressLabel)
        self.customerAddressValue = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customerAddressValue.sizePolicy().hasHeightForWidth())
        self.customerAddressValue.setSizePolicy(sizePolicy)
        self.customerAddressValue.setMinimumSize(QtCore.QSize(350, 35))
        self.customerAddressValue.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.customerAddressValue.setObjectName("customerAddressValue")
        self.verticalLayout_3.addWidget(self.customerAddressValue)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gstinLabel = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gstinLabel.sizePolicy().hasHeightForWidth())
        self.gstinLabel.setSizePolicy(sizePolicy)
        self.gstinLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.gstinLabel.setObjectName("gstinLabel")
        self.gridLayout_3.addWidget(self.gstinLabel, 0, 0, 1, 1)
        self.gstinValue = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gstinValue.sizePolicy().hasHeightForWidth())
        self.gstinValue.setSizePolicy(sizePolicy)
        self.gstinValue.setMinimumSize(QtCore.QSize(150, 35))
        self.gstinValue.setObjectName("gstinValue")
        self.gridLayout_3.addWidget(self.gstinValue, 0, 1, 1, 1)
        self.stateCodeLabel = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stateCodeLabel.sizePolicy().hasHeightForWidth())
        self.stateCodeLabel.setSizePolicy(sizePolicy)
        self.stateCodeLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.stateCodeLabel.setObjectName("stateCodeLabel")
        self.gridLayout_3.addWidget(self.stateCodeLabel, 1, 0, 1, 1)
        self.stateCodeValue = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stateCodeValue.sizePolicy().hasHeightForWidth())
        self.stateCodeValue.setSizePolicy(sizePolicy)
        self.stateCodeValue.setMinimumSize(QtCore.QSize(150, 35))
        self.stateCodeValue.setObjectName("stateCodeValue")
        self.gridLayout_3.addWidget(self.stateCodeValue, 1, 1, 1, 1)
        self.paidByLabel = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.paidByLabel.sizePolicy().hasHeightForWidth())
        self.paidByLabel.setSizePolicy(sizePolicy)
        self.paidByLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.paidByLabel.setObjectName("paidByLabel")
        self.gridLayout_3.addWidget(self.paidByLabel, 2, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_3.addWidget(self.comboBox, 2, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(SalesInvoice)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setCheckable(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.billNoLabel = QtGui.QLabel(self.groupBox_2)
        self.billNoLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.billNoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.billNoLabel.setObjectName("billNoLabel")
        self.gridLayout_4.addWidget(self.billNoLabel, 0, 0, 1, 1)
        self.billNoValue = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.billNoValue.sizePolicy().hasHeightForWidth())
        self.billNoValue.setSizePolicy(sizePolicy)
        self.billNoValue.setMinimumSize(QtCore.QSize(250, 30))
        self.billNoValue.setReadOnly(True)
        self.billNoValue.setObjectName("billNoValue")
        self.gridLayout_4.addWidget(self.billNoValue, 0, 1, 1, 1)
        self.billDatelabel = QtGui.QLabel(self.groupBox_2)
        self.billDatelabel.setMinimumSize(QtCore.QSize(150, 30))
        self.billDatelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.billDatelabel.setObjectName("billDatelabel")
        self.gridLayout_4.addWidget(self.billDatelabel, 0, 2, 1, 1)
        self.billDateValue = QtGui.QDateEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.billDateValue.sizePolicy().hasHeightForWidth())
        self.billDateValue.setSizePolicy(sizePolicy)
        self.billDateValue.setMinimumSize(QtCore.QSize(150, 30))
        self.billDateValue.setCalendarPopup(True)
        self.billDateValue.setObjectName("billDateValue")
        self.gridLayout_4.addWidget(self.billDateValue, 0, 3, 1, 1)
        self.poNoLabel = QtGui.QLabel(self.groupBox_2)
        self.poNoLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.poNoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.poNoLabel.setObjectName("poNoLabel")
        self.gridLayout_4.addWidget(self.poNoLabel, 1, 0, 1, 1)
        self.poNoValue = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.poNoValue.sizePolicy().hasHeightForWidth())
        self.poNoValue.setSizePolicy(sizePolicy)
        self.poNoValue.setMinimumSize(QtCore.QSize(150, 30))
        self.poNoValue.setObjectName("poNoValue")
        self.gridLayout_4.addWidget(self.poNoValue, 1, 1, 1, 1)
        self.poDatelabel = QtGui.QLabel(self.groupBox_2)
        self.poDatelabel.setMinimumSize(QtCore.QSize(150, 30))
        self.poDatelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.poDatelabel.setObjectName("poDatelabel")
        self.gridLayout_4.addWidget(self.poDatelabel, 1, 2, 1, 1)
        self.poDateValue = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.poDateValue.sizePolicy().hasHeightForWidth())
        self.poDateValue.setSizePolicy(sizePolicy)
        self.poDateValue.setMinimumSize(QtCore.QSize(150, 30))
        self.poDateValue.setObjectName("poDateValue")
        self.gridLayout_4.addWidget(self.poDateValue, 1, 3, 1, 1)
        self.vendorCodeLabel = QtGui.QLabel(self.groupBox_2)
        self.vendorCodeLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.vendorCodeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.vendorCodeLabel.setObjectName("vendorCodeLabel")
        self.gridLayout_4.addWidget(self.vendorCodeLabel, 2, 0, 1, 1)
        self.vendorCodeValue = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vendorCodeValue.sizePolicy().hasHeightForWidth())
        self.vendorCodeValue.setSizePolicy(sizePolicy)
        self.vendorCodeValue.setMinimumSize(QtCore.QSize(150, 30))
        self.vendorCodeValue.setObjectName("vendorCodeValue")
        self.gridLayout_4.addWidget(self.vendorCodeValue, 2, 1, 1, 1)
        self.paymentTermslabel = QtGui.QLabel(self.groupBox_2)
        self.paymentTermslabel.setMinimumSize(QtCore.QSize(150, 30))
        self.paymentTermslabel.setAlignment(QtCore.Qt.AlignCenter)
        self.paymentTermslabel.setObjectName("paymentTermslabel")
        self.gridLayout_4.addWidget(self.paymentTermslabel, 2, 2, 1, 1)
        self.paymentTermsValue = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.paymentTermsValue.sizePolicy().hasHeightForWidth())
        self.paymentTermsValue.setSizePolicy(sizePolicy)
        self.paymentTermsValue.setMinimumSize(QtCore.QSize(150, 30))
        self.paymentTermsValue.setObjectName("paymentTermsValue")
        self.gridLayout_4.addWidget(self.paymentTermsValue, 2, 3, 1, 1)
        self.dcNoLabel = QtGui.QLabel(self.groupBox_2)
        self.dcNoLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.dcNoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dcNoLabel.setObjectName("dcNoLabel")
        self.gridLayout_4.addWidget(self.dcNoLabel, 3, 0, 1, 1)
        self.dcNoValue = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dcNoValue.sizePolicy().hasHeightForWidth())
        self.dcNoValue.setSizePolicy(sizePolicy)
        self.dcNoValue.setMinimumSize(QtCore.QSize(150, 30))
        self.dcNoValue.setObjectName("dcNoValue")
        self.gridLayout_4.addWidget(self.dcNoValue, 3, 1, 1, 1)
        self.daDateLabel = QtGui.QLabel(self.groupBox_2)
        self.daDateLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.daDateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.daDateLabel.setObjectName("daDateLabel")
        self.gridLayout_4.addWidget(self.daDateLabel, 3, 2, 1, 1)
        self.dcDateValue = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dcDateValue.sizePolicy().hasHeightForWidth())
        self.dcDateValue.setSizePolicy(sizePolicy)
        self.dcDateValue.setMinimumSize(QtCore.QSize(150, 30))
        self.dcDateValue.setObjectName("dcDateValue")
        self.gridLayout_4.addWidget(self.dcDateValue, 3, 3, 1, 1)
        self.vehicleNoLabel = QtGui.QLabel(self.groupBox_2)
        self.vehicleNoLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.vehicleNoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.vehicleNoLabel.setObjectName("vehicleNoLabel")
        self.gridLayout_4.addWidget(self.vehicleNoLabel, 4, 0, 1, 1)
        self.vehicleNoValue = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vehicleNoValue.sizePolicy().hasHeightForWidth())
        self.vehicleNoValue.setSizePolicy(sizePolicy)
        self.vehicleNoValue.setMinimumSize(QtCore.QSize(150, 30))
        self.vehicleNoValue.setObjectName("vehicleNoValue")
        self.gridLayout_4.addWidget(self.vehicleNoValue, 4, 1, 1, 1)
        self.dispatchedlabel = QtGui.QLabel(self.groupBox_2)
        self.dispatchedlabel.setMinimumSize(QtCore.QSize(150, 30))
        self.dispatchedlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dispatchedlabel.setObjectName("dispatchedlabel")
        self.gridLayout_4.addWidget(self.dispatchedlabel, 4, 2, 1, 1)
        self.dispatchedValue = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dispatchedValue.sizePolicy().hasHeightForWidth())
        self.dispatchedValue.setSizePolicy(sizePolicy)
        self.dispatchedValue.setMinimumSize(QtCore.QSize(150, 30))
        self.dispatchedValue.setObjectName("dispatchedValue")
        self.gridLayout_4.addWidget(self.dispatchedValue, 4, 3, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_2, 1, 1, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.addButton = QtGui.QPushButton(SalesInvoice)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(35)
        sizePolicy.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_4.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(SalesInvoice)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(35)
        sizePolicy.setHeightForWidth(self.removeButton.sizePolicy().hasHeightForWidth())
        self.removeButton.setSizePolicy(sizePolicy)
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout_4.addWidget(self.removeButton)
        self.clearButton = QtGui.QPushButton(SalesInvoice)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(35)
        sizePolicy.setHeightForWidth(self.clearButton.sizePolicy().hasHeightForWidth())
        self.clearButton.setSizePolicy(sizePolicy)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout_4.addWidget(self.clearButton)
        self.importButton = QtGui.QPushButton(SalesInvoice)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(35)
        sizePolicy.setHeightForWidth(self.importButton.sizePolicy().hasHeightForWidth())
        self.importButton.setSizePolicy(sizePolicy)
        self.importButton.setObjectName("importButton")
        self.horizontalLayout_4.addWidget(self.importButton)
        self.gridLayout_7.addLayout(self.horizontalLayout_4, 2, 0, 1, 2)
        self.salesInvoiceTable = TableWidget(SalesInvoice)
        self.salesInvoiceTable.setObjectName("salesInvoiceTable")
        self.salesInvoiceTable.setColumnCount(0)
        self.salesInvoiceTable.setRowCount(0)
        self.gridLayout_7.addWidget(self.salesInvoiceTable, 3, 0, 1, 2)
        self.groupBox_3 = QtGui.QGroupBox(SalesInvoice)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 40))
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 150))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setCheckable(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.beforeTaxLabel = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.beforeTaxLabel.sizePolicy().hasHeightForWidth())
        self.beforeTaxLabel.setSizePolicy(sizePolicy)
        self.beforeTaxLabel.setMinimumSize(QtCore.QSize(300, 30))
        self.beforeTaxLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.beforeTaxLabel.setObjectName("beforeTaxLabel")
        self.verticalLayout.addWidget(self.beforeTaxLabel)
        self.beforeTaxValue = QtGui.QLineEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.beforeTaxValue.sizePolicy().hasHeightForWidth())
        self.beforeTaxValue.setSizePolicy(sizePolicy)
        self.beforeTaxValue.setMinimumSize(QtCore.QSize(300, 35))
        self.beforeTaxValue.setObjectName("beforeTaxValue")
        self.verticalLayout.addWidget(self.beforeTaxValue)
        self.afterTaxLabel = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.afterTaxLabel.sizePolicy().hasHeightForWidth())
        self.afterTaxLabel.setSizePolicy(sizePolicy)
        self.afterTaxLabel.setMinimumSize(QtCore.QSize(300, 30))
        self.afterTaxLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.afterTaxLabel.setObjectName("afterTaxLabel")
        self.verticalLayout.addWidget(self.afterTaxLabel)
        self.afterTaxValue = QtGui.QLineEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.afterTaxValue.sizePolicy().hasHeightForWidth())
        self.afterTaxValue.setSizePolicy(sizePolicy)
        self.afterTaxValue.setMinimumSize(QtCore.QSize(300, 35))
        self.afterTaxValue.setObjectName("afterTaxValue")
        self.verticalLayout.addWidget(self.afterTaxValue)
        self.gridLayout_6.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.amountPaidLabel = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amountPaidLabel.sizePolicy().hasHeightForWidth())
        self.amountPaidLabel.setSizePolicy(sizePolicy)
        self.amountPaidLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.amountPaidLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.amountPaidLabel.setObjectName("amountPaidLabel")
        self.horizontalLayout.addWidget(self.amountPaidLabel)
        self.amountPaidValue = QtGui.QLineEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amountPaidValue.sizePolicy().hasHeightForWidth())
        self.amountPaidValue.setSizePolicy(sizePolicy)
        self.amountPaidValue.setMinimumSize(QtCore.QSize(150, 30))
        self.amountPaidValue.setObjectName("amountPaidValue")
        self.horizontalLayout.addWidget(self.amountPaidValue)
        self.taxValueLabel = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.taxValueLabel.sizePolicy().hasHeightForWidth())
        self.taxValueLabel.setSizePolicy(sizePolicy)
        self.taxValueLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.taxValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.taxValueLabel.setObjectName("taxValueLabel")
        self.horizontalLayout.addWidget(self.taxValueLabel)
        self.taxValue = QtGui.QLineEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.taxValue.sizePolicy().hasHeightForWidth())
        self.taxValue.setSizePolicy(sizePolicy)
        self.taxValue.setMinimumSize(QtCore.QSize(150, 30))
        self.taxValue.setObjectName("taxValue")
        self.horizontalLayout.addWidget(self.taxValue)
        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.performaLayout = QtGui.QHBoxLayout()
        self.performaLayout.setObjectName("performaLayout")
        self.deliveryChallan = QtGui.QCheckBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deliveryChallan.sizePolicy().hasHeightForWidth())
        self.deliveryChallan.setSizePolicy(sizePolicy)
        self.deliveryChallan.setObjectName("deliveryChallan")
        self.performaLayout.addWidget(self.deliveryChallan)
        self.gridLayout_5.addLayout(self.performaLayout, 1, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 1, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.remarksLabel = QtGui.QLabel(self.groupBox_3)
        self.remarksLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.remarksLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.remarksLabel.setObjectName("remarksLabel")
        self.gridLayout_2.addWidget(self.remarksLabel, 0, 0, 1, 1)
        self.amountWordLabel = QtGui.QLabel(self.groupBox_3)
        self.amountWordLabel.setMinimumSize(QtCore.QSize(150, 30))
        self.amountWordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.amountWordLabel.setObjectName("amountWordLabel")
        self.gridLayout_2.addWidget(self.amountWordLabel, 0, 1, 1, 1)
        self.remarksValue = QtGui.QTextEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remarksValue.sizePolicy().hasHeightForWidth())
        self.remarksValue.setSizePolicy(sizePolicy)
        self.remarksValue.setMinimumSize(QtCore.QSize(350, 40))
        self.remarksValue.setObjectName("remarksValue")
        self.gridLayout_2.addWidget(self.remarksValue, 1, 0, 1, 1)
        self.amountWordsValue = QtGui.QTextEdit(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amountWordsValue.sizePolicy().hasHeightForWidth())
        self.amountWordsValue.setSizePolicy(sizePolicy)
        self.amountWordsValue.setMinimumSize(QtCore.QSize(350, 40))
        self.amountWordsValue.setObjectName("amountWordsValue")
        self.gridLayout_2.addWidget(self.amountWordsValue, 1, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_2, 0, 2, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_3, 4, 0, 1, 2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.printCheckBox = QtGui.QCheckBox(SalesInvoice)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(35)
        sizePolicy.setHeightForWidth(self.printCheckBox.sizePolicy().hasHeightForWidth())
        self.printCheckBox.setSizePolicy(sizePolicy)
        self.printCheckBox.setObjectName("printCheckBox")
        self.horizontalLayout_2.addWidget(self.printCheckBox)
        self.previewButton = QtGui.QPushButton(SalesInvoice)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(35)
        sizePolicy.setHeightForWidth(self.previewButton.sizePolicy().hasHeightForWidth())
        self.previewButton.setSizePolicy(sizePolicy)
        self.previewButton.setObjectName("previewButton")
        self.horizontalLayout_2.addWidget(self.previewButton)
        self.saveButton = QtGui.QPushButton(SalesInvoice)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_2.addWidget(self.saveButton)
        self.discardButton = QtGui.QPushButton(SalesInvoice)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discardButton.sizePolicy().hasHeightForWidth())
        self.discardButton.setSizePolicy(sizePolicy)
        self.discardButton.setObjectName("discardButton")
        self.horizontalLayout_2.addWidget(self.discardButton)
        self.gridLayout_7.addLayout(self.horizontalLayout_2, 5, 0, 1, 2)

        self.retranslateUi(SalesInvoice)
        QtCore.QMetaObject.connectSlotsByName(SalesInvoice)

    def retranslateUi(self, SalesInvoice):
        SalesInvoice.setWindowTitle(QtGui.QApplication.translate("SalesInvoice", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.customerNameLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Customer Name", None, QtGui.QApplication.UnicodeUTF8))
        self.customerNameValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter Customer Name", None, QtGui.QApplication.UnicodeUTF8))
        self.customerAddressLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Customer Address", None, QtGui.QApplication.UnicodeUTF8))
        self.customerAddressValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter Customer Address", None, QtGui.QApplication.UnicodeUTF8))
        self.gstinLabel.setText(QtGui.QApplication.translate("SalesInvoice", "GSTIN", None, QtGui.QApplication.UnicodeUTF8))
        self.gstinValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter GSTIN ", None, QtGui.QApplication.UnicodeUTF8))
        self.stateCodeLabel.setText(QtGui.QApplication.translate("SalesInvoice", "State Code", None, QtGui.QApplication.UnicodeUTF8))
        self.stateCodeValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter State Code", None, QtGui.QApplication.UnicodeUTF8))
        self.paidByLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Paid By", None, QtGui.QApplication.UnicodeUTF8))
        self.billNoLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Bill no", None, QtGui.QApplication.UnicodeUTF8))
        self.billDatelabel.setText(QtGui.QApplication.translate("SalesInvoice", "Bill Date", None, QtGui.QApplication.UnicodeUTF8))
        self.poNoLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Po No", None, QtGui.QApplication.UnicodeUTF8))
        self.poNoValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter PO No", None, QtGui.QApplication.UnicodeUTF8))
        self.poDatelabel.setText(QtGui.QApplication.translate("SalesInvoice", "PO Date", None, QtGui.QApplication.UnicodeUTF8))
        self.poDateValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter PO Date", None, QtGui.QApplication.UnicodeUTF8))
        self.vendorCodeLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Vendor Code", None, QtGui.QApplication.UnicodeUTF8))
        self.vendorCodeValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter Vendor Code", None, QtGui.QApplication.UnicodeUTF8))
        self.paymentTermslabel.setText(QtGui.QApplication.translate("SalesInvoice", "Payment Terms", None, QtGui.QApplication.UnicodeUTF8))
        self.paymentTermsValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter Payment Terms", None, QtGui.QApplication.UnicodeUTF8))
        self.dcNoLabel.setText(QtGui.QApplication.translate("SalesInvoice", "DC No", None, QtGui.QApplication.UnicodeUTF8))
        self.dcNoValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter DC No", None, QtGui.QApplication.UnicodeUTF8))
        self.daDateLabel.setText(QtGui.QApplication.translate("SalesInvoice", "DC Date", None, QtGui.QApplication.UnicodeUTF8))
        self.dcDateValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter DC Date", None, QtGui.QApplication.UnicodeUTF8))
        self.vehicleNoLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Vehicle No", None, QtGui.QApplication.UnicodeUTF8))
        self.vehicleNoValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter vehicle No", None, QtGui.QApplication.UnicodeUTF8))
        self.dispatchedlabel.setText(QtGui.QApplication.translate("SalesInvoice", "Dispatched Through", None, QtGui.QApplication.UnicodeUTF8))
        self.dispatchedValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter Dispatched Through", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("SalesInvoice", "Add Row", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("SalesInvoice", "Remove Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setText(QtGui.QApplication.translate("SalesInvoice", "Clear Table", None, QtGui.QApplication.UnicodeUTF8))
        self.importButton.setText(QtGui.QApplication.translate("SalesInvoice", "Import Table", None, QtGui.QApplication.UnicodeUTF8))
        self.beforeTaxLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Total Amount Before Tax", None, QtGui.QApplication.UnicodeUTF8))
        self.afterTaxLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Total Amount After Tax", None, QtGui.QApplication.UnicodeUTF8))
        self.amountPaidLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Amount Paid", None, QtGui.QApplication.UnicodeUTF8))
        self.amountPaidValue.setPlaceholderText(QtGui.QApplication.translate("SalesInvoice", "Enter Amount Paid", None, QtGui.QApplication.UnicodeUTF8))
        self.taxValueLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Tax Value", None, QtGui.QApplication.UnicodeUTF8))
        self.deliveryChallan.setText(QtGui.QApplication.translate("SalesInvoice", "Create Delivery Challan", None, QtGui.QApplication.UnicodeUTF8))
        self.remarksLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Remarks", None, QtGui.QApplication.UnicodeUTF8))
        self.amountWordLabel.setText(QtGui.QApplication.translate("SalesInvoice", "Total Amount in words", None, QtGui.QApplication.UnicodeUTF8))
        self.printCheckBox.setText(QtGui.QApplication.translate("SalesInvoice", "Print", None, QtGui.QApplication.UnicodeUTF8))
        self.previewButton.setText(QtGui.QApplication.translate("SalesInvoice", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("SalesInvoice", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.discardButton.setText(QtGui.QApplication.translate("SalesInvoice", "Discard", None, QtGui.QApplication.UnicodeUTF8))

from _widgets.header import Header
from _widgets.utils import TableWidget