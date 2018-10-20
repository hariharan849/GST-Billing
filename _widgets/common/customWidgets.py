from PySide.QtGui import QComboBox, QDateEdit, QLineEdit, QPushButton
from PySide.QtCore import QDate, QAbstractTableModel, Qt

class CustomDateEdit(QDateEdit):
    def __init__(self, parent=None):
        super(CustomDateEdit, self).__init__(parent)
        self.setDate(QDate.currentDate())
        self.setCalendarPopup(True)

class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super(CustomComboBox, self).__init__(parent)

    def setComboItems(self, items):
        self.addItems(items)

class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(CustomLineEdit, self).__init__(parent)
        self.setCursorPosition(0)

class CustomPushButton(QPushButton):
    def __init__(self, parent=None):
        super(CustomPushButton, self).__init__(parent)


class TableModel(QAbstractTableModel):
    def __init__(self, headerdata, arraydata=None, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.__arraydata = arraydata if arraydata else [[]]
        self.headerdata = headerdata

    def setArrayData(self, data):
        self.__arraydata = data

    @property
    def arraydata(self, data):
        self.__arraydata = data

    @arraydata.getter
    def arraydata(self):
        return self.__arraydata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if self.arraydata:
            return len(self.arraydata[0])
        return 0

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.arraydata[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerdata[col]
        return None

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))