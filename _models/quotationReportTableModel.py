#!/usr/bin/env python
# quotationReportTableModel.py

"""
QuotationReport information for tableview in pyside
"""

import datetime as _datetime
import re as _re
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
import constants as _constants
import genericProxyTableModel as _genericProxyTableModel
import genericTableModel as _genericTableModel

mutex = _QtCore.QMutex()

class QuotationDetailsSaveWorker(_QtCore.QThread):

    def __init__(self, QuotationDetailsInfo, manager):
        super(QuotationDetailsSaveWorker, self).__init__()
        self.__quotationDetailsInfo = QuotationDetailsInfo
        self.__manager = manager

    def run(self):
        for quotationInfo in self.__quotationDetailsInfo:
            mutex.lock()
            # for voucherInfo in self.__voucherModelData.tableData:
                # if voucherInfo.paymentType.value == 'Cheque' and voucherInfo.chequeNo.value == 'NA':
                #     return _QtGui.QMessageBox.information(
                #         self, 'Not saved', 'Voucher No {0} has payment type Cheque but has no Cheque No.'.format(
                #             voucherInfo.voucherNo.value),
                #         buttons=_QtGui.QMessageBox.Ok)
            quotationData = self.__manager.getQuotationDetailsInfo(quotationInfo.quotationNo.value)
            quotationData.customerName = quotationInfo.customerName.value
            quotationData.customerAddress = quotationInfo.customerAddress.value
            quotationData.quotationDate = _datetime.datetime.strptime(quotationInfo.quotationDate.value, '%d - %b - %Y')
            quotationData.quotationValidity = _datetime.datetime.strptime(quotationInfo.validUntilDate.value,
                                                                          '%d - %b - %Y')
            quotationData.estAmount = quotationInfo.amount.value
            quotationData.estTotal = quotationInfo.total.value
            quotationData.cancelReason = quotationInfo.cancelReason.value
            quotationData.save()
            mutex.unlock()

class QuotationReportDetails(object):
    '''
    Wrapper class for adding quotation information
    '''
    def __init__(self, customerName, customerAddress, quotationNo, quotationDate, validUntilDate, amount, tax, total, cancel):
        self.customerName = _constants.valueWrapper(customerName, False)
        self.customerAddress = _constants.valueWrapper(customerAddress, False)
        self.quotationNo = _constants.valueWrapper(quotationNo, False)
        self.quotationDate = _constants.valueWrapper(quotationDate, False)
        self.validUntilDate = _constants.valueWrapper(validUntilDate, False)
        self.amount = _constants.valueWrapper(amount, False)
        self.tax = _constants.valueWrapper(tax, False)
        self.total = _constants.valueWrapper(total, False)
        self.cancelReason = _constants.valueWrapper(cancel, False)


class QuotationReportTableModel(_genericTableModel.GenericTableModel):
    '''
    Quotation table model to display quotation Report information
    '''
    def __init__(self, parent=None):
        super(QuotationReportTableModel, self).__init__([], _constants._quotationReportSettings, parent)

    def flags(self, index):
        '''
        Flags for editing/selecting a column
        '''
        if index.column() == 2:
            return _QtCore.Qt.ItemIsEnabled | _QtCore.Qt.ItemIsSelectable
        # if index.column() == 8 and index.data().strip():
        #     return _QtCore.Qt.ItemIsEnabled | _QtCore.Qt.ItemIsSelectable
        if self.index(index.row(), 8).data().strip():
            return _QtCore.Qt.ItemIsEnabled | _QtCore.Qt.ItemIsSelectable
        return super(QuotationReportTableModel, self).flags(index)

    def addQuotationInfo(self, customerName, customerAddress, quotationNo, quotationDate, validUntilDate, amount, tax, total, cancel=''):
        '''
        Adds Quotation Report information to the model
        customerName: str
        customerAddress: str
        uotationNo,
        quotationDate,
        validUntilDate,
        amount,
        tax,
        total
        '''
        quotationInfo = QuotationReportDetails(
            customerName,
            customerAddress,
            quotationNo,
            quotationDate,
            validUntilDate,
            amount,
            tax,
            total,
            cancel
        )
        super(QuotationReportTableModel, self).insertRows(self.rowCount(self), [quotationInfo])

    def data(self, index, role):
        '''
        Data method for displaying background color
        '''
        row = index.row()
        column = index.column()
        if role == _QtCore.Qt.BackgroundRole:
            if self._getData(row, column).flag:
                return _QtGui.QBrush(_QtCore.Qt.green)
            if self._getData(row, 8).value:
                return _QtGui.QBrush(_QtCore.Qt.darkYellow)
        return super(QuotationReportTableModel, self).data(index, role)

    def removeRow(self, position, parent=_QtCore.QModelIndex()):
        '''
        Removes quotation report info from model
        '''
        self.removeRows(position, 1, parent)

    def clearTable(self):
        '''
        Clear model
        '''
        self.removeRows(0, self.rowCount(self))


class QuotationReportProxyModel(_genericProxyTableModel.GenericProxyModel):
    '''
    SortFilterProxy model for quotation information
    '''
    def __init__(self, *args, **kwargs):
        super(QuotationReportProxyModel, self).__init__(*args, **kwargs)