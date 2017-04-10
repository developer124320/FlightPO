'''
Created on Feb 21, 2015

@author: Administrator
'''
from FlightPlanner.helpers0 import MathHelper, Unit
from FlightPlanner.messages import Messages
from FlightPlanner.types0 import TurnDirection, Point3D, AngleUnits, Point3dCollection
from FlightPlanner.Polyline import Polyline
from FlightPlanner.QgisHelper0 import QgisHelper
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
        

               
    def Add(self, polylineAreaPoint):
        self.append(polylineAreaPoint)
        
    def CenterPoint(self):
        if len(self) > 0:
            return self[0].Position
        else:
            return None

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
        
    def getOffsetCurve(self, distance):
        pointList = self.method_14_closed()
#         pointList.append(self[1].Position)
        polyline = QgisHelper.offsetCurve(pointList, distance)
        polylineAreaNew = PolylineArea()
        polylineAreaNew.method_5(polyline)
        return polylineAreaNew
    def getOffsetCurveNoClosed(self, distance, segment = 0, joinStyle = 0, mitreLimit = 0):
#         pointList = self.method_14()
#
#         originPointList = []
#
#         for item in self:
#             originPointList.append(item.Position)
#
#
# #         pointList.append(self[1].Position)
#         polyline = QgisHelper.offsetCurve(pointList, distance,segment , joinStyle , mitreLimit )
#
#         index = 0
#         resultPointList = []
#         for item in self:
#             point000 = polyline[0]
#             for i in range(1, len(polyline) - 1):
#                 if MathHelper.calcDistance(item.Position, point000) >  MathHelper.calcDistance(item.Position, polyline[i]):
#                     point000 = polyline[i]
#             resultPointList.append(point000)
#             index = 0
#         polylineAreaNew = PolylineArea()
#         for i in range(self.Count):
#             polylineAreaNew.Add(PolylineAreaPoint(resultPointList[i], self[i].Bulge))
#         # polylineAreaNew.method_5(polyline)
#         return polylineAreaNew


        # pointList = self.method_14()
