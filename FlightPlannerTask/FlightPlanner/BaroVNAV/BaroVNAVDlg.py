# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt, QString,QVariant
from PyQt4.QtGui import QMessageBox, QStandardItem,QApplication, QFileDialog, QLabel, QSpinBox, QFrame, QHBoxLayout
from qgis.core import QgsDataSourceURI,QgsRasterLayer,QgsCredentials, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes, DistanceUnits,AircraftSpeedCategory,\
    AerodromeSurfacesCriteriaType, AltitudeUnits, ObstacleAreaResult, RnavSpecification, RnavGnssFlightPhase, SpeedUnits, AngleUnits, ConstructionType
from FlightPlanner.BaroVNAV.ui_BaroVNAV import Ui_BaroVNAV
from FlightPlanner.expressions import Expressions
from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.RnavTolerance0 import RnavGnssTolerance
from FlightPlanner.Captions import Captions
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.types import Point3D, Point3dCollection
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, SecondaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.TempCorrection.TempCorrection import TempCorrection
from FlightPlanner.messages import Messages
from Type.switch import switch
from Type.Degrees import Degrees
# from Composer.ComposerDlg import ComposerDlg

import define, math
from ctypes import cdll
# #load dll file , the file in the same .py file location or enter the full path
# mylib=cdll.LoadLibrary("E:\CholNam\FlightPlanner\Resource\dlls\SKGL.dll")
# import mylib

# from FlightPlanner.BaroVNAV.clr import clr
class BaroVNAVDlg(FlightPlanBaseDlg):
    obstacles = [];

    obstaclesChecked = 0;

    resultOCH = None;

    resultOCA = None;

    resultCriticalObst = None

    calculationResults = [];


    # #call a function from this dll (c-ext)
    # ReturnedValue=mylib.FunctionName()

    s = "assd"
    # print len(s)
    # pass

    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)

        self.customIas = Speed(185);
        self.customIasAtThr = Speed(165);
        self.segmentTerminationDist = Distance(5, DistanceUnits.NM);
        self.maptDist = Distance(0.5, DistanceUnits.NM);
        BaroVNAVDlg.resultCriticalObst = BaroVnavCriticalObstacle();

        self.setObjectName("PathTerminatorsDlg")
        self.surfaceType = SurfaceTypes.BaroVNAV
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.BaroVNAV)
        self.resize(600, 610)
        QgisHelper.matchingDialogSize(self, 670, 700)
        self.surfaceList = None

        self.calculationResults = []

        self.resultLayerList = []

        # aerodromeSurfacesApproachType_0 = AerodromeSurfacesCriteriaType.Annex14
        # for case0 in switch(aerodromeSurfacesApproachType_0):
        #     if case0(AerodromeSurfacesCriteriaType.Custom):
        #         pass
        #     if case0(AerodromeSurfacesCriteriaType.Annex14):
        #         pass
        # g = QgsGeometry()
        # g.simplify(0,5)
        # p1 = Point3D(24.438694444444444444444444444444, 54.446305555555555555555555555556)
        # p2 = Point3D(24.397726111111111111111111111111, 54.3294125)
        # d = MathHelper.calcDistance(p1, p2)
        # b1 = Unit.ConvertRadToDeg(MathHelper.getBearing(p1, p2))
        # b2 = Unit.ConvertRadToDeg(MathHelper.getBearing(p2, p1))

        # uri = QgsDataSourceURI()
        # uri. setDatabase("D:/hg.dll")
        # schema = ""
        # table = "hg"
        # geom_column = "Geometry"
        # uri. setDataSource(schema, table, geom_column)
        # display_name = "Towns"
        # vlayer = QgsVectorLayer(uri. uri(), display_name, 'spatialite')
        # a, b = vlayer.loadNamedStyle("D:/a.qml")
        # QgisHelper.appendToCanvas(define._canvas, [vlayer])

        # connInfo = QgsDataSourceURI(vlayer.dataProvider().dataSourceUri()).connectionInfo()
        # # QgsCredentials.put(connInfo, "a", "sda")
        # QgsCredentials.instance().put(connInfo, "as", "asd")
        # success, username, password = QgsCredentials.instance().get(connInfo, "", "")
        # if success:
        #
        #     pass

        self.arpFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.rwyFeatureArray = []
        self.initAerodromeAndRwyCmb()
    def initAerodromeAndRwyCmb(self):
        # self.currentLayer = define._canvas.currentLayer()
        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.arpFeatureArray = self.aerodromeAndRwyCmbFill(self.currentLayer, self.parametersPanel.cmbAerodrome, self.parametersPanel.pnlArp, self.parametersPanel.cmbRwyDir)
            self.calcRwyBearing()
    def calcRwyBearing(self):
        try:
            point3End = self.parametersPanel.pnlThrEnd.Point3d
            point3dThr = self.parametersPanel.pnlThr.Point3d
            self.parametersPanel.pnlRwyDir.Value = round(Unit.ConvertRadToDeg(MathHelper.getBearing(point3dThr, point3End)), 4)
        except:
            pass


