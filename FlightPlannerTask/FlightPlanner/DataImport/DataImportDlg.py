'''
Created on 25 May 2014

@author: Administrator
'''
from PyQt4.QtGui import QColor, QDialogButtonBox, QStandardItemModel,QStandardItem, QMessageBox,\
             QFileDialog,QColor, QPushButton, QMessageBox, QDialog, QHBoxLayout, QVBoxLayout,\
             QProgressBar, QSortFilterProxyModel, QApplication, QAbstractItemView
from PyQt4.QtCore import QCoreApplication,Qt,QFileInfo, QFile, QVariant, QString, QDir, QStringList
from PyQt4.QtXml import QDomDocument
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.DataImport.ui_DataImport import Ui_DataImport
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.FlightPlanBaseSimpleDlg import FlightPlanBaseSimpleDlg
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.types import SurfaceTypes, AltitudeUnits, DegreesType, DegreesStyle,\
                                 GeoCalculationType, DataBaseCoordinateType
from FlightPlanner.Captions import Captions
from FlightPlanner.validations import Validations
from FlightPlanner.helpers import MathHelper, Altitude, Distance
from FlightPlanner.helpers import Unit
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Captions import Captions
from map.tools import SelectByRect, QgsMapToolSelectFreehand, QgsMapToolSelectPolygon, QgsMapToolSelectRadius
import define
import math
# from Type.Degrees import Degrees
from FlightPlanner.types import SurfaceTypes, DistanceUnits, Point3D, TurnDirection, SymbolType
from FlightPlanner.QgisHelper import QgisHelper
from qgis.gui import QgsComposerView, QgsRubberBand, QgsRendererV2PropertiesDialog
from qgis.core import QGis, QgsVectorFileWriter, QgsGeometry, QgsCsException, QgsPoint,\
        QgsFeatureRequest, QgsCoordinateTransform, QgsFeature, QgsVectorLayer, QgsProviderRegistry,\
        QgsStyleV2, QgsField,QgsCoordinateReferenceSystem, QgsSymbolV2, QgsSvgMarkerSymbolLayerV2,\
        QgsRendererCategoryV2, QgsCategorizedSymbolRendererV2
import os, math, random
from qgis.core import (QgsVectorLayer,
                        QgsMapLayerRegistry,
                        QgsCategorizedSymbolRendererV2,
                        QgsSymbolV2,
                        QgsRendererCategoryV2)
import ctypes, win32api
# import os, datetime
from FlightPlanner.DataImport.DlgAirspaceDataEdit import DlgAirspaceDataEdit
from FlightPlanner.DataImport.DlgPointDataEdit import DlgPointDataEdit
from FlightPlanner.DataImport.DlgGeoBorderDataEdit import DlgGeoBorderDataEdit
from FlightPlanner.DataImport.DlgRouteDataEdit import DlgRouteDataEdit
from FlightPlanner.DataImport.DlgDetailDataEdit import DlgDetailDataEdit
from Type.String import String

class DataImportDlg(FlightPlanBaseSimpleDlg):    
    def __init__(self, parent):
        FlightPlanBaseSimpleDlg.__init__(self, parent)
        self.setObjectName("DataImport")
        self.surfaceType = SurfaceTypes.DataImport
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.DataImport)
        self.vectorLayer = None
        self.resize(900, 550)
        QgisHelper.matchingDialogSize(self, 900, 550)
        self.dataImportCount = 0
        self.symbolImportCount = 0
        self.xmlFlag = False
        self.csvLayerSelect = False
        self.standardItemModel = QStandardItemModel()
        self.standardItemModelDetail = QStandardItemModel()
#         self.parametersPanel.tableView.setModel(self.standardItemModel)
        self.aixm = None
        self.standardItemModel_tree = QStandardItemModel()
        self.parametersPanel.tree.setModel(self.standardItemModel_tree)
        
        self.airspaceColumnLabels = ["Name",
                                     "Lower Limit(m)",
                                     "Upper Limit(m)",
                                     "Radius(m)",
                                     "No. Vertices",
                                     "No",
                                     "SortByName"]
        self.airspaceDetailColumnLabels = ["X",
                                           "Y",
                                           "Latitude",
                                           "Longitude",
                                           "Altitude(m)",
                                           "Type",
                                           "Cen. Latitude",
                                           "Cen. Longitude"]
        self.routesColumnLabels = ["Name",
                                   "No. Segments",
                                     "No",
                                     "SortByName"]
        self.routesDetailColumnLabels = ["X",
                                           "Y",
                                           "Latitude",
                                           "Longitude",
                                           "Altitude(m)",
                                           "Type",
                                           "Magn. Variation"]
        self.borderColumnLabels = ["Name",
                                   "Type",
                                   "No. Vertices",
                                     "No",
                                     "SortByName"]
        self.borderDetailColumnLabels = ["X",
                                           "Y",
                                           "Latitude",
                                           "Longitude",
                                           "Altitude(m)",
                                           "Type"]
        self.obstaclesColumnLabels = ["Name",
                                      "Latitude",
                                      "Longitude",
                                      "Altitude(m)",
                                      "Type",
                                      "Remarks",
                                     "SortByName"]
        self.symbolsColumnLabels = ["Name",
                                    "Latitude",
                                    "Longitude",
                                    "Altitude",
                                    "Type",
                                    "Remarks",
                                     "SortByName"]
        
        self.sortFilterProxyModel = QSortFilterProxyModel()
#         self.sortFilterProxyModel.setDynamicSortFilter(True)
        self.sortFilterProxyModel.setSourceModel(self.standardItemModel)
        self.sortFilterProxyModel.layoutChanged.connect(self.setVerticalHeader)
        self.parametersPanel.tableView.setModel(self.sortFilterProxyModel)
        self.parametersPanel.tableViewDetail.setModel(self.standardItemModelDetail)
        self.parametersPanel.tableView.setSortingEnabled(True)
        self.parametersPanel.tableViewDetail.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.csvLayerSelect  = False
        self.selectedItem = None
#         self.sortFilterProxyModel.setSortRole(Qt.UserRole + 1)
        self.abstructModel = QStandardItemModel()
        
        self.csvLayerName = ""
        self.csvCrsDescription = "4326"

        s = "EVRR FIR"
        ss = s.index(" ")
        ss1 = s.index("")
        ss2 = s[ss+1:len(s)]

        self.xFieldName = None
        self.yFieldName = None
        print ss2

        self.addDataDlg = None
        self.selectedRow = None
        self.selectedDetailRow = None
        self.selectedRowSortModel = None

#         sss = [[], 1, "s", [1,2]]
#         print len(sss[0])
    def createLayer(self):
#         if self.xmlFlag:
#             self.dataImportCount = 0
        fileInfo = QFileInfo(self.parametersPanel.txtFile.text())
        fileName0 = fileInfo.fileName()
        constructionLayer = None
        
        progressMessageBar = define._messagBar.createMessage("Creating layer...")
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)        
        progressMessageBar.layout().addWidget(self.progress)
        define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
        pointDataCount = 0
        
        
        
        if len(self.aixm.pointData) > 0 and self.selectedItem != None and self.selectedItem.text() == Captions.SYMBOLS:
            constructionLayer = QgsVectorLayer("point?crs=EPSG:4326", Captions.SYMBOLS, "memory")

            # if define.obstaclePath != None:
            #     shpPath = define.obstaclePath
            # elif define.xmlPath != None:
            #     shpPath = define.xmlPath
            # else:
            #     shpPath = define.appPath
            # er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + Captions.SYMBOLS + ".shp", "utf-8", constructionLayer.crs())
            # constructionLayer = QgsVectorLayer(shpPath + "/" + Captions.SYMBOLS + ".shp", Captions.SYMBOLS, "ogr")

            constructionLayer.startEditing()
            pr = constructionLayer.dataProvider()          
            pr.addAttributes([QgsField("Name", QVariant.String),
                              QgsField("Latitude", QVariant.Double),
                              QgsField("Longitude", QVariant.Double),
                               QgsField("Altitude", QVariant.Double),
                                QgsField("Attributes", QVariant.String),
                                QgsField("Type", QVariant.String)])
            if not self.parametersPanel.cmbType.currentIndex() > 0:
                pointDataCount = len(self.aixm.pointData)
                self.progress.setMaximum(pointDataCount)
                i = 0
                for sym in self.aixm.pointData:   
                    self.progress.setValue(i)
                    feature = QgsFeature()
                    lat = self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, 1)).toDouble()
                    lon = self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, 2)).toDouble()
                    feature.setGeometry( QgsGeometry.fromPoint(QgsPoint(lon[0], lat[0])) )
                    sym5 = self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, 3))
                    if sym5 == None or sym5.toString() == "":
                        feature.setAttributes([self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, 0)).toString(),
                                               lat[0],
                                               lon[0],
                                                0.0,
                                                self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, 5)).toString(),
                                                self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, 4)).toString()])
                    else:
                        altitude = self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, 3)).toDouble()
                        feature.setAttributes([self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, 0)).toString(),
                                               lat[0],
                                               lon[0],
                                                altitude[0] ,
                                                self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, 5)).toString(),
                                                self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, 4)).toString()])
                    pr.addFeatures([feature])
                    i += 1
#                 constructionLayer.setLayerName(Captions.SYMBOLS + "_" + self.parametersPanel.cmbType.currentText())
            else:
                pointDataCount = self.sortFilterProxyModel.rowCount()
                self.progress.setMaximum(pointDataCount)
                i = 0
                for sym in self.aixm.pointData:
                    if sym[7] == self.parametersPanel.cmbType.currentText():   
                        self.progress.setValue(i)
                        feature = QgsFeature()
                        lat = float(sym[3])
                        lon = float(sym[4])
                        feature.setGeometry( QgsGeometry.fromPoint(QgsPoint(lon, lat)) )
                        if sym[5] == None or sym[5] == "":
                            feature.setAttributes([sym[0],
                                                    0.0,
                                                    sym[6],
                                                    sym[7]])
                        else:
                            feature.setAttributes([sym[0],
                                                    float(sym[5]),
                                                    sym[6],
                                                    sym[7]])
                        pr.addFeatures([feature])
                        i += 1
                constructionLayer.setLayerName(Captions.SYMBOLS + "_" + self.parametersPanel.cmbType.currentText())
                
        if len(self.aixm.pointDataObstacles) > 0 and self.selectedItem != None and self.selectedItem.text() == Captions.OBSTACLES:
            constructionLayer = QgsVectorLayer("point?crs=EPSG:4326", Captions.OBSTACLES, "memory")
            # shpPath = ""
            # if define.obstaclePath != None:
            #     shpPath = define.obstaclePath
            # elif define.xmlPath != None:
            #     shpPath = define.xmlPath
            # else:
            #     shpPath = define.appPath
            # er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + Captions.OBSTACLES + ".shp", "utf-8", constructionLayer.crs())
            # constructionLayer = QgsVectorLayer(shpPath + "/" + Captions.OBSTACLES + ".shp", Captions.OBSTACLES, "ogr")


            constructionLayer.startEditing()
            pr = constructionLayer.dataProvider()          
            pr.addAttributes([QgsField("Name", QVariant.String),
                               QgsField("Altitude", QVariant.Double),
                                QgsField("Attributes", QVariant.String),
                                QgsField("Type", QVariant.String)])
            pointDataCount = self.sortFilterProxyModel.rowCount()
            self.progress.setMaximum(pointDataCount)
            i = 0
            if not self.parametersPanel.cmbType.currentIndex() > 0:
                for obs in self.aixm.pointDataObstacles:      
                    self.progress.setValue(i)      
                    feature = QgsFeature()
                    feature.setGeometry( QgsGeometry.fromPoint(QgsPoint(float(obs[4]),float(obs[3]))) )
    #                     if obs[3] == None or obs[3] == "":
                    
                    if obs[5] == None or obs[5] == "":
                        feature.setAttributes([obs[0], 0.0, obs[6], obs[7]])
                    else:
                        feature.setAttributes([obs[0], float(obs[5]), obs[6], obs[7]])
    #                     else:
    #                         feature.setAttributes([obs[0], float(obs[3]), FlightPlanner.DataImport.DataImportDlg[4]])
                    pr.addFeatures([feature])
                    i += 1
            else:
                for obs in self.aixm.pointDataObstacles:
                    if obs[7] == self.parametersPanel.cmbType.currentText():          
                        self.progress.setValue(i)      
                        feature = QgsFeature()
                        feature.setGeometry( QgsGeometry.fromPoint(QgsPoint(float(obs[4]),float(obs[3]))) )
        #                     if obs[3] == None or obs[3] == "":
                        
                        if obs[5] == None or obs[5] == "":
                            feature.setAttributes([obs[0], 0.0, obs[6], obs[7]])
                        else:
                            feature.setAttributes([obs[0], float(obs[5]), obs[6], obs[7]])
        #                     else:
        #                         feature.setAttributes([obs[0], float(obs[3]), FlightPlanner.DataImport.DataImportDlg[4]])
                        pr.addFeatures([feature])
                        i += 1
                constructionLayer.setLayerName(Captions.OBSTACLES + "_" + self.parametersPanel.cmbType.currentText())
        if len(self.aixm.pointDataAirspace) > 0 and self.selectedItem != None and self.selectedItem.text() == Captions.AIRSPACE:
            resultPolylineAreaArray = self.method_49()
            constructionLayer = QgsVectorLayer("linestring?crs=EPSG:4326", Captions.AIRSPACE, "memory")
            # shpPath = ""
            # if define.obstaclePath != None:
            #     shpPath = define.obstaclePath
            # elif define.xmlPath != None:
            #     shpPath = define.xmlPath
            # else:
            #     shpPath = define.appPath
            # er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + Captions.AIRSPACE + ".shp", "utf-8", constructionLayer.crs())
            # constructionLayer = QgsVectorLayer(shpPath + "/" + Captions.AIRSPACE + ".shp", Captions.AIRSPACE, "ogr")



            constructionLayer.startEditing()
            pr = constructionLayer.dataProvider()
            pr.addAttributes([QgsField("Name", QVariant.String),
                               QgsField("Type_Name", QVariant.String),
                                QgsField("LowerLimit", QVariant.String),
                                QgsField("UpperLimit", QVariant.String),
                                QgsField("Radius", QVariant.String)])
            count = len(resultPolylineAreaArray)
            for polylineArea, dataRow in resultPolylineAreaArray:
                name = dataRow[0]
                startIndex = name.indexOf("(") + 1
                endIndex = name.indexOf(")")
                typeName = name.mid(startIndex, endIndex - startIndex)
                feature = QgsFeature()
                point3dArray = polylineArea.method_14()
                if QgsGeometry.fromPolyline(point3dArray) == None:
                    continue
                feature.setGeometry(QgsGeometry.fromPolyline(point3dArray))
                feature.setAttributes([dataRow[0], typeName, dataRow[1], dataRow[2], dataRow[3], dataRow[6]])
                pr.addFeatures([feature])
        if len(self.aixm.pointDataRoutes) > 0 and self.selectedItem != None and self.selectedItem.text() == Captions.ROUTES:
            resultPoint3dArrayList = self.method_53()
            if resultPoint3dArrayList == None or len(resultPoint3dArrayList) == 0:
#                 constructionLayer.commitChanges()
                self.vectorLayer = None
#                 self.progress.setValue(pointDataCount)
                define._messagBar.hide() 
                return
            constructionLayer = QgsVectorLayer("linestring?crs=EPSG:4326", Captions.ROUTES, "memory")
            # shpPath = ""
            # if define.obstaclePath != None:
            #     shpPath = define.obstaclePath
            # elif define.xmlPath != None:
            #     shpPath = define.xmlPath
            # else:
            #     shpPath = define.appPath
            # er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + Captions.ROUTES + ".shp", "utf-8", constructionLayer.crs())
            # constructionLayer = QgsVectorLayer(shpPath + "/" + Captions.ROUTES + ".shp", Captions.ROUTES, "ogr")


            constructionLayer.startEditing()
            pointDataCount = len(resultPoint3dArrayList)
            self.progress.setMaximum(pointDataCount)
            i = 0

            pr = constructionLayer.dataProvider()
            pr.addAttributes([QgsField("Name", QVariant.String),
                               QgsField("Type_Name", QVariant.String)])
            for point3dArrayL, dataRow in resultPoint3dArrayList:
                self.progress.setValue(i)
                name = dataRow[0]
                startIndex = name.indexOf(" ") + 1
                endIndex = name.length()
                typeName = name.mid(startIndex, endIndex - startIndex)
                for point3dArray in point3dArrayL:
                    feature = QgsFeature()
                    feature.setGeometry(QgsGeometry.fromPolyline(point3dArray))
                    feature.setAttributes([dataRow[0], typeName])
                    pr.addFeatures([feature])
                i += 1
        if len(self.aixm.pointDataBorder) > 0 and self.selectedItem != None and self.selectedItem.text() == Captions.GEOGRAPHICAL_BORDER:
            resultPoint3dArrayList = self.method_51()
            if resultPoint3dArrayList == None or len(resultPoint3dArrayList) == 0:
#                 constructionLayer.commitChanges()
                self.vectorLayer = None
#                 self.progress.setValue(pointDataCount)
                define._messagBar.hide() 
                return
            constructionLayer = QgsVectorLayer("linestring?crs=EPSG:4326", Captions.GEOGRAPHICAL_BORDER, "memory")

            # shpPath = ""
            # if define.obstaclePath != None:
            #     shpPath = define.obstaclePath
            # elif define.xmlPath != None:
            #     shpPath = define.xmlPath
            # else:
            #     shpPath = define.appPath
            # er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + QString(Captions.GEOGRAPHICAL_BORDER).replace(" ", "") + ".shp", "utf-8", constructionLayer.crs())
            # constructionLayer = QgsVectorLayer(shpPath + "/" + QString(Captions.GEOGRAPHICAL_BORDER).replace(" ", "") + ".shp", Captions.GEOGRAPHICAL_BORDER, "ogr")


            constructionLayer.startEditing()
            pointDataCount = len(resultPoint3dArrayList)
            self.progress.setMaximum(pointDataCount)
            i = 0

            pr = constructionLayer.dataProvider()
            pr.addAttributes([QgsField("Name", QVariant.String),
                               QgsField("Type_Name", QVariant.String),
                                QgsField("Type", QVariant.String)])
            for point3dArrayL, dataRow in resultPoint3dArrayList:
                name = dataRow[0]
                startIndex = name.indexOf("_") + 1
                endIndex = name.length()
                typeName = name.mid(startIndex, endIndex - startIndex)

                self.progress.setValue(i)
                feature = QgsFeature()
                feature.setGeometry(QgsGeometry.fromPolyline(point3dArrayL))
                feature.setAttributes([dataRow[0], typeName, dataRow[1]])
                pr.addFeatures([feature])
                i += 1
                    
#                     feature.setGeometry(QgsGeometry.fromPolyline(point3dArray[1]))
#                     constructionLayer.addFeature(feature)
#                     
#                     feature.setGeometry(QgsGeometry.fromPolyline(point3dArray[2]))
#                     constructionLayer.addFeature(feature)
#         if len(self.aixm.pointDataRoutes) > 0:
#             for route in self.aixm.pointDataRoutes:            
#                 feature = QgsFeature()
#                 feature.setGeometry( QgsGeometry.fromPoint(QgsPoint(float(route[1]),float(route[2]))) )
# #                     if route[3] == None or route[3] == "":
#                 feature.setAttributes([route[0], 0.0, route[3], "Routes"])
# #                     else:
# #                         feature.setAttributes([route[0], float(route[3]), route[4]])
#                 pr.addFeatures([feature])
        constructionLayer.commitChanges()
#             QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.Obstacles)
        shpPath = ""
        if define.obstaclePath != None:
            shpPath = define.obstaclePath
        elif define.xmlPath != None:
            shpPath = define.xmlPath
        else:
            shpPath = define.appPath
        # er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + Captions.SYMBOLS + ".shp", "utf-8", define._canvas.mapSettings().destinationCrs())
        # self.vectorLayer = QgsVectorLayer(shpPath + "/" + Captions.SYMBOLS + ".shp", Captions.SYMBOLS, "ogr")

        # self.vectorLayer = constructionLayer

        self.dataImportCount += 1
        
        self.progress.setValue(pointDataCount)
        define._messagBar.hide()

        shpPath = ""
        if define.obstaclePath != None:
            shpPath = define.obstaclePath
        elif define.xmlPath != None:
            shpPath = define.xmlPath
        else:
            shpPath = define.appPath
        layerName = String.QString2Str(constructionLayer.name())
        layerName = layerName.replace(".", "_")
        layerName = layerName.replace("-", "_")
        fileInfo = QFileInfo(shpPath + "/" + QString(layerName).replace(" ", "") + ".shp")
        if fileInfo.exists():
            f = QFile.remove(shpPath + "/" + QString(layerName).replace(" ", "") + ".shp")
            # f = file.remove()

        if self.vectorLayer != None and isinstance(self.vectorLayer, QgsVectorLayer) and self.vectorLayer.name() == layerName:
            QgisHelper.removeFromCanvas(define._canvas, [self.vectorLayer])
        er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + QString(layerName).replace(" ", "")
                                                     + ".shp", "utf-8", constructionLayer.crs())
        self.vectorLayer = QgsVectorLayer(shpPath + "/" + QString(layerName).replace(" ", "") + ".shp", layerName, "ogr")


    def btnConstruct_Click(self):
        # dlg = QgsComposerView(self, "Composer")
        # self.ui.horizontalLayout_3.addWidget(dlg)
        # mD = dlg.composerWindow()
        # mD.show()

        # dlg._class_ = QDialog
        # dlg.exec_()

        if self.xmlFlag:
            self.createLayer()
        try:
            if self.vectorLayer == None or not self.vectorLayer.isValid():
                QMessageBox.warning(self, "Warning", "No data exist or data is not valid.")
                return
        except:
            return
        
#         if self.csvLayerSelect or self.parametersPanel.txtName.text() == Captions.SYMBOLS or self.parametersPanel.txtName.text() == Captions.OBSTACLES:
        
        if self.selectedItem != None and (self.selectedItem.text() == Captions.OBSTACLES or self.selectedItem.text() == Captions.SYMBOLS):
            myTargetField = "Type"
            myRenderer = None
            if self.parametersPanel.cmbType.currentIndex() > 0:
#                 if self.selectedItem.text() == Captions.SYMBOLS:
                svgFileName = "Default"
                if self.parametersPanel.cmbType.currentText() == SymbolType.Arp:
                    svgFileName = "Arp.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Repnc:
                    svgFileName = "Repnc.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Faf:
                    svgFileName = "Faf.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Vor:
                    svgFileName = "Vor.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Vord:
                    svgFileName = "Vord.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Tacan:
                    svgFileName = "Tacan.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Dme:
                    svgFileName = "Dme.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Ndb:
                    svgFileName = "Ndb.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Be1:
                    svgFileName = "Be1.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Gp:
                    svgFileName = "Gp.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Obst1:
                    svgFileName = "Obst1.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Obst2:
                    svgFileName = "Obst2.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Obst3:
                    svgFileName = "Obst3.svg"
                elif self.parametersPanel.cmbType.currentText() == SymbolType.Obst4:
                    svgFileName = "Obst4.svg"
                    
                symbol = QgsSymbolV2.defaultSymbol(self.vectorLayer.geometryType())
                
                svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/Symbols/" + svgFileName, 6.0, 0.0)
                if svgFileName != "Default":
                    symbol.deleteSymbolLayer(0)
                    symbol.appendSymbolLayer(svgSymLayer)
                myRange2 = QgsRendererCategoryV2(self.parametersPanel.cmbType.currentText(),
                                            symbol,
                                            self.parametersPanel.cmbType.currentText())
#                 myRangeList.append(myRange2)
                myRenderer = QgsCategorizedSymbolRendererV2("", [myRange2])
            else:
                myRangeList = []
                for i in range(1, self.parametersPanel.cmbType.count()):
                    svgFileName = "Default"
                    if self.parametersPanel.cmbType.itemText(i) == SymbolType.Arp:
                        svgFileName = "Arp.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Repnc:
                        svgFileName = "Repnc.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Faf:
                        svgFileName = "Faf.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Vor:
                        svgFileName = "Vor.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Vord:
                        svgFileName = "Vord.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Tacan:
                        svgFileName = "Tacan.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Dme:
                        svgFileName = "Dme.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Ndb:
                        svgFileName = "Ndb.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Be1:
                        svgFileName = "Be1.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Gp:
                        svgFileName = "Gp.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Obst1:
                        svgFileName = "Obst1.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Obst2:
                        svgFileName = "Obst2.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Obst3:
                        svgFileName = "Obst3.svg"
                    elif self.parametersPanel.cmbType.itemText(i) == SymbolType.Obst4:
                        svgFileName = "Obst4.svg"
                        
                    symbol = QgsSymbolV2.defaultSymbol(self.vectorLayer.geometryType())
                    
                    svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/Symbols/" + svgFileName, 6.0, 0.0)
                    if svgFileName != "Default":
                        symbol.deleteSymbolLayer(0)
                        symbol.appendSymbolLayer(svgSymLayer)
                    myRange2 = QgsRendererCategoryV2(self.parametersPanel.cmbType.itemText(i),
                                                symbol,
                                                self.parametersPanel.cmbType.itemText(i))
                    myRangeList.append(myRange2)
                myRenderer = QgsCategorizedSymbolRendererV2("", myRangeList)
                
        #         myRenderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
            myRenderer.setClassAttribute(myTargetField)
#             layer.setRendererV2(myRenderer)
            self.vectorLayer.setRendererV2(myRenderer)


            QgisHelper.appendToCanvas(define._canvas, [self.vectorLayer], "AIXM")
            self.vectorLayer.triggerRepaint()
            return
        
        
        
        
        if not self.xmlFlag:
            csvVectorLayer = QgsVectorLayer("point?crs=EPSG:" + self.csvCrsDescription, self.csvLayerName, "memory")
            # shpPath = ""
            # if define.obstaclePath != None:
            #     shpPath = define.obstaclePath
            # elif define.xmlPath != None:
            #     shpPath = define.xmlPath
            # else:
            #     shpPath = define.appPath
            # er = QgsVectorFileWriter.writeAsVectorFormat(csvVectorLayer, shpPath + "/" + self.csvLayerName + ".shp", "utf-8", csvVectorLayer.crs())
            # csvVectorLayer = QgsVectorLayer(shpPath + "/" + self.csvLayerName + ".shp", self.csvLayerName, "ogr")


            csvVectorLayer.startEditing()
            pr = csvVectorLayer.dataProvider()
            altitudeFieldName = self.parametersPanel.cmbAlFieldName.currentText()
            for i in range(self.standardItemModel.columnCount()):
                columnName = self.standardItemModel.headerData(i, Qt.Horizontal).toString()
                if i == 0:
                    pr.addAttributes([QgsField("Name", QVariant.String)])
                elif columnName == altitudeFieldName:
                    pr.addAttributes([QgsField("Altitude", QVariant.Double)])
                elif columnName == self.xFieldName:
                    pr.addAttributes([QgsField(self.xFieldName, QVariant.String)])
                elif columnName == self.yFieldName:
                    pr.addAttributes([QgsField(self.yFieldName, QVariant.String)])

                else:
                    pr.addAttributes([QgsField(columnName, QVariant.String)])
            
            progressMessageBar = define._messagBar.createMessage("Creating layer...")
            self.progress = QProgressBar()
            self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)        
            progressMessageBar.layout().addWidget(self.progress)
            define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
            pointDataCount = self.standardItemModel.rowCount()
            
            self.progress.setMaximum(self.standardItemModel.rowCount())
            
            for i in range(self.standardItemModel.rowCount()):
                pointData = []
                lat = 0.0
                lon = 0.0
                altitude = 0.0   
                for j in range(self.standardItemModel.columnCount()):
                    columnName = self.standardItemModel.headerData(j, Qt.Horizontal).toString()
                    if self.standardItemModel.item(i, j) != None:
#                         pointData.append(self.standardItemModel.item(i, j).text())
                        value = self.standardItemModel.item(i, j).text()
                        if columnName == self.yFieldName:
                            if self.csvCrsDescription == "4326":
                                if value.toDouble()[0] > 90 or value.toDouble()[0] < -90:
                                    lat = Degrees.String2Degree(str(value.toDouble()[0])).value
                                else:
                                    lat = value.toDouble()[0]
                            else:
                                lat = value.toDouble()[0]
                            pointData.append(self.standardItemModel.item(i, j).text())
#                             break
                        elif columnName == self.xFieldName:
                            if self.csvCrsDescription == "4326":
                                if value.toDouble()[0] > 180 or value.toDouble()[0] < -180:
                                    lon = Degrees.String2Degree(str(value.toDouble()[0])).value
                                else:
                                    lon = value.toDouble()[0]
                            else:
                                lon = value.toDouble()[0]
                            pointData.append(self.standardItemModel.item(i, j).text())
#                             break
                        elif columnName == altitudeFieldName:
                            if self.parametersPanel.cmbAlUnit.currentText() == "Meter":
                                altitude = value.toDouble()[0]
                                pointData.append(str(altitude))
#                                 break
                            else:
                                altitudeFeet = value.toDouble()[0]
                                altitude = Unit.ConvertFeetToMeter(altitudeFeet)
                                pointData.append(str(altitude))
#                                 break
#                             break
                        else:
                            pointData.append(self.standardItemModel.item(i, j).text())
                            
                    else:
                        pointData.append("")
                     
                 
                feature = QgsFeature()
                feature.setGeometry( QgsGeometry.fromPoint(QgsPoint(lon, lat)) )
                feature.setAttributes(pointData)
                pr.addFeatures([feature])
                self.progress.setValue(i)
            self.progress.setValue(pointDataCount)
            define._messagBar.hide() 
            csvVectorLayer.commitChanges()

            shpPath = ""
            if define.obstaclePath != None:
                shpPath = define.obstaclePath
            elif define.xmlPath != None:
                shpPath = define.xmlPath
            else:
                shpPath = define.appPath

            layers = define._canvas.layers()
            removeFlag = False
            if len(layers) > 0:
                for ly in layers:
                    if self.csvLayerName == ly.name():
                        QgisHelper.removeFromCanvas(define._canvas, [ly])
                        removeFlag = True
                        break
                define._canvas.refresh()
            if removeFlag:
                directory = QDir(shpPath)
                strList = QStringList()
                strList.append(self.csvLayerName)
                entryInfoList = directory.entryInfoList()
                for fileInfo in entryInfoList:
                    if fileInfo.isFile() and fileInfo.fileName().contains(self.csvLayerName):
                        b = QFile.remove(fileInfo.filePath())
                        pass
                fileInfo = QFileInfo(shpPath + "/" + self.csvLayerName + ".shp")

            er = QgsVectorFileWriter.writeAsVectorFormat(csvVectorLayer, shpPath + "/" + self.csvLayerName + ".shp", "utf-8", define._canvas.mapSettings().destinationCrs())
            csvVectorLayer = QgsVectorLayer(shpPath + "/" + self.csvLayerName + ".shp", self.csvLayerName, "ogr")

    #         QgisHelper.appendToCanvas(define._canvas, [csvVectorLayer], "AIXM")      
    #         pr.addAttributes([QgsField("Name", QVariant.String),
    #                            QgsField("Altitude", QVariant.Double),
    #                             QgsField("Attributes", QVariant.String),
    #                             QgsField("Type", QVariant.String)])
                
            
            
            dlg = QDialog(self)
            dlg.setObjectName("dlg")
            dlg.setWindowTitle("Select Symbol")
            vLayout = QVBoxLayout(dlg)
            vLayout.setObjectName("vLayout")
             
            self.mRendererDialog = QgsRendererV2PropertiesDialog( csvVectorLayer, QgsStyleV2.defaultStyle(), True )
            vLayout.addWidget(self.mRendererDialog)
             
            buttonBox = QDialogButtonBox(dlg)
            buttonBox.setOrientation(Qt.Horizontal)
            buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
            buttonBox.setObjectName("buttonBox")
             
            buttonBox.accepted.connect(dlg.accept)
            buttonBox.rejected.connect(dlg.reject)
             
            vLayout.addWidget(buttonBox)
            dlg.setLayout(vLayout)
            resultAccept = dlg.exec_()
            if resultAccept:
                self.mRendererDialog.apply()
    #             if self.dataImportCount != self.symbolImportCount:
                QgisHelper.appendToCanvas(define._canvas, [csvVectorLayer], "AIXM")
                     
    #                 self.symbolImportCount += 1
                csvVectorLayer.triggerRepaint()
            return    
            
            

            
        # dlg = QDialog(self)
        # dlg.setObjectName("dlg")
        # dlg.setWindowTitle("Select Symbol")
        # vLayout = QVBoxLayout(dlg)
        # vLayout.setObjectName("vLayout")
        #
        # self.mRendererDialog = QgsRendererV2PropertiesDialog( self.vectorLayer, QgsStyleV2.defaultStyle(), True )
        # vLayout.addWidget(self.mRendererDialog)
        #
        # buttonBox = QDialogButtonBox(dlg)
        # buttonBox.setOrientation(Qt.Horizontal)
        # buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        # buttonBox.setObjectName("buttonBox")
        #
        # buttonBox.accepted.connect(dlg.accept)
        # buttonBox.rejected.connect(dlg.reject)
        #
        # vLayout.addWidget(buttonBox)
        # dlg.setLayout(vLayout)
        # resultAccept = dlg.exec_()
        # if resultAccept:
        #     self.mRendererDialog.apply()



        myTargetField = "Type_Name"
        myRangeList = []
        myOpacity = 1
        count = int(round((self.parametersPanel.cmbType.count() - 1) / 3.0) + 0.5)
        # Make our first symbol and range...
        redValue = 0
        greenValue = 0
        blueValue = 0

        for i in range(1, self.parametersPanel.cmbType.count()):

            myLabel = self.parametersPanel.cmbType.itemText(i)
            # if i < count:
            #     redValue = i * int(255 / count)
            # elif i < 2 * count:
            #     greenValue = (i - count) * int(255 / count)
            # elif i < 3 * count:
            #     blueValue = (i -2 *  count) * int(255 / count)

            redValue = random.randint(0, 255)
            greenValue = random.randint(0, 255)
            blueValue = random.randint(0, 255)

            myColour = QColor(redValue, greenValue, blueValue)
            mySymbol1 = QgsSymbolV2.defaultSymbol(self.vectorLayer.geometryType())
            mySymbol1.setColor(myColour)
            # mySymbol1.setAlpha(myOpacity)
            myRange1 = QgsRendererCategoryV2(myLabel,
                                        mySymbol1,
                                        myLabel)
            myRangeList.append(myRange1)
        myRenderer = QgsCategorizedSymbolRendererV2("", myRangeList)
        myRenderer.setClassAttribute(myTargetField)
        self.vectorLayer.setRendererV2(myRenderer)
        if self.dataImportCount != self.symbolImportCount:
            QgisHelper.appendToCanvas(define._canvas, [self.vectorLayer], "AIXM")

            self.symbolImportCount += 1
        self.vectorLayer.triggerRepaint()
    def btnFile_Click(self):
        result = QMessageBox.warning(self, "Warning", "Click YES button if you want to open '*.xml' file.\nClick NO button if you want to open '*.txt' or '*.csv' file.", QMessageBox.Yes, QMessageBox.No, QMessageBox.Cancel)
        if result == QMessageBox.Yes:
            self.parametersPanel.cmbAlFieldName.clear()
            self.csvLayerSelect = False
            filePathDir = QFileDialog.getOpenFileName(self, "Open XML File",QCoreApplication.applicationDirPath (),"Obstclefiles(*.xml)")        
            if filePathDir == "":
                return

            self.aixm = DataBaseLoaderAixm(filePathDir, False)
            self.parametersPanel.txtFile.setText(filePathDir)
            self.standardItemModel_tree.clear()
            item = QStandardItem("Item:")
            self.standardItemModel_tree.setHorizontalHeaderItem(0, item)
#             if len(self.aixm.pointDataAirspace) >0:
#                 self.parametersPanel.cmbType.addItem(Captions.AIRSPACE)
            n = 0
            if len(self.aixm.pointDataAirspace) > 0:
                self.standardItemModel_tree.setItem(n, 0, QStandardItem(Captions.AIRSPACE))
                n += 1
            if len(self.aixm.pointDataBorder) > 0:
                self.standardItemModel_tree.setItem(n, 0, QStandardItem(Captions.GEOGRAPHICAL_BORDER))
                n += 1
            if len(self.aixm.pointDataObstacles) > 0:
                self.standardItemModel_tree.setItem(n, 0, QStandardItem(Captions.OBSTACLES))
                n += 1
            if len(self.aixm.pointDataRoutes) > 0:
                self.standardItemModel_tree.setItem(n, 0, QStandardItem(Captions.ROUTES))
                n += 1
            if len(self.aixm.pointData) > 0:
                self.standardItemModel_tree.setItem(n, 0, QStandardItem(Captions.SYMBOLS))
                n += 1
#             self.loadTable(self.aixm)
#             self.createLayer()
            self.ui.btnConstruct.setEnabled(True)
            self.xmlFlag = True
            self.csvLayerSelect = False
            fileInfo = QFileInfo(filePathDir)
            define.xmlPath = fileInfo.path()
        elif result == QMessageBox.No:     
            self.selectedItem = None       
            dlg = QgsProviderRegistry.instance().selectWidget("delimitedtext", self)

            dlg._class_ = QDialog
            dlg.addVectorLayer.connect(self.addSelectedVectorLayer)
            self.xmlFlag = False
            
            dlg.exec_()

            pass

    def loadTable(self, aixm):
        self.standardItemModel.clear()
        if self.parametersPanel.cmbType.currentText() == Captions.SYMBOLS:            
            item0 = QStandardItem("Name")
            self.standardItemModel.setHorizontalHeaderItem(0, item0)
            
            item1 = QStandardItem("Latitude")
            self.standardItemModel.setHorizontalHeaderItem(1, item1)
            item2 = QStandardItem("Longitude")
            self.standardItemModel.setHorizontalHeaderItem(2, item2)
            item3 = QStandardItem("Altitude")
            self.standardItemModel.setHorizontalHeaderItem(3, item3)
            item4 = QStandardItem("Attributes")
            self.standardItemModel.setHorizontalHeaderItem(4, item4)
            i = 0
            for sym in aixm.pointData:
                item = QStandardItem(sym[0])
                self.standardItemModel.setItem(i, 0, item)
                
                item = QStandardItem(sym[3])
                self.standardItemModel.setItem(i, 1, item)
                
                item = QStandardItem(sym[4])
                self.standardItemModel.setItem(i, 2, item)
                
                item = QStandardItem(sym[5])
                self.standardItemModel.setItem(i, 3, item)
                
                item = QStandardItem(sym[6])
                self.standardItemModel.setItem(i, 4, item)
                
                i += 1
        if self.parametersPanel.cmbType.currentText() == Captions.OBSTACLES:            
            item0 = QStandardItem("Name")
            self.standardItemModel.setHorizontalHeaderItem(0, item0)
            
            item1 = QStandardItem("Latitude")
            self.standardItemModel.setHorizontalHeaderItem(1, item1)
            item2 = QStandardItem("Longitude")
            self.standardItemModel.setHorizontalHeaderItem(2, item2)
#             item3 = QStandardItem("Altitude")
#             self.standardItemModel.setHorizontalHeaderItem(3, item3)
            item4 = QStandardItem("Attributes")
            self.standardItemModel.setHorizontalHeaderItem(3, item4)
            i = 0
            for sym in aixm.pointDataObstacles:
                item = QStandardItem(sym[0])
                self.standardItemModel.setItem(i, 0, item)
                
                item = QStandardItem(sym[3])
                self.standardItemModel.setItem(i, 1, item)
                
                item = QStandardItem(sym[4])
                self.standardItemModel.setItem(i, 2, item)
                
                item = QStandardItem(sym[5])
                self.standardItemModel.setItem(i, 3, item)
                
#                 item = QStandardItem(sym[6])
#                 self.standardItemModel.setItem(i, 4, item)
                
                i += 1
        if self.parametersPanel.cmbType.currentText() == Captions.ROUTES:            
            item0 = QStandardItem("Name")
            self.standardItemModel.setHorizontalHeaderItem(0, item0)
            
            item1 = QStandardItem("Latitude")
            self.standardItemModel.setHorizontalHeaderItem(1, item1)
            item2 = QStandardItem("Longitude")
            self.standardItemModel.setHorizontalHeaderItem(2, item2)
#             item3 = QStandardItem("Altitude")
#             self.standardItemModel.setHorizontalHeaderItem(3, item3)
            item4 = QStandardItem("Attributes")
            self.standardItemModel.setHorizontalHeaderItem(3, item4)
            i = 0
            for sym in aixm.pointDataObstacles:
                item = QStandardItem(sym[0])
                self.standardItemModel.setItem(i, 0, item)
                
                item = QStandardItem(sym[1])
                self.standardItemModel.setItem(i, 1, item)
                
                item = QStandardItem(sym[2])
                self.standardItemModel.setItem(i, 2, item)
                
                item = QStandardItem(sym[3])
                self.standardItemModel.setItem(i, 3, item)
                
#                 item = QStandardItem(sym[6])
#                 self.standardItemModel.setItem(i, 4, item)
                
                i += 1
            
        
    def addSelectedVectorLayer(self, uri, layerName, provider):
        if String.QString2Str(uri).find("xyDms=yes") == -1:
            self.csvCrsDescription = "32633"
        else:
            self.csvCrsDescription = "4326"
        self.parametersPanel.cmbAlFieldName.clear()
#         self.dataImportCount = 0
        self.vectorLayer = None
        self.csvLayerName = layerName
        s = uri
        s = s.mid(8, s.indexOf("?type") - 8)

        self.parametersPanel.txtFile.setText(s)
        uri = String.QString2Str(uri).replace("&xyDms=yes", "")
        self.vectorLayer = QgsVectorLayer(uri, layerName, provider)
        fields = self.vectorLayer.dataProvider().fields()
        fileInfo = QFileInfo(s)
        define.xmlPath = fileInfo.path()
        iterFeat = self.vectorLayer.getFeatures()
        self.standardItemModel.clear()
        feat = None
        pt = None
        for i in range(fields.count()):
            fieldName = fields.field(i).name()
            self.parametersPanel.cmbAlFieldName.addItems([fieldName])
            for feature in iterFeat:
                feat = feature
                break
            pt = feat.geometry().asPoint()
            valueStr = feat.attributes()[i].toString()
            if valueStr == str(pt.x()):
                self.xFieldName = fieldName
            elif valueStr == str(pt.y()):
                self.yFieldName = fieldName
            item = QStandardItem(fieldName)
            self.standardItemModel.setHorizontalHeaderItem(i, item)
#         self.parametersPanel.tableView.setModel(self.standardItemModel)

        iterFeat = self.vectorLayer.getFeatures()
        i = 0
        for feature in iterFeat:
            for idx in range(fields.count()):
                value = feature.attributes()[idx]
                item = QStandardItem(value.toString())
                self.standardItemModel.setItem(i, idx, item)
            i += 1
        self.dataImportCount += 1
        self.ui.btnConstruct.setEnabled(True)
        self.csvLayerSelect = True
#         QgisHelper.appendToCanvas(define._canvas, [self.vectorLayer], "New")
    def initParametersPan(self):
        ui = Ui_DataImport()
        self.parametersPanel = ui
        
        FlightPlanBaseSimpleDlg.initParametersPan(self)
#         self.parametersPanel.txtName.setEnabled(False)
        self.parametersPanel.groupBox.setVisible(False)
        self.parametersPanel.tableView.setSelectionBehavior(1)
        
        self.parametersPanel.cmbAlUnit.addItems(["Meter", "Feet"])
