# -*- coding: UTF-8 -*-
'''
Created on 30 Jun 2015

@author: Administrator
'''
from FlightPlanner.types import DistanceUnits, RnavSpecification, RnavDmeDmeFlightPhase, RnavDmeDmeCriteria

from FlightPlanner.helpers import Distance, Unit
import math

   
class RnavDmeDmeTolerance:
    def __init__(self, rnavSpecification_0, rnavDmeDmeFlightPhase_0, rnavDmeDmeCriteria_0, altitude_0):
#         double num;
#         double num1;
        self.xtt = Distance(0, DistanceUnits.NM);
        self.att = Distance(0, DistanceUnits.NM);
        self.asw = Distance(0, DistanceUnits.NM);



        if rnavSpecification_0 == RnavSpecification.Rnav5:
            if (rnavDmeDmeFlightPhase_0 != RnavDmeDmeFlightPhase.EnrouteStarSid):
                return
#                 throw new ArgumentException(string.Format(Validations.RNAV_FLIGHT_PHASE_NOT_SUPPORTED, EnumHelper.smethod_0(rnavDmeDmeFlightPhase_0)));
            num = 2.5;
        elif rnavSpecification_0 == RnavSpecification.Rnav2:
            num = 1;
        elif rnavSpecification_0 == RnavSpecification.Rnav1:
            num = 0.5;
        else:
            return
        if rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.EnrouteStarSid:
            num1 = 2;
        elif rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.Star30Sid30IfIaf:
            num1 = 1;
        elif rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.Sid15:
            num1 = 0.5;
        else:
            return
        num2 = 0.25;
        num3 = Unit.ConvertDegToRad(90);
        if (rnavDmeDmeCriteria_0 == RnavDmeDmeCriteria.Two):
            num3 = Unit.ConvertDegToRad(30);
        num4 = 1.23 * math.sqrt(altitude_0.Feet);
        if (rnavSpecification_0 == RnavSpecification.Rnav5):
            num4 = 300;
        elif (rnavDmeDmeFlightPhase_0 == RnavDmeDmeFlightPhase.EnrouteStarSid):
            num4 = 1.23 * math.sqrt(15000);
        num5 = max([0.085, 0.00125 * num4]);
        num6 = 0.05;
        num7 = 2 * math.sqrt(2 * (num5 * num5 + num6 * num6)) / math.sin(num3);
        self.xtt = Distance(math.sqrt(num7 * num7 + num * num + num2 * num2), DistanceUnits.NM);
        self.att = Distance(math.sqrt(num7 * num7 + num2 * num2), DistanceUnits.NM);
        self.asw = Distance(1.5 * self.xtt.NauticalMiles + num1, DistanceUnits.NM);
    
    def get_asw(self):
        return self.asw
    ASW = property(get_asw, None, None, None)
    
    def get_xtt(self):
        return self.xtt
    XTT = property(get_xtt, None, None, None)
    
    def get_att(self):
        return self.att
    ATT = property(get_att, None, None, None)