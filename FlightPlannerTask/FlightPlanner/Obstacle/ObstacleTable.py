# -*- coding: UTF-8 -*-
'''
Created on Feb 26, 2015

@author: Administrator
'''
from PyQt4.QtGui import QMessageBox, QSortFilterProxyModel, QApplication, QStandardItemModel, QProgressBar, QStandardItem, QAbstractItemView
from PyQt4.QtCore import Qt, QVariant,QReadWriteLock,QThread

from qgis.core import QGis, QgsPoint, QgsRasterLayer, QgsRectangle, QgsGeometry,QgsMapLayerRegistry

from FlightPlanner.types import SelectionModeType, Point3D, ObstacleTableColumnType, SurfaceTypes
from FlightPlanner.helpers import Unit
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Obstacle.Obstacle import Obstacle
from FlightPlanner.multiThread import multiThread
from FlightPlanner.Obstacle.cellsizeWnd import cellsizeWnd

import define
import math, time,threading
class ObstacleTable(QSortFilterProxyModel):
    
    MocMultiplier = 1
    SelectionMode = SelectionModeType.Automatic
    
    def __init__(self, surfacesList, fileWriter = None):
        QSortFilterProxyModel.__init__(self)
        ObstacleTable.SelectionMode = SelectionModeType.Automatic
        self.manualPolygon = None
        self.surfacesList = surfacesList
        self.surfaceType = None
        self.source = QStandardItemModel()
        self.setSourceModel(self.source)
#         tableView.hideColumn(self.IndexObjectId)
#         tableView.hideColumn(self.IndexLayerId)
#         tableView.hideColumn(self.IndexX)
#         tableView.hideColumn(self.IndexY)
#         tableView.hideColumn(self.IndexLat)
#         tableView.hideColumn(self.IndexLon)
#         tableView.hideColumn(self.IndexSurface)
        self.hideColumnLabels = [ObstacleTableColumnType.ObjectId,
                                  ObstacleTableColumnType.LayerId,
                                  ObstacleTableColumnType.X,
                                  ObstacleTableColumnType.Y,
                                  ObstacleTableColumnType.Lat,
                                  ObstacleTableColumnType.Lon,
                                  ObstacleTableColumnType.Surface
                                  ]
 
        self.fixedColumnLabels = [ObstacleTableColumnType.ObjectId,
                                  ObstacleTableColumnType.LayerId,
                                  ObstacleTableColumnType.Name,
                                  ObstacleTableColumnType.X,
                                  ObstacleTableColumnType.Y,
                                  ObstacleTableColumnType.Lat,
                                  ObstacleTableColumnType.Lon,
                                  ObstacleTableColumnType.AltM,
                                  ObstacleTableColumnType.AltFt,
                                  ObstacleTableColumnType.TreesM,
                                  ObstacleTableColumnType.TreesFt
                                  ]

        self.IndexObjectId = 0
        self.IndexLayerId = 1
        self.IndexName = 2
        self.IndexX = 3
        self.IndexY = 4
        self.IndexLat = 5
        self.IndexLon = 6
        self.IndexAltM = 7
        self.IndexAltFt = 8
        self.IndexTreesM = 9
        self.IndexTreesFt = 10
        self.IndexOcaM = -1
        self.IndexOcaFt = -1
        self.IndexOchM = -1
        self.IndexOchFt = -1
        self.IndexObstArea = -1
        self.IndexDistInSecM = -1
        self.IndexMocAppliedM = -1
        self.IndexMocAppliedFt = -1
        self.IndexMocMultiplier = -1
        self.IndexMocReqM = -1
        self.IndexMocReqFt = -1
        self.IndexDoM = -1
        self.IndexDrM = -1
        self.IndexDzM = -1
        self.IndexDxM = -1
        self.IndexDsocM = -1
        self.IndexHeightLossM = -1
        self.IndexHeightLossFt = -1
        self.IndexAcAltM = -1
        self.IndexAcAltFt = -1
        self.IndexAltReqM = -1
        self.IndexAltReqFt = -1
        self.IndexCritical = -1
        self.IndexMACG = -1
        self.IndexPDG = -1
        self.IndexSurfAltM = -1
        self.IndexSurfAltFt = -1
        self.IndexDifferenceM = -1
        self.IndexDifferenceFt = -1
        self.IndexIlsX = -1
        self.IndexIlsY = -1
        self.IndexEqAltM = -1
        self.IndexEqAltFt = -1
        self.IndexSurfaceName = -1
        self.IndexDisregardable = -1
        self.IndexCloseIn = -1
        self.IndexTag = -1
        self.IndexSurface = -1
        self.IndexArea = -1
        self.IndexHLAppliedM = -1
        self.setHeaderLabels()
        self.setFilterKeyColumn(self.IndexSurface)
        self.setSortRole(Qt.UserRole + 1)
        self.layoutChanged.connect(self.setVerticalHeader)
        self.btnLocate = None
        self.tblObstacles = None
        
        
    
    
    def FilterDisregardableObstacles(self, state):
        if state:
            self.setFilterKeyColumn(self.IndexDisregardable)
            self.setFilterFixedString("Yes")
            self.setFilterKeyColumn(self.IndexSurface)
            
    def setSurfaceType(self, surfaceType):
        self.surfaceType = surfaceType
        
    def setFilterFixedString(self, filterString):
        QSortFilterProxyModel.setFilterFixedString(self, filterString)
        self.setVerticalHeader()
        if self.btnLocate != None and self.tblObstacles != None:
            selectedIndexes = self.tblObstacles.selectedIndexes()
            if len(selectedIndexes) == 0:
                self.btnLocate.setEnabled(False)
            else:
                self.btnLocate.setEnabled(True)


    def setLocateBtn(self, btnLocate):
        self.btnLocate = btnLocate
        self.btnLocate.setEnabled(False)
        self.btnLocate.clicked.connect(self.btnLocateClicked)
        
    def btnLocateClicked(self):
        if self.tblObstacles == None:
            return
        selectedIndexes = self.tblObstacles.selectedIndexes()
        self.locate(selectedIndexes)
        
    def tblObstaclesClicked(self, idx):
        if len(self.tblObstacles.selectedIndexes()) > 0:
            self.btnLocate.setEnabled(True)

    def setTableView(self, tblObstacles):
        self.tblObstacles = tblObstacles
        self.tblObstacles.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblObstacles.setSortingEnabled(True)
        self.tblObstacles.clicked.connect(self.tblObstaclesClicked)
        self.tblObstacles.verticalHeader().sectionClicked.connect(self.tblObstaclesClicked)
        pass
    def setHeaderLabels(self):
