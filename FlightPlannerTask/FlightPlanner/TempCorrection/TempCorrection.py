
from FlightPlanner.helpers import Altitude, AltitudeUnits
import math
class TempCorrection:
    def __init__(self):
        pass
    @staticmethod
    def smethod_2(altitude_0, altitude_1, altitude_2, double_0):
        num = 0.0065;
        metres = 15 - num * altitude_2.Metres;
        double0 = -(metres - double_0);
        return Altitude(-double0 / -num * math.log(1 - num * altitude_0.Metres / (288.15 - num * altitude_1.Metres)), AltitudeUnits.M);

