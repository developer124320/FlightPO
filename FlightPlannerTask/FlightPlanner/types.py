'''
Created on Feb 20, 2015

@author: Administrator
'''

from qgis.core import QgsPoint
# from flightPlannerMain import QgsPoint
from Type.enum.enum import Enum
import math, define
import numpy




class QADefaultView:
    QA = "QA"
    Report = "Report"
class QASnapshotFormat:
    Jpeg = "Jpeg"
    Gif = "Gif"
    Png = "Png"

class QATableType:
    General = "General"
    OCAH = "OCAH"
    ObstacleList = "ObstacleList"
class QAFileVersion:
    V4 = "V4"
    V4_1 = "V4_1"
    V8 = "V8"
    V8_1 = "V8_1"
    V10 = "V10"

class QASessionType:
    Started = "Started"
    Opened = "Opened"
class QAExportType:
    QA = "QA"
    Report = "Report"
class QARecordType:
    Unknown = "Unknown"
    Attached = "Attached"
    Table = "Table"
    Comment = "Comment"
    Snapshot = "Snapshot"
    Session = "Session"

    VariableNames = ["Unknown", "Attached", "Table", "Comment", "Snapshot", "Session"]
    Items = [Unknown, Attached, Table, Comment, Snapshot, Session]
class QAColorCode:
    Nothing =0# "Noting"
    Blue =1# "Blue"
    Red =2# "Red"
    Green =3# "Green"
    Yellow =4# "Yellow"
    Cyan =5# "Cyan"
    Magenta = 6#"Magenta"

    VariableNames = ["Noting", "Blue", "Red", "Green", "Yellow", "Cyan", "Magenta"]
    Items = [Nothing, Blue, Red, Green, Yellow, Cyan, Magenta]
class QgsComposerOutputMode:
    Single = 0
    Atlas = 1
    # VariableNames = ["Single", "Atlas"]
    # Items = [Single, Atlas]
class AerodromeSurfacesDatumElevation:
    Arp = "Arp"
    Thr = "Thr"
    End = "End"
    Thr_End = "Thr_End"

    VariableNames = ["Arp", "Thr", "End", "Thr_End"]
    Items = [Arp, Thr, End, Thr_End]
class AerodromeSurfacesRunwayCode:
    Code1 = "Code1"
    Code2 = "Code2"
    Code3 = "Code3"
    Code4 = "Code4"

    VariableNames = ["Code1", "Code2", "Code3", "Code4"]
    Items = [Code1, Code2, Code3, Code4]

class AerodromeSurfacesApproachType:
    NonInstrument = "NonInstrument"
    NonPrecision = "NonPrecision"
    Precision = "Precision"

    VariableNames = ["NonInstrument", "NonPrecision", "Precision"]
    Items = [NonInstrument, NonPrecision, Precision]
class HeliportSurfacesApproachType:
    NonInstrument = "NonInstrument"
    NonPrecision = "NonPrecision"
    Precision = "Precision"

    VariableNames = ["NonInstrument", "NonPrecision", "Precision"]
    Items = [NonInstrument, NonPrecision, Precision]


class HeliportSurfacesSlopeCategory:
    A = "A"
    B = "B"
    C = "C"

    VariableNames = ["A", "B", "C"]
    Items = [A, B, C]

class HeliportSurfacesUsage:
    DayOnly = "DayOnly"
    Night = "Night"

    VariableNames = ["DayOnly", "Night"]
    Items = [DayOnly, Night]



class HeliportSurfacesApproachHeight:
    H90 = "H90"
    H60 = "H60"
    H45 = "H45"
    H30 = "H30"

    VariableNames = ["H90", "H60", "H45", "H30"]
    Items = [H90, H60, H45, H30]

class HeliportSurfacesApproachAngle:
    A3 = "A3"
    A6 = "A6"

    VariableNames = ["A3", "A6"]
    Items = [A3, A6]



class TurnInvolvedType:
    No = "No"
    Yes = "Yes"

    VariableNames = ["No", "Yes"]
    Items = [No, Yes]

class AerodromeSurfacesCriteriaType:
    Annex14 = "Annex14"
    Cap168 = "Cap168"
    Custom = "Custom"

    VariableNames = ["Annex14", "Cap168", "Custom"]
    Items = [Annex14, Cap168, Custom]

class AerodromeSurfacesBalkedLandingFrom:
    EndOfStrip = "EndOfStrip"
    EndOfRwyOr = "EndOfRwyOr"
    Exactly = "Exactly"

    VariableNames = ["EndOfStrip", "EndOfRwyOr", "Exactly"]
    Items = [EndOfStrip, EndOfRwyOr, Exactly]

class AerodromeSurfacesInnerHorizontalLocation:
    MidPoint = "MidPoint"
    Runway = "Runway"
    Strip = "Strip"

    VariableNames = ["MidPoint", "Runway", "Strip"]
    Items = [MidPoint, Runway, Strip]

class AerodromeSurfacesTakeOffFrom:
    CwyOr = "CwyOr"
    CwyExactly = "CwyExactly"

    VariableNames = ["CwyOr", "CwyExactly"]
    Items = [CwyOr, CwyExactly]

class CodeCatAcftAixm(Enum):
    A = "Category A"
    A20 = "Category A with 2% climb gradient"
    A30 = "Category A with 3% climb gradient"
    A35 = "Category A with 3.5% climb gradient"
    B = "Category B"
    C = "Category C"
    D = "Category D"
    E = "Category E"
    AB = "Category A and B"
    CD = "Category C and D"
    CDE = "Category C, D and E"
    BCD = "Category B, C and D"
    ABCD = "Category A, B, C and D"
    DE = "Category D and E"
    ABC = "Category A, B and C"
    H = "Category H - helicopter"
    Other = "Other"

    VariableNames = ["A", "A20", "A30", "A35", "B", "C", "D", "E", "AB", "CD", "CDE", "BCD", "ABCD", "DE", "ABC", "H", "Other"]
    Items = ["Category A", "Category A with 2% climb gradient", "Category A with 3% climb gradient",
             "Category A with 3.5% climb gradient", "Category B", "Category C",
             "Category D", "Category E", "Category A and B",
             "Category C and D", "Category C, D and E", "Category B, C and D",
             "Category A, B, C and D", "Category D and E", "Category A, B and C",
             "Category H - helicopter", "Other"]

class DataBaseProcedureExportDlgType(Enum):
    Created = "Created"
    Deleted = "Deleted"
    Updated = "Updated"

    VariableNames = ["Created", "Deleted", "Updated"]
    Items = ["Created", "Deleted", "Updated"]
class DataBaseProcedureExportType(Enum):
    Created = "Created"
    Deleted = "Deleted"
    Updated = "Updated"

    VariableNames = ["Created", "Deleted", "Updated"]
    Items = ["Created", "Deleted", "Updated"]
class CodeTypeApchAixm(Enum):
    STA = "Straight-in non-precision approach"
    STA1 = "Straight-in CAT I approach"
    STA2 = "Straight-in CAT II approach"
    STA3A = "Straight-in CAT III A approach"
    STA3B = "Straight-in CAT III B approach"
    STA3C = "Straight-in CAT III C approach"
    CA = "Circling approach"
    OTHER = "Other"

    VariableNames = ["STA", "STA1", "STA2", "STA3A", "STA3B", "STA3C", "CA", "OTHER"]
    Items = ["Straight-in non-precision approach", "Straight-in CAT I approach",
             "Straight-in CAT II approach", "Straight-in CAT III A approach",
             "Straight-in CAT III B approach", "Straight-in CAT III C approach",
             "Circling approach", "Other"]
