

'''
Money
'''
from PyQt4.QtCore import QFile, QDataStream, QIODevice, QString
from FlightPlanner.types import AerodromeSurfacesInnerHorizontalLocation, AerodromeSurfacesCriteriaType,\
    AerodromeSurfacesRunwayCode, AerodromeSurfacesApproachType, AerodromeSurfacesBalkedLandingFrom,\
    AerodromeSurfacesTakeOffFrom, HeliportSurfacesSlopeCategory, HeliportSurfacesUsage, HeliportSurfacesApproachAngle, HeliportSurfacesApproachHeight
from FlightPlanner.Captions import Captions
from FlightPlanner.messages import Messages
from FlightPlanner.helpers import MathHelper, Distance, Altitude, AngleGradientSlope, AngleGradientSlopeUnits
from Type.Extensions import Extensions
from Type.switch import switch

from Type.String import String, StringBuilder
from Type.double import double
import define
import math
class ApproachSurfaceCriteria:
    def __init__(self, innerEdge = None, distFromTHR = None, divergence = None, length1 = None, slope1 = None, length2 = None, slope2 = None, length3 = None, totalLength = None):
        self.Enabled = (not Extensions.smethod_18(innerEdge) or not Extensions.smethod_18(distFromTHR) or not Extensions.smethod_18(divergence) or not Extensions.smethod_18(length1) or not Extensions.smethod_18(slope1) or not Extensions.smethod_18(length2) or not Extensions.smethod_18(slope2) or ((not Extensions.smethod_18(length3)) and False or Extensions.smethod_18(totalLength)))
        self.InnerEdge = Extensions.smethod_17(innerEdge)
        self.DistFromTHR = Extensions.smethod_17(distFromTHR)
        self.Divergence = Extensions.smethod_17(divergence)
        self.Length1 = Extensions.smethod_17(length1)
        self.Slope1 = Extensions.smethod_17(slope1)
        self.HasSection2 = Extensions.smethod_18(length2)
        self.Length2 = Extensions.smethod_17(length2)
        self.Slope2 = Extensions.smethod_17(slope2)
        self.Length3 = Extensions.smethod_17(length3)
        self.TotalLength = Extensions.smethod_17(totalLength)
    @staticmethod
    def Empty():
        approachSurfaceCriterium = ApproachSurfaceCriteria()
        approachSurfaceCriterium.Enabled = False
        approachSurfaceCriterium.InnerEdge = 0
        approachSurfaceCriterium.DistFromTHR = 0
        approachSurfaceCriterium.Divergence = 0
        approachSurfaceCriterium.Length1 = 0
        approachSurfaceCriterium.Slope1 = 0
        approachSurfaceCriterium.HasSection2 = False
        approachSurfaceCriterium.Length2 = 0
        approachSurfaceCriterium.Slope2 = 0
        approachSurfaceCriterium.Length3 = 0
        approachSurfaceCriterium.TotalLength = 0
        return approachSurfaceCriterium
    # Empty = property(ApproachSurfaceCriteria.get_Empty, None, None, None)

class BalkedLandingSurfaceCriteria:
    def __init__(self, innerEdge = None, distFromTHR = None, distFromTHRFixed = False, divergence = None, slope = None):
        self.Enabled = (not Extensions.smethod_18(innerEdge) or not Extensions.smethod_18(distFromTHR) or ((not Extensions.smethod_18(divergence)) and  False or Extensions.smethod_18(slope)))
        self.InnerEdge = Extensions.smethod_17(innerEdge)
        self.DistFromTHR = Extensions.smethod_17(distFromTHR)
        self.DistFromTHRFixed = distFromTHRFixed
        self.Divergence = Extensions.smethod_17(divergence)
        self.Slope = Extensions.smethod_17(slope)
    @staticmethod
    def Empty():
        balkedLandingSurfaceCriterium = BalkedLandingSurfaceCriteria()
        balkedLandingSurfaceCriterium.Enabled = False
        balkedLandingSurfaceCriterium.InnerEdge = 0
        balkedLandingSurfaceCriterium.DistFromTHR = 0
        balkedLandingSurfaceCriterium.DistFromTHRFixed = False
        balkedLandingSurfaceCriterium.Divergence = 0
        balkedLandingSurfaceCriterium.Slope = 0
        return balkedLandingSurfaceCriterium
    # Empty = property(get_Empty, None, None, None)

class ConicalSurfaceCriteria:
    def __init__(self, slope = None, height = None):
        self.Enabled = (not ((Extensions.smethod_18(height)) and False or Extensions.smethod_18(slope)))
        self.Height = Extensions.smethod_17(height)
        self.Slope = Extensions.smethod_17(slope)
    @staticmethod
    def Empty():
        conicalSurfaceCriterium = ConicalSurfaceCriteria()
        conicalSurfaceCriterium.Enabled = False
        conicalSurfaceCriterium.Slope = 0
        conicalSurfaceCriterium.Height = 0
        return conicalSurfaceCriterium
    # Empty = property(get_Empty, None, None, None)

class InnerApproachSurfaceCriteria:
    def __init__(self, width = None, distFromTHR = None, length = None, slope = None):
        self.Enabled = (not Extensions.smethod_18(width) or not Extensions.smethod_18(distFromTHR) or ((not Extensions.smethod_18(length)) and False or Extensions.smethod_18(slope)))
        self.Width = Extensions.smethod_17(width)
        self.DistFromTHR = Extensions.smethod_17(distFromTHR)
        self.Length = Extensions.smethod_17(length)
        self.Slope = Extensions.smethod_17(slope)
    @staticmethod
    def Empty():
        innerApproachSurfaceCriterium = InnerApproachSurfaceCriteria()
        innerApproachSurfaceCriterium.Enabled = False
        innerApproachSurfaceCriterium.Width = 0
        innerApproachSurfaceCriterium.DistFromTHR = 0
        innerApproachSurfaceCriterium.Length = 0
        innerApproachSurfaceCriterium.Slope = 0
        return innerApproachSurfaceCriterium
    # Empty = property(get_Empty, None, None, None)

class InnerHorizontalSurfaceCriteria:
    def __init__(self, location = None, height = None, radius = None):
        self.Enabled = ((not Extensions.smethod_18(height)) and False or Extensions.smethod_18(radius))
        self.Location = location
        self.Height = Extensions.smethod_17(height)
        self.Radius = Extensions.smethod_17(radius)
    @staticmethod
    def Empty():
        innerHorizontalSurfaceCriterium = InnerHorizontalSurfaceCriteria()
        innerHorizontalSurfaceCriterium.Enabled = False
        innerHorizontalSurfaceCriterium.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
        innerHorizontalSurfaceCriterium.Height = 0
        innerHorizontalSurfaceCriterium.Radius = 0
        return innerHorizontalSurfaceCriterium
    # Empty = property(get_Empty, None, None, None)

class InnerTransitionalSurfaceCriteria:
    def __init__(self, slope = None):
        self.Enabled = Extensions.smethod_18(slope)
        self.Slope = Extensions.smethod_17(slope)
    @staticmethod
    def Empty():
        innerTransitionalSurfaceCriteria = InnerTransitionalSurfaceCriteria()
        innerTransitionalSurfaceCriteria.Enabled = False
        innerTransitionalSurfaceCriteria.Slope = 0
        return innerTransitionalSurfaceCriteria
    # Empty = property(get_Empty, None, None, None)

class NavigationalAidSurfaceCriteria:
    def __init__(self, slope = None):
        self.Enabled = Extensions.smethod_18(slope)
        self.Slope = Extensions.smethod_17(slope)
    @staticmethod
    def Empty():
        navigationalAidSurfaceCriteria = NavigationalAidSurfaceCriteria()
        navigationalAidSurfaceCriteria.Slope = 0
        return navigationalAidSurfaceCriteria
    # Empty = property(get_Empty, None, None, None)

class OuterHorizontalSurfaceCriteria:
    def __init__(self, height = None, radius = None):
        self.Enabled = ((not Extensions.smethod_18(height)) and False or Extensions.smethod_18(radius))
        self.Height = Extensions.smethod_17(height)
        self.Radius = Extensions.smethod_17(radius)
    @staticmethod
    def Empty():
        outerHorizontalSurfaceCriteria = OuterHorizontalSurfaceCriteria()
        outerHorizontalSurfaceCriteria.Enabled = False
        outerHorizontalSurfaceCriteria.Height = 0
        outerHorizontalSurfaceCriteria.Radius = 0
        return outerHorizontalSurfaceCriteria
    # Empty = property(get_Empty, None, None, None)

class StripSurfaceCriteria:
    def __init__(self, length = None, width = None):
        self.Enabled = ((not Extensions.smethod_18(length)) and False or Extensions.smethod_18(width))
        self.Length = Extensions.smethod_17(length)
        self.Width = Extensions.smethod_17(width)
    @staticmethod
    def Empty():
        stripSurfaceCriteria = StripSurfaceCriteria()
        stripSurfaceCriteria.Enabled = False
        stripSurfaceCriteria.Length = 0
        stripSurfaceCriteria.Width = 0
        return stripSurfaceCriteria
    # Empty = property(get_Empty, None, None, None)

