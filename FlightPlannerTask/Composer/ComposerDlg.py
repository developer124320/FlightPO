

from qgis.core import *
from qgis.gui import *
from PyQt4 import QtGui, uic
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from PyQt4.QtXml import *
from PyQt4.QtGui import QToolButton
from PyQt4.QtCore import *
from PyQt4.QtGui import QMessageBox, QFileDialog
from FlightPlanner.types import QgsComposerOutputMode
from Composer.QgsAtlasCompositionWidget import QgsAtlasCompositionWidget
from Composer.Qgscomposerimageexportoptions import QgsComposerImageExportOptionsDialog
from Composer.Qgssvgexportoptions import QgsSvgExportOptionsDialog
from Composer.QgsCompositionWidget import QgsCompositionWidget
from FlightPlanner.Panels.GroupBox import GroupBox
from map.myLayerTreeView import MyLayerTreeView
from Composer.QgsComposerLabelWidget import QgsComposerLabelWidget
from Composer.QgsComposerMapWidget import QgsComposerMapWidget
from Composer.QgsComposerArrowWidget import QgsComposerArrowWidget
from Composer.QgsComposerShapeWidget import QgsComposerShapeWidget
from Composer.ui_qgscomposer import Ui_QgsComposer
from Composer.tableEditWidget import TableEditWidget
import define, os, time

print "FORM_CLASS"
# print os.path.join(os.path.dirname(__file__), 'grid_zone_generator_dialog_base.ui')
# FORM_CLASS, _ = uic.loadUiType(define.appPath + "/UI/Composer/qgscomposerbase.ui")