class CodeTypeProcPathAixm(Enum):
    AF = "AF - constant DME arc to a fix"
    HF = "HF - hold pattern terminating at a fix after one circuit"
    HA = "HA - hold pattern term. at fix after reach. an altitude"
    HM = "HM - holding pattern terminating manually"
    IF = "IF - initial fix"
    PI = "PI - procedure turn followed by a course to a fix (CF)"
    PT = "PT - timed outbound leg to a procedure turn"
    TF = "TF - track between two fixes"
    CA = "CA - course to an altitude"
    CD = "CD - course to a DME distance"
    CI = "CI - course to next leg followed by course oriented leg"
    CR = "CR - course to a radial termination"
    CF = "CF - course to a fix"
    DF = "DF - Computed track direct to a fix"
    FA = "FA - course from a fix to an altitude"
    FC = "FC - course from a fix to a distance"
    FT = "FT - course from a fix during a specified time"
    FD = "FD - course from a fix to a DME distance"
    FM = "FM - course from a fix to a manual termination"
    RF = "RF - constant radius to a fix"
    VA = "VA - heading to an altitude (position unspecified)"
    VD = "VD - heading to a DME distance"
    VI = "VI - heading to next leg"
    VM = "VM - heading to a manual termination"
    VR = "VR - heading to a radial termination"
    OTHER = "Other"

    VariableNames = ["AF", "HF", "HA", "HM", "IF", "PI", "PT", "TF", "CA", "CD", "CI", "CR", "CF", "DF",
                     "FA", "FC", "FT", "FD", "FM", "RF", "VA", "VD", "VI", "VM", "VR", "OTHER"]
    Items = ["AF - constant DME arc to a fix", "HF - hold pattern terminating at a fix after one circuit", "HA - hold pattern term. at fix after reach. an altitude",
             "HM - holding pattern terminating manually", "IF - initial fix", "PI - procedure turn followed by a course to a fix (CF)",
             "PT - timed outbound leg to a procedure turn", "TF - track between two fixes", "CA - course to an altitude",
             "CD - course to a DME distance", "CI - course to next leg followed by course oriented leg", "CR - course to a radial termination",
             "CF - course to a fix", "DF - Computed track direct to a fix", "FA - course from a fix to an altitude",
             "FC - course from a fix to a distance", "FT - course from a fix during a specified time", "FD - course from a fix to a DME distance",
             "FM - course from a fix to a manual termination", "RF - constant radius to a fix", "VA - heading to an altitude (position unspecified)",
             "VD - heading to a DME distance", "VI - heading to next leg", "VM - heading to a manual termination",
             "VR - heading to a radial termination", "Other"]

class CodeTypeSidAixm(Enum):
    O = "Engine Out"
    C = "Conventional"
    R = "RNAV"
    F = "FMS"
    Other = "Other"

    VariableNames = ["O", "C", "R", "F", "Other"]
    Items = ["Engine Out", "Conventional", "RNAV", "FMS", "Other"]

class CodeTypeStarAixm(Enum):
    C = "Conventional"
    R = "RNAV"
    F = "FMS"
    Other = "Other"

    VariableNames = ["C", "R", "F", "Other"]
    Items = ["Conventional", "RNAV", "FMS", "Other"]

class CodeTypeIapAixm(Enum):
    B = "LLZ Backcourse"
    E = "RNAV, GPS Required"
    F = "Flight Management System (FMS)"
    G = "Instrument Guidance System (IGS)"
    H = "Helicopter to runway"
    I = "Instrument Landing System (ILS)"
    J = "LAAS-GPS/GLS"
    K = "WAAS-GPS"
    L = "Localizer Only (LOC)"
    M = "Microwave Landing System (MLS)"
    N = "NDB"
    P = "Global Positioning System (GPS)"
    R = "Area Navigation (RNAV)"
    T = "TACAN"
    U = "Simplified directional Facility (SDF)"
    V = "VOR"
    W = "MLS, Type A"
    Y = "MLS, Type B and C"
    Other = "Other"

    VariableNames = ["B", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "P", "R", "T", "U", "V", "W", "Y", "Other"]
    Items = [B, E, F, G, H, I, J, K, L, M, N, P, R, T, U, V, W, Y ,Other]
class CodeTypeDesigPtAixm(Enum):
    ICAO = "ICAO 5 letter name code designator"
    ADHP = "Aerodrome/Heliport related name code designator"
    COORD = "Point with identifier derived from its geographical coordinates"
    OTHER = "Other type of code designator"

    VariableNames = ["ICAO", "ADHP", "COORD", "OTHER"]
    Items = ["ICAO 5 letter name code designator", "Aerodrome/Heliport related name code designator",
             "Point with identifier derived from its geographical coordinates", "Other type of code designator"]
class CodeRefOchAixm(Enum):
    Nothing = ""
    ARP = "Aerodrome elevation"
    THR = "Threshold elevation"
    OTHER = "Other"

    VariableNames =["Nothing", "ARP", "THR", "OTHER"]
    Items = [Nothing, ARP, THR, OTHER]

class NavigationalAidType:
    Omnidirectional = "Omnidirectional"
    Directional = "Directional"
    LineOfSight = "LineOfSight"

    VariableNames = ["Omnidirectional", "TDirectionalER", "LineOfSight"]
    Items = [Omnidirectional, Directional, LineOfSight]
class CodeTypeHoldProcAixm(Enum):
    ENR = "En-route holding"
    TER = "Terminal area holding"
    Other = "Other"

    VariableNames = ["ENR", "TER", "Other"]
    Items = [ENR, TER, Other]
class ListInsertPosition:
    Before = "Before"
    After = "After"
    Append = "Append"

    VariableNames = ["Before", "After", "Append"]
    Items = [Before, After, Append]

class DataBaseGeoBorderType(Enum):
    ST = "State Border"
    TW = "Territorial Waters Limit"
    CS = "Coastline"
    RW = "River Centreline"
    RB = "River Bank"
    OTHER = "Other"

    VariableNames = ["ST", "TW", "CS", "RW", "RB", "OTHER"]
    Items = ["State Border", "Territorial Waters Limit", "Coastline",
             "River Centreline", "River Bank", "Other"]
class DrawingSpace:
    PaperSpace = "PaperSpace"
    ModelSpace = "ModelSpace"
    MSpace = "MSpace"

    Items = ["PaperSpace", "ModelSpace", "MSpace"]

class ProcEntityListType(Enum):
    Holding = "Holding"
    Fixes = "Fixes"
    FixesEx = "FixesEx"
    Centers = "Centers"
    CentersEx = "CentersEx"
    RecommendedNavAids = "RecommendedNavAids"
    VORs = "VORs"
    DMEs = "DMEs"
    AHPs = "AHPs"
    LocationsDPN = "LocationsDPN"

    VariableNames = ["Holding",
            "Fixes",
            "FixesEx",
            "Centers",
            "CentersEx",
            "RecommendedNavAids",
            "VORs",
            "DMEs",
            "AHPs",
            "LocationsDPN"]
    Items = [Holding,
            Fixes,
            FixesEx,
            Centers,
            CentersEx,
            RecommendedNavAids,
            VORs,
            DMEs,
            AHPs,
            LocationsDPN]


class CodePhaseProcAixm(Enum):
    Nothing = ""
    X0 = "Engine out(SID)"
    X1 = "Runway transition (SID) or en-route transition (STAR)"
    X2 = "Common route"
    X3 = "En-route transition (SID) or runway transition (STAR)"
    X4 = "RNAV runway transition (SID) or en-route transition (STAR)"
    X5 = "RNAV Common route"
    X6 = "RNAV en-route transition (SID) or runway transition (STAR)"
    X7 = "Profile descent en-route transition"
    X8 = "Profile descent common route"
    X9 = "Profile descent runway transition"
    F = "FMS runway transition (SID) or en-route transition (STAR)"
    M = "FMS common route"
    S = "FMS en-route transition (SID) or runway transition (STAR)"
    T = "Vector runway transition (SID)"
    V = "Vector en-route transition (SID)"
    A = "Approach transition (IAP)"
    Z = "Missed approach (IAP)"
    P = "Primary Missed Approach"
    R = "Secondary Missed Approach"
    OTHER = "Other"

    VariableNames = ["Nothing", "X0", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "F", "M", "S", "T", "V", "A", "Z", "P", "R", "OTHER"]
    Items = [Nothing, X0, X1, X2, X3, X4, X5, X6, X7, X8, X9, F, M, S, T, V, A, Z, P, R, OTHER]

