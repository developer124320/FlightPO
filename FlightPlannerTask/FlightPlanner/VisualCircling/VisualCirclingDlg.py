# -*- coding: UTF-8 -*-
'''
Created on 30 Jun 2015

@author: Administrator
'''
from PyQt4.QtGui import QStandardItemModel, QSizePolicy, QSpinBox, QLabel, QFileDialog, QFrame, QLineEdit, QHBoxLayout, QFont, QStandardItem, QSpacerItem
from PyQt4.QtCore import SIGNAL,Qt, QCoreApplication, QSize
from PyQt4.QtGui import QColor
from qgis.gui import QgsMapTool, QgsRubberBand


from qgis.gui import QgsMapToolPan
from qgis.core import QGis

from FlightPlanner.types import SelectionModeType,ConstructionType, CriticalObstacleType, ObstacleTableColumnType, OrientationType, DistanceUnits, AltitudeUnits, TurnDirection
from FlightPlanner.captureCoordinateTool import CaptureCoordinateToolUpdate
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
# 
from FlightPlanner.Captions import Captions
from FlightPlanner.QgisHelper import QgisHelper, Geo
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.VisualCircling.ui_VisualCircling import Ui_VisualCircling

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import AircraftSpeedCategory, AltitudeUnits, SpeedUnits, \
                Point3D, SurfaceTypes
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.helpers import Distance, Speed, Altitude,  MathHelper, Unit
from FlightPlanner.messages import Messages
from FlightPlanner.PdtCheckResult.PdtCheckResultDlg import PdtCheckResultDlg
from Type.Degrees import Degrees, DegreesType
import define

class VisualCirclingDlg(FlightPlanBaseDlg):
        
    def __init__(self, parent):
        '''
        Constructor
        '''
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("VisualCircling")
        self.surfaceType = SurfaceTypes.VisualCircling
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.VisualCircling)
                
        self.resize(600, 650)
        QgisHelper.matchingDialogSize(self, 1260, 700)
        # self.layers = []
        self.accepted.connect(self.closed)
        self.rejected.connect(self.closed)
        # self.resultLayers = []
        self.manualPolygon = None
        self.mapToolPan = None
        self.toolSelectByPolygon = None
#         self.rejected.connect(self.closeEvent)
        define._mLayerTreeView.currentLayerChanged.connect(self.currentLayerChangedMethod)
#         self.connect(define._mLayerTreeView, SIGNAL("currentLayerChanged(QgsMapLayer *layer)"), self.currentLayerChanged)
#     def closeEvent(self):
#         self.reject()
    
    def closed(self):
        if self.mapToolPan != None:
            self.mapToolPan.deactivate()
        if self.toolSelectByPolygon != None:
            self.toolSelectByPolygon.deactivate()
        define._mLayerTreeView.currentLayerChanged.disconnect(self.currentLayerChangedMethod)
    def currentLayerChangedMethod(self, mapLayer):
        define._selectedLayerName = mapLayer.name()
    def changeResultUnit(self):
        if self.newDlgExisting:
            if len(self.visualCirclingAreas) <= 0:
                return FlightPlanBaseDlg.setResultPanel(self)
            
            surfaceCount = len(self.visualCirclingAreas)
            
            self.ui.txtOCH.setText(self.visualCirclingAreas[0].Category)
            ochResults = self.obstaclesModel.method_12(self.visualCirclingAreas[0].Category, self.ui.cmbUnits.currentIndex())
            self.ui.txtOCHResults.setText(ochResults)
            
            if surfaceCount > 1:
                self.ui.txtOCA.setText(self.visualCirclingAreas[1].Category)
                ocaResults = self.obstaclesModel.method_12(self.visualCirclingAreas[1].Category, self.ui.cmbUnits.currentIndex())
                self.ui.txtOCAResults.setText(ocaResults)
                self.ui.frame_114.setVisible(True)
                
            if surfaceCount > 2:
                self.ui.txtIAWP3.setText(self.visualCirclingAreas[2].Category)
                iawp3Results = self.obstaclesModel.method_12(self.visualCirclingAreas[2].Category, self.ui.cmbUnits.currentIndex())
                self.ui.txtIAWP3Results.setText(iawp3Results)  
                self.ui.frame_IAWP3.setVisible(True)      
            
            if surfaceCount > 3:
                self.ui.txtIAWP4.setText(self.visualCirclingAreas[3].Category)
                iawp4Results = self.obstaclesModel.method_12(self.visualCirclingAreas[3].Category, self.ui.cmbUnits.currentIndex())
                self.ui.txtIAWP4Results.setText(iawp4Results)
                self.ui.frame_IAWP4.setVisible(True)
            if surfaceCount > 4:
                self.ui.txtIAWP5.setText(self.visualCirclingAreas[4].Category)
                iawp5Results = self.obstaclesModel.method_12(self.visualCirclingAreas[4].Category, self.ui.cmbUnits.currentIndex())
                self.ui.txtIAWP5Results.setText(iawp5Results)
                self.ui.frame_IAWP5.setVisible(True)
            if surfaceCount > 5:
                self.ui.txtIAWP6.setText(self.visualCirclingAreas[5].Category)
                iawp6Results = self.obstaclesModel.method_12(self.visualCirclingAreas[5].Category, self.ui.cmbUnits.currentIndex())
                self.ui.txtIAWP6Results.setText(iawp6Results)
                self.ui.frame_IAWP6.setVisible(True)
        return FlightPlanBaseDlg.changeResultUnit(self)


    def initObstaclesModel(self):
        ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = VisualCirclingObstacles(self.visualCirclingAreas, Altitude(float(self.parametersPanel.txtAdElevation.text()), AltitudeUnits.M), self.manualPolygon)
        return FlightPlanBaseDlg.initObstaclesModel(self)


    def initSurfaceCombo(self):
        self.ui.cmbObstSurface.addItem("All")
        for visualCirclingArea in self.visualCirclingAreas:
            self.ui.cmbObstSurface.addItem(visualCirclingArea.Category)   
        return FlightPlanBaseDlg.initSurfaceCombo(self)
    
    def setResultPanel(self):
        self.newDlgExisting = True
        if len(self.visualCirclingAreas) <= 0:
            return FlightPlanBaseDlg.setResultPanel(self)
        
        surfaceCount = len(self.visualCirclingAreas)
        
        self.ui.txtOCH.setText(self.visualCirclingAreas[0].Category)
        ochResults = self.obstaclesModel.method_12(self.visualCirclingAreas[0].Category, self.ui.cmbUnits.currentIndex())
        self.ui.txtOCHResults.setText(ochResults)
        
        if surfaceCount > 1:
            self.ui.txtOCA.setText(self.visualCirclingAreas[1].Category)
            ocaResults = self.obstaclesModel.method_12(self.visualCirclingAreas[1].Category, self.ui.cmbUnits.currentIndex())
            self.ui.txtOCAResults.setText(ocaResults)
            self.ui.frame_114.setVisible(True)
            
        if surfaceCount > 2:
            self.ui.txtIAWP3.setText(self.visualCirclingAreas[2].Category)
            iawp3Results = self.obstaclesModel.method_12(self.visualCirclingAreas[2].Category, self.ui.cmbUnits.currentIndex())
            self.ui.txtIAWP3Results.setText(iawp3Results)  
            self.ui.frame_IAWP3.setVisible(True)      
        
        if surfaceCount > 3:
            self.ui.txtIAWP4.setText(self.visualCirclingAreas[3].Category)
            iawp4Results = self.obstaclesModel.method_12(self.visualCirclingAreas[3].Category, self.ui.cmbUnits.currentIndex())
            self.ui.txtIAWP4Results.setText(iawp4Results)
            self.ui.frame_IAWP4.setVisible(True)
        if surfaceCount > 4:
            self.ui.txtIAWP5.setText(self.visualCirclingAreas[4].Category)
            iawp5Results = self.obstaclesModel.method_12(self.visualCirclingAreas[4].Category, self.ui.cmbUnits.currentIndex())
            self.ui.txtIAWP5Results.setText(iawp5Results)
            self.ui.frame_IAWP5.setVisible(True)
        if surfaceCount > 5:
            self.ui.txtIAWP6.setText(self.visualCirclingAreas[5].Category)
            iawp6Results = self.obstaclesModel.method_12(self.visualCirclingAreas[5].Category, self.ui.cmbUnits.currentIndex())
            self.ui.txtIAWP6Results.setText(iawp6Results)
            self.ui.frame_IAWP6.setVisible(True)
            
        return FlightPlanBaseDlg.setResultPanel(self)
    
    def visualCirclingRadiusComparer(self,a, b):
        if (a.Radius.Metres < b.Radius.Metres):
            return -1;
        if (a.Radius.Metres > b.Radius.Metres):
            return 1;
        return 0;
    def btnEvaluate_Click(self):
        self.ui.frame_114.hide()
        self.ui.frame_IAWP3.hide()
        self.ui.frame_IAWP4.hide()
        self.ui.frame_IAWP5.hide()
        self.ui.frame_IAWP6.hide()
         
        self.visualCirclingAreas = self.method_39();
        self.visualCirclingAreas.sort(self.visualCirclingRadiusComparer);
        self.selectedArea = None
        # for visualCirclingArea in self.visualCirclingAreas:
        #     radius = visualCirclingArea.Radius.Metres
        #     tempVisualCirclingAreas = []
        #     for visualCirclingArea0 in self.visualCirclingAreas:
        #         if round(radius, 3) >= round(visualCirclingArea0.Radius.Metres, 3):
        #             tempVisualCirclingAreas.append(visualCirclingArea0)
        #     self.visualCirclingAreas = tempVisualCirclingAreas
        #
        #     break
        self.selectedArea = self.visualCirclingAreas[len(self.visualCirclingAreas) - 1].SelectionArea;
        FlightPlanBaseDlg.btnEvaluate_Click(self)
        
        # self.manualPolygon = None

    def getSelectFeaturesMethod(self, selectedFeatures):
        i = 0
        radiusTuple = selectedFeatures[0].attribute("RadiusFromCenterPoint").toFloat()
        radius = radiusTuple[0]
        for i in range(1, len(selectedFeatures)):            
            tempRadius = selectedFeatures[i].attribute("RadiusFromCenterPoint").toFloat()
            if radius < tempRadius[0]:
                radius = tempRadius[0]
        for visualCirclingArea in self.visualCirclingAreas:
            if round(radius, 3) == round(visualCirclingArea.Radius.Metres, 3):
                self.selectedArea = visualCirclingArea
                break
        i = 0
        tempVisualCirclingAreas = []
        for visualCirclingArea in self.visualCirclingAreas:
            if round(radius, 3) >= round(visualCirclingArea.Radius.Metres, 3):
                tempVisualCirclingAreas.append(visualCirclingArea)
        self.visualCirclingAreas = tempVisualCirclingAreas
                