class TakeOffSurfaceCriteria:
    def __init__(self,  innerEdge = None, distFromEND = None, distFromENDFixed = False, divergence = None, finalWidth = None, length = None, slope = None):
        self.Enabled = not Extensions.smethod_18(innerEdge) or not Extensions.smethod_18(distFromEND) or not Extensions.smethod_18(divergence) or not Extensions.smethod_18(finalWidth) or ((not Extensions.smethod_18(length)) and False or Extensions.smethod_18(slope))
        self.InnerEdge = Extensions.smethod_17(innerEdge)
        self.DistFromEND = Extensions.smethod_17(distFromEND)
        self.DistFromENDFixed = distFromENDFixed
        self.Divergence = Extensions.smethod_17(divergence)
        self.FinalWidth = Extensions.smethod_17(finalWidth)
        self.Length = Extensions.smethod_17(length)
        self.Slope = Extensions.smethod_17(slope)
    @staticmethod
    def Empty():
        takeOffSurfaceCriterium = TakeOffSurfaceCriteria()
        takeOffSurfaceCriterium.Enabled = False
        takeOffSurfaceCriterium.InnerEdge = 0
        takeOffSurfaceCriterium.DistFromEND = 0
        takeOffSurfaceCriterium.DistFromENDFixed = False
        takeOffSurfaceCriterium.Divergence = 0
        takeOffSurfaceCriterium.FinalWidth = 0
        takeOffSurfaceCriterium.Length = 0
        takeOffSurfaceCriterium.Slope = 0
        return takeOffSurfaceCriterium
    # Empty = property(get_Empty, None, None, None)

class TransitionalSurfaceCriteria:
    def __init__(self, slope = None):
        self.Enabled = Extensions.smethod_18(slope)
        self.Slope = Extensions.smethod_17(slope)
    @staticmethod
    def Empty():
        transitionalSurfaceCriteria = TransitionalSurfaceCriteria()
        transitionalSurfaceCriteria.Enabled = False
        transitionalSurfaceCriteria.Slope = 0
        return transitionalSurfaceCriteria
    # Empty = property(get_Empty, None, None, None)


