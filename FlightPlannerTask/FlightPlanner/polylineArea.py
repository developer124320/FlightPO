'''
Created on Feb 21, 2015

@author: Administrator
'''
from FlightPlanner.helpers import MathHelper, Unit
from FlightPlanner.messages import Messages
from FlightPlanner.types import TurnDirection, Point3D, AngleUnits, Point3dCollection
# from FlightPlanner.Polyline import Polyline
from FlightPlanner.QgisHelper import QgisHelper
from qgis.core import QgsGeometry

import numpy, math
class PolylineAreaPoint:
    def __init__(self, point3d_0 = None, bulge = 0.0):
#         private Point3d position;
        if not isinstance(point3d_0, Point3D):
            point3d_0 = Point3D(point3d_0.x(), point3d_0.y())
        self.position = point3d_0
#         private double bulge;
        self.bulge = bulge
        
    def get_Position(self):
        return self.position
    
    def set_Position(self, value):
        self.position = value
        
    def get_Bulge(self):
        return self.bulge
    
    def set_Bulge(self, value):
        self.bulge = value
        
    Position = property(get_Position, set_Position, None, None)
    Bulge = property(get_Bulge, set_Bulge, None, None)

class PolylineArea(list) :
    def __init__(self, point3dCollection_0 = None, point3d_0 = None, double_0 = 0.0):
        
        if point3d_0 != None:
            self.isCircle = True
            list.__init__(self,[PolylineAreaPoint(point3d_0, double_0)])
        else:
            self.isCircle = False
            if point3dCollection_0 != None:
                for point3d in point3dCollection_0:
                    self.append(PolylineAreaPoint(point3d))
                return
            list.__init__(self)

    def IntersectWithNew(self, other, tolerance = 0.0, result = []):
        # result = []
        minePointList = self.getQgsPointList()
        otherPointList = other.getQgsPointList()

        for i in range(1, len(minePointList)):
            mineGeom = QgsGeometry.fromPolyline([minePointList[i - 1], minePointList[i]])
            for j in range(1, len(otherPointList)):
                otherGeom = QgsGeometry.fromPolyline([otherPointList[j - 1], otherPointList[j]])
                if mineGeom.intersects(otherGeom):
                    intersectGeom = mineGeom.intersection(otherGeom)
                    pt = intersectGeom.asPoint()
                    if pt.x() != 0 and pt.y() != 0:
                        result.append(Point3D(pt.x(), pt.y()))
                elif mineGeom.touches(otherGeom):
                    pass

        return len(result) > 0, result

    def IntersectWith(self, other, tolerance, result):
        minePointList = self.getQgsPointList()
        otherPointList = other.getQgsPointList()
        mineGeom = QgsGeometry.fromPolyline(minePointList)
        otherGeom = QgsGeometry.fromPolyline(otherPointList)
        intersectGeom = mineGeom.intersection(otherGeom)
        if intersectGeom != None:
            if len(intersectGeom.asPolyline()) > 0:
                for pt in intersectGeom.asPolyline():
                    result.append(pt)
                return True
            qgsPoint = intersectGeom.asPoint()
            result.append(qgsPoint)
            return True
        else:
            return False
    def Add(self, polylineAreaPoint):
        self.append(polylineAreaPoint)
        
    def CenterPoint(self):
        if len(self) > 0:
            return self[0].Position
        else:
            return None

    def GetPoint3dAt(self, index):
        return self[index].Position

    def Direction(self):
        point3dCollection = []
        count = len(self)
        i = 0
        while i < count:
            position = self[i].position
            bulge = self[i].Bulge
            if i != count - 1:
                point3d = self[i + 1].position
            else:
                point3d = self[0].position
            if (not position.smethod_170(point3d)):
                point3dCollection.append(position)
                if (not MathHelper.smethod_96(bulge)):
#                     if int(position.get_X()) == 688211:
#                         nn= 1
                    point3d1 = MathHelper.smethod_71(position, point3d, bulge)
#                     if point3d1 == None:
#                         nn = 0
                    num1 = MathHelper.smethod_5(bulge) / 2
                    if MathHelper.smethod_66(bulge) != TurnDirection.Left:
                        num = MathHelper.getBearing(point3d1, position) + num1 
                    else:
                        num = MathHelper.getBearing(point3d1, position) - num1
                    point3dCollection.append(MathHelper.distanceBearingPoint(point3d1, num, MathHelper.calcDistance(point3d1, position)));
            i += 1
        return MathHelper.smethod_65(point3dCollection);

    def Radius(self):
        return self[0].Bulge

    def offsetCurve(self, distance, segment = 0, joinStyle = 0, mitreLimit = 0):
        pointList = self.method_14_closed()
        pointList.append(self[1].Position)
        polyline = QgisHelper.offsetCurve(pointList, distance)
        self.clear()
        self.method_5(polyline)
        
    def getOffsetCurve(self, distance, level = 8):  ###### case in closed
        polylineAreaList = []
        startPointIndex = 0
        for i in range(len(self)):
            if i == len(self) - 1:
                if self[i].bulge != 0:
                    temp = PolylineArea()
                    temp.Add(PolylineAreaPoint(self[i].Position, self[i].bulge))
                    temp.Add(PolylineAreaPoint(self[0].Position))
                    polylineAreaList.append(temp)
                else:
                    point3dArray = []
                    for j in range(startPointIndex, i + 1):
                        point3dArray.append(self[j].Position)
                    point3dArray.append(self[0].Position)
                    polylineAreaList.append(PolylineArea(point3dArray))
            elif self[i].bulge != 0:
                if startPointIndex != i:
                    point3dArray = []
                    for j in range(startPointIndex, i + 1):
                        point3dArray.append(self[j].Position)
                    polylineAreaList.append(PolylineArea(point3dArray))

                temp = PolylineArea()
                temp.Add(PolylineAreaPoint(self[i].Position, self[i].bulge))
                temp.Add(PolylineAreaPoint(self[i + 1].Position))
                polylineAreaList.append(temp)

                startPointIndex = i + 1


        pointList = self.method_14_closed(level)
