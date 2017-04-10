'''
Created on Mar 13, 2015

@author: Administrator
'''
import math

from FlightPlanner.helpers import Unit, MathHelper
from FlightPlanner.messages import Messages
from FlightPlanner.types import OasCategory, AircraftSize

class OasConstants:

    def __init__(self):
        self.comTable = ComTable()
        self.comSurco = ComSurco()
        self.comTemp1 = ComTemp1()
        self.Assigned = False;

    def method_0(self, double_0, double_1, double_2, double_3, double_4, double_5, double_6, double_7, double_8, double_9, double_10, double_11):
        self.WA = double_0;
        self.WC = double_1;
        self.WSA = double_2;
        self.WSC = double_3;
        self.XA = double_4;
        self.XB = double_5;
        self.XC = double_6;
        self.YA = double_7;
        self.YB = double_8;
        self.YC = double_9;
        self.ZA = double_10;
        self.ZC = double_11;
        self.Assigned = True;

    def method_1(self, oasCategory_0, missedApproachClimbGradient_0, double_0, double_1, double_2, double_3, double_4):
        self.Assigned = False;
        self.comTable.method_0();
        self.comSurco.method_0();
        self.comTemp1.method_0();
        self.method_7(oasCategory_0);
        if (double_0 <= 3.5):
            self.method_8(oasCategory_0, double_0, double_1, AircraftSize.Standard);
        else:
            self.method_8(oasCategory_0, 3.5, double_1, AircraftSize.Standard);
        self.method_9(AircraftSize.Standard);
        self.WA = self.comSurco.AW;
        self.WC = self.comSurco.CW;
        self.WSA = self.comSurco.AWS;
        self.WSC = self.comSurco.CWS;
        if (double_0 > 3.5):
            self.WA = 0.0239 + 0.0092 * (double_0 - 2.5);
            self.WC = -6.45;
        self.XA = self.comSurco.AX;
        self.XB = self.comSurco.BX;
        self.XC = self.comSurco.CX;
        self.YA = self.comSurco.AY[missedApproachClimbGradient_0];
        self.YB = self.comSurco.BY[missedApproachClimbGradient_0];
        self.YC = self.comSurco.CY[missedApproachClimbGradient_0];
        self.ZA = self.comSurco.AZ[missedApproachClimbGradient_0];
        self.ZC = self.comSurco.CZ[missedApproachClimbGradient_0];
        if (double_0 > 3.5):
            self.ZC = -self.ZA * (-900 - 50 * ((double_0 - 3.5) / 0.1));
        if (oasCategory_0 == OasCategory.ILS2AP):
            self.comTable.method_0();
            self.comSurco.method_0();
            self.comTemp1.method_0();
            self.method_7(OasCategory.ILS2);
            if (double_0 <= 3.5):
                self.method_8(OasCategory.ILS2, double_0, double_1, AircraftSize.Standard);
            else:
                self.method_8(OasCategory.ILS2, 3.5, double_1, AircraftSize.Standard);
            self.method_9(AircraftSize.Standard);
            self.YA = self.comSurco.AY[missedApproachClimbGradient_0];
            self.YB = self.comSurco.BY[missedApproachClimbGradient_0];
            self.YC = self.comSurco.CY[missedApproachClimbGradient_0];
        num = max([double_4 / self.XB, double_3 + (double_4 - 3) / self.XB]) - max([6 / self.XB, 30 + 3 / self.XB]);
        self.WC = self.WC - (double_4 - 6) + (double_2 - 15);
        if (oasCategory_0 == OasCategory.ILS2AP):
            self.WSC = self.WSC - (double_4 - 6) + (double_2 - 15);
        self.XC = self.XC - self.XB * num + (double_2 - 15);
        self.YC = self.YC - self.YB * num + (double_2 - 15);
        if (oasCategory_0 == OasCategory.SBAS_APV1):
            num1 = math.tan(Unit.ConvertDegToRad(double_0));
            num2 = math.tan(Unit.ConvertDegToRad(0.75 * double_0));
            self.WSA = num2;
            self.WSC = -50 + double_2 * num2 / num1;
            self.XC = self.XC - 38;
            self.YC = self.YC - 38;
            if (double_0 <= 3.5):
                self.ZC = -self.ZA * -(900 + 38 / num1);
            else:
                self.WC = -6.45;
                self.ZC = -self.ZA * -(900 + 38 / num1 + 50 * (double_0 - 3.5) / 0.1);
        elif (oasCategory_0 == OasCategory.SBAS_APV2):
            num3 = math.tan(Unit.ConvertDegToRad(double_0));
            num4 = math.tan(Unit.ConvertDegToRad(0.75 * double_0));
            self.WSA = num4;
            self.WSC = -20 + double_2 * num4 / num3;
            self.XC = self.XC - 8;
            self.YC = self.YC - 8;
            if (double_0 <= 3.5):
                self.ZC = -self.ZA * -(900 + 8 / num3);
            else:
                self.WC = -6.45;
                self.ZC = -self.ZA * -(900 + 8 / num3 + 50 * (double_0 - 3.5) / 0.1);
        if (oasCategory_0 == OasCategory.SBAS_APV1 or oasCategory_0 == OasCategory.SBAS_APV2):
            num5 = (self.WC - self.WSC) / (self.WSA - self.WA);
            if (self.WA * num5 + self.WC <= 0):
                self.WSA = 0;
                self.WSC = 0;
        self.WA = round(self.WA, 6);
        self.WC = round(self.WC, 2);
        if (not MathHelper.smethod_96(self.WSA)):
            self.WSA = round(self.WSA, 6);
        else:
            self.WSA = None
        if (not MathHelper.smethod_96(self.WSC)):
            self.WSC = round(self.WSC, 2);
        else:
            self.WSC = None
        self.XA = round(self.XA, 6);
        self.XB = round(self.XB, 6);
        self.XC = round(self.XC, 2);
        self.YA = round(self.YA, 6);
        self.YB = round(self.YB, 6);
        self.YC = round(self.YC, 2);
        self.ZA = round(self.ZA, 6);
        self.ZC = round(self.ZC, 2);
        self.Assigned = True;

    def method_2(self):
        self.Assigned = False;

    def method_3(self, double_0, double_1, double_2):
        double1 = double_1[0];
        num = double_1[1];
        double11 = double_1[2];
        double0 = double_0 - double1;
        double01 = double_0 - num;
        num1 = double_0 - double11;
        num2 = double1 - num;
        num3 = double1 - double11;
        num4 = num - double11;
        num5 = double01 * num1 / (num2 * num3);
        num6 = double0 * num1 / (-num2 * num4);
        num7 = double0 * double01 / (num3 * num4);
        return num5 * double_2[0] + num6 * double_2[1] + num7 * double_2[2];

    def method_4(self, double_0, double_1, double_2):
        double1 = double_1[0];
        num = double_1[1];
        double11 = double_1[2];
        num1 = double_1[3];
        double0 = double_0 - double1;
        double01 = double_0 - num;
        double02 = double_0 - double11;
        num2 = double_0 - num1;
        num3 = double1 - num;
        num4 = double1 - double11;
        num5 = double1 - num1;
        num6 = num - double11;
        num7 = num - num1;
        num8 = double11 - num1;
        num9 = double01 * double02 * num2 / (num3 * num4 * num5);
        num10 = double0 * double02 * num2 / (-num3 * num6 * num7);
        num11 = double0 * double01 * num2 / (num4 * num6 * num8);
        num12 = double0 * double01 * double02 / (-num5 * num7 * num8);
        return num9 * double_2[0] + num10 * double_2[1] + num11 * double_2[2] + num12 * double_2[3];

    def method_5(self, double_0, double_1, double_2, double_3, double_4):
        double4 = [0.0, 0.0, 0.0, 0.0]
        numArray = [0.0, 0.0, 0.0]
        double0 = double_0 - 0.001;
        num = double_0 + 0.001;
        double1 = double_1 - 1E-05;
        double11 = double_1 + 1E-05;
        if (num < double_2[0] or double0 > double_2[3] or double11 < double_3[0] or double1 > double_3[2]):
            raise UserWarning, Messages.ERR_OAS_CONSTANTS_X_Y_OUT_OF_RANGE
        for i in range(3 + 1):
            for j in range(2 + 1):
                numArray[j] = double_4[i][j];
            double4[i] = self.method_3(double_1, double_3, numArray);
        num1 = self.method_4(double_0, double_2, double4);
        for k in range(2 + 1):
            for l in range(3 + 1):
                double4[l] = double_4[l][k];
            numArray[k] = self.method_4(double_0, double_2, double4);
        num2 = self.method_3(double_1, double_3, numArray);
        return 0.5 * (num1 + num2);

    def method_6(self, double_0, double_1, double_2, double_3, double_4, double_5, double_6, lstDouble2):#ref double double_7, ref double double_8)
        double0 = double_0 * double_4 - double_3 * double_1;
        double_7 = (double_4 * (double_6 - double_2) - double_1 * (double_6 - double_5)) / double0;
        double_8 = (-double_3 * (double_6 - double_2) + double_0 * (double_6 - double_5)) / double0;
        lstDouble2.append(double_7)
        lstDouble2.append(double_8)

    def method_7(self, oasCategory_0):
        self.comTable.XT[0] = 2000;
        self.comTable.XT[1] = 3000;
        self.comTable.XT[2] = 3800;
        self.comTable.XT[3] = 4500;
        self.comTable.YT[0] = 2.5;
        self.comTable.YT[1] = 3;
        self.comTable.YT[2] = 3.5;
        self.comTable.FAG[0] = 344;
        self.comTable.FAG[1] = 286;
        self.comTable.FAG[2] = 245;
        self.comTable.FAF = 900;
        if oasCategory_0 == OasCategory.ILS1 \
            or oasCategory_0 == OasCategory.SBAS_APV1 \
            or oasCategory_0 == OasCategory.SBAS_APV2 \
            or oasCategory_0 == OasCategory.SBAS_CAT1:
                self.comTable.FAB[0] = 394;
                self.comTable.FAB[1] = 281;
                self.comTable.FAB[2] = 195;
                self.comTable.FBC[0] = 33;
                self.comTable.FBC[1] = 49;
                self.comTable.FBC[2] = 68;
                self.comTable.FGD = 135;
                self.comTable.FTANX[0][0] = 0.15;
                self.comTable.FTANX[0][1] = 0.1688;
                self.comTable.FTANX[0][2] = 0.1975;
                self.comTable.FTANX[1][0] = 0.1625;
                self.comTable.FTANX[1][1] = 0.1825;
                self.comTable.FTANX[1][2] = 0.2138;
                self.comTable.FTANX[2][0] = 0.1681;
                self.comTable.FTANX[2][1] = 0.1888;
                self.comTable.FTANX[2][2] = 0.2188;
                self.comTable.FTANX[3][0] = 0.1738;
                self.comTable.FTANX[3][1] = 0.19;
                self.comTable.FTANX[3][2] = 0.22;
                self.comTable.FTANW[0] = 0.0239;
                self.comTable.FTANW[1] = 0.0285;
                self.comTable.FTANW[2] = 0.0331;
                self.comTable.FEF[0][0] = 169;
                self.comTable.FEF[0][1] = 177;
                self.comTable.FEF[0][2] = 187;
                self.comTable.FEF[0][3] = 193;
                self.comTable.FEF[0][4] = 201;
                self.comTable.FEF[1][0] = 178;
                self.comTable.FEF[1][1] = 187;
                self.comTable.FEF[1][2] = 198;
                self.comTable.FEF[1][3] = 205;
                self.comTable.FEF[1][4] = 213;
                self.comTable.FEF[2][0] = 188;
                self.comTable.FEF[2][1] = 197;
                self.comTable.FEF[2][2] = 209;
                self.comTable.FEF[2][3] = 216;
                self.comTable.FEF[2][4] = 223;
        elif oasCategory_0 == OasCategory.ILS2:
            self.comTable.FAB[0] = 268;
            self.comTable.FAB[1] = 173;
            self.comTable.FAB[2] = 128;
            self.comTable.FBC[0] = 51;
            self.comTable.FBC[1] = 66;
            self.comTable.FBC[2] = 80;
            self.comTable.FGD = 135;
            self.comTable.FTANX[0][0] = 0.195;
            self.comTable.FTANX[0][1] = 0.2179;
            self.comTable.FTANX[0][2] = 0.2571;
            self.comTable.FTANX[1][0] = 0.2126;
            self.comTable.FTANX[1][1] = 0.2347;
            self.comTable.FTANX[1][2] = 0.2729;
            self.comTable.FTANX[2][0] = 0.2167;
            self.comTable.FTANX[2][1] = 0.2383;
            self.comTable.FTANX[2][2] = 0.28;
            self.comTable.FTANX[3][0] = 0.2185;
            self.comTable.FTANX[3][1] = 0.24;
            self.comTable.FTANX[3][2] = 0.285;
            self.comTable.FTANW[0] = 0.0298;
            self.comTable.FTANW[1] = 0.0358;
            self.comTable.FTANW[2] = 0.0415;
            self.comTable.FEF[0][0] = 169;
            self.comTable.FEF[0][1] = 177;
            self.comTable.FEF[0][2] = 187;
            self.comTable.FEF[0][3] = 193;
            self.comTable.FEF[0][4] = 201;
            self.comTable.FEF[1][0] = 178;
            self.comTable.FEF[1][1] = 187;
            self.comTable.FEF[1][2] = 198;
            self.comTable.FEF[1][3] = 205;
            self.comTable.FEF[1][4] = 213;
            self.comTable.FEF[2][0] = 188;
            self.comTable.FEF[2][1] = 197;
            self.comTable.FEF[2][2] = 209;
            self.comTable.FEF[2][3] = 216;
            self.comTable.FEF[2][4] = 223;
        elif oasCategory_0 == OasCategory.ILS2AP:
            self.comTable.FAB[0] = 268;
            self.comTable.FAB[1] = 173;
            self.comTable.FAB[2] = 128;
            self.comTable.FBC[0] = 51;
            self.comTable.FBC[1] = 66;
            self.comTable.FBC[2] = 80;
            self.comTable.FGD = 135;
            self.comTable.FTANX[0][0] = 0.2296;
            self.comTable.FTANX[0][1] = 0.2538;
            self.comTable.FTANX[0][2] = 0.3;
            self.comTable.FTANX[1][0] = 0.2489;
            self.comTable.FTANX[1][1] = 0.2752;
            self.comTable.FTANX[1][2] = 0.3125;
            self.comTable.FTANX[2][0] = 0.2562;
            self.comTable.FTANX[2][1] = 0.2854;
            self.comTable.FTANX[2][2] = 0.3275;
            self.comTable.FTANX[3][0] = 0.2579;
            self.comTable.FTANX[3][1] = 0.2878;
            self.comTable.FTANX[3][2] = 0.3333;
            self.comTable.FTANW[0] = 0.0298;
            self.comTable.FTANW[1] = 0.0358;
            self.comTable.FTANW[2] = 0.0415;
            self.comTable.FTANWS[0] = 0.0354;
            self.comTable.FTANWS[1] = 0.042;
            self.comTable.FTANWS[2] = 0.0489;
            self.comTable.FEF[0][0] = 169;
            self.comTable.FEF[0][1] = 177;
            self.comTable.FEF[0][2] = 187;
            self.comTable.FEF[0][3] = 198;
            self.comTable.FEF[0][4] = 201;
            self.comTable.FEF[1][0] = 178;
            self.comTable.FEF[1][1] = 187;
            self.comTable.FEF[1][2] = 198;
            self.comTable.FEF[1][3] = 205;
            self.comTable.FEF[1][4] = 213;
            self.comTable.FEF[2][0] = 188;
            self.comTable.FEF[2][1] = 197;
            self.comTable.FEF[2][2] = 209;
            self.comTable.FEF[2][3] = 216;
            self.comTable.FEF[2][4] = 223;

        self.comTable.CG[0] = 0.05;
        self.comTable.CG[1] = 0.04;
        self.comTable.CG[2] = 0.03;
        self.comTable.CG[3] = 0.025;
        self.comTable.CG[4] = 0.02;

    def method_8(self, oasCategory_0, double_0, double_1, aircraftSize_0):
        fEF = [0.0, 0.0, 0.0]
        if (aircraftSize_0 != AircraftSize.Large):
            self.comSurco.AG = self.method_3(double_0, self.comTable.YT, self.comTable.FAG);
            self.comSurco.AF = self.comTable.FAF;
            self.comSurco.AB = self.method_3(double_0, self.comTable.YT, self.comTable.FAB);
            self.comSurco.BC = self.method_3(double_0, self.comTable.YT, self.comTable.FBC);
            self.comSurco.GD = self.comTable.FGD;
            self.comSurco.TANMU = (self.comSurco.GD - self.comSurco.BC) / (self.comSurco.AG + self.comSurco.AB);
            self.comSurco.TANX = self.method_5(double_1, double_0, self.comTable.XT, self.comTable.YT, self.comTable.FTANX);
            self.comSurco.TANW = self.method_3(double_0, self.comTable.YT, self.comTable.FTANW);
            if (oasCategory_0 == OasCategory.ILS2AP):
                self.comSurco.TANWS = self.method_3(double_0, self.comTable.YT, self.comTable.FTANWS);
            for i in range(4 + 1):
                for j in range(2 + 1):
                    fEF[j] = self.comTable.FEF[j][i];
                self.comSurco.EF[i] = self.method_3(double_0, self.comTable.YT, fEF);
                self.comSurco.TANNU[i] = (self.comSurco.EF[i] - self.comSurco.GD) / (self.comSurco.AF - self.comSurco.AG);
                self.comSurco.TANZ[i] = self.comTable.CG[i];

        self.comSurco.AW = self.comSurco.TANW;
        self.comSurco.BW = 0;
        self.comSurco.CW = -self.comSurco.AB * self.comSurco.TANW;
        if (oasCategory_0 == OasCategory.ILS2AP):
            self.comSurco.AWS = self.comSurco.TANWS;
            self.comSurco.BWS = 0;
            self.comSurco.CWS = 1000 * (self.comSurco.TANW - self.comSurco.TANWS) - self.comSurco.AB * self.comSurco.TANW;

        self.comSurco.AX = self.comSurco.TANMU * self.comSurco.TANX;
        self.comSurco.BX = self.comSurco.TANX;
        self.comSurco.CX = (-self.comSurco.GD + self.comSurco.AG * self.comSurco.TANMU) * self.comSurco.TANX;
        for k in range(4 + 1):
            self.comSurco.AZ[k] = -self.comSurco.TANZ[k];
            self.comSurco.CZ[k] = -self.comSurco.AF * self.comSurco.TANZ[k];

        self.comSurco.BZ = 0;
        self.comTemp1.XC = self.comSurco.AB;
        self.comTemp1.YC = self.comSurco.BC;
        self.comTemp1.XD = -self.comSurco.AG;
        self.comTemp1.YD = self.comSurco.GD;
        self.comTemp1.XE = -self.comSurco.AF;
        for l in range(4 + 1):
            self.comTemp1.YE[l] = self.comSurco.EF[l];

        aW = 300;
        if (oasCategory_0 == OasCategory.ILS2 or oasCategory_0 == OasCategory.ILS2AP):
            aW = 150;

        self.comTemp1.XC1 = (aW - self.comSurco.CW) / self.comSurco.AW;
        if (oasCategory_0 == OasCategory.ILS2AP):
            self.comTemp1.XC1 = (aW - self.comSurco.CWS) / self.comSurco.AWS;

        self.comTemp1.YC1 = (aW - self.comSurco.AX * self.comTemp1.XC1 - self.comSurco.CX) / self.comSurco.BX;
        num = math.tan(Unit.ConvertDegToRad(double_0));
        aG = aW / num - self.comSurco.AG;
        aX = (aW - self.comSurco.AX * aG - self.comSurco.CX) / self.comSurco.BX;
        if oasCategory_0 == OasCategory.ILS1 \
            or oasCategory_0 == OasCategory.SBAS_APV1 \
            or oasCategory_0 == OasCategory.SBAS_APV2 \
            or oasCategory_0 == OasCategory.SBAS_CAT1:
                for m in range(4 + 1):
                    self.comSurco.TANY[m] = aW * (-self.comSurco.AF + self.comSurco.AG) / ((self.comSurco.AG - self.comSurco.AF) * (aX - self.comSurco.GD) + (self.comSurco.AG + aG) * (self.comSurco.GD - self.comSurco.EF[m]));
        elif oasCategory_0 == OasCategory.ILS2:
            for n in range(4 + 1):
                self.comSurco.TANY[n] = aW * (-self.comSurco.AF + self.comSurco.AG) / ((self.comSurco.AG - self.comSurco.AF) * (aX - self.comSurco.GD) + (self.comSurco.AG + aG) * (self.comSurco.GD - self.comSurco.EF[n]));
        elif oasCategory_0 == OasCategory.ILS2AP:
            for o in range(4 + 1):
                self.comSurco.TANY[o] = aW * (-self.comSurco.AF + self.comSurco.AG) / ((self.comSurco.AG - self.comSurco.AF) * (aX - self.comSurco.GD) + (self.comSurco.AG + aG) * (self.comSurco.GD - self.comSurco.EF[o]));
        
        for p in range(4 + 1):
            self.comSurco.AY[p] = self.comSurco.TANNU[p] * self.comSurco.TANY[p];
            self.comSurco.BY[p] = self.comSurco.TANY[p];
            self.comSurco.CY[p] = (-self.comSurco.GD + self.comSurco.AG * self.comSurco.TANNU[p]) * self.comSurco.TANY[p];

        for q in range(4 + 1):
            self.comTemp1.XD1[q] = aG;
            self.comTemp1.YD1[q] = aX;
            if (oasCategory_0 != OasCategory.ILS2AP):
                lstParam = [self.comTemp1.XE1[q], self.comTemp1.YE1[q]]
                self.method_6(self.comSurco.AY[q], self.comSurco.BY[q], self.comSurco.CY[q], self.comSurco.AZ[q], self.comSurco.BZ, self.comSurco.CZ[q], aW, lstParam);
                self.comTemp1.XE1[q] = lstParam[0]
                self.comTemp1.YE1[q] = lstParam[1]
            else:
                lstParam = [self.comTemp1.XD1[q], self.comTemp1.YD1[q]]
                self.method_6(self.comSurco.AX, self.comSurco.BX, self.comSurco.CX, self.comSurco.AY[q], self.comSurco.BY[q], self.comSurco.CY[q], aW, lstParam);
                self.comTemp1.XD1[q] = lstParam[0]
                self.comTemp1.YD1[q] = lstParam[1]

        if (oasCategory_0 == OasCategory.ILS2AP):
            aW = self.comSurco.AW * 1000 + self.comSurco.CW;
            self.comTemp1.XC2 = (aW - self.comSurco.CW) / self.comSurco.AW;
            self.comTemp1.YC2 = (aW - self.comSurco.AX * self.comTemp1.XC2 - self.comSurco.CX) / self.comSurco.BX;

    def method_9(self, aircraftSize_0):
        if (aircraftSize_0 == AircraftSize.Standard):
            num = 6;
            num1 = 30;
            num2 = 3;
            num3 = 12;
            num4 = 35;
            num5 = 9;
            tANW = (num3 - num) / self.comSurco.TANW;
            self.comSurco.AB = self.comSurco.AB + tANW;
            tANX = num3 / self.comSurco.TANX;
            tANX1 = num4 + num5 / self.comSurco.TANX;
            tANX2 = num / self.comSurco.TANX;
            tANX3 = num1 + num2 / self.comSurco.TANX;
            num6 = max([tANX, tANX1]) - max([tANX2, tANX3]);
            self.comSurco.GD = self.comSurco.GD + num6;
            for i in range(4 + 1):
                self.comSurco.EF[i] = self.comSurco.EF[i] + num6;
            self.comSurco.BC = self.comSurco.BC - tANW * self.comSurco.TANMU + num6;


