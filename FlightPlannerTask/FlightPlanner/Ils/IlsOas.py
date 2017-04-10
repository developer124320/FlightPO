'''
Created on Mar 13, 2015

@author: Administrator
'''
from qgis.core import QGis
from FlightPlanner.types import Point3D, OasCategory, OasSurface
from FlightPlanner.helpers import MathHelper
from FlightPlanner.messages import Messages
from FlightPlanner.Ils.OasObstacles import OasObstacles

import define

class OasSurfaces:

# public OasSurfaces(OasCategory oasCategory_0, Point3d point3d_0, double double_0, double double_1, double double_2)
#     {
    def __init__(self, oasCategory_0, point3d_0, double_0, double_1, double_2):
        self.APV_WIDTH = 1759.4;
        #public Point3dCollection Ofz;
        self.Ofz = []
        #public Point3dCollection W;
        self.W = []
        #public Point3dCollection WS;
        self.WS = []
        #public Point3dCollection X1;
        self.X1 = []
        #public Point3dCollection X2;
        self.X2 = []
        #public Point3dCollection Y1;
        self.Y1 = []
        #public Point3dCollection Y2;
        self.Y2 = []
        #public Point3dCollection Z;
        self.Z = []
        #public Point3d C;
        self.C = Point3D()
        #public Point3d D;
        self.D = Point3D()
        #public Point3d E;
        self.E = Point3D()
        #public Point3d CC;
        self.CC = Point3D()
        #public Point3d DD;
        self.DD = Point3D()
        #public Point3d EE;
        self.EE = Point3D()
        #public Point3d CCC;
        self.CCC = Point3D()
        #public Point3d DDD;
        self.DDD = Point3D()
        #public bool HasWS;
        self.HasWS = Point3D()
        #private OasCategory cat;
        self.cat = ""
        self.cat = oasCategory_0;
        double0 = double_0 - 1.5707963267949;
        double01 = double_0 + 1.5707963267949;
        double02 = double_0 + 3.14159265358979;
        self.HasWS = False if OasObstacles.constants.WSA == None  else OasObstacles.constants.WSC != None
        num2 = 0;
        num = (num2 - OasObstacles.constants.WC) / OasObstacles.constants.WA if not self.HasWS or (oasCategory_0 != OasCategory.SBAS_APV1 and oasCategory_0 != OasCategory.SBAS_APV2) else (num2 - OasObstacles.constants.WSC) / OasObstacles.constants.WSA
        xA1 = (num2 - OasObstacles.constants.XA * num - OasObstacles.constants.XC) / OasObstacles.constants.XB;
        yB1 = (OasObstacles.constants.YB * (num2 - OasObstacles.constants.XC) - OasObstacles.constants.XB * (num2 - OasObstacles.constants.YC)) / (OasObstacles.constants.YB * OasObstacles.constants.XA - OasObstacles.constants.XB * OasObstacles.constants.YA);
        yA1 = (num2 - OasObstacles.constants.YA * yB1 - OasObstacles.constants.YC) / OasObstacles.constants.YB;
        zC = (num2 - OasObstacles.constants.ZC) / OasObstacles.constants.ZA;
        yA2 = (num2 - OasObstacles.constants.YA * zC - OasObstacles.constants.YC) / OasObstacles.constants.YB;
        self.Ofz = []
        self.Ofz.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double0, xA1));
        self.Ofz.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB1), double0, yA1));
        self.Ofz.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, zC), double0, yA2));
        self.Ofz.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, zC), double01, yA2));
        self.Ofz.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB1), double01, yA1));
        self.Ofz.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double01, xA1));
        num1 = (double_2 - OasObstacles.constants.WC) / OasObstacles.constants.WA if not self.HasWS or (oasCategory_0 != OasCategory.ILS2AP) else (double_2 - OasObstacles.constants.WSC) / OasObstacles.constants.WSA
        double2 = (double_2 - OasObstacles.constants.XA * num1 - OasObstacles.constants.XC) / OasObstacles.constants.XB;
        if not self.HasWS or (oasCategory_0 != OasCategory.SBAS_APV1 and oasCategory_0 != OasCategory.SBAS_APV2 and oasCategory_0 != OasCategory.ILS2AP):
            wC = num;
            xA = xA1;
            wA = 0;
        else:
            wC = (OasObstacles.constants.WC - OasObstacles.constants.WSC) / (OasObstacles.constants.WSA - OasObstacles.constants.WA);
            if (wC >= num1):
                raise UserWarning, Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM
            wA = OasObstacles.constants.WA * wC + OasObstacles.constants.WC;
            xA = (wA - OasObstacles.constants.XA * wC - OasObstacles.constants.XC) / OasObstacles.constants.XB;
        self.W = []
        if (oasCategory_0 != OasCategory.ILS2AP):
            self.W.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num1), double0, double2).smethod_167(point3d_0.z() + double_2));
            self.W.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double0, xA).smethod_167(point3d_0.z() + wA));
            self.W.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double01, xA).smethod_167(point3d_0.z() + wA));
            self.W.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num1), double01, double2).smethod_167(point3d_0.z() + double_2));
        else:
            self.W.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double0, xA).smethod_167(point3d_0.z() + wA));
            self.W.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double0, xA1).smethod_167(point3d_0.z()));
            self.W.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double01, xA1).smethod_167(point3d_0.z()));
            self.W.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double01, xA).smethod_167(point3d_0.z() + wA));
        if (self.HasWS and (oasCategory_0 == OasCategory.SBAS_APV1 or oasCategory_0 == OasCategory.SBAS_APV2 or oasCategory_0 == OasCategory.ILS2AP)):
            self.WS = []
            if (oasCategory_0 != OasCategory.ILS2AP):
                self.WS.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double0, xA).smethod_167(point3d_0.z() + wA));
                self.WS.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double0, xA1).smethod_167(point3d_0.z()));
                self.WS.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double01, xA1).smethod_167(point3d_0.z()));
                self.WS.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double01, xA).smethod_167(point3d_0.z() + wA));
            else:
                self.WS.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num1), double0, double2).smethod_167(point3d_0.z() + double_2));
                self.WS.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double0, xA).smethod_167(point3d_0.z() + wA));
                self.WS.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double01, xA).smethod_167(point3d_0.z() + wA));
                self.WS.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num1), double01, double2).smethod_167(point3d_0.z() + double_2));

        if (oasCategory_0 != OasCategory.SBAS_APV1 and oasCategory_0 != OasCategory.SBAS_APV2 and oasCategory_0 != OasCategory.SBAS_CAT1):
            double1 = (double_1 - OasObstacles.constants.ZC) / OasObstacles.constants.ZA;
            double11 = (double_1 - OasObstacles.constants.YC - OasObstacles.constants.YA * double1) / OasObstacles.constants.YB;
            zA = double_1;
        else:
            double1 = (OasObstacles.constants.ZC - 1759.4 * OasObstacles.constants.YB - OasObstacles.constants.YC) / (OasObstacles.constants.YA - OasObstacles.constants.ZA);
            double11 = 1759.4;
            zA = OasObstacles.constants.ZA * double1 + OasObstacles.constants.ZC;

        self.Z = []
        self.Z.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, zC), double0, yA2).smethod_167(point3d_0.z()));
        self.Z.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, double1), double0, double11).smethod_167(point3d_0.z() + zA));
        self.Z.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, double1), double01, double11).smethod_167(point3d_0.z() + zA));
        self.Z.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, zC), double01, yA2).smethod_167(point3d_0.z()));
        yB2 = (OasObstacles.constants.YB * (double_2 - OasObstacles.constants.XC) - OasObstacles.constants.XB * (double_2 - OasObstacles.constants.YC)) / (OasObstacles.constants.YB * OasObstacles.constants.XA - OasObstacles.constants.XB * OasObstacles.constants.YA);
        double21 = (double_2 - OasObstacles.constants.XC - OasObstacles.constants.XA * yB2) / OasObstacles.constants.XB;
        self.X1 = []
        self.X1.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num1), double0, double2).smethod_167(point3d_0.z() + double_2));
        self.X1.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB2), double0, double21).smethod_167(point3d_0.z() + double_2));
        self.X1.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB1), double0, yA1).smethod_167(point3d_0.z()));
        self.X1.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double0, xA1).smethod_167(point3d_0.z()));
        if (self.HasWS and (oasCategory_0 == OasCategory.SBAS_APV1 or oasCategory_0 == OasCategory.SBAS_APV2 or oasCategory_0 == OasCategory.ILS2AP)):
            self.X1.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double0, xA).smethod_167(point3d_0.z() + wA));
        self.X2 = []
        self.X2.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num1), double01, double2).smethod_167(point3d_0.z() + double_2));
        self.X2.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB2), double01, double21).smethod_167(point3d_0.z() + double_2));
        self.X2.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB1), double01, yA1).smethod_167(point3d_0.z()));
        self.X2.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double01, xA1).smethod_167(point3d_0.z()));
        if (self.HasWS and (oasCategory_0 == OasCategory.SBAS_APV1 or oasCategory_0 == OasCategory.SBAS_APV2 or oasCategory_0 == OasCategory.ILS2AP)):
            self.X2.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double01, xA).smethod_167(point3d_0.z() + wA));
        if (oasCategory_0 != OasCategory.SBAS_APV1 and oasCategory_0 != OasCategory.SBAS_APV2 and oasCategory_0 != OasCategory.SBAS_CAT1):
            yB = (OasObstacles.constants.YB * (double_1 - OasObstacles.constants.XC) - OasObstacles.constants.XB * (double_1 - OasObstacles.constants.YC)) / (OasObstacles.constants.YB * OasObstacles.constants.XA - OasObstacles.constants.XB * OasObstacles.constants.YA);
            double12 = (double_1 - OasObstacles.constants.YC - OasObstacles.constants.YA * yB) / OasObstacles.constants.YB;
            yA = double_1;
        else:
            double12 = 1759.4;
            yB = (OasObstacles.constants.YB * double12 + OasObstacles.constants.YC - OasObstacles.constants.XB * double12 - OasObstacles.constants.XC) / (OasObstacles.constants.XA - OasObstacles.constants.YA) if double21 >= double12 else num1 - (double12 - double2) * (num1 - yB2) / (double21 - double2);
            yA = OasObstacles.constants.YA * yB + OasObstacles.constants.YB * double12 + OasObstacles.constants.YC;

        self.Y1 = []
        if (double21 < double12):
            self.Y1.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB2), double0, double21).smethod_167(point3d_0.z() + double_2));
        self.Y1.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB), double0, double12).smethod_167(point3d_0.z() + yA));
        self.Y1.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, double1), double0, double11).smethod_167(point3d_0.z() + zA));
        self.Y1.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, zC), double0, yA2).smethod_167(point3d_0.z()));
        self.Y1.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB1), double0, yA1).smethod_167(point3d_0.z()));
        self.Y2 = []
        if (double21 < double12):
            self.Y2.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB2), double01, double21).smethod_167(point3d_0.z() + double_2));
        self.Y2.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB), double01, double12).smethod_167(point3d_0.z() + yA));
        self.Y2.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, double1), double01, double11).smethod_167(point3d_0.z() + zA));
        self.Y2.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, zC), double01, yA2).smethod_167(point3d_0.z()));
        self.Y2.append(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB1), double01, yA1).smethod_167(point3d_0.z()));
        self.C = Point3D(num, xA1, 0);
        self.D = Point3D(yB1, yA1, 0);
        self.E = Point3D(zC, yA2, 0);
        self.CC = Point3D(num1, double2, double_2);
        self.DD = Point3D(yB2, double21, double_2);
        self.EE = Point3D(double1, double11, zA);
        self.CCC = Point3D(wC, xA, wA);
        self.DDD = Point3D(yB, double12, yA);
        self.SelectionArea = []
        self.SelectionArea.append(self.X1[0])
        self.SelectionArea.append(self.X1[1])
        if (double21 >= double12):
            self.SelectionArea.append(self.Y1[0])
        else:
            self.SelectionArea.append(self.Y1[1])
        self.SelectionArea.append(self.Z[1])
        self.SelectionArea.append(self.Z[2])
        if (double21 >= double12):
            self.SelectionArea.append(self.Y2[0]);
        else:
            self.SelectionArea.append(self.Y2[1]);
        self.SelectionArea.append(self.X2[1]);
        self.SelectionArea.append(self.X2[0]);
