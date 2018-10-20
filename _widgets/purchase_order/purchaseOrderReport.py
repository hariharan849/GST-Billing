#!/usr/bin/env python
# purchaseOrderReport.py

"""
PO report widget for displaying po information
"""

import collections as _collections
import datetime as _datetime

from database import PurchaseOrderManager
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
from ui.purchaseOrderReportUI import Ui_purchaseOrderReport
from models import PurchaseOrderReportTableModel, PurchaseOrderReportProxyModel, PurchaseOrderSaveWorker
from models import constants as _constants
from _widgets import utils, common

class PurchaseReportWidget(_QtGui.QWidget):
    '''
    UI for Purchase Report widget
    '''
    def __init__(self, parent=None):
        super(PurchaseReportWidget, self).__init__(parent)
        self.poManager = PurchaseOrderManager()
        self.__purchaseOrderReportUI = Ui_purchaseOrderReport()
        self.__setupWidget()
        self.__connectWidget()
        self.__setPurchaseOrderInformation()

    def __setupWidget(self):
        '''
        Sets all quotation req widgets
        '''
        self.__purchaseOrderReportUI.setupUi(self)

        self.__purchaseOrderModelData = PurchaseOrderReportTableModel()
        self.__purchaseOrderProxyModel = PurchaseOrderReportProxyModel()
        self.__purchaseOrderProxyModel.setSourceModel(self.__purchaseOrderModelData)
        self.__purchaseOrderProxyModel.setDynamicSortFilter(True)
        self.__purchaseOrderProxyModel.setFilterCaseSensitivity(_QtCore.Qt.CaseInsensitive)
        self.__purchaseOrderReportUI.purchaseOrderTable.setModel(self.__purchaseOrderProxyModel)

        self.__purchaseOrderReportUI.fromDateValue.setDate(_QtCore.QDate.currentDate())
        self.__purchaseOrderReportUI.toDateValue.setDate(_QtCore.QDate.currentDate())

        self.showMaximized()

    def __connectWidget(self):
        '''
        Connect all widget signal and slots
        '''
        self.__purchaseOrderReportUI.resetButton.clicked.connect(self.__discardChanges)
        self.__purchaseOrderReportUI.searchButton.clicked.connect(self.__searchChanges)
        self.__purchaseOrderReportUI.saveButton.clicked.connect(self.__saveTableChanges)
        self.__purchaseOrderReportUI.purchaseOrderTable.removeEntry.connect(self.__removeFromDatabase)
        self.__purchaseOrderReportUI.removeButton.clicked.connect(self.__purchaseOrderReportUI.purchaseOrderTable.removeSlot)
        self.__purchaseOrderReportUI.clearButton.clicked.connect(self.__purchaseOrderReportUI.purchaseOrderTable.clearSlot)

    def __setPurchaseOrderInformation(self):
        '''
        Sets all purchase order information from db
        '''
        purcheaseOrderData = self.poManager.fetchAllPOInfo()

        for info in purcheaseOrderData:
            self.__purchaseOrderModelData.addPurchaseOrderReportInfo(
                str(info.customerName),
                str(info.poNo),
                info.poDate.strftime('%d - %b - %Y'),
                str(info.remarks),
                info.cancelReason
            )

    @utils.showWaitCursor
    def __saveTableChanges(self):
        '''
        Save Table change to database
        '''
        worker = PurchaseOrderSaveWorker(self.__purchaseOrderModelData.tableData, self.poManager)
        worker.start()
        _QtGui.QMessageBox.information(self, 'Saved', 'PO Information Saved Successfully.',
                                       buttons=_QtGui.QMessageBox.Ok)

    def __removeFromDatabase(self, row='all'):
        '''
        Removes entry from database
        '''
        if row != 'all':
            poInfoEntry = self.poManager.getPOInfo(self.__purchaseOrderProxyModel.index(row, 1).data())
            poInfoEntry.delete()
            return
        self.poManager.deletePOInfo()

    def __validateSearchDate(self):
        '''
        Validates search from and to date
        '''
        if self.__purchaseOrderReportUI.fromDateValue.date() > self.__purchaseOrderReportUI.toDateValue.date():
            _QtGui.QMessageBox.critical(self, 'Error', 'From Date is Greater than To Date', buttons=_QtGui.QMessageBox.Ok)
            return False
        return True

    @utils.showWaitCursor
    def __searchChanges(self):
        '''
        Validates input and save changes in database and updates table.
        '''
        if not self.__validateSearchDate():
            return

        customerName = str(self.__purchaseOrderReportUI.customerSearchValue.text())
        quotationNo = str(self.__purchaseOrderReportUI.billSearchValue.text())
        fromDate = self.__purchaseOrderReportUI.fromDateValue.date()
        toDate = self.__purchaseOrderReportUI.toDateValue.date()

        self.__purchaseOrderProxyModel.setFilterByColumn(
            _QtCore.QRegExp(quotationNo, _QtCore.Qt.CaseSensitive, _QtCore.QRegExp.FixedString),1)
        self.__purchaseOrderProxyModel.setFilterByColumn(
            _QtCore.QRegExp(customerName, _QtCore.Qt.CaseSensitive, _QtCore.QRegExp.FixedString), 0)
        self.__purchaseOrderProxyModel.setFilterByColumn(
            _constants.dateFilter(fromDate.toString('dd - MMM - yyyy'), toDate.toString('dd - MMM - yyyy')), 2)

    @utils.showWaitCursor
    def __discardChanges(self):
        '''
        Discards all widgets to default values.
        '''
        self.__purchaseOrderReportUI.customerSearchValue.setText('')
        self.__purchaseOrderReportUI.billSearchValue.setText('')
        self.__purchaseOrderReportUI.fromDateValue.setDate(_QtCore.QDate.currentDate())
        self.__purchaseOrderReportUI.toDateValue.setDate(_QtCore.QDate.currentDate())
        self.__purchaseOrderReportUI.purchaseOrderTable.clearSlot()
        self.__setPurchaseOrderInformation()

    def cancelBill(self, poNo, cancelReason):
        poDetails = self.poManager.getPOInfo(poNo)
        # self.model
        poDetails.cancelReason = cancelReason
        poTableData = [data for data in self.__purchaseOrderModelData.tableData if data.poNo.value == poNo]
        poTableData[0].cancelReason = _constants.valueWrapper(cancelReason, False)
        poDetails.save()

    # def viewCancelReason(self, poNo):
    #     poDetails = self.poManager.getPOInfo(poNo)
    #     _QtGui.QMessageBox.warning(self, 'Reason for cancellation', poDetails.cancelReason, buttons=_QtGui.QMessageBox.Ok)

    def viewItems(self, poNo):
        poProduct = self.poManager.getPurchaseOrderItemInfo(poNo)

        itemInfoWidget = common.itemInfoWidget.ItemInfoWidget(poNo, poProduct, _constants._purchaseOrderSettings, parent=self)
        itemInfoWidget.show()
        itemInfoWidget.showMaximized()

    def addItemInfo(self, itemInfo):
        return ItemDetails(itemInfo)

class ItemDetails(object):
    '''
    Wrapper class for adding quotation information
    '''
    def __init__(self, itemInfo):
        self.itemCode = _constants.valueWrapper(itemInfo.itemCode, False)
        self.particulars = _constants.valueWrapper(itemInfo.particular, False)
        self.hsnCode = _constants.valueWrapper(itemInfo.hsnCode, False)
        self.quantity = _constants.valueWrapper(itemInfo.quantity, False)
