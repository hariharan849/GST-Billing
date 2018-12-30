#!/usr/bin/env python
# customerTableView.py

"""
Customer view for displaying customer information
"""

import os, datetime
from PySide import QtGui as _QtGui

import genericTableView as _genericTableView
from _widgets import utils
import pandas

class CustomerTable(_genericTableView.GenericTableView):
    '''
    Customer table view for displaying model
    '''

    def __init__(self, parent=None):
        super(CustomerTable, self).__init__(parent)

        header = self.horizontalHeader()
        header.setResizeMode(1, _QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, _QtGui.QHeaderView.ResizeToContents)

    def contextMenuEvent(self, event):
        '''
        Triggered on mouse right click event
        '''
        super(CustomerTable, self).contextMenuEvent(event)

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
        customerCode = excelInfo['Customer Code']
        customerName = excelInfo['Customer Name']
        customerAddress = excelInfo['Customer Address']
        customerGstin = excelInfo['GSTIN']
        customerState = excelInfo['State Code']
        customerContact = excelInfo['Customer Contact']
        for code, name, address, gstin, contact, state in zip(
                customerCode, customerName, customerAddress, customerGstin, customerContact, customerState):
            self.model().sourceModel().addCustomerInfo(
                code, name, address, gstin, state, contact)
            self.parent().customerManager.saveCustomerInfo(str(code), str(name), str(address), str(gstin), int(state), str(contact))
        _QtGui.QMessageBox.information(self, 'Imported', 'Customer Information Imported Successfully.',
                                      buttons=_QtGui.QMessageBox.Ok)

    @utils.showWaitCursor
    def exportSlot(self):
        '''
        Slot for importing excel
        '''
        voucherFolder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Exports', 'Customer Info')
        try:
            os.makedirs(voucherFolder)
        except:
            pass
        fileName = os.path.join(voucherFolder,
                                '{0}.xlsx'.format(datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')))
        super(CustomerTable, self).exportSlot(fileName)
        _QtGui.QMessageBox.information(self, 'Exported', 'Customer Information Exported Successfully.', buttons=_QtGui.QMessageBox.Ok)