#         pointList.append(self[1].Position)
        polyline = QgisHelper.offsetCurve(pointList, distance)
        polylineAreaNew = PolylineArea()
        polylineAreaNew.method_5(polyline)
        return polylineAreaNew
    def getOffsetCurveNo(self, distance, level = 8):
        pointList = self.method_14(level)
#         pointList.append(self[1].Position)
        polyline = QgisHelper.offsetCurve(pointList, distance)
        polylineAreaNew = PolylineArea()
        polylineAreaNew.method_5(polyline)
        return polylineAreaNew
    def getOffsetCurveNoClosed(self, distance, segment = 0, joinStyle = 0, mitreLimit = 0):
        pointList = []
        count = len(self)
        i = 0
        radiusDifference = 0
        for item in self:
            i += 1
            if i == 1:
                bearing = MathHelper.getBearing(self[i-1].Position, self[i].Position)
                point = MathHelper.distanceBearingPoint(self[i - 1].Position, bearing - Unit.ConvertDegToRad(90) , distance)
                pointList.append(point)

                # if self[i-1].Bulge != 0:
                #     radiusDifference = distance if distance >= 0 else distance * (-1)
            elif i == count:
                bearing = MathHelper.getBearing(self[i-1].Position, self[i - 2].Position)
                point = MathHelper.distanceBearingPoint(self[i-1].Position, bearing + Unit.ConvertDegToRad(90) , distance)

                line = QgsGeometry.fromPolyline([self[i-1].Position, self[i - 2].Position])
                newLine = QgsGeometry.fromPolyline([pointList[i-2], point])
                if line.intersects(newLine):
                    bearing = MathHelper.getBearing(self[i-1].Position, self[i - 2].Position)
                    point = MathHelper.distanceBearingPoint(self[i-1].Position, bearing + Unit.ConvertDegToRad(270) , distance)

                pointList.append(point)
            else:
                turnDirection = MathHelper.smethod_65([self[i-2].Position, self[i-1].Position, self[i].Position])
                angle = 0
                if turnDirection == TurnDirection.Right:
                    angle = Unit.ConvertDegToRad(360) - math.fabs(MathHelper.getBearing(self[i-1].Position, self[i].Position) - MathHelper.getBearing(self[i-1].Position, self[i-2].Position))
                else:
                    angle =  math.fabs(MathHelper.getBearing(self[i-1].Position, self[i].Position) - MathHelper.getBearing(self[i-1].Position, self[i-2].Position))

                angle = math.fabs(Unit.ConvertDegToRad(90) - angle / 2)
                dist = distance / math.cos(angle)
                angle = (MathHelper.getBearing(self[i-1].Position, self[i].Position) + MathHelper.getBearing(self[i-1].Position, self[i-2].Position)) / 2
                point = MathHelper.distanceBearingPoint(self[i-1].Position, angle , dist)

                line = QgsGeometry.fromPolyline([self[i-1].Position, self[i - 2].Position])
                newLine = QgsGeometry.fromPolyline([pointList[i-2], point])
                if line.intersects(newLine):
                    bearing = MathHelper.getBearing(self[i-1].Position, self[i - 2].Position)
                    point = MathHelper.distanceBearingPoint(self[i-1].Position, angle + Unit.ConvertDegToRad(180) , dist)
                if self[i-1].Bulge != 0:
                    radiusDifference = dist if dist >= 0 else dist * (-1)
                pointList.append(point)
        polylineAreaNew = PolylineArea()
        for i in range(count):
            polylineAreaNew.Add(PolylineAreaPoint(pointList[i], self[i].Bulge))
        return polylineAreaNew
    def getPointWithShortestDist(self, point3d, closed = True):
        if self.Count == 0:
            return None
        if closed:
            point3dList = self.method_14_closed()
        else:
            point3dList = self.method_14()
        # i = 0
        # for point3d0 in point3dList:
        #     if i == 0:
        #         i += 1
        #         continue
        #     previousPoint = point3dList[i - 1]
        #     currentPoint = point3d0
        #     f = QgsGeometry.fromPolyline([previousPoint, currentPoint]).contains(point3d)
        #     if f:
        #         return point3d
        i = 0
        for point3d0 in point3dList:
            if i == 0:
                i += 1
                continue
            previousPoint = point3dList[i - 1]
            currentPoint = point3d0
            f = QgsGeometry.fromPolyline([previousPoint, currentPoint]).contains(point3d)
            dist = MathHelper.calcDistance(point3d, previousPoint)
            bearing = MathHelper.smethod_4(MathHelper.getBearing(previousPoint, currentPoint) - math.pi / 2)
            vPoint1 = MathHelper.distanceBearingPoint(point3d, bearing, dist)
            bearing = MathHelper.smethod_4(MathHelper.getBearing(previousPoint, currentPoint) + math.pi / 2)
            dist = MathHelper.calcDistance(point3d, previousPoint)
            vPoint2 = MathHelper.distanceBearingPoint(point3d, bearing, dist)
            geom = QgsGeometry.fromPolyline([previousPoint, currentPoint]).intersection(QgsGeometry.fromPolyline([vPoint1, vPoint2]))
            intersectionPoint = geom.asPoint()
            if intersectionPoint.x() == 0 and intersectionPoint.y() == 0:
                i += 1
                continue
            pt = None
            if point3d.x() > intersectionPoint.x():
                pt = Point3D(intersectionPoint.x() + 1, intersectionPoint.y())
            else:
                pt = Point3D(intersectionPoint.x() - 1, intersectionPoint.y())
            geom = QgsGeometry.fromPolyline(point3dList).intersection(QgsGeometry.fromPolyline([point3d, pt]))
            intersectionPoint1 = geom.asPoint()
            if intersectionPoint1.x() != 0 and intersectionPoint1.y() != 0:
                i += 1
                continue
            return Point3D(intersectionPoint.x(), intersectionPoint.y())
        return self.getClosestPointTo(point3d, False)


    def getClosestPointTo(self, point, bExtend):
        if not bExtend:
            closestPoint = self[0].Position
            for polylineAreaPoint in self:
                if MathHelper.calcDistance(point, polylineAreaPoint.Position) < MathHelper.calcDistance(closestPoint, point):
                    closestPoint = polylineAreaPoint.Position
            return closestPoint

        pointList = self.getQgsPointList()
        minDistance = 9.0E+9
        index = 0
        for linePoint in pointList:
            distance = MathHelper.calcDistance(linePoint, point)
            if minDistance > distance:
                minDistance = distance
                index = pointList.index(linePoint)

        pointAt = pointList[index]
        if index != 0 and index != len(pointList) - 1:
            pointBefore = pointList[index - 1]
            pointAfter = pointList[index + 1]
            projPointB = MathHelper.getProjectionPoint(pointBefore, pointAt, point)
            if projPointB != None:
                lenBeforeSegment = MathHelper.calcDistance(pointBefore, pointAt)
                lenBeforeProj = MathHelper.calcDistance(pointBefore, projPointB)
                if lenBeforeProj < lenBeforeSegment:
                    return projPointB

            projPointA = MathHelper.getProjectionPoint(pointAt, pointAfter, point)
            if projPointA != None:
                lenAfterSegment = MathHelper.calcDistance(pointAt, pointAfter)
                lenAfterProj = MathHelper.calcDistance(pointAt, projPointA)
                if lenAfterProj < lenAfterSegment:
                    return projPointA
        elif index == 0:
            pointAfter = pointList[index + 1]
            projPointA = MathHelper.getProjectionPoint(pointAt, pointAfter, point)
            if projPointA != None:
                lenAfterSegment = MathHelper.calcDistance(pointAt, pointAfter)
                lenAfterProj = MathHelper.calcDistance(pointAt, projPointA)
                if lenAfterProj < lenAfterSegment:
                    return projPointA
        elif index == len(pointList) - 1:
            pointBefore = pointList[index - 1]
            projPointB = MathHelper.getProjectionPoint(pointBefore, pointAt, point)
            if projPointB != None:
                lenBeforeSegment = MathHelper.calcDistance(pointBefore, pointAt)
                lenBeforeProj = MathHelper.calcDistance(pointBefore, projPointB)
                if lenBeforeProj < lenBeforeSegment:
                    return projPointB

        return pointAt
    def getQgsPointList(self):
        resultPointList = []
        geom = QgsGeometry.fromPolyline(self.method_14())
        return geom.asPolyline()
