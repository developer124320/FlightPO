# -*- coding: UTF-8 -*-


from PyQt4.QtGui import QDialog, QMessageBox, QStandardItemModel, QTextDocument,\
        QStandardItem, QProgressBar, QFileDialog, QFont, QPushButton, QLineEdit, QComboBox
from PyQt4.QtCore import Qt, QSizeF, QVariant, QCoreApplication, SIGNAL
# from PyQt4.QtCore import Qt

from FlightPlanner.ui_BaroVNavDlg import Ui_BaroV_Dialog
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.baroVnavSurfaces import BaroVnavSurfaceZ, BaroVnavSurfaceH, BaroVnavSurfaceFAS, BaroVnavFasSegment
from FlightPlanner.RnavTolerance0 import RnavGnssTolerance
from FlightPlanner.helpers import MathHelper, Unit, Altitude
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.types import Point3D, RnavSpecification, RnavGnssFlightPhase, ObstacleAreaResult, SurfaceTypes, ObstacleTableColumnType, AltitudeUnits, DistanceUnits
# from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.captureCoordinateTool import CaptureCoordinateTool, CaptureCoordinateToolUpdate
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.Obstacle.Obstacle import Obstacle, BaroVnavCriticalObstacle
from FlightPlanner.messages import Messages
from FlightPlanner.expressions import Expressions
from FlightPlanner.ExportDlg.ExportDlg import ExportDlg
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.AcadHelper import AcadHelper

from qgis.gui import QgsMapToolPan, QgsTextAnnotationItem
from qgis.core import QGis, QgsCsException, QgsMapLayerRegistry, QgsPoint, \
        QgsVectorLayer, QgsField, QgsGeometry, QgsFeature, QgsSymbolV2, QgsSvgMarkerSymbolLayerV2,\
        QgsRendererCategoryV2, QgsCategorizedSymbolRendererV2, QgsVectorFileWriter
import define

import math
import sys

