'''
Created on 10 Jun 2014

@author: Administrator
'''
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QString, SIGNAL

from qgis.core import QGis, QgsRectangle, QgsPalLayerSettings, QgsVectorLayer

from FlightPlanner.DmeTolerance.ui_DmeTolerance import Ui_DmeToleranceDlg
from FlightPlanner.FlightPlanBaseSimpleDlg import FlightPlanBaseSimpleDlg
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.types import DmeToleranceCalculationType, DmeToleranceConstructionType, \
    AltitudeUnits, DistanceUnits, Point3D
from FlightPlanner.Captions import Captions
from FlightPlanner.helpers import MathHelper, Distance, Unit, Altitude
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.polylineArea import PolylineArea
import define

import math
from FlightPlanner.types import SurfaceTypes


class DmeToleranceDlg(FlightPlanBaseSimpleDlg):    
    def __init__(self, parent):
        FlightPlanBaseSimpleDlg.__init__(self, parent)
        self.setObjectName("DmeToleranceDlg")
        self.surfaceType = SurfaceTypes.DmeTolerance
        
        self.dmeTolerance = Distance.NaN()
        self.slantTolerance = Distance.NaN()
        self.pilotDistance = Distance.NaN()
        self.groundDistance = Distance.NaN()
        
        self.initParametersPan()
        self.setWindowTitle("DME Tolerance and Slant Range")
        
        self.method_29()
        self.method_28()

        self.resize(550, 550)
        QgisHelper.matchingDialogSize(self, 550, 600)

        self.vorDmeFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.resultLayerList = []
        # self.rwyFeatureArray = []
        # self.thrPoint3d = None
        # self.thrEndPoint3d = None
        self.initBasedOnCmb()
    def initBasedOnCmb(self):

        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.vorDmeFeatureArray = self.basedOnCmbFill(self.currentLayer, self.parametersPanel.cmbBasedOn, self.parametersPanel.pnlDME)
    def basedOnCmbFill(self, layer, basedOnCmbObj, vorDmePositionPanelObj):
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')
        vorDmeList = []
        vorDmeFeatureList = []
        if idx >= 0:
            featIter = layer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idx].toString()
                attrValue = QString(attrValue)
                attrValue = attrValue.replace(" ", "")
                attrValue = attrValue.replace("/", "")
                attrValue = attrValue.toUpper()
                if attrValue == "DME":
                    vorDmeList.append(attrValue)
                    vorDmeFeatureList.append(feat)
            if len(vorDmeList) != 0:

                i = -1
                basedOnCmbObjItems = []
                for feat in vorDmeFeatureList:
                    typeValue = feat.attributes()[idx].toString()
                    nameValue = feat.attributes()[idxName].toString()
                    basedOnCmbObjItems.append(typeValue + " " + nameValue)
                basedOnCmbObjItems.sort()
                basedOnCmbObj.Items = basedOnCmbObjItems
                basedOnCmbObj.SelectedIndex = 0

                # if idxAttributes
                feat = vorDmeFeatureList[0]
                attrValue = feat.attributes()[idxLat].toDouble()
                lat = attrValue[0]

                attrValue = feat.attributes()[idxLong].toDouble()
                long = attrValue[0]

                attrValue = feat.attributes()[idxAltitude].toDouble()
                alt = attrValue[0]

                vorDmePositionPanelObj.Point3d = Point3D(long, lat, alt)
                self.connect(basedOnCmbObj, SIGNAL("Event_0"), self.basedOnCmbObj_Event_0)

        return vorDmeFeatureList
    def basedOnCmbObj_Event_0(self):
        if self.currentLayer == None or not self.currentLayer.isValid():
            return
        layer = self.currentLayer
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')

        feat = self.vorDmeFeatureArray[self.parametersPanel.cmbBasedOn.SelectedIndex]
        attrValue = feat.attributes()[idxLat].toDouble()
        lat = attrValue[0]

        attrValue = feat.attributes()[idxLong].toDouble()
        long = attrValue[0]

        attrValue = feat.attributes()[idxAltitude].toDouble()
        alt = attrValue[0]

        self.parametersPanel.pnlDME.Point3d = Point3D(long, lat, alt)


    def btnConstruct_Click(self):
        flag = FlightPlanBaseSimpleDlg.btnConstruct_Click(self)
        if not flag:
            return
        constructionLayer = AcadHelper.createVectorLayer(SurfaceTypes.DmeTolerance, QGis.Line)
        point3d1 = self.parametersPanel.pnlDME.Point3d
        circleAreaList = []
        