#     def getClosestPointTo(self, point3d, bool):
#         resultPoint3d = None
#         if not bool:
#
#             for i in range(len(self)):
# #                 distanceDouble = MathHelper.calcDistance(self[i].Position, point3d)
#                 if i > 0:
#                     if MathHelper.calcDistance(self[i].Position, point3d) > MathHelper.calcDistance(self[i - 1].Position, point3d):
#                         resultPoint3d = self[i - 1].Position
#                     else:
#                         resultPoint3d = self[i].Position
#         return resultPoint3d
    def SetBulgeAt(self, i, bulgeValue):
        self[i].Bulge = bulgeValue
    
    def GetPointAtDist(self, length_0, startAndEndPoint3ds = None):
        if length_0 == 0:
            return self[0].Position
        length = 0.0
        
        for i in range(len(self)):
            if i > 0:
                length = MathHelper.calcDistance(self[i - 1].Position, self[i].Position)
                if length_0 == length:
                    startAndEndPoint3ds.append(self[i - 1].Position)
                    startAndEndPoint3ds.append(self[i].Position)
                    return self[i].Position
                elif length_0 > length:
                    length_0 -= length
                    continue
                else:
#                     length_0 = (length - length_0)
                    bearing = MathHelper.getBearing(self[i - 1].Position, self[i].Position)
                    startAndEndPoint3ds.append(self[i - 1].Position)
                    startAndEndPoint3ds.append(self[i].Position)
                    return MathHelper.distanceBearingPoint(self[i - 1].Position, bearing, length_0)
