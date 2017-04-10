'''
Created on 29 May 2014

@author: Administrator
'''
from PyQt4.QtGui import QMessageBox, QAbstractItemView, QInputDialog, QPushButton,\
         QSizePolicy, QLabel, QFrame
from PyQt4.QtCore import QVariant, Qt, QAbstractTableModel, SIGNAL, QModelIndex, QSize
from FlightPlanner.DepartureNominal.ui_DepartureNominal import Ui_DepartureNominal
from FlightPlanner.FlightPlanBaseSimpleDlg import FlightPlanBaseSimpleDlg
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.types import SurfaceTypes, ConstructionType, AngleUnits, TurnDirection,\
     AltitudeUnits, DistanceUnits, Point3D
from FlightPlanner.Captions import Captions
from FlightPlanner.helpers import Speed, MathHelper, Altitude, Unit, Distance
from FlightPlanner.validations import Validations
from FlightPlanner.polylineArea import PolylineAreaPoint,PolylineArea
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.captureCoordinateTool import CaptureCoordinateToolUpdate
from FlightPlanner.messages import Messages

from qgis.core import QGis, QgsVectorLayer, QgsGeometry, QgsFeature, QgsField, QgsPalLayerSettings
import math, define

class DepartureNominalDlg(FlightPlanBaseSimpleDlg):    
    def __init__(self, parent):
        FlightPlanBaseSimpleDlg.__init__(self, parent)
        self.setObjectName("CRM")
        self.surfaceType = SurfaceTypes.DepartureNominal
        self.initParametersPan()
#         self.uiStateInit()
        self.setWindowTitle(SurfaceTypes.DepartureNominal + " Construction")
        self.speeds = []
        self.method_28()
        self.method_29()
#         self.method_31()
        self.resize(780, 580)
        QgisHelper.matchingDialogSize(self, 820, 620)
        self.multiplePoint3d = []
        self.constructionLayer = None
        self.polyline = PolylineArea();
        self.mouseMove = False
        self.multipointFlag = False
        self.startMulti = False
        self.multiPolylineCount = 0
        self.constructFlag = False
        self.featMultiEnd = None
        self.featConstruct = None
        self.markConstructFeatIds = []
        self.markMultiFeatIds = []
#         define._canvas.xyCoordinates.connect(self.mouseMoveHandler)
    def mouseMoveHandler(self, point):
        if self.mouseMove:
            percent = float(self.parametersPanel.txtPdg.text())/ 100;
            value = float(self.parametersPanel.txtIsa.text())
            appendResult = self.method_39(self.polyline, Point3D(point.x(), point.y()).smethod_176(), self.parametersPanel.pnlDer.Point3d, percent, value);
            define._messageLabel.setText(appendResult)
    def btnConstruct_Click(self):
        flag = FlightPlanBaseSimpleDlg.btnConstruct_Click(self)
        if not flag:
            return
        point3d = self.parametersPanel.pnlDer.Point3d;
        point3d1 = self.parametersPanel.pnlPosition1.Point3d;
        point3d2 = self.parametersPanel.pnlPosition2.Point3d;
        percent = float(self.parametersPanel.txtPdg.text())/ 100;
        value = float(self.parametersPanel.txtIsa.text())
#         self.method_37(transaction, blockTableRecord, self.constructionLayer, polyline, point3d, percent);

        polyline_0 = PolylineArea()
        self.method_39(polyline_0, point3d.smethod_176(), point3d, percent, value);
        self.method_39(polyline_0, point3d1.smethod_176(), point3d, percent, value);
        self.method_39(polyline_0, point3d2.smethod_176(), point3d, percent, value);
        mapUnits = define._canvas.mapUnits()

        if (self.parametersPanel.cmbConstructionType.currentText() != "2D"):
            pass
        else:
            if self.constructionLayer == None:
                self.constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
                AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, polyline_0)
                QgisHelper.appendToCanvas(define._canvas, [self.constructionLayer], SurfaceTypes.DepartureNominal)
                QgisHelper.zoomToLayers([self.constructionLayer])
                self.constructFlag = True
                iter = self.constructionLayer.getFeatures()
                for feat in iter:
                    self.featConstruct = feat
                palSetting = QgsPalLayerSettings()
                palSetting.readFromLayer(self.constructionLayer)
                palSetting.enabled = True
                palSetting.fieldName = "Caption"
                palSetting.isExpression = True
                palSetting.placement = QgsPalLayerSettings.Line
                palSetting.placementFlags = QgsPalLayerSettings.AboveLine
                palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '8', "")
                palSetting.writeToLayer(self.constructionLayer)
            else:
                self.constructionLayer.startEditing()
                if self.featConstruct != None:
                    self.constructionLayer.deleteFeature(self.featConstruct.id())
                self.constructionLayer.commitChanges()
                AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, polyline_0)
                # feature = QgsFeature()
                # feature.setGeometry(QgsGeometry.fromPolyline(polyline_0.method_14()))
                # feature.setAttributes([""])
                # self.constructionLayer.addFeature(feature)
                #
                # self.constructionLayer.commitChanges()
                self.constructionLayer.triggerRepaint()
                iter = self.constructionLayer.getFeatures()
                for feat in iter:
                    self.featConstruct = feat
