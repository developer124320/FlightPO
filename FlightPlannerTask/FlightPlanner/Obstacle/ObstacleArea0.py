'''
Created on Jan 23, 2015

@author: KangKuk
'''

from FlightPlanner.helpers0 import MathHelper
from FlightPlanner.QgisHelper0 import QgisHelper
from FlightPlanner.messages import Messages
from FlightPlanner.types0 import Point3D, TurnDirection, ObstacleAreaResult, IntersectionStatus, Point3dCollection
from FlightPlanner.polylineArea0 import PolylineArea, PolylineAreaPoint
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper
from qgis.core import QGis, QgsRectangle, QgsGeometry, QgsCsException, QgsPoint,\
        QgsFeatureRequest, QgsCoordinateTransform, QgsFeature
import math
class IObstacleArea:
    '''
    Interface for Obstacle Area
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
    def isValid(self):
        pass
    
    def isValidForPreview(self):
        pass
    
#     def nominalTrack(self):
#         pass
    
    def pointInArea(self, point3d, tolerance):
        '''
        return Bool
        '''
    
    def imethod_1(self, point3d_0, double_0, double_1, lstOutput):
        '''
        return ObstacleAreaResult
        '''
    def imethod_2(self):
        '''
        return Bool
        '''
    def imethod_3(self):
        '''
        '''
    def imethod_4(self, bool_0):
        '''
        return Bool
        '''
    def imethod_5(self, xmlFile_0, xmlNode_0):
        '''
        '''

# namespace PHX.Types
# {
#     internal class PrimaryObstacleArea : IObstacleArea
#     {
class ComplexObstacleArea(list):
    '''
    PrimaryObstacleArea
    '''
    def __init__(self):
        self.obstacleArea = None 
        self.nominalTrack = None
        pass
    
    def Add(self, iobstacleArea_0):
        self.append(iobstacleArea_0)
    def Insert(self, i, iobstacleArea_0):
        self.insert(i, iobstacleArea_0)
            
    def method_0(self, iobstacleArea_0, double_0):
        iobstacleArea_0.nominalTrack = double_0;
        self.Add(iobstacleArea_0);   
    
    def pointInArea(self, point3d_0, double_0, double_1):
        num = None;
        num1 = None;
        obstacleAreaResult = None;
        obstacleAreaResult1 = ObstacleAreaResult.Outside;
        double_2 = None;
        double_3 = None;
#         if not len(self) > 0:
        if (self.obstacleArea != None and not self.obstacleArea.pointInPolygon(point3d_0, double_0)):
            return (ObstacleAreaResult.Outside, double_2, double_3);
#         using (IEnumerator<IObstacleArea> enumerator = base.GetEnumerator())
#         {
#             while (enumerator.MoveNext())
#             {
        if len(self) > 0:
            for current in self:
    #             IObstacleArea current = enumerator.Current;
                num0_1 = []
                if math.fabs(point3d_0.get_X() - 666426) < 1:
                    n=0
                obstacleAreaResult2 = current.imethod_1(point3d_0, double_0, double_1, num0_1);
                if len(num0_1) > 0:
                    num = num0_1[0]
                    num1 = num0_1[1]
                else:
                    num = None
                    num1 = None
                if (obstacleAreaResult2 == ObstacleAreaResult.Primary):
                    double_2 = num;
                    double_3 = num1;
                    obstacleAreaResult1 = obstacleAreaResult2;
                    obstacleAreaResult = obstacleAreaResult1;
                    return (obstacleAreaResult, double_2, double_3);
                else:
                    if (obstacleAreaResult2 != ObstacleAreaResult.Secondary or (not double_2 == None and num <= double_2)):
                        continue;
                    double_2 = num;
                    double_3 = num1;
                    obstacleAreaResult1 = obstacleAreaResult2;
                    return (obstacleAreaResult1, double_2, double_3);
            return (obstacleAreaResult1, double_2, double_3);
        else:
            return (obstacleAreaResult, double_2, double_3);
    def imethod_1(self, point3d_0, double_0, double_1, listOutPut):
        num = None;
        num1 = None;
        obstacleAreaResult = None;
        obstacleAreaResult1 = ObstacleAreaResult.Outside;
        double_2 = None;
        double_3 = None;
#         if not len(self) > 0:
        if (self.obstacleArea != None and not self.obstacleArea.pointInPolygon(point3d_0, double_0)):
            listOutPut.append(double_2)
            listOutPut.append(double_3)
            return ObstacleAreaResult.Outside
#         using (IEnumerator<IObstacleArea> enumerator = base.GetEnumerator())
#         {
#             while (enumerator.MoveNext())
#             {
        if len(self) > 0:
            for current in self:
    #             IObstacleArea current = enumerator.Current;
                num0_1 = []
                if math.fabs(point3d_0.get_X() - 666426) < 1:
                    n=0
                obstacleAreaResult2 = current.imethod_1(point3d_0, double_0, double_1, num0_1);
                if len(num0_1) > 0:
                    num = num0_1[0]
                    num1 = num0_1[1]
                else:
                    num = None
                    num1 = None
                if (obstacleAreaResult2 == ObstacleAreaResult.Primary):
                    double_2 = num;
                    double_3 = num1;
                    obstacleAreaResult1 = obstacleAreaResult2;
                    obstacleAreaResult = obstacleAreaResult1;
                    listOutPut.append(double_2)
                    listOutPut.append(double_3)
                    return obstacleAreaResult
                    # return (obstacleAreaResult, double_2, double_3);
                else:
                    if (obstacleAreaResult2 != ObstacleAreaResult.Secondary or (not double_2 == None and num <= double_2)):
                        continue;
                    double_2 = num;
                    double_3 = num1;
                    obstacleAreaResult1 = obstacleAreaResult2;
                    listOutPut.append(double_2)
                    listOutPut.append(double_3)
                    return obstacleAreaResult1
                    # return (obstacleAreaResult1, double_2, double_3);
            listOutPut.append(double_2)
            listOutPut.append(double_3)
            return obstacleAreaResult1
            # return (obstacleAreaResult1, double_2, double_3);
        else:
            listOutPut.append(double_2)
            listOutPut.append(double_3)
            return obstacleAreaResult
            # return (obstacleAreaResult, double_2, double_3);
    def isValid(self):
        if len(self) <= 0:
            return False
        for area1 in self:
            if area1.IsValid:
                continue
            else:
                return False
        return True
    IsValid = property(isValid, None, None, None)

    def isValidForPreview(self):
        if len(self) <= 0:
            return False
        for area1 in self:
            if area1.IsValidForPreview:
                continue
            else:
                return False
        return True
    IsValidForPreview = property(isValidForPreview, None, None, None)

    def ToString(self):
        num = 0;
        num1 = 0;
        num2 = 0;
        for obstacleArea in self:
            if (isinstance(obstacleArea , PrimaryObstacleArea)):
                num += 1;
            elif (not isinstance(obstacleArea , SecondaryObstacleArea)):
                if (not isinstance(obstacleArea , PrimarySecondaryObstacleArea)):
                    continue;
                num2 += 1;
            else:
                num1 += 1;
        if (num == 0 and num1 == 0 and num2 == 0):
            return "Complex area (0 sub-areas defined)";
        stringBuilder = "Complex area (";
        if (num > 0):
            stringBuilder += "{%i} primary area(s)"%(num)
        if (num1 > 0):
            stringBuilder += "{%i} secondary area(s)"%(num1)
        if (num2 > 0):
            stringBuilder += "{%i} primary & secondary area(s)"%(num2)
        return stringBuilder

    def get_ObstacleArea(self):
        if (self.obstacleArea != None):
            return self.obstacleArea;
        point3dCollection = Point3dCollection();
        for obstacleArea in self:
            point3dCollection.appendList(obstacleArea.SelectionArea);
        return PrimaryObstacleArea(PolylineArea(MathHelper.smethod_190(point3dCollection)));
    def set_ObstacleArea(self, value):
        self.obstacleArea = value
    ObstacleArea = property(get_ObstacleArea, set_ObstacleArea, None, None)

    def get_SelectionArea(self):
        if (self.obstacleArea != None):
            return self.obstacleArea.SelectionArea;
        point3dCollection = Point3dCollection();
        for obstacleArea in self:
            point3dCollection.appendList(obstacleArea.SelectionArea);
        return MathHelper.smethod_190(point3dCollection);
    SelectionArea = property(get_SelectionArea, None, None, None)
    
    def get_NominalTrack(self):
        return self.nominalTrack;
    def set_NominalTrack(self, value):
        self.nominalTrack = value;
        for obstacleArea in self:
            obstacleArea.NominalTrack = self.nominalTrack;
    NominalTrack = property(get_NominalTrack, set_NominalTrack, None, None)
class PrimaryObstacleArea(IObstacleArea):
    '''
    PrimaryObstacleArea
    '''
    def __init__(self, polylineArea_0 = None):        
        '''
        costructor
        '''
        '''Point3dCollection'''
        self.selectionArea = []
        
        '''Point3dCollection'''
        self.polygonArea = []
        
        '''PolylineArea'''
        self.previewArea = None
        
        '''PolylineArea'''
        self.originalArea = None
        
        '''List<PrimaryObstacleArea.IPrimaryArcArea>'''
        self.arcs = []
 
        '''bool'''
        self.isCircularArea = None
        
        '''bool'''
        self.isSimpleArea = None
        
        '''Point3d'''
        self.circAreaCenter = Point3D.get_Origin();
 
        '''double'''
        self.circAreaRadius = 0.0001;
 
        '''string'''
        self.error = Messages.ERR_NO_AREA_SELECTED
        
        self.nominalTrack = None
        
        if polylineArea_0 != None:
            self.method_1(polylineArea_0)
 
    def isValid(self):
        return self.error == None or self.error == ""
    IsValid = property(isValid, None, None, None)

    def isArc(self):
        return len(self.arcs) > 0
    IsArc = property(isArc, None, None, None)
    def isValidForPreview(self):
        return self.previewArea != None and len(self.previewArea) > 1
    IsValidForPreview = property(isValidForPreview, None, None, None)

#     def nominalTrack(self):
#         return IObstacleArea.nominalTrack(self)


#         public bool pointInArea(Point3d point3d_0, double double_0)
#         {
    def get_SelectionArea(self):
        return self.selectionArea
    SelectionArea = property(get_SelectionArea, None, None, None)

    def get_PreviewArea(self):
        return self.previewArea
    PreviewArea = property(get_PreviewArea, None, None, None)


    
    def pointInPolygon(self, point3d, tolerance):
        return self.pointInArea(point3d, tolerance)
    
    def pointInArea(self, point3d, tolerance):
        flag = False
        if not self.isCircularArea:
            if self.isSimpleArea:
                return MathHelper.pointInPolygon(self.polygonArea, point3d, tolerance)
            if MathHelper.pointInPolygon(self.selectionArea, point3d, tolerance):
                if MathHelper.pointInPolygon(self.polygonArea, point3d, tolerance):
                    return True
                for current in self.arcs:
                    if not current.imethod_0(point3d, tolerance):
                        continue
                    flag = True
                    return flag
                return False
            return flag
        elif MathHelper.calcDistance(self.circAreaCenter, point3d) - tolerance <= self.circAreaRadius:
            return True
        return False

    def imethod_1(self, point3d_0, double_0, double_1, lstOutput):
        double_2 = double_1;
        double_3 = None

        
        if self.pointInArea(point3d_0, double_0):
            lstOutput.append(double_2)
            lstOutput.append(double_3)
            return ObstacleAreaResult.Primary
        return ObstacleAreaResult.Outside


    def imethod_2(self):
        return IObstacleArea.imethod_2(self)


    def imethod_3(self):
        return IObstacleArea.imethod_3(self)


    def imethod_4(self, bool_0):
        return IObstacleArea.imethod_4(self, bool_0)


    def imethod_5(self, xmlFile_0, xmlNode_0):
        return IObstacleArea.imethod_5(self, xmlFile_0, xmlNode_0)
    def set_areas(self, pointArrayIn0, pointArrayOut0):
        innerStartPoint = Point3D(pointArrayOut0[0].x(), pointArrayOut0[0].y())
        innerEndPoint = Point3D(pointArrayOut0[1].x(), pointArrayOut0[1].y())
        outerStartPoint = Point3D(pointArrayIn0[0].x(), pointArrayIn0[0].y())
        outerEndPoint = Point3D(pointArrayIn0[1].x(), pointArrayIn0[1].y())
        num = int(len(pointArrayOut0) / 2)
        innerMiddlePoint = Point3D(pointArrayOut0[num].x(), pointArrayOut0[num].y())
        bulge0 = MathHelper.smethod_60(innerStartPoint, innerMiddlePoint, innerEndPoint)
        outerMiddlePoint = Point3D(pointArrayIn0[num].x(), pointArrayIn0[num].y())
        bulge1 = MathHelper.smethod_60(outerEndPoint, outerMiddlePoint, outerStartPoint)
        polylineArea = PolylineArea()

        polylineArea.Add(PolylineAreaPoint(innerStartPoint, bulge0))
        polylineArea.Add(PolylineAreaPoint(innerEndPoint))
        polylineArea.Add(PolylineAreaPoint(outerEndPoint, bulge1))
        polylineArea.Add(PolylineAreaPoint(outerStartPoint))
        self.method_1(polylineArea)
    def method_1(self, polylineArea_0):
            self.selectionArea = []
            self.polygonArea = []
            self.originalArea = polylineArea_0
            self.previewArea = None
            self.arcs = []
            self.isCircularArea = False
            self.isSimpleArea = True
            self.circAreaCenter = Point3D.get_Origin()
            self.circAreaRadius = 0.0001
            self.error = Messages.ERR_NO_AREA_SELECTED
            try:
                if (not polylineArea_0.isCircle):
                    direction = polylineArea_0.Direction()
                    count = polylineArea_0.Count
                    if (direction != TurnDirection.Nothing):
                        self.previewArea = PolylineArea()
                        i = 0
                        while i < count:
                            item = polylineArea_0[i]
                            position = item.position
                            bulge = item.Bulge
                            if i != count - 1:
                                point3d = polylineArea_0[i + 1].position 
                            else:
                                point3d = polylineArea_0[0].position
                            if (not position.smethod_170(point3d)):
                                self.previewArea.Add(PolylineAreaPoint(item.position, item.Bulge))
                                if (not MathHelper.smethod_96(bulge)):
                                    self.isSimpleArea = False
                                    point3d2 = position
                                    point3d3 = point3d
                                    turnDirection = MathHelper.smethod_66(bulge)
                                    point3d1 = MathHelper.smethod_71(point3d2, point3d3, bulge)
                                    num = MathHelper.calcDistance(point3d1, point3d2)
                                    num1 = MathHelper.smethod_5(bulge)

                                    polylineArea = PolylineArea()
                                    polylineArea.Add(PolylineAreaPoint(point3d2, bulge))
                                    polylineArea.Add(PolylineAreaPoint(point3d3))
                                    pointCount = len(polylineArea.method_14())

                                    if (turnDirection != direction):
                                        point3dCollection = MathHelper.smethod_137(point3d2, point3d1, num, num1, 3, turnDirection)
                                        self.selectionArea.extend(point3dCollection)
                                        self.polygonArea.extend(MathHelper.smethod_138(point3d2, point3d1, num, num1, 3, turnDirection))
                                        point3dCollection1 = MathHelper.smethod_138(point3d2, point3d1, num + 1, num1, 3, turnDirection)
                                        point3dCollection.append(point3d3)
                                        point3dCollection1.reverse()
                                        point3dCollection.extend(point3dCollection1)
#                                         point3dCollection.smethod_146()
                                        self.arcs.append(PrimaryArcAreaOuter(point3d1, num, point3dCollection))
                                    else:
                                        point3dCollection2 = MathHelper.smethod_138(point3d2, point3d1, num, num1, 3, turnDirection)
                                        self.selectionArea.extend(point3dCollection2)
                                        self.polygonArea.extend(MathHelper.smethod_137(point3d2, point3d1, num, num1, 3, turnDirection))
                                        point3dCollection3 = []
                                        point3dCollection3 = MathHelper.smethod_137(point3d2, point3d1, max([num - 1, 0.1]), num1, 3, turnDirection)
                                        point3dCollection2.append(point3d3)
                                        point3dCollection3.reverse()
                                        point3dCollection2.extend(point3dCollection3)
#                                         point3dCollection2.smethod_146()
                                        self.arcs.append(PrimaryArcAreaInner(point3d1, num, point3dCollection2))
                                else:
                                    self.selectionArea.append(position)
                                    self.polygonArea.append(position)
                            i += 1
                else:
                    point3d4 = MathHelper.distanceBearingPoint(polylineArea_0.CenterPoint(), 0, polylineArea_0.Radius())
                    self.selectionArea.extend(MathHelper.smethod_138(point3d4, polylineArea_0.CenterPoint(), polylineArea_0.Radius(), 6.28318530717959, 3, TurnDirection.Right))
                    self.circAreaCenter = polylineArea_0.CenterPoint()
                    self.circAreaRadius = polylineArea_0.Radius()
                    self.isCircularArea = True
                    point2d = Point3D(self.circAreaCenter.get_X(), self.circAreaCenter.get_Y(), 0)
                    point2d1 = MathHelper.distanceBearingPoint(point2d, 0, self.circAreaRadius)
                    point2d2 = MathHelper.distanceBearingPoint(point2d, 1.5707963267949, self.circAreaRadius)
                    point2d3 = MathHelper.distanceBearingPoint(point2d, 3.14159265358979, self.circAreaRadius)
                    point2d4 = MathHelper.distanceBearingPoint(point2d, 4.71238898038469, self.circAreaRadius)
                    self.previewArea = PolylineArea()
                    self.previewArea.Add(PolylineAreaPoint(point2d1, MathHelper.smethod_60(point2d1, point2d2, point2d3)))
                    self.previewArea.Add(PolylineAreaPoint(point2d3, MathHelper.smethod_60(point2d3, point2d4, point2d1)))
                    self.previewArea.Add(PolylineAreaPoint(point2d1))
                    self.error = None
            finally:
                if (len(self.selectionArea) < 3):
                    self.error = Messages.ERR_INVALID_POLYGON_AREA
                elif (not self.isCircularArea):
                    if (len(self.polygonArea) < 3):
                        self.error = Messages.ERR_INVALID_POLYGON_AREA
                    elif (MathHelper.smethod_132(self.selectionArea)):
                        self.error = Messages.ERR_COMPLEX_POLYGON_SELECTED
                    elif (not MathHelper.smethod_132(self.polygonArea)):
                        self.error = None
                    else:
                        self.error = Messages.ERR_COMPLEX_POLYGON_SELECTED
    def ToString(self):
        if (not self.IsValid):
            return self.error;
        if (self.isCircularArea):
            return Messages.CIRCULAR_AREA;
        if (len(self.arcs) == 0):
            return Messages.SIMPLE_AREA_N_POINTS%(len(self.polygonArea));
        return Messages.SIMPLE_AREA_N_POINTS_WITH_ARCS%(len(self.polygonArea));
class IPrimaryArcArea:
    def __init__(self):
        self.Center = None
        self.Points = None
        self.Radius = None
    def imethod_0(self, point3d_0, double_0):
        pass

class PrimaryArcAreaInner(IPrimaryArcArea):
    def __init__(self, point3d_0, double_0, point3dCollection_0):
        self.Center = point3d_0;
        self.Radius = double_0;
        self.Points = point3dCollection_0;

    def imethod_0(self, point3d_0, double_0):
        if (MathHelper.calcDistance(self.Center, point3d_0) - double_0 > self.Radius):
            return False
        return MathHelper.pointInPolygon(self.Points, point3d_0, double_0)

class PrimaryArcAreaOuter(IPrimaryArcArea):
    def __init__(self, point3d_0, double_0, point3dCollection_0):
        self.Center = point3d_0;
        self.Radius = double_0;
        self.Points = point3dCollection_0;

    def imethod_0(self, point3d_0, double_0):
        if (MathHelper.calcDistance(self.Center, point3d_0) + double_0 < self.Radius):
            return False
        return MathHelper.pointInPolygon(self.Points, point3d_0, double_0)


class SecondaryObstacleArea(IObstacleArea):
    def __init__(self, point3d_0, point3d_1, point3d_2, point3d_3 = None, double_0 = None, point3d_4 = None, point3d_5 = None, innerR =None, outerR =None):
        '''
        SecondaryObstacleArea.ISecondaryArea
        '''
        self.nominalTrack = 0.0
        self.obstacleArea = None
        self.isArc = False
        if (point3d_3 == None):
            self.area = SecondaryAreaPie(point3d_0, point3d_1, point3d_2)
            return
        if(double_0 != None):
            self.area = SecondaryAreaStraight(point3d_0, point3d_1, point3d_2, point3d_3)
            self.nominalTrack = double_0
            return
            
        if(point3d_4 == None):
            self.area = SecondaryAreaStraight(point3d_0, point3d_1, point3d_2, point3d_3)
#             self.nominalTrack = double_0
            return
            
        if(double_0 == None):
            self.area = SecondaryAreaArc(point3d_0, point3d_1, point3d_2, point3d_3, point3d_4, point3d_5 , innerR, outerR)
            self.isArc = True
            
        '''
        PrimaryObstacleArea
        '''

        '''
        double
        '''
        
    def get_SelectionArea(self):
        return self.area.selectionArea
    SelectionArea = property(get_SelectionArea, None, None, None)

    def get_PreviewArea(self):
        return self.area.PreviewArea
    PreviewArea = property(get_PreviewArea, None, None, None)

    def get_IsArc(self):
        return self.isArc
    IsArc = property(get_IsArc, None, None, None)
    def pointInArea(self, point3d, tolerance):
        return IObstacleArea.pointInArea(self, point3d, tolerance)


    def imethod_1(self, point3d_0, double_0, double_1, lstOutput):
        if (self.obstacleArea != None and not self.obstacleArea.pointInPolygon(point3d_0, double_0)):
            double_2 = None
            double_3 = None
            return ObstacleAreaResult.Outside
#         outputList = []
        return self.area.imethod_1(point3d_0, double_0, double_1, self.nominalTrack, lstOutput)
#         lstOutput = outputList
#         return result
    def set_areas(self, pointArrayIn0, pointArrayOut0):
        if len(pointArrayIn0) > 2 and len(pointArrayOut0) > 2:
            innerStartPoint = Point3D(pointArrayIn0[0].x(), pointArrayIn0[0].y())
            innerEndPoint = Point3D(pointArrayIn0[len(pointArrayIn0) - 1].x(), pointArrayIn0[len(pointArrayIn0) - 1].y())
            num = int(len(pointArrayIn0) / 2)
            innerMiddlePoint = Point3D(pointArrayIn0[num].x(), pointArrayIn0[num].y())
            outerStartPoint = Point3D(pointArrayOut0[0].x(), pointArrayOut0[0].y())
            outerEndPoint = Point3D(pointArrayOut0[len(pointArrayOut0) - 1].x(), pointArrayOut0[len(pointArrayOut0) - 1].y())
            outerMiddlePoint = Point3D(pointArrayOut0[num].x(), pointArrayOut0[num].y())
            self.area = SecondaryAreaArc(innerStartPoint, innerMiddlePoint, innerEndPoint, outerStartPoint, outerMiddlePoint, outerEndPoint, MathHelper.smethod_60(innerStartPoint, innerMiddlePoint, innerEndPoint), MathHelper.smethod_60(outerStartPoint, outerMiddlePoint, outerEndPoint))
        # if len(pointArrayIn1) == 2 and len(pointArrayOut1) == 2:
        #     innerStartPoint = Point3D(pointArrayIn1[0].x(), pointArrayIn1[0].y())
        #     innerEndPoint = Point3D(pointArrayIn1[1].x(), pointArrayIn1[1].y())
        #     outerStartPoint = Point3D(pointArrayOut1[0].x(), pointArrayOut1[0].y())
        #     outerEndPoint = Point3D(pointArrayOut1[1].x(), pointArrayOut1[1].y())
        #     self.primaryArea = PrimaryObstacleArea(PolylineArea([innerStartPoint, innerEndPoint, outerEndPoint, outerStartPoint]))
    def get_NominalTrack(self):
        return self.nominalTrack
    def set_NominalTrack(self, value):
        self.nominalTrack = value
    NominalTrack = property(get_NominalTrack, set_NominalTrack, None, None)
    def isValidForPreview(self):
        if self.area == None:
            return False
        return self.area.IsValidForPreview;
    IsValidForPreview = property(isValidForPreview, None, None, None)

    def isValid(self):
        if self.area == None:
            return False
        return self.area.IsValid;
    IsValid = property(isValid, None, None, None)


    def ToString(self):
        if (self.area.error == None or self.area.error == ""):
            return self.area.ToString();
        return self.area.error
class ISecondaryArea:
    def imethod_0(self, point3d_0, double_0):
        '''
        bool imethod_0(Point3d point3d_0, double double_0)
        '''
    def imethod_1(self, point3d_0, double_0, double_1, double_2):
        '''
        ObstacleAreaResult imethod_1(Point3d point3d_0, double double_0, double double_1, double double_2, out double double_3, out double double_4);
        '''

# class SecondaryAreaStraight(ISecondaryArea):
#     def __init__(self, point3d_0, point3d_1, point3d_2, point3d_3):
#         self.innerStart = None;
#
#         self.innerEnd = None;
#
#         self.outerStart = None;
#
#         self.outerEnd = None;
#
#         self.selectionArea = None;
#
#         self.previewArea = None;
#
#         self.error = None;
#
#         self.innerTrack = None;
#
#         self.outerTrack = None;
#
#         self.ang90 = None;
#         try:
#             self.innerStart = point3d_0;
#             self.innerEnd = point3d_1;
#             self.outerStart = point3d_2;
#             self.outerEnd = point3d_3;
#             point3d0 = [point3d_0, point3d_1, point3d_3, point3d_2 ];
#             self.selectionArea = Point3dCollection(point3d0);
#             if (MathHelper.smethod_132(self.selectionArea)):
#                 self.outerStart = point3d_3;
#                 self.outerEnd = point3d_2;
#                 self.selectionArea.set_Item(2, point3d_2);
#                 self.selectionArea.set_Item(3, point3d_3);
#             Point3dCollection.smethod_146(self.selectionArea);
#             if (self.selectionArea.get_Count() >= 3):
#                 self.method_0();
#             else:
#                 self.error = Messages.ERR_INVALID_POLYGON_AREA;
#         except:
#             eRRINVALIDPOLYGONAREA = Messages.ERR_INVALID_POLYGON_AREA;
#             str = eRRINVALIDPOLYGONAREA;
#             self.error = eRRINVALIDPOLYGONAREA;
#             self.error = str;
#             self.selectionArea = None;
#             self.previewArea = None;
#     def get_innerEnd(self):
#         return self.innerEnd
#     InnerEnd = property(get_innerEnd, None, None, None)
#
#     def get_innerStart(self):
#         return self.innerStart
#     InnerStart = property(get_innerStart, None, None, None)
#
#     def get_isValid(self):
#         return self.error == None or self.error == ""
#     IsValid = property(get_isValid, None, None, None)
#
#     def get_isValidIsValidForPreview(self):
#         return self.previewArea != None
#     IsValidIsValidForPreview = property(get_isValidIsValidForPreview, None, None, None)
#
#     def get_outerEnd(self):
#         return self.outerEnd
#     OuterEnd = property(get_outerEnd, None, None, None)
#
#     def get_outerStart(self):
#         return self.outerStart
#     OuterStart = property(get_outerStart, None, None, None)
#
#     def get_previewArea(self):
#         return self.previewArea
#     PreviewArea = property(get_previewArea, None, None, None)
#
#     def get_selectionArea(self):
#         return self.selectionArea
#     SelectionArea = property(get_selectionArea, None, None, None)
#
#     def imethod_0(self, point3d_0, double_0):
#         return MathHelper.pointInPolygon(self.selectionArea, point3d_0, double_0);
#
#     def imethod_1(self, point3d_0, double_0, double_1, double_2, returnList):
#         point3d = None;
#         point3d1 = None;
#         double_3 = None;
#         double_4 = None;
#         if (self.selectionArea != None and MathHelper.pointInPolygon(self.selectionArea, point3d_0, double_0)):
#             if (double_2 == None):
#                 double_2 = self.innerTrack;
#             pointList = []
#             # intersectionStatus_0 = MathHelper.smethod_34(self.innerStart, self.innerEnd, point3d_0, double_0, pointList)
#
#
#             if ( MathHelper.smethod_34(self.innerStart, self.innerEnd, point3d_0, double_0, pointList) != IntersectionStatus.Nothing and (MathHelper.smethod_110(point3d, self.innerStart, self.innerEnd) or MathHelper.smethod_110(point3d1, self.innerStart, self.innerEnd))):
#                 point3d = pointList[0]
#                 point3d1 = pointList[1]
#                 double_3 = double_1;
#                 returnList.append(double_3)
#                 returnList.append(double_4)
#                 return ObstacleAreaResult.Primary;
#             point3d2 = MathHelper.distanceBearingPoint(point3d_0, self.outerTrack + self.ang90, double_0);
#             if (MathHelper.smethod_40(self.selectionArea, point3d2)):
#                 point3d3 = MathHelper.distanceBearingPoint(point3d2, double_2 + self.ang90, 100);
#                 point3d = MathHelper.getIntersectionPoint(point3d2, point3d3, self.innerStart, self.innerEnd)
#                 if (point3d == None):
#                     returnList.append(None)
#                     returnList.append(Messages.ERR_NOMINAL_TRACK_PERPENDICULAR_INNER_OUTER)
#                     return ObstacleAreaResult.Secondary;
#                     # raise UserWarning , Messages.ERR_NOMINAL_TRACK_PERPENDICULAR_INNER_OUTER
#                 point3d1 = MathHelper.getIntersectionPoint(point3d2, point3d3, self.outerStart, self.outerEnd)
#                 if (point3d1 == None):
#                     returnList.append(None)
#                     returnList.append(Messages.ERR_NOMINAL_TRACK_PERPENDICULAR_INNER_OUTER)
#                     return ObstacleAreaResult.Secondary;
#                     # raise UserWarning , Messages.ERR_NOMINAL_TRACK_PERPENDICULAR_INNER_OUTER
#                 double_3 = double_1 * (1 - MathHelper.calcDistance(point3d2, point3d) / MathHelper.calcDistance(point3d1, point3d));
#                 double_4 = MathHelper.calcDistance(point3d2, point3d);
#                 returnList.append(double_3)
#                 returnList.append(double_4)
#                 return ObstacleAreaResult.Secondary;
#             double1 = -1;
#             num = -1;
#             num1 = -1;
#             num2 = -1;
#             pointList = []
#             # intersectionStatus_0 = MathHelper.smethod_34(self.innerStart, self.outerStart, point3d_0, double_0, pointList)
#
#             if (self.innerStart != self.outerStart and  MathHelper.smethod_34(self.innerStart, self.outerStart, point3d_0, double_0, pointList) != IntersectionStatus.Nothing):
#                 point3d = pointList[0]
#                 point3d1 = pointList[1]
#                 point3d2 = None
#                 if (not MathHelper.smethod_115(point3d_0, self.innerStart, self.innerEnd)):
#                     point3d2 = point3d1 if(not MathHelper.smethod_119(point3d, self.innerStart, self.innerEnd)) else point3d;
#                 else:
#                     point3d2 = point3d1 if(not MathHelper.smethod_115(point3d, self.innerStart, self.innerEnd)) else point3d;
#                 point3d4 = MathHelper.distanceBearingPoint(point3d2, double_2 + self.ang90, 100);
#                 point3d = MathHelper.getIntersectionPoint(point3d2, point3d4, self.innerStart, self.innerEnd)
#                 point3d1 = MathHelper.getIntersectionPoint(point3d2, point3d4, self.outerStart, self.outerEnd)
#                 if (point3d != None and point3d1 != None):
#                     double1 = double_1 * (1 - MathHelper.calcDistance(point3d2, point3d) / MathHelper.calcDistance(point3d1, point3d));
#                     num1 = MathHelper.calcDistance(point3d2, point3d);
#             pointList = []
#             # intersectionStatus_0 = MathHelper.smethod_34(self.innerEnd, self.outerEnd, point3d_0, double_0, pointList)
#
#             if (self.innerEnd != self.outerEnd and  MathHelper.smethod_34(self.innerEnd, self.outerEnd, point3d_0, double_0, pointList) != IntersectionStatus.Nothing):
#                 point3d = pointList[0]
#                 point3d1 = pointList[1]
#                 if (not MathHelper.smethod_115(point3d_0, self.innerStart, self.innerEnd)):
#                     point3d2 = point3d1 if(not MathHelper.smethod_119(point3d, self.innerStart, self.innerEnd)) else point3d;
#                 else:
#                     point3d2 = point3d1 if(not MathHelper.smethod_115(point3d, self.innerStart, self.innerEnd)) else point3d;
#                 point3d5 = MathHelper.distanceBearingPoint(point3d2, double_2 + self.ang90, 100);
#                 point3d1 = MathHelper.getIntersectionPoint(point3d2, point3d5, self.outerStart, self.outerEnd)
#                 point3d = MathHelper.getIntersectionPoint(point3d2, point3d5, self.innerStart, self.innerEnd)
#                 if (point3d != None and point3d1 != None ):
#                     num = double_1 * (1 - MathHelper.calcDistance(point3d2, point3d) / MathHelper.calcDistance(point3d1, point3d));
#                     num2 = MathHelper.calcDistance(point3d2, point3d);
#             if (double1 > 0 or num > 0):
#                 if (double1 <= num):
#                     double_3 = num;
#                     double_4 = num2;
#                 else:
#                     double_3 = double1;
#                     double_4 = num1;
#                 returnList.append(double_3)
#                 returnList.append(double_4)
#                 return ObstacleAreaResult.Secondary;
#         return ObstacleAreaResult.Outside;
#     def method_0(self):
#         point3d = None;
#         self.innerTrack = MathHelper.getBearing(self.innerStart, self.innerEnd);
#         self.outerTrack = MathHelper.getBearing(self.outerStart, self.outerEnd);
#         if (self.innerStart.smethod_170(self.innerEnd)):
#             self.innerEnd = MathHelper.distanceBearingPoint(self.innerStart, self.outerTrack, 1);
#             self.innerTrack = self.outerTrack;
#         if (self.outerStart.smethod_170(self.outerEnd)):
#             self.outerEnd = MathHelper.distanceBearingPoint(self.outerStart, self.innerTrack, 1);
#             self.outerTrack = self.innerTrack;
#         if (MathHelper.smethod_132(self.selectionArea)):
#             self.error = Messages.ERR_COMPLEX_POLYGON_SELECTED;
#             return;
#         if (MathHelper.smethod_65(self.selectionArea) == TurnDirection.Nothing):
#             self.error = Messages.ERR_INVALID_POLYGON_AREA;
#             return;
#         point3d1 = MathHelper.distanceBearingPoint(self.innerStart, self.innerTrack + 1.5707963267949, 100);
#         point3d = MathHelper.getIntersectionPoint(self.innerStart, point3d1, self.outerStart, self.outerEnd)
#         if (point3d == None):
#             self.error = Messages.ERR_INNER_OUTER_PERPENDICULAR;
#             return;
#         self.previewArea = PolylineArea(self.selectionArea);
#         if (MathHelper.smethod_128(self.outerStart, self.outerEnd, self.innerStart, self.innerEnd)):
#             self.ang90 = -1.5707963267949;
#             return;
#         self.ang90 = 1.5707963267949;
class SecondaryAreaStraight(ISecondaryArea):
    def __init__(self, point3d_0, point3d_1, point3d_2, point3d_3):
        '''
        public SecondaryAreaStraight(Point3d point3d_0, Point3d point3d_1, Point3d point3d_2, Point3d point3d_3)
        '''
        self.innerStart = point3d_0;
        self.innerEnd = point3d_1;
        self.outerStart = point3d_2;
        self.outerEnd = point3d_3;
        self.PreviewArea = None
        point3d0 = [point3d_0, point3d_1, point3d_3, point3d_2 ];
        self.selectionArea = Point3dCollection(point3d0);
        self.error = None
        # if (MathHelper.smethod_132(self.selectionArea)):
        #     self.outerStart = point3d_3;
        #     self.outerEnd = point3d_2;
        #     self.selectionArea.set_Item(2, point3d_2);
        #     self.selectionArea.set_Item(3, point3d_3);
        # self.selectionArea.smethod_146();
        # if (self.selectionArea.get_Count() >= 3):
        #     self.method_0();
        # else:
        #     self.error = Messages.ERR_INVALID_POLYGON_AREA;
        self.method_0()

    def getArea(self):
        return [self.innerStart, self.innerEnd, self.outerEnd, self.outerStart]

    def imethod_0(self, point3d_0, double_0):
        '''
        check fall the point in self area
        '''
        return QgisHelper.pointInPolygon(point3d_0, self.getArea)


    def imethod_1(self, point3d_0, double_0, double_1, double_2, returnList):
        '''
        ObstacleAreaResult imethod_1(Point3d point3d_0, double double_0, double double_1, double double_2, out double double_3, out double double_4);
        '''
        if double_2 == None:
            double_2 = self.innerTrack
        resultList = []
        if MathHelper.smethod_34(self.innerStart, self.innerEnd, point3d_0, double_0, resultList) != "None":
            point3d = resultList[0]
            point3d1 = resultList[1]
            if MathHelper.smethod_110(point3d, self.innerStart, self.innerEnd) or MathHelper.smethod_110(point3d1, self.innerStart, self.innerEnd):
                returnList.append(double_1)
                returnList.append(None)
                if len(returnList) < 2:
                    return ObstacleAreaResult.Outside
                return ObstacleAreaResult.Primary
        point3d2 = MathHelper.distanceBearingPoint(point3d_0, self.outerTrack + self.ang90, double_0);
        if MathHelper.smethod_40(self.getArea(), point3d2):
            point3d3 = None
            try:
                point3d3 = MathHelper.distanceBearingPoint(point3d2, double_2 + self.ang90, 100)
            except:
                pass
            point3d = MathHelper.getIntersectionPoint(point3d2, point3d3, self.innerStart, self.innerEnd)
            if point3d == None :
                returnList.append(None)
                returnList.append(Messages.ERR_NOMINAL_TRACK_PERPENDICULAR_INNER_OUTER)
                return ObstacleAreaResult.Secondary
                # raise UserWarning , Messages.ERR_NOMINAL_TRACK_PERPENDICULAR_INNER_OUTER
            point3d1 = MathHelper.getIntersectionPoint(point3d2, point3d3, self.outerStart, self.outerEnd)
            if point3d1 == None:
                returnList.append(None)
                returnList.append(Messages.ERR_NOMINAL_TRACK_PERPENDICULAR_INNER_OUTER)
                return ObstacleAreaResult.Secondary
                # raise UserWarning, Messages.ERR_NOMINAL_TRACK_PERPENDICULAR_INNER_OUTER
            double_3 = double_1 * (1 - MathHelper.calcDistance(point3d2, point3d) / MathHelper.calcDistance(point3d1, point3d));
            double_4 = MathHelper.calcDistance(point3d2, point3d)
            returnList.append(double_3)
            returnList.append(double_4)
            if len(returnList) < 2:
                return ObstacleAreaResult.Outside
            return ObstacleAreaResult.Secondary

        double1 = -1
        num = -1
        num1 = -1
        num2 = -1
        resultList = []
        if MathHelper.smethod_34(self.innerStart, self.outerStart, point3d_0, double_0, resultList) != "None":
            point3d = resultList[0]
            point3d1 = resultList[1]
            if self.innerStart != self.outerStart:
                if not MathHelper.smethod_115(point3d_0, self.innerStart, self.innerEnd):
                    if not MathHelper.smethod_119(point3d, self.innerStart, self.innerEnd):
                        point3d2 = point3d1
                    else:
                        point3d2 = point3d
                else:
                    if not MathHelper.smethod_115(point3d, self.innerStart, self.innerEnd):
                        point3d2 = point3d1
                    else:
                        point3d2 = point3d
                point3d4 = MathHelper.distanceBearingPoint(point3d2, double_2 + self.ang90, 100)
                point3d = MathHelper.getIntersectionPoint(point3d2, point3d4, self.innerStart, self.innerEnd)
                point3d1 = MathHelper.getIntersectionPoint(point3d2, point3d4, self.outerStart, self.outerEnd)
                if point3d != None and point3d1 != None:
                    double1 = double_1 * (1 - MathHelper.calcDistance(point3d2, point3d) / MathHelper.calcDistance(point3d1, point3d))
                    num1 = MathHelper.calcDistance(point3d2, point3d)
        resultList = []
        if MathHelper.smethod_34(self.innerEnd, self.outerEnd, point3d_0, double_0, resultList) != "None":
            point3d = resultList[0]
            point3d1 = resultList[1]
            if self.innerEnd != self.outerEnd:
                if not MathHelper.smethod_115(point3d_0, self.innerStart, self.innerEnd):
                    if MathHelper.smethod_119(point3d, self.innerStart, self.innerEnd) :
                        point3d2 = point3d1
                    else:
                        point3d2 = point3d
                else:
                    if not MathHelper.smethod_115(point3d, self.innerStart, self.innerEnd):
                        point3d2 = point3d1
                    else:
                        point3d2 = point3d
                point3d5 = MathHelper.distanceBearingPoint(point3d2, double_2 + self.ang90, 100)
                point3d = MathHelper.getIntersectionPoint(point3d2, point3d5, self.innerStart, self.innerEnd)
                point3d1 = MathHelper.getIntersectionPoint(point3d2, point3d5, self.outerStart, self.outerEnd)
                if point3d != None and point3d1 != None:
                    num = double_1 * (1 - MathHelper.calcDistance(point3d2, point3d) / MathHelper.calcDistance(point3d1, point3d))
                    num2 = MathHelper.calcDistance(point3d2, point3d)
        if (double1 > 0 or num > 0):
            if (double1 <= num):
                double_3 = num
                double_4 = num2
            else:
                double_3 = double1
                double_4 = num1
            resultList.append(double_3)
            resultList.append(double_4)
            if len(resultList) < 2:
                return ObstacleAreaResult.Outside
            return ObstacleAreaResult.Secondary
        return ObstacleAreaResult.Outside
    def method_0(self):
        self.innerTrack = MathHelper.getBearing(self.innerStart, self.innerEnd)
        self.outerTrack = MathHelper.getBearing(self.outerStart, self.outerEnd)
        if self.innerStart.smethod_170(self.innerEnd):
            self.innerEnd = MathHelper.distanceBearingPoint(self.innerStart, self.outerTrack, 1)
            self.innerTrack = self.outerTrack;
        if self.outerStart.smethod_170(self.outerEnd):
            self.outerEnd = MathHelper.distanceBearingPoint(self.outerStart, self.innerTrack, 1)
            self.outerTrack = self.innerTrack
#         if MathHelper.smethod_132(self.getArea()):
#             self.error = "ERR_COMPLEX_POLYGON_SELECTED"
#             return
#         if MathHelper.smethod_65(self.selectionArea) == "None":
#             self.error = "ERR_INVALID_POLYGON_AREA"
#             return
        point3d1 = MathHelper.distanceBearingPoint(self.innerStart, self.innerTrack + 1.5707963267949, 100)
        point3d = MathHelper.getIntersectionPoint(self.innerStart, point3d1, self.outerStart, self.outerEnd)
        if point3d == None:
            self.error = "ERR_INNER_OUTER_PERPENDICULAR"
            return
        self.PreviewArea = PolylineArea(self.selectionArea);
        if MathHelper.smethod_128(self.outerStart, self.outerEnd, self.innerStart, self.innerEnd):
            self.ang90 = -1.5707963267949
            return
        self.ang90 = 1.5707963267949;

    def ToString(self):
        if (self.error == None or self.error == ""):
            return Messages.SECONDARY_AREA_STRAIGHT;
        return self.error;

    def get_SelectionArea(self):
        return self.selectionArea
    SelectionArea = property(get_SelectionArea, None, None, None)

    def isValidForPreview(self):
        return self.PreviewArea != None;
    IsValidForPreview = property(isValidForPreview, None, None, None)

    def isValid(self):
        return self.error == None or self.error == ""
    IsValid = property(isValid, None, None, None)
class SecondaryAreaArc(ISecondaryArea):
    def __init__(self, point3d_0, point3d_1, point3d_2, point3d_3, point3d_4, point3d_5, innerR = None, outerR = None):
        num = MathHelper.smethod_60(point3d_0, point3d_1, point3d_2)
        num1 = MathHelper.smethod_60(point3d_3, point3d_4, point3d_5)
        turnDirection = MathHelper.smethod_7(num)
        turnDirection1 = MathHelper.smethod_7(num1)
        self.InnerStart = point3d_0
        self.InnerEnd = point3d_2
        self.InnerMiddle = point3d_1
        self.OuterMiddle = point3d_4
        self.error = None

        polylineArea = PolylineArea()
        polylineArea.Add(PolylineAreaPoint(self.InnerStart, num))
        polylineArea.Add(PolylineAreaPoint(self.InnerEnd))
        self.innerPointCount = len(polylineArea.method_14())
        polylineArea = PolylineArea()
        polylineArea.Add(PolylineAreaPoint(point3d_3, num1))
        polylineArea.Add(PolylineAreaPoint(point3d_5))
        self.outerPointCount = len(polylineArea.method_14())

        if (turnDirection != turnDirection1):
            point3dCollection = [point3d_0, point3d_1, point3d_2, point3d_3, point3d_4, point3d_5]
            self.OuterStart = point3d_5
            self.OuterEnd = point3d_3
        else:
            point3dCollection1 = [point3d_0, point3d_1, point3d_2, point3d_5, point3d_4, point3d_3]
#             = new Point3dCollection(point3dArray);
            self.OuterStart = point3d_3
            self.OuterEnd = point3d_5
        
        self.selectionArea = []
        self.innerBulge = None
        self.outerBulge = None
        self.PreviewArea = None
        if innerR != None:
            self.innerBulge = innerR
            self.outerBulge = outerR
        self.method_0(point3d_1, point3d_4)

    def getArea(self):
        return self.selectionArea
    SelectionArea = property(getArea, None, None, None)
    def imethod_0(self, point3d_0, double_0):
        return MathHelper.pointInPolygon(self.selectionArea, point3d_0, double_0);

    def imethod_1(self, point3d_0, double_0, double_1, double_2, result2):
        if len(self.selectionArea) > 2 and (MathHelper.pointInPolygon(self.selectionArea, point3d_0, double_0)):
            if (self.innerRadius >= self.outerRadius):
                double0 = MathHelper.calcDistance(self.center, point3d_0) + double_0
                if (double0 >= self.innerRadius):
                    double0 = double0 - 2 * double_0
                    if (double0 <= self.innerRadius):
                        result2.append(double_1)
                        result2.append(None)
#                         double_3 = double_1;
                        return ObstacleAreaResult.Secondary
                elif (double0 >= self.outerRadius):
                    point3d4 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(self.center, point3d_0), double_0)
                    if (MathHelper.smethod_40(self.selectionArea, point3d4)):
                        double_3 = double_1 * (1 - (self.innerRadius - double0) / (self.innerRadius - self.outerRadius))
                        double_4 = self.innerRadius - double0;
                        result2.append(double_3)
                        result2.append(double_4)
                        return ObstacleAreaResult.Secondary
                    return2 = []
                    if (MathHelper.smethod_34(self.InnerStart, self.OuterStart, point3d_0, double_0, return2) != IntersectionStatus.Nothing):
                        point3d2 = return2[0]
                        point3d3 = return2[1]
                        if (MathHelper.smethod_110(point3d2, self.InnerStart, self.OuterStart)):
                            double0 = MathHelper.calcDistance(self.center, point3d2);
                        elif (MathHelper.smethod_110(point3d3, self.InnerStart, self.OuterStart)):
                            double0 = MathHelper.calcDistance(self.center, point3d3);
                        double_3 = double_1 * (1 - (self.innerRadius - double0) / (self.innerRadius - self.outerRadius));
                        double_4 = self.innerRadius - double0;
                        result2.append(double_3)
                        result2.append(double_4)
                        return ObstacleAreaResult.Secondary

                    return2 = []
                    if (MathHelper.smethod_34(self.InnerEnd, self.OuterEnd, point3d_0, double_0, return2) != IntersectionStatus.Nothing):
                        point3d2 = return2[0]
                        point3d3 = return2[1] 
                        if (MathHelper.smethod_110(point3d2, self.InnerEnd, self.OuterEnd)):
                            double0 = MathHelper.calcDistance(self.center, point3d2);
                        elif (MathHelper.smethod_110(point3d3, self.InnerEnd, self.OuterEnd)):
                            double0 = MathHelper.calcDistance(self.center, point3d3);
                        double_3 = double_1 * (1 - (self.innerRadius - double0) / (self.innerRadius - self.outerRadius));
                        double_4 = self.innerRadius - double0;
                        result2.append(double_3)
                        result2.append(double_4)
                        return ObstacleAreaResult.Secondary

            else:
                num = MathHelper.calcDistance(self.center, point3d_0) - double_0;
                if (num <= self.innerRadius):
                    num = num + 2 * double_0
                    if (num >= self.innerRadius):
                        double_3 = double_1
                        result2.append(double_3)
                        result2.append(None)
                        return ObstacleAreaResult.Primary

                elif (num <= self.outerRadius):
                    point3d5 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, self.center), double_0)
                    if (MathHelper.smethod_40(self.selectionArea, point3d5)):
                        double_3 = double_1 * (1 - (num - self.innerRadius) / (self.outerRadius - self.innerRadius));
                        double_4 = num - self.innerRadius;
                        result2.append(double_3)
                        result2.append(double_4)
                        return ObstacleAreaResult.Secondary
                    
                    return2 = []
                    if (MathHelper.smethod_34(self.InnerStart, self.OuterStart, point3d_0, double_0, return2) != IntersectionStatus.Nothing):
                        point3d = return2[0]
                        point3d1 = return2[1] 
                        if (MathHelper.smethod_110(point3d, self.InnerStart, self.OuterStart)):
                            num = MathHelper.calcDistance(self.center, point3d);
                        elif (MathHelper.smethod_110(point3d1, self.InnerStart, self.OuterStart)):
                            num = MathHelper.calcDistance(self.center, point3d1);
                        double_3 = double_1 * (1 - (num - self.innerRadius) / (self.outerRadius - self.innerRadius))
                        double_4 = num - self.innerRadius
                        result2.append(double_3)
                        result2.append(double_4)
                        return ObstacleAreaResult.Secondary
                    return2 = []
                    if (MathHelper.smethod_34(self.InnerEnd, self.OuterEnd, point3d_0, double_0, return2) != IntersectionStatus.Nothing):
                        point3d = return2[0]
                        point3d1 = return2[1] 
                        if (MathHelper.smethod_110(point3d, self.InnerEnd, self.OuterEnd)):
                            num = MathHelper.calcDistance(self.center, point3d);
                        elif (MathHelper.smethod_110(point3d1, self.InnerEnd, self.OuterEnd)):
                            num = MathHelper.calcDistance(self.center, point3d1);
                        double_3 = double_1 * (1 - (num - self.innerRadius) / (self.outerRadius - self.innerRadius));
                        double_4 = num - self.innerRadius;
                        result2.append(double_3)
                        result2.append(double_4)
                        return ObstacleAreaResult.Secondary

        return ObstacleAreaResult.Outside;

    def method_0(self, point3d_0, point3d_1):
        num = MathHelper.smethod_60(self.InnerStart, point3d_0, self.InnerEnd);
        num1 = MathHelper.smethod_60(self.OuterStart, point3d_1, self.OuterEnd);
        turnDirection = MathHelper.smethod_7(num);
        turnDirection1 = MathHelper.smethod_7(num1);
        self.center = MathHelper.smethod_71(self.InnerStart, self.InnerEnd, num)
        point3d = MathHelper.smethod_71(self.OuterStart, self.OuterEnd, num1)

        if (not MathHelper.smethod_103(self.center, point3d, 0.1)):
            if self.innerBulge != self.outerBulge:
                self.error = Messages.ERR_INNER_OUTER_CENTER;
                return;

        self.innerRadius = MathHelper.calcDistance(self.center, point3d_0);
        self.outerRadius = MathHelper.calcDistance(self.center, point3d_1);
        if (MathHelper.smethod_99(self.outerRadius, self.innerRadius, 1)):
            self.error = Messages.ERR_INNER_OUTER_RADIUS;
            return;

        num1 = MathHelper.smethod_60(self.OuterEnd, point3d_1, self.OuterStart);
        turnDirection1 = MathHelper.smethod_66(num1);
        num2 = MathHelper.smethod_5(num);
        num3 = MathHelper.smethod_5(num1);
        self.selectionArea = []
        if (self.innerRadius >= self.outerRadius):
            self.selectionArea.extend(MathHelper.smethod_138(self.InnerStart, self.center, self.innerRadius, num2, 3, turnDirection));
            self.selectionArea.append(self.InnerEnd);
            self.selectionArea.extend(MathHelper.smethod_137(self.OuterEnd, self.center, self.outerRadius, num3, 3, turnDirection1));
            self.selectionArea.append(self.OuterStart);
        else:
            self.selectionArea.extend(MathHelper.smethod_137(self.InnerStart, self.center, self.innerRadius, num2, 3, turnDirection));
            self.selectionArea.append(self.InnerEnd);
            self.selectionArea.extend(MathHelper.smethod_138(self.OuterEnd, self.center, self.outerRadius, num3, 3, turnDirection1))
            self.selectionArea.append(self.OuterStart)

#         self.selectionArea.smethod_146();
        if (len(self.selectionArea) < 3):
            self.error = Messages.ERR_INVALID_ARC_AREA;
            return;
        # if (MathHelper.smethod_132(self.selectionArea)):
        #     self.error = Messages.ERR_INVALID_ARC_AREA;
        #     return;
        self.PreviewArea = PolylineArea()
        self.PreviewArea.append(PolylineAreaPoint(self.InnerStart, MathHelper.smethod_60(self.InnerStart, point3d_0, self.InnerEnd)))
        self.PreviewArea.append(PolylineAreaPoint(self.InnerEnd))
        self.PreviewArea.append(PolylineAreaPoint(self.OuterEnd, MathHelper.smethod_60(self.OuterEnd, point3d_1, self.OuterStart)))
        self.PreviewArea.append(PolylineAreaPoint(self.OuterStart))


    def ToString(self):
        if (self.error == None):
            return Messages.SECONDARY_AREA_ARC;
        return self.error;
    def isValidForPreview(self):
        return self.PreviewArea != None;
    IsValidForPreview = property(isValidForPreview, None, None, None)

    def isValid(self):
        return self.error == None or self.error == ""
    IsValid = property(isValid, None, None, None)
class SecondaryAreaPie(ISecondaryArea):

    def __init__(self, point3d_0, point3d_1, point3d_2):
        self.error = None
        num = MathHelper.smethod_60(point3d_0, point3d_1, point3d_2)
        self.center = MathHelper.smethod_71(point3d_0, point3d_2, num)
        self.radius = MathHelper.calcDistance(self.center, point3d_1)

        polylineArea = PolylineArea()
        polylineArea.Add(PolylineAreaPoint(self.point3d_0, num))
        polylineArea.Add(PolylineAreaPoint(self.point3d_2))
        pointCount = len(polylineArea.method_14())

        num1 = MathHelper.smethod_5(num)
        turnDirection = MathHelper.smethod_7(num)
        self.SelectionArea = []
        self.SelectionArea.append(self.center)
        self.SelectionArea.extend(MathHelper.smethod_138(point3d_0, self.center, self.radius, num1, 3, turnDirection));
        self.SelectionArea.append(point3d_2);
#         self.SelectionArea.smethod_146();
        if (MathHelper.smethod_132(self.SelectionArea)):
            self.error = Messages.ERR_INVALID_PIE_AREA;
            return;
        self.Start = point3d_0;
        self.middle = point3d_1;
        self.end = point3d_2;
        self.PreviewArea = PolylineArea()
        self.PreviewArea.append(PolylineAreaPoint(self.center))
        self.PreviewArea.append(PolylineAreaPoint(point3d_0, num))
        self.PreviewArea.append(PolylineAreaPoint(point3d_2))
    def getArea(self):
        return self.SelectionArea

    def imethod_0(self, point3d_0, double_0):
        return MathHelper.pointInPolygon(self.SelectionArea, point3d_0, double_0);

    def imethod_1(self, point3d_0, double_0, double_1, double_2, result2):
        if (MathHelper.pointInPolygon(self.SelectionArea, point3d_0, double_0)):
            num = MathHelper.calcDistance(self.center, point3d_0) - double_0
            if (num <= 0):
                double_3 = double_1;
#                 result2 = []
                result2.append(double_3)
                result2.append(None)
                return ObstacleAreaResult.Primary;
            if (num <= self.radius):
                point3d2 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, self.center), double_0)
                if (MathHelper.smethod_40(self.SelectionArea, point3d2)):
                    double_3 = double_1 * (1 - num / self.radius);
                    double_4 = num
#                     result2 = []
                    result2.append(double_3)
                    result2.append(double_4)
                    return ObstacleAreaResult.Secondary;
                return2 = []
                if (MathHelper.smethod_34(self.center, self.Start, point3d_0, double_0, return2) != IntersectionStatus.Nothing):
                    point3d = return2[0]
                    point3d1 = return2[1] 
                    if (MathHelper.smethod_110(point3d, self.center, self.Start)):
                        num = MathHelper.calcDistance(self.center, point3d);
                    elif (MathHelper.smethod_110(point3d1, self.center, self.Start)):
                        num = MathHelper.calcDistance(self.center, point3d1)
                    double_3 = double_1 * (1 - num / self.radius);
                    double_4 = num
#                     result2 = []
                    result2.append(double_3)
                    result2.append(double_4)
                    return ObstacleAreaResult.Secondary;
                return2 = []
                if (MathHelper.smethod_34(self.center, self.end, point3d_0, double_0, return2) != IntersectionStatus.Nothing):
                    point3d = return2[0]
                    point3d1 = return2[1]
                    if (MathHelper.smethod_110(point3d, self.center, self.end)):
                        num = MathHelper.calcDistance(self.center, point3d);
                    elif (MathHelper.smethod_110(point3d1, self.center, self.end)):
                        num = MathHelper.calcDistance(self.center, point3d1);
                    double_3 = double_1 * (1 - num / self.radius);
                    double_4 = num;
                    return ObstacleAreaResult.Secondary;

        return ObstacleAreaResult.Outside;

    def ToString(self):
        if (self.error == None or self.error == ""):
            return Messages.SECONDARY_AREA_PIE;
        return self.error;
    def isValidForPreview(self):
        return self.PreviewArea != None;
    IsValidForPreview = property(isValidForPreview, None, None, None)

    def isValid(self):
        return self.error == None or self.error == ""
    IsValid = property(isValid, None, None, None)
class PrimarySecondaryObstacleArea(IObstacleArea):
    def __init__(self, primaryArea = None, secondaryArea1 = None, secondarayArea2 = None):
        self.obstacleArea = None
        self.selectionArea = None
        self.primaryArea = primaryArea
        self.secondaryArea1 = secondaryArea1
        self.secondaryArea2 = secondarayArea2
        self.nominalTrack = None
        self.error = Messages.ERR_NO_AREA_SELECTED
        self.isArc = False
    def pointInPolygon(self, point3d_0, double_0):
        if (self.obstacleArea != None and not self.obstacleArea.pointInArea(point3d_0, double_0)):
            return False;
        if (self.primaryArea.pointInArea(point3d_0, double_0)):
            return True;
        if (self.secondaryArea1.pointInArea(point3d_0, double_0)):
            return True;
        if (self.secondaryArea2.pointInArea(point3d_0, double_0)):
            return True;
        return False;

    def imethod_1(self, point3d_0, double_0, double_1, listOutPut):
        obstacleAreaResult = ObstacleAreaResult.Outside;
        double_2 = double_1;
        double_3 = None;
        if (self.obstacleArea != None and not self.obstacleArea.pointInArea(point3d_0, double_0)):
            listOutPut.append(double_2)
            listOutPut.append(double_3)
            return ObstacleAreaResult.Outside;
        obstacleAreaResult = self.primaryArea.imethod_1(point3d_0, double_0, double_1, listOutPut);
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            return obstacleAreaResult;
        obstacleAreaResult = self.secondaryArea1.imethod_1(point3d_0, double_0, double_1, listOutPut);
        if (obstacleAreaResult != ObstacleAreaResult.Outside):
            return obstacleAreaResult;
        obstacleAreaResult = self.secondaryArea2.imethod_1(point3d_0, double_0, double_1, listOutPut);
        return obstacleAreaResult;

    # def set_areas(self, pointArrayIn0, pointArrayOut0, pointArrayIn1, pointArrayOut1):
    #     if len(pointArrayIn0) == 2 and len(pointArrayOut0) == 2 and len(pointArrayIn1) == 2 and len(pointArrayOut1) == 2:
    #         if len(pointArrayIn0) == 2 and len(pointArrayOut0) == 2:
    #             innerStartPoint = Point3D(pointArrayIn0[0].x(), pointArrayIn0[0].y())
    #             innerEndPoint = Point3D(pointArrayIn0[1].x(), pointArrayIn0[1].y())
    #             outerStartPoint = Point3D(pointArrayOut0[0].x(), pointArrayOut0[0].y())
    #             outerEndPoint = Point3D(pointArrayOut0[1].x(), pointArrayOut0[1].y())
    #             self.secondaryArea1 = SecondaryObstacleArea(innerStartPoint, innerEndPoint, outerStartPoint, outerEndPoint, MathHelper.getBearing(innerStartPoint, innerEndPoint))
    #         if len(pointArrayIn1) == 2 and len(pointArrayOut1) == 2:
    #             innerStartPoint = Point3D(pointArrayIn1[0].x(), pointArrayIn1[0].y())
    #             innerEndPoint = Point3D(pointArrayIn1[1].x(), pointArrayIn1[1].y())
    #             outerStartPoint = Point3D(pointArrayOut1[0].x(), pointArrayOut1[0].y())
    #             outerEndPoint = Point3D(pointArrayOut1[1].x(), pointArrayOut1[1].y())
    #             self.secondaryArea2 = SecondaryObstacleArea(innerStartPoint, innerEndPoint, outerStartPoint, outerEndPoint, MathHelper.getBearing(innerStartPoint, innerEndPoint))
    #
    #         if len(pointArrayIn1) == 2 and len(pointArrayIn0) == 2:
    #             innerStartPoint = Point3D(pointArrayIn1[0].x(), pointArrayIn1[0].y())
    #             innerEndPoint = Point3D(pointArrayIn1[1].x(), pointArrayIn1[1].y())
    #             outerStartPoint = Point3D(pointArrayIn0[0].x(), pointArrayIn0[0].y())
    #             outerEndPoint = Point3D(pointArrayIn0[1].x(), pointArrayIn0[1].y())
    #             self.primaryArea = PrimaryObstacleArea(PolylineArea([innerStartPoint, innerEndPoint, outerEndPoint, outerStartPoint]))
    #         if len(pointArrayOut0) == 2 and len(pointArrayOut1) == 2:
    #             innerStartPoint = Point3D(pointArrayOut0[0].x(), pointArrayOut0[0].y())
    #             innerEndPoint = Point3D(pointArrayOut0[1].x(), pointArrayOut0[1].y())
    #             outerStartPoint = Point3D(pointArrayOut1[0].x(), pointArrayOut1[0].y())
    #             outerEndPoint = Point3D(pointArrayOut1[1].x(), pointArrayOut1[1].y())
    #             self.selectionArea = [innerStartPoint, innerEndPoint, outerEndPoint, outerStartPoint]
    #         self.isArc = False
    #         self.error = None
    #     elif len(pointArrayIn0) > 2 and len(pointArrayOut0) > 2 and len(pointArrayIn1) > 2 and len(pointArrayOut1) > 2:
    #         #Calculate secondaryArea1
    #         innerStartPoint = Point3D(pointArrayIn0[0].x(), pointArrayIn0[0].y())
    #         innerEndPoint = Point3D(pointArrayIn0[len(pointArrayIn0) - 1].x(), pointArrayIn0[len(pointArrayIn0) - 1].y())
    #         num = int(len(pointArrayIn0) / 2)
    #         innerMiddlePoint = Point3D(pointArrayIn0[num].x(), pointArrayIn0[num].y())
    #         outerStartPoint = Point3D(pointArrayOut0[0].x(), pointArrayOut0[0].y())
    #         outerEndPoint = Point3D(pointArrayOut0[len(pointArrayOut0) - 1].x(), pointArrayOut0[len(pointArrayOut0) - 1].y())
    #         outerMiddlePoint = Point3D(pointArrayOut0[num].x(), pointArrayOut0[num].y())
    #         self.secondaryArea1 = SecondaryObstacleArea(innerStartPoint, innerMiddlePoint, innerEndPoint, outerStartPoint, None, outerMiddlePoint, outerEndPoint)
    #
    #      #Calculate secondaryArea2
    #         innerStartPoint = Point3D(pointArrayIn1[0].x(), pointArrayIn1[0].y())
    #         innerEndPoint = Point3D(pointArrayIn1[len(pointArrayIn1) - 1].x(), pointArrayIn1[len(pointArrayIn1) - 1].y())
    #         num = int(len(pointArrayIn1) / 2)
    #         innerMiddlePoint = Point3D(pointArrayIn1[num].x(), pointArrayIn1[num].y())
    #
    #         outerStartPoint = Point3D(pointArrayOut1[0].x(), pointArrayOut1[0].y())
    #         outerEndPoint = Point3D(pointArrayOut1[len(pointArrayOut1) - 1].x(), pointArrayOut1[len(pointArrayOut1) - 1].y())
    #         outerMiddlePoint = Point3D(pointArrayOut1[num].x(), pointArrayOut1[num].y())
    #
    #         self.secondaryArea2 = SecondaryObstacleArea(innerStartPoint, innerMiddlePoint, innerEndPoint, outerMiddlePoint, None, outerStartPoint, outerEndPoint)
    #
    #         #  Calculate primaryArea
    #         innerStartPoint = Point3D(pointArrayIn1[0].x(), pointArrayIn1[0].y())
    #         innerEndPoint = Point3D(pointArrayIn1[1].x(), pointArrayIn1[1].y())
    #         outerStartPoint = Point3D(pointArrayIn0[0].x(), pointArrayIn0[0].y())
    #         outerEndPoint = Point3D(pointArrayIn0[1].x(), pointArrayIn0[1].y())
    #         num = int(len(pointArrayIn1) / 2)
    #         innerMiddlePoint = Point3D(pointArrayIn1[num].x(), pointArrayIn1[num].y())
    #         bulge0 = MathHelper.smethod_60(innerStartPoint, innerMiddlePoint, innerEndPoint)
    #         outerMiddlePoint = Point3D(pointArrayIn0[num].x(), pointArrayIn0[num].y())
    #         bulge1 = MathHelper.smethod_60(outerEndPoint, outerMiddlePoint, outerStartPoint)
    #         polylineArea = PolylineArea()
    #
    #         polylineArea.Add(PolylineAreaPoint(innerStartPoint, bulge0))
    #         polylineArea.Add(PolylineAreaPoint(innerEndPoint))
    #         polylineArea.Add(PolylineAreaPoint(outerEndPoint, bulge1))
    #         polylineArea.Add(PolylineAreaPoint(outerStartPoint))
    #         self.primaryArea = PrimaryObstacleArea(polylineArea)
    #         # if len(pointArrayOut0) == 2 and len(pointArrayOut1) == 2:
    #         #     innerStartPoint = Point3D(pointArrayOut0[0].x(), pointArrayOut0[0].y())
    #         #     innerEndPoint = Point3D(pointArrayOut0[1].x(), pointArrayOut0[1].y())
    #         #     outerStartPoint = Point3D(pointArrayOut1[0].x(), pointArrayOut1[0].y())
    #         #     outerEndPoint = Point3D(pointArrayOut1[1].x(), pointArrayOut1[1].y())
    #         #     self.selectionArea = [innerStartPoint, innerEndPoint, outerEndPoint, outerStartPoint]
    #         self.isArc = True
    #         self.error = None
    def ToString(self):
        if (not self.IsValid):
            return self.error;
        if (not self.IsArc):
            return Messages.PRIMARY_AND_SECONDARY_AREA_STRAIGHT;
        return Messages.PRIMARY_AND_SECONDARY_AREA_ARC;

    def get_IsValid(self):
        if (self.primaryArea != None and self.primaryArea.IsValid):
            return True;
        if (self.secondaryArea1 != None and self.secondaryArea1.IsValid):
            return True;
        if (self.secondaryArea2 != None and self.secondaryArea2.IsValid):
            return True;
        return False;
    IsValid = property(get_IsValid, None, None, None)

    def get_IsValidForPreview(self):
        if (self.primaryArea != None and self.primaryArea.IsValidForPreview):
            return True;
        if (self.secondaryArea1 != None and self.secondaryArea1.IsValidForPreview):
            return True;
        if (self.secondaryArea2 != None and self.secondaryArea2.IsValidForPreview):
            return True;
        return False;
    IsValidForPreview = property(get_IsValidForPreview, None, None, None)

    def get_NominalTrack(self):
        return self.nominalTrack
    def set_NominalTrack(self, value):
        self.nominalTrack = value;
        if (self.secondaryArea1 != None):
            self.secondaryArea1.NominalTrack = value;
        if (self.secondaryArea2 != None):
            self.secondaryArea2.NominalTrack = value;
    NominalTrack = property(get_NominalTrack, set_NominalTrack, None, None)

    def get_ObstacleArea(self):
        if (self.obstacleArea != None):
            return self.obstacleArea;
        if (self.selectionArea.get_Count() < 3):
            return None  #throw new InvalidOperationException(Messages.ERR_MINIMUM_3_AREA_POINTS);
        return PrimaryObstacleArea(PolylineArea(self.selectionArea));
    def set_ObstacleArea(self, value):
        self.obstacleArea = value
    ObstacleArea = property(get_ObstacleArea, set_ObstacleArea, None, None)

    def get_SelectionArea(self):
        if (self.obstacleArea != None):
            return self.obstacleArea.SelectionArea;
        if (len(self.selectionArea) < 3):
            return None #throw new InvalidOperationException(Messages.ERR_MINIMUM_3_AREA_POINTS);
        return self.selectionArea;
    SelectionArea = property(get_SelectionArea, None, None, None)

    def get_IsArc(self):
        if self.primaryArea.IsArc and self.secondaryArea1.IsArc and self.secondaryArea2.IsArc:
            self.isArc = True
            return True
        return False