class ComposerDlg(Ui_QgsComposer):
    def __init__(self, parent, comp, model, data, newFlag = True):
        """Constructor."""
        Ui_QgsComposer.__init__(self, parent)
        # self.setupUi(self)

        self.setWindowTitle("Print Dialog")
        self.mTitle = "Print Dialog"
        self.currentDir = os.getcwdu()
        self.setupTheme()
        self.mItemWidgetMap = dict()
        self.mPanelStatus = dict()
        self.mPrinter = None
        self.mSetPageOrientation = False
        self.parentDlg = parent
        self.data = data
        self.gpw = None
        self.mTblView = None
        self.mStdModel = None
        self.timeStart = 0
        self.timeEnd = 0
        self.newFlag = newFlag
        if self.newFlag:
            self.gpw = self.parentDlg.gpw
            self.mTblView = self.parentDlg.tblView
        
        orderingToolButton = QtGui.QToolButton( self )
        orderingToolButton.setPopupMode( QtGui.QToolButton.InstantPopup )
        orderingToolButton.setAutoRaise( True )
        orderingToolButton.setToolButtonStyle( Qt.ToolButtonIconOnly )
        orderingToolButton.addAction( self.mActionRaiseItems )
        orderingToolButton.addAction( self.mActionLowerItems )
        orderingToolButton.addAction( self.mActionMoveItemsToTop )
        orderingToolButton.addAction( self.mActionMoveItemsToBottom )
        orderingToolButton.setDefaultAction( self.mActionRaiseItems )
        self.mItemActionToolbar.addWidget( orderingToolButton )
        
        alignToolButton = QtGui.QToolButton( self )
        alignToolButton.setPopupMode( QtGui.QToolButton.InstantPopup )
        alignToolButton.setAutoRaise( True )
        alignToolButton.setToolButtonStyle( Qt.ToolButtonIconOnly )
        
        alignToolButton.addAction( self.mActionAlignLeft )
        alignToolButton.addAction( self.mActionAlignHCenter )
        alignToolButton.addAction( self.mActionAlignRight )
        alignToolButton.addAction( self.mActionAlignTop )
        alignToolButton.addAction( self.mActionAlignVCenter )
        alignToolButton.addAction( self.mActionAlignBottom )
        alignToolButton.setDefaultAction( self.mActionAlignLeft )
        self.mItemActionToolbar.addWidget( alignToolButton )
        
        shapeToolButton = QtGui.QToolButton( self.mItemToolbar )
        shapeToolButton.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAddBasicShape.svg" ) )
        shapeToolButton.setCheckable( True )
        shapeToolButton.setPopupMode( QtGui.QToolButton.InstantPopup )
        shapeToolButton.setAutoRaise( True )
        shapeToolButton.setToolButtonStyle( Qt.ToolButtonIconOnly )
        shapeToolButton.addAction( self.mActionAddRectangle )
        shapeToolButton.addAction( self.mActionAddTriangle )
        shapeToolButton.addAction( self.mActionAddEllipse )
        shapeToolButton.setToolTip( "Add Shape" )
        self.mItemToolbar.insertWidget( self.mActionAddArrow, shapeToolButton )
        
        toggleActionGroup = QtGui.QActionGroup( self )
        toggleActionGroup.addAction( self.mActionMoveItemContent )
        toggleActionGroup.addAction( self.mActionPan )
        toggleActionGroup.addAction( self.mActionMouseZoom )
        toggleActionGroup.addAction( self.mActionAddNewMap )
        toggleActionGroup.addAction( self.mActionAddNewLabel )
        toggleActionGroup.addAction( self.mActionAddNewLegend )
        toggleActionGroup.addAction( self.mActionAddNewScalebar )
        toggleActionGroup.addAction( self.mActionAddImage )
        toggleActionGroup.addAction( self.mActionSelectMoveItem )
        toggleActionGroup.addAction( self.mActionAddRectangle )
        toggleActionGroup.addAction( self.mActionAddTriangle )
        toggleActionGroup.addAction( self.mActionAddEllipse )
        toggleActionGroup.addAction( self.mActionAddArrow )
        # //toggleActionGroup.addAction( self.mActionAddTable )
        toggleActionGroup.addAction( self.mActionAddAttributeTable )
        toggleActionGroup.addAction( self.mActionAddHtml )
        toggleActionGroup.setExclusive( True )
        
        self.mActionAddNewMap.setCheckable( True )
        self.mActionAddNewLabel.setCheckable( True )
        self.mActionAddNewLegend.setCheckable( True )
        self.mActionSelectMoveItem.setCheckable( True )
        self.mActionAddNewScalebar.setCheckable( True )
        self.mActionAddImage.setCheckable( True )
        self.mActionMoveItemContent.setCheckable( True )
        self.mActionPan.setCheckable( True )
        self.mActionMouseZoom.setCheckable( True )
        self.mActionAddArrow.setCheckable( True )
        self.mActionAddHtml.setCheckable( True )
        
        self.mActionShowGrid.setCheckable( True )
        self.mActionSnapGrid.setCheckable( True )
        self.mActionShowGuides.setCheckable( True )
        self.mActionSnapGuides.setCheckable( True )
        self.mActionSmartGuides.setCheckable( True )
        self.mActionShowRulers.setCheckable( True )
        self.mActionShowBoxes.setCheckable( True )
        
        self.mActionAtlasPreview.setCheckable( True )

        composerMenu = self.menuBar().addMenu( "&Composer" )
        # composerMenu.addAction( self.mActionSaveProject )
        # composerMenu.addAction( self.mActionOpenProject )
        # composerMenu.addAction( self.mActionLoadFromTemplate )
        composerMenu.addAction( self.mActionSaveAsTemplate )
        composerMenu.addSeparator()
        # composerMenu.addAction( self.mActionNewComposer )
        # composerMenu.addAction( self.mActionDuplicateComposer )
        # composerMenu.addAction( self.mActionComposerManager )

        # self.mPrintComposersMenu = QtGui.QMenu( "Print &Composers" , self )
        # self.mPrintComposersMenu.setObjectName( "mPrintComposersMenu" )
        # self.connect( self.mPrintComposersMenu, SIGNAL( "aboutToShow()" ), self.populatePrintComposersMenu )
        # composerMenu.addMenu( self.mPrintComposersMenu )

        # composerMenu.addSeparator()
        # composerMenu.addAction( self.mActionLoadFromTemplate )
        # composerMenu.addAction( self.mActionSaveAsTemplate )
        composerMenu.addSeparator()
        composerMenu.addAction( self.mActionExportAsImage )
        composerMenu.addAction( self.mActionExportAsPDF )
        # composerMenu.addAction( self.mActionExportAsSVG )
        composerMenu.addSeparator()
        # composerMenu.addAction( self.mActionPageSetup )
        composerMenu.addAction( self.mActionPrint )
        composerMenu.addSeparator()
        composerMenu.addAction( self.mActionQuit )
        self.connect( self.mActionQuit, SIGNAL( "triggered()" ), self, SLOT("close()"))

        # //cut/copy/paste actions. Note these are not included in the ui file
        # //as ui files have no support for QKeySequence shortcuts
        self.mActionCut = QtGui.QAction( "Cu&t", self )
        self.mActionCut.setShortcuts( QtGui.QKeySequence.Cut )
        self.mActionCut.setStatusTip( "Cut")
        self.mActionCut.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionEditCut.png" ) )
        self.connect( self.mActionCut, SIGNAL( "triggered()" ), self.actionCutTriggered)

        self.mActionCopy = QtGui.QAction( "&Copy" , self )
        self.mActionCopy.setShortcuts( QtGui.QKeySequence.Copy )
        self.mActionCopy.setStatusTip( "Copy" )
        self.mActionCopy.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionEditCopy.png" ) )
        self.connect( self.mActionCopy, SIGNAL( "triggered()" ), self.actionCopyTriggered )

        self.mActionPaste = QtGui.QAction( "&Paste" , self )
        self.mActionPaste.setShortcuts( QtGui.QKeySequence.Paste )
        self.mActionPaste.setStatusTip( "Paste"  )
        self.mActionPaste.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionEditPaste.png" ) )
        self.connect( self.mActionPaste, SIGNAL( "triggered()" ), self.actionPasteTriggered )

        editMenu = self.menuBar().addMenu( "&Edit" )
        editMenu.addAction( self.mActionUndo )
        editMenu.addAction( self.mActionRedo )
        editMenu.addSeparator()

        # //Backspace should also trigger delete selection
        backSpace = QtGui.QShortcut( QtGui.QKeySequence( "Backspace" ), self )
        self.connect( backSpace, SIGNAL( "activated()" ), self.mActionDeleteSelection, SLOT( "trigger()" ) )
        editMenu.addAction( self.mActionDeleteSelection )
        editMenu.addSeparator()

        editMenu.addAction( self.mActionCut )
        editMenu.addAction( self.mActionCopy )
        editMenu.addAction( self.mActionPaste )
        # //TODO : "Ctrl+Shift+V" is one way to paste in place, but on some platforms you can use Shift+Ins and F18
        editMenu.addAction( self.mActionPasteInPlace )
        editMenu.addSeparator()
        editMenu.addAction( self.mActionSelectAll )
        editMenu.addAction( self.mActionDeselectAll )
        editMenu.addAction( self.mActionInvertSelection )
        editMenu.addAction( self.mActionSelectNextBelow )
        editMenu.addAction( self.mActionSelectNextAbove )

        self.mActionPreviewModeOff = QtGui.QAction( "&Normal", self )
        self.mActionPreviewModeOff.setStatusTip( "Normal" )
        self.mActionPreviewModeOff.setCheckable( True )
        self.mActionPreviewModeOff.setChecked( True )
        self.connect( self.mActionPreviewModeOff, SIGNAL( "triggered()" ), self.disablePreviewMode) 
        self.mActionPreviewModeGrayscale = QtGui.QAction( "Simulate Photocopy (&Grayscale)" , self )
        self.mActionPreviewModeGrayscale.setStatusTip( "Simulate photocopy (grayscale)"  )
        self.mActionPreviewModeGrayscale.setCheckable( True )
        self.connect( self.mActionPreviewModeGrayscale, SIGNAL( "triggered()" ), self.activateGrayscalePreview )
        self.mActionPreviewModeMono = QtGui.QAction( "Simulate Fax (&Mono)" , self )
        self.mActionPreviewModeMono.setStatusTip( "Simulate fax (mono)" )
        self.mActionPreviewModeMono.setCheckable( True )
        self.connect( self.mActionPreviewModeMono, SIGNAL( "triggered()" ), self.activateMonoPreview)
        self.mActionPreviewProtanope = QtGui.QAction( "Simulate Color Blindness (&Protanope)" , self )
        self.mActionPreviewProtanope.setStatusTip( "Simulate color blindness (Protanope)" )
        self.mActionPreviewProtanope.setCheckable( True )
        self.connect( self.mActionPreviewProtanope, SIGNAL( "triggered()" ), self.activateProtanopePreview)
        self.mActionPreviewDeuteranope = QtGui.QAction( "Simulate Color Blindness (&Deuteranope)" , self )
        self.mActionPreviewDeuteranope.setStatusTip( "Simulate color blindness (Deuteranope)" )
        self.mActionPreviewDeuteranope.setCheckable( True )
        self.connect( self.mActionPreviewDeuteranope, SIGNAL( "triggered()" ), self.activateDeuteranopePreview)

        self.mPreviewGroup = QtGui.QActionGroup( self )
        self.mPreviewGroup.setExclusive( True )
        self.mActionPreviewModeOff.setActionGroup( self.mPreviewGroup )
        self.mActionPreviewModeGrayscale.setActionGroup( self.mPreviewGroup )
        self.mActionPreviewModeMono.setActionGroup( self.mPreviewGroup )
        self.mActionPreviewProtanope.setActionGroup( self.mPreviewGroup )
        self.mActionPreviewDeuteranope.setActionGroup( self.mPreviewGroup )

        viewMenu = self.menuBar().addMenu( "&View" )
        # //Ctrl+= should also trigger zoom in
        ctrlEquals = QtGui.QShortcut( QtGui.QKeySequence( "Ctrl+=" ), self )
        self.connect( ctrlEquals, SIGNAL( "activated()" ), self.mActionZoomIn, SLOT( "trigger()" ) )
        
        viewMenu.addSeparator()
        viewMenu.addAction( self.mActionZoomIn )
        viewMenu.addAction( self.mActionZoomOut )
        viewMenu.addAction( self.mActionZoomAll )
        viewMenu.addAction( self.mActionZoomActual )
        viewMenu.addSeparator()
        viewMenu.addAction( self.mActionRefreshView )
        # viewMenu.addSeparator()
        # viewMenu.addAction( self.mActionShowGrid )
        # viewMenu.addAction( self.mActionSnapGrid )
        # viewMenu.addSeparator()
        # viewMenu.addAction( self.mActionShowGuides )
        # viewMenu.addAction( self.mActionSnapGuides )
        # viewMenu.addAction( self.mActionSmartGuides )
        # viewMenu.addAction( self.mActionClearGuides )
        viewMenu.addSeparator()
        # viewMenu.addAction( self.mActionShowBoxes )
        viewMenu.addAction( self.mActionShowRulers )
        viewMenu.addAction( self.mActionShowPage )
        
        # // Panel and toolbar submenus
        self.mPanelMenu = QtGui.QMenu( "P&anels" , self )
        self.mPanelMenu.setObjectName( "mPanelMenu" )
        self.mToolbarMenu = QtGui.QMenu(  "&Toolbars" , self )
        self.mToolbarMenu.setObjectName( "mToolbarMenu" )
        viewMenu.addSeparator()
        viewMenu.addAction( self.mActionToggleFullScreen )
        viewMenu.addAction( self.mActionHidePanels )
        viewMenu.addMenu( self.mPanelMenu )
        viewMenu.addMenu( self.mToolbarMenu )
        # // toolBar already exists, add other widgets as they are created
        self.mToolbarMenu.addAction( self.mComposerToolbar.toggleViewAction() )
        self.mToolbarMenu.addAction( self.mPaperNavToolbar.toggleViewAction() )
        # self.mToolbarMenu.addAction( self.mItemActionToolbar.toggleViewAction() )
        self.mToolbarMenu.addAction( self.mItemToolbar.toggleViewAction() )
        
        layoutMenu = self.menuBar().addMenu(  "&Layout" )
        # layoutMenu.addAction( self.mActionAddNewMap )
        layoutMenu.addAction( self.mActionAddNewLabel )
        # layoutMenu.addAction( self.mActionAddNewScalebar )
        # layoutMenu.addAction( self.mActionAddNewLegend )
        # layoutMenu.addAction( self.mActionAddImage )
        shapeMenu = layoutMenu.addMenu( "Add Shape" )
        shapeMenu.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAddBasicShape.png" ) )
        shapeMenu.addAction( self.mActionAddRectangle )
        shapeMenu.addAction( self.mActionAddTriangle )
        shapeMenu.addAction( self.mActionAddEllipse )
        layoutMenu.addAction( self.mActionAddArrow )
        # //layoutMenu.addAction( self.mActionAddTable )
        # layoutMenu.addAction( self.mActionAddAttributeTable )
        # layoutMenu.addAction( self.mActionAddHtml )
        layoutMenu.addSeparator()
        layoutMenu.addAction( self.mActionSelectMoveItem )
        # layoutMenu.addAction( self.mActionMoveItemContent )
        # layoutMenu.addSeparator()
        # layoutMenu.addAction( self.mActionGroupItems )
        # layoutMenu.addAction( self.mActionUngroupItems )
        # layoutMenu.addSeparator()
        # layoutMenu.addAction( self.mActionRaiseItems )
        # layoutMenu.addAction( self.mActionLowerItems )
        # layoutMenu.addAction( self.mActionMoveItemsToTop )
        # layoutMenu.addAction( self.mActionMoveItemsToBottom )
        # layoutMenu.addAction( self.mActionLockItems )
        # layoutMenu.addAction( self.mActionUnlockAll )
        
        # atlasMenu = self.menuBar().addMenu(  "&Atlas" )
        # atlasMenu.addAction( self.mActionAtlasPreview )
        # atlasMenu.addAction( self.mActionAtlasFirst )
        # atlasMenu.addAction( self.mActionAtlasPrev )
        # atlasMenu.addAction( self.mActionAtlasNext )
        # atlasMenu.addAction( self.mActionAtlasLast )
        # atlasMenu.addSeparator()
        # atlasMenu.addAction( self.mActionPrintAtlas )
        # atlasMenu.addAction( self.mActionExportAtlasAsImage )
        # atlasMenu.addAction( self.mActionExportAtlasAsSVG )
        # atlasMenu.addAction( self.mActionExportAtlasAsPDF )
        # atlasMenu.addSeparator()
        # atlasMenu.addAction( self.mActionAtlasSettings )

        
        atlasExportToolButton = QtGui.QToolButton( self.mAtlasToolbar )
        atlasExportToolButton.setPopupMode( QToolButton.InstantPopup )
        atlasExportToolButton.setAutoRaise( True)
        atlasExportToolButton.setToolButtonStyle( Qt.ToolButtonIconOnly )
        atlasExportToolButton.addAction( self.mActionExportAtlasAsImage )
        atlasExportToolButton.addAction( self.mActionExportAtlasAsSVG )
        atlasExportToolButton.addAction( self.mActionExportAtlasAsPDF )
        atlasExportToolButton.setDefaultAction( self.mActionExportAtlasAsImage )
        self.mAtlasToolbar.insertWidget( self.mActionAtlasSettings, atlasExportToolButton )
        self.mAtlasPageComboBox = QtGui.QComboBox()
        self.mAtlasPageComboBox.setEditable( True)
        self.mAtlasPageComboBox.addItem( QString.number( 1 ) )
        self.mAtlasPageComboBox.setCurrentIndex( 0 )
        self.mAtlasPageComboBox.setMinimumHeight( self.mAtlasToolbar.height() )
        self.mAtlasPageComboBox.setMinimumContentsLength( 6 )
        self.mAtlasPageComboBox.setMaxVisibleItems( 20 )
        self.mAtlasPageComboBox.setSizeAdjustPolicy( QtGui.QComboBox.AdjustToContents )
        self.mAtlasPageComboBox.setInsertPolicy( QtGui.QComboBox.NoInsert )
        self.connect( self.mAtlasPageComboBox.lineEdit(), SIGNAL( "editingFinished()" ), self.atlasPageComboEditingFinished)
        self.connect( self.mAtlasPageComboBox, SIGNAL( "currentIndexChanged( QString )" ), self.atlasPageComboEditingFinished)
        self.mAtlasToolbar.insertWidget( self.mActionAtlasNext, self.mAtlasPageComboBox )
        
        # settingsMenu = self.menuBar().addMenu(  "&Settings" )
        # settingsMenu.addAction( self.mActionOptions )
        
        mFirstTime = True

        # Create action to select self window
        self.mWindowAction = QtGui.QAction( self.windowTitle(), self )
        self.connect( self.mWindowAction, SIGNAL( "triggered()" ), self.activate)
        
        # QgsDebugMsg( "entered." )
        
        self.setMouseTracking( True )
        self.mViewFrame.setMouseTracking( True )
        
        self.mStatusZoomCombo = QtGui.QComboBox( self.mStatusBar )
        self.mStatusZoomCombo.setEditable( True )
        self.mStatusZoomCombo.setInsertPolicy( QtGui.QComboBox.NoInsert )
        self.mStatusZoomCombo.setCompleter( None )
        self.mStatusZoomCombo.setMinimumWidth( 100 )
        #zoom combo box accepts decimals in the range 1-9999, with an optional decimal point and "%" sign
        zoomRx = QRegExp( "\\s*\\d{1,4}(\\.\\d?)?\\s*%?" )
        zoomValidator = QtGui.QRegExpValidator( zoomRx, self.mStatusZoomCombo )
        self.mStatusZoomCombo.lineEdit().setValidator( zoomValidator )
        
        #add some nice zoom levels to the zoom combobox
        self.mStatusZoomLevelsList = [0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
        # QList<double>.iterator zoom_it
        for zoom_it in self.mStatusZoomLevelsList:
            self.mStatusZoomCombo.insertItem( 0, QString("%1%").arg( zoom_it * 100.0, 0, 'f', 1 ) )
        self.connect( self.mStatusZoomCombo, SIGNAL( "currentIndexChanged( int )" ), self.statusZoomCombo_currentIndexChanged)
        self.connect( self.mStatusZoomCombo.lineEdit(), SIGNAL( "returnPressed()" ), self.statusZoomCombo_zoomEntered)
        
        #create status bar labels
        self.mStatusCursorXLabel = QtGui.QLabel( self.mStatusBar )
        self.mStatusCursorXLabel.setMinimumWidth( 100 )
        self.mStatusCursorYLabel = QtGui.QLabel( self.mStatusBar )
        self.mStatusCursorYLabel.setMinimumWidth( 100 )
        self.mStatusCursorPageLabel = QtGui.QLabel( self.mStatusBar )
        self.mStatusCursorPageLabel.setMinimumWidth( 100 )
        self.mStatusCompositionLabel = QtGui.QLabel( self.mStatusBar )
        self.mStatusCompositionLabel.setMinimumWidth( 350 )
        self.mStatusAtlasLabel = QtGui.QLabel( self.mStatusBar )
        
        #hide borders from child items in status bar under Windows
        self.mStatusBar.setStyleSheet( "QStatusBar.item {border: none}" )
        
        self.mStatusBar.addWidget( self.mStatusCursorXLabel )
        self.mStatusBar.addWidget( self.mStatusCursorYLabel )
        self.mStatusBar.addWidget( self.mStatusCursorPageLabel )
        self.mStatusBar.addWidget( self.mStatusZoomCombo )
        self.mStatusBar.addWidget( self.mStatusCompositionLabel )
        self.mStatusBar.addWidget( self.mStatusAtlasLabel )
        
        #create composer view and layout with rulers
        self.mView = QgsComposerView(self)
        self.mViewLayout = QtGui.QGridLayout()
        self.mViewLayout.setSpacing( 0 )
        self.mViewLayout.setMargin( 0 )
        self.mHorizontalRuler = QgsComposerRuler( QgsComposerRuler.Horizontal )
        self.mVerticalRuler = QgsComposerRuler( QgsComposerRuler.Vertical )
        self.mRulerLayoutFix = QtGui.QWidget()
        self.mRulerLayoutFix.setAttribute( Qt.WA_NoMousePropagation )
        self.mRulerLayoutFix.setBackgroundRole( QtGui.QPalette.Window )
        self.mRulerLayoutFix.setFixedSize( self.mVerticalRuler.rulerSize(), self.mHorizontalRuler.rulerSize() )
        self.mViewLayout.addWidget( self.mRulerLayoutFix, 0, 0 )
        self.mViewLayout.addWidget( self.mHorizontalRuler, 0, 1 )
        self.mViewLayout.addWidget( self.mVerticalRuler, 1, 0 )
        self.createComposerView()
        self.mViewFrame.setLayout( self.mViewLayout )

        self.mView.cursorPosChanged.connect(self.mView_cursorPosChangedEvent)
        
        #initial state of rulers
        self.myQSettings = QSettings()
        showRulers = self.myQSettings.value( "/Composer/showRulers", True ).toBool()
        self.mActionShowRulers.blockSignals( True )
        self.mActionShowRulers.setChecked( showRulers )
        self.mHorizontalRuler.setVisible( showRulers )
        self.mVerticalRuler.setVisible( showRulers )
        self.mRulerLayoutFix.setVisible( showRulers )
        self.mActionShowRulers.blockSignals( False )
        self.connect( self.mActionShowRulers, SIGNAL( "triggered( bool )" ), self.toggleRulers)

        #init undo/redo buttons
        # self.mComposition = QgsComposition( define._canvas.mapSettings() )
        self.mComposition = None
        if newFlag:
            self.mComposition = comp
        else:
            self.on_mActionLoadFromTemplate_triggered()

        self.addItemWidget(self.mComposition)

        self.mActionUndo.setEnabled( False )
        self.mActionRedo.setEnabled( False )
        if ( self.mComposition.undoStack() ):
            self.connect( self.mComposition.undoStack(), SIGNAL( "canUndoChanged( bool )" ), self.mActionUndo, SLOT( "setEnabled( bool )" ) )
            self.connect( self.mComposition.undoStack(), SIGNAL( "canRedoChanged( bool )" ), self.mActionRedo, SLOT( "setEnabled( bool )" ))

        self.mActionShowPage.setChecked( self.mComposition.pagesVisible() )
        self.restoreGridSettings()
        self.connectViewSlots()
        self.connectCompositionSlots()
        self.connectOtherSlots()

        self.mView.setComposition( self.mComposition )
        # self.mComposition = self.mView.composition()
        #self self.connection is set up after setting the view's composition, as we don't want setComposition called
        #for QtGui.composers
        self.connect( self.mView, SIGNAL( "compositionSet( QgsComposition* )" ), self.setComposition)

        minDockWidth =  335

        self.setTabPosition( Qt.AllDockWidgetAreas, QtGui.QTabWidget.North )
        self.mGeneralDock = QtGui.QDockWidget( "Composition", self )
        self.mGeneralDock.setObjectName( "CompositionDock" )
        self.mGeneralDock.setMinimumWidth( minDockWidth )
        self.mPanelMenu.addAction( self.mGeneralDock.toggleViewAction() )
        self.mItemDock = QtGui.QDockWidget( "Item properties", self )
        self.mItemDock.setObjectName( "ItemDock" )
        self.mItemDock.setMinimumWidth( minDockWidth )
        self.mPanelMenu.addAction( self.mItemDock.toggleViewAction() )
        self.mUndoDock = QtGui.QDockWidget( "Command history", self )
        self.mUndoDock.setObjectName( "CommandDock" )
        self.mPanelMenu.addAction( self.mUndoDock.toggleViewAction() )
        # self.mAtlasDock = QtGui.QDockWidget( "Atlas generation", self )
        # self.mAtlasDock.setObjectName( "AtlasDock" )
        # self.mPanelMenu.addAction( self.mAtlasDock.toggleViewAction() )
        self.mItemsDock = QtGui.QDockWidget( "Items", self )
        self.mItemsDock.setObjectName( "ItemsDock" )
        self.mPanelMenu.addAction( self.mItemsDock.toggleViewAction() )
        self.mTableDock = QtGui.QDockWidget( "Table", self )
        self.mTableDock.setObjectName( "TableDock" )
        self.mPanelMenu.addAction( self.mTableDock.toggleViewAction() )


        docks = self.findChildren(QtGui.QDockWidget)
        for dock in docks:
            dock.setFeatures( QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetClosable )
            self.connect( dock, SIGNAL( "visibilityChanged( bool )" ), self.dockVisibilityChanged)

        self.createCompositionWidget()

        #undo widget
        self.mUndoView = QtGui.QUndoView( self.mComposition.undoStack(), self )
        self.mUndoDock.setWidget( self.mUndoView )

        self.tableEditWidget = TableEditWidget(self.mTableDock)
        self.tableEditWidget.spinBoxX.setValue(int(self.gpw.pos().x()))
        self.tableEditWidget.spinBoxY.setValue(int(self.gpw.pos().y()))
        self.tableEditWidget.spinBoxWidth.setValue(int(self.mTblView.width()))
        self.tableEditWidget.spinBoxHeight.setValue(int(self.mTblView.height()))
        self.tableEditWidget.txtFontSize.setText(str(self.gpw.font().pixelSize()))
        self.tableEditWidget.spinBoxX.valueChanged.connect(self.tableLocationChanged)
        self.tableEditWidget.spinBoxY.valueChanged.connect(self.tableLocationChanged)
        self.tableEditWidget.spinBoxWidth.valueChanged.connect(self.tableLocationChanged)
        self.tableEditWidget.spinBoxHeight.valueChanged.connect(self.tableLocationChanged)
        self.tableEditWidget.txtFontSize.textChanged.connect(self.tableLocationChanged)
        self.mTableView = self.tableEditWidget.mTableView
        hHeder = self.mTableView.horizontalHeader()
        hHeder.sectionResized.connect(self.tableHheder_sectionResized)
        # hHeder.setVisible(False)
        vHeder = self.mTableView.verticalHeader()
        vHeder.sectionResized.connect(self.tableVheder_sectionResized)
        # vHeder.setVisible(False)
        # self.connect(self.parentDlg, SIGNAL("itemChanged"), self.mStdModel_itemChanged)

        if newFlag:
            self.mStdModel = model
            # self.mStdModel.itemChanged.connect(self.mStdModel_itemChanged)
        self.mTableView.setModel(self.mStdModel)

        self.mTableView.setSpan(0, 0, 1, int(self.data["CatOfAcftCount"][0]) + 3)
        self.mTableView.setSpan(1, 0, 1, 3)
        if self.data["Template"][0] >= 0 and int(self.data["Template"][0]) <= 4:
            self.mTableView.setSpan(2, 0, 1, 3)
            self.mTableView.setSpan(2, 3, 1, int(self.data["CatOfAcftCount"][0]))
            self.mTableView.setSpan(3, 0, 1, int(self.data["CatOfAcftCount"][0]) + 3)
            self.mTableView.setSpan(4, 0, 1, 3)
            self.mTableView.setSpan(5, 0, 1, 3)
            self.mTableView.setSpan(6, 0, 1, 3)
        else:
            self.mTableView.setSpan(2, 0, 1, 3)
            self.mTableView.setSpan(3, 0, 1, 3)
            self.mTableView.setSpan(4, 0, 1, 3)
            self.mTableView.setSpan(5, 0, 1, 3)
            self.mTableView.setSpan(6, 0, 1, 3)

        # self.mTableView.setSpan(data["StraightCount"] + 2, 0, 1, 3)

        self.mTableView.setSpan(0, int(self.data["CatOfAcftCount"][0]) + 3, 1, 9)
        # self.mTableView.setSpan(1, data["CatOfAcftCount"][0] + 4, 1, 5)
        # self.mTableView.setSpan(1, data["CatOfAcftCount"][0] + 9, 1, 3)
        # self.mTableView.setSpan(2, data["CatOfAcftCount"][0] + 5, 1, 4)
        # self.mTableView.setSpan(2, data["CatOfAcftCount"][0] + 9, 1, 3)

        self.mTableView.setSpan(1, int(self.data["CatOfAcftCount"][0]) + 3, 1, 2)
        self.mTableView.setSpan(2, int(self.data["CatOfAcftCount"][0]) + 3, 1, 2)
        self.mTableView.setSpan(3, int(self.data["CatOfAcftCount"][0]) + 3, 1, 2)
        self.mTableView.setSpan(4, int(self.data["CatOfAcftCount"][0]) + 3, 1, 2)
        self.mTableView.setSpan(5, int(self.data["CatOfAcftCount"][0]) + 3, 1, 2)
        self.mTableView.setSpan(6, int(self.data["CatOfAcftCount"][0]) + 3, 1, 2)

        
        self.mTableDock.setWidget(self.tableEditWidget)

        tblView = self.mTblView
        self.hHederRate = float(hHeder.sectionSize(0) / float(tblView.horizontalHeader().sectionSize(0)))
        self.vHederRate = float(vHeder.sectionSize(0) / float(tblView.verticalHeader().sectionSize(0)))

        #items tree widget
        self.mItemsTreeView = QtGui.QTreeView( self.mItemsDock )
        self.mItemsTreeView.setModel( self.mComposition.itemsModel() )

        self.mItemsTreeView.setColumnWidth( 0, 30 )
        self.mItemsTreeView.setColumnWidth( 1, 30 )
        self.mItemsTreeView.header().setResizeMode( 0, QtGui.QHeaderView.Fixed )
        self.mItemsTreeView.header().setResizeMode( 1, QtGui.QHeaderView.Fixed )
        self.mItemsTreeView.header().setMovable( False )

        self.mItemsTreeView.setDragEnabled( True )
        self.mItemsTreeView.setAcceptDrops( True )
        self.mItemsTreeView.setDropIndicatorShown( True )
        self.mItemsTreeView.setDragDropMode( QtGui.QAbstractItemView.InternalMove )

        self.mItemsTreeView.setIndentation( 0 )
        self.mItemsDock.setWidget( self.mItemsTreeView )
        self.connect( self.mItemsTreeView.selectionModel(), SIGNAL( "currentChanged( QModelIndex, QModelIndex )" ), self.mComposition.itemsModel(), SLOT( "setSelected( QModelIndex )" ) )

        self.addDockWidget( Qt.RightDockWidgetArea, self.mItemDock )
        self.addDockWidget( Qt.RightDockWidgetArea, self.mGeneralDock )
        self.addDockWidget( Qt.RightDockWidgetArea, self.mUndoDock )
        # self.addDockWidget( Qt.RightDockWidgetArea, self.mAtlasDock )
        self.addDockWidget( Qt.RightDockWidgetArea, self.mItemsDock )
        self.addDockWidget( Qt.RightDockWidgetArea, self.mTableDock )

        # atlasWidget = QgsAtlasCompositionWidget( self.mGeneralDock, self.mComposition )
        # self.mAtlasDock.setWidget( atlasWidget )

        self.mItemDock.show()
        self.mGeneralDock.show()
        self.mUndoDock.show()
        # self.mAtlasDock.show()
        self.mItemsDock.show()

        self.tabifyDockWidget( self.mGeneralDock, self.mUndoDock )
        self.tabifyDockWidget( self.mItemDock, self.mUndoDock )
        self.tabifyDockWidget( self.mGeneralDock, self.mItemDock )
        # self.tabifyDockWidget( self.mItemDock, self.mAtlasDock )
        self.tabifyDockWidget( self.mItemDock, self.mItemsDock )


        self.mGeneralDock.show()

        #set initial state of atlas controls
        self.mActionAtlasPreview.setEnabled( False )
        self.mActionAtlasPreview.setChecked( False )
        self.mActionAtlasFirst.setEnabled( False )
        self.mActionAtlasLast.setEnabled( False )
        self.mActionAtlasNext.setEnabled( False )
        self.mActionAtlasPrev.setEnabled( False )
        self.mActionPrintAtlas.setEnabled( False )
        self.mAtlasPageComboBox.setEnabled( False )
        self.mActionExportAtlasAsImage.setEnabled( False )
        self.mActionExportAtlasAsSVG.setEnabled( False )
        self.mActionExportAtlasAsPDF.setEnabled( False )
        atlasMap = self.mComposition.atlasComposition()
        self.connect( atlasMap, SIGNAL( "toggled( bool )" ), self.toggleAtlasControls)
        self.connect( atlasMap, SIGNAL( "coverageLayerChanged( QgsVectorLayer* )" ), self.updateAtlasMapLayerAction)
        self.connect( atlasMap, SIGNAL( "numberFeaturesChanged( int )" ), self.updateAtlasPageComboBox)
        self.connect( atlasMap, SIGNAL( "featureChanged( QgsFeature* )" ), self.atlasFeatureChanged)

        # Create size grip (needed by Mac OS X for QMainWindow if QStatusBar is not visible)
        #should not be needed now that composer has a status bar?
        #if 0
        self.mSizeGrip = QtGui.QSizeGrip( self )
        self.mSizeGrip.resize( self.mSizeGrip.sizeHint() )
        self.mSizeGrip.move( self.rect().bottomRight() - self.mSizeGrip.rect().bottomRight() )
        #endif

        self.restoreWindowState()
        self.setSelectionTool()

        self.mView.setFocus()

        #connect with signals from QgsProject to write project files
        if ( QgsProject.instance() ):
            self.connect( QgsProject.instance(), SIGNAL( "writeProject( QDomDocument& )" ), self.writeXML)

        #if defined(ANDROID)
        # fix for Qt Ministro hiding app's menubar in favor of native Android menus
        self.menuBar().setNativeMenuBar( False )
        self.menuBar().setVisible( True )

        self.initLayerTreeView()

        self.mItemActionToolbar.setVisible(False)
        self.mAtlasToolbar.setVisible(False)


        self.addItemName = ""
        self.scenePoint = None

        self.compStartPointF = None
        self.compEndPointF = None
        self.mNewItems = []

        if self.mComposition.plotStyle() != QgsComposition.Preview:
            self.mComposition.setPlotStyle(QgsComposition.Preview)


        self.tableChangedValue = None
        self.connect(self.mComposition, SIGNAL("itemRemoved (QgsComposerItem *)"), self.mComposition_itemRemoved)

        define._canvas.setCachingEnabled(True)
        define._canvas.setCacheMode(QGraphicsView.CacheBackground)

    def mComposition_itemRemoved(self, composerItem):
        uuid = composerItem.uuid()
        self.mItemWidgetMap.pop(uuid)
        i = 0
        for item in self.mNewItems:
            if uuid == item.uuid():
                self.mNewItems.pop(i)
                break
            i += 1
        pass
    def tableHheder_sectionResized(self, logicalIndex, oldSize, newSize):
        hHeder = self.mTblView.horizontalHeader()
        hHeder.resizeSection( logicalIndex, int(round(float(newSize) / float(self.hHederRate))))
    def tableVheder_sectionResized(self, logicalIndex, oldSize, newSize):
        vHeder = self.mTblView.verticalHeader()
        vHeder.resizeSection( logicalIndex, int(round(float(newSize) / float(self.vHederRate))))
    def tableLocationChanged(self):
        gpw0 = self.gpw
        tblView = self.mTblView
        try:
            self.tableChangedValue = {"X": self.tableEditWidget.spinBoxX.value(),
                                        "Y": self.tableEditWidget.spinBoxY.value(),
                                        "Width": self.tableEditWidget.spinBoxWidth.value(),
                                        "Height": self.tableEditWidget.spinBoxHeight.value(),
                                        "FontSize": int(self.tableEditWidget.txtFontSize.text())}
        except:
            # QMessageBox.warning(self, "Warning", "please input correct value.")
            return
        if self.newFlag:
            self.parentDlg.tableChangedValue = self.tableChangedValue
        gpw0.setPos(self.tableChangedValue["X"], self.tableChangedValue["Y"])
        font = QFont()
        font.setPixelSize(self.tableChangedValue["FontSize"])
        gpw0.setFont(font)

        tblView.setFixedWidth(self.tableChangedValue["Width"])
        tblView.setFixedHeight(self.tableChangedValue["Height"])

    def addItemWidget(self, comp):
        if not comp or not isinstance(comp, QgsComposition):
            return
        mapItems = comp.composerMapItems()
        for mapItem in mapItems:
            widget = QgsComposerMapWidget(None, mapItem)
            self.mItemWidgetMap.__setitem__(mapItem.uuid(), widget)
        graphicsItemList = comp.items()
        # QList<QGraphicsItem *>::iterator itemIt = graphicsItemList.begin()
        for itemIt in graphicsItemList:
            itemIt._class_ = QgsComposerLabel
            if ( isinstance(itemIt, QgsComposerLabel )):
                widget = QgsComposerLabelWidget(None, itemIt)
                self.mItemWidgetMap.__setitem__(itemIt.uuid(), widget)
        pass

    def mView_cursorPosChangedEvent(self, scenePointF):
        self.scenePoint = scenePointF
    def initLayerTreeView(self):
        mLegend = QDockWidget("Layers", self)
        mLegend.setObjectName( "Layers" )
        mLegend.setAllowedAreas( Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea )
        self._mLayerTreeView = MyLayerTreeView(self)
        define._mLayerTreeView = self._mLayerTreeView
        self._mLayerTreeView.setObjectName("theLayerTreeView")

        model = QgsLayerTreeModel( QgsProject.instance().layerTreeRoot(), self )
        model.setFlag( QgsLayerTreeModel.AllowNodeReorder )
        model.setFlag( QgsLayerTreeModel.AllowNodeRename )
        model.setFlag( QgsLayerTreeModel.AllowNodeChangeVisibility )
        model.setAutoCollapseSymbologyNodes( 10 )

        self._mLayerTreeView.setModel( model )
        # self._mLayerTreeView.setMenuProvider( QgsAppLayerTreeViewMenuProvider( self._mLayerTreeView) )
        # self.setupLayerTreeViewFromSettings()
        #
        # self._mLayerTreeView.selectionModel().selectionChanged.connect(self.legendLayerSelectionChanged)
        # self._mLayerTreeView.layerTreeModel().rootGroup().addedChildren.connect(self.markDirty)
        # self._mLayerTreeView.layerTreeModel().rootGroup().addedChildren.connect(self.updateNewLayerInsertionPoint)
        # self._mLayerTreeView.layerTreeModel().rootGroup().removedChildren.connect( self.markDirty )
        # self._mLayerTreeView.layerTreeModel().rootGroup().removedChildren.connect( self.updateNewLayerInsertionPoint )
        # self._mLayerTreeView.layerTreeModel().rootGroup().visibilityChanged.connect( self.markDirty )
        # self._mLayerTreeView.layerTreeModel().rootGroup().customPropertyChanged.connect( self.markDirty )
        #
        # self._mLayerTreeView.currentLayerChanged.connect( self.activeLayerChanged)
        # self._mLayerTreeView.selectionModel().currentChanged.connect(self.updateNewLayerInsertionPoint)

        vboxLayout = QVBoxLayout()
        vboxLayout.setMargin(0)
        vboxLayout.addWidget(self._mLayerTreeView)
        w = QWidget()
        w.setLayout( vboxLayout )
        mLegend.setWidget( w )

        self.addDockWidget( Qt.LeftDockWidgetArea, mLegend )

        mLayerTreeCanvasBridge = QgsLayerTreeMapCanvasBridge( QgsProject.instance().layerTreeRoot(), define._canvas, self )

        self.mPanelMenu.addAction( mLegend.toggleViewAction() )
        define._canvas.renderComplete.connect(self.canvas_renderComplete)
        define._canvas.layersChanged.connect(self.canvas_renderComplete)
        # define._canvas.layersChanged.connect(self.composerMapRefresh)

        self.layerChangedFlag = False

    def canvas_renderComplete(self):
        # mapList = []
        # if self.layerChangedFlag:
        #     mapList = self.mComposition.composerMapItems()
        # else:
        if len(self.mComposition.selectedComposerItems()) == 0:
                return
        composerMap = self.mComposition.selectedComposerItems()[0]
        if not isinstance(composerMap, QgsComposerMap):
            return
        renderer = self.mComposition.mapRenderer()
        # renderer.setExtent(define._canvas.extent())
        renderer.updateFullExtent()
        newExtent = renderer.extent()

        #Make sure the width/height ratio is the same as in current composer map extent.
        #This is to keep the map item frame and the page layout fixed
        currentMapExtent = composerMap.currentMapExtent()
        currentWidthHeightRatio = currentMapExtent.width() / currentMapExtent.height()
        newWidthHeightRatio = newExtent.width() / newExtent.height()

        if currentWidthHeightRatio < newWidthHeightRatio :
            #enlarge height of new extent, ensuring the map center stays the same
            newHeight = newExtent.width() / currentWidthHeightRatio
            deltaHeight = newHeight - newExtent.height()
            newExtent.setYMinimum( newExtent.yMinimum() - deltaHeight / 2 )
            newExtent.setYMaximum( newExtent.yMaximum() + deltaHeight / 2 )

        else:
            #enlarge width of new extent, ensuring the map center stays the same
            newWidth = currentWidthHeightRatio * newExtent.height()
            deltaWidth = newWidth - newExtent.width()
            newExtent.setXMinimum( newExtent.xMinimum() - deltaWidth / 2 )
            newExtent.setXMaximum( newExtent.xMaximum() + deltaWidth / 2 )

        composerMap.beginCommand( "Map extent changed")
        composerMap.setNewExtent( newExtent )
        composerMap.endCommand()
        pass
        # item.updateCachedImage()
    def rePresent(self, comp, model, data):
        self.data = data
        self.mComposition = comp
        self.mStdModel = model

        self.mTableView.clearSpans()
        # hHeder = self.mTableView.horizontalHeader()
        # hHeder.setVisible(False)
        # vHeder = self.mTableView.verticalHeader()
        # vHeder.setVisible(False)
        # self.mStdModel = model
        self.mTableView.setModel(self.mStdModel)

        self.mTableView.setSpan(0, 0, 1, int(data["CatOfAcftCount"][0]) + 3)
        self.mTableView.setSpan(1, 0, 1, 3)
        if int(data["Template"][0]) >= 0 and int(data["Template"][0]) <= 4:
            self.mTableView.setSpan(2, 0, 1, 3)
            self.mTableView.setSpan(2, 3, 1, int(data["CatOfAcftCount"][0]))
            self.mTableView.setSpan(3, 0, 1, int(data["CatOfAcftCount"][0]) + 3)
            self.mTableView.setSpan(4, 0, 1, 3)
            self.mTableView.setSpan(5, 0, 1, 3)
            self.mTableView.setSpan(6, 0, 1, 3)
        else:
            self.mTableView.setSpan(2, 0, 1, 3)
            self.mTableView.setSpan(3, 0, 1, 3)
            self.mTableView.setSpan(4, 0, 1, 3)
            self.mTableView.setSpan(5, 0, 1, 3)
            self.mTableView.setSpan(6, 0, 1, 3)

        # self.mTableView.setSpan(data["StraightCount"] + 2, 0, 1, 3)

        self.mTableView.setSpan(0, int(data["CatOfAcftCount"][0]) + 3, 1, 9)
        # self.mTableView.setSpan(1, data["CatOfAcftCount"][0] + 4, 1, 5)
        # self.mTableView.setSpan(1, data["CatOfAcftCount"][0] + 9, 1, 3)
        # self.mTableView.setSpan(2, data["CatOfAcftCount"][0] + 5, 1, 4)
        # self.mTableView.setSpan(2, data["CatOfAcftCount"][0] + 9, 1, 3)

        self.mTableView.setSpan(1, int(data["CatOfAcftCount"][0]) + 3, 1, 2)
        self.mTableView.setSpan(2, int(data["CatOfAcftCount"][0]) + 3, 1, 2)
        self.mTableView.setSpan(3, int(data["CatOfAcftCount"][0]) + 3, 1, 2)
        self.mTableView.setSpan(4, int(data["CatOfAcftCount"][0]) + 3, 1, 2)
        self.mTableView.setSpan(5, int(data["CatOfAcftCount"][0]) + 3, 1, 2)
        self.mTableView.setSpan(6, int(data["CatOfAcftCount"][0]) + 3, 1, 2)

        self.tableEditWidget.vLayoutForm.addWidget(self.mTableView)
        i = 0

        for item in self.mNewItems:
            if isinstance(item, QgsComposerMap):
                x = item.pagePos().x()
                y = item.pagePos().y()
                w = item.rectWithFrame().width()
                h = item.rectWithFrame().height()
                composerMap = QgsComposerMap(comp, x, y, w, h)
        #         composerMap.setPreviewMode(QgsComposerMap.Render)
        #         composerMap.setGridEnabled(False)

                #rect = composerMap.currentMapExtent ()
                renderer = composerMap.mapRenderer()
                newExtent = renderer.extent()

                #Make sure the width/height ratio is the same as in current composer map extent.
                #This is to keep the map item frame and the page layout fixed
                currentMapExtent = composerMap.currentMapExtent()
                currentWidthHeightRatio = currentMapExtent.width() / currentMapExtent.height()
                newWidthHeightRatio = newExtent.width() / newExtent.height()

                if currentWidthHeightRatio < newWidthHeightRatio :
                    #enlarge height of new extent, ensuring the map center stays the same
                    newHeight = newExtent.width() / currentWidthHeightRatio
                    deltaHeight = newHeight - newExtent.height()
                    newExtent.setYMinimum( newExtent.yMinimum() - deltaHeight / 2 )
                    newExtent.setYMaximum( newExtent.yMaximum() + deltaHeight / 2 )

                else:
                    #enlarge width of new extent, ensuring the map center stays the same
                    newWidth = currentWidthHeightRatio * newExtent.height()
                    deltaWidth = newWidth - newExtent.width()
                    newExtent.setXMinimum( newExtent.xMinimum() - deltaWidth / 2 )
                    newExtent.setXMaximum( newExtent.xMaximum() + deltaWidth / 2 )

                composerMap.beginCommand( "Map extent changed")
                composerMap.setNewExtent( newExtent )
                composerMap.endCommand()
                # composerMap.setNewScale(3500)

                composerMap.setFrameEnabled(True)
                composerMap.setFrameOutlineWidth(1.0)
                composerMap.setPreviewMode(QgsComposerMap.Render)
                composerMap.updateCachedImage()

                composerMap.setGridEnabled(True)
                composerMap.setGridPenColor(QColor(255,255,255,0))
                composerMap.setGridPenWidth(0.0)
                #composerMap.setGridStyle(QgsComposerMap.FrameAnnotationsOnly)
                composerMap.setGridIntervalX(1.0)
                composerMap.setGridIntervalY(1.0)
        #         mySymbol1 = composerMap.gridLineSymbol ()
        #         mySymbol1.setAlpha(0)
                #composerMap.setGridLineSymbol(mySymbol1)
                composerMap.setShowGridAnnotation(True)
                composerMap.setGridAnnotationFormat(1)
                composerMap.setGridAnnotationPrecision (0)
                composerMap.setGridAnnotationDirection(1,0)
                composerMap.setGridAnnotationDirection(1,1)

                comp.addItem(composerMap)
                self.mComposition.addItem(composerMap)


                composerMap.setMapCanvas( define._canvas)#set canvas to composer map to have the possibility to draw canvas items
                mapWidget = QgsComposerMapWidget( None, composerMap )
                composerMap.setCacheUpdated(True)
                self.connect( self, SIGNAL( "zoomLevelChanged()" ), composerMap, SLOT( "renderModeUpdateCachedImage()" ) )
                self.mItemWidgetMap.pop(str(item.uuid()))
                self.mItemWidgetMap.__setitem__( composerMap.uuid(), mapWidget )
                self.mNewItems.pop(i)
                self.mNewItems.insert(i, composerMap)
                i += 1
                continue
            self.mComposition.addItem(item)
        self.mView.setComposition(comp)
        self.addItemWidget(self.mComposition)
        if self.mComposition.plotStyle() != QgsComposition.Preview:
            self.mComposition.setPlotStyle(QgsComposition.Preview)

        tblView = self.mTblView
        hHeder = self.mTableView.horizontalHeader()
        vHeder = self.mTableView.verticalHeader()
        self.hHederRate = float(hHeder.sectionSize(0) / float(tblView.horizontalHeader().sectionSize(0)))
        self.vHederRate = float(vHeder.sectionSize(0) / float(tblView.verticalHeader().sectionSize(0)))

        # self.scene = self.view.composition()
    def composerMapRefresh(self):
        if self.newFlag:
            self.parentDlg.renderFlag = True
            self.parentDlg.changedComposerMap = self.mComposition.composerMapItems()[0]
            self.parentDlg.btnExit_clicked()
        # else:
        #
        #     for item in self.mComposition.composerMapItems():
        #         uuid = item.uuid()
        #         x = item.pagePos().x()
        #         y = item.pagePos().y()
        #         w = item.rectWithFrame().width()
        #         h = item.rectWithFrame().height()
        #         composerMap = QgsComposerMap(self.mComposition, x, y, w, h)
        # #         composerMap.setPreviewMode(QgsComposerMap.Render)
        # #         composerMap.setGridEnabled(False)
        #
        #         #rect = composerMap.currentMapExtent ()
        #         renderer = composerMap.mapRenderer()
        #         newExtent = renderer.extent()
        #
        #         #Make sure the width/height ratio is the same as in current composer map extent.
        #         #This is to keep the map item frame and the page layout fixed
        #         currentMapExtent = composerMap.currentMapExtent()
        #         currentWidthHeightRatio = currentMapExtent.width() / currentMapExtent.height()
        #         newWidthHeightRatio = newExtent.width() / newExtent.height()
        #
        #         if currentWidthHeightRatio < newWidthHeightRatio :
        #             #enlarge height of new extent, ensuring the map center stays the same
        #             newHeight = newExtent.width() / currentWidthHeightRatio
        #             deltaHeight = newHeight - newExtent.height()
        #             newExtent.setYMinimum( newExtent.yMinimum() - deltaHeight / 2 )
        #             newExtent.setYMaximum( newExtent.yMaximum() + deltaHeight / 2 )
        #
        #         else:
        #             #enlarge width of new extent, ensuring the map center stays the same
        #             newWidth = currentWidthHeightRatio * newExtent.height()
        #             deltaWidth = newWidth - newExtent.width()
        #             newExtent.setXMinimum( newExtent.xMinimum() - deltaWidth / 2 )
        #             newExtent.setXMaximum( newExtent.xMaximum() + deltaWidth / 2 )
        #
        #         composerMap.beginCommand( "Map extent changed")
        #         composerMap.setNewExtent( newExtent )
        #         composerMap.endCommand()
        #         # composerMap.setNewScale(3500)
        #
        #         composerMap.setFrameEnabled(True)
        #         composerMap.setFrameOutlineWidth(1.0)
        #         composerMap.setPreviewMode(QgsComposerMap.Render)
        #         composerMap.updateCachedImage()
        #
        #         composerMap.setGridEnabled(True)
        #         composerMap.setGridPenColor(QColor(255,255,255,0))
        #         composerMap.setGridPenWidth(0.0)
        #         #composerMap.setGridStyle(QgsComposerMap.FrameAnnotationsOnly)
        #         composerMap.setGridIntervalX(1.0)
        #         composerMap.setGridIntervalY(1.0)
        # #         mySymbol1 = composerMap.gridLineSymbol ()
        # #         mySymbol1.setAlpha(0)
        #         #composerMap.setGridLineSymbol(mySymbol1)
        #         composerMap.setShowGridAnnotation(True)
        #         composerMap.setGridAnnotationFormat(1)
        #         composerMap.setGridAnnotationPrecision (0)
        #         composerMap.setGridAnnotationDirection(1,0)
        #         composerMap.setGridAnnotationDirection(1,1)
        #
        #         # self.mComposition.addItem(composerMap)
        #
        #
        #         composerMap.setMapCanvas( define._canvas)#set canvas to composer map to have the possibility to draw canvas items
        #         mapWidget = QgsComposerMapWidget( None, composerMap )
        #         composerMap.setCacheUpdated(True)
        #         self.connect( self, SIGNAL( "zoomLevelChanged()" ), composerMap, SLOT( "renderModeUpdateCachedImage()" ) )
        #         # self.mItemWidgetMap.pop(uuid)
        #         self.mItemWidgetMap.__setitem__( composerMap.uuid(), mapWidget )
        #
        #         self.mComposition.removeComposerItem(item)
        #         self.mComposition.addItem(composerMap)
                # i = 0
                # for newItem in self.mNewItems:
                #     if uuid == newItem.uuid():
                #         self.mNewItems.pop(i)
                #         self.mNewItems.insert(i, composerMap)
                #         break
                #     i += 1
                # item = composerMap
    def atlasFeatureChanged(self, feature):
        if ( not self.mComposition ):
            return

        # self.mAtlasPageComboBox.blockSignals( True )
        # # //prefer to set index of current atlas page, if combo box is showing enough page items
        # if ( self.mComposition.atlasComposition().currentFeatureNumber() < self.mAtlasPageComboBox.count() ):
        #     self.mAtlasPageComboBox.setCurrentIndex( self.mComposition.atlasComposition().currentFeatureNumber() )
        # else:
        #     # //fallback to setting the combo text to the page number
        #     self.mAtlasPageComboBox.setEditText( QString.number( self.mComposition.atlasComposition().currentFeatureNumber() + 1 ) )
        # self.mAtlasPageComboBox.blockSignals( False )
        #
        # # //update expression context variables in map canvas to allow for previewing atlas feature based renderering
        # define._canvas.expressionContextScope().addVariable( QgsExpressionContextScope.StaticVariable( "atlas_featurenumber", self.mComposition.atlasComposition().currentFeatureNumber() + 1, True ) )
        # define._canvas.expressionContextScope().addVariable( QgsExpressionContextScope.StaticVariable( "atlas_pagename", self.mComposition.atlasComposition().currentPageName(), True ) )
        # atlasFeature = self.mComposition.atlasComposition().feature()
        # define._canvas.expressionContextScope().addVariable( QgsExpressionContextScope.StaticVariable( "atlas_feature", QVariant.fromValue( atlasFeature ), True ) )
        # define._canvas.expressionContextScope().addVariable( QgsExpressionContextScope.StaticVariable( "atlas_featureid", atlasFeature.id(), True ) )
        # define._canvas.expressionContextScope().addVariable( QgsExpressionContextScope.StaticVariable( "atlas_geometry", QVariant.fromValue( *atlasFeature.constGeometry() ), True ) )
    def on_mActionAtlasPreview_triggered(self, checked):
        atlasMap = self.mComposition.atlasComposition()

        # //check if composition has an atlas map enabled
        if ( checked and not atlasMap.enabled() ):
            # //no atlas current enabled
            QMessageBox.warning( None, "Enable atlas preview" ,
                                  "Atlas in not currently enabled for this composition!" ,
                                  QMessageBox.Ok,
                                  QMessageBox.Ok )
            self.mActionAtlasPreview.blockSignals( True )
            self.mActionAtlasPreview.setChecked( False )
            self.mActionAtlasPreview.blockSignals( False )
            self.mStatusAtlasLabel.setText( QString() )
            return

        # //toggle other controls depending on whether atlas preview is active
        self.mActionAtlasFirst.setEnabled( checked )
        self.mActionAtlasLast.setEnabled( checked )
        self.mActionAtlasNext.setEnabled( checked )
        self.mActionAtlasPrev.setEnabled( checked )
        self.mAtlasPageComboBox.setEnabled( checked )

        if ( checked ):
            self.loadAtlasPredefinedScalesFromProject()

        previewEnabled = self.mComposition.setAtlasMode( QgsComposition.PreviewAtlas if(checked) else QgsComposition.AtlasOff )
        if ( not previewEnabled ):
            # //something went wrong, eg, no matching features
            QMessageBox.warning( None, "Enable atlas preview" ,
                                  "No matching atlas features found!" ,
                                  QMessageBox.Ok,
                                  QMessageBox.Ok )
            self.mActionAtlasPreview.blockSignals( True )
            self.mActionAtlasPreview.setChecked( False )
            self.mActionAtlasFirst.setEnabled( False )
            self.mActionAtlasLast.setEnabled( False )
            self.mActionAtlasNext.setEnabled( False )
            self.mActionAtlasPrev.setEnabled( False )
            self.mAtlasPageComboBox.setEnabled( False )
            self.mActionAtlasPreview.blockSignals( False )
            self.mStatusAtlasLabel.setText( QString() )
            return

        if ( checked ):
            define._canvas.stopRendering()
            self.emit(SIGNAL("atlasPreviewFeatureChanged()"))
        else:
            self.mStatusAtlasLabel.setText( QString() )
    def loadAtlasPredefinedScalesFromProject(self):
        pass
    def toggleAtlasControls(self, atlasEnabled):
        # //preview defaults to unchecked
        self.mActionAtlasPreview.blockSignals( True )
        self.mActionAtlasPreview.setChecked( False )
        self.mActionAtlasFirst.setEnabled( False )
        self.mActionAtlasLast.setEnabled( False )
        self.mActionAtlasNext.setEnabled( False )
        self.mActionAtlasPrev.setEnabled( False )
        self.mAtlasPageComboBox.setEnabled( False )
        self.mActionAtlasPreview.blockSignals( False )
        self.mActionAtlasPreview.setEnabled( atlasEnabled )
        self.mActionPrintAtlas.setEnabled( atlasEnabled )
        self.mActionExportAtlasAsImage.setEnabled( atlasEnabled )
        self.mActionExportAtlasAsSVG.setEnabled( atlasEnabled )
        self.mActionExportAtlasAsPDF.setEnabled( atlasEnabled )

        self.updateAtlasMapLayerActionBool( atlasEnabled )
    def updateAtlasPageComboBox(self, pageCount):
        if ( not self.mComposition ):
            return

        self.mAtlasPageComboBox.blockSignals( True )
        self.mAtlasPageComboBox.clear()
        i = 1
        while (i <= pageCount and i < 500):
            name = self.mComposition.atlasComposition().nameForPage( i - 1 )
            fullName = ( QString( "%1: %2" ).arg( i ).arg( name ) if(not name.isEmpty()) else QString.number( i )) 

            self.mAtlasPageComboBox.addItem( fullName, i )
            self.mAtlasPageComboBox.setItemData( i - 1, name, Qt.UserRole + 1 )
            self.mAtlasPageComboBox.setItemData( i - 1, fullName, Qt.UserRole + 2 )
            i += 1
        self.mAtlasPageComboBox.blockSignals( False )

    def setSelectionTool(self):
        self.mActionSelectMoveItem.setChecked(True)
        self.on_mActionSelectMoveItem_triggered()
    def updateAtlasMapLayerAction(self, coverageLayer):
        if ( self.mAtlasFeatureAction ):
            self.mAtlasFeatureAction == None
            self.mAtlasFeatureAction = 0

        if ( coverageLayer ):
            self.mAtlasFeatureAction = QgsMapLayerAction( QString( "Set as atlas feature for %1"  ).arg( self.mTitle ), self, coverageLayer )
            QgsMapLayerActionRegistry.instance().addMapLayerAction( self.mAtlasFeatureAction )
            self.connect(self, self.mAtlasFeatureAction, SIGNAL( "triggeredForFeature( QgsMapLayer*, QgsFeature* )"), self.setAtlasFeature)

    def updateAtlasMapLayerActionBool(self, atlasEnabled):
        pass
    def connectCompositionSlots(self):
        if ( not self.mComposition ):
            return

        self.connect( self.mView, SIGNAL( "actionFinished()" ), self.mView_actionFinished)
        self.connect( self.mComposition, SIGNAL( "selectedItemChanged( QgsComposerItem* )" ), self.showItemOptions)
        self.connect( self.mComposition, SIGNAL( "composerArrowAdded( QgsComposerArrow* )" ), self.addComposerArrow)
        self.connect( self.mComposition, SIGNAL( "composerHtmlFrameAdded( QgsComposerHtml*, QgsComposerFrame* )" ), self.addComposerHtmlFrame)
        self.connect( self.mComposition, SIGNAL( "composerLabelAdded( QgsComposerLabel* )" ), self.addComposerLabel)
        # self.mComposition.composerMapAdded.connect(lambda item: self.addComposerMap(self.mComposition, item))
        QObject.connect( self.mComposition, SIGNAL( "composerMapAdded( QgsComposerMap* )" ), self.addComposerMap)
        self.connect( self.mComposition, SIGNAL( "composerScaleBarAdded( QgsComposerScaleBar* )" ), self.addComposerScaleBar)
        self.connect( self.mComposition, SIGNAL( "composerLegendAdded( QgsComposerLegend* )" ), self.addComposerLegend)
        self.connect( self.mComposition, SIGNAL( "composerPictureAdded( QgsComposerPicture* )" ), self.addComposerPicture)
        self.connect( self.mComposition, SIGNAL( "composerShapeAdded( QgsComposerShape* )" ), self.addComposerShape)
        self.connect( self.mComposition, SIGNAL( "composerTableAdded( QgsComposerAttributeTable* )" ), self.addComposerTable)
        self.connect( self.mComposition, SIGNAL( "composerTableFrameAdded( QgsComposerAttributeTableV2*, QgsComposerFrame* )" ), self.addComposerTableV2)
        self.connect( self.mComposition, SIGNAL( "itemRemoved( QgsComposerItem* )" ), self.deleteItem)
        self.connect( self.mComposition, SIGNAL( "paperSizeChanged()" ), self.mHorizontalRuler, SLOT( "update()" ) )
        self.connect( self.mComposition, SIGNAL( "paperSizeChanged()" ), self.mVerticalRuler, SLOT( "update()" ) )
        self.connect( self.mComposition, SIGNAL( "nPagesChanged()" ), self.mHorizontalRuler, SLOT( "update()" ) )
        self.connect( self.mComposition, SIGNAL( "nPagesChanged()" ), self.mVerticalRuler, SLOT( "update()" ) )

        # //listen out to status bar updates from the atlas
        atlasMap = self.mComposition.atlasComposition()
        self.connect( atlasMap, SIGNAL( "statusMsgChanged( QString )" ), self.updateStatusAtlasMsg)

        # //listen out to status bar updates from the composition
        self.connect( self.mComposition, SIGNAL( "statusMsgChanged( QString )" ), self.updateStatusCompositionMsg)
    def updateStatusAtlasMsg(self, message):
        self.mStatusAtlasLabel.setText( message )
    def updateStatusCompositionMsg(self, message):
        self.mStatusCompositionLabel.setText( message )
    def addComposerTableV2(self, table, frame):
        pass
    def addComposerTable(self, table):
        if ( not table ):
            return
        # tWidget = QgsComposerTableWidget( table )
        # self.mItemWidgetMap.insert( table, tWidget )
    def addComposerShape(self, shape):
        self.addItemName = "Shape"
    def addComposerPicture(self, picture):
        pass
    def addComposerLegend(self, legend):
        pass
    def addComposerScaleBar(self, scalebar):
        pass

    def connectOtherSlots(self):
        # //also listen out for position updates from the horizontal/vertical rulers
        self.connect( self.mHorizontalRuler, SIGNAL( "cursorPosChanged( QPointF )" ), self.updateStatusCursorPos)
        self.connect( self.mVerticalRuler, SIGNAL( "cursorPosChanged( QPointF )" ), self.updateStatusCursorPos)
        # //listen out for zoom updates
        self.connect( self, SIGNAL( "zoomLevelChanged()" ), self.updateStatusZoom)
    def restoreGridSettings(self):
        # //restore grid settings
        self.mActionSnapGrid.setChecked( self.mComposition.snapToGridEnabled() )
        self.mActionShowGrid.setChecked( self.mComposition.gridVisible() )
        # //restore guide settings
        self.mActionShowGuides.setChecked( self.mComposition.snapLinesVisible() )
        self.mActionSnapGuides.setChecked( self.mComposition.alignmentSnap() )
        self.mActionSmartGuides.setChecked( self.mComposition.smartGuidesEnabled() )
        # //general view settings
        self.mActionShowBoxes.setChecked( self.mComposition.boundingBoxesVisible() )
    def mView_actionFinished(self):
        if len(self.mComposition.selectedComposerItems()) == 0:
                return
        item = self.mComposition.selectedComposerItems()[0]
        qRectF = item.rectWithFrame()
        pos = item.pagePos()

        x = pos.x()
        y = pos.y()
        w = qRectF.width()
        h = qRectF.height()
        if self.addItemName == "Map":
    #         self.mView.deleteSelectedItems()
    #         # x, y = 20, 45
    #         composerMap = QgsComposerMap(self.mComposition, x, y, w, h)
    # #         composerMap.setPreviewMode(QgsComposerMap.Render)
    # #         composerMap.setGridEnabled(False)
    #
    #         #rect = composerMap.currentMapExtent ()
    #         renderer = composerMap.mapRenderer()
    #         newExtent = renderer.extent()
    #
    #         #Make sure the width/height ratio is the same as in current composer map extent.
    #         #This is to keep the map item frame and the page layout fixed
    #         currentMapExtent = composerMap.currentMapExtent()
    #         currentWidthHeightRatio = currentMapExtent.width() / currentMapExtent.height()
    #         newWidthHeightRatio = newExtent.width() / newExtent.height()
    #
    #         if currentWidthHeightRatio < newWidthHeightRatio :
    #             #enlarge height of new extent, ensuring the map center stays the same
    #             newHeight = newExtent.width() / currentWidthHeightRatio
    #             deltaHeight = newHeight - newExtent.height()
    #             newExtent.setYMinimum( newExtent.yMinimum() - deltaHeight / 2 )
    #             newExtent.setYMaximum( newExtent.yMaximum() + deltaHeight / 2 )
    #
    #         else:
    #             #enlarge width of new extent, ensuring the map center stays the same
    #             newWidth = currentWidthHeightRatio * newExtent.height()
    #             deltaWidth = newWidth - newExtent.width()
    #             newExtent.setXMinimum( newExtent.xMinimum() - deltaWidth / 2 )
    #             newExtent.setXMaximum( newExtent.xMaximum() + deltaWidth / 2 )
    #
    #         composerMap.beginCommand( "Map extent changed")
    #         composerMap.setNewExtent( newExtent )
    #         composerMap.endCommand()
    #         # composerMap.setNewScale(3500)
    #
            item.setFrameEnabled(True)
            item.setFrameOutlineWidth(1.0)
            item.setPreviewMode(QgsComposerMap.Render)
            item.updateCachedImage()

            item.setGridEnabled(True)
            item.setGridPenColor(QColor(255,255,255,0))
            item.setGridPenWidth(0.0)
            #item.setGridStyle(Qgsitem.FrameAnnotationsOnly)
            item.setGridIntervalX(1.0)
            item.setGridIntervalY(1.0)
    #         mySymbol1 = item.gridLineSymbol ()
    #         mySymbol1.setAlpha(0)
            #item.setGridLineSymbol(mySymbol1)
            item.setShowGridAnnotation(True)
            item.setGridAnnotationFormat(1)
            item.setGridAnnotationPrecision (0)
            item.setGridAnnotationDirection(1,0)
            item.setGridAnnotationDirection(1,1)
            item.setMapCanvas( define._canvas)#set canvas to composer map to have the possibility to draw canvas items
            mapWidget = QgsComposerMapWidget( None, item )
            item.setCacheUpdated(True)
            self.connect( self, SIGNAL( "zoomLevelChanged()" ), item, SLOT( "renderModeUpdateCachedImage()" ) )
            self.mItemWidgetMap.__setitem__( item.uuid(), mapWidget )
            # composerMap.setSelected(True)
            pass
        elif self.addItemName == "Label":
            labelWidget = QgsComposerLabelWidget( None, item )
            self.mItemWidgetMap.__setitem__( item.uuid(), labelWidget )
        elif self.addItemName == "Arrow":
            widget = QgsComposerArrowWidget( None, item )
            self.mItemWidgetMap.__setitem__( item.uuid(), widget )
        elif self.addItemName == "Shape":
            widget = QgsComposerShapeWidget( None, item )
            self.mItemWidgetMap.__setitem__( item.uuid(), widget );
        self.showItemOptions(item)
        self.mNewItems.append(item)

        self.addItemName = "Select"
    def addComposerArrow(self, arrow):
        self.addItemName = "Arrow"
    def addComposerHtmlFrame(self, html, frame):
        pass
    def addComposerLabel(self, label):
        self.addItemName = "Label"
    def addComposerMap(self, map):
        self.addItemName = "Map"
        # if ( not map ):
        #     return
        # if not isinstance(map, QgsComposerMap):
        #     map._class_ = QgsComposerMap
        # if not isinstance(map, QgsComposerMap):
        #     return
        # map.setMapCanvas( define._canvas)#set canvas to composer map to have the possibility to draw canvas items
        # mapWidget = QgsComposerMapWidget( self, map )
        # self.connect( self, SIGNAL( "zoomLevelChanged()" ), map, SLOT( "renderModeUpdateCachedImage()" ) )
        # self.mItemWidgetMap.__setitem__( map.uuid(), mapWidget )
        # pass


    def connectViewSlots(self):
        if ( not self.mView ):
            return

        self.connect( self.mView, SIGNAL( "selectedItemChanged( QgsComposerItem* )" ), self.showItemOptions)
        self.connect( self.mView, SIGNAL( "itemRemoved( QgsComposerItem* )" ), self.deleteItem)
        self.connect( self.mView, SIGNAL( "actionFinished()" ), self.setSelectionTool)

        # //listen out for position updates from the QgsComposerView
        self.connect( self.mView, SIGNAL( "cursorPosChanged( QPointF )" ), self.updateStatusCursorPos)
        self.connect( self.mView, SIGNAL( "zoomLevelChanged()" ), self.updateStatusZoom)
    def showItemOptions(self, item):

        currentWidget = self.mItemDock.widget()

        if ( not item):
            self.mItemDock.setWidget( None)
            return
        it = None
        try:
            it = self.mItemWidgetMap.get( item.uuid() )
        except:
            return
        # QMap<QgsComposerItem*, QWidget*>::const_iterator it = self.mItemWidgetMap.constFind( item )
        # if not ( len(self.mItemWidgetMap) > 0 and it == self.mItemWidgetMap.items()[len(self.mItemWidgetMap) - 1][1] ):
        #     return

        newWidget = it

        if ( not newWidget or newWidget == currentWidget ): #//bail out if new widget does not exist or is already there
            return

        self.mItemDock.setWidget( newWidget )
    def deleteItem(self, item):
        pass
    def updateStatusCursorPos(self, cursorPosition):
        if ( not self.mComposition ):
            return

        # //convert cursor position to position on current page
        pagePosition = self.mComposition.positionOnPage( cursorPosition )
        currentPage = self.mComposition.pageNumberForPoint( cursorPosition )

        self.mStatusCursorXLabel.setText( QString( "x: %1 mm" ).arg( pagePosition.x() ) )
        self.mStatusCursorYLabel.setText( QString( "y: %1 mm" ).arg( pagePosition.y() ) )
        self.mStatusCursorPageLabel.setText( QString( "page: %3" ).arg( currentPage ) )
    def updateStatusZoom(self):
        dpi = QgsApplication.desktop().logicalDpiX()
        # //monitor dpi is not always correct - so make sure the value is sane
        if (( dpi < 60 ) or ( dpi > 250 ) ):
            dpi = 72

        # //pixel width for 1mm on screen
        scale100 = float(dpi) / 25.4
        # //current zoomLevel
        zoomLevel = self.mView.transform().m11() * 100 / scale100

        self.mStatusZoomCombo.blockSignals( True )
        self.mStatusZoomCombo.lineEdit().setText( QString("%1%" ).arg( zoomLevel, 0, 'f', 1 ) )
        self.mStatusZoomCombo.blockSignals( False )
    def populatePrintComposersMenu(self):
        pass

    def disablePreviewMode(self):
        if ( not self.mView ):
            return
        self.mView.setPreviewModeEnabled( False )
    def activateGrayscalePreview(self):
        if ( not self.mView ):
            return
        self.mView.setPreviewMode( QgsPreviewEffect.PreviewGrayscale )
        self.mView.setPreviewModeEnabled( True )
    def activateMonoPreview(self):
        if ( not self.mView ):
            return
        self.mView.setPreviewMode( QgsPreviewEffect.PreviewMono )
        self.mView.setPreviewModeEnabled( True )
    def activateProtanopePreview(self):
        if ( not self.mView ):
            return
        self.mView.setPreviewMode( QgsPreviewEffect.PreviewProtanope )
        self.mView.setPreviewModeEnabled( True )
    def activateDeuteranopePreview(self):
        pass
    def mapCanvas(self):
        return define._canvas
    def view(self):
        return self.mView
    def atlasPageComboEditingFinished(self):
        text = self.mAtlasPageComboBox.lineEdit().text()

        # //find matching record in combo box
        page = -1 #//note - first page starts at 1, not 0
        for i in range(self.mAtlasPageComboBox.count()):
            if ( text.compare( self.mAtlasPageComboBox.itemData( i, Qt.UserRole + 1 ).toString(), Qt.CaseInsensitive ) == 0
                 or text.compare( self.mAtlasPageComboBox.itemData( i, Qt.UserRole + 2 ).toString(), Qt.CaseInsensitive ) == 0
                 or QString.number( i + 1 ) == text ):
                page = i + 1
                break
        ok = page > 0 

        if ( not ok or page > self.mComposition.atlasComposition().numFeatures() or page < 1 ):
            self.mAtlasPageComboBox.blockSignals( True )
            self.mAtlasPageComboBox.setCurrentIndex( self.mComposition.atlasComposition().currentFeatureNumber() )
            self.mAtlasPageComboBox.blockSignals( False )
        elif ( page != self.mComposition.atlasComposition().currentFeatureNumber() + 1 ):
            define._canvas.stopRendering()
            self.loadAtlasPredefinedScalesFromProject()
            self.mComposition.atlasComposition().prepareForFeature( page - 1 )
            self.emit(SIGNAL("atlasPreviewFeatureChanged()"))

    def statusZoomCombo_currentIndexChanged(self, index):
        selectedZoom = self.mStatusZoomLevelsList[len(self.mStatusZoomLevelsList) - index - 1 ]
        if ( self.mView ):
            self.mView.setZoomLevel( selectedZoom )
            # //update zoom combobox text for correct format (one decimal place, trailing % sign)
            self.mStatusZoomCombo.blockSignals( True )
            self.mStatusZoomCombo.lineEdit().setText( QString("%1%" ).arg( selectedZoom * 100.0, 0, 'f', 1 ) )
            self.mStatusZoomCombo.blockSignals( False )

    def statusZoomCombo_zoomEntered(self):
        if ( not self.mView ):
            return

        # //need to remove spaces and "%" characters from input text
        zoom = self.mStatusZoomCombo.currentText().remove( QChar( '%' ) ).trimmed()
        self.mView.setZoomLevel( zoom.toDouble() / 100 )
    def toggleRulers(self, checked):
        # //show or hide rulers
        self.mHorizontalRuler.setVisible( checked )
        self.mVerticalRuler.setVisible( checked )
        self.mRulerLayoutFix.setVisible( checked )

        myQSettings = QSettings()
        myQSettings.setValue( "/Composer/showRulers", checked )
    def setComposition(self, composition):
        if ( not composition ):
            return

        # //delete composition widget
        oldCompositionWidget = self.mGeneralDock.widget()
        # delete oldCompositionWidget

        self.deleteItemWidgets()

        # delete mComposition
        self.mComposition = composition

        self.connectCompositionSlots()
        self.createCompositionWidget()
        self.restoreGridSettings()
        self.setupUndoView()

        self.mActionShowPage.setChecked( self.mComposition.pagesVisible() )

        # //setup atlas composition widget
        # oldAtlasWidget = self.mAtlasDock.widget()
        # delete oldAtlasWidget
        # self.mAtlasDock.setWidget( QgsAtlasCompositionWidget( self.mAtlasDock, self.mComposition ) )

        # //set state of atlas controls
        atlasMap = self.mComposition.atlasComposition()
        self.toggleAtlasControls( atlasMap.enabled() )
        self.connect( atlasMap, SIGNAL( "toggled( bool )" ), self.toggleAtlasControls)
        self.connect( atlasMap, SIGNAL( "coverageLayerChanged( QgsVectorLayer* )" ), self.updateAtlasMapLayerAction)
        self.connect( atlasMap, SIGNAL( "numberFeaturesChanged( int )" ), self.updateAtlasPageComboBox)
        self.connect( atlasMap, SIGNAL( "featureChanged( QgsFeature* )" ), self.atlasFeatureChanged)

        self.mSetPageOrientation = False
        if ( self.mPrinter ):
        # //if printer has already been created then we need to reset the page orientation to match
        # //new composition
            self.setPrinterPageOrientation()
    def setupUndoView(self):
        if ( not self.mUndoView or not self.mComposition ):
            return
        
        # //init undo/redo buttons
        self.mActionUndo.setEnabled( False )
        self.mActionRedo.setEnabled( False )
        if ( self.mComposition.undoStack() ):
            self.mUndoView.setStack( self.mComposition.undoStack() )
            self.connect( self.mComposition.undoStack(), SIGNAL( "canUndoChanged( bool )" ), self.mActionUndo, SLOT( "setEnabled( bool )" ) )
            self.connect( self.mComposition.undoStack(), SIGNAL( "canRedoChanged( bool )" ), self.mActionRedo, SLOT( "setEnabled( bool )" ) )

    def deleteItemWidgets(self):
        self.mItemWidgetMap.clear()
    def dockVisibilityChanged(self, visible):
        pass
    def createComposerView(self):
        if ( not self.mViewLayout ):
            return

        # delete mView
        # mView = QgsComposerView()
        self.mView.setContentsMargins( 0, 0, 0, 0 )
        self.mView.setHorizontalRuler( self.mHorizontalRuler )
        self.mView.setVerticalRuler( self.mVerticalRuler )
        self.mViewLayout.addWidget( self.mView, 1, 1 )

        # //view does not accept focus via tab
        self.mView.setFocusPolicy( Qt.ClickFocus )
        # //instead, if view is focused and tab is pressed than mActionHidePanels is triggered,
        # //to toggle display of panels
        tab = QtGui.QShortcut( Qt.Key_Tab, self.mView )
        tab.setContext( Qt.WidgetWithChildrenShortcut )
        self.connect( tab, SIGNAL( "activated()" ),self.mActionHidePanels, SLOT( "trigger()" ) )
    def setupTheme(self):
        # //now set all the icons - getThemeIcon will fall back to default theme if its
        # //missing from active theme
        self.mActionQuit.setIcon(QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionFileExit.png"))
        self.mActionSaveProject.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionFileSave.svg" ) )
        self.mActionOpenProject.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionFileOpen.svg" ) )
        self.mActionNewComposer.setIcon(QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionNewComposer.svg"))
        self.mActionDuplicateComposer.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionDuplicateComposer.svg" ) )
        self.mActionComposerManager.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionComposerManager.svg" ) )
        self.mActionLoadFromTemplate.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionFileOpen.svg" ) )
        self.mActionSaveAsTemplate.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionFileSaveAs.svg" ) )
        self.mActionExportAsImage.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionSaveMapAsImage.png" ) )
        self.mActionExportAsSVG.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionSaveAsSVG.png" ) )
        self.mActionExportAsPDF.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionSaveAsPDF.png" ) )
        self.mActionPrint.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionFilePrint.png" ) )
        self.mActionZoomAll.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionZoomFullExtent.svg" ) )
        self.mActionZoomIn.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionZoomIn.svg" ) )
        self.mActionZoomOut.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionZoomOut.svg" ) )
        self.mActionZoomActual.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionZoomActual.svg" ) )
        self.mActionMouseZoom.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionZoomToArea.svg" ) )
        self.mActionRefreshView.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionDraw.svg" ) )
        self.mActionUndo.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionUndo.png" ) )
        self.mActionRedo.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionRedo.png" ) )
        self.mActionAddImage.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAddImage.svg" ) )
        self.mActionAddNewMap.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAddMap.svg" ) )
        self.mActionAddNewLabel.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionLabel.svg" ) )
        self.mActionAddNewLegend.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAddLegend.svg" ) )
        self.mActionAddNewScalebar.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionScaleBar.svg" ) )
        self.mActionAddRectangle.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAddBasicRectangle.svg" ) )
        self.mActionAddTriangle.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAddBasicTriangle.svg" ) )
        self.mActionAddEllipse.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAddBasicCircle.svg" ) )
        self.mActionAddArrow.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAddArrow.svg" ) )
        self.mActionAddTable.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAddTable.svg" ) )
        self.mActionAddAttributeTable.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAddTable.svg" ) )
        self.mActionAddHtml.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAddHtml.svg" ) )
        self.mActionSelectMoveItem.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionSelect.svg" ) )
        self.mActionMoveItemContent.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionMoveItemContent.svg" ) )
        self.mActionGroupItems.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionGroupItems.png" ) )
        self.mActionUngroupItems.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionUngroupItems.png" ) )
        self.mActionRaiseItems.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionRaiseItems.png" ) )
        self.mActionLowerItems.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionLowerItems.png" ) )
        self.mActionMoveItemsToTop.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionMoveItemsToTop.png" ) )
        self.mActionMoveItemsToBottom.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionMoveItemsToBottom.png" ) )
        self.mActionAlignLeft.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAlignLeft.png" ) )
        self.mActionAlignHCenter.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAlignHCenter.png" ) )
        self.mActionAlignRight.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAlignRight.png" ) )
        self.mActionAlignTop.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAlignTop.png" ) )
        self.mActionAlignVCenter.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAlignVCenter.png" ) )
        self.mActionAlignBottom.setIcon( QtGui.QIcon(self.currentDir + "/Resource/images/themes/default/mActionAlignBottom.png" ) )


    def open(self):
        if ( self.mFirstTime ):
            # //mComposition.createDefault()
            self.mFirstTime = False
            self.show()
            self.zoomFull() # zoomFull() does not work properly until we have called show()
            if ( self.mView ):
                self.mView.updateRulers()
        else:
            self.show() #make sure the window is displayed - with a saved project, it's possible to not have already called show()
            # //is that a bug?
            self.activate() #bring the composer window to the front
    def zoomFull( self ):
        if ( self.mView ):
            self.mView.fitInView( self.mComposition.sceneRect(), Qt.KeepAspectRatio )
    def activate(self):
        shown = self.isVisible()
        self.show()
        self.raise_()
        self.setWindowState( self.windowState() & ~Qt.WindowMinimized )
        self.activateWindow()
        if ( not shown ):
            self.on_mActionZoomAll_triggered()
    def on_mActionZoomAll_triggered(self):
        self.zoomFull()
        self.mView.updateRulers()
        self.mView.update()
        self.emit(SIGNAL("zoomLevelChanged()"))
    def on_mActionZoomIn_triggered(self):
        self.mView.scale( 2, 2 )
        self.mView.updateRulers()
        self.mView.update()
        self.emit(SIGNAL("zoomLevelChanged()"))
    def on_mActionZoomOut_triggered(self):
        self.mView.scale( .5, .5 )
        self.mView.updateRulers()
        self.mView.update()
        self.emit(SIGNAL("zoomLevelChanged()"))
    def on_mActionZoomActual_triggered(self):
        self.mView.setZoomLevel( 1.0 )
    def on_mActionMouseZoom_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.Zoom )
    def on_mActionRefreshView_triggered(self):
        if ( not self.mComposition ):
            return

        # //refresh atlas feature first, to update attributes
        if ( self.mComposition.atlasMode() == QgsComposition.PreviewAtlas ):
            # //block signals from atlas, since the later call to mComposition.refreshItems() will
            # //also trigger items to refresh atlas dependent properties
            self.mComposition.atlasComposition().blockSignals( True )
            self.mComposition.atlasComposition().refreshFeature()
            self.mComposition.atlasComposition().blockSignals( False )
        self.mComposition.refreshItems()
        self.mComposition.update()
    def on_mActionShowGrid_triggered(self, checked):
        if ( self.mComposition ):
            self.mComposition.setGridVisible( checked )
    def on_mActionSnapGrid_triggered(self, checked):
        if ( self.mComposition ):
            self.mComposition.setSnapToGridEnabled( checked )
    def on_mActionShowGuides_triggered(self, checked):
        if ( self.mComposition ):
            self.mComposition.setSnapLinesVisible( checked )
    def on_mActionSnapGuides_triggered(self, checked):
        if ( self.mComposition ):
            self.mComposition.setAlignmentSnap( checked )
    def on_mActionSmartGuides_triggered(self, checked):
        if ( self.mComposition ):
            self.mComposition.setSmartGuidesEnabled( checked )
    def on_mActionShowBoxes_triggered(self, checked):
        if ( self.mComposition ):
            self.mComposition.setBoundingBoxesVisible( checked )
    def on_mActionShowPage_triggered(self, checked):
        if ( self.mComposition ):
            self.mComposition.setPagesVisible( checked )
    def on_mActionClearGuides_triggered(self):
        if ( self.mComposition ):
            self.mComposition.clearSnapLines()
    # def on_mActionAtlasSettings_triggered(self):
    #     if ( not self.mAtlasDock.isVisible() ):
    #         self.mAtlasDock.show()
    #     self.mAtlasDock.raise_()
    def on_mActionToggleFullScreen_triggered(self):
        if ( self.mActionToggleFullScreen.isChecked() ):
            self.showFullScreen()
        else:
            self.showNormal()


    def on_mActionHidePanels_triggered(self):
        # /*
        # workaround the limited Qt dock widget API
        # see http://qt-project.org/forums/viewthread/1141/
        # and http://qt-project.org/faq/answer/how_can_i_check_which_tab_is_the_current_one_in_a_tabbed_qdockwidget
        # */

        showPanels = not self.mActionHidePanels.isChecked()
        docks = self.findChildren(QtGui.QDockWidget)
        tabBars = self.findChildren(QtGui.QTabBar)

        if ( not showPanels ):
            self.mPanelStatus.clear()
            # //record status of all docks

            for dock in docks:
                panelStatus = PanelStatus()
                panelStatus.setValue( dock.isVisible(), False )
                self.mPanelStatus.__setitem__( dock.windowTitle(), panelStatus )
                dock.setVisible( False )

            # //record active dock tabs
            for tabBar in tabBars:
                currentTabTitle = tabBar.tabText( tabBar.currentIndex() )
                self.mPanelStatus[ currentTabTitle ].isActive = True
        else:
            # //restore visibility of all docks
            for dock in docks:
                if ( not self.mPanelStatus.has_key(dock.windowTitle() ) ):
                    dock.setVisible( True )
                    continue
                dock.setVisible( self.mPanelStatus.get(dock.windowTitle() ).isVisible )

            # //restore previously active dock tabs
            for tabBar in tabBars:
                # //loop through all tabs in tab bar
                for i in range(tabBar.count()):
                    tabTitle = tabBar.tabText( i )
                    if ( self.mPanelStatus.get( tabTitle ).isActive ):
                        tabBar.setCurrentIndex( i )

    def on_mActionAtlasNext_triggered(self):
        atlasMap = self.mComposition.atlasComposition()
        if ( not atlasMap.enabled() ):
            return

        define._canvas.stopRendering()

        self.loadAtlasPredefinedScalesFromProject()
        atlasMap.nextFeature()
        self.emit(SIGNAL("atlasPreviewFeatureChanged()"))
    def on_mActionAtlasPrev_triggered(self):
        atlasMap = self.mComposition.atlasComposition()
        if ( not atlasMap.enabled() ):
            return

        define._canvas.stopRendering()

        self.loadAtlasPredefinedScalesFromProject()
        atlasMap.prevFeature()
        self.emit(SIGNAL("atlasPreviewFeatureChanged()"))
    def on_mActionAtlasFirst_triggered(self):
        atlasMap = self.mComposition.atlasComposition()
        if ( not atlasMap.enabled() ):
            return

        define._canvas.stopRendering()

        self.loadAtlasPredefinedScalesFromProject()
        atlasMap.firstFeature()
        self.emit(SIGNAL("atlasPreviewFeatureChanged()"))
    def on_mActionAtlasLast_triggered(self):
        atlasMap = self.mComposition.atlasComposition()
        if ( not atlasMap.enabled() ):
            return

        define._canvas.stopRendering()

        self.loadAtlasPredefinedScalesFromProject()
        atlasMap.lastFeature()
        self.emit(SIGNAL("atlasPreviewFeatureChanged()"))
    def on_mActionExportAtlasAsPDF_triggered(self):
        previousMode = self.mComposition.atlasMode()
        self.mComposition.setAtlasMode( QgsComposition.ExportAtlas )
        self.exportCompositionAsPDF( QgsComposerOutputMode.Atlas )
        self.mComposition.setAtlasMode( previousMode )

        if ( self.mComposition.atlasMode() == QgsComposition.PreviewAtlas ):
        # //after atlas output, jump back to preview first feature
            atlasMap = self.mComposition.atlasComposition()
            atlasMap.firstFeature()
    def on_mActionExportAsPDF_triggered(self):
        self.exportCompositionAsPDF( QgsComposerOutputMode.Single )

    def exportCompositionAsPDF( self, mode ):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        if ( not self.mComposition or not self.mView ):
            return

        # if ( self.containsWMSLayer() ):
        #     self.showWMSPrintingWarning()

        # if ( self.containsAdvancedEffects() ):
        #     self.showAdvancedEffectsWarning()

        # // If we are not printing as raster, temporarily disable advanced effects
        # // as QPrinter does not support composition modes and can result
        # // in items missing from the output
        if ( self.mComposition.printAsRaster() ):
            self.mComposition.setUseAdvancedEffects( True )
        else:
            self.mComposition.setUseAdvancedEffects( False )

        hasAnAtlas = self.mComposition.atlasComposition().enabled()
        atlasOnASingleFile = hasAnAtlas and self.mComposition.atlasComposition().singleFile()
        atlasMap = self.mComposition.atlasComposition()

        outputFileName = None
        outputDir = None

        if ( mode == QgsComposerOutputMode.Single or ( mode == QgsComposerOutputMode.Atlas and atlasOnASingleFile ) ):
            myQSettings = QSettings()   # where we keep last used filter in persistent state
            lastUsedFile = myQSettings.value( "/UI/lastSaveAsPdfFile", "qgis.pdf" ).toString()
            file = QFileInfo( lastUsedFile )

            if ( hasAnAtlas and not atlasOnASingleFile and
                 ( mode == QgsComposerOutputMode.Atlas or self.mComposition.atlasMode() == QgsComposition.PreviewAtlas ) ):
                outputFileName = QDir( file.path() ).filePath( atlasMap.currentFilename() ) + ".pdf"
            else:
                outputFileName = file.path()
            # #ifdef Q_OS_MAC
            # mQgis.activateWindow()
            # self.raise()
            # #endif
            outputFileName = QFileDialog.getSaveFileName(
                               self,
                               "Save composition as" ,
                               outputFileName,
                               "PDF Format"  + " (*.pdf *.PDF)" )
            self.activateWindow()
            if ( outputFileName.isEmpty() ):
                self.timeStart = time.time()
                return

            self.timeStart = time.time()

            if ( not outputFileName.endsWith( ".pdf", Qt.CaseInsensitive ) ):
                outputFileName += ".pdf"

            myQSettings.setValue( "/UI/lastSaveAsPdfFile", outputFileName )
        # // else, we need to choose a directory
        else:
            if ( atlasMap.filenamePattern().isEmpty() ):
                res = QMessageBox.warning( None, "Empty filename pattern" ,
                                              "The filename pattern is empty. A default one will be used." ,
                                              QMessageBox.Ok | QMessageBox.Cancel,
                                              QMessageBox.Ok )
                if ( res == QMessageBox.Cancel ):
                    return
                atlasMap.setFilenamePattern( "'output_'or@atlas_featurenumber" )

            myQSettings = QSettings() 
            lastUsedDir = myQSettings.value( "/UI/lastSaveAtlasAsPdfDir", QDir.homePath() ).toString()
            outputDir = QFileDialog.getExistingDirectory( self,
                        "Export atlas to directory" ,
                        lastUsedDir,
                        QFileDialog.ShowDirsOnly )
            if ( outputDir.isEmpty() ):
                return
            # // test directory (if it exists and is writable)
            if ( not QDir( outputDir ).exists() or not QFileInfo( outputDir ).isWritable() ):
                QMessageBox.warning( None, "Unable to write into the directory" ,
                                    "The given output directory is not writable. Cancelling." ,
                                    QMessageBox.Ok,
                                    QMessageBox.Ok )
                return

            myQSettings.setValue( "/UI/lastSaveAtlasAsPdfDir", outputDir )

        self.mView.setPaintingEnabled( False )

        if ( mode == QgsComposerOutputMode.Atlas ):
            printer = QtGui.QPrinter()

            painter = QtGui.QPainter()

            self.loadAtlasPredefinedScalesFromProject()
            if ( not  atlasMap.beginRender() and not atlasMap.featureFilterErrorString().isEmpty() ):
                QMessageBox.warning( self, "Atlas processing error" ,
                                    QString("Feature filter parser error: %1").arg( atlasMap.featureFilterErrorString()) ,
                                    QMessageBox.Ok,
                                    QMessageBox.Ok )
                self.mView.setPaintingEnabled( True )
                return
            if ( atlasOnASingleFile ):
                # //prepare for first feature, so that we know paper size to begin with
                atlasMap.prepareForFeature( 0 )
                self.mComposition.beginPrintAsPDF( printer, outputFileName )
                # // set the correct resolution
                self.mComposition.beginPrint( printer )
                printReady =  painter.begin( printer )
                if ( not printReady ):
                    QMessageBox.warning( self, "Atlas processing error" ,
                                          QString( "Error creating %1." ).arg( outputFileName ),
                                          QMessageBox.Ok,
                                          QMessageBox.Ok )
                    self.mView.setPaintingEnabled( True )
                    return

            progress = QtGui.QProgressDialog( "Rendering maps...", "Abort" , 0, atlasMap.numFeatures(), self )
            progress.setWindowTitle( "Exporting atlas" )
            QtGui.QApplication.setOverrideCursor( Qt.BusyCursor )

            for featureI in range(atlasMap.numFeatures()):
                progress.setValue( featureI )
                # // process input events in order to allow aborting
                QCoreApplication.processEvents()
                if ( progress.wasCanceled() ):
                    atlasMap.endRender()
                    break
                if ( not atlasMap.prepareForFeature( featureI ) ):
                    QMessageBox.warning( self, "Atlas processing error",
                                          "Atlas processing error",
                                          QMessageBox.Ok,
                                          QMessageBox.Ok )
                    self.mView.setPaintingEnabled( True )
                    QtGui.QApplication.restoreOverrideCursor()
                    return
                if ( not atlasOnASingleFile ):
                    # // bugs #7263 and #6856
                    # // QPrinter does not seem to be reset correctly and may cause generated PDFs (all except the first) corrupted
                    # // when transparent objects are rendered. We thus use a new QPrinter object here
                    multiFilePrinter = QtGui.QPrinter() 
                    outputFileName = QDir( outputDir ).filePath( atlasMap.currentFilename() ) + ".pdf"
                    self.mComposition.beginPrintAsPDF( multiFilePrinter, outputFileName )
                    # // set the correct resolution
                    self.mComposition.beginPrint( multiFilePrinter )
                    printReady = painter.begin( multiFilePrinter )
                    if ( not printReady ):
                        QMessageBox.warning( self, "Atlas processing error",
                                            QString( "Error creating %1." ).arg( outputFileName ),
                                            QMessageBox.Ok,
                                            QMessageBox.Ok )
                        self.mView.setPaintingEnabled( True )
                        QtGui.QApplication.restoreOverrideCursor()
                        return
                    self.mComposition.doPrint( multiFilePrinter, painter )
                    painter.end()
                else:
                # //start print on a new page if we're not on the first feature
                    self.mComposition.doPrint( printer, painter, featureI > 0 )
            atlasMap.endRender()
            if ( atlasOnASingleFile ):
                painter.end()
        else:
            exportOk = self.mComposition.exportAsPDF( outputFileName )
            if ( not exportOk ):
                QMessageBox.warning( self, "Atlas processing error",
                                    QString( "Error creating %1." ).arg( outputFileName ),
                                    QMessageBox.Ok,
                                    QMessageBox.Ok )
                self.mView.setPaintingEnabled( True )
                QtGui.QApplication.restoreOverrideCursor()
                return

        if ( not  self.mComposition.useAdvancedEffects() ):
        # //Switch advanced effects back on
            self.mComposition.setUseAdvancedEffects( True )
        self.mView.setPaintingEnabled( True )
        QtGui.QApplication.restoreOverrideCursor()

    def on_mActionPrint_triggered(self):
  # //print only current feature
        self.printComposition( QgsComposerOutputMode.Single )
    def on_mActionPrintAtlas_triggered(self):
        # //print whole atlas
        previousMode = self.mComposition.atlasMode()
        self.mComposition.setAtlasMode( QgsComposition.ExportAtlas )
        self.printComposition( QgsComposerOutputMode.Atlas )
        self.mComposition.setAtlasMode( previousMode )
    def containsAdvancedEffects(self):
        # // Check if composer contains any blend modes or flattened layers for transparency
        # item_it = self.mItemWidgetMap.constBegin();
        currentItem = None;
        currentMap = None;

        # for item_it in self.mItemWidgetMap:
        #     currentItem = item_it.key();
        #     # // Check composer item's blend mode
        #     if ( currentItem.blendMode() != QPainter.CompositionMode_SourceOver ):
        #         return True;
                # // If item is a composer map, check if it contains any advanced effects
            # currentMap._ = dynamic_cast<QgsComposerMap *>( currentItem );
            # if ( currentMap && currentMap->containsAdvancedEffects() )
            # {
            #     return true;
        return True;
    def printComposition( self, mode ):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        if ( not self.mComposition or not self.mView ):
            return
        # if ( self.containsWMSLayer() ):
        #     self.showWMSPrintingWarning()
        # if ( self.containsAdvancedEffects() ):
        #     self.showAdvancedEffectsWarning()

        # If we are not printing as raster, temporarily disable advanced effects
        # as QPrinter does not support composition modes and can result
        # in items missing from the output
        if ( self.mComposition.printAsRaster() ):
            self.mComposition.setUseAdvancedEffects( True )
        else:
            self.mComposition.setUseAdvancedEffects( False )

        #set printer page orientation
        self.setPrinterPageOrientation()

        printDialog = QtGui.QPrintDialog( self.printer(), None)
        if ( printDialog.exec_() != QtGui.QDialog.Accepted ):
            self.timeStart = time.time()
            return

        QtGui.QApplication.setOverrideCursor( Qt.BusyCursor )
        self.mView.setPaintingEnabled( False )

        atlasMap = self.mComposition.atlasComposition()
        if ( mode == QgsComposerOutputMode.Single ):
            self.mComposition.beginPrint( self.printer(), True )
            painter = QtGui.QPainter( self.printer() )
            self.mComposition.doPrint( self.printer(), painter)
            painter.end()
        else:
            #prepare for first feature, so that we know paper size to begin with
            atlasMap.prepareForFeature( 0 )

            self.mComposition.beginPrint( self.printer(), True )
            painter = QtGui.QPainter( self.printer() )

            self.loadAtlasPredefinedScalesFromProject()
            if ( not  atlasMap.beginRender() and not atlasMap.featureFilterErrorString().isEmpty() ):
                QMessageBox.warning( self, "Atlas processing error" ,
                                    QString("Feature filter parser error: %1").arg( atlasMap.featureFilterErrorString() ),
                                    QMessageBox.Ok,
                                    QMessageBox.Ok )
                self.mView.setPaintingEnabled( True )
                QtGui.QApplication.restoreOverrideCursor()
                return
            progress = QtGui.QProgressDialog( "Rendering maps...", "Abort", 0, atlasMap.numFeatures(), self )
            progress.setWindowTitle( "Exporting atlas" )

            for i in range(atlasMap.numFeatures()):
                progress.setValue( i )
                # process input events in order to allow cancelling
                QCoreApplication.processEvents()

                if ( progress.wasCanceled() ):
                    atlasMap.endRender()
                    break
                if ( not atlasMap.prepareForFeature( i ) ):
                    QMessageBox.warning( self, "Atlas processing error",
                                          "Atlas processing error",
                                          QMessageBox.Ok,
                                          QMessageBox.Ok )
                    self.mView.setPaintingEnabled( True )
                    QtGui.QApplication.restoreOverrideCursor()
                    return

                #start print on a new page if we're not on the first feature
                self.mComposition.doPrint( self.printer(), painter, i > 0 )
            atlasMap.endRender()
            painter.end()
        if ( not  self.mComposition.useAdvancedEffects() ):
            #Switch advanced effects back on
            self.mComposition.setUseAdvancedEffects( True )
        self.mView.setPaintingEnabled( True )
        QtGui.QApplication.restoreOverrideCursor()
        self.timeStart = time.time()
    def on_mActionExportAtlasAsImage_triggered(self):
        # //print whole atlas
        previousMode = self.mComposition.atlasMode()
        self.mComposition.setAtlasMode( QgsComposition.ExportAtlas )
        self.exportCompositionAsImage( QgsComposerOutputMode.Atlas )
        self.mComposition.setAtlasMode( previousMode )

        if ( self.mComposition.atlasMode() == QgsComposition.PreviewAtlas ):
        # //after atlas output, jump back to preview first feature
            atlasMap = self.mComposition.atlasComposition()
            atlasMap.firstFeature()
    def on_mActionExportAsImage_triggered(self):
        self.exportCompositionAsImage( QgsComposerOutputMode.Single )
    def exportCompositionAsImage( self, mode ):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        if ( not self.mComposition or not self.mView ):
            return

        # if ( self.containsWMSLayer() ):
        #     self.showWMSPrintingWarning()

        settings = QSettings() 

        # Image size
        width = int( self.mComposition.printResolution() * self.mComposition.paperWidth() / 25.4 )
        height = int( self.mComposition. printResolution() * self.mComposition.paperHeight() / 25.4 )
        dpi = self.mComposition.printResolution()

        memuse = width * height * 3 / 1000000  # pixmap + image
        # QgsDebugMsg( QString( "Image %1x%2" ).arg( width ).arg( height ) )
        # QgsDebugMsg( QString( "memuse = %1" ).arg( memuse ) )

        if ( memuse > 200 ):   # about 4500x4500
            answer = QMessageBox.warning( None, "Big image",
                                               "To create image %1x%2 requires about %3 MB of memory. Proceed?".format(str(width), str(height), str(memuse )),
                                               QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok )

            self.raise_()
            if ( answer == QMessageBox.Cancel ):
                return

        #get some defaults from the composition
        cropToContents = self.mComposition.customProperty( "imageCropToContents", False ).toBool()
        marginTop = self.mComposition.customProperty( "imageCropMarginTop", 0 ).toInt()[0]
        marginRight = self.mComposition.customProperty( "imageCropMarginRight", 0 ).toInt()[0]
        marginBottom = self.mComposition.customProperty( "imageCropMarginBottom", 0 ).toInt()[0]
        marginLeft = self.mComposition.customProperty( "imageCropMarginLeft", 0 ).toInt()[0]

        imageDlg = QgsComposerImageExportOptionsDialog( self )
        imageDlg.setImageSize( QSizeF( self.mComposition.paperWidth(), self.mComposition.paperHeight() ) )
        imageDlg.setResolution( self.mComposition.printResolution() )
        imageDlg.setCropToContents( cropToContents )
        imageDlg.setCropMargins( marginTop, marginRight, marginBottom, marginLeft )

        atlasMap = self.mComposition.atlasComposition()
        if ( mode == QgsComposerOutputMode.Single ):
            outputFileName = None

            if ( atlasMap.enabled() and self.mComposition.atlasMode() == QgsComposition.PreviewAtlas ):
                lastUsedDir = settings.value( "/UI/lastSaveAsImageDir", QDir.homePath() ).toString()
                outputFileName = QDir( lastUsedDir ).filePath( atlasMap.currentFilename() )

            fileNExt = QFileDialog.getSaveFileName(self, "Save composition as",QCoreApplication.applicationDirPath (),"PNG format (*.png *.PNG);;BMP format (*.bmp *.BMP);;ICO format (*.ico *.ICO);;JPEG format (*.jpeg *.JPEG);;JPG format (*.jpg *.JPG);;PPM format (*.ppm *.PPM);;TIF format (*.tif *.TIF);;TIFF format (*.tiff *.TIFF);;XBM format (*.xbm *.XBM);;XPM format (*.xpm *.XPM)")
            if fileNExt == "":
                return

            # QPair<QString, QString> fileNExt = QgisGui.getSaveAsImageName( self, tr( "Save composition as" ), outputFileName )
            self.activateWindow()

            # if ( fileNExt.first.isEmpty() )
            # {
            #     return
            # }

            if ( not imageDlg.exec_() ):
                self.timeStart = time.time()
                return
            self.timeStart = time.time()
            print self.timeStart
            cropToContents = imageDlg.cropToContents()
            marginTop, marginRight, marginBottom, marginLeft = imageDlg.getCropMargins()
            self.mComposition.setCustomProperty( "imageCropToContents", cropToContents )
            self.mComposition.setCustomProperty( "imageCropMarginTop", marginTop )
            self.mComposition.setCustomProperty( "imageCropMarginRight", marginRight )
            self.mComposition.setCustomProperty( "imageCropMarginBottom", marginBottom )
            self.mComposition.setCustomProperty( "imageCropMarginLeft", marginLeft )

            self.mView.setPaintingEnabled( False )

            worldFilePageNo = -1
            if ( self.mComposition.generateWorldFile() and self.mComposition.worldFileMap() ):
                worldFilePageNo = self.mComposition.worldFileMap().page() - 1

            for i in range(self.mComposition.numPages()):
                if ( not self.mComposition.shouldExportPage( i + 1 ) ):
                    continue

                # QImage image
                # QRectF bounds
                image = QtGui.QImage()
                bounds = QRectF()
                if ( cropToContents ):
                    if ( self.mComposition.numPages() == 1 ):
                      # single page, so include everything
                        bounds = self.mComposition.compositionBounds( True )
                    else:
                      # multi page, so just clip to items on current page
                        bounds = self.mComposition.pageItemBounds( i, True )
                    if ( bounds.width() <= 0 or bounds.height() <= 0 ):
                      #invalid size, skip page
                        continue
                    pixelToMm = 25.4 / self.mComposition.printResolution()
                    bounds = bounds.adjusted( -marginLeft * pixelToMm,
                                              -marginTop * pixelToMm,
                                              marginRight * pixelToMm,
                                              marginBottom * pixelToMm )
                    image = self.mComposition.renderRectAsRaster( bounds, QSize(), imageDlg.resolution() )
                else:
                    image = self.mComposition.printPageAsRaster( i, QSize( imageDlg.imageWidth(), imageDlg.imageHeight() ) )

                if ( image.isNull() ):
                    QMessageBox.warning( None, "Memory Allocation Error",
                                      QString("Trying to create image #%1( %2x%3 @ %4dpi ) may result in a memory overflow.\nPlease try a lower resolution or a smaller papersize").arg( i + 1 ).arg( width ).arg( height ).arg( dpi ),
                                      QMessageBox.Ok, QMessageBox.Ok )
                    self.mView.setPaintingEnabled( True )
                    return
                saveOk = False
                outputFilePath = ""
                if ( i == 0 ):
                    outputFilePath = fileNExt
                else:
                    fi = QFileInfo( fileNExt)
                    outputFilePath = fi.absolutePath() + '/' + fi.baseName() + '_' + QString.number( i + 1 ) + '.' + fi.suffix()
                fi = QFileInfo( fileNExt)
                fileExtension = fi.suffix()
                saveOk = image.save( outputFilePath)#, fileExtension.toLocal8Bit().constData() )

                if ( not saveOk ):
                    QMessageBox.warning( self, "Image export error",
                                          QString( "Error creating %1." ).arg( fileNExt ),
                                          QMessageBox.Ok,
                                          QMessageBox.Ok )
                    self.mView.setPaintingEnabled( True )
                    return

                if ( i == worldFilePageNo ):
                # should generate world file for self page
                    a = b = c = d = e = f = 0.0
                    if ( bounds.isValid() ):
                        a, b, c, d, e, f = self.mComposition.computeWorldFileParameters( bounds)
                    else:
                        a, b, c, d, e, f = self.mComposition.computeWorldFileParameters()

                    fi = QFileInfo( outputFilePath )
                    # build the world file name
                    outputSuffix = fi.suffix()
                    worldFileName = fi.absolutePath() + '/' + fi.baseName() + '.' + outputSuffix.at( 0 ) + outputSuffix.at( fi.suffix().size() - 1 ) + 'w'

                    self.writeWorldFile( worldFileName, a, b, c, d, e, f )
            self.mView.setPaintingEnabled( True )
        else:
            # else, it has an atlas to render, so a directory must first be selected
            if ( atlasMap.filenamePattern().isEmpty() ):
                res = QMessageBox.warning( None, "Empty filename pattern",
                                              "The filename pattern is empty. A default one will be used.",
                                              QMessageBox.Ok | QMessageBox.Cancel,
                                              QMessageBox.Ok )
                if ( res == QMessageBox.Cancel ):
                    return
                atlasMap.setFilenamePattern( "'output_'or@atlas_featurenumber" )

            myQSettings = QSettings()
            lastUsedDir = myQSettings.value( "/UI/lastSaveAtlasAsImagesDir", QDir.homePath() ).toString()
            lastUsedFormat = myQSettings.value( "/UI/lastSaveAtlasAsImagesFormat", "jpg" ).toString()

            dlg = QFileDialog( self, "Export atlas to directory")
            dlg.setFileMode( QFileDialog.Directory )
            dlg.setOption( QFileDialog.ShowDirsOnly, True )
            dlg.setDirectory( lastUsedDir )

            #
            # Build an augmented FileDialog with a combo box to select the output format
            box = QtGui.QComboBox()
            hlayout = QtGui.QHBoxLayout()
            widget = QtGui.QWidget()

            formats = QtGui.QImageWriter.supportedImageFormats()
            selectedFormat = 0
            for i in range(formats.size()):
                format0 = QString( formats.at( i ) )
                if ( format0 == lastUsedFormat ):
                    selectedFormat = i
                box.addItem( format0 )
            box.setCurrentIndex( selectedFormat )

            hlayout.setMargin( 0 )
            hlayout.addWidget( QtGui.QLabel( "Image format: ") )
            hlayout.addWidget( box )
            widget.setLayout( hlayout )
            dlg.layout().addWidget( widget )

            if ( not dlg.exec_() ):
                return
            s = dlg.selectedFiles()
            if ( s.size() < 1 or s.at( 0 ).isEmpty() ):
                return
            dir = s.at( 0 )
            format0 = box.currentText()
            fileExt = '.' + format0

            if ( dir.isEmpty() ):
                return
            # test directory (if it exists and is writable)
            if ( not QDir( dir ).exists() or not QFileInfo( dir ).isWritable() ):
                QMessageBox.warning( None, "Unable to write into the directory",
                                    "The given output directory is not writable. Cancelling.",
                                    QMessageBox.Ok,
                                    QMessageBox.Ok )
                return

            if ( not imageDlg.exec_() ):
                return

            cropToContents = imageDlg.cropToContents()
            imageDlg.getCropMargins( marginTop, marginRight, marginBottom, marginLeft )
            self.mComposition.setCustomProperty( "imageCropToContents", cropToContents )
            self.mComposition.setCustomProperty( "imageCropMarginTop", marginTop )
            self.mComposition.setCustomProperty( "imageCropMarginRight", marginRight )
            self.mComposition.setCustomProperty( "imageCropMarginBottom", marginBottom )
            self.mComposition.setCustomProperty( "imageCropMarginLeft", marginLeft )

            myQSettings.setValue( "/UI/lastSaveAtlasAsImagesDir", dir )

            # So, now we can render the atlas
            self.mView.setPaintingEnabled( False )
            QtGui.QApplication.setOverrideCursor( Qt.BusyCursor )

            self.loadAtlasPredefinedScalesFromProject()
            if ( not  atlasMap.beginRender() and not atlasMap.featureFilterErrorString().isEmpty() ):
                QMessageBox.warning( self, "Atlas processing error",
                                    QString( "Feature filter parser error: %1" ).arg( atlasMap.featureFilterErrorString() ),
                                    QMessageBox.Ok,
                                    QMessageBox.Ok )
                self.mView.setPaintingEnabled( True )
                QtGui.QApplication.restoreOverrideCursor()
                return

            progress = QtGui.QProgressDialog( "Rendering maps...", "Abort", 0, atlasMap.numFeatures(), self )
            progress.setWindowTitle("Exporting atlas")

            for feature in range(atlasMap.numFeatures()):
                progress.setValue( feature )
                # process input events in order to allow cancelling
                QCoreApplication.processEvents()

                if ( progress.wasCanceled() ):
                    atlasMap.endRender()
                    break
                if ( not  atlasMap.prepareForFeature( feature ) ):
                    QMessageBox.warning( self, "Atlas processing error",
                                          "Atlas processing error",
                                          QMessageBox.Ok,
                                          QMessageBox.Ok )
                    self.mView.setPaintingEnabled( True )
                    QtGui.QApplication.restoreOverrideCursor()
                    return

                filename = QDir( dir ).filePath( atlasMap.currentFilename() ) + fileExt

                worldFilePageNo = -1
                if ( self.mComposition.generateWorldFile() and self.mComposition.worldFileMap() ):
                    worldFilePageNo = self.mComposition.worldFileMap().page() - 1

                for i in range(self.mComposition.numPages()):
                    if ( not self.mComposition.shouldExportPage( i + 1 ) ):
                        continue

                    image = QtGui.QImage()
                    bounds = QRectF()
                    if ( cropToContents ):
                        if ( self.mComposition.numPages() == 1 ):
                        # single page, so include everything
                            bounds = self.mComposition.compositionBounds( True )
                        else:
                        # multi page, so just clip to items on current page
                            bounds = self.mComposition.pageItemBounds( i, True )
                        if ( bounds.width() <= 0 or bounds.height() <= 0 ):
                        #invalid size, skip page
                            continue
                        pixelToMm = 25.4 / self.mComposition.printResolution()
                        bounds = bounds.adjusted( -marginLeft * pixelToMm,
                                    -marginTop * pixelToMm,
                                    marginRight * pixelToMm,
                                    marginBottom * pixelToMm )
                        image = self.mComposition.renderRectAsRaster( bounds, QSize(), imageDlg.resolution() )
                    else:
                    #note - we can't safely use the preset width/height set in imageDlg here,
                    #as the atlas may have differing page size. So use resolution instead.
                        image = self.mComposition.printPageAsRaster( i, QSize(), imageDlg.resolution() )

                    imageFilename = filename

                    if ( i != 0 ):
                    #append page number
                        fi = QFileInfo( filename )
                        imageFilename = fi.absolutePath() + '/' + fi.baseName() + '_' + QString.number( i + 1 ) + '.' + fi.suffix()

                    saveOk = image.save( imageFilename)#, format0.toLocal8Bit().constData() )
                    if ( not saveOk ):
                        QMessageBox.warning( self, "Atlas processing error",
                                QString( "Error creating %1." ).arg( imageFilename ),
                                QMessageBox.Ok,
                                QMessageBox.Ok )
                        self.mView.setPaintingEnabled( True )
                        QtGui.QApplication.restoreOverrideCursor()
                        return

                    if ( i == worldFilePageNo ):
                    # should generate world file for self page
                    #     double a, b, c, d, e, f
                        if ( bounds.isValid() ):
                            a, b, c, d, e, f  = self.mComposition.computeWorldFileParameters( bounds)
                        else:
                            a, b, c, d, e, f  = self.mComposition.computeWorldFileParameters()

                        fi = QFileInfo( imageFilename )
                        # build the world file name
                        outputSuffix = fi.suffix()
                        worldFileName = fi.absolutePath() + '/' + fi.baseName() + '.' + outputSuffix.at( 0 ) + outputSuffix.at( fi.suffix().size() - 1 ) + 'w'

                        self.writeWorldFile( worldFileName, a, b, c, d, e, f )

            atlasMap.endRender()
            self.mView.setPaintingEnabled( True )
            QtGui.QApplication.restoreOverrideCursor()


    def on_mActionExportAtlasAsSVG_triggered(self):
        previousMode = self.mComposition.atlasMode()
        self.mComposition.setAtlasMode( QgsComposition.ExportAtlas )
        self.exportCompositionAsSVG( QgsComposerOutputMode.Atlas )
        self.mComposition.setAtlasMode( previousMode )

        if ( self.mComposition.atlasMode() == QgsComposition.PreviewAtlas ):
            # //after atlas output, jump back to preview first feature
            atlasMap = self.mComposition.atlasComposition()
            atlasMap.firstFeature()
    def on_mActionExportAsSVG_triggered(self):
        self.exportCompositionAsSVG( QgsComposerOutputMode.Single )
# // utility class that will hide all items until it's destroyed
# struct QgsItemTempHider
# {
#   explicit QgsItemTempHider( const QList<QGraphicsItem *> & items )
#   {
#     QList<QGraphicsItem *>::const_iterator it = items.begin()
#     for (  it != items.end() ++it )
#     {
#       mItemVisibility[*it] = ( *it ).isVisible()
#       ( *it ).hide()
#     }
#   }
#   void hideAll()
#   {
#     QgsItemVisibilityHash::const_iterator it = mItemVisibility.constBegin()
#     for (  it != mItemVisibility.constEnd() ++it ) it.key().hide()
#   }
#   ~QgsItemTempHider()
#   {
#     QgsItemVisibilityHash::const_iterator it = mItemVisibility.constBegin()
#     for (  it != mItemVisibility.constEnd() ++it )
#     {
#       it.key().setVisible( it.value() )
#     }
#   }
# private:
#   Q_DISABLE_COPY( QgsItemTempHider )
#   typedef QHash<QGraphicsItem*, bool> QgsItemVisibilityHash
#   QgsItemVisibilityHash mItemVisibility
# }
    def exportCompositionAsSVG(self, mode):
        # if ( self.containsWMSLayer() ):
        #     self.showWMSPrintingWarning()

        settingsLabel = "/UI/displaySVGWarning"
        settings = QSettings()

        displaySVGWarning = settings.value( settingsLabel, True ).toBool()

        if ( displaySVGWarning ):
            m = QgsMessageViewer( self )
            m.setWindowTitle(  "SVG warning" )
            m.setCheckBoxText(  "Don't show self message again")
            m.setCheckBoxState( Qt.Unchecked )
            m.setCheckBoxVisible( True )
            m.setCheckBoxQSettingsLabel( settingsLabel )
            m.setMessageAsHtml(  "<p>The SVG export function in QGIS has several "
                                "problems due to bugs and deficiencies in the "
                                +  "Qt4 svg code. In particular, there are problems "
                                "with layers not being clipped to the map "
                                "bounding box.</p>"
                                +  "If you require a vector-based output file from "
                                "Qgis it is suggested that you try printing "
                                "to PostScript if the SVG output is not "
                                "satisfactory."
                                "</p>" )
            m.exec_()

        atlasMap = self.mComposition.atlasComposition()

        outputFileName = ""
        outputDir = ""
        groupLayers = False
        prevSettingLabelsAsOutlines = QgsProject.instance().readBoolEntry( "PAL", "/DrawOutlineLabels", True )[0]
        clipToContent = False
        marginTop = 0.0
        marginRight = 0.0
        marginBottom = 0.0
        marginLeft = 0.0

        if ( mode == QgsComposerOutputMode.Single ):
            lastUsedFile = settings.value( "/UI/lastSaveAsSvgFile", "qgis.svg" ).toString()
            file0 = QFileInfo( lastUsedFile )

            if ( atlasMap.enabled() and self.mComposition.atlasMode() == QgsComposition.PreviewAtlas ):
                outputFileName = QDir( file0.path() ).filePath( atlasMap.currentFilename() ) + ".svg"
            else:
                outputFileName = file0.path()

            # open file dialog
            # #ifdef Q_OS_MAC
            # mQgis.activateWindow()
            # self.raise()
            # #endif
            outputFileName = QFileDialog.getSaveFileName(self,
                                                         "Save composition as" ,
                                                        outputFileName,
                                                         "SVG Format" + " (*.svg *.SVG)" )
            self.activateWindow()

            if ( outputFileName.isEmpty() ):
                return

            if ( not outputFileName.endsWith( ".svg", Qt.CaseInsensitive ) ):
                outputFileName += ".svg"

            settings.setValue( "/UI/lastSaveAsSvgFile", outputFileName )
        else:
            # If we have an Atlas
            if ( atlasMap.filenamePattern().isEmpty() ):
                res = QMessageBox.warning( None,  "Empty filename pattern" ,
                                         "The filename pattern is empty. A default one will be used.",
                                        QMessageBox.Ok | QMessageBox.Cancel,
                                        QMessageBox.Ok )
                if ( res == QMessageBox.Cancel ):
                    return
                atlasMap.setFilenamePattern( "'output_'or@atlas_featurenumber" )

            myQSettings = QSettings()
            lastUsedDir = myQSettings.value( "/UI/lastSaveAtlasAsSvgDir", QDir.homePath() ).toString()

            # open file dialog
            outputDir = QFileDialog.getExistingDirectory( self,
                                                         "Export atlas to directory" ,
                                                        lastUsedDir,
                                                        QFileDialog.ShowDirsOnly )

            if ( outputDir.isEmpty() ):
                return
            # test directory (if it exists and is writable)
            if ( not QDir( outputDir ).exists() or not QFileInfo( outputDir ).isWritable() ):
                QMessageBox.warning( None,  "Unable to write into the directory" ,
                                     "The given output directory is not writable. Cancelling." ,
                                    QMessageBox.Ok,
                                    QMessageBox.Ok )
                return
            myQSettings.setValue( "/UI/lastSaveAtlasAsSvgDir", outputDir )

        # open options dialog
        dialog = QtGui.QDialog()
        options = QgsSvgExportOptionsDialog()
        options.setupUi( dialog )
        options.chkTextAsOutline.setChecked( prevSettingLabelsAsOutlines )
        options.chkMapLayersAsGroup.setChecked( self.mComposition.customProperty( "svgGroupLayers", False ).toBool() )
        options.mClipToContentGroupBox.setChecked( self.mComposition.customProperty( "svgCropToContents", False ).toBool() )
        options.mTopMarginSpinBox.setValue( self.mComposition.customProperty( "svgCropMarginTop", 0 ).toInt()[0] )
        options.mRightMarginSpinBox.setValue( self.mComposition.customProperty( "svgCropMarginRight", 0 ).toInt()[0] )
        options.mBottomMarginSpinBox.setValue( self.mComposition.customProperty( "svgCropMarginBottom", 0 ).toInt()[0] )
        options.mLeftMarginSpinBox.setValue( self.mComposition.customProperty( "svgCropMarginLeft", 0 ).toInt()[0] )

        if ( dialog.exec_() != QtGui.QDialog.Accepted ):
            return

        groupLayers = options.chkMapLayersAsGroup.isChecked()
        clipToContent = options.mClipToContentGroupBox.isChecked()
        marginTop = options.mTopMarginSpinBox.value()
        marginRight = options.mRightMarginSpinBox.value()
        marginBottom = options.mBottomMarginSpinBox.value()
        marginLeft = options.mLeftMarginSpinBox.value()

        #save dialog settings
        self.mComposition.setCustomProperty( "svgGroupLayers", groupLayers )
        self.mComposition.setCustomProperty( "svgCropToContents", clipToContent )
        self.mComposition.setCustomProperty( "svgCropMarginTop", marginTop )
        self.mComposition.setCustomProperty( "svgCropMarginRight", marginRight )
        self.mComposition.setCustomProperty( "svgCropMarginBottom", marginBottom )
        self.mComposition.setCustomProperty( "svgCropMarginLeft", marginLeft )

        #temporarily override label draw outlines setting
        QgsProject.instance().writeEntry( "PAL", "/DrawOutlineLabels", options.chkTextAsOutline.isChecked() )

        self.mView.setPaintingEnabled( False )

        featureI = 0
        if ( mode == QgsComposerOutputMode.Atlas ):
            self.loadAtlasPredefinedScalesFromProject()
            if ( not  atlasMap.beginRender() and not atlasMap.featureFilterErrorString().isEmpty() ):
                QMessageBox.warning( self,  "Atlas processing error" ,
                                     QString("Feature filter parser error: %1" ).arg( atlasMap.featureFilterErrorString() ),
                                    QMessageBox.Ok,
                                    QMessageBox.Ok )
                self.mView.setPaintingEnabled( True )
                QgsProject.instance().writeEntry( "PAL", "/DrawOutlineLabels", prevSettingLabelsAsOutlines )
                return
        progress = QtGui.QProgressDialog(  "Rendering maps..." ,  "Abort" , 0, atlasMap.numFeatures(), self )
        progress.setWindowTitle(  "Exporting atlas" )

        while ( mode == QgsComposerOutputMode.Atlas and featureI < atlasMap.numFeatures() ):
            if ( mode == QgsComposerOutputMode.Atlas ):
                if ( atlasMap.numFeatures() == 0 ):
                    break

                progress.setValue( featureI )
                # process input events in order to allow aborting
                QCoreApplication.processEvents()
                if ( progress.wasCanceled() ):
                    atlasMap.endRender()
                    break
                if ( not atlasMap.prepareForFeature( featureI ) ):
                    QMessageBox.warning( self,  "Atlas processing error" ,
                                         "Atlas processing error" ,
                                        QMessageBox.Ok,
                                        QMessageBox.Ok )
                    self.mView.setPaintingEnabled( True )
                    QgsProject.instance().writeEntry( "PAL", "/DrawOutlineLabels", prevSettingLabelsAsOutlines )
                    return
                outputFileName = QDir( outputDir ).filePath( atlasMap.currentFilename() ) + ".svg"

            if ( not groupLayers ):
                for i in range(self.mComposition.numPages()):
                    if ( not self.mComposition.shouldExportPage( i + 1 ) ):
                        continue
                    generator = QSvgGenerator()
                    generator.setTitle( QgsProject.instance().title() )
                    currentFileName = outputFileName
                    if ( i == 0 ):
                        generator.setFileName( outputFileName )
                    else:
                        fi = QFileInfo( outputFileName )
                        currentFileName = fi.absolutePath() + '/' + fi.baseName() + '_' + QString.number( i + 1 ) + '.' + fi.suffix()
                        generator.setFileName( currentFileName )

                    bounds = QRectF()
                    if ( clipToContent ):
                        if ( self.mComposition.numPages() == 1 ):
                        # single page, so include everything
                            bounds = self.mComposition.compositionBounds( True )
                        else:
                        # multi page, so just clip to items on current page
                            bounds = self.mComposition.pageItemBounds( i, True )
                        bounds = bounds.adjusted( -marginLeft, -marginTop, marginRight, marginBottom )
                    else:
                        bounds = QRectF( 0, 0, self.mComposition.paperWidth(), self.mComposition.paperHeight() )

                    #width in pixel
                    width = int( bounds.width() * self.mComposition.printResolution() / 25.4 )
                    #height in pixel
                    height = int( bounds.height() * self.mComposition.printResolution() / 25.4 )
                    if ( width == 0 or height == 0 ):
                    #invalid size, skip self page
                        continue
                    generator.setSize( QSize( width, height ) )
                    generator.setViewBox( QRect( 0, 0, width, height ) )
                    generator.setResolution( self.mComposition.printResolution() ) #because the rendering is done in mm, convert the dpi

                    p = QtGui.QPainter()
                    createOk = p.begin( generator )
                    if ( not createOk ):
                        QMessageBox.warning( self,  "SVG export error" ,
                            QString(  "Error creating %1." ).arg( currentFileName ),
                            QMessageBox.Ok,
                            QMessageBox.Ok )
                        self.mView.setPaintingEnabled( True )
                        QgsProject.instance().writeEntry( "PAL", "/DrawOutlineLabels", prevSettingLabelsAsOutlines )
                        return

                    if ( clipToContent ):
                        self.mComposition.renderRect( p, bounds )
                    else:
                        self.mComposition.renderPage( p, i )
                    p.end()
            else:
                #width and height in pixel
                pageWidth = int( self.mComposition.paperWidth() * self.mComposition.printResolution() / 25.4 )
                pageHeight = int( self.mComposition.paperHeight() * self.mComposition.printResolution() / 25.4 )
                paperItems = self.mComposition.pages()

                for i in range(self.mComposition.numPages()):
                    if ( not self.mComposition.shouldExportPage( i + 1 ) ):
                        continue

                    width = pageWidth
                    height = pageHeight

                    bounds = QRectF()
                    if ( clipToContent ):
                        if ( self.mComposition.numPages() == 1 ):
                        # single page, so include everything
                            bounds = self.mComposition.compositionBounds( True )
                        else:
                        # multi page, so just clip to items on current page
                            bounds = self.mComposition.pageItemBounds( i, True )
                        bounds = bounds.adjusted( -marginLeft, -marginTop, marginRight, marginBottom )
                        width = bounds.width() * self.mComposition.printResolution() / 25.4
                        height = bounds.height() * self.mComposition.printResolution() / 25.4

                    if ( width == 0 or height == 0 ):
                    #invalid size, skip self page
                        continue

                    svg = QDomDocument()
                    svgDocRoot = QDomNode()
                    paperItem = paperItems[i]
                    paperRect = QRectF( paperItem.pos().x(),
                                        paperItem.pos().y(),
                                        paperItem.rect().width(),
                                        paperItem.rect().height() )

                    items = self.mComposition.items( paperRect,
                                                    Qt.IntersectsItemBoundingRect,
                                                    Qt.AscendingOrder )
                    it = items.last()
                    it._class_ = QgsPaperGrid
                    if ( not  items.isEmptiy()
                        and isinstance(it, QgsPaperGrid)
                        and not self.mComposition.gridVisible() ):
                        items.pop_back()
                    itemsHider = QgsItemTempHider( items )
                    composerItemLayerIdx = 0
                    it = items.begin()
                    svgLayerId = 1
                    # while it != items.end():
                    itNum = 0
                    while it != items.end():
                    # for itNum in range(items):
                        it = items.at(itNum)
                        if it == items.end():
                            break
                        itemsHider.hideAll()
                        it._class_ = QgsComposerItem
                        composerItem = it
                        # composerItem = dynamic_cast<QgsComposerItem*>( *it )
                        layerName = QString( "Layer " + QString.number( svgLayerId ) )
                        if ( isinstance(composerItem, QgsComposerItem) and composerItem.numberExportLayers() ):
                            composerItem.show()
                            composerItem.setCurrentExportLayer( composerItemLayerIdx )
                            composerItemLayerIdx += 1
                        else:
                        # show all items until the next item that renders on a separate layer
                            while it != items.end():
                                it = items.at(itNum)
                            # for (  it not = items.end() ++it )
                                it._class_ = QgsComposerMap
                                composerItem = it
                                # composerItem = dynamic_cast<QgsComposerMap*>( *it )
                                if ( isinstance(composerItem, QgsComposerMap) and composerItem.numberExportLayers() ):
                                    break
                                else:
                                    it.show()
                                itNum += 1

                        svgBuffer = QBuffer()
                        generator = QSvgGenerator()
                        generator.setTitle( QgsProject.instance().title() )
                        generator.setOutputDevice( svgBuffer )
                        generator.setSize( QSize( width, height ) )
                        generator.setViewBox( QRect( 0, 0, width, height ) )
                        generator.setResolution( self.mComposition.printResolution() ) #because the rendering is done in mm, convert the dpi

                        p = QtGui.QPainter( generator )
                        if ( clipToContent ):
                            self.mComposition.renderRect( p, bounds )
                        else:
                            self.mComposition.renderPage( p, i )
                        # post-process svg output to create groups in a single svg file
                        # we create inkscape layers since it's nice and clean and free
                        # and fully svg compatible
                        svgBuffer.close()
                        svgBuffer.open( QIODevice.ReadOnly )
                        doc = QDomDocument()
                        errorMsg = QString()
                        errorLine = 0
                        flag, errorMsg, errorLine, n = doc.setContent( svgBuffer, False)
                        if ( not  flag ):
                            QMessageBox.warning( None,  "SVG error" ,  "There was an error in SVG output for SVG layer "  + layerName +  " on page "  + QString.number( i + 1 ) + '(' + errorMsg + ')' )
                        if ( 1 == svgLayerId ):
                            svg = QDomDocument( doc.doctype() )
                            svg.appendChild( svg.importNode( doc.firstChild(), False ) )
                            svgDocRoot = svg.importNode( doc.elementsByTagName( "svg" ).at( 0 ), False )
                            svgDocRoot.toElement().setAttribute( "xmlns:inkscape", "http:#www.inkscape.org/namespaces/inkscape" )
                            svg.appendChild( svgDocRoot )
                        mainGroup = svg.importNode( doc.elementsByTagName( "g" ).at( 0 ), True )
                        mainGroup.toElement().setAttribute( "id", layerName )
                        mainGroup.toElement().setAttribute( "inkscape:label", layerName )
                        mainGroup.toElement().setAttribute( "inkscape:groupmode", "layer" )
                        defs = svg.importNode( doc.elementsByTagName( "defs" ).at( 0 ), True )
                        svgDocRoot.appendChild( defs )
                        svgDocRoot.appendChild( mainGroup )

                        if ( isinstance(composerItem, QgsComposerItem) and composerItem.numberExportLayers() and composerItem.numberExportLayers() == composerItemLayerIdx ): # restore and pass to next item
                            composerItem.setCurrentExportLayer()
                            composerItemLayerIdx = 0
                            itNum += 1
                        svgLayerId += 1
                    fi = QFileInfo( outputFileName )
                    currentFileName = outputFileName if(i == 0) else fi.absolutePath() + '/' + fi.baseName() + '_' + QString.number( i + 1 ) + '.' + fi.suffix()
                    out = QFile( currentFileName )
                    openOk = out.open( QIODevice.WriteOnly | QIODevice.Text )
                    if ( not openOk ):
                        QMessageBox.warning( self,  "SVG export error" ,
                                            QString(  "Error creating %1." ).arg( currentFileName ),
                                            QMessageBox.Ok,
                                            QMessageBox.Ok )
                        self.mView.setPaintingEnabled( True )
                        QgsProject.instance().writeEntry( "PAL", "/DrawOutlineLabels", prevSettingLabelsAsOutlines )
                        return

                    out.write( svg.toByteArray() )
            featureI += 1
        # while ( mode == QgsComposer.Atlas and featureI < atlasMap.numFeatures() )

        if ( mode == QgsComposerOutputMode.Atlas ):
            atlasMap.endRender()

        self.mView.setPaintingEnabled( True )
        QgsProject.instance().writeEntry( "PAL", "/DrawOutlineLabels", prevSettingLabelsAsOutlines )

    def on_mActionSelectMoveItem_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.Select )

    def on_mActionAddNewMap_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.AddMap )


    def on_mActionAddNewLegend_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.AddLegend )

    def on_mActionAddNewLabel_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.AddLabel )


    def on_mActionAddNewScalebar_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.AddScalebar )

    def on_mActionAddImage_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.AddPicture )

    def on_mActionAddRectangle_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.AddRectangle )

    def on_mActionAddTriangle_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.AddTriangle )

    def on_mActionAddEllipse_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.AddEllipse )

    def on_mActionAddTable_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.AddTable )

    def on_mActionAddAttributeTable_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.AddAttributeTable )

    def on_mActionAddHtml_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.AddHtml )

    def on_mActionAddArrow_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.AddArrow )

    def on_mActionSaveProject_triggered(self):
        # self.parent().saveProj()
        print "Save Project"

    def on_mActionOpenProject_triggered(self):
        print "Open Project"
    def on_mActionNewComposer_triggered(self):
        pass
        # title = None
        # if ( !mQgis.uniqueComposerTitle( this, title, true ) ):
        #     return
        # mQgis.createNewComposer( title )
    def on_mActionDuplicateComposer_triggered(self):
        pass
        # newTitle
        # if ( !mQgis.uniqueComposerTitle( this, newTitle, false, title() + tr( " copy" ) ) )
        # {
        # return
        # }
        #
        # // provide feedback, since loading of template into duplicate composer will be hidden
        # QDialog* dlg = new QgsBusyIndicatorDialog( tr( "Duplicating composer..." ) )
        # dlg.setStyleSheet( mQgis.styleSheet() )
        # dlg.show()
        #
        # QgsComposer* newComposer = mQgis.duplicateComposer( this, newTitle )
        #
        # dlg.close()
        # delete dlg
        # dlg = nullptr
        #
        # if ( !newComposer )
        # {
        # QMessageBox::warning( this, tr( "Duplicate Composer" ),
        #                   tr( "Composer duplication failed." ) )
        # }
    def on_mActionComposerManager_triggered(self):
        # // NOTE: on_mActionSaveAsTemplate_triggeredgleShot( 0, mQgis.actionShowComposerManager(), SLOT( trigger() ) )
        pass
    def on_mActionSaveAsTemplate_triggered(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        #show file dialog
        settings = QSettings()
        lastSaveDir = settings.value( "UI/lastComposerTemplateDir", QDir.homePath() ).toString()
        # #ifdef Q_OS_MAC
        # mQgis.activateWindow()
        # this.raise()
        # #endif
        saveFileName = QFileDialog.getSaveFileName(self,
                                                   "Save Composer Project",
                                                   lastSaveDir,
                                                   "Composer Project"  + " (*.qpt *.QPT)" )
        if ( saveFileName.isEmpty() ):
            self.timeStart = time.time()
            return

        saveFileInfo = QFileInfo( saveFileName )
        #check if suffix has been added
        if ( saveFileInfo.suffix().isEmpty() ):
            saveFileNameWithSuffix = saveFileName.append( ".qpt" )
            saveFileInfo = QFileInfo( saveFileNameWithSuffix )
        settings.setValue( "UI/lastComposerTemplateDir", saveFileInfo.absolutePath() )

        templateFile = QFile( saveFileName )
        if ( not templateFile.open( QIODevice.WriteOnly ) ):
            self.timeStart = time.time()
            return

        saveDocument = QDomDocument() 
        self.templateXML( saveDocument )

        if ( templateFile.write( saveDocument.toByteArray() ) == -1 ):
            QMessageBox.warning( None, "Save error" , "Error, could not save file"  )
        else:
            f = templateFile.flush()
            templateFile.close()
            doc = QDomDocument()
            qFile = QFile(saveFileName)
            if qFile.open(QFile.ReadWrite):
                doc.setContent(qFile)
                qFile.close()
            else:
                raise UserWarning, "can not open file:" + saveFileName
            domNodeList = doc.elementsByTagName("Composition")
            compositionNode = domNodeList.item(0)

            tableElem = doc.createElement("Table")

            graphicsProxyWidgetElem = doc.createElement("QGraphicsProxyWidget")
            graphicsProxyWidgetElem.setAttribute("x", int(self.gpw.pos().x()))
            graphicsProxyWidgetElem.setAttribute("y", int(self.gpw.pos().y()))
            graphicsProxyWidgetElem.setAttribute("fontSize", int(self.gpw.font().pixelSize()))
            tableElem.appendChild(graphicsProxyWidgetElem)

            tableViewElem = doc.createElement("QTableView")
            tableViewElem.setAttribute("width", int(self.mTblView.width()))
            tableViewElem.setAttribute("height", int(self.mTblView.height()))
            tableElem.appendChild(tableViewElem)

            spanDatElem = doc.createElement("SpanData")
            spanDatElem.setAttribute("row", 0)
            spanDatElem.setAttribute("column", 0)
            spanDatElem.setAttribute("rowSpanCount", 1)
            spanDatElem.setAttribute("columnSpanCount", int(self.data["CatOfAcftCount"][0]) + 3)
            tableViewElem.appendChild(spanDatElem)

            spanDatElem = doc.createElement("SpanData")
            spanDatElem.setAttribute("row", 1)
            spanDatElem.setAttribute("column", 0)
            spanDatElem.setAttribute("rowSpanCount", 1)
            spanDatElem.setAttribute("columnSpanCount", 3)
            tableViewElem.appendChild(spanDatElem)

            if self.data["Template"][0] >= 0 and int(self.data["Template"][0]) <= 4:
                spanDatElem = doc.createElement("SpanData")
                spanDatElem.setAttribute("row", 2)
                spanDatElem.setAttribute("column", 0)
                spanDatElem.setAttribute("rowSpanCount", 1)
                spanDatElem.setAttribute("columnSpanCount", 3)
                tableViewElem.appendChild(spanDatElem)

                spanDatElem = doc.createElement("SpanData")
                spanDatElem.setAttribute("row", 2)
                spanDatElem.setAttribute("column", 3)
                spanDatElem.setAttribute("rowSpanCount", 1)
                spanDatElem.setAttribute("columnSpanCount", int(self.data["CatOfAcftCount"][0]))
                tableViewElem.appendChild(spanDatElem)

                spanDatElem = doc.createElement("SpanData")
                spanDatElem.setAttribute("row", 3)
                spanDatElem.setAttribute("column", 0)
                spanDatElem.setAttribute("rowSpanCount", 1)
                spanDatElem.setAttribute("columnSpanCount", int(self.data["CatOfAcftCount"][0]) + 3)
                tableViewElem.appendChild(spanDatElem)

                spanDatElem = doc.createElement("SpanData")
                spanDatElem.setAttribute("row", 4)
                spanDatElem.setAttribute("column", 0)
                spanDatElem.setAttribute("rowSpanCount", 1)
                spanDatElem.setAttribute("columnSpanCount", 3)
                tableViewElem.appendChild(spanDatElem)

                spanDatElem = doc.createElement("SpanData")
                spanDatElem.setAttribute("row", 5)
                spanDatElem.setAttribute("column", 0)
                spanDatElem.setAttribute("rowSpanCount", 1)
                spanDatElem.setAttribute("columnSpanCount", 3)
                tableViewElem.appendChild(spanDatElem)

                spanDatElem = doc.createElement("SpanData")
                spanDatElem.setAttribute("row", 6)
                spanDatElem.setAttribute("column", 0)
                spanDatElem.setAttribute("rowSpanCount", 1)
                spanDatElem.setAttribute("columnSpanCount", 3)
                tableViewElem.appendChild(spanDatElem)
            else:
                spanDatElem = doc.createElement("SpanData")
                spanDatElem.setAttribute("row", 2)
                spanDatElem.setAttribute("column", 0)
                spanDatElem.setAttribute("rowSpanCount", 1)
                spanDatElem.setAttribute("columnSpanCount", 3)
                tableViewElem.appendChild(spanDatElem)

                spanDatElem = doc.createElement("SpanData")
                spanDatElem.setAttribute("row", 3)
                spanDatElem.setAttribute("column", 0)
                spanDatElem.setAttribute("rowSpanCount", 1)
                spanDatElem.setAttribute("columnSpanCount", 3)
                tableViewElem.appendChild(spanDatElem)

                spanDatElem = doc.createElement("SpanData")
                spanDatElem.setAttribute("row", 4)
                spanDatElem.setAttribute("column", 0)
                spanDatElem.setAttribute("rowSpanCount", 1)
                spanDatElem.setAttribute("columnSpanCount", 3)
                tableViewElem.appendChild(spanDatElem)

                spanDatElem = doc.createElement("SpanData")
                spanDatElem.setAttribute("row", 5)
                spanDatElem.setAttribute("column", 0)
                spanDatElem.setAttribute("rowSpanCount", 1)
                spanDatElem.setAttribute("columnSpanCount", 3)
                tableViewElem.appendChild(spanDatElem)

                spanDatElem = doc.createElement("SpanData")
                spanDatElem.setAttribute("row", 6)
                spanDatElem.setAttribute("column", 0)
                spanDatElem.setAttribute("rowSpanCount", 1)
                spanDatElem.setAttribute("columnSpanCount", 3)
                tableViewElem.appendChild(spanDatElem)
            spanDatElem = doc.createElement("SpanData")
            spanDatElem.setAttribute("row", 0)
            spanDatElem.setAttribute("column", int(self.data["CatOfAcftCount"][0]) + 3)
            spanDatElem.setAttribute("rowSpanCount", 1)
            spanDatElem.setAttribute("columnSpanCount", 9)
            tableViewElem.appendChild(spanDatElem)

            spanDatElem = doc.createElement("SpanData")
            spanDatElem.setAttribute("row", 1)
            spanDatElem.setAttribute("column", int(self.data["CatOfAcftCount"][0]) + 3)
            spanDatElem.setAttribute("rowSpanCount", 1)
            spanDatElem.setAttribute("columnSpanCount", 2)
            tableViewElem.appendChild(spanDatElem)

            spanDatElem = doc.createElement("SpanData")
            spanDatElem.setAttribute("row", 2)
            spanDatElem.setAttribute("column", int(self.data["CatOfAcftCount"][0]) + 3)
            spanDatElem.setAttribute("rowSpanCount", 1)
            spanDatElem.setAttribute("columnSpanCount", 2)
            tableViewElem.appendChild(spanDatElem)

            spanDatElem = doc.createElement("SpanData")
            spanDatElem.setAttribute("row", 2)
            spanDatElem.setAttribute("column", int(self.data["CatOfAcftCount"][0]) + 3)
            spanDatElem.setAttribute("rowSpanCount", 1)
            spanDatElem.setAttribute("columnSpanCount", 2)
            tableViewElem.appendChild(spanDatElem)

            spanDatElem = doc.createElement("SpanData")
            spanDatElem.setAttribute("row", 3)
            spanDatElem.setAttribute("column", int(self.data["CatOfAcftCount"][0]) + 3)
            spanDatElem.setAttribute("rowSpanCount", 1)
            spanDatElem.setAttribute("columnSpanCount", 2)
            tableViewElem.appendChild(spanDatElem)

            spanDatElem = doc.createElement("SpanData")
            spanDatElem.setAttribute("row", 4)
            spanDatElem.setAttribute("column", int(self.data["CatOfAcftCount"][0]) + 3)
            spanDatElem.setAttribute("rowSpanCount", 1)
            spanDatElem.setAttribute("columnSpanCount", 2)
            tableViewElem.appendChild(spanDatElem)

            spanDatElem = doc.createElement("SpanData")
            spanDatElem.setAttribute("row", 5)
            spanDatElem.setAttribute("column", int(self.data["CatOfAcftCount"][0]) + 3)
            spanDatElem.setAttribute("rowSpanCount", 1)
            spanDatElem.setAttribute("columnSpanCount", 2)
            tableViewElem.appendChild(spanDatElem)

            spanDatElem = doc.createElement("SpanData")
            spanDatElem.setAttribute("row", 6)
            spanDatElem.setAttribute("column", int(self.data["CatOfAcftCount"][0]) + 3)
            spanDatElem.setAttribute("rowSpanCount", 1)
            spanDatElem.setAttribute("columnSpanCount", 2)
            tableViewElem.appendChild(spanDatElem)

            stdModelElem = doc.createElement("QStandardItemModel")
            tableElem.appendChild(stdModelElem)

            for i in range(self.mStdModel.rowCount()):
                for j in range(self.mStdModel.columnCount()):
                    item = self.mStdModel.item(i, j)

                    itemElem = doc.createElement("Item")
                    itemElem.setAttribute("row", i)
                    itemElem.setAttribute("column", j)
                    if item != None and item.text() != "":
                        itemElem.setAttribute("text", item.text())
                    else:
                        itemElem.setAttribute("text", "")
                    stdModelElem.appendChild(itemElem)

            compositionNode.appendChild(tableElem)
            otherDataElem = doc.createElement("OtherData")
            compositionNode.appendChild(otherDataElem)
            d = dict()
            d.iteritems()
            for key, val in self.data.iteritems():
                elem = doc.createElement(key)
                otherDataElem.appendChild(elem)

                if isinstance(val, list):
                    for i in range(len(val)):
                        elem0 = doc.createElement("val" + str(i))
                        elem0.appendChild(doc.createTextNode(str(val[i])))
                        elem.appendChild(elem0)

                else:
                    elem.appendChild(doc.createTextNode(str(val)))


            qFile = QFile( saveFileName )
            if ( not qFile.open( QIODevice.WriteOnly ) ):
                self.timeStart = time.time()
                return
            qFile.write( doc.toByteArray() )

            i = 0
        self.timeStart = time.time()
    def on_mActionLoadFromTemplate_triggered(self):
        self.loadTemplate( False )
    def loadTemplate( self, newComposer ):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        settings = QSettings()
        openFileDir = settings.value( "UI/lastComposerTemplateDir", QDir.homePath() ).toString()
        openFileString = QFileDialog.getOpenFileName( None,  "Load Composer Project" , openFileDir, "*.qpt" )

        if ( openFileString.isEmpty() ):
            self.timeStart = time.time()
            return #canceled by the user

        openFileInfo = QFileInfo( openFileString )
        settings.setValue( "UI/LastComposerTemplateDir", openFileInfo.absolutePath() )

        templateFile = QFile( openFileString )
        if ( not templateFile.open( QIODevice.ReadOnly ) ):
            QMessageBox.warning( self,  "Read error" ,  "Error, could not read file"  )
            self.timeStart = time.time()
            return

        # c = self
        # comp = self.mComposition
        mapRenderer = define._canvas.mapRenderer()
        comp = QgsComposition(mapRenderer)
        comp.setPlotStyle(QgsComposition.Preview)

        if ( comp ):
            templateDoc = QDomDocument()
            if ( templateDoc.setContent( templateFile ) ):
                compElem = templateDoc.elementsByTagName("Composition").item(0).toElement()
                paperWidth = int(compElem.attribute("paperWidth"))
                paperHeight = int(compElem.attribute("paperHeight"))
                comp.setPaperSize(paperWidth, paperHeight)

                otherDataNode = compElem.elementsByTagName("OtherData").item(0)
                otherDataFirstNode = otherDataNode.firstChild()
                self.data = dict()

                node0 = otherDataFirstNode.firstChild()
                i = 0
                subDataList = []
                while True:
                    node0 = node0.nextSibling()
                    if node0 == None or node0.nodeName() == "":
                        break
                    subDataList.append(node0.toElement().text())
                    i += 1
                if i == 0:
                    self.data.__setitem__(str(otherDataFirstNode.nodeName()), otherDataFirstNode.toElement().text())
                else:
                    subDataList.insert(0, otherDataFirstNode.firstChild().toElement().text())
                    self.data.__setitem__(str(otherDataFirstNode.nodeName()), subDataList)
                node1 = otherDataFirstNode
                while True:
                    node1 = node1.nextSibling()
                    if node1 == None or node1.nodeName() == "":
                        break

                    node2 = node1.firstChild()
                    i = 0
                    subDataList = []
                    while True:
                        node2 = node2.nextSibling()
                        if node2 == None or node2.nodeName() == "":
                            break
                        subDataList.append(node2.toElement().text())
                        i += 1
                    if i == 0:
                        self.data.__setitem__(str(node1.nodeName()), node1.toElement().text())
                    else:
                        subDataList.insert(0, node1.firstChild().toElement().text())
                        self.data.__setitem__(str(node1.nodeName()), subDataList)



                # try:
                tableElem = compElem.elementsByTagName("Table").item(0).toElement()
                graphicsProxyWidgetElem = tableElem.elementsByTagName("QGraphicsProxyWidget").item(0).toElement()


                tableViewElem = tableElem.elementsByTagName("QTableView").item(0).toElement()

                self.mTblView = QTableView()
                tableHeight = int(tableViewElem.attribute("height"))
                tableWidth = int(tableViewElem.attribute("width"))
                self.mTblView.setFixedWidth(int(tableViewElem.attribute("width")))
                self.mTblView.setFixedHeight(int(tableViewElem.attribute("height")))
                self.mTblView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.mTblView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                hHeder = self.mTblView.horizontalHeader()
                hHeder.setVisible(False)
                vHeder = self.mTblView.verticalHeader()
                vHeder.setVisible(False)

                stdModelElem = tableElem.elementsByTagName("QStandardItemModel").item(0).toElement()
                itemNodeList = stdModelElem.elementsByTagName("Item")
                count = itemNodeList.count()

                self.mStdModel = QStandardItemModel()
                for i in range(7):
                    for j in range(12 + int(self.data["CatOfAcftCount"][0])):
                        item = QStandardItem("")
                        item.setEditable(True)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.mStdModel.setItem(i, j, item)
                for i in range(count):
                    itemElem = itemNodeList.item(i).toElement()
                    self.mStdModel.setItem(int(itemElem.attribute("row")), int(itemElem.attribute("column")), QStandardItem(itemElem.attribute("text")))
                self.mTblView.setModel(self.mStdModel)
                # self.mTableView.setModel(self.mStdModel)

                for i in range(7):
                    self.mTblView.setRowHeight(i, int(tableHeight / 7))
                for j in range(12 + int(self.data["CatOfAcftCount"][0])):
                    self.mTblView.setColumnWidth(j, int(tableWidth / float(12 + int(self.data["CatOfAcftCount"][0]))))
                    # self.mTableView.setColumnWidth(j, int(tableWidth / float(12 + self.data["CatOfAcftCount"][0])))

                itemSpanDataNodeList = tableViewElem.elementsByTagName("SpanData")
                spanDataCount = itemSpanDataNodeList.count()
                for i in range(spanDataCount):
                    itemElem = itemSpanDataNodeList.item(i).toElement()
                    self.mTblView.setSpan(int(itemElem.attribute("row")), int(itemElem.attribute("column")), int(itemElem.attribute("rowSpanCount")), int(itemElem.attribute("columnSpanCount")))
                    # self.mTableView.setSpan(int(itemElem.attribute("row")), int(itemElem.attribute("column")), int(itemElem.attribute("rowSpanCount")), int(itemElem.attribute("columnSpanCount")))

                self.gpw = QGraphicsProxyWidget()
                self.gpw.setWidget(self.mTblView)
                self.gpw.setPos(int(graphicsProxyWidgetElem.attribute("x")), int(graphicsProxyWidgetElem.attribute("y")))
                font = QFont()
                font.setPixelSize(int(graphicsProxyWidgetElem.attribute("fontSize")))
                self.gpw.setFont(font)

                comp.addItem(self.gpw)
                # except:
                #     pass


                # provide feedback, since composer will be hidden when loading template (much faster)
                dlg = QgsBusyIndicatorDialog(  "Loading template into composer..." )
                # dlg.setStyleSheet( mQgis.styleSheet() )
                dlg.show()

                # c.setUpdatesEnabled( False )
                comp.loadFromTemplate( templateDoc, None, False, newComposer )
                # c.setUpdatesEnabled( True )
                self.mComposition = comp
                # self.mView.setComposition(self.mComposition)
                dlg.close()
                # delete dlg
                dlg = None
                composerMapItems = self.mComposition.composerMapItems()
                for composerMap in composerMapItems:
                    renderer = composerMap.mapRenderer()
                    newExtent = renderer.extent()

                    #Make sure the width/height ratio is the same as in current composer map extent.
                    #This is to keep the map item frame and the page layout fixed
                    currentMapExtent = composerMap.currentMapExtent()
                    currentWidthHeightRatio = currentMapExtent.width() / currentMapExtent.height()
                    newWidthHeightRatio = newExtent.width() / newExtent.height()

                    if currentWidthHeightRatio < newWidthHeightRatio :
                        #enlarge height of new extent, ensuring the map center stays the same
                        newHeight = newExtent.width() / currentWidthHeightRatio
                        deltaHeight = newHeight - newExtent.height()
                        newExtent.setYMinimum( newExtent.yMinimum() - deltaHeight / 2 )
                        newExtent.setYMaximum( newExtent.yMaximum() + deltaHeight / 2 )

                    else:
                        #enlarge width of new extent, ensuring the map center stays the same
                        newWidth = currentWidthHeightRatio * newExtent.height()
                        deltaWidth = newWidth - newExtent.width()
                        newExtent.setXMinimum( newExtent.xMinimum() - deltaWidth / 2 )
                        newExtent.setXMaximum( newExtent.xMaximum() + deltaWidth / 2 )

                    composerMap.beginCommand( "Map extent changed")
                    composerMap.setNewExtent( newExtent )
                    composerMap.endCommand()
        self.setWindowTitle("Print Dialog (" + openFileString + ")")
        self.timeStart = time.time()
    def on_mActionMoveItemContent_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.MoveItemContent )

    def on_mActionPan_triggered(self):
        if ( self.mView ):
            self.mView.setCurrentTool( QgsComposerView.Pan )

    def on_mActionGroupItems_triggered(self):
        if ( self.mView ):
            self.mView.groupItems()

    def on_mActionUngroupItems_triggered(self):
        if ( self.mView ):
            self.mView.ungroupItems()

    def on_mActionLockItems_triggered(self):
        if ( self.mComposition ):
            self.mComposition.lockSelectedItems()

    def on_mActionUnlockAll_triggered(self):
        if ( self.mComposition ):
            self.mComposition.unlockAllItems()

    def actionCutTriggered(self):
        if ( self.mView ):
            self.mView.copyItems( QgsComposerView.ClipboardModeCut )

    def actionCopyTriggered(self):
        if ( self.mView ):
            self.mView.copyItems( QgsComposerView.ClipboardModeCopy )

    def actionPasteTriggered(self):
        if ( self.mView ):
            pt = self.mView.mapToScene( self.mView.mapFromGlobal( QtGui.QCursor.pos() ) )
            #TODO - use a better way of determining whether paste was triggered by keystroke
            #or menu item
            if (( pt.x() < 0 ) or ( pt.y() < 0 ) ):
            #action likely triggered by menu, paste items in center of screen
                self.mView.pasteItems( QgsComposerView.PasteModeCenter )
            else:
            #action likely triggered by keystroke, paste items at cursor position
                self.mView.pasteItems( QgsComposerView.PasteModeCursor )

    def on_mActionPasteInPlace_triggered(self):
        if ( self.mView ):
            self.mView.pasteItems( QgsComposerView.PasteModeInPlace )

    def on_mActionDeleteSelection_triggered(self):
        if ( self.mView ):
            self.mView.deleteSelectedItems()

    def on_mActionSelectAll_triggered(self):
        if ( self.mView ):
            self.mView.selectAll()

    def on_mActionDeselectAll_triggered(self):
        if ( self.mView ):
            self.mView.selectNone()

    def on_mActionInvertSelection_triggered(self):
        if ( self.mView ):
            self.mView.selectInvert()

    def on_mActionSelectNextAbove_triggered(self):
        if ( self.mComposition ):
            self.mComposition.selectNextByZOrder( QgsComposition.ZValueAbove )

    def on_mActionSelectNextBelow_triggered(self):
        if ( self.mComposition ):
            self.mComposition.selectNextByZOrder( QgsComposition.ZValueBelow )

    def on_mActionRaiseItems_triggered(self):
        if ( self.mComposition ):
            self.mComposition.raiseSelectedItems()

    def on_mActionLowerItems_triggered(self):
        if ( self.mComposition ):
            self.mComposition.lowerSelectedItems()

    def on_mActionMoveItemsToTop_triggered(self):
        if ( self.mComposition ):
            self.mComposition.moveSelectedItemsToTop()

    def on_mActionMoveItemsToBottom_triggered(self):
        if ( self.mComposition ):
            self.mComposition.moveSelectedItemsToBottom()

    def on_mActionAlignLeft_triggered(self):
        if ( self.mComposition ):
            self.mComposition.alignSelectedItemsLeft()

    def on_mActionAlignHCenter_triggered(self):
        if ( self.mComposition ):
            self.mComposition.alignSelectedItemsHCenter()

    def on_mActionAlignRight_triggered(self):
        if ( self.mComposition ):
            self.mComposition.alignSelectedItemsRight()

    def on_mActionAlignTop_triggered(self):
        if ( self.mComposition ):
            self.mComposition.alignSelectedItemsTop()

    def on_mActionAlignVCenter_triggered(self):
        if ( self.mComposition ):
            self.mComposition.alignSelectedItemsVCenter()

    def on_mActionAlignBottom_triggered(self):
        if ( self.mComposition ):
            self.mComposition.alignSelectedItemsBottom()

    def on_mActionUndo_triggered(self):
        if ( self.mComposition and self.mComposition.undoStack() ):
            self.mComposition.undoStack().undo()

    def on_mActionRedo_triggered(self):
        if ( self.mComposition and self.mComposition.undoStack() ):
            self.mComposition.undoStack().redo()

    def closeEvent(self, event):
        self.saveWindowState()
    def moveEvent(self, event):
        self.saveWindowState()
    def resizeEvent(self, event):
        self.saveWindowState()
    def saveWindowState(self):
        settings = QSettings()
        settings.setValue( "/Composer/geometry", self.saveGeometry() )
        # // store the toolbar/dock widget settings using Qt4 settings API
        settings.setValue( "/ComposerUI/state", self.saveState() )
    def restoreWindowState(self):
        pass
        # // restore the toolbar and dock widgets postions using Qt4 settings API
        # settings = QSettings()
        #
        # if ( not self.restoreState( settings.value( "/ComposerUI/state", QByteArray.fromRawData(defaultComposerUIstate, sizeof defaultComposerUIstate ) ).toByteArray() ) )
        # {
        #     QgsDebugMsg( "restore of composer UI state failed" )
        # }
        # // restore window geometry
        # if ( !restoreGeometry( settings.value( "/Composer/geometry", QByteArray::fromRawData(( char * )defaultComposerUIgeometry, sizeof defaultComposerUIgeometry ) ).toByteArray() ) )
        # {
        # QgsDebugMsg( "restore of composer UI geometry failed" )
        # }
    def writeXML( self, doc ):
        nl = doc.elementsByTagName( "qgis" )
        if ( nl.count() < 1 ):
            return
        qgisElem = nl.at( 0 ).toElement()
        if ( qgisElem.isNull() ):
            return

        self.writeXML_New( qgisElem, doc )
    def writeXML_New( self, parentNode, doc ):
        composerElem = doc.createElement( "Composer" )
        composerElem.setAttribute( "title", self.mTitle )

        # //change preview mode of minimised / hidden maps before saving XML (show contents only on demand)
        # mapIt = self.mMapsToRestore.constBegin()
        # for (  mapIt != mMapsToRestore.constEnd() ++mapIt )
        # {
        # mapIt.key().setPreviewMode(( QgsComposerMap::PreviewMode )( mapIt.value() ) )
        # }
        # mMapsToRestore.clear()
        #
        # //store if composer is open or closed
        if ( self.isVisible() ):
            composerElem.setAttribute( "visible", 1 )
        else:
            composerElem.setAttribute( "visible", 0 )
        parentNode.appendChild( composerElem )

        # //store composition
        if ( self.mComposition ):
            self.mComposition.writeXML( composerElem, doc )

        # // store atlas
        # mComposition.atlasComposition().writeXML( composerElem, doc )
    def templateXML( self, doc ):
        self.writeXML_New( doc, doc )
        pass
    def readXML( self, doc ):
        # composerNodeList = doc.elementsByTagName( "Composer" )
        # if ( composerNodeList.size() < 1 ):
        #     return
        # readXML( composerNodeList.at( 0 ).toElement(), doc, true )
        # self.cleanupAfterTemplateRead()
        pass
    def createCompositionWidget(self):
        if ( not self.mComposition ):
            return

        self.compositionWidget = QgsCompositionWidget( self.mGeneralDock, self.mComposition , self.mView)
        self.connect( self.mComposition, SIGNAL( "paperSizeChanged()" ), self.compositionWidget.displayCompositionWidthHeight)
        self.connect( self, SIGNAL( "printAsRasterChanged( bool )" ), self.compositionWidget.setPrintAsRasterCheckBox)
        self.connect( self.compositionWidget, SIGNAL( "pageOrientationChanged( QString )" ), self.pageOrientationChanged)

        self.mGeneralDock.setWidget( self.compositionWidget )
    def pageOrientationChanged( self):
        self.mSetPageOrientation = False

    def setPrinterPageOrientation(self):
        if ( not self.mSetPageOrientation ):
            paperWidth = self.mComposition.paperWidth()
            paperHeight = self.mComposition.paperHeight()
    
            # //set printer page orientation
            if ( paperWidth > paperHeight ):
                self.printer().setOrientation( QPrinter.Landscape )
            else:
                self.printer().setOrientation( QPrinter.Portrait )
    
            self.mSetPageOrientation = True
    def printer(self):
        # //only create the printer on demand - creating a printer object can be very slow
        # //due to QTBUG-3033
        if ( not self.mPrinter ):
            self.mPrinter = QPrinter()

        return self.mPrinter


class QgsItemTempHider:
    def __init__(self, items ):
        self.mItemVisibility = []
        it = items.begin()
        for it in items:
            if it == items.end():
                break
            self.mItemVisibility.append(it.isVisible())
            it.hide()
        self.items = items
    def hideAll(self):
        for i in range(self.items):
            it = self.items.at(i)
            if it == self.items.end():
                break
            it.hide()
        # QgsItemVisibilityHash::const_iterator it = mItemVisibility.constBegin()
        # for (  it != mItemVisibility.constEnd() ++it ) it.key().hide()
class PanelStatus:
    isVisibleValue =  False
    isActiveValue = False


    def setValue(self, visible = True, active = False):
        PanelStatus.isActiveValue = active
        PanelStatus.isVisibleValue = visible