#         self.ui.horizontalLayout_6.addWidget(self.ui.frame_3)
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
                attrValueList = []
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    items = attrValueList
                    if len(items) != 0:
                        existFlag = False
                        for item in items:
                            if item == attrValue:
                                existFlag = True
                        if existFlag:
                            continue
                    attrValueList.append(attrValue)
                attrValueList.sort()
                aerodromeCmbObj.Items = attrValueList
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

                    aerodromePositionPanelObj.Point3d = Point3D(long, lat, alt)
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
        # rwyFeatList = []
        featIter = self.currentLayer.getFeatures()
        # for feat in featIter:
        #     attrValue = feat.attributes()[idxAttr].toString()
        #     if attrValue == self.cmbAerodrome.SelectedItem:
        #         attrValue = feat.attributes()[idxName].toString()
        #         s = attrValue.replace(" ", "")
        #         compStr = s.left(6).toUpper()
        #         if compStr == "THRRWY":
        #             valStr = s.right(s.length() - 6)
        #             rwyFeatList.append(feat)
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

                self.parametersPanel.pnlThrEnd.Point3d = Point3D(long, lat, alt)
                break
            break
        self.calcRwyBearing()
    def aerodromeCmbObj_Event_0(self):
        if len(self.arpFeatureArray) == 0:
            return
        self.parametersPanel.pnlArp.Point3d = None
        self.parametersPanel.pnlThr.Point3d = None
        self.parametersPanel.pnlThrEnd.Point3d = None
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

            self.parametersPanel.pnlArp.Point3d = Point3D(long, lat, alt)
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

    def initObstaclesModel(self):
        self.obstaclesModel.MocMultiplier = 1
        return FlightPlanBaseDlg.initObstaclesModel(self)

    
    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return  
        self.filterList = []
        self.filterList.append("")
        for surf in self.surfaceList:
            self.filterList.append(surf.type)
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.BaroVNAV, self.ui.tblObstacles, self.filterList, parameterList, resultHideColumnNames)
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Aerodrome", "group"))
        parameterList.append(("Reference Point (ARP)", "group"))
        # longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlArp.txtPointX.text()), float(self.parametersPanel.pnlArp.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlArp.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlArp.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlArp.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlArp.txtPointY.text()))
        parameterList.append(("Altitude", self.parametersPanel.pnlArp.txtAltitudeM.text() + "m"))
        parameterList.append(("", self.parametersPanel.pnlArp.txtAltitudeFt.text() + "ft"))

        parameterList.append(("Minimum Temperature", str(self.parametersPanel.pnlMinTemp.Value) + define._degreeStr))

        parameterList.append(("Runway", "group"))
        parameterList.append(("Threshold Position", "group"))
        # longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlThr.txtPointX.text()), float(self.parametersPanel.pnlThr.txtPointY.text()))

        parameterList.append(("Lat", self.parametersPanel.pnlThr.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlThr.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlThr.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlThr.txtPointY.text()))
        parameterList.append(("Altitude", self.parametersPanel.pnlThr.txtAltitudeM.text() + "m"))
        parameterList.append(("", self.parametersPanel.pnlThr.txtAltitudeFt.text() + "ft"))


        parameterList.append(("Direction", "Plan : " + str(self.parametersPanel.pnlRwyDir.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.pnlRwyDir.txtRadialGeodetic.Value) + define._degreeStr))


        parameterList.append(("Parameters", "group"))
        parameterList.append(("Intermediate Segment", str(self.parametersPanel.pnlOCAH.Value.Feet) + "ft"))
        parameterList.append(("Intermediate Segment MOC", str(self.parametersPanel.pnlMocI.Value.Metres) + "m"))
        parameterList.append(("RDH at THR", str(self.parametersPanel.pnlRDH.Value.Metres) + "m"))
        parameterList.append(("RDH at THR", str(self.parametersPanel.pnlRDH.Value.Metres) + "m"))
        parameterList.append(("Vertical Path Angle [VPA]", str(self.parametersPanel.pnlVPA.SelectedItem[:3])))
        parameterList.append(("THR to FAWP Distance", str(self.parametersPanel.pnlThrFafDist.Value.NauticalMiles) + "nm"))
        parameterList.append(("Aircraft Category", str(self.parametersPanel.pnlAcCat.SelectedItem)))
        parameterList.append(("Max. IAS", str(self.parametersPanel.pnlIas.Value.Knots) + "kts"))
        parameterList.append(("Max. IAS at THR", str(self.parametersPanel.pnlIasAtThr.Value.Knots) + "kts"))
        parameterList.append(("Height Loss", str(self.parametersPanel.pnlHL.Value.Metres) + "m"))
        parameterList.append(("Temperature Correction", str(self.parametersPanel.pnlTC.Value.Metres) + "m"))
        parameterList.append(("APV Segment Termination", str(self.parametersPanel.cmbTermination.SelectedItem)))
        parameterList.append(("", "Dist. : " + str(self.parametersPanel.pnlTerminationDist.Value.NauticalMiles) + "nm"))
        parameterList.append(("Missed Approach Point", str(self.parametersPanel.cmbMAPt.SelectedItem)))
        parameterList.append(("", "Dist. : " + str(self.parametersPanel.pnlMAPtDist.Value.NauticalMiles) + "nm"))
        parameterList.append(("Missed Approach Climb Gradient", str(self.parametersPanel.pnlMACG.Value) + "%"))
        parameterList.append(("Missed Approach MOC", str(self.parametersPanel.pnlMocMA.Value.Metres) + "m"))
        parameterList.append(("Missed Approach Evaluation", str(self.parametersPanel.pnlEvalMethodMA.SelectedItem)))
        parameterList.append(("Construction Type", str(self.parametersPanel.pnlConstructionType.SelectedItem)))
        
        parameterList.append(("Results / Checked Obstacles", "group"))   
        parameterList.append(("Checked Obstacles", "group"))
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))
        return parameterList
    
    def uiStateInit(self):
        # self.ui.grbMostCritical.setVisible(False)
        # self.ui.grbResult_2.setVisible(False)
        # self.ui.btnUpdateQA.setVisible(False)
        # self.ui.btnUpdateQA_2.setVisible(False)
        # self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)

        self.ui.txtCriticalID.setEnabled(False)
        self.ui.txtCriticalX.setEnabled(False)
        self.ui.txtCriticalY.setEnabled(False)
        self.ui.txtCriticalAltitudeM.setEnabled(False)
        self.ui.txtCriticalAltitudeFt.setEnabled(False)
        self.ui.txtCriticalSurface.setEnabled(False)
        self.ui.txtOCAResults.setEnabled(False)
        self.ui.txtOCHResults.setEnabled(False)



        return FlightPlanBaseDlg.uiStateInit(self)
    def btnPDTCheck_Click(self):
        # clip = QApplication.clipboard()
        # clip.setText("asadasf")

        resultString = ""
        if not self.parametersPanel.pnlArp.IsValid():
            QMessageBox.warning(self, "Warning", "Please pick up the " + self.parametersPanel.pnlArp.Caption + ".")
            return
        if not self.parametersPanel.pnlThr.IsValid():
            QMessageBox.warning(self, "Warning", "Please pick up the " + self.parametersPanel.pnlThr.Caption + ".")
            return
        baroVnavSurfaces, num = self.method_51();
        if len(self.calculationResults) == 0:
            return
        for cur in self.calculationResults:
            resultString += cur + "\n"
        QMessageBox.warning(self, "Reports", resultString)
    def btnEvaluate_Click(self):
        self.method_31();
        baroVnavSurfaces, num = self.method_51();
        # for baroVnavSurface in baroVnavSurfaces:
        #     BaroVNAVDlg.obstacles.append(BaroVnavObstacles(baroVnavSurface.Type));
        # point3dCollection = Point3dCollection();
        # point3dCollection1 = Point3dCollection();
        # for baroVnavSurface1 in baroVnavSurfaces:
        #     point3dCollection.appendList(baroVnavSurface1.LineSL);
        #     point3dCollection1.appendList(baroVnavSurface1.LineSR);
        # point3dCollection1.reverse()
        # point3dCollection.appendList(point3dCollection1);
        baroVnavMaEvaluationMethod = self.parametersPanel.pnlEvalMethodMA.SelectedIndex
        num1 = math.tan(Unit.ConvertDegToRad(self.method_39()))
        percent = self.parametersPanel.pnlMACG.Value / 100;
        # baroVnavObstacles = BaroVNAVDlg.obstacles;
        value = self.parametersPanel.pnlHL.Value;

        self.obstaclesModel = BaroVnavObstacles(baroVnavSurfaces, baroVnavMaEvaluationMethod, percent, num1, num, value.Metres, self.parametersPanel.pnlThr.Point3d)
        FlightPlanBaseDlg.btnEvaluate_Click(self)
        self.ui.cmbObstSurface.addItems(["All","FAS", "H", "Z"])
        self.setCriticalObstacle()
        self.cmbObstSurface_currentIndexChanged()
    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return

        if not self.parametersPanel.pnlArp.IsValid():
            QMessageBox.warning(self, "Warning", "Please pick up the " + self.parametersPanel.pnlArp.Caption + ".")
            return
        if not self.parametersPanel.pnlThr.IsValid():
            QMessageBox.warning(self, "Warning", "Please pick up the " + self.parametersPanel.pnlThr.Caption + ".")
            return

        baroVnavSurfaces, num = self.method_51();

        if baroVnavSurfaces == None and num == None:
            return

        constructionLayer = None;
        mapUnits = define._canvas.mapUnits()
        self.surfaceList = baroVnavSurfaces
        for i in range(len(baroVnavSurfaces)):
            if (self.parametersPanel.pnlConstructionType.Value == 0):
                constructionLayer = AcadHelper.createVectorLayer(baroVnavSurfaces[i].type, QGis.Line)
                baroVnavSurfaces[i].vmethod_1(constructionLayer, i == len(baroVnavSurfaces) - 1);
                QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType)
                self.resultLayerList.append(constructionLayer)
            else:
                constructionLayer = AcadHelper.createVectorLayer(baroVnavSurfaces[i].type, QGis.Polygon)
                baroVnavSurfaces[i].vmethod_2(constructionLayer);
                QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType)
                self.resultLayerList.append(constructionLayer)
        wptLayer = self.WPT2Layer()
        nominalTrackLayer = self.nominal2Layer()
        QgisHelper.appendToCanvas(define._canvas, [wptLayer, nominalTrackLayer], self.surfaceType)
        QgisHelper.zoomToLayers([constructionLayer, wptLayer, nominalTrackLayer])
        resultString = ""
        self.resultLayerList.extend([wptLayer, nominalTrackLayer])
        for cur in self.calculationResults:
            resultString += cur + "\n"
        # QMessageBox.warning(self, "Reports", resultString)

        self.ui.btnEvaluate.setEnabled(True)
    def nominal2Layer(self):
        resultLayer = AcadHelper.createVectorLayer("NominalTrack_" + self.surfaceType.replace(" ", "_"), QGis.Line)
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, PolylineArea([self.pointFAWP, self.pointMAHWP]))
        return resultLayer
    def WPT2Layer(self):
        resultLayer = AcadHelper.createVectorLayer("WPT_" + self.surfaceType.replace(" ", "_").replace("-", "_"), QGis.Point)
        i = 1
        while i < 4:
            if i == 1:
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.pointFAWP, False, {"Category":"FAWP"})
            elif i == 2:
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.pointMAHWP, False, {"Category":"MAHWP"})
            elif i == 3:
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, self.pointMAWP, False, {"Category":"MAPT"})
            i += 1
        '''FlyOver'''
        symbolFlyOver = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyOver.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyover.svg", 9.0, 0.0)#float(strRwyDir))
        symbolFlyOver.appendSymbolLayer(svgSymLayer)
        renderCatFlyOver = QgsRendererCategoryV2(1, symbolFlyOver,"FlyOver")

        '''FlyBy'''
        symbolFlyBy = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyBy.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyby.svg", 9.0, 0.0)#float(strRwyDir))
        symbolFlyBy.appendSymbolLayer(svgSymLayer)
        renderCatFlyBy = QgsRendererCategoryV2(0, symbolFlyBy,"FlyBy")

        symRenderer = QgsCategorizedSymbolRendererV2(Expressions.BARO_WPT_EXPRESION, [renderCatFlyOver, renderCatFlyBy])

        resultLayer.setRendererV2(symRenderer)
        return resultLayer
    # def locateCritical(self):
    #     if BaroVNAVDlg.resultCriticalObst == None or not BaroVNAVDlg.resultCriticalObst.Assigned:
    #         return
    #
    #     fId = BaroVNAVDlg.resultCriticalObst.Obstacle.featureId
    #     layerId = BaroVNAVDlg.resultCriticalObst.Obstacle.layerId
    #     layer = QgsMapLayerRegistry.instance().mapLayer (layerId)
    #     if not isinstance(layer, QgsRasterLayer):
    #         layer.select(fId)
    #     pt = QgsPoint(BaroVNAVDlg.resultCriticalObst.Obstacle.Position.x(), BaroVNAVDlg.resultCriticalObst.Obstacle.Position.y())
    #     define._canvas.zoomByFactor (0.2, pt)
    def cmbObstSurface_currentIndexChanged(self):
        if self.ui.cmbObstSurface.currentText() != BaroVnavSurfaceType.Z:
            eqMindex = self.obstaclesModel.IndexEqAltM
            eqFtindex = self.obstaclesModel.IndexEqAltFt
            self.ui.tblObstacles.hideColumn(eqMindex)
            self.ui.tblObstacles.hideColumn(eqFtindex)
        else:
            eqMindex = self.obstaclesModel.IndexEqAltM
            eqFtindex = self.obstaclesModel.IndexEqAltFt
            self.ui.tblObstacles.showColumn(eqMindex)
            self.ui.tblObstacles.showColumn(eqFtindex)

    def menuSetCriticalObstClick(self):
        BaroVNAVDlg.resultCriticalObst.Obstacle = self.changedCriticalObstacleValue["Obstacle"]
        BaroVNAVDlg.resultCriticalObst.surface = self.changedCriticalObstacleValue["SurfaceName"]
        BaroVNAVDlg.resultCriticalObst.Assigned = True
        BaroVNAVDlg.resultCriticalObst.eqAltitude = None
        ocaMValue = self.changedCriticalObstacleValue["OcaM"]

        BaroVNAVDlg.resultCriticalObst.oca = float(ocaMValue) if ocaMValue != "" else None

        self.setCriticalObstacle()

    def setCriticalObstacle(self):

        if BaroVNAVDlg.resultCriticalObst == None or not BaroVNAVDlg.resultCriticalObst.Assigned:
            return
        else:
            self.ui.txtCriticalID.setText(BaroVNAVDlg.resultCriticalObst.Obstacle.name)
            self.ui.txtCriticalX.setText(str(BaroVNAVDlg.resultCriticalObst.Obstacle.Position.x()))
            self.ui.txtCriticalY.setText(str(BaroVNAVDlg.resultCriticalObst.Obstacle.Position.y()))
            self.ui.txtCriticalAltitudeM.setText(str(round(BaroVNAVDlg.resultCriticalObst.Obstacle.Position.z(), 4)))
            self.ui.txtCriticalAltitudeFt.setText(str(round(Unit.ConvertMeterToFeet(BaroVNAVDlg.resultCriticalObst.Obstacle.Position.z()), 4)))
            self.ui.txtCriticalSurface.setText(BaroVNAVDlg.resultCriticalObst.surface)

            if self.ui.cmbUnits.currentIndex() == 1:# feet
                self.ui.txtOCAResults.setText(str(round(Unit.ConvertMeterToFeet(BaroVNAVDlg.resultCriticalObst.oca), 4)) + "ft")
                self.ui.txtOCHResults.setText(str(round(Unit.ConvertMeterToFeet(BaroVNAVDlg.resultCriticalObst.oca - self.parametersPanel.pnlThr.Altitude().Metres), 4)) + "ft")
            else:
                self.ui.txtOCAResults.setText(str(round(BaroVNAVDlg.resultCriticalObst.oca, 4)) + "m")
                self.ui.txtOCHResults.setText(str(round(BaroVNAVDlg.resultCriticalObst.oca - self.parametersPanel.pnlThr.Altitude().Metres, 4)) + "m")
    def trackRadialPanelSetEnabled(self):
        positionPanels = self.findChildren(PositionPanel)
        if len(positionPanels) > 0:
            flag = False
            for pnl in positionPanels:
                if pnl.IsValid():
                    flag = True
                    break
            self.parametersPanel.pnlRwyDir.Enabled = flag

    def initParametersPan(self):
        ui = Ui_BaroVNAV()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        BaroVNAVDlg.resultCriticalObst = BaroVnavCriticalObstacle()
        self.connect(self.parametersPanel.pnlEvalMethodMA, SIGNAL("Event_0"), self.pnlEvalMethodMA_Event_0)
        self.connect(self.parametersPanel.pnlMACG, SIGNAL("Event_0"), self.pnlMACG_Event_0)
        self.connect(self.parametersPanel.pnlMocMA, SIGNAL("Event_0"), self.pnlMocMA_Event_0)
        self.connect(self.parametersPanel.pnlTerminationDist, SIGNAL("Event_0"), self.pnlTerminationDist_Event_0)
        self.connect(self.parametersPanel.pnlMAPtDist, SIGNAL("Event_0"), self.pnlMAPtDist_Event_0)

        self.connect(self.parametersPanel.cmbMAPt, SIGNAL("Event_0"), self.cmbMAPt_Event_0)
        self.connect(self.parametersPanel.pnlTC, SIGNAL("Event_0"), self.pnlTC_Event_0)
        self.connect(self.parametersPanel.pnlHL, SIGNAL("Event_0"), self.pnlHL_Event_0)
        self.connect(self.parametersPanel.pnlIasAtThr, SIGNAL("Event_0"), self.pnlIasAtThr_Event_0)
        self.connect(self.parametersPanel.pnlIas, SIGNAL("Event_0"), self.pnlIas_Event_0)
        self.connect(self.parametersPanel.pnlAcCat, SIGNAL("Event_0"), self.pnlAcCat_Event_0)
        self.connect(self.parametersPanel.pnlThrFafDist, SIGNAL("Event_0"), self.pnlThrFafDist_Event_0)
        self.connect(self.parametersPanel.pnlVPA, SIGNAL("Event_0"), self.pnlVPA_Event_0)
        self.connect(self.parametersPanel.pnlRDH, SIGNAL("Event_0"), self.pnlRDH_Event_0)
        self.connect(self.parametersPanel.pnlOCAH, SIGNAL("Event_0"), self.pnlOCAH_Event_0)
        self.connect(self.parametersPanel.pnlRwyDir, SIGNAL("Event_0"), self.pnlRwyDir_Event_0)
        self.connect(self.parametersPanel.pnlThr, SIGNAL("positionChanged"), self.pnlThr_Event_0)
        self.connect(self.parametersPanel.pnlArp, SIGNAL("positionChanged"), self.pnlArp_Event_0)
        self.connect(self.parametersPanel.pnlMinTemp, SIGNAL("Event_0"), self.pnlMinTemp_Event_0)



        self.ui.cmbUnits.currentIndexChanged.connect(self.setCriticalObstacle)
        # self.ui.btnCriticalLocate.clicked.connect(self.locateCritical)

        self.ui.cmbObstSurface.currentIndexChanged.connect(self.cmbObstSurface_currentIndexChanged)
        items = []
        for i in range(25, 71):
            num = float(i) / 10;
            items.append(QString(str(num)) + define._degreeStr)
        self.parametersPanel.pnlVPA.Items = items
        self.parametersPanel.pnlVPA.SelectedIndex = 5

        self.parametersPanel.pnlAcCat.Items = ["A", "B", "C", "D", "E", "Custom"]
        self.parametersPanel.pnlAcCat.SelectedIndex = 3
        self.parametersPanel.cmbTermination.Items = ["THR", "PastTHR"]
        self.parametersPanel.cmbTermination.SelectedIndex = 1
        self.parametersPanel.cmbMAPt.Items = ["THR", "BeforeTHR"]
        self.parametersPanel.pnlEvalMethodMA.Items = ["Standard", "Alternative"]
        self.parametersPanel.pnlConstructionType.Items = ["2D", "3D"]


        self.connect(self.parametersPanel.cmbTermination, SIGNAL("Event_0"), self.cmbTermination_Event_0)
        self.trackRadialPanelSetEnabled()

    def pnlMinTemp_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlMinTemp)
    def pnlArp_Event_0(self):
        # try:
        #     point3dArp = self.parametersPanel.pnlArp.Point3d
        #     point3dThr = self.parametersPanel.pnlThr.Point3d
        #     self.parametersPanel.pnlRwyDir.Value = round(Unit.ConvertRadToDeg(MathHelper.getBearing(point3dArp, point3dThr)), 4)
        # except:
        #     pass
        self.trackRadialPanelSetEnabled()
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlArp)
    def pnlThr_Event_0(self):
        # try:
        #     point3dArp = self.parametersPanel.pnlArp.Point3d
        #     point3dThr = self.parametersPanel.pnlThr.Point3d
        #     self.parametersPanel.pnlRwyDir.Value = round(Unit.ConvertRadToDeg(MathHelper.getBearing(point3dArp, point3dThr)), 4)
        # except:
        #     pass
        self.trackRadialPanelSetEnabled()
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlThr)
    def pnlRwyDir_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlRwyDir)
    def pnlOCAH_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlOCAH)
    def pnlRDH_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlRDH)
    def pnlVPA_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlVPA)
    def pnlThrFafDist_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlThrFafDist)
    def pnlAcCat_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlAcCat)
    def pnlIas_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlIas)
    def pnlIasAtThr_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlIasAtThr)
    def pnlHL_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlHL)
    def pnlTC_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlTC)
    def cmbMAPt_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.cmbMAPt)
    def cmbTermination_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.cmbTermination)
    def pnlMAPtDist_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlMAPtDist)
    def pnlTerminationDist_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlTerminationDist)
    def pnlMocMA_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlMocMA)
    def pnlMACG_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlMACG)
    def pnlEvalMethodMA_Event_0(self):
        self.cmbMAPt_SelectedIndexChanged(self.parametersPanel.pnlEvalMethodMA)
    def cmbMAPt_SelectedIndexChanged(self, sender):
        # Control control = sender as Control;
        self.method_34();
        self.method_31();
        if (sender == None):
            return;
        if (sender == self.parametersPanel.pnlIas):
            self.customIas = self.parametersPanel.pnlIas.Value;
        if (sender == self.parametersPanel.pnlMAPtDist):
            if self.parametersPanel.pnlMAPtDist.Enabled:
                self.maptDist = self.parametersPanel.pnlMAPtDist.Value;
        if (sender == self.parametersPanel.pnlTerminationDist):
            if self.parametersPanel.pnlTerminationDist.Enabled:
                self.segmentTerminationDist = self.parametersPanel.pnlTerminationDist.Value;
        if (sender == self.parametersPanel.pnlAcCat):
            self.method_35();
        if (sender == self.parametersPanel.cmbTermination):
            # if (!control.Focused)
            #     return;
            self.method_36();
        if (sender == self.parametersPanel.cmbMAPt):
            # if (!control.Focused)
            #     return;
            self.method_37();
        if (sender == self.parametersPanel.pnlAcCat or sender == self.parametersPanel.pnlIasAtThr or sender == self.parametersPanel.pnlArp or sender == self.parametersPanel.pnlVPA):
            self.method_40();
        if (sender == self.parametersPanel.pnlOCAH or sender == self.parametersPanel.pnlArp or sender == self.parametersPanel.pnlThr or sender == self.parametersPanel.pnlMinTemp):
            self.method_41();

    def method_31(self):
        BaroVNAVDlg.obstacles = []
        BaroVNAVDlg.obstaclesChecked = 0;
        # self.ui.grbMostCritical.setVisible(False)
        BaroVNAVDlg.resultCriticalObst.method_1();
        BaroVNAVDlg.resultOCH = None
        BaroVNAVDlg.resultOCA = None
        BaroVNAVDlg.calculationResults = []
    def method_34(self):
        self.parametersPanel.pnlIas.ReadOnly = self.parametersPanel.pnlAcCat.SelectedIndex == len(self.parametersPanel.pnlAcCat.Items) - 1;
        self.parametersPanel.pnlIasAtThr.ReadOnly = self.parametersPanel.pnlAcCat.SelectedIndex == len(self.parametersPanel.pnlAcCat.Items) - 1;
        self.parametersPanel.pnlTerminationDist.Enabled = self.parametersPanel.cmbTermination.SelectedIndex == 1;
        self.parametersPanel.pnlMAPtDist.Enabled = self.parametersPanel.cmbMAPt.SelectedIndex == 1;
        self.parametersPanel.lblAbove35.setVisible(self.parametersPanel.pnlVPA.SelectedIndex > 10);

    def method_35(self):
        if self.parametersPanel.pnlAcCat.SelectedIndex == AircraftSpeedCategory.A:
            self.parametersPanel.pnlIas.Value = Speed(100);
            self.parametersPanel.pnlIasAtThr.Value = Speed(90);
        elif self.parametersPanel.pnlAcCat.SelectedIndex == AircraftSpeedCategory.B:
            self.parametersPanel.pnlIas.Value = Speed(130);
            self.parametersPanel.pnlIasAtThr.Value = Speed(120);
        elif self.parametersPanel.pnlAcCat.SelectedIndex == AircraftSpeedCategory.C:
            self.parametersPanel.pnlIas.Value = Speed(160);
            self.parametersPanel.pnlIasAtThr.Value = Speed(140);
        elif self.parametersPanel.pnlAcCat.SelectedIndex == AircraftSpeedCategory.D:
            self.parametersPanel.pnlIas.Value = Speed(185);
            self.parametersPanel.pnlIasAtThr.Value = Speed(165);
        elif self.parametersPanel.pnlAcCat.SelectedIndex == AircraftSpeedCategory.E:
            self.parametersPanel.pnlIas.Value = Speed(230);
            self.parametersPanel.pnlIasAtThr.Value = Speed(210);
        elif self.parametersPanel.pnlAcCat.SelectedIndex == AircraftSpeedCategory.Custom - 1:
            self.parametersPanel.pnlIas.Value = self.customIas;
            self.parametersPanel.pnlIasAtThr.Value = self.customIasAtThr;
    def method_36(self):
        if (self.parametersPanel.cmbTermination.SelectedIndex != 1):
            self.parametersPanel.pnlTerminationDist.Value = Distance(0.0);
            return;
        self.parametersPanel.pnlTerminationDist.Value = self.segmentTerminationDist;
    def method_37(self):
        if ( self.parametersPanel.cmbMAPt.SelectedIndex != 1):
            self.parametersPanel.pnlMAPtDist.Value = Distance(0.0);
            return;
        self.parametersPanel.pnlMAPtDist.Value =  self.maptDist;
    def method_38(self):
        return self.parametersPanel.pnlAcCat.Value
    def method_39(self):
        num = 2.5;
        for i in range(0, self.parametersPanel.pnlVPA.SelectedIndex):
            num = num + 0.1;
        return num    #math.Round(num, 1);
    def method_40(self):
        try:
            num =  self.method_39();
            num1 =  self.parametersPanel.pnlArp.Altitude().Metres
            num2 =  self.parametersPanel.pnlIasAtThr.Value.Knots
            num3 = round(0.125 * num2 + 28.3);
            num4 = round(0.177 * num2 - 3.2);
            num5 = 0;
            if (num1 > 900):
                num5 = num5 + num4 * 0.02 * (num1 / 300);
            if (num > 3.2):
                num5 = num5 + num4 * 0.05 * ((num - 3.2) / 0.1);
            num5 = MathHelper.smethod_0(num5, 0);
            self.parametersPanel.pnlHL.Value = Altitude(num3 + num5);
        except:
             self.parametersPanel.pnlHL.Value = Altitude(0.0);
    def method_41(self):
        try:
            altitude = self.parametersPanel.pnlArp.Altitude();
            num = self.parametersPanel.pnlMinTemp.Value
            altitude1 = self.parametersPanel.pnlOCAH.method_3(self.parametersPanel.pnlArp.Altitude());
            self.parametersPanel.pnlTC.Value = TempCorrection.smethod_2(altitude1, altitude, self.parametersPanel.pnlArp.Altitude(), num);
        except:
            self.parametersPanel.pnlTC.Value = Altitude(0.0);

    def method_51(self):
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
        point3d4 = self.parametersPanel.pnlArp.Point3d;
        value = self.parametersPanel.pnlMinTemp.Value;
        point3d5 = self.parametersPanel.pnlThr.Point3d;
        num = Unit.ConvertDegToRad(self.parametersPanel.pnlRwyDir.Value);
        num1 = MathHelper.smethod_4(num - 1.5707963267949);
        num2 = MathHelper.smethod_4(num + 1.5707963267949);
        num3 = MathHelper.smethod_4(num + 3.14159265358979);
        num4 = Unit.ConvertDegToRad(15);
        num5 = Unit.ConvertDegToRad(30);
        altitude = self.parametersPanel.pnlOCAH.method_2(self.parametersPanel.pnlThr.Altitude);
        metres = altitude.Metres;
        altitude = self.parametersPanel.pnlOCAH.method_3(self.parametersPanel.pnlThr.Altitude());
        metres1 = altitude.Metres;
        metres2 = self.parametersPanel.pnlRDH.Value.Metres;
        num6 = self.method_39();
        num7 = math.tan(Unit.ConvertDegToRad(num6));
        num8 = math.sin(Unit.ConvertDegToRad(num6));
        metres3 = self.parametersPanel.pnlMocI.Value.Metres;
        metres4 = self.parametersPanel.pnlMocMA.Value.Metres;
        angleGradientSlope = self.parametersPanel.pnlMACG.Value;
        percent = angleGradientSlope / 100;
        rnavGnssTolerance = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Star30Sid30IfIafMa30, AircraftSpeedCategory.D);
        rnavGnssTolerance1 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Faf, AircraftSpeedCategory.D);
        rnavGnssTolerance2 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Mapt, AircraftSpeedCategory.D);
        rnavGnssTolerance3 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Ma15, AircraftSpeedCategory.D);
        rnavGnssTolerance4 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Star30Sid30IfIafMa30, AircraftSpeedCategory.D);
        metres5 = rnavGnssTolerance.ATT.Metres;
        metres6 = rnavGnssTolerance.ASW.Metres;
        metres7 = rnavGnssTolerance1.ATT.Metres;
        metres8 = rnavGnssTolerance1.ASW.Metres;
        metres9 = rnavGnssTolerance2.ATT.Metres;
        num9 = rnavGnssTolerance2.ASW.Metres;
        metres10 = rnavGnssTolerance3.ATT.Metres;
        num10 = rnavGnssTolerance3.ASW.Metres;
        metres11 = rnavGnssTolerance4.ATT.Metres;
        num11 = rnavGnssTolerance4.ASW.Metres;
        distance = self.parametersPanel.pnlThrFafDist.Value;
        point3d6 = MathHelper.distanceBearingPoint(point3d5, num3, distance.Metres);
        self.pointFAWP = point3d6
        distance = self.parametersPanel.pnlMAPtDist.Value;
        point3d7 = MathHelper.distanceBearingPoint(point3d5, num3, distance.Metres);
        self.pointMAWP = point3d7
        distance = self.parametersPanel.pnlTerminationDist.Value;
        point3d8 = MathHelper.distanceBearingPoint(point3d5, num, distance.Metres);
        self.pointMAHWP = point3d8
        if (point3d5.get_Z() < Unit.ConvertFeetToMeter(5000)):
            if (metres1 <= 75):
                QMessageBox.warning(self, "Warning", Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM);
                return None, None
        elif (point3d5.get_Z() <= Unit.ConvertFeetToMeter(10000)):
            if (metres1 <= 105):
                QMessageBox.warning(self, "Warning", Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM);
                return None, None
        elif (metres1 <= 120):
            QMessageBox.warning(self, "Warning", Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM);
            return None, None
        num12 = (metres1 - metres2) / num7;
        metres12 = self.parametersPanel.pnlTC.Value.Metres;
        num13 = Unit.smethod_1(math.atan((metres1 - metres2 - metres12) / num12));
        baroVnavFasSegments = [];
        baroVnavFasSegment = BaroVnavFasSegment()
        baroVnavFasSegment.moc = 75
        baroVnavFasSegment.tanafas = (metres1 - metres12 - baroVnavFasSegment.moc) * num7 / (metres1 - baroVnavFasSegment.moc)
        baroVnavFasSegment.xfas = (baroVnavFasSegment.moc - metres2) / num7 + metres7
        baroVnavFasSegment.xstart = baroVnavFasSegment.xfas
        baroVnavFasSegment.xend = baroVnavFasSegment.xfas + (Unit.ConvertFeetToMeter(5000) - point3d5.get_Z()) / baroVnavFasSegment.tanafas
        baroVnavFasSegment.ptStart = MathHelper.distanceBearingPoint(point3d5, num3, baroVnavFasSegment.xstart)
        baroVnavFasSegment.ptEnd = MathHelper.distanceBearingPoint(point3d5, num3, baroVnavFasSegment.xend)
        baroVnavFasSegments.append(baroVnavFasSegment);
        baroVnavFasSegment = BaroVnavFasSegment()
        baroVnavFasSegment.moc = 105
        baroVnavFasSegment.tanafas = (metres1 - metres12 - baroVnavFasSegment.moc) * num7 / (metres1 - baroVnavFasSegment.moc)
        baroVnavFasSegment.xfas = (baroVnavFasSegment.moc - metres2) / num7 + metres7
        baroVnavFasSegment.xstart = baroVnavFasSegment.xfas + (Unit.ConvertFeetToMeter(5000) - point3d5.get_Z()) / baroVnavFasSegment.tanafas
        baroVnavFasSegment.xend = baroVnavFasSegment.xfas + (Unit.ConvertFeetToMeter(10000) - point3d5.get_Z()) / baroVnavFasSegment.tanafas
        baroVnavFasSegment.ptStart = MathHelper.distanceBearingPoint(point3d5, num3, baroVnavFasSegment.xstart)
        baroVnavFasSegment.ptEnd = MathHelper.distanceBearingPoint(point3d5, num3, baroVnavFasSegment.xend)
        baroVnavFasSegments.append(baroVnavFasSegment);
        baroVnavFasSegment = BaroVnavFasSegment()
        baroVnavFasSegment.moc = 120
        baroVnavFasSegment.tanafas = (metres1 - metres12 - baroVnavFasSegment.moc) * num7 / (metres1 - baroVnavFasSegment.moc)
        baroVnavFasSegment.xfas = (baroVnavFasSegment.moc - metres2) / num7 + metres7
        baroVnavFasSegment.xstart = baroVnavFasSegment.xfas + (Unit.ConvertFeetToMeter(10000) - point3d5.get_Z()) / baroVnavFasSegment.tanafas
        baroVnavFasSegment.xend = baroVnavFasSegment.xfas + (metres1 - metres3) / baroVnavFasSegment.tanafas
        baroVnavFasSegment.ptStart = MathHelper.distanceBearingPoint(point3d5, num3, baroVnavFasSegment.xstart)
        baroVnavFasSegment.ptEnd = MathHelper.distanceBearingPoint(point3d5, num3, baroVnavFasSegment.xend)
        baroVnavFasSegments.append(baroVnavFasSegment);
        if (point3d5.get_Z() >= Unit.ConvertFeetToMeter(5000)):
            baroVnavFasSegments.pop(0);
            baroVnavFasSegments[0].xstart = baroVnavFasSegments[0].xfas;
            baroVnavFasSegments[0].ptStart = MathHelper.distanceBearingPoint(point3d5, num3, baroVnavFasSegments[0].xstart);
        if (point3d5.get_Z() >= Unit.ConvertFeetToMeter(10000)):
            baroVnavFasSegments.pop(0);
            baroVnavFasSegments[0].xstart = baroVnavFasSegments[0].xfas;
            baroVnavFasSegments[0].ptStart = MathHelper.distanceBearingPoint(point3d5, num3, baroVnavFasSegments[0].xstart);
        if (metres - metres3 <= Unit.ConvertFeetToMeter(10000)):
            baroVnavFasSegments.pop(len(baroVnavFasSegments) - 1);
            baroVnavFasSegments[len(baroVnavFasSegments) - 1].xend = baroVnavFasSegments[len(baroVnavFasSegments) - 1].xfas + (metres1 - metres3) / baroVnavFasSegments[len(baroVnavFasSegments) - 1].tanafas;
            baroVnavFasSegments[len(baroVnavFasSegments) - 1].ptEnd = MathHelper.distanceBearingPoint(point3d5, num3, baroVnavFasSegments[len(baroVnavFasSegments) - 1].xend);
        if (metres - metres3 <= Unit.ConvertFeetToMeter(5000)):
            baroVnavFasSegments.pop(len(baroVnavFasSegments) - 1);
            baroVnavFasSegments[len(baroVnavFasSegments) - 1].xend = baroVnavFasSegments[len(baroVnavFasSegments) - 1].xfas + (metres1 - metres3) / baroVnavFasSegments[len(baroVnavFasSegments) - 1].tanafas;
            baroVnavFasSegments[len(baroVnavFasSegments) - 1].ptEnd = MathHelper.distanceBearingPoint(point3d5, num3, baroVnavFasSegments[len(baroVnavFasSegments) - 1].xend);

        speed = Speed.smethod_0(self.parametersPanel.pnlIas.Value, 15, Altitude(point3d4.get_Z()));
        metresPerSecond = speed.MetresPerSecond;
        metres13 = self.parametersPanel.pnlHL.Value.Metres;
        result = self.method_38();
        if result == AircraftSpeedCategory.A or result == AircraftSpeedCategory.B:
            double_0 = -900;
        elif result == AircraftSpeedCategory.C:
            double_0 = -1100;
        else:
            double_0 = -1400;
        num14 = (metres13 - metres2) / num7;
        num15 = 2 * metresPerSecond * num8 / 0.784;
        speed = Speed(10, SpeedUnits.KTS);
        metresPerSecond1 = num14 - (metres9 + num15 * (metresPerSecond + speed.MetresPerSecond));
        if (num6 > 3.2 or point3d4.get_Z() > 900):
            double_0 = min([double_0, metresPerSecond1]);
        if (num13 < 2.5):
            QMessageBox.warning(self, "Warning", Messages.ERR_BAROVNAV_MIN_VPA%(str(num13)))
            return None, None
            # throw new Exception(string.Format(Messages.ERR_BAROVNAV_MIN_VPA, num13.ToString("0.0#")));

        num16 = Unit.ConvertNMToMeter(15);
        num17 = Unit.ConvertNMToMeter(30);
        if (MathHelper.calcDistance(point3d4, point3d5) > (Distance(10, DistanceUnits.NM)).Metres):
            QMessageBox.warning(self, "Warning", Messages.ERR_DISTANCE_BETWEEN_X_AND_ARP_EXCEEDS_10_NM%("THR"))
            return None, None
            # throw new Exception(string.Format(Messages.ERR_DISTANCE_BETWEEN_X_AND_ARP_EXCEEDS_10_NM, Captions.THR_BIG));

        if (MathHelper.calcDistance(point3d4, point3d8) > num17):
            QMessageBox.warning(self, "Warning", Messages.ERR_BAROVNAV_APV_ARP_DISTANCE)
            return None, None
        num18 = (metres8 - num9) / math.tan(num5) + 500;
        if (MathHelper.calcDistance(point3d5, point3d7) > MathHelper.calcDistance(point3d5, point3d6)):
            QMessageBox.warning(self, "Warning", Messages.ERR_BAROVNAV_THR_FAWP_MAWP_DISTANCE)
            return None, None
        if (MathHelper.calcDistance(point3d7, point3d6) < num18):
            QMessageBox.warning(self, "Warning", Messages.ERR_INSUFFICIENT_FINAL_APPROACH_SEGMENT_LENGTH)
            return None, None
        point3d0_1 = []
        MathHelper.smethod_34(point3d7, MathHelper.distanceBearingPoint(point3d7, num, 1000), point3d4, num16, point3d0_1);
        point3d = point3d0_1[0]
        point3d1 = point3d0_1[1]
        point3d2 = point3d1 if(not MathHelper.smethod_135(num, MathHelper.getBearing(point3d7, point3d), Unit.ConvertDegToRad(5), AngleUnits.Radians)) else point3d;
        point3d0_1 = []
        MathHelper.smethod_34(point3d7, MathHelper.distanceBearingPoint(point3d7, num, 1000), point3d4, num17, point3d0_1);
        point3d = point3d0_1[0]
        point3d1 = point3d0_1[1]
        point3d3 = point3d1 if(not MathHelper.smethod_135(num, MathHelper.getBearing(point3d7, point3d), Unit.ConvertDegToRad(5), AngleUnits.Radians)) else point3d;
        point3d9 = MathHelper.distanceBearingPoint(point3d6, num1, metres8);
        MathHelper.distanceBearingPoint(point3d6, num1, metres8 / 2);
        point3d10 = MathHelper.distanceBearingPoint(point3d6, num2, metres8);
        MathHelper.distanceBearingPoint(point3d6, num2, metres8 / 2);
        point3d11 = MathHelper.distanceBearingPoint(point3d9, num3 + num5, (metres6 - metres8) / math.sin(num5));
        point3d12 = MathHelper.distanceBearingPoint(point3d11, num2, metres6 / 2);
        point3d13 = MathHelper.distanceBearingPoint(point3d10, num3 - num5, (metres6 - metres8) / math.sin(num5));
        point3d14 = MathHelper.distanceBearingPoint(point3d13, num1, metres6 / 2);
        point3d15 = MathHelper.distanceBearingPoint(point3d11, num3, 5000);
        point3d16 = MathHelper.distanceBearingPoint(point3d12, num3, 5000);
        point3d17 = MathHelper.distanceBearingPoint(point3d13, num3, 5000);
        point3d18 = MathHelper.distanceBearingPoint(point3d14, num3, 5000);
        point3d19 = MathHelper.distanceBearingPoint(point3d9, num + num5, (metres8 - num9) / math.sin(num5));
        point3d20 = MathHelper.distanceBearingPoint(point3d19, num2, num9 / 2);
        point3d21 = MathHelper.distanceBearingPoint(point3d10, num - num5, (metres8 - num9) / math.sin(num5));
        point3d22 = MathHelper.distanceBearingPoint(point3d21, num1, num9 / 2);
        point3d23 = MathHelper.distanceBearingPoint(point3d7, num3, metres9);
        point3d24 = MathHelper.distanceBearingPoint(point3d23, num1, num9);
        point3d25 = MathHelper.distanceBearingPoint(point3d23, num1, num9 / 2);
        point3d26 = MathHelper.distanceBearingPoint(point3d23, num2, num9);
        point3d27 = MathHelper.distanceBearingPoint(point3d23, num2, num9 / 2);
        point3d28 = MathHelper.distanceBearingPoint(point3d24, num - num4, (num10 - num9) / math.sin(num4));
        point3d29 = MathHelper.distanceBearingPoint(point3d28, num2, num10 / 2);
        point3d30 = MathHelper.distanceBearingPoint(point3d26, num + num4, (num10 - num9) / math.sin(num4));
        point3d31 = MathHelper.distanceBearingPoint(point3d30, num1, num10 / 2);
        point3d23 = MathHelper.distanceBearingPoint(point3d2, num3, metres10);
        point3d32 = MathHelper.distanceBearingPoint(point3d23, num1, num10);
        point3d33 = MathHelper.distanceBearingPoint(point3d23, num1, num10 / 2);
        point3d34 = MathHelper.distanceBearingPoint(point3d23, num2, num10);
        point3d35 = MathHelper.distanceBearingPoint(point3d23, num2, num10 / 2);
        point3d36 = MathHelper.distanceBearingPoint(point3d32, num - num4, (num11 - num10) / math.sin(num4));
        point3d37 = MathHelper.distanceBearingPoint(point3d36, num2, num11 / 2);
        point3d38 = MathHelper.distanceBearingPoint(point3d34, num + num4, (num11 - num10) / math.sin(num4));
        point3d39 = MathHelper.distanceBearingPoint(point3d38, num1, num11 / 2);
        point3d23 = MathHelper.distanceBearingPoint(point3d3, num3, metres11);
        point3d40 = MathHelper.distanceBearingPoint(point3d23, num1, num11);
        point3d41 = MathHelper.distanceBearingPoint(point3d23, num1, num11 / 2);
        point3d42 = MathHelper.distanceBearingPoint(point3d23, num2, num11);
        point3d43 = MathHelper.distanceBearingPoint(point3d23, num2, num11 / 2);
        point3dArray = [point3d15, point3d11, point3d19, point3d24, point3d28, point3d32, point3d36, point3d40];
        point3dCollection = Point3dCollection(point3dArray);
        point3dArray = [point3d16, point3d12, point3d20, point3d25, point3d29, point3d33, point3d37, point3d41];
        point3dCollection1 = Point3dCollection(point3dArray);
        point3dArray = [point3d18, point3d14, point3d22, point3d27, point3d31, point3d35, point3d39, point3d43 ];
        point3dCollection2 = Point3dCollection(point3dArray);
        point3dArray = [point3d17, point3d13, point3d21, point3d26, point3d30, point3d34, point3d38, point3d42 ];
        point3dCollection3 = Point3dCollection(point3dArray);
        baroVnavSurfaces = [];
        distance = self.parametersPanel.pnlTerminationDist.Value;
        num19 = -distance.Metres;
        baroVnavSurfaceFA = BaroVnavSurfaceFAS(point3d5, num, num12, metres3, baroVnavFasSegments);
        if (num12 > baroVnavFasSegments[len(baroVnavFasSegments) - 1].xend):
            baroVnavSurfaceFA.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, MathHelper.distanceBearingPoint(point3d5, num3, num12), baroVnavFasSegments[len(baroVnavFasSegments) - 1].ptEnd);

        for i in range(len(baroVnavFasSegments)):
            baroVnavSurfaceFA.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, baroVnavFasSegments[len(baroVnavFasSegments) - 1 - i].ptEnd, baroVnavFasSegments[len(baroVnavFasSegments) - 1 - i].ptStart);

        baroVnavSurfaces.append(baroVnavSurfaceFA);
        baroVnavSurfaceH = BaroVnavSurfaceH(point3d5, num, double_0, baroVnavFasSegments[0].xfas, baroVnavFasSegments[0].moc, metres4, metres9);
        if (double_0 >= num19):
            baroVnavSurfaceH.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, MathHelper.distanceBearingPoint(point3d5, num3, baroVnavFasSegments[0].xfas), MathHelper.distanceBearingPoint(point3d5, num3, double_0));
        else:
            baroVnavSurfaceH.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, MathHelper.distanceBearingPoint(point3d5, num3, baroVnavFasSegments[0].xfas), point3d8);
        baroVnavSurfaces.append(baroVnavSurfaceH);
        if (double_0 > num19):
            baroVnavSurfaceZ = BaroVnavSurfaceZ(point3d5, num, double_0, metres4, percent);
            baroVnavSurfaceZ.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, MathHelper.distanceBearingPoint(point3d5, num3, double_0), point3d8);
            baroVnavSurfaces.append(baroVnavSurfaceZ);
        BaroVNAVDlg.calculationResults = [];
        strs = BaroVNAVDlg.calculationResults;
        distance = Distance(num12);
        strs.append("%s\t%s"%("X FAP", str(round(distance.NauticalMiles, 4)) + "nm"));
        strs1 = BaroVNAVDlg.calculationResults;
        tEMPERATURECORRECTION = Captions.TEMPERATURE_CORRECTION;
        distance = Distance(metres12);
        strs1.append("%s\t%s"%(tEMPERATURECORRECTION, str(round(distance.NauticalMiles, 4)) + "nm"))
        strs2 = BaroVNAVDlg.calculationResults;
        mINIMUMVPA = Captions.MINIMUM_VPA;
        angleGradientSlope = num13;
        strs2.append("%s\t%s"%(mINIMUMVPA, str(angleGradientSlope)));
        for j in range(len(baroVnavFasSegments)):
            altitude1 = Altitude(baroVnavFasSegments[j].moc);
            strs3 = BaroVNAVDlg.calculationResults;
            strS = str(round(altitude1.Metres, 4)) + "m";
            distance = Distance(baroVnavFasSegments[j].xfas);
            strs3.append("%s [%s]\t%s"%("X FAS", strS, str(round(distance.NauticalMiles, 4)) + "nm"))
            strs4 = BaroVNAVDlg.calculationResults;
            fASANGLE = Captions.FAS_ANGLE;
            str1 = str(round(altitude1.Metres, 4)) + "m";
            angleGradientSlope = Unit.smethod_1(math.atan(baroVnavFasSegments[j].tanafas));
            strs4.append("%s [%s]\t%s"%(fASANGLE, str1, str(angleGradientSlope)));
        strs5 = BaroVNAVDlg.calculationResults;
        distance = Distance(double_0);
        strs5.append("%s\t%s"%("Xz", str(round(distance.NauticalMiles, 4)) + "nm"))

        self.calculationResults = []
        heightFAP = self.parametersPanel.pnlOCAH.Value.Metres - self.parametersPanel.pnlThr.Altitude().Metres
        RDH = self.parametersPanel.pnlRDH.Value.Metres
        num6 = self.GetVPAValue();
        tanVPA = math.tan(Unit.ConvertDegToRad(num6));
        num12 = (heightFAP - RDH) / tanVPA;
        self.calculationResults.append("X FAP:\t" + str(num12) + " m")

        tempCorrection = self.parametersPanel.pnlTC.Value.Metres
        self.calculationResults.append("Temperature Correction:\t" + str(round(tempCorrection, 4)) + " m")
        self.calculationResults.append("Temperature Correction:\t" + str(round(Unit.ConvertMeterToFeet(tempCorrection), 4)) + " ft")

        num14 = Unit.smethod_1(math.atan((heightFAP - RDH - tempCorrection) / num12));
        self.calculationResults.append(unicode("Minimum VPA:\t" + str(num14) + "°", "utf-8"))
        for current in baroVnavFasSegments:
            self.calculationResults.append("X FAS [" + str(current.moc) + "]:\t" + str(current.xfas) + " m")
            self.calculationResults.append(unicode("FAS Angle [" + str(current.moc) + "]:\t" + str(Unit.ConvertRadToDeg(math.atan(current.tanafas))) + "°", "utf-8"))
        self.calculationResults.append("Xz:\t" + str(round(double_0)) + " m")
        return baroVnavSurfaces, double_0;
    def GetVPAValue(self):
        i = 0
        num = 2.5
        while i < self.parametersPanel.pnlVPA.SelectedIndex:
            num = num + 0.1
            i += 1

        return round(num, 1)