class AerodromeSurfacesCriteria:
    def __init__(self, aerodromeSurfacesCriteriaType_0, aerodromeSurfacesApproachType_0 = None, aerodromeSurfacesRunwayCode_0 = None, double_0 = None, bool_0 = False, bool_1 = False, bool_2 = False, bool_3 = False):
        self.name = None
        self.Criteria = AerodromeSurfacesCriteriaType.Custom
        self.Approach = ApproachSurfaceCriteria.Empty()
        self.BalkedLanding = BalkedLandingSurfaceCriteria.Empty()
        self.Conical = ConicalSurfaceCriteria.Empty()
        self.InnerApproach = InnerApproachSurfaceCriteria.Empty()
        self.InnerHorizontal = InnerHorizontalSurfaceCriteria.Empty()
        self.InnerTransitional = InnerTransitionalSurfaceCriteria.Empty()
        self.NavigationalAid = NavigationalAidSurfaceCriteria.Empty()
        self.OuterHorizontal = OuterHorizontalSurfaceCriteria.Empty()
        self.Strip = StripSurfaceCriteria.Empty()
        self.TakeOff = TakeOffSurfaceCriteria.Empty()
        self.Transitional = TransitionalSurfaceCriteria.Empty()

        if aerodromeSurfacesApproachType_0 == None:
            self.Criteria = aerodromeSurfacesCriteriaType_0
            self.name = aerodromeSurfacesCriteriaType_0
            return

        self.method_0(aerodromeSurfacesCriteriaType_0, aerodromeSurfacesApproachType_0, aerodromeSurfacesRunwayCode_0, double_0, bool_0, bool_1, bool_2, bool_3)

    def method_0(self, aerodromeSurfacesCriteriaType_0, aerodromeSurfacesApproachType_0, aerodromeSurfacesRunwayCode_0, double_0, bool_0, bool_1, bool_2, bool_3):
        num = None
        self.Criteria = aerodromeSurfacesCriteriaType_0
        self.name = aerodromeSurfacesCriteriaType_0
        if (aerodromeSurfacesCriteriaType_0 == AerodromeSurfacesCriteriaType.Annex14):
            for case0 in switch(aerodromeSurfacesApproachType_0):
                if case0 (AerodromeSurfacesApproachType.NonInstrument):
                    for case1 in switch (aerodromeSurfacesRunwayCode_0):
                        if case1(AerodromeSurfacesRunwayCode.Code1):
                            self.Strip.Enabled = True
                            self.Strip.Length = 30
                            self.Strip.Width = 30
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 35
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            self.InnerHorizontal.Radius = 2000
                            self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 60
                            self.Approach.DistFromTHR = 30
                            self.Approach.Divergence = 10
                            self.Approach.Length1 = 1600
                            self.Approach.Slope1 = 5
                            self.Approach.HasSection2 = False
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 20
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 60
                            self.TakeOff.DistFromEND = 30
                            self.TakeOff.DistFromENDFixed = False
                            self.TakeOff.Divergence = 10
                            self.TakeOff.FinalWidth = 380
                            self.TakeOff.Length = 1600
                            self.TakeOff.Slope = 5
                            self.OuterHorizontal.Enabled = False
                            self.NavigationalAid.Enabled = False
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code2):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 40
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 55
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            self.InnerHorizontal.Radius = 2500
                            self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 80
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 10
                            self.Approach.Length1 = 2500
                            self.Approach.Slope1 = 4
                            self.Approach.HasSection2 = False
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 20
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 80
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = False
                            self.TakeOff.Divergence = 10
                            self.TakeOff.FinalWidth = 580
                            self.TakeOff.Length = 2500
                            self.TakeOff.Slope = 4
                            self.OuterHorizontal.Enabled = False
                            self.NavigationalAid.Enabled = False
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code3):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 75
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 75
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            self.InnerHorizontal.Radius = 4000
                            self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 150
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 10
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 3.33
                            self.Approach.HasSection2 = False
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 180
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = False
                            self.TakeOff.Divergence = 12.5
                            self.TakeOff.FinalWidth = (bool_1) and 1800 or 1200
                            self.TakeOff.Length = 15000
                            self.TakeOff.Slope = (bool_2) and 1.6 or 2
                            self.OuterHorizontal.Enabled = True
                            self.OuterHorizontal.Height = 150
                            self.OuterHorizontal.Radius = 15000
                            self.NavigationalAid.Enabled = False
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code4):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 75
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 100
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            self.InnerHorizontal.Radius = 4000
                            self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 150
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 10
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2.5
                            self.Approach.HasSection2 = False
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 180
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = False
                            self.TakeOff.Divergence = 12.5
                            self.TakeOff.FinalWidth = (bool_1) and 1800 or 1200
                            self.TakeOff.Length = 15000
                            self.TakeOff.Slope = (bool_2) and 1.6 or 2
                            self.OuterHorizontal.Enabled = True
                            self.OuterHorizontal.Height = 150
                            self.OuterHorizontal.Radius = 15000
                            self.NavigationalAid.Enabled = False
                            return
                        else:
                            return
                    break
                elif case0(AerodromeSurfacesApproachType.NonPrecision):
                    for case1 in switch (aerodromeSurfacesRunwayCode_0):
                        if case1(AerodromeSurfacesRunwayCode.Code1):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 75
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 60
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            self.InnerHorizontal.Radius = 3500
                            self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 150
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 2500
                            self.Approach.Slope1 = 3.33
                            self.Approach.HasSection2 = False
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 20
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 60
                            self.TakeOff.DistFromEND = 30
                            self.TakeOff.DistFromENDFixed = False
                            self.TakeOff.Divergence = 10
                            self.TakeOff.FinalWidth = 380
                            self.TakeOff.Length = 1600
                            self.TakeOff.Slope = 5
                            self.OuterHorizontal.Enabled = False
                            self.NavigationalAid.Enabled = False
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code2):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 75
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 60
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            self.InnerHorizontal.Radius = 3500
                            self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 150
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 2500
                            self.Approach.Slope1 = 3.33
                            self.Approach.HasSection2 = False
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 20
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 80
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = False
                            self.TakeOff.Divergence = 10
                            self.TakeOff.FinalWidth = 580
                            self.TakeOff.Length = 2500
                            self.TakeOff.Slope = 4
                            self.OuterHorizontal.Enabled = False
                            self.NavigationalAid.Enabled = False
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code3):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 150
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 75
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            self.InnerHorizontal.Radius = 4000
                            self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 300
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2
                            self.Approach.HasSection2 = True
                            self.Approach.Length2 = 3600
                            self.Approach.Slope2 = 2.5
                            self.Approach.Length3 = 8400
                            self.Approach.TotalLength = 15000
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 180
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = False
                            self.TakeOff.Divergence = 12.5
                            self.TakeOff.FinalWidth = (bool_1) and 1800 or 1200
                            self.TakeOff.Length = 15000
                            self.TakeOff.Slope = (bool_2) and 1.6 or 2
                            self.OuterHorizontal.Enabled = True
                            self.OuterHorizontal.Height = 150
                            self.OuterHorizontal.Radius = 15000
                            self.NavigationalAid.Enabled = False
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code4):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 150
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 100
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            self.InnerHorizontal.Radius = 4000
                            self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 300
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2
                            self.Approach.HasSection2 = True
                            self.Approach.Length2 = 3600
                            self.Approach.Slope2 = 2.5
                            self.Approach.Length3 = 8400
                            self.Approach.TotalLength = 15000
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 180
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = False
                            self.TakeOff.Divergence = 12.5
                            self.TakeOff.FinalWidth = (bool_1) and 1800 or 1200
                            self.TakeOff.Length = 15000
                            self.TakeOff.Slope = (bool_2) and 1.6 or 2
                            self.OuterHorizontal.Enabled = True
                            self.OuterHorizontal.Height = 150
                            self.OuterHorizontal.Radius = 15000
                            self.NavigationalAid.Enabled = False
                            return
                        else:
                            return
                    break
                elif case0(AerodromeSurfacesApproachType.Precision):
                    for case1 in switch (aerodromeSurfacesRunwayCode_0):
                        if case1(AerodromeSurfacesRunwayCode.Code1):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 75
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 60
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            self.InnerHorizontal.Radius = 3500
                            self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
                            self.InnerApproach.Enabled = True
                            self.InnerApproach.Width = 90
                            self.InnerApproach.DistFromTHR = 60
                            self.InnerApproach.Length = 900
                            self.InnerApproach.Slope = 2.5
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 150
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2.5
                            self.Approach.HasSection2 = True
                            self.Approach.Length2 = 12000
                            self.Approach.Slope2 = 3
                            self.Approach.Length3 = 0
                            self.Approach.TotalLength = 15000
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = True
                            self.InnerTransitional.Slope = 40
                            self.BalkedLanding.Enabled = True
                            self.BalkedLanding.InnerEdge = 90
                            self.BalkedLanding.DistFromTHR = 0
                            self.BalkedLanding.DistFromTHRFixed = False
                            self.BalkedLanding.Divergence = 10
                            self.BalkedLanding.Slope = 4
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 60
                            self.TakeOff.DistFromEND = 30
                            self.TakeOff.DistFromENDFixed = False
                            self.TakeOff.Divergence = 10
                            self.TakeOff.FinalWidth = 380
                            self.TakeOff.Length = 1600
                            self.TakeOff.Slope = 5
                            self.OuterHorizontal.Enabled = False
                            self.NavigationalAid.Enabled = False
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code2):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 75
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 60
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            self.InnerHorizontal.Radius = 3500
                            self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
                            self.InnerApproach.Enabled = True
                            self.InnerApproach.Width = 90
                            self.InnerApproach.DistFromTHR = 60
                            self.InnerApproach.Length = 900
                            self.InnerApproach.Slope = 2
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 150
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2.5
                            self.Approach.HasSection2 = True
                            self.Approach.Length2 = 12000
                            self.Approach.Slope2 = 3
                            self.Approach.Length3 = 0
                            self.Approach.TotalLength = 15000
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = True
                            self.InnerTransitional.Slope = 40
                            self.BalkedLanding.Enabled = True
                            self.BalkedLanding.InnerEdge = 90
                            self.BalkedLanding.DistFromTHR = 0
                            self.BalkedLanding.DistFromTHRFixed = False
                            self.BalkedLanding.Divergence = 10
                            self.BalkedLanding.Slope = 4
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 80
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = False
                            self.TakeOff.Divergence = 10
                            self.TakeOff.FinalWidth = 580
                            self.TakeOff.Length = 2500
                            self.TakeOff.Slope = 4
                            self.OuterHorizontal.Enabled = False
                            self.NavigationalAid.Enabled = False
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code3):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 150
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 100
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            self.InnerHorizontal.Radius = 4000
                            self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
                            self.InnerApproach.Enabled = True
                            self.InnerApproach.Width = (bool_0) and 155 or 120
                            self.InnerApproach.DistFromTHR = 60
                            self.InnerApproach.Length = 900
                            self.InnerApproach.Slope = 2
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 300
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2
                            self.Approach.HasSection2 = True
                            self.Approach.Length2 = 3600
                            self.Approach.Slope2 = 2.5
                            self.Approach.Length3 = 8400
                            self.Approach.TotalLength = 15000
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = True
                            self.InnerTransitional.Slope = 33.3
                            self.BalkedLanding.Enabled = True
                            self.BalkedLanding.InnerEdge = (bool_0) and 155 or 120
                            self.BalkedLanding.DistFromTHR = 1800
                            self.BalkedLanding.DistFromTHRFixed = False
                            self.BalkedLanding.Divergence = 10
                            self.BalkedLanding.Slope = 3.33
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 180
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = False
                            self.TakeOff.Divergence = 12.5
                            self.TakeOff.FinalWidth = (bool_1) and 1800 or 1200
                            self.TakeOff.Length = 15000
                            self.TakeOff.Slope = (bool_2) and 1.6 or 2
                            self.OuterHorizontal.Enabled = True
                            self.OuterHorizontal.Height = 150
                            self.OuterHorizontal.Radius = 15000
                            self.NavigationalAid.Enabled = False
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code4):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 150
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 100
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            self.InnerHorizontal.Radius = 4000
                            self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Runway
                            self.InnerApproach.Enabled = True
                            self.InnerApproach.Width = (bool_0) and 155 or 120
                            self.InnerApproach.DistFromTHR = 60
                            self.InnerApproach.Length = 900
                            self.InnerApproach.Slope = 2
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 300
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2
                            self.Approach.HasSection2 = True
                            self.Approach.Length2 = 3600
                            self.Approach.Slope2 = 2.5
                            self.Approach.Length3 = 8400
                            self.Approach.TotalLength = 15000
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = True
                            self.InnerTransitional.Slope = 33.3
                            self.BalkedLanding.Enabled = True
                            self.BalkedLanding.InnerEdge = (bool_0) and 155 or 120
                            self.BalkedLanding.DistFromTHR = 1800
                            self.BalkedLanding.DistFromTHRFixed = False
                            self.BalkedLanding.DistFromTHRFixed = False
                            self.BalkedLanding.Divergence = 10
                            self.BalkedLanding.Slope = 3.33
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 180
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = False
                            self.TakeOff.Divergence = 12.5
                            self.TakeOff.FinalWidth = (bool_1) and 1800 or 1200
                            self.TakeOff.Length = 15000
                            self.TakeOff.Slope = (bool_2) and 1.6 or 2
                            self.OuterHorizontal.Enabled = True
                            self.OuterHorizontal.Height = 150
                            self.OuterHorizontal.Radius = 15000
                            self.NavigationalAid.Enabled = False
                            return
                        else:
                            return
                    break
                else:
                    return
        if (aerodromeSurfacesCriteriaType_0 == AerodromeSurfacesCriteriaType.Cap168):
            for case0 in switch (aerodromeSurfacesApproachType_0):
                if case0(AerodromeSurfacesApproachType.NonInstrument):
                    for case1 in switch (aerodromeSurfacesRunwayCode_0):
                        if case1(AerodromeSurfacesRunwayCode.Code1):
                            self.Strip.Enabled = True
                            self.Strip.Length = 30
                            self.Strip.Width = 30
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 35
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            if (double_0 >= 1800):
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Strip
                            else:
                                self.InnerHorizontal.Radius = 2000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.MidPoint
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 60
                            self.Approach.DistFromTHR = 30
                            self.Approach.Divergence = 10
                            self.Approach.Length1 = 1600
                            self.Approach.Slope1 = 5
                            self.Approach.HasSection2 = False
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 20
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = (bool_3) and 150 or 60
                            self.TakeOff.DistFromEND = 30
                            self.TakeOff.DistFromENDFixed = True
                            self.TakeOff.Divergence = 10
                            self.TakeOff.FinalWidth = 380
                            self.TakeOff.Length = 1600
                            self.TakeOff.Slope = 5
                            self.OuterHorizontal.Enabled = False
                            self.NavigationalAid.Enabled = True
                            self.NavigationalAid.Slope = 10
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code2):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 40
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 55
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            if (double_0 >= 1800):
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Strip
                            else:
                                self.InnerHorizontal.Radius = 2500
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.MidPoint
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 80
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 10
                            self.Approach.Length1 = 2500
                            self.Approach.Slope1 = 4
                            self.Approach.HasSection2 = False
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 20
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = (bool_3) and 150 or 80
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = True
                            self.TakeOff.Divergence = 10
                            self.TakeOff.FinalWidth = 580
                            self.TakeOff.Length = 2500
                            self.TakeOff.Slope = 4
                            self.OuterHorizontal.Enabled = False
                            self.NavigationalAid.Enabled = True
                            self.NavigationalAid.Slope = 10
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code3):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 75
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 105
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            if (double_0 >= 1800):
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Strip
                            else:
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.MidPoint
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 150
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 10
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 3.33
                            self.Approach.HasSection2 = False
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 180
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = True
                            self.TakeOff.Divergence = 12.5
                            if (bool_1):
                                num = 1800
                            else:
                                num1 = 1200
                                num2 = num1
                                self.TakeOff.FinalWidth = num1
                                num = num2
                            self.TakeOff.FinalWidth = num
                            self.TakeOff.Length = 15000
                            self.TakeOff.Slope = (bool_2) and 1.6 or 2
                            if (double_0 < 1100):
                                self.OuterHorizontal.Enabled = False
                            elif (double_0 >= 1860):
                                self.OuterHorizontal.Enabled = True
                                self.OuterHorizontal.Height = 150
                                self.OuterHorizontal.Radius = 15000
                            else:
                                self.OuterHorizontal.Enabled = True
                                self.OuterHorizontal.Height = 150
                                self.OuterHorizontal.Radius = 10000
                            self.NavigationalAid.Enabled = True
                            self.NavigationalAid.Slope = 10
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code4):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 75
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 105
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            if (double_0 >= 1800):
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Strip
                            else:
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.MidPoint
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 150
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 10
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2.5
                            self.Approach.HasSection2 = False
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 180
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = True
                            self.TakeOff.Divergence = 12.5
                            self.TakeOff.FinalWidth = (bool_1) and 1800 or 1200
                            self.TakeOff.Length = 15000
                            self.TakeOff.Slope = (bool_2) and 1.6 or 2
                            if (double_0 < 1100):
                                self.OuterHorizontal.Enabled = False
                            elif (double_0 >= 1860):
                                self.OuterHorizontal.Enabled = True
                                self.OuterHorizontal.Height = 150
                                self.OuterHorizontal.Radius = 15000
                            else:
                                self.OuterHorizontal.Enabled = True
                                self.OuterHorizontal.Height = 150
                                self.OuterHorizontal.Radius = 10000
                            self.NavigationalAid.Enabled = True
                            self.NavigationalAid.Slope = 10
                            return
                        else:
                            return
                    break
                elif case0(AerodromeSurfacesApproachType.NonPrecision):
                    for case1 in switch (aerodromeSurfacesRunwayCode_0):
                        if case1(AerodromeSurfacesRunwayCode.Code1):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 75
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 105
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            if (double_0 >= 1800):
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Strip
                            else:
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.MidPoint
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 150
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 4500
                            self.Approach.Slope1 = 3.33
                            self.Approach.HasSection2 = False
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 20
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = (bool_3) and 150 or 60
                            self.TakeOff.DistFromEND = 30
                            self.TakeOff.DistFromENDFixed = True
                            self.TakeOff.Divergence = 10
                            self.TakeOff.FinalWidth = 380
                            self.TakeOff.Length = 1600
                            self.TakeOff.Slope = 5
                            self.OuterHorizontal.Enabled = False
                            self.NavigationalAid.Enabled = True
                            self.NavigationalAid.Slope = 10
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code2):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 75
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 105
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            if (double_0 >= 1800):
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Strip
                            else:
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.MidPoint
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 150
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 4500
                            self.Approach.Slope1 = 3.33
                            self.Approach.HasSection2 = False
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 20
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = (bool_3) and 150 or 80
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = True
                            self.TakeOff.Divergence = 10
                            self.TakeOff.FinalWidth = 580
                            self.TakeOff.Length = 2500
                            self.TakeOff.Slope = 4
                            self.OuterHorizontal.Enabled = False
                            self.NavigationalAid.Enabled = True
                            self.NavigationalAid.Slope = 10
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code3):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 150
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 105
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            if (double_0 >= 1800):
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Strip
                            else:
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.MidPoint
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 300
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2
                            self.Approach.HasSection2 = True
                            self.Approach.Length2 = 3600
                            self.Approach.Slope2 = 2.5
                            self.Approach.Length3 = 8400
                            self.Approach.TotalLength = 15000
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 180
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = True
                            self.TakeOff.Divergence = 12.5
                            self.TakeOff.FinalWidth = (bool_1) and 1800 or 1200
                            self.TakeOff.Length = 15000
                            self.TakeOff.Slope = (bool_2) and 1.6 or 2
                            if (double_0 < 1100):
                                self.OuterHorizontal.Enabled = False
                            elif (double_0 >= 1860):
                                self.OuterHorizontal.Enabled = True
                                self.OuterHorizontal.Height = 150
                                self.OuterHorizontal.Radius = 15000
                            else:
                                self.OuterHorizontal.Enabled = True
                                self.OuterHorizontal.Height = 150
                                self.OuterHorizontal.Radius = 10000
                            self.NavigationalAid.Enabled = True
                            self.NavigationalAid.Slope = 10
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code4):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 150
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 105
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            if (double_0 >= 1800):
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Strip
                            else:
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.MidPoint
                            self.InnerApproach.Enabled = False
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 300
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2
                            self.Approach.HasSection2 = True
                            self.Approach.Length2 = 3600
                            self.Approach.Slope2 = 2.5
                            self.Approach.Length3 = 8400
                            self.Approach.TotalLength = 15000
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = False
                            self.BalkedLanding.Enabled = False
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 180
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = True
                            self.TakeOff.Divergence = 12.5
                            self.TakeOff.FinalWidth = (bool_1) and 1800 or 1200
                            self.TakeOff.Length = 15000
                            self.TakeOff.Slope = (bool_2) and 1.6 or 2
                            if (double_0 < 1100):
                                self.OuterHorizontal.Enabled = False
                            elif (double_0 >= 1860):
                                self.OuterHorizontal.Enabled = True
                                self.OuterHorizontal.Height = 150
                                self.OuterHorizontal.Radius = 15000
                            else:
                                self.OuterHorizontal.Enabled = True
                                self.OuterHorizontal.Height = 150
                                self.OuterHorizontal.Radius = 10000
                            self.NavigationalAid.Enabled = True
                            self.NavigationalAid.Slope = 10
                            return
                        else:
                            return
                    break
                elif case0(AerodromeSurfacesApproachType.Precision):
                    for case1 in switch (aerodromeSurfacesRunwayCode_0):
                        if case1(AerodromeSurfacesRunwayCode.Code1):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 75
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 105
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            if (double_0 >= 1800):
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Strip
                            else:
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.MidPoint
                            self.InnerApproach.Enabled = True
                            self.InnerApproach.Width = 90
                            self.InnerApproach.DistFromTHR = 60
                            self.InnerApproach.Length = 1500
                            self.InnerApproach.Slope = 2.5
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 150
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2.5
                            self.Approach.HasSection2 = True
                            self.Approach.Length2 = 2500
                            self.Approach.Slope2 = 3
                            self.Approach.Length3 = 9500
                            self.Approach.TotalLength = 15000
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = True
                            self.InnerTransitional.Slope = 40
                            self.BalkedLanding.Enabled = True
                            self.BalkedLanding.InnerEdge = 90
                            self.BalkedLanding.DistFromTHR = 0
                            self.BalkedLanding.DistFromTHRFixed = False
                            self.BalkedLanding.Divergence = 10
                            self.BalkedLanding.Slope = 4
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = (bool_3) and 150 or 60
                            self.TakeOff.DistFromEND = 30
                            self.TakeOff.DistFromENDFixed = True
                            self.TakeOff.Divergence = 10
                            self.TakeOff.FinalWidth = 380
                            self.TakeOff.Length = 1600
                            self.TakeOff.Slope = 5
                            self.OuterHorizontal.Enabled = False
                            self.NavigationalAid.Enabled = True
                            self.NavigationalAid.Slope = 10
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code2):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 75
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 105
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            if (double_0 >= 1800):
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Strip
                            else:
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.MidPoint
                            self.InnerApproach.Enabled = True
                            self.InnerApproach.Width = 90
                            self.InnerApproach.DistFromTHR = 60
                            self.InnerApproach.Length = 1500
                            self.InnerApproach.Slope = 2.5
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 150
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2.5
                            self.Approach.HasSection2 = True
                            self.Approach.Length2 = 2500
                            self.Approach.Slope2 = 3
                            self.Approach.Length3 = 9500
                            self.Approach.TotalLength = 15000
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = True
                            self.InnerTransitional.Slope = 40
                            self.BalkedLanding.Enabled = True
                            self.BalkedLanding.InnerEdge = 90
                            self.BalkedLanding.DistFromTHR = 0
                            self.BalkedLanding.DistFromTHRFixed = False
                            self.BalkedLanding.Divergence = 10
                            self.BalkedLanding.Slope = 4
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = (bool_3) and 150 or 80
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = True
                            self.TakeOff.Divergence = 10
                            self.TakeOff.FinalWidth = 580
                            self.TakeOff.Length = 2500
                            self.TakeOff.Slope = 4
                            self.OuterHorizontal.Enabled = False
                            self.NavigationalAid.Enabled = True
                            self.NavigationalAid.Slope = 10
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code3):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 150
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 105
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            if (double_0 >= 1800):
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Strip
                            else:
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.MidPoint
                            self.InnerApproach.Enabled = True
                            self.InnerApproach.Width = 120
                            self.InnerApproach.DistFromTHR = 60
                            self.InnerApproach.Length = 1500
                            self.InnerApproach.Slope = 2
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 300
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2
                            self.Approach.HasSection2 = True
                            self.Approach.Length2 = 3600
                            self.Approach.Slope2 = 2.5
                            self.Approach.Length3 = 8400
                            self.Approach.TotalLength = 15000
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = True
                            self.InnerTransitional.Slope = 33.3
                            self.BalkedLanding.Enabled = True
                            self.BalkedLanding.InnerEdge = 120
                            self.BalkedLanding.DistFromTHR = 1800
                            self.BalkedLanding.DistFromTHRFixed = True
                            self.BalkedLanding.Divergence = 10
                            self.BalkedLanding.Slope = 3.33
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 180
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = True
                            self.TakeOff.Divergence = 12.5
                            self.TakeOff.FinalWidth = (bool_1) and 1800 or 1200
                            self.TakeOff.Length = 15000
                            self.TakeOff.Slope = (bool_2) and 1.6 or 2
                            if (double_0 < 1100):
                                self.OuterHorizontal.Enabled = False
                            elif (double_0 >= 1860):
                                self.OuterHorizontal.Enabled = True
                                self.OuterHorizontal.Height = 150
                                self.OuterHorizontal.Radius = 15000
                            else:
                                self.OuterHorizontal.Enabled = True
                                self.OuterHorizontal.Height = 150
                                self.OuterHorizontal.Radius = 10000
                            self.NavigationalAid.Enabled = True
                            self.NavigationalAid.Slope = 10
                            return
                        elif case1(AerodromeSurfacesRunwayCode.Code4):
                            self.Strip.Enabled = True
                            self.Strip.Length = 60
                            self.Strip.Width = 150
                            self.Conical.Enabled = True
                            self.Conical.Slope = 5
                            self.Conical.Height = 105
                            self.InnerHorizontal.Enabled = True
                            self.InnerHorizontal.Height = 45
                            if (double_0 >= 1800):
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.Strip
                            else:
                                self.InnerHorizontal.Radius = 4000
                                self.InnerHorizontal.Location = AerodromeSurfacesInnerHorizontalLocation.MidPoint
                            self.InnerApproach.Enabled = True
                            self.InnerApproach.Width = 120
                            self.InnerApproach.DistFromTHR = 60
                            self.InnerApproach.Length = 1500
                            self.InnerApproach.Slope = 2
                            self.Approach.Enabled = True
                            self.Approach.InnerEdge = 300
                            self.Approach.DistFromTHR = 60
                            self.Approach.Divergence = 15
                            self.Approach.Length1 = 3000
                            self.Approach.Slope1 = 2
                            self.Approach.HasSection2 = True
                            self.Approach.Length2 = 3600
                            self.Approach.Slope2 = 2.5
                            self.Approach.Length3 = 8400
                            self.Approach.TotalLength = 15000
                            self.Transitional.Enabled = True
                            self.Transitional.Slope = 14.3
                            self.InnerTransitional.Enabled = True
                            self.InnerTransitional.Slope = 33.3
                            self.BalkedLanding.Enabled = True
                            self.BalkedLanding.InnerEdge = 120
                            self.BalkedLanding.DistFromTHR = 1800
                            self.BalkedLanding.DistFromTHRFixed = True
                            self.BalkedLanding.Divergence = 10
                            self.BalkedLanding.Slope = 3.33
                            self.TakeOff.Enabled = True
                            self.TakeOff.InnerEdge = 180
                            self.TakeOff.DistFromEND = 60
                            self.TakeOff.DistFromENDFixed = True
                            self.TakeOff.Divergence = 12.5
                            self.TakeOff.FinalWidth = (bool_1) and 1800 or 1200
                            self.TakeOff.Length = 15000
                            self.TakeOff.Slope = (bool_2) and 1.6 or 2
                            if (double_0 < 1100):
                                self.OuterHorizontal.Enabled = False
                            elif (double_0 >= 1860):
                                self.OuterHorizontal.Enabled = True
                                self.OuterHorizontal.Height = 150
                                self.OuterHorizontal.Radius = 15000
                            else:
                                self.OuterHorizontal.Enabled = True
                                self.OuterHorizontal.Height = 150
                                self.OuterHorizontal.Radius = 10000
                            self.NavigationalAid.Enabled = True
                            self.NavigationalAid.Slope = 10
                            break
                        else:
                            return
                    break
                else:
                    return

    def method_1(self, dataStream):
        if not isinstance(dataStream, QDataStream):
            return
        dataStream.writeQString(self.name)

        dataStream.writeQString("Approach")
        dataStream.writeBool(self.Approach.Enabled)
        dataStream.writeInt(self.Approach.InnerEdge)
        dataStream.writeInt(self.Approach.DistFromTHR)
        dataStream.writeInt(self.Approach.Divergence)
        dataStream.writeInt(self.Approach.Length1)
        dataStream.writeInt(self.Approach.Slope1)
        dataStream.writeBool(self.Approach.HasSection2)
        dataStream.writeInt(self.Approach.Length2)
        dataStream.writeInt(self.Approach.Slope2)
        dataStream.writeInt(self.Approach.Length3)
        dataStream.writeInt(self.Approach.TotalLength)

        dataStream.writeQString("BalkedLanding")
        dataStream.writeBool(self.BalkedLanding.Enabled)
        dataStream.writeInt(self.BalkedLanding.InnerEdge)
        dataStream.writeInt(self.BalkedLanding.DistFromTHR)
        dataStream.writeBool(self.BalkedLanding.DistFromTHRFixed)
        dataStream.writeInt(self.BalkedLanding.Divergence)
        dataStream.writeInt(self.BalkedLanding.Slope)

        dataStream.writeQString("Conical")
        dataStream.writeBool(self.Conical.Enabled)
        dataStream.writeInt(self.Conical.Slope)
        dataStream.writeInt(self.Conical.Height)

        dataStream.writeQString("InnerApproach")
        dataStream.writeBool(self.InnerApproach.Enabled)
        dataStream.writeInt(self.InnerApproach.Width)
        dataStream.writeInt(self.InnerApproach.DistFromTHR)
        dataStream.writeBool(self.InnerApproach.Length)
        dataStream.writeInt(self.InnerApproach.Slope)

        dataStream.writeQString("InnerHorizontal")
        dataStream.writeBool(self.InnerHorizontal.Enabled)
        dataStream.writeQString(self.InnerHorizontal.Location)
        dataStream.writeInt(self.InnerHorizontal.Height)
        dataStream.writeBool(self.InnerHorizontal.Radius)

        dataStream.writeQString("InnerTransitional")
        dataStream.writeBool(self.InnerTransitional.Enabled)
        dataStream.writeInt(self.InnerTransitional.Slope)

        dataStream.writeQString("NavigationalAid")
        dataStream.writeBool(self.NavigationalAid.Enabled)
        dataStream.writeInt(self.NavigationalAid.Slope)

        dataStream.writeQString("OuterHorizontal")
        dataStream.writeBool(self.OuterHorizontal.Enabled)
        dataStream.writeInt(self.OuterHorizontal.Height)
        dataStream.writeBool(self.OuterHorizontal.Radius)

        dataStream.writeQString("Strip")
        dataStream.writeBool(self.Strip.Enabled)
        dataStream.writeInt(self.Strip.Length)
        dataStream.writeBool(self.Strip.Width)

        dataStream.writeQString("TakeOff")
        dataStream.writeBool(self.TakeOff.Enabled)
        dataStream.writeInt(self.TakeOff.InnerEdge)
        dataStream.writeInt(self.TakeOff.DistFromEND)
        dataStream.writeBool(self.TakeOff.DistFromENDFixed)
        dataStream.writeInt(self.TakeOff.Divergence)
        dataStream.writeInt(self.TakeOff.FinalWidth)
        dataStream.writeInt(self.TakeOff.Length)
        dataStream.writeInt(self.TakeOff.Slope)

        dataStream.writeQString("Transitional")
        dataStream.writeBool(self.Transitional.Enabled)
        dataStream.writeInt(self.Transitional.Slope)
            # binaryWriter_0.Write(Encoding.Default.GetByteCount(this.name))
            # binaryWriter_0.Write(Encoding.Default.GetBytes(this.name))
            # binaryWriter_0.Write(AerodromeSurfacesCriteria.smethod_1(this.approach))
            # binaryWriter_0.Write(AerodromeSurfacesCriteria.smethod_1(this.balkedLanding))
            # binaryWriter_0.Write(AerodromeSurfacesCriteria.smethod_1(this.conical))
            # binaryWriter_0.Write(AerodromeSurfacesCriteria.smethod_1(this.innerApproach))
            # binaryWriter_0.Write(AerodromeSurfacesCriteria.smethod_1(this.innerHorizontal))
            # binaryWriter_0.Write(AerodromeSurfacesCriteria.smethod_1(this.innerTransitional))
            # binaryWriter_0.Write(AerodromeSurfacesCriteria.smethod_1(this.navigationalAid))
            # binaryWriter_0.Write(AerodromeSurfacesCriteria.smethod_1(this.outerHorizontal))
            # binaryWriter_0.Write(AerodromeSurfacesCriteria.smethod_1(this.strip))
            # binaryWriter_0.Write(AerodromeSurfacesCriteria.smethod_1(this.takeOff))
            # binaryWriter_0.Write(AerodromeSurfacesCriteria.smethod_1(this.transitional))

    def method_2(self, string_0, string_1):
        stringBuilder = StringBuilder()
        stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, Captions.NAME, self.Name))
        stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, Captions.STANDARD, str(self.criteria != AerodromeSurfacesCriteriaType.Custom)))
        if (self.Approach.Enabled):
            stringBuilder.AppendLine("{0}{1} {2}".format(string_0, Captions.APPROACH, Captions.SURFACE))
            lENGTHOFINNEREDGE = Captions.LENGTH_OF_INNER_EDGE
            distance = Distance(self.Approach.InnerEdge)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, lENGTHOFINNEREDGE, distance.method_0(":u")))
            dISTANCEFROMRWYTHR = Captions.DISTANCE_FROM_RWY_THR
            distance1 = Distance(self.Approach.DistFromTHR)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, dISTANCEFROMRWYTHR, distance1.method_0(":u")))
            dIVERGENCE = Captions.DIVERGENCE
            angleGradientSlope = AngleGradientSlope(self.Approach.Divergence, AngleGradientSlopeUnits.Percent)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, dIVERGENCE, angleGradientSlope.method_0(":u")))
            fIRSTSECTIONLENGTH = Captions.FIRST_SECTION_LENGTH
            distance2 = Distance(self.Approach.Length1)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, fIRSTSECTIONLENGTH, distance2.method_0(":u")))
            fIRSTSECTIONSLOPE = Captions.FIRST_SECTION_SLOPE
            angleGradientSlope1 = AngleGradientSlope(self.Approach.Slope1, AngleGradientSlopeUnits.Percent)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, fIRSTSECTIONSLOPE, angleGradientSlope1.method_0(":u")))
            if (self.Approach.HasSection2):
                sECONDSECTIONLENGTH = Captions.SECOND_SECTION_LENGTH
                distance3 = Distance(self.Approach.Length2)
                stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, sECONDSECTIONLENGTH, distance3.method_0(":u")))
                sECONDSECTIONSLOPE = Captions.SECOND_SECTION_SLOPE
                angleGradientSlope2 = AngleGradientSlope(self.Approach.Slope2, AngleGradientSlopeUnits.Percent)
                stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, sECONDSECTIONSLOPE, angleGradientSlope2.method_0(":u")))
                hORIZONTALSECTIONLENGTH = Captions.HORIZONTAL_SECTION_LENGTH
                distance4 = Distance(self.Approach.Length3)
                stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, hORIZONTALSECTIONLENGTH, distance4.method_0(":u")))
                tOTALLENGTH = Captions.TOTAL_LENGTH
                distance5 = Distance(self.Approach.TotalLength)
                stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, tOTALLENGTH, distance5.method_0(":u")))
        if (self.BalkedLanding.Enabled):
            stringBuilder.AppendLine("{0}{1} {2}".format(string_0, Captions.BALKED_LANDING, Captions.SURFACE))
            str = Captions.LENGTH_OF_INNER_EDGE
            distance6 = Distance(self.BalkedLanding.InnerEdge)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, str, distance6.method_0(":u")))
            if (MathHelper.smethod_96(self.BalkedLanding.DistFromTHR)):
                stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, Captions.DISTANCE_FROM_RWY_THR, AerodromeSurfacesBalkedLandingFrom.EndOfStrip))
            elif (not self.BalkedLanding.DistFromTHRFixed):
                string1 = [string_1, Captions.DISTANCE_FROM_RWY_THR, AerodromeSurfacesBalkedLandingFrom.EndOfStrip, None ]
                distance7 = Distance(self.BalkedLanding.DistFromTHR)
                string1[3] = distance7.method_0(":u")
                stringBuilder.AppendLine("{0}{1}\t{2} {3}".format(string1))
            else:
                dISTANCEFROMRWYTHR1 = Captions.DISTANCE_FROM_RWY_THR
                distance8 = Distance(self.BalkedLanding.DistFromTHR)
                stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, dISTANCEFROMRWYTHR1, distance8.method_0(":u")))
            dIVERGENCE1 = Captions.DIVERGENCE
            angleGradientSlope3 = AngleGradientSlope(self.BalkedLanding.Divergence, AngleGradientSlopeUnits.Percent)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, dIVERGENCE1, angleGradientSlope3.method_0(":u")))
            sLOPE = Captions.SLOPE
            angleGradientSlope4 = AngleGradientSlope(self.BalkedLanding.Slope, AngleGradientSlopeUnits.Percent)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, sLOPE, angleGradientSlope4.method_0(":u")))
        if (self.Conical.Enabled):
            stringBuilder.AppendLine("{0}{1} {2}".format(string_0, Captions.CONICAL, Captions.SURFACE))
            sLOPE1 = Captions.SLOPE
            angleGradientSlope5 = AngleGradientSlope(self.Conical.Slope, AngleGradientSlopeUnits.Percent)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, sLOPE1, angleGradientSlope5.method_0(":u")))
            hEIGHT = Captions.HEIGHT
            altitude = Altitude(self.Conical.Height)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, hEIGHT, altitude.method_0(":u")))
        if (self.InnerApproach.Enabled):
            stringBuilder.AppendLine("{0}{1} {2}".format(string_0, Captions.INNER_APPROACH, Captions.SURFACE))
            wIDTH = Captions.WIDTH
            distance9 = Distance(self.InnerApproach.Width)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, wIDTH, distance9.method_0(":u")))
            str1 = Captions.DISTANCE_FROM_RWY_THR
            distance10 = Distance(self.InnerApproach.DistFromTHR)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, str1, distance10.method_0(":u")))
            lENGTH = Captions.LENGTH
            distance11 = Distance(self.InnerApproach.Length)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, lENGTH, distance11.method_0(":u")))
            sLOPE2 = Captions.SLOPE
            angleGradientSlope6 = AngleGradientSlope(self.InnerApproach.Slope, AngleGradientSlopeUnits.Percent)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, sLOPE2, angleGradientSlope6.method_0(":u")))
        if (self.InnerHorizontal.Enabled):
            stringBuilder.AppendLine("{0}{1} {2}".format(string_0, Captions.INNER_HORIZONTAL, Captions.SURFACE))
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, Captions.LOCATION, self.InnerHorizontal.Location))
            hEIGHT1 = Captions.HEIGHT
            altitude1 = Altitude(self.InnerHorizontal.Height)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, hEIGHT1, altitude1.method_0(":u")))
            rADIUS = Captions.RADIUS
            distance12 = Distance(self.InnerHorizontal.Radius)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, rADIUS, distance12.method_0(":u")))
        if (self.InnerTransitional.Enabled):
            stringBuilder.AppendLine("{0}{1} {2}".format(string_0, Captions.INNER_TRANSITIONAL, Captions.SURFACE))
            str2 = Captions.SLOPE
            angleGradientSlope7 = AngleGradientSlope(self.InnerTransitional.Slope, AngleGradientSlopeUnits.Percent)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, str2, angleGradientSlope7.method_0(":u")))
        if (self.NavigationalAid.Enabled):
            stringBuilder.AppendLine("{0}{1} {2}".format(string_0, Captions.NAVIGATIONAL_AID_SURFACE, Captions.SURFACE))
            sLOPE3 = Captions.SLOPE
            angleGradientSlope8 = AngleGradientSlope(self.NavigationalAid.Slope, AngleGradientSlopeUnits.Percent)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, sLOPE3, angleGradientSlope8.method_0(":u")))
        if (self.OuterHorizontal.Enabled):
            stringBuilder.AppendLine("{0}{1} {2}".format(string_0, Captions.OUTER_HORIZONTAL, Captions.SURFACE))
            hEIGHT2 = Captions.HEIGHT
            altitude2 = Altitude(self.OuterHorizontal.Height)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, hEIGHT2, altitude2.method_0(":u")))
            rADIUS1 = Captions.RADIUS
            distance13 = Distance(self.OuterHorizontal.Radius)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, rADIUS1, distance13.method_0(":u")))
        if (self.Strip.Enabled):
            stringBuilder.AppendLine("{0}{1} {2}".format(string_0, Captions.STRIP, Captions.SURFACE))
            wIDTH1 = Captions.WIDTH
            distance14 = Distance(self.Strip.Width)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, wIDTH1, distance14.method_0(":u")))
            lENGTH1 = Captions.LENGTH
            distance15 = Distance(self.Strip.Length)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, lENGTH1, distance15.method_0(":u")))
        if (self.TakeOff.Enabled):
            stringBuilder.AppendLine("{0}{1} {2}".format(string_0, Captions.TAKE_OFF_CLIMB, Captions.SURFACE))
            lENGTHOFINNEREDGE1 = Captions.LENGTH_OF_INNER_EDGE
            distance16 = Distance(self.TakeOff.InnerEdge)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, lENGTHOFINNEREDGE1, distance16.method_0(":u")))
            if (not self.TakeOff.DistFromENDFixed):
                objArray = [string_1, Captions.DISTANCE_FROM_RWY_END, AerodromeSurfacesTakeOffFrom.CwyExactly, None ]
                distance17 = Distance(self.TakeOff.DistFromEND)
                objArray[3] = distance17.method_0(":u")
                stringBuilder.AppendLine("{0}{1}\t{2} {3}".format(objArray))
            else:
                string11 = [string_1, Captions.DISTANCE_FROM_RWY_END, AerodromeSurfacesTakeOffFrom.CwyOr, None ]
                distance18 = Distance(self.TakeOff.DistFromEND)
                string11[3] = distance18.method_0(":u")
                stringBuilder.AppendLine("{0}{1}\t{2} {3}".format(string11))
            dIVERGENCE2 = Captions.DIVERGENCE
            angleGradientSlope9 = AngleGradientSlope(self.TakeOff.Divergence, AngleGradientSlopeUnits.Percent)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, dIVERGENCE2, angleGradientSlope9.method_0(":u")))
            fINALWIDTH = Captions.FINAL_WIDTH
            distance19 = Distance(self.TakeOff.FinalWidth)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, fINALWIDTH, distance19.method_0(":u")))
            lENGTH2 = Captions.LENGTH
            distance20 = Distance(self.TakeOff.Length)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, lENGTH2, distance20.method_0(":u")))
            str3 = Captions.SLOPE
            angleGradientSlope10 = AngleGradientSlope(self.TakeOff.Slope, AngleGradientSlopeUnits.Percent)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, str3, angleGradientSlope10.method_0(":u")))
        if (self.Transitional.Enabled):
            stringBuilder.AppendLine("{0}{1} {2}".format(string_0, Captions.TRANSITIONAL, Captions.SURFACE))
            sLOPE4 = Captions.SLOPE
            angleGradientSlope11 = AngleGradientSlope(self.Transitional.Slope, AngleGradientSlopeUnits.Percent)
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_1, sLOPE4, angleGradientSlope11.method_0(":u")))
        return stringBuilder.ToString()

    def ToString(self):
        return self.Name
    @staticmethod
    def smethod_0(dataStream):
        if not isinstance(dataStream, QDataStream):
            return None
        aerodromeSurfacesCriterium = AerodromeSurfacesCriteria(AerodromeSurfacesCriteriaType.Custom)
        aerodromeSurfacesCriterium.Name = dataStream.readQString()

        ####  making ApproachSurfaceCriteria class
        className = dataStream.readQString()
        aerodromeSurfacesCriterium.Approach.Enabled = dataStream.readBool()
        aerodromeSurfacesCriterium.Approach.InnerEdge = dataStream.readInt()
        aerodromeSurfacesCriterium.Approach.DistFromTHR = dataStream.readInt()
        aerodromeSurfacesCriterium.Approach.Divergence = dataStream.readInt()
        aerodromeSurfacesCriterium.Approach.Length1 = dataStream.readInt()
        aerodromeSurfacesCriterium.Approach.Slope1 = dataStream.readInt()
        aerodromeSurfacesCriterium.Approach.HasSection2 = dataStream.readBool()
        aerodromeSurfacesCriterium.Approach.Length2 = dataStream.readInt()
        aerodromeSurfacesCriterium.Approach.Slope2 = dataStream.readInt()
        aerodromeSurfacesCriterium.Approach.Length3 = dataStream.readInt()
        aerodromeSurfacesCriterium.Approach.TotalLength = dataStream.readInt()
        
        className = dataStream.readQString()
        aerodromeSurfacesCriterium.BalkedLanding.Enabled = dataStream.readBool()
        aerodromeSurfacesCriterium.BalkedLanding.InnerEdge = dataStream.readInt()
        aerodromeSurfacesCriterium.BalkedLanding.DistFromTHR = dataStream.readInt()
        aerodromeSurfacesCriterium.BalkedLanding.DistFromTHRFixed = dataStream.readBool()
        aerodromeSurfacesCriterium.BalkedLanding.Divergence = dataStream.readInt()
        aerodromeSurfacesCriterium.BalkedLanding.Slope = dataStream.readInt()
        
        className = dataStream.readQString()
        aerodromeSurfacesCriterium.Conical.Enabled = dataStream.readBool()
        aerodromeSurfacesCriterium.Conical.Slope = dataStream.readInt()
        aerodromeSurfacesCriterium.Conical.Height = dataStream.readInt()
        
        className = dataStream.readQString()
        aerodromeSurfacesCriterium.InnerApproach.Enabled = dataStream.readBool()
        aerodromeSurfacesCriterium.InnerApproach.Width = dataStream.readInt()
        aerodromeSurfacesCriterium.InnerApproach.DistFromTHR = dataStream.readInt()
        aerodromeSurfacesCriterium.InnerApproach.Length = dataStream.readBool()
        aerodromeSurfacesCriterium.InnerApproach.Slope = dataStream.readInt()

        className = dataStream.readQString()
        aerodromeSurfacesCriterium.InnerHorizontal.Enabled = dataStream.readBool()
        aerodromeSurfacesCriterium.InnerHorizontal.Location = dataStream.readQString()
        aerodromeSurfacesCriterium.InnerHorizontal.Height = dataStream.readInt()
        aerodromeSurfacesCriterium.InnerHorizontal.Radius = dataStream.readBool()

        className = dataStream.readQString()
        aerodromeSurfacesCriterium.InnerTransitional.Enabled = dataStream.readBool()
        aerodromeSurfacesCriterium.InnerTransitional.Slope = dataStream.readInt()

        className = dataStream.readQString()
        aerodromeSurfacesCriterium.NavigationalAid.Enabled = dataStream.readBool()
        aerodromeSurfacesCriterium.NavigationalAid.Slope = dataStream.readInt()

        className = dataStream.readQString()
        aerodromeSurfacesCriterium.OuterHorizontal.Enabled = dataStream.readBool()
        aerodromeSurfacesCriterium.OuterHorizontal.Height = dataStream.readInt()
        aerodromeSurfacesCriterium.OuterHorizontal.Radius = dataStream.readBool()

        className = dataStream.readQString()
        aerodromeSurfacesCriterium.Strip.Enabled = dataStream.readBool()
        aerodromeSurfacesCriterium.Strip.Length = dataStream.readInt()
        aerodromeSurfacesCriterium.Strip.Width = dataStream.readBool()

        className = dataStream.readQString()
        aerodromeSurfacesCriterium.TakeOff.Enabled = dataStream.readBool()
        aerodromeSurfacesCriterium.TakeOff.InnerEdge = dataStream.readInt()
        aerodromeSurfacesCriterium.TakeOff.DistFromEND = dataStream.readInt()
        aerodromeSurfacesCriterium.TakeOff.DistFromENDFixed = dataStream.readBool()
        aerodromeSurfacesCriterium.TakeOff.Divergence = dataStream.readInt()
        aerodromeSurfacesCriterium.TakeOff.FinalWidth = dataStream.readInt()
        aerodromeSurfacesCriterium.TakeOff.Length = dataStream.readInt()
        aerodromeSurfacesCriterium.TakeOff.Slope = dataStream.readInt()

        className = dataStream.readQString()
        aerodromeSurfacesCriterium.Transitional.Enabled = dataStream.readBool()
        aerodromeSurfacesCriterium.Transitional.Slope = dataStream.readInt()

        return aerodromeSurfacesCriterium
                


    def get_Name(self):
        if (self.Criteria == AerodromeSurfacesCriteriaType.Custom):
            return self.name
        return self.Criteria
    def set_Name(self, value):
        self.name = value
    Name = property(get_Name, set_Name, None, None)