#                     if bearing >= 0 and bearing <= math.pi / 2:
#                         alpha = math.pi / 2 - bearing
#                         
#                         startAndEndPoint3ds.append(self[i - 1].Position)
#                         startAndEndPoint3ds.append(self[i].Position)
#                         
#                         return Point3D(self[i - 1].Position.get_X() + math.cos(alpha) * length_0, self[i - 1].Position.get_Y() + math.sin(alpha) * length_0)
#                     elif bearing > math.pi / 2 and bearing <= math.pi:
#                         alpha = bearing - math.pi / 2
#                         
#                         startAndEndPoint3ds.append(self[i - 1].Position)
#                         startAndEndPoint3ds.append(self[i].Position)
#                         
#                         return Point3D(self[i - 1].Position.get_X() + math.cos(alpha) * length_0, self[i - 1].Position.get_Y() - math.sin(alpha) * length_0)
#                     elif bearing > math.pi and bearing <= math.pi * 3 / 2:
#                         alpha = math.pi * 3 / 2 - bearing
#                         
#                         startAndEndPoint3ds.append(self[i - 1].Position)
#                         startAndEndPoint3ds.append(self[i].Position)
#                         
#                         return Point3D(self[i - 1].Position.get_X() - math.cos(alpha) * length_0, self[i - 1].Position.get_Y() - math.sin(alpha) * length_0)
#                     elif bearing > math.pi * 3 / 2 and bearing <= 2 * math.pi:
#                         alpha = bearing - math.pi * 3 / 2
#                         
#                         startAndEndPoint3ds.append(self[i - 1].Position)
#                         startAndEndPoint3ds.append(self[i].Position)
#                         
#                         return Point3D(self[i - 1].Position.get_X() - math.cos(alpha) * length_0, self[i - 1].Position.get_Y() + math.sin(alpha) * length_0)
                    
                    
                
        pass
    def set_Closed(self, bool_0):
        if bool_0:
            polylineAreaPoint = self[0]
            self.append(polylineAreaPoint)
    def clear(self):
        while self.Count > 0:
            self.pop()
    def TransformBy(self, matrix3d):
        polylineAreaPointList = []
        for polylineAreaPoint in self:
            point3d = polylineAreaPoint.Position
            pointMatrix = [point3d.get_X(), point3d.get_Y(), point3d.get_Z(), 1]
            resultMatrix = []
            for matrix in matrix3d:
                matrix = numpy.multiply(matrix, pointMatrix)
                value = 0.0
                for num in matrix:
                    value += num
                resultMatrix.append(value)
            polylineAreaPointList.append(PolylineAreaPoint(Point3D(resultMatrix[0], resultMatrix[1], resultMatrix[2]), polylineAreaPoint.Bulge))
            resultPolylineArea = PolylineArea()
            for polylineAreaPoint in polylineAreaPointList:
                resultPolylineArea.Add(polylineAreaPoint)
        return resultPolylineArea
    def method_0(self, point2d_0):
        self.append(PolylineAreaPoint(point2d_0))

    def method_1(self, point3d_0):
        self.append(PolylineAreaPoint(point3d_0))

    def method_10(self):
        if (not self[len(self)- 1].position.smethod_170(self[0].position)):
            self.method_1(self[0].position)

    def method_11(self, int_0):
        item = self[int_0]
        return Point3D(item.Position.get_X(), item.Position.get_Y(), 0.0)

    def method_12(self, int_0):
        return self[int_0].position

    def method_13(self, int_0):
        return self[int_0].Bulge
    
    def get_Count(self):
        return len(self)
    Count = property(get_Count, None, None, None)
    
    # def asPolyline(self):
    #     polyline = Polyline()
    #     if (not self.isCircle):
    #         for item in self:
    #             position = item.Position;
    #             polyline.AddVertexAt(polyline.Length, position, item.Bulge, 0, 0)
    #     else:
    #         point3d = MathHelper.distanceBearingPoint(self.CenterPoint, 0, self.Radius);
    #         point3d1 = MathHelper.distanceBearingPoint(self.CenterPoint, 1.5707963267949, self.Radius);
    #         point3d2 = MathHelper.distanceBearingPoint(self.CenterPoint, 3.14159265358979, self.Radius);
    #         point3d3 = MathHelper.distanceBearingPoint(self.CenterPoint, 4.71238898038469, self.Radius);
    #         polyline.AddVertexAt(0, point3d, MathHelper.smethod_60(point3d, point3d1, point3d2), 0, 0);
    #         polyline.AddVertexAt(1, point3d2, MathHelper.smethod_60(point3d2, point3d3, point3d), 0, 0);
    #         polyline.AddVertexAt(2, point3d, 0, 0, 0);
    #     return polyline;

    def method_14_closed(self, levelNum = 8):
        point3dCollection = []
        count = len(self)
        if self.isCircle:
            return MathHelper.constructCircle(self[0].Position, self[0].bulge, 50)

        i = 0
        while i < count:
            position = self[i].position
            bulge = self[i].Bulge
            if i != count - 1:
                point3d = self[i + 1].position
            else:
                point3d = self[0].position
            point3dCollection.append(position)
