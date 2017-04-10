'''
Created on Feb 20, 2015

@author: KangKuk
'''

from qgis.core import QGis, QgsVectorLayer, QgsFeature, QgsGeometry, QgsVectorFileWriter
from PyQt4.QtCore import QString
from FlightPlanner.RnavTolerance0 import RnavGnssTolerance
from FlightPlanner.polylineArea import PolylineArea
from FlightPlanner.helpers import MathHelper, Unit, Altitude, Distance, Speed
from FlightPlanner.types import ObstacleAreaResult, CriticalObstacleType, RnavSegmentType,\
    RnavGnssFlightPhase, RnavSpecification, AngleUnits, TurnDirection, DistanceUnits,\
    AircraftSpeedCategory, IntersectionStatus, RnavWaypointType, RnavFlightPhase, SpeedUnits
from FlightPlanner.messages import Messages
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, SecondaryObstacleArea, SecondaryAreaArc
from FlightPlanner.BasicGNSS.windSpiral import WindSpiral
from FlightPlanner.BasicGNSS.rnavWaypoints import RnavWaypoints
from FlightPlanner.AcadHelper import AcadHelper

import define

import math, time

class IGnssSegment:
    def __init__(self):
#         Point3dCollection selectionArea;
        self.selectionArea = None
#             protected List<PrimaryObstacleArea> primary;
        self.primary = None
#             protected List<SecondaryObstacleArea> secondary;
        self.secondary = None
#             protected List<PolylineArea> drawingLines;
        self.drawingLines = None
#             protected PolylineArea nominalLine;
        self.nominalLine = None
#             protected double primaryMoc;
        self.primaryMoc = 0.0
#             protected List<Symbol> waypoints;
        self.waypoints = None
        
        self.Type = 0
#             public virtual void vmethod_0(Obstacle obstacle_0, BasicGnssApproachObstacleAnalyser.GnssSegmentObstacles gnssSegmentObstacles_0)
#             {
    def vmethod_0(self, obstacle_0):
        if define._units == QGis.Meters: 
            obstPosition = obstacle_0.position
        else:
            obstPosition = obstacle_0.positionDegree    
#         startTime = time.time()       
        if (MathHelper.pointInPolygon(self.selectionArea, obstPosition, obstacle_0.tolerance)):
#             endTime = time.time()
#             print "pointInPolygon = " + str(endTime - startTime) 
            obstacleAreaResult = ObstacleAreaResult.Outside
            mocMultiplier = self.primaryMoc * obstacle_0.mocMultiplier
            for primaryObstacleArea in self.primary:
                return2 = []
                obstacleAreaResult = primaryObstacleArea.imethod_1(obstPosition, obstacle_0.tolerance, mocMultiplier, return2)
                if (obstacleAreaResult != ObstacleAreaResult.Primary):
                    continue
                
                num = return2[0]
                num1 = return2[1]
                position = obstPosition
#                 gnssSegmentObstacles_0.method_11(obstacle0, obstacleAreaResult, num1, num, position.z() + obstacle_0.trees + num, CriticalObstacleType.No)
                return [obstacleAreaResult, num1, None, num, position.z() + obstacle_0.trees + num, CriticalObstacleType.No, self.Type]
            
            num = 0.0
            num1 = None
            obstacleAreaResult = ObstacleAreaResult.Outside
            for current in self.secondary:
                if (current.area != None):
                    return2 = []
                    obstacleAreaResult1 = current.imethod_1(obstPosition, obstacle_0.tolerance, mocMultiplier, return2)
                    if (obstacleAreaResult1 != ObstacleAreaResult.Outside):
                        if len(return2) < 2:
                            return None
                        num2 = return2[0]
                        num3 = return2[1]
                        if (num2 > num or num == 0.0):
                            num = num2
                            num1 = num3
                            obstacleAreaResult = obstacleAreaResult1
                        
                        if (obstacleAreaResult1 == ObstacleAreaResult.Primary):
                            num = num2
                            num1 = None
                            obstacleAreaResult = ObstacleAreaResult.Primary
                            break
            return [obstacleAreaResult, num1, None, num, obstPosition.z() + obstacle_0.trees + num, CriticalObstacleType.No, self.Type]
        return None
#             if (obstacleAreaResult != ObstacleAreaResult.Outside):
#                 obstacle = obstacle_0
#                 point3d = obstPosition
#                 gnssSegmentObstacles_0.method_11(obstacle, obstacleAreaResult, num1, num, point3d.get_Z() + obstacle_0.trees + num, CriticalObstacleType.No)
                

#             public virtual void vmethod_1(Transaction transaction_0, BlockTableRecord blockTableRecord_0, string string_0)
#             {
    def vmethod_1(self, string_0, mapLayers):
        string_0 = string_0 + "_" + self.Type
        resultLayer = AcadHelper.createVectorLayer(string_0, QGis.Line)
        for drawingLine in self.drawingLines:
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, drawingLine)
        mapLayers.append(resultLayer)
    def drawPrimary(self, layerNamePrefix, mapLayers):
        string_0 = layerNamePrefix + "_" + self.Type + "_PrimaryArea"
        resultLayer = AcadHelper.createVectorLayer(string_0, QGis.Line)
        for drawingLine in self.primary:
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, drawingLine)
        mapLayers.append(resultLayer)
    def drawSecondary(self, layerNamePrefix, mapLayers):
        string_0 = layerNamePrefix + "_" + self.Type + "_SecondaryArea"

        mapUnits = define._canvas.mapUnits()
        
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                resultLayer = QgsVectorLayer("polygon?crs=EPSG:32633", string_0, "memory")
            else:
                resultLayer = QgsVectorLayer("polygon?crs=EPSG:4326", string_0, "memory")
        else:
            resultLayer = QgsVectorLayer("polygon?crs=%s"%define._mapCrs.authid (), string_0, "memory")


        shpPath = ""
        if define.obstaclePath != None:
            shpPath = define.obstaclePath
        elif define.xmlPath != None:
            shpPath = define.xmlPath
        else:
            shpPath = define.appPath
        er = QgsVectorFileWriter.writeAsVectorFormat(resultLayer, shpPath + "/" + QString(string_0).replace(" ", "") + ".shp", "utf-8", resultLayer.crs())
        resultLayer = QgsVectorLayer(shpPath + "/" + QString(string_0).replace(" ", "") + ".shp", string_0, "ogr")

#         if mapUnits == QGis.Meters:
#             resultLayer = QgsVectorLayer("linestring?crs=EPSG:32633", string_0, "memory")
#         else:
#             resultLayer = QgsVectorLayer("linestring?crs=EPSG:4326", string_0, "memory")

        resultLayer.startEditing()

#         AcadHelper.smethod_42(blockTableRecord_0.get_Database(), string_0, num);
        for drawingLine in self.secondary:
            feature = QgsFeature()
#             drawingLine = drawingLine as list
            try:
                if isinstance(drawingLine.area, SecondaryAreaArc):
                    feature.setGeometry( QgsGeometry.fromPolyline(drawingLine.area.getArea()) )
            except TypeError:
                pass
            pr = resultLayer.dataProvider()
            pr.addFeatures([feature])
            # resultLayer.addFeature(feature)

        resultLayer.commitChanges()
        mapLayers.append(resultLayer)

    def vmethod_3(self):
        for primaryObstacleArea in self.primary:
            primaryObstacleArea.imethod_3()
        for secondaryObstacleArea in self.secondary:
            secondaryObstacleArea.imethod_3()

    def vmethod_4(self, gnssSegmentObstacles_0):
        pass

class FinalApproachSegment(IGnssSegment):
#             public FinalApproachSegment(Position position_0, Position position_1, Position position_2, Position position_3, RnavSpecification rnavSpecification_0, AircraftSpeedCategory aircraftSpeedCategory_0, Altitude altitude_0)
#             { 
    def __init__(self, position_0, position_1, position_2, position_3, rnavSpecification_0, aircraftSpeedCategory_0, altitude_0):
        self.Type = RnavSegmentType.FinalApproach
        self.drawingLines = []
        self.primary = []
        self.secondary = []
        self.selectionArea = []
        
        point3d19 = position_1
        point3d20 = position_2
        if position_0 == None:
            point3d = MathHelper.distanceBearingPoint(point3d19, MathHelper.getBearing(point3d20, point3d19), Unit.ConvertNMToMeter(5))
        else:
            point3d = position_0
            
        point3d21 = position_3
        self.primaryMoc = altitude_0
        num = MathHelper.getBearing(point3d, point3d19)
        num1 = MathHelper.smethod_4(num + 1.5707963267949)
        num2 = MathHelper.smethod_4(num - 1.5707963267949)
        num3 = MathHelper.smethod_4(num + 3.14159265358979)
        num4 = MathHelper.getBearing(point3d19, point3d20)
        num5 = MathHelper.smethod_4(num4 + 1.5707963267949)
        num6 = MathHelper.smethod_4(num4 - 1.5707963267949)
        num7 = MathHelper.smethod_4(num4 + 3.14159265358979)
        num8 = Unit.ConvertDegToRad(30)
        if MathHelper.calcDistance(point3d21, point3d20) > Unit.ConvertNMToMeter(10):            
            raise UserWarning, Messages.ERR_DISTANCE_BETWEEN_X_AND_ARP_EXCEEDS_10_NM%"RnavCommonWaypoint_MAWP"
#         self.waypoints.Add(new Symbol(SymbolType.Flyb));
#         self.waypoints.Add(new Symbol(SymbolType.Flyo));
#         self.waypoints[0].Tag = point3d19;
#         self.waypoints[1].Tag = point3d20;
#         if (!Geo.DatumLoaded)
#         {
#             Symbol item = self.waypoints[0];
#             rnavCommonWaypointFAWP = new string[] { Enums.RnavCommonWaypoint_FAWP };
#             item.Attributes = new SymbolAttributes(rnavCommonWaypointFAWP);
#             Symbol symbolAttribute = self.waypoints[1];
#             rnavCommonWaypointFAWP = new string[] { Enums.RnavCommonWaypoint_MAWP };
#             symbolAttribute.Attributes = new SymbolAttributes(rnavCommonWaypointFAWP);
#         }
#         else
#         {
#             position_1.method_1(out degree, out degree1);
#             Symbol symbol = self.waypoints[0];
#             rnavCommonWaypointFAWP = new string[] { Enums.RnavCommonWaypoint_FAWP, degree.ToString(), degree1.ToString() };
#             symbol.Attributes = new SymbolAttributes(rnavCommonWaypointFAWP);
#             position_2.method_1(out degree, out degree1);
#             Symbol item1 = self.waypoints[1];
#             rnavCommonWaypointFAWP = new string[] { Enums.RnavCommonWaypoint_MAWP, degree.ToString(), degree1.ToString() };
#             item1.Attributes = new SymbolAttributes(rnavCommonWaypointFAWP);
#         }
        rnavGnssTolerance = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0)
        metres = rnavGnssTolerance.getASWMetres()
        metres1 = rnavGnssTolerance.getATTMetres()
        metres2 = rnavGnssTolerance.getXTTMetres()
        rnavGnssTolerance1 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Faf, aircraftSpeedCategory_0);
        metres3 = rnavGnssTolerance1.getASWMetres()
        metres4 = rnavGnssTolerance1.getATTMetres()
        metres5 = rnavGnssTolerance1.getXTTMetres()
        rnavGnssTolerance2 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Mapt, aircraftSpeedCategory_0);
        metres6 = rnavGnssTolerance2.getASWMetres()
        metres7 = rnavGnssTolerance2.getATTMetres()
        metres8 = rnavGnssTolerance2.getXTTMetres()
        point3d22 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d19, num4, metres4), num6, metres5)
        point3d23 = MathHelper.distanceBearingPoint(point3d22, num7, metres4 * 2)
        point3d24 = MathHelper.distanceBearingPoint(point3d23, num5, metres5 * 2)
        point3d25 = MathHelper.distanceBearingPoint(point3d24, num4, metres4 * 2)
        point3d26 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d20, num4, metres7), num6, metres8);
        point3d27 = MathHelper.distanceBearingPoint(point3d26, num7, metres7 * 2)
        point3d28 = MathHelper.distanceBearingPoint(point3d27, num5, metres8 * 2)
        point3d29 = MathHelper.distanceBearingPoint(point3d28, num4, metres7 * 2)
        return1 = []
        num9 = MathHelper.smethod_77(Unit.smethod_1(num), Unit.smethod_1(num4), AngleUnits.Degrees, return1)
        turnDirection = return1[0]
        if (turnDirection == TurnDirection.Nothing or num9 < 0.5):
            point3d30 = MathHelper.distanceBearingPoint(point3d19, num6, metres3);
            point3d31 = MathHelper.distanceBearingPoint(point3d19, num6, metres3 / 2);
            point3d32 = MathHelper.distanceBearingPoint(point3d19, num5, metres3);
            point3d33 = MathHelper.distanceBearingPoint(point3d19, num5, metres3 / 2);
            point3d34 = MathHelper.distanceBearingPoint(point3d30, num4 + num8, (metres3 - metres6) / math.sin(num8));
            point3d35 = MathHelper.distanceBearingPoint(point3d34, num5, metres6 / 2);
            point3d36 = MathHelper.distanceBearingPoint(point3d32, num4 - num8, (metres3 - metres6) / math.sin(num8));
            point3d37 = MathHelper.distanceBearingPoint(point3d36, num6, metres6 / 2);
            point3d38 = MathHelper.distanceBearingPoint(point3d30, num7 + num8, metres4 / math.cos(num8));
            point3d39 = MathHelper.distanceBearingPoint(point3d32, num7 - num8, metres4 / math.cos(num8));
            point3d1 = MathHelper.getIntersectionPoint(point3d38, point3d39, point3d31, point3d35)
            point3d2 = MathHelper.getIntersectionPoint(point3d38, point3d39, point3d33, point3d37)
            point3d40 = MathHelper.distanceBearingPoint(point3d20, num6, metres6);
            point3d41 = MathHelper.distanceBearingPoint(point3d20, num6, metres6 / 2);
            point3d42 = MathHelper.distanceBearingPoint(point3d20, num5, metres6);
            point3d43 = MathHelper.distanceBearingPoint(point3d20, num5, metres6 / 2);
            point3dArray = [point3d38, point3d30, point3d34, point3d40 ]
            self.drawingLines.append(point3dArray)
            point3dArray = [point3d1, point3d31, point3d35, point3d41]
            self.drawingLines.append(point3dArray)
            point3dArray = [point3d39, point3d32, point3d36, point3d42 ]
            self.drawingLines.append(point3dArray)
            point3dArray = [point3d2, point3d33, point3d37, point3d43]
            self.drawingLines.append(point3dArray)
            point3dArray = [point3d38, point3d39]
            self.drawingLines.append(point3dArray)
            point3dArray = [point3d40, point3d42]
            self.drawingLines.append(point3dArray)
            self.selectionArea.extend([point3d38, point3d30, point3d34, point3d40, point3d42, point3d36, point3d32, point3d39])
            point3dArray = [point3d1, point3d31, point3d35, point3d41, point3d43, point3d37, point3d33, point3d2]
            polylineArea = PolylineArea(point3dArray)
            self.primary.append(PrimaryObstacleArea(polylineArea))
            self.secondary.append(SecondaryObstacleArea(point3d1, point3d35, point3d38, point3d34, num4))
            self.secondary.append(SecondaryObstacleArea(point3d2, point3d37, point3d39, point3d36, num4))
            self.secondary.append(SecondaryObstacleArea(point3d35, point3d41, point3d34, point3d40, num4))
            self.secondary.append(SecondaryObstacleArea(point3d37, point3d43, point3d36, point3d42, num4))
        else:
            point3d44 = MathHelper.distanceBearingPoint(point3d19, num2, metres3);
            point3d45 = MathHelper.distanceBearingPoint(point3d19, num2, metres3 / 2);
            point3d46 = MathHelper.distanceBearingPoint(point3d19, num1, metres3);
            point3d47 = MathHelper.distanceBearingPoint(point3d19, num1, metres3 / 2);
            point3d48 = MathHelper.distanceBearingPoint(point3d44, num3 + num8, (metres - metres3) / math.sin(num8));
            point3d49 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d19, num3, (metres - metres3) / math.tan(num8)), num2, metres / 2)
            point3d50 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d19, num3, (metres - metres3) / math.tan(num8)), num1, metres / 2)
            point3d51 = MathHelper.distanceBearingPoint(point3d46, num3 - num8, (metres - metres3) / math.sin(num8))
            point3d52 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d19, num3, metres4), num2, metres / 2)
            point3d53 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d19, num3, metres4), num1, metres / 2)
            point3d54 = MathHelper.distanceBearingPoint(point3d19, num6, metres3)
            point3d55 = MathHelper.distanceBearingPoint(point3d19, num6, metres3 / 2)
            point3d56 = MathHelper.distanceBearingPoint(point3d19, num5, metres3)
            point3d57 = MathHelper.distanceBearingPoint(point3d19, num5, metres3 / 2)
            point3d58 = MathHelper.distanceBearingPoint(point3d54, num4 + num8, (metres3 - metres6) / math.sin(num8))
            point3d59 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d19, num4, (metres3 - metres6) / math.tan(num8)), num6, metres6 / 2)
            point3d60 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d19, num4, (metres3 - metres6) / math.tan(num8)), num5, metres6 / 2)
            point3d61 = MathHelper.distanceBearingPoint(point3d56, num4 - num8, (metres3 - metres6) / math.sin(num8))
            point3d62 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d19, num7, metres4), num6, metres / 2)
            point3d63 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d19, num7, metres4), num5, metres / 2)
            point3d64 = point3d58
            point3d65 = point3d59
            point3d66 = point3d61
            point3d67 = point3d60
            point3d68 = MathHelper.distanceBearingPoint(point3d20, num6, metres6)
            point3d69 = MathHelper.distanceBearingPoint(point3d20, num6, metres6 / 2)
            point3d70 = MathHelper.distanceBearingPoint(point3d20, num5, metres6)
            point3d71 = MathHelper.distanceBearingPoint(point3d20, num5, metres6 / 2)
            point3d15 = MathHelper.getIntersectionPoint(point3d52, point3d53, point3d62, point3d63)
            if (turnDirection != TurnDirection.Right):
                point3d3 = MathHelper.getIntersectionPoint(point3d48, point3d44, point3d62, point3d63)
                point3d6 = MathHelper.getIntersectionPoint(point3d49, point3d45, point3d62, point3d63)
                point3d9 = MathHelper.getIntersectionPoint(point3d51, point3d46, point3d52, point3d53)
                point3d12 = MathHelper.getIntersectionPoint(point3d50, point3d47, point3d52, point3d53)
                point3d4 = MathHelper.getIntersectionPoint(point3d48, point3d44, point3d54, point3d56)
                point3d7 = MathHelper.getIntersectionPoint(point3d49, point3d45, point3d54, point3d56)
                point3d10 = point3d46
                point3d13 = point3d47
                point3d5 = MathHelper.getIntersectionPoint(point3d54, point3d58, point3d44, point3d46)
                point3d8 = MathHelper.getIntersectionPoint(point3d55, point3d59, point3d44, point3d46)
                point3d11 = point3d56
                point3d14 = point3d57
                point3dArray = [point3d3, point3d4, point3d5, point3d64, point3d68]
                self.drawingLines.append(point3dArray)
                point3dArray = [point3d6, point3d7, point3d8, point3d65, point3d69]
                self.drawingLines.append(point3dArray)
                point3dArray = [point3d12, point3d13, point3d14, point3d67, point3d71]
                self.drawingLines.append(point3dArray)
                point3dArray = [point3d9, point3d10, point3d11, point3d66, point3d70]
                self.drawingLines.append(point3dArray)
                point3dArray = [point3d3, point3d15, point3d9]
                self.drawingLines.append(point3dArray)
                point3dArray = [point3d68, point3d70]
                self.drawingLines.append(point3dArray)
                self.drawingLines[2][1].bulge = MathHelper.smethod_57(TurnDirection.Left, point3d13, point3d14, point3d19);
                self.drawingLines[3][1].bulge = MathHelper.smethod_57(TurnDirection.Left, point3d10, point3d11, point3d19);
                point3d18 = MathHelper.getIntersectionPoint(point3d10, MathHelper.distanceBearingPoint(point3d10, num, 100), point3d11, MathHelper.distanceBearingPoint(point3d11, num7, 100))
                self.selectionArea.extend([point3d3, point3d4, point3d5, point3d64, point3d68, point3d70, point3d66, point3d11, point3d18, point3d10, point3d9, point3d15])
                point3d16 = MathHelper.distanceBearingPoint(point3d19, MathHelper.getBearing(point3d19, point3d18), metres3);
                point3d17 = MathHelper.distanceBearingPoint(point3d19, MathHelper.getBearing(point3d19, point3d18), metres3 / 2);
                point3dArray = [point3d6, point3d7, point3d8, point3d65, point3d69, point3d71, point3d67, point3d14, point3d13, point3d12, point3d15]
                polylineArea = PolylineArea(point3dArray)
                polylineArea[7].Bulge = MathHelper.smethod_57(TurnDirection.Right, point3d14, point3d13, point3d19);
                self.primary.append(PrimaryObstacleArea(polylineArea))
                self.secondary.append(SecondaryObstacleArea(point3d6, point3d7, point3d3, point3d4, num))
                self.secondary.append(SecondaryObstacleArea(point3d12, point3d13, point3d9, point3d10, num))
                self.secondary.append(SecondaryObstacleArea(point3d7, point3d8, point3d4, point3d5, num))
                self.secondary.append(SecondaryObstacleArea(point3d13, point3d17, point3d14, point3d10, 0.0, point3d16, point3d11))
                self.secondary.append(SecondaryObstacleArea(point3d8, point3d65, point3d5, point3d64, num4))
                self.secondary.append(SecondaryObstacleArea(point3d14, point3d67, point3d11, point3d66, num4))
                self.secondary.append(SecondaryObstacleArea(point3d65, point3d69, point3d64, point3d68, num4))
                self.secondary.append(SecondaryObstacleArea(point3d67, point3d71, point3d66, point3d70, num4))
            else:
                point3d3 = MathHelper.getIntersectionPoint(point3d48, point3d44, point3d52, point3d53)
                point3d6 = MathHelper.getIntersectionPoint(point3d49, point3d45, point3d52, point3d53)
                point3d9 = MathHelper.getIntersectionPoint(point3d51, point3d46, point3d62, point3d63)
                point3d12 = MathHelper.getIntersectionPoint(point3d50, point3d47, point3d62, point3d63)
                point3d4 = point3d44
                point3d7 = point3d45
                point3d10 = MathHelper.getIntersectionPoint(point3d51, point3d46, point3d54, point3d56)
                point3d13 = MathHelper.getIntersectionPoint(point3d50, point3d47, point3d54, point3d56)
                point3d5 = point3d54
                point3d8 = point3d55
                point3d11 = MathHelper.getIntersectionPoint(point3d56, point3d61, point3d44, point3d46)
                point3d14 = MathHelper.getIntersectionPoint(point3d57, point3d60, point3d44, point3d46)
                point3dArray = [point3d3, point3d4, point3d5, point3d64, point3d68]
                self.drawingLines.append(point3dArray)
                point3dArray = [point3d6, point3d7, point3d8, point3d65, point3d69]
                self.drawingLines.append(point3dArray)
                point3dArray = [point3d12, point3d13, point3d14, point3d67, point3d71]
                self.drawingLines.append(point3dArray)
                point3dArray = [point3d9, point3d10, point3d11, point3d66, point3d70]
                self.drawingLines.append(point3dArray)
                point3dArray = [point3d3, point3d15, point3d9]
                self.drawingLines.append(point3dArray)
                point3dArray = [point3d68, point3d70]
                self.drawingLines.append(point3dArray)
                self.drawingLines[0][1].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d4, point3d5, point3d19)
                self.drawingLines[1][1].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d7, point3d8, point3d19)
                point3d18 = MathHelper.getIntersectionPoint(point3d4, MathHelper.distanceBearingPoint(point3d4, num, 100), point3d5, MathHelper.distanceBearingPoint(point3d5, num7, 100))
                self.selectionArea.extend([point3d3, point3d4, point3d18, point3d5, point3d64, point3d68, point3d70, point3d66, point3d11, point3d10, point3d9, point3d15])
                point3d16 = MathHelper.distanceBearingPoint(point3d19, MathHelper.getBearing(point3d19, point3d18), metres3);
                point3d17 = MathHelper.distanceBearingPoint(point3d19, MathHelper.getBearing(point3d19, point3d18), metres3 / 2);
                point3dArray = [point3d6, point3d7, point3d8, point3d65, point3d69, point3d71, point3d67, point3d14, point3d13, point3d12, point3d15]
                polylineArea1 = PolylineArea(point3dArray)
                polylineArea1[1].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d7, point3d8, point3d19)
                self.primary.append(PrimaryObstacleArea(polylineArea1))
                self.secondary.append(SecondaryObstacleArea(point3d6, point3d7, point3d3, point3d4, num))
                self.secondary.append(SecondaryObstacleArea(point3d12, point3d13, point3d9, point3d10, num))
                self.secondary.append(SecondaryObstacleArea(point3d7, point3d17, point3d8, point3d4, 0.0, point3d16, point3d5))
                self.secondary.append(SecondaryObstacleArea(point3d13, point3d14, point3d10, point3d11, num))
                self.secondary.append(SecondaryObstacleArea(point3d8, point3d65, point3d5, point3d64, num4))
                self.secondary.append(SecondaryObstacleArea(point3d14, point3d67, point3d11, point3d66, num4))
                self.secondary.append(SecondaryObstacleArea(point3d65, point3d69, point3d64, point3d68, num4))
                self.secondary.append(SecondaryObstacleArea(point3d67, point3d71, point3d66, point3d70, num4))

        point3dArray = [point3d22, point3d23, point3d24, point3d25, point3d22]
        self.drawingLines.append(point3dArray)
        point3dArray = [point3d26, point3d27, point3d28, point3d29, point3d26]
        self.drawingLines.append(point3dArray)
        point3dArray = [point3d19, point3d20]
        self.nominalLine = PolylineArea(point3dArray)

