'''
Created on 4 Jun 2014

@author: Administrator
'''
from PyQt4.QtGui import QDialog, QMessageBox, QIcon, QPixmap
from PyQt4.QtCore import SIGNAL
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.MSA.ui_SplitSector import Ui_SplitSector
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.types import SelectionModeType,ConstructionType, CriticalObstacleType, ObstacleTableColumnType, OrientationType, DistanceUnits, AltitudeUnits, TurnDirection
import define, math

class SplitSectorDlg(QDialog):
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setObjectName("SplitSectorDlg")
        self.ui = Ui_SplitSector()
        self.ui.setupUi(self)
#         self.ui.txtTo.textChanged.connect(self.txtToChanged)
#         self.ui.txtRadius.textChanged.connect(self.txtRadiusChanged)
        self.numTo = 0
        self.numRadius = 0
        self.ui.btnMeasureDegreeTo.clicked.connect(self.btnMeasureDegreeTo_clicked)
        self.ui.btnMeasureRadius.clicked.connect(self.btnMeasureRadius_clicked)

        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/btnImage/dlgIcon.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        
    def btnMeasureDegreeTo_clicked(self):
        measuareBearing = CaptureBearingTool(define._canvas, self.ui.txtTo)
        define._canvas.setMapTool(measuareBearing) 
    def btnMeasureRadius_clicked(self):
        measureDistanceTool = MeasureTool(define._canvas, self.ui.txtRadius, DistanceUnits.NM)
        define._canvas.setMapTool(measureDistanceTool) 
    def txtToChanged(self):
        try:
            n = int(self.ui.txtTo.text())
            self.numTo = n
        except:
            QMessageBox.warning(self, "Warning", "Value must be type of Number.")
            self.ui.txtTo.setText(str(self.numTo))
    def txtRadiusChanged(self):
        try:
            n = int(self.ui.txtRadius.text())
            self.numRadius = n
        except:
            QMessageBox.warning(self, "Warning", "Value must be type of Number.")
            self.ui.txtRadius.setText(str(self.numRadius))