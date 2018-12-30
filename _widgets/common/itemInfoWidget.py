from ui.itemInfoUI import Ui_itemInfoWidget
from models import ItemTableModel, ItemTableProxyModel
from PySide import (
    QtGui as _QtGui,
    QtCore as _QtCore
)

class ItemInfoWidget(_QtGui.QWidget):
    '''
    UI for company item widget
    '''
    def __init__(self, billNo, databaseInfo, headerSettings, remarks='', parent=None):
        super(ItemInfoWidget, self).__init__(parent)
        self.__itemInfoUI = Ui_itemInfoWidget()
        self.__billNo = billNo
        self.__headerSettings = headerSettings
        self.__databaseInfo = databaseInfo
        self.__remarks = remarks
        self._setupUI()
        self.connectWidgets()
        self.setWindowTitle('Items for bill no:' + str(self.__billNo))
        # self.setWindowFlags(_QtCore.Qt.WindowStaysOnTopHint)
        # self.showMaximized()
        self.setWindowFlags(_QtCore.Qt.Window | _QtCore.Qt.WindowMinimizeButtonHint | _QtCore.Qt.WindowCloseButtonHint)
        self.show()

    def _setupUI(self):
        self.__itemInfoUI.setupUi(self)
        self.__itemModelData = ItemTableModel(self.__headerSettings)
        self.__itemProxyModel = ItemTableProxyModel()
        self.__itemProxyModel.setSourceModel(self.__itemModelData)
        self.__itemInfoUI.itemTable.setModel(self.__itemProxyModel)

        print dir(self.__databaseInfo)
        for itemInfo in self.__databaseInfo:
            itemDetails = self.parent().addItemInfo(
                itemInfo
            )
            self.__itemModelData.addItemInfo(itemDetails)

        self.__itemInfoUI.remarksValue.setText(self.__remarks)

    def connectWidgets(self):
        self.__itemInfoUI.searchButton.clicked.connect(self.__searchNames)

    def __searchNames(self):
        itemName = self.__itemInfoUI.itemNameValue.text()
        if not itemName:
            _QtGui.QMessageBox.critical(self, 'Error', 'Item Name must be entered.',
                                        buttons=_QtGui.QMessageBox.Ok)
        self.__itemProxyModel.setFilterByColumn(
            _QtCore.QRegExp(itemName, _QtCore.Qt.CaseInsensitive, _QtCore.QRegExp.FixedString), 1)