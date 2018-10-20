#!/usr/bin/env python
# abstractTableModel.py

"""
GenericModel for tableview in pyside
"""

from PySide import QtCore as _QtCore
import constants as _constants


class GenericTableModel(_QtCore.QAbstractTableModel):
    '''
    Inherited from QAbstractTablemodel to customize in the child class
    '''
    def __init__(self, tableData, settings, parent=None):
        super(GenericTableModel, self).__init__(parent)
        self.__tableData = tableData
        self.__settings = settings

    @property
    def settings(self):
        return self.__settings

    @property
    def tableData(self):
        '''
        returns model information
        '''
        return self.__tableData

    def rowCount(self, parent):
        '''
        Returns row count of the model
        '''
        return len(self.__tableData)

    def columnCount(self, parent):
        '''
        Returns column count of the model
        '''
        return len(self.__settings)

    def flags(self, index):
        '''
        Sets flags for the cell
        '''
        return _QtCore.Qt.ItemIsEditable | _QtCore.Qt.ItemIsEnabled | _QtCore.Qt.ItemIsSelectable

    def data(self, index, role):
        '''
        Returns data for the specified role
        '''
        row = index.row()
        column = index.column()
        if role in (_QtCore.Qt.EditRole, _QtCore.Qt.ToolTipRole, _QtCore.Qt.DisplayRole):
            return self._getData(row, column).value

    def setData(self, index, value, role=_QtCore.Qt.EditRole):
        '''
        Sets data for the specified cell upon edit
        '''
        if role == _QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            if index.data() == value:
                return False
            setattr(self.__tableData[row], self.__settings[column][_constants._columnId], _constants.valueWrapper(value, True))
            return True
        return False

    def headerData(self, section, orientation, role):
        '''
        Sets header data to the table
        '''
        if role == _QtCore.Qt.DisplayRole:
            if orientation == _QtCore.Qt.Horizontal:
                if section < len(self.__settings):
                    return self._getColumnHeader(section)
                else:
                    return "not implemented"
            else:
                return section

    def _getColumnHeader(self, row):
        '''
        Return header data for specified row
        '''
        return self.__settings[row][_constants._columnName]

    def _getData(self, row, column):
        '''
        Gets data for the specified row, column from wrapper class
        '''
        return getattr(self.__tableData[row], self.__settings[column][_constants._columnId])

    def _setData(self, row, column, value):
        '''
        Gets data for the specified row, column from wrapper class
        '''
        return setattr(self.__tableData[row], self.__settings[column][_constants._columnId], _constants.valueWrapper(value, True))

    def insertRows(self, position, rows, parent=_QtCore.QModelIndex()):
        '''
        Insert rows from the table
        '''
        self.beginInsertRows(parent, position, position + len(rows) - 1)

        for i in rows:
            self.__tableData.insert(position, i)

        self.endInsertRows()

        return True

    def removeRows(self, position, rows, parent=_QtCore.QModelIndex()):
        '''
        Removes rows from the table
        '''
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            self.__tableData.pop(position)

        self.endRemoveRows()

        return True

    def sort(self, Ncol, order):
        self.layoutAboutToBeChanged.emit()
        import operator
        self.__tableData = sorted(self.__tableData, key=operator.itemgetter(Ncol))
        if order == _QtCore.Qt.DescendingOrder:
            self.__tableData.reverse()
        self.layoutChanged.emit()