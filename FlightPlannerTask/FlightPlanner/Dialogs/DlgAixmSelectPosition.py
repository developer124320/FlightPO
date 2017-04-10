# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from qgis.gui import QgsMapToolEmitPoint, QgsMapTool, QgsMapCanvasSnapper, QgsRubberBand
from qgis.core import QGis, QgsFeatureRequest, QgsRaster,QgsPoint
from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QMessageBox, QDialogButtonBox, QPushButton, QListView
from PyQt4.QtCore import SIGNAL, QObject, Qt
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.QgisHelper import Geo, QgisHelper
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.ListBox import ListBox
from FlightPlanner.types import Point3D, ProcEntityListType, SurfaceTypes, CodeTypeApchAixm, CodeRefOchAixm
from FlightPlanner.Dialogs.DlgAixmNewDPN import DlgAixmNewDPN
from FlightPlanner.Dialogs.DlgAixmNewPCP import DlgAixmNewPCP
from Type.switch import switch
from Type.Degrees import Degrees, DegreesType
from Type.String import String

from Type.DataBaseProcedureLegs import DataBaseProcedureLegs, DataBaseProcedureLegsEx
from Type.DataBase import DataBaseIapOcaOchs, DataBaseIapOcaOch
import math, define



class DlgAixmSelectPosition(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136);
        self.setWindowTitle("New DPN DB Entry")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));

        self.groupBox = GroupBox(self)
        self.groupBox.Caption = "Existing DB Entries"
        verticalLayoutDlg.addWidget(self.groupBox)

        self.lstItems = ListBox(self.groupBox)
        self.groupBox.Add = self.lstItems

        frame = Frame(self, "HL")
        verticalLayoutDlg.addWidget(frame)

        self.btnNewDPN = QPushButton(frame)
        self.btnNewDPN.setObjectName("btnNewDPN")
        self.btnNewDPN.setText("New DPN...")
        frame.Add = self.btnNewDPN

        self.btnNewPCP = QPushButton(frame)
        self.btnNewPCP.setObjectName("btnNewPCP")
        self.btnNewPCP.setText("New PCP...")
        frame.Add = self.btnNewPCP

        self.btnBoxOkCancel = QDialogButtonBox(frame)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        self.btnNewDPN.clicked.connect(self.btnNewDPN_Click)
        self.btnNewPCP.clicked.connect(self.btnNewPCP_Click)

        frame.Add = self.btnBoxOkCancel

        self.newTypeSelected = None
    def acceptDlg(self):
        self.accept()
    def btnNewDPN_Click(self):
        self.newTypeSelected = NewDbEntryType.DPN;
        self.reject()
    def btnNewPCP_Click(self):
        self.newTypeSelected = NewDbEntryType.PCP;
        self.reject()
    @staticmethod
    def resultPointValueListMethod(resultValueList, dataBaseProcedureData_0, point3d_0, procEntityListType_0, parent):
        if len(resultValueList) > 0:
            lat = None
            lon = None
            if define._units == QGis.Meters:
                point3d = QgisHelper.CrsTransformPoint(float(resultValueList[1]), float(resultValueList[2]), define._xyCrs, define._latLonCrs)

                lat = Degrees(point3d.get_Y(), None, None, DegreesType.Latitude)
                lon = Degrees(point3d.get_X(), None, None, DegreesType.Longitude)
            else:
                lat = Degrees(float(resultValueList[2]), None, None, DegreesType.Latitude)
                lon = Degrees(float(resultValueList[1]), None, None, DegreesType.Longitude)
            str0 = lon.method_1("dddmmss.ssssH")
            textString = lat.method_1("ddmmss.ssssH")
            procEntityBases = DlgAixmSelectPosition.smethod_1(dataBaseProcedureData_0, procEntityListType_0, point3d_0, textString, str0);
            dlgAixmSelectPosition = DlgAixmSelectPosition()
            naN = None;
            degree = None;
            result, naN, degree = Geo.smethod_2(point3d_0.get_X(), point3d_0.get_Y())
            if (result):
                dataBaseProcedureData_0.method_60(procEntityBases, procEntityListType_0, naN.ToString(), degree.ToString());
            dlgAixmSelectPosition.lstItems.Sorted = True;
            for procEntityBase in procEntityBases:
                dlgAixmSelectPosition.lstItems.Add(procEntityBase);
            if (procEntityListType_0 != ProcEntityListType.CentersEx and procEntityListType_0 != ProcEntityListType.FixesEx):
                dlgAixmSelectPosition.btnNewPCP.setEnabled(False);
                dlgAixmSelectPosition.btnNewPCP.setVisible(False);
            resultDlg = dlgAixmSelectPosition.exec_()
            procEntityBase_0 = None
            if (resultDlg != 1):
                if dlgAixmSelectPosition.newTypeSelected == NewDbEntryType.DPN:
                    flag, procEntityBase_0 = DlgAixmNewDPN.smethod_0(dataBaseProcedureData_0, naN, degree);
                elif dlgAixmSelectPosition.newTypeSelected == NewDbEntryType.PCP:
                    flag, procEntityBase_0 = DlgAixmNewPCP.smethod_0(dataBaseProcedureData_0, naN, degree);
                else:
                    flag = False;
            else:
                procEntityBase_0 = dlgAixmSelectPosition.lstItems.SelectedItem;
                flag = True;
            QObject.emit(parent, SIGNAL("DlgAixmSelectPosition_Smethod_0_Event"), flag, procEntityBase_0)
            return ;

    @staticmethod   #### complete
    def smethod_0(dataBaseProcedureData_0, point3d_0, procEntityListType_0):
        flag = False;
        procEntityBase_0 = None;
        CaptureCoordTool = CaptureCoordinateToolUpdate(define._canvas, dataBaseProcedureData_0, point3d_0, procEntityListType_0)
        define._canvas.setMapTool(CaptureCoordTool)
        QObject.connect(CaptureCoordTool, SIGNAL("resultPointValueList"), DlgAixmSelectPosition.resultPointValueListMethod)
        return CaptureCoordTool
    @staticmethod
    def smethod_1(dataBaseProcedureData_0, procEntityListType_0, point3d_0, textString, strS):
        procEntityBases = [];
        for case in switch(procEntityListType_0):
            if case(ProcEntityListType.Holding) or case(ProcEntityListType.Fixes) or case(ProcEntityListType.FixesEx) or case(ProcEntityListType.Centers)or case(ProcEntityListType.CentersEx):
                if (not String.IsNullOrEmpty(textString) and not String.IsNullOrEmpty(strS)):
                    dataBaseProcedureData_0.method_60(procEntityBases, procEntityListType_0, textString, strS);
                return procEntityBases;
            else:
                return None;
        return None