#         self.surface = self.selectedArea
        return FlightPlanBaseDlg.btnEvaluate_Click(self)
    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
#         if self.parametersPanel.cmbSelectionMode.currentIndex() != 0:
        self.manualEvent(self.parametersPanel.cmbSelectionMode.currentIndex())
            
        visualCirclingAreas = self.method_39();
#         constructionLayer  = None
#         mapUnits = define._canvas.mapUnits()
#         if define._mapCrs == None:
#             if mapUnits == QGis.Meters:
#                 constructionLayer = QgsVectorLayer("linestring?crs=EPSG:32633", self.surfaceType, "memory")
#             else:
#                 constructionLayer = QgsVectorLayer("linestring?crs=EPSG:4326", self.surfaceType, "memory")
#         else:
#             constructionLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")
        
#         constructionLayer.startEditing()
#         constructionLayer.dataProvider().addAttributes( [ QgsField("RadiusFromCenterPoint", QVariant.Double)])
#         layerList = []
#         if len(self.layers) > 0:
#             QgisHelper.removeFromCanvas(define._canvas, self.layers)
#             self.layers = []
        for visualCirclingArea in visualCirclingAreas:
            polylineArea = visualCirclingArea.area.previewArea
            constructionLayer = AcadHelper.createVectorLayer(visualCirclingArea.Category)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea, True)
            # polylineArea = visualCirclingArea.method_0();
            # polyline = (polylineArea.method_14_closed(), [("RadiusFromCenterPoint", visualCirclingArea.Radius.Metres)])
            # constructionLayer = QgisHelper.createPolylineLayer(visualCirclingArea.Category, [polyline], [QgsField("RadiusFromCenterPoint", QVariant.Double)])
            self.resultLayerList.append(constructionLayer)
#         constructionLayer.commitChanges()   
#         if len(self.resultLayers) > 0:
#             QgisHelper.removeFromCanvas(define._canvas, self.resultLayers)
        QgisHelper.appendToCanvas(define._canvas, self.resultLayerList, self.surfaceType)
        # self.resultLayerList = self.layers
        QgisHelper.zoomToLayers(self.resultLayerList)
        # self.resultLayers = self.layers
        self.ui.btnEvaluate.setEnabled(True)    

    def outputResultMethod(self):
        self.manualPolygon = self.toolSelectByPolygon.polygonGeom
#         QgisHelper.ClearRubberBandInCanvas(define._canvas)
#         tempFileName = ""
#         tempFileName = self.parametersPanel.txtFile.text()
#         if self.file1.closed:
# #             tempFileName = self.parametersPanel.txtFile.text()
#             fileInfo = QFileInfo(tempFileName)
#             if fileInfo.exists():
#                 QFile.remove(tempFileName)
#                 
#     #         n= 0
#     #         if not fileInfo.exists():
#             file0 = open(tempFileName, 'w')
#             file0.close()
#             self.file1 = open(tempFileName, 'r+')
        if self.toolSelectByPolygon == None:
            return
#         tempFileName = self.parametersPanel.txtFile.text()
#         self.file = open(tempFileName, 'r+')
#         mapUnits = define._canvas.mapUnits()
#         constructionLayer = None
#         if define._mapCrs == None:
#             if mapUnits == QGis.Meters:
#                 constructionLayer = QgsVectorLayer("Polygon?crs=EPSG:32633", SurfaceTypes.VisualCircling, "memory")
#             else:
#                 constructionLayer = QgsVectorLayer("Polygon?crs=EPSG:4326", SurfaceTypes.VisualCircling, "memory")
#         else:
#             constructionLayer = QgsVectorLayer("Polygon?crs=%s"%define._mapCrs.authid (), SurfaceTypes.VisualCircling, "memory")
#         constructionLayer.startEditing()
#         feature = QgsFeature()
#         feature.setGeometry(self.toolSelectByPolygon.polygonGeom)
#         constructionLayer.addFeature(feature)
#         constructionLayer.commitChanges()
#         if len(self.resultLayers) > 0:
#             QgisHelper.removeFromCanvas(define._canvas, self.resultLayers)
#         self.resultLayers = [constructionLayer]
#         
#         QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.VisualCircling)
#         QgisHelper.zoomToLayers([constructionLayer])
#         self.ui.btnEvaluate.setEnabled(True) 
        
        
        
    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return  
        self.filterList = []
        self.filterList.append("")
        for visualCirclingArea in self.visualCirclingAreas:
            self.filterList.append(visualCirclingArea.Category)
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.VisualCircling, self.ui.tblObstacles, self.filterList, parameterList, resultHideColumnNames)
        self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
     
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Thresholds", "group"))
        nameList = []
        n = 0
        for i in range(self.standardItermModel.rowCount()):
            if self.standardItermModel.item(i) == None or self.standardItermModel.item(i).text() == "":
                nameList.append("None_" + str(n))
                n += 1
            else:    
                str0 = self.standardItermModel.item(i).text()
                if len(nameList) > 0:
                    m = 0
                    for name0 in nameList:
                        if name0.count(str0) > 0:
                            m += 1
                            
                    if m > 0:
                        try:
                            float0 = float(str0[:1])
                            str0 = "Name_" + str0 + "_" + str(m - 1)
                            nameList.append(str0)
                        except:
                            nameList.append(str0 + "_" + str(m - 1))
                    else:
                        try:
                            float0 = float(str0[:1])
                            str0 = "Name_" + str0
                            nameList.append(str0)
                        except:
                            nameList.append(str0)
                else:
                    try:
                        float0 = float(str0[:1])
                        str0 = "Name_" + str0
                        nameList.append(str0)
                    except:
                        nameList.append(str0)
