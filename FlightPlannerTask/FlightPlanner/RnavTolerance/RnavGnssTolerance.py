# -*- coding: UTF-8 -*-
'''
Created on 30 Jun 2015

@author: Administrator
'''
from FlightPlanner.types import DistanceUnits, RnavSpecification, RnavDmeDmeFlightPhase, \
                            RnavDmeDmeCriteria, RnavGnssFlightPhase, RnavFlightPhase, AircraftSpeedCategory

from FlightPlanner.helpers import Distance, Unit
import math

   
class RnavGnssTolerance:
    def __init__(self, rnavSpecification_0, rnavGnssFlightPhase_0, rnavFlightPhase_0, aircraftSpeedCategory_0, distance_0 = None, distance_1 = None, distance_2 = None):
        self.asw = None
        self.att = None
        self.xtt = None
        
        if distance_1 != None:
            self.asw = distance_2.NauticalMiles;
            self.att = distance_1.NauticalMiles;
            self.xtt = distance_0.NauticalMiles;
        if rnavGnssFlightPhase_0 != None:
            self.method_0(rnavSpecification_0, rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
            return
        if  rnavFlightPhase_0 != None:
            rnavGnssFlightPhase = RnavGnssFlightPhase.Enroute;
            if (rnavFlightPhase_0 == RnavFlightPhase.SID):
                if (distance_0.NauticalMiles >= 30):
                    rnavGnssFlightPhase = RnavGnssFlightPhase.StarSid;
                elif (distance_0.NauticalMiles < 15):
                    rnavGnssFlightPhase = RnavGnssFlightPhase.Sid15;
                else:
                    rnavGnssFlightPhase = RnavGnssFlightPhase.Star30Sid30IfIafMa30;
            elif rnavFlightPhase_0 == RnavFlightPhase.STAR:
                if (distance_0.NauticalMiles < 30):
                    rnavGnssFlightPhase = RnavGnssFlightPhase.Star30Sid30IfIafMa30;
                else:
                    rnavGnssFlightPhase = RnavGnssFlightPhase.StarSid;
            elif rnavFlightPhase_0 == RnavFlightPhase.IafIf:
                rnavGnssFlightPhase = RnavGnssFlightPhase.Star30Sid30IfIafMa30;
            elif rnavFlightPhase_0 == RnavFlightPhase.Faf:
                rnavGnssFlightPhase = RnavGnssFlightPhase.Faf;
            elif rnavFlightPhase_0 == RnavFlightPhase.MissedApproach:
                if (distance_0.NauticalMiles >= 30):
                    rnavGnssFlightPhase = RnavGnssFlightPhase.StarSid;
                elif (distance_0.NauticalMiles < 15):
                    rnavGnssFlightPhase = RnavGnssFlightPhase.Ma15;
                else:
                    rnavGnssFlightPhase = RnavGnssFlightPhase.Star30Sid30IfIafMa30;
            self.method_0(rnavSpecification_0, rnavGnssFlightPhase, aircraftSpeedCategory_0);
        
        
        pass
    def method_0(self, rnavSpecification_0, rnavGnssFlightPhase_0, aircraftSpeedCategory_0):
        num = 0.0;
        num1 = 0.0;
        RnavGnssTolerance.smethod_2(rnavSpecification_0, rnavGnssFlightPhase_0);
        if rnavSpecification_0 == RnavSpecification.Rnav5:
            num1 = 2.51;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.Rnav2:
            if (rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Enroute):
                if (rnavGnssFlightPhase_0 == RnavGnssFlightPhase.StarSid):
                    num1 = 2;
                else:
                    num1 = 1;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.Rnav1:
            if (rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Enroute):
                if (rnavGnssFlightPhase_0 == RnavGnssFlightPhase.StarSid):
                    num1 = 2;
                else:
                    num1 = 1;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.Rnp4:
            num1 = 4;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.Rnp2:
            num1 = 2;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.Rnp1:
            num1 = 1;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.ARnp2:
            num1 = 2;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.ARnp1:
            if (rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf):
                if (rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt):
                    num1 = 0.3;
                else:
                    num1 = 1;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.ARnp09:
            if (rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf):
                if (rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt):
                    num1 = 0.3;
                else:
                    num1 = 0.9;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.ARnp08:
            if (rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf):
                if (rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt):
                    num1 = 0.3;
                else:
                    num1 = 0.8;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.ARnp07:
            if (rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf):
                if (rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt):
                    num1 = 0.3;
                else:
                    num1 = 0.7;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.ARnp06:
            if (rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf):
                if (rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt):
                    num1 = 0.3;
                else:
                    num1 = 0.6;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.ARnp05:
            if (rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf):
                if (rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt):
                    num1 = 0.3;
                else:
                    num1 = 0.5;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.ARnp04:
            if (rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Faf):
                if (rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt):
                    num1 = 0.3;
                else:
                    num1 = 0.4;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.ARnp03:
            num1 = 0.3;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
        elif rnavSpecification_0 == RnavSpecification.RnpApch:
            if (rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Star30Sid30IfIafMa30):
                if (rnavGnssFlightPhase_0 != RnavGnssFlightPhase.Ma15):
                    num1 = 0.3;
                    num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
            num1 = 1;
            num = self.method_1(rnavGnssFlightPhase_0, aircraftSpeedCategory_0);
#         else:
#             throw new ArgumentException(string.Format(Validations.RNAV_SPECIFICATION_NOT_SUPPORTED, EnumHelper.smethod_0(rnavSpecification_0)));
        self.xtt = num1;
        self.att = 0.8 * self.xtt;
        self.asw = 1.5 * self.xtt + num;
    def method_1(self, rnavGnssFlightPhase_0, aircraftSpeedCategory_0):
        if rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Enroute or rnavGnssFlightPhase_0 == RnavGnssFlightPhase.StarSid:
            if (aircraftSpeedCategory_0 == AircraftSpeedCategory.H):
                return 1;
            return 2;
        elif rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Star30Sid30IfIafMa30 or rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Faf:
            if (aircraftSpeedCategory_0 == AircraftSpeedCategory.H):
                return 0.7;
            return 1;
        elif rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Sid15 or rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Ma15 or rnavGnssFlightPhase_0 == RnavGnssFlightPhase.Mapt:
            if (aircraftSpeedCategory_0 == AircraftSpeedCategory.H):
                return 0.35;
            return 0.5;
#         else:
#             throw new ArgumentException(string.Format(Validations.RNAV_FLIGHT_PHASE_NOT_SUPPORTED, EnumHelper.smethod_0(rnavGnssFlightPhase_0)));
    @staticmethod
    def smethod_0(rnavSpecification_0):
        rnavGnssFlightPhases = [];
        if rnavSpecification_0 == RnavSpecification.Rnav5 or rnavSpecification_0 == RnavSpecification.Rnav2 or rnavSpecification_0 == RnavSpecification.Rnp4 or rnavSpecification_0 == RnavSpecification.Rnp2:
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Enroute);
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.StarSid);
        elif rnavSpecification_0 == RnavSpecification.Rnav1 or rnavSpecification_0 == RnavSpecification.Rnp1 or rnavSpecification_0 == RnavSpecification.ARnp1: 
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Enroute);
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.StarSid);
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Star30Sid30IfIafMa30);
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Sid15);
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Ma15);
        elif rnavSpecification_0 == RnavSpecification.ARnp2:
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Enroute);
        elif rnavSpecification_0 == RnavSpecification.ARnp09 or rnavSpecification_0 == RnavSpecification.ARnp08 or rnavSpecification_0 == RnavSpecification.ARnp07 or rnavSpecification_0 == RnavSpecification.ARnp06 or rnavSpecification_0 == RnavSpecification.ARnp05 or rnavSpecification_0 == RnavSpecification.ARnp04 or rnavSpecification_0 == RnavSpecification.ARnp03:
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.StarSid);
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Star30Sid30IfIafMa30);
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Sid15);
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Ma15);
        elif rnavSpecification_0 == RnavSpecification.RnpApch:
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Star30Sid30IfIafMa30);
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Faf);
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Mapt);
            rnavGnssFlightPhases.append(RnavGnssFlightPhase.Ma15);
