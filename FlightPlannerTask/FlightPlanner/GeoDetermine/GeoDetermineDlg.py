# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QString,QSize, Qt, QDate
from PyQt4.QtGui import QIcon, QPixmap, QMessageBox, QStandardItemModel, QStandardItem,QSizePolicy,QFont, QFileDialog, \
    QLabel, QSpinBox, QFrame, QHBoxLayout, QDateEdit, QCalendarWidget, QMenu, QVBoxLayout
from qgis.core import QgsVectorFileWriter, QgsMapLayerRegistry,QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2
from qgis.gui import QgsEllipseSymbolLayerV2Widget
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import SurfaceTypes, DistanceUnits, MagneticModel
from FlightPlanner.GeoDetermine.ui_GeoDetermine import Ui_GeoDetermine
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.Panels.DegreesBoxPanel import DegreesBoxPanel
from FlightPlanner.Dialogs.DlgMagneticVariationParameters import DlgMagneticVariationParameters
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.QgisHelper import QgisHelper, Geo
from FlightPlanner.types import Point3D
from FlightPlanner.Captions import Captions
from FlightPlanner.messages import Messages
from Type.Degrees import Degrees, DegreesType
from Type.String import String
import define

class GeoDetermineDlg(FlightPlanBaseDlg):
    HistoryDataP = []
    HistoryDataBD = []
    HistoryDataMV = []
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("HoldingRnavDlg")
        self.surfaceType = SurfaceTypes.GeoDetermine
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.GeoDetermine)
        self.resize(540, 550)
        self.surfaceList = None

        self.date = QDate.currentDate()
        self.model = MagneticModel.WMM2010
        geo = Geo()

        self.resultLayerList = []
        self.resultPoint3d = None

        self.resultLat = None
        self.resultLon = None

    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.btnExportResult.setVisible(False)
        self.ui.btnEvaluate.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(1)

        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/Calculator.bmp")), QIcon.Normal, QIcon.Off)
        self.ui.btnConstruct.setIcon(icon)
        self.ui.btnConstruct.setToolTip("Calculate")

        return FlightPlanBaseDlg.uiStateInit(self)
    def tblHistory_Click(self, modelIndex):
        if modelIndex != None:
            if self.parametersPanel.tabGeneral.currentIndex() == 0:
                dataList = GeoDetermineDlg.HistoryDataP[modelIndex.row()]

                self.parametersPanel.pnlStartPosP.Point3d = Point3D(float(dataList[1][1]), float(dataList[1][0]))
                self.parametersPanel.pnlVarStartP.Value = float(dataList[1][2])
                self.parametersPanel.txtForwardTP.Value = float(dataList[1][3])
                self.parametersPanel.txtForwardMP.Value = float(dataList[1][4])
                self.parametersPanel.txtDistanceP.Value = Distance(float(dataList[1][5]), DistanceUnits.NM)
                self.parametersPanel.pnlVarFinishP.Value = float(dataList[1][9])

                self.method_29_P();
                self.resultModelP.setItem(0, 0, QStandardItem(Captions.LATITUDE))
                self.resultModelP.setItem(0, 1, QStandardItem(dataList[1][7]))

                self.resultModelP.setItem(1, 0, QStandardItem(Captions.LONGITUDE))
                self.resultModelP.setItem(1, 1, QStandardItem(dataList[1][8]))

                self.resultModelP.setItem(2, 0, QStandardItem(Captions.REVERSE_TRUE_BEARING))
                self.resultModelP.setItem(2, 1, QStandardItem(dataList[1][10]))

                self.resultModelP.setItem(3, 0, QStandardItem(Captions.REVERSE_MAGNETIC_BEARING))
                self.resultModelP.setItem(3, 1, QStandardItem(dataList[1][11]))
            elif self.parametersPanel.tabGeneral.currentIndex() == 1:
                dataList = GeoDetermineDlg.HistoryDataBD[modelIndex.row()]

                self.parametersPanel.pnlStartPosBD.ID = dataList[1][0]
                self.parametersPanel.pnlStartPosBD.Point3d = Point3D(float(dataList[1][2]), float(dataList[1][1]))
                self.parametersPanel.pnlVarStartBD.Value = float(dataList[1][3])
                self.parametersPanel.pnlFinishPosBD.ID = dataList[1][4]
                self.parametersPanel.pnlFinishPosBD.Point3d = Point3D(float(dataList[1][6]), float(dataList[1][5]))
                self.parametersPanel.pnlVarFinishBD.Value = float(dataList[1][7])

                self.method_31_BD();
                self.resultModelBD.setItem(0, 0, QStandardItem(Captions.FORWARD_TRUE_BEARING))
                self.resultModelBD.setItem(0, 1, QStandardItem(dataList[1][8]))

                self.resultModelBD.setItem(1, 0, QStandardItem(Captions.FORWARD_MAGNETIC_BEARING))
                self.resultModelBD.setItem(1, 1, QStandardItem(dataList[1][9]))

                self.resultModelBD.setItem(2, 0, QStandardItem(Captions.REVERSE_TRUE_BEARING))
                self.resultModelBD.setItem(2, 1, QStandardItem(dataList[1][10]))

                self.resultModelBD.setItem(3, 0, QStandardItem(Captions.REVERSE_MAGNETIC_BEARING))
                self.resultModelBD.setItem(3, 1, QStandardItem(dataList[1][11]))

                self.resultModelBD.setItem(2, 0, QStandardItem(Captions.DISTANCE_BETWEEN_POSITIONS))
                self.resultModelBD.setItem(2, 1, QStandardItem(dataList[1][12]))

                self.resultModelBD.setItem(3, 0, QStandardItem(Captions.DISTANCE_BETWEEN_POSITIONS))
                self.resultModelBD.setItem(3, 1, QStandardItem(dataList[1][13]))
            else:
                dataList = GeoDetermineDlg.HistoryDataMV[modelIndex.row()]

                self.parametersPanel.pnlPositionMVD.Point3d = Point3D(float(dataList[1][1]), float(dataList[1][0]))
                self.parametersPanel.pnlPositionMVD.txtAltitudeM.setText(dataList[1][2])
                self.parametersPanel.txtResult.Value = dataList[1][6]

    def calculateP(self):
        degree = None;
        degree1 = None;
        degree2 = None;
        degree3 = None;
        num = None;
        result, degree, degree1 = self.parametersPanel.pnlStartPosP.method_3()
        if (result):
            # self.pnlVarStart.Value.smethod_17();
            num1 = float(self.parametersPanel.pnlVarFinishP.Value);
            value = float(self.parametersPanel.txtForwardTP.Value);
            value1 = float(self.parametersPanel.txtForwardTP.Value);
            distance = self.parametersPanel.txtDistanceP.Value;
            result, degree2, degree3, num = Geo.smethod_6(self.parametersPanel.cmbCalculationTypeP.SelectedItem, degree, degree1, value, distance)
            if (result):
                num2 = MathHelper.smethod_3(num - num1);
                self.method_29_P();
                self.resultPoint3d = Point3D(degree3, degree2)

                self.resultLat = degree2
                self.resultLon = degree3

                latStr = Degrees(degree2, None, None, DegreesType.Latitude).ToString()

                self.resultModelP.setItem(0, 0, QStandardItem(Captions.LATITUDE))
                self.resultModelP.setItem(0, 1, QStandardItem(latStr))

                lonStr = Degrees(degree3, None, None, DegreesType.Longitude).ToString()
                if String.Str2QString(lonStr).mid(0, 1) == "0":
                    lonStr = String.Str2QString(lonStr).mid(1, String.Str2QString(lonStr).length() - 1)


                self.resultModelP.setItem(1, 0, QStandardItem(Captions.LONGITUDE))
                self.resultModelP.setItem(1, 1, QStandardItem(lonStr))

                self.resultModelP.setItem(2, 0, QStandardItem(Captions.REVERSE_TRUE_BEARING))
                self.resultModelP.setItem(2, 1, QStandardItem(str(round(num, 4))))

                self.resultModelP.setItem(3, 0, QStandardItem(Captions.REVERSE_MAGNETIC_BEARING))
                self.resultModelP.setItem(3, 1, QStandardItem(str(round(num2, 4))))

                dataList = []
                dataList.append(["Latitude (Start)",
                                 "Longitude (Start)",
                                 "Variation (Start)",
                                 "Forward (° T)",
                                 "Forward (° M)",
                                 "Distance (nm)",
                                 "Distance (km)",
                                 "Latitude (Finish)",
                                 "Longitude (Finish)",
                                 "Variation (Finish)",
                                 "Reverse (° T)",
                                 "Reverse (° M)"])
                dataList.append([str(degree),
                                 str(degree1),
                                 str(self.parametersPanel.pnlVarStartP.Value),
                                 str(self.parametersPanel.txtForwardTP.Value),
                                 str(self.parametersPanel.txtForwardMP.Value),
                                 str(distance.NauticalMiles),
                                 str(distance.Kilometres),
                                 str(degree2),
                                 str(degree3),
                                 str(self.parametersPanel.pnlVarFinishP.Value),
                                 str(round(num, 4)),
                                 str(round(num2, 4))])
                GeoDetermineDlg.HistoryDataP.append(dataList)
                self.setDataInHistoryModel(dataList)
                self.method_28_P(degree2, degree3)
    def calculateBD(self):
        degree = None;
        degree1 = None;
        degree2 = None;
        degree3 = None;
        num = None;
        result, degree, degree1 = self.parametersPanel.pnlStartPosBD.method_3()
        if (result):
            num2 = self.parametersPanel.pnlVarStartBD.Value;
            result1, degree2, degree3 = self.parametersPanel.pnlFinishPosBD.method_3()
            if (result1):
                num3 = self.parametersPanel.pnlVarFinishBD.Value;
                result2, distance, num, num1 = Geo.smethod_4(self.parametersPanel.cmbCalculationTypeBD.SelectedItem, degree, degree1, degree2, degree3)
                if define._units == QGis.Meters:
                    QgisHelper.convertMeasureUnits(QGis.Degrees)
                    distance = Distance(MathHelper.calcDistance(self.parametersPanel.pnlStartPosBD.Point3d, self.parametersPanel.pnlFinishPosBD.Point3d))
                    QgisHelper.convertMeasureUnits(QGis.Meters)
                else:
                    distance = Distance(MathHelper.calcDistance(self.parametersPanel.pnlStartPosBD.Point3d, self.parametersPanel.pnlFinishPosBD.Point3d))
                if result2:
                    num4 = MathHelper.smethod_3(num - num2);
                    num5 = MathHelper.smethod_3(num1 - num3);
                    self.method_31_BD()

                    self.resultModelBD.setItem(0, 0, QStandardItem(Captions.FORWARD_TRUE_BEARING))
                    self.resultModelBD.setItem(0, 1, QStandardItem(str(round(num, 4))))

                    self.resultModelBD.setItem(1, 0, QStandardItem(Captions.FORWARD_MAGNETIC_BEARING))
                    self.resultModelBD.setItem(1, 1, QStandardItem(str(round(num4, 4))))

                    self.resultModelBD.setItem(2, 0, QStandardItem(Captions.REVERSE_TRUE_BEARING))
                    self.resultModelBD.setItem(2, 1, QStandardItem(str(round(num1, 4))))

                    self.resultModelBD.setItem(3, 0, QStandardItem(Captions.REVERSE_MAGNETIC_BEARING))
                    self.resultModelBD.setItem(3, 1, QStandardItem(str(round(num5, 4))))

                    self.resultModelBD.setItem(4, 0, QStandardItem(Captions.DISTANCE_BETWEEN_POSITIONS))
                    self.resultModelBD.setItem(4, 1, QStandardItem(str(round(distance.NauticalMiles, 4)) + " nm"))

                    self.resultModelBD.setItem(5, 0, QStandardItem(Captions.DISTANCE_BETWEEN_POSITIONS))
                    self.resultModelBD.setItem(5, 1, QStandardItem(str(round(distance.Kilometres, 4)) + " km"))

                    dataList = []
                    dataList.append(["ID (Start)",
                                     "Latitude (Start)",
                                     "Longitude (Start)",
                                     "Variation (Start)",
                                     "ID (Finish)",
                                     "Latitude (Finish)",
                                     "Longitude (Finish)",
                                     "Variation (Finish)",
                                     "Forward (° T)",
                                     "Forward (° M)",
                                     "Reverse (° T)",
                                     "Reverse (° M)",
                                     "Distance (nm)",
                                     "Distance (km)"])
                    dataList.append([self.parametersPanel.pnlStartPosBD.ID,
                                     str(degree),
                                     str(degree1),
                                     str(self.parametersPanel.pnlVarStartBD.Value),
                                     self.parametersPanel.pnlFinishPosBD.ID,
                                     str(degree2),
                                     str(degree3),
                                     str(self.parametersPanel.pnlVarFinishBD.Value),
                                     str(num),
                                     str(num4),
                                     str(round(num, 4)),
                                     str(round(num2, 4)),
                                     str(distance.NauticalMiles),
                                     str(distance.Kilometres)])
                    GeoDetermineDlg.HistoryDataBD.append(dataList)
                    self.setDataInHistoryModel(dataList)
                    self.method_28_BD()

    def calculateMVD(self):
        degree = None;
        degree1 = None;
        degree2 = None;
        
        result, degree, degree1 = self.parametersPanel.pnlPositionMVD.method_3();
        # position.method_1(out degree, out degree1);
        altitude = self.parametersPanel.pnlPositionMVD.Altitude();
        result, degree2 = Geo.smethod_7(degree, degree1, altitude, self.parametersPanel.cmbModel.SelectedIndex, self.parametersPanel.dtpDate.date())
        if (result):
            self.parametersPanel.txtResult.Value = str(round(degree2, 4))#.method_1(Formats.VariationFormat);
            date = self.parametersPanel.dtpDate.date()
            dataList = []
            dataList.append(["Latitude",
                             "Longitude",
                             "Altitude  (m)",
                             "Altitude (ft)",
                             "Date",
                             "Magnetic Model",
                             "Magnetic Variation"])
            dataList.append([str(degree),
                             str(degree1),
                             str(altitude.Metres),
                             str(altitude.Feet),
                             date.toString(),
                             self.parametersPanel.cmbModel.SelectedItem,
                             self.parametersPanel.txtResult.Value])
            GeoDetermineDlg.HistoryDataMV.append(dataList)
            self.setDataInHistoryModel(dataList)
    def autoCalcFinishMagVar(self):
        try:
            if self.parametersPanel.chbAutoFinishMagVar.Checked:
                finishPt = None;
                finishLat = None;
                finishLon = None;
                degree3 = None;
                num = None;
                result, degree, degree1 = self.parametersPanel.pnlStartPosP.method_3()
                if (result):
                    value = float(self.parametersPanel.txtForwardTP.Value);
                    value1 = float(self.parametersPanel.txtForwardTP.Value);
                    distance = self.parametersPanel.txtDistanceP.Value;
                    result1, degree2, degree3, num = Geo.smethod_6(self.parametersPanel.cmbCalculationTypeP.SelectedItem, degree, degree1, value, distance)
                    if (result1):
                        finishPt = Point3D(degree3, degree2)

                        finishLat = degree2
                        finishLon = degree3
                if finishPt != None and self.model != None and self.date != None:
                    # result, degree, degree1 = self.parametersPanel.pnlStartPosP.method_3();
                    result2, degree2 = Geo.smethod_7(finishLat, finishLon, Altitude(0), self.model, self.date)
                    if (result2):
                        degree2 = round(degree2, 2);
                        self.parametersPanel.pnlVarFinishP.Value = degree2
        except:
            pass
    def btnConstruct_Click(self):
        # flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        # if not flag:
        #     return
        if self.parametersPanel.tabGeneral.currentIndex() == 0:
            self.autoCalcFinishMagVar()
            self.calculateP()

        elif self.parametersPanel.tabGeneral.currentIndex() == 1:
            self.calculateBD()
        else:
            self.calculateMVD()
        
    def initParametersPan(self):
        ui = Ui_GeoDetermine()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)
        

        self.parametersPanel.pnlStartPosP = PositionPanel(self.parametersPanel.gbStartPosP, None, None, "Degree")
        # self.parametersPanel.pnlStartPosP.degreeFormat = "ddmmss.ssssH"
        self.parametersPanel.pnlStartPosP.alwwaysShowString = "Degree"
