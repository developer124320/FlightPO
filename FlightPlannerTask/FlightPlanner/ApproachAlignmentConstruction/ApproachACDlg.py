# -*- coding: utf-8 -*-
'''
Created on 18 May 2014

@author: Administrator
'''

from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.types import Point3D, SurfaceTypes, QATableType
from FlightPlanner.helpers import MathHelper, Unit
from qgis.core import QGis, QgsVectorLayer
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Captions import Captions
from FlightPlanner.FlightPlanBaseSimpleDlg import FlightPlanBaseSimpleDlg
from FlightPlanner.ApproachAlignmentConstruction.ui_ApproachACDlg import Ui_Form_AAC
from FlightPlanner.messages import Messages
from FlightPlanner.Dialogs.DlgQaHeading import DlgQaHeading
from FlightPlanner.polylineArea import PolylineArea
from Type.String import StringBuilder
from FlightPlanner.QtObjectMethods import ComboBox
from Type.QA.QaHeadingColumn import QaHeadingColumn
from Type.QA.QaWindow import QaWindow
from Type.QA.QATable import QATable
from PyQt4.QtCore import SIGNAL, QString
from PyQt4.QtGui import QApplication, QMessageBox
import define

class ApproachACDlg(FlightPlanBaseSimpleDlg):    
    def __init__(self, parent):
        FlightPlanBaseSimpleDlg.__init__(self, parent)
        self.setObjectName("ApproachAlignmentDesigner")
        self.surfaceType = SurfaceTypes.ApproachAlignment
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.ApproachAlignment)
        QgisHelper.matchingDialogSize(self, 670, 600)

        self.arpFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.rwyFeatureArray = []
        self.thrPoint3d = None
        self.thrEndPoint3d = None
        self.resultLayers = []
        self.initAerodromeAndRwyCmb()

        pt = QaHeadingColumn("ttt", 2, True)
        d = pt.__class__.__dict__['Index']

        pass

    def initAerodromeAndRwyCmb(self):

        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.arpFeatureArray = self.aerodromeAndRwyCmbFill(self.currentLayer, self.parametersPanel.cmbAerodrome, self.parametersPanel.pnlNavAid, self.parametersPanel.cmbRwyDir)
            self.calcRwyBearing()
    def calcRwyBearing(self):
        try:
            point3End = self.thrEndPoint3d
            point3dThr = self.thrPoint3d

            self.parametersPanel.txtDirection.Value = round(Unit.ConvertRadToDeg(MathHelper.getBearing(point3dThr, point3End)), 4)
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

                    aerodromePositionPanelObj.Point3d = Point3D(long, lat, alt)
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
                self.parametersPanel.pnlEnd.Point3d = Point3D(long, lat, alt)
                break
            break
        self.calcRwyBearing()
    def aerodromeCmbObj_Event_0(self):
        if len(self.arpFeatureArray) == 0:
            return
        self.parametersPanel.pnlNavAid.Point3d = None
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

            self.parametersPanel.pnlNavAid.Point3d = Point3D(long, lat, alt)
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
    
    def btnUpdateQA_Click(self):
        # clip = QApplication.clipboard()
        # QMessageBox.warning(self, "WWW", clip.text())
        # dlg = QaWindow(self)
        # dlg.show()

        if (not self.method_27(False)):
            return;
        text = self.windowTitle();
        flag, text = DlgQaHeading.smethod_0(self, text)
        if (flag):
            qATable = QATable()
            qATable.TableType = QATableType.General,
            qATable.Heading = text
            stringBuilder = StringBuilder();
            stringBuilder.AppendLine("Runway THR");
            stringBuilder.AppendLine(self.parametersPanel.pnlTHR.method_8("    "));
            stringBuilder.AppendLine("Navigational AID Position");
            stringBuilder.AppendLine(self.parametersPanel.pnlNavAid.method_8("    "));
            stringBuilder.AppendLine(self.parametersPanel.grbParameters.title());
            stringBuilder.AppendLine(self.parametersPanel.txtDirection.method_6("    "));
            stringBuilder.AppendLine(ComboBox.method_11(self.parametersPanel.cmbCategory, self.parametersPanel.label_69, "    "));
            qATable.Text = stringBuilder.ToString();
            FlightPlanBaseSimpleDlg.method_27(self, qATable);
    
    def btnConstruct_Click(self):
        flag = FlightPlanBaseSimpleDlg.btnConstruct_Click(self)
        if not flag:
            return
        num = 0.0
        point3d = Point3D()
        point3d1 = Point3D()
        if not self.method_27(True):
            return


        
        point3d2 = self.parametersPanel.pnlTHR.getPoint3D()
        point3d3 = self.parametersPanel.pnlNavAid.getPoint3D()
        num1 = Unit.ConvertDegToRad(float(self.parametersPanel.txtDirection.Value))
        point3d4 = MathHelper.distanceBearingPoint(point3d2, num1 + 3.14159265358979, 1400)
        num2 = -1
        if MathHelper.smethod_115(point3d3, point3d2, point3d4):
            num2 = 1
        point3d5 = MathHelper.distanceBearingPoint(point3d4, num2 * 1.5707963267949 + num1, 150)
        point3d6 = MathHelper.distanceBearingPoint(point3d5, num1 + 3.14159265358979, 17120)
        if self.parametersPanel.cmbCategory.currentIndex() != 1:
            num = 0.267949192 
        elif self.parametersPanel.cmbCategory.currentIndex() == 1: 
            num = 0.577350269
        point3d7 = MathHelper.distanceBearingPoint(point3d6, num1 - num2 * 1.5707963267949, 150 + num * 17120)
        MathHelper.distanceBearingPoint(point3d5, num1, 150 / num)
        point3d = MathHelper.getIntersectionPoint(point3d3, MathHelper.distanceBearingPoint(point3d3, num1 + 1.5707963267949, 100), point3d2, point3d4)
        if point3d == None:
            raise UserWarning, Messages.ERR_FAILED_TO_CALCULATE_INTERSECTION_POINT
        num3 = MathHelper.calcDistance(point3d3, point3d) / 0.087488664
        if MathHelper.calcDistance(point3d, point3d4) >= num3:
            point3d1 = point3d4
            MathHelper.distanceBearingPoint(point3d6, num1 - num2 * 1.5707963267949, 1525.321791)
        else:
            point3d1 = MathHelper.distanceBearingPoint(point3d, num1 + 3.14159265358979, num3)
            MathHelper.distanceBearingPoint(point3d6, num1 - num2 * 1.5707963267949, 150 + 0.087488664 * (17120 - MathHelper.calcDistance(point3d4, point3d1)))
        MathHelper.distanceBearingPoint(point3d4, num1 + 3.14159265358979, 17120);

        constructionLayer = AcadHelper.createVectorLayer("AAConstruction", QGis.Line)
        AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, PolylineArea([point3d7, point3d4]))
        AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, PolylineArea([point3d1, point3d4, point3d5]))

        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.ApproachAlignment)
        QgisHelper.zoomToLayers([constructionLayer])
        self.resultLayerList = [constructionLayer]

    def method_27(self, bool_0):
