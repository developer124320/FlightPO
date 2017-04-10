# -*- coding: UTF-8 -*-
'''
Created on Mar 19, 2015

@author: jin
'''
import math

from PyQt4.QtGui import QColor, QDialog, QMessageBox, QLineEdit, QTextDocument, QPushButton, QAbstractItemView, QFont, QComboBox, QFileDialog, QMenu
from PyQt4.QtCore import QSize, QCoreApplication, Qt, QSizeF, QString
from FlightPlanner.Ils.ui_OasDlg import Ui_OsaDlg
from PyQt4.QtCore import SIGNAL
from FlightPlanner.Ils.OasConstantsDlg import OasConstantsDlg
from FlightPlanner.validations import Validations
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.helpers import Speed, Altitude, AngleGradientSlope, MathHelper, Unit, Distance
from qgis.gui import QgsMapTool, QgsTextAnnotationItem, QgsAnnotationItem, QgsRubberBand, QgsMapToolPan
from qgis.core import QgsVectorLayer, QgsRectangle, QGis, QgsFeature, QgsGeometry, QgsPoint, QgsField, QgsRendererCategoryV2, QgsSymbolV2, QgsCategorizedSymbolRendererV2
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.types import OasCategory, Point3D, ConstructionType, SurfaceTypes, OasMaEvaluationMethod, OasSurface, DistanceUnits, AltitudeUnits, SelectionModeType
from FlightPlanner.Ils.OasObstacles import OasCriticalObstacle, OasObstacles
from FlightPlanner.Ils.OasConstants import OasConstants
from FlightPlanner.Ils.IlsOas import OasSurfaces
from FlightPlanner.messages import Messages
from FlightPlanner.captureCoordinateTool import CaptureCoordinateTool
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.Captions import Captions
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.Obstacle.Obstacle import Obstacle
from Type.Geometry import Feature
from Type.switch import switch
import define


class OasDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent, catType = "ILS"):
        QDialog.__init__(self, parent)

        # self.ui = Ui_OsaDlg()
        # self.parametersPanel = self.ui
        # FlightPlanBaseDlg.initParametersPan(self)
        self.ui = Ui_OsaDlg()
        self.manualPolygon = None

        self.mapToolPan = None
        self.toolSelectByPolygon = None

        self.ui.setupUi(self, catType)
        QgisHelper.matchingDialogSize(self, 500, 400)
        # self.ui.txtTrack.setText("")
        self.ui.btnEvaluate.setEnabled(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        
        self.ui.cmbConstructionType.Items = [ConstructionType.Construct2D, ConstructionType.Construct3D]
        if catType == "ILS":
            self.surfaceType = SurfaceTypes.IlsOas

            self.ui.cmbOasCategory.Items = [OasCategory.ILS1, OasCategory.ILS2, OasCategory.ILS2AP]#, OasCategory.SBAS_APV1, OasCategory.SBAS_APV2, OasCategory.SBAS_CAT1]
        else:
            self.surfaceType = SurfaceTypes.SbasOas
            self.ui.txtContourHeight.Visible = False
            self.ui.cmbOasCategory.Items = [OasCategory.SBAS_APV1, OasCategory.SBAS_APV2, OasCategory.SBAS_CAT1]
        self.setWindowTitle(self.surfaceType)
        self.ui.cmbMAMethod.Items = ["XE datum (std.)", "GP'"]
        self.ui.cmbAcCategory.Items = ["A", "B", "C", "D", "DL"]
        self.ui.cmbSelectionMode.Items = [SelectionModeType.Automatic, SelectionModeType.Manual]
        self.ui.cmbMACG.Items = ["5", "4", "3", "2.5", "2"]
        self.ui.cmbMACG.SelectedIndex = 3
        self.ui.cmbGPA.Add("3.0")
        self.ui.cmbMACG.Add("2.5")
        self.ui.cmbUnits.addItems(["meter", "feet"])
        self.ui.cmbUnits.setCurrentIndex(1)
        self.ui.cmbUnits.currentIndexChanged.connect(self.setCriticalObstacle)
        self.oasCategoryChange()
        self.acCategoryChange()
        self.ui.cmbSurface.addItems(["All", OasSurface.OFZ, OasSurface.W, OasSurface.WS, OasSurface.X1, OasSurface.X2, OasSurface.Y1, OasSurface.Y2, OasSurface.Z])
        # Signal and Slot
        self.connect(self.ui.cmbAcCategory, SIGNAL("Event_0"), self.acCategoryChange)
        self.connect(self.ui.cmbGPA, SIGNAL("Event_0"), self.GPAChange)
        self.ui.lblConstants.setTextFormat(Qt.RichText)
        self.ui.lblConstants.setText("<html><head/><body><p><a href=\"asd\"><span style=\" text-decoration: underline color:#0000ff\">Constants</span></a></p></body></html>")
#         event = QAccessibleEvent(self.ui.lblConstants, QAccessible.HypertextLinkActivated)
#         QAccessible.updateAccessibility(event)
#         self.ui.lblConstants.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
#         self.connect(self.ui.lblConstants, SIGNAL("linkActivated()"), SLOT("OasConstantsShow()")
        self.ui.btnOpenData.clicked.connect(self.openData)
        self.ui.btnSaveData.clicked.connect(self.saveData)
        self.ui.lblConstants.linkActivated.connect(self.OasConstantsShow)
        self.connect(self.ui.cmbOasCategory, SIGNAL("Event_0"),self.oasCategoryChange)
        self.ui.btnConstruct.clicked.connect(self.construct)
        self.ui.btnEvaluate.clicked.connect(self.evaluate)
        self.ui.btnClose.clicked.connect(self.reject)
        self.ui.btnClose_2.clicked.connect(self.reject)
        self.ui.cmbSurface.currentIndexChanged.connect(self.surfaceChanged)

        # self.connect(self.ui.pnlThr, SIGNAL("positionChanged"), self.changeDistGradient)
        # self.connect(self.ui.pnlThr, SIGNAL("positionChanged"), self.changeDistGradient)

        # self.ui.btnCaptureTrack.clicked.connect(self._captureTrack)
        # self.ui.btnCaptureDLT.clicked.connect(self._captureDLT)
        # self.ui.btnCaptureDLT.setCheckable(True)
        # self.ui.btnCaptureTrack.setCheckable(True)
        self.thrAnnotation= QgsTextAnnotationItem(define._canvas)
        self.thrAnnotation.setDocument(QTextDocument("THR"))
        self.thrAnnotation.setFrameSize( QSizeF( 30, 20 ) )
        self.thrAnnotation.hide()
        # self.CaptureBearingTool = CaptureBearingTool(define._canvas, self.ui.txtTrack)
        # self.distanceMeasureTool = MeasureTool(define._canvas, self.ui.txtDLT, DistanceUnits.M)
        self.flag = 0
        
        self.obstaclesModel = OasObstacles(None, self.manualPolygon)
        self.obstaclesModel.setTableView(self.ui.tblObstacles)
        self.obstaclesModel.setLocateBtn(self.ui.btnLocate)
        self.obstaclesModel.setSurfaceType(self.surfaceType)
        
        self.ui.tblObstacles.setModel(self.obstaclesModel)
        self.ui.tblObstacles.setSortingEnabled(True)
        self.ui.tblObstacles.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.connect(self.ui.tblObstacles, SIGNAL("tableViewObstacleMouseReleaseEvent_rightButton"), self.tableViewObstacleMouseTeleaseEvent_rightButton)
        self.connect(self.ui.tblObstacles, SIGNAL("pressedEvent"), self.tblObstacles_pressed)


        self.ui.btnMarkSoc.clicked.connect(self.markSocClicked)
        self.ui.toolButton.clicked.connect(self.criticalLocate)
        self.connect(self.ui.cmbSelectionMode, SIGNAL("Event_0"), self.cmbSelectionModeChanged)
                
        self.socRubber = None
        self.socAnnotation = QgsTextAnnotationItem(define._canvas)
        self.socAnnotation.setDocument(QTextDocument(Captions.SOC))
        self.socAnnotation.setFrameBackgroundColor(Qt.white)
        self.socAnnotation.setFrameSize(QSizeF(30, 20))
        self.socAnnotation.setFrameColor(Qt.magenta)
        self.socAnnotation.hide()
        
        font = QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.btnExportResult = QPushButton("")
        self.btnExportResult.setFont(font)
        self.btnExportResult.setIcon(self.ui.iconExport)
        self.btnExportResult.setToolTip("Export Result")
        self.ui.verticalLayout_4.insertWidget(3, self.btnExportResult)
        self.btnExportResult.setDisabled(True)
        self.btnExportResult.clicked.connect(self.exportResult)
        
        lstTextControls = self.ui.groupBox_11.findChildren(QLineEdit)
        for ctrl in lstTextControls:
            ctrl.textChanged.connect(self.initResultPanel)
        lstTextControls = self.ui.groupBox_11.findChildren(QComboBox)
        for ctrl in lstTextControls:
            ctrl.currentIndexChanged.connect(self.initResultPanel)

        self.btnExportResult.setIconSize(QSize(32,32))

        self.connect(self.ui.pnlThr, SIGNAL("positionChanged"), self.calcRwyBearing)
        self.connect(self.ui.pnlRwyEnd, SIGNAL("positionChanged"), self.calcRwyBearing)
        self.ui.cmbGPA.SelectedItem = "3.0"

        self.arpFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.rwyFeatureArray = []
        self.thrPoint3d = None
        self.thrEndPoint3d = None
        self.initAerodromeAndRwyCmb()
        self.resultLayerList = []

        self.catType = catType
        self.changedCriticalObstacleValue = None
    def initAerodromeAndRwyCmb(self):

        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.arpFeatureArray = self.aerodromeAndRwyCmbFill(self.currentLayer, self.ui.cmbAerodrome, None, self.ui.cmbRwyDir)
            self.calcRwyBearing()
    def calcRwyBearing(self):
        try:
            self.ui.txtTrack.Value = round(Unit.ConvertRadToDeg(MathHelper.getBearing(self.ui.pnlThr.Point3d, self.ui.pnlRwyEnd.Point3d)), 4)
        except:
            pass

    def aerodromeAndRwyCmbFill(self, layer, aerodromeCmbObj, aerodromePositionPanelObj, rwyDirCmbObj = None):
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')
        arpList = []
        arpFeatureList = []
        if idx >= 0:
            featIter = layer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idx].toString()
                attrValue = QString(attrValue)
                attrValue = attrValue.replace(" ", "")
                attrValue = attrValue.toUpper()
                if attrValue == "AERODROMEREFERENCEPOINT":
                    arpList.append(attrValue)
                    arpFeatureList.append(feat)
            if len(arpList) != 0:

                i = -1
                attrValueList = []
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    items = attrValueList
                    if len(items) != 0:
                        existFlag = False
                        for item in items:
                            if item == attrValue:
                                existFlag = True
                        if existFlag:
                            continue
                    attrValueList.append(attrValue)
                attrValueList.sort()
                aerodromeCmbObj.Items = attrValueList
                aerodromeCmbObj.SelectedIndex = 0

                # if idxAttributes
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    if attrValue != aerodromeCmbObj.SelectedItem:
                        continue
                    attrValue = feat.attributes()[idxLat].toDouble()
                    lat = attrValue[0]

                    attrValue = feat.attributes()[idxLong].toDouble()
                    long = attrValue[0]

                    attrValue = feat.attributes()[idxAltitude].toDouble()
                    alt = attrValue[0]

                    # aerodromePositionPanelObj.Point3d = Point3D(long, lat, alt)
                    self.connect(aerodromeCmbObj, SIGNAL("Event_0"), self.aerodromeCmbObj_Event_0)
                    break
            if rwyDirCmbObj != None:
                idxAttr = layer.fieldNameIndex('Attributes')
                if idxAttr >= 0:
                    rwyFeatList = []
                    featIter = layer.getFeatures()
                    rwyDirCmbObjItems = []
                    for feat in featIter:
                        attrValue = feat.attributes()[idxAttr].toString()
                        if attrValue == aerodromeCmbObj.SelectedItem:
                            attrValue = feat.attributes()[idxName].toString()
                            s = attrValue.replace(" ", "")
                            compStr = s.left(6).toUpper()
                            if compStr == "THRRWY":
                                valStr = s.right(s.length() - 6)
                                rwyDirCmbObjItems.append(aerodromeCmbObj.SelectedItem + " RWY " + valStr)
                                rwyFeatList.append(feat)
                    rwyDirCmbObjItems.sort()
                    rwyDirCmbObj.Items = rwyDirCmbObjItems
                    self.connect(rwyDirCmbObj, SIGNAL("Event_0"), self.rwyDirCmbObj_Event_0)
                    self.rwyFeatureArray = rwyFeatList
                    self.rwyDirCmbObj_Event_0()

                    self.aerodromeCmbObj_Event_0()
                    self.calcRwyBearing()
        return arpFeatureList
    def rwyDirCmbObj_Event_0(self):
        if len(self.rwyFeatureArray) == 0:
            return
        idxName = self.currentLayer.fieldNameIndex('Name')
        idxLat = self.currentLayer.fieldNameIndex('Latitude')
        idxLong = self.currentLayer.fieldNameIndex('Longitude')
        idxAltitude = self.currentLayer.fieldNameIndex('Altitude')
        idxAttr = self.currentLayer.fieldNameIndex('Attributes')
        for feat in self.rwyFeatureArray:
            attrValue = feat.attributes()[idxName].toString()
            attrValueStr = QString(attrValue)
            attrValueStr = attrValueStr.replace(" ", "").right(attrValueStr.length() - 3)
            itemStr = self.ui.cmbRwyDir.SelectedItem
            itemStr = QString(itemStr)
            itemStr = itemStr.replace(" ", "").right(itemStr.length() - 4)
            if attrValueStr != itemStr:
                continue
            latAttrValue = feat.attributes()[idxLat].toDouble()
            lat = latAttrValue[0]

            longAttrValue = feat.attributes()[idxLong].toDouble()
            long = longAttrValue[0]

            altAttrValue = feat.attributes()[idxAltitude].toDouble()
            alt = altAttrValue[0]

            self.thrPoint3d = Point3D(long, lat, alt)
            self.ui.pnlThr.Point3d = Point3D(long, lat, alt)

            valStr = None
            if attrValue.right(1).toUpper() =="L" or attrValue.right(1).toUpper() =="R":
                s = attrValue.left(attrValue.length() - 1)
                valStr = s.right(2)
            else:
                valStr = attrValue.right(2)
            val = int(valStr)
            val += 18
            if val > 36:
                val -= 36
            newValStr = None
            if len(str(val)) == 1:
                newValStr = "0" + str(val)
            else:
                newValStr = str(val)
            otherAttrValue = attrValue.replace(valStr, newValStr)
            ss = otherAttrValue.right(1)
            if ss.toUpper() == "L":
                otherAttrValue = otherAttrValue.left(otherAttrValue.length() - 1) + "R"
            elif ss.toUpper() == "R":
                otherAttrValue = otherAttrValue.left(otherAttrValue.length() - 1) + "L"
            for feat in self.rwyFeatureArray:
                attrValue = feat.attributes()[idxName].toString()
                if attrValue != otherAttrValue:
                    continue
                latAttrValue = feat.attributes()[idxLat].toDouble()
                lat = latAttrValue[0]

                longAttrValue = feat.attributes()[idxLong].toDouble()
                long = longAttrValue[0]

                altAttrValue = feat.attributes()[idxAltitude].toDouble()
                alt = altAttrValue[0]

                self.thrEndPoint3d = Point3D(long, lat, alt)
                self.ui.pnlRwyEnd.Point3d = Point3D(long, lat, alt)
                break
            break
        self.calcRwyBearing()
    def aerodromeCmbObj_Event_0(self):
        if len(self.arpFeatureArray) == 0:
            return
        self.ui.pnlThr.Point3d = None
        self.thrPoint3d = None
        self.thrEndPoint3d = None
        idxName = self.currentLayer.fieldNameIndex('Name')
        idxLat = self.currentLayer.fieldNameIndex('Latitude')
        idxLong = self.currentLayer.fieldNameIndex('Longitude')
        idxAltitude = self.currentLayer.fieldNameIndex('Altitude')
        self.rwyFeatureArray = []
        # if idxAttributes
        for feat in self.arpFeatureArray:
            attrValue = feat.attributes()[idxName].toString()
            if attrValue != self.ui.cmbAerodrome.SelectedItem:
                continue
            attrValue = feat.attributes()[idxLat].toDouble()
            lat = attrValue[0]

            attrValue = feat.attributes()[idxLong].toDouble()
            long = attrValue[0]

            attrValue = feat.attributes()[idxAltitude].toDouble()
            alt = attrValue[0]

            # self.parametersPanel.pnlNavAid.Point3d = Point3D(long, lat, alt)
            break
        idxAttr = self.currentLayer.fieldNameIndex('Attributes')
        if idxAttr >= 0:
            self.ui.cmbRwyDir.Clear()
            rwyFeatList = []
            featIter = self.currentLayer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idxAttr].toString()
                if attrValue == self.ui.cmbAerodrome.SelectedItem:
                    attrValue = feat.attributes()[idxName].toString()
                    s = attrValue.replace(" ", "")
                    compStr = s.left(6).toUpper()
                    if compStr == "THRRWY":
                        valStr = s.right(s.length() - 6)
                        self.ui.cmbRwyDir.Add(self.ui.cmbAerodrome.SelectedItem + " RWY " + valStr)
                        rwyFeatList.append(feat)
                        self.rwyFeatureArray = rwyFeatList
            self.rwyDirCmbObj_Event_0()
    def tblObstacles_pressed(self, modelIndex):
        self.selectedObstacleMoselIndex = modelIndex
    def tableViewObstacleMouseTeleaseEvent_rightButton(self, e):
        if self.obstaclesModel == None:
            return
        featID = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexObjectId)).toString()
        layerID = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexLayerId)).toString()
        name = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexName)).toString()
        xValue = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexX)).toString()
        yValue = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexY)).toString()
        altitudeMValue = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexAltM)).toString()
        surfaceName = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexSurface)).toString()
        ocaMValue = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexOcaM)).toString()
        # ocaMValue = self.obstaclesModel.data(self.obstaclesModel.index(self.selectedObstacleMoselIndex.row(), self.obstaclesModel.IndexOcaM)).toString()
        obstacle = Obstacle(name, Point3D(float(xValue), float(yValue), float(altitudeMValue)), layerID, featID, None, 0.0, self.obstaclesModel.MocMultiplier, 0.0)
        self.changedCriticalObstacleValue = {"Obstacle": obstacle,
                                             "SurfaceName": surfaceName,
                                             "OcaM": float(ocaMValue) if ocaMValue != "" else None}


        menu = QMenu()
        actionSetCriticalObst = QgisHelper.createAction(menu, "Set Most Critical Obstacles", self.menuSetCriticalObstClick)
        menu.addAction( actionSetCriticalObst )
        menu.exec_( self.ui.tblObstacles.mapToGlobal(e.pos() ))
    def menuSetCriticalObstClick(self):
        OasObstacles.resultCriticalObst.Obstacle = self.changedCriticalObstacleValue["Obstacle"]
        OasObstacles.resultCriticalObst.Surface = self.changedCriticalObstacleValue["SurfaceName"]
        OasObstacles.resultCriticalObst.Assigned = True
        OasObstacles.resultCriticalObst.eqAltitude = None
        ocaMValue = self.changedCriticalObstacleValue["OcaM"]

        OasObstacles.resultOCA = Altitude(float(ocaMValue) if ocaMValue != "" else None)
        if OasObstacles.resultOCA == None:
            OasObstacles.resultOCH = None
        else:
            OasObstacles.resultOCH = Altitude(OasObstacles.resultOCA.Metres - self.ui.pnlThr.Altitude().Metres)

        point3d = self.ui.pnlThr.Point3d
        num = Unit.ConvertDegToRad(float(self.ui.txtTrack.Value))
        num1 = self.method_40()
        zC = OasObstacles.constants.ZC / OasObstacles.constants.ZA
        point3d1 = MathHelper.distanceBearingPoint(point3d, num, zC)
        metres2 = OasObstacles.resultCriticalObst.method_2(point3d).Metres
        z = metres2 - point3d.z()
        num3 = math.tan(Unit.ConvertDegToRad(num1))
        num4 = z / num3
        OasObstacles.resultSocPosition = MathHelper.distanceBearingPoint(point3d1, num + 3.14159265358979, num4).smethod_167(0)
        if (num4 > zC):
            OasObstacles.resultSocText = Messages.X_BEFORE_THRESHOLD % (num4 - zC)
        else:
            OasObstacles.resultSocText = Messages.X_PAST_THRESHOLD % (zC - num4)
        self.setCriticalObstacle()
    def cmbSelectionModeChanged(self):
        pass
        # if self.ui.cmbSelectionMode.currentIndex() == 1:
        #     msgBox = QMessageBox()
        #     msgBox.setText("It is need to select obstacles.")
        #     msgBox.setInformativeText("Do you want to select obstacles now?")
        #     msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        #     msgBox.setDefaultButton(QMessageBox.Ok)
        #     ret = msgBox.exec_()
        #     if ret == QMessageBox.Ok:
        #         define._canvas.selectionChanged.connect(self.obstacleSelected)
        #         self.hide()
                
    def obstacleSelected(self):
        obstacleLayers = QgisHelper.getSurfaceLayers(SurfaceTypes.Obstacles)
        sum = 0
        for layer in obstacleLayers:
            selCount = layer.selectedFeatureCount()
            sum += selCount
        if sum > 0:
            define._canvas.selectionChanged.disconnect(self.obstacleSelected)
            self.show()
        else:
            reselect = QgisHelper.showMessageBoxYesNo("There is no selected obstacles.", "Do you want to select again?")
            if not reselect:
                define._canvas.selectionChanged.disconnect(self.obstacleSelected)
                self.show()
        
    def initResultPanel(self):
        if self.obstaclesModel != None  and self.ui.btnEvaluate.isEnabled():
            self.obstaclesModel.clear()
            
            lstTextControls = self.ui.groupBox.findChildren(QLineEdit)
            for ctrl in lstTextControls:
                if ctrl != self.ui.txtOCA and ctrl != self.ui.txtOCA_2:
                    ctrl.setText("")
        self.ui.btnEvaluate.setEnabled(False)
        self.btnExportResult.setEnabled(False)
    def criticalLocate(self):
        point = None
        try:
            point = QgsPoint(float(self.ui.txtX.text()), float(self.ui.txtY.text()))
        except:
            return
        if define._units == QGis.Meters:
            extent = QgsRectangle(point.x() - 350, point.y() - 350, point.x() + 350, point.y() + 350)
        else:
            extent = QgsRectangle(point.x() - 0.005, point.y() - 0.005, point.x() + 0.005, point.y() + 0.005)

        if extent is None:
            return

        QgisHelper.zoomExtent(point, extent, 2)

    def getExtentForLocate(self, point):
        extent = None
