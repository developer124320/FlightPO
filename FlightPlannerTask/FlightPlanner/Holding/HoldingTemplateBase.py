'''
Created on 2 Jul 2015

@author: Administrator
'''
from FlightPlanner.types import Point3D, Matrix3d, Vector3d
from FlightPlanner.helpers import MathHelper, Unit
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.types import SurfaceTypes, DistanceUnits, OrientationType, AltitudeUnits, TurnDirection
from qgis.core import QgsPoint, QGis, QgsGeometry

class HoldingTemplateBase:
    '''
    classdocs
    '''


    def __init__(self,params):
        '''
        Constructor
        '''
    def method_0(self, point3dCollection_0):
        self.time = 0.0
        point3d = Point3D(0, 0, 0)
        matrix3d = Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d));
        matrix3d1 = Matrix3d.Rotation(self.trackRad, Vector3d(0, 0, 1), point3d);
        item = point3dCollection_0[0]
        point3d1 = item.TransformBy(matrix3d).TransformBy(matrix3d1);
        point3d2 = point3d1;
        point3d3 = point3d1;
        point3d4 = point3d1;
        point3d5 = point3d1;
        for i in range(1, len(point3dCollection_0)):
            item1 = point3dCollection_0[i]
            point3d6 = item1.TransformBy(matrix3d).TransformBy(matrix3d1);
            if (point3d6.get_Y() > point3d5.get_Y()):
                point3d5 = point3d6;
            if (point3d6.get_X() > point3d4.get_X()):
                point3d4 = point3d6;
            if (point3d6.get_Y() < point3d3.get_Y()):
                point3d3 = point3d6;
            if (point3d6.get_X() < point3d2.get_X()):
                point3d2 = point3d6
        point3d7 = point3d5.TransformBy(Matrix3d.Inverse(matrix3d1));
        point3d5 = point3d7.TransformBy(Matrix3d.Inverse(matrix3d));
        point3d8 = point3d4.TransformBy(Matrix3d.Inverse(matrix3d1));
        point3d4 = point3d8.TransformBy(Matrix3d.Inverse(matrix3d));
        point3d9 = point3d3.TransformBy(Matrix3d.Inverse(matrix3d1));
        point3d3 = point3d9.TransformBy(Matrix3d.Inverse(matrix3d));
        point3d10 = point3d2.TransformBy(Matrix3d.Inverse(matrix3d1));
        point3d2 = point3d10.TransformBy(Matrix3d.Inverse(matrix3d));
        self.bounds = [point3d5, point3d4, point3d3, point3d2]
#         self.bounds = new Point3dCollection();
#         Point3dCollection point3dCollection = self.bounds;
#         Point3d[] point3dArray = new Point3d[] { point3d5, point3d4, point3d3, point3d2 };
#         point3dCollection.smethod_145(point3dArray);
    
    def method_1(self, point3d_0, point3d_1, point3d_2):
        self.spiralBounds = [point3d_0, point3d_1, point3d_2 ]
#         self.spiralBounds = new Point3dCollection();
#         Point3dCollection point3dCollection = self.spiralBounds;
#         Point3d[] point3d0 = new Point3d[] { point3d_0, point3d_1, point3d_2 };
#         point3dCollection.smethod_145(point3d0);
    
    def method_2(self, polylineArea_0):
        polyLineAreaList = []
#         Region region;
        num = Unit.ConvertDegToRad(70) if(self.orientation == OrientationType.Right) else Unit.ConvertDegToRad(-70)
        vector3d = Vector3d(0, 0, 1);
        matrix3d = Matrix3d.Rotation(num, vector3d, self.ptBase);
        matrix3d1 = Matrix3d.Mirroring(self.ptBase, MathHelper.distanceBearingPoint(self.ptBase, self.trackRad, 100), self.ptBase.smethod_167(2))
#         DBObjectCollection dBObjectCollection = new DBObjectCollection();
#         DBObjectCollection dBObjectCollection1 = new DBObjectCollection();
#         try
#         {
        num1 = 0;
        origin = Point3D.get_Origin();
        point3d = polylineArea_0[0].Position.TransformBy(matrix3d)
        point3dCollection = self.spiral.method_14_closed(4)
        polyline1 = PolylineArea(point3dCollection)
        polyline2 = polyline1.TransformBy(matrix3d);
        polyline = polyline2.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d)));
        polyLineAreaList.append(polyline)
