
from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QGis

from FlightPlanner.helpers import MathHelper
from FlightPlanner.Obstacle.ObstacleArea import SecondaryObstacleArea
from FlightPlanner.types import Point3D, ObstacleAreaResult
import define

class BaroVnavFasSegment:
    def __init__(self):
        
        # Point3D
        self.ptStart = None
        # Point3D
        self.ptEnd = None
        # double
        self.moc = 0.0
        # double
        self.tanafas = 0.0
        # double 
        self.xfas = 0.0
        # double 
        self.xstart = 0.0
        # double 
        self.xend = 0.0

class IBaroVnavSurface:
    def __init__(self):
        # protected BaroVNAV.BaroVnavSurfaceType Type;
        self.Type = ""
        # protected Point3dCollection selectionArea;
        self.selectionArea = []
        # protected PrimaryObstacleArea primaryArea;
        self.primaryArea = []
        # protected List<SecondaryObstacleArea> secondaryAreas;
        self.secondaryAreas = []
        # protected Point3dCollection linesl;
        self.linesl = []
        # protected Point3dCollection linepl;
        self.linepl = []
        #protected Point3dCollection linepr;
        self.linepr = []
        # protected Point3dCollection linesr;
        self.linesr = []
        # protected Point3d ptTHR;
        self.ptTHR = None
        # protected Point3d ptTHRm90;
        self.ptTHRm90 = None
        # protected Point3d ptEND;
        self.ptEND = None
        # protected double tr;
        self.tr = 0.0
        # protected double tr180;
        self.tr180 = 0.0
        # protected double trp90;
        self.trp90 = 0.0
        # protected double trm90;
        self.trm90 = 0.0
        
    # public void method_0(Point3dCollection point3dCollection_0, Point3dCollection point3dCollection_1, Point3dCollection point3dCollection_2, Point3dCollection point3dCollection_3, Point3d point3d_0, Point3d point3d_1)
    def method_0(self, point3dCollection_0, point3dCollection_1, point3dCollection_2, point3dCollection_3, point3d_0, point3d_1):
        point3d = Point3D()
        point3d1 = Point3D()
        point3d2 = Point3D()
        point3d3 = Point3D()
        flag = False;
        flag1 = False;
        count = len(point3dCollection_0)
        num = 1;
        while (True):
            if (num < count):
                num1 = num - 1
                num2 = num
                if (num1 < 0):
                    num1 = num
                    num2 = num + 1
                if (flag == False and MathHelper.smethod_117(point3d_0, point3dCollection_3[num], point3dCollection_0[num], False)):
                    point3d4 = MathHelper.distanceBearingPoint(point3d_0, self.trm90, 100)
                    point3d = MathHelper.getIntersectionPoint(point3dCollection_0[num1], point3dCollection_0[num2], point3d_0, point3d4);
                    point3d1 = MathHelper.getIntersectionPoint(point3dCollection_1[num1], point3dCollection_1[num2], point3d_0, point3d4);
                    point3d2 = MathHelper.getIntersectionPoint(point3dCollection_2[num1], point3dCollection_2[num2], point3d_0, point3d4)
                    point3d3 = MathHelper.getIntersectionPoint(point3dCollection_3[num1], point3dCollection_3[num2], point3d_0, point3d4)
                    self.linesl.append(point3d.smethod_167(self.vmethod_3(point3d, True)))
                    self.linepl.append(point3d1.smethod_167(self.vmethod_3(point3d1, False)))
                    self.linepr.append(point3d2.smethod_167(self.vmethod_3(point3d2, False)))
                    self.linesr.append(point3d3.smethod_167(self.vmethod_3(point3d3, True)))
                    flag = True;
                if (flag1 or not MathHelper.smethod_117(point3d_1, point3dCollection_3[num], point3dCollection_0[num], False)):
                    if (flag and not flag1):
                        self.linesl.append(point3dCollection_0[num].smethod_167(self.vmethod_3(point3dCollection_0[num], True)));
                        self.linepl.append(point3dCollection_1[num].smethod_167(self.vmethod_3(point3dCollection_1[num], False)));
                        self.linepr.append(point3dCollection_2[num].smethod_167(self.vmethod_3(point3dCollection_2[num], False)));
                        self.linesr.append(point3dCollection_3[num].smethod_167(self.vmethod_3(point3dCollection_3[num], True)));
                    num += 1
                else:
                    point3d5 = MathHelper.distanceBearingPoint(point3d_1, self.trm90, 100);
                    point3d = MathHelper.getIntersectionPoint(point3dCollection_0[num1], point3dCollection_0[num2], point3d_1, point3d5)
                    point3d1 = MathHelper.getIntersectionPoint(point3dCollection_1[num1], point3dCollection_1[num2], point3d_1, point3d5)
                    point3d2 = MathHelper.getIntersectionPoint(point3dCollection_2[num1], point3dCollection_2[num2], point3d_1, point3d5)
                    point3d3 = MathHelper.getIntersectionPoint(point3dCollection_3[num1], point3dCollection_3[num2], point3d_1, point3d5)
                    self.linesl.append(point3d.smethod_167(self.vmethod_3(point3d, True)));
                    self.linepl.append(point3d1.smethod_167(self.vmethod_3(point3d1, False)));
                    self.linepr.append(point3d2.smethod_167(self.vmethod_3(point3d2, False)));
                    self.linesr.append(point3d3.smethod_167(self.vmethod_3(point3d3, True)));
                    flag1 = True;
                    break;
            else:
                break
        
