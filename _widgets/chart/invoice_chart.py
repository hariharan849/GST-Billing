# -*- coding: utf-8 -*-
'''
User Interface for viewing sales reports.
'''

from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
from ui.chartUI import Ui_chart
from database import PurchaseManager, SalesManager


class ChartWidget(_QtGui.QWidget):
    '''
    Creates Invoice Report UI with search and table.
    '''
    def __init__(self):
        super(ChartWidget, self).__init__()
        self.__chartType = 'bo'
        self.__searchPressed = False
        self._chartUI = Ui_chart()

        self.__setupWidgets()
        self.__connectWidget()

    def __setupWidgets(self):
        '''
        Sets widget with canvas and toolbar
        '''
        self._chartUI.setupUi(self)

        self.__figure = plt.figure()
        self.__canvas = FigureCanvas(self.__figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.__toolbar = NavigationToolbar(self.__canvas, self)

        layout = _QtGui.QVBoxLayout(self._chartUI.matplotLibWidget)
        layout.addWidget(self.__toolbar)
        layout.addWidget(self.__canvas)

        self._chartUI.fromDateValue.setDate(_QtCore.QDate.currentDate())
        self._chartUI.toDateValue.setDate(_QtCore.QDate.currentDate())

    def __connectWidget(self):
        '''
        Connect all widget signal and slots
        '''
        self._chartUI.barRadioButton.setChecked(True)
        self._chartUI.barRadioButton.toggled.connect(lambda: self.__setChartType('bo'))
        self._chartUI.lineRadioButton.toggled.connect(lambda: self.__setChartType('k'))
        self._chartUI.scatterRadioButton.toggled.connect(lambda: self.__setChartType('o'))

        self._chartUI.searchButton.clicked.connect(self.__searchData)
        self._chartUI.resetButton.clicked.connect(self.__resetDates)

    def __searchData(self):
        '''
        Sets flag when search is pressed
        '''
        self.__searchPressed = True
        self._createChart()

    def __setChartType(self, type):
        '''
        Sets chart type when toggled on bar, line and scatter
        '''
        self.__chartType = type
        self._createChart()

    def updateAnnotBar(self, bar):
        x = bar.get_x() + bar.get_width() / 2.
        y = bar.get_y() + bar.get_height()
        self.annot.xy = (x, y)
        text = "{}".format(float(y))
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)

    def update_annot(self, ind):

        pos = self.chartItem.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        text = "{}".format(float(pos[-1]))
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)

    def hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            if self.__chartType == 'bo':
                for bar in self.chartItem:
                    cont, ind = bar.contains(event)
                    if cont:
                        self.updateAnnotBar(bar)
                        # bar.set_color('red')
                        self.annot.set_visible(True)
                        self.__figure.canvas.draw_idle()
                        return
            else:
                vis = self.annot.get_visible()
                if event.inaxes == self.ax:
                    cont, ind = self.chartItem.contains(event)
                    if cont:
                        self.update_annot(ind)
                        self.annot.set_visible(True)
                        self.__figure.canvas.draw_idle()
                    else:
                        if vis:
                            self.annot.set_visible(False)
                            self.__figure.canvas.draw_idle()

        if vis:
            self.annot.set_visible(False)
            self.__figure.canvas.draw_idle()

    def _createChart(self):
        '''
        Creates chart in the widget
        '''
        if not self.__searchPressed:
            return
        self.__figure.clear()

        # create an axis
        self.ax = self.__figure.add_subplot(111)

        customerDetails = self.fetchDataWithinDate()
        self.__figure.clear()

        # create an axis
        self.ax = self.__figure.add_subplot(111)
        self.annot = self.ax.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)

        x_values, y_values = [], []
        if not customerDetails:
            return
        for (cust, val) in sorted(customerDetails.iteritems()):
            x_values.append(cust)
            y_values.append(val)
            self.ax.text(cust, val + .5, str(val), color='blue', fontweight='bold')
        if self.__chartType == 'bo':
            self.chartItem = self.ax.bar(x_values, y_values)
            self.__figure.canvas.mpl_connect("motion_notify_event", self.hover)
        elif self.__chartType == 'o':
            norm = plt.Normalize(1, 4)
            cmap = plt.cm.RdYlGn
            self.chartItem = plt.scatter(x_values, y_values, s=100, cmap=cmap, norm=norm)
        else:
            self.chartItem = self.ax.plot(x_values, y_values, self.__chartType)
        # refresh canvas
        self.__canvas.draw()
        # markerline, stemlines, baseline = self.ax.stem(x_values, y_values, '-.')
        # plt.setp(markerline, 'markerfacecolor', 'b')
        # plt.setp(baseline, 'color', 'r', 'linewidth', 2)
        # cursor = FollowDotCursor(self.ax, y_values, tolerance=20)

    def fetchDataWithinDate(self):
        '''
        Searched invoice between from and to date
        '''
        raise NotImplementedError()


    def __resetDates(self):
        '''
        Resets dates to today
        '''
        self._chartUI.fromDateValue.setDate(_QtCore.QDate.currentDate())
        self._chartUI.toDateValue.setDate(_QtCore.QDate.currentDate())