#                 QgisHelper.appendToCanvas(define._canvas, [self.constructionLayer], SurfaceTypes.DepartureNominal)

        self.constructionLayer.startEditing()
        if len(self.markConstructFeatIds) > 0:
            for i in self.markConstructFeatIds:
                self.constructionLayer.deleteFeature(i)
        self.constructionLayer.commitChanges()
        markResult = self.method_37(PolylineArea(polyline_0.method_14()), point3d, percent)
        self.markConstructFeatIds = []
        for pointList, caption in  markResult:
            AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, pointList, False, {"Caption":caption})
            iter = self.constructionLayer.getFeatures()
            for feat in iter:
                featId = feat.id()
            self.markConstructFeatIds.append(featId)

        self.constructionLayer.triggerRepaint()
        # return FlightPlanBaseSimpleDlg.btnConstruct_Click(self)


    def uiStateInit(self):
        self.ui.btnMultiple = QPushButton(self.ui.frame_Btns)
        self.ui.verticalLayout_Btns.insertWidget(3, self.ui.btnMultiple)
        self.ui.btnMultiple.setText("")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui.btnMultiple.sizePolicy().hasHeightForWidth())
        self.ui.btnMultiple.setSizePolicy(sizePolicy)
        
        self.ui.btnMultiple.setToolTip("Multiple Positions")
#         self.ui.btnMultiple.setMinimumSize(QSize(0, 40))
#         self.ui.btnMultiple.setMaximumSize(QSize(100, 40))
        
        self.ui.btnMultiple.clicked.connect(self.btnMultiple_Click)    
        return FlightPlanBaseSimpleDlg.uiStateInit(self)
      
    def initParametersPan(self):
        ui = Ui_DepartureNominal()
        self.parametersPanel = ui
        FlightPlanBaseSimpleDlg.initParametersPan(self)
        self.ui.btnMultiple.setIcon(ui.iconMulti)
        self.CaptureCoordTool = CaptureCoordinateToolUpdate(define._canvas) 
        
        '''init panel'''
        self.parametersPanel.pnlPosition1 = PositionPanel(ui.gbP1)
        self.parametersPanel.pnlPosition1.btnCalculater.hide()
        self.parametersPanel.pnlPosition1.hideframe_Altitude()
        self.parametersPanel.pnlPosition1.setObjectName("pnlPosition1")
        ui.vLayout_P1.insertWidget(0, self.parametersPanel.pnlPosition1)
        
        self.parametersPanel.pnlPosition2 = PositionPanel(ui.gbP2)
        self.parametersPanel.pnlPosition2.btnCalculater.hide()
        self.parametersPanel.pnlPosition2.hideframe_Altitude()
        self.parametersPanel.pnlPosition2.setObjectName("pnlPosition2")
        ui.vLayout_p2.insertWidget(0, self.parametersPanel.pnlPosition2)
        
        self.parametersPanel.pnlDer = PositionPanel(ui.frmoMain)
        self.parametersPanel.pnlDer.groupBox.setTitle("DER Position")
        self.parametersPanel.pnlDer.btnCalculater.hide()
        self.parametersPanel.pnlDer.setObjectName("pnlDer")
        ui.vLayout_Main.insertWidget(0, self.parametersPanel.pnlDer)
        
        self.parametersPanel.tblSpeeds.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.parametersPanel.cmbConstructionType.addItems([ConstructionType.Construct2D, ConstructionType.Construct3D])
        i = 1
        while (i < 11):
            self.parametersPanel.cmbSpeedEvery.addItem(str(i)+"nm", QVariant(i))
            i += 1
        
        '''Event Handlers Connect'''
        self.parametersPanel.tblSpeeds.clicked.connect(self.method_30)
        self.parametersPanel.btnEdit.clicked.connect(self.mniEdit_Click)
        self.parametersPanel.btnReset.clicked.connect(self.mniReset_Click)
        self.parametersPanel.txtPdg.textChanged.connect(self.method_31)
        self.parametersPanel.txtIsa.textChanged.connect(self.method_31)
        self.connect(self.parametersPanel.pnlDer, SIGNAL("positionChanged"), self.method_31)
        self.connect(self.parametersPanel.pnlPosition2, SIGNAL("positionChanged"), self.method_31)
        self.connect(self.parametersPanel.pnlPosition1, SIGNAL("positionChanged"), self.method_31)
        self.connect(self.CaptureCoordTool, SIGNAL("resultPointValueList"), self.resultPointValueListMethod)

        self.parametersPanel.txtAltitudeM1.textChanged.connect(self.txtAltitudeM1Changed)
        self.parametersPanel.txtAltitude1.textChanged.connect(self.txtAltitudeFt1Changed)

        self.flag = 0


        self.parametersPanel.txtAltitudeM2.textChanged.connect(self.txtAltitudeM2Changed)
        self.parametersPanel.txtAltitude2.textChanged.connect(self.txtAltitudeFt2Changed)

        self.flag1 = 0

    def txtAltitudeM1Changed(self):
        if self.flag==0:
            self.flag=1;
        if self.flag==2:
            self.flag=0;
        if self.flag==1:
            try:
                self.parametersPanel.txtAltitude1.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM1.text())), 4)))
            except:
                self.parametersPanel.txtAltitude1.setText("0.0")
    def txtAltitudeFt1Changed(self):
        if self.flag==0:
            self.flag=2;
        if self.flag==1:
            self.flag=0;
        if self.flag==2:
            try:
                self.parametersPanel.txtAltitudeM1.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude1.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM1.setText("0.0")
    def txtAltitudeM2Changed(self):
        if self.flag1==0:
            self.flag1=1;
        if self.flag1==2:
            self.flag1=0;
        if self.flag1==1:
            try:
                self.parametersPanel.txtAltitude2.setText(str(round(Unit.ConvertMeterToFeet(float(self.parametersPanel.txtAltitudeM2.text())), 4)))
            except:
                self.parametersPanel.txtAltitude2.setText("0.0")
    def txtAltitudeFt2Changed(self):
        if self.flag1==0:
            self.flag1=2;
        if self.flag1==1:
            self.flag1=0;
        if self.flag1==2:
            try:
                self.parametersPanel.txtAltitudeM2.setText(str(round(Unit.ConvertFeetToMeter(float(self.parametersPanel.txtAltitude2.text())), 4)))
            except:
                self.parametersPanel.txtAltitudeM2.setText("0.0")
    def method_28(self):
        self.speeds = []
        self.speeds.append(Speed(185))
        self.speeds.append(Speed(192))
        self.speeds.append(Speed(200))
        self.speeds.append(Speed(209))
        self.speeds.append(Speed(218))
        self.speeds.append(Speed(229))
        self.speeds.append(Speed(238))
        self.speeds.append(Speed(244))
        self.speeds.append(Speed(248))
        self.speeds.append(Speed(252))
        self.speeds.append(Speed(255))
        self.speeds.append(Speed(258))
        self.speeds.append(Speed(261))
        self.speeds.append(Speed(263))
        self.speeds.append(Speed(265))
        self.speeds.append(Speed(266))
        self.speeds.append(Speed(267))
        self.speeds.append(Speed(269))
        self.speeds.append(Speed(271))
        self.speeds.append(Speed(272))
        self.speeds.append(Speed(276))
        self.speeds.append(Speed(278))
        self.speeds.append(Speed(280))
        self.speeds.append(Speed(283))
        self.speeds.append(Speed(284))
        self.speeds.append(Speed(286))
    
    def method_29(self):
        
        self.tblModel = tableModel()
