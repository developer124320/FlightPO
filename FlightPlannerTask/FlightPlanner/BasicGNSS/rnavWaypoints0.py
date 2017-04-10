'''
Created on Feb 23, 2015

@author: Administrator
'''
from FlightPlanner.types0 import AircraftSpeedCategory, RnavSegmentType, RnavWaypointType, AngleUnits,\
                                RnavFlightPhase, DistanceUnits, RnavCommonWaypoint
from FlightPlanner.helpers0 import MathHelper, Unit, Distance
from FlightPlanner.messages import Messages
import math

class RnavWaypoints:
    
    @staticmethod
    def smethod_0(position_0, position_1):
        return Unit.smethod_1(MathHelper.getBearing(position_0, position_1))         
 
    @staticmethod
    def smethod_1(position_0, position_1):
#         double_0 = Unit.smethod_1(MathHelper.getBearing(position_1, position_0))
        return Unit.smethod_1(MathHelper.getBearing(position_0, position_1))
   
    
    @staticmethod
    def smethod_10(rnavSegmentType_0, aircraftSpeedCategory_0, double_0):
        if (aircraftSpeedCategory_0 == AircraftSpeedCategory.Custom):
            raise UserWarning, "Custom aircraft category is not surported"
        if rnavSegmentType_0 == RnavSegmentType.MissedApproach:
            double0 = double_0 + 7;
        elif rnavSegmentType_0 == RnavSegmentType.Intermediate:
            if (aircraftSpeedCategory_0 != AircraftSpeedCategory.H):
                double0 = double_0 + 10;
            else:
                double0 = double_0 + 30;
        elif rnavSegmentType_0 == RnavSegmentType.Initial1:
            double0 = double_0 - 70;
        elif rnavSegmentType_0 == RnavSegmentType.Initial3:
            double0 = double_0 + 90;
        else:
            if (aircraftSpeedCategory_0 != AircraftSpeedCategory.H):
                double0 = double_0 + 30;
            else:
                double0 = double_0 + 60;
        return round(MathHelper.smethod_3(double0), 1)

    @staticmethod
    def smethod_11(rnavWaypointType_0, distance_0, distance_1, double_0, angleUnits_0):
        if (rnavWaypointType_0 != RnavWaypointType.FlyBy):
            if (rnavWaypointType_0 != RnavWaypointType.FlyOver):
                raise UserWarning, "RNAV WayPoint type not SUPPORTED"
            return distance_0
        if (angleUnits_0 == AngleUnits.Degrees):
            double_0 = Unit.ConvertDegToRad(double_0)
        return Distance(distance_1.Metres * math.tan(double_0 / 2) + distance_0.Metres)

    @staticmethod
    def smethod_12(rnavWaypointType_0, speed_0, speed_1, double_0, double_1, distance_0, distance_1, double_2, angleUnits_0):
        if (rnavWaypointType_0 != RnavWaypointType.FlyBy):
            if (rnavWaypointType_0 != RnavWaypointType.FlyOver):
                raise UserWarning, "RNAV WayPoint type not SUPPORTED"
            double0 = double_0 + double_1;
            num = double0 * (speed_0.MetresPerSecond + speed_1.MetresPerSecond)
            return Distance(-(distance_0.Metres + num))

        if (angleUnits_0 == AngleUnits.Degrees):
            double_2 = Unit.ConvertDegToRad(double_2);
        num1 = min([distance_1.Metres * math.tan(double_2 / 2), distance_1.Metres])
        double01 = double_0 * (speed_0.MetresPerSecond + speed_1.MetresPerSecond)
        return Distance(num1 - distance_0.Metres - double01)

    @staticmethod
    def smethod_13(rnavFlightPhase_0, rnavWaypointType_0, speed_0, speed_1, distance_0, distance_1, double_0, angleUnits_0):
        if (rnavWaypointType_0 != RnavWaypointType.FlyBy):
            if (rnavWaypointType_0 != RnavWaypointType.FlyOver):
                raise UserWarning, "RNAV WayPoint type not SUPPORTED"
            if rnavFlightPhase_0 == RnavFlightPhase.Enroute:
                num1 = 15;
            elif rnavFlightPhase_0 == RnavFlightPhase.SID:
                num1 = 6;
            elif rnavFlightPhase_0 == RnavFlightPhase.STAR:
                raise UserWarning, "RNAV_FLIGHT_PHASE_NOT_SUPPORTED"
            elif rnavFlightPhase_0 == RnavFlightPhase.IafIf or rnavFlightPhase_0 == RnavFlightPhase.Faf:
                num1 = 11;
            elif rnavFlightPhase_0 == RnavFlightPhase.MissedApproach:
                num1 = 6;
            else:
                raise UserWarning, "RNAV_FLIGHT_PHASE_NOT_SUPPORTED"
            num2 = num1 * (speed_0.MetresPerSecond + speed_1.MetresPerSecond)
            return Distance(-(distance_0.Metres + num2))
        if (angleUnits_0 == AngleUnits.Degrees):
            double_0 = Unit.ConvertDegToRad(double_0)
        num3 = min([distance_1.Metres * math.tan(double_0 / 2), distance_1.Metres])
        if rnavFlightPhase_0 == RnavFlightPhase.Enroute:
            num = 10;
        elif rnavFlightPhase_0 == RnavFlightPhase.SID:
            num = 3;
        elif rnavFlightPhase_0 == RnavFlightPhase.STAR:
            raise UserWarning, "RNAV_FLIGHT_PHASE_NOT_SUPPORTED"
        elif rnavFlightPhase_0 == RnavFlightPhase.IafIf or rnavFlightPhase_0 == RnavFlightPhase.Faf:
            num = 6;
        elif rnavFlightPhase_0 == RnavFlightPhase.MissedApproach:
            num = 3;
        else:
            raise UserWarning, "RNAV_FLIGHT_PHASE_NOT_SUPPORTED"
        num4 = num * (speed_0.MetresPerSecond + speed_1.MetresPerSecond);
        return Distance(num3 - distance_0.Metres - num4)
    @staticmethod
    def smethod_2(position_0, position_1):
        return Distance(Unit.ConvertMeterToNM(MathHelper.calcDistance(position_0, position_1)), DistanceUnits.NM)