#         surfaceType = self.source.item(sourceRow, self.IndexSurface).text()
        surfaceLayers = QgisHelper.getSurfaceLayers(self.surfaceType)
        sfLayer = surfaceLayers[0]
        featIter = sfLayer.getFeatures()
        for feat in featIter:
            geom = feat.geometry()
            if geom.contains(point):
                extent = geom. boundingBox()
                break
        return extent
    def method_37(self):
        return self.ui.cmbOasCategory.SelectedItem
    
    def method_38(self):
        return self.ui.cmbMACG.SelectedIndex
    
    def method_39(self):
        if self.ui.cmbMACG.SelectedIndex == 0:
            return 5
        elif self.ui.cmbMACG.SelectedIndex == 1:
            return 4
        elif self.ui.cmbMACG.SelectedIndex == 2:
            return 3
        elif self.ui.cmbMACG.SelectedIndex == 3:
            return 2.5
        elif self.ui.cmbMACG.SelectedIndex == 4:
            return 2
        else:
            raise UserWarning, Messages.ERR_INVALID_MISSED_APPROACH_CLIMB_GRADIENT_TYPE


    def method_40(self):
        num = 2.5
        for i in range(self.ui.cmbGPA.SelectedIndex):
            num = num + 0.1
        return round(num, 1)

    def method_41(self):


            oasCategory = self.method_37()
            missedApproachClimbGradient = self.method_38()
            num = self.method_40()
            try:
                metres = self.ui.txtDLT.Value.Metres
            except:
                metres = 0.0
            try:
                metres1 = float(self.ui.txtRDH.Value)
            except:
                metres1 = 0.0
            try:
                num1 = float(self.ui.txtWSS.Value)
            except:
                num1 = 0.0
            try:
                value = self.ui.txtWH.Value
            except:
                value = 0.0
            OasObstacles.constants.method_1(oasCategory, missedApproachClimbGradient, num, metres, metres1, num1, value)

    def construct(self):
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        try:
            self.method_41()
            point3d = self.ui.pnlThr.Point3d
            thrAlt = self.ui.pnlThr.Altitude().Metres
            try:
                num = Unit.ConvertDegToRad(float(self.ui.txtTrack.Value))
            except:
                raise UserWarning, "In-bound track is invalid!"
            
            try:
                metres = float(self.ui.txtContourHeight.Value)
            except:
                if self.ui.txtContourHeight.Enabled:
                    raise UserWarning, "OAS Contour Height is invalid!"
                else:
                    metres = None
            oasCategory = self.method_37()
            self.method_40()
            self.method_39()
            metres1 = 0
            if ((oasCategory == OasCategory.ILS1 or oasCategory == OasCategory.SBAS_APV1 or oasCategory == OasCategory.SBAS_APV2 or oasCategory == OasCategory.SBAS_CAT1) ):
                try:
                    ocahMeter = self.ui.txtOCAH.Value.Metres
                except:
                    raise UserWarning, "Intermediate Segnment Minimum Height is invalide!"
                if self.ui.txtOCAH.cmbType.currentIndex() != 0:
                    altitude = ocahMeter
                else:
                    altitude = ocahMeter - thrAlt
                #altitude = self.pnlOCAH.method_3(self.pnlThr.Altitude)
                #metres1 = altitude.Metres - self.pnlMOC.Value.Metres
                try:
                    moc = self.ui.txtMOC.Value.Metres
                except:
                    raise UserWarning, "Intermediate Segment MOC is invalid!"
                    
                metres1 = altitude - moc
                
            if ((oasCategory == OasCategory.ILS1 or oasCategory == OasCategory.ILS2 or oasCategory == OasCategory.ILS2AP) and metres1 < metres):
                metres1 = metres
            
            oasSurface = OasSurfaces(oasCategory, point3d, num, metres, metres1)
            constructionType = self.ui.cmbConstructionType.SelectedItem
            
            mapUnits = define._canvas.mapUnits()
            renderList = []
            
            if constructionType != ConstructionType.Construct2D:
                layerName = self.catType + "_" + self.ui.cmbOasCategory.SelectedItem
                layerName = layerName.replace("|", "_")
                layerName = layerName.replace(" ", "")
                resultLayer = AcadHelper.createVectorLayer(layerName, QGis.Polygon)
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.Ofz[0], oasSurface.Ofz[1], oasSurface.Ofz[2], oasSurface.Ofz[3], oasSurface.Ofz[4], oasSurface.Ofz[5]], True, {"Surface":OasSurface.OFZ})
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.W[0], oasSurface.W[1], oasSurface.W[2], oasSurface.W[3], oasSurface.W[0]], True, {"Surface":OasSurface.W})
                if len(oasSurface.WS) == 4:
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.WS[0], oasSurface.WS[1], oasSurface.WS[2], oasSurface.WS[3], oasSurface.WS[0]], True, {"Surface":OasSurface.WS})
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.Z[0], oasSurface.Z[1], oasSurface.Z[2], oasSurface.Z[3], oasSurface.Z[0]], True, {"Surface":OasSurface.Z})
                if len(oasSurface.X1) == 4:
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.X1[0], oasSurface.X1[1], oasSurface.X1[2], oasSurface.X1[3], oasSurface.X1[0]], True, {"Surface":OasSurface.X1})
                elif (oasCategory != OasCategory.ILS2AP):
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.X1[0], oasSurface.X1[1], oasSurface.X1[2], oasSurface.X1[3], oasSurface.X1[4]], True, {"Surface":OasSurface.X1})
                else:
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.X1[0], oasSurface.X1[1], oasSurface.X1[2], oasSurface.X1[3], oasSurface.X1[4]], True, {"Surface":OasSurface.X1})
                if len(oasSurface.X2) == 4:
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.X2[0], oasSurface.X2[1], oasSurface.X2[2], oasSurface.X2[3], oasSurface.X2[0]], True, {"Surface":OasSurface.X2})
                elif (oasCategory != OasCategory.ILS2AP):
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.X2[0], oasSurface.X2[1], oasSurface.X2[2], oasSurface.X2[3], oasSurface.X2[4]], True, {"Surface":OasSurface.X2})
                else:
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.X2[0], oasSurface.X2[1], oasSurface.X2[2], oasSurface.X2[3], oasSurface.X2[4]], True, {"Surface":OasSurface.X2})
                if len(oasSurface.Y1) != 4:
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.Y1[0], oasSurface.Y1[1], oasSurface.Y1[2], oasSurface.Y1[3], oasSurface.Y1[4]], True, {"Surface":OasSurface.Y1})
                else:
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.Y1[0], oasSurface.Y1[1], oasSurface.Y1[2], oasSurface.Y1[3], oasSurface.Y1[0]], True, {"Surface":OasSurface.Y1})
                if len(oasSurface.Y2) != 4:
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.Y2[0], oasSurface.Y2[1], oasSurface.Y2[2], oasSurface.Y2[3], oasSurface.Y2[4]], True, {"Surface":OasSurface.Y2})
                else:
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.Y2[0], oasSurface.Y2[1], oasSurface.Y2[2], oasSurface.Y2[3], oasSurface.Y2[0]], True, {"Surface":OasSurface.Y2})
            else:
                layerName = self.catType + "_" + self.ui.cmbOasCategory.SelectedItem
                layerName = layerName.replace("|", "")
                layerName = layerName.replace(" ", "")
                resultLayer = AcadHelper.createVectorLayer(layerName)
                lstSelectionArea = []
                lstSelectionArea.extend(oasSurface.SelectionArea)
                lstSelectionArea.append(oasSurface.SelectionArea[0])
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, lstSelectionArea, False, {"Surface":"SelectionArea"})
                lstOfz = []
                lstOfz.extend(oasSurface.Ofz)
                lstOfz.append(oasSurface.Ofz[0])
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, lstOfz, False, {"Surface":OasSurface.OFZ})
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.W[0], oasSurface.W[1]], False, {"Surface":OasSurface.W})
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.W[3], oasSurface.W[2]], False, {"Surface":OasSurface.W})
                if len(oasSurface.WS) == 4:
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.WS[0], oasSurface.WS[1]], False, {"Surface":OasSurface.WS})
                    AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.WS[3], oasSurface.WS[2]], False, {"Surface":OasSurface.WS})
                    if (oasCategory != OasCategory.ILS2AP):
                        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.WS[0], oasSurface.WS[3]])#, False, {"Surface":OasSurface.WS})
                    else:
                        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.WS[1], oasSurface.WS[2]], False, {"Surface":OasSurface.WS})
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.Z[0], oasSurface.Z[1]], False, {"Surface":OasSurface.Z})
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.Z[3], oasSurface.Z[2]], False, {"Surface":OasSurface.Z})
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.Y1[0], oasSurface.Ofz[1]], False, {"Surface":OasSurface.Y1})
                AcadHelper.setGeometryAndAttributesInLayer(resultLayer, [oasSurface.Y2[0], oasSurface.Ofz[4]], False, {"Surface":OasSurface.Y2})

                
            symbolOfz = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            renderCatOfz = QgsRendererCategoryV2(OasSurface.OFZ, symbolOfz,OasSurface.OFZ)
            renderList.append(renderCatOfz)
            
            symbolW = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            renderCatW = QgsRendererCategoryV2(OasSurface.W, symbolW,OasSurface.W)
            renderList.append(renderCatW)

            symbolWS = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            renderCatWS = QgsRendererCategoryV2(OasSurface.WS, symbolWS,OasSurface.WS)
            renderList.append(renderCatWS)

            symbolZ = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            renderCatZ = QgsRendererCategoryV2(OasSurface.Z, symbolZ,OasSurface.Z)
            renderList.append(renderCatZ)

            symbolX1 = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            renderCatX1 = QgsRendererCategoryV2(OasSurface.X1, symbolX1, OasSurface.X1)
            renderList.append(renderCatX1)

            symbolX2 = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            renderCatX2 = QgsRendererCategoryV2(OasSurface.X2, symbolX2,OasSurface.X2)
            renderList.append(renderCatX2)

            symbolY1 = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            renderCatY1 = QgsRendererCategoryV2(OasSurface.Y1, symbolY1, OasSurface.Y1)
            renderList.append(renderCatY1)

            symbolY2 = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            renderCatY2 = QgsRendererCategoryV2(OasSurface.Y2, symbolY2, OasSurface.Y2)
            renderList.append(renderCatY2)

            symbol = QgsSymbolV2.defaultSymbol(resultLayer.geometryType())
            renderCatY2 = QgsRendererCategoryV2("SelectionArea", symbol, "SelectionArea")
            renderList.append(renderCatY2)

            resultLayer.commitChanges()
            myCategoryRender = QgsCategorizedSymbolRendererV2("surface", renderList)
            resultLayer.setRendererV2(myCategoryRender)

            QgisHelper.appendToCanvas(define._canvas, [resultLayer], self.surfaceType )
            QgisHelper.zoomToLayers([resultLayer])
            self.resultLayerList = [resultLayer]
            self.ui.btnEvaluate.setEnabled(True)
            self.manualEvent(self.ui.cmbSelectionMode.SelectedIndex)
            self.btnExportResult.setEnabled(True)
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
    def outputResultMethod(self):
        self.manualPolygon = self.toolSelectByPolygon.polygonGeom
    def manualEvent(self, index):
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        self.manualPolygon = None
        if index != 0:
            self.toolSelectByPolygon = RubberBandPolygon(define._canvas)
            define._canvas.setMapTool(self.toolSelectByPolygon)
            self.connect(self.toolSelectByPolygon, SIGNAL("outputResult"), self.outputResultMethod)
        else:
            self.mapToolPan = QgsMapToolPan(define._canvas)
            define._canvas.setMapTool(self.mapToolPan )

    def evaluate(self):
        try:
            self.ui.txtOCAResults.setText("")
            self.ui.txtOCHResults.setText("")

            self.ui.txtResultSocText.setText("")
            self.ui.txtX.setText("")
            self.ui.txtY.setText("")
            self.ui.txtAltitude.setText("")
            self.ui.txtAltitudeM.setText("")
            self.ui.txtSurface.setText("")
            self.ui.txtID.setText("")

            OasObstacles.obstaclesChecked = 0
            OasObstacles.constants = OasConstants()
            OasObstacles.resultOCH = Altitude(0)
            OasObstacles.resultOCA = Altitude(0)
            OasObstacles.resultSocText = ""
            OasObstacles.resultSocPosition = Point3D()
            OasObstacles.resultCriticalObst = OasCriticalObstacle()

            self.method_41()
            try:
                thrAlt = self.ui.pnlThr.Altitude().Metres
            except:
                raise UserWarning, "Threshold altitude is invalid!"
            
            point3d = self.ui.pnlThr.Point3d

            try:
                num = Unit.ConvertDegToRad(float(self.ui.txtTrack.Value))
            except:
                raise UserWarning, "In-bound track is invalid!"

            try:
                metres = float(self.ui.txtContourHeight.Value)
            except:
                if self.ui.txtContourHeight.Enabled:
                    raise UserWarning, "OAS Contour Height is invalid!"
                else:
                    metres = None

            oasCategory = self.method_37()
            num1 = self.method_40()
            num2 = self.method_39()
            metres1 = 0
            if ((oasCategory == OasCategory.ILS1 or oasCategory == OasCategory.SBAS_APV1 or oasCategory == OasCategory.SBAS_APV2 or oasCategory == OasCategory.SBAS_CAT1)):
                try:
                    ocahMeter = self.ui.txtOCAH.Value.Metres
                except:
                    raise UserWarning, "Intermediate Segnment Minimum Height is invalide!"
                if self.ui.txtOCAH.cmbType.currentIndex() != 0:
                    altitude = ocahMeter
                else:
                    altitude = ocahMeter - thrAlt
                #altitude = self.pnlOCAH.method_3(self.pnlThr.Altitude)
                #metres1 = altitude.Metres - self.pnlMOC.Value.Metres
                try:
                    moc = self.ui.txtMOC.Value.Metres
                except:
                    raise UserWarning, "Intermediate Segment MOC is invalid!"
                    
                metres1 = altitude - moc
                
            if ((oasCategory == OasCategory.ILS1 or oasCategory == OasCategory.ILS2 or oasCategory == OasCategory.ILS2AP) and metres1 < metres):
                metres1 = metres
            
            try:
                value = Altitude(float(self.ui.txtHL.Value))
            except:
                raise UserWarning, "Height Loss is invalid!"
            oasSurface = OasSurfaces(oasCategory, point3d, num, metres, metres1)

            oasMaEvaluationMethod = OasMaEvaluationMethod.Standard
            if (self.ui.cmbMAMethod.SelectedIndex == 1):
                oasMaEvaluationMethod = OasMaEvaluationMethod.Alternative

            self.obstaclesModel.initModel([oasSurface], oasCategory, point3d, num, num2, num1, oasMaEvaluationMethod, value)
            ObstacleTable.SelectionMode = self.ui.cmbSelectionMode.SelectedItem
            self.obstaclesModel.manualPolygon = self.manualPolygon
            gnssMapLayers = QgisHelper.getSurfaceLayers(self.surfaceType)
            if not self.obstaclesModel.loadObstacles(gnssMapLayers):
                raise UserWarning, "There are not exist obstacles in surface"
            else:
                zC = OasObstacles.constants.ZC / OasObstacles.constants.ZA
                point3d1 = MathHelper.distanceBearingPoint(point3d, num, zC)
                metres2 = OasObstacles.resultCriticalObst.method_2(point3d).Metres
                z = metres2 - point3d.z()
                num3 = math.tan(Unit.ConvertDegToRad(num1))
                num4 = z / num3
                OasObstacles.resultSocPosition = MathHelper.distanceBearingPoint(point3d1, num + 3.14159265358979, num4).smethod_167(0)
                if (num4 > zC):
                    OasObstacles.resultSocText = Messages.X_BEFORE_THRESHOLD % (num4 - zC)
                else:
                    OasObstacles.resultSocText = Messages.X_PAST_THRESHOLD % (zC - num4)
                OasObstacles.resultOCA = Altitude(metres2 + value.Metres)
                value1 = value
                OasObstacles.resultOCH = Altitude(metres2 + value1.Metres - point3d.z())
                self.setCriticalObstacle()
                self.ui.tblObstacles.setModel(self.obstaclesModel)
                self.obstaclesModel.setHiddenColumns(self.ui.tblObstacles)
                if self.ui.cmbSurface.currentIndex() == 0:
                    self.obstaclesModel.setFilterFixedString("")
                else:
                    self.obstaclesModel.setFilterFixedString(str(self.ui.cmbSurface.currentText()))
                # self.ui.btn.setDisabled(False)
                self.ui.tabControls.setCurrentIndex(1)
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message + "\n")
       
    def markSocClicked(self):
        if not self.method_27(True, False, False, False):
            return
        point3d = MathHelper.distanceBearingPoint(OasObstacles.resultSocPosition, Unit.ConvertDegToRad(450) - 0, 100)
        point3d1 = MathHelper.distanceBearingPoint(OasObstacles.resultSocPosition, Unit.ConvertDegToRad(450) - 1.5707963267949, 100)
        point3d2 = MathHelper.distanceBearingPoint(OasObstacles.resultSocPosition, Unit.ConvertDegToRad(450) - 3.14159265358979, 100)
        point3d3 = MathHelper.distanceBearingPoint(OasObstacles.resultSocPosition, Unit.ConvertDegToRad(450) - 4.71238898038469, 100)
        
        if self.socRubber == None:
            self.socRubber = QgsRubberBand(define._canvas, QGis.Line)
            self.socRubber.setColor(Qt.yellow)
        else:
            self.socRubber.reset(QGis.Line)
        self.socRubber.addGeometry(QgsGeometry.fromPolyline([point3d, point3d2]), None)
        self.socRubber.addGeometry(QgsGeometry.fromPolyline([point3d1, point3d3]), None)
        circle = MathHelper.constructCircle(OasObstacles.resultSocPosition, 100, 16)
        self.socRubber.addGeometry(QgsGeometry.fromPolyline(circle), None)
        self.socRubber.show()
        
        self.socAnnotation.setMapPosition(OasObstacles.resultSocPosition)
        self.socAnnotation.show()
        
    def setCriticalObstacle(self):
        resultUnit = self.ui.cmbUnits.currentIndex()
        if resultUnit == AltitudeUnits.M:
            self.ui.txtOCAResults.setText(str(round(OasObstacles.resultOCA.Metres, 2)) + " m")
            self.ui.txtOCHResults.setText(str(round(OasObstacles.resultOCH.Metres, 2)) + " m")
        else:
            self.ui.txtOCAResults.setText(str(round(Unit.ConvertMeterToFeet(OasObstacles.resultOCA.Metres), 2)) + " ft")
            self.ui.txtOCHResults.setText(str(round(Unit.ConvertMeterToFeet(OasObstacles.resultOCH.Metres), 2)) + " ft")
        
        if not OasObstacles.resultCriticalObst.Assigned:
            return 
        self.ui.txtResultSocText.setText(OasObstacles.resultSocText)
        self.ui.txtX.setText(str(OasObstacles.resultCriticalObst.Position.get_X()))
        self.ui.txtY.setText(str(OasObstacles.resultCriticalObst.Position.get_Y()))
        self.ui.txtAltitude.setText(str(OasObstacles.resultCriticalObst.Position.get_Z()))
        self.ui.txtAltitudeM.setText(str(Unit.ConvertMeterToFeet(OasObstacles.resultCriticalObst.Position.get_Z())))
        self.ui.txtSurface.setText(OasObstacles.resultCriticalObst.Surface)
        self.ui.txtID.setText(OasObstacles.resultCriticalObst.Obstacle.name)
        

    def surfaceChanged(self):
        if self.ui.cmbSurface.currentIndex() == 0:
            self.obstaclesModel.setFilterFixedString("")
        else:
            self.obstaclesModel.setFilterFixedString(self.ui.cmbSurface.currentText())
        
    def oasCategoryChange(self):
        self.method_31(self.ui.cmbGPA.SelectedIndex)
        self.method_32()
        self.method_34()
        self.method_36()
        return
    def acCategoryChange(self):
        self.method_33()
        self.method_34()
        return
    def GPAChange(self):
        self.method_34()
        
    def OasConstantsShow(self):
            
        # if (self.method_27(False, False, True, True)):
        self.method_41()
        dlg = OasConstantsDlg(self, OasObstacles.constants)
        result = dlg.exec_()
        if result == QDialog.Accepted:
            OasObstacles.constants.method_0(dlg.WA,dlg.WC,dlg.WSA,dlg.WSC,dlg.XA,dlg.XB,dlg.XC,dlg.YA,dlg.YB,dlg.YC,dlg.ZA,dlg.ZC)


    def method_27(self, bool_0, bool_1, bool_2, bool_3):
        try:
            if (bool_0):
                if self.ui.cmbConstructionType.SelectedItem == "":
                    return False
            if (bool_1):
                if not self.ui.pnlThr.IsValid():
                    return False           
            if (bool_2):
                # if self.ui.txtTrack.text() == "":
                #     return False
                oasCategory = self.method_37()
                if (oasCategory == OasCategory.SBAS_APV1 or oasCategory == OasCategory.SBAS_APV2 or oasCategory == OasCategory.SBAS_CAT1 or oasCategory == OasCategory.ILS1):
                    if (self.ui.txtOCAH.Value.IsNaN()):
                        if self.ui.txtMOC.Value.IsNaN():
                            return False
            if (bool_3):
                if self.ui.cmbOasCategory.SelectedIndex < 0:
                    return False
                if self.ui.cmbGPA.SelectedIndex < 0:
                    return False
                if self.ui.cmbMACG.SelectedIndex < 0:
                    return False
                # if self.ui.txtRDH.Value == "" :
                #     return False
                if self.ui.txtDLT.Value.Metres < 2000 or self.ui.txtDLT.Value.Metres > 4500:
                    raise UserWarning, Validations.VALUE_CANNOT_BE_SMALLER_THAN_OR_GREATER_THAN%(2000, 4500)
                    return False
                if self.ui.txtContourHeight.Enabled:
                    return False
            return True
        except UserWarning as e:
            QMessageBox.warning(self, "warning", e.message)

        
    def method_31(self, int_0):
        if (int_0 < 0):
            int_0 = self.ui.cmbGPA.SelectedIndex
        self.ui.cmbGPA.Clear()
