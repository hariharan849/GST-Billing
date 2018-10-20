# -*- coding: utf-8 -*-
'''
User Interface for customer.
'''

from database import CustomerNames, CustomerManager
from delegates import customDelegates as _customDelegates
from models import constants, CustomerTableModel, CustomerProxyModel, CustomerSaveWorker
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
from ui.addCustomerUI import Ui_addCustomer

from _widgets import utils

class CustomerWidget(_QtGui.QWidget):
    '''
    UI for credit voucher widget
    '''
    def __init__(self, parent=None):
        super(CustomerWidget, self).__init__(parent)
        self.__customerUI = Ui_addCustomer()
        self.customerManager = CustomerManager()
        self.__setupWidget()
        self.__connectWidget()
        self.__addWidgetValidators()

    def __setupWidget(self):
        '''
        Sets up widget before initializing.
        '''
        self.__customerUI.setupUi(self)

        self.__customerModelData = CustomerTableModel()
        self.__customerProxyModel = CustomerProxyModel()
        self.__customerProxyModel.setSourceModel(self.__customerModelData)
        self.__customerProxyModel.setDynamicSortFilter(True)
        self.__customerProxyModel.setFilterCaseSensitivity(_QtCore.Qt.CaseInsensitive)
        self.__customerUI.customerTable.setModel(self.__customerProxyModel)

        self.__setCustomerInformation()

        self._disableAllLabels()
        self.showMaximized()

    def __connectWidget(self):
        '''
        Connect all widget signal and slots
        '''
        self.__customerUI.saveButton.clicked.connect(self.__saveChanges)
        self.__customerUI.discardButton.clicked.connect(self.__discardChanges)
        self.__customerUI.searchButton.clicked.connect(self.__searchCustomerInfo)
        self.__customerUI.tableSaveButton.clicked.connect(self.__saveEditedChanges)
        self.__customerUI.customerTable.removeEntry.connect(self.__removeFromDatabase)
        self.__customerUI.removeButton.clicked.connect(self.__customerUI.customerTable.removeSlot)
        self.__customerUI.clearButton.clicked.connect(self.__customerUI.customerTable.clearSlot)
        self.__customerUI.importButton.clicked.connect(self.__customerUI.customerTable.importSlot)


    def _disableAllLabels(self):
        self.__customerUI.codeMandLabel.setVisible(False)
        self.__customerUI.nameMandLabel.setVisible(False)
        self.__customerUI.gstinMandLabel.setVisible(False)
        self.__customerUI.addressMandLabel.setVisible(False)
        self.__customerUI.stateMandLabel.setVisible(False)
        self.__customerUI.contactMandLabel.setVisible(False)

    def __setCustomerInformation(self, customerInfo=None):
        '''
        Sets all Customer information
        '''
        customerData = self.customerManager.fetchAllCustomerInfo()
        for customerInfo in customerData:
            self.__customerModelData.addCustomerInfo(
                str(customerInfo.custCode),
                str(customerInfo.custName),
                str(customerInfo.custAddress),
                str(customerInfo.gstin),
                str(customerInfo.stateCode),
                str(customerInfo.contactNo)
            )

    def __removeFromDatabase(self, customerId='all'):
        '''
        Removes entry from database
        '''
        if customerId != 'all':
            self.customerManager.deleteCustomerInfo(self.__customerProxyModel.index(customerId, 0).data())
            return
        self.customerManager.deleteCustomerInfo()

    @utils.showWaitCursor
    def __searchCustomerInfo(self):
        '''
        Search Customer
        '''
        customerName = str(self.__customerUI.searchNameValue.text())
        gstinValue = self.__customerUI.searchGstinValue.text()
        self.__customerProxyModel.setFilterByColumn(
            _QtCore.QRegExp(customerName, _QtCore.Qt.CaseInsensitive, _QtCore.QRegExp.FixedString), 1)
        self.__customerProxyModel.setFilterByColumn(
            _QtCore.QRegExp(gstinValue, _QtCore.Qt.CaseInsensitive, _QtCore.QRegExp.FixedString), 2)

    def __validateCustomerInputs(self):
        '''
        Validates mandatory field.
        '''
        valid = True
        if not self.__customerUI.customerCodeValue.text():
            self.__customerUI.codeMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Name must be entered', buttons=_QtGui.QMessageBox.Ok)
            valid = False
        if not self.__customerUI.customerNameValue.text():
            self.__customerUI.nameMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Name must be entered', buttons=_QtGui.QMessageBox.Ok)
            valid = False
        if not self.__customerUI.customerAddressValue.text():
            self.__customerUI.addressMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Address is not entered.', buttons=_QtGui.QMessageBox.Ok)
            valid = False
        if not self.__customerUI.customerGstinValue.text():
            self.__customerUI.gstinMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Gstin must be entered', buttons=_QtGui.QMessageBox.Ok)
            valid = False
        if not self.__customerUI.stateCodeValue.text():
            self.__customerUI.stateMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'State Code must be entered', buttons=_QtGui.QMessageBox.Ok)
            valid = False
        if not self.__customerUI.contactNoValue.text():
            self.__customerUI.contactMandLabel.setVisible(True)
            # _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Phone no must be entered', buttons=_QtGui.QMessageBox.Ok)
            valid = False
        if len(self.__customerUI.contactNoValue.text()) != 10:
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Contact no is invalid', buttons=_QtGui.QMessageBox.Ok)
            valid = False
        customerCodes = self.customerManager.fetchAllItemCodes()
        if self.__customerUI.customerCodeValue.text() in customerCodes:
            _QtGui.QMessageBox.critical(self, 'ERROR', 'Customer Code is already available',
                                        buttons=_QtGui.QMessageBox.Ok)
            valid = False
        return valid

    def __addWidgetValidators(self):
        '''
        Adds validators for the widgets
        '''
        self.__customerUI.stateCodeValue.setValidator(_QtGui.QIntValidator())
        # self.__customerUI.contactNoValue.setValidator(_QtGui.QIntValidatorValidator())

    @utils.showWaitCursor
    def __discardChanges(self):
        '''
        Discards all field changes
        '''
        self.__customerUI.customerCodeValue.setText('')
        self.__customerUI.customerNameValue.setText('')
        self.__customerUI.customerAddressValue.setText('')
        self.__customerUI.customerGstinValue.setText('')
        self.__customerUI.stateCodeValue.setText('')
        self.__customerUI.contactNoValue.setText('')
        self._disableAllLabels()

    @utils.showWaitCursor
    def __saveChanges(self):
        '''
        Saves customer data to database.
        '''
        if not self.__validateCustomerInputs():
            return
        custCode = str(self.__customerUI.customerCodeValue.text())
        custName = str(self.__customerUI.customerNameValue.text()).capitalize()
        custAddress = str(self.__customerUI.customerAddressValue.text())
        gstinText = str(self.__customerUI.customerGstinValue.text())
        stateCode = int(self.__customerUI.stateCodeValue.text())
        contactNo = str(self.__customerUI.contactNoValue.text())

        args = (custCode, custName, custAddress, gstinText, stateCode, contactNo)
        self.customerManager.saveCustomerInfo(*args)
        self.__customerModelData.addCustomerInfo(
            custCode,
            custName,
            custAddress,
            gstinText,
            str(stateCode),
            contactNo
        )
        self.__discardChanges()

    @utils.showWaitCursor
    def __saveEditedChanges(self):
        '''
        Save edited changes
        '''
        worker = CustomerSaveWorker(self.__customerModelData.tableData, self.customerManager)
        worker.start()
        _QtGui.QMessageBox.information(self, 'Saved', 'Customer Details Saved Successfully.', buttons=_QtGui.QMessageBox.Ok)
