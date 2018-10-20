#!/usr/bin/env python
# companyItemTableModel.py

"""
Company item model for displaying company information
"""

import re as _re
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
from database import CompanyItems
import constants as _constants
import genericProxyTableModel as _genericProxyTableModel
import genericTableModel as _genericTableModel

mutex = _QtCore.QMutex()

class CompanyItemSaveWorker(_QtCore.QThread):

    def __init__(self, companyItemInfo, type, manager):
        super(CompanyItemSaveWorker, self).__init__()
        self.__companyItemInfo = companyItemInfo
        self.__type = type
        self.__manager = manager

    def run(self):
        for companyItemInfo in self.__companyItemInfo:
            mutex.lock()
            companyData = self.__manager.getCompanyItemInfo(companyItemInfo.itemCode.value)
            companyData.itemName = companyItemInfo.particulars.value
            companyData.hsnCode = companyItemInfo.hsnCode.value
            companyData.quantity = companyItemInfo.quantity.value
            companyData.itemPrice = float(companyItemInfo.rate.value)
            companyData.type = self.__type
            companyData.save()
            mutex.unlock()

class CompanyItemDetails(object):
    '''
    Wrapper class for adding company item information
    '''
    def __init__(self, itemCode, particulars, hsnCode, quantity, rate):
        self.itemCode = _constants.valueWrapper(itemCode, False)
        self.particulars = _constants.valueWrapper(particulars, False)
        self.hsnCode = _constants.valueWrapper(hsnCode, False)
        self.quantity = _constants.valueWrapper(quantity, False)
        self.rate = _constants.valueWrapper(rate, False)


class CompanyItemTableModel(_genericTableModel.GenericTableModel):
    '''
    Company item table model to display item information
    '''
    def __init__(self, parent=None):
        super(CompanyItemTableModel, self).__init__([], _constants._companyItemSettings, parent)

    def data(self, index, role):
        '''
        Data method for displaying background color
        '''
        row = index.row()
        column = index.column()
        if role == _QtCore.Qt.BackgroundRole:
            if self._getData(row, column).flag:
                return _QtGui.QBrush(_QtCore.Qt.green)
        return super(CompanyItemTableModel, self).data(index, role)

    def flags(self, index):
        '''
        Flags for editing/selecting a column
        '''
        if index.column() == 0:
            return _QtCore.Qt.ItemIsEnabled | _QtCore.Qt.ItemIsSelectable
        return super(CompanyItemTableModel, self).flags(index)

    def addCompanyItemInfo(self, itemCode, particulars, hsnCode, quantity, rate):
        '''
        itemCode: (str)
        particulars: (str)
        hsnCode:(str)
        quantity: (str)
        rate: (str)
        '''
        companyItemInfo = CompanyItemDetails(
            itemCode,
            particulars,
            hsnCode,
            quantity,
            rate
        )
        super(CompanyItemTableModel, self).insertRows(self.rowCount(self), [companyItemInfo])

    def removeRow(self, position, parent=_QtCore.QModelIndex()):
        '''
        Removes company item info from model
        '''
        self.removeRows(position, 1, parent)

    def clearTable(self):
        '''
        Clear model
        '''
        self.removeRows(0, self.rowCount(self))


class CompanyItemProxyModel(_genericProxyTableModel.GenericProxyModel):
    '''
    SortFilterProxy model for company information
    '''
    def __init__(self, *args, **kwargs):
        super(CompanyItemProxyModel, self).__init__(*args, **kwargs)