'''
Created on 18 May 2014

@author: Administrator
'''

from PyQt4.QtGui import QDialog, QColor, QMessageBox, QMenu, QLineEdit, QComboBox, QStandardItemModel, QStandardItem, QInputDialog
from PyQt4.QtCore import QCoreApplication, SIGNAL

from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Obstacle.ObstacleAreaJig import ObstacleAreaJigCreateArea, ObstacleAreaJigSelectArea
from FlightPlanner.Obstacle.ui_DlgComplexAreas import Ui_DlgComplexAreas
from FlightPlanner.types import ProtectionAreaType
from FlightPlanner.helpers import Unit
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.Obstacle.ObstacleArea import ComplexObstacleArea, PrimaryObstacleArea, SecondaryObstacleArea, SecondaryAreaStraight
from qgis.gui import QgsMapTool, QgsRubberBand, QgsMapCanvasSnapper
from qgis.core import QGis, QgsRectangle, QgsGeometry, QgsCsException, QgsPoint,\
        QgsFeatureRequest, QgsCoordinateTransform, QgsFeature, QgsVectorLayer, QgsLayerTreeGroup
import  define

class DlgComplexAreas(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.ui = Ui_DlgComplexAreas()
        self.ui.setupUi(self)

        self.stdItemModel = QStandardItemModel()
        self.ui.lstAreas.setModel(self.stdItemModel)

              
        ''' buttons clicked connect '''
        self.ui.btnAddPrimaryArea.clicked.connect(self.btnAddPrimaryArea_Click)
        self.ui.btnAddSecondaryArea.clicked.connect(self.btnAddSecondaryArea_Click)
        self.ui.btnRemove.clicked.connect(self.btnRemove_Click)
        self.ui.btnCaptureTrack.clicked.connect(self.btnCaptureTrack_Click)
        self.ui.buttonBoxOkCancel.accepted.connect(self.acceptEvent)
        self.ui.buttonBoxOkCancel.rejected.connect(self.rejectedEvent)
        self.ui.txtTrack.textChanged.connect(self.txtTrack_TextChanged)
        self.ui.lstAreas.clicked.connect(self.lstAreas_Click)

        self.ui.btnCaptureTrack.clicked.connect(self.captureTrack)

        self.complexObstacleArea = ComplexObstacleArea()
        self.itemCount = 0
        self.selectedModelIndex = None
        self.resultPolylineAreaListForDrawing = []
        self.method_9()


        self.constructionLayer = AcadHelper.createVectorLayer("TempComplexObstacleAreaLayer");
        QgisHelper.appendToCanvas(define._canvas, [self.constructionLayer], "Temp")
    def txtTrack_TextChanged(self):
        self.complexObstacleArea[self.selectedModelIndex.row()].nominalTrack = Unit.smethod_0(float(self.ui.txtTrack.text()));
    def btnAddPrimaryArea_Click(self):
        if QMessageBox.question(self, "Question", "Please click \"Yes\" if you want to create new area.\nPlease click \"No\" if you want to select any area.", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            # if self.comboBox.currentIndex() == ProtectionAreaType.Primary:
            obstacleAreaJig= ObstacleAreaJigCreateArea(define._canvas, ProtectionAreaType.Primary)
            define._canvas.setMapTool(obstacleAreaJig)
            self.connect(obstacleAreaJig, SIGNAL("outputResult"), self.AreaResult)
            # elif self.comboBox.currentIndex() == ProtectionAreaType.Secondary:
        else:
            obstacleAreaJig= ObstacleAreaJigSelectArea(define._canvas, ProtectionAreaType.Primary)
            define._canvas.setMapTool(obstacleAreaJig)
            self.connect(obstacleAreaJig, SIGNAL("outputResult"), self.AreaResult)
    def btnAddSecondaryArea_Click(self):
        if QMessageBox.question(self, "Question", "Please click \"Yes\" if you want to create new area.\nPlease click \"No\" if you want to select any area.", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            # if self.comboBox.currentIndex() == ProtectionAreaType.Primary:
            obstacleAreaJig= ObstacleAreaJigCreateArea(define._canvas, ProtectionAreaType.Secondary)
            define._canvas.setMapTool(obstacleAreaJig)
            self.connect(obstacleAreaJig, SIGNAL("outputResult"), self.AreaResult)
            # elif self.comboBox.currentIndex() == ProtectionAreaType.Secondary:
        else:
            obstacleAreaJig= ObstacleAreaJigSelectArea(define._canvas, ProtectionAreaType.Secondary)
            define._canvas.setMapTool(obstacleAreaJig)
            self.connect(obstacleAreaJig, SIGNAL("outputResult"), self.AreaResult)
    def AreaResult(self, area, rubberBand):
        if area != None:
            rubberBand.setFillColor( QColor(46, 64, 142, 100) )
            rubberBand.setBorderColor( QColor(0, 10, 238) )
            define._canvas.refresh()

            QgisHelper.ClearRubberBandInCanvas(define._canvas)
            self.complexObstacleArea.Add(area)
            self.stdItemModel.setItem(self.itemCount, QStandardItem(area.ToString()))
            # polygon  = rubberBand.asGeometry()
            # lineList = polygon.asPolygon()
            # self.resultPolylineAreaListForDrawing.append(PolylineArea(lineList[0]))
            self.itemCount += 1

            AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, area.PreviewArea, True)
            # self.constructionLayer.startEditing()
            # feature = QgsFeature()
            # feature.setGeometry(QgsGeometry.fromPolyline(area.PreviewArea.method_14_closed()))
            # self.constructionLayer.addFeature(feature)
            # self.constructionLayer.commitChanges()
    def btnRemove_Click(self):
        if self.selectedModelIndex != None:
            if QMessageBox.question(self, "Question", "Do you want to remove the selected item?", QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
                n = self.selectedModelIndex.row()

                self.complexObstacleArea.pop(n)
                self.stdItemModel.removeRow(self.selectedModelIndex.row())
                self.itemCount -= 1

                self.constructionLayer = AcadHelper.createVectorLayer("TempComplexObstacleAreaLayer")
                for area in self.complexObstacleArea:
                    AcadHelper.setGeometryAndAttributesInLayer(self.constructionLayer, area.PreviewArea, True)
                QgisHelper.appendToCanvas(define._canvas, [self.constructionLayer], "Temp")
                QgisHelper.ClearRubberBandInCanvas(define._canvas)



            pass
    def btnCaptureTrack_Click(self):
        pass
    def acceptEvent(self):
        QgisHelper.removeGroupFromName(define._mLayerTreeView, "Temp")

        # for node in define._mLayerTreeView.selectedNodes( True ) :
        #     item = node.parent()
        #     item._class_ = QgsLayerTreeGroup
        #     if isinstance(item, QgsLayerTreeGroup):
        #         if node.name() == "Temp":
        #             node.parent().removeChildNode( node )
        # QgisHelper.removeFromCanvas(define._canvas, [self.constructionLayer])
        self.accept()
    def rejectedEvent(self):
        QgisHelper.removeGroupFromName(define._mLayerTreeView, "Temp")
        self.reject()
    def lstAreas_Click(self, modelIndex):
        self.selectedModelIndex = modelIndex
        self.method_9()
    def method_9(self):
        if self.selectedModelIndex == None:
            self.ui.frame_Track.setVisible(False)
            return
        else:
            selectedArea = self.complexObstacleArea[self.selectedModelIndex.row()]
            QgisHelper.ClearRubberBandInCanvas(define._canvas)
            rBand = QgsRubberBand(define._canvas, QGis.Polygon)

            for point in selectedArea.PreviewArea.method_14_closed():
                rBand.addPoint(point)
            rBand.setFillColor( QColor(46, 64, 142, 100) )
            rBand.setBorderColor( QColor(0, 10, 238) )
            rBand.show()


            if not isinstance(selectedArea, SecondaryObstacleArea) or  not isinstance(selectedArea.area, SecondaryAreaStraight):
                self.ui.frame_Track.setVisible(False)
                return
            else:
                self.ui.txtTrack.setText(str(round(Unit.smethod_1(selectedArea.nominalTrack), 4)));
                self.ui.frame_Track.setVisible(True)
        # self.pnlTrack.Visible = true;
        # selectedItem = self.lstAreas.SelectedItem as SecondaryObstacleArea;
        # if (selectedItem == null || !(selectedItem.Area is SecondaryObstacleArea.SecondaryAreaStraight))
        # {
        #     self.pnlTrack.Value = double.NaN;
        #     self.pnlTrack.Visible = false;
        #     return;
        # }
        # self.pnlTrack.Value = Units.smethod_1(selectedItem.NominalTrack);
        # self.pnlTrack.Visible = true;
    def captureTrack(self):
        captureTrackTool= CaptureBearingTool(define._canvas, self.ui.txtTrack)
        define._canvas.setMapTool(captureTrackTool)