#         else:
#             throw new ArgumentException(string.Format(Validations.RNAV_SPECIFICATION_NOT_SUPPORTED, EnumHelper.smethod_0(rnavSpecification_0)));
        return rnavGnssFlightPhases;
    
    @staticmethod
    def smethod_1(rnavSpecification_0):
        rnavFlightPhases = [];
        if rnavSpecification_0 == RnavSpecification.Rnav5 or rnavSpecification_0 == RnavSpecification.Rnav2 or rnavSpecification_0 == RnavSpecification.Rnp4 or rnavSpecification_0 == RnavSpecification.Rnp2:
            rnavFlightPhases.append(RnavFlightPhase.Enroute);
            rnavFlightPhases.append(RnavFlightPhase.STAR);
            rnavFlightPhases.append(RnavFlightPhase.SID);
        elif rnavSpecification_0 == RnavSpecification.Rnav1 or rnavSpecification_0 == RnavSpecification.Rnp1 or rnavSpecification_0 == RnavSpecification.ARnp1:
            rnavFlightPhases.append(RnavFlightPhase.Enroute);
            rnavFlightPhases.append(RnavFlightPhase.STAR);
            rnavFlightPhases.append(RnavFlightPhase.SID);
            rnavFlightPhases.append(RnavFlightPhase.IafIf);
            rnavFlightPhases.append(RnavFlightPhase.MissedApproach);
        elif rnavSpecification_0 == RnavSpecification.ARnp2:
            rnavFlightPhases.append(RnavFlightPhase.Enroute);
        elif rnavSpecification_0 == RnavSpecification.ARnp09 or rnavSpecification_0 == RnavSpecification.ARnp08 or rnavSpecification_0 == RnavSpecification.ARnp07 or rnavSpecification_0 == RnavSpecification.ARnp06 or rnavSpecification_0 == RnavSpecification.ARnp05 or rnavSpecification_0 == RnavSpecification.ARnp04 or rnavSpecification_0 == RnavSpecification.ARnp03:
            rnavFlightPhases.append(RnavFlightPhase.STAR);
            rnavFlightPhases.append(RnavFlightPhase.SID);
            rnavFlightPhases.append(RnavFlightPhase.IafIf);
            rnavFlightPhases.append(RnavFlightPhase.MissedApproach);
        elif rnavSpecification_0 == RnavSpecification.RnpApch:
            rnavFlightPhases.append(RnavFlightPhase.STAR);
            rnavFlightPhases.append(RnavFlightPhase.SID);
            rnavFlightPhases.append(RnavFlightPhase.IafIf);
            rnavFlightPhases.append(RnavFlightPhase.Faf);
            rnavFlightPhases.append(RnavFlightPhase.MissedApproach);
#         else:
#             throw new ArgumentException(string.Format(Validations.RNAV_SPECIFICATION_NOT_SUPPORTED, EnumHelper.smethod_0(rnavSpecification_0)));
        return rnavFlightPhases;
    
    @staticmethod
    def smethod_2(rnavSpecification_0, rnavGnssFlightPhase_0):
        enumerator = RnavGnssTolerance.smethod_0(rnavSpecification_0);
        for current in enumerator:
            if (current != rnavGnssFlightPhase_0):
                continue;
            return;
#         raise 
#         throw new ArgumentException(string.Format(Validations.RNAV_FLIGHT_PHASE_NOT_SUPPORTED, EnumHelper.smethod_0(rnavGnssFlightPhase_0)));
#         }
#         finally
#         {
#                 ((IDisposable)enumerator).Dispose();

     
    def get_asw(self):
        return Distance(self.asw, DistanceUnits.NM)
    ASW = property(get_asw, None, None, None)
    
    def get_xtt(self):
        return Distance(self.xtt, DistanceUnits.NM)
    XTT = property(get_xtt, None, None, None)
    
    def get_att(self):
        return Distance(self.att, DistanceUnits.NM)
    ATT = property(get_att, None, None, None)