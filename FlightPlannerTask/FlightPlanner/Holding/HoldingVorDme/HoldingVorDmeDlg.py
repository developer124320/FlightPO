# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QString, Qt
from PyQt4.QtGui import QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsVectorFileWriter,QgsPoint, QGis, QgsGeometry,\
     QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, \
     QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2,\
     QgsFeature

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes,\
        DistanceUnits,AircraftSpeedCategory, OrientationType, AltitudeUnits, ObstacleAreaResult,\
        TurnDirection, IntersectionStatus
from FlightPlanner.Holding.HoldingVorDme.ui_HoldingVorDme import Ui_HoldingVorDme
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Holding.HoldingRnav.HoldingTemplateRnav import HoldingTemplateRnav
from FlightPlanner.Holding.HoldingTemplate import HoldingTemplate
from FlightPlanner.Panels.WindPanel import WindPanel
from FlightPlanner.Holding.HoldingTemplateBase import HoldingTemplateBase
from FlightPlanner.types import Point3D
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.IasHelp.IasHelpDlg import IasHelpDlg
from FlightPlanner.messages import Messages
from FlightPlanner.AcadHelper import AcadHelper
import define, math

class HoldingVorDmeDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("HoldingOverHeadDlg")
        self.surfaceType = SurfaceTypes.HoldingVorDme
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.HoldingVorDme)
        self.resize(500, 550)
        QgisHelper.matchingDialogSize(self, 650, 700)
        self.surfaceList = None

        self.vorDmeFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.initBasedOnCmb()
    def initBasedOnCmb(self):

        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.vorDmeFeatureArray = self.basedOnCmbFill(self.currentLayer, self.parametersPanel.cmbBasedOn, self.parametersPanel.pnlVorDme)
    def basedOnCmbFill(self, layer, basedOnCmbObj, vorDmePositionPanelObj):
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')
        vorDmeList = []
        vorDmeFeatureList = []
        if idx >= 0:
            featIter = layer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idx].toString()
                attrValue = QString(attrValue)
                attrValue = attrValue.replace(" ", "")
                attrValue = attrValue.replace("/", "")
                attrValue = attrValue.toUpper()
                if attrValue == "VORDME" or attrValue == "VORTAC" or attrValue == "TACAN":
                    vorDmeList.append(attrValue)
                    vorDmeFeatureList.append(feat)
            if len(vorDmeList) != 0:

                i = -1
                basedOnCmbObjItems = []
                resultfeatDict = dict()
                for feat in vorDmeFeatureList:
                    typeValue = feat.attributes()[idx].toString()
                    nameValue = feat.attributes()[idxName].toString()
                    basedOnCmbObjItems.append(typeValue + " " + nameValue)
                    resultfeatDict.__setitem__(typeValue + " " + nameValue, feat)
                basedOnCmbObjItems.sort()
                basedOnCmbObj.Items = basedOnCmbObjItems
                basedOnCmbObj.SelectedIndex = 0

                # if idxAttributes
                feat = resultfeatDict.__getitem__(basedOnCmbObjItems[0])
                attrValue = feat.attributes()[idxLat].toDouble()
                lat = attrValue[0]

                attrValue = feat.attributes()[idxLong].toDouble()
                long = attrValue[0]

                attrValue = feat.attributes()[idxAltitude].toDouble()
                alt = attrValue[0]

                vorDmePositionPanelObj.Point3d = Point3D(long, lat, alt)
                self.connect(basedOnCmbObj, SIGNAL("Event_0"), self.basedOnCmbObj_Event_0)

                return resultfeatDict
        return dict()
    def basedOnCmbObj_Event_0(self):
        if self.currentLayer == None or not self.currentLayer.isValid():
            return
        layer = self.currentLayer
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')

        feat = self.vorDmeFeatureArray.__getitem__(self.parametersPanel.cmbBasedOn.SelectedItem)
        attrValue = feat.attributes()[idxLat].toDouble()
        lat = attrValue[0]

        attrValue = feat.attributes()[idxLong].toDouble()
        long = attrValue[0]

        attrValue = feat.attributes()[idxAltitude].toDouble()
        alt = attrValue[0]

        self.parametersPanel.pnlVorDme.Point3d = Point3D(long, lat, alt)

    
    def initObstaclesModel(self):
        self.obstaclesModel.MocMultiplier = self.parametersPanel.spinBoxMocmulipiler.value()
        return FlightPlanBaseDlg.initObstaclesModel(self)
    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return  
#         self.filterList = []
#         for taaArea in self.taaCalculationAreas:
#             self.filterList.append(taaArea.title)
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.HoldingVorDme, self.ui.tblObstacles, None, parameterList, resultHideColumnNames)
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    
    def getParameterList(self):
        parameterList = []
        parameterList.append(("General", "group"))
        parameterList.append(("VOE/DME Position", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlVorDme.txtPointX.text()), float(self.parametersPanel.pnlVorDme.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlVorDme.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlVorDme.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlVorDme.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlVorDme.txtPointY.text()))
        parameterList.append(("Altitude", self.parametersPanel.pnlVorDme.txtAltitudeFt.text() + "ft"))
        parameterList.append(("", self.parametersPanel.pnlVorDme.txtAltitudeM.text() + "m"))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Used For", self.parametersPanel.cmbUsedFor.currentText()))
        parameterList.append(("Type", self.parametersPanel.cmbType.currentText()))
#         if self.parametersPanel.cmbHoldingFunctionality.currentIndex() != 0:            
#             parameterList.append(("Out-bound Red Limitation", self.parametersPanel.cmbOutboundLimit.currentText()))
#         parameterList.append(("Aircraft Category", self.parametersPanel.cmbAircraftCategory.currentText()))
        parameterList.append(("IAS", self.parametersPanel.txtIas.text() + "kts"))
        parameterList.append(("TAS", self.parametersPanel.txtTas.text() + "kts"))
        parameterList.append(("Altitude", self.parametersPanel.txtAltitudeM.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtAltitude.text() + "ft"))
        parameterList.append(("ISA", self.parametersPanel.txtIsa.text() + unicode("°C", "utf-8")))
        
        parameterList.append(("Wind", self.parametersPanel.pnlWind.speedBox.text() + "kts"))        
        parameterList.append(("Holding DME", self.parametersPanel.txtHoldingDme.text() + "nm"))
        parameterList.append(("Limiting DME", self.parametersPanel.txtLimitingDme.text() + "nm"))
        parameterList.append(("MOC", self.parametersPanel.txtMoc.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtMocFt.text() + "ft"))
#         parameterList.append(("Time", self.parametersPanel.txtTime.text()))
        if self.parametersPanel.chbLimitingRadial.isVisible():
            if self.parametersPanel.chbCatH.isChecked():
                parameterList.append(("Limiting Radial", "Checked"))
            else:
                parameterList.append(("Limiting Radial", "Unchecked"))        
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstruction.currentText()))
        parameterList.append(("MOCmultipiler", str(self.parametersPanel.spinBoxMocmulipiler.value())))
        
        parameterList.append(("Entry Areas", "group"))       
        if self.parametersPanel.chbSector1.isChecked():
            parameterList.append(("Sector1", "Checked"))
        else:
            parameterList.append(("Sector1", "Unchecked")) 
        
        if self.parametersPanel.chbSector2.isChecked():
            parameterList.append(("Sector 2", "Checked"))
        else:
            parameterList.append(("Sector 2", "Unchecked")) 
            
        if self.parametersPanel.chbReciprocalEntry.isChecked():
            parameterList.append(("Reciprocal Entry", "Checked"))
        else:
            parameterList.append(("Reciprocal Entry", "Unchecked")) 
        
    
        parameterList.append(("Orientation", "group"))
        parameterList.append(("In-bound Track", "Plan : " + str(self.parametersPanel.txtTrack.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtTrack.txtRadialGeodetic.Value) + define._degreeStr))

        # parameterList.append(("In-bound Trak", self.parametersPanel.txtTrack.Value + unicode("°", "utf-8")))
        parameterList.append(("Turns", self.parametersPanel.cmbOrientation.currentText()))
        
        parameterList.append(("Results / Checked Obstacles", "group"))   
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList
    
    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        return FlightPlanBaseDlg.uiStateInit(self)
    
        
    def btnPDTCheck_Click(self):
        pdtResultStr = MathHelper.pdtCheckResultToString(float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), float(self.parametersPanel.txtIas.text()))
        
        
        QMessageBox.warning(self, "PDT Check", pdtResultStr)
    def btnEvaluate_Click(self):
        if (self.parametersPanel.cmbType.currentIndex() != 0):
            vorDmeHoldingAway = VorDmeHoldingAway(self);
        else:
            vorDmeHoldingAway = VorDmeHoldingTowards(self);
        altitude_0 = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)
        altitude_1 = Altitude(float(self.parametersPanel.txtMoc.text()))
        if (vorDmeHoldingAway.Valid):
            if (self.parametersPanel.cmbUsedFor.currentIndex() != 0):
                hVDSE = HoldingVorDmeSecondaryEvaluator(vorDmeHoldingAway.BasicArea, altitude_0, altitude_1, Distance(2.5, DistanceUnits.NM));
                self.obstaclesModel = HoldingVorDmeObstacles(False, "second", None, altitude_0, hVDSE.inner, hVDSE.outer, hVDSE.poly, altitude_1, Distance(2.5, DistanceUnits.NM)) 
#                 selectionArea = (holdingVorDmeSecondaryEvaluator as HoldingVorDme.HoldingVorDmeSecondaryEvaluator).SelectionArea;
            else:
                entities = vorDmeHoldingAway.Entities;
                entities.pop(0)
                entities.pop(0)
                num = 0;
                while (num < len(entities)):
                    if (not (entities[num].isGeosValid())):
#                         entities[num].Dispose();
                        entities.pop(num);
                    else:
                        num += 1
                count = len(entities)
                if (count >= 5):
                    num1 = 0.1 * count;
                    metres = altitude_1.Metres;
                    holdingVorDmeAreas = []
                    for i in range(count):
                        if (i > 0):
                            metres = num1 * altitude_1.Metres;
                            num1 = num1 - 0.1;
                        holdingVorDmeAreas.append(HoldingVorDmeArea(PolylineArea.smethod_0(entities[i]), Altitude(metres)));
                    holdingVorDmeSecondaryEvaluator = HoldingVorDmeBufferEvaluator(holdingVorDmeAreas, altitude_0);
                    self.obstaclesModel = HoldingVorDmeObstacles(False, "buffer", holdingVorDmeAreas, altitude_0)
                else:
                    QMessageBox.warning(self, "Warning", Messages.ERR_FAILED_TO_CREATE_BUFFER_AREAS)
