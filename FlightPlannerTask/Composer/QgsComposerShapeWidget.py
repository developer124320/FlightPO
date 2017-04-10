
from PyQt4.QtGui import QWidget, QMenu, QDoubleValidator, QColorDialog,\
    QDialog, QFontDialog, QIcon, QPixmap, QAction, QComboBox, QListWidgetItem, QTextCursor
from PyQt4 import uic
from PyQt4.QtCore import SIGNAL, SLOT, QString, Qt, QStringList, QSettings
from Composer.QgsComposerItemWidget import QgsComposerItemWidget

from qgis.core import QgsComposition, QgsComposerMap, QgsComposerMergeCommand, QGis, QgsRectangle, QgsStyleV2,\
    QgsSymbolLayerV2Utils, QgsComposerShape, QgsExpressionContext, QgsComposerObject, QgsProject, QgsCoordinateReferenceSystem,\
    QgsComposerMapOverview
from qgis.gui import QgsSymbolV2SelectorDialog, QgsDataDefinedButton, QgsGenericProjectionSelector, QgsExpressionBuilderDialog
import define, time
from Type.switch import switch

from Composer.ui_qgscomposershapewidget import Ui_QgsComposerShapeWidgetBase
from Composer.ui_qgscomposeritemwidget import Ui_QgsComposerItemWidgetBase
# FORM_CLASS, _ = uic.loadUiType(define.appPath + "/UI/Composer/qgsComposerMapWidgetBase.ui")

class QgsComposerShapeWidget(Ui_QgsComposerShapeWidgetBase):
    def __init__(self, parent, composerShape):
        Ui_QgsComposerShapeWidgetBase.__init__(self, parent)

        self.mComposerShape = composerShape
        
        itemPropertiesWidget = QgsComposerItemWidget( self, composerShape )

        #shapes don't use background or frame, since the symbol style is set through a QgsSymbolV2SelectorDialog
        itemPropertiesWidget.showBackgroundGroup( False )
        itemPropertiesWidget.showFrameGroup( False )
        
        self.mainLayout.addWidget( itemPropertiesWidget )
        
        self.blockAllSignals( True )
        
        #shape types
        self.mShapeComboBox.addItem( QString( "Ellipse" ) )
        self.mShapeComboBox.addItem( QString( "Rectangle" ) )
        self.mShapeComboBox.addItem( QString( "Triangle" ) )
        
        self.setGuiElementValues()
        
        self.blockAllSignals( False )
        
        if ( self.mComposerShape ):
            self.connect( self.mComposerShape, SIGNAL( "itemChanged()" ), self.setGuiElementValues)

        self.connect(self.mCornerRadiusSpinBox, SIGNAL("valueChanged( double )"), self.on_mCornerRadiusSpinBox_valueChanged)

        self.timeStart = 0
        self.timeEnd = 0

    def blockAllSignals( self, block ):
        self.mShapeComboBox.blockSignals( block )
        self.mCornerRadiusSpinBox.blockSignals( block )
        self.mShapeStyleButton.blockSignals( block )

    def setGuiElementValues(self):
        if ( not self.mComposerShape ):
            return
        
        self.blockAllSignals( True )
        
        self.updateShapeStyle()
        
        self.mCornerRadiusSpinBox.setValue( self.mComposerShape.cornerRadius() )
        if ( self.mComposerShape.shapeType() == QgsComposerShape.Ellipse ):
            self.mShapeComboBox.setCurrentIndex( self.mShapeComboBox.findText( QString( "Ellipse" ) ) )
            self.mCornerRadiusSpinBox.setEnabled( False )
        elif ( self.mComposerShape.shapeType() == QgsComposerShape.Rectangle ):
            self.mShapeComboBox.setCurrentIndex( self.mShapeComboBox.findText( QString( "Rectangle" ) ) )
            self.mCornerRadiusSpinBox.setEnabled( True )
        elif ( self.mComposerShape.shapeType() == QgsComposerShape.Triangle ):
            self.mShapeComboBox.setCurrentIndex( self.mShapeComboBox.findText( QString( "Triangle" ) ) )
            self.mCornerRadiusSpinBox.setEnabled( False )
        
        self.blockAllSignals( False )

    def on_mShapeStyleButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        if ( not self.mComposerShape ):
            return

        # use the atlas coverage layer, if any
        coverageLayer = self.atlasCoverageLayer()

        newSymbol = self.mComposerShape.shapeStyleSymbol().clone()
        d = QgsSymbolV2SelectorDialog( newSymbol, QgsStyleV2.defaultStyle(), coverageLayer, self)
        d.setExpressionContext( self.mComposerShape.createExpressionContext() )

        if ( d.exec_() == QDialog.Accepted ):

            self.mComposerShape.beginCommand( QString( "Shape style changed" ) )
            self.mComposerShape.setShapeStyleSymbol( newSymbol )
            self.updateShapeStyle()
            self.mComposerShape.endCommand()
        self.timeStart = time.time()

    def updateShapeStyle(self):
        if ( self.mComposerShape ):
            self.mComposerShape.refreshSymbol()
            icon = QgsSymbolLayerV2Utils.symbolPreviewIcon( self.mComposerShape.shapeStyleSymbol(), self.mShapeStyleButton.iconSize() )
            self.mShapeStyleButton.setIcon( icon )

    def on_mCornerRadiusSpinBox_valueChanged( self, val ):
        if ( self.mComposerShape ):
            self.mComposerShape.beginCommand( QString( "Shape radius changed" ), QgsComposerMergeCommand.ShapeCornerRadius )
            self.mComposerShape.setCornerRadius( val )
            self.mComposerShape.update()
            self.mComposerShape.endCommand()

    def on_mShapeComboBox_currentIndexChanged( self, text ):
        if ( not self.mComposerShape ):
            return

        self.mComposerShape.beginCommand( QString( "Shape type changed" ) )
        if ( text == QString( "Ellipse" ) ):
            self.mComposerShape.setShapeType( QgsComposerShape.Ellipse )
        elif ( text == QString( "Rectangle" ) ):
            self.mComposerShape.setShapeType( QgsComposerShape.Rectangle )
        elif ( text == QString( "Triangle" ) ):
            self.mComposerShape.setShapeType( QgsComposerShape.Triangle )
        self.toggleRadiusSpin( text )
        self.mComposerShape.update()
        self.mComposerShape.endCommand()

    def toggleRadiusSpin( self, shapeText ):
        if ( shapeText == QString( "Rectangle" ) ):
            self.mCornerRadiusSpinBox.setEnabled( True )
        else:
            self.mCornerRadiusSpinBox.setEnabled( False )

    def atlasComposition(self):
        if ( not self.mComposerShape ):
            return None;
        composition = self.mComposerShape.composition();

        if ( not composition ):
            return None;

        return composition.atlasComposition();
    def atlasCoverageLayer(self):
        atlasMap = self.atlasComposition();

        if ( atlasMap and atlasMap.enabled() ):
            return atlasMap.coverageLayer();

        return None;