#         length = self.groundDistance.Metres / 5
# #         rectangle = QgsRectangle(point3d1.get_X() - length / 2, point3d1.get_Y() - length / 2, point3d1.get_X() + length / 2, point3d1.get_Y() + length / 2,)
#         point1 = Point3D(point3d1.get_X() - length / 2, point3d1.get_Y() + length / 2)
#         point2 = Point3D(point3d1.get_X() - length / 2, point3d1.get_Y() - length / 2)
        captionCircleLine = []
        centerPoint = None
        radius = 0.0
        arc = None;
        resultPoint3dArrayList = []
        if (self.groundDistance.Metres > 0):
            metres = self.dmeTolerance.valueMetres / 1.7;
            if (self.parametersPanel.cmbConstructionType.currentIndex() != 0):
                num1 = Unit.ConvertDegToRad(float(self.parametersPanel.pnlRadial.Value));
                num2 = math.asin(min([1 / self.groundDistance.NauticalMiles, 1]));
                num3 = num1 + num2
                num4 = num1 - num2
                # arc = PolylineArea()
                # arc.Add(PolylineAreaPoint(point3d1, self.groundDistance.Metres))
                arc = MathHelper.constructArc(point3d1, self.groundDistance.Metres, num3, num4, 30);
                point3d = MathHelper.distanceBearingPoint(point3d1, num1, self.groundDistance.Metres);
                
                captionCircleLine = [MathHelper.distanceBearingPoint(point3d, MathHelper.getBearing(point3d, point3d1) + math.pi / 2, self.groundDistance.Metres / 20), MathHelper.distanceBearingPoint(point3d, MathHelper.getBearing(point3d, point3d1) - math.pi / 2, self.groundDistance.Metres / 20)]
                num = -num1;
                if (self.parametersPanel.chbDrawRadial.isChecked()):
                    line = PolylineArea([point3d1, point3d]);
                    resultPoint3dArrayList.append([point3d1, point3d])
#                     AcadHelper.smethod_18(transaction, blockTableRecord, line, constructionLayer);
            else:
                arc = MathHelper.constructCircle(point3d1, self.groundDistance.Metres, 50);
                circleAreaList.append(PolylineArea(None, point3d1, self.groundDistance.Metres))
                centerPoint = point3d1
                radius = self.groundDistance.Metres
                point3d = MathHelper.distanceBearingPoint(point3d1, 0, self.groundDistance.Metres);
                
                length = self.groundDistance.Metres / 5
#                 rectangle = QgsRectangle(point3d1.get_X() - length / 2, point3d1.get_Y() - length / 2, point3d1.get_X() + length / 2, point3d1.get_Y() + length / 2,)
                point1 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(270), length / 4)#Point3D(point3d.get_X() - length / 4, point3d.get_Y())
                point2 = MathHelper.distanceBearingPoint(point3d, Unit.ConvertDegToRad(90), length / 4)#Point3D(point3d.get_X() + length / 4, point3d.get_Y())
                captionCircleLine = [point1, point2]
                num = 0;
            resultPoint3dArrayList.append(arc)
#             AcadHelper.smethod_18(transaction, blockTableRecord, arc, constructionLayer);
            if (self.parametersPanel.chbWriteText.isChecked()):
                nauticalMiles = self.groundDistance.NauticalMiles;
#                 DBText dBText = AcadHelper.smethod_138(string.Format("{0} DME", nauticalMiles.ToString("0.#")), point3d, metres, 1);
#                 dBText.set_Rotation(num);
#                 AcadHelper.smethod_18(transaction, blockTableRecord, dBText, constructionLayer);
        if (self.parametersPanel.chbDrawDmeTol.isVisible() and self.parametersPanel.chbDrawDmeTol.isChecked() and self.dmeTolerance.IsValid() and arc != None):
            offsetCurf = QgisHelper.offsetCurve(arc, self.dmeTolerance.Metres)
            if self.parametersPanel.cmbConstructionType.currentIndex() == 0:
                circleAreaList.append(PolylineArea(None, centerPoint, radius + self.dmeTolerance.Metres))
            if (self.parametersPanel.cmbConstructionType.currentIndex() == 0):
                endPoint = offsetCurf[0]
                offsetCurf.append(endPoint)
            resultPoint3dArrayList.append(offsetCurf)
