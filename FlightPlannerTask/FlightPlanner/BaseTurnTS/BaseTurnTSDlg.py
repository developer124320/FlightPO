# -*- coding: UTF-8 -*-
'''
Created on 24 May 2014

@author: Administrator
'''
from PyQt4.QtGui import QMessageBox, QStandardItem, QFileDialog
from PyQt4.QtCore import QCoreApplication, QString, SIGNAL, Qt
from qgis.core import QGis, QgsLayerTreeGroup, QgsLayerTreeLayer, QgsVectorLayer
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.WindPanel import WindPanel
from FlightPlanner.MeasureTool import MeasureTool
# 
from FlightPlanner.Captions import Captions
from FlightPlanner.QgisHelper import QgisHelper

from FlightPlanner.BaseTurnTS.ui_BaseTurnTS import Ui_BaseTurnTS

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType,\
                      DistanceUnits, OrientationType,\
                       ObstacleAreaResult
from FlightPlanner.types import AltitudeUnits, Point3D, AngleUnits, SurfaceTypes,\
                Matrix3d, Vector3d
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.AcadHelper import AcadHelper
from map.QgsAppLayerTreeViewMenuProvider import QgsAppLayerTreeViewMenuProvider
from FlightPlanner.helpers import Distance, Speed, Altitude, MathHelper, Unit

import define
import math