class BaroVNavDlg(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.ui = Ui_BaroV_Dialog()
        self.ui.setupUi(self)
        
        QgisHelper.ClearCanvas(define._canvas)
        
#         if define._canvas.mapUnits() == QGis.Meters:        
#             self.ui.txtARPX.setText("664465.4750")
#             self.ui.txtARPY.setText("6616266.0911")
#             self.ui.txtThrX.setText("667815.8160")
#             self.ui.txtThrY.setText("6617747.9122")
#         else:
#             self.ui.txtARPX.setText("17.9186110008")
#             self.ui.txtARPY.setText("59.6519439999")
#             self.ui.txtThrX.setText("17.9791530008")
#             self.ui.txtThrY.setText("59.6638969994")
            
#         self.ui.txtARPAltM.setText("3.05")
#         self.ui.txtARPAltFt.setText("10")
        self.ui.txtMinTemperature.setText("-15")
#         self.ui.txtThrAltM.setText("6.1")
#         self.ui.txtThrAltFt.setText("20")
#         self.ui.txtRwyDir.setText("253.32")
        self.ui.cmbISType.addItem("OCA")
        self.ui.cmbISType.addItem("OCH")
        self.ui.txtISHeight.setText("2000")
        self.ui.txtISMoc.setText("150")
        self.ui.txtRDHatTHR.setText("15")
        i = 2.5
        while i<3.6:
            self.ui.cmbVerticalPathAngle.addItem(str(i))
            i += 0.1
        self.ui.txtTHRtoFAWP.setText("5")
        self.ui.cmbAircraftCategory.addItems(["A", "B", "C", "D","E","Custom"])
        self.ui.cmbAircraftCategory.setCurrentIndex(3)
        self.ui.txtMaxIAS.setText("185")
        self.ui.txtMaxIASatTHR.setText("165")
        self.ui.txtHeightLoss.setText("49")
        self.ui.cmbAPV.addItem("THR")
        self.ui.cmbAPV.addItem("Past THR")   
        self.ui.cmbAPV.setCurrentIndex(1)    
#         self.ui.frame_APV.setDisabled(True)
        self.ui.cmbAPV.currentIndexChanged.connect(self.enableTxtAPV)
#         self.ui.txtAPV.setText("5")
        self.ui.cmbMissedAppPoint.addItem("THR")
        self.ui.cmbMissedAppPoint.addItem("Before THR")
        self.ui.frame_MissApPt.setDisabled(True)
        self.ui.cmbMissedAppPoint.currentIndexChanged.connect(self.enableTxtMissApPt)
        
#         self.ui.txtMissedAppPoint.setDisabled(True)
        self.ui.txtMissedAppClimb.setText("2.5")
        self.ui.txtMissedAppMOC.setText("30")
        self.ui.cmbMissedAppEvalution.addItem("Xzi datum (std.)")
        self.ui.cmbMissedAppEvalution.addItem("VPA\'")
        self.ui.cmbConstructionType.addItem("2D")
        self.ui.cmbConstructionType.addItem("3D")
        self.ui.cmbSurface.addItems(["Final Approach (FAS)", "H", "Z"])
        self.ui.cmbUnits.addItems(["feet", "meter"])
        self.ui.cmbUnits.currentIndexChanged.connect(self.changeObstacleResults)
        
        self.ui.txtOCA.setText("OCA")
        self.ui.txtOCH.setText("OCH")
        self.aprAnnotation = QgsTextAnnotationItem(define._canvas)
        self.aprAnnotation.setDocument(QTextDocument("ARP"))
        self.aprAnnotation.setFrameSize( QSizeF( 30, 20 ) )
        self.aprAnnotation.hide()
        self.thrAnnotation= QgsTextAnnotationItem(define._canvas)
        self.thrAnnotation.setDocument(QTextDocument("THR"))
        self.thrAnnotation.setFrameSize( QSizeF( 30, 20 ) )
        self.thrAnnotation.hide()
        self.CaptureCoordARPTool = CaptureCoordinateToolUpdate(define._canvas, self.aprAnnotation)
        self.connect(self.CaptureCoordARPTool, SIGNAL("resultPointValueList"), self.resultPointValueListMethodArp)
        self.CaptureCoordThrTool = CaptureCoordinateToolUpdate(define._canvas, self.thrAnnotation)
        self.connect(self.CaptureCoordThrTool, SIGNAL("resultPointValueList"), self.resultPointValueListMethodThr)
        self.CaptureBearingTool = CaptureBearingTool(define._canvas, self.ui.txtRwyDir)

        '''buttons signal connect'''
        self.ui.btnCaptureCoordARP.setCheckable(True)
        self.ui.btnCaptureCoordThr.setCheckable(True)
        self.ui.btnCaptureDirRwy.setCheckable(True)
        self.ui.btnConstruct.clicked.connect(self._Construct)
        self.ui.btnEvaluate.clicked.connect(self._Evaluate)
        self.ui.btnPDCheck.clicked.connect(self._PDCheck)
        self.ui.btnClose.clicked.connect(self.exit)
        self.ui.btnEvaluate_2.clicked.connect(self._Locate)
        self.ui.btnClose_2.clicked.connect(self.exit)
        self.ui.btnCaptureCoordARP.clicked.connect(self._CaptureCoordARP)
        self.ui.btnCaptureCoordThr.clicked.connect(self._CaptureCoordThr)
        self.ui.btnCaptureDirRwy.clicked.connect(self._CaptureRunwayDir)
        self.ui.btnSaveData.clicked.connect(self.saveData)
        self.ui.btnOpenData.clicked.connect(self.openData)
        font = QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.ui.btnExportResult = QPushButton("")
        self.ui.btnExportResult.setFont(font)
        self.ui.btnExportResult.setIcon(self.ui.iconEvaluate)
        self.ui.btnExportResult.setToolTip("Export Result")
        self.ui.verticalLayout_4.insertWidget(2, self.ui.btnExportResult)
        self.ui.btnExportResult.setDisabled(True)
        self.ui.btnExportResult.clicked.connect(self.exportResult)
        self.ui.cmbSurface.currentIndexChanged.connect(self._cmbSurfaceChanged)
        self.ui.txtARPAltM.textChanged.connect(self._chageFromMToFt_ARP)
        self.ui.txtThrAltM.textChanged.connect(self._chageFromMToFt_Thr)
        self.ui.txtARPAltFt.textChanged.connect(self._chageFromFtToM_ARP)
        self.ui.txtThrAltFt.textChanged.connect(self._chageFromFtToM_Thr)
        self.ui.tblObstacles.clicked.connect(self.tblObstaclesClicked)
        self.ui.tblObstacles.verticalHeader().sectionClicked.connect(self.tblObstaclesClicked)
        
        
        self.ui.txtMaxIAS.textChanged.connect(self._iasChanged)
        self.ui.txtMissedAppPoint.textChanged.connect(self._missedAppPtChanged)
        self.ui.txtAPV.setText("5")
        self.ui.txtAPV.textChanged.connect(self._apvChanged)
        self.ui.cmbAircraftCategory.currentIndexChanged.connect(self._aircraftCategoryChanged)
#         self.ui.cmbAPV.currentIndexChanged.connect(self._apvChanged)
#         self.ui.cmbMissedAppPoint.currentIndexChanged.connect(self._cmbMissedAppPtChanged)
        self.ui.txtMaxIASatTHR.textChanged.connect(self._iasAtThrChanged)
        self.ui.txtARPAltM.textChanged.connect(self._arpAltChanged)
        self.ui.cmbVerticalPathAngle.currentIndexChanged.connect(self._vpaChanged)
        self.ui.cmbVerticalPathAngle.setCurrentIndex(5) # 3.0
        self.ui.toolButton.clicked.connect(self._LocateCritical)
        self.flag = 0
    #Unit.smethod_0

        self.modelObstaclesFAS = QStandardItemModel()
        self.modelObstaclesH = QStandardItemModel()
        self.modelObstaclesZ = QStandardItemModel()
#         self.ui.table.setColumnWidth(0, 200)
#         self.ui.table.setColumnWidth(1, 160)
        self.initTblOstacle()
        
        
        self.ui.tblObstacles.setModel(self.modelObstaclesFAS)
        self.ui.tblObstacles.setSortingEnabled(True)
        self.calculationResults = []

        self.segmentTerminationDist = 5
        self.customIas = 185
        self.customIasAtThr = 165
        self.mapPtDist = 0.5
        self.percent = 0
        self.criticalObstacle = None
        self.obstacleModel = None
        # define._canvas.mapUnitsChanged.connect(self.changeMapUnit)
        
        lstTextControls = self.ui.groupBox_11.findChildren(QLineEdit)
        for ctrl in lstTextControls:
            ctrl.textChanged.connect(self.initResultPanel)
        lstComboControls = self.ui.groupBox_11.findChildren(QComboBox)
        for ctrl in lstComboControls:
            ctrl.currentIndexChanged.connect(self.initResultPanel)

        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)

        self.ui.btnAPV.clicked.connect(self.measureToolAPV)
        self.ui.btnMAPoint.clicked.connect(self.measureToolMAPoint)

        self.ui.txtARPX.textChanged.connect(self.directionCalc)
        self.ui.txtARPY.textChanged.connect(self.directionCalc)
        self.ui.txtThrX.textChanged.connect(self.directionCalc)
        self.ui.txtThrY.textChanged.connect(self.directionCalc)

        self.ui.txtISHeight.textChanged.connect(self.txtAltitudeFtChanged)
        self.ui.txtISHeightM.textChanged.connect(self.txtAltitudeMChanged)

        self.flag = 0
        self.metreChangedFlag = False
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.ui.txtISHeightM.setText(str(round(Unit.ConvertFeetToMeter(float(self.ui.txtISHeight.text())), 4)))
                self.metreChangedFlag = False
            except:
                self.ui.txtISHeightM.setText("0.0")

    def txtAltitudeMChanged(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.ui.txtISHeight.setText(str(round(Unit.ConvertMeterToFeet(float(self.ui.txtISHeightM.text())), 4)))
                self.metreChangedFlag = True
            except:
                self.ui.txtISHeight.setText("0.0")
    def txtAltitudeFtChanged(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.ui.txtISHeightM.setText(str(round(Unit.ConvertFeetToMeter(float(self.ui.txtISHeight.text())), 4)))
                self.metreChangedFlag = False
            except:
                self.ui.txtISHeightM.setText("0.0")
    def directionCalc(self):
        try:
            pointArp = Point3D(self.ui.txtARPX.text().toFloat()[0], self.ui.txtARPY.text().toFloat()[0])
            pointThr = Point3D(self.ui.txtThrX.text().toFloat()[0], self.ui.txtThrY.text().toFloat()[0])
            if (pointArp.get_X() == 0 and pointArp.get_Y() == 0) or (pointThr.get_X() == 0 and pointThr.get_Y() == 0):
                return
            self.ui.txtRwyDir.setText(str(round(Unit.ConvertRadToDeg(MathHelper.getBearing(pointArp, pointThr)), 4)))
        except:
            pass
    def initResultPanel(self):
        self.ui.btnEvaluate.setEnabled(False)
        if self.modelObstaclesFAS != None and self.ui.btnEvaluate.isEnabled():
            self.modelObstaclesFAS.clear()
            self.modelObstaclesH.clear()
            self.modelObstaclesZ.clear()
            self.initTblOstacle()
            self.ui.btnExportResult.setEnabled(False)
            lstTextControls = self.ui.groupBox.findChildren(QLineEdit)
            for ctrl in lstTextControls:
                if ctrl.objectName() != "txtOCH" and ctrl.objectName() != "txtOCA":
                    ctrl.setText("")
                    
                    
    def initTblOstacle(self):
        self.modelObstaclesFAS.setHorizontalHeaderLabels(["Name", "Alt.(m)", "Trees(m)", "Area", "Dist.in(m)", \
                                               "MOC applied(m)", "Eq.alt.(m)", "Eq.alt.(ft)", "Surf.alt.(m)"\
                                               ,"Difference(m)", "HL applied(m)", "OCA(ft)", "Critical"])
        self.modelObstaclesH.setHorizontalHeaderLabels(["Name", "Alt.(m)", "Trees(m)", "Area", "Dist.in(m)", \
                                               "MOC applied(m)", "Eq.alt.(m)", "Eq.alt.(ft)", "Surf.alt.(m)"\
                                               ,"Difference(m)", "HL applied(m)", "OCA(ft)", "Critical"])
        self.modelObstaclesZ.setHorizontalHeaderLabels(["Name", "Alt.(m)", "Trees(m)", "Area", "Dist.in(m)", \
                                               "MOC applied(m)", "Eq.alt.(m)", "Eq.alt.(ft)", "Surf.alt.(m)"\
                                               ,"Difference(m)", "HL applied(m)", "OCA(ft)", "Critical"])
        self.modelObstaclesZ.setSortRole(Qt.UserRole + 1)
        self.modelObstaclesFAS.setSortRole(Qt.UserRole + 1)
        self.modelObstaclesH.setSortRole(Qt.UserRole + 1)

    def Speed_smethod_0(self, speed_0, double_0, altitude_0, isKTS=True):
        if isKTS:
            knots = speed_0 * 171233 * math.pow(288 + double_0 - 0.00198 * altitude_0, 0.5);
            num = math.pow(288 - 0.00198 * altitude_0, 2.628);
            return knots / num
        kilometresPerHour = speed_0 * 171233 * math.pow(288 + double_0 - 0.006496 * altitude_0, 0.5)
        num1 = math.pow(288 - 0.006496 * altitude_0, 2.628);
        return kilometresPerHour / num1;

    #this.method_37()
    def GetVPAValue(self):
        i = 0
        num = 2.5
        while i < self.ui.cmbVerticalPathAngle.currentIndex():
            num = num + 0.1
            i += 1
            
        return round(num, 1)

    # TempCorrection.smethod_0
    # return double
    # input double, double, double, double
    def TempCorrection_smethod_0(self, altitude_0, altitude_1, altitude_2, double_0, hFAP = None):
        num = 0.0065;
        metres = 15 - num * altitude_2;
        double0 = -(metres - double_0);
        return ((-double0) / (-num)) * (math.log(1 - num * altitude_0 / (288.15 - num * altitude_1)))

        # num = 0.0065
        # double0 = double_0 + num * altitude_2;
        # return altitude_0 * ((15 - double0) / (273 + double0 - 0.5 * num * (altitude_0 + altitude_1)));

    def loadPointForArea(self, features, area, surfaceType, layerid):

        for feature in features:
            name = feature.attribute("Name").toString()
            altitude = feature.attribute("Altitude").toString()
            trees = str(define._trees)
            point = feature.geometry().asPoint()
            layer = QgsMapLayerRegistry.instance().mapLayer(layerid)
            altItem = QStandardItem(altitude)
            altItem.setData(feature.attribute("Altitude"))
            treeItem = QStandardItem(trees)
            treeItem.setData(define._trees)
            if define._units == QGis.Meters:
                point = QgisHelper.Degree2Meter(point.x(), point.y())
            if surfaceType == "FAS":
                self.modelObstaclesFAS.appendRow(\
                    [ QStandardItem(name), altItem, treeItem,\
                     QStandardItem(area), QStandardItem(""), QStandardItem(""), QStandardItem("")\
                    , QStandardItem(""), QStandardItem(""), QStandardItem(""), QStandardItem("")\
                    , QStandardItem(""), QStandardItem(""),\
                     QStandardItem(layerid), QStandardItem(str(feature.id())), QStandardItem(str(point.x())), QStandardItem(str(point.y()))])
            elif surfaceType == "H":
                self.modelObstaclesH.appendRow(\
                    [ QStandardItem(name), altItem, treeItem,\
                     QStandardItem(area), QStandardItem(""), QStandardItem(""), QStandardItem("")\
                    , QStandardItem(""), QStandardItem(""), QStandardItem(""), QStandardItem("")\
                    , QStandardItem(""), QStandardItem(""),\
                     QStandardItem(layerid), QStandardItem(str(feature.id())), QStandardItem(str(point.x())), QStandardItem(str(point.y()))])
            elif surfaceType == "Z":
                self.modelObstaclesZ.appendRow(\
                    [ QStandardItem(name), altItem, treeItem,\
                     QStandardItem(area), QStandardItem(""), QStandardItem(""), QStandardItem("")\
                    , QStandardItem(""), QStandardItem(""), QStandardItem(""), QStandardItem("")\
                    , QStandardItem(""), QStandardItem(""),\
                     QStandardItem(layerid), QStandardItem(str(feature.id())), QStandardItem(str(point.x())), QStandardItem(str(point.y()))])
            if self.progress is not None:
                k = self.progress.value() + 1
                self.progress.setValue(k)
    def loadPointObstacles(self, baroVNavSurfaces):
       pass
#         for obstacleLayer in define._obstacleLayers:            
#             for surface in baroVNavSurfaces:
#                 features = QgisHelper.getFeaturesInPolygon(define._canvas, obstacleLayer, surface.primaryArea)
#                 self.loadPointForArea(features, ObstacleAreaResult.Primary, surface.Type, obstacleLayer.id())
#                 
#                 for secondary in surface.secondaryAreas:
#                     featuresSecondary = QgisHelper.getFeaturesInPolygon(define._canvas, obstacleLayer, secondary.area.getArea())
#                     self.loadPointForArea(featuresSecondary, ObstacleAreaResult.Secondary, surface.Type, obstacleLayer.id())
               
    def getObstacleFromModel(self, modelObstacles, row):
        
        item = modelObstacles.item(row, 0)
        name = item.text()        
        item = modelObstacles.item(row, 1)
        z = float(item.text())
        item = modelObstacles.item(row, 2)
        trees = float(item.text())
        item = modelObstacles.item(row, 3)
        area = item.text()
        
        item = modelObstacles.item(row, 13)
        layerId = item.text()
        item = modelObstacles.item(row, 14)
        featureId = int(item.text())
        item = modelObstacles.item(row, 15)
        x = float(item.text())
        item = modelObstacles.item(row, 16)
        y = float(item.text())
        point3d = Point3D(x, y, z)
        
        obstacle = Obstacle(name, point3d, layerId, featureId, area, trees, 1, define._tolerance)
        return obstacle
    
    def setMocResultToModel(self, model, row, distInMeter, MocAppMeter, eqAltMeter,\
                             surfAltMeter, differenceMeter, heightLossMeter, ocaMeter):
        item = model.item(row, 4)
        item.setText(str(distInMeter))
        item.setData(distInMeter if distInMeter != None else -9999)
        
        item = model.item(row, 5)
        item.setText(str(MocAppMeter))
        item.setData(MocAppMeter if MocAppMeter != None else -9999)
        
        item = model.item(row, 6)
        item.setText(str(eqAltMeter))
        item.setData(eqAltMeter if eqAltMeter != None else -9999)
        
        item = model.item(row, 7)
        item.setText(str(Unit.ConvertMeterToFeet(eqAltMeter)))
        item.setData(Unit.ConvertMeterToFeet(eqAltMeter) if eqAltMeter != None else -9999)
        
        item = model.item(row, 8)
        item.setText(str(surfAltMeter))
        item.setData(surfAltMeter if surfAltMeter != None else -9999)
        
        item = model.item(row, 9)
        item.setText(str(differenceMeter))
        item.setData(differenceMeter if differenceMeter != None else -9999)
        
        item = model.item(row, 10)
        item.setText(str(heightLossMeter))
        item.setData(heightLossMeter if heightLossMeter != None else -9999)
        
        item = model.item(row, 11)
        item.setText(str(Unit.ConvertMeterToFeet(ocaMeter)))
        item.setData(Unit.ConvertMeterToFeet(ocaMeter) if ocaMeter != None else -9999)
        
        item = model.item(row, 12)
        if (differenceMeter <= 0):
            item.setText("No")
        else:
            item.setText("Yes")
    
    def changeObstacleResults(self):
        if self.criticalObstacle == None:
            return
        else:
            if self.ui.cmbUnits.currentIndex() == 0:# feet
                self.ui.txtOCAResults.setText(str(Unit.ConvertMeterToFeet(self.criticalObstacle.oca)))
                self.ui.txtOCHResults.setText(str(Unit.ConvertMeterToFeet(self.criticalObstacle.getOCH())))
            else:
                self.ui.txtOCAResults.setText(str(self.criticalObstacle.oca))
                self.ui.txtOCHResults.setText(str(self.criticalObstacle.getOCH())) 
    def setCriticalObstacle(self):
        if self.criticalObstacle == None:
            return
        else:
            self.ui.txtID.setText(self.criticalObstacle.obstacle.name)
            self.ui.txtX.setText(str(self.criticalObstacle.obstacle.Position.x()))
            self.ui.txtY.setText(str(self.criticalObstacle.obstacle.Position.y()))
            self.ui.txtAltitude.setText(str(self.criticalObstacle.obstacle.Position.z()))
            self.ui.txtAltitudeM.setText(str(Unit.ConvertMeterToFeet(self.criticalObstacle.obstacle.Position.z())))
            self.ui.txtSurface.setText(self.criticalObstacle.baroVnavSurfaceType)
            
            if self.ui.cmbSurface.currentIndex() == 0:# feet
                self.ui.txtOCAResults.setText(str(Unit.ConvertMeterToFeet(self.criticalObstacle.oca)))
                self.ui.txtOCHResults.setText(str(Unit.ConvertMeterToFeet(self.criticalObstacle.getOCH())))
            else:
                self.ui.txtOCAResults.setText(str(self.criticalObstacle.oca))
                self.ui.txtOCHResults.setText(str(self.criticalObstacle.getOCH()))
    def changeMapUnit(self):
        try:
            dblARPX = float(self.ui.txtARPX.text())
        except ValueError:
            dblARPX = 0
        try:
            dblARPY = float(self.ui.txtARPY.text())
        except ValueError:
            dblARPY = 0
        try:
            dblThrX = float(self.ui.txtThrX.text())
        except ValueError:
            dblThrX = 0
        try:
            dblThrY = float(self.ui.txtThrY.text())
        except ValueError:
            dblThrY = 0
        
#         latCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
#         meterCrs = QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.EpsgCrsId)
# 
#         if define._units == QGis.DecimalDegrees:
#             crsTransform = QgsCoordinateTransform (meterCrs, latCrs)
#         else:
#             crsTransform = QgsCoordinateTransform (latCrs, meterCrs)
        
        arpPoint1 = QgisHelper.transformPoint(dblARPX, dblARPY)
        thrPoint1 = QgisHelper.transformPoint(dblThrX, dblThrY)
        self.ui.txtARPX.setText(str(arpPoint1.x()))
        self.ui.txtARPY.setText(str(arpPoint1.y()))
        self.ui.txtThrX.setText(str(thrPoint1.x()))
        self.ui.txtThrY.setText(str(thrPoint1.y()))
            
    def calcHeightLoss(self):
        try:
            num = self.GetVPAValue();
            try:
                num1 = float(self.ui.txtARPAltM.text())
            except:
                num1 = 0.0
            try:
                num2 = float(self.ui.txtMaxIASatTHR.text())
            except:
                num2 = 0.0
            num3 = round(0.125 * num2 + 28.3)
            num4 = round(0.177 * num2 - 3.2)
            num5 = 0;
            if num1 > 900:
                num5 = num5 + num4 * 0.02 * (num1 / 300);
            if num > 3.2:
                num5 = num5 + num4 * 0.05 * ((num - 3.2) / 0.1);
#             num5 = MathHelper.smethod_0(num5, 0)
            self.ui.txtHeightLoss.setText(str(num3 + num5))
        except:
            self.ui.txtHeightLoss.setText("")
#        self.ui.tblObstacles.setModel(self.modelObstaclesFAS)
    def method_48(self, calculationResults, isPDCheck = False):
            point3d2 = None
            point3d3 = None
            
            textValARPX = self.ui.txtARPX.text()
            if textValARPX is None or textValARPX == "":
                raise SyntaxWarning, "X Coordination of ARP"
            textValARPY = self.ui.txtARPY.text()
            if textValARPY is None or textValARPY == "":
                raise SyntaxWarning, "Y Coordination of ARP"
            textValARPAltM = self.ui.txtARPAltM.text()
            if textValARPAltM is None or textValARPAltM == "":
                dblARPAltM = 0.0
            else:
                dblARPAltM = float(textValARPAltM)
            pointARP = Point3D(float(textValARPX),float(textValARPY),dblARPAltM)
            #pointARP.SetZ(34)
#             #print (pointARP.z())

            textValThrX = self.ui.txtThrX.text()
            if textValThrX is None or textValThrX == "":
                raise SyntaxWarning, "X Coordination of THR"
            textValThrY = self.ui.txtThrY.text()
            if textValThrY is None or textValThrY == "":
                raise SyntaxWarning, "Y Coordination of THR"
            textValThrAltM = self.ui.txtThrAltM.text()
            if textValThrAltM is None or textValThrAltM == "":
                dblThrAltM = 0.0
            else:
                dblThrAltM = float(textValThrAltM)
            try:
                self.pointTHR = Point3D(float(textValThrX),float(textValThrY),dblThrAltM)
            except ValueError:
                raise UserWarning, "THR Position is invalid!"
#             #print (pointARP.z())
#             #print self.self.pointTHR.z() 
            ''' for Degree '''                 
#             if define._canvas.mapUnits() != QGis.Meters:
#                 pointARP = QgisHelper.Degree2MeterPoint3D(pointARP)
#                 self.pointTHR = QgisHelper.Degree2MeterPoint3D(self.pointTHR)
                
            strRwyDir = self.ui.txtRwyDir.text()
            if strRwyDir is None or strRwyDir == "":
                strRwyDir = "0"
            rwyDir = Unit.ConvertDegToRad(strRwyDir)
            rwyDirLeft = MathHelper.smethod_4(rwyDir - 1.5707963267949);
            rwyDirRight = MathHelper.smethod_4(rwyDir + 1.5707963267949);
            rwyDirBack = MathHelper.smethod_4(rwyDir + 3.14159265358979);
            angle15 = Unit.ConvertDegToRad(15);
            angle30 = Unit.ConvertDegToRad(30);
#             Altitude altitude = this.pnlOCAH.method_2(this.pnlThr.Altitude);
            metres = 0.0
            strISHeight = self.ui.txtISHeight.text()
            if strISHeight is None or strISHeight == "":
                strISHeight = "0"
            if self.ui.cmbISType.currentIndex() == 0:
                metres = Unit.ConvertFeetToMeter(float(strISHeight))
            else:
                metres = Unit.ConvertFeetToMeter(float(strISHeight)) + dblThrAltM
#             altitude = this.pnlOCAH.method_3(this.pnlThr.Altitude);
            heightFAP = Unit.ConvertFeetToMeter(float(strISHeight)) - dblThrAltM
            
            strRDH = self.ui.txtRDHatTHR.text()
            if strRDH is None or strRDH == "":
                strRDH = "0"
            RDH = float(strRDH)
            num6 = self.GetVPAValue();
            tanVPA = math.tan(Unit.ConvertDegToRad(num6));
            sinVPA = math.sin(Unit.ConvertDegToRad(num6));
            
            try:
                ISMoc = float(self.ui.txtISMoc.text())#this.pnlMocI.Value.Metres;
            except ValueError:
                ISMoc = 0.0
                
            try:
                MAMoc = float(self.ui.txtMissedAppMOC.text())#double MAMoc = this.pnlMocMA.Value.Metres;
            except ValueError:
                MAMoc = 0.0
            #AngleGradientSlope angleGradientSlope = this.pnlMACG.Value;
            
            try:
                self.percent = float(self.ui.txtMissedAppClimb.text()) / 100#double self.percent = angleGradientSlope.self.percent / 100;
            except ValueError:
                self.percent = 0.0
#             RnavGnssTolerance rnavGnssTolerance = new RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Star30Sid30IfIafMa30, AircraftSpeedCategory.D);
            rnavGnssTolerance = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Star30Sid30IfIafMa30, "D")
            
#             RnavGnssTolerance rnavGnssTolerance1 = new RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Faf, AircraftSpeedCategory.D);
            rnavGnssTolerance1 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Faf, "D")