#             public override void vmethod_4(BasicGnssApproachObstacleAnalyser.GnssSegmentObstacles gnssSegmentObstacles_0)
#             {
    def vmethod_4(self, gnssSegmentObstacles_0):
        gnssSegmentObstacles_0.method_15()

class IntermediateSegment(IGnssSegment):

    def __init__(self, position_0, position_1, position_2, position_3, rnavSpecification_0, aircraftSpeedCategory_0, altitude_0):
        self.Type = RnavSegmentType.Intermediate
        self.drawingLines = []
        self.selectionArea = []
        self.primary = []
        self.secondary = []
        
        rnavCommonWaypointIWP = []
        point3dArray = []
        point3d32 = position_1
        point3d33 = position_2
        point3d34 = position_3
        if position_0 == None:
            point3d = MathHelper.distanceBearingPoint(point3d32, MathHelper.getBearing(point3d33, point3d32), Unit.ConvertNMToMeter(5)) 
        else:
            point3d = position_0
            
        self.primaryMoc = altitude_0.Metres
        num = MathHelper.getBearing(point3d, point3d32)
        num1 = MathHelper.smethod_4(num + 1.5707963267949)
        num2 = MathHelper.smethod_4(num - 1.5707963267949)
        num3 = MathHelper.smethod_4(num + 3.14159265358979)
        num4 = MathHelper.getBearing(point3d32, point3d33)
        num5 = MathHelper.smethod_4(num4 + 1.5707963267949)
        num6 = MathHelper.smethod_4(num4 - 1.5707963267949)
        num7 = MathHelper.smethod_4(num4 + 3.14159265358979)
        num8 = MathHelper.getBearing(point3d33, point3d34)
        num9 = MathHelper.smethod_4(num8 + 1.5707963267949)
        num10 = MathHelper.smethod_4(num8 - 1.5707963267949)
        num11 = MathHelper.smethod_4(num8 + 3.14159265358979)
        num12 = Unit.ConvertDegToRad(30)
        rnavGnssTolerance = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0)
        metres = rnavGnssTolerance.getASWMetres()
        metres1 = rnavGnssTolerance.getATTMetres()
        metres2 = rnavGnssTolerance.getXTTMetres()
        rnavGnssTolerance1 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Faf, aircraftSpeedCategory_0)
        metres3 = rnavGnssTolerance1.getASWMetres()
        metres4 = rnavGnssTolerance1.getATTMetres()
        metres5 = rnavGnssTolerance1.getXTTMetres()
        rnavGnssTolerance2 = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0)
        metres6 = rnavGnssTolerance2.getASWMetres()
        metres7 = rnavGnssTolerance2.getATTMetres()
        metres8 = rnavGnssTolerance2.getXTTMetres()
        rnavGnssTolerance3 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Mapt, aircraftSpeedCategory_0)
        metres9 = rnavGnssTolerance3.getASWMetres()
        metres10 = rnavGnssTolerance3.getATTMetres()
        metres11 = rnavGnssTolerance3.getXTTMetres()
        point3d35 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d32, num4, metres1), num6, metres2)
        point3d36 = MathHelper.distanceBearingPoint(point3d35, num7, metres1 * 2);
        point3d37 = MathHelper.distanceBearingPoint(point3d36, num5, metres2 * 2);
        point3d38 = MathHelper.distanceBearingPoint(point3d37, num4, metres1 * 2);
        point3d39 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d33, num4, metres4), num6, metres5);
        point3d40 = MathHelper.distanceBearingPoint(point3d39, num7, metres4 * 2);
        point3d41 = MathHelper.distanceBearingPoint(point3d40, num5, metres5 * 2);
        point3d42 = MathHelper.distanceBearingPoint(point3d41, num4, metres4 * 2);