#                     nameList.append(str0)
                        
        for i in range(self.standardItermModel.rowCount()):
            parameterList.append((nameList[i], "group"))
#             if self.standardItermModel.item(i) == None or self.standardItermModel.item(i).text() == "":
#                 parameterList.append(("None", "group"))
#             else:    
#                 str0 = self.standardItermModel.item(i).text()
# #                 print str0[:1]
#                 try:
#                     float0 = float(str0[:1])
#                     parameterList.append(("Name_" + self.standardItermModel.item(i).text(), "group"))
#                 except:
#                     parameterList.append((self.standardItermModel.item(i).text(), "group"))
#                 parameterList.append(("ddf", "group"))
            longLatPoint = QgisHelper.Meter2Degree(float(self.standardItermModel.item(i, 1).text()), float(self.standardItermModel.item(i, 2).text()))
             
            # parameterList.append(("Lat", MathHelper.degree2DegreeMinuteSecond(longLatPoint.get_Y())))
            # parameterList.append(("Lon", MathHelper.degree2DegreeMinuteSecond(longLatPoint.get_X())))
            parameterList.append(("X", self.standardItermModel.item(i, 1).text()))
            parameterList.append(("Y", self.standardItermModel.item(i, 2).text()))
            parameterList.append(("Lat", self.standardItermModel.item(i, 3).text()))
            parameterList.append(("Lon", self.standardItermModel.item(i, 4).text()))
            if self.standardItermModel.item(i, 5).text() == "":
                parameterList.append(("Altitude", "0m"))
            else:
                parameterList.append(("Altitude", self.standardItermModel.item(i, 5).text() + "m"))
             
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Selection Mode", self.parametersPanel.cmbSelectionMode.currentText()))
        parameterList.append(("Aerodrome Elevation", self.parametersPanel.txtAdElevation.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtAdElevationFt.text() + "ft"))
        parameterList.append(("ISA", self.parametersPanel.txtIsa.text() + unicode("°C", "utf-8")))
        parameterList.append(("MOCmultiplier", str(self.parametersPanel.mocSpinBox.value())))
         
        parameterList.append(("Aircraft Categories", "group"))
        if self.parametersPanel.chbCatA.isChecked():
            parameterList.append(("A", "group"))
            parameterList.append(("MOC", self.parametersPanel.txtMocA.text() + "m"))
            parameterList.append(("Tas + Wind", self.parametersPanel.txtTasA.text() + "km/h"))
            parameterList.append(("Radius of Turn", self.parametersPanel.txtr.text() + "km"))
            parameterList.append(("Straight Segment", self.parametersPanel.txtStraightSegment.text() + "km"))
            parameterList.append(("Radius from threshold", self.parametersPanel.txtR.text() + "km"))
       
        if self.parametersPanel.chbCatB.isChecked():
            parameterList.append(("B", "group"))
            
            parameterList.append(("MOC", self.parametersPanel.txtMocB.text() + "m"))
            parameterList.append(("Tas + Wind", self.parametersPanel.txtTasB.text() + "km/h"))
            parameterList.append(("Radius of Turn", self.parametersPanel.txtrB.text() + "km"))
            parameterList.append(("Straight Segment", self.parametersPanel.txtStraightSegmentB.text() + "km"))
            parameterList.append(("Radius from threshold", self.parametersPanel.txtRB.text() + "km"))
       
        if self.parametersPanel.chbCatC.isChecked():
            parameterList.append(("C", "group"))
            
            parameterList.append(("MOC", self.parametersPanel.txtMocC.text() + "m"))
            parameterList.append(("Tas + Wind", self.parametersPanel.txtTasC.text() + "km/h"))
            parameterList.append(("Radius of Turn", self.parametersPanel.txtrC.text() + "km"))
            parameterList.append(("Straight Segment", self.parametersPanel.txtStraightSegmentC.text() + "km"))
            parameterList.append(("Radius from threshold", self.parametersPanel.txtRC.text() + "km"))
       
        if self.parametersPanel.chbCatD.isChecked():
            parameterList.append(("D", "group"))
#             parameterList.append(("Aircraft Altitude", self.parametersPanel.txtAltitudeD.text() + "ft"))
            parameterList.append(("MOC", self.parametersPanel.txtMocD.text() + "m"))
            parameterList.append(("Tas + Wind", self.parametersPanel.txtTasD.text() + "km/h"))
            parameterList.append(("Radius of Turn", self.parametersPanel.txtrD.text() + "km"))
            parameterList.append(("Straight Segment", self.parametersPanel.txtStraightSegmentD.text() + "km"))
            parameterList.append(("Radius from threshold", self.parametersPanel.txtRD.text() + "km"))
       
        if self.parametersPanel.chbCatE.isChecked():
            parameterList.append(("E", "group"))
#             parameterList.append(("Aircraft Altitude", self.parametersPanel.txtAltitudeE.text() + "ft"))
            parameterList.append(("MOC", self.parametersPanel.txtMocE.text() + "m"))
            parameterList.append(("Tas + Wind", self.parametersPanel.txtTasE.text() + "km/h"))
            parameterList.append(("Radius of Turn", self.parametersPanel.txtrE.text() + "km"))
            parameterList.append(("Straight Segment", self.parametersPanel.txtStraightSegmentE.text() + "km"))
            parameterList.append(("Radius from threshold", self.parametersPanel.txtRE.text() + "km"))
       
        if self.parametersPanel.chbCatCustom.isChecked():
            parameterList.append(("Custom", "group"))
#             parameterList.append(("Aircraft Altitude", self.parametersPanel.txtAltitudeCustom.text() + "ft"))
            parameterList.append(("MOC", self.parametersPanel.txtMocCustom.text() + "m"))
            parameterList.append(("Tas + Wind", self.parametersPanel.txtTasCustom.text() + "km/h"))
            parameterList.append(("Radius of Turn", self.parametersPanel.txtrCustom.text() + "km"))
            parameterList.append(("Straight Segment", self.parametersPanel.txtStraightSegmentCustom.text() + "km"))
            parameterList.append(("Radius from threshold", self.parametersPanel.txtRCustom.text() + "km"))
                   
            
        parameterList.append(("Results / Checked Obstacles", "group"))   
        parameterList.append(("Results", "group")) 
        parameterList.append(("Units", self.ui.cmbUnits.currentText())) 
        unitStr = ""
        vcaCount = len(self.visualCirclingAreas)
        if self.ui.cmbUnits.currentIndex() == 0:
            unitStr = "m"
        else:
            unitStr = "ft"
        parameterList.append((self.visualCirclingAreas[0].Category, self.ui.txtOCHResults.text()))
        if vcaCount > 1: 
            parameterList.append((self.visualCirclingAreas[1].Category, self.ui.txtOCAResults.text()))
        if vcaCount > 2: 
            parameterList.append((self.visualCirclingAreas[2].Category, self.ui.txtIAWP3Results.text())) 
        if vcaCount > 3:
            parameterList.append((self.visualCirclingAreas[3].Category, self.ui.txtIAWP4Results.text())) 
        if vcaCount > 4:
            parameterList.append((self.visualCirclingAreas[4].Category, self.ui.txtIAWP5Results.text())) 
        if vcaCount > 5:
            parameterList.append((self.visualCirclingAreas[5].Category, self.ui.txtIAWP6Results.text())) 
        
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList
#     def initObstaclesModel(self):
# #         ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
#         self.obstaclesModel = HoldingRnpObstacles(self.surfaceList)
#         
#         return FlightPlanBaseDlg.initObstaclesModel(self)
    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
