from FlightPlanner.types import DegreesStyle, DegreesType
from Type.String import String, StringBuilder
from PyQt4.QtCore import QString
import math, define
class Degrees:
    def __init__(self, double_0 = None, double_1 = None, double_2 = None, degreesType_0 = None):
        self.value = None
        self.type = None
        self.defaultformatStr = "ddmmss.ssssH";
        if degreesType_0 != None:
            if degreesType_0 == DegreesType.Longitude:
                self.defaultformatStr = "dddmmss.ssssH";

        if double_0 == None and double_1 == None and double_2 == None:
            self.value = None;
            self.type = DegreesType.Degrees;
            self.method_0();
            return
        if double_1 == None and double_2 == None and degreesType_0 == None:
            self.value = double_0;
            self.type = DegreesType.Degrees;
            self.method_0();
            return
        if double_2 == None and degreesType_0 == None:
            self.value = double_0 + double_1 / 60;
            self.type = DegreesType.Degrees;
            self.method_0();
            return
        if degreesType_0 == None:
            self.value = double_0 + double_1 / 60 + double_2 / 3600;
            self.type = DegreesType.Degrees;
            self.method_0();
            return
        if double_1 == None and double_2 == None:
            self.value = double_0;
            self.type = degreesType_0
            self.method_0();
            return
        if double_2 == None:
            self.value =  double_0 + double_1 / 60;
            self.type = degreesType_0
            self.method_0();
            return

        self.value =  double_0 + double_1 / 60 + double_2 / 3600;
        self.type = degreesType_0

        self.method_0();
        pass

    def method_0(self):
#         switch (self.type)
#     {
        if self.type == DegreesType.Latitude:
            if (self.value >= -90 and self.value <= 90):
                return
            raise ValueError("ERR_LATITUDE_OUT_OF_BOUNDS")
#             throw new Exception(string.Format(Messages.ERR_LATITUDE_OUT_OF_BOUNDS, self.value));
        elif self.type == DegreesType.Longitude:
            if (self.value >= -180 and self.value <= 180):
                return
            raise ValueError("ERR_LONGITUDE_OUT_OF_BOUNDS")
#             throw new Exception(string.Format(Messages.ERR_LONGITUDE_OUT_OF_BOUNDS, self.value));
        elif self.type == DegreesType.Variation:
            if (self.value >= -180 and self.value <= 180):
                return
            raise ValueError("ERR_VARIATION_OUT_OF_BOUNDS")
#             throw new Exception(string.Format(Messages.ERR_VARIATION_OUT_OF_BOUNDS, self.value));

    def method_1(self, string_0 = None):
        return self.ToString(string_0);
    def method_2(self):
        return self.ToString("G")

    def method_3(self, degrees_0):
        if (self.method_1("dddmmss.ssssh") != degrees_0.method_1("dddmmss.ssssh")):
            return False;
        return self.type == degrees_0.type;


    @staticmethod
    def String2Degree(qStr):
        qStr = String.Str2QString(qStr)
        degreeFormat = qStr.right(1)
        existFormat = False
        tempDegreeStr = None
        if degreeFormat == "E" or degreeFormat == "W" or\
           degreeFormat == "e" or degreeFormat == "w" or\
           degreeFormat == "N" or degreeFormat == "S" or\
           degreeFormat == "n" or degreeFormat == "s":
            existFormat = True
        if existFormat:
            tempDegreeStr = qStr.left(qStr.length() - 1)
        else:
            tempDegreeStr = qStr
        tempDegreeFloat = None
        try:
            tempDegreeFloat = float(tempDegreeStr)
        except:
            return None
        ssDecimal = tempDegreeFloat - int(tempDegreeFloat)
        degreeQStrWithOutDecimal = QString(str(int(tempDegreeFloat)))
        ssInt = int(degreeQStrWithOutDecimal.right(2))
        degreeQStrWithOutDecimal = degreeQStrWithOutDecimal.left(degreeQStrWithOutDecimal.length() - 2)
        mmInt = int(degreeQStrWithOutDecimal.right(2))
        degreeQStrWithOutDecimal = degreeQStrWithOutDecimal.left(degreeQStrWithOutDecimal.length() - 2)
        ddInt = int(degreeQStrWithOutDecimal)

        decimaldegree = ddInt + float(mmInt) / 60 + float(ssInt + ssDecimal) / 3600

        if degreeFormat == "E" or degreeFormat == "W" or\
           degreeFormat == "e" or degreeFormat == "w":
            return Degrees(decimaldegree, None, None, DegreesType.Longitude)
        elif degreeFormat == "N" or degreeFormat == "S" or\
             degreeFormat == "n" or degreeFormat == "s":
            return Degrees(decimaldegree, None, None, DegreesType.Latitude)
        return Degrees(decimaldegree)

    @staticmethod
    def smethod_1(double_0):
        return Degrees(double_0, None, None, DegreesType.Latitude);

    @staticmethod
    def smethod_5(double_0):
        return Degrees(double_0, None, None, DegreesType.Longitude);

    @staticmethod
    def smethod_12(degreesStyle_0, degreesStyle_1):
        return (degreesStyle_0 & degreesStyle_1) == degreesStyle_1;
    @staticmethod
    def smethod_15(string_0, degreesType_0):