#         dBObjectCollection.Add(polyline);
        num1, origin = self.method_6(polyline, self.ptBase, num1, origin);
        point3d1 = polylineArea_0[1].Position.TransformBy(matrix3d);
        
        point3dCollection = self.spiral.method_14_closed(4)
        polyline1 = PolylineArea(point3dCollection)
        polyline2 = polyline1.TransformBy(matrix3d);
        polyline = polyline2.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d1)));
#         polyline = AcadHelper.smethod_136(self.spiral, true);
#         polyline.TransformBy(matrix3d);
#         polyline.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d1)));
        polyLineAreaList.append(polyline)
#         dBObjectCollection.Add(polyline);
        num1, origin = self.method_6(polyline, self.ptBase, num1, origin);
        point3d2 = polylineArea_0[3].Position.TransformBy(matrix3d);
        point3dCollection = self.spiral.method_14_closed(4)
        polyline1 = PolylineArea(point3dCollection)
        polyline2 = polyline1.TransformBy(matrix3d1);
        polyline3 = polyline2.TransformBy(matrix3d);
        polyline = polyline3.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d2)));
        
#         polyline = AcadHelper.smethod_136(self.spiral, true);
#         polyline.TransformBy(matrix3d1);
#         polyline.TransformBy(matrix3d);
#         polyline.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d2)));
        polyLineAreaList.append(polyline)        
#         dBObjectCollection.Add(polyline);
        point3d3 = polylineArea_0[2].Position.TransformBy(matrix3d);
        point3dCollection = self.spiral.method_14_closed(4)
        polyline1 = PolylineArea(point3dCollection)
        polyline2 = polyline1.TransformBy(matrix3d1);
        polyline3 = polyline2.TransformBy(matrix3d);
        polyline = polyline3.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d3)));
        
        
#         polyline = AcadHelper.smethod_136(self.spiral, true);
#         polyline.TransformBy(matrix3d1);
#         polyline.TransformBy(matrix3d);
#         polyline.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d3)));
        polyLineAreaList.append(polyline)    
#         dBObjectCollection.Add(polyline);
#         if (num1 > 0):
#             point3d4 = MathHelper.distanceBearingPoint(self.ptBase, self.trackRad + 3.14159265358979, num1);
#             polyline = PolylineArea()
#             polyline.Add(origin.smethod_176(), MathHelper.smethod_57((self.orientation == OrientationType.Left ? TurnDirection.Left : TurnDirection.Right), origin, point3d4, self.ptBase), 0, 0);
#             polyline.AddVertexAt(1, point3d4.smethod_176(), 0, 0, 0);
#             polyline.set_Closed(true);
#             dBObjectCollection.Add(polyline);
#         }
        point3dCollection = []
        item = self.spiralBounds[0]
        point3d5 = item.TransformBy(matrix3d);
        point3dCollection.append(point3d5.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d))));
        item1 = self.spiralBounds[1]
        point3d6 = item1.TransformBy(matrix3d);
        point3dCollection.append(point3d6.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d))));
        item2 = self.spiralBounds[1]
        point3d7 = item2.TransformBy(matrix3d);
        point3dCollection.append(point3d7.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d1))));
        item3 = self.spiralBounds[2]
        point3d8 = item3.TransformBy(matrix3d);
        point3dCollection.append(point3d8.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d1))));
        item4 = self.spiralBounds[2]
        point3d9 = item4.TransformBy(matrix3d1).TransformBy(matrix3d);
        point3dCollection.append(point3d9.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d3))));
        item5 = self.spiralBounds[1]
        point3d10 = item5.TransformBy(matrix3d1).TransformBy(matrix3d);
        point3dCollection.append(point3d10.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d3))));
        item6 = self.spiralBounds[1]
        point3d11 = item6.TransformBy(matrix3d1).TransformBy(matrix3d);
        point3dCollection.append(point3d11.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d2))));
        item7 = self.spiralBounds[0]
        point3d12 = item7.TransformBy(matrix3d1).TransformBy(matrix3d);
        point3dCollection.append(point3d12.TransformBy(Matrix3d.Displacement(self.ptBase.GetVectorTo(point3d2))));
        point3dCollection = MathHelper.smethod_190(point3dCollection);
        polylineArea1 = PolylineArea(point3dCollection)
        polyLineAreaList.append(polyline)   
        return  polyLineAreaList
        
