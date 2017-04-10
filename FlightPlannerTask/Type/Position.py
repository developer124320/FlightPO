
from FlightPlanner.types import PositionType, Point3D
from FlightPlanner.helpers import Altitude, AltitudeUnits
from FlightPlanner.messages import Messages
from FlightPlanner.Captions import Captions
from FlightPlanner.QgisHelper import Geo
from Type.Degrees import Degrees
from Type.String import String, StringBuilder, QString

import math

class Position:
    def __init__(self, positionType = None, idValueStr = None, xlatValue = None, ylonValue = None, altitudeValue = None, degreesLatValue = None, degreesLonValue = None):
        self.type = PositionType.Position
        self.xy = True
        self.id = None
        self.xlat = None
        self.ylon = None
        self.altitude = None
        
        if positionType == None and idValueStr == None and xlatValue == None and ylonValue == None and \
                                    altitudeValue == None and degreesLatValue == None and degreesLonValue == None:
            self.type = PositionType.Position
            self.xy = True
            self.id = None
            self.xlat = None
            self.ylon = None
            self.altitude = None
        elif positionType != None and idValueStr == None and xlatValue == None and ylonValue == None and \
                                    altitudeValue == None and degreesLatValue == None and degreesLonValue == None:
            self.type = positionType
            self.xy = True
            self.id = None
            self.xlat = None
            self.ylon = None
            self.altitude = None
        elif positionType == None and idValueStr == None and xlatValue != None and ylonValue != None and \
                                    altitudeValue == None and degreesLatValue == None and degreesLonValue == None:
            self.type = PositionType.Position
            self.xy = True
            self.id = None
            self.xlat = xlatValue
            self.ylon = ylonValue
            self.altitude = None
        elif positionType != None and idValueStr == None and xlatValue != None and ylonValue != None and \
                                    altitudeValue == None and degreesLatValue == None and degreesLonValue == None:
            self.type = positionType
            self.xy = True
            self.id = None
            self.xlat = xlatValue
            self.ylon = ylonValue
            self.altitude = None
        elif positionType == None and idValueStr == None and xlatValue != None and ylonValue != None and \
                                    altitudeValue != None and degreesLatValue == None and degreesLonValue == None:
            self.type = PositionType.Position
            self.xy = True
            self.id = None
            self.xlat = xlatValue
            self.ylon = ylonValue
            self.altitude = altitudeValue.Metres
        elif positionType != None and idValueStr == None and xlatValue != None and ylonValue != None and \
                                    altitudeValue != None and degreesLatValue == None and degreesLonValue == None:
            self.type = positionType
            self.xy = True
            self.id = None
            self.xlat = xlatValue
            self.ylon = ylonValue
            self.altitude = altitudeValue.Metres
        elif positionType == None and idValueStr != None and xlatValue != None and ylonValue != None and \
                                    altitudeValue == None and degreesLatValue == None and degreesLonValue == None:
            self.type = PositionType.Position
            self.xy = True
            self.id = idValueStr
            self.xlat = xlatValue
            self.ylon = ylonValue
            self.altitude = None
        elif positionType != None and idValueStr != None and xlatValue != None and ylonValue != None and \
                                    altitudeValue == None and degreesLatValue == None and degreesLonValue == None:
            self.type = positionType
            self.xy = True
            self.id = idValueStr
            self.xlat = xlatValue
            self.ylon = ylonValue
            self.altitude = None
        elif positionType == None and idValueStr != None and xlatValue != None and ylonValue != None and \
                                    altitudeValue != None and degreesLatValue == None and degreesLonValue == None:
            self.type = PositionType.Position
            self.xy = True
            self.id = idValueStr
            self.xlat = xlatValue
            self.ylon = ylonValue
            self.altitude = altitudeValue.Metres
        elif positionType != None and idValueStr != None and xlatValue != None and ylonValue != None and \
                                    altitudeValue != None and degreesLatValue == None and degreesLonValue == None:
            self.type = positionType
            self.xy = True
            self.id = idValueStr
            self.xlat = xlatValue
            self.ylon = ylonValue
            self.altitude = altitudeValue.Metres
        elif positionType == None and idValueStr == None and xlatValue == None and ylonValue == None and \
                                    altitudeValue == None and degreesLatValue != None and degreesLonValue != None:
            self.type = PositionType.Position
            self.xy = False
            self.id = None
            self.xlat = degreesLatValue.Value
            self.ylon = degreesLonValue.Value
            self.altitude = None
        elif positionType != None and idValueStr == None and xlatValue == None and ylonValue == None and \
                                    altitudeValue == None and degreesLatValue != None and degreesLonValue != None:
            self.type = positionType
            self.xy = False
            self.id = None
            self.xlat = degreesLatValue.Value
            self.ylon = degreesLonValue.Value
            self.altitude = None
        elif positionType == None and idValueStr == None and xlatValue == None and ylonValue == None and \
                                    altitudeValue != None and degreesLatValue != None and degreesLonValue != None:
            self.type = PositionType.Position
            self.xy = False
            self.id = None
            self.xlat = degreesLatValue.Value
            self.ylon = degreesLonValue.Value
            self.altitude = altitudeValue.Metres
        elif positionType != None and idValueStr == None and xlatValue == None and ylonValue == None and \
                                    altitudeValue != None and degreesLatValue != None and degreesLonValue != None:
            self.type = positionType
            self.xy = False
            self.id = None
            self.xlat = degreesLatValue.Value
            self.ylon = degreesLonValue.Value
            self.altitude = altitudeValue.Metres
        elif positionType == None and idValueStr != None and xlatValue == None and ylonValue == None and \
                                    altitudeValue == None and degreesLatValue != None and degreesLonValue != None:
            self.type = PositionType.Position
            self.xy = False
            self.id = idValueStr
            self.xlat = degreesLatValue.Value
            self.ylon = degreesLonValue.Value
            self.altitude = None
        elif positionType != None and idValueStr != None and xlatValue == None and ylonValue == None and \
                                    altitudeValue == None and degreesLatValue != None and degreesLonValue != None:
            self.type = positionType
            self.xy = False
            self.id = idValueStr
            self.xlat = degreesLatValue.Value
            self.ylon = degreesLonValue.Value
            self.altitude = None
        elif positionType == None and idValueStr != None and xlatValue == None and ylonValue == None and \
                                    altitudeValue != None and degreesLatValue != None and degreesLonValue != None:
            self.type = PositionType.Position
            self.xy = False
            self.id = idValueStr
            self.xlat = degreesLatValue.Value
            self.ylon = degreesLonValue.Value
            self.altitude = altitudeValue.Metres
        elif positionType != None and idValueStr != None and xlatValue == None and ylonValue == None and \
                                    altitudeValue != None and degreesLatValue != None and degreesLonValue != None:
            self.type = positionType
            self.xy = False
            self.id = idValueStr
            self.xlat = degreesLatValue.Value
            self.ylon = degreesLonValue.Value
            self.altitude = altitudeValue.Metres
        
    def get_altitude(self):
        return Altitude(self.altitude)
    def set_altitude(self, value):
        self.altitude = value.Metres
    AltitudeValue = property(get_altitude, set_altitude, None, None)
    
    def get_ID(self):
        return self.id
    def set_ID(self, value):
        self.id = value
    ID = property(get_ID, set_ID, None, None)
    
    def isEmpty(self):
        if (not self.xlat == None):
            return False
        return self.ylon == None
    IsEmpty = property(isEmpty, None, None, None)
    
    def isValid(self):
        if (self.xlat == None or self.xlat == None or self.ylon == None):
            return False
        return not math.isinf(self.ylon)
    IsValid = property(isValid, None, None, None)
    
    def isValidIncludingAltitude(self):
        if (self.xlat == None or math.isinf(self.xlat) or self.ylon == None or math.isinf(self.ylon) or self.altitude == None):            return False
        return not math.isinf(self.altitude)
    IsValidIncludingAltitude = property(isValidIncludingAltitude, None, None, None)

    def isXY(self):
        return self.xy
    IsXY = property(isXY, None, None, None)

    def get_Point3d(self):
        if (not self.IsValid):
            raise Messages.ERR_INVALID_OR_INCOMPLETE_POSITION
        if (self.xy):
            if (self.altitude == None or math.isinf(self.altitude)):
                return Point3D(self.xlat, self.ylon, 0)
            return Point3D(self.xlat, self.ylon, self.altitude)
        result, num, num1 = Geo.smethod_3(Degrees.smethod_1(self.xlat), Degrees.smethod_5(self.ylon))
        if (not result):
            raise "Geo.LastError"
        if (self.altitude == None or math.isinf(self.altitude)):
            return Point3D(num, num1, 0)
        return Point3D(num, num1, self.altitude)
    def set_Point3d(self, point3d):
        self.xy = True
        self.xlat = point3d.get_X()
        self.ylon = point3d.get_Y()
        self.altitude = point3d.get_Z()
    Point3d = property(get_Point3d, set_Point3d, None, None)

    def get_Type(self):
        return self.type
    def set_Type(self, value):
        self.type = value
    Type = property(get_Type, set_Type, None, None)

    def get_XLat(self):
        return self.xlat
    def set_XLat(self, value):
        self.xlat = value
    XLat = property(get_XLat, set_XLat, None, None)

    def get_YLon(self):
        return self.ylon
    def set_YLon(self, value):
        self.ylon = value
    YLon = property(get_YLon, set_YLon, None, None)

    def __eq__(self, other):
        if not isinstance(other, Position) or other == None:
            return False
        if (not self.xy == other.xy or not self.id == other.id or not self.xlat == other.xlat or not self.ylon == other.ylon):
            return False
        return self.altitude == other.altitude
