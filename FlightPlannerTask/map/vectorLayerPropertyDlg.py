'''
Created on Mar 31, 2015

@author: jin
'''
# from map.ui_layerSaveAsDlg import ui_layerSaveAsDlg
from qgis.core import QgsCoordinateReferenceSystem, QgsSymbolV2, QgsStyleV2, QgsProject, QgsPalLayerSettings, QGis
from qgis.gui import QgsGenericProjectionSelector, QgsFieldExpressionWidget, QgsRendererV2PropertiesDialog

from PyQt4.QtGui import QDialog, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy
from PyQt4.QtCore import Qt, QCoreApplication, SIGNAL, SLOT
import define
import qrc_images 
from map.ui_propertyDlg import Ui_VectorLayerProPertyDialog
class vectorLayerPropertyDlg(QDialog):
    '''
    classdocs
    '''
    def __init__(self, parent, layer):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self.ui = Ui_VectorLayerProPertyDialog()
        self.ui.setupUi(self)
        
        self.ui.txtLayerName.setText(layer.name ())
        self.ui.txtLayerSource.setText(layer.source ())
        self.ui.txtCrs.setText(layer.crs().authid() + " - " + layer.crs().description ())
        self.ui.btnCrsSelect.clicked.connect(self.selectCrs)
        self.mCrs = layer.crs()
        self.vLayer = layer
        self.ui.mOptionsListWidget.currentRowChanged.connect(self.changeStackWidget)
        
        ''' init RenderV2 Widget'''          
        self.mRendererDialog = QgsRendererV2PropertiesDialog( self.vLayer, QgsStyleV2.defaultStyle(), True )
        self.ui.stackedWidget.insertWidget(1, self.mRendererDialog)
        self.ui.buttonBox.accepted.connect(self.OK)
        
        frame_Label = QFrame()
        verticalLayout_Label = QVBoxLayout(frame_Label)        
        self.mLabelWidget = QgsFieldExpressionWidget()
        self.mLabelWidget.setLayer(layer)
        verticalLayout_Label.addWidget(self.mLabelWidget)
        
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        verticalLayout_Label.addItem(spacerItem)
        frame_Label.setLayout(verticalLayout_Label)
        self.ui.stackedWidget.insertWidget(2, frame_Label)
#         self.ui.buttonBox.accepted.connect(self.OK)
    def selectCrs(self):
        projectionDlg = QgsGenericProjectionSelector(self)
        projectionDlg.setSelectedAuthId(self.mCrs.authid())
        if projectionDlg.exec_():
            self.mCrs = QgsCoordinateReferenceSystem(projectionDlg.selectedCrsId(), QgsCoordinateReferenceSystem.InternalCrsId)
            self.ui.txtCrs.setText(self.mCrs.authid() + " - " +self.mCrs.description())
    def changeStackWidget(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)
    def OK(self):
        self.vLayer.setCrs(self.mCrs)
        self.mRendererDialog.apply()
        self.vLayer.triggerRepaint()
        if self.ui.stackedWidget.currentIndex() == 2 and self.mLabelWidget.currentText() != "":
            self.vLayer.setCustomProperty("labeling", "pal")
            self.vLayer.setCustomProperty("labeling/enabled", "true")
            self.vLayer.setCustomProperty("labeling/fontFamily", "Arial")
            self.vLayer.setCustomProperty("labeling/fontSize", "8")
            self.vLayer.setCustomProperty("labeling/fieldName", self.mLabelWidget.currentText())

            # palLayerSetting = QgsPalLayerSettings()
            # palLayerSetting.readFromLayer(self.vLayer)
            # palLayerSetting.enabled = True
            # palLayerSetting.fieldName = self.mLabelWidget.currentText()
            # palLayerSetting.isExpression = True
            if self.vLayer.geometryType() == QGis.Line:
                self.vLayer.setCustomProperty("labeling/placement", "2")
                self.vLayer.setCustomProperty("labeling/placementFlags", str(QgsPalLayerSettings.AboveLine))
                # palLayerSetting.placement = QgsPalLayerSettings.Line
                # palLayerSetting.placementFlags = QgsPalLayerSettings.AboveLine
            elif self.vLayer.geometryType() == QGis.Point:
                self.vLayer.setCustomProperty("labeling/placement", "0")
                self.vLayer.setCustomProperty("labeling/placementFlags", str(QgsPalLayerSettings.AroundPoint))
                # self.vLayer.setCustomProperty("labeling/placementFlags", "0")
                # palLayerSetting.placement = QgsPalLayerSettings.Points
                # palLayerSetting.placementFlags = QgsPalLayerSettings.AroundPoint
            else:
                self.vLayer.setCustomProperty("labeling/placement", "3")
                self.vLayer.setCustomProperty("labeling/placementFlags", str(QgsPalLayerSettings.AboveLine))
                # palLayerSetting.placement = QgsPalLayerSettings.PolygonBoundary
                # palLayerSetting.placementFlags = QgsPalLayerSettings.AboveLine
            # palLayerSetting.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '8', "")
            # palLayerSetting.writeToLayer(self.vLayer)
        elif self.ui.stackedWidget.currentIndex() == 2 and self.mLabelWidget.currentText() == "":
            self.vLayer.setCustomProperty("labeling", "")
        QgsProject.instance().dirty( True )
        QDialog.accept(self)