class BaseTurnTSDlg(FlightPlanBaseDlg):    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("BaseTurnTC")
        self.surfaceType = SurfaceTypes.BaseTurnTC

        self.initParametersPan()
        self.uiStateInit()
        self.setWindowTitle(SurfaceTypes.BaseTurnTC)
        self.resize(540, 550)
        QgisHelper.matchingDialogSize(self, 650, 700)
        self.method_30()
        self.constructionLayer = None

        # define._qgsDistanceArea.setSourceCrs()
        # id = define._qgsDistanceArea.sourceCrs()
        # crs = QgsCoordinateReferenceSystem(id, QgsCoordinateReferenceSystem.InternalCrsId)
        # n = crs.authid()

        #test
        mod = 19 % 8
        # meterCrs = QgsCoordinateReferenceSystem(2284, QgsCoordinateReferenceSystem.EpsgCrsId)
        # latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        # mptBase1 = QgisHelper.CrsTransformPoint(-77.775063000000003, 37.695704999999997,latCrs, meterCrs)
        # mptBase2 = QgisHelper.CrsTransformPoint(-77.775346999999996, 37.695664000000001,latCrs, meterCrs)
        #
        # dist = MathHelper.calcDistance(mptBase1, mptBase2)
        #
        #
        # cellsize = dist/ 432.1307672
        # d0 = cellsize * 1336
        # d1 = cellsize * 2004
        # heading = 241.177220000000010
        # mptBase1 = QgisHelper.CrsTransformPoint(-77.775347, 37.695664,latCrs, meterCrs)
        #
        # pt0 = MathHelper.distanceBearingPoint(mptBase1 , Unit.ConvertDegToRad(heading), d0)
        # pt1 = MathHelper.distanceBearingPoint(mptBase1 , Unit.ConvertDegToRad(heading + 90), d1)
        # pt2 = MathHelper.distanceBearingPoint(mptBase1 , Unit.ConvertDegToRad(heading - 180), d0)
        # pt3 = MathHelper.distanceBearingPoint(mptBase1 , Unit.ConvertDegToRad(heading - 90), d1)
        # #
        # #
        # point0 = MathHelper.distanceBearingPoint(pt0 , Unit.ConvertDegToRad(heading + 90), d1)
        # point1 = MathHelper.distanceBearingPoint(pt2 , Unit.ConvertDegToRad(heading + 90), d1)
        # point2 = MathHelper.distanceBearingPoint(pt2 , Unit.ConvertDegToRad(heading - 90), d1)
        # point3 = MathHelper.distanceBearingPoint(pt0 , Unit.ConvertDegToRad(heading - 90), d1)
        # #
        # pointLT = Point3D(point0.x(), point1.y())
        # pointRB = Point3D(point2.x(), point3.y())
        self.vorDmeFeatureArray = dict()
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
                elif self.parametersPanel.cmbNavAidType.SelectedIndex == 1:
                    if attrValue == "VORDME" or attrValue == "VORTAC" or attrValue == "TACAN":
                        vorDmeList.append(attrValue)
                        vorDmeFeatureList.append(feat)
                elif self.parametersPanel.cmbNavAidType.SelectedIndex == 2:
                    if attrValue == "NDB" or attrValue == "NDBDME":
                        vorDmeList.append(attrValue)
                        vorDmeFeatureList.append(feat)
                elif self.parametersPanel.cmbNavAidType.SelectedIndex == 3:
                    if attrValue == "NDBDME":
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

    def btnEvaluate_Click(self):
        num = 0.0
        metres = 0.0
        num1 = 0.0
        num2 = 0.0
        num3 = 0.0
        value = 0.0
        num4 = 0.0
        num5 = 0.0
        num6 = 0.0
        point3d = Point3D()
        point3d1  = Point3D()
        point3d2 = Point3D()
        point3d3 = Point3D()
        point3d4 = Point3D()
        point3d5 = Point3D()
        flag = False
        point3d6 = Point3D()
        num7 = 0.0
        point3d7 = Point3D()
        origin = Point3D()
        origin1 = Point3D()
        origin2 = Point3D()
        point3d8 = Point3D()
        point3d9 = Point3D()
        origin3 = Point3D()
        origin4 = Point3D()
        origin5 = Point3D()
        num8 = 0.0
        num9 = 0.0
        point3d10 = Point3D()
        flag1 = False
        origin6 = Point3D()
        origin7 = Point3D()
        point3d11 = Point3D()
        num10 = 0.0
        point3d12 = Point3D()
        point3d13 = Point3D()
        point3d14 = Point3D()
        point3d15 = Point3D()
        point3d16 = Point3D()
        point3d17 = Point3D()
        point3d18 = Point3D()
        point3d19 = Point3D()
        point3d20 = Point3D()
        point3d21 = Point3D()
        point3d22 = Point3D()
        point3d23 = Point3D()
        point3d24 = Point3D()
        point3d25 = Point3D()
        point3d26 = Point3D()
        point3d27 = Point3D()
        point3d28 = Point3D()
        point3d29 = Point3D()
        point3d30 = Point3D()
        point3dArray = []
        polylineArea = PolylineArea()
        polylineArea1 = PolylineArea()
        
        point3d31 = self.parametersPanel.pnlNavAid.Point3d
        speed = Speed(float(self.parametersPanel.txtIas.text()))
        altitude = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)
        value1 = float(self.parametersPanel.txtIsa.text())
        value2 = float(self.parametersPanel.txtOffset.text())
        speed1 = Speed(float(self.parametersPanel.pnlWind.speedBox.text()))
        speed2 = Speed.smethod_0(speed, value1, altitude)
        num11 = Unit.ConvertKMToMeters(speed2.KilometresPerHour)
        num12 = num11 / 3600
        num13 = min([943270 / num11, 3])
        num14 = 1000 * (num11 / (62830 * num13))
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 0):
            if (self.parametersPanel.cmbNavAidType.SelectedIndex == 1):
                num = Unit.ConvertDegToRad(5.2)
            else:
                num = Unit.ConvertDegToRad(6.9)
        else:
            num = Unit.ConvertDegToRad(5.2)
        metres1 = altitude.Metres - point3d31.get_Z()
        if ((self.parametersPanel.cmbNavAidType.SelectedIndex == 1 or self.parametersPanel.cmbNavAidType.SelectedIndex == 3) and self.parametersPanel.cmbTurnLimitation.currentIndex() == 1):
            metres = Distance(float(self.parametersPanel.txtDmeDistance.text()), DistanceUnits.NM).Metres
            num1 = 460 + metres * 0.0125
            num2 = 1.5707963267949 if(MathHelper.smethod_96(metres)) else math.atan(num14 / metres)
            num3 = Unit.smethod_1(num2) * 2
            value = metres / (num11 / 60)
        else:
            metres = 0
            num1 = 0
            value = float(self.parametersPanel.txtTime.text())
            num3 = 0.215 * (speed2.Knots / value) if(speed2.Knots > 170) else 36 / value
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 2):
            if (self.parametersPanel.cmbNavAidType.SelectedIndex == 3):
                num4 = 0.839099631
            else:
                num4 = 1.191753593
        else:
            num4 = 0.839099631
        num15 = metres1 * num4
        num16 = 60 * value
        num17 = Unit.ConvertDegToRad(num3)
        num18 = num17 + num
        num19 = num17 - num
        num20 = Unit.ConvertDegToRad(num3) / 2
        num21 = Unit.ConvertNMToMeter(speed1.Knots)
        metresPerSecond = speed1.MetresPerSecond
        num22 = metresPerSecond / num13
        if (self.parametersPanel.cmbTurnLimitation.currentIndex() != 1):
            num5 = (num16 - 5) * (num12 - metresPerSecond) - num15
            num6 = (num16 + 21) * (num12 + metresPerSecond) + num15
        else:
            num5 = metres - num1 + 5 * (num12 - metresPerSecond)
            num6 = metres + num1 + 11 * (num12 + metresPerSecond)
        num23 = 50 * num22
        num24 = 100 * num22
        num25 = 190 * num22
        num26 = 235 * num22
        num27 = 11 * metresPerSecond
        num28 = num27 + num23
        num29 = num27 + num24
        num30 = 11 * num12
        num31 = math.asin(num21 / num11)
        Unit.smethod_1(num31)
        num32 = math.sin(num20) / math.cos(num20)
        point3d32 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num17, num6)
        point3d33 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - Unit.ConvertDegToRad(0), num6)
        num33 = num14 / math.sin(num17 / 2)
        point3d34 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num17 / 2, num33)
        MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num18, num5)
        point3d35 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num19, num5)
        point3d36 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num18, num6)
        point3d37 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num19, num6)
        num34 = num17 - Unit.ConvertDegToRad(90)
        point3d38 = MathHelper.distanceBearingPoint(point3d36, Unit.ConvertDegToRad(450) - num34, num14)
        point3d39 = MathHelper.distanceBearingPoint(point3d35, Unit.ConvertDegToRad(450) - num34, num14)
        point3d40 = MathHelper.distanceBearingPoint(point3d37, Unit.ConvertDegToRad(450) - num34, num14)
        num35 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d38, point3d36)
        point3d41 = MathHelper.distanceBearingPoint(point3d38, Unit.ConvertDegToRad(450) - (num35 - Unit.ConvertDegToRad(50)), num14)
        point3d42 = MathHelper.distanceBearingPoint(point3d38, Unit.ConvertDegToRad(450) - (num35 - Unit.ConvertDegToRad(100)), num14)
        num36 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d40, point3d37)
        point3d43 = MathHelper.distanceBearingPoint(point3d40, Unit.ConvertDegToRad(450) - (num36 - Unit.ConvertDegToRad(100)), num14)
        point3d44 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(450) - (num36 - Unit.ConvertDegToRad(190)), num14)
        point3d45 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(450) - (num36 - Unit.ConvertDegToRad(235)), num14)
        point3d46 = MathHelper.distanceBearingPoint(point3d42, Unit.ConvertDegToRad(450) - num31, num24)
        point3d46.get_X()
        y = point3d46.get_Y()
        num37 = math.sin(num31)
        num38 = num37 / math.cos(num31)
        num39 = max([point3d31.get_Y(), y])
        num40 = min([point3d31.get_Y(), y])
        num41 = num38 * (num39 - num40)
        point3d47 = MathHelper.distanceBearingPoint(point3d46, Unit.ConvertDegToRad(450) - 0, num41)
        x = point3d47.get_X()
        point3d48 = Point3D(x, point3d31.get_Y(), 0)
        point3d49 = MathHelper.distanceBearingPoint(point3d43, Unit.ConvertDegToRad(450) - num31, num24)
        point3d49.get_X()
        y = point3d49.get_Y()
        num39 = max([point3d31.get_Y(), y])
        num40 = min([point3d31.get_Y(), y])
        num41 = num38 * (num39 - num40)
        point3d47 = MathHelper.distanceBearingPoint(point3d49, Unit.ConvertDegToRad(450) - 0, num41)
        x = point3d47.get_X()
        point3d50 = Point3D(x, point3d31.get_Y(), 0)
        num42 = MathHelper.calcDistance(point3d31, point3d48)
        if (MathHelper.calcDistance(point3d31, point3d50) <= num42):
            point3d = point3d48
            point3d1 = point3d46
        else:
            point3d = point3d50
            point3d1 = point3d49
        point3d51 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - Unit.ConvertDegToRad(180), num14)
        point3d52 = MathHelper.distanceBearingPoint(point3d51, Unit.ConvertDegToRad(450) - (0 - Unit.ConvertDegToRad(50)), num14)
        point3d53 = MathHelper.distanceBearingPoint(point3d51, Unit.ConvertDegToRad(450) - (0 - Unit.ConvertDegToRad(100)), num14)
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d36, 0, point3d41, num23)
        point3d54 = point3d5
        point3d55 = MathHelper.distanceBearingPoint(point3d38, Unit.ConvertDegToRad(450) - (num35 - Unit.ConvertDegToRad(50)), num14 + num23)
        num43 = MathHelper.calcDistance(point3d54, point3d55)
        num44 = math.asin(num43 / 2 / num23)
        point3d56 = MathHelper.distanceBearingPoint(point3d41, Unit.ConvertDegToRad(450) - (num35 - (Unit.ConvertDegToRad(50) - num44)), num23)
        if (not MathHelper.smethod_102(point3d, point3d48)):
            flag = False
            origin = MathHelper.distanceBearingPoint(point3d38, Unit.ConvertDegToRad(450) - (num35 - Unit.ConvertDegToRad(100)), num24 + num14)
            point3d6 = MathHelper.smethod_68(point3d36, point3d56, origin)
            num7 = MathHelper.calcDistance(point3d36, point3d6)
            point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(origin, 0, point3d43, num24)
            origin1 = point3d5
            num45 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d43, origin1)
            num46 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d43, point3d1)
            num47 = (num45 + num46) / 2
            origin2 = MathHelper.distanceBearingPoint(point3d43, Unit.ConvertDegToRad(450) - num47, num24)
            point3d7 = origin
        else:
            flag = True
            point3d6 = MathHelper.smethod_68(point3d36, point3d56, point3d1)
            num7 = MathHelper.calcDistance(point3d36, point3d6)
            point3d7 = point3d1
            origin = Point3D.get_Origin()
            origin1 = Point3D.get_Origin()
            origin2 = Point3D.get_Origin()
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d, 0, point3d52, num23)
        point3d57 = point3d5
        point3d58 = MathHelper.distanceBearingPoint(point3d51, Unit.ConvertDegToRad(450) - (0 - Unit.ConvertDegToRad(50)), num14 + num23)
        num48 = MathHelper.calcDistance(point3d57, point3d58)
        num49 = math.asin(num48 / 2 / num23)
        point3d59 = MathHelper.distanceBearingPoint(point3d52, Unit.ConvertDegToRad(450) - (0 - (Unit.ConvertDegToRad(50) - num49)), num23)
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d53, num24, point3d44, num25)
        point3d60 = point3d4
        point3d61 = point3d5
        num50 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d60, point3d61)
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d53, num24, point3d45, num26)
        point3d62 = point3d4
        point3d63 = point3d5
        num51 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d62, point3d63)
        if (num51 <= num50):
            point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d44, num25, point3d45, num26)
            point3d9 = point3d5
            origin5 = point3d4
            point3d8 = point3d60
            origin3 = point3d61
            num52 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d44, origin3)
            num53 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d44, origin5)
            num54 = (num52 + num53) / 2
            origin4 = MathHelper.distanceBearingPoint(point3d44, Unit.ConvertDegToRad(450) - num54, num25)
        else:
            point3d8 = point3d62
            point3d9 = point3d63
            origin3 = Point3D.get_Origin()
            origin4 = Point3D.get_Origin()
            origin5 = Point3D.get_Origin()
        num55 = num3 + value2
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 2):
            if (self.parametersPanel.cmbNavAidType.SelectedIndex == 3):
                num8 = 25
                num9 = metres1 * 0.839099631
            else:
                num8 = 15
                num9 = metres1 * 1.191753593
        else:
            num8 = 25
            num9 = metres1 * 0.839099631
        num56 = Unit.ConvertDegToRad(num55 + num8)
        num57 = Unit.ConvertDegToRad(num55)
        point3d64 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num56, num9)
        point3d65 = MathHelper.distanceBearingPoint(point3d64, Unit.ConvertDegToRad(450) - num57, num30)
        point3d66 = MathHelper.distanceBearingPoint(point3d65, Unit.ConvertDegToRad(450) - (num57 - Unit.ConvertDegToRad(90)), num14)
        point3d67 = MathHelper.distanceBearingPoint(point3d66, Unit.ConvertDegToRad(450) - (num57 + Unit.ConvertDegToRad(40)), num14)
        point3d68 = MathHelper.distanceBearingPoint(point3d66, Unit.ConvertDegToRad(450) - (num57 - Unit.ConvertDegToRad(10)), num14)
        MathHelper.distanceBearingPoint(point3d65, Unit.ConvertDegToRad(450) - (num57 + Unit.ConvertDegToRad(90)), num27)
        MathHelper.distanceBearingPoint(point3d67, Unit.ConvertDegToRad(450) - (num57 + Unit.ConvertDegToRad(40)), num28)
        point3d69 = MathHelper.distanceBearingPoint(point3d68, Unit.ConvertDegToRad(450) - (num57 - Unit.ConvertDegToRad(10)), num29)
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d65, num27, point3d67, num28)
        point3d70 = point3d5
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d67, num28, point3d68, num29)
        point3d71 = point3d4
        num58 = MathHelper.calcDistance(point3d70, point3d71)
        num59 = math.asin(num58 / 2 / num28)
        point3d72 = MathHelper.distanceBearingPoint(point3d67, Unit.ConvertDegToRad(450) - (Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d67, point3d71) + num59), num28)
        point3d10 = MathHelper.smethod_68(point3d64, point3d72, point3d69)
        num60 = MathHelper.calcDistance(point3d10, point3d64)
        if (num26 <= max([point3d45.get_X(), point3d31.get_X()]) - min([point3d45.get_X(), point3d31.get_X()])):
            flag1 = False
            origin7 = Point3D.get_Origin()
            origin6 = Point3D.get_Origin()
        else:
            flag1 = True
            point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d10, num60, point3d45, num26)
            origin6 = point3d3
            origin7 = point3d2
        point3d11 = MathHelper.smethod_68(point3d36, point3d56, point3d7)
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d11, MathHelper.calcDistance(point3d11, point3d36), point3d67, num28)
        point3d73 = point3d3
        point3d74 = point3d2
        num61 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d10, point3d73)
        num10 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d10, point3d64) if(not flag1) else Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d10, origin7)
        num62 = (num10 + num61) / 2
        point3d75 = MathHelper.distanceBearingPoint(point3d10, Unit.ConvertDegToRad(450) - num62, num60)
        num63 = MathHelper.calcDistance(point3d31, point3d10)
        num64 = num60
        num65 = num63 * num63 - num64 * num64
        math.sqrt(math.fabs(num65))
        MathHelper.calcDistance(point3d31, point3d64)
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d31, 0, point3d10, num60)
        point3d12 = point3d5 if(not flag1) else origin7
        if (not flag):
            point3d13 = origin
            point3d14 = origin1
            point3d15 = origin2
            point3d16 = point3d1
            point3d17 = point3d
        else:
            point3d13 = point3d1
            point3d14 = point3d
            point3d15 = point3d
            point3d16 = point3d
            point3d17 = point3d
        num66 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d6, point3d13)
        num67 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d6, point3d74)
        point3d76 = MathHelper.distanceBearingPoint(point3d6, MathHelper.getBearing(point3d6, point3d74) + Unit.ConvertDegToRad(1), num7)
        point3d77 = point3d59
        point3d78 = point3d8
        if (num51 <= num50):
            point3d18 = origin3
            point3d19 = origin4
            point3d20 = origin5
            point3d21 = point3d9
        else:
            point3d18 = point3d9
            point3d19 = point3d9
            point3d20 = point3d9
            point3d21 = point3d9
        if (not flag1):
            point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d31, 0, point3d45, num26)
            point3d79 = point3d3
            num68 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d45, point3d9)
            num69 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d45, point3d79)
            point3d22 = point3d79
            point3d23 = point3d31
            point3d24 = MathHelper.distanceBearingPoint(point3d45, MathHelper.getBearing(point3d45, point3d21) + MathHelper.smethod_53(MathHelper.getBearing(point3d45, point3d21), MathHelper.getBearing(point3d45, point3d22)) / 2, num26)
        else:
            num70 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d45, point3d9)
            num71 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d45, origin6)
            point3d22 = origin6
            point3d23 = origin7
            point3d24 = MathHelper.distanceBearingPoint(point3d45, MathHelper.getBearing(point3d45, point3d21) + MathHelper.smethod_53(MathHelper.getBearing(point3d45, point3d21), MathHelper.getBearing(point3d45, point3d22)) / 2, num26)
        x1 = point3d22.get_X()
        x2 = point3d18.get_X()
        point3d25 = MathHelper.getIntersectionPoint(point3d31, point3d32, point3d34, MathHelper.distanceBearingPoint(point3d34, MathHelper.getBearing(point3d32, point3d31) + Unit.ConvertDegToRad(90), num14))
        point3d26 = MathHelper.getIntersectionPoint(point3d31, point3d33, point3d34, MathHelper.distanceBearingPoint(point3d34, MathHelper.getBearing(point3d33, point3d31) - Unit.ConvertDegToRad(90), num14))
        polylineArea1 = PolylineArea()
        polylineArea1.Add(PolylineAreaPoint(point3d31))
        polylineArea1.Add(PolylineAreaPoint(point3d25, MathHelper.smethod_57(MathHelper.smethod_63(MathHelper.getBearing(point3d31, point3d25), MathHelper.getBearing(point3d25, point3d26), AngleUnits.Radians), point3d25, point3d26, point3d34)))
        polylineArea1.Add(PolylineAreaPoint(point3d26))
        num72 = MathHelper.calcDistance(point3d31, point3d34) / 2
        num73 = num72 + num72 / 2
        num74 = num14 / 10
        num75 = num14 / 3
        point3d80 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - 0, num72).smethod_167(0)
        point3d81 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - 0, num72 + num75).smethod_167(0)
        point3d82 = MathHelper.distanceBearingPoint(point3d81, Unit.ConvertDegToRad(450) - Unit.ConvertDegToRad(90), num74).smethod_167(0)
        point3d83 = MathHelper.distanceBearingPoint(point3d81, Unit.ConvertDegToRad(450) - Unit.ConvertDegToRad(270), num74).smethod_167(0)
        if (self.parametersPanel.cmbOrientation.currentText() != OrientationType.Left):
            point3d27 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num17, num73).smethod_167(0)
            point3d28 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num17, num73 + num75).smethod_167(0)
            point3d29 = MathHelper.distanceBearingPoint(point3d27, Unit.ConvertDegToRad(450) - (Unit.ConvertDegToRad(90) + num17), num74).smethod_167(0)
            point3d30 = MathHelper.distanceBearingPoint(point3d27, Unit.ConvertDegToRad(450) - (num17 - Unit.ConvertDegToRad(90)), num74).smethod_167(0)
        else:
            num76 = Unit.ConvertDegToRad(90) + (Unit.ConvertDegToRad(90) - (Unit.ConvertDegToRad(450) - num17))
            point3d27 = MathHelper.distanceBearingPoint(point3d31, num76, num73).smethod_167(0)
            point3d28 = MathHelper.distanceBearingPoint(point3d31, num76, num73 + num75).smethod_167(0)
            point3d29 = MathHelper.distanceBearingPoint(point3d27, num76 + Unit.ConvertDegToRad(90), num74).smethod_167(0)
            point3d30 = MathHelper.distanceBearingPoint(point3d27, num76 - Unit.ConvertDegToRad(90), num74).smethod_167(0)
        if (x1 > x2):
            if (not flag):
                point3dArray = [point3d12, point3d73, point3d74, point3d13, point3d14, point3d16, point3d17, point3d78, point3d23]
                polylineArea = PolylineArea(point3dArray)
                polylineArea.method_19(0, MathHelper.smethod_60(point3d12, point3d75, point3d73))
                polylineArea.method_19(2, MathHelper.smethod_60(point3d74, point3d76, point3d13))
                polylineArea.method_19(4, MathHelper.smethod_60(point3d14, point3d15, point3d16))
                polylineArea.method_19(6, MathHelper.smethod_60(point3d17, point3d77, point3d78))
            else:
                point3dArray = [point3d12, point3d73, point3d74, point3d13, point3d17, point3d78, point3d23]
                polylineArea = PolylineArea(point3dArray)
                polylineArea.method_19(0, MathHelper.smethod_60(point3d12, point3d75, point3d73))
                polylineArea.method_19(2, MathHelper.smethod_60(point3d74, point3d76, point3d13))
                polylineArea.method_19(4, MathHelper.smethod_60(point3d17, point3d77, point3d78))
        elif (flag):
            if (num51 <= num50):
                point3dArray = [point3d12, point3d73, point3d74, point3d13, point3d17, point3d78, point3d18, point3d20, point3d21, point3d22, point3d23]
                polylineArea = PolylineArea(point3dArray)
                polylineArea.method_19(0, MathHelper.smethod_60(point3d12, point3d75, point3d73))
                polylineArea.method_19(2, MathHelper.smethod_60(point3d74, point3d76, point3d13))
                polylineArea.method_19(4, MathHelper.smethod_60(point3d17, point3d77, point3d78))
                polylineArea.method_19(6, MathHelper.smethod_60(point3d18, point3d19, point3d20))
                polylineArea.method_19(8, MathHelper.smethod_60(point3d21, point3d24, point3d22))
            else:
                point3dArray = [point3d12, point3d73, point3d74, point3d13, point3d17, point3d78, point3d21, point3d22, point3d23]
                polylineArea = PolylineArea(point3dArray)
                polylineArea.method_19(0, MathHelper.smethod_60(point3d12, point3d75, point3d73))
                polylineArea.method_19(2, MathHelper.smethod_60(point3d74, point3d76, point3d13))
                polylineArea.method_19(4, MathHelper.smethod_60(point3d17, point3d77, point3d78))
                polylineArea.method_19(6, MathHelper.smethod_60(point3d21, point3d24, point3d22))
        elif (num51 <= num50):
            point3dArray = [point3d12, point3d73, point3d74, point3d13, point3d14, point3d16, point3d17, point3d78, point3d18, point3d20, point3d21, point3d22, point3d23]
            polylineArea = PolylineArea(point3dArray)
            polylineArea.method_19(0, MathHelper.smethod_60(point3d12, point3d75, point3d73))
            polylineArea.method_19(2, MathHelper.smethod_60(point3d74, point3d76, point3d13))
            polylineArea.method_19(4, MathHelper.smethod_60(point3d14, point3d15, point3d16))
            polylineArea.method_19(6, MathHelper.smethod_60(point3d17, point3d77, point3d78))
            polylineArea.method_19(8, MathHelper.smethod_60(point3d18, point3d19, point3d20))
            polylineArea.method_19(10, MathHelper.smethod_60(point3d21, point3d24, point3d22))
        else:
            point3dArray = [point3d12, point3d73, point3d74, point3d13, point3d14, point3d16, point3d17, point3d78, point3d21, point3d22, point3d23]
            polylineArea = PolylineArea(point3dArray)
            polylineArea.method_19(0, MathHelper.smethod_60(point3d12, point3d75, point3d73))
            polylineArea.method_19(2, MathHelper.smethod_60(point3d74, point3d76, point3d13))
            polylineArea.method_19(4, MathHelper.smethod_60(point3d14, point3d15, point3d16))
            polylineArea.method_19(6, MathHelper.smethod_60(point3d17, point3d77, point3d78))
            polylineArea.method_19(8, MathHelper.smethod_60(point3d21, point3d24, point3d22))
        # mapUnits = define._canvas.mapUnits()
        # constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
        # if define._mapCrs == None:
        #     if mapUnits == QGis.Meters:
        #         constructionLayer = QgsVectorLayer("linestring?crs=EPSG:32633", self.surfaceType, "memory")
        #     else:
        #         constructionLayer = QgsVectorLayer("linestring?crs=EPSG:4326", self.surfaceType, "memory")
        # else:
        #     constructionLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")


        matrix3d = Matrix3d.MirroringFromVector3d(point3d31, Vector3d(0, 1, 0))
        matrix3d1 = Matrix3d.Rotation(-Unit.ConvertDegToRad(float(self.parametersPanel.txtTrackRadial.Value) + 90), Vector3d(0, 0, 1), point3d31)
        polyline = PolylineArea.smethod_136(polylineArea1, True)
        polyline1 = PolylineArea.smethod_136(polylineArea, True)
        
        polylineTemp = None
        polylineTemp1 = None
        if (self.parametersPanel.cmbOrientation.currentText() == OrientationType.Left):
            polylineTemp = polyline.TransformBy(matrix3d)
            polylineTemp1 = polyline1.TransformBy(matrix3d)
        polylineTemp = polyline.TransformBy(matrix3d1)
        polylineTemp1 = polyline1.TransformBy(matrix3d1)
        
        offsetCurvePointArray = QgisHelper.offsetCurve(polylineTemp1.method_14_closed(4), 4600)
        
        altitude_0 = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)
        altitude_1 = Altitude(float(self.parametersPanel.txtMoc.text()))
        
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 0):
            hOSE = BaseTurnTSSecondaryEvaluator(polylineTemp1, altitude_0, altitude_1, Distance(2.5, DistanceUnits.NM))
            self.obstaclesModel = BaseTurnTSObstacles(False, "second", None, altitude_0, hOSE.inner, hOSE.outer, hOSE.poly, altitude_1, Distance(2.5, DistanceUnits.NM)) 