# 
#     public override int GetHashCode()
#     {
#         if (string.IsNullOrEmpty(self.id))
#         {
#             return self.xy.GetHashCode() ^ self.xlat.GetHashCode() ^ self.ylon.GetHashCode() ^ self.altitude.GetHashCode()
#         }
#         return self.xy.GetHashCode() ^ self.id.GetHashCode() ^ self.xlat.GetHashCode() ^ self.ylon.GetHashCode() ^ self.altitude.GetHashCode()
#     }
# 
    def method_0(self):
        if (self.xy):
            xlatValue = self.xlat
            ylonValue = self.ylon
            return True, xlatValue, ylonValue
        result, ylonValue, xlatValue = Geo.smethod_3(Degrees.smethod_1(self.xlat), Degrees.smethod_5(self.ylon))
        return result, xlatValue, ylonValue

    def method_1(self):
        if (self.xy):
            return Geo.smethod_2(self.xlat, self.ylon)
        degreesLat = Degrees.smethod_1(self.xlat)
        degreesLon = Degrees.smethod_5(self.ylon)
        return True, degreesLat, degreesLon

    def method_2(self):
        result, xlatValue, ylonValue = self.method_0()
        if (not result):
            raise "Geo.LastError"
        return Position(self.type, self.id, xlatValue, ylonValue, Altitude(self.altitude), None, None)

    def method_3(self):
        result, degreesLat, degreesLon = self.method_1()
        if (not result):
            raise "Geo.LastError"
        return Position(self.type, self.id, None, None, Altitude(self.altitude), degreesLat, degreesLon)
