# -*- coding: UTF-8 -*-
'''
Created on 30 Jun 2015

@author: Administrator
'''
from PyQt4.QtGui import QFileDialog, QColor, QStandardItem, QMessageBox
from PyQt4.QtCore import SIGNAL,Qt, QCoreApplication, QString
from qgis.core import QGis, QgsRectangle, QgsPoint, QgsVectorLayer
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapToolPan
from FlightPlanner.types import ConstructionType, CriticalObstacleType, ObstacleTableColumnType, OrientationType, DistanceUnits, AltitudeUnits, TurnDirection
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.OCAHPanel import OCAHPanel
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
# 
from FlightPlanner.Captions import Captions
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Ils.IlsBasic.ui_IlsBasic import Ui_IlsBasic
from FlightPlanner.DataHelper import DataHelper

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import Point3D, Point3dCollection, AltitudeUnits, SurfaceTypes
from FlightPlanner.polylineArea import PolylineArea
from FlightPlanner.helpers import Altitude, MathHelper, Unit
import define
import math

class IlsBasicDlg(FlightPlanBaseDlg):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("IlsBasic")
        self.surfaceType = SurfaceTypes.IlsBasic
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.IlsBasic)
        self.ilsBasicSurface = None
        self.resize(540, 300)
        QgisHelper.matchingDialogSize(self, 700, 450)
        self.manualPolygon = None

        self.arpFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.rwyFeatureArray = []
        self.thrPoint3d = None
        self.thrEndPoint3d = None
        self.initAerodromeAndRwyCmb()
    def initAerodromeAndRwyCmb(self):

        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.arpFeatureArray = self.aerodromeAndRwyCmbFill(self.currentLayer, self.parametersPanel.cmbAerodrome, None, self.parametersPanel.cmbRwyDir)
            self.calcRwyBearing()
    def calcRwyBearing(self):
        try:
            self.parametersPanel.txtTrack.Value = round(Unit.ConvertRadToDeg(MathHelper.getBearing(self.parametersPanel.pnlThr.Point3d, self.parametersPanel.pnlRwyEnd.Point3d)), 4)
        except:
            pass

    def aerodromeAndRwyCmbFill(self, layer, aerodromeCmbObj, aerodromePositionPanelObj, rwyDirCmbObj = None):
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')
        arpList = []
        arpFeatureList = []
        if idx >= 0:
            featIter = layer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idx].toString()
                attrValue = QString(attrValue)
                attrValue = attrValue.replace(" ", "")
                attrValue = attrValue.toUpper()
                if attrValue == "AERODROMEREFERENCEPOINT":
                    arpList.append(attrValue)
                    arpFeatureList.append(feat)
            if len(arpList) != 0:

                i = -1
                aerodromeCmbObjItems = []
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    items = aerodromeCmbObjItems
                    if len(items) != 0:
                        existFlag = False
                        for item in items:
                            if item == attrValue:
                                existFlag = True
                        if existFlag:
                            continue
                    aerodromeCmbObjItems.append(attrValue)
                aerodromeCmbObjItems.sort()
                aerodromeCmbObj.Items = aerodromeCmbObjItems
                aerodromeCmbObj.SelectedIndex = 0

                # if idxAttributes
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    if attrValue != aerodromeCmbObj.SelectedItem:
                        continue
                    attrValue = feat.attributes()[idxLat].toDouble()
                    lat = attrValue[0]

                    attrValue = feat.attributes()[idxLong].toDouble()
                    long = attrValue[0]

                    attrValue = feat.attributes()[idxAltitude].toDouble()
                    alt = attrValue[0]

                    # aerodromePositionPanelObj.Point3d = Point3D(long, lat, alt)
                    self.connect(aerodromeCmbObj, SIGNAL("Event_0"), self.aerodromeCmbObj_Event_0)
                    break
            if rwyDirCmbObj != None:
                idxAttr = layer.fieldNameIndex('Attributes')
                if idxAttr >= 0:
                    rwyFeatList = []
                    featIter = layer.getFeatures()
                    rwyDirCmbObjItems = []
                    for feat in featIter:
                        attrValue = feat.attributes()[idxAttr].toString()
                        if attrValue == aerodromeCmbObj.SelectedItem:
                            attrValue = feat.attributes()[idxName].toString()
                            s = attrValue.replace(" ", "")
                            compStr = s.left(6).toUpper()
                            if compStr == "THRRWY":
                                valStr = s.right(s.length() - 6)
                                rwyDirCmbObjItems.append(aerodromeCmbObj.SelectedItem + " RWY " + valStr)
                                rwyFeatList.append(feat)
                    rwyDirCmbObjItems.sort()
                    rwyDirCmbObj.Items = rwyDirCmbObjItems
                    self.connect(rwyDirCmbObj, SIGNAL("Event_0"), self.rwyDirCmbObj_Event_0)
                    self.rwyFeatureArray = rwyFeatList
                    self.rwyDirCmbObj_Event_0()

                    self.aerodromeCmbObj_Event_0()
                    self.calcRwyBearing()
        return arpFeatureList
    def rwyDirCmbObj_Event_0(self):
        if len(self.rwyFeatureArray) == 0:
            return
        idxName = self.currentLayer.fieldNameIndex('Name')
        idxLat = self.currentLayer.fieldNameIndex('Latitude')
        idxLong = self.currentLayer.fieldNameIndex('Longitude')
        idxAltitude = self.currentLayer.fieldNameIndex('Altitude')
        idxAttr = self.currentLayer.fieldNameIndex('Attributes')
        for feat in self.rwyFeatureArray:
            attrValue = feat.attributes()[idxName].toString()
            attrValueStr = QString(attrValue)
            attrValueStr = attrValueStr.replace(" ", "").right(attrValueStr.length() - 3)
            itemStr = self.parametersPanel.cmbRwyDir.SelectedItem
            itemStr = QString(itemStr)
            itemStr = itemStr.replace(" ", "").right(itemStr.length() - 4)
            if attrValueStr != itemStr:
                continue
            latAttrValue = feat.attributes()[idxLat].toDouble()
            lat = latAttrValue[0]

            longAttrValue = feat.attributes()[idxLong].toDouble()
            long = longAttrValue[0]

            altAttrValue = feat.attributes()[idxAltitude].toDouble()
            alt = altAttrValue[0]

            self.thrPoint3d = Point3D(long, lat, alt)
            self.parametersPanel.pnlThr.Point3d = Point3D(long, lat, alt)

            valStr = None
            if attrValue.right(1).toUpper() =="L" or attrValue.right(1).toUpper() =="R":
                s = attrValue.left(attrValue.length() - 1)
                valStr = s.right(2)
            else:
                valStr = attrValue.right(2)
            val = int(valStr)
            val += 18
            if val > 36:
                val -= 36
            newValStr = None
            if len(str(val)) == 1:
                newValStr = "0" + str(val)
            else:
                newValStr = str(val)
            otherAttrValue = attrValue.replace(valStr, newValStr)
            ss = otherAttrValue.right(1)
            if ss.toUpper() == "L":
                otherAttrValue = otherAttrValue.left(otherAttrValue.length() - 1) + "R"
            elif ss.toUpper() == "R":
                otherAttrValue = otherAttrValue.left(otherAttrValue.length() - 1) + "L"
            for feat in self.rwyFeatureArray:
                attrValue = feat.attributes()[idxName].toString()
                if attrValue != otherAttrValue:
                    continue
                latAttrValue = feat.attributes()[idxLat].toDouble()
                lat = latAttrValue[0]

                longAttrValue = feat.attributes()[idxLong].toDouble()
                long = longAttrValue[0]

                altAttrValue = feat.attributes()[idxAltitude].toDouble()
                alt = altAttrValue[0]

                self.thrEndPoint3d = Point3D(long, lat, alt)
                self.parametersPanel.pnlRwyEnd.Point3d = Point3D(long, lat, alt)
                break
            break
        self.calcRwyBearing()
    def aerodromeCmbObj_Event_0(self):
        if len(self.arpFeatureArray) == 0:
            return
        self.parametersPanel.pnlThr.Point3d = None
        self.thrPoint3d = None
        self.thrEndPoint3d = None
        idxName = self.currentLayer.fieldNameIndex('Name')
        idxLat = self.currentLayer.fieldNameIndex('Latitude')
        idxLong = self.currentLayer.fieldNameIndex('Longitude')
        idxAltitude = self.currentLayer.fieldNameIndex('Altitude')
        self.rwyFeatureArray = []
        # if idxAttributes
        for feat in self.arpFeatureArray:
            attrValue = feat.attributes()[idxName].toString()
            if attrValue != self.parametersPanel.cmbAerodrome.SelectedItem:
                continue
            attrValue = feat.attributes()[idxLat].toDouble()
            lat = attrValue[0]

            attrValue = feat.attributes()[idxLong].toDouble()
            long = attrValue[0]

            attrValue = feat.attributes()[idxAltitude].toDouble()
            alt = attrValue[0]

            # self.parametersPanel.pnlNavAid.Point3d = Point3D(long, lat, alt)
            break
        idxAttr = self.currentLayer.fieldNameIndex('Attributes')
        if idxAttr >= 0:
            self.parametersPanel.cmbRwyDir.Clear()
            rwyFeatList = []
            featIter = self.currentLayer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idxAttr].toString()
                if attrValue == self.parametersPanel.cmbAerodrome.SelectedItem:
                    attrValue = feat.attributes()[idxName].toString()
                    s = attrValue.replace(" ", "")
                    compStr = s.left(6).toUpper()
                    if compStr == "THRRWY":
                        valStr = s.right(s.length() - 6)
                        self.parametersPanel.cmbRwyDir.Add(self.parametersPanel.cmbAerodrome.SelectedItem + " RWY " + valStr)
                        rwyFeatList.append(feat)
                        self.rwyFeatureArray = rwyFeatList
            self.rwyDirCmbObj_Event_0()

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
        self.surfaceNames.pop(0)
        self.surfaceNames.insert(0, "")
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.IlsBasic, self.ui.tblObstacles, self.surfaceNames, parameterList, resultHideColumnNames)
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Threshold Position", "group"))
        longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlThr.txtPointX.text()), float(self.parametersPanel.pnlThr.txtPointY.text()))
        
        parameterList.append(("Lat", QgisHelper.strDegree(longLatPoint.get_Y())))
        parameterList.append(("Lon", QgisHelper.strDegree(longLatPoint.get_X())))
        parameterList.append(("X", self.parametersPanel.pnlThr.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlThr.txtPointY.text()))
        parameterList.append(("Altitude", self.parametersPanel.pnlThr.txtAltitudeM.text() + "m"))
        parameterList.append(("", self.parametersPanel.pnlThr.txtAltitudeFt.text() + "ft"))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("In-bount Track()", str(self.parametersPanel.txtTrack.Value)))
        parameterList.append(("Intermediate Segment Minmum", self.parametersPanel.pnlOCAH.txtAltitude.text() + "ft"))
        if self.parametersPanel.cmbGPA.Visible:
            parameterList.append(("Construction Type", self.parametersPanel.cmbGPA.SelectedItem))
        if self.parametersPanel.txtRDH.Visible:
            parameterList.append((self.parametersPanel.txtRDH.Caption, str(self.parametersPanel.txtRDH.Value.Metres) + "m"))
            parameterList.append(("", str(self.parametersPanel.txtRDH.Value.Feet) + "ft"))
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstructionType.SelectedItem))
        # parameterList.append(("MOCmultipiler", self.parametersPanel.mocSpinBox.text()))

        parameterList.append(("Results / Checked Obstacles", "group"))   
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList

    def initObstaclesModel(self):
        # ObstacleTable.MocMultiplier = self.parametersPanel.mocSpinBox.value()
        self.obstaclesModel = IlsBasicObstacles(self.ilsBasicSurface, self.manualPolygon, self.parametersPanel.txtHL.Value, self.parametersPanel.pnlThr.Point3d)
        
        return FlightPlanBaseDlg.initObstaclesModel(self)
    def surfaceChanged(self):
        if self.ui.cmbObstSurface.currentIndex() == 0:
            self.obstaclesModel.setFilterFixedString("")
        else:
            self.obstaclesModel.setFilterFixedString(self.ui.cmbObstSurface.currentText())
    def criticalDataClear(self):
        self.ui.txtOCHResults.setText("")
        self.ui.txtOCAResults.setText("")
        self.ui.txtCriticalID.setText("")
        self.ui.txtCriticalX.setText("")
        self.ui.txtCriticalY.setText("")
        self.ui.txtCriticalAltitudeM.setText("")
        self.ui.txtCriticalAltitudeFt.setText("")
        self.ui.txtCriticalSurface.setText("")
    def btnEvaluate_Click(self):
        self.criticalDataClear()
        num = 2.5 + self.parametersPanel.cmbGPA.SelectedIndex * 0.1;
        # for (int i = 0; i < this.pnlGPA.SelectedIndex; i++)
        # {
        #     num = num + 0.1;
        # }
        point3d = self.parametersPanel.pnlThr.Point3d;
        value = float(self.parametersPanel.txtTrack.Value);
        altitude = self.parametersPanel.pnlOCAH.method_3(self.parametersPanel.pnlThr.Altitude());
        metres = altitude.Metres;
        value1 = self.parametersPanel.txtRDH.Value#Altitude(float(self.parametersPanel.txtRDH.text()));
        self.ilsBasicSurface = IlsBasicSurfaces(point3d, value, metres, num, value1.Metres);
        # IlsBasic.IlsBasicEvaluator ilsBasicEvaluator = new IlsBasic.IlsBasicEvaluator(ilsBasicSurface, IlsBasic.obstacles);

        FlightPlanBaseDlg.btnEvaluate_Click(self)


        point3d = self.parametersPanel.pnlThr.Point3d

        # value = altitude
        metres2 = IlsBasicObstacles.resultCriticalObst.method_2(point3d).Metres
        # z = metres2 - point3d.z()
        # num3 = math.tan(Unit.ConvertDegToRad(num1))
        # num4 = z / num3
        # IlsBasicObstacles.resultSocPosition = MathHelper.distanceBearingPoint(point3d1, num + 3.14159265358979, num4).smethod_167(0)
        # if (num4 > zC):
        #     IlsBasicObstacles.resultSocText = Messages.X_BEFORE_THRESHOLD % (num4 - zC)
        # else:
        #     IlsBasicObstacles.resultSocText = Messages.X_PAST_THRESHOLD % (zC - num4)
        hlValue = self.parametersPanel.txtHL.Value#Altitude(float(self.parametersPanel.txtHL.text()))
        IlsBasicObstacles.resultOCA = Altitude(metres2)

        IlsBasicObstacles.resultOCH = Altitude(metres2 - point3d.get_Z())
        self.setCriticalObstacle()
        self.surfaceNames = ["All", Captions.TRANSITIONAL, Captions.STRIP, Captions.APPROACH + "_", Captions.MISSED_APPROACH]
        self.ui.cmbObstSurface.addItems(self.surfaceNames)
    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        num = 2.5 + self.parametersPanel.cmbGPA.SelectedIndex * 0.1;
        # for (int i = 0; i < self.pnlGPA.SelectedIndex; i++)
        # {
        #     num = num + 0.1;
        # }
        point3d = self.parametersPanel.pnlThr.Point3d;
        value = float(self.parametersPanel.txtTrack.Value);
        altitude = self.parametersPanel.pnlOCAH.method_3(self.parametersPanel.pnlThr.Altitude());
        metres = altitude.Metres;
        value1 = self.parametersPanel.txtRDH.Value#Altitude(float(self.parametersPanel.txtRDH.text()));
        ilsBasicSurface = IlsBasicSurfaces(point3d, value, metres, num, value1.Metres);
        mapUnits = define._canvas.mapUnits()
        constructionLayer = None
        resultPoint3dArrayList = []

        if (self.parametersPanel.cmbConstructionType.SelectedItem != ConstructionType.Construct2D):
            resultPoint3dArrayList = ilsBasicSurface.method_1()
            # if self.parametersPanel.cmbConstruct.currentText() == "2D":
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Polygon)
            # if define._mapCrs == None:
            #     if mapUnits == QGis.Meters:
            #         constructionLayer = QgsVectorLayer("polygon?crs=EPSG:32633", self.surfaceType , "memory")
            #     else:
            #         constructionLayer = QgsVectorLayer("polygon?crs=EPSG:4326", self.surfaceType , "memory")
            # else:
            #     constructionLayer = QgsVectorLayer("polygon?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")
            #
            # constructionLayer.startEditing()
            for pointArray in resultPoint3dArrayList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, pointArray)
            #     feature = QgsFeature()
            #     feature.setGeometry(QgsGeometry.fromPolygon([pointArray]))
            #     constructionLayer.addFeature(feature)
            # constructionLayer.commitChanges()
        else:
            resultPoint3dArrayList = ilsBasicSurface.method_0()
            constructionLayer = AcadHelper.createVectorLayer(self.surfaceType)
            for pointArray in resultPoint3dArrayList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, pointArray)
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType)
        QgisHelper.zoomToLayers([constructionLayer])
        self.resultLayerList = [constructionLayer]
        self.ui.btnEvaluate.setEnabled(True)
        self.manualEvent(self.parametersPanel.cmbSelectionMode.SelectedIndex)


    def outputResultMethod(self):
        self.manualPolygon = self.toolSelectByPolygon.polygonGeom
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
    def changeResultUnit(self):
        resultUnit = self.ui.cmbUnits.currentIndex()
        if resultUnit == AltitudeUnits.M:
            self.ui.txtOCAResults.setText(str(round(IlsBasicObstacles.resultOCA.Metres, 4)))
            self.ui.txtOCHResults.setText(str(round(IlsBasicObstacles.resultOCH.Metres, 4)))
        else:
            self.ui.txtOCAResults.setText(str(round(Unit.ConvertMeterToFeet(IlsBasicObstacles.resultOCA.Metres), 4)))
            self.ui.txtOCHResults.setText(str(round(Unit.ConvertMeterToFeet(IlsBasicObstacles.resultOCH.Metres), 4)))
    def menuSetCriticalObstClick(self):
        IlsBasicObstacles.resultCriticalObst.Obstacle = self.changedCriticalObstacleValue["Obstacle"]
        IlsBasicObstacles.resultCriticalObst.Surface = self.changedCriticalObstacleValue["SurfaceName"]
        IlsBasicObstacles.resultCriticalObst.Assigned = True
        IlsBasicObstacles.resultCriticalObst.eqAltitude = None
        ocaMValue = self.changedCriticalObstacleValue["OcaM"]
    
        IlsBasicObstacles.resultOCA = Altitude(float(ocaMValue) if ocaMValue != "" else None)
        if IlsBasicObstacles.resultOCA == None:
            IlsBasicObstacles.resultOCH = None
        else:
            IlsBasicObstacles.resultOCH = Altitude(IlsBasicObstacles.resultOCA.Metres - self.parametersPanel.pnlThr.Altitude().Metres)
        self.setCriticalObstacle()
    def setCriticalObstacle(self):
        resultUnit = self.ui.cmbUnits.currentIndex()
        if resultUnit == AltitudeUnits.M:
            self.ui.txtOCAResults.setText(str(round(IlsBasicObstacles.resultOCA.Metres, 4)))
            self.ui.txtOCHResults.setText(str(round(IlsBasicObstacles.resultOCH.Metres, 4)))
        else:
            self.ui.txtOCAResults.setText(str(round(Unit.ConvertMeterToFeet(IlsBasicObstacles.resultOCA.Metres), 4)))
            self.ui.txtOCHResults.setText(str(round(Unit.ConvertMeterToFeet(IlsBasicObstacles.resultOCH.Metres), 4)))
        
        if not IlsBasicObstacles.resultCriticalObst.Assigned:
            return 
        # self.ui.txtResultSocText.setText(IlsBasicObstacles.resultSocText)
        self.ui.txtCriticalX.setText(str(round(IlsBasicObstacles.resultCriticalObst.Position.x(), 4)))
        self.ui.txtCriticalY.setText(str(round(IlsBasicObstacles.resultCriticalObst.Position.y(), 4)))
        self.ui.txtCriticalAltitudeFt.setText(str(round(Unit.ConvertMeterToFeet(IlsBasicObstacles.resultCriticalObst.Position.z()), 4)))
        self.ui.txtCriticalAltitudeM.setText(str(round(IlsBasicObstacles.resultCriticalObst.Position.z(), 4)))
        self.ui.txtCriticalSurface.setText(IlsBasicObstacles.resultCriticalObst.Surface)
        self.ui.txtCriticalID.setText(IlsBasicObstacles.resultCriticalObst.Obstacle.name)
    def uiStateInit(self):
        # self.ui.grbMostCritical.setVisible(False)
        # self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        # self.ui.frm_cmbObstSurface.setVisible(False)
        
