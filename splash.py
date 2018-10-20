# from PySide.QtCore import *
# from PySide.QtGui import *
# import time
#
#
# class Form(QDialog):
#     """ Just a simple dialog with a couple of widgets
#     """
#
#     def __init__(self, parent=None):
#         super(Form, self).__init__(parent)
#         self.browser = QTextBrowser()
#         self.setWindowTitle('Just a dialog')
#         self.lineedit = QLineEdit("Write something and press Enter")
#         self.lineedit.selectAll()
#         layout = QVBoxLayout()
#         layout.addWidget(self.browser)
#         layout.addWidget(self.lineedit)
#         self.setLayout(layout)
#         self.lineedit.setFocus()
#         self.connect(self.lineedit, SIGNAL("returnPressed()"),
#                      self.update_ui)
#
#     def update_ui(self):
#         self.browser.append(self.lineedit.text())
#
#
# if __name__ == "__main__":
#     import sys, time
#
#     app = QApplication(sys.argv)
#
#     # Create and display the splash screen
#     splash_pix = QPixmap(r'E:\deploy\logos\lokri.png')
#
#     splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
#     splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
#     splash.setEnabled(False)
#     # splash = QSplashScreen(splash_pix)
#     # adding progress bar
#     progressBar = QProgressBar(splash)
#     progressBar.setMaximum(10)
#     progressBar.setGeometry(0, splash_pix.height() - 50, splash_pix.width(), 20)
#
#     # splash.setMask(splash_pix.mask())
#
#     splash.show()
#     splash.showMessage("<h1><font color='green'>GST Application</font></h1>", Qt.AlignTop | Qt.AlignCenter, Qt.black)
#
#     for i in range(1, 11):
#         progressBar.setValue(i)
#         t = time.time()
#         while time.time() < t + 0.1:
#             app.processEvents()
#
#     # Simulate something that takes time
#     time.sleep(1)
#
#     form = Form()
#     form.show()
#     splash.finish(form)
#     sys.exit(app.exec_())
from PySide.QtCore import *
from PySide.QtGui import *

class SplashScreen(QSplashScreen):
    """
    Class implementing a splashscreen for eric6.
    """

    def __init__(self):
        """
        Constructor
        """
        ericPic = QPixmap(r'E:\deploy\logos\lokriLauch.png')
        self.labelAlignment = Qt.Alignment(
            Qt.AlignBottom | Qt.AlignRight | Qt.AlignAbsolute)
        super(SplashScreen, self).__init__(ericPic)
        lblVersion = QLabel(self)
        lblVersion.setText('GST 1.0')
        lblVersion.adjustSize()
        lblVersion.setStyleSheet("QLabel { color : white; }")
        lblVersion.setAttribute(Qt.WA_TranslucentBackground)
        lblVersion.move(425 - lblVersion.width(), 195)
        self.show()
        self.raise_()  # needed for mac
        QApplication.flush()

    def showMessage(self, msg):
        """
        Public method to show a message in the bottom part of the splashscreen.

        @param msg message to be shown (string)
        """
        super(SplashScreen, self).showMessage(
            msg, self.labelAlignment, QColor(Qt.white))
        QApplication.processEvents()

    def clearMessage(self):
        """
        Public method to clear the message shown.
        """
        super(SplashScreen, self).clearMessage()
        QApplication.processEvents()

if __name__ == '__main__':
    import sys, time

    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.showMessage(QCoreApplication.translate("Lokri", "Starting..."))
    time.sleep(2)
    splash.showMessage(QCoreApplication.translate("Lokri", "Launching GST..."))
    time.sleep(2)

    sys.exit(app.exec_())
