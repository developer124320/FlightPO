'''
Created on 27 Apr 2014

@author: Administrator
'''
from PyQt4.QtGui import QWidget, QDialog, QCheckBox, QPushButton, QColorDialog, \
    QLabel,  QGridLayout, QDoubleSpinBox
from PyQt4.QtCore import QSize, Qt
from qgis.gui import QgsColorButton, QgsSymbolV2SelectorDialog
from qgis.core import  QgsStyleV2, QgsSymbolLayerV2Utils
import qrc_images
class QgsAnnotationWidget(QWidget):
    def __init__(self, parent, item):
        QWidget.__init__(self, parent)
        self.gridLayout_2 = QGridLayout(self)
        self.gridLayout_2.setObjectName(("gridLayout_2"))
        self.mMapPositionFixedCheckBox = QCheckBox(self)
        self.mMapPositionFixedCheckBox.setObjectName(("mMapPositionFixedCheckBox"))
        self.gridLayout_2.addWidget(self.mMapPositionFixedCheckBox, 0, 0, 1, 1)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(("gridLayout"))
        self.mFrameColorButton = QgsColorButton(self)
        self.mFrameColorButton.setText((""))
        self.mFrameColorButton.setObjectName(("mFrameColorButton"))
        self.gridLayout.addWidget(self.mFrameColorButton, 3, 1, 1, 1)
        self.mFrameColorButton.colorChanged.connect(self.on_mFrameColorButton_colorChanged)
        self.mBackgroundColorLabel = QLabel(self)
        self.mBackgroundColorLabel.setObjectName(("mBackgroundColorLabel"))
        self.gridLayout.addWidget(self.mBackgroundColorLabel, 2, 0, 1, 1)
        self.mMapMarkerLabel = QLabel(self)
        self.mMapMarkerLabel.setObjectName(("mMapMarkerLabel"))
        self.gridLayout.addWidget(self.mMapMarkerLabel, 0, 0, 1, 1)
        self.mBackgroundColorButton = QgsColorButton(self)
        self.mBackgroundColorButton.setText((""))
        self.mBackgroundColorButton.setObjectName(("mBackgroundColorButton"))
        self.gridLayout.addWidget(self.mBackgroundColorButton, 2, 1, 1, 1)
        self.mBackgroundColorButton.colorChanged.connect(self.on_mBackgroundColorButton_colorChanged)
        self.mMapMarkerButton = QPushButton(self)
        self.mMapMarkerButton.setText((""))
        self.mMapMarkerButton.setObjectName(("mMapMarkerButton"))
        self.gridLayout.addWidget(self.mMapMarkerButton, 0, 1, 1, 1)
        self.mMapMarkerButton.clicked.connect(self.on_mMapMarkerButton_clicked)
        self.mFrameWidthLabel = QLabel(self)
        self.mFrameWidthLabel.setObjectName(("mFrameWidthLabel"))
        self.gridLayout.addWidget(self.mFrameWidthLabel, 1, 0, 1, 1)
        self.mFrameWidthSpinBox = QDoubleSpinBox(self)
        self.mFrameWidthSpinBox.setObjectName(("mFrameWidthSpinBox"))
        self.gridLayout.addWidget(self.mFrameWidthSpinBox, 1, 1, 1, 1)
        self.mFrameColorLabel = QLabel(self)
        self.mFrameColorLabel.setObjectName(("mFrameColorLabel"))
        self.gridLayout.addWidget(self.mFrameColorLabel, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.mMapMarkerLabel.setBuddy(self.mMapMarkerButton)
        self.mFrameWidthLabel.setBuddy(self.mFrameWidthSpinBox)
                
        self.setWindowTitle("QgsAnnotationWidgetBase")
        self.mMapPositionFixedCheckBox.setText("Fixed map position")
        self.mBackgroundColorLabel.setText("Background color")
        self.mMapMarkerLabel.setText("Map marker")
        self.mFrameWidthLabel.setText( "Frame width")
        self.mFrameColorLabel.setText( "Frame color")
        self.setLayout(self.gridLayout_2)
        self.mItem = item
        if ( self.mItem != None ):
            self.blockAllSignals( True )
            
            if ( self.mItem.mapPositionFixed() ):
                self.mMapPositionFixedCheckBox.setCheckState( Qt.Checked )
            else:
                self.mMapPositionFixedCheckBox.setCheckState( Qt.Unchecked )
            
            self.mFrameWidthSpinBox.setValue( self.mItem.frameBorderWidth() )
            self.mFrameColorButton.setColor( self.mItem.frameColor() )
            self.mFrameColorButton.setColorDialogTitle(  "Select frame color" )
            self.mFrameColorButton.setColorDialogOptions( QColorDialog.ShowAlphaChannel )
            self.mBackgroundColorButton.setColor( self.mItem.frameBackgroundColor() )
            self.mBackgroundColorButton.setColorDialogTitle(  "Select background color"  )
            self.mBackgroundColorButton.setColorDialogOptions( QColorDialog.ShowAlphaChannel )
            self.symbol = self.mItem.markerSymbol()
            if ( self.symbol != None ):
                self.mMarkerSymbol =  self.symbol.clone() 
                self.updateCenterIcon()
            self.blockAllSignals( False )
        
    def apply(self):
        if ( self.mItem != None ):
            self.mItem.setMapPositionFixed( self.mMapPositionFixedCheckBox.checkState() == Qt.Checked )
            self.mItem.setFrameBorderWidth( self.mFrameWidthSpinBox.value() )
            self.mItem.setFrameColor( self.mFrameColorButton.color() )
            self.mItem.setFrameBackgroundColor( self.mBackgroundColorButton.color() )
            self.mItem.setMarkerSymbol( self.mMarkerSymbol )
            self.mMarkerSymbol = None  #//item takes ownership
            self.mItem.update()
        
    def blockAllSignals(self, block ):
        self.mMapPositionFixedCheckBox.blockSignals( block )
        self.mMapMarkerButton.blockSignals( block )
        self.mFrameWidthSpinBox.blockSignals( block )
        self.mFrameColorButton.blockSignals( block )
    def on_mMapMarkerButton_clicked(self):
        if ( self.mMarkerSymbol == None ):
            return
        markerSymbol = self.mMarkerSymbol.clone() 
        dlg = QgsSymbolV2SelectorDialog ( markerSymbol, QgsStyleV2.defaultStyle(), None, self )
        if ( dlg.exec_()!= QDialog.Rejected ):
            self.mMarkerSymbol = markerSymbol
            self.updateCenterIcon()
    def on_mFrameColorButton_colorChanged(self, color ):
        if ( self.mItem == None):
            return
        self.mItem.setFrameColor( color )
        
    def updateCenterIcon(self):
        if ( self.mMarkerSymbol == None ):
            return
        icon = QgsSymbolLayerV2Utils.symbolPreviewIcon( self.mMarkerSymbol, self.mMapMarkerButton.iconSize() )
        self.mMapMarkerButton.setIcon( icon )
    def on_mBackgroundColorButton_colorChanged(self, color ):
        if ( self.mItem == None ):
            return
        self.mItem.setFrameBackgroundColor( color )
        
    
    
