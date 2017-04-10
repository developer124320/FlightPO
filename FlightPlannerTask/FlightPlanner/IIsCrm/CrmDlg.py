'''
Created on 25 May 2014

@author: Administrator
'''
from PyQt4.QtGui import QMessageBox, QFileDialog,QColor, QPushButton, QMessageBox, QProgressBar
from PyQt4.QtCore import QCoreApplication,Qt,QFileInfo, QFile, SIGNAL, QDir, QString
from FlightPlanner.IIsCrm.ui_CrmDlg import Ui_CrmDlg
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.FlightPlanBaseDlg import FlightPlanBaseDlg
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.types import IlsCrmYesNoType, IlsCrmCategoryType, IlsCrmMinimumType, IlsCrmRiskType, Point3D
from FlightPlanner.Captions import Captions
from FlightPlanner.validations import Validations
from FlightPlanner.helpers import MathHelper
from FlightPlanner.helpers import Unit, DistanceUnits
from FlightPlanner import QgisHelper
from map.tools import SelectByRect, QgsMapToolSelectFreehand, QgsMapToolSelectPolygon, QgsMapToolSelectRadius
import define
import math
from FlightPlanner.types import SurfaceTypes
from FlightPlanner.QgisHelper import QgisHelper
from qgis.gui import QgsMapTool, QgsRubberBand
from FlightPlanner.MeasureTool import MeasureTool
from qgis.core import QGis, QgsVectorFileWriter, QgsGeometry, QgsCsException, QgsPoint,\
        QgsFeatureRequest, QgsCoordinateTransform, QgsFeature, QgsVectorLayer
import os
import ctypes, win32api
# import os, datetime



class CrmDlg(FlightPlanBaseDlg):
    def __init__(self, parent):
        FlightPlanBaseDlg.__init__(self, parent)
        self.setObjectName("CRM")
        self.surfaceType = SurfaceTypes.CRM
        self.initParametersPan()
        self.setWindowTitle(SurfaceTypes.CRM)
        self.method_28()
        self.resize(700, 550)
        QgisHelper.matchingDialogSize(self, 700, 600)
        self.toolSelectByPolygon = None
        self.currentDir = os.getcwdu()

        self.arpFeatureArray = []
        self.currentLayer = define._canvas.currentLayer()
        self.rwyFeatureArray = []
        self.locFeatureList = []
        self.initAerodromeAndRwyCmb()
    def initAerodromeAndRwyCmb(self):

        if self.currentLayer != None and self.currentLayer.isValid() and isinstance(self.currentLayer, QgsVectorLayer):
            self.arpFeatureArray = self.aerodromeAndRwyCmbFill(self.currentLayer, self.parametersPanel.cmbAerodrome, None, self.parametersPanel.cmbRwyDir)
            # self.calcRwyBearing()
    def calcRwyBearing(self):
        try:
            point3End = self.parametersPanel.pnlThrEnd.Point3d
            point3dThr = self.parametersPanel.pnlThr.Point3d
            self.parametersPanel.pnlRwyDir.Value = round(Unit.ConvertRadToDeg(MathHelper.getBearing(point3dThr, point3End)), 4)
        except:
            pass