#         string_0 = "11223"
#         s = "fsafs"
#         s.
        if isinstance(string_0, str):
            string_0 = String.Str2QString(string_0)
        num = string_0.indexOf('.');
        if (num == -1):
            num = string_0.indexOf("N");
        if (num == -1):
            num = string_0.indexOf("S");
        if (num == -1):
            num = string_0.indexOf("E");
        if (num == -1):
            num = string_0.indexOf("W");
        if (num == -1):
            num = string_0.indexOf("n");
        if (num == -1):
            num = string_0.indexOf("s");
        if (num == -1):
            num = string_0.indexOf("e");
        if (num == -1):
            num = string_0.indexOf("w");
#         try
#         {
        str0 = string_0[:num];
        degreesStyle = None
#         DegreesStyle degreesStyle = DegreesStyle.Degrees;
        if (degreesType_0 == DegreesType.Latitude):
            if (str0.size() == 6):
                degreesStyle = DegreesStyle.DegreesMinutesSeconds;
            elif (str0.size() == 4):
                degreesStyle = DegreesStyle.DegreesMinutes;
            elif (str0.size() != 2):
                raise ValueError("NOT_VALID_LATITUDE_VALUE")
#                 throw new Exception(string.Format(Validations.NOT_VALID_LATITUDE_VALUE, string_0));
        elif (str0.size() == 7 or str0.size() == 6):
            degreesStyle = DegreesStyle.DegreesMinutesSeconds;
        elif (str0.size() == 5 or str0.size() == 4):
            degreesStyle = DegreesStyle.DegreesMinutes;
        elif (str0.size() != 3 or str0.size() == 2):
            raise ValueError("NOT_VALID_LONGITUDE_VALUE")
#             throw new Exception(string.Format(Validations.NOT_VALID_LONGITUDE_VALUE, string_0));
        degree = Degrees.smethod_17(string_0, degreesType_0, degreesStyle)
#         if (degree == None):
#             switch (degreesType_0)
#             {
#                 case DegreesType.Degrees:
#                 {
#                     throw new Exception(string.Format(Validations.NOT_VALID_DEGREES_VALUE, string_0));
#                 }
#                 case DegreesType.Latitude:
#                 {
#                     throw new Exception(string.Format(Validations.NOT_VALID_LATITUDE_VALUE, string_0));
#                 }
#                 case DegreesType.Longitude:
#                 {
#                     throw new Exception(string.Format(Validations.NOT_VALID_LONGITUDE_VALUE, string_0));
#                 }
#                 case DegreesType.Variation:
#                 {
#                     throw new Exception(string.Format(Validations.NOT_VALID_MAGNETIC_VARIATION_VALUE, string_0));
#                 }
#                 default:
#                 {
#                     throw new Exception(Messages.ERR_INVALID_DEGREES_TYPE);
#                 }
#             }
#         }
#     }
#         catch
#         {
#             throw;
#         }
        return degree;
#         pass
    @staticmethod
    def smethod_17(string_0, degreesType_0, degreesStyle_0):
        num = None;
        num1 = None;
        num2 = None;
        num3 = None;
        num4 = None;
        flag = False;
#         numberStyle = NumberStyles.Float;
        degrees_0 = Degrees(None, None, None, degreesType_0);
        try:
            string_0 = string_0.toUpper();
            num5 = 1;
            if (string_0.contains("+")):
                string_0 = string_0.replace("+", "");
            if (string_0.contains("-")):
                string_0 = string_0.replace("-", "");
                num5 = -1;
            if (string_0.contains("N")):
                string_0 = string_0.replace("N", "");
            if (string_0.contains("E")):
                string_0 = string_0.replace("E", "");
            if (string_0.contains("S")):
                string_0 = string_0.replace("S", "");
                num5 = -1;
            if (string_0.contains("W")):
                string_0 = string_0.replace("W", "");
                num5 = -1;
            if (not Degrees.smethod_12(degreesStyle_0, DegreesStyle.DelimitedBySpace)):
                string_0 = string_0.replace(" ", "");
            string_0 = string_0.trimmed();
            if (Degrees.smethod_12(degreesStyle_0, DegreesStyle.Degrees)):
                try:
                    num, result = string_0.toDouble()