#         self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        self.ui.frame_IAWP3 = QFrame(self.ui.grbResult_2)
        self.ui.frame_IAWP3.setFrameShape(QFrame.NoFrame)
        self.ui.frame_IAWP3.setFrameShadow(QFrame.Raised)
        self.ui.frame_IAWP3.setObjectName("frame_IAWP3")
        horizontalLayout_IAWP3 = QHBoxLayout(self.ui.frame_IAWP3)
        horizontalLayout_IAWP3.setSpacing(0)
        horizontalLayout_IAWP3.setMargin(0)
        horizontalLayout_IAWP3.setObjectName("horizontalLayout_IAWP3")
        self.ui.txtIAWP3 = QLineEdit(self.ui.frame_IAWP3)
        self.ui.txtIAWP3.setText("IAWP 3")
        font = QFont()
        font.setFamily("Arial")
        self.ui.txtIAWP3.setFont(font)
        self.ui.txtIAWP3.setObjectName("txtIAWP3")
        horizontalLayout_IAWP3.addWidget(self.ui.txtIAWP3)
        self.ui.txtIAWP3Results = QLineEdit(self.ui.frame_IAWP3)
        self.ui.txtIAWP3Results.setFont(font)
        self.ui.txtIAWP3Results.setObjectName("txtIAWP3Results")
        horizontalLayout_IAWP3.addWidget(self.ui.txtIAWP3Results)
        
        self.ui.frame_IAWP4 = QFrame(self.ui.grbResult_2)
        self.ui.frame_IAWP4.setFrameShape(QFrame.NoFrame)
        self.ui.frame_IAWP4.setFrameShadow(QFrame.Raised)
        self.ui.frame_IAWP4.setObjectName("self.ui.frame_IAWP4")
        horizontalLayout_IAWP4 = QHBoxLayout(self.ui.frame_IAWP4)
        horizontalLayout_IAWP4.setSpacing(0)
        horizontalLayout_IAWP4.setMargin(0)
        horizontalLayout_IAWP4.setObjectName("horizontalLayout_IAWP4")
        self.ui.txtIAWP4 = QLineEdit(self.ui.frame_IAWP4)
#         self.ui.txtIAWP3.setText("IAWP ")
#         font = QFont()
#         font.setFamily("Arial")
        self.ui.txtIAWP4.setFont(font)
        self.ui.txtIAWP4.setObjectName("txtIAWP4")
        horizontalLayout_IAWP4.addWidget(self.ui.txtIAWP4)
        self.ui.txtIAWP4Results = QLineEdit(self.ui.frame_IAWP4)
        self.ui.txtIAWP4Results.setFont(font)
        self.ui.txtIAWP4Results.setObjectName("txtIAWP4Results")
        horizontalLayout_IAWP4.addWidget(self.ui.txtIAWP4Results)
        
        self.ui.frame_IAWP5 = QFrame(self.ui.grbResult_2)
        self.ui.frame_IAWP5.setFrameShape(QFrame.NoFrame)
        self.ui.frame_IAWP5.setFrameShadow(QFrame.Raised)
        self.ui.frame_IAWP5.setObjectName("self.ui.frame_IAWP5")
        horizontalLayout_IAWP5 = QHBoxLayout(self.ui.frame_IAWP5)
        horizontalLayout_IAWP5.setSpacing(0)
        horizontalLayout_IAWP5.setMargin(0)
        horizontalLayout_IAWP5.setObjectName("horizontalLayout_IAWP5")
        self.ui.txtIAWP5 = QLineEdit(self.ui.frame_IAWP5)
#         self.ui.txtIAWP3.setText("IAWP ")
#         font = QFont()
#         font.setFamily("Arial")
        self.ui.txtIAWP5.setFont(font)
        self.ui.txtIAWP5.setObjectName("txtIAWP5")
        horizontalLayout_IAWP5.addWidget(self.ui.txtIAWP5)
        self.ui.txtIAWP5Results = QLineEdit(self.ui.frame_IAWP5)
        self.ui.txtIAWP5Results.setFont(font)
        self.ui.txtIAWP5Results.setObjectName("txtIAWP5Results")
        horizontalLayout_IAWP5.addWidget(self.ui.txtIAWP5Results)
        
        self.ui.frame_IAWP6 = QFrame(self.ui.grbResult_2)
        self.ui.frame_IAWP6.setFrameShape(QFrame.NoFrame)
        self.ui.frame_IAWP6.setFrameShadow(QFrame.Raised)
        self.ui.frame_IAWP6.setObjectName("self.ui.frame_IAWP6")
        horizontalLayout_IAWP6 = QHBoxLayout(self.ui.frame_IAWP6)
        horizontalLayout_IAWP6.setSpacing(0)
        horizontalLayout_IAWP6.setMargin(0)
        horizontalLayout_IAWP6.setObjectName("horizontalLayout_IAWP6")
        self.ui.txtIAWP6 = QLineEdit(self.ui.frame_IAWP6)
#         self.ui.txtIAWP3.setText("IAWP ")
#         font = QFont()
#         font.setFamily("Arial")
        self.ui.txtIAWP6.setFont(font)
        self.ui.txtIAWP6.setObjectName("txtIAWP6")
        horizontalLayout_IAWP6.addWidget(self.ui.txtIAWP6)
        self.ui.txtIAWP6Results = QLineEdit(self.ui.frame_IAWP6)
        self.ui.txtIAWP6Results.setFont(font)
        self.ui.txtIAWP6Results.setObjectName("txtIAWP6Results")
        horizontalLayout_IAWP6.addWidget(self.ui.txtIAWP6Results)
        
        self.ui.verticalLayout_17.addWidget(self.ui.frame_IAWP3)
        self.ui.verticalLayout_17.addWidget(self.ui.frame_IAWP4)
        self.ui.verticalLayout_17.addWidget(self.ui.frame_IAWP5)
        self.ui.verticalLayout_17.addWidget(self.ui.frame_IAWP6)
        self.ui.frame_114.hide()
        self.ui.frame_IAWP3.hide()
        self.ui.frame_IAWP4.hide()
        self.ui.frame_IAWP5.hide()
        self.ui.frame_IAWP6.hide()
         
        self.ui.btnPDTCheck.setVisible(True)   
        self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_clicked)
      
        return FlightPlanBaseDlg.uiStateInit(self)
    def btnPDTCheck_clicked(self):
        parameterList = []
        if self.parametersPanel.chbCatA.isChecked():
            parameterList.append(["A", 
                                  float(self.parametersPanel.txtIsa.text()),
                                  Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300),
                                  100,
                                  None
                                  ])
        if self.parametersPanel.chbCatB.isChecked():
            parameterList.append(["B", 
                                  float(self.parametersPanel.txtIsa.text()),
                                  Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300),
                                  135,
                                  None
                                  ])
        if self.parametersPanel.chbCatC.isChecked():
            parameterList.append(["C", 
                                  float(self.parametersPanel.txtIsa.text()),
                                  Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300),
                                  180,
                                  None
                                  ])
        if self.parametersPanel.chbCatD.isChecked():
            parameterList.append(["D", 
                                  float(self.parametersPanel.txtIsa.text()),
                                  Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300),
                                  205,
                                  None
                                  ])
        if self.parametersPanel.chbCatE.isChecked():
            parameterList.append(["E", 
                                  float(self.parametersPanel.txtIsa.text()),
                                  Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300),
                                  240,
                                  None
                                  ])
        if self.parametersPanel.chbCatCustom.isChecked():
            parameterList.append(["Custom", 
                                  float(self.parametersPanel.txtIsa.text()),
                                  Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300),
                                  float(self.parametersPanel.txtIasCustom.text()),
                                  None
                                  ])
        dlg = PdtCheckResultDlg(self, parameterList)
        dlg.resize(350, 300)
        dlg.exec_()
    def initParametersPan(self):
        ui = Ui_VisualCircling()
        self.parametersPanel = ui        
        FlightPlanBaseDlg.initParametersPan(self) 
        
        
        self.parametersPanel.txtTasCustom.setEnabled(True)
        
        self.frame_8_1 = QFrame(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_8_1.sizePolicy().hasHeightForWidth())
        self.frame_8_1.setSizePolicy(sizePolicy)
        self.frame_8_1.setFrameShape(QFrame.NoFrame)
        self.frame_8_1.setFrameShadow(QFrame.Raised)
        self.frame_8_1.setObjectName("frame_8")
        self.horizontalLayout_10_1 = QHBoxLayout(self.frame_8_1)
