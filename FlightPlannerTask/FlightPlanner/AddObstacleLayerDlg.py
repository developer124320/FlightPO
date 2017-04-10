'''
Created on 23 Jan 2015

@author: Administrator
'''
from PyQt4.QtGui import QDialog, QFileDialog, QColor
from PyQt4.QtCore import Qt, QCoreApplication, QFileInfo
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry, QgsCoordinateReferenceSystem, QGis
from qgis.gui import QgsMapCanvasLayer
from FlightPlanner.ui_AddObstacleLayerDlg import Ui_AddObstacleLayerDlg
from FlightPlanner.types import SurfaceTypes
from QgisHelper import QgisHelper
from qgis.core import (QgsVectorLayer,
                        QgsMapLayerRegistry,
                        QgsCategorizedSymbolRendererV2,
                        QgsSymbolV2,
                        QgsRendererCategoryV2)

import define

class AddObstcleLayerDlg(QDialog):
    '''
    classdocsAz
    '''

    def __init__(self, parent, canvas):
        QDialog.__init__(self, parent)
        self.ui = Ui_AddObstacleLayerDlg()
        self.ui.setupUi(self)
#         self.layerSet = layerSet
        self.canvas = canvas
        self.ui.buttonBox.accepted.connect(self.verify)
#         self.ui.btnClose.clicked.connect(self.exit)
        self.ui.cmbCurrentCrs.addItem("DecimalDegree")
        self.ui.cmbCurrentCrs.addItem("Meter")
        self.ui.cmbDisplayCrs.addItem("DecimalDegree")
        self.ui.cmbDisplayCrs.addItem("Meter")
        self.ui.cmbDisplayCrs.setDisabled(True)
        self.ui.btnBrowse.clicked.connect(self.OpenObstacleFile)
        if define._units == QGis.DecimalDegrees:
            self.ui.cmbDisplayCrs.setCurrentIndex(0)
        else:
            self.ui.cmbDisplayCrs.setCurrentIndex(1)
        
    def OpenObstacleFile(self):
        filePathDir = QFileDialog.getOpenFileName(self, "Open Obstacle File",QCoreApplication.applicationDirPath (),"Obstclefiles(*.txt *.csv)")        
        if filePathDir == "":
            return
        self.ui.txtPath.setText(filePathDir)
        # define.obstaclePath = QFileInfo(filePathDir).path()
        
    def verify(self):
        if self.ui.txtPath.text() =="":
            return
        filePathDirInfo=QFileInfo(self.ui.txtPath.text())
        sName=filePathDirInfo.fileName() 
        vectorName = sName[:len(sName)-4]
        uri1 = ""
        latCrs = define._latLonCrs #QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        meterCrs = define._xyCrs # QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        if self.ui.cmbCurrentCrs.currentText() == self.ui.cmbDisplayCrs.currentText():
            if self.ui.cmbCurrentCrs.currentText() == "DecimalDegree":
                uri1 ="file:"+self.ui.txtPath.text()+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % ("\t", "Long", "Lat")
                self.AddMapLayer(uri1, vectorName, latCrs)
            else:
                uri1 ="file:"+self.ui.txtPath.text()+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:32633" % ("\t", "Long", "Lat")
                self.AddMapLayer(uri1, vectorName, meterCrs)

        else:            
            if self.ui.cmbCurrentCrs.currentText() == "DecimalDegree":
                uri1 ="file:"+self.ui.txtPath.text()+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326"% ("\t", "Long", "Lat")              
                self.AddMapLayer(uri1, vectorName, meterCrs)
            else:
                uri1 ="file:"+self.ui.txtPath.text()+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:32633" % ("\t", "Long", "Lat")
                self.AddMapLayer(uri1, vectorName, latCrs)
        
    def AddMapLayer(self, uri1, vectorName, crs):
        layer = QgsVectorLayer(uri1, vectorName, "delimitedtext") 
        
#         myTargetField = "Info"
#         myRangeList = []
#         myOpacity = 1
#         # Make our first symbol and range...
#         myMin = 0.0
#         myMax = 50.0
#         myLabel = "Windsock"
#         myColour = QColor("#ffee00")
#         mySymbol1 = QgsSymbolV2.defaultSymbol(layer.geometryType())
#         mySymbol1.setColor(myColour)
#         mySymbol1.setAlpha(myOpacity)
#         myRange1 = QgsRendererCategoryV2(myLabel,
#                                     mySymbol1,
#                                     myLabel + "aa")
#         myRangeList.append(myRange1)
#         #now make another symbol and range...
#         myMin = 50.1
#         myMax = 100
#         myLabel = "Building"
#         myColour = QColor("#00eeff")
#         mySymbol2 = QgsSymbolV2.defaultSymbol(layer.geometryType())
#         mySymbol2.setColor(myColour)
#         mySymbol2.setAlpha(myOpacity)
#         myRange2 = QgsRendererCategoryV2(myLabel,
#                                     mySymbol2,
#                                     myLabel + "dd")
#         myRangeList.append(myRange2)
#         myRenderer = QgsCategorizedSymbolRendererV2("", myRangeList)
# #         myRenderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
#         myRenderer.setClassAttribute(myTargetField)
#         layer.setRendererV2(myRenderer)
#         QgsMapLayerRegistry.instance().addMapLayer(layer)
#         
        
        
        QgisHelper.appendToCanvas(define._canvas, [layer], SurfaceTypes.Obstacles)
        self.canvas.zoomToFullExtent ()