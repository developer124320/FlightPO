'''
Created on 2 Jul 2015

@author: Administrator
'''
from FlightPlanner.types import Point3D
from FlightPlanner.Holding.HoldingTemplateBase import HoldingTemplateBase
from FlightPlanner.helpers import MathHelper, Speed, Unit, Distance
from FlightPlanner.types import DistanceUnits, OrientationType, TurnDirection, Matrix3d, Vector3d, Point3D
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint

import math

class HoldingTemplate(HoldingTemplateBase):
    '''
    classdocs
    '''


    def __init__(self, point3d_0, double_0, speed_0, altitude_0, speed_1, double_1, double_2, orientationType_0):
        '''
        Constructor
        '''
#         double num;
#         double num1;
#         double num2;
#         double num3;
#         double num4;
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
#         Point3d point3d16;
#         Point3d point3d17;
#         Point3d point3d18;
#         Point3d point3d19;
#         Point3d point3d20;
#         Point3d point3d21;
#         Point3d point3d22;
#         Point3d point3d23;
#         Point3d point3d24;
#         Point3d point3d25;
#         Point3d point3d26;
#         Point3d point3d27;
#         Point3d point3d28;
#         Point3d point3d29;
#         Point3d point3d30;
#         Point3d point3d31;
#         Point3d point3d32;
#         Point3d point3d33;
#         Point3d point3d34;
#         Point3d point3d35;
        point3d_0 = point3d_0.smethod_167(0);
        self.ptBase = point3d_0;
        self.trackDeg = MathHelper.smethod_3(double_0);
        self.trackRad = MathHelper.smethod_4(Unit.ConvertDegToRad(double_0));
        self.orientation = orientationType_0;
        self.tas = Speed.smethod_0(speed_0, double_1, altitude_0);
        self.R = min([943.27 / self.tas.KilometresPerHour, 3]);
        self.radius = Distance(Unit.ConvertKMToMeters(self.tas.KilometresPerHour / (62.8318530717959 * self.R)));
        metresPerSecond = self.tas.MetresPerSecond;
        metres = self.radius.Metres;
        kilometresPerHour = speed_1.KilometresPerHour;
        metresPerSecond1 = speed_1.MetresPerSecond;
        r = 45 * metresPerSecond1 / self.R;
        double2 = double_2 * 60;
        self.ds = Distance(metresPerSecond * double2);
        self.wd = Distance(math.sqrt(self.ds.Metres * self.ds.Metres + 4 * metres * metres));
        num5 = 5 * metresPerSecond;
        num6 = 11 * metresPerSecond;
        num7 = (double2 - 5) * metresPerSecond;
        num8 = (double2 - 5) * metresPerSecond;
        num9 = (double2 + 21) * metresPerSecond;
        num10 = (double2 + 21) * metresPerSecond;
        num11 = 5 * metresPerSecond1;
        num12 = 11 * metresPerSecond1;
        num13 = num12 + r;
        num14 = num12 + 2 * r;
        num15 = num12 + 3 * r;
        num16 = num12 + 4 * r;
        num17 = num11 + 5 * r;
        num18 = num11 + 6 * r;
        num19 = (double2 + 6) * metresPerSecond1 + 4 * r;
        num20 = (double2 + 6) * metresPerSecond1 + 4 * r;
        num21 = num19 + 14 * metresPerSecond1;
        num22 = num19 + 14 * metresPerSecond1;
        num23 = num21 + r;
        num24 = num21 + 2 * r;
        num25 = num21 + 2 * r;
        num26 = num21 + 3 * r;
        num27 = num19 + 4 * r;
        num28 = num21 + 4 * r;
        r1 = 2 * metres + (double2 + 15) * metresPerSecond + (double2 + 26 + 195 / self.R) * metresPerSecond1;
        num29 = 11 * metresPerSecond * math.cos(Unit.ConvertDegToRad(20)) + metres * (1 + math.sin(Unit.ConvertDegToRad(20))) + (double2 + 15) * metresPerSecond * math.tan(Unit.ConvertDegToRad(5)) + (double2 + 26 + 125 / self.R) * metresPerSecond1;
        self.ias = speed_0;
        self.wind = speed_1;
        self.isa = double_1;
        self.altitude = altitude_0;
        self.time = double_2;
        num30 = 1 if(orientationType_0 == OrientationType.Right) else -1
        turnDirection = TurnDirection.Right if(orientationType_0 == OrientationType.Right) else TurnDirection.Left
        turnDirection1 = TurnDirection.Left if(orientationType_0 == OrientationType.Right) else TurnDirection.Right
        point3d36 = MathHelper.distanceBearingPoint(point3d_0, 0, 0);
        point3d37 = MathHelper.distanceBearingPoint(point3d36, Unit.ConvertDegToRad(double_0), num5);
        point3d38 = MathHelper.distanceBearingPoint(point3d36, Unit.ConvertDegToRad(double_0), num6);
        point3d39 = MathHelper.distanceBearingPoint(point3d38, Unit.ConvertDegToRad(double_0 + num30 * 90), metres);
        point3d40 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0 + num30 * -45), metres);
        point3d41 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0), metres);
        point3d42 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0 + num30 * 45), metres);
        point3d43 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0 + num30 * 90), metres);
        point3d39 = MathHelper.distanceBearingPoint(point3d37, Unit.ConvertDegToRad(double_0 + num30 * 90), metres);
        MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0 + num30 * 90), metres);
        point3d44 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0 + num30 * 135), metres);
        point3d45 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0 + 180), metres);
        point3d46 = MathHelper.distanceBearingPoint(point3d43, Unit.ConvertDegToRad(double_0 + 180 - num30 * 5), num7);
        point3d47 = MathHelper.distanceBearingPoint(point3d43, Unit.ConvertDegToRad(double_0 + 180 - num30 * 5), num9);
        point3d48 = MathHelper.distanceBearingPoint(point3d43, Unit.ConvertDegToRad(double_0 + 180 + num30 * 5), num8);
        point3d49 = MathHelper.distanceBearingPoint(point3d43, Unit.ConvertDegToRad(double_0 + 180 + num30 * 5), num10);
        point3d39 = MathHelper.distanceBearingPoint(point3d47, Unit.ConvertDegToRad(double_0 - num30 * 90), metres);
        point3d50 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0 + 180 - num30 * 45), metres);
        point3d51 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0 + 180), metres);
        MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0 + num30 * 90), metres);
        point3d39 = MathHelper.distanceBearingPoint(point3d49, Unit.ConvertDegToRad(double_0 - num30 * 90), metres);
        point3d52 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0 + 180), metres);
        point3d53 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0 + 180 + num30 * 45), metres);
        point3d54 = MathHelper.distanceBearingPoint(point3d39, Unit.ConvertDegToRad(double_0 - num30 * 90), metres);
        point3d55 = MathHelper.distanceBearingPoint(point3d48, Unit.ConvertDegToRad(double_0 - num30 * 90), metres * 2);
        point3d, num = MathHelper.smethod_193(point3d38, num12, point3d40, num13, point3d41, num14, False);
        point3d1, num1 = MathHelper.smethod_193(point3d41, num14, point3d42, num15, point3d43, num16, False);
        point3d2, num2 = MathHelper.smethod_193(point3d43, num16, point3d44, num17, point3d45, num18, False);
        point3d3, num3 = MathHelper.smethod_193(point3d47, num21, point3d50, num23, point3d51, num24, False);
        point3d4, num4 = MathHelper.smethod_193(point3d52, num25, point3d53, num26, point3d54, num28, False);
        point3d56 = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(double_0 - num30 * 90), num4);
        point3d57 = MathHelper.distanceBearingPoint(point3d56, Unit.ConvertDegToRad(double_0 + num30 * 90), num29);
        point3d58 = MathHelper.distanceBearingPoint(point3d3, Unit.ConvertDegToRad(double_0 + 180), num3);
        point3d58 = MathHelper.getIntersectionPoint(point3d_0, MathHelper.distanceBearingPoint(point3d_0, Unit.ConvertDegToRad(double_0 + 180), 100), point3d58, MathHelper.distanceBearingPoint(point3d58, Unit.ConvertDegToRad(double_0 + 90), 100));
        point3d59 = MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(double_0 + 180), num4);
        point3d59 = MathHelper.getIntersectionPoint(point3d_0, MathHelper.distanceBearingPoint(point3d_0, Unit.ConvertDegToRad(double_0 + 180), 100), point3d59, MathHelper.distanceBearingPoint(point3d59, Unit.ConvertDegToRad(double_0 + 90), 100));
        point3d5 = MathHelper.distanceBearingPoint(point3d58, Unit.ConvertDegToRad(double_0), r1) if(MathHelper.calcDistance(point3d_0, point3d58) >= MathHelper.calcDistance(point3d_0, point3d59)) else MathHelper.distanceBearingPoint(point3d59, Unit.ConvertDegToRad(double_0), r1)
        self.ptE = MathHelper.getIntersectionPoint(point3d5, MathHelper.distanceBearingPoint(point3d5, Unit.ConvertDegToRad(double_0 + 90), 100), point3d57, MathHelper.distanceBearingPoint(point3d57, Unit.ConvertDegToRad(double_0), 100));
        self.nominal = PolylineArea();
        point3d56 = MathHelper.distanceBearingPoint(point3d_0, Unit.ConvertDegToRad(double_0 + num30 * 90), 2 * metres);
        point3d58 = MathHelper.distanceBearingPoint(point3d56, Unit.ConvertDegToRad(double_0 + 180), self.ds.Metres);
        point3d59 = MathHelper.distanceBearingPoint(point3d58, Unit.ConvertDegToRad(double_0 - num30 * 90), 2 * metres);
        self.nominal.Add(PolylineAreaPoint(point3d_0, MathHelper.smethod_59(Unit.ConvertDegToRad(double_0), point3d_0, point3d56)));
        self.nominal.method_1(point3d56);
        self.nominal.Add(PolylineAreaPoint(point3d58, MathHelper.smethod_59(Unit.ConvertDegToRad(double_0 + 180), point3d58, point3d59)));
        self.nominal.method_1(point3d59);
        self.nominal.method_1(point3d_0);
        self.wd = Distance(MathHelper.calcDistance(point3d_0, point3d58));
        self.area = PolylineArea();
        point3dCollection = [] 
        point3dCollection.append(MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(double_0), num));
        point3dCollection.append(MathHelper.distanceBearingPoint(point3d1, Unit.ConvertDegToRad(double_0), num1));
        point3dCollection.append(MathHelper.distanceBearingPoint(point3d3, Unit.ConvertDegToRad(double_0 + num30 * 90), num3));
        point3dCollection.append(MathHelper.distanceBearingPoint(point3d3, Unit.ConvertDegToRad(double_0 + 180), num3));
        point3dCollection.append(MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(double_0 + 180), num4));
        point3dCollection.append(MathHelper.distanceBearingPoint(point3d4, Unit.ConvertDegToRad(double_0 - num30 * 90), num4));
        point3dCollection.append(MathHelper.distanceBearingPoint(point3d55, Unit.ConvertDegToRad(double_0), num27));
        point3d7, point3d8 = MathHelper.smethod_91(point3d3, num3, point3d4, num4, turnDirection);
        point3d9, point3d10 = MathHelper.smethod_91(point3d4, num4, point3d55, num27, turnDirection);
        point3d11, point3d12 = MathHelper.smethod_91(point3d4, num4, point3d, num, turnDirection);
        point3d13, point3d14 = MathHelper.smethod_91(point3d4, num4, point3d1, num1, turnDirection);
        point3d15, point3d16 = MathHelper.smethod_91(point3d4, num4, point3d3, num3, turnDirection);
        point3d17, point3d18 = MathHelper.smethod_91(point3d55, num27, point3d, num, turnDirection);
        point3d19, point3d20 = MathHelper.smethod_91(point3d55, num27, point3d1, num1, turnDirection);
        point3d21, point3d22 = MathHelper.smethod_91(point3d55, num27, point3d3, num3, turnDirection);
        point3d23, point3d6 = MathHelper.smethod_91(point3d, num, point3d1, num1, turnDirection);
        point3d24, point3d25 = MathHelper.smethod_91(point3d1, num1, point3d46, num19, turnDirection);
        point3d26, point3d27 = MathHelper.smethod_91(point3d46, num19, point3d3, num3, turnDirection);
        point3d28, point3d29 = MathHelper.smethod_91(point3d43, num16, point3d48, num20, turnDirection1);
        point3d30, point3d31 = MathHelper.smethod_91(point3d48, num20, point3d49, num22, turnDirection1);
        if (num4 >= MathHelper.calcDistance(point3d4, point3d55) + num27):
            self.area.method_1(point3d7);
            self.area.method_3(point3d8, MathHelper.smethod_57(turnDirection, point3d8, point3d9, point3d4));
            self.area.method_1(point3d9);
            if (num27 <= MathHelper.calcDistance(point3d55, point3d1) + num1):
                flag = False;
                if (num27 < MathHelper.calcDistance(point3d55, point3d) + num):
                    point3d39 = MathHelper.distanceBearingPoint(point3d18, MathHelper.getBearing(point3d17, point3d18) + 1.5707963267949 * num30, 100);
                    flag = MathHelper.smethod_119(point3d23, point3d18, point3d39) if(turnDirection != TurnDirection.Right) else MathHelper.smethod_115(point3d23, point3d18, point3d39)
                if (flag):
                    self.area.Add(PolylineAreaPoint(point3d10, MathHelper.smethod_57(turnDirection, point3d10, point3d17, point3d55)));
                    self.area.method_1(point3d17);
                    self.area.method_3(point3d18, MathHelper.smethod_57(turnDirection, point3d18, point3d23, point3d));
                    self.area.method_3(point3d23, MathHelper.smethod_57(turnDirection, point3d23, point3d24, point3d1));
                    self.area.method_1(point3d24);
                else:
                    self.area.Add(PolylineAreaPoint(point3d10, MathHelper.smethod_57(turnDirection, point3d10, point3d19, point3d55)));
                    self.area.method_1(point3d19);
                    self.area.Add(PolylineAreaPoint(point3d20, MathHelper.smethod_57(turnDirection, point3d20, point3d24, point3d1)));
                    self.area.method_1(point3d24);
                self.area.method_3(point3d25, MathHelper.smethod_57(turnDirection, point3d25, point3d26, point3d46));
                self.area.method_1(point3d26);
                self.area.method_3(point3d27, MathHelper.smethod_57(turnDirection, point3d27, point3d7, point3d3));
                self.area.method_1(point3d7);
            else:
                self.area.method_3(point3d10, MathHelper.smethod_57(turnDirection, point3d10, point3d21, point3d55));
                self.area.method_1(point3d21);
                self.area.method_3(point3d22, MathHelper.smethod_57(turnDirection, point3d22, point3d7, point3d3));
                self.area.method_1(point3d7);
        elif (num4 <= MathHelper.calcDistance(point3d4, point3d1) + num1):
            flag1 = False;
            if (num4 < MathHelper.calcDistance(point3d4, point3d) + num):
                point3d39 = MathHelper.distanceBearingPoint(point3d12, MathHelper.getBearing(point3d11, point3d12) + 1.5707963267949 * num30, 100);
                flag1 = MathHelper.smethod_119(point3d23, point3d12, point3d39) if(turnDirection != TurnDirection.Right) else MathHelper.smethod_115(point3d23, point3d12, point3d39)
            if (flag1):
                self.area.method_1(point3d7);
                self.area.method_3(point3d8, MathHelper.smethod_57(turnDirection, point3d8, point3d11, point3d4));
                self.area.method_1(point3d11);
                self.area.method_3(point3d12, MathHelper.smethod_57(turnDirection, point3d12, point3d23, point3d));
                self.area.method_3(point3d23, MathHelper.smethod_57(turnDirection, point3d23, point3d24, point3d1));
                self.area.method_1(point3d24);
            else:
                self.area.method_1(point3d7);
                self.area.method_3(point3d8, MathHelper.smethod_57(turnDirection, point3d8, point3d13, point3d4));
                self.area.method_1(point3d13);
                self.area.method_3(point3d14, MathHelper.smethod_57(turnDirection, point3d14, point3d24, point3d1));
                self.area.method_1(point3d24);
            self.area.method_3(point3d25, MathHelper.smethod_57(turnDirection, point3d25, point3d26, point3d46));
            self.area.method_1(point3d26);
            self.area.method_3(point3d27, MathHelper.smethod_57(turnDirection, point3d27, point3d7, point3d3));
            self.area.method_1(point3d7);
        else:
            self.area.method_1(point3d7);
            self.area.method_3(point3d8, MathHelper.smethod_57(turnDirection, point3d8, point3d15, point3d4));
            self.area.method_1(point3d15);
            self.area.method_3(point3d16, MathHelper.smethod_57(turnDirection, point3d16, point3d7, point3d3));
            self.area.method_1(point3d7);
        self.outboundLineTop = PolylineArea();
        self.outboundLineTop.method_1(point3d24);
        self.outboundLineTop.method_3(point3d25, MathHelper.smethod_57(turnDirection, point3d25, point3d26, point3d46));
