# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QMessageBox, QDialogButtonBox
from PyQt4.QtCore import  SIGNAL
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.types import CodeCatAcftAixm, CodeTypeIapAixm, CodeTypeApchAixm, CodeRefOchAixm
from Type.String import String
from Type.DataBaseProcedureLegs import DataBaseProcedureLegs, DataBaseProcedureLegsEx
from Type.DataBase import DataBaseIapOcaOchs, DataBaseIapOcaOch
import math



class DlgAixmOcaOch(QDialog):
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

        self.pnlCodeCatAcft = ComboBoxPanel(self.groupBox)
        self.pnlCodeCatAcft.Caption = "Ac. Category"
        self.pnlCodeCatAcft.LabelWidth = 100
        self.groupBox.Add = self.pnlCodeCatAcft

        self.pnlCodeTypeApch = ComboBoxPanel(self.groupBox)
        self.pnlCodeTypeApch.Caption = "Approach Type"
        self.pnlCodeTypeApch.LabelWidth = 100
        self.groupBox.Add = self.pnlCodeTypeApch

        self.pnlValOca = AltitudeBoxPanel(self.groupBox)
        self.pnlValOca.CaptionUnits = "ft"
        self.pnlValOca.Caption = "OCA"
        self.pnlValOca.LabelWidth = 100
        self.groupBox.Add = self.pnlValOca

        self.pnlOchBase = Frame(self.groupBox, "HL")
        self.groupBox.Add = self.pnlOchBase

        self.pnlValOch = AltitudeBoxPanel(self.pnlOchBase)
        self.pnlValOch.CaptionUnits = "ft"
        self.pnlValOch.Caption = "OCH"
        self.pnlValOch.LabelWidth = 100
        self.pnlOchBase.Add = self.pnlValOch

        self.pnlCodeRefOch = ComboBoxPanel(self.pnlOchBase)
        self.pnlCodeRefOch.Caption = ""
        self.pnlCodeRefOch.LabelWidth = 0
        self.pnlOchBase.Add = self.pnlCodeRefOch



        self.txtRemarks = TextBoxPanel(self.groupBox, True)
        self.txtRemarks.Caption = "Remarks"
        self.txtRemarks.LabelWidth = 100
        self.groupBox.Add = self.txtRemarks


        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

        self.pnlCodeCatAcft.Items = CodeCatAcftAixm.Items
        self.pnlCodeTypeApch.Items = CodeTypeApchAixm.Items
        self.pnlCodeRefOch.Items = CodeRefOchAixm.Items
    def acceptDlg(self):
        self.accept()
    

    @staticmethod
    def smethod_0(dataBaseIapOcaOch_0):
        flag = False;
        dlgAixmOcaOch = DlgAixmOcaOch()
        dlgAixmOcaOch.pnlCodeCatAcft.SelectedIndex = DlgAixmOcaOch.smethod_1(dlgAixmOcaOch.pnlCodeCatAcft.Items, dataBaseIapOcaOch_0.CodeCatAcft);
        dlgAixmOcaOch.pnlCodeTypeApch.SelectedIndex = DlgAixmOcaOch.smethod_1(dlgAixmOcaOch.pnlCodeTypeApch.Items, dataBaseIapOcaOch_0.CodeTypeApch);
        dlgAixmOcaOch.pnlValOca.Value = dataBaseIapOcaOch_0.ValOca;
        dlgAixmOcaOch.pnlValOch.Value = dataBaseIapOcaOch_0.ValOch;
        dlgAixmOcaOch.pnlCodeRefOch.SelectedIndex = DlgAixmOcaOch.smethod_1(dlgAixmOcaOch.pnlCodeRefOch.Items, dataBaseIapOcaOch_0.CodeRefOch);
        dlgAixmOcaOch.txtRemarks.Value = dataBaseIapOcaOch_0.TxtRmk;
        resultDlg = dlgAixmOcaOch.exec_()
        if (resultDlg == 0):
            return False;
        else:
            dataBaseIapOcaOch_0.CodeCatAcft = dlgAixmOcaOch.pnlCodeCatAcft.SelectedItem;
            dataBaseIapOcaOch_0.CodeTypeApch = dlgAixmOcaOch.pnlCodeTypeApch.SelectedItem
            dataBaseIapOcaOch_0.ValOca = dlgAixmOcaOch.pnlValOca.Value;
            dataBaseIapOcaOch_0.ValOch = dlgAixmOcaOch.pnlValOch.Value;
            if (dataBaseIapOcaOch_0.ValOch.IsValid()):
                dataBaseIapOcaOch_0.CodeRefOch = dlgAixmOcaOch.pnlCodeRefOch.SelectedItem
            dataBaseIapOcaOch_0.TxtRmk = dlgAixmOcaOch.txtRemarks.Value;
            dataBaseIapOcaOch_0.refresh()
        flag = True;
        return flag;
    @staticmethod
    def smethod_1(ilist_0, string_0):
        for i in range(len(ilist_0)):
            if ilist_0[i] == string_0:# (string.Equals(ilist_0[i].ToString(), string_0, StringComparison.OrdinalIgnoreCase))
                return i;
        return -1;