#         try:
        oasCategory = self.method_37()
        if (oasCategory != OasCategory.ILS1):
            if (oasCategory != OasCategory.ILS2):
                if (oasCategory == OasCategory.ILS2AP):
#                     self.ui.txtContourHeight.setText(str(Altitude(150).Metres))
                    i = 25
                    while i < 31:
                        num1 = float(i) / 10.0
                        self.ui.cmbGPA.Add(str(num1))
                        i += 1
                        if (int_0 > self.ui.cmbGPA.Count):
                            int_0 = self.ui.cmbGPA.Count - 1
                        self.ui.cmbGPA.SelectedIndex = int_0
                    return
                i = 25
                while i <64:
                    num = float(i) / 10.0
                    self.ui.cmbGPA.Add(str(num))
                    i += 1
                if (int_0 > self.ui.cmbGPA.Count):
                    int_0 = self.ui.cmbGPA.Count - 1
                self.ui.cmbGPA.SelectedIndex = int_0
                return
            else:
                i = 25
                while i < 31:
                    num1 = float(i) / 10.0
                    self.ui.cmbGPA.Add(str(num1))
                    i += 1
                   
            
        else:
            i = 25
            while i < 100:
                num1 = float(i) / 10.0
                self.ui.cmbGPA.Add(str(num1))
                i += 1
        if (int_0 > self.ui.cmbGPA.Count):
            int_0 = self.ui.cmbGPA.Count - 1
        self.ui.cmbGPA.SelectedIndex = int_0
