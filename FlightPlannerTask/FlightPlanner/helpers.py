# -*- coding: UTF-8 -*-

from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QString, QStringList, QFile, QTextStream
from PyQt4.QtXml import QDomDocument
from qgis.core import QGis,  QgsCoordinateTransform, QgsPoint
from FlightPlanner.types import  Point3D, AngleUnits, SpeedUnits, AltitudeUnits,\
                                AngleGradientSlopeUnits, DistanceUnits, Enums, Formats
from FlightPlanner.messages import Messages
from FlightPlanner.types import TurnDirection
from FlightPlanner.validations import Validations
from Type.String import String, StringBuilder
from Type.Extensions import Extensions


from qgis.core import QgsGeometry
import math
import define

class EnumHelper:
    @staticmethod
    def Parse(TYPE, nameValue):
        if TYPE == None:
            return None
        attrDict = vars(TYPE)
        if len(attrDict) == 0:
            return None
        for name in attrDict:
            if name == nameValue:
                return attrDict[name]
        return None
    @staticmethod
    def smethod_0(TYPE, nameValue):
        if TYPE == None:
            return None
        attrDict = vars(TYPE)
        if len(attrDict) == 0:
            return None
        for name in attrDict:
            if name == nameValue:
                return attrDict[name]
        return None

    @staticmethod
    def smethod_1(value, TYPE):
        if TYPE == None:
            return None
        attrDict = vars(TYPE)
        if len(attrDict) == 0:
            return None
        for name in attrDict:
            if attrDict[name] == value:
                return name
        return None


class MathHelper:
    def __init__(self):
        pass
    @staticmethod
    def getPointsOfArcWithContactPtAndOutPt(contactPt, contactBearing, outPt, outBearing, turnDirection):
        outBearing = MathHelper.smethod_4(outBearing + math.pi)
        intersectPt = MathHelper.getIntersectionPoint(contactPt, MathHelper.distanceBearingPoint(contactPt, contactBearing, 1000), outPt, MathHelper.distanceBearingPoint(outPt, outBearing, 1000))
        if turnDirection == TurnDirection.Right:
            turnAngleRad = MathHelper.smethod_4(contactBearing + math.pi) - MathHelper.smethod_4(outBearing + math.pi)
            contactPtResult = MathHelper.getIntersectionPoint(contactPt, MathHelper.distanceBearingPoint(contactPt, MathHelper.smethod_4(contactBearing + math.pi / 2 - turnAngleRad / 2), 100),
                                                              outPt, MathHelper.distanceBearingPoint(outPt, outBearing, 100))
            centerPt = MathHelper.getIntersectionPoint(contactPt, MathHelper.distanceBearingPoint(contactPt, MathHelper.smethod_4(contactBearing + math.pi / 2), 100),
                                                       contactPtResult, MathHelper.distanceBearingPoint(contactPtResult, MathHelper.smethod_4(outBearing - math.pi / 2), 100))
            middlePt = MathHelper.distanceBearingPoint(centerPt, MathHelper.getBearing(centerPt, intersectPt), MathHelper.calcDistance(centerPt, contactPt))

            return contactPt, middlePt, contactPtResult
        else:
            turnAngleRad = MathHelper.smethod_4(outBearing + math.pi) - MathHelper.smethod_4(contactBearing + math.pi)
            contactPtResult = MathHelper.getIntersectionPoint(contactPt, MathHelper.distanceBearingPoint(contactPt, MathHelper.smethod_4(contactBearing - (math.pi / 2 - turnAngleRad / 2)), 100),
                                                              outPt, MathHelper.distanceBearingPoint(outPt, outBearing, 100))
            centerPt = MathHelper.getIntersectionPoint(contactPt, MathHelper.distanceBearingPoint(contactPt, MathHelper.smethod_4(contactBearing - math.pi / 2), 100),
                                                       contactPtResult, MathHelper.distanceBearingPoint(contactPtResult, MathHelper.smethod_4(outBearing + math.pi / 2), 100))
            middlePt = MathHelper.distanceBearingPoint(centerPt, MathHelper.getBearing(centerPt, intersectPt), MathHelper.calcDistance(centerPt, contactPt))

            return contactPt, middlePt, contactPtResult

    @staticmethod
    def IsContainedInTwoPoint(point1, point2, containedObject):
        if isinstance(containedObject, QgsPoint) or isinstance(containedObject, Point3D):
            if (point1.x() >= containedObject.x() and point2.x() <= containedObject.x()) or (point1.x() <= containedObject.x() and point2.x() >= containedObject.x()):
                return True
        return False


    @staticmethod
    def calcCenterAngle(bulge):
        #Return value is radian.
        return math.atan(bulge) * 4

    @staticmethod
    def calcRadiusWithTwoPointsAndBulge(startPoint, endPoint, bulge):
        centerAngle = MathHelper.calcCenterAngle(bulge)
        d = MathHelper.calcDistance(startPoint, endPoint) / 2
        h = math.atan(d * math.tan(centerAngle))
        return math.sqrt(d * d + h * h)

    @staticmethod
    def calcCenterPointWithTwoPointsAndBulge(startPoint, endPoint, bulge):
        r = MathHelper.calcRadiusWithTwoPointsAndBulge(startPoint, endPoint, bulge)
        angle = math.pi / 2 - MathHelper.calcCenterAngle(bulge) / 2
        bearing = MathHelper.getBearing(startPoint, endPoint) + angle
        return MathHelper.distanceBearingPoint(startPoint, bearing, r)

    @staticmethod
    def convertMeasureUnits(unit):
        if unit == QGis.Meters:
            define._qgsDistanceArea.setSourceCrs(define._xyCrs)
        else:
            define._qgsDistanceArea.setSourceCrs(define._latLonCrs)

        define._qgsDistanceArea.setEllipsoid(define._xyCrs.ellipsoidAcronym())
        if unit != QGis.Meters:
            define._qgsDistanceArea.setEllipsoidalMode(True)
        else:
            define._qgsDistanceArea.setEllipsoidalMode(False)
    @staticmethod
    def isObtuseTriangle(point3d0, point3d1, point3d2):
        turnDerection = MathHelper.smethod_65([point3d0, point3d1, point3d2])
        if turnDerection == TurnDirection.Nothing:
            return None
        bulge = MathHelper.smethod_60([point3d0, point3d1, point3d2])
        angle = math.atan(bulge / turnDerection) * 4
        if angle > 90:
            return True
        bulge = MathHelper.smethod_60([point3d1, point3d2, point3d0])
        angle = math.atan(bulge / turnDerection) * 4
        if angle > 90:
            return True
        bulge = MathHelper.smethod_60([point3d2, point3d0, point3d1])
        angle = math.atan(bulge / turnDerection) * 4
        if angle > 90:
            return True
        return False



    @staticmethod
    def findArcOrLineInLineGeometry(inputLineGeom, intersectGeom):
        # This method find the arc or line that intersects with geometry named "intersectGeom"  when user input the line named "inputLineGeom".
        #//////// Input Parameter //////////#
            # Here, "intersectGeom" can be Polygon or Line.
            # "inputLineGeom" must be Line containing curves.
        #/////// Return Value /////////////#
            # Here, arc or line has two points and arc has his bulge.
            # The return value is array with start point and end point, bulge.

        pointArray = inputLineGeom.asPolyline()
        dist0 = MathHelper.calcDistance(pointArray[0], pointArray[1])
        equalCount = 0
        findPointArrayInLine = []
        temppointArray = [pointArray[0], pointArray[1]]
        pointCount  = len(pointArray)
        startNum = 0
        endNum = 1
        for i in range(1, pointCount):
            if i == pointCount - 1:
                break
            dist1 = MathHelper.calcDistance(pointArray[i], pointArray[i + 1])
            if round(dist0, 2) == round(dist1, 2):
                temppointArray.append(pointArray[i + 1])
                equalCount += 1

            else:
                if equalCount > 3:
                    endNum = i
                    # c0 = MathHelper.calcDistance(temppointArray[0], temppointArray[1])
                    # c1 = MathHelper.calcDistance(temppointArray[0], pointArray[startNum - 1])
                    # c2 = MathHelper.calcDistance(temppointArray[len(temppointArray) -1], pointArray[endNum + 1])

                    temppointArray.insert(0, pointArray[startNum - 1])
                    temppointArray.append(pointArray[endNum + 1])
                    findPointArrayInLine.append(temppointArray)
                temppointArray = [pointArray[i], pointArray[i + 1]]
                dist0 = dist1
                equalCount = 0
                startNum = i
        if len(findPointArrayInLine) == 0:
            for i in range(1, pointCount):
                line = QgsGeometry.fromPolyline([pointArray[i - 1], pointArray[i]])
                if line.intersects(intersectGeom):
                    startPoint3d = Point3D(pointArray[i - 1].x(), pointArray[i - 1].y())
                    endPoint3d = Point3D(pointArray[i].x(), pointArray[i].y())
                    return [startPoint3d, endPoint3d, 0.0]
            return None
        for ptArray in findPointArrayInLine:
            line = QgsGeometry.fromPolyline(ptArray)
            if line.intersects(intersectGeom):
                startPoint3d = Point3D(ptArray[0].x(), ptArray[0].y())
                endPoint3d = Point3D(ptArray[len(ptArray) - 1].x(), ptArray[len(ptArray) - 1].y())
                middlePoint3d = Point3D(ptArray[int(len(ptArray) / 2)].x(), ptArray[int(len(ptArray) / 2)].y())
                bulge0 = MathHelper.smethod_60(startPoint3d, middlePoint3d, endPoint3d)

                return [startPoint3d, endPoint3d, bulge0]
        return None
    @staticmethod
    def pdtCheckResultToString(isaValue, altitude, iasValue, timeValue = None):
        pdtResultStr = ""
        K = round(171233 * math.pow(288 + isaValue - 0.00198 * altitude.Feet, 0.5)/(math.pow(288 - 0.00198 * altitude.Feet, 2.628)), 4)
        pdtResultStr = "1. K = \t" + str(K) + "\n"
        
        V = Speed.smethod_0(Speed(float(iasValue)), float(isaValue), altitude).Knots
        pdtResultStr += "2. V = \t" + str(V) + "kt\n"
        
        v = V / 3600
        pdtResultStr += "3. v = \t" + str(v) + "NM/s\n"
        
        R = 509.26 / V
        pdtResultStr += "4. R = \t" + str(R)  + unicode("°/s", "utf-8") + "\n"     
        
        r = V / (62.83 * R) 
        pdtResultStr += "5. r = \t" + str(r) + "NM\n" 
        
        h = altitude.Feet / 1000
        pdtResultStr += "6. h = \t" + str(h) + "\n" 
        
        w = 2 * h + 47
        pdtResultStr += "7. w = \t" + str(w) + "kt\n" 
        
        wd = w / 3600
        pdtResultStr += "8. w' = \t" + str(wd) + "NM/s\n" 
        
        E45 = 45 * wd / R
        pdtResultStr += "9. E45' = \t" + str(E45) + "NM\n" 
        
        if timeValue != None:
            t = 60 * timeValue
            pdtResultStr += "10. t = \t" + str(t) + "s\n" 
            
            L = v * t
            pdtResultStr += "11. L = \t" + str(L) + "NM\n"
            
            ab = 5 * v
            pdtResultStr += "12. ab = \t" + str(ab) + "NM\n"
            
            ac = 11 * v
            pdtResultStr += "13. ac = \t" + str(ac) + "NM\n"
            
            gi1 = (t - 5) * v
            pdtResultStr += "14. gi1 = gi3 = \t" + str(gi1) + "NM\n"
            
            gi2 = (t + 21) * v
            pdtResultStr += "15. gi2 = gi4 = \t" + str(gi2) + "NM\n"
            
            Wb = 5 * wd
            pdtResultStr += "16. Wb = \t" + str(Wb) + "NM\n"
            
            Wc = 11 * wd
            pdtResultStr += "17. Wc = \t" + str(Wc) + "NM\n"
            
            Wd = Wc + E45
            pdtResultStr += "18. Wd = \t" + str(Wd) + "NM\n"
            
            We = Wc + 2 * E45
            pdtResultStr += "19. We = \t" + str(We) + "NM\n"
            
            Wf = Wc + 3 * E45
            pdtResultStr += "20. Wf = \t" + str(Wf) + "NM\n"
            
            Wg = Wc + 4 * E45
            pdtResultStr += "21. Wg = \t" + str(Wg) + "NM\n"
            
            Wh = Wb + 4 * E45
            pdtResultStr += "22. Wh = \t" + str(Wh) + "NM\n"
            
            Wo = Wb + 5 * E45
            pdtResultStr += "23. Wo = \t" + str(Wo) + "NM\n"
            
            Wp = Wb + 6 * E45
            pdtResultStr += "24. Wp = \t" + str(Wp) + "NM\n"
            
            Wi1 = (t + 6) * wd + 4 * E45
            pdtResultStr += "25. Wi1 = Wi3 = \t" + str(Wi1) + "NM\n"
            
            Wi2 = Wi1 + 14 * wd
            pdtResultStr += "26. Wi2 = Wi4 = \t" + str(Wi2) + "NM\n"
            
            Wj = Wi2 + E45
            pdtResultStr += "27. Wj = \t" + str(Wj) + "NM\n"
            
            Wk = Wi2 + 2 * E45        
            pdtResultStr += "28. Wk = Wi = \t" + str(Wk) + "NM\n"
            
            Wm = Wi2 + 3 * E45
            pdtResultStr += "29. Wm = \t" + str(Wm) + "NM\n"
            
            Wn3 = Wi1 + 4 * E45
            pdtResultStr += "30. Wn3 = \t" + str(Wn3) + "NM\n"
            
            Wn4 = Wi2 + 4 * E45
            pdtResultStr += "31. Wn4 = \t" + str(Wn4) + "NM\n"
            
            XE = 2 * r + (t + 15) * v + (t + 26 + 195 / R) * wd
            pdtResultStr += "32. XE = \t" + str(XE) + "NM\n"
            
            YE = 11 * v * math.cos(math.pi * 20 / 180) + r * (1 + math.sin(math.pi * 20 / 180)) + (t + 15) * v * math.tan(math.pi * 5 / 180) + (t + 26 + 125 / R) * wd
            pdtResultStr += "33. YE = \t" + str(YE) + "NM"
        
        return pdtResultStr
        
    
    @staticmethod
    def pointInPolygon(polygonArea, point3d, tolerance):
        # polygonArea.append(polygonArea[0])
        # geom = QgsGeometry.fromPolygon([polygonArea])
        # if not geom.contains(point3d):
        #     pass
        # return geom.contains(point3d)
        return MathHelper.smethod_46(polygonArea, point3d, tolerance, True)
    @staticmethod
    def constructCircle(centerPoint, radius, pointCount, startAngle = None, endAngle = None):
        start = 0.0
        end = 0.0
        if startAngle == None:
            start = 0
            end = 2 * math.pi
        else:
            start = startAngle
            end = endAngle
        pointList = []
        for i in range(pointCount):
            angle = (end - start) * i / pointCount
            point = MathHelper.distanceBearingPoint(centerPoint, angle, radius)
            pointList.append(point)
        pointList.append(pointList[0])
        return pointList 
#     @staticmethod
#     def constructArc(centerPoint3d, radius, startAngle, endAngle, pointCount):
    @staticmethod
    def constructArc(centerPoint, radius, startRad, endRad, pointCount):
        pointList = []
        for i in range(pointCount):
            angle = startRad + (endRad - startRad) * i / pointCount
            point = MathHelper.distanceBearingPoint(centerPoint, MathHelper.smethod_4(angle), radius)
            pointList.append(point)
#         pointList.append(pointList[0])
        return pointList

    @staticmethod
    def constructArcWithCenterAngle(centerPoint, radius, startRad, crnterAngleRad, pointCount):
        pointList = []
        for i in range(pointCount):
            angle = startRad + crnterAngleRad * i / pointCount
            point = MathHelper.distanceBearingPoint(centerPoint, MathHelper.smethod_4(angle), radius)
            pointList.append(point)
#         pointList.append(pointList[0])
        return pointList

    @staticmethod
    def constructArcWithThreePointAndOrientation(centerPoint, fromPoint, toPoint, orientation):
        radius = MathHelper.calcDistance(centerPoint, toPoint)
        bearing = MathHelper.getBearing(centerPoint, fromPoint)
        centerAngle = MathHelper.smethod_50(orientation, fromPoint, toPoint, centerPoint)
        middleBearing = None
        if orientation == TurnDirection.Left:
            middleBearing = MathHelper.smethod_4(bearing - centerAngle / 2)
        else:
            middleBearing = MathHelper.smethod_4(bearing + centerAngle / 2)
        middlePoint = MathHelper.distanceBearingPoint(centerPoint, middleBearing, radius)
        bulge = MathHelper.smethod_60(fromPoint, middlePoint, toPoint)
        return fromPoint, toPoint, bulge

    
    @staticmethod
    def smethod_0(double_0, int_0):
        num = pow(10, float(int_0))
        return math.ceil(double_0 * num) / num
    
    @staticmethod
    def smethod_1(double_0, int_0):
        num = pow(10, float(int_0))
        return math.floor(double_0 * num) / num
            
    @staticmethod
    def getArc(startPoint, endPoint, bulge, level, arcPtList):
