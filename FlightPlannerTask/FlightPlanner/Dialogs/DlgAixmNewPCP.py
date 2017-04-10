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
from FlightPlanner.types import DegreesType, CodeTypeDesigPtAixm
from FlightPlanner.validations import Validations
from Type.Degrees import Degrees
from Type.ProcEntity import ProcEntityPCP



class DlgAixmNewPCP(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136);
        self.setWindowTitle("New PCP DB Entry")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));

        self.groupBox1 = GroupBox(self)
        verticalLayoutDlg.addWidget(self.groupBox1)

        self.pnlDesig = TextBoxPanel(self.groupBox1)
        self.pnlDesig.Caption = "Designator"
        self.groupBox1.Add = self.pnlDesig

        self.pnlType = TextBoxPanel(self.groupBox1)
        self.pnlType.Caption = "Type / Description"
        self.groupBox1.Add = self.pnlType

        self.pnlPosition = PositionPanel(self.groupBox1, None, None, "Degree")
        self.pnlPosition.hideframe_Altitude()
        self.pnlPosition.btnCalculater.hide()
        self.groupBox1.Add = self.pnlPosition

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



        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)


        self.data = None
        self.dbEntry = None

        # self.pnlCodeType.Items = CodeTypeDesigPtAixm.Items

    def acceptDlg(self):
        degree = None;
        degree1 = None;
        value = self.pnlDesig.Value;
        result, degree, degree1 = self.pnlPosition.method_3();
        if (self.data.method_26(self.pnlDesig.Value, Degrees(degree1, None, None, DegreesType.Latitude), Degrees(degree, None, None, DegreesType.Latitude)) != None):
            strS = "Cannot create a duplicate PCP entry.\n\nCodeID = {0}\nLatitude = {1}\nLongitude = {2}".format(value, str(degree), str(degree1));
            QMessageBox.warning(self, "Error", strS);
            return;
        self.dbEntry = ProcEntityPCP(None, value, Degrees(degree1, None, None, DegreesType.Latitude).ToString(), Degrees(degree, None, None, DegreesType.Longitude).ToString(), self.pnlType.Value, self.txtRemarks.Value, True);
        self.data.method_24(self.dbEntry);
        self.accept()



    @staticmethod
    def smethod_0(dataBaseProcedureData_0, degrees_0, degrees_1):
        flag = False;
        procEntityBase_0 = None;
        dlgAixmNewPCP = DlgAixmNewPCP()
        dlgAixmNewPCP.data = dataBaseProcedureData_0;
        dlgAixmNewPCP.pnlPosition.method_5(degrees_0, degrees_1);
        resultDlg = dlgAixmNewPCP.exec_()
        if (resultDlg == 0):
            flag = False;
        else:
            procEntityBase_0 = dlgAixmNewPCP.dbEntry;
            flag = True;
        return flag, procEntityBase_0;