#             selectionArea = (holdingOverheadSecondaryEvaluator as HoldingOverhead.HoldingOverheadSecondaryEvaluator).SelectionArea
        else:
            hOSE = BaseTurnTSSecondaryEvaluator(polylineTemp1, altitude_0, altitude_1, Distance(2, DistanceUnits.NM))
            self.obstaclesModel = BaseTurnTSObstacles(True, "second", None, altitude_0, hOSE.inner, hOSE.outer, hOSE.poly, altitude_1, Distance(2, DistanceUnits.NM)) 
        
        
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
        
    def btnPDTCheck_Click(self):
        pdtResultStr = ""
        if self.parametersPanel.txtTime.isVisible():
            pdtResultStr = MathHelper.pdtCheckResultToString(float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), float(self.parametersPanel.txtIas.text()), float(self.parametersPanel.txtTime.text()))
        else:
            pdtResultStr = MathHelper.pdtCheckResultToString(float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT), float(self.parametersPanel.txtIas.text()))

        QMessageBox.warning(self, "PDT Check", pdtResultStr)
        return FlightPlanBaseDlg.btnPDTCheck_Click(self)


    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        return FlightPlanBaseDlg.uiStateInit(self)
         


    def initParametersPan(self):
        ui = Ui_BaseTurnTS()
        self.parametersPanel = ui
        
        FlightPlanBaseDlg.initParametersPan(self) 
        
               
        self.parametersPanel.txtTas.setEnabled(False)
        self.parametersPanel.pnlNavAid = PositionPanel(self.parametersPanel.gbNavAid)