#         self.ui.horizontalLayout_6.addWidget(self.ui.frame_3)
    def aerodromeAndRwyCmbFill(self, layer, aerodromeCmbObj, aerodromePositionPanelObj, rwyDirCmbObj = None):
        idx = layer.fieldNameIndex('Type')
        idxName = layer.fieldNameIndex('Name')
        idxLat = layer.fieldNameIndex('Latitude')
        idxLong = layer.fieldNameIndex('Longitude')
        idxAltitude = layer.fieldNameIndex('Altitude')
        idxAttr = layer.fieldNameIndex('Attributes')
        arpList = []
        arpFeatureList = []
        locList = []
        self.locFeatureList = []
        if idx >= 0:
            featIter = layer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idx].toString()
                attrValue = QString(attrValue)
                attrValue = attrValue.replace(" ", "")
                attrValue = attrValue.toUpper()
                if attrValue == "AERODROMEREFERENCEPOINT":
                    arpList.append(attrValue)
                    arpFeatureList.append(feat)
                elif attrValue == "BASICRADIONAVIGATIONAID":
                    attrValue = feat.attributes()[idxAttr].toString()
                    attrValue = QString(attrValue)
                    attrValue = attrValue.replace(" ", "")
                    attrValue = attrValue.toUpper()
                    if attrValue.contains("ILSLOCALIZER"):
                        locList.append(attrValue)
                        self.locFeatureList.append(feat)
            if len(locList) != 0:

                i = -1
                for feat in self.locFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    self.parametersPanel.cmbLocalizer.Add(attrValue)
                self.parametersPanel.cmbLocalizer.SelectedIndex = 0

                # if idxAttributes
                for feat in self.locFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    if attrValue != self.parametersPanel.cmbLocalizer.SelectedItem:
                        continue
                    attrValue = feat.attributes()[idxLat].toDouble()
                    lat = attrValue[0]

                    attrValue = feat.attributes()[idxLong].toDouble()
                    long = attrValue[0]

                    attrValue = feat.attributes()[idxAltitude].toDouble()
                    alt = attrValue[0]

                    self.parametersPanel.pnlLoc.Point3d = Point3D(long, lat, alt)
                    self.connect(self.parametersPanel.cmbLocalizer, SIGNAL("Event_0"), self.cmbLocalizer_Event_0)
                    break
            if len(arpList) != 0:

                i = -1
                aerodromeCmbObjItems = []
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    items = aerodromeCmbObjItems
                    if len(items) != 0:
                        existFlag = False
                        for item in items:
                            if item == attrValue:
                                existFlag = True
                        if existFlag:
                            continue
                    aerodromeCmbObjItems.append(attrValue)
                aerodromeCmbObjItems.sort()
                aerodromeCmbObj.Items = aerodromeCmbObjItems
                aerodromeCmbObj.SelectedIndex = 0

                # if idxAttributes
                for feat in arpFeatureList:
                    attrValue = feat.attributes()[idxName].toString()
                    if attrValue != aerodromeCmbObj.SelectedItem:
                        continue
                    attrValue = feat.attributes()[idxLat].toDouble()
                    lat = attrValue[0]

                    attrValue = feat.attributes()[idxLong].toDouble()
                    long = attrValue[0]

                    attrValue = feat.attributes()[idxAltitude].toDouble()
                    alt = attrValue[0]

                    # aerodromePositionPanelObj.Point3d = Point3D(long, lat, alt)
                    self.connect(aerodromeCmbObj, SIGNAL("Event_0"), self.aerodromeCmbObj_Event_0)
                    break
            if rwyDirCmbObj != None:

                if idxAttr >= 0:
                    rwyFeatList = []
                    featIter = layer.getFeatures()
                    rwyDirCmbObjItems = []
                    for feat in featIter:
                        attrValue = feat.attributes()[idxAttr].toString()
                        if attrValue == aerodromeCmbObj.SelectedItem:
                            attrValue = feat.attributes()[idxName].toString()
                            s = attrValue.replace(" ", "")
                            compStr = s.left(6).toUpper()
                            if compStr == "THRRWY":
                                valStr = s.right(s.length() - 6)
                                rwyDirCmbObjItems.append(aerodromeCmbObj.SelectedItem + " RWY " + valStr)
                                rwyFeatList.append(feat)
                    rwyDirCmbObjItems.sort()
                    rwyDirCmbObj.Items = rwyDirCmbObjItems
                    self.connect(rwyDirCmbObj, SIGNAL("Event_0"), self.rwyDirCmbObj_Event_0)
                    self.rwyFeatureArray = rwyFeatList
                    self.rwyDirCmbObj_Event_0()

                    self.aerodromeCmbObj_Event_0()
                    # self.calcRwyBearing()
        return arpFeatureList
    def cmbLocalizer_Event_0(self):
        if len(self.locFeatureList) > 0:
            idxName = self.currentLayer.fieldNameIndex('Name')
            idxLat = self.currentLayer.fieldNameIndex('Latitude')
            idxLong = self.currentLayer.fieldNameIndex('Longitude')
            idxAltitude = self.currentLayer.fieldNameIndex('Altitude')
            idxAttr = self.currentLayer.fieldNameIndex('Attributes')
            # for feat in self.locFeatureList:
            #     attrValue = feat.attributes()[idxName].toString()
            #     self.parametersPanel.cmbLocalizer.Add(attrValue)
            # self.parametersPanel.cmbLocalizer.SelectedIndex = 0

            # if idxAttributes
            for feat in self.locFeatureList:
                attrValue = feat.attributes()[idxName].toString()
                if attrValue != self.parametersPanel.cmbLocalizer.SelectedItem:
                    continue
                attrValue = feat.attributes()[idxLat].toDouble()
                lat = attrValue[0]

                attrValue = feat.attributes()[idxLong].toDouble()
                long = attrValue[0]

                attrValue = feat.attributes()[idxAltitude].toDouble()
                alt = attrValue[0]

                self.parametersPanel.pnlLoc.Point3d = Point3D(long, lat, alt)
                    # self.connect(self.parametersPanel.cmbLocalizer, SIGNAL("Event_0"), self.cmbLocalizer_Event_0)
                    # break
    def rwyDirCmbObj_Event_0(self):
        if len(self.rwyFeatureArray) == 0:
            return
        idxName = self.currentLayer.fieldNameIndex('Name')
        idxLat = self.currentLayer.fieldNameIndex('Latitude')
        idxLong = self.currentLayer.fieldNameIndex('Longitude')
        idxAltitude = self.currentLayer.fieldNameIndex('Altitude')
        idxAttr = self.currentLayer.fieldNameIndex('Attributes')

        for feat in self.rwyFeatureArray:
            attrValue = feat.attributes()[idxName].toString()
            attrValueStr = QString(attrValue)
            attrValueStr = attrValueStr.replace(" ", "").right(attrValueStr.length() - 3)
            itemStr = self.parametersPanel.cmbRwyDir.SelectedItem
            itemStr = QString(itemStr)
            itemStr = itemStr.replace(" ", "").right(itemStr.length() - 4)
            if attrValueStr != itemStr:
                continue
            latAttrValue = feat.attributes()[idxLat].toDouble()
            lat = latAttrValue[0]

            longAttrValue = feat.attributes()[idxLong].toDouble()
            long = longAttrValue[0]

            altAttrValue = feat.attributes()[idxAltitude].toDouble()
            alt = altAttrValue[0]

            self.parametersPanel.pnlThr.Point3d = Point3D(long, lat, alt)

            valStr = None
            if attrValue.right(1).toUpper() =="L" or attrValue.right(1).toUpper() =="R":
                s = attrValue.left(attrValue.length() - 1)
                valStr = s.right(2)
            else:
                valStr = attrValue.right(2)
            val = int(valStr)
            val += 18
            if val > 36:
                val -= 36
            newValStr = None
            if len(str(val)) == 1:
                newValStr = "0" + str(val)
            else:
                newValStr = str(val)
            otherAttrValue = attrValue.replace(valStr, newValStr)
            ss = otherAttrValue.right(1)
            if ss.toUpper() == "L":
                otherAttrValue = otherAttrValue.left(otherAttrValue.length() - 1) + "R"
            elif ss.toUpper() == "R":
                otherAttrValue = otherAttrValue.left(otherAttrValue.length() - 1) + "L"
            for feat in self.rwyFeatureArray:
                attrValue = feat.attributes()[idxName].toString()
                if attrValue != otherAttrValue:
                    continue
                latAttrValue = feat.attributes()[idxLat].toDouble()
                lat = latAttrValue[0]

                longAttrValue = feat.attributes()[idxLong].toDouble()
                long = longAttrValue[0]

                altAttrValue = feat.attributes()[idxAltitude].toDouble()
                alt = altAttrValue[0]

                # self.parametersPanel.pnlThrEnd.Point3d = Point3D(long, lat, alt)
                break
            break
        # self.calcRwyBearing()
    def aerodromeCmbObj_Event_0(self):
        if len(self.arpFeatureArray) == 0:
            return
        # self.parametersPanel.pnlArp.Point3d = None
        self.parametersPanel.pnlThr.Point3d = None
        # self.parametersPanel.pnlThrEnd.Point3d = None
        idxName = self.currentLayer.fieldNameIndex('Name')
        idxLat = self.currentLayer.fieldNameIndex('Latitude')
        idxLong = self.currentLayer.fieldNameIndex('Longitude')
        idxAltitude = self.currentLayer.fieldNameIndex('Altitude')
        self.rwyFeatureArray = []
        # if idxAttributes
        for feat in self.arpFeatureArray:
            attrValue = feat.attributes()[idxName].toString()
            if attrValue != self.parametersPanel.cmbAerodrome.SelectedItem:
                continue
            attrValue = feat.attributes()[idxLat].toDouble()
            lat = attrValue[0]

            attrValue = feat.attributes()[idxLong].toDouble()
            long = attrValue[0]

            attrValue = feat.attributes()[idxAltitude].toDouble()
            alt = attrValue[0]

            # self.parametersPanel.pnlArp.Point3d = Point3D(long, lat, alt)
            break
        idxAttr = self.currentLayer.fieldNameIndex('Attributes')
        if idxAttr >= 0:
            self.parametersPanel.cmbRwyDir.Clear()
            rwyFeatList = []
            featIter = self.currentLayer.getFeatures()
            for feat in featIter:
                attrValue = feat.attributes()[idxAttr].toString()
                if attrValue == self.parametersPanel.cmbAerodrome.SelectedItem:
                    attrValue = feat.attributes()[idxName].toString()
                    s = attrValue.replace(" ", "")
                    compStr = s.left(6).toUpper()
                    if compStr == "THRRWY":
                        valStr = s.right(s.length() - 6)
                        self.parametersPanel.cmbRwyDir.Add(self.parametersPanel.cmbAerodrome.SelectedItem + " RWY " + valStr)
                        rwyFeatList.append(feat)
                        self.rwyFeatureArray = rwyFeatList
            self.rwyDirCmbObj_Event_0()

    def initParametersPan(self):
        ui = Ui_CrmDlg()
        self.parametersPanel = ui
        
        FlightPlanBaseDlg.initParametersPan(self)
        
        '''init panel'''

        
        self.parametersPanel.cmbC13.addItems([IlsCrmYesNoType.Yes, IlsCrmYesNoType.No])
        self.parametersPanel.cmbC13a.addItems([IlsCrmYesNoType.Yes, IlsCrmYesNoType.No])
        self.parametersPanel.cmbC14.addItems([IlsCrmYesNoType.Yes, IlsCrmYesNoType.No])
        self.parametersPanel.cmbC15.addItems([IlsCrmYesNoType.Yes, IlsCrmYesNoType.No])
        self.parametersPanel.cmbC16.addItems([IlsCrmCategoryType.Cat1, IlsCrmCategoryType.Cat2, IlsCrmCategoryType.Cat1RA, IlsCrmCategoryType.Cat2AP])
        self.parametersPanel.cmbC17.addItems([IlsCrmMinimumType.OCA, IlsCrmMinimumType.OCH])
        self.parametersPanel.cmbC18.addItems([Captions.METRES, Captions.FEET])
        self.parametersPanel.cmbC19XA.addItems([IlsCrmYesNoType.Yes, IlsCrmYesNoType.No])
        self.parametersPanel.cmbC19XA.setCurrentIndex(1)
        self.parametersPanel.cmbC19XB.addItems([IlsCrmYesNoType.Yes, IlsCrmYesNoType.No])
        self.parametersPanel.cmbC19XB.setCurrentIndex(1)
        self.parametersPanel.cmbC19XC.addItems([IlsCrmYesNoType.Yes, IlsCrmYesNoType.No])
        self.parametersPanel.cmbC19XC.setCurrentIndex(1)
        self.parametersPanel.cmbC19XD.addItems([IlsCrmYesNoType.Yes, IlsCrmYesNoType.No])
        self.parametersPanel.cmbC19XD.setCurrentIndex(1)
        self.parametersPanel.cmbC19YA.addItems([IlsCrmYesNoType.Yes, IlsCrmYesNoType.No])
        self.parametersPanel.cmbC19YB.addItems([IlsCrmYesNoType.Yes, IlsCrmYesNoType.No])
        self.parametersPanel.cmbC19YC.addItems([IlsCrmYesNoType.Yes, IlsCrmYesNoType.No])
        self.parametersPanel.cmbC19YD.addItems([IlsCrmYesNoType.Yes, IlsCrmYesNoType.No])
        self.parametersPanel.cmbC22.addItems([IlsCrmRiskType.Highest, IlsCrmRiskType.HigherThan, IlsCrmRiskType.All])
        '''Event Handlers Connect'''
        self.parametersPanel.btnBrowser.clicked.connect(self.saveObstacleFile)    
        self.parametersPanel.cmbC13.currentIndexChanged.connect(self.method_28) 
        self.parametersPanel.cmbC14.currentIndexChanged.connect(self.method_28)
        self.parametersPanel.cmbC15.currentIndexChanged.connect(self.method_28)
        self.parametersPanel.cmbC17.currentIndexChanged.connect(self.method_28)
        self.parametersPanel.cmbC18.currentIndexChanged.connect(self.method_28)
        self.parametersPanel.cmbC19XA.currentIndexChanged.connect(self.method_28)
        self.parametersPanel.cmbC19XB.currentIndexChanged.connect(self.method_28)
        self.parametersPanel.cmbC19XC.currentIndexChanged.connect(self.method_28)
        self.parametersPanel.cmbC19XD.currentIndexChanged.connect(self.method_28)
        
        self.parametersPanel.btnCapture12.clicked.connect(self.measureDistance12)
        self.parametersPanel.btnCaptureC13b.clicked.connect(self.measureDistanceC13b)