#         self.waypoints.Add(new Symbol(SymbolType.Flyb));
#         self.waypoints[0].Tag = point3d32;
#         if (!Geo.DatumLoaded)
#         {
#             Symbol item = self.waypoints[0];
#             rnavCommonWaypointIWP = new string[] { Enums.RnavCommonWaypoint_IWP };
#             item.Attributes = new SymbolAttributes(rnavCommonWaypointIWP);
#         }
#         else
#         {
#             position_1.method_1(out degree, out degree1);
#             Symbol symbolAttribute = self.waypoints[0];
#             rnavCommonWaypointIWP = new string[] { Enums.RnavCommonWaypoint_IWP, degree.ToString(), degree1.ToString() };
#             symbolAttribute.Attributes = new SymbolAttributes(rnavCommonWaypointIWP);
#         }
        polylineArea = PolylineArea()
        polylineArea1 = PolylineArea()
        polylineArea2 = PolylineArea()
        polylineArea3 = PolylineArea()
        polylineArea4 = PolylineArea()
        return1 = []
        num13 = MathHelper.smethod_77(Unit.smethod_1(num), Unit.smethod_1(num4), AngleUnits.Degrees, return1)
        turnDirection = return1[0]
        if (turnDirection == TurnDirection.Nothing or num13 < 0.5):
            point3d43 = MathHelper.distanceBearingPoint(point3d32, num6, metres);
            point3d44 = MathHelper.distanceBearingPoint(point3d32, num6, metres / 2);
            point3d45 = MathHelper.distanceBearingPoint(point3d32, num5, metres);
            point3d46 = MathHelper.distanceBearingPoint(point3d32, num5, metres / 2);
            point3d47 = MathHelper.distanceBearingPoint(point3d43, num7, metres1);
            point3d48 = MathHelper.distanceBearingPoint(point3d44, num7, metres1);
            point3d49 = MathHelper.distanceBearingPoint(point3d45, num7, metres1);
            point3d50 = MathHelper.distanceBearingPoint(point3d46, num7, metres1);
            polylineArea.method_1(point3d47);
            polylineArea1.method_1(point3d48);
            polylineArea2.method_1(point3d49);
            polylineArea3.method_1(point3d50);
            point3dArray = [point3d50, point3d48]
            polylineArea4.method_7(point3dArray)
            point3dArray = [point3d49, point3d47]
            self.selectionArea.extend(point3dArray)
            point3dArray = [point3d47, point3d49]
            self.drawingLines.append(PolylineArea(point3dArray))
        else:
            point3d51 = MathHelper.distanceBearingPoint(point3d32, num2, metres);
            point3d52 = MathHelper.distanceBearingPoint(point3d32, num2, metres / 2);
            point3d53 = MathHelper.distanceBearingPoint(point3d32, num1, metres);
            point3d54 = MathHelper.distanceBearingPoint(point3d32, num1, metres / 2);
            point3d55 = MathHelper.distanceBearingPoint(point3d51, num3, metres1);
            point3d56 = MathHelper.distanceBearingPoint(point3d52, num3, metres1);
            point3d57 = MathHelper.distanceBearingPoint(point3d53, num3, metres1);
            point3d58 = MathHelper.distanceBearingPoint(point3d54, num3, metres1);
            point3d59 = MathHelper.distanceBearingPoint(point3d32, num6, metres);
            point3d60 = MathHelper.distanceBearingPoint(point3d32, num6, metres / 2);
            point3d61 = MathHelper.distanceBearingPoint(point3d32, num5, metres);
            point3d62 = MathHelper.distanceBearingPoint(point3d32, num5, metres / 2);
            point3d63 = MathHelper.distanceBearingPoint(point3d59, num7, metres1);
            point3d64 = MathHelper.distanceBearingPoint(point3d60, num7, metres1);
            point3d65 = MathHelper.distanceBearingPoint(point3d61, num7, metres1);
            point3d66 = MathHelper.distanceBearingPoint(point3d62, num7, metres1);
            point3d13 = MathHelper.getIntersectionPoint(point3d55, point3d57, point3d63, point3d65)
            if (turnDirection != TurnDirection.Right):
                point3d1 = MathHelper.getIntersectionPoint(point3d55, point3d51, point3d63, point3d65)
                point3d4 = MathHelper.getIntersectionPoint(point3d56, point3d52, point3d63, point3d65)
                point3d2 = MathHelper.getIntersectionPoint(point3d55, point3d51, point3d59, point3d61)
                point3d5 = MathHelper.getIntersectionPoint(point3d56, point3d52, point3d59, point3d61)
                point3d3 = MathHelper.getIntersectionPoint(point3d63, point3d59, point3d51, point3d53)
                point3d6 = MathHelper.getIntersectionPoint(point3d64, point3d60, point3d51, point3d53)
                point3d7 = point3d57;
                point3d8 = point3d53;
                point3d9 = point3d61;
                point3d10 = point3d58;
                point3d11 = point3d54;
                point3d12 = point3d62;
                point3dArray = [point3d1, point3d2, point3d3]
                polylineArea.method_7(point3dArray)
                point3dArray = [point3d4, point3d5, point3d6]
                polylineArea1.method_7(point3dArray)
                point3dArray = [point3d7, point3d8, point3d9]
                polylineArea2.method_7(point3dArray)
                polylineArea2[1].bulge = MathHelper.smethod_57(TurnDirection.Left, point3d8, point3d9, point3d32)
                point3dArray = [point3d10, point3d11, point3d12]
                polylineArea3.method_7(point3dArray)
                polylineArea3[1].bulge = MathHelper.smethod_57(TurnDirection.Left, point3d11, point3d12, point3d32)
                point3d16 = MathHelper.getIntersectionPoint(point3d8, MathHelper.distanceBearingPoint(point3d8, num, 100), point3d9, MathHelper.distanceBearingPoint(point3d9, num7, 100));
                point3dArray = [point3d9, point3d16, point3d8, point3d7, point3d13, point3d1, point3d2, point3d3]
                self.selectionArea.extend(point3dArray)
                point3d14 = MathHelper.distanceBearingPoint(point3d32, MathHelper.getBearing(point3d32, point3d16), metres);
                point3d15 = MathHelper.distanceBearingPoint(point3d32, MathHelper.getBearing(point3d32, point3d16), metres / 2);
                point3dArray = [point3d12, point3d11, point3d10, point3d13, point3d4, point3d5, point3d6]
                polylineArea4.method_7(point3dArray)
                polylineArea4[0].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d12, point3d11, point3d32)
                self.secondary.append(SecondaryObstacleArea(point3d4, point3d5, point3d1, point3d2, num))
                self.secondary.append(SecondaryObstacleArea(point3d10, point3d11, point3d7, point3d8, num))
                self.secondary.append(SecondaryObstacleArea(point3d5, point3d6, point3d2, point3d3, MathHelper.getBearing(point3d5, point3d6)))
                self.secondary.append(SecondaryObstacleArea(point3d11, point3d15, point3d12, point3d8, 0.0, point3d14, point3d9))
                point3dArray = [point3d1, point3d13, point3d7]
                self.drawingLines.append(PolylineArea(point3dArray))
            else:
                point3d1 = point3d55
                point3d2 = point3d51
                point3d3 = point3d59
                point3d4 = point3d56
                point3d5 = point3d52
                point3d6 = point3d60
                point3d7 = MathHelper.getIntersectionPoint(point3d57, point3d53, point3d63, point3d65)
                point3d10 = MathHelper.getIntersectionPoint(point3d58, point3d54, point3d63, point3d65)
                point3d8 = MathHelper.getIntersectionPoint(point3d57, point3d53, point3d59, point3d61)
                point3d11 = MathHelper.getIntersectionPoint(point3d58, point3d54, point3d59, point3d61)
                point3d9 = MathHelper.getIntersectionPoint(point3d65, point3d61, point3d51, point3d53)
                point3d12 = MathHelper.getIntersectionPoint(point3d66, point3d62, point3d51, point3d53)
                point3dArray = [point3d1, point3d2, point3d3]
                polylineArea.method_7(point3dArray)
                polylineArea[1].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d2, point3d3, point3d32)
                point3dArray = [point3d4, point3d5, point3d6]
                polylineArea1.method_7(point3dArray)
                polylineArea1[1].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d5, point3d6, point3d32)
                point3dArray = [point3d7, point3d8, point3d9]
                polylineArea2.method_7(point3dArray)
                point3dArray = [point3d10, point3d11, point3d12]
                polylineArea3.method_7(point3dArray)
                point3d16 = MathHelper.getIntersectionPoint(point3d2, MathHelper.distanceBearingPoint(point3d2, num, 100), point3d3, MathHelper.distanceBearingPoint(point3d3, num7, 100))
                point3dArray = [point3d9, point3d8, point3d7, point3d13, point3d1, point3d2, point3d16, point3d3]
                self.selectionArea.extend(point3dArray)
                point3d14 = MathHelper.distanceBearingPoint(point3d32, MathHelper.getBearing(point3d32, point3d16), metres);
                point3d15 = MathHelper.distanceBearingPoint(point3d32, MathHelper.getBearing(point3d32, point3d16), metres / 2);
                point3dArray = [point3d12, point3d11, point3d10, point3d13, point3d4, point3d5, point3d6]
                polylineArea4.method_7(point3dArray)
                polylineArea4[5].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d5, point3d6, point3d32)
                self.secondary.append(SecondaryObstacleArea(point3d4, point3d5, point3d1, point3d2, num));
                self.secondary.append(SecondaryObstacleArea(point3d10, point3d11, point3d7, point3d8, num));
                self.secondary.append(SecondaryObstacleArea(point3d5, point3d15, point3d6, point3d2, 0.0, point3d14, point3d3));
                self.secondary.append(SecondaryObstacleArea(point3d11, point3d12, point3d8, point3d9, MathHelper.getBearing(point3d11, point3d12)));
                point3dArray = [point3d1, point3d13, point3d7]
                self.drawingLines.append(PolylineArea(point3dArray))

        return1 = []
        num13 = MathHelper.smethod_77(Unit.smethod_1(num4), Unit.smethod_1(num8), AngleUnits.Degrees, return1)
        turnDirection = return1[0]
        if (turnDirection == TurnDirection.Nothing or num13 < 0.5):
            point3d67 = MathHelper.distanceBearingPoint(point3d33, num6, metres3);
            point3d68 = MathHelper.distanceBearingPoint(point3d33, num6, metres3 / 2);
            point3d69 = MathHelper.distanceBearingPoint(point3d33, num5, metres3);
            point3d70 = MathHelper.distanceBearingPoint(point3d33, num5, metres3 / 2);
            point3d71 = MathHelper.distanceBearingPoint(point3d67, num7 + num12, (metres - metres3) / math.sin(num12))
            point3d72 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d33, num7, (metres - metres3) / math.tan(num12)), num6, metres / 2)
            point3d73 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d33, num7, (metres - metres3) / math.tan(num12)), num5, metres / 2);
            point3d74 = MathHelper.distanceBearingPoint(point3d69, num7 - num12, (metres - metres3) / math.sin(num12));
            point3dArray = [point3d71, point3d67, point3d69, point3d74]
            self.selectionArea.extend(point3dArray)
            point3dArray = [point3d72, point3d68, point3d70, point3d73]
            polylineArea4.method_7(point3dArray)
            self.secondary.append(SecondaryObstacleArea(polylineArea1[polylineArea1.Count - 1].position, point3d72, polylineArea[polylineArea.Count - 1].position, point3d71, num4));
            self.secondary.append(SecondaryObstacleArea(polylineArea3[polylineArea3.Count - 1].position, point3d73, polylineArea2[polylineArea2.Count - 1].position, point3d74, num4));
            self.secondary.append(SecondaryObstacleArea(point3d72, point3d68, point3d71, point3d67, num4));
            self.secondary.append(SecondaryObstacleArea(point3d73, point3d70, point3d74, point3d69, num4));
            point3dArray = [point3d71, point3d67]
            polylineArea.method_7(point3dArray)
            point3dArray = [point3d72, point3d68]
            polylineArea1.method_7(point3dArray)
            point3dArray = [point3d74, point3d69]
            polylineArea2.method_7(point3dArray)
            point3dArray = [point3d73, point3d70]
            polylineArea3.method_7(point3dArray)
            point3dArray = [point3d67, point3d69]
            self.drawingLines.append(PolylineArea(point3dArray))
        else:
            point3d75 = MathHelper.distanceBearingPoint(point3d33, num6, metres3);
            point3d76 = MathHelper.distanceBearingPoint(point3d33, num6, metres3 / 2);
            point3d77 = MathHelper.distanceBearingPoint(point3d33, num5, metres3);
            point3d78 = MathHelper.distanceBearingPoint(point3d33, num5, metres3 / 2);
            point3d79 = MathHelper.distanceBearingPoint(point3d75, num7 + num12, (metres - metres3) / math.sin(num12));
            point3d80 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d33, num7, (metres - metres3) / math.tan(num12)), num6, metres / 2);
            point3d81 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d33, num7, (metres - metres3) / math.tan(num12)), num5, metres / 2);
            point3d82 = MathHelper.distanceBearingPoint(point3d77, num7 - num12, (metres - metres3) / math.sin(num12))
            point3d83 = MathHelper.distanceBearingPoint(point3d33, num10, metres3);
            point3d84 = MathHelper.distanceBearingPoint(point3d33, num10, metres3 / 2);
            point3d85 = MathHelper.distanceBearingPoint(point3d33, num9, metres3);
            point3d86 = MathHelper.distanceBearingPoint(point3d33, num9, metres3 / 2);
            point3d87 = MathHelper.distanceBearingPoint(point3d83, num8 + num12, (metres3 - metres9) / math.sin(num12));
            point3d88 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d33, num8, (metres3 - metres9) / math.tan(num12)), num10, metres9 / 2);
            point3d89 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d33, num8, (metres3 - metres9) / math.tan(num12)), num9, metres9 / 2);
            point3d90 = MathHelper.distanceBearingPoint(point3d85, num8 - num12, (metres3 - metres9) / math.sin(num12))
            if (turnDirection != TurnDirection.Right):
                point3d17 = point3d79
                point3d20 = point3d80
                point3d23 = point3d82
                point3d26 = point3d81
                point3d18 = MathHelper.getIntersectionPoint(point3d79, point3d75, point3d83, point3d85)
                point3d21 = MathHelper.getIntersectionPoint(point3d80, point3d76, point3d83, point3d85)
                point3d24 = point3d77
                point3d27 = point3d78
                point3d19 = MathHelper.getIntersectionPoint(point3d83, point3d87, point3d75, point3d77)
                point3d22 = MathHelper.getIntersectionPoint(point3d84, point3d88, point3d75, point3d77)
                point3d25 = point3d85
                point3d28 = point3d86
                point3d31 = MathHelper.getIntersectionPoint(point3d24, MathHelper.distanceBearingPoint(point3d24, num4, 100), point3d25, MathHelper.distanceBearingPoint(point3d25, num11, 100))
                point3dArray = [point3d17, point3d18, point3d19, point3d33, point3d25, point3d31, point3d24, point3d23]
                self.selectionArea.extend(point3dArray)
                point3d29 = MathHelper.distanceBearingPoint(point3d33, MathHelper.getBearing(point3d33, point3d31), metres3);
                point3d30 = MathHelper.distanceBearingPoint(point3d33, MathHelper.getBearing(point3d33, point3d31), metres3 / 2);
                count = polylineArea4.Count
                point3dArray = [point3d20, point3d21, point3d22, point3d33, point3d28, point3d27, point3d26]
                polylineArea4.method_7(point3dArray)
                polylineArea4[count + 4].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d28, point3d27, point3d33)
                self.secondary.append(SecondaryObstacleArea(polylineArea1[polylineArea1.Count - 1].position, point3d20, polylineArea[polylineArea.Count - 1].position, point3d17, num4));
                self.secondary.append(SecondaryObstacleArea(polylineArea3[polylineArea3.Count - 1].position, point3d26, polylineArea2[polylineArea2.Count - 1].position, point3d23, num4));
                self.secondary.append(SecondaryObstacleArea(point3d20, point3d21, point3d17, point3d18, num4));
                self.secondary.append(SecondaryObstacleArea(point3d26, point3d27, point3d23, point3d24, num4));
                self.secondary.append(SecondaryObstacleArea(point3d21, point3d22, point3d18, point3d19, num4));
                self.secondary.append(SecondaryObstacleArea(point3d27, point3d30, point3d28, point3d24, 0.0, point3d29, point3d25));
                point3dArray = [point3d17, point3d18, point3d19]
                polylineArea.method_7(point3dArray)
                point3dArray = [point3d20, point3d21, point3d22]
                polylineArea1.method_7(point3dArray)
                count = polylineArea2.Count
                point3dArray = [point3d23, point3d24, point3d25]
                polylineArea2.method_7(point3dArray)
                polylineArea2[count + 1].bulge = MathHelper.smethod_57(TurnDirection.Left, point3d24, point3d25, point3d33)
                count = polylineArea3.Count
                point3dArray = [point3d26, point3d27, point3d28]
                polylineArea3.method_7(point3dArray)
                polylineArea3[count + 1].bulge = MathHelper.smethod_57(TurnDirection.Left, point3d27, point3d28, point3d33)
                point3dArray = [point3d19, point3d33, point3d25]
                self.drawingLines.append(PolylineArea(point3dArray))
            else:
                point3d17 = point3d79;
                point3d20 = point3d80;
                point3d23 = point3d82;
                point3d26 = point3d81;
                point3d18 = point3d75;
                point3d21 = point3d76;
                point3d24 = MathHelper.getIntersectionPoint(point3d82, point3d77, point3d83, point3d85)
                point3d27 = MathHelper.getIntersectionPoint(point3d81, point3d78, point3d83, point3d85)
                point3d19 = point3d83;
                point3d22 = point3d84;
                point3d25 = MathHelper.getIntersectionPoint(point3d85, point3d90, point3d75, point3d77)
                point3d28 = MathHelper.getIntersectionPoint(point3d86, point3d89, point3d75, point3d77)
                point3d31 = MathHelper.getIntersectionPoint(point3d18, MathHelper.distanceBearingPoint(point3d18, num4, 100), point3d19, MathHelper.distanceBearingPoint(point3d19, num11, 100))
                point3dArray = [point3d17, point3d18, point3d31, point3d19, point3d33, point3d25, point3d24, point3d23]
                self.selectionArea.extend(point3dArray)
                point3d29 = MathHelper.distanceBearingPoint(point3d33, MathHelper.getBearing(point3d33, point3d31), metres3);
                point3d30 = MathHelper.distanceBearingPoint(point3d33, MathHelper.getBearing(point3d33, point3d31), metres3 / 2);
                count = polylineArea4.Count
                point3dArray = [point3d20, point3d21, point3d22, point3d33, point3d28, point3d27, point3d26]
                polylineArea4.method_7(point3dArray)
                polylineArea4[count + 1].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d21, point3d22, point3d33)
                self.secondary.append(SecondaryObstacleArea(polylineArea1[polylineArea1.Count - 1].position, point3d20, polylineArea[polylineArea.Count - 1].position, point3d17, num4))
                self.secondary.append(SecondaryObstacleArea(polylineArea3[polylineArea3.Count - 1].position, point3d26, polylineArea2[polylineArea2.Count - 1].position, point3d23, num4))
                self.secondary.append(SecondaryObstacleArea(point3d20, point3d21, point3d17, point3d18, num4))
                self.secondary.append(SecondaryObstacleArea(point3d26, point3d27, point3d23, point3d24, num4))
                self.secondary.append(SecondaryObstacleArea(point3d21, point3d30, point3d22, point3d18, 0.0, point3d29, point3d19))
                self.secondary.append(SecondaryObstacleArea(point3d27, point3d28, point3d24, point3d25, num4))
                count = polylineArea.Count
                point3dArray = [point3d17, point3d18, point3d19]
                polylineArea.method_7(point3dArray)
                polylineArea[count + 1].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d18, point3d19, point3d33)
                count = polylineArea1.Count
                point3dArray = [point3d20, point3d21, point3d22]
                polylineArea1.method_7(point3dArray)
                polylineArea1[count + 1].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d21, point3d22, point3d33)
                point3dArray = [point3d23, point3d24, point3d25]
                polylineArea2.method_7(point3dArray)
                point3dArray = [point3d26, point3d27, point3d28]
                polylineArea3.method_7(point3dArray)
                point3dArray = [point3d19, point3d33, point3d25]
                self.drawingLines.append(PolylineArea(point3dArray))

            point3d39 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d33, num4, metres4), num6, metres5)
            point3d40 = MathHelper.distanceBearingPoint(point3d39, num7, metres4 * 2)
            point3d41 = MathHelper.distanceBearingPoint(point3d40, num5, metres5 * 2)
            point3d42 = MathHelper.distanceBearingPoint(point3d41, num4, metres4 * 2)
            point3dArray = [point3d39, point3d40, point3d41, point3d42, point3d39]
            self.drawingLines.append(PolylineArea(point3dArray))

        point3d35 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d32, num4, metres1), num6, metres2)
        point3d36 = MathHelper.distanceBearingPoint(point3d35, num7, metres1 * 2)
        point3d37 = MathHelper.distanceBearingPoint(point3d36, num5, metres2 * 2)
        point3d38 = MathHelper.distanceBearingPoint(point3d37, num4, metres1 * 2)
        point3dArray = [point3d35, point3d36, point3d37, point3d38, point3d35]
        self.drawingLines.append(PolylineArea(point3dArray))
        self.drawingLines.append(polylineArea)
        self.drawingLines.append(polylineArea2)
        self.drawingLines.append(polylineArea1)
        self.drawingLines.append(polylineArea3)
        point3dArray = [point3d32, point3d33]
        self.nominalLine = PolylineArea(point3dArray)
        self.primary.append(PrimaryObstacleArea(polylineArea4))

    def vmethod_4(self, gnssSegmentObstacles_0):
        gnssSegmentObstacles_0.method_15()

class InitialSegment1(IGnssSegment):

    def __init__(self, position_0, position_1, position_2, position_3, rnavSpecification_0, aircraftSpeedCategory_0, speed_0, altitude_0, double_0, double_1, speed_1, altitude_1):
        self.initialOca = Altitude(0.0)
        self.Type = RnavSegmentType.Initial1
        self.drawingLines = []
        self.primary = []
        self.secondary = []
        self.selectionArea = []
        
        rnavCommonWaypointIAWP1 = []
        strArrays = []
        point3dArray = []
        point3d29 = position_1
        point3d30 = position_2
        point3d31 = position_0
        point3d32 = position_3
        self.primaryMoc = altitude_1.Metres;
        self.initialOca = altitude_0;
        num1 = MathHelper.getBearing(point3d31, point3d29)
        num2 = MathHelper.smethod_4(num1 + 1.5707963267949);
        num3 = MathHelper.smethod_4(num1 - 1.5707963267949);
        num4 = MathHelper.smethod_4(num1 + 3.14159265358979);
        num5 = MathHelper.getBearing(point3d29, point3d30);
        num6 = MathHelper.smethod_4(num5 + 1.5707963267949);
        num7 = MathHelper.smethod_4(num5 - 1.5707963267949);
        num8 = MathHelper.smethod_4(num5 + 3.14159265358979);
        num9 = Unit.ConvertDegToRad(30);
        if (MathHelper.calcDistance(point3d32, point3d31) > (Distance(30, DistanceUnits.NM)).Metres and rnavSpecification_0 == RnavSpecification.RnpApch):
            raise UserWarning, Messages.ERR_DISTANCE_BETWEEN_X_AND_ARP_EXCEEDS_RNP_SPEC%'Initial Waypoint1'
        rnavGnssTolerance1 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Faf, aircraftSpeedCategory_0)
        metres = rnavGnssTolerance1.getASWMetres()
        metres1 = rnavGnssTolerance1.getATTMetres()
        metres2 = rnavGnssTolerance1.getXTTMetres()
        rnavGnssTolerance2 = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0)
        metres3 = rnavGnssTolerance2.getASWMetres()
        metres4 = rnavGnssTolerance2.getATTMetres()
        metres5 = rnavGnssTolerance2.getXTTMetres()
        rnavGnssTolerance3 = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0)
        metres6 = rnavGnssTolerance3.getASWMetres()
        metres7 = rnavGnssTolerance3.getATTMetres()
        metres8 = rnavGnssTolerance3.getXTTMetres()
        if rnavSpecification_0 != RnavSpecification.RnpApch:
            rnavGnssTolerance = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.StarSid, aircraftSpeedCategory_0) 
        else:
            rnavGnssTolerance = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0)
        metres9 = rnavGnssTolerance.getASWMetres()
        metres10 = rnavGnssTolerance.getATTMetres()
        num10 = rnavGnssTolerance.getXTTMetres()
        num11 = MathHelper.smethod_76(Unit.smethod_1(num1), Unit.smethod_1(num5), AngleUnits.Degrees)
        speed = Speed.smethod_0(speed_0, double_0, altitude_0)
        distance = Distance.smethod_0(speed, double_1)
        metres11 = distance.Metres
        num12 = metres11 * math.tan(Unit.ConvertDegToRad(0.5 * num11))
        if aircraftSpeedCategory_0 != AircraftSpeedCategory.H:
            num = 5 * speed.MetresPerSecond
        else: 
            num = 3 * speed.MetresPerSecond
        distance1 = Distance(num12 + num)
        if (distance1.Metres > MathHelper.calcDistance(point3d31, point3d29)):
            eRRINSUFFICIENTMINIMUMSTABILISATIONDISTANCE = Messages.ERR_INSUFFICIENT_MINIMUM_STABILISATION_DISTANCE
            rnavCommonWaypointIAWP1 = ["Initial Waypoint 1", "Intermediate Waypoint", distance1.Metres]
            raise UserWarning, eRRINSUFFICIENTMINIMUMSTABILISATIONDISTANCE % rnavCommonWaypointIAWP1

        distance2 = Distance(num12 + num + Unit.ConvertNMToMeter(2))
        if (distance2.Metres > MathHelper.calcDistance(point3d29, point3d30)):
            strMessage = Messages.ERR_INSUFFICIENT_MINIMUM_STABILISATION_DISTANCE
            rnavCommonWaypointIAWP1 = ["Intermediate Waypoint", "Final Approach Waypoint", distance2.Metres]
            raise UserWarning, strMessage % ("Intermediate Waypoint", "Final Approach Waypoint", distance2.Metres)

        distance = RnavWaypoints.getDistanceFromWaypointToEarliestTurningPoint(RnavWaypointType.FlyBy, Distance(metres4), Distance(metres11), num11, AngleUnits.Degrees)
        metres12 = distance.Metres
        if metres12 >= 0:
            point3d23 = MathHelper.distanceBearingPoint(point3d29, num4, math.fabs(metres12)) 
        else:
            point3d23 = MathHelper.distanceBearingPoint(point3d29, num1, math.fabs(metres12))
        distance = RnavWaypoints.smethod_13(RnavFlightPhase.IafIf, RnavWaypointType.FlyBy, speed, speed_1, Distance(metres4), Distance(metres11), num11, AngleUnits.Degrees)
        metres13 = distance.Metres
        if metres13 >= 0:
            point3d24 = MathHelper.distanceBearingPoint(point3d29, num4, math.fabs(metres13)) 
        else:
            point3d24 = MathHelper.distanceBearingPoint(point3d29, num1, math.fabs(metres13))