#         except:
#             pass
    def method_32(self):
        try:
            oasCategory = self.method_37()
            if (oasCategory != OasCategory.ILS1):
                if (oasCategory != OasCategory.ILS2):
                    if (oasCategory == OasCategory.ILS2AP):
                        self.ui.txtContourHeight.Value = Altitude(150).Metres
                        return
                    self.ui.txtContourHeight.Value = 0.0
                    return
                self.ui.txtContourHeight.Value = Altitude(150).Metres
            else:
                self.ui.txtContourHeight.Value = Altitude(300).Metres
        except:
            pass
        
    def method_33(self):
        for case in switch (self.ui.cmbAcCategory.SelectedIndex):
            if case(0) or case(1):
                self.ui.txtWSS.Value = Distance(30).Metres
                self.ui.txtWH.Value = Distance(6).Metres
                return
            elif case(2) or case(3):
                self.ui.txtWSS.Value = Distance(32.5).Metres
                self.ui.txtWH.Value = Distance(7).Metres
                return
            elif case(4):
                self.ui.txtWSS.Value = Distance(40).Metres
                self.ui.txtWH.Value = Distance(8).Metres
                return
            else:
                return
        # oasCategoty = self.method_37()
        # if oasCategoty == OasCategory.ILS1 or oasCategoty == OasCategory.ILS2:
        #     self.ui.txtWSS.Value = Distance(30).Metres
        #     self.ui.txtWH.Value = Distance(6).Metres
        #     return
        # elif oasCategoty == OasCategory.ILS2AP or oasCategoty == OasCategory.SBAS_APV1:
        #     self.ui.txtWSS.Value = Distance(32.5).Metres
        #     self.ui.txtWH.Value = Distance(7).Metres
        #     return
        # elif oasCategoty == OasCategory.SBAS_APV2:
        #     self.ui.txtWSS.Value = Distance(40).Metres
        #     self.ui.txtWH.Value = Distance(8).Metres
        #     return
        # else:
        #     return
       
    def method_34(self):
