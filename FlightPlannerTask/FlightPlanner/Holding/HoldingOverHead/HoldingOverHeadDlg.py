# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt, QString
from PyQt4.QtGui import QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, \
     QgsVectorFileWriter, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2,\
     QgsFeature

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes, DistanceUnits,AircraftSpeedCategory, OrientationType, AltitudeUnits, ObstacleAreaResult
from FlightPlanner.Holding.HoldingOverHead.ui_HoldingOverHead import Ui_HoldingOverHead
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.AcadHelper import AcadHelper
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
import define

class HoldingOverHeadDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("HoldingOverHeadDlg")
        self.surfaceType = SurfaceTypes.HoldingOverHead
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.HoldingOverHead)
        self.resize(540, 550)
        QgisHelper.matchingDialogSize(self, 630, 610)
        self.surfaceList = None
        self.resultLayerList = dict()
        
        self.vorDmeFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.initBasedOnCmb()
    def initBasedOnCmb(self):

        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.vorDmeFeatureArray = self.basedOnCmbFill(self.currentLayer, self.parametersPanel.cmbBasedOn, self.parametersPanel.pnlNavAid)
    def basedOnCmbFill(self, layer, basedOnCmbObj, vorDmePositionPanelObj):
        basedOnCmbObj.Clear()
        vorDmePositionPanelObj.Point3d = None
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
                if self.parametersPanel.cmbNavAidType.SelectedIndex == 0:
                    if attrValue == "VOR" or attrValue == "VORDME" or attrValue == "VORTAC" or attrValue == "TACAN":
                        vorDmeList.append(attrValue)
                        vorDmeFeatureList.append(feat)
                else:
                    if attrValue == "NDB" or attrValue == "NDBDME":
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
        if len(self.vorDmeFeatureArray) == 0:
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

        self.parametersPanel.pnlNavAid.Point3d = Point3D(long, lat, alt)
    
    def initObstaclesModel(self):
        self.obstaclesModel.MocMultiplier = self.parametersPanel.mocSpinBox.Value
        return FlightPlanBaseDlg.initObstaclesModel(self)
    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return  

        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.HoldingOverHead, self.ui.tblObstacles, None, parameterList, resultHideColumnNames)

    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append((self.surfaceType, "group"))
        parameterList.append(("Type", self.parametersPanel.cmbNavAidType.SelectedItem))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAid.txtPointX.text()), float(self.parametersPanel.pnlNavAid.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlNavAid.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlNavAid.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlNavAid.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlNavAid.txtPointY.text()))
        parameterList.append(("Altitude", self.parametersPanel.pnlNavAid.txtAltitudeFt.text() + "ft"))
        parameterList.append(("", self.parametersPanel.pnlNavAid.txtAltitudeM.text() + "m"))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Used For", self.parametersPanel.cmbUsedFor.SelectedItem))

        parameterList.append(("IAS", str(self.parametersPanel.txtIas.Value.Knots) + "kts"))
        parameterList.append(("TAS", str(self.parametersPanel.txtTas.Value.Knots) + "kts"))
        parameterList.append(("Altitude", str(self.parametersPanel.txtAltitude.Value.Metres) + "m"))
        parameterList.append(("", str(self.parametersPanel.txtAltitude.Value.Feet) + "ft"))
        parameterList.append(("ISA", QString(str(self.parametersPanel.txtIsa.Value)) + unicode("°C", "utf-8")))
        
        parameterList.append(("Wind", self.parametersPanel.pnlWind.speedBox.text() + "kts"))
        parameterList.append(("MOC", str(self.parametersPanel.txtMoc.Value.Metres) + "m"))
        parameterList.append(("", str(self.parametersPanel.txtMoc.Value.Feet) + "ft"))
        parameterList.append(("Time", str(self.parametersPanel.txtTime.Value)))
        if self.parametersPanel.chbCatH.Visible:
            if self.parametersPanel.chbCatH.Checked:
                parameterList.append(("Cat.H(linear MOC reduction up to 2NM", "Checked"))
            else:
                parameterList.append(("Cat.H(linear MOC reduction up to 2NM", "Unchecked"))        
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstruction.SelectedItem))
        parameterList.append(("MOCmultipiler", str(self.parametersPanel.mocSpinBox.Value)))
        
        parameterList.append(("Entry Areas", "group"))       
        if self.parametersPanel.chbIntercept.Checked:
            parameterList.append(("70 Intercept", "Checked"))
        else:
            parameterList.append(("70 Intercept", "Unchecked")) 
        
        if self.parametersPanel.chbSectors12.Checked:
            parameterList.append(("Sector 1_2", "Checked"))
        else:
            parameterList.append(("Sector 1_2", "Unchecked")) 
        
        parameterList.append(("In-bound Track", QString("Plan : ") + QString(self.parametersPanel.txtTrack.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", QString("Geodetic : ") + QString(self.parametersPanel.txtTrack.txtRadialGeodetic.Value) + define._degreeStr))

        parameterList.append(("Turns", self.parametersPanel.cmbOrientation.SelectedItem))
        
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
        pdtResultStr = MathHelper.pdtCheckResultToString(float(self.parametersPanel.txtIsa.Value), self.parametersPanel.txtAltitude.Value, float(self.parametersPanel.txtIas.Value.Knots), float(self.parametersPanel.txtTime.Value))
        QMessageBox.warning(self, "PDT Check", pdtResultStr)

    def btnEvaluate_Click(self):
        if not self.method_27():
            return
        holdingTemplate = HoldingTemplate(self.parametersPanel.pnlNavAid.Point3d, float(self.parametersPanel.txtTrack.Value), self.parametersPanel.txtIas.Value, self.parametersPanel.txtAltitude.Value, Speed(float(self.parametersPanel.pnlWind.speedBox.text())), float(self.parametersPanel.txtIsa.Value), float(self.parametersPanel.txtTime.Value), self.parametersPanel.cmbOrientation.SelectedItem);
        polylineArea = self.method_35();
        polylineAreaTemp = holdingTemplate.vmethod_0(polylineArea, self.parametersPanel.chbIntercept.Checked, self.parametersPanel.chbSectors12.Checked);
        polylineArea1 = polylineAreaTemp[0]
        altitude_0 = self.parametersPanel.txtAltitude.Value
        altitude_1 = self.parametersPanel.txtMoc.Value
        if (self.parametersPanel.cmbUsedFor.SelectedIndex != 0):
            hOSE = HoldingOverheadSecondaryEvaluator(polylineArea1, altitude_0, altitude_1, Distance(2.5, DistanceUnits.NM));
            self.obstaclesModel = HoldingOverHeadObstacles(False, "second", None, altitude_0, hOSE.inner, hOSE.outer, hOSE.poly, altitude_1, Distance(2.5, DistanceUnits.NM)) 
#             selectionArea = (holdingOverheadSecondaryEvaluator as HoldingOverhead.HoldingOverheadSecondaryEvaluator).SelectionArea;
        elif (not self.parametersPanel.chbCatH.isChecked()):
            hOBE = HoldingOverheadBufferEvaluator(polylineArea1, altitude_0, altitude_1);
            self.obstaclesModel = HoldingOverHeadObstacles(self.parametersPanel.chbCatH.Checked, "buffer", hOBE.areas, altitude_0)
#             selectionArea = (holdingOverheadSecondaryEvaluator as HoldingOverhead.HoldingOverheadBufferEvaluator).SelectionArea;
        else:
            hOSE = HoldingOverheadSecondaryEvaluator(polylineArea1, altitude_0, altitude_1, Distance(2, DistanceUnits.NM))
            self.obstaclesModel = HoldingOverHeadObstacles(True, "second", None, altitude_0, hOSE.inner, hOSE.outer, hOSE.poly, altitude_1, Distance(2, DistanceUnits.NM)) 
#             selectionArea = (holdingOverheadSecondaryEvaluator as HoldingOverhead.HoldingOverheadSecondaryEvaluator).SelectionArea;
        return FlightPlanBaseDlg.btnEvaluate_Click(self)

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        if not self.method_27():
            return
        holdingTemplate = HoldingTemplate(self.parametersPanel.pnlNavAid.Point3d, float(self.parametersPanel.txtTrack.Value), self.parametersPanel.txtIas.Value, self.parametersPanel.txtAltitude.Value, Speed(float(self.parametersPanel.pnlWind.speedBox.text())), float(self.parametersPanel.txtIsa.Value), float(self.parametersPanel.txtTime.Value), self.parametersPanel.cmbOrientation.SelectedItem);
        polylineArea2 = self.method_35();
        polylineAreaTemp = holdingTemplate.vmethod_0(polylineArea2, self.parametersPanel.chbIntercept.Checked, self.parametersPanel.chbSectors12.Checked);
        polylineArea3 = polylineAreaTemp[0]
        
        polyline = PolylineArea.smethod_131(holdingTemplate.Nominal)
        resultPolylineAreaList = []
        
        if (self.parametersPanel.cmbConstruction.SelectedIndex == 0):
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType)
            resultPolylineAreaList.append(polylineArea3)
            resultPolylineAreaList.append(PolylineArea.smethod_136(polylineArea2, True))
            if (self.parametersPanel.cmbUsedFor.SelectedIndex == 1 or self.parametersPanel.chbCatH.Checked):
                for entity in HoldingTemplateBase.smethod_2(polylineArea3, Distance(2.5, DistanceUnits.NM) if(self.parametersPanel.cmbUsedFor.SelectedIndex == 1) else Distance(2, DistanceUnits.NM)):
                    resultPolylineAreaList.append(entity)
            else:
                for entity1 in HoldingTemplateBase.smethod_1(polylineArea3, True):
                    resultPolylineAreaList.append(entity1)
            if self.parametersPanel.cmbOrientation.SelectedIndex == 0:
                polyline[0].bulge = -1
                polyline[2].bulge = -1
            else:
                polyline[0].bulge = 1
                polyline[2].bulge = 1
            resultPolylineAreaList.append(polyline)
            resultPolylineList = []
            for polylineArea in resultPolylineAreaList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea, True)
            #     point3dCollection = []
            #     for polylineAreaPoint in polylineArea:
            #
            #         point3dCollection.append(polylineAreaPoint.Position)
            #     resultPolylineList.append((point3dCollection, []))
            # constructionLayer = QgisHelper.createPolylineLayer(self.surfaceType, resultPolylineList)
            QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType, True)
            QgisHelper.zoomToLayers([constructionLayer])
            self.resultLayerList = [constructionLayer]
        else:
#             polyline.set_Elevation(self.pnlAltitude.Value.Metres);
#             polyline.set_Thickness(-self.pnlMoc.Value.Metres);
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Polygon)
            # mapUnits = define._canvas.mapUnits()
            # constructionLayer = None
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
            #
            # constructionLayer.startEditing()
            geometryList = []
            if (self.parametersPanel.cmbUsedFor.SelectedIndex == 1):
                distance = Distance(2.5, DistanceUnits.NM) if(self.parametersPanel.cmbUsedFor.SelectedIndex == 1) else Distance(2, DistanceUnits.NM)
                polylineArea, polylineArea1 = HoldingTemplateBase.smethod_4(polylineArea3, self.parametersPanel.txtAltitude.Value, self.parametersPanel.txtMoc.Value, distance);
#                 point3dCollection = polylineArea.method_15(False)
#                 point3dCollection1 = polylineArea1.method_15(False)
                geometryList = QgisHelper.smethod_146(polylineArea.method_15(True), polylineArea1.method_15(True));
                
            else:
                geometryList = HoldingTemplateBase.smethod_3(polylineArea3, self.parametersPanel.txtAltitude.Value, self.parametersPanel.txtMoc.Value);

            # feature = QgsFeature()
            # feature.setGeometry(QgsGeometry.fromPolygon([polyline.method_14_closed()]))
            # constructionLayer.addFeature(feature)
            i = 0
            for entity2 in geometryList:
                i += 1
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, PolylineArea(geometryList[len(geometryList) - i].asPolygon()[0]))
                # feature = QgsFeature()
                # feature.setGeometry(entity2)
                # constructionLayer.addFeature(feature)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polyline, True)
            
            # constructionLayer.commitChanges()
            QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType, True)
            QgisHelper.zoomToLayers([constructionLayer])
            self.resultLayerList = [constructionLayer]
        self.ui.btnEvaluate.setEnabled(True)
