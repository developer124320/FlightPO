'''
Created on 2 Jul 2015

@author: Administrator
'''
from PyQt4.QtGui import QMessageBox
from FlightPlanner.Holding.HoldingTemplateBase import HoldingTemplateBase
from FlightPlanner.Holding.HoldingTemplate import HoldingTemplate
from FlightPlanner.helpers import MathHelper, Speed, Unit, Distance
from FlightPlanner.types import IntersectionStatus, DistanceUnits, OrientationType, TurnDirection, Matrix3d, Vector3d, Point3D
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from qgis.core import QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.messages import Messages
import math

class HoldingTemplateRnav(HoldingTemplateBase):
    '''
    classdocs
    '''


    def __init__(self, point3d_0, double_0, speed_0, altitude_0, speed_1, double_1, distance_0, orientationType_0,  distance_1 = None, distance_2 = None):
        '''
        Constructor
        '''
        
        if distance_1 == None:
    #         Point3d point3d;
    #         double num;
    #         Point3d point3d1;
    #         double num1;
    #         Point3d point3d2;
    #         double num2;
    #         Point3d point3d3;
    #         Point3d point3d4;
    #         Point3d point3d5;
    #         Point3d point3d6;
    #         Point3d point3d7;
            point3d_0 = point3d_0.smethod_167(0)
            self.ptBase = point3d_0
            self.trackDeg = MathHelper.smethod_3(double_0)
            self.trackRad = MathHelper.smethod_4(Unit.ConvertDegToRad(double_0))
            self.orientation = orientationType_0
            self.tas = Speed.smethod_0(speed_0, double_1, altitude_0)
            self.R = min([943.27 / self.tas.KilometresPerHour, 3])
            self.radius = Distance(Unit.ConvertKMToMeters(self.tas.KilometresPerHour / (62.8318530717959 * self.R)))
            metresPerSecond = self.tas.MetresPerSecond
            metres = self.radius.Metres
            kilometresPerHour = speed_1.KilometresPerHour
            metresPerSecond1 = speed_1.MetresPerSecond
            r = 45 * metresPerSecond1 / self.R
            self.ds = distance_0
            if (self.ds.Metres < 2 * metres):
                num3 = MathHelper.smethod_0(Unit.ConvertMeterToNM(2 * metres), 0)

    #             if (WarningMessageBox.smethod_1(iwin32Window_0, string.Format(Confirmations.INSUFFICIENT_LENGTH_OF_OUTBOUND_LEG, num3), ExtendedMessageBoxButtons.YesNo) != ExtendedDialogResult.Yes)
    #             {
    #                 throw new AbortException();
    #             }
                self.ds = Distance(num3, DistanceUnits.NM)
            self.wd = Distance(math.sqrt(self.ds.Metres * self.ds.Metres + 4 * metres * metres))
            num4 = 5 * metresPerSecond
            num5 = 11 * metresPerSecond
            num6 = 5 * metresPerSecond1
            num7 = 11 * metresPerSecond1
            num8 = num7 + r
            num9 = num7 + 2 * r
            num10 = num7 + 3 * r
            num11 = num7 + 4 * r
            num12 = num6 + 5 * r
            num13 = num6 + 6 * r
            metres1 = 2 * metres + self.ds.Metres + 11 * metresPerSecond + (11 + 90 / self.R + 11 + 105 / self.R) * metresPerSecond1;
            num14 = 11 * metresPerSecond * math.cos(Unit.ConvertDegToRad(20)) + metres * math.sin(Unit.ConvertDegToRad(20)) + metres + (11 + 20 / self.R + 90 / self.R + 11 + 15 / self.R) * metresPerSecond1;
            self.ias = speed_0;
            self.wind = speed_1;
            self.isa = double_1;
            self.altitude = altitude_0;
            self.time = 0#self.time;
            num15 = 1 if(orientationType_0 == OrientationType.Right) else -1
            turnDirection = TurnDirection.Right if(orientationType_0 == OrientationType.Right) else TurnDirection.Left
            point3d8 = MathHelper.distanceBearingPoint(point3d_0, 0, 0);
            point3d9 = MathHelper.distanceBearingPoint(point3d8, Unit.ConvertDegToRad(double_0), num4);
            point3d10 = MathHelper.distanceBearingPoint(point3d8, Unit.ConvertDegToRad(double_0), num5);
            point3d11 = MathHelper.distanceBearingPoint(point3d10, Unit.ConvertDegToRad(double_0 + num15 * 90), metres);
            point3d12 = MathHelper.distanceBearingPoint(point3d11, Unit.ConvertDegToRad(double_0 + num15 * -45), metres);
            point3d13 = MathHelper.distanceBearingPoint(point3d11, Unit.ConvertDegToRad(double_0), metres);
            point3d14 = MathHelper.distanceBearingPoint(point3d11, Unit.ConvertDegToRad(double_0 + num15 * 45), metres);
            point3d15 = MathHelper.distanceBearingPoint(point3d11, Unit.ConvertDegToRad(double_0 + num15 * 90), metres);
            point3d11 = MathHelper.distanceBearingPoint(point3d9, Unit.ConvertDegToRad(double_0 + num15 * 90), metres);
            MathHelper.distanceBearingPoint(point3d11, Unit.ConvertDegToRad(double_0 + num15 * 90), metres);
            point3d16 = MathHelper.distanceBearingPoint(point3d11, Unit.ConvertDegToRad(double_0 + num15 * 135), metres);
            point3d17 = MathHelper.distanceBearingPoint(point3d11, Unit.ConvertDegToRad(double_0 + 180), metres);
            point3d, num = MathHelper.smethod_193(point3d10, num7, point3d12, num8, point3d13, num9, False);
            point3d1, num1 = MathHelper.smethod_193(point3d13, num9, point3d14, num10, point3d15, num11, False);
            point3d2, num2 = MathHelper.smethod_193(point3d15, num11, point3d16, num12, point3d17, num13, False);
            point3d11 = MathHelper.distanceBearingPoint(point3d8, Unit.ConvertDegToRad(double_0 + num15 * 90), 2 * metres);
            point3d18 = MathHelper.distanceBearingPoint(point3d11, Unit.ConvertDegToRad(double_0 + 180), self.ds.Metres);
            matrix3d = Matrix3d.Displacement(point3d_0.GetVectorTo(point3d18));
            matrix3d1 = Matrix3d.Rotation(-Unit.ConvertDegToRad(180), Vector3d(0, 0, 1), point3d18);
            point3d19 = point3d1.TransformBy(matrix3d);
            point3d20 = point3d19.TransformBy(matrix3d1);
            num16 = num1;
            point3d21 = point3d2.TransformBy(matrix3d).TransformBy(matrix3d1);
            num17 = num2;
            point3d11 = MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(double_0 + num15 * 90), num2);
            point3d3 = MathHelper.getIntersectionPoint(point3d11, MathHelper.distanceBearingPoint(point3d11, Unit.ConvertDegToRad(double_0 + 180), 100), point3d18, MathHelper.distanceBearingPoint(point3d18, Unit.ConvertDegToRad(double_0 + num15 * 90), 100));
            matrix3d = Matrix3d.Displacement(point3d_0.GetVectorTo(point3d3));
            matrix3d1 = Matrix3d.Rotation(-Unit.ConvertDegToRad(180), Vector3d(0, 0, 1), point3d3);
            point3d22 = point3d.TransformBy(matrix3d).TransformBy(matrix3d1);
            num18 = num;
            point3d19 = point3d1.TransformBy(matrix3d);
            point3d23 = point3d19.TransformBy(matrix3d1);
            num19 = num1;
            point3d24 = MathHelper.distanceBearingPoint(point3d21, Unit.ConvertDegToRad(double_0 - num15 * 90), num17);
            point3d25 = MathHelper.distanceBearingPoint(point3d24, Unit.ConvertDegToRad(double_0 + num15 * 90), num14);
            point3d26 = MathHelper.distanceBearingPoint(point3d20, Unit.ConvertDegToRad(double_0 + 180), num16);
            point3d27 = MathHelper.distanceBearingPoint(point3d26, Unit.ConvertDegToRad(double_0), metres1);
            self.ptE = MathHelper.getIntersectionPoint(point3d27, MathHelper.distanceBearingPoint(point3d27, Unit.ConvertDegToRad(double_0 + 90), 100), point3d25, MathHelper.distanceBearingPoint(point3d25, Unit.ConvertDegToRad(double_0), 100));
            self.nominal = PolylineArea();
            point3d24 = MathHelper.distanceBearingPoint(point3d_0, Unit.ConvertDegToRad(double_0 + num15 * 90), 2 * metres);
            point3d26 = MathHelper.distanceBearingPoint(point3d24, Unit.ConvertDegToRad(double_0 + 180), self.ds.Metres);
            point3d28 = MathHelper.distanceBearingPoint(point3d26, Unit.ConvertDegToRad(double_0 - num15 * 90), 2 * metres);
            self.nominal.Add(PolylineAreaPoint(point3d_0, MathHelper.smethod_59(Unit.ConvertDegToRad(double_0), point3d_0, point3d24)));
            self.nominal.method_1(point3d24);
            self.nominal.Add(PolylineAreaPoint(point3d26, MathHelper.smethod_59(Unit.ConvertDegToRad(double_0 + 180), point3d26, point3d28)));
            self.nominal.method_1(point3d28);
            self.nominal.method_1(point3d_0);
            self.spiral = PolylineArea();
            if (MathHelper.calcDistance(point3d, point3d_0) <= num):
                point3d4_11 = []
                MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, Unit.ConvertDegToRad(double_0), 100), point3d, num, point3d4_11);
                point3d4 = point3d4_11[0]
                point3d11 = point3d4_11[1]
                point3d5 = MathHelper.distanceBearingPoint(point3d, MathHelper.getBearing(point3d, point3d10), num);
                self.spiral.Add(PolylineAreaPoint(point3d4, MathHelper.smethod_57(turnDirection, point3d4, point3d5, point3d)));
            else:
                point3d4, point3d5 = MathHelper.smethod_91(point3d_0, 0, point3d, num, turnDirection)
                self.spiral.method_1(point3d4);
            point3d6, point3d7 = MathHelper.smethod_91(point3d, num, point3d1, num1, turnDirection);
            self.spiral.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d6, point3d)));
            self.spiral.method_1(point3d6);
            point3d5 = point3d7;
            point3d6, point3d7 = MathHelper.smethod_91(point3d1, num1, point3d2, num2, turnDirection);
            self.spiral.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d6, point3d1)));
            self.spiral.method_1(point3d6);
            point3d11 = MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(double_0 + 180), num2);
            self.spiral.Add(PolylineAreaPoint(point3d7, MathHelper.smethod_57(turnDirection, point3d7, point3d11, point3d2)));
            self.spiral.method_1(point3d11);
            self.area = PolylineArea();
            point3d4, point3d5 = MathHelper.smethod_91(point3d21, num17, point3d, num, turnDirection);
            point3d6, point3d7 = MathHelper.smethod_91(point3d, num, point3d1, num1, turnDirection);
            self.area.method_1(point3d4);
            self.area.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d6, point3d)));
            self.area.method_1(point3d6);
            point3d4, point3d5 = MathHelper.smethod_91(point3d1, num1, point3d2, num2, turnDirection);
            point3d11 = MathHelper.distanceBearingPoint(point3d22, MathHelper.getBearing(point3d4, point3d5) - num15 * 1.5707963267949, num18);
            if (not MathHelper.smethod_115(point3d11, point3d4, point3d5) if(turnDirection == TurnDirection.Right) else not MathHelper.smethod_119(point3d11, point3d4, point3d5)):
                point3d4, point3d5 = MathHelper.smethod_91(point3d, num, point3d1, num1, turnDirection);
                point3d6, point3d7 = MathHelper.smethod_91(point3d1, num1, point3d2, num2, turnDirection);
                self.area.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d6, point3d1)));
                self.area.method_1(point3d6);
                point3d4, point3d5 = MathHelper.smethod_91(point3d1, num1, point3d2, num2, turnDirection);
                point3d6, point3d7 = MathHelper.smethod_91(point3d2, num2, point3d22, num18, turnDirection);
                self.area.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d6, point3d2)));
                self.area.method_1(point3d6);
            else:
                point3d4, point3d5 = MathHelper.smethod_91(point3d, num, point3d1, num1, turnDirection);
                point3d6, point3d7 = MathHelper.smethod_91(point3d1, num1, point3d22, num18, turnDirection);
                self.area.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d6, point3d1)));
                self.area.method_1(point3d6);
            point3d5 = point3d7;
            point3d6, point3d7 = MathHelper.smethod_91(point3d22, num18, point3d23, num19, turnDirection);
            self.area.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d6, point3d22)));
            self.area.method_1(point3d6);
            point3d5 = point3d7;
            point3d6, point3d7 = MathHelper.smethod_91(point3d23, num19, point3d20, num16, turnDirection);
            self.area.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d6, point3d23)));
            self.area.method_1(point3d6);
            point3d5 = point3d7;
            point3d6, point3d7 = MathHelper.smethod_91(point3d20, num16, point3d21, num17, turnDirection);
            self.area.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d6, point3d20)));
            self.area.method_1(point3d6);
            point3d5 = point3d7;
            point3d6, point3d7 = MathHelper.smethod_91(point3d21, num17, point3d, num, turnDirection);
            self.area.Add(PolylineAreaPoint(point3d5, MathHelper.smethod_57(turnDirection, point3d5, point3d6, point3d21)));
            self.area.method_1(point3d6);
            point3dCollection = []
            point3dCollection.append(MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(double_0), num));
            point3dCollection.append(MathHelper.distanceBearingPoint(point3d1, Unit.ConvertDegToRad(double_0), num1));
            point3dCollection.append(MathHelper.distanceBearingPoint(point3d22, Unit.ConvertDegToRad(double_0 + num15 * 90), num18));
            point3dCollection.append(MathHelper.distanceBearingPoint(point3d23, Unit.ConvertDegToRad(double_0 + 180), num19));
            point3dCollection.append(MathHelper.distanceBearingPoint(point3d21, Unit.ConvertDegToRad(double_0 - num15 * 90), num17));
            self.method_0(point3dCollection);
            self.method_1(MathHelper.distanceBearingPoint(point3d1, Unit.ConvertDegToRad(double_0), num1), MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(double_0 + num15 * 90), num2), MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(double_0 + 180), num2));
        else:
            if (speed_0.Knots < 80):
                raise ValueError("IAS's value must be greater than 80.")
            point3d_0 = point3d_0.smethod_167(0);
            self.tas = Speed.smethod_0(speed_0, double_1, altitude_0);
            self.R = min([943.27 / self.tas.KilometresPerHour, 3]);
            self.radius = Distance(Unit.ConvertKMToMeters(self.tas.KilometresPerHour / (62.8318530717959 * self.R)));
            metresPerSecond = self.tas.MetresPerSecond;
            metres = self.radius.Metres;
            kilometresPerHour = speed_1.KilometresPerHour;
            num = speed_1.MetresPerSecond;
            r = 45 * num / self.R;
            num1 = 11 * num + 4 * r;
            self.wd = distance_0;
            num2 = math.sqrt(math.pow(distance_2.Metres + 11 * self.tas.MetresPerSecond, 2) + math.pow(distance_1.Metres + 2 * metres, 2)) + num1;
            if (self.wd.Metres < num2):
                num3 = MathHelper.smethod_0(Unit.ConvertMeterToNM(num2), 1);