#         self.horizontalLayout_10_1.setAlignment(Qt.AlignHCenter)
        self.horizontalLayout_10_1.setSpacing(0)
        self.horizontalLayout_10_1.setMargin(0)
        self.horizontalLayout_10_1.setObjectName("horizontalLayout_10")
        
        self.label_19 = QLabel(self.frame_8_1)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setMinimumSize(QSize(200, 0))
        self.label_19.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.label_19.setText("MOCmultiplier")
        self.horizontalLayout_10_1.addWidget(self.label_19)
        
        self.parametersPanel.mocSpinBox = QSpinBox(self.frame_8_1)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parametersPanel.mocSpinBox.sizePolicy().hasHeightForWidth())
        self.parametersPanel.mocSpinBox.setSizePolicy(sizePolicy)
        self.parametersPanel.mocSpinBox.setMinimumSize(QSize(60, 0))
        self.parametersPanel.mocSpinBox.setMaximumSize(QSize(60, 5666666))
        self.parametersPanel.mocSpinBox.setFont(font)
        self.parametersPanel.mocSpinBox.setObjectName("mocSpinBox")
        self.parametersPanel.mocSpinBox.setMinimum(1)
#         self.parametersPanel.mocSpinBox.setMinimumSize(QSize(105, 16777215))
#         self.parametersPanel.mocSpinBox.setFixedWidth(105)
        self.horizontalLayout_10_1.addWidget(self.parametersPanel.mocSpinBox)
#         self.verticalLayout_9.addWidget(self.frame_8_1)
        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_10_1.addItem(horizontalSpacer)
        self.parametersPanel.vl_gbParameters.insertWidget(3, self.frame_8_1)
        
        self.standardItermModel=QStandardItemModel()
        itemID = QStandardItem("ID")
        itemX = QStandardItem("X")
        itemY = QStandardItem("Y")

        itemLat = QStandardItem("Latitude")
        itemLon = QStandardItem("Longitude")
        itemAltitude = QStandardItem("Altitude(m)")
        self.standardItermModel.setHorizontalHeaderItem(0, itemID)
        self.standardItermModel.setHorizontalHeaderItem(1, itemX)
        self.standardItermModel.setHorizontalHeaderItem(2, itemY)
        self.standardItermModel.setHorizontalHeaderItem(3, itemLat)
        self.standardItermModel.setHorizontalHeaderItem(4, itemLon)
        self.standardItermModel.setHorizontalHeaderItem(5, itemAltitude)
        self.standardItermModel.setHorizontalHeaderItem(6, QStandardItem("RealX"))
        self.standardItermModel.setHorizontalHeaderItem(7, QStandardItem("RealY"))
        self.parametersPanel.tblThresholds.setModel(self.standardItermModel)
        self.parametersPanel.tblThresholds.setColumnHidden(6, True)
        self.parametersPanel.tblThresholds.setColumnHidden(7, True)
        
        self.parametersPanel.cmbSelectionMode.addItems(["Automatic", "Manual"])
#         self.parametersPanel.cmbSelectionMode.setCurrentIndex(1)
        
        self.parametersPanel.chbCatE.setChecked(False)
        self.parametersPanel.chbCatCustom.setChecked(False)
        
        self.parametersPanel.btnPickThresholds.clicked.connect(self.capturePosition)
        self.CaptureCoordTool = CaptureCoordinateToolUpdate(define._canvas)   
        self.parametersPanel.btnCaptureAdElevation.clicked.connect(self.measureDistance)
        self.parametersPanel.txtIasCustom.textChanged.connect(self.txtIasCustomChange)
#         self.parametersPanel.txtAltitudeB.textChanged.connect(self.altitudeBChanged)
#         self.parametersPanel.txtAltitudeC.textChanged.connect(self.altitudeCChanged)
#         self.parametersPanel.txtAltitudeD.textChanged.connect(self.altitudeDChanged)
#         self.parametersPanel.txtAltitudeE.textChanged.connect(self.altitudeEChanged)
#         self.parametersPanel.txtAltitudeCustom.textChanged.connect(self.altitudeCustomChanged)
        self.connect(self.CaptureCoordTool, SIGNAL("resultPointValueList"), self.resultPointValueListMethod)
        self.parametersPanel.txtAdElevation.textChanged.connect(self.txtAdElevation_textChange)
        self.parametersPanel.txtAdElevationFt.textChanged.connect(self.txtAdElevationFt_textChange)
        
