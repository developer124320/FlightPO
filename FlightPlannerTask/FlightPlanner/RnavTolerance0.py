
from FlightPlanner.types import DistanceUnits, RnavGnssFlightPhase, RnavFlightPhase, RnavSpecification, AircraftSpeedCategory
from FlightPlanner.helpers import Distance, Unit
import math

class RnavGnssTolerance:

    def __init__(self, rnavSpecification_0=None, rnavGnssFlightPhase_0=None, aircraftSpeedCategory_0=None, rnavFlightPhase_0=None, distance_0=None, distance_1=None, distance_2=None):
        self.xtt = 0.0    
        self.att = 0.0    
        self.asw = 0.0
        if rnavSpecification_0 == None:
            self.asw = distance_2.NauticalMiles
            self.att = distance_1.NauticalMiles
            self.xtt = distance_0.NauticalMiles
            return
        if rnavGnssFlightPhase_0 != None:
            self.method_0(rnavSpecification_0, rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        else:
            self.RnavGnssTolerance(rnavSpecification_0, rnavFlightPhase_0, aircraftSpeedCategory_0, distance_0)
        
#     public RnavGnssTolerance(Distance distance_0, Distance distance_1, Distance distance_2)
#     {
#         self.asw = distance_2.NauticalMiles
#         self.att = distance_1.NauticalMiles
#         self.xtt = distance_0.NauticalMiles
#     }
# 
#     public RnavGnssTolerance(RnavSpecification rnavSpecification_0, RnavGnssFlightPhase rnavGnssFlightPhase_0, AircraftSpeedCategory aircraftSpeedCategory_0)
#     {
#         self.method_0(rnavSpecification_0, rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
#     }
# 
    def getATTMetres(self):
        return self.att * 1.852 * 1000
    
    def getXTTMetres(self):
        return self.xtt * 1.852 * 1000
    
    def getASWMetres(self):
        return self.asw * 1.852 * 1000
    
    def getATT(self):
        return Distance(self.att, DistanceUnits.NM)
    ATT = property(getATT, None, None, None)
    
    def getXTT(self):
        return Distance(self.xtt, DistanceUnits.NM)
    XTT = property(getXTT, None, None, None)
    
    def getASW(self):
        return Distance(self.asw, DistanceUnits.NM)
    ASW = property(getASW, None, None, None)
    
    def getBV(self):
        return Distance(self.asw - 1.5 * self.xtt, DistanceUnits.NM)
    BV = property(getBV, None, None, None)
    
    def RnavGnssTolerance(self, rnavSpecification_0, rnavFlightPhase_0, aircraftSpeedCategory_0, distance_0):
        rnavGnssFlightPhase = RnavGnssFlightPhase.Enroute
        if rnavFlightPhase_0 == RnavFlightPhase.SID:
            if distance_0 >= 30:
                rnavGnssFlightPhase = RnavGnssFlightPhase.StarSid
            elif distance_0 < 15:
                rnavGnssFlightPhase = RnavGnssFlightPhase.Sid15
            else:
                rnavGnssFlightPhase = RnavGnssFlightPhase.Star30Sid30IfIafMa30
        elif rnavFlightPhase_0 == RnavFlightPhase.STAR:
            if distance_0 < 30:
                rnavGnssFlightPhase = RnavGnssFlightPhase.Star30Sid30IfIafMa30
            else:
                rnavGnssFlightPhase = RnavGnssFlightPhase.StarSid
        elif rnavFlightPhase_0 == RnavFlightPhase.IafIf:
            rnavGnssFlightPhase = RnavGnssFlightPhase.Star30Sid30IfIafMa30
        elif rnavFlightPhase_0 == RnavFlightPhase.Faf:
            rnavGnssFlightPhase = RnavGnssFlightPhase.Faf
        elif rnavFlightPhase_0 == RnavFlightPhase.MissedApproach:
            if distance_0 >= 30:
                rnavGnssFlightPhase = RnavGnssFlightPhase.StarSid
            elif distance_0 < 15:
                rnavGnssFlightPhase = RnavGnssFlightPhase.Ma15
            else:
                rnavGnssFlightPhase = RnavGnssFlightPhase.Star30Sid30IfIafMa30
        self.method_0(rnavSpecification_0, rnavGnssFlightPhase, aircraftSpeedCategory_0)
    def method_0(self, rnavSpecification_0, rnavGnssFlightPhase_0, aircraftSpeedCategory_0):
        num = 0.0
        num1 = 0.0
        RnavGnssTolerance.smethod_2(rnavSpecification_0, rnavGnssFlightPhase_0)
        if rnavSpecification_0 == RnavSpecification.Rnav5:
            num1 = 2.51
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.Rnav2:
            if rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Enroute:
                if rnavGnssFlightPhase_0 == RnavGnssFlightPhase.StarSid:
                    num1 = 2
                else:
                    num1 = 1
            else:
                num1 = 2
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.Rnav1:
            if rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Enroute:
                if rnavGnssFlightPhase_0 == RnavGnssFlightPhase.StarSid:
                    num1 = 2
                else:
                    num1 = 1
            else:
                num1 = 2
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.Rnp4:
            num1 = 4
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.Rnp2:
            num1 = 2
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.Rnp1:
            num1 = 1
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.ARnp2:
            num1 = 2
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.ARnp1:
            if rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf:
                if rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt:
                    num1 = 0.3
                else:
                    num1 = 1
            else:
                num1 = 0.3
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.ARnp09:
            if rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf:
                if rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt:
                    num1 = 0.3
                else:
                    num1 = 0.9
            else:
                num1 = 0.3
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.ARnp08:
            if rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf:
                if rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt:
                    num1 = 0.3
                else:
                    num1 = 0.8
            else:
                num1 = 0.3
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.ARnp07:
            if rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf:
                if rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt:
                    num1 = 0.3
                else:
                    num1 = 0.7
            else:
                num1 = 0.3
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.ARnp06:
            if rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf:
                if rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt:
                    num1 = 0.3
                else:
                    num1 = 0.6
            else:
                num1 = 0.3
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.ARnp05:
            if rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf:
                if rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt:
                    num1 = 0.3
                else:
                    num1 = 0.5
            else:
                num1 = 0.3
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.ARnp04:
            if rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf:
                if rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt:
                    num1 = 0.3
                else:
                    num1 = 0.4
            else:
                num1 = 0.3
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.ARnp03:
            num1 = 0.3
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        elif rnavSpecification_0 == RnavSpecification.RnpApch:
            if rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Star30Sid30IfIafMa30:
                if rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Ma15:
                    num1 = 0.3
                else:
                    num1 = 1
            else:
                num1 = 1
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0)
        else:
            raise UserWarning, ("INVALID RnavSpecification")
        self.xtt = num1
        self.att = 0.8 * self.xtt
        self.asw = 1.5 * self.xtt + num
    def method_1(self, rnavGnssFlightPhase_0, aircraftSpeedCategory_0):
        if rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Enroute or rnavGnssFlightPhase_0 == RnavGnssFlightPhase.StarSid:
            if (aircraftSpeedCategory_0 == AircraftSpeedCategory.H):
                return 1
            return 2
        if  rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Star30Sid30IfIafMa30 or rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Faf:
            if (aircraftSpeedCategory_0 == AircraftSpeedCategory.H):
                return 0.7
            return 1
        elif rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Sid15 or rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Ma15 or rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt:
            if aircraftSpeedCategory_0 == AircraftSpeedCategory.H:
                return 0.35
            return 0.5
        else:
            raise UserWarning, "RNAVFLIGHTPHASE NOT SUPPORTED"
    
    # return List<RnavGnssFlightPhase>
    # input RnavSpecification
    @staticmethod
    def smethod_0(rnavSpecification_0):
        #List<RnavGnssFlightPhase>
        rnavGnssFlightPhases = []
        if rnavSpecification_0 == "Rnav5" or rnavSpecification_0 == "Rnav2" or rnavSpecification_0 == "Rnp4" or rnavSpecification_0 == "Rnp2":
            rnavGnssFlightPhases.append("Enroute")
            rnavGnssFlightPhases.append("StarSid")
        elif rnavSpecification_0 == "Rnav1" or rnavSpecification_0 == "Rnp1" or rnavSpecification_0 == "ARnp1":
            rnavGnssFlightPhases.append("Enroute")
            rnavGnssFlightPhases.append("StarSid")
            rnavGnssFlightPhases.append("Star30Sid30IfIafMa30")
            rnavGnssFlightPhases.append("Sid15")
            rnavGnssFlightPhases.append("Ma15")
        elif rnavSpecification_0 == "ARnp2":
            rnavGnssFlightPhases.append("Enroute")
        elif rnavSpecification_0 == "ARnp09" or rnavSpecification_0 == "ARnp08" or rnavSpecification_0 == "ARnp07" or rnavSpecification_0 == "ARnp06" or rnavSpecification_0 == "ARnp05" or rnavSpecification_0 == "ARnp04" or rnavSpecification_0 == "ARnp03":
            rnavGnssFlightPhases.append("StarSid")
            rnavGnssFlightPhases.append("Star30Sid30IfIafMa30")
            rnavGnssFlightPhases.append("Sid15")
            rnavGnssFlightPhases.append("Ma15")
        elif rnavSpecification_0 == "RnpApch":
            rnavGnssFlightPhases.append("Star30Sid30IfIafMa30")
            rnavGnssFlightPhases.append("Faf")
            rnavGnssFlightPhases.append("Mapt")
            rnavGnssFlightPhases.append("Ma15")
        else:
            return []
        return rnavGnssFlightPhases
    # return List<RnavFlightPhase>
    # input RnavSpecification
    @staticmethod
    def smethod_1(rnavSpecification_0):
        rnavFlightPhases = []
        if rnavSpecification_0 == "Rnav5" or rnavSpecification_0 == "Rnav2" or rnavSpecification_0 == "Rnp4" or rnavSpecification_0 == "Rnp2":
            rnavFlightPhases.append("Enroute")
            rnavFlightPhases.append("STAR")
            rnavFlightPhases.append("SID")
        elif rnavSpecification_0 == "Rnav1" or rnavSpecification_0 == "Rnp1" or rnavSpecification_0 == "ARnp1":
            rnavFlightPhases.append("Enroute")
            rnavFlightPhases.append("STAR")
            rnavFlightPhases.append("SID")
            rnavFlightPhases.append("IafIf")
            rnavFlightPhases.append("MissedApproach")
        elif rnavSpecification_0 == "ARnp2":
            rnavFlightPhases.append("Enroute")
        elif rnavSpecification_0 == "ARnp09" or rnavSpecification_0 == "ARnp08" or rnavSpecification_0 == "ARnp07" or rnavSpecification_0 == "ARnp06" or rnavSpecification_0 == "ARnp05" or rnavSpecification_0 == "ARnp04" or rnavSpecification_0 == "ARnp03":
            rnavFlightPhases.append("STAR")
            rnavFlightPhases.append("SID")
            rnavFlightPhases.append("IafIf")
            rnavFlightPhases.append("MissedApproach")
        elif rnavSpecification_0 == "RnpApch":
            rnavFlightPhases.append("STAR")
            rnavFlightPhases.append("SID")
            rnavFlightPhases.append("IafIf")
            rnavFlightPhases.append("Faf")
            rnavFlightPhases.append("MissedApproach")
        else:
            return ("RnavGnssTolerance.smethod_1")
        return rnavFlightPhases
    
    # return void
    # input RnavSpecification
    # input RnavGnssFlightPhase
    @staticmethod
    def smethod_2(rnavSpecification_0, rnavGnssFlightPhase_0):
        #List<RnavGnssFlightPhase>
        listRnavGnssFlightPhase = RnavGnssTolerance.smethod_0(rnavSpecification_0)
        for current in listRnavGnssFlightPhase:
            if current == rnavGnssFlightPhase_0:
                return
        return ("RnavGnssTolerance.smethod_2")