#                 if (WarningMessageBox.smethod_1(iwin32Window_0, string.Format(Confirmations.INSUFFICIENT_DISTANCE_FROM_WPT_TO_OUTBOUND_LEG, num3), ExtendedMessageBoxButtons.YesNo) != ExtendedDialogResult.Yes)
#                 {
#                     throw new AbortException();
#                 }
                self.wd = Distance(num3, DistanceUnits.NM);
            self.ds = Distance(math.sqrt(self.wd.Metres * self.wd.Metres - 4 * metres * metres));
            metres1 = self.ds.Metres / metresPerSecond;
            self.xtt = distance_1;
            self.att = distance_2;
            self.ias = speed_0;
            self.wind = speed_1;
            self.isa = double_1;
            self.altitude = altitude_0;
            self.time = metres1 / 60;
            self.orientation = orientationType_0;
            holdingTemplate = HoldingTemplate(point3d_0, double_0, speed_0, altitude_0, speed_1, double_1, self.time, orientationType_0);
            self.ptBase = point3d_0;
            self.trackDeg = MathHelper.smethod_3(double_0);
            self.trackRad = MathHelper.smethod_4(Unit.ConvertDegToRad(double_0));
            self.arc = holdingTemplate.OutboundLineBottom;
            self.area = holdingTemplate.Area;
            self.spiral = holdingTemplate.Spiral;
            self.nominal = holdingTemplate.Nominal;
            self.ptE = holdingTemplate.PointE;
            self.tas = holdingTemplate.TAS;
            self.radius = holdingTemplate.Radius;
            self.R = holdingTemplate.RateOfTurn;
