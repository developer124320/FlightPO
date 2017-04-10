'''
Created on Feb 28, 2015

@author: Administrator
'''
from PyQt4.QtGui import QStandardItem
from PyQt4.QtCore import Qt,QReadWriteLock

from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.types import ObstacleTableColumnType, RnavSegmentType, AltitudeUnits, CriticalObstacleType
from FlightPlanner.helpers import Unit, Altitude
from FlightPlanner.Captions import Captions
from FlightPlanner.messages import Messages
import time,threading

class GnssSegmentObstacles(ObstacleTable):
    '''
    classdocs
    '''
    def __init__(self, surfacesList):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
        self.ocaMaxObstacle = None
        self.ocaMax = 0.0
        self.lock = threading.Lock()
        
    def addObstacleToModel(self, obstacle, checkResult):
        ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
        row = self.source.rowCount() - 1
        item = QStandardItem(str(checkResult[0]))
        item.setData(checkResult[0])
        self.source.setItem(row, self.IndexObstArea, item)

        item = QStandardItem(str(checkResult[1]))
        item.setData(checkResult[1])
        self.source.setItem(row, self.IndexDistInSecM, item)

        item = QStandardItem(str(checkResult[2]))
        item.setData(checkResult[2])
        self.source.setItem(row, self.IndexDoM, item)

        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexMocAppliedM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[3]))
        self.source.setItem(row, self.IndexMocAppliedFt, item)

        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexOcaM, item)

        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[4])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[4]))
        self.source.setItem(row, self.IndexOcaFt, item)

        item = QStandardItem(str(checkResult[5]))
        item.setData(checkResult[5])
        self.source.setItem(row, self.IndexCritical, item)

        item = QStandardItem(str(checkResult[6]))
        item.setData(checkResult[6])
        self.source.setItem(row, self.IndexSurface, item)

    def setHiddenColumns(self, tableView):
        ObstacleTable.setHiddenColumns(self, tableView)
        tableView.hideColumn(self.IndexSurface)
        tableView.hideColumn(self.IndexCritical)
        
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexObstArea = fixedColumnCount
        self.IndexDistInSecM = fixedColumnCount + 1
        self.IndexDoM = fixedColumnCount + 2
        self.IndexMocAppliedM = fixedColumnCount + 3
        self.IndexMocAppliedFt = fixedColumnCount + 4
        self.IndexMocMultiplier = fixedColumnCount + 5
        self.IndexOcaM = fixedColumnCount + 6
        self.IndexOcaFt = fixedColumnCount + 7
        self.IndexCritical = fixedColumnCount + 8
        self.IndexSurface = fixedColumnCount + 9
        
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.ObstArea,
                ObstacleTableColumnType.DistInSecM,
                ObstacleTableColumnType.DoM,
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt,
                ObstacleTableColumnType.Critical,
                ObstacleTableColumnType.Surface
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)

    def checkObstacle(self, obstacle):
        
        for surface in self.surfacesList:
            calcList = surface.vmethod_0(obstacle)
            if calcList != None:
#                 self.lock.acquire()
#                 try:
                self.addObstacleToModel(obstacle, calcList)
                           
                type0 = surface.Type
                if not type0.count("Initial") > 0:
                    if self.ocaMax < calcList[4]:
                        self.ocaMax = calcList[4]
                        obstacle.area = surface.Type
    #                     obstacle.surfaceName = 
                        self.ocaMaxObstacle = obstacle
#                 finally:
#                     self.lock.release()


    def CompareObstacleRows(self, newRow, row, ignore):
        return ObstacleTable.CompareObstacleRows(self, newRow, row, ignore)

    def method_13(self, rnavSegmentType, altitudeUnits_0):
        self.setFilterFixedString(rnavSegmentType)
        self.sort(self.IndexOcaM, Qt.DescendingOrder )
        
        if (self.rowCount() == 0):
            return Captions.GROUND_PLANE;
        num1 = 5;
        num2 = 10;
        if (rnavSegmentType == RnavSegmentType.Initial1 or rnavSegmentType == RnavSegmentType.Initial2 or rnavSegmentType == RnavSegmentType.Initial3 or rnavSegmentType == RnavSegmentType.Intermediate):
            num1 = 50;
            num2 = 100;
        if (rnavSegmentType != RnavSegmentType.MissedApproach):
            num = self.data(self.index(0, self.IndexOcaFt), Qt.DisplayRole).toDouble()[0] if altitudeUnits_0 != AltitudeUnits.M else self.data(self.index(0, self.IndexOcaM), Qt.DisplayRole).toDouble()[0]
        else:
            num3 = -10000;
            num4 = -10000;
            isCritical = self.data(self.index(0, self.IndexCritical), Qt.DisplayRole).toString()
            if self.rowCount() > 0:
                ocaFt = self.data(self.index(0, self.IndexOcaFt), Qt.DisplayRole)
                ocaM = self.data(self.index(0, self.IndexOcaM), Qt.DisplayRole)
                num3 = ocaFt.toDouble()[0] if altitudeUnits_0 != AltitudeUnits.M else ocaM.toDouble()[0] 
                
            
            if self.rowCount() > 1 :#and self.data(self.index(1, self.IndexCritical), Qt.DisplayRole).toString() == CriticalObstacleType.Yes == CriticalObstacleType.Yes:
                ocaFt = self.data(self.index(1, self.IndexOcaFt), Qt.DisplayRole)
                ocaM = self.data(self.index(1, self.IndexOcaM), Qt.DisplayRole)
                num4 = ocaFt.toDouble()[0] if altitudeUnits_0 != AltitudeUnits.M else ocaM.toDouble()[0]
                 
            num = max([num3, num4])
        if (altitudeUnits_0 == AltitudeUnits.M):
            num5 = num % num1
            if num5 > 0:
                num = num + (num1 - num5)
            altitude = Altitude(round(num));
            return str(altitude.Metres) + " m"
        if (altitudeUnits_0 != AltitudeUnits.FT):
            raise UserWarning, Messages.ERR_INVALID_ALTITUDE_UNITS
        num6 = num % num2;
        if (num6 > 0):
            num = num + (num2 - num6)
        altitude1 = Altitude(round(num), AltitudeUnits.FT)
        return str(altitude1.Feet) + " ft"
        