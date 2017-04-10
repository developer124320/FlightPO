# -*- coding: UTF-8 -*-
'''
Created on 24 May 2014

@author: Administrator
'''
from PyQt4.QtGui import QMessageBox, QStandardItem, QFileDialog
from PyQt4.QtCore import QCoreApplication, QString, SIGNAL, Qt, QRect
from qgis.core import QGis, QgsLayerTreeLayer, QgsVectorLayer, QgsPalLayerSettings
from qgis.gui import QgsMapTool, QgsMapCanvasSnapper, QgsRubberBand
from map.tools import QgsMapToolSelectUtils
from FlightPlanner.QgisHelper import QgisHelper, Geo

from FlightPlanner.ChartingGrid.ui_ChartingGrid import Ui_ChartingGrid

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import AltitudeUnits, Point3D, AngleUnits, SurfaceTypes,\
                Matrix3d, Vector3d
from FlightPlanner.types import EnumsType, TurnDirection, Point3dCollection
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.helpers import Distance, Speed, Altitude, MathHelper, Unit
from Type.Degrees import Degrees, DegreesType, DegreesStyle
from Type.switch import switch
from Type.String import String
import define
import math

class ChartingGridLinesCategory:
    Major = 0
    Intermediate = 1
    Minor = 2

class ChartingGridDlg(FlightPlanBaseDlg):
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("ChartingGridDlg")
        self.surfaceType = SurfaceTypes.ChartingGrid

        self.initParametersPan()
        self.uiStateInit()
        self.setWindowTitle(SurfaceTypes.ChartingGrid)
        self.resize(540, 550)
        QgisHelper.matchingDialogSize(self, 570, 570)

        self.constructionLayer = None


    def btnEvaluate_Click(self):
        return FlightPlanBaseDlg.btnEvaluate_Click(self)


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
        DataHelper.saveExportResult(filePathDir, SurfaceTypes.BaseTurnTC, self.ui.tblObstacles, None, parameterList, resultHideColumnNames )
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbObstSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    
    def getParameterList(self):
        parameterList = []
        parameterList.append(("General", "group"))
        parameterList.append(("Navigational Aid", "group"))
        parameterList.append(("Type", self.parametersPanel.cmbNavAidType.SelectedItem))
        # longLatPoint = QgisHelper.Meter2Degree(float(self.parametersPanel.pnlNavAid.txtPointX.text()), float(self.parametersPanel.pnlNavAid.txtPointY.text()))
        
        parameterList.append(("Lat", self.parametersPanel.pnlNavAid.txtLat.Value))
        parameterList.append(("Lon", self.parametersPanel.pnlNavAid.txtLong.Value))
        parameterList.append(("X", self.parametersPanel.pnlNavAid.txtPointX.text()))
        parameterList.append(("Y", self.parametersPanel.pnlNavAid.txtPointY.text()))
        parameterList.append(("Altitude", self.parametersPanel.pnlNavAid.txtAltitudeFt.text() + "ft"))
        parameterList.append(("", self.parametersPanel.pnlNavAid.txtAltitudeM.text() + "m"))
        
        parameterList.append(("Parameters", "group"))
