'''
Created on Mar 19, 2015

@author: Administrator
'''

import math

from qgis.core import QgsRectangle
from PyQt4.QtGui import QStandardItem

from FlightPlanner.Ils.OasConstants import OasConstants
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.types import ObstacleTableColumnType, OasSurface, CriticalObstacleType, OasMaEvaluationMethod, Point3D
from FlightPlanner.helpers import Unit, MathHelper, Altitude
from FlightPlanner.QgisHelper import QgisHelper

class OasCriticalObstacle:

    def get_Position(self):
        if not self.Assigned:
            return None
        return self.Obstacle.Position
    Position = property(get_Position, None, None, None)
    def __init__(self):
        self.eqAltitude = None
        self.Assigned = False

    def method_0(self, obstacle_0, double_0, oasSurface_0):
        if (self.Assigned):
            double0 = double_0;
            if double0 == None:
                double0 = obstacle_0.Position.z() + obstacle_0.trees;
            z = self.eqAltitude;
            if z == None:
                position = self.Obstacle.Position;
                z = position.z() + self.Obstacle.trees
            if (z >= double0):
                return;

        self.Obstacle = obstacle_0;
        self.eqAltitude = double_0;
        self.Surface = oasSurface_0;
        self.Assigned = True;

    def method_1(self):
        self.Assigned = False

    def method_2(self, point3d_0):
        if (not self.Assigned):
            return Altitude(point3d_0.z())
        if self.eqAltitude != None:
            return Altitude(self.eqAltitude)
        position = self.Obstacle.position
        return Altitude(position.z() + self.Obstacle.trees)