#         if define._canvas.mapUnits() != QGis.Meters:
#             self.linesl = QgisHelper.transformPoints(self.linesl, True)
#             self.linepl = QgisHelper.transformPoints(self.linepl, True)
#             self.linepr = QgisHelper.transformPoints(self.linepr, True)
#             self.linesr = QgisHelper.transformPoints(self.linesr, True)
#             
            
        for point3d_enum in self.linepl:
            self.primaryArea.append(point3d_enum)
            
        self.linepr.reverse()
        for point3d_enum in self.linepr:
            self.primaryArea.append(point3d_enum)
        self.linepr.reverse()

#         for (int m = 1; m < self.linesl.get_Count(); m++)
#         {
#             self.secondaryAreas.append(new SecondaryObstacleArea(self.linepl[m - 1), self.linepl[m), self.linesl[m), self.linesl[m - 1), self.tr));
#             self.secondaryAreas.append(new SecondaryObstacleArea(self.linepr[m - 1), self.linepr[m), self.linesr[m), self.linesr[m - 1), self.tr));
#         }
#     }
        m = 1
        count = len(self.linesl)
        while m < count:
            self.secondaryAreas.append(SecondaryObstacleArea(self.linepl[m - 1], self.linepl[m], self.linesl[m], self.linesl[m - 1], self.tr))
            self.secondaryAreas.append(SecondaryObstacleArea(self.linepr[m - 1], self.linepr[m], self.linesr[m], self.linesr[m - 1], self.tr))
            m += 1

#         m = 1
#         count = len(self.linesl)
#         print len(self.linesl)
#         print len(self.linepl)
#         print len(self.linepr)
#         print len(self.linesr)
#         while m < count:
#             self.secondaryAreas.append([self.linepl[m - 1], self.linepl[m], self.linesl[m], self.linesl[m - 1]])
#             self.secondaryAreas.append([self.linepr[m - 1], self.linepr[m], self.linesr[m], self.linesr[m - 1]])
#             m += 1
            
            
#             public double method_1(Obstacle obstacle_0)
    def method_1(self, obstacle_0):
        point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.tr180, obstacle_0.tolerance)
        point3d = MathHelper.getIntersectionPoint(self.ptTHR, self.ptEND, point3d1, MathHelper.distanceBearingPoint(point3d1, self.trm90, 100))
        num = MathHelper.calcDistance(self.ptTHR, point3d)
        if (MathHelper.smethod_119(point3d, self.ptTHR, self.ptTHRm90)):
            num = num * -1;
        return num;
    
