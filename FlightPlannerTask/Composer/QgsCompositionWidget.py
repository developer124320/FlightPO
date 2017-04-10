
from PyQt4.QtGui import QWidget, QMenu, QDoubleValidator, QColorDialog,\
    QDialog, QFontDialog, QIcon, QPixmap, QAction, QComboBox, QListWidgetItem, QTextCursor
from PyQt4 import uic
from PyQt4.QtCore import SIGNAL, SLOT, QString, Qt, QStringList, QSettings
from Composer.QgsComposerItemWidget import QgsComposerItemWidget

from qgis.core import QgsComposition, QgsComposerMap, QgsComposerMergeCommand, QGis, QgsRectangle, QgsStyleV2,\
    QgsSymbolLayerV2Utils, QgsComposerMapGrid, QgsExpressionContext, QgsComposerObject, QgsProject, QgsCoordinateReferenceSystem,\
    QgsComposerMapOverview, QgsApplication, QgsExpressionContextUtils, QgsFillSymbolV2
from qgis.gui import QgsDataDefinedButton, QgsGenericProjectionSelector, QgsExpressionBuilderDialog, QgsSymbolV2SelectorDialog
import define, time
from Type.switch import switch

from Composer.ui_qgscompositionwidget import Ui_QgsCompositionWidgetBase

class QgsCompositionPaper:
    def __init__(self, name = "", width = 0.0, height = 0.0):
        self.mName = name
        self.mWidth = width
        self.mHeight = height

