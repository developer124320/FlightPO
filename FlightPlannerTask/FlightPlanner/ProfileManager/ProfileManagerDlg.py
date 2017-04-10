# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import SurfaceTypes, DistanceUnits, Point3D, Point3dCollection
from FlightPlanner.ProfileManager.ui_ProfileManager import Ui_ProfileManager
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.helpers import MathHelper, Unit, Distance
from FlightPlanner.Captions import Captions
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Prompts import Prompts
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.AcadHelper import AcadHelper
from map.tools import QgsMapToolSelectUtils
from Type.Geometry import Line

from PyQt4.QtCore import SIGNAL, QString, QObject, Qt, QRect
from PyQt4.QtGui import QColor, QIcon, QPixmap, QMenu, QLabel
from qgis.core import QGis, QgsVectorLayer, QgsGeometry, QgsVectorFileWriter, QgsFeature, QgsRectangle
from qgis.gui import  QgsMapTool, QgsRubberBand, QgsMapToolPan, QgsMapCanvasSnapper
import define, math

class ProfileManagerDlg(FlightPlanBaseDlg):
    constructionLayer = None
    REG_APP_NAME = "PHXPROFILEMANAGER";
    polylinePoints = [];
    ang = 0.0;
    angop = 0.0

    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("PathTerminatorsDlg")
        self.surfaceType = SurfaceTypes.ProfileManager
        self.selectedRow = None
        self.editingModelIndex = None

        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.ProfileManager)
        self.resize(600, 650)
        QgisHelper.matchingDialogSize(self, 650, 650)
        self.surfaceList = None
        self.manualPolygon = None

        # d = dict()
        # d = dict(y='d', s= 'df')
        # for name, data in d:
        #     n= name;
        #     c = data
        #     pass
        # s = d['s']

        self.pointLayer = None
        self.lineLayer = None
        self.proceedClicked = False
        mapUnits = define._canvas.mapUnits()
        ProfileManagerDlg.constructionLayer = AcadHelper.createVectorLayer(self.surfaceType + " Result")

    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        # self.ui.btnConstruct.setVisible(False)
        # self.ui.btnEvaluate.setVisible(False)
        # self.ui.btnPDTCheck.setVisible(False)
        # self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        self.ui.tabCtrlGeneral.removeTab(1)

        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/btnImage/locate.png")), QIcon.Normal, QIcon.Off)
        self.ui.btnPDTCheck.setIcon(icon)

        self.ui.btnEvaluate.setToolTip("Proceed")
        self.ui.btnPDTCheck.setToolTip("Locate")