#         self.tblModel.re
        for rowNum in range(len(self.speeds)):                       
            self.tblModel.Add((rowNum + 1, self.speeds[rowNum].Knots))
        self.parametersPanel.tblSpeeds.setModel(self.tblModel)
    
    def method_30(self):
        selectedIndexes = self.parametersPanel.tblSpeeds.selectedIndexes()
        if len(selectedIndexes) > 0 :
            self.parametersPanel.btnEdit.setEnabled(True) 
        else:
            self.parametersPanel.btnEdit.setEnabled(False)
    def method_31(self, point3d0 = None, point3d1 = None, point3d2 = None):
#         double num
#         double num1
#         double num2
#         Point3d point3d
#         Point3d point3d1
#         bool flag
#         bool flag1
        nOTAPPLICABLE = Captions.NOT_APPLICABLE
        nVALIDPOSITION = Captions.NOT_APPLICABLE
        try:
                    
            try:
            
                if (self.parametersPanel.txtPdg.text() == ""):
                    flag1 = False
                    return (flag1, Validations.INVALID_POSITION)
                elif point3d0 != None:
                    point3d2 = point3d0
                    z = point3d2.get_Z()
#                     if (self.parametersPanel.pnlPosition1.IsValid()):
                    point3d3 = point3d1
                    if ( not MathHelper.smethod_96(MathHelper.calcDistance(point3d2, point3d3))):
                        num3 = MathHelper.calcDistance(point3d2, point3d3)
                        percent = float(self.parametersPanel.txtPdg.text())/ 100
                        num4 = z + percent * num3
                        nOTAPPLICABLE = "%.1f"%(Altitude(num4).Feet)