#         try
#         {
#             while (enumerator.MoveNext())
#             {
#                 if (enumerator.Current != rnavGnssFlightPhase_0)
#                 {
#                     continue
#                 }
#                 return
#             }
#             throw new ArgumentException(string.Format(Validations.RNAV_FLIGHT_PHASE_NOT_SUPPORTED, EnumHelper.smethod_0(rnavGnssFlightPhase_0)))
#         }
#         finally
#         {
#             ((IDisposable)enumerator).Dispose()
#         }
#     }
    @staticmethod
    def translateParameter(rnavGnssFlightPhase_0):
        if rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Enroute:
            return "En-route"
        elif rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Faf:
            return "FAF"
        elif rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Ma15:
            return "MA(< 15nm ARP)"
        elif rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt:
            return "MAPt"
        elif rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Sid15:
            return "SID(< 15nm ARP)"
        elif rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Star30Sid30IfIafMa30:
            return "STAR/SID/IF/IAF/MA(< 30 nm ARP)"
        elif rnavGnssFlightPhase_0 == RnavGnssFlightPhase.StarSid:
            return "STAR/SID(> 30 nm ARP)"
class RnavVorDmeTolerance:
    
    
    def __init__(self, rnavSpecification_0 = None, rnavVorDmeFlightPhase_0 = None, distance_0 = None, distance_1 = None, distance_2 = None):
        self.xtt =  Distance(0.0)
        self.att = Distance(0.0) 
        self.asw = Distance(0.0)
        
