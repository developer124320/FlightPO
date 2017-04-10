# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QSize, Qt, QModelIndex
from PyQt4.QtGui import QMessageBox, QStandardItem,QSizePolicy,QFont, QFileDialog, QLabel, QSpinBox, \
    QIcon, QPixmap, QApplication, QMenu, QCursor
from qgis.core import QgsMapLayerRegistry,QgsCoordinateReferenceSystem,QgsPoint, QGis, QgsGeometry, QgsVectorLayer, QgsFeature, QgsField, QgsSvgMarkerSymbolLayerV2, QgsCategorizedSymbolRendererV2, QgsSingleSymbolRendererV2, QgsSymbolV2, QgsRendererCategoryV2

from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import CriticalObstacleType, ObstacleTableColumnType, SurfaceTypes, DistanceUnits,AircraftSpeedCategory,\
    OrientationType, AltitudeUnits, ObstacleAreaResult, TurnDirection, GeoCalculationType
from FlightPlanner.PathTerminators.ui_PathTerminators import Ui_PathTerminators
from FlightPlanner.QgisHelper import Geo
from FlightPlanner.helpers import Altitude, Unit, Distance, MathHelper, Speed
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Confirmations import Confirmations
from FlightPlanner.types import Point3D, DegreesType
from FlightPlanner.DataHelper import DataHelper
from FlightPlanner.Captions import Captions
from FlightPlanner.messages import Messages
from Type.Degrees import Degrees
import define

class PathTerminatorsDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("PathTerminatorsDlg")
        self.surfaceType = SurfaceTypes.PathTerminators
        self.selectedRow = None
        self.editingModelIndex = None

        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.PathTerminators)
        self.resize(540, 550)
        QgisHelper.matchingDialogSize(self, 1100, 650)
        self.surfaceList = None

        #   const variable
        self.ID = "id";
        self.LAT = "lat";
        self.LON = "lon";
        self.PT = "pt";
        self.FLYOVER = "flyover";
        self.COURSE = "course";
        self.TURNDIR = "turndir";
        self.ALT = "altitude";
        self.TIMEDIST = "timedist";
        self.SPEED = "speed";
        self.CENLAT = "cenlat";
        self.CENLON = "cenlon";

        self.table = None;
        self.updating = False;
        self.loaded = True;

    
    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        # self.ui.btnConstruct.setVisible(False)
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/btnImage/exportResult.png"), QIcon.Normal, QIcon.Off)
        self.ui.btnConstruct.setIcon(icon)
        self.ui.btnConstruct.setToolTip("Export")
        self.ui.btnEvaluate.setVisible(False)
        self.ui.btnPDTCheck.setVisible(False)
        # self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        self.ui.tabCtrlGeneral.removeTab(1)
#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)

    def btnEvaluate_Click(self):
        return FlightPlanBaseDlg.btnEvaluate_Click(self)

    def btnConstruct_Click(self):
        filePathDir = QFileDialog.getSaveFileName(self, "Export XML Data", QCoreApplication.applicationDirPath (),"ExportXMLfiles(*.xml)")
        if filePathDir == "":
            return

        DataHelper.saveExportResult(filePathDir, self.surfaceType, self.parametersPanel.grid, None, [], [], "Table")