#                         if (self.parametersPanel.pnlPosition2.IsValid()):
                        point3d4 = point3d2
                        if (MathHelper.smethod_96(MathHelper.calcDistance(point3d3, point3d4))):
                            nVALIDPOSITION = Validations.INVALID_POSITION
                            flag1 = False
                            return (flag1, Validations.INVALID_POSITION)
                        
                        elif (MathHelper.smethod_84(point3d2, point3d3, point3d4, AngleUnits.Radians) > 0.26):
                            num5 = int(math.trunc(Unit.ConvertMeterToNM(num3)) + 1)
                            if (num5 > 25):                                    
                                num5 = 25
                            
                            speed = self.speeds[num5]
                            speed1 = Speed.smethod_0(speed, float(self.parametersPanel.txtIsa.text()), Altitude(num4))
                            if (percent >= 0):
                                feet = (Altitude(percent * num3)).Feet
                                if (feet <= 3000):
                                    num1 = (15 if feet <= 1000 else 20)
                                
                                else:
                                    num1 = 25
                                
                            else:                                    
                                num1 = 25
                            
                            num6 = 3.14159265358979 * (num1 / 180.0)
                            num7 = math.sin(num6) / math.cos(num6)
                            num8 = min([3431 * num7 / (3.14159265358979 * speed1.Knots), 3])
                            num9 = Unit.ConvertNMToMeter(speed1.Knots / (3.14159265358979 * num8 * 20))
                            flag2 = MathHelper.smethod_115(point3d4, point3d2, point3d3)
                            flag3 = flag2
                            point3d = (MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d2, point3d3) + 1.5707963267949, num9) if not flag2 else MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d2, point3d3) - 1.5707963267949, num9))
                            if (MathHelper.calcDistance(point3d, point3d4) >= num9):
                                num10 = MathHelper.calcDistance(point3d, point3d4)
                                num11 = math.sin(num10 * num10 - num9 * num9)
                                num12 = math.atan(num9 / num11)
                                if (not flag3):
                                    point3d1 = MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d) + num12, num11)
                                    flag = MathHelper.smethod_115(point3d1, point3d, point3d3)
                                
                                else:
                                    point3d1 = MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d) - num12, num11)
                                    flag = MathHelper.smethod_115(point3d1, point3d3, point3d)
                                
                                num13 = MathHelper.smethod_84(point3d3, point3d, point3d1, AngleUnits.Radians)
                                num2 = (3.14159265358979 - num13 if not flag else 3.14159265358979 + num13)
                                num14 = num2 * num9
                                num = MathHelper.calcDistance(point3d1, point3d4) + num14
                                altitude = Altitude(num4 + percent * num)
                                nVALIDPOSITION = "%.1f"%altitude.Feet
                                flag1 = True
                                return (flag1, nVALIDPOSITION)
                            
                            else:
                                nVALIDPOSITION = Validations.POSITION_INSIDE_TURN
                                return (False, Validations.INVALID_POSITION)
                        
                        else:
                            num = MathHelper.calcDistance(point3d3, point3d4)
                            altitude1 = Altitude(num4 + percent * num)
                            nVALIDPOSITION = "%.1f"%altitude1.Feet
                            flag1 = True
                            return (flag1, nVALIDPOSITION)
                            
                        
                     
                    else:
                        nOTAPPLICABLE = Validations.INVALID_POSITION
                        flag1 = False
                        return (flag1, nOTAPPLICABLE)
                        
                    
                elif (self.parametersPanel.pnlDer.IsValid()):
                    point3d2 = self.parametersPanel.pnlDer.Point3d
                    z = point3d2.get_Z()
                    if (self.parametersPanel.pnlPosition1.IsValid()):
                        point3d3 = self.parametersPanel.pnlPosition1.Point3d
                        if ( not MathHelper.smethod_96(MathHelper.calcDistance(point3d2, point3d3))):
                            num3 = MathHelper.calcDistance(point3d2, point3d3)
                            percent = float(self.parametersPanel.txtPdg.text())/ 100
                            num4 = z + percent * num3
                            nOTAPPLICABLE = "%.1f"%(Altitude(num4).Feet)
                            if (self.parametersPanel.pnlPosition2.IsValid()):
                                point3d4 = self.parametersPanel.pnlPosition2.Point3d
                                if (MathHelper.smethod_96(MathHelper.calcDistance(point3d3, point3d4))):
                                    nVALIDPOSITION = Validations.INVALID_POSITION
                                    flag1 = False
                                    return (flag1, nVALIDPOSITION)
                                
                                elif (MathHelper.smethod_84(point3d2, point3d3, point3d4, AngleUnits.Radians) > 0.26):
                                    num5 = int(math.trunc(Unit.ConvertMeterToNM(num3)) + 1)
                                    if (num5 > 25):                                    
                                        num5 = 25
                                    
                                    speed = self.speeds[num5]
                                    speed1 = Speed.smethod_0(speed, float(self.parametersPanel.txtIsa.text()), Altitude(num4))
                                    if (percent >= 0):
                                        feet = (Altitude(percent * num3)).Feet
                                        if (feet <= 3000):
                                            num1 = (15 if feet <= 1000 else 20)
                                        
                                        else:
                                            num1 = 25
                                        
                                    else:                                    
                                        num1 = 25
                                    
                                    num6 = 3.14159265358979 * (num1 / 180.0)
                                    num7 = math.sin(num6) / math.cos(num6)
                                    num8 = min([3431 * num7 / (3.14159265358979 * speed1.Knots), 3])
                                    num9 = Unit.ConvertNMToMeter(speed1.Knots / (3.14159265358979 * num8 * 20))
                                    flag2 = MathHelper.smethod_115(point3d4, point3d2, point3d3)
                                    flag3 = flag2
                                    point3d = (MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d2, point3d3) + 1.5707963267949, num9) if not flag2 else MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d2, point3d3) - 1.5707963267949, num9))
                                    if (MathHelper.calcDistance(point3d, point3d4) >= num9):
                                        num10 = MathHelper.calcDistance(point3d, point3d4)
                                        num11 = math.sin(num10 * num10 - num9 * num9)
                                        num12 = math.atan(num9 / num11)
                                        if (not flag3):
                                            point3d1 = MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d) + num12, num11)
                                            flag = MathHelper.smethod_115(point3d1, point3d, point3d3)
                                        
                                        else:
                                            point3d1 = MathHelper.distanceBearingPoint(point3d4, MathHelper.getBearing(point3d4, point3d) - num12, num11)
                                            flag = MathHelper.smethod_115(point3d1, point3d3, point3d)
                                        
                                        num13 = MathHelper.smethod_84(point3d3, point3d, point3d1, AngleUnits.Radians)
                                        num2 = (3.14159265358979 - num13 if not flag else 3.14159265358979 + num13)
                                        num14 = num2 * num9
                                        num = MathHelper.calcDistance(point3d1, point3d4) + num14
                                        altitude = Altitude(num4 + percent * num)
                                        nVALIDPOSITION = "%.1f"%altitude.Feet
                                        flag1 = True
                                        return (flag1, nVALIDPOSITION)
                                    
                                    else:
                                        nVALIDPOSITION = Validations.POSITION_INSIDE_TURN
                                    
                                
                                else:
                                    num = MathHelper.calcDistance(point3d3, point3d4)
                                    altitude1 = Altitude(num4 + percent * num)
                                    nVALIDPOSITION = "%.1f"%altitude1.Feet
                                    flag1 = True
                                    return (flag1, nVALIDPOSITION)
                                
                            
                            else:
                                flag1 = False
                                return (flag1, Validations.INVALID_POSITION)
                            
                         
                        else:
                            nOTAPPLICABLE = Validations.INVALID_POSITION
                            flag1 = False
                            return (flag1, Validations.INVALID_POSITION)
                        
                    else:
                        flag1 = False
                        return (flag1, Validations.INVALID_POSITION)
                
                else:
                    flag1 = False
                    return (flag1, Validations.INVALID_POSITION)            
            
            finally:
                self.parametersPanel.txtAltitude1.setText(nOTAPPLICABLE)
                self.parametersPanel.txtAltitude2.setText(nVALIDPOSITION)
            
            return (False, Validations.INVALID_POSITION)
        
        except ValueError , e: 
            self.parametersPanel.txtAltitude1.setText(e.message)
            self.parametersPanel.txtAltitude2.setText(e.message)
            return (False, Validations.INVALID_POSITION)
        
        return (flag1, "")
    def method_37(self, polyline_0, point3d_0, double_0):
        markResult = []
        if (self.parametersPanel.chbMarkAltitudes.isChecked()):
            metres = Altitude(float(self.parametersPanel.txtAltitudeEvery.text()), AltitudeUnits.FT).Metres;
            if (double_0 < 0):
                metres = metres * -1;