class QgsCompositionWidget(Ui_QgsCompositionWidgetBase):
    def __init__(self, parent, c, view):
        Ui_QgsCompositionWidgetBase.__init__(self, parent)

        # s = ["a", "b"]
        # i = s.index().__contains__("b")
        # o = s.__contains__("n")

        self.mComposition = c
        self.mPaperMap = dict()
        self.mMapItems = []
        self.timeStart = 0
        self.timeEnd = 0
        
        self.blockSignals( True )
        self.createPaperEntries()
        
        #unit
        self.mPaperUnitsComboBox.addItem( QString( "mm" ) )
        self.mPaperUnitsComboBox.addItem( QString( "inch" ) )
        
        #orientation
        self.mPaperOrientationComboBox.insertItem( 0, QString( "Landscape" ) )
        self.mPaperOrientationComboBox.insertItem( 1, QString( "Portrait" ) )
        self.mPaperOrientationComboBox.setCurrentIndex( 0 )
        
        #read with/height from composition and find suitable entries to display
        self.displayCompositionWidthHeight()
        
        self.updateVariables()
        self.connect( self.mVariableEditor, SIGNAL( "scopeChanged()" ), self.variablesChanged)
        self.connect(self.mWorldFileMapComboBox, SIGNAL("currentIndexChanged(int)"), self.on_mWorldFileMapComboBox_currentIndexChanged)
        self.connect( view, SIGNAL( "actionFinished()" ), self.mView_actionFinished)

        # listen out for variable edits
        app = QgsApplication.instance() 
        if ( app ):
            self.connect( app, SIGNAL( "settingsChanged()" ), self.updateVariables)
        self.connect( QgsProject.instance(), SIGNAL( "variablesChanged()" ), self.updateVariables)
        
        if ( self.mComposition ):
            self.mNumPagesSpinBox.setValue( self.mComposition.numPages() )
            self.connect( self.mComposition, SIGNAL( "nPagesChanged()" ), self.setNumberPages)
            
            self.updatePageStyle()
            
            #read printout resolution from composition
            self.mResolutionSpinBox.setValue( self.mComposition.printResolution() )
            
            topMargin = 0
            rightMargin = 0
            bottomMargin = 0
            leftMargin = 0
            topMargin, rightMargin, bottomMargin, leftMargin = self.mComposition.resizeToContentsMargins()
            self.mTopMarginSpinBox.setValue( topMargin )
            self.mRightMarginSpinBox.setValue( rightMargin )
            self.mBottomMarginSpinBox.setValue( bottomMargin )
            self.mLeftMarginSpinBox.setValue( leftMargin )
            
            #print as raster
            self.mPrintAsRasterCheckBox.setChecked( self.mComposition.printAsRaster() )
            
            # world file generation
            self.mGenerateWorldFileCheckBox.setChecked( self.mComposition.generateWorldFile() )
            
            # populate the map list
            self.mWorldFileMapComboBox.clear()
            availableMaps = self.mComposition.composerMapItems()
            # QList<const QgsComposerMap*>.const_iterator mapItemIt = availableMaps.constBegin()
            for mapItemIt in availableMaps:
                self.mWorldFileMapComboBox.addItem( QString( "Map %1" ).arg(( mapItemIt ).id() ), self.qVariantFromValue(mapItemIt, "Add" ) )
            
            idx = self.mWorldFileMapComboBox.findData( self.qVariantFromValue(self.mComposition.worldFileMap(), "Find" ) )
            if ( idx != -1 ):
                self.mWorldFileMapComboBox.setCurrentIndex( idx )
            
            # Connect to addition / removal of maps
            self.connect( self.mComposition, SIGNAL( "composerMapAdded( QgsComposerMap* )" ), self.onComposerMapAdded)
            self.connect( self.mComposition, SIGNAL( "itemRemoved( QgsComposerItem* )" ), self.onItemRemoved)
            
            self.mSnapToleranceSpinBox.setValue( self.mComposition.snapTolerance() )
            
            #snap grid
            self.mGridResolutionSpinBox.setValue( self.mComposition.snapGridResolution() )
            self.mOffsetXSpinBox.setValue( self.mComposition.snapGridOffsetX() )
            self.mOffsetYSpinBox.setValue( self.mComposition.snapGridOffsetY() )
            
            atlas = self.mComposition.atlasComposition()
            if ( atlas ):
                # repopulate data defined buttons if atlas layer changes
                self.connect( atlas, SIGNAL( "coverageLayerChanged( QgsVectorLayer* )" ), self.populateDataDefinedButtons) 
                self.connect( atlas, SIGNAL( "toggled( bool )" ), self.populateDataDefinedButtons)
        
        self.connect( self.mTopMarginSpinBox, SIGNAL( "valueChanged( double )" ), self.resizeMarginsChanged)
        self.connect( self.mRightMarginSpinBox, SIGNAL( "valueChanged( double )" ), self.resizeMarginsChanged)
        self.connect( self.mBottomMarginSpinBox, SIGNAL( "valueChanged( double )" ), self.resizeMarginsChanged)
        self.connect( self.mLeftMarginSpinBox, SIGNAL( "valueChanged( double )" ), self.resizeMarginsChanged)
        
        self.connect( self.mPaperSizeDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty)
        self.connect( self.mPaperSizeDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty)
        self.connect( self.mPaperSizeDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.mPaperSizeComboBox, SLOT( "setDisabled( bool )" ) )
        self.connect( self.mPaperWidthDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty)
        self.connect( self.mPaperWidthDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty)
        self.connect( self.mPaperWidthDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.mPaperWidthDoubleSpinBox, SLOT( "setDisabled( bool )" ) )
        self.connect( self.mPaperHeightDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty)
        self.connect( self.mPaperHeightDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty)
        self.connect( self.mPaperHeightDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.mPaperHeightDoubleSpinBox, SLOT( "setDisabled( bool )" ) )
        self.connect( self.mNumPagesDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty)
        self.connect( self.mNumPagesDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty)
        self.connect( self.mNumPagesDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.mNumPagesSpinBox, SLOT( "setDisabled( bool )" ) )
        self.connect( self.mPaperOrientationDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty)
        self.connect( self.mPaperOrientationDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty)
        self.connect( self.mPaperOrientationDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.mPaperOrientationComboBox, SLOT( "setDisabled( bool )" ) )
        
        #initialize data defined buttons
        self.populateDataDefinedButtons()
        
        self.blockSignals( False )
        self.addItemName = ""


    def qVariantFromValue(self, mapItem, typeStr):
        if typeStr == "Add":
            self.mMapItems.append(mapItem)
            return QString("Map " + str(len(self.mMapItems) - 1))
        else:
            try:
                idx = self.mMapItems.index(mapItem)
                return QString("Map " + str(idx))
            except:
                return QString("Map " + str(-1))
            return QString("Map " + str(-1))
    def _getExpressionContext( self, context ):
        composition = context
        if ( not composition ):
            return QgsExpressionContext()
        
        expContext = composition.createExpressionContext()
        return QgsExpressionContext( expContext )

    def populateDataDefinedButtons(self):
        if ( not self.mComposition ):
            return
        
        vl = None
        atlas = self.mComposition.atlasComposition()
        
        if ( atlas and atlas.enabled() ):
            vl = atlas.coverageLayer()
        
        for button in self.findChildren(QgsDataDefinedButton):
            button.blockSignals( True )
            # button.registerGetExpressionContextCallback( self._getExpressionContext, self.mComposition )
        
        self.mPaperSizeDDBtn.init( vl, self.mComposition.dataDefinedProperty( QgsComposerObject.PresetPaperSize ),
                         QgsDataDefinedButton.String, QgsDataDefinedButton.paperSizeDesc() )
        self.mPaperWidthDDBtn.init( vl, self.mComposition.dataDefinedProperty( QgsComposerObject.PaperWidth ),
                          QgsDataDefinedButton.Double, QgsDataDefinedButton.doublePosDesc() )
        self.mPaperHeightDDBtn.init( vl, self.mComposition.dataDefinedProperty( QgsComposerObject.PaperHeight ),
                           QgsDataDefinedButton.Double, QgsDataDefinedButton.doublePosDesc() )
        self.mNumPagesDDBtn.init( vl, self.mComposition.dataDefinedProperty( QgsComposerObject.NumPages ),
                        QgsDataDefinedButton.Int, QgsDataDefinedButton.intPosOneDesc() )
        self.mPaperOrientationDDBtn.init( vl, self.mComposition.dataDefinedProperty( QgsComposerObject.PaperOrientation ),
                                QgsDataDefinedButton.String, QgsDataDefinedButton.paperOrientationDesc() )
        
        #initial state of controls - disable related controls when dd buttons are active
        self.mPaperSizeComboBox.setEnabled( not self.mPaperSizeDDBtn.isActive() )
        
        for button in self.findChildren(QgsDataDefinedButton):
            button.blockSignals( False )

    def variablesChanged(self):
        QgsExpressionContextUtils.setCompositionVariables( self.mComposition, self.mVariableEditor.variablesInActiveScope() )

    def resizeMarginsChanged(self):
        if ( not self.mComposition ):
            return
        
        self.mComposition.setResizeToContentsMargins( self.mTopMarginSpinBox.value(),
                                                      self.mRightMarginSpinBox.value(),
                                                      self.mBottomMarginSpinBox.value(),
                                                      self.mLeftMarginSpinBox.value() )

    def updateVariables(self):
        pass
        # QgsExpressionContext context
        # context << QgsExpressionContextUtils.globalScope()
        # << QgsExpressionContextUtils.projectScope()
        # << QgsExpressionContextUtils.compositionScope( mComposition )
        # mVariableEditor.setContext( &context )
        # mVariableEditor.setEditableScopeIndex( 2 )    }

    def setDataDefinedProperty( self, ddBtn, property ):
        if ( not self.mComposition ):
            return
        
        map = ddBtn.definedProperty()
        self.mComposition.setDataDefinedProperty( property, map.value( "active" ).toInt(), map.value( "useexpr" ).toInt(), map.value( "expression" ), map.value( "field" ) )

    def ddPropertyForWidget( self, widget ):
        if ( widget == self.mPaperSizeDDBtn ):
            return QgsComposerObject.PresetPaperSize
        elif ( widget == self.mPaperWidthDDBtn ):
            return QgsComposerObject.PaperWidth
        elif ( widget == self.mPaperHeightDDBtn ):
            return QgsComposerObject.PaperHeight
        elif ( widget == self.mNumPagesDDBtn ):
            return QgsComposerObject.NumPages
        elif ( widget == self.mPaperOrientationDDBtn ):
            return QgsComposerObject.PaperOrientation
        
        return QgsComposerObject.NoProperty

    def updateDataDefinedProperty(self):
        ddButton = self.sender() 
        if ( not ddButton or not self.mComposition ):
            return
        
        property = self.ddPropertyForWidget( ddButton )
        if ( property == QgsComposerObject.NoProperty ):
            return
        
        self.setDataDefinedProperty( ddButton, property )
        self.mComposition.refreshDataDefinedProperty( property )

    def createPaperEntries(self):
        # QList<QgsCompositionPaper> formats
        
        formats = [QgsCompositionPaper( QString( "A5 (148x210 mm)" ), 148, 210 ),
                    QgsCompositionPaper( QString( "A4 (210x297 mm)" ), 210, 297 ),
                    QgsCompositionPaper( QString( "A3 (297x420 mm)" ), 297, 420 ),
                    QgsCompositionPaper( QString( "A2 (420x594 mm)" ), 420, 594 ),
                    QgsCompositionPaper( QString( "A1 (594x841 mm)" ), 594, 841 ),
                    QgsCompositionPaper( QString( "A0 (841x1189 mm)" ), 841, 1189 ),
                    QgsCompositionPaper( QString( "B5 (176 x 250 mm)" ), 176, 250 ),
                    QgsCompositionPaper( QString( "B4 (250 x 353 mm)" ), 250, 353 ),
                    QgsCompositionPaper( QString( "B3 (353 x 500 mm)" ), 353, 500 ),
                    QgsCompositionPaper( QString( "B2 (500 x 707 mm)" ), 500, 707 ),
                    QgsCompositionPaper( QString( "B1 (707 x 1000 mm)" ), 707, 1000 ),
                    QgsCompositionPaper( QString( "B0 (1000 x 1414 mm)" ), 1000, 1414 ),
                    # North american formats
                    QgsCompositionPaper( QString( "Legal (8.5x14 in)" ), 215.9, 355.6 ),
                    QgsCompositionPaper( QString( "ANSI A (Letter 8.5x11 in)" ), 215.9, 279.4 ),
                    QgsCompositionPaper( QString( "ANSI B (Tabloid 11x17 in)" ), 279.4, 431.8 ),
                    QgsCompositionPaper( QString( "ANSI C (17x22 in)" ), 431.8, 558.8 ),
                    QgsCompositionPaper( QString( "ANSI D (22x34 in)" ), 558.8, 863.6 ),
                    QgsCompositionPaper( QString( "ANSI E (34x44 in)" ), 863.6, 1117.6 ),
                    QgsCompositionPaper( QString( "Arch A (9x12 in)" ), 228.6, 304.8 ),
                    QgsCompositionPaper( QString( "Arch B (12x18 in)" ), 304.8, 457.2 ),
                    QgsCompositionPaper( QString( "Arch C (18x24 in)" ), 457.2, 609.6 ),
                    QgsCompositionPaper( QString( "Arch D (24x36 in)" ), 609.6, 914.4 ),
                    QgsCompositionPaper( QString( "Arch E (36x48 in)" ), 914.4, 1219.2 ),
                    QgsCompositionPaper( QString( "Arch E1 (30x42 in)" ), 762, 1066.8 )]
        
        self.mPaperSizeComboBox.addItem( QString( "Custom" ) )
        
        for it in formats:
            self.mPaperSizeComboBox.addItem( it.mName )
            self.mPaperMap.__setitem__( it.mName, it )

    def on_mPaperSizeComboBox_currentIndexChanged( self, text ):
        # Q_UNUSED( text )

        if ( self.mPaperSizeComboBox.currentText() == QString( "Custom" ) ):
            self.mPaperWidthDoubleSpinBox.setEnabled( True )
            self.mPaperHeightDoubleSpinBox.setEnabled( True )
            self.mPaperUnitsComboBox.setEnabled( True )
        else:
            self.mPaperWidthDoubleSpinBox.setEnabled( False )
            self.mPaperHeightDoubleSpinBox.setEnabled( False )
            self.mPaperUnitsComboBox.setEnabled( False )
        self.applyCurrentPaperSettings()

    def on_mPaperOrientationComboBox_currentIndexChanged( self, text ):
        # Q_UNUSED( text )

        if ( self.mPaperSizeComboBox.currentText() == QString( "Custom" ) ):
            self.adjustOrientation()
            self.applyWidthHeight()
        else:
            self.adjustOrientation()
            self.applyCurrentPaperSettings()

    def on_mPaperUnitsComboBox_currentIndexChanged( self, text ):
        # Q_UNUSED( text )
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        width = self.size( self.mPaperWidthDoubleSpinBox )
        height = self.size( self.mPaperHeightDoubleSpinBox )

        if ( self.mPaperUnitsComboBox.currentIndex() == 0 ):
            # mm, value was inch
            width *= 25.4
            height *= 25.4
        else:
            # inch, values was mm,
            width /= 25.4
            height /= 25.4

        self.setSize( self.mPaperWidthDoubleSpinBox, width )
        self.setSize( self.mPaperHeightDoubleSpinBox, height )

        if ( self.mPaperSizeComboBox.currentText() == QString( "Custom" ) ):
            self.adjustOrientation()
            self.applyWidthHeight()
        else:
            self.adjustOrientation()
            self.applyCurrentPaperSettings()
        self.timeStart = time.time()

    def adjustOrientation(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        width = self.size( self.mPaperWidthDoubleSpinBox )
        height = self.size( self.mPaperHeightDoubleSpinBox )

        if ( width < 0 or height < 0 ):
            return

        if ( height > width ): #change values such that width > height
            tmp = width
            width = height
            height = tmp

        lineEditsEnabled = self.mPaperWidthDoubleSpinBox.isEnabled()

        self.mPaperWidthDoubleSpinBox.setEnabled( True )
        self.mPaperHeightDoubleSpinBox.setEnabled( True )
        if ( self.mPaperOrientationComboBox.currentText() == QString( "Landscape" ) ):
            self.setSize( self.mPaperWidthDoubleSpinBox, width )
            self.setSize( self.mPaperHeightDoubleSpinBox, height )
        else:
            self.setSize( self.mPaperWidthDoubleSpinBox, height )
            self.setSize( self.mPaperHeightDoubleSpinBox, width )

        self.mPaperWidthDoubleSpinBox.setEnabled( lineEditsEnabled )
        self.mPaperHeightDoubleSpinBox.setEnabled( lineEditsEnabled )

        self.emit(SIGNAL("pageOrientationChanged"), self.mPaperOrientationComboBox.currentText() )
        self.timeStart = time.time()
    def setSize( self, spin, v ):
        # if self.timeStart != 0:
        #     self.timeEnd = time.time()
        #     print self.timeEnd
        #     if self.timeEnd - self.timeStart <= 2:
        #         self.timeStart = 0
        #         return
        if ( self.mPaperUnitsComboBox.currentIndex() == 0 ):
            # mm
            spin.setValue( v )
        else:
            # inch (show width in inch)
            spin.setValue( v / 25.4 )
        # self.timeStart = time.time()

    def size( self, spin ):
        # if self.timeStart != 0:
        #     self.timeEnd = time.time()
        #     print self.timeEnd
        #     if self.timeEnd - self.timeStart <= 2:
        #         self.timeStart = 0
        #         return
        size = spin.value()

        if ( self.mPaperUnitsComboBox.currentIndex() == 0 ):
            # mm
            return size
        else:
            # inch return in mm
            return size * 25.4
        # self.timeStart = time.time()

    def applyCurrentPaperSettings(self):
        if ( self.mComposition ):
            #find entry in mPaper map to set width and height
            it = self.mPaperMap.get( self.mPaperSizeComboBox.currentText() )
            if it == None:
                return
            i = 0
            test = None
            for item in self.mPaperMap.itervalues():
                if i == self.mPaperMap.__len__() - 1:
                    test = item
                    break
                i += 1

            if ( it == test):
                return

            self.mPaperWidthDoubleSpinBox.setEnabled( True )
            self.mPaperHeightDoubleSpinBox.setEnabled( True )
            self.setSize( self.mPaperWidthDoubleSpinBox, it.mWidth )
            self.setSize( self.mPaperHeightDoubleSpinBox, it.mHeight )
            self.mPaperWidthDoubleSpinBox.setEnabled( False )
            self.mPaperHeightDoubleSpinBox.setEnabled( False )

            self.adjustOrientation()
            self.applyWidthHeight()

    def applyWidthHeight(self):
        width = self.size( self.mPaperWidthDoubleSpinBox )
        height = self.size( self.mPaperHeightDoubleSpinBox )

        if ( width < 0 or height < 0 ):
            return

        self.mComposition.setPaperSize( width, height )

    def on_mPaperWidthDoubleSpinBox_editingFinished(self):
        self.applyWidthHeight()

    def on_mPaperHeightDoubleSpinBox_editingFinished(self):
        self.applyWidthHeight()

    def on_mNumPagesSpinBox_valueChanged( self, value ):
        if ( not self.mComposition ):
            return
        self.mComposition.setNumPages( self.mNumPagesSpinBox.value() )

    def displayCompositionWidthHeight(self):
        if ( not self.mComposition ):
            return

        paperWidth = self.mComposition.paperWidth()
        self.setSize( self.mPaperWidthDoubleSpinBox, paperWidth )

        paperHeight = self.mComposition.paperHeight()
        self.setSize( self.mPaperHeightDoubleSpinBox, paperHeight )

        #set orientation
        self.mPaperOrientationComboBox.blockSignals( True )
        if ( paperWidth > paperHeight ):
            self.mPaperOrientationComboBox.setCurrentIndex( self.mPaperOrientationComboBox.findText( QString( "Landscape" ) ) )
        else:
            self.mPaperOrientationComboBox.setCurrentIndex( self.mPaperOrientationComboBox.findText( QString( "Portrait" ) ) )
        self.mPaperOrientationComboBox.blockSignals( False )

        #set paper name
        found = False
        # paper_it = self.mPaperMap.constBegin()
        for paper_it in self.mPaperMap.itervalues():
            currentPaper = paper_it

            #consider width and height values may be exchanged
            if (( self.qgsDoubleNear( currentPaper.mWidth, paperWidth ) and self.qgsDoubleNear( currentPaper.mHeight, paperHeight ) )
                        or ( self.qgsDoubleNear( currentPaper.mWidth, paperHeight ) and self.qgsDoubleNear( currentPaper.mHeight, paperWidth ) ) ):
                self.mPaperSizeComboBox.setCurrentIndex( self.mPaperSizeComboBox.findText( paper_it.mName ) )
                found = True
                break

        if ( not found ):
            #custom
            self.mPaperSizeComboBox.setCurrentIndex( 0 )
        else:
            self.mPaperWidthDoubleSpinBox.setEnabled( False )
            self.mPaperHeightDoubleSpinBox.setEnabled( False )
            self.mPaperUnitsComboBox.setEnabled( False )
    def qgsDoubleNear(self, d1, d2):
        if round(d1, 1) == round(d2, 1):
            return True
        return False
    def on_mPageStyleButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        if ( not self.mComposition ):
            return

        coverageLayer = None
        # use the atlas coverage layer, if any
        if ( self.mComposition.atlasComposition().enabled() ):
            coverageLayer = self.mComposition.atlasComposition().coverageLayer()

        newSymbol = self.mComposition.pageStyleSymbol().clone()
        if ( not newSymbol ):
            newSymbol = QgsFillSymbolV2()
        d = QgsSymbolV2SelectorDialog( newSymbol, QgsStyleV2.defaultStyle(), coverageLayer, self)
        d.setExpressionContext( self.mComposition.createExpressionContext() )

        if ( d.exec_() == QDialog.Accepted ):

            self.mComposition.setPageStyleSymbol( newSymbol )
            self.updatePageStyle()
        self.timeStart = time.time()
        # delete newSymbol
    # def displayCompositionWidthHeight(self):
    #     if ( not self.mComposition ):
    #         return;
    #     }
    #
    #     double paperWidth = mComposition.paperWidth();
    #     setSize( mPaperWidthDoubleSpinBox, paperWidth );
    #
    #     double paperHeight = mComposition.paperHeight();
    #     setSize( mPaperHeightDoubleSpinBox, paperHeight );
    #
    #     #set orientation
    #     mPaperOrientationComboBox.blockSignals( true );
    #     if ( paperWidth > paperHeight )
    #     {
    #         mPaperOrientationComboBox.setCurrentIndex( mPaperOrientationComboBox.findText( tr( "Landscape" ) ) );
    #     }
    #     else
    #     {
    #         mPaperOrientationComboBox.setCurrentIndex( mPaperOrientationComboBox.findText( tr( "Portrait" ) ) );
    #     }
    #     mPaperOrientationComboBox.blockSignals( false );
    #
    #     #set paper name
    #     bool found = false;
    #     QMap<QString, QgsCompositionPaper>.const_iterator paper_it = mPaperMap.constBegin();
    #     for ( ; paper_it != mPaperMap.constEnd(); ++paper_it )
    #     {
    #         QgsCompositionPaper currentPaper = paper_it.value();
    #
    #         #consider width and height values may be exchanged
    #         if (( qgsDoubleNear( currentPaper.mWidth, paperWidth ) && qgsDoubleNear( currentPaper.mHeight, paperHeight ) )
    #         || ( qgsDoubleNear( currentPaper.mWidth, paperHeight ) && qgsDoubleNear( currentPaper.mHeight, paperWidth ) ) )
    #         {
    #             mPaperSizeComboBox.setCurrentIndex( mPaperSizeComboBox.findText( paper_it.key() ) );
    #             found = true;
    #             break;
    #         }
    #     }
    #
    #     if ( !found )
    #     {
    #         #custom
    #         mPaperSizeComboBox.setCurrentIndex( 0 );
    #     }
    #     else
    #     {
    #         mPaperWidthDoubleSpinBox.setEnabled( false );
    #         mPaperHeightDoubleSpinBox.setEnabled( false );
    #         mPaperUnitsComboBox.setEnabled( false );
    #     }
    def on_mResizePageButton_clicked(self):
        if ( not self.mComposition ):
            return

        self.mComposition.resizePageToContents( self.mTopMarginSpinBox.value(),
                                                  self.mRightMarginSpinBox.value(),
                                                  self.mBottomMarginSpinBox.value(),
                                                  self.mLeftMarginSpinBox.value() )

    def updatePageStyle(self):
        if ( self.mComposition ):
            icon = QgsSymbolLayerV2Utils.symbolPreviewIcon( self.mComposition.pageStyleSymbol(), self.mPageStyleButton.iconSize() )
            self.mPageStyleButton.setIcon( icon )

    def setPrintAsRasterCheckBox( self, state ):
        self.mPrintAsRasterCheckBox.blockSignals( True )
        self.mPrintAsRasterCheckBox.setChecked( state )
        self.mPrintAsRasterCheckBox.blockSignals( False )

    def setNumberPages(self):
        if ( not self.mComposition ):
            return

        self.mNumPagesSpinBox.blockSignals( True )
        self.mNumPagesSpinBox.setValue( self.mComposition.numPages() )
        self.mNumPagesSpinBox.blockSignals( False )

    def displaySnapingSettings(self):
        if ( not self.mComposition ):
            return

        self.mGridResolutionSpinBox.setValue( self.mComposition.snapGridResolution() )
        self.mOffsetXSpinBox.setValue( self.mComposition.snapGridOffsetX() )
        self.mOffsetYSpinBox.setValue( self.mComposition.snapGridOffsetY() )

    def on_mResolutionSpinBox_valueChanged( self, value ):
        self.mComposition.setPrintResolution( self.mResolutionSpinBox.value() )

    def on_mPrintAsRasterCheckBox_toggled( self, state ):
        if ( not self.mComposition ):
            return

        self.mComposition.setPrintAsRaster( state )

    def on_mGenerateWorldFileCheckBox_toggled( self, state ):
        if ( not self.mComposition ):
            return

        self.mComposition.setGenerateWorldFile( state )
        self.mWorldFileMapComboBox.setEnabled( state )

    def mView_actionFinished(self):
        if len(self.mComposition.selectedComposerItems()) == 0:
                return
        item = self.mComposition.selectedComposerItems()[0]
        if self.addItemName == "Map":
            self.mWorldFileMapComboBox.addItem( QString( "Map %1" ).arg( item.id() ), self.qVariantFromValue(item, "Add" ) )
            if ( self.mWorldFileMapComboBox.count() == 1 ):
                self.mComposition.setWorldFileMap( item )
        self.addItemName = ""

    def onComposerMapAdded( self, map ):
        if ( not self.mComposition ):
            return
        self.addItemName = "Map"



    def onItemRemoved( self, item ):
        if ( not self.mComposition ):
            return

        item._class_ = QgsComposerMap
        map = item
        if ( isinstance(map, QgsComposerMap) ):
            idx = self.mWorldFileMapComboBox.findData( self.qVariantFromValue(map, "Find" ) )
            if ( idx != -1 ):
                self.mWorldFileMapComboBox.removeItem( idx )
        if ( self.mWorldFileMapComboBox.count() == 0 ):
            self.mComposition.setWorldFileMap( None)

    def on_mWorldFileMapComboBox_currentIndexChanged( self, index ):
        if ( not self.mComposition ):
            return
        if ( index == -1 ):
            self.mComposition.setWorldFileMap( None)
        else:
            # map = self.mWorldFileMapComboBox.itemData( index ).value()
            map = self.mMapItems[self.mWorldFileMapComboBox.currentIndex()]
            self.mComposition.setWorldFileMap( map )

    def on_mGridResolutionSpinBox_valueChanged( self, d ):
        if ( self.mComposition ):
            self.mComposition.setSnapGridResolution( self.mGridResolutionSpinBox.value() )

    def on_mOffsetXSpinBox_valueChanged( self, d ):
        if ( self.mComposition ):
            self.mComposition.setSnapGridOffsetX( self.mOffsetXSpinBox.value() )

    def on_mOffsetYSpinBox_valueChanged( self, d ):
        if ( self.mComposition ):
            self.mComposition.setSnapGridOffsetY( self.mOffsetYSpinBox.value() )

    def on_mSnapToleranceSpinBox_valueChanged( self, tolerance ):
        if ( self.mComposition ):
            self.mComposition.setSnapTolerance( self.mSnapToleranceSpinBox.value() )

    def blockSignals( self, block ):
        self.mPaperSizeComboBox.blockSignals( block )
        self.mPaperUnitsComboBox.blockSignals( block )
        self.mPaperWidthDoubleSpinBox.blockSignals( block )
        self.mPaperHeightDoubleSpinBox.blockSignals( block )
        self.mNumPagesSpinBox.blockSignals( block )
        self.mPaperOrientationComboBox.blockSignals( block )
        self.mPageStyleButton.blockSignals( block )
        self.mResolutionSpinBox.blockSignals( block )
        self.mPrintAsRasterCheckBox.blockSignals( block )
        self.mGridResolutionSpinBox.blockSignals( block )
        self.mOffsetXSpinBox.blockSignals( block )
        self.mOffsetYSpinBox.blockSignals( block )
        self.mSnapToleranceSpinBox.blockSignals( block )