#         self.parametersPanel.pnlNavAid.hideframe_Altitude()
        self.parametersPanel.pnlNavAid.setObjectName("positionNavAid")
        self.parametersPanel.pnlNavAid.btnCalculater.hide()
        self.parametersPanel.verticalLayout_gbNavAid.addWidget(self.parametersPanel.pnlNavAid)
        self.connect(self.parametersPanel.pnlNavAid, SIGNAL("positionChanged"), self.iasChanged)

        # self.parametersPanel.pnlNavAid.Point3d = Point3D(17.9, 57.8)
        
        self.parametersPanel.pnlWind = WindPanel(self.parametersPanel.grbParameters)
        self.parametersPanel.pnlWind.lblIA.setMinimumSize(134, 0)
        self.parametersPanel.vLayout_grbParameters.insertWidget(4, self.parametersPanel.pnlWind)
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
        
#         self.resize(460,600)
        self.parametersPanel.cmbNavAidType.Items = [Captions.VOR, Captions.VOR_DME, Captions.NDB, Captions.NDB_DME ]
        self.parametersPanel.cmbOrientation.addItems([OrientationType.Left, OrientationType.Right])
        self.parametersPanel.cmbOrientation.setCurrentIndex(1)
        
        '''Event Handlers Connect'''
        
        self.parametersPanel.txtAltitude.textChanged.connect(self.method_31)
        self.parametersPanel.cmbTurnLimitation.currentIndexChanged.connect(self.method_28)
        self.connect(self.parametersPanel.cmbNavAidType, SIGNAL("Event_0"), self.initBasedOnCmb)
        self.connect(self.parametersPanel.cmbNavAidType, SIGNAL("Event_0"), self.method_30)
        self.parametersPanel.btnCaptureDME.clicked.connect(self.measureTool)
        self.parametersPanel.txtIas.textChanged.connect(self.iasChanged)
        self.parametersPanel.txtIsa.textChanged.connect(self.method_31)
        
        self.parametersPanel.txtAltitudeM.textChanged.connect(self.txtAltitudeMChanged)
        self.parametersPanel.txtAltitude.textChanged.connect(self.txtAltitudeFtChanged)

        self.flag = 0
        if self.flag==0:
            self.flag=2
        if self.flag==1:
            self.flag=0
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")

        self.parametersPanel.txtMoc.textChanged.connect(self.txtMocMChanged)
        self.parametersPanel.txtMocFt.textChanged.connect(self.txtMocFtChanged)

        self.flag1 = 0
        if self.flag1==0:
            self.flag1=2
        if self.flag1==1:
            self.flag1=0
        if self.flag1==2:
            try:
                self.parametersPanel.txtMocFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMoc.text())), 4)))
            except:
                self.parametersPanel.txtMocFt.setText("0.0")

        self.parametersPanel.txtTas.setEnabled(False)
        
        try:
            self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT) - self.parametersPanel.pnlNavAid.Altitude()).Knots, 4)))
        except:
            raise ValueError("Value Invalid")
    def txtAltitudeMChanged(self):
        if self.flag==0:
            self.flag=1
        if self.flag==2:
            self.flag=0
        if self.flag==1:
            try:
                self.parametersPanel.txtAltitude.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM.text())), 4)))
            except:
                self.parametersPanel.txtAltitude.setText("0.0")
    def txtAltitudeFtChanged(self):
        if self.flag==0:
            self.flag=2
        if self.flag==1:
            self.flag=0
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM.setText("0.0")

    def txtMocMChanged(self):
        if self.flag1==0:
            self.flag1=1
        if self.flag1==2:
            self.flag1=0
        if self.flag1==1:
            try:
                self.parametersPanel.txtMocFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtMoc.text())), 4)))
            except:
                self.parametersPanel.txtMocFt.setText("0.0")
    def txtMocFtChanged(self):
        if self.flag1==0:
            self.flag1=2
        if self.flag1==1:
            self.flag1=0
        if self.flag1==2:
            try:
                self.parametersPanel.txtMoc.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtMocFt.text())), 4)))
            except:
                self.parametersPanel.txtMoc.setText("0.0")
    def iasChanged(self):
        try:
            self.parametersPanel.txtTas.setText(str(round(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT) - self.parametersPanel.pnlNavAid.Altitude()).Knots, 4)))
        except:
            raise ValueError("Value Invalid")