#             Group group = AcadHelper.smethod_20(transaction_0, blockTableRecord_0.get_Database(), "Average Flight Path (altitudes)");
            value = Altitude(float(self.parametersPanel.txtAltitudeEvery.text()), AltitudeUnits.FT)
#             str_0 = str(value.Feet)
            distanceAtParameter = polyline_0.get_Length()#polyline_0.GetDistanceAtParameter(polyline_0.get_EndParam());
            z = point3d_0.get_Z();
            num = math.trunc(z / metres) * metres;
            if (num <= z and double_0 > 0 or num >= z and double_0 < 0):
                num = num + metres;
            j = 1
            i = 0
            i = (math.fabs((num - z) / double_0))
            while i <= distanceAtParameter:
                
                startAndEndPoints = []
                pointAtDist = polyline_0.GetPointAtDist(i, startAndEndPoints);
                point3d1, point3d2 = MathHelper.getVerticalLine(startAndEndPoints, pointAtDist, 50)
#                 altitude = Altitude(num);
                markResult.append(([point3d1, point3d2], str( int(value.Feet * j)) + "ft"))
                
#                 self.method_36(pointAtDist, "- A -", altitude.method_0(str), False);
                num = num + metres;
                i = (math.fabs((num - z) / double_0))
                j += 1
#             return markResult
#             for (double i = Math.Abs((num - z) / double_0); i <= distanceAtParameter; i = Math.Abs((num - z) / double_0))
                
        if (self.parametersPanel.chbMarkDistances.isChecked()):
            metres1 = Distance(float(self.parametersPanel.txtDistanceEvery.text()), DistanceUnits.NM).Metres
#             group1 = AcadHelper.smethod_20(transaction_0, blockTableRecord_0.get_Database(), "Average Flight Path (distances)");
            distance = Distance(float(self.parametersPanel.txtDistanceEvery.text()), DistanceUnits.NM)
            str1 = str(distance.NauticalMiles)#OriginalUnits.ToString().ToLowerInvariant().Trim());
            distanceAtParameter1 = polyline_0.get_Length()#.GetDistanceAtParameter(polyline_0.get_EndParam());
            for k in range(1, int(distanceAtParameter1 / metres1) + 1):