#         if (rnavSpecification_0 != RnavSpecification.Rnav5)
#         {
#             throw new ArgumentException(string.Format(Validations.RNAV_SPECIFICATION_NOT_SUPPORTED, EnumHelper.smethod_0(rnavSpecification_0)))
#         }
#         if (rnavVorDmeFlightPhase_0 != RnavVorDmeFlightPhase.Enroute)
#         {
#             throw new ArgumentException(string.Format(Validations.RNAV_FLIGHT_PHASE_NOT_SUPPORTED, EnumHelper.smethod_0(rnavVorDmeFlightPhase_0)))
#         }
        num = round(distance_0.NauticalMiles, 5)
        num1 = round(distance_1.NauticalMiles, 5)
        num2 = round(distance_2.NauticalMiles, 5)
        num3 = max([0.085, 0.00125 * num])
        num4 = 0.05
        num5 = 2 * math.sqrt(num3 * num3 + num4 * num4)
        num6 = Unit.ConvertDegToRad(4.5)
        num7 = 5707963267949 if (num1 == 0) else math.atan(num2 / num1)
        num8 = num1 - num * math.cos(num7 + num6)
        num9 = num5 * math.cos(num7)
        num10 = num2 - num * math.sin(num7 - num6)
        num11 = num5 * math.sin(num7)
        num12 = 2.5
        num13 = 0.25
        num14 = 2
        self.xtt = Distance(math.sqrt(num8 * num8 + num9 * num9 + num12 * num12 + num13 * num13), DistanceUnits.NM)
        self.att = Distance(math.sqrt(num10 * num10 + num11 * num11 + num13 * num13), DistanceUnits.NM)
        self.asw = Distance(1.5 * self.xtt.NauticalMiles + num14, DistanceUnits.NM)