#                     AcadHelper.smethod_18(transaction, blockTableRecord, entity2, constructionLayer); 
        pass
    def initParametersPan(self):
        ui = Ui_HoldingOverHead()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        
        self.connect(self.parametersPanel.pnlNavAid, SIGNAL("positionChanged"), self.initResultPanel)
        self.connect(self.parametersPanel.pnlNavAid, SIGNAL("positionChanged"), self.iasChanged)



        self.parametersPanel.pnlWind.setAltitude(self.parametersPanel.txtAltitude.Value)
#                
        self.parametersPanel.cmbNavAidType.Items = ["VOR", "NDB"]
        self.parametersPanel.cmbUsedFor.Items = ["Holding", "Racetrack"]
        self.parametersPanel.cmbUsedFor.SelectedIndex = 1
        self.parametersPanel.cmbConstruction.Items = ["2D", "3D"]
        self.parametersPanel.cmbOrientation.Items = ["Right", "Left"]

        self.parametersPanel.chbSector1.Visible = False
        self.parametersPanel.chbSector2.Visible = False
        self.parametersPanel.chbSector3.Visible = False
        self.parametersPanel.chbCatH.Visible = False
        
        self.connect(self.parametersPanel.cmbNavAidType, SIGNAL("Event_0"), self.initBasedOnCmb)
        self.connect(self.parametersPanel.cmbUsedFor, SIGNAL("Event_0"), self.cmbUsedForCurrentIndexChanged)
        self.connect(self.parametersPanel.txtAltitude, SIGNAL("Event_0"), self.altitudeChanged)
        self.connect(self.parametersPanel.txtIas, SIGNAL("Event_0"), self.iasChanged)
        self.connect(self.parametersPanel.txtIsa, SIGNAL("Event_0"), self.iasChanged)


        self.parametersPanel.txtTas.Value = Speed.smethod_0(self.parametersPanel.txtIas.Value, self.parametersPanel.txtIsa.Value, self.parametersPanel.txtAltitude.Value - self.parametersPanel.pnlNavAid.Altitude())
    def cmbNavAidType_Event_0(self):
        self.parametersPanel.cmbBasedOn.Visible = self.parametersPanel.cmbNavAidType.SelectedIndex == 0
        if self.parametersPanel.cmbNavAidType.SelectedIndex == 1:
            self.parametersPanel.pnlNavAid.Point3d = None

    def cmbUsedForCurrentIndexChanged(self):
        if self.parametersPanel.cmbUsedFor.SelectedIndex == 0:
            self.parametersPanel.chbCatH.Visible = True
        else:
            self.parametersPanel.chbCatH.Visible = False
    def iasChanged(self):
        try:
            self.parametersPanel.txtTas.Value = Speed.smethod_0(self.parametersPanel.txtIas.Value, float(self.parametersPanel.txtIsa.Value), self.parametersPanel.txtAltitude.Value - self.parametersPanel.pnlNavAid.Altitude())
        except:
            raise ValueError("Value Invalid")
