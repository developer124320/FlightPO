# -*- coding: UTF-8 -*-
'''
Created on 25 Apr 2014

@author: Administrator
'''
from PyQt4.QtGui import QDialog, QMessageBox, QStandardItem, QFileDialog, QCheckBox, QFont
from PyQt4.QtCore import QCoreApplication, QString, SIGNAL
from qgis.core import QgsRectangle, QgsVectorLayer

from FlightPlanner.AcadHelper import AcadHelper

from FlightPlanner.types import ConstructionType, SurfaceTypes, Point3D, CriticalObstacleType, ObstacleTableColumnType, \
        AngleUnits, DisregardableObstacleType
from FlightPlanner.helpers import Altitude, Unit, MathHelper, Point3dCollection
from FlightPlanner.helpers import Distance
from FlightPlanner.messages import Messages
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.PinSVisualSegment.ui_VSS import Ui_form_VSS
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.polylineArea import PolylineArea
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
import define
import math

class VisualSegmentSurfaceDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("VisualSegmentSurfaceDlg")
        self.surfaceType = SurfaceTypes.VisualSegmentSurface
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.VisualSegmentSurface)
        QgisHelper.matchingDialogSize(self, 700, 650)
        # self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtTrack)
        self.surfaceArea = None

        self.arpFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.rwyFeatureArray = []
        self.thrPoint3d = None
        self.thrEndPoint3d = None
        self.initAerodromeAndRwyCmb()
    def initAerodromeAndRwyCmb(self):

        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.arpFeatureArray = self.aerodromeAndRwyCmbFill(self.currentLayer, self.parametersPanel.cmbAerodrome, None, self.parametersPanel.cmbRwyDir)
            self.calcRwyBearing()
    def calcRwyBearing(self):
        try:
            point3End = self.parametersPanel.pnlRwyEnd.Point3d
            point3dThr = self.parametersPanel.pnlTHR.Point3d

            self.parametersPanel.txtRwyDir.Value = round(Unit.ConvertRadToDeg(MathHelper.getBearing(point3dThr, point3End)), 4)
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
                aerodromeCmbObjItems = []
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    items = aerodromeCmbObjItems
                    if len(items) != 0:
                        existFlag = False
                        for item in items:
                            if item == attrValue:
                                existFlag = True
                        if existFlag:
                            continue
                    aerodromeCmbObjItems.append(attrValue)
                aerodromeCmbObjItems.sort()
                aerodromeCmbObj.Items = aerodromeCmbObjItems
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
            itemStr = self.parametersPanel.cmbRwyDir.SelectedItem
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
            self.parametersPanel.pnlTHR.Point3d = Point3D(long, lat, alt)

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
                self.parametersPanel.pnlRwyEnd.Point3d = Point3D(long, lat, alt)
                break
            break
        self.calcRwyBearing()
    def aerodromeCmbObj_Event_0(self):
        if len(self.arpFeatureArray) == 0:
            return
        self.parametersPanel.pnlTHR.Point3d = None
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
            if attrValue != self.parametersPanel.cmbAerodrome.SelectedItem:
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
            self.parametersPanel.cmbRwyDir.Clear()
            rwyFeatList = []
            featIter = self.currentLayer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idxAttr].toString()
                if attrValue == self.parametersPanel.cmbAerodrome.SelectedItem:
                    attrValue = feat.attributes()[idxName].toString()
                    s = attrValue.replace(" ", "")
                    compStr = s.left(6).toUpper()
                    if compStr == "THRRWY":
                        valStr = s.right(s.length() - 6)
                        self.parametersPanel.cmbRwyDir.Add(self.parametersPanel.cmbAerodrome.SelectedItem + " RWY " + valStr)
                        rwyFeatList.append(feat)
                        self.rwyFeatureArray = rwyFeatList
            self.rwyDirCmbObj_Event_0()

    def saveData(self):
        fileName = FlightPlanBaseDlg.saveData(self)
        if fileName == None:
            return
        doc = DataHelper.loadXmlDocFromFile(fileName)
        dialogNodeList = doc.elementsByTagName(self.objectName())
        if dialogNodeList.isEmpty():
            raise UserWarning, "self file is not correct."
        dialogElem = dialogNodeList.at(0).toElement()
        elemTrack = doc.createElement("Track")
        
        elemStart = doc.createElement("StartPoint")
        elemX = doc.createElement("X")
        elemX.appendChild(doc.createTextNode(str(self.parametersPanel.txtTrack.captureRadialTool.startPoint.x())))
        elemY = doc.createElement("Y")
        elemY.appendChild(doc.createTextNode(str(self.parametersPanel.txtTrack.captureRadialTool.startPoint.y())))
        elemStart.appendChild(elemX)
        elemStart.appendChild(elemY)
        elemTrack.appendChild(elemStart)
        
        elemEnd = doc.createElement("EndPoint")
        elemX = doc.createElement("X")
        elemX.appendChild(doc.createTextNode(str(self.parametersPanel.txtTrack.captureRadialTool.endPoint.x())))
        elemY = doc.createElement("Y")
        elemY.appendChild(doc.createTextNode(str(self.parametersPanel.txtTrack.captureRadialTool.endPoint.y())))
        elemEnd.appendChild(elemX)
        elemEnd.appendChild(elemY)
        elemTrack.appendChild(elemEnd)
        dialogElem.appendChild(elemTrack)
        DataHelper.saveXmlDocToFile(fileName, doc)
        

    def openData(self):
        try:
            fileName = FlightPlanBaseDlg.openData(self)
            if fileName == None:
                return
            doc = DataHelper.loadXmlDocFromFile(fileName)
            dialogNodeList = doc.elementsByTagName(self.objectName())
            if dialogNodeList.isEmpty():
                raise UserWarning, "self file is not correct."
            dialogElem = dialogNodeList.at(0).toElement()
            trackNodeList = dialogElem.elementsByTagName("Track")
            if trackNodeList.isEmpty():
                return
            elemTrack = trackNodeList.at(0).toElement()
            elemStart = elemTrack.elementsByTagName("StartPoint").at(0).toElement()
            elemEnd = elemTrack.elementsByTagName("EndPoint").at(0).toElement()
        
            x, y = DataHelper.getPointValueFromElem(elemStart)
            self.parametersPanel.txtTrack.captureRadialTool.startPoint = Point3D(x, y)
            
            x, y = DataHelper.getPointValueFromElem(elemEnd)
            self.parametersPanel.txtTrack.captureRadialTool.endPoint = Point3D(x, y)
        except BaseException as e:
            QMessageBox.warning(self, "Error", e.message)

    def btnConstruct_Click(self):
        if len(self.resultLayerList) > 0:
            QgisHelper.removeFromCanvas(define._canvas, self.resultLayerList)
            self.resultLayerList = []
        try:
            point3d = self.parametersPanel.pnlTHR.getPoint3D()
            try:
                num = MathHelper.smethod_4(Unit.ConvertDegToRad(float(self.parametersPanel.txtRwyDir.Value) + 180))
            except ValueError:
                raise UserWarning, "Runway Direction is invalide!"
            altitude = self.parametersPanel.pnlOCAH.method_3(Altitude(point3d.get_Z()));
            metres = altitude.Metres
            if (metres < 10):
                raise UserWarning, Messages.ERR_INSUFFICIENT_MINIMUM_ALTITUDE
            try:
                res, point3dCollection = self.method_37(point3d, num, metres, metres / math.tan(Unit.ConvertDegToRad(float(self.parametersPanel.txtDescAngle.Value.Degrees) - 1.12)))
            except ValueError:
                raise UserWarning, "DescAngle is invalide!"
            if (not res):
                return;
            self.surfaceArea = PrimaryObstacleArea(PolylineArea(point3dCollection))
            layer = AcadHelper.createVectorLayer("Visual Segment Surface")
            if (self.parametersPanel.cmbConstructionType.SelectedIndex != ConstructionType.Construct2D):
                face = [point3dCollection.get_Item(0), point3dCollection.get_Item(1), point3dCollection.get_Item(2), point3dCollection.get_Item(3), point3dCollection.get_Item(0)]
                AcadHelper.setGeometryAndAttributesInLayer(layer, face)
                # layer = QgisHelper.createPolylineLayer("Visual Segment Surface 3D", [(face, [])], [])
            else:
                face = point3dCollection
                face.append(point3dCollection[0])
                AcadHelper.setGeometryAndAttributesInLayer(layer, face)
                # layer = QgisHelper.createPolylineLayer("Visual Segment Surface 2D", [(face, [])], [])
            
            QgisHelper.appendToCanvas(define._canvas, [layer], SurfaceTypes.VisualSegmentSurface)
            QgisHelper.zoomToLayers([layer])
            self.resultLayerList = [layer]
            self.ui.btnEvaluate.setEnabled(True)
            
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)
            

    def obstacleTableInit(self):
        return FlightPlanBaseDlg.obstacleTableInit(self)


    def btnEvaluate_Click(self):
        return FlightPlanBaseDlg.btnEvaluate_Click(self)


    def initObstaclesModel(self):
        if self.surfaceArea == None:
            return
        self.obstaclesModel = VisualSegmentSurfaceObstacles([self.surfaceArea], self.ui.chbHideDisregardableObst.isChecked())
        try:
            double_0 = float(self.parametersPanel.txtRwyDir.Value)
        except ValueError:
            raise UserWarning, "Runway Direction is invalid!"
        try:
            double_1 = math.tan(Unit.ConvertDegToRad(float(self.parametersPanel.txtDescAngle.Value.Degrees) - 1.12))
        except ValueError:
            raise UserWarning, "DescAngle is invalid!"
        point3d_0 = MathHelper.distanceBearingPoint(self.parametersPanel.pnlTHR.getPoint3D(), double_0, 60)
        self.obstaclesModel.ptStart = point3d_0;
        self.obstaclesModel.ptStart2 = MathHelper.distanceBearingPoint(point3d_0, double_0 - 1.5707963267949, 100);
        self.obstaclesModel.outbound = double_0;
        self.obstaclesModel.tang = double_1;
        return FlightPlanBaseDlg.initObstaclesModel(self)

    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)   
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        self.ui.chbHideDisregardableObst = QCheckBox(self.ui.grbObstacles)
        self.ui.chbHideDisregardableObst.setText("Hide disregardable obstacles")
        font = QFont()
        font.setFamily("Arial")
        font.setBold(False)
        self.ui.chbHideDisregardableObst.setFont(font)
        self.ui.vlObstacles.addWidget(self.ui.chbHideDisregardableObst)
        return FlightPlanBaseDlg.uiStateInit(self)        

    def initParametersPan(self):
        ui = Ui_form_VSS()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        
        self.connect(self.parametersPanel.pnlTHR, SIGNAL("positionChanged"), self.initResultPanel)
        self.connect(self.parametersPanel.pnlTHR, SIGNAL("positionChanged"), self.calcRwyBearing)
        self.connect(self.parametersPanel.pnlRwyEnd, SIGNAL("positionChanged"), self.calcRwyBearing)
        
        ui.cmbConstructionType.Items = [ConstructionType.Construct2D, ConstructionType.Construct3D]
        ui.cmbRwyCode.Items = [VssRunwayCode.Code12, VssRunwayCode.Code34]
        ui.cmbRwyCode.SelectedIndex = 1
        ui.cmbApproachType.Items = [VssApproachType.NonPrecision, VssApproachType.RwyAlignedPrecision]
        ui.txtTrack.Enabled = True
        
        self.connect(ui.cmbRwyCode, SIGNAL("Event_0"), self.chbAdCodeF_Click)
        self.connect(ui.cmbApproachType, SIGNAL("Event_0"), self.chbAdCodeF_Click)
        # ui.btnMeasureThrFaf.clicked.connect(self.measureToolThrFaf)
        # ui.btnCaptureRwyDir.clicked.connect(self.captureRwyDir)
        # ui.btnCaptureTrack.clicked.connect(self.captureTrack)
        self.connect(ui.chbAdCodeF, SIGNAL("Event+0"), self.chbAdCodeF_Click)
        self.connect(ui.cmbConstructionType, SIGNAL("Event_0"), self.chbAdCodeF_Click)
        
        
        self.ui.chbHideDisregardableObst.stateChanged.connect(self.chbHideDisregardableObst_clicked)
    
        