#         ui.chbAutoRun.hide()
    def uiStateInit(self):
#         self.ui.btnConstruct.setText("Create")
#         self.ui.btnOutput = QPushButton(self.ui.frame_Btns)
# #         font = QtGui.QFont()
# #         font.setFamily(_fromUtf8("Arial"))
# #         font.setBold(False)
# #         font.setWeight(50)
# #         self.btnOpenData.setFont(font)
#         self.ui.btnOutput.setObjectName("btnOutput")
#         self.ui.btnOutput.setText("Output")
#         self.ui.verticalLayout_Btns.insertWidget(3, self.ui.btnOutput)
#         self.ui.btnOutput.setEnabled(False)
#         self.ui.btnOutput.clicked.connect(self.btnOutputClicked)
        
        return FlightPlanBaseDlg.uiStateInit(self)
    
    def saveObstacleFile(self):
        saveFileName = QFileDialog.getSaveFileName(self, "Save as", QCoreApplication.applicationDirPath(),"CRM Obstacle Files(*.obs)")
        if saveFileName == "":
            return
        else:
            self.parametersPanel.txtFile.setText(saveFileName)
            
    def method_27(self):
        try:        
            if self.parametersPanel.txtFile == "":
                raise UserWarning ,"Obstacle Save File Path is incorrect. "
            
            if (self.parametersPanel.txtC07.text() == "" or (float(self.parametersPanel.txtC07.text()) < 2.5 or float(self.parametersPanel.txtC07.text()) > 3.5)):
                raise UserWarning ,Validations.VALUE_CANNOT_BE_SMALLER_THAN_OR_GREATER_THAN%(2.5,3.5)
            Validations.valueValidate(self.parametersPanel.txtC08, "[08] value is error.")
            Validations.valueValidate(self.parametersPanel.txtC10, "[10] value is error.")
            Validations.valueValidate(self.parametersPanel.txtC12, "[12] value is error.")
            
            if self.parametersPanel.cmbC13.currentIndex() == 1:
                Validations.valueValidate(self.parametersPanel.txtC13a, "[13a] value is error.")
 
            if self.parametersPanel.cmbC14.currentIndex() == 1:
                Validations.valueValidate(self.parametersPanel.txtC14a, "[14a] value is error.")
                Validations.valueValidate(self.parametersPanel.txtC14b, "[14a] value is error.")
            
            if self.parametersPanel.cmbC15.currentIndex() == 1 and float(self.parametersPanel.txtC15a.text()) > 20:
                raise UserWarning , Validations.VALUE_CANNOT_BE_GREATER_THAN%20
       
            if not self.parametersPanel.pnlThr.IsValid():
                raise UserWarning, "Threshold Position value is incorrect."
            if not self.parametersPanel.pnlLoc.IsValid():
                raise UserWarning, "Localizer Position value is incorrect."
        except UserWarning as e:
            QMessageBox.warning(self, "Error", e.message)

    def method_28(self):
        self.parametersPanel.frame_C13a.setVisible(self.parametersPanel.cmbC13.currentIndex()== 1)
        self.parametersPanel.frame_C13b.setVisible(self.parametersPanel.cmbC13.currentIndex()== 1)
        self.parametersPanel.frame_C14a.setVisible(self.parametersPanel.cmbC14.currentIndex()== 1)
        self.parametersPanel.frame_C14b.setVisible(self.parametersPanel.cmbC14.currentIndex()== 1)
        self.parametersPanel.frame_C15a.setVisible(self.parametersPanel.cmbC15.currentIndex()== 1)
        oCA = Captions.OCA
        if (self.parametersPanel.cmbC17.currentIndex()== 1):
            oCA = Captions.OCH
            
        altitudeUnitsM = "m"
        if (self.parametersPanel.cmbC18.currentIndex()== 1):
            altitudeUnitsM = "ft"
        self.parametersPanel.txtC19ZA.setEnabled(self.parametersPanel.cmbC19XA.currentIndex()== 0)
        self.parametersPanel.label_25.setText(oCA + "(%s):"%altitudeUnitsM)
        self.parametersPanel.txtC19ZB.setEnabled(self.parametersPanel.cmbC19XB.currentIndex()== 0)
        self.parametersPanel.label_26.setText(oCA + "(%s):"%altitudeUnitsM)        
        self.parametersPanel.txtC19ZC.setEnabled(self.parametersPanel.cmbC19XC.currentIndex()== 0)
        self.parametersPanel.label_27.setText(oCA + "(%s):"%altitudeUnitsM)
        self.parametersPanel.txtC19ZD.setEnabled(self.parametersPanel.cmbC19XD.currentIndex()== 0)
        self.parametersPanel.label_28.setText(oCA + "(%s):"%altitudeUnitsM)
    def method_33(self, string_0):
        fileInfo = QFileInfo(string_0)
        path = fileInfo.path()
        fileName = fileInfo.fileName()
        dirPath = QDir(path)
        
        if dirPath.exists(path + "/CRMF01"):
            dirPath.remove(path + "/CRMF01")
        if dirPath.exists(path + "/CRMF02"):
            dirPath.remove(path + "/CRMF02")
        if dirPath.exists(path + "/CRMF03"):
            dirPath.remove(path + "/CRMF03")
        if dirPath.exists(path + "/CRMF04"):
            dirPath.remove(path + "/CRMF04")
        if dirPath.exists(path + "/CRMF05"):
            dirPath.remove(path + "/CRMF05")
        
        if dirPath.exists(path + "/CRMF06"):
            dirPath.remove(path + "/CRMF06")
        if dirPath.exists(path + "/CRMF07"):
            dirPath.remove(path + "/CRMF07")
        if dirPath.exists(path + "/CRMF08"):
            dirPath.remove(path + "/CRMF08")
        if dirPath.exists(path + "/CRMX16"):
            dirPath.remove(path + "/CRMX16")
        
        
        if not dirPath.exists(path + "/CRMEDT.EXE"):
            file0 = QFile("Resource/CRM/CRMEDT.EXE")
            result = file0.copy(path + "/CRMEDT.EXE")
        if not dirPath.exists(path + "/CRMRPT.EXE"):
            file0 = QFile("Resource/CRM/CRMRPT.EXE")
            result = file0.copy(path + "/CRMRPT.EXE")
        if not dirPath.exists(path + "/CRMRSK.EXE"):
            file0 = QFile("Resource/CRM/CRMRSK.EXE")
            result = file0.copy(path + "/CRMRSK.EXE")
        if not dirPath.exists(path + "/CRMSORT.EXE"):
            file0 = QFile("Resource/CRM/CRMSORT.EXE")
            result = file0.copy(path + "/CRMSORT.EXE")
        if not dirPath.exists(path + "/CRM.bat"):
            file0 = QFile("Resource/CRM/CRM.bat")
            result = file0.copy(path + "/CRM.bat")
        file0 = QFile(string_0)
        result = file0.copy(path + "/CRMF05")
