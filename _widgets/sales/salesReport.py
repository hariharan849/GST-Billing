import collections as _collections
import datetime as _datetime

from database import SalesManager
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
import os as _os
from ui.salesReportUI import Ui_salesReport
from models import SalesReportTableModel, SalesReportProxyModel, constants, SalesDetailsSaveWorker
from widgets import utils as _utils
from models import constants as _constants
from _widgets import common
from pdf_templates import invoiceTemplate

from reportlab.lib.pagesizes import letter as _letter
from reportlab.pdfgen.canvas import Canvas as _Canvas


class SalesReport(_QtGui.QWidget):
    '''
    UI for Sales Report widget
    '''
    def __init__(self, type='sales', parent=None):
        super(SalesReport, self).__init__(parent)
        self._manager = SalesManager(type)
        self._type = type
        self.__salesReportUI = Ui_salesReport()
        self.__setupWidget()
        self.__connectWidget()
        self.__setSalesInformation()

    def __setupWidget(self):
        '''
        Sets all quotation req widgets
        '''
        self.__salesReportUI.setupUi(self)

        self.__salesModelData = SalesReportTableModel()
        self.__salesProxyModel = SalesReportProxyModel()
        self.__salesProxyModel.setSourceModel(self.__salesModelData)
        self.__salesProxyModel.setDynamicSortFilter(True)
        self.__salesProxyModel.setFilterCaseSensitivity(_QtCore.Qt.CaseInsensitive)
        self.__salesReportUI.salesReportTable.setModel(self.__salesProxyModel)

        self.__salesReportUI.fromDateValue.setDate(_QtCore.QDate.currentDate())
        self.__salesReportUI.toDateValue.setDate(_QtCore.QDate.currentDate())

        self.showMaximized()

    def __connectWidget(self):
        '''
        Connect all widget signal and slots
        '''
        self.__salesReportUI.resetButton.clicked.connect(self.__discardChanges)
        self.__salesReportUI.searchButton.clicked.connect(self.__searchChanges)
        self.__salesReportUI.saveButton.clicked.connect(self.__saveTableChanges)
        self.__salesReportUI.salesReportTable.removeEntry.connect(self.__removeFromDatabase)
        self.__salesReportUI.removeButton.clicked.connect(self.__salesReportUI.salesReportTable.removeSlot)
        self.__salesReportUI.clearButton.clicked.connect(self.__salesReportUI.salesReportTable.clearSlot)

    def __removeFromDatabase(self, row='all'):
        '''
        Removes entry from database
        '''
        if row != 'all':
            salesInfoEntry = self._manager.getSalesInfo(self.__salesProxyModel.index(row, 2).data())
            # salesInfoEntry.delete()
            if not salesInfoEntry.cancelReason:
                self.updateAmountValue(row)
            return
        import inspect
        print inspect.stack()[1]
        self._manager.deleteSalesInfo()
        self.__salesReportUI.amountValue.setText('')
        self.__salesReportUI.taxValue.setText('')
        self.__salesReportUI.totalValue.setText('')
        self.__salesReportUI.amountPaidValue.setText('')
        self.__salesReportUI.amountPaidValue.setText('')
        self.__salesReportUI.balanceValue.setText('')

    def updateAmountValue(self, cancelRow=None):
        '''
        Received when model data is removed
        '''
        amount = tax = total = amountPaid = balance = 0
        # print self.__purchaseProxyModel.rowCount()
        for row in range(self.__salesProxyModel.rowCount()):
            print row, cancelRow
            if row == cancelRow:
                continue
            if self.__salesProxyModel.index(row, 14).data():
                continue
            amount += float(self.__salesProxyModel.index(row, 7).data())
            tax += float(self.__salesProxyModel.index(row, 8).data())
            total += float(self.__salesProxyModel.index(row, 9).data())
            amountPaid += float(self.__salesProxyModel.index(row, 10).data())
            balance += float(self.__salesProxyModel.index(row, 11).data())
        self.__salesReportUI.amountValue.setText(str(amount))
        self.__salesReportUI.totalValue.setText(str(total))
        self.__salesReportUI.taxValue.setText(str(tax))
        self.__salesReportUI.amountPaidValue.setText(str(amountPaid))
        self.__salesReportUI.balanceValue.setText(str(balance))

    def __setSalesInformation(self):
        '''
        Sets all purchase order information from db
        '''
        salesData = self._manager.fetchAllSalesInfo()

        amount = tax = total = amountPaid = balance = 0
        for info in salesData:
            self.__salesModelData.addSalesReportInfo(
                str(info.customerName),
                str(info.customerAddress),
                str(info.customerGstin),
                str(info.customerStateCode),
                str(info.billNo),
                str(info.paidBy),
                str(info.billDate),
                str(info.poNo),
                str(info.poDate),
                str(info.dcCode),
                str(info.dcDate),
                str(info.vehicleNo),
                str(info.dispatchedThrough),
                str(info.vendorCode),
                str(info.paymentTerms),
                str(info.amount),
                str(info.total),
                str(info.amountPaid),
                str(info.total-info.amountPaid),
                str(info.remarks),
                'True',
                info.cancelReason
            )
            amount += float(info.amount)
            total += float(info.total)
            amountPaid += float(info.amountPaid)
        self.__salesReportUI.amountValue.setText(str(amount))
        self.__salesReportUI.totalValue.setText(str(total))
        self.__salesReportUI.taxValue.setText(str(total - amount))
        self.__salesReportUI.amountPaidValue.setText(str(amountPaid))
        self.__salesReportUI.balanceValue.setText(str(total - amountPaid))

    _utils.showWaitCursor
    def __saveTableChanges(self):
        '''
        Save Table change to database
        '''
        salesWorker = SalesDetailsSaveWorker(self.__quotationModelData.tableData, self._manager)
        salesWorker.start()
        _QtGui.QMessageBox.information(self, 'Saved', 'Sales Information Saved Successfully.',
                                       buttons=_QtGui.QMessageBox.Ok)

    def __validateSearchDate(self):
        '''
        Validates search from and to date
        '''
        if self.__salesReportUI.fromDateValue.date() > self.__salesReportUI.toDateValue.date():
            _QtGui.QMessageBox.critical(self, 'Error', 'From Date is Greater than To Date', buttons=_QtGui.QMessageBox.Ok)
            return False
        return True

    _utils.showWaitCursor
    def __searchChanges(self):
        '''
        Validates input and save changes in database and updates table.
        '''
        if not self.__validateSearchDate():
            return

        customerName = str(self.__salesReportUI.customerSearchValue.text())
        quotationNo = str(self.__salesReportUI.billSearchValue.text())
        fromDate = self.__salesReportUI.fromDateValue.date()
        toDate = self.__salesReportUI.toDateValue.date()

        self.__salesProxyModel.setFilterByColumn(
            _QtCore.QRegExp(quotationNo, _QtCore.Qt.CaseSensitive, _QtCore.QRegExp.FixedString),2)
        self.__salesProxyModel.setFilterByColumn(
            _QtCore.QRegExp(customerName, _QtCore.Qt.CaseSensitive, _QtCore.QRegExp.FixedString), 0)
        self.__salesProxyModel.setFilterByColumn(
            constants.dateFilter(fromDate.toString('dd - MMM - yyyy'), toDate.toString('dd - MMM - yyyy')), 4)
        self.updateAmountValue()

    _utils.showWaitCursor
    def __discardChanges(self):
        self.__salesReportUI.customerSearchValue.setText('')
        self.__salesReportUI.billSearchValue.setText('')
        self.__salesReportUI.fromDateValue.setDate(_QtCore.QDate.currentDate())
        self.__salesReportUI.toDateValue.setDate(_QtCore.QDate.currentDate())
        self.__salesReportUI.salesReportTable.clear()
        self.__salesReportUI.amountValue.setText('')
        self.__salesReportUI.taxValue.setText('')
        self.__salesReportUI.totalValue.setText('')
        self.__salesReportUI.amountPaidValue.setText('')
        self.__salesReportUI.balanceValue.setText('')

    def viewItems(self, billNo):
        salesProduct = self._manager.getSalesItemInfo(billNo)

        itemInfoWidget = common.itemInfoWidget.ItemInfoWidget(billNo, salesProduct, _constants._quotationSettings, parent=self)
        itemInfoWidget.show()

    def addItemInfo(self, itemInfo):
        return ItemDetails(itemInfo)

    def cancelBill(self, billNo, cancelReason):
        billDetails = self._manager.getSalesInfo(billNo)
        billDetails.cancelReason = cancelReason
        salesTableData = [data for data in self.__salesModelData.tableData if data.billNo.value == billNo]
        salesTableData[0].cancelReason = _constants.valueWrapper(cancelReason, False)
        billDetails.save()

        self.updateAmountValue()

    def createPDF(self, billNo):
        try:
            billDirectory = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(__file__))),
                                          self._type, billNo)
            _os.makedirs(billDirectory)
        except:
            pass
        today = _datetime.datetime.today().strftime('%Y_%m_%d-%H_%M_%S')
        canvas = _Canvas(
            _os.path.join(billDirectory, '{0}.pdf'.format(today)),
            pagesize=_letter)
        invoiceTemplate.InvoiceTemplate(canvas, self.__getSalesDetails(billNo), 'Original')
        canvas.save()
        _QtGui.QMessageBox.information(self, 'Saved', 'Sales Information PDF created.',
                                       buttons=_QtGui.QMessageBox.Ok)

    def __getSalesDetails(self, billNo):
        salesDetails = self._manager.getSalesInfo(billNo)
        salesItem = self._manager.getSalesItemInfo(billNo)
        itemCodes = []
        particulars = []
        hsnCode = []
        quantity = []
        rate = []
        amounts = []
        total = 0
        cgst, sgst, igst = '', '', ''
        cgstValue, sgstValue, igstValue = 0, 0, 0
        for item in salesItem:
            itemCodes.append(item.itemCode)
            particulars.append(item.particular)
            hsnCode.append(item.hsnCode)
            quantity.append(item.quantity)
            rate.append(item.rate)
            if not cgst:
                cgst = item.cgst
            if not sgst:
                sgst = item.sgst
            if not igst:
                igst = item.igst
            amount = (float(item.quantity) * float(item.rate))
            amounts.append(amount)
            cgstValue += amount + (amount * (int(item.cgst)/100))
            sgstValue += amount + (amount * (int(item.sgst)/100))
            igstValue += amount + (amount * (int(item.igst)/100))

        amountBeforeRs, amountBeforePs = '{: 0.2f}'.format(salesDetails.amount).split('.')
        amountAfterRs, amountAfterPs = '{: 0.2f}'.format(salesDetails.total).split('.')
        cgstRs, cgstPs = '{: 0.2f}'.format(float(cgstValue)).split('.')
        sgstRs, sgstPs = '{: 0.2f}'.format(float(sgstValue)).split('.')
        igstRs, igstPs = '{: 0.2f}'.format(float(igstValue)).split('.')

        convertor = _utils.Number2Words()
        amountWord = convertor.convertNumberToWords(salesDetails.total) + ' Only'
        amountWords = amountWord.split(' ')
        if len(amountWords) > 7:
            amountWords = ' '.join(amountWords[: 7]) + ' '.join(amountWords[7:])
        else:
            amountWords = [' '.join(amountWords)]

        billInfo = {
            'customerName': salesDetails.customerName,
            'customerAddress': salesDetails.customerAddress,
            'gstin': salesDetails.customerGstin,
            'stateCode': str(salesDetails.customerStateCode),
            'billNo': billNo,
            'billDate': salesDetails.billDate.strftime('%d-%b-%y'),
            'poNo': salesDetails.poNo,
            'poDate': salesDetails.poDate,
            'vendorCode': salesDetails.vendorCode,
            'paymentTerms': salesDetails.paymentTerms,
            'dcNo': salesDetails.dcCode,
            'dcDate': salesDetails.dcDate,
            'vehicleNo': salesDetails.vehicleNo,
            'dispatchedThrough': salesDetails.dispatchedThrough,
            'amountWithoutTaxRs': amountBeforeRs,
            'amountWithoutTaxPs': amountBeforePs,
            'cgst': '{}%'.format(cgst),
            'cgstRs': cgstRs,
            'cgstPs': cgstPs,
            'sgst': '{}%'.format(sgst),
            'sgstRs': sgstRs,
            'sgstPs': sgstPs,
            'igst': '{}%'.format(igst),
            'igstRs': igstRs,
            'igstPs': igstPs,
            'taxPs': '**',
            'amountWithTaxRs': amountAfterRs,
            'amountWithTaxPs': amountAfterPs,
            'amountWord': amountWords,

            'itemCodes': itemCodes,
            'particulars': particulars,
            'hsnCodes': hsnCode,
            'quantities': quantity,
            'rates': rate,
            'amounts': amounts,
            'fileName': billNo
        }

        return billInfo



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