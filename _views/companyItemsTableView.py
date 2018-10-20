#!/usr/bin/env python
# companyItemTableModel.py

"""
Company item model for displaying company information
"""

import os, datetime
import pandas

import genericTableView as _genericTableView
from delegates import customDelegates as _customDelegates
from PySide import (
    QtCore as _QtCore,
    QtGui as _QtGui
)
from _widgets import utils


class CompanyItemTable(_genericTableView.GenericTableView):
    '''
    Customer table view for displaying model
    '''

    def __init__(self, parent=None, type='sales'):
        super(CompanyItemTable, self).__init__(parent)
        header = self.horizontalHeader()
        header.setResizeMode(1, _QtGui.QHeaderView.ResizeToContents)

    def contextMenuEvent(self, event):
        '''
        Triggered on mouse right click event
        '''
        super(CompanyItemTable, self).contextMenuEvent(event)

        importAction = _QtGui.QAction('Import from Excel', self)
        importAction.triggered.connect(self.importSlot)
        self.menu.addAction(importAction)

    @utils.showWaitCursor
    def importSlot(self):
        '''
        Slot for importing excel
        '''
        fileName, ok = _QtGui.QFileDialog.getOpenFileName(
            self, 'Import Excel', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'import', ))
        if not ok:
            return
        excelInfo = pandas.read_excel(fileName)
        itemCodes = excelInfo['Item Code']
        particulars = excelInfo['Particulars']
        hsnCodes = excelInfo['HSN Code']
        quantities = excelInfo['Quantity']
        rates = excelInfo['Rate']
        for itemCode, particular, hsnCode, quantity, rate in zip(
                itemCodes, particulars, hsnCodes, quantities, rates):
            self.model().sourceModel().addCompanyItemInfo(
                itemCode, particular, hsnCode, quantity, rate)
            self.parent().companyItemManager.saveCompanyItemInfo(itemCode, particular, hsnCode, quantity, rate)
        _QtGui.QMessageBox.information(self, 'Imported', 'Company Item Information Imported Successfully.',
                                      buttons=_QtGui.QMessageBox.Ok)

    @utils.showWaitCursor
    def exportSlot(self):
        '''
        Slot for importing excel
        '''
        voucherFolder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Exports', 'CompanyItems')
        try:
            os.makedirs(voucherFolder)
        except:
            pass
        fileName = os.path.join(voucherFolder, '{0}.xlsx'.format(datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')))
        super(CompanyItemTable, self).exportSlot(fileName)
        _QtGui.QMessageBox.information(self, 'Exported', 'Company Item Information Exported Successfully.', buttons=_QtGui.QMessageBox.Ok)