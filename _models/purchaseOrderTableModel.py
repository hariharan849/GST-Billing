#!/usr/bin/env python
# purchaseorderTableModel.py

"""
Purchase order Model for holding purchase order information
"""

from genericTableModel import GenericTableModel
from PySide import QtCore as _QtCore
import constants as _constants
from database import CompanyItemManager


class PurchaseOrderTableDetails(object):
    '''
    Wrapper class for adding quotation information
    '''
    __slots__ = ['itemCode', 'particulars', 'hsnCode', 'quantity']
    def __init__(self, itemCode, particulars, hsnCode, quantity):
        self.itemCode = _constants.valueWrapper(itemCode, False)
        self.particulars = _constants.valueWrapper(particulars, False)
        self.hsnCode = _constants.valueWrapper(hsnCode, False)
        self.quantity = _constants.valueWrapper(quantity, False)


class PurchaseOrderTableModel(GenericTableModel):
    '''
    Quotation table model to display quotation information
    '''
    def __init__(self, parent=None):
        super(PurchaseOrderTableModel, self).__init__([], _constants._purchaseOrderSettings, parent)
        self.__manager = CompanyItemManager('purchase')
        self.__salesInfo = {companyInfo.itemCode: companyInfo for companyInfo in self.__manager.fetchAllCompanyItemInfo()}

        for i in range(15):
            self.addPurchaseOrderInfo()

    def data(self, index, role):
        '''
        Returns data for the specified role
        '''
        row = index.row()
        column = index.column()
        if role in (_QtCore.Qt.ToolTipRole, _QtCore.Qt.DisplayRole):
            if column == 0:
                itemCode = self._getData(row, 0).value
                if itemCode and itemCode in self.__salesInfo:
                    salesInfo = self.__salesInfo[itemCode]
                    self._setData(row, 1, salesInfo.itemName)
                    self._setData(row, 2, salesInfo.hsnCode)
        return super(PurchaseOrderTableModel, self).data(index, role)

    def addPurchaseOrderInfo(self, itemCode='', particulars='', hsnCode='', quantity=''):
        '''
        itemCode:
        particulars:
        hsnCode:
        quantity:
        rate:
        sgstValue:
        cgstValue:
        igstValue:
        amount:
        tax:
        total:
        '''
        poInfo = PurchaseOrderTableDetails(
            itemCode,
            particulars,
            hsnCode,
            quantity
        )
        # self.tableData.append([itemCode, particulars, hsnCode, quantity])
        super(PurchaseOrderTableModel, self).insertRows(self.rowCount(self), [poInfo])

    def setFromTextData(self, itemCode, index):
        if itemCode in self.__salesInfo:
            salesInfo = self.__salesInfo[itemCode]
            self._setData(index.row(), 1, salesInfo.itemName)
            self._setData(index.row(), 2, salesInfo.hsnCode)
            self.layoutChanged.emit()

    def removeRow(self, position, parent=_QtCore.QModelIndex()):
        '''
        Removes quotation info from model
        '''
        self.removeRows(position, 1, parent)

    def clearTable(self):
        '''
        Clear model
        '''
        self.removeRows(0, self.rowCount(self))
