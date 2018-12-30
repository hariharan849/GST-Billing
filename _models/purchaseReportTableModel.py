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
            purchaseData.vendorName = purchaseInfo.vendorName.value
            purchaseData.vendorAddress = purchaseInfo.vendorAddress.value
            purchaseData.vendorGstin = purchaseInfo.vendorGstin.value
            purchaseData.vendorStateCode = purchaseInfo.vendorStateCode.value
            purchaseData.billNo = purchaseInfo.billNo.value
            purchaseData.billDate = _datetime.datetime.strptime(purchaseInfo.billDate.value, '%Y-%m-%d')
            purchaseData.dueDate = _datetime.datetime.strptime(purchaseInfo.dueDate.value, '%Y-%m-%d')

            # print purchaseInfo.total.value, purchaseInfo.total.value-purchaseInfo.amount.value, purchaseInfo.amountPaid.value
            purchaseData.total = float(purchaseInfo.amount.value)
            purchaseData.tax = float(purchaseInfo.tax.value)
            purchaseData.amountPaid = float(purchaseInfo.amountPaid.value)
            purchaseData.remarks = purchaseInfo.remarks.value
            purchaseData.save()
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
        if self.index(index.row(), 15).data() and self.index(index.row(), 15).data().strip():
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
            if self._getData(row, 14) == 'Paid':
                return _QtGui.QBrush(_QtCore.Qt.green)
            if self._getData(row, 15).value:
                return _QtGui.QBrush(_QtCore.Qt.darkYellow)
        return super(PurchaseReportTableModel, self).data(index, role)

    def setData(self, index, value, role=_QtCore.Qt.EditRole):
        '''
        Sets data for the specified cell upon edit
        '''
        if index.column() not in [8, 9, 10, 11, 12]:
            return super(PurchaseReportTableModel, self).setData(index, value, role)
        if role == _QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            if index.data() == value:
                return False
            setattr(self.tableData[row], self.settings[column][_constants._columnId],
                    _constants.valueWrapper(value, True))
            amount = float(getattr(self.tableData[row], self.settings[8][_constants._columnId]).value)
            tax = float(getattr(self.tableData[row], self.settings[9][_constants._columnId]).value)
            total = float(getattr(self.tableData[row], self.settings[10][_constants._columnId]).value)
            amountPaid = float(getattr(self.tableData[row], self.settings[11][_constants._columnId]).value)
            balance = float(getattr(self.tableData[row], self.settings[12][_constants._columnId]).value)
            # print column, amount+tax
            value = float(value)
            if column in [8, 9]:
                setattr(self.tableData[row], self.settings[10][_constants._columnId],
                        _constants.valueWrapper(amount+tax, True))
            elif column == 10:
                setattr(self.tableData[row], self.settings[8][_constants._columnId],
                        _constants.valueWrapper(total - tax, True))
            elif column == 11:
                if value > total:
                    _QtGui.QMessageBox.critical(None, 'Error',
                                                'Amount Paid is greater than Total',
                                                buttons=_QtGui.QMessageBox.Ok)
                    return True
                setattr(self.tableData[row], self.settings[12][_constants._columnId],
                        _constants.valueWrapper(total-value, True))
            elif column == 12:
                if value > total:
                    _QtGui.QMessageBox.critical(None, 'Error',
                                                'Balance is greater than Total',
                                                buttons=_QtGui.QMessageBox.Ok)
                    return True
                setattr(self.tableData[row], self.settings[11][_constants._columnId],
                        _constants.valueWrapper(total-value, True))
            status = 'Paid' if round(float(total)) == round(float(amountPaid)) else 'Not Paid'
            setattr(self.tableData[row], self.settings[14][_constants._columnId],
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


class PurchaseReportProxyModel(_genericProxyTableModel.GenericProxyModel):
    '''
    SortFilterProxy model for purchase information
    '''
    def __init__(self, *args, **kwargs):
        super(PurchaseReportProxyModel, self).__init__(*args, **kwargs)
        self.settings = _constants._purchaseReportSettings