# 
#             protected void method_2(Point3d point3d_0, double double_0)
    def method_2(self, point3d_0, double_0):
        self.tr = double_0;
        self.tr180 = MathHelper.smethod_4(double_0 + 3.14159265358979);
        self.trm90 = MathHelper.smethod_4(double_0 - 1.5707963267949);
        self.trp90 = MathHelper.smethod_4(double_0 + 1.5707963267949);
        self.ptTHR = point3d_0;
        self.ptEND = MathHelper.distanceBearingPoint(self.ptTHR, self.tr, 1000);
        self.ptTHRm90 = MathHelper.distanceBearingPoint(self.ptTHR, self.trm90, 1000);
# 
#             public abstract bool vmethod_0(Obstacle obstacle_0, out ObstacleAreaResult obstacleAreaResult_0, out double double_0, out double double_1, out double double_2, out double double_3);
# 
    def vmethod_0(self, obstacle_0, obstacleAreaResult_0, double_0, double_1, double_2, double_3):
        return False
#             public virtual void vmethod_1(Transaction transaction_0, BlockTableRecord blockTableRecord_0, string string_0, bool bool_0)
#             {
    def vmethod_1(self, sufaceLayers, bool_0):          
        item = [self.linesl[0], self.linesr[0] ]
        mapUnits = define._canvas.mapUnits()
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                resultLayer = QgsVectorLayer("linestring?crs=EPSG:32633", self.Type, "memory")
            else:
                resultLayer = QgsVectorLayer("linestring?crs=EPSG:4326", self.Type, "memory")
        else:
            resultLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), self.Type, "memory")
            
        resultLayer.startEditing()
        
        feature = QgsFeature()
        feature.setGeometry( QgsGeometry.fromPolyline(self.linesl) )
        pr = resultLayer.dataProvider()
        pr.addFeatures([feature])
        # resultLayer.addFeature(feature)

        feature = QgsFeature()
        feature.setGeometry( QgsGeometry.fromPolyline(self.linepl) )
        pr = resultLayer.dataProvider()
        pr.addFeatures([feature])
        # resultLayer.addFeature(feature)

        feature = QgsFeature()
        feature.setGeometry( QgsGeometry.fromPolyline(self.linepr) )
        pr = resultLayer.dataProvider()
        pr.addFeatures([feature])
        # resultLayer.addFeature(feature)

        feature = QgsFeature()
        feature.setGeometry( QgsGeometry.fromPolyline(self.linesr) )
        pr = resultLayer.dataProvider()
        pr.addFeatures([feature])
        # resultLayer.addFeature(feature)

        feature = QgsFeature()
        feature.setGeometry( QgsGeometry.fromPolyline(item) )
        pr = resultLayer.dataProvider()
        pr.addFeatures([feature])
        # resultLayer.addFeature(feature)
        if (bool_0):
            point3dArray = [ self.linesl[len(self.linesl) - 1], self.linesr[len(self.linesr) - 1]]
            feature1 = QgsFeature()
            feature1.setGeometry( QgsGeometry.fromPolyline(point3dArray) )
            pr = resultLayer.dataProvider()
            pr.addFeatures([feature])
            # resultLayer.addFeature(feature1)
            
        resultLayer.commitChanges()
        sufaceLayers.append(resultLayer)

#             }
# 
#             public virtual void vmethod_2(Transaction transaction_0, BlockTableRecord blockTableRecord_0, string string_0)
#             {
    def vmethod_2(self, sufaceLayers):
        i = 1
        count = len(self.linesl)
        mapUnits = define._canvas.mapUnits()
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                resultLayer = QgsVectorLayer("linestring?crs=EPSG:32633", self.Type, "memory")
            else:
                resultLayer = QgsVectorLayer("linestring?crs=EPSG:4326", self.Type, "memory")
        else:
            resultLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), self.Type, "memory")
