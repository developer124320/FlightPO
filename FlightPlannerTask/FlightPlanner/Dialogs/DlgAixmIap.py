# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QTableView, QDialog, QMessageBox, QDialogButtonBox,\
                        QStandardItem, QStandardItemModel, QPushButton, QIcon, QPixmap
from PyQt4.QtCore import QSizeF, SIGNAL, QCoreApplication
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.StandardItemModel import StandardItemModel
from FlightPlanner.types import CodeCatAcftAixm, CodeTypeIapAixm
from FlightPlanner.Dialogs.DlgAixmOcaOch import DlgAixmOcaOch
from Type.String import String
from Type.DataBaseProcedureLegs import DataBaseProcedureLegs, DataBaseProcedureLegsEx
from Type.DataBase import DataBaseIapOcaOchs, DataBaseIapOcaOch
import math



class DlgAixmIap(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136);
        self.setWindowTitle("Instrument Approach Procedure (IAP)")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));

        self.groupBox = GroupBox(self)
        verticalLayoutDlg.addWidget(self.groupBox)

        self.pnlAerodrome = ComboBoxPanel(self.groupBox)
        self.pnlAerodrome.Caption = "Aerodrome"
        self.groupBox.Add = self.pnlAerodrome

        self.pnlDesignator = TextBoxPanel(self.groupBox)
        self.pnlDesignator.Caption = "Designator"
        self.groupBox.Add = self.pnlDesignator

        self.pnlAcCategory = ComboBoxPanel(self.groupBox)
        self.pnlAcCategory.Caption = "Ac. Category"
        self.groupBox.Add = self.pnlAcCategory

        self.pnlTransID = TextBoxPanel(self.groupBox)
        self.pnlTransID.Caption = "ransitional Identifier"
        self.groupBox.Add = self.pnlTransID

        self.pnlType = ComboBoxPanel(self.groupBox)
        self.pnlType.Caption = "Type"
        self.groupBox.Add = self.pnlType

        self.pnlRunway = ComboBoxPanel(self.groupBox)
        self.pnlRunway.Caption = "Runway Direction"
        self.groupBox.Add = self.pnlRunway

        self.pnlMSA = ComboBoxPanel(self.groupBox)
        self.pnlMSA.Caption = "MSA Group"
        self.groupBox.Add = self.pnlMSA

        self.pnlRNP = NumberBoxPanel(self.groupBox)
        self.pnlRNP.Caption = "RNP"
        self.groupBox.Add = self.pnlRNP

        self.tableLayoutPanel = Frame(self.groupBox)
        self.groupBox.Add = self.tableLayoutPanel

        self.txtDescription = TextBoxPanel(self.tableLayoutPanel, True)
        self.txtDescription.Caption = "Description"
        self.tableLayoutPanel.Add = self.txtDescription

        self.txtDescrComFail = TextBoxPanel(self.tableLayoutPanel, True)
        self.txtDescrComFail.Caption = "Communication Failure"
        self.tableLayoutPanel.Add = self.txtDescrComFail

        self.txtRemarks = TextBoxPanel(self.tableLayoutPanel, True)
        self.txtRemarks.Caption = "Remarks"
        self.tableLayoutPanel.Add = self.txtRemarks

        self.gbOcaOch = GroupBox(self.groupBox, "HL")
        self.gbOcaOch.Caption = "Minimum OCA/OCH"
        self.groupBox.Add = self.gbOcaOch

        self.gridOcah = QTableView(self.gbOcaOch)
        self.gridOcahModel = StandardItemModel(None, ["Ac. Category", "Approach Type", "OCA", "OCH", "OCH Ref.", "Remarks"])
        self.gridOcah.setModel(self.gridOcahModel)
        self.gbOcaOch.Add = self.gridOcah

        self.pnlProcButtons = Frame(self.gbOcaOch)
        self.gbOcaOch.Add = self.pnlProcButtons

        self.btnAdd = QPushButton(self.pnlProcButtons)
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/add.png"), QIcon.Normal, QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.pnlProcButtons.Add = self.btnAdd

        self.btnEdit = QPushButton(self.pnlProcButtons)
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/mIconEditableEdits.png"), QIcon.Normal, QIcon.Off)
        self.btnEdit.setIcon(icon)
        self.pnlProcButtons.Add = self.btnEdit

        self.btnRemove = QPushButton(self.pnlProcButtons)
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/remove.png"), QIcon.Normal, QIcon.Off)
        self.btnRemove.setIcon(icon)
        self.pnlProcButtons.Add = self.btnRemove


        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

        self.btnAdd.clicked.connect(self.btnAdd_Click)
        self.btnEdit.clicked.connect(self.btnEdit_Click)
        self.btnRemove.clicked.connect(self.btnRemove_Click)

        self.gridOcah.pressed.connect(self.gridOcah_pressed)

        self.data = None
        self.table = None
        self.selected = None;
        self.minimums = None
    def gridOcah_pressed(self):
        self.method_7()
    def btnAdd_Click(self):
        dataBaseIapOcaOch = DataBaseIapOcaOch();
        if (not DlgAixmOcaOch.smethod_0(dataBaseIapOcaOch)):
            return;
        self.minimums.Add(dataBaseIapOcaOch);
        self.gridOcahModel.Refresh(self.minimums);
        self.method_7();

    def btnEdit_Click(self):
        selectedIndexes = self.gridOcah.selectedIndexes()
        selectedRow = selectedIndexes[0].row()
        if (DlgAixmOcaOch.smethod_0( self.minimums[selectedRow])):
            self.gridOcahModel.Refresh(self.minimums);
            self.method_7();
    def btnRemove_Click(self):
        selectedIndexes = self.gridOcah.selectedIndexes()
        selectedRow = selectedIndexes[0].row()
        self.minimums.pop(selectedRow);
        self.gridOcahModel.Refresh(self.minimums);
        self.method_7();

    def acceptDlg(self):
        strS = None;
        selectedItem = self.pnlAerodrome.SelectedItem;
        num = (self.pnlAcCategory.SelectedIndex >= 0) and self.pnlAcCategory.SelectedIndex or -1;
        for row in self.table:
            flag = True;
            if (self.selected != None and row == self.selected):
                flag = False;
            if (row["ahpEnt"] != selectedItem):
                flag = False;
            if (not self.pnlDesignator.Value == row["txtDesig"]):
                flag = False;
            if (num != (row["codeCatAcft"] == None) and -1 or int(row["codeCatAcft"])):
                flag = False;
            strS = (row["codeTransId"] == None) and "" or row["codeTransId"];
            if (not self.pnlTransID.Value == strS):
                flag = False;
            if (not flag):
                continue;
            str1 = "Cannot create a duplicate procedure entry.\n\nAerodrome = {0}\nDesignator = {1}".format(self.pnlAerodrome.SelectedItem, self.pnlDesignator.Value);
            if (self.pnlAcCategory.SelectedIndex >= 0):
                str1 = String.Concat([str1, "\nAc. Category = {0}".format(self.pnlAcCategory.SelectedItem)]);
            if (not String.IsNullOrEmpty(self.pnlTransID.Value)):
                str1 = String.Concat([str1, "\nTransition Identifier = {0}".format(self.pnlTransID.Value)]);
            QMessageBox.warning(self, "Error", str1);
            return;
        self.accept()
    
    def method_5(self):
        self.data.method_35(self.pnlRunway.Items, self.pnlAerodrome.SelectedItem);
        # self.pnlRunway.comboBox.insertItem(0, "");

    def method_6(self):
        self.btnEdit_Click()

    def method_7(self):
        self.btnEdit.setEnabled(len(self.gridOcah.selectedIndexes()) == 1);
        self.btnRemove.setEnabled(len(self.gridOcah.selectedIndexes()) == 1);

    @staticmethod
    def smethod_0(dataBaseIAPs_0, dataBaseProcedureData_0, dataRow_0):
        flag = False;
        dlgAixmIap = DlgAixmIap()
        dlgAixmIap.data = dataBaseProcedureData_0;
        dlgAixmIap.table = dataBaseIAPs_0;
        dlgAixmIap.selected = dataRow_0;
        dataBaseProcedureData_0.method_51(dlgAixmIap.pnlAerodrome);
        dataBaseProcedureData_0.method_47(dlgAixmIap.pnlMSA);
        dlgAixmIap.pnlAcCategory.Items = CodeCatAcftAixm.Items
        dlgAixmIap.pnlType.Items = CodeTypeIapAixm.Items
        # dlgAixmIap.pnlAcCategory.Insert(0, "");
        # dlgAixmIap.pnlMSA.Items.Insert(0, "");
        if (dataRow_0 != None and len(dataRow_0) != 0):
            dlgAixmIap.pnlAerodrome.SelectedIndex = dlgAixmIap.pnlAerodrome.IndexOf(dataRow_0["ahpEnt"]);
            if (dlgAixmIap.pnlAerodrome.SelectedIndex >= 0):
                dataBaseProcedureData_0.method_35(dlgAixmIap.pnlRunway, dlgAixmIap.pnlAerodrome.SelectedItem);
                # dlgAixmIap.pnlRunway.Insert(0, "");
            dlgAixmIap.pnlDesignator.Value = dataRow_0["txtDesig"];
            if (dataRow_0["codeCatAcft"] != None):
                dlgAixmIap.pnlAcCategory.SelectedIndex = dlgAixmIap.pnlAcCategory.method_3(dataRow_0["codeCatAcft"]);
            if (dataRow_0["codeTransId"] != None):
                dlgAixmIap.pnlTransID.Value = dataRow_0["codeTransId"];
            if (dataRow_0["rdnEnt"] != None):
                dlgAixmIap.pnlRunway.SelectedIndex = dlgAixmIap.pnlRunway.IndexOf(dataRow_0["rdnEnt"]);
            if (dataRow_0["mgpEnt"] != None):
                dlgAixmIap.pnlMSA.SelectedIndex = dlgAixmIap.pnlMSA.IndexOf(dataRow_0["mgpEnt"]);
            if (dataRow_0["codeRnp"] != None):
                dlgAixmIap.pnlRNP.Value = dataRow_0["codeRnp"]
            if (dataRow_0["txtDescrComFail"] != None):
                dlgAixmIap.txtDescrComFail.Value = dataRow_0["txtDescrComFail"];
            dlgAixmIap.pnlType.SelectedIndex = dlgAixmIap.pnlType.method_3(dataRow_0["codeTypeRte"]);
            if (dataRow_0["txtDescrMiss"] != None):
                dlgAixmIap.txtDescription.Value = dataRow_0["txtDescrMiss"];
            if (dataRow_0["txtRmk"] != None):
                dlgAixmIap.txtRemarks.Value = dataRow_0["txtRmk"];
            dlgAixmIap.minimums = dataRow_0["ocah"];
        if (dlgAixmIap.minimums == None):
            dlgAixmIap.minimums = DataBaseIapOcaOchs();
        dlgAixmIap.gridOcahModel.DataSource = dlgAixmIap.minimums;
        resultDlg = dlgAixmIap.exec_()
        if resultDlg == 1:
            dataRow0 = dataRow_0 == None or len(dataRow_0) == 0;
            strS = [];
            if (not dataRow0):
                for i in range(len(dataBaseIAPs_0.nameList)):
                    strS.append(None)
                # strS = new string[dataBaseIAPs_0.Columns.Count];
                i = 0
                for name in dataBaseIAPs_0.nameList:
                    strS[i] = dataRow_0[name];
                    i += 1
            else:
                dataRow_0 = dataBaseIAPs_0.NewRow();
            dataRow_0["ahpEnt"] = dlgAixmIap.pnlAerodrome.SelectedItem;
            if (dataRow0):
                dataRow_0["oldAhpEnt"] = dataRow_0["ahpEnt"];
            dataRow_0["txtDesig"] = dlgAixmIap.pnlDesignator.Value;
            if (dataRow0):
                dataRow_0["oldTxtDesig"] = dataRow_0["txtDesig"];
            if (dlgAixmIap.pnlAcCategory.SelectedIndex >= 0):
                dataRow_0["codeCatAcft"] = dlgAixmIap.pnlAcCategory.SelectedItem;
            else:
                dataRow_0["codeCatAcft"] = None;
            if (dataRow0):
                dataRow_0["oldCodeCatAcft"] = dataRow_0["codeCatAcft"];
            if (not String.IsNullOrEmpty(dlgAixmIap.pnlTransID.Value)):
                dataRow_0["codeTransId"] = dlgAixmIap.pnlTransID.Value;
            else:
                dataRow_0["codeTransId"] = None;
            if (dataRow0):
                dataRow_0["oldCodeTransId"] = dataRow_0["codeTransId"];
            if (dlgAixmIap.pnlRunway.SelectedIndex >= 0):
                dataRow_0["rdnEnt"] = dlgAixmIap.pnlRunway.SelectedItem;
            else:
                dataRow_0["rdnEnt"] = None;
            if (dlgAixmIap.pnlMSA.SelectedIndex >= 0):
                dataRow_0["mgpEnt"] = dlgAixmIap.pnlMSA.SelectedItem;
            else:
                dataRow_0["mgpEnt"] = None;
            if (not math.isnan(dlgAixmIap.pnlRNP.Value) and not math.isinf(dlgAixmIap.pnlRNP.Value)):
                dataRow_0["codeRnp"] = dlgAixmIap.pnlRNP.Value;
            else:
                dataRow_0["codeRnp"] = None;
            dataRow_0["codeTypeRte"] = dlgAixmIap.pnlType.SelectedItem;
            if (not String.IsNullOrEmpty(dlgAixmIap.txtDescrComFail.Value)):
                dataRow_0["txtDescrComFail"] = dlgAixmIap.txtDescrComFail.Value;
            else:
                dataRow_0["txtDescrComFail"] = None;
            if (not String.IsNullOrEmpty(dlgAixmIap.txtDescription.Value)):
                dataRow_0["txtDescrMiss"] = dlgAixmIap.txtDescription.Value;
            else:
                dataRow_0["txtDescrMiss"] = None;
            if (not String.IsNullOrEmpty(dlgAixmIap.txtRemarks.Value)):
                dataRow_0["txtRmk"] = dlgAixmIap.txtRemarks.Value;
            else:
                dataRow_0["txtRmk"] = None;
            dataRow_0["ocah"] = dlgAixmIap.minimums;
            if (dataRow0):
                dataRow_0["procLegs"] = DataBaseProcedureLegs();
                dataRow_0["procLegsEx"] = DataBaseProcedureLegsEx();
            if (not dataRow0):
                num = 1;
                while (num < len(strS)):
                    if (not strS[num] == dataRow_0[dataRow_0.nameList[num]]):
                        dataRow_0["changed"] = "True";
                        if (dataRow0):
                            dataBaseIAPs_0.RowsAdd(dataRow_0);
                        flag = True;
                        return flag;
                    else:
                        num += 1;
            else:
                dataRow_0["new"] = "True";
            if (dataRow0):
                dataBaseIAPs_0.RowsAdd(dataRow_0);
            flag = True;
            return flag;
        return flag