#             if (not position.smethod_170(point3d)):
            if (not MathHelper.smethod_96(bulge)):
                if bulge < 0.25 and bulge > -0.25:
                    levelNum = 3
                MathHelper.getArc(position, point3d, bulge, levelNum, point3dCollection)
            i += 1
        point3dCollection.append(self[0].position)
        return point3dCollection


        # point3dCollection = []
        # count = len(self)
        # i = 0
        # while i < count:
        #     position = self[i].position
        #     bulge = self[i].Bulge
        #     if i != count - 1:
        #         point3d = self[i + 1].position
        #     else:
        #         point3d = self[0].position
        #     point3dCollection.append(position)
        #     if (not MathHelper.smethod_96(bulge)):
        #         centerPoint = MathHelper.smethod_71(position, point3d, bulge)
        #         radius = MathHelper.calcDistance(centerPoint, point3d)
        #         differenceAngle = (MathHelper.getBearing(centerPoint, point3d) - MathHelper.getBearing(centerPoint, position)) / (levelNum*10)
        #         for i in range(1, levelNum*10):
        #             if MathHelper.smethod_66(bulge) != TurnDirection.Left:
        #                 point3dCollection.append(MathHelper.distanceBearingPoint(centerPoint, (MathHelper.getBearing(centerPoint, position) + differenceAngle * i), radius))
        #             else:
        #                 point3dCollection.append(MathHelper.distanceBearingPoint(centerPoint, (MathHelper.getBearing(centerPoint, position) - differenceAngle * i), radius))
        #
        #
        #     i += 1
        # point3dCollection.append(self[0].position)
        # return point3dCollection
        
    def method_14(self, levelNum = 8):
        point3dCollection = []
        count = len(self)
        i = 0
        while i < count:
            position = self[i].position
            bulge = self[i].Bulge
            if i != count - 1:
                point3d = self[i + 1].position
            else:
                point3d = self[0].position
            point3dCollection.append(position)
#             if (not position.smethod_170(point3d)):
            if (not MathHelper.smethod_96(bulge)):
                if bulge < 0.25 and bulge > -0.25:
                    levelNum = 3
                MathHelper.getArc(position, point3d, bulge, levelNum, point3dCollection)
            i += 1
        return point3dCollection


        # point3dCollection = []
        # count = len(self)
        # i = 0
        # while i < count:
        #     position = self[i].position
        #     bulge = self[i].Bulge
        #     if i != count - 1:
        #         point3d = self[i + 1].position
        #     else:
        #         point3d = self[0].position
        #     point3dCollection.append(position)
        #     if (not MathHelper.smethod_96(bulge)):
        #         centerPoint = MathHelper.smethod_71(position, point3d, bulge)
        #         radius = MathHelper.calcDistance(centerPoint, point3d)
        #         differenceAngle =(MathHelper.getBearing(centerPoint, point3d) - MathHelper.getBearing(centerPoint, position)) / (levelNum*10)
        #         for i in range(1, levelNum*10):
        #             if MathHelper.smethod_66(bulge) != TurnDirection.Left:
        #                 point3dCollection.append(MathHelper.distanceBearingPoint(centerPoint, (MathHelper.getBearing(centerPoint, position) + differenceAngle * i), radius))
        #             else:
        #                 point3dCollection.append(MathHelper.distanceBearingPoint(centerPoint, (MathHelper.getBearing(centerPoint, position) - differenceAngle * i), radius))
        #
        #     i += 1
        # return point3dCollection

    def getCurve(self, smooth):
        point3dCollection = []
        count = len(self)
        i = 0
        while i < count:
            position = self[i].position
            bulge = self[i].Bulge
            if i != count - 1:
                point3d = self[i + 1].position
            else:
                point3d = self[0].position
            point3dCollection.append(position)
#             if (not position.smethod_170(point3d)):
            if (not MathHelper.smethod_96(bulge)):
                MathHelper.getArc(position, point3d, bulge, smooth, point3dCollection)
#                 print bulge
                
            i += 1 
        return point3dCollection
    def get_Length(self):
        length = 0.0
        for i in range(len(self)):
            if i > 0:
                length += MathHelper.calcDistance(self[i - 1].Position, self[i].Position)
        return length

    def method_15(self, bool_0):
        point3dCollection = Point3dCollection()
        for polylineAreaPoint in self:
            point3dCollection.Add(polylineAreaPoint.position)