#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)
    def initParametersPan(self):
        ui = Ui_IlsBasic()
        self.parametersPanel = ui
        
        
        FlightPlanBaseDlg.initParametersPan(self)        

        self.ui.txtCriticalID.setEnabled(False)
        self.ui.txtCriticalX.setEnabled(False)
        self.ui.txtCriticalY.setEnabled(False)
        self.ui.txtCriticalAltitudeM.setEnabled(False)
        self.ui.txtCriticalAltitudeFt.setEnabled(False)
        self.ui.txtCriticalSurface.setEnabled(False)
        self.ui.txtOCAResults.setEnabled(False)
        self.ui.txtOCHResults.setEnabled(False)


        self.parametersPanel.pnlOCAH = OCAHPanel(self.parametersPanel.grbParameters)
        # self.parametersPanel.pnlOCAH.speedBox.setEnabled(True)
        self.parametersPanel.vLayout_grbParameters.insertWidget(1, self.parametersPanel.pnlOCAH)
        # self.parametersPanel.pnlOCAH.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
        
#         self.resize(460,600)
        self.parametersPanel.cmbConstructionType.Items = ["2D", "3D"]
        self.parametersPanel.cmbSelectionMode.Items = ["Automatic", "Manual"]

        for i in range(25, 100):
            num = round(float(i) / 10.0, 1)
            self.parametersPanel.cmbGPA.Add(str(num))
        self.parametersPanel.cmbGPA.SelectedIndex = 5

        self.parametersPanel.cmbAcCategory.Items = ["A", "B", "C", "D", "DL", "H"]
        self.parametersPanel.txtHL.Value = Altitude(40)
        self.parametersPanel.txtHL.Enabled = False

        # self.parametersPanel.btnCaptureTrack.clicked.connect(self.captureBearing)
        self.parametersPanel.pnlOCAH.txtAltitude.textChanged.connect(self.method_28)
        # self.ui.btnCriticalLocate.clicked.connect(self.criticalLocate)

        self.connect(self.parametersPanel.cmbAcCategory, SIGNAL("Event_0"), self.cmbAcCategoryIndexChanged)

        self.connect(self.parametersPanel.pnlThr, SIGNAL("positionChanged"), self.calcRwyBearing)
        self.connect(self.parametersPanel.pnlRwyEnd, SIGNAL("positionChanged"), self.calcRwyBearing)


        self.method_28()
    def cmbAcCategoryIndexChanged(self, index):
        if index == 0:
            self.parametersPanel.txtHL.Value = Altitude(40)
        elif index == 1:
            self.parametersPanel.txtHL.Value = Altitude(43)
        elif index == 2:
            self.parametersPanel.txtHL.Value = Altitude(46)
        elif index == 3:
            self.parametersPanel.txtHL.Value = Altitude(49)
        elif index == 4:
            self.parametersPanel.txtHL.Value = Altitude(49)
        elif index == 5:
            self.parametersPanel.txtHL.Value = Altitude(35)

    def method_28(self):
        isEmpty = not self.parametersPanel.pnlOCAH.IsEmpty;
        self.parametersPanel.cmbGPA.Visible = isEmpty
        self.parametersPanel.txtRDH.Visible = isEmpty


    def captureBearing(self):
        self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrack)
        define._canvas.setMapTool(self.captureTrackTool)