#         self.waypoints.Add(new Symbol(SymbolType.Flyb));
#         self.waypoints[0].Tag = point3d31;
#         if (!Geo.DatumLoaded)
#         {
#             Symbol item = self.waypoints[0];
#             strArrays = new string[] { Enums.RnavCommonWaypoint_IAWP1 };
#             item.Attributes = new SymbolAttributes(strArrays);
#         }
#         else
#         {
#             position_0.method_1(out degree, out degree1);
#             Symbol symbolAttribute = self.waypoints[0];
#             strArrays = new string[] { Enums.RnavCommonWaypoint_IAWP1, degree.ToString(), degree1.ToString() };
#             symbolAttribute.Attributes = new SymbolAttributes(strArrays);
#         }
        polylineArea = PolylineArea()
        polylineArea1 = PolylineArea()
        polylineArea2 = PolylineArea()
        polylineArea3 = PolylineArea()
        polylineArea4 = PolylineArea()
        return2 = []
        flag = MathHelper.smethod_34(point3d31, point3d29, point3d32, Unit.ConvertNMToMeter(30), return2) == IntersectionStatus.Intersection #out point3d27, out point3d28) ;
        point3d27 = return2[0]
        point3d28 = return2[1]
        flag1 = flag
        if (flag):
            if not MathHelper.smethod_135(MathHelper.getBearing(point3d31, point3d27), MathHelper.getBearing(point3d31, point3d29), Unit.ConvertDegToRad(5), AngleUnits.Radians):
                flag1 = False
            else:
                flag1 = MathHelper.calcDistance(point3d29, point3d31) > MathHelper.calcDistance(point3d29, point3d27) + (metres9 - metres6 / math.tan(num9))
        if (not flag1):
            point3d = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d31, num1, metres7), num3, metres8);
            point3d1 = MathHelper.distanceBearingPoint(point3d, num4, metres7 * 2);
            point3d2 = MathHelper.distanceBearingPoint(point3d1, num2, metres8 * 2);
            point3d3 = MathHelper.distanceBearingPoint(point3d2, num1, metres7 * 2);
            point3d33 = MathHelper.distanceBearingPoint(point3d31, num3, metres6);
            point3d34 = MathHelper.distanceBearingPoint(point3d31, num3, metres6 / 2);
            point3d35 = MathHelper.distanceBearingPoint(point3d31, num2, metres6);
            point3d36 = MathHelper.distanceBearingPoint(point3d31, num2, metres6 / 2);
            point3d37 = MathHelper.distanceBearingPoint(point3d33, num4, metres7);
            point3d38 = MathHelper.distanceBearingPoint(point3d34, num4, metres7);
            point3d39 = MathHelper.distanceBearingPoint(point3d35, num4, metres7);
            point3d40 = MathHelper.distanceBearingPoint(point3d36, num4, metres7);
            point3dArray = [point3d37, point3d33]
            polylineArea.method_7(point3dArray)
            point3dArray = [point3d38, point3d34]
            polylineArea1.method_7(point3dArray)
            point3dArray = [point3d39, point3d35]
            polylineArea2.method_7(point3dArray)
            point3dArray = [point3d40, point3d36]
            polylineArea3.method_7(point3dArray)
            point3dArray = [point3d40, point3d38]
            polylineArea4.method_7(point3dArray)
            point3dArray = [point3d39, point3d37]
            self.selectionArea.extend(point3dArray)
            self.secondary.append(SecondaryObstacleArea(point3d38, point3d34, point3d37, point3d33, num1))
            self.secondary.append(SecondaryObstacleArea(point3d40, point3d36, point3d39, point3d35, num1))
            point3dArray = [point3d37, point3d39]
            self.drawingLines.append(PolylineArea(point3dArray))
        else:
            point3d = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d31, num1, metres10), num3, num10);
            point3d1 = MathHelper.distanceBearingPoint(point3d, num4, metres10 * 2);
            point3d2 = MathHelper.distanceBearingPoint(point3d1, num2, num10 * 2);
            point3d3 = MathHelper.distanceBearingPoint(point3d2, num1, metres10 * 2);
            point3d41 = MathHelper.distanceBearingPoint(point3d31, num3, metres9);
            point3d42 = MathHelper.distanceBearingPoint(point3d31, num3, metres9 / 2);
            point3d43 = MathHelper.distanceBearingPoint(point3d31, num2, metres9);
            point3d44 = MathHelper.distanceBearingPoint(point3d31, num2, metres9 / 2);
            point3d45 = MathHelper.distanceBearingPoint(point3d41, num4, metres10);
            point3d46 = MathHelper.distanceBearingPoint(point3d42, num4, metres10);
            point3d47 = MathHelper.distanceBearingPoint(point3d43, num4, metres10);
            point3d48 = MathHelper.distanceBearingPoint(point3d44, num4, metres10);
            point3d49 = MathHelper.distanceBearingPoint(point3d27, num3, metres9);
            point3d50 = MathHelper.distanceBearingPoint(point3d27, num3, metres9 / 2);
            point3d51 = MathHelper.distanceBearingPoint(point3d27, num2, metres9);
            point3d52 = MathHelper.distanceBearingPoint(point3d27, num2, metres9 / 2);
            point3d28 = MathHelper.distanceBearingPoint(point3d27, num1, (metres9 - metres6) / math.tan(num9))
            point3d53 = MathHelper.distanceBearingPoint(point3d28, num3, metres6);
            point3d54 = MathHelper.distanceBearingPoint(point3d28, num3, metres6 / 2);
            point3d55 = MathHelper.distanceBearingPoint(point3d28, num2, metres6);
            point3d56 = MathHelper.distanceBearingPoint(point3d28, num2, metres6 / 2);
            point3dArray = [point3d45, point3d41, point3d49, point3d53]
            polylineArea.method_7(point3dArray)
            point3dArray = [point3d46, point3d42, point3d50, point3d54]
            polylineArea1.method_7(point3dArray)
            point3dArray = [point3d47, point3d43, point3d51, point3d55]
            polylineArea2.method_7(point3dArray)
            point3dArray = [point3d48, point3d44, point3d52, point3d56]
            polylineArea3.method_7(point3dArray)
            point3dArray = [point3d56, point3d52, point3d44, point3d48, point3d46, point3d42, point3d50, point3d54]
            polylineArea4.method_7(point3dArray)
            point3dArray = [point3d55, point3d51, point3d43, point3d47, point3d45, point3d41, point3d49, point3d53]
            self.selectionArea.extend(point3dArray)
            self.secondary.append(SecondaryObstacleArea(point3d46, point3d50, point3d45, point3d49, num1))
            self.secondary.append(SecondaryObstacleArea(point3d48, point3d52, point3d47, point3d51, num1))
            self.secondary.append(SecondaryObstacleArea(point3d50, point3d54, point3d49, point3d53, num1))
            self.secondary.append(SecondaryObstacleArea(point3d52, point3d56, point3d51, point3d55, num1))
            point3dArray = [point3d45, point3d47]
            self.drawingLines.append(PolylineArea(point3dArray))

        point3d57 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d29, num1, metres7), num3, metres5);
        point3d58 = MathHelper.distanceBearingPoint(point3d57, num4, metres4 * 2);
        point3d59 = MathHelper.distanceBearingPoint(point3d58, num2, metres5 * 2);
        point3d60 = MathHelper.distanceBearingPoint(point3d59, num1, metres4 * 2);
        position = polylineArea[polylineArea.Count - 1].position;
        position1 = polylineArea1[polylineArea1.Count - 1].position;
        position2 = polylineArea3[polylineArea3.Count - 1].position;
        position3 = polylineArea2[polylineArea2.Count - 1].position;
        point3d61 = MathHelper.distanceBearingPoint(point3d30, num6, metres / 2);
        point3d62 = MathHelper.distanceBearingPoint(point3d30, num6, metres);
        point3d63 = MathHelper.distanceBearingPoint(point3d30, num7, metres / 2);
        point3d64 = MathHelper.distanceBearingPoint(point3d30, num7, metres);
        point3d65 = MathHelper.distanceBearingPoint(point3d64, num8 + num9, (metres3 - metres) / math.sin(num9));
        point3d66 = MathHelper.distanceBearingPoint(point3d62, num8 - num9, (metres3 - metres) / math.sin(num9));
        point3d67 = MathHelper.distanceBearingPoint(point3d65, num6, metres3 / 2);
        point3d68 = MathHelper.distanceBearingPoint(point3d66, num7, metres3 / 2);
        point3d69 = MathHelper.distanceBearingPoint(point3d24, num3, metres6);
        point3d70 = MathHelper.distanceBearingPoint(point3d24, num3, metres6 / 2);
        windSpiral = WindSpiral(MathHelper.distanceBearingPoint(point3d24, num3, metres6 / 2), num1, speed, speed_1, double_1, TurnDirection.Right);
        windSpiral1 = WindSpiral(MathHelper.distanceBearingPoint(point3d24, num2, metres6 / 2), num1, speed, speed_1, double_1, TurnDirection.Right);
        point3d71 = MathHelper.distanceBearingPoint(windSpiral.Center[0], num3, windSpiral.Radius[0]);
        point3d72 = MathHelper.distanceBearingPoint(point3d71, num3, metres6 / 2);
        point3d73 = MathHelper.distanceBearingPoint(point3d70, MathHelper.getBearing(point3d70, windSpiral.Center[0]) - 1.5707963267949, 100);
        point3d74 = MathHelper.distanceBearingPoint(point3d71, num1, 100);
        point3d10 = MathHelper.getIntersectionPoint(point3d70, point3d73, point3d71, point3d74)
        point3d75 = MathHelper.distanceBearingPoint(point3d10, num3, metres6 / 2);
        point3d76 = MathHelper.distanceBearingPoint(windSpiral1.Center[0], num1, windSpiral1.Radius[0]);
        point3d77 = MathHelper.distanceBearingPoint(windSpiral1.Center[0], num1, windSpiral1.Radius[0] + metres6 / 2);
        point3d78 = MathHelper.distanceBearingPoint(point3d65, num8, 100);
        point3d79 = MathHelper.distanceBearingPoint(point3d67, num8, 100);
        if (MathHelper.smethod_119(point3d76, point3d79, point3d67)):
            point3d77 = MathHelper.getIntersectionPoint(point3d78, point3d65, MathHelper.distanceBearingPoint(point3d77, num3, 100), point3d77)
            point3d76 = MathHelper.getIntersectionPoint(point3d79, point3d67, MathHelper.distanceBearingPoint(point3d76, num3, 100), point3d76)
            point3d13 = point3d77;
            point3d22 = point3d77;
            point3d14 = point3d77;
            point3d16 = point3d77;
            finish = point3d76;
            point3d15 = point3d76;
            point3d17 = point3d76;
            center = windSpiral1.Center[0];
            center1 = windSpiral1.Center[0];
        elif (not MathHelper.smethod_115(point3d76, windSpiral1.Center[0], windSpiral1.Finish[0])):
            point3d76 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], num1, windSpiral1.Radius[1]);
            point3d77 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], num1, windSpiral1.Radius[1] + metres6 / 2);
            finish = point3d76;
            point3d13 = point3d77;
            point3d15 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], num5 - Unit.ConvertDegToRad(60), windSpiral1.Radius[1]);
            point3d14 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], num5 - Unit.ConvertDegToRad(60), windSpiral1.Radius[1] + metres6 / 2);
            center = windSpiral1.Center[1];
            center1 = windSpiral1.Center[1];
        else:
            point3d15 = MathHelper.distanceBearingPoint(windSpiral1.Center[0], num5 - Unit.ConvertDegToRad(60), windSpiral1.Radius[0]);
            point3d14 = MathHelper.distanceBearingPoint(windSpiral1.Center[0], num5 - Unit.ConvertDegToRad(60), windSpiral1.Radius[0] + metres6 / 2);
            if (not MathHelper.smethod_115(point3d15, windSpiral1.Center[0], windSpiral1.Finish[0])):
                finish = windSpiral1.Finish[0];
                point3d13 = MathHelper.distanceBearingPoint(windSpiral1.Center[0], MathHelper.getBearing(windSpiral1.Center[0], windSpiral1.Finish[0]), windSpiral1.Radius[0] + metres6 / 2);
                point3d15 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], num5 - Unit.ConvertDegToRad(60), windSpiral1.Radius[1]);
                point3d14 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], num5 - Unit.ConvertDegToRad(60), windSpiral1.Radius[1] + metres6 / 2);
                center = windSpiral1.Center[0];
                center1 = windSpiral1.Center[1];
            else:
                finish = point3d15;
                point3d13 = point3d14;
                center = windSpiral1.Center[0];
                center1 = windSpiral1.Center[0];

        point3d80 = MathHelper.distanceBearingPoint(point3d76, num3, 100)
        point3d74 = MathHelper.distanceBearingPoint(point3d71, num1, 100)
        point3d12 = MathHelper.getIntersectionPoint(point3d76, point3d80, point3d71, point3d74)
        point3d81 = MathHelper.distanceBearingPoint(point3d77, num3, 100)
        point3d82 = MathHelper.distanceBearingPoint(point3d72, num1, 100)
        point3d11 = MathHelper.getIntersectionPoint(point3d77, point3d81, point3d72, point3d82)
        point3d83 = MathHelper.distanceBearingPoint(point3d14, num5 + Unit.ConvertDegToRad(30), 100)
        point3d84 = MathHelper.distanceBearingPoint(point3d15, num5 + Unit.ConvertDegToRad(30), 100)
        point3d16 = MathHelper.getIntersectionPoint(point3d14, point3d83, point3d65, point3d78)
        point3d17 = MathHelper.getIntersectionPoint(point3d15, point3d84, point3d67, point3d79)
        point3d22 = MathHelper.getIntersectionPoint(point3d11, point3d77, point3d14, point3d83)
        if (not point3d76.smethod_171(finish, 0.001)):
            point3d25 = MathHelper.distanceBearingPoint(point3d76, MathHelper.getBearing(point3d76, finish), MathHelper.calcDistance(point3d76, finish) / 2);
            point3d25 = MathHelper.distanceBearingPoint(center, MathHelper.getBearing(center, point3d25), MathHelper.calcDistance(center, point3d76));
            point3d26 = MathHelper.distanceBearingPoint(point3d77, MathHelper.getBearing(point3d77, point3d13), MathHelper.calcDistance(point3d77, point3d13) / 2);
            point3d26 = MathHelper.distanceBearingPoint(center, MathHelper.getBearing(center, point3d26), MathHelper.calcDistance(center, point3d77));
            self.secondary.append(SecondaryObstacleArea(point3d76, point3d25, finish, point3d77, 0.0, point3d26, point3d13))
        if (not finish.smethod_171(point3d15, 0.001)):
            point3d25 = MathHelper.distanceBearingPoint(finish, MathHelper.getBearing(finish, point3d15), MathHelper.calcDistance(finish, point3d15) / 2);
            point3d25 = MathHelper.distanceBearingPoint(center1, MathHelper.getBearing(center1, point3d25), MathHelper.calcDistance(center1, finish));
            point3d26 = MathHelper.distanceBearingPoint(point3d13, MathHelper.getBearing(point3d13, point3d14), MathHelper.calcDistance(point3d13, point3d14) / 2);
            point3d26 = MathHelper.distanceBearingPoint(center1, MathHelper.getBearing(center1, point3d26), MathHelper.calcDistance(center1, point3d13));
            self.secondary.append(SecondaryObstacleArea(finish, point3d25, point3d15, point3d13, 0.0, point3d26, point3d14));
        if (not MathHelper.smethod_115(point3d17, point3d67, point3d65)) or not (MathHelper.smethod_115(point3d16, point3d67, point3d65)):
            point3d16 = MathHelper.getIntersectionPoint(point3d14, point3d83, point3d29, point3d30)
            point3d17 = MathHelper.getIntersectionPoint(point3d15, point3d84, point3d29, point3d30)
            point3d18 = point3d16
            point3d19 = point3d17;
            point3d20 = point3d16;
            point3d21 = point3d17;
            self.secondary.append(SecondaryObstacleArea(point3d15, point3d17, point3d14, point3d16, num5))
        else:
            return2 = []
            if (MathHelper.smethod_115(point3d14, point3d65, point3d78) and MathHelper.smethod_34(point3d65, point3d78, center1, MathHelper.calcDistance(point3d14, center1), return2) == IntersectionStatus.Intersection):
                point3d25 = return2[0]
                point3d26 = return2[1]
                if (not MathHelper.smethod_115(point3d77, point3d65, point3d78)):
                    point3d14 = point3d25
                    point3d16 = point3d25
                    point3d22 = MathHelper.getIntersectionPoint(point3d11, point3d77, point3d14, MathHelper.distanceBearingPoint(point3d14, num7, 100))
                else:
                    point3d77 = MathHelper.getIntersectionPoint(point3d11, point3d77, point3d65, point3d78)
                    point3d13 = point3d77;
                    point3d14 = point3d77;
                    point3d16 = point3d77;
                    point3d22 = point3d77;
            return2 = []
            if (MathHelper.smethod_115(point3d15, point3d67, point3d79) and MathHelper.smethod_34(point3d67, point3d79, center1, MathHelper.calcDistance(point3d15, center1), return2) == IntersectionStatus.Intersection):
                point3d25 = return2[0]
                point3d26 = return2[1] 
                point3d15 = point3d25;
                point3d17 = point3d25;
            if (not point3d15.smethod_171(point3d17, 0.001) and not MathHelper.smethod_119(point3d15, point3d79, point3d67)):
                self.secondary.append(SecondaryObstacleArea(point3d15, point3d17, point3d14, point3d16, num5))

            point3d18 = point3d65;
            point3d19 = point3d67;
            point3d20 = point3d64;
            point3d21 = point3d63;
            self.secondary.append(SecondaryObstacleArea(point3d17, point3d19, point3d16, point3d18, num5));
            self.secondary.append(SecondaryObstacleArea(point3d19, point3d21, point3d18, point3d20, num5));

        point3d85 = MathHelper.distanceBearingPoint(point3d23, num2, metres6 / 2);
        point3d86 = MathHelper.distanceBearingPoint(point3d23, num2, metres6);
        point3d87 = MathHelper.distanceBearingPoint(point3d85, num1 + Unit.ConvertDegToRad(num11 / 2), 100)
        point3d88 = MathHelper.distanceBearingPoint(point3d86, num1 + Unit.ConvertDegToRad(num11 / 2), 100)
        point3d89 = MathHelper.distanceBearingPoint(point3d68, num8, 100);
        point3d90 = MathHelper.distanceBearingPoint(point3d66, num8, 100);
        point3d4 = MathHelper.getIntersectionPoint(point3d85, point3d87, point3d68, point3d89)
        point3d5 = MathHelper.getIntersectionPoint(point3d86, point3d88, point3d66, point3d90)
        if (not MathHelper.smethod_115(point3d68, position2, point3d85)):
            if (not MathHelper.smethod_115(point3d85, point3d68, point3d89)):
                point3d85 = MathHelper.getIntersectionPoint(position2, point3d85, point3d68, point3d89)
                point3d4 = point3d85;
                point3d6 = point3d68;
            elif (not MathHelper.smethod_115(point3d4, point3d66, point3d68)):
                point3d4 = MathHelper.getIntersectionPoint(point3d85, point3d4, point3d66, point3d68)
                point3d6 = point3d4;
            else:
                point3d6 = point3d68;
            point3d8 = point3d61;
        else:
            if (MathHelper.smethod_119(point3d85, point3d61, point3d68)):
                point3d85 = MathHelper.getIntersectionPoint(position2, point3d85, point3d61, point3d68)
            point3d4 = point3d85;
            point3d6 = point3d85;
            point3d8 = point3d61;
        if (not MathHelper.smethod_115(point3d66, position3, point3d86)):
            if (not MathHelper.smethod_115(point3d86, point3d66, point3d90)):
                point3d88 = MathHelper.distanceBearingPoint(point3d86, num5 + Unit.ConvertDegToRad(15), 100);
                point3d5 = MathHelper.getIntersectionPoint(point3d86, point3d88, point3d66, point3d90)
                if (not MathHelper.smethod_115(point3d5, point3d66, point3d68)):
                    point3d5 = MathHelper.getIntersectionPoint(point3d86, point3d5, point3d62, point3d66)
                    point3d7 = point3d5;
                else:
                    point3d7 = point3d66;
            elif (not MathHelper.smethod_115(point3d5, point3d66, point3d68)):
                point3d5 = MathHelper.getIntersectionPoint(point3d86, point3d5, point3d66, point3d68)
                point3d7 = point3d5;
            else:
                point3d7 = point3d66;
            point3d9 = point3d62;
        else:
            if (MathHelper.smethod_119(point3d86, point3d62, point3d66)):
                point3d86 = MathHelper.getIntersectionPoint(position3, point3d86, point3d62, point3d66)
            
            point3d5 = point3d86;
            point3d7 = point3d86;
            point3d9 = point3d62;
        if (not point3d85.smethod_171(point3d4, 0.001) or not point3d86.smethod_171(point3d5, 0.001)):
            if (MathHelper.smethod_115(point3d86, point3d66, point3d90) or point3d85.smethod_171(point3d4, 0.001) or point3d86.smethod_171(point3d5, 0.001)):
                self.secondary.append(SecondaryObstacleArea(point3d85, point3d4, point3d86, point3d5, MathHelper.getBearing(point3d85, point3d4)));
            else:
                self.secondary.append(SecondaryObstacleArea(point3d85, point3d4, point3d86, point3d86, MathHelper.getBearing(point3d85, point3d4)));
                self.secondary.append(SecondaryObstacleArea(point3d4, point3d4, point3d86, point3d5, num5));
            
        if (not point3d4.smethod_171(point3d6, 0.001) or not point3d5.smethod_171(point3d7, 0.001)):
            self.secondary.append(SecondaryObstacleArea(point3d4, point3d6, point3d5, point3d7, num5));

        if (not point3d6.smethod_171(point3d8, 0.001) or not point3d7.smethod_171(point3d9, 0.001)):
            self.secondary.append(SecondaryObstacleArea(point3d6, point3d8, point3d7, point3d9, num5));

        self.secondary.append(SecondaryObstacleArea(position1, point3d70, position, point3d69, num1));
        self.secondary.append(SecondaryObstacleArea(point3d70, point3d10, point3d69, point3d75, num1));
        self.secondary.append(SecondaryObstacleArea(point3d10, point3d12, point3d75, point3d11, num1));
        self.secondary.append(SecondaryObstacleArea(point3d12, point3d76, point3d11, point3d77, num5));
        self.secondary.append(SecondaryObstacleArea(position2, point3d85, position3, point3d86, num1));