#         if mapUnits == QGis.Meters:
#             resultLayer = QgsVectorLayer("linestring?crs=EPSG:3857 - WGS 84 / Pseudo Mercator", self.Type, "memory")
#         else:
#             resultLayer = QgsVectorLayer("linestring?crs=EPSG:4326", self.Type, "memory")
            
        resultLayer.startEditing()

        while (i < count):
            face = [self.linepl[i - 1], self.linepl[i], self.linepr[i], self.linepr[i - 1], self.linepl[i - 1]]
            feature = QgsFeature()
            feature.setGeometry( QgsGeometry.fromPolyline(face) )
            pr = resultLayer.dataProvider()
            pr.addFeatures([feature])
            # resultLayer.addFeature(feature)
            face = [self.linesl[i - 1], self.linesl[i], self.linepl[i], self.linepl[i - 1], self.linesl[i - 1]]
            feature = QgsFeature()
            feature.setGeometry( QgsGeometry.fromPolyline(face) )
            pr = resultLayer.dataProvider()
            pr.addFeatures([feature])
            # resultLayer.addFeature(feature)
            face = [self.linesr[i - 1], self.linesr[i], self.linepr[i], self.linepr[i - 1], self.linesr[i - 1]]
            feature = QgsFeature()
            feature.setGeometry( QgsGeometry.fromPolyline(face) )
            pr = resultLayer.dataProvider()
            pr.addFeatures([feature])
            # resultLayer.addFeature(feature)
            i += 1
        resultLayer.commitChanges()
        sufaceLayers.append(resultLayer)
#             }
# 
#             protected abstract double vmethod_3(Point3d point3d_0, bool bool_0);
    def vmethod_3(self, point3d_0, bool_0):
        '''
        virtual function
        '''
#         private class BaroVnavSurfaceZ : BaroVNAV.IBaroVnavSurface
class BaroVnavSurfaceZ(IBaroVnavSurface):
# 
#             public BaroVnavSurfaceZ(Point3d point3d_0, double double_0, double double_1, double double_2, double double_3)
#             {
    def __init__(self, point3d_0 = Point3D(), double_0 = 0.0, double_1 = 0.0, double_2 = 0.0, double_3 = 0.0):
        IBaroVnavSurface.__init__(self)

        self.Type = "Z";
        IBaroVnavSurface.method_2(self, point3d_0, double_0);
        self.xstart = double_1;
        self.tanslope = double_3;
        self.mocma = double_2;
#             }
# 
#             public override bool vmethod_0(Obstacle obstacle_0, out ObstacleAreaResult obstacleAreaResult_0, out double double_0, out double double_1, out double double_2, out double double_3)
#             {
    def vmethod_0(self, obstacle_0, returnList):
        obstacleAreaResult_0 = ObstacleAreaResult.Primary
        double_0 = None;
        double_1 = self.mocma;
        double_2 = double_1
        double_3 = None;
#         if (MathHelper.smethod_44(self.selectionArea, obstacle_0.Position, obstacle_0.tolerance)):
        #obstacleAreaResult_0 = self.primaryArea.imethod_1(obstacle_0.Position, obstacle_0.tolerance, double_1, out double_2, out double_0);
        if not MathHelper.pointInPolygon(self.primaryArea, obstacle_0.Position, obstacle_0.tolerance):
            double_0 = 0.0
            double_2 = 0.0
            #List<SecondaryObstacleArea>.Enumerator enumerator = self.secondaryAreas.GetEnumerator();
            for current in self.secondaryAreas:
                try:
                    num = None;
                    num1 = None;
                    resultList = []
                    obstacleAreaResult = current.imethod_1(obstacle_0.Position, obstacle_0.tolerance, double_1, resultList)
                    if obstacleAreaResult == ObstacleAreaResult.Outside or len(resultList) < 2:
                        obstacleAreaResult_0 = ObstacleAreaResult.Outside
                        continue
                    num = resultList[0]
                    num1 = resultList[1]
                    if obstacleAreaResult == ObstacleAreaResult.Primary:
                        obstacleAreaResult_0 = obstacleAreaResult;
                        double_2 = num;
                        double_0 = num1;
                        break
                    elif obstacleAreaResult == ObstacleAreaResult.Secondary and (num > double_2 or double_2 == 0.0):
                        obstacleAreaResult_0 = obstacleAreaResult
                        double_2 = num
                        double_0 = num1
                        break
                except IndexError:
                    pass
        if obstacleAreaResult_0 != ObstacleAreaResult.Outside:
            obstacle_0.area = obstacleAreaResult_0
            point3d = MathHelper.distanceBearingPoint(obstacle_0.Position, self.tr180, obstacle_0.tolerance);
            double_3 = self.vmethod_3(point3d, False);
            if obstacleAreaResult_0 == ObstacleAreaResult.Primary:
                double_3 = double_3 + (double_1 - double_2)
            
            returnList.append(double_0) 
            returnList.append(double_1) 
            returnList.append(double_2) 
            returnList.append(double_3) 
            return True
        return False
