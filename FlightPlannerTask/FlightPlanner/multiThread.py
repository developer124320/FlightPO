
from PyQt4.QtCore import QThread, QMutex
from PyQt4.QtGui import QMessageBox, QSortFilterProxyModel, QApplication, QStandardItemModel, QProgressBar, QStandardItem, QAbstractItemView
from PyQt4.QtCore import Qt, QVariant

from qgis.core import QGis, QgsPoint, QgsRasterLayer, QgsRectangle, QgsGeometry

from FlightPlanner.types import SelectionModeType, Point3D, ObstacleTableColumnType, SurfaceTypes
from FlightPlanner.helpers import Unit
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Obstacle.Obstacle import Obstacle
# from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable

import define
import math, time
import threading

class multiThread(threading.Thread):
    def __init__(self,  i,j,hCount,wCount,block,wStartNumber,hStartNumber,xStartValue,yStartValue,xOffSet, yOffSet,obstacleLayer,obstacleTable,obstacleUnits,mocMultiplier):
        threading.Thread().__init__(self)
        self.lock = threading.Lock()
        self.stopped = False
        self.mutex = QMutex()
        self.path = None
        self.completed = False
        self.i = i
        self.j = j
        self.hCount = hCount
        self.wCount = wCount
        self.block = block
        self.wStartNumber = wStartNumber
        self.hStartNumber = hStartNumber
        self.xStartValue = xStartValue
        self.yStartValue = yStartValue
        self.xOffSet = xOffSet
        self.yOffSet = yOffSet
        self.obstacleLayer = obstacleLayer
        self.obstacleTable = obstacleTable
        self.obstacleUnits = obstacleUnits
        self.mocMultiplier = mocMultiplier
    def run(self):
        self.processMethod(self.i ,self.j ,self.hCount,self.wCount,self.block,self.wStartNumber,self.hStartNumber,self.xStartValue,self.yStartValue,self.xOffSet, self.yOffSet,self.obstacleLayer,self.obstacleTable,self.obstacleUnits,self.mocMultiplier)
#         self.stop()
#         self.emit(SIGNAL("finished(bool)"), self.completed)
#     def stop(self):
#         try:
#             self.mutex.lock()
#             self.stopped = True
#         finally:
#             self.mutex.unlock()
#     def isStopped(self):
#         try:
#             self.mutex.lock()
#             return self.stopped
#         finally:
#             self.mutex.unlock()
    def processMethod(self ,i ,j ,hCount,wCount,block,wStartNumber,hStartNumber,xStartValue,yStartValue,xOffSet, yOffSet,obstacleLayer,obstacleTable,obstacleUnits,mocMultiplier):
        featureID = 0
        while i <=  hCount - 1:
            j = 0
            while j <=  wCount - 1:
    #                         altitude = block.value(wStartNumber, hStartNumber)
                name = "DEM"
    #                     startTime = time.time()
    #                     print "startTime" + str(startTime)
                if block.isNoData(j + wStartNumber, i + hStartNumber):
                    j += 1
                    continue
                altitude = block.value(j + wStartNumber, i + hStartNumber)
                trees = define._trees
                tolerance = define._tolerance
                point = QgsPoint(xStartValue + (j + wStartNumber) * xOffSet + xOffSet / 2, yStartValue - (i + hStartNumber) * yOffSet - yOffSet / 2)
                position = Point3D()
                positionDegree = Point3D()
                if obstacleUnits == QGis.Meters:
                    position = Point3D(point.x(), point.y(), altitude)
                    if obstacleUnits != define._units:
                        positionDegree = QgisHelper.Meter2DegreePoint3D(position)
                else:
                    positionDegree = Point3D(point.x(), point.y(), altitude)
                    if obstacleUnits != define._units:
                        position = QgisHelper.Degree2MeterPoint3D(positionDegree)
                    
                featureId = featureID
                layerId = obstacleLayer.id()
                obstacle = Obstacle(name, position, layerId, featureId, None, trees, mocMultiplier, tolerance)
                obstacle.positionDegree = positionDegree 
                
    #                     middleTime = time.time()
    #                     print "middleTime" + str(middleTime)
    #                 obstacle.positionDegree = positionDegree
                
                obstacleTable.checkObstacle(obstacle)
                self.lock.acquire()
                try:
                    
                    obstacleTable.progress.setValue(obstacleTable.progress.value() + 1)
                    QApplication.processEvents()
                finally:
                    self.lock.release()
                
    #                     endTime = time.time()
    #                     print "endTime" + str(endTime)
                
                j += 1
                featureID += 1
#                 obstacle = None
#             print i
            i += 1  