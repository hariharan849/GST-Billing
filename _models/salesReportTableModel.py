#!/usr/bin/env python
# salesReportTableModel.py

"""
Sales report Model for holding sales information
"""

import genericTableModel as _genericTableModel
import genericProxyTableModel as _genericProxyTableModel
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
import constants as _constants
import datetime as _datetime
from database import SalesInvoice

mutex = _QtCore.QMutex()

class SalesDetailsSaveWorker(_QtCore.QThread):

    def __init__(self, salesDetailsInfo, manager):
        super(SalesDetailsSaveWorker, self).__init__()
        self.__salesDetailsInfo = salesDetailsInfo
        self.__manager = manager

    def run(self):
        for salesDetailsInfo in self.__salesDetailsInfo:
            mutex.lock()
            salesData = self.__manager.getSalesInfo(salesDetailsInfo.billNo.value)
            salesData.customerName = salesDetailsInfo.customerName
            salesData.cusotmerAddress = salesDetailsInfo.customerAddress
            salesData.paidBy = salesDetailsInfo.paidBy
            salesData.invoiceDate = _datetime.datetime.strptime(salesDetailsInfo.invoiceDate.value, '%d - %b - %y')
            salesData.vendorCode = salesDetailsInfo.vendorCode
            salesData.paymentTerms = salesDetailsInfo.paymentTerms
            salesData.amount = salesDetailsInfo.amount
            salesData.total = salesDetailsInfo.total
            salesData.tax = salesDetailsInfo.tax
            salesData.amountPaid = salesDetailsInfo.amountPaid
            salesData.remarks = salesDetailsInfo.remarks
            salesData.save()
            mutex.unlock()

class SalesReportDetails(object):
    '''
    Wrapper class for adding sales information
    '''
    def __init__(self, customerName, customerAddress, customerGstin, customerStateCode, billNo, paidBy, invoiceDate,
                 poNo, poDate, dcCode, dcDate, vehicleNo, dispatchedThrough, vendorCode,
                 paymentTerms, amount, total, amountPaid, balance, paymentRemarks, status, cancel):
        self.customerName = _constants.valueWrapper(customerName, False)
        self.customerAddress = _constants.valueWrapper(customerAddress, False)
        self.customerGstin = _constants.valueWrapper(customerGstin, False)
        self.customerStateCode = _constants.valueWrapper(customerStateCode, False)
        self.billNo = _constants.valueWrapper(billNo, False)
        self.paidBy = _constants.valueWrapper(paidBy, False)
        self.invoiceDate = _constants.valueWrapper(invoiceDate, False)
        self.poNo = _constants.valueWrapper(poNo, False)
        self.poDate = _constants.valueWrapper(poDate, False)
        self.dcCode = _constants.valueWrapper(dcCode, False)
        self.dcDate = _constants.valueWrapper(dcDate, False)
        self.vehicleNo = _constants.valueWrapper(vehicleNo, False)
        self.dispatchedThrough = _constants.valueWrapper(dispatchedThrough, False)
        self.vendorCode = _constants.valueWrapper(vendorCode, False)
        self.paymentTerms = _constants.valueWrapper(paymentTerms, False)
        self.amount = _constants.valueWrapper(amount, False)
        self.tax = _constants.valueWrapper(float(total)-float(amount), False)
        self.total = _constants.valueWrapper(total, False)
        self.amountPaid = _constants.valueWrapper(amountPaid, False)
        self.balance = _constants.valueWrapper(balance, False)
        self.paymentRemarks = _constants.valueWrapper(paymentRemarks, False)
        self.status = _constants.valueWrapper(status, False)
        self.cancelReason = _constants.valueWrapper(cancel, False)


class SalesReportTableModel(_genericTableModel.GenericTableModel):
    '''
    Sales table model to display sales information
    '''
    def __init__(self, parent=None):
        super(SalesReportTableModel, self).__init__([], _constants._salesReportSettings, parent)

    def flags(self, index):
        '''
        Flags for editing/selecting a column
        '''
        if index.column() == 2:
            return _QtCore.Qt.ItemIsEnabled | _QtCore.Qt.ItemIsSelectable
        return super(SalesReportTableModel, self).flags(index)

    def addSalesReportInfo(self, customerName, customerAddress, customerGstin, customerStateCode, billNo, paidBy, invoiceDate,
                 poNo, poDate, dcCode, dcDate, vehicleNo, dispatchedThrough, vendorCode,
                 paymentTerms, amount, total, amountPaid, balance, paymentRemarks, status, cancel=''):
        '''
        Adds Sales information to the model
        '''
        salesInfo = SalesReportDetails(
            customerName, customerAddress, customerGstin, customerStateCode, billNo, paidBy, invoiceDate,
            poNo, poDate, dcCode, dcDate, vehicleNo, dispatchedThrough, vendorCode,
            paymentTerms, amount, total, amountPaid, balance, paymentRemarks, status, cancel
        )
        super(SalesReportTableModel, self).insertRows(self.rowCount(self), [salesInfo])

    def data(self, index, role):
        row = index.row()
        column = index.column()
        if role == _QtCore.Qt.BackgroundRole:
            if self._getData(row, column).flag:
                return _QtGui.QBrush(_QtCore.Qt.green)
            if self._getData(row, 14).value is not None:
                return _QtGui.QBrush(_QtCore.Qt.darkGray)
        return super(SalesReportTableModel, self).data(index, role)

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


class SalesReportProxyModel(_genericProxyTableModel.GenericProxyModel):
    '''
    SortFilterProxy model for sales information
    '''
    def __init__(self, *args, **kwargs):
        super(SalesReportProxyModel, self).__init__(*args, **kwargs)