#         dBObjectCollection.Insert(0, AcadHelper.smethod_133(point3dCollection, true));
#         dBObjectCollection1 = Region.CreateFromCurves(dBObjectCollection);
#         Region region1 = dBObjectCollection1.get_Item(0) as Region;
#         dBObjectCollection1.RemoveAt(0);
#         for (int i = 0; i < 4; i++)
#         {
#             region1.BooleanOperation(0, dBObjectCollection1.get_Item(i) as Region);
#         }
#         region = region1;
#         }
#         finally
#         {
#             AcadHelper.smethod_25(dBObjectCollection);
#             AcadHelper.smethod_25(dBObjectCollection1);
#         }
#         return region;
    
    def method_3(self, polylineArea_0):
        point3dCollection = self.area.method_14_closed(4)
        polylineArea0 = PolylineArea(point3dCollection)
        num = MathHelper.calcDistance(self.ptBase, polylineArea_0[0].Position);
        num1 = self.trackRad
        point3d = MathHelper.distanceBearingPoint(self.ptBase, num1, num);
        matrix = Matrix3d.Displacement(self.ptE.GetVectorTo(point3d))
        polylineArea = polylineArea0.TransformBy(matrix)
        polylineAreaList = []
        polylineAreaList.append(polylineArea)
#         Region transformedCopy = region1.GetTransformedCopy(Matrix3d.Displacement(self.ptE.GetVectorTo(point3d))) as Region;
        for i in range(1, 72):
            point3d = MathHelper.distanceBearingPoint(self.ptBase, num1 + i * 0.0872664625997165, num);
            polylineArea = polylineArea0.TransformBy(Matrix3d.Displacement(self.ptE.GetVectorTo(point3d)))
            polylineAreaList.append(polylineArea)
#             Region transformedCopy1 = region1.GetTransformedCopy(Matrix3d.Displacement(self.ptE.GetVectorTo(point3d))) as Region;
#             try
#             {
#                 transformedCopy.BooleanOperation(0, transformedCopy1);
#             }
#             finally
#             {
#                 AcadHelper.smethod_24(transformedCopy1);
#             }
#         }
#         region = transformedCopy;
#         }
#         finally
#         {
#             AcadHelper.smethod_24(region1);
#         }
        return polylineAreaList
    
    def method_4(self, region_0):
        pass
    
    def method_5(self, point3dCollection_0, double_0):
        pass
    
    def method_6(self, polyline_0, point3d_0, double0, point3d1):
        double_0 = double0
        point3d_1 = point3d1
#         Point3d point3d;
        flag = False;
        origin = Point3D.get_Origin();
        i = 0
        for plylineAreaPoint in polyline_0:
            bulgeAt = plylineAreaPoint.Bulge
            if (bulgeAt != 0):
                point3dAt = plylineAreaPoint.Position
                point3d1 = polyline_0[0].Position if(i == polyline_0.Count - 1) else  polyline_0[i + 1].Position
                point3d = MathHelper.smethod_71(point3dAt, point3d1, bulgeAt)
                if (point3d != None):
                    point3d2 = MathHelper.distanceBearingPoint(point3d, MathHelper.getBearing(point3d_0, point3d), MathHelper.calcDistance(point3d, point3dAt));
                    if (flag):
                        if (self.orientation == OrientationType.Left):
                            if (not MathHelper.smethod_119(point3d2, point3d_0, origin)):
                                num = MathHelper.calcDistance(point3d_0, point3d2);
                                if (num > double_0):
                                    double_0 = num;
                                    point3d_1 = point3d2;
                                origin = point3d1;
                                flag = True;
                                continue
                            continue
                        elif (MathHelper.smethod_115(point3d2, point3d_0, origin)):
                            continue
                    num = MathHelper.calcDistance(point3d_0, point3d2);
                    if (num > double_0):
                        double_0 = num;
                        point3d_1 = point3d2;
                    origin = point3d1;
                    flag = True;
            i += 1
        return (double_0, point3d_1)
    @staticmethod
    def smethod_0( polylineArea_0, double_0, int_0):
        polylineAreaList = []
