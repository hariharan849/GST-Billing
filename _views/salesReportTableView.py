#!/usr/bin/env python
# salesReportTableView.py

"""
salesreportView for displaying sales report model information
"""


import os as _os
import datetime as _datetime
from PySide import QtGui as _QtGui
from delegates import customDelegates as _customDelegates
import genericTableView as _genericTableView
from _widgets import utils


class SalesReportTable(_genericTableView.GenericTableView):
    '''
    Sales report table view for displaying model
    '''
    def __init__(self, parent=None):
        super(SalesReportTable, self).__init__(parent)

        dateDelegate = _customDelegates.DateDelegate(self)
        self.setItemDelegateForColumn(4, dateDelegate)

        header = self.horizontalHeader()
        header.setResizeMode(0, _QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, _QtGui.QHeaderView.ResizeToContents)


    def contextMenuEvent(self, event):
        '''
        Triggered on mouse right click event
        '''

        row = self.indexAt(self.parent().mapToParent(event.pos())).row()
        itemViewAction = _QtGui.QAction('View Items', self)
        itemViewAction.triggered.connect(self._viewItems)

        cancelAction = _QtGui.QAction('Cancel PO', self)
        cancelAction.triggered.connect(self._cancelPO)

        createPdfAction = _QtGui.QAction('Create PDF', self)

        limitedExportAction = _QtGui.QAction('Limited Detail Export', self)
        limitedExportAction.triggered.connect(self.parent().exportToExcel)

        exportAction = _QtGui.QAction('Export to Excel', self)
        exportAction.triggered.connect(lambda: self.parent().exportToExcel(islimited=True))

        super(SalesReportTable, self).contextMenuEvent(event)
        self.menu.addAction(itemViewAction)

        billNo = self.model().index(self.selectedIndexes()[-1].row(), 2).data()
        salesDetails = self.parent()._manager.getSalesInfo(billNo)
        createPdfAction.triggered.connect(lambda: self.parent().createPDF(billNo))

        if not salesDetails.cancelReason:
            self.menu.addAction(cancelAction)
        self.menu.addAction(createPdfAction)
        self.menu.addAction(limitedExportAction)
        self.menu.addAction(exportAction)

    def _viewItems(self):
        billNo = self.model().index(self.selectedIndexes()[-1].row(), 2).data()
        self.parent().viewItems(billNo)

    def _cancelPO(self):
        text, ok = _QtGui.QInputDialog.getText(self, 'Reason', 'Enter Reason for cancel')
        if not ok:
            return
        billNo = self.model().index(self.selectedIndexes()[-1].row(), 2).data()
        self.parent().cancelBill(billNo, text)

        _QtGui.QMessageBox.information(self, 'Cancel', 'Sales Details Cancelled from Table Successfully', buttons=_QtGui.QMessageBox.Ok)

    @utils.showWaitCursor
    def exportSlot(self):
        '''
        Slot for exporting excel
        '''
        purchaseFolder = _os.path.join(
            _os.path.dirname(
                _os.path.dirname(__file__)),
            'Exports',
            self.parent().type
        )
        try:
            _os.makedirs(purchaseFolder)
        except:
            pass
        fileName = _os.path.join(
            purchaseFolder,
            '{0}.xlsx'.format(_datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S'))
        )
        super(SalesReportTable, self).exportSlot(fileName, 14)
        _QtGui.QMessageBox.information(self, 'Exported', 'Sales Information Exported Successfully.', buttons=_QtGui.QMessageBox.Ok)
