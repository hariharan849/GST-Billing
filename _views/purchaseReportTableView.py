#!/usr/bin/env python
# purchaseReportTableView.py

"""
purchasereportView for displaying purchase report model information
"""

import os, datetime
from PySide import QtGui as _QtGui, QtCore as _QtCore
from delegates import customDelegates as _customDelegates
import genericTableView as _genericTableView
from _widgets import utils


class PurchaseReportTable(_genericTableView.GenericTableView):
    '''
    Purchase Order table view for displaying model
    '''
    def __init__(self, parent=None):
        super(PurchaseReportTable, self).__init__(parent)

        dateDelegate = _customDelegates.DateDelegate(self)
        dateDelegate.dataUpdate.connect(self.__updateDateInModel)
        self.setItemDelegateForColumn(5, dateDelegate)

        dateDelegate = _customDelegates.DateDelegate(self)
        dateDelegate.dataUpdate.connect(self.__updateDateInModel)
        self.setItemDelegateForColumn(6, dateDelegate)

        header = self.horizontalHeader()
        header.setResizeMode(0, _QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, _QtGui.QHeaderView.ResizeToContents)

        self.setAlternatingRowColors(True)

    def contextMenuEvent(self, event):
        '''
        Triggered on mouse right click event
        '''
        row = self.indexAt(self.parent().mapToParent(event.pos())).row()
        itemViewAction = _QtGui.QAction('View Items', self)
        itemViewAction.triggered.connect(self._viewItems)

        cancelAction = _QtGui.QAction('Cancel Purchase', self)
        cancelAction.triggered.connect(self._cancelPO)

        limitedExportAction = _QtGui.QAction('Limited Detail Export', self)
        limitedExportAction.triggered.connect(self.parent().exportToExcel)

        exportAction = _QtGui.QAction('Export to Excel', self)
        exportAction.triggered.connect(lambda: self.parent().exportToExcel(isLimited=True))

        super(PurchaseReportTable, self).contextMenuEvent(event)
        self.menu.addAction(itemViewAction)

        billNo = self.model().index(self.selectedIndexes()[-1].row(), 4).data()
        poDetails = self.parent()._manager.getPurchaseDetailsInfo(billNo)

        if not poDetails.cancelReason:
            self.menu.addAction(cancelAction)
        self.menu.addAction(limitedExportAction)
        self.menu.addAction(exportAction)

    def _viewItems(self):
        billNo = self.model().index(self.selectedIndexes()[-1].row(), 4).data()
        self.parent().viewItems(billNo)

    def _cancelPO(self):
        text, ok = _QtGui.QInputDialog.getText(self, 'Reason', 'Enter Reason for cancel')
        if not ok:
            return
        billNo = self.model().index(self.selectedIndexes()[-1].row(), 4).data()
        self.parent().cancelBill(billNo, text)

        _QtGui.QMessageBox.information(self, 'Cancel', 'Purchase Details Cancelled from Table Successfully', buttons=_QtGui.QMessageBox.Ok)

    @utils.showWaitCursor
    def exportSlot(self):
        '''
        Slot for importing excel
        '''
        purchaseFolder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Exports', 'Purchase')
        try:
            os.makedirs(purchaseFolder)
        except:
            pass
        fileName = os.path.join(purchaseFolder,
                                '{0}.xlsx'.format(datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')))
        super(PurchaseReportTable, self).exportSlot(fileName)
        _QtGui.QMessageBox.information(self, 'Exported', 'Purchase Information Exported Successfully.', buttons=_QtGui.QMessageBox.Ok)

    def __updateDateInModel(self, date, index):
        self.model().sourceModel().setData(index, date.toString('dd - MMM - yyyy'), role=_QtCore.Qt.EditRole)

    def _viewItems(self):
        poNo = self.model().index(self.selectedIndexes()[-1].row(), 4).data()
        self.parent().viewItems(poNo)

    @utils.showWaitCursor
    def exportSlot(self):
        '''
        Slot for exporting excel
        '''
        purchaseFolder = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)),
            'Exports',
            'Purchase'
        )
        try:
            os.makedirs(purchaseFolder)
        except:
            pass
        fileName = os.path.join(
            purchaseFolder,
            '{0}.xlsx'.format(datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S'))
        )
        super(PurchaseReportTable, self).exportSlot(fileName, 15)
        _QtGui.QMessageBox.information(self, 'Exported', 'Purchase Information Exported Successfully.', buttons=_QtGui.QMessageBox.Ok)