#             RnavGnssTolerance rnavGnssTolerance2 = new RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Mapt, AircraftSpeedCategory.D);
            rnavGnssTolerance2 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Mapt, "D")
#             RnavGnssTolerance rnavGnssTolerance3 = new RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Ma15, AircraftSpeedCategory.D);
            rnavGnssTolerance3 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Ma15, "D")
#             RnavGnssTolerance rnavGnssTolerance4 = new RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Star30Sid30IfIafMa30, AircraftSpeedCategory.D);
            rnavGnssTolerance4 = RnavGnssTolerance(RnavSpecification.RnpApch, RnavGnssFlightPhase.Star30Sid30IfIafMa30, "D");
#             double metres5 = rnavGnssTolerance.ATT.Metres;
#             metres5 = rnavGnssTolerance.getATTMetres()
#             double metres6 = rnavGnssTolerance.ASW.Metres;
            metres6 = rnavGnssTolerance.getASWMetres()
#             double ATT = rnavGnssTolerance1.ATT.Metres;
            ATT = rnavGnssTolerance1.getATTMetres()
#             double metres8 = rnavGnssTolerance1.ASW.Metres;
            metres8 = rnavGnssTolerance1.getASWMetres()
#             double metres9 = rnavGnssTolerance2.ATT.Metres;
            metres9 = rnavGnssTolerance2.getATTMetres()
#             double num9 = rnavGnssTolerance2.ASW.Metres;
            num9 = rnavGnssTolerance2.getASWMetres()
#             double metres10 = rnavGnssTolerance3.ATT.Metres;
            metres10 = rnavGnssTolerance3.getATTMetres()
#             double num10 = rnavGnssTolerance3.ASW.Metres;
            num10 = rnavGnssTolerance3.getASWMetres()
#             double metres11 = rnavGnssTolerance4.ATT.Metres;
            metres11 = rnavGnssTolerance4.getATTMetres()
#             double num11 = rnavGnssTolerance4.ASW.Metres;
            num11 = rnavGnssTolerance4.getASWMetres()
#             Distance distanceTHRtoFAWP = this.pnlThrFafDist.Value;
            try:
                distanceTHRtoFAWP = Unit.ConvertNMToMeter(float(self.ui.txtTHRtoFAWP.text()))
            except ValueError:
                distanceTHRtoFAWP = 0.0
                
#             Point3d pointFAP = MathHelper.distanceBearingPoint(self.self.pointTHR, rwyDirBack, distanceTHRtoFAWP.Metres);
#             #print self.self.pointTHR.x()   
            pointFAP = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, distanceTHRtoFAWP)
            self.pointFAWP = pointFAP
#             pointFAP1 = QgisHelper.transformPoint(pointFAP.x(), pointFAP.y(), False)
#             distanceTHRtoFAWP = this.pnlMAPtDist.Value;
            if self.ui.txtMissedAppPoint.text() == "":
                distanceTHRtoFAWP = 0.0
            else:
                distanceTHRtoFAWP = Unit.ConvertNMToMeter(float(self.ui.txtMissedAppPoint.text()))
#             Point3d pointMA = MathHelper.distanceBearingPoint(self.self.pointTHR, rwyDirBack, distanceTHRtoFAWP.Metres.smethod_17());
            pointMA = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, distanceTHRtoFAWP)
            self.pointMAWP = pointMA
#             pointMA1 = QgisHelper.transformPoint(pointMA.x(), pointMA.y(), False)

#             point3d9 = MathHelper.distanceBearingPoint(pointFAP, rwyDirLeft, metres8)
# #             print metres8
# #             print rwyDirLeft
#             print point3d9
#             print QgisHelper.transformPoint(point3d9.x(), point3d9.y(), False)
     
#             distanceTHRtoFAWP = this.pnlTerminationDist.Value;
            if self.ui.txtAPV.text() == "":
                distanceTHRtoFAWP = 0.0
            else:
                distanceTHRtoFAWP = Unit.ConvertNMToMeter(float(self.ui.txtAPV.text()))
#             Point3d pointAPV = MathHelper.distanceBearingPoint(pointMA, rwyDir, distanceTHRtoFAWP.Metres.smethod_17());
            pointAPV = MathHelper.distanceBearingPoint(pointMA, rwyDir, distanceTHRtoFAWP);
            self.pointMAHWP = pointAPV
#             if (self.self.pointTHR.get_Z() < Units.distanceBearingPoint(5000))
            if self.pointTHR.z() < Unit.ConvertFeetToMeter(5000.0):
                if heightFAP <= 75.0:
                    if isPDCheck:
                        calculationResults.append(Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM)
                    else:
                        raise UserWarning, Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM
            elif self.pointTHR.z() < Unit.ConvertFeetToMeter(10000.0):
                if heightFAP <= 105.0:
                    if isPDCheck:
                        calculationResults.append(Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM)
                    else:
                        raise UserWarning, Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM
            elif heightFAP <=120:
                if isPDCheck:
                    calculationResults.append(Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM)
                else:
                    raise UserWarning, Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM
#             {
#                 if (heightFAP <= 75)
#                 {
#                     throw new Exception(Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM);
#                 }
#             }
#             else if (self.self.pointTHR.get_Z() <= Units.distanceBearingPoint(10000))
#             {
#                 if (heightFAP <= 105)
#                 {
#                     throw new Exception(Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM);
#                 }
#             }
#             else if (heightFAP <= 120)
#             {
#                 throw new Exception(Messages.ERR_INSUFFICIENT_INTERMEDIATE_SEGMENT_MINIMUM);
#             }
#             double num12 = (heightFAP - RDH) / tanVPA;
            num12 = (heightFAP - RDH) / tanVPA;
#             double tempCorrection = TempCorrection.smethod_0(new Altitude(metres - pointARP.get_Z()), new Altitude(pointARP.get_Z()), new Altitude(pointARP.get_Z()), this.pnlMinTemp.Value);
            minTemp = 0.0
            try:
                minTemp = float(self.ui.txtMinTemperature.text())
            except ValueError:
                minTemp = 0.0

            altitudeISValue = None
            if self.metreChangedFlag:
                altitudeISValue= Altitude(float(self.ui.txtISHeightM.text()))
            else:
                altitudeISValue= Altitude(float(self.ui.txtISHeight.text()), AltitudeUnits.FT)
            # altitudeARPValue = Altitude(float(self.ui.txtARPAltM.text()))
            altitudeValue = (altitudeISValue.Metres -  pointARP.z()) if self.ui.cmbISType.currentIndex() == 0 else altitudeISValue.Metres
            tempCorrection = self.TempCorrection_smethod_0(altitudeValue, pointARP.z(), pointARP.z(), minTemp);
            
#             num = 0.0065
#             
#             double0 = minTemp + num * pointARP.z();
#             aa = ((15 - minTemp) / num) * math.log(1 + num * heightFAP / (15.15  + num * dblThrAltM))
#             bb = Unit.ConvertMeterToFeet(aa)
            
#             double num14 = Units.smethod_1(Math.Atan((heightFAP - RDH - tempCorrection) / num12));
            num14 = Unit.smethod_1(math.atan((heightFAP - RDH - tempCorrection) / num12));
#             List<BaroVNAV.BaroVnavFasSegment> baroVnavFasSegments = new List<BaroVNAV.BaroVnavFasSegment>();
            baroVnavFasSegments = [];
            
#             BaroVNAV.BaroVnavFasSegment baroVnavFasSegment = new BaroVNAV.BaroVnavFasSegment()
            baroVnavFasSegment = BaroVnavFasSegment()
            baroVnavFasSegment.moc = 75
            baroVnavFasSegment.tanafas = (heightFAP - tempCorrection - baroVnavFasSegment.moc) * tanVPA / (heightFAP - baroVnavFasSegment.moc)
            baroVnavFasSegment.xfas = (baroVnavFasSegment.moc - RDH) / tanVPA + ATT
            baroVnavFasSegment.xstart = baroVnavFasSegment.xfas
            baroVnavFasSegment.xend = baroVnavFasSegment.xfas + (Unit.ConvertFeetToMeter(5000) - self.pointTHR.z()) / baroVnavFasSegment.tanafas
            baroVnavFasSegment.ptStart = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegment.xstart)
            baroVnavFasSegment.ptEnd = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegment.xend)
#             baroVnavFasSegments.Add(baroVnavFasSegment);
            baroVnavFasSegments.append(baroVnavFasSegment)
            
#             baroVnavFasSegment = new BaroVNAV.BaroVnavFasSegment()
            baroVnavFasSegment1 = BaroVnavFasSegment()
            baroVnavFasSegment1.moc = 105.0
            baroVnavFasSegment1.tanafas = (heightFAP - tempCorrection - baroVnavFasSegment1.moc) * tanVPA / (heightFAP - baroVnavFasSegment1.moc)
            baroVnavFasSegment1.xfas = (baroVnavFasSegment1.moc - RDH) / tanVPA + ATT
            baroVnavFasSegment1.xstart = baroVnavFasSegment1.xfas + (Unit.ConvertFeetToMeter(5000) - self.pointTHR.z()) / baroVnavFasSegment1.tanafas
            baroVnavFasSegment1.xend = baroVnavFasSegment1.xfas + (Unit.ConvertFeetToMeter(10000) - self.pointTHR.z()) / baroVnavFasSegment1.tanafas
            baroVnavFasSegment1.ptStart = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegment1.xstart)
            baroVnavFasSegment1.ptEnd = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegment1.xend)
#             baroVnavFasSegments.Add(baroVnavFasSegment);
            baroVnavFasSegments.append(baroVnavFasSegment1);
            
#             baroVnavFasSegment = new BaroVNAV.BaroVnavFasSegment()
            baroVnavFasSegment2 = BaroVnavFasSegment()
            baroVnavFasSegment2.moc = 120
            baroVnavFasSegment2.tanafas = (heightFAP - tempCorrection - baroVnavFasSegment2.moc) * tanVPA / (heightFAP - baroVnavFasSegment2.moc)
            baroVnavFasSegment2.xfas = (baroVnavFasSegment2.moc - RDH) / tanVPA + ATT
            baroVnavFasSegment2.xstart = baroVnavFasSegment2.xfas + (Unit.ConvertFeetToMeter(10000) - self.pointTHR.z()) / baroVnavFasSegment2.tanafas
            baroVnavFasSegment2.xend = baroVnavFasSegment2.xfas + (heightFAP - ISMoc) / baroVnavFasSegment2.tanafas
            baroVnavFasSegment2.ptStart = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegment2.xstart)
            baroVnavFasSegment2.ptEnd = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegment2.xend)
#             baroVnavFasSegments.Add(baroVnavFasSegment);
            baroVnavFasSegments.append(baroVnavFasSegment2)
#             if (self.pointTHR.get_Z() >= Units.distanceBearingPoint(5000))
#             {
#                 baroVnavFasSegments.RemoveAt(0);
#                 baroVnavFasSegments[0].xstart = baroVnavFasSegments[0].xfas;
#                 baroVnavFasSegments[0].ptStart = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegments[0].xstart);
#             }
            if self.pointTHR.z() >= Unit.ConvertFeetToMeter(5000):
                baroVnavFasSegments.pop(0);
                baroVnavFasSegments[0].xstart = baroVnavFasSegments[0].xfas;
                baroVnavFasSegments[0].ptStart = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegments[0].xstart);
#             if (self.pointTHR.get_Z() >= Units.distanceBearingPoint(10000))
#             {
#                 baroVnavFasSegments.RemoveAt(0);
#                 baroVnavFasSegments[0].xstart = baroVnavFasSegments[0].xfas;
#                 baroVnavFasSegments[0].ptStart = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegments[0].xstart);
#             }
            if (self.pointTHR.z() >= Unit.ConvertFeetToMeter(10000)):
                baroVnavFasSegments.pop(0);
                baroVnavFasSegments[0].xstart = baroVnavFasSegments[0].xfas
                baroVnavFasSegments[0].ptStart = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegments[0].xstart)