# 
#             protected override double vmethod_3(Point3d point3d_0, bool bool_0)
#             {
    def vmethod_3(self, point3d_0, bool_0):
        point3d = Point3D()
        point3d = MathHelper.getIntersectionPoint(self.ptTHR, self.ptEND, point3d_0, MathHelper.distanceBearingPoint(point3d_0, self.trm90, 100))
        num = MathHelper.calcDistance(self.ptTHR, point3d)
        if not MathHelper.smethod_115(point3d, self.ptTHR, self.ptTHRm90):
            num = num + self.xstart 
        else:
            num = self.xstart - min([num, self.xstart])
        num1 = num * self.tanslope
        if (bool_0):
            num1 = num1 + self.mocma;
        return self.ptTHR.z() + num1;

#         private class BaroVnavSurfaceH : BaroVNAV.IBaroVnavSurface
#         {
class BaroVnavSurfaceH(IBaroVnavSurface):
#             public BaroVnavSurfaceH(Point3d point3d_0, double double_0, double double_1, double double_2, double double_3, double double_4)
#             {
    def __init__(self, point3d_0 = Point3D(), double_0 = 0.0, double_1 = 0.0, double_2 = 0.0, double_3 = 0.0, double_4 = 0.0):
        IBaroVnavSurface.__init__(self)
        self.Type = "H";
        IBaroVnavSurface.method_2(self, point3d_0, double_0);
        self.xstart = min([double_1, double_2]);
        self.tanslope = (max([double_3, double_4]) - min([double_3, double_4])) / (max([double_1, double_2]) - min([double_1, double_2]))
        self.mocfa = max([double_3, double_4])
        self.mocma = min([double_3, double_4])
#             }
# 
#             public override bool vmethod_0(Obstacle obstacle_0, out ObstacleAreaResult obstacleAreaResult_0, out double double_0, out double double_1, out double double_2, out double double_3)
#             {
    def vmethod_0(self, obstacle_0, returnList):
        double_0 = None
        double_3 = None
        point3d = MathHelper.getIntersectionPoint(self.ptTHR, self.ptEND, obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, self.trm90, 100))
        obstacleAreaResult_0 = ObstacleAreaResult.Primary
        num = MathHelper.calcDistance(self.ptTHR, point3d) - obstacle_0.tolerance
        if not MathHelper.smethod_115(point3d, self.ptTHR, self.ptTHRm90):
            num = self.xstart
        else:
            num = max([self.xstart, num])
            
        double_1 = self.mocma + (num - self.xstart) * self.tanslope
        double_2 = double_1
        if not MathHelper.pointInPolygon(self.primaryArea, obstacle_0.Position, obstacle_0.tolerance):
            double_0 = 0.0
            double_2 = 0.0
            for current in self.secondaryAreas:
                try:
                    num1 = None
                    num2 = None
                    resultList = []
                    obstacleAreaResult = current.imethod_1(obstacle_0.Position, obstacle_0.tolerance, double_1, resultList)
                    if obstacleAreaResult == ObstacleAreaResult.Outside:
                        obstacleAreaResult_0 = ObstacleAreaResult.Outside
                        continue
                    num1 = resultList[0]
                    num2 = resultList[1]
    
    #                 obstacleAreaResult = current.imethod_1(obstacle_0.Position, obstacle_0.tolerance, double_1, out num1, out num2);
                    if obstacleAreaResult == ObstacleAreaResult.Primary:
                        obstacleAreaResult_0 = obstacleAreaResult;
                        double_2 = num1
                        double_0 = num2
                        break;
                    elif obstacleAreaResult == ObstacleAreaResult.Secondary and (num1 > double_2 or double_2 == 0.0):
                        obstacleAreaResult_0 = obstacleAreaResult
                        double_2 = num1
                        double_0 = num2
                except IndexError:
                    pass
        if obstacleAreaResult_0 != ObstacleAreaResult.Outside:
            obstacle_0.area = obstacleAreaResult_0
            point3d1 = MathHelper.distanceBearingPoint(obstacle_0.Position, self.tr, obstacle_0.tolerance);
            double_3 = self.vmethod_3(point3d1, False);
            if obstacleAreaResult_0 == ObstacleAreaResult.Primary:
                double_3 = double_3 + (double_1 - double_2)
            
            returnList.append(double_0) 
            returnList.append(double_1) 
            returnList.append(double_2) 
            returnList.append(double_3) 

            return True
        return False