#             for (double j = metres1; j <= distanceAtParameter1; j = j + metres1)
                m = k * metres1
                startAndEndPoints = []
                pointAtDist = polyline_0.GetPointAtDist(m, startAndEndPoints);
                point3d1, point3d2 = MathHelper.getVerticalLine(startAndEndPoints, pointAtDist, 50)
                distance1 = Distance(m);
                markResult.append(([point3d1, point3d2], str( int(distance1.NauticalMiles)) + "nm"))
#                 self.method_36(point3d, "- D -", distance1.method_0(str1), False);
        if (self.parametersPanel.chbMarkSpeeds.isChecked()):
            selectedIndex = float(self.parametersPanel.cmbSpeedEvery.currentIndex() + 1);
#             Group group2 = AcadHelper.smethod_20(transaction_0, blockTableRecord_0.get_Database(), "Average Flight Path (speeds)");
            num1 = polyline_0.get_Length()#.GetDistanceAtParameter(polyline_0.get_EndParam());
            for n in range(1, int(num1 / Unit.ConvertNMToMeter(selectedIndex)) + 1):
                k = n * Unit.ConvertNMToMeter(selectedIndex)
#             for (double k = Units.ConvertNMToMeter(selectedIndex); k <= num1; k = k + Units.ConvertNMToMeter(selectedIndex))
                startAndEndPoints = []
                pointAtDist = polyline_0.GetPointAtDist(k, startAndEndPoints);
                point3d1, point3d2 = MathHelper.getVerticalLine(startAndEndPoints, pointAtDist, 50)
                num2 = math.trunc(Unit.ConvertMeterToNM(k));
                if (num2 > 25):
                    num2 = 25;
                markResult.append(([point3d1, point3d2], str( int(self.speeds[num2].Knots)) + "kts"))
        return markResult
#                 self.method_36(pointAtDist1, "- S -", self.speeds[num2].method_0(":u"), True);
#             }
    def method_39(self, polyline_0, point2d_0, point3d_0, double_0, double_1):
#         double num;
#         Point2d point2d;
#         TurnDirection turnDirection;
#         double num1;
#         Point2d point2d1;
#         Point2d point2d2;
        num = 0.0
        point2d = None
        point2d1 = None
        point2d2 = None
        num1 = 0.0
        turnDirection = None
        
        numberOfVertices = len(polyline_0)
        if (numberOfVertices == 0):
            polyline_0.Add(PolylineAreaPoint(point2d_0));
            return AppendResult.OK
        point2dAt = polyline_0[numberOfVertices - 1].Position;
        if (MathHelper.smethod_100(point2dAt, point2d_0)):
            return AppendResult.Identical
        if (numberOfVertices == 1):
            polyline_0.Add(PolylineAreaPoint(point2d_0));
            return AppendResult.OK
        point2dAt1 = polyline_0[numberOfVertices - 2].Position
        bulgeAt = polyline_0[numberOfVertices - 2].get_Bulge()
        if (not MathHelper.smethod_96(bulgeAt)):
            point2d = MathHelper.smethod_70(point2dAt1, point2dAt, bulgeAt);
            num = MathHelper.smethod_4(MathHelper.getBearing(point2d, point2dAt) + 1.5707963267949) if(MathHelper.smethod_66(bulgeAt) != TurnDirection.Left) else MathHelper.smethod_4(MathHelper.getBearing(point2d, point2dAt) - 1.5707963267949)
        else:
            num = MathHelper.getBearing(point2dAt1, point2dAt);
        turnDirectionList = []
        if (MathHelper.smethod_77(num, MathHelper.getBearing(point2dAt, point2d_0), AngleUnits.Degrees, turnDirectionList) <= 0.26):
            turnDirection = turnDirectionList[0]
            polyline_0.Add(PolylineAreaPoint(point2d_0))
            return AppendResult.OK
        turnDirection = turnDirectionList[0]
        z = point3d_0.get_Z();
        distanceAtParameter = polyline_0.get_Length()#polyline_0.GetDistanceAtParameter(polyline_0.get_EndParam());
        num2 = math.trunc(Unit.ConvertMeterToNM(distanceAtParameter)) + 1;
        if (num2 > 25):
            num2 = 25;
        speed = self.speeds[num2];
        altitude = Altitude(double_0 * distanceAtParameter + z);
        if (double_0 >= 0):
            feet = (Altitude(double_0 * distanceAtParameter)).Feet;
            if (feet <= 3000):
                num1 = 15 if(feet <= 1000) else 20
            else:
                num1 = 25;
        else:
            num1 = 25;
        speed1 = Speed.smethod_0(speed, double_1, altitude);
        if speed1 == None:
            return "Tas's value is not valid."
        metres = Distance.smethod_0(speed1, num1).Metres;
        point2d1 = MathHelper.distanceBearingPoint(point2dAt, num + 1.5707963267949, metres) if(turnDirection != TurnDirection.Left) else MathHelper.distanceBearingPoint(point2dAt, num - 1.5707963267949, metres)
        if (MathHelper.calcDistance(point2d1, point2d_0) < metres):
            return AppendResult.InsideTurn
        num3 = math.acos(metres / MathHelper.calcDistance(point2d1, point2d_0));
        point2d2 = MathHelper.distanceBearingPoint(point2d1, MathHelper.getBearing(point2d1, point2d_0) - num3, metres) if(turnDirection != TurnDirection.Left) else MathHelper.distanceBearingPoint(point2d1, MathHelper.getBearing(point2d1, point2d_0) + num3, metres)
        polyline_0[numberOfVertices - 1].set_Bulge(MathHelper.smethod_57(turnDirection, point2dAt, point2d2, point2d1));
        polyline_0.Add(PolylineAreaPoint(point2d2));
        if (not MathHelper.smethod_103(point2d2, point2d_0, 0.0001)):
            polyline_0.Add(PolylineAreaPoint(point2d_0));
        return AppendResult.OK
    
    def mniEdit_Click(self):
        selectedIndexes = self.parametersPanel.tblSpeeds.selectedIndexes()
        if len(selectedIndexes) > 0 :
            trees, dlgResult = QInputDialog.getInt(self, "Nominal Speed(s)", "Speed (kts):")
            if dlgResult:                
                for index in selectedIndexes:
                    if index.column() == 1:
                        self.tblModel.setData(index, QVariant(trees), Qt.EditRole)
                        self.speeds.pop(index.row())
                        self.speeds.insert(index.row(), Speed(trees))
                        self.parametersPanel.tblSpeeds.setModel(self.tblModel)
                        return
                    
    def mniReset_Click(self):
        self.method_28()
        self.method_29()
        self.method_30()
        self.method_31()
    def btnMultiple_Click(self):
        self.mouseMove = True
        
        define._canvas.setMapTool(self.CaptureCoordTool)
        
        percent = float(self.parametersPanel.txtPdg.text())/ 100;
        value = float(self.parametersPanel.txtIsa.text())
        if not self.multipointFlag:
            if len(self.polyline) != 0:
                self.polyline = PolylineArea()
                
                self.method_39(self.polyline, self.parametersPanel.pnlDer.Point3d.smethod_176(), self.parametersPanel.pnlDer.Point3d, percent, value);
                self.multipointFlag = True
        if len(self.polyline) == 0:
            self.method_39(self.polyline, self.parametersPanel.pnlDer.Point3d.smethod_176(), self.parametersPanel.pnlDer.Point3d, percent, value);
            self.multipointFlag = True