#     }
    def get_asw(self):
        return self.asw
    
    def get_att(self):
        return self.att
    
    def get_xtt(self):
        return self.xtt
    ASW = property(get_asw, None, None, None)
    ATT = property(get_att, None, None, None)
    XTT = property(get_xtt, None, None, None)
class RnavDmeDmeTolerance:
    
#     private Distance xtt
# 
#     private Distance att
# 
#     private Distance asw
# 
    def __init__(self, rnavSpecification_0 = None, rnavDmeDmeFlightPhase_0 = None, rnavDmeDmeCriteria_0 = None, altitude_0 = None):
        self.xtt =  Distance(0.0)
        self.att = Distance(0.0) 
        self.asw = Distance(0.0)
#     def RnavDmeDmeTolerance(RnavSpecification rnavSpecification_0, RnavDmeDmeFlightPhase rnavDmeDmeFlightPhase_0, RnavDmeDmeCriteria rnavDmeDmeCriteria_0, Altitude altitude_0)
#     {
        num = 0.0
        num1 = 0.0
        if rnavSpecification_0 == RnavSpecification.Rnav5:
            num = 2.5
        elif rnavSpecification_0 == RnavSpecification.Rnav2:
            num = 1
        elif rnavSpecification_0 == RnavSpecification.Rnav1:
            num = 0.5
        
            
