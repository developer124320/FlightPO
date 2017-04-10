# -*- coding: UTF-8 -*-

'''

Created on 30 Jun 2014

@author: Administrator
'''
from PyQt4.QtCore import SIGNAL, QCoreApplication, QString, QUrl, QSize
from PyQt4.QtGui import QFileDialog, QIcon, QPixmap, QDesktopServices, QApplication
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.types import SurfaceTypes
from FlightPlanner.FasDataBlock.ui_FasDataBlock import Ui_FasDataBlock
from FlightPlanner.types import Point3D
from Type.Degrees import Degrees
from Type.FasDataBlockFile import FasDataBlockFile
from FlightPlanner.Dialogs.DlgFasDataBlockImport import DlgFasDataBlockImport
from FlightPlanner.QgisHelper import QgisHelper
import define, Type.ByteFunc
import urllib
import urlparse

def url_fix(s, charset='utf-8'):
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))
class FasDataBlockDlg(FlightPlanBaseDlg):
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)

        s = QString("safggjkk")
        x = s.mid(3, 2)

        # dlg = DlgHelp()
        # dlg.exec_()

        self.setObjectName("PathTerminatorsDlg")
        self.surfaceType = SurfaceTypes.FasDataBlock
        self.selectedRow = None
        self.editingModelIndex = None

        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.FasDataBlock)
        self.resize(540, 550)
        QgisHelper.matchingDialogSize(self, 630, 700)
        self.surfaceList = None



        ss = bytearray(40)
        s = len(ss)
        pass
    #     # print "int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}".format("FF", 16)
    #
    #     d = int('-0xFF', 16)
    #     # sss = ord(ss)
    #     a = oct('0xFF')
    #     for c in s:
    #         x= c
    #
    #     n = bytearray(20)
    #     b = len(n)
    #     s = b
    #
    #
    # def sfcas(self):
    #     pass

    def uiStateInit(self):
        self.ui.grbMostCritical.setVisible(False)
        self.ui.grbResult_2.setVisible(False)
        # self.ui.btnUpdateQA.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.btnUpdateQA_2.setVisible(False)
        self.ui.frm_cmbObstSurface.setVisible(False)
        self.ui.tabCtrlGeneral.removeTab(2)
        self.ui.tabCtrlGeneral.removeTab(1)
        # self.ui.btnUpdateQA.setText("")
        # self.ui.btnUpdateQA.setFixedWidth(28)
        self.ui.btnUpdateQA.setEnabled(True)
        self.ui.btnUpdateQA.setToolTip("Help")
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/btnImage/help.png"), QIcon.Normal, QIcon.Off)

        self.ui.btnUpdateQA.setIcon(icon)
        self.ui.btnUpdateQA.setIconSize(QSize(32,32))

        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/import.png"), QIcon.Normal, QIcon.Off)
        self.ui.btnConstruct.setIcon(icon)
        self.ui.btnConstruct.setToolTip("Import")

        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/export.png"), QIcon.Normal, QIcon.Off)
        self.ui.btnPDTCheck.setIcon(icon)
        self.ui.btnPDTCheck.setToolTip("Export")

        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/dataClear.png"), QIcon.Normal, QIcon.Off)
        self.ui.btnEvaluate.setIcon(icon)
        self.ui.btnEvaluate.setToolTip("Clear")
        self.ui.btnEvaluate.setEnabled(True)

        #         self.ui.btnPDTCheck.clicked.connect(self.btnPDTCheck_Click)
        return FlightPlanBaseDlg.uiStateInit(self)

    def btnEvaluate_Click(self):  #### ---------------  Clear  -------------------###
        self.parametersPanel.pnlOperationType.SelectedIndex = 0
        self.parametersPanel.pnlSbasProvider.SelectedIndex = 0
        self.parametersPanel.pnlAirportId.Value = ""
        self.parametersPanel.txtRunwayDesignator.Value = 0
        self.parametersPanel.cmbRunwayLetter.SelectedIndex = 0
        self.parametersPanel.pnlApproachPerformanceDesignator.SelectedIndex = 0
        self.parametersPanel.pnlRouteIndicator.SelectedIndex = -1
        self.parametersPanel.pnlReferencePathDataSelector.Value = 0
        self.parametersPanel.pnlReferencePathId.Value = ""
        self.parametersPanel.pnlLtpFtpEllipsoidalHeight.Value = 0
        self.parametersPanel.txtApproachTCH.Value = 0
        self.parametersPanel.cmbApproachTCHunits.SelectedIndex = 0
        self.parametersPanel.pnlGPA.Value = 0.0
        self.parametersPanel.pnlLengthOffset.Value = 0
        self.parametersPanel.pnlHAL.Value = 0.0
        self.parametersPanel.pnlVAL.Value = 0.0
        self.parametersPanel.txtDataBlock.Value = ""
        self.parametersPanel.pnlCRC.Value = ""
        self.parametersPanel.pnlIcaoCode.Value = ""
        self.parametersPanel.pnlLtpFtpOrthoHeight.Value = 0
        self.parametersPanel.pnlFpapOrthoHeight.Value = 0
        self.parametersPanel.pnlCourseWidth.Value = 0
        self.parametersPanel.pnlLtpFtp.Point3d = None
        self.parametersPanel.pnlFpap.Point3d = None
        # self.method_30()

    def btnConstruct_Click(self):  ### ---------------  Import  ---------------------###
        fasDataBlockFile = DlgFasDataBlockImport.smethod_0(self);
        if (fasDataBlockFile != None):
            self.method_33(fasDataBlockFile);


    def btnPDTCheck_Click(self):  ### ---------------  Export  ---------------------###
        try:
            fasDataBlockFile = self.method_32(True);
        except:
            pass
        if (fasDataBlockFile == None):
            return;
        filePathDir = QFileDialog.getSaveFileName(self, "Export Data",QCoreApplication.applicationDirPath (),"FAS Data Block Binary Files (*.bin)")
        if filePathDir == "":
            return
        # DataHelper.saveInputParameters(filePathDir, self)
        # return filePathDir
        fasDataBlockFile.method_2(filePathDir)#self.sfd.FileName)
        # this.sfd.FileName = "";
        # if (this.sfd.ShowDialog(this) == System.Windows.Forms.DialogResult.OK)
        # {
        #     fasDataBlockFile.method_2(this.sfd.FileName);

    def initParametersPan(self):
        ui = Ui_FasDataBlock()
        self.parametersPanel = ui
        FlightPlanBaseDlg.initParametersPan(self)

        self.parametersPanel.pnlOperationType.Items = ["StraightInOffset",
                                                       "spare1",
                                                       "spare2",
                                                       "spare3",
                                                       "spare4",
                                                       "spare5",
                                                       "spare6",
                                                       "spare7",
                                                       "spare8",
                                                       "spare9",
                                                       "spare10",
                                                       "spare11",
                                                       "spare12",
                                                       "spare13",
                                                       "spare14",
                                                       "spare15"]

        self.parametersPanel.pnlSbasProvider.Items = ["WAAS",
                                                      "EGNOS",
                                                      "MSAS",
                                                      "GAGAN",
                                                      "SDCM",
                                                      "spare5",
                                                      "spare6",
                                                      "spare7",
                                                      "spare8",
                                                      "spare9",
                                                      "spare10",
                                                      "spare11",
                                                      "spare12",
                                                      "spare13",
                                                      "GBASonly",
                                                      "AnySBASprovider"]

        self.parametersPanel.cmbRunwayLetter.Items = ["None", "R", "C", "L"]
        self.parametersPanel.pnlApproachPerformanceDesignator.Items = ["APV", "Cat1", "Cat2", "Cat3", "spare4",
                                                                       "spare5", "spare6", "spare7"]
        self.parametersPanel.pnlRouteIndicator.Items = ["", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N",
                                                        "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.parametersPanel.cmbApproachTCHunits.Items = ["ft", "m"]

        # self.parametersPanel.pnlSbasProvider.SelectedIndex = 1
        # self.parametersPanel.pnlRouteIndicator.SelectedIndex = 4
        # self.parametersPanel.cmbRunwayLetter.SelectedIndex = 2
        # self.parametersPanel.pnlLtpFtp.Point3d = Point3D(10.511416667, 1.169722222222222e-4)
        # self.parametersPanel.pnlFpap.Point3d = Point3D(16.136785166667, 58.58778436111111)
        # a = 'a'
        # b = 1


        self.ui.btnUpdateQA.clicked.connect(self.btnUpdateQA_clicked)
        # self.parametersPanel.btnRemove.clicked.connect(self.btnRemove_clicked)
        # self.parametersPanel.btnDown.clicked.connect(self.btnDown_clicked)
        # self.parametersPanel.btnUp.clicked.connect(self.btnUp_clicked)
        # self.parametersPanel.pnlWpt.txtID.textChanged.connect(self.pnlWpt_positionChanged)
        #
        self.connect(self.parametersPanel.pnlVAL, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.pnlHAL, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.pnlLengthOffset, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.pnlCourseWidth, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.pnlLtpFtp, SIGNAL("positionChanged"), self.method_34)
        self.connect(self.parametersPanel.pnlFpap, SIGNAL("positionChanged"), self.method_34)
        self.connect(self.parametersPanel.pnlGPA, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.txtApproachTCH, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.cmbApproachTCHunits, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.pnlLtpFtpEllipsoidalHeight, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.pnlReferencePathId, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.pnlReferencePathDataSelector, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.pnlRouteIndicator, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.pnlApproachPerformanceDesignator, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.txtRunwayDesignator, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.cmbRunwayLetter, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.pnlAirportId, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.pnlSbasProvider, SIGNAL("Event_0"), self.method_34)
        self.connect(self.parametersPanel.pnlOperationType, SIGNAL("Event_0"), self.method_34)
        self.btnEvaluate_Click()
        # self.method_31(False);
    def btnUpdateQA_clicked(self):
        path = define.appPath
        path = path + "/Resource/FasDataBlockHelp.html"
        # path = url_fix(path)
        # print path
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))

        # print QUrl.fromLocalFile(path).errorString()
    def method_30(self):
        self.parametersPanel.pnlOperationType.SelectedIndex = -1;
        self.parametersPanel.pnlSbasProvider.SelectedIndex = -1;
        self.parametersPanel.pnlAirportId.Value = "";
        self.parametersPanel.txtRunwayDesignator.Value = 0;
        self.parametersPanel.cmbRunwayLetter.SelectedIndex = -1;
        self.parametersPanel.pnlApproachPerformanceDesignator.SelectedIndex = -1;
        self.parametersPanel.pnlRouteIndicator.SelectedIndex = -1;
        self.parametersPanel.pnlReferencePathDataSelector.Value = 0;
        self.parametersPanel.pnlReferencePathId.Value = "";
        self.parametersPanel.pnlLtpFtp.Point3d = None
        self.parametersPanel.pnlLtpFtpEllipsoidalHeight.Value = 0;
        self.parametersPanel.pnlFpap.Point3d = None
        self.parametersPanel.txtApproachTCH.Value = 0;
        self.parametersPanel.cmbApproachTCHunits.SelectedIndex = -1;
        self.parametersPanel.pnlGPA.Value = 0;
        self.parametersPanel.pnlCourseWidth.Value = 0;
        self.parametersPanel.pnlLengthOffset.Value = 0;
        self.parametersPanel.pnlHAL.Value = 0;
        self.parametersPanel.pnlVAL.Value = 0;
        self.parametersPanel.pnlIcaoCode.Value = "";
        self.parametersPanel.pnlLtpFtpOrthoHeight.Value = 0;
        self.parametersPanel.pnlFpapOrthoHeight.Value = 0;
        self.method_31(False);
    
    def method_31(self, bool_0):
        try:
            fasDataBlockFile = self.method_32(bool_0);
        except:
            return
        if (fasDataBlockFile == None):
            self.parametersPanel.txtDataBlock.Value = "";
            self.parametersPanel.pnlCRC.Value = "";
            return;
        self.parametersPanel.txtDataBlock.Value = fasDataBlockFile.HexString;
        self.parametersPanel.pnlCRC.Value = fasDataBlockFile.CRC;
    
    def method_32(self, bool_0):
        # degree = Degrees();
        # degree1 = Degrees();
        # degree2 = Degrees();
        # degree3 = Degrees();
        # if (not self.method_29(bool_0))
        # {
        #     return null;
        # }
        fasDataBlockFile = FasDataBlockFile()
        fasDataBlockFile.set_OperationType(self.parametersPanel.pnlOperationType.Value)
        fasDataBlockFile.set_SbasProviderId(self.parametersPanel.pnlSbasProvider.Value)
        fasDataBlockFile.set_AirportId(self.parametersPanel.pnlAirportId.Value.toUpper())
        fasDataBlockFile.set_RunwayNumber(Type.ByteFunc.d2b(self.parametersPanel.txtRunwayDesignator.Value))
        fasDataBlockFile.set_RunwayLetter(self.parametersPanel.cmbRunwayLetter.Value)
        fasDataBlockFile.set_ApproachPerformanceDesignator(self.parametersPanel.pnlApproachPerformanceDesignator.Value)
        fasDataBlockFile.set_RouteIndicator(self.parametersPanel.pnlRouteIndicator.SelectedItem)
        fasDataBlockFile.set_ReferencePathDataSelector(Type.ByteFunc.d2b(self.parametersPanel.pnlReferencePathDataSelector.Value))
        fasDataBlockFile.set_ReferencePathIdentifier(self.parametersPanel.pnlReferencePathId.Value)
        result, degree, degree1 = self.parametersPanel.pnlLtpFtp.method_3()
        if (not result):
            return None
            # throw new Exception(Geo.LastError);
        fasDataBlockFile.set_LtpFtpLatitude(degree);
        fasDataBlockFile.set_LtpFtpLongitude(degree1)
        fasDataBlockFile.set_LtpFtpHeight(self.parametersPanel.pnlLtpFtpEllipsoidalHeight.Value)
        result1, degree2, degree3 = self.parametersPanel.pnlFpap.method_3()
        if (not result1):
            return None
            # throw new Exception(Geo.LastError);

        fasDataBlockFile.set_DeltaFpapLatitude(degree2 - degree);
        fasDataBlockFile.set_DeltaFpapLongitude(degree3 - degree1);
        fasDataBlockFile.method_0(self.parametersPanel.txtApproachTCH.Value, self.parametersPanel.cmbApproachTCHunits.Value);
        fasDataBlockFile.set_GPA(self.parametersPanel.pnlGPA.Value)
        fasDataBlockFile.set_CourseWidth(self.parametersPanel.pnlCourseWidth.Value)
        fasDataBlockFile.set_DeltaLengthOffset(self.parametersPanel.pnlLengthOffset.Value);
        fasDataBlockFile.set_HAL(self.parametersPanel.pnlHAL.Value);
        fasDataBlockFile.set_VAL(self.parametersPanel.pnlVAL.Value);
        return fasDataBlockFile;
    
    def method_33(self, fasDataBlockFile_0):
        if (fasDataBlockFile_0 == None):
            self.method_30();
            return;
        self.parametersPanel.pnlOperationType.SelectedIndex = fasDataBlockFile_0.OperationType
        self.parametersPanel.pnlSbasProvider.SelectedIndex = fasDataBlockFile_0.SbasProviderId;
        self.parametersPanel.pnlAirportId.Value = fasDataBlockFile_0.AirportId;
        self.parametersPanel.txtRunwayDesignator.Value = float(fasDataBlockFile_0.RunwayNumber);
        self.parametersPanel.cmbRunwayLetter.SelectedIndex = fasDataBlockFile_0.RunwayLetter;
        self.parametersPanel.pnlApproachPerformanceDesignator.SelectedIndex = fasDataBlockFile_0.ApproachPerformanceDesignator;
        self.parametersPanel.pnlRouteIndicator.SelectedItem = fasDataBlockFile_0.RouteIndicator;
        self.parametersPanel.pnlReferencePathDataSelector.Value = float(fasDataBlockFile_0.ReferencePathDataSelector);
        self.parametersPanel.pnlReferencePathId.Value = fasDataBlockFile_0.ReferencePathIdentifier;
        deltaFpapLatitude = fasDataBlockFile_0.LtpFtpLatitude;
        deltaFpapLongitude = fasDataBlockFile_0.LtpFtpLongitude;
        self.parametersPanel.pnlLtpFtp.Point3d = Point3D(deltaFpapLongitude, deltaFpapLatitude);
        self.parametersPanel.pnlLtpFtpEllipsoidalHeight.Value = fasDataBlockFile_0.LtpFtpHeight;
        deltaFpapLatitude = deltaFpapLatitude + fasDataBlockFile_0.DeltaFpapLatitude;
        deltaFpapLongitude = deltaFpapLongitude + fasDataBlockFile_0.DeltaFpapLongitude;
        self.parametersPanel.pnlFpap.Point3d = Point3D(deltaFpapLongitude, deltaFpapLatitude);
        self.parametersPanel.txtApproachTCH.Value = fasDataBlockFile_0.ApproachTch;
        self.parametersPanel.cmbApproachTCHunits.SelectedIndex = fasDataBlockFile_0.ApproachTchUnits;
        self.parametersPanel.pnlGPA.Value = fasDataBlockFile_0.GPA;
        self.parametersPanel.pnlCourseWidth.Value = fasDataBlockFile_0.CourseWidth;
        self.parametersPanel.pnlLengthOffset.Value = fasDataBlockFile_0.DeltaLengthOffset;
        self.parametersPanel.pnlHAL.Value = fasDataBlockFile_0.HAL;
        self.parametersPanel.pnlVAL.Value = fasDataBlockFile_0.VAL;
        self.method_31(False);

    def method_34(self):
        self.method_31(False);