#         print self.setHeaderData(1, Qt.Vertical, 1, Qt.DisplayRole)
        pass
    def setVerticalHeader(self):
        for i in range(self.rowCount()):
            self.setHeaderData(i, Qt.Vertical, i+1, Qt.DisplayRole)
    
    def setHiddenColumns(self, tableView):
        tableView.hideColumn(self.IndexObjectId)
        tableView.hideColumn(self.IndexLayerId)
        tableView.hideColumn(self.IndexX)
        tableView.hideColumn(self.IndexY)
        tableView.hideColumn(self.IndexLat)
        tableView.hideColumn(self.IndexLon)
        tableView.hideColumn(self.IndexSurface)
    
    def getExtentForLocate(self, sourceRow):
        extent = None
        surfaceType = None
        if self.IndexSurface < 0:
            surfaceType =  self.surfaceType
        else:
            surfaceType = self.source.item(sourceRow, self.IndexSurface).text()
        surfaceLayers = QgisHelper.getSurfaceLayers(self.surfaceType)
        for sfLayer in surfaceLayers:
            lId = sfLayer.name()
            if lId.contains(surfaceType):
                extent = sfLayer.extent()
                break
        return extent    
    
    
    def clear(self):
        self.source.clear()
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
#         self.setHeaderLabels()
        
    def locate(self, selectedRowIndexes):
        if selectedRowIndexes == None or len(selectedRowIndexes) <= 0:
            return
        sourceRow = self.mapToSource(selectedRowIndexes[0]).row()
        objectId = int(self.source.item(sourceRow, self.IndexObjectId).text())
        layerId = self.source.item(sourceRow, self.IndexLayerId).text()
        QgisHelper.selectFeature(layerId, objectId)
        layer = QgsMapLayerRegistry.instance().mapLayer(layerId)
        crs = define._canvas.mapSettings().destinationCrs()
        if crs.mapUnits() == QGis.Meters:
            x = float(self.source.item(sourceRow, self.IndexX).text())
            y = float(self.source.item(sourceRow, self.IndexY).text())
            extent = QgsRectangle(x - 350, y - 350, x + 350, y + 350)
        else:
            x, result1 = self.source.item(sourceRow, self.IndexLon).data().toDouble()
            y, result2 = self.source.item(sourceRow, self.IndexLat).data().toDouble()
            extent = QgsRectangle(x - 0.005, y - 0.005, x + 0.005, y + 0.005)
        point = QgsPoint(x, y)
        # extent = self.getExtentForLocate(sourceRow)

        if extent is None:
            return           
 
        QgisHelper.zoomExtent(point, extent, 2)
        pass


    def loadObstacles(self, surfaceLayers):
        if self.source.rowCount() > 0:
            self.source.clear()
            self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
        demEvaluateAg = None
        existingDemFlag = False
        obstacleLayersDEM = QgisHelper.getSurfaceLayers(SurfaceTypes.DEM)
        obstacleLayers = QgisHelper.getSurfaceLayers(SurfaceTypes.Obstacles)
        if obstacleLayersDEM != None and len(obstacleLayersDEM) > 0:
            if QMessageBox.question(None, "Question", "Do you want to use DEM for evaluating Obstacle?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.loadObstaclesDEM(obstacleLayersDEM, surfaceLayers)
        if obstacleLayers != None and len(obstacleLayers) > 0:
#             if QMessageBox.question(None, "Question", "Do you want to use DEM for evaluating Obstacle?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            self.loadObstaclesVector(obstacleLayers, surfaceLayers)
        return True
    
    def loadObstaclesDEM(self, obstacleLayersDEM, surfaceLayers):
        progressMessageBar = define._messagBar.createMessage("Loading DEM Obstacles...")
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)        
        progressMessageBar.layout().addWidget(self.progress)
        define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
        maxium = 0
        offset = 0.0
        self.progress.setValue(0)
        wCount = 0
        hCount = 0
        for ly in obstacleLayersDEM:
            demDataProvider = ly.dataProvider()
            boundDem = demDataProvider.extent()
            xMin = boundDem.xMinimum()
            xMax = boundDem.xMaximum()
            yMin = boundDem.yMinimum()
            yMax = boundDem.yMaximum()
            bound = QgisHelper.getIntersectExtent(ly, QgsGeometry.fromRect(boundDem), surfaceLayers)
