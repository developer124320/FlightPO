# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication,QRect, Qt, QDateTime
from PyQt4.QtGui import QMessageBox, QFileDialog, QProgressBar, QApplication, QMenu
from PyQt4.QtXml import QDomNode, QDomElement, QDomDocument
from qgis.core import QGis, QgsVectorLayer
from qgis.gui import QgsRubberBand, QgsMapTool, QgsMapCanvasSnapper
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import SurfaceTypes, DistanceUnits, Point3D
from FlightPlanner.DataExport.ui_DataExport import Ui_DataExport
from FlightPlanner.QgisHelper import Geo
from map.tools import QgsMapToolSelectUtils
from FlightPlanner.helpers import MathHelper
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Captions import Captions
from FlightPlanner.messages import Messages
from Type.String import String, StringBuilder
from Type.CRC import CRC
from Type.Symbol import Symbol
from Type.Extensions import XmlNode
import define, math, HTMLParser


class DataExportDlg(FlightPlanBaseDlg):
    
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        
        self.delimiter = "";
        self.numFormat = "";
        self.latFormat = "";
        self.lonFormat = "";
        self.hasName = False;
        self.hasXY = False;
        self.hasLatLon = False;
        self.hasAlt = False;
        self.hasRadius = False;
        
        self.setObjectName("DataExportDlg")
        self.surfaceType = SurfaceTypes.DataExport
        self.selectedRow = None
        self.editingModelIndex = None

        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.DataExport)
        self.resize(540, 550)
        QgisHelper.matchingDialogSize(self, 540, 550)
        self.surfaceList = None
        self.fileStream = None



        # doc = QDomDocument()
        # a = doc.createElement("sam");
        # aa = XmlNode.smethod_30(a, "as", "323435")
        # aaa = XmlNode.smethod_30(aa, "ass", "323")
        # s = a.namedItem("as")
        # ss = s.namedItem("ass")
        # print ss.toElement().text()
        # ss = ''
        # for i in range(6):
        #     a.append(None)
        # a = Point3D()
        # b = Point3D(234, 2332)
        # if a.__class__ == b.__class__:
        #     pass
        # print a.__class__
        # strs = "c:/d/asfa/wsws.txt"
        # # for s in strs:
        # date = QDateTime.fromString("2012-02-09T00:00:00", "yyyy-MM-dd'T'hh:mm:ss")
        # d = date.toString("yyyy.MM.dd hh-mm-ss")


        # v = strs.index("sad")
        #
        # d = Degrees(55.9)
        # d1 = Degrees(55.9)
        # d2 = Degrees(55.900)
        # d3 = Degrees(43.9)
        # if d == d1:
        #     pass
        # if d2 == d1:
        #     pass
        # if d3 == d1:
        #     pass
        # a = {"s":"asd", "a":5}
        # for m in a:
        #     s = m
        #     pass
        # a["a"] = 10
        # model = QStandardItemModel()

        # model.setItem(0,0, QStandardItem("ass"))
        # model.setItem(0,1, QStandardItem("rr"))
        # s = model.item(0,0).text()
        # ss = model.item(0,1).text()
        pass

    
    def uiStateInit(self):

        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.btnConstruct.setVisible(False)
        self.ui.btnEvaluate.setToolTip("Export")
        self.ui.btnPDTCheck.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        self.ui.tabCtrlGeneral.removeTab(1)
        self.ui.btnEvaluate.setEnabled(True)