#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)
    def btnPDTCheck_Click(self):
        define._messageLabel.setText(Prompts.SELECT_PROFILE_MANAGER_OBSTACLES)
        selectLineMapTool = SelectLine(define._canvas, Prompts.SELECT_PROFILE_MANAGER_OBSTACLES, self)
        define._canvas.setMapTool(selectLineMapTool)
        QObject.connect(selectLineMapTool, SIGNAL("outputResult"), self.selectLineResult)
        a = define._canvas.focusPolicy()
        self.hide()
        # define._canvas.setFocus()
    def selectLineResult(self, selectedFeatures):
        mapUnits = define._units
        layer = AcadHelper.createVectorLayer("result Arrow")
        point3dCollection0 = Point3dCollection()
        for feat in selectedFeatures:
            try:
                xDataName = feat.attribute("XDataName").toString()

                if xDataName != "":
                    xDataX = float(feat.attribute("XDataPointX").toString())
                    xDataY = float(feat.attribute("XDataPointY").toString())
                    point3dCollection0.Add(Point3D(xDataX, xDataY))
            except:
                pass
        point3dCollection = Point3dCollection.smethod_146(point3dCollection0)
        origin = None
        maxPoint = None
        num = 0;
        for point3d in point3dCollection:
            boundingBox = AcadHelper.smethod_144(point3d, layer).boundingBox();

            if (num != 0):
                origin = MathHelper.smethod_178(origin, Point3D(boundingBox.xMinimum(), boundingBox.yMinimum()));
                maxPoint = MathHelper.smethod_180(maxPoint, Point3D(boundingBox.xMaximum(), boundingBox.yMaximum()))
            else:
                origin = Point3D(boundingBox.xMinimum(), boundingBox.yMinimum())
                maxPoint = Point3D(boundingBox.xMaximum(), boundingBox.yMaximum())
            num += 1;
        if len(point3dCollection) != 0:
            QgisHelper.appendToCanvas(define._canvas, [layer], self.surfaceType)
            extent = QgsRectangle(origin, maxPoint)

            centerPoint = Point3D((origin.get_X() + maxPoint.get_X()) / 2, (origin.get_Y() + maxPoint.get_Y()) / 2)
            QgisHelper.zoomExtent(centerPoint, extent, 2)
        # define._canvas.zoomWithCenter((origin.get_X() + maxPoint.get_X()) / 2, (origin.get_Y() + maxPoint.get_Y()) / 2, True)



    def btnEvaluate_Click(self):   #### ---------------  Proceed  -------------------###
        ProfileManagerDlg.constructionLayer = AcadHelper.createVectorLayer(self.surfaceType + " Result")

        if (self.parametersPanel.chbPolyline.isChecked()):
            ProfileManagerDlg.polylinePoints = [];
        # ProfileManagerDlg.space = AcadHelper.smethod_32(1, ProfileManagerDlg.transaction, activeDocument.get_Database());
        if (self.parametersPanel.cmbBaseOrientation.SelectedIndex != 1):
            ProfileManagerDlg.ang = 1.5707963267949;
            ProfileManagerDlg.angop = 4.71238898038469;
        else:
            ProfileManagerDlg.ang = 4.71238898038469;
            ProfileManagerDlg.angop = 1.5707963267949;
        # RegAppTable obj = (RegAppTable)ProfileManagerDlg.transaction.GetObject(activeDocument.get_Database().get_RegAppTableId(), 0);
        # if (!obj.Has("PHXPROFILEMANAGER"))
        # {
        #     RegAppTableRecord regAppTableRecord = new RegAppTableRecord();
        #     regAppTableRecord.set_Name("PHXPROFILEMANAGER");
        #     obj.UpgradeOpen();
        #     obj.Add(regAppTableRecord);
        #     obj.DowngradeOpen();
        #     ProfileManagerDlg.transaction.AddNewlyCreatedDBObject(regAppTableRecord, true);
        # }
        self.input1Evaluator = None;
        if self.parametersPanel.pnlMode.SelectedIndex == 1:
            self.input1Evaluator = Input1Evaluator(self.parametersPanel.pnlBasePoint.Point3d, self.parametersPanel.pnlThrDer.Point3d, self.parametersPanel.pnlOutbound.Value, self.parametersPanel.chbUseTolerance.isChecked(), self.parametersPanel.chbWriteName.isChecked(), self.parametersPanel.pnlTextHeight.Value, self.parametersPanel.chbPolyline.isChecked());

        elif self.parametersPanel.pnlMode.SelectedIndex == 2:
            self.input1Evaluator = Input2Evaluator(self.parametersPanel.pnlBasePoint.Point3d, self.parametersPanel.pnlThrDer.Point3d, self.parametersPanel.pnlOutbound.Value, self.parametersPanel.chbUseTolerance.isChecked(), self.parametersPanel.chbWriteName.isChecked(), self.parametersPanel.pnlTextHeight.Value, self.parametersPanel.pnlEtp.Point3d, self.parametersPanel.chbPolyline.isChecked());

        elif self.parametersPanel.pnlMode.SelectedIndex == 3:
            define._messageLabel.setText(Prompts.SELECT_ALTITUDE_BOUNDARY_LINE)
            # base.method_26(PHX.Programs.HideReason.DrawingInteraction);
            selectTool = AcadHelper.smethod_102(Prompts.SELECT_ALTITUDE_BOUNDARY_LINE, None, None, self);
            QObject.connect(selectTool, SIGNAL("AcadHelper_Smethod_102_Event"), self.acadHelper_Smethod_102_Event)
            self.proceedClicked = True
            define._canvas.setToolTip(Prompts.SELECT_ALTITUDE_BOUNDARY_LINE)
            self.hide()

            return
            # if (line != None):
            #     input1Evaluator = ProfileManagerDlg.Input3Evaluator(self.parametersPanel.pnlBasePoint.Point3d, self.parametersPanel.pnlBaseAltitude.Value, self.parametersPanel.pnlThrDer.Point3d, self.parametersPanel.pnlOutbound.Value, self.parametersPanel.chbUseTolerance.isChecked(), self.parametersPanel.chbWriteName.isChecked(), self.parametersPanel.pnlTextHeight.Value, self.parametersPanel.pnlHASP.Value, self.parametersPanel.pnlTA.Value, self.parametersPanel.pnlClimbGradient.Value, self.parametersPanel.chbMarkTA.isChecked(), self.parametersPanel.chbDeparture.isChecked(), line.get_StartPoint(), line.get_EndPoint(), self.parametersPanel.chbPolyline.isChecked());
            #     # AcadHelper.smethod_24(line);
            # else:
            #     # AcadHelper.smethod_1();
            #     # base.method_24();
            #     return;
        else:
            return;
        # self.obstaclesModel = ProfileManagerObstacles(input1Evaluator)
        self.manualEvent(1)
        self.proceedClicked = True


    def acadHelper_Smethod_102_Event(self, geom):
        if (geom != None):
            pointList = geom.asPolyline()
            self.input1Evaluator = Input3Evaluator(self.parametersPanel.pnlBasePoint.Point3d, self.parametersPanel.pnlBaseAltitude.Value, self.parametersPanel.pnlThrDer.Point3d, self.parametersPanel.pnlOutbound.Value, self.parametersPanel.chbUseTolerance.isChecked(), self.parametersPanel.chbWriteName.isChecked(), self.parametersPanel.pnlTextHeight.Value, self.parametersPanel.pnlHASP.Value, self.parametersPanel.pnlTA.Value, self.parametersPanel.pnlClimbGradient.Value, self.parametersPanel.chbMarkTA.isChecked(), self.parametersPanel.chbDeparture.isChecked(), pointList[0], pointList[1], self.parametersPanel.chbPolyline.isChecked());

            # define._messageLabel.setText("Create area that obstacles can be contained manually.")
            self.manualEvent(1)
    def outputResultMethod(self):
        self.manualPolygon = self.toolSelectByPolygon.polygonGeom
        mapUnits = define._units
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                constructLayer = QgsVectorLayer("polygon?crs=EPSG:32633", self.surfaceType, "memory")
            else:
                constructLayer = QgsVectorLayer("polygon?crs=EPSG:4326", self.surfaceType, "memory")
        else:
            constructLayer = QgsVectorLayer("polygon?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")
        shpPath = ""
        if define.obstaclePath != None:
            shpPath = define.obstaclePath
        elif define.xmlPath != None:
            shpPath = define.xmlPath
        else:
            shpPath = define.appPath
        er = QgsVectorFileWriter.writeAsVectorFormat(constructLayer, shpPath + "/" + QString(self.surfaceType).replace(" ", "") + ".shp", "utf-8", constructLayer.crs())
        constructLayer = QgsVectorLayer(shpPath + "/" + QString(self.surfaceType).replace(" ", "") + ".shp", self.surfaceType, "ogr")

        constructLayer.startEditing()
        feature = QgsFeature()
        feature.setGeometry(self.manualPolygon)
        pr = constructLayer.dataProvider()
        pr.addFeatures([feature])
        # constructLayer.addFeature(feature)
        constructLayer.commitChanges()
        QgisHelper.appendToCanvas(define._canvas, [constructLayer], self.surfaceType)


        self.obstaclesModel = ProfileManagerObstacles(self.input1Evaluator, self.manualPolygon)
        FlightPlanBaseDlg.btnEvaluate_Click(self)

        if (self.parametersPanel.chbPolyline.isChecked() and len(ProfileManagerDlg.polylinePoints) != 0):
            ProfileManagerDlg.polylinePoints.sort(self.Point3dsComparer)
            if (len(ProfileManagerDlg.polylinePoints) > 0):
                if (len(ProfileManagerDlg.polylinePoints) == 1):
                    point3d = self.parametersPanel.pnlBasePoint.Point3d;
                    value = self.parametersPanel.pnlBaseAltitude.Value;
                    point3d1 = MathHelper.distanceBearingPoint(point3d, 0, value.Metres);
                    ProfileManagerDlg.polylinePoints.insert(0, point3d1);

                # AcadHelper.smethod_18(AcadHelper.smethod_130(ProfileManagerDlg.polylinePoints), ProfileManagerDlg.constructionLayer);

                if define._mapCrs == None:
                    if mapUnits == QGis.Meters:
                        self.pointLayer = QgsVectorLayer("point?crs=EPSG:32633", "result points", "memory")
                    else:
                        self.pointLayer = QgsVectorLayer("point?crs=EPSG:4326", "result points", "memory")
                else:
                    self.pointLayer = QgsVectorLayer("point?crs=%s"%define._mapCrs.authid (), "result points", "memory")
                shpPath = ""
                if define.obstaclePath != None:
                    shpPath = define.obstaclePath
                elif define.xmlPath != None:
                    shpPath = define.xmlPath
                else:
                    shpPath = define.appPath
                er = QgsVectorFileWriter.writeAsVectorFormat(self.pointLayer, shpPath + "/" + "result points" + ".shp", "utf-8", self.pointLayer.crs())
                self.pointLayer = QgsVectorLayer(shpPath + "/" + "result points" + ".shp", "result points", "ogr")

                self.pointLayer.startEditing()
                for point in ProfileManagerDlg.polylinePoints:
                    feature = QgsFeature()
                    offset = 0.0
                    if define._units == QGis.Meters:
                        offset = 60
                    else:
                        offset = define._qgsDistanceArea.convertMeasurement (60, define._xyCrs, define._latLonCrs, False)
                    feature.setGeometry(QgsGeometry.fromPoint(Point3D(point.x(), point.y() + offset)))
                    pr = self.pointLayer.dataProvider()
                    pr.addFeatures([feature])
                    # self.pointLayer.addFeature(feature)
                self.pointLayer.commitChanges()

                if define._mapCrs == None:
                    if mapUnits == QGis.Meters:
                        self.lineLayer = QgsVectorLayer("linestring?crs=EPSG:32633", "result points line", "memory")
                    else:
                        self.lineLayer = QgsVectorLayer("linestring?crs=EPSG:4326", "result points line", "memory")
                else:
                    self.lineLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), "result points line", "memory")
                shpPath = ""
                if define.obstaclePath != None:
                    shpPath = define.obstaclePath
                elif define.xmlPath != None:
                    shpPath = define.xmlPath
                else:
                    shpPath = define.appPath
                er = QgsVectorFileWriter.writeAsVectorFormat(self.lineLayer, shpPath + "/" + "result points line" + ".shp", "utf-8", self.lineLayer.crs())
                self.lineLayer = QgsVectorLayer(shpPath + "/" + "result points line" + ".shp", "result points line", "ogr")

                self.lineLayer.startEditing()
                i = 0
                for point in ProfileManagerDlg.polylinePoints:
                    if i == 0:
                        i += 1
                        continue
                    feature = QgsFeature()
                    feature.setGeometry(QgsGeometry.fromPolyline([ProfileManagerDlg.polylinePoints[i-1], point]))
                    pr = self.lineLayer.dataProvider()
                    pr.addFeatures([feature])
                    # self.lineLayer.addFeature(feature)
                    i += 1
                self.lineLayer.commitChanges()




        if (len(ProfileManagerDlg.polylinePoints) != 0):
            ProfileManagerDlg.polylinePoints = []
    def manualEvent(self, index):
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        self.manualPolygon = None

        if index != 0:
            self.toolSelectByPolygon = RubberBandPolygon(define._canvas, self)
            define._canvas.setMapTool(self.toolSelectByPolygon)
            self.connect(self.toolSelectByPolygon, SIGNAL("outputResult"), self.outputResultMethod)
        else:
            self.mapToolPan = QgsMapToolPan(define._canvas)
            define._canvas.setMapTool(self.mapToolPan )

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        num = None
        num1 = None;
        percent = None;
        metres = None;
        percent1 = None;
        strS = "";
        if not self.proceedClicked:
            ProfileManagerDlg.constructionLayer = AcadHelper.createVectorLayer(self.surfaceType + " Result")



        point3d = self.parametersPanel.pnlBasePoint.Point3d;
        num2 = Unit.ConvertDegToRad(270);
        if (self.parametersPanel.cmbBaseOrientation.SelectedIndex != 0):
            num1 = Unit.ConvertDegToRad(180);
            num = 0;
        else:
            num = Unit.ConvertDegToRad(180);
            num1 = 0;
        metres1 = self.parametersPanel.pnlLength.Value.Metres;
        num3 = metres1 / 100;
        point3d1 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num1, metres1);
        line = QgsGeometry.fromPolyline([point3d, point3d1]);
        AcadHelper.smethod_19( line, ProfileManagerDlg.constructionLayer, 5);
        # dBPoint = new DBPoint(point3d);
        # AcadHelper.smethod_18(transaction, blockTableRecord, dBPoint, ProfileManagerDlg.constructionLayer);
        value = self.parametersPanel.pnlBaseAltitude.Value;
        point3d = MathHelper.distanceBearingPoint(point3d, 0, value.Metres);
        point3d1 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num1, metres1);
        line = QgsGeometry.fromPolyline([point3d, point3d1]);
        AcadHelper.smethod_18(line, ProfileManagerDlg.constructionLayer);
        point3d2 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num, 2 * num3);
        point3d3 = MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(450) - num2, 2 * num3);
        dBText = AcadHelper.smethod_140(Captions.RWY, point3d3, num3, 1, 2);
        AcadHelper.smethod_18(dBText, ProfileManagerDlg.constructionLayer);
        if (self.parametersPanel.chbMarkDistances.isChecked()):
            originalUnits = self.parametersPanel.pnlLength.Value.OriginalUnits();
            distance = self.parametersPanel.pnlLength.Value;
            num4 = None
            if self.parametersPanel.pnlLength.distanceUnit == DistanceUnits.M:
                num4 = distance.Metres
            elif self.parametersPanel.pnlLength.distanceUnit == DistanceUnits.NM:
                num4 = distance.NauticalMiles
            elif self.parametersPanel.pnlLength.distanceUnit == DistanceUnits.FT:
                num4 = distance.Feet
            elif self.parametersPanel.pnlLength.distanceUnit == DistanceUnits.KM:
                num4 = distance.Kilometres
            # num4 = double.Parse(distance.ToString());
            i = 1.0
            while i < num4:
            # for (i = 1; i < num4; i = i + 1)
                distance1 = Distance(i, originalUnits);
                point3d4 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num1, distance1.Metres);
                point3d5 = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(450) - num2, num3);
                line = QgsGeometry.fromPolyline([point3d4, point3d5]);
                AcadHelper.smethod_18(line, ProfileManagerDlg.constructionLayer);
                point3d5 = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(450) - num2, 2 * num3);
                dBText = AcadHelper.smethod_140(str(int(round(i))), point3d5, num3, 1, 2);
                AcadHelper.smethod_18(dBText, ProfileManagerDlg.constructionLayer);
                i += 1
            value1 = self.parametersPanel.pnlLength.Value;
            point3d6 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num1, value1.Metres);
            point3d7 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(450) - num2, num3);
            line = QgsGeometry.fromPolyline([point3d6, point3d7]);
            AcadHelper.smethod_18(line, ProfileManagerDlg.constructionLayer);
            point3d7 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(450) - num2, 2 * num3);
            value2 = self.parametersPanel.pnlLength.Value;
            dBText = AcadHelper.smethod_140(str(int(value2.NauticalMiles)), point3d7, num3, 1, 2);
            AcadHelper.smethod_18(dBText, ProfileManagerDlg.constructionLayer);
            point3d6 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num1, metres1 + 3 * num3);
            point3d7 = MathHelper.distanceBearingPoint(point3d6, Unit.ConvertDegToRad(450) - num2, num3);
            dBText = AcadHelper.smethod_137(DistanceUnits.ToString(originalUnits), point3d7, num3);
            if (self.parametersPanel.cmbBaseOrientation.SelectedIndex != 0):
                dBText.set_HorizontalMode(2);
            else:
                dBText.set_HorizontalMode(0);
            dBText.set_VerticalMode(2);
            dBText.set_AlignmentPoint(point3d7);
            AcadHelper.smethod_18(dBText, ProfileManagerDlg.constructionLayer);
        point3d8 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num2, 4 * num3);
        line = QgsGeometry.fromPolyline([point3d, point3d8]);
        AcadHelper.smethod_18(line, ProfileManagerDlg.constructionLayer);
        if (self.parametersPanel.pnlUsedFor.SelectedIndex == 0):
            point3d9 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num2, 5 * num3);
            dBText = AcadHelper.smethod_140(Captions.DER, point3d9, num3, 1, 2);
            AcadHelper.smethod_18(dBText, ProfileManagerDlg.constructionLayer);
            percent = self.parametersPanel.pnlPDG.Value / 100;
            percent1 = self.parametersPanel.pnlMOC.Value / 100;
            metres = 5;
            pDG = Captions.PDG;
            angleGradientSlope = self.parametersPanel.pnlPDG.Value;
            strS = "%s = %f"%(pDG, angleGradientSlope);
        elif (self.parametersPanel.pnlUsedFor.SelectedIndex != 1):
            num5 = Unit.ConvertDegToRad(self.parametersPanel.pnlGP.Value);
            percent = math.sin(num5) / math.cos(num5);
            metres = self.parametersPanel.pnlRDH.Value.Metres;
            percent1 = 0;
            gP = Captions.GP;
            angleGradientSlope1 = self.parametersPanel.pnlGP.Value;
            strS = "%s = %f"%(gP, angleGradientSlope1);
        else:
            num6 = Unit.ConvertDegToRad(self.parametersPanel.pnlGP.Value);
            percent = math.sin(num6) / math.cos(num6);
            metres = 15;
            percent1 = 0;
            gP1 = Captions.GP;
            angleGradientSlope2 = self.parametersPanel.pnlGP.Value;
            strS = "%s = %f"%(gP1, angleGradientSlope2);
        num7 = Unit.ConvertDegToRad(90);
        point3d10 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num7, metres);
        num8 = metres + percent * metres1;
        point3d11 = MathHelper.distanceBearingPoint(point3d1, Unit.ConvertDegToRad(450) - num7, num8);
        if (self.parametersPanel.pnlUsedFor.SelectedIndex == 0):
            num9 = metres + (percent - percent1) * metres1;
            point3d12 = MathHelper.distanceBearingPoint(point3d1, Unit.ConvertDegToRad(450) - num7, num9);
            line = QgsGeometry.fromPolyline([point3d10, point3d12]);
            AcadHelper.smethod_19(line, ProfileManagerDlg.constructionLayer, 1);
        line = QgsGeometry.fromPolyline([point3d10, point3d11]);
        AcadHelper.smethod_19(line, ProfileManagerDlg.constructionLayer, 3);
        point3d8 = MathHelper.distanceBearingPoint(point3d11, MathHelper.getBearing(point3d10, point3d11) + Unit.ConvertDegToRad(90), num3 / 4) if(self.parametersPanel.cmbBaseOrientation.SelectedIndex != 0) else MathHelper.distanceBearingPoint(point3d11, MathHelper.getBearing(point3d10, point3d11) - Unit.ConvertDegToRad(90), num3 / 4);
        dBText = AcadHelper.smethod_137(strS, point3d8, num3);
        if (self.parametersPanel.cmbBaseOrientation.SelectedIndex != 0):
            dBText.set_HorizontalMode(0);
        else:
            dBText.set_HorizontalMode(2);
        dBText.set_VerticalMode(1);
        dBText.set_AlignmentPoint(point3d8);
        if (self.parametersPanel.cmbBaseOrientation.SelectedIndex != 0):
            dBText.set_Rotation(Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d11, point3d10));
        else:
            dBText.set_Rotation(Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d10, point3d11));
        AcadHelper.smethod_19(dBText, ProfileManagerDlg.constructionLayer, 3);
        if (self.parametersPanel.txtDist1.Value.IsValid()):
            distance2 = self.parametersPanel.txtDist1.Value;
            point3d13 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num1, distance2.Metres);
            point3d8 = MathHelper.distanceBearingPoint(point3d13, Unit.ConvertDegToRad(450) - num2, 3 * num3);
            line = QgsGeometry.fromPolyline([point3d8, point3d13]);
            AcadHelper.smethod_18(line, ProfileManagerDlg.constructionLayer);
            if (not self.parametersPanel.txtText1.Value == ""):
                point3d8 = MathHelper.distanceBearingPoint(point3d13, Unit.ConvertDegToRad(450) - num2, 4 * num3);
                dBText = AcadHelper.smethod_140(self.parametersPanel.txtText1.Value, point3d8, num3, 1, 2);
                AcadHelper.smethod_18(dBText, ProfileManagerDlg.constructionLayer);
        if (self.parametersPanel.txtDist2.Value.IsValid()):
            value3 = self.parametersPanel.txtDist2.Value;
            point3d14 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num1, value3.Metres);
            point3d8 = MathHelper.distanceBearingPoint(point3d14, Unit.ConvertDegToRad(450) - num2, 3 * num3);
            line = QgsGeometry.fromPolyline([point3d8, point3d14]);
            AcadHelper.smethod_18(line, ProfileManagerDlg.constructionLayer);
            if (not self.parametersPanel.txtText2.Value == ""):
                point3d8 = MathHelper.distanceBearingPoint(point3d14, Unit.ConvertDegToRad(450) - num2, 4 * num3);
                dBText = AcadHelper.smethod_140(self.parametersPanel.txtText2.Value, point3d8, num3, 1, 2);
                AcadHelper.smethod_18(dBText, ProfileManagerDlg.constructionLayer);
        if (self.parametersPanel.txtDist3.Value.IsValid()):
            distance3 = self.parametersPanel.txtDist3.Value;
            point3d15 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num1, distance3.Metres);
            point3d8 = MathHelper.distanceBearingPoint(point3d15, Unit.ConvertDegToRad(450) - num2, 3 * num3);
            line = QgsGeometry.fromPolyline([point3d8, point3d15]);
            AcadHelper.smethod_18(line, ProfileManagerDlg.constructionLayer);
            if (not self.parametersPanel.txtText3.Value == ""):
                point3d8 = MathHelper.distanceBearingPoint(point3d15, Unit.ConvertDegToRad(450) - num2, 4 * num3);
                dBText = AcadHelper.smethod_140(self.parametersPanel.txtText3.Value, point3d8, num3, 1, 2);
                AcadHelper.smethod_18(dBText, ProfileManagerDlg.constructionLayer);
        if self.parametersPanel.chbPolyline.isChecked():
            QgisHelper.appendToCanvas(define._canvas, [ProfileManagerDlg.constructionLayer, self.pointLayer, self.lineLayer], self.surfaceType)
            self.resultLayerList = [ProfileManagerDlg.constructionLayer, self.pointLayer, self.lineLayer]
        else:
            QgisHelper.appendToCanvas(define._canvas, [ProfileManagerDlg.constructionLayer], self.surfaceType)
            self.resultLayerList = [ProfileManagerDlg.constructionLayer]
        self.proceedClicked = False

    def initParametersPan(self):
        ui = Ui_ProfileManager()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.pnlMode.Items = ["Setup", "Input1", "Input2","Input3"]
        self.parametersPanel.pnlUsedFor.Items = ["Departure", "Approach","ILS"]
        self.parametersPanel.cmbBaseOrientation.Items = ["LR", "RL"]

        self.parametersPanel.chbWriteName.clicked.connect(self.chbWriteName_clicked)
        self.parametersPanel.chbPolyline.clicked.connect(self.method_31)
        #
        self.connect(self.parametersPanel.pnlUsedFor, SIGNAL("Event_0"), self.method_31)
        self.connect(self.parametersPanel.pnlMode, SIGNAL("Event_0"), self.method_31)
        self.chbWriteName_clicked(self.parametersPanel.chbWriteName.isChecked())
        self.ui.btnEvaluate.setEnabled(True)
        self.parametersPanel.pnlBasePoint.Point3d = Point3D(677803.9246, 6617150.6787)
        self.parametersPanel.pnlThrDer.Point3d = Point3D(664684.9484, 6617888.008)
        self.parametersPanel.pnlEtp.Point3d = Point3D(666182.2544, 6625897.6157)
        self.parametersPanel.pnlOutbound.Value = 10.58
        self.method_31()
    def method_31(self):
        selectedIndex = self.parametersPanel.pnlMode.SelectedIndex == 0;
        self.parametersPanel.pnlUsedFor.Visible = selectedIndex;
        self.parametersPanel.pnlPDG.Visible = False if(not selectedIndex) else self.parametersPanel.pnlUsedFor.SelectedIndex == 0;
        self.parametersPanel.pnlMOC.Visible = False if(not selectedIndex) else self.parametersPanel.pnlUsedFor.SelectedIndex == 0;
        self.parametersPanel.pnlGP.Visible = False if(not selectedIndex)  else self.parametersPanel.pnlUsedFor.SelectedIndex != 0;
        self.parametersPanel.pnlRDH.Visible = False if(not selectedIndex) else self.parametersPanel.pnlUsedFor.SelectedIndex == 2;
        self.parametersPanel.gbConstruction.Visible = selectedIndex;
        self.ui.btnConstruct.setVisible(selectedIndex);
        flag = self.parametersPanel.pnlMode.SelectedIndex != 0;
        self.parametersPanel.pnlThrDer.Visible = flag;
        self.parametersPanel.pnlOutbound.Visible = flag;
        self.parametersPanel.pnlEtp.Visible = False if(not flag) else self.parametersPanel.pnlMode.SelectedIndex == 2;
        self.parametersPanel.pnlHASP.Visible = False if(not flag) else self.parametersPanel.pnlMode.SelectedIndex == 3;
        self.parametersPanel.pnlTA.Visible = False if(not flag) else self.parametersPanel.pnlMode.SelectedIndex == 3;
        self.parametersPanel.pnlClimbGradient.Visible = False if(not flag) else self.parametersPanel.pnlMode.SelectedIndex == 3;
        self.parametersPanel.chbMarkTA.setVisible(False if(not flag) else self.parametersPanel.pnlMode.SelectedIndex == 3);
        self.parametersPanel.chbDeparture.setVisible(False if(not flag) else self.parametersPanel.pnlMode.SelectedIndex == 3);
        self.parametersPanel.pnlInput.Visible = flag;
        self.ui.btnEvaluate.setVisible(flag);
        self.parametersPanel.chbPolyline.setVisible(flag);
        self.parametersPanel.chbWriteName.setVisible(True if(not self.parametersPanel.chbPolyline.isVisible()) else not self.parametersPanel.chbPolyline.isChecked());
        self.parametersPanel.pnlTextHeight.Visible = True if(not self.parametersPanel.chbPolyline.isVisible()) else not self.parametersPanel.chbPolyline.isChecked();

    def Point3dsComparer(self,a, b):
        if (a.get_X() < b.get_X()):
            return -1;
        if (a.get_X() > b.get_X()):
            return 1;
        if (a.get_Y() < b.get_Y()):
            return -1;
        if (a.get_Y() > b.get_Y()):
            return 1;
        if (a.get_Z() < b.get_Z()):
            return -1;
        if (a.get_Z() > b.get_Z()):
            return 1;
        return 0;
    # if (MathHelper.smethod_105(a, b, 0.00000001)):
    #     return 0;
    # if (a.get_X() < b.get_X()):
    #     return -1;
    # if (a.get_X() > b.get_X()):
    #     return 1;
    # if (a.get_Y() < b.get_Y()):
    #     return -1;
    # if (a.get_Y() > b.get_Y()):
    #     return 1;
    # if (a.get_Z() < b.get_Z()):
    #     return -1;
    # if (a.get_Z() > b.get_Z()):
    #     return 1;
    # return 0;

    def chbWriteName_clicked(self, state):
        self.parametersPanel.pnlTextHeight.Enabled = state
