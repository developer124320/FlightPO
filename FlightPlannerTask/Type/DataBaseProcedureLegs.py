from FlightPlanner.types import CodeTypeProcPathAixm
from FlightPlanner.helpers import Altitude, Distance, Speed

class DataBaseProcedureLeg:
    def __init__(self):
        self.RecommendedEnt = None;
        self.PointEnt = None;
        self.CenterEnt = None;
        self.CodePhase = "";
        self.CodeType = CodeTypeProcPathAixm.OTHER;
        self.ValCourse = 0;
        self.CodeTypeCourse = "";
        self.CodeDirTurn = "";
        self.CodeTurnValid = "";
        self.CodeDescrDistVer = "";
        self.CodeDistVerUpper = "";
        self.ValDistVerUpper = Altitude(0);
        self.CodeDistVerLower = "";
        self.ValDistVerLower = Altitude(0);
        self.ValVerAngle = 0;
        self.ValSpeedLimit = Speed(0);
        self.CodeSpeedRef = "";
        self.ValDist = Distance(0);
        self.ValDur = 0;
        self.ValTheta = 0;
        self.ValRho = Distance(0);
        self.ValBankAngle = 0;
        self.CodeRepAtc = "";
        self.CodeRoleFix = "";
        self.TxtRmk = "";

        self.dataList = []
        self.nameList = ["Fix Position", "Fix Type", "Recommended Nav. Aid",
                         "Flight Phase", "Leg Type", "Course Type",
                         "Course Angle", "Turn Direction", "Center",
                         "Fly-By", "Bank Angle", "Altitude Interpretation",
                         "Lower Limit Ref.", "Lower Limit", "Upper Limit Ref.",
                         "Upper Limit", "Climb / Descent Angle", "Speed Restriction Ref.",
                         "Speed Restriction", "Segment Length", "Duration",
                         "ATC Reporting"]
    def refresh(self):
        self.dataList = [self.PointEnt, self.CodeRoleFix, self.RecommendedEnt,
                         self.CodePhase, self.CodeType, self.CodeTypeCourse,
                         self.ValCourse, self.CodeDirTurn, self.CenterEnt,
                         self.CodeTurnValid, self.ValBankAngle, self.CodeDescrDistVer,
                         self.CodeDistVerLower, self.ValDistVerLower, self.CodeDistVerUpper,
                         self.ValDistVerUpper, self.ValVerAngle, self.CodeSpeedRef,
                         self.ValSpeedLimit, self.ValDist, self.ValDur,
                         self.CodeRepAtc]
    def method_0(self):
        dataBaseProcedureLeg = DataBaseProcedureLeg()
        dataBaseProcedureLeg.RecommendedEnt = self.RecommendedEnt
        dataBaseProcedureLeg.PointEnt = self.PointEnt
        dataBaseProcedureLeg.CenterEnt = self.CenterEnt
        dataBaseProcedureLeg.CodePhase = self.CodePhase
        dataBaseProcedureLeg.CodeType = self.CodeType
        dataBaseProcedureLeg.ValCourse = self.ValCourse
        dataBaseProcedureLeg.CodeTypeCourse = self.CodeTypeCourse
        dataBaseProcedureLeg.CodeDirTurn = self.CodeDirTurn
        dataBaseProcedureLeg.CodeTurnValid = self.CodeTurnValid
        dataBaseProcedureLeg.CodeDescrDistVer = self.CodeDescrDistVer
        dataBaseProcedureLeg.CodeDistVerUpper = self.CodeDistVerUpper
        dataBaseProcedureLeg.ValDistVerUpper = self.ValDistVerUpper
        dataBaseProcedureLeg.CodeDistVerLower = self.CodeDistVerLower
        dataBaseProcedureLeg.ValDistVerLower = self.ValDistVerLower
        dataBaseProcedureLeg.ValVerAngle = self.ValVerAngle
        dataBaseProcedureLeg.ValSpeedLimit = self.ValSpeedLimit
        dataBaseProcedureLeg.CodeSpeedRef = self.CodeSpeedRef
        dataBaseProcedureLeg.ValDist = self.ValDist
        dataBaseProcedureLeg.ValDur = self.ValDur
        dataBaseProcedureLeg.ValTheta = self.ValTheta
        dataBaseProcedureLeg.ValRho = self.ValRho
        dataBaseProcedureLeg.ValBankAngle = self.ValBankAngle
        dataBaseProcedureLeg.CodeRepAtc = self.CodeRepAtc
        dataBaseProcedureLeg.CodeRoleFix = self.CodeRoleFix
        dataBaseProcedureLeg.TxtRmk = self.TxtRmk

        dataBaseProcedureLeg.dataList = [dataBaseProcedureLeg.PointEnt, dataBaseProcedureLeg.CodeRoleFix, dataBaseProcedureLeg.RecommendedEnt,
                                         dataBaseProcedureLeg.CodePhase, dataBaseProcedureLeg.CodeType, dataBaseProcedureLeg.CodeTypeCourse,
                                         dataBaseProcedureLeg.ValCourse, dataBaseProcedureLeg.CodeDirTurn, dataBaseProcedureLeg.CenterEnt,
                                         dataBaseProcedureLeg.CodeTurnValid, dataBaseProcedureLeg.ValBankAngle, dataBaseProcedureLeg.CodeDescrDistVer,
                                         dataBaseProcedureLeg.CodeDistVerLower, dataBaseProcedureLeg.ValDistVerLower, dataBaseProcedureLeg.CodeDistVerUpper,
                                         dataBaseProcedureLeg.ValDistVerUpper, dataBaseProcedureLeg.ValVerAngle, dataBaseProcedureLeg.CodeSpeedRef,
                                         dataBaseProcedureLeg.ValSpeedLimit, dataBaseProcedureLeg.ValDist, dataBaseProcedureLeg.ValDur,
                                         dataBaseProcedureLeg.CodeRepAtc]
        return dataBaseProcedureLeg;
    def ToString(self):
        return "DataBaseProcedureLeg"

    # # [DisplayName("Center")]
    # def get_CenterEnt(self):
    #     return self.CenterEnt
    # def set_CenterEnt(self, value):
    #     self.CenterEnt = value
    # CenterEnt = property(get_CenterEnt, set_CenterEnt, None, None)
    #
    # # [DisplayName("Altitude Interpretation")]
    # def get_CodeDescrDistVer(self):
    #     return self.CodeDescrDistVer
    # def set_CodeDescrDistVer(self, value):
    #     self.CodeDescrDistVer = value
    # CodeDescrDistVer = property(get_CodeDescrDistVer, set_CodeDescrDistVer, None, None)
    #
    # # [DisplayName("urn Direction")]
    # def get_CodeDirTurn(self):
    #     return self.CodeDirTurn
    # def set_CodeDirTurn(self, value):
    #     self.CodeDirTurn = value
    # CodeDirTurn = property(get_CodeDirTurn, set_CodeDirTurn, None, None)