#             if (metres - ISMoc <= Units.distanceBearingPoint(10000))
#             {
#                 baroVnavFasSegments.RemoveAt(baroVnavFasSegments.Count - 1);
#                 baroVnavFasSegments[baroVnavFasSegments.Count - 1].xend = baroVnavFasSegments[baroVnavFasSegments.Count - 1].xfas + (heightFAP - ISMoc) / baroVnavFasSegments[baroVnavFasSegments.Count - 1].tanafas;
#                 baroVnavFasSegments[baroVnavFasSegments.Count - 1].ptEnd = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegments[baroVnavFasSegments.Count - 1].xend);
#             }
            if (metres - ISMoc <= Unit.ConvertFeetToMeter(10000)):
                baroVnavFasSegments.pop(len(baroVnavFasSegments) - 1);
#                 #print baroVnavFasSegment2.tanafas
#                 #print baroVnavFasSegments[len(baroVnavFasSegments) - 1]
#                 #print len(baroVnavFasSegments) - 1
                baroVnavFasSegments[len(baroVnavFasSegments) - 1].xend = baroVnavFasSegments[len(baroVnavFasSegments) - 1].xfas + (heightFAP - ISMoc) / baroVnavFasSegments[len(baroVnavFasSegments) - 1].tanafas
                baroVnavFasSegments[len(baroVnavFasSegments) - 1].ptEnd = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegments[len(baroVnavFasSegments) - 1].xend)

#             if (metres - ISMoc <= Units.distanceBearingPoint(5000))
#             {
#                 baroVnavFasSegments.RemoveAt(baroVnavFasSegments.Count - 1);
#                 baroVnavFasSegments[baroVnavFasSegments.Count - 1].xend = baroVnavFasSegments[baroVnavFasSegments.Count - 1].xfas + (heightFAP - ISMoc) / baroVnavFasSegments[baroVnavFasSegments.Count - 1].tanafas;
#                 baroVnavFasSegments[baroVnavFasSegments.Count - 1].ptEnd = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegments[baroVnavFasSegments.Count - 1].xend);
#             }
            if (metres - ISMoc <= Unit.ConvertFeetToMeter(5000)):
                baroVnavFasSegments.pop(len(baroVnavFasSegments) - 1);
                baroVnavFasSegments[len(baroVnavFasSegments) - 1].xend = baroVnavFasSegments[len(baroVnavFasSegments) - 1].xfas + (heightFAP - ISMoc) / baroVnavFasSegments[len(baroVnavFasSegments) - 1].tanafas
                baroVnavFasSegments[len(baroVnavFasSegments) - 1].ptEnd = MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegments[len(baroVnavFasSegments) - 1].xend)
                
#             Speed speed = Speed.smethod_0(this.pnlIas.Value, 15, new Altitude(pointARP.get_Z()));
            try:
                dblMaxIAS = float(self.ui.txtMaxIAS.text())
            except ValueError:
                dblMaxIAS = 0.0
            speed = self.Speed_smethod_0(dblMaxIAS, 15, Unit.ConvertMeterToFeet(pointARP.z()))
#             double metresPerSecond = speed.MetresPerSecond;
            metresPerSecond = Unit.ConvertKTSToMPS(speed)
#             double heightLoss = this.pnlHL.Value.Metres;
            try:
                heightLoss = float(self.ui.txtHeightLoss.text())
            except ValueError:
                heightLoss = 0.0
#             this.method_36(); this is AircraftCategory validation
#             switch (this.method_36())
#             {
#                 case AircraftSpeedCategory.A:
#                 case AircraftSpeedCategory.B:
#                 {
#                     double_0 = -900;
#                     break;
#                 }
#                 case AircraftSpeedCategory.C:
#                 {
#                     double_0 = -1100;
#                     break;
#                 }
#                 default:
#                 {
#                     double_0 = -1400;
#                     break;
#                 }
#             }
            aircraftCategory = self.ui.cmbAircraftCategory.currentText()
            if aircraftCategory == "A" or aircraftCategory == "B":
                self.double_0 = -900.0
            elif aircraftCategory == "C":
                self.double_0 = -1100.0
            else:
                self.double_0 = -1400
#             #print self.double_0
#             double num15 = (heightLoss - RDH) / tanVPA;
            num15 = (heightLoss - RDH) / tanVPA;
#             double num16 = 2 * metresPerSecond * sinVPA / 0.784;
            num16 = 2 * metresPerSecond * sinVPA / 0.784;
#             speed = new Speed(10, SpeedUnits.KTS);
            speed = Unit.ConvertKTSToMPS(10.0)
#             double metresPerSecond1 = num15 - (metres9 + num16 * (metresPerSecond + speed.MetresPerSecond));
            metresPerSecond1 = num15 - (metres9 + num16 * (metresPerSecond + speed));
#             if (num6 > 3.2 || pointARP.get_Z() > 900)
#             {
#                 double_0 = Math.Min(double_0, metresPerSecond1);
#             }
            if (num6 > 3.2 or pointARP.z() > 900):
                self.double_0 = min([self.double_0, metresPerSecond1]);
#             distanceTHRtoFAWP = this.pnlTerminationDist.Value;
#             double num17 = distanceTHRtoFAWP.Metres.smethod_17();
            num17 = 0.0
            if self.ui.txtAPV.text() != "":
                num17 = Unit.ConvertNMToMeter(float(self.ui.txtAPV.text()))
#             if (num14 < 2.5)
#             {
#                 throw new Exception(string.Format(Messages.ERR_BAROVNAV_MIN_VPA, num14.ToString("0.0#")));
#             }
            if num14 < 2.5:
                if isPDCheck:
                    calculationResults.append(unicode(Messages.ERR_BAROVNAV_MIN_VPA, "utf-8")%num14)
                else:
                    raise UserWarning, unicode(Messages.ERR_BAROVNAV_MIN_VPA, "utf-8")%num14
            
#             double NM15 = Units.smethod_22(15);
            NM15 = Unit.ConvertNMToMeter(15)
#             double NM30 = Units.smethod_22(30);
            NM30 = Unit.ConvertNMToMeter(30)
#             if (MathHelper.calcDistance(pointARP, self.pointTHR) > (new Distance(10, DistanceUnits.NM)).Metres)
#             {
#                 throw new Exception(string.Format(Messages.ERR_DISTANCE_BETWEEN_X_AND_ARP_EXCEEDS_10_NM, Captions.THR_BIG));
#             }
            if MathHelper.calcDistance(pointARP, self.pointTHR) > Unit.ConvertNMToMeter(10):
                if isPDCheck:
                    calculationResults.append(Messages.ERR_DISTANCE_BETWEEN_X_AND_ARP_EXCEEDS_10_NM%"THR")
                else:
                    raise UserWarning, Messages.ERR_DISTANCE_BETWEEN_X_AND_ARP_EXCEEDS_10_NM%"THR"
#             if (MathHelper.calcDistance(pointARP, pointAPV) > NM30)
#             {
#                 throw new Exception(Messages.ERR_BAROVNAV_APV_ARP_DISTANCE);
#             }
            if MathHelper.calcDistance(pointARP, pointAPV) > NM30:
                if isPDCheck:
                    calculationResults.append(Messages.ERR_BAROVNAV_APV_ARP_DISTANCE)
                else:
                    raise UserWarning, Messages.ERR_BAROVNAV_APV_ARP_DISTANCE
#             double num20 = (metres8 - num9) / Math.Tan(angle30) + 500;
            num20 = (metres8 - num9) / math.tan(angle30) + 500
#             if (MathHelper.calcDistance(self.pointTHR, pointMA) > MathHelper.calcDistance(self.pointTHR, pointFAP))
#             {
#                 throw new Exception(Messages.ERR_BAROVNAV_THR_FAWP_MAWP_DISTANCE);
#             }
            if MathHelper.calcDistance(self.pointTHR, pointMA) > MathHelper.calcDistance(self.pointTHR, pointFAP):
                if isPDCheck:
                    calculationResults.append(Messages.ERR_BAROVNAV_THR_FAWP_MAWP_DISTANCE)
                else:
                    raise UserWarning, Messages.ERR_BAROVNAV_THR_FAWP_MAWP_DISTANCE
#             if (MathHelper.calcDistance(pointMA, pointFAP) < num20)
#             {
#                 throw new Exception(Messages.ERR_INSUFFICIENT_FINAL_APPROACH_SEGMENT_LENGTH);
#             }
            if MathHelper.calcDistance(pointMA, pointFAP) < num20:
                if isPDCheck:
                    calculationResults.append(Messages.ERR_INSUFFICIENT_FINAL_APPROACH_SEGMENT_LENGTH)
                else:
                    raise UserWarning, Messages.ERR_INSUFFICIENT_FINAL_APPROACH_SEGMENT_LENGTH
#             MathHelper.smethod_34(pointMA, MathHelper.distanceBearingPoint(pointMA, rwyDir, 1000), pointARP, NM15, out point3d, out point3d1);
            listResults = []
            MathHelper.smethod_34(pointMA, MathHelper.distanceBearingPoint(pointMA, rwyDir, 1000.0), pointARP, NM15, listResults)
            point3d1 = listResults.pop()
            point3d = listResults.pop()

#             point3d2 = (!MathHelper.smethod_135(rwyDir, MathHelper.getBearing(pointMA, point3d), Units.smethod_0(5), AngleUnits.Radians) ? point3d1 : point3d);
            #point3d2 = (!MathHelper.smethod_135(rwyDir, MathHelper.getBearing(pointMA, point3d), Unit.ConvertDegToRad(5), "Radians") ? point3d1 : point3d);
            if MathHelper.smethod_135(rwyDir, MathHelper.getBearing(pointMA, point3d), Unit.ConvertDegToRad(5), "Radians"):
                point3d2 = point3d
            else:
                point3d2 = point3d1
#             MathHelper.smethod_34(pointMA, MathHelper.distanceBearingPoint(pointMA, rwyDir, 1000), pointARP, NM30, out point3d, out point3d1);
            listResults = []
            MathHelper.smethod_34(pointMA, MathHelper.distanceBearingPoint(pointMA, rwyDir, 1000.0), pointARP, NM30, listResults)
            point3d1 = listResults.pop()
            point3d = listResults.pop()
            
#             point3d3 = (!MathHelper.smethod_135(rwyDir, MathHelper.getBearing(pointMA, point3d), Units.smethod_0(5), AngleUnits.Radians) ? point3d1 : point3d);
            if MathHelper.smethod_135(rwyDir, MathHelper.getBearing(pointMA, point3d), Unit.ConvertDegToRad(5), "Radians"):
                point3d3 = point3d
            else:
                point3d3 = point3d1
#             Point3d point3d9 = MathHelper.distanceBearingPoint(pointFAP, rwyDirLeft, metres8);
            point3d9 = MathHelper.distanceBearingPoint(pointFAP, rwyDirLeft, metres8)
#             print metres8
#             print rwyDirLeft
#             print point3d9
#             print QgisHelper.transformPoint(point3d9.x(), point3d9.y(), False)
#             MathHelper.distanceBearingPoint(pointFAP, rwyDirLeft, metres8 / 2);
            MathHelper.distanceBearingPoint(pointFAP, rwyDirLeft, metres8 / 2);
#             Point3d point3d10 = MathHelper.distanceBearingPoint(pointFAP, rwyDirRight, metres8);
            point3d10 = MathHelper.distanceBearingPoint(pointFAP, rwyDirRight, metres8);
#             MathHelper.distanceBearingPoint(pointFAP, rwyDirRight, metres8 / 2);
            MathHelper.distanceBearingPoint(pointFAP, rwyDirRight, metres8 / 2);
#             Point3d point3d11 = MathHelper.distanceBearingPoint(point3d9, rwyDirBack + angle30, (metres6 - metres8) / Math.Sin(angle30));
            point3d11 = MathHelper.distanceBearingPoint(point3d9, rwyDirBack + angle30, (metres6 - metres8) / math.sin(angle30));
            #print "point3d11:", point3d11.x(), point3d11.y()
#             Point3d point3d12 = MathHelper.distanceBearingPoint(point3d11, rwyDirRight, metres6 / 2);
            point3d12 = MathHelper.distanceBearingPoint(point3d11, rwyDirRight, metres6 / 2);
            #print "point3d12:", point3d12.x(), point3d12.y()
#             Point3d point3d13 = MathHelper.distanceBearingPoint(point3d10, rwyDirBack - angle30, (metres6 - metres8) / Math.Sin(angle30));
            point3d13 = MathHelper.distanceBearingPoint(point3d10, rwyDirBack - angle30, (metres6 - metres8) / math.sin(angle30));
            #print "point3d13:", point3d13.x(), point3d13.y()
#             Point3d point3d14 = MathHelper.distanceBearingPoint(point3d13, rwyDirLeft, metres6 / 2);
            point3d14 = MathHelper.distanceBearingPoint(point3d13, rwyDirLeft, metres6 / 2);
            #print "point3d14:", point3d14.x(), point3d14.y()
#             Point3d point3d15 = MathHelper.distanceBearingPoint(point3d11, rwyDirBack, 5000);
            point3d15 = MathHelper.distanceBearingPoint(point3d11, rwyDirBack, 5000.0);
            #print "point3d15:", point3d15.x(), point3d15.y()
#             Point3d point3d16 = MathHelper.distanceBearingPoint(point3d12, rwyDirBack, 5000);
            point3d16 = MathHelper.distanceBearingPoint(point3d12, rwyDirBack, 5000.0);
            #print "point3d16:", point3d16.x(), point3d16.y()
#             Point3d point3d17 = MathHelper.distanceBearingPoint(point3d13, rwyDirBack, 5000);
            point3d17 = MathHelper.distanceBearingPoint(point3d13, rwyDirBack, 5000.0);
            #print "point3d17:", point3d17.x(), point3d17.y()
#             Point3d point3d18 = MathHelper.distanceBearingPoint(point3d14, rwyDirBack, 5000);
            point3d18 = MathHelper.distanceBearingPoint(point3d14, rwyDirBack, 5000.0);
            #print "point3d18:", point3d18.x(), point3d18.y()