class CodeTypeCourseAixm(Enum):
    Nothing = ""
    TT = "True Track"
    MT = "Magnetic Track"
    TBRG = "True bearing"
    MBRG = "Magnetic bearing"
    HDG = "Heading"
    RAD = "VOR radial"
    OTHER = "Other"

    VariableNames = ["Nothing", "TT", "MT", "TBRG", "MBRG", "HDG", "RAD", "OTHER"]
    Items = [Nothing, TT, MT, TBRG, MBRG, HDG, RAD, OTHER]

class CodeDirTurnAixm(Enum):
    Nothing = ""
    L = "Left"
    R = "Right"
    E = "Either left or right"

    VariableNames = ["Nothing", "L", "R", "E"]
    Items = [Nothing, L, R, E]

class CodeTypeFlyByAixm(Enum):
    Nothing = ""
    Y = "Yes"
    N = "No"

    VariableNames = ["Nothing", "Y", "N"]
    Items = [Nothing, Y, N]

class CodeDescrDistVerAixm(Enum):
    Nothing = ""
    LA = "At or above the lower altitude"
    BH = "At or below the higher altitude"
    L = "At the lower altitude"
    B = "Between the lower and the upper altitudes"
    OTHER = "Other"

    VariableNames = ["Nothing", "LA", "BH", "L", "B", "OTHER"]
    Items = [Nothing, LA, BH, L, B, OTHER]

class CodeDistVerAixm(Enum):
    Nothing = ""
    HEI = "The distance measured from GND"
    ALT = "The distance measured from MSL"
    W84 = "The distance measured from WGS-84 ellipsoid"
    QFE = "A reading of 0 on the altimeter setting which occurs on GND"
    QNH = "Altimeter setting gives field elevation on GND (~ 0 at MSL)"
    STD = "The altimeter setting is set to standard atmosphere"
    OTHER= "Other"

    VariableNames = ["Nothing", "HEI", "ALT", "W84", "QFE", "QNH", "STD", "OTHER"]
    Items = [Nothing, HEI, ALT, W84, QFE, QNH, STD, OTHER]

class CodeSpeedRefAixm(Enum):
    Nothing = ""
    IAS = "Indicated air speed"
    TAS = "True air speed"
    GS = "Ground speed"
    OTHER = "Other"

    VariableNames = ["Nothing", "IAS", "TAS", "GS", "OTHER"]
    Items = [Nothing, IAS, TAS, GS, OTHER]

class CodeRepAtcAixm(Enum):
    Nothing = ""
    C = "Compulsory"
    R = "On Request"
    N = "No Report"
    Other = "Other"

    VariableNames = ["Nothing", "C", "R", "N", "Other"]
    Items = [Nothing, C, R, N, Other]

class CodeIapFixAixm(Enum):
    Nothing = ""
    IAF = "Initial Approach Fix"
    IF = "Intermediate Approach Fix"
    FAF = "Final Approach Fix"
    MAPT = "Missed Approach Point"
    OTHER = "Other"

    VariableNames = ["Nothing", "IAF", "IF", "FAF", "MAPT", "OTHER"]
    Items = [Nothing, IAF, IF, FAF, MAPT, OTHER]

class CodeLegTypeAixm(Enum):
    Nothing = ""
    GRC = "Great Circle"
    CCA = "Counter Clockwise Arc"
    CWA = "Clockwise Arc"

    VariableNames = ["Nothing", "GRC", "CCA", "CWA"]
    Items = [Nothing, GRC, CCA, CWA]
class CodeCatIlsAixm:
    # [Description("CAT I")]
    I = "CAT I"
    # [Description("CAT II")]
    II = "CAT II"
    # [Description("CAT III")]
    III = "CAT III"
    # [Description("CAT III A")]
    IIIA = "CAT III A"
    # [Description("CAT III B")]
    IIIB = "CAT III B"
    # [Description("CAT III C")]
    IIIC = "CAT III C"
    # [Description("No category")]
    NOCAT = "No category"

    VariableNames = ["I", "II", "III", "IIIA", "IIIB", "IIIC", "NOCAT"]
    Items = [I, II, III, IIIA, IIIB, IIIC, NOCAT]
class CodePathTypeAixm(Enum):
    Nothing = ""
    NRM = "Normal"
    MAP = "Missed Approach"

    VariableNames = ["Nothing", "NRM", "MAP"]
    Items = [Nothing, NRM, MAP]
class Formating:
    BELOW = "Below"
    BOOLEAN_Y_N = "Y|N"
    BOOLEAN_YES_NO = "Yes|No"
    DIFFERENCE = "Difference {0}"
    LINE_WEIGHT = "0.00 mm"
    MOC_MULTIPLIER = "0.# x"
    OBSTACLE_FORMAT = "Name: {0}, Position: {1:0.##},{2:0.##},{3:0.##}, Tolerance: {4}, Trees: {5}, Type: {6}"

class Point3dCollection(list):
    def __init__(self, point3dCollection = None):
        list.__init__(self)
        if point3dCollection != None:
            self.extend(point3dCollection)
        pass
    def Add(self, point3d_0):
        self.append(point3d_0)
        return self.get_Count() - 1
    def Insert(self, index, point3d):
        self.insert(index, point3d)
    def appendList(self, point3dCollection):
        self.extend(point3dCollection)
    def set_Item(self, i, point3d):
        self.pop(i)
        self.insert(i, point3d)
    def RemoveAt(self, index):
        self.pop(index)
    def get_Item(self, i):
        pt = self[i]
        if not isinstance(pt, Point3D):
            return Point3D(pt.x(), pt.y())
        return self[i]
    def get_Count(self):
        return len(self)
    def smethod_144(self, point3dCollection):
        self.extend(point3dCollection)
    def smethod_145(self, point3dArray):
        self.extend(point3dArray)

    @staticmethod
    def smethod_146(point3dCollection_0):
        point3d = None;
        num = 0;
        i = point3dCollection_0.get_Count()
        while num < i:
            i = point3dCollection_0.get_Count()
        # for (int i = point3dCollection_0.get_Count(); num < i; i = point3dCollection_0.get_Count())
            if (i < 2):
                return point3dCollection_0;
            point3d = point3dCollection_0.get_Item(num + 1) if(num != i - 1) else point3dCollection_0.get_Item(0);
            if (not point3dCollection_0.get_Item(num).smethod_170(point3d)):
                num += 1;
            else:
                point3dCollection_0.RemoveAt(num);
        return point3dCollection_0;
    @staticmethod
    def smethod_147(point3dCollection_0, bool_0):
#         Point3d item;
        num = 0;
        item = None
        i = len(point3dCollection_0)
        aa= []
        while num < i:
            if (i < 2):
                return point3dCollection_0
            if (num != i - 1):
                item = point3dCollection_0[num + 1]
            else:
                if (bool_0):
                    return point3dCollection_0
                item = point3dCollection_0[0]
            if (not point3dCollection_0[num].smethod_170(item)):
                num += 1
            else:
                point3dCollection_0.remove(point3dCollection_0[num]);
                i -= 1
                aa.append(num)
#         for index in aa:
#             point3dCollection_0.remove(point3dCollection_0[index])
        return point3dCollection_0

    def smethod_153(self):
        point3dCollection = Point3dCollection()
        for i in range(self.get_Count()):
            point3dCollection.Add(self.get_Item(i))
        return point3dCollection

