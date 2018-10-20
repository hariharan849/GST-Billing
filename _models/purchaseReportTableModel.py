#!/usr/bin/env python
# purchaseReportTableModel.py

"""
Purchase report Model for holding purchase information
"""

import genericTableModel as _genericTableModel
import genericProxyTableModel as _genericProxyTableModel
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
import constants as _constants
import datetime as _datetime
from database import PurchaseInvoice

mutex = _QtCore.QMutex()

class PurchaseSaveWorker(_QtCore.QThread):

    def __init__(self, purchaseOrderInfo, manager):
        super(PurchaseSaveWorker, self).__init__()
        self.__purchaseOrderInfo = purchaseOrderInfo
        self.__manager = manager

    def run(self):
        for purchaseInfo in self.__purchaseOrderInfo:
            mutex.lock()
            purchaseData = self.__manager.getPurchaseDetailsInfo(purchaseInfo.billNo.value)
            purchaseData.vendorName = purchaseInfo.customerName
            purchaseData.vendorAddress = purchaseInfo.customerAddress
            purchaseData.vendorGstin = purchaseInfo.customerGstin
            purchaseData.vendorStateCode = purchaseInfo.vendorStateCode
            purchaseData.billNo = purchaseInfo.billNo
            purchaseData.billDate = _datetime.datetime.strptime(purchaseInfo.billDate.value, '%d - %b - %y')
            purchaseData.dueDate = _datetime.datetime.strptime(purchaseInfo.dueDate.value, '%d - %b - %y')
            purchaseData.total = purchaseInfo.amount
            purchaseData.tax = purchaseInfo.total
            purchaseData.amountPaid = purchaseInfo.amountPaid
            purchaseData.remarks = purchaseInfo.remarks
            mutex.unlock()

class PuchaseReportDetails(object):
    '''
    Wrapper class for adding purchase information
    '''
    def __init__(self, vendorName, vendorAddress, vendorGstin, vendorStateCode, billNo, billDate, dueDate,
                              payBy, total, tax, amountPaid, remarks, status, cancel):
        self.vendorName = _constants.valueWrapper(vendorName, False)
        self.vendorAddress = _constants.valueWrapper(vendorAddress, False)
        self.vendorGstin = _constants.valueWrapper(vendorGstin, False)
        self.vendorStateCode = _constants.valueWrapper(vendorStateCode, False)
        self.billNo = _constants.valueWrapper(billNo, False)
        self.billDate = _constants.valueWrapper(billDate, False)
        self.dueDate = _constants.valueWrapper(dueDate, False)
        self.total = _constants.valueWrapper(total, False)
        self.paidBy = _constants.valueWrapper(payBy, False)
        self.tax = _constants.valueWrapper(tax, False)
        self.amount = _constants.valueWrapper(float(total) - float(tax), False)
        self.amountPaid = _constants.valueWrapper(amountPaid, False)
        self.balance = _constants.valueWrapper(float(total) - float(amountPaid), False)
        self.remarks = _constants.valueWrapper(remarks, False)
        self.status = _constants.valueWrapper(status, False)
        self.cancelReason = _constants.valueWrapper(cancel, False)

class PurchaseReportTableModel(_genericTableModel.GenericTableModel):
    '''
    Purchase table model to display purchase information
    '''
    def __init__(self, parent=None):
        super(PurchaseReportTableModel, self).__init__([], _constants._purchaseReportSettings, parent)

    def flags(self, index):
        '''
        Flags for editing/selecting a column
        '''
        if index.column() == 4:
            return _QtCore.Qt.ItemIsEnabled | _QtCore.Qt.ItemIsSelectable
        return super(PurchaseReportTableModel, self).flags(index)

    def addPurchaseReportInfo(self, vendorName, vendorAddress, vendorGstin, vendorStateCode, billNo, billDate, dueDate,
                              payBy, total, tax, amountPaid, remarks, status, cancel=''):
        '''
        Adds Purchase information to the model
        '''
        purchaseInfo = PuchaseReportDetails(
            vendorName, vendorAddress, vendorGstin, vendorStateCode, billNo, billDate, dueDate,
            payBy, total, tax, amountPaid, remarks, status, cancel
        )
        super(PurchaseReportTableModel, self).insertRows(self.rowCount(self), [purchaseInfo])

    def data(self, index, role):
        row = index.row()
        column = index.column()
        if role == _QtCore.Qt.BackgroundRole:
            if self._getData(row, column).flag:
                return _QtGui.QBrush(_QtCore.Qt.green)
            if self._getData(row, 15).value is not None:
                return _QtGui.QBrush(_QtCore.Qt.darkGray)
        return super(PurchaseReportTableModel, self).data(index, role)

    def removeRow(self, position, parent=_QtCore.QModelIndex()):
        '''
        Removes voucher info from model
        '''
        self.removeRows(position, 1, parent)

    def clearTable(self):
        '''
        Clear model
        '''
        self.removeRows(0, self.rowCount(self))


class PurchaseReportProxyModel(_genericProxyTableModel.GenericProxyModel):
    '''
    SortFilterProxy model for purchase information
    '''
    def __init__(self, *args, **kwargs):
        super(PurchaseReportProxyModel, self).__init__(*args, **kwargs)