#             Point3d point3d19 = MathHelper.distanceBearingPoint(point3d9, rwyDir + angle30, (metres8 - num9) / Math.Sin(angle30));
            point3d19 = MathHelper.distanceBearingPoint(point3d9, rwyDir + angle30, (metres8 - num9) / math.sin(angle30));
            #print "point3d19:", point3d19.x(), point3d19.y()
#             Point3d point3d20 = MathHelper.distanceBearingPoint(point3d19, rwyDirRight, num9 / 2);
            point3d20 = MathHelper.distanceBearingPoint(point3d19, rwyDirRight, num9 / 2);
            #print "point3d20:", point3d20.x(), point3d20.y()
#             Point3d point3d21 = MathHelper.distanceBearingPoint(point3d10, rwyDir - angle30, (metres8 - num9) / Math.Sin(angle30));
            point3d21 = MathHelper.distanceBearingPoint(point3d10, rwyDir - angle30, (metres8 - num9) / math.sin(angle30));
            #print "point3d21:", point3d21.x(), point3d21.y()
#             Point3d point3d22 = MathHelper.distanceBearingPoint(point3d21, rwyDirLeft, num9 / 2);
            point3d22 = MathHelper.distanceBearingPoint(point3d21, rwyDirLeft, num9 / 2);
            #print "point3d22:", point3d22.x(), point3d22.y()
#             Point3d point3d23 = MathHelper.distanceBearingPoint(pointMA, rwyDirBack, metres9);
            point3d23 = MathHelper.distanceBearingPoint(pointMA, rwyDirBack, metres9);
            #print "point3d23:", point3d23.x(), point3d23.y()
#             Point3d point3d24 = MathHelper.distanceBearingPoint(point3d23, rwyDirLeft, num9);
            point3d24 = MathHelper.distanceBearingPoint(point3d23, rwyDirLeft, num9);
            #print "point3d24:", point3d24.x(), point3d24.y()
#             Point3d point3d25 = MathHelper.distanceBearingPoint(point3d23, rwyDirLeft, num9 / 2);
            point3d25 = MathHelper.distanceBearingPoint(point3d23, rwyDirLeft, num9 / 2);
            #print "point3d25:", point3d25.x(), point3d25.y()
#             Point3d point3d26 = MathHelper.distanceBearingPoint(point3d23, rwyDirRight, num9);
            point3d26 = MathHelper.distanceBearingPoint(point3d23, rwyDirRight, num9);
            #print "point3d26:", point3d26.x(), point3d26.y()
#             Point3d point3d27 = MathHelper.distanceBearingPoint(point3d23, rwyDirRight, num9 / 2);
            point3d27 = MathHelper.distanceBearingPoint(point3d23, rwyDirRight, num9 / 2);
            #print "point3d27:", point3d27.x(), point3d27.y()
#             Point3d point3d28 = MathHelper.distanceBearingPoint(point3d24, rwyDir - angle15, (num10 - num9) / Math.Sin(angle15));
            point3d28 = MathHelper.distanceBearingPoint(point3d24, rwyDir - angle15, (num10 - num9) / math.sin(angle15));
            #print "point3d28:", point3d28.x(), point3d28.y()
#             Point3d point3d29 = MathHelper.distanceBearingPoint(point3d28, rwyDirRight, num10 / 2);
            point3d29 = MathHelper.distanceBearingPoint(point3d28, rwyDirRight, num10 / 2);
            #print "point3d29:", point3d29.x(), point3d29.y()
#             Point3d point3d30 = MathHelper.distanceBearingPoint(point3d26, rwyDir + angle15, (num10 - num9) / Math.Sin(angle15));
            point3d30 = MathHelper.distanceBearingPoint(point3d26, rwyDir + angle15, (num10 - num9) / math.sin(angle15));
            #print "point3d30:", point3d30.x(), point3d30.y()
#             Point3d point3d31 = MathHelper.distanceBearingPoint(point3d30, rwyDirLeft, num10 / 2);
            point3d31 = MathHelper.distanceBearingPoint(point3d30, rwyDirLeft, num10 / 2);
            #print "point3d31:", point3d31.x(), point3d31.y()
#             point3d23 = MathHelper.distanceBearingPoint(point3d2, rwyDirBack, metres10);
            point3d23 = MathHelper.distanceBearingPoint(point3d2, rwyDirBack, metres10);
            #print "point3d23:", point3d23.x(), point3d23.y()
#             Point3d point3d32 = MathHelper.distanceBearingPoint(point3d23, rwyDirLeft, num10);
            point3d32 = MathHelper.distanceBearingPoint(point3d23, rwyDirLeft, num10);
            #print "point3d32:", point3d32.x(), point3d32.y()
#             Point3d point3d33 = MathHelper.distanceBearingPoint(point3d23, rwyDirLeft, num10 / 2);
            point3d33 = MathHelper.distanceBearingPoint(point3d23, rwyDirLeft, num10 / 2);
            #print "point3d33:", point3d33.x(), point3d33.y()
#             Point3d point3d34 = MathHelper.distanceBearingPoint(point3d23, rwyDirRight, num10);
            point3d34 = MathHelper.distanceBearingPoint(point3d23, rwyDirRight, num10);
            #print "point3d34:", point3d34.x(), point3d34.y()
#             Point3d point3d35 = MathHelper.distanceBearingPoint(point3d23, rwyDirRight, num10 / 2);
            point3d35 = MathHelper.distanceBearingPoint(point3d23, rwyDirRight, num10 / 2);
            #print "point3d35:", point3d35.x(), point3d35.y()
#             Point3d point3d36 = MathHelper.distanceBearingPoint(point3d32, rwyDir - angle15, (num11 - num10) / Math.Sin(angle15));
            point3d36 = MathHelper.distanceBearingPoint(point3d32, rwyDir - angle15, (num11 - num10) / math.sin(angle15));
            #print "point3d36:", point3d36.x(), point3d36.y()
#             Point3d point3d37 = MathHelper.distanceBearingPoint(point3d36, rwyDirRight, num11 / 2);
            point3d37 = MathHelper.distanceBearingPoint(point3d36, rwyDirRight, num11 / 2);
            #print "point3d37:", point3d37.x(), point3d37.y()
#             Point3d point3d38 = MathHelper.distanceBearingPoint(point3d34, rwyDir + angle15, (num11 - num10) / Math.Sin(angle15));
            point3d38 = MathHelper.distanceBearingPoint(point3d34, rwyDir + angle15, (num11 - num10) / math.sin(angle15));
            #print "point3d138:", point3d38.x(), point3d38.y()
#             Point3d point3d39 = MathHelper.distanceBearingPoint(point3d38, rwyDirLeft, num11 / 2);
            point3d39 = MathHelper.distanceBearingPoint(point3d38, rwyDirLeft, num11 / 2);
            #print "point3d39:", point3d39.x(), point3d39.y()
#             point3d23 = MathHelper.distanceBearingPoint(point3d3, rwyDirBack, metres11);
            point3d23 = MathHelper.distanceBearingPoint(point3d3, rwyDirBack, metres11);
            #print "point3d23:", point3d23.x(), point3d23.y()
#             Point3d point3d40 = MathHelper.distanceBearingPoint(point3d23, rwyDirLeft, num11);
            point3d40 = MathHelper.distanceBearingPoint(point3d23, rwyDirLeft, num11);
            #print "point3d40:", point3d40.x(), point3d40.y()
#             Point3d point3d41 = MathHelper.distanceBearingPoint(point3d23, rwyDirLeft, num11 / 2);
            point3d41 = MathHelper.distanceBearingPoint(point3d23, rwyDirLeft, num11 / 2);
            #print "point3d41:", point3d41.x(), point3d41.y()
#             Point3d point3d42 = MathHelper.distanceBearingPoint(point3d23, rwyDirRight, num11);
            point3d42 = MathHelper.distanceBearingPoint(point3d23, rwyDirRight, num11);
            #print "point3d42:", point3d42.x(), point3d42.y()
#             Point3d point3d43 = MathHelper.distanceBearingPoint(point3d23, rwyDirRight, num11 / 2);
            point3d43 = MathHelper.distanceBearingPoint(point3d23, rwyDirRight, num11 / 2);
            #print "point3d43:", point3d43.x(), point3d43.y()
#             Point3d[] point3dArray = new Point3d[] { point3d15, point3d11, point3d19, point3d24, point3d28, point3d32, point3d36, point3d40 };
            point3dCollection = [ point3d15, point3d11, point3d19, point3d24, point3d28, point3d32, point3d36, point3d40 ]
#             Point3dCollection point3dCollection = new Point3dCollection(point3dArray);
#             point3dArray = new Point3d[] { point3d16, point3d12, point3d20, point3d25, point3d29, point3d33, point3d37, point3d41 };
#             Point3dCollection point3dCollection1 = new Point3dCollection(point3dArray);
            point3dCollection1 = [point3d16, point3d12, point3d20, point3d25, point3d29, point3d33, point3d37, point3d41]
#             point3dArray = new Point3d[] { point3d18, point3d14, point3d22, point3d27, point3d31, point3d35, point3d39, point3d43 };
#             Point3dCollection point3dCollection2 = new Point3dCollection(point3dArray);
            point3dCollection2 = [point3d18, point3d14, point3d22, point3d27, point3d31, point3d35, point3d39, point3d43]
#             point3dArray = new Point3d[] { point3d17, point3d13, point3d21, point3d26, point3d30, point3d34, point3d38, point3d42 };
#             Point3dCollection point3dCollection3 = new Point3dCollection(point3dArray);
            point3dCollection3 = [point3d17, point3d13, point3d21, point3d26, point3d30, point3d34, point3d38, point3d42]
#             List<BaroVNAV.IBaroVnavSurface> baroVnavSurfaces = new List<BaroVNAV.IBaroVnavSurface>();
            baroVnavSurfaces = []
#             BaroVNAV.BaroVnavSurfaceFAS baroVnavSurfaceFA = new BaroVNAV.BaroVnavSurfaceFAS(self.pointTHR, rwyDir, num12, ISMoc, baroVnavFasSegments);
            baroVnavSurfaceFA = BaroVnavSurfaceFAS(self.pointTHR, rwyDir, num12, ISMoc, baroVnavFasSegments)
#             if (num12 > baroVnavFasSegments[baroVnavFasSegments.Count - 1].xend)
#             {
#                 baroVnavSurfaceFA.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, num12), baroVnavFasSegments[baroVnavFasSegments.Count - 1].ptEnd);
#             }
            if (num12 > baroVnavFasSegments[len(baroVnavFasSegments) - 1].xend):
                baroVnavSurfaceFA.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, num12), baroVnavFasSegments[len(baroVnavFasSegments) - 1].ptEnd)
            self.pointFAF = baroVnavFasSegments[len(baroVnavFasSegments) - 1].ptEnd
            
#             print point3dCollection
#             print self.transformPoints(point3dCollection)
#             print point3dCollection1
#             print self.transformPoints(point3dCollection1)
#             print point3dCollection2
#             print self.transformPoints(point3dCollection2)
#             print point3dCollection3
#             print self.transformPoints(point3dCollection3)
#             for (int i = baroVnavFasSegments.Count - 1; i >= 0; i--)
#             {
#                 baroVnavSurfaceFA.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, baroVnavFasSegments[i].ptEnd, baroVnavFasSegments[i].ptStart);
#             }
            baroVnavFasSegments.reverse()
            for cur in baroVnavFasSegments:
                baroVnavSurfaceFA.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, cur.ptEnd, cur.ptStart)
            baroVnavFasSegments.reverse()

#             baroVnavSurfaces.Add(baroVnavSurfaceFA);
            baroVnavSurfaces.append(baroVnavSurfaceFA)
#             BaroVNAV.BaroVnavSurfaceH baroVnavSurfaceH = new BaroVNAV.BaroVnavSurfaceH(self.pointTHR, rwyDir, double_0, baroVnavFasSegments[0].xfas, baroVnavFasSegments[0].moc, MAMoc);
            baroVnavSurfaceH = BaroVnavSurfaceH(self.pointTHR, rwyDir, self.double_0, baroVnavFasSegments[0].xfas, baroVnavFasSegments[0].moc, MAMoc)
#             baroVnavSurfaceH.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegments[0].xfas), MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, double_0));
            baroVnavSurfaceH.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, baroVnavFasSegments[0].xfas), MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, self.double_0))
#             baroVnavSurfaces.Add(baroVnavSurfaceH);
            baroVnavSurfaces.append(baroVnavSurfaceH)
#             BaroVNAV.BaroVnavSurfaceZ baroVnavSurfaceZ = new BaroVNAV.BaroVnavSurfaceZ(self.pointTHR, rwyDir, double_0, MAMoc, self.percent);
            baroVnavSurfaceZ = BaroVnavSurfaceZ(self.pointTHR, rwyDir, self.double_0, MAMoc, self.percent)
#             baroVnavSurfaceZ.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, self.double_0), MathHelper.distanceBearingPoint(self.pointTHR, rwyDir, num17).smethod_167(self.percent * (num17 - self.double_0)));
            baroVnavSurfaceZ.method_0(point3dCollection, point3dCollection1, point3dCollection2, point3dCollection3, MathHelper.distanceBearingPoint(self.pointTHR, rwyDirBack, self.double_0), MathHelper.distanceBearingPoint(self.pointTHR, rwyDir, num17).smethod_167(self.percent * (num17 - self.double_0)))
#             baroVnavSurfaces.Add(baroVnavSurfaceZ);
            baroVnavSurfaces.append(baroVnavSurfaceZ)
            
#             BaroVNAV.calculationResults = new List<string>();
            self.calculationResults = []
#             List<string> strs = BaroVNAV.calculationResults;
#             calculationResults = []
#             distanceTHRtoFAWP = new Distance(num12);
#             strs.Add(string.Format("{0}\t{1}", "X FAP", distanceTHRtoFAWP.method_0(":u")));
            self.calculationResults.append("X FAP:\t" + str(num12) + " m")
