'''
Created on Mar 18, 2015

@author: jin
'''
from FlightPlanner.helpers import Altitude, Speed, Unit
from FlightPlanner.types import SpeedUnits, AltitudeUnits
from PyQt4.QtGui import QSpacerItem, QDialog, QFrame, QSizePolicy, QLabel, QHBoxLayout, QFont, QLineEdit, QComboBox, QMessageBox
from PyQt4.QtCore import QSize, SIGNAL
from FlightPlanner.Panels.Frame import Frame

class OCAHPanel(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("OCAHPanel" + str(len(parent.findChildren(OCAHPanel))))

#         self.frame_WindIA = QFrame(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName(("frame_WindIA"))
        self.hLayout = QHBoxLayout(self)
        self.hLayout.setSpacing(0)
        self.hLayout.setMargin(0)
        self.hLayout.setObjectName(("hLayout"))

        self.basicFrame = Frame(self, "HL")
        self.basicFrame.layoutBoxPanel.setSpacing(0)
        # self.basicFrame.layoutBoxPanel.setMargin(0)
        self.hLayout.addWidget(self.basicFrame)

        self.lblIA = QLabel(self.basicFrame)
        self.lblIA.setMinimumSize(QSize(200, 0))
        self.lblIA.setMaximumSize(QSize(200, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.lblIA.setFont(font)
        self.lblIA.setObjectName(("lblIA"))
        self.basicFrame.Add = self.lblIA
        self.cmbType = QComboBox(self.basicFrame)
        self.cmbType.setMinimumSize(QSize(70, 0))
        self.cmbType.setMaximumWidth(70)
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.cmbType.setFont(font)
        self.cmbType.setObjectName(("cmbType"))
        self.basicFrame.Add = self.cmbType



        self.txtAltitudeM = QLineEdit(self.basicFrame)
        self.txtAltitudeM.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtAltitudeM.setFont(font)
        self.txtAltitudeM.setObjectName(self.objectName() + "_txtAltitudeM")
        self.txtAltitudeM.setText("0.0")
        self.txtAltitudeM.setMinimumWidth(70)
        self.txtAltitudeM.setMaximumWidth(70)
        self.basicFrame.Add = self.txtAltitudeM

        labelM = QLabel(self.basicFrame)
        labelM.setObjectName(("labelM"))
        labelM.setText(" m ")
        self.basicFrame.Add = labelM

        self.txtAltitude = QLineEdit(self.basicFrame)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtAltitude.sizePolicy().hasHeightForWidth())
        self.txtAltitude.setSizePolicy(sizePolicy)
        self.txtAltitude.setMinimumSize(QSize(70, 0))
        self.txtAltitude.setMaximumSize(QSize(70, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.txtAltitude.setFont(font)
        self.txtAltitude.setObjectName(self.objectName() + "_txtAltitude")
        self.basicFrame.Add = self.txtAltitude

        labelFt = QLabel(self.basicFrame)
        labelFt.setObjectName(("labelFt"))
        labelFt.setText(" ft")
        self.basicFrame.Add = labelFt

        spacerItem = QSpacerItem(10,10,QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout.addItem(spacerItem)
        
        self.altitude = Altitude.NaN()
        self.customValue = Speed(30).Knots
        self.cmbType.addItems(["OCA", "OCH"])
        # self.cmbType.currentIndexChanged.connect(self.changeType)
        self.cmbType.setCurrentIndex(0)
        self.lblIA.setText("Intermediate Segment Minimum:")
        # self.txtAltitude.setEnabled(False)
        self.txtAltitudeM.textChanged.connect(self.txtAltitudeMChanged)
        self.txtAltitude.textChanged.connect(self.txtAltitudeChanged)
        
        self.captionUnits = "ft"

        self.flag = 0
        self.txtAltitudeM.setText("0.0")
        self.txtAltitude.setText("0.0")
    def txtAltitudeChanged(self):
        try:
            test = float(self.txtAltitude.text())
            if self.flag==0:
                self.flag=1;
            if self.flag==2:
                self.flag=0;
            if self.flag==1:
                try:
                    self.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.txtAltitude.text())), 4)))
                except:
                    self.txtAltitudeM.setText("0.0")
                self.emit(SIGNAL("Event_0"), self)
        except:
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtAltitudeM.setText("0.0")
            self.txtAltitude.setText("0.0")


    def txtAltitudeMChanged(self):
        try:
            test = float(self.txtAltitudeM.text())
            if self.flag==0:
                self.flag=2;
            if self.flag==1:
                self.flag=0;
            if self.flag==2:
                try:
                    self.txtAltitude.setText(str(round(Unit.ConvertMeterToFeet(float(self.txtAltitudeM.text())), 4)))
                except:
                    self.txtAltitude.setText("0.0")
                self.emit(SIGNAL("Event_0"), self)
        except:
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtAltitude.setText("0.0")
            self.txtAltitudeM.setText("0.0")

        try:
            self.altitude = Altitude(float(self.txtAltitude.text()), AltitudeUnits.FT)
        except:
            self.altitude = Altitude.NaN()
    # def txtAltitudeChanged(self):
    #     try:
    #         self.altitude = Altitude(float(self.txtAltitude.text()), AltitudeUnits.FT)
    #     except:
    #         self.altitude = Altitude.NaN()
    # def setAltitude(self, value):
    #     self.altitude = value