#         try:
        oasCategory = self.method_37()
        if (self.ui.cmbGPA.SelectedIndex >= 0):
            num = self.method_40()
            try:
                metres = self.ui.pnlThr.Altitude().Metres
            except ValueError:
                metres = 0.0
            num1 = 0
            num2 = 0
            if self.ui.cmbAcCategory.SelectedIndex == 0:
                if (oasCategory != OasCategory.ILS1 and oasCategory != OasCategory.SBAS_APV1 and oasCategory != OasCategory.SBAS_APV2):
                    if (oasCategory == OasCategory.SBAS_CAT1):
                        num1 = 40
                        num2 = 13
                    else:
                        num1 = 13
                        num2 = 13
                else:
                    num1 = 40                
                    num2 = 13
            if self.ui.cmbAcCategory.SelectedIndex == 1:
                if (oasCategory != OasCategory.ILS1 and oasCategory != OasCategory.SBAS_APV1 and oasCategory != OasCategory.SBAS_APV2):
                    if (oasCategory == OasCategory.SBAS_CAT1):
                        num1 = 43
                        num2 = 18
                    else:
                        num1 = 18
                        num2 = 18
                else:
                    num1 = 43
                    num2 = 18
            if self.ui.cmbAcCategory.SelectedIndex == 2:
                if (oasCategory != OasCategory.ILS1 and oasCategory != OasCategory.SBAS_APV1 and oasCategory != OasCategory.SBAS_APV2):
                    if (oasCategory == OasCategory.SBAS_CAT1):
                        num1 = 46
                        num2 = 22
                    else:
                        num1 = 22
                        num2 = 22
                else:
                    num1 = 46
                    num2 = 22
            if self.ui.cmbAcCategory.SelectedIndex == 3 or self.ui.cmbAcCategory.SelectedIndex == 4:
                if (oasCategory != OasCategory.ILS1 and oasCategory != OasCategory.SBAS_APV1 and oasCategory != OasCategory.SBAS_APV2):
                    if (oasCategory == OasCategory.SBAS_CAT1):
                        num1 = 49                        
                        num2 = 26
                    else:
                        num1 = 26
                        num2 = 26
                else:
                    num1 = 49
                    num2 = 26
            num3 = 0
            if (metres > 900):
                num3 = num3 + num2 * 0.02 * (float(metres) / 300)
            if (num > 3.2):
                num3 = num3 + num2 * 0.05 * ((num - 3.2) / 0.1)                    
            num3 = MathHelper.smethod_0(num3, 0)
            self.ui.txtHL.Value = Altitude(num1 + num3).Metres