#             foreach (Entity offsetCurf in arc.GetOffsetCurves(self.dmeTolerance.Metres))
#             {
#                 AcadHelper.smethod_19(transaction, blockTableRecord, offsetCurf, constructionLayer, 5);
#             }
            entity = QgisHelper.offsetCurve(arc, -(self.dmeTolerance.Metres + self.slantTolerance.Metres))
            if self.parametersPanel.cmbConstructionType.currentIndex() == 0:
                circleAreaList.append(PolylineArea(None, centerPoint, radius -(self.dmeTolerance.Metres + self.slantTolerance.Metres)))
            if (self.parametersPanel.cmbConstructionType.currentIndex() == 0):
                endPoint = entity[0]
                entity.append(endPoint)
            resultPoint3dArrayList.append(entity)
#             foreach (Entity entity in arc.GetOffsetCurves(-(self.dmeTolerance.Metres + self.slantTolerance.Metres)))
#             {
#                 AcadHelper.smethod_19(transaction, blockTableRecord, entity, constructionLayer, 5);
#             }
#         }
        if (self.parametersPanel.chbDrawSlantTol.isVisible() and self.parametersPanel.chbDrawSlantTol.isChecked() and self.slantTolerance.IsValid() and arc != None):
            offsetCurf1 = QgisHelper.offsetCurve(arc, -self.slantTolerance.Metres)
            if self.parametersPanel.cmbConstructionType.currentIndex() == 0:
                circleAreaList.append(PolylineArea(None, centerPoint, radius -self.slantTolerance.Metres))
            if (self.parametersPanel.cmbConstructionType.currentIndex() == 0):
                endPoint = offsetCurf1[0]
                offsetCurf1.append(endPoint)
            resultPoint3dArrayList.append(offsetCurf1)
#             foreach (Entity offsetCurf1 in arc.GetOffsetCurves(-self.slantTolerance.Metres))
#             {
#                 AcadHelper.smethod_19(transaction, blockTableRecord, offsetCurf1, constructionLayer, 2);
#             }
#         }
        if (self.parametersPanel.chbInsertSymbol.isChecked()):
            length = self.groundDistance.Metres / 5
            rectangle = QgsRectangle(point3d1.get_X() - length / 2, point3d1.get_Y() - length / 2, point3d1.get_X() + length / 2, point3d1.get_Y() + length / 2,)
            point1 = MathHelper.distanceBearingPoint(point3d1, Unit.ConvertDegToRad(315), length / 2)#Point3D(point3d1.get_X() - length / 2, point3d1.get_Y() + length / 2)
            point2 = MathHelper.distanceBearingPoint(point3d1, Unit.ConvertDegToRad(225), length / 2)#Point3D(point3d1.get_X() - length / 2, point3d1.get_Y() - length / 2)
            point3 = MathHelper.distanceBearingPoint(point3d1, Unit.ConvertDegToRad(135), length / 2)#Point3D(point3d1.get_X() + length / 2, point3d1.get_Y() - length / 2)
            point4 = MathHelper.distanceBearingPoint(point3d1, Unit.ConvertDegToRad(45), length / 2)#Point3D(point3d1.get_X() + length / 2, point3d1.get_Y() + length / 2)
            resultPoint3dArrayList.append([point1, point2, point3, point4, point1])