#         point3dCollection2 = self.selectionArea;
        point3dArray = [point3d69, point3d75, point3d11, point3d77, point3d22, point3d14, point3d16, point3d18, point3d20, point3d21, point3d30, point3d8, point3d9, point3d7, point3d5, point3d86]
        self.selectionArea.extend(point3dArray)
#         self.selectionArea.smethod_146()
        point3dArray = [point3d70, point3d10, point3d12, point3d76, finish, point3d15, point3d17, point3d19, point3d21, point3d30, point3d8, point3d6, point3d4, point3d85]
        polylineArea4.method_7(point3dArray)
        if (not point3d76.smethod_171(finish, 0.001)):
            polylineArea4[polylineArea4.Count - 11].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d76, finish, center)
        if (not finish.smethod_171(point3d15, 0.001)):
            polylineArea4[polylineArea4.Count - 10].bulge = MathHelper.smethod_57(TurnDirection.Right, finish, point3d15, center1)
        self.primary.append(PrimaryObstacleArea(polylineArea4))
        point3dArray = [point3d69, point3d75, point3d11, point3d77, point3d13, point3d14, point3d16, point3d18, point3d20]
        polylineArea.method_7(point3dArray);
        if (not point3d77.smethod_171(point3d13, 0.001)):
            polylineArea[polylineArea.Count - 6].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d77, point3d13, center)
        if (not point3d13.smethod_171(point3d14, 0.001)):
            polylineArea[polylineArea.Count - 5].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d13, point3d14, center1)
        point3dArray = [point3d70, point3d10, point3d12, point3d76, finish, point3d15, point3d17, point3d19, point3d21]
        polylineArea1.method_7(point3dArray)
        if (not point3d76.smethod_171(finish, 0.001)):
            polylineArea1[polylineArea1.Count - 6].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d76, finish, center)
        if (not finish.smethod_171(point3d15, 0.001)):
            polylineArea1[polylineArea1.Count - 5].bulge = MathHelper.smethod_57(TurnDirection.Right, finish, point3d15, center1)
        point3dArray = [point3d85, point3d4, point3d6, point3d8]
        polylineArea3.method_7(point3dArray)
        point3dArray = [point3d86, point3d5, point3d7, point3d9]
        polylineArea2.method_7(point3dArray)
        self.drawingLines.append(polylineArea)
        self.drawingLines.append(polylineArea2)
        self.drawingLines.append(polylineArea1)
        self.drawingLines.append(polylineArea3)
        point3d91 = MathHelper.distanceBearingPoint(point3d29, num4, num12)
        point3d92 = MathHelper.distanceBearingPoint(point3d29, num5, num12)
        point3dArray = [point3d31, MathHelper.distanceBearingPoint(point3d29, num4, num12 + num), point3d91, point3d92, MathHelper.distanceBearingPoint(point3d29, num5, num12 + num)]
        self.nominalLine = PolylineArea(point3dArray)
        self.nominalLine[2].bulge = MathHelper.smethod_59(num1, point3d91, point3d92)
#         List<PolylineArea> polylineAreas2 = self.drawingLines;
        point3dArray = [point3d20, point3d21, point3d30, point3d8, point3d9]
        self.drawingLines.append(PolylineArea(point3dArray))
#         List<PolylineArea> polylineAreas3 = self.drawingLines;
        point3dArray = [point3d, point3d1, point3d2, point3d3, point3d]
        self.drawingLines.append(PolylineArea(point3dArray))
#         List<PolylineArea> polylineAreas4 = self.drawingLines;
        point3dArray = [point3d57, point3d58, point3d59, point3d60, point3d57]
        self.drawingLines.append(PolylineArea(point3dArray))

    def vmethod_4(self, gnssSegmentObstacles_0):
        gnssSegmentObstacles_0.method_16(self.initialOca)

class InitialSegment2(IGnssSegment):
#             return RnavSegmentType.Initial2;

    def __init__(self, position_0, position_1, position_2, position_3, rnavSpecification_0, aircraftSpeedCategory_0, altitude_0):
        self.Type = RnavSegmentType.Initial2
        self.drawingLines = []
        self.selectionArea = []
        self.primary = []
        self.secondary = []

        rnavCommonWaypointIAWP2 = []
        point3dArray = []
        point3d21 = position_1
        point3d22 = position_2
        point3d23 = position_0
        point3d24 = position_3
        self.primaryMoc = altitude_0.Metres
        num = MathHelper.getBearing(point3d23, point3d21);
        num1 = MathHelper.smethod_4(num + 1.5707963267949);
        num2 = MathHelper.smethod_4(num - 1.5707963267949);
        num3 = MathHelper.smethod_4(num + 3.14159265358979);
        num4 = MathHelper.getBearing(point3d21, point3d22);
        num5 = MathHelper.smethod_4(num4 + 1.5707963267949);
        num6 = MathHelper.smethod_4(num4 - 1.5707963267949);
        num7 = MathHelper.smethod_4(num4 + 3.14159265358979);
        num8 = Unit.ConvertDegToRad(30);
        if (MathHelper.calcDistance(point3d24, point3d23) > (Distance(30, DistanceUnits.NM)).Metres and rnavSpecification_0 == RnavSpecification.RnpApch):
            raise UserWarning, Messages.ERR_DISTANCE_BETWEEN_X_AND_ARP_EXCEEDS_RNP_SPEC % "Initial Approach Waypoint 2"

        rnavGnssTolerance1 = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0)
        metres = rnavGnssTolerance1.getASWMetres()
        metres1 = rnavGnssTolerance1.getATTMetres();
        metres2 = rnavGnssTolerance1.getXTTMetres();
        rnavGnssTolerance2 = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0)
        metres3 = rnavGnssTolerance2.getASWMetres()
        metres4 = rnavGnssTolerance2.getATTMetres()
        metres5 = rnavGnssTolerance2.getXTTMetres()
        if rnavSpecification_0 != RnavSpecification.RnpApch:
            rnavGnssTolerance = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.StarSid, aircraftSpeedCategory_0) 
        else:
            rnavGnssTolerance = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0)

        metres6 = rnavGnssTolerance.getASWMetres()
        metres7 = rnavGnssTolerance.getATTMetres()
        metres8 = rnavGnssTolerance.getXTTMetres()
#         self.waypoints.Add(new Symbol(SymbolType.Flyb));
#         self.waypoints[0].Tag = point3d23;
#         if (!Geo.DatumLoaded)
#         {
#             Symbol item = self.waypoints[0];
#             rnavCommonWaypointIAWP2 = new string[] { Enums.RnavCommonWaypoint_IAWP2 };
#             item.Attributes = new SymbolAttributes(rnavCommonWaypointIAWP2);
#         }
#         else
#         {
#             position_0.method_1(out degree, out degree1);
#             Symbol symbolAttribute = self.waypoints[0];
#             rnavCommonWaypointIAWP2 = new string[] { Enums.RnavCommonWaypoint_IAWP2, degree.ToString(), degree1.ToString() };
#             symbolAttribute.Attributes = new SymbolAttributes(rnavCommonWaypointIAWP2);
#         }
        polylineArea = PolylineArea()
        polylineArea1 = PolylineArea()
        polylineArea2 = PolylineArea()
        polylineArea3 = PolylineArea()
        polylineArea4 = PolylineArea()
        return2 = []
        flag = MathHelper.smethod_34(point3d23, point3d21, point3d24, Unit.ConvertNMToMeter(30), return2) == IntersectionStatus.Intersection
        point3d4 = return2[0]
        point3d5 = return2[1]
        flag1 = flag
        if (flag):
            if not MathHelper.smethod_135(MathHelper.getBearing(point3d23, point3d4), MathHelper.getBearing(point3d23, point3d21), Unit.ConvertDegToRad(5), AngleUnits.Radians):
                flag1 = False 
            else:
                flag1 = MathHelper.calcDistance(point3d21, point3d23) > MathHelper.calcDistance(point3d21, point3d4) + (metres6 - metres3 / math.tan(num8))
        if (not flag1):
            point3d = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d23, num, metres4), num2, metres5);
            point3d1 = MathHelper.distanceBearingPoint(point3d, num3, metres4 * 2);
            point3d2 = MathHelper.distanceBearingPoint(point3d1, num1, metres5 * 2);
            point3d3 = MathHelper.distanceBearingPoint(point3d2, num, metres4 * 2);
            point3d25 = MathHelper.distanceBearingPoint(point3d23, num2, metres3);
            point3d26 = MathHelper.distanceBearingPoint(point3d23, num2, metres3 / 2);
            point3d27 = MathHelper.distanceBearingPoint(point3d23, num1, metres3);
            point3d28 = MathHelper.distanceBearingPoint(point3d23, num1, metres3 / 2);
            point3d29 = MathHelper.distanceBearingPoint(point3d25, num3, metres4);
            point3d30 = MathHelper.distanceBearingPoint(point3d26, num3, metres4);
            point3d31 = MathHelper.distanceBearingPoint(point3d27, num3, metres4);
            point3d32 = MathHelper.distanceBearingPoint(point3d28, num3, metres4);
            point3dArray = [point3d29, point3d25]
            polylineArea.method_7(point3dArray)
            point3dArray = [point3d30, point3d26]
            polylineArea1.method_7(point3dArray)
            point3dArray = [point3d31, point3d27]
            polylineArea2.method_7(point3dArray)
            point3dArray = [point3d32, point3d28]
            polylineArea3.method_7(point3dArray)
            point3dArray = [point3d32, point3d30]
            polylineArea4.method_7(point3dArray)
#             point3dCollection = self.selectionArea
            point3dArray = [point3d31, point3d29]
            self.selectionArea.extend(point3dArray)
            self.secondary.append(SecondaryObstacleArea(point3d30, point3d26, point3d29, point3d25, num));
            self.secondary.append(SecondaryObstacleArea(point3d32, point3d28, point3d31, point3d27, num));
#             List<PolylineArea> polylineAreas = self.drawingLines;
            point3dArray = [point3d29, point3d31]
            self.drawingLines.append(PolylineArea(point3dArray))
        else:
            point3d = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d23, num, metres7), num2, metres8);
            point3d1 = MathHelper.distanceBearingPoint(point3d, num3, metres7 * 2);
            point3d2 = MathHelper.distanceBearingPoint(point3d1, num1, metres8 * 2);
            point3d3 = MathHelper.distanceBearingPoint(point3d2, num, metres7 * 2);
            point3d33 = MathHelper.distanceBearingPoint(point3d23, num2, metres6);
            point3d34 = MathHelper.distanceBearingPoint(point3d23, num2, metres6 / 2);
            point3d35 = MathHelper.distanceBearingPoint(point3d23, num1, metres6);
            point3d36 = MathHelper.distanceBearingPoint(point3d23, num1, metres6 / 2);
            point3d37 = MathHelper.distanceBearingPoint(point3d33, num3, metres7);
            point3d38 = MathHelper.distanceBearingPoint(point3d34, num3, metres7);
            point3d39 = MathHelper.distanceBearingPoint(point3d35, num3, metres7);
            point3d40 = MathHelper.distanceBearingPoint(point3d36, num3, metres7);
            point3d41 = MathHelper.distanceBearingPoint(point3d4, num2, metres6);
            point3d42 = MathHelper.distanceBearingPoint(point3d4, num2, metres6 / 2);
            point3d43 = MathHelper.distanceBearingPoint(point3d4, num1, metres6);
            point3d44 = MathHelper.distanceBearingPoint(point3d4, num1, metres6 / 2);
            point3d5 = MathHelper.distanceBearingPoint(point3d4, num, (metres6 - metres3) / math.tan(num8))
            point3d45 = MathHelper.distanceBearingPoint(point3d5, num2, metres3);
            point3d46 = MathHelper.distanceBearingPoint(point3d5, num2, metres3 / 2);
            point3d47 = MathHelper.distanceBearingPoint(point3d5, num1, metres3);
            point3d48 = MathHelper.distanceBearingPoint(point3d5, num1, metres3 / 2);
            point3dArray = [point3d37, point3d33, point3d41, point3d45]
            polylineArea.method_7(point3dArray)
            point3dArray = [point3d38, point3d34, point3d42, point3d46]
            polylineArea1.method_7(point3dArray)
            point3dArray = [point3d39, point3d35, point3d43, point3d47]
            polylineArea2.method_7(point3dArray)
            point3dArray = [point3d40, point3d36, point3d44, point3d48]
            polylineArea3.method_7(point3dArray)
            point3dArray = [point3d48, point3d44, point3d36, point3d40, point3d38, point3d34, point3d42, point3d46]
            polylineArea4.method_7(point3dArray)
#             Point3dCollection point3dCollection1 = self.selectionArea;
            point3dArray = [point3d47, point3d43, point3d35, point3d39, point3d37, point3d33, point3d41, point3d45]
            self.selectionArea.extend(point3dArray)
            self.secondary.append(SecondaryObstacleArea(point3d38, point3d42, point3d37, point3d41, num));
            self.secondary.append(SecondaryObstacleArea(point3d40, point3d44, point3d39, point3d43, num));
            self.secondary.append(SecondaryObstacleArea(point3d42, point3d46, point3d41, point3d45, num));
            self.secondary.append(SecondaryObstacleArea(point3d44, point3d48, point3d43, point3d47, num));
#             List<PolylineArea> polylineAreas1 = self.drawingLines;
            point3dArray = [point3d37, point3d39]
            self.drawingLines.append(PolylineArea(point3dArray))

        point3d49 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d21, num, metres1), num2, metres2);
        point3d50 = MathHelper.distanceBearingPoint(point3d49, num3, metres1 * 2);
        point3d51 = MathHelper.distanceBearingPoint(point3d50, num1, metres2 * 2);
        point3d52 = MathHelper.distanceBearingPoint(point3d51, num, metres1 * 2);
        return1 = []
        num9 = MathHelper.smethod_77(Unit.smethod_1(num), Unit.smethod_1(num4), AngleUnits.Degrees, return1)
        turnDirection = return1[0]
        if (turnDirection == TurnDirection.Nothing or num9 < 0.5):
            position = polylineArea[polylineArea.Count - 1].position
            position1 = polylineArea1[polylineArea1.Count - 1].position
            position2 = polylineArea2[polylineArea2.Count - 1].position
            position3 = polylineArea3[polylineArea3.Count - 1].position
            point3d53 = MathHelper.distanceBearingPoint(point3d21, num2, metres3);
            point3d54 = MathHelper.distanceBearingPoint(point3d21, num2, metres3 / 2);
            point3d55 = MathHelper.distanceBearingPoint(point3d21, num1, metres3);
            point3d56 = MathHelper.distanceBearingPoint(point3d21, num1, metres3 / 2);
            polylineArea.method_1(point3d53)
            polylineArea1.method_1(point3d54)
            polylineArea2.method_1(point3d55)
            polylineArea3.method_1(point3d56)
            point3dArray = [point3d54, point3d56]
            polylineArea4.method_7(point3dArray)
#             point3dCollection2 = self.selectionArea;
            point3dArray = [point3d53, point3d55]
            self.selectionArea.extend(point3dArray)
            self.secondary.append(SecondaryObstacleArea(position1, point3d54, position, point3d53, num));
            self.secondary.append(SecondaryObstacleArea(position3, point3d56, position2, point3d55, num));
#             List<PolylineArea> polylineAreas2 = self.drawingLines;
            point3dArray = [point3d53, point3d55]
            self.drawingLines.append(PolylineArea(point3dArray))
        else:
            position4 = polylineArea[polylineArea.Count - 1].position
            position5 = polylineArea1[polylineArea1.Count - 1].position
            position6 = polylineArea2[polylineArea2.Count - 1].position
            position7 = polylineArea3[polylineArea3.Count - 1].position
            point3d57 = MathHelper.distanceBearingPoint(point3d21, num2, metres3)
            point3d58 = MathHelper.distanceBearingPoint(point3d21, num2, metres3 / 2);
            point3d59 = MathHelper.distanceBearingPoint(point3d21, num1, metres3);
            point3d60 = MathHelper.distanceBearingPoint(point3d21, num1, metres3 / 2);
            point3d61 = MathHelper.distanceBearingPoint(point3d21, num6, metres);
            point3d62 = MathHelper.distanceBearingPoint(point3d21, num6, metres / 2);
            point3d63 = MathHelper.distanceBearingPoint(point3d21, num5, metres);
            point3d64 = MathHelper.distanceBearingPoint(point3d21, num5, metres / 2);
            point3d65 = MathHelper.distanceBearingPoint(point3d61, num7, metres1);
            point3d66 = MathHelper.distanceBearingPoint(point3d62, num7, metres1);
            point3d67 = MathHelper.distanceBearingPoint(point3d63, num7, metres1);
            point3d68 = MathHelper.distanceBearingPoint(point3d64, num7, metres1);
            if (turnDirection != TurnDirection.Right):
                point3d6 = position4;
                point3d7 = MathHelper.getIntersectionPoint(position4, point3d57, point3d61, point3d63)
                point3d8 = MathHelper.getIntersectionPoint(point3d65, point3d61, point3d57, point3d59)
                point3d9 = position5;
                point3d10 = MathHelper.getIntersectionPoint(position5, point3d58, point3d61, point3d63)
                point3d11 = MathHelper.getIntersectionPoint(point3d66, point3d62, point3d57, point3d59)
                point3d12 = position6;
                point3d13 = point3d59;
                point3d14 = point3d63;
                point3d15 = position7;
                point3d16 = point3d60;
                point3d17 = point3d64;
                point3dArray = [point3d7, point3d8]
                polylineArea.method_7(point3dArray)
                point3dArray = [point3d10, point3d11]
                polylineArea1.method_7(point3dArray)
                point3dArray = [point3d13, point3d14]
                polylineArea2.method_7(point3dArray)
                polylineArea2[polylineArea2.Count - 2].bulge = MathHelper.smethod_57(TurnDirection.Left, point3d13, point3d14, point3d21)
                point3dArray = [point3d16, point3d17]
                polylineArea3.method_7(point3dArray)
                polylineArea3[polylineArea3.Count - 2].bulge = MathHelper.smethod_57(TurnDirection.Left, point3d16, point3d17, point3d21)
                point3d20 = MathHelper.getIntersectionPoint(point3d13, MathHelper.distanceBearingPoint(point3d13, num, 100), point3d14, MathHelper.distanceBearingPoint(point3d14, num7, 100))
#                 point3dCollection3 = self.selectionArea;
                point3dArray = [point3d7, point3d8, point3d21, point3d14, point3d20, point3d13]
                self.selectionArea.extend(point3dArray)
                point3d18 = MathHelper.distanceBearingPoint(point3d21, MathHelper.getBearing(point3d21, point3d20), metres);
                point3d19 = MathHelper.distanceBearingPoint(point3d21, MathHelper.getBearing(point3d21, point3d20), metres / 2);
                point3dArray = [point3d10, point3d11, point3d21, point3d17, point3d16]
                polylineArea4.method_7(point3dArray)
                polylineArea4[polylineArea4.Count - 2].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d17, point3d16, point3d21)
                self.secondary.append(SecondaryObstacleArea(point3d9, point3d10, point3d6, point3d7, num))
                self.secondary.append(SecondaryObstacleArea(point3d15, point3d16, point3d12, point3d13, num))
                self.secondary.append(SecondaryObstacleArea(point3d10, point3d11, point3d7, point3d8, MathHelper.getBearing(point3d10, point3d11)))
                self.secondary.append(SecondaryObstacleArea(point3d16, point3d19, point3d17, point3d13, 0.0, point3d18, point3d14))
            else:
                point3d6 = position4;
                point3d7 = point3d57;
                point3d8 = point3d61;
                point3d9 = position5;
                point3d10 = point3d58;
                point3d11 = point3d62;
                point3d12 = position6;
                point3d13 = MathHelper.getIntersectionPoint(position6, point3d59, point3d61, point3d63)
                point3d14 = MathHelper.getIntersectionPoint(point3d67, point3d63, point3d57, point3d59)
                point3d15 = position7;
                point3d16 = MathHelper.getIntersectionPoint(position7, point3d60, point3d61, point3d63)
                point3d17 = MathHelper.getIntersectionPoint(point3d68, point3d64, point3d57, point3d59)
                point3dArray = [point3d7, point3d8]
                polylineArea.method_7(point3dArray)
                polylineArea[polylineArea.Count - 2].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d7, point3d8, point3d21)
                point3dArray = [point3d10, point3d11]
                polylineArea1.method_7(point3dArray)
                polylineArea1[polylineArea1.Count - 2].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d10, point3d11, point3d21)
                point3dArray = [point3d13, point3d14]
                polylineArea2.method_7(point3dArray)
                point3dArray = [point3d16, point3d17]
                polylineArea3.method_7(point3dArray)
                point3d20 = MathHelper.getIntersectionPoint(point3d7, MathHelper.distanceBearingPoint(point3d7, num, 100), point3d8, MathHelper.distanceBearingPoint(point3d8, num7, 100))