#         parameterList.append(("Used For", self.parametersPanel.cmbUsedFor.currentText()))
#         parameterList.append(("Holding Functionality Required", self.parametersPanel.cmbHoldingFunctionality.currentText()))
#         if self.parametersPanel.cmbHoldingFunctionality.currentIndex() != 0:            
#             parameterList.append(("Out-bound Red Limitation", self.parametersPanel.cmbOutboundLimit.currentText()))
#         parameterList.append(("Aircraft Category", self.parametersPanel.cmbAircraftCategory.currentText()))
        parameterList.append(("IAS", self.parametersPanel.txtIas.text() + "kts"))
        parameterList.append(("TAS", self.parametersPanel.txtTas.text() + "kts"))
        parameterList.append(("Altitude", self.parametersPanel.txtAltitudeM.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtAltitude.text() + "ft"))
        parameterList.append(("ISA", self.parametersPanel.txtIsa.text() + unicode("°C", "utf-8")))
        parameterList.append(("Offset Entry Angle", self.parametersPanel.txtOffset.text() + unicode("°", "utf-8")))
        parameterList.append(("Turn Limitation", self.parametersPanel.cmbTurnLimitation.currentText()))
        if self.parametersPanel.cmbTurnLimitation.currentText() == "Time":
            parameterList.append(("Time", self.parametersPanel.txtTime.text() + "min"))
        else:
            parameterList.append(("DME Distance", self.parametersPanel.txtDmeDistance.text() + "nm"))
        parameterList.append(("Wind", self.parametersPanel.pnlWind.speedBox.text() + "kts"))
        
        parameterList.append(("Time", self.parametersPanel.txtTime.text()))
        parameterList.append(("MOC", self.parametersPanel.txtMoc.text() + "m"))
        parameterList.append(("", self.parametersPanel.txtMocFt.text() + "ft"))
        parameterList.append(("MOCmultipiler", str(self.parametersPanel.spinBoxMocmulipiler.value())))

        parameterList.append(("Orientation", "Plan : " + str(self.parametersPanel.txtTrackRadial.txtRadialPlan.Value) + define._degreeStr))
        parameterList.append(("", "Geodetic : " + str(self.parametersPanel.txtTrackRadial.txtRadialGeodetic.Value) + define._degreeStr))

        parameterList.append(("major Turn", self.parametersPanel.cmbOrientation.currentText()))
        
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
        self.ui.tabCtrlGeneral.removeTab(1)
        self.ui.tabCtrlGeneral.removeTab(1)
        return FlightPlanBaseDlg.uiStateInit(self)
         


    def initParametersPan(self):
        ui = Ui_ChartingGrid()
        self.parametersPanel = ui
        
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.cmbLatFormat.Items = ["DDMM", "DD° MM'", "DDMM(N/S)", "DD° MM' (N/S)", "(N/S)DDMM", "(N/S) DD° MM'"]
        self.parametersPanel.pnlLonFormat.Items = ["DDMM", "DD° MM'", "DDDMM(E/W)", "DDD° MM' (E/W)", "(E/W)DDDMM", "(E/W) DDD° MM'"]
        self.parametersPanel.cmbMajorLines.Items = [EnumsType.ChartingGridLinesType_FullArcs, EnumsType.ChartingGridLinesType_Ticks]
        self.parametersPanel.cmbIntermediateLines.Items = [EnumsType.ChartingGridLinesType_None, EnumsType.ChartingGridLinesType_FullArcs, EnumsType.ChartingGridLinesType_Ticks]
        self.parametersPanel.cmbMinorLines.Items = [EnumsType.ChartingGridLinesType_None, EnumsType.ChartingGridLinesType_FullArcs, EnumsType.ChartingGridLinesType_Ticks]

        # self.connect(self.parametersPanel.pnlMinorLinesTickLength, SIGNAL("Event_1"), self.method_34)
        self.connect(self.parametersPanel.cmbMinorLines, SIGNAL("Event_0"), self.method_31)
        # self.connect(self.parametersPanel.pnlMajorLinesTickLength, SIGNAL("Event_1"), self.method_33)
        self.connect(self.parametersPanel.cmbMajorLines, SIGNAL("Event_0"), self.method_31)
        self.connect(self.parametersPanel.cmbLatFormat, SIGNAL("Event_0"), self.method_31)
        self.connect(self.parametersPanel.cmbIntermediateLines, SIGNAL("Event_0"), self.method_31)
        # self.connect(self.parametersPanel.pnlTextHeight, SIGNAL("Event_1"), self.method_32)
        self.parametersPanel.btnPickArea.clicked.connect(self.btnPicArea_Click)

        self.parametersPanel.cmbMajorLines.SelectedIndex = 1

        self.method_31()

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        point3d = self.parametersPanel.pnlLL.Point3d
        point3d1 = self.parametersPanel.pnlUR.Point3d

        result, degree, degree1 = self.parametersPanel.pnlLL.method_3()
        if (not result):
            QMessageBox.warning(self, "Warning", "Geo Error")
            return
            # throw new Exception(Geo.LastError)

        result, degree2, degree3 = self.parametersPanel.pnlUR.method_3()
        if (not result):
            QMessageBox.warning(self, "Warning", "Geo Error")
            return
            # throw new Exception(Geo.LastError)
        xMaxDegree = degree3
        xMinDegree = degree1
        yMaxDegree = degree2
        yMinDegree = degree

        num = int((xMinDegree - int(xMinDegree)) * 60) + 1
        xStartDegree = int(xMinDegree) + num / float(60)

        num = int((yMinDegree - int(yMinDegree)) * 60) + 1
        yStartDegree = int(yMinDegree) + num / float(60)

        constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)

        ptIn0 = self.parametersPanel.pnlLL.Point3d
        ptIn1 = Point3D(self.parametersPanel.pnlLL.Point3d.get_X(), self.parametersPanel.pnlUR.Point3d.get_Y())
        ptIn2 = self.parametersPanel.pnlUR.Point3d
        ptIn3 = Point3D(self.parametersPanel.pnlUR.Point3d.get_X(), self.parametersPanel.pnlLL.Point3d.get_Y())

        polylineArea = None
        # if define._units == QGis.Meters:
        #     polylineArea = PolylineArea([QgisHelper.CrsTransformPoint(ptIn0.get_X(), ptIn0.get_Y(), define._latLonCrs, define._xyCrs),
        #                                  QgisHelper.CrsTransformPoint(ptIn1.get_X(), ptIn1.get_Y(), define._latLonCrs, define._xyCrs),
        #                                  QgisHelper.CrsTransformPoint(ptIn2.get_X(), ptIn2.get_Y(), define._latLonCrs, define._xyCrs),
        #                                  QgisHelper.CrsTransformPoint(ptIn3.get_X(), ptIn3.get_Y(), define._latLonCrs, define._xyCrs),
        #                                  QgisHelper.CrsTransformPoint(ptIn0.get_X(), ptIn0.get_Y(), define._latLonCrs, define._xyCrs)])
        # else:
        #     polylineArea = PolylineArea([ptIn0, ptIn1, ptIn2, ptIn3, ptIn0])
        # AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea)

        value = math.sqrt((math.pow(int(self.parametersPanel.pnlMajorLinesTickLength.Value.Metres), 2)) * 2)
        majorValue = self.parametersPanel.pnlMajorLinesTickLength.Value.Metres

        ptOut0 = MathHelper.distanceBearingPoint(ptIn0, math.pi + math.pi / float(4), value, QGis.Degrees)
        ptOut1 = MathHelper.distanceBearingPoint(ptIn1, math.pi + (math.pi * 3) / float(4), value, QGis.Degrees)
        ptOut2 = MathHelper.distanceBearingPoint(ptIn2, math.pi / float(4), value, QGis.Degrees)
        ptOut3 = MathHelper.distanceBearingPoint(ptIn3, (math.pi * 3) / float(4), value, QGis.Degrees)

        # if define._units == QGis.Meters:
        #     polylineArea = PolylineArea([QgisHelper.CrsTransformPoint(ptOut0.get_X(), ptOut0.get_Y(), define._latLonCrs, define._xyCrs),
        #                                  QgisHelper.CrsTransformPoint(ptOut1.get_X(), ptOut1.get_Y(), define._latLonCrs, define._xyCrs),
        #                                  QgisHelper.CrsTransformPoint(ptOut2.get_X(), ptOut2.get_Y(), define._latLonCrs, define._xyCrs),
        #                                  QgisHelper.CrsTransformPoint(ptOut3.get_X(), ptOut3.get_Y(), define._latLonCrs, define._xyCrs),
        #                                  QgisHelper.CrsTransformPoint(ptOut0.get_X(), ptOut0.get_Y(), define._latLonCrs, define._xyCrs)])
        # else:
        #     polylineArea = PolylineArea([ptOut0, ptOut1, ptOut2, ptOut3, ptOut0])
        # AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea)


        pt = Point3D(xMinDegree, yStartDegree)#QgisHelper.CrsTransformPoint(xMinDegree, yStartDegree, define._latLonCrs, define._xyCrs)
        pt0 = Point3D(self.parametersPanel.pnlLL.Point3d.get_X(), pt.get_Y())


        yStartDegreeInt = int(yStartDegree)
        yStartMinuteInt = int(round(((yStartDegree - int(yStartDegree)) * 60), 10))



        i = 0
        outPoints = []
        inPoints = []

        outPoints1 = []
        inPoints1 = []
        majorFullFlag = self.parametersPanel.cmbMajorLines.SelectedIndex == 0
        minFullFlag = self.parametersPanel.cmbMinorLines.SelectedIndex == 1
        intermediaFullFlag = self.parametersPanel.cmbIntermediateLines.SelectedIndex == 1
        majorTickLength = self.parametersPanel.pnlMajorLinesTickLength.Value.Metres
        minTickLength = self.parametersPanel.pnlMinorLinesTickLength.Value.Metres
        intermediaTickLength = self.parametersPanel.pnlIntermediateLinesTickLength.Value.Metres

        majorLinesEvery = int(self.parametersPanel.txtMajorLinesEvery.Value)
        minLinesEvery = int(self.parametersPanel.txtMinorLinesEvery.Value)
        intermediaLinesEvery = int(self.parametersPanel.txtIntermediateLinesEvery.Value)

        fullLinesVertical = []
        while True:
            ptTemp = Point3D(ptOut0.get_X(), pt0.get_Y() + i / float(60))
            if ptTemp.get_Y() >= self.parametersPanel.pnlUR.Point3d.get_Y() or ptTemp.get_Y() <= self.parametersPanel.pnlLL.Point3d.get_Y():
                break
            if majorLinesEvery == 0:
                return
            if yStartMinuteInt == 60:
                yStartDegreeInt += 1
                yStartMinuteInt = 0
            dist = None
            if yStartMinuteInt % majorLinesEvery == 0:
                dist = majorTickLength
            elif intermediaLinesEvery > 0 and yStartMinuteInt % intermediaLinesEvery == 0:
                dist = intermediaTickLength
                if intermediaFullFlag:
                    dist = 0
                    # i += 1
                    # yStartMinuteInt += 1
                    # continue
            elif minLinesEvery > 0 and yStartMinuteInt % minLinesEvery == 0:
                dist = minTickLength
                if minFullFlag:
                    dist = 0
                    # i += 1
                    # yStartMinuteInt += 1
                    # continue
            else:
                i += 1
                yStartMinuteInt += 1
                continue
            if majorFullFlag and yStartMinuteInt % majorLinesEvery == 0:
                dist = 300
            ptTemp1 = MathHelper.distanceBearingPoint(ptTemp, math.pi / float(2), dist, QGis.Degrees)

            caption = ""
            space = ""
            if self.parametersPanel.chbMultiline.Visible and self.parametersPanel.chbMultiline.Checked:
                space = "\n"
            else:
                space = " "
            latFormatStr = "(N)"
            if yMinDegree <= 0:
                latFormatStr = "(S)"
            yStartMinuteStr = ""
            if yStartMinuteInt == 0:
                yStartMinuteStr = "00"
            else:
                yStartMinuteStr = str(yStartMinuteInt)
            if self.parametersPanel.cmbLatFormat.SelectedIndex == 0:
                caption = str(yStartDegreeInt) + space + str(yStartMinuteStr)
            elif self.parametersPanel.cmbLatFormat.SelectedIndex == 1:
                caption = str(yStartDegreeInt) + space + str(yStartMinuteStr) + "'"
            elif self.parametersPanel.cmbLatFormat.SelectedIndex == 2:
                caption = str(yStartDegreeInt) + space + str(yStartMinuteStr) + latFormatStr
            elif self.parametersPanel.cmbLatFormat.SelectedIndex == 4:
                caption = latFormatStr + str(yStartDegreeInt) + space + str(yStartMinuteStr)
            else:
                caption = latFormatStr + str(yStartDegreeInt) + space + str(yStartMinuteStr) + "'"

            if define._units == QGis.Meters:
                ptTemp = QgisHelper.CrsTransformPoint(ptTemp.get_X(), ptTemp.get_Y(), define._latLonCrs, define._xyCrs)
                ptTemp1 = QgisHelper.CrsTransformPoint(ptTemp1.get_X(), ptTemp1.get_Y(), define._latLonCrs, define._xyCrs)
            if yStartMinuteInt % majorLinesEvery == 0:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [ptTemp, ptTemp1], False, {"Caption": caption})
                # AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [ptTemp1, ptTemp], False, {"Caption": str(yStartMinuteInt) + "'"})
            else:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [ptTemp, ptTemp1])
            outPoints.append(ptTemp)
            if yStartMinuteInt % majorLinesEvery == 0:
                inPoints.append(ptTemp1)

            ptTemp = Point3D(ptOut3.get_X(), pt0.get_Y() + i / float(60))
            ptTemp1 = MathHelper.distanceBearingPoint(ptTemp, math.pi * 3 / float(2), dist, QGis.Degrees)


            if define._units == QGis.Meters:
                ptTemp = QgisHelper.CrsTransformPoint(ptTemp.get_X(), ptTemp.get_Y(), define._latLonCrs, define._xyCrs)
                ptTemp1 = QgisHelper.CrsTransformPoint(ptTemp1.get_X(), ptTemp1.get_Y(), define._latLonCrs, define._xyCrs)
            if yStartMinuteInt % majorLinesEvery == 0:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [ptTemp1, ptTemp], False, {"Caption": caption})
                # AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [ptTemp, ptTemp1], False, {"Caption": str(yStartMinuteInt) + "'"})
            else:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [ptTemp1, ptTemp])
            outPoints1.append(ptTemp)
            if yStartMinuteInt % majorLinesEvery == 0:
                inPoints1.append(ptTemp1)

            # if (majorFullFlag and yStartMinuteInt % majorLinesEvery == 0) or (intermediaFullFlag and yStartMinuteInt % intermediaLinesEvery == 0) or (minFullFlag and yStartMinuteInt % minLinesEvery == 0):
            #     fullLinePoints = []
            #     j = 0
            #     while True:
            #         ptT = Point3D(xStartDegree + j / float(60), ptOut0.get_Y())
            #         if ptT.get_X() >= self.parametersPanel.pnlUR.Point3d.get_X() or ptT.get_X() <= self.parametersPanel.pnlLL.Point3d.get_X():
            #             break
            #         if define._units == QGis.Meters:
            #             ptT = QgisHelper.CrsTransformPoint(ptT.get_X(), ptT.get_Y(), define._latLonCrs, define._xyCrs)
            #         fullLinePoints.append(Point3D(ptT.get_X(), ptTemp1.get_Y()))
            #         j += 1
            #     fullLinesVertical.append(PolylineArea(fullLinePoints))


            i += 1
            yStartMinuteInt += 1
        # if len(fullLinesVertical) > 0:
        #     for polylineArea0 in fullLinesVertical:
        #         AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, polylineArea0)
        pt = Point3D(xStartDegree, yMinDegree)#QgisHelper.CrsTransformPoint(xStartDegree, yMinDegree, define._latLonCrs, define._xyCrs)
        pt0 = Point3D(pt.get_X(), self.parametersPanel.pnlLL.Point3d.get_Y())
        xStartDegreeInt = int(xStartDegree)
        xStartMinuteInt = int(round(((xStartDegree - int(xStartDegree)) * 60), 10))
        i = 0
        outPoints2 = []
        inPoints2 = []
        outPoints3 = []
        inPoints3 = []
        while True:
            ptTemp = Point3D(pt0.get_X() + i / float(60), ptOut0.get_Y())
            if ptTemp.get_X() >= self.parametersPanel.pnlUR.Point3d.get_X() or ptTemp.get_X() <= self.parametersPanel.pnlLL.Point3d.get_X():
                break
            if xStartMinuteInt == 60:
                xStartDegreeInt += 1
                xStartMinuteInt = 0
            dist = None
            if xStartMinuteInt % majorLinesEvery == 0:
                dist = majorTickLength
            elif intermediaLinesEvery > 0 and xStartMinuteInt % intermediaLinesEvery == 0:
                dist = intermediaTickLength
                if intermediaFullFlag:
                    dist = 0
                    # i += 1
                    # yStartMinuteInt += 1
                    # continue
            elif minLinesEvery > 0 and xStartMinuteInt % minLinesEvery == 0:
                dist = minTickLength
                if minFullFlag:
                    dist = 0
                    # i += 1
                    # yStartMinuteInt += 1
                    # continue
            else:
                i += 1
                xStartMinuteInt += 1
                continue
            if majorFullFlag and xStartMinuteInt % majorLinesEvery == 0:
                dist = 300
            caption = ""
            space = ""
            latFormatStr = "(E)"
            if yMinDegree <= 0:
                latFormatStr = "(W)"
            xStartMinuteStr = ""
            if xStartMinuteInt == 0:
                xStartMinuteStr = "00"
            else:
                xStartMinuteStr = str(xStartMinuteInt)

            if self.parametersPanel.pnlLonFormat.SelectedIndex == 0:
                caption = str(xStartDegreeInt) + space + str(xStartMinuteStr)
            elif self.parametersPanel.pnlLonFormat.SelectedIndex == 1:
                caption = str(xStartDegreeInt) + space + str(xStartMinuteStr) + "'"
            elif self.parametersPanel.pnlLonFormat.SelectedIndex == 2:
                caption = str(xStartDegreeInt) + space + str(xStartMinuteStr) + latFormatStr
            elif self.parametersPanel.pnlLonFormat.SelectedIndex == 4:
                caption = latFormatStr + str(xStartDegreeInt) + space + str(xStartMinuteStr)
            else:
                caption = latFormatStr + str(xStartDegreeInt) + space + str(xStartMinuteStr) + "'"

            ptTemp1 = MathHelper.distanceBearingPoint(ptTemp, 0.0, dist, QGis.Degrees)

            if define._units == QGis.Meters:
                ptTemp = QgisHelper.CrsTransformPoint(ptTemp.get_X(), ptTemp.get_Y(), define._latLonCrs, define._xyCrs)
                ptTemp1 = QgisHelper.CrsTransformPoint(ptTemp1.get_X(), ptTemp1.get_Y(), define._latLonCrs, define._xyCrs)
            if xStartMinuteInt % majorLinesEvery == 0:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [ptTemp, ptTemp1])
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [Point3D(ptTemp1.get_X() + 0.00001, ptTemp1.get_Y()), Point3D(ptTemp1.get_X() - 0.00001, ptTemp1.get_Y())], False, {"Caption": caption})
            else:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [ptTemp, ptTemp1])
            outPoints2.append(ptTemp)
            if xStartMinuteInt % majorLinesEvery == 0:
                inPoints2.append(ptTemp1)

            ptTemp = Point3D(pt0.get_X() + i / float(60), ptOut1.get_Y())
            ptTemp1 = MathHelper.distanceBearingPoint(ptTemp, math.pi, dist, QGis.Degrees)
            if define._units == QGis.Meters:
                ptTemp = QgisHelper.CrsTransformPoint(ptTemp.get_X(), ptTemp.get_Y(), define._latLonCrs, define._xyCrs)
                ptTemp1 = QgisHelper.CrsTransformPoint(ptTemp1.get_X(), ptTemp1.get_Y(), define._latLonCrs, define._xyCrs)
            if xStartMinuteInt % majorLinesEvery == 0:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [ptTemp, ptTemp1])
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [Point3D(ptTemp1.get_X() - 0.00001, ptTemp1.get_Y()), Point3D(ptTemp1.get_X() + 0.00001, ptTemp1.get_Y())], False, {"Caption": caption})
            else:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [ptTemp, ptTemp1])
            outPoints3.append(ptTemp)
            if xStartMinuteInt % majorLinesEvery == 0:
                inPoints3.append(ptTemp1)
            i += 1
            xStartMinuteInt += 1

        outLine = []
        ptOut00 = ptOut0
        if define._units == QGis.Meters:
            ptOut00 = QgisHelper.CrsTransformPoint(ptOut0.get_X(), ptOut0.get_Y(), define._latLonCrs, define._xyCrs)
        outLine.append(ptOut00)
        outLine.extend(outPoints)
        ptOut10 = ptOut1
        if define._units == QGis.Meters:
            ptOut10 = QgisHelper.CrsTransformPoint(ptOut1.get_X(), ptOut1.get_Y(), define._latLonCrs, define._xyCrs)
        outLine.append(ptOut10)
        outLine.extend(outPoints3)
        ptOut20 = ptOut2
        if define._units == QGis.Meters:
            ptOut20 = QgisHelper.CrsTransformPoint(ptOut2.get_X(), ptOut2.get_Y(), define._latLonCrs, define._xyCrs)
        outLine.append(ptOut20)
        outPoints1.reverse()
        outLine.extend(outPoints1)
        ptOut30 = ptOut3
        if define._units == QGis.Meters:
            ptOut30 = QgisHelper.CrsTransformPoint(ptOut3.get_X(), ptOut3.get_Y(), define._latLonCrs, define._xyCrs)
        outLine.append(ptOut30)
        outPoints2.reverse()
        outLine.extend(outPoints2)
        outLine.append(ptOut00)
        if self.parametersPanel.chbDrawRectangle.Checked:
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, outLine)

        inLine = []
        if define._units == QGis.Meters:
            ptIn0 = QgisHelper.CrsTransformPoint(ptIn0.get_X(), ptIn0.get_Y(), define._latLonCrs, define._xyCrs)
        inLine.append(ptIn0)
        inLine.extend(inPoints)
        if define._units == QGis.Meters:
            ptIn1 = QgisHelper.CrsTransformPoint(ptIn1.get_X(), ptIn1.get_Y(), define._latLonCrs, define._xyCrs)
        inLine.append(ptIn1)
        inLine.extend(inPoints3)
        if define._units == QGis.Meters:
            ptIn2 = QgisHelper.CrsTransformPoint(ptIn2.get_X(), ptIn2.get_Y(), define._latLonCrs, define._xyCrs)
        inLine.append(ptIn2)
        inPoints1.reverse()
        inLine.extend(inPoints1)
        if define._units == QGis.Meters:
            ptIn3 = QgisHelper.CrsTransformPoint(ptIn3.get_X(), ptIn3.get_Y(), define._latLonCrs, define._xyCrs)
        inLine.append(ptIn3)
        inPoints2.reverse()
        inLine.extend(inPoints2)
        inLine.append(ptIn0)
        if self.parametersPanel.chbDrawRectangle.Checked and not majorFullFlag:
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, inLine)

        fullLines = []
        xStartDegreeInt = int(xStartDegree)
        xStartMinuteInt = int(round(((xStartDegree - int(xStartDegree)) * 60), 10))
        yStartDegreeInt = int(yStartDegree)
        yStartMinuteInt = int(round(((yStartDegree - int(yStartDegree)) * 60), 10))
        i = 0
        while True:
            if yStartMinuteInt == 60:
                yStartDegreeInt += 1
                yStartMinuteInt = 0
            ptTemp0 = Point3D(ptOut0.get_X(), yStartDegree + i / float(60))
            if ptTemp0.get_Y() >= self.parametersPanel.pnlUR.Point3d.get_Y() or ptTemp0.get_Y() <= self.parametersPanel.pnlLL.Point3d.get_Y():
                break
            if (majorFullFlag and yStartMinuteInt % majorLinesEvery == 0) or (intermediaFullFlag and yStartMinuteInt % intermediaLinesEvery == 0) or (minFullFlag and yStartMinuteInt % minLinesEvery == 0):
                fullLinePoints = []
                j = 0
                while True:
                    ptTemp1 = Point3D(xStartDegree + j / float(60), ptOut0.get_Y())
                    if ptTemp1.get_X() >= self.parametersPanel.pnlUR.Point3d.get_X() or ptTemp1.get_X() <= self.parametersPanel.pnlLL.Point3d.get_X():
                        break
                    ptTemp1 = Point3D(xStartDegree + j / float(60), yStartDegree + i / float(60))
                    if define._units == QGis.Meters:
                        ptTemp1 = QgisHelper.CrsTransformPoint(ptTemp1.get_X(), ptTemp1.get_Y(), define._latLonCrs, define._xyCrs)
                    fullLinePoints.append(ptTemp1)
                    j += 1
                if define._units == QGis.Meters:
                    ptTemp0 = QgisHelper.CrsTransformPoint(ptTemp0.get_X(), ptTemp0.get_Y(), define._latLonCrs, define._xyCrs)
                fullLinePoints.insert(0, ptTemp0)

                ptTemp0 = Point3D(ptOut3.get_X(), yStartDegree + i / float(60))
                if define._units == QGis.Meters:
                    ptTemp0 = QgisHelper.CrsTransformPoint(ptTemp0.get_X(), ptTemp0.get_Y(), define._latLonCrs, define._xyCrs)
                fullLinePoints.append(ptTemp0)

                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, fullLinePoints)
            i += 1
            yStartMinuteInt += 1

        i = 0
        while True:
            if xStartMinuteInt == 60:
                xStartDegreeInt += 1
                xStartMinuteInt = 0
            ptTemp0 = Point3D(xStartDegree + i / float(60), ptOut0.get_Y())
            if ptTemp0.get_X() >= self.parametersPanel.pnlUR.Point3d.get_X() or ptTemp0.get_X() <= self.parametersPanel.pnlLL.Point3d.get_X():
                break
            if (majorFullFlag and xStartMinuteInt % majorLinesEvery == 0) or (intermediaFullFlag and xStartMinuteInt % intermediaLinesEvery == 0) or (minFullFlag and xStartMinuteInt % minLinesEvery == 0):
                fullLinePoints = []
                j = 0
                while True:
                    ptTemp1 = Point3D(ptOut0.get_X(), xStartDegree + j / float(60))
                    if ptTemp1.get_Y() >= self.parametersPanel.pnlUR.Point3d.get_Y() or ptTemp1.get_Y() <= self.parametersPanel.pnlLL.Point3d.get_Y():
                        break
                    ptTemp1 = Point3D(xStartDegree + i / float(60), yStartDegree + j / float(60))
                    if define._units == QGis.Meters:
                        ptTemp1 = QgisHelper.CrsTransformPoint(ptTemp1.get_X(), ptTemp1.get_Y(), define._latLonCrs, define._xyCrs)
                    fullLinePoints.append(ptTemp1)
                    j += 1
                if define._units == QGis.Meters:
                    ptTemp0 = QgisHelper.CrsTransformPoint(ptTemp0.get_X(), ptTemp0.get_Y(), define._latLonCrs, define._xyCrs)
                fullLinePoints.insert(0, ptTemp0)

                ptTemp0 = Point3D(xStartDegree + i / float(60), ptOut1.get_Y())
                if define._units == QGis.Meters:
                    ptTemp0 = QgisHelper.CrsTransformPoint(ptTemp0.get_X(), ptTemp0.get_Y(), define._latLonCrs, define._xyCrs)
                fullLinePoints.append(ptTemp0)

                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, fullLinePoints)
            i += 1
            xStartMinuteInt += 1



        palSetting = QgsPalLayerSettings()
        palSetting.readFromLayer(constructionLayer)
        palSetting.enabled = True
        palSetting.fieldName = "Caption"
        palSetting.isExpression = True
        palSetting.placement = QgsPalLayerSettings.Line
        palSetting.placementFlags = QgsPalLayerSettings.Underline

        # palSetting.Rotation = Unit.ConvertRadToDeg(MathHelper.smethod_4(entity_0.rotation))
        palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, str(int(self.parametersPanel.pnlTextHeight.Value)), "")
        palSetting.writeToLayer(constructionLayer)


        self.resultLayerList = [constructionLayer]
        QgisHelper.appendToCanvas(define._canvas, self.resultLayerList, self.surfaceType)
        QgisHelper.zoomToLayers(self.resultLayerList)






    def btnPicArea_Click(self):
        selectMapTool = SelectRect(define._canvas)
        define._canvas.setMapTool(selectMapTool)
        self.connect(selectMapTool, SIGNAL("resultPoints"), self.resultPoints)

    def resultPoints(self, startPoint, endPoint):
        ptLL = None
        ptUR = None
        leftX = None
        lowerY = None
        upperY = None
        if startPoint.x() < endPoint.x():
            leftX = startPoint.x()
            rightX = endPoint.x()
        else:
            leftX = endPoint.x()
            rightX = startPoint.x()
        if startPoint.y() < endPoint.y():
            lowerY = startPoint.y()
            upperY = endPoint.y()
        else:
            lowerY = endPoint.y()
            upperY = startPoint.y()
        ptLL = Point3D(leftX, lowerY)
        ptUR = Point3D(rightX, upperY)
        self.parametersPanel.pnlUR.Point3d = ptUR
        self.parametersPanel.pnlLL.Point3d = ptLL

        pass

    def method_30(self):
        self.parametersPanel.chbMultiline.Visible = self.parametersPanel.cmbLatFormat.SelectedIndex == 0
        self.parametersPanel.pnlMajorLinesTickLength.Visible = self.parametersPanel.cmbMajorLines.SelectedIndex == 1
        self.parametersPanel.txtIntermediateLinesEvery.Visible = self.parametersPanel.cmbIntermediateLines.SelectedIndex != 0
        self.parametersPanel.pnlIntermediateLinesTickLength.Visible = self.parametersPanel.cmbIntermediateLines.SelectedIndex == 2
        self.parametersPanel.txtMinorLinesEvery.Visible = self.parametersPanel.cmbMinorLines.SelectedIndex != 0
        self.parametersPanel.pnlMinorLinesTickLength.Visible = self.parametersPanel.cmbMinorLines.SelectedIndex == 2
    def method_31(self):
        self.method_30()
    def method_35(self, constructLayer, polyline_0, point3d_0, point3d_1, point3d_2, double_0, bool_0, chartingGridLinesCategory_0, point3d_3, point3d_4, double_1):
        # Degrees degree
        # Degrees degree1
        # Degrees degree2
        # Degrees degree3
        # double num
        # double num1
        # Degrees degree4
        # Degrees degree5
        # Degrees degree6
        # Degrees degree7
        # double num2
        # double num3
        # Degrees degree8
        # Degrees degree9
        # Degrees degree10
        # Degrees degree11
        # double num4
        # double num5
        # Degrees degree12
        # Degrees degree13
        # Degrees degree14
        # Degrees degree15
        # double num6
        # double num7
        # Degrees degree16
        # Degrees degree17
        # Degrees degree18
        # Degrees degree19
        # double num8
        # double num9
        # Degrees degree20
        # Degrees degree21
        # Degrees degree22
        # Degrees degree23
        # double num10
        # double num11
        turnDirection = MathHelper.smethod_63(MathHelper.getBearing(point3d_0, point3d_1), MathHelper.getBearing(point3d_1, point3d_2), AngleUnits.Radians)
        flag = True
        num12 = 0
        if (turnDirection != TurnDirection.Nothing):
            flag = False
            num12 = MathHelper.smethod_60(point3d_0, point3d_1, point3d_2)
        point3d0 = [point3d_0, point3d_2]
        polyline = PolylineArea(point3d0)
        polyline.SetBulgeAt(0, num12)
        point3dCollection = Point3dCollection()
        polyline_0.IntersectWith(polyline, 2, point3dCollection)
        if (point3dCollection.get_Count() != 2):
            return
        point3d_0 = point3dCollection.get_Item(0)
        point3d_2 = point3dCollection.get_Item(1)
        if (not bool_0):
            if (chartingGridLinesCategory_0 == ChartingGridLinesCategory.Major):
                if (self.cmbMajorLines.SelectedIndex != 0):
                    self.method_36(constructLayer, point3d_0, MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_2), self.parametersPanel.pnlMajorLinesTickLength.Value.Milimeters * double_1), point3d_3, point3d_4, False)
                    self.method_36(constructLayer, point3d_2, MathHelper.distanceBearingPoint(point3d_2, MathHelper.getBearing(point3d_2, point3d_0), self.parametersPanel.pnlMajorLinesTickLength.Value.Milimeters * double_1), point3d_3, point3d_4, False)
                elif (not flag):
                    result0, degree12, degree13 = Geo.smethod_2(point3d_0.get_X(), point3d_0.get_Y())
                    if (not result0):
                        QMessageBox.warning(self, "Warning", "Geo Error")
                        return
                        # throw new Exception(Geo.LastError)
                    result1, degree14, degree15 =  Geo.smethod_2(point3d_2.get_X(), point3d_2.get_Y())
                    if (not result1):
                        QMessageBox.warning(self, "Warning", "Geo Error")
                        return
                        # throw new Exception(Geo.LastError)
                    result2, num6, num7 = Geo.smethod_3(Degrees.smethod_1(min(degree12.Value, degree14.Value) + math.fabs(max(degree12.Value, degree14.Value) - min(degree12.Value, degree14.Value)) / 2), Degrees.smethod_5(double_0))
                    if (not result2):
                        QMessageBox.warning(self, "Warning", "Geo Error")
                        return
                        # throw new Exception(Geo.LastError)
                    point3d_1 = Point3D(num6, num7, 0)
                    point3dArray = [point3d_0, point3d_2]
                    polyline = PolylineArea(point3dArray)
                    polyline.SetBulgeAt(0, MathHelper.smethod_60(point3d_0, point3d_1, point3d_2))
                    AcadHelper.smethod_18(polyline, constructLayer)
                else:
                    AcadHelper.smethod_18([point3d_0, point3d_2], constructLayer)
                self.method_37(constructLayer, point3d_0, double_0, MathHelper.getBearing(point3d_0, point3d_2), point3d_3, point3d_4, False, double_1)
                self.method_37(constructLayer, point3d_2, double_0, MathHelper.getBearing(point3d_2, point3d_0), point3d_3, point3d_4, False, double_1)
                return
            if (chartingGridLinesCategory_0 == ChartingGridLinesCategory.Intermediate):
                if (self.parametersPanel.cmbIntermediateLines.SelectedIndex != 1):
                    self.method_36(constructLayer, point3d_0, MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_2), self.pnlIntermediateLinesTickLength.Value * double_1), point3d_3, point3d_4, False)
                    self.method_36(constructLayer, point3d_2, MathHelper.distanceBearingPoint(point3d_2, MathHelper.getBearing(point3d_2, point3d_0), self.pnlIntermediateLinesTickLength.Value * double_1), point3d_3, point3d_4, False)
                    return
                if (flag):
                    AcadHelper.smethod_18([point3d_0, point3d_2], constructLayer)
                    return
                result3, degree16, degree17 = Geo.smethod_2(point3d_0.get_X(), point3d_0.get_Y())
                if (not result3):
                    QMessageBox.warning(self, "Warning", "Geo Error")
                    return
                    # throw new Exception(Geo.LastError)
                result4, degree18, degree19 = Geo.smethod_2(point3d_2.get_X(), point3d_2.get_Y())
                if (not result4):
                    QMessageBox.warning(self, "Warning", "Geo Error")
                    return
                    # throw new Exception(Geo.LastError)
                result5, num8, num9 = Geo.smethod_3(Degrees.smethod_1(min(degree16.Value, degree18.Value) + math.fabs(max(degree16.Value, degree18.Value) - min(degree16.Value, degree18.Value)) / 2), Degrees.smethod_5(double_0))
                if (not result5):
                    QMessageBox.warning(self, "Warning", "Geo Error")
                    return
                    # throw new Exception(Geo.LastError)
                point3d_1 = Point3D(num8, num9, 0)
                point3d01 = [point3d_0, point3d_2 ]
                polyline = PolylineArea(point3d01)
                polyline.SetBulgeAt(0, MathHelper.smethod_60(point3d_0, point3d_1, point3d_2))
                AcadHelper.smethod_18(polyline, constructLayer)
                return
            if (self.parametersPanel.cmbMinorLines.SelectedIndex != 1):
                self.method_36(constructLayer, point3d_0, MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_2), self.parametersPanel.pnlMinorLinesTickLength.Value.Milimeters * double_1), point3d_3, point3d_4, False)
                self.method_36(constructLayer, point3d_2, MathHelper.distanceBearingPoint(point3d_2, MathHelper.getBearing(point3d_2, point3d_0), self.parametersPanel.pnlMinorLinesTickLength.Value.Milimeters * double_1), point3d_3, point3d_4, False)
                return
            if (flag):
                AcadHelper.smethod_18([point3d_0, point3d_2], constructLayer)
                return
            result6, degree20, degree21 = Geo.smethod_2(point3d_0.get_X(), point3d_0.get_Y())
            if (not result6):
                QMessageBox.warning(self, "Warning", "Geo Error")
                return
                # throw new Exception(Geo.LastError)
            result7, degree22, degree23 = Geo.smethod_2(point3d_2.get_X(), point3d_2.get_Y())
            if (not result7):
                QMessageBox.warning(self, "Warning", "Geo Error")
                return
                # throw new Exception(Geo.LastError)
            result8, num10, num11 = Geo.smethod_3(Degrees.smethod_1(min(degree20.Value, degree22.Value) + math.fabs(max(degree20.Value, degree22.Value) - min(degree20.Value, degree22.Value)) / 2), Degrees.smethod_5(double_0))
            if (not result8):
                QMessageBox.warning(self, "Warning", "Geo Error")
                return
                # throw new Exception(Geo.LastError)
            point3d_1 = Point3D(num10, num11, 0)
            point3dArray1 = [point3d_0, point3d_2 ]
            polyline = PolylineArea(point3dArray1)
            polyline.SetBulgeAt(0, MathHelper.smethod_60(point3d_0, point3d_1, point3d_2))
            AcadHelper.smethod_18(polyline, constructLayer)
            return
        if (chartingGridLinesCategory_0 == ChartingGridLinesCategory.Major):
            if (self.parametersPanel.cmbMajorLines.SelectedIndex != 0):
                self.method_36(constructLayer, point3d_0, MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_2), self.parametersPanel.pnlMajorLinesTickLength.Value.Milimeters * double_1), point3d_3, point3d_4, True)
                self.method_36(constructLayer, point3d_2, MathHelper.distanceBearingPoint(point3d_2, MathHelper.getBearing(point3d_2, point3d_0), self.parametersPanel.pnlMajorLinesTickLength.Value.Milimeters * double_1), point3d_3, point3d_4, True)
            elif (not flag):
                result9, degree, degree1 = Geo.smethod_2(point3d_0.get_X(), point3d_0.get_Y())
                if (not result9):
                    QMessageBox.warning(self, "Warning", "Geo Error")
                    return
                    # throw new Exception(Geo.LastError
                result10, degree2, degree3 = Geo.smethod_2(point3d_2.get_X(), point3d_2.get_Y())
                if (not result10):
                    QMessageBox.warning(self, "Warning", "Geo Error")
                    return
                    # throw new Exception(Geo.LastError)
                num13 = min(degree1.Value, degree3.Value) + math.fabs(max(degree1.Value, degree3.Value) - min(degree1.Value, degree3.Value)) / 2
                result11, num, num1 = Geo.smethod_3(Degrees.smethod_1(double_0), Degrees.smethod_5(num13))
                if (not result11):
                    QMessageBox.warning(self, "Warning", "Geo Error")
                    return
                    # throw new Exception(Geo.LastError)
                point3d_1 = Point3D(num, num1, 0)
                point3d02 = [point3d_0, point3d_2 ]
                polyline = PolylineArea(point3d02)
                polyline.SetBulgeAt(0, MathHelper.smethod_60(point3d_0, point3d_1, point3d_2))
                AcadHelper.smethod_18(polyline, constructLayer)
            else:
                AcadHelper.smethod_18([point3d_0, point3d_2], constructLayer)
            self.method_37(constructLayer, point3d_0, double_0, MathHelper.getBearing(point3d_0, point3d_2), point3d_3, point3d_4, True, double_1)
            self.method_37(constructLayer, point3d_2, double_0, MathHelper.getBearing(point3d_2, point3d_0), point3d_3, point3d_4, True, double_1)
            return
        if (chartingGridLinesCategory_0 == ChartingGridLinesCategory.Intermediate):
            if (self.parametersPanel.cmbIntermediateLines.SelectedIndex != 1):
                self.method_36(constructLayer, point3d_0, MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_2), self.pnlIntermediateLinesTickLength.Value * double_1), point3d_3, point3d_4, True)
                self.method_36(constructLayer, point3d_2, MathHelper.distanceBearingPoint(point3d_2, MathHelper.getBearing(point3d_2, point3d_0), self.pnlIntermediateLinesTickLength.Value * double_1), point3d_3, point3d_4, True)
                return
            if (flag):
                AcadHelper.smethod_18([point3d_0, point3d_2], constructLayer)
                return
            result12, degree4, degree5 = Geo.smethod_2(point3d_0.get_X(), point3d_0.get_Y())
            if (not result12):
                QMessageBox.warning(self, "Warning", "Geo Error")
                return
                # throw new Exception(Geo.LastError)
            result13, degree6, degree7 = Geo.smethod_2(point3d_2.get_X(), point3d_2.get_Y())
            if (not result13):
                QMessageBox.warning(self, "Warning", "Geo Error")
                return
                # throw new Exception(Geo.LastError)
            num14 = min(degree5.Value, degree7.Value) + math.fabs(max(degree5.Value, degree7.Value) - min(degree5.Value, degree7.Value)) / 2
            result14, num2, num3 = Geo.smethod_3(Degrees.smethod_1(double_0), Degrees.smethod_5(num14))
            if (not result14):
                QMessageBox.warning(self, "Warning", "Geo Error")
                return
                # throw new Exception(Geo.LastError)
            point3d_1 = Point3D(num2, num3, 0)
            point3dArray2 = [point3d_0, point3d_2 ]
            polyline = PolylineArea(point3dArray2)
            polyline.SetBulgeAt(0, MathHelper.smethod_60(point3d_0, point3d_1, point3d_2))
            AcadHelper.smethod_18(polyline, constructLayer)
            return
        if (self.parametersPanel.cmbMinorLines.SelectedIndex != 1):
            self.method_36(constructLayer, point3d_0, MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_2), self.parametersPanel.pnlMinorLinesTickLength.Value.Milimeters * double_1), point3d_3, point3d_4, True)
            self.method_36(constructLayer, point3d_2, MathHelper.distanceBearingPoint(point3d_2, MathHelper.getBearing(point3d_2, point3d_0), self.parametersPanel.pnlMinorLinesTickLength.Value.Milimeters * double_1), point3d_3, point3d_4, True)
            return
        if (flag):
            AcadHelper.smethod_18([point3d_0, point3d_2], constructLayer)
            return
        result15, degree8, degree9 = Geo.smethod_2(point3d_0.get_X(), point3d_0.get_Y())
        if (not result15):
            QMessageBox.warning(self, "Warning", "Geo Error")
            return
            # throw new Exception(Geo.LastError)
        result16, degree10, degree11 = Geo.smethod_2(point3d_2.get_X(), point3d_2.get_Y())
        if (not result16):
            QMessageBox.warning(self, "Warning", "Geo Error")
            return
            # throw new Exception(Geo.LastError)
        num15 = min(degree9.Value, degree11.Value) + math.fabs(max(degree9.Value, degree11.Value) - min(degree9.Value, degree11.Value)) / 2
        result17, num4, num5 = Geo.smethod_3(Degrees.smethod_1(double_0), Degrees.smethod_5(num15))
        if (not result17):
            QMessageBox.warning(self, "Warning", "Geo Error")
            return
            # throw new Exception(Geo.LastError)
        point3d_1 = Point3D(num4, num5, 0)
        point3d03 = [point3d_0, point3d_2 ]
        polyline = PolylineArea(point3d03)
        polyline.SetBulgeAt(0, MathHelper.smethod_60(point3d_0, point3d_1, point3d_2))
        AcadHelper.smethod_18(polyline, constructLayer)
    
    def method_36(self, constructLayer, point3d_0, point3d_1, point3d_2, point3d_3, bool_0):
        if (bool_0):
            if (MathHelper.smethod_99(point3d_0.get_X(), point3d_2.get_X(), 1E-05) or MathHelper.smethod_99(point3d_1.get_X(), point3d_2.get_X(), 1E-05) or MathHelper.smethod_99(point3d_0.get_X(), point3d_3.get_X(), 1E-05) or MathHelper.smethod_99(point3d_1.get_X(), point3d_3.get_X(), 1E-05)):
                AcadHelper.smethod_18([point3d_0, point3d_1], constructLayer)
                return
        elif (MathHelper.smethod_99(point3d_0.get_Y(), point3d_2.get_Y(), 1E-05) or MathHelper.smethod_99(point3d_1.get_Y(), point3d_2.get_Y(), 1E-05) or MathHelper.smethod_99(point3d_0.get_Y(), point3d_3.get_Y(), 1E-05) or MathHelper.smethod_99(point3d_1.get_Y(), point3d_3.get_Y(), 1E-05)):
            AcadHelper.smethod_18([point3d_0, point3d_1], constructLayer)
    
    def method_37(self, constructLayer, point3d_0, double_0, double_1, point3d_1, point3d_2, bool_0, double_2):
        flag = False if(not self.parametersPanel.chbMultiline.Checked) else self.parametersPanel.chbMultiline.Visible
        value = self.parametersPanel.pnlTextHeight.Value.Milimeters * double_2
        if (not bool_0):
            str0 = "E"
            if (double_0 < 0):
                str0 = "W"
            double_0 = math.fabs(double_0)
            str1 = ""
            for case in switch (self.parametersPanel.pnlLonFormat.SelectedIndex):
                if case(0):
                    str1 = "{0:00}{1:00}".format(math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60)
                    break
                elif case(1):
                    str1 = "{0:00}° {1:00}'".format(math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60)
                    break
                elif case(2):
                    str1 = "{0:00}{1:00}{2}".format(math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60, str0)
                    break
                elif case(3):
                    str1 = "{0:00}° {1:00}' {2}".format(math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60, str)
                    break
                elif case(4):
                    str1 = "{0}{1:00}{2:00}".format(str0, math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60)
                    break
                elif case(5):
                    str1 = "{0} {1:00}° {2:00}'".format(str0, math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60)
                    break
            if (MathHelper.smethod_99(point3d_0.get_Y(), point3d_1.get_Y(), 0.0001)):
                point3d_0 = MathHelper.distanceBearingPoint(point3d_0, 0, value / 2)
                AcadHelper.smethod_18(AcadHelper.smethod_142(str1, point3d_0, value, 8), constructLayer)
                return
            if (MathHelper.smethod_99(point3d_0.get_Y(), point3d_2.get_Y(), 0.0001)):
                point3d_0 = MathHelper.distanceBearingPoint(point3d_0, 3.14159265358979, value / 2)
                AcadHelper.smethod_18(AcadHelper.smethod_142(str1, point3d_0, value, 2), constructLayer)
        else:
            if (not MathHelper.smethod_136(double_1, AngleUnits.Radians)):
                double_1 = double_1 - 3.14159265358979
            str2 = "N"
            if (double_0 < 0):
                str2 = "S"
            double_0 = math.fabs(double_0)
            str3 = ""
            for case in switch (self.parametersPanel.cmbLatFormat.SelectedIndex):
                if case(0):
                    if (not flag):
                        str3 = "{0:00}{1:00}".format(math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60)
                        break
                    else:
                        str3 = "{0:00}\\P{1:00}".format(math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60)
                        break
                elif case(1):
                    if (not flag):
                        str3 = "{0:00}° {1:00}'".format(math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60)
                        break
                    else:
                        str3 = "{0:00}°\\P{1:00}'".format(math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60)
                        break
                elif case(2):
                    str3 = "{0:00}{1:00}{2}".format(math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60, str2)
                    break
                elif case(3):
                    str3 = "{0:00}° {1:00}' {2}".format(math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60, str2)
                    break
                elif case(4):
                    str3 = "{0}{1:00}{2:00}".format(str2, math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60)
                    break
                elif case(5):
                    str3 = "{0} {1:00}° {2:00}'".format(str2, math.trunc(double_0), (double_0 - math.trunc(double_0)) * 60)
                    break
            if (MathHelper.smethod_99(point3d_0.get_X(), point3d_1.get_X(), 0.0001)):
                if (flag):
                    point3d_0 = MathHelper.distanceBearingPoint(point3d_0, 1.5707963267949, value / 4)
                    AcadHelper.smethod_18(AcadHelper.smethod_142(str3, point3d_0, value * double_2, 4), constructLayer)
                    return
                point3d_0 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, 0, value / 4), 1.5707963267949, value / 4)
                mText = AcadHelper.smethod_142(str3, point3d_0, value, 7)
                mText.set_Rotation(7.85398163397448 - double_1)
                AcadHelper.smethod_18(mText, constructLayer)
                return
            if (MathHelper.smethod_99(point3d_0.get_X(), point3d_2.get_X(), 0.0001)):
                if (flag):
                    point3d_0 = MathHelper.distanceBearingPoint(point3d_0, 4.71238898038469, value / 1.5 * 3.5)
                    AcadHelper.smethod_18(AcadHelper.smethod_142(str3, point3d_0, value, 4), constructLayer)
                    return
                point3d_0 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, 0, value / 4), 4.71238898038469, value / 4)
                mText1 = AcadHelper.smethod_142(str3, point3d_0, value, 9)
                mText1.set_Rotation(7.85398163397448 - double_1)
                AcadHelper.smethod_18(mText1, constructLayer)
                return