#             List<string> strs1 = BaroVNAV.calculationResults;
#             string tEMPERATURECORRECTION = Captions.TEMPERATURE_CORRECTION;
#             distanceTHRtoFAWP = new Distance(tempCorrection);
#             strs1.Add(string.Format("{0}\t{1}", tEMPERATURECORRECTION, distanceTHRtoFAWP.method_0(":u")));
            self.calculationResults.append("Temperature Correction:\t" + str(self.makeInt(tempCorrection)) + " m")
            self.calculationResults.append("Temperature Correction:\t" + str(self.makeInt(Unit.ConvertMeterToFeet(tempCorrection))) + " ft")
#             List<string> strs2 = BaroVNAV.calculationResults;
#             string mINIMUMVPA = Captions.MINIMUM_VPA;
#             angleGradientSlope = new AngleGradientSlope(num14);
#             strs2.Add(string.Format("{0}\t{1}", mINIMUMVPA, angleGradientSlope.method_0(":u")));
            self.calculationResults.append(unicode("Minimum VPA:\t" + str(num14) + "°", "utf-8"))
#             for (int j = 0; j < baroVnavFasSegments.Count; j++)
#             {
#                 Altitude altitude1 = new Altitude(baroVnavFasSegments[j].moc);
#                 List<string> strs3 = BaroVNAV.calculationResults;
#                 string str = altitude1.method_0(":u");
#                 distanceTHRtoFAWP = new Distance(baroVnavFasSegments[j].xfas);
#                 strs3.Add(string.Format("{0} [{1}]\t{2}", "X FAS", str, distanceTHRtoFAWP.method_0(":u")));
#                 List<string> strs4 = BaroVNAV.calculationResults;
#                 string fASANGLE = Captions.FAS_ANGLE;
#                 string str1 = altitude1.method_0(":u");
#                 angleGradientSlope = new AngleGradientSlope(Units.smethod_1(Math.Atan(baroVnavFasSegments[j].tanafas)));
#                 strs4.Add(string.Format("{0} [{1}]\t{2}", fASANGLE, str1, angleGradientSlope.method_0(":u")));
#             }
            for current in baroVnavFasSegments:
                self.calculationResults.append("X FAS [" + str(current.moc) + "]:\t" + str(current.xfas) + " m")
                self.calculationResults.append(unicode("FAS Angle [" + str(current.moc) + "]:\t" + str(Unit.ConvertRadToDeg(math.atan(current.tanafas))) + "°", "utf-8"))
#             List<string> strs5 = BaroVNAV.calculationResults;
#             distanceTHRtoFAWP = new Distance(self.double_0);
#             strs5.Add(string.Format("{0}\t{1}", "Xz", distanceTHRtoFAWP.method_0(":u")));
            self.calculationResults.append("Xz:\t" + str(self.double_0) + " m")
#             return baroVnavSurfaces;
            return baroVnavSurfaces
    def _Construct(self):
        try:
            # cavas all layers delete    
            define._canvas.setMapTool(QgsMapToolPan(define._canvas))
#             QgisHelper.removeFromCanvas(define._canvas, define._surfaceLayers)              
            surfaceLayers = []      
            results = []
            
#             if define._canvas.mapUnits() != QGis.Meters:
#                 define._units = QGis.Meters
#                 QgisHelper.convertMeasureUnits(QGis.Meters)

            self.baroVnavSurfaces = self.method_48(results)
            
            count = len(self.baroVnavSurfaces)
            if self.ui.cmbConstructionType.currentText() == "2D":
                for surface in self.baroVnavSurfaces:
                    surface.vmethod_1(surfaceLayers, self.baroVnavSurfaces.index(surface) == count - 1)
            else:
                for surface in self.baroVnavSurfaces:
                    surface.vmethod_2(surfaceLayers)
            self.surfaceMapLayer = []
            for layer in surfaceLayers:
                self.surfaceMapLayer.append(layer)
            surfaceLayers.append(self.WPT2Layer())
            surfaceLayers.append(self.nominal2Layer())
            QgisHelper.appendToCanvas(define._canvas, surfaceLayers, SurfaceTypes.BaroVNAV)
            QgisHelper.zoomToLayers(surfaceLayers)
             
            resultString = ""
            for cur in self.calculationResults:
                resultString += cur + "\n"
            QMessageBox.warning(self, "Reports", resultString)
            self.ui.btnEvaluate.setEnabled(True)
        except SyntaxWarning as e:
            QMessageBox.warning(self, "Input Error", "Please input " + e.message)
#             surface.vmethod_1(baroVnavSurfaces.index(surface) == count - 1)
        except UserWarning as e:
            QMessageBox.warning(self, "Input Error", e.message)
        except QgsCsException as e:
            QMessageBox.warning(self, "CoordinateTransform Error", e.message)
#         finally:
#             ''' for Degree '''                 
#             if define._canvas.mapUnits() != QGis.Meters:
#                 define._units = define._canvas.mapUnits()
#                 QgisHelper.convertMeasureUnits(define._canvas.mapUnits())

    def nominal2Layer(self):
        resultLayer = AcadHelper.createVectorLayer("NominalTrack", QGis.Line)
        resultLayer.startEditing()
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPolyline ([self.pointFAWP, self.pointMAHWP]))
        pr = resultLayer.dataProvider()
        pr.addFeatures([feature])
        # resultLayer.addFeature(feature)
            
        resultLayer.commitChanges()
        return resultLayer
        
    def WPT2Layer(self):
        mapUnits = define._canvas.mapUnits()
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                resultLayer = QgsVectorLayer("Point?crs=EPSG:32633", "WPT_BaroVNAV", "memory")
            else:
                resultLayer = QgsVectorLayer("Point?crs=EPSG:4326", "WPT_BaroVNAV", "memory")
        else:
            resultLayer = QgsVectorLayer("Point?crs=%s"%define._mapCrs.authid (), "WPT_BaroVNAV", "memory")

        shpPath = ""
        if define.obstaclePath != None:
            shpPath = define.obstaclePath
        elif define.xmlPath != None:
            shpPath = define.xmlPath
        else:
            shpPath = define.appPath
        er = QgsVectorFileWriter.writeAsVectorFormat(resultLayer, shpPath + "/" + "WPT_BaroVNAV" + ".shp", "utf-8", resultLayer.crs())
        resultLayer = QgsVectorLayer(shpPath + "/" + "WPT_BaroVNAV" + ".shp", "WPT_BaroVNAV", "ogr")

#         if mapUnits == QGis.Meters:
#             resultLayer = QgsVectorLayer("Point?crs=EPSG:32633", "WPT", "memory")
#         else:
#             resultLayer = QgsVectorLayer("Point?crs=EPSG:4326", "WPT", "memory")
        fieldName = "CATEGORY"
        resultLayer.dataProvider().addAttributes( [QgsField(fieldName, QVariant.String)] )
        resultLayer.startEditing()
        fields = resultLayer.pendingFields()
        i = 1
        while i < 4:
            feature = QgsFeature()
            if i == 1:
                feature.setGeometry(QgsGeometry.fromPoint (self.pointFAWP))                
                feature.setFields(fields)
                feature.setAttribute(fieldName, "FAWP")               
            elif i == 2:
                feature.setGeometry(QgsGeometry.fromPoint (self.pointMAHWP))                
                feature.setFields(fields)
                feature.setAttribute(fieldName, "MAHWP")
            elif i == 3:
                feature.setGeometry(QgsGeometry.fromPoint (self.pointMAWP))                
                feature.setFields(fields)
                feature.setAttribute(fieldName, "MAPT")
            pr = resultLayer.dataProvider()
            pr.addFeatures([feature])
            # resultLayer.addFeature(feature)
            i += 1
        resultLayer.commitChanges()
        
        '''FlyOver'''
        strRwyDir = self.ui.txtRwyDir.text()
        if strRwyDir is None or strRwyDir == "":
            strRwyDir = "0"
        symbolFlyOver = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyOver.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyover.svg", 9.0, 0.0)#float(strRwyDir))
        symbolFlyOver.appendSymbolLayer(svgSymLayer)
        renderCatFlyOver = QgsRendererCategoryV2(1, symbolFlyOver,"FlyOver")
         
        '''FlyBy'''
        symbolFlyBy = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
        symbolFlyBy.deleteSymbolLayer(0)
        svgSymLayer = QgsSvgMarkerSymbolLayerV2("Resource/flyby.svg", 9.0, 0.0)#float(strRwyDir))
        symbolFlyBy.appendSymbolLayer(svgSymLayer)
        renderCatFlyBy = QgsRendererCategoryV2(0, symbolFlyBy,"FlyBy")
 
        symRenderer = QgsCategorizedSymbolRendererV2(Expressions.BARO_WPT_EXPRESION, [renderCatFlyOver, renderCatFlyBy])
 
        resultLayer.setRendererV2(symRenderer)
        return resultLayer
        
    def _Evaluate(self):
        self.ui.txtID.setText("")
        self.ui.txtX.setText("")
        self.ui.txtY.setText("")
        self.ui.txtAltitude.setText("")
        self.ui.txtAltitudeM.setText("")
        self.ui.txtSurface.setText("")

        self.ui.txtOCAResults.setText("")
        self.ui.txtOCHResults.setText("")
#         progressMessageBar = define._messagBar.createMessage("Evaluting...")
#         self.progress = QProgressBar()
#         self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)        
#         progressMessageBar.layout().addWidget(self.progress)
#         define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
#         max = 100
#         self.progress.setMaximum(max)
#         self.progress.setValue(1)
#         for ly in define._obstacleLayers:
#             max += ly.featureCount ()             
#         self.progress.setMaximum(max)
        try:
#             ''' for Degree '''                 
#             if define._canvas.mapUnits() != QGis.Meters:
#                 define._units = QGis.Meters
#                 QgisHelper.convertMeasureUnits(QGis.Meters)            
            
            hl = float(self.ui.txtHeightLoss.text())
            cotmacg = 1.0 / self.percent
            cotvpa = 1.0 / math.tan(Unit.ConvertDegToRad(self.GetVPAValue()))
            xz = self.double_0
            self.obstacleModel = BaroVNavObstacles(self.baroVnavSurfaces, hl, cotmacg, cotvpa, xz, self.pointTHR.z(), self.ui.cmbMissedAppEvalution)
            self.obstacleModel.loadObstacles(self.surfaceMapLayer)
#             self.setResultPanel()
#             self.ui.btnMarkSoc.setEnabled(True)
    #         self.obstacleModel.setVerticalHeader()
            self.obstacleModel.setHiddenColumns(self.ui.tblObstacles)
            self.obstacleModel.setTableView(self.ui.tblObstacles)
            self.ui.tabBaroV.setCurrentIndex(1)
            self.criticalObstacle = self.obstacleModel.criticalObstacle
#             self.modelObstaclesFAS.removeRows(0, self.modelObstaclesFAS.rowCount())
#             self.modelObstaclesH.removeRows(0, self.modelObstaclesH.rowCount())
#             self.modelObstaclesZ.removeRows(0, self.modelObstaclesZ.rowCount())
#             
#                         
#             self.loadPointObstacles(self.baroVnavSurfaces)
#             k = self.progress.value()
#             
#             for surface in self.baroVnavSurfaces:
#                 if surface.Type == "FAS":
#                     modelObstacle = self.modelObstaclesFAS
#                 elif surface.Type == "H":
#                     modelObstacle = self.modelObstaclesH
#                 else:
#                     modelObstacle = self.modelObstaclesZ
#                      
#                 count = modelObstacle.rowCount()
#                 i = 0
#                 while i < count:
#                     obstacle = self.getObstacleFromModel(modelObstacle, i)
#                     results = []
#                     num4 = None
#                     if surface.vmethod_0(obstacle, results):
#                         num = results[0]
#                         num1 = results[1]
#                         num2 = results[2]
#                         num3 = results[3]
#                         z = obstacle.Position.z() + obstacle.trees
#                         num5 = None
#                         z1 = None
#                         if (z > num3):
#                             if obstacle.area == ObstacleAreaResult.Secondary:
#                                 pass
#                             num4 = hl
#                             z2 = z - self.pointTHR.z()
#                             if self.ui.cmbMissedAppEvalution.currentIndex() != 0:#BaroVNAV.BaroVnavMaEvaluationMethod.Standard)
#                                 num6 = surface.method_1(obstacle)
#                                 if surface.Type == "Z":
#                                     num6 = min([num6, xz])
#                                 z2 = z2 - (num1 - num2)
#                                 num5 = (z2 * cotmacg + (num6 - xz)) / (cotmacg + cotvpa)
#                                 if (num5 > z2):
#                                     num5 = None
#                             elif surface.Type == "Z":
#                                 num7 = min([surface.method_1(obstacle), xz])
#                                 z2 = z2 - (num1 - num2)
#                                 num5 = (z2 * cotmacg + (num7 - xz)) / (cotmacg + cotvpa)
#                                 if num5 < 0:
#                                     num5 = 0.0
#                             if num5 != None:
#                                 z1 = self.pointTHR.z() + num5 + num4
#                             else:
#                                 num4 = num2 / num1 * num4
#                                 z1 = z + num4
# 
#                             ########################################################3
#                             if self.criticalObstacle == None:
#                                 if num5 == None:
#                                     self.criticalObstacle = BaroVnavCriticalObstacle(obstacle, \
#                                                         None, z1, z1 - self.pointTHR.z(), surface.Type)
#                                 else:
#                                     self.criticalObstacle = BaroVnavCriticalObstacle(obstacle, \
#                                                         num5 + self.pointTHR.z(), z1, z1 - self.pointTHR.z(), surface.Type)
#                             else:
#                                 if num5 == None:
#                                     self.criticalObstacle.assign(obstacle, None, z1, z1 - self.pointTHR.z(), surface.Type)
#                                 else:
#                                     self.criticalObstacle.assign(obstacle, num5 + self.pointTHR.z(), z1, z1 - self.pointTHR.z(), surface.Type)
#                             #BaroVNAV.resultCriticalObst.method_0(obstacle_0, num5 + this.ptTHR.get_Z(), z1, baroVnavObstacle.Surface);
#                         #num, num2, num5 + this.ptTHR.get_Z(), num3, z - num3, num4, z1
#                         if num5 == None:
#                             self.setMocResultToModel(modelObstacle, i, num, num2,\
#                                                   None, num3, z - num3, num4, z1)    
#                         else:
#                             self.setMocResultToModel(modelObstacle, i, num, num2,\
#                                                   num5 + self.pointTHR.z(), num3, z - num3, num4, z1)    
#                     i += 1
#                     k += 1
#                     self.progress.setValue(k)
#             self.setCriticalObstacle()
#             self.ui.tabBaroV.setCurrentIndex(1)
#             define._messagBar.hide()
#             self.progress.setValue(max)
#             self.progress = None
#             self.hideColumns()
#             self.initTblOstacle()
            self.setCriticalObstacle()
            self.obstacleModel.setLocateBtn(self.ui.btnEvaluate_2)
            self.obstacleModel.setFilterFixedString("FAS")
            self.ui.cmbSurface.setCurrentIndex(0)
            self.ui.tblObstacles.setModel(self.obstacleModel)
            self.obstacleModel.setHiddenColumns(self.ui.tblObstacles)
            self.ui.btnExportResult.setDisabled(False)
            
