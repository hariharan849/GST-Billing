import os as _os
import sys as _sys
_sys.path.append(_os.path.dirname(__file__))
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
from ui import (
    launcherUI as _launcherUI,
    homePage as _homePage
)
from widgets import (VoucherWidget, CompanyItemWidget, CustomerWidget, InvoiceChart, ParticularsChart, QuotationWidget,
                     QuotationReportWidget, PurchaseOrderWidget, PurchaseReportWidget,
                     PurchaseInvoiceWidget, PurchaseReport, SalesInvoiceWidget, SalesReport, PerformaInvoiceWidget)
from database import SalesInvoice, PurchaseInvoice

_LAUNCHER = 'laucherUI.ui'


from PySide.QtCore import QTimeLine
from PySide.QtGui import *


class SplashScreen(_QtGui.QSplashScreen):
    """
    Class implementing a splashscreen for eric6.
    """

    def __init__(self):
        """
        Constructor
        """
        # launchIcon = _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'logos', 'launchIcon.png')
        launchIcon = _os.path.join(_os.path.dirname(__file__), 'logos', 'lokriLauch.png')
        print launchIcon
        ericPic = _QtGui.QPixmap(launchIcon)
        self.labelAlignment = _QtCore.Qt.Alignment(
            _QtCore.Qt.AlignBottom | _QtCore.Qt.AlignRight | _QtCore.Qt.AlignAbsolute)
        super(SplashScreen, self).__init__(ericPic)
        lblVersion = QLabel(self)
        lblVersion.setText('GST 1.0')
        lblVersion.adjustSize()
        lblVersion.setStyleSheet("QLabel { color : white; }")
        lblVersion.setAttribute(_QtCore.Qt.WA_TranslucentBackground)
        lblVersion.move(425 - lblVersion.width(), 195)
        self.show()
        self.raise_()  # needed for mac
        _QtGui.QApplication.flush()

    def showMessage(self, msg):
        """
        Public method to show a message in the bottom part of the splashscreen.

        @param msg message to be shown (string)
        """
        super(SplashScreen, self).showMessage(
            msg, self.labelAlignment, QColor(_QtCore.Qt.white))
        QApplication.processEvents()

    def clearMessage(self):
        """
        Public method to clear the message shown.
        """
        super(SplashScreen, self).clearMessage()
        QApplication.processEvents()

class FaderWidget(QWidget):

    def __init__(self, old_widget, new_widget):
        QWidget.__init__(self, new_widget)

        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(333)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()