class ProfileManagerModeType:
    Setup = "Setup"
    Input1 = "Input1"
    Input2  = "Input2"
    Input3 = "Input3"

class ProfileManagerPurposeType:
    Departure = "Departure"
    Approach = "Approach"
    ILS = "ILS"

class InputEvaluatorBase:
    def __init__(self):
        pass

    def method_0(self, point3d_0, double_0):
        typedValue = dict(ThousandOne="PHXPROFILEMANAGER", ThousandTen=point3d_0, ThousandForty=double_0);
        return typedValue

    def method_1(self, obstacle_0, point3d_0, bool_0, bool_1, double_0, bool_2, double_1, bool_3):
        num = None
        line = None;
        z = obstacle_0.Position.get_Z();
        trees = obstacle_0.Trees;
        flag = not MathHelper.smethod_96(trees)#(!Trees.Applicable ? false : !MathHelper.smethod_96(trees));
    #     if (obstacle_0.Type != ObstacleType.Contour)
    #     {
    #         if (obstacle_0.Type == ObstacleType.Terrain)
    #         {
    #             goto Label2;
    #         }
    #         num = 62;
    #         goto Label0;
    #     }
    # Label2:
    #     num = 32;
    # Label0:
        num = 62;
        resultBuffer = self.method_0(obstacle_0.Position, obstacle_0.Tolerance);
        if (not bool_0 or MathHelper.smethod_98(obstacle_0.Tolerance, 0.0001)):
            num1 = Unit.ConvertDegToRad(-70);
            num2 = Unit.ConvertDegToRad(250);
            num3 = Unit.ConvertDegToRad(20);
            num4 = z / math.cos(num3);
            point3d = MathHelper.distanceBearingPoint(point3d_0, 0, z);
            if (not bool_3):
                line = Line(point3d_0, point3d);
                line.set_XData(resultBuffer);
                AcadHelper.smethod_19(line, ProfileManagerDlg.constructionLayer, num);
            point3d1 = MathHelper.distanceBearingPoint(point3d, 7.85398163397448 - num1, num4);
            if (not bool_3):
                line = Line(point3d, point3d1);
                line.set_XData(resultBuffer);
                AcadHelper.smethod_19(line, ProfileManagerDlg.constructionLayer, num);
            point3d2 = MathHelper.distanceBearingPoint(point3d, 7.85398163397448 - num2, num4);
            if (not bool_3):
                line = Line(point3d, point3d2);
                line.set_XData(resultBuffer);
                AcadHelper.smethod_19(line, ProfileManagerDlg.constructionLayer, num);
            if (flag):
                point3d3 = MathHelper.distanceBearingPoint(point3d, 0, trees);
                if (bool_3):
                    ProfileManagerDlg.polylinePoints.append(point3d3);
                else:
                    line = Line(point3d, point3d3);
                    line.set_XData(resultBuffer);
                    AcadHelper.smethod_19(line, ProfileManagerDlg.constructionLayer, num);
            elif (bool_3):
                ProfileManagerDlg.polylinePoints.append(point3d);
            if (bool_2):
                point3d1 = MathHelper.distanceBearingPoint(point3d1, 0, z + double_1) if(not flag) else MathHelper.distanceBearingPoint(point3d1, 0, z + trees + double_1);
                point3d2 = MathHelper.distanceBearingPoint(point3d2, 0, z + double_1) if(not flag) else MathHelper.distanceBearingPoint(point3d2, 0, z + trees + double_1);
                line = Line(point3d1, point3d2);
                line.set_XData(resultBuffer);
                AcadHelper.smethod_19(line, ProfileManagerDlg.constructionLayer, 1);
        else:
            tolerance = obstacle_0.Tolerance;
            point3d4 = MathHelper.distanceBearingPoint(point3d_0, ProfileManagerDlg.ang, tolerance);
            point3d5 = MathHelper.distanceBearingPoint(point3d4, 0, z);
            point3d6 = MathHelper.distanceBearingPoint(point3d_0, ProfileManagerDlg.angop, tolerance);
            point3d7 = MathHelper.distanceBearingPoint(point3d6, 0, z);
            if (not flag):
                if (bool_3):
                    ProfileManagerDlg.polylinePoints.append(point3d7);
                else:
                    point3dArray = [point3d4, point3d5, point3d7, point3d6 ];
                    polyline0 = AcadHelper.smethod_126(point3dArray);
                    polyline = Line()
                    polyline.setGeometry(QgsGeometry.fromPolyline(polyline0.method_14()))
                    polyline.set_XData(resultBuffer);
                    AcadHelper.smethod_19(polyline, ProfileManagerDlg.constructionLayer, num);
                if (bool_2):
                    point3d5 = MathHelper.distanceBearingPoint(point3d5, 0, double_1);
                    point3d7 = MathHelper.distanceBearingPoint(point3d7, 0, double_1);
                    line1 = Line(point3d5, point3d7);
                    line1.set_XData(resultBuffer);
                    AcadHelper.smethod_19(line1, ProfileManagerDlg.constructionLayer, 1);
            else:
                point3d8 = MathHelper.distanceBearingPoint(point3d5, 0, trees);
                point3d9 = MathHelper.distanceBearingPoint(point3d7, 0, trees);
                if (bool_3):
                    ProfileManagerDlg.polylinePoints.Add(point3d9);
                else:
                    point3dArray1 = [point3d7, point3d5, point3d8, point3d9, point3d6, point3d4, point3d5 ];
                    polyline1 = AcadHelper.smethod_126(point3dArray1);
                    polyline1.set_XData(resultBuffer);
                    AcadHelper.smethod_19(polyline1, ProfileManagerDlg.constructionLayer, num);
                if (bool_2):
                    point3d8 = MathHelper.distanceBearingPoint(point3d8, 0, double_1);
                    point3d9 = MathHelper.distanceBearingPoint(point3d9, 0, double_1);
                    line2 = Line(point3d8, point3d9);
                    line2.set_XData(resultBuffer);
                    AcadHelper.smethod_19(line2, ProfileManagerDlg.constructionLayer, 1);
        if (not bool_3 and bool_1): # and (obstacle_0.Type == ObstacleType.Circle || obstacle_0.Type == ObstacleType.Position) && !string.IsNullOrEmpty(obstacle_0.Name))
            point3d10 = MathHelper.distanceBearingPoint(point3d_0, 3.14159265358979, 3 * double_0);
            dBText = AcadHelper.smethod_138(obstacle_0.Name, point3d10, double_0, 1);
            dBText.set_XData(resultBuffer);
            AcadHelper.smethod_19(dBText, ProfileManagerDlg.constructionLayer, num);

