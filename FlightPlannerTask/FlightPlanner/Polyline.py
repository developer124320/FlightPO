'''
Created on Mar 27, 2015

@author: Administrator
'''
from qgis.core import QgsGeometry

from FlightPlanner.helpers import MathHelper, Unit
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint

class PolylinePoint:
    def __init__(self, point3d, bulge = 0, startWidth = 0, endWidth = 0):
        self.point3d = point3d
        self.bulge = bulge
        self.startWidth = startWidth
        self.endWidth = endWidth
        
class Polyline(list) :
    def __init__(self, vertices = 0):
        list.__init__(self)
        self.Closed = False
        self.ConstantWidth = 0.0
        self.Elevation = 0.0
        self.HasBulges = False
        self.HasWidth = False
        self.IsOnlyLines = True
        self.Length = 0
        #public Vector3d Normal { get; set; }
        self.Normal = None
        self.NumberOfVertices = 0
        self.Plinegen = False
        self.Thickness = 0.0

    def get_NumberOfVertices(self):
        return len(self)
    
    def get_constant_width(self):
        return self.__ConstantWidth


    def get_elevation(self):
        return self.__Elevation


    def get_has_bulges(self):
        return self.__HasBulges


    def get_has_width(self):
        return self.__HasWidth


    def get_is_only_lines(self):
        return self.__IsOnlyLines


    def get_length(self):
        return len(self)


    def get_normal(self):
        return self.__Normal


    def get_number_of_vertices(self):
        return len(self)


    def get_plinegen(self):
        return self.__Plinegen


    def get_thickness(self):
        return self.__Thickness


    def set_constant_width(self, value):
        self.__ConstantWidth = value


    def set_elevation(self, value):
        self.__Elevation = value


    def set_has_bulges(self, value):
        self.__HasBulges = value


    def set_has_width(self, value):
        self.__HasWidth = value


    def set_is_only_lines(self, value):
        self.__IsOnlyLines = value


    def set_length(self, value):
        self.__Length = value


    def set_normal(self, value):
        self.__Normal = value


    def set_number_of_vertices(self, value):
        self.__NumberOfVertices = value


    def set_plinegen(self, value):
        self.__Plinegen = value


    def set_thickness(self, value):
        self.__Thickness = value


    def del_constant_width(self):
        del self.__ConstantWidth


    def del_elevation(self):
        del self.__Elevation


    def del_has_bulges(self):
        del self.__HasBulges


    def del_has_width(self):
        del self.__HasWidth


    def del_is_only_lines(self):
        del self.__IsOnlyLines


    def del_length(self):
        del self.__Length


    def del_normal(self):
        del self.__Normal


    def del_number_of_vertices(self):
        del self.__NumberOfVertices


    def del_plinegen(self):
        del self.__Plinegen


    def del_thickness(self):
        del self.__Thickness


    def get_closed(self):
        return self.__Closed


    def set_closed(self, value):
        self.__Closed = value


    def del_closed(self):
        del self.__Closed

    Closed = property(get_closed, set_closed, del_closed, "Closed's docstring")
    ConstantWidth = property(get_constant_width, set_constant_width, del_constant_width, "ConstantWidth's docstring")
    Elevation = property(get_elevation, set_elevation, del_elevation, "Elevation's docstring")
    HasBulges = property(get_has_bulges, set_has_bulges, del_has_bulges, "HasBulges's docstring")
    HasWidth = property(get_has_width, set_has_width, del_has_width, "HasWidth's docstring")
    IsOnlyLines = property(get_is_only_lines, set_is_only_lines, del_is_only_lines, "IsOnlyLines's docstring")
    Length = property(get_length, set_length, del_length, "Length's docstring")
    Normal = property(get_normal, set_normal, del_normal, "Normal's docstring")
    NumberOfVertices = property(get_number_of_vertices, set_number_of_vertices, del_number_of_vertices, "NumberOfVertices's docstring")
    Plinegen = property(get_plinegen, set_plinegen, del_plinegen, "Plinegen's docstring")
    Thickness = property(get_thickness, set_thickness, del_thickness, "Thickness's docstring")

    def IntersectWith(self, other, tolerance, result):
        minePointList = self.getQgsPointList()
        otherPointList = other.getQgsPointList()
        mineGeom = QgsGeometry.fromPolyline(minePointList)
        otherGeom = QgsGeometry.fromPolyline(otherPointList)
        intersectGeom = mineGeom.intersection(otherGeom)
        if intersectGeom != None:
            qgsPoint = intersectGeom.asPoint()
            result.append(qgsPoint)
            return True
        else:
            return False
    
    def GetClosestPointTo(self, point, bExtend):