class Matrix3d:
    def __init__(self):
        pass
    @staticmethod
    def Displacement(vector3d):  
        direction = [vector3d.x, vector3d.y, vector3d.z]    
        M = numpy.identity(4)
        M[:3, 3] = direction[:3]
        return M

    @staticmethod
    def Rotation(angle, vector3d, point3d=None):
        direction = [vector3d.x, vector3d.y, vector3d.z]
        sina = math.sin(angle)
        cosa = math.cos(angle)
        direction = unit_vector(direction[:3])
        # rotation matrix around unit vector
        R = numpy.diag([cosa, cosa, cosa])
        R += numpy.outer(direction, direction) * (1.0 - cosa)
        direction *= sina
        R += numpy.array([[ 0.0,         -direction[2],  direction[1]],
                          [ direction[2], 0.0,          -direction[0]],
                          [-direction[1], direction[0],  0.0]])
        M = numpy.identity(4)
        M[:3, :3] = R
        if point3d != None:
            point = [point3d.get_X(), point3d.get_Y(), point3d.get_Z()]
            # rotation not around origin
            point = numpy.array(point[:3], dtype=numpy.float64, copy=False)
            M[:3, 3] = point - numpy.dot(R, point)
        return M
    
    @staticmethod
    def Mirroring( point3d, point3d1, point3d2):
        point = [point3d.get_X(), point3d.get_Y(), point3d.get_Z()]
        normal = vector_product([point3d1.get_X() - point3d.get_X(), point3d1.get_Y() - point3d.get_Y(), point3d1.get_Z() - point3d.get_Z()], [point3d2.get_X() - point3d.get_X(), point3d2.get_Y() - point3d.get_Y(), point3d2.get_Z() - point3d.get_Z()])
        normal = unit_vector(normal[:3])
        M = numpy.identity(4)
        M[:3, :3] -= 2.0 * numpy.outer(normal, normal)
        M[:3, 3] = (2.0 * numpy.dot(point[:3], normal)) * normal
        return M
    @staticmethod
    def Inverse(matrix):
        return numpy.linalg.inv(matrix)
    
    @staticmethod
    def MirroringFromVector3d(point3d, vector3d):
        """Return matrix to mirror at plane defined by point and normal vector.
    
        >>> v0 = numpy.random.random(4) - 0.5
        >>> v0[3] = 1.
        >>> v1 = numpy.random.random(3) - 0.5
        >>> R = reflection_matrix(v0, v1)
        >>> numpy.allclose(2, numpy.trace(R))
        True
        >>> numpy.allclose(v0, numpy.dot(R, v0))
        True
        >>> v2 = v0.copy()
        >>> v2[:3] += v1
        >>> v3 = v0.copy()
        >>> v2[:3] -= v1
        >>> numpy.allclose(v2, numpy.dot(R, v3))
        True
    
        """
        normal = [vector3d.x, vector3d.y, vector3d.z]
        point = [point3d.get_X(), point3d.get_Y(), point3d.get_Z(), 0]
        normal = unit_vector(normal[:3])
        M = numpy.identity(4)
        M[:3, :3] -= 2.0 * numpy.outer(normal, normal)
        M[:3, 3] = (2.0 * numpy.dot(point[:3], normal)) * normal
        return M    

class Vector3d:
    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        self.x = x
        self.y = y
        self.z = z

    

class Point3D(QgsPoint):
#     def __init__(self, qgsPoint):
#         QgsPoint.__init__(qgsPoint)
#         self.z = 0.0
        
    def __init__(self, x = 0.0, y = 0.0, z = 0.0, qgsPoint = None, id = ""):
        if qgsPoint is None:
            QgsPoint.__init__(self, x, y)
        else:
            QgsPoint.__init__(qgsPoint)
        self.zVal = z
        self.ID = id
    def PutCoords(self, xVal, yVal, zVal = 0.0):
        self.setX(xVal)
        self.setY(yVal)
        self.zVal = zVal
    def ToString(self):
        if self.get_Z() == 0:
            return "(%s, %s)"%(str(self.get_X()), str(self.get_Y()))
        else:
            return "(%s, %s) z = %s"%(str(self.get_X()), str(self.get_Y()), self.get_Z())
    def get_X(self):
        return self.x()
    
    def get_Y(self):
        return self.y()
    
    def get_Z(self):
        return self.z()
    
    def SetZ(self, zValue):
        self.zVal = zValue
        
    def z(self):
        return self.zVal
    
#     def SetX(self, xValue):
#         self.xVal = xValue
#         
#     def x(self):
#         return self.xVal
#     
#     def SetY(self, yValue):
#         self.yVal = yValue
#         
#     def y(self):
#         return self.yVal
    
    # Point3D MultiBy(double )
    def smethod_167(self, multiplor):
#         multiplorResult = define._qgsDistanceArea.convertMeasurement(multiplor, QGis.Meters, define._canvas.mapUnits(), False)
        return Point3D(self.x() , self.y() , multiplor)
    
    # public bool IsEqualTo(Autodesk.AutoCAD.Geometry.Point3d point)
    def smethod_170(self, other):
        if self.x() != other.x():
            return False
        else:
            if self.y() != other.y():
                return False
            else:
                if self.zVal != other.z():
                    return False
                else:
                    return True                

    def smethod_171(self, other, double_0):
        if math.fabs(self.x() - other.x()) > double_0:
            return False
        else:
            if math.fabs(self.y() - other.y()) > double_0:
                return False
            else:
                if math.fabs(self.zVal - other.z()) > double_0:
                    return False
                else:
                    return True                
    
    
    def smethod_176(self):
        return Point3D(self.get_X(), self.get_Y());    

    @staticmethod
    def get_Origin():
        return Point3D(0,0,0)
    
    def TransformBy(self, matrix3d):
        pointMatrix = [self.x(), self.y(), self.z(), 1]
        resultMatrix = []
        for matrix in matrix3d:
            matrix = numpy.multiply(matrix, pointMatrix)
            value = 0.0
            for num in matrix:
                value += num
            resultMatrix.append(value)
        return Point3D(resultMatrix[0], resultMatrix[1], resultMatrix[2])
    def GetVectorTo(self, other):
        return Vector3d(other.x() - self.x(), other.y() - self.y(), other.z() - self.z())

    def set_X(self, xVal):
        self.setX(xVal)
    def set_Y(self, yVal):
        self.setY(yVal)
    X = property(get_X, set_X, None, None)
    Y = property(get_Y, set_Y, None, None)
    
class OCAHType:
    OCA = "OCA"
    OCH = "OCH"
    
class RnpArCalculatedLegType:
    STRAIGHT = "Straight"
    RF = "RF"
    TF = "TF"

class RnpArSegmentType:
    Initial = "Initial Approach"
    Intermediate = "Intermediate Approach"
    Final = "Final Approach"
    Missed = "Missed Approach"

class RnpArLegType:
    RF = "RF"
    TF = "TF"

class PinsSurfaceType:
    PinsSurfaceType_OIS = "PinsOIS"
    PinsSurfaceType_LevelOIS = "Level OIS"
    PinsSurfaceType_OCS = "PinsOCS"
    PinsSurfaceType_LevelOCS = "Level OCS"
class ObstacleEvaluationMode:
    Single = 0
    Multiple = 1

    VariableNames = ["Single", "Multiple"]
    Items = ["Single", "Multiple"]
class ObstacleType:
    Circle = "Circle"
    Node = "Node"
    Contour = "Contour"
    Terrain = "Terrain"
    Position = "Position"
class ProtectionAreaType:
    Primary = 0
    Secondary = 1
    PrimaryAndSecondary = 2
    Complex = 3
# class VssApproachType:
#     NonPrecision = "NonPrecision"
#     RwyAlignedPrecision
# }
# 
# private enum VssRunwayCode
# {
#     Code12,
#     Code34
# }

# class PinsAppSurfaceType:
#     pass
    
