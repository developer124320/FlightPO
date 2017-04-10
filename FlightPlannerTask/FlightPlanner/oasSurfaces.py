'''
Created on Feb 9, 2015

@author: KangKuk
'''
from FlightPlanner.helpers import Point3D, MathHelper, Unit
from FlightPlanner.ilsOas import IlsOas
class OasSurface:
    OFZ = 0
    W = 1
    WS = 2
    Z = 3
    X1 = 4
    X2 = 5
    Y1 = 6
    Y = 7
    
class OasCategory:
    ILS1 = 0
    ILS2 = 1
    ILS2AP = 2
    SBAS_APV1 = 3
    SBAS_APV2 = 4
    SBAS_CAT1 = 5

class OasSurfaces:
    
    def __init__(self, oasCategory_0, point3d_0, double_0, double_1, double_2):
#         private const double APV_WIDTH = 1759.4;
        self.APV_WIDTH = 1759.4    
#         public Point3dCollection SelectionArea;
        self.SelectionArea = []
#         public Point3dCollection Ofz;
        self.Ofz = []
#         public Point3dCollection W;
        self.W = []
#         public Point3dCollection WS;
        self.WS = []
#         public Point3dCollection X1;
        self.X1 = []
#         public Point3dCollection X2;
        self.X2 = []
#         public Point3dCollection Y1;
        self.Y1 = []
#         public Point3dCollection Y2;
        self.Y2 = []
#         public Point3dCollection Z;
        self.Z = []
#         public Point3d C;
        self.C = Point3D()
#         public Point3d D;
        self.D = Point3D()
#         public Point3d E;
        self.E = Point3D()
#         public Point3d CC;
        self.CC = Point3D()
#         public Point3d DD;
        self.DD = Point3D()
#         public Point3d EE;
        self.EE = Point3D()
#         public Point3d CCC;
        self.CCC = Point3D()
#         public Point3d DDD;
        self.DDD = Point3D()
#         public bool HasWS;
        self.HasWS = False