#             self.multiplePoint3d.append(self.parametersPanel.pnlDer.Point3d)
    def resultPointValueListMethod(self, resultValueList):
        if not self.parametersPanel.pnlDer.IsValid():
            QMessageBox.warning(self, "Warning", "DER Position is not valid.")
            return
#         if len(self.multiplePoint3d) == 0:
#             self.multiplePoint3d.append(self.parametersPanel.pnlDer.Point3d)
        itemList = []
        if len(resultValueList) > 0:
            point3d = Point3D(float(resultValueList[1]), float(resultValueList[2]))
            percent = float(self.parametersPanel.txtPdg.text())/ 100;
            value = float(self.parametersPanel.txtIsa.text())
            appendResult = self.method_39(self.polyline, point3d.smethod_176(), self.parametersPanel.pnlDer.Point3d, percent, value);
            define._messageLabel.setText(appendResult)
            if (appendResult == AppendResult.Identical):
                define._messageLabel.setText(appendResult)
            elif (appendResult != AppendResult.InsideTurn):
                mapUnits = define._canvas.mapUnits()
                if self.constructionLayer == None:
                    self.constructionLayer = AcadHelper.createVectorLayer(self.surfaceType, QGis.Line)
#                     if define._mapCrs == None:
#                         if mapUnits == QGis.Meters:
#                             self.constructionLayer = QgsVectorLayer("linestring?crs=EPSG:32633", self.surfaceType , "memory")
#                         else:
#                             self.constructionLayer = QgsVectorLayer("linestring?crs=EPSG:4326", self.surfaceType , "memory")
#                     else:
#                         self.constructionLayer = QgsVectorLayer("linestring?crs=%s"%define._mapCrs.authid (), self.surfaceType, "memory")
# #
# #
#                     self.constructionLayer.startEditing()
#                     pr = self.constructionLayer.dataProvider()
#                     pr.addAttributes([QgsField("Caption", QVariant.String)])
#                     feature = QgsFeature()
                    AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, self.polyline)
#                     feature.setGeometry(QgsGeometry.fromPolyline(self.polyline.method_14()))
# #                     feature.setAttributes([""])
#                     self.constructionLayer.addFeature(feature)
#
#                     self.constructionLayer.commitChanges()
                    QgisHelper.appendToCanvas(define._canvas, [self.constructionLayer], SurfaceTypes.DepartureNominal)