#         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)

    def btnEvaluate_Click(self):   #### ---------------  Export  -------------------###
        if ((not self.parametersPanel.chbName.Checked or not self.parametersPanel.chbName.Visible) and (not self.parametersPanel.chbXY.Checked or not self.parametersPanel.chbXY.Visible) and (not self.parametersPanel.chbLatLon.Checked or not self.parametersPanel.chbLatLon.Visible) and (not self.parametersPanel.chbAltitude.Checked and not self.parametersPanel.chbAltitude.Visible) and (not self.parametersPanel.chbRadius.Checked or not self.parametersPanel.chbRadius.Visible)):
            QMessageBox.warning(self, "Warning", Messages.ERR_NO_FIELDS_SELECTED)
            # base.method_20(Messages.ERR_NO_FIELDS_SELECTED);
            return;


        self.delimiter = self.method_30();
        self.numFormat = self.method_34();
        self.latFormat = self.method_32();
        self.lonFormat = self.method_33();
        exportObjectType = self.parametersPanel.cmbObjectType.SelectedItem
        if (exportObjectType == ExportObjectType.Circles):
            self.hasName = self.parametersPanel.chbName.Checked;
            self.hasXY = self.parametersPanel.chbXY.Checked;
            self.hasLatLon = self.parametersPanel.chbLatLon.Checked;
            self.hasAlt = self.parametersPanel.chbAltitude.Checked;
            self.hasRadius = self.parametersPanel.chbRadius.Checked;
            self.method_42();
        elif (exportObjectType == ExportObjectType.Blocks):
            self.hasName = self.parametersPanel.chbName.Checked;
            self.hasXY = self.parametersPanel.chbXY.Checked;
            self.hasLatLon = self.parametersPanel.chbLatLon.Checked;
            self.hasAlt = self.parametersPanel.chbAltitude.Checked;
            self.hasRadius = False;
            self.method_48();
        elif (exportObjectType == ExportObjectType.Lines):
            self.hasName = False;
            self.hasXY = self.parametersPanel.chbXY.Checked;
            self.hasLatLon = self.parametersPanel.chbLatLon.Checked;
            self.hasAlt = self.parametersPanel.chbAltitude.Checked;
            self.hasRadius = False;
            self.method_45();
        elif (exportObjectType == ExportObjectType.Polylines):
            self.hasName = False;
            self.hasXY = self.parametersPanel.chbXY.Checked;
            self.hasLatLon = self.parametersPanel.chbLatLon.Checked;
            self.hasAlt = self.parametersPanel.chbAltitude.Checked;
            self.hasRadius = False;
            self.method_44();
        elif (exportObjectType == ExportObjectType.Points):
            self.hasName = self.parametersPanel.chbName.Checked;
            self.hasXY = self.parametersPanel.chbXY.Checked;
            self.hasLatLon = self.parametersPanel.chbLatLon.Checked;
            self.hasAlt = self.parametersPanel.chbAltitude.Checked;
            self.hasRadius = False;
            self.method_46();
        elif (exportObjectType == ExportObjectType.Positions):
            self.hasName = self.parametersPanel.chbName.Checked;
            self.hasXY = self.parametersPanel.chbXY.Checked;
            self.hasLatLon = self.parametersPanel.chbLatLon.Checked;
            self.hasAlt = self.parametersPanel.chbAltitude.Checked;
            self.hasRadius = False;
            self.method_47();
    def btnConstruct_Click(self):   ### ---------------  Import  ---------------------###

        return FlightPlanBaseDlg.btnConstruct_Click(self)

    def btnPDTCheck_Click(self):    ### ---------------  Clear  ---------------------###
         pass
    def initParametersPan(self):
        ui = Ui_DataExport()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.cmbDelimiter.Items = ["Semicolon", "Comma", "Space", "Custom"]
        self.parametersPanel.cmbObjectType.Items = ["Circles", "Blocks", "Lines", "Points", "Polylines"]#,"Positions"]
        self.parametersPanel.cmbPolyType.Items = ["Contours", "Airspace", "Procedures"]
        self.parametersPanel.pnlSelectionMethod.Items = ["Automatic", "Manual"]
        self.parametersPanel.pnlLatLonFormat.Items = ["H(d)ddmmss.s...", "(d)ddmmss.s...H", "H(d)ddmmss.s...", "(d)ddmmss.s...H", "H(d)ddmm.m...", "(d)ddmm.m...H", "H(d)ddmm.m", "(d)ddmm.mH", "H(d)dd.d...", "(d)dd.d...H", "H(d)dd.d...", "(d)dd.d...H" ]
        self.parametersPanel.pnlNumberPrecision.Items = ["0", "0.0", "0.00", "0.000", "0.0000", "0.00000", "0.000000", "0.0000000", "0.00000000"]
        self.parametersPanel.pnlLatLonPrecision.Items = ["0", "0.0", "0.00", "0.000", "0.0000", "0.00000", "0.000000", "0.0000000", "0.00000000"]

        self.parametersPanel.pnlLatLonPrecision.SelectedIndex = 4
        self.parametersPanel.pnlNumberPrecision.SelectedIndex = 4
        self.parametersPanel.pnlLatLonFormat.SelectedIndex = 1
        self.parametersPanel.pnlSelectionMethod.SelectedIndex = 1
        # self.parametersPanel.btnAdd.clicked.connect(self.btnAdd_clicked)
        # self.parametersPanel.btnRemove.clicked.connect(self.btnRemove_clicked)
        # self.parametersPanel.btnDown.clicked.connect(self.btnDown_clicked)
        # self.parametersPanel.btnUp.clicked.connect(self.btnUp_clicked)
        # self.parametersPanel.pnlWpt.txtID.textChanged.connect(self.pnlWpt_positionChanged)
        #
        self.connect(self.parametersPanel.chbName, SIGNAL("Event_0"), self.chbName_Event_0)
        self.connect(self.parametersPanel.chbLatLon, SIGNAL("Event_0"), self.chbLatLon_Event_0)
        self.connect(self.parametersPanel.chbXY, SIGNAL("Event_0"), self.method_38)
        self.connect(self.parametersPanel.chbAltitude, SIGNAL("Event_0"), self.method_38)
        self.connect(self.parametersPanel.chbRadius, SIGNAL("Event_0"), self.method_38)
        self.connect(self.parametersPanel.cmbObjectType, SIGNAL("Event_0"), self.method_38)
        self.connect(self.parametersPanel.cmbDelimiter, SIGNAL("Event_0"), self.method_38)
        self.connect(self.parametersPanel.pnlTolerance, SIGNAL("Event_1"), self.method_40)
        self.connect(self.parametersPanel.pnlFile, SIGNAL("Event_1"), self.method_41)
        # self.connect(self.parametersPanel.pnlTurnDir, SIGNAL("Event_0"), self.pnlTurnDir_Event_0)
        # self.connect(self.parametersPanel.pnlCourse, SIGNAL("Event_0"), self.pnlCourse_Event_0)
        self.chbLatLon_Event_0()
        self.chbName_Event_0()
        self.method_38()
    def chbName_Event_0(self):

        self.parametersPanel.pnlTolerance.Enabled = self.parametersPanel.chbName.Checked
        self.method_38()
    def chbLatLon_Event_0(self):
        self.parametersPanel.pnlLatLonFormat.Enabled = self.parametersPanel.chbLatLon.Checked
        self.method_38()
        
    def method_30(self):
        if (self.parametersPanel.cmbDelimiter.SelectedIndex == 0):
            return ";";
        if (self.parametersPanel.cmbDelimiter.SelectedIndex == 1):
            return ",";
        if (self.parametersPanel.cmbDelimiter.SelectedIndex == 2):
            return " ";
        return self.parametersPanel.txtDelimiter.Value;
    def method_31(self, char_0, int_0, int_1):
        stringBuilder = "";
        for i in range(int_0):
            stringBuilder += char_0;
        if (int_1 > 0):
            stringBuilder += ".";
            for j in range(int_1):
                stringBuilder += char_0
        return stringBuilder
    
    def method_32(self):

        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 1):
            return String.Concat(["ddmm", self.method_31('s', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), "H"]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 2):
            return String.Concat(["Hddmm", self.method_31('s', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex)]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 3):
            return String.Concat(["ddmm", self.method_31('s', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), "H"]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 4):
            return String.Concat(["Hdd", self.method_31('m', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), ""]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 5):
            return String.Concat(["dd", self.method_31('m', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), "'H"]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 6):
            return String.Concat(["Hdd", self.method_31('m', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex)]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 7):
            return String.Concat(["dd", self.method_31('m', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), "H"]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 8):
            return String.Concat(["H", self.method_31('d', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), ""]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 9):
            return String.Concat([self.method_31('d', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), "H"]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 10):
            return String.Concat(["H", self.method_31('d', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex)]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 11):
            return String.Concat([self.method_31('d', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), "H"]);
        return String.Concat(["Hddmm'", self.method_31('s', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), ""]);
    
    def method_33(self):
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 1):
            return String.Concat(["dddmm", self.method_31('s', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), "H"]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 2):
            return String.Concat(["Hdddmm", self.method_31('s', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex)]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 3):
            return String.Concat(["dddmm", self.method_31('s', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), "H"]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 4):
            return String.Concat(["Hddd", self.method_31('m', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), ""]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 5):
            return String.Concat(["ddd", self.method_31('m', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), "H"]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 6):
            return String.Concat(["Hddd", self.method_31('m', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex)]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 7):
            return String.Concat(["ddd", self.method_31('m', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), "H"]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 8):
            return String.Concat(["H", self.method_31('d', 3, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), ""]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 9):
            return String.Concat([self.method_31('d', 3, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), "H"]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 10):
            return String.Concat(["H", self.method_31('d', 3, self.parametersPanel.pnlLatLonPrecision.SelectedIndex)]);
        if (self.parametersPanel.pnlLatLonFormat.SelectedIndex == 11):
            return String.Concat([self.method_31('d', 3, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), "H"]);
        return String.Concat(["Hdddmm", self.method_31('s', 2, self.parametersPanel.pnlLatLonPrecision.SelectedIndex), ""]);
    
    def method_34(self):
        return self.method_31('0', 1, self.parametersPanel.pnlNumberPrecision.SelectedIndex);
    
    def method_35(self):
        nAME = []
        if self.parametersPanel.chbCRC.Checked:
            for i in range(15):
                nAME.append("")
        else:
            for i in range(14):
                nAME.append("")
        strS = "";
        if self.parametersPanel.chbLatLon.Checked:#(Geo.DatumLoaded and self.chbLatLon.Checked)
            strS = " ({0})".format(define._canvas.mapSettings().destinationCrs().authid());
        nAME[0] = Captions.NAME;
        nAME[1] = Captions.X;
        nAME[2] = Captions.Y;
        nAME[3] = Captions.Z;
        nAME[4] = Captions.TYPE;
        nAME[5] = "{0} {1}".format(Captions.LATITUDE, strS);
        nAME[6] = "{0} {1}".format(Captions.LONGITUDE, strS);
        nAME[9] = Captions.RADIUS;
        nAME[10] = Captions.CENTER_X;
        nAME[11] = Captions.CENTER_Y;
        nAME[12] = "{0} {1}".format(Captions.CENTER_LATITUDE, strS);
        nAME[13] = "{0} {1}".format(Captions.CENTER_LONGITUDE, strS);
        if (self.parametersPanel.chbCRC.Checked):
            nAME[14] = "CRC32Q";
        return String.Join(self.delimiter, nAME);
    def method_36(self, string_0, point3d_0, double_0, string_1):
        # degree = 0.0;
        # degree1 = 0.0;
        if string_0 == None:
            string_0 = ""
        if double_0 == None:
            double_0 = 0.0
        if string_1 == None:
            string_1 = ""
        string0 = []
        if self.parametersPanel.chbCRC.Checked:
            for i in range(15):
                string0.append("")
        else:
            for i in range(14):
                string0.append("")
        # string0 = (self.chbCRC.Checked ? new string[15] : new string[14]);
        if (self.hasName):
            string0[0] = string_0;
        if (self.hasXY):
            x = point3d_0.x();
            string0[1] = str(x) #x.ToString(self.numFormat);
            y = point3d_0.y();
            string0[2] = str(y) #y.ToString(self.numFormat);
        if (self.hasAlt):
            z = point3d_0.get_Z();
            string0[3] = str(z) #z.ToString(self.numFormat);
        string0[4] = string_1
        if (self.hasLatLon):
            result, degree, degree1 = Geo.smethod_2(point3d_0.get_X(), point3d_0.get_Y())
            if (not result):
                return None
                # throw new Exception(Geo.LastError);
            string0[5] = degree.method_1(self.latFormat);
            string0[6] = degree1.method_1(self.lonFormat);
        if (self.hasRadius and (not math.isinf(double_0) and not math.isnan(double_0))):
            string0[9] = str(double_0)#.ToString(self.numFormat);
        if (self.parametersPanel.chbCRC.Checked):
            string0[14] = CRC.smethod_0(self.method_39(string0));
        return String.Join(self.delimiter, string0);
    
    def method_37(self, string_0, point3d_0, double_0, point3d_1, string_1):
        # degree = ;
        # Degrees degree1;
        # Degrees degree2;
        # Degrees degree3;
        string0 = []
        if self.parametersPanel.chbCRC.Checked:
            for i in range(15):
                string0.append("")
        else:
            for i in range(14):
                string0.append("")
        # string0 = (self.chbCRC.Checked ? new string[15] : new string[14]);
        if (self.hasName):
            string0[0] = string_0;
        if (self.hasXY):
            x = point3d_0.get_X();
            string0[1] = String.Number2String(x, self.numFormat);
            y = point3d_0.get_Y();
            string0[2] = String.Number2String(y, self.numFormat);
        if (self.hasAlt):
            z = point3d_0.get_Z();
            string0[3] = String(z, self.numFormat);
        string0[4] = string_1;
        if (self.hasLatLon):
            result, degree, degree1 = Geo.smethod_2(point3d_0.get_X(), point3d_0.get_Y())
            if (not result):
                return None
                # throw new Exception(Geo.LastError);
            string0[5] = degree.method_1(self.latFormat);
            string0[6] = degree1.method_1(self.lonFormat);
        if (self.hasRadius and  (not math.isnan(double_0) and not math.isinf(double_0))):
            string0[9] = String.Number2String(double_0, self.numFormat);
        if (not math.isnan(double_0) and not math.isinf(double_0)):
            if (self.hasXY):
                num = point3d_1.get_X();
                string0[10] = String.Number2String(num, self.numFormat);
                y1 = point3d_1.get_Y();
                string0[11] = String.Number2String(y1, self.numFormat);
            if (self.hasLatLon):
                result0, degree2, degree3 = Geo.smethod_2(point3d_1.get_X(), point3d_1.get_Y())
                if (not result0):
                    return None
                    # throw new Exception(Geo.LastError);
                string0[12] = degree2.method_1(self.latFormat);
                string0[13] = degree3.method_1(self.lonFormat);
        if (self.parametersPanel.chbCRC.Checked):
            string0[14] = CRC.smethod_0(self.method_39(string0));
        return String.Join(self.delimiter, string0);
    
    def method_38(self):

        self.parametersPanel.txtDelimiter.Enabled = self.parametersPanel.cmbDelimiter.SelectedIndex == 3;
        if self.parametersPanel.cmbDelimiter.Value == 0:
            self.parametersPanel.txtDelimiter.Value = ";"
        elif self.parametersPanel.cmbDelimiter.Value == 1:
            self.parametersPanel.txtDelimiter.Value = ","
        elif self.parametersPanel.cmbDelimiter.Value == 2:
            self.parametersPanel.txtDelimiter.Value = " "

        if (self.parametersPanel.cmbObjectType.SelectedIndex > -1):
            exportObjectType = self.parametersPanel.cmbObjectType.SelectedItem
            self.parametersPanel.pnlSelectionMethod.Visible = exportObjectType != ExportObjectType.Positions;
            self.parametersPanel.chbExcludeObjectsAtZero.Visible = exportObjectType != ExportObjectType.Positions;
            if exportObjectType == ExportObjectType.Circles:
                self.parametersPanel.cmbPolyType.Enabled = False;
                self.parametersPanel.chbName.Visible = True;
                self.parametersPanel.pnlTolerance.Visible = False;
                self.parametersPanel.chbRadius.Visible = True;
                self.parametersPanel.pnlNumberPrecision.Visible =True if(self.parametersPanel.chbXY.Checked or self.parametersPanel.chbAltitude.Checked) else self.parametersPanel.chbRadius.Checked;
                self.parametersPanel.pnlLatLonPrecision.Visible = self.parametersPanel.chbLatLon.Checked;
            elif exportObjectType == ExportObjectType.Blocks:
                self.parametersPanel.cmbPolyType.Enabled = False;
                self.parametersPanel.chbName.Visible = True;
                self.parametersPanel.pnlTolerance.Visible = False;
                self.parametersPanel.chbRadius.Visible = False;
                self.parametersPanel.pnlNumberPrecision.Visible = True if(self.parametersPanel.chbXY.Checked or self.parametersPanel.chbAltitude.Checked) else self.parametersPanel.chbRadius.Checked;
                self.parametersPanel.pnlLatLonPrecision.Visible = self.parametersPanel.chbLatLon.Checked;
            elif exportObjectType == ExportObjectType.Lines:
                self.parametersPanel.cmbPolyType.Enabled = False;
                self.parametersPanel.chbName.Visible = False;
                self.parametersPanel.pnlTolerance.Visible = False;
                self.parametersPanel.chbRadius.Visible = False;
                self.parametersPanel.pnlNumberPrecision.Visible = True if(self.parametersPanel.chbXY.Checked) else self.parametersPanel.chbAltitude.Checked;
                self.parametersPanel.pnlLatLonPrecision.Visible = self.parametersPanel.chbLatLon.Checked;
            elif exportObjectType == ExportObjectType.Points:
                self.parametersPanel.cmbPolyType.Enabled = False;
                self.parametersPanel.chbName.Visible = True;
                self.parametersPanel.pnlTolerance.Visible = True;
                self.parametersPanel.chbRadius.Visible = False;
                self.parametersPanel.pnlNumberPrecision.Visible = True if(self.parametersPanel.chbXY.Checked) else self.parametersPanel.chbAltitude.Checked;
                self.parametersPanel.pnlLatLonPrecision.Visible = self.parametersPanel.chbLatLon.Checked;
            elif exportObjectType == ExportObjectType.Polylines:
                self.parametersPanel.cmbPolyType.Enabled = True;
                self.parametersPanel.chbName.Visible = False;
                self.parametersPanel.pnlTolerance.Visible = False;
                self.parametersPanel.chbRadius.Visible = False;
                self.parametersPanel.pnlNumberPrecision.Visible = True if(self.parametersPanel.chbXY.Checked) else self.parametersPanel.chbAltitude.Checked;
                self.parametersPanel.pnlLatLonPrecision.Visible = self.parametersPanel.chbLatLon.Checked;
            elif exportObjectType == ExportObjectType.Positions:
                self.parametersPanel.cmbPolyType.Enabled = False;
                self.parametersPanel.chbName.Visible = True;
                self.parametersPanel.pnlTolerance.Visible = False;
                self.parametersPanel.chbRadius.Visible = False;
                self.parametersPanel.pnlNumberPrecision.Visible = True if(self.parametersPanel.chbXY.Checked) else self.parametersPanel.chbAltitude.Checked;
                self.parametersPanel.pnlLatLonPrecision.Visible = self.parametersPanel.chbLatLon.Checked;
        if self.parametersPanel.pnlTolerance.Visible:
            self.parametersPanel.chbName.setMinimumWidth(185)
    def method_39(self, string_0):
        stringBuilder = StringBuilder();
        for i in range(14):
            if (not String.IsNoneOrEmpty(string_0[i])):
                stringBuilder.Append(string_0[i]);
        return stringBuilder.ToString();
    def method_40(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.pnlTolerance.numberBox, DistanceUnits.M)
        define._canvas.setMapTool(measureDistanceTool)
            # double num;
            # if (AcadHelper.Ready and AcadHelper.smethod_84(this, Prompts.TOLERANCE, out num))
            # {
            # 	this.pnlTolerance.Value = num;
    def method_41(self):
        filePathDir = QFileDialog.getSaveFileName(self, "Save Data",QCoreApplication.applicationDirPath (),"CSV Files (*.csv);; Text Files (*.txt)")
        if filePathDir == "":
            return
        if filePathDir.right(3) == "csv":
            self.parametersPanel.cmbDelimiter.SelectedIndex = 1
            self.parametersPanel.cmbDelimiter.Enabled = False
            self.parametersPanel.txtDelimiter.Enabled = False
        self.parametersPanel.pnlFile.Value = filePathDir
    def method_42(self):
        if (self.parametersPanel.pnlSelectionMethod.SelectedItem != ExportMethodType.Automatic):
            selectTool = SelectTool(define._canvas, "Circle")
            define._canvas.setMapTool(selectTool)
            self.connect(selectTool, SIGNAL("outputResult"), self.selectFeatureResult)
        else:
            selectedFeatures, selectedLayers = self.allSelectFeatures("Circle")
            if len(selectedFeatures) != 0:
                self.selectFeatureResult(selectedFeatures, selectedLayers, "Circle")
            pass
    def method_43(self, streamWriter_0, string_0, list_0, bool_0):
        point3d = None;
        point3d1 = None;
        point3d2 = None;
        exportPolyType = self.parametersPanel.cmbPolyType.SelectedItem
        count = len(list_0);
        for i in range(count):
            item = list_0[i];
            strS = "";
            if (MathHelper.smethod_96(item.Bulge) or i >= count - 1 and not bool_0):
                if (not string_0 == None and not string_0 == ""):
                    if (i == 0):
                        strS = "s";
                    elif (i == count - 1):
                        strS = ((not bool_0) and "f" or "fc");
                streamWriter_0.Append(self.method_36(None, item.Position, None, String.Concat([string_0, strS])));
                streamWriter_0.Append("\n")
            else:
                point3d = (i >= count - 1) and list_0[0].Position or list_0[i + 1].Position;
                point3d1 = MathHelper.smethod_71(item.Position, point3d, item.Bulge);
                num = MathHelper.calcDistance(point3d1, point3d);
                num1 = math.atan(math.fabs(item.Bulge)) * 4;
                point3d2 = (item.Bulge <= 0) and MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(point3d1, item.Position) + num1 / 2, num) or MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(point3d1, item.Position) - num1 / 2, num)
                strS = (i != 0) and "a" or "as"
                if (exportPolyType == ExportPolyType.Airspace):
                    streamWriter_0.Append(self.method_37(None, item.Position, num, point3d1, String.Concat([string_0, strS])));
                    streamWriter_0.Append("\n")
                else:
                    streamWriter_0.Append(self.method_36(None, item.Position, None, String.Concat([string_0, strS])));
                    streamWriter_0.Append("\n")
                streamWriter_0.Append(self.method_36(None, point3d2, None, String.Concat([string_0, "m"])));
                streamWriter_0.Append("\n")
                if (i == count - 1):
                    streamWriter_0.Append(self.method_36(None, point3d, None, String.Concat([string_0, "fc"])));
                    streamWriter_0.Append("\n")
    def allSelectFeatures(self, selectType):
        resultFeatures = []
        layers = define._canvas.layers()
        selectedLayers = []
        if len(layers) != 0:

            for ly in layers:
                if selectType == "Points":
                    feats = []
                    ly._class_ = QgsVectorLayer
                    iter = ly.getFeatures()
                    for feature in iter:
                        feats.append(feature)
                    resultFeatures.append(feats)
                    selectedLayers.append(ly)
                    continue
                if selectType == "Blocks":
                    if ly.geometryType() == QGis.Line:
                        continue
                else:
                    if ly.geometryType() == QGis.Point:
                        continue
                if selectType == "Blocks":
                    feats = []
                    ly._class_ = QgsVectorLayer
                    iter = ly.getFeatures()
                    for feature in iter:
                        feats.append(feature)
                    resultFeatures.append(feats)
                    selectedLayers.append(ly)

                else:
                    ly._class_ = QgsVectorLayer
                    iter = ly.getFeatures()
                    feats = []
                    for feature in iter:
                        try:
                            type = feature.attribute("Type").toString()
                        except:
                            type = "Polyline"
                        if selectType == type:
                            feats.append(feature)
                    resultFeatures.append(feats)
                    selectedLayers.append(ly)
        return resultFeatures, selectedLayers
    def method_44(self):
        if (self.parametersPanel.pnlSelectionMethod.SelectedItem != ExportMethodType.Automatic):
            selectTool = SelectTool(define._canvas, "Polyline")
            define._canvas.setMapTool(selectTool)
            self.connect(selectTool, SIGNAL("outputResult"), self.selectFeatureResult)
        else:
            selectedFeatures, selectedLayers = self.allSelectFeatures("Polyline")
            if len(selectedFeatures) != 0:
                self.selectFeatureResult(selectedFeatures, selectedLayers, "Polyline")
            pass
            # AcadHelper.smethod_75();
            # selection = activeDocument.get_Editor().SelectAll(new SelectionFilter(typedValues.ToArray()));
        # }
    def method_45(self):
        if (self.parametersPanel.pnlSelectionMethod.SelectedItem != ExportMethodType.Automatic):
            selectTool = SelectTool(define._canvas, "Line")
            define._canvas.setMapTool(selectTool)
            self.connect(selectTool, SIGNAL("outputResult"), self.selectFeatureResult)
        else:
            selectedFeatures, selectedLayers = self.allSelectFeatures("Line")
            if len(selectedFeatures) != 0:
                self.selectFeatureResult(selectedFeatures, selectedLayers, "Line")
            pass
    def method_46(self):
        if (self.parametersPanel.pnlSelectionMethod.SelectedItem != ExportMethodType.Automatic):
            selectTool = SelectTool(define._canvas, "Points")
            define._canvas.setMapTool(selectTool)
            self.connect(selectTool, SIGNAL("outputResult"), self.selectFeatureResult)
        else:
            selectedFeatures, selectedLayers = self.allSelectFeatures("Points")
            if len(selectedFeatures) != 0:
                self.selectFeatureResult(selectedFeatures, selectedLayers, "Points")
    def method_48(self):
        if (self.parametersPanel.pnlSelectionMethod.SelectedItem != ExportMethodType.Automatic):
            selectTool = SelectTool(define._canvas, "Blocks")
            define._canvas.setMapTool(selectTool)
            self.connect(selectTool, SIGNAL("outputResult"), self.selectFeatureResult)
        else:
            selectedFeatures, selectedLayers = self.allSelectFeatures("Blocks")
            if len(selectedFeatures) != 0:
                self.selectFeatureResult(selectedFeatures, selectedLayers, "Blocks")
    def selectFeatureResult(self, selectedFeatures, selectedLayer, selectType):
        if selectedFeatures == None or len(selectedFeatures) == 0:
            return
        progressMessageBar = define._messagBar.createMessage("Writing file...")
        progress = QProgressBar()
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(progress)
        define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
        maxium = len(selectedFeatures)
        progress.setMaximum(maxium)
        progress.setValue(0)

        filePath = String.QString2Str(self.parametersPanel.pnlFile.Value)



        strinBuilder = StringBuilder()
        strinBuilder.Append(self.method_35());
        strinBuilder.Append("\n")
        if selectType == "Polyline":


            exportPolyType = self.parametersPanel.cmbPolyType.SelectedItem
            strS = None;
            if exportPolyType == ExportPolyType.Contours:
                strS = "c";
            elif exportPolyType == ExportPolyType.Airspace:
                strS = "a";
            elif exportPolyType == ExportPolyType.Procedures:
                strS = "p";

            for feats in selectedFeatures:
                i = 1

                for feat in feats:
                    exportPolylineVertexTypes = []
                    pointList = feat.geometry().asPolyline()
                    bulge = 0.0
                    try:
                        bulge = feat.attribute("Bulge").toFloat()[0]
                    except:
                        bulge = 0.0
                    altitudeStringList = None
                    try:
                        altitudeStringList = feat.attribute("Altitude").toString().split(",")
                    except:
                        altitudeStringList = None
                    if bulge == 0.0:
                        j = 0
                        for point in pointList:
                            point3d = None
                            if altitudeStringList != None:
                                point3d = Point3D(point.x(), point.y(), altitudeStringList[j].toFloat()[0])
                            else:
                                point3d = Point3D(point.x(), point.y())
                            exportPolylineVertexTypes.append(ExportPolylineVertexType(point3d, 0.0));
                            j += 1
                    else:
                        if altitudeStringList != None:
                            point3d = Point3D(pointList[0].x(), pointList[0].y(), altitudeStringList[0].toFloat()[0])
                        else:
                            point3d = Point3D(pointList[0].x(), pointList[0].y())
                        exportPolylineVertexTypes.append(ExportPolylineVertexType(point3d, bulge));

                        if altitudeStringList != None:
                            point3d = Point3D(pointList[len(pointList) - 1].x(), pointList[len(pointList) - 1].y(), altitudeStringList[1].toFloat()[0])
                        else:
                            point3d = Point3D(pointList[len(pointList) - 1].x(), pointList[len(pointList) - 1].y())
                        exportPolylineVertexTypes.append(ExportPolylineVertexType(point3d, bulge));
                    self.method_43(strinBuilder, strS, exportPolylineVertexTypes, pointList[0] == pointList[len(pointList) - 1]);
                    progress.setValue(i)
                    QApplication.processEvents()
                    i += 1

        elif selectType == "Circle":
            j = 0
            for ly in selectedLayer:
                if ly != None and define._units == QGis.Meters and ly.crs().mapUnits() == QGis.Degrees and ly.geometryType() == QGis.Point:
                    i = 0
                    for feat in ly.selectedFeatures ():
                        point0 = feat.geometry().asPoint()
                        point = QgisHelper.CrsTransformPoint(point0.x(), point0.y(), ly.crs(), define._xyCrs)
                        altitude = 0.0
                        try:
                            altitude = feat.attribute("Altitude").toDouble()[0]
                        except:
                            altitude = 0.0
                        point3d = Point3D(point.x(), point.y(), altitude)
                        # point3d = Point3D(667412.5559, 6618232.7877, 58.553)

                        name = ""
                        if self.parametersPanel.chbName.Checked:
                            try:
                                name = feat.attribute("Name").toString()
                            except:
                                name = ""
                        strinBuilder.Append(self.method_36(name, point3d, 0.1, None) + "\n")

                        i += 1
                        progress.setValue(i)
                        QApplication.processEvents()
                else:#if selectedLayer.geometryType() == QGis.Line:
                    i = 0
                    for feat in selectedFeatures[j]:
                        centerPointStrList = None
                        try:
                            centerPointStrList = feat.attribute("CenterPt").toString().split(",")
                        except:
                            pass
                        point3d = None
                        if centerPointStrList == None:
                            point3d = Point3D(0,0)
                        else:
                            point3d = Point3D(float(centerPointStrList[0]), float(centerPointStrList[1]), float(centerPointStrList[2]))

                        radius = 0.0
                        try:
                            radius = feat.attribute("Bulge").toFloat()[0]
                        except:
                            radius = 0.0

                        strinBuilder.Append(self.method_36("", point3d, radius, None) + "\n")

                        i += 1
                        progress.setValue(i)
                        QApplication.processEvents()
                j += 1
        elif selectType == "Line":
            for feats in selectedFeatures:
                i = 1
                for feat in feats:
                    exportPolylineVertexTypes = []
                    pointList = feat.geometry().asPolyline()

                    caption = None
                    try:
                        caption = feat.attribute("Caption").toString()
                    except:
                        caption = None
                    if caption != None and caption != "":
                        continue

                    altitudeStringList = None
                    try:
                        altitudeStringList = feat.attribute("Altitude").toString().split(",")
                    except:
                        altitudeStringList = None
                    if altitudeStringList != None and len(altitudeStringList) > 1:
                        point3dS = Point3D(pointList[0].x(), pointList[0].y(), altitudeStringList[0].toFloat()[0])
                        point3dF = Point3D(pointList[1].x(), pointList[1].y(), altitudeStringList[1].toFloat()[0])
                    else:
                        point3dS = Point3D(pointList[0].x(), pointList[0].y())
                        point3dF = Point3D(pointList[1].x(), pointList[1].y())

                    strinBuilder.Append(self.method_36(None, point3dS, None, "rs") + "\n")
                    strinBuilder.Append(self.method_36(None, point3dF, None, "rf") + "\n")
                    progress.setValue(i)
                    QApplication.processEvents()
                    i += 1

        elif selectType == "Blocks":
            if isinstance(selectedLayer, list):
                j = 0
                for ly in selectedLayer:
                    if selectedLayer != None and define._units == QGis.Meters and ly.crs().mapUnits() == QGis.Degrees and ly.geometryType() == QGis.Point:

                        i = 1
                        maxium = len(selectedFeatures[j])
                        progress.setMaximum(maxium)
                        progress.setValue(0)
                        for feat in selectedFeatures[j]:
                            point0 = feat.geometry().asPoint()
                            if point0.y() > 90:
                                point = Point3D(point0.x(), point0.y())
                            else:
                                point = QgisHelper.CrsTransformPoint(point0.x(), point0.y(), ly.crs(), define._xyCrs)

                            altitude = 0.0
                            try:
                                altitude = feat.attribute("Altitude").toDouble()[0]
                            except:
                                altitude = 0.0
                            point3d = Point3D(point.x(), point.y(), altitude)
                            typeStr = ""
                            try:
                                typeStr = feat.attribute("Type").toString()
                            except:
                                typeStr = ""
                            name = ""
                            try:
                                name = feat.attribute("Name").toString()
                            except:
                                name = ""
                            symbol = Symbol.smethod_4(typeStr);
                            if (symbol == None):
                                dbCode = None;
                            else:
                                dbCode = symbol.DbCode;
                            strS = dbCode;
                            strinBuilder.Append(self.method_36(name, point3d, None, strS) + "\n");
                            progress.setValue(i)
                            QApplication.processEvents()
                            i += 1
                        j += 1
        elif selectType == "Points":
            if isinstance(selectedLayer, list):
                j = 0
                for ly in selectedLayer:
                    if selectedLayer != None and define._units == QGis.Meters and ly.crs().mapUnits() == QGis.Degrees and ly.geometryType() == QGis.Point:

                        i = 1
                        if len(selectedLayer) == 1:
                            list0 = selectedFeatures[j]
                        else:
                            list0 = selectedFeatures[j]
                        maxium = len(list0)
                        progress.setMaximum(maxium)
                        progress.setValue(0)
                        for feat in list0:
                            point0 = feat.geometry().asPoint()
                            point = QgisHelper.CrsTransformPoint(point0.x(), point0.y(), ly.crs(), define._xyCrs)

                            altitude = 0.0
                            try:
                                altitude = feat.attribute("Altitude").toDouble()[0]
                            except:
                                altitude = 0.0
                            point3d = Point3D(point.x(), point.y(), altitude)
                            if (self.hasName):
                                strS = ""
                                try:
                                    strS = feat.attribute("Caption").toString()
                                except:
                                    strS = ""
                            else:
                                strS = None;
                            str1 = strS;

                            strinBuilder.Append(self.method_36(str1, point3d, None, None) + "\n");
                            progress.setValue(i)
                            QApplication.processEvents()
                            i += 1

                    elif ly.geometryType() == QGis.Line:
                        i = 1
                        if len(selectedLayer) == 1:
                            list0 = selectedFeatures[j]
                        else:
                            list0 = selectedFeatures[j]
                        maxium = len(list0)
                        progress.setMaximum(maxium)
                        progress.setValue(0)
                        for feat in list0:
                            pointList = feat.geometry().asPolyline()
                            point = Point3D(pointList[0].x(), pointList[0].y())

                            altitude = 0.0
                            try:
                                altitude = feat.attribute("Altitude").toDouble()[0]
                            except:
                                altitude = 0.0
                            point3d = Point3D(point.x(), point.y(), altitude)
                            if (self.hasName):
                                strS = ""
                                try:
                                    strS = feat.attribute("Caption").toString()
                                except:
                                    strS = ""
                            else:
                                strS = None;
                            str1 = strS;

                            strinBuilder.Append(self.method_36(str1, point3d, None, None) + "\n");
                            progress.setValue(i)
                            QApplication.processEvents()
                            i += 1
                    j += 1

        printStr = None
        if self.parametersPanel.chbUnicode.Checked:
            printStr = unicode(strinBuilder.ToString())
        else:
            printStr = strinBuilder.ToString()
        # printStr = unicode("Name;X;Y;Z;Type;Latitude  (EPSG:32633);Longitude  (EPSG:32633);;;Radius;Center X;Center Y;Center Latitude  (EPSG:32633);Center Longitude  (EPSG:32633);CRC32Q ESSA;662296.900881;6617664.55853;81.095;;59")
        progress.setValue(maxium)
        define._messagBar.hide()
        streamWriter = open(filePath, 'w')
        streamWriter.write(printStr)
        streamWriter.close()