# 
    def method_4(self):
        if (self.xy):
            return Position(self.type, self.id, self.xlat, self.ylon, Altitude(self.altitude))
        return Position(self.type, self.id, None, None, Altitude(self.altitude), Degrees.smethod_1(self.xlat), Degrees.smethod_5(self.ylon))

    def method_5(self, string_0):
        return self.ToString(string_0)

    def method_6(self, iformatProvider_0):
        return self.ToString()

    # public static bool operator ==(Position value1, Position value2)
    # {
    #     return object.Equals(value1, value2)
    # }
# 
#     public static bool operator !=(Position value1, Position value2)
#     {
#         return !(value1 == value2)
#     }
# 
    @staticmethod
    def smethod_0(position):
        if (position == None):
            return False
        return position.IsValid
# 
#     public override string ToString()
#     {
#         return self.ToString(null, CultureInfo.CurrentCulture)
#     }
# 
    def ToString(self, format_0 = None):
        stringBuilder = StringBuilder()
        if format_0 == None:
            format_0 = ""
        if not isinstance(format_0, QString):
            format_0 = String.Str2QString(format_0)
        # if (provider == null)
        # {
        #     provider = CultureInfo.CurrentCulture
        # }
        if (not String.IsNullOrEmpty(format_0)):
            format_0 = format_0.toUpper()
            if (format_0.contains("QA:")):
                format_0 = format_0.replace("QA:", "")
                num = 0
                try:
                    num = int(format_0)
                except:
                    num = 0
                stringBuilder = StringBuilder()
                str0 = ""
                for i in range(num):
                    str0 = QString(String.Concat([str0, " "]))
                if (not String.IsNullOrEmpty(self.id)):
                    stringBuilder.AppendLine("{0}{1}\t{2}".format(str0, Captions.ID, self.id))
                if (not self.xy):
                    lATITUDE = Captions.LATITUDE
                    degree = Degrees.smethod_1(self.xlat)
                    stringBuilder.AppendLine("{0}{1}\t{2}".format(str0, lATITUDE, degree.method_2()))
                    lONGITUDE = Captions.LONGITUDE
                    degree1 = Degrees.smethod_5(self.ylon)
                    stringBuilder.Append("{0}{1}\t{2}".format(str0, lONGITUDE, degree1.method_2()))
                else:
                    stringBuilder.AppendLine("{0}{1}\t{2}".format(str0, Captions.X, str(self.xlat)))#.ToString(Formats.GridXYFormat, provider)))
                    stringBuilder.Append("{0}{1}\t{2}".format(str0, Captions.Y, str(self.ylon)))#.ToString(Formats.GridXYFormat, provider)))
                if (not self.altitude == None):
                    altitude = Altitude(self.altitude)
                    stringBuilder.AppendLine("")
                    aLTITUDE = [str0, Captions.ALTITUDE, altitude.ToString(":m"), altitude.ToString(":ft")]
                    stringBuilder.Append("{0}{1}\t{2} ({3})".format(str0, Captions.ALTITUDE, altitude.ToString(":m"), altitude.ToString(":ft")))
                return stringBuilder.ToString()
        stringBuilder = StringBuilder()
        if (not String.IsNullOrEmpty(self.id)):
            stringBuilder.Append(self.id + ", ")
        if (not self.xy):
            degree2 = Degrees.smethod_1(self.xlat)
            str1 = degree2.method_2()
            degree3 = Degrees.smethod_5(self.ylon)
            stringBuilder.Append(str1 + ", " + degree3.method_2())
        else:
            stringBuilder.Append(str(self.xlat) + ", " + str(self.ylon))
        if (not self.altitude == None):
            altitude1 = Altitude(self.altitude)
            stringBuilder.Append(", {0} ({1})", ", " + altitude1.ToString(":m") + " (" + altitude1.ToString(":ft") + ")")
        return stringBuilder.ToString()