#         polyline = self.getQgsPolyline()
#         vtx, at, before, after, distance = polyline.closestVertex(point)
#         vtxBefore = polyline.vertexAt(before)
#         vtxAfter = polyline.vertexAt(after)
#         distBefore = QgsGeometry.fromPolyline([vtxBefore, vtx]).distance(QgsGeometry.fromPoint(point))
#         distAfter = QgsGeometry.fromPolyline([vtx, vtxAfter]).distance(QgsGeometry.fromPoint(point))
#         if distBefore < distance:
#             closestPoint = MathHelper.getProjectionPoint(vtxBefore, vtx, point)
#         elif distAfter < distance:
#             closestPoint = MathHelper.getProjectionPoint(vtx, vtxAfter, point)
#         else:
#             closestPoint = vtx
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
        
    def get_Length(self):
        # line = self.getQgsPolyline()
        # return line.length()
        polylineArea = PolylineArea()
        for polylinePoint in self:
            polylineArea.Add(PolylineAreaPoint(polylinePoint.point3d, polylinePoint.bulge))
        pointArray = polylineArea.method_14(4)
        count = len(pointArray)
        length = 0.0
        for i in range(1, count):
            length += MathHelper.calcDistance(pointArray[i-1], pointArray[i])
        return length


    
    def getQgsPolyline(self):
        pointList = self.getQgsPointList()
        return QgsGeometry.fromPolyline(pointList)
        
    def getQgsPointList(self):
        pointList = []
        for i in range(self.NumberOfVertices):
            polylinePoint = self[i]
            pointList.append(polylinePoint.point3d)
            if not MathHelper.smethod_96(polylinePoint.bulge):
                if i != self.NumberOfVertices - 1:
                    point3d = self[i + 1].point3d
                else:
                    point3d = self[0].point3d
                MathHelper.getArc(polylinePoint.point3d, point3d, polylinePoint.bulge, 4, pointList)
        
        if self.Closed:
            pointList.append(self[0].point3d)
        return pointList
    
    def getGeometry(self):
        pointList = []
        polygonsList = []
        width = self[0].startWidth
        if MathHelper.smethod_96(self[0].bulge):
            pt0 = MathHelper.distanceBearingPoint(self[0].point3d, MathHelper.getBearing(self[0].point3d, self[1].point3d) - Unit.ConvertDegToRad(90), width / 2.0,)
            pt1 = MathHelper.distanceBearingPoint(self[0].point3d, MathHelper.getBearing(self[0].point3d, self[1].point3d) + Unit.ConvertDegToRad(90), width / 2.0,)
            pt2 = MathHelper.distanceBearingPoint(self[1].point3d, MathHelper.getBearing(self[0].point3d, self[1].point3d) + Unit.ConvertDegToRad(90), width / 2.0,)
            pt3 = MathHelper.distanceBearingPoint(self[1].point3d, MathHelper.getBearing(self[0].point3d, self[1].point3d) - Unit.ConvertDegToRad(90), width / 2.0,)
            geom = QgsGeometry.fromPolygon([[pt0, pt1, pt2, pt3]])
            polygonsList.append(geom)
        else:
            polylineArea = PolylineArea()
            polylineArea.Add(PolylineAreaPoint(self[0].point3d, self[0].bulge))
            polylineArea.Add(PolylineAreaPoint(self[1].point3d))

            pointArray = polylineArea.method_14(4)
            pt0 = MathHelper.distanceBearingPoint(self[0].point3d, MathHelper.getBearing(self[0].point3d, pointArray[1]) - Unit.ConvertDegToRad(90), width / 2.0,)
            pt1 = MathHelper.distanceBearingPoint(self[0].point3d, MathHelper.getBearing(self[0].point3d, pointArray[1]) + Unit.ConvertDegToRad(90), width / 2.0,)
            pt2 = MathHelper.distanceBearingPoint(self[1].point3d, MathHelper.getBearing(pointArray[len(pointArray) - 2], self[1].point3d) + Unit.ConvertDegToRad(90), width / 2.0,)
            pt3 = MathHelper.distanceBearingPoint(self[1].point3d, MathHelper.getBearing(pointArray[len(pointArray) - 2], self[1].point3d) - Unit.ConvertDegToRad(90), width / 2.0,)
            polylineArea0 = PolylineArea()
            polylineArea0.Add(PolylineAreaPoint(pt0, self[0].bulge))
            polylineArea0.Add(PolylineAreaPoint(pt3))
            polylineArea1 = PolylineArea()
            polylineArea1.Add(PolylineAreaPoint(pt2, -self[0].bulge))
            polylineArea1.Add(PolylineAreaPoint(pt1))
            pointArrayResult = []
            for pt in polylineArea0.method_14(4):
                pointArrayResult.append(pt)
            for pt in polylineArea1.method_14(4):
                pointArrayResult.append(pt)
            geom = QgsGeometry.fromPolygon([pointArrayResult])
            polygonsList.append(geom)
        return polygonsList


        # for i in range(self.NumberOfVertices):
        #     polylinePoint = self[i]
        #
        #     if polylinePoint.startWidth != width:
        #         if len(pointList) > 1:
        #             geom = QgsGeometry.fromPolyline(pointList)
        #             polygon = geom.buffer(width / 2.0, 0, 2, 0, 0)
        #             polygonsList.append(polygon)
        #         width = polylinePoint.startWidth
        #         pointList = []
        #     pointList.append(polylinePoint.point3d)
        #     if not MathHelper.smethod_96(polylinePoint.bulge):
        #         if i != self.NumberOfVertices - 1:
        #             point3d = self[i + 1].point3d
        #         else:
        #             point3d = self[0].point3d
        #         MathHelper.getArc(polylinePoint.point3d, point3d, polylinePoint.bulge, 4, pointList)
        #
        # if len(pointList) > 1:
        #     geom = QgsGeometry.fromPolyline(pointList)
        #     polygon = geom.buffer(width / 2.0, 0, 2, 0, 0)
        #     polygonsList.append(polygon)
        return polygonsList
    
    def Add(self, point3d):
        self.append(PolylinePoint(point3d))