#         file0 = QFile(str(path + "/CRM.bat"))
#         os.execl(str(path + "/CRM.bat"), [str(fileName[:len(fileName) - 4])])
        try:
            os.startfile(str(path + "/CRMEDT.EXE"))
        except WindowsError as e:
            QMessageBox.warning(self, "Warning", "Please check versions of Windows.\n'CRMEDT.EXE' can not start with 64-bit versions of Windows.")
            
#         
        file0 = QFile(path + "/CRMF06")
        result = file0.copy(path + "/" + fileName[:len(fileName) - 4] + ".prt")
        
        try:
            os.startfile(str(path + "/CRMSORT.EXE"))
        except WindowsError as e:
            QMessageBox.warning(self, "Warning", "Please check versions of Windows.\n'CRMSORT.EXE' can not start with 64-bit versions of Windows.")
        try:
            os.startfile(str(path + "/CRMRSK.EXE"))
        except WindowsError as e:
            QMessageBox.warning(self, "Warning", "Please check versions of Windows.\n'CRMRSK.EXE' can not start with 64-bit versions of Windows.")
        try:
            os.startfile(str(path + "/CRMRPT.EXE"))
        except WindowsError as e:
            QMessageBox.warning(self, "Warning", "Please check versions of Windows.\n'CRMRPT.EXE' can not start with 64-bit versions of Windows.")
             
            
#         
#         win32api.ShellExecute(0, None, str(path + "/CRMSORT.EXE"),None, None, 0)
#         win32api.ShellExecute(0, None, str(path + "/CRMRSK.EXE"),None, None, 0)
#         win32api.ShellExecute(0, None, str(path + "/CRMRPT.EXE"),None, None, 0)
#         
        file0 = QFile(path + "/CRMX16")
        result = file0.copy(path + "/" + fileName[:len(fileName) - 4] + ".rsk")
        