#         pointList.append(self[1].Position)

        pointList = []
        count = len(self)
        i = 0
        radiusDifference = 0
        for item in self:
            i += 1
            if i == 1:
                # if self[i-1].Bulge != 0:
                #     centerPoint= MathHelper.smethod_71(self[i-1].Position, self[i].Position, self[i-1].Bulge)
                #     angle = math.atan(math.fabs(self[i-1].Bulge)) * 2
                #     radiusDifference = math.fabs(distance) / math.cos(angle)
                #     radius = MathHelper.calcDistance(self[i-1].Position , centerPoint) + radiusDifference
                #     bearingNew = MathHelper.getBearing(centerPoint, self[i-1].Position)
                #     point = MathHelper.distanceBearingPoint(centerPoint, bearingNew, radius)
                #     pointList.append(point)
                #     continue
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
                # if self[i-2].Bulge != 0:
                #     centerPoint= MathHelper.smethod_71(self[i-2].Position, self[i-1].Position, self[i-2].Bulge)
                #     angle = math.atan(math.fabs(self[i-2].Bulge)) * 2
                #     radiusDifference = math.fabs(distance) / math.cos(angle)
                #     radius = MathHelper.calcDistance(self[i-2].Position , centerPoint) + radiusDifference
                #     bearingNew = MathHelper.getBearing(centerPoint, self[i-1].Position)
                #     point = MathHelper.distanceBearingPoint(centerPoint, bearingNew, radius)
                #     pointList.append(point)
                #     continue
                # if self[i-1].Bulge != 0:
                #     centerPoint= MathHelper.smethod_71(self[i-1].Position, self[i].Position, self[i-1].Bulge)
                #     angle = math.atan(math.fabs(self[i-1].Bulge)) * 2
                #     radiusDifference = math.fabs(distance) / math.cos(angle)
                #     radius = MathHelper.calcDistance(self[i-1].Position , centerPoint) + radiusDifference
                #     bearingNew = MathHelper.getBearing(centerPoint, self[i-1].Position)
                #     point = MathHelper.distanceBearingPoint(centerPoint, bearingNew, radius)
                #     pointList.append(point)
                #     continue
                # # if self[i-2].Bulge != 0:
                # #     centerPoint= MathHelper.smethod_71(self[i-2].Position, self[i-1].Position, self[i-2].Bulge)
                # #     radius = MathHelper.calcDistance(pointList[len(pointList)-1] , centerPoint)
                # #
                # #     bearingNew = MathHelper.getBearing(centerPoint, self[i-1].Position)
                # #     point = MathHelper.distanceBearingPoint(centerPoint, bearingNew, radius)
                # #     radius2 = MathHelper.calcDistance(point , centerPoint)
                # #
                # #     endPoint = pointList[len(pointList)-1]
                # #     mPtX = point.get_X() + (endPoint.get_X() - point.get_X()) / 2 if endPoint.get_X() > point.get_X() else endPoint.get_X() + (point.get_X() - endPoint.get_X()) / 2
                # #     mPtY = point.get_Y() + (endPoint.get_Y() - point.get_Y()) / 2 if endPoint.get_Y() > point.get_Y() else endPoint.get_Y() + (point.get_Y() - endPoint.get_Y()) / 2
                # #
                # #     mPt = Point3D(mPtX, mPtY)
                # #     bearing1 = MathHelper.getBearing(centerPoint, mPt)
                # #     # bearing2 = MathHelper.getBearing(centerPoint, point)
                # #     # bearingDifference = math.fabs(bearing1 - bearing2)
                # #     middlePoint = None
                # #
                # #     middlePoint = MathHelper.distanceBearingPoint(centerPoint, bearing1, radius)
                # #     radius1 = MathHelper.calcDistance(middlePoint, centerPoint)
                # #     turnDirection0 = MathHelper.smethod_65([endPoint, middlePoint, point])
                # #     bulge = MathHelper.smethod_57(turnDirection0, endPoint, middlePoint, point);
                # #
                # #     centerPoint1= MathHelper.smethod_71(pointList[len(pointList)-1], point, bulge)
                # #     pointList.append(point)
                #
                # else:
                #     bearing = MathHelper.getBearing(self[i-1].Position, self[i].Position)
                #     point = MathHelper.distanceBearingPoint(self[i - 1].Position, bearing - Unit.ConvertDegToRad(90) , distance)
                #     pointList.append(point)
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

        # polyline = QgisHelper.offsetCurve(pointList, distance, segment, joinStyle, mitreLimit)
        # polyline.reverse()
        polylineAreaNew = PolylineArea()
        for i in range(count):
            # bulge = 0
            # if self[i].Bulge != 0:
            #     centerPoint= MathHelper.smethod_71(self[i].Position, self[i+ 1].Position, self[i].Bulge)
            #     radius = MathHelper.calcDistance(self[i].Position, centerPoint)
            #
            #     bearing1 = MathHelper.getBearing(centerPoint, self[i].Position)
            #     bearing2 = MathHelper.getBearing(centerPoint, self[i+1].Position)
            #     bearingDifference = math.fabs(bearing1 - bearing2)
            #     middlePoint = None
            #     if self[i].Position.get_X() < self[i+1].Position.get_X():
            #         middlePoint = MathHelper.distanceBearingPoint(centerPoint, bearing2 - bearingDifference / 2, radius + distance)
            #
            #     else:
            #         middlePoint = MathHelper.distanceBearingPoint(centerPoint, bearing1 + bearingDifference / 2, radius + distance)
            #     turnDirection0 = MathHelper.smethod_65([self[i].Position, middlePoint, self[i+1].Position])
            #     bulge = MathHelper.smethod_57(turnDirection0, self[i].Position, middlePoint, self[i+1].Position);
            # polylineAreaNew.Add(PolylineAreaPoint(pointList[i], bulge))
            polylineAreaNew.Add(PolylineAreaPoint(pointList[i], self[i].Bulge))
        # polylineAreaNew.method_5(polyline)
        i = 0
        # count = len(self) if len(self) < len(polylineAreaNew) else len(polylineAreaNew)
        # for i in range(count - 1):
        #     polylineAreaNew[i].bulge = self[i].Bulge
        return polylineAreaNew
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
    
    def asPolyline(self):
        polyline = Polyline()
        if (not self.isCircle):
            for item in self:
                position = item.Position;
                polyline.AddVertexAt(polyline.Length, position, item.Bulge, 0, 0)
        else:
            point3d = MathHelper.distanceBearingPoint(self.CenterPoint, 0, self.Radius);
            point3d1 = MathHelper.distanceBearingPoint(self.CenterPoint, 1.5707963267949, self.Radius);
            point3d2 = MathHelper.distanceBearingPoint(self.CenterPoint, 3.14159265358979, self.Radius);
            point3d3 = MathHelper.distanceBearingPoint(self.CenterPoint, 4.71238898038469, self.Radius);
            polyline.AddVertexAt(0, point3d, MathHelper.smethod_60(point3d, point3d1, point3d2), 0, 0);
            polyline.AddVertexAt(1, point3d2, MathHelper.smethod_60(point3d2, point3d3, point3d), 0, 0);
            polyline.AddVertexAt(2, point3d, 0, 0, 0);
        return polyline;

    def method_14_closed(self, levelNum = 8):
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
                MathHelper.getArc(position, point3d, bulge, levelNum, point3dCollection)
            i += 1
        point3dCollection.append(self[0].position)              
        return point3dCollection
        
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
                MathHelper.getArc(position, point3d, bulge, levelNum, point3dCollection)