class AerodromeSurfacesCriteriaList(list):
    fileName = None
    def __init__(self):
        list.__init__(self)

        self.HEADER = "PHXASAC"
        self.VERSION = 2

    @staticmethod
    def AerodromeSurfacesCriteriaList():
        path = ""
        if define.obstaclePath != None:
            path = define.obstaclePath
        elif define.xmlPath != None:
            path = define.xmlPath
        else:
            path = define.appPath
        AerodromeSurfacesCriteriaList.fileName = path + "/phxasac.dat"
    def Add(self, aerodromeSurfacesCriteria):
        self.append(aerodromeSurfacesCriteria)
    def Remove(self, item):
        self.remove(item)
    def method_0(self, iwin32Window_0):
        if QFile.exists(AerodromeSurfacesCriteriaList.fileName):
            fl = QFile.remove(AerodromeSurfacesCriteriaList.fileName)
            f = open(AerodromeSurfacesCriteriaList.fileName, 'w')
            f.flush()
            f.close()

        else:
            f = open(AerodromeSurfacesCriteriaList.fileName, 'w')
            f.flush()
            f.close()

        file0 = QFile(AerodromeSurfacesCriteriaList.fileName)
        file0.open(QIODevice.WriteOnly)
        dataStream = QDataStream(file0)

        dataStream.writeQString(QString("PHXASAC"))
        dataStream.writeInt(2)
        dataStream.writeInt(len(self) - 2)
        for i in range(2, len(self)):
            self[i].method_1(dataStream)
    #     try
    #     {
    #         using (BinaryWriter binaryWriter = new BinaryWriter(File.Open(AerodromeSurfacesCriteriaList.fileName, FileMode.Create, FileAccess.Write, FileShare.Read)))
    #         {
    #             binaryWriter.Write(Encoding.Default.GetBytes("PHXASAC"))
    #             binaryWriter.Write((byte)2)
    #             binaryWriter.Write(base.Count - 2)
    #             for (int i = 2 i < base.Count i++)
    #             {
    #                 base[i].method_1(binaryWriter)
    #             }
    #         }
    #     }
    #     catch (Exception exception1)
    #     {
    #         Exception exception = exception1
    #         ErrorMessageBox.smethod_0(iwin32Window_0, string.Format(Messages.ERR_FAILED_TO_SAVE_CUSTOM_CRITERIA, exception.Message))
    #     }
    # }
