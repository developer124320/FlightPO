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
from FlightPlanner.types import CodeCatAcftAixm, CodeTypeSidAixm
from Type.String import String
from Type.DataBaseProcedureLegs import DataBaseProcedureLegs, DataBaseProcedureLegsEx
import math



class DlgAixmSid(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136);
        self.setWindowTitle("Standard Instrument Departure (SID)")
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
            if (num != (row["codeCatAcft"] == None) and -1 or row["codeCatAcft"]):
                flag = False;
            str = (row["codeTransId"] == None) and "" or row["codeTransId"];
            if (not self.pnlTransID.Value == str):
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
        self.data.method_35(self.pnlRunway, self.pnlAerodrome.SelectedItem);
        # self.pnlRunway.comboBox.insertItem(0, "");
    
    @staticmethod
    def smethod_0(dataBaseSIDs_0, dataBaseProcedureData_0, dataRow_0):
        flag = False;
        dlgAixmSid = DlgAixmSid()
        dlgAixmSid.data = dataBaseProcedureData_0;
        dlgAixmSid.table = dataBaseSIDs_0;
        dlgAixmSid.selected = dataRow_0;
        dataBaseProcedureData_0.method_51(dlgAixmSid.pnlAerodrome);
        dataBaseProcedureData_0.method_47(dlgAixmSid.pnlMSA);

        dlgAixmSid.pnlAcCategory.Items = CodeCatAcftAixm.Items;
        dlgAixmSid.pnlType.Items = CodeTypeSidAixm.Items;
        # dlgAixmSid.pnlAcCategory.comboBox.insertItem(0, "");
        # dlgAixmSid.pnlMSA.comboBox.insertItem(0, "");
        if (dataRow_0 != None):
            dlgAixmSid.pnlAerodrome.SelectedIndex = dlgAixmSid.pnlAerodrome.comboBox.findText(dataRow_0["ahpEnt"].ToString());
            if (dlgAixmSid.pnlAerodrome.SelectedIndex >= 0):
                dataBaseProcedureData_0.method_35(dlgAixmSid.pnlRunway, dlgAixmSid.pnlAerodrome.SelectedItem);
                # dlgAixmSid.pnlRunway.comboBox.insertItem(0, "");
            dlgAixmSid.pnlDesignator.Value = dataRow_0["txtDesig"];
            if (dataRow_0["codeCatAcft"] != None):
                dlgAixmSid.pnlAcCategory.SelectedIndex = dlgAixmSid.pnlAcCategory.method_3(dataRow_0["codeCatAcft"]);
            if (dataRow_0["codeTransId"] != None):
                dlgAixmSid.pnlTransID.Value = dataRow_0["codeTransId"];
            if (dataRow_0["rdnEnt"] != None):
                dlgAixmSid.pnlRunway.SelectedIndex = dlgAixmSid.pnlRunway.comboBox.findText(dataRow_0["rdnEnt"].ToString());
            if (dataRow_0["mgpEnt"] != None):
                dlgAixmSid.pnlMSA.SelectedIndex = dlgAixmSid.pnlMSA.comboBox.findText(dataRow_0["mgpEnt"].ToString());
            if (dataRow_0["codeRnp"] != None):
                dlgAixmSid.pnlRNP.Value = dataRow_0["codeRnp"]
            if (dataRow_0["txtDescrComFail"] != None):
                dlgAixmSid.txtDescrComFail.Text = dataRow_0["txtDescrComFail"];
            dlgAixmSid.pnlType.SelectedIndex = dlgAixmSid.pnlType.method_3(dataRow_0["codeTypeRte"]);
            if (dataRow_0["txtDescr"] != None):
                dlgAixmSid.txtDescription.Value = dataRow_0["txtDescr"];
            if (dataRow_0["txtRmk"] != None):
                dlgAixmSid.txtRemarks.Value = dataRow_0["txtRmk"];
        dlgResult = dlgAixmSid.exec_()
        if (dlgResult == 1):
            dataRow0 = dataRow_0 == None;
            strS = [];
            if (not dataRow0):
                for i in range(dataBaseSIDs_0.ColumnsCount()):
                    strS.append(None)
                # str = new string[dataBaseSIDs_0.Columns.Count];
                i = 0
                for name in dataBaseSIDs_0.nameList:
                    strS[i] = dataRow_0[name];
                    i += 1
            else:
                dataRow_0 = dataBaseSIDs_0.NewRow();
            dataRow_0["ahpEnt"] = dlgAixmSid.pnlAerodrome.SelectedItem;
            if (dataRow0):
                dataRow_0["oldAhpEnt"] = dataRow_0["ahpEnt"];
            dataRow_0["txtDesig"] = dlgAixmSid.pnlDesignator.Value;
            if (dataRow0):
                dataRow_0["oldTxtDesig"] = dataRow_0["txtDesig"];
            if (dlgAixmSid.pnlAcCategory.SelectedIndex >= 0):
                dataRow_0["codeCatAcft"] = dlgAixmSid.pnlAcCategory.SelectedItem;
            else:
                dataRow_0["codeCatAcft"] = None;
            if (dataRow0):
                dataRow_0["oldCodeCatAcft"] = dataRow_0["codeCatAcft"];
            if (not String.IsNullOrEmpty(dlgAixmSid.pnlTransID.Value)):
                dataRow_0["codeTransId"] = dlgAixmSid.pnlTransID.Value;
            else:
                dataRow_0["codeTransId"] = None;
            if (dataRow0):
                dataRow_0["oldCodeTransId"] = dataRow_0["codeTransId"];
            if (dlgAixmSid.pnlRunway.SelectedIndex >= 0):
                dataRow_0["rdnEnt"] = dlgAixmSid.pnlRunway.SelectedItem;
            else:
                dataRow_0["rdnEnt"] = None;
            if (dlgAixmSid.pnlMSA.SelectedIndex >= 0):
                dataRow_0["mgpEnt"] = dlgAixmSid.pnlMSA.SelectedItem;
            else:
                dataRow_0["mgpEnt"] = None;
            if (not math.isinf(dlgAixmSid.pnlRNP.Value) and not math.isnan(dlgAixmSid.pnlRNP.Value)):
                dataRow_0["codeRnp"] = dlgAixmSid.pnlRNP.Value;
            else:
                dataRow_0["codeRnp"] = None;
            dataRow_0["codeTypeRte"] = dlgAixmSid.pnlType.SelectedItem;
            if (not String.IsNullOrEmpty(dlgAixmSid.txtDescrComFail.Value)):
                dataRow_0["txtDescrComFail"] = dlgAixmSid.txtDescrComFail.Value;
            else:
                dataRow_0["txtDescrComFail"] = None;
            if (not String.IsNullOrEmpty(dlgAixmSid.txtDescription.Value)):
                dataRow_0["txtDescr"] = dlgAixmSid.txtDescription.Value;
            else:
                dataRow_0["txtDescr"] = None;
            if (not String.IsNullOrEmpty(dlgAixmSid.txtRemarks.Value)):
                dataRow_0["txtRmk"] = dlgAixmSid.txtRemarks.Value;
            else:
                dataRow_0["txtRmk"] = None;
            if (dataRow0):
                dataRow_0["procLegs"] = DataBaseProcedureLegs();
                dataRow_0["procLegsEx"] = DataBaseProcedureLegsEx();
            if (not dataRow0):
                num = 1;
                while (num < int(len(strS))):
                    if (not strS[num] == dataRow_0[dataRow_0.nameList[num]]):
                        dataRow_0["changed"] = "True";
                        if (dataRow0):
                            dataBaseSIDs_0.RowsAdd(dataRow_0);
                        flag = True;
                        return flag;
                    else:
                        num += 1;
            else:
                dataRow_0["new"] = "True";
            if (dataRow0):
                dataBaseSIDs_0.RowsAdd(dataRow_0);
            flag = True;
            return flag;
        return False;






