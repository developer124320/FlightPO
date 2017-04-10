'''
Created on 17 Apr 2014

@author: Administrator
'''
from PyQt4.QtGui import QWidget, QComboBox,  QHBoxLayout, \
    QLabel, QFont, QLineEdit, QDialog, QSpacerItem, QSizePolicy
from PyQt4.QtCore import QSize
from FlightPlanner.helpers import Altitude
from FlightPlanner.types import MCAHType, AltitudeUnits
from FlightPlanner.Panels.Frame import Frame

class MCAHPanel(QWidget):
    def __init__(self, parent, altitudeUnit = AltitudeUnits.FT):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("MCAHPanel" + str(len(parent.findChildren(MCAHPanel))))

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.hLayout = QHBoxLayout(self)
        self.hLayout.setSpacing(0)
        self.hLayout.setMargin(0)
        self.hLayout.setObjectName("hLayout")
        
        self.basicFrame = Frame(self, "HL")
        self.basicFrame.Spacing = 0
        self.hLayout.addWidget(self.basicFrame)
        
        self.lblMCAH = QLabel(self.basicFrame)
        self.lblMCAH.setMinimumSize(QSize(250, 0))
        font = QFont()
        font.setWeight(50)
        font.setBold(False)
        self.lblMCAH.setFont(font)
        self.lblMCAH.setObjectName(("lblMCAH"))
        self.basicFrame.Add = self.lblMCAH
        self.cmbMCAH = QComboBox(self.basicFrame)
        font = QFont()
        font.setWeight(50)
        font.setBold(False)
        self.cmbMCAH.setFont(font)
        self.cmbMCAH.setObjectName(self.objectName() + "_cmbMCAH")
        self.basicFrame.Add = self.cmbMCAH
        self.txtMCAH = QLineEdit(self.basicFrame)
        font = QFont()
        font.setWeight(50)
        font.setBold(False)
        self.txtMCAH.setFont(font)
        self.txtMCAH.setObjectName(self.objectName() + "_txtMCAH")
        self.txtMCAH.setMinimumWidth(70)
        self.txtMCAH.setMaximumWidth(70)
        self.basicFrame.Add = self.txtMCAH
        self.setLayout(self.hLayout)

        spacerItem = QSpacerItem(0,10,QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.hLayout.addItem(spacerItem)
        self.cmbMCAH.addItems([MCAHType.MCA, MCAHType.MCH])        
#         self.txtMCAH.textChanged.connect(self.txtAltitude_TextChanged)
        self.altitudeUnit = altitudeUnit
    def setValue(self, altitude_0):
        if self.altitudeUnit == AltitudeUnits.FT:
            value1 = altitude_0.Feet
        elif self.altitudeUnit == AltitudeUnits.M:
            value1 = altitude_0.Metres
        self.txtMCAH.setText(str(value1))
    def set_Value(self, altitude_0):
        if self.altitudeUnit == AltitudeUnits.FT:
            value1 = altitude_0.Feet
        elif self.altitudeUnit == AltitudeUnits.M:
            value1 = altitude_0.Metres
        self.txtMCAH.setText(str(value1))
    def get_Value(self):
        try:
            return Altitude(float(self.txtMCAH.text()), self.altitudeUnit)
        except:
            raise UserWarning, self.lblMCAH.text() + " is invalid!"
    Value = property(get_Value, set_Value, None, None)
    
    def IsEmpty(self):
        if self.txtMCAH.text() == "":
            return True
        else:
            return False
    def method_2(self, altitude_0):
        if (self.cmbMCAH.currentIndex() == 0):
            return self.Value
        return self.Value + (altitude_0)
    def method_3(self, altitude_0):
        if (self.cmbMCAH.currentIndex() != 0):
            return self.Value
        return self.Value - (altitude_0)
