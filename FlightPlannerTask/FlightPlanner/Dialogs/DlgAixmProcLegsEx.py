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
    CodePathTypeAixm, CodeTypeCourseAixm, CodeDirTurnAixm, CodeDescrDistVerAixm, CodeDistVerAixm,\
    CodeSpeedRefAixm, CodeTypeFlyByAixm, CodeRepAtcAixm, ProcEntityListType, CodeLegTypeAixm,\
    ListInsertPosition
from FlightPlanner.Dialogs.DlgAixmInsertLeg import DlgAixmInsertLeg
from FlightPlanner.Dialogs.DlgAixmSelectPosition import DlgAixmSelectPosition
from Type.DataBaseProcedureLegs import DataBaseProcedureLegEx
from Type.String import String
from Type.DataBaseProcedureLegs import DataBaseProcedureLeg, DataBaseProcedureLegsEx
from Type.enum.enum import Enum
import math, define, thread, time, threading



class DlgAixmProcLegsEx(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136);
        self.setWindowTitle("Procedure Legs (AIXM 4.5+)")
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

        self.gbPosition = GroupBox(self.scrollBox)
        self.gbPosition.Caption = "Fix"
        self.scrollBox.Add = self.gbPosition

        self.cmbPosUid = ComboBoxPanel(self.gbPosition)
        self.cmbPosUid.Caption = "Position"
        self.cmbPosUid.Button = "coordinate_capture.png"
        self.gbPosition.Add = self.cmbPosUid

        self.gbAttributes = GroupBox(self.scrollBox)
        self.gbAttributes.Caption = "Attributes"
        self.scrollBox.Add = self.gbAttributes

        self.pnlPathType = ComboBoxPanel(self.gbAttributes)
        self.pnlPathType.Caption = "Path Type"
        self.gbAttributes.Add = self.pnlPathType

        self.pnlLegType = ComboBoxPanel(self.gbAttributes)
        self.pnlLegType.Caption = "Leg Type"
        self.gbAttributes.Add = self.pnlLegType

        self.cmbCenUid = ComboBoxPanel(self.gbAttributes)
        self.cmbCenUid.Caption = "Center"
        self.cmbCenUid.Button = "coordinate_capture.png"
        self.gbAttributes.Add = self.cmbCenUid

        self.pnlFlyBy = ComboBoxPanel(self.gbAttributes)
        self.pnlFlyBy.Caption = "Fly-By"
        self.gbAttributes.Add = self.pnlFlyBy

        self.pnlMinAlt = AltitudeBoxPanel(self.gbAttributes)
        self.pnlMinAlt.CaptionUnits = "ft"
        self.pnlMinAlt.Caption = "Minimum Altitude"
        self.gbAttributes.Add = self.pnlMinAlt

        self.pnlSegLength = DistanceBoxPanel(self.gbAttributes, DistanceUnits.NM)
        self.pnlSegLength.Caption = "Segment Length"
        self.gbAttributes.Add = self.pnlSegLength

        self.pnlCourse = TrackRadialBoxPanel(self.gbAttributes)
        self.pnlCourse.Caption = "Course"
        self.gbAttributes.Add = self.pnlCourse

        self.pnlLegVOR = Frame(self.gbAttributes)
        self.gbAttributes.Add = self.pnlLegVOR

        f1 = Frame(self.pnlLegVOR, "HL")
        self.pnlLegVOR.Add = f1

        self.cmbLegVor = ComboBoxPanel(f1)
        self.cmbLegVor.Caption = "VOR / Radial (" + define._degreeStr + ")"
        f1.Add = self.cmbLegVor

        self.txtLegRadial = TrackRadialBoxPanel(f1)
        self.txtLegRadial.Caption = ""
        self.txtLegRadial.LabelWidth = 0
        f1.Add = self.txtLegRadial

        f2 = Frame(self.pnlLegVOR, "HL")
        self.pnlLegVOR.Add = f2

        self.cmbLegBackVor = ComboBoxPanel(f2)
        self.cmbLegBackVor.Caption = "Reverse VOR / Radial (" + define._degreeStr + ")"
        f2.Add = self.cmbLegBackVor

        self.txtLegBackRadial = TrackRadialBoxPanel(f2)
        self.txtLegBackRadial.Caption = ""
        self.txtLegBackRadial.LabelWidth = 0
        f2.Add = self.txtLegBackRadial

        self.pnlPointType = ComboBoxPanel(self.gbAttributes)
        self.pnlPointType.Caption = "Point Type"
        self.gbAttributes.Add = self.pnlPointType

        self.pnlRepPointType = ComboBoxPanel(self.gbAttributes)
        self.pnlRepPointType.Caption = "Reporting Point Type"
        self.gbAttributes.Add = self.pnlRepPointType

        self.pnlPointVor = Frame(self.gbAttributes)
        self.gbAttributes.Add = self.pnlPointVor

        frame1 = Frame(self.pnlPointVor, "HL")
        self.pnlPointVor.Add = frame1

        self.cmbPointVor = ComboBoxPanel(frame1)
        self.cmbPointVor.Caption = "Point VOR / Radial (" + define._degreeStr + ")"
        frame1.Add = self.cmbPointVor

        self.txtPointRadial = TrackRadialBoxPanel(frame1)
        self.txtPointRadial.Caption = ""
        self.txtPointRadial.LabelWidth = 0
        frame1.Add = self.txtPointRadial

        frame2 = Frame(self.pnlPointVor, "HL")
        self.pnlPointVor.Add = frame2

        self.cmbPointDme1 = ComboBoxPanel(frame2)
        self.cmbPointDme1.Caption = "Point 1. DME / Distance (nm)"
        frame2.Add = self.cmbPointDme1

        self.txtPointDme1 = DistanceBoxPanel(frame2, DistanceUnits.NM)
        self.txtPointDme1.Caption = ""
        self.txtPointDme1.LabelWidth = 0
        frame2.Add = self.txtPointDme1

        frame3 = Frame(self.pnlPointVor, "HL")
        self.pnlPointVor.Add = frame3

        self.cmbPointDme2 = ComboBoxPanel(frame3)
        self.cmbPointDme2.Caption = "Point 2. DME / Distance (nm)"
        frame3.Add = self.cmbPointDme2

        self.txtPointDme2 = DistanceBoxPanel(frame3, DistanceUnits.NM)
        self.txtPointDme2.Caption = ""
        self.txtPointDme2.LabelWidth = 0
        frame3.Add = self.txtPointDme2

        self.txtFlyDuration = TextBoxPanel(self.pnlPointVor, True)
        self.txtFlyDuration.Caption = "Flying Time Duration"
        self.pnlPointVor.Add = self.txtFlyDuration

        self.txtRemarks = TextBoxPanel(self.pnlPointVor, True)
        self.txtRemarks.Caption = "Remarks"
        self.pnlPointVor.Add = self.txtRemarks

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        self.btnAdd.clicked.connect(self.btnAdd_Click)
        self.btnMoveDown.clicked.connect(self.btnMoveDown_Click)
        self.btnMoveUp.clicked.connect(self.btnMoveUp_Click)
        self.btnRemove.clicked.connect(self.btnRemove_Click)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

        self.trvLegs.pressed.connect(self.trvLegs_pressed)

        self.data = None
        self.legs = None
        self.aerodrome = None;
        self.magnVar = 0.0

        self.trvLegs.setHeaderHidden(True)

        self.pnlPointType.Items = ["IAF", "IF", "FAF", "FAP", "MAPt", "TP"]

        for value in CodeLegTypeAixm.Items:
            self.pnlLegType.Add(value);

        for value in CodePathTypeAixm.Items:
            self.pnlPathType.Add(value);

        for value in CodeRepAtcAixm.Items:
            self.pnlRepPointType.Add(value);

        for value in CodeTypeFlyByAixm.Items:
            self.pnlFlyBy.Add(value);
        self.method_6()

        self.connect(self.txtRemarks, SIGNAL("Event_0"), self.txtRemarks_Event_0)
        self.connect(self.txtPointDme2, SIGNAL("Event_0"), self.txtPointDme2_Event_0)
        self.connect(self.cmbPointDme2, SIGNAL("Event_0"), self.cmbPointDme2_Event_0)
        self.connect(self.txtPointDme1, SIGNAL("Event_0"), self.txtPointDme1_Event_0)
        self.connect(self.cmbPointDme1, SIGNAL("Event_0"), self.cmbPointDme1_Event_0)
        self.connect(self.cmbPointVor, SIGNAL("Event_0"), self.cmbPointVor_Event_0)
        self.connect(self.txtPointRadial, SIGNAL("Event_0"), self.txtPointRadial_Event_0)
        self.connect(self.txtFlyDuration, SIGNAL("Event_0"), self.txtFlyDuration_Event_0)
        self.connect(self.pnlRepPointType, SIGNAL("Event_0"), self.pnlRepPointType_Event_0)

        self.connect(self.pnlPointType, SIGNAL("Event_0"), self.pnlPointType_Event_0)

        self.connect(self.txtLegBackRadial, SIGNAL("Event_0"), self.txtLegBackRadial_Event_0)

        self.connect(self.cmbLegBackVor, SIGNAL("Event_0"), self.cmbLegBackVor_Event_0)

        self.connect(self.cmbLegVor, SIGNAL("Event_0"), self.cmbLegVor_Event_0)

        self.connect(self.txtLegRadial, SIGNAL("Event_0"), self.txtLegRadial_Event_0)

        self.connect(self.pnlCourse, SIGNAL("Event_0"), self.pnlCourse_Event_0)

        self.connect(self.pnlSegLength, SIGNAL("Event_0"), self.pnlSegLength_Event_0)

        self.connect(self.pnlMinAlt, SIGNAL("Event_0"), self.pnlMinAlt_Event_0)

        self.connect(self.pnlFlyBy, SIGNAL("Event_0"), self.pnlFlyBy_Event_0)

        self.connect(self.cmbCenUid, SIGNAL("Event_0"), self.cmbCenUid_Event_0)

        self.connect(self.pnlLegType, SIGNAL("Event_0"), self.pnlLegType_Event_0)

        self.connect(self.pnlPathType, SIGNAL("Event_0"), self.pnlPathType_Event_0)

        self.connect(self.cmbPosUid, SIGNAL("Event_0"), self.cmbPosUid_Event_0)
        self.connect(self.cmbCenUid, SIGNAL("Event_3"), self.method_14)
        self.connect(self.cmbPosUid, SIGNAL("Event_3"), self.method_13)

        # self.cmbCenter.imageButton.clicked.connect(self.method_14)
        # self.cmbFixPos.imageButton.clicked.connect(self.method_13)
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
        self.legs.insert(count, DataBaseProcedureLegEx());
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
    def cmbPosUid_Event_0(self):
        self.txtFlyDuration_TextChanged(self.cmbPosUid)
    def txtRemarks_Event_0(self):
        self.txtFlyDuration_TextChanged(self.txtRemarks)
    def txtPointDme2_Event_0(self):
        self.txtFlyDuration_TextChanged(self.txtPointDme2)
    def cmbPointDme2_Event_0(self):
        self.txtFlyDuration_TextChanged(self.cmbPointDme2)
    def txtPointDme1_Event_0(self):
        self.txtFlyDuration_TextChanged(self.txtPointDme1)
    def cmbPointDme1_Event_0(self):
        self.txtFlyDuration_TextChanged(self.cmbPointDme1)
    def cmbPointVor_Event_0(self):
        self.txtFlyDuration_TextChanged(self.cmbPointVor)
    def txtPointRadial_Event_0(self):
        self.txtFlyDuration_TextChanged(self.txtPointRadial)
    def txtFlyDuration_Event_0(self):
        self.txtFlyDuration_TextChanged(self.txtFlyDuration)
    def pnlRepPointType_Event_0(self):
        self.txtFlyDuration_TextChanged(self.pnlRepPointType)

    def pnlPointType_Event_0(self):
        self.txtFlyDuration_TextChanged(self.pnlPointType)

    def txtLegBackRadial_Event_0(self):
        self.txtFlyDuration_TextChanged(self.txtLegBackRadial)

    def cmbLegBackVor_Event_0(self):
        self.txtFlyDuration_TextChanged(self.cmbLegBackVor)

    def cmbLegVor_Event_0(self):
        self.txtFlyDuration_TextChanged(self.cmbLegVor)

    def txtLegRadial_Event_0(self):
        self.txtFlyDuration_TextChanged(self.txtLegRadial)

    def pnlCourse_Event_0(self):
        self.txtFlyDuration_TextChanged(self.pnlCourse)

    def pnlSegLength_Event_0(self):
        self.txtFlyDuration_TextChanged(self.pnlSegLength)

    def pnlMinAlt_Event_0(self):
        self.txtFlyDuration_TextChanged(self.pnlMinAlt)

    def pnlFlyBy_Event_0(self):
        self.txtFlyDuration_TextChanged(self.pnlFlyBy)

    def cmbCenUid_Event_0(self):
        self.txtFlyDuration_TextChanged(self.cmbCenUid)

    def pnlLegType_Event_0(self):
        self.txtFlyDuration_TextChanged(self.pnlLegType)

    def pnlPathType_Event_0(self):
        self.txtFlyDuration_TextChanged(self.pnlPathType)

    def trvLegs_pressed(self):
        self.method_6()
        self.method_8()
    def acceptDlg(self):
        self.legs.refresh()
        QObject.emit(self, SIGNAL("DlgAixmProcLegs_Smethod_0_Event"), self.legs, self.data)
        self.accept()
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
    def method_8(self):
        if (self.trvLegs.selectedIndexes() == None or len(self.trvLegs.selectedIndexes()) == 0):
            self.scrollBox.Enabled = False;
            self.cmbPosUid.SelectedIndex = -1;
            self.pnlPathType.SelectedIndex = -1;
            self.pnlLegType.SelectedIndex = -1;
            self.cmbCenUid.SelectedIndex = -1;
            self.pnlFlyBy.SelectedIndex = -1;
            self.pnlMinAlt.Value = None;
            self.pnlSegLength.Value = None;
            self.pnlCourse.Value = None;
            self.cmbLegVor.SelectedIndex = -1;
            self.txtLegRadial.Value = 0;
            self.cmbLegBackVor.SelectedIndex = -1;
            self.txtLegBackRadial.Value = 0;
            self.pnlPointType.Value = "";
            self.pnlRepPointType.SelectedIndex = -1;
            self.cmbPointVor.SelectedIndex = -1;
            self.txtPointRadial.Value = 0;
            self.cmbPointDme1.SelectedIndex = -1;
            self.txtPointDme1.Value = None;
            self.cmbPointDme2.SelectedIndex = -1;
            self.txtPointDme2.Value = None;
            self.txtFlyDuration.Value = "";
            self.txtRemarks.Value = "";
            return;
        self.scrollBox.Enabled = True;
        item = self.legs[self.trvLegs.selectedIndexes()[0].row()];
        if (item.PointEnt == None):
            self.cmbPosUid.SelectedIndex = -1;
        else:
            self.cmbPosUid.SelectedIndex = self.cmbPosUid.IndexOf(item.PointEnt);
        self.pnlPathType.SelectedIndex = self.method_10(self.pnlPathType.Items, item.CodePathType);
        self.pnlLegType.SelectedIndex = self.method_10(self.pnlLegType.Items, item.CodeLegType);
        if (item.CodeLegType != CodeLegTypeAixm.CCA):
            if (item.CodeLegType == CodeLegTypeAixm.CWA):
                if (item.CenterEnt == None):
                    self.cmbCenUid.SelectedIndex = -1;
                else:
                    self.cmbCenUid.SelectedIndex = self.cmbCenUid.IndexOf(item.CenterEnt);
                self.cmbCenUid.Visible = True;
            else:
                self.cmbCenUid.SelectedIndex = -1;
                self.cmbCenUid.Visible = False;
                # goto Label0;
        else:
    # Label2:
            if (item.CenterEnt == None):
                self.cmbCenUid.SelectedIndex = -1;
            else:
                self.cmbCenUid.SelectedIndex = self.cmbCenUid.IndexOf(item.CenterEnt);
            self.cmbCenUid.Visible = True;
    # Label0:
        self.pnlFlyBy.SelectedIndex = self.method_10(self.pnlFlyBy.Items, item.CodeFlyBy)
        self.pnlMinAlt.Value = item.ValMinAlt;
        self.pnlSegLength.Value = item.ValDist;
        self.pnlCourse.Value = item.ValCourse;
        if (item.VorUidLeg == None):
            self.cmbLegVor.SelectedIndex = -1;
        else:
            self.cmbLegVor.SelectedIndex = self.cmbLegVor.IndexOf(item.VorUidLeg);
        self.txtLegRadial.Value = item.ValLegRadial;
        if (item.VorUidLegBack == None):
            self.cmbLegBackVor.SelectedIndex = -1;
        else:
            self.cmbLegBackVor.SelectedIndex = self.cmbLegBackVor.IndexOf(item.VorUidLegBack);
        self.txtLegBackRadial.Value = item.ValLegRadialBack;
        self.pnlPointType.Value = item.CodePointType;
        self.pnlRepPointType.SelectedIndex = self.method_10(self.pnlRepPointType.Items, item.CodeRepAtc)
        if (item.VorUidPoint == None):
            self.cmbPointVor.SelectedIndex = -1;
        else:
            self.cmbPointVor.SelectedIndex = self.cmbPointVor.IndexOf(item.VorUidPoint);
        self.txtPointRadial.Value = item.ValPointRadial;
        if (item.UidPointDist1 == None):
            self.cmbPointDme1.SelectedIndex = -1;
        else:
            self.cmbPointDme1.SelectedIndex = self.cmbPointDme1.IndexOf(item.UidPointDist1);
        self.txtPointDme1.Value = item.ValPointDist1;
        if (item.UidPointDist2 == None):
            self.cmbPointDme2.SelectedIndex = -1;
        else:
            self.cmbPointDme2.SelectedIndex = self.cmbPointDme2.IndexOf(item.UidPointDist2);
        self.txtPointDme2.Value = item.ValPointDist2;
        self.txtFlyDuration.Value = item.ValDur;
        self.txtRemarks.Value = item.TxtRmk;
    def method_9(self, ilist_0, string_0):
        for i in range(len(ilist_0)):
            if (String.StartsWith(ilist_0[i], string_0)):
                return i;
        return -1;
    def method_10(self, ilist_0, string_0):
        for i in range(len(ilist_0)):
            if (String.Equals(ilist_0[i], string_0)):
                return i;
        return -1;
    def txtFlyDuration_TextChanged(self, sender):
        if (self.trvLegs.selectedIndexes() == None or len(self.trvLegs.selectedIndexes()) == 0):
            return;
        item = self.legs[self.trvLegs.selectedIndexes()[0].row()];
        if (sender == self.cmbPosUid):
            item.PointEnt = self.cmbPosUid.SelectedItem
            return;
        if (sender == self.pnlPathType):
            item.CodePathType = self.pnlPathType.SelectedItem;
            return;
        if (sender == self.pnlLegType):
            item.CodeLegType = self.pnlLegType.SelectedItem
            self.cmbCenUid.Visible = (item.CodeLegType == CodeLegTypeAixm.CCA) and True or item.CodeLegType == CodeLegTypeAixm.CWA;
            return;
        if (sender == self.cmbCenUid):
            item.CenterEnt = self.cmbCenUid.SelectedItem
            return;
        if (sender == self.pnlFlyBy):
            item.CodeFlyBy = self.pnlFlyBy.SelectedItem
            return;
        if (sender == self.pnlMinAlt):
            item.ValMinAlt = self.pnlMinAlt.Value;
            return;
        if (sender == self.pnlSegLength):
            item.ValDist = self.pnlSegLength.Value;
            return;
        if (sender == self.pnlCourse):
            item.ValCourse = self.pnlCourse.Value;
            return;
        if (sender == self.cmbLegVor):
            item.VorUidLeg = self.cmbLegVor.SelectedItem;
            return;
        if (sender == self.txtLegRadial):
            item.ValLegRadial = self.txtLegRadial.Value;
            return;
        if (sender == self.cmbLegBackVor):
            item.VorUidLegBack = self.cmbLegBackVor.SelectedItem;
            return;
        if (sender == self.txtLegBackRadial):
            item.ValLegRadialBack = self.txtLegBackRadial.Value;
            return;
        if (sender == self.pnlPointType):
            item.CodePointType = self.pnlPointType.SelectedItem;
            return;
        if (sender == self.pnlRepPointType):
            item.CodeRepAtc = self.pnlRepPointType.SelectedItem;
            return;
        if (sender == self.cmbPointVor):
            item.VorUidPoint = self.cmbPointVor.SelectedItem;
            return;
        if (sender == self.txtPointRadial):
            item.ValPointRadial = self.txtPointRadial.Value;
            return;
        if (sender == self.cmbPointDme1):
            item.UidPointDist1 = self.cmbPointDme1.SelectedItem;
            return;
        if (sender == self.txtPointDme1):
            item.ValPointDist1 = self.txtPointDme1.Value;
            return;
        if (sender == self.cmbPointDme2):
            item.UidPointDist2 = self.cmbPointDme2.SelectedItem
            return;
        if (sender == self.txtPointDme2):
            item.ValPointDist2 = self.txtPointDme2.Value;
            return;
        if (sender == self.txtFlyDuration):
            item.ValDur = self.txtFlyDuration.Value;
            return;
        if (sender == self.txtRemarks):
            item.TxtRmk = self.txtRemarks.Value;

    def method_13(self):
        point3d = None;
        procEntityBase = None;
        selectTool = DlgAixmSelectPosition.smethod_0(self.data, point3d, ProcEntityListType.FixesEx)
        QObject.connect(selectTool, SIGNAL("DlgAixmSelectPosition_Smethod_0_Event"), self.method_13_Event)
    def method_13_Event(self, flag, procEntityBase):
        # flag, procEntityBase = DlgAixmSelectPosition.smethod_0(self.data, point3d, ProcEntityListType.Fixes)
        if (flag and procEntityBase != None):
            if (not self.cmbPosUid.Contains(procEntityBase)):
                self.cmbPosUid.Add(procEntityBase);
            self.cmbPosUid.SelectedIndex = self.cmbPosUid.IndexOf(procEntityBase);
            self.txtFlyDuration_TextChanged(self.cmbPosUid);

    def method_14(self):
        point3d = None;
        procEntityBase = None;
        selectTool = DlgAixmSelectPosition.smethod_0(self.data, point3d, ProcEntityListType.CentersEx)
        QObject.connect(selectTool, SIGNAL("DlgAixmSelectPosition_Smethod_0_Event"), self.method_14_Event)
    def method_14_Event(self, flag, procEntityBase):
        # flag, procEntityBase = DlgAixmSelectPosition.smethod_0(self.data, point3d, ProcEntityListType.Centers)
        if (flag and procEntityBase != None):
            if (not self.cmbCenUid.Contains(procEntityBase)):
                self.cmbCenUid.Add(procEntityBase);
            self.cmbCenUid.SelectedIndex = self.cmbCenUid.IndexOf(procEntityBase);
            self.txtFlyDuration_TextChanged(self.cmbCenUid);
    @staticmethod
    def smethod_0(parent, dataBaseProcedureLegsEx_0, dataBaseProcedureData_0, procEntityAHP_0):
        flag = False;
        dlgAixmProcLegsEx = DlgAixmProcLegsEx(parent)
        dlgAixmProcLegsEx.legs = dataBaseProcedureLegsEx_0;
        dlgAixmProcLegsEx.data = dataBaseProcedureData_0;
        if (procEntityAHP_0 != None):
            dlgAixmProcLegsEx.aerodrome = procEntityAHP_0;
            dlgAixmProcLegsEx.magnVar = procEntityAHP_0.ValMagVar;
        dataBaseProcedureData_0.method_59(dlgAixmProcLegsEx.cmbPosUid, ProcEntityListType.FixesEx);
        dataBaseProcedureData_0.method_59(dlgAixmProcLegsEx.cmbCenUid, ProcEntityListType.CentersEx);
        dataBaseProcedureData_0.method_59(dlgAixmProcLegsEx.cmbLegVor, ProcEntityListType.VORs);
        dataBaseProcedureData_0.method_59(dlgAixmProcLegsEx.cmbLegBackVor, ProcEntityListType.VORs);
        dataBaseProcedureData_0.method_59(dlgAixmProcLegsEx.cmbPointVor, ProcEntityListType.VORs);
        dataBaseProcedureData_0.method_59(dlgAixmProcLegsEx.cmbPointDme1, ProcEntityListType.DMEs);
        dataBaseProcedureData_0.method_59(dlgAixmProcLegsEx.cmbPointDme2, ProcEntityListType.DMEs);
        if (len(dlgAixmProcLegsEx.legs) == 0):
            dlgAixmProcLegsEx.legs.append(DataBaseProcedureLegEx());

        dlgAixmProcLegsEx.method_7();
        if dlgAixmProcLegsEx.trvLegsStdModel.rowCount() > 0:
            dlgAixmProcLegsEx.trvLegs.setCurrentIndex(dlgAixmProcLegsEx.trvLegsStdModel.index(0,0))
            dlgAixmProcLegsEx.method_6()
        dlgAixmProcLegsEx.method_8();
        dlgAixmProcLegsEx.show()
        return dlgAixmProcLegsEx