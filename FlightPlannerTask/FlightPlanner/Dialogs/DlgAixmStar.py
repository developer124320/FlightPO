# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QFileDialog, QDialog, QMessageBox, QDialogButtonBox
from PyQt4.QtCore import QSizeF, SIGNAL, QCoreApplication
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.types import CodeCatAcftAixm, CodeTypeStarAixm
from Type.String import String
from Type.DataBaseProcedureLegs import DataBaseProcedureLegs, DataBaseProcedureLegsEx
import math



class DlgAixmStar(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136);
        self.setWindowTitle("Standard Terminal Arrival Route (STAR)")
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

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

        self.data = None
        self.table = None
        self.selected = None;
    def acceptDlg(self):
        strS = None;
        # self.errorProvider.method_1();
        # self.pnlAerodrome.method_0();
        # self.pnlDesignator.method_0();
        # self.pnlType.method_0();
        # self.pnlRNP.method_1(new Validator(ValidationFlags.AllowEmpty | ValidationFlags.Positive));
        # if (self.errorProvider.HasErrors)
        # {
        #     return;
        # }
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
    
    @staticmethod
    def smethod_0(dataBaseSTARs_0, dataBaseProcedureData_0, dataRow_0):
        flag = False;
        dlgAixmStar = DlgAixmStar()
        dlgAixmStar.data = dataBaseProcedureData_0;
        dlgAixmStar.table = dataBaseSTARs_0;
        dlgAixmStar.selected = dataRow_0;
        dataBaseProcedureData_0.method_51(dlgAixmStar.pnlAerodrome);
        dataBaseProcedureData_0.method_47(dlgAixmStar.pnlMSA);
        dlgAixmStar.pnlAcCategory.Items = CodeCatAcftAixm.Items;
        dlgAixmStar.pnlType.Items = CodeTypeStarAixm.Items;
        # dlgAixmStar.pnlAcCategory.comboBox.insertItem(0, "");
        # dlgAixmStar.pnlMSA.comboBox.insertItem(0, "");
        if (dataRow_0 != None and len(dataRow_0) != 0):
            dlgAixmStar.pnlAerodrome.SelectedIndex = dlgAixmStar.pnlAerodrome.IndexOf(dataRow_0["ahpEnt"]);
            dlgAixmStar.pnlDesignator.Value = dataRow_0["txtDesig"];
            if (dataRow_0["codeCatAcft"] != None):
                dlgAixmStar.pnlAcCategory.SelectedIndex = dlgAixmStar.pnlAcCategory.method_3(dataRow_0["codeCatAcft"]);
            if (dataRow_0["codeTransId"] != None):
                dlgAixmStar.pnlTransID.Value = dataRow_0["codeTransId"];
            if (dataRow_0["mgpEnt"] != None):
                dlgAixmStar.pnlMSA.SelectedIndex = dlgAixmStar.pnlMSA.IndexOf(dataRow_0["mgpEnt"]);
            if (dataRow_0["codeRnp"] != None):
                dlgAixmStar.pnlRNP.Value = dataRow_0["codeRnp"]
            if (dataRow_0["txtDescrComFail"] != None):
                dlgAixmStar.txtDescrComFail.Value = dataRow_0["txtDescrComFail"];
            dlgAixmStar.pnlType.SelectedIndex = dlgAixmStar.pnlType.method_3(dataRow_0["codeTypeRte"]);
            if (dataRow_0["txtDescr"] != None):
                dlgAixmStar.txtDescription.Value = dataRow_0["txtDescr"];
            if (dataRow_0["txtRmk"] != None):
                dlgAixmStar.txtRemarks.Value = dataRow_0["txtRmk"];
        resultDlg = dlgAixmStar.exec_()
        if (resultDlg == 1):
            dataRow0 = dataRow_0 == None or len(dataRow_0) == 0;
            strS = [];
            if (not dataRow0):
                for i in range(dataBaseSTARs_0.ColumnsCount()):
                    strS.append(None)
                # strS = new string[dataBaseSTARs_0.ColumnsCount];
                i = 0
                for name in dataBaseSTARs_0.nameList:
                    strS[i] = dataRow_0[name];
                    i += 1
            else:
                dataRow_0 = dataBaseSTARs_0.NewRow();
            dataRow_0["ahpEnt"] = dlgAixmStar.pnlAerodrome.SelectedItem;
            if (dataRow0):
                dataRow_0["oldAhpEnt"] = dataRow_0["ahpEnt"];
            dataRow_0["txtDesig"] = dlgAixmStar.pnlDesignator.Value;
            if (dataRow0):
                dataRow_0["oldTxtDesig"] = dataRow_0["txtDesig"];
            if (dlgAixmStar.pnlAcCategory.SelectedIndex >= 0):
                dataRow_0["codeCatAcft"] = dlgAixmStar.pnlAcCategory.SelectedItem;
            else:
                dataRow_0["codeCatAcft"] = None;
            if (dataRow0):
                dataRow_0["oldCodeCatAcft"] = dataRow_0["codeCatAcft"];
            if (not String.IsNullOrEmpty(dlgAixmStar.pnlTransID.Value)):
                dataRow_0["codeTransId"] = dlgAixmStar.pnlTransID.Value;
            else:
                dataRow_0["codeTransId"] = None;
            if (dataRow0):
                dataRow_0["oldCodeTransId"] = dataRow_0["codeTransId"];
            if (dlgAixmStar.pnlMSA.SelectedIndex >= 0):
                dataRow_0["mgpEnt"] = dlgAixmStar.pnlMSA.SelectedItem;
            else:
                dataRow_0["mgpEnt"] = None;
            if (not math.isnan(dlgAixmStar.pnlRNP.Value) and not math.isinf(dlgAixmStar.pnlRNP.Value)):
                dataRow_0["codeRnp"] = dlgAixmStar.pnlRNP.Value;
            else:
                dataRow_0["codeRnp"] = None;
            dataRow_0["codeTypeRte"] = dlgAixmStar.pnlType.SelectedItem;
            if (not String.IsNullOrEmpty(dlgAixmStar.txtDescrComFail.Value)):
                dataRow_0["txtDescrComFail"] = dlgAixmStar.txtDescrComFail.Value;
            else:
                dataRow_0["txtDescrComFail"] = None;
            if (not String.IsNullOrEmpty(dlgAixmStar.txtDescription.Value)):
                dataRow_0["txtDescr"] = dlgAixmStar.txtDescription.Value;
            else:
                dataRow_0["txtDescr"] = None;
            if (not String.IsNullOrEmpty(dlgAixmStar.txtRemarks.Value)):
                dataRow_0["txtRmk"] = dlgAixmStar.txtRemarks.Value;
            else:
                dataRow_0["txtRmk"] = None;
            if (dataRow0):
                dataRow_0["procLegs"] = DataBaseProcedureLegs();
                dataRow_0["procLegsEx"] = DataBaseProcedureLegsEx();
            if (not dataRow0):
                num = 1;
                while (num < len(strS)):
                    if (not strS[num] == dataRow_0[dataRow_0.nameList[num]]):
                        dataRow_0["changed"] = "True";
                        if (dataRow0):
                            dataBaseSTARs_0.RowsAdd(dataRow_0);
                        flag = True;
                        return flag;
                    else:
                        num += 1;
            else:
                dataRow_0["new"] = "True";
            if (dataRow0):
                dataBaseSTARs_0.RowsAdd(dataRow_0);
            flag = True;
            return flag;