#         ui.btnConstruct.clicked.connect(self.btnConstruct_Click)
#         ui.btnEvaluate.clicked.connect(self.btnEvaluate_Click)
#         ui.cmbSurface.currentIndexChanged.connect(self.cmbSurfaceChanged)
        self.method_31()
        
    def chbHideDisregardableObst_clicked(self, state):
#         self.obstaclesModel.setFilterKeyColumn(self.obstaclesModel.IndexDisregardable)
#         if state:
        self.FilterDisregardableObstacles(state)
        print "ok"
        pass
#         if state:
#             self.obstaclesModel(state)
    def FilterDisregardableObstacles(self, state):
        if state:
            self.obstaclesModel.setFilterKeyColumn(self.obstaclesModel.IndexDisregardable)
            self.obstaclesModel.setFilterFixedString("No")
#             self.obstaclesModel.setFilterKeyColumn(self.obstaclesModel.IndexSurface)
        else:
            self.obstaclesModel.setFilterKeyColumn(self.obstaclesModel.IndexDisregardable)
            self.obstaclesModel.setFilterFixedString("")
#             self.obstaclesModel.setFilterKeyColumn(self.obstaclesModel.IndexSurface)
    def chbAdCodeF_Click(self):
        if (self.sender() == self.parametersPanel.cmbRwyCode and self.parametersPanel.cmbApproachType.SelectedIndex == 0):
            if (self.parametersPanel.cmbRwyCode.SelectedIndex != 0):
                self.parametersPanel.txtStripWidth.Value = Distance(300)
            else:
                self.parametersPanel.txtStripWidth.Value = Distance(150)
        self.method_31()
        self.method_29()
        
        
    def method_29(self):        
        self.ui.chbHideDisregardableObst.setChecked(False)
        
        
    def method_31(self):
        if (self.parametersPanel.cmbApproachType.SelectedIndex != 1):
            self.parametersPanel.txtTrack.Visible = True
            self.parametersPanel.chbAdCodeF.Visible = False
            self.parametersPanel.txtStripWidth.Visible = True
            self.parametersPanel.txtThrFaf.Visible = True
        else:
            self.parametersPanel.txtTrack.Visible = False
            self.parametersPanel.chbAdCodeF.Visible = True
            self.parametersPanel.txtStripWidth.Visible = False
            self.parametersPanel.txtThrFaf.Visible = False
   
    def method_37(self, point3d_0, double_0, double_1, double_2):#, out Point3dCollection point3dCollection_0)
        point3dCollection_0 = Point3dCollection();
        if (self.parametersPanel.cmbApproachType.SelectedIndex != 0):
            if (self.parametersPanel.cmbRwyCode.SelectedIndex != 0):
                num2 = 120 if (self.parametersPanel.cmbRwyCode.SelectedIndex != 1 or not self.parametersPanel.chbAdCodeF.Checked) else 155
            else:
                num2 = 90;
            point3d = MathHelper.distanceBearingPoint(point3d_0, double_0, 60);
            point3d1 = MathHelper.distanceBearingPoint(point3d, double_0 + 1.5707963267949, num2 / 2).smethod_167(point3d_0.get_Z());
            point3d4 = MathHelper.distanceBearingPoint(point3d, double_0 - 1.5707963267949, num2 / 2).smethod_167(point3d_0.get_Z());
            point3d2 = MathHelper.distanceBearingPoint(point3d1, double_0, double_2).smethod_167(point3d_0.get_Z() + double_1);
            point3d3 = MathHelper.distanceBearingPoint(point3d4, double_0, double_2).smethod_167(point3d_0.get_Z() + double_1);
        else:
            try:
                metres = self.parametersPanel.txtStripWidth.Value.Metres
            except ValueError:
                raise UserWarning, "Strip Width is invalid!"
            point3d7 = MathHelper.distanceBearingPoint(point3d_0, double_0, 1400);
            point3d8 = MathHelper.distanceBearingPoint(point3d7, double_0 - 1.5707963267949, 100)
            try:
                dblTrack = float(self.parametersPanel.txtTrack.Value)
            except ValueError:
                raise UserWarning, "Track is invalid!"
            try:
                dblRwyDir = float(self.parametersPanel.txtRwyDir.Value)
            except ValueError:
                raise UserWarning, "Runway Direction is invalid!"
            listTurn = []
            num3 = MathHelper.smethod_77(dblTrack, dblRwyDir, AngleUnits.Degrees, listTurn)
            turnDirection = listTurn[0]
            if (num3 > 31):
                raise UserWarning, Messages.ERR_VSS_COURSE_CHANGE
            
            try:
                point3d5 = MathHelper.getIntersectionPoint(point3d7, point3d8, self.parametersPanel.txtTrack.captureRadialTool.startPoint, self.parametersPanel.txtTrack.captureRadialTool.endPoint)
            except AttributeError:
                raise UserWarning, "Please pick up Inbound Track!"
            if point3d5 == None:
                raise UserWarning, Messages.ERR_VSS_INTERSECTION_POINT_1400m
            num4 = MathHelper.calcDistance(point3d7, point3d5);
            if (num4 > 151):
                raise UserWarning, Messages.ERR_VSS_GATE
            try:
                dblThrFaf = float(self.parametersPanel.txtThrFaf.Value.Metres)
            except ValueError:
                raise UserWarning, "ThrFaf is invalid!"
            point3d6 = MathHelper.getIntersectionPoint(point3d_0, MathHelper.distanceBearingPoint(point3d_0, double_0, 100), self.parametersPanel.txtTrack.captureRadialTool.startPoint, self.parametersPanel.txtTrack.captureRadialTool.endPoint)
            if point3d6 == None:
                if (not MathHelper.smethod_115(point3d5, point3d_0, point3d7)):
                    num = 0.15;
                    num1 = (num4 + 201) / 1340;
                else:
                    num = (num4 + 201) / 1340;
                    num1 = 0.15;
            elif (not MathHelper.smethod_119(point3d6, point3d7, point3d8) and MathHelper.calcDistance(point3d6, point3d7) > 100):
                if (MathHelper.calcDistance(point3d6, point3d7) <= 1400):
                    raise UserWarning, Messages.ERR_VSS_INBOUND_TRACK
                if (not MathHelper.smethod_115(point3d5, point3d_0, point3d7)):
                    num = 0.15;
                    num1 = (num4 + 201) / 1340;
                else:
                    num = (num4 + 201) / 1340;
                    num1 = 0.15;
            elif (MathHelper.calcDistance(point3d6, point3d7) < dblThrFaf - 1400):
                point3d = MathHelper.distanceBearingPoint(point3d6, MathHelper.getBearing(self.parametersPanel.txtTrack.captureRadialTool.endPoint, self.parametersPanel.txtTrack.captureRadialTool.startPoint), 100);
                if (not MathHelper.smethod_115(point3d, point3d_0, point3d7)):
                    num = 0.15;
                    num1 = math.tan(Unit.ConvertDegToRad(num3) + math.atan(0.15));
                else:
                    num = math.tan(Unit.ConvertDegToRad(num3) + math.atan(0.15));
                    num1 = 0.15;
            elif (not MathHelper.smethod_115(point3d5, point3d_0, point3d7)):
                num = 0.15;
                num1 = (num4 + 201) / 1340;
            else:
                num = (num4 + 201) / 1340;
                num1 = 0.15;
            point3d = MathHelper.distanceBearingPoint(point3d_0, double_0, 60);
            point3d1 = MathHelper.distanceBearingPoint(point3d, double_0 - 1.5707963267949, metres / 2).smethod_167(point3d_0.get_Z());
            point3d4 = MathHelper.distanceBearingPoint(point3d, double_0 + 1.5707963267949, metres / 2).smethod_167(point3d_0.get_Z());
            point3d = MathHelper.distanceBearingPoint(point3d1, double_0, double_2);
            point3d2 = MathHelper.distanceBearingPoint(point3d, double_0 - 1.5707963267949, num * double_2).smethod_167(point3d_0.get_Z() + double_1);
            point3d = MathHelper.distanceBearingPoint(point3d4, double_0, double_2);
            point3d3 = MathHelper.distanceBearingPoint(point3d, double_0 + 1.5707963267949, num1 * double_2).smethod_167(point3d_0.get_Z() + double_1);

        point3dCollection_0.Add(point3d1);
        point3dCollection_0.Add(point3d2);
        point3dCollection_0.Add(point3d3);
        point3dCollection_0.Add(point3d4);
        return True, point3dCollection_0
    

    def exportResult(self):
        result, resultHideColumnNames = FlightPlanBaseDlg.exportResult(self)
        if not result:
            return
        
        filePathDir = QFileDialog.getSaveFileName(self, "Export Obstacle Data", QCoreApplication.applicationDirPath (),"ExportObstaclefiles(*.xml)")        
        if filePathDir == "":
            return   
        