#         if (bool_0):
#             point3dCollection.smethod_146()
        return point3dCollection

    def method_16(self):
        num = 0
        count = len(self)
        i = count
        while num < i: # i = base.Count):
            if (i < 2):
                return
            if num != i - 1:
                polylineAreaPoint = self[num + 1] 
            else:
                polylineAreaPoint = self[0]
            if not self[num].position.smethod_170(polylineAreaPoint.position):
                num += 1
            else:
                self.pop(num)
            i = len(self)

    def method_17(self):
        polylineArea = PolylineArea()
        polylineArea.extend(self)
        polylineArea.reverse()
        
        return polylineArea

    def method_18(self, double_0):
        if (len(self) == 0):
            raise UserWarning, Messages.ERR_INVALID_POLYLINE_AREA_FOR_OFFSET
        if (MathHelper.smethod_96(double_0)):
            return self
        if (self.isCircle):
            return PolylineArea(None, self.CenterPoint(), self.Radius() + double_0)
        if (len(self) == 1):
            return PolylineArea(None, self[0].position, double_0)
        direction = self.Direction()
        if (direction != TurnDirection.Left):
            if (direction != TurnDirection.Right):
                raise UserWarning, Messages.ERR_INVALID_POLYLINE_AREA_FOR_OFFSET
            num = -1.5707963267949
        else:
            num = 1.5707963267949
        
        polylineArea = PolylineArea()
        count = len(self)
        i = 0
        while i < count:
            position = self[i].position
            bulge = self[i].Bulge
            if i != count - 1 :
                point3d = self[i + 1].position 
            else:
                point3d = self[0].position
            if not position.smethod_170(point3d):
                if not MathHelper.smethod_96(bulge):
                    turnDirection = MathHelper.smethod_7(bulge)
                    point3d1 = MathHelper.smethod_71(position, point3d, bulge)
                    if (turnDirection != direction):
                        point3d2 = MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(point3d1, position), MathHelper.calcDistance(point3d1, position) - double_0);
                        point3d3 = MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(point3d1, point3d), MathHelper.calcDistance(point3d1, point3d) - double_0);
                    else:
                        point3d2 = MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(point3d1, position), MathHelper.calcDistance(point3d1, position) + double_0);
                        point3d3 = MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(point3d1, point3d), MathHelper.calcDistance(point3d1, point3d) + double_0);
                    polylineArea.Add(PolylineAreaPoint(point3d2, MathHelper.smethod_57(turnDirection, point3d2, point3d3, point3d1)))
                    polylineArea.Add(PolylineAreaPoint(point3d3, 5))
                else:
                    num3 = MathHelper.getBearing(position, point3d)
                    polylineArea.Add(PolylineAreaPoint(MathHelper.distanceBearingPoint(position, num3 + num, double_0)))
                    polylineArea.Add(PolylineAreaPoint(MathHelper.distanceBearingPoint(point3d, num3 + num, double_0), 5))
            i += 1
        count = polylineArea.Count
        j = 0
        while j < count:
            position = polylineArea[j].position
            bulge = polylineArea[j].Bulge
            if j != 0:
                num1 = j - 1 
            else:
                num1 = count - 1
            position1 = polylineArea[num1].position
            if j != count - 1:
                num2 = j + 1 
            else:
                num2 = 0
            point3d = polylineArea[num2].position
            if (MathHelper.smethod_98(bulge, 5)):
                bulge1 = polylineArea[num1].Bulge
                bulge2 = polylineArea[num2].Bulge
                if (MathHelper.smethod_96(bulge1) and MathHelper.smethod_96(bulge2)):
                    num4 = j + 2
                    if (j == count - 2):
                        num4 = 0
                    elif (j == count - 1):
                        num4 = 1
                    position2 = polylineArea[num4].position
                    num5 = MathHelper.getBearing(position1, position)
                    num6 = MathHelper.getBearing(point3d, position2)
                    turnDirection1 = MathHelper.smethod_63(num5, num6, AngleUnits.Radians)
                    if (turnDirection1 == TurnDirection.Nothing):
                        polylineArea[j].Bulge = 0
                    elif (turnDirection1 != direction):
                        point3d6 = MathHelper.distanceBearingPoint(position, MathHelper.getBearing(position, position1), 100);
                        point3d7 = MathHelper.distanceBearingPoint(point3d, MathHelper.getBearing(point3d, position2), 100);
                        point3d4 = MathHelper.getIntersectionPoint(point3d6, position, point3d, point3d7)
                        if point3d4 == None:
#                             point3d4 = Point3D.get_Origin()
                            j += 1
                            continue
                        polylineArea[j].position = point3d4
                        polylineArea[j].Bulge = 0
                        polylineArea[num2].position = point3d4
                        polylineArea[num2].Bulge = 0
                    else:
                        point3d8 = MathHelper.distanceBearingPoint(position, MathHelper.getBearing(position, position1) + num, double_0)
                        polylineArea[j].Bulge = MathHelper.smethod_57(direction, position, point3d, point3d8)
                elif not MathHelper.smethod_96(bulge1):
                    turnDirection2 = MathHelper.smethod_7(bulge1)
                    point3d5 = MathHelper.smethod_71(position1, position, bulge1)
                    if turnDirection2 != direction :
                        point3d5 = MathHelper.distanceBearingPoint(point3d5, MathHelper.getBearing(point3d5, position), MathHelper.calcDistance(point3d5, position) + double_0) 
                    else:
                        point3d5 = MathHelper.distanceBearingPoint(point3d5, MathHelper.getBearing(point3d5, position), MathHelper.calcDistance(point3d5, position) - double_0)
                    polylineArea[j].Bulge = MathHelper.smethod_57(direction, position, point3d, point3d5)
                else:
                    point3d9 = MathHelper.distanceBearingPoint(position, MathHelper.getBearing(position, position1) + num, double_0)
                    polylineArea[j].Bulge = MathHelper.smethod_57(direction, position, point3d, point3d9)
            j += 1
