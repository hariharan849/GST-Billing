
from database import CustomerManager

from PySide.QtGui import QDialog, QMessageBox
from ui.customerDialogUI import Ui_Dialog

class CustomerDialog(QDialog):
    def __init__(self, name, address, gstin='', state='', parent=None):
        super(CustomerDialog, self).__init__(parent)
        self.__customerUIDialog = Ui_Dialog()
        self.__setupWidgets(name, address, gstin, state)
        self.__customerManager = CustomerManager()

    def __setupWidgets(self, name, address, gstin, state):
        self.__customerUIDialog.setupUi(self)

        if name:
            self.__customerUIDialog.nameValue.setText(name)
        if address:
            self.__customerUIDialog.addressValue.setText(address)
        if gstin:
            self.__customerUIDialog.gstinValue.setText(gstin)
        if state:
            self.__customerUIDialog.stateValue.setText(state)

        self.setFixedWidth(500)
        self.setWindowTitle('New Customer')

        self.show()

        self.__customerUIDialog.saveButton.accepted.connect(self.__saveCustomerChanges)
        self.__customerUIDialog.saveButton.rejected.connect(self.__closeWidget)

    def __validateCustomerInfo(self):
        '''
        Validates mandatory field.
        '''
        if not self.__customerUIDialog.nameValue.text():
            QMessageBox.critical(self, 'ERROR', 'Customer Name must be entered', buttons=QMessageBox.Ok)
            return False
        if not self.__customerUIDialog.addressValue.text():
            QMessageBox.critical(self, 'ERROR', 'Customer Address must be entered', buttons=QMessageBox.Ok)
            return False
        if not self.__customerUIDialog.gstinValue.text():
            QMessageBox.critical(self, 'ERROR', 'Customer GSTIN must be entered', buttons=QMessageBox.Ok)
            return False
        if not self.__customerUIDialog.stateValue.text():
            QMessageBox.critical(self, 'ERROR', 'Customer State Code must be entered', buttons=QMessageBox.Ok)
            return False
        if not self.__customerUIDialog.contactNoValue.text():
            QMessageBox.critical(self, 'ERROR', 'Customer ContactNo must be entered', buttons=QMessageBox.Ok)
            return False
        return True

    def __saveCustomerChanges(self):
        if not self.__validateCustomerInfo():
            return
        custCode = max(self.__customerManager.fetchAllItemCodes())
        args = (custCode,
                self.__customerUIDialog.nameValue.text(),
                self.__customerUIDialog.addressValue.text(),
                self.__customerUIDialog.gstinValue.text(),
                int(self.__customerUIDialog.stateValue.text()),
                int(self.__customerUIDialog.contactNoValue.text())
        )
        self.__customerManager.saveCustomerInfo(*args)
        self.close()

    def __closeWidget(self):
        self.close()


def main():
    from PySide.QtGui import QApplication
    from sys import argv, exit
    app = QApplication(argv)
    ex = CustomerDialog('hariharan', 'sssffrsf')
    exit(app.exec_())


if __name__ == '__main__':
    main()