#!/usr/bin/env python
# purchaseOrderReportTableView.py

"""
quotationreportView for displaying quotation report model information
"""


from delegates import customDelegates as _customDelegates
import genericTableView as _genericTableView
from PySide import QtCore as _QtCore, QtGui as _QtGui


class PurchaseOrderReportTable(_genericTableView.GenericTableView):
    '''
    Purchase Order table view for displaying model
    '''
    def __init__(self, parent=None):
        super(PurchaseOrderReportTable, self).__init__(parent)

        dateDelegate = _customDelegates.DateDelegate(self)
        self.setItemDelegateForColumn(2, dateDelegate)
        dateDelegate.dataUpdate.connect(self.__updateDateInModel)

        header = self.horizontalHeader()
        header.setResizeMode(3, _QtGui.QHeaderView.ResizeToContents)

    def __updateDateInModel(self, index):
        '''
        Slot for updating date in model
        '''
        self.model().sourceModel().setData(index, self.indexWidget(index).date().toString('dd - MMM - yyyy'), role=_QtCore.Qt.EditRole)

    def contextMenuEvent(self, event):
        '''
        Triggered on mouse right click event
        '''

        row = self.indexAt(self.parent().mapToParent(event.pos())).row()
        itemViewAction = _QtGui.QAction('View Items', self)
        itemViewAction.triggered.connect(self._viewItems)

        cancelAction = _QtGui.QAction('Cancel PO', self)
        cancelAction.triggered.connect(self._cancelPO)

        # reasonAction = _QtGui.QAction('View Reason for Cancel', self)
        # reasonAction.triggered.connect(self._viewReasonAction)

        super(PurchaseOrderReportTable, self).contextMenuEvent(event)
        self.menu.addAction(itemViewAction)

        poNo = self.model().index(self.selectedIndexes()[-1].row(), 1).data()
        poDetails = self.parent().poManager.getPOInfo(poNo)

        if not poDetails.cancelReason:
            self.menu.addAction(cancelAction)

    def _viewItems(self):
        poNo = self.model().index(self.selectedIndexes()[-1].row(), 1).data()
        self.parent().viewItems(poNo)

    def _cancelPO(self):
        text, ok = _QtGui.QInputDialog.getText(self, 'Reason', 'Enter Reason for cancel')
        if not ok:
            return
        poNo = self.model().index(self.selectedIndexes()[-1].row(), 1).data()
        self.parent().cancelBill(poNo, text)

        _QtGui.QMessageBox.information(self, 'Cancel', 'PO Details Cancelled from Table Successfully', buttons=_QtGui.QMessageBox.Ok)

    def _viewReasonAction(self):
        poNo = self.model().index(self.selectedIndexes()[-1].row(), 1).data()
        self.parent().viewCancelReason(poNo)