#     public void AddVertexAt(int index, Point2d pt, double bulge, double startWidth, double endWidth);
    def AddVertexAt(self, index, pt, bulge, startWidth, endWidth):
        self.insert(index, PolylinePoint(pt, bulge, startWidth, endWidth))
        pass
#     public void ConvertFrom(Entity entity, bool transferId);
    def ConvertFrom(self, entity, transferId):
        pass
#     public Polyline2d ConvertTo(bool transferId);
    def ConvertTo(self, transferId):
        pass
#     public CircularArc2d GetArcSegment2dAt(int index);
    def GetPointAtDist(self, distance):
        pointList = self.getQgsPointList()
        return MathHelper.getPointAtDist(pointList, distance)
        
    def GetDistAtPoint(self, point):
        pointList = self.getQgsPointList()
        if len(pointList) < 2:
            return MathHelper.calcDistance(point, pointList[0])
        return MathHelper.distanceAlongLine(pointList, point)
        
    def GetArcSegment2dAt(self, index):
        return self.GetArcSegmentAt(index)
#     public CircularArc3d GetArcSegmentAt(int index);
    def GetArcSegmentAt(self, index):
        segment = []
        if self[index].bulge != 0.0:
            if index != self.NumberOfVertices - 1:
                MathHelper.getArc(self[index].point3d, self[index+1].point3d, self[index].bulge, 4, segment)
            else:
                if self.Closed:
                    MathHelper.getArc(self[index].point3d, self[0].point3d, self[index].bulge, 4, segment)
                else:
                    segment = None
        else:
            segment.append(self[index])
            if index != self.NumberOfVertices - 1:
                segment.append(self[index + 1])
            else:
                if self.Closed:
                    segment.append(self[0])
                else:
                    segment = None
        return segment 
    def GetOffsetCurves(self, smooth):
        point3dCollection = []
        count = len(self)
        i = 0
        while i < count:
            position = self[i].point3d
            bulge = self.GetBulgeAt(i)
            if i != count - 1:
                point3d = self[i + 1].point3d
            else:
                point3d = self[0].point3d
            point3dCollection.append(position)
#             if (not position.smethod_170(point3d)):
            if (not MathHelper.smethod_96(bulge)):
                MathHelper.getArc(position, point3d, bulge, smooth, point3dCollection)
#                 print bulge
                
            i += 1 
#         point3dCollection.append(self[0].position)                   
        return point3dCollection
#     public double GetBulgeAt(int index);
    def GetBulgeAt(self, index):
        return self[index].bulge
#     public double GetEndWidthAt(int index);
    def GetEndWidthAt(self, index):
        return self[index].endWidth
#     public LineSegment2d GetLineSegment2dAt(int index);
    def GetLineSegment2dAt(self, index):
        return self.GetLineSegmentAt(index)
#     public LineSegment3d GetLineSegmentAt(int index);
    def GetLineSegmentAt(self, index):
        if index < self.NumberOfVertices - 1:
            return [self[index], self[index + 1]] 
        else:
            return None if not self.Closed else [self[index], self[0]]
#     public Point2d GetPoint2dAt(int index);
    def GetPoint2dAt(self, index):
        return self.GetPoint3dAt(index)
#     public Point3d GetPoint3dAt(int value);
    def GetPoint3dAt(self, index):
        return self[index].point3d
#     public SegmentType GetSegmentType(int index);
    def GetSegmentType(self, index):
        pass
#     public double GetStartWidthAt(int index);
    def GetStartWidthAt(self, index):
        pass
#     public void MaximizeMemory();
#     public void MinimizeMemory();
#     public virtual bool OnSegmentAt(int index, Point2d pt2d, double value);
    def OnSegmentAt(self, index, pt2d, value):
        pass
#     public void RemoveVertexAt(int index);
    def RemoveVertexAt(self, index):
        self.pop(index)
#     public void Reset(bool reuse, int vertices);
    def Reset(self, reuse, vertices):
        pass
#     public void SetBulgeAt(int index, double bulge);
    def SetBulgeAt(self, index, bulge):
        self[index].bulge = bulge
#     public void SetEndWidthAt(int index, double endWidth);
    def SetEndWidthAt(self, index, endWidth):
        self[index].endWidth = endWidth
#     public void SetPointAt(int index, Point2d pt);
    def SetPointAt(self, index, pt):
        self[index].point3d = pt
#     public void SetStartWidthAt(int index, double startWidth);
    def SetStartWidthAt(self, index, startWidth):
        self[index].startWidth = startWidth