#     public static Distance smethod_2(Position position_0, Position position_1)
#     {
#         Degrees degree;
#         Degrees degree1;
#         Degrees degree2;
#         Degrees degree3;
#         double num;
#         double num1;
#         Distance distance;
#         Distance distance1;
#         try
#         {
#             if (!position_0.method_1(out degree, out degree1) || !position_1.method_1(out degree2, out degree3))
#             {
#                 distance1 = new Distance(Units.ConvertMeterToNM(MathHelper.calcDistance(position_0.Point3d, position_1.Point3d)), DistanceUnits.NM);
#             }
#             else
#             {
#                 if (!Geo.smethod_4(GeoCalculationType.Ellipsoid, degree, degree1, degree2, degree3, out distance, out num, out num1))
#                 {
#                     throw new Exception(Geo.LastError);
#                 }
#                 distance1 = new Distance(distance.NauticalMiles, DistanceUnits.NM);
#             }
#         }
#         catch (Exception exception1)
#         {
#             Exception exception = exception1;
#             throw new Exception(string.Format(Messages.ERR_FAILED_TO_CALCULATE_DISTANCE_BETWEEN_WAYPOINTS, exception.Message));
#         }
#         return distance1;
#     }
# 
    @staticmethod
    def smethod_3(position_0, double_0, distance_0):
        return MathHelper.distanceBearingPoint(position_0, Unit.ConvertDegToRad(double_0), distance_0.Metres)
        