class OasObstacles(ObstacleTable):
    
    obstaclesChecked = 0
    constants = OasConstants()
    resultOCH = Altitude(0)
    resultOCA = Altitude(0)
    resultSocText = ""
    resultSocPosition = Point3D()
    resultCriticalObst = OasCriticalObstacle()
    #

    def __init__(self, surfacesList = None, manualPolygon = None):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
        self.manualPolygon = manualPolygon

    def initModel(self, surfacesList, oasCategory_0, point3d_0, double_0, double_1, double_2, oasMaEvaluationMethod_0, hlAltitude):
        self.cat = oasCategory_0;
        self.ptTHR = point3d_0;
        self.ptTHR2 = MathHelper.distanceBearingPoint(point3d_0, double_0, 100);
        self.ptTHRm90 = MathHelper.distanceBearingPoint(point3d_0, double_0 - 1.5707963267949, 100);
        self.tr90p = double_0 + 1.5707963267949;
        self.tanmacg = double_1 / 100.0;
        self.tangpa = math.tan(Unit.ConvertDegToRad(double_2));
        self.method = oasMaEvaluationMethod_0;
        self.xe = OasObstacles.constants.ZC / OasObstacles.constants.ZA
        self.surfacesList = surfacesList
        self.hlAltitude = hlAltitude
        
    def addObstacleToModel(self, obstacle, checkResult):
        ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
        row = self.source.rowCount() - 1
        item = QStandardItem(str(checkResult[0]))
        item.setData(checkResult[0])
        self.source.setItem(row, self.IndexIlsX, item)

        item = QStandardItem(str(checkResult[1]))
        item.setData(checkResult[1])
        self.source.setItem(row, self.IndexIlsY, item)

        item = QStandardItem(str(checkResult[2]))
        item.setData(checkResult[2])
        self.source.setItem(row, self.IndexEqAltM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[2])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[2]))
        self.source.setItem(row, self.IndexEqAltFt, item)

        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexSurfAltM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[3]))
        self.source.setItem(row, self.IndexSurfAltFt, item)

        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexDifferenceM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[4])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[4]))
        self.source.setItem(row, self.IndexDifferenceFt, item)

        if checkResult[4] < 0:
            item = QStandardItem("")
            # item.setData(checkResult[5])
            self.source.setItem(row, self.IndexOcaM, item)
        else:
            item = QStandardItem(str(checkResult[5]))
            item.setData(checkResult[5])
            self.source.setItem(row, self.IndexOcaM, item)

        if checkResult[4] < 0:
            item = QStandardItem("")
            # item.setData(checkResult[5])
            self.source.setItem(row, self.IndexOcaM, item)
        else:
            item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[5])))
            item.setData(Unit.ConvertMeterToFeet(checkResult[5]))
            self.source.setItem(row, self.IndexOcaFt, item)

        item = QStandardItem(str(checkResult[6]))
        item.setData(checkResult[5])
        self.source.setItem(row, self.IndexCritical, item)

        item = QStandardItem(str(checkResult[7]))
        item.setData(checkResult[6])
        self.source.setItem(row, self.IndexSurface, item)

    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexIlsX = fixedColumnCount
        self.IndexIlsY = fixedColumnCount + 1
        self.IndexEqAltM = fixedColumnCount + 2
        self.IndexEqAltFt = fixedColumnCount + 3
        self.IndexSurfAltM = fixedColumnCount + 4
        self.IndexSurfAltFt = fixedColumnCount + 5
        self.IndexDifferenceM = fixedColumnCount + 6
        self.IndexDifferenceFt = fixedColumnCount + 7
        self.IndexOcaM = fixedColumnCount + 8
        self.IndexOcaFt = fixedColumnCount + 9
        self.IndexCritical = fixedColumnCount + 10
        self.IndexSurface = fixedColumnCount + 11
        
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.IlsX,
                ObstacleTableColumnType.IlsY,
                ObstacleTableColumnType.EqAltM,
                ObstacleTableColumnType.EqAltFt,
                ObstacleTableColumnType.SurfAltM,
                ObstacleTableColumnType.SurfAltFt,
                ObstacleTableColumnType.DifferenceM,
                ObstacleTableColumnType.DifferenceFt,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt,
                ObstacleTableColumnType.Critical,
                ObstacleTableColumnType.Surface
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)

    def checkObstacle(self, obstacle):
        if self.manualPolygon != None:
            if not self.manualPolygon.contains(obstacle.Position):
                return

        point3d = MathHelper.getIntersectionPoint(obstacle.Position, MathHelper.distanceBearingPoint(obstacle.Position, self.tr90p, 100), self.ptTHR, self.ptTHR2)
        tolerance = MathHelper.calcDistance(self.ptTHR, point3d)
        if (not MathHelper.smethod_115(point3d, self.ptTHR, self.ptTHRm90)):
            tolerance = tolerance * -1;
        num = tolerance + obstacle.tolerance;
        tolerance = tolerance - obstacle.tolerance;
        num1 = MathHelper.calcDistance(point3d, obstacle.Position) - obstacle.tolerance
        # if MathHelper.smethod_99(num1, 237.633410911, 0.0001):
        #     pass
        if (num1 < 0):
            num1 = 0;
        # if MathHelper.smethod_115(obstacle.position, self.ptTHR, point3d):
        #     num1 *= 1 if tolerance > 0 else -1
        # else:
        #     num1 *= -1 if tolerance > 0 else 1
        z = obstacle.Position.z() + obstacle.trees;

        for surface in self.surfacesList:
            oasSurfacesList = [OasSurface.OFZ, OasSurface.W, OasSurface.X1, OasSurface.X2, OasSurface.Y1, OasSurface.Y2, OasSurface.Z]
            if len(surface.WS) > 3:
                oasSurfacesList.append(OasSurface.WS)
                
            for oasSurface in oasSurfacesList:
                num2 = 0;
                num3 = tolerance;
                num4 = num1;
                
                calcList = [num3, num4, num2]
                
                if not surface.method_0(oasSurface, obstacle, calcList):
                    continue
                num3 = calcList[0]
                num4 = calcList[1]
                num2 = calcList[2]
                if (num2 < 0):
                    num2 = 0;
                z1 = self.ptTHR.z() + num2
                zC = None
                if (z > z1):
                    if (self.method != OasMaEvaluationMethod.Standard):
                        zC = (self.xe + (num + (z - self.ptTHR.z()) / self.tanmacg)) * self.tanmacg * self.tangpa / (self.tanmacg + self.tangpa);
                        zC = None if zC >= z - self.ptTHR.z() else zC + self.ptTHR.z()
                    elif (num < -self.xe):
                        zC = self.ptTHR.z() + ((z - self.ptTHR.z()) * (1 / self.tanmacg) + (self.xe + num)) / (1 / self.tanmacg + 1 / self.tangpa);
                    OasObstacles.resultCriticalObst.method_0(obstacle, zC, oasSurface)
                
                if zC == None:
                    oca = obstacle.Position.z() + obstacle.trees + self.hlAltitude.Metres
                    och = oca - self.ptTHR.z()
                else:
                    oca = zC + self.hlAltitude.Metres
                    och = oca - self.ptTHR.z()
                # if oca < 0:
                #     oca = None
                self.addObstacleToModel(obstacle, [num3, num4, zC, z1, z - z1, oca, CriticalObstacleType.No if z - z1 <= 0 else CriticalObstacleType.Yes, oasSurface])

        return True

    def getExtentForLocate(self, sourceRow):
        surfaceType = self.source.item(sourceRow, self.IndexSurface).text()
        surfaceLayers = QgisHelper.getSurfaceLayers(self.surfaceType)
        rect = QgsRectangle()
        rect.setMinimal()
        for sfLayer in surfaceLayers:
            lId = sfLayer.name()
            if lId.contains("2D"):
                features = sfLayer.getFeatures()
                for feature in features:
                    surfaceString = feature.attribute("surface").toString()
                    if surfaceString == surfaceType:
                        geom = feature.geometry()
                        rect.combineExtentWith(geom.boundingBox())
                break
        return rect
