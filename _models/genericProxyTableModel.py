#!/usr/bin/env python
# genericProcyTableModel.py

"""
GenericProxyModel for tableview
"""

from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)
import re as _re


class GenericProxyModel(_QtGui.QSortFilterProxyModel):
    '''
    SortFilterProxy model for voucher information
    '''
    def __init__(self, *args, **kwargs):
        super(GenericProxyModel, self).__init__(*args, **kwargs)
        self.__fromData = None
        self.__toDate = None
        self.filters = {}

    def setFilterByColumn(self, regex, column):
        '''
        Sets regular expression filter for the specified column
        regex (re): regular expression
        column (int): column
        '''
        self.filters[column] = regex
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        '''
        Applise filter set for the above columns
        '''
        for key, regex in self.filters.items():
            ix = self.sourceModel().index(source_row, key, source_parent)
            if ix.isValid():
                text = self.sourceModel().data(ix, _QtCore.Qt.DisplayRole)
                try:
                    indexDate = _QtCore.QDate.fromString(text, "dd - MMM - yyyy")
                    fromDate = _QtCore.QDate.fromString(regex.fromDate, "dd - MMM - yyyy")
                    toDate = _QtCore.QDate.fromString(regex.toDate, "dd - MMM - yyyy")
                    if indexDate.year() == -4713:
                        indexDate = _QtCore.QDate.fromString(text, "yyyy-MM-dd")
                    return indexDate >= fromDate and indexDate <= toDate
                except Exception as ex:
                    pass
                if not _re.match(regex.pattern(), text):
                    return False
        return True