#                 point3dCollection4 = self.selectionArea;
                point3dArray = [point3d7, point3d20, point3d8, point3d21, point3d14, point3d13]
                self.selectionArea.extend(point3dArray)
                point3d18 = MathHelper.distanceBearingPoint(point3d21, MathHelper.getBearing(point3d21, point3d20), metres);
                point3d19 = MathHelper.distanceBearingPoint(point3d21, MathHelper.getBearing(point3d21, point3d20), metres / 2);
                point3dArray = [point3d10, point3d11, point3d21, point3d17, point3d16]
                polylineArea4.method_7(point3dArray)
                polylineArea4[polylineArea4.Count - 5].bulge = MathHelper.smethod_57(TurnDirection.Right, point3d10, point3d11, point3d21)
                self.secondary.append(SecondaryObstacleArea(point3d9, point3d10, point3d6, point3d7, num))
                self.secondary.append(SecondaryObstacleArea(point3d15, point3d16, point3d12, point3d13, num))
                self.secondary.append(SecondaryObstacleArea(point3d10, point3d19, point3d11, point3d7, 0.0, point3d18, point3d8))
                self.secondary.append(SecondaryObstacleArea(point3d16, point3d17, point3d13, point3d14, MathHelper.getBearing(point3d16, point3d17)))

#             <PolylineArea> polylineAreas3 = self.drawingLines;
            point3dArray = [point3d8, point3d21, point3d14]
            self.drawingLines.append(PolylineArea(point3dArray))
#             List<PolylineArea> polylineAreas4 = self.drawingLines;
            point3dArray = [point3d49, point3d50, point3d51, point3d52, point3d49]
            self.drawingLines.append(PolylineArea(point3dArray))

#         List<PolylineArea> polylineAreas5 = self.drawingLines;
        point3dArray = [point3d, point3d1, point3d2, point3d3, point3d]
        self.drawingLines.append(PolylineArea(point3dArray))
        self.drawingLines.append(polylineArea)
        self.drawingLines.append(polylineArea2)
        self.drawingLines.append(polylineArea1)
        self.drawingLines.append(polylineArea3)
        point3dArray = [point3d23, point3d21]
        self.nominalLine = PolylineArea(point3dArray)
        self.primary.append(PrimaryObstacleArea(polylineArea4))

    def vmethod_4(self, gnssSegmentObstacles_0):
        gnssSegmentObstacles_0.method_15();

class InitialSegment3(IGnssSegment):

#     def __init__(self):
#             return RnavSegmentType.Initial3;

    def __init__(self, position_0, position_1, position_2, position_3, rnavSpecification_0, aircraftSpeedCategory_0, speed_0, altitude_0, double_0, double_1, speed_1, altitude_1):
        self.Type = RnavSegmentType.Initial3
        self.drawingLines = []
        self.selectionArea = []
        self.primary = []
        self.secondary = []
        
        rnavCommonWaypointIAWP3 = []
        strArrays = []
        point3dArray = []
        point3d29 = position_1
        point3d30 = position_2
        point3d31 = position_0
        point3d32 = position_3
        self.primaryMoc = altitude_1.Metres
        self.initialOca = altitude_0
        num1 = MathHelper.getBearing(point3d31, point3d29);
        num2 = MathHelper.smethod_4(num1 + 1.5707963267949);
        num3 = MathHelper.smethod_4(num1 - 1.5707963267949);
        num4 = MathHelper.smethod_4(num1 + 3.14159265358979);
        num5 = MathHelper.getBearing(point3d29, point3d30);
        num6 = MathHelper.smethod_4(num5 + 1.5707963267949);
        num7 = MathHelper.smethod_4(num5 - 1.5707963267949);
        num8 = MathHelper.smethod_4(num5 + 3.14159265358979);
        num9 = Unit.ConvertDegToRad(30);
        if (MathHelper.calcDistance(point3d32, point3d31) > (Distance(30, DistanceUnits.NM)).Metres and rnavSpecification_0 == RnavSpecification.RnpApch):
            raise UserWarning, Messages.ERR_DISTANCE_BETWEEN_X_AND_ARP_EXCEEDS_RNP_SPEC % "Initial Approach Waypoint 3"
        rnavGnssTolerance1 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Faf, aircraftSpeedCategory_0);
        metres = rnavGnssTolerance1.getASWMetres();
        metres1 = rnavGnssTolerance1.getATTMetres();
        metres2 = rnavGnssTolerance1.getXTTMetres();
        rnavGnssTolerance2 = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0);
        metres3 = rnavGnssTolerance2.getASWMetres();
        metres4 = rnavGnssTolerance2.getATTMetres();
        metres5 = rnavGnssTolerance2.getXTTMetres();
        rnavGnssTolerance3 = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0);
        metres6 = rnavGnssTolerance3.getASWMetres();
        metres7 = rnavGnssTolerance3.getATTMetres();
        metres8 = rnavGnssTolerance3.getXTTMetres()
        if rnavSpecification_0 != RnavSpecification.RnpApch:
            rnavGnssTolerance = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.StarSid, aircraftSpeedCategory_0) 
        else:
            rnavGnssTolerance = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0)
        metres9 = rnavGnssTolerance.getASWMetres();
        metres10 = rnavGnssTolerance.getATTMetres();
        num10 = rnavGnssTolerance.getXTTMetres();
        num11 = MathHelper.smethod_76(Unit.smethod_1(num1), Unit.smethod_1(num5), AngleUnits.Degrees);
        speed = Speed.smethod_0(speed_0, double_0, altitude_0);
        distance = Distance.smethod_0(speed, double_1);
        metres11 = distance.Metres
        num12 = metres11 * math.tan(Unit.ConvertDegToRad(0.5 * num11))
        if aircraftSpeedCategory_0 != AircraftSpeedCategory.H:
            num = 5 * speed.MetresPerSecond 
        else:
            num = 3 * speed.MetresPerSecond
        distance1 = Distance(num12 + num);
        if (distance1.Metres > MathHelper.calcDistance(point3d31, point3d29)):
            eRRINSUFFICIENTMINIMUMSTABILISATIONDISTANCE = Messages.ERR_INSUFFICIENT_MINIMUM_STABILISATION_DISTANCE;
            raise UserWarning, eRRINSUFFICIENTMINIMUMSTABILISATIONDISTANCE

        distance2 = Distance(num12 + num + Unit.ConvertNMToMeter(2))
        if (distance2.Metres > MathHelper.calcDistance(point3d29, point3d30)):
            strMsg = Messages.ERR_INSUFFICIENT_MINIMUM_STABILISATION_DISTANCE;
            rnavCommonWaypointIAWP3 = ["Intermediate Waypoint", "Final Approach Waypoint", distance2.Metres ]
            raise UserWarning, strMsg % ("Intermediate Waypoint", "Final Approach Waypoint", distance2.Metres)

        distance = RnavWaypoints.getDistanceFromWaypointToEarliestTurningPoint(RnavWaypointType.FlyBy, Distance(metres4), Distance(metres11), num11, AngleUnits.Degrees)
        metres12 = distance.Metres
        if metres12 >= 0:
            point3d6 = MathHelper.distanceBearingPoint(point3d29, num4, math.fabs(metres12)) 
        else:
            point3d6 = MathHelper.distanceBearingPoint(point3d29, num1, math.fabs(metres12))
        distance = RnavWaypoints.smethod_13(RnavFlightPhase.IafIf, RnavWaypointType.FlyBy, speed, speed_1, Distance(metres4), Distance(metres11), num11, AngleUnits.Degrees)
        metres13 = distance.Metres
        if metres13 >= 0 :
            point3d7 = MathHelper.distanceBearingPoint(point3d29, num4, math.fabs(metres13)) 
        else:
            point3d7 = MathHelper.distanceBearingPoint(point3d29, num1, math.fabs(metres13))

#         self.waypoints.Add(new Symbol(SymbolType.Flyb));
#         self.waypoints[0].Tag = point3d31;
#         if (!Geo.DatumLoaded)
#         {
#             Symbol item = self.waypoints[0];
#             strArrays = new string[] { Enums.RnavCommonWaypoint_IAWP3 };
#             item.Attributes = new SymbolAttributes(strArrays);
#         }
#         else
#         {
#             position_0.method_1(out degree, out degree1);
#             Symbol symbolAttribute = self.waypoints[0];
#             strArrays = new string[] { Enums.RnavCommonWaypoint_IAWP3, degree.ToString(), degree1.ToString() };
#             symbolAttribute.Attributes = new SymbolAttributes(strArrays);
#         }
        polylineArea = PolylineArea();
        polylineArea1 = PolylineArea();
        polylineArea2 = PolylineArea();
        polylineArea3 = PolylineArea();
        polylineArea4 = PolylineArea();
        return2 = []
        flag = MathHelper.smethod_34(point3d31, point3d29, point3d32, Unit.ConvertNMToMeter(30), return2) == IntersectionStatus.Intersection
        point3d1 = return2[0]
        point3d = return2[1]
        flag1 = flag
        if (flag):
            if MathHelper.smethod_135(MathHelper.getBearing(point3d31, point3d1), MathHelper.getBearing(point3d31, point3d29), Unit.ConvertDegToRad(5), AngleUnits.Radians):
                flag1 = False 
            else:
                flag1 = MathHelper.calcDistance(point3d29, point3d31) > MathHelper.calcDistance(point3d29, point3d1) + (metres9 - metres6 / math.tan(num9))
        if (not flag1):
            point3d2 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d31, num1, metres7), num3, metres8);
            point3d3 = MathHelper.distanceBearingPoint(point3d2, num4, metres7 * 2);
            point3d4 = MathHelper.distanceBearingPoint(point3d3, num2, metres8 * 2);
            point3d5 = MathHelper.distanceBearingPoint(point3d4, num1, metres7 * 2);
            point3d33 = MathHelper.distanceBearingPoint(point3d31, num2, metres6);
            point3d34 = MathHelper.distanceBearingPoint(point3d31, num2, metres6 / 2);
            point3d35 = MathHelper.distanceBearingPoint(point3d31, num3, metres6);
            point3d36 = MathHelper.distanceBearingPoint(point3d31, num3, metres6 / 2);
            point3d37 = MathHelper.distanceBearingPoint(point3d33, num4, metres7);
            point3d38 = MathHelper.distanceBearingPoint(point3d34, num4, metres7);
            point3d39 = MathHelper.distanceBearingPoint(point3d35, num4, metres7);
            point3d40 = MathHelper.distanceBearingPoint(point3d36, num4, metres7);
            point3dArray = [point3d37, point3d33]
            polylineArea.method_7(point3dArray)
            point3dArray = [point3d38, point3d34]
            polylineArea1.method_7(point3dArray)
            point3dArray = [point3d39, point3d35]
            polylineArea2.method_7(point3dArray)
            point3dArray = [point3d40, point3d36]
            polylineArea3.method_7(point3dArray)
            point3dArray = [point3d40, point3d38]
            polylineArea4.method_7(point3dArray)
#             point3dCollection = self.selectionArea;
            point3dArray = [point3d39, point3d37]
            self.selectionArea.extend(point3dArray)
            self.secondary.append(SecondaryObstacleArea(point3d38, point3d34, point3d37, point3d33, num1));
            self.secondary.append(SecondaryObstacleArea(point3d40, point3d36, point3d39, point3d35, num1));
#             List<PolylineArea> polylineAreas = self.drawingLines;
            point3dArray = [point3d37, point3d39]
            self.drawingLines.append(PolylineArea(point3dArray))
        else:
            point3d2 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d31, num1, metres10), num3, num10);
            point3d3 = MathHelper.distanceBearingPoint(point3d2, num4, metres10 * 2);
            point3d4 = MathHelper.distanceBearingPoint(point3d3, num2, num10 * 2);
            point3d5 = MathHelper.distanceBearingPoint(point3d4, num1, metres10 * 2);
            point3d41 = MathHelper.distanceBearingPoint(point3d31, num2, metres9);
            point3d42 = MathHelper.distanceBearingPoint(point3d31, num2, metres9 / 2);
            point3d43 = MathHelper.distanceBearingPoint(point3d31, num3, metres9);
            point3d44 = MathHelper.distanceBearingPoint(point3d31, num3, metres9 / 2);
            point3d45 = MathHelper.distanceBearingPoint(point3d41, num4, metres10);
            point3d46 = MathHelper.distanceBearingPoint(point3d42, num4, metres10);
            point3d47 = MathHelper.distanceBearingPoint(point3d43, num4, metres10);
            point3d48 = MathHelper.distanceBearingPoint(point3d44, num4, metres10);
            point3d49 = MathHelper.distanceBearingPoint(point3d1, num2, metres9);
            point3d50 = MathHelper.distanceBearingPoint(point3d1, num2, metres9 / 2);
            point3d51 = MathHelper.distanceBearingPoint(point3d1, num3, metres9);
            point3d52 = MathHelper.distanceBearingPoint(point3d1, num3, metres9 / 2);
            point3d = MathHelper.distanceBearingPoint(point3d1, num1, (metres9 - metres6) / math.tan(num9));
            point3d53 = MathHelper.distanceBearingPoint(point3d, num2, metres6);
            point3d54 = MathHelper.distanceBearingPoint(point3d, num2, metres6 / 2);
            point3d55 = MathHelper.distanceBearingPoint(point3d, num3, metres6);
            point3d56 = MathHelper.distanceBearingPoint(point3d, num3, metres6 / 2);
            point3dArray = [point3d45, point3d41, point3d49, point3d53]
            polylineArea.method_7(point3dArray)
            point3dArray = [point3d46, point3d42, point3d50, point3d54]
            polylineArea1.method_7(point3dArray)
            point3dArray = [point3d47, point3d43, point3d51, point3d55]
            polylineArea2.method_7(point3dArray)
            point3dArray = [point3d48, point3d44, point3d52, point3d56]
            polylineArea3.method_7(point3dArray)
            point3dArray = [point3d56, point3d52, point3d44, point3d48, point3d46, point3d42, point3d50, point3d54]
            polylineArea4.method_7(point3dArray)
#             point3dCollection1 = self.selectionArea;
            point3dArray = [point3d55, point3d51, point3d43, point3d47, point3d45, point3d41, point3d49, point3d53]
            self.selectionArea.extend(point3dArray)
            self.secondary.append(SecondaryObstacleArea(point3d46, point3d50, point3d45, point3d49, num1))
            self.secondary.append(SecondaryObstacleArea(point3d48, point3d52, point3d47, point3d51, num1));
            self.secondary.append(SecondaryObstacleArea(point3d50, point3d54, point3d49, point3d53, num1));
            self.secondary.append(SecondaryObstacleArea(point3d52, point3d56, point3d51, point3d55, num1));
