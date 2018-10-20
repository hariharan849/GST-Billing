# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'customerDialogUI.ui'
#
# Created: Sun Aug 19 18:07:46 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.nameLabel = QtGui.QLabel(Dialog)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.nameValue = QtGui.QLineEdit(Dialog)
        self.nameValue.setObjectName("nameValue")
        self.gridLayout.addWidget(self.nameValue, 0, 1, 1, 1)
        self.addressLabel = QtGui.QLabel(Dialog)
        self.addressLabel.setObjectName("addressLabel")
        self.gridLayout.addWidget(self.addressLabel, 1, 0, 1, 1)
        self.gstinLabel = QtGui.QLabel(Dialog)
        self.gstinLabel.setObjectName("gstinLabel")
        self.gridLayout.addWidget(self.gstinLabel, 2, 0, 1, 1)
        self.gstinValue = QtGui.QLineEdit(Dialog)
        self.gstinValue.setObjectName("gstinValue")
        self.gridLayout.addWidget(self.gstinValue, 2, 1, 1, 1)
        self.stateCodeLabel = QtGui.QLabel(Dialog)
        self.stateCodeLabel.setObjectName("stateCodeLabel")
        self.gridLayout.addWidget(self.stateCodeLabel, 3, 0, 1, 1)
        self.stateValue = QtGui.QLineEdit(Dialog)
        self.stateValue.setObjectName("stateValue")
        self.gridLayout.addWidget(self.stateValue, 3, 1, 1, 1)
        self.contactLabel = QtGui.QLabel(Dialog)
        self.contactLabel.setObjectName("contactLabel")
        self.gridLayout.addWidget(self.contactLabel, 4, 0, 1, 1)
        self.contactNoValue = QtGui.QLineEdit(Dialog)
        self.contactNoValue.setObjectName("contactNoValue")
        self.gridLayout.addWidget(self.contactNoValue, 4, 1, 1, 1)
        self.saveButton = QtGui.QDialogButtonBox(Dialog)
        self.saveButton.setOrientation(QtCore.Qt.Horizontal)
        self.saveButton.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 5, 0, 1, 2)
        self.addressValue = QtGui.QLineEdit(Dialog)
        self.addressValue.setObjectName("addressValue")
        self.gridLayout.addWidget(self.addressValue, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.saveButton, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("Dialog", "Customer Name", None, QtGui.QApplication.UnicodeUTF8))
        self.addressLabel.setText(QtGui.QApplication.translate("Dialog", "Customer Address", None, QtGui.QApplication.UnicodeUTF8))
        self.gstinLabel.setText(QtGui.QApplication.translate("Dialog", "Customer GSTIN", None, QtGui.QApplication.UnicodeUTF8))
        self.gstinValue.setPlaceholderText(QtGui.QApplication.translate("Dialog", "Enter Customer GSTIN", None, QtGui.QApplication.UnicodeUTF8))
        self.stateCodeLabel.setText(QtGui.QApplication.translate("Dialog", "State Code", None, QtGui.QApplication.UnicodeUTF8))
        self.stateValue.setPlaceholderText(QtGui.QApplication.translate("Dialog", "Enter Customer StateCode", None, QtGui.QApplication.UnicodeUTF8))
        self.contactLabel.setText(QtGui.QApplication.translate("Dialog", "Contact No", None, QtGui.QApplication.UnicodeUTF8))
        self.contactNoValue.setPlaceholderText(QtGui.QApplication.translate("Dialog", "Enter Customer ContactNo", None, QtGui.QApplication.UnicodeUTF8))

