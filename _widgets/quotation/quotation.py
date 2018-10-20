import tempfile
import shutil
import os as _os
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore,
    QtWebKit as _QtWebKit
)

from _widgets.dialogs.customerDialog import CustomerDialog

from ui.quotationUI import Ui_quotation
from database import CompanyItems, QuotationManager, CustomerManager, CompanyItemManager
from widgets import utils as _utils
from pdf_templates.quotationTemplate import QuotationTemplate

from reportlab.lib.pagesizes import letter as _letter
from reportlab.pdfgen.canvas import Canvas as _Canvas

class QuotationWidget(_QtGui.QWidget):
    '''
    Creates Quotation UI.
    '''

    def __init__(self, parent=None):
        super(QuotationWidget, self).__init__(parent)
        self.__manager = QuotationManager()
        self.__customerManager = CustomerManager()
        self.__companyManager = CompanyItemManager('sales')
        self.__quotationUI = Ui_quotation()
        self.__setVariables()
        self.__setUpWidget()
        self.__setDBVariables()
        self.__connectWidgets()

    def __setDBVariables(self):
        '''
        Sets variables required for widgets
        '''
        self.__quotationNo = self.__getQuotationNo()
        self.__customerInfo = {customerInfo.custName: customerInfo.custAddress for customerInfo in
                               self.__customerManager.fetchAllCustomerInfo()}
        self.__purchaseItemInfo = (item.itemCode for item in self.__companyManager.fetchAllCompanyItemInfo())

    def __setVariables(self):
        self.__itemCodes = []
        self.__particulars = []
        self.__hsnCode = []
        self.__quantity = []
        self.__rate = []
        self.__amount = []
        self.__cgstItemValue = []
        self.__sgstItemValue = []
        self.__igstItemValue = []
        self.__cgst = ''
        self.__sgst = ''
        self.__igst = '' 
        self.__cgstValue = 0
        self.__sgstValue = 0
        self.__igstValue = 0


    def __getQuotationNo(self):
        id = 1
        try:
            id = self.__manager.getOrderedQuotationNoInfo()
            id = int(id) + 1
        except:
            pass
        return id

    def __setUpWidget(self):
        '''
        Sets UI for widgets
        '''
        self.__quotationUI.setupUi(self)

        self.__quotationUI.quotationNoValue.setText(str(self.__getQuotationNo()))
        self.__quotationUI.quotationDateValue.setDate(_QtCore.QDate.currentDate())
        self.__quotationUI.validUntilValue.setDate(_QtCore.QDate.currentDate())
        self.__quotationUI.quotationTable.setTableItems(CompanyItems)

        self.showMaximized()

    def __connectWidgets(self):
        '''
        Connect all the widgets 
        '''
        self.__quotationUI.customerNameValue.textChanged.connect(self.__updateFromCustomerName)
        self.__quotationUI.customerAddressValue.textChanged.connect(self.__updateFromCustomerAddress)
        self.__quotationUI.previewButton.clicked.connect(self.__handlePreview)
        self.__quotationUI.saveButton.clicked.connect(self.__saveToPdf)
        self.__quotationUI.discardButton.clicked.connect(self.__discardChanges)

        self.__quotationUI.quotationTable.cellChanged.connect(self.__computeAmount)
        self.__quotationUI.quotationTable.taxUpdate.connect(self.update_all)

        self.__quotationUI.addButton.clicked.connect(self.__quotationUI.quotationTable.addRow)
        self.__quotationUI.removeButton.clicked.connect(self.__quotationUI.quotationTable.removeSlot)
        self.__quotationUI.clearButton.clicked.connect(self.__quotationUI.quotationTable.clearSlot)
        self.__quotationUI.importButton.clicked.connect(self.__quotationUI.quotationTable.importItems)

        _utils.setCompleter(self.__quotationUI.customerNameValue, self.__customerInfo.keys())
        _utils.setCompleter(self.__quotationUI.customerAddressValue, self.__customerInfo.values())

    def __computeAmountValues(self, row):
        '''
        Calculates amount, tax and others based on cgst, sgst and igst.
        '''
        qty = _utils.getIntegralPart(self.__quotationUI.quotationTable.item(row, 3).text())
        rate = self.__quotationUI.quotationTable.item(row, 4).text()
        if not qty or not rate:
            self.populateAmountWidget()
            return
        cgst = 0
        if self.__quotationUI.quotationTable.cellWidget(row, 5).currentText():
            cgst = float(self.__quotationUI.quotationTable.cellWidget(row, 5).currentText())
        sgst = 0
        if self.__quotationUI.quotationTable.cellWidget(row, 6).currentText():
            sgst = float(self.__quotationUI.quotationTable.cellWidget(row, 6).currentText())
        igst = 0
        if self.__quotationUI.quotationTable.cellWidget(row, 7).currentText():
            igst = float(self.__quotationUI.quotationTable.cellWidget(row, 7).currentText())
        try:
            float(qty)
        except:
            _QtGui.QMessageBox.critical(self, 'Error',
                                    'Quantity is incorrect.Enter space between quantity or enter only numbers',
                                    buttons=_QtGui.QMessageBox.Ok)
            return
        try:
            float(rate)
        except:
            _QtGui.QMessageBox.critical(self, 'Error', 'Rate is incorrect.Enter only numbers', buttons=_QtGui.QMessageBox.Ok)
            return
        amountWithoutTax = float(qty) * float(rate)
        self.__quotationUI.quotationTable.setItem(row, 8, self.__quotationUI.quotationTable.getReadOnlyItem(
            str(amountWithoutTax)))
        taxValue = (amountWithoutTax * cgst) / 100.0 + (amountWithoutTax * sgst) / 100.0 + (
                amountWithoutTax * igst) / 100.0
        self.__quotationUI.quotationTable.setItem(row, 9, self.__quotationUI.quotationTable.getReadOnlyItem(str(taxValue)))
        self.__quotationUI.quotationTable.setItem(row, 10, self.__quotationUI.quotationTable.getReadOnlyItem(str(taxValue + amountWithoutTax)))

        self.populateAmountWidget()

    def populateAmountWidget(self):
        '''
        Populates amount widget with values
        '''
        without_tax = 0
        with_tax = 0
        for i in range(self.__quotationUI.quotationTable.rowCount()):
            without_tax_text = self.__quotationUI.quotationTable.item(i, 8).text()
            tax_text = self.__quotationUI.quotationTable.item(i, 10).text()
            if without_tax_text and tax_text:
                without_tax += float(without_tax_text)
                with_tax += float(tax_text)
        self.__quotationUI.beforeTaxValue.setText(str(without_tax))
        self.__quotationUI.afterTaxValue.setText(str(round(with_tax)))
        self.__quotationUI.taxValue.setText(str(round(with_tax) - without_tax))

        convertor = _utils.Number2Words()
        amount_word = convertor.convertNumberToWords(float(self.__quotationUI.afterTaxValue.text()))
        self.__quotationUI.amountWordsValue.setText(amount_word + ' only')

    def update_all(self):
        for i in range(self.__quotationUI.quotationTable.rowCount()):
            qty = 0
            if self.__quotationUI.quotationTable.item(i, 3):
                qty = self.__quotationUI.quotationTable.item(i, 3).text().split(' ')[0]
                qty = _utils.getIntegralPart(qty)
            rate = 0
            if self.__quotationUI.quotationTable.item(i, 4):
                rate = self.__quotationUI.quotationTable.item(i, 4).text()
            if not qty:
                return
            if not rate:
                return
            try:
                float(qty)
            except:
                _QtGui.QMessageBox.critical(self, 'Error', 'Quantity is incorrect add space or enter proper value',
                                     buttons=_QtGui.QMessageBox.Ok)
                return
            try:
                float(rate)
            except:
                _QtGui.QMessageBox.critical(self, 'Error', 'Rate is incorrect enter proper value', buttons=_QtGui.QMessageBox.Ok)
                return
            cgst = 0
            if self.__quotationUI.quotationTable.cellWidget(i, 5).currentText():
                cgst = float(self.__quotationUI.quotationTable.cellWidget(i, 5).currentText())
            sgst = 0
            if self.__quotationUI.quotationTable.cellWidget(i, 6).currentText():
                sgst = float(self.__quotationUI.quotationTable.cellWidget(i, 6).currentText())
            igst = 0
            if self.__quotationUI.quotationTable.cellWidget(i, 7).currentText():
                igst = float(self.__quotationUI.quotationTable.cellWidget(i, 7).currentText())
            amountWithoutTax = float(qty) * float(rate)
            self.__quotationUI.quotationTable.setItem(i, 8, self.__quotationUI.quotationTable.getReadOnlyItem(str(amountWithoutTax)))
            tax_value = (amountWithoutTax * cgst) / 100 + (amountWithoutTax * sgst) / 100 + (
                    amountWithoutTax * igst) / 100
            self.__quotationUI.quotationTable.setItem(i, 9, self.__quotationUI.quotationTable.getReadOnlyItem(str(tax_value)))
            self.__quotationUI.quotationTable.setItem(i, 10, self.__quotationUI.quotationTable.getReadOnlyItem(str(tax_value + amountWithoutTax)))
            self.populateAmountWidget()

    def __computeAmount(self, row, col):
        if col == 3:
            if self.__quotationUI.quotationTable.item(row, col + 1):
                self.__computeAmountValues(row)
        elif col == 4:
            if self.__quotationUI.quotationTable.item(row, col - 1):
                self.__computeAmountValues(row)

    def __updateFromCustomerName(self):
        customerAddress = self.__customerInfo.get(
            self.__quotationUI.customerNameValue.text(),
            None)
        if customerAddress:
            self.__quotationUI.customerAddressValue.setText(customerAddress)

    def __updateFromCustomerAddress(self):
        customerInfo = {v: k for k, v in self.__customerInfo.iteritems()}
        customerName = customerInfo.get(
            self.__quotationUI.customerAddressValue.text(),
            None)
        if customerName:
            self.__quotationUI.customerNameValue.setText(customerName)


    def __validateInputs(self):
        if not self.__quotationUI.customerNameValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Name must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self.__quotationUI.customerAddressValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Address must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if self.__quotationUI.quotationDateValue.date() > self.__quotationUI.validUntilValue.date():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Quotation Date is Greater than Valid Until Date', buttons=_QtGui.QMessageBox.Ok)
            return False


        particulars, quantities, rates, hsn_codes, amounts = [], [], [], [], []
        item_codes, cgst, sgst, igst = [], [], [], []
        for i in range(self.__quotationUI.quotationTable.rowCount()):
            item_code = self.__quotationUI.quotationTable.cellWidget(i, 0)
            if item_code and item_code.text():
                item_codes.append(item_code.text())
            particular = self.__quotationUI.quotationTable.item(i, 1)
            if particular and particular.text():
                particulars.append(str(particular.text()))
            hsn_code = self.__quotationUI.quotationTable.item(i, 2)
            if hsn_code and hsn_code.text():
                hsn_codes.append(str(hsn_code.text()))
            quantity = self.__quotationUI.quotationTable.item(i, 3)
            if (quantity and quantity.text()):
                quantities.append(str(quantity.text()))
            rate = self.__quotationUI.quotationTable.item(i, 4)
            if (rate and rate.text()):
                rates.append(str(rate.text()))
            amount = self.__quotationUI.quotationTable.item(i, 8)
            if (amount and amount.text()):
                amounts.append(str(amount.text()))
                cgst.append(self.__quotationUI.quotationTable.cellWidget(i, 5).currentText())
                sgst.append(self.__quotationUI.quotationTable.cellWidget(i, 6).currentText())
                igst.append(self.__quotationUI.quotationTable.cellWidget(i, 7).currentText())

        max_table_items = max([len(item_codes), len(particulars), len(hsn_codes), len(quantities), len(rates)])
        for i in rates:
            try:
                float(i)
            except:
                _QtGui.QMessageBox.critical(self, 'Rate must be Numbers')
                return False
        if len(item_codes) != max_table_items:
            _QtGui.QMessageBox.critical(self, 'All Item Codes column must be entered')
            return False
        if len(particulars) != max_table_items:
            _QtGui.QMessageBox.critical(self, 'All Particulars column must be entered')
            return False
        if len(hsn_codes) != max_table_items:
            _QtGui.QMessageBox.critical(self, 'All HSN Code column must be entered')
            return False
        if len(quantities) != max_table_items:
            _QtGui.QMessageBox.critical(self, 'All Quantity column must be entered')
            return False
        if len(rates) != max_table_items:
            _QtGui.QMessageBox.critical(self, 'All Rate column must be entered')
            return False

        amount = 0
        for i, itemCode in enumerate(item_codes):
            amount += float(quantities[i]) * float(rates[i])
            if itemCode in self.__purchaseItemInfo:
                continue
            self.__companyManager.saveCompanyItemInfo(
                itemCode,
                particulars[i],
                hsn_codes[i],
                quantities[i],
                float(rates[i])
            )
        self.__itemCodes = item_codes
        self.__particulars = particulars
        self.__hsnCode = hsn_codes
        self.__quantity = quantities
        self.__rate = rates
        self.__amount = amounts
        self.__allCgst = cgst
        self.__allSgst = sgst
        self.__allIgst = igst

        self.__cgst = self.__quotationUI.quotationTable.cellWidget(0, 5).currentText()
        self.__sgst = self.__quotationUI.quotationTable.cellWidget(0, 6).currentText()
        self.__igst = self.__quotationUI.quotationTable.cellWidget(0, 7).currentText()

        self.__cgstValue = (sum(map(float, self.__amount)) * float(self.__cgst)) / 100
        self.__sgstValue = (sum(map(float, self.__amount)) * float(self.__sgst)) / 100
        self.__igstValue = (sum(map(float, self.__amount)) * float(self.__igst)) / 100

        return True

    def __handlePreview(self):
        if self.__quotationUI.customerNameValue.text().strip() and  self.__quotationUI.customerNameValue.text() not in self.__customerInfo:
            dialog = CustomerDialog(self.__quotationUI.customerNameValue.text(), self.__quotationUI.customerAddressValue.text())
            dialog.exec_()
        if not self.__validateInputs():
            return
        quotationDetails = self.__getQuotationDetails()

        quotationDirectory = tempfile.mkdtemp()
        pdfPath = _os.path.join(quotationDirectory, '{0}.pdf'.format(self.__quotationUI.quotationNoValue.text()))
        canvas = _Canvas(
            pdfPath,
            pagesize=_letter)
        QuotationTemplate(canvas, quotationDetails)
        canvas.save()
        dialog = _utils.PreviewDialog(self, pdfPath)
        dialog.exec_()
        shutil.rmtree(quotationDirectory)

    @_utils.showWaitCursor
    def __saveToPdf(self):
        if self.__quotationUI.customerNameValue.text() not in self.__customerInfo:
            dialog = CustomerDialog(self.__quotationUI.customerNameValue.text(), self.__quotationUI.customerAddressValue.text())
            dialog.exec_()
        if not self.__validateInputs():
            return

        self.__manager.saveQuotationInfo(
            self.__quotationUI.customerNameValue.text(),
            self.__quotationUI.customerAddressValue.text(),
            int(self.__quotationUI.quotationNoValue.text()),
            self.__quotationUI.validUntilValue.date().toPython(),
            self.__quotationUI.quotationDateValue.date().toPython(),
            float(self.__quotationUI.beforeTaxValue.text()),
            float(self.__quotationUI.afterTaxValue.text()),
            self.__quotationUI.remarksValue.toPlainText())

        for (itemCode, particular, hsnCode, quantity, rate, cgst, sgst, igst) in zip(self.__itemCodes, self.__particulars, self.__hsnCode, self.__quantity, self.__rate, self.__allCgst, self.__allSgst, self.__allIgst):
            self.__manager.saveQuotationItemInfo(
                self.__quotationUI.quotationNoValue.text(),
                itemCode,
                particular,
                hsnCode,
                quantity,
                float(rate),
                float(cgst),
                float(sgst),
                float(igst))
        try:
            quotationDirectory = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(__file__))),
                          'quotation', self.__quotationUI.quotationNoValue.text())
            _os.makedirs(quotationDirectory)
        except:
            return _QtGui.QMessageBox.critical(self, 'ERROR', 'Bill No is already generated.', buttons=_QtGui.QMessageBox.Ok)

        quotationDetails = self.__getQuotationDetails()
        canvas = _Canvas(_os.path.join(quotationDirectory, '{0}.pdf'.format(self.__quotationUI.quotationNoValue.text())), pagesize=_letter)
        print quotationDetails
        QuotationTemplate(canvas, quotationDetails)
        canvas.save()

        if self.__quotationUI.printCheckBox.isChecked():
            self.handlePrint()
        self.__discardChanges()
        self.__quotationNo += 1
        self.__quotationUI.quotationNoValue.setText(str(self.__quotationNo))

    def handlePrint(self):
        dialog = _QtGui.QPrintDialog()
        if dialog.exec_() == _QtGui.QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    @_utils.showWaitCursor
    def __discardChanges(self):
        self.__quotationUI.customerNameValue.setText('')
        self.__quotationUI.customerAddressValue.setText('')
        self.__quotationUI.quotationDateValue.setDate(_QtCore.QDate.currentDate())
        self.__quotationUI.validUntilValue.setDate(_QtCore.QDate.currentDate())
        self.__quotationUI.quotationTable.clear()
        self.__quotationUI.beforeTaxValue.setText('')
        self.__quotationUI.afterTaxValue.setText('')
        self.__quotationUI.taxValue.setText('')
        self.__quotationUI.remarksValue.setText('')
        self.__quotationUI.amountWordsValue.setText('')
        self.__setVariables()
        self.__quotationUI.quotationTable.setTableItems(CompanyItems)

    def __getQuotationDetails(self):
        amountBeforeRs, amountBeforePs = '{: 0.2f}'.format(float(self.__quotationUI.beforeTaxValue.text())).split('.')
        amountAfterRs, amountAfterPs = '{: 0.2f}'.format(float(self.__quotationUI.afterTaxValue.text())).split('.')
        cgstRs, cgstPs = '{: 0.2f}'.format(float(self.__cgstValue)).split('.')
        sgstRs, sgstPs = '{: 0.2f}'.format(float(self.__sgstValue)).split('.')
        igstRs, igstPs = '{: 0.2f}'.format(float(self.__igstValue)).split('.')
        amountWords = self.__quotationUI.amountWordsValue.toPlainText().split(' ')
        if len(amountWords) > 7:
            amountWords = ' '.join(amountWords[: 7]) + ' '.join(amountWords[7:])
        else:
            amountWords = [' '.join(amountWords)]
        print amountWords
        # for quotationInfo in self.__quotationModelData.tableData:

        billInfo = {
            'customerName': self.__quotationUI.customerNameValue.text(),
            'customerAddress': self.__quotationUI.customerAddressValue.text(),
            'billNo': self.__quotationUI.quotationNoValue.text(),
            'quotationDate': self.__quotationUI.quotationDateValue.date().toPython().strftime('%d-%b-%y'),
            'validDate': self.__quotationUI.validUntilValue.date().toPython().strftime('%d-%b-%y'),

            'amountBeforeRs': amountBeforeRs,
            'amountBeforePs': amountBeforePs,
            'cgst': '{}%'.format(self.__cgst),
            'cgstRs': cgstRs,
            'cgstPs': cgstPs,
            'sgst': '{}%'.format(self.__sgst),
            'sgstRs': sgstRs,
            'sgstPs': sgstPs,
            'igst': '{}%'.format(self.__igst),
            'igstRs': igstRs,
            'igstPs': igstPs,
            'origTaxPs':'',
            'afterTaxRs' : amountAfterRs,
            'afterTaxPs': amountAfterPs,
            'amountWord': amountWords,

            'particulars': self.__particulars,
            'hsnCodes': self.__hsnCode,
            'quantities': self.__quantity,
            'rates': self.__rate,
            'amounts': self.__amount
        }
        return billInfo