#         except:
        
#             pass

    def method_36(self):
        try:
            if self.ui.txtOCAH.Value.IsValid():
                self.ui.txtMOC.Visible = True
            oasCategory = self.method_37()
            if (oasCategory != OasCategory.SBAS_APV1 and oasCategory != OasCategory.SBAS_APV2):
                if (oasCategory == OasCategory.SBAS_CAT1):
                    self.ui.txtDLT.Caption = "GARP to LTP Distance"
                    self.ui.txtContourHeight.Enabled = False
                    self.ui.cmbMAMethod.comboBox.removeItem(1)
                    self.ui.cmbMAMethod.Insert(1, "VPA'")
                    return
                else:                    
                    self.ui.txtDLT.Caption = "LOC to THR Distance"
                    self.ui.txtContourHeight.Enabled = True
                    self.ui.cmbMAMethod.comboBox.removeItem(1)
                    self.ui.cmbMAMethod.Insert(1, "GP'")
                    return
            else:
                self.ui.txtDLT.Caption = "GARP to LTP Distance"
                self.ui.txtContourHeight.Enabled = False
                self.ui.cmbMAMethod.comboBox.removeItem(1)
                self.ui.cmbMAMethod.Insert(1, "VPA'")
                return     
                  
        finally:
            pass



    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return        
        self.filterList = ["", OasSurface.OFZ, OasSurface.W, OasSurface.WS, OasSurface.X1, OasSurface.X2, OasSurface.Y1, OasSurface.Y2, OasSurface.Z]
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, "Obstacle Assessment Surfaces(" + self.catType + ")", self.ui.tblObstacles, self.filterList, parameterList, resultHideColumnNames)
        self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbSurface.currentIndex()])