#         self.ui.btnExportResult.setEnabled(True)     
        
        parameterList = self.getParameterList()
        DataHelper.saveExportResult(filePathDir, "PinS Visual Segment for Approaches", self.ui.tblObstacles, None, parameterList, resultHideColumnNames)
#         self.obstaclesModel.setFilterFixedString(self.filterList[self.ui.cmbSurface.currentIndex()])
#         return FlightPlanBaseDlg.exportResult(self)
    def getParameterList(self):
        parameterList = []
        parameterList.append(("general", "group"))
        parameterList.append(("Runway", "group"))
        DataHelper.pnlPositionParameter(self.parametersPanel.pnlTHR, parameterList)
        parameterList.append(("Direction", "Plan : " + QString(str(self.parametersPanel.txtRwyDir.txtRadialPlan.Value))))
        parameterList.append(("", "Geodetic : " + QString(str(self.parametersPanel.txtRwyDir.txtRadialGeodetic.Value))))


        parameterList.append(("Code", self.parametersPanel.cmbRwyCode.SelectedItem))
        if self.parametersPanel.cmbApproachType.SelectedIndex == 0:
            parameterList.append(("Strip Width", str(self.parametersPanel.txtStripWidth.Value.Metres) + " m"))
        
        parameterList.append(("Parameters", "group"))
        parameterList.append(("Approach Type", self.parametersPanel.cmbApproachType.SelectedItem))
        parameterList.append(("Descent Angle", QString(str(self.parametersPanel.txtDescAngle.Value.Degrees))))
        parameterList.append(("Minimum Altitude(%s)"%self.parametersPanel.pnlOCAH.cmbMCAH.currentText(), self.parametersPanel.pnlOCAH.txtMCAH.text() + " ft"))
        parameterList.append(("Construction Type", self.parametersPanel.cmbConstructionType.SelectedItem))
        if self.parametersPanel.cmbApproachType.SelectedIndex == 0:
            parameterList.append(("In-bound Track", "Plan : " + QString(str(self.parametersPanel.txtTrack.txtRadialPlan.Value))))
            parameterList.append(("", "Geodetic : " + QString(str(self.parametersPanel.txtTrack.txtRadialGeodetic.Value))))


            parameterList.append(("THR to FAF Distance", str(self.parametersPanel.txtThrFaf.Value.NauticalMiles) + " nm"))
                
        c = self.obstaclesModel.rowCount()
        parameterList.append(("Number of Checked Obstacles", str(c)))  
        return parameterList