#         switch (rnavSpecification_0)
#         {
#             case RnavSpecification.Rnav5:
#             {
#                 if (rnavDmeDmeFlightPhase_0 != RnavDmeDmeFlightPhase.EnrouteStarSid)
#                 {
#                     throw new ArgumentException(string.Format(Validations.RNAV_FLIGHT_PHASE_NOT_SUPPORTED, EnumHelper.smethod_0(rnavDmeDmeFlightPhase_0)))
#                 }
#                 num = 2.5
#                 break
#             }
#             case RnavSpecification.Rnav2:
#             {
#                 num = 1
#                 break
#             }
#             case RnavSpecification.Rnav1:
#             {
#                 num = 0.5
#                 break
#             }
#             default:
#             {
#                 throw new ArgumentException(string.Format(Validations.RNAV_SPECIFICATION_NOT_SUPPORTED, EnumHelper.smethod_0(rnavSpecification_0)))
#             }
#         }
#         if rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.EnrouteStarSid:
#             num1 = 2
#         elif rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.Star30Sid30IfIaf:
#             num1 = 1
#         elif rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.Sid15:
#             num1 = 0.5
#         switch (rnavDmeDmeFlightPhase_0)
#         {
#             case RnavDmeDmeFlightPhase.EnrouteStarSid:
#             {
#                 num1 = 2
#                 break
#             }
#             case RnavDmeDmeFlightPhase.Star30Sid30IfIaf:
#             {
#                 num1 = 1
#                 break
#             }
#             case RnavDmeDmeFlightPhase.Sid15:
#             {
#                 num1 = 0.5
#                 break
#             }
#             default:
#             {
#                 throw new ArgumentException(string.Format(Validations.RNAV_FLIGHT_PHASE_NOT_SUPPORTED, EnumHelper.smethod_0(rnavDmeDmeFlightPhase_0)))
#             }
#         }
#         num2 = 0.25
#         num3 = Unit.ConvertDegToRad(90)
#         if (rnavDmeDmeCriteria_0 == RnavDmeDmeCriteria.Two):
#             num3 = Unit.ConvertDegToRad(30)
#         num4 = 1.23 * math.sqrt(altitude_0.Feet)
#         if (rnavSpecification_0 == RnavSpecification.Rnav5):
#             num4 = 300
#         elif (rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.EnrouteStarSid):
#             num4 = 1.23 * math.sqrt(15000)
#         num5 = max([0.085, 0.00125 * num4])
#         num6 = 0.05
#         num7 = 2 * math.sqrt(2 * (num5 * num5 + num6 * num6)) / math.sin(num3)
#         self.xtt = Distance(math.sqrt(num7 * num7 + num * num + num2 * num2), DistanceUnits.NM)
#         self.att = Distance(math.sqrt(num7 * num7 + num2 * num2), DistanceUnits.NM)
#         self.asw = Distance(1.5 * self.xtt.NauticalMiles + num1, DistanceUnits.NM)
#     }
    def get_asw(self):
        return self.asw
    
    def get_att(self):
        return self.att
    
    def get_xtt(self):
        return self.xtt
    ASW = property(get_asw, None, None, None)
    ATT = property(get_att, None, None, None)
    XTT = property(get_xtt, None, None, None)
# }
# }