class IlsBasicSurfaces:
    ptTHRm90 = None;
    ptS1T = None;
    ptS1B = None;
    ptS2T = None;
    ptS2B = None;
    ptMA1T = None;
    ptMA1B = None;
    ptMA2T = None;
    ptMA2B = None;
    ptA2T = None;
    ptA2B = None;
    ptA1T = None;
    ptA1B = None;
    ptT1T = None;
    ptT2T = None;
    ptT3T = None;
    ptT4T = None;
    ptT1B = None;
    ptT2B = None;
    ptT3B = None;
    ptT4B = None;
    ptFAPT = None;
    ptFAPB = None;
    ptsTransT = Point3dCollection();
    ptsTransInnerT = Point3dCollection();
    ptsTransOuterT = Point3dCollection();
    ptsTransB = Point3dCollection();
    ptsTransInnerB = Point3dCollection();
    ptsTransOuterB = Point3dCollection();
    ptsApp = Point3dCollection();
    track = None;
    tr90p = None;
    tr90m = None;
    tr180 = None;

    def __init__(self, point3d_0, double_0, double_1, double_2, double_3):
        self.track = Unit.smethod_0(double_0);
        self.tr90p = self.track + 1.5707963267949;
        self.tr90m = self.track - 1.5707963267949;
        self.tr180 = self.track + 3.14159265358979;
        self.ptTHR = point3d_0;
        self.ptTHRm90 = MathHelper.distanceBearingPoint(point3d_0, self.tr90m, 100);
        point3d = MathHelper.distanceBearingPoint(point3d_0, self.tr180, 60);
        self.ptS1T = MathHelper.distanceBearingPoint(point3d, self.tr90m, 150);
        self.ptS1B = MathHelper.distanceBearingPoint(point3d, self.tr90p, 150);
        self.ptS2T = MathHelper.distanceBearingPoint(self.ptS1T, self.track, 960);
        self.ptS2B = MathHelper.distanceBearingPoint(self.ptS1B, self.track, 960);
        point3d = MathHelper.distanceBearingPoint(self.ptS2T, self.track, 1800);
        self.ptMA1T = MathHelper.distanceBearingPoint(point3d, self.tr90m, 314.64).smethod_167(point3d_0.get_Z() + 45);
        point3d = MathHelper.distanceBearingPoint(self.ptS2B, self.track, 1800);
        self.ptMA1B = MathHelper.distanceBearingPoint(point3d, self.tr90p, 314.64).smethod_167(point3d_0.get_Z() + 45);
        point3d = MathHelper.distanceBearingPoint(self.ptMA1T, self.track, 10200);
        self.ptMA2T = MathHelper.distanceBearingPoint(point3d, self.tr90m, 2550).smethod_167(point3d_0.get_Z() + 300);
        point3d = MathHelper.distanceBearingPoint(self.ptMA1B, self.track, 10200);
        self.ptMA2B = MathHelper.distanceBearingPoint(point3d, self.tr90p, 2550).smethod_167(point3d_0.get_Z() + 300);
        point3d = MathHelper.distanceBearingPoint(self.ptS1T, self.tr180, 3000);
        self.ptA2T = MathHelper.distanceBearingPoint(point3d, self.tr90m, 450).smethod_167(point3d_0.get_Z() + 60);
        point3d = MathHelper.distanceBearingPoint(self.ptS1B, self.tr180, 3000);
        self.ptA2B = MathHelper.distanceBearingPoint(point3d, self.tr90p, 450).smethod_167(point3d_0.get_Z() + 60);
        point3d = MathHelper.distanceBearingPoint(self.ptA2T, self.tr180, 9600);
        self.ptA1T = MathHelper.distanceBearingPoint(point3d, self.tr90m, 1440).smethod_167(point3d_0.get_Z() + 300);
        point3d = MathHelper.distanceBearingPoint(self.ptA2B, self.tr180, 9600);
        self.ptA1B = MathHelper.distanceBearingPoint(point3d, self.tr90p, 1440).smethod_167(point3d_0.get_Z() + 300);
        self.ptT1T = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, self.tr180, 3060), self.tr90m, 2278.3006993007).smethod_167(point3d_0.get_Z() + 300);
        self.ptT2T = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, self.tr180, 60), self.tr90m, 2247.88111888112).smethod_167(point3d_0.get_Z() + 300);
        self.ptT3T = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, self.tr180, -900), self.tr90m, 2247.9020979021).smethod_167(point3d_0.get_Z() + 300);
        self.ptT4T = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, self.tr180, -2700), self.tr90m, 2247.86713286713).smethod_167(point3d_0.get_Z() + 300);
        self.ptT1B = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, self.tr180, 3060), self.tr90p, 2278.3006993007).smethod_167(point3d_0.get_Z() + 300);
        self.ptT2B = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, self.tr180, 60), self.tr90p, 2247.88111888112).smethod_167(point3d_0.get_Z() + 300);
        self.ptT3B = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, self.tr180, -900), self.tr90p, 2247.9020979021).smethod_167(point3d_0.get_Z() + 300);
        self.ptT4B = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, self.tr180, -2700), self.tr90p, 2247.86713286713).smethod_167(point3d_0.get_Z() + 300);
        self.ptFAPT = self.ptA1T;
        self.ptFAPB = self.ptA1B;
        if (not double_1 == None):
            double1 = (double_1 - double_3) / math.tan(Unit.smethod_0(double_2));
            if (double1 > 12660):
                point3d1 = MathHelper.distanceBearingPoint(point3d_0, self.tr180, double1);
                self.ptFAPT = MathHelper.distanceBearingPoint(point3d1, self.tr90m, (double1 - 60) * 0.15 + 150).smethod_167(0.025 * (double1 - 3060) + self.ptA2T.get_Z());
                self.ptFAPB = MathHelper.distanceBearingPoint(point3d1, self.tr90p, (double1 - 60) * 0.15 + 150).smethod_167(0.025 * (double1 - 3060) + self.ptA2B.get_Z());
        point3dArray = [self.ptA1T, self.ptT1T, self.ptT2T, self.ptT3T, self.ptT4T, self.ptMA2T, self.ptMA1T, self.ptS2T, self.ptS1T, self.ptA2T, self.ptA1T];
        self.ptsTransT = PolylineArea(point3dArray).method_15(True);
        point3dArray1 = [self.ptA1T, self.ptA2T, self.ptS1T, self.ptS2T, self.ptMA1T, self.ptMA2T];
        self.ptsTransInnerT = PolylineArea(point3dArray1).method_15(True);
        point3dArray2 = [self.ptA1T, self.ptT1T, self.ptT2T, self.ptT3T, self.ptT4T, self.ptMA2T];
        self.ptsTransOuterT = PolylineArea(point3dArray2).method_15(True);
        point3dArray3 = [self.ptA1B, self.ptT1B, self.ptT2B, self.ptT3B, self.ptT4B, self.ptMA2B, self.ptMA1B, self.ptS2B, self.ptS1B, self.ptA2B, self.ptA1B];
        self.ptsTransB = PolylineArea(point3dArray3).method_15(True);
        point3dArray4 = [self.ptA1B, self.ptA2B, self.ptS1B, self.ptS2B, self.ptMA1B, self.ptMA2B];
        self.ptsTransInnerB = PolylineArea(point3dArray4).method_15(True);
        point3dArray5 = [self.ptA1B, self.ptT1B, self.ptT2B, self.ptT3B, self.ptT4B, self.ptMA2B];
        self.ptsTransOuterB = PolylineArea(point3dArray5).method_15(True);
        if (MathHelper.smethod_102(self.ptFAPT, self.ptA1T)):
            point3dArray6 = [self.ptA1T, self.ptA2T, self.ptS1T, self.ptS2T, self.ptMA1T, self.ptMA2T, self.ptMA2B, self.ptMA1B, self.ptS2B, self.ptS1B, self.ptA2B, self.ptA1B];
            self.ptsApp = PolylineArea(point3dArray6).method_15(True);
            return;
        point3dArray7 = [self.ptFAPT, self.ptA1T, self.ptA2T, self.ptS1T, self.ptS2T, self.ptMA1T, self.ptMA2T, self.ptMA2B, self.ptMA1B, self.ptS2B, self.ptS1B, self.ptA2B, self.ptA1B, self.ptFAPB];
        self.ptsApp = PolylineArea(point3dArray7).method_15(True);
    def method_0(self):
        # DBObjectCollection dBObjectCollection = new DBObjectCollection();
        point3dArrayList = []
        if (not MathHelper.smethod_102(self.ptFAPT, self.ptA1T)):
            point3dArray = [self.ptFAPT, self.ptA1T, self.ptT1T, self.ptT2T, self.ptT3T, self.ptT4T, self.ptMA2T, self.ptMA2B, self.ptT4B, self.ptT3B, self.ptT2B, self.ptT1B, self.ptA1B, self.ptFAPB ];
            point3dArrayList.append(PolylineArea(point3dArray).method_14_closed())
            # dBObjectCollection.Add(AcadHelper.smethod_130(point3dArray));
        else:
            point3dArray1 = [self.ptA1T, self.ptT1T, self.ptT2T, self.ptT3T, self.ptT4T, self.ptMA2T, self.ptMA2B, self.ptT4B, self.ptT3B, self.ptT2B, self.ptT1B, self.ptA1B];
            point3dArrayList.append(PolylineArea(point3dArray1).method_14_closed())
            # dBObjectCollection.Add(AcadHelper.smethod_130(point3dArray1));
        point3dArray2 = [self.ptS1T, self.ptS2T, self.ptS2B, self.ptS1B ];
        point3dArrayList.append(PolylineArea(point3dArray2).method_14_closed())
        # dBObjectCollection.Add(AcadHelper.smethod_130(point3dArray2));
        point3dArray3 = [self.ptA1T, self.ptA2T, self.ptS1T];
        point3dArrayList.append(point3dArray3)
        # dBObjectCollection.Add(AcadHelper.smethod_130(point3dArray3));
        point3dArray4 = [self.ptA1B, self.ptA2B, self.ptS1B];
        point3dArrayList.append(point3dArray4)
        # dBObjectCollection.Add(AcadHelper.smethod_130(point3dArray4));
        point3dArray5 = [self.ptS2T, self.ptMA1T, self.ptMA2T ];
        point3dArrayList.append(point3dArray5)
        # dBObjectCollection.Add(AcadHelper.smethod_130(point3dArray5));
        point3dArray6 = [self.ptS2B, self.ptMA1B, self.ptMA2B];
        point3dArrayList.append(point3dArray6)
        # dBObjectCollection.Add(AcadHelper.smethod_130(point3dArray6));
        point3dArray7 = [self.ptT1T, self.ptA2T, self.ptT1B, self.ptA2B ];
        point3dArrayList.append(point3dArray7)
        # dBObjectCollection.Add(AcadHelper.smethod_130(point3dArray7));
        point3dArray8 = [self.ptT2T, self.ptS1T ];
        point3dArrayList.append(point3dArray8)
        # dBObjectCollection.Add(AcadHelper.smethod_130(point3dArray8));
        point3dArray9 = [self.ptT2B, self.ptS1B ];
        point3dArrayList.append(point3dArray9)
        # dBObjectCollection.Add(AcadHelper.smethod_130(point3dArray9));
        point3dArray10 = [self.ptT4T, self.ptMA1T, self.ptMA1B, self.ptT4B ];
        point3dArrayList.append(point3dArray10)
        return point3dArrayList
    def method_1(self):
        point3dArrayList = []
        point3dArrayList.append([self.ptS1T, self.ptS2T, self.ptS2B, self.ptS1B, self.ptS1T])
        point3dArrayList.append([self.ptS2T, self.ptMA1T, self.ptMA1B, self.ptS2B, self.ptS2T])
        point3dArrayList.append([self.ptMA1T, self.ptMA2T, self.ptMA2B, self.ptMA1B, self.ptMA1T])
        point3dArrayList.append([self.ptFAPT, self.ptA2T, self.ptA2B, self.ptFAPB, self.ptFAPT])
        point3dArrayList.append([self.ptA2T, self.ptS1T, self.ptS1B, self.ptA2B, self.ptA2T])
        point3dArrayList.append([self.ptA1T, self.ptT1T, self.ptA2T, self.ptA1T])
        point3dArrayList.append([self.ptT1T, self.ptT2T, self.ptS1T, self.ptA2T, self.ptT1T])
        point3dArrayList.append([self.ptT2T, self.ptT3T, self.ptS2T, self.ptS1T, self.ptT2T])
        point3dArrayList.append([self.ptT3T, self.ptT4T, self.ptMA1T, self.ptS2T, self.ptT3T])
        point3dArrayList.append([self.ptT4T, self.ptMA2T, self.ptMA1T, self.ptT4T, self.ptT4T])
        point3dArrayList.append([self.ptA1B, self.ptT1B, self.ptA2B, self.ptA1B])
        point3dArrayList.append([self.ptT1B, self.ptT2B, self.ptS1B, self.ptA2B, self.ptT1B])
        point3dArrayList.append([self.ptT2B, self.ptT3B, self.ptS2B, self.ptS1B, self.ptT2B])
        point3dArrayList.append([self.ptT3B, self.ptT4B, self.ptMA1B, self.ptS2B, self.ptT3B])
        point3dArrayList.append([self.ptT4B, self.ptMA2B, self.ptMA1B, self.ptT4B])
        return point3dArrayList
    
    def method_2(self, obstacle_0):
        point3d = None;
        point3d1 = None;
        string_0 = None;
        double_0 = None;
        double_1 = None;
        z = obstacle_0.Position.get_Z() + obstacle_0.Trees;
        if (not MathHelper.pointInPolygon(self.ptsApp, obstacle_0.Position, obstacle_0.Tolerance)):
            if (MathHelper.pointInPolygon(self.ptsTransT, obstacle_0.Position, obstacle_0.Tolerance)):
                string_0 = Captions.TRANSITIONAL;
                double_0 = self.method_3(obstacle_0, self.ptsTransInnerT, self.ptsTransOuterT);
                double_1 = z - double_0;
                return (True, string_0, double_0, double_1);
            if (not MathHelper.pointInPolygon(self.ptsTransB, obstacle_0.Position, obstacle_0.Tolerance)):
                return (False, string_0, double_0, double_1);
            string_0 = Captions.TRANSITIONAL;
            double_0 = self.method_3(obstacle_0, self.ptsTransInnerB, self.ptsTransOuterB);
            double_1 = z - double_0;
            return (True, string_0, double_0, double_1);
        if (not MathHelper.smethod_115(obstacle_0.Position, self.ptTHR, self.ptTHRm90)):
            point3d1 = MathHelper.getIntersectionPoint(obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, self.tr180, 100), self.ptTHR, self.ptTHRm90);
            num = MathHelper.calcDistance(obstacle_0.Position, point3d1) - obstacle_0.Tolerance;
            if (num <= 900):
                string_0 = Captions.STRIP;
                double_0 = self.ptTHR.get_Z();
                double_1 = z - double_0;
                return (True, string_0, double_0, double_1);
            string_0 = Captions.MISSED_APPROACH;
            double_0 = self.ptTHR.get_Z() + (num - 900) * 0.025;
            double_1 = z - double_0;
            return (True, string_0, double_0, double_1);
        point3d = MathHelper.getIntersectionPoint(obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, self.track, 100), self.ptTHR, self.ptTHRm90);
        num1 = MathHelper.calcDistance(obstacle_0.Position, point3d) - obstacle_0.Tolerance;
        if (num1 <= 60):
            string_0 = Captions.STRIP;
            double_0 = self.ptTHR.get_Z();
            double_1 = z - double_0;
            return (True, string_0, double_0, double_1);
        if (num1 <= 3060):
            string_0 = Captions.APPROACH + "_";
            double_0 = self.ptTHR.get_Z() + (num1 - 60) * 0.02;
            double_1 = z - double_0;
            return (True, string_0, double_0, double_1);
        string_0 = Captions.APPROACH + "_";
        double_0 = self.ptTHR.get_Z() + 60 + (num1 - 3060) * 0.025;
        double_1 = z - double_0;
        return (True, string_0, double_0, double_1);

    def method_3(self, obstacle_0, point3dCollection_0, point3dCollection_1):
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
        point3d4 = None;
        point3d5 = None;
        z = point3dCollection_1.get_Item(0).get_Z();
        for point3dCollection1 in point3dCollection_1:
            z = max([z, point3dCollection1.get_Z()]);
        point3d6 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.tr180, obstacle_0.Tolerance);
        position = obstacle_0.Position;
        point3d7 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.track, obstacle_0.Tolerance);
        for i in range(1, point3dCollection_0.get_Count() - 1):
            item = point3dCollection_0.get_Item(i - 1);
            item1 = point3dCollection_0.get_Item(i);
            item2 = point3dCollection_1.get_Item(i - 1);
            item3 = point3dCollection_1.get_Item(i);
            point3d = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, self.tr90m, 100), item, item1);
            point3d1 = MathHelper.getIntersectionPoint(position, MathHelper.distanceBearingPoint(position, self.tr90m, 100), item, item1);
            point3d2 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, self.tr90m, 100), item, item1);
            point3d3 = MathHelper.getIntersectionPoint(point3d6, MathHelper.distanceBearingPoint(point3d6, self.tr90m, 100), item2, item3);
            point3d4 = MathHelper.getIntersectionPoint(position, MathHelper.distanceBearingPoint(position, self.tr90m, 100), item2, item3);
            point3d5 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, self.tr90m, 100), item2, item3);
            num = MathHelper.calcDistance(item, item1);
            num1 = MathHelper.calcDistance(item2, item3);
            if (MathHelper.smethod_110(point3d, item, item1)):
                z1 = item.get_Z() + MathHelper.calcDistance(item, point3d) * ((item1.get_Z() - item.get_Z()) / num);
                z2 = item2.get_Z() + MathHelper.calcDistance(item2, point3d3) * ((item3.get_Z() - item2.get_Z()) / num1);
                num2 = self.method_4(point3d.smethod_167(z1), point3d3.smethod_167(z2), point3d6, obstacle_0.Tolerance);
                z = min([num2, z]);
            if (MathHelper.smethod_110(point3d1, item, item1)):
                z3 = item.get_Z() + MathHelper.calcDistance(item, point3d1) * ((item1.get_Z() - item.get_Z()) / num);
                num3 = item2.get_Z() + MathHelper.calcDistance(item2, point3d4) * ((item3.get_Z() - item2.get_Z()) / num1);
                num4 = self.method_4(point3d1.smethod_167(z3), point3d4.smethod_167(num3), position, obstacle_0.Tolerance);
                z = min([num4, z]);
            if (MathHelper.smethod_110(point3d2, item, item1)):
                z4 = item.get_Z() + MathHelper.calcDistance(item, point3d2) * ((item1.get_Z() - item.get_Z()) / num);
                z5 = item2.get_Z() + MathHelper.calcDistance(item2, point3d5) * ((item3.get_Z() - item2.get_Z()) / num1);
                num5 = self.method_4(point3d2.smethod_167(z4), point3d5.smethod_167(z5), point3d7, obstacle_0.Tolerance);
                z = min([num5, z]);
        return z;

    def method_4(self, point3d_0, point3d_1, point3d_2, double_0):
        num = max([MathHelper.calcDistance(point3d_0, point3d_2) - double_0, 0]);
        num1 = MathHelper.calcDistance(point3d_0, point3d_1);
        if (MathHelper.smethod_96(num1)):
            return point3d_0.get_Z();
        return point3d_0.get_Z() + (point3d_1.get_Z() - point3d_0.get_Z()) / num1 * num;

    def get_SelectionArea(self):
        if (MathHelper.smethod_102(self.ptFAPT, self.ptA1T)):
            point3dArray = [self.ptA1T, self.ptT1T, self.ptT2T, self.ptT3T, self.ptT4T, self.ptMA2T, self.ptMA2B, self.ptT4B, self.ptT3B, self.ptT2B, self.ptT1B, self.ptA1B];
            return PolylineArea(point3dArray);
        point3dArray1 = [self.ptFAPT, self.ptA1T, self.ptT1T, self.ptT2T, self.ptT3T, self.ptT4T, self.ptMA2T, self.ptMA2B, self.ptT4B, self.ptT3B, self.ptT2B, self.ptT1B, self.ptA1B, self.ptFAPB];
        return PolylineArea(point3dArray1);
    SelectionArea = property(get_SelectionArea, None, None, None)