#
    def method_1(self):
        self.sort(self.smethod_1)

    @staticmethod
    def smethod_0(iwin32Window_0):
        AerodromeSurfacesCriteriaList.AerodromeSurfacesCriteriaList()
        aerodromeSurfacesCriteriaList = AerodromeSurfacesCriteriaList()
        aerodromeSurfacesCriteriaList.Add(AerodromeSurfacesCriteria(AerodromeSurfacesCriteriaType.Annex14))
        aerodromeSurfacesCriteriaList.Add(AerodromeSurfacesCriteria(AerodromeSurfacesCriteriaType.Cap168))
        if (not QFile.exists(AerodromeSurfacesCriteriaList.fileName)):
            return aerodromeSurfacesCriteriaList
        file0 = QFile(AerodromeSurfacesCriteriaList.fileName)
        file0.open(QIODevice.ReadOnly)
        dataStream = QDataStream(file0)

        str0 = dataStream.readQString()#Encoding.Default.GetString(binaryReader.ReadBytes("PHXASAC".Length))
        num = dataStream.readInt()
        if (not (str0 == "PHXASAC") or num != 2):
            raise Messages.ERR_INVALID_FILE_FORMAT
        num1 = dataStream.readInt()#binaryReader.ReadInt32()
        for i in range(num1):
            aerodromeSurfacesCriteriaList.Add(AerodromeSurfacesCriteria.smethod_0(dataStream))
        # try
        # {
        #     using (BinaryReader binaryReader = new BinaryReader(File.Open(AerodromeSurfacesCriteriaList.fileName, FileMode.Open, FileAccess.Read)))
        #     {
        #         string str = Encoding.Default.GetString(binaryReader.ReadBytes("PHXASAC".Length))
        #         byte num = binaryReader.ReadByte()
        #         if (!(str == "PHXASAC") || num != 2)
        #         {
        #             throw new Exception(Messages.ERR_INVALID_FILE_FORMAT)
        #         }
        #         int num1 = binaryReader.ReadInt32()
        #         for (int i = 0 i < num1 i++)
        #         {
        #             aerodromeSurfacesCriteriaList.Add(AerodromeSurfacesCriteria.smethod_0(binaryReader))
        #         }
        #     }
        # }
        # catch (Exception exception1)
        # {
        #     Exception exception = exception1
        #     ErrorMessageBox.smethod_0(iwin32Window_0, string.Format(Messages.ERR_FAILED_TO_LOAD_CUSTOM_CRITERIA, exception.Message))
        # }
        aerodromeSurfacesCriteriaList.method_1()
        return aerodromeSurfacesCriteriaList

    @staticmethod
    def smethod_1(aerodromeSurfacesCriteria_0, aerodromeSurfacesCriteria_1):
        if (aerodromeSurfacesCriteria_0.Criteria == aerodromeSurfacesCriteria_1.Criteria):
            return 1 if(aerodromeSurfacesCriteria_0.Name == aerodromeSurfacesCriteria_1.Name) else -1
        return 1 if(aerodromeSurfacesCriteria_0.Criteria == aerodromeSurfacesCriteria_1.Criteria) else -1