#     
    def vmethod_1(self, polylineArea_0, bool_0, bool_1, bool_2):
#         Point3d point3d;
#         Point3d point3d1;
#         Point3d point3d2;
#         Point3d point3d3;
#         Point3d point3d4;
#         Point3d point3d5;
#         Point3d point3d6;
#         Point3d point3d7;
#         Point3d point3d8;
#         Point3d point3d9;
#         Point3d point3d10;
#         Point3d point3d11;
#         Point3d point3d12;
#         Point3d point3d13;
#         Point3d point3d14;
#         Point3d point3d15;
#         double num;
#         double num1;
#         double num2;
#         double num3;
#         double num4;
#         double num5;
#         double num6;
#         double num7;
#         Point3d point3d16;
#         double num8;
#         Point3d point3d17;
#         Point3d point3d18;
#         double num9;
#         double num10;
#         Point3d point3d19;
#         Point3d point3d20;
#         Point3d point3d21;
#         Point3d point3d22;
#         Point3d point3d23;
#         Point3d point3d24;
#         Point3d point3d25;
#         double num11;
#         double num12;
#         double num13;
#         double num14;
#         double num15;
#         Point3d point3d26;
#         Point3d point3d27;
#         Point3d point3d28;
#         Point3d point3d29;
#         Point3d point3d30;
#         Point3d point3d31;
#         double num16;
#         double num17;
#         double num18;
#         double num19;
#         Point3d point3d32;
#         Point3d point3d33;
#         Point3d point3d34;
#         Point3d point3d35;
#         double num20;
#         double num21;
#         double num22;
#         double num23;
#         Point3d point3d36;
#         double num24;
#         Point3d point3d37;
#         double num25;
#         PolylineArea polylineArea;
        position = polylineArea_0[0].Position;
        position1 = polylineArea_0[1].Position;
        position2 = polylineArea_0[3].Position;
        position3 = polylineArea_0[2].Position;
        metres = self.wd.Metres;
        metres1 = self.wd.Metres - self.att.Metres;
        metres2 = self.wd.Metres + self.att.Metres;
        holdingTemplate = HoldingTemplate(position, self.trackDeg, self.ias, self.altitude, self.wind, self.isa, self.time, self.orientation);
        holdingTemplate1 = HoldingTemplate(position2, self.trackDeg, self.ias, self.altitude, self.wind, self.isa, self.time, self.orientation);
        position4 = holdingTemplate.OutboundLineTop[0].Position;
        position5 = holdingTemplate.OutboundLineTop[1].Position;
        position6 = holdingTemplate1.OutboundLineBottom[0].Position;
        position7 = holdingTemplate1.OutboundLineBottom[1].Position;
        point3d_5 = []
        MathHelper.smethod_34(position4, position5, self.ptBase, metres2, point3d_5);
        point3d = point3d_5[0]
        point3d5 = point3d_5[1]
        point3d_6 = []
        MathHelper.smethod_34(position6, position7, self.ptBase, metres1, point3d_6);
        point3d = point3d_6[0]
        point3d6 = point3d_6[1]
        point3d_7 = []
        MathHelper.smethod_34(position6, position7, self.ptBase, metres2, point3d_7);
        point3d = point3d_7[0]
        point3d7 = point3d_7[1]        
        if (self.orientation != OrientationType.Right):
            if (MathHelper.smethod_115(point3d6, position2, position3)):
                point3d_6 = []
                MathHelper.smethod_34(position2, position3, self.ptBase, point3d_6);
                point3d = point3d_6[0]
                point3d6 = point3d_6[1]
            if (MathHelper.smethod_115(point3d7, position2, position3)):
                point3d_7 = []
                MathHelper.smethod_34(position2, position3, self.ptBase, metres2, point3d_7);
                point3d = point3d_7[0]
                point3d7 = point3d_7[1] 
        else:
            if (MathHelper.smethod_119(point3d6, position2, position3)):
                MathHelper.smethod_34(position2, position3, self.ptBase, metres1, point3d_6);
                point3d = point3d_6[0]
                point3d6 = point3d_6[1]
            if (MathHelper.smethod_119(point3d7, position2, position3)):
                MathHelper.smethod_34(position2, position3, self.ptBase, metres2, point3d_7);
                point3d = point3d_7[0]
                point3d7 = point3d_7[1]
        point3d38 = MathHelper.distanceBearingPoint(point3d5, MathHelper.getBearing(point3d5, point3d7), MathHelper.calcDistance(point3d5, point3d7) / 2);
        point3d38 = MathHelper.distanceBearingPoint(self.ptBase, MathHelper.getBearing(self.ptBase, point3d38), metres2);
        holdingTemplate2 = HoldingTemplate(point3d5, self.trackDeg + 180, self.ias, self.altitude, self.wind, self.isa, self.time, self.orientation);
        holdingTemplate3 = HoldingTemplate(point3d38, self.trackDeg + 180, self.ias, self.altitude, self.wind, self.isa, self.time, self.orientation);
        holdingTemplate4 = HoldingTemplate(point3d7, self.trackDeg + 180, self.ias, self.altitude, self.wind, self.isa, self.time, self.orientation);
        holdingTemplate5 = HoldingTemplate(point3d6, self.trackDeg + 180, self.ias, self.altitude, self.wind, self.isa, self.time, self.orientation);
        point3d8, num = MathHelper.smethod_73(holdingTemplate1.Spiral[1].Position, holdingTemplate1.Spiral[2].Position, holdingTemplate1.Spiral[1].Bulge);
        point3d9, num1 = MathHelper.smethod_73(holdingTemplate1.Spiral[2].Position, holdingTemplate1.Spiral[3].Position, holdingTemplate1.Spiral[2].Bulge);
        point3d10, num2 = MathHelper.smethod_73(holdingTemplate.Spiral[2].Position, holdingTemplate.Spiral[3].Position, holdingTemplate.Spiral[2].Bulge);
        point3d11, num3 = MathHelper.smethod_73(holdingTemplate2.Spiral[1].Position, holdingTemplate2.Spiral[2].Position, holdingTemplate2.Spiral[1].Bulge);
        point3d12, num4 = MathHelper.smethod_73(holdingTemplate3.Spiral[2].Position, holdingTemplate3.Spiral[3].Position, holdingTemplate3.Spiral[2].Bulge);
        point3d13, num5 = MathHelper.smethod_73(holdingTemplate4.Spiral[2].Position, holdingTemplate4.Spiral[3].Position, holdingTemplate4.Spiral[2].Bulge);
        point3d14, num6 = MathHelper.smethod_73(holdingTemplate4.Spiral[3].Position, holdingTemplate4.Spiral[4].Position, holdingTemplate4.Spiral[3].Bulge);
        point3d15, num7 = MathHelper.smethod_73(holdingTemplate5.Spiral[3].Position, holdingTemplate5.Spiral[4].Position, holdingTemplate5.Spiral[3].Bulge);
        point3d16, num8 = MathHelper.smethod_193(point3d11, num3, point3d12, num4, point3d13, num5, False);
        point3d39 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d11), num8);
        point3d40 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d13), num8);
        num26 = self.trackRad;
        num27 = MathHelper.smethod_4(num26 + 3.14159265358979);
        num28 = 1 if(self.orientation == OrientationType.Right) else -1
        turnDirection = TurnDirection.Right if(self.orientation == OrientationType.Right) else TurnDirection.Left
        turnDirection1 = TurnDirection.Left if(self.orientation == OrientationType.Right) else TurnDirection.Right
        self.nominal = PolylineArea();
        point3d41 = self.ptBase;
        point3d42 = MathHelper.distanceBearingPoint(point3d41, num27 - 1.5707963267949 * num28, 2 * self.radius.Metres);
        self.nominal.method_3(point3d41, MathHelper.smethod_59(num26, point3d41, point3d42));
        self.nominal.method_1(point3d42);
        point3d41 = MathHelper.distanceBearingPoint(point3d42, num27, self.ds.Metres);
        point3d42 = MathHelper.distanceBearingPoint(point3d41, num26 - 1.5707963267949 * num28, 2 * self.radius.Metres);
        self.nominal.method_3(point3d41, MathHelper.smethod_59(num27, point3d41, point3d42));
        self.nominal.method_1(point3d42);
        self.ptC = point3d41;
        num29 = Unit.ConvertDegToRad(70) if(self.orientation == OrientationType.Right) else  Unit.ConvertDegToRad(-70)
        vector3d = Vector3d(0, 0, 1);