class BaroVnavMaEvaluationMethod:
        Standard = 0#"Standard"
        Alternative = 1#"Alternative"
class BaroVnavMapt:
    THR = 0#"THR"
    BeforeTHR = 1#"BeforeTHR"
class BaroVnavSegmentTermination:
    THR = 0#"THR"
    PastTHR = 1#"PastTHR"

class BaroVnavCriticalObstacle:
    def __init__(self):
        self.obstacle = None;
        self.eqAltitude = None;
        self.surface = None;
        self.oca = None;
        self.assigned = False;
        
    def method_0(self, obstacle_0, double_0, double_1, baroVnavSurfaceType_0):
        if (self.assigned and double_1 <= self.oca):
            return;
        self.obstacle = obstacle_0;
        self.eqAltitude = double_0;
        self.surface = baroVnavSurfaceType_0;
        self.assigned = True;
        self.oca = double_1;
        
    def method_1(self):
        self.assigned = False;

    def method_2(self, point3d_0):
        if (self.assigned):
            return Altitude(MathHelper.smethod_0(self.oca, 1));
        return Altitude(MathHelper.smethod_0(point3d_0.get_Z() + 75, 1));
    
    def method_3(self, point3d_0):
        if (not self.assigned):
            return Altitude(MathHelper.smethod_0(75, 1));
        return Altitude(MathHelper.smethod_0(self.oca - point3d_0.get_Z(), 1));

    def get_Assigned(self):
        return self.assigned
    Assigned = property(get_Assigned, None, None, None)

    def get_Obstacle(self):
        return self.obstacle
    Obstacle = property(get_Obstacle, None, None, None)

    def get_Position(self):
        name = self.obstacle.Name;
        x = self.obstacle.Position.get_X();
        y = self.obstacle.Position.get_Y();
        position = self.obstacle.Position;
        return position
    Position = property(get_Position, None, None, None)