class IlsBasicCriticalObstacle:

    def get_Position(self):
        if not self.Assigned:
            return None
        return self.Obstacle.Position

    Position = property(get_Position, None, None, None)

    def __init__(self):
        self.eqAltitude = None
        self.Assigned = False

    def method_0(self, obstacle_0, double_0, oasSurface_0, oca):
        if (self.Assigned):
            # double0 = double_0;
            # if double0 == None:
            #     double0 = obstacle_0.position.z() + obstacle_0.trees;
            z = self.eqAltitude;
            if z == None:
                position = self.Obstacle.Position;
                z = position.z() + self.Obstacle.trees
            if (z > oca):
                return;
            elif z == oca:
                if self.Obstacle.Position.z() <= obstacle_0.Position.z():
                    return

        self.Obstacle = obstacle_0;
        self.eqAltitude = oca;
        self.Surface = oasSurface_0;
        self.Assigned = True;
        # self.SurfAltM = surfAltM

    def method_1(self):
        self.Assigned = False

    def method_2(self, point3d_0):
        if (not self.Assigned):
            return Altitude(point3d_0.z())
        if self.eqAltitude != None:
            return Altitude(self.eqAltitude)
        position = self.Obstacle.position
        return Altitude(position.z() + self.Obstacle.trees)