#         point3d43 = position.RotateBy(num29, vector3d, self.ptBase);
#         point3d44 = position1.RotateBy(num29, vector3d, self.ptBase);
#         point3d45 = position2.RotateBy(num29, vector3d, self.ptBase);
#         point3d46 = position3.RotateBy(num29, vector3d, self.ptBase);
        matrix3d = Matrix3d.Rotation(num29, vector3d, self.ptBase)
        point3d43 = position.TransformBy(matrix3d);
        point3d44 = position1.TransformBy(matrix3d);
        point3d45 = position2.TransformBy(matrix3d);
        point3d46 = position3.TransformBy(matrix3d);
        polylineArea_0 = PolylineArea();
        point3d41 = MathHelper.distanceBearingPoint(self.ptBase, num27, metres1);
        point3d42 = MathHelper.distanceBearingPoint(self.ptBase, num27, metres2);
        polylineArea_0.method_1(position);
        polylineArea_0.method_3(position1, MathHelper.smethod_60(position1, point3d42, position3));
        polylineArea_0.method_1(position3);
        polylineArea_0.method_3(position2, MathHelper.smethod_60(position2, point3d41, position));
        polylineArea_0.method_1(position);
        polylineArea1 = PolylineArea();
        point3d1, point3d2 = MathHelper.smethod_91(point3d9, num1, point3d10, num2, turnDirection);
        polylineArea1.method_1(point3d1);
        polylineArea1.method_3(point3d2, MathHelper.smethod_57(turnDirection, point3d2, position4, point3d10));
        polylineArea1.method_1(position4);
        polylineArea1.Add(holdingTemplate2.Spiral[0]);
        polylineArea1.method_3(holdingTemplate2.Spiral[1].Position, MathHelper.smethod_57(turnDirection, holdingTemplate2.Spiral[1].Position, point3d39, point3d11));
        polylineArea1.method_3(point3d39, MathHelper.smethod_57(turnDirection, point3d39, point3d40, point3d16));
        polylineArea1.method_3(point3d40, MathHelper.smethod_57(turnDirection, point3d40, holdingTemplate4.Spiral[3].Position, point3d13));
        point3d1, point3d2 = MathHelper.smethod_91(point3d14, num6, point3d15, num7, turnDirection);
        point3d3, point3d4 = MathHelper.smethod_91(point3d15, num7, point3d8, num, turnDirection);
        polylineArea1.method_3(holdingTemplate4.Spiral[3].Position, MathHelper.smethod_57(turnDirection, holdingTemplate4.Spiral[3].Position, point3d1, point3d14));
        polylineArea1.method_1(point3d1);
        polylineArea1.method_3(point3d2, MathHelper.smethod_57(turnDirection, point3d2, point3d3, point3d15));
        polylineArea1.method_1(point3d3);
        polylineArea1.method_3(point3d4, MathHelper.smethod_57(turnDirection, point3d4, holdingTemplate1.Spiral[2].Position, point3d8));
        polylineArea1.method_3(holdingTemplate1.Spiral[2].Position, MathHelper.smethod_57(turnDirection, holdingTemplate1.Spiral[2].Position, polylineArea1[0].Position, point3d9));
        polylineArea1.method_1(polylineArea1[0].Position);
        holdingTemplate6 = HoldingTemplate(point3d43, Unit.smethod_1(MathHelper.getBearing(point3d44, point3d43)), self.ias, self.altitude, self.wind, self.isa, self.time, OrientationType.Right if(self.orientation == OrientationType.Left) else OrientationType.Left);
        holdingTemplate7 = HoldingTemplate(point3d45, Unit.smethod_1(MathHelper.getBearing(point3d46, point3d45)), self.ias, self.altitude, self.wind, self.isa, self.time, OrientationType.Right if(self.orientation == OrientationType.Left) else OrientationType.Left);
        point3d17, num9 = MathHelper.smethod_73(holdingTemplate6.Spiral[2].Position, holdingTemplate6.Spiral[3].Position, holdingTemplate6.Spiral[2].Bulge);
        point3d18, num10 = MathHelper.smethod_73(holdingTemplate7.Spiral[2].Position, holdingTemplate7.Spiral[3].Position, holdingTemplate7.Spiral[2].Bulge);
        point3d47 = MathHelper.distanceBearingPoint(point3d17, MathHelper.getBearing(position6, position7) + 1.5707963267949 * num28, num9);
        point3d48 = MathHelper.distanceBearingPoint(point3d47, MathHelper.getBearing(position6, position7), 1000);
        point3d_48 = []
        MathHelper.smethod_34(point3d47, point3d48, self.ptBase, metres2, point3d_48);
        point3d = point3d_48[0]
        point3d48 = point3d_48[1]
        point3d49 = MathHelper.distanceBearingPoint(point3d18, MathHelper.getBearing(position6, position7) + 1.5707963267949 * num28, num10);
        point3d50 = MathHelper.distanceBearingPoint(point3d49, MathHelper.getBearing(position6, position7), 1000);
        point3d_50 = []
        MathHelper.smethod_34(point3d49, point3d50, self.ptBase, metres2, point3d_50);
        point3d = point3d_50[0]
        point3d50 = point3d_50[1]
        polylineArea2 = PolylineArea();
        flag = False;
        point3d_0 = []
        if (MathHelper.smethod_34(point3d47, point3d48, point3d18, num10, point3d_0) != IntersectionStatus.Nothing):
            polylineArea2.method_1(holdingTemplate6.Spiral[0].Position);
            polylineArea2.method_3(holdingTemplate6.Spiral[1].Position, holdingTemplate6.Spiral[1].Bulge);
            point3d1, point3d2 = MathHelper.smethod_91(point3d17, num9, point3d18, num10, turnDirection1);
            polylineArea2.method_3(holdingTemplate6.Spiral[2].Position, MathHelper.smethod_57(turnDirection1, holdingTemplate6.Spiral[2].Position, point3d1, point3d17));
            polylineArea2.method_1(point3d1);
            polylineArea2.method_3(point3d2, MathHelper.smethod_57(turnDirection1, point3d2, point3d49, point3d18));
            polylineArea2.method_1(point3d49);
        else:
            polylineArea2.method_1(holdingTemplate6.Spiral[0].Position);
            polylineArea2.method_3(holdingTemplate6.Spiral[1].Position, holdingTemplate6.Spiral[1].Bulge);
            polylineArea2.method_3(holdingTemplate6.Spiral[2].Position, MathHelper.smethod_57(turnDirection1, holdingTemplate6.Spiral[2].Position, point3d47, point3d17));
            polylineArea2.method_1(point3d47);
            point3d50 = point3d48;
            flag = True;
        point3d_19 = []
        MathHelper.smethod_34(position, position1, self.ptBase, metres2, point3d_19);
        point3d = point3d_19[0]
        point3d19 = point3d_19[1]
        point3d_20 = []
        MathHelper.smethod_34(position, position1, self.ptBase, metres1, point3d_20);
        point3d = point3d_20[0]
        point3d20 = point3d_20[1]
        point3d51 = MathHelper.distanceBearingPoint(point3d50, MathHelper.getBearing(point3d50, point3d19), MathHelper.calcDistance(point3d50, point3d19) / 2);
        point3d51 = MathHelper.distanceBearingPoint(self.ptBase, MathHelper.getBearing(self.ptBase, point3d51), metres2);
        holdingTemplate8 = HoldingTemplate(point3d50, self.trackDeg + 180, self.ias, self.altitude, self.wind, self.isa, self.time, OrientationType.Right if(self.orientation == OrientationType.Left) else OrientationType.Left);
        holdingTemplate9 = HoldingTemplate(point3d51, self.trackDeg + 180, self.ias, self.altitude, self.wind, self.isa, self.time, OrientationType.Right if(self.orientation == OrientationType.Left) else OrientationType.Left);
        holdingTemplate10 = HoldingTemplate(point3d19, self.trackDeg + 180, self.ias, self.altitude, self.wind, self.isa, self.time, OrientationType.Right if(self.orientation == OrientationType.Left) else OrientationType.Left);
        holdingTemplate11 = HoldingTemplate(point3d20, self.trackDeg + 180, self.ias, self.altitude, self.wind, self.isa, self.time, OrientationType.Right if(self.orientation == OrientationType.Left) else OrientationType.Left);
        point3d21, num11 = MathHelper.smethod_73(holdingTemplate8.Spiral[1].Position, holdingTemplate8.Spiral[2].Position, holdingTemplate8.Spiral[1].Bulge);
        point3d22, num12 = MathHelper.smethod_73(holdingTemplate9.Spiral[2].Position, holdingTemplate9.Spiral[3].Position, holdingTemplate9.Spiral[2].Bulge);
        point3d23, num13 = MathHelper.smethod_73(holdingTemplate10.Spiral[2].Position, holdingTemplate10.Spiral[3].Position, holdingTemplate10.Spiral[2].Bulge);
        point3d24, num14 = MathHelper.smethod_73(holdingTemplate10.Spiral[3].Position, holdingTemplate10.Spiral[4].Position, holdingTemplate10.Spiral[3].Bulge);
        point3d25, num15 = MathHelper.smethod_73(holdingTemplate11.Spiral[3].Position, holdingTemplate11.Spiral[4].Position, holdingTemplate11.Spiral[3].Bulge);
        point3d16, num8 = MathHelper.smethod_193(point3d21, num11, point3d22, num12, point3d23, num13, False);
        point3d39 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d21), num8);
        point3d40 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d23), num8);
        polylineArea2.method_1(point3d50);
        polylineArea2.method_3(holdingTemplate8.Spiral[1].Position, MathHelper.smethod_57(turnDirection1, holdingTemplate8.Spiral[1].Position, point3d39, point3d21));
        polylineArea2.method_3(point3d39, MathHelper.smethod_57(turnDirection1, point3d39, point3d40, point3d16));
        polylineArea2.method_3(point3d40, MathHelper.smethod_57(turnDirection1, point3d40, holdingTemplate10.Spiral[3].Position, point3d23));
        point3d1, point3d2 = MathHelper.smethod_91(point3d24, num14, point3d25, num15, turnDirection1);
        polylineArea2.method_3(holdingTemplate10.Spiral[3].Position, MathHelper.smethod_57(turnDirection1, holdingTemplate10.Spiral[3].Position, point3d1, point3d24));
        polylineArea2.method_1(point3d1);
        polylineArea2.method_3(point3d2, MathHelper.smethod_57(turnDirection1, point3d2, holdingTemplate11.Spiral[4].Position, point3d25));
        polylineArea2.Add(holdingTemplate11.Spiral[4]);
        polylineArea2.method_1(point3d43);
        point3d41 = MathHelper.distanceBearingPoint(position, MathHelper.getBearing(position, position1) - Unit.ConvertDegToRad(35) * num28, 1000);
        point3d_26 = []
        MathHelper.smethod_34(position, point3d41, self.ptBase, metres2, point3d_26);
        point3d = point3d_26[0]
        point3d26 = point3d_26[1]
        point3d41 = MathHelper.distanceBearingPoint(position3, MathHelper.getBearing(position2, position3) - Unit.ConvertDegToRad(25) * num28, 1000);
        point3d_27 = []
        MathHelper.smethod_34(position3, point3d41, self.ptBase, metres2, point3d_27);
        point3d = point3d_27[0]
        point3d27 = point3d_27[1]
        point3d52 = MathHelper.distanceBearingPoint(point3d26, MathHelper.getBearing(point3d26, point3d27), MathHelper.calcDistance(point3d26, point3d27) / 2);
        point3d52 = MathHelper.distanceBearingPoint(self.ptBase, MathHelper.getBearing(self.ptBase, point3d52), metres2);
        holdingTemplate12 = HoldingTemplate(point3d26, self.trackDeg + 180 - 30 * num28, self.ias, self.altitude, self.wind, self.isa, self.time, self.orientation);
        holdingTemplate13 = HoldingTemplate(point3d52, self.trackDeg + 180 - 30 * num28, self.ias, self.altitude, self.wind, self.isa, self.time, self.orientation);
        holdingTemplate14 = HoldingTemplate(point3d27, self.trackDeg + 180 - 30 * num28, self.ias, self.altitude, self.wind, self.isa, self.time, self.orientation);
        point3d28, num16 = MathHelper.smethod_73(holdingTemplate12.Spiral[1].Position, holdingTemplate12.Spiral[2].Position, holdingTemplate12.Spiral[1].Bulge);
        point3d29, num17 = MathHelper.smethod_73(holdingTemplate12.Spiral[2].Position, holdingTemplate12.Spiral[3].Position, holdingTemplate12.Spiral[2].Bulge);
        point3d30, num18 = MathHelper.smethod_73(holdingTemplate13.Spiral[2].Position, holdingTemplate13.Spiral[3].Position, holdingTemplate13.Spiral[2].Bulge);
        point3d31, num19 = MathHelper.smethod_73(holdingTemplate14.Spiral[2].Position, holdingTemplate14.Spiral[3].Position, holdingTemplate14.Spiral[2].Bulge);
        point3d16, num8 = MathHelper.smethod_193(point3d29, num17, point3d30, num18, point3d31, num19, False);
        point3d39 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d29), num8);
        point3d40 = MathHelper.distanceBearingPoint(point3d16, MathHelper.getBearing(point3d16, point3d31), num8);
        polylineArea3 = PolylineArea(None, holdingTemplate12.Spiral[0].Position)
        polylineArea3.method_3(holdingTemplate12.Spiral[1].Position, MathHelper.smethod_57(turnDirection, holdingTemplate12.Spiral[1].Position, point3d39, point3d28));
        polylineArea3.method_3(point3d39, MathHelper.smethod_57(turnDirection, point3d39, point3d40, point3d16));
        polylineArea3.method_3(point3d40, MathHelper.smethod_57(turnDirection, point3d40, holdingTemplate14.Spiral[3].Position, point3d31));
        polylineArea3.Add(holdingTemplate14.Spiral[3]);
        polylineArea3.Add(holdingTemplate14.Spiral[4]);
        polylineArea3.Add(holdingTemplate12.Spiral[0]);
        holdingTemplate15 = HoldingTemplate(point3d43, Unit.smethod_1(MathHelper.getBearing(point3d44, point3d43)), self.ias, self.altitude, self.wind, self.isa, self.time, self.orientation);
        holdingTemplate16 = HoldingTemplate(point3d45, Unit.smethod_1(MathHelper.getBearing(point3d46, point3d45)), self.ias, self.altitude, self.wind, self.isa, self.time, self.orientation);
        point3d32, num20 = MathHelper.smethod_73(holdingTemplate16.Spiral[1].Position, holdingTemplate16.Spiral[2].Position, holdingTemplate16.Spiral[1].Bulge);
        point3d33, num21 = MathHelper.smethod_73(holdingTemplate16.Spiral[2].Position, holdingTemplate16.Spiral[3].Position, holdingTemplate16.Spiral[2].Bulge);
        point3d34, num22 = MathHelper.smethod_73(holdingTemplate15.Spiral[2].Position, holdingTemplate15.Spiral[3].Position, holdingTemplate15.Spiral[2].Bulge);
        point3d35, num23 = MathHelper.smethod_73(holdingTemplate15.Spiral[3].Position, holdingTemplate15.Spiral[4].Position, holdingTemplate15.Spiral[3].Bulge);
        polylineArea4 = PolylineArea();
        if (not bool_0):
            point3d1, point3d2 = MathHelper.smethod_91(point3d33, num21, point3d34, num22, turnDirection);
            polylineArea4.Add(holdingTemplate16.Spiral[0]);
            polylineArea4.Add(holdingTemplate16.Spiral[1]);
            polylineArea4.method_3(holdingTemplate16.Spiral[2].Position, MathHelper.smethod_57(turnDirection, holdingTemplate16.Spiral[2].Position, point3d1, point3d33));
            polylineArea4.method_1(point3d1);
            polylineArea4.method_3(point3d2, MathHelper.smethod_57(turnDirection, point3d2, holdingTemplate15.Spiral[3].Position, point3d34));
            polylineArea4.Add(holdingTemplate15.Spiral[3]);
            polylineArea4.Add(holdingTemplate15.Spiral[4]);
            polylineArea4.Add(holdingTemplate16.Spiral[0]);
        elif (not flag):
            point3d37, num25 = MathHelper.smethod_73(holdingTemplate7.Spiral[3].Position, holdingTemplate7.Spiral[4].Position, holdingTemplate7.Spiral[3].Bulge);
            point3d1, point3d2 = MathHelper.smethod_91(point3d18, num10, point3d34, num22, turnDirection);
            polylineArea4.method_3(holdingTemplate7.Spiral[4].Position, MathHelper.smethod_57(turnDirection, holdingTemplate7.Spiral[4].Position, holdingTemplate7.Spiral[3].Position, point3d37));
            polylineArea4.method_3(holdingTemplate7.Spiral[3].Position, MathHelper.smethod_57(turnDirection, holdingTemplate7.Spiral[3].Position, point3d1, point3d18));
            polylineArea4.method_1(point3d1);
            polylineArea4.method_3(point3d2, MathHelper.smethod_57(turnDirection, point3d2, holdingTemplate15.Spiral[3].Position, point3d34));
            polylineArea4.Add(holdingTemplate15.Spiral[3]);
            polylineArea4.Add(holdingTemplate15.Spiral[4]);
            polylineArea4.method_1(holdingTemplate7.Spiral[4].Position);
        else:
            point3d36, num24 = MathHelper.smethod_73(holdingTemplate8.Spiral[2].Position, holdingTemplate8.Spiral[3].Position, holdingTemplate8.Spiral[2].Bulge);
            point3d1, point3d2 = MathHelper.smethod_91(point3d21, num11, point3d34, num22, turnDirection);
            polylineArea4.method_3(holdingTemplate8.Spiral[3].Position, MathHelper.smethod_57(turnDirection, holdingTemplate8.Spiral[3].Position, holdingTemplate8.Spiral[2].Position, point3d36));
            polylineArea4.method_3(holdingTemplate8.Spiral[2].Position, MathHelper.smethod_57(turnDirection, holdingTemplate8.Spiral[2].Position, point3d1, point3d21));
            polylineArea4.method_1(point3d1);
            polylineArea4.method_3(point3d2, MathHelper.smethod_57(turnDirection, point3d2, holdingTemplate15.Spiral[3].Position, point3d34));
            polylineArea4.Add(holdingTemplate15.Spiral[3]);
            polylineArea4.Add(holdingTemplate15.Spiral[4]);
            polylineArea4.method_1(holdingTemplate8.Spiral[3].Position);