class BaroVnavFasSegment:
    def __init__(self):
        self.ptStart = None;
        self.ptEnd = None;
        self.moc = None;
        self.tanafas = None;
        self.xfas = None;
        self.xstart = None;
        self.xend = None;

class BaroVnavSurfaceType:
    FAS = "FAS"
    H = "H"
    Z = "Z"


class IBaroVnavSurface:
    def __init__(self):
        self.type = None;
        self.selectionArea = None;
        self.primaryArea = None;
        self.secondaryAreas = [];
        self.linesl = Point3dCollection();
        self.linepl = Point3dCollection();
        self.linepr = Point3dCollection();
        self.linesr = Point3dCollection();
        self.ptTHR = None;
        self.ptTHRm90 = None;
        self.ptEND = None;
        self.tr = None
        self.tr180 = None
        self.trp90 = None
        self.trm90 = None;
        
    def method_0(self, point3dCollection_0, point3dCollection_1, point3dCollection_2, point3dCollection_3, point3d_0, point3d_1):
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        point3d3 = None;
        flag = False;
        flag1 = False;
        count = len(point3dCollection_0);
        num = 0;
        while (True):
            if (num < count):
                num1 = num - 1;
                num2 = num;
                if (num1 < 0):
                    num1 = num;
                    num2 = num + 1;
                if (not flag and MathHelper.smethod_117(point3d_0, point3dCollection_3.get_Item(num), point3dCollection_0.get_Item(num), False)):
                    point3d4 = MathHelper.distanceBearingPoint(point3d_0, self.trm90, 100);
                    point3d = MathHelper.getIntersectionPoint(point3dCollection_0.get_Item(num1), point3dCollection_0.get_Item(num2), point3d_0, point3d4);
                    point3d1 = MathHelper.getIntersectionPoint(point3dCollection_1.get_Item(num1), point3dCollection_1.get_Item(num2), point3d_0, point3d4);
                    point3d2 = MathHelper.getIntersectionPoint(point3dCollection_2.get_Item(num1), point3dCollection_2.get_Item(num2), point3d_0, point3d4);
                    point3d3 = MathHelper.getIntersectionPoint(point3dCollection_3.get_Item(num1), point3dCollection_3.get_Item(num2), point3d_0, point3d4);
                    self.linesl.Add(point3d.smethod_167(self.vmethod_3(point3d, True)));
                    self.linepl.Add(point3d1.smethod_167(self.vmethod_3(point3d1, False)));
                    self.linepr.Add(point3d2.smethod_167(self.vmethod_3(point3d2, False)));
                    self.linesr.Add(point3d3.smethod_167(self.vmethod_3(point3d3, True)));
                    flag = True;
                if (flag1 or not MathHelper.smethod_117(point3d_1, point3dCollection_3.get_Item(num), point3dCollection_0.get_Item(num), False)):
                    if (flag and not flag1):
                        self.linesl.Add(point3dCollection_0.get_Item(num).smethod_167(self.vmethod_3(point3dCollection_0.get_Item(num), True)));
                        self.linepl.Add(point3dCollection_1.get_Item(num).smethod_167(self.vmethod_3(point3dCollection_1.get_Item(num), False)));
                        self.linepr.Add(point3dCollection_2.get_Item(num).smethod_167(self.vmethod_3(point3dCollection_2.get_Item(num), False)));
                        self.linesr.Add(point3dCollection_3.get_Item(num).smethod_167(self.vmethod_3(point3dCollection_3.get_Item(num), True)));
                    num += 1;
                else:
                    point3d5 = MathHelper.distanceBearingPoint(point3d_1, self.trm90, 100);
                    point3d = MathHelper.getIntersectionPoint(point3dCollection_0.get_Item(num1), point3dCollection_0.get_Item(num2), point3d_1, point3d5);
                    point3d1 = MathHelper.getIntersectionPoint(point3dCollection_1.get_Item(num1), point3dCollection_1.get_Item(num2), point3d_1, point3d5);
                    point3d2 = MathHelper.getIntersectionPoint(point3dCollection_2.get_Item(num1), point3dCollection_2.get_Item(num2), point3d_1, point3d5);
                    point3d3 = MathHelper.getIntersectionPoint(point3dCollection_3.get_Item(num1), point3dCollection_3.get_Item(num2), point3d_1, point3d5);
                    self.linesl.Add(point3d.smethod_167(self.vmethod_3(point3d, True)));
                    self.linepl.Add(point3d1.smethod_167(self.vmethod_3(point3d1, False)));
                    self.linepr.Add(point3d2.smethod_167(self.vmethod_3(point3d2, False)));
                    self.linesr.Add(point3d3.smethod_167(self.vmethod_3(point3d3, True)));
                    flag1 = True;
                    break;
            else:
                break;
        self.linesl = Point3dCollection.smethod_146(self.linesl);
        self.linepl = Point3dCollection.smethod_146(self.linepl);
        self.linepr = Point3dCollection.smethod_146(self.linepr);
        self.linesr = Point3dCollection.smethod_146(self.linesr);
        self.selectionArea = Point3dCollection();
        for i in range(0, self.linesl.get_Count()):
            self.selectionArea.Add(self.linesl.get_Item(i));

        for j in range(0, self.linesr.get_Count()):
            self.selectionArea.Add(self.linesr.get_Item(self.linesr.get_Count() - 1 - j));
        polylineArea = PolylineArea();
        for k in range(0, self.linepl.get_Count()):
            polylineArea.method_1(self.linepl.get_Item(k));
        for l in range(0, self.linepr.get_Count()):
            polylineArea.method_1(self.linepr.get_Item(self.linepr.get_Count() - 1 - l));
        self.primaryArea = PrimaryObstacleArea(polylineArea);
        for m in range(1, self.linesl.get_Count()):
            self.secondaryAreas.append(SecondaryObstacleArea(self.linepl.get_Item(m - 1), self.linepl.get_Item(m), self.linesl.get_Item(m-1), self.linesl.get_Item(m ), self.tr));
            self.secondaryAreas.append(SecondaryObstacleArea(self.linepr.get_Item(m - 1), self.linepr.get_Item(m), self.linesr.get_Item(m-1), self.linesr.get_Item(m ), self.tr));
    
    def method_1(self, obstacle_0):
        point3d = None;
        point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.tr180, obstacle_0.Tolerance);
        point3d = MathHelper.getIntersectionPoint(self.ptTHR, self.ptEND, point3d1, MathHelper.distanceBearingPoint(point3d1, self.trm90, 100));
        num = MathHelper.calcDistance(self.ptTHR, point3d);
        if (MathHelper.smethod_119(point3d, self.ptTHR, self.ptTHRm90)):
            num = num * -1;
        return num;
    
    def method_2(self, point3d_0, double_0):
        self.tr = double_0;
        self.tr180 = MathHelper.smethod_4(double_0 + 3.14159265358979);
        self.trm90 = MathHelper.smethod_4(double_0 - 1.5707963267949);
        self.trp90 = MathHelper.smethod_4(double_0 + 1.5707963267949);
        self.ptTHR = point3d_0;
        self.ptEND = MathHelper.distanceBearingPoint(self.ptTHR, self.tr, 1000);
        self.ptTHRm90 = MathHelper.distanceBearingPoint(self.ptTHR, self.trm90, 1000);
    # def vmethod_0(self, obstacle_0, obstacleAreaResult_0):
    #     double_0 = None
    #     double_1 = None
    #     double_2 = None
    #     double_3 = None
    #     return

    def vmethod_1(self, constructLayer, bool_0):
        AcadHelper.smethod_18(AcadHelper.smethod_126(self.linesl), constructLayer);
        AcadHelper.smethod_18(AcadHelper.smethod_126(self.linepl), constructLayer);
        AcadHelper.smethod_18(AcadHelper.smethod_126(self.linepr), constructLayer);
        AcadHelper.smethod_18(AcadHelper.smethod_126(self.linesr), constructLayer);
        item = [self.linesl.get_Item(0), self.linesr.get_Item(0) ];
        AcadHelper.smethod_18(AcadHelper.smethod_126(item), constructLayer);
        if (bool_0):
            point3dArray = [self.linesl.get_Item(self.linesl.get_Count() - 1), self.linesr.get_Item(self.linesr.get_Count() - 1)];
            AcadHelper.smethod_18(AcadHelper.smethod_126(point3dArray), constructLayer);
    def vmethod_2(self, constructLayer):
        for i in range(1, self.linesl.get_Count()):
            face = PolylineArea([self.linepl.get_Item(i - 1), self.linepl.get_Item(i), self.linepr.get_Item(i), self.linepr.get_Item(i - 1)])
            AcadHelper.smethod_18(face, constructLayer);
            face = PolylineArea([self.linesl.get_Item(i - 1), self.linesl.get_Item(i), self.linepl.get_Item(i), self.linepl.get_Item(i - 1)])
            AcadHelper.smethod_18(face, constructLayer);
            face = PolylineArea([self.linesr.get_Item(i - 1), self.linesr.get_Item(i), self.linepr.get_Item(i), self.linepr.get_Item(i - 1)])
            AcadHelper.smethod_18(face, constructLayer);
    def get_LinePL(self):
        return self.linepl
    LinePL = property(get_LinePL, None, None, None)

    def get_LinePR(self):
        return self.linepr
    LinePR = property(get_LinePR, None, None, None)

    def get_LineSL(self):
        return self.linesl
    LineSL = property(get_LineSL, None, None, None)

    def get_LineSR(self):
        return self.linesr
    LineSR = property(get_LineSR, None, None, None)

    def get_Type(self):
        return self.type
    Type = property(get_Type, None, None, None)