class IlsBasicObstacles(ObstacleTable):
    obstaclesChecked = 0
    resultOCH = Altitude(0)
    resultOCA = Altitude(0)
    resultSocText = ""
    resultSocPosition = Point3D()
    tempSurfaceNames = []
    resultCriticalObst = IlsBasicCriticalObstacle()
    def __init__(self, ilsBasicSurfaces_0, manualPoly, hlAititude, point3dThr):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, ilsBasicSurfaces_0)
        
        self.surfaceType = SurfaceTypes.IlsBasic
        self.obstaclesChecked = None
        self.surfaces = ilsBasicSurfaces_0
        self.manualPolygon = manualPoly
        self.hlAltitude = hlAititude
        self.point3dThr = point3dThr
        # self.area = surfacesArea
        # self.primaryMoc = altitude_0.Metres;
        # self.enrouteAltitude = altitude_1.Metres;
    def setHiddenColumns(self, tableView):
        tableView.hideColumn(self.IndexObstArea)
        tableView.hideColumn(self.IndexDistInSecM)
        # tableView.hideColumn(self.IndexAltM)
        # tableView.hideColumn(self.IndexAltFt)

        return ObstacleTable.setHiddenColumns(self, tableView)

    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexSurface = fixedColumnCount
        self.IndexSurfAltM = fixedColumnCount + 1
        self.IndexSurfAltFt = fixedColumnCount + 2
        self.IndexDifferenceM = fixedColumnCount + 3
        self.IndexDifferenceFt = fixedColumnCount + 4
        self.IndexOcaM = fixedColumnCount + 5
        self.IndexOcaFt = fixedColumnCount + 6
        self.IndexOchM = fixedColumnCount + 7
        self.IndexOchFt = fixedColumnCount + 8
        self.IndexCritical = fixedColumnCount + 9
                 
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.Surface,
                ObstacleTableColumnType.SurfAltM,
                ObstacleTableColumnType.SurfAltFt,
                ObstacleTableColumnType.DifferenceM,
                ObstacleTableColumnType.DifferenceFt,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt,
                ObstacleTableColumnType.OchM,
                ObstacleTableColumnType.OchFt,
                ObstacleTableColumnType.Critical            
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
    def addObstacleToModel(self, obstacle, checkResult):
        ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
        row = self.source.rowCount() - 1

        item = QStandardItem(str(checkResult[0]))
        item.setData(checkResult[0])
        self.source.setItem(row, self.IndexSurface, item)
          
        # item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[0])))
        # item.setData(Unit.ConvertMeterToFeet(checkResult[0]))
        # self.source.setItem(row, self.IndexMocAppliedFt, item)
        #
        # item = QStandardItem(str(ObstacleTable.MocMultiplier))
        # item.setData(ObstacleTable.MocMultiplier)
        # self.source.setItem(row, self.IndexMocMultiplier, item)
          
        item = QStandardItem(str(checkResult[1]))
        item.setData(checkResult[1])
        self.source.setItem(row, self.IndexSurfAltM, item)
          
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[1])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[1]))
        self.source.setItem(row, self.IndexSurfAltFt, item)

        item = QStandardItem(str(checkResult[2]))
        item.setData(checkResult[2])
        self.source.setItem(row, self.IndexDifferenceM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[2])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[2]))
        self.source.setItem(row, self.IndexDifferenceFt, item)

        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexOcaM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[4])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[4]))
        self.source.setItem(row, self.IndexOcaFt, item)

        item = QStandardItem(str(checkResult[5]))
        item.setData(checkResult[5])
        self.source.setItem(row, self.IndexOchM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[5])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[5]))
        self.source.setItem(row, self.IndexOchFt, item)
        
        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexCritical, item) 