#         Degrees degree;
#         Degrees degree1;
#         Degrees degree2;
#         Degrees degree3;
#         Position position;
#         try
#         {
#             if (!position_0.method_1(out degree, out degree1))
#             {
#                 Point3d point3d = MathHelper.distanceBearingPoint(position_0.Point3d, Units.ConvertDegToRad(double_0), distance_0.Metres);
#                 position = new Position(point3d.get_X(), point3d.get_Y());
#             }
#             else
#             {
#                 if (!Geo.smethod_5(GeoCalculationType.Ellipsoid, degree, degree1, double_0, distance_0, out degree2, out degree3))
#                 {
#                     throw new Exception(Geo.LastError);
#                 }
#                 position = new Position(degree2, degree3);
#             }
#         }
#         catch (Exception exception1)
#         {
#             Exception exception = exception1;
#             throw new Exception(string.Format(Messages.ERR_FAILED_TO_CALCULATE_WPT_POSITION, exception.Message));
#         }
#         return position;
#     }
    @staticmethod
    def smethod_4(rnavCommonWaypoint_0, aircraftSpeedCategory_0):
        if (aircraftSpeedCategory_0 == AircraftSpeedCategory.Custom):
            raise UserWarning, Messages.CUSTOM_AC_CATEGORY_NOT_SUPPORTED
        if rnavCommonWaypoint_0 == RnavCommonWaypoint.MAHWP:
            return Distance(1, DistanceUnits.NM)
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.MAWP:
            return Distance.NaN()
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.FAWP:
            if (aircraftSpeedCategory_0 == AircraftSpeedCategory.H):
                return Distance(1, DistanceUnits.NM)
            return Distance(3, DistanceUnits.NM)
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.IWP:
            return Distance(2, DistanceUnits.NM)
        else:
            return Distance(1, DistanceUnits.NM)
      
#     public static Distance smethod_5(RnavSegmentType rnavSegmentType_0, AircraftSpeedCategory aircraftSpeedCategory_0)
#     {
#         if (aircraftSpeedCategory_0 == AircraftSpeedCategory.Custom)
#         {
#             throw new ArgumentException(Validations.CUSTOM_AC_CATEGORY_NOT_SUPPORTED);
#         }
#         switch (rnavSegmentType_0)
#         {
#             case RnavSegmentType.MissedApproach:
#             {
#                 return new Distance(1, DistanceUnits.NM);
#             }
#             case RnavSegmentType.FinalApproach:
#             {
#                 if (aircraftSpeedCategory_0 == AircraftSpeedCategory.H)
#                 {
#                     return new Distance(1, DistanceUnits.NM);
#                 }
#                 return new Distance(3, DistanceUnits.NM);
#             }
#             case RnavSegmentType.Intermediate:
#             {
#                 return new Distance(2, DistanceUnits.NM);
#             }
#             default:
#             {
#                 return new Distance(1, DistanceUnits.NM);
#             }
#         }
#     }
# 
    @staticmethod
    def smethod_6(rnavCommonWaypoint_0, aircraftSpeedCategory_0):
        if (aircraftSpeedCategory_0 == AircraftSpeedCategory.Custom):
            raise Messages.CUSTOM_AC_CATEGORY_NOT_SUPPORTED
        if rnavCommonWaypoint_0 == RnavCommonWaypoint.MAHWP:
            return Distance(10, DistanceUnits.NM)
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.MAWP:
            return Distance.NaN()
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.FAWP:
            if (aircraftSpeedCategory_0 == AircraftSpeedCategory.H):
                return Distance(2, DistanceUnits.NM)
            return Distance(5, DistanceUnits.NM)
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.IWP:
            if (aircraftSpeedCategory_0 == AircraftSpeedCategory.H):
                return Distance(3, DistanceUnits.NM)
            return Distance(5, DistanceUnits.NM)
        else:
            if (aircraftSpeedCategory_0 != AircraftSpeedCategory.H):
                pass
            else:
                return Distance(3, DistanceUnits.NM)                
        if (aircraftSpeedCategory_0 != AircraftSpeedCategory.A):
            if (aircraftSpeedCategory_0 != AircraftSpeedCategory.B):
                return Distance(6, DistanceUnits.NM)            
        return Distance(5, DistanceUnits.NM)
    
    @staticmethod
    def smethod_7(rnavCommonWaypoint_0, aircraftSpeedCategory_0, double_0):
        double0 = None
        if (aircraftSpeedCategory_0 == AircraftSpeedCategory.Custom):
            raise Messages.CUSTOM_AC_CATEGORY_NOT_SUPPORTED
        if rnavCommonWaypoint_0 == RnavCommonWaypoint.MAHWP:
            double0 = double_0 - 7
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.MAWP:
            return None
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.FAWP:
            if aircraftSpeedCategory_0 != AircraftSpeedCategory.A and aircraftSpeedCategory_0 != AircraftSpeedCategory.B:
                if (aircraftSpeedCategory_0 != AircraftSpeedCategory.H):
                    double0 = double_0 - 15
                else:
                    double0 = double_0 - 30
            else:
                    double0 = double_0 - 30
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.IWP:
            if (aircraftSpeedCategory_0 != AircraftSpeedCategory.H):
                double0 = double_0 - 10
            else:
                double0 = double_0 - 30
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.IAWP1:
            double0 = double_0 - 90
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.IAWP2:
            if (aircraftSpeedCategory_0 != AircraftSpeedCategory.H):
                double0 = double_0 - 30
                
            else:
                double0 = double_0 - 60
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.IAWP3:
            double0 = double_0 + 70
            