#             List<PolylineArea> polylineAreas1 = self.drawingLines;
            point3dArray = [point3d45, point3d47]
            self.drawingLines.append(PolylineArea(point3dArray))

        point3d57 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d29, num1, metres7), num3, metres5);
        point3d58 = MathHelper.distanceBearingPoint(point3d57, num4, metres4 * 2);
        point3d59 = MathHelper.distanceBearingPoint(point3d58, num2, metres5 * 2);
        point3d60 = MathHelper.distanceBearingPoint(point3d59, num1, metres4 * 2);
        position = polylineArea[polylineArea.Count - 1].position;
        position1 = polylineArea1[polylineArea1.Count - 1].position;
        position2 = polylineArea3[polylineArea3.Count - 1].position;
        position3 = polylineArea2[polylineArea2.Count - 1].position;
        point3d61 = MathHelper.distanceBearingPoint(point3d30, num6, metres / 2);
        point3d62 = MathHelper.distanceBearingPoint(point3d30, num6, metres);
        point3d63 = MathHelper.distanceBearingPoint(point3d30, num7, metres / 2);
        point3d64 = MathHelper.distanceBearingPoint(point3d30, num7, metres);
        point3d65 = MathHelper.distanceBearingPoint(point3d64, num8 + num9, (metres3 - metres) / math.sin(num9));
        point3d66 = MathHelper.distanceBearingPoint(point3d62, num8 - num9, (metres3 - metres) / math.sin(num9));
        point3d67 = MathHelper.distanceBearingPoint(point3d65, num6, metres3 / 2);
        point3d68 = MathHelper.distanceBearingPoint(point3d66, num7, metres3 / 2);
        point3d69 = MathHelper.distanceBearingPoint(point3d7, num2, metres6);
        point3d70 = MathHelper.distanceBearingPoint(point3d7, num2, metres6 / 2);
        windSpiral = WindSpiral(MathHelper.distanceBearingPoint(point3d7, num2, metres6 / 2), num1, speed, speed_1, double_1, TurnDirection.Left);
        windSpiral1 = WindSpiral(MathHelper.distanceBearingPoint(point3d7, num3, metres6 / 2), num1, speed, speed_1, double_1, TurnDirection.Left);
        point3d71 = MathHelper.distanceBearingPoint(windSpiral.Center[0], num2, windSpiral.Radius[0]);
        point3d72 = MathHelper.distanceBearingPoint(point3d71, num2, metres6 / 2);
        point3d73 = MathHelper.distanceBearingPoint(point3d70, MathHelper.getBearing(point3d70, windSpiral.Center[0]) + 1.5707963267949, 100);
        point3d74 = MathHelper.distanceBearingPoint(point3d71, num1, 100);
        point3d14 = MathHelper.getIntersectionPoint(point3d70, point3d73, point3d71, point3d74);
        point3d75 = MathHelper.distanceBearingPoint(point3d14, num2, metres6 / 2);
        point3d76 = MathHelper.distanceBearingPoint(windSpiral1.Center[0], num1, windSpiral1.Radius[0]);
        point3d77 = MathHelper.distanceBearingPoint(windSpiral1.Center[0], num1, windSpiral1.Radius[0] + metres6 / 2);
        point3d78 = MathHelper.distanceBearingPoint(point3d66, num8, 100);
        point3d79 = MathHelper.distanceBearingPoint(point3d68, num8, 100);
        if (MathHelper.smethod_115(point3d76, point3d79, point3d68)):
            point3d77 = MathHelper.getIntersectionPoint(point3d78, point3d66, MathHelper.distanceBearingPoint(point3d77, num3, 100), point3d77)
            point3d76 = MathHelper.getIntersectionPoint(point3d79, point3d68, MathHelper.distanceBearingPoint(point3d76, num3, 100), point3d76)
            point3d17 = point3d77;
            point3d26 = point3d77;
            point3d18 = point3d77;
            point3d20 = point3d77;
            finish = point3d76;
            point3d19 = point3d76;
            point3d21 = point3d76;
            center = windSpiral1.Center[0];
            center1 = windSpiral1.Center[0];
        elif (not MathHelper.smethod_119(point3d76, windSpiral1.Center[0], windSpiral1.Finish[0])):
            point3d76 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], num1, windSpiral1.Radius[1]);
            point3d77 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], num1, windSpiral1.Radius[1] + metres6 / 2);
            finish = point3d76;
            point3d17 = point3d77;
            point3d19 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], num5 + Unit.ConvertDegToRad(60), windSpiral1.Radius[1]);
            point3d18 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], num5 + Unit.ConvertDegToRad(60), windSpiral1.Radius[1] + metres6 / 2)
            center = windSpiral1.Center[1];
            center1 = windSpiral1.Center[1];
        else:
            point3d19 = MathHelper.distanceBearingPoint(windSpiral1.Center[0], num5 + Unit.ConvertDegToRad(60), windSpiral1.Radius[0]);
            point3d18 = MathHelper.distanceBearingPoint(windSpiral1.Center[0], num5 + Unit.ConvertDegToRad(60), windSpiral1.Radius[0] + metres6 / 2);
            if (not MathHelper.smethod_119(point3d19, windSpiral1.Center[0], windSpiral1.Finish[0])):
                finish = windSpiral1.Finish[0];
                point3d17 = MathHelper.distanceBearingPoint(windSpiral1.Center[0], MathHelper.getBearing(windSpiral1.Center[0], windSpiral1.Finish[0]), windSpiral1.Radius[0] + metres6 / 2);
                point3d19 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], num5 + Unit.ConvertDegToRad(60), windSpiral1.Radius[1]);
                point3d18 = MathHelper.distanceBearingPoint(windSpiral1.Center[1], num5 + Unit.ConvertDegToRad(60), windSpiral1.Radius[1] + metres6 / 2);
                center = windSpiral1.Center[0];
                center1 = windSpiral1.Center[1];
            else:
                finish = point3d19;
                point3d17 = point3d18;
                center = windSpiral1.Center[0];
                center1 = windSpiral1.Center[0];

        point3d80 = MathHelper.distanceBearingPoint(point3d76, num2, 100);
        point3d74 = MathHelper.distanceBearingPoint(point3d71, num1, 100);
        point3d16 = MathHelper.getIntersectionPoint(point3d76, point3d80, point3d71, point3d74)
        point3d81 = MathHelper.distanceBearingPoint(point3d77, num2, 100);
        point3d82 = MathHelper.distanceBearingPoint(point3d72, num1, 100);
        point3d15 = MathHelper.getIntersectionPoint(point3d77, point3d81, point3d72, point3d82)
        point3d83 = MathHelper.distanceBearingPoint(point3d18, num5 - Unit.ConvertDegToRad(30), 100);
        point3d84 = MathHelper.distanceBearingPoint(point3d19, num5 - Unit.ConvertDegToRad(30), 100);
        point3d20 = MathHelper.getIntersectionPoint(point3d18, point3d83, point3d66, point3d78)
        point3d21 = MathHelper.getIntersectionPoint(point3d19, point3d84, point3d68, point3d79)
        point3d26 = MathHelper.getIntersectionPoint(point3d15, point3d77, point3d18, point3d83)
        if (not point3d76.smethod_171(finish, 0.001)):
            point3d27 = MathHelper.distanceBearingPoint(point3d76, MathHelper.getBearing(point3d76, finish), MathHelper.calcDistance(point3d76, finish) / 2);
            point3d27 = MathHelper.distanceBearingPoint(center, MathHelper.getBearing(center, point3d27), MathHelper.calcDistance(center, point3d76));
            point3d28 = MathHelper.distanceBearingPoint(point3d77, MathHelper.getBearing(point3d77, point3d17), MathHelper.calcDistance(point3d77, point3d17) / 2);
            point3d28 = MathHelper.distanceBearingPoint(center, MathHelper.getBearing(center, point3d28), MathHelper.calcDistance(center, point3d77));
            self.secondary.append(SecondaryObstacleArea(point3d76, point3d27, finish, point3d77, 0.0, point3d28, point3d17));
        if (not finish.smethod_171(point3d19, 0.001)):
            point3d27 = MathHelper.distanceBearingPoint(finish, MathHelper.getBearing(finish, point3d19), MathHelper.calcDistance(finish, point3d19) / 2);
            point3d27 = MathHelper.distanceBearingPoint(center1, MathHelper.getBearing(center1, point3d27), MathHelper.calcDistance(center1, finish));
            point3d28 = MathHelper.distanceBearingPoint(point3d17, MathHelper.getBearing(point3d17, point3d18), MathHelper.calcDistance(point3d17, point3d18) / 2);
            point3d28 = MathHelper.distanceBearingPoint(center1, MathHelper.getBearing(center1, point3d28), MathHelper.calcDistance(center1, point3d17));
            self.secondary.append(SecondaryObstacleArea(finish, point3d27, point3d19, point3d17, 0.0, point3d28, point3d18));

        if (not MathHelper.smethod_119(point3d21, point3d68, point3d66) or not MathHelper.smethod_119(point3d20, point3d68, point3d66)):
            point3d20 = MathHelper.getIntersectionPoint(point3d18, point3d83, point3d29, point3d30)
            point3d21 = MathHelper.getIntersectionPoint(point3d19, point3d84, point3d29, point3d30)
            point3d22 = point3d20;
            point3d23 = point3d21;
            point3d24 = point3d20;
            point3d25 = point3d21;
            self.secondary.append(SecondaryObstacleArea(point3d19, point3d21, point3d18, point3d20, num5));
        else:
            return2 = []
            if (MathHelper.smethod_119(point3d18, point3d66, point3d78) and MathHelper.smethod_34(point3d66, point3d78, center1, MathHelper.calcDistance(point3d18, center1), return2) == IntersectionStatus.Intersection):
                point3d27 = return2[0]
                point3d28 = return2[1] 
                if (not MathHelper.smethod_119(point3d77, point3d66, point3d78)):
                    point3d18 = point3d27;
                    point3d20 = point3d27;
                    point3d26 = MathHelper.getIntersectionPoint(point3d15, point3d77, point3d18, MathHelper.distanceBearingPoint(point3d18, num7, 100))
                else:
                    point3d77 = MathHelper.getIntersectionPoint(point3d15, point3d77, point3d66, point3d78)
                    point3d17 = point3d77;
                    point3d18 = point3d77;
                    point3d20 = point3d77;
                    point3d26 = point3d77;

            return2 = []
            if (MathHelper.smethod_119(point3d19, point3d68, point3d79) and MathHelper.smethod_34(point3d68, point3d79, center1, MathHelper.calcDistance(point3d19, center1), return2) == IntersectionStatus.Intersection):
                point3d27 = return2[0]
                point3d28 = return2[1]
                point3d19 = point3d27;
                point3d21 = point3d27;

            if (not point3d19.smethod_171(point3d21, 0.001) and not MathHelper.smethod_115(point3d19, point3d79, point3d68)):
                self.secondary.append(SecondaryObstacleArea(point3d19, point3d21, point3d18, point3d20, num5));

            point3d22 = point3d66;
            point3d23 = point3d68;
            point3d24 = point3d62;
            point3d25 = point3d61;
            self.secondary.append(SecondaryObstacleArea(point3d21, point3d23, point3d20, point3d22, num5));
            self.secondary.append(SecondaryObstacleArea(point3d23, point3d25, point3d22, point3d24, num5));

        point3d85 = MathHelper.distanceBearingPoint(point3d6, num3, metres6 / 2);
        point3d86 = MathHelper.distanceBearingPoint(point3d6, num3, metres6);
        point3d87 = MathHelper.distanceBearingPoint(point3d85, num1 - Unit.ConvertDegToRad(num11 / 2), 100);
        point3d88 = MathHelper.distanceBearingPoint(point3d86, num1 - Unit.ConvertDegToRad(num11 / 2), 100);
        point3d89 = MathHelper.distanceBearingPoint(point3d67, num8, 100);
        point3d90 = MathHelper.distanceBearingPoint(point3d65, num8, 100);
        point3d8 = MathHelper.getIntersectionPoint(point3d85, point3d87, point3d67, point3d89)
        point3d9 = MathHelper.getIntersectionPoint(point3d86, point3d88, point3d65, point3d90)
        if (not MathHelper.smethod_119(point3d67, position2, point3d85)):
            if (not MathHelper.smethod_119(point3d85, point3d67, point3d89)):
                point3d85 = MathHelper.getIntersectionPoint(position2, point3d85, point3d67, point3d89)
                point3d8 = point3d85;
                point3d10 = point3d67
            elif (not MathHelper.smethod_119(point3d8, point3d65, point3d67)):
                point3d8 = MathHelper.getIntersectionPoint(point3d85, point3d8, point3d65, point3d67)
                point3d10 = point3d8;
            else:
                point3d10 = point3d67;
            point3d12 = point3d63;
        else:
            if (MathHelper.smethod_115(point3d85, point3d63, point3d67)):
                point3d85 = MathHelper.getIntersectionPoint(position2, point3d85, point3d63, point3d67)
            point3d8 = point3d85;
            point3d10 = point3d85;
            point3d12 = point3d63;

        if (not MathHelper.smethod_119(point3d65, position3, point3d86)):

            if (not MathHelper.smethod_119(point3d86, point3d65, point3d90)):
                point3d88 = MathHelper.distanceBearingPoint(point3d86, num5 - Unit.ConvertDegToRad(15), 100);
                point3d9 = MathHelper.getIntersectionPoint(point3d86, point3d88, point3d65, point3d90)
                if (not MathHelper.smethod_119(point3d9, point3d65, point3d67)):
                    point3d9 = MathHelper.getIntersectionPoint(point3d86, point3d9, point3d64, point3d65)
                    point3d11 = point3d9;
                else:
                    point3d11 = point3d65;

            elif (not MathHelper.smethod_119(point3d9, point3d65, point3d67)):
                point3d9 = MathHelper.getIntersectionPoint(point3d86, point3d9, point3d65, point3d67)
                point3d11 = point3d9;
            else:
                point3d11 = point3d65;
            point3d13 = point3d64;
        else:
            if (MathHelper.smethod_115(point3d86, point3d64, point3d65)):
                point3d86 = MathHelper.getIntersectionPoint(position3, point3d86, point3d64, point3d65)
            point3d9 = point3d86;
            point3d11 = point3d86;
            point3d13 = point3d64;
        if (not point3d85.smethod_171(point3d8, 0.001) or not point3d86.smethod_171(point3d9, 0.001)):
            if (MathHelper.smethod_115(point3d86, point3d66, point3d78) or point3d85.smethod_171(point3d8, 0.001) or point3d86.smethod_171(point3d9, 0.001)):
                self.secondary.append(SecondaryObstacleArea(point3d85, point3d8, point3d86, point3d9, MathHelper.getBearing(point3d85, point3d8)))
            else:
                self.secondary.append(SecondaryObstacleArea(point3d85, point3d8, point3d86, point3d86, MathHelper.getBearing(point3d85, point3d8)));
                self.secondary.append(SecondaryObstacleArea(point3d8, point3d8, point3d86, point3d9, num5));

        if (not point3d8.smethod_171(point3d10, 0.001) or not point3d9.smethod_171(point3d11, 0.001)):
            self.secondary.append(SecondaryObstacleArea(point3d8, point3d10, point3d9, point3d11, num5))

        if (not point3d10.smethod_171(point3d12, 0.001) or not point3d11.smethod_171(point3d13, 0.001)):
            self.secondary.append(SecondaryObstacleArea(point3d10, point3d12, point3d11, point3d13, num5));

        self.secondary.append(SecondaryObstacleArea(position1, point3d70, position, point3d69, num1));
        self.secondary.append(SecondaryObstacleArea(point3d70, point3d14, point3d69, point3d75, num1));
        self.secondary.append(SecondaryObstacleArea(point3d14, point3d16, point3d75, point3d15, num1));
        self.secondary.append(SecondaryObstacleArea(point3d16, point3d76, point3d15, point3d77, num5));
        self.secondary.append(SecondaryObstacleArea(position2, point3d85, position3, point3d86, num1));
#         Point3dCollection point3dCollection2 = self.selectionArea;
        point3dArray = [point3d69, point3d75, point3d15, point3d77, point3d26, point3d18, point3d20, point3d22, point3d24, point3d25, point3d30, point3d12, point3d13, point3d11, point3d9, point3d86]
        self.selectionArea.extend(point3dArray)
#         self.selectionArea.smethod_146();
        point3dArray = [point3d70, point3d14, point3d16, point3d76, finish, point3d19, point3d21, point3d23, point3d25, point3d30, point3d12, point3d10, point3d8, point3d85]
        polylineArea4.method_7(point3dArray)
        if (not point3d76.smethod_171(finish, 0.001)):
            polylineArea4[polylineArea4.Count - 11].bulge = MathHelper.smethod_57(TurnDirection.Left, point3d76, finish, center);

        if (not finish.smethod_171(point3d19, 0.001)):
            polylineArea4[polylineArea4.Count - 10].bulge = MathHelper.smethod_57(TurnDirection.Left, finish, point3d19, center1);
        
        self.primary.append(PrimaryObstacleArea(polylineArea4))
        point3dArray = [point3d69, point3d75, point3d15, point3d77, point3d17, point3d18, point3d20, point3d22, point3d24]
        polylineArea.method_7(point3dArray);
        if (not point3d77.smethod_171(point3d17, 0.001)):
            polylineArea[polylineArea.Count - 6].bulge = MathHelper.smethod_57(TurnDirection.Left, point3d77, point3d17, center);
        
        if (not point3d17.smethod_171(point3d18, 0.001)):
            polylineArea[polylineArea.Count - 5].bulge = MathHelper.smethod_57(TurnDirection.Left, point3d17, point3d18, center1);
        
        point3dArray = [point3d70, point3d14, point3d16, point3d76, finish, point3d19, point3d21, point3d23, point3d25]
        polylineArea1.method_7(point3dArray);
        if (not point3d76.smethod_171(finish, 0.001)):
            polylineArea1[polylineArea1.Count - 6].bulge = MathHelper.smethod_57(TurnDirection.Left, point3d76, finish, center);
        
        if (not finish.smethod_171(point3d19, 0.001)):
            polylineArea1[polylineArea1.Count - 5].bulge = MathHelper.smethod_57(TurnDirection.Left, finish, point3d19, center1);
        
        point3dArray = [point3d85, point3d8, point3d10, point3d12]
        polylineArea3.method_7(point3dArray);
        point3dArray = [point3d86, point3d9, point3d11, point3d13]
        polylineArea2.method_7(point3dArray);
        self.drawingLines.append(polylineArea);
        self.drawingLines.append(polylineArea2);
        self.drawingLines.append(polylineArea1);
        self.drawingLines.append(polylineArea3);
        point3d91 = MathHelper.distanceBearingPoint(point3d29, num4, num12);
        point3d92 = MathHelper.distanceBearingPoint(point3d29, num5, num12);
        point3dArray = [point3d31, MathHelper.distanceBearingPoint(point3d29, num4, num12 + num), point3d91, point3d92, MathHelper.distanceBearingPoint(point3d29, num5, num12 + num)]
        self.nominalLine = PolylineArea(point3dArray);
        self.nominalLine[2].bulge = MathHelper.smethod_59(num1, point3d91, point3d92);
#         List<PolylineArea> polylineAreas2 = self.drawingLines;
        point3dArray = [point3d24, point3d25, point3d30, point3d12, point3d13]
        self.drawingLines.append(PolylineArea(point3dArray));
#         List<PolylineArea> polylineAreas3 = self.drawingLines;
        point3dArray = [point3d2, point3d3, point3d4, point3d5, point3d2]
        self.drawingLines.append(PolylineArea(point3dArray))
#         List<PolylineArea> polylineAreas4 = self.drawingLines;
        point3dArray = [point3d57, point3d58, point3d59, point3d60, point3d57]
        self.drawingLines.append(PolylineArea(point3dArray))

    def vmethod_4(self, gnssSegmentObstacles_0):
        gnssSegmentObstacles_0.method_16(self.initialOca);


class MissedApproachSegment(IGnssSegment):

    def __init__(self, position_0, position_1, position_2, rnavSpecification_0, 
                              aircraftSpeedCategory_0, altitude_0, double_0, speed_0, 
                              altitude_1, altitude_2, altitude_3, angleGradientSlope_0):
        position = []
        self.Type = RnavSegmentType.MissedApproach
        self.TOL5DEG = 0.0872664625997165

#             private Point3d ptMAWP;
        self.ptMAWP = None
#             private Point3d ptMAHWP;
        self.ptMAHWP = None
#             private Point3d ptSOC;
        self.ptSOC = None
#             private Point3d ptStart;
        self.ptStart = None
#             private double mocFA;
        self.mocFA = None
#             private double mocTurn;
        self.mocTurn = None
#             private double mat;
        self.mat = None
#             private double mat180;
        self.mat180 = None
#             private double matp90;
        self.matp90 = None
#             private double matm90;
        self.matm90 = None
#             private double macg;
        self.macg = None
#             private double dStartToSOC1;
        self.dStartToSOC1 = None
#             private double dStartToSOC;
        self.dStartToSOC = None
#             private double finalSegmentOca;
        self.finalSegmentOca = None
#             private double missedSegmentOca;
        self.missedSegmentOca = None
#             private BasicGnssApproachObstacleAnalyser.MissedApproachSegment.MissedApproachCritical finalCritical;
        self.finalCritical = None
#             private BasicGnssApproachObstacleAnalyser.MissedApproachSegment.MissedApproachCritical missedCritical;
        self.missedCritical = None
#             private List<Obstacle> turnObstacles;
        self.turnObstacles = []
        self.drawingLines = []
        self.primary = []
        self.secondary = []
        self.selectionArea = []
        
        self.ptMAWP = position_0
        self.ptMAHWP = position_1
        point3d8 = position_2
        self.primaryMoc = altitude_1.Metres
        self.mocFA = altitude_0.Metres
        self.mocTurn = altitude_2.Metres
        self.macg = angleGradientSlope_0.Percent
        self.mat = MathHelper.getBearing(self.ptMAWP, self.ptMAHWP)
        self.matp90 = MathHelper.smethod_4(self.mat + 1.5707963267949)
        self.matm90 = MathHelper.smethod_4(self.mat - 1.5707963267949)
        self.mat180 = MathHelper.smethod_4(self.mat + 3.14159265358979)
        num1 = Unit.ConvertDegToRad(15)
        num2 = Unit.ConvertNMToMeter(15)
        num3 = Unit.ConvertNMToMeter(30)
        if (MathHelper.calcDistance(point3d8, self.ptMAHWP) > num3 and rnavSpecification_0 == RnavSpecification.RnpApch):
            raise UserWarning, Messages.ERR_DISTANCE_BETWEEN_X_AND_ARP_EXCEEDS_RNP_SPEC%"Missed Approach Waypoint"