#         self.SelectionArea.smethod_146();

#     public bool method_0(OasSurface oasSurface_0, Obstacle obstacle_0, ref double double_0, ref double double_1, out double double_2)
#     {
    def method_0(self, oasSurface_0, obstacle_0, lstDouble3):
        double_0 = lstDouble3[0]
        double_1 = lstDouble3[1]
        double_2 = 0;
        flag = False
        if define._units == QGis.Meters:
            position = obstacle_0.position
        else:
            position = obstacle_0.positionDegree
        if oasSurface_0 == OasSurface.OFZ:
            if (MathHelper.pointInPolygon(self.Ofz, position, obstacle_0.tolerance)):
                double_0 = max([double_0, self.E.x()]);
                double_2 = 0;
                flag = True;
        elif oasSurface_0 == OasSurface.W:
            if (MathHelper.pointInPolygon(self.W, position, obstacle_0.tolerance)):
                if not self.HasWS or (self.cat != OasCategory.SBAS_APV1 and self.cat != OasCategory.SBAS_APV2):
                    double_0 = max([double_0, self.C.x()])
                else:
                    double_0 = max([double_0, self.CCC.x()]);
                double_2 = max([0, OasObstacles.constants.WA * double_0 + OasObstacles.constants.WC])
                flag = True;
        elif oasSurface_0 == OasSurface.WS:
            if (MathHelper.pointInPolygon(self.WS, position, obstacle_0.tolerance)):
                if (not self.HasWS or self.cat != OasCategory.ILS2AP):
                    double_0 = max([double_0, self.C.x()]);
                else:
                    double_0 = max([double_0, self.CCC.x()]);
                double_2 = max([0, OasObstacles.constants.WSA * double_0 + OasObstacles.constants.WSC]);
                flag = True;
        elif oasSurface_0 == OasSurface.Z:
            if (MathHelper.pointInPolygon(self.Z, position, obstacle_0.tolerance)):
                double_0 = min([double_0 + 2 * obstacle_0.tolerance, self.E.x()]);
                double_2 = max([0, OasObstacles.constants.ZA * double_0 + OasObstacles.constants.ZC]);
                flag = True;
        elif oasSurface_0 == OasSurface.X1:
            if (MathHelper.pointInPolygon(self.X1, position, obstacle_0.tolerance)):
                double_0 = max([double_0, self.D.x()]);
                if ((OasObstacles.constants.YA * double_0 - OasObstacles.constants.XA * double_0 + OasObstacles.constants.YC - OasObstacles.constants.XC) / (OasObstacles.constants.XB - OasObstacles.constants.YB) < double_1):
                    double_0 = (OasObstacles.constants.YB * double_1 - OasObstacles.constants.XB * double_1 + OasObstacles.constants.YC - OasObstacles.constants.XC) / (OasObstacles.constants.XA - OasObstacles.constants.YA);
                double_2 = OasObstacles.constants.XA * double_0 + OasObstacles.constants.XB * double_1 + OasObstacles.constants.XC;
                if (self.HasWS and self.cat == OasCategory.ILS2AP):
                    if (double_0 <= self.CCC.x()):
                        double_2 = max([double_2, OasObstacles.constants.WA * double_0 + OasObstacles.constants.WC]);
                    else:
                        double_2 = max([double_2, OasObstacles.constants.WSA * double_0 + OasObstacles.constants.WSC]);
                elif not self.HasWS or (self.cat != OasCategory.SBAS_APV1 and self.cat != OasCategory.SBAS_APV2):
                    double_2 = max([double_2, OasObstacles.constants.WA * double_0 + OasObstacles.constants.WC]);
                elif (double_0 <= self.CCC.x()):
                    double_2 = max([double_2, OasObstacles.constants.WSA * double_0 + OasObstacles.constants.WSC]);
                else:
                    double_2 = max([double_2, OasObstacles.constants.WA * double_0 + OasObstacles.constants.WC]);
                double_2 = max([0, double_2]);
                double_1 = -(double_2 - OasObstacles.constants.XA * double_0 - OasObstacles.constants.XC) / OasObstacles.constants.XB;
                flag = True;
        elif oasSurface_0 == OasSurface.X2:
            if (MathHelper.pointInPolygon(self.X2, position, obstacle_0.tolerance)):
                double_0 = max([double_0, self.D.x()]);
                if ((OasObstacles.constants.YA * double_0 - OasObstacles.constants.XA * double_0 + OasObstacles.constants.YC - OasObstacles.constants.XC) / (OasObstacles.constants.XB - OasObstacles.constants.YB) < double_1):
                    double_0 = (OasObstacles.constants.YB * double_1 - OasObstacles.constants.XB * double_1 + OasObstacles.constants.YC - OasObstacles.constants.XC) / (OasObstacles.constants.XA - OasObstacles.constants.YA);
                double_2 = OasObstacles.constants.XA * double_0 + OasObstacles.constants.XB * double_1 + OasObstacles.constants.XC;
                if (self.HasWS and self.cat == OasCategory.ILS2AP):
                    if (double_0 <= self.CCC.x()):
                        double_2 = max([double_2, OasObstacles.constants.WA * double_0 + OasObstacles.constants.WC]);
                    else:
                        double_2 = max([double_2, OasObstacles.constants.WSA * double_0 + OasObstacles.constants.WSC]);
                elif not self.HasWS or (self.cat != OasCategory.SBAS_APV1 and self.cat != OasCategory.SBAS_APV2):
                    double_2 = max([double_2, OasObstacles.constants.WA * double_0 + OasObstacles.constants.WC]);
                elif (double_0 <= self.CCC.x()):
                    double_2 = max([double_2, OasObstacles.constants.WSA * double_0 + OasObstacles.constants.WSC]);
                else:
                    double_2 = max([double_2, OasObstacles.constants.WA * double_0 + OasObstacles.constants.WC]);
                double_2 = max([0, double_2]);
                double_1 = (double_2 - OasObstacles.constants.XA * double_0 - OasObstacles.constants.XC) / OasObstacles.constants.XB;
                flag = True;
        elif oasSurface_0 == OasSurface.Y1:
            if MathHelper.pointInPolygon(self.Y1, position, obstacle_0.tolerance):
                double_0 = max([double_0, self.EE.x()]);
                double_1 = max([double_1, (OasObstacles.constants.YA * double_0 - OasObstacles.constants.XA * double_0 + OasObstacles.constants.YC - OasObstacles.constants.XC) / (OasObstacles.constants.XB - OasObstacles.constants.YB)]);
                double_2 = max([OasObstacles.constants.YA * double_0 + OasObstacles.constants.YB * double_1 + OasObstacles.constants.YC, OasObstacles.constants.ZA * double_0 + OasObstacles.constants.ZC]);
                double_2 = max([0, double_2]);
                double_1 = -(double_2 - OasObstacles.constants.YA * double_0 - OasObstacles.constants.YC) / OasObstacles.constants.YB;
                flag = True;
        elif oasSurface_0 == OasSurface.Y2:
            if MathHelper.pointInPolygon(self.Y2, position, obstacle_0.tolerance):
                double_0 = max([double_0, self.EE.x()]);
                double_1 = max([double_1, (OasObstacles.constants.YA * double_0 - OasObstacles.constants.XA * double_0 + OasObstacles.constants.YC - OasObstacles.constants.XC) / (OasObstacles.constants.XB - OasObstacles.constants.YB)]);
                double_2 = max([OasObstacles.constants.YA * double_0 + OasObstacles.constants.YB * double_1 + OasObstacles.constants.YC, OasObstacles.constants.ZA * double_0 + OasObstacles.constants.ZC]);
                double_2 = max([0, double_2]);
                double_1 = (double_2 - OasObstacles.constants.YA * double_0 - OasObstacles.constants.YC) / OasObstacles.constants.YB;
                flag = True;
        if flag:
            lstDouble3[0] = double_0
            lstDouble3[1] = double_1
            lstDouble3[2] = double_2
            return True
        else:
            return False;