#         private OasCategory cat
        self.cat = oasCategory_0
        
        try:
            double0 = double_0 - 1.5707963267949
            double01 = double_0 + 1.5707963267949
            double02 = double_0 + 3.14159265358979
            if 
            self.HasWS = (double.IsNaN(IlsOas.constants.WSA) ? false : !double.IsNaN(IlsOas.constants.WSC));
            double num2 = 0;
            num = (!self.HasWS || oasCategory_0 != OasCategory.SBAS_APV1 && oasCategory_0 != OasCategory.SBAS_APV2 ? (num2 - IlsOas.constants.WC) / IlsOas.constants.WA : (num2 - IlsOas.constants.WSC) / IlsOas.constants.WSA);
            double xA1 = (num2 - IlsOas.constants.XA * num - IlsOas.constants.XC) / IlsOas.constants.XB;
            double yB1 = (IlsOas.constants.YB * (num2 - IlsOas.constants.XC) - IlsOas.constants.XB * (num2 - IlsOas.constants.YC)) / (IlsOas.constants.YB * IlsOas.constants.XA - IlsOas.constants.XB * IlsOas.constants.YA);
            double yA1 = (num2 - IlsOas.constants.YA * yB1 - IlsOas.constants.YC) / IlsOas.constants.YB;
            double zC = (num2 - IlsOas.constants.ZC) / IlsOas.constants.ZA;
            double yA2 = (num2 - IlsOas.constants.YA * zC - IlsOas.constants.YC) / IlsOas.constants.YB;
            self.Ofz = new Point3dCollection();
            self.Ofz.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double0, xA1));
            self.Ofz.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB1), double0, yA1));
            self.Ofz.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, zC), double0, yA2));
            self.Ofz.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, zC), double01, yA2));
            self.Ofz.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB1), double01, yA1));
            self.Ofz.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double01, xA1));
            num1 = (!self.HasWS || oasCategory_0 != OasCategory.ILS2AP ? (double_2 - IlsOas.constants.WC) / IlsOas.constants.WA : (double_2 - IlsOas.constants.WSC) / IlsOas.constants.WSA);
            double double2 = (double_2 - IlsOas.constants.XA * num1 - IlsOas.constants.XC) / IlsOas.constants.XB;
            if (!self.HasWS || oasCategory_0 != OasCategory.SBAS_APV1 && oasCategory_0 != OasCategory.SBAS_APV2 && oasCategory_0 != OasCategory.ILS2AP)
            {
                wC = num;
                xA = xA1;
                wA = 0;
            }
            else
            {
                wC = (IlsOas.constants.WC - IlsOas.constants.WSC) / (IlsOas.constants.WSA - IlsOas.constants.WA);
                if (wC >= num1)
                {
                    throw new Exception(Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM);
                }
                wA = IlsOas.constants.WA * wC + IlsOas.constants.WC;
                xA = (wA - IlsOas.constants.XA * wC - IlsOas.constants.XC) / IlsOas.constants.XB;
            }
            self.W = new Point3dCollection();
            if (oasCategory_0 != OasCategory.ILS2AP)
            {
                self.W.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num1), double0, double2).smethod_167(point3d_0.get_Z() + double_2));
                self.W.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double0, xA).smethod_167(point3d_0.get_Z() + wA));
                self.W.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double01, xA).smethod_167(point3d_0.get_Z() + wA));
                self.W.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num1), double01, double2).smethod_167(point3d_0.get_Z() + double_2));
            }
            else
            {
                self.W.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double0, xA).smethod_167(point3d_0.get_Z() + wA));
                self.W.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double0, xA1).smethod_167(point3d_0.get_Z()));
                self.W.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double01, xA1).smethod_167(point3d_0.get_Z()));
                self.W.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double01, xA).smethod_167(point3d_0.get_Z() + wA));
            }
            if (self.HasWS && (oasCategory_0 == OasCategory.SBAS_APV1 || oasCategory_0 == OasCategory.SBAS_APV2 || oasCategory_0 == OasCategory.ILS2AP))
            {
                self.WS = new Point3dCollection();
                if (oasCategory_0 != OasCategory.ILS2AP)
                {
                    self.WS.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double0, xA).smethod_167(point3d_0.get_Z() + wA));
                    self.WS.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double0, xA1).smethod_167(point3d_0.get_Z()));
                    self.WS.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double01, xA1).smethod_167(point3d_0.get_Z()));
                    self.WS.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double01, xA).smethod_167(point3d_0.get_Z() + wA));
                }
                else
                {
                    self.WS.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num1), double0, double2).smethod_167(point3d_0.get_Z() + double_2));
                    self.WS.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double0, xA).smethod_167(point3d_0.get_Z() + wA));
                    self.WS.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double01, xA).smethod_167(point3d_0.get_Z() + wA));
                    self.WS.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num1), double01, double2).smethod_167(point3d_0.get_Z() + double_2));
                }
            }
            if (oasCategory_0 != OasCategory.SBAS_APV1 && oasCategory_0 != OasCategory.SBAS_APV2)
            {
                if (oasCategory_0 == OasCategory.SBAS_CAT1)
                {
                    goto Label4;
                }
                double1 = (double_1 - IlsOas.constants.ZC) / IlsOas.constants.ZA;
                double11 = (double_1 - IlsOas.constants.YC - IlsOas.constants.YA * double1) / IlsOas.constants.YB;
                zA = double_1;
                goto Label0;
            }
        Label4:
            double1 = (IlsOas.constants.ZC - 1759.4 * IlsOas.constants.YB - IlsOas.constants.YC) / (IlsOas.constants.YA - IlsOas.constants.ZA);
            double11 = 1759.4;
            zA = IlsOas.constants.ZA * double1 + IlsOas.constants.ZC;
        Label0:
            self.Z = new Point3dCollection();
            self.Z.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, zC), double0, yA2).smethod_167(point3d_0.get_Z()));
            self.Z.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, double1), double0, double11).smethod_167(point3d_0.get_Z() + zA));
            self.Z.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, double1), double01, double11).smethod_167(point3d_0.get_Z() + zA));
            self.Z.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, zC), double01, yA2).smethod_167(point3d_0.get_Z()));
            double yB2 = (IlsOas.constants.YB * (double_2 - IlsOas.constants.XC) - IlsOas.constants.XB * (double_2 - IlsOas.constants.YC)) / (IlsOas.constants.YB * IlsOas.constants.XA - IlsOas.constants.XB * IlsOas.constants.YA);
            double double21 = (double_2 - IlsOas.constants.XC - IlsOas.constants.XA * yB2) / IlsOas.constants.XB;
            self.X1 = new Point3dCollection();
            self.X1.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num1), double0, double2).smethod_167(point3d_0.get_Z() + double_2));
            self.X1.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB2), double0, double21).smethod_167(point3d_0.get_Z() + double_2));
            self.X1.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB1), double0, yA1).smethod_167(point3d_0.get_Z()));
            self.X1.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double0, xA1).smethod_167(point3d_0.get_Z()));
            if (self.HasWS && (oasCategory_0 == OasCategory.SBAS_APV1 || oasCategory_0 == OasCategory.SBAS_APV2 || oasCategory_0 == OasCategory.ILS2AP))
            {
                self.X1.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double0, xA).smethod_167(point3d_0.get_Z() + wA));
            }
            self.X2 = new Point3dCollection();
            self.X2.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num1), double01, double2).smethod_167(point3d_0.get_Z() + double_2));
            self.X2.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB2), double01, double21).smethod_167(point3d_0.get_Z() + double_2));
            self.X2.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB1), double01, yA1).smethod_167(point3d_0.get_Z()));
            self.X2.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, num), double01, xA1).smethod_167(point3d_0.get_Z()));
            if (self.HasWS && (oasCategory_0 == OasCategory.SBAS_APV1 || oasCategory_0 == OasCategory.SBAS_APV2 || oasCategory_0 == OasCategory.ILS2AP))
            {
                self.X2.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, wC), double01, xA).smethod_167(point3d_0.get_Z() + wA));
            }
            if (oasCategory_0 != OasCategory.SBAS_APV1 && oasCategory_0 != OasCategory.SBAS_APV2)
            {
                if (oasCategory_0 == OasCategory.SBAS_CAT1)
                {
                    goto Label5;
                }
                yB = (IlsOas.constants.YB * (double_1 - IlsOas.constants.XC) - IlsOas.constants.XB * (double_1 - IlsOas.constants.YC)) / (IlsOas.constants.YB * IlsOas.constants.XA - IlsOas.constants.XB * IlsOas.constants.YA);
                double12 = (double_1 - IlsOas.constants.YC - IlsOas.constants.YA * yB) / IlsOas.constants.YB;
                yA = double_1;
                goto Label2;
            }
        Label5:
            double12 = 1759.4;
            yB = (double21 >= double12 ? (IlsOas.constants.YB * double12 + IlsOas.constants.YC - IlsOas.constants.XB * double12 - IlsOas.constants.XC) / (IlsOas.constants.XA - IlsOas.constants.YA) : num1 - (double12 - double2) * (num1 - yB2) / (double21 - double2));
            yA = IlsOas.constants.YA * yB + IlsOas.constants.YB * double12 + IlsOas.constants.YC;
        Label2:
            self.Y1 = new Point3dCollection();
            if (double21 < double12)
            {
                self.Y1.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB2), double0, double21).smethod_167(point3d_0.get_Z() + double_2));
            }
            self.Y1.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB), double0, double12).smethod_167(point3d_0.get_Z() + yA));
            self.Y1.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, double1), double0, double11).smethod_167(point3d_0.get_Z() + zA));
            self.Y1.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, zC), double0, yA2).smethod_167(point3d_0.get_Z()));
            self.Y1.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB1), double0, yA1).smethod_167(point3d_0.get_Z()));
            self.Y2 = new Point3dCollection();
            if (double21 < double12)
            {
                self.Y2.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB2), double01, double21).smethod_167(point3d_0.get_Z() + double_2));
            }
            self.Y2.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB), double01, double12).smethod_167(point3d_0.get_Z() + yA));
            self.Y2.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, double1), double01, double11).smethod_167(point3d_0.get_Z() + zA));
            self.Y2.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, zC), double01, yA2).smethod_167(point3d_0.get_Z()));
            self.Y2.Add(MathHelper.distanceBearingPoint(MathHelper.distanceBearingPoint(point3d_0, double02, yB1), double01, yA1).smethod_167(point3d_0.get_Z()));
            self.C = new Point3d(num, xA1, 0);
            self.D = new Point3d(yB1, yA1, 0);
            self.E = new Point3d(zC, yA2, 0);
            self.CC = new Point3d(num1, double2, double_2);
            self.DD = new Point3d(yB2, double21, double_2);
            self.EE = new Point3d(double1, double11, zA);
            self.CCC = new Point3d(wC, xA, wA);
            self.DDD = new Point3d(yB, double12, yA);
            self.SelectionArea = new Point3dCollection();
            self.SelectionArea.Add(self.X1.get_Item(0));
            self.SelectionArea.Add(self.X1.get_Item(1));
            if (double21 >= double12)
            {
                self.SelectionArea.Add(self.Y1.get_Item(0));
            }
            else
            {
                self.SelectionArea.Add(self.Y1.get_Item(1));
            }
            self.SelectionArea.Add(self.Z.get_Item(1));
            self.SelectionArea.Add(self.Z.get_Item(2));
            if (double21 >= double12)
            {
                self.SelectionArea.Add(self.Y2.get_Item(0));
            }
            else
            {
                self.SelectionArea.Add(self.Y2.get_Item(1));
            }
            self.SelectionArea.Add(self.X2.get_Item(1));
            self.SelectionArea.Add(self.X2.get_Item(0));
            self.SelectionArea.smethod_146();
        