#                     QgisHelper.zoomToLayers([self.constructionLayer])
                    self.multiPolylineCount += 1
                    self.startMulti = True
                    iter = self.constructionLayer.getFeatures()
                    self.featMultiEnd = None
                    for feat in iter:
                        self.featMultiEnd = feat
                    palSetting = QgsPalLayerSettings()
                    palSetting.readFromLayer(self.constructionLayer)
                    palSetting.enabled = True
                    palSetting.fieldName = "Caption"
                    palSetting.isExpression = True
                    palSetting.placement = QgsPalLayerSettings.Line
                    palSetting.placementFlags = QgsPalLayerSettings.AboveLine
                    palSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '8', "")
                    palSetting.writeToLayer(self.constructionLayer)
                else:
                    
                    self.constructionLayer.startEditing()
                    if self.featMultiEnd != None:
                        self.constructionLayer.deleteFeature(self.featMultiEnd.id())
                    self.constructionLayer.commitChanges()
                    AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, self.polyline)
                    # feature = QgsFeature()
                    # feature.setGeometry(QgsGeometry.fromPolyline(self.polyline.method_14()))
                    # feature.setAttributes([""])
                    # self.constructionLayer.addFeature(feature)
                    #
                    # self.constructionLayer.commitChanges()
                    iter = self.constructionLayer.getFeatures()
                    self.featMultiEnd = None
                    id = None
                    for feat in iter:
                        self.featMultiEnd = feat
                        id = feat.id()
                        
                
                    self.constructionLayer.triggerRepaint()
                    
                    self.multiPolylineCount += 1
                    
                self.constructionLayer.startEditing()
                if len(self.markMultiFeatIds) > 0:
                    for i in self.markMultiFeatIds:
                        self.constructionLayer.deleteFeature(i)
                self.constructionLayer.commitChanges()
                markResult = self.method_37(PolylineArea(self.polyline.method_14()), self.parametersPanel.pnlDer.Point3d, percent)
                self.markMultiFeatIds = []   
                for pointList, caption in  markResult:
                    AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, pointList, False, {"Caption":caption})
                    # self.constructionLayer.startEditing()
                    # feature = QgsFeature()
                    # feature.setGeometry(QgsGeometry.fromPolyline(pointList))
                    # feature.setAttributes([caption])
                    # self.constructionLayer.addFeature(feature)
                    # featId = None
                    # self.constructionLayer.commitChanges()
                    iter = self.constructionLayer.getFeatures()
                    
                    for feat in iter:
                        featId = feat.id()
                    self.markMultiFeatIds.append(featId)
                
                self.constructionLayer.triggerRepaint()
            else:
                define._messageLabel.setText(Messages.POSITION_INSIDE_TURN)
    def nominal2Layer(self):
        resultLayer = AcadHelper.createVectorLayer("NominalTrack", QGis.Line)
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer,[self.parametersPanel.pnlPosition1.Point3d, self.parametersPanel.pnlPosition2.Point3d])

        return resultLayer
class AppendResult:   
    OK = "OK"
    InsideTurn = "InsideTurn"
    Identical = "Identical"
    
class tableModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.itemsList = []
        self.dirty = False
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
            not (0 <= index.row() < len(self.itemsList)):
            return QVariant()
        dist, speed = self.itemsList[index.row()]         
        column = index.column()
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant("%i nm"%dist)
            elif column == 1:
                return QVariant("%i kts"%speed)
            
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
        elif (role == Qt.EditRole):
            if column == 0:
                return QVariant(dist)
            elif column == 1:
                return QVariant(speed)            
        return QVariant()
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.itemsList):
            item = self.itemsList[index.row()]
            column = index.column()
            if column == 0:
                val, ok= value.toInt()
                self.itemsList.pop(index.row())
                self.itemsList.insert(index.row(), (val, item[1]))
            elif column == 1:
                val, ok = value.toInt()
                self.itemsList.pop(index.row())
                self.itemsList.insert(index.row(), (item[0], val))
                
            self.dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
            return True
        return False
    def Add(self, rnpArLeg):
        self.beginInsertRows(QModelIndex(), self.RowCount, self.RowCount)
        self.itemsList.append(rnpArLeg)
        self.endInsertRows()
        self.dirty = True
        return True
    
    def get_rowCount(self):
        return len(self.itemsList)
    RowCount = property(get_rowCount, None, None, None)
    
    def get_columnCount(self):
        return 2
    ColumnCount = property(get_columnCount, None, None, None)
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == 0:
                return QVariant("Distance")
            elif section == 1:
                return QVariant("IAS")
    def rowCount(self, index=QModelIndex()):
        return len(self.itemsList)
    
    def columnCount(self, index=QModelIndex()):
        return 2
    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position,
                             position + rows - 1)
        for row in range(rows):
            self.itemsList.insert(position + row, (0,0))
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position,
                             position + rows - 1)
        self.itemsList = self.itemsList[:position] + \
                        self.itemsList[position + rows:]
        self.endRemoveRows()
        self.dirty = True
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)|
                            Qt.ItemIsEditable)
        return True
    