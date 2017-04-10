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
from FlightPlanner.Dialogs.DlgAixmSelectPosition import DlgAixmSelectPosition
from FlightPlanner.types import ProcEntityListType, CodeTypeHoldProcAixm
from FlightPlanner.types import Point3D
from Type.String import String
from Type.DataBaseProcedureLegs import DataBaseProcedureLegs, DataBaseProcedureLegsEx
from FlightPlanner.captureCoordinateTool import CaptureCoordinateToolUpdate

import define



class DlgAixmHolding(QDialog):
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

        self.pnlBasedOn = ComboBoxPanel(self.groupBox)
        self.pnlBasedOn.Caption = "Based On"
        self.pnlBasedOn.Button = "coordinate_capture.png"
        self.groupBox.Add = self.pnlBasedOn

        self.pnlType = ComboBoxPanel(self.groupBox)
        self.pnlType.Caption = "Type"
        self.groupBox.Add = self.pnlType

        self.txtDescription = TextBoxPanel(self.groupBox, True)
        self.txtDescription.Caption = "Description"
        self.groupBox.Add = self.txtDescription

        self.txtRemarks = TextBoxPanel(self.groupBox, True)
        self.txtRemarks.Caption = "Remarks"
        self.groupBox.Add = self.txtRemarks

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        self.connect(self.pnlBasedOn, SIGNAL("Event_3"), self.pnlBasedOn_Event_3)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)


        self.data = None
        self.table = None
        self.selected = None;

        self.CaptureCoordTool = CaptureCoordinateToolUpdate(define._canvas)
        self.connect(self.CaptureCoordTool, SIGNAL("resultPointValueList"), self.resultPointValueListMethod)

    def pnlBasedOn_Event_3(self):
        CaptureCoordTool = CaptureCoordinateToolUpdate(define._canvas)
        self.connect(CaptureCoordTool, SIGNAL("resultPointValueList"), self.resultPointValueListMethod)

        define._canvas.setMapTool(self.CaptureCoordTool)

    def resultPointValueListMethod(self, resultValueList):
        if len(resultValueList) > 0:
            point3d = Point3D(float(resultValueList[1]), float(resultValueList[2]), float(resultValueList[3]))
            resultDlg, procEntityBase = DlgAixmSelectPosition.smethod_0(self, self.data, point3d, ProcEntityListType.Holding)
            if (resultDlg and procEntityBase != None):
                if (not self.pnlBasedOn.Contains(procEntityBase)):
                    self.pnlBasedOn.Add(procEntityBase);
                self.pnlBasedOn.SelectedIndex = self.pnlBasedOn.IndexOf(procEntityBase);
    def acceptDlg(self):
        selectedItem = self.pnlBasedOn.SelectedItem;
        codeTypeHoldProcAixm = self.pnlType.SelectedItem
        for row in self.table:
            flag = True;
            if (self.selected != None and row == self.selected):
                flag = False;
            if (row["basedOnEnt"] != selectedItem):
                flag = False;
            if (row["codeType"] != codeTypeHoldProcAixm):
                flag = False;
            if (not flag):
                continue;
            strS = "Cannot create a duplicate procedure entry.\n\nBased on = {0}\nType = {1}".format(self.pnlBasedOn.SelectedItem, self.pnlType.SelectedItem);
            QMessageBox.warning(self, "Error", strS);
            return;
        self.accept()
    

    def method_6(self):
        pass

    @staticmethod
    def smethod_0(dataBaseHoldings_0, dataBaseProcedureData_0, dataRow_0):
        flag = False;
        dlgAixmHolding = DlgAixmHolding()
        dlgAixmHolding.data = dataBaseProcedureData_0;
        dlgAixmHolding.table = dataBaseHoldings_0;
        dlgAixmHolding.selected = dataRow_0;
        dataBaseProcedureData_0.method_59(dlgAixmHolding.pnlBasedOn, ProcEntityListType.Holding);
        dlgAixmHolding.pnlType.Items = CodeTypeHoldProcAixm.Items;
        if (dataRow_0 != None and len(dataRow_0) > 0):
            dlgAixmHolding.pnlBasedOn.SelectedIndex = dlgAixmHolding.pnlBasedOn.IndexOf(dataRow_0["basedOnEnt"]);
            dlgAixmHolding.pnlType.SelectedIndex = dlgAixmHolding.pnlType.method_3(dataRow_0["codeType"]);
            if (dataRow_0["txtDescr"] != None):
                dlgAixmHolding.txtDescription.Value = dataRow_0["txtDescr"];
            if (dataRow_0["txtRmk"] != None):
                dlgAixmHolding.txtRemarks.Value = dataRow_0["txtRmk"];
        resultDlg = dlgAixmHolding.exec_()
        if (resultDlg == 1):
            dataRow0 = dataRow_0 == None or len(dataRow_0) == 0;
            strS = [];
            if (not dataRow0):
                for a in dataBaseHoldings_0.nameList:
                    strS.append(None)
                # str = new string[dataBaseHoldings_0.Columns.Count];
                i = 0
                for name in dataBaseHoldings_0.nameList:
                    strS[i] = dataRow_0[name]
                    i += 1
            else:
                dataRow_0 = dataBaseHoldings_0.NewRow();
            dataRow_0["basedOnEnt"] = dlgAixmHolding.pnlBasedOn.SelectedItem;
            if (dataRow0):
                dataRow_0["oldBasedOnEnt"] = dataRow_0["basedOnEnt"];
            dataRow_0["codeType"] = dlgAixmHolding.pnlType.SelectedItem;
            if (dataRow0):
                dataRow_0["oldCodeType"] = dataRow_0["codeType"];
            if (not String.IsNullOrEmpty(dlgAixmHolding.txtDescription.Value)):
                dataRow_0["txtDescr"] = dlgAixmHolding.txtDescription.Value;
            else:
                dataRow_0["txtDescr"] = None;
            if (not String.IsNullOrEmpty(dlgAixmHolding.txtRemarks.Value)):
                dataRow_0["txtRmk"] = dlgAixmHolding.txtRemarks.Value;
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
                            dataBaseHoldings_0.RowsAdd(dataRow_0);
                        flag = True;
                        return flag;
                    else:
                        num += 1;
            else:
                dataRow_0["new"] = "True";
            if (dataRow0):
                dataBaseHoldings_0.RowsAdd(dataRow_0);
            flag = True;
            return flag;
        return flag