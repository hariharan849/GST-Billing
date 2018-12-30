import collections as _collections
import datetime as _datetime
import pandas as _pd
import os as _os

from database import PurchaseManager
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
from ui.purchaseReportUI import Ui_purchaseReport
from models import PurchaseReportTableModel, PurchaseReportProxyModel, constants, PurchaseSaveWorker
from _widgets import utils, common


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
        Sets all purchasw report widgets
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
                'Paid' if round(float(info.total)) == round(float(info.amountPaid)) else 'Not Paid',
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
        worker = PurchaseSaveWorker(self.__purchaseModelData.tableData, self._manager)
        worker.start()
        _QtGui.QMessageBox.information(self, 'Saved', 'Purchase Information Saved Successfully.',
                                       buttons=_QtGui.QMessageBox.Ok)
        self.updateAmountValue()

    def __removeFromDatabase(self, row='all'):
        '''
        Removes entry from database
        '''
        if row != 'all':
            purchaseInfoEntry = self._manager.getPurchaseDetailsInfo(self.__purchaseProxyModel.index(row, 4).data())
            # print purchaseInfoEntry.cancelReason, len(purchaseInfoEntry.cancelReason)
            if not purchaseInfoEntry.cancelReason:
                amount = float(self.__purchaseReportUI.amountValue.text()) -  float(purchaseInfoEntry.total)
                self.__purchaseReportUI.amountValue.setText(str(amount))
                self.updateAmountValue(row)
            purchaseInfoEntry.delete_instance()
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
        '''
        Resets all widgets to default value
        '''
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
        '''
        Launches dialog to show items associated with purchase no
        '''
        purchaseInfo = self._manager.getPurchaseDetailsInfo(purchaseNo)
        purchaseProduct = self._manager.getItemInfo(purchaseNo)

        dialog = _QtGui.QDialog(self)
        itemInfoWidget = common.itemInfoWidget.ItemInfoWidget(purchaseNo, purchaseProduct, constants._quotationSettings, purchaseInfo.remarks, parent=self)
        layout = _QtGui.QHBoxLayout(dialog)
        layout.addWidget(itemInfoWidget)
        dialog.setWindowTitle('Purchase Item')
        dialog.exec_()

    def cancelBill(self, billNo, cancelReason):
        '''
        Cancels the selected puchase no to cancel
        '''
        purchaseDetails = self._manager.getPurchaseDetailsInfo(billNo)
        purchaseDetails.cancelReason = cancelReason
        purchaseTableData = [data for data in self.__purchaseModelData.tableData if data.billNo.value == billNo]
        purchaseTableData[0].cancelReason = constants.valueWrapper(cancelReason, False)
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

    def exportToExcel(self, isLimited=False):
        '''
        Exports purchase information to excel
        '''
        df = self._getDataframe(isLimited)
        exportPath = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(__file__))), 'Exports', 'Purchase')
        try:
            _os.makedirs(exportPath)
        except Exception as ex:
            pass
        now = _datetime.datetime.now()
        file_name = '{}_{}_{}-{}_{}_{}.xlsx'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        writer = _pd.ExcelWriter(
            _os.path.join(exportPath, file_name)
        )
        df.to_excel(writer, 'Sheet1', index=False, index_label=False)
        writer.save()
        _QtGui.QMessageBox.information(self, 'Saved', 'Purchase Information Exported Successfully.',
                                       buttons=_QtGui.QMessageBox.Ok)

    def _getDataframe(self, isLimited):
        '''
        Gets data frame for puchase information
        '''
        name, address, gstin, state_code = [], [], [], []
        bill_no, bill_date, sgst, igst, due_date, pay_by = [], [], [], [], [], []
        amount, cgst, total, amount_paid, balance, status, remarks = [], [], [], [], [], [], []

        for i in range(self.__purchaseProxyModel.rowCount()):
            entry = self._manager.getPurchaseDetailsInfo(self.__purchaseProxyModel.index(i, 4).data())
            if entry.cancelReason:
                continue
            name.append(entry.vendorName)
            gstin.append(entry.vendorGstin)
            bill_no.append(entry.billNo)
            bill_date.append(entry.billDate)
            amount.append(entry.total)
            total.append(entry.total+entry.tax)
            amount_paid.append(entry.amountPaid)
            remarks.append(entry.remarks)

            if not isLimited:
                address.append(entry.vendorAddress)
                state_code.append(entry.vendorStateCode)
                due_date.append(entry.dueDate)
                pay_by.append(entry.payBy)
                balance.append(entry.amountPaid - (entry.total+entry.tax))
                status.append(entry.amountPaid - (entry.total+entry.tax) <= 0)

        purchaseValues = _collections.OrderedDict()
        purchaseValues['Vendor Name'] = name
        purchaseValues['Vendor GSTIN'] = gstin
        purchaseValues['Bill No'] = bill_no
        purchaseValues['Bill Date'] = bill_date
        purchaseValues['Amount'] = amount
        purchaseValues['Total'] = total
        purchaseValues['Amount Paid'] = amount_paid
        purchaseValues['Balance'] = balance
        purchaseValues['Pay Remarks'] = remarks
        if not isLimited:
            purchaseValues['Vendor Address'] = address
            purchaseValues['Vendor State Code'] = state_code
            purchaseValues['Due Date'] = due_date
            purchaseValues['Paid By'] = pay_by
            purchaseValues['Status'] = status

        return _pd.DataFrame(purchaseValues)


class ItemDetails(object):
    '''
    Wrapper class for adding quotation information
    '''
    def __init__(self, itemInfo):
        self.itemCode = constants.valueWrapper(itemInfo.itemCode, False)
        self.particulars = constants.valueWrapper(itemInfo.particular, False)
        self.hsnCode = constants.valueWrapper(itemInfo.hsnCode, False)
        self.quantity = constants.valueWrapper(itemInfo.quantity, False)
        self.rate = constants.valueWrapper(itemInfo.rate, False)
        self.cgstValue = constants.valueWrapper(itemInfo.cgst, False)
        self.sgstValue = constants.valueWrapper(itemInfo.sgst, False)
        self.igstValue = constants.valueWrapper(itemInfo.igst, False)

        tax = itemInfo.cgst + itemInfo.sgst + itemInfo.igst
        self.tax = constants.valueWrapper(tax, False)

        amount = float(itemInfo.quantity) * float(itemInfo.rate)
        self.total = constants.valueWrapper(amount+tax, False)
        self.amount = constants.valueWrapper(amount, False)