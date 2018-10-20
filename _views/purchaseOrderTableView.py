#!/usr/bin/env python
# purchaseOrderTableView.py

"""
Purchase order for displaying purchase order information
"""

import os, datetime
from PySide import QtGui, QtCore
from _widgets import utils
from delegates import customDelegates as _customDelegates
import genericTableView as _genericTableView


class PurchaseOrderTable(_genericTableView.GenericTableView):
    '''
    Voucher table view for displaying model
    '''
    def __init__(self, parent=None):
        super(PurchaseOrderTable, self).__init__(parent)
        lineEditDelegate = _customDelegates.LineEditDelegate(self)
        self.setItemDelegateForColumn(0, lineEditDelegate)
        lineEditDelegate.lineEditUpdate.connect(self.__updateItems)

    def contextMenuEvent(self, event):
        '''
        Triggered on mouse right click event
        '''
        super(PurchaseOrderTable, self).contextMenuEvent(event)

    @utils.showWaitCursor
    def importSlot(self):
        '''
        Slot for importing excel
        '''
        self.parent().importItems()

    def addRow(self):
        self.model().addPurchaseOrderInfo()

    @utils.showWaitCursor
    def exportSlot(self):
        '''
        Slot for importing excel
        '''
        voucherFolder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Exports', 'Purchase Order Item')
        try:
            os.makedirs(voucherFolder)
        except:
            pass
        fileName = os.path.join(voucherFolder,
                                '{0}.xlsx'.format(datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')))
        super(PurchaseOrderTable, self).exportSlot(fileName)
        QtGui.QMessageBox.information(self, 'Exported', 'Purchase Order Information Exported Successfully.', buttons=QtGui.QMessageBox.Ok)

    def __updateItems(self, text, index):
        self.model().setFromTextData(text, index)

    def removeSlot(self, row=None):
        removeRows = []
        for index in reversed(self.selectedIndexes()):
            if index.row() not in removeRows:
                self.removeEntry.emit(index.row())
                # self.model().removeRow(index.row())
                # self.model().cellWidget
                for i in range(1, 4):
                    value = self.model().index(index.row(), i)
                    self.model().setData(self.model().index(index.row(), i), '', role=QtCore.Qt.EditRole)
                self.model().layoutChanged.emit()
                removeRows.append(index.row())