class InvoiceChart(ChartWidget):
    def __init__(self, dbtype):
        super(InvoiceChart, self).__init__()
        if dbtype == 'sales':
            self.__manager = SalesManager(dbtype)
        else:
            self.__manager = PurchaseManager()
        self.__objXData = 'customerName'
        self.__objYData = 'amountPaid'

    def contextMenuEvent(self, ev):
        '''
        Context menu for adding row.
        '''
        customerMenu = _QtGui.QMenu(self)
        xAxisMenu = _QtGui.QMenu('&Set X Axis')
        customerAction = _QtGui.QAction('Set Customer', self)
        customerAction.triggered.connect(lambda :self.__setXObjectData('customerName'))
        dateAction = _QtGui.QAction('Set Date', self)
        dateAction.triggered.connect(lambda :self.__setXObjectData('billDate'))

        xAxisMenu.addAction(customerAction)
        xAxisMenu.addAction(dateAction)

        yAxisMenu = _QtGui.QMenu('&Set Y Axis')
        amountAction = _QtGui.QAction('Set Total Amount', self)
        amountAction.triggered.connect(lambda :self.__setYObjectData('total'))
        amountPaidAction = _QtGui.QAction('Set Amount Paid', self)
        amountPaidAction.triggered.connect(lambda :self.__setYObjectData('amountPaid'))

        yAxisMenu.addAction(amountAction)
        yAxisMenu.addAction(amountPaidAction)

        customerMenu.addMenu(xAxisMenu)
        customerMenu.addMenu(yAxisMenu)

        pos = self.mapToGlobal(ev.pos())
        customerMenu.exec_(pos)

    def __setXObjectData(self, data):
        self.__objXData = data
        self._createChart()

    def __setYObjectData(self, data):
        self.__objYData = data
        self._createChart()

    def fetchDataWithinDate(self):
        '''
        Searched invoice between from and to date
        '''
        dataEntry = self.__manager.fetchInfoWithinDate(
            self._chartUI.fromDateValue.date().toPython(),
            self._chartUI.toDateValue.date().toPython()
        )
        customerDetails = defaultdict(float)
        for entry in dataEntry:
            if self.__objXData == 'customerName':
                customerDetails[getattr(entry, self.__objXData, 'vendorName')] += float(
                    getattr(entry, self.__objYData))
            else:
                customerDetails[getattr(entry, self.__objXData).strftime('%d-%m-%Y')] += float(getattr(entry, self.__objYData))
        return customerDetails


class ParticularsChart(ChartWidget):
    def __init__(self, dbtype):
        super(ParticularsChart, self).__init__()
        if dbtype == 'sales':
            self.__manager = SalesManager(dbtype)
        else:
            self.__manager = PurchaseManager()

    def fetchDataWithinDate(self):
        '''
        Searched invoice between from and to date
        '''
        dataEntry = self.__manager.fetchInfoWithinDate(
            self._chartUI.fromDateValue.date().toPython(),
            self._chartUI.toDateValue.date().toPython()
        )

        particularDetails = defaultdict(float)
        for entry in dataEntry:
            particularInfo = self.__manager.getItemInfo(entry.billNo)
            particularDetails[particularInfo.particular] += 1

        return particularDetails


def fmt(y):
    return 'y: {y:0.2f}'.format(y=y)