#         DBObjectCollection dBObjectCollection = null;
#         DBObjectCollection dBObjectCollection1 = null;
#         try
#         {
#             dBObjectCollection1 = new DBObjectCollection();
#             dBObjectCollection1.Add(AcadHelper.smethod_136(polylineArea1, true));
#             if (bool_0)
#             {
#                 dBObjectCollection1.Add(AcadHelper.smethod_136(polylineArea2, true));
#             }
#             if (bool_1)
#             {
#                 dBObjectCollection1.Add(AcadHelper.smethod_136(polylineArea3, true));
#             }
#             if (bool_2)
#             {
#                 dBObjectCollection1.Add(AcadHelper.smethod_136(polylineArea4, true));
#             }
#             dBObjectCollection = Region.CreateFromCurves(dBObjectCollection1);
#             for (int i = 1; i < dBObjectCollection.get_Count(); i++)
#             {
#                 (dBObjectCollection.get_Item(0) as Region).BooleanOperation(0, dBObjectCollection.get_Item(i) as Region);
#             }
#             polylineArea = PolylineArea.smethod_0(dBObjectCollection.get_Item(0) as Region);
#         }
#         finally
#         {
#             AcadHelper.smethod_25(dBObjectCollection1);
#             AcadHelper.smethod_25(dBObjectCollection);
#         }
#         return polylineArea;
#     }
        polylineAreaList = []
        polylineAreaList.append(polylineArea1)
        # resultPolygon = None
        # polygon1 = QgsGeometry.fromPolygon([polylineArea1.method_14_closed()])
        if bool_0:
            # polygon1 = polygon1.intersection(QgsGeometry.fromPolygon([polylineArea2.method_14_closed()]))
            polylineAreaList.append(polylineArea2)
        if bool_1:
            # polygon1 = polygon1.intersection(QgsGeometry.fromPolygon([polylineArea3.method_14_closed()]))
            polylineAreaList.append(polylineArea3)
        if bool_2:
            # polygon1 = polygon1.intersection(QgsGeometry.fromPolygon([polylineArea4.method_14_closed()]))

            polylineAreaList.append(polylineArea4)
        pointArray = QgisHelper.convexFull(polylineAreaList)
        # polylineAreaList.append(PolylineArea(pointArrayList[0]))
        return [PolylineArea(pointArray)]