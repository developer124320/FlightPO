# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QMessageBox, QDialogButtonBox

from PyQt4.QtCore import  SIGNAL
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.types import ProcEntityListType, CodeTypeDesigPtAixm, DegreesType
from FlightPlanner.validations import Validations
from Type.Degrees import Degrees
from Type.ProcEntity import ProcEntityDPN



class DlgAixmNewDPN(QDialog):
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

        self.groupBox1 = GroupBox(self)
        verticalLayoutDlg.addWidget(self.groupBox1)

        self.pnlCodeId = TextBoxPanel(self.groupBox1)
        self.pnlCodeId.Caption = "Code ID"
        self.groupBox1.Add = self.pnlCodeId

        self.pnlCodeType = ComboBoxPanel(self.groupBox1)
        self.pnlCodeType.Caption = "Code Type"
        self.groupBox1.Add = self.pnlCodeType

        self.pnlPosition = PositionPanel(self.groupBox1, None, None, "Degree")
        self.pnlPosition.hideframe_Altitude()
        self.pnlPosition.btnCalculater.hide()
        self.groupBox1.Add = self.pnlPosition

        self.pnlLocation = ComboBoxPanel(self.groupBox1)
        self.pnlLocation.Caption = "Location"
        self.groupBox1.Add = self.pnlLocation

        self.pnlAssociation = ComboBoxPanel(self.groupBox1)
        self.pnlAssociation.Caption = "Associated With"
        self.groupBox1.Add = self.pnlAssociation

        self.pnlName = TextBoxPanel(self.groupBox1)
        self.pnlName.Caption = "Name"
        self.groupBox1.Add = self.pnlName

        self.txtRemarks = TextBoxPanel(self.groupBox1, True)
        self.txtRemarks.Caption = "Remarks"
        self.groupBox1.Add = self.txtRemarks

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        btnOK = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)
        btnOK.setText("Create")
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        self.connect(self.pnlAssociation, SIGNAL("Event_0"), self.method_8)
        self.connect(self.pnlLocation, SIGNAL("Event_0"), self.method_7)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)


        self.data = None
        self.dbEntry = None

        self.pnlCodeType.Items = CodeTypeDesigPtAixm.Items

    def acceptDlg(self):
        degree = None;
        degree1 = None;
        # this.errorProvider.method_1();
        # this.pnlCodeId.method_0();
        # # this.pnlPosition.method_6();
        # if (self.pnlCodeType.method_0())
        # {
        codeTypeDesigPtAixm = self.pnlCodeType.SelectedItem
        if (codeTypeDesigPtAixm == CodeTypeDesigPtAixm.ICAO):
            # if (self.pnlCodeId.method_0())
            # {
            procEntityBases = self.data.method_54(self.pnlCodeId.Value);
            if (procEntityBases != None and len(procEntityBases) > 0):
                self.pnlCodeId.method_2(Validations.UNIQUE_IDENTIFIER_REQUIRED);
                return
        elif (codeTypeDesigPtAixm == CodeTypeDesigPtAixm.ADHP):
            if (self.pnlLocation.SelectedIndex < 1 and self.pnlAssociation.SelectedIndex < 1):
                err = self.pnlLocation.Caption + " : \n" + \
                    Validations.PLEASE_SELECT_AN_ITEM + "\n" + \
                    self.pnlAssociation.Caption + " : \n" + \
                    Validations.PLEASE_SELECT_AN_ITEM
                QMessageBox.warning(self, "Warning", err)
                return
            elif (self.pnlAssociation.SelectedIndex > 0):
                procEntityBases1 = self.data.method_55(self.pnlCodeId.Value, self.pnlAssociation.SelectedItem);
                if (procEntityBases1 != None and procEntityBases1.Count > 0):
                    self.pnlCodeId.method_2(Validations.UNIQUE_IDENTIFIER_REQUIRED);
                    return
        value = self.pnlCodeId.Value;
        result, degree, degree1 = self.pnlPosition.method_3();
        if (self.data.method_57(self.pnlCodeId.Value, Degrees(degree1, None, None, DegreesType.Latitude), Degrees(degree, None, None, DegreesType.Longitude)) != None):
            strS = "Cannot create a duplicate DPN entry.\n\nCodeID = {0}\nLatitude = {1}\nLongitude = {2}".format(value, str(degree), str(degree1));
            QMessageBox.warning(self, "Error", strS);
            return;
        codeTypeDesigPtAixm1 = self.pnlCodeType.SelectedItem
        self.dbEntry = ProcEntityDPN(value, Degrees(degree1, None, None, DegreesType.Latitude).method_1("ddmmss.ssssh"), Degrees(degree, None, None, DegreesType.Longitude).method_1("dddmmss.ssssh"), self.pnlAssociation.SelectedItem, self.pnlLocation.SelectedItem, codeTypeDesigPtAixm1, self.pnlName.Value, self.txtRemarks.Value, True);
        self.data.method_52(self.dbEntry);
        self.accept()

    def method_8(self):
        self.pnlLocation.SelectedIndex = -1;

    def method_7(self):
        self.pnlAssociation.SelectedIndex = -1;

    @staticmethod
    def smethod_0(dataBaseProcedureData_0, degrees_0, degrees_1):
        flag = False;
        procEntityBase_0 = None;
        dlgAixmNewDPN = DlgAixmNewDPN()
        dlgAixmNewDPN.data = dataBaseProcedureData_0;
        dataBaseProcedureData_0.method_59(dlgAixmNewDPN.pnlLocation, ProcEntityListType.LocationsDPN);
        dataBaseProcedureData_0.method_59(dlgAixmNewDPN.pnlAssociation, ProcEntityListType.AHPs);
        dlgAixmNewDPN.pnlPosition.method_5(degrees_0, degrees_1);
        resultDlg = dlgAixmNewDPN.exec_()
        if (resultDlg == 0):
            flag = False;
        else:
            procEntityBase_0 = dlgAixmNewDPN.dbEntry;
            flag = True;
        return flag, procEntityBase_0;