#         i = 0
#         while i < len(polylineArea):
#             if polylineArea[i].position == None:
#                 polylineArea.pop(i)
#                 i -= 1
#             i += 1
#         for i in range(len(polylineArea:
#             if polylineAreaPoint.position == None:
#                 polylineArea.pop(polylineArea.index(polylineAreaPoint))
        return polylineArea

    def method_19(self, int_0, double_0):
        self[int_0].Bulge = double_0

    def method_2(self, point2d_0, double_0):
        self.append(PolylineAreaPoint(point2d_0, double_0))

    def method_20(self, double_0, bool_0):
        if (self.Direction() == TurnDirection.Nothing):
            return
        self[0].Bulge = double_0
        position = self[0].position
        position1 = self[1].position
        turnDirection = MathHelper.smethod_66(double_0)
        point3d = MathHelper.smethod_71(position, position1, double_0)
        if (turnDirection != TurnDirection.Left):
            if turnDirection != TurnDirection.Right :
                num = MathHelper.getBearing(position, position1) 
            else:
                num = MathHelper.getBearing(position1, point3d) - 1.5707963267949
        else:
            num = MathHelper.getBearing(position1, point3d) + 1.5707963267949
            
        count = len(self)
        i = 1
        while i < count:
            position = self[i].position
            if (i != count - 1):
                position1 = self[i + 1].position
            else:
                if (not bool_0):
                    return
                position1 = self[0].position
            point3d = MathHelper.smethod_75(num, position, position1)
            self[i].Bulge = MathHelper.smethod_59(num, position, position1)
            turnDirection = MathHelper.smethod_63(num, MathHelper.getBearing(position, position1), AngleUnits.Radians)
            if (turnDirection == TurnDirection.Left):
                num = MathHelper.getBearing(position1, point3d) + 1.5707963267949
            elif (turnDirection == TurnDirection.Right):
                num = MathHelper.getBearing(position1, point3d) - 1.5707963267949
            i += 1

#         public PolylineArea method_21(int int_0, bool bool_0, bool bool_1)
#         {
    def method_21(self, int_0, bool_0, bool_1):
            polylineArea = PolylineArea()
            if (not self.isCircle):
                direction = self.Direction()
                count = len(self)
                if (direction != TurnDirection.Nothing):
                    i = 0
                    while (i < count):
                        item = self[i]
                        position = item.position
                        bulge = item.Bulge
                        if i != count - 1 :
                            point3d = self[i + 1].position 
                        else:
                            point3d = self[0].position
                        if (not position.smethod_170(point3d)):
                            if (not MathHelper.smethod_96(bulge)):
                                point3d2 = position
                                point3d3 = point3d
                                turnDirection = MathHelper.smethod_66(bulge)
                                point3d1 = MathHelper.smethod_71(point3d2, point3d3, bulge)
                                num = MathHelper.calcDistance(point3d1, point3d2)
                                num1 = MathHelper.smethod_5(bulge)
                                if (turnDirection == direction):
                                    if (not bool_0):
                                        polylineArea.method_5(MathHelper.smethod_137(point3d2, point3d1, num, num1, int_0, turnDirection));
                                    else:
                                        polylineArea.method_5(MathHelper.smethod_138(point3d2, point3d1, num, num1, int_0, turnDirection));
                                elif (not bool_0):
                                    polylineArea.method_5(MathHelper.smethod_138(point3d2, point3d1, num, num1, int_0, turnDirection));
                                else:
                                    polylineArea.method_5(MathHelper.smethod_137(point3d2, point3d1, num, num1, int_0, turnDirection));
                            else:
                                polylineArea.method_1(position);
                        i += 1
            else:
                point3d4 = MathHelper.distanceBearingPoint(self.CenterPoint, 0, self.Radius);
                if (not bool_0):
                    polylineArea.method_5(MathHelper.smethod_137(point3d4, self.CenterPoint(), self.Radius(), 6.28318530717959, int_0, TurnDirection.Right))
                else:
                    polylineArea.method_5(MathHelper.smethod_138(point3d4, self.CenterPoint(), self.Radius(), 6.28318530717959, int_0, TurnDirection.Right))
            if (bool_1):
                polylineArea.method_10()
            return polylineArea

#         public void method_22(double double_0)
#         {
    def method_22(self, double_0):
        for polylineAreaPoint in self:
            polylineAreaPoint.position = polylineAreaPoint.position.smethod_167(double_0)

#         public PolylineArea method_23(double double_0, OffsetGapType offsetGapType_0)
#         {
    def method_23_New(self, double_0, offsetGapType_0):
        polyline = PolylineArea.smethod_131(self)
        # if self.Direction() == TurnDirection.Right:
        #     double_0 = double_0 * (-1)
        offsetCurves = polyline.getOffsetCurveNoClosed(double_0)
#         if (offsetCurves != None and offsetCurves.get_Count() == 1):
#             polylineArea = PolylineArea.smethod_1(offsetCurves[0]);
#             return polylineArea;
#         offsetCurves.pop(offsetCurves.Count - 1)
#         offsetCurves.pop(offsetCurves.Count - 2)
        return offsetCurves

    def method_23(self, double_0, offsetGapType_0, segment = 0, joinStyle = 0, mitreLimit = 0):
        polyline = PolylineArea.smethod_131(self)
        # offsetCurves = polyline.getOffsetCurveNoosed(double_0, segment, joinStyle, mitreLimit)
        offsetCurves = polyline.getOffsetCurveNo(double_0, 4)
        return offsetCurves

    def method_3(self, point3d_0, double_0):
        self.append(PolylineAreaPoint(point3d_0, double_0))