#         self.parametersPanel.cmbSelectionMode.currentIndexChanged.connect(self.manualEvent)
        
        self.aDE_EditFlag = False
        self.aDEft_EditFlag = False
        
        try:
            self.parametersPanel.txtAdElevationFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAdElevation.text())), 1)))
            
        except ValueError:
            self.parametersPanel.txtAdElevationFt.setText("")
        
        try:
            tasValue = round(Speed.smethod_0(Speed(100), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour, 4) + 46
            self.parametersPanel.txtTasA.setText(str(tasValue))
            
            tasValue = round(Speed.smethod_0(Speed(135), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour, 4) + 46
            self.parametersPanel.txtTasB.setText(str(tasValue))
            
            tasValue = round(Speed.smethod_0(Speed(180), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour, 4) + 46
            self.parametersPanel.txtTasC.setText(str(tasValue))
            
            tasValue = round(Speed.smethod_0(Speed(205), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour, 4) + 46
            self.parametersPanel.txtTasD.setText(str(tasValue))
            
            tasValue = round(Speed.smethod_0(Speed(240), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour, 4) + 46
            self.parametersPanel.txtTasE.setText(str(tasValue))
            
            tasValue = round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIasCustom.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour, 4) + 46
            self.parametersPanel.txtTasCustom.setText(str(tasValue))
        except:
            raise ValueError("Altitude's value is too large and it must be type of number.")
        
        
        self.method_38(AircraftSpeedCategory.A, True);
        self.method_38(AircraftSpeedCategory.B, True);
        self.method_38(AircraftSpeedCategory.C, True);
        self.method_38(AircraftSpeedCategory.D, True);
        self.method_38(AircraftSpeedCategory.E, True);
        self.method_38(AircraftSpeedCategory.Custom, True);
        
        self.parametersPanel.txtTasA.setEnabled(False)
        self.parametersPanel.txtTasB.setEnabled(False)
        self.parametersPanel.txtTasC.setEnabled(False)
        self.parametersPanel.txtTasD.setEnabled(False)
        self.parametersPanel.txtTasE.setEnabled(False)
    def manualEvent(self, index):
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        self.manualPolygon = None
        if index != 0:
            self.toolSelectByPolygon = RubberBandPolygon(define._canvas)
            define._canvas.setMapTool(self.toolSelectByPolygon)
            self.connect(self.toolSelectByPolygon, SIGNAL("outputResult"), self.outputResultMethod)
        else:
            
            self.mapToolPan = QgsMapToolPan(define._canvas)
            define._canvas.setMapTool(self.mapToolPan )
            
    def txtIasCustomChange(self):
        self.method_38(AircraftSpeedCategory.A, True);
        self.method_38(AircraftSpeedCategory.B, True);
        self.method_38(AircraftSpeedCategory.C, True);
        self.method_38(AircraftSpeedCategory.D, True);
        self.method_38(AircraftSpeedCategory.E, True);
        self.method_38(AircraftSpeedCategory.Custom, True);
        tasValue = round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIasCustom.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour, 4) + 46
        self.parametersPanel.txtTasCustom.setText(str(tasValue))
    def txtAdElevation_textChange(self):
        self.aDEft_EditFlag = False
        
        if self.aDE_EditFlag == True:
            try:
                self.parametersPanel.txtAdElevationFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAdElevation.text())), 4)))
                
            except ValueError:
                self.parametersPanel.txtAdElevationFt.setText("")
        self.aDEft_EditFlag = True
        try:
            tasValue = round(Speed.smethod_0(Speed(100), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour  , 4) + 46
            self.parametersPanel.txtTasA.setText(str(tasValue))
            
            tasValue = round(Speed.smethod_0(Speed(135), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour  , 4) + 46
            self.parametersPanel.txtTasB.setText(str(tasValue))
            
            tasValue = round(Speed.smethod_0(Speed(180), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour  , 4) + 46
            self.parametersPanel.txtTasC.setText(str(tasValue))
            
            tasValue = round(Speed.smethod_0(Speed(205), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour  , 4) + 46
            self.parametersPanel.txtTasD.setText(str(tasValue))
            
            tasValue = round(Speed.smethod_0(Speed(240), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour  , 4) + 46
            self.parametersPanel.txtTasE.setText(str(tasValue))
            
            tasValue = round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIasCustom.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)).KilometresPerHour  , 4) + 46
            self.parametersPanel.txtTasCustom.setText(str(tasValue))
            
            self.method_38(AircraftSpeedCategory.A, True);
            self.method_38(AircraftSpeedCategory.B, True);
            self.method_38(AircraftSpeedCategory.C, True);
            self.method_38(AircraftSpeedCategory.D, True);
            self.method_38(AircraftSpeedCategory.E, True);
            self.method_38(AircraftSpeedCategory.Custom, True);
        except:
            raise ValueError("Altitude's value is too large and it must be type of number.")
    
    def txtAdElevationFt_textChange(self):
        self.aDE_EditFlag = False
        
        if self.aDEft_EditFlag == True:
            try:
                self.parametersPanel.txtAdElevation.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAdElevationFt.text())), 4)))
                
            except ValueError:
                self.parametersPanel.txtAdElevationFt.setText("")
        self.aDE_EditFlag = True
        
        
    def resultPointValueListMethod(self, resultValueList):
        itemList = []
        xStr = None
        yStr = None
        latStr = None
        lonStr = None

        if len(resultValueList) > 0:

            if define._units == QGis.Meters:
                xStr = resultValueList[1]
                yStr = resultValueList[2]
                try:
                    flag, degreeLat, degreeLon = Geo.smethod_2(float(xStr), float(yStr))
                    latStr = degreeLat.ToString()
                    if len(str(int(degreeLon.value))) == 3:
                        lonStr = degreeLon.ToString("dddmmss.ssssH")
                    else:
                        lonStr = degreeLon.ToString("ddmmss.ssssH")
                except:
                    pass
            else:
                degreeLat = Degrees(float(resultValueList[2]), None, None, DegreesType.Latitude)
                degreeLon = Degrees(float(resultValueList[1]), None, None, DegreesType.Longitude)
                latStr = degreeLat.ToString()
                if len(str(int(degreeLon.value))) == 3:
                    lonStr = degreeLon.ToString("dddmmss.ssssH")
                else:
                    lonStr = degreeLon.ToString("ddmmss.ssssH")

                flag, xVal, yVal = Geo.smethod_3(degreeLat, degreeLon)
                if flag:
                    xStr = str(xVal)
                    yStr = str(yVal)

            # self.txtPointX.setText(resultValueList[1])
            # self.txtPointY.setText(resultValueList[2])
            # if self.alwwaysShowString == "Degree":
            #     capturePoint3d = Point3D(degreeLon.value, degreeLat.value, float(resultValueList[3]))
            # else:
            #     capturePoint3d = Point3D(float(resultValueList[1]), float(resultValueList[2]), float(resultValueList[3]))



            itemList.append(QStandardItem(resultValueList[0]))
            itemList.append(QStandardItem(xStr))
            itemList.append(QStandardItem(yStr))
            itemList.append(QStandardItem(latStr))
            itemList.append(QStandardItem(lonStr))
            itemList.append(QStandardItem(resultValueList[3]))
            itemList.append(QStandardItem(resultValueList[1]))
            itemList.append(QStandardItem(resultValueList[2]))
            
#             if resultValueList[3] != "":
#                 self.inputPoint3dList.append(Point3D(float(resultValueList[1]), float(resultValueList[2]), float(resultValueList[3])))
#             else:
#                 self.inputPoint3dList.append(Point3D(float(resultValueList[1]), float(resultValueList[2])))
            
            self.standardItermModel.appendRow(itemList)
    
    def method_38(self, aircraftSpeedCategory_0, bool_0 = False):
        kilometresPerHour = 0.0
        speed = Speed(25);
        num = 0.0
        distance_0 = None
        speed_0 = None
        speed_1 = None
        altitude0 = Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)
        if (aircraftSpeedCategory_0 == AircraftSpeedCategory.A):
            speed_0 = Speed(100, SpeedUnits.KTS);
            speed_1 = Speed.smethod_0(speed_0, float(self.parametersPanel.txtIsa.text()), altitude0) + speed;
            kilometresPerHour = 560
            
            num = 2313.03083707 / (3.14159265358979 * speed_1.KilometresPerHour);
            if (num > 3):
                num = 3;
            num = speed_1.KilometresPerHour / (62.8318530717959 * num) * 1000;
            distance_0 = Distance(2 * num + kilometresPerHour, DistanceUnits.M);
            
            if bool_0:
                self.parametersPanel.txtr.setText(str(round(num / 1000, 3)))
                self.parametersPanel.txtR.setText(str(round(distance_0.Kilometres, 3)))
                self.parametersPanel.txtStraightSegment.setText(str(round(float(kilometresPerHour)/ 1000, 3)))
        elif aircraftSpeedCategory_0 == AircraftSpeedCategory.B:
            speed_0 = Speed(135, SpeedUnits.KTS);
            speed_1 = Speed.smethod_0(speed_0, float(self.parametersPanel.txtIsa.text()), altitude0) + speed;
            kilometresPerHour = 740.8
            
            num = 2313.03083707 / (3.14159265358979 * speed_1.KilometresPerHour);
            if (num > 3):
                num = 3;
            num = speed_1.KilometresPerHour / (62.8318530717959 * num) * 1000;
            distance_0 = Distance(2 * num + kilometresPerHour, DistanceUnits.M);
            
            if bool_0:
                self.parametersPanel.txtrB.setText(str(round(num / 1000, 3)))
                self.parametersPanel.txtRB.setText(str(round(distance_0.Kilometres, 3)))
                self.parametersPanel.txtStraightSegmentB.setText(str(round(float(kilometresPerHour) / 1000, 3)))
        elif aircraftSpeedCategory_0 == AircraftSpeedCategory.C:
            speed_0 = Speed(180, SpeedUnits.KTS);
            speed_1 = Speed.smethod_0(speed_0, float(self.parametersPanel.txtIsa.text()), altitude0) + speed;
            kilometresPerHour = 930
            
            num = 2313.03083707 / (3.14159265358979 * speed_1.KilometresPerHour);
            if (num > 3):
                num = 3;
            num = speed_1.KilometresPerHour / (62.8318530717959 * num) * 1000;
            distance_0 = Distance(2 * num + kilometresPerHour, DistanceUnits.M);
            
            if bool_0:
                self.parametersPanel.txtrC.setText(str(round(num / 1000, 3)))
                self.parametersPanel.txtRC.setText(str(round(distance_0.Kilometres, 3)))
                self.parametersPanel.txtStraightSegmentC.setText(str(round(float(kilometresPerHour) / 1000, 3)))
        elif aircraftSpeedCategory_0 == AircraftSpeedCategory.D:
            speed_0 = Speed(205, SpeedUnits.KTS);
            speed_1 = Speed.smethod_0(speed_0, float(self.parametersPanel.txtIsa.text()), altitude0) + speed;
            kilometresPerHour = 1111
            
            num = 2313.03083707 / (3.14159265358979 * speed_1.KilometresPerHour);
            if (num > 3):
                num = 3;
            num = speed_1.KilometresPerHour / (62.8318530717959 * num) * 1000;
            distance_0 = Distance(2 * num + kilometresPerHour, DistanceUnits.M);
            
            if bool_0:
                self.parametersPanel.txtrD.setText(str(round(num / 1000, 3)))
                self.parametersPanel.txtRD.setText(str(round(distance_0.Kilometres, 3)))
                self.parametersPanel.txtStraightSegmentD.setText(str(round(float(kilometresPerHour) / 1000, 3)))
        elif aircraftSpeedCategory_0 == AircraftSpeedCategory.E:
            speed_0 = Speed(240, SpeedUnits.KTS);
            speed_1 = Speed.smethod_0(speed_0, float(self.parametersPanel.txtIsa.text()), altitude0) + speed;
            kilometresPerHour = 1300;
            
            num = 2313.03083707 / (3.14159265358979 * speed_1.KilometresPerHour);
            if (num > 3):
                num = 3;
            num = speed_1.KilometresPerHour / (62.8318530717959 * num) * 1000;
            distance_0 = Distance(2 * num + kilometresPerHour, DistanceUnits.M);
            
            if bool_0:
                self.parametersPanel.txtrE.setText(str(round(num / 1000, 3)))
                self.parametersPanel.txtRE.setText(str(round(distance_0.Kilometres, 3)))
                self.parametersPanel.txtStraightSegmentE.setText(str(round(float(kilometresPerHour) / 1000, 3)))
        elif aircraftSpeedCategory_0 == AircraftSpeedCategory.H:
            raise ValueError(Messages.ERR_INVALID_AIRCRAFT_CATEGORY)
        elif aircraftSpeedCategory_0 == AircraftSpeedCategory.Custom:
            speed_0 = Speed(float(self.parametersPanel.txtIasCustom.text()), SpeedUnits.KTS);
            speed_1 = Speed.smethod_0(speed_0, float(self.parametersPanel.txtIsa.text()), altitude0) + speed;
            kilometresPerHour = speed_1.KilometresPerHour * 1000 / 3600 * 9
            
            num = 2313.03083707 / (3.14159265358979 * speed_1.KilometresPerHour);
            if (num > 3):
                num = 3;
            num = speed_1.KilometresPerHour / (62.8318530717959 * num) * 1000;
            distance_0 = Distance(2 * num + kilometresPerHour, DistanceUnits.M);
            
            if bool_0:
                self.parametersPanel.txtrCustom.setText(str(round(num / 1000, 3)))
                self.parametersPanel.txtRCustom.setText(str(round(distance_0.Kilometres, 3)))
                self.parametersPanel.txtStraightSegmentCustom.setText(str(round(float(kilometresPerHour) / 1000, 3)))
        else:
            raise ValueError(Messages.ERR_INVALID_AIRCRAFT_CATEGORY)
        
            
        
        return (speed_0, speed_1, distance_0)
    
    def method_39(self):