#         DBObjectCollection dBObjectCollection;
#         OffsetGapType offsetType = AcadHelper.OffsetType;
#         try
#         {
#             AcadHelper.OffsetType = OffsetGapType.Extend;
#             using (Polyline polyline = AcadHelper.smethod_136(polylineArea_0, true))
#             {
#                 polyline.SetDatabaseDefaults();
        num = -1 if(polylineArea_0.Direction() == TurnDirection.Right) else 1
        num = 1
#         DBObjectCollection dBObjectCollection1 = new DBObjectCollection();
        for i in range(1, int_0 + 1):
            polylineAreaList.append(polylineArea_0.getOffsetCurve(float(num) * double_0 * i))
#             dBObjectCollection1.Add(polyline.GetOffsetCurves((double)num * double_0 * (double)i).get_Item(0));
#         }
#         dBObjectCollection = dBObjectCollection1;
#             }
#         }
#         finally
#         {
#             AcadHelper.OffsetType = offsetType;
#         }
        return polylineAreaList;
    
    @staticmethod
    def smethod_1( polylineArea_0, bool_0):
        polylineAreaList = HoldingTemplateBase.smethod_0(polylineArea_0, Unit.ConvertNMToMeter(1), 5);
        if (bool_0):
            polylineAreaList.append(polylineArea_0)
#             dBObjectCollection.Insert(0, AcadHelper.smethod_131(polylineArea_0));
#         }
        return polylineAreaList;
    
    @staticmethod
    def smethod_2( polylineArea_0, distance_0):
        polylineArea_0.method_16();
        polylineAreaList = HoldingTemplateBase.smethod_0(polylineArea_0, distance_0.Metres, 1);
#         dBObjectCollection.Insert(0, AcadHelper.smethod_136(polylineArea_0, true));
        return polylineAreaList;
    
    @staticmethod
    def smethod_3( polylineArea_0, altitude_0, altitude_1):
#         DBObjectCollection dBObjectCollection;
        polylineAreaList = HoldingTemplateBase.smethod_0(polylineArea_0, Unit.ConvertNMToMeter(1), 5);
#         DBObjectCollection dBObjectCollection2 = new DBObjectCollection();
        num = 0.5;
        metres = altitude_0.Metres - altitude_1.Metres;
        resultGeometryList = []
        for i in range(5):
            if (i > 0):
                metres = altitude_0.Metres - num * altitude_1.Metres;
                num = num - 0.1;
#             (dBObjectCollection1.get_Item(i) as Polyline).set_Elevation(metres);
#             DBObjectCollection dBObjectCollection3 = new DBObjectCollection();
#             dBObjectCollection3.Add(dBObjectCollection1.get_Item(i));
            item = polylineAreaList[i].method_14_closed(4)
            itemGeometry = QgsGeometry.fromPolygon([item])
#             item.SetDatabaseDefaults();
            if (i > 0):
#                 (dBObjectCollection1.get_Item(i - 1) as Polyline).set_Elevation(metres);
#                 DBObjectCollection dBObjectCollection4 = new DBObjectCollection();
#                 dBObjectCollection4.Add(dBObjectCollection1.get_Item(i - 1));
                regionGeometry = QgsGeometry.fromPolygon([polylineAreaList[i - 1].method_14_closed(4)])
                polygonNew = itemGeometry.difference(regionGeometry)
                resultGeometryList.append(polygonNew)
            else:
                resultGeometryList.append(itemGeometry)
#                 region.SetDatabaseDefaults();
#                 item.BooleanOperation(2, region);
#                 region.Dispose();
#                 }
#             dBObjectCollection2.Add(item);
#             }
#             dBObjectCollection = dBObjectCollection2;
        return resultGeometryList;
    
    @staticmethod
    def smethod_4( polylineArea_0, altitude_0, altitude_1, distance_0):
        polylineAreaList = HoldingTemplateBase.smethod_0(polylineArea_0, distance_0.Metres, 1);
        polyline = PolylineArea.smethod_131(polylineArea_0);
        item = polylineAreaList[0]
        polylineArea_1 = PolylineArea(polyline.method_160(500));
        polylineArea_2 = PolylineArea(item.method_160(500));
