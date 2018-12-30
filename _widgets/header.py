from sys import argv
from PySide.QtGui import QWidget, QLabel, QHBoxLayout, QApplication, QFont
from PySide.QtCore import Qt
from appSettings import CUSTOMER_NAME

class Header(QWidget):
    '''
    Header to be displayed in all widgets in main application.
    '''
    def __init__(self, parent=None):
        super(Header, self).__init__(parent)
        self.setupUI()

    def setupUI(self):
        '''
        Sets UI for header widget
        '''
        layout = QHBoxLayout(self)
        self.setTitleFont()
        appTitle = self.getAppLabel()
        layout.addWidget(appTitle)

    def setTitleFont(self):
        '''
        Sets font for the widget text
        '''
        fontValue = QFont('Times New Roman')
        fontValue.setPointSize(fontValue.pointSize() + 15)
        self.setFont(fontValue)

    def getAppLabel(self):
        '''
        Gets label to be displayed in widget
        '''
        appTitle = QLabel(CUSTOMER_NAME)
        appTitle.setAlignment(Qt.AlignCenter)
        appTitle.setFixedHeight(QApplication.desktop().screenGeometry().height() / 20)
        appTitle.setStyleSheet("border-style:ridge;border: 2px solid red; border-radius: 3px;"
                               "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #7EC0EE, stop: 1 #7EC0EE);"
                               "min-width: 40px;color: red;font-size: 54px; font-style=bold italic large 'New Century Schoolbook'")
        return appTitle

def main():
    app = QApplication(argv)
    header = Header()
    header.show()
    exit(app.exec_())


if __name__ == '__main__':
    main()