class VssApproachType:
    NonPrecision = "Non-precision,non-aligned precision"
    RwyAlignedPrecision = "Runway aligned precision,LOC only, APV 1 & 2"


class VssRunwayCode:
    Code12 = "1,2"
    Code34 = "3,4"
        
        
class VisualSegmentSurfaceObstacles(ObstacleTable):
    def __init__(self, surfaceList, disRegardable = False):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfaceList)
        self.disRegardableFlag = False
        if disRegardable != None:
            self.disRegardableFlag = disRegardable
        # self.surfaceType = SurfaceTypes.VisualSegmentSurface
        # self.ptStart = point3d_0;
        # self.ptStart2 = MathHelper.distanceBearingPoint(point3d_0, double_0 - 1.5707963267949, 100);
        # self.outbound = double_0;
        # self.tang = double_1;
        self.surfaceArea = surfaceList[0]

    def setHiddenColumns(self, tableView):
#         if self.disRegardableFlag:
#             tableView.hideColumn(self.IndexDisregardable)
#         else:
#             tableView.showColumn(self.IndexDisregardable) 
        return ObstacleTable.setHiddenColumns(self, tableView)

         
#     private string title;
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexSurfAltM = fixedColumnCount 
        self.IndexSurfAltFt = fixedColumnCount + 1
        self.IndexDifferenceM = fixedColumnCount + 2
        self.IndexDifferenceFt = fixedColumnCount + 3
        self.IndexCritical = fixedColumnCount + 4
        self.IndexDisregardable = fixedColumnCount + 5
         
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.SurfAltM,
                ObstacleTableColumnType.SurfAltFt,
                ObstacleTableColumnType.DifferenceM,
                ObstacleTableColumnType.DifferenceFt,
                ObstacleTableColumnType.Critical,
                ObstacleTableColumnType.Disregardable
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)
 
    def addObstacleToModel(self, obstacle, checkResult):
        ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
        row = self.source.rowCount() - 1