#         self.parametersPanel.pnlWaypoint.groupBox.setTitle("FAWP")
        self.parametersPanel.pnlStartPosP.btnCalculater.hide()
        self.parametersPanel.pnlStartPosP.hideframe_Altitude()
        # self.parametersPanel.pnlStartPosP.showframe_ID()
        self.parametersPanel.pnlStartPosP.setObjectName("pnlStartPosP")
        self.connect(self.parametersPanel.pnlStartPosP, SIGNAL("positionChanged"), self.autoCalcFinishMagVar)

        ui.verticalLayout_gbStartPosP.addWidget(self.parametersPanel.pnlStartPosP)


        self.parametersPanel.pnlVarStartP = DegreesBoxPanel(self)
        self.parametersPanel.pnlVarStartP.CaptionLabel = "Magnetic Variation"
        self.connect(self.parametersPanel.pnlVarStartP, SIGNAL("btnDegreeBoxPanel_clicked"), self.method_32_P)
        self.connect(self.parametersPanel.pnlVarStartP, SIGNAL("txtDegreeBox_textChanged"), self.txtDegreeBox_textChangedP)
        ui.verticalLayout_gbStartPosP.addWidget(self.parametersPanel.pnlVarStartP)


        self.parametersPanel.pnlVarFinishP = DegreesBoxPanel(self)
        self.parametersPanel.pnlVarFinishP.ButtonVisible = False
        self.parametersPanel.pnlVarFinishP.Enabled = False
        self.parametersPanel.pnlVarFinishP.CaptionLabel = "Magnetic Variation at Finish"
        ui.vLayout_grbParametersP.insertWidget(1, self.parametersPanel.pnlVarFinishP)
        # self.connect(self.parametersPanel.pnlVarStartP, SIGNAL("btnDegreeBoxPanel_clicked"), self.method_32_P)

        self.parametersPanel.pnlStartPosBD = PositionPanel(self.parametersPanel.gbFinishPosBD, None, None, "Degree")