#         FlightPlanBaseDlg.exportResult()
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Threshold Position", "group"))

        parameterList.append(("Lat", self.ui.pnlThr.txtLat.Value))
        parameterList.append(("Lon", self.ui.pnlThr.txtLong.Value))
        parameterList.append(("X", self.ui.pnlThr.txtPointX.text()))
        parameterList.append(("Y", self.ui.pnlThr.txtPointY.text()))
        parameterList.append(("Altitude", self.ui.pnlThr.txtAltitudeFt.text() + "ft"))
        parameterList.append(("", self.ui.pnlThr.txtAltitudeM.text() + "m"))


        parameterList.append(("Parameters", "group"))
        parameterList.append(("Selection Mode", self.ui.cmbSelectionMode.SelectedItem))
        parameterList.append(("In-bound Track", QString(str(self.ui.txtTrack.Value)) + unicode(" °", "utf-8")))
        parameterList.append(("Intermediate Segment Minimum(%s)"%self.ui.txtOCAH.cmbType.currentText(), str(self.ui.txtOCAH.Value.Feet) + " ft"))
        parameterList.append(("Intermediate Segment MOC", str(self.ui.txtMOC.Value.Metres) + " m"))
        parameterList.append(("", str(self.ui.txtMOC.Value.Feet) + " m"))
        parameterList.append(("Construction Type", self.ui.cmbConstructionType.SelectedItem))
        
        parameterList.append(("Additional Parameters / Constants", "group"))
        parameterList.append(("Category", self.ui.cmbOasCategory.SelectedItem))
        parameterList.append(("GPA", self.ui.cmbGPA.SelectedItem + unicode(" °", "utf-8")))
        parameterList.append(("MACG", self.ui.cmbMACG.SelectedItem+ " %"))
        parameterList.append(("RDH", str(self.ui.txtRDH.Value) + " m"))
        parameterList.append(("LOC Course Width", str(self.ui.txtCW.Value) + " m"))
        parameterList.append((self.ui.txtDLT.Caption, str(self.ui.txtDLT.Value.Metres) + " m"))
        parameterList.append(("OCA Contour Height AGL", str(self.ui.txtContourHeight.Value) + " m"))
        parameterList.append(("MA Obstacles Evaluation", self.ui.cmbMAMethod.SelectedItem))
                
        parameterList.append(("Aircraft", "group"))
        parameterList.append(("Category", self.ui.cmbAcCategory.SelectedItem))
        parameterList.append(("Height Loss", str(self.ui.txtHL.Value) + " m"))
        parameterList.append(("Wing Semi Span", str(self.ui.txtWSS.Value) + " m"))
        parameterList.append(("Wheel Height", str(self.ui.txtWH.Value) + " m"))
        
        parameterList.append(("Constants", "group"))
        parameterList.append(("WA", str(self.obstaclesModel.constants.WA)))
        parameterList.append(("WC", str(self.obstaclesModel.constants.WC)))
        parameterList.append(("WSA", str(self.obstaclesModel.constants.WSA)))
        parameterList.append(("WSC", str(self.obstaclesModel.constants.WSC)))
        parameterList.append(("XA", str(self.obstaclesModel.constants.XA)))
        parameterList.append(("XB", str(self.obstaclesModel.constants.XB)))
        parameterList.append(("XC", str(self.obstaclesModel.constants.XC)))
        parameterList.append(("YA", str(self.obstaclesModel.constants.YA)))
        parameterList.append(("YB", str(self.obstaclesModel.constants.YB)))
        parameterList.append(("YC", str(self.obstaclesModel.constants.YC)))
        parameterList.append(("ZA", str(self.obstaclesModel.constants.ZA)))
#         parameterList.append(("ZB", str(self.obstaclesModel.constants.ZB)))
        parameterList.append(("ZC", str(self.obstaclesModel.constants.ZC)))
                
        parameterList.append(("Results / Checked Obstacles", "group"))     
        parameterList.append(("Critical Obstacle", "group"))
        parameterList.append(("ID", self.ui.txtID.text()))
        parameterList.append(("X", self.ui.txtX.text()))
        parameterList.append(("Y", self.ui.txtY.text()))
        position = Point3D(float(self.ui.txtX.text()), float(self.ui.txtY.text()), 0)
        positionDegree = QgisHelper.Meter2DegreePoint3D(position)        
        parameterList.append(("Lat", QgisHelper.strDegree(positionDegree.y())))
        parameterList.append(("Lon", QgisHelper.strDegree(positionDegree.x())))
#         DataHelper.strPnlPositionParameter(self.ui.txtX.text(), self.ui.txtY.text(), parameterList)
        parameterList.append(("Altitude(Critical)", self.ui.txtAltitude.text() + " m/" + self.ui.txtAltitudeM.text() + " ft"))       
        parameterList.append(("Surface", self.ui.txtSurface.text()))
        
        parameterList.append(("Results", "group"))
        parameterList.append(("OCH", self.ui.txtOCHResults.text() ))
        parameterList.append(("OCA", self.ui.txtOCAResults.text() ))
        parameterList.append(("Start of Climb", self.ui.txtResultSocText.text() ))
        parameterList.append(("Checked Obstacles", "group"))
        
        for strFilter in self.filterList:
            self.obstaclesModel.setFilterFixedString(strFilter)
            c = self.obstaclesModel.rowCount()
            parameterList.append(("Number of Checked Obstacles(%s)"%strFilter, str(c)))  
        
        return parameterList
class RubberBandPolygon(QgsMapTool):
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.mCanvas = canvas
        self.mRubberBand = None
        self.mRubberBand0 = QgsRubberBand( self.mCanvas, QGis.Polygon )
        self.mCursor = Qt.ArrowCursor
        self.mFillColor = QColor( 254, 178, 76, 63 )
        self.mBorderColour = QColor( 254, 58, 29, 100 )
        self.mRubberBand0.setBorderColor( self.mBorderColour )
        self.polygonGeom = None
        self.drawFlag = False
#         self.constructionLayer = constructionLayer
    def canvasPressEvent( self, e ):
        if ( self.mRubberBand == None ):
            self.mRubberBand0.reset( QGis.Polygon )
#             define._canvas.clearCache ()
            self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRubberBand0 = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRubberBand.setFillColor( self.mFillColor )
            self.mRubberBand.setBorderColor( self.mBorderColour )
            self.mRubberBand0.setFillColor( self.mFillColor )
            self.mRubberBand0.setBorderColor( self.mBorderColour )
        if ( e.button() == Qt.LeftButton ):
            self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )
        else:
            if ( self.mRubberBand.numberOfVertices() > 2 ):
                self.polygonGeom = self.mRubberBand.asGeometry()
            else:
                return
#                 QgsMapToolSelectUtils.setSelectFeatures( self.mCanvas, polygonGeom, e )
            self.mRubberBand.reset( QGis.Polygon )
            self.mRubberBand0.addGeometry(self.polygonGeom, None)
            self.mRubberBand0.show()
            self.mRubberBand = None
            self.emit(SIGNAL("outputResult"), self.polygonGeom)

    def canvasMoveEvent( self, e ):
        pass
        if ( self.mRubberBand == None ):
            return
        if ( self.mRubberBand.numberOfVertices() > 0 ):
            self.mRubberBand.removeLastPoint( 0 )
            self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )

    def deactivate(self):
#         self.rubberBand.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))