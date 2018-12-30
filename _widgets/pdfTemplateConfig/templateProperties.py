
from os.path import join, dirname

from PySide.QtGui import QWidget, QMessageBox
from json import dump
from ui.templatePropertiesUI import Ui_Form

class TemplateProperties(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(TemplateProperties, self).__init__(parent)
        self.setupUi(self)
        self.__connectWidget()

    def __connectWidget(self):
        '''
        Connect all widget signal and slots
        '''
        self.saveButton.clicked.connect(self.__createJsonFile)
        self.discardButton.clicked.connect(self.__discardChanges)

    def __createJsonFile(self):
        '''
        Converts input to json file
        '''
        with open(join(dirname(dirname(dirname(__file__))), 'template.json'), 'w') as file_obj:
            dump(
                {'address1':[
                             str(self.address1RowValue.text()),
                             str(self.address1ColValue.text()),
                             str(self.address1Value.text())],
                 'address2':[
                             str(self.address2RowValue.text()),
                             str(self.address2ColValue.text()),
                             str(self.address2Value.text())],
                 'phoneNo': str(self.contactNoValue.text()),
                 'companyName': str(self.customerNameValue.text()),
                 'gstin': str(self.customerGstinValue.text()),
                 'stateCode': str(self.stateCodeValue.text()),
                 'companyData':[str(self.customerRowValue.text()),
                                str(self.customerColValue.text())],
                 'companyTag': str(self.companyTagValue.text()),
                 'tagData':[str(self.companyRowValue.text()),
                            str(self.companyColValue.text())],
                 'dcData':[str(self.dcRowValue.text()),
                           str(self.dcColValue.text())],
                 'bankCustomerName': str(self.bankCustomerNameValue.text()),
                 'bankBranchName': str(self.bankBranchNameValue.text()),
                 'accountNo': str(self.bankAccountValue.text()),
                 'ifscCode': str(self.bankIfscValue.text()),
                 'stateName': str(self.bankStateNameValue.text()),
                 'billStart': str(self.billNoValue.text()),
                 'performaBillStart': str(self.performaBillNoValue.text()),
                 'bankFont': int(self.bankFontSizeValue.text())},
            file_obj)
        QMessageBox.information(self, 'Updated', 'Json Created Successfully',
                                buttons=QMessageBox.Ok)
        self.parent().close()

    def __discardChanges(self):
        '''
        Sets default value
        '''
        self.customerNameValue.setText('')
        self.customerRowValue.setText('150')
        self.customerColValue.setText('735')
        self.companyTagValue.setText('')
        self.companyRowValue.setText('175')
        self.companyColValue.setText('718')
        self.address1Value.setText('')
        self.address1RowValue.setText('40')
        self.address1ColValue.setText('703')
        self.address2Value.setText('')
        self.address2RowValue.setText('75')
        self.address2ColValue.setText('693')
        self.bankCustomerNameValue.setText('')
        self.bankBranchNameValue.setText('')
        self.bankAccountValue.setText('')
        self.bankIfscValue.setText('')
        self.bankStateNameValue.setText('')
        self.bankFontSizeValue.setText('')
        self.billNoValue.setText('')
        self.performaBillNoValue.setText('')
        self.customerGstinValue.setText('')
        self.contactNoValue.setText('')
        self.stateCodeValue.setText('')
        self.dcRowValue.setText('180')
        self.dcColValue.setText('725')


# def main():
#     app = QApplication(argv)
#     customerWidget = TemplateProperties()
#     customerWidget.show()
#     styleFile = join(
#         r"E:\darshan_auto_cable\stylesheet\darkorange-pyside-stylesheet-master\darkorange\darkorange.qss")
#     with open(styleFile, "r") as fh:
#         app.setStyleSheet(fh.read())
#     exit(app.exec_())
#
# if __name__ == '__main__':
#     main()
