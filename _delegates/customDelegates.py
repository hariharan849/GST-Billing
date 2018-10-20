#!/usr/bin/env python
# customDelegates.py

"""
customDelegates module for maintaining delegates used inside tableview.
"""

from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)


class DateDelegate(_QtGui.QItemDelegate):
    '''
    Creates Date item delegate in the view
    '''
    dataUpdate = _QtCore.Signal(object)
    def __init__(self, parent):
        super(DateDelegate, self).__init__(parent)
        self.__parent = parent
        self.__dateEdit = None

    def createEditor(self, parent, option, index):
        '''
        Creates editor when mouse is clicked
        '''
        dateTimeEdit = _QtGui.QDateTimeEdit(parent) #create new editor

        dateTimeEdit.setDate(_QtCore.QDate.fromString(str(index.data()), "dd - MMM - yyyy"))
        #set properties of editor
        dateTimeEdit.setDisplayFormat("dd - MMM - yyyy")
        dateTimeEdit.setCalendarPopup(True)

        dateTimeEdit.dateChanged.connect(self._datechanges)

        return dateTimeEdit

    def setModelData(self, editor, model, index):
        '''
        Sets edited data back to model
        '''
        value = editor.dateTime().toString("dd - MMM - yyyy")
        print value
        model.setData(index, value)

    def setEditorData(self, editor, index):
        '''
        Sets edited data in the view
        '''
        value = index.model().data(index, _QtCore.Qt.EditRole)
        qdate = _QtCore.QDateTime.fromString(str(value), "dd - mm - yyyy")
        editor.setDateTime(qdate)

    def paint(self, painter, option, index):
        '''
        Renders the delegate using the given painter and style option for the item specified by index
        '''
        if not self.parent().indexWidget(index):
            self.__dateEdit = _QtGui.QDateEdit(self.parent())  # create new editor
            value = index.model().data(index, _QtCore.Qt.DisplayRole)
            date = _QtCore.QDate.fromString(str(value), "dd - MMM - yyyy")
            if date == _QtCore.QDate(-4713, 1, 1):
                try:
                    date = _QtCore.QDate.fromString(str(value.split()[0]), "yyyy-MM-dd")
                except:
                    date = _QtCore.QDate.setDate(value)
            self.__dateEdit.setDate(date)
            # set properties of editor
            self.__dateEdit.setDisplayFormat("dd - MMM - yyyy")
            self.__dateEdit.setCalendarPopup(True)
            self.__dateEdit.dateChanged.connect(lambda: self.__updateDate(index))
            self.parent().setIndexWidget(
                index,
                self.__dateEdit
            )

    def __updateDate(self, index):
        self.dataUpdate.emit(index)

class ComboBoxDelegate(_QtGui.QItemDelegate):
    '''
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied
    '''
    paymentUpdate = _QtCore.Signal(object, object)
    def __init__(self, items, parent):
        super(ComboBoxDelegate, self).__init__(parent)
        self._items = items
        self.combo = None

    def paint(self, painter, option, index):
        '''
        Renders the delegate using the given painter and style option for the item specified by index
        '''
        if not self.parent().indexWidget(index):
            self.combo = _QtGui.QComboBox(self.parent())
            value = index.model().data(index, _QtCore.Qt.DisplayRole)
            self.combo.addItems(self._items)
            self.combo.currentIndexChanged.connect(lambda: self.__updateValue(index))
            itemIndex = self.combo.findText(index.data(), _QtCore.Qt.MatchFixedString)
            if itemIndex >= 0:
                self.combo.setCurrentIndex(itemIndex)
            self.parent().setIndexWidget(
                index,
                self.combo
            )

    def __updateValue(self, index):
        self.paymentUpdate.emit(self.combo.currentText(), index)

    def createEditor(self, widget, option, index):
        '''
        returns the widget used to change data from the model and can be reimplemented to customize editing behavior
        '''
        editor = _QtGui.QComboBox(widget)
        editor.addItems(self._items)
        return editor

    def setEditorData(self, editor, index):
        '''
        provides the widget with data to manipulate.
        '''
        value = index.model().data(index, _QtCore.Qt.EditRole)
        if value:
            index = editor.findText(value)
            editor.setCurrentIndex(index)

    def setModelData(self, editor, model, index):
        '''
        returns updated data to the model.
        '''
        model.setData(index, editor.currentIndex(), _QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        '''
        ensures that the editor is displayed correctly with respect to the item view.
        '''
        editor.setGeometry(option.rect)


class LineEditDelegate(_QtGui.QItemDelegate):
    '''
    A delegate that places a fully functioning lineedit in every
    cell of the column to which it's applied
    '''
    lineEditUpdate = _QtCore.Signal(object, object)
    def __init__(self, parent):
        super(LineEditDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        '''
        returns the widget used to change data from the model and can be reimplemented to customize editing behavior
        '''
        editor = _QtGui.QLineEdit(parent)
        return editor

    def setEditorData(self,editor,index):
        '''
        provides the widget with data to manipulate.
        '''
        value = index.model().data(index, _QtCore.Qt.EditRole)
        editor.setText(value)

    def setModelData(self, editor, model, index):
        '''
        returns updated data to the model.
        '''
        text=editor.text()
        model.setData(index, text)

    def paint(self, painter, option, index):
        '''
        Renders the delegate using the given painter and style option for the item specified by index
        '''
        value = index.model().data(index, _QtCore.Qt.DisplayRole)
        if not self.parent().indexWidget(index):
            lineEdit = _QtGui.QLineEdit(self.parent())
            lineEdit.setText(str(value))
            lineEdit.textChanged.connect(lambda: self.__updateValue(index))
            self.parent().setIndexWidget(
                index,
                lineEdit
            )

    def __updateValue(self, index):
        self.lineEditUpdate.emit(self.parent().indexWidget(index).text(), index)