#         self.parametersPanel.frame.hide()
        self.parametersPanel.btnFile.clicked.connect(self.btnFile_Click)
        self.parametersPanel.cmbType.currentIndexChanged.connect(self.cmbTypeIndexChanged)
        self.parametersPanel.tree.clicked.connect(self.treeClicked)
        self.parametersPanel.tableView.clicked.connect(self.tableViewClicked)
        self.parametersPanel.tableViewDetail.clicked.connect(self.tableViewDetailClicked)
        self.parametersPanel.txtName.textChanged.connect(self.txtNameChaned)
        self.parametersPanel.tableView.verticalHeader().sectionClicked.connect(self.tableViewHeaderClick)

        self.parametersPanel.btnProcAdd.clicked.connect(self.btnProcAdd_clicked)
        self.parametersPanel.btnProcEdit.clicked.connect(self.btnProcEdit_clicked)
        self.parametersPanel.btnDetailAdd.clicked.connect(self.btnDetailAdd_clicked)
        self.parametersPanel.btnDetailEdit.clicked.connect(self.btnDetailEdit_clicked)
        self.parametersPanel.btnProcRemove.clicked.connect(self.btnProcRemove_clicked)
        self.parametersPanel.btnDetailRemove.clicked.connect(self.btnDetailRemove_clicked)
    def btnProcRemove_clicked(self):
        if self.selectedRow == None:
            return
        self.sortFilterProxyModel.removeRow(self.selectedRowSortModel)
        self.standardItemModel.removeRow(self.selectedRow)
        self.standardItemModelDetail.clear()


        if self.selectedItem != None and self.selectedItem.text() == Captions.AIRSPACE:
            self.aixm.pointDataAirspace.pop(self.selectedRow)
            for i in range(self.standardItemModel.rowCount()):
                rowVal = int(self.standardItemModel.item(i, 5).text())
                if rowVal > self.selectedRow:
                    self.standardItemModel.setItem(i, 5, QStandardItem(str(rowVal - 1)))
        elif self.selectedItem != None and self.selectedItem.text() == Captions.GEOGRAPHICAL_BORDER:
            self.aixm.pointDataBorder.pop(self.selectedRow)
            for i in range(self.standardItemModel.rowCount()):
                rowVal = int(self.standardItemModel.item(i, 3).text())
                if rowVal > self.selectedRow:
                    self.standardItemModel.setItem(i, 3, QStandardItem(str(rowVal - 1)))
        elif self.selectedItem != None and self.selectedItem.text() == Captions.ROUTES:
            self.aixm.pointDataRoutes.pop(self.selectedRow)
            for i in range(self.standardItemModel.rowCount()):
                rowVal = int(self.standardItemModel.item(i, 2).text())
                if rowVal > self.selectedRow:
                    self.standardItemModel.setItem(i, 2, QStandardItem(str(rowVal - 1)))
        elif self.selectedItem != None and self.selectedItem.text() == Captions.SYMBOLS:
            selectedNode = self.aixm.pointData[self.selectedRow][9]
            self.aixm.pointData.pop(self.selectedRow)

        elif self.selectedItem != None and self.selectedItem.text() == Captions.OBSTACLES:
            self.aixm.pointDataObstacles.pop(self.selectedRow)

        c= 1

    def btnDetailRemove_clicked(self):
        if self.selectedDetailRow == None:
            return
        self.standardItemModelDetail.removeRow(self.selectedDetailRow)
        if self.selectedItem != None and self.selectedItem.text() == Captions.AIRSPACE:
            self.aixm.pointDataAirspace[self.selectedRow][6].pop(self.selectedDetailRow)
            changedVerticsCount = int(self.standardItemModel.item(self.selectedRow, 4).text()) - 1
            self.standardItemModel.setItem(self.selectedRow, 4, QStandardItem(str(changedVerticsCount)))
        elif self.selectedItem != None and self.selectedItem.text() == Captions.GEOGRAPHICAL_BORDER:
            self.aixm.pointDataBorder[self.selectedRow][2].pop(self.selectedDetailRow)
            changedVerticsCount = int(self.standardItemModel.item(self.selectedRow, 2).text()) - 1
            self.standardItemModel.setItem(self.selectedRow, 2, QStandardItem(str(changedVerticsCount)))
        elif self.selectedItem != None and self.selectedItem.text() == Captions.ROUTES:
            self.aixm.pointDataRoutes[self.selectedRow][1].pop(self.selectedDetailRow)
            changedVerticsCount = int(self.standardItemModel.item(self.selectedRow, 1).text()) - 1
            self.standardItemModel.setItem(self.selectedRow, 1, QStandardItem(str(changedVerticsCount)))

    def btnDetailEdit_clicked(self):
        if self.selectedItem != None and self.selectedItem.text() == Captions.AIRSPACE and self.selectedDetailRow != None:
            dataList = [self.standardItemModelDetail.item(self.selectedDetailRow, 2).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 2) != None else "",
                        self.standardItemModelDetail.item(self.selectedDetailRow, 3).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 3) != None else "",
                        self.standardItemModelDetail.item(self.selectedDetailRow, 4).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 4) != None else "",
                        self.standardItemModelDetail.item(self.selectedDetailRow, 5).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 5) != None else "",
                        self.standardItemModelDetail.item(self.selectedDetailRow, 6).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 6) != None else "",
                        self.standardItemModelDetail.item(self.selectedDetailRow, 7).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 7) != None else ""]
            self.addDataDlg = DlgDetailDataEdit(self, "Modify Detail Airspace", dataList)
            self.addDataDlg.accepted.connect(self.editDetailData)
            self.addDataDlg.show()
        elif self.selectedItem != None and self.selectedItem.text() == Captions.GEOGRAPHICAL_BORDER and self.selectedDetailRow != None:
            dataList = [self.standardItemModelDetail.item(self.selectedDetailRow, 2).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 2) != None else "",
                        self.standardItemModelDetail.item(self.selectedDetailRow, 3).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 3) != None else "",
                        self.standardItemModelDetail.item(self.selectedDetailRow, 4).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 4) != None else "",
                        self.standardItemModelDetail.item(self.selectedDetailRow, 5).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 5) != None else ""]
            self.addDataDlg = DlgDetailDataEdit(self, "Modify Detail Geographical Border", dataList)
            self.addDataDlg.accepted.connect(self.editDetailData)
            self.addDataDlg.show()
        elif self.selectedItem != None and self.selectedItem.text() == Captions.ROUTES and self.selectedDetailRow != None:
            dataList = [self.standardItemModelDetail.item(self.selectedDetailRow, 2).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 2) != None else "",
                        self.standardItemModelDetail.item(self.selectedDetailRow, 3).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 3) != None else "",
                        self.standardItemModelDetail.item(self.selectedDetailRow, 4).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 4) != None else "",
                        self.standardItemModelDetail.item(self.selectedDetailRow, 5).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 5) != None else "",
                        self.standardItemModelDetail.item(self.selectedDetailRow, 6).text() if self.standardItemModelDetail.item(self.selectedDetailRow, 6) != None else ""]
            self.addDataDlg = DlgDetailDataEdit(self, "Modify Detail Routes", dataList)
            self.addDataDlg.accepted.connect(self.editDetailData)
            self.addDataDlg.show()

    def editDetailData(self):
        if self.addDataDlg.latitude == "":
            return
        if self.selectedItem != None and self.selectedItem.text() == Captions.AIRSPACE and self.selectedRow != None:
            newDataBaseCoordinate = self.aixm.pointDataAirspace[self.selectedRow][6][self.selectedDetailRow]
            # newDataBaseCoordinate = DataBaseCoordinate()
            newDataBaseCoordinate.x = float(self.addDataDlg.x)
            newDataBaseCoordinate.y = float(self.addDataDlg.y)
            newDataBaseCoordinate.latitude = Degrees(float(self.addDataDlg.latitude), None, None, DegreesType.Latitude)
            newDataBaseCoordinate.longitude = Degrees(float(self.addDataDlg.longitude), None, None, DegreesType.Longitude)
            if self.addDataDlg.altitude == "":
                newDataBaseCoordinate.altitude = Altitude.NaN()
            else:
                newDataBaseCoordinate.altitude = Altitude(float(self.addDataDlg.altitude))
            newDataBaseCoordinate.type = self.addDataDlg.type
            if self.addDataDlg.cenLatitude != "":
                newDataBaseCoordinate.centerLatitude = Degrees(float(self.addDataDlg.cenLatitude), None, None, DegreesType.Latitude)
                newDataBaseCoordinate.centerLongitude = Degrees(float(self.addDataDlg.cenLongitude), None, None, DegreesType.Longitude)
            # dataBaseCoordinates.append(newDataBaseCoordinate)

            self.standardItemModelDetail.setItem(self.selectedDetailRow, 0, QStandardItem(self.addDataDlg.x))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 1, QStandardItem(self.addDataDlg.y))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 2, QStandardItem(self.addDataDlg.latitude))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 3, QStandardItem(self.addDataDlg.longitude))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 4, QStandardItem(self.addDataDlg.altitude))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 5, QStandardItem(self.addDataDlg.type))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 6, QStandardItem(self.addDataDlg.cenLatitude))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 7, QStandardItem(self.addDataDlg.cenLongitude))
            # changedVerticsCount = int(self.standardItemModel.item(self.selectedRow, 4).text()) + 1
            # self.standardItemModel.setItem(self.selectedRow, 4, QStandardItem(str(changedVerticsCount)))

            # self.aixm.pointDataAirspace.append([dlg.name, dlg.lowerLimit, dlg.upperLimit, dlg.radius, "False", "False", DataBaseCoordinates("Vertices"), "", None])
        elif self.selectedItem != None and self.selectedItem.text() == Captions.GEOGRAPHICAL_BORDER and self.selectedRow != None:
            newDataBaseCoordinate = self.aixm.pointDataBorder[self.selectedRow][2][self.selectedDetailRow]
            # newDataBaseCoordinate = DataBaseCoordinate()
            newDataBaseCoordinate.x = float(self.addDataDlg.x)
            newDataBaseCoordinate.y = float(self.addDataDlg.y)
            newDataBaseCoordinate.latitude = Degrees(float(self.addDataDlg.latitude), None, None, DegreesType.Latitude)
            newDataBaseCoordinate.longitude = Degrees(float(self.addDataDlg.longitude), None, None, DegreesType.Longitude)
            if self.addDataDlg.altitude == "":
                newDataBaseCoordinate.altitude = Altitude.NaN()
            else:
                newDataBaseCoordinate.altitude = Altitude(float(self.addDataDlg.altitude))
            newDataBaseCoordinate.type = self.addDataDlg.type
            # dataBaseCoordinates.append(newDataBaseCoordinate)

            count = self.standardItemModelDetail.rowCount()
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 0, QStandardItem(self.addDataDlg.x))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 1, QStandardItem(self.addDataDlg.y))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 2, QStandardItem(self.addDataDlg.latitude))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 3, QStandardItem(self.addDataDlg.longitude))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 4, QStandardItem(self.addDataDlg.altitude))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 5, QStandardItem(self.addDataDlg.type))
            # changedVerticsCount = int(self.standardItemModel.item(self.selectedRow, 2).text()) + 1
            # self.standardItemModel.setItem(self.selectedRow, 2, QStandardItem(str(changedVerticsCount)))
        elif self.selectedItem != None and self.selectedItem.text() == Captions.ROUTES and self.selectedRow != None:
            newDataBaseCoordinate = self.aixm.pointDataRoutes[self.selectedRow][1][self.selectedDetailRow]
            # newDataBaseCoordinate = DataBaseCoordinate()
            newDataBaseCoordinate.x = float(self.addDataDlg.x)
            newDataBaseCoordinate.y = float(self.addDataDlg.y)
            newDataBaseCoordinate.latitude = Degrees(float(self.addDataDlg.latitude), None, None, DegreesType.Latitude)
            newDataBaseCoordinate.longitude = Degrees(float(self.addDataDlg.longitude), None, None, DegreesType.Longitude)
            if self.addDataDlg.altitude == "":
                newDataBaseCoordinate.altitude = Altitude.NaN()
            else:
                newDataBaseCoordinate.altitude = Altitude(float(self.addDataDlg.altitude))
            newDataBaseCoordinate.type = self.addDataDlg.type
            if self.addDataDlg.magVariation != "":
                newDataBaseCoordinate.variation = float(self.addDataDlg.magVariation)
            # dataBaseCoordinates.append(newDataBaseCoordinate)

            count = self.standardItemModelDetail.rowCount()
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 0, QStandardItem(self.addDataDlg.x))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 1, QStandardItem(self.addDataDlg.y))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 2, QStandardItem(self.addDataDlg.latitude))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 3, QStandardItem(self.addDataDlg.longitude))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 4, QStandardItem(self.addDataDlg.altitude))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 5, QStandardItem(self.addDataDlg.type))
            self.standardItemModelDetail.setItem(self.selectedDetailRow, 6, QStandardItem(self.addDataDlg.magVariation))
            # changedVerticsCount = int(self.standardItemModel.item(self.selectedRow, 1).text()) + 1
            # self.standardItemModel.setItem(self.selectedRow, 1, QStandardItem(str(changedVerticsCount)))


    def btnDetailAdd_clicked(self):
        if self.selectedItem != None and self.selectedItem.text() == Captions.AIRSPACE and self.selectedRow != None:
            self.addDataDlg = DlgDetailDataEdit(self, "Add Detail Airspace")
            self.addDataDlg.accepted.connect(self.addDetailData)
            self.addDataDlg.show()
        elif self.selectedItem != None and self.selectedItem.text() == Captions.GEOGRAPHICAL_BORDER and self.selectedRow != None:
            self.addDataDlg = DlgDetailDataEdit(self, "Add Detail Geographical Border")
            self.addDataDlg.accepted.connect(self.addDetailData)
            self.addDataDlg.show()
        elif self.selectedItem != None and self.selectedItem.text() == Captions.ROUTES and self.selectedRow != None:
            self.addDataDlg = DlgDetailDataEdit(self, "Add Detail Routes")
            self.addDataDlg.accepted.connect(self.addDetailData)
            self.addDataDlg.show()
    def addDetailData(self):
        if self.addDataDlg.latitude == "":
            return
        if self.selectedItem != None and self.selectedItem.text() == Captions.AIRSPACE and self.selectedRow != None:
            dataBaseCoordinates = self.aixm.pointDataAirspace[self.selectedRow][6]
            newDataBaseCoordinate = DataBaseCoordinate()
            newDataBaseCoordinate.x = float(self.addDataDlg.x)
            newDataBaseCoordinate.y = float(self.addDataDlg.y)
            newDataBaseCoordinate.latitude = Degrees(float(self.addDataDlg.latitude), None, None, DegreesType.Latitude)
            newDataBaseCoordinate.longitude = Degrees(float(self.addDataDlg.longitude), None, None, DegreesType.Longitude)
            if self.addDataDlg.altitude == "":
                newDataBaseCoordinate.altitude = Altitude.NaN()
            else:
                newDataBaseCoordinate.altitude = Altitude(float(self.addDataDlg.altitude))
            newDataBaseCoordinate.type = self.addDataDlg.type
            if self.addDataDlg.cenLatitude != "":
                newDataBaseCoordinate.centerLatitude = Degrees(float(self.addDataDlg.cenLatitude), None, None, DegreesType.Latitude)
                newDataBaseCoordinate.centerLongitude = Degrees(float(self.addDataDlg.cenLongitude), None, None, DegreesType.Longitude)
            dataBaseCoordinates.append(newDataBaseCoordinate)

            count = self.standardItemModelDetail.rowCount()
            self.standardItemModelDetail.setItem(count, 0, QStandardItem(self.addDataDlg.x))
            self.standardItemModelDetail.setItem(count, 1, QStandardItem(self.addDataDlg.y))
            self.standardItemModelDetail.setItem(count, 2, QStandardItem(self.addDataDlg.latitude))
            self.standardItemModelDetail.setItem(count, 3, QStandardItem(self.addDataDlg.longitude))
            self.standardItemModelDetail.setItem(count, 4, QStandardItem(self.addDataDlg.altitude))
            self.standardItemModelDetail.setItem(count, 5, QStandardItem(self.addDataDlg.type))
            self.standardItemModelDetail.setItem(count, 6, QStandardItem(self.addDataDlg.cenLatitude))
            self.standardItemModelDetail.setItem(count, 7, QStandardItem(self.addDataDlg.cenLongitude))
            changedVerticsCount = int(self.standardItemModel.item(self.selectedRow, 4).text()) + 1
            self.standardItemModel.setItem(self.selectedRow, 4, QStandardItem(str(changedVerticsCount)))

            # self.aixm.pointDataAirspace.append([dlg.name, dlg.lowerLimit, dlg.upperLimit, dlg.radius, "False", "False", DataBaseCoordinates("Vertices"), "", None])
        elif self.selectedItem != None and self.selectedItem.text() == Captions.GEOGRAPHICAL_BORDER and self.selectedRow != None:
            dataBaseCoordinates = self.aixm.pointDataBorder[self.selectedRow][2]
            newDataBaseCoordinate = DataBaseCoordinate()
            newDataBaseCoordinate.x = float(self.addDataDlg.x)
            newDataBaseCoordinate.y = float(self.addDataDlg.y)
            newDataBaseCoordinate.latitude = Degrees(float(self.addDataDlg.latitude), None, None, DegreesType.Latitude)
            newDataBaseCoordinate.longitude = Degrees(float(self.addDataDlg.longitude), None, None, DegreesType.Longitude)
            if self.addDataDlg.altitude == "":
                newDataBaseCoordinate.altitude = Altitude.NaN()
            else:
                newDataBaseCoordinate.altitude = Altitude(float(self.addDataDlg.altitude))
            newDataBaseCoordinate.type = self.addDataDlg.type
            dataBaseCoordinates.append(newDataBaseCoordinate)

            count = self.standardItemModelDetail.rowCount()
            self.standardItemModelDetail.setItem(count, 0, QStandardItem(self.addDataDlg.x))
            self.standardItemModelDetail.setItem(count, 1, QStandardItem(self.addDataDlg.y))
            self.standardItemModelDetail.setItem(count, 2, QStandardItem(self.addDataDlg.latitude))
            self.standardItemModelDetail.setItem(count, 3, QStandardItem(self.addDataDlg.longitude))
            self.standardItemModelDetail.setItem(count, 4, QStandardItem(self.addDataDlg.altitude))
            self.standardItemModelDetail.setItem(count, 5, QStandardItem(self.addDataDlg.type))
            changedVerticsCount = int(self.standardItemModel.item(self.selectedRow, 2).text()) + 1
            self.standardItemModel.setItem(self.selectedRow, 2, QStandardItem(str(changedVerticsCount)))
        elif self.selectedItem != None and self.selectedItem.text() == Captions.ROUTES and self.selectedRow != None:
            dataBaseCoordinates = self.aixm.pointDataRoutes[self.selectedRow][1]
            newDataBaseCoordinate = DataBaseCoordinate()
            newDataBaseCoordinate.x = float(self.addDataDlg.x)
            newDataBaseCoordinate.y = float(self.addDataDlg.y)
            newDataBaseCoordinate.latitude = Degrees(float(self.addDataDlg.latitude), None, None, DegreesType.Latitude)
            newDataBaseCoordinate.longitude = Degrees(float(self.addDataDlg.longitude), None, None, DegreesType.Longitude)
            if self.addDataDlg.altitude == "":
                newDataBaseCoordinate.altitude = Altitude.NaN()
            else:
                newDataBaseCoordinate.altitude = Altitude(float(self.addDataDlg.altitude))
            newDataBaseCoordinate.type = self.addDataDlg.type
            if self.addDataDlg.magVariation != "":
                newDataBaseCoordinate.variation = float(self.addDataDlg.magVariation)
            dataBaseCoordinates.append(newDataBaseCoordinate)

            count = self.standardItemModelDetail.rowCount()
            self.standardItemModelDetail.setItem(count, 0, QStandardItem(self.addDataDlg.x))
            self.standardItemModelDetail.setItem(count, 1, QStandardItem(self.addDataDlg.y))
            self.standardItemModelDetail.setItem(count, 2, QStandardItem(self.addDataDlg.latitude))
            self.standardItemModelDetail.setItem(count, 3, QStandardItem(self.addDataDlg.longitude))
            self.standardItemModelDetail.setItem(count, 4, QStandardItem(self.addDataDlg.altitude))
            self.standardItemModelDetail.setItem(count, 5, QStandardItem(self.addDataDlg.type))
            self.standardItemModelDetail.setItem(count, 6, QStandardItem(self.addDataDlg.magVariation))
            changedVerticsCount = int(self.standardItemModel.item(self.selectedRow, 1).text()) + 1
            self.standardItemModel.setItem(self.selectedRow, 1, QStandardItem(str(changedVerticsCount)))
    def btnProcEdit_clicked(self):
        if self.selectedItem != None and self.selectedItem.text() == Captions.OBSTACLES:
            dataList = [self.standardItemModel.item(self.selectedRow, 0).text() if self.standardItemModel.item(self.selectedRow, 0) != None else "",
                        self.standardItemModel.item(self.selectedRow, 1).text() if self.standardItemModel.item(self.selectedRow, 1) != None else "",
                        self.standardItemModel.item(self.selectedRow, 2).text() if self.standardItemModel.item(self.selectedRow, 2) != None else "",
                        self.standardItemModel.item(self.selectedRow, 3).text() if self.standardItemModel.item(self.selectedRow, 3) != None else "",
                        self.standardItemModel.item(self.selectedRow, 4).text() if self.standardItemModel.item(self.selectedRow, 4) != None else "",
                        self.standardItemModel.item(self.selectedRow, 5).text() if self.standardItemModel.item(self.selectedRow, 5) != None else ""]
            self.addDataDlg = DlgPointDataEdit(self, "Modify Obstacle", dataList)
            self.addDataDlg.accepted.connect(self.addPointData)
            self.addDataDlg.show()
        elif self.selectedItem != None and self.selectedItem.text() == Captions.SYMBOLS:
            dataList = [self.standardItemModel.item(self.selectedRow, 0).text() if self.standardItemModel.item(self.selectedRow, 0) != None else "",
                        self.standardItemModel.item(self.selectedRow, 1).text() if self.standardItemModel.item(self.selectedRow, 1) != None else "",
                        self.standardItemModel.item(self.selectedRow, 2).text() if self.standardItemModel.item(self.selectedRow, 2) != None else "",
                        self.standardItemModel.item(self.selectedRow, 3).text() if self.standardItemModel.item(self.selectedRow, 3) != None else "",
                        self.standardItemModel.item(self.selectedRow, 4).text() if self.standardItemModel.item(self.selectedRow, 4) != None else "",
                        self.standardItemModel.item(self.selectedRow, 5).text() if self.standardItemModel.item(self.selectedRow, 5) != None else ""]
            self.addDataDlg = DlgPointDataEdit(self, "Modify Symbol", dataList)
            self.addDataDlg.accepted.connect(self.addPointData)
            self.addDataDlg.show()
        elif self.selectedItem != None and self.selectedItem.text() == Captions.AIRSPACE:
            dataList = [self.standardItemModel.item(self.selectedRow, 0).text() if self.standardItemModel.item(self.selectedRow, 0) != None else "",
                        self.standardItemModel.item(self.selectedRow, 1).text() if self.standardItemModel.item(self.selectedRow, 1) != None else "",
                        self.standardItemModel.item(self.selectedRow, 2).text() if self.standardItemModel.item(self.selectedRow, 2) != None else "",
                        self.standardItemModel.item(self.selectedRow, 3).text() if self.standardItemModel.item(self.selectedRow, 3) != None else ""]
            dlg = DlgAirspaceDataEdit(self, "Modify Airspace", dataList)
            if dlg.exec_() == True:
                self.standardItemModel.setItem(self.selectedRow, 0, QStandardItem(dlg.name))
                self.standardItemModel.setItem(self.selectedRow, 1, QStandardItem(dlg.lowerLimit))
                self.standardItemModel.setItem(self.selectedRow, 2, QStandardItem(dlg.upperLimit))
                self.standardItemModel.setItem(self.selectedRow, 3, QStandardItem(dlg.radius))
                self.aixm.pointDataAirspace[self.selectedRow].__setitem__(0, dlg.name)
                self.aixm.pointDataAirspace[self.selectedRow].__setitem__(1, dlg.lowerLimit)
                self.aixm.pointDataAirspace[self.selectedRow].__setitem__(2, dlg.upperLimit)
                self.aixm.pointDataAirspace[self.selectedRow].__setitem__(3, dlg.radius)
            pass
        elif self.selectedItem != None and self.selectedItem.text() == Captions.GEOGRAPHICAL_BORDER:
            dataList = [self.standardItemModel.item(self.selectedRow, 0).text() if self.standardItemModel.item(self.selectedRow, 0) != None else "",
                        self.standardItemModel.item(self.selectedRow, 1).text() if self.standardItemModel.item(self.selectedRow, 1) != None else ""]
            dlg = DlgGeoBorderDataEdit(self, "Modify " + Captions.GEOGRAPHICAL_BORDER, dataList)
            if dlg.exec_() == True:
                self.standardItemModel.setItem(self.selectedRow, 0, QStandardItem(dlg.name))
                self.standardItemModel.setItem(self.selectedRow, 1, QStandardItem(dlg.type))
                self.aixm.pointDataBorder[self.selectedRow].__setitem__(0, dlg.name)
                self.aixm.pointDataBorder[self.selectedRow].__setitem__(1, dlg.type)
                existing = False
                for i in range(self.parametersPanel.cmbType.count()):
                    if dlg.type == self.parametersPanel.cmbType.itemText(i):
                        existing = True
                        break
                if not existing:
                    self.parametersPanel.cmbType.addItem(dlg.type)
                    pass
            pass
        elif self.selectedItem != None and self.selectedItem.text() == Captions.ROUTES:
            dataList = [self.standardItemModel.item(self.selectedRow, 0).text() if self.standardItemModel.item(self.selectedRow, 0) != None else ""]
            dlg = DlgRouteDataEdit(self, "Modify " + Captions.ROUTES, dataList)
            if dlg.exec_() == True:
                count = self.standardItemModel.rowCount()
                self.standardItemModel.setItem(self.selectedRow, 0, QStandardItem(dlg.name))
            pass
    def btnProcAdd_clicked(self):
        if self.selectedItem != None and self.selectedItem.text() == Captions.AIRSPACE:
            dlg = DlgAirspaceDataEdit(self, "Add Airspace")
            if dlg.exec_() == True:
                count = self.standardItemModel.rowCount()
                self.standardItemModel.setItem(count, 0, QStandardItem(dlg.name))
                self.standardItemModel.setItem(count, 1, QStandardItem(dlg.lowerLimit))
                self.standardItemModel.setItem(count, 2, QStandardItem(dlg.upperLimit))
                self.standardItemModel.setItem(count, 3, QStandardItem(dlg.radius))
                self.standardItemModel.setItem(count, 4, QStandardItem("0"))
                self.standardItemModel.setItem(count, 5, QStandardItem(str(count)))
                self.aixm.pointDataAirspace.append([dlg.name, dlg.lowerLimit, dlg.upperLimit, dlg.radius, "False", "False", DataBaseCoordinates("Vertices"), "", None])


        elif self.selectedItem != None and self.selectedItem.text() == Captions.OBSTACLES:
            self.addDataDlg = DlgPointDataEdit(self, "Add Obstacle")
            self.addDataDlg.accepted.connect(self.addPointData)
            self.addDataDlg.show()
        elif self.selectedItem != None and self.selectedItem.text() == Captions.SYMBOLS:
            self.addDataDlg = DlgPointDataEdit(self, "Add Symbol")
            self.addDataDlg.accepted.connect(self.addPointData)
            self.addDataDlg.show()
        elif self.selectedItem != None and self.selectedItem.text() == Captions.GEOGRAPHICAL_BORDER:
            dlg = DlgGeoBorderDataEdit(self, "Add " + Captions.GEOGRAPHICAL_BORDER)
            if dlg.exec_() == True:
                count = self.standardItemModel.rowCount()
                self.standardItemModel.setItem(count, 0, QStandardItem(dlg.name))
                self.standardItemModel.setItem(count, 1, QStandardItem(dlg.type))
                self.standardItemModel.setItem(count, 2, QStandardItem(str(0)))
                self.standardItemModel.setItem(count, 3, QStandardItem(str(count)))
                self.aixm.pointDataBorder.append([dlg.name, dlg.type, DataBaseCoordinates("Vertices"), "", None])

                existing = False
                for i in range(self.parametersPanel.cmbType.count()):
                    if dlg.type == self.parametersPanel.cmbType.itemText(i):
                        existing = True
                        break
                if not existing:
                    self.parametersPanel.cmbType.addItem(dlg.type)
                    pass
            pass
        elif self.selectedItem != None and self.selectedItem.text() == Captions.ROUTES:
            dlg = DlgRouteDataEdit(self, "Add " + Captions.ROUTES)
            if dlg.exec_() == True:
                count = self.standardItemModel.rowCount()
                self.standardItemModel.setItem(count, 0, QStandardItem(dlg.name))
                self.standardItemModel.setItem(count, 1, QStandardItem(str(0)))
                self.standardItemModel.setItem(count, 2, QStandardItem(str(count)))
                self.aixm.pointDataRoutes.append([dlg.name, DataBaseCoordinates("Segments"), "", None])
            pass
    def addPointData(self):
        row = None
        if not self.addDataDlg.editingFlag:
            row = self.standardItemModel.rowCount()

        else:
            row = self.selectedRow

        existing = False
        for i in range(self.parametersPanel.cmbType.count()):
            if self.addDataDlg.type == self.parametersPanel.cmbType.itemText(i):
                existing = True
                break
        if not existing:
            self.parametersPanel.cmbType.addItem(self.addDataDlg.type)

        self.standardItemModel.setItem(row, 0, QStandardItem(self.addDataDlg.name))
        self.standardItemModel.setItem(row, 1, QStandardItem(self.addDataDlg.latitude))
        self.standardItemModel.setItem(row, 2, QStandardItem(self.addDataDlg.longitude))
        self.standardItemModel.setItem(row, 3, QStandardItem(self.addDataDlg.altitude))
        self.standardItemModel.setItem(row, 4, QStandardItem(self.addDataDlg.type))
        self.standardItemModel.setItem(row, 5, QStandardItem(self.addDataDlg.remarks))
        self.standardItemModel.setItem(row, 6, QStandardItem(str(row)))

        title = self.addDataDlg.windowTitle()

        if title.contains("Add"):
            if title.contains("Symbol"):
                self.aixm.pointData.append([self.addDataDlg.name, "", "", float(self.addDataDlg.latitude), float(self.addDataDlg.longitude), self.addDataDlg.altitude, self.addDataDlg.remarks, self.addDataDlg.type, "", None])
            else:
                self.aixm.pointDataObstacles.append([self.addDataDlg.name, "", "", float(self.addDataDlg.latitude), float(self.addDataDlg.longitude), self.addDataDlg.altitude, self.addDataDlg.remarks, self.addDataDlg.type, "", None])
        else:
            if title.contains("Symbol"):
                self.aixm.pointData.pop(self.selectedRow)
                self.aixm.pointData.insert(self.selectedRow, [self.addDataDlg.name, "", "", float(self.addDataDlg.latitude), float(self.addDataDlg.longitude), self.addDataDlg.altitude, self.addDataDlg.remarks, self.addDataDlg.type, "", None])
            else:
                self.aixm.pointDataObstacles.pop(self.selectedRow)
                self.aixm.pointDataObstacles.insert(self.selectedRow, [self.addDataDlg.name, "", "", float(self.addDataDlg.latitude), float(self.addDataDlg.longitude), self.addDataDlg.altitude, self.addDataDlg.remarks, self.addDataDlg.type, "", None])
    def tableViewHeaderClick(self):
        self.setVerticalHeader()
    def txtNameChaned(self):
        textStr = self.parametersPanel.txtName.text()