#         speed = None
#         speed1 = None
        distance = None
        point3dCollection = []
        
        for i in range(self.standardItermModel.rowCount()):
            if self.standardItermModel.item(i, 5).text() == "":
                point3dCollection.append(Point3D(float(self.standardItermModel.item(i, 6).text()), float(self.standardItermModel.item(i, 7).text())))
            else:
                point3dCollection.append(Point3D(float(self.standardItermModel.item(i, 6).text()), float(self.standardItermModel.item(i, 7).text()), float(self.standardItermModel.item(i, 5).text())))
        if len(point3dCollection) == 0:
            pass
        point3dCollection1 = QgisHelper.convexFull([PolylineArea(point3dCollection)]);
        visualCirclingAreas = []
        altitude0 = Altitude(float(self.parametersPanel.txtAdElevation.text()) + 300)
        if (self.parametersPanel.chbCatA.isChecked()):
            speed, speed1, distance = self.method_38(AircraftSpeedCategory.A);
            visualCirclingAreas.append(VisualCirclingArea("Category.A", altitude0, Altitude(float(self.parametersPanel.txtMocA.text()), AltitudeUnits.M), distance, point3dCollection1))
        if (self.parametersPanel.chbCatB.isChecked()):
            speed, speed1, distance = self.method_38(AircraftSpeedCategory.B);
            visualCirclingAreas.append(VisualCirclingArea("Category.B", altitude0, Altitude(float(self.parametersPanel.txtMocB.text()), AltitudeUnits.M), distance, point3dCollection1))
        if (self.parametersPanel.chbCatC.isChecked()):
            speed, speed1, distance = self.method_38(AircraftSpeedCategory.C);
            visualCirclingAreas.append(VisualCirclingArea("Category.C", altitude0, Altitude(float(self.parametersPanel.txtMocC.text()), AltitudeUnits.M), distance, point3dCollection1));
        if (self.parametersPanel.chbCatD.isChecked()):
            speed, speed1, distance = self.method_38(AircraftSpeedCategory.D);
            visualCirclingAreas.append(VisualCirclingArea("Category.D", altitude0, Altitude(float(self.parametersPanel.txtMocD.text()), AltitudeUnits.M), distance, point3dCollection1));
        if (self.parametersPanel.chbCatE.isChecked()):
            speed, speed1, distance = self.method_38(AircraftSpeedCategory.E);
            visualCirclingAreas.append(VisualCirclingArea("Category.E", altitude0, Altitude(float(self.parametersPanel.txtMocE.text()), AltitudeUnits.M), distance, point3dCollection1));
        if (self.parametersPanel.chbCatCustom.isChecked()):
            speed, speed1, distance = self.method_38(AircraftSpeedCategory.Custom);
            visualCirclingAreas.append(VisualCirclingArea("Category.Custom", altitude0, Altitude(float(self.parametersPanel.txtMocCustom.text()), AltitudeUnits.M), distance, point3dCollection1));
        return visualCirclingAreas;
        
    def measureDistance(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtAdElevation, DistanceUnits.M)
        define._canvas.setMapTool(measureDistanceTool)     
    def capturePosition(self):
#         if self.parametersPanel.btnPickThresholds.isChecked():
        define._canvas.setMapTool(self.CaptureCoordTool)
#             if self.parentDialog != None:
#                 self.parentDialog.hide()
#         else:
#             define._canvas.setMapTool(QgsMapToolPan(define._canvas))
#         pass
class VisualCirclingArea:
    def __init__(self, aircraftSpeedCategory_0, altitude_0, altitude_1, distance_0, point3dCollection_0):
        polylineArea = PolylineArea()
        self.category = aircraftSpeedCategory_0;
        self.altitude = altitude_0.Metres;
        self.moc = altitude_1.Metres;
        self.radius = distance_0;
        if (len(point3dCollection_0) == 1):
            polylineArea = PolylineArea(None, point3dCollection_0[0], distance_0.Metres)
        elif (len(point3dCollection_0) != 2):
            polylineArea = (PolylineArea(point3dCollection_0)).method_18(distance_0.Metres)
        else:
            num = MathHelper.getBearing(point3dCollection_0.get_Item(0), point3dCollection_0.get_Item(1)) - 1.5707963267949;
            num1 = MathHelper.getBearing(point3dCollection_0.get_Item(0), point3dCollection_0.get_Item(1)) + 1.5707963267949;
            point3d = MathHelper.distanceBearingPoint(point3dCollection_0.get_Item(0), num, distance_0.Metres);
            point3d1 = MathHelper.distanceBearingPoint(point3dCollection_0.get_Item(1), num, distance_0.Metres);
            point3d2 = MathHelper.distanceBearingPoint(point3dCollection_0.get_Item(0), num1, distance_0.Metres);
            point3d3 = MathHelper.distanceBearingPoint(point3dCollection_0.get_Item(1), num1, distance_0.Metres);
            polylineArea = PolylineArea()
            polylineArea.Add(PolylineAreaPoint(point3d))
            polylineArea.Add(PolylineAreaPoint(point3d1, MathHelper.smethod_57(TurnDirection.Right, point3d1, point3d3, point3dCollection_0.get_Item(1))))
            polylineArea.Add(PolylineAreaPoint(point3d3))
            polylineArea.Add(PolylineAreaPoint(point3d2, MathHelper.smethod_57(TurnDirection.Right, point3d2, point3d, point3dCollection_0.get_Item(0))))
        self.area = PrimaryObstacleArea(polylineArea);
    def method_0(self):
        polylineArea = PolylineArea.smethod_131(self.area.previewArea)
        return polylineArea