class DataBaseProcedureLegs(list):
    def __init__(self):
        list.__init__(self)
    def Add(self, dataBaseProcedureLeg):
        self.append(dataBaseProcedureLeg)
    def method_0(self):
        dataBaseProcedureLeg = DataBaseProcedureLegs();
        for dataBaseProcedureLeg1 in self:
            dataBaseProcedureLeg.Add(dataBaseProcedureLeg1.method_0())
        return dataBaseProcedureLeg;
    def ToString(self):
        return "DataBaseProcedureLegs"
    def refresh(self):
        if len(self) == 0:
            return
        for item in self:
            item.refresh()

    def get_Count(self):
        return len(self)
    Count = property(get_Count, None, None, None)

class DataBaseProcedureLegEx:
    def __init__(self):
        self.PointEnt = None;
        self.CenterEnt = None;
        self.CodeLegType = "";
        self.CodePathType = "";
        self.ValMinAlt = Altitude(0);
        self.ValDist = Distance(0);
        self.ValCourse = 0;
        self.ValLegRadial = 0;
        self.VorUidLeg = None;
        self.CodePointType = "";
        self.CodeRepAtc = "";
        self.ValPointRadial = 0;
        self.VorUidPoint = None;
        self.ValLegRadialBack = 0;
        self.VorUidLegBack = None;
        self.ValPointDist1 = Distance(0);
        self.UidPointDist1 = None;
        self.ValPointDist2 = Distance(0);
        self.UidPointDist2 = None;
        self.ValDur = "";
        self.TxtRmk = "";
        self.CodeFlyBy = "";

        self.dataList = []
        self.nameList = ["Point", "Leg Type", "Path Type",
                         "Center", "Min. Alt.", "Length",
                         "Course", "Radial", "Fly-By",
                         "Pnt. Type", "Rep. Pnt. Type", "Pnt. Radial",
                         "Reverse Radial", "Pnt. Dist. 1", "Pnt. Dist. 2",
                         "Duration", ]
    def refresh(self):
        self.dataList = [self.PointEnt, self.CodeLegType, self.CodePathType,
                        self.CenterEnt, self.ValMinAlt, self.ValDist,
                        self.ValCourse, self.ValLegRadial, self.CodeFlyBy,
                        self.CodePointType, self.CodeRepAtc, self.ValPointRadial,
                        self.ValLegRadialBack, self.ValPointDist1, self.ValPointDist2,
                        self.ValDur]
    def method_0(self):
        dataBaseProcedureLegEx = DataBaseProcedureLegEx()
        dataBaseProcedureLegEx.PointEnt = self.PointEnt
        dataBaseProcedureLegEx.CenterEnt = self.CenterEnt
        dataBaseProcedureLegEx.CodeLegType = self.CodeLegType
        dataBaseProcedureLegEx.CodePathType = self.CodePathType
        dataBaseProcedureLegEx.ValMinAlt = self.ValMinAlt
        dataBaseProcedureLegEx.ValDist = self.ValDist
        dataBaseProcedureLegEx.ValCourse = self.ValCourse
        dataBaseProcedureLegEx.ValLegRadial = self.ValLegRadial
        dataBaseProcedureLegEx.VorUidLeg = self.VorUidLeg
        dataBaseProcedureLegEx.CodePointType = self.CodePointType
        dataBaseProcedureLegEx.CodeRepAtc = self.CodeRepAtc
        dataBaseProcedureLegEx.ValPointRadial = self.ValPointRadial
        dataBaseProcedureLegEx.VorUidPoint = self.VorUidPoint
        dataBaseProcedureLegEx.ValLegRadialBack = self.ValLegRadialBack
        dataBaseProcedureLegEx.VorUidLegBack = self.VorUidLegBack
        dataBaseProcedureLegEx.ValPointDist1 = self.ValPointDist1
        dataBaseProcedureLegEx.UidPointDist1 = self.UidPointDist1
        dataBaseProcedureLegEx.ValPointDist2 = self.ValPointDist2
        dataBaseProcedureLegEx.UidPointDist2 = self.UidPointDist2
        dataBaseProcedureLegEx.ValDur = self.ValDur
        dataBaseProcedureLegEx.TxtRmk = self.TxtRmk
        dataBaseProcedureLegEx.CodeFlyBy = self.CodeFlyBy

        dataBaseProcedureLegEx.dataList = [dataBaseProcedureLegEx.PointEnt, dataBaseProcedureLegEx.CodeLegType, dataBaseProcedureLegEx.CodePathType,
                                           dataBaseProcedureLegEx.CenterEnt, dataBaseProcedureLegEx.ValMinAlt, dataBaseProcedureLegEx.ValDist,
                                           dataBaseProcedureLegEx.ValCourse, dataBaseProcedureLegEx.ValLegRadial, dataBaseProcedureLegEx.CodeFlyBy,
                                           dataBaseProcedureLegEx.CodePointType, dataBaseProcedureLegEx.CodeRepAtc, dataBaseProcedureLegEx.ValPointRadial,
                                           dataBaseProcedureLegEx.ValLegRadialBack, dataBaseProcedureLegEx.ValPointDist1, dataBaseProcedureLegEx.ValPointDist2,
                                           dataBaseProcedureLegEx.ValDur]
        return dataBaseProcedureLegEx;
    def ToString(self):
        return "DataBaseProcedureLegEx"

class DataBaseProcedureLegsEx(list):
    def __init__(self):
        list.__init__(self)
    def Add(self, dataBaseProcedureLegEx):
        self.append(dataBaseProcedureLegEx)
    def method_0(self):
        dataBaseProcedureLegsEx = DataBaseProcedureLegsEx();
        for dataBaseProcedureLegEx1 in self:
            dataBaseProcedureLegsEx.Add(dataBaseProcedureLegEx1.method_0())
        return dataBaseProcedureLegsEx;
    def ToString(self):
        return "DataBaseProcedureLegsEx"
    def refresh(self):
        if len(self) == 0:
            return
        for item in self:
            item.refresh()

    def get_Count(self):
        return len(self)
    Count = property(get_Count, None, None, None)

    