#
        return FlightPlanBaseDlg.btnConstruct_Click(self)

        
    def initParametersPan(self):
        ui = Ui_PathTerminators()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.pnlProcType.Items = ["SID", "STAR", "Approach", "MissedApproach"]
        self.parametersPanel.pnlBasedOn.Items = ["Arinc424", "PansOps"]
        self.parametersPanel.pnlFlyOver.Items = ["Yes", "No"]
        self.parametersPanel.pnlTurnDir.Items = ["Nothing", "Left", "Right"]

        self.parametersPanel.grid.hideColumn(0)



        self.parametersPanel.btnAdd.clicked.connect(self.btnAdd_clicked)
        self.parametersPanel.btnRemove.clicked.connect(self.btnRemove_clicked)
        self.parametersPanel.btnDown.clicked.connect(self.btnDown_clicked)
        self.parametersPanel.btnUp.clicked.connect(self.btnUp_clicked)
        self.parametersPanel.pnlWpt.txtID.textChanged.connect(self.pnlWpt_positionChanged)

        self.connect(self.parametersPanel.pnlBasedOn, SIGNAL("Event_0"), self.pnlBasedOn_Event_0)
        self.connect(self.parametersPanel.pnlSpeed, SIGNAL("Event_0"), self.pnlSpeed_Event_0)
        self.connect(self.parametersPanel.pnlAltitude, SIGNAL("Event_0"), self.pnlAltitude_Event_0)
        self.connect(self.parametersPanel.pnlFlyOver, SIGNAL("Event_0"), self.pnlFlyOver_Event_0)
        self.connect(self.parametersPanel.pnlWpt, SIGNAL("positionChanged"), self.pnlWpt_positionChanged)
        self.connect(self.parametersPanel.pnlArcCen, SIGNAL("positionChanged"), self.pnlArcCen_positionChanged)
        self.connect(self.parametersPanel.pnlTime, SIGNAL("Event_0"), self.pnlTime_Event_0)
        self.connect(self.parametersPanel.pnlDist, SIGNAL("Event_0"), self.pnlDist_Event_0)
        self.connect(self.parametersPanel.pnlTurnDir, SIGNAL("Event_0"), self.pnlTurnDir_Event_0)
        self.connect(self.parametersPanel.pnlCourse, SIGNAL("Event_0"), self.pnlCourse_Event_0)
        # self.connect(self.parametersPanel.pnlTime, SIGNAL("Event_0"), self.pnlTime_Event_0)
        self.connect(self.parametersPanel.pnlPT, SIGNAL("Event_0"), self.pnlPT_Event_0)
        self.connect(self.parametersPanel.pnlProcType, SIGNAL("Event_0"), self.pnlProcType_Event_0)
        # self.parametersPanel.grid.clicked.connect(self.grid_clicked)
        self.parametersPanel.grid.pressed.connect(self.grid_pressed)
        # self.parametersPanel.grid.doubleClicked.connect(self.grid_doubleClicked)
        # self.parametersPanel.gridStdModel.itemChanged.connect(self.gridStdModel_itemChanged)
        self.updating = True
        self.method_31()
        self.method_30()
        self.method_32()
        self.method_33()
        self.method_39()
        self.updating = False
    def grid_pressed(self):
        if QApplication.mouseButtons() == Qt.RightButton:
            menu = QMenu()
            actionClear = QgisHelper.createAction(menu, "Clear All", self.menuClearClick)
            menu.addAction(actionClear)
            pos = QCursor.pos()
            menu.exec_(pos)
            pass
        elif QApplication.mouseButtons() == Qt.LeftButton:
            selectedIndexes = self.parametersPanel.grid.selectedIndexes()
            if self.updating:
                return
            if self.selectedRow == selectedIndexes[0].row():
                return
            self.selectedRow = selectedIndexes[0].row()
            self.method_30();
            self.method_32();
            self.method_33();
            self.method_39()
    def menuClearClick(self):
        if QMessageBox.question(self, "Question", Confirmations.DELETE_ALL_ENTRIES_FROM_LIST, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.parametersPanel.gridStdModel.clear()
            self.parametersPanel.gridStdModel.setHorizontalHeaderLabels(["#",
                                                                         "ID",
                                                                         "Latitude",
                                                                         "Longitude",
                                                                         "P/T",
                                                                         "Fly-over",
                                                                         unicode("Course (° T)", "utf-8"),
                                                                         "Turn Direction",
                                                                         "Altitude (ft)",
                                                                         "Dist. (nm) / Time (min)",
                                                                         "Speed Limit (kts)",
                                                                         "Center Latitude",
                                                                         "Center Longitude"])
            self.parametersPanel.grid.hideColumn(0)

            self.updating  = True
            self.method_30();
            self.method_32();
            self.method_33();
            self.method_39();
            self.updating = False
    def pnlBasedOn_Event_0(self, sender):
        self.method_40(self.parametersPanel.pnlBasedOn)
    def pnlSpeed_Event_0(self):
        self.method_40(self.parametersPanel.pnlSpeed)
    def pnlAltitude_Event_0(self):
        self.method_40(self.parametersPanel.pnlAltitude)
    def pnlFlyOver_Event_0(self):
        self.method_40(self.parametersPanel.pnlFlyOver)
    def pnlWpt_positionChanged(self):
        self.method_40(self.parametersPanel.pnlWpt)
    def pnlArcCen_positionChanged(self):
        self.method_40(self.parametersPanel.pnlArcCen)
    def pnlTime_Event_0(self):
        self.method_40(self.parametersPanel.pnlTime)
    def pnlDist_Event_0(self):
        self.method_40(self.parametersPanel.pnlDist)
    def pnlTurnDir_Event_0(self):
        self.method_40(self.parametersPanel.pnlTurnDir)
    def pnlCourse_Event_0(self):
        self.method_40(self.parametersPanel.pnlCourse)
    def pnlPT_Event_0(self):
        self.method_40(self.parametersPanel.pnlPT)
    def pnlProcType_Event_0(self):
        self.method_40(self.parametersPanel.pnlProcType)

    def btnDown_clicked(self):
        if self.selectedRow != None:
            self.updating = True
            itemList = self.parametersPanel.gridStdModel.takeRow(self.selectedRow)
            self.parametersPanel.gridStdModel.insertRow(self.selectedRow + 1, itemList)
            self.selectedRow += 1
            self.method_33();
            self.method_39();

            self.updating = False

    def btnUp_clicked(self):
        if self.selectedRow != None:
            self.updating = True
            itemList = self.parametersPanel.gridStdModel.takeRow(self.selectedRow)
            self.parametersPanel.gridStdModel.insertRow(self.selectedRow - 1, itemList)
            self.selectedRow -= 1
            self.method_33();
            self.method_39();

            self.updating = False

    def btnRemove_clicked(self):
        if self.selectedRow != None:
            self.updating = True
            self.parametersPanel.gridStdModel.removeRow(self.selectedRow)
            if self.selectedRow >= self.parametersPanel.gridStdModel.rowCount() and self.parametersPanel.gridStdModel.rowCount() > 0:
                self.selectedRow -= 1
            self.method_30();
            self.method_32();
            self.method_33();
            self.method_39();

            self.updating = False


    def btnAdd_clicked(self):
        # PathTerminators.table.Rows.Add(PathTerminators.table.NewRow());
        # self.grid.CurrentCell = self.grid.Rows[self.grid.RowCount - 1].Cells[0];
        self.updating = True
        newRow = self.parametersPanel.gridStdModel.rowCount()
        self.parametersPanel.gridStdModel.setItem(newRow, 0, QStandardItem(""))
        # self.parametersPanel.grid.selectRow(newRow)
        # self.grid_clicked()
        try:
            self.method_30();
            self.method_32();
            self.method_33();
            self.method_39();
        except:
            pass

        self.updating = False

    def method_30(self):
        self.updating = True
        row = None;
        if (self.selectedRow != None):
            row = self.selectedRow;
        if (row != None):
            pathTerminator = "None";
            if (not self.method_35(row, 4)):
                pathTerminator = self.parametersPanel.gridStdModel.item(row, 4).text()
            if pathTerminator != "None" and pathTerminator != "":
                self.parametersPanel.pnlPT.SelectedIndex = self.parametersPanel.pnlPT.Items.index(pathTerminator)#(string.Concat(pathTerminator.ToString(), " - ", EnumHelper.smethod_0(pathTerminator)));
            else:
                self.parametersPanel.pnlPT.SelectedIndex = -1
            strS = "";
            if (not self.method_35(row, 1)):
                strS = self.parametersPanel.gridStdModel.item(row, 1).text()#(string)item["id"];
            naN = None;
            if (not self.method_35(row, 2)):
                degree0 = Degrees.smethod_15(self.parametersPanel.gridStdModel.item(row, 2).text(), DegreesType.Latitude)
                naN = degree0.value
                # naN = float(self.parametersPanel.gridStdModel.item(row, 2).text())#item["lat"];
            degree = None;
            if (not self.method_35(row, 3)):
                degree0 = Degrees.smethod_15(self.parametersPanel.gridStdModel.item(row, 3).text(), DegreesType.Longitude)
                degree = degree0.value
                # degree = float(self.parametersPanel.gridStdModel.item(row, 3).text())#(Degrees)item["lon"];
            if naN != None:
                self.parametersPanel.pnlWpt.ID = strS
                self.parametersPanel.pnlWpt.Point3d = Point3D(degree, naN, None, None, strS);
            else:
                self.parametersPanel.pnlWpt.ID = ""
                self.parametersPanel.pnlWpt.Point3d = None
            num = -1;
            if (not self.method_35(row, 5)):
                num = 0 if(self.parametersPanel.gridStdModel.item(row, 5).text() == "Yes") else 1#((bool)item["flyover"] ? 0 : 1);
            self.parametersPanel.pnlFlyOver.SelectedIndex = num;
            altitude = None
            if (not self.method_35(row, 8)):
                altitude = Altitude(float(self.parametersPanel.gridStdModel.item(row, 8).text()), AltitudeUnits.FT)#(Altitude)item["altitude"];
            self.parametersPanel.pnlAltitude.CaptionUnits = "ft"
            self.parametersPanel.pnlAltitude.Value = altitude;
            speed = None
            if (not self.method_35(row, 10)):
                speed = Speed(float(self.parametersPanel.gridStdModel.item(row, 10).text()))#(Speed)item["speed"];
            self.parametersPanel.pnlSpeed.Value = speed;
            item1 = None;
            if (not self.method_35(row, 6)):
                item1 = float(self.parametersPanel.gridStdModel.item(row, 6).text())#(double)item["course"];
            self.parametersPanel.pnlCourse.Value = item1;
            distance = None
            if (not self.method_35(row, 9)):
                distance = Distance(float(self.parametersPanel.gridStdModel.item(row, 9).text()), DistanceUnits.NM)#(Distance)item["timedist"];
            if distance == None:
                self.parametersPanel.pnlTime.Value = None;
                self.parametersPanel.pnlDist.Value = None;
            else:
                self.parametersPanel.pnlTime.Value = distance.Metres;
                self.parametersPanel.pnlDist.Value = distance;
            turnDirection = TurnDirection.Nothing;
            if (not self.method_35(row, 7)):
                if self.parametersPanel.gridStdModel.item(row, 7).text() == "Left":
                    turnDirection = 1
                elif self.parametersPanel.gridStdModel.item(row, 7).text() == "Right":
                    turnDirection = -1
                else:
                    turnDirection = 0
                # turnDirection = (TurnDirection)item["turndir"];
            if (turnDirection == TurnDirection.Left):
                self.parametersPanel.pnlTurnDir.SelectedIndex = 1;
            elif (turnDirection != TurnDirection.Right):
                self.parametersPanel.pnlTurnDir.SelectedIndex = 0;
            else:
                self.parametersPanel.pnlTurnDir.SelectedIndex = 2;
            naN1 = None;
            if (not self.method_35(row,11)):
                degree0 = Degrees.smethod_15(self.parametersPanel.gridStdModel.item(row, 11).text(), DegreesType.Latitude)
                naN1 = degree0.value
                # naN1 = float(self.parametersPanel.gridStdModel.item(row, 11).text()) #(Degrees)item["cenlat"];

            degree1 = None;
            if (not self.method_35(row, 12)):
                degree0 = Degrees.smethod_15(self.parametersPanel.gridStdModel.item(row, 12).text(), DegreesType.Longitude)
                degree1 = degree0.value
                # degree1 = float(self.parametersPanel.gridStdModel.item(row, 12).text() )#(Degrees)item["cenlon"];
            if naN1 != None:
                self.parametersPanel.pnlArcCen.Point3d = Point3D(naN1, degree1);
            else:
                self.parametersPanel.pnlArcCen.Point3d = None
        self.updating = False
    def method_31(self):

        pathTerminator = self.method_34();
        self.parametersPanel.pnlPT.Clear();
        for value in pathTerminatorValueList:
            pathTerminator1 = value;
            if (self.parametersPanel.pnlBasedOn.SelectedIndex != 0):
                strArrays = ["IF", "CA", "CF", "DF", "FA", "FM", "HM", "RF", "TF", "VA", "VI", "VM"];
                if (not self.method_36(pathTerminator1, strArrays)):
                    continue;
                self.parametersPanel.pnlPT.Items = [pathTerminator1]# + " - ", EnumHelper.smethod_0(pathTerminator1)));
            else:
                if (pathTerminator1 == "None"):
                    continue;
                self.parametersPanel.pnlPT.Items = [pathTerminator1]#.Add(string.Concat(pathTerminator1.ToString(), " - ", EnumHelper.smethod_0(pathTerminator1)));
        if (pathTerminator != "None"):
            self.parametersPanel.pnlPT.SelectedIndex = self.parametersPanel.pnlPT.Items.index(pathTerminator)#(string.Concat(pathTerminator.ToString(), " - ", EnumHelper.smethod_0(pathTerminator)));
    
    def method_32(self):
        self.updating = True
        row = None;
        if (self.selectedRow != None):
            row = self.selectedRow;
        self.parametersPanel.pnlPT.Enabled = row != None;
        if (not self.parametersPanel.pnlPT.Enabled):
            self.parametersPanel.pnlPT.SelectedIndex = -1;
            if (row != None):
                self.parametersPanel.gridStdModel.setItem(row, 4, QStandardItem("None"))
        pathTerminator = self.method_34();
        # GroupBox groupBox = self.parametersPanel.gbWpt;
        strArrays = ["AF", "CF", "DF", "FA", "FC", "FD", "FM", "HA", "HF", "HM", "IF", "PI", "RF", "TF", "VM"];
        self.parametersPanel.gbWpt.setEnabled(self.method_36(pathTerminator, strArrays));
        if (not self.parametersPanel.gbWpt.isEnabled()):
            self.parametersPanel.pnlWpt.Point3d = None;
            if (row != None):
                self.parametersPanel.gridStdModel.setItem(row, 1, QStandardItem(""))#item["id"] = "";
                self.parametersPanel.gridStdModel.setItem(row, 2, QStandardItem(""))
                self.parametersPanel.gridStdModel.setItem(row, 3, QStandardItem(""))
                # item["lat"] = Degrees.NaN;
                # item["lon"] = Degrees.NaN;
        # ComboBoxPanel comboBoxPanel = self.pnlFlyOver;
        strArrays1 = ["AF", "CF", "CI", "CR", "DF", "FC", "FD", "RF", "TF", "VI", "VR", "IF"];
        self.parametersPanel.pnlFlyOver.Enabled = self.method_36(pathTerminator, strArrays1);
        if (not self.parametersPanel.pnlFlyOver.Enabled):
            self.parametersPanel.pnlFlyOver.SelectedIndex = -1;
            if (row != None):
                self.parametersPanel.gridStdModel.setItem(row, 5, QStandardItem(""))#item["flyover"] = DBNone.Value;
        # TrackRadialBoxPanel trackRadialBoxPanel = self.pnlCourse;
        strArrays2 = ["AF", "CA", "CD", "CF", "CI", "CR", "FA", "FC", "FD", "FM", "HF", "PI", "HA", "HM", "TF", "RF", "VA", "VD", "VI", "VM", "VR"];
        self.parametersPanel.pnlCourse.Enabled = self.method_36(pathTerminator, strArrays2);
        if (not self.parametersPanel.pnlCourse.Enabled):
            self.parametersPanel.pnlCourse.Value = 0.0;
            if (row != None):
                self.parametersPanel.gridStdModel.setItem(row, 6, QStandardItem(""))#item["course"] = DBNone.Value;
        if (pathTerminator == "AF"):
            self.parametersPanel.pnlCourse.Caption = Captions.BOUNDARY_RADIAL;
        elif (pathTerminator != "RF"):
            strArrays3 = ["VA", "VD", "VI", "VM", "VR"];
            if (not self.method_36(pathTerminator, strArrays3)):
                self.parametersPanel.pnlCourse.Caption = Captions.COURSE;
            else:
                self.parametersPanel.pnlCourse.Caption = Captions.HEADING;
        else:
            self.parametersPanel.pnlCourse.Caption = Captions.OUTBOUND_TANG_TRACK;
        # ComboBoxPanel comboBoxPanel1 = self.pnlTurnDir;
        strArrays4 = ["CA", "CD", "CF", "CI", "CR", "DF", "FA", "FC", "FD", "FM", "HA", "HF", "HM", "IF", "TF", "VA", "VD", "VI", "VM", "AF", "PI", "RF"];
        self.parametersPanel.pnlTurnDir.Enabled = self.method_36(pathTerminator, strArrays4);
        if (not self.parametersPanel.pnlTurnDir.Enabled):
            self.parametersPanel.pnlTurnDir.SelectedIndex = -1;
            if (row != None):
                self.parametersPanel.gridStdModel.setItem(row, 7, QStandardItem(""))#item["turndir"] = DBNone.Value;
        self.parametersPanel.pnlAltitude.Enabled = pathTerminator != "None";
        # NumberBoxPanel numberBoxPanel = self.pnlTime;
        strArrays5 = ["HA", "HF", "HM" ]
        self.parametersPanel.pnlTime.Enabled = self.method_36(pathTerminator, strArrays5);
        if (not self.parametersPanel.pnlTime.Enabled):
            self.parametersPanel.pnlTime.Value = None;
        # DistanceBoxPanel distanceBoxPanel = self.pnlDist;
        strArrays6 = ["TF", "CD", "FD", "VD", "FC", "PI", "RF" ];
        self.parametersPanel.pnlDist.Enabled = self.method_36(pathTerminator, strArrays6);
        if (not self.parametersPanel.pnlDist.Enabled):
            self.parametersPanel.pnlDist.Value = None;
        strArrays7 = ["CD", "FD", "VD" ];
        if (not self.method_36(pathTerminator, strArrays7)):
            strArrays8 = ["TF", "FC", "PI" ];
            if (self.method_36(pathTerminator, strArrays8)):
                self.parametersPanel.pnlDist.Caption = Captions.PATH_LENGTH;
                self.parametersPanel.pnlDist.Button = "coordinate_capture.png";
            elif (not self.method_36(pathTerminator, ["RF"])):
                self.parametersPanel.pnlDist.Caption = Captions.DISTANCE;
                self.parametersPanel.pnlDist.Button = None;
            else:
                self.parametersPanel.pnlDist.Caption = Captions.ALONG_TRACK_DISTANCE;
                self.parametersPanel.pnlDist.Button = "coordinate_capture.png";
        else:
            self.parametersPanel.pnlDist.Caption = Captions.DME_DISTANCE;
            self.parametersPanel.pnlDist.Button = "coordinate_capture.png";
        if (row != None and not self.parametersPanel.pnlTime.Enabled and not self.parametersPanel.pnlDist.Enabled):
            self.parametersPanel.gridStdModel.setItem(row, 9, QStandardItem(""))#item["timedist"] = DBNone.Value;
        self.parametersPanel.pnlSpeed.Enabled = pathTerminator != "None";
        self.parametersPanel.pnlArcCen.groupBox.setEnabled(pathTerminator == "RF");
        if (not self.parametersPanel.pnlArcCen.groupBox.isEnabled()):
            self.parametersPanel.pnlArcCen.Point3d = None;
            if (row != None):
                self.parametersPanel.gridStdModel.setItem(row, 11, QStandardItem(""))#item["cenlat"] = DBNone.Value;
                self.parametersPanel.gridStdModel.setItem(row, 12, QStandardItem(""))#item["cenlon"] = DBNone.Value;
        self.updating = False
    def method_33(self):
        flag = (self.selectedRow != None);
        index = -1;
        if (flag):
            index = self.selectedRow
            # index = self.grid.SelectedRows[0].Index;
        self.parametersPanel.btnRemove.setEnabled(flag);
        self.parametersPanel.btnUp.setEnabled(False if(not flag) else index > 0);
        self.parametersPanel.btnDown.setEnabled(False if(not flag or index < 0) else index < self.parametersPanel.gridStdModel.rowCount() - 1);
    
    def method_34(self):
        if self.parametersPanel.pnlPT.comboBox.count() == 0:
            return "None"
        if (self.parametersPanel.pnlPT.SelectedIndex < 0):
            return "None"
        return self.parametersPanel.pnlPT.SelectedItem#(PathTerminators.PathTerminator)Enum.Parse(typeof(PathTerminators.PathTerminator), self.pnlPT.SelectedItem.ToString().Substring(0, 2));


    
    def method_35(self, row, col):
        item = self.parametersPanel.gridStdModel.item(row, col)
        if (item != None):
            if item.text() != "":
                return False;
            else:
                return True
        return True;
    def method_36(self, pathTerminator_0, stringList):
        # string0 = string_0;
        for i in range(len(stringList)):
            if stringList[i] == pathTerminator_0:
                return True;
        return False;
    
    def method_37(self):
        distance = None;
        num = None;
        num1 = None;
        degree = None;
        degree1 = None;
        resultArcCen, degree, degree1 = self.parametersPanel.pnlArcCen.method_3()

        if (self.selectedRow != None):
            index = self.selectedRow;
            if (index >= 1):
                pathTerminator = self.method_34();
                if (pathTerminator != "None"):
                    # DataRow item = PathTerminators.table.Rows[index];
                    if (not self.method_35(index, 2) and not self.method_35(index, 3)):
                        item1 = float(self.parametersPanel.gridStdModel.item(index, 2).text() )#(Degrees)item["lat"];
                        item2 = float(self.parametersPanel.gridStdModel.item(index, 3).text() )#(Degrees)item["lon"];
                        strArrays = ["CF", "TF" ];
                        result, distance, num, num1 = Geo.smethod_4(GeoCalculationType.Ellipsoid, float(self.parametersPanel.gridStdModel.item(index - 1, 2).text() ), float(self.parametersPanel.gridStdModel.item(index - 1, 3).text() ), item1, item2)
                        result1, distance, num01, num11 = Geo.smethod_4(GeoCalculationType.Ellipsoid, degree, degree1, item1, item2)
                        if (self.method_36(pathTerminator, strArrays)):
                            # dataRow = PathTerminators.table.Rows[index - 1];
                            if (self.method_35(index -1 , 2) or self.method_35(index - 1, 3)):
                                return;

                        elif (result):
                                self.parametersPanel.gridStdModel.setItem(index, 6, QStandardItem(str(num)))#item["course"] = num;
                                self.parametersPanel.pnlCourse.Value = num;
                        elif (self.method_36(pathTerminator, ["RF"])):
                            if (self.parametersPanel.pnlTurnDir.SelectedIndex < 1):
                                return;
                            elif (not resultArcCen):
                                return;
                            elif (result1):
                                num = MathHelper.smethod_3(num01 + 90) if(self.parametersPanel.pnlTurnDir.SelectedIndex != 1) else MathHelper.smethod_3(num01 - 90);
                                self.parametersPanel.gridStdModel.setItem(index, 6, QStandardItem(str(num)))#item["course"] = num;
                                self.parametersPanel.pnlCourse.Value = num;
    def method_38(self):
        distance = None;
        num = None;
        num1 = None;
        degree = None;
        degree1 = None;
        num2 = None;
        num3 = None;
        if (self.selectedRow != None):
            index = self.selectedRow;
            if (index >= 1):
                pathTerminator = self.method_34();
                if (pathTerminator != "None"):
                    # DataRow item = PathTerminators.table.Rows[index];
                    if (not self.method_35(index, 2) and not self.method_35(index, 3)):
                        item1 = float(self.parametersPanel.gridStdModel.item(index, 2).text() )#(Degrees)item["lat"];
                        item2 = float(self.parametersPanel.gridStdModel.item(index, 3).text() )#(Degrees)item["lon"];
                        # DataRow dataRow = PathTerminators.table.Rows[index - 1];
                        if (not self.method_35(index - 1, 2) and  not self.method_35(index - 1, 3)):
                            degree2 = float(self.parametersPanel.gridStdModel.item(index - 1, 2).text() )
                            item3 = float(self.parametersPanel.gridStdModel.item(index - 1, 3).text() )
                            # degree2 = (Degrees)dataRow["lat"];
                            # item3 = (Degrees)dataRow["lon"];
                            if (self.method_36(pathTerminator, ["TF"])):
                                result0, distance, num, num1 = Geo.smethod_4(GeoCalculationType.Ellipsoid, degree2, item3, item1, item2)
                                if (result0):
                                    self.parametersPanel.gridStdModel.setItem(index, 9, QStandardItem(str(distance.NauticalMiles)))
                                    # item["timedist"] = new Distance(distance.NauticalMiles, DistanceUnits.NM);
                                    self.parametersPanel.pnlDist.Value = Distance(distance.NauticalMiles, DistanceUnits.NM);
                            elif (self.method_36(pathTerminator, ["RF"])):
                                result1, degree, degree1 = self.parametersPanel.pnlArcCen.method_3()
                                result2, distance, num2, num1 = Geo.smethod_4(GeoCalculationType.Ellipsoid, degree, degree1, degree2, item3)
                                result3, distance, num3, num1 = Geo.smethod_4(GeoCalculationType.Ellipsoid, degree, degree1, item1, item2)
                                if (self.parametersPanel.pnlTurnDir.SelectedIndex < 1):
                                    return;
                                elif (not result1):
                                    return;
                                elif (not result2):
                                    return;
                                elif (result3):
                                    if (self.parametersPanel.pnlTurnDir.SelectedIndex != 1):
                                        num = MathHelper.smethod_3(num3 - num2) if(num2 <= num3)else MathHelper.smethod_3(num3 + (360 - num2))
                                    else:
                                        num = MathHelper.smethod_3(num2 - num3) if(num2 >= num3) else MathHelper.smethod_3(num2 + (360 - num3));
                                    self.parametersPanel.gridStdModel.setItem(index, 9, QStandardItem(str(distance.NauticalMiles * Unit.ConvertDegToRad(num))))
                                    # item["timedist"] = new Distance(distance.NauticalMiles * Units.ConvertDegToRad(num), DistanceUnits.NM);
                                    self.parametersPanel.pnlDist.Value = Distance(distance.NauticalMiles * Unit.ConvertDegToRad(num), DistanceUnits.NM);
                                else:
                                    return;
    
    def method_39(self):
        self.parametersPanel.lblError.setText("");
        if self.parametersPanel.gridStdModel.rowCount() > 0:
            for num in range(self.parametersPanel.gridStdModel.rowCount()):
                # DataRow current = (DataRow)enumerator.Current;
                # int num = PathTerminators.table.Rows.IndexOf(current);
                item = "None";
                if (not self.method_35(num, 4)):
                    item = self.parametersPanel.gridStdModel.item(num, 4).text()#(PathTerminators.PathTerminator)current["pt"];

                if (num != 0):
                    pathTerminator = "None";
                    if (not self.method_35(num - 1, 4)):
                        pathTerminator = self.parametersPanel.gridStdModel.item(num - 1, 4).text()#(PathTerminators.PathTerminator)PathTerminators.table.Rows[num - 1]["pt"];

                    flag = False;
                    if (not self.method_35(num - 1, 5)):
                        if self.parametersPanel.gridStdModel.item(num - 1, 5).text() == "Yes":
                            flag = True
                        else:
                            flag = False
                        # flag = (bool)PathTerminators.table.Rows[num - 1]["flyover"];
                    if (pathTerminator == "AF"):
                        strArrays = ["DF", "IF", "PI", "TF" ];
                        if (self.method_36(item, strArrays)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "DF, IF, PI, TF"));
                            return;
                    elif (pathTerminator == "CA"):
                        strArrays1 = ["AF", "HA", "HF", "HM", "PI", "RF", "TF" ];
                        if (self.method_36(item, strArrays1)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "AF, HA, HF, HM, PI, RF, TF"));
                            return;
                    elif (pathTerminator == "CD"):
                        strArrays2 = ["HA", "HF", "HM", "PI", "RF", "TF" ];
                        if (self.method_36(item, strArrays2)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "HA, HF, HM, PI, RF, TF"));
                            return;
                    elif (pathTerminator == "CF"):
                        if (not flag):
                            if (item != "IF"):
                                if (item != "DF"):
                                    continue;
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "IF, DF"));
                            break;
                        elif (item == "IF"):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "IF"));
                            break;
                    elif (pathTerminator == "CI"):
                        strArrays3 = ["CA", "CD", "CI", "CR", "DF", "HA", "HF", "HM", "PI", "RF", "TF", "VA", "VD", "VI", "VM", "VR" ];
                        if (self.method_36(item, strArrays3)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "CA, CD, CI, CR, DF, HA, HF, HM, PI, RF, TF, VA, VD, VI, VM, VR"));
                            break;
                    elif (pathTerminator == "CR"):
                        strArrays4 = ["AF", "HA", "HF", "HM", "PI", "RF", "TF" ];
                        if (self.method_36(item, strArrays4)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "AF, HA, HF, HM, PI, RF, TF"));
                            break;
                    elif (pathTerminator == "DF"):
                        if (not flag):
                            if (item == "IF" or item == "DF"):
                                self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "IF, DF, RF"))
                                return;
                            if (item == "RF"):
                                self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "IF, DF, RF"));
                                return;
                        else:
                            if (item != "IF"):
                                if (item != "RF"):
                                    continue;
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "IF, RF"));
                            break;
                    elif (pathTerminator == "FA"):
                        strArrays5 = ["AF", "HA", "HF", "HM", "IF", "PI", "RF", "TF" ];
                        if (self.method_36(item, strArrays5)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "AF, HA, HF, HM, IF, PI, RF, TF"));
                            break;
                    elif (pathTerminator == "FC"):
                        strArrays6 = ["AF", "DF", "FA", "FC", "FD", "FM", "HA", "HF", "HM", "IF", "PI", "RF", "TF" ];
                        if (self.method_36(item, strArrays6)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "AF, DF, FA, FC, FD, FM, HA, HF, HM, IF, PI, RF, TF"));
                            break;
                    elif (pathTerminator == "FD"):
                        strArrays7 = ["FA", "FC", "FD", "FM", "HA", "HF", "HM", "IF", "PI", "RF", "TF" ];
                        if (self.method_36(item, strArrays7)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "FA, FC, FD, FM, HA, HF, HM, IF, PI, RF, TF"));
                            break;
                    elif (pathTerminator == "FM"):
                        strArrays8 = ["AF", "HA", "HF", "HM", "IF", "PI", "RF", "TF" ];
                        if (self.method_36(item, strArrays8)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "AF, HA, HF, HM, IF, PI, RF, TF"));
                            break;
                    elif (pathTerminator == "HA"):
                        strArrays9 = ["HA", "HF", "HM", "IF", "PI"];
                        if (self.method_36(item, strArrays9)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "HA, HF, HM, IF, PI"));
                            break;
                    elif (pathTerminator == "HF"):
                        strArrays10 = ["HA", "HF", "HM", "IF", "PI"];
                        if (self.method_36(item, strArrays10)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "HA, HF, HM, IF, PI"));
                            break;
                    elif (pathTerminator == "HM"):
                        strArrays11 = ["HA", "HF", "HM", "IF", "PI"];
                        if (self.method_36(item, strArrays11)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "HA, HF, HM, IF, PI"));
                            break;
                    elif (pathTerminator == "IF"):
                        if (item == "IF"):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "IF"));
                            break;
                    elif (pathTerminator == "PI"):
                        if (item != "CF"):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_BE_ONE_OF_THE_FOLLOWING%(num + 1, "CF"));
                            break;
                    elif (pathTerminator == "RF"):
                        strArrays12 = ["DF", "IF", "PI", "VA", "VD", "VI", "VM", "VR"];
                        if (self.method_36(item, strArrays12)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "DF, IF, PI, VA, VD, VI, VM, VR"));
                            break;
                    elif (pathTerminator == "TF"):
                        if (not flag):
                            strArrays13 = ["DF", "CF"];
                            if (self.method_36(item, strArrays13)):
                                self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "DF, CF"));
                                break;
                        else:
                            strArrays14 = ["TF", "CF"];
                            if (not self.method_36(item, strArrays14)):
                                self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_BE_ONE_OF_THE_FOLLOWING%(num + 1, "TF, CF"));
                                break;
                    elif (pathTerminator == "VA"):
                        strArrays15 = ["AF", "HA", "HF", "HM", "PI", "RF", "TF"];
                        if (self.method_36(item, strArrays15)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "AF, HA, HF, HM, PI, RF, TF"));
                            break;
                    elif (pathTerminator == "VD"):
                        strArrays16 = ["HA", "HF", "HM", "PI", "RF", "TF"];
                        if (self.method_36(item, strArrays16)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "HA, HF, HM, PI, RF, TF"));
                            break;
                    elif (pathTerminator == "VI"):
                        strArrays17 = ["AF", "CF", "FA", "FC", "FD", "FM", "IF"];
                        if (not self.method_36(item, strArrays17)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_BE_ONE_OF_THE_FOLLOWING%(num + 1, "AF, CF, FA, FC, FD, FM, IF"));
                            break;
                    elif (pathTerminator == "VM"):
                        strArrays18 = ["AF", "HA", "HF", "HM", "PI", "RF", "TF"];
                        if (self.method_36(item, strArrays18)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "AF, HA, HF, HM, PI, RF, TF"));
                            break;
                    elif (pathTerminator == "VR"):
                        strArrays19 = ["AF", "HA", "HF", "HM", "PI", "RF", "TF"];
                        if (self.method_36(item, strArrays19)):
                            self.parametersPanel.lblError.setText(Messages.PT_ENTRY_X_SHOULD_NOT_BE_ONE_OF_THE_FOLLOWING%(num + 1, "AF, HA, HF, HM, PI, RF, TF"));
                            break;
                else:
                    if self.parametersPanel.pnlProcType.SelectedIndex == 0:
                        strArrays20 = ["CF", "CA", "FA"];
                        if (self.method_36(item, strArrays20)):
                            continue;
                        self.parametersPanel.lblError.setText(Messages.PT_SID_SHOULD_START_WITH);
                        return;
                    elif self.parametersPanel.pnlProcType.SelectedIndex == 1:
                        if (self.method_36(item, ["IF"])):
                            continue;
                        self.parametersPanel.lblError.setText(Messages.PT_STAR_SHOULD_START_WITH);
                        return;
                    elif self.parametersPanel.pnlProcType.SelectedIndex == 2:
                        if (self.method_36(item, ["IF"])):
                            continue;
                        self.parametersPanel.lblError.setText(Messages.PT_APPROACH_SHOULD_START_WITH);
                        return;
                    elif self.parametersPanel.pnlProcType.SelectedIndex == 3:
                        strArrays21 = ["CF", "DF", "FA", "HA", "HM", "RF", "VM"];
                        if (self.method_36(item, strArrays21)):
                            continue;
                        self.parametersPanel.lblError.setText(Messages.PT_MISSED_APPROACH_SHOULD_START_WITH);
                        return;
                    else:
                        continue;

        # self.parametersPanel.lblError.setVisible(not self.parametersPanel.lblError.text() == "");
        # if (self.parametersPanel.lblError.isVisible()):
        #     using (Graphics graphic = self.lblError.CreateGraphics())
        #     {
        #         string text = self.lblError.Text;
        #         System.Drawing.Font font = self.lblError.Font;
        #         System.Drawing.Size size = self.lblError.Size;
        #         SizeF sizeF = graphic.MeasureString(text, font, size.Width);
        #         System.Drawing.Size size1 = sizeF.ToSize();
        #         Label label = self.lblError;
        #         int height = size1.Height;
        #         System.Windows.Forms.Padding padding = self.lblError.Padding;
        #         label.SetBounds(0, 0, 0, height + padding.Vertical, BoundsSpecified.Height);
        #    ]

    def method_40(self, sender):
        if (self.selectedRow == None):
            return;
        row = self.selectedRow;
        # DataRow item = PathTerminators.table.Rows[self.grid.SelectedRows[0].Index];
        if (sender == self.parametersPanel.pnlProcType):
            self.method_39();
            return;
        if (sender == self.parametersPanel.pnlBasedOn):
            if (self.parametersPanel.pnlBasedOn.SelectedIndex == 1):

                for i in range(self.parametersPanel.gridStdModel.rowCount()):
                    pathTerminator = "None";
                    if (not self.method_35(row, 4)):
                        pathTerminator = self.parametersPanel.gridStdModel.item(i, 4).text()#(PathTerminators.PathTerminator)row["pt"];
                    strArrays = ["HF", "HA", "PI", "CI", "CD", "CR", "FC", "FD", "AF", "VD", "VR" ];
                    if (not self.method_36(pathTerminator, strArrays)):
                        continue;
                    QMessageBox.warning(self, "Error", "One or more path terminators are based on ARINC 424.\n\nPlease change or remove the invalid path terminators (HF, HA, PI, CI, CD, CR, FC, FD, AF, VD, VR) before changing the criteria.");
                    self.parametersPanel.pnlBasedOn.SelectedIndex = 0;
                    return;
            self.method_31();
        if (self.updating):
            return
        # {
        if (sender == self.parametersPanel.pnlPT):
            self.parametersPanel.gridStdModel.setItem(row, 4, QStandardItem(self.method_34()))
            # item["pt"] = self.method_34();
            self.method_32();
        elif (sender == self.parametersPanel.pnlWpt):
            position = self.parametersPanel.pnlWpt.Point3d;
            self.parametersPanel.gridStdModel.setItem(row, 1, QStandardItem(self.parametersPanel.pnlWpt.ID))
            self.parametersPanel.gridStdModel.setItem(row, 2, QStandardItem(self.parametersPanel.pnlWpt.txtPointY.text()))
            self.parametersPanel.gridStdModel.setItem(row, 3, QStandardItem(self.parametersPanel.pnlWpt.txtPointX.text()))
            # item["id"] = position.ID;
            # item["lat"] = Degrees.smethod_1(position.XLat);
            # item["lon"] = Degrees.smethod_5(position.YLon);
            if (not self.parametersPanel.pnlCourse.Value != None ):
                self.method_37();
            if (not self.parametersPanel.pnlDist.Value.IsValid()):
                self.method_38();
        elif (sender == self.parametersPanel.pnlFlyOver):
            if (self.parametersPanel.pnlFlyOver.SelectedIndex == 0):
                self.parametersPanel.gridStdModel.setItem(row, 5, QStandardItem("Yes"))
                # item["flyover"] = true;
            elif (self.parametersPanel.pnlFlyOver.SelectedIndex != 1):
                self.parametersPanel.gridStdModel.setItem(row, 5, QStandardItem(""))
                # item["flyover"] = DBNull.Value;
            else:
                self.parametersPanel.gridStdModel.setItem(row, 5, QStandardItem("No"))
        elif (sender == self.parametersPanel.pnlAltitude):
            self.parametersPanel.gridStdModel.setItem(row, 8, QStandardItem(str(self.parametersPanel.pnlAltitude.Value.Feet)))
            # item["altitude"] = self.pnlAltitude.Value;
        elif (sender == self.parametersPanel.pnlSpeed):
            self.parametersPanel.gridStdModel.setItem(row, 10, QStandardItem(str(self.parametersPanel.pnlSpeed.Value.Knots)))
            # item["speed"] = self.pnlSpeed.Value;

        elif (sender == self.parametersPanel.pnlCourse):
            self.parametersPanel.gridStdModel.setItem(row, 6, QStandardItem(str(self.parametersPanel.pnlCourse.Value)))
            # item["course"] = self.pnlCourse.Value;
        elif (sender == self.parametersPanel.pnlTurnDir):
            if (self.parametersPanel.pnlTurnDir.SelectedIndex == 1):
                self.parametersPanel.gridStdModel.setItem(row, 7, QStandardItem("Left"))
                # item["turndir"] = TurnDirection.Left;
            elif (self.parametersPanel.pnlTurnDir.SelectedIndex != 2):
                self.parametersPanel.gridStdModel.setItem(row, 7, QStandardItem(""))
                # item["turndir"] = DBNull.Value;
            else:
                self.parametersPanel.gridStdModel.setItem(row, 7, QStandardItem("Right"))
            if (not self.parametersPanel.pnlCourse.Value != None):
                self.method_37();
        elif (sender == self.parametersPanel.pnlTime):
            self.parametersPanel.gridStdModel.setItem(row, 9, QStandardItem(str(Distance(self.parametersPanel.pnlTime.Value).NauticalMiles)))
            # item["timedist"] = new Distance(self.pnlTime.Value, DistanceUnits.NM);
        elif (sender == self.parametersPanel.pnlDist):
            self.parametersPanel.gridStdModel.setItem(row, 9, QStandardItem(str(self.parametersPanel.pnlDist.Value.NauticalMiles)))
            # item["timedist"] = self.pnlDist.Value;
        elif (sender == self.parametersPanel.pnlArcCen):
            position1 = self.parametersPanel.pnlArcCen.Point3d;
            self.parametersPanel.gridStdModel.setItem(row, 11, QStandardItem(self.parametersPanel.pnlArcCen.txtPointY.text()))
            self.parametersPanel.gridStdModel.setItem(row, 12, QStandardItem(self.parametersPanel.pnlArcCen.txtPointX.text()))
            # item["cenlat"] = Degrees.smethod_1(position1.XLat);
            # item["cenlon"] = Degrees.smethod_5(position1.YLon);
            if (not self.parametersPanel.pnlCourse.Value != None):
                self.method_37();
            if (not self.parametersPanel.pnlDist.Value.IsValid()):
                self.method_38();
        self.method_39();
        self.method_33();

        # self.parametersPanel.grid.setFocusPolicy(Qt.F)
        return;
class FlyOverType:
    Y = 1
    N = 0

class PathTerminator:
    Nothing = -1
    IF = 0
    TF = 1
    RF = 2
    HF = 3
    HA = 4
    HM = 5
    DF = 6
    FA = 7
    CF = 8
    PI = 9
    CA = 10
    CI = 11
    CD = 12
    CR = 13
    FC = 14
    FD = 15
    FM = 16
    AF = 17
    VD = 18
    VA = 19
    VM = 20
    VI = 21
    VR = 22
pathTerminatorValueList = ["None",
                            "IF",
                            "TF",
                            "RF",
                            "HF",
                            "HA",
                            "HM",
                            "DF",
                            "FA",
                            "CF",
                            "PI",
                            "CA",
                            "CI",
                            "CD",
                            "CR",
                            "FC",
                            "FD",
                            "FM",
                            "AF",
                            "VD",
                            "VA",
                            "VM",
                            "VI",
                            "VR"]
class PathTerminatorBase:
    Arinc424 = 0
    PansOps = 1

class ProcedureType:
    SID = 0
    STAR = 1
    Approach = 2
    MissedApproach = 3

class TurnDirectionType:
    Nothing = 2
    L = 1
    R = 0