import decorator
import collections as _collections
import os as _os
import pandas as _pandas
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore,
    QtWebKit as _QtWebKit
)
from database import PurchaseManager, SalesManager


class PreviewDialog(_QtGui.QDialog):
    def __init__(self, parent=None, file=None):
        super(PreviewDialog, self).__init__(parent)
        self.setAttribute(_QtCore.Qt.WA_DeleteOnClose)

        previewBox = _QtWebKit.QWebView()
        previewBox.settings().setAttribute(_QtWebKit.QWebSettings.PluginsEnabled, True)
        previewBox.settings().setAttribute(_QtWebKit.QWebSettings.WebAttribute.DeveloperExtrasEnabled, True)
        previewBox.settings().setAttribute(_QtWebKit.QWebSettings.PrivateBrowsingEnabled, True)
        previewBox.settings().setAttribute(_QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
        previewBox.load(_QtCore.QUrl().fromLocalFile(file))

        layout_Main = _QtGui.QVBoxLayout()
        layout_Main.addWidget(previewBox)
        self.setLayout(layout_Main)
        self.show()

@decorator.decorator
def showWaitCursor(func, *args, **kwargs):
    '''
    Rewrites normal cursor to show wai cursor and overwrites to normal
    '''
    _QtGui.QApplication.setOverrideCursor(_QtCore.Qt.WaitCursor)
    try:
        return func(*args, **kwargs)
    finally:
        _QtGui.QApplication.restoreOverrideCursor()


def getIntegralPart(text):
    '''
    returns integral part of text
    '''
    return_str = ''
    for i, ch in enumerate(text):
        if ch.isdigit() or (i < len(text) and text[i-1].isdigit() and ch == '.'):
            return_str += ch
        continue
    return return_str


class Number2Words(object):

    def __init__(self):
        '''Initialise the class with useful data'''

        self.wordsDict = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven',
                          8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen',
                          14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen',
                          18: 'eighteen', 19: 'nineteen', 20: 'twenty', 30: 'thirty', 40: 'forty',
                          50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninty'}

        self.powerNameList = ['thousand', 'lakh', 'crore']

    def convertNumberToWords(self, number):

        # Check if there is decimal in the number. If Yes process them as paisa part.
        formString = str(number)
        if formString.find('.') != -1:
            withoutDecimal, decimalPart = formString.split('.')

            paisaPart = str(round(float(formString), 2)).split('.')[1]
            inPaisa = self._formulateDoubleDigitWords(paisaPart)

            formString, formNumber = str(withoutDecimal), int(withoutDecimal)
        else:
            # Process the number part without decimal separately
            formNumber = int(number)
            inPaisa = None

        if not formNumber:
            return 'zero'

        self._validateNumber(formString, formNumber)

        inRupees = self._convertNumberToWords(formString)

        if inPaisa:
            return 'Rs. %s and %s paisa' % (inRupees.title(), inPaisa.title())
        else:
            return 'Rs. %s' % inRupees.title()

    def _validateNumber(self, formString, formNumber):

        assert formString.isdigit()

        # Developed to provide words upto 999999999
        if formNumber > 999999999 or formNumber < 0:
            raise AssertionError('Out Of range')

    def _convertNumberToWords(self, formString):

        MSBs, hundredthPlace, teens = self._getGroupOfNumbers(formString)

        wordsList = self._convertGroupsToWords(MSBs, hundredthPlace, teens)

        return ' '.join(wordsList)

    def _getGroupOfNumbers(self, formString):

        hundredthPlace, teens = formString[-3:-2], formString[-2:]

        msbUnformattedList = list(formString[:-3])

        # ---------------------------------------------------------------------#

        MSBs = []
        tempstr = ''
        for num in msbUnformattedList[::-1]:
            tempstr = '%s%s' % (num, tempstr)
            if len(tempstr) == 2:
                MSBs.insert(0, tempstr)
                tempstr = ''
        if tempstr:
            MSBs.insert(0, tempstr)

        # ---------------------------------------------------------------------#

        return MSBs, hundredthPlace, teens

    def _convertGroupsToWords(self, MSBs, hundredthPlace, teens):

        wordList = []

        # ---------------------------------------------------------------------#
        if teens:
            teens = int(teens)
            tensUnitsInWords = self._formulateDoubleDigitWords(teens)
            if tensUnitsInWords:
                wordList.insert(0, tensUnitsInWords)

        # ---------------------------------------------------------------------#
        if hundredthPlace:
            hundredthPlace = int(hundredthPlace)
            if not hundredthPlace:
                # Might be zero. Ignore.
                pass
            else:
                hundredsInWords = '%s hundred and' % self.wordsDict[hundredthPlace]
                wordList.insert(0, hundredsInWords)

        # ---------------------------------------------------------------------#
        if MSBs:
            MSBs.reverse()

            for idx, item in enumerate(MSBs):
                inWords = self._formulateDoubleDigitWords(int(item))
                if inWords:
                    inWordsWithDenomination = '%s %s' % (inWords, self.powerNameList[idx])
                    wordList.insert(0, inWordsWithDenomination)

        # ---------------------------------------------------------------------#
        return wordList

    def _formulateDoubleDigitWords(self, doubleDigit):

        if not int(doubleDigit):
            # Might be zero. Ignore.
            return None
        elif self.wordsDict.has_key(int(doubleDigit)):
            # Global dict has the key for this number
            tensInWords = self.wordsDict[int(doubleDigit)]
            return tensInWords
        else:
            doubleDigitStr = str(doubleDigit)
            tens, units = int(doubleDigitStr[0]) * 10, int(doubleDigitStr[1])
            tensUnitsInWords = '%s %s' % (self.wordsDict[tens], self.wordsDict[units])
            return tensUnitsInWords


class CustomLabel(_QtGui.QLabel):
    '''
    Customized label for widget
    '''
    def __init__(self, name, width, height, tooltip, parent=None):
        super(CustomLabel, self).__init__(parent)
        self.setText(name)
        self.setAlignment(_QtCore.Qt.AlignCenter)
        self.setMaximumHeight(height)
        self.setMaximumWidth(width)
        self.setToolTip(tooltip)


class CustomLineEdit(_QtGui.QLineEdit):
    '''
    Customized Lineedit for widget
    '''
    def __init__(self, width, height, readOnly=False, placeHolder='', parent=None):
        super(CustomLineEdit, self).__init__(parent)
        self.setMaximumWidth(width)
        self.setMaximumHeight(height)
        self.setReadOnly(readOnly)
        self.setPlaceholderText(placeHolder)


class CustomPushButton(_QtGui.QPushButton):
    '''
    Customized pushbutton for widget
    '''
    def __init__(self, buttonName, width, height, tooltip='', parent=None):
        super(CustomPushButton, self).__init__(buttonName, parent)
        self.setMinimumWidth(width)
        self.setMinimumHeight(height)
        self.setToolTip(tooltip)

class CustomTextEdit(_QtGui.QTextEdit):
    '''
    Customized textedit for widget
    '''
    def __init__(self, width, height, readOnly=False, parent=None):
        super(CustomTextEdit, self).__init__(parent)
        self.setMaximumHeight(height)
        self.setMaximumWidth(width)
        self.setReadOnly(readOnly)


class CustomComboBox(_QtGui.QComboBox):
    '''
    Customized combobox for widget
    '''
    def __init__(self, values, parent=None):
        super(CustomComboBox, self).__init__(parent)
        self.addItems(values)

class CustomPushButton(_QtGui.QPushButton):
    '''
    Customized pushbutton for widget
    '''
    def __init__(self, buttonName, width, height, tooltip='', parent=None):
        super(CustomPushButton, self).__init__(buttonName, parent)
        self.setMinimumWidth(width)
        self.setMinimumHeight(height)
        self.setToolTip(tooltip)


class TableWidget(_QtGui.QTableWidget):
    '''
    Customized table widget to implement excel like editing
    '''
    taxUpdate = _QtCore.Signal()
    def __init__(self, parent):
        super(TableWidget, self).__init__(parent)
        self.doubleClick = False
        self.cellEditable = False

        self.setGeometry(_QtGui.QApplication.desktop().screenGeometry())
        self.__manager = None

        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setStyleSheet("QHeaderView::section{"
                           "border-left:0px solid #D8D8D8;"
                           "border-right:1px solid #D8D8D8;"
                           "border-bottom: 1px solid #D8D8D8;"
                           "background-color:#ff9999;"
                           "padding:4px;}"
                           "QHeaderView::section:checked"
                           "{background-color: blue;}")

    @staticmethod
    def getReadOnlyItem(name=None):
        '''
        returns table widget item
        '''
        text = name if name else ''
        tableItem = _QtGui.QTableWidgetItem(text)
        tableItem.setTextAlignment(_QtCore.Qt.AlignCenter)
        tableItem.setFlags(_QtCore.Qt.ItemFlags() != _QtCore.Qt.ItemIsEnabled)
        return tableItem

    def __populateRow(self, row):
        '''
        Populates the row based on information typed
        '''
        try:
            obj = self.__manager.getItemInfoByCode(self.cellWidget(row, 0).text())
            is_code = True
        except:
            return
        if not obj:
            return
        particular = _QtGui.QTableWidgetItem(obj[0].itemName)
        self.setItem(row, 1, particular)
        hsnCode = _QtGui.QTableWidgetItem(str(obj[0].hsnCode))
        self.setItem(row, 2, hsnCode)
        itemPrice = _QtGui.QTableWidgetItem(str(obj[0].itemPrice))
        self.setItem(row, 4, itemPrice)
        self.repaint()

    def _updateTaxColor(self):
        '''
        Updates color to green or red based on value
        '''
        for i in range(self.rowCount()):
            color = ('green' if self.cellWidget(i, 5).currentText() == '9' else 'blue') if  self.cellWidget(i, 5).currentText() != '0' else 'red'
            self.cellWidget(i, 5).setStyleSheet(
                'border: 2px solid {0}; border-radius: 6px; min-width: 40px; color: {0};'
                'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);'.format(color))
            color = ('green' if self.cellWidget(i, 6).currentText() == '9' else 'blue') if self.cellWidget(i,
                                                                                                           6).currentText() != '0' else 'red'
            self.cellWidget(i, 6).setStyleSheet(
                'border: 2px solid {0}; border-radius: 6px; min-width: 40px; color: {0};'
                'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);'.format(color))
            color = ('green' if self.cellWidget(i, 7).currentText() == '18' else 'blue') \
                if self.cellWidget(i, 7).currentText() != '0' else 'red'
            self.cellWidget(i, 7).setStyleSheet(
                'border: 2px solid {0}; border-radius: 6px; min-width: 40px; color: {0};'
                'background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);'.format(color))

    def __updateTax(self):
        '''
        Updates tax color and emits data to parent to update amount widget
        '''
        self.taxUpdate.emit()
        self._updateTaxColor()


    def __getItemCode(self, row):
        '''
        Returns item code line edit
        '''
        itemCodeValue = _QtGui.QLineEdit(self)
        itemCodeValue.textChanged.connect(lambda : self.__populateRow(row))
        completer = _QtGui.QCompleter()
        completer.setCompletionMode(_QtGui.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(_QtCore.Qt.CaseInsensitive)
        completer.setCompletionRole(_QtCore.Qt.EditRole)
        itemCodeValue.setCompleter(completer)
        model = _QtGui.QStandardItemModel()
        completer.setModel(model)

        completerString = [[item.itemCode, item.itemName] for item in self.__manager.fetchAllItemInfo()]
        for i, (itemCode, particular) in enumerate(completerString):
            item = _QtGui.QStandardItem(itemCode)
            item.setToolTip(particular)
            model.setItem(i, 0, item)
            item = _QtGui.QStandardItem(particular)
            item.setToolTip(particular)
            model.setItem(i, 0, item)
        return itemCodeValue

    def setTableItems(self, dbtype='purchase'):
        self.setRowCount(15)
        self.setColumnCount(11)
        headers = ['Item Code', 'Particulars', 'HSN Code', 'Qty', 'Rate', 'CGST', 'SGST', 'IGST', 'Amount', 'Tax',
                   'Total']
        self.setHorizontalHeaderLabels(headers)
        if dbtype == 'purchase':
            self.__manager = PurchaseManager()
        else:
            self.__manager = SalesManager(dbtype)
        self.__type = dbtype
        for i in range(self.rowCount()):
            self.setTableWidgets(i)

        width = self.size().width()
        self.setColumnWidth(0, width / 20)
        self.setColumnWidth(1, (width * 1.92) / 5.5)
        self.setColumnWidth(2, width / 13)
        self.setColumnWidth(3, width / 18)
        self.setColumnWidth(4, width / 18)
        self.setColumnWidth(5, width / 25)
        self.setColumnWidth(6, width / 25)
        self.setColumnWidth(7, width / 25)
        self.setColumnWidth(8, width / 18)
        self.setColumnWidth(9, width / 18)
        self.setColumnWidth(10, width / 18)

    def addRow(self):
        self.setRowCount(self.rowCount()+1)
        self.setTableWidgets(self.rowCount())

    def removeSlot(self):
        removeRows = []
        for index in reversed(self.selectedIndexes()):
            if index.row() not in removeRows:
                self.setTableWidgets(index.row())
                self.setItem(index.row(), 1, _QtGui.QTableWidgetItem(''))
                self.setItem(index.row(), 2, _QtGui.QTableWidgetItem(''))
                self.setItem(index.row(), 3, _QtGui.QTableWidgetItem(''))
                self.setItem(index.row(), 4, _QtGui.QTableWidgetItem(''))
                removeRows.append(index.row())

    def clearSlot(self):
        '''
        Clears table
        '''
        self.clear()
        self.setTableItems(self.__type)

    @showWaitCursor
    def importItems(self):
        '''
        gets company items from table
        '''
        fileName, ok = _QtGui.QFileDialog.getOpenFileName(
            self, 'Import Excel', _os.path.join(_os.path.dirname(_os.path.dirname(__file__)), 'import', ))
        if not ok:
            return
        self.__readFromExcel(fileName)

    def __readFromExcel(self, fileName):
        '''
        Reads input from excel
        '''
        try:
            data = _pandas.read_excel(fileName)
            itemCodes = data['Item Code']
            particulars = data['Particulars']
            hsnCodes = data['HSN Code']
            quantity = data['Qty']
            rates = data['Rate']
            cgstValue = data['CGST']
            sgstValue = data['SGST']
            igstValue = data['IGST']


            for code, name, hsn, qt, rate, cgst, sgst, igst in zip(itemCodes, particulars, hsnCodes, quantity, rates, cgstValue, sgstValue, igstValue):
                self.addRow()
                lastRow = self.rowCount()
                itemCodeWidget = self.cellWidget(lastRow, 0)
                itemCodeWidget.setText(code)

                self.setItem(lastRow, 0, _QtGui.QTableWidgetItem(name))
                self.setItem(lastRow, 1, _QtGui.QTableWidgetItem(hsn))
                self.setItem(lastRow, 2, _QtGui.QTableWidgetItem(qt))
                self.setItem(lastRow, 3, _QtGui.QTableWidgetItem(rate))

                cgstWidget = self.cellWidget(lastRow, 5)
                sgstWidget = self.cellWidget(lastRow, 6)
                igstWidget = self.cellWidget(lastRow, 7)
                itemIndex = cgstWidget.findText(cgst, _QtCore.Qt.MatchFixedString)
                if itemIndex >= 0:
                    cgstWidget.setCurrentIndex(itemIndex)
                itemIndex = sgstWidget.findText(sgst, _QtCore.Qt.MatchFixedString)
                if itemIndex >= 0:
                    sgstWidget.setCurrentIndex(itemIndex)
                itemIndex = igstWidget.findText(igst, _QtCore.Qt.MatchFixedString)
                if itemIndex >= 0:
                    igstWidget.setCurrentIndex(itemIndex)

                amountWithoutTax = float(qt) * float(rate)
                self.setItem(lastRow, 8, self.getReadOnlyItem(
                    str(amountWithoutTax)))
                taxValue = (amountWithoutTax * cgst) / 100.0 + (amountWithoutTax * sgst) / 100.0 + (
                        amountWithoutTax * igst) / 100.0
                self.setItem(lastRow, 9, self.getReadOnlyItem(
                    str(taxValue)))
                self.setItem(lastRow, 10, self.getReadOnlyItem(
                    str(amountWithoutTax+taxValue)))
            self.parent().populateAmountWidget()

        except Exception as ex:
            _QtGui.QMessageBox.warning(self, 'Warning', 'Not Imported properly', buttons=_QtGui.QMessageBox.Ok)
            print ex.message

    def setTableWidgets(self, row):
        self.setCellWidget(row, 0, self.__getItemCode(row))

        cgst_value = CustomComboBox(('0', '9', '14'))
        cgst_value.currentIndexChanged.connect(self.__updateTax)
        self.setCellWidget(row, 5, cgst_value)

        sgst_value = CustomComboBox(('0', '9', '14'))
        sgst_value.currentIndexChanged.connect(self.__updateTax)
        self.setCellWidget(row, 6, sgst_value)

        igst_value = CustomComboBox(('0', '18', '28'))
        igst_value.currentIndexChanged.connect(self.__updateTax)
        self.setCellWidget(row, 7, igst_value)

        self.setItem(row, 8, self.getReadOnlyItem())
        self.setItem(row, 9, self.getReadOnlyItem())
        self.setItem(row, 10, self.getReadOnlyItem())

    def performSingleClickEvent(self, row, column):
        """Implemented single click event to disable copy selection
           if no cell is selected and disabling doubleclick editing and enabling
           navigationable editing.
        """
        actions = self.contextMenu.actions()
        if len(self.selectedItems()) <= 0:
            actions[0].setEnabled(False)
        else:
            actions[0].setEnabled(True)
            self.doubleClick = False

    def performDoubleClickEvent(self):
        """Implemented double click event to enable doubleclick editing
           and disabling navigationable editing.
        """
        self.doubleClick = True

    def focusInEvent(self, ev):
        """Extended inorder to set a cell to be not edited
        """
        self.cellEditable = False
        return super(TableWidget, self).focusInEvent(ev)

    def focusOutEvent(self, ev):
        """Extended inorder to set a cell to be edited
        """
        self.cellEditable = True
        return super(TableWidget, self).focusOutEvent(ev)

    def event(self, ev):
        if self.cellEditable and ev.type() == _QtCore.QEvent.KeyRelease and ev.key() in [
            _QtCore.Qt.Key_Left, _QtCore.Qt.Key_Right]:
            self.changeCell(ev.key())
        return super(TableWidget, self).event(ev)

    def keyPressEvent(self, ev):
        if not self.cellEditable:
            return super(TableWidget, self).keyPressEvent(ev)
        self.changeCell(ev.key())

    def changeCell(self, key):
        row = self.currentRow()
        col = self.currentColumn()
        if not self.doubleClick:
            if key == _QtCore.Qt.Key_Left and col > 0:
                col -= 1
            elif key == _QtCore.Qt.Key_Right and col < self.columnCount():
                col += 1
            elif key == _QtCore.Qt.Key_Up and row > 0:
                row -= 1
            elif key == _QtCore.Qt.Key_Down and row < self.rowCount():
                row += 1
            else:
                return
        self.setCurrentCell(row, col)
        if not self.doubleClick and self.item(row, col) and self.item(row, col).flags() != _QtCore.Qt.ItemIsEnabled:
            self.edit(self.currentIndex())

    def addRow(self):
        row = self.rowCount()
        self.insertRow(row)
        self.setCellWidget(row, 0, self.__getItemCode(row))

        cgstComboValue = CustomComboBox(('0', '9', '14'))
        cgstComboValue.currentIndexChanged.connect(self.__updateTax)
        self.setCellWidget(row, 5, cgstComboValue)

        sgstComboValue = CustomComboBox(('0', '9', '14'))
        sgstComboValue.currentIndexChanged.connect(self.__updateTax)
        self.setCellWidget(row, 6, sgstComboValue)

        igstComboValue = CustomComboBox(('0', '18', '28'))
        igstComboValue.currentIndexChanged.connect(self.__updateTax)
        self.setCellWidget(row, 7, igstComboValue)

        self.setItem(row, 8, self.getReadOnlyItem())
        self.setItem(row, 9, self.getReadOnlyItem())
        self.setItem(row, 10, self.getReadOnlyItem())
        self.repaint()

    def contextMenuEvent(self, ev):
        customerMenu = _QtGui.QMenu(self)

        addRowAction = _QtGui.QAction('Add Row', self)
        addRowAction.triggered.connect(self.addRow)

        deleteRowAction = _QtGui.QAction('Remove Row', self)
        deleteRowAction.triggered.connect(lambda: self.removeRow(pos))

        customerMenu.addAction(addRowAction)
        customerMenu.addAction(deleteRowAction)

        pos = self.mapToGlobal(ev.pos())
        customerMenu.exec_(pos)

def setCompleter(widget, completionList):
    '''
    Sets completer for widget
    '''
    completer = _QtGui.QCompleter()
    completer.setCompletionMode(_QtGui.QCompleter.PopupCompletion)
    completer.setCaseSensitivity(_QtCore.Qt.CaseInsensitive)
    widget.setCompleter(completer)
    model = _QtGui.QStringListModel()
    model.setStringList(completionList)
    completer.setModel(model)
    if not completionList:
        return
    completer.setPopup(expandCompletionView(completer.popup(), completionList))

def expandCompletionView(popup, completionList):
    '''
    Increases/decreses view based on text length
    '''
    long_str = max(completionList, key=len)
    popup.setMinimumWidth(
        popup.width() - popup.viewport().width() + 2 *
        popup.frameWidth() + popup.fontMetrics().boundingRect(long_str).width())
    return popup

def toggleGroup(ctrl):
    state = ctrl.isChecked()
    if not state:
        ctrl.hide()


class StoreRestore(object):
    def __init__(self, settings):
        self._settings = settings

    def save(self, allWidgets):
        for w in allWidgets:
            mo = w.metaObject()
            if w.objectName() != "":
                name = w.objectName()
                # print name
                if isinstance(w, _QtGui.QLineEdit):
                    value = w.text()
                    self._settings.setValue(name, value)
                if isinstance(w, _QtGui.QComboBox):
                    index = w.currentIndex()
                    text = w.itemText(index)
                    self._settings.setValue(name, text)
                if isinstance(w, _QtGui.QDateEdit):
                    value = w.date()
                    self._settings.setValue(name, value)
                if isinstance(w, _QtGui.QTableView):
                    self._settings.setValue(name, w.model().tableData)
                if isinstance(w, _QtGui.QTableWidget):
                    values = []
                    for i in range(w.rowCount()):
                        tableValue = []
                        for j in range(9):
                            if j == 0:
                                tableValue.append(w.cellWidget(i, j).text())
                            elif j in [5, 6, 7]:
                                tableValue.append(w.cellWidget(i, j).currentText())
                            else:
                                tableValue.append(w.item(i, j).text() if w.item(i, j) else '')
                        values.append(tableValue)
                        self._settings.setValue(name, values)

    def restore(self):
        finfo = _QtCore.QFileInfo(self._settings.fileName())

        if finfo.exists() and finfo.isFile():
            for w in _QtGui.qApp.allWidgets():
                mo = w.metaObject()
                if w.objectName() != "":
                    name = w.objectName()
                    if isinstance(w, _QtGui.QLineEdit):

                        value = self._settings.value(name)
                        w.setText(value)
                    if isinstance(w, _QtGui.QComboBox):
                        index = w.currentIndex()
                        value = self._settings.value(name)
                        if value == '':
                            continue
                        index = w.findText(value)
                        if index == -1:
                            w.insertItems(0, [value])
                            index = w.findText(value)
                        w.setCurrentIndex(index)
                    if isinstance(w, _QtGui.QDateEdit):
                        value = self._settings.value(name)
                        self._settings.setValue(name, value)
                    if isinstance(w, _QtGui.QTableView):
                        values = self._settings.value(name)
                        rowCount = w.model().rowCount(w.model())
                        extra = len(values) - rowCount
                        if extra > 0:
                            w.model().setRowCount(rowCount+extra-1)
                            w.model().addPurchaseOrderInfo(itemCode='', particulars='', hsnCode='', quantity='')
                        for value, modelItem in zip(values, w.model().tableData):
                            modelItem.itemCode = value.itemCode
                            modelItem.particulars = value.particulars
                            modelItem.hsnCode = value.hsnCode
                            modelItem.quantity = value.quantity
                    if isinstance(w, _QtGui.QTableWidget):
                        values = self._settings.value(name)
                        rowCount = w.rowCount()
                        extra = len(values) - rowCount
                        if extra > 0:
                            w.setRowCount(len(values)+extra-1)
                            for i in range(extra):
                                w.setTableWidgets(i+rowCount)

                        for i, value in enumerate(values):
                            for j in range(len(value)):
                                if j == 0:
                                    w.cellWidget(i, j).setText(value[0])
                                elif j in [5, 6, 7]:
                                    itemIndex = w.cellWidget(i, j).findText(value[j], _QtCore.Qt.MatchFixedString)
                                    if itemIndex >= 0:
                                        w.cellWidget(i, j).setCurrentIndex(itemIndex)
                                    else:
                                        w.cellWidget(i, j).setCurrentIndex(0)
                                else:
                                    item = _QtGui.QTableWidgetItem(value[j])
                                    w.setItem(i, j, item)



def setMandLabel(objValue, mandLabel):
    if objValue.text().strip():
        mandLabel.setVisible(False)
    else:
        mandLabel.setVisible(True)

dateFilter = _collections.namedtuple('dateFilter', 'fromDate toDate')