'''
Created on 4 Jun 2014

@author: Administrator
'''
from PyQt4.QtGui import QDialog, QVBoxLayout, QTabWidget
# from PyQt4.QtCore import SIGNAL,Qt, QCoreApplication, QSize
from FlightPlanner.PdtCheckResult.tabcontrol import tabControl
from FlightPlanner.helpers import MathHelper, Speed
from FlightPlanner.types import SpeedUnits
import math
class PdtCheckResultDlg(QDialog):
    
    def __init__(self, parent, parameterList):
        QDialog.__init__(self, parent)
        self.setObjectName("PdtCheckResultDlg")
        self.setWindowTitle("PDT Check")
        self.resize(350, 400)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidgetPDT = QTabWidget(self)
        self.tabWidgetPDT.setObjectName("tabWidgetPDT")
        
        if len(parameterList) < 1:
            return
        for parameters in parameterList:            
            self.tab = tabControl(self)
            
            isaValue = parameters[1]
            altitude = parameters[2]
            iasValue = parameters[3]
            
            
            speed_1 = Speed.smethod_0(Speed(iasValue, SpeedUnits.KTS), isaValue, altitude) + Speed(25);
            straitSegment = speed_1.KilometresPerHour * 1000 / 3600 * 9
            pdtResultStr = ""
            K = round(171233 * math.pow(288 + isaValue - 0.00198 * altitude.Feet, 0.5)/(math.pow(288 - 0.00198 * altitude.Feet, 2.628)), 4)
            pdtResultStr = "1. K = \t" + str(K) + "\n"
            
            V = K * iasValue
            pdtResultStr += "2. V = \t" + str(V) + "kts\n"
            
            h = altitude.Metres
            pdtResultStr += "3. h = \t" + str(h) + "m\n" 
            
#             h = altitude.Feet / 1000
            pdtResultStr += "4. w = \t" + "46km/h\n" 
            
            num = 2313.03083707 / (3.14159265358979 * speed_1.KilometresPerHour)
            if (num > 3):
                num = 3;
            r = speed_1.KilometresPerHour / (62.8318530717959 * num) * 1000;
            pdtResultStr += "5. r = \t" + str(r/1000) + "km\n" 
            
            R = 2 * r + straitSegment
            pdtResultStr += "6. R = \t" + str(R/1000) + "km\n" 
            
#             resultStr = MathHelper.pdtCheckResultToString(parameters[1], parameters[2], parameters[3], parameters[4])
            self.tab.plainTextEdit.setPlainText(pdtResultStr)
            try:
                self.tabWidgetPDT.addTab(self.tab, parameters[0])
            except:
                self.tabWidgetPDT.addTab(self.tab, "")
            
        
#         self.tabWidgetPDT.addTab(self.tab, "A")
        self.verticalLayout.addWidget(self.tabWidgetPDT)
        
    