#             boundGeom = QgsGeometry.fromRect(bound)
            if bound == None:
                continue
            block = ly.dataProvider().block(0,ly.extent(),ly.width(),ly.height())
            xMinimum = ly.dataProvider().extent().xMinimum() 
            yMaximum = ly.dataProvider().extent().yMaximum()
            yMinimum = ly.dataProvider().extent().yMinimum() 
            xMaximum = ly.dataProvider().extent().xMaximum() 

            xOffSet = ly.extent().width() / ly.width()
            yOffSet = ly.extent().height() / ly.height()
            offset = xOffSet
            if bound.xMinimum() < xMinimum:
                wStartNumber = 0
                xStartValue = xMinimum
            else:
                wStartNumber = int((bound.xMinimum() - xMinimum) / xOffSet)
                xStartValue = bound.xMinimum()
            if yMaximum < bound.yMaximum():
                hStartNumber = 0
                yStartValue = yMaximum
            else:
                hStartNumber = int((yMaximum - bound.yMaximum()) / yOffSet)
                yStartValue = bound.yMaximum()
                
            if bound.xMaximum() > xMaximum:
                xEndValue = xMaximum
            else:
                xEndValue = bound.xMaximum()
            if yMinimum > bound.yMinimum():
                yEndValue = yMinimum
            else:
                yEndValue = bound.yMinimum()
            wCount = int(math.fabs(xEndValue - xStartValue) / xOffSet)
            hCount = int(math.fabs(yEndValue - yStartValue) / yOffSet)
            
            pixelCount = hCount
            maxium +=  pixelCount



        cellSizeWnd = cellsizeWnd(offset,wCount * hCount,maxium * 0.04)
        cellSizeWnd.setWindowTitle("Input Cell Size")
        result = cellSizeWnd.exec_()
        cellRate = 1
        if result == 1:
            offset = cellSizeWnd.cellsize
            maxium = cellSizeWnd.cellCount + 2
            cellRate = cellSizeWnd.cellRate
