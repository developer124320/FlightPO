'''
Created on Feb 20, 2015

@author: Administrator
'''

from qgis.core import QgsPoint
import math
import numpy


class Point3dCollection(list):
    def __init__(self, point3dCollection = None):
        if point3dCollection != None:
            self.extend(point3dCollection)
        pass
    def Add(self, point3d_0):
        self.append(point3d_0)
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
        return self[i]
    def get_Count(self):
        return len(self)
    
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
        
    def __init__(self, x = 0.0, y = 0.0, z = 0.0, qgsPoint = None):
        if qgsPoint is None:
            QgsPoint.__init__(self, x, y)
        else:
            QgsPoint.__init__(qgsPoint)
        self.zVal = z
        
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
        return Point3D(self.x() , self.y() , self.zVal + multiplor)
    
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
    BaroVNAV = "Baro/VNav Surface"
    BasicGNSS = "NON-Precision with T- or Y-Bar"
    IlsOas = "Obstacle Assesment Surfaces"
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

    RnavVorDme = "RNAV Protection Area (VOR/DME)"
    RnavDmeDme = "RNAV Protection Area (DME/DME)"
    HoldingRnav = "RNAV Holding"
    HoldingRace_P = "Holding Pattern Template Construction"
    HoldingOverHead = "Over-head Holding / Racetrack"
    HoldingVorDme = "VOR/DME Holding / Racetrack"
    HoldingRnp = "RNP Holding"
    VisualCircling = "Visual Circling"
    MSA = "Minimum Sector Altitudes (MSA)"
    DataImport = "Database Import"
    EnrouteStraight = "En-route Straight Segment"
    EnrouteTurnOverHead = "En-route Turn Over-head a Facility"
    RnavStraightSegmentAnalyser = "RNAV (GNSS En-route/STAR) Straight Segment Analyser"
    RnavTurningSegmentAnalyser = "RNAV (GNSS En-route/STAR) Turning Segment Analyser"
    Radial = "Radial Tolerance Construction for VOR or NDB"
    IlsBasic = "ILS Basic Surfaces"
    IasToTas = "True Air Speed (TAS) Calculation"
    TurnArea = "Turn Protection Area Construction"
    OverheadTolerance = "Over-head Tolerance Construction"
    FixConstruction = "Fix Construction"
    FixToleranceArea = "Fix tolerance area"

    ObstacleEvaluator = "Obstacle evaluator"
    StepDownObstacleAnalyser = "15% Area Obstacle Analyser"

    RnavNominal = "RNAV Minimum Stabilisation Track Construction"
    SecondaryMoc = "Secondary MOC Calculation"
    TurnAreaObstacleAnalyser = "Turn Area Obstacle Analyser"
    StepDownObstacleAnalyser0 = "15% Area Obstacle Analyser"
    StepDownObstacleAnalyser = "Step Down Obstacle Analyser"
    InitialMissedApproachObstacleAnalyser = "Initial Missed Approach Obstacle Analyser"
    ObstacleEvaluator = "Obstacle Evaluator"
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
class AltitudeUnits:
    M = 0
    FT = 1
    FL = 2
    SM = 3

class DistanceUnits:
    M = 0
    FT = 1
    KM = 2
    NM = 3
        
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
    MissedApproach = "Missed Approach"
    FinalApproach = "Final Approach"
    Intermediate = "Intermediate"
    Initial1 = "Initial 1"
    Initial2 = "Initial 2"
    Initial3 = "Initial 3"

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

class AngleGradientSlopeUnits:
    Degrees = 0
    Percent = 1
    Slope = 2

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

        
        
        
        