#         if math.fabs(bulge) > 1:
#             print bulge
        point3d1 = MathHelper.smethod_71(startPoint, endPoint, bulge)
        if point3d1 == None:
            return False
        num1 = MathHelper.smethod_5(bulge) / 2
        if MathHelper.smethod_66(bulge) != TurnDirection.Left:
            num = MathHelper.getBearing(point3d1, startPoint) + num1 
            nextBulge = -math.tan(num1/4)
        else:
            num = MathHelper.getBearing(point3d1, startPoint) - num1
            nextBulge = math.tan(num1/4)
        midPoint = MathHelper.distanceBearingPoint(point3d1, num, MathHelper.calcDistance(point3d1, startPoint))
        if level > 0:
            level -= 1
            MathHelper.getArc(startPoint, midPoint, nextBulge, level, arcPtList)
            MathHelper.getArc(midPoint, endPoint, nextBulge, level, arcPtList)
        else:
            arcPtList.append(midPoint)
    
        
    @staticmethod
    def smethod_46(point3dCollection_0, point3d_0, double_0, bool_0):
        count = len(point3dCollection_0)
        if (count < 3):
            raise UserWarning, Messages.ERR_MINIMUM_3_AREA_POINTS
        try:
            flag = MathHelper.smethod_42(point3dCollection_0, point3d_0, bool_0)
        except:
            return False

        flag1 = flag
        if (flag or double_0 < 0.0001):
            return flag1

        for i in range(0, count):
            if bool_0:
                flag1 = MathHelper.calcDistance(point3d_0, point3dCollection_0[i]) < double_0 
            else:
                flag1 = MathHelper.calcDistance(point3d_0, point3dCollection_0[i]) <= double_0
            if (flag1):
                return True

        for j in range(0, count):
            item = point3dCollection_0[j]
            if j != count - 1:
                point3d = point3dCollection_0[j + 1]
            else:
                point3d = point3dCollection_0[0]
                
            if (item.x() != point3d.x() or item.y() != point3d.y()):
                point3d1 = MathHelper.getIntersectionPoint(item, point3d, point3d_0, MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(item, point3d) + math.pi / 2, 1))
                num = MathHelper.calcDistance(item, point3d)
                if (MathHelper.calcDistance(point3d1, item) <= num and MathHelper.calcDistance(point3d1, point3d) <= num):
                    num = MathHelper.calcDistance(point3d_0, point3d1)
                    if bool_0:
                        flag1 = num < double_0 
                    else:
                        flag1 = num <= double_0
                    if (flag1):
                        return True
        return False

    @staticmethod
    def calcDistance(point3d1, point3d2):
        distance = define._qgsDistanceArea.measureLine(QgsPoint(point3d1.x(), point3d1.y()), QgsPoint(point3d2.x(), point3d2.y()))
        return distance
    @staticmethod
    def calcDistance0(point3d1, point3d2):
        x = point3d1.get_X() - point3d2.get_X()
        y = point3d1.get_Y() - point3d2.get_Y()
        return math.sqrt(x * x + y * y)
    @staticmethod
    def getProjectionPoint(point1, point2, otherPoint):
        num = MathHelper.getBearing(point1, point2)
        num1 = MathHelper.getBearing(point1, otherPoint)
        turn = MathHelper.smethod_63(num, num1, AngleUnits.Radians)
        point3 = MathHelper.distanceBearingPoint(otherPoint, num + turn * math.pi / 2, 100)
        return MathHelper.getIntersectionPoint(point1, point2, otherPoint, point3)
        
    @staticmethod
    def pair(ptlist): 
        '''Iterate over pairs in a list ''' 
        for i in range(1, len(ptlist)): 
            yield ptlist[i-1], ptlist[i] 
    
    @staticmethod
    def getPointAtDist(line, distance):
        sum = 0
        i = 0
        for point in line:
            if i == 0:
                i += 1
                continue
            sum += MathHelper.calcDistance(line[i-1], point)
            i += 1
        if round(distance, 4) > round(sum, 4):
            return MathHelper.distanceBearingPoint(line[len(line) - 1], MathHelper.getBearing(line[len(line) - 2], line[len(line) - 1]), distance - sum)
        elif round(distance, 4) == round(sum, 4):
            return line[len(line) - 1]
        sum = 0
        for seg_start, seg_end in MathHelper.pair(line): 
            segmentLength = MathHelper.calcDistance(seg_start, seg_end)
            if sum + segmentLength >= distance : # correction of the floating point precision errors
                remainder = distance - sum
                bearing = MathHelper.getBearing(seg_start, seg_end)
                return MathHelper.distanceBearingPoint(seg_start, bearing, remainder)
            else:
                sum = sum + segmentLength
        return None
    @staticmethod  
    def distanceAlongLine(line,point):
        if isinstance(line, QgsGeometry):
            line = line.asPolyline() 
            
        polyline = QgsGeometry.fromPolyline(line)
        vtx, at, before, after, distance = polyline.closestVertex(point)
        vtxBefore = polyline.vertexAt(before)
        distBefore = QgsGeometry.fromPolyline([vtxBefore, vtx]).distance(QgsGeometry.fromPoint(point))
        if distBefore < distance:
            pointList = line[0:before + 1]
        else:
            pointList = line[0:at + 1]
        pointList.append(point)
        if len(pointList) < 2:
            pointList = [line[0], point]

        length = 0.0
        for i in range(1, len(pointList)):
            length += MathHelper.calcDistance(pointList[i - 1], pointList[i])
        #length = QgsGeometry.fromPolyline(pointList).length()
        return length
    
    @staticmethod  
    def degree2DegreeMinuteSecond(double_Degree):
        degreeInt = int(double_Degree)
        minuteDouble = (double_Degree - degreeInt) * 60
        minuteInt = int(minuteDouble)
        secondDouble = (minuteDouble - minuteInt) * 60
        
        return str(degreeInt) + unicode("° ", "utf-8") + str(minuteInt) + "' " + str(secondDouble) + "\"" 
    
    
    @staticmethod
    def smethod_112(double_0, double_1, double_2, angleUnits_0):
        if (angleUnits_0 == AngleUnits.Degrees):
            double_0 = MathHelper.smethod_3(double_0)
            double_1 = MathHelper.smethod_3(double_1 - 0.1)
            double_2 = MathHelper.smethod_3(double_2 + 0.1)
            if (double_2 > double_1):
                if (double_0 < double_1):
                    return False
                if double_0 <= double_2:
                    return True
                else:
                    return False
            if (double_0 >= double_1 and double_0 <= 360):
                return True
            if (double_0 < 0):
                return False
            if double_0 <= double_2:
                return True
            else:
                return False
        double_0 = MathHelper.smethod_4(double_0)
        double_1 = MathHelper.smethod_4(double_1 - 0.1)
        double_2 = MathHelper.smethod_4(double_2 + 0.1)
        if (double_2 > double_1):
            if (double_0 < double_1):
                return False
            if double_0 <= double_2:
                return True
            else:
                return False
        if (double_0 >= double_1 and double_0 <= math.pi * 2):
            return True
        if (double_0 < 0):
            return False        
        if double_0 <= double_2:
            return True
        else:
            return False
    
    # MathHelper : public static double smethod_3(double double_0)
    @staticmethod
    def smethod_3(double_0):
        while (double_0 >= 360):
            double_0 = double_0 - 360
        while (double_0 < 0):
            double_0 = double_0 + 360
        return double_0

    # MathHelper : public static bool smethod_135(double double_0, double double_1, double double_2, AngleUnits AngleUnits_0)
    @staticmethod
    def smethod_130(double_0, double_1):
        double_0 = MathHelper.smethod_4(double_0)
        double_1 = MathHelper.smethod_4(double_1)
        if (double_0 - double_1 >= 0):
            if (double_0 - double_1 <= math.pi):
                return False
        elif (double_1 - double_0 > math.pi):
            return False
        return True
    @staticmethod
    def smethod_132(point3dCollection_0):
        item = None
        point3d = None
        point3dCollection = []
        count = len(point3dCollection_0)
        i = 0
        while i < count:
            item1 = point3dCollection_0[i]
            if i == count - 1:
                item = point3dCollection_0[0]
            else:
                item = point3dCollection_0[i + 1]
            if (item1 != item):
                point3dCollection.append(item1)
            i += 1

        count = len(point3dCollection)
        if (count < 3):
            raise UserWarning, "ERR_MINIMUM_3_AREA_POINTS"
        j = 1
        while j < count:
            point3d1 = point3dCollection[j - 1]
            item2 = point3dCollection[j]
            k = j
            while k < count:
                point3d2 = point3dCollection[k]
                if k == count - 1:
                    if MathHelper.smethod_30(point3d1, item2, point3d2, point3dCollection[0] , False):
                        return True
                else:
                    if MathHelper.smethod_30(point3d1, item2, point3d2, point3dCollection[k + 1], False):
                        return True
                k += 1
                
            if j == count - 1:
                point3d = point3dCollection[0]
            else:
                point3d = point3dCollection[j + 1]
                
            if MathHelper.smethod_98(MathHelper.smethod_76(MathHelper.getBearing(point3d1, item2), MathHelper.getBearing(item2, point3d), "Radians"), math.pi):
                return True
            j += 1
        return MathHelper.smethod_65(point3dCollection) == TurnDirection.Nothing

    
    @staticmethod
    def smethod_135(double_0, double_1, double_2, AngleUnits_0):
        if (AngleUnits_0 == "Degrees"):
            double_0 = MathHelper.smethod_3(double_0)
            num = MathHelper.smethod_3(double_1 - double_2)
            num1 = MathHelper.smethod_3(double_1 + double_2)
            if (num1 > num):
                if (double_0 < num):
                    return False
                return double_0 <= num1
            if (double_0 >= num and double_0 <= 360):
                return True
            if (double_0 < 0):
                return False
            return double_0 <= num1
        double_0 = MathHelper.smethod_4(double_0)
        num2 = MathHelper.smethod_4(double_1 - double_2)
        num3 = MathHelper.smethod_4(double_1 + double_2)
        if (num3 > num2):
            if (double_0 < num2):
                return False
            return double_0 <= num3
        if (double_0 >= num2 and double_0 <= math.pi * 2):
            return True
        if (double_0 < 0):
            return False
        return double_0 <= num3

#     public static bool smethod_136(double double_0, AngleUnits angleUnits_0)
#     {
    @staticmethod
    def smethod_136(double_0, angleUnits_0):
        num = 1E-07
        if (angleUnits_0 != AngleUnits.Degrees):
            double_0 = MathHelper.smethod_4(double_0)
            if (MathHelper.smethod_96(double_0) or MathHelper.smethod_99(double_0, math.pi * 2, num)):
                return True
            if (double_0 <= 0):
                return False
            return double_0 < math.pi
        double_0 = MathHelper.smethod_3(double_0)
        if (MathHelper.smethod_97(double_0, num) or MathHelper.smethod_99(double_0, 360, num)):
            return True
        if (double_0 <= 0):
            return False
        return double_0 < 180

#         public static Point3dCollection smethod_137(Point3d point3d_0, Point3d point3d_1, double double_0, double double_1, int int_0, TurnDirection turnDirection_0)
#         {
    @staticmethod
    def smethod_137(point3d_0, point3d_1, double_0, double_1, int_0, turnDirection_0):

        double1 = (int)(double_1 / (math.pi / 2 / int_0)) + 1
        num = double_1 / double1
        if (turnDirection_0 == TurnDirection.Left):
            num = num * -1
        num1 = MathHelper.getBearing(point3d_1, point3d_0)
        point3dCollection = []
        i = 0
        while (i < double1):
            point3dCollection.append(MathHelper.distanceBearingPoint(point3d_1, num1 + num * i, double_0))
            i += 1
        return point3dCollection

#         public static Point3dCollection smethod_138(Point3d point3d_0, Point3d point3d_1, double double_0, double double_1, int int_0, TurnDirection turnDirection_0)
#         {
    @staticmethod
    def smethod_138(point3d_0, point3d_1, double_0, double_1, int_0, turnDirection_0):

        double1 = (int)(double_1 / (math.pi / 2 / int_0)) + 1
        double11 = double_1 / double1
        if (turnDirection_0 == TurnDirection.Left):
            double11 = double11 * -1
        num2 = MathHelper.getBearing(point3d_1, point3d_0)
        if (turnDirection_0 != TurnDirection.Left):
            num = math.pi / 2
            num1 = -math.pi / 2
        else:
            num = -math.pi / 2
            num1 = math.pi / 2
        point3dCollection = []
        point3dCollection.append(point3d_0)
        point3d0 = point3d_0
        point3d3 = MathHelper.distanceBearingPoint(point3d0, num2 + num, 100)
        i = 1
        while (i < double1):
            point3d = MathHelper.distanceBearingPoint(point3d_1, num2 + double11 * i, double_0)
            point3d1 = MathHelper.distanceBearingPoint(point3d, num2 + double11 * i + num1, double_0)
            point3d2 = MathHelper.getIntersectionPoint(point3d0, point3d3, point3d, point3d1)
            point3dCollection.append(point3d2)
            point3dCollection.append(point3d)
            point3d0 = point3d
            point3d3 = MathHelper.distanceBearingPoint(point3d0, num2 + double11 * i + num, 100)
            i += 1
            
        point3d = MathHelper.distanceBearingPoint(point3d_1, num2 + double11 * double1, double_0)
        point3d1 = MathHelper.distanceBearingPoint(point3d, num2 + double11 * double1 + num1, double_0)
        point3d2 = MathHelper.getIntersectionPoint(point3d0, point3d3, point3d, point3d1)
        point3dCollection.append(point3d2)
        return point3dCollection
    
    @staticmethod
    def smethod_139(point3d_0, point3d_1, point3d_2, int_0):
        num = MathHelper.getBearing(point3d_0, point3d_1)
        num1 = MathHelper.getBearing(point3d_1, point3d_2)
        point3dCollection = []
        point3d = MathHelper.smethod_68(point3d_0, point3d_1, point3d_2)
        if (point3d != None):
            num2 = MathHelper.calcDistance(point3d, point3d_0)
            num3 = MathHelper.getBearing(point3d, point3d_0)
            turnDirection = MathHelper.smethod_63(num, num1, AngleUnits.Radians)
            num4 = MathHelper.smethod_48(point3d_0, point3d_1, point3d_2)
            point3d = point3d.smethod_167(point3d_0.get_Z())
            if (int_0 < 0):
                int_0 = int(math.trunc(num2 * num4 / 100) + 1)
            for i in range(int_0):
                int0 = num4 * (float(i) / float(int_0))
                if (turnDirection != TurnDirection.Left):
                    point3dCollection.append(MathHelper.distanceBearingPoint(point3d, num3 + int0, num2))
                else:
                    point3dCollection.append(MathHelper.distanceBearingPoint(point3d, num3 - int0, num2))
        return (point3dCollection, int_0)
    
    @staticmethod
    def smethod_140(double_0, point3d_0, point3d_1, int_0):
        point3d = None
        num = None
        num1 = MathHelper.getBearing(point3d_0, point3d_1)
        num2 = MathHelper.calcDistance(point3d_0, point3d_1) / 2
        turnDirection = MathHelper.smethod_63(double_0, num1, AngleUnits.Radians)
        num = -1 if(turnDirection != TurnDirection.Right) else 1
        point3d1 = MathHelper.distanceBearingPoint(point3d_0, double_0 + math.pi / 2 * float(num), 100)
        point3d2 = MathHelper.distanceBearingPoint(point3d_0, num1, num2)
        point3d3 = MathHelper.distanceBearingPoint(point3d2, num1 + math.pi / 2 * float(num), 100)
        point3dCollection = []
        point3d = MathHelper.getIntersectionPoint(point3d_0, point3d1, point3d2, point3d3)
        if (point3d != None):
            num3 = MathHelper.calcDistance(point3d, point3d_0)
            num4 = MathHelper.getBearing(point3d, point3d_0)
            num5 = MathHelper.smethod_50(turnDirection, point3d_0, point3d_1, point3d)
            point3d = point3d.smethod_167(point3d_0.get_Z())
            if (int_0 < 0):
                int_0 = int(math.trunc(num3 * num5 / 100) + 1)
            for i in range(int_0):
                int0 = num5 * (float(i) / float(int_0))
                if (turnDirection != TurnDirection.Left):
                    point3dCollection.append(MathHelper.distanceBearingPoint(point3d, num4 + int0, num3))
                else:
                    point3dCollection.append(MathHelper.distanceBearingPoint(point3d, num4 - int0, num3))
        return (point3dCollection, int_0)
    
    @staticmethod
    def smethod_91(point3d_0, double_0, point3d_1, double_1, turnDirection_0):
        num = MathHelper.calcDistance(point3d_0, point3d_1)
        num1 = 0
        if (not MathHelper.smethod_96(num)):
            if (double_1 - double_0) / num > 1 or (double_1 - double_0) / num < -1:
                num1 = 1
            else:
                num1 = math.fabs(math.asin((double_1 - double_0) / num))
        if (double_1 > double_0):
            if (turnDirection_0 == TurnDirection.Left):
                point3d_2 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_1) + num1 + Unit.ConvertDegToRad(90), double_0)
                point3d_3 = MathHelper.distanceBearingPoint(point3d_1, MathHelper.getBearing(point3d_0, point3d_1) + num1 + Unit.ConvertDegToRad(90), double_1)
                return (point3d_2, point3d_3)
            point3d_2 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_1) - num1 - Unit.ConvertDegToRad(90), double_0)
            point3d_3 = MathHelper.distanceBearingPoint(point3d_1, MathHelper.getBearing(point3d_0, point3d_1) - num1 - Unit.ConvertDegToRad(90), double_1)
            return (point3d_2, point3d_3)
        if (turnDirection_0 == TurnDirection.Left):
            point3d_2 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_1) - num1 + Unit.ConvertDegToRad(90), double_0)
            point3d_3 = MathHelper.distanceBearingPoint(point3d_1, MathHelper.getBearing(point3d_0, point3d_1) - num1 + Unit.ConvertDegToRad(90), double_1)
            return (point3d_2, point3d_3)
        point3d_2 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_1) + num1 - Unit.ConvertDegToRad(90), double_0)
        point3d_3 = MathHelper.distanceBearingPoint(point3d_1, MathHelper.getBearing(point3d_0, point3d_1) + num1 - Unit.ConvertDegToRad(90), double_1)
        return (point3d_2, point3d_3)
    
    @staticmethod
    def smethod_93(turnDirection_0, point3d_0, point3d_1, point3d_2):
        if (turnDirection_0 == TurnDirection.Nothing):
            QMessageBox.warning(None, "Warning", Messages.ERR_INVALID_TURN_DIRECTION_VALUE)
