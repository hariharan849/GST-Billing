# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chartUI.ui'
#
# Created: Tue Sep 25 07:37:24 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_chart(object):
    def setupUi(self, chart):
        chart.setObjectName("chart")
        chart.resize(1716, 734)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(chart.sizePolicy().hasHeightForWidth())
        chart.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QtGui.QGridLayout(chart)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.widget = Header(chart)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(chart)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle("")
        self.groupBox.setCheckable(True)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.fromDateLabel = QtGui.QLabel(self.groupBox)
        self.fromDateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fromDateLabel.setObjectName("fromDateLabel")
        self.gridLayout_2.addWidget(self.fromDateLabel, 0, 0, 1, 1)
        self.toDateLabel = QtGui.QLabel(self.groupBox)
        self.toDateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.toDateLabel.setObjectName("toDateLabel")
        self.gridLayout_2.addWidget(self.toDateLabel, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(400, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 4, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.barRadioButton = QtGui.QRadioButton(self.groupBox)
        self.barRadioButton.setObjectName("barRadioButton")
        self.horizontalLayout_2.addWidget(self.barRadioButton)
        self.lineRadioButton = QtGui.QRadioButton(self.groupBox)
        self.lineRadioButton.setObjectName("lineRadioButton")
        self.horizontalLayout_2.addWidget(self.lineRadioButton)
        self.scatterRadioButton = QtGui.QRadioButton(self.groupBox)
        self.scatterRadioButton.setObjectName("scatterRadioButton")
        self.horizontalLayout_2.addWidget(self.scatterRadioButton)
        spacerItem1 = QtGui.QSpacerItem(500, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 5)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.searchButton = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMinimumSize(QtCore.QSize(300, 35))
        self.searchButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_3.addWidget(self.searchButton)
        self.resetButton = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resetButton.sizePolicy().hasHeightForWidth())
        self.resetButton.setSizePolicy(sizePolicy)
        self.resetButton.setMinimumSize(QtCore.QSize(300, 35))
        self.resetButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout_3.addWidget(self.resetButton)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 0, 1, 5)
        self.fromDateValue = QtGui.QDateTimeEdit(self.groupBox)
        self.fromDateValue.setCalendarPopup(True)
        self.fromDateValue.setObjectName("fromDateValue")
        self.gridLayout_2.addWidget(self.fromDateValue, 0, 1, 1, 1)
        self.toDateValue = QtGui.QDateTimeEdit(self.groupBox)
        self.toDateValue.setCalendarPopup(True)
        self.toDateValue.setObjectName("toDateValue")
        self.gridLayout_2.addWidget(self.toDateValue, 0, 3, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 1, 0, 1, 1)
        self.matplotLibWidget = QtGui.QWidget(chart)
        self.matplotLibWidget.setObjectName("matplotLibWidget")
        self.gridLayout_3.addWidget(self.matplotLibWidget, 2, 0, 1, 1)

        self.retranslateUi(chart)
        QtCore.QMetaObject.connectSlotsByName(chart)

    def retranslateUi(self, chart):
        chart.setWindowTitle(QtGui.QApplication.translate("chart", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.fromDateLabel.setText(QtGui.QApplication.translate("chart", "From Date", None, QtGui.QApplication.UnicodeUTF8))
        self.toDateLabel.setText(QtGui.QApplication.translate("chart", "To Date", None, QtGui.QApplication.UnicodeUTF8))
        self.barRadioButton.setText(QtGui.QApplication.translate("chart", "Bar Chart", None, QtGui.QApplication.UnicodeUTF8))
        self.lineRadioButton.setText(QtGui.QApplication.translate("chart", "Line Chart", None, QtGui.QApplication.UnicodeUTF8))
        self.scatterRadioButton.setText(QtGui.QApplication.translate("chart", "Scatter Chart", None, QtGui.QApplication.UnicodeUTF8))
        self.searchButton.setText(QtGui.QApplication.translate("chart", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.resetButton.setText(QtGui.QApplication.translate("chart", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.fromDateValue.setDisplayFormat(QtGui.QApplication.translate("chart", "dd-MMM-yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.toDateValue.setDisplayFormat(QtGui.QApplication.translate("chart", "dd-MMM-yyyy", None, QtGui.QApplication.UnicodeUTF8))

from _widgets.header import Header
