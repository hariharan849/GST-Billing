#!/usr/bin/env python
# purchaseOrderReport.py

"""
PO report widget for displaying po information
"""

import collections as _collections
import datetime as _datetime
import pandas as _pd
import os as _os

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
        # self.__purchaseOrderReportUI.groupBox.toggled.connect(
        #     lambda: utils.toggleGroup(self.__purchaseOrderReportUI.groupBox))

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
            poInfoEntry.delete_instance()
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
            _QtCore.QRegExp(quotationNo, _QtCore.Qt.CaseInsensitive, _QtCore.QRegExp.FixedString),1)
        self.__purchaseOrderProxyModel.setFilterByColumn(
            _QtCore.QRegExp(customerName, _QtCore.Qt.CaseInsensitive, _QtCore.QRegExp.FixedString), 0)
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

    def viewItems(self, poNo):
        poDetails = self.poManager.getPOInfo(poNo)
        poProduct = self.poManager.getPurchaseOrderItemInfo(poNo)

        dialog = _QtGui.QDialog(self)
        itemInfoWidget = common.itemInfoWidget.ItemInfoWidget(poNo, poProduct, _constants._purchaseOrderSettings, poDetails.remarks, parent=self)
        layout = _QtGui.QHBoxLayout(dialog)
        layout.addWidget(itemInfoWidget)
        dialog.setWindowTitle('Purchase Order Item')
        dialog.exec_()

    def addItemInfo(self, itemInfo):
        return ItemDetails(itemInfo)

    def exportToExcel(self):
        df = self._getDataframe()
        exportPath = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(__file__))), 'Exports', 'PurchaseOrder')
        try:
            _os.makedirs(exportPath)
        except Exception as ex:
            pass
        now = _datetime.datetime.now()
        file_name = '{}_{}_{}-{}_{}_{}.xlsx'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        writer = _pd.ExcelWriter(
            _os.path.join(exportPath, file_name)
        )
        df.to_excel(writer, 'Sheet1', index=False, index_label=False)
        writer.save()
        _QtGui.QMessageBox.information(self, 'Saved', 'PurchaseOrder Information Exported Successfully.',
                                       buttons=_QtGui.QMessageBox.Ok)

    def _getDataframe(self):
        names, po_nos, po_dates, remarks = [], [], [], []
        for i in range(self.__purchaseOrderProxyModel.rowCount()):
            entry = self.poManager.getPOInfo(self.__purchaseOrderProxyModel.index(i, 1).data())
            if entry.cancelReason:
                continue
            names.append(entry.customerName)
            po_nos.append(entry.poNo)
            po_dates.append(entry.poDate)
            remarks.append(entry.remarks)
        purchase_values = _collections.OrderedDict()
        purchase_values['Customer Name'] = names
        purchase_values['PO No'] = po_nos
        purchase_values['PO Date'] = po_dates
        purchase_values['Remarks'] = remarks
        return _pd.DataFrame(purchase_values)

class ItemDetails(object):
    '''
    Wrapper class for adding quotation information
    '''
    def __init__(self, itemInfo):
        self.itemCode = _constants.valueWrapper(itemInfo.itemCode, False)
        self.particulars = _constants.valueWrapper(itemInfo.particular, False)
        self.hsnCode = _constants.valueWrapper(itemInfo.hsnCode, False)
        self.quantity = _constants.valueWrapper(itemInfo.quantity, False)