# 
#             protected override double vmethod_3(Point3d point3d_0, bool bool_0)
#             {
    def vmethod_3(self, point3d_0, bool_0):
        
        point3d = Point3D()
        point3d = MathHelper.getIntersectionPoint(self.ptTHR, self.ptEND, point3d_0, MathHelper.distanceBearingPoint(point3d_0, self.trm90, 100))
        num = 0
        if (MathHelper.smethod_115(point3d, self.ptTHR, self.ptTHRm90)):
            num = max([MathHelper.calcDistance(self.ptTHR, point3d), self.xstart]) - self.xstart;
        num1 = 0;
        if (bool_0):
            num1 = self.mocma + num * self.tanslope
        return self.ptTHR.z() + num1
#             }
#         }

#         private class BaroVnavSurfaceFAS : BaroVNAV.IBaroVnavSurface
#         {
class BaroVnavSurfaceFAS(IBaroVnavSurface):
#             private List<BaroVNAV.BaroVnavFasSegment> segments;
# 
#             private double moci;
# 
#             private double xfap;
# 
#             public BaroVnavSurfaceFAS(Point3d point3d_0, double double_0, double double_1, double double_2, List<BaroVNAV.BaroVnavFasSegment> list_0)
#             {
    def __init__(self, point3d_0 = Point3D, double_0 = 0.0, double_1 = 0.0, double_2 = 0.0, list_0 = []):
        IBaroVnavSurface.__init__(self)
        self.Type = "FAS";
        IBaroVnavSurface.method_2(self, point3d_0, double_0);
        self.moci = double_2;
        self.xfap = double_1;
        self.segments = list_0;
#             }
# 
#             private double getMOC(Point3d point3d_0)
#             {
    def getMOC(self, point3d_0):
        point3d = MathHelper.getIntersectionPoint(self.ptTHR, self.ptEND, point3d_0, MathHelper.distanceBearingPoint(point3d_0, self.trm90, 100))
        if (MathHelper.smethod_115(point3d, self.ptTHR, self.ptTHRm90)):
            num = MathHelper.calcDistance(self.ptTHR, point3d)
            for current in self.segments:
                if (num < current.xstart):
                    return current.moc
                if (num >= current.xstart and num <= current.xend):
                    return current.moc
                if self.segments.index(current) == len(self.segments) - 1:
                    return current.moc
                if (num <= self.segments[self.segments.index(current) + 1].xstart):
                    item = current.moc
                    item1 = self.segments[self.segments.index(current) + 1].moc
                    num1 = (item1 - item) / (self.segments[self.segments.index(current) + 1].xstart - current.xend)
                    return item + (num - current.xend) * num1
        return self.segments[0].moc