#             throw new ArgumentException(Messages.ERR_INVALID_TURN_DIRECTION_VALUE, "direction")
            return
        num = MathHelper.smethod_50(turnDirection_0, point3d_0, point3d_1, point3d_2) / 2
        if (turnDirection_0 == TurnDirection.Left):
            return MathHelper.distanceBearingPoint(point3d_2, MathHelper.getBearing(point3d_2, point3d_0) - num, MathHelper.calcDistance(point3d_2, point3d_0))
        return MathHelper.distanceBearingPoint(point3d_2, MathHelper.getBearing(point3d_2, point3d_0) + num, MathHelper.calcDistance(point3d_2, point3d_0))
      
    @staticmethod
    def smethod_96(double_0):
        return math.fabs(double_0) <= 0.00000001

    @staticmethod
    def smethod_97(double_0, double_1):
        return math.fabs(double_0) <= double_1

    # MathHelper : public static bool smethod_98(double double_0, double double_1)
    @staticmethod
    def smethod_98(double_0, double_1):
        return math.fabs(double_0 - double_1) <= 0.000000008
    
    @staticmethod
    def smethod_99(double_0, double_1, double_2):
        return math.fabs(double_0 - double_1) <= double_2
    
    @staticmethod
    def smethod_100(point2d_0, point2d_1):
        if (math.fabs(point2d_1.get_X() - point2d_0.get_X()) > 1E-08):
            return False
        return math.fabs(point2d_1.get_Y() - point2d_0.get_Y()) <= 1E-08
    @staticmethod
    def smethod_102(point3d_0, point3d_1):
        if (math.fabs(point3d_1.get_X() - point3d_0.get_X()) > 1E-08):
            return False
        return math.fabs(point3d_1.get_Y() - point3d_0.get_Y()) <= 1E-08

    # public static double MathHelper.getBearing(Point3D point3d_0, Point3D point3d_1)
    @staticmethod
    def getBearing(point3d_0, point3d_1, unit = None):
        if unit != None:
            MathHelper.convertMeasureUnits(unit)
        if point3d_0 == None or point3d_1 == None:
            MathHelper.convertMeasureUnits(define._units)
            return 0
        bearing = define._qgsDistanceArea.bearing(point3d_0, point3d_1)
        if bearing < 0:
            bearing += 2 * math.pi
        if unit != None:
            MathHelper.convertMeasureUnits(define._units)
        return bearing

    @staticmethod
    def getVerticalLine(lineWithTwoPoint3d, point3d, length = None):
        bearing = MathHelper.getBearing(lineWithTwoPoint3d[0], lineWithTwoPoint3d[1])
        point3d1 = MathHelper.distanceBearingPoint(point3d, bearing + math.pi / 2, length)
        point3d2 = MathHelper.distanceBearingPoint(point3d, bearing - math.pi / 2, length)
        return (point3d1, point3d2)
        
    @staticmethod
    def GetInsidePointForSegment(ipStPoint, ipEdPoint, radio):
        # double stX, stY, edX, edY, resX, resY
        stX = ipStPoint.x()
        stY = ipStPoint.y()
        edX = ipEdPoint.x()
        edY = ipEdPoint.y()

        resX = (radio * stX + edX) / (radio + 1)
        resY = (radio * stY + edY) / (radio + 1)

        # respoint = new PointClass()
        # respoint.SpatialReference = ipStPoint.SpatialReference

        return Point3D(resX, resY)
    @staticmethod
    def getPointsLeftWithLine(polylineArea, points):
        polyline = QgsGeometry.fromPolyline(polylineArea.method_14())
        result, geomList, ptList = polyline.splitGeometry(points, False)
        if result != 0 or len(geomList) == 0:
            return None
        return geomList[0].asPolyline(), ptList

    @staticmethod
    def getIntersectionPointWithTwoLine(point3d_0, point3d_1, point3d_2, point3d_3):
        line1 = QgsGeometry.fromPolyline([point3d_0, point3d_1])
        line2 = QgsGeometry.fromPolyline([point3d_2, point3d_3])
        if not line1.intersects(line2):
            return None
        geom = line1.intersection(line2)
        return geom.asPoint()

    @staticmethod
    def getIntersectionPoint(point3d_0, point3d_1, point3d_2, point3d_3):
        if point3d_1 == None:
            pass

        x = point3d_1.x() - point3d_0.x()
        y = point3d_1.y() - point3d_0.y()
        num = point3d_2.x() - point3d_0.x()
        y1 = point3d_2.y() - point3d_0.y()
        x1 = point3d_3.x() - point3d_2.x()
        num1 = point3d_3.y() - point3d_2.y()
        if (MathHelper.smethod_98(num1, 0)):
            if (MathHelper.smethod_98(y, 0)):
                return None
            num2 = y1
            num3 = x / y * y1
            point3d_4 = Point3D(point3d_0.x() + num3, point3d_0.y() + num2, 0)
            return point3d_4
        if (MathHelper.smethod_98(x1, 0)):
            if (MathHelper.smethod_98(x, 0)):
                return None
            num4 = y / x * num
            num5 = num
            point3d_4 = Point3D(point3d_0.x() + num5, point3d_0.y() + num4, 0)
            return point3d_4
        if (MathHelper.smethod_98(y, 0)):
            num6 = 0
            num7 = num - x1 / num1 * y1
            point3d_4 = Point3D(point3d_0.x() + num7, point3d_0.y() + num6, 0)
            return point3d_4
        if (MathHelper.smethod_98(x, 0)):
            num8 = y1 - num1 / x1 * num
            num9 = 0
            point3d_4 = Point3D(point3d_0.x() + num9, point3d_0.y() + num8, 0)
            return point3d_4

        if (MathHelper.smethod_98(y / x, num1 / x1)):
        # if (MathHelper.smethod_99(y / x, num1 / x1, 0.01)):
            return None
        num10 = (num - x1 / num1 * y1) / (1 - x1 / num1 * (y / x))
        num11 = y / x * num10
        point3d_4 = Point3D(point3d_0.x() + num10, point3d_0.y() + num11, 0)
        return point3d_4


    # MathHelper.smethod_34
    # return String
    # input Point3D, Point3D, Point3D, double, out Point3D, out Point3D
    @staticmethod
    def smethod_34(point3d_0, point3d_1, point3d_2, double_0, listPoints):
        '''
            calculate intersection points of line segment point3d_0 to point3d_1 and circle with point3d_2 as centre, double_0 as radius.
        '''
        if (double_0 <= 0):
            return "None"
        num = MathHelper.getBearing(point3d_0, point3d_1)
        point3d = MathHelper.getIntersectionPoint(point3d_0, point3d_1, point3d_2, MathHelper.distanceBearingPoint(point3d_2, num + math.pi / 2, 100.0))
        if point3d == None:
            return "None"
        num1 = MathHelper.calcDistance(point3d, point3d_2)
        if (num1 == double_0):
            listPoints.append(point3d)
            listPoints.append(point3d)
            return "Tangent"
        if (num1 >= double_0):
            listPoints.append(Point3D.get_Origin())
            listPoints.append(Point3D.get_Origin())
            return "None"
        num2 = math.sqrt(double_0 * double_0 - num1 * num1)
        point3d_3 = MathHelper.distanceBearingPoint(point3d, num + math.pi, num2)
        point3d_4 = MathHelper.distanceBearingPoint(point3d, num, num2)
        listPoints.append(point3d_3)
        listPoints.append(point3d_4)
        return "Intersection"
    
    # MathHelper.smethod_4()
    @staticmethod
    def smethod_4(radian):
        while (radian >= math.pi * 2):
            radian = radian - math.pi * 2
        while (radian < 0):
            radian = radian + math.pi * 2
        return radian

    @staticmethod
    def smethod_5(double_0):
        return math.atan(math.fabs(double_0)) * 4

    @staticmethod
    def smethod_21(point3d_0, point3d_1, bool_0):
        if (not bool_0):
            x = point3d_0.get_X() - point3d_1.get_X()
            y = point3d_0.get_Y() - point3d_1.get_Y()
            return math.sqrt(x * x + y * y)
        num = point3d_0.get_X() - point3d_1.get_X()
        y1 = point3d_0.get_Y() - point3d_1.get_Y()
        z = point3d_0.get_Z() - point3d_1.get_Z()
        return math.sqrt(math.pow(math.sqrt(num * num + y1 * y1), 2) + z * z)
    
    @staticmethod
    def smethod_26(point3d_0, point3d_1):
        return MathHelper.smethod_4((math.pi * 5  /  2) - MathHelper.getBearing(point3d_0, point3d_1))
    
    @staticmethod
    def smethod_48(point3d_0, point3d_1, point3d_2):
        point3d = MathHelper.smethod_68(point3d_0, point3d_1, point3d_2)
        if (point3d == None ):
            return 0
        num = MathHelper.getBearing(point3d_0, point3d_1)
        num1 = MathHelper.getBearing(point3d_1, point3d_2)
        turnDirection = MathHelper.smethod_63(num, num1, AngleUnits.Radians)
        num2 = MathHelper.getBearing(point3d, point3d_0)
        num3 = MathHelper.getBearing(point3d, point3d_2)
        if (turnDirection == TurnDirection.Left):
            if (num2 >= num3):
                return num2 - num3
            return math.pi * 2 - num3 + num2
        if (num3 >= num2):
            return num3 - num2
        return math.pi * 2 - num2 + num3
    
    @staticmethod
    def smethod_50(turnDirection_0, point3d_0, point3d_1, point3d_2):
        # This method is calculating center angle if three points.
        #Center point is point3d_2.
        num = MathHelper.getBearing(point3d_2, point3d_0)
        num1 = MathHelper.getBearing(point3d_2, point3d_1)
        if (turnDirection_0 == TurnDirection.Left):
            if (num >= num1):
                return num - num1
            return math.pi * 2 - num1 + num
        if (num1 >= num):
            return num1 - num
        return math.pi * 2 - num + num1

    @staticmethod
    def smethod_51(double_0, double_1):
        num = None
        double_0 = MathHelper.smethod_4(double_0)
        double_1 = MathHelper.smethod_4(double_1)
        num = double_0 + (math.pi * 2 - double_0 + double_1) / 2  if(double_0 > double_1) else double_0 + (double_1 - double_0) / 2
        return MathHelper.smethod_4(num)

    @staticmethod
    def smethod_52(double_0, double_1, bool_0):
        if (not bool_0):
            return MathHelper.smethod_51(double_0, double_1)
        point3d = MathHelper.distanceBearingPoint(Point3D(0, 0, 0), double_0, 1000)
        point3d1 = MathHelper.distanceBearingPoint(Point3D(0, 0, 0), double_1, 1000)
        point3d2 = MathHelper.distanceBearingPoint(point3d, MathHelper.getBearing(point3d, point3d1), MathHelper.calcDistance(point3d, point3d1) / 2)
        return MathHelper.getBearing(Point3D(0, 0, 0), point3d2)
    
    @staticmethod
    
    def smethod_53(double_0, double_1):
        double_0 = MathHelper.smethod_4(double_0)
        double_1 = MathHelper.smethod_4(double_1)
        if (double_0 <= double_1):
            return double_1 - double_0
        return (math.pi * 2 - double_0 + double_1)

    @staticmethod
    def smethod_55(point3d_0, point3d_1, double_0):
        return math.tan(2 * math.asin(MathHelper.calcDistance(point3d_0, point3d_1) / (2 * double_0)) / 4)


    @staticmethod
    def smethod_57(turnDirection_0, point3d_0, point3d_1, point3d_2):
        num1 = MathHelper.getBearing(point3d_2, point3d_0)
        num2 = MathHelper.getBearing(point3d_2, point3d_1)
        if turnDirection_0 == TurnDirection.Right:
            if (num2 <= num1):
                num = num2 + (math.pi * 2 - num1)
            else:
                num = num2 - num1
        elif turnDirection_0 == TurnDirection.Nothing:
            return 0
        elif turnDirection_0 == TurnDirection.Left:
            if (num2 <= num1):
                num = num1 - num2
            else:
                num = num1 + (math.pi * 2 - num2)
        else:
            return 0
        return (math.tan(num / 4) * turnDirection_0)

    @staticmethod
    def smethod_59(double_0, point3d_0, point3d_1):
        num = MathHelper.getBearing(point3d_0, point3d_1)
        num1 = MathHelper.calcDistance(point3d_0, point3d_1) / 2
        turnDirection = MathHelper.smethod_63(double_0, num, AngleUnits.Radians)
        if (turnDirection == TurnDirection.Nothing):
            return 0
        num2 = TurnDirection.Right * turnDirection
        point3d1 = MathHelper.distanceBearingPoint(point3d_0, double_0 + math.pi / 2 * num2, 100)
        point3d2 = MathHelper.distanceBearingPoint(point3d_0, num, num1)
        point3d = MathHelper.getIntersectionPoint(point3d_0, point3d1, point3d2, MathHelper.distanceBearingPoint(point3d2, num + math.pi / 2 * num2, 100))
        if point3d == None:
            return 0
        return MathHelper.smethod_57(turnDirection, point3d_0, point3d_1, point3d)

    # MathHelper.distanceBearingPoint
    # return Point3D
    # input Point3D, double, double
    @staticmethod
    def distanceBearingPoint2d(point2d_0, double_0, double_1):
        x = point2d_0.get_X() + math.sin(double_0) * double_1
        y = point2d_0.get_Y() + math.cos(double_0) * double_1
        return Point3D(x, y)

    @staticmethod
    def GetIntersectionPointBetweenLineandArc(fPoint, alpha, cPoint, d):
        # double b, c
        # double x1, y1, x2, y2
        if (cPoint == None or fPoint == None):
            return False, None

        x1 = fPoint.x()
        y1 = fPoint.y()
        x2 = cPoint.x()
        y2 = cPoint.y()

        b = math.cos(alpha) * (x1 - x2) + math.sin(alpha) * (y1 - y2)
        c = math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2) - math.pow(d, 2)

        # double r

        if (math.pow(b, 2) - c < 0.0000001):
            return False, None

        r = -b + math.sqrt(math.pow(b, 2) - c)
        outPoint = MathHelper.distanceBearingPoint(fPoint, alpha, r)
        return True, outPoint
    @staticmethod
    def getIntersectionPointBetweenPolylineArea(polylineArea0, polylineArea1):
        geom0 = QgsGeometry.fromPolyline(polylineArea0.method_14())
        geom1 = QgsGeometry.fromPolyline(polylineArea1.method_14())
        if not geom0.intersects(geom1):
            return None
        resultGeom = geom0.intersection(geom1)
        return resultGeom.asPoint()

    @staticmethod
    def distanceBearingPoint(point3d_0, double_0, double_1, unit = None):

        #///////// Input Parameter /////////#
        # double_0 ------- Bearing
        # double_1 ------- Distance
        if unit == None:
            unit = define._units
        if double_1 == 0:
            return point3d_0
        if unit != QGis.Meters:
            y = math.asin( math.sin(Unit.ConvertDegToRad(point3d_0.y()))*math.cos(double_1 / 1000.0 /6393.1) +
                    math.cos(Unit.ConvertDegToRad(point3d_0.y()))*math.sin(double_1 / 1000.0 / 6393.1) * math.cos(double_0) )
            x = Unit.ConvertDegToRad(point3d_0.x()) + math.atan2(math.sin(double_0)*math.sin(double_1 / 1000.0 / 6393.1) * math.cos(Unit.ConvertDegToRad(point3d_0.y())),
                         math.cos(double_1 / 1000.0 / 6393.1) - math.sin(Unit.ConvertDegToRad(point3d_0.y())) * math.sin(y))
            if isinstance(point3d_0, Point3D):
                point3d_1 = Point3D(Unit.ConvertRadToDeg(x), Unit.ConvertRadToDeg(y), point3d_0.z())
            else:
                point3d_1 = Point3D(Unit.ConvertRadToDeg(x), Unit.ConvertRadToDeg(y))


            # double_1 = define._qgsDistanceArea.convertMeasurement(double_1, QGis.Meters, QGis.Degrees, False)[0]
            # x = point3d_0.x() + math.sin(double_0) * double_1
            # y = point3d_0.y() + math.cos(double_0) * double_1
            # if isinstance(point3d_0, Point3D):
            #     point3d_1 = Point3D(x, y, point3d_0.z())
            # else:
            #     point3d_1 = Point3D(x, y, 0.0)
        else:
            x = point3d_0.x() + math.sin(double_0) * double_1
            y = point3d_0.y() + math.cos(double_0) * double_1
            if isinstance(point3d_0, Point3D):
                point3d_1 = Point3D(x, y, point3d_0.get_Z())
            else:
                point3d_1 = Point3D(x, y, 0.0)
        return point3d_1

    @staticmethod
    def distanceBearingPointArcGIS(point3d_0, double_0, double_1, unit = None):

        #///////// Input Parameter /////////#
        # double_0 ------- Bearing
        # double_1 ------- Distance
        double_0 = math.pi / 2 - double_0

        if unit == None:
            unit = define._units
        if double_1 == 0:
            return point3d_0
        if unit != QGis.Meters:
            y = math.asin( math.sin(Unit.ConvertDegToRad(point3d_0.y()))*math.cos(double_1 / 1000.0 /6393.1) +
                    math.cos(Unit.ConvertDegToRad(point3d_0.y()))*math.sin(double_1 / 1000.0 / 6393.1) * math.cos(double_0) )
            x = Unit.ConvertDegToRad(point3d_0.x()) + math.atan2(math.sin(double_0)*math.sin(double_1 / 1000.0 / 6393.1) * math.cos(Unit.ConvertDegToRad(point3d_0.y())),
                         math.cos(double_1 / 1000.0 / 6393.1) - math.sin(Unit.ConvertDegToRad(point3d_0.y())) * math.sin(y))
            if isinstance(point3d_0, Point3D):
                point3d_1 = Point3D(Unit.ConvertRadToDeg(x), Unit.ConvertRadToDeg(y), point3d_0.z())
            else:
                point3d_1 = Point3D(Unit.ConvertRadToDeg(x), Unit.ConvertRadToDeg(y))


            # double_1 = define._qgsDistanceArea.convertMeasurement(double_1, QGis.Meters, QGis.Degrees, False)[0]
            # x = point3d_0.x() + math.sin(double_0) * double_1
            # y = point3d_0.y() + math.cos(double_0) * double_1
            # if isinstance(point3d_0, Point3D):
            #     point3d_1 = Point3D(x, y, point3d_0.z())
            # else:
            #     point3d_1 = Point3D(x, y, 0.0)
        else:
            x = point3d_0.x() + math.sin(double_0) * double_1
            y = point3d_0.y() + math.cos(double_0) * double_1
            if isinstance(point3d_0, Point3D):
                point3d_1 = Point3D(x, y, point3d_0.get_Z())
            else:
                point3d_1 = Point3D(x, y, 0.0)
        return point3d_1
#         public static bool smethod_117(Point3d point3d_0, Point3d point3d_1, Point3d point3d_2, bool bool_0)
    @staticmethod
    def smethod_117(point3d_0, point3d_1, point3d_2, bool_0):
        res = (point3d_2.x() - point3d_1.x()) * (point3d_0.y() - point3d_1.y()) - (point3d_0.x() - point3d_1.x()) * (point3d_2.y() - point3d_1.y())
        res1 = (point3d_2.x() - point3d_1.x()) * (point3d_0.y() - point3d_1.y()) - (point3d_0.x() - point3d_1.x()) * (point3d_2.y() - point3d_1.y())
        if (not bool_0):
            return res > 0
        return res1 >= 0
    
#        public static bool smethod_115(Point3d point3d_0, Point3d point3d_1, Point3d point3d_2)
#         {
    @staticmethod
    def smethod_115(point3d_0, point3d_1, point3d_2):
        if point3d_0 == None:
            return False
        return MathHelper.smethod_117(point3d_0, point3d_1, point3d_2, True)
#         }
#             public static bool smethod_110(Point3d point3d_0, Point3d point3d_1, Point3d point3d_2)
#         {
    @staticmethod
    def smethod_110(point3d_0, point3d_1, point3d_2):
        num = MathHelper.getBearing(point3d_1, point3d_2) - math.pi / 2
        point3d = MathHelper.distanceBearingPoint(point3d_1, num, 100)
        point3d1 = MathHelper.distanceBearingPoint(point3d_2, num, 100)
        if not MathHelper.smethod_121(point3d_0, point3d_1, point3d, True):
            return False
        return MathHelper.smethod_117(point3d_0, point3d_2, point3d1, True)

#         public static bool smethod_121(Point3d point3d_0, Point3d point3d_1, Point3d point3d_2, bool bool_0)
#         {
    @staticmethod
    def smethod_121(point3d_0, point3d_1, point3d_2, bool_0):
        if not bool_0:
            return (point3d_2.x() - point3d_1.x()) * (point3d_0.y() - point3d_1.y()) - (point3d_0.x() - point3d_1.x()) * (point3d_2.y() - point3d_1.y()) < 0
        return (point3d_2.x() - point3d_1.x()) * (point3d_0.y() - point3d_1.y()) - (point3d_0.x() - point3d_1.x()) * (point3d_2.y() - point3d_1.y()) <= 0