class SelectRect(QgsMapTool):

    def __init__(self, canvas):
        self.mCanvas = canvas
        # self.areaType = areaType
        QgsMapTool.__init__(self, canvas)
        self.mCursor = Qt.ArrowCursor
        self.mRubberBand = None
        self.mDragging = False
        self.mSelectRect = QRect()
        self.mRubberBandResult = None
        self.mSnapper = QgsMapCanvasSnapper(canvas)
        self.lineCount = 0
        self.resultGeomList = []
        self.geomList = []
        self.area = None
        self.isFinished = False

        self.startPoint = None
        self.endPoint = None


    def canvasPressEvent(self, e):
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        self.mSelectRect.setRect( 0, 0, 0, 0 )
        self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
        self.startPoint, self.pointID, self.layer= self.snapPoint(e.pos())

    def canvasMoveEvent(self, e):
        if ( e.buttons() != Qt.LeftButton ):
            return
        if ( not self.mDragging ):
            self.mDragging = True
            self.mSelectRect.setTopLeft( e.pos() )
        self.mSelectRect.setBottomRight( e.pos() )
        QgsMapToolSelectUtils.setRubberBand( self.mCanvas, self.mSelectRect,self.mRubberBand )

    def canvasReleaseEvent(self, e):
        self.endPoint, self.pointID, self.layer = self.snapPoint(e.pos())


        self.mRubberBand.reset( QGis.Polygon )
        del self.mRubberBand
        self.mRubberBand = None
        self.mDragging = False
        self.emit(SIGNAL("resultPoints"), self.startPoint, self.endPoint)
    def snapPoint(self, p, bNone = False):
        if define._snapping == False:
            return (define._canvas.getCoordinateTransform().toMapCoordinates( p ), None, None)
        snappingResults = self.mSnapper.snapToBackgroundLayers( p )
        if ( snappingResults[0] != 0 or len(snappingResults[1]) < 1 ):

            if bNone:
                return (None, None, None)
            else:
                return (define._canvas.getCoordinateTransform().toMapCoordinates( p ), None, None)
        else:
            return (snappingResults[1][0].snappedVertex, snappingResults[1][0].snappedAtGeometry, snappingResults[1][0].layer)

