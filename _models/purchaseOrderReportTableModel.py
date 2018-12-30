#!/usr/bin/env python
# purchaseOrderReportTableModel.py

"""
Purchase Order report information for tableview in pyside
"""

import datetime as _datetime
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
import constants as _constants
import genericProxyTableModel as _genericProxyTableModel
import genericTableModel as _genericTableModel


mutex = _QtCore.QMutex()

class PurchaseOrderSaveWorker(_QtCore.QThread):

    def __init__(self, purchaseOrderInfo, manager):
        super(PurchaseOrderSaveWorker, self).__init__()
        self.__purchaseOrderInfo = purchaseOrderInfo
        self.__manager = manager

    def run(self):
        for purchaseOrderInfo in self.__purchaseOrderInfo:
            mutex.lock()
            purchaseOrderData = self.__manager.getPOInfo(purchaseOrderInfo.poNo.value)
            purchaseOrderData.customerName = purchaseOrderInfo.customerName.value
            purchaseOrderData.poDate = _datetime.datetime.strptime(purchaseOrderInfo.poDate.value, '%d - %b - %Y')
            purchaseOrderData.remarks = purchaseOrderInfo.remarks.value
            purchaseOrderData.save()
            mutex.unlock()

class PurchaseOrderReportDetails(object):
    '''
    Wrapper class for adding Purchase order information
    '''
    __slots__ = ['customerName', 'poDate', 'poNo', 'remarks', 'cancelReason']
    def __init__(self, customerName, poNo, poDate, remarks, cancel):
        self.customerName = _constants.valueWrapper(customerName, False)
        self.poDate = _constants.valueWrapper(poDate, False)
        self.poNo = _constants.valueWrapper(poNo, False)
        self.remarks = _constants.valueWrapper(remarks, False)
        self.cancelReason = _constants.valueWrapper(cancel, False)


class PurchaseOrderReportTableModel(_genericTableModel.GenericTableModel):
    '''
    Purchase order table model to display po information
    '''
    def __init__(self, parent=None):
        super(PurchaseOrderReportTableModel, self).__init__([], _constants._purchaseOrderReportSettings, parent)

    def flags(self, index):
        '''
        Flags for editing/selecting a column
        '''
        if index.column() == 1 or self.index(index.row(), 4).data().strip():
            return _QtCore.Qt.ItemIsEnabled | _QtCore.Qt.ItemIsSelectable
        return super(PurchaseOrderReportTableModel, self).flags(index)

    def addPurchaseOrderReportInfo(self, customerName, poNo, poDate, remarks, cancel=''):
        '''
        Adds Voucher information to the model
        '''
        purchaseOrderInfo = PurchaseOrderReportDetails(
            customerName,
            poNo,
            poDate,
            remarks,
            cancel
        )
        super(PurchaseOrderReportTableModel, self).insertRows(self.rowCount(self), [purchaseOrderInfo])

    def data(self, index, role):
        '''
        Data method for displaying background color
        '''
        row = index.row()
        column = index.column()
        if role == _QtCore.Qt.BackgroundRole:
            if self._getData(row, column).flag:
                return _QtGui.QBrush(_QtCore.Qt.green)
            if self._getData(row, 4).value:
                return _QtGui.QBrush(_QtCore.Qt.darkGray)
        return super(PurchaseOrderReportTableModel, self).data(index, role)

    def removeRow(self, position, parent=_QtCore.QModelIndex()):
        '''
        Removes purchase info from model
        '''
        self.removeRows(position, 1, parent)

    def clearTable(self):
        '''
        Clear model
        '''
        self.removeRows(0, self.rowCount(self))


class PurchaseOrderReportProxyModel(_genericProxyTableModel.GenericProxyModel):
    '''
    SortFilterProxy model for purchase order information
    '''
    def __init__(self, *args, **kwargs):
        super(PurchaseOrderReportProxyModel, self).__init__(*args, **kwargs)