class HeliportSurfacesCriteria:
    def __init__(self):
        self.Name = ""
        self.TransitionalHeight = 0.0
        self.TransitionalSlope = 0.0

    def vmethod_0(self, string_0, string_1):
        pass

class HeliportSurfacesCriteriaStandard(HeliportSurfacesCriteria):
    def __init__(self):
        HeliportSurfacesCriteria.__init__(self)
        self.Name = "ANNEX14"

    def vmethod_0(self, string_0, string_1):
        # throw new NotImplementedException()
        pass
    def ToString(self):
        return self.Name

class HeliportSurfacesCriteriaNonInstrument(HeliportSurfacesCriteria):
    def __init__(self, heliportSurfacesSlopeCategory_0, heliportSurfacesUsage_0):
        HeliportSurfacesCriteria.__init__(self)
        
        for case in switch(heliportSurfacesSlopeCategory_0):
            if case(HeliportSurfacesSlopeCategory.A):
                self.FromCWY = True
                self.Divergence = 10.0 if(heliportSurfacesUsage_0 == HeliportSurfacesUsage.DayOnly) else 15.0
                self.Length1 = double.NaN()
                self.Slope1 = 4.5
                self.OuterWidth = 120.0
                self.Length2 = double.NaN()
                self.Slope2 = double.NaN()
                self.TotalLength = 3377.77777777778
                break
            elif case(HeliportSurfacesSlopeCategory.B):
                self.FromCWY = True
                self.Divergence = 10.0 if(heliportSurfacesUsage_0 == HeliportSurfacesUsage.DayOnly) else 15.0
                self.Length1 = 245.0
                self.Slope1 = 8.0
                self.Length2 = 830.0
                self.Slope2 = 16.0
                self.OuterWidth = 120.0
                self.TotalLength = 1075.0
                break
            elif case(HeliportSurfacesSlopeCategory.C):
                self.FromCWY = False
                self.Divergence = 10.0 if(heliportSurfacesUsage_0 == HeliportSurfacesUsage.DayOnly) else 15.0
                self.Length1 = 1220.0
                self.Slope1 = 12.5
                self.OuterWidth = 120.0
                self.Length2 = double.NaN()
                self.Slope2 = double.NaN()
                self.TotalLength = 1220.0
                break
        self.TransitionalHeight = 45.0
        self.TransitionalSlope = 50.0
    
    def vmethod_0(self, string_0, string_1):
        pass
        # throw new NotImplementedException()