#         public static bool smethod_42(Point3dCollection point3dCollection_0, Point3d point3d_0, bool bool_0)
#         {
    @staticmethod
    def smethod_42(point3dCollection_0, point3d_0, bool_0=True):
        count = len(point3dCollection_0)
        if (count < 3):
            raise UserWarning, "ERR_MINIMUM_3_AREA_POINTS"
        num = 0
        num1 = 0
        num2 = 0
        while True:
            if (num2 >= count):
                if (num % 2 == 1 and num1 % 2 == 1):
                    return True
                return False
            item = point3dCollection_0[num2]
            if num2 != count - 1 :
                point3d = point3dCollection_0[num2 + 1]
            else :
                point3d = point3dCollection_0[0]
            if item.x() != point3d.x() or item.y() != point3d.y():
                if item.x() == point3d_0.x() and item.y() == point3d_0.y():
                    break
                if point3d.x() == point3d_0.x() and point3d.y() == point3d_0.y():
                    break
                elif (item.y() <= point3d_0.y() and point3d.y() > point3d_0.y()) or (item.y() > point3d_0.y() and point3d.y() <= point3d_0.y()):
                    x = item.x() + (point3d_0.y() - item.y()) / (point3d.y() - item.y()) * (point3d.x() - item.x())
                    if x == point3d_0.x():
                        if (bool_0):
                            return True
                        return False
                    if x < point3d_0.x():
                        num += 1
                    if x > point3d_0.x():
                        num1 += 1
            num2 += 1
        if (bool_0):
            return True
        
        return False
    
#         public static bool smethod_119(Point3d point3d_0, Point3d point3d_1, Point3d point3d_2)
#         {
#             return MathHelper.smethod_121(point3d_0, point3d_1, point3d_2, true)
#         }
    @staticmethod
    def smethod_119(point3d_0, point3d_1, point3d_2):
        if point3d_0 == None:
            return False
        return MathHelper.smethod_121(point3d_0, point3d_1, point3d_2, True)
    
#         public static bool smethod_40(Point3dCollection point3dCollection_0, Point3d point3d_0)
#         {
#             return MathHelper.smethod_42(point3dCollection_0, point3d_0, true)
#         }
    @staticmethod
    def smethod_40(point3dCollection_0, point3d_0):
#         return True
        return MathHelper.smethod_42(point3dCollection_0, point3d_0, True)

#         public static double smethod_60(Point2d point2d_0, Point2d point2d_1, Point2d point2d_2)
#         {
    @staticmethod
    def smethod_60(point2d_0, point2d_1, point2d_2):

        #  Method calculating the bulge when three points exist.
        # ///////////  Input Parameter  ///////////////#
        # point2d_0  ---------  start point (Point3D)
        # point2d_1  ---------  middle point (Point3D)
        # point2d_2  ---------  end point (Point3D)

        # //////////  Output parameter  //////////////#
        # This method return bulge value.
        # The type return vlaue is "double".

        # //////////  Keywords  //////////////#
        # "Calculate Bulge", "Return Bulge", "Get Bulge", "Bulge Get", "Bulge Return", "Bulge Calculate", "BulgeGet", "BulgeReturn", "BulgeCalculate", "CalculateBulge", "ReturnBulge", "GetBulge"

        num = MathHelper.getBearing(point2d_0, point2d_1)
        num1 = MathHelper.getBearing(point2d_0, point2d_2)
        point2d = MathHelper.smethod_68(point2d_0, point2d_1, point2d_2)
        if point2d == None:
            return 0.0
        return MathHelper.smethod_57(MathHelper.smethod_63(num, num1, AngleUnits.Radians), point2d_0, point2d_2, point2d)
    @staticmethod
    def smethod_61_v15(point2d_0, point2d_1, point2d_2):

        #  Method calculating the bulge when three points exist.
        # ///////////  Input Parameter  ///////////////#
        # point2d_0  ---------  start point (Point3D)
        # point2d_1  ---------  middle point (Point3D)
        # point2d_2  ---------  end point (Point3D)

        # //////////  Output parameter  //////////////#
        # This method return bulge value.
        # The type return vlaue is "double".

        # //////////  Keywords  //////////////#
        # "Calculate Bulge", "Return Bulge", "Get Bulge", "Bulge Get", "Bulge Return", "Bulge Calculate", "BulgeGet", "BulgeReturn", "BulgeCalculate", "CalculateBulge", "ReturnBulge", "GetBulge"

        num = MathHelper.getBearing(point2d_0, point2d_1)
        num1 = MathHelper.getBearing(point2d_0, point2d_2)
        point2d = MathHelper.smethod_68(point2d_0, point2d_1, point2d_2)
        if point2d == None:
            return 0.0
        return MathHelper.smethod_57(MathHelper.smethod_63(num, num1, AngleUnits.Radians), point2d_0, point2d_2, point2d)


    @staticmethod
    def smethod_62(turnDirection_0, double_0, angleUnits_0):
        if (double_0 == 0):
            return 0
        if (angleUnits_0 == AngleUnits.Degrees):
            Unit.ConvertDegToRad(double_0)
        if (turnDirection_0 == TurnDirection.Left):
            return math.tan(double_0 / 4)
        if (turnDirection_0 != TurnDirection.Right):
            return 0
        return math.tan(double_0 / 4) * -1
        
    @staticmethod
    def smethod_63(double_0, double_1, AngleUnits_0):
        if (AngleUnits_0 == AngleUnits.Degrees):
            double_0 = MathHelper.smethod_3(double_0)
            double_1 = MathHelper.smethod_3(double_1)
            num = math.fabs(double_0 - double_1)
            if (MathHelper.smethod_98(double_0, double_1) or (MathHelper.smethod_96(num)) or MathHelper.smethod_98(num, 360)):
                return TurnDirection.Nothing
            if (double_0 - double_1 > 0):
                if (double_0 - double_1 <= 180):
                    return TurnDirection.Left
                return TurnDirection.Right
            if (double_1 - double_0 < 180):
                return TurnDirection.Right
            return TurnDirection.Left
        double_0 = MathHelper.smethod_4(double_0)
        double_1 = MathHelper.smethod_4(double_1)
        num1 = math.fabs(double_0 - double_1)
        if (MathHelper.smethod_98(double_0, double_1) or (MathHelper.smethod_96(num1)) or MathHelper.smethod_98(num1, math.pi * 2)):
            return TurnDirection.Nothing
        if (double_0 - double_1 > 0):
            if (double_0 - double_1 <= math.pi):
                return TurnDirection.Left
            return TurnDirection.Right
        if (double_1 - double_0 < math.pi):
            return TurnDirection.Right
        return TurnDirection.Left
    
#         public static TurnDirection smethod_65(Point3dCollection point3dCollection_0)
#         {
    @staticmethod
    def smethod_65(point3dCollection_0):        
        y = 0
        count = len(point3dCollection_0)
        if count == 0:
            return TurnDirection.Nothing
        i = 1
        while i < count:
            x = point3dCollection_0[i].x()
            item = point3dCollection_0[i - 1]
            num = x - item.x()
            y1 = point3dCollection_0[i].y()
            point3d = point3dCollection_0[i - 1]
            y = y + num * (y1 + point3d.y()) / 2
            i += 1
        x1 = point3dCollection_0[0].x()
        item1 = point3dCollection_0[count - 1]
        num1 = x1 - item1.x()
        y2 = point3dCollection_0[0].y()
        point3d1 = point3dCollection_0[count - 1]
        y = y + num1 * (y2 + point3d1.y()) / 2
        if (y > 0):
            return TurnDirection.Right
        if (y < 0):
            return TurnDirection.Left
        return TurnDirection.Nothing

    @staticmethod
    def smethod_66(double_0):
        if (double_0 > 0):
            return TurnDirection.Left
        if (double_0 < 0):
            return TurnDirection.Right
        return TurnDirection.Nothing
    
    @staticmethod
    def smethod_67(turnDirection_0):
        if (turnDirection_0 == TurnDirection.Right):
            return TurnDirection.Left
        elif (turnDirection_0 == TurnDirection.Nothing):
            return turnDirection_0
        elif (turnDirection_0 == TurnDirection.Left):
            return TurnDirection.Right
        else:
            return turnDirection_0
        
    @staticmethod
    def smethod_7(double_0):
        return MathHelper.smethod_66(double_0)
#                 

#         public static bool smethod_68(Point2d point2d_0, Point2d point2d_1, Point2d point2d_2, out Point2d point2d_3)
#         { 
    @staticmethod
    def smethod_68(point2d_0, point2d_1, point2d_2):
        # calculate intersection of 2 devided line perpendicular.
        num = MathHelper.getBearing(point2d_0, point2d_1)
        num1 = MathHelper.getBearing(point2d_1, point2d_2)
        num2 = TurnDirection.Right * MathHelper.smethod_63(num, num1, AngleUnits.Radians)
        point2d = MathHelper.distanceBearingPoint(point2d_0, num, MathHelper.calcDistance(point2d_0, point2d_1) / 2)
        point2d1 = MathHelper.distanceBearingPoint(point2d, num + num2 * math.pi / 2, 1000)
        point2d2 = MathHelper.distanceBearingPoint(point2d_1, num1, MathHelper.calcDistance(point2d_1, point2d_2) / 2)
        point2d3 = MathHelper.distanceBearingPoint(point2d2, num1 + num2 * math.pi / 2, 1000)
        return MathHelper.getIntersectionPoint(point2d, point2d1, point2d2, point2d3)


#         public static bool smethod_132(Point3dCollection point3dCollection_0)
#         {
    
#         public static bool smethod_71(Point3d point3d_0, Point3d point3d_1, double double_0, out Point3d point3d_2)
#         {
    @staticmethod
    def smethod_70(point3d_0, point3d_1, double_0):
        
        point3d_2 = Point3D.get_Origin()
        if (MathHelper.smethod_96(double_0)):
            return None
        if double_0 <= 0 :
            turnDirection = TurnDirection.Right
        else:
            turnDirection = TurnDirection.Left
            
        num = math.atan(math.fabs(double_0)) * 4
        num1 = MathHelper.getBearing(point3d_0, point3d_1)
        num2 = MathHelper.getBearing(point3d_1, point3d_0)
        if (turnDirection != TurnDirection.Left):
            if (MathHelper.smethod_98(num, math.pi)):
                point3d_2 = MathHelper.distanceBearingPoint(point3d_0, num1, MathHelper.calcDistance(point3d_0, point3d_1) / 2)
                return point3d_2
            if (num <= math.pi):
                num = (math.pi - num) / 2
                point3d = MathHelper.distanceBearingPoint(point3d_0, num1 + num, 100)
                point3d1 = MathHelper.distanceBearingPoint(point3d_1, num2 - num, 100)
            else:
                num = (math.pi - (math.pi * 2 - num)) / 2
                point3d = MathHelper.distanceBearingPoint(point3d_0, num1 - num, 100)
                point3d1 = MathHelper.distanceBearingPoint(point3d_1, num2 + num, 100)
        else:
            if (MathHelper.smethod_98(num, math.pi)):
                point3d_2 = MathHelper.distanceBearingPoint(point3d_0, num1, MathHelper.calcDistance(point3d_0, point3d_1) / 2)
                return point3d_2
            if (num <= math.pi):
                num = (math.pi - num) / 2
                point3d = MathHelper.distanceBearingPoint(point3d_0, num1 - num, 100)
                point3d1 = MathHelper.distanceBearingPoint(point3d_1, num2 + num, 100)
            else:
                num = (math.pi - (math.pi * 2 - num)) / 2
                point3d = MathHelper.distanceBearingPoint(point3d_0, num1 + num, 100)
                point3d1 = MathHelper.distanceBearingPoint(point3d_1, num2 - num, 100)
        return MathHelper.getIntersectionPoint(point3d_0, point3d, point3d_1, point3d1)
    
    @staticmethod
    def smethod_71(point3d_0, point3d_1, double_0):

        #  Method calculating the center point when two points and bulge exist.
        # ///////////  Input Parameter  ///////////////#
        # point3d_0  ---------  start point (Point3D)
        # point3d_1  ---------  end point (Point3D)
        # double_0  ---------  bulge (double)

        # //////////  Output parameter  //////////////#
        # This method return center point.
        # The type return vlaue is "Point3D".

        # //////////  Keywords  //////////////#
        # "Calculate CenterPoint", "Return CenterPoint", "Get CenterPoint", "CenterPoint Get", "CenterPoint Return", "CenterPoint Calculate", "CenterPointGet", "CenterPointReturn", "CenterPointCalculate", "CenterPointBulge", "ReturnCenterPoint", "GetCenterPoint"

        
        point3d_2 = Point3D.get_Origin()
        if (MathHelper.smethod_96(double_0)):
            return point3d_2
        if double_0 <= 0 :
            turnDirection = TurnDirection.Right
        else:
            turnDirection = TurnDirection.Left
            
        num = math.atan(math.fabs(double_0)) * 4
        num1 = MathHelper.getBearing(point3d_0, point3d_1)
        num2 = MathHelper.getBearing(point3d_1, point3d_0)
        if (turnDirection != TurnDirection.Left):
            if (MathHelper.smethod_98(num, math.pi)):
                point3d_2 = MathHelper.distanceBearingPoint(point3d_0, num1, MathHelper.calcDistance(point3d_0, point3d_1) / 2)
                return point3d_2
            if (num <= math.pi):
                num = (math.pi - num) / 2
                point3d = MathHelper.distanceBearingPoint(point3d_0, num1 + num, 100)
                point3d1 = MathHelper.distanceBearingPoint(point3d_1, num2 - num, 100)
            else:
                num = (math.pi - (math.pi * 2 - num)) / 2
                point3d = MathHelper.distanceBearingPoint(point3d_0, num1 - num, 100)
                point3d1 = MathHelper.distanceBearingPoint(point3d_1, num2 + num, 100)
        else:
            if (MathHelper.smethod_98(num, math.pi)):
                point3d_2 = MathHelper.distanceBearingPoint(point3d_0, num1, MathHelper.calcDistance(point3d_0, point3d_1) / 2)
                return point3d_2
            if (num <= math.pi):
                num = (math.pi - num) / 2
                point3d = MathHelper.distanceBearingPoint(point3d_0, num1 - num, 100)
                point3d1 = MathHelper.distanceBearingPoint(point3d_1, num2 + num, 100)
            else:
                num = (math.pi - (math.pi * 2 - num)) / 2
                point3d = MathHelper.distanceBearingPoint(point3d_0, num1 + num, 100)
                point3d1 = MathHelper.distanceBearingPoint(point3d_1, num2 - num, 100)
        return MathHelper.getIntersectionPoint(point3d_0, point3d, point3d_1, point3d1)
    
    @staticmethod
    def smethod_73(point3d_0, point3d_1, double_0):
        point3d_2 = MathHelper.smethod_71(point3d_0, point3d_1, double_0)
        if ( point3d_2 == None):
            return (None, None)
        double_1 = MathHelper.calcDistance(point3d_2, point3d_0)
        return (point3d_2, double_1)
    
    @staticmethod
    def smethod_75(turnAngleRadian, startPt, endPt):
        ''' Calculate center point '''
        num1 = MathHelper.getBearing(startPt, endPt)
        num2 = MathHelper.calcDistance(startPt, endPt) / 2
        turnDirection = MathHelper.smethod_63(turnAngleRadian, num1, AngleUnits.Radians)
        if (turnDirection != TurnDirection.Left):
            if (turnDirection != TurnDirection.Right):
                point3d_2 = Point3D.get_Origin()
                return point3d_2
            num = 1
        else:
            num = -1
        point3d = MathHelper.distanceBearingPoint(startPt, turnAngleRadian + math.pi / 2 * num, 100)
        point3d1 = MathHelper.distanceBearingPoint(startPt, num1, num2)
        point3d2 = MathHelper.distanceBearingPoint(point3d1, num1 + math.pi / 2 * num, 100)
        return MathHelper.getIntersectionPoint(startPt, point3d, point3d1, point3d2)

    @staticmethod
    def getArcWithTwoContactAndBearing(contactPtStart, bearingStart, contactPtEnd, bearingEnd, turnDirection):
        intersectPt = MathHelper.getIntersectionPoint(contactPtStart, MathHelper.distanceBearingPoint(contactPtStart, bearingStart, 100),
                                                      contactPtEnd, MathHelper.distanceBearingPoint(contactPtEnd, bearingEnd, 100))
        dist = MathHelper.calcDistance(contactPtStart, intersectPt)
        if turnDirection == TurnDirection.Right:
            rad = MathHelper.smethod_4(bearingStart - bearingEnd) / 2
            radius = dist * math.tan(rad)
            centerPt = MathHelper.distanceBearingPoint(contactPtStart, MathHelper.smethod_4(bearingStart + math.pi / 2), radius)
            middlePt = MathHelper.distanceBearingPoint(centerPt, MathHelper.smethod_4(MathHelper.getBearing(centerPt, contactPtStart) + math.pi / 2 - rad), radius)
            resultBearing = MathHelper.smethod_60(contactPtStart, middlePt, contactPtEnd)
            return contactPtStart, contactPtEnd, resultBearing
        else:
            rad = MathHelper.smethod_4(bearingEnd - bearingStart) / 2
            radius = dist * math.tan(rad)
            centerPt = MathHelper.distanceBearingPoint(contactPtStart, MathHelper.smethod_4(bearingStart - math.pi / 2), radius)
            middlePt = MathHelper.distanceBearingPoint(centerPt, MathHelper.smethod_4(MathHelper.getBearing(centerPt, contactPtStart) - (math.pi / 2 - rad)), radius)
            resultBearing = MathHelper.smethod_60(contactPtStart, middlePt, contactPtEnd)
            return contactPtStart, contactPtEnd, resultBearing




    @staticmethod
    def CalcCenter(turnAngleRadian, startPt, endPt):
        return MathHelper.smethod_75(turnAngleRadian, startPt, endPt)

#         public static double smethod_76(double double_0, double double_1, AngleUnits AngleUnits_0)
#         {
    @staticmethod
    def smethod_76(double_0, double_1, AngleUnits_0):
        ### This method ia the method that calculate angle of turn in radian.
        ### Parameters
        ### double_0 : inbound track
        ### double_1 : outbound track
        turnDirection = []
        return MathHelper.smethod_77(double_0, double_1, AngleUnits_0, turnDirection)
#             TurnDirection turnDirection
#             return MathHelper.smethod_77(double_0, double_1, AngleUnits_0, out turnDirection)
#         }
# 
#         public static double smethod_77(double double_0, double double_1, AngleUnits AngleUnits_0, out TurnDirection turnDirection_0)
#         {
    @staticmethod
    def smethod_77(double_0, double_1, AngleUnits_0, turnDirection_0):
        if AngleUnits_0 == AngleUnits.Degrees:
            double_0 = MathHelper.smethod_3(double_0)
            double_1 = MathHelper.smethod_3(double_1)
            double1 = double_1 - double_0
            if (MathHelper.smethod_96(double1)):
                turnDirection_0.append(TurnDirection.Nothing)
            elif (double1 > 0):
                if (double1 <= 180):
                    turnDirection_0.append(TurnDirection.Right)
                else:
                    turnDirection_0.append(TurnDirection.Left)
                    double1 = double1 - 360
            elif (double1 >= -180):
                turnDirection_0.append(TurnDirection.Left)
            else:
                turnDirection_0.append(TurnDirection.Right)
                double1 = -360 - double1
            return MathHelper.smethod_3(math.fabs(double1))

        double_0 = MathHelper.smethod_4(double_0)
        double_1 = MathHelper.smethod_4(double_1)
        num = double_1 - double_0
        if (MathHelper.smethod_96(num)):
            turnDirection_0.append(TurnDirection.Nothing)
        elif (num > 0):
            if (num <= math.pi):
                turnDirection_0.append(TurnDirection.Right)
            else:
                turnDirection_0.append(TurnDirection.Left)
                num = num - math.pi * 2
        elif (num >= -math.pi):
            turnDirection_0.append(TurnDirection.Left)
        else:
            turnDirection_0.append(TurnDirection.Right)
            num = -math.pi * 2 - num
        return MathHelper.smethod_4(math.fabs(num))