#         default:
#         {
#             goto case RnavCommonWaypoint.IAWP2;
#         }
#         }
        return MathHelper.smethod_3(double0)

    @staticmethod
    def smethod_8(rnavCommonWaypoint_0, aircraftSpeedCategory_0, double_0):
        double0 = None
        if (aircraftSpeedCategory_0 == AircraftSpeedCategory.Custom):
            raise Messages.CUSTOM_AC_CATEGORY_NOT_SUPPORTED
        if rnavCommonWaypoint_0 == RnavCommonWaypoint.MAHWP:
            double0 = double_0 + 7
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.MAWP:
            return None
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.FAWP:
            if (aircraftSpeedCategory_0 != AircraftSpeedCategory.A and aircraftSpeedCategory_0 != AircraftSpeedCategory.B):
                if (aircraftSpeedCategory_0 != AircraftSpeedCategory.H):
                    double0 = double_0 + 15
                else:
                    double0 = double_0 + 30
            else:
                double0 = double_0 + 30
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.IWP:
            if (aircraftSpeedCategory_0 != AircraftSpeedCategory.H):
                double0 = double_0 + 10
            else:
                double0 = double_0 + 30
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.IAWP1:
            double0 = double_0 - 70
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.IAWP2:
            if (aircraftSpeedCategory_0 != AircraftSpeedCategory.H):
                double0 = double_0 + 30
            else:
                double0 = double_0 + 60
        elif rnavCommonWaypoint_0 == RnavCommonWaypoint.IAWP3:
            double0 = double_0 + 90
        return MathHelper.smethod_3(double0)
    
#     public static double smethod_9(RnavSegmentType rnavSegmentType_0, AircraftSpeedCategory aircraftSpeedCategory_0, double double_0)
#     {
#         double double0;
#         if (aircraftSpeedCategory_0 == AircraftSpeedCategory.Custom)
#         {
#             throw new ArgumentException(Validations.CUSTOM_AC_CATEGORY_NOT_SUPPORTED);
#         }
#         switch (rnavSegmentType_0)
#         {
#             case RnavSegmentType.MissedApproach:
#             {
#                 double0 = double_0 - 7;
#                 break;
#             }
#             case RnavSegmentType.FinalApproach:
#             case RnavSegmentType.Initial2:
#             {
#                 if (aircraftSpeedCategory_0 != AircraftSpeedCategory.H)
#                 {
#                     double0 = double_0 - 30;
#                     break;
#                 }
#                 else
#                 {
#                     double0 = double_0 - 60;
#                     break;
#                 }
#             }
#             case RnavSegmentType.Intermediate:
#             {
#                 if (aircraftSpeedCategory_0 != AircraftSpeedCategory.H)
#                 {
#                     double0 = double_0 - 10;
#                     break;
#                 }
#                 else
#                 {
#                     double0 = double_0 - 30;
#                     break;
#                 }
#             }
#             case RnavSegmentType.Initial1:
#             {
#                 double0 = double_0 - 90;
#                 break;
#             }
#             case RnavSegmentType.Initial3:
#             {
#                 double0 = double_0 + 70;
#                 break;
#             }
#             default:
#             {
#                 goto case RnavSegmentType.Initial2;
#             }
#         }
#         return Math.Round(MathHelper.smethod_3(double0), 1);
#     }
# }