class BaroVnavSurfaceZ(IBaroVnavSurface):
    def __init__(self, point3d_0, double_0, double_1, double_2, double_3):
        IBaroVnavSurface.__init__(self)

        self.xz = None;
        self.tanslope = None;
        self.mocma = None;
        self.ptXz = None;
        self.ptXzm90 = None;
        self.turnObstacles = [];
        
        self.type = BaroVnavSurfaceType.Z;
        self.method_2(point3d_0, double_0);
        if (double_1 >= 0):
            self.ptXz = MathHelper.distanceBearingPoint(self.ptTHR, self.tr180, math.fabs(double_1));
        else:
            self.ptXz = MathHelper.distanceBearingPoint(self.ptTHR, self.tr, math.fabs(double_1));
        self.ptXzm90 = MathHelper.distanceBearingPoint(self.ptXz, self.trm90, 1000);
        self.xz = double_1;
        self.tanslope = double_3;
        self.mocma = double_2;
        
    def vmethod_0(self, obstacle_0):
        obstacleAreaResult_0 = ObstacleAreaResult.Outside;
        double_0 = None;
        double_1 = self.mocma;
        double_2 = None;
        double_3 = None;
        if (MathHelper.pointInPolygon(self.selectionArea, obstacle_0.Position, obstacle_0.Tolerance)):
            resultList = []
            obstacleAreaResult_0 = self.primaryArea.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, double_1, resultList);
            if len(resultList) != 0:
                double_2 = resultList[0]
                double_0 = resultList[1]
            if (obstacleAreaResult_0 != ObstacleAreaResult.Primary):
                double_0 = None;
                double_2 = None;
                for current in self.secondaryAreas:
                    num = None;
                    num1 = None;
                    resultList = []
                    obstacleAreaResult = current.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, double_1, resultList);
                    if len(resultList) != 0:
                        num = resultList[0]
                        num1 = resultList[1]
                    if (obstacleAreaResult == ObstacleAreaResult.Primary):
                        obstacleAreaResult_0 = obstacleAreaResult;
                        double_2 = num;
                        double_0 = num1;
                        break;
                    elif (obstacleAreaResult == ObstacleAreaResult.Secondary and (num > double_2 or double_2 == None)):
                        obstacleAreaResult_0 = obstacleAreaResult;
                        double_2 = num;
                        double_0 = num1;
            if (obstacleAreaResult_0 != ObstacleAreaResult.Outside):
                point3d = MathHelper.distanceBearingPoint(obstacle_0.Position, self.tr180, obstacle_0.Tolerance);
                double_3 = self.vmethod_3(point3d, False);
                if (obstacleAreaResult_0 == ObstacleAreaResult.Secondary):
                    double_3 = double_3 + (double_1 - double_2);
                return True, obstacleAreaResult_0, double_0, double_1, double_2, double_3;
        return False, obstacleAreaResult_0, double_0, double_1, double_2, double_3;
    def vmethod_3(self, point3d_0, bool_0):
        point3d = None;
        point3d == MathHelper.getIntersectionPoint(self.ptTHR, self.ptEND, point3d_0, MathHelper.distanceBearingPoint(point3d_0, self.trm90, 100));
        num = 0;
        if (MathHelper.smethod_119(point3d, self.ptXz, self.ptXzm90)):
            num = MathHelper.calcDistance(self.ptXz, point3d);
        num1 = num * self.tanslope;
        if (bool_0):
            num1 = num1 + self.mocma;
        return self.ptTHR.get_Z() + num1;
        
    def get_Moc(self):
        return self.mocma
    Moc = property(get_Moc, None, None, None)

