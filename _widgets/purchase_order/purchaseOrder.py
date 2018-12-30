import os as _os
import pandas as _pandas
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
from _widgets import utils
from ui.purchaseOrderUI import Ui_PurchaseOrder
from models import PurchaseOrderTableModel

from database import PurchaseOrderManager, CompanyItemManager, CustomerManager

class PurchaseOrderWidget(_QtGui.QWidget):
    '''
    Creates Quotation UI.
    '''
    settings = _QtCore.QSettings("po.ini", _QtCore.QSettings.IniFormat)
    def __init__(self, parent=None):
        super(PurchaseOrderWidget, self).__init__(parent)
        self.__manager = PurchaseOrderManager()
        self.__companyItemManager = CompanyItemManager('purchase')
        self.__customerManager = CustomerManager()
        self.__purchaseOrderUI = Ui_PurchaseOrder()
        self.__setVariables()
        self.__setUpWidget()
        self.__connectWidgets()
        self.__saveRestore = utils.StoreRestore(self.settings)

        saveShortcut = _QtGui.QShortcut(_QtGui.QKeySequence("Ctrl+S"), self)
        saveShortcut.activated.connect(self.saveSlot)
        restoreShortcut = _QtGui.QShortcut(_QtGui.QKeySequence("Ctrl+R"), self)
        restoreShortcut.activated.connect(self.restoreSlot)

    def __setVariables(self):
        '''
        Sets req varaibles
        '''
        self.__particulars = []
        self.__hsnCode = []
        self.__quantity = []
        self.__purchaseItemInfo = (item.itemCode for item in self.__companyItemManager.fetchAllCompanyItemInfo())
        self.__customerInfo = {customerInfo.custName: customerInfo.custAddress for customerInfo in
                               self.__customerManager.fetchAllCustomerInfo()}

    def __setUpWidget(self):
        self.__purchaseOrderUI.setupUi(self)

        self.__purchaseOrderUI.poDateValue.setDate(_QtCore.QDate.currentDate())

        self.__poModelData = PurchaseOrderTableModel()
        self.__purchaseOrderUI.purchaseOrderTable.setModel(self.__poModelData)

        self.__purchaseOrderUI.purchaseOrderTable.setGeometry(_QtGui.QApplication.desktop().screenGeometry())
        width = self.size().width()
        self.__purchaseOrderUI.purchaseOrderTable.setColumnWidth(0, width / 15)
        self.__purchaseOrderUI.purchaseOrderTable.setColumnWidth(1, (width * 3.92) / 5.5)
        self.__purchaseOrderUI.purchaseOrderTable.setColumnWidth(2, width / 8)
        self.__purchaseOrderUI.purchaseOrderTable.setColumnWidth(3, width / 18)
        self.showMaximized()

    def __connectWidgets(self):
        self.__purchaseOrderUI.saveButton.clicked.connect(self.__saveToPdf)
        self.__purchaseOrderUI.discardButton.clicked.connect(self.__discardChanges)
        self.__purchaseOrderUI.addButton.clicked.connect(self.__purchaseOrderUI.purchaseOrderTable.addRow)
        self.__purchaseOrderUI.removeButton.clicked.connect(self.__purchaseOrderUI.purchaseOrderTable.removeSlot)
        self.__purchaseOrderUI.clearButton.clicked.connect(self.__clearSlot)
        self.__purchaseOrderUI.importButton.clicked.connect(self.importItems)
        # self.__purchaseOrderUI.groupBox.toggled.connect(
        #     lambda: utils.toggleGroup(self.__purchaseOrderUI.groupBox))

        utils.setCompleter(self.__purchaseOrderUI.customerNameValue, self.__customerInfo.keys())

    @utils.showWaitCursor
    def importItems(self):
        '''
        gets company items from table
        '''
        fileName, ok = _QtGui.QFileDialog.getOpenFileName(
            self, 'Import Excel', _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'import', ))
        if not ok:
            return
        self.__readFromExcel(fileName)

    def __readFromExcel(self, fileName):
        '''
        Reads input from excel
        '''
        try:
            data = _pandas.read_excel(fileName)
            itemCodes = data['Item Code']
            particulars = data['Particulars']
            hsnCodes = data['HSN Code']
            quantity = data['Qty']

            for code, name, hsn, qt in zip(itemCodes, particulars, hsnCodes, quantity):
                self.__poModelData.addPurchaseOrderInfo(
                    str(code),
                    str(name),
                    str(hsn),
                    str(qt)
                )

        except Exception as ex:
            _QtGui.QMessageBox.warning(self, 'Warning', 'Not Imported properly', buttons=_QtGui.QMessageBox.Ok)
            print ex.message

    def __validateInputs(self):
        if not self.__purchaseOrderUI.poNoValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Purchase Order No must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        if not self.__purchaseOrderUI.customerNameValue.text().strip():
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Name must be entered', buttons=_QtGui.QMessageBox.Ok)
            return False

        poNos = self.__manager.fetchAllpoNo()
        if self.__purchaseOrderUI.poNoValue.text() in poNos:
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Purchase Order number is already available', buttons=_QtGui.QMessageBox.Ok)
            return False

        #TODO: validate for table items
        for poInfo in self.__poModelData.tableData:
            # if not all((poInfo.particulars.value,
            #             poInfo.hsnCode.value,
            #             poInfo.quantity.value,
            #             poInfo.itemCode.value)):
            #     _QtGui.QMessageBox.critical(self, 'ERROR', 'All table data must be entered',
            #                          buttons=_QtGui.QMessageBox.Ok)
            #     return False
            if poInfo.itemCode.value and poInfo.itemCode.value not in self.__purchaseItemInfo:
                item = self.__companyItemManager.saveCompanyItemInfo(
                    itemCode=poInfo.itemCode.value,
                    itemName=poInfo.particulars.value,
                    hsnCode=poInfo.hsnCode.value,
                    quantity=poInfo.quantity.value,
                    itemPrice=0.0)
                item.save()
                continue
            self.__particulars.append(poInfo.particulars.value)
            self.__hsnCode.append(poInfo.hsnCode.value)
            self.__quantity.append(poInfo.quantity.value)
            return True
        else:
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Table is empty',
                                 buttons=_QtGui.QMessageBox.Ok)
            return False
        return True

    utils.showWaitCursor
    def __saveToPdf(self):
        if not self.__validateInputs():
            return

        self.__manager.savePOInfo(
            self.__purchaseOrderUI.customerNameValue.text(),
            self.__purchaseOrderUI.poNoValue.text(),
            self.__purchaseOrderUI.poDateValue.date().toPython(),
            self.__purchaseOrderUI.remarksValue.toPlainText()
        )

        for itemInfo in self.__poModelData.tableData:
            if not itemInfo.itemCode.value or not itemInfo.particulars.value or not itemInfo.hsnCode.value or not itemInfo.quantity.value:
                continue
            self.__manager.savePurchaseOrderProduct(
                self.__purchaseOrderUI.poNoValue.text(),
                itemInfo.itemCode.value,
                itemInfo.particulars.value,
                itemInfo.hsnCode.value,
                itemInfo.quantity.value)
            break

        _QtGui.QMessageBox.information(self, 'Saved', 'Entered Purchase Order Value saved successfully', buttons=_QtGui.QMessageBox.Ok)
        self.__discardChanges()

    def __clearSlot(self):
        '''
        Clears table
        '''
        self.__poModelData = PurchaseOrderTableModel()
        self.__purchaseOrderUI.purchaseOrderTable.setModel(self.__poModelData)
        width = self.__purchaseOrderUI.purchaseOrderTable.horizontalHeader().size().width()

    utils.showWaitCursor
    def __discardChanges(self):
        '''
        Resets all widgets to default value
        '''
        self.__purchaseOrderUI.customerNameValue.setText('')
        self.__purchaseOrderUI.poDateValue.setDate(_QtCore.QDate.currentDate())
        self.__purchaseOrderUI.poNoValue.setText('')
        # self.__purchaseOrderUI.purchaseOrderTable.model().clearTable()
        self.__purchaseOrderUI.remarksValue.setText('')

        self.__poModelData = PurchaseOrderTableModel()
        self.__purchaseOrderUI.purchaseOrderTable.setModel(self.__poModelData)
        width = self.__purchaseOrderUI.purchaseOrderTable.horizontalHeader().size().width()

    def saveSlot(self):
        self.__saveRestore.save(_QtGui.qApp.allWidgets())

    def restoreSlot(self):
        self.__saveRestore.restore()