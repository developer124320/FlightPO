# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QTreeView, QDialog, QMessageBox, QDialogButtonBox,\
    QPushButton, QIcon, QPixmap
from PyQt4.QtCore import QSizeF, SIGNAL, QObject, QModelIndex
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.StandardItemModel import StandardItemModel, QStandardItem
from FlightPlanner.Panels.SpeedBoxPanel import SpeedBoxPanel, SpeedUnits
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel
from FlightPlanner.types import CodeIapFixAixm, CodeTypeProcPathAixm,\
    CodePhaseProcAixm, CodeTypeCourseAixm, CodeDirTurnAixm, CodeDescrDistVerAixm, CodeDistVerAixm,\
    CodeSpeedRefAixm, CodeTypeFlyByAixm, CodeRepAtcAixm, ProcEntityListType, ListInsertPosition
from FlightPlanner.helpers import EnumHelper
from FlightPlanner.Dialogs.DlgAixmSelectPosition import DlgAixmSelectPosition
from FlightPlanner.Dialogs.DlgAixmInsertLeg import DlgAixmInsertLeg
from Type.String import String
from Type.DataBaseProcedureLegs import DataBaseProcedureLeg, DataBaseProcedureLegsEx
from Type.enum.enum import Enum
import math, define, thread, time, threading



