
import os as _os
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)

from _widgets.dialogs.customerDialog import CustomerDialog
from ui.purchaseInvoiceUI import Ui_PurchaseInvoice
from database import CompanyItems, PurchaseManager, CustomerManager, CompanyItemManager
from widgets import utils as _utils
from _widgets import utils

class PurchaseInvoiceWidget(_QtGui.QWidget):
    '''
    Creates Purchase invoice UI.
    '''
    settings = _QtCore.QSettings("purchase.ini", _QtCore.QSettings.IniFormat)
    def __init__(self, parent=None):
        super(PurchaseInvoiceWidget, self).__init__(parent)

        self.__purchaseInvoiceUI = Ui_PurchaseInvoice()
        self.__manager = PurchaseManager()
        self.__customerManager = CustomerManager()
        self.__companyItemManager = CompanyItemManager('purchase')
        self.__setVariables()
        self.__setUpWidget()
        self.__connectWidgets()
        self.__saveRestore = utils.StoreRestore(self.settings)

    def __setVariables(self):
        '''
        Sets variables required for widgets
        '''
        self.__particulars = []
        self.__hsnCode = []
        self.__quantity = []
        self.__rate = []
        self.__amount = []
        self.__cgst = ''
        self.__sgst = ''
        self.__igst = ''
        self.__cgstValue = 0
        self.__sgstValue = 0
        self.__igstValue = 0
        self.__customerInfo = {customerInfo.custName : [customerInfo.custAddress,
                                                        customerInfo.gstin,
                                                        customerInfo.stateCode] for customerInfo in self.__customerManager.fetchAllCustomerInfo()}
        print [item.itemCode for item in self.__companyItemManager.fetchAllCompanyItemInfo()]
        self.__purchaseItemInfo = (item.itemCode for item in self.__companyItemManager.fetchAllCompanyItemInfo())

    def __getPurcahseNo(self):
        id = 1
        try:
            id = self.__manager.getOrderedPurchaseNoInfo().billNo
            id = int(id) + 1
        except Exception as ex:
            print ex.message
            pass
        return id

    def __setUpWidget(self):
        '''
        Sets UI for widgets
        '''
        self.__purchaseInvoiceUI.setupUi(self)

        self.__purchaseInvoiceUI.billNoValue.setText(str(self.__getPurcahseNo()))

        self.__purchaseInvoiceUI.billDateValue.setDate(_QtCore.QDate.currentDate())
        self.__purchaseInvoiceUI.dueDateValue.setDate(_QtCore.QDate.currentDate())

        self.__purchaseInvoiceUI.purchaseTable.setTableItems(CompanyItems)

        paymentTypes = ('Cash', 'Cheque', 'online')
        self.__purchaseInvoiceUI.paymentValue.addItems(paymentTypes)

        self.showMaximized()

    def __connectWidgets(self):
        '''
        Connect all the widgets 
        '''
        self.__purchaseInvoiceUI.customerNameValue.textChanged.connect(self.__updateFromCustomerName)
        self.__purchaseInvoiceUI.customerAddressValue.textChanged.connect(self.__updateFromCustomerAddress)
        self.__purchaseInvoiceUI.saveButton.clicked.connect(self.__saveToPdf)
        self.__purchaseInvoiceUI.discardButton.clicked.connect(self.__discardChanges)

        self.__purchaseInvoiceUI.purchaseTable.cellChanged.connect(self.__computeAmount)
        self.__purchaseInvoiceUI.purchaseTable.taxUpdate.connect(self.update_all)

        self.__purchaseInvoiceUI.addButton.clicked.connect(self.__purchaseInvoiceUI.purchaseTable.addRow)
        self.__purchaseInvoiceUI.removeButton.clicked.connect(self.removeSlot)
        self.__purchaseInvoiceUI.clearButton.clicked.connect(self.clearSlot)
        self.__purchaseInvoiceUI.importButton.clicked.connect(self.__purchaseInvoiceUI.purchaseTable.importItems)

        saveShortcut = _QtGui.QShortcut(_QtGui.QKeySequence("Ctrl+S"), self)
        saveShortcut.activated.connect(self.saveSlot)
        restoreShortcut = _QtGui.QShortcut(_QtGui.QKeySequence("Ctrl+R"), self)
        restoreShortcut.activated.connect(self.restoreSlot)

        _utils.setCompleter(self.__purchaseInvoiceUI.customerNameValue, self.__customerInfo.keys())
        if self.__customerInfo:
            _utils.setCompleter(self.__purchaseInvoiceUI.customerAddressValue, zip(*self.__customerInfo.values())[0])

    def removeSlot(self):
        self.__purchaseInvoiceUI.purchaseTable.removeSlot()
        self.__populateAmountWidget()

    def clearSlot(self):
        self.__purchaseInvoiceUI.purchaseTable.clearSlot()
        self.__populateAmountWidget()

    def __computeAmountValues(self, row):
        '''
        Calculates amount, tax and others based on cgst, sgst and igst.
        '''
        qty = _utils.getIntegralPart(self.__purchaseInvoiceUI.purchaseTable.item(row, 3).text())
        rate = self.__purchaseInvoiceUI.purchaseTable.item(row, 4).text()
        if not qty or not rate:
            self.__populateAmountWidget()
            return
        cgst = 0
        if self.__purchaseInvoiceUI.purchaseTable.cellWidget(row, 5).currentText():
            cgst = float(self.__purchaseInvoiceUI.purchaseTable.cellWidget(row, 5).currentText())
        sgst = 0
        if self.__purchaseInvoiceUI.purchaseTable.cellWidget(row, 6).currentText():
            sgst = float(self.__purchaseInvoiceUI.purchaseTable.cellWidget(row, 6).currentText())
        igst = 0
        if self.__purchaseInvoiceUI.purchaseTable.cellWidget(row, 7).currentText():
            igst = float(self.__purchaseInvoiceUI.purchaseTable.cellWidget(row, 7).currentText())
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
        self.__purchaseInvoiceUI.purchaseTable.setItem(row, 8, self.__purchaseInvoiceUI.purchaseTable.getReadOnlyItem(
            str(amountWithoutTax)))
        taxValue = (amountWithoutTax * cgst) / 100.0 + (amountWithoutTax * sgst) / 100.0 + (
                amountWithoutTax * igst) / 100.0
        self.__purchaseInvoiceUI.purchaseTable.setItem(row, 9, self.__purchaseInvoiceUI.purchaseTable.getReadOnlyItem(str(taxValue)))
        self.__purchaseInvoiceUI.purchaseTable.setItem(row, 10, self.__purchaseInvoiceUI.purchaseTable.getReadOnlyItem(str(taxValue + amountWithoutTax)))

        self.__populateAmountWidget()

    def __populateAmountWidget(self):
        '''
        Populates amount widget with values
        '''
        without_tax = 0
        with_tax = 0
        for i in range(self.__purchaseInvoiceUI.purchaseTable.rowCount()):
            without_tax_text = self.__purchaseInvoiceUI.purchaseTable.item(i, 8).text()
            tax_text = self.__purchaseInvoiceUI.purchaseTable.item(i, 10).text()
            if without_tax_text and tax_text:
                without_tax += float(without_tax_text)
                with_tax += float(tax_text)
        self.__purchaseInvoiceUI.beforeTaxValue.setText(str(without_tax))
        self.__purchaseInvoiceUI.afterTaxValue.setText(str(round(with_tax)))
        self.__purchaseInvoiceUI.taxValue.setText(str(round(with_tax) - without_tax))

        convertor = _utils.Number2Words()
        amount_word = convertor.convertNumberToWords(float(self.__purchaseInvoiceUI.afterTaxValue.text()))
        self.__purchaseInvoiceUI.amountWordsValue.setText(amount_word + ' only')

    def update_all(self):
        for i in range(self.__purchaseInvoiceUI.purchaseTable.rowCount()):
            qty = 0
            if self.__purchaseInvoiceUI.purchaseTable.item(i, 3):
                qty = self.__purchaseInvoiceUI.purchaseTable.item(i, 3).text().split(' ')[0]
                qty = _utils.getIntegralPart(qty)
            rate = 0
            if self.__purchaseInvoiceUI.purchaseTable.item(i, 4):
                rate = self.__purchaseInvoiceUI.purchaseTable.item(i, 4).text()
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
            if self.__purchaseInvoiceUI.purchaseTable.cellWidget(i, 5).currentText():
                cgst = float(self.__purchaseInvoiceUI.purchaseTable.cellWidget(i, 5).currentText())
            sgst = 0
            if self.__purchaseInvoiceUI.purchaseTable.cellWidget(i, 6).currentText():
                sgst = float(self.__purchaseInvoiceUI.purchaseTable.cellWidget(i, 6).currentText())
            igst = 0
            if self.__purchaseInvoiceUI.purchaseTable.cellWidget(i, 7).currentText():
                igst = float(self.__purchaseInvoiceUI.purchaseTable.cellWidget(i, 7).currentText())
            amountWithoutTax = float(qty) * float(rate)
            self.__purchaseInvoiceUI.purchaseTable.setItem(i, 8, self.__purchaseInvoiceUI.purchaseTable.getReadOnlyItem(str(amountWithoutTax)))
            tax_value = (amountWithoutTax * cgst) / 100 + (amountWithoutTax * sgst) / 100 + (
                    amountWithoutTax * igst) / 100
            self.__purchaseInvoiceUI.purchaseTable.setItem(i, 9, self.__purchaseInvoiceUI.purchaseTable.getReadOnlyItem(str(tax_value)))
            self.__purchaseInvoiceUI.purchaseTable.setItem(i, 10, self.__purchaseInvoiceUI.purchaseTable.getReadOnlyItem(str(tax_value + amountWithoutTax)))
            self.__populateAmountWidget()

    def __computeAmount(self, row, col):
        if col == 3:
            if self.__purchaseInvoiceUI.purchaseTable.item(row, col + 1):
                self.__computeAmountValues(row)
        elif col == 4:
            if self.__purchaseInvoiceUI.purchaseTable.item(row, col - 1):
                self.__computeAmountValues(row)

    def __updateFromCustomerName(self):
        '''
        Updates customer address, gstin and statecode from customer name
        '''
        customerInfo = self.__customerInfo.get(
            self.__purchaseInvoiceUI.customerNameValue.text(), None)
        if customerInfo:
            self.__purchaseInvoiceUI.customerAddressValue.setText(customerInfo[0])
            self.__purchaseInvoiceUI.gstinValue.setText(customerInfo[1])
            self.__purchaseInvoiceUI.stateCodeValue.setText(str(customerInfo[2]))

    def __updateFromCustomerAddress(self):
        '''
        Updates customer name, gstin and statecode from customer address
        '''
        customerInfo = {v[0]: [k]+v[1:] for k, v in self.__customerInfo.iteritems()}
        customerValues = customerInfo.get(
            self.__purchaseInvoiceUI.customerAddressValue.text(),
            None)
        if customerValues:
            self.__purchaseInvoiceUI.customerNameValue.setText(customerValues[0])
            self.__purchaseInvoiceUI.gstinValue.setText(customerValues[1])
            self.__purchaseInvoiceUI.stateCodeValue.setText(str(customerValues[2]))


    def __validateInputs(self):
        '''
        Validates purchase information before saving
        '''
        if not self.__purchaseInvoiceUI.customerNameValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Name must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self.__purchaseInvoiceUI.customerAddressValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Address must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if self.__purchaseInvoiceUI.billDateValue.date() > self.__purchaseInvoiceUI.dueDateValue.date():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Quotation Date is Greater than Valid Until Date', buttons=_QtGui.QMessageBox.Ok)
            return False


        particulars, quantities, rates, hsn_codes, amounts = [], [], [], [], []
        item_codes = []
        for i in range(self.__purchaseInvoiceUI.purchaseTable.rowCount()):
            item_code = self.__purchaseInvoiceUI.purchaseTable.cellWidget(i, 0)
            if item_code and item_code.text():
                item_codes.append(item_code.text())
            particular = self.__purchaseInvoiceUI.purchaseTable.item(i, 1)
            if particular and particular.text():
                particulars.append(str(particular.text()))
            hsn_code = self.__purchaseInvoiceUI.purchaseTable.item(i, 2)
            if hsn_code and hsn_code.text():
                hsn_codes.append(str(hsn_code.text()))
            quantity = self.__purchaseInvoiceUI.purchaseTable.item(i, 3)
            if (quantity and quantity.text()):
                quantities.append(str(quantity.text()))
            rate = self.__purchaseInvoiceUI.purchaseTable.item(i, 4)
            if (rate and rate.text()):
                rates.append(str(rate.text()))
            amount = self.__purchaseInvoiceUI.purchaseTable.item(i, 8)
            if (amount and amount.text()):
                amounts.append(str(amount.text()))

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

        if not self.__purchaseInvoiceUI.amountPaidValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Amount Paid must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if float(self.__purchaseInvoiceUI.amountPaidValue.text().strip()) > float(self.__purchaseInvoiceUI.afterTaxValue.text().strip()):
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Amount Paid is greater than total value', buttons=_QtGui.QMessageBox.Ok)
            return False

        amount = 0
        for i, itemCode in enumerate(item_codes):
            amount += float(quantities[i]) * float(rates[i])
            if itemCode in self.__purchaseItemInfo:
                continue
            self.__companyItemManager.saveCompanyItemInfo(
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
        self.__amount = amount

        self.__cgst = self.__purchaseInvoiceUI.purchaseTable.cellWidget(0, 5).currentText()
        self.__sgst = self.__purchaseInvoiceUI.purchaseTable.cellWidget(0, 6).currentText()
        self.__igst = self.__purchaseInvoiceUI.purchaseTable.cellWidget(0, 7).currentText()

        self.__cgstValue = (self.__amount * float(self.__cgst)) / 100
        self.__sgstValue = (self.__amount * float(self.__sgst)) / 100
        self.__igstValue = (self.__amount * float(self.__igst)) / 100

        return True

    def __saveToPdf(self):
        '''
        Saves purchase information to database
        '''
        if self.__purchaseInvoiceUI.customerNameValue.text() not in self.__customerInfo:
            dialog = CustomerDialog(self.__purchaseInvoiceUI.customerNameValue.text(), self.__purchaseInvoiceUI.customerAddressValue.text())
            dialog.exec_()
        if not self.__validateInputs():
            return

        self.__manager.savePurchaseInfo(
            self.__purchaseInvoiceUI.customerNameValue.text(),
            self.__purchaseInvoiceUI.customerAddressValue.text(),
            self.__purchaseInvoiceUI.gstinValue.text(),
            self.__purchaseInvoiceUI.stateCodeValue.text(),
            self.__purchaseInvoiceUI.billNoValue.text(),
            self.__purchaseInvoiceUI.billDateValue.date().toPython(),
            self.__purchaseInvoiceUI.dueDateValue.date().toPython(),
            self.__purchaseInvoiceUI.paymentValue.currentText(),
            self.__purchaseInvoiceUI.afterTaxValue.text(),
            self.__purchaseInvoiceUI.taxValue.text(),
            self.__purchaseInvoiceUI.amountPaidValue.text(),
            self.__purchaseInvoiceUI.remarksValue.toPlainText()
        )

        for (itemCode, particular, hsnCode, quantity, rate) in zip(self.__itemCodes, self.__particulars, self.__hsnCode, self.__quantity,
                                                         self.__rate):
            self.__manager.savePurchaseItemInfo(
                self.__purchaseInvoiceUI.billNoValue.text(),
                itemCode,
                particular,
                hsnCode,
                quantity,
                rate,
                float(self.__cgst),
                float(self.__sgst),
                float(self.__igst)
            )

        _QtGui.QMessageBox.information(self, 'Saved', 'Entered Purchase Invoice saved successfully', buttons=_QtGui.QMessageBox.Ok)
        self.__discardChanges()

    def __discardChanges(self):
        '''
        Discards all widgets and default to empty string
        '''
        self.__purchaseInvoiceUI.customerNameValue.setText('')
        self.__purchaseInvoiceUI.customerAddressValue.setText('')
        self.__purchaseInvoiceUI.gstinValue.setText('')
        self.__purchaseInvoiceUI.stateCodeValue.setText('')
        self.__purchaseInvoiceUI.billNoValue.setText(str(self.__getPurcahseNo()))
        self.__purchaseInvoiceUI.billDateValue.setDate(_QtCore.QDate.currentDate())
        self.__purchaseInvoiceUI.dueDateValue.setDate(_QtCore.QDate.currentDate())
        self.__purchaseInvoiceUI.purchaseTable.clearSlot()
        self.__purchaseInvoiceUI.beforeTaxValue.setText('')
        self.__purchaseInvoiceUI.afterTaxValue.setText('')
        self.__purchaseInvoiceUI.taxValue.setText('')
        self.__purchaseInvoiceUI.amountPaidValue.setText('')
        self.__purchaseInvoiceUI.remarksValue.setText('')
        self.__purchaseInvoiceUI.gstinValue.setText('')
        self.__purchaseInvoiceUI.amountWordsValue.setText('')

    def __getPurchaseDetails(self):
        '''
        returns dict of all purchase details that needs to be saved
        '''
        amountBeforeRs, amountBeforePs = '{: 0.2f}'.format(float(self.__purchaseInvoiceUI.beforeTaxValue.text())).split('.')
        amountAfterRs, amountAfterPs = '{: 0.2f}'.format(float(self.__purchaseInvoiceUI.afterTaxValue.text())).split('.')
        cgstRs, cgstPs = '{: 0.2f}'.format(float('0.0')).split('.')
        sgstRs, sgstPs = '{: 0.2f}'.format(float('0.0')).split('.')
        igstRs, igstPs = '{: 0.2f}'.format(float('0.0')).split('.')
        amountWords = self.__purchaseInvoiceUI.amountWordsValue.toPlainText().split(' ')
        amountWords = amountWords[: 7] + amountWords[7: ]

        # for quotationInfo in self.__quotationModelData.tableData:

        billInfo = {
            'customerName': self.__purchaseInvoiceUI.customerNameValue.text(),
            'customerAddress': self.__purchaseInvoiceUI.customerAddressValue.text(),
            'billNo': self.__purchaseInvoiceUI.billNoValue.text(),
            'quotationDate': self.__purchaseInvoiceUI.billDateValue.date().toPython().strftime('%d-%b-%y'),
            'validDate': self.__purchaseInvoiceUI.dueDateValue.date().toPython().strftime('%d-%b-%y'),

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

    def saveSlot(self):
        self.__saveRestore.save(_QtGui.qApp.allWidgets())

    def restoreSlot(self):
        self.__saveRestore.restore()