#         self.parametersPanel.pnlStartPosBD.groupBox.setTitle("FAWP")
#         self.parametersPanel.pnlStartPosBD.degreeFormat = "ddmmss.ssssH"
        self.parametersPanel.pnlStartPosBD.alwwaysShowString = "Degree"
        self.parametersPanel.pnlStartPosBD.btnCalculater.hide()
        self.parametersPanel.pnlStartPosBD.hideframe_Altitude()
        self.parametersPanel.pnlStartPosBD.showframe_ID()
        self.parametersPanel.pnlStartPosBD.setObjectName("pnlStartPosBD")
        ui.verticalLayout_gbStartPosBD.insertWidget(0, self.parametersPanel.pnlStartPosBD)
        self.connect(self.parametersPanel.pnlStartPosBD, SIGNAL("positionChanged"), self.positionChangedStartBD)

        self.parametersPanel.pnlVarStartBD = DegreesBoxPanel(self)
        self.parametersPanel.pnlVarStartBD.CaptionLabel = "Magnetic Variation"
        # self.parametersPanel.pnlVarStartBD.Enabled = False
        self.connect(self.parametersPanel.pnlVarStartBD, SIGNAL("btnDegreeBoxPanel_clicked"), self.method_34_BD)
        # self.connect(self.parametersPanel.pnlVarStartBD, SIGNAL("txtDegreeBox_textChanged"), self.txtDegreeBox_textChangedP)
        ui.verticalLayout_gbStartPosBD.addWidget(self.parametersPanel.pnlVarStartBD)



        self.parametersPanel.pnlFinishPosBD = PositionPanel(self.parametersPanel.gbFinishPosBD, None, None, "Degree")