#         this.errorProvider.method_1();
#         if bool_0:
#             base.method_26();
#         }
#         self.pnlTHR.method_6();
#         this.pnlNavAid.method_6();
#         this.pnlDirection.method_0();
#         this.pnlCategory.method_0();
        if not self.parametersPanel.pnlTHR.IsValid() or not self.parametersPanel.pnlNavAid.IsValid() :
            return False
        return True#!this.errorProvider.HasErrors;
    def initParametersPan(self):
        ui = Ui_Form_AAC()
        self.parametersPanel = ui
        
        FlightPlanBaseSimpleDlg.initParametersPan(self)        
        
        self.parametersPanel.pnlNavAid = PositionPanel(self.ui.scrollAreaWidgetContents)
        self.parametersPanel.pnlNavAid.groupBox.setTitle("Navigational AID Position")
        self.parametersPanel.pnlNavAid.hideframe_Altitude()
        self.parametersPanel.pnlNavAid.setObjectName("positionNavAid")
        self.parametersPanel.pnlNavAid.btnCalculater.hide()
        self.parametersPanel.verticalLayout_AAC.insertWidget(2, self.parametersPanel.pnlNavAid)

        
        self.parametersPanel.pnlTHR = PositionPanel(self.ui.scrollAreaWidgetContents)
        self.parametersPanel.pnlTHR.groupBox.setTitle("Runway THR")
        self.parametersPanel.pnlTHR.btnCalculater.hide()
        self.parametersPanel.pnlTHR.hideframe_Altitude()
        self.parametersPanel.pnlTHR.setObjectName("positionTHR")
        self.parametersPanel.verticalLayout_AAC.insertWidget(3, self.parametersPanel.pnlTHR)
        self.resize(500,450)
        self.parametersPanel.cmbCategory.addItems([Captions.ALL, Captions.CAT_A_B_ONLY])
        self.connect(self.parametersPanel.pnlTHR, SIGNAL("positionChanged"), self.calcBearing)

        
        self.parametersPanel.pnlEnd = PositionPanel(self.ui.scrollAreaWidgetContents)
        self.parametersPanel.pnlEnd.groupBox.setTitle("Runway End")
        self.parametersPanel.pnlEnd.btnCalculater.hide()
        self.parametersPanel.pnlEnd.hideframe_Altitude()
        self.parametersPanel.pnlEnd.setObjectName("positionEnd")
        self.parametersPanel.verticalLayout_AAC.insertWidget(4, self.parametersPanel.pnlEnd)
        self.connect(self.parametersPanel.pnlEnd, SIGNAL("positionChanged"), self.calcBearing)

#         self.resize(460,350)
#         self.parametersPanel.cmbCategory.addItems([Captions.ALL, Captions.CAT_A_B_ONLY])
        
        '''Event Handlers Connect'''
        
#         self.parametersPanel.cmbCategory.currentIndexChanged.connect(self.chbLeftTurnProhibited_Click)
#         self.parametersPanel.btnCaptureDir.clicked.connect(self.captureBearing)
#         self.captureTrackTool= CaptureBearingTool(define._canvas, self.parametersPanel.txtDirection)
#         self.parametersPanel.pnlEnd.txtPointX.textChanged.connect(self.calcBearing)
#         self.parametersPanel.pnlEnd.txtPointY.textChanged.connect(self.calcBearing)
#         self.parametersPanel.pnlTHR.txtPointX.textChanged.connect(self.calcBearing)
#         self.parametersPanel.pnlTHR.txtPointY.textChanged.connect(self.calcBearing)
    def calcBearing(self):
        try:
            thrPoint = self.parametersPanel.pnlTHR.Point3d
            endPoint = self.parametersPanel.pnlEnd.Point3d
        except:
            return
        bearing = Unit.ConvertRadToDeg(MathHelper.getBearing(thrPoint, endPoint))
        self.parametersPanel.txtDirection.Value = bearing
    def captureBearing(self):
        define._canvas.setMapTool(self.captureTrackTool)
    
    
    