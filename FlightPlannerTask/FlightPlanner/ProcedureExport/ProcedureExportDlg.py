# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication, QFileInfo, QObject, QFile, QTextStream, QDateTime
from PyQt4.QtGui import QFileDialog, QMessageBox, QSortFilterProxyModel, QDesktopServices
from PyQt4.QtXml import QDomDocument
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import SurfaceTypes, DataBaseProcedureExportDlgType
from FlightPlanner.ProcedureExport.ui_ProcedureExport import Ui_ProcedureExport
from FlightPlanner.Dialogs.DlgAixmHolding import DlgAixmHolding
from FlightPlanner.Dialogs.DlgAixmIap import DlgAixmIap
from FlightPlanner.Dialogs.DlgAixmSid import DlgAixmSid
from FlightPlanner.Dialogs.DlgAixmStar import DlgAixmStar
from FlightPlanner.Dialogs.DlgAixmProcLegs import DlgAixmProcLegs
from FlightPlanner.Dialogs.DlgAixmProcLegsEx import DlgAixmProcLegsEx
from FlightPlanner.Dialogs.DlgAixmEffectiveDate import DlgAixmEffectiveDate
from FlightPlanner.QgisHelper import QgisHelper

from Type.DataBaseLoaderAixm import DataBaseLoaderAixm
from Type.DataBaseProcedureLegs import DataBaseProcedureLegs, DataBaseProcedureLegsEx
from Type.String import String
from Type.ProcEntity import ProcEntityDPN, ProcEntityPCP


class ProcedureExportDlg(FlightPlanBaseDlg):
    dataBase = None
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("PathTerminatorsDlg")
        self.surfaceType = SurfaceTypes.ProcedureExport
        self.selectedRow = None
        self.editingModelIndex = None

        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.ProcedureExport)
        self.resize(540, 550)
        QgisHelper.matchingDialogSize(self, 540, 650)
        self.surfaceList = None


        self.loaderAixm = DataBaseLoaderAixm();
        self.directory = None;
        self.adding = False;
        self.newRowIndex = -1;

        # assa = vars(SurfaceTypes)
        # asa = SurfaceTypes.__dict__
        pass

    
    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.btnConstruct.setVisible(False)
        self.ui.btnEvaluate.setEnabled(True)
        self.ui.btnPDTCheck.setVisible(False)

        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        self.ui.tabCtrlGeneral.removeTab(1)