#         public static bool smethod_128(Point3d point3d_0, Point3d point3d_1, Point3d point3d_2, Point3d point3d_3)
#         {
#             if (!MathHelper.smethod_121(point3d_0, point3d_2, point3d_3, true))
#             {
#                 return false
#             }
#             return MathHelper.smethod_121(point3d_1, point3d_2, point3d_3, true)
#         }
    @staticmethod
    def smethod_84(point3d_0, point3d_1, point3d_2, angleUnits_0):
        
        turnDirection = []
        num = MathHelper.getBearing(point3d_0, point3d_1)
        num1 = MathHelper.getBearing(point3d_1, point3d_2)
        if (angleUnits_0 == AngleUnits.Radians):
            return MathHelper.smethod_77(num, num1, AngleUnits.Radians, turnDirection)
        
        return MathHelper.smethod_77(Unit.smethod_1(num), Unit.smethod_1(num1), AngleUnits.Degrees, turnDirection)
    @staticmethod
    def smethod_128(point3d_0, point3d_1, point3d_2, point3d_3):
        if not MathHelper.smethod_121(point3d_0, point3d_2, point3d_3, True):
            return False
        return MathHelper.smethod_121(point3d_1, point3d_2, point3d_3, True)

#         public static bool smethod_30(Point3d point3d_0, Point3d point3d_1, Point3d point3d_2, Point3d point3d_3, bool bool_0)
#         {
    @staticmethod
    def smethod_30(point3d_0, point3d_1, point3d_2, point3d_3, bool_0):
        x = point3d_0.get_X()
        num = point3d_1.get_X()
        x1 = point3d_2.get_X()
        num1 = point3d_3.get_X()
        y = point3d_0.get_Y()
        y1 = point3d_1.get_Y()
        y2 = point3d_2.get_Y()
        num2 = point3d_3.get_Y()
        num3 = (num2 - y2) * (num - x) - (num1 - x1) * (y1 - y)
        if (num3 == 0):
            return False
        num4 = ((num1 - x1) * (y - y2) - (num2 - y2) * (x - x1)) / num3
        num5 = ((num - x) * (y - y2) - (y1 - y) * (x - x1)) / num3
        if not MathHelper.smethod_107(num4, 0, 1, bool_0, bool_0):
            return False
        return MathHelper.smethod_107(num5, 0, 1, bool_0, bool_0)
#         }
#         public static bool smethod_107(double double_0, double double_1, double double_2, bool bool_0, bool bool_1)
#         {
    @staticmethod
    def smethod_107(double_0, double_1, double_2, bool_0, bool_1):
        if (bool_0 and bool_1):
            if (double_0 < double_1):
                return False
            return double_0 <= double_2
        if (bool_0):
            if (double_0 < double_1):
                return False
            return double_0 < double_2
        if (not bool_1):
            if (double_0 <= double_1):
                return False
            return double_0 < double_2
        if (double_0 <= double_1):
            return False
        return double_0 <= double_2
    
    @staticmethod
    def smethod_106(double_0, double_1, double_2):
        if (double_0 < double_1):
            return False
        if double_0 <= double_2:
            return True
        else:
            return False
    
    @staticmethod
    def smethod_2(double_0):
        if (double_0 == 0):
            return 1E-08
        return double_0
    @staticmethod
    def smethod_103(point3d_0, point3d_1, double_0):
        if (math.fabs(point3d_1.x() - point3d_0.x()) > double_0):
            return False
        return math.fabs(point3d_1.y() - point3d_0.y()) <= double_0
    @staticmethod
    def smethod_89(point3d_0, double_0, point3d_1, double_1):#, out Point3d point3d_2, out Point3d point3d_3, out Point3d point3d_4, out Point3d point3d_5)
        num = 0
        num1 = MathHelper.calcDistance(point3d_0, point3d_1)
        if (num1 != 0):
            num = math.fabs(math.asin((double_1 - double_0) / num1))
        if (double_1 > double_0):
            point3d_2 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_1) + num + math.pi / 2, double_0)
            point3d_3 = MathHelper.distanceBearingPoint(point3d_1, MathHelper.getBearing(point3d_0, point3d_1) + num + math.pi / 2, double_1)
            point3d_4 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_1) - num - math.pi / 2, double_0)
            point3d_5 = MathHelper.distanceBearingPoint(point3d_1, MathHelper.getBearing(point3d_0, point3d_1) - num - math.pi / 2, double_1)
            return point3d_2, point3d_3, point3d_4, point3d_5
        point3d_2 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_1) - num + math.pi / 2, double_0)
        point3d_3 = MathHelper.distanceBearingPoint(point3d_1, MathHelper.getBearing(point3d_0, point3d_1) - num + math.pi / 2, double_1)
        point3d_4 = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_1) + num - math.pi / 2, double_0)
        point3d_5 = MathHelper.distanceBearingPoint(point3d_1, MathHelper.getBearing(point3d_0, point3d_1) + num - math.pi / 2, double_1)
        return point3d_2, point3d_3, point3d_4, point3d_5

    @staticmethod
    def smethod_178(point3d_0, point3d_1):
        return Point3D(min([point3d_0.get_X(), point3d_1.get_X()]), min([point3d_0.get_Y(), point3d_1.get_Y()]), 0)

    @staticmethod
    def smethod_180(point3d_0, point3d_1):
        return Point3D(max([point3d_0.get_X(), point3d_1.get_X()]), max([point3d_0.get_Y(), point3d_1.get_Y()]), 0)

    @staticmethod
    def smethod_184(point3d_0, point3d_1):
        point3d0 = point3d_0
        point3d_0 = point3d_1
        point3d_1 = point3d0
        return point3d_0, point3d_1
    
    @staticmethod
    def smethod_186(point3dCollection_0):
        count = len(point3dCollection_0)
        return MathHelper.smethod_119(point3dCollection_0[count - 1], point3dCollection_0[count - 3], point3dCollection_0[count - 2])
    
    @staticmethod
    def smethod_188(point3dCollection_0):
        count = len(point3dCollection_0)
        return MathHelper.smethod_115(point3dCollection_0[count - 1], point3dCollection_0[count - 3], point3dCollection_0[count - 2])
    
    
    
    ####
    @staticmethod
    def smethod_190(point3dCollection_0):
        if (len(point3dCollection_0) < 3):
            return point3dCollection_0
        point3ds = []
        for point3dCollection0 in point3dCollection_0:
            point3ds.append(point3dCollection0)
        point3ds.sort()
        item = point3ds[0]
        point3d = point3ds[len(point3ds) - 1]
        point3dCollection = []
        for point3d1 in point3ds:
            if (not MathHelper.smethod_115(point3d1, item, point3d)):
                continue
            point3dCollection.append(point3d1)
            while (len(point3dCollection) > 2 and MathHelper.smethod_188(point3dCollection)):
                point3dCollection.remove(point3dCollection[len(point3dCollection) - 2])
        point3dCollection1 = []
        for point3d2 in point3ds:
            if (not MathHelper.smethod_119(point3d2, item, point3d)):
                continue
            point3dCollection1.append(point3d2)
            while (len(point3dCollection1) > 2 and MathHelper.smethod_186(point3dCollection1)):
                point3dCollection1.remove(point3dCollection1[len(point3dCollection1) - 2])
        point3dCollection1.remove(point3dCollection1[0])
        point3dCollection1.remove(point3dCollection1[len(point3dCollection1) - 1])
        point3dCollection1.reverse()
        point3dCollection.extend(point3dCollection1)
        return point3dCollection
    
    @staticmethod
    def smethod_191(double_0, double_1, double_2, double_3):
        if (MathHelper.smethod_96(double_1) or math.isinf(double_1) or math.isnan(double_1)):
            if (double_3 <= 0):
                return double_0
            double3 = double_3 + double_0
            num = math.sqrt(double_2 * double_2 + double3 * double3)
            return num - double_3
        if (double_1 > 0):
            if (double_3 <= 0):
                return double_2 * math.tan(double_1) + double_0
            double2 = double_2 / math.cos(double_1)
            double31 = double_3 + double_0
            double1 = math.pi / 2 + double_1
            num1 = math.sqrt(double2 * double2 + double31 * double31 - 2 * double2 * double31 * math.cos(double1))
            return num1 - double_3
        if (double_3 <= 0):
            return double_2 * math.tan(double_1) + double_0
        double21 = double_2 / math.cos(math.fabs(double_1))
        double32 = double_3 + double_0
        num2 = math.pi / 2 - math.fabs(double_1)
        num3 = math.sqrt(double21 * double21 + double32 * double32 - 2 * double21 * double32 * math.cos(num2))
        return num3 - double_3
    
    @staticmethod
    def smethod_192(double_0, double_1, double_2, double_3, double_4):
        if (MathHelper.smethod_96(double_1) or math.isinf(double_1) or math.isnan(double_1)):
            if (double_4 <= 0):
                return double_3
            double4 = double_4 + double_0
            num = double_4 + double_2
            return math.sqrt(num * num - double4 * double4)
        if (double_1 > 0):
            if (double_4 <= 0):
                return (double_2 - double_0) / math.tan(double_1)
            double41 = double_4 + double_2
            double1 = math.pi / 2 + double_1
            num1 = double_4 + double_0
            num2 = math.asin(num1 * math.sin(double1) / double41)
            num3 = math.pi - (num2 + double1)
            num4 = math.sqrt(num1 * num1 + double41 * double41 - 2 * num1 * double41 * math.cos(num3))
            return num4 * math.cos(double_1)
        if (double_4 <= 0):
            return math.fabs((double_2 - double_0) / math.tan(double_1))
        double42 = double_4 + double_2
        num5 = math.pi / 2 - math.fabs(double_1)
        double43 = double_4 + double_0
        num6 = math.pi / 2 - math.asin(double43 * math.sin(num5) / double42) + 1.5707963267949
        num7 = math.pi - (num6 + num5)
        num8 = math.sqrt(double43 * double43 + double42 * double42 - 2 * double43 * double42 * math.cos(num7))
        return num8 * math.cos(math.fabs(double_1))
    
    @staticmethod
    def CrsTransformPoint(X, Y, inputCrs, outputCrs, altitude = 0):
        crsTransform = QgsCoordinateTransform (inputCrs, outputCrs)
        qgsPoint = crsTransform.transform(X, Y)
        return Point3D(qgsPoint.x(), qgsPoint.y(), altitude)
    @staticmethod    
    def smethod_193(point3d_0, double_0, point3d_1, double_1, point3d_2, double_2, bool_0):
        if define._units != QGis.Meters:
            # double_0 = define._qgsDistanceArea.convertMeasurement(double_0, QGis.Meters, QGis.Degrees, False)[0]
            # double_1 = define._qgsDistanceArea.convertMeasurement(double_1, QGis.Meters, QGis.Degrees, False)[0]
            # double_2 = define._qgsDistanceArea.convertMeasurement(double_2, QGis.Meters, QGis.Degrees, False)[0]# (double &measure, QGis::UnitType &measureUnits, QGis::UnitType displayUnits, bool isArea)
            point3d_0 = MathHelper.CrsTransformPoint(point3d_0.get_X(), point3d_0.get_Y(), define._latLonCrs, define._xyCrs, point3d_0.get_Z())
            point3d_1 = MathHelper.CrsTransformPoint(point3d_1.get_X(), point3d_1.get_Y(), define._latLonCrs, define._xyCrs, point3d_1.get_Z())
            point3d_2 = MathHelper.CrsTransformPoint(point3d_2.get_X(), point3d_2.get_Y(), define._latLonCrs, define._xyCrs, point3d_2.get_Z())
        x = point3d_0.get_X()
        y = point3d_0.get_Y()
        num = point3d_1.get_X()
        y1 = point3d_1.get_Y()
        x1 = point3d_2.get_X()
        num1 = point3d_2.get_Y()

        num2 = 1 if(not bool_0) else -1
        num3 = 1 if(not bool_0) else -1
        num4 = 1 if(not bool_0) else -1
        num5 = 2 * num - 2 * x
        num6 = 2 * y1 - 2 * y
        double0 = x * x - num * num + y * y - y1 * y1 - double_0 * double_0 + double_1 * double_1
        double1 = (2 * num3) * double_1 - (2 * num2) * double_0
        num7 = 2 * x1 - 2 * num
        num8 = 2 * num1 - 2 * y1
        double11 = num * num - x1 * x1 + y1 * y1 - num1 * num1 - double_1 * double_1 + double_2 * double_2
        double2 = (2 * num4) * double_2 - (2 * num3) * double_1
        num9 = num6 / num5
        num10 = double0 / num5
        num11 = double1 / num5
        num12 = num8 / num7 - num9
        num13 = double11 / num7 - num10
        num14 = double2 / num7 - num11
        num15 = -num13 / num12
        num16 = num14 / num12
        num17 = -num9 * num15 - num10
        num18 = num11 - num9 * num16
        num19 = num18 * num18 + num16 * num16 - 1
        double01 = 2 * num17 * num18 - 2 * num18 * x + 2 * num15 * num16 - 2 * num16 * y + (2 * num2) * double_0
        double02 = x * x + num17 * num17 - 2 * num17 * x + num15 * num15 + y * y - 2 * num15 * y - double_0 * double_0
        num20 = double01 * double01 - 4 * num19 * double02
        num21 = (-double01 - math.sqrt(num20)) / (2 * num19)
        if (num21 == None):
            raise "NoneType is raised!"
        num22 = num17 + num18 * num21
        num23 = num15 + num16 * num21
        point3d_3 = Point3D(num22, num23, 0)
        double_3 = num21
        # if define._units != QGis.Meters:
        #     double_3 = define._qgsDistanceArea.convertMeasurement(num21, QGis.Degrees, QGis.Meters, False)[0]
        if define._units != QGis.Meters:
            point3d_3 = MathHelper.CrsTransformPoint(point3d_3.get_X(), point3d_3.get_Y(), define._xyCrs, define._latLonCrs, point3d_3.get_Z())

        return point3d_3, double_3

class Unit:
    def __init__(self):
        pass
    
    @staticmethod
    def ConvertDegToRad(degree): 
        if degree == None:
            return None        
        return math.pi * float(degree) / 180

    @staticmethod
    def ConvertRadToDeg(degree): 
        if degree == None:
            return None        
        return 180 * float(degree) / math.pi
    
    @staticmethod
    def ConvertFeetToMeter(feet):
        if feet == None:
            return None        
        return feet * 0.3048
    @staticmethod
    def ConvertFeetToNM(feet):
        if feet == None:
            return None        
        return Unit.ConvertMeterToNM(feet * 0.3048)

    @staticmethod
    def ConvertMeterToFeet(meter):
        if meter == None:
            return None        
        return meter / 0.3048
    
    # Unit.smethod_22
    @staticmethod
    def ConvertNMToMeter(nm):
        if nm == None:
            return None        
        return nm * 1.852 * 1000.0
    
    @staticmethod
    def ConvertKTSToMPS(kts):
        if kts == None:
            return None        
        return Unit.ConvertNMToMeter(kts / 3600.0)
    
    @staticmethod
    def ConvertKMToMeters(km):
        if km == None:
            return None
        return km * 1000.0
    
    @staticmethod
    def ConvertKMToNM(km):
        if km == None:
            return None
        return km / 1.852
    
    @staticmethod
    def ConvertKMToFeet(km):
        if km == None:
            return None
        return km* 1000.0 / 0.3048
    
    @staticmethod
    def ConvertMeterToNM(meter):
        return Unit.ConvertKMToNM(meter / 1000)
    # Unit.smethod_1
    # return double
    # input double
    
    @staticmethod 
    def smethod_0(double_0):
        if double_0 == None:
            return None        
        return double_0 * math.pi / 180
    @staticmethod 
    def smethod_1(double_0):
        if double_0 == None:
            return None        
        return double_0 * 57.2957795130823

    @staticmethod
    def smethod_2(double_0):
        return math.tan(Unit.ConvertDegToRad(double_0)) * 100
    
    @staticmethod
    def smethod_3(double_0):
        return Unit.smethod_1(math.atan(double_0 / float(100)))

    @staticmethod
    def smethod_4( double_0):
        return math.tan(double_0) * 100

    @staticmethod
    def smethod_5(double_0):
        return math.atan(double_0 / float(100))

    @staticmethod
    def smethod_6( double_0):
        return 1 / math.tan(Unit.ConvertDegToRad(double_0))

    @staticmethod
    def smethod_7( double_0):
        return Unit.smethod_1(math.atan(1 / double_0))

    @staticmethod
    def smethod_8( double_0):
        return 1 / math.tan(double_0)

    @staticmethod
    def smethod_9(double_0):
        return math.atan(1 / double_0)

    @staticmethod
    def smethod_13(double_0):
        return double_0 / 1000

    @staticmethod 
    def smethod_21(double_0):
        return double_0 * 1.852

class Point3dCollection(list):
    def __init__(self, list_0 = None):
        if list_0 == None:
            list.__init__(self)
        else:
            list.__init__(self)
            for point in list_0:
                self.append(point)
    
    
    def Add(self, point3d):
        self.append(point3d)
        
        
    def get_Item(self, idx):
        return self[idx]
    
    
    def get_Count(self):
        return len(self)
    Count = property(get_Count, None, None, None)
    
    
    def Clear(self):
        while len(self) > 0:
            self.pop()
    
    
    def Contains(self, value):
        return value in self
    
    
    def IndexOf(self, value):
        return self.index(value)
    
    
    def Insert(self, index, value):
        self.insert(index, value)
        
        
    def Remove(self, value):
        self.remove(value)
        
        
    def RemoveAt(self, index):
        self.pop(index)
        
        
    # Remove repeatation same points
    @staticmethod
    def smethod_146(point3dCollection_0):    
        point3d = Point3D()
        num = 0
        i = len(point3dCollection_0)
        while ( num < i):
            if (i < 2):
                return
            if num != i - 1:
                point3d = point3dCollection_0[num + 1]
            else: 
                point3d = point3dCollection_0[0]
            if (not point3dCollection_0[num].smethod_170(point3d)):
                num += 1
            else:
                point3dCollection_0.pop(num)
            i = len(point3dCollection_0)

