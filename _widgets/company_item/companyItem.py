import os as _os
import pandas as _pandas
from ui.companyItemsUI import Ui_companyItem

from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
from models import CompanyItemTableModel, CompanyItemProxyModel, CompanyItemSaveWorker
from database import CompanyItemManager
from _widgets import utils


class CompanyItemWidget(_QtGui.QWidget):
    '''
    UI for company item widget
    '''
    def __init__(self, parent=None, type='sales'):
        super(CompanyItemWidget, self).__init__(parent)
        self.type = type
        self.settings = _QtCore.QSettings("company{0}item.ini".format(type), _QtCore.QSettings.IniFormat)
        self.companyItemManager = CompanyItemManager(type)
        self.__companyItemUI = Ui_companyItem()
        self.__setupWidget()
        self.__connectWidget()
        self.__addWidgetValidators()


        self.__saveRestore = utils.StoreRestore(self.settings)

        saveShortcut = _QtGui.QShortcut(_QtGui.QKeySequence("Ctrl+S"), self)
        saveShortcut.activated.connect(self.saveSlot)
        restoreShortcut = _QtGui.QShortcut(_QtGui.QKeySequence("Ctrl+R"), self)
        restoreShortcut.activated.connect(self.restoreSlot)

    def __setupWidget(self):
        '''
        Sets up widget before initializing.
        '''
        self.__companyItemUI.setupUi(self)

        self.__companyModelData = CompanyItemTableModel()
        self.__companyProxyModel = CompanyItemProxyModel()
        self.__companyProxyModel.setSourceModel(self.__companyModelData)
        self.__companyProxyModel.setDynamicSortFilter(True)
        self.__companyProxyModel.setFilterCaseSensitivity(_QtCore.Qt.CaseInsensitive)
        self.__companyItemUI.companyItemsTable.setModel(self.__companyProxyModel)

        self.__setComapanyItemInformation()

        self.__companyItemUI.inputGroupBox.setTitle(self.type.capitalize())
        self._disableAllLabels()

        self.__saveRestore = utils.StoreRestore(self.settings)

        saveShortcut = _QtGui.QShortcut(_QtGui.QKeySequence("Ctrl+S"), self)
        saveShortcut.activated.connect(self.saveSlot)
        restoreShortcut = _QtGui.QShortcut(_QtGui.QKeySequence("Ctrl+R"), self)
        restoreShortcut.activated.connect(self.restoreSlot)

    def __addWidgetValidators(self):
        '''
        Adds validators for the widgets
        '''
        self.__companyItemUI.itemPriceValue.setValidator(_QtGui.QDoubleValidator())

    def __connectWidget(self):
        '''
        Connect all widget signal and slots
        '''
        self.__companyItemUI.saveButton.clicked.connect(self.__saveChanges)
        self.__companyItemUI.discardButton.clicked.connect(self.__discardChanges)
        self.__companyItemUI.searchButton.clicked.connect(self.__searchCompanyItemInfo)
        # self.__companyItemUI.importButton.clicked.connect(self.__importItems)
        self.__companyItemUI.saveTableData.clicked.connect(self.__saveEditedChanges)
        self.__companyItemUI.companyItemsTable.removeEntry.connect(self.__removeFromDatabase)
        self.__companyItemUI.removeButton.clicked.connect(self.__companyItemUI.companyItemsTable.removeSlot)
        self.__companyItemUI.clearButton.clicked.connect(self.__companyItemUI.companyItemsTable.clearSlot)
        self.__companyItemUI.importButton.clicked.connect(self.__importItems)
        self.__companyItemUI.itemCodeValue.textChanged.connect(
            lambda: utils.setMandLabel(self.__companyItemUI.itemCodeValue, self.__companyItemUI.codeMandLabel))
        self.__companyItemUI.itemNameValue.textChanged.connect(
            lambda: utils.setMandLabel(self.__companyItemUI.itemNameValue, self.__companyItemUI.nameMandLabel))
        self.__companyItemUI.hsnCodeValue.textChanged.connect(
            lambda: utils.setMandLabel(self.__companyItemUI.hsnCodeValue, self.__companyItemUI.hsnMandLabel))
        self.__companyItemUI.quantityValue.textChanged.connect(
            lambda: utils.setMandLabel(self.__companyItemUI.quantityValue, self.__companyItemUI.quantityMandLabel))
        self.__companyItemUI.itemPriceValue.textChanged.connect(
            lambda: utils.setMandLabel(self.__companyItemUI.itemPriceValue, self.__companyItemUI.priceMandLabel))

        # self.__companyItemUI.inputGroupBox.toggled.connect(lambda: utils.toggleGroup(self.__companyItemUI.inputGroupBox))
        # self.__companyItemUI.groupBox.toggled.connect(lambda: utils.toggleGroup(self.__companyItemUI.groupBox))

    def __setComapanyItemInformation(self, companyItemInfo=None):
        '''
        Sets all Customer information
        '''
        companyItemData = self.companyItemManager.fetchAllCompanyItemInfo()
        for companyItemInfo in companyItemData:
            self.__companyModelData.addCompanyItemInfo(
                str(companyItemInfo.itemCode),
                str(companyItemInfo.itemName),
                str(companyItemInfo.hsnCode),
                str(companyItemInfo.quantity),
                str(companyItemInfo.itemPrice)
            )

    @utils.showWaitCursor
    def __importItems(self):
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
            quantity = data['Quantity']
            rates = data['Rate']

            for code, name, hsn, qt, rate in zip(itemCodes, particulars, hsnCodes, quantity, rates):

                self.companyItemManager.saveCompanyItemInfo(str(code), str(name), str(hsn), str(qt), float(rate))
                self.__companyModelData.addCompanyItemInfo(
                    str(code),
                    str(name),
                    str(hsn),
                    str(qt),
                    str(rate)
                )

        except Exception as ex:
            _QtGui.QMessageBox.warning(self, 'Warning', 'Not Imported properly', buttons=_QtGui.QMessageBox.Ok)
            print ex.message

    def __removeFromDatabase(self, row='all'):
        '''
        Removes entry from database
        '''
        if row != 'all':
            self.companyItemManager.deleteCompanyItemInfo(self.__companyProxyModel.index(row, 0).data())
            return
        self.companyItemManager.deleteCompanyItemInfo()

    @utils.showWaitCursor
    def __searchCompanyItemInfo(self):
        '''
        Search Customer
        '''
        itemName = str(self.__companyItemUI.searchNameValue.text())
        itemCode = self.__companyItemUI.searchItemCodeValue.text()
        self.__companyProxyModel.setFilterByColumn(
            _QtCore.QRegExp(itemCode, _QtCore.Qt.CaseSensitive, _QtCore.QRegExp.FixedString), 0)
        self.__companyProxyModel.setFilterByColumn(
            _QtCore.QRegExp(itemName, _QtCore.Qt.CaseSensitive, _QtCore.QRegExp.FixedString), 1)

    def __validateCompanyItems(self):
        '''
        Validates input field provided for company items
        '''
        valid = True
        if not self.__companyItemUI.itemCodeValue.text():
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Item Code must be entered', buttons=_QtGui.QMessageBoxOk)
            self.__companyItemUI.codeMandLabel.setVisible(True)
            valid = False

        if not self.__companyItemUI.itemNameValue.text():
            self.__companyItemUI.nameMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Item Name must be entered', buttons=_QtGui.QMessageBoxOk)
            valid = False

        if not self.__companyItemUI.hsnCodeValue.text():
            self.__companyItemUI.hsnMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'HSN Code must be entered', buttons=_QtGui.QMessageBoxOk)
            valid = False

        if not self.__companyItemUI.quantityValue.text():
            self.__companyItemUI.quantityMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Quantity must be entered', buttons=_QtGui.QMessageBoxOk)
            valid = False

        if not self.__companyItemUI.itemPriceValue.text():
            self.__companyItemUI.priceMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Item Price must be entered', buttons=_QtGui.QMessageBoxOk)
            valid = False

        itemCodes = self.companyItemManager.fetchAllItemCodes()
        if self.__companyItemUI.itemCodeValue.text() in  itemCodes:
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Company Item Code is already available', buttons=_QtGui.QMessageBox.Ok)
            valid = False

        return valid


    def _disableAllLabels(self):
        self.__companyItemUI.codeMandLabel.setVisible(False)
        self.__companyItemUI.nameMandLabel.setVisible(False)
        self.__companyItemUI.hsnMandLabel.setVisible(False)
        self.__companyItemUI.quantityMandLabel.setVisible(False)
        self.__companyItemUI.priceMandLabel.setVisible(False)

    @utils.showWaitCursor
    def __discardChanges(self):
        '''
        Discards all inputs to default values
        '''
        self.__companyItemUI.itemCodeValue.setText('')
        self.__companyItemUI.itemNameValue.setText('')
        self.__companyItemUI.hsnCodeValue.setText('')
        self.__companyItemUI.quantityValue.setText('')
        self.__companyItemUI.itemPriceValue.setText('')
        self._disableAllLabels()

    @utils.showWaitCursor
    def __saveChanges(self):
        '''
        Saves input company items to db
        '''
        if not self.__validateCompanyItems():
            return
        itemCode = str(self.__companyItemUI.itemCodeValue.text())
        itemName = str(self.__companyItemUI.itemNameValue.text())
        hsnCode = str(self.__companyItemUI.hsnCodeValue.text())
        quantity = str(self.__companyItemUI.quantityValue.text())
        itemPrice = float(self.__companyItemUI.itemPriceValue.text())
        self.companyItemManager.saveCompanyItemInfo(itemCode, itemName, hsnCode, quantity, itemPrice)
        self.__companyModelData.addCompanyItemInfo(
            itemCode,
            itemName,
            hsnCode,
            quantity,
            itemPrice
        )
        self.__discardChanges()

    def __saveEditedChanges(self):
        '''
        Save edited changes
        '''
        worker = CompanyItemSaveWorker(self.__companyModelData.tableData, self.type, self.companyItemManager)
        worker.start()
        _QtGui.QMessageBox.information(self, 'Saved', 'Company Item Saved Successfully.', buttons=_QtGui.QMessageBox.Ok)


    def saveSlot(self):
        self.__saveRestore.save(_QtGui.qApp.allWidgets())

    def restoreSlot(self):
        self.__saveRestore.restore()