#         polylineArea_1 = polyline
#         polylineArea_2 = item
        polylineArea_2.method_22(altitude_0.Metres);
        polylineArea_1.method_22(altitude_0.Metres - altitude_1.Metres);
        return (polylineArea_1, polylineArea_2)
    @staticmethod
    def smethod_5( polylineArea_0, distance_0):
#         PolylineArea polylineArea;
        polylineAreaList = HoldingTemplateBase.smethod_0(polylineArea_0, distance_0.Metres, 1);
#         try
#         {
        point3dCollection = polylineAreaList[0].method_14_closed(4)
#         }
#         finally
#         {
#             AcadHelper.smethod_25(dBObjectCollection);
#         }
        return PolylineArea(point3dCollection);
    
    @staticmethod
    def smethod_6( polylineArea_0, distance_0):
        pass
    
    def vmethod_0(self, polylineArea_0, bool_0, bool_1):
        point3dArray = self.area.method_14_closed(4)
        polylineArea0 = PolylineArea(point3dArray)
        polylineAreaList = []#self.area]
        point3dCollection = []
        for i in range(4):
            matrix = Matrix3d.Displacement(self.ptBase.GetVectorTo(polylineArea_0[i].Position))
            polylinAreaNew = polylineArea0.TransformBy(matrix)
            polylineAreaList.append(polylinAreaNew)
            point3dCollection = []
            for point3d0 in self.bounds:
                point3d = point3d0.TransformBy(matrix)
                point3dCollection.append(point3d)
            point3dCollection.append(self.bounds[0].TransformBy(matrix))
            polylineAreaList.append(polylinAreaNew)
            polylineAreaList.append(PolylineArea(point3dCollection))
                
#         point3dCollection0 = MathHelper.smethod_190(point3dCollection)
#         polylinAreaNew = PolylineArea(point3dCollection0)
#         polylineAreaList.append(polylinAreaNew)
        
# #             break
        if bool_1:
            polylineAreaList.extend(self.method_3(polylineArea_0))
        if bool_0:
            polylineAreaList.extend(self.method_2(polylineArea_0))
          
#         polylineAreaList.append(polylineArea_0)
#                 
#         return polylineAreaList
        pointList = QgisHelper.convexFull(polylineAreaList)
#         pointList = QgisHelper.UnionFromPolylineAreaList(polylineAreaList)
        polylineArea = PolylineArea()
        for point in pointList:
            polylineArea.Add(PolylineAreaPoint(point))
        return [polylineArea]
#         return [polylineArea0]
    
    def vmethod_1(self, polylineArea_0, bool_0, bool_1, bool_2):
        pass
    
    def get_area(self):
        return self.area
    Area = property(get_area, None, None, None)
    
    def get_ptBase(self):
        return self.ptBase
    BasePoint = property(get_ptBase, None, None, None)
    
    def get_ds(self):
        return self.ds
    D = property(get_ds, None, None, None)
    
    def get_nominal(self):
        return self.nominal
    Nominal = property(get_nominal, None, None, None)
    
    def get_orientation(self):
        return self.orientation
    Orientation = property(get_orientation, None, None, None)
    
    def get_ptE(self):
        return self.ptE
    PointE = property(get_ptE, None, None, None)
    
    def get_ptR(self):
        return self.ptR
    PointR = property(get_ptR, None, None, None)
    
    def get_radius(self):
        return self.radius
    Radius = property(get_radius, None, None, None)
    
    def get_R(self):
        return self.R
    RateOfTurn = property(get_R, None, None, None)
    
    def get_spiral(self):
        return self.spiral
    Spiral = property(get_spiral, None, None, None)
    
    def get_tas(self):
        return self.tas
    TAS = property(get_tas, None, None, None)
    
    def get_trackDeg(self):
        return self.trackDeg
    TrackDeg = property(get_trackDeg, None, None, None)
    
    def get_wd(self):
        return self.wd
    WD = property(get_wd, None, None, None)
    
        