#         PolylineArea polylineArea = self.outboundLineTop;
        point3dArray = [point3d26, point3d27]
        self.outboundLineTop.method_7(point3dArray);
        self.outboundLineBottom = PolylineArea();
        self.outboundLineBottom.method_1(point3d28);
        self.outboundLineBottom.method_3(point3d29, MathHelper.smethod_57(turnDirection1, point3d29, point3d30, point3d48));
#         PolylineArea polylineArea1 = self.outboundLineBottom;
        point3dArray = [point3d30, point3d31]
        self.outboundLineBottom.method_7(point3dArray);
        self.spiral = PolylineArea();
        if (MathHelper.calcDistance(point3d, point3d_0) <= num):
            point3d32_39 = []
            MathHelper.smethod_34(point3d_0, MathHelper.distanceBearingPoint(point3d_0, Unit.ConvertDegToRad(double_0), 100), point3d, num, point3d32_39);
            point3d32 = point3d32_39[0]
            point3d39 = point3d32_39[1]
            point3d33 = MathHelper.distanceBearingPoint(point3d, MathHelper.getBearing(point3d, point3d38), num);
            self.spiral.Add(PolylineAreaPoint(point3d32, MathHelper.smethod_57(turnDirection, point3d32, point3d33, point3d)));
        else:
            point3d32, point3d33 = MathHelper.smethod_91(point3d_0, 0, point3d, num, turnDirection);
            self.spiral.method_1(point3d32);
        point3d34, point3d35 = MathHelper.smethod_91(point3d, num, point3d1, num1, turnDirection);
        self.spiral.Add(PolylineAreaPoint(point3d33, MathHelper.smethod_57(turnDirection, point3d33, point3d34, point3d)));
        point3d33 = point3d34;
        point3d34, point3d35 = MathHelper.smethod_91(point3d1, num1, point3d2, num2, turnDirection);
        self.spiral.Add(PolylineAreaPoint(point3d33, MathHelper.smethod_57(turnDirection, point3d33, point3d34, point3d1)));
        point3d33 = point3d34;
        point3d39 = MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(double_0 + 180), num2);
        self.spiral.Add(PolylineAreaPoint(point3d33, MathHelper.smethod_57(turnDirection, point3d33, point3d39, point3d2)));
        self.spiral.method_1(point3d39);
        self.method_0(point3dCollection);
        self.method_1(MathHelper.distanceBearingPoint(point3d1, Unit.ConvertDegToRad(double_0), num1), MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(double_0 + num30 * 90), num2), MathHelper.distanceBearingPoint(point3d2, Unit.ConvertDegToRad(double_0 + 180), num2));
        point3d56 = MathHelper.distanceBearingPoint(point3d_0, Unit.ConvertDegToRad(double_0 + 180), 1000);
        point3d39 = MathHelper.getIntersectionPoint(point3d_0, point3d56, point3d7, point3d8);
        point3d6_58 = []
        MathHelper.smethod_34(point3d_0, point3d56, point3d3, num3, point3d6_58);
        point3d6 = point3d6_58[0]
        point3d58 = point3d6_58[1]
        point3d6_59 = []
        MathHelper.smethod_34(point3d_0, point3d56, point3d4, num4, point3d6_59);
        point3d6 = point3d6_59[0]
        point3d59 = point3d6_59[1]
        if (orientationType_0 == OrientationType.Right):
            if (not MathHelper.smethod_119(point3d39, point3d3, point3d7) or not MathHelper.smethod_115(point3d39, point3d4, point3d8)):
                self.ptC = point3d58 if(MathHelper.calcDistance(point3d_0, point3d58) > MathHelper.calcDistance(point3d_0, point3d59)) else point3d59
            else:
                self.ptC = point3d39;
        elif (not MathHelper.smethod_115(point3d39, point3d3, point3d7) or not MathHelper.smethod_119(point3d39, point3d4, point3d8)):
            self.ptC = point3d58 if(MathHelper.calcDistance(point3d_0, point3d58) > MathHelper.calcDistance(point3d_0, point3d59)) else point3d59
        else:
            self.ptC = point3d39;
        num31 = MathHelper.calcDistance(self.ptC, point3d43);
        point3d60 = MathHelper.distanceBearingPoint(self.ptC, MathHelper.getBearing(self.ptC, point3d43) + math.asin(num16 / num31) * num30, math.sqrt(num31 * num31 - num16 * num16));
        point3d6_58 = []
        MathHelper.smethod_34(self.ptC, point3d60, point3d1, num1, point3d6_58);
        point3d6 = point3d6_58[0]
        point3d58 = point3d6_58[1]
        point3d6_59 = []
        MathHelper.smethod_34(self.ptC, point3d60, point3d2, num2, point3d6_59);
        point3d6 = point3d6_59[0]
        point3d59 = point3d6_59[1]
        self.ptR = point3d58 if(MathHelper.calcDistance(self.ptC, point3d58) > MathHelper.calcDistance(self.ptC, point3d59)) else point3d59
    
    def get_outboundLineBottom(self):
        return self.outboundLineBottom
    OutboundLineBottom = property(get_outboundLineBottom, None, None, None)
    
    def get_outboundLineTop(self):
        return self.outboundLineTop
    OutboundLineTop = property(get_outboundLineTop, None, None, None)
    
    