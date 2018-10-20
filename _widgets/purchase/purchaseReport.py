import collections as _collections
import datetime as _datetime

from database import PurchaseManager
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
from ui.purchaseReportUI import Ui_purchaseReport
from models import PurchaseReportTableModel, PurchaseReportProxyModel, constants, PurchaseSaveWorker
from _widgets import utils

from models import constants as _constants
from _widgets import common

class PurchaseReport(_QtGui.QWidget):
    '''
    UI for Purchase Report widget
    '''
    def __init__(self, parent=None):
        super(PurchaseReport, self).__init__(parent)
        self._manager = PurchaseManager()
        self.__purchaseReportUI = Ui_purchaseReport()
        self.__setupWidget()
        self.__connectWidget()
        self.__setpurchaseInformation()

    def __setupWidget(self):
        '''
        Sets all quotation req widgets
        '''
        self.__purchaseReportUI.setupUi(self)

        self.__purchaseModelData = PurchaseReportTableModel()
        self.__purchaseProxyModel = PurchaseReportProxyModel()
        self.__purchaseProxyModel.setSourceModel(self.__purchaseModelData)
        self.__purchaseProxyModel.setDynamicSortFilter(True)
        self.__purchaseProxyModel.setFilterCaseSensitivity(_QtCore.Qt.CaseInsensitive)
        self.__purchaseReportUI.purchaseReportTable.setModel(self.__purchaseProxyModel)

        self.__purchaseReportUI.fromDateValue.setDate(_QtCore.QDate.currentDate())
        self.__purchaseReportUI.toDateValue.setDate(_QtCore.QDate.currentDate())

        self.showMaximized()

    def __connectWidget(self):
        '''
        Connect all widget signal and slots
        '''
        self.__purchaseReportUI.resetButton.clicked.connect(self.__discardChanges)
        self.__purchaseReportUI.searchButton.clicked.connect(self.__searchChanges)
        self.__purchaseReportUI.saveButton.clicked.connect(self.__saveTableChanges)
        self.__purchaseReportUI.purchaseReportTable.removeEntry.connect(self.__removeFromDatabase)
        self.__purchaseReportUI.removeButton.clicked.connect(self.__purchaseReportUI.purchaseReportTable.removeSlot)
        self.__purchaseReportUI.clearButton.clicked.connect(self.__purchaseReportUI.purchaseReportTable.clearSlot)

    def __setpurchaseInformation(self):
        '''
        Sets all purchase order information from db
        '''
        purchaseData = self._manager.fetchAllPurchaseInfo()
        amountPaid = total = tax = 0
        for info in purchaseData:
            self.__purchaseModelData.addPurchaseReportInfo(
                str(info.vendorName),
                str(info.vendorAddress),
                str(info.vendorGstin),
                str(info.vendorStateCode),
                str(info.billNo),
                str(info.billDate),
                str(info.dueDate),
                str(info.payBy),
                str(info.total),
                str(info.tax),
                str(info.amountPaid),
                str(info.remarks),
                str(True),
                info.cancelReason
            )
            if info.cancelReason:
                continue
            tax += float(info.tax)
            total += float(info.total)
            amountPaid += float(info.amountPaid)
        self.__purchaseReportUI.amountValue.setText(str(total))
        self.__purchaseReportUI.totalValue.setText(str(total + tax))
        self.__purchaseReportUI.taxValue.setText(str(tax))
        self.__purchaseReportUI.amountPaidValue.setText(str(amountPaid))
        self.__purchaseReportUI.balanceValue.setText(str(total + tax - amountPaid))

    utils.showWaitCursor
    def __saveTableChanges(self):
        '''
        Save Table change to database
        '''
        worker = PurchaseSaveWorker(self.__purchaseReportUI.tableData, self._manager)
        worker.start()
        _QtGui.QMessageBox.information(self, 'Saved', 'Purchase Information Saved Successfully.',
                                       buttons=_QtGui.QMessageBox.Ok)

    def __removeFromDatabase(self, row='all'):
        '''
        Removes entry from database
        '''
        if row != 'all':
            purchaseInfoEntry = self._manager.getPurchaseDetailsInfo(self.__purchaseProxyModel.index(row, 4).data())
            # print purchaseInfoEntry.cancelReason, len(purchaseInfoEntry.cancelReason)
            if not purchaseInfoEntry.cancelReason:
                print float(self.__purchaseReportUI.amountValue.text())
                amount = float(self.__purchaseReportUI.amountValue.text()) -  float(purchaseInfoEntry.total)
                self.__purchaseReportUI.amountValue.setText(str(amount))
                self.updateAmountValue(row)
            purchaseInfoEntry.delete()
            return
        self._manager.deletePurchaseDetailsInfo()
        self.__purchaseReportUI.amountValue.setText('')
        self.__purchaseReportUI.taxValue.setText('')
        self.__purchaseReportUI.totalValue.setText('')
        self.__purchaseReportUI.amountPaidValue.setText('')
        self.__purchaseReportUI.balanceValue.setText('')

    def __validateSearchDate(self):
        '''
        Validates search from and to date
        '''
        if self.__purchaseReportUI.fromDateValue.date() > self.__purchaseReportUI.toDateValue.date():
            _QtGui.QMessageBox.critical(self, 'Error', 'From Date is Greater than To Date', buttons=_QtGui.QMessageBox.Ok)
            return False
        return True

    utils.showWaitCursor
    def __searchChanges(self):
        '''
        Validates input and save changes in database and updates table.
        '''
        if not self.__validateSearchDate():
            return

        customerName = str(self.__purchaseReportUI.customerSearchValue.text())
        billNo = str(self.__purchaseReportUI.billSearchValue.text())
        fromDate = self.__purchaseReportUI.fromDateValue.date()
        toDate = self.__purchaseReportUI.toDateValue.date()

        self.__purchaseProxyModel.setFilterByColumn(
            _QtCore.QRegExp(billNo, _QtCore.Qt.CaseSensitive, _QtCore.QRegExp.FixedString),4)
        self.__purchaseProxyModel.setFilterByColumn(
            _QtCore.QRegExp(customerName, _QtCore.Qt.CaseSensitive, _QtCore.QRegExp.FixedString), 0)
        self.__purchaseProxyModel.setFilterByColumn(
            constants.dateFilter(fromDate.toString('dd - MMM - yyyy'), toDate.toString('dd - MMM - yyyy')), 5)
        self.updateAmountValue()

    utils.showWaitCursor
    def __discardChanges(self):
        self.__purchaseReportUI.customerSearchValue.setText('')
        self.__purchaseReportUI.billSearchValue.setText('')
        self.__purchaseReportUI.fromDateValue.setDate(_QtCore.QDate.currentDate())
        self.__purchaseReportUI.toDateValue.setDate(_QtCore.QDate.currentDate())
        self.__purchaseReportUI.purchaseReportTable.clearSlot()
        self.__purchaseReportUI.amountValue.setText('')
        self.__purchaseReportUI.taxValue.setText('')
        self.__purchaseReportUI.totalValue.setText('')
        self.__purchaseReportUI.amountPaidValue.setText('')
        self.__purchaseReportUI.balanceValue.setText('')

    def viewItems(self, purchaseNo):
        purchaseProduct = self._manager.getPurchaseItemInfo(purchaseNo)

        itemInfoWidget = common.itemInfoWidget.ItemInfoWidget(purchaseNo, purchaseProduct, _constants._quotationSettings, parent=self)
        itemInfoWidget.show()

    def cancelBill(self, billNo, cancelReason):
        purchaseDetails = self._manager.getPurchaseDetailsInfo(billNo)
        purchaseDetails.cancelReason = cancelReason
        purchaseTableData = [data for data in self.__purchaseModelData.tableData if data.billNo.value == billNo]
        purchaseTableData[0].cancelReason = _constants.valueWrapper(cancelReason, False)
        purchaseDetails.save()
        self.updateAmountValue()

    def addItemInfo(self, itemInfo):
        return ItemDetails(itemInfo)

    def updateAmountValue(self, cancelRow=None):
        '''
        Received when model data is removed
        '''
        amount = tax = total = amountPaid = balance = 0
        # print self.__purchaseProxyModel.rowCount()
        for row in range(self.__purchaseProxyModel.rowCount()):
            if row == cancelRow:
                continue
            if self.__purchaseProxyModel.index(row, 15).data():
                continue
            amount += float(self.__purchaseProxyModel.index(row, 8).data())
            tax += float(self.__purchaseProxyModel.index(row, 9).data())
            total += float(self.__purchaseProxyModel.index(row, 10).data())
            amountPaid += float(self.__purchaseProxyModel.index(row, 11).data())
            balance += float(self.__purchaseProxyModel.index(row, 12).data())
        self.__purchaseReportUI.amountValue.setText(str(amount))
        self.__purchaseReportUI.totalValue.setText(str(total))
        self.__purchaseReportUI.taxValue.setText(str(tax))
        self.__purchaseReportUI.amountPaidValue.setText(str(amountPaid))
        self.__purchaseReportUI.balanceValue.setText(str(balance))


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
        self.cgstValue = _constants.valueWrapper(itemInfo.cgst, False)
        self.sgstValue = _constants.valueWrapper(itemInfo.sgst, False)
        self.igstValue = _constants.valueWrapper(itemInfo.igst, False)

        # taxValue = (amountWithoutTax * cgst) / 100.0 + (amountWithoutTax * sgst) / 100.0 + (
        #         amountWithoutTax * igst) / 100.0
        tax = itemInfo.cgst + itemInfo.sgst + itemInfo.igst
        self.tax = _constants.valueWrapper(tax, False)

        amount = float(itemInfo.quantity) * float(itemInfo.rate)
        self.total = _constants.valueWrapper(amount+tax, False)
        self.amount = _constants.valueWrapper(amount, False)