class HeliportSurfacesCriteriaNonPrecision(HeliportSurfacesCriteria):
    def __init__(self, heliportSurfacesUsage_0):
        HeliportSurfacesCriteria.__init__(self)
        
        self.ApproachDivergence = 16.0
        self.ApproachInnerEdge = 90.0
        self.ApproachLength = 2500.0
        self.ApproachSlope = 3.33
        self.ApproachOuterWidth = 890.0
        self.TransitionalSlope = 20.0
        self.TransitionalHeight = 45.0
        self.TakeOffInnerEdge = 90.0
        self.TakeOffDivergence1 = 30.0
        self.TakeOffLength1 = 2850.0
        self.TakeOffSlope1 = 3.5
        self.TakeOffOuterWidth1 = 1800.0
        self.TakeOffDivergence2 = double.NaN()
        self.TakeOffLength2 = 1510.0
        self.TakeOffSlope2 = 3.5
        self.TakeOffOuterWidth2 = 1800.0
        self.TakeOffDivergence3 = double.NaN()
        self.TakeOffLength3 = 7640.0
        self.TakeOffSlope3 = 2.0
        self.TakeOffOuterWidth3 = 1800.0

    def vmethod_0(self, string_0, string_1):
        pass
        # throw new NotImplementedException()

class HeliportSurfacesCriteriaPrecision(HeliportSurfacesCriteria):
    def __init__(self, heliportSurfacesApproachAngle_0, heliportSurfacesApproachHeight_0):
        HeliportSurfacesCriteria.__init__(self)
        
        for case in switch(heliportSurfacesApproachHeight_0):
            if case(HeliportSurfacesApproachHeight.H90):
                self.ApproachInnerEdge = 90.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 90.0
                self.ApproachDistFromEnd = 60.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 60.0
                self.ApproachDivergence1 = 25.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 25.0
                self.ApproachLengthDivergence1 = 1745.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 870.0
                self.ApproachWidthDivergence1 = 962.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 521.0
                self.ApproachDivergence2 = 15.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 15.0
                self.ApproachLengthDivergence2 = 2793.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 4250.0
                self.ApproachWidthDivergence2 = 1800.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 1800.0
                self.ApproachSlope1 = 2.5 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 5.0
                self.ApproachLengthSlope1 = 3000.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 1500.0
                self.ApproachSlope2 = 3.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 6.0
                self.ApproachLengthSlope2 = 2500.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 1250.0
                self.ApproachTotalLength = 10000.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 8500.0
                break
            elif case(HeliportSurfacesApproachHeight.H60):
                self.ApproachInnerEdge = 90.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 90.0
                self.ApproachDistFromEnd = 60.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 60.0
                self.ApproachDivergence1 = 25.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 25.0
                self.ApproachLengthDivergence1 = 1163.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 580.0
                self.ApproachWidthDivergence1 = 671.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 380.0
                self.ApproachDivergence2 = 15.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 15.0
                self.ApproachLengthDivergence2 = 3763.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 4733.0
                self.ApproachWidthDivergence2 = 1800.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 1800.0
                self.ApproachSlope1 = 2.5 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 5.0
                self.ApproachLengthSlope1 = 3000.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 1500.0
                self.ApproachSlope2 = 3.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 6.0
                self.ApproachLengthSlope2 = 2500.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 1250.0
                self.ApproachTotalLength = 10000.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 8500.0
                break
            elif case(HeliportSurfacesApproachHeight.H45):
                self.ApproachInnerEdge = 90.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 90.0
                self.ApproachDistFromEnd = 60.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 60.0
                self.ApproachDivergence1 = 25.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 25.0
                self.ApproachLengthDivergence1 = 872.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 435.0
                self.ApproachWidthDivergence1 = 526.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 307.5
                self.ApproachDivergence2 = 15.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 15.0
                self.ApproachLengthDivergence2 = 4246.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 4975.0
                self.ApproachWidthDivergence2 = 1800.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 1800.0
                self.ApproachSlope1 = 2.5 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 5.0
                self.ApproachLengthSlope1 = 3000.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 1500.0
                self.ApproachSlope2 = 3.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 6.0
                self.ApproachLengthSlope2 = 2500.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 1250.0
                self.ApproachTotalLength = 10000.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 8500.0
                break
            elif case(HeliportSurfacesApproachHeight.H30):
                self.ApproachInnerEdge = 90.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 90.0
                self.ApproachDistFromEnd = 60.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 60.0
                self.ApproachDivergence1 = 25.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 25.0
                self.ApproachLengthDivergence1 = 581.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 290.0
                self.ApproachWidthDivergence1 = 380.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 235.0
                self.ApproachDivergence2 = 15.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 15.0
                self.ApproachLengthDivergence2 = 4733.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 5217.0
                self.ApproachWidthDivergence2 = 1800.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 1800.0
                self.ApproachSlope1 = 2.5 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 5
                self.ApproachLengthSlope1 = 3000.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 1500
                self.ApproachSlope2 = 3.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 6
                self.ApproachLengthSlope2 = 2500.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 1250.0
                self.ApproachTotalLength = 10000.0 if(heliportSurfacesApproachAngle_0 == HeliportSurfacesApproachAngle.A3) else 8500.0
                break
        self.TransitionalSlope = 14.3
        self.TransitionalHeight = 45.0
        self.TakeOffInnerEdge = 90.0
        self.TakeOffDivergence1 = 30.0
        self.TakeOffLength1 = 2850.0
        self.TakeOffSlope1 = 3.5
        self.TakeOffOuterWidth1 = 1800.0
        self.TakeOffDivergence2 = double.NaN()
        self.TakeOffLength2 = 1510.0
        self.TakeOffSlope2 = 3.5
        self.TakeOffOuterWidth2 = 1800.0
        self.TakeOffDivergence3 = double.NaN()
        self.TakeOffLength3 = 7640.0
        self.TakeOffSlope3 = 2.0
        self.TakeOffOuterWidth3 = 1800.0
    
    def vmethod_0(self, string_0, string_1):
        pass
        # throw new NotImplementedException()


