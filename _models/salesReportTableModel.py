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
            salesData.customerName = salesDetailsInfo.customerName.value
            salesData.cusotmerAddress = salesDetailsInfo.customerAddress.value
            salesData.paidBy = salesDetailsInfo.paidBy.value
            salesData.invoiceDate = _datetime.datetime.strptime(salesDetailsInfo.invoiceDate.value, '%Y-%m-%d')
            salesData.vendorCode = salesDetailsInfo.vendorCode.value
            salesData.paymentTerms = salesDetailsInfo.paymentTerms.value
            salesData.amount = float(salesDetailsInfo.amount.value)
            salesData.total = float(salesDetailsInfo.total.value)
            salesData.tax = float(salesDetailsInfo.tax.value)
            salesData.amountPaid = float(salesDetailsInfo.amountPaid.value)
            salesData.remarks = salesDetailsInfo.paymentRemarks.value
            salesData.cancelReason = salesDetailsInfo.cancelReason.value
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
        if index.column() in [2, 8]:
            return _QtCore.Qt.ItemIsEnabled | _QtCore.Qt.ItemIsSelectable
        if self.index(index.row(), 14).data() and self.index(index.row(), 14).data().strip():
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
            if self._getData(row, 13) == 'Paid':
                return _QtGui.QBrush(_QtCore.Qt.green)
            if self._getData(row, 14).value:
                return _QtGui.QBrush(_QtCore.Qt.darkYellow)
        # if role == _QtCore.Qt.DisplayRole:
        #     if column == 13 and round(float(self._getData(row, 9).value)) == round(float(self._getData(row, 10).value)):
        #         return 'True'

        return super(SalesReportTableModel, self).data(index, role)


    def setData(self, index, value, role=_QtCore.Qt.EditRole):
        '''
        Sets data for the specified cell upon edit
        '''
        if index.column() not in [7, 8, 9, 10, 11]:
            return super(SalesReportTableModel, self).setData(index, value, role)
        if role == _QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            if index.data() == value:
                return False
            setattr(self.tableData[row], self.settings[column][_constants._columnId],
                    _constants.valueWrapper(value, True))
            amount = float(getattr(self.tableData[row], self.settings[7][_constants._columnId]).value)
            tax = float(getattr(self.tableData[row], self.settings[8][_constants._columnId]).value)
            total = float(getattr(self.tableData[row], self.settings[9][_constants._columnId]).value)
            amountPaid = float(getattr(self.tableData[row], self.settings[10][_constants._columnId]).value)
            balance = float(getattr(self.tableData[row], self.settings[11][_constants._columnId]).value)
            # print column, amount+tax
            value = float(value)
            if column in [7, 8]:
                setattr(self.tableData[row], self.settings[9][_constants._columnId],
                        _constants.valueWrapper(amount+tax, True))
            elif column == 9:
                setattr(self.tableData[row], self.settings[7][_constants._columnId],
                        _constants.valueWrapper(total - tax, True))
            elif column == 10:
                # print total, value
                if value > total:
                    _QtGui.QMessageBox.critical(None, 'Error',
                                                'Amount Paid is greater than Total',
                                                buttons=_QtGui.QMessageBox.Ok)
                    return True
                setattr(self.tableData[row], self.settings[11][_constants._columnId],
                        _constants.valueWrapper(total-value, True))
            elif column == 11:
                if value > total:
                    _QtGui.QMessageBox.critical(None, 'Error',
                                                'Balance is greater than Total',
                                                buttons=_QtGui.QMessageBox.Ok)
                    return True
                setattr(self.tableData[row], self.settings[10][_constants._columnId],
                        _constants.valueWrapper(total-value, True))
            status = 'Paid' if round(float(total)) == round(float(amountPaid)) else 'Not Paid'
            setattr(self.tableData[row], self.settings[13][_constants._columnId],
                    _constants.valueWrapper(status, True))
            return True
        return False

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