#!/usr/bin/env python
# quotationTableModel.py

"""
Quotation Model for holding quotation information
"""

from genericTableModel import GenericTableModel
from PySide import QtCore as _QtCore
import constants as _constants
from database import CompanyItems


class QuotationDetails(object):
    '''
    Wrapper class for adding quotation information
    '''
    def __init__(self, itemCode, particulars, hsnCode, quantity, rate, sgstValue, cgstValue, igstValue, amount, tax, total):
        self.itemCode = _constants.valueWrapper(itemCode, False)
        self.particulars = _constants.valueWrapper(particulars, False)
        self.hsnCode = _constants.valueWrapper(hsnCode, False)
        self.quantity = _constants.valueWrapper(quantity, False)
        self.rate = _constants.valueWrapper(rate, False)
        self.sgstValue = _constants.valueWrapper(sgstValue, False)
        self.cgstValue = _constants.valueWrapper(cgstValue, False)
        self.igstValue = _constants.valueWrapper(igstValue, False)
        self.amount = _constants.valueWrapper(amount, False)
        self.tax = _constants.valueWrapper(tax, False)
        self.total = _constants.valueWrapper(total, False)


class QuotationTableModel(GenericTableModel):
    '''
    Quotation table model to display quotation information
    '''
    def __init__(self, parent=None):
        super(QuotationTableModel, self).__init__([], _constants._quotationSettings, parent)

        self.__salesInfo = {companyInfo.itemCode: companyInfo for companyInfo in CompanyItems.select().where(CompanyItems.type == 'sales')}

        for i in range(15):
            self.addQuotationInfo()

    def flags(self, index):
        '''
        Flags for setting columns editable or not
        '''
        if index.column() in [8, 9, 10]:
            return _QtCore.Qt.ItemIsSelectable
        return super(QuotationTableModel, self).flags(index)

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
                    self._setData(row, 4, salesInfo.itemPrice)

            qty = self._getData(row, 3).value
            rate = self._getData(row, 4).value
            if column not in [8, 9, 10]:
                return super(QuotationTableModel, self).data(index, role)
            if (not qty) or (not rate):
                return ''

            qty, rate = float(qty), float(rate)
            amountWithoutTax = qty * rate

            if column == 8:
                self._setData(row, 8, amountWithoutTax)
                return amountWithoutTax


            cgst = float('0')
            sgst = float('0')
            igst = float('0')
            tax = (amountWithoutTax * cgst) / 100 + (amountWithoutTax * sgst) / 100 + (
                    amountWithoutTax * igst) / 100
            if column == 9:
                self._setData(row, 9, tax)
                return tax
            if column == 10:
                self._setData(row, 10, amountWithoutTax + tax)
                # self.parent(self.index(row, 10)).updateAmountInformation()
                return amountWithoutTax + tax
        return super(QuotationTableModel, self).data(index, role)

    def addQuotationInfo(self, itemCode='', particulars='', hsnCode='', quantity='', rate='',
                         sgstValue='', cgstValue='', igstValue='', amount='', tax='', total=''):
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
        quotationInfo = QuotationDetails(
            itemCode,
            particulars,
            hsnCode,
            quantity,
            rate,
            sgstValue,
            cgstValue,
            igstValue,
            amount,
            tax,
            total
        )
        super(QuotationTableModel, self).insertRows(self.rowCount(self), [quotationInfo])

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