#         colCount = self.source.columnCount()
          
        item = QStandardItem(str(checkResult[0]))
        item.setData(checkResult[0])
        self.source.setItem(row, self.IndexSurfAltM, item)
          
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[0])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[0]))
        self.source.setItem(row, self.IndexSurfAltFt, item)
          
        item = QStandardItem(str(checkResult[1]))
        item.setData(checkResult[1])
        self.source.setItem(row, self.IndexDifferenceM, item)
          
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[1])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[1]))
        self.source.setItem(row, self.IndexDifferenceFt, item)
          
        item = QStandardItem(str(checkResult[2]))
        item.setData(checkResult[2])
        self.source.setItem(row, self.IndexCritical, item)
  
        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexDisregardable, item)
 

    def checkObstacle(self, obstacle_0):
        if not self.surfaceArea.pointInPolygon(obstacle_0.Position, obstacle_0.Tolerance):
            return
        point3d = MathHelper.getIntersectionPoint(self.ptStart, self.ptStart2, obstacle_0.Position, MathHelper.distanceBearingPoint(obstacle_0.Position, self.outbound + 3.14159265358979, obstacle_0.Tolerance));
        num = max([0.001, MathHelper.calcDistance(obstacle_0.Position, point3d) - obstacle_0.Tolerance])
        z = num * self.tang + self.ptStart.get_Z();
        position = obstacle_0.Position;
        z1 = position.get_Z() + obstacle_0.Trees - z;
        criticalObstacleType = CriticalObstacleType.No;
        if (z1 > 0):
            criticalObstacleType = CriticalObstacleType.Yes;
        disregardableObstacleType = DisregardableObstacleType.No
        if (obstacle_0.Position.get_Z() + obstacle_0.Trees <= self.ptStart.get_Z() + 15):
            disregardableObstacleType = DisregardableObstacleType.Yes;
        self.addObstacleToModel(obstacle_0, [z, z1, criticalObstacleType, disregardableObstacleType]);

 
    def getExtentForLocate(self, sourceRow):
        surfaceLayers = QgisHelper.getSurfaceLayers(self.surfaceType)
        rect = QgsRectangle()
        rect.setMinimal()
        for sfLayer in surfaceLayers:
            rect.combineExtentWith(sfLayer.extent())
        return rect
    