#         
#     def iasHelpShow(self):
#         dlg = IasHelpDlg()
#         dlg.exec_()
    def altitudeChanged(self):
        try:
            self.parametersPanel.txtTas.Value = Speed.smethod_0(self.parametersPanel.txtIas.Value, float(self.parametersPanel.txtIsa.Value), self.parametersPanel.txtAltitude.Value - self.parametersPanel.pnlNavAid.Altitude())
        except:
            raise ValueError("Value Invalid")
        self.parametersPanel.pnlWind.setAltitude(self.parametersPanel.txtAltitude.Value)
    def method_27(self):
        try:
            if (float(self.parametersPanel.txtTime.Value)< 1):
                QMessageBox.warning(self, "Warning", "Time's value can not be smaller than 1.")
                return False
            return True
        except:
            QMessageBox.warning(self, "Warning", "Time's value must be type of number.")
            return False
    def method_35(self):
        point3d = self.parametersPanel.pnlNavAid.Point3d;
        value = self.parametersPanel.txtAltitude.Value;
        metres = value.Metres - point3d.get_Z();
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 0):
            num = 25;
            num1 = 15;
            num2 = metres * 0.839099631;
        else:
            num = 15;
            num1 = 5;
            num2 = metres * 1.191753593;
        num3 = 1 if(self.parametersPanel.cmbOrientation.SelectedItem == OrientationType.Right) else -1
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
class HoldingOverheadArea:
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
    
class HoldingOverheadBufferEvaluator:
    def __init__(self, polylineArea_0, altitude_0, altitude_1):
        polylineAreaList = []

        polylineAreaList = HoldingTemplateBase.smethod_1(polylineArea_0, False);
        # polylineAreaList.append
        polylineAreaList.append(polylineArea_0)
        self.areas = []
        count = len(polylineAreaList)
        num = 0.1 * count;
        metres = altitude_1.Metres;
        for i in range(count):
            if (i > 0):
                metres = num * altitude_1.Metres;
                num = num - 0.1;
            self.areas.append(HoldingOverheadArea(polylineAreaList[i], Altitude(metres)));
        self.selectionArea = self.areas[len(self.areas) - 1].Area;
        self.altitude = altitude_0.Metres;
class HoldingOverheadSecondaryEvaluator:
    def __init__(self, polylineArea_0, altitude_0, altitude_1, distance_0):
        self.inner = PrimaryObstacleArea(polylineArea_0);
        self.outer = PrimaryObstacleArea(HoldingTemplateBase.smethod_5(polylineArea_0, distance_0));
        self.poly = PolylineArea.smethod_131(self.inner.previewArea);
        self.altitude = altitude_0.Metres;
        self.moc = altitude_1.Metres;
        self.offset = distance_0;
class HoldingOverHeadObstacles(ObstacleTable):
    def __init__(self, bool_0, typeStr, surfacesList = None, altitude = None, inner = None, outer = None, poly = None, altitude_1 = None, distance_0 = None):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
         
        self.surfaceType = SurfaceTypes.HoldingOverHead
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
                result, num, num1 = current.method_0
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
#             HoldingRnav.obstacles.method_12(obstacle_0, obstacleAreaResult, num, metres, z, criticalObstacleType);
# 
# #     def method_11(self, obstacle_0, double_0, double_1, criticalObstacleType_0):
# #         double0 = []
# #         double0.append(double_0)
# #         double0[self.IndexMocAppliedFt] = Unit.ConvertMeterToFeet(double_0);
# #         double0[self.IndexOcaM] = double_1;
# #         double0[self.IndexOcaFt] = Unit.ConvertMeterToFeet(double_1);
# #         double0[self.IndexCritical] = criticalObstacleType_0;
# #         return base.method_1(double0)