class BaroVnavSurfaceH(IBaroVnavSurface):
    def __init__(self, point3d_0, double_0, double_1, double_2, double_3, double_4, double_5):
        IBaroVnavSurface.__init__(self)

        self.type = BaroVnavSurfaceType.H;
        self.method_2(point3d_0, double_0);
        self.xfas = double_2;
        self.xz = double_1;
        self.xatt = double_5;
        self.tanslope = (max([double_3, double_4]) - min([double_3, double_4])) / (double_2 - double_5);
        self.mocfa = max(double_3, double_4);
        self.mocma = min(double_3, double_4);

    def vmethod_0(self, obstacle_0):
        point3d = None;
        obstacleAreaResult_0 = ObstacleAreaResult.Outside;
        double_0 = None;
        double_1 = None;
        double_2 = None;
        double_3 = None;
        if (not MathHelper.pointInPolygon(self.selectionArea, obstacle_0.Position, obstacle_0.Tolerance)):
            pass
        if (MathHelper.pointInPolygon(self.selectionArea, obstacle_0.Position, obstacle_0.Tolerance)):
            point3d = MathHelper.getIntersectionPoint(self.ptTHR, self.ptEND, obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, self.trm90, 100));
            num = 0;
            if (MathHelper.smethod_115(point3d, self.ptTHR, self.ptTHRm90)):
                num = max(MathHelper.calcDistance(self.ptTHR, point3d) - obstacle_0.Tolerance - self.xatt, 0);
            double_1 = self.mocma + num * self.tanslope;
            resultList = []
            obstacleAreaResult_0 = self.primaryArea.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, double_1, resultList);
            if len(resultList) != 0:
                double_2 = resultList[0]
                double_0 = resultList[1]
            if (obstacleAreaResult_0 != ObstacleAreaResult.Primary):
                double_0 = None;
                double_2 = None;
                for current in self.secondaryAreas:
                    num1 = None;
                    num2 = None;
                    resultList = []
                    obstacleAreaResult = current.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, double_1, resultList);
                    if len(resultList) != 0:
                        num1 = resultList[0]
                        num2 = resultList[1]
                    if (obstacleAreaResult == ObstacleAreaResult.Primary):
                        obstacleAreaResult_0 = obstacleAreaResult;
                        double_2 = num1;
                        double_0 = num2;
                        break;
                    elif (obstacleAreaResult == ObstacleAreaResult.Secondary and (num1 > double_2 or double_2 == None)):
                        obstacleAreaResult_0 = obstacleAreaResult;
                        double_2 = num1;
                        double_0 = num2;
            if (obstacleAreaResult_0 != ObstacleAreaResult.Outside):
                point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.tr, obstacle_0.Tolerance);
                double_3 = self.vmethod_3(point3d1, False);
                if (obstacleAreaResult_0 == ObstacleAreaResult.Secondary):
                    double_3 = double_3 + (double_1 - double_2);
                return True, obstacleAreaResult_0, double_0, double_1, double_2, double_3;
        return False, obstacleAreaResult_0, double_0, double_1, double_2, double_3;
    
    def vmethod_3(self, point3d_0, bool_0):
        point3d = None;
        point3d = MathHelper.getIntersectionPoint(self.ptTHR, self.ptEND, point3d_0, MathHelper.distanceBearingPoint(point3d_0, self.trm90, 100));
        num = 0;
        if (MathHelper.smethod_115(point3d, self.ptTHR, self.ptTHRm90)):
            num = max([MathHelper.calcDistance(self.ptTHR, point3d) - self.xatt, 0]);
        num1 = 0;
        if (bool_0):
            num1 = self.mocma + num * self.tanslope;
        return self.ptTHR.get_Z() + num1;