class NewDbEntryType:
    Nothing  = "None"
    DPN = "DPN"
    PCP = "PCP"

class CaptureCoordinateToolUpdate(QgsMapTool):
    def __init__(self, canvas, dataBaseProcedureData0, point3d0, procEntityListType0):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.mSnapper = QgsMapCanvasSnapper(canvas)
        self.rubberBand = QgsRubberBand(canvas, QGis.Point)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(10)
        self.rubberBandClick = QgsRubberBand(canvas, QGis.Point)
        self.rubberBandClick.setColor(Qt.green)
        self.rubberBandClick.setWidth(3)
        self.obstaclesLayerList = QgisHelper.getSurfaceLayers(SurfaceTypes.Obstacles)
        self.demLayerList = QgisHelper.getSurfaceLayers(SurfaceTypes.DEM)
        self.reset()

        self.dataBaseProcedureData_0 = dataBaseProcedureData0
        self.point3d_0 = point3d0
        self.procEntityListType_0 = procEntityListType0
    def reset(self):
        self.Point = None
    def canvasReleaseEvent(self, e):
        pointBackground = e.pos()
        self.Point, self.pointID, self.layer= self.snapPoint(e.pos())
        self.selectedLayerFromSnapPoint = None
        resultValueList = []
        self.rubberBandClick.reset(QGis.Point)

        self.rubberBandClick.addPoint(self.Point)
        self.rubberBandClick.show()
        if self.obstaclesLayerList != None:
            for obstacleLayer in self.obstaclesLayerList:
                if self.layer == None:
                    break
                if obstacleLayer.name() == self.layer.name():
                    self.selectedLayerFromSnapPoint = self.layer
                    break
#         itemList = []
        if self.selectedLayerFromSnapPoint != None:
            dataProvider = self.selectedLayerFromSnapPoint.dataProvider()
            featureIter = dataProvider.getFeatures( QgsFeatureRequest(self.pointID))
            feature = None
            for feature0 in featureIter:
                feature = feature0

            idx = self.selectedLayerFromSnapPoint.fieldNameIndex('Name')
            idValue = feature.attributes()[idx]
            resultValueList.append(idValue.toString())

            resultValueList.append(str(self.Point.x()))
            resultValueList.append(str(self.Point.y()))

            idx = self.selectedLayerFromSnapPoint.fieldNameIndex('Altitude')
            altitudeValue = feature.attributes()[idx]

            resultValueList.append(altitudeValue.toString())
        else:
            if self.Point != None:
                identifyResult = None
                idValue = "Background"
                if self.demLayerList != None:

                    for demLayer in self.demLayerList:
                        identifyResults = demLayer.dataProvider().identify(self.Point, QgsRaster.IdentifyFormatValue)
                        identifyResult = identifyResults.results()
                if identifyResult != None and identifyResult[1].toString() != "":
                    idValue = "DEM"

                resultValueList.append(idValue)
                resultValueList.append(str(self.Point.x()))
                resultValueList.append(str(self.Point.y()))
                if identifyResult != None:
                    resultValueList.append(identifyResult[1].toString())
                else:
                    resultValueList.append("0")
        self.point3d_0 = Point3D(self.Point.x(), self.Point.y())
        self.emit(SIGNAL("resultPointValueList"), resultValueList, self.dataBaseProcedureData_0, self.point3d_0, self.procEntityListType_0, self)
    def canvasMoveEvent(self, e):
        if define._snapping == False:
            return
        self.rubberBand.reset(QGis.Point)
#         snapPoint = QgisHelper.snapPoint(e.pos(), self.mSnapper, define._canvas, True)
        snapPoint, snapPointID, layer = self.snapPoint(e.pos(), True)
        if snapPoint == None:
            return
        self.rubberBand.addPoint(snapPoint)
        self.rubberBand.show()
#         print snapPointID
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

    def deactivate(self):
        self.rubberBand.reset(QGis.Point)
        QgsMapTool.deactivate(self)
        self.emit(SIGNAL("deactivated()"))