#                 if (double.TryParse(string_0, numberStyle, iformatProvider_0, out num)):
#                     degrees_0 = math.fabs(num) * num5
                    degrees_0 =  Degrees(math.fabs(num) * num5, None, None, degreesType_0);
                    flag = degrees_0;
                    return flag;
                except:
                    return None
            elif (Degrees.smethod_12(degreesStyle_0, DegreesStyle.DegreesMinutes)):
                if (Degrees.smethod_12(degreesStyle_0, DegreesStyle.DelimitedBySpace)):
                    strArrays = string_0.split(" ".ToCharArray());
                    if (string_0.size() < 2):
                        flag = None;
                        return flag;
#                     elif (!double.TryParse(strArrays[0], numberStyle, iformatProvider_0, out num))
# #                     {
# #                         flag = false;
# #                         return flag;
# #                     }
                    else:
                        try:
                            degrees_0 = Degrees(math.fabs(num) * num5, math.fabs(num1) * num5, None, degreesType_0);
                        except:
                            flag = None;
                            return False
#                     else
#                     {
#                         flag = false;
#                         return flag;
#                     }
#                 }
                else:
                    try:
                        num3, result = string_0.toDouble()
        #                 {
                        num3 = math.fabs(num3) / 100;
                        num1 = (num3 - math.trunc(num3)) * 100;
                        num = math.trunc(num3);
                        degrees_0 = Degrees(num * num5, num1 * num5, None, degreesType_0);
                    except:
                        flag = None
                        return flag
                flag = degrees_0
                return flag
#                 }
#                 else
#                 {
#                     flag = false;
#                     return flag;
#                 }
#                 flag = true;
#                 return flag;
#             }
            elif (Degrees.smethod_12(degreesStyle_0, DegreesStyle.DegreesMinutesSeconds)):
                if (Degrees.smethod_12(degreesStyle_0, DegreesStyle.DelimitedBySpace)):
#                     string[] strArrays1 = string_0.Split(" ".ToCharArray());
#                     if ((int)strArrays1.Length < 3)
#                     {
#                         flag = false;
#                         return flag;
#                     }
#                     else if (!double.TryParse(strArrays1[0], numberStyle, iformatProvider_0, out num))
#                     {
#                         flag = false;
#                         return flag;
#                     }
#                     else if (!double.TryParse(strArrays1[1], numberStyle, iformatProvider_0, out num1))
#                     {
#                         flag = false;
#                         return flag;
#                     }
#                     else if (double.TryParse(strArrays1[2], numberStyle, iformatProvider_0, out num2))
#                     {
                    try:
                        degrees_0 = Degrees(math.fabs(num) * num5, math.fabs(num1) * num5, math.fabs(num2) * num5, degreesType_0);
                    except:
                        flag = None;
                        return flag;
#                     }
#                 }
                else:
                    try:
                        num4, result = string_0.toDouble()
                        num4 = math.fabs(num4) / 100;
                        num2 = (num4 - math.trunc(num4)) * 100;
                        num4 = float(math.trunc(num4)) / 100;
                        num1 = (num4 - math.trunc(num4)) * 100;
                        num = math.trunc(num4);
                        degrees_0 = Degrees(num * num5, num1 * num5, num2 * num5, degreesType_0);
                    except:
                        flag = None;
                        return flag;
#                 }
                flag = degrees_0;
                return flag;
#             }
#             return false;
#         }
#         catch (Exception exception)
        except:
            return None
