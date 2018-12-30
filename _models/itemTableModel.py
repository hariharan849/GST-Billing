#!/usr/bin/env python
# ItemTableModel.py

"""
Item model for displaying company information
"""
#!/usr/bin/env python
# quotationTableModel.py

"""
Quotation Model for holding quotation information
"""

from genericTableModel import GenericTableModel
import genericProxyTableModel as _genericProxyTableModel
from PySide import QtCore as _QtCore
import constants as _constants
from database import CompanyItemManager


class ItemDetails(object):
    '''
    Wrapper class for adding quotation information
    '''
    def __init__(self, itemInfo):
        self.itemCode = _constants.valueWrapper(itemInfo.itemCode, False)
        self.particulars = _constants.valueWrapper(itemInfo.particular, False)
        self.hsnCode = _constants.valueWrapper(itemInfo.hsnCode, False)
        self.quantity = _constants.valueWrapper(itemInfo.quantity, False)
        self.rate = _constants.valueWrapper(itemInfo.rate, False)
        self.sgstValue = _constants.valueWrapper('{} %'.format(itemInfo.sgst or 0), False)
        self.cgstValue = _constants.valueWrapper('{} %'.format(itemInfo.cgst or 0), False)
        self.igstValue = _constants.valueWrapper('{} %'.format(itemInfo.igst or 0), False)

        amountWithoutTax = float(itemInfo.quantity) * float(itemInfo.rate)
        tax = ((amountWithoutTax * float(itemInfo.cgst or 0)) / 100 + (amountWithoutTax * float(itemInfo.sgst or 0)) / 100 + (amountWithoutTax * float(itemInfo.igst or 0)) / 100)
        self.amount = _constants.valueWrapper(str(amountWithoutTax), False)
        self.tax = _constants.valueWrapper(str(tax), False)
        self.total = _constants.valueWrapper(str(amountWithoutTax+tax), False)


class ItemTableModel(GenericTableModel):
    '''
    Item table model to display item information
    '''
    def __init__(self, settings, parent=None):
        super(ItemTableModel, self).__init__([], settings, parent)

        companymanager = CompanyItemManager('sales')
        self.__salesInfo = {companyInfo.itemCode: companyInfo for companyInfo in companymanager.fetchAllCompanyItemInfo()}

    def flags(self, index):
        '''
        Flags for setting columns editable or not
        '''
        return _QtCore.Qt.ItemIsSelectable

    def addItemInfo(self, itemInfo):
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
        # quotationInfo = ItemDetails(
        #     itemCode,
        #     particulars,
        #     hsnCode,
        #     quantity,
        #     rate,
        #     sgstValue,
        #     cgstValue,
        #     igstValue
        # )
        super(ItemTableModel, self).insertRows(self.rowCount(self), [itemInfo])

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

class ItemTableProxyModel(_genericProxyTableModel.GenericProxyModel):
    '''
    SortFilterProxy model for quotation information
    '''
    def __init__(self, *args, **kwargs):
        super(ItemTableProxyModel, self).__init__(*args, **kwargs)