class Input1Evaluator(InputEvaluatorBase):
    def __init__(self, point3d_0, point3d_1, double_0, bool_0, bool_1, double_1, bool_2):
        InputEvaluatorBase.__init__(self)

        self.ptStart = point3d_0;
        self.ptThrDer = point3d_1;
        self.track = MathHelper.smethod_4(Unit.ConvertDegToRad(450 - double_0));
        self.useTolerance = bool_0;
        self.writeName = bool_1;
        self.textHeight = double_1;
        self.drawPolyline = bool_2;
        
    def imethod_0(self, obstacle_0):
        point3d = obstacle_0.Position.smethod_167(0);
        num = MathHelper.smethod_26(self.ptThrDer, point3d);
        num1 = max([self.track, num]);
        num2 = min([self.track, num]);
        num3 = math.cos(num1 - num2);
        num4 = num3 * MathHelper.calcDistance(point3d, self.ptThrDer);
        point3d1 = MathHelper.distanceBearingPoint(self.ptStart, ProfileManagerDlg.ang, num4);
        self.method_1(obstacle_0, point3d1, self.useTolerance, self.writeName, self.textHeight, False, None, self.drawPolyline);


class Input2Evaluator(InputEvaluatorBase):

    def __init__(self, point3d_0, point3d_1, double_0, bool_0, bool_1, double_1, point3d_2, bool_2):

        InputEvaluatorBase.__init__(self)

        self.ptStart = point3d_0;
        self.ptThrDer = point3d_1;
        self.useTolerance = bool_0;
        self.writeName = bool_1;
        self.textHeight = double_1;
        self.ptEtp = point3d_2;
        self.drawPolyline = bool_2;
        num = MathHelper.smethod_26(point3d_1, point3d_2);
        num1 = MathHelper.calcDistance(point3d_2, point3d_1);
        num2 = MathHelper.smethod_3(450 - double_0);
        num3 = Unit.smethod_1(num);
        num4 = math.fabs(num2 - num3);
        self.dst = math.cos(Unit.ConvertDegToRad(num4)) * num1;

    def imethod_0(self, obstacle_0):
        point3d = obstacle_0.Position.smethod_167(0);
        num = self.dst + MathHelper.calcDistance(point3d, self.ptEtp);
        point3d1 = MathHelper.distanceBearingPoint(self.ptStart, ProfileManagerDlg.ang, num);
        self.method_1(obstacle_0, point3d1, self.useTolerance, self.writeName, self.textHeight, False, None, self.drawPolyline);