class SurfaceTypes:
    AerodromeSurfaces = "Aerodrome Surfaces Analyser"
    HeliportSurfaces = "Heliport Surfaces Analyser"
    BaroVNAV = "Baro-VNav Surface"
    BasicGNSS = "NON-Precision with T- or Y-Bar"
    IlsOas = "Obstacle Assesment Surfaces(ILS OAS)"
    SbasOas = "Obstacle Assesment Surfaces(SBAS OAS)"
    Obstacles = "Obstacle Layers"
    RnpAR = "RnpAR Surfaces"
    PinSVisualSegmentDep = "PinS Visual Segment Departure"
    PinSVisualSegmentApp = "PinS Visual Segment Approach"
    VisualSegmentSurface = "Visual Segment Surface"
    DEM = "DEM"
    DepartureRnav = "RNAV Departure Protection Area"
    DepartureStandard = "Standard Departure Protection Area"
    DepartureOmnidirectional = "Omnidirectional Departure Obstacle Analyser"
    ApproachAlignment = "Approach Alignment Construction"
    BaseTurnTC = "Base Turn Template Construction"
    CRM = "Collision Risk Model(CRM) Obstacle File Creation"
    DepartureNominal = "Departure Average Flight Path"
    TaaCalculation = "Terminal Arrival Altitudes(TAA)"
    DmeTolerance = "DME Tolerance and Slant Range"
    DmeUpdateArea = "DME Update Area Construction"

    RnavVorDme = "RNAV Protection Area (VOR-DME)"
    RnavDmeDme = "RNAV Protection Area (DME-DME)"
    HoldingRnav = "RNAV Holding"
    HoldingRace_P = "Holding Pattern Template Construction"
    HoldingOverHead = "Over-head Holding-Racetrack"
    HoldingVorDme = "VOR - DME Holding - Racetrack"
    HoldingRnp = "RNP Holding"
    VisualCircling = "Visual Circling"
    MSA = "Minimum Sector Altitudes (MSA)"
    DataImport = "Database Import"
    EnrouteStraight = "En-route Straight Segment"
    EnrouteTurnOverHead = "En-route Turn Over-head a Facility"
    RnavStraightSegmentAnalyser = "RNAV (GNSS En-route-STAR) Straight Segment Analyser"
    RnavTurningSegmentAnalyser = "RNAV (GNSS En-route-STAR) Turning Segment Analyser"
    Radial = "Radial Tolerance Construction for VOR or NDB"
    IlsBasic = "ILS Basic Surfaces"
    IasToTas = "True Air Speed (TAS) Calculation"
    TurnArea = "Turn Protection Area Construction"
    OverheadTolerance = "Over-head Tolerance Construction"
    FixConstruction = "Fix Construction"
    FixToleranceArea = "Tolerance area"

    ObstacleEvaluator = "Obstacle evaluator"
    StepDownObstacleAnalyser = "15% Area Obstacle Analyser"

    RnavNominal = "RNAV Minimum Stabilisation Track Construction"
    SecondaryMoc = "Secondary MOC Calculation"
    TurnAreaObstacleAnalyser = "Turn Area Obstacle Analyser"
    StepDownObstacleAnalyser0 = "15% Area Obstacle Analyser"
    StepDownObstacleAnalyser = "Step Down Obstacle Analyser"
    InitialMissedApproachObstacleAnalyser = "Initial Missed Approach Obstacle Analyser"
    MountainousTerrainAnalyser = "Mountainous Terrain Analyser"
    ObstacleEvaluator = "Obstacle Evaluator"

    GeoDeterminePosition = "Position"
    GeoDetermineBD = "Bearing and Distance"
    GeoDetermineMV = "Theoretical Magnetic Variation"
    GeoDetermine = "Geo Tools"

    PathTerminators = "Path Terminators"
    FasDataBlock = "SBAS FAS Data Block (Import-Export)"
    ProcedureExport = "Procedure Export"
    ProfileManager = "Profile Manager"
    DataExport = "Database Export"

    ApproachSegment = "Approach Segment"
    MASegment = "Missed Approach Segment"

    RaceTrackNavAid = "RaceTrack over NAVAID"
    RaceTrackFix = "RaceTrack based on Fix"
    Holding = "Holding"

    ChartingGrid = "Charting Grid"
    ChartingTemplates = "Charting Templates"

    PaIls = "PA-ILS"
    PaGbas = "PA-GBAS"
    BARO_VNAV = "BARO-VNAV"
    SBAS = "SBAS"
    NpaOnFix = "NPA On-FIX"
    NpaOverheadingNavaid = "NPA-Overheading a NAVAID"
    NpaAtDistanceTime = "NPA-At Distance/Time"

    Shielding = "Theoretical Shielding"

    TurnProtectionAndObstacleAssessment = "Turn Protection And Obstacle Assessment"

class DataBaseFileDelimiter:
    Semicolon = "Semicolon"
    Comma = "Comma"
    Space = "Space"
    Custom = "Custom"

class EnumsType:
    ChartingGridLinesType_FullArcs = "Full Arcs"
    ChartingGridLinesType_Ticks = "Ticks"
    ChartingGridLinesType_None = "None"
class FasDbOperationType:
    StraightInOffset = "StraightInOffset"
    spare1 = "spare1"
    spare2 = "spare2"
    spare3 = "spare3"
    spare4 = "spare4"
    spare5 = "spare5"
    spare6 = "spare6"
    spare7 = "spare7"
    spare8 = "spare8"
    spare9 = "spare9"
    spare10 = "spare10"
    spare11 = "spare11"
    spare12 = "spare12"
    spare13 = "spare13"
    spare14 = "spare14"
    spare15 = "spare15"

class FasDbSbasServiceProvider:
    WAAS = "WAAS"
    EGNOS = "EGNOS"
    MSAS = "MSAS"
    GAGAN = "GAGAN"
    SDCM = "SDCM",
    spare5 = "spare5"
    spare6 = "spare6"
    spare7 = "spare7"
    spare8 = "spare8"
    spare9 = "spare9"
    spare10 = "spare10"
    spare11 = "spare11"
    spare12 = "spare12"
    spare13 = "spare13"
    GBASonly = "GBASonly"
    AnySBASprovider = "AnySBASprovider"



class FasDbRunwayLetter:
    Nothing = "None"
    R = "R"
    C = "C"
    L = "L"

class FasDbApproachPerformanceDesignator:
    APV = "APV"
    Cat1 = "Cat1"
    Cat2 = "Cat2"
    Cat3 = "Cat3"
    spare4 = "spare4"
    spare5 = "spare5"
    spare6 = "spare6"
    spare7 = "spare7"
class PositionType:
    CWY = 1
    SWY = 2
    THR = 3
    END = 4
    Position = 5
    START = 6

    VariableNames = ["CWY", "SWY", "THR", "END", "Position", "START"]
    Items = [CWY, SWY, THR, END, Position, START]
class FasDbApproachTchUnits:
    ft = 0#"ft"
    m = 1#"m"
class ProcedureType:
    pass
class MagneticModel:
    WMM2015 = 0
    WMM2010 = 1#"WMM2010"
    WMM2005 = 2#"WMM2005"
    WMM2000 = 3#"WMM2000"
    WMM95 = 4#"WMM95"
    WMM90 = 5#"WMM90"
    WMM85 = 6#"WMM85"
    IGRF2000 = 7#"IGRF2000"
    IGRF95 = 8#"IGRF95"
    IGRF90 = 9#"IGRF90"

class IlsCrmYesNoType:
    Yes = "Yes"
    No = "No"
    
class IlsCrmCategoryType:
    Cat1 = "CAT I"
    Cat2 = "CAT II"
    Cat1RA = "CAT I (Radio Altimeter Only)"
    Cat2AP = "CAT II (Autopilot Only)"
    
class IlsCrmMinimumType:
    OCA = "OCA (Above Mean Sea Level)"
    OCH = "OCH (Above THR)"

class IlsCrmRiskType:
    Highest = "Highest Risk"
    HigherThan = "Risk Higher Than 0.0000000001"
    All = "All Obstacles"

class SelectionModeType:
    Automatic = "Automatic"
    Manual = "Manual"
class StandardDepartureType:
    Straight = "Straight"
    WithTrackAdjustment = "With Track Adjustment"
    VOR = "VOR"
    NDB = "NDB"
class SpeedUnits:
    KTS = 0
    KMH = 1

    @staticmethod
    def ToString(unit):
        if unit == SpeedUnits.KTS:
            return "kts"
        elif unit == SpeedUnits.KMH:
            return "kmh"
        else:
            return ""
class AltitudeUnits:
    M = 0
    FT = 1
    FL = 2
    SM = 3

    @staticmethod
    def ToString(unit):
        if unit == AltitudeUnits.M:
            return "m"
        elif unit == AltitudeUnits.FT:
            return "ft"
        elif unit == AltitudeUnits.FL:
            return "fl"
        elif unit == AltitudeUnits.SM:
            return "sm"
        else:
            return ""
