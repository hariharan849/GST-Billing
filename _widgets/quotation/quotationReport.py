

from database import QuotationManager
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
from _widgets.common.itemInfoWidget import ItemInfoWidget
from ui.quotationReportUI import Ui_quotationReport
from models import QuotationReportTableModel, QuotationReportProxyModel, constants, QuotationDetailsSaveWorker, ItemDetails
from widgets import utils as _utils
from _widgets import common
import os as _os
import datetime as _datetime
import collections as _collections
import pandas as _pd
from pdf_templates.quotationTemplate import QuotationTemplate

from reportlab.lib.pagesizes import letter as _letter
from reportlab.pdfgen.canvas import Canvas as _Canvas

class QuotationReportWidget(_QtGui.QWidget):
    '''
    UI for quotation widget
    '''
    def __init__(self, parent=None):
        super(QuotationReportWidget, self).__init__(parent)
        self.__quotationReportUI = Ui_quotationReport()
        self._manager = QuotationManager()
        self.__setupWidget()
        self.__connectWidget()
        self.__setQuotationInformation()

    def __setupWidget(self):
        '''
        Sets all quotation req widgets
        '''
        self.__quotationReportUI.setupUi(self)

        self.__quotationModelData = QuotationReportTableModel()
        self.__quotationProxyModel = QuotationReportProxyModel()
        self.__quotationProxyModel.setSourceModel(self.__quotationModelData)
        self.__quotationProxyModel.setDynamicSortFilter(True)
        self.__quotationProxyModel.setFilterCaseSensitivity(_QtCore.Qt.CaseInsensitive)
        self.__quotationReportUI.quotationReportTable.setModel(self.__quotationProxyModel)

        self.__quotationReportUI.fromDateValue.setDate(_QtCore.QDate.currentDate())
        self.__quotationReportUI.toDateValue.setDate(_QtCore.QDate.currentDate())

        self.showMaximized()

    def __connectWidget(self):
        '''
        Connect all widget signal and slots
        '''
        self.__quotationReportUI.resetButton.clicked.connect(self.__discardChanges)
        self.__quotationReportUI.searchButton.clicked.connect(self.__searchChanges)
        self.__quotationReportUI.saveButton.clicked.connect(self.__saveTableChanges)
        self.__quotationReportUI.quotationReportTable.removeEntry.connect(self.__removeFromDatabase)
        self.__quotationReportUI.removeButton.clicked.connect(self.__quotationReportUI.quotationReportTable.removeSlot)
        self.__quotationReportUI.clearButton.clicked.connect(self.__quotationReportUI.quotationReportTable.clearSlot)
        # self.__quotationReportUI.groupBox.toggled.connect(lambda: _utils.toggleGroup(self.__quotationReportUI.groupBox))

    def __removeFromDatabase(self, row='all'):
        '''
        Removes entry from database
        '''
        if row != 'all':
            quotationInfoEntry = self._manager.getQuotationDetailsInfo(self.__quotationProxyModel.index(row, 2).data())
            quotationInfoEntry.delete_instance()
            if not quotationInfoEntry.cancelReason:
                self.updateAmountValue(row)
            return
        self._manager.deleteQuotationDetailsInfo()
        self.__quotationReportUI.amountValue.setText('')
        self.__quotationReportUI.taxValue.setText('')
        self.__quotationReportUI.totalValue.setText('')

    def setData(self, index, value, role=_QtCore.Qt.EditRole):
        '''
        Sets data for the specified cell upon edit
        '''
        if index.column() not in [5, 6, 7]:
            super(QuotationReportTableModel, self).setData(index, value, role)
            return
        if role == _QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            if index.data() == value:
                return False
            setattr(self.tableData[row], self.settings[column][constants._columnId],
                    constants.valueWrapper(value, True))
            amount = float(getattr(self.tableData[row], self.settings[5][constants._columnId]).value)
            tax = float(getattr(self.tableData[row], self.settings[6][constants._columnId]).value)
            total = float(getattr(self.tableData[row], self.settings[7][constants._columnId]).value)
            if column == 5:
                setattr(self.tableData[row], self.settings[7][constants._columnId],
                        constants.valueWrapper(amount+tax, True))
            elif column == 6:
                setattr(self.tableData[row], self.settings[7][constants._columnId],
                        constants.valueWrapper(amount + tax, True))
            elif column == 7:
                setattr(self.tableData[row], self.settings[5][constants._columnId],
                        constants.valueWrapper(total-tax, True))
            return True
        return False

    def updateAmountValue(self, cancelRow=None):
        '''
        Received when model data is removed
        '''
        amount = tax = total = 0
        # print self.__purchaseProxyModel.rowCount()
        for row in range(self.__quotationProxyModel.rowCount()):
            print self.__quotationProxyModel.index(row, 2).data()
            if cancelRow == row:
                continue
            if self.__quotationProxyModel.index(row, 8).data():
                continue
            amount += float(self.__quotationProxyModel.index(row, 5).data())
            tax += float(self.__quotationProxyModel.index(row, 6).data())
            total += float(self.__quotationProxyModel.index(row, 7).data())
        self.__quotationReportUI.amountValue.setText(str(amount))
        self.__quotationReportUI.totalValue.setText(str(total))
        self.__quotationReportUI.taxValue.setText(str(tax))

    def __setQuotationInformation(self):
        '''
        Sets all quotation information from db
        '''
        quotationReportTableData = []
        quotationData = self._manager.fetchAllQuotationInfo()
        totalEstAmount = 0
        totalAmount = 0
        for info in quotationData:
            self.__quotationModelData.addQuotationInfo(
                str(info.customerName),
                str(info.customerAddress),
                str(info.quotationNo),
                info.quotationDate.strftime('%d - %b - %Y'),
                info.quotationValidity.strftime('%d - %b - %Y'),
                str(info.estAmount),
                str(info.estTotal - info.estAmount),
                str(info.estTotal),
                info.cancelReason
            )
            if info.cancelReason:
                continue
            totalEstAmount += float(info.estAmount)
            totalAmount += float(info.estTotal)
        self.__quotationReportUI.amountValue.setText(str(totalEstAmount))
        self.__quotationReportUI.totalValue.setText(str(totalAmount))
        self.__quotationReportUI.taxValue.setText(str(totalAmount - totalEstAmount))

    _utils.showWaitCursor
    def __saveTableChanges(self):
        '''
        Save Table change to database
        '''
        quotationWorker = QuotationDetailsSaveWorker(self.__quotationModelData.tableData, self._manager)
        quotationWorker.start()
        _QtGui.QMessageBox.information(self, 'Saved', 'Quotation Information Saved Successfully.',
                                       buttons=_QtGui.QMessageBox.Ok)
        self.updateAmountValue()

    def __validateSearchDate(self):
        '''
        Validates search from and to date
        '''
        if self.__quotationReportUI.fromDateValue.date() > self.__quotationReportUI.toDateValue.date():
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

        customerName = str(self.__quotationReportUI.customerSearchValue.text())
        quotationNo = str(self.__quotationReportUI.billSearchValue.text())
        fromDate = self.__quotationReportUI.fromDateValue.date()
        toDate = self.__quotationReportUI.toDateValue.date()

        self.__quotationProxyModel.setFilterByColumn(
            _QtCore.QRegExp(quotationNo, _QtCore.Qt.CaseInsensitive, _QtCore.QRegExp.FixedString), 2)
        self.__quotationProxyModel.setFilterByColumn(
            _QtCore.QRegExp(customerName, _QtCore.Qt.CaseInsensitive, _QtCore.QRegExp.FixedString), 0)
        self.__quotationProxyModel.setFilterByColumn(
            constants.dateFilter(fromDate.toString('dd - MMM - yyyy'), toDate.toString('dd - MMM - yyyy')), 3)
        self.updateAmountValue()

    _utils.showWaitCursor
    def __discardChanges(self):
        '''
        Discards all widgets to default values.
        '''
        self.__quotationReportUI.customerSearchValue.setText('')
        self.__quotationReportUI.billSearchValue.setText('')
        self.__quotationReportUI.fromDateValue.setDate(_QtCore.QDate.currentDate())
        self.__quotationReportUI.toDateValue.setDate(_QtCore.QDate.currentDate())
        self.__quotationReportUI.quotationReportTable.clearSlot()
        self.__quotationReportUI.amountValue.setText('')
        self.__quotationReportUI.taxValue.setText('')
        self.__quotationReportUI.totalValue.setText('')
        self.__setQuotationInformation()

    def viewItems(self, quotationNo):
        '''
        launche dialog to dispay items associated with quotation no
        '''
        quotationDetail = self._manager.getQuotationDetailsInfo(quotationNo)
        quotationProduct = self._manager.getQuotationItemInfo(quotationNo)

        dialog = _QtGui.QDialog(self)
        itemInfoWidget = common.itemInfoWidget.ItemInfoWidget(quotationNo, quotationProduct, constants._quotationSettings, quotationDetail.remarks, parent=self)
        layout = _QtGui.QHBoxLayout(dialog)
        layout.addWidget(itemInfoWidget)
        dialog.setWindowTitle('Quotation Item')
        dialog.exec_()

    def cancelBill(self, quotationNo, cancelReason):
        '''
        Cancels quoation for the passed quotationno
        '''
        quotationDetails = self._manager.getQuotationDetailsInfo(quotationNo)
        quotationDetails.cancelReason = cancelReason
        quotationTableData = [data for data in self.__quotationModelData.tableData if data.quotationNo.value == quotationNo]
        quotationTableData[0].cancelReason = constants.valueWrapper(cancelReason, False)
        quotationDetails.save()
        self.updateAmountValue()

    def addItemInfo(self, itemInfo):
        return ItemDetails(itemInfo)

    def createPDF(self, quotationNo):
        '''
        Creates pdf for the passed quotation no
        '''
        try:
            quotationDirectory = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(__file__))),
                          'quotation', quotationNo)
            _os.makedirs(quotationDirectory)
        except:
            pass
        today = _datetime.datetime.today().strftime('%Y_%m_%d-%H_%M_%S')
        canvas = _Canvas(
            _os.path.join(quotationDirectory, '{0}.pdf'.format(today)),
            pagesize=_letter)
        QuotationTemplate(canvas, self.__getQuotationDetails(quotationNo))
        canvas.save()

        _QtGui.QMessageBox.information(self, 'Saved', 'Quotation Information PDF created.',
                                       buttons=_QtGui.QMessageBox.Ok)

    def __getQuotationDetails(self, quotationNo):
        '''
        Returns quotation details for the passed quotation no
        '''
        quotationDetails = self._manager.getQuotationDetailsInfo(quotationNo)
        quotationItem = self._manager.getQuotationItemInfo(quotationNo)
        particulars = []
        hsnCode = []
        quantity = []
        rate = []
        amounts = []
        total = 0
        cgst, sgst, igst = '', '', ''
        cgstValue, sgstValue, igstValue = 0, 0, 0
        for item in quotationItem:
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

        amountBeforeRs, amountBeforePs = '{: 0.2f}'.format(quotationDetails.estAmount).split('.')
        amountAfterRs, amountAfterPs = '{: 0.2f}'.format(quotationDetails.estTotal).split('.')
        cgstRs, cgstPs = '{: 0.2f}'.format(float(cgstValue)).split('.')
        sgstRs, sgstPs = '{: 0.2f}'.format(float(sgstValue)).split('.')
        igstRs, igstPs = '{: 0.2f}'.format(float(igstValue)).split('.')

        convertor = _utils.Number2Words()
        amountWord = convertor.convertNumberToWords(quotationDetails.estAmount) + ' Only'
        amountWords = amountWord.split(' ')
        if len(amountWords) > 7:
            amountWords = ' '.join(amountWords[: 7]) + ' '.join(amountWords[7:])
        else:
            amountWords = [' '.join(amountWords)]

        billInfo = {
            'customerName': quotationDetails.customerName,
            'customerAddress': quotationDetails.customerAddress,
            'billNo': quotationNo,
            'quotationDate': quotationDetails.quotationDate.strftime('%d-%b-%y'),
            'validDate': quotationDetails.quotationValidity.strftime('%d-%b-%y'),

            'amountBeforeRs': amountBeforeRs,
            'amountBeforePs': amountBeforePs,
            'cgst': '{}%'.format(cgst),
            'cgstRs': cgstRs,
            'cgstPs': cgstPs,
            'sgst': '{}%'.format(sgst),
            'sgstRs': sgstRs,
            'sgstPs': sgstPs,
            'igst': '{}%'.format(igst),
            'igstRs': igstRs,
            'igstPs': igstPs,
            'origTaxPs':'',
            'afterTaxRs' : amountAfterRs,
            'afterTaxPs': amountAfterPs,
            'amountWord': amountWords,

            'particulars': particulars,
            'hsnCodes': hsnCode,
            'quantities': quantity,
            'rates': rate,
            'amounts': amounts
        }
        return billInfo

    def exportToExcel(self):
        '''
        Exports all the quotation information to excel
        '''
        df = self._getDataframe()
        exportPath = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(__file__))), 'Exports', 'Quotation')
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
        _QtGui.QMessageBox.information(self, 'Saved', 'Quotation Information Exported Successfully.',
                                       buttons=_QtGui.QMessageBox.Ok)

    def _getDataframe(self):
        '''
        Returns dataframe for quotion table
        '''
        name, address, quotation_no, quotation_date = [], [], [], []
        valid_until, amount, cgst, sgst, igst, total, remarks = [], [], [], [], [], [], []
        for i in range(self.__quotationProxyModel.rowCount()):
            entry = self._manager.getQuotationDetailsInfo(self.__quotationProxyModel.index(i, 2).data())
            if entry.cancelReason:
                continue
            name.append(entry.customerName)
            address.append(entry.customerAddress)
            quotation_no.append(entry.quotationNo)
            quotation_date.append(entry.quotationDate)

            valid_until.append(entry.quotationValidity)
            amount.append(entry.estAmount)
            total.append(entry.estTotal)
            remarks.append(entry.remarks)

        purchase_values = _collections.OrderedDict()
        purchase_values = _collections.OrderedDict()
        purchase_values['Customer Name'] = name
        purchase_values['Customer Address'] = address

        purchase_values['Quotation No'] = quotation_no
        purchase_values['Quotation Date'] = quotation_date
        purchase_values['Valid Until Date'] = valid_until

        purchase_values['Amount'] = amount
        purchase_values['Total'] = total
        purchase_values['Remarks'] = remarks

        return _pd.DataFrame(purchase_values)