#         
#     def iasHelpShow(self):
#         dlg = IasHelpDlg()
#         dlg.exec_()
   
    def measureTool(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtDmeDistance, DistanceUnits.NM)
        define._canvas.setMapTool(measureDistanceTool)
    def method_28(self):
        self.parametersPanel.frame_IasMA_3.setVisible(self.parametersPanel.cmbTurnLimitation.currentIndex() == 0)
        self.parametersPanel.frame_DMEDistance.setVisible(self.parametersPanel.cmbTurnLimitation.currentIndex()== 1)
    def method_29(self, int_0):

        self.parametersPanel.cmbTurnLimitation.clear()
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 1):
            if (self.parametersPanel.cmbNavAidType.SelectedIndex == 3):
#                 items = self..pnlTurnLimitation.Items
                tIME = [Captions.TIME, Captions.DME_DISTANCE ]
#                 items.AddRange(tIME)
                self.parametersPanel.cmbTurnLimitation.addItems(tIME)
                if (int_0 < 0 or int_0 >= self.parametersPanel.cmbTurnLimitation.count()):
                    int_0 = 0
                self.parametersPanel.cmbTurnLimitation.setCurrentIndex(int_0)
                return
            
            self.parametersPanel.cmbTurnLimitation.addItems([Captions.TIME])
            if (int_0 < 0 or int_0 >= self.parametersPanel.cmbTurnLimitation.count()):
                int_0 = 0
            self.parametersPanel.cmbTurnLimitation.setCurrentIndex(int_0)
            
            return
        
#         items = self.pnlTurnLimitation.Items
        self.parametersPanel.cmbTurnLimitation.addItems([Captions.TIME, Captions.DME_DISTANCE])
        
        if (int_0 < 0 or int_0 >= self.parametersPanel.cmbTurnLimitation.count()):
            int_0 = 0
            
        self.parametersPanel.cmbTurnLimitation.setCurrentIndex(int_0)
        
    def method_31(self):
        try:
            self.parametersPanel.txtTas.setText(str(Speed.smethod_0(Speed(float(self.parametersPanel.txtIas.text())), float(self.parametersPanel.txtIsa.text()), Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT) - self.parametersPanel.pnlNavAid.Altitude()).Knots))
        except:
            raise ValueError("Value Invalid")
        self.parametersPanel.pnlWind.setAltitude(Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT))
    def method_30(self):
        self.method_29(self.parametersPanel.cmbTurnLimitation.currentIndex())
        self.method_28()
        