class DistanceUnits:
    M = 0
    FT = 1
    KM = 2
    NM = 3
    MM = 4

    @staticmethod
    def ToString(unit):
        if unit == DistanceUnits.M:
            return "m"
        elif unit == DistanceUnits.FT:
            return "ft"
        elif unit == DistanceUnits.KM:
            return "km"
        elif unit == DistanceUnits.NM:
            return "nm"
        elif unit == DistanceUnits.MM:
            return "mm"
        else:
            return ""
        
class AircraftSpeedCategory:
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    H = 5
    Custom = 6
    
class WindType:
    ICAO = "ICAO"
    UK = "UK"
    Custom = "Custom"

class ObstacleAreaResult:
    Primary = "Primary"
    Secondary = "Secondary"
    Outside = "Outside"
    
class CriticalObstacleType:
    Yes = "Yes"
    No = "No"
class CloseInObstacleType:
    Yes = "Yes"
    No = "No"
class DisregardableObstacleType:
    Yes = "Yes"
    No = "No"
    
class RnavSegmentType:
    MissedApproach = 'Missed Approach'
    FinalApproach = 'Final Approach'
    Intermediate = 'Intermediate'
    Initial1 = 'Initial 1'
    Initial2 = 'Initial 2'
    Initial3 = 'Initial 3'

    Items = ['Missed Approach', 'Final Approach', 'Intermediate', 'Initial 1', 'Initial 2', 'Initial 3']

class OrientationType:
    Left = "Left"
    Right = "Right"
    
       
class OasSurface:
    OFZ = "Oas Ofz"
    W = "Oas W"
    WS = "Oas W*/W'"
    Z = "Oas Z"
    X1 = "Oas X1"
    X2 = "Oas X2"
    Y1 = "Oas Y1"
    Y2 = "Oas Y2"

class OasCategory:
    ILS1 = "ILS CAT |"
    ILS2 = "ILS CAT ||"
    ILS2AP = "ILS CAT || (Autopilot Only)"
    SBAS_APV1 = "SBAS APV |"
    SBAS_APV2 = "SBAS APV ||"
    SBAS_CAT1 = "SBAS Category |"

class OasMaEvaluationMethod:
    Standard = "Standard"
    Alternative = "Alternative"

class OffsetGapType:
    Extend = "Extend"
    Fillet = "Fillet"
    Chamfer = "Chamfer"

class IlsOasMaEvaluationMethod:
    Standard = "Standard"
    GP = "GP"
    VPA = "VPA"

class MissedApproachClimbGradient:
    MACG5 = 0
    MACG4 = 1
    MACG3 = 2
    MACG2_5 = 3
    MACG2 = 4

class AircraftSize:
    Standard = "Standard"
    Large = "Large"

class ConstructionType:
    Construct2D = "2D"
    Construct3D = "3D"

class RnavCommonWaypoint:    
    MAHWP = 0
    MAWP = 1
    FAWP = 2
    IWP = 3
    IAWP1 = 4
    IAWP2 = 5
    IAWP3 = 6
#     @staticmethod
#     def toString(rnavSegmentType):
#         if rnavSegmentType == RnavSegmentType.MissedApproach:
#             return "MissedApproach"
#         elif rnavSegmentType == RnavSegmentType.FinalApproach:
#             return "FinalApproach"
#         elif rnavSegmentType == RnavSegmentType.Intermediate:
#             return "Intermediate"
#         elif rnavSegmentType == RnavSegmentType.Initial1:
#             return "Initial1"
#         elif rnavSegmentType == RnavSegmentType.Initial2:
#             return "Initial2"
#         elif rnavSegmentType == RnavSegmentType.Initial3:
#             return "Initial3"
class RnavFlightPhase:
    Enroute = 0
    SID = 1
    STAR = 2
    IafIf = 3
    Faf = 4
    MissedApproach = 5
        
class RnavGnssFlightPhase:
    Enroute = 0
    StarSid = 1
    Star30Sid30IfIafMa30 = 2
    Sid15 = 3
    Ma15 = 4
    Faf = 5
    Mapt = 6

class RnavSpecification:
    Rnav5 = "Rnav5"
    Rnav2 = "Rnav2"
    Rnav1 = "Rnav1"
    Rnp4 = "Rnp4"
    Rnp2 = "Rnp2"
    Rnp1 = "Rnp1"
    ARnp2 = "ARnp2"
    ARnp1 = "ARnp1"
    ARnp09 = "ARnp09"
    ARnp08 = "ARnp08"
    ARnp07 = "ARnp07"
    ARnp06 = "ARnp06"
    ARnp05 = "ARnp05"
    ARnp04 = "ARnp04"
    ARnp03 = "ARnp03"
    RnpApch = "RnpApch"
class RnavVorDmeFlightPhase:
    Enroute = "En-route"
class RnavDmeDmeFlightPhase:
    EnrouteStarSid = 0
    Star30Sid30IfIaf = 1
    Sid15 = 2
    Faf = 3
class RnavDmeDmeCriteria:
    Two = 0
    MoreThanTwo = 1

class TurnDirection:
    Right = -1
    Nothing = 0
    Left = 1

class AngleUnits:
    Degrees = 0
    Radians = 1
class Formats:
    DurationFormat = "0.##";
    DistanceFormat = "0.##";
    AltitudeFormat = "0.##";
    SpeedFormat = "0.#";
    AngleFormat = "0.##";
    GradientFormat = "0.##";
    SlopeFormat = "0.##";
    TrackFormat = "000.##";
    GridXYFormat = "0.0000";
    NumberFormat = "0.##";
    DegreesFormat = "ddd" + define._degreeStr + "mm'ss.ssss\"";
    LatitudeFormat = "dd" + define._degreeStr + "mm'ss.ssss\"h";
    LongitudeFormat = "ddd" + define._degreeStr + "mm'ss.ssss\"h";
    VariationFormat = "d.dddd" + define._degreeStr + "h";
    # booleanFormat = Formating.BOOLEAN_YES_NO;
    MapScale = "#,0";
class AngleGradientSlopeUnits:
    Degrees = 0
    Percent = 1
    Slope = 2

    @staticmethod
    def ToString(unit):
        if unit == AngleGradientSlopeUnits.Degrees:
            return define._degreeStr
        elif unit == AngleGradientSlopeUnits.Percent:
            return "%"
        elif unit == AngleGradientSlopeUnits.Slope:
            return "1:"
        else:
            return ""
class Enums:
    AngleGradientSlopeUnits_Slope = "1:"
    AngleGradientSlopeUnits_Slope_1 = "1/"
    AngleGradientSlopeUnits_Percent = "%"
    AngleGradientSlopeUnits_Degrees = define._degreeStr
    AngleGradientSlopeUnits_Degrees_1 = "D"

class IntersectionStatus:
    Nothing = "None"
    Tangent = "Tangent"
    Intersection = "Intersection"
    
class RnavWaypointType:
    FlyBy = 0
    FlyOver = 1
    RF = 2

class ObstacleTableColumnType:
    ObjectId = "ObjectId"
    LayerId = "LayerId"
    Name = "Name"
    X = "X"
    Y = "Y"
    Lat = "Lat"
    Lon = "Lon"
    AltM = "Alt.(m)" 
    AltFt = "Alt.(ft)" 
    TreesM = "Obstacle Vertical Tolerance(m)" 
    TreesFt = 'Obstacle Vertical Tolerance(ft)'
    OcaM = 'Oca(m)'
    OcaFt = 'Oca(ft)'
    OchM = 'Och(m)'
    OchFt = 'Och(ft)'
    ObstArea = 'Obstacle Area'
    DistInSecM = 'DistIn.(m)'
    DsocM = "Dsoc(m)"
    MocMultiplier = 'MocMultiplier'
    MocAppliedM = 'MocApplied(m)'
    MocAppliedFt = 'MocApplied(ft)'
    MocReqM = 'MocReq(m)'
    MocReqFt = 'MocReq(ft)'
    DzM = 'DzM'
    DrM = 'DrM'
    DoM = 'DoM'
    DxM = 'DxM'
    HeightLossM = 'HeightLoss(m)'
    HeightLossFt = 'HeightLoss(ft)'
    AcAltM = 'AcAlt(M)'
    AcAltFt = 'AcAlt(ft)'
    AltReqM = 'AltReq(m)'
    AltReqFt = 'AltReq(ft)'
    Critical = 'Critical'
    MACG = 'MACG'
    PDG = 'PDG'
    SurfAltM = 'SurfAltM'
    SurfAltFt = 'SurfAltFt'
    DifferenceM = 'DifferenceM'
    DifferenceFt = 'DifferenceFt'
    IlsX = 'IlsX'
    IlsY = 'IlsY'
    EqAltM = 'EqAltM'
    EqAltFt = 'EqAltFt'
    SurfaceName = 'SurfaceName'
    Disregardable = 'Disregardable'
    CloseIn = 'CloseIn'
    Variation = 'Variation'
    Tag = 'Tag'
    Surface = 'Surface'
    Area = 'Area'
    HLAppliedM = 'HL applied(m)'
