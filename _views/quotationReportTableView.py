#!/usr/bin/env python
# quotationreportTableView.py

"""
quotationreportView for displaying quotation report model information
"""

import os as _os
import datetime as _datetime
from PySide import QtGui as _QtGui
from PySide.QtCore import Qt
from PySide.QtGui import QAction

from delegates import customDelegates as _customDelegates
import genericTableView as _genericTableView
from _widgets import utils

class QuotationReportTable(_genericTableView.GenericTableView):
    '''
    Quotation table view for displaying model
    '''
    def __init__(self, parent=None):
        super(QuotationReportTable, self).__init__(parent)

        dateDelegate = _customDelegates.DateDelegate(self)
        self.setItemDelegateForColumn(3, dateDelegate)
        dateDelegate.dataUpdate.connect(self.__updateDateInModel)
        dateDelegate = _customDelegates.DateDelegate(self)
        self.setItemDelegateForColumn(4, dateDelegate)
        dateDelegate.dataUpdate.connect(self.__updateDateInModel)

        header = self.horizontalHeader()
        header.setResizeMode(0, _QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, _QtGui.QHeaderView.ResizeToContents)

    def contextMenuEvent(self, event):
        super(QuotationReportTable, self).contextMenuEvent(event)

        row = self.indexAt(self.parent().mapToParent(event.pos())).row()
        quotationNo = self.model().index(self.selectedIndexes()[-1].row(), 2).data()
        viewQuotatedItemAction = QAction('View Items', self)
        viewQuotatedItemAction.triggered.connect(lambda : self.parent().viewItems(quotationNo))

        cancelAction = _QtGui.QAction('Cancel Quotation', self)
        cancelAction.triggered.connect(self._cancelPO)

        self.menu.addAction(viewQuotatedItemAction)

        quotationNo = self.model().index(self.selectedIndexes()[-1].row(), 2).data()
        quotationDetails = self.parent()._manager.getQuotationDetailsInfo(quotationNo)

        createPdfAction = _QtGui.QAction('Create PDF', self)
        createPdfAction.triggered.connect(lambda: self.parent().createPDF(quotationNo))

        exportAction = _QtGui.QAction('Export to Excel', self)
        exportAction.triggered.connect(self.parent().exportToExcel)

        if not quotationDetails.cancelReason:
            self.menu.addAction(cancelAction)
        self.menu.addAction(createPdfAction)
        self.menu.addAction(exportAction)

    def _cancelPO(self):
        text, ok = _QtGui.QInputDialog.getText(self, 'Reason', 'Enter Reason for cancel')
        if not ok:
            return
        quotationNo = self.model().index(self.selectedIndexes()[-1].row(), 2).data()
        self.parent().cancelBill(quotationNo, text)

        _QtGui.QMessageBox.information(self, 'Cancel', 'Quotation Details Cancelled from Table Successfully', buttons=_QtGui.QMessageBox.Ok)

    def __updateDateInModel(self, date, index):
        self.model().sourceModel().setData(index, date.toString('dd - MMM - yyyy'), role=Qt.EditRole)

    @utils.showWaitCursor
    def exportSlot(self):
        '''
        Slot for exporting excel
        '''
        quotationFolder = _os.path.join(
            _os.path.dirname(
                _os.path.dirname(__file__)),
            'Exports',
            'Quotation'
        )
        try:
            _os.makedirs(quotationFolder)
        except:
            pass
        fileName = _os.path.join(
            quotationFolder,
            '{0}.xlsx'.format(_datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S'))
        )
        super(QuotationReportTable, self).exportSlot(fileName, 8)
        _QtGui.QMessageBox.information(self, 'Exported', 'Quotation Information Exported Successfully.', buttons=_QtGui.QMessageBox.Ok)
