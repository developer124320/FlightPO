'''
Created on Mar 20, 2015

@author: jin
'''

from PyQt4.QtGui import QDialog, QDialogButtonBox, QFont, QMessageBox, QStandardItemModel, QPixmap, QStandardItem, QTextDocument, QPushButton, QAbstractItemView
# from PyQt4.QtCore import Qt
from FlightPlanner.Ils.ui_OasConstantsDlg import Ui_OasConstantsDlg
# from PyQt4.QtCore import SIGNAL, Qt
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.helpers import Altitude, MathHelper, Distance
from qgis.gui import QgsTextAnnotationItem, QgsAnnotationItem, QgsRubberBand
from qgis.core import QgsPoint, QGis, QgsGeometry
from FlightPlanner.types import OasCategory
import define
class OasConstantsDlg(QDialog):
    def __init__(self, parent, oasConstants_0):
        QDialog.__init__(self, parent)
        self.ui = Ui_OasConstantsDlg()
        self.ui.setupUi(self)
        
        self.ui.txtWA.setText(str(oasConstants_0.WA))
        self.ui.txtWC.setText(str(oasConstants_0.WC))
        self.ui.txtWSA.setText(str(oasConstants_0.WSA))
        self.ui.txtWSC.setText(str(oasConstants_0.WSC))
        self.ui.txtWSA.setEnabled(oasConstants_0.WSA != None)
        self.ui.txtWSC.setEnabled(oasConstants_0.WSC != None)
        self.ui.txtXA.setText(str(oasConstants_0.XA))
        self.ui.txtXB.setText(str(oasConstants_0.XB))
        self.ui.txtXC.setText(str(oasConstants_0.XC))
        self.ui.txtYA.setText(str(oasConstants_0.YA))
        self.ui.txtYB.setText(str(oasConstants_0.YB))
        self.ui.txtYC.setText(str(oasConstants_0.YC))
        self.ui.txtZA.setText(str(oasConstants_0.ZA))
        self.ui.txtZC.setText(str(oasConstants_0.ZC))
        
        self.okBtn =self.ui.buttonBox.button(QDialogButtonBox.Ok)
        self.okBtn.setEnabled(False)
        self.okBtn.clicked.connect(self.setValue)
        
        self.ui.txtWA.textChanged.connect(self.enableOkBtn)
        self.ui.txtWC.textChanged.connect(self.enableOkBtn)
        self.ui.txtWSA.textChanged.connect(self.enableOkBtn)
        self.ui.txtWSC.textChanged.connect(self.enableOkBtn)        
        self.ui.txtXA.textChanged.connect(self.enableOkBtn)
        self.ui.txtXB.textChanged.connect(self.enableOkBtn)
        self.ui.txtXC.textChanged.connect(self.enableOkBtn)
        self.ui.txtYA.textChanged.connect(self.enableOkBtn)
        self.ui.txtYB.textChanged.connect(self.enableOkBtn)
        self.ui.txtYC.textChanged.connect(self.enableOkBtn)
        self.ui.txtZA.textChanged.connect(self.enableOkBtn)
        self.ui.txtZC.textChanged.connect(self.enableOkBtn)
    def enableOkBtn(self):
        self.okBtn.setEnabled(True)
    def setValue(self):
        self.WA = float(self.ui.txtWA.text())
        self.WC = float(self.ui.txtWC.text())
        if self.ui.txtWSA.isEnabled():
            self.WSA = float(self.ui.txtWSA.text())
        else:
            self.WSA = None
        if self.ui.txtWSC.isEnabled():
            self.WSC = float(self.ui.txtWSA.text())
        else:
            self.WSC = None
        self.XA = float(self.ui.txtXA.text())
        self.XB = float(self.ui.txtXB.text())
        self.XC = float(self.ui.txtXC.text())
        self.YA = float(self.ui.txtYA.text())
        self.YB = float(self.ui.txtYB.text())
        self.YC = float(self.ui.txtYC.text())
        self.ZA = float(self.ui.txtZA.text())
        self.ZC = float(self.ui.txtZC.text())
        QDialog.accept(self)