#                 print bulge
                
            i += 1      
#         point3dCollection.append(self[0].position)              
        return point3dCollection

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
        # if self.Direction() == TurnDirection.Right:
        #     double_0 = double_0 * -1
        offsetCurves = polyline.getOffsetCurveNoClosed(double_0, segment, joinStyle, mitreLimit)
#         if (offsetCurves != None and offsetCurves.get_Count() == 1):
#             polylineArea = PolylineArea.smethod_1(offsetCurves[0]);
#             return polylineArea;
#         offsetCurves.pop(offsetCurves.Count - 1)
#         offsetCurves.pop(offsetCurves.Count - 2)
        return offsetCurves
    
#             offsetType = AcadHelper.OffsetType
#             try
#             {
#                 if (self.Direction == TurnDirection.Right)
#                 {
#                     double_0 = double_0 * -1;
#                 }
#                 AcadHelper.OffsetType = offsetGapType_0;
#                 Polyline polyline = AcadHelper.smethod_131(self);
#                 try
#                 {
#                     DBObjectCollection offsetCurves = polyline.GetOffsetCurves(double_0);
#                     try
#                     {
#                         if (offsetCurves != null && offsetCurves.get_Count() == 1)
#                         {
#                             polylineArea = PolylineArea.smethod_1(offsetCurves.get_Item(0) as Polyline);
#                             return polylineArea;
#                         }
#                     }
#                     finally
#                     {
#                         AcadHelper.smethod_25(offsetCurves);
#                     }
#                 }
#                 finally
#                 {
#                     AcadHelper.smethod_24(polyline);
#                 }
#                 return null;
#             }
#             finally
#             {
#                 AcadHelper.OffsetType = offsetType;
#             }
#             return polylineArea;
#         }

#         public void method_3(Point3d point3d_0, double double_0)
#         {
#             base.Add(new PolylineAreaPoint(point3d_0, double_0));
#         }
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
            point3dCollection.append(self.GetPointAtDist(i * length))