#             self.ui.btnEvaluate_2.setEnabled(True)
        except UserWarning as e:
            QMessageBox.warning(self, "Evaluate Error", e.message)
        except QgsCsException as e:
            QMessageBox.warning(self, "CoordinateTransform Error", e.message)
#         finally:
#             ''' for Degree '''                 
#             if define._canvas.mapUnits() != QGis.Meters:
#                 define._units = define._canvas.mapUnits()
#                 QgisHelper.convertMeasureUnits(define._canvas.mapUnits())

    def saveData(self):
        filePathDir = QFileDialog.getSaveFileName(self, "Save Input Data",QCoreApplication.applicationDirPath (),"Obstclefiles(*.xml)")        
        if filePathDir == "":
            return
        DataHelper.saveInputParameters(filePathDir, self)

    def openData(self):
        filePathDir = QFileDialog.getOpenFileName(self, "Open Input Data",QCoreApplication.applicationDirPath (),"Obstclefiles(*.xml)")        
        if filePathDir == "":
            return
        DataHelper.loadInputParameters(filePathDir, self)
        
    def hideColumns(self):
        self.ui.tblObstacles.hideColumn(13)
        self.ui.tblObstacles.hideColumn(14)
        self.ui.tblObstacles.hideColumn(15)
        self.ui.tblObstacles.hideColumn(16)
        self.ui.tblObstacles.hideColumn(17)
        
    def _PDCheck(self):
        warnings = []
        self.method_48(warnings, True)
        resultString = "Warnings:\n"
        for cur in warnings:
            resultString += cur + "\n"
        
        resultString += "Results:\n"
        for cur in self.calculationResults:
            resultString += cur + "\n"
        QMessageBox.warning(self, "PD Check Results", resultString)

    def _LocateCritical(self):
        if self.criticalObstacle != None:
            fId = self.criticalObstacle.obstacle.featureId
            layerId = self.criticalObstacle.obstacle.layerId
            layer = QgsMapLayerRegistry.instance().mapLayer (layerId)
            layer.select(fId)
            pt = QgsPoint(self.criticalObstacle.obstacle.Position.x(), self.criticalObstacle.obstacle.Position.y())                
            define._canvas.zoomByFactor (0.2, pt)
    def tblObstaclesClicked(self, idx):
        if len(self.ui.tblObstacles.selectedIndexes()) > 0:
            self.ui.btnEvaluate_2.setEnabled(True) 
    def _Locate(self):
        selectedRowIndexes = self.ui.tblObstacles.selectedIndexes()
        self.obstacleModel.locate(selectedRowIndexes)
#         pass
#         for layer in define._obstacleLayers:
#             if isinstance(layer, QgsVectorLayer):
#                 layer.removeSelection()        
#         if len(self.ui.tblObstacles.selectedIndexes()) > 0:
#             indexs = self.ui.tblObstacles.selectedIndexes()     
#             rows = []  
#             obstacleModel = self.obstacleModel  
# #             if self.ui.cmbSurface.currentIndex() == 0:
# #                 obstacleModel = self.modelObstaclesFAS                 
# #             elif self.ui.cmbSurface.currentIndex() == 1:
# #                 obstacleModel = self.modelObstaclesH
# # #             self.ui.tblObstacles.setHorizontalHeader(self.header)
# #             elif self.ui.cmbSurface.currentIndex() == 2:
# #                 obstacleModel = self.modelObstaclesZ
#             layer = None
#             scalePoint = None
#             for index in indexs:
#                 if not(index.row() in rows):
#                     rows.append(index.row())
#                     sourceRow = self.obstacleModel.mapToSource(index).row()
#                     id1 = int(obstacleModel.source.item(sourceRow, 0).text())
#                     layerId = obstacleModel.source.item(sourceRow, 1).text()
#                     positonx = float(obstacleModel.source.item(sourceRow, 3).text())
#                     positony = float(obstacleModel.source.item(sourceRow, 4).text())
#                     scalePoint = QgsPoint(positonx, positony) 
#                     layer = QgsMapLayerRegistry.instance().mapLayer (layerId)
#                     if isinstance(layer, QgsVectorLayer):
#                         layer.select(id1)
#             if len(rows) > 1:
#                 define._canvas.zoomToSelected(layer)
#             else:
#                 define._canvas.zoomByFactor (0.2, scalePoint)
#         else:
#             self._LocateCritical()
    def _cmbSurfaceChanged(self):
        if self.ui.cmbSurface.currentIndex() == 0 and self.obstacleModel != None:
            self.obstacleModel.setFilterFixedString("FAS")
            self.ui.tblObstacles.setModel(self.obstacleModel)
#             self.ui.tblObstacles.setHorizontalHeader(self.header)
        elif self.ui.cmbSurface.currentIndex() == 1:
            self.obstacleModel.setFilterFixedString("H")
            self.ui.tblObstacles.setModel(self.obstacleModel)
#             self.ui.tblObstacles.setHorizontalHeader(self.header)
        elif self.ui.cmbSurface.currentIndex() == 2:
            self.obstacleModel.setFilterFixedString("Z")
            self.ui.tblObstacles.setModel(self.obstacleModel)
#         self.hideColumns()

#             self.ui.tblObstacles.setHorizontalHeader(self.header)
    def _CaptureCoordARP(self):
        if self.ui.btnCaptureCoordARP.isChecked():
            define._canvas.setMapTool(self.CaptureCoordARPTool)
            self.ui.btnCaptureCoordThr.setChecked(False)
            self.ui.btnCaptureDirRwy.setChecked(False)
        else:
            define._canvas.setMapTool(QgsMapToolPan(define._canvas))
#         try:
#         pointArp = Point3D(self.ui.txtARPX.text().toFloat()[0], self.ui.txtARPY.text().toFloat()[0])
#         pointThr = Point3D(self.ui.txtThrX.text().toFloat()[0], self.ui.txtThrY.text().toFloat()[0])
#         self.ui.txtRwyDir.setText(str(Unit.ConvertRadToDeg(MathHelper.getBearing(pointArp, pointThr))))
# #         except:
# #             pass
            
    def _CaptureCoordThr(self):
        if self.ui.btnCaptureCoordThr.isChecked():
            define._canvas.setMapTool(self.CaptureCoordThrTool)            
            self.ui.btnCaptureCoordARP.setChecked(False)
            self.ui.btnCaptureDirRwy.setChecked(False)
        else:
            define._canvas.setMapTool(QgsMapToolPan(define._canvas))
#         try:
#         pointArp = Point3D(self.ui.txtARPX.text().toFloat()[0], self.ui.txtARPY.text().toFloat()[0])
#         pointThr = Point3D(self.ui.txtThrX.text().toFloat()[0], self.ui.txtThrY.text().toFloat()[0])
#         self.ui.txtRwyDir.setText(str(Unit.ConvertRadToDeg(MathHelper.getBearing(pointArp, pointThr))))
# #         except:
#             pass
            
    def _CaptureRunwayDir(self):
        if self.ui.btnCaptureDirRwy.isChecked():
            define._canvas.setMapTool(self.CaptureBearingTool)
           
            
            self.ui.btnCaptureCoordThr.setChecked(False)
            self.ui.btnCaptureCoordARP.setChecked(False)
        else:
            define._canvas.setMapTool(QgsMapToolPan(define._canvas))
            
    def _aircraftCategoryChanged(self):
        index = self.ui.cmbAircraftCategory.currentIndex()
        if index == 0: # A
            self.ui.txtMaxIAS.setText("100")
            self.ui.txtMaxIASatTHR.setText("90")
        elif index == 1: # B
            self.ui.txtMaxIAS.setText("130")
            self.ui.txtMaxIASatTHR.setText("120")
        elif index == 2: # C
            self.ui.txtMaxIAS.setText("160")
            self.ui.txtMaxIASatTHR.setText("140")
        elif index == 3: # D
            self.ui.txtMaxIAS.setText("185")
            self.ui.txtMaxIASatTHR.setText("165")
        elif index == 4: # E
            self.ui.txtMaxIAS.setText("230")
            self.ui.txtMaxIASatTHR.setText("210")
        elif index == 5: # Custom
            self.ui.txtMaxIAS.setText("185")
            self.ui.txtMaxIASatTHR.setText("165")
        
    def exit(self):
        self.reject()
    def reject(self):        
        self.CaptureBearingTool.rubberBand.reset(QGis.Line)
        define._canvas.setMapTool(QgsMapToolPan(define._canvas))
        QDialog.reject(self)
        
    def resultPointValueListMethodArp(self, resultValueList):
        if len(resultValueList) > 0: 
            self.ui.txtARPX.setText(resultValueList[1])
            self.ui.txtARPY.setText(resultValueList[2])
#             if resultValueList[3] == None or resultValueList[3] == "" or resultValueList[3] == '':
#                 self.txtAltitudeM.setText("0")
#             else:
            self.ui.txtARPAltM.setText(resultValueList[3])
    def resultPointValueListMethodThr(self, resultValueList):
        if len(resultValueList) > 0: 
            self.ui.txtThrX.setText(resultValueList[1])
            self.ui.txtThrY.setText(resultValueList[2])
#             if resultValueList[3] == None or resultValueList[3] == "" or resultValueList[3] == '':
#                 self.txtAltitudeM.setText("0")
#             else:
            self.ui.txtThrAltM.setText(resultValueList[3])
    def _chageFromMToFt_ARP(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.ui.txtARPAltFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.ui.txtARPAltM.text())), 4)))
            except ValueError:
                self.ui.txtARPAltFt.setText("")
            
    def _chageFromFtToM_ARP(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.ui.txtARPAltM.setText(str(round(Unit.ConvertFeetToMeter(float(self.ui.txtARPAltFt.text())), 4)))
            except ValueError:
                self.ui.txtARPAltM.setText("")
            
    def _chageFromMToFt_Thr(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.ui.txtThrAltFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.ui.txtThrAltM.text())), 4)))
            except ValueError:
                self.ui.txtThrAltFt.setText("")
    def _chageFromFtToM_Thr(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.ui.txtThrAltM.setText(str(round(Unit.ConvertFeetToMeter(float(self.ui.txtThrAltFt.text())), 4)))
            except ValueError:
                self.ui.txtThrAltM.setText("")
          
    def enableTxtAPV(self):
        if self.ui.frame_APV.isEnabled():
            self.ui.frame_APV.setDisabled(True)
            self.ui.txtAPV.setText("")
        else:
            self.ui.txtAPV.setText(str(self.segmentTerminationDist))
            self.ui.frame_APV.setEnabled(True)
    def enableTxtMissApPt(self):
        if self.ui.frame_MissApPt.isEnabled():
            self.ui.frame_MissApPt.setDisabled(True)
            self.ui.txtMissedAppPoint.setText("")
        else:
            self.ui.txtMissedAppPoint.setText(str(self.mapPtDist))
            self.ui.frame_MissApPt.setEnabled(True)
            
#         self.ui.txtMaxIAS.textChanged.connect(self._iasChanged)
#         self.ui.txtMissedAppPoint.textChanged.connect(self._missedAppPtChanged)
#         self.ui.txtAPV.textChanged.connect(self._apvChanged)
#         self.ui.cmbAircraftCategory.currentIndexChanged.connect(self._aircraftCategoryChanged)
#         self.ui.cmbAPV.currentIndexChanged.connect(self._apvChanged)
#         self.ui.cmbMissedAppPoint.currentIndexChanged.connect(self._cmbMissedAppPtChanged)
#         self.ui.txtMaxIASatTHR.textChanged.connect(self._iasAtThrChanged)
#         self.ui.txtARPAltM.textChanged.connect(self._arpAltChanged)
#         self.ui.cmbVerticalPathAngle.currentIndexChanged.connect(self._vpaChanged)
    def _iasChanged(self):
        try:
            self.customIas = float(self.ui.txtMaxIAS.text())
        except ValueError:
            self.customIas = 0.0
    def _missedAppPtChanged(self):
        try:
            if self.ui.txtMissedAppPoint.isEnabled():
                self.mapPtDist = float(self.ui.txtMissedAppPoint.text())
        except ValueError:
            self.mapPtDist = 0.0
    def _apvChanged(self):
        try:
            if self.ui.txtAPV.isEnabled():
                self.segmentTerminationDist = float(self.ui.txtAPV.text())
        except ValueError:
            self.segmentTerminationDist = 0.0
    def _iasAtThrChanged(self):
        self.calcHeightLoss()
    def _arpAltChanged(self):
        self.calcHeightLoss()
    def _vpaChanged(self):
        self.calcHeightLoss()
    def exportResult(self):
        dlg = ExportDlg(self)
        columnNames = []
        if self.obstacleModel != None:
            columnNames = self.obstacleModel.fixedColumnLabels
        self.stModel = QStandardItemModel()
        for i in range(len(columnNames)):
            stItem = QStandardItem(columnNames[i])
            stItem.setCheckable(True)
            checkFlag = True
            for hideColName in self.obstacleModel.hideColumnLabels:
                if columnNames[i] == hideColName:
                    checkFlag = False
                    break
            if checkFlag: 
                stItem.setCheckState(Qt.Checked)
            else:
                stItem.setCheckState(Qt.Unchecked)
            self.stModel.setItem(i, 0, stItem)
        if len(columnNames) <= 0:
            return
        dlg.ui.txtHeading.setText("APV/Baro-VNAV_Export")
        dlg.ui.listColumns.setModel(self.stModel)
        result = dlg.exec_()
#         return (result, dlg.resultHideColumnIndexs)
        resultHideColumnNames = dlg.resultHideColumnIndexs
        if not result:
            return
        
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return        
        filterList = ["FAS", "H", "Z"]
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, "APV/Baro-VNAV Surfaces", self.ui.tblObstacles, filterList, parameterList, resultHideColumnNames)
        self.obstacleModel.setFilterFixedString(filterList[self.ui.cmbSurface.currentIndex()])
    def measureToolAPV(self):
        measureAPV = MeasureTool(define._canvas, self.ui.txtAPV, DistanceUnits.NM)
        define._canvas.setMapTool(measureAPV)
    def measureToolMAPoint(self):
        measureMAPoint = MeasureTool(define._canvas, self.ui.txtMissedAppPoint, DistanceUnits.NM)
        define._canvas.setMapTool(measureMAPoint)
    def makeInt(self, double_0):
        return round(double_0)# + 0.5)
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Aerodrome", "group"))
#         parameterList.append(("X", self.ui.txtARPX.text()))
#         parameterList.append(("Y", self.ui.txtARPY.text()))
        DataHelper.strPnlPositionParameter(self.ui.txtARPX.text(), self.ui.txtARPY.text(), parameterList)