#             print cellSizeWnd.textedit1.text()
        
        if maxium == 0:
            return False             
        self.progress.setMaximum(maxium)

        trees = define._treesDEM
        tolerance = define._toleranceDEM
        
        for obstacleLayer in obstacleLayersDEM:
            obstacleUnits = obstacleLayer.crs().mapUnits()
            demDataProvider = obstacleLayer.dataProvider()
            boundDem = demDataProvider.extent()
            bound = QgisHelper.getIntersectExtent(obstacleLayer, QgsGeometry.fromRect(boundDem), surfaceLayers)
            if bound == None:
                continue
            boundGeom = QgsGeometry.fromRect(bound)
            if not boundGeom.intersects(QgsGeometry.fromRect(boundDem)):
                continue
            block = obstacleLayer.dataProvider().block(1,obstacleLayer.extent(),obstacleLayer.width(),obstacleLayer.height())
            xMinimum = obstacleLayer.extent().xMinimum() 
            yMaximum = obstacleLayer.extent().yMaximum()
            yMinimum = obstacleLayer.extent().yMinimum() 
            xMaximum = obstacleLayer.extent().xMaximum() 

            xOffSet = obstacleLayer.extent().width() / obstacleLayer.width()
            yOffSet = obstacleLayer.extent().height() / obstacleLayer.height()
            
            
            if bound.xMinimum() < xMinimum:
                hStartNumber = 0
                xStartValue = xMinimum
            else:
                hStartNumber = int((bound.xMinimum() - xMinimum) / xOffSet)
                xStartValue = bound.xMinimum()
            if yMaximum < bound.yMaximum():
                wStartNumber = 0
                yStartValue = yMaximum
            else:
                wStartNumber = int((yMaximum - bound.yMaximum()) / yOffSet)
                yStartValue = bound.yMaximum()
                
            if bound.xMaximum() > xMaximum:
                xEndValue = xMaximum
            else:
                xEndValue = bound.xMaximum()
            if yMinimum > bound.yMinimum():
                yEndValue = yMinimum
            else:
                yEndValue = bound.yMinimum()
            wCount = int(math.fabs(xEndValue - xStartValue) / offset)
            hCount = int(math.fabs(yEndValue - yStartValue) / offset)
            
            xPixelWidth = 0.0
            yPixelWidth = 0.0
            featureID = 0
            # i = 0
            # k = 0
            # altitudeList = []
            # self.progress.setValue(0)
            # while i  <=  hCount - 1:
            #     j = 0
            #     while j <= wCount - 1:
            #         if block.isNoData(j * int(cellRate) + wStartNumber, i* int(cellRate) + hStartNumber):
            #             self.progress.setValue(k)
            #             QApplication.processEvents()
            #             j += 1
            #             k += 1
            #             altitudeList.append(None)
            #             continue
            #         altitude = block.value(j * int(cellRate) + wStartNumber, i * int(cellRate) + hStartNumber)
            #         altitudeList.append(altitude)
            #         self.progress.setValue(k)
            #         QApplication.processEvents()
            #         j += 1
            #         k += 1
            #     i += 1


            i = 0
            k = 0
            name = "DEM"
            semiXoffset = xOffSet / 2
            semiYoffset = yOffSet / 2
            while i <= hCount - 1:
                j = 0
                while j <= wCount - 1:
                    if block.isNoData(j * cellRate + wStartNumber, i * cellRate + hStartNumber):
                        self.progress.setValue(k)
                        QApplication.processEvents()
                        j += 1
                        k += 1
                        continue
                    altitude = block.value(j * cellRate + wStartNumber, i * cellRate + hStartNumber)
                    # # if block.isNoData(j * int(cellRate) + wStartNumber, i* int(cellRate) + hStartNumber):
                    # #     j += 1
                    # #     self.progress.setValue(self.progress.value() + 1)
                    # #     QApplication.processEvents()
                    # #     continue
                    # # altitude = block.value(j* int(cellRate) + wStartNumber, i* int(cellRate)+ hStartNumber)
                    # altitude = altitudeList[k]
                    # if altitude == None:
                    #     self.progress.setValue(k)
                    #     QApplication.processEvents()
                    #     j += 1
                    #     k += 1
                    #     continue

                    point = QgsPoint(xStartValue + (i * cellRate) * xOffSet + semiXoffset, yStartValue - (j * cellRate - 1) * yOffSet - semiYoffset)
                    position = Point3D()
                    positionDegree = Point3D()

                    if define._canvas.mapUnits() == QGis.Meters:
                        if define._canvas.mapSettings().destinationCrs() != obstacleLayer.crs():
                            position = QgisHelper.CrsTransformPoint(point.x(), point.y(),obstacleLayer.crs(), define._canvas.mapSettings().destinationCrs(), altitude)
                        else:
                            position = Point3D(point.x(), point.y(), altitude)
                    else:
                        if define._canvas.mapSettings().destinationCrs() != obstacleLayer.crs():
                            positionDegree = QgisHelper.CrsTransformPoint(point.x(), point.y(),obstacleLayer.crs(), define._canvas.mapSettings().destinationCrs(), altitude)
                        else:
                            positionDegree = Point3D(point.x(), point.y(), altitude)
                    obstacle = Obstacle(name, position, obstacleLayer.id(), featureID, None, trees, ObstacleTable.MocMultiplier, tolerance)
                    obstacle.positionDegree = positionDegree
                    if self.manualPolygon != None:
                        if not self.manualPolygon.contains(obstacle.Position):
                            continue
                    self.checkObstacle(obstacle)
                    self.progress.setValue(k)
                    QApplication.processEvents()
                    j += 1
                    featureID += 1
                    k += 1
                i += 1
        self.progress.setValue(maxium)
        define._messagBar.hide()
        self.manualPolygon = None
    def loadObstaclesVector(self, obstacleLayers, surfaceLayers):
        progressMessageBar = define._messagBar.createMessage("Loading Vector Obstacles...")
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)        
        progressMessageBar.layout().addWidget(self.progress)
        define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
        maxium = 0        
        self.progress.setValue(0)
        for ly in obstacleLayers:
            maxium += ly.featureCount ()
        
        if maxium == 0:
            return False             
        self.progress.setMaximum(maxium)
        
        for obstacleLayer in obstacleLayers:
            obstacleUnits = obstacleLayer.crs().mapUnits()    
            features = QgisHelper.getFeaturesInLayerExtent(define._canvas, obstacleLayer, surfaceLayers, SelectionModeType.Automatic)