#                 self.waypoints.Add(new Symbol(SymbolType.Flyb));
#                 self.waypoints[0].Tag = self.ptMAHWP;
#                 if (!Geo.DatumLoaded)
#                 {
#                     Symbol item = self.waypoints[0];
#                     string[] rnavCommonWaypointMAHWP = new string[] { Enums.RnavCommonWaypoint_MAHWP };
#                     item.Attributes = new SymbolAttributes(rnavCommonWaypointMAHWP);
#                 }
#                 else
#                 {
#                     position_1.method_1(out degree, out degree1);
#                     Symbol symbolAttribute = self.waypoints[0];
#                     string[] strArrays = new string[] { Enums.RnavCommonWaypoint_MAHWP, degree.ToString(), degree1.ToString() };
#                     symbolAttribute.Attributes = new SymbolAttributes(strArrays);
#                 }
        polylineArea = PolylineArea()
        polylineArea1 = PolylineArea()
        polylineArea2 = PolylineArea()
        polylineArea3 = PolylineArea()
        polylineArea4 = PolylineArea()
        return2 = []
        MathHelper.smethod_34(self.ptMAWP, self.ptMAHWP, point3d8, num2, return2)#out point3d2, out point3d3);
        point3d2 = return2[0]
        point3d3 = return2[1]
        if not MathHelper.smethod_135(self.mat, MathHelper.getBearing(self.ptMAWP, point3d2), Unit.ConvertDegToRad(5), AngleUnits.Radians):
            point3d = point3d3 
        else:
            point3d = point3d2
        return2 = []
        MathHelper.smethod_34(self.ptMAWP, self.ptMAHWP, point3d8, num3, return2)#out point3d2, out point3d3);
        point3d2 = return2[0]
        point3d3 = return2[1]
        if not MathHelper.smethod_135(self.mat, MathHelper.getBearing(self.ptMAWP, point3d2), Unit.ConvertDegToRad(5), AngleUnits.Radians):
            point3d1 = point3d3 
        else:
            point3d1 = point3d2
        rnavGnssTolerance = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Mapt, aircraftSpeedCategory_0)
        metres = rnavGnssTolerance.getATTMetres()
        metres1 = rnavGnssTolerance.getASWMetres()
        metres2 = rnavGnssTolerance.getXTTMetres()
        rnavGnssTolerance = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Ma15, aircraftSpeedCategory_0)
        metres3 = rnavGnssTolerance.getATTMetres()
        metres4 = rnavGnssTolerance.getASWMetres()
        num4 = rnavGnssTolerance.getXTTMetres()
        point3d9 = MathHelper.distanceBearingPoint(self.ptMAWP, self.mat180, metres)
        point3d10 = MathHelper.distanceBearingPoint(point3d9, self.matm90, metres1);
        point3d11 = MathHelper.distanceBearingPoint(point3d9, self.matm90, metres1 / 2);
        point3d12 = MathHelper.distanceBearingPoint(point3d9, self.matp90, metres1 / 2);
        point3d13 = MathHelper.distanceBearingPoint(point3d9, self.matp90, metres1);
        speed = Speed.smethod_0(speed_0, double_0, altitude_3)
        speed1 = Speed(10, SpeedUnits.KTS)
        if aircraftSpeedCategory_0 != AircraftSpeedCategory.H:
            num = metres + (speed.MetresPerSecond + speed1.MetresPerSecond) * 18 
        else:
            num = metres + (speed.MetresPerSecond + speed1.MetresPerSecond * 8)
        self.ptSOC = MathHelper.distanceBearingPoint(self.ptMAWP, self.mat, num);
        self.ptStart = MathHelper.distanceBearingPoint(self.ptMAWP, self.mat180, metres);
        self.dStartToSOC = metres + num;
        self.dStartToSOC1 = max([0, self.dStartToSOC - (altitude_0.Metres - self.primaryMoc) / (angleGradientSlope_0.Percent / 100)])
        num5 = MathHelper.calcDistance(self.ptMAWP, self.ptMAHWP) + metres;
        num6 = (metres4 - metres1) / math.tan(num1)
        if (num5 > num6):
            num6 = (metres4 - metres1) / math.sin(num1)
            point3d4 = MathHelper.distanceBearingPoint(point3d10, self.mat - num1, num6);
            point3d5 = MathHelper.distanceBearingPoint(point3d4, self.matp90, metres4 / 2);
            point3d6 = MathHelper.distanceBearingPoint(point3d13, self.mat + num1, num6);
            point3d7 = MathHelper.distanceBearingPoint(point3d6, self.matm90, metres4 / 2);
            polylineArea.method_7([point3d10, point3d4])
            polylineArea1.method_7([point3d11, point3d5])
            polylineArea2.method_7([point3d13, point3d6])
            polylineArea3.method_7([point3d12, point3d7])
            num2 = MathHelper.calcDistance(self.ptMAWP, point3d) - metres3
            if (MathHelper.calcDistance(self.ptMAWP, self.ptMAHWP) > num2):
                metres = metres3;
                metres1 = metres4;
                rnavGnssTolerance = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.Star30Sid30IfIafMa30, aircraftSpeedCategory_0)
                metres3 = rnavGnssTolerance.getATTMetres()
                metres4 = rnavGnssTolerance.getASWMetres()
                num4 = rnavGnssTolerance.getXTTMetres()
                point3d9 = MathHelper.distanceBearingPoint(self.ptMAWP, self.mat, num2)
                point3d10 = MathHelper.distanceBearingPoint(point3d9, self.matm90, metres1)
                point3d11 = MathHelper.distanceBearingPoint(point3d9, self.matm90, metres1 / 2)
                point3d12 = MathHelper.distanceBearingPoint(point3d9, self.matp90, metres1 / 2)
                point3d13 = MathHelper.distanceBearingPoint(point3d9, self.matp90, metres1)
                num5 = MathHelper.calcDistance(self.ptMAWP, self.ptMAHWP)
                num6 = (metres4 - metres1) / math.tan(num1)
                if (num5 > num6 + num2):
                    num6 = (metres4 - metres1) / math.sin(num1)
                    point3d4 = MathHelper.distanceBearingPoint(point3d10, self.mat - num1, num6)
                    point3d5 = MathHelper.distanceBearingPoint(point3d4, self.matp90, metres4 / 2)
                    point3d6 = MathHelper.distanceBearingPoint(point3d13, self.mat + num1, num6)
                    point3d7 = MathHelper.distanceBearingPoint(point3d6, self.matm90, metres4 / 2)
                    position = [point3d10, point3d4]
                    polylineArea.method_7(position)
                    position = [point3d11, point3d5]
                    polylineArea1.method_7(position)
                    position = [point3d13, point3d6]
                    polylineArea2.method_7(position)
                    position = [point3d12, point3d7]
                    polylineArea3.method_7(position)
                    num3 = MathHelper.calcDistance(self.ptMAWP, point3d1) - metres3;
                    if (num5 > num3):
                        metres = metres3
                        metres1 = metres4
                        rnavGnssTolerance = RnavGnssTolerance(rnavSpecification_0, RnavGnssFlightPhase.StarSid, aircraftSpeedCategory_0)
                        metres3 = rnavGnssTolerance.getATTMetres()
                        metres4 = rnavGnssTolerance.getASWMetres()
                        num4 = rnavGnssTolerance.getXTTMetres()
                        point3d9 = MathHelper.distanceBearingPoint(self.ptMAWP, self.mat, num3)
                        point3d10 = MathHelper.distanceBearingPoint(point3d9, self.matm90, metres1)
                        point3d11 = MathHelper.distanceBearingPoint(point3d9, self.matm90, metres1 / 2)
                        point3d12 = MathHelper.distanceBearingPoint(point3d9, self.matp90, metres1 / 2)
                        point3d13 = MathHelper.distanceBearingPoint(point3d9, self.matp90, metres1)
                        num6 = (metres4 - metres1) / math.tan(num1)
                        if (num5 > num6 + num3):
                            num6 = (metres4 - metres1) / math.sin(num1)
                            point3d4 = MathHelper.distanceBearingPoint(point3d10, self.mat - num1, num6)
                            point3d5 = MathHelper.distanceBearingPoint(point3d4, self.matp90, metres4 / 2)
                            point3d6 = MathHelper.distanceBearingPoint(point3d13, self.mat + num1, num6)
                            point3d7 = MathHelper.distanceBearingPoint(point3d6, self.matm90, metres4 / 2)
                            position = [point3d10, point3d4]
                            polylineArea.method_7(position)
                            position = [point3d11, point3d5]
                            polylineArea1.method_7(position)
                            position = [point3d13, point3d6]
                            polylineArea2.method_7(position)
                            position = [point3d12, point3d7]
                            polylineArea3.method_7(position)
                            polylineArea.method_1(MathHelper.distanceBearingPoint(self.ptMAHWP, self.matm90, metres4))
                            polylineArea1.method_1(MathHelper.distanceBearingPoint(self.ptMAHWP, self.matm90, metres4 / 2))
                            polylineArea2.method_1(MathHelper.distanceBearingPoint(self.ptMAHWP, self.matp90, metres4))
                            polylineArea3.method_1(MathHelper.distanceBearingPoint(self.ptMAHWP, self.matp90, metres4 / 2))
                        else:
                            num6 = (num5 - num3) / math.cos(num1)
                            point3d4 = MathHelper.distanceBearingPoint(point3d10, self.mat - num1, num6)
                            point3d5 = MathHelper.distanceBearingPoint(point3d4, self.matp90, MathHelper.calcDistance(self.ptMAHWP, point3d4) / 2)
                            point3d6 = MathHelper.distanceBearingPoint(point3d13, self.mat + num1, num6)
                            point3d7 = MathHelper.distanceBearingPoint(point3d6, self.matm90, MathHelper.calcDistance(self.ptMAHWP, point3d6) / 2)
                            position = [point3d10, point3d4]
                            polylineArea.method_7(position)
                            position = [point3d11, point3d5]
                            polylineArea1.method_7(position)
                            position = [point3d13, point3d6]
                            polylineArea2.method_7(position)
                            position = [point3d12, point3d7]
                            polylineArea3.method_7(position)
                    else:
                        polylineArea.method_1(MathHelper.distanceBearingPoint(self.ptMAHWP, self.matm90, metres4))
                        polylineArea1.method_1(MathHelper.distanceBearingPoint(self.ptMAHWP, self.matm90, metres4 / 2))
                        polylineArea2.method_1(MathHelper.distanceBearingPoint(self.ptMAHWP, self.matp90, metres4))
                        polylineArea3.method_1(MathHelper.distanceBearingPoint(self.ptMAHWP, self.matp90, metres4 / 2))
                else:
                    num6 = (num5 - num2) / math.cos(num1)
                    point3d4 = MathHelper.distanceBearingPoint(point3d10, self.mat - num1, num6)
                    point3d5 = MathHelper.distanceBearingPoint(point3d4, self.matp90, MathHelper.calcDistance(self.ptMAHWP, point3d4) / 2)
                    point3d6 = MathHelper.distanceBearingPoint(point3d13, self.mat + num1, num6)
                    point3d7 = MathHelper.distanceBearingPoint(point3d6, self.matm90, MathHelper.calcDistance(self.ptMAHWP, point3d6) / 2)
                    position = [point3d10, point3d4]
                    polylineArea.method_7(position)
                    position = [point3d11, point3d5]
                    polylineArea1.method_7(position)
                    position = [point3d13, point3d6]
                    polylineArea2.method_7(position)
                    position = [point3d12, point3d7]
                    polylineArea3.method_7(position)
            else:
                polylineArea.method_1(MathHelper.distanceBearingPoint(self.ptMAHWP, self.matm90, metres4))
                polylineArea1.method_1(MathHelper.distanceBearingPoint(self.ptMAHWP, self.matm90, metres4 / 2))
                polylineArea2.method_1(MathHelper.distanceBearingPoint(self.ptMAHWP, self.matp90, metres4))
                polylineArea3.method_1(MathHelper.distanceBearingPoint(self.ptMAHWP, self.matp90, metres4 / 2))
        else:
            num6 = num5 / math.cos(num1)
            point3d4 = MathHelper.distanceBearingPoint(point3d10, self.mat - num1, num6)
            point3d5 = MathHelper.distanceBearingPoint(point3d4, self.matp90, MathHelper.calcDistance(self.ptMAHWP, point3d4) / 2)
            point3d6 = MathHelper.distanceBearingPoint(point3d13, self.mat + num1, num6)
            point3d7 = MathHelper.distanceBearingPoint(point3d6, self.matm90, MathHelper.calcDistance(self.ptMAHWP, point3d6) / 2)
            position = [point3d10, point3d4]
            polylineArea.method_7(position)
            polylineArea1.method_7([point3d11, point3d5])
            polylineArea2.method_7([point3d13, point3d6])
            polylineArea3.method_7([point3d12, point3d7])
        self.drawingLines.append(polylineArea)
        self.drawingLines.append(polylineArea2)
        self.drawingLines.append(polylineArea1)
        self.drawingLines.append(polylineArea3)
        position = [polylineArea[0].position, polylineArea2[0].position]
        self.drawingLines.append(PolylineArea(position))
        position = [polylineArea[polylineArea.Count - 1].position, polylineArea2[polylineArea2.Count - 1].position]
        self.drawingLines.append(PolylineArea(position))
        position = [self.ptMAWP, self.ptMAHWP]
        self.nominalLine = PolylineArea(position)
        point3d14 = MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(self.ptMAHWP, self.mat, metres3), self.matm90, num4);
        point3d15 = MathHelper.distanceBearingPoint(point3d14, self.mat180, metres3 * 2);
        point3d16 = MathHelper.distanceBearingPoint(point3d15, self.matp90, num4 * 2);
        point3d17 = MathHelper.distanceBearingPoint(point3d16, self.mat, metres3 * 2);
        
        position = [point3d14, point3d15, point3d16, point3d17, point3d14]
        self.drawingLines.append(PolylineArea(position))
        count = polylineArea.Count
        i = 0
        while i < count:#i++)
            self.selectionArea.append(polylineArea[i].position)
            polylineArea4.method_1(polylineArea1[i].position)
            i += 1
        j = count - 1
        while j >= 0: # j--)
            self.selectionArea.append(polylineArea2[j].position)
            polylineArea4.method_1(polylineArea3[j].position)
            j -= 1
        self.primary.append(PrimaryObstacleArea(polylineArea4))
        k = 1
        while k < polylineArea.Count: #; k++)
            self.secondary.append(SecondaryObstacleArea(polylineArea1[k - 1].position, polylineArea1[k].position, polylineArea[k - 1].position, polylineArea[k].position, self.mat))
            self.secondary.append(SecondaryObstacleArea(polylineArea3[k - 1].position, polylineArea3[k].position, polylineArea2[k - 1].position, polylineArea2[k].position, self.mat))
            k += 1
        
    def SOC(self):
        return self.ptSOC.smethod_167(0)

    def StartOfFinalMA(self):
        num = self.dStartToSOC;
        for turnObstacle in self.turnObstacles:
            point3d = MathHelper.getIntersectionPoint(self.ptMAWP, self.ptMAHWP, turnObstacle.position, MathHelper.distanceBearingPoint(turnObstacle.position, self.matp90, 100))
            point3d1 = MathHelper.distanceBearingPoint(point3d, self.mat180, turnObstacle.tolerance)
            num1 = MathHelper.getBearing(self.ptStart, point3d1)
            num2 = 0
            if (MathHelper.smethod_135(num1, self.mat, 0.0872664625997165, AngleUnits.Radians)):
                num2 = MathHelper.calcDistance(self.ptStart, point3d1);
            if (num2 <= self.dStartToSOC):
                continue;
            tag = turnObstacle.tag
            num3 = tag * (self.mocTurn / self.primaryMoc)
            if (turnObstacle.position.z() + turnObstacle.trees + num3 - (num2 - self.dStartToSOC) * (self.macg / 100) <= self.missedSegmentOca):
                continue
            num = max([num, num2 + turnObstacle.tolerance * 2])
        return MathHelper.distanceBearingPoint(self.ptStart, self.mat, num).smethod_167(0);

    def vmethod_0(self, obstacle_0):
        if define._units == QGis.Meters: 
            obstPosition = obstacle_0.position
        else:
            obstPosition = obstacle_0.positionDegree           
        if (MathHelper.pointInPolygon(self.selectionArea, obstPosition, obstacle_0.tolerance)):
            obstacleAreaResult = ObstacleAreaResult.Outside
            mocMultiplier = self.primaryMoc * obstacle_0.mocMultiplier
#             gnssSegmentObstacles0.ObstaclesChecked = gnssSegmentObstacles0.ObstaclesChecked + 1
            for current in self.primary:
                return2 = []
                obstacleAreaResult = current.imethod_1(obstPosition, obstacle_0.tolerance, mocMultiplier, return2) # out num2, out num3);

                if obstacleAreaResult == ObstacleAreaResult.Primary:
                    num2 = return2[0]
                    num3 = return2[1]
                    break
            if (obstacleAreaResult != ObstacleAreaResult.Primary):
                num2 = None
                num3 = None
                obstacleAreaResult = ObstacleAreaResult.Outside
                for secondaryObstacleArea in self.secondary:
                    return2 = []
                    obstacleAreaResult1 = secondaryObstacleArea.imethod_1(obstPosition, obstacle_0.tolerance, mocMultiplier, return2) #out num, out num1);
                    if (obstacleAreaResult1 != ObstacleAreaResult.Outside):
                        if len(return2) < 2:
                            return None
                        num = return2[0]
                        num1 = return2[1]
                        if (num > num2 or num2 == None):
                            num2 = num
                            num3 = num1
                            obstacleAreaResult = obstacleAreaResult1
                        if (obstacleAreaResult1 == ObstacleAreaResult.Primary):
                            num2 = num
                            num3 = None
                            obstacleAreaResult = ObstacleAreaResult.Primary
                            break
            if (obstacleAreaResult != ObstacleAreaResult.Outside):
                point3d = MathHelper.getIntersectionPoint(self.ptMAWP, self.ptMAHWP, obstPosition, MathHelper.distanceBearingPoint(obstPosition, self.matp90, 100))
                point3d1 = MathHelper.distanceBearingPoint(point3d, self.mat180, obstacle_0.tolerance)
                num4 = MathHelper.getBearing(self.ptStart, point3d1)
                num5 = 0
                if (MathHelper.smethod_135(num4, self.mat, 0.0872664625997165, AngleUnits.Radians)):
                    num5 = MathHelper.calcDistance(self.ptStart, point3d1)
                if (num5 <= self.dStartToSOC):
                    if num5 > self.dStartToSOC1:
                        num2 = num2 * ((self.primaryMoc + (self.dStartToSOC - num5) * (self.macg / 100)) / self.primaryMoc) 
                    else:
                        num2 = num2 * (self.mocFA / self.primaryMoc)
                        
                    position = obstPosition
                    z = position.z() + obstacle_0.trees + num2
                    if self.finalSegmentOca != None and self.finalSegmentOca > z:
#                         gnssSegmentObstacles_0.method_12(obstacle_0, obstacleAreaResult, num3, None, num2, z, CriticalObstacleType.No)
                        return [obstacleAreaResult, num3, None, num2, z, CriticalObstacleType.No, self.Type]
                    else:
                        self.finalSegmentOca = z
#                         if (self.finalCritical != None):
    #                         gnssSegmentObstacles_0.method_12(self.finalCritical.Obstacle, self.finalCritical.Area, self.finalCritical.DistIn, self.finalCritical.DistTo, self.finalCritical.Moc, self.finalCritical.Oca, CriticalObstacleType.No)
                        self.finalCritical = MissedApproachCritical(obstacle_0, obstacleAreaResult, num2, num3, None, z)
                        return [obstacleAreaResult, num3, None, num2, z, CriticalObstacleType.No, self.Type]
                position1 = obstPosition
                z = position1.z() + obstacle_0.trees + num2 - (num5 - self.dStartToSOC) * (self.macg / 100)
                if (self.missedSegmentOca == None or self.missedSegmentOca <= z):
                    self.missedSegmentOca = z
#                     if (self.missedCritical != None):
#                         gnssSegmentObstacles_0.method_12(self.missedCritical.Obstacle, self.missedCritical.Area, self.missedCritical.DistIn, self.missedCritical.DistTo, self.missedCritical.Moc, self.missedCritical.Oca, CriticalObstacleType.No);
                    self.missedCritical = MissedApproachCritical(obstacle_0, obstacleAreaResult, num2, num3, num5 - self.dStartToSOC, z);
#                     gnssSegmentObstacles_0.method_12(obstacle_0, obstacleAreaResult, num3, num5 - self.dStartToSOC, num2, z, CriticalObstacleType.No);
                obstacle_0.tag = num2
                self.turnObstacles.append(obstacle_0)
                return [obstacleAreaResult, num3, num5 - self.dStartToSOC, num2, z, CriticalObstacleType.No, self.Type]
        return None

    def vmethod_4(self, gnssSegmentObstacles_0):
        if (self.missedCritical != None):
            gnssSegmentObstacles_0.method_12(self.missedCritical.Obstacle, self.missedCritical.Area, self.missedCritical.DistIn, self.missedCritical.DistTo, self.missedCritical.Moc, self.missedCritical.Oca, CriticalObstacleType.Yes)
        if (self.finalCritical != None):
            gnssSegmentObstacles_0.method_12(self.finalCritical.Obstacle, self.finalCritical.Area, self.finalCritical.DistIn, self.finalCritical.DistTo, self.finalCritical.Moc, self.finalCritical.Oca, CriticalObstacleType.Yes)

class MissedApproachCritical:
    def __init__(self, obstacle_0, obstacleAreaResult_0, moc, distIn, distTo, oca):
        self.Obstacle = obstacle_0
        self.Area = obstacleAreaResult_0
        self.Moc = moc
        self.DistIn = distIn
        self.DistTo = distTo
        self.Oca = oca