class Launcher(_QtGui.QMainWindow):
    '''
    Create launcher main window for the application
    '''
    def __init__(self, *args, **kwargs):
        super(Launcher, self).__init__(*args, **kwargs)

        self.__launcherUI = _launcherUI.Ui_MainWindow()
        self._setUpApplication()

    def _setUpApplication(self):
        '''
        Sets up initial UI in the application
        '''
        self.__launcherUI.setupUi(self)

        class HomeWidget(_QtGui.QWidget, _homePage.Ui_applicationHome):
            def __init__(self, *args, **kwargs):
                super(HomeWidget, self).__init__(*args, **kwargs)
                self.setupUi(self)

        homePage = HomeWidget()
        self.setCentralWidget(homePage)
        self.key_list = []
        self.first_release = False
        self.__setUpActionMenus()
        self.setWindowTitle('GST Application')
        self.showMaximized()

    def _setWidgetInCentral(self, widget):
        self.setWindowOpacity(0.8)
        _QtCore.QTimer.singleShot(500, lambda: self.setWindowOpacity(1))
        self.setCentralWidget(widget)

    def unfade(self):
       self.setWindowOpacity(1)

    def __createVoucherWidget(self, type):
        '''
        Creates Voucher widget on action of debit/credit voucher
        '''
        self._setWidgetInCentral(VoucherWidget(self, type))
        # self.setCentralWidget(widget)

    def __createCompanyItemWidget(self, type):
        '''
        Creates Voucher widget on action of debit/credit voucher
        '''
        widget = CompanyItemWidget(self, type)
        self.setCentralWidget(widget)

    def __createCustomerWidget(self):
        '''
        Creates Customer widget
        '''
        widget = CustomerWidget(self)
        self.setCentralWidget(widget)

    def __createInvoiceChart(self, type='sales'):
        '''
        Create chart for invoice
        '''
        db = SalesInvoice if type == 'sales' else PurchaseInvoice
        widget = InvoiceChart(db)
        self.setCentralWidget(widget)

    def __createQuotationReportWidget(self):
        '''
        Create quotation report widget
        '''
        widget = QuotationReportWidget(self)
        self.setCentralWidget(widget)

    def __createQuotationWidget(self):
        '''
        Create quotation widget
        '''
        widget = QuotationWidget(self)
        self.setCentralWidget(widget)

    def __createPOWidget(self):
        '''
        Create Purchase order
        '''
        widget = PurchaseOrderWidget(self)
        self.setCentralWidget(widget)

    def __createPOReportWidget(self):
        '''
        Create Purchase order
        '''
        widget = PurchaseReportWidget(self)
        self.setCentralWidget(widget)

    def __createPurchaseReportWidget(self):
        '''
        Create Purchase order
        '''
        widget = PurchaseReport(self)
        self.setCentralWidget(widget)

    def __createPurchaseInvoiceWidget(self):
        '''
        Create Purchase order
        '''
        widget = PurchaseInvoiceWidget(self)
        self.setCentralWidget(widget)

    def __createIllegalSalesWidget(self):
        '''
        Create Purchase order
        '''
        widget = SalesInvoiceWidget('illegal', self)
        self.setCentralWidget(widget)

    def __createIllaegalSalesReportWidget(self):
        '''
        Create Purchase order
        '''
        widget = SalesReport('illegal', self)
        self.setCentralWidget(widget)

    def __createSalesWidget(self):
        '''
        Create Purchase order
        '''
        widget = SalesInvoiceWidget('sales', self)
        self.setCentralWidget(widget)

    def __createSalesReportWidget(self):
        '''
        Create Purchase order
        '''
        widget = SalesReport(parent=self)
        self.setCentralWidget(widget)

    def __createPerformaWidget(self):
        widget = PerformaInvoiceWidget('performa', self)
        self.setCentralWidget(widget)

    def __createPerformaReportWidget(self):
        '''
        Create Purchase order
        '''
        widget = SalesReport('performa', self)
        self.setCentralWidget(widget)

    def __createInvoiceItemChart(self, type='sales'):
        '''
        Create invoice item chart
        '''
        db = SalesInvoice if type == 'sales' else SalesInvoice
        widget = ParticularsChart(db)
        self.setCentralWidget(widget)

    def __setUpActionMenus(self):
        '''
        Sets up action slot connection for the application
        '''
        self.__launcherUI.actionCredit_Voucher.triggered.connect(lambda: self.__createVoucherWidget('credit'))
        self.__launcherUI.actionDebit_Voucher.triggered.connect(lambda: self.__createVoucherWidget('debit'))

        self.__launcherUI.actionSales_Item.triggered.connect(lambda: self.__createCompanyItemWidget('sales'))
        self.__launcherUI.actionPurchase_Item.triggered.connect(lambda: self.__createCompanyItemWidget('purchase'))

        self.__launcherUI.actionCustomer_Details.triggered.connect(self.__createCustomerWidget)

        self.__launcherUI.actionSales_Chart.triggered.connect(lambda :self.__createInvoiceChart('sales'))
        self.__launcherUI.actionPurchase_Chart.triggered.connect(lambda :self.__createInvoiceChart('purchase'))

        self.__launcherUI.actionSaled_Item.triggered.connect(lambda: self.__createInvoiceItemChart('sales'))
        self.__launcherUI.actionPurchased_Item.triggered.connect(lambda: self.__createInvoiceItemChart('purchase'))

        self.__launcherUI.actionCreate_Quotation.triggered.connect(self.__createQuotationWidget)
        self.__launcherUI.actionQuotation_Report.triggered.connect(self.__createQuotationReportWidget)

        self.__launcherUI.actionCreate_Purchase_Order.triggered.connect(self.__createPOWidget)
        self.__launcherUI.actionPurchase_Order_Report.triggered.connect(self.__createPOReportWidget)

        self.__launcherUI.actionPurchase_Invoice.triggered.connect(self.__createPurchaseInvoiceWidget)
        self.__launcherUI.actionPurchase_Report.triggered.connect(self.__createPurchaseReportWidget)

        self.__launcherUI.actionSales_Invoice.triggered.connect(self.__createSalesWidget)
        self.__launcherUI.actionSales_Report.triggered.connect(self.__createSalesReportWidget)

        self.__launcherUI.actionPerforma_Invoice.triggered.connect(self.__createPerformaWidget)
        self.__launcherUI.actionPerforma_Report.triggered.connect(self.__createPerformaReportWidget)

    def keyPressEvent(self, ev):
        self.first_release = True
        self.key_list.append(str(ev.key()))

    def keyReleaseEvent(self, ev):
        if self.first_release:
            self.process_multiple_keys()
        self.first_release = False
        if self.key_list:
            del self.key_list[-1]
            self.key_list = []

    def process_multiple_keys(self):
        if not hasattr(self, 'key_list'):
            return
        if len(self.key_list) != 2:
            return
        if ' '.join(self.key_list) == '16777251 66':

            self.__createIllegalSalesWidget()
        elif ' '.join(self.key_list) == '16777251 82':
            self.__createIllaegalSalesReportWidget()


def main():
    import time
    app = _QtGui.QApplication(_sys.argv)
    try:
        splash = SplashScreen()
        splash.show()
        splash.showMessage(_QtCore.QCoreApplication.translate("Lokri", "Starting..."))
        time.sleep(2)
        splash.showMessage(_QtCore.QCoreApplication.translate("Lokri", "Launching GST..."))
        time.sleep(2)

        widget = Launcher()
        widget.show()
        styleFile = _os.path.join(_os.path.dirname(__file__), 'styleSheet', 'QTDark.stylesheet')
        print styleFile, _os.path.dirname(__file__)
        with open(styleFile, "r") as fh:
            app.setStyleSheet(fh.read())
    except Exception as ex:
        errorFile = _os.path.join(_os.path.dirname(__file__), 'error.txt')
        with open(styleFile, "w") as fh:
            fh.write(ex.message)
    _sys.exit(app.exec_())


if __name__ == '__main__':
    main()