#             print len(features)
            for feature in features:
                name = feature.attribute("Name").toString()
                altitude = feature.attribute("Altitude").toFloat()[0]
                trees = define._trees
                tolerance = define._tolerance
                point = feature.geometry().asPoint()
                position = Point3D()
                positionDegree = Point3D()
                if define._canvas.mapUnits() == QGis.Meters:
                    if define._canvas.mapSettings().destinationCrs() != obstacleLayer.crs():
                        position = QgisHelper.CrsTransformPoint(point.x(), point.y(),obstacleLayer.crs(), define._canvas.mapSettings().destinationCrs(), altitude)
                    else:
                        position = Point3D(point.x(), point.y(), altitude)
                else:
                    if define._canvas.mapSettings().destinationCrs() != obstacleLayer.crs():
                        positionDegree = QgisHelper.CrsTransformPoint(point.x(), point.y(),obstacleLayer.crs(), define._canvas.mapSettings().destinationCrs(), altitude)
                    else:
                        positionDegree = Point3D(point.x(), point.y(), altitude)
                featureId = feature.id()
                layerId = obstacleLayer.id()
                obstacle = Obstacle(name, position, layerId, featureId, None, trees, ObstacleTable.MocMultiplier, tolerance)
                obstacle.positionDegree = positionDegree
