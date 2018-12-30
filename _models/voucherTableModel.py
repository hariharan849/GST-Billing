#!/usr/bin/env python
# voucherTableModel.py

"""
Voucher Model for holding voucher information
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

class VoucherSaveWorker(_QtCore.QThread):
    '''
    Worker for saving the information in database.
    '''
    def __init__(self, voucherInfo, voucherManager):
        super(VoucherSaveWorker, self).__init__()
        self.__voucherInfo = voucherInfo
        self.__voucherManager = voucherManager

    def run(self):
        for voucherInfo in self.__voucherInfo:
            mutex.lock()
            voucherData = self.__voucherManager.getVoucherInfo(voucherInfo.voucherNo.value)
            voucherData.customerName = voucherInfo.customerName.value
            voucherData.voucherDate = _datetime.datetime.strptime(voucherInfo.debitDate.value, '%d - %b - %Y')
            voucherData.remarks = voucherInfo.remarks.value
            voucherData.paymentType = voucherInfo.paymentType.value
            voucherData.chequeNo = voucherInfo.chequeNo.value
            voucherData.amount = voucherInfo.amount.value
            voucherData.cancelReason = voucherInfo.cancelReason.value
            voucherData.save()
            mutex.unlock()


class VoucherDetails(object):
    '''
    Wrapper class for adding voucher information
    '''
    def __init__(self, voucherNo, customerName, debitDate, remarks, paymentType, chequeNo, amount, cancelReason):
        self.voucherNo = _constants.valueWrapper(voucherNo, False)
        self.customerName = _constants.valueWrapper(customerName, False)
        self.debitDate = _constants.valueWrapper(debitDate, False)
        self.remarks = _constants.valueWrapper(remarks, False)
        self.paymentType = _constants.valueWrapper(paymentType, False)
        self.chequeNo = _constants.valueWrapper(chequeNo, False)
        self.amount = _constants.valueWrapper(amount, False)
        self.cancelReason = _constants.valueWrapper(cancelReason, False)


class VoucherTableModel(_genericTableModel.GenericTableModel):
    '''
    Vocuher table model to display voucher information
    '''
    def __init__(self, parent=None):
        super(VoucherTableModel, self).__init__([], _constants._voucherSettings, parent)

    def flags(self, index):
        '''
        Sets flag for the columns
        '''
        if index.column() == 0 or self._getData(index.row(), 7).value:
            return _QtCore.Qt.ItemIsEnabled | _QtCore.Qt.ItemIsSelectable
        return super(VoucherTableModel, self).flags(index)

    def addVoucherInfo(self, voucherNo, customerName, voucherDate, remarks, paymentType, checkNo, amount, cancelReason=""):
        '''
        Adds Voucher information to the model
        voucherNo: str
        customerName: str
        voucherDate: str
        remarks: str
        paymentType: str
        checkNo: str
        amount: str
        '''
        voucherInfo = VoucherDetails(
            voucherNo,
            customerName,
            voucherDate,
            remarks,
            paymentType,
            checkNo,
            amount,
            cancelReason
        )
        super(VoucherTableModel, self).insertRows(self.rowCount(self), [voucherInfo])

    def data(self, index, role):
        '''
        Sets data for the role
        '''
        row = index.row()
        column = index.column()
        if role == _QtCore.Qt.BackgroundRole:
            if self._getData(row, 7).value:
                return _QtGui.QBrush(_QtCore.Qt.lightGray)
            if self._getData(row, column).flag:
                return _QtGui.QBrush(_QtCore.Qt.green)
        return super(VoucherTableModel, self).data(index, role)

    def removeRow(self, position, parent=_QtCore.QModelIndex()):
        '''
        Removes voucher info from model
        '''
        self.parent().removeEntry.emit(position)
        self.removeRows(position, 1, parent)

    def clearTable(self):
        '''
        Clear model
        '''
        self.removeRows(0, self.rowCount(self))

class VoucherProxyModel(_genericProxyTableModel.GenericProxyModel):
    '''
    SortFilterProxy model for voucher information
    '''
    def __init__(self, *args, **kwargs):
        super(VoucherProxyModel, self).__init__(*args, **kwargs)
        self.settings = _constants._voucherSettings