class BaroVnavSurfaceFAS(IBaroVnavSurface):
    def __init__(self, point3d_0, double_0, double_1, double_2, list_0):
        IBaroVnavSurface.__init__(self)

        self.type = BaroVnavSurfaceType.FAS;
        self.method_2(point3d_0, double_0);
        self.moci = double_2;
        self.xfap = double_1;
        self.segments = list_0;
        
    def method_3(self, point3d_0):
        point3d = None;
        point3d = MathHelper.getIntersectionPoint(self.ptTHR, self.ptEND, point3d_0, MathHelper.distanceBearingPoint(point3d_0, self.trm90, 100));
        if (MathHelper.smethod_115(point3d, self.ptTHR, self.ptTHRm90)):
            num = MathHelper.calcDistance(self.ptTHR, point3d);
            for i in range(len(self.segments)):
                if (num < self.segments[i].xstart):
                    return self.segments[i].moc;
                if (num >= self.segments[i].xstart and num <= self.segments[i].xend):
                    return self.segments[i].moc;
                if (i + 1 >= len(self.segments)):
                    return self.segments[i].moc;
                if (num <= self.segments[i + 1].xstart):
                    item = self.segments[i].moc;
                    item1 = self.segments[i + 1].moc;
                    num1 = (item1 - item) / (self.segments[i + 1].xstart - self.segments[i].xend);
                    return item + (num - self.segments[i].xend) * num1;
        return self.segments[0].moc;

    def vmethod_0(self, obstacle_0):
        point3d = MathHelper.distanceBearingPoint(obstacle_0.Position, self.tr, obstacle_0.Tolerance);
        obstacleAreaResult_0 = ObstacleAreaResult.Outside;
        double_0 = None;
        double_1 = self.method_3(point3d);
        double_2 = None;
        double_3 = None;
        if not MathHelper.pointInPolygon(self.selectionArea, obstacle_0.Position, obstacle_0.Tolerance):
            pass
        if (MathHelper.pointInPolygon(self.selectionArea, obstacle_0.Position, obstacle_0.Tolerance)):
            resultList = []
            obstacleAreaResult_0 = self.primaryArea.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, double_1, resultList);
            if len(resultList) != 0:
                double_2 = resultList[0]
                double_0 = resultList[1]
            if (obstacleAreaResult_0 != ObstacleAreaResult.Primary):
                double_0 = None;
                double_2 = None;
                for current in self.secondaryAreas:
                    num = None;
                    num1 = None;
                    resultList = []

                    obstacleAreaResult = current.imethod_1(obstacle_0.Position, obstacle_0.Tolerance, double_1, resultList);
                    if len(resultList) != 0:
                        num = resultList[0]
                        num1 = resultList[1]
                        if double_2 != None and num > double_2:
                            pass
                    if (obstacleAreaResult == ObstacleAreaResult.Primary):
                        obstacleAreaResult_0 = obstacleAreaResult;
                        double_2 = num;
                        double_0 = num1;
                        break;
                    elif (obstacleAreaResult == ObstacleAreaResult.Secondary and (num > double_2 or double_2 == None)):
                        obstacleAreaResult_0 = obstacleAreaResult;
                        double_2 = num;
                        double_0 = num1;
            if (obstacleAreaResult_0 != ObstacleAreaResult.Outside):
                double_3 = self.vmethod_3(point3d, False);
                if (obstacleAreaResult_0 == ObstacleAreaResult.Secondary):
                    double_3 = double_3 + (double_1 - double_2);
                return True, obstacleAreaResult_0, double_0, double_1, double_2, double_3;
        return False, obstacleAreaResult_0, double_0, double_1, double_2, double_3;
    
    def vmethod_3(self, point3d_0, bool_0):
        point3d = None;
        point3d = MathHelper.getIntersectionPoint(self.ptTHR, self.ptEND, point3d_0, MathHelper.distanceBearingPoint(point3d_0, self.trm90, 100));
        item = 0;
        if (MathHelper.smethod_115(point3d, self.ptTHR, self.ptTHRm90)):
            num = MathHelper.calcDistance(self.ptTHR, point3d);
            num1 = 0;
            while (num1 < len(self.segments)):
                if (num < self.segments[num1].xstart):
                    if (not bool_0):
                        return self.ptTHR.get_Z() + item;
                    item = item + self.segments[num1].moc;
                    return self.ptTHR.get_Z() + item;
                elif (num < self.segments[num1].xstart or num > self.segments[num1].xend):
                    if (num1 + 1 >= len(self.segments)):
                        item = (self.segments[num1].xend - self.segments[num1].xfas) * self.segments[num1].tanafas;
                        if (bool_0):
                            item = item + self.segments[num1].moc;
                    elif (num <= self.segments[num1 + 1].xstart):
                        item = (self.segments[num1].xend - self.segments[num1].xfas) * self.segments[num1].tanafas;
                        if (not bool_0):
                            return self.ptTHR.get_Z() + item;
                        item1 = self.segments[num1].moc;
                        item2 = self.segments[num1 + 1].moc;
                        num2 = (item2 - item1) / (self.segments[num1 + 1].xstart - self.segments[num1].xend);
                        item3 = item1 + (num - self.segments[num1].xend) * num2;
                        item = item + item3;
                        return self.ptTHR.get_Z() + item;
                    num1 += 1;
                else:
                    item = (num - self.segments[num1].xfas) * self.segments[num1].tanafas;
                    if (not bool_0):
                        return self.ptTHR.get_Z() + item;
                    item = item + self.segments[num1].moc;
                    return self.ptTHR.get_Z() + item;
        elif (bool_0):
            item = item + self.segments[0].moc;
        return self.ptTHR.get_Z() + item;