#         print fileInfo.path()
#         dir = QDir(self.currentDir + "/FlightPlanner/IIsCrm/CRM")
#         print dir.count()
#         result = file.copy("c:\\t.xml")
#         print result
#         pass
#         pathRoot = Path.GetPathRoot(Environment.SystemDirectory);
#         currentDirectory = root#.CurrentDirectory;
#         os.startfile(str(parh + "/CRM.bat"), str(string_0[:len(string_0) - 4]))
#         win32api.ShellExecute(0, None, str(parh + "/CRM.bat"),None, None, 0)
#         os.execl(str(path + "/CRM.bat"), str(string_0[:len(string_0) - 4]))
#         str = os.path.genericpath
#         m = 0
#         Path.GetPathRoot(currentDirectory);
#         string str = Path.Combine(pathRoot, "CRM");
#         string str1 = Path.ChangeExtension(string_0, ".rsk");
#         string str2 = Path.ChangeExtension(string_0, ".prt");
#         try
#         {
#             if (File.Exists(str1))
#             {
#                 File.Delete(str1);
#             }
#             if (File.Exists(str2))
#             {
#                 File.Delete(str2);
#             }
#             Environment.CurrentDirectory = str;
#             if (File.Exists(Path.Combine(str, "CRMF01")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF01"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMF02")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF02"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMF03")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF03"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMF05")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF05"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMF06")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF06"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMF07")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF07"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMF08")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF08"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMX16")))
#             {
#                 File.Delete(Path.Combine(str, "CRMX16"));
#             }
#             File.Copy(string_0, Path.Combine(str, "CRMF05"), true);
#             if (!Win32.smethod_1(Path.Combine(str, "crmedt.exe"), null))
#             {
#                 throw new Exception(string.Format(Messages.ERR_FAILED_TO_EXECUTE_X, Path.Combine(str, "crmedt.exe")));
#             }
#             File.Copy(Path.Combine(str, "CRMF06"), str2, true);
#             if (!Win32.smethod_1(Path.Combine(str, "crmsort.exe"), null))
#             {
#                 throw new Exception(string.Format(Messages.ERR_FAILED_TO_EXECUTE_X, Path.Combine(str, "crmsort.exe")));
#             }
#             if (!Win32.smethod_1(Path.Combine(str, "crmrsk.exe"), null))
#             {
#                 throw new Exception(string.Format(Messages.ERR_FAILED_TO_EXECUTE_X, Path.Combine(str, "crmrsk.exe")));
#             }
#             if (!Win32.smethod_1(Path.Combine(str, "crmrpt.exe"), null))
#             {
#                 throw new Exception(string.Format(Messages.ERR_FAILED_TO_EXECUTE_X, Path.Combine(str, "crmrpt.exe")));
#             }
#             File.Copy(Path.Combine(str, "CRMX16"), str1, true);
#             if (File.Exists(Path.Combine(str, "CRMF01")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF01"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMF02")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF02"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMF03")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF03"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMF05")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF05"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMF06")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF06"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMF07")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF07"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMF08")))
#             {
#                 File.Delete(Path.Combine(str, "CRMF08"));
#             }
#             if (File.Exists(Path.Combine(str, "CRMX16")))
#             {
#                 File.Delete(Path.Combine(str, "CRMX16"));
#             }
#             Environment.CurrentDirectory = currentDirectory;
#             if (File.Exists(str2) && File.Exists(str1) && ConfirmMessageBox.smethod_0(this, string.Format(Confirmations.OPEN_CREATED_FILES, str2, str1)) == ExtendedDialogResult.Yes)
#             {
#                 Win32.ShellExecute(Win32.GetDesktopWindow(), "open", "notepad.exe", str2, null, Win32.ShowCommand.SW_SHOWDEFAULT);
#                 Win32.ShellExecute(Win32.GetDesktopWindow(), "open", "notepad.exe", str1, null, Win32.ShowCommand.SW_SHOWDEFAULT);
#             }
#         }
#         catch (Exception exception1)
#         {
#             Exception exception = exception1;
#             ErrorMessageBox.smethod_0(this, string.Format(Messages.ERR_CRM_AUTO_EXECUTION, exception.Message, str));
    def createFile(self, point3d, point3d1):
        
        str13 = self.ilsCrmEvaluator.method_1("00 3")
        str14 = self.ilsCrmEvaluator.method_1("01 ")
        str15 = self.ilsCrmEvaluator.method_1("02 " + self.parametersPanel.txtC02.text())
        str16 = self.ilsCrmEvaluator.method_1("03 " + self.parametersPanel.txtC03.text())
        str17 = self.ilsCrmEvaluator.method_1("04 ")
        str18 = self.ilsCrmEvaluator.method_1("05  space")
        str19 = self.ilsCrmEvaluator.method_1("06 ")
        str20 = self.ilsCrmEvaluator.method_1("07 " + self.ilsCrmEvaluator.method_4(float(self.parametersPanel.txtC07.text()), 100))
        str21 = self.ilsCrmEvaluator.method_1("08 " + self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(float(self.parametersPanel.txtC08.text()), 10), 3) + "M")
        num = float(self.parametersPanel.txtC10.text())
        str22 = self.ilsCrmEvaluator.method_1("10 " + self.ilsCrmEvaluator.method_0(str(num), 3) + "M")
        value1 = float(self.parametersPanel.txtC12.text())
        str23 = self.ilsCrmEvaluator.method_1("12 " + self.ilsCrmEvaluator.method_0(str(value1), 5) + "M")
        str0 = ""
        if (self.parametersPanel.cmbC13.currentIndex() == 0):
            str0 = self.ilsCrmEvaluator.method_1("13 Y")
        elif (self.parametersPanel.cmbC13a.currentIndex() != 0):
            num1 = float(self.parametersPanel.txtC13b.text())
            str0 = self.ilsCrmEvaluator.method_1("13 N N " + self.ilsCrmEvaluator.method_0(str(num1), 5) + "M")
        else:
            value2 = float(self.parametersPanel.txtC13b.text())
            str0 = self.ilsCrmEvaluator.method_1("13 N Y " + self.ilsCrmEvaluator.method_0(str(value2), 5) + "M")
        str1 = ""
        if (self.parametersPanel.cmbC14.currentIndex() != 0):
            strArrays = "14 N " + self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(float(self.parametersPanel.txtC14a.text()), 10), 3) + "M ", self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(float(self.parametersPanel.txtC14b.text()), 10), 4) + "M" 
            str1 = self.ilsCrmEvaluator.method_1(strArrays)
        else:
            str1 = self.ilsCrmEvaluator.method_1("14 Y")
        str2 = self.ilsCrmEvaluator.method_1("15 N "+ self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(float(self.parametersPanel.txtC15a.text()), 10), 2)) if (self.parametersPanel.cmbC15.currentIndex() != 0) else self.ilsCrmEvaluator.method_1("15 Y")
        selectedIndex = self.parametersPanel.cmbC16.currentIndex() + 1
        str24 = self.ilsCrmEvaluator.method_1("16 " + str(selectedIndex))
        selectedIndex1 = self.parametersPanel.cmbC17.currentIndex() + 1
        str25 = self.ilsCrmEvaluator.method_1("17 " + str(selectedIndex1))
        str3 = self.ilsCrmEvaluator.method_1("18 F") if (self.parametersPanel.cmbC18.currentIndex() != 0) else self.ilsCrmEvaluator.method_1("18 M")
        str4 = "N      " if (self.parametersPanel.cmbC19XA.currentIndex() != 0) else "Y " + self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(float(self.parametersPanel.txtC19ZA.text()), 1), 5)
        str5 = "N      " if (self.parametersPanel.cmbC19XB.currentIndex() != 0) else "Y " + self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(float(self.parametersPanel.txtC19ZB.text()), 1), 5)
        str6 = "N      " if (self.parametersPanel.cmbC19XC.currentIndex() != 0) else "Y " + self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(float(self.parametersPanel.txtC19ZC.text()), 1), 5)
        str7 = "N      " if (self.parametersPanel.cmbC19XD.currentIndex() != 0) else "Y " + self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(float(self.parametersPanel.txtC19ZD.text()), 1), 5)
        str8 = "N" if (self.parametersPanel.cmbC19YA.currentIndex() != 0) else "Y"
        str9 = "N" if (self.parametersPanel.cmbC19YB.currentIndex() != 0) else "Y"
        str10 = "N" if (self.parametersPanel.cmbC19YC.currentIndex() != 0) else "Y"
        str11 = "N" if (self.parametersPanel.cmbC19YD.currentIndex() != 0) else "Y"
        strArrays = "19 " + str4 + " " + str8 + " " + str5 + " " + str9 + " " + str6 + " " + str10 + " " + str7 + " " + str11
        str26 = self.ilsCrmEvaluator.method_1(strArrays)
        num = MathHelper.calcDistance0(point3d, point3d1)
        str27 = self.ilsCrmEvaluator.method_1("09 " + self.ilsCrmEvaluator.method_0(str(int(round(num))), 5) + "M")
        str28 = self.ilsCrmEvaluator.method_1("11 " + self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(point3d.get_Z(), 1), 5) + "M")
        str29 = self.ilsCrmEvaluator.method_1("20 1")
        selectedIndex = self.parametersPanel.cmbC22.currentIndex( )+ 1
        str30 = self.ilsCrmEvaluator.method_1("22 " + str(selectedIndex))
        str31 = self.ilsCrmEvaluator.method_1("23 N")
        str32 = self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(point3d.get_X(), 1), 8)
        str33 = self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(point3d.get_Y(), 1), 8);
        str34 = self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(point3d.get_Z(), 1), 5);
        str35 = self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(point3d1.get_X(), 1), 8);
        str36 = self.ilsCrmEvaluator.method_0(self.ilsCrmEvaluator.method_4(point3d1.get_Y(), 1), 8);
        strArrays = "24 Y M M " + str32 + " " + str33 + " " + str34 + " " + str35 + " " + str36 
        str37 = self.ilsCrmEvaluator.method_1(strArrays)
        str38 = self.ilsCrmEvaluator.method_1("25 N")
        str39 = self.ilsCrmEvaluator.method_1("26 N")
        
        self.file1.write(str13)
        self.file1.write(str14)
        self.file1.write(str15)
        self.file1.write(str16)
        self.file1.write(str17)
        self.file1.write(str18)
        self.file1.write(str19)
        self.file1.write(str20)
        self.file1.write(str21)
        self.file1.write(str27)
        self.file1.write(str22)
        self.file1.write(str28)
        self.file1.write(str23)
        self.file1.write(str0)
        self.file1.write(str1)
        self.file1.write(str2)
        self.file1.write(str24)
        self.file1.write(str25)
        self.file1.write(str3)
        self.file1.write(str26)
        self.file1.write(str29)