# internal struct Speed : IComparable<Speed>, IEquatable<Speed>, IFormattable
class Speed:
    
    def __init__(self, double_0, SpeedUnits_0 = SpeedUnits.KTS):

        self.originalUnit = SpeedUnits_0
        if (SpeedUnits_0 != SpeedUnits.KMH):
            self.valueKnots = double_0
            return
        self.valueKnots = Unit.smethod_18(double_0)

    def get_knots(self):
        return self.valueKnots


    def get_metres_per_second(self):
        return Unit.ConvertNMToMeter(self.valueKnots / 3600)


    def get_kilometres_per_hour(self):
        return Unit.smethod_21(self.valueKnots)


    def IsNaN(self):
        return self.valueKnots == None

    def IsValid(self):
        return self.valueKnots != None

    def KilometresPerHour(self):
        return Unit.smethod_21(self.valueKnots)

    def Knots(self):
        return self.valueKnots

    def MetresPerSecond(self):
        return Unit.ConvertNMToMeter(self.valueKnots / 3600)

    @staticmethod
    def NaN():
        return Speed(None)

    def OriginalUnit(self):
        return self.originalUnit
    def OriginalUnits_ToString(self):
        if self.originalUnit == SpeedUnits.KMH:
            return "km/h"
        else:
            return "kts"

    def CompareTo(self, other):
        return self.valueKnots.CompareTo(other.valueKnots)

    def Equals(self, obj):
        if (not (obj is Speed)):
            return False
        return self.valueKnots == obj.valueKnots

    def method_0(self, string_0):
        return str(string_0)

    def method_1(self, iformatProvider_0 = None):
        return "G"

    def __add__(self, other):
        if other == None or self.valueKnots == None:
            return None
        if not isinstance(other, Speed):
            other = Speed(other)
        
        return Speed(self.valueKnots + other.valueKnots)
    def __div__(self, b):
        speed = self
        if isinstance(b, Speed):
            speed.Knots = speed.Knots / b.Knots
        else:
            speed.Knots = speed.Knots / b
        return Speed(speed.Knots, SpeedUnits.KTS)



    @staticmethod
    def plus(a, b):
        speed = a
        speed.valueKnots = speed.valueKnots + b.valueKnots
        return speed

    @staticmethod
    def devide(a, b):
        speed = a
        if b is Speed:
            speed.valueKnots = a.valueKnots / b.valueKnots
        else:
            speed.valueKnots = a.valueKnots / b
        return speed

    @staticmethod
    def multiply(a, b):
        speed = a
        if b is Speed:
            speed.valueKnots = a.valueKnots * b.valueKnots
        else:
            speed.valueKnots = a.valueKnots * b
        return speed

    @staticmethod
    def minus(a, b):
        speed = a
        if b is Speed:
            speed.valueKnots = speed.valueKnots - b.valueKnots
        else:
            speed.valueKnots = speed.valueKnots - b
        return speed

    @staticmethod
    def smethod_0(speed_0, double_0, altitude_0):
        try:
            if (speed_0.originalUnit == SpeedUnits.KTS):
                knots = speed_0.Knots * 171233 * math.pow(288 + double_0 - 0.00198 * altitude_0.Feet, 0.5)
                num = math.pow(288 - 0.00198 * altitude_0.Feet, 2.628)
                
                K= round(171233 * math.pow(288 + double_0 - 0.00198 * altitude_0.Feet, 0.5)/(math.pow(288 - 0.00198 * altitude_0.Feet, 2.628)), 4)
                return Speed(knots / num, SpeedUnits.KTS)
            kilometresPerHour = speed_0.KilometresPerHour * 171233 * math.pow(288 + double_0 - 0.006496 * altitude_0.Metres, 0.5)
            num1 = math.pow(288 - 0.006496 * altitude_0.Metres, 2.628)
            return Speed(kilometresPerHour / num1, SpeedUnits.KMH)
        except:
            QMessageBox.warning(None, "Warning", "Altitude's value is too large.")
            return None

    @staticmethod
    def smethod_1(altitude_0):
        if (not altitude_0.IsValid()):
            return Speed.NaN()
        return Speed((87000 + 12 * altitude_0.Metres) / 1852)

    @staticmethod
    def smethod_2(altitude_0):
            if (not altitude_0.IsValid()):
                return Speed.NaN()
            feet = altitude_0.Feet
            if (feet < 10000):
                return Speed(feet / 1000 + 40)
            if (feet >= 10000 and feet < 15000):
                return Speed(11 * (feet / 1000) / 5 + 28)
            if (feet < 15000 or feet >= 30000):
                return Speed(105)
            return Speed(44 * (feet / 1000) / 15 + 17)

    @staticmethod
    def smethod_3(altitude_0, altitude_1):
        if (not altitude_0.IsValid() or not altitude_1.IsValid()):
            return Speed.NaN()
        feet = altitude_0.Feet - altitude_1.Feet
        if (feet < 500):
            num = 0
            num1 = 500
            num2 = 15
            num3 = 25
        elif (feet < 1000):
            num = 500
            num1 = 1000
            num2 = 25
            num3 = 38
        elif (feet >= 1500):
            if (feet < 3000):
                return Speed(50)
            if (feet >= 11000):
                return Speed(130)
            num = 3000
            num1 = 11000
            num2 = 50
            num3 = 130
        else:
            num = 1000
            num1 = 1500
            num2 = 38
            num3 = 50
        return Speed(num2 + (num3 - num2) * (feet - num) / (num1 - num))
    
    @staticmethod
    def smethod_6(string_0, string_1):
        num = None
        if (String.IsNullOrEmpty(string_0) or String.IsNullOrEmpty(string_1)):
            return Speed.NaN()
        try:
            num = float(string_0)
        except:
            return Speed.NaN()
        speedUnit = SpeedUnits.KTS

        if isinstance(string_1, QString):
            string_1 = String.QString2Str(string_1)

        upper0 = string_1.upper()
        strS = upper0
        if (upper0 != None):
            if (strS == "KM/H"):
                speedUnit = SpeedUnits.KMH
            elif (strS == "MACH"):
                num = num * 666.74
            elif (strS == "M/MIN"):
                num = num * 0.0323974082073434
            elif (strS == "FT/MIN"):
                num = num * 0.00987473
            elif (strS == "M/SEC"):
                num = num * 1.9438444924406
            elif (strS == "FT/SEC"):
                num = num * 0.5924838
        return Speed(num, speedUnit)
    
    Knots = property(get_knots, None, None, None)
    MetresPerSecond = property(get_metres_per_second, None, None, None)
    KilometresPerHour = property(get_kilometres_per_hour, None, None, None)
#     @staticmethod
#     def smethod_112(double_0, double_1, double_2, angleUnits_0):
#         if (angleUnits_0 == AngleUnits.Degrees):
#             double_0 = MathHelper.smethod_3(double_0)
#             double_1 = MathHelper.smethod_3(double_1 - 0.1)
#             double_2 = MathHelper.smethod_3(double_2 + 0.1)
#             if (double_2 > double_1):
#                 if (double_0 < double_1):
#                     return False
#                 if double_0 <= double_2:
#                     return True
#                 else:
#                     return False
#             if (double_0 >= double_1 and double_0 <= 360):
#                 return True
#             if (double_0 < 0):
#                 return False
#             if double_0 <= double_2:
#                 return True
#             else:
#                 return False
#         double_0 = MathHelper.smethod_4(double_0)
#         double_1 = MathHelper.smethod_4(double_1 - 0.1)
#         double_2 = MathHelper.smethod_4(double_2 + 0.1)
#         if (double_2 > double_1):
#             if (double_0 < double_1):
#                 return False
#             if double_0 <= double_2:
#                 return True
#             else:
#                 return False
#         if (double_0 >= double_1 and double_0 <= math.pi * 2):
#             return True
#         if (double_0 < 0):
#             return False        
#         if double_0 <= double_2:
#             return True
#         else:
#             return False
  

#     @staticmethod
#     def smethod_4(string_0, SpeedUnits_0):
#         return Speed.smethod_5(string_0, SpeedUnits_0, CultureInfo.CurrentCulture)

#     @staticmethod
#     def smethod_5(string_0, SpeedUnits_0, iformatProvider_0):
#         naN = Speed.NaN()
#         if (not Speed.smethod_8(string_0, SpeedUnits_0, iformatProvider_0, out naN))
#         {
#             throw new Exception(string.Format(Validations.NOT_VALID_SPEED_VALUE, string_0))
#         }
#         return naN

#         public static Speed smethod_6(string string_0, string string_1, IFormatProvider iformatProvider_0)
#         {
#             double num
#             if (string.IsNullOrEmpty(string_0) || string.IsNullOrEmpty(string_1))
#             {
#                 return Speed.NaN
#             }
#             if (!double.TryParse(string_0, NumberStyles.Number, iformatProvider_0, out num))
#             {
#                 return Speed.NaN
#             }
#             SpeedUnits SpeedUnits = SpeedUnits.KTS
#             string upper = string_1.ToUpper()
#             string str = upper
#             if (upper != null)
#             {
#                 if (str == "KM/H")
#                 {
#                     SpeedUnits = SpeedUnits.KMH
#                 }
#                 elif (str == "MACH")
#                 {
#                     num = num * 666.74
#                 }
#                 elif (str == "M/MIN")
#                 {
#                     num = num * 0.0323974082073434
#                 }
#                 elif (str == "FT/MIN")
#                 {
#                     num = num * 0.00987473
#                 }
#                 elif (str == "M/SEC")
#                 {
#                     num = num * 1.9438444924406
#                 }
#                 elif (str == "FT/SEC")
#                 {
#                     num = num * 0.5924838
#                 }
#             }
#             return new Speed(num, SpeedUnits)
#         }

#         public static bool smethod_7(string string_0, SpeedUnits SpeedUnits_0, out Speed speed_0)
#         {
#             return Speed.smethod_8(string_0, SpeedUnits_0, CultureInfo.CurrentCulture, out speed_0)
#         }
# 
#         public static bool smethod_8(string string_0, SpeedUnits SpeedUnits_0, IFormatProvider iformatProvider_0, out Speed speed_0)
#         {
#             double num
#             if (iformatProvider_0 == null)
#             {
#                 iformatProvider_0 = CultureInfo.CurrentCulture
#             }
#             string_0 = string_0.ToUpper()
#             if (string_0.IndexOf(Enums.SpeedUnits_KTS, StringComparison.CurrentCultureIgnoreCase) > -1)
#             {
#                 SpeedUnits_0 = SpeedUnits.KTS
#                 string_0 = string_0.smethod_11(Enums.SpeedUnits_KTS, "", StringComparison.CurrentCultureIgnoreCase)
#             }
#             elif (string_0.IndexOf(Enums.SpeedUnits_KMH, StringComparison.CurrentCultureIgnoreCase) > -1)
#             {
#                 SpeedUnits_0 = SpeedUnits.KMH
#                 string_0 = string_0.smethod_11(Enums.SpeedUnits_KMH, "", StringComparison.CurrentCultureIgnoreCase)
#             }
#             elif (string_0.IndexOf(Enums.SpeedUnits_KMH_1, StringComparison.CurrentCultureIgnoreCase) > -1)
#             {
#                 SpeedUnits_0 = SpeedUnits.KMH
#                 string_0 = string_0.smethod_11(Enums.SpeedUnits_KMH_1, "", StringComparison.CurrentCultureIgnoreCase)
#             }
#             if (!double.TryParse(string_0, NumberStyles.Number, iformatProvider_0, out num))
#             {
#                 speed_0 = Speed.NaN
#                 return false
#             }
#             speed_0 = new Speed(num, SpeedUnits_0)
#             return true
#         }
# 
#         public override string ToString()
#         {
#             return self.ToString("G", CultureInfo.CurrentCulture)
#         }
# 
    def ToString(self, format0 = None):

        speedUnits = self.originalUnit
        flag = False
        if format0.__class__ == QString:
            format0 = String.QString2Str(format0)
        if (self.IsNaN()):
            return ""
        if (String.IsNoneOrEmpty(format0)):
            format0 = "0.#"#Formats.SpeedFormat
        # if (provider == None)
        # {
        #     provider = CultureInfo.CurrentCulture
        # }
        format0 = format0.upper()
        if (format0 == "G"):
            format0 = "0.#"#Formats.SpeedFormat
        elif (format0.find(":U")):
            format0 = format0.replace(":U", "")
            flag = True
        elif (format0.find(":KTS")):
            speedUnits = SpeedUnits.KTS
            format0 = format0.replace(":KTS", "")
            flag = True
        elif (format0.find(":KMH")):
            speedUnits = SpeedUnits.KMH
            format0 = format0.replace(":KMH", "")
            flag = True
        if (String.IsNoneOrEmpty(format0)):
            format0 = "0.#"#Formats.SpeedFormat
        if (speedUnits == SpeedUnits.KTS):
            if (not flag):
                return str(self.Knots)
            knots = self.Knots
            return "{0} {1}".format(str(knots), "kts")
        if (not flag):
            return str(self.KilometresPerHour)
        kilometresPerHour = self.KilometresPerHour
        return "{0} {1}".format(str(kilometresPerHour), "km/h")

class Altitude :
    
    def __init__(self, double_0, altitudeUnit_0 = None):

        if altitudeUnit_0 == None:
            self.originalUnit = AltitudeUnits.M
            self.valueMetres = double_0
        else:
            self.originalUnit = altitudeUnit_0
            if altitudeUnit_0 == AltitudeUnits.FT:
                self.valueMetres = Unit.ConvertFeetToMeter(double_0)
                return
            elif altitudeUnit_0 == AltitudeUnits.FL:
                self.valueMetres = Unit.ConvertFeetToMeter(double_0 * 100)
                return
            elif altitudeUnit_0 == AltitudeUnits.SM:
                self.valueMetres = double_0 * 10
                return
            else:
                self.valueMetres = double_0
                return
    def get_OriginalUnits(self):
        if self.originalUnit == AltitudeUnits.M:
            return "m"
        elif self.originalUnit == AltitudeUnits.FT:
            return "ft"
        elif self.originalUnit == AltitudeUnits.FL:
            return "fl"
        elif self.originalUnit == AltitudeUnits.SM:
            return "sm"
        else:
            return ""
    OriginalUnits = property(get_OriginalUnits, None, None, None)
    def get_metres(self):
        return self.valueMetres


    def get_feet(self):
        return Unit.ConvertMeterToFeet(self.valueMetres)


    def get_flight_level(self):
        return Unit.ConvertMeterToFeet(self.valueMetres) / 100


    def get_standard_metres(self):
        return self.valueMetres / 10


    def Feet(self):
        return Unit.ConvertMeterToFeet(self.valueMetres)

    def FlightLevel(self):
        return Unit.ConvertMeterToFeet(self.valueMetres) / 100

    def IsNaN(self):
        return self.valueMetres is None

    def IsValid(self):
        return self.valueMetres is not None

    def IsZero(self):
        return MathHelper.smethod_96(self.valueMetres)

    def Metres(self):
        return self.valueMetres
    @staticmethod
    def NaN():
        return Altitude(None)

    def OriginalUnit(self):
        return self.originalUnit
    def OriginalUnits_ToString(self):
        if self.originalUnit == AltitudeUnits.M:
            return "m"
        elif self.originalUnit == AltitudeUnits.FT:
            return "ft"
        elif self.originalUnit == AltitudeUnits.FL:
            return "FL"
        else:
            return "SM"

    def StandardMetres(self):
        return self.valueMetres / 10

# 
#         public int CompareTo(Altitude other)
#         {
#             return self.valueMetres.CompareTo(other.valueMetres)
#         }
# 
#         public int CompareTo(object obj)
#         {
#             if (obj is Altitude)
#             {
#                 return self.CompareTo((Altitude)obj)
#             }
#             return self.valueMetres.CompareTo(obj)
#         }

#         public bool Equals(Altitude other)
#         {
#             return self.valueMetres.Equals(other.valueMetres)
#         }

    def Equals(self, obj):
        if (not obj is Altitude):
            return False
        return self.valueMetres == obj.valueMetres

#         public override int GetHashCode()
#         {
#             return self.valueMetres.GetHashCode()
#         }