#         define._canvas.setMapTool(self.captureTrackTool)

    def btnConstruct_Click(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return

        num = 0.0
        metres = 0.0
        num1 = 0.0
        num2 = 0.0
        num3 = 0.0
        value = 0.0
        num4 = 0.0
        num5 = 0.0
        num6 = 0.0
        point3d = Point3D()
        point3d1  = Point3D()
        point3d2 = Point3D()
        point3d3 = Point3D()
        point3d4 = Point3D()
        point3d5 = Point3D()
        flag = False
        point3d6 = Point3D()
        num7 = 0.0
        point3d7 = Point3D()
        origin = Point3D()
        origin1 = Point3D()
        origin2 = Point3D()
        point3d8 = Point3D()
        point3d9 = Point3D()
        origin3 = Point3D()
        origin4 = Point3D()
        origin5 = Point3D()
        num8 = 0.0
        num9 = 0.0
        point3d10 = Point3D()
        flag1 = False
        origin6 = Point3D()
        origin7 = Point3D()
        point3d11 = Point3D()
        num10 = 0.0
        point3d12 = Point3D()
        point3d13 = Point3D()
        point3d14 = Point3D()
        point3d15 = Point3D()
        point3d16 = Point3D()
        point3d17 = Point3D()
        point3d18 = Point3D()
        point3d19 = Point3D()
        point3d20 = Point3D()
        point3d21 = Point3D()
        point3d22 = Point3D()
        point3d23 = Point3D()
        point3d24 = Point3D()
        point3d25 = Point3D()
        point3d26 = Point3D()
        point3d27 = Point3D()
        point3d28 = Point3D()
        point3d29 = Point3D()
        point3d30 = Point3D()
        point3dArray = []
        polylineArea = PolylineArea()
        polylineArea1 = PolylineArea()
        
        point3d31 = self.parametersPanel.pnlNavAid.Point3d
        speed = Speed(float(self.parametersPanel.txtIas.text()))
        altitude = Altitude(float(self.parametersPanel.txtAltitude.text()), AltitudeUnits.FT)
        value1 = float(self.parametersPanel.txtIsa.text())
        value2 = float(self.parametersPanel.txtOffset.text())
        speed1 = Speed(float(self.parametersPanel.pnlWind.speedBox.text()))
        speed2 = Speed.smethod_0(speed, value1, altitude)
        num11 = Unit.ConvertKMToMeters(speed2.KilometresPerHour)
        num12 = num11 / 3600
        num13 = min([943270 / num11, 3])
        num14 = 1000 * (num11 / (62830 * num13))
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 0):
            if (self.parametersPanel.cmbNavAidType.SelectedIndex == 1):
                num = Unit.ConvertDegToRad(5.2)
            else:
                num = Unit.ConvertDegToRad(6.9)
        else:
            num = Unit.ConvertDegToRad(5.2)
        metres1 = altitude.Metres - point3d31.get_Z()
        if ((self.parametersPanel.cmbNavAidType.SelectedIndex == 1 or self.parametersPanel.cmbNavAidType.SelectedIndex == 3) and self.parametersPanel.cmbTurnLimitation.currentIndex() == 1):
            metres = Distance(float(self.parametersPanel.txtDmeDistance.text()), DistanceUnits.NM).Metres
            num1 = 460 + metres * 0.0125
            num2 = 1.5707963267949 if(MathHelper.smethod_96(metres)) else math.atan(num14 / metres)
            num3 = Unit.smethod_1(num2) * 2
            value = metres / (num11 / 60)
        else:
            metres = 0
            num1 = 0
            value = float(self.parametersPanel.txtTime.text())
            num3 = 0.215 * (speed2.Knots / value) if(speed2.Knots > 170) else 36 / value
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 2):
            if (self.parametersPanel.cmbNavAidType.SelectedIndex == 3):
                num4 = 0.839099631
            else:
                num4 = 1.191753593
        else:
            num4 = 0.839099631
        num15 = metres1 * num4
        num16 = 60 * value
        num17 = Unit.ConvertDegToRad(num3)
        num18 = num17 + num
        num19 = num17 - num
        num20 = Unit.ConvertDegToRad(num3) / 2
        num21 = Unit.ConvertNMToMeter(speed1.Knots)
        metresPerSecond = speed1.MetresPerSecond
        num22 = metresPerSecond / num13
        if (self.parametersPanel.cmbTurnLimitation.currentIndex() != 1):
            num5 = (num16 - 5) * (num12 - metresPerSecond) - num15
            num6 = (num16 + 21) * (num12 + metresPerSecond) + num15
        else:
            num5 = metres - num1 + 5 * (num12 - metresPerSecond)
            num6 = metres + num1 + 11 * (num12 + metresPerSecond)
        num23 = 50 * num22
        num24 = 100 * num22
        num25 = 190 * num22
        num26 = 235 * num22
        num27 = 11 * metresPerSecond
        num28 = num27 + num23
        num29 = num27 + num24
        num30 = 11 * num12
        num31 = math.asin(num21 / num11)
        Unit.smethod_1(num31)
        num32 = math.sin(num20) / math.cos(num20)
        point3d32 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num17, num6)
        point3d33 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - Unit.ConvertDegToRad(0), num6)
        num33 = num14 / math.sin(num17 / 2)
        point3d34 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num17 / 2, num33)
        MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num18, num5)
        point3d35 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num19, num5)
        point3d36 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num18, num6)
        point3d37 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num19, num6)
        num34 = num17 - Unit.ConvertDegToRad(90)
        point3d38 = MathHelper.distanceBearingPoint(point3d36, Unit.ConvertDegToRad(450) - num34, num14)
        point3d39 = MathHelper.distanceBearingPoint(point3d35, Unit.ConvertDegToRad(450) - num34, num14)
        point3d40 = MathHelper.distanceBearingPoint(point3d37, Unit.ConvertDegToRad(450) - num34, num14)
        num35 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d38, point3d36)
        point3d41 = MathHelper.distanceBearingPoint(point3d38, Unit.ConvertDegToRad(450) - (num35 - Unit.ConvertDegToRad(50)), num14)
        point3d42 = MathHelper.distanceBearingPoint(point3d38, Unit.ConvertDegToRad(450) - (num35 - Unit.ConvertDegToRad(100)), num14)
        num36 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d40, point3d37)
        point3d43 = MathHelper.distanceBearingPoint(point3d40, Unit.ConvertDegToRad(450) - (num36 - Unit.ConvertDegToRad(100)), num14)
        point3d44 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(450) - (num36 - Unit.ConvertDegToRad(190)), num14)
        point3d45 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(450) - (num36 - Unit.ConvertDegToRad(235)), num14)
        point3d46 = MathHelper.distanceBearingPoint(point3d42, Unit.ConvertDegToRad(450) - num31, num24)
        point3d46.get_X()
        y = point3d46.get_Y()
        num37 = math.sin(num31)
        num38 = num37 / math.cos(num31)
        num39 = max([point3d31.get_Y(), y])
        num40 = min([point3d31.get_Y(), y])
        num41 = num38 * (num39 - num40)
        point3d47 = MathHelper.distanceBearingPoint(point3d46, Unit.ConvertDegToRad(450) - 0, num41)
        x = point3d47.get_X()
        point3d48 = Point3D(x, point3d31.get_Y(), 0)
        point3d49 = MathHelper.distanceBearingPoint(point3d43, Unit.ConvertDegToRad(450) - num31, num24)
        point3d49.get_X()
        y = point3d49.get_Y()
        num39 = max([point3d31.get_Y(), y])
        num40 = min([point3d31.get_Y(), y])
        num41 = num38 * (num39 - num40)
        point3d47 = MathHelper.distanceBearingPoint(point3d49, Unit.ConvertDegToRad(450) - 0, num41)
        x = point3d47.get_X()
        point3d50 = Point3D(x, point3d31.get_Y(), 0)
        num42 = MathHelper.calcDistance(point3d31, point3d48)
        if (MathHelper.calcDistance(point3d31, point3d50) <= num42):
            point3d = point3d48
            point3d1 = point3d46
        else:
            point3d = point3d50
            point3d1 = point3d49
        point3d51 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - Unit.ConvertDegToRad(180), num14)
        point3d52 = MathHelper.distanceBearingPoint(point3d51, Unit.ConvertDegToRad(450) - (0 - Unit.ConvertDegToRad(50)), num14)
        point3d53 = MathHelper.distanceBearingPoint(point3d51, Unit.ConvertDegToRad(450) - (0 - Unit.ConvertDegToRad(100)), num14)
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d36, 0, point3d41, num23)
        point3d54 = point3d5
        point3d55 = MathHelper.distanceBearingPoint(point3d38, Unit.ConvertDegToRad(450) - (num35 - Unit.ConvertDegToRad(50)), num14 + num23)
        num43 = MathHelper.calcDistance(point3d54, point3d55)
        num44 = math.asin(num43 / 2 / num23)
        point3d56 = MathHelper.distanceBearingPoint(point3d41, Unit.ConvertDegToRad(450) - (num35 - (Unit.ConvertDegToRad(50) - num44)), num23)
        if (not MathHelper.smethod_102(point3d, point3d48)):
            flag = False
            origin = MathHelper.distanceBearingPoint(point3d38, Unit.ConvertDegToRad(450) - (num35 - Unit.ConvertDegToRad(100)), num24 + num14)
            point3d6 = MathHelper.smethod_68(point3d36, point3d56, origin)
            num7 = MathHelper.calcDistance(point3d36, point3d6)
            point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(origin, 0, point3d43, num24)
            origin1 = point3d5
            num45 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d43, origin1)
            num46 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d43, point3d1)
            num47 = (num45 + num46) / 2
            origin2 = MathHelper.distanceBearingPoint(point3d43, Unit.ConvertDegToRad(450) - num47, num24)
            point3d7 = origin
        else:
            flag = True
            point3d6 = MathHelper.smethod_68(point3d36, point3d56, point3d1)
            num7 = MathHelper.calcDistance(point3d36, point3d6)
            point3d7 = point3d1
            origin = Point3D.get_Origin()
            origin1 = Point3D.get_Origin()
            origin2 = Point3D.get_Origin()
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d, 0, point3d52, num23)
        point3d57 = point3d5
        point3d58 = MathHelper.distanceBearingPoint(point3d51, Unit.ConvertDegToRad(450) - (0 - Unit.ConvertDegToRad(50)), num14 + num23)
        num48 = MathHelper.calcDistance(point3d57, point3d58)
        num49 = math.asin(num48 / 2 / num23)
        point3d59 = MathHelper.distanceBearingPoint(point3d52, Unit.ConvertDegToRad(450) - (0 - (Unit.ConvertDegToRad(50) - num49)), num23)
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d53, num24, point3d44, num25)
        point3d60 = point3d4
        point3d61 = point3d5
        num50 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d60, point3d61)
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d53, num24, point3d45, num26)
        point3d62 = point3d4
        point3d63 = point3d5
        num51 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d62, point3d63)
        if (num51 <= num50):
            point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d44, num25, point3d45, num26)
            point3d9 = point3d5
            origin5 = point3d4
            point3d8 = point3d60
            origin3 = point3d61
            num52 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d44, origin3)
            num53 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d44, origin5)
            num54 = (num52 + num53) / 2
            origin4 = MathHelper.distanceBearingPoint(point3d44, Unit.ConvertDegToRad(450) - num54, num25)
        else:
            point3d8 = point3d62
            point3d9 = point3d63
            origin3 = Point3D.get_Origin()
            origin4 = Point3D.get_Origin()
            origin5 = Point3D.get_Origin()
        num55 = num3 + value2
        if (self.parametersPanel.cmbNavAidType.SelectedIndex != 2):
            if (self.parametersPanel.cmbNavAidType.SelectedIndex == 3):
                num8 = 25
                num9 = metres1 * 0.839099631
            else:
                num8 = 15
                num9 = metres1 * 1.191753593
        else:
            num8 = 25
            num9 = metres1 * 0.839099631
        num56 = Unit.ConvertDegToRad(num55 + num8)
        num57 = Unit.ConvertDegToRad(num55)
        point3d64 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num56, num9)
        point3d65 = MathHelper.distanceBearingPoint(point3d64, Unit.ConvertDegToRad(450) - num57, num30)
        point3d66 = MathHelper.distanceBearingPoint(point3d65, Unit.ConvertDegToRad(450) - (num57 - Unit.ConvertDegToRad(90)), num14)
        point3d67 = MathHelper.distanceBearingPoint(point3d66, Unit.ConvertDegToRad(450) - (num57 + Unit.ConvertDegToRad(40)), num14)
        point3d68 = MathHelper.distanceBearingPoint(point3d66, Unit.ConvertDegToRad(450) - (num57 - Unit.ConvertDegToRad(10)), num14)
        MathHelper.distanceBearingPoint(point3d65, Unit.ConvertDegToRad(450) - (num57 + Unit.ConvertDegToRad(90)), num27)
        MathHelper.distanceBearingPoint(point3d67, Unit.ConvertDegToRad(450) - (num57 + Unit.ConvertDegToRad(40)), num28)
        point3d69 = MathHelper.distanceBearingPoint(point3d68, Unit.ConvertDegToRad(450) - (num57 - Unit.ConvertDegToRad(10)), num29)
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d65, num27, point3d67, num28)
        point3d70 = point3d5
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d67, num28, point3d68, num29)
        point3d71 = point3d4
        num58 = MathHelper.calcDistance(point3d70, point3d71)
        num59 = math.asin(num58 / 2 / num28)
        point3d72 = MathHelper.distanceBearingPoint(point3d67, Unit.ConvertDegToRad(450) - (Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d67, point3d71) + num59), num28)
        point3d10 = MathHelper.smethod_68(point3d64, point3d72, point3d69)
        num60 = MathHelper.calcDistance(point3d10, point3d64)
        if (num26 <= max([point3d45.get_X(), point3d31.get_X()]) - min([point3d45.get_X(), point3d31.get_X()])):
            flag1 = False
            origin7 = Point3D.get_Origin()
            origin6 = Point3D.get_Origin()
        else:
            flag1 = True
            point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d10, num60, point3d45, num26)
            origin6 = point3d3
            origin7 = point3d2
        point3d11 = MathHelper.smethod_68(point3d36, point3d56, point3d7)
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d11, MathHelper.calcDistance(point3d11, point3d36), point3d67, num28)
        point3d73 = point3d3
        point3d74 = point3d2
        num61 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d10, point3d73)
        num10 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d10, point3d64) if(not flag1) else Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d10, origin7)
        num62 = (num10 + num61) / 2
        point3d75 = MathHelper.distanceBearingPoint(point3d10, Unit.ConvertDegToRad(450) - num62, num60)
        num63 = MathHelper.calcDistance(point3d31, point3d10)
        num64 = num60
        num65 = num63 * num63 - num64 * num64
        math.sqrt(math.fabs(num65))
        MathHelper.calcDistance(point3d31, point3d64)
        point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d31, 0, point3d10, num60)
        point3d12 = point3d5 if(not flag1) else origin7
        if (not flag):
            point3d13 = origin
            point3d14 = origin1
            point3d15 = origin2
            point3d16 = point3d1
            point3d17 = point3d
        else:
            point3d13 = point3d1
            point3d14 = point3d
            point3d15 = point3d
            point3d16 = point3d
            point3d17 = point3d
        num66 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d6, point3d13)
        num67 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d6, point3d74)
        point3d76 = MathHelper.distanceBearingPoint(point3d6, MathHelper.getBearing(point3d6, point3d74) + Unit.ConvertDegToRad(1), num7)
        point3d77 = point3d59
        point3d78 = point3d8
        if (num51 <= num50):
            point3d18 = origin3
            point3d19 = origin4
            point3d20 = origin5
            point3d21 = point3d9
        else:
            point3d18 = point3d9
            point3d19 = point3d9
            point3d20 = point3d9
            point3d21 = point3d9
        if (not flag1):
            point3d2, point3d3, point3d4, point3d5 = MathHelper.smethod_89(point3d31, 0, point3d45, num26)
            point3d79 = point3d3
            num68 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d45, point3d9)
            num69 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d45, point3d79)
            point3d22 = point3d79
            point3d23 = point3d31
            point3d24 = MathHelper.distanceBearingPoint(point3d45, MathHelper.getBearing(point3d45, point3d21) + MathHelper.smethod_53(MathHelper.getBearing(point3d45, point3d21), MathHelper.getBearing(point3d45, point3d22)) / 2, num26)
        else:
            num70 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d45, point3d9)
            num71 = Unit.ConvertDegToRad(450) - MathHelper.getBearing(point3d45, origin6)
            point3d22 = origin6
            point3d23 = origin7
            point3d24 = MathHelper.distanceBearingPoint(point3d45, MathHelper.getBearing(point3d45, point3d21) + MathHelper.smethod_53(MathHelper.getBearing(point3d45, point3d21), MathHelper.getBearing(point3d45, point3d22)) / 2, num26)
        x1 = point3d22.get_X()
        x2 = point3d18.get_X()
        point3d25 = MathHelper.getIntersectionPoint(point3d31, point3d32, point3d34, MathHelper.distanceBearingPoint(point3d34, MathHelper.getBearing(point3d32, point3d31) + Unit.ConvertDegToRad(90), num14))
        point3d26 = MathHelper.getIntersectionPoint(point3d31, point3d33, point3d34, MathHelper.distanceBearingPoint(point3d34, MathHelper.getBearing(point3d33, point3d31) - Unit.ConvertDegToRad(90), num14))
        polylineArea1 = PolylineArea()
        polylineArea1.Add(PolylineAreaPoint(point3d31))
        polylineArea1.Add(PolylineAreaPoint(point3d25, MathHelper.smethod_57(MathHelper.smethod_63(MathHelper.getBearing(point3d31, point3d25), MathHelper.getBearing(point3d25, point3d26), AngleUnits.Radians), point3d25, point3d26, point3d34)))
        polylineArea1.Add(PolylineAreaPoint(point3d26))
        num72 = MathHelper.calcDistance(point3d31, point3d34) / 2
        num73 = num72 + num72 / 2
        num74 = num14 / 10
        num75 = num14 / 3
        point3d80 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - 0, num72).smethod_167(0)
        point3d81 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - 0, num72 + num75).smethod_167(0)
        point3d82 = MathHelper.distanceBearingPoint(point3d81, Unit.ConvertDegToRad(450) - Unit.ConvertDegToRad(90), num74).smethod_167(0)
        point3d83 = MathHelper.distanceBearingPoint(point3d81, Unit.ConvertDegToRad(450) - Unit.ConvertDegToRad(270), num74).smethod_167(0)
        if (self.parametersPanel.cmbOrientation.currentText() != OrientationType.Left):
            point3d27 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num17, num73).smethod_167(0)
            point3d28 = MathHelper.distanceBearingPoint(point3d31, Unit.ConvertDegToRad(450) - num17, num73 + num75).smethod_167(0)
            point3d29 = MathHelper.distanceBearingPoint(point3d27, Unit.ConvertDegToRad(450) - (Unit.ConvertDegToRad(90) + num17), num74).smethod_167(0)
            point3d30 = MathHelper.distanceBearingPoint(point3d27, Unit.ConvertDegToRad(450) - (num17 - Unit.ConvertDegToRad(90)), num74).smethod_167(0)
        else:
            num76 = Unit.ConvertDegToRad(90) + (Unit.ConvertDegToRad(90) - (Unit.ConvertDegToRad(450) - num17))
            point3d27 = MathHelper.distanceBearingPoint(point3d31, num76, num73).smethod_167(0)
            point3d28 = MathHelper.distanceBearingPoint(point3d31, num76, num73 + num75).smethod_167(0)
            point3d29 = MathHelper.distanceBearingPoint(point3d27, num76 + Unit.ConvertDegToRad(90), num74).smethod_167(0)
            point3d30 = MathHelper.distanceBearingPoint(point3d27, num76 - Unit.ConvertDegToRad(90), num74).smethod_167(0)
        if (x1 > x2):
            if (not flag):
                point3dArray = [point3d12, point3d73, point3d74, point3d13, point3d14, point3d16, point3d17, point3d78, point3d23]
                polylineArea = PolylineArea(point3dArray)
                polylineArea.method_19(0, MathHelper.smethod_60(point3d12, point3d75, point3d73))
                polylineArea.method_19(2, MathHelper.smethod_60(point3d74, point3d76, point3d13))
                polylineArea.method_19(4, MathHelper.smethod_60(point3d14, point3d15, point3d16))
                polylineArea.method_19(6, MathHelper.smethod_60(point3d17, point3d77, point3d78))
            else:
                point3dArray = [point3d12, point3d73, point3d74, point3d13, point3d17, point3d78, point3d23]
                polylineArea = PolylineArea(point3dArray)
                polylineArea.method_19(0, MathHelper.smethod_60(point3d12, point3d75, point3d73))
                polylineArea.method_19(2, MathHelper.smethod_60(point3d74, point3d76, point3d13))
                polylineArea.method_19(4, MathHelper.smethod_60(point3d17, point3d77, point3d78))
        elif (flag):
            if (num51 <= num50):
                point3dArray = [point3d12, point3d73, point3d74, point3d13, point3d17, point3d78, point3d18, point3d20, point3d21, point3d22, point3d23]
                polylineArea = PolylineArea(point3dArray)
                polylineArea.method_19(0, MathHelper.smethod_60(point3d12, point3d75, point3d73))
                polylineArea.method_19(2, MathHelper.smethod_60(point3d74, point3d76, point3d13))
                polylineArea.method_19(4, MathHelper.smethod_60(point3d17, point3d77, point3d78))
                polylineArea.method_19(6, MathHelper.smethod_60(point3d18, point3d19, point3d20))
                polylineArea.method_19(8, MathHelper.smethod_60(point3d21, point3d24, point3d22))
            else:
                point3dArray = [point3d12, point3d73, point3d74, point3d13, point3d17, point3d78, point3d21, point3d22, point3d23]
                polylineArea = PolylineArea(point3dArray)
                polylineArea.method_19(0, MathHelper.smethod_60(point3d12, point3d75, point3d73))
                polylineArea.method_19(2, MathHelper.smethod_60(point3d74, point3d76, point3d13))
                polylineArea.method_19(4, MathHelper.smethod_60(point3d17, point3d77, point3d78))
                polylineArea.method_19(6, MathHelper.smethod_60(point3d21, point3d24, point3d22))
        elif (num51 <= num50):
            point3dArray = [point3d12, point3d73, point3d74, point3d13, point3d14, point3d16, point3d17, point3d78, point3d18, point3d20, point3d21, point3d22, point3d23]
            polylineArea = PolylineArea(point3dArray)
            polylineArea.method_19(0, MathHelper.smethod_60(point3d12, point3d75, point3d73))
            polylineArea.method_19(2, MathHelper.smethod_60(point3d74, point3d76, point3d13))
            polylineArea.method_19(4, MathHelper.smethod_60(point3d14, point3d15, point3d16))
            polylineArea.method_19(6, MathHelper.smethod_60(point3d17, point3d77, point3d78))
            polylineArea.method_19(8, MathHelper.smethod_60(point3d18, point3d19, point3d20))
            polylineArea.method_19(10, MathHelper.smethod_60(point3d21, point3d24, point3d22))
        else:
            point3dArray = [point3d12, point3d73, point3d74, point3d13, point3d14, point3d16, point3d17, point3d78, point3d21, point3d22, point3d23]
            polylineArea = PolylineArea(point3dArray)
            polylineArea.method_19(0, MathHelper.smethod_60(point3d12, point3d75, point3d73))
            polylineArea.method_19(2, MathHelper.smethod_60(point3d74, point3d76, point3d13))
            polylineArea.method_19(4, MathHelper.smethod_60(point3d14, point3d15, point3d16))
            polylineArea.method_19(6, MathHelper.smethod_60(point3d17, point3d77, point3d78))
            polylineArea.method_19(8, MathHelper.smethod_60(point3d21, point3d24, point3d22))
        mapUnits = define._canvas.mapUnits()
        self.constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
 
        matrix3d = Matrix3d.MirroringFromVector3d(point3d31, Vector3d(0, 1, 0))
        matrix3d1 = Matrix3d.Rotation(-Unit.ConvertDegToRad(float(self.parametersPanel.txtTrackRadial.Value) + 90), Vector3d(0, 0, 1), point3d31)
        polyline = PolylineArea.smethod_136(polylineArea1, True)
        polyline1 = PolylineArea.smethod_136(polylineArea, True)
        
        polylineTemp = polyline
        polylineTemp1 = polyline1
        offsetDist = 4600
        if (self.parametersPanel.cmbOrientation.currentText() == OrientationType.Left):
            polylineTemp = polyline.TransformBy(matrix3d)
            polylineTemp1 = polyline1.TransformBy(matrix3d)
            offsetDist = -4600
        polylineTemp = polylineTemp.TransformBy(matrix3d1)
        polylineTemp1 = polylineTemp1.TransformBy(matrix3d1)

        # offsetCurvePointArray = polylineTemp1.getOffsetCurve(4600)


        offsetCurvePointArray = QgisHelper.offsetCurve(polylineTemp1.method_14_closed(4), offsetDist)
        
        AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, polylineTemp)
        AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, polylineTemp1)
        AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, PolylineArea(offsetCurvePointArray))
        QgisHelper.appendToCanvas(define._canvas, [self.constructionLayer], SurfaceTypes.BaseTurnTC)
        QgisHelper.zoomToLayers([self.constructionLayer])
        self.resultLayerList = [self.constructionLayer]
        self.ui.btnEvaluate.setEnabled(True)


