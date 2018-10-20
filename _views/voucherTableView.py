#!/usr/bin/env python
# voucherTableView.py

"""
Voucher item model for displaying voucher information
"""

import os as _os
import datetime as _datetime
import pandas as _pandas

from PySide import (
    QtCore as _QtCore,
    QtGui as _QtGui
)
from delegates import customDelegates as _customDelegates
import genericTableView as _genericTableView
from _widgets import utils


class VoucherTableView(_genericTableView.GenericTableView):
    '''
    Voucher table view for displaying model
    '''
    def __init__(self, parent=None):
        super(VoucherTableView, self).__init__(parent)

        dateDelegate = _customDelegates.DateDelegate(self)
        self.setItemDelegateForColumn(2, dateDelegate)
        dateDelegate.dataUpdate.connect(self.__updateDateInModel)

        paymentTypes = ['Cash', 'Cheque', 'online']
        comboDelegate = _customDelegates.ComboBoxDelegate(paymentTypes, self)
        self.setItemDelegateForColumn(4, comboDelegate)
        comboDelegate.paymentUpdate.connect(self.__updateComboInModel)

        header = self.horizontalHeader()
        header.setResizeMode(0, _QtGui.QHeaderView.Stretch)
        header.setResizeMode(1, _QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(3, _QtGui.QHeaderView.ResizeToContents)


    def __updateDateInModel(self, index):
        '''
        Slot for updating date in model
        '''
        self.model().setData(index, self.indexWidget(index).date().toString('dd - MMM - yyyy'), role=_QtCore.Qt.EditRole)

    def __updateComboInModel(self, value, index):
        '''
        Slot for updating combobox in model
        '''
        self.model().setData(index, value, role=_QtCore.Qt.EditRole)

    def contextMenuEvent(self, event):
        '''
        Triggered on mouse right click event
        '''
        super(VoucherTableView, self).contextMenuEvent(event)

        importAction = _QtGui.QAction('Import from Excel', self)
        importAction.triggered.connect(self.importSlot)
        self.menu.addAction(importAction)

    @utils.showWaitCursor
    def importSlot(self):
        '''
        Slot for importing excel
        '''
        fileName, ok = _QtGui.QFileDialog.getOpenFileName(
            self, 'Import Excel', _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'import', ))
        if not ok:
            return
        excelInfo = _pandas.read_excel(fileName)
        voucherN_os = excelInfo['Voucher No']
        customerNames = excelInfo['Customer Name']
        creditDates = excelInfo['Credit Date' if self.parent()._type == 'credit' else 'Debit Date']
        remarks = excelInfo['Remarks']
        paymentModes = excelInfo['Payment Mode']
        chequeNos = excelInfo['Cheque No']
        amounts = excelInfo['Amount']
        for voucherNo, customerName, creditDate, remark, paymentMode, chequeNo, amount in zip(
                voucherN_os, customerNames, creditDates, remarks, paymentModes, chequeNos, amounts):
            voucherDate = _datetime.datetime.strptime(creditDate, "%d - %b - %Y")
            voucherInfo = (
                voucherNo,
                customerName,
                voucherDate,
                remark,
                paymentMode,
                chequeNo if chequeNo != 'NaN' else '',
                amount
            )
            self.model().sourceModel().addVoucherInfo(*voucherInfo)
            self.parent().voucherManager.saveVoucherInfo(*voucherInfo)
        _QtGui.QMessageBox.information(
            self,
            'Imported',
            'Voucher Information Imported Successfully.',
            buttons=_QtGui.QMessageBox.Ok
        )

    @utils.showWaitCursor
    def exportSlot(self):
        '''
        Slot for importing excel
        '''
        voucherFolder = _os.path.join(
            _os.path.dirname(
                _os.path.dirname(__file__)),
            'Exports',
            'Voucher'
        )
        try:
            _os.makedirs(voucherFolder)
        except:
            pass
        fileName = _os.path.join(
            voucherFolder,
            '{0}.xlsx'.format(_datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S'))
        )
        super(VoucherTableView, self).exportSlot(fileName)
        _QtGui.QMessageBox.information(self, 'Exported', 'Voucher Information Exported Successfully.', buttons=_QtGui.QMessageBox.Ok)