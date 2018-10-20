#!/usr/bin/env python
# quotationreportTableView.py

"""
quotationreportView for displaying quotation report model information
"""

from PySide.QtGui import QAbstractItemView

import genericTableView as _genericTableView

class ItemReportTable(_genericTableView.GenericTableView):
    '''
    Quotation table view for displaying model
    '''
    def __init__(self, parent=None):
        super(ItemReportTable, self).__init__(parent)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