#         if (self.get_Closed() or self.GetPoint2dAt(0) == self.GetPoint2dAt(self.get_NumberOfVertices() - 1)):
        point3dCollection.append(self.GetPointAtDist(0));
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
    
    
#         public static PolylineArea smethod_1(Polyline polyline_0)
#         {
#             PolylineArea polylineArea;
#             DBObjectCollection dBObjectCollection = new DBObjectCollection();
#             polyline_0.Explode(dBObjectCollection);
#             try
#             {
#                 polylineArea = PolylineArea.smethod_4(dBObjectCollection, polyline_0.get_Normal());
#             }
#             finally
#             {
#                 AcadHelper.smethod_25(dBObjectCollection);
#             }
#             return polylineArea;
#         }
# 
#         public static PolylineArea smethod_2(Polyline2d polyline2d_0)
#         {
#             PolylineArea polylineArea;
#             DBObjectCollection dBObjectCollection = new DBObjectCollection();
#             polyline2d_0.Explode(dBObjectCollection);
#             try
#             {
#                 polylineArea = PolylineArea.smethod_4(dBObjectCollection, polyline2d_0.get_Normal());
#             }
#             finally
#             {
#                 AcadHelper.smethod_25(dBObjectCollection);
#             }
#             return polylineArea;
#         }
# 
#         public static PolylineArea smethod_3(Circle circle_0)
#         {
#             return new PolylineArea(circle_0.get_Center(), circle_0.get_Radius());
#         }
# 
#         private static PolylineArea smethod_4(DBObjectCollection dbobjectCollection_0, Vector3d vector3d_0)
#         {
#             int num;
#             PolylineArea polylineArea = null;
#             for (int i = 0; i < dbobjectCollection_0.get_Count(); i++)
#             {
#                 Curve item = dbobjectCollection_0.get_Item(i) as Curve;
#                 if (item == null)
#                 {
#                     return null;
#                 }
#                 if (item.get_Closed())
#                 {
#                     if (dbobjectCollection_0.get_Count() > 1)
#                     {
#                         return null;
#                     }
#                     if (!(item is Circle))
#                     {
#                         return null;
#                     }
#                     return PolylineArea.smethod_3(item as Circle);
#                 }
#             }
#             using (Plane plane = new Plane(new Point3d(0, 0, 0), vector3d_0))
#             {
#                 polylineArea = new PolylineArea();
#                 int count = dbobjectCollection_0.get_Count();
#                 Curve curve = dbobjectCollection_0.get_Item(0) as Curve;
#                 Point3d startPoint = curve.get_StartPoint();
#                 PolylineAreaPoint polylineAreaPoint = new PolylineAreaPoint(startPoint.TransformBy(Matrix3d.PlaneToWorld(plane)), PolylineArea.smethod_5(curve, false));
#                 polylineArea.Add(polylineAreaPoint);
#                 Point3d endPoint = curve.get_EndPoint();
#                 polylineAreaPoint = new PolylineAreaPoint(endPoint.TransformBy(Matrix3d.PlaneToWorld(plane)));
#                 polylineArea.Add(polylineAreaPoint);
#                 Point3d point3d = curve.get_StartPoint();
#                 Point3d endPoint1 = curve.get_EndPoint();
#                 curve.Dispose();
#                 count--;
#                 do
#                 {
#                     num = count;
#                     IEnumerator enumerator = dbobjectCollection_0.GetEnumerator();
#                     try
#                     {
#                         while (true)
#                         {
#                             if (enumerator.MoveNext())
#                             {
#                                 Curve current = (Curve)enumerator.Current;
#                                 if (!current.get_IsDisposed())
#                                 {
#                                     if (MathHelper.smethod_103(current.get_StartPoint(), endPoint1, 0.0001) || MathHelper.smethod_103(current.get_EndPoint(), endPoint1, 0.0001))
#                                     {
#                                         polylineAreaPoint.Bulge = PolylineArea.smethod_5(current, MathHelper.smethod_103(current.get_EndPoint(), endPoint1, 0.0001));
#                                         endPoint1 = (!MathHelper.smethod_103(current.get_StartPoint(), endPoint1, 0.0001) ? current.get_StartPoint() : current.get_EndPoint());
#                                         polylineAreaPoint = new PolylineAreaPoint(endPoint1.TransformBy(Matrix3d.PlaneToWorld(plane)));
#                                         polylineArea.Add(polylineAreaPoint);
#                                         current.Dispose();
#                                         count--;
#                                         break;
#                                     }
#                                     else if (MathHelper.smethod_103(current.get_StartPoint(), point3d, 0.0001) || MathHelper.smethod_103(current.get_EndPoint(), point3d, 0.0001))
#                                     {
#                                         double num1 = PolylineArea.smethod_5(current, MathHelper.smethod_103(current.get_StartPoint(), point3d, 0.0001));
#                                         point3d = (!MathHelper.smethod_103(current.get_StartPoint(), point3d, 0.0001) ? current.get_StartPoint() : current.get_EndPoint());
#                                         PolylineAreaPoint polylineAreaPoint1 = new PolylineAreaPoint(point3d.TransformBy(Matrix3d.PlaneToWorld(plane)), num1);
#                                         polylineArea.Insert(0, polylineAreaPoint1);
#                                         current.Dispose();
#                                         count--;
#                                         break;
#                                     }
#                                 }
#                             }
#                             else
#                             {
#                                 break;
#                             }
#                         }
#                     }
#                     finally
#                     {
#                         IDisposable disposable = enumerator as IDisposable;
#                         if (disposable != null)
#                         {
#                             disposable.Dispose();
#                         }
#                     }
#                 }
#                 while (num > count && count > 0);
#             }
#             return polylineArea;
#         }
# 
#         private static double smethod_5(Curve curve_0, bool bool_0)
#         {
#             double num;
#             double num1 = 0;
#             Arc curve0 = curve_0 as Arc;
#             if (curve0 != null)
#             {
#                 num = (curve0.get_StartAngle() <= curve0.get_EndAngle() ? curve0.get_StartAngle() : curve0.get_StartAngle() - 6.28318530717959);
#                 num1 = Math.Tan((curve0.get_EndAngle() - num) / 4);
#                 if (bool_0)
#                 {
#                     num1 = -num1;
#                 }
#             }
#             return num1;
#         }
#     }
# }