class Input3Evaluator(InputEvaluatorBase):
    def __init__(self, point3d_0, altitude_0, point3d_1, double_0, bool_0, bool_1, double_1, altitude_1, altitude_2, angleGradientSlope_0, bool_2, bool_3, point3d_2, point3d_3, bool_4):
        InputEvaluatorBase.__init__(self)

        self.ptStart = point3d_0;
        self.ptThrDer = point3d_1;
        self.track = MathHelper.smethod_3(450 - double_0);
        self.useTolerance = bool_0;
        self.writeName = bool_1;
        self.textHeight = double_1;
        self.ta = altitude_2.Metres;
        self.isDeparture = bool_3;
        self.lineStart = point3d_2;
        self.lineEnd = point3d_3;
        self.drawPolyline = bool_4;
        metres = altitude_2.Metres - (altitude_1.Metres + altitude_0.Metres);
        self.stp2 = metres / (angleGradientSlope_0 / 100);
        self.pt1 = MathHelper.distanceBearingPoint(point3d_0, ProfileManagerDlg.ang, self.stp2);
        if (bool_2):
            point3d = MathHelper.distanceBearingPoint(self.pt1, 0, altitude_2.Metres);
            line = Line(self.pt1, point3d);
            AcadHelper.smethod_18(line, ProfileManagerDlg.constructionLayer);
            point3d1 = MathHelper.distanceBearingPoint(point3d, 0, (altitude_2.Metres - altitude_0.Metres) / 4);
            dBText = AcadHelper.smethod_138(Captions.TP, point3d1, double_1, 4);
            AcadHelper.smethod_18(dBText, ProfileManagerDlg.constructionLayer);

    def imethod_0(self, obstacle_0):
        point3d = None;
        point3d1 = None;
        num = None;
        num1 = None;
        point3d2 = obstacle_0.Position.smethod_167(0);
        num2 = MathHelper.smethod_26(self.lineStart, self.lineEnd);
        num3 = num2 + 1.5707963267949;
        point3d3 = MathHelper.distanceBearingPoint(point3d2, 7.85398163397448 - num3, 100);
        point3d = MathHelper.getIntersectionPoint(self.lineStart, self.lineEnd, point3d2, point3d3)
        if (point3d == None):
            return
            # throw new Exception(Messages.ERR_FAILED_TO_CALCULATE_INTERSECTION_POINT);
        num4 = MathHelper.calcDistance(point3d2, point3d);
        point3d4 = MathHelper.distanceBearingPoint(self.ptThrDer, 7.85398163397448 - Unit.ConvertDegToRad(self.track), 100);
        point3d1 = MathHelper.getIntersectionPoint(self.ptThrDer, point3d4, point3d2, point3d)
        if (point3d1 == None):
            return
            # throw new Exception(Messages.ERR_FAILED_TO_CALCULATE_INTERSECTION_POINT);
        num5 = 0;
        if (MathHelper.calcDistance(point3d1, point3d) > MathHelper.calcDistance(point3d1, point3d2)):
            num4 = 0;
            num5 = 1;
        num6 = MathHelper.smethod_26(self.ptThrDer, point3d);
        num7 = MathHelper.calcDistance(self.ptThrDer, point3d);
        num8 = Unit.smethod_1(num6);
        num9 = MathHelper.smethod_3(math.fabs(self.track - num8));
        num10 = math.cos(Unit.ConvertDegToRad(num9)) * num7;
        if (num10 < 0 or num10 > self.stp2):
            num1 = self.stp2;
        else:
            num1 = num10;
            num = num1;
        num = num1;
        if (num5 == 1):
            num = num10
        mocMultiplier = 0.008 * (num4 + num);
        mocMultiplier = mocMultiplier * obstacle_0.MocMultiplier;
        if (mocMultiplier < 90):
            mocMultiplier = 90;
        mocMultiplier1 = 300 * obstacle_0.MocMultiplier;
        if (mocMultiplier > mocMultiplier1):
            mocMultiplier = mocMultiplier1;
        point3d5 = MathHelper.distanceBearingPoint(self.pt1, ProfileManagerDlg.ang, num4);
        self.method_1(obstacle_0, point3d5, self.useTolerance, self.writeName, self.textHeight, self.isDeparture, mocMultiplier, self.drawPolyline);