#                     raise ValueError(Messages.ERR_FAILED_TO_CREATE_BUFFER_AREAS);
                    return;
        return FlightPlanBaseDlg.btnEvaluate_Click(self)

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        vorDmeHoldingAway = None
        if (self.parametersPanel.cmbType.currentIndex() != 0):
            vorDmeHoldingAway = VorDmeHoldingAway(self);
        else:
            vorDmeHoldingAway = VorDmeHoldingTowards(self);
        resultRegion = []
        resultRegion3D = []
        
        if (vorDmeHoldingAway.Valid):
            entities = vorDmeHoldingAway.Entities;
            if (self.parametersPanel.cmbUsedFor.currentIndex() == 0):
                num = 0;
                for i in range(len(entities)):
                    if (entities[i].isGeosValid()):
                        num += 1
                if (num >= 5):
                    if (self.parametersPanel.cmbConstruction.currentText() != "3D"):
                        resultRegion = entities
                    else:
                        j = len(entities)
                        i = 0
                        while i < j - 1: 
                            region = entities[i + 1]
                            region1 = entities[i]
                            newRegion = region.difference(region1);
                            resultRegion3D.append(newRegion)
                            i += 1
                        resultRegion3D.append(entities[0])
                else:
                    num2 = 0;
                    while (num2 < entities.Count):
                        if (not (entities[num2].isGeosValid())):
                            num2 += 1
                        else:
                            entities.remove(entities[num2]);
                    raise ValueError(Messages.ERR_FAILED_TO_CREATE_BUFFER_AREAS);
                    return;
            elif (self.parametersPanel.cmbConstruction.currentText() == "2D"):
                item1 = entities[0]
                resultRegion.append(item1)
                polyline1 = entities[1]
                resultRegion.append(polyline1)
                distance = Distance(2.5, DistanceUnits.NM);
                resultRegion.append(QgsGeometry.fromPolygon([vorDmeHoldingAway.BasicArea.method_14_closed(4)]))
                for entity1 in HoldingTemplateBase.smethod_2(vorDmeHoldingAway.BasicArea, distance):
                    resultRegion.append(QgsGeometry.fromPolygon([entity1.method_14_closed(4)]))
            elif (self.parametersPanel.cmbConstruction.currentText() == "3D"):
                item2 = entities[0]
                resultRegion3D.append(item2)
                polyline2 = entities[1]
                resultRegion3D.append(polyline2)
                distance1 = Distance(2.5, DistanceUnits.NM);
                polylineArea, polylineArea1 = HoldingTemplateBase.smethod_4(vorDmeHoldingAway.BasicArea, Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), Altitude(float(self.parametersPanel.txtMoc.text())), distance1);
                polygonList = QgisHelper.smethod_146(polylineArea.method_15(False), polylineArea1.method_15(False));
                for poly in polygonList:
                    resultRegion3D.append(poly)
        mapUnits = define._canvas.mapUnits()
        constructionLayer = None
        if self.parametersPanel.cmbConstruction.currentText() != "3D":
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType)
            # if define._mapCrs == None:
            #     if mapUnits == QGis.Meters:
            #         constructionLayer = QgsVectorLayer("linestring?crs=EPSG:32633", self.surfaceType, "memory")
            #     else:
            #         constructionLayer = QgsVectorLayer("linestring?crs=EPSG:4326", self.surfaceType, "memory")
            # else:
            #     constructionLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")
            # shpPath = ""
            # if define.obstaclePath != None:
            #     shpPath = define.obstaclePath
            # elif define.xmlPath != None:
            #     shpPath = define.xmlPath
            # else:
            #     shpPath = define.appPath
            # er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + QString(self.surfaceType).replace(" ", "") + ".shp", "utf-8", constructionLayer.crs())
            # constructionLayer = QgsVectorLayer(shpPath + "/" + QString(self.surfaceType).replace(" ", "") + ".shp", self.surfaceType, "ogr")
            #
            # constructionLayer.startEditing()
            
            for region in resultRegion:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, PolylineArea(region.asPolygon()[0]))
                # feature = QgsFeature()
                # feature.setGeometry(QgsGeometry.fromPolyline(region.asPolygon()[0]))
                # constructionLayer.addFeature(feature)
            
            # constructionLayer.commitChanges()
        else:
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Polygon)
            # if define._mapCrs == None:
            #     if mapUnits == QGis.Meters:
            #         constructionLayer = QgsVectorLayer("polygon?crs=EPSG:32633", self.surfaceType, "memory")
            #     else:
            #         constructionLayer = QgsVectorLayer("polygon?crs=EPSG:4326", self.surfaceType, "memory")
            # else:
            #     constructionLayer = QgsVectorLayer("polygon?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")
            # shpPath = ""
            # if define.obstaclePath != None:
            #     shpPath = define.obstaclePath
            # elif define.xmlPath != None:
            #     shpPath = define.xmlPath
            # else:
            #     shpPath = define.appPath
            # er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + QString(self.surfaceType).replace(" ", "") + ".shp", "utf-8", constructionLayer.crs())
            # constructionLayer = QgsVectorLayer(shpPath + "/" + QString(self.surfaceType).replace(" ", "") + ".shp", self.surfaceType, "ogr")
            #
            # constructionLayer.startEditing()
            #
            i = 0
            for region in resultRegion3D:
                i += 1
                feature = QgsFeature()
                if region == None:
                    continue
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, PolylineArea(resultRegion3D[len(resultRegion3D) - i].asPolygon()[0]))
            #     feature.setGeometry(region)
            #     constructionLayer.addFeature(feature)
            #
            # constructionLayer.commitChanges()
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType, True)
        self.resultLayerList = [constructionLayer]
        QgisHelper.zoomToLayers([constructionLayer]) 
        self.ui.btnEvaluate.setEnabled(True)
    def initParametersPan(self):
        ui = Ui_HoldingVorDme()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        
        ui.frameAircraftCategory.hide()
        self.parametersPanel.txtTas.setEnabled(False)
        self.parametersPanel.chbLimitingRadial.setVisible(False)
        
        self.parametersPanel.pnlVorDme = PositionPanel(self.parametersPanel.gbVorDmePosition)
#         self.parametersPanel.pnlWaypoint.groupBox.setTitle("FAWP")
        self.parametersPanel.pnlVorDme.btnCalculater.hide()
#         self.parametersPanel.pnlNavAid.hideframe_Altitude()
        self.parametersPanel.pnlVorDme.setObjectName("pnlVorDme")
        ui.vl_VorDmePosition.addWidget(self.parametersPanel.pnlVorDme)
        self.connect(self.parametersPanel.pnlVorDme, SIGNAL("positionChanged"), self.initResultPanel)
        self.connect(self.parametersPanel.pnlVorDme, SIGNAL("positionChanged"), self.iasChanged)
        
        self.parametersPanel.pnlWind = WindPanel(self.parametersPanel.gbParameters)
        self.parametersPanel.pnlWind.lblIA.setMinimumSize(113, 0)
        self.parametersPanel.vl_gbParameters.insertWidget(7, self.parametersPanel.pnlWind)
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
#                
        self.parametersPanel.cmbType.addItems(["Towards the Station", "Away From the Station"])
#         self.parametersPanel.cmbAircraftCategory.addItems(["A", "B", "C", "D", "E", "H", "Custom"])
        self.parametersPanel.cmbUsedFor.addItems(["Holding", "Racetrack"])
#         self.parametersPanel.cmbUsedFor.setCurrentIndex(1)
        self.parametersPanel.cmbConstruction.addItems(["2D", "3D"])
        self.parametersPanel.cmbOrientation.addItems(["Right", "Left"])
#         
        
        self.parametersPanel.cmbType.currentIndexChanged.connect(self.cmbTypeCurrentIndexChanged)
        self.parametersPanel.cmbUsedFor.currentIndexChanged.connect(self.cmbUsedForCurrentIndexChanged)
        # self.parametersPanel.btnCaptureTrack.clicked.connect(self.captureBearing)
        self.parametersPanel.btnCaptureHoldingDme.clicked.connect(self.measureDistanceHD)
        self.parametersPanel.btnCaptureLimitingDme.clicked.connect(self.measureDistanceLD)        
        self.parametersPanel.txtAltitude.textChanged.connect(self.altitudeChanged)
#         self.parametersPanel.cmbAircraftCategory.currentIndexChanged.connect(self.changeCategory)
#         self.parametersPanel.btnIasHelp.clicked.connect(self.iasHelpShow)
        self.parametersPanel.txtIas.textChanged.connect(self.iasChanged)
        self.parametersPanel.txtIsa.textChanged.connect(self.iasChanged)
        self.parametersPanel.txtAltitude.textChanged.connect(self.iasChanged)
        self.parametersPanel.txtAltitudeM.textChanged.connect(self.txtAltitudeMChanged)
        self.parametersPanel.txtAltitude.textChanged.connect(self.txtAltitudeFtChanged)

        self.flag = 0
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")

        self.parametersPanel.txtMoc.textChanged.connect(self.txtMocMChanged)
        self.parametersPanel.txtMocFt.textChanged.connect(self.txtMocFtChanged)

        self.flag1 = 0
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtMocFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMoc.text())), 4)))
            except:
                self.parametersPanel.txtMocFt.setText("0.0")

        self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT) - self.parametersPanel.pnlVorDme.Altitude()).Knots, 4)))
    def txtAltitudeMChanged(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.parametersPanel.txtAltitude.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM.text())), 4)))
            except:
                self.parametersPanel.txtAltitude.setText("0.0")
    def txtAltitudeFtChanged(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")

    def txtMocMChanged(self):
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtMocFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMoc.text())), 4)))
            except:
                self.parametersPanel.txtMocFt.setText("0.0")
    def txtMocFtChanged(self):
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                self.parametersPanel.txtMoc.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtMocFt.text())), 4)))
            except:
                self.parametersPanel.txtMoc.setText("0.0")
    def cmbUsedForCurrentIndexChanged(self, index):
        pass

    def cmbTypeCurrentIndexChanged(self, index):
        if index == 1:
            self.parametersPanel.chbLimitingRadial.setVisible(True)
        else:
            self.parametersPanel.chbLimitingRadial.setVisible(False)
        pass
    def iasChanged(self):
        try:
            self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT) - self.parametersPanel.pnlVorDme.Altitude()).Knots, 4)))
        except:
            raise ValueError("Value Invalid")