class DlgAixmProcLegs(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136);
        self.setWindowTitle("Procedure Legs (AIXM 4.5)")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));

        self.gbAll = GroupBox(self, "HL")
        self.gbAll.Caption = "Legs"
        verticalLayoutDlg.addWidget(self.gbAll)

        self.trvLegs = QTreeView(self.gbAll)
        self.trvLegsStdModel = StandardItemModel()
        self.trvLegs.setModel(self.trvLegsStdModel)
        self.gbAll.Add = self.trvLegs

        self.flowLayoutPanel1 = Frame(self.gbAll)
        self.gbAll.Add = self.flowLayoutPanel1

        self.btnAdd = QPushButton(self.flowLayoutPanel1)
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/add.png"), QIcon.Normal, QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.flowLayoutPanel1.Add = self.btnAdd

        self.btnRemove = QPushButton(self.flowLayoutPanel1)
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/remove.png"), QIcon.Normal, QIcon.Off)
        self.btnRemove.setIcon(icon)
        self.flowLayoutPanel1.Add = self.btnRemove

        self.btnMoveUp = QPushButton(self.flowLayoutPanel1)
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/up.png"), QIcon.Normal, QIcon.Off)
        self.btnMoveUp.setIcon(icon)
        self.flowLayoutPanel1.Add = self.btnMoveUp

        self.btnMoveDown = QPushButton(self.flowLayoutPanel1)
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/down.png"), QIcon.Normal, QIcon.Off)
        self.btnMoveDown.setIcon(icon)
        self.flowLayoutPanel1.Add = self.btnMoveDown

        self.scrollBox = Frame(self.gbAll)
        self.gbAll.Add = self.scrollBox

        self.gbFix = GroupBox(self.scrollBox)
        self.gbFix.Caption = "Fix"
        self.scrollBox.Add = self.gbFix

        self.cmbFixPos = ComboBoxPanel(self.gbFix)
        self.cmbFixPos.Caption = "Position"
        self.cmbFixPos.Button = "coordinate_capture.png"
        self.gbFix.Add = self.cmbFixPos

        self.pnlCodeRoleFix = ComboBoxPanel(self.gbFix)
        self.pnlCodeRoleFix.Caption = "Type"
        self.gbFix.Add = self.pnlCodeRoleFix

        self.gbAttributes = GroupBox(self.scrollBox)
        self.gbAttributes.Caption = "Attributes"
        self.scrollBox.Add = self.gbAttributes

        self.cmbRecommendedEnt = ComboBoxPanel(self.gbAttributes)
        self.cmbRecommendedEnt.Caption = "Recommended Navigational Aid"
        self.gbAttributes.Add = self.cmbRecommendedEnt

        self.pnlCodePhase = ComboBoxPanel(self.gbAttributes)
        self.pnlCodePhase.Caption = "Fligh Phase"
        self.gbAttributes.Add = self.pnlCodePhase

        self.pnlCodeType = ComboBoxPanel(self.gbAttributes)
        self.pnlCodeType.Caption = "Leg Type"
        self.gbAttributes.Add = self.pnlCodeType

        self.pnlLegVOR = Frame(self.gbAttributes, "HL")
        self.gbAttributes.Add = self.pnlLegVOR

        self.cmbCodeTypeCourse = ComboBoxPanel(self.pnlLegVOR)
        self.cmbCodeTypeCourse.Caption = "Course Angle (" + define._degreeStr + ")"
        self.pnlLegVOR.Add = self.cmbCodeTypeCourse

        self.txtValCourse = TrackRadialBoxPanel(self.pnlLegVOR)
        self.txtValCourse.LabelWidth = 0
        self.pnlLegVOR.Add = self.txtValCourse

        self.pnlCodeDirTurn = ComboBoxPanel(self.gbAttributes)
        self.pnlCodeDirTurn.Caption = "Turn Direction"
        self.gbAttributes.Add = self.pnlCodeDirTurn

        self.pnlTurnValid = ComboBoxPanel(self.gbAttributes)
        self.pnlTurnValid.Caption = "Fly-By"
        self.gbAttributes.Add = self.pnlTurnValid

        self.cmbCenter = ComboBoxPanel(self.gbAttributes)
        self.cmbCenter.Caption = "Center"
        self.cmbCenter.Button = "coordinate_capture.png"
        self.gbAttributes.Add = self.cmbCenter

        self.pnlValBankAngle = NumberBoxPanel(self.gbAttributes)
        self.pnlValBankAngle.Caption = "Bank Angle (" + define._degreeStr + ")"
        self.gbAttributes.Add = self.pnlValBankAngle

        self.pnlCodeDescrDistVer = ComboBoxPanel(self.gbAttributes)
        self.pnlCodeDescrDistVer.Caption = "Altitude Interpretation"
        self.gbAttributes.Add = self.pnlCodeDescrDistVer

        self.pnlVerDistLower = Frame(self.gbAttributes, "HL")
        self.gbAttributes.Add = self.pnlVerDistLower

        self.cmbDistVerLower = ComboBoxPanel(self.pnlVerDistLower)
        self.cmbDistVerLower.CaptionUnits = "ft"
        self.cmbDistVerLower.Caption = "Lower Altitude Limit"
        self.pnlVerDistLower.Add = self.cmbDistVerLower

        self.txtDistVerLower = AltitudeBoxPanel(self.pnlVerDistLower)
        self.txtDistVerLower.CaptionUnits = "ft"
        self.txtDistVerLower.LabelWidth = 0
        self.pnlVerDistLower.Add = self.txtDistVerLower

        self.pnlDistVerUpper = Frame(self.gbAttributes, "HL")
        self.gbAttributes.Add = self.pnlDistVerUpper

        self.cmbDistVerUpper = ComboBoxPanel(self.pnlDistVerUpper)
        self.cmbDistVerUpper.CaptionUnits = "ft"
        self.cmbDistVerUpper.Caption = "Upper Altitude Limit"
        self.pnlDistVerUpper.Add = self.cmbDistVerUpper

        self.txtDistVerUpper = AltitudeBoxPanel(self.pnlDistVerUpper)
        self.txtDistVerUpper.CaptionUnits = "ft"
        self.txtDistVerUpper.LabelWidth = 0
        self.pnlDistVerUpper.Add = self.txtDistVerUpper

        self.pnlValVerAngle = NumberBoxPanel(self.gbAttributes)
        self.pnlValVerAngle.Caption = "Climb / Descent Angle [+/-] (" + define._degreeStr + ")"
        self.gbAttributes.Add = self.pnlValVerAngle

        self.tableLayoutPanel2 = Frame(self.gbAttributes, "HL")
        self.gbAttributes.Add = self.tableLayoutPanel2

        self.cmbCodeSpeedRef = ComboBoxPanel(self.tableLayoutPanel2)
        self.cmbCodeSpeedRef.CaptionUnits = "kts"
        self.cmbCodeSpeedRef.Caption = "Speed Restriction"
        self.tableLayoutPanel2.Add = self.cmbCodeSpeedRef

        self.txtValSpeed = SpeedBoxPanel(self.tableLayoutPanel2)
        self.txtValSpeed.LabelWidth = 0
        self.tableLayoutPanel2.Add = self.txtValSpeed

        self.pnlValDist = DistanceBoxPanel(self.gbAttributes, DistanceUnits.NM)
        self.pnlValDist.Caption = "Segment Length"
        self.pnlValDist.Button = None
        self.gbAttributes.Add = self.pnlValDist

        self.pnlValDur = NumberBoxPanel(self.gbAttributes)
        self.pnlValDur.CaptionUnits = "min"
        self.pnlValDur.Caption = "Duration"
        self.gbAttributes.Add = self.pnlValDur

        self.pnlCodeRepAtc = ComboBoxPanel(self.gbAttributes)
        self.pnlCodeRepAtc.Caption = "ATC Reporting"
        self.gbAttributes.Add = self.pnlCodeRepAtc

        self.pnlValTheta = TrackRadialBoxPanel(self.gbAttributes)
        self.pnlValTheta.Caption = "Magnetic Bearing / Radial from Recommended Nav. Aid"
        self.pnlValTheta.LabelWidth = 350
        self.gbAttributes.Add = self.pnlValTheta

        self.pnlValRho = DistanceBoxPanel(self.gbAttributes, DistanceUnits.NM)
        self.pnlValRho.Caption = "Distance from Recommended Nav. Aid"
        self.pnlValRho.LabelWidth = 350
        self.gbAttributes.Add = self.pnlValRho

        self.txtRemarks = TextBoxPanel(self.gbAttributes, True)
        self.txtRemarks.Caption = "Remarks"
        self.gbAttributes.Add = self.txtRemarks

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)



        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

        self.trvLegs.pressed.connect(self.trvLegs_pressed)

        self.data = None
        self.legs = None
        self.aerodrome = None;
        self.magnVar = 0.0



        for value in CodeIapFixAixm.Items:
            self.pnlCodeRoleFix.Add(value);
        for codeTypeProcPathAixm in CodeTypeProcPathAixm.Items:
            self.pnlCodeType.Add(codeTypeProcPathAixm);
        for codePhaseProcAixm in CodePhaseProcAixm.Items:
            self.pnlCodePhase.Add(codePhaseProcAixm);
        for codeTypeCourseAixm in CodeTypeCourseAixm.Items:
            self.cmbCodeTypeCourse.Add(codeTypeCourseAixm);
        for codeDirTurnAixm in CodeDirTurnAixm.Items:
            self.pnlCodeDirTurn.Add(codeDirTurnAixm);
        for codeDescrDistVerAixm in CodeDescrDistVerAixm.Items:
            self.pnlCodeDescrDistVer.Add(codeDescrDistVerAixm);
        for codeDistVerAixm in CodeDistVerAixm.Items:
            self.cmbDistVerLower.Add(codeDistVerAixm);
        for value1 in CodeDistVerAixm.Items:
            self.cmbDistVerUpper.Add(value1);
        for codeSpeedRefAixm in CodeSpeedRefAixm.Items:
            self.cmbCodeSpeedRef.Add(codeSpeedRefAixm);
        for codeTypeFlyByAixm in CodeTypeFlyByAixm.Items:
            self.pnlTurnValid.Add(codeTypeFlyByAixm);
        for codeRepAtcAixm in CodeRepAtcAixm.Items:
            self.pnlCodeRepAtc.Add(codeRepAtcAixm);
        self.method_6()

        self.connect(self.pnlValRho, SIGNAL("Event_0"), self.pnlValRho_Event_0)
        self.connect(self.pnlValTheta, SIGNAL("Event_0"), self.pnlValTheta_Event_0)
        self.connect(self.pnlCodeRepAtc, SIGNAL("Event_0"), self.pnlCodeRepAtc_Event_0)
        self.connect(self.pnlValDur, SIGNAL("Event_0"), self.pnlValDur_Event_0)
        self.connect(self.pnlValDist, SIGNAL("Event_0"), self.pnlValDist_Event_0)
        self.connect(self.cmbCodeSpeedRef, SIGNAL("Event_0"), self.cmbCodeSpeedRef_Event_0)
        self.connect(self.txtValSpeed, SIGNAL("Event_0"), self.txtValSpeed_Event_0)
        self.connect(self.txtDistVerUpper, SIGNAL("Event_0"), self.txtDistVerUpper_Event_0)
        self.connect(self.cmbDistVerUpper, SIGNAL("Event_0"), self.cmbDistVerUpper_Event_0)
        self.connect(self.txtDistVerLower, SIGNAL("Event_0"), self.txtDistVerLower_Event_0)

        self.connect(self.cmbDistVerLower, SIGNAL("Event_0"), self.cmbDistVerLower_Event_0)
        self.connect(self.pnlValBankAngle, SIGNAL("Event_0"), self.pnlValBankAngle_Event_0)
        self.connect(self.cmbCenter, SIGNAL("Event_0"), self.cmbCenter_Event_0)
        self.connect(self.pnlTurnValid, SIGNAL("Event_0"), self.pnlTurnValid_Event_0)
        self.connect(self.pnlCodeDirTurn, SIGNAL("Event_0"), self.pnlCodeDirTurn_Event_0)
        self.connect(self.cmbCodeTypeCourse, SIGNAL("Event_0"), self.cmbCodeTypeCourse_Event_0)
        self.connect(self.txtValCourse, SIGNAL("Event_0"), self.txtValCourse_Event_0)
        self.connect(self.pnlCodeType, SIGNAL("Event_0"), self.pnlCodeType_Event_0)
        self.connect(self.pnlCodePhase, SIGNAL("Event_0"), self.pnlCodePhase_Event_0)
        self.connect(self.pnlCodeRoleFix, SIGNAL("Event_0"), self.pnlCodeRoleFix_Event_0)
        self.connect(self.txtRemarks, SIGNAL("Event_0"), self.txtRemarks_Event_0)
        self.connect(self.cmbRecommendedEnt, SIGNAL("Event_0"), self.cmbRecommendedEnt_Event_0)

        self.connect(self.cmbFixPos, SIGNAL("Event_0"), self.cmbFixPos_Event_0)
        self.connect(self.cmbCenter, SIGNAL("Event_3"), self.method_14)
        self.connect(self.cmbFixPos, SIGNAL("Event_3"), self.method_13)

        self.btnAdd.clicked.connect(self.btnAdd_Click)
        self.btnMoveDown.clicked.connect(self.btnMoveDown_Click)
        self.btnMoveUp.clicked.connect(self.btnMoveUp_Click)
        self.btnRemove.clicked.connect(self.btnRemove_Click)

        self.trvLegs.setHeaderHidden(True)

        if self.trvLegsStdModel.rowCount() > 0:
            self.trvLegs.setCurrentIndex(self.trvLegsStdModel.index(0,0))
            self.method_8()
        # rootModelIndex = self.trvLegs.rootIndex()
        # rootItem = self.trvLegsStdModel.itemFromIndex(rootModelIndex)
        # rootItem.setText("Legs")
    def btnAdd_Click(self):
        if (len(self.trvLegs.selectedIndexes()) == 0 and not self.method_5()):
            return;
        listInsertPosition = ListInsertPosition.Append;
        resultDlg, listInsertPosition = DlgAixmInsertLeg.smethod_0(listInsertPosition)
        if (self.trvLegsStdModel.rowCount() > 0 and not resultDlg):
            return;
        count = self.trvLegsStdModel.rowCount()
        if (listInsertPosition == ListInsertPosition.Before):
            count = self.trvLegs.selectedIndexes()[0].row();
        elif (listInsertPosition == ListInsertPosition.After):
            count = self.trvLegs.selectedIndexes()[0].row() + 1;
        self.trvLegsStdModel.setItem(self.trvLegsStdModel.rowCount(), QStandardItem(str(self.trvLegsStdModel.rowCount() + 1)));
        self.legs.insert(count, DataBaseProcedureLeg());
        self.trvLegs.setCurrentIndex(self.trvLegsStdModel.index(count, 0))
        self.trvLegs_pressed()
    def btnMoveDown_Click(self):
        if (len(self.trvLegs.selectedIndexes()) == 0):
            return;
        index = self.trvLegs.selectedIndexes()[0].row();
        item = self.legs[index];
        self.legs.pop(index);
        self.legs.insert(index + 1, item);
        self.trvLegs.setCurrentIndex(self.trvLegsStdModel.index(index + 1, 0))
        self.trvLegs_pressed()
    def btnMoveUp_Click(self):
        if (len(self.trvLegs.selectedIndexes()) == 0):
            return;
        index = self.trvLegs.selectedIndexes()[0].row();
        item = self.legs[index];
        self.legs.pop(index);
        self.legs.insert(index - 1, item);
        self.trvLegs.setCurrentIndex(self.trvLegsStdModel.index(index - 1, 0))
        self.trvLegs_pressed()
    def btnRemove_Click(self):
        item = None;
        if (len(self.trvLegs.selectedIndexes()) == 0):
            return;
        if (QMessageBox.question(self, "Question", "Are you sure you want to delete the selected procedure leg?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
            index = self.trvLegs.selectedIndexes()[0].row();
            self.legs.pop(index);
            self.trvLegsStdModel.takeRow(self.trvLegsStdModel.rowCount() - 1);
            if (index >= self.trvLegsStdModel.rowCount() - 1):
                index -= 1;
            # treeView = self.trvLegs;
            # if (index >= 0):
            if self.trvLegsStdModel.rowCount() > 0 and index < 0:
                index = 0
            self.trvLegs.setCurrentIndex(self.trvLegsStdModel.index(index, 0))

            self.trvLegs_pressed()
    def cmbRecommendedEnt_Event_0(self):
        self.method_10(self.cmbRecommendedEnt)
    def txtRemarks_Event_0(self):
        self.method_10(self.txtRemarks)
    def cmbFixPos_Event_0(self):
        self.method_10(self.cmbFixPos)
    def cmbDistVerLower_Event_0(self):
        self.method_10(self.cmbDistVerLower)
    def pnlValBankAngle_Event_0(self):
        self.method_10(self.pnlValBankAngle)
    def cmbCenter_Event_0(self):
        self.method_10(self.cmbCenter)
    def pnlTurnValid_Event_0(self):
        self.method_10(self.pnlTurnValid)
    def pnlCodeDirTurn_Event_0(self):
        self.method_10(self.pnlCodeDirTurn)
    def cmbCodeTypeCourse_Event_0(self):
        self.method_10(self.cmbCodeTypeCourse)
    def txtValCourse_Event_0(self):
        self.method_10(self.txtValCourse)
    def pnlCodeType_Event_0(self):
        self.method_10(self.pnlCodeType)
    def pnlCodePhase_Event_0(self):
        self.method_10(self.pnlCodePhase)
    def pnlCodeRoleFix_Event_0(self):
        self.method_10(self.pnlCodeRoleFix)
    def txtDistVerLower_Event_0(self):
        self.method_10(self.txtDistVerLower)
    def cmbDistVerUpper_Event_0(self):
        self.method_10(self.cmbDistVerUpper)
    def txtDistVerUpper_Event_0(self):
        self.method_10(self.txtDistVerUpper)
    def txtValSpeed_Event_0(self):
        self.method_10(self.txtValSpeed)
    def cmbCodeSpeedRef_Event_0(self):
        self.method_10(self.cmbCodeSpeedRef)
    def pnlValDist_Event_0(self):
        self.method_10(self.pnlValDist)
    def pnlValDur_Event_0(self):
        self.method_10(self.pnlValDur)
    def pnlCodeRepAtc_Event_0(self):
        self.method_10(self.pnlCodeRepAtc)
    def pnlValTheta_Event_0(self):
        self.method_10(self.pnlValTheta)
    def pnlValRho_Event_0(self):
        self.method_10(self.pnlValRho)
    def trvLegs_pressed(self):
        self.method_6()
        self.method_8()
    def acceptDlg(self):
        self.legs.refresh()
        QObject.emit(self, SIGNAL("DlgAixmProcLegs_Smethod_0_Event"), self.legs, self.data)
        self.accept()
    
    def method_5(self):
        pass
    def method_6(self):
        self.btnOK = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)
        self.btnOK.setEnabled(len(self.trvLegs.selectedIndexes()) > 0)
        self.btnRemove.setEnabled(len(self.trvLegs.selectedIndexes()) > 0);
        self.btnMoveUp.setEnabled((len(self.trvLegs.selectedIndexes()) > 0 and self.trvLegs.selectedIndexes()[0].row() != 0) and True or False);
        self.btnMoveDown.setEnabled((len(self.trvLegs.selectedIndexes()) <=  0 or self.trvLegsStdModel.rowCount() <= 0) and False or ((len(self.trvLegs.selectedIndexes()) >  0) and self.trvLegs.selectedIndexes()[0].row() < self.trvLegsStdModel.rowCount() - 1));
	
    def method_7(self):
        for i in range(self.legs.Count):
            num = i + 1;
            self.trvLegsStdModel.setItem(i, QStandardItem(str(num)));
        self.method_6()
        # if (self.trvLegsStdModel.rowCount() > 0):
        #     self.trvLegs.setCurrentIndex() = self.trvLegs.Nodes[0];
    def method_8(self):
        if (len(self.trvLegs.selectedIndexes()) <= 0):
            self.scrollBox.Enabled = False;
            self.cmbFixPos.SelectedIndex = -1;
            self.pnlCodeRoleFix.SelectedIndex = -1;
            self.cmbRecommendedEnt.SelectedIndex = -1;
            self.pnlCodePhase.SelectedIndex = -1;
            self.pnlCodeType.SelectedIndex = -1;
            self.cmbCodeTypeCourse.SelectedIndex = -1;
            self.txtValCourse.Value = 0;
            self.pnlCodeDirTurn.SelectedIndex = -1;
            self.cmbCenter.SelectedIndex = -1;
            self.pnlTurnValid.SelectedIndex = -1;
            self.pnlValBankAngle.Value = 0;
            self.pnlCodeDescrDistVer.SelectedIndex = -1;
            self.cmbDistVerLower.SelectedIndex = -1;
            self.txtDistVerLower.Value = None;
            self.cmbDistVerUpper.SelectedIndex = -1;
            self.txtDistVerUpper.Value = None;
            self.pnlValVerAngle.Value = None;
            self.cmbCodeSpeedRef.SelectedIndex = -1;
            self.txtValSpeed.Value = None;
            self.pnlValDist.Value = None;
            self.pnlValDur.Value = 0;
            self.pnlCodeRepAtc.SelectedIndex = -1;
            self.pnlValTheta.Value = 0;
            self.pnlValRho.Value = None;
            self.txtRemarks.Value = ""
            return;
        self.scrollBox.Enabled = True;
        item = self.legs[self.trvLegs.selectedIndexes()[0].row()];
        if (item.PointEnt == None):
            self.cmbFixPos.SelectedIndex = -1;
        else:
            self.cmbFixPos.SelectedIndex = self.cmbFixPos.IndexOf(item.PointEnt);
        self.pnlCodeRoleFix.SelectedIndex = self.method_9(self.pnlCodeRoleFix.Items, item.CodeRoleFix);
        if (item.RecommendedEnt == None):
            self.cmbRecommendedEnt.SelectedIndex = -1;
        else:
            self.cmbRecommendedEnt.SelectedIndex = self.cmbRecommendedEnt.IndexOf(item.RecommendedEnt);
        self.pnlCodePhase.SelectedIndex = self.method_9(self.pnlCodePhase.Items, item.CodePhase);
        self.pnlCodeType.SelectedIndex = self.method_9(self.pnlCodeType.Items, item.CodeType);
        self.cmbCodeTypeCourse.SelectedIndex = self.method_9(self.cmbCodeTypeCourse.Items, item.CodeTypeCourse);
        self.txtValCourse.Value = item.ValCourse;
        self.pnlCodeDirTurn.SelectedIndex = self.method_9(self.pnlCodeDirTurn.Items, item.CodeDirTurn);
        if (item.CenterEnt == None):
            self.cmbCenter.SelectedIndex = -1;
        else:
            self.cmbCenter.SelectedIndex = self.cmbCenter.IndexOf(item.CenterEnt);
        self.pnlTurnValid.SelectedIndex = self.method_9(self.pnlTurnValid.Items, item.CodeTurnValid)
        self.pnlValBankAngle.Value = item.ValBankAngle;
        self.pnlCodeDescrDistVer.SelectedIndex = self.method_9(self.pnlCodeDescrDistVer.Items, item.CodeDescrDistVer)
        self.cmbDistVerLower.SelectedIndex = self.method_9(self.cmbDistVerLower.Items, item.CodeDistVerLower)
        self.txtDistVerLower.Value = item.ValDistVerLower;
        self.cmbDistVerUpper.SelectedIndex = self.method_9(self.cmbDistVerUpper.Items, item.CodeDistVerUpper)
        self.txtDistVerUpper.Value = item.ValDistVerUpper;
        self.pnlValVerAngle.Value = item.ValVerAngle;
        self.cmbCodeSpeedRef.SelectedIndex = self.method_9(self.cmbCodeSpeedRef.Items, item.CodeSpeedRef)
        self.txtValSpeed.Value = item.ValSpeedLimit;
        self.pnlValDist.Value = item.ValDist;
        self.pnlValDur.Value = item.ValDur;
        self.pnlCodeRepAtc.SelectedIndex = self.method_9(self.pnlCodeRepAtc.Items, item.CodeRepAtc)
        self.pnlValTheta.Value = item.ValTheta;
        self.pnlValRho.Value = item.ValRho;
        self.txtRemarks.Value = item.TxtRmk;
        self.method_6()

    def method_9(self, ilist_0, string_0):
        for i in range(len(ilist_0)):
            if (ilist_0[i] == string_0):
                return i;
        return -1;
    def method_10(self, sender):
        if (len(self.trvLegs.selectedIndexes()) == 0):
            return;
        item = self.legs[self.trvLegs.selectedIndexes()[0].row()];
        if (sender == self.cmbFixPos):
            item.PointEnt = self.cmbFixPos.SelectedItem;
        if (sender == self.pnlCodeRoleFix):
            item.CodeRoleFix = self.pnlCodeRoleFix.SelectedItem;
        if (sender == self.cmbRecommendedEnt):
            item.RecommendedEnt = self.cmbRecommendedEnt.SelectedItem
        if (sender == self.pnlCodePhase):
            item.CodePhase = self.pnlCodePhase.SelectedItem
        if (sender == self.pnlCodeType):
            item.CodeType = self.pnlCodeType.SelectedItem
        if (sender == self.cmbCodeTypeCourse):
            item.CodeTypeCourse = self.cmbCodeTypeCourse.SelectedItem
        if (sender == self.txtValCourse):
            item.ValCourse = self.txtValCourse.Value;
        if (sender == self.pnlCodeDirTurn):
            item.CodeDirTurn = self.pnlCodeDirTurn.SelectedItem
        if (sender == self.cmbCenter):
            item.CenterEnt = self.cmbCenter.SelectedItem;
            return;
        if (sender == self.pnlTurnValid):
            item.CodeTurnValid = self.pnlTurnValid.SelectedItem
            return;
        if (sender == self.pnlValBankAngle):
            item.ValBankAngle = self.pnlValBankAngle.Value;
            return;
        if (sender == self.pnlCodeDescrDistVer):
            item.CodeDescrDistVer = self.pnlTurnValid.SelectedItem
            return;
        if (sender == self.cmbDistVerLower):
            item.CodeDistVerLower = self.cmbDistVerLower.SelectedItem
            return;
        if (sender == self.txtDistVerLower):
            item.ValDistVerLower = self.txtDistVerLower.Value;
            return;
        if (sender == self.cmbDistVerUpper):
            item.CodeDistVerUpper = self.cmbDistVerUpper.SelectedItem
            return;
        if (sender == self.txtDistVerUpper):
            item.ValDistVerUpper = self.txtDistVerUpper.Value;
            return;
        if (sender == self.pnlValVerAngle):
            item.ValVerAngle = self.pnlValVerAngle.Value;
            return;
        if (sender == self.cmbCodeSpeedRef):
            item.CodeSpeedRef = self.cmbCodeSpeedRef.SelectedItem
            return;
        if (sender == self.txtValSpeed):
            item.ValSpeedLimit = self.txtValSpeed.Value;
            return;
        if (sender == self.pnlValDist):
            item.ValDist = self.pnlValDist.Value;
            return;
        if (sender == self.pnlValDur):
            item.ValDur = self.pnlValDur.Value;
            return;
        if (sender == self.pnlCodeRepAtc):
            item.CodeRepAtc = self.pnlCodeRepAtc.SelectedItem
            return;
        if (sender == self.pnlValTheta):
            item.ValTheta = self.pnlValTheta.Value;
            return;
        if (sender == self.pnlValRho):
            item.ValRho = self.pnlValRho.Value;
            return;
        if (sender == self.txtRemarks):
            item.TxtRmk = self.txtRemarks.Value;
    def method_13(self):
        point3d = None;
        procEntityBase = None;
        selectTool = DlgAixmSelectPosition.smethod_0(self.data, point3d, ProcEntityListType.Fixes)
        QObject.connect(selectTool, SIGNAL("DlgAixmSelectPosition_Smethod_0_Event"), self.method_13_Event)
    def method_13_Event(self, flag, procEntityBase):
        # flag, procEntityBase = DlgAixmSelectPosition.smethod_0(self.data, point3d, ProcEntityListType.Fixes)
        if (flag and procEntityBase != None):
            if (not self.cmbFixPos.Contains(procEntityBase)):
                self.cmbFixPos.Add(procEntityBase);
            self.cmbFixPos.SelectedIndex = self.cmbFixPos.IndexOf(procEntityBase);
            self.method_10(self.cmbFixPos);

    def method_14(self):
        point3d = None;
        procEntityBase = None;
        selectTool = DlgAixmSelectPosition.smethod_0(self.data, point3d, ProcEntityListType.Centers)
        QObject.connect(selectTool, SIGNAL("DlgAixmSelectPosition_Smethod_0_Event"), self.method_14_Event)
    def method_14_Event(self, flag, procEntityBase):
        # flag, procEntityBase = DlgAixmSelectPosition.smethod_0(self.data, point3d, ProcEntityListType.Centers)
        if (flag and procEntityBase != None):
            if (not self.cmbCenter.Contains(procEntityBase)):
                self.cmbCenter.Add(procEntityBase);
            self.cmbCenter.SelectedIndex = self.cmbCenter.IndexOf(procEntityBase);
            self.method_10(self.cmbCenter);
    @staticmethod
    def smethod_0(parent, dataBaseProcedureLegs_0, dataBaseProcedureData_0, procEntityAHP_0):
        flag = False
        dlgAixmProcLeg = DlgAixmProcLegs(parent)
        dlgAixmProcLeg.legs = dataBaseProcedureLegs_0;
        dlgAixmProcLeg.data = dataBaseProcedureData_0;
        if (procEntityAHP_0 != None):
            dlgAixmProcLeg.aerodrome = procEntityAHP_0;
            dlgAixmProcLeg.magnVar = procEntityAHP_0.ValMagVar;
        dataBaseProcedureData_0.method_59(dlgAixmProcLeg.cmbFixPos, ProcEntityListType.Fixes);
        dataBaseProcedureData_0.method_59(dlgAixmProcLeg.cmbCenter, ProcEntityListType.Centers);
        dataBaseProcedureData_0.method_59(dlgAixmProcLeg.cmbRecommendedEnt, ProcEntityListType.RecommendedNavAids);
        if (dlgAixmProcLeg.legs.Count == 0):
            dlgAixmProcLeg.legs.Add(DataBaseProcedureLeg());

        dlgAixmProcLeg.method_7()
        if dlgAixmProcLeg.trvLegsStdModel.rowCount() > 0:
            dlgAixmProcLeg.trvLegs.setCurrentIndex(dlgAixmProcLeg.trvLegsStdModel.index(0,0))
            dlgAixmProcLeg.method_6()

        dlgAixmProcLeg.method_8();
        dlgAixmProcLeg.show()
        return dlgAixmProcLeg
        # while True:
        #     if dlgAixmProcLeg.result() == 1:
        #         return True;
        #     else:
        #         threading._sleep(0.1)