class ExportPolylineVertexType:
    def __init__(self,  point3d_0, double_0):
        self.Position = point3d_0
        self.Bulge = double_0;
class ExportMethodType:
    Automatic = "Automatic"
    Manual = "Manual"

class ExportObjectType:
    Circles = "Circles"
    Blocks = "Blocks"
    Lines = "Lines"
    Points = "Points"
    Polylines = "Polylines"
    Positions = "Positions"

class ExportPolyType:
    Contours = "Contours"
    Airspace = "Airspace"
    Procedures = "Procedures"

class SelectTool(QgsMapTool):

    def __init__(self, canvas, selectType = None):
        self.mCanvas = canvas
        # self.areaType = areaType
        QgsMapTool.__init__(self, canvas)
        self.mCursor = Qt.ArrowCursor
        self.mRubberBand = None
        self.mDragging = False
        self.mSelectRect = QRect()
        self.mRubberBandResult = None
        self.mSnapper = QgsMapCanvasSnapper(canvas)
        self.lineCount = 0
        self.resultFeatureList = []
        self.geomList = []
        self.area = None
        self.isFinished = False
        self.selectType = selectType

        self.outFeatures = []
        self.menuClick = False

    def createContextMenu(self):
        menu = QMenu()
        # h = QHBoxLayout(menu)
        # c = QCalendarWidget()
        # h.addWidget(c)

        actionFinish = QgisHelper.createAction(menu, "Finish", self.menuFinishClick)
        menu.addAction(actionFinish)
        return menu
    def menuFinishClick(self):
        self.menuClick = True
    def canvasPressEvent(self, e):
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        self.mSelectRect.setRect( 0, 0, 0, 0 )
        self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
        self.startPoint, self.pointID, self.layer= self.snapPoint(e.pos())

    def canvasMoveEvent(self, e):
        if ( e.buttons() != Qt.LeftButton ):
            return
        if ( not self.mDragging ):
            self.mDragging = True
            self.mSelectRect.setTopLeft( e.pos() )
        self.mSelectRect.setBottomRight( e.pos() )
        QgsMapToolSelectUtils.setRubberBand( self.mCanvas, self.mSelectRect,self.mRubberBand )

    def canvasReleaseEvent(self, e):
        # if( e.button() == Qt.RightButton ):
        #     menu = self.createContextMenu()
        #     menu.exec_( define._canvas.mapToGlobal(e.pos() ))
        self.endPoint, self.pointID, self.layer= self.snapPoint(e.pos())

        vlayer = QgsMapToolSelectUtils.getCurrentVectorLayer( self.mCanvas )

        if ( vlayer == None ):
            if ( self.mRubberBand != None):
                self.mRubberBand.reset( QGis.Polygon )
                del self.mRubberBand
                self.mRubberBand = None
                self.mDragging = False
            return

        # if self.menuClick:
        #     self.emit(SIGNAL("outputResult"), self.outFeatures, [vlayer], self.selectType)
        #     self.mRubberBand.reset( QGis.Polygon )
        #     del self.mRubberBand
        #     self.mRubberBand = None
        #     self.mDragging = False
        #     self.menuClick = False
        #     return



        if (not self.mDragging ):
            QgsMapToolSelectUtils.expandSelectRectangle(self. mSelectRect, vlayer, e.pos() )
        else:
            if ( self.mSelectRect.width() == 1 ):
                self.mSelectRect.setLeft( self.mSelectRect.left() + 1 )
            if ( self.mSelectRect.height() == 1 ):
                self.mSelectRect.setBottom( self.mSelectRect.bottom() + 1 )

        if ( self.mRubberBand != None ):
            QgsMapToolSelectUtils.setRubberBand( self.mCanvas, self.mSelectRect, self.mRubberBand )
            selectGeom = self.mRubberBand.asGeometry()


            selectedFeatures = QgsMapToolSelectUtils.setSelectFeaturesOrRubberband_Tas_1( self.mCanvas, selectGeom, e )
            if len(selectedFeatures) > 0:
                if self.selectType != None:
                    resultFeatures = None
                    if vlayer.geometryType() != QGis.Point:
                        if self.selectType == "Points":
                            resultFeatures = []
                            for feat in selectedFeatures:
                                try:
                                    type = feat.attribute("Type").toString()
                                except:
                                    type = "Polyline"
                                try:
                                    caption = feat.attribute("Caption").toString()
                                except:
                                    caption = ""
                                if type == "Line" and caption != "":
                                    resultFeatures.append(feat)
                        else:
                            resultFeatures = []
                            for feat in selectedFeatures:
                                try:
                                    type = feat.attribute("Type").toString()
                                except:
                                    type = "Polyline"

                                if self.selectType == "Polyline" and (type == "Polyline" or type == ""):
                                    resultFeatures.append(feat)
                                elif self.selectType == type:
                                    resultFeatures.append(feat)
                    else:
                        resultFeatures = selectedFeatures
                    self.outFeatures.extend(resultFeatures)
                    self.emit(SIGNAL("outputResult"), [resultFeatures], [vlayer], self.selectType)
                else:
                    self.outFeatures.extend(selectedFeatures)
                    self.emit(SIGNAL("outputResult"), [selectedFeatures], [vlayer], self.selectType)


            del selectGeom

            self.mRubberBand.reset( QGis.Polygon )
            del self.mRubberBand
            self.mRubberBand = None
        self.mDragging = False

    def snapPoint(self, p, bNone = False):
        if define._snapping == False:
            return (define._canvas.getCoordinateTransform().toMapCoordinates( p ), None, None)
        snappingResults = self.mSnapper.snapToBackgroundLayers( p )
        if ( snappingResults[0] != 0 or len(snappingResults[1]) < 1 ):

            if bNone:
                return (None, None, None)
            else:
                return (define._canvas.getCoordinateTransform().toMapCoordinates( p ), None, None)
        else:
            return (snappingResults[1][0].snappedVertex, snappingResults[1][0].snappedAtGeometry, snappingResults[1][0].layer)

