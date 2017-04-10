'''
Created on Apr 3, 2015

@author: jin
'''
from PyQt4.QtGui import QDialog, QIcon, QPixmap

from FlightPlanner.RnpAR.ui_RnpRegDlg import Ui_RnpRegDialog

from FlightPlanner.types import RnpArLegType, RnpArSegmentType, DistanceUnits, AltitudeUnits
from FlightPlanner.helpers import Speed, Altitude, Unit, Distance, MathHelper
from FlightPlanner.Captions import Captions
import math
class RnpArLegDlg(QDialog):
    
    def __init__(self, parent, rnpArDataGroup_0, rnpArLeg_0, altitude_0 = None, bool_0 = None):
        QDialog.__init__(self, parent)
        self.ui = Ui_RnpRegDialog()
        self.ui.setupUi(self)
#         self.ui.frame_Wind.hide()
        self.ui.btnAltitude.hide()
        
        self.group = rnpArDataGroup_0
        self.leg = rnpArLeg_0
        self.ui.txtRnpValue.setText(str(rnpArLeg_0.Rnp))
        if rnpArLeg_0.Altitude.IsValid():
            self.ui.txtAltitude.setText(str(round(rnpArLeg_0.Altitude.Feet, 2)))# + Unit.ConvertMeterToFeet(parent.pnlLTP.Point3d.get_Z()), 2)))
        self.ui.txtAltitude.setDisabled(rnpArLeg_0.IsFAP)
        
        if rnpArLeg_0.Wind.IsValid():
            self.ui.txtWind.setText(str(round(rnpArLeg_0.Wind.Knots,1)))
        
        if rnpArLeg_0.Radius.IsValid():
            self.ui.txtRadius.setText(str(round(rnpArLeg_0.Radius.Metres, 2)))
        
        if rnpArLeg_0.Bank != None:
            self.ui.txtBank.setText(str(round(rnpArLeg_0.Bank, 2)))
            
        self.ui.chbIsFap.setChecked(rnpArLeg_0.IsFAP)
        
        if altitude_0 == None and bool_0 == None:
            self.ui.chbIsFap.setEnabled(rnpArLeg_0.Segment == RnpArSegmentType.Final)
            self.ui.chbIsFap.setVisible(self.ui.chbIsFap.isEnabled())
            if (rnpArLeg_0.Type != RnpArLegType.TF):
                if (not rnpArLeg_0.IsFAP):
                    self.setWindowTitle(Captions.RF_LEG)
                else:
                    self.setWindowTitle(Captions.RF_LEG + " - " + Captions.FAP)
                if (not rnpArLeg_0.Wind.IsValid()):
                    self.method_5()
                self.ui.txtBank.setDisabled(True)
                self.method_4()
            else:                
                if (not rnpArLeg_0.IsFAP):
                    self.setWindowTitle(Captions.TF_LEG)
                else:
                    self.setWindowTitle(Captions.TF_LEG +" - "+ Captions.FAP)
                if (self.ui.txtBank.text() == ""):
                    self.ui.txtBank.setText(str(18))
                if (not rnpArLeg_0.Wind.IsValid()):
                    self.method_5()
                self.ui.frame_R.setVisible(False)
                self.ui.txtR.setEnabled(False)
                self.ui.frame_Radius.setVisible(False)
                self.ui.txtRadius.setEnabled(False)
        else:
            self.calculatedAltitude = altitude_0
            self.ui.btnAltitude.setVisible(True)
            if rnpArLeg_0.Segment != RnpArSegmentType.Final:
                self.ui.chbIsFap.setVisible(False)
            else:
                self.ui.chbIsFap.setVisible(bool_0)                
        
            if (rnpArLeg_0.Type != RnpArLegType.TF):
                self.setWindowTitle(Captions.RF_LEG)
                if (self.leg.Wind.IsValid()):
                    self.method_5()
                #self.ui.txtBank.setDisabled(True)
                self.method_4()
            else:
                self.setWindowTitle(Captions.TF_LEG)
               
                if (self.ui.txtBank.text() == ""):
                    self.ui.txtBank.setText(str(18))
                if (self.leg.Wind == None):
                    self.method_5()
                self.ui.frame_R.setVisible(False)
                self.ui.txtR.setEnabled(False)
                self.ui.frame_Radius.setVisible(False)
                self.ui.txtRadius.setEnabled(False)
        
        self.ui.txtAltitude.textChanged.connect(self.method_6)
        self.ui.btnAltitude.clicked.connect(self.method_8)
        self.ui.txtBank.textChanged.connect(self.txtBankChanged)
        self.ui.txtWind.textChanged.connect(self.method_7)
        self.ui.buttonBox.accepted.connect(self.OK)

        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/btnImage/dlgIcon.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        
    def txtBankChanged(self):
        pass
        
    def method_4(self):
        aSFA = None
        if (self.leg.Type == RnpArLegType.RF):
            if (self.ui.txtAltitude.text() != "" and self.ui.txtWind.text() != ""):
                if (self.leg.Segment == RnpArSegmentType.Final):
                    aSFA = self.group.IAS_FA;
                elif (self.leg.Segment != RnpArSegmentType.Initial):
                    if self.leg.Segment != RnpArSegmentType.Intermediate:
                        aSFA = self.group.IAS_MA
                    else:
                        aSFA = self.group.IAS_I
                else:
                    aSFA = self.group.IAS_IA
                    
                try:
                    altitude = Altitude(float(self.ui.txtAltitude.text()), AltitudeUnits.FT)
                except ValueError:
                    raise UserWarning, "Altitude Value is invalid!"
                speed = Speed.plus(Speed.smethod_0(aSFA, self.group.ISA, altitude) , Speed(float(self.ui.txtWind.text())))
                num = math.pow(speed.Knots, 2)
                value = Distance(float(self.ui.txtRadius.text()), DistanceUnits.M) 
                num1 = Unit.smethod_1(math.atan(num / (68625 * value.NauticalMiles)))
                num2 = 3431 * math.tan(Unit.ConvertDegToRad(num1)) / (3.14159265358979 * speed.Knots)
                self.ui.txtBank.setText(str(round(num1, 2)))
                self.ui.txtR.setText(str(round(num2, 2)))
                return
            self.ui.txtBank.setText("")
            self.ui.txtR.setText("")
    def method_5(self):
        self.ui.txtWind.setText(str(round((Speed.smethod_3(Altitude(float(self.ui.txtAltitude.text()), AltitudeUnits.FT), self.group.AerodromeElevation)).Knots, 1)))
    
    def method_6(self):
        self.method_5()
        self.method_4()
    
    def method_7(self):
        self.method_4()
    
    def method_8(self):        
        self.ui.txtAltitude.setText(str(round(MathHelper.smethod_0(self.calculatedAltitude.Feet, -2), 2)))
        self.method_5()
        self.method_4()
        
    def OK(self):
        self.leg.Rnp = float(self.ui.txtRnpValue.text())
        self.leg.Altitude = Altitude(float(self.ui.txtAltitude.text()), AltitudeUnits.FT)
        self.leg.Bank = float(self.ui.txtBank.text())
        self.leg.Wind = Speed(float(self.ui.txtWind.text()))
        
        if (self.ui.chbIsFap.isEnabled()):
            self.leg.IsFAP = self.ui.chbIsFap.isChecked()
                    
    