#         public string method_0(string string_0)
#         {
#             return self.ToString(string_0, CultureInfo.CurrentCulture)
#         }
# 
#         public string method_1(IFormatProvider iformatProvider_0)
#         {
#             return self.ToString("G", iformatProvider_0)
#         }
    def method_0(self, formatString):
        if self.Feet == None:
            return "0.0"
        if self.originalUnit == AltitudeUnits.FT:
            return str(round(self.Feet, 4)) + " ft"
        elif self.originalUnit == AltitudeUnits.M:
            return str(round(self.Metres, 4)) + " m"
        elif self.originalUnit == AltitudeUnits.FL:
            return str(round(self.FlightLevel, 4)) + " fl"
        elif self.originalUnit == AltitudeUnits.SM:
            return str(round(self.StandardMetres, 4)) + " sm"


    @staticmethod
    def smethod_0(string_0, altitudeUnits_0):
        return Altitude.smethod_1(string_0, altitudeUnits_0)

    @staticmethod
    def smethod_1(string_0, altitudeUnits_0):
        naN = Altitude.NaN()
        result, naN = Altitude.smethod_3(string_0, altitudeUnits_0)
        if (not result):
            raise Validations.NOT_VALID_ALTITUDE_VALUE.format(string_0)
            # throw new Exception(string.Format(Validations.NOT_VALID_ALTITUDE_VALUE, string_0))
        return naN

    @staticmethod
    def smethod_2(string_0, altitudeUnits_0):
        return Altitude.smethod_3(string_0, altitudeUnits_0)

    @staticmethod
    def smethod_3(string_0, altitudeUnits_0):
        num = None
        # if (iformatProvider_0 == null)
        # {
        #     iformatProvider_0 = CultureInfo.CurrentCulture
        # }
        if not isinstance(string_0, QString):
            string_0 = QString(string_0)
        string_0 = string_0.trimmed()
        if (string_0.indexOf("FL") > -1):
            altitudeUnits_0 = AltitudeUnits.FL
            string_0 = Extensions.smethod_11(string_0, "FL", "").trimmed()
        elif (string_0.indexOf("SM") > -1):
            altitudeUnits_0 = AltitudeUnits.SM
            string_0 = Extensions.smethod_11(string_0, "SM", "").trimmed()
        elif (string_0.indexOf("FT") > -1):
            altitudeUnits_0 = AltitudeUnits.FT
            string_0 = Extensions.smethod_11(string_0, "FT", "").trimmed()
        elif (string_0.indexOf("M") > -1):
            altitudeUnits_0 = AltitudeUnits.M
            string_0 = Extensions.smethod_11(string_0, "M", "").trimmed()
        try:
            num = float(string_0)
            altitude_0 = Altitude(num, altitudeUnits_0)
            return True, altitude_0
        except:
            altitude_0 = Altitude.NaN
            return False, None


    @staticmethod
    def smethod_4(string_0, string_1):
        num = None
        if (string_0 == "" or string_1 == ""):
            return None
        try:
            num = float(string_0)#.toDouble()
        except:
            return None
        if string_1 == "M":            
            return Altitude(num)
        elif string_1 == "FT":
            return Altitude(num, AltitudeUnits.FT)
        elif string_1 == "FL":
            return Altitude(num, AltitudeUnits.FL)
        else:
            return Altitude(num, AltitudeUnits.SM)
    @staticmethod
    def add(a, b):
        altitude = a
        if isinstance(b, Altitude):
            altitude.valueMetres = altitude.valueMetres + b.valueMetres
        else:
            altitude.valueMetres = altitude.valueMetres + b
        return altitude

    def __add__(self, b):
        altitude = self
        if isinstance(b, Altitude):
            altitude.valueMetres = altitude.valueMetres + b.valueMetres
        else:
            altitude.valueMetres = altitude.valueMetres + b
        return altitude

        
    @staticmethod
    def div(a, b):
        altitude = a
        if isinstance(b, Altitude):
            altitude.valueMetres = altitude.valueMetres / b.valueMetres
        else:
            altitude.valueMetres = altitude.valueMetres / b
        return altitude
    
    def __div__(self, b):
        altitude = self
        if isinstance(b, Altitude):
            altitude.valueMetres = altitude.valueMetres / b.valueMetres
        else:
            altitude.valueMetres = altitude.valueMetres / b
        return altitude

    @staticmethod
    def equals(a, b):
        return a.valueMetres == b.valueMetres

    def __eq__(self, b):
        if b == None:
            return self.valueMetres == None
        return self.valueMetres == b.valueMetres

    @staticmethod
    def mul(a, b):
        altitude = a
        if isinstance(b, Altitude):
            altitude.valueMetres = altitude.valueMetres * b.valueMetres
        else:
            altitude.valueMetres = altitude.valueMetres * b
        return altitude
    
    def __mul__(self, b):
        altitude = self
        if isinstance(b, Altitude):
            altitude.valueMetres = altitude.valueMetres * b.valueMetres
        else:
            altitude.valueMetres = altitude.valueMetres * b
        return altitude

    @staticmethod
    def sub(a, b):
        altitude = a
        if isinstance(b, Altitude):
            altitude.valueMetres = altitude.valueMetres - b.valueMetres
        else:
            altitude.valueMetres = altitude.valueMetres - b
        return altitude

    def __sub__(self, b):
        altitude = self
        if isinstance(b, Altitude):
            altitude.valueMetres = altitude.valueMetres - b.valueMetres
        else:
            altitude.valueMetres = altitude.valueMetres - b
        return altitude
    Metres = property(get_metres, None, None, None)
    Feet = property(get_feet, None, None, None)
    FlightLevel = property(get_flight_level, None, None, None)
    StandardMetres = property(get_standard_metres, None, None, None)

    def ToString(self, format0 = None):
        altitudeUnit = self.originalUnit
        flag = False
        if format0.__class__ == QString:
            format0 = String.QString2Str(format0)
        if (self.IsNaN()):
            return ""
        if (String.IsNullOrEmpty(format0)):
            format0 = "0.##"#format0s.Altitudeformat0
        # if (provider == null)
        # {
        #     provider = CultureInfo.CurrentCulture
        # }
        format0 = format0.upper()
        if (format0 == "G"):
            format0 = "0.##"#format0s.Altitudeformat0
        elif (format0.find(":U")):
            format0 = format0.replace(":U", "")
            flag = True
        elif (format0.find(":M")):
            altitudeUnit = AltitudeUnits.M
            format0 = format0.replace(":M", "")
            flag = True
        elif (format0.find(":FT")):
            altitudeUnit = AltitudeUnits.FT
            format0 = format0.replace(":FT", "")
            flag = True
        elif (format0.find(":FL")):
            altitudeUnit = AltitudeUnits.FL
            format0 = format0.replace(":FL", "")
            flag = True
        elif (format0.find(":SM")):
            altitudeUnit = AltitudeUnits.SM
            format0 = format0.replace(":SM", "")
            flag = True
        if (String.IsNullOrEmpty(format0)):
            format0 = "0.##"#format0s.Altitudeformat0

        if altitudeUnit == AltitudeUnits.FT:
            if (not flag):
                return str(self.Feet)
            feet = self.Feet
            return "{0} {1}".format(str(feet), "ft")
        elif altitudeUnit == AltitudeUnits.FL:
            if (not flag):
                return str(self.FlightLevel)
            altitudeUnitsFL = "FL"
            num = self.FlightLevel
            return "{0} {1}".format(str(num), altitudeUnitsFL)
        elif altitudeUnit == AltitudeUnits.SM:
            if (not flag):
                return self.StandardMetres#.smethod_16(0).ToString()
            num1 = self.StandardMetres#.smethod_16(0)
            return "{0} {1}".format(str(num1), "SM")
        else:
            if (not flag):
                pass
            else:
                metres = self.Metres
                return "{0} {1}".format(str(metres), "m")
        return str(self.Metres)#.ToString(format0, provider)
        

class AngleGradientSlope:

    def __init__(self, double_0, angleGradientSlopeUnits_0 = AngleGradientSlopeUnits.Degrees):
        self.originalUnits = angleGradientSlopeUnits_0
        if double_0 == None:
            self.valueDegrees = 0.0
            return
        
        if angleGradientSlopeUnits_0 == AngleGradientSlopeUnits.Percent:
            self.valueDegrees = Unit.smethod_3(double_0)
            return
        elif angleGradientSlopeUnits_0 == AngleGradientSlopeUnits.Slope:
            self.valueDegrees = Unit.smethod_7(double_0)
            return
        else:
            self.valueDegrees = double_0
            return
    def method_0(self, string_0):
        return self.ToString(string_0)
    def ToString(self, format0):
        if format0 == None:
            self.ToString("G")
        angleGradientSlopeUnit = self.originalUnits
        flag = False
        if (self.IsNaN()):
            return ""
        if (String.IsNullOrEmpty(format0)):
            format0 = self.defaultFormat
        # if (provider == null)
        # {
        #     provider = CultureInfo.CurrentCulture
        # }
        if isinstance(format0, str):
            format0 = String.Str2QString(format0)
        format0 = format0.toUpper()
        if (format0 == "G"):
            format0 = String.Str2QString(self.defaultFormat)
        elif (format0.contains((":U"))):
            format0 = format0.replace(":U", "").trimmed()
            flag = True
        elif (format0.contains(":D")):
            angleGradientSlopeUnit = AngleGradientSlopeUnits.Degrees
            format0 = format0.replace(":D", "").trimmed()
            flag = True
        elif (format0.contains(":%")):
            angleGradientSlopeUnit = AngleGradientSlopeUnits.Percent
            format0 = format0.replace(":%", "").trimmed()
            flag = True
        elif (format0.contains(":S")):
            angleGradientSlopeUnit = AngleGradientSlopeUnits.Slope
            format0 = format0.replace(":S", "").trimmed()
            flag = True
        if (String.IsNullOrEmpty(format0)):
            format0 = String.Str2QString(self.defaultFormat)

        if angleGradientSlopeUnit == AngleGradientSlopeUnits.Percent:
            if (not flag):
                return str(self.Percent)#.ToString(format0, provider)
            percent = self.Percent
            return "{0} {1}".format(str(percent), Enums.AngleGradientSlopeUnits_Percent)
        elif angleGradientSlopeUnit ==  AngleGradientSlopeUnits.Slope:
            angleGradientSlopeUnitsSlope = Enums.AngleGradientSlopeUnits_Slope
            slope = self.Slope
            return String.Concat([angleGradientSlopeUnitsSlope, str(slope)])
        else:
            if (not flag):
                pass
            else:
                degrees = self.Degrees
                return "{0} {1}".format(degrees.ToString(format0), Enums.AngleGradientSlopeUnits_Degrees)
        return str(self.Degrees)#self.Degrees.ToString(format0)
    def get_radians(self):
        return Unit.ConvertDegToRad(self.valueDegrees)


    def get_degrees(self):
        return self.valueDegrees


    def get_percent(self):
        return Unit.smethod_2(self.valueDegrees)


    def get_slope(self):
        return Unit.smethod_6(self.valueDegrees)


    def Abs(self):
        if (self.originalUnits == AngleGradientSlopeUnits.Percent):
            return AngleGradientSlope(math.fabs(self.Percent), AngleGradientSlopeUnits.Percent)
        if (self.originalUnits != AngleGradientSlopeUnits.Slope):
            return AngleGradientSlope(math.fabs(self.Degrees))
        return AngleGradientSlope(math.fabs(self.Slope), AngleGradientSlopeUnits.Slope)

    def get_defaultFormat(self):
        if self.originalUnits == AngleGradientSlopeUnits.Percent:
            return Formats.GradientFormat
        elif self.originalUnits ==  AngleGradientSlopeUnits.Slope:
            return Formats.SlopeFormat
        else:
            return Formats.AngleFormat
    defaultFormat = property(get_defaultFormat, None, None, None)
    def Degrees(self):
        return self.valueDegrees

    def IsNaN(self):
        return self.valueDegrees == None

    def IsValid(self):
        return self.valueDegrees != None

    def IsZero(self):
        return MathHelper.smethod_96(self.valueDegrees)

    @staticmethod
    def NaN():
        return AngleGradientSlope(None)

    def OriginalUnits(self):
        return self.originalUnits

    def Percent(self):
        return Unit.smethod_2(self.valueDegrees)

    def Radians(self):
        return Unit.ConvertDegToRad(self.valueDegrees)

    def Slope(self):
        return Unit.smethod_6(self.valueDegrees)

    def CompareTo(self, other):
        return self.valueDegrees == other.valueDegrees
    Radians = property(get_radians, None, None, None)
    Degrees = property(get_degrees, None, None, None)
    Percent = property(get_percent, None, None, None)
    Slope = property(get_slope, None, None, None)

    def __eq__(self, other):
        return self.valueDegrees == other.valueDegrees
# 

# 
    def __add__(self, b):
        angleGradientSlope = AngleGradientSlope(0)
        if isinstance(b, AngleGradientSlope):
            angleGradientSlope.valueDegrees = self.valueDegrees + b.valueDegrees
        else:
            angleGradientSlope.valueDegrees = self.valueDegrees + b
        return angleGradientSlope
    def __div__(self, b):
        angleGradientSlope = AngleGradientSlope(0)
        if isinstance(b, AngleGradientSlope):
            angleGradientSlope.valueDegrees = self.valueDegrees / b.valueDegrees
        else:
            angleGradientSlope.valueDegrees = self.valueDegrees / b
        return angleGradientSlope

    def __sub__(self, b):
        angleGradientSlope = AngleGradientSlope(0)
        if isinstance(b, AngleGradientSlope):
            angleGradientSlope.valueDegrees = self.valueDegrees - b.valueDegrees
        else:
            angleGradientSlope.valueDegrees = self.valueDegrees - b
        return angleGradientSlope
    def __mul__(self, b):
        angleGradientSlope = AngleGradientSlope(0)
        if isinstance(b, AngleGradientSlope):
            angleGradientSlope.valueDegrees = self.valueDegrees * b.valueDegrees
        else:
            angleGradientSlope.valueDegrees = self.valueDegrees * b
        return angleGradientSlope

    @staticmethod
    def smethod_0(string_0, angleGradientSlopeUnits_0):
        return AngleGradientSlope.smethod_1(string_0, angleGradientSlopeUnits_0)

    @staticmethod
    def smethod_1(string_0, angleGradientSlopeUnits_0):
        angleGradientSlope = None
        result, angleGradientSlope = AngleGradientSlope.smethod_3(string_0, angleGradientSlopeUnits_0)
        if (not result):
            raise UserWarning, Validations.NOT_VALID_ANGLE_GRADIENT_SLOPE_VALUE.format(string_0)
        return angleGradientSlope

    @staticmethod
    def smethod_2(string_0, angleGradientSlopeUnits_0):
        return AngleGradientSlope.smethod_3(string_0, angleGradientSlopeUnits_0)

    @staticmethod
    def smethod_3(string_0, angleGradientSlopeUnits_0):
        num = None
        # if (iformatProvider_0 == null)
        # {
        #     iformatProvider_0 = CultureInfo.CurrentCulture
        # }
        string_0 = String.Str2QString(string_0)
        string_0 = string_0.replace(" ", "").toUpper()
        if (string_0.indexOf(Enums.AngleGradientSlopeUnits_Degrees) > -1):
            angleGradientSlopeUnits_0 = AngleGradientSlopeUnits.Degrees
            string_0 = String.smethod_11(string_0, Enums.AngleGradientSlopeUnits_Degrees, "")
        elif (string_0.indexOf(Enums.AngleGradientSlopeUnits_Degrees_1) > -1):
            angleGradientSlopeUnits_0 = AngleGradientSlopeUnits.Degrees
            string_0 = String.smethod_11(string_0, Enums.AngleGradientSlopeUnits_Degrees_1, "")
        elif (string_0.indexOf(Enums.AngleGradientSlopeUnits_Percent) > -1):
            angleGradientSlopeUnits_0 = AngleGradientSlopeUnits.Percent
            string_0 = String.smethod_11(string_0, Enums.AngleGradientSlopeUnits_Percent, "")
        elif (string_0.indexOf(Enums.AngleGradientSlopeUnits_Slope) > -1):
            angleGradientSlopeUnits_0 = AngleGradientSlopeUnits.Slope
            string_0 = String.smethod_11(string_0, Enums.AngleGradientSlopeUnits_Slope, "")
        elif (string_0.indexOf(Enums.AngleGradientSlopeUnits_Slope_1) > -1):
            angleGradientSlopeUnits_0 = AngleGradientSlopeUnits.Slope
            string_0 = String.smethod_11(string_0, Enums.AngleGradientSlopeUnits_Slope_1, "")
        try:
            num = float(string_0)
        except:
            angleGradientSlope_0 = AngleGradientSlope(None)
            return False, angleGradientSlope_0
        angleGradientSlope_0 = AngleGradientSlope(num, angleGradientSlopeUnits_0)
        return True, angleGradientSlope_0

class Distance:
    def __init__(self, double_0 , distanceUnits_0 = DistanceUnits.M):
#         if double_0 == None:
#             self.valueMetres = None
#             return
        self.originalUnits = distanceUnits_0
        if distanceUnits_0 == DistanceUnits.FT:
            self.valueMetres = Unit.ConvertFeetToMeter(double_0)
            return
        elif distanceUnits_0 == DistanceUnits.KM:
            self.valueMetres = Unit.ConvertKMToMeters(double_0)
            return
        elif distanceUnits_0 == DistanceUnits.NM:
            self.valueMetres = Unit.ConvertNMToMeter(double_0)
            return
        elif distanceUnits_0 == DistanceUnits.MM:
            self.valueMetres = int(double_0 / 1000)
            return
        else:
            self.valueMetres = double_0
            return

    def get_feet(self):
        return Unit.ConvertMeterToFeet(self.valueMetres)


    def get_kilometres(self):
        return self.valueMetres / 1000.0


    def get_metres(self):
        return self.valueMetres


    def get_nautical_miles(self):
        return Unit.ConvertMeterToNM(self.valueMetres)

    def __add__(self, other):
        if other == None or self.Metres == None:
            return None
        if not isinstance(other, Distance):
            other = Distance(other)

        return Distance(self.Metres + other.Metres)
    def __div__(self, other):
        if other == None or self.Metres == None:
            return None
        if not isinstance(other, Distance):
            return Distance(self.Metres / other)

        return Distance(self.Metres / other.Metres)

    def Feet(self):
        return Unit.ConvertMeterToFeet(self.valueMetres)

    def IsNaN(self):
        return self.valueMetres == None

    def IsValid(self):
        return self.valueMetres != None

    def IsZero(self):
        return MathHelper.smethod_96(self.valueMetres)

    def Kilometres(self):
        return self.valueMetres / 1000.0

    def Metres(self):
        return self.valueMetres
    def get_milimeters(self):
        return int(self.valueMetres * 1000)

    @staticmethod
    def NaN():
        return Distance(None)

    def NauticalMiles(self):
        return Unit.ConvertMeterToNM(self.valueMetres)

    def OriginalUnits(self):
        return self.originalUnits

#     public int CompareTo(Distance other)
#     {
#         return self.valueMetres.CompareTo(other.valueMetres)
#     }
# 
#     public int CompareTo(object obj)
#     {
#         if (obj is Distance)
#         {
#             return self.CompareTo((Distance)obj)
#         }
#         return self.valueMetres.CompareTo(obj)
#     }
# 
#     public bool Equals(Distance other)
#     {
#         return self.valueMetres.Equals(other.valueMetres)
#     }
# 
#     public override bool Equals(object obj)
#     {
#         if (!(obj is Distance))
#         {
#             return false
#         }
#         return self.valueMetres == ((Distance)obj).valueMetres
#     }
# 
#     public override int GetHashCode()
#     {
#         return self.valueMetres.GetHashCode()
#     }
# 
#     public string method_0(string string_0)
#     {
#         return self.ToString(string_0, CultureInfo.CurrentCulture)
#     }
# 
#     public string method_1(IFormatProvider iformatProvider_0)
#     {
#         return self.ToString("G", iformatProvider_0)
#     }
# 
#     public static Distance operator +(Distance a, Distance b)
#     {
#         Distance distance = a
#         distance.valueMetres = distance.valueMetres + b.valueMetres
#         return distance
#     }
# 
#     public static Distance operator +(Distance a, double b)
#     {
#         Distance distance = a
#         distance.valueMetres = distance.valueMetres + b
#         return distance
#     }
# 
#     public static Distance operator /(Distance a, Distance b)
#     {
#         Distance distance = a
#         distance.valueMetres = a.valueMetres / b.valueMetres
#         return distance
#     }
# 
#     public static Distance operator /(Distance a, double b)
#     {
#         Distance distance = a
#         distance.valueMetres = a.valueMetres / b
#         return distance
#     }
# 
#     public static Distance operator /(Distance a, int b)
#     {
#         Distance distance = a
#         distance.valueMetres = a.valueMetres / (double)b
#         return distance
#     }
# 
#     public static bool operator ==(Distance a, Distance b)
#     {
#         return a.valueMetres == b.valueMetres
#     }
# 
#     public static bool operator !=(Distance a, Distance b)
#     {
#         return a.valueMetres != b.valueMetres
#     }
# 
#     public static Distance operator *(Distance a, Distance b)
#     {
#         Distance distance = a
#         distance.valueMetres = a.valueMetres * b.valueMetres
#         return distance
#     }
# 
#     public static Distance operator *(Distance a, double b)
#     {
#         Distance distance = a
#         distance.valueMetres = a.valueMetres * b
#         return distance
#     }
# 
#     public static Distance operator *(Distance a, int b)
#     {
#         Distance distance = a
#         distance.valueMetres = a.valueMetres * (double)b
#         return distance
#     }
# 
#     public static Distance operator -(Distance a, Distance b)
#     {
#         Distance distance = a
#         distance.valueMetres = distance.valueMetres - b.valueMetres
#         return distance
#     }
# 
#     public static Distance operator -(Distance a, double b)
#     {
#         Distance distance = a
#         distance.valueMetres = distance.valueMetres - b
#         return distance
#     }
# 
    @staticmethod
    def smethod_0(speed_0, double_0):
        return1 = []
        return Distance.smethod_1(speed_0, double_0, return1)