#         if textStr == "":
#             return
#         if not self.parametersPanel.cmbType.currentIndex() > 0:
#             rowCount0 = self.standardItemModel.rowCount()
#             colCount = self.standardItemModel.columnCount()
#             if rowCount0 > 0:
#                 for i in range(rowCount0):
#                     itemStr = self.standardItemModel.item(i).text() 
#                     
#                     if itemStr.count(textStr) > 0:                    
#                         item = self.standardItemModel.setItem(i, colCount - 1, QStandardItem(textStr)) 
#                     else:
#                         item = self.standardItemModel.setItem(i, colCount - 1, QStandardItem(itemStr))
#                 self.sortFilterProxyModel.setFilterKeyColumn(colCount - 1)
#                 self.setFilterFixedString(self.parametersPanel.txtName.text())
#         else:
#             rowCount0 = self.abstructModel.rowCount()
#             colCount = self.abstructModel.columnCount()
#             if rowCount0 > 0:
#                 for i in range(rowCount0):
#                     itemStr = self.abstructModel.item(i).text() 
#                     
#                     if itemStr.count(textStr) > 0:                    
#                         item = self.abstructModel.setItem(i, colCount - 1, QStandardItem(textStr)) 
#                     else:
#                         item = self.abstructModel.setItem(i, colCount - 1, QStandardItem(itemStr))
        self.sortFilterProxyModel.setFilterKeyColumn(0)
        self.setFilterFixedString(self.parametersPanel.txtName.text())
        self.setVerticalHeader()
    def tableViewDetailClicked(self, modelIndex):
        if self.standardItemModelDetail.rowCount() > 0 and self.selectedItem != None and self.selectedRow != None:
            self.selectedDetailRow = modelIndex.row()

    def tableViewClicked(self, modelIndex):
        self.selectedRowSortModel = modelIndex.row()
        progressMessageBar = define._messagBar.createMessage("Displaying detail data...")
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(self.progress)
        define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
        # pointDataCount = self.standardItemModel.rowCount()

        # self.progress.setMaximum(self.standardItemModel.rowCount())

#         self.parametersPanel.tableView.setSortingEnabled(True)
#         modelIndex = self.parametersPanel.tableView.rootIndex()
        if self.standardItemModel.rowCount() > 0 and self.selectedItem != None and self.selectedItem.text() == Captions.AIRSPACE:
            data = self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(modelIndex.row(), 5)).toInt()
            rowIndex = data[0]
            self.selectedRow = rowIndex
            dataBaseCoordinates = self.aixm.pointDataAirspace[rowIndex][6]
            self.standardItemModelDetail.clear()
            self.standardItemModelDetail.setHorizontalHeaderLabels(self.airspaceDetailColumnLabels)
            i = 0
            self.progress.setMaximum(len(dataBaseCoordinates))
#             print rowIndex, len(dataBaseCoordinates)
            for dataBaseCoordinate in dataBaseCoordinates:
                if dataBaseCoordinate.x == None:
                    self.standardItemModelDetail.setItem(i, 0, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 0, QStandardItem(str(dataBaseCoordinate.x)))
                if dataBaseCoordinate.y == None:
                    self.standardItemModelDetail.setItem(i, 1, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 1, QStandardItem(str(dataBaseCoordinate.y)))

                if dataBaseCoordinate.x != None and dataBaseCoordinate.y != None:
                    pointDegree = QgisHelper.Meter2Degree(dataBaseCoordinate.x, dataBaseCoordinate.y)
                    self.standardItemModelDetail.setItem(i, 2, QStandardItem(str(pointDegree.get_Y())))
                    self.standardItemModelDetail.setItem(i, 3, QStandardItem(str(pointDegree.get_X())))
                else:
                    if dataBaseCoordinate.latitude == None:
                        self.standardItemModelDetail.setItem(i, 2, QStandardItem(""))
                    else:
                        self.standardItemModelDetail.setItem(i, 2, QStandardItem(str(dataBaseCoordinate.latitude.value)))
                    if dataBaseCoordinate.longitude == None:
                        self.standardItemModelDetail.setItem(i, 3, QStandardItem(""))
                    else:
                        self.standardItemModelDetail.setItem(i, 3, QStandardItem(str(dataBaseCoordinate.longitude.value)))
                    if dataBaseCoordinate.latitude != None and dataBaseCoordinate.longitude != None:
                        pointMeter = QgisHelper.Degree2Meter(dataBaseCoordinate.longitude.value , dataBaseCoordinate.latitude.value)
                        self.standardItemModelDetail.setItem(i, 0, QStandardItem(str(pointMeter.get_X())))
                        self.standardItemModelDetail.setItem(i, 1, QStandardItem(str(pointMeter.get_Y())))

                if dataBaseCoordinate.altitude == None or dataBaseCoordinate.altitude.Metres == None:
                    self.standardItemModelDetail.setItem(i, 4, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 4, QStandardItem(str(dataBaseCoordinate.altitude.Metres)))
                if dataBaseCoordinate.type == None:
                    self.standardItemModelDetail.setItem(i, 5, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 5, QStandardItem(str(dataBaseCoordinate.type)))
                if dataBaseCoordinate.centerLatitude == None:
                    self.standardItemModelDetail.setItem(i, 6, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 6, QStandardItem(str(dataBaseCoordinate.centerLatitude.value)))
                if dataBaseCoordinate.centerLongitude == None:
                    self.standardItemModelDetail.setItem(i, 7, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 7, QStandardItem(str(dataBaseCoordinate.centerLongitude.value)))
                i += 1
                self.progress.setValue(i)
                QApplication.processEvents()
                
        if self.standardItemModel.rowCount() > 0 and self.selectedItem != None and self.selectedItem.text() == Captions.GEOGRAPHICAL_BORDER:
#             rowIndex = int(self.standardItemModel.item(modelIndex.row(), 5).text())
            data = self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(modelIndex.row(), 3)).toInt()
            rowIndex = data[0]
            self.selectedRow = rowIndex
            dataBaseCoordinates = self.aixm.pointDataBorder[rowIndex][2]
            
#             dataBaseCoordinates = self.aixm.pointDataBorder[modelIndex.row()][2]
            self.standardItemModelDetail.clear()
            self.standardItemModelDetail.setHorizontalHeaderLabels(self.borderDetailColumnLabels)
            i = 0
            self.progress.setMaximum(len(dataBaseCoordinates))
#             print rowIndex, len(dataBaseCoordinates)
            for dataBaseCoordinate in dataBaseCoordinates:
                if dataBaseCoordinate.x == None:
                    self.standardItemModelDetail.setItem(i, 0, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 0, QStandardItem(str(dataBaseCoordinate.x)))
                if dataBaseCoordinate.y == None:
                    self.standardItemModelDetail.setItem(i, 1, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 1, QStandardItem(str(dataBaseCoordinate.y)))

                if dataBaseCoordinate.x != None and dataBaseCoordinate.y != None:
                    pointDegree = QgisHelper.Meter2Degree(dataBaseCoordinate.x, dataBaseCoordinate.y)
                    self.standardItemModelDetail.setItem(i, 2, QStandardItem(str(pointDegree.get_Y())))
                    self.standardItemModelDetail.setItem(i, 3, QStandardItem(str(pointDegree.get_X())))
                else:

                    if dataBaseCoordinate.latitude == None:
                        self.standardItemModelDetail.setItem(i, 2, QStandardItem(""))
                    else:
                        self.standardItemModelDetail.setItem(i, 2, QStandardItem(str(dataBaseCoordinate.latitude.value)))
                    if dataBaseCoordinate.longitude == None:
                        self.standardItemModelDetail.setItem(i, 3, QStandardItem(""))
                    else:
                        self.standardItemModelDetail.setItem(i, 3, QStandardItem(str(dataBaseCoordinate.longitude.value)))
                    if dataBaseCoordinate.latitude != None and dataBaseCoordinate.longitude != None:
                        pointMeter = QgisHelper.Degree2Meter(dataBaseCoordinate.longitude.value , dataBaseCoordinate.latitude.value)
                        self.standardItemModelDetail.setItem(i, 0, QStandardItem(str(pointMeter.get_X())))
                        self.standardItemModelDetail.setItem(i, 1, QStandardItem(str(pointMeter.get_Y())))

                if dataBaseCoordinate.altitude == None or dataBaseCoordinate.altitude.Metres == None:
                    self.standardItemModelDetail.setItem(i, 4, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 4, QStandardItem(str(dataBaseCoordinate.altitude.Metres)))
                if dataBaseCoordinate.type == None:
                    self.standardItemModelDetail.setItem(i, 5, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 5, QStandardItem(str(dataBaseCoordinate.type)))
                
                i += 1
                self.progress.setValue(i)
                QApplication.processEvents()
        if self.standardItemModel.rowCount() > 0 and self.selectedItem != None and self.selectedItem.text() == Captions.ROUTES:
#             rowIndex = int(self.standardItemModel.item(modelIndex.row(), 5).text())
            data = self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(modelIndex.row(), 2)).toInt()
            rowIndex = data[0]
            self.selectedRow = rowIndex
            dataBaseCoordinates = self.aixm.pointDataRoutes[rowIndex][1]
            
#             dataBaseCoordinates = self.aixm.pointDataRoutes[modelIndex.row()][1]
            self.standardItemModelDetail.clear()
            self.standardItemModelDetail.setHorizontalHeaderLabels(self.routesDetailColumnLabels)
            i = 0
            self.progress.setMaximum(len(dataBaseCoordinates))
#             print rowIndex, len(dataBaseCoordinates)
            for dataBaseCoordinate in dataBaseCoordinates:
                if dataBaseCoordinate.x == None:
                    self.standardItemModelDetail.setItem(i, 0, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 0, QStandardItem(str(dataBaseCoordinate.x)))
                if dataBaseCoordinate.y == None:
                    self.standardItemModelDetail.setItem(i, 1, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 1, QStandardItem(str(dataBaseCoordinate.y)))

                if dataBaseCoordinate.x != None and dataBaseCoordinate.y != None:
                    pointDegree = QgisHelper.Meter2Degree(dataBaseCoordinate.x, dataBaseCoordinate.y)
                    self.standardItemModelDetail.setItem(i, 2, QStandardItem(str(pointDegree.get_Y())))
                    self.standardItemModelDetail.setItem(i, 3, QStandardItem(str(pointDegree.get_X())))
                else:

                    if dataBaseCoordinate.latitude == None:
                        self.standardItemModelDetail.setItem(i, 2, QStandardItem(""))
                    else:
                        self.standardItemModelDetail.setItem(i, 2, QStandardItem(str(dataBaseCoordinate.latitude.value)))
                    if dataBaseCoordinate.longitude == None:
                        self.standardItemModelDetail.setItem(i, 3, QStandardItem(""))
                    else:
                        self.standardItemModelDetail.setItem(i, 3, QStandardItem(str(dataBaseCoordinate.longitude.value)))
                    if dataBaseCoordinate.latitude != None and dataBaseCoordinate.longitude != None:
                        pointMeter = QgisHelper.Degree2Meter(dataBaseCoordinate.longitude.value , dataBaseCoordinate.latitude.value)
                        self.standardItemModelDetail.setItem(i, 0, QStandardItem(str(pointMeter.get_X())))
                        self.standardItemModelDetail.setItem(i, 1, QStandardItem(str(pointMeter.get_Y())))

                if dataBaseCoordinate.altitude == None or dataBaseCoordinate.altitude.Metres == None:
                    self.standardItemModelDetail.setItem(i, 4, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 4, QStandardItem(str(dataBaseCoordinate.altitude.Metres)))
                if dataBaseCoordinate.type == None:
                    self.standardItemModelDetail.setItem(i, 5, QStandardItem(""))
                else:
                    self.standardItemModelDetail.setItem(i, 5, QStandardItem(str(dataBaseCoordinate.type)))
                
                i += 1
                self.progress.setValue(i)
                QApplication.processEvents()
                pass
            pass
        if self.standardItemModel.rowCount() > 0 and self.selectedItem != None and self.selectedItem.text() == Captions.SYMBOLS:
            self.selectedRow = self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(modelIndex.row(), 6)).toInt()[0]
        if self.standardItemModel.rowCount() > 0 and self.selectedItem != None and self.selectedItem.text() == Captions.OBSTACLES:
            self.selectedRow = self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(modelIndex.row(), 6)).toInt()[0]
        define._messagBar.hide()
        self.selectedDetailRow = None

    def treeClicked(self, modelIndex):
        self.standardItemModel.clear()
        self.standardItemModelDetail.clear()
        self.parametersPanel.cmbType.clear()
        self.parametersPanel.txtName.setText("")
        item = self.standardItemModel_tree.itemFromIndex(modelIndex)
        self.selectedItem = item
        
        if item.text() == Captions.AIRSPACE:
            self.parametersPanel.groupBox.setVisible(True)
            self.standardItemModelDetail.setHorizontalHeaderLabels(self.airspaceDetailColumnLabels)
            self.standardItemModel.setHorizontalHeaderLabels(self.airspaceColumnLabels)
            self.parametersPanel.tableView.hideColumn(5)
            self.parametersPanel.tableView.hideColumn(6)
            i = 0
            n = 0
            s = ""
            subList = []
            for dataRow in self.aixm.pointDataAirspace:
                name = dataRow[0]
                startIndex = name.indexOf("(") + 1
                endIndex = name.indexOf(")")
                subName = name.mid(startIndex, endIndex - startIndex)

                if n != 0:
                    m = 0
                    for sub in subList:
                        if sub.contains(subName):
                            m += 1
                    if m == 0:
                        subList.append(subName)
                else:
                    subList.append(subName)
                n += 1

            self.parametersPanel.cmbType.addItem("")
            for sub in subList:
                self.parametersPanel.cmbType.addItem(sub)


            for dataRow in self.aixm.pointDataAirspace:
                self.standardItemModel.setItem(i, 0, QStandardItem(dataRow[0]))
                if dataRow[1] == None or dataRow[1] == "":
                    self.standardItemModel.setItem(i, 1, QStandardItem(""))
                else:
                    self.standardItemModel.setItem(i, 1, QStandardItem(dataRow[1]))
                if dataRow[2] == None or dataRow[2] == "":
                    self.standardItemModel.setItem(i, 2, QStandardItem(""))
                else:
                    self.standardItemModel.setItem(i, 2, QStandardItem(dataRow[2]))
                if dataRow[3] == None or dataRow[3] == "":
                    self.standardItemModel.setItem(i, 3, QStandardItem(""))
                else:
                    self.standardItemModel.setItem(i, 3, QStandardItem(dataRow[3]))
                self.standardItemModel.setItem(i, 4, QStandardItem(str(len(dataRow[6]))))
                self.standardItemModel.setItem(i, 5, QStandardItem(str(i)))
                