#         
#     def iasHelpShow(self):
#         dlg = IasHelpDlg()
#         dlg.exec_()
    def altitudeChanged(self):
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
        self.iasChanged()
    def method_27(self):
        pass
        
    def method_33(self, distance_0, bool_0):
        num = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT).Metres
        num1 = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT).Feet
        altitude = Altitude(float(self.parametersPanel.pnlVorDme.txtAltitudeM.text()))
        num2 = num - altitude.Metres
        num3 = Unit.ConvertMeterToNM(math.sqrt(distance_0.Metres * distance_0.Metres + num2 * num2));
        if (not bool_0):
            num3 = round(num3, 0);
        else:
            num4 = num3 - math.trunc(num3);
            if (num1 > 14000 or num4 >= 0.25):
                num3 = MathHelper.smethod_0(num3, 0) if(num1 <= 14000 or num4 >= 0.5) else MathHelper.smethod_1(num3, 0)
            else:
                num3 = MathHelper.smethod_1(num3, 0);
        return Distance(num3, DistanceUnits.NM);
    def method_35(self):
        point3d = self.parametersPanel.pnlNavAid.Point3d;
        value = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT);
        metres = value.Metres - point3d.get_Z();
        if (self.parametersPanel.cmbNavAidType.currentIndex() != 0):
            num = 25;
            num1 = 15;
            num2 = metres * 0.839099631;
        else:
            num = 15;
            num1 = 5;
            num2 = metres * 1.191753593;
        num3 = 1 if(self.parametersPanel.cmbOrientation.currentText() == OrientationType.Right) else -1
        num4 = MathHelper.smethod_3(float(self.parametersPanel.txtTrack.Value))
        point3d1 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(num4 + num3 * num), num2).smethod_167(0);
        point3d2 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(num4 + 180 - num3 * num1), num2).smethod_167(0);
        point3d3 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(num4 - num3 * num), num2).smethod_167(0);
        point3d4 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(num4 + 180 + num3 * num1), num2).smethod_167(0);
        point3dArray = [point3d1, point3d2, point3d4, point3d3]
        polylineArea = PolylineArea(point3dArray);
        polylineArea[3].set_Bulge( MathHelper.smethod_60(point3d3, MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(num4), num2).smethod_167(0), point3d1))
        polylineArea[1].set_Bulge( MathHelper.smethod_60(point3d2, MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(num4 + 180), num2).smethod_167(0), point3d4))
        return polylineArea;

    def measureDistanceHD(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtHoldingDme, DistanceUnits.NM)
        define._canvas.setMapTool(measureDistanceTool)
    def measureDistanceLD(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtLimitingDme, DistanceUnits.NM)
        define._canvas.setMapTool(measureDistanceTool)