#         {
#             return false;
#         }
        return flag;

    def get_IsNaN(self):
        return self.value == None
    IsNaN = property(get_IsNaN, None, None, None)


    def ToString(self, formatStr = None):
        if formatStr == None:
            return self.ToString("G")
        num = 0.0;
        num1 = 0.0;
        num2 = 0.0;
        if (self.IsNaN):
            return "";
        if (formatStr == None or formatStr == ""):
            formatStr = self.defaultformatStr;
        # if (provider == null)
        # {
        #     provider = CultureInfo.CurrentCulture;
        # }
        # s = QString(45)
        # s.toUpper()

        if isinstance(formatStr, QString):
            formatStr = formatStr.toUpper();
        else:
            formatStr = formatStr.upper();
        if (formatStr == "G"):
            formatStr = self.defaultformatStr.upper();
        stringBuilder = StringBuilder();
        strS = None;
        str1 = None;
        str2 = None;
        num3 = 0;
        num4 = 0;
        num5 = 0;
        length = -1;
        length1 = -1;
        length2 = -1;
        num6 = 0;
        while (len(formatStr) > num6):
            chr = formatStr[num6];
            if (chr == 'D'):
                if (strS != None):
                    return None
                    # throw new ArgumentException("formatStr");
                strS = "0";
                num6 += 1
                flag = False;
                while (len(formatStr) > num6):
                    if (formatStr[num6] != 'D'):
                        if (formatStr[num6] != '.'):
                            break;
                        strS = String.Concat([strS, "."]);
                        flag = True;
                        num6 += 1;
                    else:
                        strS = String.Concat([strS, "0"]);
                        if (flag):
                            num3 += 1;
                        num6 += 1;
                length = stringBuilder.Length;
            elif (chr == 'M'):
                if (strS == None):
                    return None
                    # throw new ArgumentException("formatStr");
                if (str1 != None):
                    return None
                    # throw new ArgumentException("formatStr");
                str1 = "0";
                num6 += 1;
                flag1 = False;
                while (len(formatStr) > num6):
                    if (formatStr[num6] != 'M'):
                        if (formatStr[num6] != '.'):
                            break;
                        str1 = String.Concat([str1, "."]);
                        flag1 = True;
                        num6 += 1;
                    else:
                        str1 = String.Concat([str1, "0"]);
                        if (flag1):
                            num4 += 1;
                        num6 += 1;
                length1 = stringBuilder.Length;
            elif (chr == 'S'):
                if (strS == None):
                    return None
                    # throw new ArgumentException("formatStr");
                if (str1 == None):
                    return None
                    # throw new ArgumentException("formatStr");
                if (str2 != None):
                    return None
                    # throw new ArgumentException("formatStr");
                str2 = "0";
                num6 += 1;
                flag2 = False;
                while (len(formatStr) > num6):
                    if (formatStr[num6] != 'S'):
                        if (formatStr[num6] != '.'):
                            break;
                        str2 = String.Concat([str2, "."]);
                        flag2 = True;
                        num6 += 1;
                    else:
                        str2 = String.Concat([str2, "0"]);
                        if (flag2):
                            num5 += 1;
                        num6 += 1;
                length2 = stringBuilder.Length;
            elif (chr == 'H'):
                if (self.type == DegreesType.Latitude):
                    if (self.value >= 0):
                        stringBuilder.Append("N");
                    else:
                        stringBuilder.Append("S");
                elif (self.type == DegreesType.Longitude or self.type == DegreesType.Variation):
                    if (self.value >= 0):
                        stringBuilder.Append("E");
                    else:
                        stringBuilder.Append("W");
                num6 += 1;
            elif (chr != '-'):
                stringBuilder.Append(chr);
                num6 += 1;
            else:
                if (self.value < 0):
                    stringBuilder.Append("-");
                num6 += 1;
        if (str2 != None):
            num = math.fabs(self.value) if(not math.isinf(self.value)) else 0;
            num7 = math.trunc(num);
            num8 = (num - num7) * 60;
            num9 = math.trunc(num8);
            num10 = round((num8 - num9) * 60, num5);
            if (num10 >= 60):
                num10 = num10 - 60;
                num9 = num9 + 1;
            if (num9 >= 60):
                num9 = num9 - 60;
                num7 = num7 + 1;

            stringBuilder.Insert(length2, String.Number2String(num10, str2));
            stringBuilder.Insert(length1, String.Number2String(num9, str1));
            stringBuilder.Insert(length, String.Number2String(num7, strS));
        elif (str1 == None):
            if (strS == None):
                return None
                # throw new ArgumentException("formatStr");
            num2 = math.fabs(self.value) if(not math.isinf(self.value)) else 0;
            num11 = round(num2, num3);
            stringBuilder.Insert(length, String.Number2String(num11, strS));
        else:
            num1 = math.fabs(self.value) if(not math.isinf(self.value)) else 0;
            num12 = math.trunc(num1);
            num13 = round((num1 - num12) * 60, num4);
            if (num13 >= 60):
                num13 = num13 - 60;
                num12 = num12 + 1;
            stringBuilder.Insert(length1, String.Number2String(num13, str1));
            stringBuilder.Insert(length, String.Number2String(num12, strS));

        return stringBuilder.ToString();
    def __eq__(self, b):
        if b == None:
            return self.value == None
        return self.value == b.value