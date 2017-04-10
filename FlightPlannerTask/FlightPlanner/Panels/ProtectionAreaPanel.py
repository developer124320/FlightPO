#__author__ = 'Administrator'
from PyQt4 import QtCore, QtGui
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.types import ProtectionAreaType
from FlightPlanner.AcadHelper import AcadHelper
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea, SecondaryObstacleArea, ComplexObstacleArea, \
    PrimarySecondaryObstacleArea, SecondaryObstacleAreaWithManyPoints
from FlightPlanner.Obstacle.ObstacleAreaJig import ObstacleAreaJigSelectArea, ObstacleAreaJigCreateArea
from FlightPlanner.Obstacle.DlgComplexAreas import DlgComplexAreas
from FlightPlanner.Captions import Captions
from qgis.core import QGis, QgsLayerTreeGroup
from qgis.gui import QgsRubberBand
from FlightPlanner.Panels.Frame import Frame
import define

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class ProtectionAreaPanel(QtGui.QWidget):
    ClipboardObstacleArea = None
    def __init__(self, parent, surfaceType):
        QtGui.QWidget.__init__(self, parent)
        while not isinstance(parent, QtGui.QDialog):
            parent = parent.parent()
        self.setObjectName("ProtectionAreaPanel" + str(len(parent.findChildren(ProtectionAreaPanel))))


        self.resize(328, 45)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.basicFrame = Frame(self, "HL")
        self.horizontalLayout.addWidget(self.basicFrame)

        self.captionLabel = QtGui.QLabel(self.basicFrame)
        self.captionLabel.setMinimumSize(QtCore.QSize(150, 25))
        self.captionLabel.setMaximumSize(QtCore.QSize(150, 16777215))
        self.captionLabel.setObjectName("captionLabel")
        self.basicFrame.Add = self.captionLabel

        self.tableBox = QtGui.QFrame(self.basicFrame)
        self.tableBox.setFrameShape(QtGui.QFrame.StyledPanel)
        self.tableBox.setFrameShadow(QtGui.QFrame.Raised)
        self.tableBox.setObjectName("tableBox")
        self.horizontalLayout_tableBox = QtGui.QHBoxLayout(self.tableBox)
        self.horizontalLayout_tableBox.setObjectName("horizontalLayout_tableBox")
        self.comboBox = QtGui.QComboBox(self.tableBox)
        self.comboBox.setMinimumSize(QtCore.QSize(100, 23))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setMinimumWidth(70)
        # self.comboBox.setMaximumWidth(200)
        self.horizontalLayout_tableBox.addWidget(self.comboBox)
        self.btnPickScreen = QtGui.QPushButton(self.tableBox)
        self.btnPickScreen.setMinimumSize(QtCore.QSize(25, 25))
        self.btnPickScreen.setMaximumSize(QtCore.QSize(25, 25))
        self.btnPickScreen.setText("")
        self.btnPickScreen.setIconSize(QtCore.QSize(25, 16))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/coordinate_capture.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPickScreen.setIcon(icon)
        self.btnPickScreen.setObjectName("btnPickScreen")
        self.horizontalLayout_tableBox.addWidget(self.btnPickScreen)
        self.btnPreview = QtGui.QPushButton(self.tableBox)
        self.btnPreview.setMinimumSize(QtCore.QSize(25, 25))
        self.btnPreview.setMaximumSize(QtCore.QSize(25, 25))
        self.btnPreview.setText("")
        self.btnPreview.setIconSize(QtCore.QSize(25, 25))
        self.btnPreview.setObjectName("btnPreview")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/Preview_32x32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPreview.setIcon(icon)
        self.horizontalLayout_tableBox.addWidget(self.btnPreview)
        self.btnSelectionArea = QtGui.QPushButton(self.tableBox)
        self.btnSelectionArea.setMinimumSize(QtCore.QSize(25, 25))
        self.btnSelectionArea.setMaximumSize(QtCore.QSize(25, 25))
        self.btnSelectionArea.setText("")
        self.btnSelectionArea.setIconSize(QtCore.QSize(25, 25))
        self.btnSelectionArea.setObjectName("btnSelectionArea")
        self.horizontalLayout_tableBox.addWidget(self.btnSelectionArea)
        self.imgStatus = QtGui.QToolButton(self.tableBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imgStatus.sizePolicy().hasHeightForWidth())
        self.imgStatus.setSizePolicy(sizePolicy)
        self.imgStatus.setMinimumSize(QtCore.QSize(25, 25))
        self.imgStatus.setMaximumSize(QtCore.QSize(25, 25))
        self.imgStatus.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.imgStatus.setAcceptDrops(False)
        self.imgStatus.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/Warning.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.imgStatus.setIcon(icon)
        self.imgStatus.setIconSize(QtCore.QSize(25, 25))
        self.imgStatus.setCheckable(False)
        self.imgStatus.setObjectName("imgStatus")
        self.horizontalLayout_tableBox.addWidget(self.imgStatus)
        self.basicFrame.Add = self.tableBox

        # spacerItem = QtGui.QSpacerItem(10,10,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        # self.horizontalLayout.addItem(spacerItem)


        self.retranslateUi()

        self.comboBox.addItems(["Primary", "Secondary", "Primary & Secondary", "Complex"])
        self.comboBox.currentIndexChanged.connect(self.comboBoxCurrentIndexChanged)
        self.imgStatus.clicked.connect(self.btnDropDown_Click)
        self.btnPickScreen.clicked.connect(self.btnPickScreen_Click)
        self.btnPreview.clicked.connect(self.btnPreview_Click)
        QtCore.QMetaObject.connectSlotsByName(self)
        
        self.updating = True;
        self.comboBox.setCurrentIndex(0);
        self.updating = False;
        self.rubberBand = None
        self.area = None
        self.complexDlg = None
        self.surfaceType = surfaceType
        self.method_2()
        self.btnSelectionArea.setVisible(False)
        self.forcedSelectionAreaOverwrite = False
        self.priviewClickFlag = False
        self.resultLayerList = []
    def retranslateUi(self):
        self.setWindowTitle(_translate("ProtectionAreaPanel", "ProtectionAreaPanel", None))
        self.captionLabel.setText(_translate("ProtectionAreaPanel", "Protection Area:", None))
        self.btnPickScreen.setToolTip(_translate("ProtectionAreaPanel", "Pick from screen", None))
        self.btnPreview.setToolTip(_translate("ProtectionAreaPanel", "Preview protection area(s)", None))
        self.btnSelectionArea.setToolTip(_translate("ProtectionAreaPanel", "Preview/overwrite selection area", None))
    def comboBoxCurrentIndexChanged(self):
        self.method_2()
        self.method_3()
        self.emit(QtCore.SIGNAL("Event0"), self)
    def btnPickScreen_Click(self):
        self.area = None
        self.priviewClickFlag = False
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        # self.rubberBand = None
        if self.comboBox.currentIndex() == ProtectionAreaType.Complex:
            self.complexDlg = DlgComplexAreas(self)
            self.complexDlg.show()
            self.complexDlg.ui.buttonBoxOkCancel.accepted.connect(self.ComplexAreaResult)
            return
        elif self.comboBox.currentIndex() == ProtectionAreaType.PrimaryAndSecondary:
            obstacleAreaJig= ObstacleAreaJigSelectArea(define._canvas, self.comboBox.currentIndex())
            define._canvas.setMapTool(obstacleAreaJig)
            self.connect(obstacleAreaJig, QtCore.SIGNAL("outputResult"), self.AreaResult)
            return
        if QtGui.QMessageBox.question(self, "Question", "Please click \"Yes\" if you want to create new area.\nPlease click \"No\" if you want to select any area.", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
            # if self.comboBox.currentIndex() == ProtectionAreaType.Primary:
            obstacleAreaJig= ObstacleAreaJigCreateArea(define._canvas, self.comboBox.currentIndex())
            define._canvas.setMapTool(obstacleAreaJig)
            self.connect(obstacleAreaJig, QtCore.SIGNAL("outputResult"), self.AreaResult)
            # elif self.comboBox.currentIndex() == ProtectionAreaType.Secondary:
        else:
            obstacleAreaJig= ObstacleAreaJigSelectArea(define._canvas, self.comboBox.currentIndex())
            define._canvas.setMapTool(obstacleAreaJig)
            self.connect(obstacleAreaJig, QtCore.SIGNAL("outputResult"), self.AreaResult)
    def ComplexAreaResult(self):
        self.area = self.complexDlg.complexObstacleArea

        self.DrawCanvas()


        self.method_2();
        self.method_3();

    def DrawCanvas(self):
        qgsLayerTreeView = define._mLayerTreeView
        groupName = self.surfaceType
        layerTreeModel = qgsLayerTreeView.layerTreeModel()
        layerTreeGroup = layerTreeModel.rootGroup()
        rowCount = layerTreeModel.rowCount()
        groupExisting = False
        if rowCount > 0:
            for i in range(rowCount):
                qgsLayerTreeNode = layerTreeModel.index2node(layerTreeModel.index(i, 0))
                if qgsLayerTreeNode.nodeType() == 0:
                    qgsLayerTreeNode._class_ =  QgsLayerTreeGroup
                    if isinstance(qgsLayerTreeNode, QgsLayerTreeGroup) and qgsLayerTreeNode.name() == groupName:
                        groupExisting = True

        if groupExisting:
            if len(self.resultLayerList) > 0:
                QgisHelper.removeFromCanvas(define._canvas, self.resultLayerList)
                self.resultLayerList = []
            else:
                QtGui.QMessageBox.warning(self, "Warning", "Please remove \"" + self.surfaceType + "\" layer group from LayerTreeView.")
                return

        constructionLayer = AcadHelper.createVectorLayer(self.surfaceType);
        if self.comboBox.currentIndex() == ProtectionAreaType.Primary or self.comboBox.currentIndex() == ProtectionAreaType.Secondary:
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, self.area.PreviewArea, True)

        elif self.comboBox.currentIndex() == ProtectionAreaType.PrimaryAndSecondary:
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, self.area.primaryArea.PreviewArea, True)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, self.area.secondaryArea1.PreviewArea, True)
            AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, self.area.secondaryArea2.PreviewArea, True)
        else:

            for obstacleArea in self.area:
                AcadHelper.setGeometryAndAttributesInLayer(constructionLayer, obstacleArea.PreviewArea, True)
        QgisHelper.appendToCanvas(define._canvas, [constructionLayer], self.surfaceType)
        self.resultLayerList = [constructionLayer]
    def AreaResult(self, resultArea, resultRubberBand):
        self.area = resultArea
        self.rubberBand = resultRubberBand
        QgisHelper.ClearRubberBandInCanvas(define._canvas)
        self.DrawCanvas()
        self.method_2()
        self.method_3()
    def btnPreview_Click(self):
        self.priviewClickFlag = not self.priviewClickFlag
        if not self.priviewClickFlag:
            QgisHelper.ClearRubberBandInCanvas(define._canvas)
            return
        if self.comboBox.currentIndex() == ProtectionAreaType.Primary:
            rBand = QgsRubberBand(define._canvas, QGis.Polygon)

            for point in self.area.PreviewArea.method_14():
                rBand.addPoint(point)
            rBand.setFillColor( QtGui.QColor(46, 64, 142, 100) )
            rBand.setBorderColor( QtGui.QColor(0, 10, 238) )
            rBand.show()
        elif self.comboBox.currentIndex() == ProtectionAreaType.Secondary:
            rBand = QgsRubberBand(define._canvas, QGis.Polygon)
            if isinstance(self.area, SecondaryObstacleAreaWithManyPoints):
                for point in self.area.PreviewArea.method_14():
                    rBand.addPoint(point)
                rBand.setFillColor( QtGui.QColor(46, 64, 142, 100) )
                rBand.setBorderColor( QtGui.QColor(0, 10, 238) )
                rBand.show()
            else:
                for point in self.area.area.PreviewArea.method_14():
                    rBand.addPoint(point)
                rBand.setFillColor( QtGui.QColor(46, 64, 142, 100) )
                rBand.setBorderColor( QtGui.QColor(0, 10, 238) )
                rBand.show()
        elif self.comboBox.currentIndex() == ProtectionAreaType.PrimaryAndSecondary:
            rBand = QgsRubberBand(define._canvas, QGis.Polygon)
            for point in self.area.primaryArea.PreviewArea.method_14():
                rBand.addPoint(point)
            rBand.setFillColor( QtGui.QColor(46, 64, 142, 100) )
            rBand.setBorderColor( QtGui.QColor(0, 10, 238) )
            rBand.show()

            rBand = QgsRubberBand(define._canvas, QGis.Polygon)
            for point in self.area.secondaryArea1.PreviewArea.method_14():
                rBand.addPoint(point)
            rBand.setFillColor( QtGui.QColor(46, 64, 142, 100) )
            rBand.setBorderColor( QtGui.QColor(0, 10, 238) )
            rBand.show()

            rBand = QgsRubberBand(define._canvas, QGis.Polygon)
            for point in self.area.secondaryArea2.PreviewArea.method_14():
                rBand.addPoint(point)
            rBand.setFillColor( QtGui.QColor(46, 64, 142, 100) )
            rBand.setBorderColor( QtGui.QColor(0, 10, 238) )
            rBand.show()
        else:
            for obstacleArea in self.area:
                if isinstance(obstacleArea, PrimaryObstacleArea):
                    rBand = QgsRubberBand(define._canvas, QGis.Polygon)

                    for point in obstacleArea.PreviewArea.method_14():
                        rBand.addPoint(point)
                    rBand.setFillColor( QtGui.QColor(46, 64, 142, 100) )
                    rBand.setBorderColor( QtGui.QColor(0, 10, 238) )
                    rBand.show()
                else:
                    rBand = QgsRubberBand(define._canvas, QGis.Polygon)
                    if isinstance(obstacleArea, SecondaryObstacleAreaWithManyPoints):
                        for point in obstacleArea.PreviewArea.method_14():
                            rBand.addPoint(point)
                        rBand.setFillColor( QtGui.QColor(46, 64, 142, 100) )
                        rBand.setBorderColor( QtGui.QColor(0, 10, 238) )
                        rBand.show()
                    else:
                        for point in obstacleArea.area.PreviewArea.method_14():
                            rBand.addPoint(point)
                        rBand.setFillColor( QtGui.QColor(46, 64, 142, 100) )
                        rBand.setBorderColor( QtGui.QColor(0, 10, 238) )
                        rBand.show()

        define._canvas.refresh()
    def btnDropDown_Click(self):
        self.mnuArea = QtGui.QMenu("")
        self.mniCopy = QgisHelper.createAction(self, "Copy", self.menuCopyActionEvent, None, "copy", None)
        self.mniPaste = QgisHelper.createAction(self, "Paste", self.menuPasteActionEvent, None, "paste", None)
        self.mnuArea.addAction(self.mniCopy)
        self.mnuArea.addAction(self.mniPaste)

        flag = True;
        obstacleArea = self.area;
        self.mniCopy.setEnabled(False if(obstacleArea == None) else obstacleArea.IsValid);
        if (self.mniCopy.isEnabled()):
            self.mniCopy.setText("{%s} {%s}"%(Captions.COPY, obstacleArea.ToString()));
        if (self.ClipboardObstacleArea == None):
            flag = False;
        else:
            flag = self.comboBox.count() == 4 if(isinstance(self.ClipboardObstacleArea, ComplexObstacleArea)) else True;
        self.mniPaste.setEnabled(flag);
        if (self.mniPaste.isEnabled()):
            self.mniPaste.setText("{%s} {%s}"%(Captions.PASTE, self.ClipboardObstacleArea.ToString()));

        rcRect = self.imgStatus.geometry()
        ptPoint = rcRect.bottomRight()
        self.mnuArea.exec_( self.mapToGlobal(ptPoint) )
    def menuCopyActionEvent(self):
        self.ClipboardObstacleArea = self.area;
        self.method_2()
        self.method_3()
        pass
    def menuPasteActionEvent(self):
        self.area = self.ClipboardObstacleArea;
        if (self.area != None):
            self.updating = True;
            try:
                if isinstance(self.area , PrimaryObstacleArea):
                    self.comboBox.setCurrentIndex(0);
                elif isinstance(self.area , SecondaryObstacleArea):
                    self.comboBox.setCurrentIndex(1);
                elif isinstance(self.area , PrimarySecondaryObstacleArea):
                    self.comboBox.setCurrentIndex(2);
                else:
                    self.comboBox.setCurrentIndex(3);
            finally:
                self.updating = False;
                self.method_2();
                self.method_3();
                # self.method_7(self, EventArgs.Empty);
            self.DrawCanvas()
    def method_2(self):
        obstacleArea = self.area;
        if (obstacleArea == None):
            self.btnPreview.setEnabled(False);
            self.btnSelectionArea.setEnabled(False);
        else:
            self.btnPreview.setEnabled(obstacleArea.IsValidForPreview);
            # self.btnSelectionArea.Enabled = obstacleArea.IsValid;
        # self.btnSelectionArea.setVisible(self.Value != ProtectionAreaType.Primary);
    def method_3(self):
        obstacleArea = self.area;
        if (obstacleArea != None):
            if (not obstacleArea.IsValid):
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("Resource/abort.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.imgStatus.setIcon(icon)
            else:
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("Resource/check.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.imgStatus.setIcon(icon)
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Resource/Warning.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.imgStatus.setIcon(icon)
    def get_Value(self):
        return self.comboBox.currentIndex()
    def set_Value(self, index):
        self.updating = True
        self.comboBox.setCurrentIndex(index)
        self.method_2()
        self.method_3()
        self.updating = False
    Value = property(get_Value, set_Value, None, None)

    def get_SelectedArea(self):
        return self.area
    def set_SelectedArea(self, value):
        self.area = value
    SelectedArea = property(get_SelectedArea, set_SelectedArea, None, None )

    def get_ForcedSelectionAreaOverwrite(self):
        return self.forcedSelectionAreaOverwrite
    def set_ForcedSelectionAreaOverwrite(self, value):
        self.forcedSelectionAreaOverwrite = value
    ForcedSelectionAreaOverwrite = property(get_ForcedSelectionAreaOverwrite, set_ForcedSelectionAreaOverwrite, None, None)

    def get_AllowComplexArea(self):
        return self.comboBox.count() == 4;
    def set_AllowComplexArea(self, value):
        if (value):
            if (self.comboBox.count() < 4):
                self.comboBox.addItem("Complex");
                return;
        elif (self.comboBox.count() == 4):
            selectedIndex = self.comboBox.currentIndex();
            self.comboBox.removeItem(3);
            self.comboBox.setCurrentIndex( min(selectedIndex, self.comboBox.count() - 1));
    AllowComplexArea = property(get_AllowComplexArea, set_AllowComplexArea, None, None)

    def get_SelectedIndex(self):
        return self.comboBox.currentIndex()
    def set_SelectedIndex(self, index):
        if self.comboBox.count() == 0:
            return
        if index > self.comboBox.count() - 1:
            self.comboBox.setCurrentIndex(0)
        else:
            self.comboBox.setCurrentIndex(index)
    SelectedIndex = property(get_SelectedIndex, set_SelectedIndex, None, None)