#                 self.standardItemModel.setItem(i, 5, QStandardItem(dataRow[5]))
#                 self.standardItemModel.setItem(i, 6, QStandardItem("DataBaseCoordinates(" + str(len(dataRow[6])) + ")"))
                i += 1
                
        if item.text() == Captions.ROUTES:
            self.parametersPanel.groupBox.setVisible(True)
            self.standardItemModelDetail.setHorizontalHeaderLabels(self.routesDetailColumnLabels)
            self.standardItemModel.setHorizontalHeaderLabels(self.routesColumnLabels)
            self.parametersPanel.tableView.hideColumn(2)
            self.parametersPanel.tableView.hideColumn(3)

            n = 0
            s = ""
            subList = []
            for dataRow in self.aixm.pointDataRoutes:
                name = dataRow[0]
                startIndex = name.indexOf(" ") + 1
                endIndex = name.length()
                subName = name.mid(startIndex, endIndex - startIndex)

                if n != 0:
                    m = 0
                    for sub in subList:
                        if sub.contains(subName):
                            m += 1
                    if m == 0:
                        subList.append(subName)
                else:
                    subList.append(subName)
                n += 1

            self.parametersPanel.cmbType.addItem("")
            for sub in subList:
                self.parametersPanel.cmbType.addItem(sub)


            i = 0
            for dataRow in self.aixm.pointDataRoutes:
                self.standardItemModel.setItem(i, 0, QStandardItem(dataRow[0]))
                self.standardItemModel.setItem(i, 1, QStandardItem(str(len(dataRow[1]))))
                self.standardItemModel.setItem(i, 2, QStandardItem(str(i)))
                i += 1
        if item.text() == Captions.GEOGRAPHICAL_BORDER:
            self.parametersPanel.groupBox.setVisible(True)
            self.standardItemModelDetail.setHorizontalHeaderLabels(self.borderDetailColumnLabels)
            self.standardItemModel.setHorizontalHeaderLabels(self.borderColumnLabels)
            self.parametersPanel.tableView.hideColumn(3)
            self.parametersPanel.tableView.hideColumn(4)

            n = 0
            s = ""
            subList = []
            for dataRow in self.aixm.pointDataBorder:
                name = dataRow[0]
                startIndex = name.indexOf("_") + 1
                endIndex = name.length()
                subName = name.mid(startIndex, endIndex - startIndex)

                if n != 0:
                    m = 0
                    for sub in subList:
                        if sub.contains(subName):
                            m += 1
                    if m == 0:
                        subList.append(subName)
                else:
                    subList.append(subName)
                n += 1

            self.parametersPanel.cmbType.addItem("")
            for sub in subList:
                self.parametersPanel.cmbType.addItem(sub)

            # item0 = self.aixm.pointDataBorder[0]
            # typeList = []
            # typeList.append(item0[1])
            # for dataRow in self.aixm.pointDataBorder:
            #     n = 0
            #     for typeStr in typeList:
            #         if typeStr == dataRow[1]:
            #             n += 1
            #     if n == 0 :
            #         typeList.append(dataRow[1])
            #
#             for typeStr in typeList:
#                 self.parametersPanel.cmbType.addItem(typeStr)
#             self.parametersPanel.txtName.setText(Captions.GEOGRAPHICAL_BORDER)
            i = 0
            for dataRow in self.aixm.pointDataBorder:
                self.standardItemModel.setItem(i, 0, QStandardItem(dataRow[0]))
                self.standardItemModel.setItem(i, 1, QStandardItem(dataRow[1]))
                self.standardItemModel.setItem(i, 2, QStandardItem(str(len(dataRow[2]))))
                self.standardItemModel.setItem(i, 3, QStandardItem(str(i)))
                i += 1
            self.sortFilterProxyModel.setFilterKeyColumn(1) 
            self.setFilterFixedString(self.parametersPanel.cmbType.currentText())   
        if item.text() == Captions.OBSTACLES:
            self.parametersPanel.groupBox.setVisible(False)
            self.standardItemModel.setHorizontalHeaderLabels(self.obstaclesColumnLabels)
            self.parametersPanel.tableView.hideColumn(6)
            self.parametersPanel.cmbType.clear()
            item0 = self.aixm.pointDataObstacles[0]
            typeList = []
            typeList.append(item0[7])
            for dataRow in self.aixm.pointDataObstacles:
                n = 0
                for typeStr in typeList:
                    if typeStr == dataRow[7]:
                        n += 1
                if n == 0 :
                    typeList.append(dataRow[7])
            self.parametersPanel.cmbType.addItem("")
            for typeStr in typeList:
                self.parametersPanel.cmbType.addItem(typeStr)
#             self.parametersPanel.txtName.setText(Captions.OBSTACLES)
            
            i = 0
            for dataRow in self.aixm.pointDataObstacles:
                self.standardItemModel.setItem(i, 0, QStandardItem(dataRow[0]))
                self.standardItemModel.setItem(i, 1, QStandardItem(dataRow[3]))
                self.standardItemModel.setItem(i, 2, QStandardItem(dataRow[4]))
                self.standardItemModel.setItem(i, 3, QStandardItem(dataRow[5]))
                self.standardItemModel.setItem(i, 4, QStandardItem(dataRow[7]))
                self.standardItemModel.setItem(i, 5, QStandardItem(dataRow[6]))
                self.standardItemModel.setItem(i, 6, QStandardItem(str(i)))
                i += 1
            self.sortFilterProxyModel.setFilterKeyColumn(4) 
            self.setFilterFixedString(self.parametersPanel.cmbType.currentText())   
        if item.text() == Captions.SYMBOLS:
            self.parametersPanel.groupBox.setVisible(False)
            self.standardItemModel.setHorizontalHeaderLabels(self.symbolsColumnLabels)
#             self.parametersPanel.tableView.hideColumn(6)
            item0 = self.aixm.pointData[0]
            typeList = []
            typeList.append(item0[7])
            for dataRow in self.aixm.pointData:
                n = 0
                for typeStr in typeList:
                    if typeStr == dataRow[7]:
                        n += 1
                if n == 0 :
                    typeList.append(dataRow[7])
                    
            self.parametersPanel.cmbType.addItem("")
            for typeStr in typeList:
                self.parametersPanel.cmbType.addItem(typeStr)
#             self.parametersPanel.txtName.setText(Captions.SYMBOLS)
            i = 0
            for dataRow in self.aixm.pointData:
                self.standardItemModel.setItem(i, 0, QStandardItem(dataRow[0]))
                self.standardItemModel.setItem(i, 1, QStandardItem(dataRow[3]))
                self.standardItemModel.setItem(i, 2, QStandardItem(dataRow[4]))
                self.standardItemModel.setItem(i, 3, QStandardItem(dataRow[5]))
                self.standardItemModel.setItem(i, 4, QStandardItem(dataRow[7]))
                if dataRow[6] == "ESSA":
                    pass
                self.standardItemModel.setItem(i, 5, QStandardItem(dataRow[6]))
                self.standardItemModel.setItem(i, 6, QStandardItem(str(i)))
                i += 1
            self.sortFilterProxyModel.setFilterKeyColumn(4) 
            self.setFilterFixedString(self.parametersPanel.cmbType.currentText())
        self.selectedRow = None
        self.selectedRowSortModel = None
#         print "ok", modelIndex.row()
    def setFilterFixedString(self, filterString):
        
        self.sortFilterProxyModel.setFilterFixedString(filterString)
#         self.sortFilterProxyModel.setFilterFixedString(filterString)
#         self.setVerticalHeader()
    def setVerticalHeader(self):
        for i in range(self.sortFilterProxyModel.rowCount()):
            self.sortFilterProxyModel.setHeaderData(i, Qt.Vertical, i+1, Qt.DisplayRole)
    
    def cmbTypeIndexChanged(self):
        self.parametersPanel.txtName.setText("")
#         self.parametersPanel.tableView.setSortingEnabled(False)
        self.sortFilterProxyModel.setSourceModel(self.standardItemModel)

        if self.selectedItem.text() == Captions.AIRSPACE or self.selectedItem.text() == Captions.ROUTES or self.selectedItem.text() == Captions.GEOGRAPHICAL_BORDER:
            self.sortFilterProxyModel.setFilterKeyColumn(0)
            self.setFilterFixedString(self.parametersPanel.cmbType.currentText())

            if self.parametersPanel.cmbType.currentIndex() > 0:
                self.abstructModel.clear()
                if self.selectedItem.text() == Captions.AIRSPACE:
                    self.abstructModel.setHorizontalHeaderLabels(self.airspaceColumnLabels)
                elif self.selectedItem.text() == Captions.GEOGRAPHICAL_BORDER:
                    self.abstructModel.setHorizontalHeaderLabels(self.borderColumnLabels)
                elif self.selectedItem.text() == Captions.ROUTES:
                    self.abstructModel.setHorizontalHeaderLabels(self.routesColumnLabels)
                for i in range(self.sortFilterProxyModel.rowCount()):
                    for j in range(self.sortFilterProxyModel.columnCount()):
                        if self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, j)) != None:
                            data = self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, j)).toString()
                        else:
                            data = ""
#                         itemTxt = self.sortFilterProxyModel.item(i, j).text()
                        self.abstructModel.setItem(i, j, QStandardItem(data))

                self.sortFilterProxyModel.setSourceModel(self.abstructModel)

        if self.selectedItem.text() == Captions.OBSTACLES or self.selectedItem.text() == Captions.SYMBOLS:
            self.sortFilterProxyModel.setFilterKeyColumn(4)
            self.setFilterFixedString(self.parametersPanel.cmbType.currentText())

            if self.parametersPanel.cmbType.currentIndex() > 0:
                self.abstructModel.clear()
                self.abstructModel.setHorizontalHeaderLabels(self.obstaclesColumnLabels)
                for i in range(self.sortFilterProxyModel.rowCount()):
                    for j in range(self.sortFilterProxyModel.columnCount()):
                        if self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, j)) != None:
                            data = self.sortFilterProxyModel.data(self.sortFilterProxyModel.index(i, j)).toString()
                        else:
                            data = ""
#                         itemTxt = self.sortFilterProxyModel.item(i, j).text()
                        self.abstructModel.setItem(i, j, QStandardItem(data))

                self.sortFilterProxyModel.setSourceModel(self.abstructModel)
#                 self.sortFilterProxyModel.setFilterKeyColumn(0)
#                 self.setFilterFixedString(self.parametersPanel.txtName.text())


        self.setVerticalHeader()        
#         self.loadTable(self.aixm)
    def uiStateInit(self):
        self.ui.btnConstruct.setText("Insert")
        self.ui.btnConstruct.setEnabled(False)
        self.ui.btnOpenData.hide()
        self.ui.btnSaveData.hide()
#         self.ui.btnOutput = QPushButton(self.ui.frame_Btns)
# #         font = QtGui.QFont()
# #         font.setFamily(_fromUtf8("Arial"))
# #         font.setBold(False)
# #         font.setWeight(50)
# #         self.btnOpenData.setFont(font)
#         self.ui.btnOutput.setObjectName("btnOutput")
#         self.ui.btnOutput.setText("Output")
#         self.ui.verticalLayout_Btns.insertWidget(3, self.ui.btnOutput)
#         self.ui.btnOutput.setEnabled(False)
#         self.ui.btnOutput.clicked.connect(self.btnOutputClicked)
        
        return FlightPlanBaseSimpleDlg.uiStateInit(self)    
    def method_49(self):
        resultPolylineAreaList = []
        
        progressMessageBar = define._messagBar.createMessage("Creating airspace layer...")
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)        
        progressMessageBar.layout().addWidget(self.progress)
        define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
        pointDataAirspaceCount = len(self.aixm.pointDataAirspace)
        self.progress.setMaximum(pointDataAirspaceCount)
        n = 0
        for current in self.aixm.pointDataAirspace:
            value = current[0]
            altitude = None
            if current[1] == None or current[1] == "" or current[1] == "0.0":
                altitude = Altitude(None)
            else:
                altitude = Altitude(float(current[1]))
            value1 = None
            if current[2] == None or current[2] == "" or current[2] == "0,0":
                value1 = Altitude(None)
            else:
                value1 = Altitude(float(current[2]))
            distance = None
            if current[3] == None or current[3] == "":
                distance = Distance(None)
            else:
                distance = Distance(float(current[3]), DistanceUnits.M)
            flag1 = False
            if current[4] == "True":
                flag1 = True
            else:
                flag1 = False
            value2 = False
            if current[5] == "True":
                value2 = True
            else:
                value2 = False
            dataBaseCoordinate = current[6]
            
            if (dataBaseCoordinate == None or len(dataBaseCoordinate) == 0):
                n += 1
                continue
            if (distance == None or not distance.IsValid()):
                if (not altitude.IsValid()):
                    altitude = Altitude(0.0)
                polylineArea = self.method_55(dataBaseCoordinate)
                if len(polylineArea) == 0:
                    n += 1
                    continue
                polyline = PolylineArea.smethod_136(polylineArea, value2)
                if (value1 == None or not value1.IsValid() or not flag1):
                    resultPolylineAreaList.append((polyline, current))
#                     AcadHelper.smethod_18(transaction_0, blockTableRecord_0, polyline, string_0)
                else:
                    count = len(dataBaseCoordinate) < 200
                    flag2 = count
                    if (not count):
                        flag2 = False
                    if (not value2 or not flag2):
                        resultPolylineAreaList.append((polyline, current))
                    else:
                        resultPolylineAreaList.append((polyline, current))
            else:
                if (altitude == None or not altitude.IsValid()):
                    altitude = Altitude(0)
                item1 = dataBaseCoordinate[0]
                if (value1 == None or not value1.IsValid() or not flag1):
                    point3d1 = Point3D(item1.longitude.value, item1.latitude.value, 0.0)
                    degreeLength = self.getDegreeLength(point3d1, distance.Metres)
                    point3dArray = MathHelper.constructCircle(point3d1.smethod_167(value1.Metres), degreeLength, 50)
                    resultPolylineAreaList.append((PolylineArea(point3dArray), current))
                else:
                    point3d1 = Point3D(item1.longitude.value, item1.latitude.value, altitude.Metres)
                    degreeLength = self.getDegreeLength(point3d1, distance.Metres)
#                     point3d1 = self.method_54(item1.x, item1.y, item1.latitude, item1.longitude, altitude)
                    point3dArray = MathHelper.constructCircle(point3d1.smethod_167(value1.Metres), degreeLength, 50)
                    resultPolylineAreaList.append((PolylineArea(point3dArray), current))
            self.progress.setValue(n)
            QApplication.processEvents()
            n += 1
        self.progress.setValue(pointDataAirspaceCount)
        define._messagBar.hide() 
        return resultPolylineAreaList
    def getDegreeLength(self, point3d0_dgree, length_metre):
        llCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        xyCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        point3d0 = QgisHelper.CrsTransformPoint(point3d0_dgree.get_X(), point3d0_dgree.get_Y(), llCrs, xyCrs)
        point3d = Point3D(point3d0.get_X() + length_metre, point3d0.get_Y())
        point3d1 = QgisHelper.CrsTransformPoint(point3d.get_X(), point3d.get_Y(), xyCrs, llCrs)
        return math.fabs(point3d1.get_X() - point3d0_dgree.get_X())
    def method_51(self):
        flag = False
        dataList = []
        for current in self.aixm.pointDataBorder:
            value = current[0]
            dataBaseCoordinate = current[2]
            if dataBaseCoordinate == None or len(dataBaseCoordinate) == 0:
                continue
            polylineArea = self.method_55(dataBaseCoordinate)
            if len(polylineArea) == 0:
                continue
            dataList.append((PolylineArea.smethod_131(polylineArea).method_14(), current))
        return dataList
    def method_53(self):
        flag = False
        dataList = []
        for current in self.aixm.pointDataRoutes:
            value = current[0]
            dataBaseCoordinate = current[1]
            if dataBaseCoordinate == None or len(dataBaseCoordinate) == 0:
                continue
            result, resultPoint3dArrayList = self.method_56(dataBaseCoordinate, value)
            if not result:
                flag = False
                continue
            else:
                dataList.append((resultPoint3dArrayList, current))
        return dataList
                
            
    def method_54(self, double_0, double_1, degrees_0, degrees_1, altitude_0):
        metres = 0
        if (altitude_0 != None and altitude_0.IsValid()):
            metres = altitude_0.Metres
#         if (double_0 == None or double_1 == None):
        llCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
        xyCrs = QgsCoordinateReferenceSystem(32633, QgsCoordinateReferenceSystem.EpsgCrsId)
        point3d0 = QgisHelper.CrsTransformPoint(degrees_1.value, degrees_0.value, llCrs, xyCrs, metres)
        return point3d0
#             if (!Geo.smethod_3(degrees_0, degrees_1, out double_0, out double_1))
#             {
#                 throw new Exception(Geo.LastError)
#             }
#             return new Point3d(double_0, double_1, metres)
#         }
#         if (!self.transformXY)
#         {
#             return new Point3d(double_0, double_1, metres)
#         }
#         point3d = Point3D(0, 0, metres)
#         point3d1 = Point3D(double_0, double_1, metres)
#         num = MathHelper.getBearing(point3d, point3d1)
#         num1 = MathHelper.calcDistance(point3d, point3d1)
#         return MathHelper.distanceBearingPoint(self.ptThr, self.trThrEndP90 + num, num1).smethod_167(metres)
    def method_55(self, dataBaseCoordinates_0):
        num = None
        num1 = None
        polylineArea = None
        polylineArea1 = PolylineArea()
        origin = Point3D.get_Origin()
        point3d = Point3D.get_Origin()
        origin1 = Point3D.get_Origin()
        flag = False
        flag1 = False
        turnDirection = TurnDirection.Nothing
        
        for current in dataBaseCoordinates_0:
            point3d1 = None
            if current.longitude == None or current.latitude == None:
                continue
            if current.altitude != None and current.altitude.isValid():
                point3d1 = Point3D(current.longitude.value, current.latitude.value, current.altitude.Metres)
            else:
                point3d1 = Point3D(current.longitude.value, current.latitude.value, 0.0)
#             point3d1 = self.method_54(current.x, current.y, current.latitude, current.longitude, current.altitude)
            if current.type == DataBaseCoordinateType.FNT or current.type == DataBaseCoordinateType.GRC or current.type == DataBaseCoordinateType.Point or current.type == DataBaseCoordinateType.ArcPoint:
                if (flag):
                    polylineArea1[polylineArea1.Count - 1].set_Bulge(MathHelper.smethod_60(origin, point3d, point3d1))
                elif (flag1):
                    polylineArea1[polylineArea1.Count - 1].set_Bulge(MathHelper.smethod_57(turnDirection, origin, point3d1, origin1))
                polylineArea1.method_1(point3d1)
                flag = False
                flag1 = False
            elif current.type == DataBaseCoordinateType.MidPoint:
                origin = polylineArea1[polylineArea1.Count - 1].Position
                point3d = point3d1
                flag = True
                flag1 = False
            elif current.type == DataBaseCoordinateType.CWA or current.type == DataBaseCoordinateType.CCA:
                if (flag):
                    polylineArea1[polylineArea1.Count - 1].set_Bulge(MathHelper.smethod_60(origin, point3d, point3d1))
                elif (flag1):
                    polylineArea1[polylineArea1.Count - 1].set_Bulge(MathHelper.smethod_57(turnDirection, origin, point3d1, origin1))
                polylineArea1.method_1(point3d1)
                origin = point3d1
#                 if (!Geo.smethod_3(current.CenterLatitude, current.CenterLongitude, out num, out num1))
#                 {
#                     throw new Exception(Geo.LastError)
#                 }
                if current.centerLongitude == None or current.centerLatitude == None:
                    origin1 = Point3D.get_Origin()
                else:
#                     origin1 = self.method_54(None, None, current.centerLatitude, current.centerLongitude, Altitude(0))
                    origin1 = Point3D(current.centerLongitude.value, current.centerLatitude.value, 0)
                turnDirection = TurnDirection.Right if(current.type != DataBaseCoordinateType.CCA) else TurnDirection.Left
                flag = False
                flag1 = True
        if (flag):
            polylineArea1[polylineArea1.Count - 1].set_Bulge(MathHelper.smethod_60(origin, point3d, polylineArea1[0].Position))
        elif (flag1):
            polylineArea1[polylineArea1.Count - 1].set_Bulge(MathHelper.smethod_57(turnDirection, origin, polylineArea1[0].Position, origin1))
        return polylineArea1
    
    def method_56(self, dataBaseCoordinates_0, string_1):
        self.textHeight = 0.0005
        distance = None
        num = None
        num1 = None
        point3d = None
        point3d1 = None
        str0 = None
        flag = False
        if (dataBaseCoordinates_0 == None or len(dataBaseCoordinates_0) == 0):
            return True
        naN = None
        degree = None
        origin = Point3D.get_Origin()
        num2 = 0
        resultPoint3dArrayList = []
        while (num2 < len(dataBaseCoordinates_0)):
            item = dataBaseCoordinates_0[num2]
#             if (AcadHelper.Cancelled)
#             {
#                 flag = false
#                 return flag
#             }
#             else
#             {
            latitude = item.latitude
            longitude = item.longitude
#             if ((!latitude.IsValid || !longitude.IsValid) && !Geo.smethod_2(item.X, item.Y, out latitude, out longitude))
#             {
#                 throw new Exception(Geo.LastError)
#             }
            point3d2 = Point3D(item.longitude.value, item.latitude.value, item.altitude)
#             point3d2 = self.method_54(item.X, item.Y, item.Latitude, item.Longitude, item.Altitude)
            if (num2 > 0):
                result, distance, num, num1 = QgisHelper.smethod_4(GeoCalculationType.Ellipsoid, naN, degree, latitude, longitude)
                if (not result):
                    return (False, None)
