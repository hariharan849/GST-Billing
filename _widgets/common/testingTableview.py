from customWidgets import TableModel

import sys

from PySide.QtCore import QAbstractTableModel, Qt
from PySide.QtGui import (
    QApplication,
    QTableView,
    QFileSystemModel,
    QStyledItemDelegate,
    QAbstractItemView
)


class HighlightingRowsTable(QTableView):
    def __init__(self, *args, **kw):
        super(HighlightingRowsTable, self).__init__(*args, **kw)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())
        self.selectRow(index.row())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = TableModel(['sino', 'name'], [[1, 'hari'], [2, 'sdfsdfsd']])
    hrt = HighlightingRowsTable()
    hrt.setModel(model)
    hrt.show()
app.exec_()