#         self.parametersPanel.pnlStartPosBD.groupBox.setTitle("FAWP")
#         self.parametersPanel.pnlFinishPosBD.degreeFormat = "ddmmss.ssssH"
        self.parametersPanel.pnlFinishPosBD.alwwaysShowString = "Degree"
        self.parametersPanel.pnlFinishPosBD.btnCalculater.hide()
        self.parametersPanel.pnlFinishPosBD.hideframe_Altitude()
        self.parametersPanel.pnlFinishPosBD.showframe_ID()
        self.parametersPanel.pnlFinishPosBD.setObjectName("pnlFinishPosBD")
        ui.verticalLayout_gbFinishPosBD.insertWidget(0, self.parametersPanel.pnlFinishPosBD)
        self.connect(self.parametersPanel.pnlFinishPosBD, SIGNAL("positionChanged"), self.positionChangedFinishBD)

        self.parametersPanel.pnlVarFinishBD = DegreesBoxPanel(self)
        self.parametersPanel.pnlVarFinishBD.CaptionLabel = "Magnetic Variation"
        # self.parametersPanel.pnlVarFinishBD.Enabled = False
        self.connect(self.parametersPanel.pnlVarFinishBD, SIGNAL("btnDegreeBoxPanel_clicked"), self.method_36_BD)
        # self.connect(self.parametersPanel.pnlVarFinishBD, SIGNAL("txtDegreeBox_textChanged"), self.txtDegreeBox_textChangedP)
        ui.verticalLayout_gbFinishPosBD.addWidget(self.parametersPanel.pnlVarFinishBD)

        self.parametersPanel.pnlPositionMVD = PositionPanel(self.parametersPanel.tabGeoDetermineMV, None, None, "Degree")
        self.parametersPanel.pnlPositionMVD.groupBox.setTitle("Position")
        self.parametersPanel.pnlPositionMVD.alwwaysShowString = "Degree"
        self.parametersPanel.pnlPositionMVD.btnCalculater.hide()
        self.parametersPanel.pnlPositionMVD.setObjectName("pnlPositionMVD")
        ui.verticalLayout_3.insertWidget(0, self.parametersPanel.pnlPositionMVD)
        self.connect(self.parametersPanel.pnlPositionMVD, SIGNAL("positionChanged"), self.method_28_MVD)

        self.connect(self.parametersPanel.txtForwardTP, SIGNAL("Event_0"), self.txtForwardTP_textChanged)
        self.connect(self.parametersPanel.chbAutoFinishMagVar, SIGNAL("Event_0"), self.chbAutoFinishMagVar_clicked)
        self.connect(self.parametersPanel.txtDistanceP, SIGNAL("Event_0"), self.autoCalcFinishMagVar)

        self.connect(self.parametersPanel.txtForwardMP, SIGNAL("Event_0"), self.txtForwardMP_textChanged)
        self.parametersPanel.btnResultP.clicked.connect(self.btnResultP_clicked)
        self.parametersPanel.tabGeneral.currentChanged.connect(self.tabGeneral_CurrentChanged)
        self.parametersPanel.chbAutoVarBD.clicked.connect(self.chbAutoVarBD_clicked)
        self.parametersPanel.dtpDate.dateChanged.connect(self.method_28_MVD)
        self.connect(self.parametersPanel.cmbModel, SIGNAL("Event_0"), self.method_28_MVD)
        self.parametersPanel.btnDtpDate.clicked.connect(self.btnDtpDate_clicked)

        self.resultModelP = QStandardItemModel()
        self.parametersPanel.tblResultP.setModel(self.resultModelP)

        self.resultModelBD = QStandardItemModel()
        self.parametersPanel.tblResultBD.setModel(self.resultModelBD)

        self.ttt = 0
        self.txtForwardTP_textChanged()

        self.setHistoryData()

        self.autoVarSet = False;
        self.dateBD = QDate.currentDate()
        self.modelBD = MagneticModel.WMM2010;
        self.parametersPanel.btnResultBD.setVisible(False)

        self.parametersPanel.dtpDate.setDate(QDate.currentDate())

        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.calendar_clicked)

        self.menu = QMenu()
        layout = QVBoxLayout(self.menu)
        layout.addWidget(self.calendar)
    def chbAutoFinishMagVar_clicked(self):
        if self.parametersPanel.chbAutoFinishMagVar.Checked:
            self.parametersPanel.pnlVarFinishP.Enabled = False
        else:
            self.parametersPanel.pnlVarFinishP.Enabled = True
    def calendar_clicked(self, date):
        self.parametersPanel.dtpDate.setDate(date)
    def btnDtpDate_clicked(self):
        rcRect = self.parametersPanel.btnDtpDate.geometry()
        ptPoint = rcRect.bottomLeft()
        self.menu.exec_( self.mapToGlobal(ptPoint) )
    def positionChangedStartBD(self):
        if (self.parametersPanel.chbAutoVarBD.isChecked() and self.autoVarSet):
            self.method_29_BD();
        self.method_31_BD()
    def positionChangedFinishBD(self):
        if (self.parametersPanel.chbAutoVarBD.isChecked() and self.autoVarSet):
            self.method_30_BD();
        self.method_31_BD()
    def chbAutoVarBD_clicked(self):
        if (self.parametersPanel.chbAutoVarBD.isChecked() and not self.autoVarSet):
            result, self.dateBD, self.modelBD = DlgMagneticVariationParameters.smethod_0(self.dateBD, self.modelBD);
            self.parametersPanel.chbAutoVarBD.setChecked(result)
            self.autoVarSet = self.parametersPanel.chbAutoVarBD.isChecked();
        if (self.parametersPanel.chbAutoVarBD.isChecked()):
            self.method_29_BD();
            self.method_30_BD();
        self.method_31_BD()
    def tabGeneral_CurrentChanged(self):
        if self.parametersPanel.tabGeneral.currentIndex() == 0:
            self.stdItemModelHistory.clear()
            if len(GeoDetermineDlg.HistoryDataP) > 0:
                self.setDataInHistoryModel(GeoDetermineDlg.HistoryDataP, True)
                pass
        elif self.parametersPanel.tabGeneral.currentIndex() == 1:
            self.stdItemModelHistory.clear()
            if len(GeoDetermineDlg.HistoryDataBD) > 0:
                self.setDataInHistoryModel(GeoDetermineDlg.HistoryDataBD, True)
                pass
        else:
            self.stdItemModelHistory.clear()
            if len(GeoDetermineDlg.HistoryDataMV) > 0:
                self.setDataInHistoryModel(GeoDetermineDlg.HistoryDataMV, True)
                pass
    def setHistoryData(self):
        if len(self.HistoryDataP) > 0:
            self.setDataInHistoryModel(GeoDetermineDlg.HistoryDataP, True)
            pass
    def btnResultP_clicked(self):
        self.resultModelP.clear()
        self.parametersPanel.pnlVarStartP.Value = self.parametersPanel.pnlVarFinishP.Value
        self.parametersPanel.pnlVarFinishP.Value = 0.0
        self.parametersPanel.pnlStartPosP.Point3d = self.resultPoint3d

    def txtForwardTP_textChanged(self):
        if self.ttt==0:
            self.ttt=1;
        if self.ttt==2:
            self.ttt=0;
        if self.ttt==1:
            try:
                value = float(self.parametersPanel.txtForwardTP.Value);
                self.parametersPanel.txtForwardMP.Value = MathHelper.smethod_3(value - float(self.parametersPanel.pnlVarStartP.Value))
                self.autoCalcFinishMagVar()
            except:
                self.parametersPanel.txtForwardMP.Value = 0.0
    def txtForwardMP_textChanged(self):
        if self.ttt==0:
            self.ttt=2;
        if self.ttt==1:
            self.ttt=0;
        if self.ttt==2:
            try:
                value = float(self.parametersPanel.txtForwardMP.Value);
                self.parametersPanel.txtForwardTP.Value = MathHelper.smethod_3(value + float(self.parametersPanel.pnlVarStartP.Value));
            except:
                self.parametersPanel.txtForwardTP.Value = 0.0
    def txtDegreeBox_textChangedP(self):

        try:
            value = float(self.parametersPanel.txtForwardTP.Value);
            self.parametersPanel.txtForwardMP.Value = MathHelper.smethod_3(value - float(self.parametersPanel.pnlVarStartP.Value))
        except:
            self.parametersPanel.txtForwardMP.Value = 0.0
    def method_28_P(self, degrees_Lat, degrees_Lon):
        point3d = None
        point3d1 = None
        self.surfaceType = SurfaceTypes.GeoDeterminePosition
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        if define._units == QGis.Meters:
            point3d0 = self.parametersPanel.pnlStartPosP.Point3d

            point3d = QgisHelper.CrsTransformPoint(point3d0.get_X(), point3d0.get_Y(), define._latLonCrs, define._xyCrs)
            point3d1 = QgisHelper.CrsTransformPoint(degrees_Lon, degrees_Lat, define._latLonCrs, define._xyCrs)
        else:
            point3d = self.parametersPanel.pnlStartPosP.Point3d
            point3d1 = Point3D(degrees_Lon, degrees_Lat)


        constructionLayer = None;
        mapUnits = define._canvas.mapUnits()
        if self.parametersPanel.chbMarkPointsP.isChecked():
            constructionLayer = AcadHelper.createVectorLayer(SurfaceTypes.GeoDeterminePosition + "_MarkPoint", QGis.Point)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, point3d)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, point3d1)

            # if mapUnits == QGis.Meters:
            #     constructionLayer = QgsVectorLayer("point?crs=%s"%define._xyCrs.authid (), SurfaceTypes.GeoDeterminePosition + "_MarkPoint", "memory")
            # else:
            #     constructionLayer = QgsVectorLayer("point?crs=%s"%define._latLonCrs.authid (), SurfaceTypes.GeoDeterminePosition + " MarkPoint", "memory")
            #
            # shpPath = ""
            # if define.obstaclePath != None:
            #     shpPath = define.obstaclePath
            # elif define.xmlPath != None:
            #     shpPath = define.xmlPath
            # else:
            #     shpPath = define.appPath
            # er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + SurfaceTypes.GeoDeterminePosition + "_MarkPoint" + ".shp", "utf-8", constructionLayer.crs())
            # constructionLayer = QgsVectorLayer(shpPath + "/" + SurfaceTypes.GeoDeterminePosition + "_MarkPoint" + ".shp", SurfaceTypes.GeoDeterminePosition + " MarkPoint", "ogr")
            #
            # constructionLayer.startEditing()
            #
            # feature = QgsFeature()
            # feature.setGeometry(QgsGeometry.fromPoint(point3d))
            # constructionLayer.addFeature(feature)
            # feature.setGeometry(QgsGeometry.fromPoint(point3d1))
            # constructionLayer.addFeature(feature)
            # constructionLayer.commitChanges()
            QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.GeoDeterminePosition)

            self.resultLayerList.append(constructionLayer)
        if self.parametersPanel.chbDrawLineP.isChecked():
            constructionLayer1 = AcadHelper.createVectorLayer(SurfaceTypes.GeoDeterminePosition + "_Line", QGis.Line)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer1, [point3d, point3d1])
            QgisHelper.appendToCanvas(define._canvas, [constructionLayer1], SurfaceTypes.GeoDeterminePosition)
            self.resultLayerList.append(constructionLayer1)
    def method_28_BD(self):
        point3d = None
        point3d1 = None
        self.surfaceType = SurfaceTypes.GeoDetermineBD
        flag = FlightPlanBaseDlg.btnConstruct_Click(self)
        if not flag:
            return
        if define._units == QGis.Meters:
            point3d0 = self.parametersPanel.pnlStartPosBD.Point3d
            point3dF0 = self.parametersPanel.pnlFinishPosBD.Point3d

            point3d = QgisHelper.CrsTransformPoint(point3d0.get_X(), point3d0.get_Y(), define._latLonCrs, define._xyCrs)
            point3d1 = QgisHelper.CrsTransformPoint(point3dF0.get_X(), point3dF0.get_Y(), define._latLonCrs, define._xyCrs)
        else:
            point3d = self.parametersPanel.pnlStartPosBD.Point3d
            point3d1 = self.parametersPanel.pnlFinishPosBD.Point3d

        constructionLayer = None;
        mapUnits = define._canvas.mapUnits()
        if self.parametersPanel.chbMarkPointsBD.isChecked():
            constructionLayer = AcadHelper.createVectorLayer(SurfaceTypes.GeoDetermineBD + "_MarkPoint", QGis.Point)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, point3d)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, point3d1)

            # if mapUnits == QGis.Meters:
            #     constructionLayer = QgsVectorLayer("point?crs=%s"%define._xyCrs.authid (), SurfaceTypes.GeoDetermineBD + "_MarkPoint", "memory")
            # else:
            #     constructionLayer = QgsVectorLayer("point?crs=%s"%define._latLonCrs.authid (), SurfaceTypes.GeoDetermineBD + " MarkPoint", "memory")
            #
            # shpPath = ""
            # if define.obstaclePath != None:
            #     shpPath = define.obstaclePath
            # elif define.xmlPath != None:
            #     shpPath = define.xmlPath
            # else:
            #     shpPath = define.appPath
            # er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + QString(SurfaceTypes.GeoDetermineBD).replace(" ", "") + "_MarkPoint" + ".shp", "utf-8", constructionLayer.crs())
            # constructionLayer = QgsVectorLayer(shpPath + "/" + QString(SurfaceTypes.GeoDetermineBD).replace(" ", "") + "_MarkPoint" + ".shp", SurfaceTypes.GeoDetermineBD + " MarkPoint", "ogr")
            #
            # constructionLayer.startEditing()
            #
            #
            # feature = QgsFeature()
            # feature.setGeometry(QgsGeometry.fromPoint(point3d))
            # constructionLayer.addFeature(feature)
            # feature.setGeometry(QgsGeometry.fromPoint(point3d1))
            # constructionLayer.addFeature(feature)
            # constructionLayer.commitChanges()
            QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.GeoDetermineBD)
            self.resultLayerList.append(constructionLayer)
        if self.parametersPanel.chbDrawLineBD.isChecked():
            constructionLayer = AcadHelper.createVectorLayer(SurfaceTypes.GeoDetermineBD + "_Line", QGis.Line)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, [point3d, point3d1])
            QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.GeoDetermineBD)
            self.resultLayerList.append(constructionLayer)
    def method_28_MVD(self):
        self.parametersPanel.txtResult.Value = ""
    def method_29_P(self):
        self.resultModelP.clear()
        self.resultModelP.setHorizontalHeaderLabels(["Type", "Value"])

    def method_29_BD(self):
        degree = None;
        degree1 = None;
        degree2 = None;
        if (self.parametersPanel.pnlStartPosBD.IsValid()):

            result, degree, degree1 = self.parametersPanel.pnlStartPosBD.method_3();
            result, degree2 = Geo.smethod_7(degree, degree1, Altitude(0), self.modelBD, self.dateBD)
            if (result):
                degree2 = round(degree2, 2);
                self.parametersPanel.pnlVarStartBD.Value = degree2;

    def method_30_BD(self):
        degree = None;
        degree1 = None;
        degree2 = None;
        if (self.parametersPanel.pnlFinishPosBD.IsValid()):

            result, degree, degree1 = self.parametersPanel.pnlFinishPosBD.method_3();
            result, degree2 = Geo.smethod_7(degree, degree1, Altitude(0), self.modelBD, self.dateBD)
            if (result):
                degree2 = round(degree2, 2);
                self.parametersPanel.pnlVarFinishBD.Value = degree2;
    def method_31_BD(self):
        self.resultModelBD.clear()
        self.resultModelBD.setHorizontalHeaderLabels(["Type", "Value"])
    def method_32_P(self):
        startPos = self.parametersPanel.pnlStartPosP.Point3d
        result, self.date, self.model = DlgMagneticVariationParameters.smethod_0(self.date, self.model)
        if self.parametersPanel.pnlStartPosP.IsValid() and result:
            result, degree, degree1 = self.parametersPanel.pnlStartPosP.method_3();
            result, degree2 = Geo.smethod_7(degree, degree1, Altitude(0), self.model, self.date)
            if (result):
                degree2 = round(degree2, 2);
                self.parametersPanel.pnlVarStartP.Value = degree2;
                try:
                    self.parametersPanel.txtForwardMP.Value = MathHelper.smethod_3(float(self.parametersPanel.txtForwardTP.Value) - degree2)
                except:
                    self.parametersPanel.txtForwardMP.Value = 0.0
                self.method_29_P();


    def method_34_BD(self):
        startPos = self.parametersPanel.pnlStartPosBD.Point3d
        result, self.dateBD, self.modelBD = DlgMagneticVariationParameters.smethod_0(self.dateBD, self.modelBD)
        if self.parametersPanel.pnlStartPosBD.IsValid() and result:
            self.method_29_BD();
            self.method_31_BD()
    def method_36_BD(self):
        startPos = self.parametersPanel.pnlFinishPosBD.Point3d
        result, self.dateBD, self.modelBD = DlgMagneticVariationParameters.smethod_0(self.dateBD, self.modelBD)
        if self.parametersPanel.pnlFinishPosBD.IsValid() and result:
            self.method_30_BD();
            self.method_31_BD()