#                 obstacle.positionDegree = positionDegree
                self.checkObstacle(obstacle)
                self.progress.setValue(self.progress.value() + 1)
                QApplication.processEvents()
            QApplication.processEvents()
        self.progress.setValue(maxium)
        define._messagBar.hide()
        self.manualPolygon = None
    def addObstacleToModel(self, obstacle, checkResult = None):
        standardItemList = []
        # obstacle.positionDegree = QgisHelper.Meter2Degree(obstacle.Position.x(), obstacle.Position.y())
        standardItem = QStandardItem(str(obstacle.featureId))
        standardItem.setData(obstacle.featureId)
        standardItemList.append(standardItem)
           
        standardItem = QStandardItem(str(obstacle.layerId))
        standardItem.setData(obstacle.layerId)
        standardItemList.append(standardItem)
           
        standardItem = QStandardItem(str(obstacle.name))
        standardItem.setData(obstacle.name)
        standardItemList.append(standardItem)
          
        standardItem = QStandardItem(str(obstacle.Position.x()))
        standardItem.setData(obstacle.Position.x())
        standardItemList.append(standardItem)
            
        standardItem = QStandardItem(str(obstacle.Position.y()))
        standardItem.setData(obstacle.Position.y())
        standardItemList.append(standardItem)
        
        value = QVariant(QgisHelper.strDegree(obstacle.positionDegree.y()))
        standardItem = QStandardItem(value.toString())
        standardItem.setData(obstacle.positionDegree.y())
        standardItemList.append(standardItem)
        strV = QgisHelper.strDegree(obstacle.positionDegree.y())
        
        value = QVariant(QgisHelper.strDegree(obstacle.positionDegree.x()))
        standardItem = QStandardItem(value.toString())
        standardItem.setData(obstacle.positionDegree.x())
        standardItemList.append(standardItem)
            
        standardItem = QStandardItem(str(obstacle.Position.z()))
        standardItem.setData(obstacle.Position.z())
        standardItemList.append(standardItem)
            
        standardItem = QStandardItem(str(Unit.ConvertMeterToFeet(obstacle.Position.z())))
        standardItem.setData(Unit.ConvertMeterToFeet(obstacle.Position.z()))
        standardItemList.append(standardItem)
            
        standardItem = QStandardItem(str(obstacle.trees))
        standardItem.setData(obstacle.trees)
        standardItemList.append(standardItem)
            
        standardItem = QStandardItem(str(Unit.ConvertMeterToFeet(obstacle.trees)))
        standardItem.setData(Unit.ConvertMeterToFeet(obstacle.trees))
        standardItemList.append(standardItem)
                
#         for i in range(len(standardItemList), self.source.columnCount()):
#             standardItemList.append(QStandardItem("None"))
        
        self.source.appendRow(standardItemList)
        
        standardItem = QStandardItem(str(obstacle.mocMultiplier))
        standardItem.setData(obstacle.mocMultiplier)
        self.source.setItem(self.source.rowCount() - 1, self.IndexMocMultiplier, standardItem)

    def checkObstacle(self, obstacle):
        pass

    def CompareObstacleRows(self, newRow, row, ignore):
        pass

    def method_0(self, obstacle_0):
        colCount = self.columnCount()
        objectId = range(colCount)
        
        objectId[0] = (obstacle_0.featureId)
        objectId[1] = (obstacle_0.name)
        objectId[2] = (obstacle_0.position.x())
        objectId[3] = (obstacle_0.position.y())
        objectId[4] = (obstacle_0.Position.z())
        position = obstacle_0.position
        objectId[6] = (Unit.ConvertMeterToFeet(position.z()))
        objectId[7] = (obstacle_0.trees)
        objectId[8] = (Unit.ConvertMeterToFeet(obstacle_0.Trees))
        if (self.IndexMocMultiplier > -1):
            objectId[self.IndexMocMultiplier] = obstacle_0.MocMultiplier;

        return objectId
    
    def method_1(self, object_0):
        pass
def processDEMMethod(lock,i ,j ,hCount,wCount,block,wStartNumber,hStartNumber,xStartValue,yStartValue,xOffSet, yOffSet,obstacleLayer,obstacleTable,obstacleUnits,mocMultiplier):
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
            
            
#                     endTime = time.time()
#                     print "endTime" + str(endTime)
            
            j += 1
            featureID += 1
#                 obstacle = None
#             print i
        lock.acquire()
        try:
            
            obstacleTable.progress.setValue(obstacleTable.progress.value() + 1)
            QApplication.processEvents()
        finally:
            lock.release()
        i += 1  
#         print i