# #         
        noObstacles = self.ilsCrmEvaluator.noObstacles
        noSpikes = self.ilsCrmEvaluator.noSpikes;
        str12 = self.ilsCrmEvaluator.method_1("21 " + self.ilsCrmEvaluator.method_0(str(noObstacles), 4))
        self.file1.write(str12)
        
#         self.file.write(self.ilsCrmEvaluator.method_1(" "))
        self.file1.write(str30)
        self.file1.write(str31)
        self.file1.write(str37)
        self.file1.write(str38)
        self.file1.write(str39)        
    def measureDistance12(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtC12, DistanceUnits.M)
        define._canvas.setMapTool(measureDistanceTool)    
    def measureDistanceC13b(self):
        measureDistanceTool = MeasureTool(define._canvas, self.parametersPanel.txtC13b, DistanceUnits.M)
        define._canvas.setMapTool(measureDistanceTool)
    def btnConstruct_Click(self):  
        if len(self.resultLayerList) > 0:
            QgisHelper.removeFromCanvas(define._canvas, self.resultLayerList)
            self.resultLayerList = []
        tempFileName = self.parametersPanel.txtFile.text()
#         self.method_33(tempFileName)
        self.point3dThr = self.parametersPanel.pnlThr.Point3d
        self.point3dLoc = self.parametersPanel.pnlLoc.Point3d
        str12 = ""
        noObstacles = 0
        noSpikes = 0
        fileInfo = QFileInfo(tempFileName)
#         file0 = QFile(tempFileName) 
# #         result = file0.remove()
        if fileInfo.exists():
            QFile.remove(tempFileName)
            
#         n= 0
#         if not fileInfo.exists():
        file0 = open(tempFileName, 'w')
        file0.close()
        self.file1 = open(tempFileName, 'r+')
         
        self.ilsCrmEvaluator = IlsCrmEvaluator(file, self.point3dThr, self.point3dLoc)
 
        self.toolSelectByPolygon = RubberBandPolygon(define._canvas)
        define._canvas.setMapTool(self.toolSelectByPolygon)
        self.connect(self.toolSelectByPolygon, SIGNAL("outputResult"), self.outputResultMethod)   
#         self.ui.btnOutput.setEnabled(True)
        
    def outputResultMethod(self):
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
#         tempFileName = ""
        tempFileName = self.parametersPanel.txtFile.text()
        if self.file1.closed:
#             tempFileName = self.parametersPanel.txtFile.text()
            fileInfo = QFileInfo(tempFileName)
            if fileInfo.exists():
                QFile.remove(tempFileName)
                
    #         n= 0
    #         if not fileInfo.exists():
            file0 = open(tempFileName, 'w')
            file0.close()
            self.file1 = open(tempFileName, 'r+')
        if self.toolSelectByPolygon == None:
            return
#         tempFileName = self.parametersPanel.txtFile.text()
#         self.file = open(tempFileName, 'r+')
        mapUnits = define._canvas.mapUnits()
        constructionLayer = None
        if define._mapCrs == None:
            if mapUnits == QGis.Meters:
                constructionLayer = QgsVectorLayer("Polygon?crs=EPSG:32633", "CRM", "memory")
            else:
                constructionLayer = QgsVectorLayer("Polygon?crs=EPSG:4326", "CRM", "memory")
        else:
            constructionLayer = QgsVectorLayer("Polygon?crs=%s"%define._mapCrs.authid (), "CRM", "memory")
        shpPath = ""
        if define.obstaclePath != None:
            shpPath = define.obstaclePath
        elif define.xmlPath != None:
            shpPath = define.xmlPath
        else:
            shpPath = define.appPath
        er = QgsVectorFileWriter.writeAsVectorFormat(constructionLayer, shpPath + "/" + "CRM" + ".shp", "utf-8", constructionLayer.crs())
        constructionLayer = QgsVectorLayer(shpPath + "/" + "CRM" + ".shp", "CRM", "ogr")

        constructionLayer.startEditing()
        feature = QgsFeature()
        feature.setGeometry(self.toolSelectByPolygon.polygonGeom)
        pr = constructionLayer.dataProvider()
        pr.addFeatures([feature])
        # constructionLayer.addFeature(feature)
        constructionLayer.commitChanges()
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], SurfaceTypes.CRM)
        QgisHelper.zoomToLayers([constructionLayer])
        self.resultLayerList = [constructionLayer]
        surfaceGeom =  self.toolSelectByPolygon.polygonGeom
        surface = surfaceGeom.asPolygon () 
        self.obstaclesModel = CrmObstacles([surface],self.file1, self.ilsCrmEvaluator)
        try:
            if self.obstaclesModel == None:
                self.initObstaclesModel()
                if self.obstaclesModel == None:
                    return
            surfaceLayers = QgisHelper.getSurfaceLayers(self.surfaceType)
            self.initObstaclesModel()
            self.obstaclesModel.loadObstacles(surfaceLayers)
            
#             noObstacles = self.ilsCrmEvaluator.noObstacles
#             noSpikes = self.ilsCrmEvaluator.noSpikes;
#             str12 = self.ilsCrmEvaluator.method_1("21 " + self.ilsCrmEvaluator.method_0(str(noObstacles), 4))
            
            progressMessageBar = define._messagBar.createMessage("Writing obstacle file...")
            self.progress = QProgressBar()
            self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)        
            progressMessageBar.layout().addWidget(self.progress)
            define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
            self.progress.setMaximum(100000)
            
            self.createFile(self.point3dThr, self.point3dLoc)
            
            for i in range(50000):
                self.progress.setValue(i)
            
            self.file1.writelines(self.obstaclesModel.resultStrList)
            
            for i in range(50001, 100000):
                self.progress.setValue(i)
            self.progress.setValue(100000)
            define._messagBar.hide()  
            
            self.file1.close()
            
            messageStr = "Obstacle file with " + str(self.ilsCrmEvaluator.noObstacles) + " obstacle(s) successfully created " + str(self.ilsCrmEvaluator.noSpikes) + " obstacle wall(s) represented SPIKES"
            QMessageBox.information(self, "Result", messageStr)
            if self.parametersPanel.chbAutoRun.isChecked():
                self.method_33(tempFileName)
        except UserWarning as e:
            QMessageBox.warning(self, "Information", e.message)
       
        

