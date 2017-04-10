'''
Created on Mar 31, 2015

@author: jin
'''
# from map.ui_layerSaveAsDlg import ui_layerSaveAsDlg
from qgis.core import QgsCoordinateReferenceSystem, QgsSymbolV2, QgsStyleV2, QgsProject, QgsPalLayerSettings
from qgis.gui import QgsGenericProjectionSelector, QgsMultiBandColorRendererWidget, QgsPalettedRendererWidget, QgsSingleBandGrayRendererWidget, QgsSingleBandPseudoColorRendererWidget

from PyQt4.QtGui import QDialog, QVBoxLayout, QFrame, QSizePolicy, QGroupBox, QDialogButtonBox, QHBoxLayout, QStackedWidget, QWidget
from PyQt4.QtCore import Qt, QCoreApplication, SIGNAL, SLOT, QObject
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
import define
import qrc_images 
from map.ui_propertyDlg import Ui_VectorLayerProPertyDialog
class rasterLayerPropertyDlg(QDialog):
    '''
    classdocs
    '''
    def __init__(self, parent, layer):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self.resize(200, 200)

        self.rasterLayer = layer

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        verticalLayout = QVBoxLayout(self)
        verticalLayout.setObjectName("verticalLayout")
        stackedWidget = QStackedWidget(self)
        stackedWidget.setObjectName("stackedWidget")
        pageRender = QWidget(stackedWidget)
        pageRender.setObjectName("pageRender")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pageRender.sizePolicy().hasHeightForWidth())
        pageRender.setSizePolicy(sizePolicy)

        horizontalLayout = QHBoxLayout(pageRender)
        horizontalLayout.setObjectName("horizontalLayout")
        frameRender = QFrame(pageRender)
        frameRender.setObjectName("frameRender")
        frameRender.setFrameShape(QFrame.StyledPanel)
        frameRender.setFrameShadow(QFrame.Raised)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frameRender.sizePolicy().hasHeightForWidth())
        frameRender.setSizePolicy(sizePolicy)
        self.vLayoutFrameRender = QVBoxLayout(frameRender)
        self.vLayoutFrameRender.setObjectName("vLayoutFrameRender")

        horizontalLayout.addWidget(frameRender)
        self.cmbRendererType = ComboBoxPanel(frameRender)
        self.cmbRendererType.Caption = "Render Type"
        self.cmbRendererType.LabelWidth = 70
        self.cmbRendererType.Items = ["Mutiband color", "Paletted", "Singleband gray", "Singleband pseudocolor"]
        self.connect(self.cmbRendererType, SIGNAL("Event_0"), self.cmbRendererType_currentIndexChanged)

        self.vLayoutFrameRender.addWidget(self.cmbRendererType)
        self.gbRenderer = GroupBox(frameRender)
        self.gbRenderer.Caption = self.cmbRendererType.SelectedItem
        self.vLayoutFrameRender.addWidget(self.gbRenderer)

        self.qgsMultiBandColorRendererWidget = QgsMultiBandColorRendererWidget(self.rasterLayer)
        self.qgsPalettedRendererWidget = QgsPalettedRendererWidget(self.rasterLayer)
        self.qgsSingleBandGrayRendererWidget = QgsSingleBandGrayRendererWidget(self.rasterLayer)
        self.qgsSingleBandPseudoColorRendererWidget = QgsSingleBandPseudoColorRendererWidget(self.rasterLayer)


        self.gbRenderer.Add = self.qgsMultiBandColorRendererWidget
        self.gbRenderer.Add = self.qgsPalettedRendererWidget
        self.gbRenderer.Add = self.qgsSingleBandGrayRendererWidget
        self.gbRenderer.Add = self.qgsSingleBandPseudoColorRendererWidget

        self.qgsPalettedRendererWidget.setVisible(False)
        self.qgsSingleBandGrayRendererWidget.setVisible(False)
        self.qgsSingleBandPseudoColorRendererWidget.setVisible(False)

        stackedWidget.addWidget(pageRender)
        # page_2 = QWidget()
        # page_2.setObjectName("page_2")
        # stackedWidget.addWidget(page_2)

        verticalLayout.addWidget(stackedWidget)

        buttonBox = QDialogButtonBox(self)
        buttonBox.setObjectName("buttonBox")
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok | QDialogButtonBox.Apply)
        btnApply = buttonBox.button(QDialogButtonBox.Apply)
        btnApply.clicked.connect(self.btnApply_clicked)
        verticalLayout.addWidget(buttonBox)


        # retranslateUi(Dialog)
        buttonBox.accepted.connect(self.OK)
        buttonBox.rejected.connect(self.reject)

        if self.rasterLayer.renderer().bandCount() == 1:
            self.cmbRendererType.SelectedIndex = 2
        elif self.rasterLayer.renderer().bandCount() > 1:
            self.cmbRendererType.SelectedIndex = 0

        # QObject.connect(buttonBox, SIGNAL("accepted()"), self, SLOT(accept()))
        # QObject.connect(buttonBox, SIGNAL("rejected()"), self, SLOT(reject()))
    def cmbRendererType_currentIndexChanged(self):

        if self.cmbRendererType.SelectedIndex == 0:
            self.qgsPalettedRendererWidget.setVisible(False)
            self.qgsSingleBandGrayRendererWidget.setVisible(False)
            self.qgsSingleBandPseudoColorRendererWidget.setVisible(False)
            # self.resize(200, 200)
            self.qgsMultiBandColorRendererWidget.setVisible(True)
        elif self.cmbRendererType.SelectedIndex == 1:
            self.qgsMultiBandColorRendererWidget.setVisible(False)
            self.qgsSingleBandGrayRendererWidget.setVisible(False)
            self.qgsSingleBandPseudoColorRendererWidget.setVisible(False)
            # self.resize(200, 200)
            self.qgsPalettedRendererWidget.setVisible(True)
        elif self.cmbRendererType.SelectedIndex == 2:
            self.qgsMultiBandColorRendererWidget.setVisible(False)
            self.qgsPalettedRendererWidget.setVisible(False)
            self.qgsSingleBandPseudoColorRendererWidget.setVisible(False)
            # self.resize(200, 200)
            self.qgsSingleBandGrayRendererWidget.setVisible(True)
        else:
            self.qgsMultiBandColorRendererWidget.setVisible(False)
            self.qgsPalettedRendererWidget.setVisible(False)
            self.qgsSingleBandGrayRendererWidget.setVisible(False)
            self.qgsSingleBandPseudoColorRendererWidget.setVisible(True)

        self.resize(200, 200)
        self.gbRenderer.Caption = self.cmbRendererType.SelectedItem


    def selectCrs(self):
        projectionDlg = QgsGenericProjectionSelector(self)
        projectionDlg.setSelectedAuthId(self.mCrs.authid())
        if projectionDlg.exec_():
            self.mCrs = QgsCoordinateReferenceSystem(projectionDlg.selectedCrsId(), QgsCoordinateReferenceSystem.InternalCrsId)
            self.ui.txtCrs.setText(self.mCrs.authid() + " - " + self.mCrs.description())
    def changeStackWidget(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)
    def btnApply_clicked(self):
        if self.cmbRendererType.SelectedIndex == 0:
            self.rasterLayer.setRenderer(self.qgsMultiBandColorRendererWidget.renderer())
        elif self.cmbRendererType.SelectedIndex == 1:
            self.rasterLayer.setRenderer(self.qgsPalettedRendererWidget.renderer())
        elif self.cmbRendererType.SelectedIndex == 2:
            self.rasterLayer.setRenderer(self.qgsSingleBandGrayRendererWidget.renderer())
        else:
            self.rasterLayer.setRenderer(self.qgsSingleBandPseudoColorRendererWidget.renderer())
        self.rasterLayer.triggerRepaint()
    def OK(self):
        self.btnApply_clicked()
        QDialog.accept(self)