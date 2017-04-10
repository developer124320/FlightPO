'''
Created on Mar 18, 2015

@author: jin
'''
from FlightPlanner.helpers import Altitude, Speed
from FlightPlanner.types import SpeedUnits, AltitudeUnits
from PyQt4.QtGui import QFrame, QDialog, QSizePolicy, QLabel, QHBoxLayout, QFont, QLineEdit, QComboBox, QSpacerItem
from PyQt4.QtCore import QSize
from FlightPlanner.Panels.Frame import Frame
class WindPanel(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("WindPanel" + str(len(parent.findChildren(WindPanel))))

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

        self.comboBox = QComboBox(self.basicFrame)
        # sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        # self.comboBox.setSizePolicy(sizePolicy)
        # self.comboBox.setMinimumSize(QSize(60, 0))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName(("comboBox"))
        self.basicFrame.Add = self.comboBox

        self.speedBox = QLineEdit(self.basicFrame)
        # sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.speedBox.sizePolicy().hasHeightForWidth())
        # self.speedBox.setSizePolicy(sizePolicy)
        # self.speedBox.setMinimumSize(QSize(70, 0))
        # self.speedBox.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.speedBox.setFont(font)
        self.speedBox.setObjectName(("speedBox"))
        self.speedBox.setMinimumSize(QSize(60, 0))
        self.speedBox.setMaximumSize(QSize(60, 16777215))
        self.basicFrame.Add = self.speedBox

        spacerItem = QSpacerItem(0,0,QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.basicFrame.layoutBoxPanel.addItem(spacerItem)
        
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

    def set_LabelWidth(self, width):
        self.lblIA.setMinimumSize(QSize(width, 0))
        self.lblIA.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

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

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)