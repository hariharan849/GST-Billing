# -*- coding: utf-8 -*-
'''
User Interface for credit Voucher.
'''

import datetime as _datetime

from database import Voucher, VoucherManager
from models import constants, VoucherTableModel, VoucherProxyModel, VoucherSaveWorker
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
from ui.voucherUI import Ui_Voucher
from _widgets import utils


class VoucherWidget(_QtGui.QWidget):
    '''
    UI for credit voucher widget
    '''
    def __init__(self, parent=None, type='credit'):
        super(VoucherWidget, self).__init__(parent)
        self.__type = type
        self.voucherManager = VoucherManager(type)
        self.__voucherUI = Ui_Voucher()
        self.__setupWidget()
        self.__connectWidget()
        self.__addWidgetValidators()

    def __setVoucherInformation(self):
        '''
        Sets all voucher information from db
        '''
        voucherTableData = []
        voucherData = self.voucherManager.fetchAllVoucherInfo()
        totalAmount = 0
        for info in voucherData:
            print info.voucherDate.strftime('%d - %b - %Y')
            self.__voucherModelData.addVoucherInfo(
                str(info.voucherNo),
                str(info.customerName),
                info.voucherDate.strftime('%d - %b - %Y'),
                str(info.remarks),
                str(info.paymentType),
                str(info.chequeNo),
                str(info.amount)
            )
            totalAmount += float(info.amount)
        self.__voucherUI.totalAmountValue.setText(str(totalAmount))

    def __setupWidget(self):
        '''
        Sets up widget before initializing.
        '''
        self.__voucherUI.setupUi(self)
        paymentTypes = ('Cash', 'Cheque', 'online')
        self.__voucherUI.paymentValue.addItems(paymentTypes)

        self.__voucherModelData = VoucherTableModel()
        self.__voucherProxyModel = VoucherProxyModel()
        self.__voucherProxyModel.setSourceModel(self.__voucherModelData)
        self.__voucherProxyModel.setDynamicSortFilter(True)
        self.__voucherProxyModel.setFilterCaseSensitivity(_QtCore.Qt.CaseInsensitive)
        self.__voucherUI.voucherTable.setModel(self.__voucherProxyModel)

        dateLabel = 'Credit Date' if self.__type == 'credit' else 'Debit Date'
        self.__voucherUI.dateLabel.setText(dateLabel)
        constants._voucherSettings[2][constants._columnName] = dateLabel
        self.__voucherUI.dateValue.setDate(_QtCore.QDate.currentDate())

        self.__voucherUI.fromDateValue.setDate(_QtCore.QDate.currentDate())
        self.__voucherUI.toDateValue.setDate(_QtCore.QDate.currentDate())

        self.__setVoucherInformation()

        for i in range(self.__voucherModelData.rowCount(self)):
            self.__voucherUI.voucherTable.openPersistentEditor(self.__voucherModelData.index(i, 4))

        self._disableAllLabels()

        self.showMaximized()

    def _disableAllLabels(self):
        self.__voucherUI.voucherMandLabel.setVisible(False)
        self.__voucherUI.nameMandLabel.setVisible(False)
        self.__voucherUI.remarksMandLabel.setVisible(False)
        self.__voucherUI.amountMandLabel.setVisible(False)
        self.__voucherUI.chequeMandLabel.setVisible(False)

    def __addWidgetValidators(self):
        '''
        Adds validators for the widgets
        '''
        self.__voucherUI.billSearchValue.setValidator(_QtGui.QIntValidator())
        self.__voucherUI.voucherNoValue.setValidator(_QtGui.QIntValidator())
        self.__voucherUI.amountValue.setValidator(_QtGui.QDoubleValidator())
        inpHeight = self.__voucherUI.inputGroupBox.height()#self.__voucherUI.inputGroupBox.height()
        self.__voucherUI.inputGroupBox.toggled.connect(lambda: utils.toggleGroup(self.__voucherUI.inputGroupBox, inpHeight))
        self.__voucherUI.groupBox.toggled.connect(lambda: utils.toggleGroup(self.__voucherUI.groupBox, self.__voucherUI.groupBox.height()))

    def __connectWidget(self):
        '''
        Connect all widget signal and slots
        '''
        self.__voucherUI.saveButton.clicked.connect(self.__saveChanges)
        self.__voucherUI.discardButton.clicked.connect(self._discardChanges)
        self.__voucherUI.searchButton.clicked.connect(self.__searchVoucherInfo)
        self.__voucherUI.resetButton.clicked.connect(self.__resetSearchWidget)
        self.__voucherUI.paymentValue.currentIndexChanged.connect(self.__flagChequeValue)
        self.__voucherUI.saveTableButton.clicked.connect(self.__saveTableChanges)
        self.__voucherUI.voucherTable.removeEntry.connect(self.__removeFromDatabase)
        self.__voucherUI.removeButton.clicked.connect(self.__voucherUI.voucherTable.removeSlot)
        self.__voucherUI.clearButton.clicked.connect(self.__voucherUI.voucherTable.clearSlot)
        self.__voucherUI.importButton.clicked.connect(self.__voucherUI.voucherTable.importSlot)

    @utils.showWaitCursor
    def __resetSearchWidget(self):
        '''
        Resets all search widget values to default
        '''
        self.__voucherUI.customerSearchValue.setText('')
        self.__voucherUI.billSearchValue.setText('')
        self.__voucherUI.fromDateValue.setDate(_QtCore.QDate.currentDate())
        self.__voucherUI.toDateValue.setDate(_QtCore.QDate.currentDate())

    def __flagChequeValue(self, index):
        '''
        Enables/disables cheque value based on payment index
        '''
        if index != 0:
            self.__voucherUI.chequeNoValue.setText('')
        self.__voucherUI.chequeNoValue.setReadOnly(index == 0)

    def __validateSearchDate(self):
        '''
        Validates search from and to date
        '''
        if self.__voucherUI.fromDateValue.date() > self.__voucherUI.toDateValue.date():
            _QtGui.QMessageBox.critical(self, 'Error', 'From Date is Greater than To Date', buttons=_QtGui.QMessageBox.Ok)
            return False
        return True

    @utils.showWaitCursor
    def __searchVoucherInfo(self):
        '''
        Search Voucher information for the entered inputs
        '''
        customerName = str(self.__voucherUI.customerSearchValue.text())
        voucherNo = str(self.__voucherUI.billSearchValue.text())
        fromDate = self.__voucherUI.fromDateValue.date()
        toDate = self.__voucherUI.toDateValue.date()
        if not self.__validateSearchDate():
            return

        self.__voucherProxyModel.setFilterByColumn(
            _QtCore.QRegExp(voucherNo, _QtCore.Qt.CaseSensitive, _QtCore.QRegExp.FixedString),0)
        self.__voucherProxyModel.setFilterByColumn(
            _QtCore.QRegExp(customerName, _QtCore.Qt.CaseSensitive, _QtCore.QRegExp.FixedString), 1)
        self.__voucherProxyModel.setFilterByColumn(
            utils.dateFilter(fromDate.toString('dd - MMM - yyyy'), toDate.toString('dd - MMM - yyyy')), 2)
        self.__updateAmountValue()

    def __removeFromDatabase(self, row='all'):
        '''
        Removes entry from database
        '''
        if row != 'all':
            voucherInfoEntry = self.voucherManager.getVoucherInfo(self.__voucherProxyModel.index(row, 0).data())
            amount = float(self.__voucherUI.totalAmountValue.text()) -  float(voucherInfoEntry.amount)
            self.__voucherUI.totalAmountValue.setText(str(amount))
            voucherInfoEntry.delete()
            return
        self.voucherManager.deleteVoucherInfo()
        self.__voucherUI.totalAmountValue.setText('')

    def __saveTableChanges(self):
        '''
        Save Table change to database
        '''
        worker = VoucherSaveWorker(self.__voucherModelData.tableData, self.voucherManager)
        worker.start()
        worker.wait()
        self.__updateAmountValue()
        _QtGui.QMessageBox.information(self, 'Saved', 'Voucher Information Saved Successfully.', buttons=_QtGui.QMessageBox.Ok)

    @utils.showWaitCursor
    def __saveChanges(self):
        '''
        Validates input and save changes in database and updates table.
        '''
        if not self.__validateVoucherInputs():
            return
        voucherNo = str(self.__voucherUI.voucherNoValue.text())
        customerName = str(self.__voucherUI.nameValue.text())
        voucherDate = _datetime.date(
            self.__voucherUI.dateValue.date().year(),
            self.__voucherUI.dateValue.date().month(),
            self.__voucherUI.dateValue.date().day()
        )
        remarks = str(self.__voucherUI.remarksValue.text())
        paymentType = str(self.__voucherUI.paymentValue.currentText())
        chequeNo = str(self.__voucherUI.chequeNoValue.text() if self.__voucherUI.chequeNoValue.text() else 'NA')
        amount = str(self.__voucherUI.amountValue.text())
        voucherDate = voucherDate.strftime("%d - %b - %Y")

        args = (voucherNo, customerName, voucherDate, remarks, paymentType, chequeNo, amount)
        self.voucherManager.saveVoucherInfo(*args)
        self.__voucherModelData.addVoucherInfo(*args)
        self.__updateAmountValue()
        self._discardChanges()

    def _discardChanges(self):
        '''
        Discards all widgets to default values.
        '''
        self.__voucherUI.voucherNoValue.setText('')
        self.__voucherUI.nameValue.setText('')
        self.__voucherUI.dateValue.setDate(_QtCore.QDate.currentDate())
        self.__voucherUI.remarksValue.setText('')
        self.__voucherUI.paymentValue.setCurrentIndex(0)
        self.__voucherUI.chequeNoValue.setText('')
        self.__voucherUI.amountValue.setText('')
        self._disableAllLabels()

    def __validateVoucherInputs(self):
        '''
        Validates all user inputs.
        '''
        valid = True
        if not self.__voucherUI.voucherNoValue.text():
            self.__voucherUI.voucherMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Voucher Number must be entered', buttons=_QtGui.QMessageBox.Ok)
            valid = False
        if not self.__voucherUI.nameValue.text():
            self.__voucherUI.nameMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Name must be entered', buttons=_QtGui.QMessageBox.Ok)
            valid = False
        if not self.__voucherUI.remarksValue.text():
            self.__voucherUI.remarksMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Remarks must be entered', buttons=_QtGui.QMessageBox.Ok)
            valid = False
        if not self.__voucherUI.amountValue.text():
            self.__voucherUI.amountMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Amount must be entered', buttons=_QtGui.QMessageBox.Ok)
            valid = False
        if self.__voucherUI.paymentValue.currentText() == 'Cheque' and self.__voucherUI.chequeNoValue.text().strip():
            self.__voucherUI.chequeMandLabel.setVisible(True)
            valid = False
        voucherNos = self.voucherManager.fetchAllVoucherNo()
        if self.__voucherUI.voucherNoValue.text() in  voucherNos:
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Voucher Number is already available', buttons=_QtGui.QMessageBox.Ok)
            valid = False
        return valid

    def __updateAmountValue(self):
        '''
        Received when model data is removed
        '''
        amount = 0
        for row in range(self.__voucherProxyModel.rowCount()):
            amount += float(self.__voucherProxyModel.index(row, 6).data())
        self.__voucherUI.totalAmountValue.setText(str(amount))
