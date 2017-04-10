# -*- coding: UTF-8 -*-


from PyQt4.QtGui import QDialog, QMessageBox, QStandardItemModel, QTextDocument,\
        QStandardItem, QProgressBar, QFileDialog, QFont, QPushButton, QLineEdit, QComboBox
from PyQt4.QtCore import Qt, QSizeF, QVariant, QCoreApplication, SIGNAL
# from PyQt4.QtCore import Qt
from FlightPlanner.ExportDlg.ui_ExportDlg import Ui_ExportDlg
import define

import math
import sys

class ExportDlg(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.ui = Ui_ExportDlg()
        self.ui.setupUi(self)
        self.ui.chbLimit.setChecked(True)
        self.resultHideColumnIndexs = []
        self.ui.frame.setVisible(False)
        self.ui.frame_2.setVisible(False)
#         self.ui.buttonBox.setVisible(False)
        self.ui.buttonBox.accepted.connect(self.acceptEvent)
        self.ui.buttonBox.rejected.connect(self.reject)
    def acceptEvent(self):
        m = QStandardItem()
#         m.checkState().it()
        model = self.ui.listColumns.model()
        columnCount = model.rowCount()
        if columnCount > 0:
            for i in range(columnCount):
                if model.item(i, 0).checkState() == Qt.Unchecked:
                    self.resultHideColumnIndexs.append(i)
        self.accept()