class IlsCrmEvaluator:
    def __init__(self, streamWriter_0, point3d_0, point3d_1):
        self.writer = streamWriter_0
        self.cAng = MathHelper.smethod_26(point3d_1, point3d_0)
        self.cp9ang = self.cAng + 1.5707963267949
        self.cm9ang = self.cAng - 1.5707963267949
        self.c18ang = self.cAng + 3.14159265358979
        self.c9thr = MathHelper.distanceBearingPoint(point3d_0, MathHelper.getBearing(point3d_0, point3d_1), 900)
        self.ide = "28 "
        self.csp2 = "  "
        self.noObstacles = 0
        self.noSpikes = 0
        
    def imethod_0(self, obstacle_0):
        position = obstacle_0.Position
        point3d = obstacle_0.Position
        point3d1 = position.smethod_167(point3d.get_Z() + obstacle_0.Trees)
        num = MathHelper.smethod_26(self.c9thr, point3d1)
        num1 = num - self.cAng
        if (num < self.cAng):
            num1 = 6.28318530717959 - (self.cAng - num)
        
        num2 = self.c18ang
        if (num1 > 1.5707963267949 and num1 < 4.71238898038469):
        
            num2 = self.cAng
        
        tolerance = obstacle_0.Tolerance
        point3d2 = MathHelper.distanceBearingPoint(point3d1, 7.85398163397448 - num2, tolerance)
        point3d3 = MathHelper.distanceBearingPoint(point3d2, 7.85398163397448 - self.cp9ang, tolerance)
        point3d4 = MathHelper.distanceBearingPoint(point3d2, 7.85398163397448 - self.cm9ang, tolerance)
        x = point3d3.get_X()
        y = point3d3.get_Y()
        z = point3d3.get_Z()
        x1 = point3d4.get_X()
        y1 = point3d4.get_Y()
        z1 = point3d4.get_Z()
        num3 = round(x, 0)
        num4 = round(y, 0)
        num5 = round(x1, 0)
        num6 = round(y1, 0)
        num7 = Unit.smethod_1(self.cp9ang)
        num8 = 7
        num9 = 0
        num10 = 0.5
        point3d5 = Point3D(x, y, 0)
        point3d6 = Point3D(x1, y1, 0)
        num11 = 0
        flag = False
        while (num8 > 5.1):
            point3d7 = Point3D(num5, num6, 0)
            point3d8 = Point3D(num3, num4, 0)
            num12 = Unit.smethod_1(MathHelper.smethod_26(point3d7, point3d8))
            num13 = Unit.smethod_1(MathHelper.smethod_26(point3d8, point3d7))
            num14 = math.fabs(num12 - num7)
            num15 = math.fabs(num13 - num7)
            num8 = min([num14, num15])
            if (num8 > 90):
                num8 = math.fabs(num8 - 180)
            
            if (num8 <= 5.1):
                continue
            
            if (num9 >= 1):
                point3d9 = MathHelper.distanceBearingPoint(point3d6, 7.85398163397448 - num2, num10)
                num5 = round(point3d9.get_X(), 0)
                num6 = round(point3d9.get_Y(), 0)
                num9 = 0
            
            else:
                point3d10 = MathHelper.distanceBearingPoint(point3d5, 7.85398163397448 - num2, num10)
                num3 = round(point3d10.get_X(), 0)
                num4 = round(point3d10.get_Y(), 0)
                num9 = 1
            
            if (num9 == 0):
                num10 = num10 + 0.5
            
            if (num11 > 20):
                flag = True
                num3 = round(x, 0)
                num4 = round(y, 0)
                num5 = round(x1, 0)
                num6 = round(y1, 0)
                num8 = 5
                self.noSpikes += 1
#                 IlsCrm.IlsCrmEvaluator ilsCrmEvaluator = self
#                 ilsCrmEvaluator.noSpikes = ilsCrmEvaluator.noSpikes + 1
            
            num11 = 1 + num11
        
        x = num3
        y = num4
        x1 = num5
        y1 = num6
        str2 = self.method_2(obstacle_0.Name, 13) + self.csp2
        str3 = self.method_3(x, 8)
        str4 = self.method_3(y, 8)
        str5 = self.method_3(z, 5)
        str6 = self.method_3(x1, 8)
        str7 = self.method_3(y1, 8)
        str8 = self.method_3(z1, 5)
        if not flag:
            str = self.ide + "A         " + str2 + str3 + "    " + str4 + "        " + str5 + " 1" 
#             str = string.Concat(strArrays)
            str1 = self.ide + "B         "+ str2+ str6+ "    "+ str7+ "        "+ str8+ " 2" 
#             str1 = string.Concat(strArrays1)
        
        else:
            str = self.ide+ "A         "+ str2+ str3+ "    "+ str4+ "        "+ str5+ " 0" 
#             str = string.Concat(strArrays2)
            str1 = self.ide+ "A         "+ str2+ str6+ "    "+ str7+ "        "+ str8+ " 0" 
#             str1 = string.Concat(strArrays3)
            self.noObstacles += 1
#             IlsCrm.IlsCrmEvaluator ilsCrmEvaluator1 = self
#             ilsCrmEvaluator1.noObstacles = ilsCrmEvaluator1.noObstacles + 1
        
        self.writer.write(self.method_1(str))
        self.writer.write(self.method_1(str1))
        self.noObstacles += 1
#         IlsCrm.IlsCrmEvaluator ilsCrmEvaluator2 = self
#         ilsCrmEvaluator2.noObstacles = ilsCrmEvaluator2.noObstacles + 1
    
    def method_0(self, string_0, int_0):
        length = len(string_0)
#         StringBuilder stringBuilder = new StringBuilder(string_0)
        if (length < int_0):
            int0 = int_0 - length
            for i in range(int0):
                string_0 = " " + string_0             
        return string_0
    
    def method_1(self, string_0):
        length = 80 - len(string_0)
#         StringBuilder stringBuilder = new StringBuilder(string_0)
        for i in range(length):
            string_0 = string_0 + " "
        return string_0 + "\n"
    
    def method_2(self, string_0, int_0):
        length = len(string_0)
        if (length >= int_0):
            return string_0[0:int_0]
        
        int0 = int_0 - length
#         StringBuilder stringBuilder = new StringBuilder(string_0)
        for i in range(int0):
            string_0 = string_0 + " "         
        return string_0
    
    def method_3(self, double_0, int_0):
#         StringBuilder stringBuilder = new StringBuilder(double_0.ToString("0"))
        string_0 = str(int(round(double_0)))
        length = len(string_0)
        if (length < int_0):
            int0 = int_0 - length
            for i in range(length):
                string_0 = " " + string_0 
        
        return string_0
    
    def method_4(self, double_0, double_1):
        return str(int(round(double_0 * double_1)))
    
class CrmObstacles(ObstacleTable):
    def __init__(self, surfacesList, fileWriter , ilsCrmEvaluator):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, surfacesList)
        
        self.surfaceType = SurfaceTypes.TaaCalculation
        self.title = None
        self.radius = None
        self.waypoint = None
        self.obstaclesChecked = None
        self.surfacesList = surfacesList
