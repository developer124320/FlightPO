# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HoldingRnav.ui'
#
# Created: Wed Nov 25 16:19:08 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.SpeedBoxPanel import SpeedBoxPanel, SpeedUnits
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PathTerminators(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(473, 580)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        Form.setFont(font)
        self.vlForm = QtGui.QVBoxLayout(Form)
        self.vlForm.setObjectName(_fromUtf8("vlForm"))


        self.gbGeneral = QtGui.QGroupBox(Form)
        self.gbGeneral.setObjectName(_fromUtf8("gbGeneral"))
        self.gbGeneral.setTitle("General")
        self.vl_gbGeneral = QtGui.QVBoxLayout(self.gbGeneral)
        self.vl_gbGeneral.setObjectName(_fromUtf8("vl_gbGeneral"))

        self.pnlProcType = ComboBoxPanel(self.gbGeneral)
        self.pnlProcType.Caption = "Procedure Type"
        self.vl_gbGeneral.addWidget(self.pnlProcType)

        self.pnlBasedOn = ComboBoxPanel(self.gbGeneral)
        self.pnlBasedOn.Caption = "Path Terminators Based On"
        self.vl_gbGeneral.addWidget(self.pnlBasedOn)
        self.vlForm.addWidget(self.gbGeneral)

        self.gbParameters = QtGui.QGroupBox(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.gbParameters.setFont(font)
        self.gbParameters.setObjectName(_fromUtf8("gbParameters"))
        self.gbParameters.setTitle("Path Terminators")
        self.vl_gbParameters = QtGui.QVBoxLayout(self.gbParameters)
        self.vl_gbParameters.setObjectName(_fromUtf8("vl_gbParameters"))

        self.pnlPT = ComboBoxPanel(self.gbParameters)
        self.pnlPT.Caption = "Type"
        self.vl_gbParameters.addWidget(self.pnlPT)

        self.pnlProperties = QtGui.QFrame(self.gbParameters)
        self.pnlProperties.setObjectName("pnlProperties")
        self.hl_pnlProperties = QtGui.QHBoxLayout(self.pnlProperties)
        self.hl_pnlProperties.setObjectName("hl_pnlProperties")
        # self.hl_pnlProperties.setMargin(0)
        # self.hl_pnlProperties.setSpacing(0)

        self.pnlLeft = QtGui.QFrame(self.pnlProperties)
        self.pnlLeft.setFrameShape(QtGui.QFrame.NoFrame)
        self.pnlLeft.setFrameShadow(QtGui.QFrame.Raised)
        self.pnlLeft.setObjectName("pnlLeft")
        self.vl_pnlLeft = QtGui.QVBoxLayout(self.pnlLeft)
        self.vl_pnlLeft.setObjectName("vl_pnlLeft")
        self.vl_pnlLeft.setMargin(0)
        self.vl_pnlLeft.setSpacing(0)

        self.gbWpt = QtGui.QGroupBox(self.pnlLeft)
        self.gbWpt.setObjectName("gbWpt")
        self.gbWpt.setTitle("Waypoint")
        self.vl_gbWpt = QtGui.QVBoxLayout(self.gbWpt)
        self.vl_gbWpt.setObjectName("vl_gbWpt")

        self.pnlWpt = PositionPanel(self.gbWpt, None, None, "Degree")
        self.pnlWpt.btnCalculater.hide()
        self.pnlWpt.showframe_ID()
        self.pnlWpt.hideframe_Altitude()
        self.pnlWpt.degreeFormat = "ddmmss.ssssH"
        self.vl_gbWpt.addWidget(self.pnlWpt)

        self.pnlFlyOver = ComboBoxPanel(self.gbWpt)
        self.pnlFlyOver.Caption = "Fly-over"
        self.pnlFlyOver.LabelWidth = 150
        self.vl_gbWpt.addWidget(self.pnlFlyOver)
        self.vl_pnlLeft.addWidget(self.gbWpt)

        self.pnlAltitude = AltitudeBoxPanel(self.pnlLeft)
        self.pnlAltitude.Caption = "Altitude Restriction"
        self.pnlAltitude.CaptionUnits = "ft"
        self.pnlAltitude.LabelWidth = 150
        self.vl_pnlLeft.addWidget(self.pnlAltitude)

        self.pnlSpeed = SpeedBoxPanel(self.pnlLeft, SpeedUnits.KTS)
        self.pnlSpeed.Caption = "Speed Limit"
        self.pnlSpeed.LabelWidth = 150
        self.vl_pnlLeft.addWidget(self.pnlSpeed)

        self.hl_pnlProperties.addWidget(self.pnlLeft)

        self.pnlRight = QtGui.QFrame(self.pnlProperties)
        self.pnlRight.setObjectName("pnlRight")
        self.pnlRight.setFrameShape(QtGui.QFrame.NoFrame)
        self.pnlRight.setFrameShadow(QtGui.QFrame.Raised)
        self.vl_pnlRight = QtGui.QVBoxLayout(self.pnlRight)
        self.vl_pnlRight.setObjectName("vl_pnlRight")
        self.vl_pnlRight.setMargin(0)
        self.vl_pnlRight.setSpacing(0)

        self.pnlCourse = TrackRadialBoxPanel(self.pnlRight)
        self.pnlCourse.Caption = "Course"
        self.pnlCourse.LabelWidth = 150
        self.vl_pnlRight.addWidget(self.pnlCourse)

        self.pnlTurnDir = ComboBoxPanel(self.pnlRight)
        self.pnlTurnDir.Caption = "Turn Direction"
        self.pnlTurnDir.LabelWidth = 150
        self.vl_pnlRight.addWidget(self.pnlTurnDir)

        self.pnlDist = DistanceBoxPanel(self.pnlRight, DistanceUnits.NM)
        self.pnlDist.Caption = "Distance"
        self.pnlDist.LabelWidth = 150
        self.vl_pnlRight.addWidget(self.pnlDist)

        self.pnlTime = NumberBoxPanel(self.pnlRight)
        self.pnlTime.CaptionUnits = "min"
        self.pnlTime.Caption = "Time"
        self.pnlTime.LabelWidth = 150
        self.vl_pnlRight.addWidget(self.pnlTime)

        self.pnlArcCen = PositionPanel(self.pnlRight, None, None, "Degree")
        self.pnlArcCen.groupBox.setTitle("Arc Center")
        self.pnlArcCen.btnCalculater.hide()
        self.pnlArcCen.hideframe_Altitude()
        self.pnlWpt.degreeFormat = "ddmmss.ssssH"
        self.vl_pnlRight.addWidget(self.pnlArcCen)

        self.hl_pnlProperties.addWidget(self.pnlRight)
        self.vl_gbParameters.addWidget(self.pnlProperties)

        self.frameResult = Frame(self.gbParameters, "HL")
        self.vl_gbParameters.addWidget(self.frameResult)

        self.grid = QtGui.QTableView(self.frameResult)
        self.grid.setObjectName("grid")
        self.frameResult.Add = self.grid

        self.lblError = QtGui.QLabel(self.gbParameters)
        self.lblError.setObjectName("lblError")
        self.lblError.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.lblError.setFont(font)
        palette = QtGui.QPalette();
        brush = QtGui.QBrush(QtGui.QColor(207, 56, 86, 255));
        # brush.setStyle(Qt::SolidPattern);
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush);
        # palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush2);
        # palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush1);
        self.lblError.setPalette(palette);
        self.vl_gbParameters.addWidget(self.lblError)

        self.gridStdModel = QtGui.QStandardItemModel()
        self.gridStdModel.setHorizontalHeaderLabels(["#",
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
        # self.gridSelectionModel = QtGui.QSortFilterProxyModel()
        #
        # self.gridSelectionModel.setSourceModel(self.gridStdModel)
        self.grid.setModel(self.gridStdModel)
        self.grid.setSelectionBehavior(1)
        # self.grid.setSelectionMode(1)


        self.pnlTreeViewActions = QtGui.QFrame(self.frameResult)
        self.pnlTreeViewActions.setObjectName("pnlTreeViewActions")
        self.vl_pnlTreeViewActions = QtGui.QVBoxLayout(self.pnlTreeViewActions)
        self.vl_pnlTreeViewActions.setObjectName("vl_pnlTreeViewActions")

        self.btnAdd = QtGui.QPushButton(self.pnlTreeViewActions)
        self.btnAdd.setObjectName("btnAdd")
        self.btnAdd.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.vl_pnlTreeViewActions.addWidget(self.btnAdd)

        self.btnRemove = QtGui.QPushButton(self.pnlTreeViewActions)
        self.btnRemove.setObjectName("btnRemove")
        self.btnRemove.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRemove.setIcon(icon)
        self.vl_pnlTreeViewActions.addWidget(self.btnRemove)

        self.btnUp = QtGui.QPushButton(self.pnlTreeViewActions)
        self.btnUp.setObjectName("btnUp")
        self.btnUp.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUp.setIcon(icon)
        self.vl_pnlTreeViewActions.addWidget(self.btnUp)

        self.btnDown = QtGui.QPushButton(self.pnlTreeViewActions)
        self.btnDown.setObjectName("btnDown")
        self.btnDown.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDown.setIcon(icon)
        self.vl_pnlTreeViewActions.addWidget(self.btnDown)

        self.frameResult.Add = self.pnlTreeViewActions

        self.vlForm.addWidget(self.gbParameters)


