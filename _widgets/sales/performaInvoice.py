
import os as _os
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)

from _widgets.dialogs.customerDialog import CustomerDialog
from ui.performaInvoiceUI import Ui_SalesInvoice
from database import CompanyItems, CustomerManager, CompanyItemManager, SalesManager
from widgets import utils as _utils
from pdf_templates import invoiceTemplate, deliveryChallanTemplate

from reportlab.lib.pagesizes import letter as _letter
from reportlab.pdfgen.canvas import Canvas as _Canvas


class PerformaInvoiceWidget(_QtGui.QWidget):
    '''
    Creates Quotation UI.
    '''
    settings = _QtCore.QSettings("performa.ini", _QtCore.QSettings.IniFormat)
    def __init__(self, type='performa', parent=None):
        super(PerformaInvoiceWidget, self).__init__(parent)
        self._salesInvoiceUI = Ui_SalesInvoice()
        self._manager = SalesManager(type)
        self.__customerManager = CustomerManager()
        self.__companyItemManager = CompanyItemManager('sales')

        self.__type = type
        self.__setVariables()
        self.__setUpWidget()
        self.__connectWidgets()
        self.__saveRestore = _utils.StoreRestore(self.settings)

        saveShortcut = _QtGui.QShortcut(_QtGui.QKeySequence("Ctrl+S"), self)
        saveShortcut.activated.connect(self.saveSlot)
        restoreShortcut = _QtGui.QShortcut(_QtGui.QKeySequence("Ctrl+R"), self)
        restoreShortcut.activated.connect(self.restoreSlot)

    def __setVariables(self):
        '''
        Sets variables required for widgets
        '''
        self.__itemCodes = []
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
        self.__customerInfo = {customerInfo.custName : (customerInfo.custAddress, customerInfo.gstin, customerInfo.stateCode)
                               for customerInfo in self.__customerManager.fetchAllCustomerInfo()}
        self.__purchaseItemInfo = (item.itemCode for item in self.__companyItemManager.fetchAllCompanyItemInfo())

    def __getSalesBillNo(self):
        id = 1
        try:
            id = self._manager.getOrderedSalesNoInfo().billNo
            id = int(id) + 1
        except Exception as ex:
            print ex, '@@@@@@@@@@'
            pass
        return id

    def __setUpWidget(self):
        '''
        Sets UI for widgets
        '''
        self.__billNo = self.__getSalesBillNo()
        self._salesInvoiceUI.setupUi(self)
        self._salesInvoiceUI.billNoValue.setText(str(self.__billNo))
        self._salesInvoiceUI.billNoValue.setReadOnly(False)
        self._salesInvoiceUI.billDateValue.setDate(_QtCore.QDate.currentDate())
        self._salesInvoiceUI.salesInvoiceTable.setTableItems(CompanyItems, self.__type)
        paymentTypes = ('Cash', 'Cheque', 'online')
        self._salesInvoiceUI.comboBox.addItems(paymentTypes)

        self._salesInvoiceUI.stateCodeValue.setValidator(_QtGui.QIntValidator())
        self._salesInvoiceUI.amountPaidValue.setValidator(_QtGui.QDoubleValidator())
        # self.updateAmountInformation()
        self.showMaximized()

    def __connectWidgets(self):
        '''
        Connect all the widgets 
        '''
        self._salesInvoiceUI.customerNameValue.textChanged.connect(self.__updateFromCustomerName)
        self._salesInvoiceUI.customerAddressValue.textChanged.connect(self.__updateFromCustomerAddress)
        self._salesInvoiceUI.previewButton.clicked.connect(self.__handlePreview)
        self._salesInvoiceUI.saveButton.clicked.connect(self.__saveToPdf)
        self._salesInvoiceUI.discardButton.clicked.connect(self.__discardChanges)

        self._salesInvoiceUI.salesInvoiceTable.cellChanged.connect(self.__computeAmount)
        self._salesInvoiceUI.salesInvoiceTable.taxUpdate.connect(self.update_all)

        self._salesInvoiceUI.addButton.clicked.connect(self._salesInvoiceUI.salesInvoiceTable.addRow)
        self._salesInvoiceUI.removeButton.clicked.connect(self.removeSlot)
        self._salesInvoiceUI.clearButton.clicked.connect(self.clearSlot)
        self._salesInvoiceUI.importButton.clicked.connect(self._salesInvoiceUI.salesInvoiceTable.importItems)

        # self._salesInvoiceUI.groupBox.toggled.connect(
        #     lambda: _utils.toggleGroup(self._salesInvoiceUI.groupBox))
        # self._salesInvoiceUI.groupBox_2.toggled.connect(
        #     lambda: _utils.toggleGroup(self._salesInvoiceUI.groupBox_2))
        # self._salesInvoiceUI.groupBox_3.toggled.connect(
        #     lambda: _utils.toggleGroup(self._salesInvoiceUI.groupBox_3))

        _utils.setCompleter(self._salesInvoiceUI.customerNameValue, self.__customerInfo.keys())
        if self.__customerInfo:
            _utils.setCompleter(self._salesInvoiceUI.customerAddressValue, zip(*self.__customerInfo.values())[0])

    def removeSlot(self):
        '''
        Clears selected row from table
        '''
        self._salesInvoiceUI.salesInvoiceTable.removeSlot()
        self.__populateAmountWidget()

    def clearSlot(self):
        self._salesInvoiceUI.salesInvoiceTable.clearSlot()
        self.__populateAmountWidget()

    def populateAmountWidget(self):
        '''
        Populates amount widget with values
        '''
        without_tax = 0
        with_tax = 0
        for i in range(self._salesInvoiceUI.salesInvoiceTable.rowCount()):
            without_tax_text = self._salesInvoiceUI.salesInvoiceTable.item(i, 8).text()
            tax_text = self._salesInvoiceUI.salesInvoiceTable.item(i, 9).text()
            if without_tax_text and tax_text:
                without_tax += float(without_tax_text)
                with_tax += float(tax_text)
        self._salesInvoiceUI.beforeTaxValue.setText(str(without_tax))
        self._salesInvoiceUI.afterTaxValue.setText(str(round(with_tax)))
        self._salesInvoiceUI.taxValue.setText(str(round(with_tax) - without_tax))

        convertor = _utils.Number2Words()
        amount_word = convertor.convertNumberToWords(float(self._salesInvoiceUI.afterTaxValue.text()))
        self._salesInvoiceUI.amountWordsValue.setText(amount_word + ' only')

    def __computeAmountValues(self, row):
        '''
        Calculates amount, tax and others based on cgst, sgst and igst.
        '''
        qty = _utils.getIntegralPart(self._salesInvoiceUI.salesInvoiceTable.item(row, 3).text())
        rate = self._salesInvoiceUI.salesInvoiceTable.item(row, 4).text()
        if not qty or not rate:
            self.__populateAmountWidget()
            return
        cgst = 0
        if self._salesInvoiceUI.salesInvoiceTable.cellWidget(row, 5).currentText():
            cgst = float(self._salesInvoiceUI.salesInvoiceTable.cellWidget(row, 5).currentText())
        sgst = 0
        if self._salesInvoiceUI.salesInvoiceTable.cellWidget(row, 6).currentText():
            sgst = float(self._salesInvoiceUI.salesInvoiceTable.cellWidget(row, 6).currentText())
        igst = 0
        if self._salesInvoiceUI.salesInvoiceTable.cellWidget(row, 7).currentText():
            igst = float(self._salesInvoiceUI.salesInvoiceTable.cellWidget(row, 7).currentText())
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
        self._salesInvoiceUI.salesInvoiceTable.setItem(row, 8, self._salesInvoiceUI.salesInvoiceTable.getReadOnlyItem(
            str(amountWithoutTax)))
        taxValue = (amountWithoutTax * cgst) / 100.0 + (amountWithoutTax * sgst) / 100.0 + (
                amountWithoutTax * igst) / 100.0
        self._salesInvoiceUI.salesInvoiceTable.setItem(row, 9, self._salesInvoiceUI.salesInvoiceTable.getReadOnlyItem(str(taxValue)))
        self._salesInvoiceUI.salesInvoiceTable.setItem(row, 10, self._salesInvoiceUI.salesInvoiceTable.getReadOnlyItem(str(taxValue + amountWithoutTax)))

        self.__populateAmountWidget()

    def __populateAmountWidget(self):
        '''
        Populates amount widget with values
        '''
        without_tax = 0
        with_tax = 0
        for i in range(self._salesInvoiceUI.salesInvoiceTable.rowCount()):
            without_tax_text = self._salesInvoiceUI.salesInvoiceTable.item(i, 8).text()
            tax_text = self._salesInvoiceUI.salesInvoiceTable.item(i, 10).text()
            if without_tax_text and tax_text:
                without_tax += float(without_tax_text)
                with_tax += float(tax_text)
        self._salesInvoiceUI.beforeTaxValue.setText(str(without_tax))
        self._salesInvoiceUI.afterTaxValue.setText(str(round(with_tax)))
        self._salesInvoiceUI.taxValue.setText(str(round(with_tax) - without_tax))

        convertor = _utils.Number2Words()
        amount_word = convertor.convertNumberToWords(float(self._salesInvoiceUI.afterTaxValue.text()))
        self._salesInvoiceUI.amountWordsValue.setText(amount_word + ' only')

    def update_all(self):
        for i in range(self._salesInvoiceUI.salesInvoiceTable.rowCount()):
            qty = 0
            if self._salesInvoiceUI.salesInvoiceTable.item(i, 3):
                qty = self._salesInvoiceUI.salesInvoiceTable.item(i, 3).text().split(' ')[0]
                qty = _utils.getIntegralPart(qty)
            rate = 0
            if self._salesInvoiceUI.salesInvoiceTable.item(i, 4):
                rate = self._salesInvoiceUI.salesInvoiceTable.item(i, 4).text()
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
            if self._salesInvoiceUI.salesInvoiceTable.cellWidget(i, 5).currentText():
                cgst = float(self._salesInvoiceUI.salesInvoiceTable.cellWidget(i, 5).currentText())
            sgst = 0
            if self._salesInvoiceUI.salesInvoiceTable.cellWidget(i, 6).currentText():
                sgst = float(self._salesInvoiceUI.salesInvoiceTable.cellWidget(i, 6).currentText())
            igst = 0
            if self._salesInvoiceUI.salesInvoiceTable.cellWidget(i, 7).currentText():
                igst = float(self._salesInvoiceUI.salesInvoiceTable.cellWidget(i, 7).currentText())
            amountWithoutTax = float(qty) * float(rate)
            self._salesInvoiceUI.salesInvoiceTable.setItem(i, 8, self._salesInvoiceUI.salesInvoiceTable.getReadOnlyItem(str(amountWithoutTax)))
            tax_value = (amountWithoutTax * cgst) / 100 + (amountWithoutTax * sgst) / 100 + (
                    amountWithoutTax * igst) / 100
            self._salesInvoiceUI.salesInvoiceTable.setItem(i, 9, self._salesInvoiceUI.salesInvoiceTable.getReadOnlyItem(str(tax_value)))
            self._salesInvoiceUI.salesInvoiceTable.setItem(i, 10, self._salesInvoiceUI.salesInvoiceTable.getReadOnlyItem(str(tax_value + amountWithoutTax)))
            self.__populateAmountWidget()

    def __computeAmount(self, row, col):
        if col == 3:
            if self._salesInvoiceUI.salesInvoiceTable.item(row, col + 1):
                self.__computeAmountValues(row)
        elif col == 4:
            if self._salesInvoiceUI.salesInvoiceTable.item(row, col - 1):
                self.__computeAmountValues(row)

    _utils.showWaitCursor
    def __updateFromCustomerName(self):
        customerInfo = self.__customerInfo.get(
            self._salesInvoiceUI.customerNameValue.text(),
            None)
        if customerInfo:
            customerAddress, gstin, stateCode = customerInfo
            self._salesInvoiceUI.customerAddressValue.setText(customerAddress)
            self._salesInvoiceUI.gstinValue.setText(gstin)
            self._salesInvoiceUI.stateCodeValue.setText(str(stateCode))

    _utils.showWaitCursor
    def __updateFromCustomerAddress(self):
        customerInfo = {v[0]: [k]+list(v[1:]) for k, v in self.__customerInfo.iteritems()}
        customerInfo = customerInfo.get(
            self._salesInvoiceUI.customerAddressValue.text(),
            None)
        if customerInfo:
            customerName, gstin, stateCode = customerInfo
            self._salesInvoiceUI.customerNameValue.setText(customerName)
            self._salesInvoiceUI.gstinValue.setText(gstin)
            self._salesInvoiceUI.stateCodeValue.setText(str(stateCode))


    def __validateInputs(self):
        if not self._salesInvoiceUI.customerNameValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Name must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self._salesInvoiceUI.customerAddressValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Address must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self._salesInvoiceUI.gstinValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer GSTIN must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self._salesInvoiceUI.stateCodeValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer State Code must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False


        if not self._salesInvoiceUI.stateCodeValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer State Code must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self._salesInvoiceUI.poNoValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Purchase Order No must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self._salesInvoiceUI.poDateValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Purchase Order Date must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self._salesInvoiceUI.vendorCodeValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Vendor Code must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self._salesInvoiceUI.paymentTermsValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Payment Terms must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self._salesInvoiceUI.dcNoValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Delivery Challan must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self._salesInvoiceUI.dcDateValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Delivery Challan Date must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self._salesInvoiceUI.vehicleNoValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Vehicle No must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self._salesInvoiceUI.dispatchedValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Dispatched through must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self._salesInvoiceUI.amountPaidValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Amount Paid must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        particulars, quantities, rates, hsn_codes, amounts = [], [], [], [], []
        item_codes, cgst, sgst, igst = [], [], [], []
        for i in range(self._salesInvoiceUI.salesInvoiceTable.rowCount()):
            item_code = self._salesInvoiceUI.salesInvoiceTable.cellWidget(i, 0)
            if item_code and item_code.text():
                item_codes.append(item_code.text())
            particular = self._salesInvoiceUI.salesInvoiceTable.item(i, 1)
            if particular and particular.text():
                particulars.append(str(particular.text()))
            hsn_code = self._salesInvoiceUI.salesInvoiceTable.item(i, 2)
            if hsn_code and hsn_code.text():
                hsn_codes.append(str(hsn_code.text()))
            quantity = self._salesInvoiceUI.salesInvoiceTable.item(i, 3)
            if (quantity and quantity.text()):
                quantities.append(str(quantity.text()))
            rate = self._salesInvoiceUI.salesInvoiceTable.item(i, 4)
            if (rate and rate.text()):
                rates.append(str(rate.text()))
            amount = self._salesInvoiceUI.salesInvoiceTable.item(i, 8)
            if (amount and amount.text()):
                amounts.append(str(amount.text()))
                cgst.append(self._salesInvoiceUI.salesInvoiceTable.cellWidget(i, 5).currentText())
                sgst.append(self._salesInvoiceUI.salesInvoiceTable.cellWidget(i, 6).currentText())
                igst.append(self._salesInvoiceUI.salesInvoiceTable.cellWidget(i, 7).currentText())

        max_table_items = max([len(item_codes), len(particulars), len(hsn_codes), len(quantities), len(rates)])
        for i in rates:
            try:
                float(i)
            except:
                _QtGui.QMessageBox.critical(self, 'Rate must be Numbers')
                return False
        if len(item_codes) != max_table_items:
            _QtGui.QMessageBox.critical(self, 'ERROR', 'All Item Codes column must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False
        if len(particulars) != max_table_items:
            _QtGui.QMessageBox.critical(self, 'ERROR', 'All Particulars column must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False
        if len(hsn_codes) != max_table_items:
            _QtGui.QMessageBox.critical(self, 'ERROR', 'All HSN Code column must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False
        if len(quantities) != max_table_items:
            _QtGui.QMessageBox.critical(self, 'ERROR', 'All Quantity column must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False
        if len(rates) != max_table_items:
            _QtGui.QMessageBox.critical(self, 'ERROR', 'All Rate column must be entered', buttons=_QtGui.QMessageBox.Ok)
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
                float(rates[i]))
        self.__itemCodes = item_codes
        self.__particulars = particulars
        self.__hsnCode = hsn_codes
        self.__quantity = quantities
        self.__rate = rates
        self.__amount = amounts
        self.__allCgst = cgst
        self.__allSgst = sgst
        self.__allIgst = igst

        self.__cgst = str(self._salesInvoiceUI.salesInvoiceTable.cellWidget(0, 5).currentText())
        self.__sgst = str(self._salesInvoiceUI.salesInvoiceTable.cellWidget(0, 6).currentText())
        self.__igst = str(self._salesInvoiceUI.salesInvoiceTable.cellWidget(0, 7).currentText())

        self.__cgstValue = (sum(map(float, self.__amount)) * float(self.__cgst)) / 100
        self.__sgstValue = (sum(map(float, self.__amount)) * float(self.__sgst)) / 100
        self.__igstValue = (sum(map(float, self.__amount)) * float(self.__igst)) / 100

        return True

    _utils.showWaitCursor
    def __saveToPdf(self):
        if self._salesInvoiceUI.customerNameValue.text() not in self.__customerInfo:
            dialog = CustomerDialog(
                self._salesInvoiceUI.customerNameValue.text(),
                self._salesInvoiceUI.customerAddressValue.text(),
                self._salesInvoiceUI.gstinValue.text(),
                self._salesInvoiceUI.stateCodeValue.text())
            dialog.setWindowTitle('Preview')
            dialog.exec_()
        if not self.__validateInputs():
            return

        self._manager.saveSalesInfo(
            self._salesInvoiceUI.customerNameValue.text(),
            self._salesInvoiceUI.customerAddressValue.text(),
            self._salesInvoiceUI.gstinValue.text(),
            int(self._salesInvoiceUI.stateCodeValue.text()),
            self._salesInvoiceUI.comboBox.currentText(),
            self._salesInvoiceUI.billNoValue.text(),
            self._salesInvoiceUI.billDateValue.date().toPython(),
            self._salesInvoiceUI.poNoValue.text(),
            self._salesInvoiceUI.poDateValue.text(),
            self._salesInvoiceUI.vendorCodeValue.text(),
            self._salesInvoiceUI.paymentTermsValue.text(),
            self._salesInvoiceUI.dcNoValue.text(),
            self._salesInvoiceUI.dcDateValue.text(),
            self._salesInvoiceUI.vehicleNoValue.text(),
            self._salesInvoiceUI.dispatchedValue.text(),
            float(self._salesInvoiceUI.beforeTaxValue.text()),
            float(self._salesInvoiceUI.afterTaxValue.text()),
            float(self._salesInvoiceUI.amountPaidValue.text()),
            self._salesInvoiceUI.remarksValue.toPlainText(),
        '')

        for (itemCode, particular, hsnCode, quantity, rate, cgst, sgst, igst) in zip(self.__itemCodes, self.__particulars, self.__hsnCode, self.__quantity,
                                                         self.__rate, self.__allCgst, self.__allSgst, self.__allIgst):
            self._manager.saveSalesItemInfo(
                self._salesInvoiceUI.billNoValue.text(),
                itemCode,
                particular,
                hsnCode,
                quantity,
                float(rate),
                float(cgst),
                float(sgst),
                float(igst))
        try:
            salesDirectory = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(__file__))),
                     self.__type, self._salesInvoiceUI.billNoValue.text())
            _os.makedirs(salesDirectory)
        except:
            return _QtGui.QMessageBox.critical(self, 'ERROR', 'Bill No is already generated.', buttons=_QtGui.QMessageBox.Ok)

        salesDetails = self.__getSalesDetails()
        pdfPath = _os.path.join(salesDirectory, '{0}.pdf'.format(self._salesInvoiceUI.billNoValue.text()))
        canvas = _Canvas(
            pdfPath,
            pagesize=_letter)
        invoiceTemplate.InvoiceTemplate(canvas, salesDetails, 'original')
        canvas.save()
        pdfPath = _os.path.join(salesDirectory, '{0}_duplicate.pdf'.format(self._salesInvoiceUI.billNoValue.text()))
        canvas = _Canvas(
            pdfPath,
            pagesize=_letter)
        invoiceTemplate.InvoiceTemplate(canvas, salesDetails, 'duplicate')
        canvas.save()
        pdfPath = _os.path.join(salesDirectory, '{0}_triplicate.pdf'.format(self._salesInvoiceUI.billNoValue.text()))
        canvas = _Canvas(
            pdfPath,
            pagesize=_letter)
        invoiceTemplate.InvoiceTemplate(canvas, salesDetails, 'triplicate')
        canvas.save()
        pdfPath = _os.path.join(salesDirectory, '{0}_extraCopy.pdf'.format(self._salesInvoiceUI.billNoValue.text()))
        canvas = _Canvas(
            pdfPath,
            pagesize=_letter)
        invoiceTemplate.InvoiceTemplate(canvas, salesDetails, 'extra copy')
        canvas.save()


        if self._salesInvoiceUI.deliveryChallan.isChecked():
            dcDirectory = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(__file__))),
                                  'Delivery Challan', self._salesInvoiceUI.billNoValue.text())
            try:
                _os.makedirs(dcDirectory)
            except:
                return _QtGui.QMessageBox.critical(self, 'ERROR', 'Delivery Challan is already generated.',
                                                   buttons=_QtGui.QMessageBox.Ok)
            removeKeys = ('customerName', 'customerAddress', 'gstin', 'stateCode',
                          'billNo', 'billDate', 'poNo', 'poDate', 'vendorCode',
                          'paymentTerms', 'dcNo', 'dcDate', 'vehicleNo', 'dispatchedThrough')
            for dictKey in removeKeys:
                if dictKey in salesDetails:
                    continue
                del salesDetails[dictKey]
            pdfPath = _os.path.join(dcDirectory, '{0}.pdf'.format(self._salesInvoiceUI.billNoValue.text()))
            canvas = _Canvas(
                pdfPath,
                pagesize=_letter)
            deliveryChallanTemplate.DeliveryChallanTemplate(canvas, salesDetails)
            canvas.save()

        if self._salesInvoiceUI.printCheckBox.isChecked():
            self.handlePrint()
        _QtGui.QMessageBox.information(self, 'Saved', 'Entered Sales Invoice saved successfully', buttons=_QtGui.QMessageBox.Ok)
        self.__discardChanges()

    _utils.showWaitCursor
    def __discardChanges(self):
        self._salesInvoiceUI.customerNameValue.setText('')
        self._salesInvoiceUI.customerAddressValue.setText('')
        self._salesInvoiceUI.gstinValue.setText('')
        self._salesInvoiceUI.stateCodeValue.setText('')
        self.__billNo += 1
        self._salesInvoiceUI.billNoValue.setText(str(self.__billNo))
        self._salesInvoiceUI.billDateValue.setDate(_QtCore.QDate.currentDate())
        self._salesInvoiceUI.poNoValue.setText('')
        self._salesInvoiceUI.poDateValue.setText('')
        self._salesInvoiceUI.vendorCodeValue.setText('')
        self._salesInvoiceUI.paymentTermsValue.setText('')
        self._salesInvoiceUI.dcNoValue.setText('')
        self._salesInvoiceUI.dcDateValue.setText('')
        self._salesInvoiceUI.vehicleNoValue.setText('')
        self._salesInvoiceUI.dispatchedValue.setText('')

        self._salesInvoiceUI.salesInvoiceTable.clearSlot()
        self._salesInvoiceUI.beforeTaxValue.setText('')
        self._salesInvoiceUI.afterTaxValue.setText('')
        self._salesInvoiceUI.taxValue.setText('')
        self._salesInvoiceUI.amountPaidValue.setText('')
        self._salesInvoiceUI.remarksValue.setText('')
        self._salesInvoiceUI.amountWordsValue.setText('')

    def __getSalesDetails(self):
        amountBeforeRs, amountBeforePs = '{: 0.2f}'.format(float(self._salesInvoiceUI.beforeTaxValue.text())).split('.')
        amountAfterRs, amountAfterPs = '{: 0.2f}'.format(float(self._salesInvoiceUI.afterTaxValue.text())).split('.')
        cgstRs, cgstPs = '{: 0.2f}'.format(float(self.__cgstValue)).split('.')
        sgstRs, sgstPs = '{: 0.2f}'.format(float(self.__sgstValue)).split('.')
        igstRs, igstPs = '{: 0.2f}'.format(float(self.__igstValue)).split('.')
        amountWords = self._salesInvoiceUI.amountWordsValue.toPlainText().split(' ')
        if len(amountWords) > 7:
            amountWords = ' '.join(amountWords[: 7]) + ' '.join(amountWords[7:])
        else:
            amountWords = [' '.join(amountWords)]

        # for quotationInfo in self.__quotationModelData.tableData:
        billInfo = {
            'customerName': self._salesInvoiceUI.customerNameValue.text(),
            'customerAddress': self._salesInvoiceUI.customerAddressValue.text(),
            'gstin': self._salesInvoiceUI.gstinValue.text(),
            'stateCode': self._salesInvoiceUI.stateCodeValue.text(),
            'billNo': self._salesInvoiceUI.billNoValue.text(),
            'billDate': self._salesInvoiceUI.billDateValue.date().toPython().strftime('%d-%b-%y'),
            'poNo': self._salesInvoiceUI.poNoValue.text(),
            'poDate': self._salesInvoiceUI.poDateValue.text(),
            'vendorCode': self._salesInvoiceUI.vendorCodeValue.text(),
            'paymentTerms': self._salesInvoiceUI.paymentTermsValue.text(),
            'dcNo': self._salesInvoiceUI.dcNoValue.text(),
            'dcDate': self._salesInvoiceUI.dcDateValue.text(),
            'vehicleNo': self._salesInvoiceUI.vehicleNoValue.text(),
            'dispatchedThrough': self._salesInvoiceUI.dispatchedValue.text(),
            'amountWithoutTaxRs': amountBeforeRs,
            'amountWithoutTaxPs': amountBeforePs,
            'cgst': '{}%'.format(self.__cgst),
            'cgstRs': cgstRs,
            'cgstPs': cgstPs,
            'sgst': '{}%'.format(self.__sgst),
            'sgstRs': sgstRs,
            'sgstPs': sgstPs,
            'igst': '{}%'.format(self.__igst),
            'igstRs': igstRs,
            'igstPs': igstPs,
            'taxPs':'**',
            'amountWithTaxRs' : amountAfterRs,
            'amountWithTaxPs': amountAfterPs,
            'amountWord': amountWords,

            'itemCodes': self.__itemCodes,
            'particulars': self.__particulars,
            'hsnCodes': self.__hsnCode,
            'quantities': self.__quantity,
            'rates': self.__rate,
            'amounts': self.__amount,
            'fileName': self._salesInvoiceUI.billNoValue.text()
        }
        return billInfo

    _utils.showWaitCursor
    def __handlePreview(self):
        if self._salesInvoiceUI.customerNameValue.text().strip() and  self._salesInvoiceUI.customerNameValue.text() not in self.__customerInfo:
            dialog = CustomerDialog(self._salesInvoiceUI.customerNameValue.text(), self._salesInvoiceUI.customerAddressValue.text())
            dialog.exec_()
        if not self.__validateInputs():
            return

        import tempfile, shutil
        salesDirectory = tempfile.mkdtemp()
        pdfPath = _os.path.join(salesDirectory, '{0}.pdf'.format(self._salesInvoiceUI.billNoValue.text()))
        canvas = _Canvas(
            pdfPath,
            pagesize=_letter)
        salesDetails = self.__getSalesDetails()
        invoiceTemplate.InvoiceTemplate(canvas, salesDetails, '')
        canvas.save()
        dialog = _utils.PreviewDialog(self, pdfPath)
        dialog.setWindowTitle('')
        dialog.exec_()
        shutil.rmtree(salesDirectory)

    _utils.showWaitCursor
    def handlePrint(self):
        dialog = _QtGui.QPrintDialog()
        if dialog.exec_() == _QtGui.QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def saveSlot(self):
        self.__saveRestore.save(_QtGui.qApp.allWidgets())

    def restoreSlot(self):
        self.__saveRestore.restore()