class ProfileManagerObstacles(ObstacleTable):
    def __init__(self, evaluator, manualPoly):
        ObstacleTable.__init__(self, None)

        self.evaluator = evaluator
        self.manualPolygon = manualPoly
    def checkObstacle(self, obstacle_0):
        if self.manualPolygon.contains(obstacle_0.Position):
            self.evaluator.imethod_0(obstacle_0)
class RubberBandPolygon(QgsMapTool):
    def __init__(self, canvas, parent):
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
        self.pointCount = 0
        self.parentDlg = parent
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
            self.pointCount += 1
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
            self.parentDlg.show()
            self.pointCount = 0
            define._canvas.setToolTip("")
            define._messageLabel.setText("")
            self.emit(SIGNAL("outputResult"), self.polygonGeom)


    def canvasMoveEvent( self, e ):
        if self.pointCount == 0:
            define._canvas.setToolTip(Prompts.START_POINT_OF_OBSTACLE_AREA_OR)
            define._messageLabel.setText(Prompts.START_POINT_OF_OBSTACLE_AREA_OR)
        else:
            define._canvas.setToolTip(Prompts.NEXT_POINT_OF_OBSTACLE_AREA_OR)
            define._messageLabel.setText(Prompts.NEXT_POINT_OF_OBSTACLE_AREA_OR)
        if ( self.mRubberBand == None ):
            return
        if ( self.mRubberBand.numberOfVertices() > 0 ):
            self.mRubberBand.removeLastPoint( 0 )
            self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )

    def deactivate(self):