#             Symbol symbol = new Symbol(SymbolType.Dme);
#             AcadHelper.smethod_57(transaction, blockTableRecord, symbol.BlockName, symbol.BlockFileName, point3d1, new Scale3d(1), 0, constructionLayer, None);
#         }

        for point3dArray in resultPoint3dArrayList:
            if (self.parametersPanel.cmbConstructionType.currentIndex() != 0):
                bulge = MathHelper.smethod_60(point3dArray[0], point3dArray[int(len(point3dArray)/2)], point3dArray[len(point3dArray)-1])
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, point3dArray, False, {"Bulge":bulge})
        if self.parametersPanel.cmbConstructionType.currentIndex() == 0:
            for area in circleAreaList:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, area)
            if self.parametersPanel.chbInsertSymbol.isChecked():
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [point1, point2, point3, point4, point1])

        
        if (self.parametersPanel.chbWriteText.isChecked()):
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, captionCircleLine, False, {"Caption":"3DME"} )
        
        palSetting = QgsPalLayerSettings()
        palSetting.readFromLayer(constructionLayer)
        palSetting.enabled = True
        palSetting.fieldName = "Caption"
        palSetting.isExpression = True
        palSetting.placement = QgsPalLayerSettings.Line
        palSetting.placementFlags = QgsPalLayerSettings.AboveLine
        palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '12', "")
        palSetting.writeToLayer(constructionLayer)
        
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType, True)
        QgisHelper.zoomToLayers([constructionLayer])
        self.resultLayerList = [constructionLayer]

    def initParametersPan(self):
        ui = Ui_DmeToleranceDlg()
        self.parametersPanel = ui
        FlightPlanBaseSimpleDlg.initParametersPan(self)
        
        '''init panel'''
        self.parametersPanel.pnlDME = PositionPanel(ui.gbConstruction)
        self.parametersPanel.pnlDME.groupBox.setTitle("DME Position")
        self.parametersPanel.pnlDME.btnCalculater.hide()
        self.parametersPanel.pnlDME.hideframe_Altitude()
        self.parametersPanel.pnlDME.setObjectName("positionDme")        
        ui.vl_gbConstruction.insertWidget(1, self.parametersPanel.pnlDME)
        
        self.parametersPanel.cmbCalculationType.addItems([DmeToleranceCalculationType.Ground, DmeToleranceCalculationType.Aircraft])
        self.parametersPanel.cmbConstructionType.addItems([DmeToleranceConstructionType.Circle, DmeToleranceConstructionType.Arc])
        self.parametersPanel.btnMesureSlant.setVisible(False)
        self.parametersPanel.btnMesureTolerance.setVisible(False)
        # self.parametersPanel.txtRadial.setText("0")
        self.parametersPanel.cmbCalculationType.setCurrentIndex(1)
        '''signal and slost'''
        self.parametersPanel.cmbCalculationType.currentIndexChanged.connect(self.method_30)
        self.parametersPanel.txtDistance.textChanged.connect(self.method_30)
        self.parametersPanel.btnMesureDist.clicked.connect(self.measureToolDistance)
        self.parametersPanel.txtAcAltitude.textChanged.connect(self.method_30)
        self.parametersPanel.txtDmeAltitude.textChanged.connect(self.method_30)
        self.parametersPanel.cmbConstructionType.currentIndexChanged.connect(self.method_28)
        # self.parametersPanel.btnCaptureRadial.clicked.connect(self.captureRadial)
        self.parametersPanel.btnMesureAltitude.clicked.connect(self.measureToolAltitude)

        self.parametersPanel.txtAcAltitudeM.textChanged.connect(self.txtAcAltitudeMChanged)
        self.parametersPanel.txtAcAltitude.textChanged.connect(self.txtAcAltitudeFtChanged)

        self.flag = 0
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAcAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAcAltitude.text())), 4)))
            except:
                self.parametersPanel.txtAcAltitudeM.setText("0.0")

        self.parametersPanel.txtDmeAltitude.textChanged.connect(self.txtDmeAltitudeMChanged)
        self.parametersPanel.txtDmeAltitudeFt.textChanged.connect(self.txtDmeAltitudeFtChanged)

        self.flag1 = 0
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtDmeAltitudeFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtDmeAltitude.text())), 4)))
            except:
                self.parametersPanel.txtDmeAltitudeFt.setText("0.0")
    def txtAcAltitudeMChanged(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.parametersPanel.txtAcAltitude.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAcAltitudeM.text())), 4)))
            except:
                self.parametersPanel.txtAcAltitude.setText("0.0")
    def txtAcAltitudeFtChanged(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAcAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAcAltitude.text())), 4)))
            except:
                self.parametersPanel.txtAcAltitudeM.setText("0.0")

    def txtDmeAltitudeMChanged(self):
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtDmeAltitudeFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtDmeAltitude.text())), 4)))
            except:
                self.parametersPanel.txtDmeAltitudeFt.setText("0.0")
    def txtDmeAltitudeFtChanged(self):
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                self.parametersPanel.txtDmeAltitude.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtDmeAltitudeFt.text())), 4)))
            except:
                self.parametersPanel.txtDmeAltitude.setText("0.0")
    def method_28(self):
        if (self.parametersPanel.cmbCalculationType.currentIndex()!= 0):
            self.parametersPanel.label_76.setText(Captions.PILOT_READOUT + " (nm):")
            self.parametersPanel.btnMesureDist.setVisible(False)
        
        else:
            self.parametersPanel.label_76.setText(Captions.GROUND_DISTANCE + " (nm):")
            self.parametersPanel.btnMesureDist.setVisible(True)
        
        self.parametersPanel.cmbConstructionType.setVisible(self.groundDistance.Metres > 0)
        self.parametersPanel.pnlRadial.Visible = False if self.parametersPanel.cmbConstructionType.currentIndex() != 1 else self.groundDistance.Metres > 0
        self.parametersPanel.chbDrawDmeTol.setVisible(self.dmeTolerance.IsValid())
        self.parametersPanel.chbDrawSlantTol.setVisible(self.slantTolerance.IsValid())
        self.parametersPanel.chbDrawRadial.setVisible(self.parametersPanel.cmbConstructionType.currentIndex()== 1)
        self.parametersPanel.chbWriteText.setVisible(self.groundDistance.Metres > 0)

    def method_29(self):
        self.dmeTolerance = Distance.NaN
        self.slantTolerance = Distance.NaN
        self.pilotDistance = Distance.NaN
        self.groundDistance = Distance.NaN
        if self.parametersPanel.txtDistance.text() == "" or self.parametersPanel.txtAcAltitude.text() == "" or self.parametersPanel.txtDmeAltitude.text() == "":
            self.parametersPanel.gbResult.setVisible(False)
        else:
            nauticalMiles = float(self.parametersPanel.txtDistance.text())
            metres = Altitude(float(self.parametersPanel.txtAcAltitude.text()), AltitudeUnits.FT).Metres
            value = Altitude(float(self.parametersPanel.txtDmeAltitude.text()))
            num = Unit.ConvertMeterToNM(metres - value.Metres)
            if (nauticalMiles <= 0):
                self.parametersPanel.label_72.setText(Captions.DME_TOLERANCE_OVERHEAD)
                self.dmeTolerance = Distance(460)
            elif (num <= nauticalMiles):
                if (self.parametersPanel.cmbCalculationType.currentIndex() != 0):
                    self.groundDistance = Distance(math.sqrt(nauticalMiles * nauticalMiles - num * num), DistanceUnits.NM)
                    self.pilotDistance = Distance(nauticalMiles, DistanceUnits.NM)
                    self.slantTolerance = Distance(self.pilotDistance.NauticalMiles - self.groundDistance.NauticalMiles, DistanceUnits.NM)
                    self.parametersPanel.lblResultDistance.setText(Captions.GROUND_DISTANCE)
                    self.parametersPanel.label_72.setText(Captions.DME_TOLERANCE)
                    self.parametersPanel.txtResultDistance.setText(str(round(self.groundDistance.NauticalMiles,2)) +" nm" + " / " + str(round(self.groundDistance.Metres,2)) +" m")
                else:
                    self.pilotDistance = Distance(math.sqrt(nauticalMiles * nauticalMiles + num * num), DistanceUnits.NM)
                    self.groundDistance = Distance(nauticalMiles, DistanceUnits.NM)
                    self.slantTolerance = Distance(nauticalMiles - math.sqrt(nauticalMiles * nauticalMiles - num * num), DistanceUnits.NM)
                    self.parametersPanel.lblResultDistance.setText(Captions.PILOT_READOUT)
                    self.parametersPanel.label_72.setText(Captions.DME_TOLERANCE)
                    self.parametersPanel.txtResultDistance.setText(str(round(self.pilotDistance.NauticalMiles, 2)) +" nm" + " / " + str(round(self.pilotDistance.Metres, 2)) +" m")
                
                self.dmeTolerance = Distance(Unit.ConvertNMToMeter(self.pilotDistance.NauticalMiles * 0.0125) + 460)
            else:
                flag = False
            if (self.dmeTolerance.IsValid()):
                self.parametersPanel.txtResultDmeTol.setText(str(round(self.dmeTolerance.NauticalMiles, 2)) +" nm" + " / " + str(round(self.dmeTolerance.Metres, 2)) +" m")
            
            if (self.slantTolerance.IsValid()):
                self.parametersPanel.txtResultSlantTol.setText(str(round(self.slantTolerance.NauticalMiles, 2)) +"nm" + " / " + str(round(self.slantTolerance.Metres, 2)) +" m")
            self.parametersPanel.frame_62.setVisible(False if not self.pilotDistance.IsValid() else self.groundDistance.IsValid())
            self.parametersPanel.frame_TakeOffSurfaceTrack_2.setVisible(self.dmeTolerance.IsValid())
            self.parametersPanel.frame_TakeOffSurfaceTrack_3.setVisible(self.slantTolerance.IsValid())
#                 self.txtResult.Visible = !flag
            self.parametersPanel.gbResult.setVisible(True)
            
           
    def method_30(self):
        self.method_29()
        self.method_28()
        
    def measureToolDistance(self):
        measureThrFaf = MeasureTool(define._canvas, self.parametersPanel.txtDistance, DistanceUnits.NM)
        define._canvas.setMapTool(measureThrFaf)
    
    def measureToolAltitude(self):
        measureThrFaf = MeasureTool(define._canvas, self.parametersPanel.txtDmeAltitude)
        define._canvas.setMapTool(measureThrFaf)
    # def captureRadial(self):
    #     CaptureBearingTrackFrom = CaptureBearingTool(define._canvas, self.parametersPanel.txtRadial)
    #     define._canvas.setMapTool(CaptureBearingTrackFrom)
        