#                     throw new Exception(Geo.LastError)
#                 }
                value = None
                try:
                    value = dataBaseCoordinates_0[num2 - 1].variation.value
                except:
                    value = 0.0
                value1 = None
                try:
                    value1 = item.variation.value
                except:
                    value1 = 0.0
                num3 = MathHelper.calcDistance(origin, point3d2)
                num4 = MathHelper.smethod_26(origin, point3d2)
                point3d3 = MathHelper.distanceBearingPoint(origin, 7.85398163397448 - num4, num3 / 2)
                num5 = MathHelper.smethod_3(num + value)
                str1 = str(num5)
                num6 = MathHelper.smethod_3(num1 + value1)
                str2 = str(num6)
                str3 = str(int(distance.NauticalMiles))
                length = len(str3)
                num7 = self.textHeight * 0.75
                num8 = num7 * (float(length) / 1.5)
                num9 = num4 + 1.5707963267949
                num10 = num4 - 1.5707963267949
                num11 = num4 + 3.14159265358979
                point3d4 = MathHelper.distanceBearingPoint(point3d3, 7.85398163397448 - num4, num8)
                point3d5 = MathHelper.distanceBearingPoint(point3d4, 7.85398163397448 - num4, num7)
                point3d6 = MathHelper.distanceBearingPoint(point3d4, 7.85398163397448 - num9, num7)
                point3d7 = MathHelper.distanceBearingPoint(point3d4, 7.85398163397448 - num10, num7)
                point3d8 = MathHelper.distanceBearingPoint(point3d3, 7.85398163397448 - num11, num8)
                point3d9 = MathHelper.distanceBearingPoint(point3d8, 7.85398163397448 - num11, num7)
                point3d10 = MathHelper.distanceBearingPoint(point3d8, 7.85398163397448 - num9, num7)
                point3d11 = MathHelper.distanceBearingPoint(point3d8, 7.85398163397448 - num10, num7)
                num12 = 450 - Unit.smethod_1(num11)
                if (Unit.smethod_1(num4) <= 90 or Unit.smethod_1(num4) >= 270):
                    num12 = num12 + 180
                    point3d = MathHelper.distanceBearingPoint(point3d3, Unit.ConvertDegToRad(450) - num9, num7)
                    point3d1 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num9, 3 * num7)
                else:
                    point3d = MathHelper.distanceBearingPoint(point3d3, Unit.ConvertDegToRad(450) - num10, num7)
                    point3d1 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(450) - num10, 3 * num7)
                point3dArray = [point3d5, point3d6, point3d10, point3d9, point3d11, point3d7]
                polyline = PolylineArea(point3dArray)
                resultPoint3dArrayList.append(polyline.method_14_closed())
                resultPoint3dArrayList.append([point3d5, point3d2])
                resultPoint3dArrayList.append([point3d9, origin])
#                 polyline.set_Closed(true)
#                 AcadHelper.smethod_18(transaction_0, blockTableRecord_0, polyline, string_0)
#                 AcadHelper.smethod_18(transaction_0, blockTableRecord_0, new Line(point3d5.smethod_167(0), point3d2.smethod_167(0)), string_0)
#                 AcadHelper.smethod_18(transaction_0, blockTableRecord_0, new Line(point3d9.smethod_167(0), origin.smethod_167(0)), string_0)
#                 DBText dBText = AcadHelper.smethod_138(str3, point3d3, self.textHeight, 4)
#                 dBText.set_Rotation(7.85398163397448 - Units.ConvertDegToRad(num12))
#                 AcadHelper.smethod_18(transaction_0, blockTableRecord_0, dBText, string_0)
#                 DBText dBText1 = AcadHelper.smethod_138(str, point3d1, self.textHeight, 4)
#                 dBText1.set_Rotation(7.85398163397448 - Units.ConvertDegToRad(num12))
#                 AcadHelper.smethod_18(transaction_0, blockTableRecord_0, dBText1, string_0)
#             }
            naN = latitude
            degree = longitude
            origin = point3d2
#             progressMeter.MeterProgress()
            num2 += 1
#             }
#         }
#         progressMeter.Stop()
        return (True, resultPoint3dArrayList)
#         return 
class DataBaseLoaderAixm:
    def __init__(self, fileName, bool_0):
        dateTime = None
        num = None
        
        self.pointData = []
        self.pointDataObstacles = []
        self.pointDataRoutes = []
        self.pointDataAirspace = []
        self.pointDataBorder = []
        
        doc = QDomDocument()
        qFile = QFile(fileName)
        if qFile.open(QFile.ReadOnly):
            doc.setContent(qFile)
            qFile.close()
        else:
            raise UserWarning, "can not open file:" + fileName
        
        progressMessageBar = define._messagBar.createMessage("Reding xml file...")
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)        
        progressMessageBar.layout().addWidget(self.progress)
        define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
        self.progress.setMaximum(100)
        if bool_0:
            nodes = doc.elementsByTagName("AIXM-Snapshot") 
            if (self.method_20(doc.elementsByTagName("Vor") )):
                pass
        elif (self.method_3(doc.elementsByTagName("Ahp"))):
            self.progress.setValue(6)
            QApplication.processEvents()
            if (self.method_4(doc.elementsByTagName("Rcp"))):
                self.progress.setValue(12)
                QApplication.processEvents()
                if (self.method_5(doc.elementsByTagName("Rdn"))):
                    self.progress.setValue(18)
                    QApplication.processEvents()
                    if (self.method_6(doc.elementsByTagName("Dpn"))):
                        self.progress.setValue(24)
                        QApplication.processEvents()
                        if (self.method_7(doc.elementsByTagName("Vor"))):
                            self.progress.setValue(30)
                            QApplication.processEvents()
                            if (self.method_8(doc.elementsByTagName("Tcn"))):
                                self.progress.setValue(36)
                                QApplication.processEvents()
                                if (self.method_10(doc.elementsByTagName("Ndb"))):
                                    self.progress.setValue(39)
                                    QApplication.processEvents()
                                    if (self.method_9(doc.elementsByTagName("Dme"))):
                                        self.progress.setValue(42)
                                        QApplication.processEvents()
                                        if (self.method_11(doc.elementsByTagName("Mkr"))):
                                            self.progress.setValue(48)
                                            QApplication.processEvents()
                                            if (self.method_12(doc.elementsByTagName("Sns"))):
                                                self.progress.setValue(54)
                                                QApplication.processEvents()
                                                if (self.method_13(doc.elementsByTagName("Ils"))):
                                                    self.progress.setValue(60)
                                                    QApplication.processEvents()
                                                    if (self.method_14(doc.elementsByTagName("Mls"))):
                                                        self.progress.setValue(66)
                                                        QApplication.processEvents()
                                                        if (self.method_15(doc.elementsByTagName("Obs"))):
                                                            self.progress.setValue(72)
                                                            QApplication.processEvents()
                                                            if (self.method_16(doc.elementsByTagName("Rsg"))):
                                                                self.progress.setValue(80)
                                                                QApplication.processEvents()
                                                                if (self.method_17(doc.elementsByTagName("Ase"))):
                                                                    self.progress.setValue(86)
                                                                    QApplication.processEvents()
                                                                    if (self.method_18(doc.elementsByTagName("Abd"))):
                                                                        self.progress.setValue(95)
                                                                        QApplication.processEvents()
                                                                        if (self.method_19(doc.elementsByTagName("Gbr"))):
                                                                            self.progress.setValue(100)
                                                                            QApplication.processEvents()
                                                                            pass
        self.progress.setValue(100)
        define._messagBar.hide()  
        
#         print element.text()
#         print "sdfadsgad"
    def method_3(self, xmlNodeList_0):
        flag = None
        resultPoint = []
        altitude_metre = None
        if (xmlNodeList_0 != None and xmlNodeList_0.count() > 0):
#             IEnumerator enumerator = xmlNodeList_0.GetEnumerator()
            count = xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                xmlNodes = current.namedItem("AhpUid")
                if (xmlNodes != None):
                    node = xmlNodes.namedItem("codeId")
                    symbolAttribute.append(node.toElement().text())
                    pass
                xmlNodes = current.namedItem("geoLat")
                if (xmlNodes != None):
                    symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.toElement().text(), DegreesType.Latitude).value))
                xmlNodes = current.namedItem("geoLong")
                if (xmlNodes != None):
                    symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.toElement().text(), DegreesType.Longitude).value))
                xmlNodes = current.namedItem("OrgUid")
                if (xmlNodes != None):
                    symbolAttribute.append(xmlNodes.namedItem("txtName").toElement().text())
                xmlNodes = current.namedItem("txtName")
                if (xmlNodes != None):
                    symbolAttribute.append(xmlNodes.toElement().text())
                xmlNodes = current.namedItem("valElev")
                if (xmlNodes != None):
                    innerText = xmlNodes.toElement().text()
                xmlNodes = current.namedItem("uomDistVer")
                if (xmlNodes != None):
                    str0 = xmlNodes.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
#                         symbolAttribute.append(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
#                         symbolAttribute.append(Altitude(float(innerText)).Metres)
                else:
                    altitude_metre = "0.0"
#                     symbolAttribute.append(0)
                
                
                xmlNodes = current.namedItem("valMagVar")
                if (xmlNodes != None):
                    symbolAttribute.append(xmlNodes.toElement().text() + " (" + Captions.MAGN_VAR + ")")
                xmlNodes = current.namedItem("dateMagVar")
                if (xmlNodes != None):
                    symbolAttribute.append(xmlNodes.toElement().text() + " (" + Captions.MAGN_VAR_DATE + ")")
                xmlNodes = current.namedItem("dateMagVarChg")
                if (xmlNodes != None):
                    symbolAttribute.append(xmlNodes.toElement().text() + " (" + Captions.MAGN_VAR_ANNUAL_CHANGE + ")")
#                 self.dataBase.method_1(symbolAttribute[0], Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude, self.formatProvider), Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude, self.formatProvider), Altitude.smethod_4(innerText, str, self.formatProvider), new Symbol(SymbolType.Arp), symbolAttribute)
                
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]

                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Arp, "Ahp", current])
#             print self.pointData
            return True
        return True
    def method_4(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
#             try:
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                altitude_metre = None
                xmlNodes = current.namedItem("RcpUid")
                xmlNodes1 = xmlNodes.namedItem("RwyUid")
                xmlNodes2 = xmlNodes1.namedItem("AhpUid")
                symbolAttribute.append(Captions.RWY_BIG + " " + xmlNodes1.namedItem("txtDesig").toElement().text())
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
#                     symbolAttribute.append(xmlNodes.namedItem("geoLat").toElement().text())
#                     symbolAttribute.append(xmlNodes.namedItem("geoLong").toElement().text())
                symbolAttribute.append(xmlNodes2.namedItem("codeId").toElement().text())
                xmlNodes3 = current.namedItem("valElev")
                if (xmlNodes3 != None):
                    innerText = xmlNodes3.toElement().text()
                xmlNodes3 = current.namedItem("uomDistVer")
                if (xmlNodes3 != None):
                    str0 = xmlNodes3.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                if attr == "ESNY":
                    pass
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Default, "Rcp", current])
#                 print self.pointData
            return True
#             except:
#                 return False
        return True
    
    def method_5(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
#             try:
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                altitude_metre = None
                xmlNodes = current.namedItem("RdnUid")
                xmlNodes1 = xmlNodes.namedItem("RwyUid").namedItem("AhpUid")
                symbolAttribute.append(Captions.THR_BIG + " " + Captions.RWY_BIG + " " + xmlNodes.namedItem("txtDesig").toElement().text())
                xmlNodes2 = current.namedItem("geoLat")
                if xmlNodes2.toElement().text() == "":
                    continue
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes2.toElement().text(), DegreesType.Latitude).value))
                if current.namedItem("geoLong").toElement().text() == "":
                    continue
                symbolAttribute.append(str(Degrees.smethod_15(current.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
#                     symbolAttribute.append(xmlNodes.namedItem("geoLat").toElement().text())
#                     symbolAttribute.append(xmlNodes.namedItem("geoLong").toElement().text())
                symbolAttribute.append(xmlNodes1.namedItem("codeId").toElement().text())
                xmlNodes3 = current.namedItem("valElevTdz")
                if (xmlNodes3 != None):
                    innerText = xmlNodes3.toElement().text()
                xmlNodes3 = current.namedItem("uomElevTdz")
                if (xmlNodes3 != None):
                    str0 = xmlNodes3.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                if attr == "ESKN":
                    pass
                isSameData = False
                n = 0
                for pointData0 in self.pointData:
                    if pointData0[3] == symbolAttribute[1] and pointData0[4] == symbolAttribute[2] and pointData0[7] == SymbolType.Default:
                        isSameData = True
                        break
                    n += 1
                if not isSameData:
                    self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Default, "Rdn", current])
                else:
                    self.pointData[n][0] = symbolAttribute[0]
                    if altitude_metre == "0.0" or float(self.pointData[n][5]) > 0.0:
                        continue
                    else:
                        self.pointData[n][5] = altitude_metre
                    # symbolAttribute = item[8] as SymbolAttributes
                    # if (symbolAttribute == null)
                    # {
                    #     continue
                    # }
                    # symbolAttribute[0] = item[0] as string
                    # if (!altitude.IsValid)
                    # {
                    #     continue
                    # }
                    # symbolAttribute[4] = string.Format("{0} {1}", Captions.TOUCH_DOWN_ZONE_ELEVATION, altitude.method_0(":u"))

#                 print self.pointData
            return True
#             except:
#                 return False
        return True
    
    def method_6(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
#             try:
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                altitude_metre = None
                xmlNodes = current.namedItem("DpnUid")
                symbolAttribute.append(xmlNodes.namedItem("codeId").toElement().text())
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                symbolAttribute.append(current.namedItem("codeType").toElement().text())
#                     symbolAttribute.append(xmlNodes.namedItem("geoLong").toElement().text())
                
                xmlNodes1 = current.namedItem("txtName")
                if (xmlNodes1 != None):
                    symbolAttribute.append(xmlNodes1.toElement().text())
                xmlNodes3 = current.namedItem("txtRmk")
                if (xmlNodes3 != None):
                    symbolAttribute.append(xmlNodes3.toElement().text())
                xmlNodes3 = current.namedItem("valCrc")
                if (xmlNodes3 != None):
                    symbolAttribute.append(xmlNodes3.toElement().text())
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                symbolType = SymbolType.Repnc
                if symbolAttribute[4].count("FAF") > 0:
                    symbolType = SymbolType.Faf
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], "", attr, symbolType, "Dpn", current])
#                 print self.pointData
            return True
#             except:
#                 return False
        return True
    
    
    def method_7(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
#             try:
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                altitude_metre = None
                xmlNodes = current.namedItem("VorUid")
                xmlNodes1 = xmlNodes.namedItem("OrgUid")
                symbolAttribute.append(xmlNodes.namedItem("codeId").toElement().text())
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                symbolAttribute.append(xmlNodes1.namedItem("txtName").toElement().text())
                xmlNodes2 = current.namedItem("valFreq")
                if (xmlNodes2 != None):
                    symbolAttribute.append(Captions.FREQUENCY_BIG + " " + xmlNodes2.toElement().text())
                    
                xmlNodes2 = current.namedItem("uomFreq")
                if (xmlNodes2 != None):
                    if len(symbolAttribute) > 4:
                        s = symbolAttribute[4]
                        symbolAttribute.pop(4)
                        symbolAttribute.append(s + " " + xmlNodes2.toElement().text())  
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text())   
                xmlNodes2 = current.namedItem("txtName")
                if (xmlNodes2 != None):
                    symbolAttribute.append(xmlNodes2.toElement().text()) 
                xmlNodes2 = current.namedItem("valMagVar")
                if (xmlNodes2 != None):
                    symbolAttribute.append(xmlNodes2.toElement().text()) 
                xmlNodes2 = current.namedItem("dateMagVar")
                if (xmlNodes2 != None):
                    if len(symbolAttribute) > 6:
                        s = symbolAttribute[6]
                        symbolAttribute.pop(6)
                        symbolAttribute.append(s + " " + xmlNodes2.toElement().text())  
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text())       
                xmlNodes2 = current.namedItem("txtRmk")
                if (xmlNodes2 != None):
                    symbolAttribute.append(xmlNodes2.toElement().text()) 
                xmlNodes3 = current.namedItem("valElev")
                if (xmlNodes3 != None):
                    innerText = xmlNodes3.toElement().text()
                xmlNodes3 = current.namedItem("uomDistVer")
                if (xmlNodes3 != None):
                    str0 = xmlNodes3.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                symbolType = SymbolType.Vor
                
                xmlNodes2 = current.namedItem("codeType")
                codeTypeStr = xmlNodes2.toElement().text()
                if xmlNodes2 != None and codeTypeStr.count("DVOR") > 0:
                    symbolType = SymbolType.Vord
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, symbolType, "Vor", current])
#                 print self.pointData
            return True
#             except:
#                 return False
        return True
    
    def method_8(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
#             try:
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                altitude_metre = None
                xmlNodes = current.namedItem("TcnUid")
                xmlNodes1 = current.namedItem("VorUid")
                xmlNodes2 = current.namedItem("OrgUid")
                symbolAttribute.append(xmlNodes.namedItem("codeId").toElement().text())
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                xmlNodes3 = current.namedItem("valElev")
                if (xmlNodes3 != None):
                    innerText = xmlNodes3.toElement().text()
                xmlNodes3 = current.namedItem("uomDistVer")
                if (xmlNodes3 != None):
                    str0 = xmlNodes3.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                symbolAttribute.append(xmlNodes2.namedItem("txtName").toElement().text())
                xmlNodes3 = current.namedItem("codeChannel")
                if (xmlNodes3 != None and xmlNodes3.toElement().text() != ""):
                    symbolAttribute.append(Captions.CHANNEL_BIG + " " + xmlNodes3.toElement().text())
                if xmlNodes1 != None and xmlNodes1.toElement().text() != "":
                    sym5 = Captions.COLLOCATED_WITH + " " + symbolAttribute[0]
                    symbolAttribute.append(Captions.COLLOCATED_WITH + " " + symbolAttribute[0])
                    s = symbolAttribute[0]
                    symbolAttribute.pop(0)
                    symbolAttribute.insert(0, xmlNodes1.namedItem("codeId").toElement().text())
                    xmlNodes3 = current.namedItem("codeChannel")
                    if (xmlNodes3 != None and xmlNodes3.toElement().text() != ""):
                        symbolAttribute.append(Captions.CHANNEL_BIG + " " + xmlNodes3.toElement().text())
                    xmlNodes3 = current.namedItem("txtName")
                    if (xmlNodes3 != None):
                        symbolAttribute.append(xmlNodes3.toElement().text())

                    degreeStr = symbolAttribute[1]
                    degree1Str = symbolAttribute[2]
                    # DataBaseSymbols symbols = this.dataBase.Symbols
                    # SymbolType[] symbolTypeArray = new SymbolType[] { SymbolType.Vor }
                    dataRow = None
                    for pointData0 in self.pointData:
                        symbolType = pointData0[7]
                        if symbolType == SymbolType.Vor:
                            if degreeStr == pointData0[3] and degree1Str == pointData0[4]:
                                dataRow = pointData0
                                break
                    # DataRow dataRow = symbols.method_2(degree, degree1, symbolTypeArray)
                    if (dataRow != None):
                        dataRow[7] = SymbolType.Vortac
                        item = dataRow[6]
                        if (item == None):
                            continue
                        # item[5] = sym5
                        # item[6] = symbolAttribute[6]
                        # item[7] = symbolAttribute[7]
                        continue
                
                xmlNodes3 = current.namedItem("txtName")
                if (xmlNodes3 != None):
                    if len(symbolAttribute) > 5:
                        symbolAttribute.pop(5)
                        symbolAttribute.insert(5, xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text())
                xmlNodes3 = current.namedItem("valMagVar")
                if (xmlNodes3 != None):
                    if len(symbolAttribute) > 6:
                        symbolAttribute.pop(6)
                        symbolAttribute.insert(6, xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text())
                xmlNodes3 = current.namedItem("dateMagVar")
                if (xmlNodes3 != None):
                    if len(symbolAttribute) > 6:
                        s = symbolAttribute[6]
                        symbolAttribute.pop(6)
                        symbolAttribute.insert(6, s + " (" + xmlNodes3.toElement().text() + ")")
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text())
                xmlNodes3 = current.namedItem("txtRmk")
                if (xmlNodes3 != None):
                    if len(symbolAttribute) > 7:
                        symbolAttribute.pop(7)
                        symbolAttribute.insert(7, xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text())
                
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Tacan, "Tcn", current])
#                 print self.pointData
            return True
#             except:
#                 return False
        return True
    
    def method_9(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
#             try:
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                altitude_metre = None
                xmlNodes = current.namedItem("DmeUid")
                xmlNodes1 = current.namedItem("VorUid")
                xmlNodes2 = current.namedItem("OrgUid")
                symbolAttribute.append(xmlNodes.namedItem("codeId").toElement().text())
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                xmlNodes3 = current.namedItem("valElev")
                if (xmlNodes3 != None):
                    innerText = xmlNodes3.toElement().text()
                xmlNodes3 = current.namedItem("uomDistVer")
                if (xmlNodes3 != None):
                    str0 = xmlNodes3.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                symbolAttribute.append(xmlNodes2.namedItem("txtName").toElement().text())
                xmlNodes3 = current.namedItem("codeChannel")
                if (xmlNodes3 != None):
                    symbolAttribute.append(Captions.CHANNEL_BIG + " " + xmlNodes3.toElement().text())
                if xmlNodes1 != None and xmlNodes1.toElement().text() != "":
                    symbolAttribute.append(Captions.COLLOCATED_WITH + " " + symbolAttribute[0])
                    s = symbolAttribute[0]
                    symbolAttribute.pop(0)
                    symbolAttribute.insert(0, xmlNodes1.namedItem("codeId").toElement().text())
                    xmlNodes3 = current.namedItem("codeChannel")
                    if (xmlNodes3 != None and xmlNodes3.toElement().text() != ""):
                        symbolAttribute.append(Captions.CHANNEL_BIG + " " + xmlNodes3.toElement().text())
                    xmlNodes3 = current.namedItem("txtName")
                    if (xmlNodes3 != None):
                        symbolAttribute.append(xmlNodes3.toElement().text())
                
                xmlNodes3 = current.namedItem("txtName")
                if (xmlNodes3 != None):
                    if len(symbolAttribute) > 5:
                        symbolAttribute.pop(5)
                        symbolAttribute.insert(5, xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text())
                xmlNodes3 = current.namedItem("valMagVar")
                if (xmlNodes3 != None):
                    if len(symbolAttribute) > 6:
                        symbolAttribute.pop(6)
                        symbolAttribute.insert(6, xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text())
                xmlNodes3 = current.namedItem("dateMagVar")
                if (xmlNodes3 != None):
                    if len(symbolAttribute) > 6:
                        s = symbolAttribute[6]
                        symbolAttribute.pop(6)
                        symbolAttribute.insert(6, s + " (" + xmlNodes3.toElement().text() + ")")
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text())
                xmlNodes3 = current.namedItem("txtRmk")
                if (xmlNodes3 != None):
                    if len(symbolAttribute) > 7:
                        symbolAttribute.pop(7)
                        symbolAttribute.insert(7, xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text())
                
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Dme, "Dme", current])
#                 print self.pointData
            return True
