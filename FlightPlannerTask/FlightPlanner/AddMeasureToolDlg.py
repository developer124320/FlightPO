'''
Created on 25 Jan 2015

@author: Administrator
'''
from FlightPlanner.ui_QgsMeasureLine import Ui_MeasureDialog
from qgis.core import QgsDistanceArea, QGis
from qgis.gui import QgsMapTool, QgsRubberBand
# from PyQt4.QtCore import Qt, QObject
from PyQt4.QtGui import QDialog, QFont
from PyQt4.QtCore import Qt, QCoreApplication, QFileInfo
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.helpers import Unit
from FlightPlanner.types import DistanceUnits
class AddMeasureToolDlg(QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent, canvas):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self.ui = Ui_MeasureDialog()
        self.ui.setupUi(self)
#         self.layerSet = layerSet
        self.canvas = canvas
        self.ui.cmbMeasureType.addItems(["M", "FT", "KM", "NM"])   
        self.setFont(QFont("Arial"))             
        self.ui.btnNew.clicked.connect(self.Measure)
        self.ui.btnClose.clicked.connect(self.exit)
        self.ui.cmbMeasureType.currentIndexChanged.connect(self.changeType)
        self.measureType = DistanceUnits.M
        self.toolCaptureCoord = MeasureTool(self.canvas, self.ui.txtToal, self.measureType)
    def Measure(self):
        self.measureType = self.ui.cmbMeasureType.currentIndex()
        self.toolCaptureCoord = MeasureTool(self.canvas, self.ui.txtToal, self.measureType)
        self.canvas.setMapTool(self.toolCaptureCoord)
#         if self.btnCaptureCoord.isChecked():
#             self.iface.mapCanvas().setMapTool(self.toolCaptureCoord)
#         else:   
    def exit(self):
#         self.toolCaptureCoord.deactivate()
#         self.toolCaptureCoord.restart()    
        self.toolCaptureCoord.rubberBand.reset(QGis.Line)    
        self.canvas.unsetMapTool (self.toolCaptureCoord)
        self.reject() 
    def changeType(self):
        
        if self.ui.txtToal != "" and self.ui.cmbMeasureType.currentIndex() != self.measureType:
            if self.measureType == DistanceUnits.M:
                if self.ui.cmbMeasureType.currentIndex() == DistanceUnits.FT:
                    dist = float(self.ui.txtToal.text())
                    self.ui.txtToal.setText(str(Unit.ConvertMeterToFeet(dist)))
                elif self.ui.cmbMeasureType.currentIndex() == DistanceUnits.KM:
                    dist = float(self.ui.txtToal.text())
                    self.ui.txtToal.setText(str(dist / 1000.0))
                elif self.ui.cmbMeasureType.currentIndex() == DistanceUnits.NM:
                    dist = float(self.ui.txtToal.text())
                    self.ui.txtToal.setText(str(Unit.ConvertMeterToNM(dist)))
            elif self.measureType == DistanceUnits.FT:
                if self.ui.cmbMeasureType.currentIndex() == DistanceUnits.M:
                    dist = float(self.ui.txtToal.text())
                    self.ui.txtToal.setText(str(Unit.ConvertFeetToMeter(dist)))
                elif self.ui.cmbMeasureType.currentIndex() == DistanceUnits.KM:
                    dist = float(self.ui.txtToal.text())
                    self.ui.txtToal.setText(str(Unit.ConvertFeetToMeter(dist) / 1000.0))
                elif self.ui.cmbMeasureType.currentIndex() == DistanceUnits.NM:
                    dist = float(self.ui.txtToal.text())
                    self.ui.txtToal.setText(str(Unit.ConvertFeetToNM(dist)))
            elif self.measureType == DistanceUnits.KM:
                if self.ui.cmbMeasureType.currentIndex() == DistanceUnits.M:
                    dist = float(self.ui.txtToal.text())
                    self.ui.txtToal.setText(str(Unit.ConvertKMToMeters(dist)))
                elif self.ui.cmbMeasureType.currentIndex() == DistanceUnits.FT:
                    dist = float(self.ui.txtToal.text())
                    self.ui.txtToal.setText(str(Unit.ConvertKMToFeet(dist)))
                elif self.ui.cmbMeasureType.currentIndex() == DistanceUnits.NM:
                    dist = float(self.ui.txtToal.text())
                    self.ui.txtToal.setText(str(Unit.ConvertKMToNM(dist)))
            elif self.measureType == DistanceUnits.NM:
                if self.ui.cmbMeasureType.currentIndex() == DistanceUnits.M:
                    dist = float(self.ui.txtToal.text())
                    self.ui.txtToal.setText(str(Unit.ConvertNMToMeter(dist)))
                elif self.ui.cmbMeasureType.currentIndex() == DistanceUnits.FT:
                    dist = float(self.ui.txtToal.text())
                    self.ui.txtToal.setText(str(Unit.ConvertMeterToFeet(Unit.ConvertNMToMeter(dist))))
                elif self.ui.cmbMeasureType.currentIndex() == DistanceUnits.KM:
                    dist = float(self.ui.txtToal.text())
                    self.ui.txtToal.setText(str(Unit.ConvertNMToMeter(dist) / 1000.0))
                                                                                              
        self.measureType = self.ui.cmbMeasureType.currentIndex()    