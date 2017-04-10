'''
Created on Feb 23, 2015

@author: Administrator
'''

from FlightPlanner.helpers0 import MathHelper, Distance, Unit
from FlightPlanner.types0 import TurnDirection, AngleUnits, Point3D
from qgis.core import QgsGeometry, QgsFeature, QgsPoint
from FlightPlanner.polylineArea0 import PolylineArea

class WindSpiral:

    def __init__(self, point3d_0, double_0, speed_0, speed_1, double_1, turnDirection_0):
        
#     public WindSpiral(Point3d point3d_0, double double_0, Speed speed_0, Speed speed_1, double double_1, TurnDirection turnDirection_0)
#     {
#         double num;
#         int num1;
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
        point3d = MathHelper.distanceBearingPoint(point3d_0, num1 * 1.5707963267949 + double_0, metres)
        self.Start[0] = point3d_0;
        self.Middle[0] = MathHelper.distanceBearingPoint(point3d, -1 * num1 * 0.785398163397448 + double_0, metres + metresPerSecond);
        self.Finish[0] = MathHelper.distanceBearingPoint(point3d, double_0, metres + metresPerSecond1);
        self.Start[1] = self.Finish[0];
        self.Middle[1] = MathHelper.distanceBearingPoint(point3d, num1 * 0.785398163397448 + double_0, metres + metresPerSecond2);
        self.Finish[1] = MathHelper.distanceBearingPoint(point3d, num1 * 1.5707963267949 + double_0, metres + num2);
        self.Start[2] = self.Finish[1];
        self.Middle[2] = MathHelper.distanceBearingPoint(point3d, num1 * 2.35619449019234 + double_0, metres + metresPerSecond3);
        self.Finish[2] = MathHelper.distanceBearingPoint(point3d, num1 * 3.14159265358979 + double_0, metres + num3);
        self.Center[0] = MathHelper.smethod_68(self.Start[0], self.Middle[0], self.Finish[0])
        self.Center[1] = MathHelper.smethod_68(self.Start[1], self.Middle[1], self.Finish[1])
        self.Center[2] = MathHelper.smethod_68(self.Start[2], self.Middle[2], self.Finish[2])
        self.Radius[0] = MathHelper.calcDistance(self.Center[0], self.Middle[0])
        self.Radius[1] = MathHelper.calcDistance(self.Center[1], self.Middle[1])
        self.Radius[2] = MathHelper.calcDistance(self.Center[2], self.Middle[2])
        
#     public Polyline Object
#     {
#         get
#         {
#             Point3d[] point3dArray = new Point3d[] { self.start[0], self.start[1], self.start[2], self.finish[2] };
#             Polyline polyline = AcadHelper.smethod_126(point3dArray);
#             polyline.SetBulgeAt(0, MathHelper.smethod_60(self.start[0], self.middle[0], self.finish[0]));
#             polyline.SetBulgeAt(1, MathHelper.smethod_60(self.start[1], self.middle[1], self.finish[1]));
#             polyline.SetBulgeAt(2, MathHelper.smethod_60(self.start[2], self.middle[2], self.finish[2]));
#             return polyline;
#         }
#     }


    def method_0(self, double_0, angleUnits_0):
        if (angleUnits_0 == AngleUnits.Degrees):
            double_0 = Unit.ConvertDegToRad(double_0)
        if self.Direction != TurnDirection.Left:
            num = double_0 - 1.5707963267949 
        else:
            num = double_0 + 1.5707963267949
            
        point3d = MathHelper.distanceBearingPoint(self.Center[0], num, self.Radius[0]);
        point3d1 = MathHelper.distanceBearingPoint(self.Center[1], num, self.Radius[1]);
        point3d2 = MathHelper.distanceBearingPoint(self.Center[2], num, self.Radius[2]);
        if (self.Direction == TurnDirection.Left):
            if (MathHelper.smethod_115(point3d1, point3d, MathHelper.distanceBearingPoint(point3d, double_0, 1000)) or MathHelper.smethod_119(point3d1, self.Center[0], self.Finish[0])):
                return point3d;
            if (not MathHelper.smethod_115(point3d2, point3d1, MathHelper.distanceBearingPoint(point3d1, double_0, 1000))) and (not MathHelper.smethod_119(point3d2, self.Center[1], self.Finish[1])):
                return point3d2;
            return point3d1;
        if (MathHelper.smethod_119(point3d1, point3d, MathHelper.distanceBearingPoint(point3d, double_0, 1000)) or MathHelper.smethod_115(point3d1, self.Center[0], self.Finish[0])):
            return point3d;
        if (not MathHelper.smethod_119(point3d2, point3d1, MathHelper.distanceBearingPoint(point3d1, double_0, 1000))) and (not MathHelper.smethod_115(point3d2, self.Center[1], self.Finish[1])):
            return point3d2;
        return point3d1;

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
#         point3dCollection = Point3dCollection();
        flag = obj.intersects(line) if (not bool_0) else obj.intersects(lineBound) #? obj.IntersectWith(line, 0, point3dCollection) > 0 : obj.IntersectWith(line, 2, point3dCollection) > 0);
#             }
#         }
        return flag;

    def get_Object(self):
        point3dArray = [self.Start[0], self.Start[1], self.Start[2], self.Finish[2]];
        polyline = PolylineArea(point3dArray);
        polyline.SetBulgeAt(0, MathHelper.smethod_60(self.Start[0], self.Middle[0], self.Finish[0]));
        polyline.SetBulgeAt(1, MathHelper.smethod_60(self.Start[1], self.Middle[1], self.Finish[1]));
        polyline.SetBulgeAt(2, MathHelper.smethod_60(self.Start[2], self.Middle[2], self.Finish[2]));
        return QgsGeometry.fromPolyline(polyline.method_14());
    Object = property(get_Object, None, None, None)