#         public void method_4(Point2dCollection point2dCollection_0)
#         {
    def method_4(self, point2dCollection_0):
        for current in point2dCollection_0:
            self.append(PolylineAreaPoint(current))

#         public void method_5(Point3dCollection point3dCollection_0)
#         {
    def method_5(self, point3dCollection_0):
        for point3d in point3dCollection_0:
            self.append(PolylineAreaPoint(point3d))

#         public void method_6(params Point2d[] point2d_0)
#         {
    def method_6(self, point2d_0):
        for point2d0 in point2d_0:
            self.append(PolylineAreaPoint(point2d0))

#         public void method_7(params Point3d[] point3d_0)
#         {
    def method_7(self, point3dList):
        for point3d0 in point3dList:
            self.append(PolylineAreaPoint(point3d0))

#         public void method_8(PolylineArea polylineArea_0)
#         {
    def method_8(self, polylineArea_0):
        for polylineArea0 in polylineArea_0:
            self.append(PolylineAreaPoint(polylineArea0.position, polylineArea0.Bulge))

#         public void method_9(int int_0, Point3d point3d_0)
#         {
    def method_9(self, int_0, point3d_0):
            self.insert(int_0, PolylineAreaPoint(point3d_0))

#         public static PolylineArea smethod_0(Region region_0)
#         {
    def method_160(self, int_0):
        length = self.get_Length() / int_0;
        point3dCollection = []
        for i in range(int_0):
            self.GetPointAtDist(i * length, point3dCollection)
#         if (self.get_Closed() or self.GetPoint2dAt(0) == self.GetPoint2dAt(self.get_NumberOfVertices() - 1)):
        self.GetPointAtDist(0, point3dCollection);
        return point3dCollection;
    
    @staticmethod
    def smethod_0(region_0):
        return PolylineArea(QgsGeometry.asPolygon(region_0)[0])
    @staticmethod
    def smethod_1(lineGeometry):

        return PolylineArea(lineGeometry.asPolyline())

    @staticmethod
    def smethod_131(polylineArea_0):
        polylineArea = PolylineArea();
        if (not polylineArea_0.isCircle):
            for i in range(len(polylineArea_0)):
                item = polylineArea_0[i];
                x = item.Position.get_X();
                position = item.Position;
                polylineArea.Add(item);
        else:
            point3d = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint(), 0, polylineArea_0.Radius());
            point3d1 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint(), 1.5707963267949, polylineArea_0.Radius());
            point3d2 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint(), 3.14159265358979, polylineArea_0.Radius());
            point3d3 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint(), 4.71238898038469, polylineArea_0.Radius());
            polylineArea.Add(PolylineAreaPoint(point3d, MathHelper.smethod_60(point3d, point3d1, point3d2)));
            polylineArea.Add(PolylineAreaPoint(point3d2, MathHelper.smethod_60(point3d2, point3d3, point3d)));
            polylineArea.Add(PolylineAreaPoint(point3d));
        return polylineArea;
    
    @staticmethod
    def smethod_133(point3dCollection_0, bool_0):
        polylineArea = PolylineArea(point3dCollection_0)
        if bool_0:
            return PolylineArea(polylineArea.method_14_closed())
        return polylineArea



    @staticmethod
    def smethod_136(polylineArea_0, bool_0):
        polylineArea = PolylineArea.smethod_131(polylineArea_0);
        if bool_0:
            polylineArea = PolylineArea(polylineArea.method_14_closed())
        return polylineArea;

    @staticmethod
    def RotatePolyLineArcGIS(polylineArea, originPt, angle):
        # angle = math.pi / 2 - angle
        resultPolylineArea = PolylineArea()
        if not isinstance(polylineArea, PolylineArea) or len(polylineArea) == 0:
            return None
        for polylineAreaPt in polylineArea:
            pt = polylineAreaPt.Position
            dist = MathHelper.calcDistance(pt, originPt)
            bearing = MathHelper.getBearing(originPt, pt) + angle
            newPt = MathHelper.distanceBearingPointArcGIS(originPt, bearing, dist)
            resultPolylineArea.Add(PolylineAreaPoint(newPt, polylineAreaPt.bulge))
        return resultPolylineArea
    @staticmethod
    def RotatePolyLine(polylineArea, originPt, angle):
        resultPolylineArea = PolylineArea()
        if not isinstance(polylineArea, PolylineArea) or len(polylineArea) == 0:
            return None
        for polylineAreaPt in polylineArea:
            pt = polylineAreaPt.Position
            dist = MathHelper.calcDistance(pt, originPt)
            bearing = MathHelper.getBearing(originPt, pt) + angle
            newPt = MathHelper.distanceBearingPoint(originPt, bearing, dist)
            resultPolylineArea.Add(PolylineAreaPoint(newPt, polylineAreaPt.bulge))
        return resultPolylineArea

    @staticmethod
    def MovePolyLine(polylineArea, dx, dy):
        resultPolylineArea = PolylineArea()
        if not isinstance(polylineArea, PolylineArea) or len(polylineArea) == 0:
            return None
        for polylineAreaPt in polylineArea:
            pt = polylineAreaPt.Position
            newPt = Point3D(pt.x() - dx, pt.y() - dy, pt.get_Z())
            resultPolylineArea.Add(PolylineAreaPoint(newPt, polylineAreaPt.bulge))
        return resultPolylineArea