class ComSurco:

    def __init__(self):
        self.EF = [0,0,0,0,0]
        self.TANY = [0,0,0,0,0]
        self.TANNU = [0,0,0,0,0]
        self.TANZ = [0,0,0,0,0]
        self.AY = [0,0,0,0,0]
        self.BY = [0,0,0,0,0]
        self.CY = [0,0,0,0,0]
        self.AZ = [0,0,0,0,0]
        self.CZ = [0,0,0,0,0]
        self.method_0()

    def method_0(self):
        self.AG = 0;
        self.AF = 0;
        self.AB = 0;
        self.BC = 0;
        self.GD = 0;
        self.TANMU = 0;
        self.TANX = 0;
        self.TANW = 0;
        self.AW = 0;
        self.BW = 0;
        self.CW = 0;
        self.AWS = 0;
        self.BWS = 0;
        self.CWS = 0;
        self.AX = 0;
        self.BX = 0;
        self.CX = 0;
        self.BZ = 0;
        self.TANWS = 0;

class ComTable:

    def __init__(self):
        self.XT = [0.0, 0.0, 0.0, 0.0]
        self.YT = [0.0, 0.0, 0.0]
        self.FAG = [0.0, 0.0, 0.0]
        self.FAB = [0.0, 0.0, 0.0]
        self.FBC = [0.0, 0.0, 0.0]
        self.FTANX = [[0.0, 0.0, 0.0], 
                      [0.0, 0.0, 0.0], 
                      [0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0]]
        self.FTANW = [0.0, 0.0, 0.0]
        self.FTANWS = [0.0, 0.0, 0.0]
        self.FEF = [[0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0]]
        self.FTANY = [[[0.0, 0.0, 0.0, 0.0], 
                       [0.0, 0.0, 0.0, 0.0], 
                       [0.0, 0.0, 0.0, 0.0]],
                      [[0.0, 0.0, 0.0, 0.0], 
                       [0.0, 0.0, 0.0, 0.0], 
                       [0.0, 0.0, 0.0, 0.0]],
                      [[0.0, 0.0, 0.0, 0.0], 
                       [0.0, 0.0, 0.0, 0.0], 
                       [0.0, 0.0, 0.0, 0.0]],
                      [[0.0, 0.0, 0.0, 0.0], 
                       [0.0, 0.0, 0.0, 0.0], 
                       [0.0, 0.0, 0.0, 0.0]],
                      [[0.0, 0.0, 0.0, 0.0], 
                       [0.0, 0.0, 0.0, 0.0], 
                       [0.0, 0.0, 0.0, 0.0]],]
        self.CG = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.method_0()

    def method_0(self):
 
        self.FAF = 0;

        self.FGD = 0;


class ComTemp1:

    def __init__(self):
        self.YE = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.XD1 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.YD1 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.XE1 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.YE1 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.XD2 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.YD2 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.XE2 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.YE2 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.A3 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.A5 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.A6 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.A7 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.A8 = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.method_0();

    def method_0(self):
        self.XC = 0;
        self.YC = 0;
        self.XD = 0;
        self.YD = 0;
        self.XE = 0;
        self.XC1 = 0;
        self.YC1 = 0;
        self.XC2 = 0;
        self.YC2 = 0;
        self.A1 = 0;
        self.A2 = 0;
        self.A4 = 0;