#         polyline.set_Closed(true);
#         AcadHelper.smethod_18(transaction_0, blockTableRecord_0, polyline, string_0);
    def method_1(self, obstacle_0):
        double_0 = self.moc * obstacle_0.MocMultiplier;
        double_1 = None
        criticalObstacleType_0 = CriticalObstacleType.No;
        if (not self.area.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
            return (False, double_0, double_1, criticalObstacleType_0)
        position = obstacle_0.Position;
        double_1 = position.get_Z() + obstacle_0.Trees + double_0;
        if (double_1 > self.altitude):
            criticalObstacleType_0 = CriticalObstacleType.Yes
        return (True, double_0, double_1, criticalObstacleType_0)
    def method_2(self, obstacle_0):
        double_0 = self.moc * obstacle_0.MocMultiplier;
        position = obstacle_0.Position;
        double_1 = position.get_Z() + obstacle_0.Trees + double_0;
        if (double_1 > self.altitude):
            return (CriticalObstacleType.Yes, double_0, double_1)
        return (CriticalObstacleType.No, double_0, double_1)
            
    def get_altitude(self):
        return Altitude(self.altitude)
    Altitude = property(get_altitude, None, None, None)
    
    def get_area(self):
        return self.area
    SelectionArea = property(get_area, None, None, None)
    
    def get_category(self):
        return self.category
    Category = property(get_category, None, None, None)
    
    def get_radius(self):
        return self.radius
    Radius = property(get_radius, None, None, None)
class VisualCirclingObstacles(ObstacleTable):
    def __init__(self, surfacesList, altitude, manualPoly):
        ObstacleTable.__init__(self, surfacesList)
        self.surfaceType = SurfaceTypes.VisualCircling
        self.surfacesList  = surfacesList
        self.altitude = altitude
        self.ObstaclesChecked = 0
        self.manualPolygon = manualPoly
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexMocAppliedM = fixedColumnCount 
        self.IndexMocAppliedFt = fixedColumnCount + 1
        self.IndexMocMultiplier = fixedColumnCount + 2
        self.IndexOcaM = fixedColumnCount + 3
        self.IndexOcaFt = fixedColumnCount + 4
        self.IndexCritical = fixedColumnCount + 5
        self.IndexSurface = fixedColumnCount + 6
                 
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt, 
                ObstacleTableColumnType.Critical,
                ObstacleTableColumnType.Surface               
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
    def addObstacleToModel(self, obstacle, checkResult):
        ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
        row = self.source.rowCount() - 1

        item = QStandardItem(str(checkResult[0]))
        item.setData(checkResult[0])
        self.source.setItem(row, self.IndexMocAppliedM, item)
          
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[0])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[0]))
        self.source.setItem(row, self.IndexMocAppliedFt, item)
          
        item = QStandardItem(str(ObstacleTable.MocMultiplier))
        item.setData(ObstacleTable.MocMultiplier)
        self.source.setItem(row, self.IndexMocMultiplier, item)
          
        item = QStandardItem(str(checkResult[1]))
        item.setData(checkResult[1])
        self.source.setItem(row, self.IndexOcaM, item)
          
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[1])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[1]))
        self.source.setItem(row, self.IndexOcaFt, item)  
        
        item = QStandardItem(str(checkResult[2]))
        item.setData(checkResult[2])
        self.source.setItem(row, self.IndexCritical, item)
        
        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexSurface, item)
    def checkObstacle(self, obstacle_0):
        num2 = 0;
        if self.manualPolygon != None:
            if not self.manualPolygon.contains(obstacle_0.Position):
                return
        for current in self.surfacesList:
            result, num, num1, criticalObstacleType = current.method_1(obstacle_0)
            if (result):
                checkResult = []
                checkResult.append(num)
                checkResult.append(num1)
                checkResult.append(criticalObstacleType)
                checkResult.append(current.Category)
#                 checkResult = [num, num1, criticalObstacleType, current.Category]
                self.addObstacleToModel(obstacle_0, checkResult)
                self.ObstaclesChecked += 1;
                break;
            else:
                num2 += 1
        for i in range(num2 + 1, len(self.surfacesList)):
            criticalObstacleType, num, num1 = self.surfacesList[i].method_2(obstacle_0);
            checkResult = []
            checkResult.append(num)
            checkResult.append(num1)
            checkResult.append(criticalObstacleType)
            checkResult.append(self.surfacesList[i].Category)
#             checkResult = [num, num1, criticalObstacleType, current.Category]
            self.addObstacleToModel(obstacle_0, checkResult)
            self.ObstaclesChecked += 1;
    def method_12(self, category, altitudeUnits_0):
        self.setFilterFixedString(category)
        self.sort(self.IndexOcaM, Qt.DescendingOrder )
        
        if (self.rowCount() == 0):
            if (category == "Category.Custom"):
                return Captions.GROUND_PLANE
            return self.method_13(self.minimumOCA(category), altitudeUnits_0);
        item = self.data(self.index(0, self.IndexOcaM), Qt.DisplayRole).toDouble()[0]
        
        if (category == "Category.Custom"):
            return self.method_13(Altitude(item), altitudeUnits_0)
        altitude = self.minimumOCA(category)
        return self.method_13(Altitude(max([altitude.Metres, item])), altitudeUnits_0);
    def method_13(self, altitude_0, altitudeUnits_0):
        if (altitudeUnits_0 == AltitudeUnits.M):
            metres = altitude_0.Metres;
            num = metres % 5;
            if (num > 0):
                metres = metres + (5 - num);
            altitude = round(metres)
            return str(altitude) + "m"
        feet = altitude_0.Feet;
        num1 = feet % 10;
        if (num1 > 0):
            feet = feet + (10 - num1);
        altitude1 = round(feet)
        return str(altitude1) + "ft"
    def minimumOCA(self, category):
        altitude0 = None
        if (category == "Category.A"):
            altitude0 = Altitude(self.altitude.Metres + 120)
        elif (category == "Category.B"):
            altitude0 = Altitude(self.altitude.Metres + 150)
        elif (category == "Category.C"):
            altitude0 = Altitude(self.altitude.Metres + 180)
        elif (category == "Category.D"):
            altitude0 = Altitude(self.altitude.Metres + 210)
        elif (category == "Category.E"):
            altitude0 = Altitude(self.altitude.Metres + 240)
        return altitude0    
class RubberBandPolygon(QgsMapTool):
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.mCanvas = canvas
        self.mRubberBand = None
        self.mRubberBand0 = QgsRubberBand( self.mCanvas, QGis.Polygon )
        self.mCursor = Qt.ArrowCursor
        self.mFillColor = QColor( 254, 178, 76, 63 )
        self.mBorderColour = QColor( 254, 58, 29, 100 )
        self.mRubberBand0.setBorderColor( self.mBorderColour )
        self.polygonGeom = None
        self.drawFlag = False
#         self.constructionLayer = constructionLayer
    def canvasPressEvent( self, e ):
        if ( self.mRubberBand == None ):
            self.mRubberBand0.reset( QGis.Polygon )
#             define._canvas.clearCache ()
            self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRubberBand0 = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRubberBand.setFillColor( self.mFillColor )
            self.mRubberBand.setBorderColor( self.mBorderColour )
            self.mRubberBand0.setFillColor( self.mFillColor )
            self.mRubberBand0.setBorderColor( self.mBorderColour )
        if ( e.button() == Qt.LeftButton ):
            self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )
        else:
            if ( self.mRubberBand.numberOfVertices() > 2 ):
                self.polygonGeom = self.mRubberBand.asGeometry()
            else:
                return
#                 QgsMapToolSelectUtils.setSelectFeatures( self.mCanvas, polygonGeom, e )
            self.mRubberBand.reset( QGis.Polygon )
            self.mRubberBand0.addGeometry(self.polygonGeom, None)
            self.mRubberBand0.show()
            self.mRubberBand = None
            self.emit(SIGNAL("outputResult"), self.polygonGeom)
    
    def canvasMoveEvent( self, e ):
        pass
        if ( self.mRubberBand == None ):
            return
        if ( self.mRubberBand.numberOfVertices() > 0 ):
            self.mRubberBand.removeLastPoint( 0 )
            self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )
    def deactivate(self):
#         self.rubberBand.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))