class DataBaseCoordinateType:
#     [Description("Point")]
    Point = "Point"
#     [Description("Arc Point")]
    ArcPoint = "Arc Point"
#     [Description("Middle Arc Point")]
    MidPoint = "Middle Arc Point"
#     [Description("Circle")]
    CenPoint = "Circle"
#     [Description("Line")]
    GRC = "Line"
#     [Description("Counter Clockwise Arc")]
    CCA = "Counter Clockwise Arc"
#     [Description("Clockwise Arc")]
    CWA = "Clockwise Arc"
#     [Description("Geographic Border")]
    FNT = "Geographic Border"
class PinsVisualSegmentType: 
    Direct = "Direct"
    Manoeuvring = "Manoeuvring"
    
class PinsOperationType:
    DayOnly = "Day-only Operations"
    DayNight = "Day & Night Operations" 

class MCAHType:
    MCA = "MCA"
    MCH = "MCH"   
class DmeToleranceCalculationType:
    Ground = "Ground"
    Aircraft = "Aircraft"
class DmeToleranceConstructionType:
    Circle = "DME Distance"
    Arc = "Trim on Radial"
class GeoCalculationType:
    GreatCircle = "GreatCircle"
    Ellipsoid = "Ellipsoid"    
class DegreesType:
    Degrees = "Degrees"
    Latitude = "Latitude"
    Longitude = "Longitude"
    Variation = "Variation"
class ProcEntityParseNodeType:
    Node = "Node"
    UidNode = "UidNode"

    Items = ["Node", "UidNode"]
class SymbolType:
#     [Description("Default")]
    Default = "Default"
#     [Description("Civil land")]
    Ad1 = "Civil land"
#     [Description("Civil water")]
    Ad2 = "Civil water"
#     [Description("Military land")]
    Ad3 = "Military land"
#     [Description("Military water")]
    Ad4 = "Military water"
#     [Description("Civil/Military land")]
    Ad5 = "Civil/Military land"
#     [Description("Civil/Military water")]
    Ad6 = "Civil/Military water"
#     [Description("Emergency aerodrome")]
    Ad7 = "Emergency aerodrome"
#     [Description("Sheltered anchorage")]
    Ad8 = "Sheltered anchorage"
#     [Description("Aerodrome")]
    Ad9 = "Aerodrome"
#     [Description("Heliport")]
    Ad10 = "Heliport"
#     [Description("Aerodrome reference point")]
    Arp = "Aerodrome reference point"
#     [Description("Arrow")]
    Arr = "Arrow"
#     [Description("Elliptical radio marker beacon")]
    Be1 = "Elliptical radio marker beacon"
#     [Description("Bone shape radio marker beacon")]
    Be2 = "Bone shape radio marker beacon"
#     [Description("Navigational aid box 1")]
    Box1 = "Navigational aid box 1"
#     [Description("Navigational aid box 2")]
    Box2 = "Navigational aid box 2"
#     [Description("Navigational aid box 3")]
    Box3 = "Navigational aid box 3"
#     [Description("Navigational aid box 4")]
    Box4 = "Navigational aid box 4"
#     [Description("Bearing and distance")]
    Brg = "Bearing and distance"
#     [Description("Bearing and distance (one way)")]
    Brg1 = "Bearing and distance (one way)"
#     [Description("Church")]
    Church = "Church"
#     [Description("DME")]
    Dme = "DME"
#     [Description("DME")]
    Dme_P = "DME"
#     [Description("Localizer")]
    Loc = "Localizer"
#     [Description("Final approach fix (FAF)")]
    Faf = "Final approach fix (FAF)"
#     [Description("Fly-By WPT")]
    Flyb = "Fly-By WPT"
#     [Description("Fly-Over WPT")]
    Flyo = "Fly-Over WPT"
#     [Description("Glider activity")]
    Gld = "Glider activity"
#     [Description("Basic radio navigation aid")]
    Gp = "Basic radio navigation aid"
#     [Description("Helicopter activity")]
    Hel = "Helicopter activity"
#     [Description("ILS")]
    Ils = "ILS"
#     [Description("3D Obstacle")]
    Imp0 = "3D Obstacle"
#     [Description("Insertion 1")]
    Imp1 = "Insertion 1"
#     [Description("Insertion 2")]
    Imp2 = "Insertion 2"
#     [Description("Insertion 3")]
    Imp3 = "Insertion 3"
#     [Description("Insertion 4")]
    Imp4 = "Insertion 4"
#     [Description("Locator beacon")]
    Lmm = "Locator beacon"
#     [Description("ATS/MET compulsory reporting point")]
    Mrp1 = "ATS/MET compulsory reporting point"
#     [Description("ATS/MET on request reporting point")]
    Mrp2 = "ATS/MET on request reporting point"
#     [Description("MSA box")]
    Msab = "MSA box"
#     [Description("MSA arrow")]
    Msaa = "MSA arrow"
#     [Description("Compass rose")]
    Nav = "Compass rose"
#     [Description("NDB")]
    Ndb = "NDB"
#     [Description("NDB")]
    Ndb_P = "NDB"
#     [Description("Obstacle")]
    Obst1 = "Unlighted obstacle"
#     [Description("Lighted obstacle")]
    Obst2 = "Lighted obstacle"
#     [Description("Group obstacles")]
    Obst3 = "Unlighted group obstacles"
#     [Description("Lighted group obstacles")]
    Obst4 = "Lighted group obstacles"
#     [Description("Exceptionally high obstacle")]
    Obst5 = "Unlighted exceptionally high obstacle"
#     [Description("Lighted exceptionally high obstacle")]
    Obst6 = "Lighted exceptionally high obstacle"
#     [Description("Parachute activity")]
    Par = "Parachute activity"
#     [Description("RDH box")]
    Rdh_P = "RDH box"
#     [Description("Compulsory reporting point")]
    Repc = "Compulsory reporting point"
#     [Description("On request reporting point")]
    Repnc = "On request reporting point"
#     [Description("VFR reporting point")]
    Repv = "VFR reporting point"
#     [Description("Runway visual range (RVR) observation site")]
    Rvr = "Runway visual range (RVR) observation site"
#     [Description("Scale - enroute")]
    Sca1 = "Scale - enroute"
#     [Description("Scale - approach")]
    Sca2 = "Scale - approach"
#     [Description("Scale - aerodrome")]
    Sca3 = "Scale - aerodrome"
#     [Description("TACAN")]
    Tacan = "TACAN"
#     [Description("Transitional altitude box")]
    TAlt_P = "Transitional altitude box"
#     [Description("Tree or shrub")]
    Tree = "Tree or shrub"
#     [Description("Variation east")]
    Vare = "Variation east"
#     [Description("Variation west")]
    Varw = "Variation west"
#     [Description("VOR")]
    Vor = "VOR "
#     [Description("VOR/DME")]
    Vord = "VOR/DME"
#     [Description("VOR/TACAN")]
    Vortac = "VOR/TACAN"
#     [Description("VOR/TACAN")]
    Vortac_P = "VOR/TACAN"
#     [Description("Spotheight (m)")]
    Spot = "Spotheight (m)"