class BaroVnavObstacles(ObstacleTable):
    def __init__(self, list_0, baroVnavMaEvaluationMethod_0, double_0, double_1, double_2, double_3, point3d_0):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, None)
        self.surfaces = list_0;
        # self.obstacles = list_1;
        self.evalMethod = baroVnavMaEvaluationMethod_0;
        self.cotmacg = 1 / double_0;
        self.cotvpa = 1 / double_1;
        self.xz = double_2;
        self.hl = double_3;
        self.ptTHR = point3d_0;
    def setHiddenColumns(self, tableView):
        tableView.hideColumn(self.IndexSurface)
        # tableView.hideColumn(self.IndexHeightLossMFt)
#         tableView.hideColumn(self.IndexDistInSecM)
        return ObstacleTable.setHiddenColumns(self, tableView)
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)

        self.IndexObstArea = fixedColumnCount
        self.IndexDistInSecM = fixedColumnCount + 1
        self.IndexMocAppliedM = fixedColumnCount + 2
        self.IndexMocAppliedFt = fixedColumnCount + 3
        # self.IndexMocMultiplier = fixedColumnCount + 4
        self.IndexEqAltM = fixedColumnCount + 4
        self.IndexEqAltFt = fixedColumnCount + 5
        self.IndexSurfAltM = fixedColumnCount + 6
        self.IndexSurfAltFt = fixedColumnCount + 7
        self.IndexDifferenceM = fixedColumnCount + 8
        self.IndexDifferenceFt = fixedColumnCount + 9
        self.IndexHeightLossM = fixedColumnCount + 10
        self.IndexHeightLossMFt = fixedColumnCount + 11
        self.IndexOcaM = fixedColumnCount + 12
        self.IndexOcaFt = fixedColumnCount + 13
        self.IndexCritical = fixedColumnCount + 14
        self.IndexSurface = fixedColumnCount + 15

        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM,
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                # ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.EqAltM,
                ObstacleTableColumnType.EqAltFt,
                ObstacleTableColumnType.SurfAltM,
                ObstacleTableColumnType.SurfAltFt,
                ObstacleTableColumnType.DifferenceM,
                ObstacleTableColumnType.DifferenceFt,
                ObstacleTableColumnType.HeightLossM,
                ObstacleTableColumnType.HeightLossFt,
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

        # item = QStandardItem(str(ObstacleTable.MocMultiplier))
        # item.setData(ObstacleTable.MocMultiplier)
        # self.source.setItem(row, self.IndexMocMultiplier, item)

        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexEqAltM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[3]))
        self.source.setItem(row, self.IndexEqAltFt, item)

        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexSurfAltM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[4])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[4]))
        self.source.setItem(row, self.IndexSurfAltFt, item)

        item = QStandardItem(str(checkResult[5]))
        item.setData(checkResult[5])
        self.source.setItem(row, self.IndexDifferenceM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[5])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[5]))
        self.source.setItem(row, self.IndexDifferenceFt, item)

        item = QStandardItem(str(checkResult[6]))
        item.setData(checkResult[6])
        self.source.setItem(row, self.IndexHeightLossM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[6])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[6]))
        self.source.setItem(row, self.IndexHeightLossMFt, item)

        item = QStandardItem(str(checkResult[7]))
        item.setData(checkResult[7])
        self.source.setItem(row, self.IndexOcaM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[7])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[7]))
        self.source.setItem(row, self.IndexOcaFt, item)

        critical = CriticalObstacleType.No
        if checkResult[5] <= 0:
            critical = CriticalObstacleType.No
        else:
            critical = CriticalObstacleType.Yes
        item = QStandardItem(str(critical))
        item.setData(critical)
        self.source.setItem(row, self.IndexCritical, item)

        item = QStandardItem(str(checkResult[8]))
        item.setData(checkResult[8])
        self.source.setItem(row, self.IndexSurface, item)

    def checkObstacle(self, obstacle_0):
        num = None;
        num1 = None;
        num2 = None;
        num3 = None;
        for i in range(len(self.surfaces)):
            item = self.surfaces[i];
            # baroVnavObstacle = self.obstacles[i];
            num4 = None;
            obstacleAreaResult = ObstacleAreaResult.Outside;
            result, obstacleAreaResult, num, num1, num2, num3 = item.vmethod_0(obstacle_0)
            if (result):
                z = obstacle_0.Position.get_Z() + obstacle_0.Trees;
                num5 = None;
                z1 = None;
                if (z > num3):
                    num4 = self.hl;
                    z2 = z - self.ptTHR.get_Z();
                    if (self.evalMethod != BaroVnavMaEvaluationMethod.Standard):
                        num6 = item.method_1(obstacle_0);
                        if (item.Type == BaroVnavSurfaceType.Z):
                            num6 = min([num6, self.xz]);
                        z2 = z2 - (num1 - num2);
                        num5 = (z2 * self.cotmacg + (num6 - self.xz)) / (self.cotmacg + self.cotvpa);
                        if (num5 > z2):
                            num5 = None;
                    elif (item.Type == BaroVnavSurfaceType.Z):
                        num7 = min(item.method_1(obstacle_0), self.xz);
                        z2 = z2 - (num1 - num2);
                        num5 = (z2 * self.cotmacg + (num7 - self.xz)) / (self.cotmacg + self.cotvpa);
                    if (not num5 == None):
                        z1 = self.ptTHR.get_Z() + num5 + num4;
                    else:
                        num4 = num2 / num1 * num4;
                        z1 = z + num4;
                    if num5 == None:
                        num5 = 0
                    BaroVNAVDlg.resultCriticalObst.method_0(obstacle_0, num5 + self.ptTHR.get_Z(), z1, self.surfaces[i].type);
                if num5 == None:
                    num5 = 0
                checkResults = [obstacleAreaResult, num, num2, num5 + self.ptTHR.get_Z(), num3, z - num3, num4, z1, self.surfaces[i].type]
                self.addObstacleToModel(obstacle_0, checkResults)