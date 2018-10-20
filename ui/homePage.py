# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\homePage.ui'
#
# Created: Sat Aug 18 10:41:47 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_applicationHome(object):
    def setupUi(self, applicationHome):
        applicationHome.setObjectName("applicationHome")
        applicationHome.resize(400, 340)
        self.verticalLayout = QtGui.QVBoxLayout(applicationHome)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(applicationHome)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../logos/lokri.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(applicationHome)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.retranslateUi(applicationHome)
        QtCore.QMetaObject.connectSlotsByName(applicationHome)

    def retranslateUi(self, applicationHome):
        applicationHome.setWindowTitle(QtGui.QApplication.translate("applicationHome", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("applicationHome", "<html><head/><body><p><a href=\"http://www.lokri.in\"><span style=\" text-decoration: underline; color:#0000ff;\">www.lokri.in</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

