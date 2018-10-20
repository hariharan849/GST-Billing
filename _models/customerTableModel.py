#!/usr/bin/env python
# customerTableModel.py

"""
CustomerModel for Displaying customer information
"""

import re as _re
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)

import constants as _constants
import genericProxyTableModel as _genericProxyTableModel
import genericTableModel as _genericTableModel
from database import CustomerNames


mutex = _QtCore.QMutex()

class CustomerSaveWorker(_QtCore.QThread):

    def __init__(self, customerInfo, customerManager):
        super(CustomerSaveWorker, self).__init__()
        self.__customerInfo = customerInfo
        self.__customerManager = customerManager

    def run(self):

        for customerInfo in self.__customerInfo:
            mutex.lock()
            companyItemData = self.__customerManager.getCustomerInfo(customerInfo.customerCode.value)
            companyItemData.custName = customerInfo.customerName.value
            companyItemData.custAddress = customerInfo.customerAddress.value
            companyItemData.gstin = customerInfo.gstin.value
            companyItemData.stateCode = customerInfo.stateCode.value
            companyItemData.contactNo = customerInfo.contactNo.value
            companyItemData.save()
            mutex.unlock()

class CustomerDetails(object):
    '''
    Wrapper class for adding customer information
    '''
    def __init__(self, customerCode, customerName, customerAddress, gstin, stateCode, contactNo):
        self.customerCode = _constants.valueWrapper(customerCode, False)
        self.customerName = _constants.valueWrapper(customerName, False)
        self.customerAddress = _constants.valueWrapper(customerAddress, False)
        self.gstin = _constants.valueWrapper(gstin, False)
        self.stateCode = _constants.valueWrapper(stateCode, False)
        self.contactNo = _constants.valueWrapper(contactNo, False)


class CustomerTableModel(_genericTableModel.GenericTableModel):
    '''
    Customer table model to display customer information
    '''
    def __init__(self, parent=None):
        super(CustomerTableModel, self).__init__([], _constants._addCustomerSettings, parent)

    def flags(self, index):
        '''
        Flags for editing/selecting a column
        '''
        if index.column() == 0:
            return _QtCore.Qt.ItemIsEnabled | _QtCore.Qt.ItemIsSelectable
        return super(CustomerTableModel, self).flags(index)

    def addCustomerInfo(self, customerCode, customerName, customerAddress, gstin, stateCode, contactNo):
        '''
        customerNo: (str)
        customerName: (str)
        customerAddress:(str)
        gstin: (str)
        stateCode: (str)
        contactNo: (str)
        '''
        customerInfo = CustomerDetails(
            customerCode,
            customerName,
            customerAddress,
            gstin,
            stateCode,
            contactNo
        )
        return super(CustomerTableModel, self).insertRows(self.rowCount(self), [customerInfo])

    def data(self, index, role):
        '''
        Data method for displaying background color
        '''
        row = index.row()
        column = index.column()
        if role == _QtCore.Qt.BackgroundRole:
            if self._getData(row, column).flag:
                return _QtGui.QBrush(_QtCore.Qt.green)
        return super(CustomerTableModel, self).data(index, role)

    def removeRow(self, position, parent=_QtCore.QModelIndex()):
        '''
        Removes customer info from model
        '''
        self.removeRows(position, 1, parent)

    def clearTable(self):
        '''
        Clear model
        '''
        self.removeRows(0, self.rowCount(self))


class CustomerProxyModel(_genericProxyTableModel.GenericProxyModel):
    '''
    SortFilterProxy model for customer information
    '''
    def __init__(self, *args, **kwargs):
        super(CustomerProxyModel, self).__init__(*args, **kwargs)