#     def method_11(self, obstacle_0, double_0, double_1, criticalObstacleType_0):
#         double0 = []
#         double0.append(double_0)#[self.IndexMocAppliedM] = double_0
# #         double0.append(Unit.ConvertMeterToFeet(double_0))#[self.IndexMocAppliedFt] = Unit.ConvertMeterToFeet(double_0)
# #         double0.append(ObstacleTable.method_1(double0))
#         double0.append(double_1)#[self.IndexOcaM] = double_1
# #         double0[self.IndexOcaFt] = Unit.ConvertMeterToFeet(double_1)
# #         double0[self.IndexCritical] = criticalObstacleType_0;
#         return ObstacleTable.method_1(double0)
    def checkObstacle(self, obstacle_0):
        str = None;
        num = None;
        num1 = None;
        string0 = None
        if self.manualPolygon != None:
            if not self.manualPolygon.contains(obstacle_0.Position):
                return
        result, str, num, num1 = self.surfaces.method_2(obstacle_0)
        oca = None
        och = None
        if (result):
            # self.tempSurfaceNames.append(str)
            if (num1 <= 0):
                string0 = CriticalObstacleType.No;
            else:
                string0 = CriticalObstacleType.Yes;

                oca = obstacle_0.Position.get_Z() + self.hlAltitude.Metres
                och = obstacle_0.Position.get_Z() + self.hlAltitude.Metres - self.point3dThr.get_Z()
                IlsBasicObstacles.resultCriticalObst.method_0(obstacle_0, num1, str, oca)
            self.addObstacleToModel(obstacle_0, [str, num, num1, string0, oca, och])

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