#         self.rubberBand.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))

class SelectLine(QgsMapTool):

    def __init__(self, canvas, stringMsg = None, parent = None):
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
        self.stringMsg = stringMsg
        self.msgMenu = None
        self.parentDlg = parent
        if self.stringMsg != None:
            define._canvas.setToolTip(stringMsg)
            pass
            # self.msgMenu = self.createContextMenu(self.stringMsg)
#     QgsRubberBand* mRubberBand;
#     def reset(self):
#         self.startPoint = None
#         self.endPoint = None
#         self.isDrawing = False
#         SelectByRect.RubberRect.reset(QGis.Polygon)
#         self.layer = self.canvas.currentLayer()
    def createContextMenu(self, msg):
        label = QLabel(msg)
        # actionEnterMsg = QgisHelper.createAction(menu, msg, self.menuMsgClick)
        # menu.addAction(actionEnterMsg)
        return label
    def menuMsgClick(self):
        pass
    def canvasPressEvent(self, e):
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        self.mSelectRect.setRect( 0, 0, 0, 0 )
        self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
        self.startPoint, self.pointID, self.layer= self.snapPoint(e.pos())

    def canvasMoveEvent(self, e):
        # self.msgMenu.setGeometry()
        # self.msgMenu.exec_(define._canvas.mapToGlobal(e.pos()))
        if ( e.buttons() != Qt.LeftButton ):
            return
        if ( not self.mDragging ):
            self.mDragging = True
            self.mSelectRect.setTopLeft( e.pos() )
        self.mSelectRect.setBottomRight( e.pos() )
        QgsMapToolSelectUtils.setRubberBand( self.mCanvas, self.mSelectRect,self.mRubberBand )

    def canvasReleaseEvent(self, e):
        self.endPoint, self.pointID, self.layer= self.snapPoint(e.pos())

        vlayer = QgsMapToolSelectUtils.getCurrentVectorLayer( self.mCanvas )
        if ( vlayer == None ):
            if ( self.mRubberBand != None):
                self.mRubberBand.reset( QGis.Polygon )
                del self.mRubberBand
                self.mRubberBand = None
                self.mDragging = False
            return


        if (not self.mDragging ):
            QgsMapToolSelectUtils.expandSelectRectangle(self. mSelectRect, vlayer, e.pos() )
        else:
            if ( self.mSelectRect.width() == 1 ):
                self.mSelectRect.setLeft( self.mSelectRect.left() + 1 )
            if ( self.mSelectRect.height() == 1 ):
                self.mSelectRect.setBottom( self.mSelectRect.bottom() + 1 )

        if ( self.mRubberBand != None ):
            QgsMapToolSelectUtils.setRubberBand( self.mCanvas, self.mSelectRect, self.mRubberBand )
            selectGeom = self.mRubberBand.asGeometry()


            selectedFeatures = QgsMapToolSelectUtils.setSelectFeaturesOrRubberband_Tas_1( self.mCanvas, selectGeom, e )
            if len(selectedFeatures) > 0:
                self.emit(SIGNAL("outputResult"), selectedFeatures)
                self.parentDlg.show()


            del selectGeom

            self.mRubberBand.reset( QGis.Polygon )
            del self.mRubberBand
            self.mRubberBand = None
        self.mDragging = False

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