class HeliportSurfacesCriteriaList(list):

    fileName = None
    
    @staticmethod
    def HeliportSurfacesCriteriaList():
        path = ""
        if define.obstaclePath != None:
            path = define.obstaclePath
        elif define.xmlPath != None:
            path = define.xmlPath
        else:
            path = define.appPath
        HeliportSurfacesCriteriaList.fileName = path + "/phxhsac.dat"
        # HeliportSurfacesCriteriaList.fileName = Path.Combine(ApplicationInfo.FolderAsapCommonData, "phxhsac.dat")

    def __init__(self):
        list.__init__(self)
        
        self.HEADER = "PHXHSAC"
        self.VERSION = 2

    def Add(self, item):
        self.append(item)

    def Remove(self, index):
        self.pop(index)


    def method_0(self, iwin32Window_0):
        pass

    def method_1(self):
        # base.Sort(new Comparison<HeliportSurfacesCriteria>(HeliportSurfacesCriteriaList.smethod_1))
        pass

    @staticmethod
    def smethod_0(iwin32Window_0):
        HeliportSurfacesCriteriaList.HeliportSurfacesCriteriaList()
        heliportSurfacesCriteriaList = HeliportSurfacesCriteriaList()
        heliportSurfacesCriteriaList.Add(HeliportSurfacesCriteriaStandard())
        # return new HeliportSurfacesCriteriaList()
        # {
        #     new HeliportSurfacesCriteriaStandard()
        # }
        return heliportSurfacesCriteriaList

    def smethod_1(self, heliportSurfacesCriteria_0, heliportSurfacesCriteria_1):
        if (isinstance(heliportSurfacesCriteria_0 ,HeliportSurfacesCriteriaStandard)):
            return -1
        return heliportSurfacesCriteria_0.Name == heliportSurfacesCriteria_1.Name
    