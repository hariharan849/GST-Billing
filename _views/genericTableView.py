#!/usr/bin/env python
# companyItemTableModel.py

"""
Company item model for displaying company information
"""

import collections
import pandas


from PySide.QtGui import QTableView, QMenu, QAction, QCursor, QHeaderView, QAbstractItemView, QMessageBox
from PySide.QtCore import QEvent, Qt, Signal

class GenericTableView(QTableView):
    """ Class for implementing generic table view
    """

    removeEntry = Signal(object)
    def __init__(self, parent=None):
        super(GenericTableView, self).__init__(parent)
        self.doubleClick = False
        self.cellEditable = False
        self.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.CurrentChanged)

    def contextMenuEvent(self, event):
        '''
        Triggered on mouse right click event
        '''
        if not len(self.selectedIndexes()):
            return
        row = self.selectedIndexes()[-1].row()
        col = self.indexAt(self.parent().mapToParent(event.pos())).column()

        self.menu = QMenu(self)

        print row
        removeAction = QAction('Remove Row', self)
        removeAction.triggered.connect(lambda: self.removeSlot(row))
        self.menu.addAction(removeAction)

        clearAction = QAction('Clear Table', self)
        clearAction.triggered.connect(self.clearSlot)
        self.menu.addAction(clearAction)

        exportAction = QAction('Export to Excel', self)
        exportAction.triggered.connect(self.exportSlot)
        self.menu.addAction(exportAction)

        self.menu.popup(QCursor.pos())

    def exportSlot(self, filePath, cancelColumn=None):
        '''
        Slot for exporting to excel
        '''
        tableInformation = collections.OrderedDict()
        model = self.model()
        for row in range(model.rowCount()):
            for col, header in zip(range(model.columnCount()), model.settings):
                if cancelColumn is not None and model.index(row, cancelColumn).data():
                    continue
                elif header[1] not in tableInformation:
                    tableInformation[header[1]] = [model.index(row, col).data()]
                else:
                    tableInformation[header[1]].append(model.index(row, col).data())

        df = pandas.DataFrame(tableInformation)
        writer = pandas.ExcelWriter(filePath)
        df.to_excel(writer, 'Sheet1', index=False, index_label=False)
        writer.save()

    def clearSlot(self):
        '''
        Slot for clear event
        Clears voucher model for table.
        '''
        reply = QMessageBox.warning(self, 'Alert', 'Are You Sure To Delete all.', buttons=QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.StandardButton.No:
            return
        self.model().sourceModel().clearTable()
        self.removeEntry.emit('all')

    def removeSlot(self, row=None):
        '''
        Slot for remove event
        removes selected voucher model for table.
        '''
        result = QMessageBox.critical(self, 'ERROR', 'Are you sure to remove the selected row',
                                      buttons=QMessageBox.Ok | QMessageBox.Cancel)
        if result == QMessageBox.StandardButton.Cancel:
            return
        removeRows = []
        if row:
            self.removeEntry.emit(row)
            self.model().removeRow(row)
            removeRows.append(row)
            return
        for index in reversed(self.selectedIndexes()):
            if index.row() not in removeRows:
                self.removeEntry.emit(index.row())
                self.model().removeRow(index.row())
                removeRows.append(index.row())

    def performSingleClickEvent(self, row, column):
        '''Implemented single click event to disable copy selection
           if no cell is selected and disabling doubleclick editing and enabling
           navigationable editing.
        '''
        actions = self.contextMenu.actions()
        if len(self.selectedItems()) <= 0:
            actions[0].setEnabled(False)
        else:
            actions[0].setEnabled(True)
            self.doubleClick = False

    def performDoubleClickEvent(self):
        '''Implemented double click event to enable doubleclick editing
           and disabling navigationable editing.
        '''
        self.doubleClick = True

    def focusInEvent(self, ev):
        '''
        Extended inorder to set a cell to be not edited
        '''
        self.cellEditable = False
        return super(GenericTableView, self).focusInEvent(ev)

    def focusOutEvent(self, ev):
        '''
        Extended inorder to set a cell to be edited
        '''
        self.cellEditable = True
        return super(GenericTableView, self).focusOutEvent(ev)

    def event(self, ev):
        '''
        Reimplemented event
        '''
        if self.cellEditable and ev.type() == QEvent.KeyRelease and ev.key() in [
            Qt.Key_Left, Qt.Key_Right]:
            self.changeCell(ev)
        return super(GenericTableView, self).event(ev)

    def keyPressEvent(self, ev):
        '''
        Reimplemented key press event
        '''
        if not self.cellEditable:
            return super(GenericTableView, self).keyPressEvent(ev)
        self.changeCell(ev)

    def changeCell(self, event):
        '''
        Implemented change cell on key press event
        '''
        key = event.key()
        row = self.selectedIndexes()[0].row()
        col = self.selectedIndexes()[0].column()
        if not self.doubleClick:
            if key == Qt.Key_Left and col > 0:
                col -= 1
            elif key == Qt.Key_Right and col < self.model().columnCount(self):
                col += 1
            elif key == Qt.Key_Up and row > 0:
                row -= 1
            elif key == Qt.Key_Down and row < self.model().rowCount(self):
                row += 1
            else:
                return
        self.setCurrentIndex(self.model().index(row, col))
        if not self.doubleClick and self.model().index(row, col) and self.model().index(row, col).flags() != Qt.ItemIsEnabled:
            self.edit(self.currentIndex())