class HoldingVorDmeArea:
    def __init__(self, polylineArea_0, altitude_0):
        self.area = PrimaryObstacleArea(polylineArea_0);
        self.moc = altitude_0.Metres;
    
    
    def get_area(self):
        return self.area;
    Area = property(get_area, None, None, None)
    
    def get_moc(self):
        return self.moc;
    Moc = property(get_moc, None, None, None)

    def method_0(self, obstacle_0):
        double_0 = self.moc * obstacle_0.MocMultiplier;
        double_1 = None;
        if (not self.area.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
            return (False, double_0, double_1)
        position = obstacle_0.Position;
        double_1 = position.get_Z() + obstacle_0.Trees + double_0;
        return (True, double_0, double_1)
    
class HoldingVorDmeBufferEvaluator:
    def __init__(self, list_0, altitude_0):
        self.areas = list_0;
        self.altitude = altitude_0.Metres;
class HoldingVorDmeSecondaryEvaluator:
    def __init__(self, polylineArea_0, altitude_0, altitude_1, distance_0):
        self.inner = PrimaryObstacleArea(polylineArea_0);
        self.outer = PrimaryObstacleArea(HoldingTemplateBase.smethod_5(polylineArea_0, distance_0));
        self.poly = PolylineArea.smethod_131(self.inner.previewArea);
        self.altitude = altitude_0.Metres;
        self.moc = altitude_1.Metres;
        self.offset = distance_0;
class HoldingVorDmeObstacles(ObstacleTable):
    def __init__(self, bool_0, typeStr, surfacesList = None, altitude = None, inner = None, outer = None, poly = None, altitude_1 = None, distance_0 = None):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
         
        self.surfaceType = SurfaceTypes.HoldingVorDme
        self.obstaclesChecked = None
        self.typeStr = typeStr
        self.altitude = altitude.Metres
        if self.typeStr == "buffer":            
            self.surfacesList = surfacesList
             
        else:
            self.inner = inner
            self.outer = outer
            self.poly = poly
            self.moc = altitude_1.Metres
            self.offset = distance_0
        self.bool = bool_0
    def setHiddenColumns(self, tableView):
        tableView.hideColumn(self.IndexObstArea)
        tableView.hideColumn(self.IndexDistInSecM)
        return ObstacleTable.setHiddenColumns(self, tableView)
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        newHeaderCount = 0
        if bool:
            self.IndexObstArea = fixedColumnCount 
            self.IndexDistInSecM = fixedColumnCount + 1
            self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM
                ])
            newHeaderCount = 2
        self.IndexMocAppliedM = fixedColumnCount + newHeaderCount
        self.IndexMocAppliedFt = fixedColumnCount + 1 + newHeaderCount
        self.IndexMocMultiplier = fixedColumnCount + 2 + newHeaderCount
        self.IndexOcaM = fixedColumnCount + 3 + newHeaderCount
        self.IndexOcaFt = fixedColumnCount + 4 + newHeaderCount
        self.IndexCritical = fixedColumnCount + 5 + newHeaderCount
                  
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt,
                ObstacleTableColumnType.Critical            
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
#     
    def addObstacleToModel(self, obstacle, checkResult):
        if self.typeStr == "buffer":
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
        else:
            ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
            row = self.source.rowCount() - 1
         
            item = QStandardItem(str(checkResult[0]))
            item.setData(checkResult[0])
            self.source.setItem(row, self.IndexObstArea, item)
             
            item = QStandardItem(str(checkResult[1]))
            item.setData(checkResult[1])
            self.source.setItem(row, self.IndexDistInSecM, item)
             
            item = QStandardItem(str(checkResult[2]))
            item.setData(checkResult[2])
            self.source.setItem(row, self.IndexMocAppliedM, item)
               
            item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[2])))
            item.setData(Unit.ConvertMeterToFeet(checkResult[2]))
            self.source.setItem(row, self.IndexMocAppliedFt, item)
               
            item = QStandardItem(str(ObstacleTable.MocMultiplier))
            item.setData(ObstacleTable.MocMultiplier)
            self.source.setItem(row, self.IndexMocMultiplier, item)
               
            item = QStandardItem(str(checkResult[3]))
            item.setData(checkResult[3])
            self.source.setItem(row, self.IndexOcaM, item)
               
            item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
            item.setData(Unit.ConvertMeterToFeet(checkResult[3]))
            self.source.setItem(row, self.IndexOcaFt, item)
             
            item = QStandardItem(str(checkResult[4]))
            item.setData(checkResult[4])
            self.source.setItem(row, self.IndexCritical, item) 
             
    def checkObstacle(self, obstacle_0):
        if self.typeStr == "buffer":
            criticalObstacleType = CriticalObstacleType.No;
            for current in self.surfacesList:
                result, num, num1 = current.method_0(obstacle_0)
                if (result):
                    if (num1 > self.altitude):
                        criticalObstacleType = CriticalObstacleType.Yes;
                    checkResult = []
                    checkResult.append(num)
                    checkResult.append(num1)
                    checkResult.append(criticalObstacleType)
                    self.addObstacleToModel(obstacle_0, checkResult)
                    break
        else:
            mocMultiplier = self.moc * obstacle_0.MocMultiplier;
            metres = None
            num = None
            obstacleAreaResult = ObstacleAreaResult.Outside;
            if (not self.inner.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
                num = MathHelper.calcDistance(self.poly.getClosestPointTo(obstacle_0.Position, False), obstacle_0.Position) - obstacle_0.Tolerance;
                if (num > self.offset.Metres):
                    return;
                metres = mocMultiplier * (1 - num / self.offset.Metres);
                obstacleAreaResult = ObstacleAreaResult.Secondary;
            else:
                metres = mocMultiplier;
                obstacleAreaResult = ObstacleAreaResult.Primary;
            position = obstacle_0.Position;
            z = position.get_Z() + obstacle_0.Trees + metres;
            criticalObstacleType = CriticalObstacleType.No;
            if (z > self.altitude):
                criticalObstacleType = CriticalObstacleType.Yes;
            checkResult = []
            checkResult.append(obstacleAreaResult)
            checkResult.append(num)
            checkResult.append(metres)
            checkResult.append(z)
            checkResult.append(criticalObstacleType)
            self.addObstacleToModel(obstacle_0, checkResult)
class VordDmeHoldingBase:
    def __init__(self):
        self.nominal = None
        self.tolerance = None
        self.basicArea = None
        self.sector1 = None
        self.sector2 = None
        self.sector3 = None
        self.re = None
        self.rl = None
        self.sign = None
        self.valid = None
    def get_basicArea(self):
        polylineArea = None
#         Autodesk.AutoCAD.DatabaseServices.Region region = None;
        polyline = PolylineArea.smethod_136(self.basicArea, False)
        polyline1 = None
        if (self.sector1 != None):
            polyline1 = PolylineArea.smethod_131(self.sector1)
        polyline2 = None
        if (self.sector2 != None):
            polyline2 = PolylineArea.smethod_131(self.sector2)
        polyline3 = None
        if (self.sector3 != None):
            polyline3 = PolylineArea.smethod_131(self.sector3)
        region = self.method_0(polyline);
        if (polyline1 != None):
            region1 = self.method_0(polyline1)
            region = region.combine(region1)
        if (polyline2 != None):
            region2 = self.method_0(polyline2);
            region = region.combine(region2)
        if (polyline3 != None):
            region3 = self.method_0(polyline3)
            region = region.combine(region3)
        polylineArea = PolylineArea.smethod_0(region)
        return polylineArea;
    
    BasicArea = property(get_basicArea, None, None, None)
    
    def get_Entities(self):
        entities = []
        
        entities.append(QgsGeometry.fromPolygon([PolylineArea.smethod_136(self.tolerance, True).method_14_closed(4)]))

        entities.append(QgsGeometry.fromPolygon([PolylineArea.smethod_136(self.nominal, True).method_14_closed(4)]))
        entities1 = [PolylineArea.smethod_136(self.nominal, True), PolylineArea.smethod_136(self.tolerance, True)]
        polyline = PolylineArea.smethod_136(self.basicArea, False);
#         entities.append(QgsGeometry.fromPolygon([PolylineArea.smethod_136(self.basicArea, False).method_14_closed(4)]))
        polyline1 = None;
        if (self.sector1 != None):
            polyline1 = PolylineArea.smethod_131(self.sector1);
        polyline2 = None;
        if (self.sector2 != None):
            polyline2 = PolylineArea.smethod_131(self.sector2)
        polyline3 = None;
        if (self.sector3 != None):
            polyline3 = PolylineArea.smethod_131(self.sector3)
        for i in range(0, 6):
            num = 1852.0 * self.sign * i
            region = self.method_1(polyline, num)
            if (polyline1 != None):
                region1 = self.method_1(polyline1, -num);
                region = region.combine(region1)
            if (polyline2 != None):
                region2 = self.method_1(polyline2, num);
                region = region.combine(region2)
            if (polyline3 != None):
                region3 = self.method_1(polyline3, num);
                region = region.combine(region3)
            entities.append(region)
        return entities
    Entities = property(get_Entities, None, None, None)
    
    def get_RE(self):
        return Unit.smethod_1(self.re);
    RE = property(get_RE, None, None, None)
    
    def get_RL(self):
        return Unit.smethod_1(self.rl);
    RL = property(get_RL, None, None, None)
    
    def get_Valid(self):
        return self.valid
    Valid = property(get_Valid, None, None, None)
    
    
    def method_0(self, polyline_0):
        return QgsGeometry.fromPolygon([polyline_0.method_14_closed(4)])
  
    def method_1(self, polyline_0, double_0):
        item = None;
        for i in range(9):
            if (double_0 >= 0):
                double_0 = double_0 + i * 0.2;
            else:
                double_0 = double_0 - i * 0.2;
            offsetCurves = QgisHelper.offsetCurve(polyline_0.method_14_closed(4), double_0);
            try:
                item = QgsGeometry.fromPolygon([offsetCurves])
            except:
                item = None;
#             AcadHelper.smethod_25(offsetCurves);
            if (item != None):
                return item;
#         QMessageBox.warning(HoldingVorDmeDlg, "Warning", Messages.ERR_FAILED_TO_CREATE_SECONDARY_AREAS)
        raise ValueError(Messages.ERR_FAILED_TO_CREATE_SECONDARY_AREAS)
    
class VorDmeHoldingAway(VordDmeHoldingBase):
    def __init__(self, holdingVorDme_0):
        self.nominal = None
        self.tolerance = None
        self.basicArea = None
        self.sector1 = None
        self.sector2 = None
        self.sector3 = None
        self.re = None
        self.rl = None
        self.sign = None
        self.valid = None
        point3d33 = holdingVorDme_0.parametersPanel.pnlVorDme.Point3d;
        value = Speed(float(holdingVorDme_0.parametersPanel.txtIas.text()))
        altitude = Altitude(float(holdingVorDme_0.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)
        speed = Speed(float(holdingVorDme_0.parametersPanel.pnlWind.speedBox.text()))
        value1 = float(holdingVorDme_0.parametersPanel.txtIsa.text())
        distance = Distance(float(holdingVorDme_0.parametersPanel.txtHoldingDme.text()), DistanceUnits.NM)
        distance1 = Distance(float(holdingVorDme_0.parametersPanel.txtLimitingDme.text()),DistanceUnits.NM)
        orientationType = holdingVorDme_0.parametersPanel.cmbOrientation.currentText()
        value2 = float(holdingVorDme_0.parametersPanel.txtTrack.Value)
        speed1 = Speed.smethod_0(value, value1, altitude);
        num20 = Unit.ConvertDegToRad(value2);
        num21 = Unit.ConvertDegToRad(value2 + 180);
        self.sign = 1 if(orientationType == OrientationType.Right) else -1
        turnDirection = TurnDirection.Right if(orientationType == OrientationType.Right) else TurnDirection.Left
        turnDirection1 = TurnDirection.Left if(orientationType == OrientationType.Right) else TurnDirection.Right
        num22 = min([943.27 / speed1.KilometresPerHour, 3]);
        num23 = Unit.ConvertKMToMeters(speed1.KilometresPerHour / (62.8318530717959 * num22));
        metres = altitude.Metres - point3d33.get_Z();
        num24 = max(math.tan(Unit.ConvertDegToRad(55)) * metres, 2 * num23);
        num25 = speed1.MetresPerSecond * 60 if(altitude.Feet <= 14000) else speed1.MetresPerSecond * 90
        metres1 = distance1.Metres;
        try:
            num26 = math.sqrt(metres1 * metres1 - metres * metres);
        except:
            num26 = None
        if (num26 == None or num24 >= num26):
            distance1 = Distance(MathHelper.smethod_0(Unit.ConvertMeterToNM(math.sqrt(num24 * num24 + metres * metres)), 0), DistanceUnits.NM);
            QMessageBox.warning(holdingVorDme_0, "Warning", Messages.LIMITING_DME_DISTANCE_WITHIN_OVERHEAD_TOLERANCE + str(distance1.NauticalMiles) + "nm.");
            holdingVorDme_0.parametersPanel.txtLimitingDme.setText(str(distance1.NauticalMiles))
            metres1 = distance1.Metres;
            num26 = math.sqrt(metres1 * metres1 - metres * metres);
        metres2 = distance.Metres;
        num27 = math.sqrt(metres2 * metres2 - metres * metres);
        try:
            num28 = num27 - math.sqrt(num26 * num26 - 4 * num23 * num23);
        except:
            num28 = None
        if (num28 == None or num28 < num25):
            num29 = math.sqrt((num27 - num25) * (num27 - num25) + 4 * num23 * num23);
            distance2 = holdingVorDme_0.method_33(Distance(num29), True);
            if (num29 <= num24 or distance2.Metres >= distance1.Metres):
                num30 = math.sqrt(num26 * num26 - 4 * num23 * num23) + num25;
                distance3 = holdingVorDme_0.method_33(Distance(num30), False);
                if (distance3.Metres > distance.Metres):
                    distance = distance3;
                    QMessageBox.warning(holdingVorDme_0, "Warning", Messages.HOLDING_DME_DISTANCE_TOO_CLOSE + str(distance.NauticalMiles) + "nm.")
                    holdingVorDme_0.parametersPanel.txtHoldingDme.setText(str(distance.NauticalMiles))
                    metres2 = distance.Metres;
                    num27 = math.sqrt(metres2 * metres2 - metres * metres);
            else:
                distance1 = distance2;
#                 InfoMessageBox.smethod_0(holdingVorDme_0, string.Format(Messages.LIMITING_DME_DISTANCE_TOO_FAR, distance1.method_0(":u")));
                QMessageBox.warning(holdingVorDme_0, "Warning", Messages.LIMITING_DME_DISTANCE_TOO_FAR + str(distance1.NauticalMiles) + "nm.")
                holdingVorDme_0.parametersPanel.txtLimitingDme.setText(str(distance1.NauticalMiles))
                metres1 = distance1.Metres;
                num26 = math.sqrt(metres1 * metres1 - metres * metres);
        num25 = num27 - math.sqrt(metres1 * metres1 - 4 * num23 * num23 - metres * metres);
        metresPerSecond = num25 / speed1.MetresPerSecond / 60;
        num31 = Unit.ConvertDegToRad(5.2) * self.sign;
        metres3 = Distance.smethod_2(distance).Metres;
        metres4 = Distance.smethod_2(distance1).Metres;
        num32 = num27 + metres3;
        num33 = num27 - metres3;
        num34 = num26 + metres4;
        num35 = num26 - metres4;
        point3d34 = MathHelper.distanceBearingPoint(point3d33, num20, num27);
        point3d35 = MathHelper.distanceBearingPoint(point3d33, num20 + num31, num32);
        point3d36 = MathHelper.distanceBearingPoint(point3d33, num20 - num31, num32);
        point3d37 = MathHelper.distanceBearingPoint(point3d33, num20 + num31, num33);
        point3d38 = MathHelper.distanceBearingPoint(point3d33, num20 - num31, num33);
        self.nominal = PolylineArea();
        point3d39 = point3d34;
        point3d40 = MathHelper.distanceBearingPoint(point3d39, num21 - 1.5707963267949 * self.sign, 2 * num23);
        self.nominal.method_3(point3d39, MathHelper.smethod_59(num20, point3d39, point3d40));
        self.nominal.method_1(point3d40);
        point3d39 = MathHelper.distanceBearingPoint(point3d40, num21, num25);
        point3d40 = MathHelper.distanceBearingPoint(point3d39, num20 - 1.5707963267949 * self.sign, 2 * num23);
        self.nominal.method_3(point3d39, MathHelper.smethod_59(num21, point3d39, point3d40));
        self.nominal.method_1(point3d40);
        point3d41 = point3d39;
        self.tolerance = PolylineArea();
        point3d39 = MathHelper.distanceBearingPoint(point3d33, num20, num32);
        point3d40 = MathHelper.distanceBearingPoint(point3d33, num20, num33);
        self.tolerance.method_1(point3d35);
        self.tolerance.method_3(point3d37, MathHelper.smethod_60(point3d37, point3d40, point3d38));
        self.tolerance.method_1(point3d38);
        self.tolerance.method_3(point3d36, MathHelper.smethod_60(point3d36, point3d39, point3d35));
        self.tolerance.method_1(point3d35);
        holdingTemplate = HoldingTemplate(point3d35, value2, value, altitude, speed, value1, metresPerSecond, orientationType);
        holdingTemplate1 = HoldingTemplate(point3d36, value2, value, altitude, speed, value1, metresPerSecond, orientationType);
        position = holdingTemplate.OutboundLineTop[0].Position;
        position1 = holdingTemplate.OutboundLineTop[1].Position;
        position2 = holdingTemplate1.OutboundLineBottom[0].Position;
        position3 = holdingTemplate1.OutboundLineBottom[1].Position;
        point3d5_0 = []
        intersectionStatu = MathHelper.smethod_34(position, position1, point3d33, num35, point3d5_0)
        point3d5 = point3d5_0[0]
        point3d = point3d5_0[1]
        origin1 = Point3D.get_Origin();
        origin2 = Point3D.get_Origin();
        if (holdingVorDme_0.parametersPanel.chbLimitingRadial.isChecked() or intersectionStatu == IntersectionStatus.Nothing):
            if ( not holdingVorDme_0.parametersPanel.chbLimitingRadial.isChecked()):
                if (QMessageBox.warning(holdingVorDme_0, "Warning", "APPLY_LIMITING_RADIAL") == QMessageBox.No):
                    self.valid = False;
                    return;
                holdingVorDme_0.parametersPanel.chbLimitingRadial.setChecked(True)
            holdingTemplate2 = HoldingTemplate(point3d37, value2, value, altitude, speed, value1, metresPerSecond, orientationType);
            pointR = holdingTemplate2.PointR;
            num36 = Unit.ConvertDegToRad(4.5);
            num37 = MathHelper.getBearing(point3d33, point3d34);
            num38 = MathHelper.getBearing(point3d33, pointR);
            num39 = MathHelper.smethod_53(num37, num38) if(orientationType == OrientationType.Right) else MathHelper.smethod_53(num38, num37)
            num39 = Unit.ConvertDegToRad(MathHelper.smethod_0(Unit.smethod_1(num39 + num36), 0));
            self.rl = MathHelper.smethod_4(num37 + num39 if(orientationType == OrientationType.Right) else num37 - num39)
            num40 = MathHelper.smethod_4(num37 + num39 + num36 if(orientationType == OrientationType.Right) else num37 - num39 - num36)
            origin2 = MathHelper.distanceBearingPoint(point3d33, num40, num26);
            point3d0_6 = []
            MathHelper.smethod_34(point3d33, origin2, point3d33, num34, point3d0_6);
            point3d = point3d0_6[0]
            point3d6 = point3d0_6[1]
            point3d0_7 = []
            MathHelper.smethod_34(point3d33, origin2, point3d33, num35, point3d0_7);
            point3d = point3d0_7[0]
            point3d7 = point3d0_7[1]
            point3d8 = MathHelper.getIntersectionPoint(position, position1, point3d33, origin2);
            point3d1_8 = []
            intersectionStatu = MathHelper.smethod_34(position, position1, point3d33, num34, point3d1_8);
            origin1 = point3d1_8[0]
            point3d = point3d1_8[1]
            if (intersectionStatu != IntersectionStatus.Nothing):
                point3d5_0 = []
                intersectionStatu = MathHelper.smethod_34(position, position1, point3d33, num35, point3d5_0);
                point3d5 = point3d5_0[0]
                point3d = point3d5_0[1]
                if (intersectionStatu == IntersectionStatus.Nothing):
                    origin1 = point3d8;
                    point3d5 = point3d7;
                elif (orientationType == OrientationType.Right):
                    if (not MathHelper.smethod_115(origin1, point3d33, origin2) or not MathHelper.smethod_115(point3d5, point3d33, origin2)):
                        origin1 = point3d8;
                        point3d5 = point3d7;
                    else:
                        self.rl = None
                        holdingVorDme_0.parametersPanel.chbLimitingRadial.setChecked(False)
                elif (not MathHelper.smethod_119(origin1, point3d33, origin2) or not MathHelper.smethod_119(point3d5, point3d33, origin2)):
                    origin1 = point3d8;
                    point3d5 = point3d7;
                else:
                    self.rl = None
                    holdingVorDme_0.parametersPanel.chbLimitingRadial.setChecked(False)
            else:
                origin1 = point3d8;
                point3d5 = point3d7;
        point3d9_0 = []
        MathHelper.smethod_34(position2, position3, point3d33, num34, point3d9_0);
        point3d9 = point3d9_0[0]
        point3d = point3d9_0[1]
        point3d10_0 = []
        MathHelper.smethod_34(position2, position3, point3d33, num35, point3d10_0);
        point3d10 = point3d10_0[0]
        point3d = point3d9_0[1]
        if (orientationType != OrientationType.Right):
            if (MathHelper.smethod_115(point3d9, point3d36, point3d38)):
                point3d9_0 = []
                MathHelper.smethod_34(point3d36, point3d38, point3d33, num34, point3d9_0);
                point3d9 = point3d9_0[0]
                point3d = point3d9_0[1]
            if (MathHelper.smethod_115(point3d10, point3d36, point3d38)):
                point3d10_0 = []
                MathHelper.smethod_34(point3d36, point3d38, point3d33, num35, point3d10_0);
                point3d10 = point3d10_0[0]
                point3d = point3d9_0[1]
        else:
            if (MathHelper.smethod_119(point3d9, point3d36, point3d38)):
                point3d9_0 = []
                MathHelper.smethod_34(point3d36, point3d38, point3d33, num34, point3d9_0);
                point3d9 = point3d9_0[0]
                point3d = point3d9_0[1]
            if (MathHelper.smethod_119(point3d10, point3d36, point3d38)):
                point3d10_0 = []
                MathHelper.smethod_34(point3d36, point3d38, point3d33, num35, point3d10_0);
                point3d9 = point3d9_0[0]
                point3d = point3d9_0[1]
        point3d42 = MathHelper.distanceBearingPoint(point3d5, MathHelper.getBearing(point3d5, point3d10), MathHelper.calcDistance(point3d5, point3d10) / 2);
        point3d42 = MathHelper.distanceBearingPoint(point3d33, MathHelper.getBearing(point3d33, point3d42), num35);
        holdingTemplate3 = None;
        holdingTemplate4 = HoldingTemplate(point3d5, value2 + 180, value, altitude, speed, value1, metresPerSecond, orientationType);
        holdingTemplate5 = HoldingTemplate(point3d42, value2 + 180, value, altitude, speed, value1, metresPerSecond, orientationType);
        holdingTemplate6 = HoldingTemplate(point3d10, value2 + 180, value, altitude, speed, value1, metresPerSecond, orientationType);
        holdingTemplate7 = HoldingTemplate(point3d9, value2 + 180, value, altitude, speed, value1, metresPerSecond, orientationType);
        point3d11, num = MathHelper.smethod_73(holdingTemplate1.Spiral[1].Position, holdingTemplate1.Spiral[2].Position, holdingTemplate1.Spiral[1].Bulge);
        point3d12, num1 = MathHelper.smethod_73(holdingTemplate1.Spiral[2].Position, holdingTemplate1.Spiral[3].Position, holdingTemplate1.Spiral[2].Bulge);
        point3d13, num2 = MathHelper.smethod_73(holdingTemplate.Spiral[2].Position, holdingTemplate.Spiral[3].Position, holdingTemplate.Spiral[2].Bulge);
        if (self.rl == None):
            origin = Point3D.get_Origin();
            num3 = None
        else:
            holdingTemplate3 = HoldingTemplate(origin1, value2 + 180, value, altitude, speed, value1, metresPerSecond, orientationType);
            origin, num3 = MathHelper.smethod_73(holdingTemplate3.Spiral[1].Position, holdingTemplate3.Spiral[2].Position, holdingTemplate3.Spiral[1].Bulge);
        point3d14, num4 = MathHelper.smethod_73(holdingTemplate4.Spiral[1].Position, holdingTemplate4.Spiral[2].Position, holdingTemplate4.Spiral[1].Bulge);
        point3d15, num5 = MathHelper.smethod_73(holdingTemplate4.Spiral[2].Position, holdingTemplate4.Spiral[3].Position, holdingTemplate4.Spiral[2].Bulge);
        point3d16, num6 = MathHelper.smethod_73(holdingTemplate5.Spiral[2].Position, holdingTemplate5.Spiral[3].Position, holdingTemplate5.Spiral[2].Bulge);
        point3d17, num7 = MathHelper.smethod_73(holdingTemplate6.Spiral[2].Position, holdingTemplate6.Spiral[3].Position, holdingTemplate6.Spiral[2].Bulge);
        point3d18, num8 = MathHelper.smethod_73(holdingTemplate6.Spiral[3].Position, holdingTemplate6.Spiral[4].Position, holdingTemplate6.Spiral[3].Bulge);
        point3d19, num9 = MathHelper.smethod_73(holdingTemplate7.Spiral[3].Position, holdingTemplate7.Spiral[4].Position, holdingTemplate7.Spiral[3].Bulge);
        point3d20, num10 = MathHelper.smethod_193(point3d15, num5, point3d16, num6, point3d17, num7, True);
        point3d43 = MathHelper.distanceBearingPoint(point3d20, MathHelper.getBearing(point3d20, point3d15), num10);
        point3d44 = MathHelper.distanceBearingPoint(point3d20, MathHelper.getBearing(point3d20, point3d17), num10);
        self.basicArea = PolylineArea();
        point3d1, point3d2 = MathHelper.smethod_91(point3d12, num1, point3d13, num2, turnDirection);
        self.basicArea.method_1(point3d1);
        self.basicArea.method_3(point3d2, MathHelper.smethod_57(turnDirection, point3d2, position, point3d13));
        self.basicArea.method_1(position);
        if (self.rl == None):
            self.basicArea.Add(holdingTemplate4.Spiral[0]);
            self.basicArea.method_3(holdingTemplate4.Spiral[1].Position, holdingTemplate4.Spiral[1].Bulge);
        else:
            point3d1, point3d2 = MathHelper.smethod_91(origin, num3, point3d14, num4, turnDirection);
            self.basicArea.Add(holdingTemplate3.Spiral[0]);
            self.basicArea.method_3(holdingTemplate3.Spiral[1].Position, MathHelper.smethod_57(turnDirection, holdingTemplate3.Spiral[1].Position, point3d1, origin));
            self.basicArea.method_1(point3d1);
            self.basicArea.method_3(point3d2, MathHelper.smethod_57(turnDirection, point3d2, holdingTemplate4.Spiral[2].Position, point3d14));
        self.basicArea.method_3(holdingTemplate4.Spiral[2].Position, MathHelper.smethod_57(turnDirection, holdingTemplate4.Spiral[2].Position, point3d43, point3d15));
        self.basicArea.method_3(point3d43, MathHelper.smethod_57(turnDirection1, point3d43, point3d44, point3d20));
        self.basicArea.method_3(point3d44, MathHelper.smethod_57(turnDirection, point3d44, holdingTemplate6.Spiral[3].Position, point3d17));
        point3d1, point3d2 = MathHelper.smethod_91(point3d18, num8, point3d19, num9, turnDirection);
        point3d3, point3d4 = MathHelper.smethod_91(point3d19, num9, point3d11, num, turnDirection);
        self.basicArea.method_3(holdingTemplate6.Spiral[3].Position, MathHelper.smethod_57(turnDirection, holdingTemplate6.Spiral[3].Position, point3d1, point3d18));
        self.basicArea.method_1(point3d1);
        self.basicArea.method_3(point3d2, MathHelper.smethod_57(turnDirection, point3d2, point3d3, point3d19));
        self.basicArea.method_1(point3d3);
        self.basicArea.method_3(point3d4, MathHelper.smethod_57(turnDirection, point3d4, holdingTemplate1.Spiral[2].Position, point3d11));
        self.basicArea.method_3(holdingTemplate1.Spiral[2].Position, MathHelper.smethod_57(turnDirection, holdingTemplate1.Spiral[2].Position, self.basicArea[0].Position, point3d12));
        self.basicArea.method_1(self.basicArea[0].Position);
        if (holdingVorDme_0.parametersPanel.chbSector1.isChecked()):
            holdingTemplate8 = HoldingTemplate(point3d36, Unit.smethod_1(MathHelper.getBearing(point3d35, point3d36)), value, altitude, speed, value1, metresPerSecond, OrientationType.Right if(orientationType == OrientationType.Left) else OrientationType.Left);
            point3d11, num = MathHelper.smethod_73(holdingTemplate8.Spiral[1].Position, holdingTemplate8.Spiral[2].Position, holdingTemplate8.Spiral[1].Bulge);
            point3d45 = MathHelper.distanceBearingPoint(point3d11, MathHelper.getBearing(position2, position3) + 1.5707963267949 * self.sign, num);
            point3d46 = MathHelper.distanceBearingPoint(point3d45, MathHelper.getBearing(position2, position3), 100);
            point3d46_0 = []
            if (MathHelper.smethod_34(point3d45, point3d46, point3d33, num35, point3d46_0) != IntersectionStatus.Nothing):
                point3d46 = point3d46_0[0]
                point3d = point3d46_0[1]
                point3d47 = MathHelper.distanceBearingPoint(point3d33, MathHelper.getBearing(point3d33, point3d35), num35);
                point3d48 = MathHelper.distanceBearingPoint(point3d46, MathHelper.getBearing(point3d46, point3d47), MathHelper.calcDistance(point3d46, point3d47) / 2);
                point3d48 = MathHelper.distanceBearingPoint(point3d33, MathHelper.getBearing(point3d33, point3d48), num35);
                holdingTemplate9 = HoldingTemplate(point3d46, value2 + 180, value, altitude, speed, value1, metresPerSecond, OrientationType.Right if(orientationType == OrientationType.Left) else OrientationType.Left);
                holdingTemplate10 = HoldingTemplate(point3d48, value2 + 180, value, altitude, speed, value1, metresPerSecond, OrientationType.Right if(orientationType == OrientationType.Left) else OrientationType.Left)
                holdingTemplate11 = HoldingTemplate(point3d47, value2 + 180, value, altitude, speed, value1, metresPerSecond, OrientationType.Right if(orientationType == OrientationType.Left) else OrientationType.Left)
                point3d21, num11 = MathHelper.smethod_73(holdingTemplate9.Spiral[2].Position, holdingTemplate9.Spiral[3].Position, holdingTemplate9.Spiral[2].Bulge);
                point3d22, num12 = MathHelper.smethod_73(holdingTemplate10.Spiral[2].Position, holdingTemplate10.Spiral[3].Position, holdingTemplate10.Spiral[2].Bulge);
                point3d23, num13 = MathHelper.smethod_73(holdingTemplate11.Spiral[2].Position, holdingTemplate11.Spiral[3].Position, holdingTemplate11.Spiral[2].Bulge);
                point3d20, num10 = MathHelper.smethod_193(point3d21, num11, point3d22, num12, point3d23, num13, True);
                point3d43 = MathHelper.distanceBearingPoint(point3d20, MathHelper.getBearing(point3d20, point3d21), num10);
                point3d44 = MathHelper.distanceBearingPoint(point3d20, MathHelper.getBearing(point3d20, point3d23), num10);
                self.sector1 = PolylineArea();
                self.sector1.method_1(holdingTemplate8.Spiral[0].Position);
                self.sector1.method_3(holdingTemplate8.Spiral[1].Position, MathHelper.smethod_57(turnDirection1, holdingTemplate8.Spiral[1].Position, point3d45, point3d11));
                self.sector1.method_7([point3d45, point3d46]);
                self.sector1.method_3(holdingTemplate9.Spiral[1].Position, holdingTemplate9.Spiral[1].Bulge);
                self.sector1.method_3(holdingTemplate9.Spiral[2].Position, MathHelper.smethod_57(turnDirection1, holdingTemplate9.Spiral[2].Position, point3d43, point3d21));
                self.sector1.method_3(point3d43, MathHelper.smethod_57(turnDirection, point3d43, point3d44, point3d20));
                self.sector1.method_3(point3d44, MathHelper.smethod_57(turnDirection1, point3d44, holdingTemplate11.Spiral[3].Position, point3d23));
                self.sector1.Add(holdingTemplate11.Spiral[3]);
                self.sector1.Add(holdingTemplate11.Spiral[4]);
                self.sector1.method_1(point3d36);
        if (holdingVorDme_0.parametersPanel.chbSector2.isChecked() and metresPerSecond <= 1.5):
            flag = False;
            origin3 = Point3D.get_Origin();
            point3d39 = MathHelper.distanceBearingPoint(point3d35, MathHelper.getBearing(point3d34, point3d33) - Unit.ConvertDegToRad(35) * self.sign, 1000);
            point3d24_0 = []
            if (MathHelper.smethod_34(point3d35, point3d39, point3d33, num35, point3d24_0) != IntersectionStatus.Nothing):
                point3d24 = point3d24_0[0]
                point3d = point3d24_0[1]
                point3d25 = MathHelper.getIntersectionPoint(point3d35, point3d39, point3d33, origin2);
                if (self.rl != None and MathHelper.calcDistance(point3d35, point3d24) > MathHelper.calcDistance(point3d35, point3d25)):
                    origin3 = point3d24;
                    point3d24 = MathHelper.distanceBearingPoint(point3d33, MathHelper.getBearing(point3d33, origin2), num35);
                    flag = True;
            else:
                origin3 = MathHelper.getIntersectionPoint(point3d35, point3d39, point3d33, origin2);
                point3d24 = MathHelper.distanceBearingPoint(point3d33, MathHelper.getBearing(point3d33, origin2), num35);
                flag = True;
            point3d39 = MathHelper.distanceBearingPoint(point3d38, MathHelper.getBearing(point3d34, point3d33) - Unit.ConvertDegToRad(25) * self.sign, 1000);
            point3d26_0 = []
            MathHelper.smethod_34(point3d38, point3d39, point3d33, num35, point3d26_0)
            point3d26 = point3d26_0[0]
            point3d = point3d26_0[1]
            point3d49 = MathHelper.distanceBearingPoint(point3d24, MathHelper.getBearing(point3d24, point3d26), MathHelper.calcDistance(point3d24, point3d26) / 2);
            point3d49 = MathHelper.distanceBearingPoint(point3d33, MathHelper.getBearing(point3d33, point3d49), num35);
            holdingTemplate12 = HoldingTemplate(point3d24, value2 + 180 - 30 * self.sign, value, altitude, speed, value1, metresPerSecond, orientationType);
            holdingTemplate13 = HoldingTemplate(point3d49, value2 + 180 - 30 * self.sign, value, altitude, speed, value1, metresPerSecond, orientationType);
            holdingTemplate14 = HoldingTemplate(point3d26, value2 + 180 - 30 * self.sign, value, altitude, speed, value1, metresPerSecond, orientationType);
            point3d27, num14 = MathHelper.smethod_73(holdingTemplate12.Spiral[2].Position, holdingTemplate12.Spiral[3].Position, holdingTemplate12.Spiral[2].Bulge);
            point3d28, num15 = MathHelper.smethod_73(holdingTemplate13.Spiral[2].Position, holdingTemplate13.Spiral[3].Position, holdingTemplate13.Spiral[2].Bulge);
            point3d29, num16 = MathHelper.smethod_73(holdingTemplate14.Spiral[2].Position, holdingTemplate14.Spiral[3].Position, holdingTemplate14.Spiral[2].Bulge);
            point3d20, num10 = MathHelper.smethod_193(point3d27, num14, point3d28, num15, point3d29, num16, True);
            point3d43 = MathHelper.distanceBearingPoint(point3d20, MathHelper.getBearing(point3d20, point3d27), num10);
            point3d44 = MathHelper.distanceBearingPoint(point3d20, MathHelper.getBearing(point3d20, point3d29), num10);
            self.sector2 = PolylineArea();
            if (not flag):
                self.sector2.Add(holdingTemplate12.Spiral[0]);
                self.sector2.Add(holdingTemplate12.Spiral[1]);
                self.sector2.method_3(holdingTemplate12.Spiral[2].Position, MathHelper.smethod_57(turnDirection, holdingTemplate12.Spiral[2].Position, point3d43, point3d27));
            else:
                holdingTemplate15 = HoldingTemplate(origin3, value2 + 180 - 30 * self.sign, value, altitude, speed, value1, metresPerSecond, orientationType);
                point3d30, num17 = MathHelper.smethod_73(holdingTemplate15.Spiral[1].Position, holdingTemplate15.Spiral[2].Position, holdingTemplate15.Spiral[1].Bulge);
                point3d31, num18 = MathHelper.smethod_73(holdingTemplate15.Spiral[2].Position, holdingTemplate15.Spiral[3].Position, holdingTemplate15.Spiral[2].Bulge);
                point3d32, num19 = MathHelper.smethod_73(holdingTemplate12.Spiral[1].Position, holdingTemplate12.Spiral[2].Position, holdingTemplate12.Spiral[1].Bulge);
                point3d1, point3d2 = MathHelper.smethod_91(point3d30, num17, point3d32, num19, turnDirection);
                self.sector2.Add(holdingTemplate15.Spiral[0]);
                self.sector2.method_3(holdingTemplate15.Spiral[1].Position, MathHelper.smethod_57(turnDirection, holdingTemplate15.Spiral[1].Position, point3d1, point3d30));
                self.sector2.method_1(point3d1);
                self.sector2.method_3(point3d2, MathHelper.smethod_57(turnDirection, point3d2, holdingTemplate12.Spiral[2].Position, point3d32));
                self.sector2.method_3(holdingTemplate12.Spiral[2].Position, MathHelper.smethod_57(turnDirection, holdingTemplate12.Spiral[2].Position, point3d43, point3d27));
            self.sector2.method_3(point3d43, MathHelper.smethod_57(turnDirection1, point3d43, point3d44, point3d20));
            self.sector2.method_3(point3d44, MathHelper.smethod_57(turnDirection, point3d44, holdingTemplate14.Spiral[3].Position, point3d29));
            self.sector2.Add(holdingTemplate14.Spiral[3]);
            self.sector2.Add(holdingTemplate14.Spiral[4]);
            self.sector2.Add(self.sector2[0]);
        if (holdingVorDme_0.parametersPanel.chbReciprocalEntry.isChecked()):
            num41 = MathHelper.getBearing(point3d33, point3d34);
            num42 = MathHelper.getBearing(point3d33, point3d41);
            num43 = MathHelper.smethod_53(num41, num42) if(orientationType == OrientationType.Right) else MathHelper.smethod_53(num42, num41)
            num43 = round(Unit.smethod_1(num43), 0);
            num43 = Unit.ConvertDegToRad(num43);
            self.re = MathHelper.smethod_4(num41 + num43 if(orientationType == OrientationType.Right) else num41 - num43);
        self.valid = True;

        if holdingVorDme_0.parametersPanel.cmbOrientation.currentIndex() == 0:
            self.nominal[0].bulge = -1
            self.nominal[2].bulge = -1
        else:
            self.nominal[0].bulge = 1
            self.nominal[2].bulge = 1
class VorDmeHoldingTowards(VordDmeHoldingBase):
    def __init__(self, holdingVorDme_0):
        self.nominal = None
        self.tolerance = None
        self.basicArea = None
        self.sector1 = None
        self.sector2 = None
        self.sector3 = None
        self.re = None
        self.rl = None
        self.sign = None
        self.valid = None
        point3d28 = holdingVorDme_0.parametersPanel.pnlVorDme.Point3d;
        value = Speed(float(holdingVorDme_0.parametersPanel.txtIas.text()))
        altitude = Altitude(float(holdingVorDme_0.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)
        speed = Speed(float(holdingVorDme_0.parametersPanel.pnlWind.speedBox.text()))
        value1 = float(holdingVorDme_0.parametersPanel.txtIsa.text())
        distance = Distance(float(holdingVorDme_0.parametersPanel.txtHoldingDme.text()), DistanceUnits.NM)
        distance1 = Distance(float(holdingVorDme_0.parametersPanel.txtLimitingDme.text()), DistanceUnits.NM)
        orientationType = holdingVorDme_0.parametersPanel.cmbOrientation.currentText()
        value2 = float(holdingVorDme_0.parametersPanel.txtTrack.Value)
        speed1 = Speed.smethod_0(value, value1, altitude);
        num18 = Unit.ConvertDegToRad(value2);
        num19 = Unit.ConvertDegToRad(value2 + 180);
        self.sign = 1 if(orientationType == OrientationType.Right) else -1
        turnDirection = TurnDirection.Right if(orientationType == OrientationType.Right) else TurnDirection.Left
        turnDirection1 = TurnDirection.Left if(orientationType == OrientationType.Right) else TurnDirection.Right
        num20 = min([943.27 / speed1.KilometresPerHour, 3]);
        num21 = Unit.ConvertKMToMeters(speed1.KilometresPerHour / (62.8318530717959 * num20));
        metres = altitude.Metres - point3d28.get_Z();
        num22 = math.tan(Unit.ConvertDegToRad(55)) * metres;
        metres1 = distance.Metres;
        num23 = math.sqrt(metres1 * metres1 - metres * metres);
        if (num22 >= num23):
            distance = Distance(MathHelper.smethod_0(Unit.ConvertMeterToNM(math.sqrt(num22 * num22 + metres * metres)), 0), DistanceUnits.NM);
            QMessageBox.warning(holdingVorDme_0, "Warning" ,Messages.HOLDING_DME_DISTANCE_WITHIN_OVERHEAD_TOLERANCE + str(distance.NauticalMiles) + "nm.")
            holdingVorDme_0.parametersPanel.txtHoldingDme.setText(str(distance.NauticalMiles))
        metres1 = distance.Metres;
        num23 = math.sqrt(metres1 * metres1 - metres * metres);
        num24 = speed1.MetresPerSecond * 60 if(altitude.Feet <= 14000) else speed1.MetresPerSecond * 90
        metres2 = math.sqrt((num23 + num24) * (num23 + num24) + 4 * num21 * num21 + metres * metres);
        num25 = math.sqrt(metres2 * metres2 - metres * metres);
        if (holdingVorDme_0.method_33(Distance(num25), True).Metres > distance1.Metres):
            distance1 = holdingVorDme_0.method_33(Distance(num25), True);
            QMessageBox.warning(holdingVorDme_0, "Warning", Messages.LIMITING_DME_DISTANCE_TOO_CLOSE + str(distance1.NauticalMiles) + "nm.")
            holdingVorDme_0.parametersPanel.txtLimitingDme.setText(str(distance1.NauticalMiles))
        metres2 = distance1.Metres;
        num25 = math.sqrt(metres2 * metres2 - metres * metres);
        num24 = math.sqrt(metres2 * metres2 - 4 * num21 * num21 - metres * metres) - num23;
        metresPerSecond = num24 / speed1.MetresPerSecond / 60;
        num26 = Unit.ConvertDegToRad(5.2) * self.sign;
        metres3 = Distance.smethod_2(distance).Metres;
        metres4 = Distance.smethod_2(distance1).Metres;
        num27 = num23 - metres3;
        num28 = num23 + metres3;
        num29 = num25 - metres4;
        num30 = num25 + metres4;
        point3d29 = MathHelper.distanceBearingPoint(point3d28, num19, num23);
        point3d30 = MathHelper.distanceBearingPoint(point3d28, num19 - num26, num27);
        point3d31 = MathHelper.distanceBearingPoint(point3d28, num19 + num26, num27);
        point3d32 = MathHelper.distanceBearingPoint(point3d28, num19 - num26, num28);
        point3d33 = MathHelper.distanceBearingPoint(point3d28, num19 + num26, num28);
        holdingTemplate = HoldingTemplate(point3d30, value2, value, altitude, speed, value1, metresPerSecond, orientationType);
        holdingTemplate1 = HoldingTemplate(point3d31, value2, value, altitude, speed, value1, metresPerSecond, orientationType);
        position = holdingTemplate.OutboundLineTop[0].Position;
        position1 = holdingTemplate.OutboundLineTop[1].Position;
        position2 = holdingTemplate1.OutboundLineBottom[0].Position;
        position3 = holdingTemplate1.OutboundLineBottom[1].Position;
        point3d0_5 = []
        MathHelper.smethod_34(position, position1, point3d28, num30, point3d0_5);
        point3d = point3d0_5[0]
        point3d5 = point3d0_5[1]
        point3d0_6 = []
        MathHelper.smethod_34(position2, position3, point3d28, num29, point3d0_6);
        point3d = point3d0_6[0]
        point3d6 = point3d0_6[1]
        point3d0_7 = []
        MathHelper.smethod_34(position2, position3, point3d28, num30, point3d0_7);
        point3d = point3d0_7[0]
        point3d7 = point3d0_7[1]
        if (orientationType != OrientationType.Right):
            if (MathHelper.smethod_115(point3d6, point3d31, point3d33)):
                point3d0_6 = []
                MathHelper.smethod_34(point3d31, point3d33, point3d28, num29, point3d0_6);
                point3d = point3d0_6[0]
                point3d6 = point3d0_6[1]
            if (MathHelper.smethod_115(point3d7, point3d31, point3d33)):
                point3d0_7 = []
                MathHelper.smethod_34(point3d31, point3d33, point3d28, num30, point3d0_7);
                point3d = point3d0_7[0]
                point3d7 = point3d0_7[1]
        else:
            if (MathHelper.smethod_119(point3d6, point3d31, point3d33)):
                point3d0_6 = []
                MathHelper.smethod_34(point3d31, point3d33, point3d28, num29, point3d0_6);
                point3d = point3d0_6[0]
                point3d6 = point3d0_6[1]
            if (MathHelper.smethod_119(point3d7, point3d31, point3d33)):
                point3d0_7 = []
                MathHelper.smethod_34(point3d31, point3d33, point3d28, num30, point3d0_7);
                point3d = point3d0_7[0]
                point3d7 = point3d0_7[1]
        point3d34 = MathHelper.distanceBearingPoint(point3d5, MathHelper.getBearing(point3d5, point3d7), MathHelper.calcDistance(point3d5, point3d7) / 2);
        point3d34 = MathHelper.distanceBearingPoint(point3d28, MathHelper.getBearing(point3d28, point3d34), num30);
        holdingTemplate2 = HoldingTemplate(point3d5, value2 + 180, value, altitude, speed, value1, metresPerSecond, orientationType);
        holdingTemplate3 = HoldingTemplate(point3d34, value2 + 180, value, altitude, speed, value1, metresPerSecond, orientationType);
        holdingTemplate4 = HoldingTemplate(point3d7, value2 + 180, value, altitude, speed, value1, metresPerSecond, orientationType);
        holdingTemplate5 = HoldingTemplate(point3d6, value2 + 180, value, altitude, speed, value1, metresPerSecond, orientationType);
        point3d8, num = MathHelper.smethod_73(holdingTemplate1.Spiral[1].Position, holdingTemplate1.Spiral[2].Position, holdingTemplate1.Spiral[1].Bulge);
        point3d9, num1 = MathHelper.smethod_73(holdingTemplate1.Spiral[2].Position, holdingTemplate1.Spiral[3].Position, holdingTemplate1.Spiral[2].Bulge);
        point3d10, num2 = MathHelper.smethod_73(holdingTemplate.Spiral[2].Position, holdingTemplate.Spiral[3].Position, holdingTemplate.Spiral[2].Bulge);
        point3d11, num3 = MathHelper.smethod_73(holdingTemplate2.Spiral[1].Position, holdingTemplate2.Spiral[2].Position, holdingTemplate2.Spiral[1].Bulge);
        point3d12, num4 = MathHelper.smethod_73(holdingTemplate3.Spiral[2].Position, holdingTemplate3.Spiral[3].Position, holdingTemplate3.Spiral[2].Bulge);
        point3d13, num5 = MathHelper.smethod_73(holdingTemplate4.Spiral[2].Position, holdingTemplate4.Spiral[3].Position, holdingTemplate4.Spiral[2].Bulge);
        point3d14, num6 = MathHelper.smethod_73(holdingTemplate4.Spiral[3].Position, holdingTemplate4.Spiral[4].Position, holdingTemplate4.Spiral[3].Bulge);
        point3d15, num7 = MathHelper.smethod_73(holdingTemplate5.Spiral[3].Position, holdingTemplate5.Spiral[4].Position, holdingTemplate5.Spiral[3].Bulge);
        point3d16, num8 = MathHelper.smethod_193(point3d11, num3, point3d12, num4, point3d13, num5, False);
        point3d35 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d11), num8);
        point3d36 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d13), num8);
        self.nominal = PolylineArea();
        point3d37 = point3d29;
        point3d38 = MathHelper.distanceBearingPoint(point3d37, num19 - 1.5707963267949 * self.sign, 2 * num21);
        self.nominal.method_3(point3d37, MathHelper.smethod_59(num18, point3d37, point3d38));
        self.nominal.method_1(point3d38);
        point3d37 = MathHelper.distanceBearingPoint(point3d38, num19, num24);
        point3d38 = MathHelper.distanceBearingPoint(point3d37, num18 - 1.5707963267949 * self.sign, 2 * num21);
        self.nominal.method_3(point3d37, MathHelper.smethod_59(num19, point3d37, point3d38));
        self.nominal.method_1(point3d38);
        point3d39 = point3d37;
        self.tolerance = PolylineArea();
        point3d37 = MathHelper.distanceBearingPoint(point3d28, num19, num27);
        point3d38 = MathHelper.distanceBearingPoint(point3d28, num19, num28);
        self.tolerance.method_1(point3d30);
        self.tolerance.method_3(point3d32, MathHelper.smethod_60(point3d32, point3d38, point3d33));
        self.tolerance.method_1(point3d33);
        self.tolerance.method_3(point3d31, MathHelper.smethod_60(point3d31, point3d37, point3d30));
        self.tolerance.method_1(point3d30);
        self.basicArea = PolylineArea();
        point3d1, point3d2 = MathHelper.smethod_91(point3d9, num1, point3d10, num2, turnDirection);
        self.basicArea.method_1(point3d1);
        self.basicArea.method_3(point3d2, MathHelper.smethod_57(turnDirection, point3d2, position, point3d10));
        self.basicArea.method_1(position);
        self.basicArea.Add(holdingTemplate2.Spiral[0]);
        self.basicArea.method_3(holdingTemplate2.Spiral[1].Position, MathHelper.smethod_57(turnDirection, holdingTemplate2.Spiral[1].Position, point3d35, point3d11));
        self.basicArea.method_3(point3d35, MathHelper.smethod_57(turnDirection, point3d35, point3d36, point3d16));
        self.basicArea.method_3(point3d36, MathHelper.smethod_57(turnDirection, point3d36, holdingTemplate4.Spiral[3].Position, point3d13));
        point3d1, point3d2 = MathHelper.smethod_91(point3d14, num6, point3d15, num7, turnDirection);
        point3d3, point3d4 = MathHelper.smethod_91(point3d15, num7, point3d8, num, turnDirection);
        self.basicArea.method_3(holdingTemplate4.Spiral[3].Position, MathHelper.smethod_57(turnDirection, holdingTemplate4.Spiral[3].Position, point3d1, point3d14));
        self.basicArea.method_1(point3d1);
        self.basicArea.method_3(point3d2, MathHelper.smethod_57(turnDirection, point3d2, point3d3, point3d15));
        self.basicArea.method_1(point3d3);
        self.basicArea.method_3(point3d4, MathHelper.smethod_57(turnDirection, point3d4, holdingTemplate1.Spiral[2].Position, point3d8));
        self.basicArea.method_3(holdingTemplate1.Spiral[2].Position, MathHelper.smethod_57(turnDirection, holdingTemplate1.Spiral[2].Position, self.basicArea[0].Position, point3d9));
        self.basicArea.method_1(self.basicArea[0].Position);
        if (holdingVorDme_0.parametersPanel.chbSector1.isChecked()):
            holdingTemplate6 = HoldingTemplate(point3d31, Unit.smethod_1(MathHelper.getBearing(point3d30, point3d31)), value, altitude, speed, value1, metresPerSecond, OrientationType.Right if(orientationType == OrientationType.Left) else OrientationType.Left);
            point3d8, num = MathHelper.smethod_73(holdingTemplate6.Spiral[1].Position, holdingTemplate6.Spiral[2].Position, holdingTemplate6.Spiral[1].Bulge);
            point3d40 = MathHelper.distanceBearingPoint(point3d8, MathHelper.getBearing(position2, position3) + 1.5707963267949 * self.sign, num);
            point3d41 = MathHelper.distanceBearingPoint(point3d40, MathHelper.getBearing(position2, position3), 100);
            point3d0_41 = []
            MathHelper.smethod_34(point3d40, point3d41, point3d28, num30, point3d0_41)
            point3d = point3d0_41[0]
            point3d41 = point3d0_41[1]
            point3d42 = MathHelper.distanceBearingPoint(point3d28, MathHelper.getBearing(point3d28, point3d30), num30);
            point3d43 = MathHelper.distanceBearingPoint(point3d41, MathHelper.getBearing(point3d41, point3d42), MathHelper.calcDistance(point3d41, point3d42) / 2);
            point3d43 = MathHelper.distanceBearingPoint(point3d28, MathHelper.getBearing(point3d28, point3d43), num30);
            holdingTemplate7 = HoldingTemplate(point3d41, value2 + 180, value, altitude, speed, value1, metresPerSecond, OrientationType.Right if(orientationType == OrientationType.Left) else OrientationType.Left);
            holdingTemplate8 = HoldingTemplate(point3d43, value2 + 180, value, altitude, speed, value1, metresPerSecond, OrientationType.Right if(orientationType == OrientationType.Left) else OrientationType.Left);
            holdingTemplate9 = HoldingTemplate(point3d42, value2 + 180, value, altitude, speed, value1, metresPerSecond, OrientationType.Right if(orientationType == OrientationType.Left) else OrientationType.Left);
            point3d17, num9 = MathHelper.smethod_73(holdingTemplate7.Spiral[1].Position, holdingTemplate7.Spiral[2].Position, holdingTemplate7.Spiral[1].Bulge);
            point3d18, num10 = MathHelper.smethod_73(holdingTemplate8.Spiral[2].Position, holdingTemplate8.Spiral[3].Position, holdingTemplate8.Spiral[2].Bulge);
            point3d19, num11 = MathHelper.smethod_73(holdingTemplate9.Spiral[2].Position, holdingTemplate9.Spiral[3].Position, holdingTemplate9.Spiral[2].Bulge);
            point3d16, num8 = MathHelper.smethod_193(point3d17, num9, point3d18, num10, point3d19, num11, False);
            point3d35 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d17), num8);
            point3d36 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d19), num8);
            self.sector1 = PolylineArea();
            self.sector1.method_1(holdingTemplate6.Spiral[0].Position);
            self.sector1.method_3(holdingTemplate6.Spiral[1].Position, MathHelper.smethod_57(turnDirection1, holdingTemplate6.Spiral[1].Position, point3d40, point3d8));
            self.sector1.method_7([point3d40, point3d41]);
            self.sector1.method_3(holdingTemplate7.Spiral[1].Position, MathHelper.smethod_57(turnDirection1, holdingTemplate7.Spiral[1].Position, point3d35, point3d17));
            self.sector1.method_3(point3d35, MathHelper.smethod_57(turnDirection1, point3d35, point3d36, point3d16));
            self.sector1.method_3(point3d36, MathHelper.smethod_57(turnDirection1, point3d36, holdingTemplate9.Spiral[3].Position, point3d19));
            self.sector1.Add(holdingTemplate9.Spiral[3]);
            self.sector1.Add(holdingTemplate9.Spiral[4]);
            self.sector1.method_1(point3d31);
        if (holdingVorDme_0.parametersPanel.chbSector2.isChecked()):
            point3d37 = MathHelper.distanceBearingPoint(point3d30, MathHelper.getBearing(point3d28, point3d29) - Unit.ConvertDegToRad(35) * self.sign, 1000);
            point3d0_20 = []
            MathHelper.smethod_34(point3d30, point3d37, point3d28, num30, point3d0_20)
            point3d = point3d0_20[0]
            point3d20 = point3d0_20[1]
            point3d37 = MathHelper.distanceBearingPoint(point3d33, MathHelper.getBearing(point3d28, point3d29) - Unit.ConvertDegToRad(25) * self.sign, 1000);
            point3d0_21 = []
            MathHelper.smethod_34(point3d33, point3d37, point3d28, num30, point3d0_21)
            point3d = point3d0_21[0]
            point3d21 = point3d0_21[1]
            point3d44 = MathHelper.distanceBearingPoint(point3d20, MathHelper.getBearing(point3d20, point3d21), MathHelper.calcDistance(point3d20, point3d21) / 2);
            point3d44 = MathHelper.distanceBearingPoint(point3d28, MathHelper.getBearing(point3d28, point3d44), num30);
            holdingTemplate10 = HoldingTemplate(point3d20, value2 + 180 - 30 * self.sign, value, altitude, speed, value1, metresPerSecond, orientationType);
            holdingTemplate11 = HoldingTemplate(point3d44, value2 + 180 - 30 * self.sign, value, altitude, speed, value1, metresPerSecond, orientationType);
            holdingTemplate12 = HoldingTemplate(point3d21, value2 + 180 - 30 * self.sign, value, altitude, speed, value1, metresPerSecond, orientationType);
            point3d22, num12 = MathHelper.smethod_73(holdingTemplate10.Spiral[2].Position, holdingTemplate10.Spiral[3].Position, holdingTemplate10.Spiral[2].Bulge);
            point3d23, num13 = MathHelper.smethod_73(holdingTemplate11.Spiral[2].Position, holdingTemplate11.Spiral[3].Position, holdingTemplate11.Spiral[2].Bulge);
            point3d24, num14 = MathHelper.smethod_73(holdingTemplate12.Spiral[2].Position, holdingTemplate12.Spiral[3].Position, holdingTemplate12.Spiral[2].Bulge);
            point3d16, num8 = MathHelper.smethod_193(point3d22, num12, point3d23, num13, point3d24, num14, False);
            point3d35 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d22), num8);
            point3d36 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d24), num8);
            self.sector2 = PolylineArea()
            self.sector2.Add(holdingTemplate10.Spiral[0])
            self.sector2.Add(holdingTemplate10.Spiral[1])
            self.sector2.method_3(holdingTemplate10.Spiral[2].Position, MathHelper.smethod_57(turnDirection, holdingTemplate10.Spiral[2].Position, point3d35, point3d22));
            self.sector2.method_3(point3d35, MathHelper.smethod_57(turnDirection, point3d35, point3d36, point3d16));
            self.sector2.method_3(point3d36, MathHelper.smethod_57(turnDirection, point3d36, holdingTemplate12.Spiral[3].Position, point3d24));
            self.sector2.Add(holdingTemplate12.Spiral[3]);
            self.sector2.Add(holdingTemplate12.Spiral[4]);
            self.sector2.Add(holdingTemplate10.Spiral[0]);
        if (holdingVorDme_0.parametersPanel.chbReciprocalEntry.isChecked()):
            num31 = MathHelper.getBearing(point3d28, point3d29);
            num32 = MathHelper.getBearing(point3d28, point3d39);
            num33 = MathHelper.smethod_53(num32, num31) if(orientationType == OrientationType.Right) else MathHelper.smethod_53(num31, num32)
            num33 = round(Unit.smethod_1(num33), 0);
            num33 = Unit.ConvertDegToRad(num33);
            self.re = MathHelper.smethod_4(num31 - num33 if(orientationType == OrientationType.Right) else num31 + num33);
            point3d45 = MathHelper.distanceBearingPoint(point3d28, self.re - num26, num30);
            point3d46 = MathHelper.distanceBearingPoint(point3d28, self.re + num26, num30);
            point3d47 = MathHelper.distanceBearingPoint(point3d28, self.re, num30);
            holdingTemplate13 = HoldingTemplate(point3d45, Unit.smethod_1(self.re), value, altitude, speed, value1, metresPerSecond, orientationType);
            holdingTemplate14 = HoldingTemplate(point3d47, Unit.smethod_1(self.re), value, altitude, speed, value1, metresPerSecond, orientationType);
            holdingTemplate15 = HoldingTemplate(point3d46, Unit.smethod_1(self.re), value, altitude, speed, value1, metresPerSecond, orientationType);
            point3d25, num15 = MathHelper.smethod_73(holdingTemplate13.Spiral[2].Position, holdingTemplate13.Spiral[3].Position, holdingTemplate13.Spiral[2].Bulge);
            point3d26, num16 = MathHelper.smethod_73(holdingTemplate14.Spiral[2].Position, holdingTemplate14.Spiral[3].Position, holdingTemplate14.Spiral[2].Bulge);
            point3d27, num17 = MathHelper.smethod_73(holdingTemplate15.Spiral[2].Position, holdingTemplate15.Spiral[3].Position, holdingTemplate15.Spiral[2].Bulge);
            point3d16, num8 = MathHelper.smethod_193(point3d25, num15, point3d26, num16, point3d27, num17, False);
            point3d35 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d25), num8);
            point3d36 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d27), num8);
            self.sector3 = PolylineArea()
            self.sector3.Add(holdingTemplate13.Spiral[0])
            self.sector3.Add(holdingTemplate13.Spiral[1])
            self.sector3.method_3(holdingTemplate13.Spiral[2].Position, MathHelper.smethod_57(turnDirection, holdingTemplate13.Spiral[2].Position, point3d35, point3d25));
            self.sector3.method_3(point3d35, MathHelper.smethod_57(turnDirection, point3d35, point3d36, point3d16));
            self.sector3.method_3(point3d36, MathHelper.smethod_57(turnDirection, point3d36, holdingTemplate15.Spiral[3].Position, point3d27));
            self.sector3.Add(holdingTemplate15.Spiral[3]);
            self.sector3.Add(holdingTemplate15.Spiral[4]);
            self.sector3.Add(holdingTemplate13.Spiral[0]);
        self.valid = True;
        if holdingVorDme_0.parametersPanel.cmbOrientation.currentIndex() == 0:
            self.nominal[0].bulge = -1
            self.nominal[2].bulge = -1
        else:
            self.nominal[0].bulge = 1
            self.nominal[2].bulge = 1
class VorDmeHoldingType:
    Towards = "Towards"
    Away = "Away"