#         position = Point3D(float(self.ui.txtARPX.text()), float(self.ui.txtARPY.text()), 0)
#         positionDegree = QgisHelper.Meter2DegreePoint3D(position)        
#         parameterList.append(("Lat", QgisHelper.strDegree(positionDegree.y())))
#         parameterList.append(("Lon", QgisHelper.strDegree(positionDegree.x())))
        parameterList.append(("Altitude", self.ui.txtARPAltM.text() + " m/" + self.ui.txtARPAltFt.text() + " ft"))
        parameterList.append(("Minimum Temperature", self.ui.txtMinTemperature.text() + unicode(" °C", "utf-8")))
        parameterList.append(("Runway", "group"))
#         parameterList.append(("X", self.ui.txtThrX.text()))
#         parameterList.append(("Y", self.ui.txtThrY.text()))
#         position = Point3D(float(self.ui.txtThrX.text()), float(self.ui.txtThrY.text()), 0)
#         positionDegree = QgisHelper.Meter2DegreePoint3D(position)        
#         parameterList.append(("Lat", QgisHelper.strDegree(positionDegree.y())))
#         parameterList.append(("Lon", QgisHelper.strDegree(positionDegree.x())))
        DataHelper.strPnlPositionParameter(self.ui.txtThrX.text(), self.ui.txtThrY.text(), parameterList)
        parameterList.append(("Altitude", self.ui.txtThrAltM.text() + " m/" + self.ui.txtThrAltFt.text() + " ft"))
        parameterList.append(("Direction", self.ui.txtRwyDir.text() + unicode(" °", "utf-8")))
        
        parameterList.append(("IS(%s)"%self.ui.cmbISType.currentText() , self.ui.txtOCA.text() + " ft"))
        parameterList.append(("ISMOC", self.ui.txtISMoc.text() + " m"))
        parameterList.append(("RDH at THR", self.ui.txtRDHatTHR.text() + "m"))
        parameterList.append(("VPA", self.ui.cmbVerticalPathAngle.currentText() + unicode(" °", "utf-8")))
        parameterList.append(("THR to FAWP Distance", self.ui.txtTHRtoFAWP.text() + " nm"))
        parameterList.append(("Max.IAS", self.ui.txtMaxIAS.text() + " kts"))
        parameterList.append(("Max. IAS at THR", self.ui.txtMaxIASatTHR.text() + " kts"))
        parameterList.append(("Height Loss", self.ui.txtHeightLoss.text() + " m"))
        parameterList.append(("APV(%s)"%self.ui.cmbAPV.currentText(), self.ui.txtAPV.text() + " nm" ))
        parameterList.append(("MAP(%s)"%self.ui.cmbMissedAppPoint.currentText(), self.ui.txtMissedAppPoint.text() + " nm"))
        parameterList.append(("MACG", self.ui.txtMissedAppClimb.text() + " %"))
        parameterList.append(("MAMOC", self.ui.txtMissedAppMOC.text() + " m"))
        parameterList.append(("MAE", self.ui.cmbMissedAppEvalution.currentText()))
        parameterList.append(("Construction Type", self.ui.cmbConstructionType.currentText())) 
        parameterList.append(("Results / Checked Obstacles", "group"))
        parameterList.append(("Critical Obstacle", "group"))
        parameterList.append(("ID", self.ui.txtID.text()))
        parameterList.append(("X", self.ui.txtX.text()))
        parameterList.append(("Y", self.ui.txtY.text()))
        if self.ui.txtX.text() != "" and self.ui.txtY.text() != "":        
            position = Point3D(float(self.ui.txtX.text()), float(self.ui.txtY.text()), 0)
            positionDegree = QgisHelper.Meter2DegreePoint3D(position)        
            parameterList.append(("Lat", QgisHelper.strDegree(positionDegree.y())))
            parameterList.append(("Lon", QgisHelper.strDegree(positionDegree.x())))
#         DataHelper.strPnlPositionParameter(self.ui.txtX.text(), self.ui.txtY.text(), parameterList)
        parameterList.append(("Altitude", self.ui.txtAltitude.text() + " m/" + self.ui.txtAltitudeM.text() + " ft"))       
        parameterList.append(("Surface", self.ui.txtSurface.text()))
        parameterList.append(("Result", "group"))
        parameterList.append(("OCH", self.ui.txtOCHResults.text() + " " + self.ui.cmbUnits.currentText()))
        parameterList.append(("OCA", self.ui.txtOCAResults.text() + " " + self.ui.cmbUnits.currentText()))
        parameterList.append(("Checked Obstacles", "group"))
        self.obstacleModel.setFilterFixedString("FAS")
        c = self.obstacleModel.rowCount()
        parameterList.append(("Number of Checked Obstacles(FAS)", str(c)))  
        self.obstacleModel.setFilterFixedString("H")
        c = self.obstacleModel.rowCount()
        parameterList.append(("Number of Checked Obstacles(H)", str(c)))  
        self.obstacleModel.setFilterFixedString("Z")
        c = self.obstacleModel.rowCount()
        parameterList.append(("Number of Checked Obstacles(Z)", str(c)))  
        return parameterList             
class BaroVNavObstacles(ObstacleTable):
    def __init__(self, surfacesList, hl, cotmacg, cotvpa, xz, pointThrZ, cmbMissedAppEvalution):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
        self.surfaceType = SurfaceTypes.BaroVNAV
        self.hl = hl
        self.cotmacg = cotmacg
        self.cotvpa = cotvpa
        self.xz = xz
        self.pointThrZ = pointThrZ
        self.cmbMissedAppEvalution = cmbMissedAppEvalution
        self.criticalObstacle = None
#     private string title;
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexArea = fixedColumnCount 
        self.IndexDistInSecM = fixedColumnCount + 1
        self.IndexMocAppliedM = fixedColumnCount + 2
        self.IndexEqAltM = fixedColumnCount + 3
        self.IndexEqAltFt = fixedColumnCount + 4
        self.IndexSurfAltM = fixedColumnCount + 5
        self.IndexDifferenceM = fixedColumnCount + 6
        self.IndexHLAppliedM = fixedColumnCount +7
        self.IndexOcaFt = fixedColumnCount + 8
        self.IndexCritical = fixedColumnCount + 9
        self.IndexSurface = fixedColumnCount + 10
          
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.Area,
                ObstacleTableColumnType.DistInSecM,
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.EqAltM,
                ObstacleTableColumnType.EqAltFt,
                ObstacleTableColumnType.SurfAltM,
                ObstacleTableColumnType.DifferenceM,
                ObstacleTableColumnType.HLAppliedM,
                ObstacleTableColumnType.OcaFt,
                ObstacleTableColumnType.Critical,
                ObstacleTableColumnType.Surface
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
  
    def addObstacleToModel(self, obstacle, checkResult):
        ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
        row = self.source.rowCount() - 1
#         colCount = self.source.columnCount()
           
        item = QStandardItem(str(checkResult[0]))
        item.setData(checkResult[0])
        self.source.setItem(row, self.IndexArea, item)
           
        item = QStandardItem(str(checkResult[1]))
        item.setData(checkResult[1] if checkResult[1] != None else -9999)
        self.source.setItem(row, self.IndexDistInSecM, item)
           
        item = QStandardItem(str(checkResult[2]))
        item.setData(checkResult[2] if checkResult[2] != None else -9999)
        self.source.setItem(row, self.IndexMocAppliedM, item)
           
        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3] if checkResult[3] != None else -9999)
        self.source.setItem(row, self.IndexEqAltM, item)
           
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[3]) if checkResult[3] != None else -9999)
        self.source.setItem(row, self.IndexEqAltFt, item)
        
        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4] if checkResult[4] != None else -9999)
        self.source.setItem(row, self.IndexSurfAltM, item)
   
        item = QStandardItem(str(checkResult[5]))
        item.setData(checkResult[5] if checkResult[5] != None else -9999)
        self.source.setItem(row, self.IndexDifferenceM, item)
        
        item = QStandardItem(str(checkResult[6]))
        item.setData(checkResult[6] if checkResult[6] != None else -9999)
        self.source.setItem(row, self.IndexHLAppliedM, item)
        
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[7])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[7]) if checkResult[7] != None else -9999)
        self.source.setItem(row, self.IndexOcaFt, item)
        
        if (checkResult[5] <= 0):
            CriticalCheck = "No"
        else:
            CriticalCheck = "Yes"
        item = QStandardItem(CriticalCheck)
        item.setData(CriticalCheck)
        self.source.setItem(row, self.IndexCritical, item)        
        
        item = QStandardItem(str(checkResult[8]))
        item.setData(checkResult[8])
        self.source.setItem(row, self.IndexSurface, item)
  
    def checkObstacle(self, obstacle):
        for surface in self.surfacesList:
            results = []
            num4 = None
            if surface.vmethod_0(obstacle, results):
                num = results[0]
                num1 = results[1]
                num2 = results[2]
                num3 = results[3]
                z = obstacle.Position.z() + obstacle.trees
                num5 = None
                z1 = None
                if (z > num3):
                    if obstacle.area == ObstacleAreaResult.Secondary:
                        pass
                    num4 = self.hl
                    z2 = z - self.pointThrZ
                    if self.cmbMissedAppEvalution.currentIndex() != 0:#BaroVNAV.BaroVnavMaEvaluationMethod.Standard)
                        num6 = surface.method_1(obstacle)
                        if surface.Type == "Z":
                            num6 = min([num6, self.xz])
                        z2 = z2 - (num1 - num2)
                        num5 = (z2 * self.cotmacg + (num6 - self.xz)) / (self.cotmacg + self.cotvpa)
                        if (num5 > z2):
                            num5 = None
                    elif surface.Type == "Z":
                        num7 = min([surface.method_1(obstacle), self.xz])
                        z2 = z2 - (num1 - num2)
                        num5 = (z2 * self.cotmacg + (num7 - self.xz)) / (self.cotmacg + self.cotvpa)
                        if num5 < 0:
                            num5 = 0.0
                    if num5 != None:
                        z1 = self.pointThrZ + num5 + num4
                    else:
                        num4 = num2 / num1 * num4
                        z1 = z + num4

                    ########################################################3
                    if self.criticalObstacle == None:
                        if num5 == None:
                            self.criticalObstacle = BaroVnavCriticalObstacle(obstacle, \
                                                None, z1, z1 - self.pointThrZ, surface.Type)
                        else:
                            self.criticalObstacle = BaroVnavCriticalObstacle(obstacle, \
                                                num5 + self.pointThrZ, z1, z1 - self.pointThrZ, surface.Type)
                    else:
                        if num5 == None:
                            self.criticalObstacle.assign(obstacle, None, z1, z1 - self.pointThrZ, surface.Type)
                        else:
                            self.criticalObstacle.assign(obstacle, num5 + self.pointThrZ, z1, z1 - self.pointThrZ, surface.Type)
                    #BaroVNAV.resultCriticalObst.method_0(obstacle_0, num5 + this.ptTHR.get_Z(), z1, baroVnavObstacle.Surface);
                #num, num2, num5 + this.ptTHR.get_Z(), num3, z - num3, num4, z1
                if num5 == None:
                    checkList =[obstacle.area, num, num2, None, num3, z-num3, num4, z1, surface.Type]
                    self.addObstacleToModel(obstacle, checkList)    
                else:
                    checkList =[obstacle.area, num, num2, num5 + self.pointThrZ, num3, z - num3, num4, z1, surface.Type]
                    self.addObstacleToModel(obstacle, checkList)    
            
                           
        return ObstacleTable.checkObstacle(self, obstacle)
    def setHiddenColumns(self, tableView):
        tableView.hideColumn(self.IndexAltFt)
        tableView.hideColumn(self.IndexTreesFt)
        tableView.hideColumn(self.IndexSurface)
        ObstacleTable.setHiddenColumns(self, tableView)
  
#     def getExtentForLocate(self, sourceRow):
#         surfaceType = self.source.item(sourceRow, self.IndexSurface).text()
#         surfaceLayers = QgisHelper.getSurfaceLayers(self.surfaceType)
#         rect = QgsRectangle()
#         rect.setMinimal()
#         for sfLayer in surfaceLayers:
#             features = sfLayer.getFeatures()
#             for feature in features:
#                 surfaceString = feature.attribute("surface").toString()
#                 if surfaceString == surfaceType:
#                     geom = feature.geometry()
#                     rect.combineExtentWith(geom.boundingBox())
#         return rect