#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)

    def btnEvaluate_Click(self):   #### ---------------  Export  -------------------###
        if ProcedureExportDlg.dataBase == None:
            return
        filePathDir = QFileDialog.getSaveFileName(self, "Save Data",QCoreApplication.applicationDirPath (),"XML Files (*.xml)")
        if filePathDir == "":
            return

        effectiveDate = ProcedureExportDlg.dataBase.EffectiveDate;
        resultDlg, effectiveDate = DlgAixmEffectiveDate.smethod_0(effectiveDate)
        if (not resultDlg):
            return;
        xmlDocument = QDomDocument()
        xmlDeclaration = xmlDocument.createProcessingInstruction("xml", "version=\"1.0\" encoding=\"UTF-8\"" )
        xmlDocument.appendChild(xmlDeclaration)
        xmlElement = xmlDocument.createElement("AIXM-update")
        # xmlAttribute = xmlDocument.createAttribute("xsi")
        # xmlAttribute.setValue("http://www.w3.org/2001/XMLSchema-instance")
        xmlElement.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance");
        xmlElement.setAttribute("xsi:noNamespaceSchemaLocation", "AIXM+Update.xsd");
    #     xmlAttribute.Value = "AIXM+Update.xsd";
        xmlElement.setAttribute("version", "4.5");
        xmlElement.setAttribute("origin", "ASAP s.r.o.");
        strS = QDateTime.currentDateTime().toString("yyyy-MM-dd");
        now = QDateTime.currentDateTime();
        xmlElement.setAttribute("created", String.Concat([strS, "T", now.toString("hh:mm:ss")]));
        xmlElement.setAttribute("effective", String.Concat([effectiveDate.toString("yyyy-MM-dd"), "T00:00:00"]));
        # xmlElement.Attributes.Append(xmlAttribute);
        xmlDocument.appendChild(xmlElement)
        xmlElement1 = xmlDocument.createElement("Group");
        xmlElement1.setAttribute("Name", "Group 1 of 1");
        ProcedureExportDlg.dataBase.ProcedureData.method_61(xmlElement1, self.newProcedurePointsInUse);
        ProcedureExportDlg.dataBase.ProcedureData.method_62(xmlElement1, ProcedureExportDlg.dataBase.SIDs.Select({"deleted":"True", "new":"False"}), DataBaseProcedureExportDlgType.Deleted);
        ProcedureExportDlg.dataBase.ProcedureData.method_62(xmlElement1, ProcedureExportDlg.dataBase.SIDs.Select({"deleted":"False", "changed":"True", "new":"False"}), DataBaseProcedureExportDlgType.Updated);
        ProcedureExportDlg.dataBase.ProcedureData.method_62(xmlElement1, ProcedureExportDlg.dataBase.SIDs.Select({"deleted":"False", "new":"True"}), DataBaseProcedureExportDlgType.Created);
        ProcedureExportDlg.dataBase.ProcedureData.method_63(xmlElement1, ProcedureExportDlg.dataBase.STARs.Select({"deleted":"True", "new":"False"}), DataBaseProcedureExportDlgType.Deleted);
        ProcedureExportDlg.dataBase.ProcedureData.method_63(xmlElement1, ProcedureExportDlg.dataBase.STARs.Select({"deleted":"False", "changed":"True", "new":"False"}), DataBaseProcedureExportDlgType.Updated);
        ProcedureExportDlg.dataBase.ProcedureData.method_63(xmlElement1, ProcedureExportDlg.dataBase.STARs.Select({"deleted":"False", "new":"True"}), DataBaseProcedureExportDlgType.Created);
        ProcedureExportDlg.dataBase.ProcedureData.method_64(xmlElement1, ProcedureExportDlg.dataBase.IAPs.Select({"deleted":"True", "new":"False"}), DataBaseProcedureExportDlgType.Deleted);
        ProcedureExportDlg.dataBase.ProcedureData.method_64(xmlElement1, ProcedureExportDlg.dataBase.IAPs.Select({"deleted":"False", "changed":"True", "new":"False"}), DataBaseProcedureExportDlgType.Updated);
        ProcedureExportDlg.dataBase.ProcedureData.method_64(xmlElement1, ProcedureExportDlg.dataBase.IAPs.Select({"deleted":"False", "new":"True"}), DataBaseProcedureExportDlgType.Created);
        ProcedureExportDlg.dataBase.ProcedureData.method_65(xmlElement1, ProcedureExportDlg.dataBase.Holdings.Select({"deleted":"True", "new":"False"}), DataBaseProcedureExportDlgType.Deleted);
        ProcedureExportDlg.dataBase.ProcedureData.method_65(xmlElement1, ProcedureExportDlg.dataBase.Holdings.Select({"deleted":"False", "changed":"True", "new":"False"}), DataBaseProcedureExportDlgType.Updated);
        ProcedureExportDlg.dataBase.ProcedureData.method_65(xmlElement1, ProcedureExportDlg.dataBase.Holdings.Select({"deleted":"False", "new":"True"}), DataBaseProcedureExportDlgType.Created);
        xmlElement.appendChild(xmlElement1);
    #     xmlDocument.Save(self.sfd.FileName);
    #     base.method_20(string.Format(Messages.X_SUCCESSFULLY_CREATED, self.pnlFile.Value));
        qFile = QFile(filePathDir)
        if qFile.open(QFile.WriteOnly):
            textStream = QTextStream(qFile)
            xmlDocument.save(textStream, 4)
            qFile.close()
        else:
            raise UserWarning, "can not open file:" + filePathDir
    def btnConstruct_Click(self):   ### ---------------  Import  ---------------------###

        return FlightPlanBaseDlg.btnConstruct_Click(self)

    def btnPDTCheck_Click(self):    ### ---------------  Clear  ---------------------###
         pass
    def initParametersPan(self):
        ui = Ui_ProcedureExport()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.tabControl.currentChanged.connect(self.tabControl_CurrentChanged)
        self.parametersPanel.gridProcedures.pressed.connect(self.gridProcedures_pressed)
        self.parametersPanel.btnProcEdit.clicked.connect(self.btnProcEdit_Click)
        self.parametersPanel.btnProcRemove.clicked.connect(self.btnProcRemove_Click)
        self.parametersPanel.btnProcAdd.clicked.connect(self.btnProcAdd_Click)
        self.parametersPanel.btnLegsEdit.clicked.connect(self.btnLegsEdit_Click)
        self.parametersPanel.btnLegsExEdit.clicked.connect(self.btnLegsExEdit_Click)
        #
        self.connect(self.parametersPanel.pnlFile, SIGNAL("Event_1"), self.method_41)

        self.parametersPanel.btnLegsPreview.setVisible(True)
        self.parametersPanel.btnLegsExPreview.setVisible(True)
    def btnLegsExEdit_Click(self):
        dataRow = self.selectedProcedureRow;
        item = dataRow["procLegsEx"];
        dataBaseProcedureLegsEx = (item == None or len(item) == 0) and DataBaseProcedureLegsEx() or item.method_0();
        procEntityAHP = None;
        # num = dataRow.Table.Columns.IndexOf("ahpEnt");
        try:
            if (dataRow["ahpEnt"] != None):
                procEntityAHP = dataRow["ahpEnt"];
        except:
            pass
        self.anyData = dataRow
        dlgAixmProcLegsEx = DlgAixmProcLegsEx.smethod_0(self, dataBaseProcedureLegsEx, ProcedureExportDlg.dataBase.ProcedureData, procEntityAHP)
        QObject.connect(dlgAixmProcLegsEx, SIGNAL("DlgAixmProcLegs_Smethod_0_Event"), self.dlgAixmProcLegsEx_Smethod_0_Event)
    def dlgAixmProcLegsEx_Smethod_0_Event(self, dataBaseProcedureLegsEx, data):
        self.anyData["procLegsEx"] = dataBaseProcedureLegsEx;
        self.parametersPanel.gridLegsExStdModel.DataSource = dataBaseProcedureLegsEx;
        self.anyData["changed"] = "True";
        self.method_32()
        # if (DlgAixmProcLegsEx.smethod_0(dataBaseProcedureLegsEx, ProcedureExportDlg.dataBase.ProcedureData, procEntityAHP)):
        #     dataRow["procLegsEx"] = dataBaseProcedureLegsEx;
        #     self.parametersPanel.gridLegsExStdModel.DataSource = dataBaseProcedureLegsEx;
        #     dataRow["changed"] = "True";
    def btnLegsEdit_Click(self):
        dataRow = self.selectedProcedureRow;
        item = dataRow["procLegs"];
        dataBaseProcedureLeg = (item == None or len(item) == 0) and DataBaseProcedureLegs() or item.method_0();
        procEntityAHP = None;
        # num = dataRow.IndexOf("ahpEnt");
        try:
            if (dataRow["ahpEnt"] != None):
                procEntityAHP = dataRow["ahpEnt"];
        except:
            pass
        self.anyData = dataRow
        dlgAixmProcLegs = DlgAixmProcLegs.smethod_0(self, dataBaseProcedureLeg, ProcedureExportDlg.dataBase.ProcedureData, procEntityAHP)
        QObject.connect(dlgAixmProcLegs, SIGNAL("DlgAixmProcLegs_Smethod_0_Event"), self.dlgAixmProcLegs_Smethod_0_Event)
    def dlgAixmProcLegs_Smethod_0_Event(self, dataBaseProcedureLeg, data):
        self.anyData["procLegs"] = dataBaseProcedureLeg;
        self.parametersPanel.gridLegsStdModel.DataSource = dataBaseProcedureLeg;
        self.anyData["changed"] = "True";
        self.method_32()
    def btnProcAdd_Click(self):
        self.newRowIndex = -1;
        self.adding = True;
        if ProcedureExportDlg.dataBase == None:
            QMessageBox.warning(self, "Warning", "Import the database!")
            return
        if self.parametersPanel.tabControl.currentIndex() == 0:
            DlgAixmSid.smethod_0(ProcedureExportDlg.dataBase.SIDs, ProcedureExportDlg.dataBase.ProcedureData, None);
        elif self.parametersPanel.tabControl.currentIndex() == 1:
            DlgAixmStar.smethod_0(ProcedureExportDlg.dataBase.STARs, ProcedureExportDlg.dataBase.ProcedureData, None);
        elif self.parametersPanel.tabControl.currentIndex() == 2:
            DlgAixmIap.smethod_0(ProcedureExportDlg.dataBase.IAPs, ProcedureExportDlg.dataBase.ProcedureData, None);
        elif self.parametersPanel.tabControl.currentIndex() == 3:
            DlgAixmHolding.smethod_0(ProcedureExportDlg.dataBase.Holdings, ProcedureExportDlg.dataBase.ProcedureData, None);
        self.method_32()
        self.adding = False;
    def btnProcEdit_Click(self):
        dataRow = self.selectedProcedureRow;
        if (dataRow == None):
            return;
        if (self.parametersPanel.tabControl.currentIndex() == 0):
            DlgAixmSid.smethod_0(ProcedureExportDlg.dataBase.SIDs, ProcedureExportDlg.dataBase.ProcedureData, dataRow);
        elif (self.parametersPanel.tabControl.currentIndex() == 1):
            DlgAixmStar.smethod_0(ProcedureExportDlg.dataBase.STARs, ProcedureExportDlg.dataBase.ProcedureData, dataRow);
        elif (self.parametersPanel.tabControl.currentIndex() == 2):
            DlgAixmIap.smethod_0(ProcedureExportDlg.dataBase.IAPs, ProcedureExportDlg.dataBase.ProcedureData, dataRow);
        elif (self.parametersPanel.tabControl.currentIndex() == 3):
            DlgAixmHolding.smethod_0(ProcedureExportDlg.dataBase.Holdings, ProcedureExportDlg.dataBase.ProcedureData, dataRow);
        self.method_32()
    def btnProcRemove_Click(self):
        dataRow = self.selectedProcedureRow;
        if (dataRow == None):
            return;
        if (QMessageBox.question(self, "Question", "Are you sure you want to delete the selected procedure?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
            return;
        dataRow["deleted"] = "True";
        self.method_32()
        pass
    def tabControl_CurrentChanged(self, index):
        widget = self.parametersPanel.tabControl.currentWidget()
        widget.layout().addWidget(self.parametersPanel.splitContainer)
        self.method_32()

    def gridProcedures_pressed(self):
        self.method_34()
    def method_32(self):
        self.parametersPanel.pnlFile.Value = "";
        self.parametersPanel.lblEffectiveDate.setText("");
        self.parametersPanel.gridProceduresStdModel.clear();
        self.parametersPanel.gridLegsStdModel.clear();
        self.parametersPanel.gridLegsExStdModel.clear();
        if (ProcedureExportDlg.dataBase != None):
            self.parametersPanel.pnlFile.Value = ProcedureExportDlg.dataBase.FileName;
            self.parametersPanel.lblEffectiveDate.setText(ProcedureExportDlg.dataBase.EffectiveDate.toString());
            if (self.parametersPanel.tabControl.currentIndex() == 0):
                self.parametersPanel.gridProceduresStdModel.DataSource = ProcedureExportDlg.dataBase.SIDs;
                self.parametersPanel.gridProceduresSortModel.setFilterKeyColumn(19)
            elif (self.parametersPanel.tabControl.currentIndex() == 1):
                self.parametersPanel.gridProceduresStdModel.DataSource = ProcedureExportDlg.dataBase.STARs;
                self.parametersPanel.gridProceduresSortModel.setFilterKeyColumn(18)
            elif (self.parametersPanel.tabControl.currentIndex() == 2):
                self.parametersPanel.gridProceduresStdModel.DataSource = ProcedureExportDlg.dataBase.IAPs;
                self.parametersPanel.gridProceduresSortModel.setFilterKeyColumn(20)
            elif (self.parametersPanel.tabControl.currentIndex() == 3):
                self.parametersPanel.gridProceduresStdModel.DataSource = ProcedureExportDlg.dataBase.Holdings;
                self.parametersPanel.gridProceduresSortModel.setFilterKeyColumn(10)
        self.method_33();
        self.method_34();
        QSortFilterProxyModel.setFilterFixedString(self.parametersPanel.gridProceduresSortModel, "False")
        if self.parametersPanel.gridProceduresSortModel.rowCount() > 0:
            self.parametersPanel.gridProcedures.setCurrentIndex(self.parametersPanel.gridProceduresSortModel.index(0,0))
            self.gridProcedures_pressed()
    def method_33(self):
        num = None;
        strArrays = ["ID", "mgpEnt", "codeRnp", "txtDescrComFail", "txtDescr", "txtDescrMiss", "txtRmk", "new", "changed", "deleted", "oldBasedOnEnt", "oldCodeType", "oldAhpEnt", "oldTxtDesig", "oldCodeCatAcft", "oldCodeTransId", "procLegsEx", "procLegs", "ocah"];
        strArrays1 = strArrays;
        colCount = self.parametersPanel.gridProceduresStdModel.columnCount()
        for i in range(colCount):
            colItem = self.parametersPanel.gridProceduresStdModel.horizontalHeaderItem(i)
            flag = False
            for str0 in strArrays1:
                if colItem.text() == str0:
                    flag = True
                    break
            if not flag:
                self.parametersPanel.gridProcedures.setColumnHidden(i, False)
                dataPropertyName = colItem.text()
                strS = dataPropertyName;
                if (dataPropertyName == ""):
                    continue;
                if strS == "ahpEnt":
                    colItem.setText("Aerodrome")
                elif strS == "txtDesig":
                    colItem.setText("Designator")
                elif strS == "codeCatAcft":
                    colItem.setText("Ac. Category")
                elif strS == "codeTransId":
                    colItem.setText("Transition ID")
                elif strS == "rdnEnt":
                    colItem.setText("Runway / FATO")
                elif strS == "codeTypeRte":
                    colItem.setText("Type")
                elif strS == "codeRnp":
                    colItem.setText("RNP")
                elif strS == "basedOnEnt":
                    colItem.setText("Based On")
                elif strS == "codeType":
                    colItem.setText("Type")
            else:
                self.parametersPanel.gridProcedures.setColumnHidden(i, True)
    def method_34(self):
        selectedIndexes = self.parametersPanel.gridProcedures.selectedIndexes()
        if selectedIndexes != None and len(selectedIndexes) >= 1:
            dataRow = self.selectedProcedureRow;
            if (dataRow != None):
                item = dataRow["procLegs"];
                if (item != None):
                    self.parametersPanel.gridLegsStdModel.DataSource = item;
                    # self.gridLegs.AutoResizeColumns(DataGridViewAutoSizeColumnsMode.DisplayedCells);
                dataBaseProcedureLegsEx = dataRow["procLegsEx"];
                if (dataBaseProcedureLegsEx != None):
                    self.parametersPanel.gridLegsExStdModel.DataSource = dataBaseProcedureLegsEx;
                    # self.gridLegsEx.AutoResizeColumns(DataGridViewAutoSizeColumnsMode.DisplayedCells);
    def method_35(self, int_0):
        pass
        # if (int_0 > 0):
        #     # self.parametersPanel.gridProcedures.setCurrentIndex().Rows[int_0].Selected = true;
        #     this.gridProcedures.CurrentCell = this.gridProcedures.Rows[int_0].Cells[this.gridProcedures.Columns.GetFirstColumn(DataGridViewElementStates.Displayed).Index];
        # }
    def method_40(self):
        ProcedureExportDlg.dataBase = self.loaderAixm.dataBase
        self.method_32()

    def method_41(self):
        filePathDir = QFileDialog.getOpenFileName(self, "Open Data",QCoreApplication.applicationDirPath (),"XML Files (*.xml)")
        if filePathDir == "":
            return
        self.parametersPanel.pnlFile.Value = filePathDir
        fileInfo = QFileInfo(filePathDir)
        self.directory = fileInfo.filePath()

        self.loaderAixm.method_1(filePathDir, True);

        self.method_40()
    def method_42(self, list_0, dataBaseProcedureLegs_0):
        if (dataBaseProcedureLegs_0 == None):
            return;
        for dataBaseProcedureLegs0 in dataBaseProcedureLegs_0:
            pointEnt = dataBaseProcedureLegs0.PointEnt;
            centerEnt = dataBaseProcedureLegs0.CenterEnt;
            indexFlag = False
            try:
                temp = list_0.index(pointEnt)
                indexFlag = True
            except:
                pass
            if ((pointEnt.__class__ == ProcEntityPCP or pointEnt.__class__ == ProcEntityDPN) and pointEnt.Custom and not indexFlag):
                list_0.append(pointEnt);
            indexFlag = False
            try:
                temp = list_0.index(centerEnt)
                indexFlag = True
            except:
                pass
            if (not (centerEnt.__class__ == ProcEntityPCP) and not (centerEnt.__class__ == ProcEntityDPN) or not centerEnt.Custom or indexFlag):
                continue;
            list_0.append(centerEnt);
    def method_43(self, list_0, dataBaseProcedureLegsEx_0):
        if (dataBaseProcedureLegsEx_0 == None):
            return;
        for dataBaseProcedureLegsEx0 in dataBaseProcedureLegsEx_0:
            pointEnt = dataBaseProcedureLegsEx0.PointEnt;
            centerEnt = dataBaseProcedureLegsEx0.CenterEnt;
            indexFlag = False
            try:
                temp = list_0.index(pointEnt)
                indexFlag = True
            except:
                pass
            if ((pointEnt.__class__ == ProcEntityPCP or pointEnt.__class__ == ProcEntityDPN) and pointEnt.Custom and not indexFlag):
                list_0.append(pointEnt);
            indexFlag = False
            try:
                temp = list_0.index(centerEnt)
                indexFlag = True
            except:
                pass
            if (not (centerEnt.__class__ == ProcEntityPCP) and not (centerEnt.__class__ == ProcEntityDPN) or not centerEnt.Custom or indexFlag):
                continue;
            list_0.append(centerEnt);

    def get_selectedProcedureRow(self):
        if self.parametersPanel.gridProceduresStdModel.DataSource == None:
            return None

        selectedIndexes = self.parametersPanel.gridProcedures.selectedIndexes()
        if selectedIndexes != None and len(selectedIndexes) >= 1:
            col = len(self.parametersPanel.gridProceduresStdModel.hLabelList) - 1
            row = self.parametersPanel.gridProcedures.selectedIndexes()[0].row()
            modelIndex = self.parametersPanel.gridProceduresSortModel.index(row, col)
            itemVariant = self.parametersPanel.gridProceduresSortModel.itemData(modelIndex)

            # rowID = itemVariant[0].toInt()
            rowID = itemVariant[0].toInt()[0]
            return self.parametersPanel.gridProceduresStdModel.DataSource[rowID]
        else:
            return None

    selectedProcedureRow = property(get_selectedProcedureRow, None, None, None)

    def get_newProcedurePointsInUse(self):
        procEntityBases = [];
        dataRowArray = ProcedureExportDlg.dataBase.SIDs.Select({"deleted":"False"})#("isnull(deleted, false) = false");
        for i in range(len(dataRowArray)):
            dataRow = dataRowArray[i];
            self.method_42(procEntityBases, dataRow["procLegs"]);
            self.method_43(procEntityBases, dataRow["procLegsEx"]);
        dataRowArray1 = ProcedureExportDlg.dataBase.STARs.Select({"deleted":"False"})#("isnull(deleted, false) = false");
        for j in range(len(dataRowArray1)):
            dataRow1 = dataRowArray1[j];
            self.method_42(procEntityBases, dataRow1["procLegs"]);
            self.method_43(procEntityBases, dataRow1["procLegsEx"]);
        dataRowArray2 = ProcedureExportDlg.dataBase.IAPs.Select({"deleted":"False"})#("isnull(deleted, false) = false");
        for k in  range(len(dataRowArray2)):
            dataRow2 = dataRowArray2[k];
            self.method_42(procEntityBases, dataRow2["procLegs"]);
            self.method_43(procEntityBases, dataRow2["procLegsEx"]);
        dataRowArray3 = ProcedureExportDlg.dataBase.Holdings.Select({"deleted":"False"})#("isnull(deleted, false) = false");
        for l in range(len(dataRowArray3)):
            dataRow3 = dataRowArray3[l];
            item = dataRow3["basedOnEnt"];
            indexFlag = False
            try:
                temp = procEntityBases.index(item)
                indexFlag = True
            except:
                pass
            try:
                if (item.Custom and not indexFlag):
                    procEntityBases.append(item);
            except:
                pass
            self.method_42(procEntityBases, dataRow3["procLegs"]);
            self.method_43(procEntityBases, dataRow3["procLegsEx"]);
        return procEntityBases;
    newProcedurePointsInUse = property(get_newProcedurePointsInUse, None, None, None)