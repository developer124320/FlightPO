'''
Created on Mar 18, 2015

@author: jin
'''
from FlightPlanner.helpers import Altitude, Speed
from FlightPlanner.types import SpeedUnits, AltitudeUnits
from PyQt4.QtGui import QFrame, QSizePolicy, QLabel, QHBoxLayout, QFont, QLineEdit, QComboBox, QMessageBox
from PyQt4.QtCore import QSize
class WindPanel(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
#         self.frame_WindIA = QFrame(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName(("frame_WindIA"))
        self.horizontalLayout_32 = QHBoxLayout(self)
        self.horizontalLayout_32.setSpacing(0)
        self.horizontalLayout_32.setMargin(0)
        self.horizontalLayout_32.setObjectName(("horizontalLayout_32"))
        self.lblIA = QLabel(self)
        self.lblIA.setMinimumSize(QSize(140, 0))
        self.lblIA.setMaximumSize(QSize(100, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.lblIA.setFont(font)
        self.lblIA.setObjectName(("lblIA"))
        self.horizontalLayout_32.addWidget(self.lblIA)
        self.comboBox = QComboBox(self)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QSize(60, 0))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName(("comboBox"))
        self.horizontalLayout_32.addWidget(self.comboBox)
        self.speedBox = QLineEdit(self)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speedBox.sizePolicy().hasHeightForWidth())
        self.speedBox.setSizePolicy(sizePolicy)
        self.speedBox.setMinimumSize(QSize(70, 0))
        self.speedBox.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.speedBox.setFont(font)
        self.speedBox.setObjectName(("speedBox"))
        self.horizontalLayout_32.addWidget(self.speedBox)
        
        self.altitude = Altitude.NaN()
        self.customValue = Speed(30).Knots
        self.comboBox.addItems(["ICAO", "UK", "Custom"])
        self.comboBox.currentIndexChanged.connect(self.changeWindType)
        self.comboBox.setCurrentIndex(0)
        self.lblIA.setText("Wind (kts):")
        self.speedBox.setEnabled(False)
    
    def setAltitude(self, value):
        self.altitude = value
        self.method_5()
#     def getValue(self, SpeedUnits_0 = SpeedUnits.KTS):    
#         return Speed(float(self.speedBox.text()), SpeedUnits_0)
    def method_3(self, altitude_0):
        altitude = Altitude(float(self.speedBox.text()), AltitudeUnits.FT)
        if (self.comboBox.currentIndex() != 0):
            return altitude
        return Altitude(altitude.Feet - altitude_0.Feet, AltitudeUnits.FT);


    def method_5(self):
        if self.comboBox.currentIndex() == 0:
            self.speedBox.setText(str(round(Speed.smethod_1(self.altitude).Knots,1)))
        elif self.comboBox.currentIndex() == 1:
            self.speedBox.setText(str(round(Speed.smethod_2(self.altitude).Knots,1)))
        else:
            self.speedBox.setText(str(self.customValue))
        if self.comboBox.currentIndex() != 2:
            self.speedBox.setEnabled(False)
        else:
            self.speedBox.setEnabled(True)
    def changeWindType(self):
        self.method_5()
    def method_7(self, string_0):
        # object[] string0 = new object[] { string_0, this.captionLabel.Caption, this.speedBox.ToString(), this.comboBox.Items[this.comboBox.SelectedIndex] };
        return "%s%s\t%s (%s)"%(string_0, "Wind: ", self.speedBox.text(), self.comboBox.currentText());
    def get_speed(self):
        try:
            return Speed(float(self.speedBox.text()))
        except:
            return None
    Value = property(get_speed, None, None, None)

    def get_isEmpty(self):
        try:
            num = float(self.speedBox.text())
            return False
        except:
            return True
    IsEmpty = property(get_isEmpty, None, None, None)