# 
    @staticmethod
    def smethod_1(speed_0, double_0, return1): #double_1)
        double_1 = 3431 * math.tan(Unit.ConvertDegToRad(double_0)) / (math.pi * speed_0.Knots)
        if double_1 > 3:
            double_1 = 3
        return1.append(double_1)
        return Distance(Unit.ConvertNMToMeter(speed_0.Knots / (math.pi * double_1 * 20)))
    Feet = property(get_feet, None, None, None)
    Kilometres = property(get_kilometres, None, None, None)
    Metres = property(get_metres, None, None, None)
    NauticalMiles = property(get_nautical_miles, None, None, None)
    Milimeters = property(get_milimeters, None, None, None)
 
    @staticmethod
    def smethod_2(distance_0):
        return Distance(0.25 + 0.0125 * distance_0.NauticalMiles, DistanceUnits.NM)
    @staticmethod
    def smethod_7(string_0, string_1):
        num = None
        if (string_0 == None or string_0 == "") or (string_1 == None or string_1 == ""):
            return Distance.NaN
        try:
            num = float(string_0)
        except:
            return Distance.NaN
        if string_1 == "M":
            return Distance(num, DistanceUnits.M)
        elif string_1 == "FT":
            return Distance(num, DistanceUnits.FT)
        elif string_1 == "KM":
            return Distance(num, DistanceUnits.KM)
        elif string_1 == "NM":
            return Distance(num, DistanceUnits.NM)
        else:
            return Distance.NaN
        
# 
#     public static Distance smethod_3(string string_0, DistanceUnits distanceUnits_0)
#     {
#         return Distance.smethod_4(string_0, distanceUnits_0, CultureInfo.CurrentCulture)
#     }
# 
#     public static Distance smethod_4(string string_0, DistanceUnits distanceUnits_0, IFormatProvider iformatProvider_0)
#     {
#         Distance naN = Distance.NaN
#         if (!Distance.smethod_6(string_0, distanceUnits_0, iformatProvider_0, out naN))
#         {
#             throw new Exception(string.Format(Validations.NOT_VALID_DISTANCE_VALUE, string_0))
#         }
#         return naN
#     }
# 
#     public static bool smethod_5(string string_0, DistanceUnits distanceUnits_0, out Distance distance_0)
#     {
#         return Distance.smethod_6(string_0, distanceUnits_0, CultureInfo.CurrentCulture, out distance_0)
#     }
# 
#     public static bool smethod_6(string string_0, DistanceUnits distanceUnits_0, IFormatProvider iformatProvider_0, out Distance distance_0)
#     {
#         double num
#         if (iformatProvider_0 == null)
#         {
#             iformatProvider_0 = CultureInfo.CurrentCulture
#         }
#         string_0 = string_0.ToUpper()
#         if (string_0.IndexOf(Enums.DistanceUnits_KM, StringComparison.CurrentCultureIgnoreCase) > -1)
#         {
#             distanceUnits_0 = DistanceUnits.KM
#             string_0 = string_0.smethod_11(Enums.DistanceUnits_KM, "", StringComparison.CurrentCultureIgnoreCase)
#         }
#         elif (string_0.IndexOf(Enums.DistanceUnits_NM, StringComparison.CurrentCultureIgnoreCase) > -1)
#         {
#             distanceUnits_0 = DistanceUnits.NM
#             string_0 = string_0.smethod_11(Enums.DistanceUnits_NM, "", StringComparison.CurrentCultureIgnoreCase)
#         }
#         elif (string_0.IndexOf(Enums.DistanceUnits_FT, StringComparison.CurrentCultureIgnoreCase) > -1)
#         {
#             distanceUnits_0 = DistanceUnits.FT
#             string_0 = string_0.smethod_11(Enums.DistanceUnits_FT, "", StringComparison.CurrentCultureIgnoreCase)
#         }
#         elif (string_0.IndexOf(Enums.DistanceUnits_M, StringComparison.CurrentCultureIgnoreCase) > -1)
#         {
#             distanceUnits_0 = DistanceUnits.M
#             string_0 = string_0.smethod_11(Enums.DistanceUnits_M, "", StringComparison.CurrentCultureIgnoreCase)
#         }
#         if (!double.TryParse(string_0, NumberStyles.Number, iformatProvider_0, out num))
#         {
#             distance_0 = Distance.NaN
#             return false
#         }
#         distance_0 = new Distance(num, distanceUnits_0)
#         return true
#     }
# 
#     public static Distance smethod_7(string string_0, string string_1, IFormatProvider iformatProvider_0)
#     {
#         double num
#         if (string.IsNullOrEmpty(string_0) || string.IsNullOrEmpty(string_1))
#         {
#             return Distance.NaN
#         }
#         if (!double.TryParse(string_0, NumberStyles.Number, iformatProvider_0, out num))
#         {
#             return Distance.NaN
#         }
#         return new Distance(num, (DistanceUnits)Enum.Parse(typeof(DistanceUnits), string_1, true))
#     }
# 
#     public override string ToString()
#     {
#         return self.ToString("G", CultureInfo.CurrentCulture)
#     }
#

    def OriginalUnits_ToString(self):
        if self.originalUnits == DistanceUnits.M:
            return "m"
        elif self.originalUnits == DistanceUnits.FT:
            return "ft"
        elif self.originalUnits == DistanceUnits.KM:
            return "km"
        else:
            return "nm"
    def method_0(self, string_0):
        return self.ToString(string_0)
    def ToString(self, format0 = None):
        distanceUnit = self.originalUnits
        flag = False
        if format0.__class__ == QString:
            format0 = String.QString2Str(format0)
        if (self.IsNaN()):
            return ""
        if (String.IsNullOrEmpty(format0)):
            format0 = "0.##"#Formats.DistanceFormat
        # if (provider == null)
        # {
        #     provider = CultureInfo.CurrentCulture
        # }
        format0 = format0.upper()
        if (format0 == "G"):
            format0 = "0.##"#Formats.DistanceFormat
        elif (format0.find(":U")):
            format0 = format0.replace(":U", "")
            flag = True
        elif (format0.find(":M")):
            distanceUnit = DistanceUnits.M
            format = format0.replace(":M", "")
            flag = True
        elif (format0.find(":FT")):
            distanceUnit = DistanceUnits.FT
            format = format0.replace(":FT", "")
            flag = True
        elif (format0.find(":KM")):
            distanceUnit = DistanceUnits.KM
            format = format0.replace(":KM", "")
            flag = True
        elif (format0.find(":NM")):
            distanceUnit = DistanceUnits.NM
            format = format0.replace(":NM", "")
            flag = True
        if (String.IsNullOrEmpty(format0)):
            format0 = "0.##"#Formats.DistanceFormat
        if distanceUnit == DistanceUnits.FT:
            if (not flag):
                return str(self.Feet)
            feet = self.Feet
            return "{0} {1}".format(str(feet), "ft")
        elif distanceUnit == DistanceUnits.KM:
            if (not flag):
                return str(self.Kilometres)
            kilometres = self.Kilometres
            return "{0} {1}".format(str(kilometres), "km")
        elif distanceUnit == DistanceUnits.NM:
            if (not flag):
                return str(self.NauticalMiles)
            nauticalMiles = self.NauticalMiles
            return "{0} {1}".format(str(nauticalMiles), "nm")
        else:
            if (not flag):
                pass
            else:
                metres = self.Metres
                return "{0} {1}".format(str(metres), "m")
        return str(self.Metres)


class XmlFile(QDomDocument):
    def __init__(self, string_0, string_1, bool_0):
        QDomDocument.__init__(self)

        if string_1 == None:
            if (String.IsNullOrEmpty(string_0)):
                raise "name error"
                # throw new ArgumentException("name")

            path = ""
            if define.obstaclePath != None:
                path = define.obstaclePath
            elif define.xmlPath != None:
                path = define.xmlPath
            else:
                path = define.appPath
            self.fileName = path + "/" + string_0 + ".xml"
            # this.fileName = Path.Combine(ApplicationInfo.FolderApplicationSettings, string.Concat(string_0, ".xml"))
            self.rootName = string_0
            self.rootElement = self.createElement(self.rootName)
            self.appendChild(self.rootElement)
            if (not bool_0):
                self.method_6()
            else:
                self.method_5()
        elif bool_0 == None:
            if (String.IsNullOrEmpty(string_0)):
                raise "filename error"
                # throw new ArgumentException("fileName")
            if (String.IsNullOrEmpty(string_1)):
                raise "rootName error"
                # throw new ArgumentException("rootName")
            self.fileName = string_0
            self.rootName = string_1
            self.rootElement = self.createElement(self.rootName)
            self.appendChild(self.rootElement)
            if (not QFile.Exists(string_0)):
                self.method_5()
                return
            self.method_6()
        else:
            if (String.IsNullOrEmpty(string_0)):
                raise "filename error"
                # throw new ArgumentException("fileName")
            if (String.IsNullOrEmpty(string_1)):
                raise "rootName error"
                # throw new ArgumentException("rootName")
            self.fileName = string_0
            self.rootName = string_1
            self.rootElement = self.createElement(self.rootName)
            self.appendChild(self.rootElement)
            if (bool_0):
                self.method_5()
                return
            self.method_6()

    def method_0(self):
        qFile = QFile(self.fileName)
        if qFile.open(QFile.WriteOnly):
            textStream = QTextStream(qFile)
            self.save(textStream, 4)
            qFile.close()
        else:
            raise UserWarning, "can not open file:" + self.fileName


    def method_2(self, xmlElement_0, string_0):
        if not isinstance(string_0, QString):
            string_0 = String.Str2QString(string_0)
        # str0 = string_0.trimmed.Trim(new char[] { '/' })
        # char[] chrArray = new char[] { '/' }
        if string_0.right(1) == "/":
            string_0 = string_0.left(string_0.size() - 1)
        strs = string_0.split("/")
        if (len(strs) == 0):
            return xmlElement_0
        item = strs[0]
        if (String.IsNullOrEmpty(item)):
            return xmlElement_0
        elemList = xmlElement_0.elementsByTagName(item)
        childElem = None
        if elemList.count() == 0:
            childElem = self.createElement(item)
            xmlElement_0.appendChild(childElem)
        # strs = QStringList()
        strs.removeAt(0)
        # XmlElement xmlElement = xmlElement_0.SelectSingleNode(item) as XmlElement ?? xmlElement_0.AppendChild(base.CreateElement(item)) as XmlElement
        # strs.RemoveAt(0)
        str1 = String.Join("/", strs)
        if childElem == None:
            return self.method_2(xmlElement_0, str1)
        else:
            return self.method_2(childElem, str1)

    def method_5(self):
        pass
    def method_6(self):
        # doc = QDomDocument()
        qFile = QFile(self.fileName)
        if qFile.open(QFile.ReadOnly):
            self.setContent(qFile)
            qFile.close()
        else:
            raise UserWarning, "can not open file:" + self.fileName
    def method_7(self, xmlElement_0, string_0):
        string_1 = None
        if (xmlElement_0 == None):
            return False, None
        return self.method_8(xmlElement_0.namedItem(string_0))

    def method_8(self, xmlNode_0):
        string_0 = None
        if (xmlNode_0 == None):
            return False, None
        string_0 = xmlNode_0.toElement().text()
        return True, string_0

    def method_9(self, xmlElement_0, string_0, string_1):
        self.method_10(self.method_2(xmlElement_0, string_0), string_1)

    def method_10(self, xmlNode_0, string_0):
        xmlNode_0.appendChild(self.createTextNode(string_0))

    def method_15(self, xmlElement_0, string_0):
        int_0 = 0
        if (xmlElement_0 == None):
            return False, None
        return self.method_16(xmlElement_0.namedItem(string_0))

    def method_16(self, xmlNode_0):
        flag = False
        int_0 = 0
        if (xmlNode_0 == None):
            return False, None
        try:
            int_0 = int(xmlNode_0.toElement().text())
            flag = True
        except:
            flag = False
        return flag, int_0

    def method_17(self, xmlElement_0, string_0, int_0):
        self.method_18(self.method_2(xmlElement_0, string_0), int_0)

    def method_18(self, xmlNode_0, int_0):
        # xmlNode_0.InnerText = int_0.ToString(CultureInfo.InvariantCulture)
        xmlNode_0.appendChild(self.createTextNode(str(int_0)))
        
    def method_35(self, xmlElement_0, string_0):
        altitude_0 = None
        if (xmlElement_0 == None):
            return False, None
        return self.method_36(xmlElement_0.namedItem(string_0))

    def method_36(self, xmlNode_0):
        flag = False
        altitude_0 = None
        # try
        # {
        if (xmlNode_0 != None):
            xmlNodes = xmlNode_0.namedItem("Value")
            if (xmlNodes != None):
                xmlNodes1 = xmlNode_0.namedItem("Units")
                if (xmlNodes1 != None):
                    altitudeUnit = 0
                    unitStr = xmlNodes1.toElement().text()
                    if unitStr == "m":
                        altitudeUnit = AltitudeUnits.M
                    elif unitStr == "ft":
                        altitudeUnit = AltitudeUnits.FT
                    elif unitStr == "fl":
                        altitudeUnit = AltitudeUnits.FL
                    elif unitStr == "sm":
                        altitudeUnit = AltitudeUnits.SM
                    else:
                        altitudeUnit = AltitudeUnits.M
                    num = 0.0
                    if (not String.IsNullOrEmpty(xmlNodes.toElement().text())):
                        valStr = xmlNodes.toElement().text().split(" ")[0]
                        num = float(valStr)
                        # num = double.Parse(xmlNodes.InnerText, CultureInfo.InvariantCulture)
                    altitude_0 = Altitude(num, altitudeUnit)
                    flag = True
                else:
                    flag = False
            else:
                flag = False
        else:
            flag = False
        # catch
        # {
        #     flag = false
        # }
        return flag, altitude_0

    def method_37(self, xmlElement_0, string_0, altitude_0):
        self.method_38(self.method_2(xmlElement_0, string_0), altitude_0)

    def method_38(self, xmlNode_0, altitude_0):
        str0 = self.createElement("Value")
        str0.appendChild(self.createTextNode(altitude_0.ToString("R")))
        # str0.InnerText = altitude_0.ToString("R", CultureInfo.InvariantCulture)
        xmlNodes = self.createElement("Units")
        xmlNodes.appendChild(self.createTextNode(AltitudeUnits.ToString(altitude_0.originalUnit)))
        # xmlNodes.InnerText = altitude_0.OriginalUnits.ToString()
        xmlNode_0.appendChild(str0)
        xmlNode_0.appendChild(xmlNodes)
        
    def method_39(self, xmlElement_0, string_0):
        distance_0 = Distance.NaN
        if (xmlElement_0 == None):
            return False, None
        return self.method_40(xmlElement_0.namedItem(string_0))

    def method_40(self, xmlNode_0):
        flag = False
        distance_0 = None
        # try:
        if (xmlNode_0 != None):
            xmlNodes = xmlNode_0.namedItem("Value")
            if (xmlNodes != None):
                xmlNodes1 = xmlNode_0.namedItem("Units")
                if (xmlNodes1 != None):
                    distanceUnit = 0
                    unitStr = xmlNodes1.toElement().text()
                    if unitStr == "m":
                        distanceUnit = DistanceUnits.M
                    elif unitStr == "ft":
                        distanceUnit = DistanceUnits.FT
                    elif unitStr == "nm":
                        distanceUnit = DistanceUnits.NM
                    else:
                        distanceUnit = DistanceUnits.M
                    num = 0.0
                    if (not String.IsNullOrEmpty(xmlNodes.toElement().text())):
                        valStr = xmlNodes.toElement().text().split(" ")[0]
                        num = float(valStr)
                    distance_0 = Distance(num, distanceUnit)
                    flag = True
                else:
                    flag = False
            else:
                flag = False
        else:
            flag = False
        # catch
        # {
        #     flag = false
        # }
        return flag, distance_0

    def method_41(self, xmlElement_0, string_0, distance_0):
        self.method_42(self.method_2(xmlElement_0, string_0), distance_0)

    def method_42(self, xmlNode_0, distance_0):
        str0 = self.createElement("Value")
        str0.appendChild(self.createTextNode(distance_0.ToString("R")))
        # str.InnerText = distance_0.ToString("R", CultureInfo.InvariantCulture)
        xmlNodes = self.createElement("Units")
        xmlNodes.appendChild(self.createTextNode(DistanceUnits.ToString(distance_0.originalUnits)))
        # xmlNodes.InnerText = distance_0.OriginalUnits.ToString()
        xmlNode_0.appendChild(str0)
        xmlNode_0.appendChild(xmlNodes)
        
    def method_47(self, xmlElement_0, string_0):
        angleGradientSlope_0 = None
        if (xmlElement_0 == None):
            return False, None
        return self.method_48(xmlElement_0.namedItem(string_0))

    def method_48(self, xmlNode_0):
        flag = False
        angleGradientSlope_0 = None
        # try
        # {
        if (xmlNode_0 != None):
            xmlNodes = xmlNode_0.namedItem("Value")
            if (xmlNodes != None):
                xmlNodes1 = xmlNode_0.namedItem("Units")
                if (xmlNodes1 != None):
                    angleGradientSlopeUnit = 0
                    unitStr = xmlNodes1.toElement().text()
                    if unitStr == define._degreeStr:
                        angleGradientSlopeUnit = AngleGradientSlopeUnits.Degrees
                    elif unitStr == "%":
                        angleGradientSlopeUnit = AngleGradientSlopeUnits.Percent
                    elif unitStr == "1:":
                        angleGradientSlopeUnit = AngleGradientSlopeUnits.Slope
                    else:
                        angleGradientSlopeUnit = AngleGradientSlopeUnits.Degrees
                    # AngleGradientSlopeUnits angleGradientSlopeUnit = (AngleGradientSlopeUnits)Enum.Parse(typeof(AngleGradientSlopeUnits), xmlNodes1.InnerText)
                    num = None
                    if (not String.IsNullOrEmpty(xmlNodes.toElement().text())):
                        num = float(xmlNodes.toElement().text())
                    angleGradientSlope_0 = AngleGradientSlope(num, angleGradientSlopeUnit)
                    flag = True
                else:
                    flag = False
            else:
                flag = False
        else:
            flag = False
        # catch
        # {
        #     flag = false
        # }
        return flag, angleGradientSlope_0

    def method_49(self, xmlElement_0, string_0, angleGradientSlope_0):
        self.method_50(self.method_2(xmlElement_0, string_0), angleGradientSlope_0)

    def method_50(self, xmlNode_0, angleGradientSlope_0):
        str0 = self.createElement("Value")
        if (angleGradientSlope_0.OriginalUnits != AngleGradientSlopeUnits.Slope):
            str0.appendChild(self.createTextNode(angleGradientSlope_0.ToString("R")))
            # str.InnerText = angleGradientSlope_0.ToString("R", CultureInfo.InvariantCulture)
        else:
            slope = angleGradientSlope_0.Slope
            str0.appendChild(self.createTextNode(str(slope)))
            # str.InnerText = slope.ToString("R", CultureInfo.InvariantCulture)
        xmlNodes = self.createElement("Units")
        xmlNodes.appendChild(self.createTextNode(AngleGradientSlopeUnits.ToString(angleGradientSlope_0.originalUnits)))
        # xmlNodes.InnerText = angleGradientSlope_0.OriginalUnits.ToString()
        xmlNode_0.appendChild(str0)
        xmlNode_0.appendChild(xmlNodes)