#         if fileWriter == None:
        self.fileWriter = fileWriter
        self.ilsCrmEvaluator = ilsCrmEvaluator
        self.resultStrList = []
    def checkObstacle(self, obstacle_0):
        position = obstacle_0.Position
        point3d = obstacle_0.Position
        point3d1 = position.smethod_167(point3d.get_Z() + obstacle_0.Trees)
        num = MathHelper.smethod_26(self.ilsCrmEvaluator.c9thr, point3d1)
        num1 = num - self.ilsCrmEvaluator.cAng
        if (num < self.ilsCrmEvaluator.cAng):
            num1 = 6.28318530717959 - (self.ilsCrmEvaluator.cAng - num)
        
        num2 = self.ilsCrmEvaluator.c18ang
        if (num1 > 1.5707963267949 and num1 < 4.71238898038469):
        
            num2 = self.ilsCrmEvaluator.cAng
        
        tolerance = obstacle_0.Tolerance
        point3d2 = MathHelper.distanceBearingPoint(point3d1, 7.85398163397448 - num2, tolerance)
        point3d3 = MathHelper.distanceBearingPoint(point3d2, 7.85398163397448 - self.ilsCrmEvaluator.cp9ang, tolerance)
        point3d4 = MathHelper.distanceBearingPoint(point3d2, 7.85398163397448 - self.ilsCrmEvaluator.cm9ang, tolerance)
        x = point3d3.get_X()
        y = point3d3.get_Y()
        z = point3d3.get_Z()
        x1 = point3d4.get_X()
        y1 = point3d4.get_Y()
        z1 = point3d4.get_Z()
        num3 = round(x, 0)
        num4 = round(y, 0)
        num5 = round(x1, 0)
        num6 = round(y1, 0)
        num7 = Unit.smethod_1(self.ilsCrmEvaluator.cp9ang)
        num8 = 7
        num9 = 0
        num10 = 0.5
        point3d5 = Point3D(x, y, 0)
        point3d6 = Point3D(x1, y1, 0)
        num11 = 0
        flag = False
        while (num8 > 5.1):
            point3d7 = Point3D(num5, num6, 0)
            point3d8 = Point3D(num3, num4, 0)
            num12 = Unit.smethod_1(MathHelper.smethod_26(point3d7, point3d8))
            num13 = Unit.smethod_1(MathHelper.smethod_26(point3d8, point3d7))
            num14 = math.fabs(num12 - num7)
            num15 = math.fabs(num13 - num7)
            num8 = min([num14, num15])
            if (num8 > 90):
                num8 = math.fabs(num8 - 180)
            
            if (num8 <= 5.1):
                continue
            
            if (num9 >= 1):
                point3d9 = MathHelper.distanceBearingPoint(point3d6, 7.85398163397448 - num2, num10)
                num5 = round(point3d9.get_X(), 0)
                num6 = round(point3d9.get_Y(), 0)
                num9 = 0
            
            else:
                point3d10 = MathHelper.distanceBearingPoint(point3d5, 7.85398163397448 - num2, num10)
                num3 = round(point3d10.get_X(), 0)
                num4 = round(point3d10.get_Y(), 0)
                num9 = 1
            
            if (num9 == 0):
                num10 = num10 + 0.5
            
            if (num11 > 20):
                flag = True
                num3 = round(x, 0)
                num4 = round(y, 0)
                num5 = round(x1, 0)
                num6 = round(y1, 0)
                num8 = 5
                self.ilsCrmEvaluator.noSpikes += 1
#                 IlsCrm.IlsCrmEvaluator ilsCrmEvaluator = self
#                 ilsCrmEvaluator.noSpikes = ilsCrmEvaluator.noSpikes + 1
            
            num11 = 1 + num11
        
        x = num3
        y = num4
        x1 = num5
        y1 = num6
        str2 = self.ilsCrmEvaluator.method_2(obstacle_0.name, 13) + self.ilsCrmEvaluator.csp2
        str3 = self.ilsCrmEvaluator.method_3(x, 8)
        str4 = self.ilsCrmEvaluator.method_3(y, 8)
        str5 = self.ilsCrmEvaluator.method_3(z, 5)
        str6 = self.ilsCrmEvaluator.method_3(x1, 8)
        str7 = self.ilsCrmEvaluator.method_3(y1, 8)
        str8 = self.ilsCrmEvaluator.method_3(z1, 5)
        str0 = ""
        str1 = ""
        if not flag:
            str0 = self.ilsCrmEvaluator.ide + "A         " + str2 + str3 + "    " + str4 + "        " + str5 + " 1" 
#             str = string.Concat(strArrays)
            str1 = self.ilsCrmEvaluator.ide + "B         "+ str2+ str6+ "    "+ str7+ "        "+ str8+ " 2" 
#             str1 = string.Concat(strArrays1)
        
        else:
            str0 = self.ilsCrmEvaluator.ide+ "A         "+ str2+ str3+ "    "+ str4+ "        "+ str5+ " 0" 
#             str = string.Concat(strArrays2)
            str1 = self.ilsCrmEvaluator.ide+ "A         "+ str2+ str6+ "    "+ str7+ "        "+ str8+ " 0" 
#             str1 = string.Concat(strArrays3)
            self.ilsCrmEvaluator.noObstacles += 1
        self.resultStrList.append(self.ilsCrmEvaluator.method_1(str0))
        self.resultStrList.append(self.ilsCrmEvaluator.method_1(str1))
#         self.fileWriter.write(self.ilsCrmEvaluator.method_1(str0))
#         self.fileWriter.write(self.ilsCrmEvaluator.method_1(str1))
        self.ilsCrmEvaluator.noObstacles += 1
        pass
class RubberBandPolygon(QgsMapTool):
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.mCanvas = canvas
        self.mRubberBand = None
        self.mRubberBand0 = QgsRubberBand( self.mCanvas, QGis.Polygon )
        self.mCursor = Qt.ArrowCursor
        self.mFillColor = QColor( 254, 178, 76, 63 )
        self.mBorderColour = QColor( 254, 58, 29, 100 )
        self.mRubberBand0.setBorderColor( self.mBorderColour )
        self.polygonGeom = None
#         self.constructionLayer = constructionLayer
    def canvasPressEvent( self, e ):
        if ( self.mRubberBand == None ):
#             define._canvas.clearCache ()
            self.mRubberBand = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRubberBand0 = QgsRubberBand( self.mCanvas, QGis.Polygon )
            self.mRubberBand.setFillColor( self.mFillColor )
            self.mRubberBand.setBorderColor( self.mBorderColour )
            self.mRubberBand0.setFillColor( self.mFillColor )
            self.mRubberBand0.setBorderColor( self.mBorderColour )
        if ( e.button() == Qt.LeftButton ):
            self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )
        else:
            if ( self.mRubberBand.numberOfVertices() > 2 ):
                self.polygonGeom = self.mRubberBand.asGeometry()
            else:
                return
#                 QgsMapToolSelectUtils.setSelectFeatures( self.mCanvas, polygonGeom, e )
            self.mRubberBand.reset( QGis.Polygon )
            self.mRubberBand0.addGeometry(self.polygonGeom, None)
            self.mRubberBand0.show()
            self.mRubberBand = None
            self.emit(SIGNAL("outputResult"), self.polygonGeom)
    
    def canvasMoveEvent( self, e ):
        if ( self.mRubberBand == None ):
            return
        if ( self.mRubberBand.numberOfVertices() > 0 ):
            self.mRubberBand.removeLastPoint( 0 )
            self.mRubberBand.addPoint( self.toMapCoordinates( e.pos() ) )