class BaseTurnTSArea:
    def __init__(self, polylineArea_0, altitude_0):
        self.area = PrimaryObstacleArea(polylineArea_0)
        self.moc = altitude_0.Metres
    
    
    def get_area(self):
        return self.area
    Area = property(get_area, None, None, None)
    
    def get_moc(self):
        return self.moc
    Moc = property(get_moc, None, None, None)

    def method_0(self, obstacle_0):
        double_0 = self.moc * obstacle_0.MocMultiplier
        double_1 = None
        if (not self.area.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
            return (False, double_0, double_1)
        position = obstacle_0.Position
        double_1 = position.get_Z() + obstacle_0.Trees + double_0
        return (True, double_0, double_1)
    

class BaseTurnTSSecondaryEvaluator:
    def __init__(self, polylineArea_0, altitude_0, altitude_1, distance_0):
        self.inner = PrimaryObstacleArea(polylineArea_0)
        self.outer = PrimaryObstacleArea(PolylineArea(QgisHelper.offsetCurve(polylineArea_0.method_14_closed(4), 4600)))
        self.poly = PolylineArea.smethod_131(self.inner.previewArea)
        self.altitude = altitude_0.Metres
        self.moc = altitude_1.Metres
        self.offset = distance_0
class BaseTurnTSObstacles(ObstacleTable):
    def __init__(self, bool_0, typeStr, surfacesList = None, altitude = None, inner = None, outer = None, poly = None, altitude_1 = None, distance_0 = None):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
         
        self.surfaceType = SurfaceTypes.BaseTurnTC
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
            criticalObstacleType = CriticalObstacleType.No
            for current in self.surfacesList:
                result, num, num1 = current.method_0
                if (result):
                    if (num1 > self.altitude):
                        criticalObstacleType = CriticalObstacleType.Yes
                    checkResult = []
                    checkResult.append(num)
                    checkResult.append(num1)
                    checkResult.append(criticalObstacleType)
                    self.addObstacleToModel(obstacle_0, checkResult)
                    break
        else:
            mocMultiplier = self.moc * obstacle_0.MocMultiplier
            metres = None
            num = None
            obstacleAreaResult = ObstacleAreaResult.Outside
            if (not self.inner.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance)):
                num = MathHelper.calcDistance(self.poly.getClosestPointTo(obstacle_0.Position, False), obstacle_0.Position) - obstacle_0.Tolerance
                if (num > self.offset.Metres):
                    return
                metres = mocMultiplier * (1 - num / self.offset.Metres)
                obstacleAreaResult = ObstacleAreaResult.Secondary
            else:
                metres = mocMultiplier
                obstacleAreaResult = ObstacleAreaResult.Primary
            position = obstacle_0.Position
            z = position.get_Z() + obstacle_0.Trees + metres
            criticalObstacleType = CriticalObstacleType.No
            if (z > self.altitude):
                criticalObstacleType = CriticalObstacleType.Yes
            checkResult = []
            checkResult.append(obstacleAreaResult)
            checkResult.append(num)
            checkResult.append(metres)
            checkResult.append(z)
            checkResult.append(criticalObstacleType)
            self.addObstacleToModel(obstacle_0, checkResult)