#             except:
#                 return False
        return True
    def method_10(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                altitude_metre = None
                xmlNodes = current.namedItem("NdbUid")
                xmlNodes1 = current.namedItem("OrgUid")
                symbolAttribute.append(xmlNodes.namedItem("codeId").toElement().text())
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                xmlNodes3 = current.namedItem("valElev")
                if (xmlNodes3 != None):
                    innerText = xmlNodes3.toElement().text()
                xmlNodes3 = current.namedItem("uomDistVer")
                if (xmlNodes3 != None):
                    str0 = xmlNodes3.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                symbolAttribute.append(xmlNodes1.namedItem("txtName").toElement().text())
                xmlNodes2 = current.namedItem("valFreq")
                if (xmlNodes2 != None):
                    symbolAttribute.append(Captions.FREQUENCY_BIG + " " + xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("uomFreq")
                if (xmlNodes2 != None):
                    if len(symbolAttribute) > 4:
                        s = symbolAttribute[4]
                        symbolAttribute.pop(4)
                        symbolAttribute.append(s + " " + xmlNodes2.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("txtName")
                if (xmlNodes2 != None):
                    symbolAttribute.append(xmlNodes2.toElement().text())
                    
                xmlNodes2 = current.namedItem("valMagVar")
                if (xmlNodes2 != None):
                    symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("dateMagVar")
                if (xmlNodes2 != None):
                    if len(symbolAttribute) > 6:
                        s = symbolAttribute[6]
                        symbolAttribute.pop(6)
                        symbolAttribute.append(s + " " + xmlNodes2.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("txtRmk")
                if (xmlNodes2 != None):
                    symbolAttribute.append(xmlNodes2.toElement().text())
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Ndb, "Ndb", current])
#                 print self.pointData
            return True
        return True
    def method_11(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                altitude_metre = None
                xmlNodes = current.namedItem("MkrUid")
                xmlNodes1 = current.namedItem("OrgUid")
                symbolAttribute.append(xmlNodes.namedItem("codeId").toElement().text())
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                xmlNodes3 = current.namedItem("valElev")
                if (xmlNodes3 != None):
                    innerText = xmlNodes3.toElement().text()
                xmlNodes3 = current.namedItem("uomDistVer")
                if (xmlNodes3 != None):
                    str0 = xmlNodes3.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                symbolAttribute.append(xmlNodes1.namedItem("txtName").toElement().text())
                xmlNodes2 = current.namedItem("valFreq")
                if (xmlNodes2 != None):
                    symbolAttribute.append(Captions.FREQUENCY_BIG + " " + xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("uomFreq")
                if (xmlNodes2 != None):
                    if len(symbolAttribute) > 4:
                        s = symbolAttribute[4]
                        symbolAttribute.pop(4)
                        symbolAttribute.append(s + " " + xmlNodes2.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("txtName")
                if (xmlNodes2 != None):
                    symbolAttribute.append(xmlNodes2.toElement().text())
                    
                xmlNodes2 = current.namedItem("txtRmk")
                if (xmlNodes2 != None):
                    symbolAttribute.append(xmlNodes2.toElement().text())
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Be1, "Mkr", current])
#                 print self.pointData
            return True
        return True
    def method_12(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                altitude_metre = None
                xmlNodes = current.namedItem("SnsUid")
                xmlNodes1 = xmlNodes.namedItem("SnyUid")
                xmlNodes2 = current.namedItem("OrgUid")
                symbolAttribute.append(xmlNodes1.namedItem("codeId").toElement().text())
                symbolAttribute.append(str(Degrees.smethod_15(current.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(current.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                xmlNodes3 = current.namedItem("valElev")
                if (xmlNodes3 != None):
                    innerText = xmlNodes3.toElement().text()
                xmlNodes3 = current.namedItem("uomDistVer")
                if (xmlNodes3 != None):
                    str0 = xmlNodes3.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                symbolAttribute.append(xmlNodes2.namedItem("txtName").toElement().text())
                xmlNodes2 = current.namedItem("valFreq")
                if (xmlNodes2 != None):
                    symbolAttribute.append(Captions.FREQUENCY_BIG + " " + xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("uomFreq")
                if (xmlNodes2 != None):
                    if len(symbolAttribute) > 4:
                        s = symbolAttribute[4]
                        symbolAttribute.pop(4)
                        symbolAttribute.append(s + " " + xmlNodes2.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes2 = xmlNodes.namedItem("txtName")
                if (xmlNodes2 != None):
                    symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("codeTypeSer")
                if (xmlNodes2 != None):
                    symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("txtRmk")
                if (xmlNodes2 != None):
                    symbolAttribute.append(xmlNodes2.toElement().text())
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Gp, "Sns", current])
#                 print self.pointData
            return True
        return True
    def method_13(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                altitude_metre = None
                xmlNodes = current.namedItem("IlsUid").namedItem("RdnUid")
                xmlNodes1 = current.namedItem("Ilz")
                xmlNodes2 = current.namedItem("Igp")
                symbolAttribute.append(xmlNodes1.namedItem("codeId").toElement().text())
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes1.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes1.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))

                symbolAttribute.append(Captions.ILS_LOCALIZER_RWY_BIG + " " + xmlNodes.namedItem("txtDesig").toElement().text())
                symbolAttribute.append(Captions.CAT_BIG + " " + current.namedItem("codeCat").toElement().text())
                symbolAttribute.append(Captions.FREQUENCY_BIG + " " + xmlNodes1.namedItem("valFreq").toElement().text() + " " + xmlNodes1.namedItem("uomFreq").toElement().text())
                xmlNodes3 = xmlNodes1.namedItem("valElev")
                if (xmlNodes3 != None):
                    innerText = xmlNodes3.toElement().text()
                xmlNodes3 = xmlNodes1.namedItem("uomDistVer")
                if (xmlNodes3 != None):
                    str0 = xmlNodes3.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Gp, "Ils", current])
                
                symbolAttribute = []
                if xmlNodes2.isNull():
                    continue
                symbolAttribute.append(Captions.ILS_GP_RWY_BIG + " " + xmlNodes.namedItem("txtDesig").toElement().text())
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes2.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes2.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                
                symbolAttribute.append(Captions.CAT_BIG + " " + current.namedItem("codeCat").toElement().text())
                symbolAttribute.append(Captions.FREQUENCY_BIG + " " + xmlNodes2.namedItem("valFreq").toElement().text() + " " + xmlNodes2.namedItem("uomFreq").toElement().text())
                xmlNodes3 = xmlNodes2.namedItem("valSlope")
                if (xmlNodes3 != None):
                    symbolAttribute.append(Captions.SLOPE + " " + xmlNodes3.toElement().text())
                xmlNodes3 = xmlNodes2.namedItem("valRdh")
                if (xmlNodes3 != None):
                    symbolAttribute.append(Captions.RDH + " " + xmlNodes3.toElement().text())
                xmlNodes3 = xmlNodes2.namedItem("uomRdh")
                if (xmlNodes3 != None):
                    if len(symbolAttribute) > 6:
                        s = symbolAttribute[6]
                        symbolAttribute.pop(6)
                        symbolAttribute.append(s + " " + xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes3 = xmlNodes2.namedItem("valElev")
                if (xmlNodes3 != None):
                    innerText = xmlNodes3.toElement().text()
                xmlNodes3 = xmlNodes2.namedItem("uomDistVer")
                if (xmlNodes3 != None):
                    str0 = xmlNodes3.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Gp, "Ils", current])
            return True
        return True   
    def method_14(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count = xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                altitude_metre = None 
                
                xmlNodes = current.namedItem("MlsUid").namedItem("RdnUid")
                current.namedItem("DmeUid")
                xmlNodes1 = current.namedItem("Men")
                symbolAttribute.append(Captions.MLS_ELEVATION_RWY_BIG + " " + xmlNodes.namedItem("txtDesig").toElement().text())
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes1.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes1.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                symbolAttribute.append(Captions.CAT_BIG + " " + current.namedItem("codeCat").toElement().text())
                symbolAttribute.append(Captions.CHANNEL_BIG + " " + current.namedItem("codeChannel").toElement().text())
                xmlNodes2 = xmlNodes1.namedItem("valAngleNml")
                if (xmlNodes2 != None):
                    symbolAttribute.append(Captions.NOMINAL_ANGLE_BIG + " " + xmlNodes2.toElement().text())
                xmlNodes2 = xmlNodes1.namedItem("valAngleMnm")
                if (xmlNodes2 != None):
                    symbolAttribute.append(Captions.MINIMAL_ANGLE_BIG + " " + xmlNodes2.toElement().text())
                xmlNodes2 = xmlNodes1.namedItem("valAngleSpan")
                if (xmlNodes2 != None):
                    symbolAttribute.append(Captions.ANGLE_SPAN_BIG + " " + xmlNodes2.toElement().text())
                xmlNodes2 = xmlNodes1.namedItem("valElev")
                if (xmlNodes2 != None):
                    innerText = xmlNodes2.toElement().text()
                xmlNodes2 = xmlNodes1.namedItem("uomDistVer")
                if (xmlNodes2 != None):
                    str0 = xmlNodes2.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Gp, "Mls", current])
                
                
                current1_List = current.childNodes()
                for current1 in current1_List:
                    if (current1.nodeName() != "Mah"):
                        continue
                    symbolAttribute = []
                    symbolAttribute.append(Captions.MLS_AZIMUTH_RWY_BIG + " " + xmlNodes.namedItem("txtDesig").toElement().text())
                    symbolAttribute.append(str(Degrees.smethod_15(current1.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                    symbolAttribute.append(str(Degrees.smethod_15(current1.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                    symbolAttribute.append(Captions.CODE_TYPE_BIG + " " + current1.namedItem("codeType").toElement().text())
                    xmlNodes2 = current1.namedItem("valAnglePropLeft")
                    if (xmlNodes2 != None):
                        symbolAttribute.append(Captions.LEFT_ANGLE_OF_PROPORTIONALITY_BIG + " " + xmlNodes2.toElement().text())
                    xmlNodes2 = current1.namedItem("valAnglePropRight")
                    if (xmlNodes2 != None):
                        symbolAttribute.append(Captions.RIGHT_ANGLE_OF_PROPORTIONALITY_BIG + " " + xmlNodes2.toElement().text())
                    
                    xmlNodes2 = current1.namedItem("valAngleCoverLeft")
                    if (xmlNodes2 != None):
                        symbolAttribute.append(Captions.LEFT_ANGLE_OF_COVERAGE_BIG + " " + xmlNodes2.toElement().text())
                    
                    xmlNodes2 = current1.namedItem("valAngleCoverRight")
                    if (xmlNodes2 != None):
                        symbolAttribute.append(Captions.RIGHT_ANGLE_OF_COVERAGE_BIG + " " + xmlNodes2.toElement().text())
                    
                    xmlNodes2 = xmlNodes1.namedItem("valElev")
                    if (xmlNodes2 != None):
                        innerText = xmlNodes2.toElement().text()
                    xmlNodes2 = xmlNodes1.namedItem("uomDistVer")
                    if (xmlNodes2 != None):
                        str0 = xmlNodes2.toElement().text()
                    if innerText != None and innerText != "":
                        if str0 == "FT":
                            altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                        elif str0 == "M":
                            altitude_metre = innerText
                    else:
                        altitude_metre = "0.0"
                        
                    attr = ""
                    for n in range(3, len(symbolAttribute)):
                        if len(attr) > 0:
                            attr += ", "
                        attr += symbolAttribute[n]
                    self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Gp, "Mls", current])
#                 return True
            return True
        return True
    def method_15(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None
                str0 = None
                altitude_metre = None
                xmlNodes = current.namedItem("ObsUid")
                xmlNodes1 = current.namedItem("txtName")
                
                if (xmlNodes1 == None):
                    symbolAttribute.append(Captions.OBS)
                else:
                    symbolAttribute.append(xmlNodes1.toElement().text())
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                
                innerText1 = current.namedItem("codeGroup").toElement().text()
                str1 = current.namedItem("codeLgt").toElement().text()
                xmlNodes1 = current.namedItem("txtDescrType")
                if (xmlNodes1 != None):
                    symbolAttribute.append(xmlNodes1.toElement().text())
                xmlNodes1 = current.namedItem("txtRmk")
                if (xmlNodes1 != None):
                    symbolAttribute.append(xmlNodes1.toElement().text())
                    
                xmlNodes2 = current.namedItem("valElev")
                if (xmlNodes2 != None):
                    innerText = xmlNodes2.toElement().text()
                xmlNodes2 = current.namedItem("uomDistVer")
                if (xmlNodes2 != None):
                    str0 = xmlNodes2.toElement().text()
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                symbolAttribute.append(Captions.VERTICAL_UNITS_BIG + " " + str0)
                symbolAttribute.append(innerText)
                xmlNodes1 = current.namedItem("valHgt")
                if (xmlNodes1 != None):
                    symbolAttribute.append(xmlNodes1.toElement().text())
                attr = ""
                for j in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[j]
                symbolType = SymbolType.Obst1
                if innerText1.count("Y") > 0 and str1.count("Y"):
                    symbolType = SymbolType.Obst4
                elif innerText1.count("Y") > 0:
                    symbolType = SymbolType.Obst3
                elif str1.count("Y") > 0:
                    symbolType = SymbolType.Obst2
                self.pointDataObstacles.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, symbolType, "Obs", current])
            return True
        return True
    
    def method_16(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            strArrays = ["TcnUidSta", "VorUidSta", "DpnUidSta", "NdbUidSta", "DmeUidSta", "MkrUidSta"]
            strArrays1 = strArrays
            strArrays2 = ["TcnUidEnd", "VorUidEnd", "DpnUidEnd", "NdbUidEnd", "DmeUidEnd", "MkrUidEnd"]
            strArrays3 = strArrays2
            
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                
                xmlNodes = current.namedItem("RsgUid")
                xmlNodes1 = xmlNodes.namedItem("RteUid")
                nodes = xmlNodes.childNodes()
#                 n = nodes.count()
                itemOf = nodes.item(1)
                if (not self.listComp(itemOf.nodeName(), strArrays1)):
                    continue
                itemOf1 = nodes.item(2)
                if (not self.listComp(itemOf1.nodeName(), strArrays3)):
                    continue
                str0 = xmlNodes1.namedItem("txtDesig").toElement().text() + " " + xmlNodes1.namedItem("txtLocDesig").toElement().text()
                symbolAttribute = []
                symbolAttribute.append(str0)
                symbolAttribute.append(str(Degrees.smethod_15(itemOf.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                symbolAttribute.append(str(Degrees.smethod_15(itemOf.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                
                degree = Degrees.smethod_15(itemOf.namedItem("geoLat").toElement().text(), DegreesType.Latitude)
                degree1 = Degrees.smethod_15(itemOf.namedItem("geoLong").toElement().text(), DegreesType.Longitude)
                
                symbolAttribute.append(itemOf.namedItem("codeId").toElement().text())
#                 Degrees degree = Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude, self.formatProvider)
#                 Degrees degree1 = Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude, self.formatProvider)
                innerText = []
                innerText.append(str0)
                innerText.append(str(Degrees.smethod_15(itemOf1.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value))
                innerText.append(str(Degrees.smethod_15(itemOf1.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value))
                
                degree2 = Degrees.smethod_15(itemOf1.namedItem("geoLat").toElement().text(), DegreesType.Latitude)
                degree3 = Degrees.smethod_15(itemOf1.namedItem("geoLong").toElement().text(), DegreesType.Longitude)
                
                innerText.append(itemOf1.namedItem("codeId").toElement().text())
                routList = []
                dataBaseCoordinate = DataBaseCoordinates("Segments")
                dataBaseCoordinate.method_0(degree, degree1, Altitude.NaN(), DataBaseCoordinateType.Point, symbolAttribute)
                dataBaseCoordinate.method_0(degree2, degree3, Altitude.NaN(), DataBaseCoordinateType.Point, innerText)
#                 routList.append([symbolAttribute[1], symbolAttribute[2], symbolAttribute[3]])
#                 routList.append([innerText[1], innerText[2], innerText[3]])
                self.pointDataRoutes.append([str0, dataBaseCoordinate, "Rsg", current])
            return True
        return True
    def method_17(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                
                xmlNodes = current.namedItem("AseUid")
                str0 = xmlNodes.namedItem("codeId").toElement().text() + " (" +  xmlNodes.namedItem("codeType").toElement().text() + ")"
                naN = None
                xmlNodes1 = current.namedItem("valDistVerLower")
                if (xmlNodes1 != None):
                    naN = Altitude.smethod_4(xmlNodes1.toElement().text(), current.namedItem("uomDistVerLower").toElement().text())
                altitude = None
                xmlNodes1 = current.namedItem("valDistVerUpper")
                if (xmlNodes1 != None):
                    altitude = Altitude.smethod_4(xmlNodes1.toElement().text(), current.namedItem("uomDistVerUpper").toElement().text())
                dataRow, rowIndex = self.airspaceMethod2(str0)
                if (dataRow == None):
                    if naN == None:
                        naN = Altitude(0)
                    if altitude == None:
                        altitude = Altitude(0)
                    self.pointDataAirspace.append([str0, str(naN.Metres), str(altitude.Metres), None, "True", "True", [], "Ase", current])
#                     self.dataBase.method_6(str, naN, altitude, Distance.NaN, true, true, null)
                else:
                    if (naN.IsValid()):
                        dataRow.pop(1)
                        dataRow.insert(1, str(naN.Metres))
#                         dataRow["LowerLimit"] = naN
#                     }
                    if (altitude.IsValid()):
                        dataRow.pop(2)
                        dataRow.insert(2, str(altitude.Metres))
#                         dataRow["UpperLimit"] = altitude
#                     }
                    
                    dataRow.pop(4)
                    dataRow.insert(4, "True")
                    item = dataRow[6]
                    if len(item) == 0:
                        self.pointDataAirspace.pop(rowIndex)
                        self.pointDataAirspace.insert(rowIndex, dataRow)
                        continue
                    for dataBaseCoordinate in item:
                        if dataBaseCoordinate.attributes == None:
                            continue
                        if (naN.IsValid()):
                            dataBaseCoordinate.set_attribute(4,  Captions.LOWER_LIMIT_BIG + " " + str(naN.Metres))
                        if (not altitude.IsValid()):
                            continue
                        dataBaseCoordinate.set_attribute(5, Captions.UPPER_LIMIT_BIG + " " + str(altitude.Metres))
#                     dataRow.pop(6)
#                     self.pointDataAirspace.insert(rowIndex, dataRow)
                    self.pointDataAirspace.pop(rowIndex)
                    self.pointDataAirspace.insert(rowIndex, dataRow)
            return True
        return True
    
    def method_18(self, xmlNodeList_0):
        flag = False
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                
                xmlNodes = current.namedItem("AbdUid").namedItem("AseUid")
                str0 = xmlNodes.namedItem("codeId").toElement().text() + " (" + xmlNodes.namedItem("codeType").toElement().text() + ")"
                symbolAttribute = SymbolAttributes()
                
                symbolAttribute.pop(0)
                symbolAttribute.insert(0, str0)
                
                dataRow, rowIndex = self.airspaceMethod2(str0)
                if (dataRow != None):
                    item = Altitude(float(dataRow[1]))
                    altitude = Altitude(float(dataRow[2]))
                    if (item.IsValid()):
                        symbolAttribute.pop(4)
                        symbolAttribute.insert(4, Captions.LOWER_LIMIT_BIG + " " + str(item.Metres))
                    if (altitude.IsValid()):
                        symbolAttribute.pop(5)
                        symbolAttribute.insert(5, Captions.UPPER_LIMIT_BIG + " " + str(altitude.Metres))
                
                xmlNodes1 = current.namedItem("Circle")
                if xmlNodes1.isNull():
                    flag1 = False
                    dataBaseCoordinate = DataBaseCoordinates("Vertices")
                    nodes = current.childNodes()
                    for j in range(nodes.count()):
                        current1 = nodes.item(j)
                        name = current1.nodeName()
                        if not name.count("Avx") > 0: 
                            continue
                        innerText = current1.namedItem("codeType").toElement().text()
                        if innerText.count("CIR") > 0:
                            xmlNodes2 = current1.namedItem("geoLatArc")
                            xmlNodes3 = current1.namedItem("geoLongArc")
                            if (xmlNodes2 == None or xmlNodes3 == None):
                                symbolAttribute.pop(1)
                                symbolAttribute.insert(1, current1.namedItem("geoLat").toElement().text())
                                symbolAttribute.pop(2)
                                symbolAttribute.insert(2, current1.namedItem("geoLong").toElement().text())
#                 
#                                 symbolAttribute.append(current1.namedItem("geoLat").toElement().text())
#                                 symbolAttribute[2] = current1.SelectSingleNode("geoLong").toElement().text()
                            else:
                                symbolAttribute.pop(1)
                                symbolAttribute.insert(1, xmlNodes2.toElement().text())
                                symbolAttribute.pop(2)
                                symbolAttribute.insert(2, xmlNodes3.toElement().text())
# #                 
#                                 symbolAttribute[1] = xmlNodes2.InnerText
#                                 symbolAttribute[2] = xmlNodes3.InnerText
                            degree = Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude)
                            degree1 = Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude)
                            xmlNodes2 = current1.namedItem("valRadiusArc")
                            xmlNodes3 = current1.namedItem("uomRadiusArc")
                            if (xmlNodes2 == None or xmlNodes3 == None):
                                flag1 = True
                                break
                            else:
                                distance = Distance.smethod_7(xmlNodes2.toElement().text(), xmlNodes3.toElement().text())
                                symbolAttribute.pop(3)
                                symbolAttribute.insert(3, Captions.RADIUS_BIG + "" + str(distance.Metres))
                                dataBaseCoordinate.method_0(degree, degree1, Altitude.NaN, DataBaseCoordinateType.CenPoint, symbolAttribute)
                                
                                if (dataRow == None):
                                    self.pointDataAirspace.append([str0, None, None, distance, "False", "False", dataBaseCoordinate, "Abd", current])
                                else:
                                    dataRow.pop(3)
                                    dataRow.insert(3, str(distance.Metres))
                                    dataRow.pop(6)
                                    dataRow.insert(6, dataBaseCoordinate)
                                    
                                    self.pointDataAirspace.pop(rowIndex)
                                    self.pointDataAirspace.insert(rowIndex, dataRow)
                                flag1 = True
                                break
                        else:
                            naN = None
                            naN1 = None
                            symbolAttribute.pop(1)
                            symbolAttribute.insert(1, current1.namedItem("geoLat").toElement().text())
                            symbolAttribute.pop(2)
                            symbolAttribute.insert(2, current1.namedItem("geoLong").toElement().text())
                            degree2 = Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude)
                            degree3 = Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude)
                            dataBaseCoordinateType = DataBaseCoordinateType.GRC
                            if (innerText.count("FNT") > 0):
                                dataBaseCoordinateType = DataBaseCoordinateType.FNT
                            elif (innerText.count("CCA") > 0):
                                dataBaseCoordinateType = DataBaseCoordinateType.CCA
                            elif (innerText.count("CWA")>0):
                                dataBaseCoordinateType = DataBaseCoordinateType.CWA
                            if (dataBaseCoordinateType == DataBaseCoordinateType.CCA or dataBaseCoordinateType == DataBaseCoordinateType.CWA):
                                try:
                                    symbolAttribute.pop(6)
                                    symbolAttribute.insert(6, current1.namedItem("geoLatArc").toElement().text())
                                    symbolAttribute.pop(7)
                                    symbolAttribute.insert(7, current1.namedItem("geoLongArc").toElement().text())
                                    naN = Degrees.smethod_15(symbolAttribute[6], DegreesType.Latitude)
                                    naN1 = Degrees.smethod_15(symbolAttribute[7], DegreesType.Longitude)
                                    sss = symbolAttribute[6]
                                    symbolAttribute.pop(6)
                                    symbolAttribute.insert(6, Captions.CENTER_LATITUDE_BIG + " " + sss)
                                    sss = symbolAttribute[7]
                                    symbolAttribute.pop(7)
                                    symbolAttribute.insert(7, Captions.CENTER_LONGITUDE_BIG + " " + sss)
                                except:
                                    dataBaseCoordinateType = DataBaseCoordinateType.GRC
                                    
                                    symbolAttribute.pop(6)
                                    symbolAttribute.insert(6, "")
                                    symbolAttribute.pop(7)
                                    symbolAttribute.insert(7, "")
                                    naN = None
                                    naN1 = None
                            dataBaseCoordinate.method_3(None, None, degree2, degree3, None, naN, naN1, dataBaseCoordinateType, symbolAttribute)
                    if (flag1):
                        continue
                    if (dataRow == None):
                        self.pointDataAirspace.append([str0, None, None, None, "False", "False", dataBaseCoordinate, "Abd", current])
                    else:
                        dataRow.pop(6)
                        dataRow.insert(6, dataBaseCoordinate)
                        self.pointDataAirspace.pop(rowIndex)
                        self.pointDataAirspace.insert(rowIndex, dataRow)
                else:
                    symbolAttribute.pop(1)
                    symbolAttribute.insert(1, xmlNodes1.namedItem("geoLatCen").toElement().text())
                    symbolAttribute.pop(2)
                    symbolAttribute.insert(2, xmlNodes1.namedItem("geoLongCen").toElement().text())
                    degree4 = Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude)
                    degree5 = Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude)
                    distance1 = Distance.smethod_7(xmlNodes1.namedItem("valRadius").toElement().text(), xmlNodes1.namedItem("uomRadius").toElement().text())
                    symbolAttribute.pop(3)
                    symbolAttribute.insert(3, Captions.RADIUS_BIG + " " + str(distance1.Metres))
                    dataBaseCoordinate1 = DataBaseCoordinates("Vertices")
                    dataBaseCoordinate1.method_0(degree4, degree5, None, "CenPoint", symbolAttribute)
                    if (dataRow == None):
                        self.pointDataAirspace.append([str0, None, None, str(distance1.Metres), "False", "False", dataBaseCoordinate1, "Abd", current])
                    else:
                        dataRow.pop(3)
                        dataRow.insert(3, str(distance1.Metres))
                        dataRow.pop(6)
                        dataRow.insert(6, dataBaseCoordinate1)
                        self.pointDataAirspace.pop(rowIndex)
                        self.pointDataAirspace.insert(rowIndex, dataRow)
                
            self.airspaceMethod3()
            return True
        return True
    def method_19(self, xmlNodeList_0):
        flag = None
        if (xmlNodeList_0 != None):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                xmlNodes = current.namedItem("GbrUid")
                innerText = xmlNodes.namedItem("txtName").toElement().text()
                dataBaseGeoBorderType = current.namedItem("codeType").toElement().text()
                dataBaseCoordinate = DataBaseCoordinates("Vertices")
                nodes = current.childNodes()
                for j in range(nodes.count()):
                    current1 = nodes.item(j)
                    if current1.nodeName() != "Gbv":
                        continue
#                 for current1 in current.namedItem("Gbv"):
                    symbolAttribute = SymbolAttributes()
                    symbolAttribute.pop(0)
                    symbolAttribute.insert(0,innerText)
                    symbolAttribute.pop(1)
                    symbolAttribute.insert(1,current1.namedItem("geoLat").toElement().text())
                    symbolAttribute.pop(2)
                    symbolAttribute.insert(2,current1.namedItem("geoLong").toElement().text())
                    symbolAttribute.pop(3)
                    symbolAttribute.insert(3,dataBaseGeoBorderType)
                    degree = Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude)
                    degree1 = Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude)
                    dataBaseCoordinate.method_0(degree, degree1, None, DataBaseCoordinateType.GRC, symbolAttribute)
                self.pointDataBorder.append([innerText, dataBaseGeoBorderType, dataBaseCoordinate, "Gbr", current])
            return True
        return True
    def method_20(self, domNodeList):
        pass
        
    def findNodes(self, domNodeList, findedStr):
        count = domNodeList.count()
        resultIndex = []
        for i in range(count):
            node = domNodeList.item(i)
            name = node.nodeName()
            if name.contains(findedStr):
                resultIndex.append(i)
        return resultIndex
    def listComp(self, str0, strArray):
        for str1 in strArray:
            if str0 == str1:
                return True
        return False
        
    def airspaceMethod2(self, str0):
        if len(self.pointDataAirspace) == 0:
            return (None, 0)
        i = 0
        for airspace in self.pointDataAirspace:
            if airspace[0].count(str0) > 0:
                return (airspace, i)
            i += 1
            
        return (None, 0)
    def airspaceMethod3(self):
        num = 0
        numList = []
        if len(self.pointDataAirspace) > 0:
            flag = False
            i = 0
            while not flag:
                
                if i == len(self.pointDataAirspace):
                    flag = True
                    continue
                dataBaseCoordinate = self.pointDataAirspace[i][6]    
                if dataBaseCoordinate == None or len(dataBaseCoordinate) == 0:
                    self.pointDataAirspace.pop(i)
                    continue
                i += 1
#             for item in self.pointDataAirspace:
#                 dataBaseCoordinate = item[6]
#                 if dataBaseCoordinate == None or len(dataBaseCoordinate) == 0:
# #                     numList.append(num)
# #                     num += 1
#                     self.pointDataAirspace.pop(self.pointDataAirspace.index(item))
#                     self.pointDataAirspace.remove(item)
#             for i in numList:
#                 self.pointDataAirspace.pop(i)
            
#         return None
                 
#         XmlDocument xmlDocument = new XmlDocument()
#         xmlDocument.Load(self.dataBase.FileName)
#         XmlNode xmlNodes = xmlDocument.namedItem("AIXM-Snapshot")
    
class Degrees:
    def __init__(self, double_0, double_1 = None, double_2 = None, degreesType_0 = None):
        self.value = None
        self.type = None
        
        if double_0 == None and double_1 == None and double_2 == None:
            self.value = None
            self.type = DegreesType.Degrees
            self.method_0()
            return
        if double_1 == None and double_2 == None and degreesType_0 == None:
            self.value = double_0
            self.type = DegreesType.Degrees
            self.method_0()
            return
        if double_2 == None and degreesType_0 == None:
            self.value = double_0 + double_1 / 60
            self.type = DegreesType.Degrees
            self.method_0()
            return
        if degreesType_0 == None:
            self.value = double_0 + double_1 / 60 + double_2 / 3600
            self.type = DegreesType.Degrees
            self.method_0()
            return
        if double_1 == None and double_2 == None:
            self.value = double_0
            self.type = degreesType_0
            self.method_0() 
            return
        if double_2 == None:
            self.value =  double_0 + double_1 / 60
            self.type = degreesType_0
            self.method_0()
            return
        
        self.value =  double_0 + double_1 / 60 + double_2 / 3600
        self.type = degreesType_0
        self.method_0()
        pass
    
    def method_0(self):
#         switch (self.type)
#     {
        if self.type == DegreesType.Latitude:
            if (self.value >= -90 and self.value <= 90):
                return
            raise ValueError("ERR_LATITUDE_OUT_OF_BOUNDS")
#             throw new Exception(string.Format(Messages.ERR_LATITUDE_OUT_OF_BOUNDS, self.value))
        elif self.type == DegreesType.Longitude:
            if (self.value >= -180 and self.value <= 180):
                return
            raise ValueError("ERR_LONGITUDE_OUT_OF_BOUNDS")
#             throw new Exception(string.Format(Messages.ERR_LONGITUDE_OUT_OF_BOUNDS, self.value))
        elif self.type == DegreesType.Variation:
            if (self.value >= -180 and self.value <= 180):
                return
            raise ValueError("ERR_VARIATION_OUT_OF_BOUNDS")
#             throw new Exception(string.Format(Messages.ERR_VARIATION_OUT_OF_BOUNDS, self.value))
    @staticmethod
    def String2Degree(qStr):
        qStr = String.Str2QString(qStr)
        degreeFormat = qStr.right(1)
        existFormat = False
        tempDegreeStr = None
        if degreeFormat == "E" or degreeFormat == "W" or\
           degreeFormat == "e" or degreeFormat == "w" or\
           degreeFormat == "N" or degreeFormat == "S" or\
           degreeFormat == "n" or degreeFormat == "s":
            existFormat = True
        if existFormat:
            tempDegreeStr = qStr.left(qStr.length() - 1)
        else:
            tempDegreeStr = qStr
        tempDegreeFloat = None
        try:
            tempDegreeFloat = float(tempDegreeStr)
        except:
            return None
        ssDecimal = tempDegreeFloat - int(tempDegreeFloat)
        degreeQStrWithOutDecimal = QString(str(int(tempDegreeFloat)))
        ssInt = int(degreeQStrWithOutDecimal.right(2))
        degreeQStrWithOutDecimal = degreeQStrWithOutDecimal.left(degreeQStrWithOutDecimal.length() - 2)
        mmInt = int(degreeQStrWithOutDecimal.right(2))
        degreeQStrWithOutDecimal = degreeQStrWithOutDecimal.left(degreeQStrWithOutDecimal.length() - 2)
        ddInt = int(degreeQStrWithOutDecimal)

        decimaldegree = ddInt + float(mmInt) / 60 + float(ssInt + ssDecimal) / 3600

        if degreeFormat == "E" or degreeFormat == "W" or\
           degreeFormat == "e" or degreeFormat == "w":
            return Degrees(decimaldegree, None, None, DegreesType.Longitude)
        elif degreeFormat == "N" or degreeFormat == "S" or\
             degreeFormat == "n" or degreeFormat == "s":
            return Degrees(decimaldegree, None, None, DegreesType.Latitude)
        return Degrees(decimaldegree)
    @staticmethod
    def smethod_12(degreesStyle_0, degreesStyle_1):
        return (degreesStyle_0 & degreesStyle_1) == degreesStyle_1
    @staticmethod
    def smethod_15(string_0, degreesType_0):
#         string_0 = "11223"  
#         s = "fsafs"
#         s.      
        num = string_0.indexOf('.')
        if (num == -1):
            num = string_0.indexOf("N")
        if (num == -1):
            num = string_0.indexOf("S")
        if (num == -1):
            num = string_0.indexOf("E")
        if (num == -1):
            num = string_0.indexOf("W")
        if (num == -1):
            num = string_0.indexOf("n")
        if (num == -1):
            num = string_0.indexOf("s")
        if (num == -1):
            num = string_0.indexOf("e")
        if (num == -1):
            num = string_0.indexOf("w")
#         try
#         {
        str0 = string_0[:num]
        degreesStyle = None
#         DegreesStyle degreesStyle = DegreesStyle.Degrees
        if (degreesType_0 == DegreesType.Latitude):
            if (str0.size() == 6):
                degreesStyle = DegreesStyle.DegreesMinutesSeconds
            elif (str0.size() == 4):
                degreesStyle = DegreesStyle.DegreesMinutes
            elif (str0.size() != 2):
                raise ValueError("NOT_VALID_LATITUDE_VALUE")
#                 throw new Exception(string.Format(Validations.NOT_VALID_LATITUDE_VALUE, string_0))
        elif (str0.size() == 7):
            degreesStyle = DegreesStyle.DegreesMinutesSeconds
        elif (str0.size() == 5):
            degreesStyle = DegreesStyle.DegreesMinutes
        elif (str0.size() != 3):
            raise ValueError("NOT_VALID_LONGITUDE_VALUE")
#             throw new Exception(string.Format(Validations.NOT_VALID_LONGITUDE_VALUE, string_0))
        degree = Degrees.smethod_17(string_0, degreesType_0, degreesStyle)
#         if (degree == None):
#             switch (degreesType_0)
#             {
#                 case DegreesType.Degrees:
#                 {
#                     throw new Exception(string.Format(Validations.NOT_VALID_DEGREES_VALUE, string_0))
#                 }
#                 case DegreesType.Latitude:
#                 {
#                     throw new Exception(string.Format(Validations.NOT_VALID_LATITUDE_VALUE, string_0))
#                 }
#                 case DegreesType.Longitude:
#                 {
#                     throw new Exception(string.Format(Validations.NOT_VALID_LONGITUDE_VALUE, string_0))
#                 }
#                 case DegreesType.Variation:
#                 {
#                     throw new Exception(string.Format(Validations.NOT_VALID_MAGNETIC_VARIATION_VALUE, string_0))
#                 }
#                 default:
#                 {
#                     throw new Exception(Messages.ERR_INVALID_DEGREES_TYPE)
#                 }
#             }
#         }
#     }
#         catch
#         {
#             throw
#         }
        return degree
#         pass
    @staticmethod
    def smethod_17(string_0, degreesType_0, degreesStyle_0):
        num = None
        num1 = None
        num2 = None
        num3 = None
        num4 = None
        flag = False
#         numberStyle = NumberStyles.Float
        degrees_0 = Degrees(None, None, None, degreesType_0)
        try:
            string_0 = string_0.toUpper()
            num5 = 1
            if (string_0.contains("+")):
                string_0 = string_0.replace("+", "")
            if (string_0.contains("-")):
                string_0 = string_0.replace("-", "")
                num5 = -1
            if (string_0.contains("N")):
                string_0 = string_0.replace("N", "")
            if (string_0.contains("E")):
                string_0 = string_0.replace("E", "")
            if (string_0.contains("S")):
                string_0 = string_0.replace("S", "")
                num5 = -1
            if (string_0.contains("W")):
                string_0 = string_0.replace("W", "")
                num5 = -1
            if (not Degrees.smethod_12(degreesStyle_0, DegreesStyle.DelimitedBySpace)):
                string_0 = string_0.replace(" ", "")
            string_0 = string_0.trimmed()
            if (Degrees.smethod_12(degreesStyle_0, DegreesStyle.Degrees)):
                try:
                    num, result = string_0.toDouble()
#                 if (double.TryParse(string_0, numberStyle, iformatProvider_0, out num)):
#                     degrees_0 = math.fabs(num) * num5
                    degrees_0 =  Degrees(math.fabs(num) * num5, None, None, degreesType_0)
                    flag = degrees_0
                    return flag
                except:
                    return None
            elif (Degrees.smethod_12(degreesStyle_0, DegreesStyle.DegreesMinutes)):
                if (Degrees.smethod_12(degreesStyle_0, DegreesStyle.DelimitedBySpace)):
                    strArrays = string_0.split(" ".ToCharArray())
                    if (string_0.size() < 2):
                        flag = None
                        return flag
#                     elif (!double.TryParse(strArrays[0], numberStyle, iformatProvider_0, out num))
# #                     {
# #                         flag = false
# #                         return flag
# #                     }
                    else:
                        try:
                            degrees_0 = Degrees(math.fabs(num) * num5, math.fabs(num1) * num5, None, degreesType_0)
                        except:
                            flag = None
                            return False
#                     else
#                     {
#                         flag = false
#                         return flag
#                     }
#                 }
                else:
                    try:
                        num3, result = string_0.toDouble()
        #                 {
                        num3 = math.fabs(num3) / 100
                        num1 = (num3 - math.trunc(num3)) * 100
                        num = math.trunc(num3)
                        degrees_0 = Degrees(num * num5, num1 * num5, None, degreesType_0)
                    except:
                        flag = None
                        return flag
                flag = degrees_0
                return flag
#                 }
#                 else
#                 {
#                     flag = false
#                     return flag
#                 }
#                 flag = true
#                 return flag
#             }
            elif (Degrees.smethod_12(degreesStyle_0, DegreesStyle.DegreesMinutesSeconds)):
                if (Degrees.smethod_12(degreesStyle_0, DegreesStyle.DelimitedBySpace)):
#                     string[] strArrays1 = string_0.Split(" ".ToCharArray())
#                     if ((int)strArrays1.Length < 3)
#                     {
#                         flag = false
#                         return flag
#                     }
#                     else if (!double.TryParse(strArrays1[0], numberStyle, iformatProvider_0, out num))
#                     {
#                         flag = false
#                         return flag
#                     }
#                     else if (!double.TryParse(strArrays1[1], numberStyle, iformatProvider_0, out num1))
#                     {
#                         flag = false
#                         return flag
#                     }
#                     else if (double.TryParse(strArrays1[2], numberStyle, iformatProvider_0, out num2))
#                     {
                    try:
                        degrees_0 = Degrees(math.fabs(num) * num5, math.fabs(num1) * num5, math.fabs(num2) * num5, degreesType_0)
                    except:
                        flag = None
                        return flag
#                     }
#                 }
                else:
                    try:
                        num4, result = string_0.toDouble()
                        num4 = math.fabs(num4) / 100
                        num2 = (num4 - math.trunc(num4)) * 100
                        num4 = float(math.trunc(num4)) / 100
                        num1 = (num4 - math.trunc(num4)) * 100
                        num = math.trunc(num4)
                        degrees_0 = Degrees(num * num5, num1 * num5, num2 * num5, degreesType_0)
                    except:
                        flag = None
                        return flag
#                 }
                flag = degrees_0
                return flag
#             }
#             return false
#         }
#         catch (Exception exception)
        except:
            return None
#         {
#             return false
#         }
        return flag
class DataBaseCoordinate:
    def __init__(self, double_0 = None, double_1 = None, degrees_0 = None, degrees_1 = None, altitude_0 = None, degrees_2 = None, degrees_3 = None, dataBaseCoordinateType_0 = None, symbolAttributes_0 = None):
        self.x = None
        self.y = None
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.centerLatitude = None
        self.centerLongitude = None
        self.type = None
        self.attributes = None
        self.variation = None
        if double_0 == None and double_1 == None and degrees_2 == None and degrees_3 == None:
            self.latitude = degrees_0
            self.longitude = degrees_1
            self.altitude = altitude_0
            self.type = dataBaseCoordinateType_0
            self.attributes = symbolAttributes_0
        elif degrees_2 == None and degrees_3 == None:
            self.x = double_0
            self.y = double_1
            self.latitude = degrees_0
            self.longitude = degrees_1
            self.altitude = altitude_0
            self.type = dataBaseCoordinateType_0
            self.attributes = symbolAttributes_0
        elif degrees_3 == None:
            self.x = double_0
            self.y = double_1
            self.latitude = degrees_0
            self.longitude = degrees_1
            self.altitude = altitude_0
            self.variation = degrees_2
            self.type = dataBaseCoordinateType_0
            self.attributes = symbolAttributes_0
        else:
            self.x = double_0
            self.y = double_1
            self.latitude = degrees_0
            self.longitude = degrees_1
            self.altitude = altitude_0
            self.centerLatitude = degrees_2
            self.centerLongitude = degrees_3
            self.type = dataBaseCoordinateType_0
            self.attributes = symbolAttributes_0
    def set_attribute(self, index, value):
        self.attributes.pop(index)
        self.attributes.insert(index, value)
    def get_altitude(self):
        return self.altitude
    def get_attributes(self):
        return self.attributes
    def get_centerLatitude(self):
        return self.centerLatitude
    def get_centerLongitude(self):
        return self.centerLongitude
    def get_latitude(self):
        return self.latitude
    def get_longitude(self):
        return self.longitude
    def get_type(self):
        return self.type
    def get_variation(self):
        return self.variation
class DataBaseCoordinates(list):
    def __init__(self, dataBaseCoordinatesType_0):
        self.type = dataBaseCoordinatesType_0
        pass
    def method_0(self, degrees_0, degrees_1, altitude_0, dataBaseCoordinateType_0, symbolAttributes_0):
        dataBaseCoordinate = DataBaseCoordinate(None, None, degrees_0, degrees_1, altitude_0, None, None, dataBaseCoordinateType_0, symbolAttributes_0)
        self.append(dataBaseCoordinate)
        return dataBaseCoordinate
    def method_1(self, double_0, double_1, degrees_0, degrees_1, altitude_0, dataBaseCoordinateType_0, symbolAttributes_0):
        dataBaseCoordinate = DataBaseCoordinate(double_0, double_1, degrees_0, degrees_1, altitude_0, None, None, dataBaseCoordinateType_0, symbolAttributes_0)
        self.append(dataBaseCoordinate)
        return dataBaseCoordinate
    def  method_2(self, double_0, double_1, degrees_0, degrees_1, altitude_0, degrees_2, dataBaseCoordinateType_0, symbolAttributes_0):
        dataBaseCoordinate = DataBaseCoordinate(double_0, double_1, degrees_0, degrees_1, altitude_0, degrees_2, None, dataBaseCoordinateType_0, symbolAttributes_0)
        self.append(dataBaseCoordinate)
        return dataBaseCoordinate
    def method_3(self, double_0, double_1, degrees_0, degrees_1, altitude_0, degrees_2, degrees_3, dataBaseCoordinateType_0, symbolAttributes_0):
        dataBaseCoordinate = DataBaseCoordinate(double_0, double_1, degrees_0, degrees_1, altitude_0, degrees_2, degrees_3, dataBaseCoordinateType_0, symbolAttributes_0)
        self.append(dataBaseCoordinate)
        return dataBaseCoordinate
    def method_4(self):
        self = []
    def method_5(self, dataBaseCoordinate_0):
        return self.index(dataBaseCoordinate_0)
    def method_6(self, dataBaseCoordinate_0):
        self.remove(dataBaseCoordinate_0)
    def method_7(self, int_0):
        self.pop(int_0)

    def get_Count(self):
        return len(self)
    Count = property(get_Count, None, None, None)

    def get_List(self):
        return self
    List = property(get_List, None, None, None)

    def get_Type(self):
        return self.type
    Type = property(get_Type, None, None, None)

    def __eq__(self, other):
        if (other == None):
            return 0
        return self.Count == other.Count
class SymbolAttributes(list):
    def __init__(self, stringList = None):
        self.attributes = []
        if stringList != None:
            self = stringList
            return
        for i in range(8):
            self.append(None)
            
    def get_attributes(self):
        return self.attributes
    Array = property(get_attributes, None, None, None)   
    
    def get_Remarks(self):
        if len(self.attributes) == 0:
            return
        strBuild = ""
        for i in range(3, len(self.attributes)):
            str0 = self.attributes[i]
            if str0 != None and str0 != "":
                if strBuild != "":
                    strBuild += ", "
                strBuild += str0  
        return self.strBuild
    Remarks = property(get_Remarks, None, None, None)      
    