# 
#             public override bool vmethod_0(Obstacle obstacle_0, out ObstacleAreaResult obstacleAreaResult_0, out double double_0, out double double_1, out double double_2, out double double_3)
    def vmethod_0(self, obstacle_0, returnList):
        point3d = MathHelper.distanceBearingPoint(obstacle_0.Position, self.tr, obstacle_0.tolerance)
        obstacleAreaResult_0 = ObstacleAreaResult.Primary
        double_0 = None
        double_1 = self.getMOC(point3d)
        double_3 = None
        double_2 = double_1
        if not MathHelper.pointInPolygon(self.primaryArea, obstacle_0.Position, obstacle_0.tolerance):
            double_0 = 0.0
            double_2 = 0.0
            for current in self.secondaryAreas:
                try:
                    num = None
                    num1 = None
                    resultList = []
                    obstacleAreaResult = current.imethod_1(obstacle_0.Position, obstacle_0.tolerance, double_1, resultList)
                    if obstacleAreaResult == ObstacleAreaResult.Outside:
                        obstacleAreaResult_0 = ObstacleAreaResult.Outside
                        continue
                    num = resultList[0]
                    num1 = resultList[1]
                    if (obstacleAreaResult == ObstacleAreaResult.Primary):
                        obstacleAreaResult_0 = obstacleAreaResult
                        double_2 = num
                        double_0 = num1
                        break
                    elif obstacleAreaResult == ObstacleAreaResult.Secondary and (num > double_2 or double_2 == 0.0):
                        obstacleAreaResult_0 = obstacleAreaResult;
                        double_2 = num;
                        double_0 = num1;
                except IndexError:
                    pass
        if obstacleAreaResult_0 != ObstacleAreaResult.Outside:
            obstacle_0.area = obstacleAreaResult_0
            double_3 = self.vmethod_3(point3d, False)
            if obstacleAreaResult_0 == ObstacleAreaResult.Secondary:
                double_3 = double_3 + (double_1 - double_2)
                
            returnList.append(double_0) 
            returnList.append(double_1) 
            returnList.append(double_2) 
            returnList.append(double_3) 
            return True
        return False
#             }
# 
#             protected override double vmethod_3(Point3d point3d_0, bool bool_0)
#             {
    def vmethod_3(self, point3d_0, bool_0):
        point3d = MathHelper.getIntersectionPoint(self.ptTHR, self.ptEND, point3d_0, MathHelper.distanceBearingPoint(point3d_0, self.trm90, 100));
        item = 0;
        if (MathHelper.smethod_115(point3d, self.ptTHR, self.ptTHRm90)):
            num = MathHelper.calcDistance(self.ptTHR, point3d);
            num1 = 0;
            count = len(self.segments)
            while (num1 < count):
                if (num < self.segments[num1].xstart):
                    if ( not bool_0):
                        return self.ptTHR.z() + item;
                    item = item + self.segments[num1].moc;
                    return self.ptTHR.z() + item
                elif (num < self.segments[num1].xstart or num >= self.segments[num1].xend):
                    if (num1 + 1 >= len(self.segments)):
                        item = (self.segments[num1].xend - self.segments[num1].xfas) * self.segments[num1].tanafas;
                        if (bool_0):
                            item = item + self.segments[num1].moc;
                    elif (num <= self.segments[num1 + 1].xstart):
                        item = (self.segments[num1].xend - self.segments[num1].xfas) * self.segments[num1].tanafas;
                        if (not bool_0):
                            return self.ptTHR.z() + item;
                        item1 = self.segments[num1].moc;
                        item2 = self.segments[num1 + 1].moc;
                        num2 = (item2 - item1) / (self.segments[num1 + 1].xstart - self.segments[num1].xend);
                        item3 = item1 + (num - self.segments[num1].xend) * num2;
                        item = item + item3;
                        return self.ptTHR.z() + item;
                    num1 += 1
                else:
                    item = (num - self.segments[num1].xfas) * self.segments[num1].tanafas;
                    if (not bool_0):
                        return self.ptTHR.z() + item;
                    item = item + self.segments[num1].moc;
                    return self.ptTHR.z() + item;
        elif (bool_0):
            item = item + self.segments[0].moc;
        return self.ptTHR.z() + item;
#             }
#         }