#     def getValue(self, SpeedUnits_0 = SpeedUnits.KTS):    
#         return Speed(float(self.txtAltitude.text()), SpeedUnits_0)
    def method_2(self, altitude_0):
        altitude = Altitude(0)
        try:
            altitude = Altitude(float(self.txtAltitude.text()), AltitudeUnits.FT)
        except:
            altitude = Altitude(0)
        if (self.cmbType.currentIndex() == 0):
            return altitude
        return Altitude(altitude.Feet + altitude_0.Feet, AltitudeUnits.FT);

    def method_3(self, altitude_0):
        altitude = Altitude(0)
        try:
            altitude = Altitude(float(self.txtAltitude.text()), AltitudeUnits.FT)
        except:
            altitude = Altitude(0)
        if (self.cmbType.currentIndex() != 0):
            return altitude
        return Altitude(altitude.Feet - altitude_0.Feet, AltitudeUnits.FT);


    
    def changeType(self):
        pass
        
    # def get_altitude(self):
    #     return self.altitude
    # Value = property(get_altitude, setAltitude, None, None)

    def get_isEmpty(self):
        try:
            num = float(self.txtAltitude.text())
            return False
        except:
            return True
    IsEmpty = property(get_isEmpty, None, None, None)
    
    def get_CaptionUnits(self):
        return self.captionUnits
    def set_CaptionUnits(self, captionUnits):
        self.captionUnits = captionUnits
    CaptionUnits = property(get_CaptionUnits, set_CaptionUnits, None, None)

    def get_Caption(self):
        caption = self.lblIA.text()
        val = caption.left(caption.length() - 1)
        return val
    def set_Caption(self, captionStr):
        self.lblIA.setText(captionStr + ":")
    Caption = property(get_Caption, set_Caption, None, None)



    def get_Value(self):
        try:
            return Altitude(float(self.txtAltitudeM.text()))
        except:
            return Altitude(0.0)

    def set_Value(self, altitude):
        if isinstance(altitude, Altitude):
            if self.captionUnits == "m":
                self.txtAltitudeM.setText(str(altitude.Metres))
            else:
                self.txtAltitude.setText(str(altitude.Feet))
        else:
            str0 = "You must input the type \"Altitude\" in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtAltitudeM.setText("0.0")
    Value = property(get_Value, set_Value, None, None)

    

    def set_LabelWidth(self, width):
        self.lblIA.setMinimumSize(QSize(width, 0))
        self.lblIA.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

    def get_ReadOnly(self):
        return self.txtAltitudeM.isReadOnly()
    def set_ReadOnly(self, bool):
        self.txtAltitudeM.setReadOnly(bool)
        self.txtAltitude.setReadOnly(bool)
    ReadOnly = property(get_ReadOnly, set_ReadOnly, None, None)

    def get_Enabled(self):
        return self.txtAltitudeM.isEnabled()
    def set_Enabled(self, bool):
        self.txtAltitudeM.setEnabled(bool)
        self.txtAltitude.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)
