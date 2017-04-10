'''
Created on Feb 23, 2015

@author: Administrator
'''

from FlightPlanner.helpers import MathHelper, Distance, Unit
from FlightPlanner.types import TurnDirection, AngleUnits, Point3D
from qgis.core import QgsGeometry, QgsFeature, QgsPoint
from FlightPlanner.polylineArea import PolylineArea
import math

class WindSpiral:

    def __init__(self, point3d_0, double_0, speed_0, speed_1, double_1, turnDirection_0):
        ### point3d_0 : start point
        ### double_0  is  inboundTrack angle(radian).
        ### speed_0 is speed of airplane(TAS).
        ### speed_1 is speed of wind.
        ### double_1  is  value of bank anlge(float).
        self.Start = [Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 0.0)]
        self.Middle = [Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 0.0)]
        self.Finish = [Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 0.0)]
        self.Center = [Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 0.0)]
        self.Radius = [Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 0.0), Point3D(0.0, 0.0, 0.0)]
        self.Direction = turnDirection_0
        return1 = []
        distance = Distance.smethod_1(speed_0, double_1, return1) # out num)
        num = return1[0]
        metres = distance.Metres
        metresPerSecond = 45 / num * speed_1.MetresPerSecond
        metresPerSecond1 = 90 / num * speed_1.MetresPerSecond
        metresPerSecond2 = 135 / num * speed_1.MetresPerSecond
        num2 = 180 / num * speed_1.MetresPerSecond
        metresPerSecond3 = 225 / num * speed_1.MetresPerSecond
        num3 = 270 / num * speed_1.MetresPerSecond
        if turnDirection_0 != TurnDirection.Left:
            num1 = 1 
        else:
            num1 = -1
        point3d = MathHelper.distanceBearingPoint(point3d_0, num1 * math.pi / 2 + double_0, metres)
        self.Start[0] = point3d_0
        self.Middle[0] = MathHelper.distanceBearingPoint(point3d, -1 * num1 * (math.pi / 4) + double_0, metres + metresPerSecond)
        self.Finish[0] = MathHelper.distanceBearingPoint(point3d, double_0, metres + metresPerSecond1)
        self.Start[1] = self.Finish[0]
        self.Middle[1] = MathHelper.distanceBearingPoint(point3d, num1 * (math.pi / 4) + double_0, metres + metresPerSecond2)
        self.Finish[1] = MathHelper.distanceBearingPoint(point3d, num1 * math.pi / 2 + double_0, metres + num2)
        self.Start[2] = self.Finish[1]
        self.Middle[2] = MathHelper.distanceBearingPoint(point3d, num1 * (math.pi / 4) * 3 + double_0, metres + metresPerSecond3)
        self.Finish[2] = MathHelper.distanceBearingPoint(point3d, num1 * math.pi + double_0, metres + num3)
        self.Center[0] = MathHelper.smethod_68(self.Start[0], self.Middle[0], self.Finish[0])
        self.Center[1] = MathHelper.smethod_68(self.Start[1], self.Middle[1], self.Finish[1])
        self.Center[2] = MathHelper.smethod_68(self.Start[2], self.Middle[2], self.Finish[2])
        self.Radius[0] = MathHelper.calcDistance(self.Center[0], self.Middle[0])
        self.Radius[1] = MathHelper.calcDistance(self.Center[1], self.Middle[1])
        self.Radius[2] = MathHelper.calcDistance(self.Center[2], self.Middle[2])

    def getBearingOfTangentWithOutPt(self, outPt, spiralNumber, turnDirection = None):
        if self.Direction == TurnDirection.Right:
            B = math.asin(self.Radius[spiralNumber] / MathHelper.calcDistance(self.Center[spiralNumber], outPt))
            return MathHelper.smethod_4(MathHelper.getBearing(self.Center[spiralNumber], outPt) + B)
        else:
            B = math.asin(self.Radius[spiralNumber] / MathHelper.calcDistance(self.Center[spiralNumber], outPt))
            return MathHelper.smethod_4(MathHelper.getBearing(self.Center[spiralNumber], outPt) - B)
    def getContactWithBearingOfTangent(self, bearingOfContact, spiralNumber = None, turnDirection = None):
        if spiralNumber == None:
            contactPt = self.method_0(bearingOfContact, AngleUnits.Radians)
            if round(self.Radius[0], 2) == round(MathHelper.calcDistance(self.Center[0], contactPt), 2):
                centerPt = self.Center[0]
                spiralNumber = 0
            elif round(self.Radius[1], 2) == round(MathHelper.calcDistance(self.Center[1], contactPt), 2):
                centerPt = self.Center[1]
                spiralNumber = 1
            else:
                centerPt = self.Center[2]
                spiralNumber = 2
            bearing = MathHelper.getBearing(centerPt, contactPt)
            if self.Direction == TurnDirection.Right:
                leftMiddlePt = MathHelper.distanceBearingPoint(centerPt, MathHelper.smethod_4(bearing - 0.01), self.Radius[spiralNumber])
                rightMiddlePt = MathHelper.distanceBearingPoint(centerPt, MathHelper.smethod_4(bearing + 0.01), self.Radius[spiralNumber])
                return leftMiddlePt, contactPt, rightMiddlePt
            else:
                rightMiddlePt = MathHelper.distanceBearingPoint(centerPt, MathHelper.smethod_4(bearing + 0.01), self.Radius[spiralNumber])
                leftMiddlePt = MathHelper.distanceBearingPoint(centerPt, MathHelper.smethod_4(bearing - 0.01), self.Radius[spiralNumber])
                return leftMiddlePt, contactPt, rightMiddlePt

        if self.Direction == TurnDirection.Right:
            bearing = MathHelper.smethod_4(bearingOfContact - math.pi /2)
            contactPt = MathHelper.distanceBearingPoint(self.Center[spiralNumber], bearing, self.Radius[spiralNumber])
            leftMiddlePt = MathHelper.distanceBearingPoint(self.Center[spiralNumber], MathHelper.smethod_4(bearing - 0.01), self.Radius[spiralNumber])
            rightMiddlePt = MathHelper.distanceBearingPoint(self.Center[spiralNumber], MathHelper.smethod_4(bearing + 0.01), self.Radius[spiralNumber])

            return leftMiddlePt, contactPt, rightMiddlePt
        else:
            bearing = MathHelper.smethod_4(bearingOfContact + math.pi /2)
            contactPt = MathHelper.distanceBearingPoint(self.Center[spiralNumber], bearing, self.Radius[spiralNumber])
            rightMiddlePt = MathHelper.distanceBearingPoint(self.Center[spiralNumber], MathHelper.smethod_4(bearing + 0.01), self.Radius[spiralNumber])
            leftMiddlePt = MathHelper.distanceBearingPoint(self.Center[spiralNumber], MathHelper.smethod_4(bearing - 0.01), self.Radius[spiralNumber])
            return leftMiddlePt, contactPt, rightMiddlePt

    def getContact(self, point3d, radBetweenTangentAndPoint = None, spiralNumber = None, turnDirection = None):
        a = MathHelper.calcDistance(point3d, self.Center[spiralNumber])
        b = MathHelper.calcDistance(self.Center[spiralNumber], self.Finish[spiralNumber])
        A = math.pi / 2 - radBetweenTangentAndPoint
        B = math.asin(math.sin(A) * b / a)
        C = math.pi - A - B
        bearing = 0.0
        middlePt = Point3D()
        if self.Direction == TurnDirection.Right:
            bearing = MathHelper.smethod_4(MathHelper.getBearing(self.Center[spiralNumber], point3d) - C)
            middlePt = MathHelper.distanceBearingPoint(self.Center[spiralNumber], MathHelper.smethod_4(bearing - 0.001), self.Radius[spiralNumber])
        elif self.Direction == TurnDirection.Left:
            bearing = MathHelper.smethod_4(MathHelper.getBearing(self.Center[spiralNumber], point3d) + C)
            middlePt = MathHelper.distanceBearingPoint(self.Center[spiralNumber], MathHelper.smethod_4(bearing + 0.001), self.Radius[spiralNumber])
        return middlePt, MathHelper.distanceBearingPoint(self.Center[spiralNumber], bearing, self.Radius[0])

    def getIntersectPolylineArea(self, angle, angleUnits_0):
        point3dArray = [self.Start[0], self.Start[1], self.Start[2], self.Finish[2]]
        polyline = PolylineArea(point3dArray)
        polyline.SetBulgeAt(0, MathHelper.smethod_60(self.Start[0], self.Middle[0], self.Finish[0]))
        polyline.SetBulgeAt(1, MathHelper.smethod_60(self.Start[1], self.Middle[1], self.Finish[1]))
        polyline.SetBulgeAt(2, MathHelper.smethod_60(self.Start[2], self.Middle[2], self.Finish[2]))

        intersectPt = self.method_0(angle, angleUnits_0)
        if intersectPt == None:
            return None, None
        polylineArea = None
        if round(self.Radius[0]) == round(MathHelper.calcDistance(self.Center[0], intersectPt)):
            point3dArray = [self.Start[0], intersectPt]
            polylineArea = PolylineArea(point3dArray)
            polylineArea.SetBulgeAt(0, MathHelper.smethod_60(self.Start[0], self.Middle[0], self.Finish[0]))
        elif round(self.Radius[1]) == round(MathHelper.calcDistance(self.Center[1], intersectPt)):
            point3dArray = [self.Start[0], self.Start[1], intersectPt]
            polylineArea = PolylineArea(point3dArray)
            polylineArea.SetBulgeAt(0, MathHelper.smethod_60(self.Start[0], self.Middle[0], self.Finish[0]))
            polylineArea.SetBulgeAt(1, MathHelper.smethod_60(self.Start[1], self.Middle[1], self.Finish[1]))
        else:
            point3dArray = [self.Start[0], self.Start[1], self.Start[2], intersectPt]
            polylineArea = PolylineArea(point3dArray)
            polylineArea.SetBulgeAt(0, MathHelper.smethod_60(self.Start[0], self.Middle[0], self.Finish[0]))
            polylineArea.SetBulgeAt(1, MathHelper.smethod_60(self.Start[1], self.Middle[1], self.Finish[1]))
            polylineArea.SetBulgeAt(2, MathHelper.smethod_60(self.Start[2], self.Middle[2], self.Finish[2]))
        return intersectPt, polylineArea

    def method_0(self, double_0, angleUnits_0):
        if (angleUnits_0 == AngleUnits.Degrees):
            double_0 = Unit.ConvertDegToRad(double_0)
        if self.Direction != TurnDirection.Left:
            num = double_0 - math.pi / 2
        else:
            num = double_0 + math.pi / 2
            
        point3d = MathHelper.distanceBearingPoint(self.Center[0], num, self.Radius[0])
        point3d1 = MathHelper.distanceBearingPoint(self.Center[1], num, self.Radius[1])
        point3d2 = MathHelper.distanceBearingPoint(self.Center[2], num, self.Radius[2])
        if (self.Direction == TurnDirection.Left):
            if (MathHelper.smethod_115(point3d1, point3d, MathHelper.distanceBearingPoint(point3d, double_0, 1000)) or MathHelper.smethod_119(point3d1, self.Center[0], self.Finish[0])):
                return point3d
            if (not MathHelper.smethod_115(point3d2, point3d1, MathHelper.distanceBearingPoint(point3d1, double_0, 1000))) and (not MathHelper.smethod_119(point3d2, self.Center[1], self.Finish[1])):
                return point3d2
            return point3d1
        if (MathHelper.smethod_119(point3d1, point3d, MathHelper.distanceBearingPoint(point3d, double_0, 1000)) or MathHelper.smethod_115(point3d1, self.Center[0], self.Finish[0])):
            return point3d
        if (not MathHelper.smethod_119(point3d2, point3d1, MathHelper.distanceBearingPoint(point3d1, double_0, 1000))) and (not MathHelper.smethod_115(point3d2, self.Center[1], self.Finish[1])):
            return point3d2
        return point3d1

    def method_1(self, point3d_0, point3d_1, bool_0):
        obj = self.Object
        line = QgsGeometry.fromPolyline([point3d_0, point3d_1])
        lineBound = None

        if point3d_0.get_X() == point3d_1.get_X() or point3d_0.get_Y() == point3d_1.get_Y():
            lineBound = QgsGeometry.fromPolyline([point3d_0, point3d_1])
        else:
            point0 = QgsPoint(point3d_0.get_X(), point3d_1.get_Y())
            point1 = QgsPoint(point3d_1.get_X(), point3d_0.get_Y())
            lineBound = QgsGeometry.fromPolyline([point3d_0, point0, point3d_1, point1, point3d_0])
        flag = obj.intersects(line) if (not bool_0) else obj.intersects(lineBound) #? obj.IntersectWith(line, 0, point3dCollection) > 0 : obj.IntersectWith(line, 2, point3dCollection) > 0)
        return flag

    def get_Object(self):
        point3dArray = [self.Start[0], self.Start[1], self.Start[2], self.Finish[2]]
        polyline = PolylineArea(point3dArray)
        polyline.SetBulgeAt(0, MathHelper.smethod_60(self.Start[0], self.Middle[0], self.Finish[0]))
        polyline.SetBulgeAt(1, MathHelper.smethod_60(self.Start[1], self.Middle[1], self.Finish[1]))
        polyline.SetBulgeAt(2, MathHelper.smethod_60(self.Start[2], self.Middle[2], self.Finish[2]))
        return QgsGeometry.fromPolyline(polyline.method_14())
    Object = property(get_Object, None, None, None)