
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
from performaInvoice import PerformaInvoiceWidget


class SalesInvoiceWidget(PerformaInvoiceWidget):
    '''
    Creates Quotation UI.
    '''

    def __init__(self, type='sales', parent=None):
        super(SalesInvoiceWidget, self).__init__(type, parent)
        self.performaNoValue = _QtGui.QLineEdit()
        self.performaNoValue.setPlaceholderText('Enter Performa No')

        sizePolicy = _QtGui.QSizePolicy(
            _QtGui.QSizePolicy.Fixed, _QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.performaNoValue.sizePolicy().hasHeightForWidth())
        self.performaNoValue.setMinimumSize(_QtCore.QSize(150, 30))
        self.performaNoValue.setSizePolicy(sizePolicy)

        self._salesInvoiceUI.performaLayout.addWidget(self.performaNoValue)
        self._connectWidgets()

    def _connectWidgets(self):
        self.performaNoValue.textChanged.connect(self._populateFromPerforma)

    def _populateFromPerforma(self, text):
        info = self._manager.getSalesInfo(self.performaNoValue.text(), 'performa')

        self._salesInvoiceUI.customerNameValue.setText(info.customerName)
        self._salesInvoiceUI.customerAddressValue.setText(info.customerAddress)
        self._salesInvoiceUI.gstinValue.setText(info.customerGstin)
        self._salesInvoiceUI.stateCodeValue.setText(str(info.customerStateCode))
        itemIndex = self._salesInvoiceUI.comboBox.findText(info.paidBy, _QtCore.Qt.MatchFixedString)
        self._salesInvoiceUI.comboBox.setCurrentIndex(itemIndex if itemIndex >= 0 else 0)

        billDate = _QtCore.QDate(2011, 4, 22)
        self._salesInvoiceUI.billDateValue.setDate(billDate)
        self._salesInvoiceUI.poNoValue.setText(info.poNo)
        self._salesInvoiceUI.poDateValue.setText(info.poDate)
        self._salesInvoiceUI.vendorCodeValue.setText(info.vendorCode)
        self._salesInvoiceUI.paymentTermsValue.setText(info.paymentTerms)
        self._salesInvoiceUI.dcNoValue.setText(info.dcCode)
        self._salesInvoiceUI.dcDateValue.setText(info.dcDate)
        self._salesInvoiceUI.vehicleNoValue.setText(info.vehicleNo)
        self._salesInvoiceUI.dispatchedValue.setText(info.dispatchedThrough)

        self._salesInvoiceUI.remarksValue.setText(info.remarks)

        itemDetails = self._manager.getSalesItemInfo(info.billNo, 'performa')
        for row, item in enumerate(itemDetails):
            print dir(item), item.hsnCode
            particular = _QtGui.QTableWidgetItem(item.particular)
            self._salesInvoiceUI.salesInvoiceTable.setItem(row, 1, particular)
            hsnCode = _QtGui.QTableWidgetItem(str(item.hsnCode))
            self._salesInvoiceUI.salesInvoiceTable.setItem(row, 2, hsnCode)
            quantity = _QtGui.QTableWidgetItem(str(item.quantity))
            self._salesInvoiceUI.salesInvoiceTable.setItem(row, 3, quantity)
            itemPrice = _QtGui.QTableWidgetItem(str(item.rate))
            self._salesInvoiceUI.salesInvoiceTable.setItem(row, 4, itemPrice)
            