#     [Description("Spotheight (ft)")]
    SpotFt = "Spotheight (ft)"
#     [Description("No Symbol")]
    NoSymbol = "No Symbol"
class DegreesStyle:
    Degrees = 1
    DegreesMinutes = 2
    DegreesMinutesSeconds = 4
    DelimitedBySpace = 8
def vector_norm(data, axis=None, out=None):
    """Return length, i.e. Euclidean norm, of ndarray along axis.

    >>> v = numpy.random.random(3)
    >>> n = vector_norm(v)
    >>> numpy.allclose(n, numpy.linalg.norm(v))
    True
    >>> v = numpy.random.rand(6, 5, 3)
    >>> n = vector_norm(v, axis=-1)
    >>> numpy.allclose(n, numpy.sqrt(numpy.sum(v*v, axis=2)))
    True
    >>> n = vector_norm(v, axis=1)
    >>> numpy.allclose(n, numpy.sqrt(numpy.sum(v*v, axis=1)))
    True
    >>> v = numpy.random.rand(5, 4, 3)
    >>> n = numpy.empty((5, 3))
    >>> vector_norm(v, axis=1, out=n)
    >>> numpy.allclose(n, numpy.sqrt(numpy.sum(v*v, axis=1)))
    True
    >>> vector_norm([])
    0.0
    >>> vector_norm([1])
    1.0

    """
    data = numpy.array(data, dtype=numpy.float64, copy=True)
    if out is None:
        if data.ndim == 1:
            return math.sqrt(numpy.dot(data, data))
        data *= data
        out = numpy.atleast_1d(numpy.sum(data, axis=axis))
        numpy.sqrt(out, out)
        return out
    else:
        data *= data
        numpy.sum(data, axis=axis, out=out)
        numpy.sqrt(out, out)


def unit_vector(data, axis=None, out=None):
    """Return ndarray normalized by length, i.e. Euclidean norm, along axis.

    >>> v0 = numpy.random.random(3)
    >>> v1 = unit_vector(v0)
    >>> numpy.allclose(v1, v0 / numpy.linalg.norm(v0))
    True
    >>> v0 = numpy.random.rand(5, 4, 3)
    >>> v1 = unit_vector(v0, axis=-1)
    >>> v2 = v0 / numpy.expand_dims(numpy.sqrt(numpy.sum(v0*v0, axis=2)), 2)
    >>> numpy.allclose(v1, v2)
    True
    >>> v1 = unit_vector(v0, axis=1)
    >>> v2 = v0 / numpy.expand_dims(numpy.sqrt(numpy.sum(v0*v0, axis=1)), 1)
    >>> numpy.allclose(v1, v2)
    True
    >>> v1 = numpy.empty((5, 4, 3))
    >>> unit_vector(v0, axis=1, out=v1)
    >>> numpy.allclose(v1, v2)
    True
    >>> list(unit_vector([]))
    []
    >>> list(unit_vector([1]))
    [1.0]

    """
    if out is None:
        data = numpy.array(data, dtype=numpy.float64, copy=True)
        if data.ndim == 1:
            data /= math.sqrt(numpy.dot(data, data))
            return data
    else:
        if out is not data:
            out[:] = numpy.array(data, copy=False)
        data = out
    length = numpy.atleast_1d(numpy.sum(data*data, axis))
    numpy.sqrt(length, length)
    if axis is not None:
        length = numpy.expand_dims(length, axis)
    data /= length
    if out is None:
        return data


def random_vector(size):
    """Return array of random doubles in the half-open interval [0.0, 1.0).

    >>> v = random_vector(10000)
    >>> numpy.all(v >= 0) and numpy.all(v < 1)
    True
    >>> v0 = random_vector(10)
    >>> v1 = random_vector(10)
    >>> numpy.any(v0 == v1)
    False

    """
    return numpy.random.random(size)


def vector_product(v0, v1, axis=0):
    """Return vector perpendicular to vectors.

    >>> v = vector_product([2, 0, 0], [0, 3, 0])
    >>> numpy.allclose(v, [0, 0, 6])
    True
    >>> v0 = [[2, 0, 0, 2], [0, 2, 0, 2], [0, 0, 2, 2]]
    >>> v1 = [[3], [0], [0]]
    >>> v = vector_product(v0, v1)
    >>> numpy.allclose(v, [[0, 0, 0, 0], [0, 0, 6, 6], [0, -6, 0, -6]])
    True
    >>> v0 = [[2, 0, 0], [2, 0, 0], [0, 2, 0], [2, 0, 0]]
    >>> v1 = [[0, 3, 0], [0, 0, 3], [0, 0, 3], [3, 3, 3]]
    >>> v = vector_product(v0, v1, axis=1)
    >>> numpy.allclose(v, [[0, 0, 6], [0, -6, 0], [6, 0, 0], [0, -6, 6]])
    True

    """
    return numpy.cross(v0, v1, axis=axis)


def angle_between_vectors(v0, v1, directed=True, axis=0):
    """Return angle between vectors.

    If directed is False, the input vectors are interpreted as undirected axes,
    i.e. the maximum angle is pi/2.

    >>> a = angle_between_vectors([1, -2, 3], [-1, 2, -3])
    >>> numpy.allclose(a, math.pi)
    True
    >>> a = angle_between_vectors([1, -2, 3], [-1, 2, -3], directed=False)
    >>> numpy.allclose(a, 0)
    True
    >>> v0 = [[2, 0, 0, 2], [0, 2, 0, 2], [0, 0, 2, 2]]
    >>> v1 = [[3], [0], [0]]
    >>> a = angle_between_vectors(v0, v1)
    >>> numpy.allclose(a, [0, 1.5708, 1.5708, 0.95532])
    True
    >>> v0 = [[2, 0, 0], [2, 0, 0], [0, 2, 0], [2, 0, 0]]
    >>> v1 = [[0, 3, 0], [0, 0, 3], [0, 0, 3], [3, 3, 3]]
    >>> a = angle_between_vectors(v0, v1, axis=1)
    >>> numpy.allclose(a, [1.5708, 1.5708, 1.5708, 0.95532])
    True

    """
    v0 = numpy.array(v0, dtype=numpy.float64, copy=False)
    v1 = numpy.array(v1, dtype=numpy.float64, copy=False)
    dot = numpy.sum(v0 * v1, axis=axis)
    dot /= vector_norm(v0, axis=axis) * vector_norm(v1, axis=axis)
    return numpy.arccos(dot if directed else numpy.fabs(dot))


def inverse_matrix(matrix):
    """Return inverse of square transformation matrix.

    >>> M0 = random_rotation_matrix()
    >>> M1 = inverse_matrix(M0.T)
    >>> numpy.allclose(M1, numpy.linalg.inv(M0.T))
    True
    >>> for size in range(1, 7):
    ...     M0 = numpy.random.rand(size, size)
    ...     M1 = inverse_matrix(M0)
    ...     if not numpy.allclose(M1, numpy.linalg.inv(M0)): print(size)

    """
    return numpy.linalg.inv(matrix)


def concatenate_matrices(*matrices):
    """Return concatenation of series of transformation matrices.

    >>> M = numpy.random.rand(16).reshape((4, 4)) - 0.5
    >>> numpy.allclose(M, concatenate_matrices(M))
    True
    >>> numpy.allclose(numpy.dot(M, M.T), concatenate_matrices(M, M.T))
    True

    """
    M = numpy.identity(4)
    for i in matrices:
        M = numpy.dot(M, i)
    return M


def is_same_transform(matrix0, matrix1):
    """Return True if two matrices perform same transformation.

    >>> is_same_transform(numpy.identity(4), numpy.identity(4))
    True
    >>> is_same_transform(numpy.identity(4), random_rotation_matrix())
    False

    """
    matrix0 = numpy.array(matrix0, dtype=numpy.float64, copy=True)
    matrix0 /= matrix0[3, 3]
    matrix1 = numpy.array(matrix1, dtype=numpy.float64, copy=True)
    matrix1 /= matrix1[3, 3]
    return numpy.allclose(matrix0, matrix1)

        
        
        
        