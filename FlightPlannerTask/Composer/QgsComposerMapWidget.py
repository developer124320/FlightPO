
from PyQt4.QtGui import QWidget, QMenu, QDoubleValidator, QColorDialog,\
    QDialog, QFontDialog, QIcon, QPixmap, QAction, QComboBox, QListWidgetItem
from PyQt4 import uic
from PyQt4.QtCore import SIGNAL, SLOT, QString, Qt, QStringList, QSettings
from Composer.QgsComposerItemWidget import QgsComposerItemWidget

from qgis.core import QgsComposition, QgsComposerMap, QgsComposerMergeCommand, QGis, QgsRectangle, QgsStyleV2,\
    QgsSymbolLayerV2Utils, QgsComposerMapGrid, QgsExpressionContext, QgsComposerObject, QgsProject, QgsCoordinateReferenceSystem,\
    QgsComposerMapOverview
from qgis.gui import QgsSymbolV2SelectorDialog, QgsDataDefinedButton, QgsGenericProjectionSelector, QgsExpressionBuilderDialog
import define, time
from Type.switch import switch

from Composer.ui_qgscomposermapwidget import Ui_QgsComposerMapWidgetBase
from Composer.ui_qgscomposeritemwidget import Ui_QgsComposerItemWidgetBase
# FORM_CLASS, _ = uic.loadUiType(define.appPath + "/UI/Composer/qgsComposerMapWidgetBase.ui")

class QgsComposerMapWidget(Ui_QgsComposerMapWidgetBase):
    def __init__(self, parent, composerMap):
        Ui_QgsComposerMapWidgetBase.__init__(self, parent)
        self.mComposerMap = composerMap
        itemPropertiesWidget = QgsComposerItemWidget( self, composerMap )
        self.mainLayout.addWidget( itemPropertiesWidget )

        self.mScaleLineEdit.setValidator( QDoubleValidator( self.mScaleLineEdit ) )

        self.mXMinLineEdit.setValidator( QDoubleValidator( self.mXMinLineEdit ) )
        self.mXMaxLineEdit.setValidator( QDoubleValidator( self.mXMaxLineEdit ) )
        self.mYMinLineEdit.setValidator( QDoubleValidator( self.mYMinLineEdit ) )
        self.mYMaxLineEdit.setValidator( QDoubleValidator( self.mYMaxLineEdit ) )

        self.blockAllSignals( True )
        self.mPreviewModeComboBox.insertItem( 0, "Cache" )
        self.mPreviewModeComboBox.insertItem( 1, "Render" )
        self.mPreviewModeComboBox.insertItem( 2, "Rectangle" )

        self.mGridTypeComboBox.insertItem( 0, "Solid" )
        self.mGridTypeComboBox.insertItem( 1, "Cross" )
        self.mGridTypeComboBox.insertItem( 2, "Markers" )
        self.mGridTypeComboBox.insertItem( 3, "Frame and annotations only" )

        self.insertFrameDisplayEntries( self.mFrameDivisionsLeftComboBox );
        self.insertFrameDisplayEntries( self.mFrameDivisionsRightComboBox );
        self.insertFrameDisplayEntries( self.mFrameDivisionsTopComboBox );
        self.insertFrameDisplayEntries( self.mFrameDivisionsBottomComboBox );

        self.mAnnotationFormatComboBox.addItem( "Decimal" , QgsComposerMapGrid.Decimal );
        self.mAnnotationFormatComboBox.addItem( "Decimal with suffix" , QgsComposerMapGrid.DecimalWithSuffix );
        self.mAnnotationFormatComboBox.addItem( "Degree, minute" , QgsComposerMapGrid.DegreeMinuteNoSuffix );
        self.mAnnotationFormatComboBox.addItem( "Degree, minute with suffix", QgsComposerMapGrid.DegreeMinute );
        self.mAnnotationFormatComboBox.addItem( "Degree, minute aligned" , QgsComposerMapGrid.DegreeMinutePadded );
        self.mAnnotationFormatComboBox.addItem( "Degree, minute, second" , QgsComposerMapGrid.DegreeMinuteSecondNoSuffix );
        self.mAnnotationFormatComboBox.addItem( "Degree, minute, second with suffix" , QgsComposerMapGrid.DegreeMinuteSecond );
        self.mAnnotationFormatComboBox.addItem( "Degree, minute, second aligned" , QgsComposerMapGrid.DegreeMinuteSecondPadded );
        self.mAnnotationFormatComboBox.addItem( "Custom" , QgsComposerMapGrid.CustomFormat );


        self.mAnnotationFontColorButton.setColorDialogTitle( "Select font color" )
        self.mAnnotationFontColorButton.setAllowAlpha(True)
        self.mAnnotationFontColorButton.setContext("composer")
        # self.mAnnotationFontColorButton.setColorDialogOptions( QColorDialog.ShowAlphaChannel )

        self.insertAnnotationDisplayEntries( self.mAnnotationDisplayLeftComboBox )
        self.insertAnnotationDisplayEntries( self.mAnnotationDisplayRightComboBox )
        self.insertAnnotationDisplayEntries( self.mAnnotationDisplayTopComboBox )
        self.insertAnnotationDisplayEntries( self.mAnnotationDisplayBottomComboBox )

        self.insertAnnotationPositionEntries( self.mAnnotationPositionLeftComboBox )
        self.insertAnnotationPositionEntries( self.mAnnotationPositionRightComboBox )
        self.insertAnnotationPositionEntries( self.mAnnotationPositionTopComboBox )
        self.insertAnnotationPositionEntries( self.mAnnotationPositionBottomComboBox )

        self.insertAnnotationDirectionEntries( self.mAnnotationDirectionComboBoxLeft )
        self.insertAnnotationDirectionEntries( self.mAnnotationDirectionComboBoxRight )
        self.insertAnnotationDirectionEntries( self.mAnnotationDirectionComboBoxTop )
        self.insertAnnotationDirectionEntries( self.mAnnotationDirectionComboBoxBottom )

        # self.mFrameStyleComboBox.insertItem( 0, "No frame" )
        # self.mFrameStyleComboBox.insertItem( 1, "Zebra" )

        self.mGridFramePenColorButton.setColorDialogTitle( "Select grid frame color" )
        self.mGridFramePenColorButton.setAllowAlpha(True)
        self.mGridFramePenColorButton.setContext("composer")
        self.mGridFramePenColorButton.setNoColorString("Transparent frame")
        self.mGridFramePenColorButton.setShowNoColor(True)

        self.mGridFrameFill1ColorButton.setColorDialogTitle( "Select grid frame fill color" )
        self.mGridFrameFill1ColorButton.setAllowAlpha(True)
        self.mGridFrameFill1ColorButton.setContext("composer")
        self.mGridFrameFill1ColorButton.setNoColorString("Transparent frame")
        self.mGridFrameFill1ColorButton.setShowNoColor(True)

        self.mGridFrameFill2ColorButton.setColorDialogTitle( "Select grid frame fill color" )
        self.mGridFrameFill2ColorButton.setAllowAlpha(True)
        self.mGridFrameFill2ColorButton.setContext("composer")
        self.mGridFrameFill2ColorButton.setNoColorString("Transparent frame")
        self.mGridFrameFill2ColorButton.setShowNoColor(True)

        #set initial state of frame style controls
        self.toggleFrameControls( False, False, False )

        m = QMenu( self);
        self.mLayerListFromPresetButton.setMenu( m );
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/images/themes/default/mActionShowAllLayers.png"), QIcon.Normal, QIcon.Off)
        self.mLayerListFromPresetButton.setIcon( icon);
        self.mLayerListFromPresetButton.setToolTip( "Set layer list from a visibility preset" )

        self.connect( m, SIGNAL( "aboutToShow()" ), self.aboutToShowVisibilityPresetsMenu);

        # self.connect( self.mGridCheckBox, SIGNAL( "toggled( bool )" ),
        #        self.mDrawAnnotationCheckableGroupBox, SLOT( "setEnabled( bool )"))
        #
        # self.connect( self.mAtlasCheckBox, SIGNAL( "toggled( bool )" ), self.atlasToggled)

        if ( composerMap ):
            self.mLabel.setText( QString( "Map %1" ).arg( composerMap.id() ) );
            self.connect( composerMap, SIGNAL( "itemChanged()" ), self.setGuiElementValues)

            # #get composition
            atlas = self.atlasComposition()
            if ( atlas ):
                self.connect( atlas, SIGNAL( "coverageLayerChanged( QgsVectorLayer* )" ), self.atlasLayerChanged)
                self.connect( atlas, SIGNAL( "toggled( bool )" ), self.compositionAtlasToggled)
                self.connect( atlas, SIGNAL( "coverageLayerChanged( QgsVectorLayer* )" ), self.populateDataDefinedButtons)
                self.connect( atlas, SIGNAL( "toggled( bool )" ), self.populateDataDefinedButtons)

                self.compositionAtlasToggled( atlas.enabled() )

        # self.updateOverviewSymbolMarker()
        # self.updateLineSymbolMarker()

        self.connect( self.mScaleDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mScaleDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);

        self.connect( self.mMapRotationDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mMapRotationDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);

        self.connect( self.mXMinDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mXMinDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);

        self.connect( self.mYMinDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mYMinDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);

        self.connect( self.mXMaxDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mXMaxDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);

        self.connect( self.mYMaxDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mYMaxDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);

        self.connect( self.mAtlasMarginDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mAtlasMarginDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);

        self.connect( self.mLayersDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mLayersDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);

        self.connect( self.mStylePresetsDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mStylePresetsDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);


        self.updateGuiElements()
        self.loadGridEntries();
        self.loadOverviewEntries();
        self.blockAllSignals( False )


        #content of QgsComposerMapWidget.h file


        # self.connect( self.mPreviewModeComboBox, SIGNAL( "activated( int )" ), self.on_mPreviewModeComboBox_activated)
        # self.connect( self.mScaleLineEdit, SIGNAL( "editingFinished()" ), self.on_mScaleLineEdit_editingFinished)
        # self.connect( self.mMapRotationSpinBox, SIGNAL( "valueChanged( double )" ), self.on_mMapRotationSpinBox_valueChanged)
        # self.connect( self.mSetToMapCanvasExtentButton, SIGNAL( "clicked()" ), self.on_mSetToMapCanvasExtentButton_clicked)
        # self.mViewExtentInCanvasButton.clicked.connect(self.on_mViewExtentInCanvasButton_clicked)
        # self.connect( self.mUpdatePreviewButton, SIGNAL( "clicked()" ), self.on_mUpdatePreviewButton_clicked)
        # self.connect( self.mKeepLayerListCheckBox, SIGNAL( "stateChanged( int )" ), self.on_mKeepLayerListCheckBox_stateChanged)
        # self.connect( self.mKeepLayerStylesCheckBox, SIGNAL( "stateChanged( int )" ), self.on_mKeepLayerStylesCheckBox_stateChanged)
        # self.connect( self.mDrawCanvasItemsCheckBox, SIGNAL( "stateChanged( int )" ), self.on_mDrawCanvasItemsCheckBox_stateChanged)
        # self.connect( self.mOverviewFrameMapComboBox, SIGNAL( "currentIndexChanged( const QString& )" ), self.on_mOverviewFrameMapComboBox_currentIndexChanged)
        # self.connect( self.mOverviewFrameStyleButton, SIGNAL( "clicked()" ), self.on_mOverviewFrameStyleButton_clicked)
        # self.connect( self.mOverviewBlendModeComboBox, SIGNAL( "currentIndexChanged( int )" ), self.on_mOverviewBlendModeComboBox_currentIndexChanged)
        # self.connect( self.mOverviewInvertCheckbox, SIGNAL( "toggled( bool )" ), self.on_mOverviewInvertCheckbox_toggled)
        # self.connect( self.mOverviewCenterCheckbox, SIGNAL( "toggled( bool )" ), self.on_mOverviewCenterCheckbox_toggled)
        #
        # self.mXMinLineEdit.editingFinished.connect(self.on_mXMinLineEdit_editingFinished)
        # self.mXMaxLineEdit.editingFinished.connect(self.on_mXMaxLineEdit_editingFinished)
        # self.mYMinLineEdit.editingFinished.connect(self.on_mYMinLineEdit_editingFinished)
        # self.mYMaxLineEdit.editingFinished.connect(self.on_mYMaxLineEdit_editingFinished)
        #
        # self.connect( self.mAtlasMarginRadio, SIGNAL( "toggled( bool )" ), self.on_mAtlasMarginRadio_toggled)
        # self.connect( self.mAtlasCheckBox, SIGNAL( "toggled( bool )" ), self.on_mAtlasCheckBox_toggled)
        # self.connect( self.mAtlasMarginSpinBox, SIGNAL( "valueChanged( int )" ), self.on_mAtlasMarginSpinBox_valueChanged)
        # self.connect( self.mAtlasFixedScaleRadio, SIGNAL( "toggled( bool )" ), self.on_mAtlasFixedScaleRadio_toggled)
        # self.connect( self.mAtlasPredefinedScaleRadio, SIGNAL( "toggled( bool )" ), self.on_mAtlasPredefinedScaleRadio_toggled)
        #
        # # self.mAddGridPushButton.clicked.connect(self.on_mAddGridPushButton_clicked)
        # # self.mRemoveGridPushButton.clicked.connect(self.on_mRemoveGridPushButton_clicked)
        # # self.mGridUpButton.clicked.connect(self.on_mGridUpButton_clicked)
        # # self.mGridDownButton.clicked.connect(self.on_mGridDownButton_clicked)
        #
        # self.connect( self.mGridListWidget, SIGNAL( "currentItemChanged( QListWidgetItem*, QListWidgetItem* )" ), self.on_mGridListWidget_currentItemChanged)
        # self.connect( self.mGridListWidget, SIGNAL( "itemChanged( QListWidgetItem* )" ), self.on_mGridListWidget_itemChanged)
        # self.mGridMarkerStyleButton.clicked.connect(self.on_mGridMarkerStyleButton_clicked)
        #
        # self.mIntervalXSpinBox.editingFinished.connect(self.on_mIntervalXSpinBox_editingFinished)
        # self.mIntervalYSpinBox.editingFinished.connect(self.on_mIntervalYSpinBox_editingFinished)
        # self.mOffsetXSpinBox.valueChanged.connect(self.on_mOffsetXSpinBox_valueChanged)
        # self.mOffsetYSpinBox.valueChanged.connect(self.on_mOffsetYSpinBox_valueChanged)
        #
        # self.mGridLineStyleButton.clicked.connect(self.on_mGridLineStyleButton_clicked)
        # self.mMapGridCRSButton.clicked.connect(self.on_mMapGridCRSButton_clicked)
        # self.connect( self.mMapGridUnitComboBox, SIGNAL( "currentIndexChanged( const QString& )" ), self.on_mMapGridUnitComboBox_currentIndexChanged)
        # self.connect( self.mCheckGridLeftSide, SIGNAL( "toggled( bool )" ), self.on_mCheckGridLeftSide_toggled)
        # self.connect( self.mCheckGridRightSide, SIGNAL( "toggled( bool )" ), self.on_mCheckGridRightSide_toggled)
        # self.connect( self.mCheckGridTopSide, SIGNAL( "toggled( bool )" ), self.on_mCheckGridTopSide_toggled)
        # self.connect( self.mCheckGridBottomSide, SIGNAL( "toggled( bool )" ), self.on_mCheckGridBottomSide_toggled)
        #
        #
        # self.connect( self.mGridCheckBox, SIGNAL( "toggled( bool )" ), self.on_mGridCheckBox_toggled)
        # self.connect( self.mGridTypeComboBox, SIGNAL( "currentIndexChanged( const QString& )" ), self.on_mGridTypeComboBox_currentIndexChanged)
        # self.connect( self.mFrameStyleComboBox, SIGNAL( "currentIndexChanged( const QString& )" ), self.on_mFrameStyleComboBox_currentIndexChanged)
        # self.connect( self.mFrameWidthSpinBox, SIGNAL( "valueChanged( double )" ), self.on_mFrameWidthSpinBox_valueChanged)
        # self.connect( self.mGridFramePenSizeSpinBox, SIGNAL( "valueChanged( double )" ), self.on_mGridFramePenSizeSpinBox_valueChanged)
        # self.connect( self.mGridFramePenColorButton, SIGNAL( "colorChanged( const QColor& )" ), self.on_mGridFramePenColorButton_colorChanged)
        # self.connect( self.mGridFrameFill1ColorButton, SIGNAL( "colorChanged( const QColor& )" ), self.on_mGridFrameFill1ColorButton_colorChanged)
        # self.connect( self.mGridFrameFill2ColorButton, SIGNAL( "colorChanged( const QColor& )" ), self.on_mGridFrameFill2ColorButton_colorChanged)
        #
        #
        # self.connect( self.mCrossWidthSpinBox, SIGNAL( "valueChanged( double )" ), self.on_mCrossWidthSpinBox_valueChanged)
        # self.connect( self.mGridBlendComboBox, SIGNAL( "currentIndexChanged( int )" ), self.on_mGridBlendComboBox_currentIndexChanged)
        # self.connect( self.mFrameDivisionsLeftComboBox, SIGNAL( "currentIndexChanged( int )" ), self.on_mFrameDivisionsLeftComboBox_currentIndexChanged)
        # self.connect( self.mFrameDivisionsRightComboBox, SIGNAL( "currentIndexChanged( int )" ), self.on_mFrameDivisionsRightComboBox_currentIndexChanged)
        # self.connect( self.mFrameDivisionsTopComboBox, SIGNAL( "currentIndexChanged( int )" ), self.on_mFrameDivisionsTopComboBox_currentIndexChanged)
        # self.connect( self.mFrameDivisionsBottomComboBox, SIGNAL( "currentIndexChanged( int )" ), self.on_mFrameDivisionsBottomComboBox_currentIndexChanged)
        #
        # self.connect( self.mDrawAnnotationGroupBox, SIGNAL( "toggled( bool )" ), self.on_mDrawAnnotationGroupBox_toggled)
        # self.mAnnotationFormatButton.clicked.connect(self.on_mAnnotationFormatButton_clicked)
        #
        # self.connect( self.mAnnotationDisplayLeftComboBox, SIGNAL( "currentIndexChanged( const QString& )" ), self.on_mAnnotationDisplayLeftComboBox_currentIndexChanged)
        # self.connect( self.mAnnotationDisplayRightComboBox, SIGNAL( "currentIndexChanged( const QString& )" ), self.on_mAnnotationDisplayRightComboBox_currentIndexChanged)
        # self.connect( self.mAnnotationDisplayTopComboBox, SIGNAL( "currentIndexChanged( const QString& )" ), self.on_mAnnotationDisplayTopComboBox_currentIndexChanged)
        # self.connect( self.mAnnotationDisplayBottomComboBox, SIGNAL( "currentIndexChanged( const QString& )" ), self.on_mAnnotationDisplayBottomComboBox_currentIndexChanged)
        #
        #
        #
        #
        # self.mAnnotationFontButton.clicked.connect(self.on_mAnnotationFontButton_clicked)
        # self.connect( self.mAnnotationFontColorButton, SIGNAL( "colorChanged( const QColor& )" ), self.on_mAnnotationFontColorButton_colorChanged)
        # self.connect( self.mDistanceToMapFrameSpinBox, SIGNAL( "valueChanged( double )" ), self.on_mDistanceToMapFrameSpinBox_valueChanged)
        # self.connect( self.mAnnotationFormatComboBox, SIGNAL( "currentIndexChanged( int )" ), self.on_mAnnotationFormatComboBox_currentIndexChanged)
        #
        # self.connect( self.mAnnotationPositionLeftComboBox, SIGNAL( "currentIndexChanged( const QString& )" ), self.on_mAnnotationPositionLeftComboBox_currentIndexChanged)
        # self.connect( self.mAnnotationPositionRightComboBox, SIGNAL( "currentIndexChanged( const QString& )" ), self.on_mAnnotationPositionRightComboBox_currentIndexChanged)
        # self.connect( self.mAnnotationPositionTopComboBox, SIGNAL( "currentIndexChanged( const QString& )" ), self.on_mAnnotationPositionTopComboBox_currentIndexChanged)
        # self.connect( self.mAnnotationPositionBottomComboBox, SIGNAL( "currentIndexChanged( const QString& )" ), self.on_mAnnotationPositionBottomComboBox_currentIndexChanged)
        #
        # self.connect( self.mAnnotationDirectionComboBoxLeft, SIGNAL( "currentIndexChanged( int )" ), self.on_mAnnotationDirectionComboBoxLeft_currentIndexChanged)
        # self.connect( self.mAnnotationDirectionComboBoxRight, SIGNAL( "currentIndexChanged( int )" ), self.on_mAnnotationDirectionComboBoxRight_currentIndexChanged)
        # self.connect( self.mAnnotationDirectionComboBoxTop, SIGNAL( "currentIndexChanged( int )" ), self.on_mAnnotationDirectionComboBoxTop_currentIndexChanged)
        # self.connect( self.mAnnotationDirectionComboBoxBottom, SIGNAL( "currentIndexChanged( int )" ), self.on_mAnnotationDirectionComboBoxBottom_currentIndexChanged)
        #
        # # self.connect( self.mDrawAnnotationCheckableGroupBox, SIGNAL( "toggled( bool )" ), self.on_mDrawAnnotationCheckableGroupBox_toggled)
        # self.connect( self.mCoordinatePrecisionSpinBox, SIGNAL( "valueChanged( int )" ), self.on_mCoordinatePrecisionSpinBox_valueChanged)
        #
        # self.mAddOverviewPushButton.clicked.connect(self.on_mAddOverviewPushButton_clicked)
        # self.mRemoveOverviewPushButton.clicked.connect(self.on_mRemoveOverviewPushButton_clicked)
        # self.mOverviewUpButton.clicked.connect(self.on_mOverviewUpButton_clicked)
        # self.mOverviewDownButton.clicked.connect(self.on_mOverviewDownButton_clicked)
        #
        # self.connect( self.mOverviewCheckBox, SIGNAL( "toggled( bool )" ), self.on_mOverviewCheckBox_toggled)
        # self.connect( self.mOverviewListWidget, SIGNAL( "currentItemChanged( QListWidgetItem*, QListWidgetItem* )" ), self.on_mOverviewListWidget_currentItemChanged)
        # self.connect( self.mOverviewListWidget, SIGNAL( "itemChanged( QListWidgetItem* )" ), self.on_mOverviewListWidget_itemChanged)

        self.timeStart = 0
        self.timeEnd = 0
    def _getExpressionContext( self, context ):
        composerObject = context;
        if ( not composerObject ):
            return QgsExpressionContext();
        expContext = composerObject.createExpressionContext()
        return QgsExpressionContext( expContext );

    def populateDataDefinedButtons(self):
        vl = self.atlasCoverageLayer();

        for button in self.findChildren(QgsDataDefinedButton):
            button.blockSignals( True );
            # button.registerGetExpressionContextCallback( &_getExpressionContext, mComposerMap );

        # #initialise buttons to use atlas coverage layer
        self.mScaleDDBtn.init( vl, self.mComposerMap.dataDefinedProperty( QgsComposerObject.MapScale ),
                         QgsDataDefinedButton.AnyType, QgsDataDefinedButton.doubleDesc() );
        self.mMapRotationDDBtn.init( vl, self.mComposerMap.dataDefinedProperty( QgsComposerObject.MapRotation ),
                               QgsDataDefinedButton.AnyType, QgsDataDefinedButton.doubleDesc() );
        self.mXMinDDBtn.init( vl, self.mComposerMap.dataDefinedProperty( QgsComposerObject.MapXMin ),
                        QgsDataDefinedButton.AnyType, QgsDataDefinedButton.doubleDesc() );
        self.mYMinDDBtn.init( vl, self.mComposerMap.dataDefinedProperty( QgsComposerObject.MapYMin ),
                        QgsDataDefinedButton.AnyType, QgsDataDefinedButton.doubleDesc() );
        self.mXMaxDDBtn.init( vl, self.mComposerMap.dataDefinedProperty( QgsComposerObject.MapXMax ),
                        QgsDataDefinedButton.AnyType, QgsDataDefinedButton.doubleDesc() );
        self.mYMaxDDBtn.init( vl, self.mComposerMap.dataDefinedProperty( QgsComposerObject.MapYMax ),
                        QgsDataDefinedButton.AnyType, QgsDataDefinedButton.doubleDesc() );
        self.mAtlasMarginDDBtn.init( vl, self.mComposerMap.dataDefinedProperty( QgsComposerObject.MapAtlasMargin ),
                               QgsDataDefinedButton.AnyType, QgsDataDefinedButton.doubleDesc() );
        self.mStylePresetsDDBtn.init( vl, self.mComposerMap.dataDefinedProperty( QgsComposerObject.MapStylePreset ),
                                QgsDataDefinedButton.String, "string matching a style preset name" ) ;
        self.mLayersDDBtn.init( vl, self.mComposerMap.dataDefinedProperty( QgsComposerObject.MapLayers ),
                          QgsDataDefinedButton.String, "list of map layer names separated by | characters" )

        for button in self.findChildren(QgsDataDefinedButton):
            button.blockSignals( False );

    def ddPropertyForWidget( self, widget ):
        if ( widget == self.mScaleDDBtn ):
            return QgsComposerObject.MapScale;
        elif ( widget == self.mMapRotationDDBtn ):
            return QgsComposerObject.MapRotation;
        elif ( widget == self.mXMinDDBtn ):
            return QgsComposerObject.MapXMin;
        elif ( widget == self.mYMinDDBtn ):
            return QgsComposerObject.MapYMin;
        elif ( widget == self.mXMaxDDBtn ):
            return QgsComposerObject.MapXMax;
        elif ( widget == self.mYMaxDDBtn ):
            return QgsComposerObject.MapYMax;
        elif ( widget == self.mAtlasMarginDDBtn ):
            return QgsComposerObject.MapAtlasMargin;
        elif ( widget == self.mStylePresetsDDBtn ):
            return QgsComposerObject.MapStylePreset;
        elif ( widget == self.mLayersDDBtn ):
            return QgsComposerObject.MapLayers;
        return QgsComposerObject.NoProperty;


    def compositionAtlasToggled( self, atlasEnabled ):
        if ( atlasEnabled and self.mComposerMap and self.mComposerMap.composition() and self.mComposerMap.composition().atlasComposition().coverageLayer() and \
                         self.mComposerMap.composition().atlasComposition().coverageLayer().wkbType() != QGis.WKBNoGeometry):
            self.mAtlasCheckBox.setEnabled( True )
        else:
            self.mAtlasCheckBox.setEnabled( False )
            self.mAtlasCheckBox.setChecked( False )

    def aboutToShowVisibilityPresetsMenu(self):
        menu = self.sender() ;
        if ( not isinstance(menu, QMenu )):
            return;

        # menu.clear();
        # for  presetName in QgsProject.instance().visibilityPresetCollection().presets():
        #     a = menu.addAction( presetName, self, SLOT( "visibilityPresetSelected()" ) );
        #     a.setCheckable( True );
        #     layers = QgsVisibilityPresets.instance().orderedPresetVisibleLayers( presetName );
        #     QMap<QString, QString> styles = QgsProject.instance().visibilityPresetCollection().presetStyleOverrides( presetName );
        #     if ( layers == mComposerMap.layerSet() && styles == mComposerMap.layerStyleOverrides() )
        #       a.setChecked( true );
        # }
        #
        # if ( menu.actions().isEmpty() )
        # menu.addAction( tr( "No presets defined" ) ).setEnabled( false );
    # def visibilityPresetSelected(self):
    #     action = self.sender()
    #     if ( not isinstance(action, QAction )):
    #         return;
    #
    #     presetName = action.text();
    #     lst = QgsVisibilityPresets.instance().orderedPresetVisibleLayers( presetName );
    #     if ( self.mComposerMap ):
    #         self.mKeepLayerListCheckBox.setChecked( True );
    #         self.mComposerMap.setLayerSet( lst );
    #
    #         self.mKeepLayerStylesCheckBox.setChecked( True );
    #
    #         # self.mComposerMap.setLayerStyleOverrides( QgsProject.instance().visibilityPresetCollection().presetStyleOverrides( presetName ) );
    #
    #         self.mComposerMap.cache();
    #         self.mComposerMap.update();


    def atlasToggled( self, checked ):
        if ( checked and self.mComposerMap ):
            #check atlas coverage layer type
            composition = self.mComposerMap.composition()
            if ( composition ):
                self.toggleAtlasMarginByLayerType()
            else:
                self.mAtlasMarginRadio.setEnabled( False )
        else:
            self.mAtlasMarginRadio.setEnabled( False )

        self.mAtlasFixedScaleRadio.setEnabled( checked )
        if ( self.mAtlasMarginRadio.isEnabled() and self.mAtlasMarginRadio.isChecked() ):
            self.mAtlasMarginSpinBox.setEnabled( True )
        else:
            self.mAtlasMarginSpinBox.setEnabled( False )

    def on_mAtlasCheckBox_toggled( self, checked ):
        if ( not self.mComposerMap ):
            return
        self.mAtlasFixedScaleRadio.setEnabled( checked );
        self.mAtlasMarginRadio.setEnabled( checked );

        if ( self.mAtlasMarginRadio.isEnabled() and self.mAtlasMarginRadio.isChecked() ):
            self.mAtlasMarginSpinBox.setEnabled( True );
        else:
            self.mAtlasMarginSpinBox.setEnabled( False )

        self.mAtlasPredefinedScaleRadio.setEnabled( checked );

        if ( checked ):
            # #check atlas coverage layer type
            composition = self.mComposerMap.composition();
            if ( composition ):
              self.toggleAtlasScalingOptionsByLayerType();

        # # disable predefined scales if none are defined
        if ( not self.hasPredefinedScales() ):
            self.mAtlasPredefinedScaleRadio.setEnabled( False );
        self.mComposerMap.setAtlasDriven( checked )
        self.updateMapForAtlas()

    def updateMapForAtlas(self):
    #update map if in atlas preview mode
        composition = self.mComposerMap.composition()
        if ( not composition ):
            return
        if ( composition.atlasMode() == QgsComposition.AtlasOff ):
            return
        if ( self.mComposerMap.atlasDriven() ):
            #update atlas based extent for map
            atlas = composition.atlasComposition()
            atlas.prepareMap( self.mComposerMap )
        else:
            #redraw map
            self.mComposerMap.cache()
            self.mComposerMap.update()

    def on_mAtlasMarginRadio_toggled( self, checked ):
        self.mAtlasMarginSpinBox.setEnabled( checked )
        if ( checked and self.mComposerMap ):
            self.mComposerMap.setAtlasScalingMode( QgsComposerMap.Auto );
            self.updateMapForAtlas();

    def on_mAtlasMarginSpinBox_valueChanged( self, value ):
        if ( not self.mComposerMap ):
            return

        self.mComposerMap.setAtlasMargin( value / 100. )
        self.updateMapForAtlas()

    def on_mAtlasFixedScaleRadio_toggled( self, checked ):
        if ( not self.mComposerMap ):
            return
        if checked:
            self.mComposerMap.setAtlasScalingMode( QgsComposerMap.Fixed )
            self.updateMapForAtlas()

    def on_mAtlasPredefinedScaleRadio_toggled( self, checked ):
        if ( not self.mComposerMap ):
            return;

        if ( self.hasPredefinedScales() ):
            if ( checked ):
                self.mComposerMap.setAtlasScalingMode( QgsComposerMap.Predefined );
                self.updateMapForAtlas();
        else:
            # # restore to fixed scale if no predefined scales exist
            self.mAtlasFixedScaleRadio.blockSignals( True );
            self.mAtlasFixedScaleRadio.setChecked( True );
            self.mAtlasFixedScaleRadio.blockSignals( False );
            self.mComposerMap.setAtlasScalingMode( QgsComposerMap.Fixed );

    def on_mPreviewModeComboBox_activated( self, i ):
        # Q_UNUSED( i )

        if ( not self.mComposerMap ):
            return

        if ( self.mComposerMap.isDrawing() ):
            return

        comboText = self.mPreviewModeComboBox.currentText()
        if ( comboText == "Cache"):
            self.mComposerMap.setPreviewMode( QgsComposerMap.Cache )
            self.mUpdatePreviewButton.setEnabled( True )
        elif ( comboText == "Render" ):
            self.mComposerMap.setPreviewMode( QgsComposerMap.Render )
            self.mUpdatePreviewButton.setEnabled( True )
        elif ( comboText == "Rectangle"):
            self.mComposerMap.setPreviewMode( QgsComposerMap.Rectangle )
            self.mUpdatePreviewButton.setEnabled( False )

        self.mComposerMap.cache()
        self.mComposerMap.update()

    def on_mScaleLineEdit_editingFinished(self):
        if ( not self.mComposerMap ):
            return

        # bool conversionSuccess
        scaleDenominator, conversionSuccess = self.mScaleLineEdit.text().toDouble()

        if ( not conversionSuccess ):
            return
        if ( round( scaleDenominator ) == round( self.mComposerMap.scale() ) ):
            return;
        self.mComposerMap.beginCommand( "Map scale changed" )
        self.mComposerMap.setNewScale( scaleDenominator )
        self.mComposerMap.endCommand()

    def on_mMapRotationSpinBox_valueChanged( self, value ):
        if ( not self.mComposerMap ):
            return

        self.mComposerMap.beginCommand( "Map rotation changed", QgsComposerMergeCommand.ComposerMapRotation )
        self.mComposerMap.setMapRotation( self.mMapRotationSpinBox.value() )
        self.mComposerMap.endCommand()
        self.mComposerMap.cache()
        self.mComposerMap.update()

    def on_mSetToMapCanvasExtentButton_clicked(self):
        if ( self.mComposerMap ):
            newExtent = self.mComposerMap.composition().mapSettings().visibleExtent()

            self.mComposerMap.beginCommand( "Map extent changed" )
            self.mComposerMap.zoomToExtent( newExtent )
            self.mComposerMap.endCommand()
    def on_mViewExtentInCanvasButton_clicked(self):
        if ( not self.mComposerMap ):
            return;

        currentMapExtent = self.mComposerMap.currentMapExtent()

        if ( not currentMapExtent.isEmpty() ):
            define._canvas.setExtent( currentMapExtent );
            define._canvas.refresh();

    def on_mXMinLineEdit_editingFinished(self):
        self.updateComposerExtentFromGui()

    def on_mXMaxLineEdit_editingFinished(self):
        self.updateComposerExtentFromGui()

    def on_mYMinLineEdit_editingFinished(self):
        self.updateComposerExtentFromGui()

    def on_mYMaxLineEdit_editingFinished(self):
        self.updateComposerExtentFromGui()

    def setGuiElementValues(self):
        self.mScaleLineEdit.blockSignals( True )
        self.mPreviewModeComboBox.blockSignals( True )

        self.updateGuiElements()

        self.mScaleLineEdit.blockSignals( False )
        self.mPreviewModeComboBox.blockSignals( False )

    def updateGuiElements(self):
        if ( self.mComposerMap ):
            self.blockAllSignals( True )

            # #width, height, scale
            scale = self.mComposerMap.scale();

            #round scale to an appropriate number of decimal places
            if ( scale >= 10 ):
                #round scale to integer if it's greater than 10
                self.mScaleLineEdit.setText( QString.number( self.mComposerMap.scale(), 'f', 0 ) );
            elif ( scale >= 1 ):
                #don't round scale if it's less than 10, instead use 4 decimal places
                self.mScaleLineEdit.setText( QString.number( self.mComposerMap.scale(), 'f', 4 ) )
            else:
                #if scale < 1 then use 10 decimal places
                self.mScaleLineEdit.setText( QString.number( self.mComposerMap.scale(), 'f', 10 ) );
            #preview mode
            previewMode = self.mComposerMap.previewMode()
            index = -1
            if ( previewMode == QgsComposerMap.Cache ):
                index = self.mPreviewModeComboBox.findText( "Cache" )
                self.mUpdatePreviewButton.setEnabled( True )
            elif ( previewMode == QgsComposerMap.Render ):
                index = self.mPreviewModeComboBox.findText( "Render" )
                self.mUpdatePreviewButton.setEnabled( True )
            elif ( previewMode == QgsComposerMap.Rectangle ):
                index = self.mPreviewModeComboBox.findText( "Rectangle" )
                self.mUpdatePreviewButton.setEnabled( False )
            if ( index != -1 ):
                self.mPreviewModeComboBox.setCurrentIndex( index )

            #composer map extent
            composerMapExtent = self.mComposerMap.currentMapExtent()
            self.mXMinLineEdit.setText( QString.number( composerMapExtent.xMinimum(), 'f', 3 ) )
            self.mXMaxLineEdit.setText( QString.number( composerMapExtent.xMaximum(), 'f', 3 ) )
            self.mYMinLineEdit.setText( QString.number( composerMapExtent.yMinimum(), 'f', 3 ) )
            self.mYMaxLineEdit.setText( QString.number( composerMapExtent.yMaximum(), 'f', 3 ) )

            self.mMapRotationSpinBox.setValue( self.mComposerMap.mapRotation(QgsComposerObject.OriginalValue) )

            #keep layer list check box
            if ( self.mComposerMap.keepLayerSet() ):
                self.mKeepLayerListCheckBox.setCheckState( Qt.Checked )
            else:
                self.mKeepLayerListCheckBox.setCheckState( Qt.Unchecked )

            self.mKeepLayerStylesCheckBox.setEnabled( self.mComposerMap.keepLayerSet() );
            self.mKeepLayerStylesCheckBox.setCheckState( Qt.Checked if(self.mComposerMap.keepLayerStyles()) else Qt.Unchecked );

            #draw canvas items
            if ( self.mComposerMap.drawCanvasItems() ):
                self.mDrawCanvasItemsCheckBox.setCheckState( Qt.Checked )
            else:
                self.mDrawCanvasItemsCheckBox.setCheckState( Qt.Unchecked )

            # #overview frame
            # overviewMapFrameId = self.mComposerMap.overviewFrameMapId()
            # self.mOverviewFrameMapComboBox.setCurrentIndex( self.mOverviewFrameMapComboBox.findData( overviewMapFrameId ) )
            # #overview frame blending mode
            # self.mOverviewBlendModeComboBox.setBlendMode( self.mComposerMap.overviewBlendMode() )
            # #overview inverted
            # self.mOverviewInvertCheckbox.setChecked( self.mComposerMap.overviewInverted() )
            # #center overview
            # self.mOverviewCenterCheckbox.setChecked( self.mComposerMap.overviewCentered() )
            #
            # #grid
            # if ( self.mComposerMap.gridEnabled() ):
            #     self.mGridCheckBox.setChecked( True )
            # else:
            #     self.mGridCheckBox.setChecked( False )
            #
            # self.mIntervalXSpinBox.setValue( self.mComposerMap.gridIntervalX() )
            # self.mIntervalYSpinBox.setValue( self.mComposerMap.gridIntervalY() )
            # self.mOffsetXSpinBox.setValue( self.mComposerMap.gridOffsetX() )
            # self.mOffsetYSpinBox.setValue( self.mComposerMap.gridOffsetY() )
            #
            # gridStyle = self.mComposerMap.gridStyle()
            # if ( gridStyle == QgsComposerMap.Cross ):
            #     self.mGridTypeComboBox.setCurrentIndex( self.mGridTypeComboBox.findText( "Cross" ) )
            # else:
            #     self.mGridTypeComboBox.setCurrentIndex( self.mGridTypeComboBox.findText( "Solid" ) )
            #
            # self.mCrossWidthSpinBox.setValue( self.mComposerMap.crossLength() )
            #
            # #grid frame
            # self.mFrameWidthSpinBox.setValue( self.mComposerMap.gridFrameWidth() )
            # self.mGridFramePenSizeSpinBox.setValue( self.mComposerMap.gridFramePenSize() )
            # self.mGridFramePenColorButton.setColor( self.mComposerMap.gridFramePenColor() )
            # self.mGridFrameFill1ColorButton.setColor( self.mComposerMap.gridFrameFillColor1() )
            # self.mGridFrameFill2ColorButton.setColor( self.mComposerMap.gridFrameFillColor2() )
            # gridFrameStyle = self.mComposerMap.gridFrameStyle()
            # if ( gridFrameStyle == QgsComposerMap.Zebra ):
            #     self.mFrameStyleComboBox.setCurrentIndex( self.mFrameStyleComboBox.findText( "Zebra" ) )
            #     self.toggleFrameControls( True )
            # else: #NoGridFrame
            #     self.mFrameStyleComboBox.setCurrentIndex( self.mFrameStyleComboBox.findText( "No frame" ) )
            #     self.toggleFrameControls( False )
            #
            # #grid blend mode
            # self.mGridBlendComboBox.setBlendMode( self.mComposerMap.gridBlendMode() )
            #
            # #grid annotation format
            # gf = self.mComposerMap.gridAnnotationFormat()
            # self.mAnnotationFormatComboBox.setCurrentIndex(int(gf))
            #
            # #grid annotation position
            # self.initAnnotationPositionBox( self.mAnnotationPositionLeftComboBox, self.mComposerMap.gridAnnotationPosition( QgsComposerMap.Left ) )
            # self.initAnnotationPositionBox( self.mAnnotationPositionRightComboBox, self.mComposerMap.gridAnnotationPosition( QgsComposerMap.Right ) )
            # self.initAnnotationPositionBox( self.mAnnotationPositionTopComboBox, self.mComposerMap.gridAnnotationPosition( QgsComposerMap.Top ) )
            # self.initAnnotationPositionBox( self.mAnnotationPositionBottomComboBox, self.mComposerMap.gridAnnotationPosition( QgsComposerMap.Bottom ) )
            #
            # #grid annotation direction
            # self.initAnnotationDirectionBox( self.mAnnotationDirectionComboBoxLeft, self.mComposerMap.gridAnnotationDirection( QgsComposerMap.Left ) )
            # self.initAnnotationDirectionBox( self.mAnnotationDirectionComboBoxRight, self.mComposerMap.gridAnnotationDirection( QgsComposerMap.Right ) )
            # self.initAnnotationDirectionBox( self.mAnnotationDirectionComboBoxTop, self.mComposerMap.gridAnnotationDirection( QgsComposerMap.Top ) )
            # self.initAnnotationDirectionBox( self.mAnnotationDirectionComboBoxBottom, self.mComposerMap.gridAnnotationDirection( QgsComposerMap.Bottom ) )
            #
            # self.mAnnotationFontColorButton.setColor( self.mComposerMap.annotationFontColor() )
            #
            # self.mDistanceToMapFrameSpinBox.setValue( self.mComposerMap.annotationFrameDistance() )
            #
            # if ( self.mComposerMap.showGridAnnotation() ):
            #     self.mDrawAnnotationCheckableGroupBox.setChecked( True )
            # else:
            #     self.mDrawAnnotationCheckableGroupBox.setChecked( False )
            #
            # self.mCoordinatePrecisionSpinBox.setValue( self.mComposerMap.gridAnnotationPrecision() )

            #atlas controls
            self.mAtlasCheckBox.setChecked( self.mComposerMap.atlasDriven() )
            self.mAtlasMarginSpinBox.setValue( int(self.mComposerMap.atlasMargin(QgsComposerObject.OriginalValue)) * 100 )

            self.mAtlasFixedScaleRadio.setEnabled( self.mComposerMap.atlasDriven() );
            self.mAtlasFixedScaleRadio.setChecked( self.mComposerMap.atlasScalingMode() == QgsComposerMap.Fixed );
            self.mAtlasMarginSpinBox.setEnabled( self.mComposerMap.atlasScalingMode() == QgsComposerMap.Auto );
            self.mAtlasMarginRadio.setEnabled( self.mComposerMap.atlasDriven() );
            self.mAtlasMarginRadio.setChecked( self.mComposerMap.atlasScalingMode() == QgsComposerMap.Auto );
            self.mAtlasPredefinedScaleRadio.setEnabled( self.mComposerMap.atlasDriven() );
            self.mAtlasPredefinedScaleRadio.setChecked( self.mComposerMap.atlasScalingMode() == QgsComposerMap.Predefined );

            if ( self.mComposerMap.atlasDriven() ):
                self.toggleAtlasScalingOptionsByLayerType();
            # // disable predefined scales if none are defined
            if ( not self.hasPredefinedScales() ):
                self.mAtlasPredefinedScaleRadio.setEnabled( False );

            self.populateDataDefinedButtons();
            self.loadGridEntries();
            self.loadOverviewEntries();
            self.blockAllSignals( False );
            # if ( self.mComposerMap.atlasFixedScale() ):
            #     self.mAtlasFixedScaleRadio.setChecked( True )
            #     self.mAtlasMarginSpinBox.setEnabled( False )
            # else:
            #     self.mAtlasMarginRadio.setChecked( True )
            #     self.mAtlasMarginSpinBox.setEnabled( True )
            # if ( not self.mComposerMap.atlasDriven() ):
            #     self.mAtlasMarginSpinBox.setEnabled( False )
            #     self.mAtlasMarginRadio.setEnabled( False )
            #     self.mAtlasFixedScaleRadio.setEnabled( False )
            # else:
            #     self.mAtlasFixedScaleRadio.setEnabled( True )
            #     self.toggleAtlasMarginByLayerType()
            #
            # self.blockAllSignals( False )
    def toggleAtlasScalingOptionsByLayerType(self):
        if ( not self.mComposerMap ):
            return;

        # //get atlas coverage layer
        coverageLayer = self.atlasCoverageLayer();
        if ( not coverageLayer ):
            return;

        for case in switch ( coverageLayer.wkbType() ):
            if case(QGis.WKBPoint) and  case(QGis.WKBPoint25D) and case(QGis.WKBMultiPoint) and case(QGis.WKBMultiPoint25D):
            # //For point layers buffer setting makes no sense, so set "fixed scale" on and disable margin control
                self.mAtlasFixedScaleRadio.setChecked( True );
                self.mAtlasMarginRadio.setEnabled( False );
                self.mAtlasPredefinedScaleRadio.setEnabled( False );
                break;
            else:
            # //Not a point layer, so enable changes to fixed scale control
                self.mAtlasMarginRadio.setEnabled( True );
                self.mAtlasPredefinedScaleRadio.setEnabled( True );

    def toggleAtlasMarginByLayerType(self):
        if ( not self.mComposerMap ):
            return

        #get composition
        composition = self.mComposerMap.composition()
        if ( not composition ):
            return

        atlas = composition.atlasComposition()

        coverageLayer = atlas.coverageLayer()
        if ( not coverageLayer ):
            return

        if atlas.coverageLayer().wkbType() == QGis.WKBPoint or atlas.coverageLayer().wkbType() == QGis.WKBPoint25D or \
            atlas.coverageLayer().wkbType() == QGis.WKBMultiPoint or \
            atlas.coverageLayer().wkbType() == QGis.WKBMultiPoint25D:
        #For point layers buffer setting makes no sense, so set "fixed scale" on and disable margin control
            self.mAtlasFixedScaleRadio.setChecked( True )
            self.mAtlasMarginRadio.setEnabled( False )
        else:
        #Not a point layer, so enable changes to fixed scale control
            self.mAtlasMarginRadio.setEnabled( True )

    def updateComposerExtentFromGui(self):
        if ( not self.mComposerMap ):
            return

        # double xmin, ymin, xmax, ymax
        # bool conversionSuccess

        xmin, conversionSuccess = self.mXMinLineEdit.text().toDouble()
        if ( not conversionSuccess ):
            return
        xmax, conversionSuccess = self.mXMaxLineEdit.text().toDouble()
        if ( not conversionSuccess ):
            return
        ymin, conversionSuccess = self.mYMinLineEdit.text().toDouble()
        if ( not conversionSuccess ):
            return
        ymax, conversionSuccess = self.mYMaxLineEdit.text().toDouble()
        if ( not conversionSuccess ):
            return

        newExtent = QgsRectangle( xmin, ymin, xmax, ymax )
        self.mComposerMap.beginCommand( "Map extent changed" )
        self.mComposerMap.setNewExtent( newExtent )
        self.mComposerMap.endCommand()

    def blockAllSignals( self, b ):
        self.mScaleLineEdit.blockSignals( b )
        self.mXMinLineEdit.blockSignals( b )
        self.mXMaxLineEdit.blockSignals( b )
        self.mYMinLineEdit.blockSignals( b )
        self.mYMaxLineEdit.blockSignals( b )
        self.mDrawCanvasItemsCheckBox.blockSignals( b );
        self.mOverviewFrameMapComboBox.blockSignals( b );
        self.mOverviewFrameStyleButton.blockSignals( b );
        self.mOverviewBlendModeComboBox.blockSignals( b );
        self.mOverviewInvertCheckbox.blockSignals( b );
        self.mOverviewCenterCheckbox.blockSignals( b );
        self.mAtlasCheckBox.blockSignals( b );
        self.mAtlasMarginSpinBox.blockSignals( b );
        self.mAtlasFixedScaleRadio.blockSignals( b );
        self.mAtlasMarginRadio.blockSignals( b );
        self.mKeepLayerListCheckBox.blockSignals( b );
        self.mKeepLayerStylesCheckBox.blockSignals( b );
        self.mSetToMapCanvasExtentButton.blockSignals( b );
        self.mUpdatePreviewButton.blockSignals( b );

        self.blockGridItemsSignals( b );
        self.blockOverviewItemsSignals( b );

    def handleChangedFrameDisplay( self, border, mode ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( "Frame divisions changed" )
        grid.setFrameDivisions( mode, border );
        self.mComposerMap.endCommand();
        self.mComposerMap.updateBoundingRect();
    def handleChangedAnnotationDisplay( self, border, text ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( "Annotation display changed" )
        if ( text == "Show all" ):
            grid.setAnnotationDisplay( QgsComposerMapGrid.ShowAll, border );
        elif ( text == "Show latitude only" ):
            grid.setAnnotationDisplay( QgsComposerMapGrid.LatitudeOnly, border );
        elif ( text == "Show longitude only" ):
            grid.setAnnotationDisplay( QgsComposerMapGrid.LongitudeOnly, border );
        else:# //disabled
            grid.setAnnotationDisplay( QgsComposerMapGrid.HideAll, border );

        self.mComposerMap.updateBoundingRect();
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def on_mUpdatePreviewButton_clicked(self):
        if ( not self.mComposerMap ):
            return

        if ( self.mComposerMap.isDrawing() ):
            return

        self.mUpdatePreviewButton.setEnabled( False ) #prevent crashes because of many button clicks

        self.mComposerMap.setCacheUpdated( False )
        self.mComposerMap.cache()
        self.mComposerMap.update()

        self.mUpdatePreviewButton.setEnabled( True )

    def on_mKeepLayerListCheckBox_stateChanged( self, state ):
        if ( not self.mComposerMap ):
            return

        if ( state == Qt.Checked ):
            self.mComposerMap.storeCurrentLayerSet()
            self.mComposerMap.setKeepLayerSet( True )
        else:
            emptyLayerSet = QStringList()
            self.mComposerMap.setLayerSet( emptyLayerSet )
            self.mComposerMap.setKeepLayerSet( False )
            self.mKeepLayerStylesCheckBox.setChecked( Qt.Unchecked )
        self.mKeepLayerStylesCheckBox.setEnabled( state == Qt.Checked )

    def on_mKeepLayerStylesCheckBox_stateChanged( self, state ):
        if ( not self.mComposerMap ):
            return;

        if ( state == Qt.Checked ):
            self.mComposerMap.storeCurrentLayerStyles();
            self.mComposerMap.setKeepLayerStyles( True );
        else:
            self.mComposerMap.setLayerStyleOverrides( dict() );
            self.mComposerMap.setKeepLayerStyles( False );

    def on_mDrawCanvasItemsCheckBox_stateChanged( self, state ):
        if ( not self.mComposerMap ):
            return

        self.mComposerMap.beginCommand( "Canvas items toggled" )
        self.mComposerMap.setDrawCanvasItems( state == Qt.Checked )
        self.mUpdatePreviewButton.setEnabled( False ) #prevent crashes because of many button clicks
        self.mComposerMap.setCacheUpdated( False )
        self.mComposerMap.cache()
        self.mComposerMap.update()
        self.mUpdatePreviewButton.setEnabled( True )
        self.mComposerMap.endCommand()

    def on_mOverviewFrameMapComboBox_currentIndexChanged( self, text ):
        overview = self.currentOverview();
        if ( not overview ):
            return;

        # int id;
        id = None
        if ( text == QString( "None" ) ):
            id = -1;
        else:
            # //get composition
            composition = self.mComposerMap.composition();
            if ( not composition ):
                return;

            # //extract id
            conversionOk = False;
            textSplit = text.split( ' ' );
            if ( textSplit.size() < 1 ):
                return;

            idString = textSplit.at( textSplit.size() - 1 );
            id, conversionOk = idString.toInt();

            if ( not conversionOk ):
                return;

            composerMap = composition.getComposerMapById( id );
            if ( not composerMap ):
                return;

        self.mComposerMap.beginCommand( QString( "Overview map changed" ) );
        overview.setFrameMap( id );
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def on_mOverviewFrameStyleButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        overview = self.currentOverview();
        if ( not overview ):
            return;

        newSymbol = overview.frameSymbol().clone()
        d = QgsSymbolV2SelectorDialog( newSymbol, QgsStyleV2.defaultStyle(), None, self);

        if ( d.exec_() == QDialog.Accepted ):

            self.mComposerMap.beginCommand( QString( "Overview frame style changed" ) );
            overview.setFrameSymbol( newSymbol );
            self.updateOverviewFrameSymbolMarker( overview );
            self.mComposerMap.endCommand();
            self.mComposerMap.update();
        self.timeStart = time.time()

    def on_mOverviewBlendModeComboBox_currentIndexChanged( self, index ):
        overview = self.currentOverview();
        if ( not overview ):
            return;

        self.mComposerMap.beginCommand( QString( "Overview blend mode changed" ) );
        overview.setBlendMode( self.mOverviewBlendModeComboBox.blendMode() );
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def on_mOverviewInvertCheckbox_toggled( self, state ):
        overview = self.currentOverview();
        if ( not overview ):
            return;

        self.mComposerMap.beginCommand( QString( "Overview inverted toggled" ) );
        overview.setInverted( state );
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def on_mOverviewCenterCheckbox_toggled( self, state ):
        overview = self.currentOverview();
        if ( not overview ):
            return;

        self.mComposerMap.beginCommand( QString( "Overview centered toggled" ) );
        overview.setCentered( state );
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def on_mGridCheckBox_toggled( self, state ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( "Grid checkbox toggled" )
        if ( state ):
            grid.setEnabled( True )
        else:
            grid.setEnabled( False )
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mIntervalXSpinBox_editingFinished(self):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( "Grid interval changed" )
        grid.setIntervalX( self.mIntervalXSpinBox.value() );
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mIntervalYSpinBox_editingFinished(self):
        grid = self.currentGrid();
        if ( not grid ):
            return;
        self.mComposerMap.beginCommand( "Grid interval changed" )
        grid.setIntervalY( self.mIntervalYSpinBox.value() );
        # self.mComposerMap.setGridIntervalY( self.mIntervalYSpinBox.value() )
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mOffsetXSpinBox_valueChanged(self, value):
        grid = self.currentGrid();
        if ( not grid ):
            return;
        self.mComposerMap.beginCommand( "Grid offset changed" )
        # self.mComposerMap.setGridOffsetX( self.mOffsetXSpinBox.value() )
        grid.setOffsetX( self.mOffsetXSpinBox.value() )
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mOffsetYSpinBox_valueChanged(self, value):
        grid = self.currentGrid();
        if ( not grid ):
            return;
        self.mComposerMap.beginCommand( "Grid offset changed" )
        # self.mComposerMap.setGridOffsetY( self.mOffsetYSpinBox.value() )
        grid.setOffsetY( self.mOffsetYSpinBox.value() )
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mGridLineStyleButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        grid = self.currentGrid();
        if ( not grid ):
            return;

        newSymbol = grid.lineSymbol().clone()

        d = QgsSymbolV2SelectorDialog( self.mComposerMap.gridLineSymbol(), QgsStyleV2.defaultStyle(), None, self )
        if ( d.exec_() == QDialog.Accepted ):

            self.mComposerMap.beginCommand( QString( "Grid line style changed" ) );
            grid.setLineSymbol( newSymbol );
            self.updateGridLineSymbolMarker( grid );
            self.mComposerMap.endCommand();
            self.mComposerMap.update();
        self.timeStart = time.time()

    def on_mGridTypeComboBox_currentIndexChanged( self, text ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( QString( "Grid type changed" ) );
        if ( text == QString( "Cross" ) ):
            grid.setStyle( QgsComposerMapGrid.Cross );
            self.mCrossWidthSpinBox.setVisible( True );
            self.mCrossWidthLabel.setVisible( True );
            self.mGridLineStyleButton.setVisible( True );
            self.mLineStyleLabel.setVisible( True );
            self.mGridMarkerStyleButton.setVisible( False );
            self.mMarkerStyleLabel.setVisible( False );
            self.mGridBlendComboBox.setVisible( True );
            self.mGridBlendLabel.setVisible( True );
        elif ( text == QString( "Markers" ) ):
            grid.setStyle( QgsComposerMapGrid.Markers );
            self.mCrossWidthSpinBox.setVisible( False );
            self.mCrossWidthLabel.setVisible( False );
            self.mGridLineStyleButton.setVisible( False );
            self.mLineStyleLabel.setVisible( False );
            self.mGridMarkerStyleButton.setVisible( True );
            self.mMarkerStyleLabel.setVisible( True );
            self.mGridBlendComboBox.setVisible( True );
            self.mGridBlendLabel.setVisible( True );
        elif ( text == QString( "Solid" ) ):
            grid.setStyle( QgsComposerMapGrid.Solid );
            self.mCrossWidthSpinBox.setVisible( False );
            self.mCrossWidthLabel.setVisible( False );
            self.mGridLineStyleButton.setVisible( True );
            self.mLineStyleLabel.setVisible( True );
            self.mGridMarkerStyleButton.setVisible( False );
            self.mMarkerStyleLabel.setVisible( False );
            self.mGridBlendComboBox.setVisible( True );
            self.mGridBlendLabel.setVisible( True );
        else:
            grid.setStyle( QgsComposerMapGrid.FrameAnnotationsOnly );
            self.mCrossWidthSpinBox.setVisible( False );
            self.mCrossWidthLabel.setVisible( False );
            self.mGridLineStyleButton.setVisible( False );
            self.mLineStyleLabel.setVisible( False );
            self.mGridMarkerStyleButton.setVisible( False );
            self.mMarkerStyleLabel.setVisible( False );
            self.mGridBlendComboBox.setVisible( False );
            self.mGridBlendLabel.setVisible( False );

        self.mComposerMap.updateBoundingRect();
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def on_mCrossWidthSpinBox_valueChanged( self, d ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( "Grid cross width changed" )
        grid.setCrossLength( self.mCrossWidthSpinBox.value() )
        # self.mComposerMap.setCrossLength( d )
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mGridBlendComboBox_currentIndexChanged( self, index ):
        # Q_UNUSED( index )
        grid = self.currentGrid();
        if ( grid ):
            self.mComposerMap.beginCommand( QString( "Grid blend mode changed" ) );
            grid.setBlendMode( self.mGridBlendComboBox.blendMode() );
            self.mComposerMap.update();
            self.mComposerMap.endCommand();

    def on_mAnnotationFontButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        grid = self.currentGrid();
        if ( not grid ):
            return;

        # bool ok
        #if defined(Q_WS_MAC) and defined(QT_MAC_USE_COCOA)
        # Native Mac dialog works only for Qt Carbon
        # newFont, ok = QFontDialog.getFont( self.mComposerMap.gridAnnotationFont(), 0, QString(), QFontDialog.DontUseNativeDialog )
        #else
        newFont, ok = QFontDialog.getFont( grid.annotationFont() )
        #endif
        if ( ok ):

            self.mComposerMap.beginCommand( "Annotation font changed" )
            # self.mComposerMap.setGridAnnotationFont( newFont )
            grid.setAnnotationFont( newFont );
            self.mComposerMap.updateBoundingRect()
            self.mComposerMap.update()
            self.mComposerMap.endCommand()
        self.timeStart = time.time()

    def on_mAnnotationFontColorButton_colorChanged( self, newFontColor ):
        grid = self.currentGrid();
        if ( not grid ):
            return;
        self.mComposerMap.beginCommand( "Label font changed" )
        grid.setAnnotationFontColor( newFontColor);
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mDistanceToMapFrameSpinBox_valueChanged( self, d ):
        grid = self.currentGrid();
        if ( not grid ):
            return;
        self.mComposerMap.beginCommand( "Annotation distance changed" , QgsComposerMergeCommand.ComposerMapAnnotationDistance )
        # self.mComposerMap.setAnnotationFrameDistance( d )
        grid.setAnnotationFrameDistance( self.mDistanceToMapFrameSpinBox.value() )
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mAnnotationFormatComboBox_currentIndexChanged( self, index ):
        grid = self.currentGrid();
        if ( not grid ):
            return;
        self.mComposerMap.beginCommand( "Annotation format changed" )
        # self.mComposerMap.setGridAnnotationFormat(index )
        grid.setAnnotationFormat(self.mAnnotationFormatComboBox.itemData( index ).toInt()[0] );
        self.mAnnotationFormatButton.setEnabled( grid.annotationFormat() == QgsComposerMapGrid.CustomFormat );
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mAnnotationPositionLeftComboBox_currentIndexChanged( self, text ):
        self.handleChangedAnnotationPosition( QgsComposerMap.Left, text )

    def on_mAnnotationPositionRightComboBox_currentIndexChanged( self, text ):
        self.handleChangedAnnotationPosition( QgsComposerMap.Right, text )

    def on_mAnnotationPositionTopComboBox_currentIndexChanged( self, text ):
        self.handleChangedAnnotationPosition( QgsComposerMap.Top, text )

    def on_mAnnotationPositionBottomComboBox_currentIndexChanged( self, text ):
        self.handleChangedAnnotationPosition( QgsComposerMap.Bottom, text )

    def on_mDrawAnnotationCheckableGroupBox_toggled( self, state ):
        if ( not self.mComposerMap ):
            return

        self.mComposerMap.beginCommand( "Annotation toggled" )
        if ( state ):
            self.mComposerMap.setShowGridAnnotation( True )
        else:
            self.mComposerMap.setShowGridAnnotation( False )
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mAnnotationDirectionComboBoxLeft_currentIndexChanged( self, index ):
        self.handleChangedAnnotationDirection( QgsComposerMapGrid.Left, self.mAnnotationDirectionComboBoxLeft.itemData( index ).toInt()[0] );

    def on_mAnnotationDirectionComboBoxRight_currentIndexChanged( self, index):
        self.handleChangedAnnotationDirection( QgsComposerMapGrid.Right, self.mAnnotationDirectionComboBoxRight.itemData( index ).toInt()[0] )

    def on_mAnnotationDirectionComboBoxTop_currentIndexChanged( self, index ):
        self.handleChangedAnnotationDirection( QgsComposerMap.Top, self.mAnnotationDirectionComboBoxTop.itemData( index ).toInt()[0] )

    def on_mAnnotationDirectionComboBoxBottom_currentIndexChanged( self, index ):
        self.handleChangedAnnotationDirection( QgsComposerMap.Bottom, self.mAnnotationDirectionComboBoxBottom.itemData( index ).toInt()[0] )

    def on_mCoordinatePrecisionSpinBox_valueChanged( self, value ):
        grid = self.currentGrid();
        if ( not grid ):
            return;
        self.mComposerMap.beginCommand("Changed annotation precision" )
        # self.mComposerMap.setGridAnnotationPrecision( value )
        grid.setAnnotationPrecision( self.mCoordinatePrecisionSpinBox.value());
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def toggleFrameControls( self, frameEnabled, frameFillEnabled, frameSizeEnabled ):
        # //set status of frame controls
        self.mFrameWidthSpinBox.setEnabled( frameSizeEnabled );
        self.mGridFramePenSizeSpinBox.setEnabled( frameEnabled );
        self.mGridFramePenColorButton.setEnabled( frameEnabled );
        self.mGridFrameFill1ColorButton.setEnabled( frameFillEnabled );
        self.mGridFrameFill2ColorButton.setEnabled( frameFillEnabled );
        self.mFrameWidthLabel.setEnabled( frameSizeEnabled );
        self.mFramePenLabel.setEnabled( frameEnabled );
        self.mFrameFillLabel.setEnabled( frameFillEnabled );
        self.mCheckGridLeftSide.setEnabled( frameEnabled );
        self.mCheckGridRightSide.setEnabled( frameEnabled );
        self.mCheckGridTopSide.setEnabled( frameEnabled );
        self.mCheckGridBottomSide.setEnabled( frameEnabled );
        self.mFrameDivisionsLeftComboBox.setEnabled( frameEnabled );
        self.mFrameDivisionsRightComboBox.setEnabled( frameEnabled );
        self.mFrameDivisionsTopComboBox.setEnabled( frameEnabled );
        self.mFrameDivisionsBottomComboBox.setEnabled( frameEnabled );
        self.mLeftDivisionsLabel.setEnabled( frameEnabled );
        self.mRightDivisionsLabel.setEnabled( frameEnabled );
        self.mTopDivisionsLabel.setEnabled( frameEnabled );
        self.mBottomDivisionsLabel.setEnabled( frameEnabled );

    def on_mFrameStyleComboBox_currentIndexChanged( self, text ):
        # self.toggleFrameControls( text !=  "No frame" )

        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( "Changed grid frame style" )
        if ( text == "Zebra" ):
            # self.mComposerMap.setGridFrameStyle( QgsComposerMap.Zebra )
            grid.setFrameStyle( QgsComposerMapGrid.Zebra );
            self.toggleFrameControls( True, True, True );
        elif ( text == QString( "Interior ticks" ) ):
            grid.setFrameStyle( QgsComposerMapGrid.InteriorTicks );
            self.toggleFrameControls( True, False, True );
        elif ( text == QString( "Exterior ticks" ) ):
            grid.setFrameStyle( QgsComposerMapGrid.ExteriorTicks );
            self.toggleFrameControls( True, False, True );
        elif ( text == QString( "Interior and exterior ticks" ) ):
            grid.setFrameStyle( QgsComposerMapGrid.InteriorExteriorTicks );
            self.toggleFrameControls( True, False, True );
        elif ( text == QString( "Line border" ) ):
            grid.setFrameStyle( QgsComposerMapGrid.LineBorder );
            self.toggleFrameControls( True, False, False );
        else:# //no frame
            grid.setFrameStyle( QgsComposerMapGrid.NoFrame );
            self.toggleFrameControls( False, False, False );
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mFrameWidthSpinBox_valueChanged( self, d ):
        grid = self.currentGrid();
        if ( not grid ):
            return;
        self.mComposerMap.beginCommand( "Frame width changed" )
        # self.mComposerMap.setGridFrameWidth( d )
        grid.setFrameWidth( self.mFrameWidthSpinBox.value() )
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mGridFramePenSizeSpinBox_valueChanged( self, d ):
        grid = self.currentGrid();
        if ( not grid or not self.mComposerMap ):
            return;
        self.mComposerMap.beginCommand( "Changed grid frame line thickness" )
        # self.mComposerMap.setGridFramePenSize( d )
        grid.setFramePenSize( self.mGridFramePenSizeSpinBox.value() )
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mGridFramePenColorButton_colorChanged( self, newColor ):
        grid = self.currentGrid();
        if ( not grid or not self.mComposerMap ):
            return;
        self.mComposerMap.beginCommand( "Grid frame color changed" )
        # self.mComposerMap.setGridFramePenColor( newColor )
        grid.setFramePenColor( newColor )
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mGridFrameFill1ColorButton_colorChanged( self, newColor ):
        grid = self.currentGrid();
        if ( not grid or not self.mComposerMap ):
            return;
        self.mComposerMap.beginCommand( "Grid frame first fill color changed" )
        # self.mComposerMap.setGridFrameFillColor1( newColor )
        grid.setFrameFillColor1( newColor )
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def on_mGridFrameFill2ColorButton_colorChanged( self, newColor ):
        grid = self.currentGrid();
        if ( not grid or not self.mComposerMap ):
            return;
        self.mComposerMap.beginCommand( "Grid frame second fill color changed" )
        # self.mComposerMap.setGridFrameFillColor2( newColor )
        grid.setFrameFillColor2( newColor )
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def showEvent( self, event ):
        self.refreshMapComboBox()
        # QWidget.showEvent( event )

    def addPageToToolbox( self, widget, name ):
        # Q_UNUSED( name )
        #TODO : wrap the widget in a collapsibleGroupBox to be more consistent with previous implementation
        self.mainLayout.addWidget( widget )

    def insertAnnotationPositionEntries( self, c ):
        c.insertItem( 0, "Inside frame" )
        c.insertItem( 1, "Outside frame" )

    def insertAnnotationDirectionEntries( self, c ):
        c.addItem( "Horizontal" , QgsComposerMapGrid.Horizontal );
        c.addItem( "Vertical ascending" , QgsComposerMapGrid.Vertical );
        c.addItem( "Vertical descending" , QgsComposerMapGrid.VerticalDescending );

    def initFrameDisplayBox( self, c, display ):
        if ( not isinstance(c, QComboBox) ):
            return;
        c.setCurrentIndex( c.findData( display ) );

    def initAnnotationDisplayBox( self, c, display ):
        if ( not isinstance(c, QComboBox) ):
            return;

        if ( display == QgsComposerMapGrid.ShowAll ):
            c.setCurrentIndex( c.findText( "Show all" ) );
        elif ( display == QgsComposerMapGrid.LatitudeOnly ):
            c.setCurrentIndex( c.findText( "Show latitude only" ) )
        elif ( display == QgsComposerMapGrid.LongitudeOnly ):
            c.setCurrentIndex( c.findText( "Show longitude only" ) )
        else:
            c.setCurrentIndex( c.findText( "Disabled" ) )

    def handleChangedAnnotationPosition( self, border, text ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( "Annotation position changed" )
        if ( text == "Inside frame" ):
            grid.setAnnotationPosition( QgsComposerMapGrid.InsideMapFrame, border );
        elif ( text == "Disabled" ):
            grid.setAnnotationPosition( QgsComposerMapGrid.Disabled, border );
        else: #Outside frame
            grid.setAnnotationPosition( QgsComposerMapGrid.OutsideMapFrame, border )

        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def handleChangedAnnotationDirection( self, border, direction ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( "Changed annotation direction" )
        grid.setAnnotationDirection( direction, border )
        self.mComposerMap.updateBoundingRect()
        self.mComposerMap.update()
        self.mComposerMap.endCommand()

    def insertFrameDisplayEntries( self, c ):
        c.addItem( "All" , QgsComposerMapGrid.ShowAll );
        c.addItem( "Latitude/Y only" , QgsComposerMapGrid.LatitudeOnly );
        c.addItem( "Longitude/X only" , QgsComposerMapGrid.LongitudeOnly );

    def insertAnnotationDisplayEntries( self, c ):
        c.insertItem( 0, "Show all" )
        c.insertItem( 1, "Show latitude only" )
        c.insertItem( 2, "Show longitude only" )
        c.insertItem( 3, "Disabled" );

    def initAnnotationPositionBox( self, c, pos ):
        if ( not isinstance(c, QComboBox) ):
            return

        if ( pos == QgsComposerMap.InsideMapFrame ):
            c.setCurrentIndex( c.findText( "Inside frame" ) )
        else:
            c.setCurrentIndex( c.findText( "Outside frame" ) )

    def initAnnotationDirectionBox( self, c, dir ):
        if ( not isinstance(c, QComboBox) ):
            return

        c.setCurrentIndex( c.findData( dir ) )

    def updateOverviewSymbolMarker(self):
        if ( self.mComposerMap ):
            icon = QgsSymbolLayerV2Utils.symbolPreviewIcon( self.mComposerMap.overviewFrameMapSymbol(), self.mOverviewFrameStyleButton.iconSize() )
            self.mOverviewFrameStyleButton.setIcon( icon )

    def updateLineSymbolMarker(self):
        if ( self.mComposerMap ):
            icon = QgsSymbolLayerV2Utils.symbolPreviewIcon( self.mComposerMap.gridLineSymbol(), self.mGridLineStyleButton.iconSize() )
            self.mGridLineStyleButton.setIcon( icon )

    def refreshMapComboBox(self):
        if ( not self.mComposerMap ):
            return

        self.mOverviewFrameMapComboBox.blockSignals( True )

        #save the current entry in case it is still present after refresh
        saveComboText = self.mOverviewFrameMapComboBox.currentText()

        self.mOverviewFrameMapComboBox.clear()
        self.mOverviewFrameMapComboBox.addItem( "None", -1 )
        composition = self.mComposerMap.composition()
        if ( not composition ):
            return

        availableMaps = composition.composerMapItems()
        # QList<const QgsComposerMap*>.const_iterator mapItemIt = availableMaps.constBegin()
        for mapItemIt in availableMaps:
            if (mapItemIt.id() != self.mComposerMap.id() ):
                self.mOverviewFrameMapComboBox.addItem( QString("Map %1").arg(mapItemIt.id() ), mapItemIt.id() )


        if ( not saveComboText.isEmpty() ):
            saveTextIndex = self.mOverviewFrameMapComboBox.findText( saveComboText )
            if ( saveTextIndex == -1 ):
            #entry is no longer present
                self.mOverviewFrameMapComboBox.setCurrentIndex( self.mOverviewFrameMapComboBox.findText( "None" ) )
            else:
                self.mOverviewFrameMapComboBox.setCurrentIndex( saveTextIndex )

        self.mOverviewFrameMapComboBox.blockSignals( False )

    def atlasLayerChanged( self, layer ):
        if ( not layer or layer.wkbType() == QGis.WKBNoGeometry ):
            # //geometryless layer, disable atlas control
            self.mAtlasCheckBox.setChecked( False );
            self.mAtlasCheckBox.setEnabled( False );
            return;
        else:
            self.mAtlasCheckBox.setEnabled( True );

        # // enable or disable fixed scale control based on layer type
        if ( self.mAtlasCheckBox.isChecked() ):
            self.toggleAtlasScalingOptionsByLayerType();
    def hasPredefinedScales(self):
        # // first look at project's scales
        scales = QStringList( QgsProject.instance().readListEntry( "Scales", "/ScalesList" )[0] );
        hasProjectScales = QgsProject.instance().readBoolEntry( "Scales", "/useProjectScales" )[0] ;
        if ( not hasProjectScales or scales.isEmpty() ):
            # // default to global map tool scales
            settings = QSettings();
            scalesStr = QString( settings.value( "Map/scales", "" ).toString() );
            myScalesList = scalesStr.split( ',' );
            return not myScalesList.isEmpty() and myScalesList[0] != "";
        return True;

    def on_mAddGridPushButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        if ( not self.mComposerMap ):
            return;

        itemName = QString( "Grid %1" ).arg( self.mComposerMap.grids().size() + 1 );
        grid = QgsComposerMapGrid( itemName, self.mComposerMap );
        self.mComposerMap.beginCommand( QString( "Add map grid" ) );
        self.mComposerMap.grids().addGrid( grid );
        self.mComposerMap.endCommand();
        self.mComposerMap.updateBoundingRect();
        self.mComposerMap.update();

        self.addGridListItem( grid.id(), grid.name() );
        self.mGridListWidget.setCurrentRow( 0 );
        self.on_mGridListWidget_currentItemChanged( self.mGridListWidget.currentItem(), None);
        self.timeStart = time.time()

    def on_mRemoveGridPushButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        item = self.mGridListWidget.currentItem();
        if ( not item ):
            return;

        self.mComposerMap.grids().removeGrid( item.data( Qt.UserRole ).toString() );
        delItem = self.mGridListWidget.takeItem( self.mGridListWidget.row( item ) );
        # delete delItem;
        self.mComposerMap.updateBoundingRect();
        self.mComposerMap.update();
        self.timeStart = time.time()

    def on_mGridUpButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        item = self.mGridListWidget.currentItem();
        if ( not item ):
            return;

        row = self.mGridListWidget.row( item );
        if ( row < 1 ):
            return;
        self.mGridListWidget.takeItem( row );
        self.mGridListWidget.insertItem( row - 1, item );
        self.mGridListWidget.setCurrentItem( item );
        self.mComposerMap.grids().moveGridUp( item.data( Qt.UserRole ).toString() );
        self.mComposerMap.update();
        self.timeStart = time.time()

    def on_mGridDownButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        item = self.mGridListWidget.currentItem();
        if ( not item ):
            return

        row = self.mGridListWidget.row( item );
        if ( self.mGridListWidget.count() <= row ):
            return
        self.mGridListWidget.takeItem( row );
        self.mGridListWidget.insertItem( row + 1, item );
        self.mGridListWidget.setCurrentItem( item );
        self.mComposerMap.grids().moveGridDown( item.data( Qt.UserRole ).toString() );
        self.mComposerMap.update();
        self.timeStart = time.time()

    def currentGrid(self):
        if ( not self.mComposerMap ):
            return None

        item = self.mGridListWidget.currentItem();
        if ( not item ):
            return None

        return self.mComposerMap.grids().grid( item.data( Qt.UserRole ).toString() );
    def on_mGridListWidget_currentItemChanged( self, current, previous ):
        # Q_UNUSED( previous );
        if ( not current ):
            self.mGridCheckBox.setEnabled( False );
            return;

        self.mGridCheckBox.setEnabled( True );
        self.setGridItems( self.mComposerMap.grids().constGrid( current.data( Qt.UserRole ).toString() ) );

    def on_mGridListWidget_itemChanged( self, item ):
        if ( not self.mComposerMap ):
            return;

        grid = self.mComposerMap.grids().grid( item.data( Qt.UserRole ).toString() );
        if ( not grid ):
            return;

        grid.setName( item.text() );
        if ( item.isSelected() ):
            # //update check box title if item is current item
            self.mGridCheckBox.setTitle( QString( "Draw \"%1\" grid" ).arg( grid.name() ) );

    def setGridItemsEnabled( self, enabled ):
        self.mGridTypeComboBox.setEnabled( enabled );
        self.mIntervalXSpinBox.setEnabled( enabled );
        self.mIntervalYSpinBox.setEnabled( enabled );
        self.mOffsetXSpinBox.setEnabled( enabled );
        self.mOffsetYSpinBox.setEnabled( enabled );
        self.mCrossWidthSpinBox.setEnabled( enabled );
        self.mFrameStyleComboBox.setEnabled( enabled );
        self.mFrameWidthSpinBox.setEnabled( enabled );
        self.mGridLineStyleButton.setEnabled( enabled );
        self.mGridFramePenSizeSpinBox.setEnabled( enabled );
        self.mGridFramePenColorButton.setEnabled( enabled );
        self.mGridFrameFill1ColorButton.setEnabled( enabled );
        self.mGridFrameFill2ColorButton.setEnabled( enabled );
        self.mFrameDivisionsLeftComboBox.setEnabled( enabled );
        self.mFrameDivisionsRightComboBox.setEnabled( enabled );
        self.mFrameDivisionsTopComboBox.setEnabled( enabled );
        self.mFrameDivisionsBottomComboBox.setEnabled( enabled );

    def blockGridItemsSignals( self, block ):
        # //grid
        self.mGridCheckBox.blockSignals( block );
        self.mGridTypeComboBox.blockSignals( block );
        self.mIntervalXSpinBox.blockSignals( block );
        self.mIntervalYSpinBox.blockSignals( block );
        self.mOffsetXSpinBox.blockSignals( block );
        self.mOffsetYSpinBox.blockSignals( block );
        self.mCrossWidthSpinBox.blockSignals( block );
        self.mFrameStyleComboBox.blockSignals( block );
        self.mFrameWidthSpinBox.blockSignals( block );
        self.mGridLineStyleButton.blockSignals( block );
        self.mMapGridUnitComboBox.blockSignals( block );
        self.mGridFramePenSizeSpinBox.blockSignals( block );
        self.mGridFramePenColorButton.blockSignals( block );
        self.mGridFrameFill1ColorButton.blockSignals( block );
        self.mGridFrameFill2ColorButton.blockSignals( block );
        self.mGridBlendComboBox.blockSignals( block );
        self.mCheckGridLeftSide.blockSignals( block );
        self.mCheckGridRightSide.blockSignals( block );
        self.mCheckGridTopSide.blockSignals( block );
        self.mCheckGridBottomSide.blockSignals( block );
        self.mFrameDivisionsLeftComboBox.blockSignals( block );
        self.mFrameDivisionsRightComboBox.blockSignals( block );
        self.mFrameDivisionsTopComboBox.blockSignals( block );
        self.mFrameDivisionsBottomComboBox.blockSignals( block );

        # //grid annotation
        self.mDrawAnnotationGroupBox.blockSignals( block );
        self.mAnnotationFormatComboBox.blockSignals( block );
        self.mAnnotationDisplayLeftComboBox.blockSignals( block );
        self.mAnnotationPositionLeftComboBox.blockSignals( block );
        self.mAnnotationDirectionComboBoxLeft.blockSignals( block );
        self.mAnnotationDisplayRightComboBox.blockSignals( block );
        self.mAnnotationPositionRightComboBox.blockSignals( block );
        self.mAnnotationDirectionComboBoxRight.blockSignals( block );
        self.mAnnotationDisplayTopComboBox.blockSignals( block );
        self.mAnnotationPositionTopComboBox.blockSignals( block );
        self.mAnnotationDirectionComboBoxTop.blockSignals( block );
        self.mAnnotationDisplayBottomComboBox.blockSignals( block );
        self.mAnnotationPositionBottomComboBox.blockSignals( block );
        self.mAnnotationDirectionComboBoxBottom.blockSignals( block );
        self.mDistanceToMapFrameSpinBox.blockSignals( block );
        self.mCoordinatePrecisionSpinBox.blockSignals( block );
        self.mAnnotationFontColorButton.blockSignals( block );
        self.mAnnotationFontButton.blockSignals( block );

    def setGridItems( self, grid ):
        if ( not grid ):
            return;

        self.blockGridItemsSignals( True );

        self.mGridCheckBox.setTitle( QString( QString( "Draw \"%1\" grid" ) ).arg( grid.name() ) );
        self.mGridCheckBox.setChecked( grid.enabled() );
        self.mIntervalXSpinBox.setValue( grid.intervalX() );
        self.mIntervalYSpinBox.setValue( grid.intervalY() );
        self.mOffsetXSpinBox.setValue( grid.offsetX() );
        self.mOffsetYSpinBox.setValue( grid.offsetY() );
        self.mCrossWidthSpinBox.setValue( grid.crossLength() );
        self.mFrameWidthSpinBox.setValue( grid.frameWidth() );
        self.mGridFramePenSizeSpinBox.setValue( grid.framePenSize() );
        self.mGridFramePenColorButton.setColor( grid.framePenColor() );
        self.mGridFrameFill1ColorButton.setColor( grid.frameFillColor1() );
        self.mGridFrameFill2ColorButton.setColor( grid.frameFillColor2() );

        gridStyle = grid.style();
        for case in switch ( gridStyle ):
            if case(QgsComposerMapGrid.Cross):
                self.mGridTypeComboBox.setCurrentIndex( self.mGridTypeComboBox.findText( QString( "Cross" ) ) );
                self.mCrossWidthSpinBox.setVisible( True );
                self.mCrossWidthLabel.setVisible( True );
                self.mGridLineStyleButton.setVisible( True );
                self.mLineStyleLabel.setVisible( True );
                self.mGridMarkerStyleButton.setVisible( False );
                self.mMarkerStyleLabel.setVisible( False );
                self.mGridBlendComboBox.setVisible( True );
                self.mGridBlendLabel.setVisible( True );
                break;
            elif case(QgsComposerMapGrid.Markers):
                self.mGridTypeComboBox.setCurrentIndex( self.mGridTypeComboBox.findText( QString( "Markers" ) ) );
                self.mCrossWidthSpinBox.setVisible( False );
                self.mCrossWidthLabel.setVisible( False );
                self.mGridLineStyleButton.setVisible( False );
                self.mLineStyleLabel.setVisible( False );
                self.mGridMarkerStyleButton.setVisible( True );
                self.mMarkerStyleLabel.setVisible( True );
                self.mGridBlendComboBox.setVisible( True );
                self.mGridBlendLabel.setVisible( True );
                break;
            elif case(QgsComposerMapGrid.Solid):
                self.mGridTypeComboBox.setCurrentIndex( self.mGridTypeComboBox.findText( QString( "Solid" ) ) );
                self.mCrossWidthSpinBox.setVisible( False );
                self.mCrossWidthLabel.setVisible( False );
                self.mGridLineStyleButton.setVisible( True );
                self.mLineStyleLabel.setVisible( True );
                self.mGridMarkerStyleButton.setVisible( False );
                self.mMarkerStyleLabel.setVisible( False );
                self.mGridBlendComboBox.setVisible( True );
                self.mGridBlendLabel.setVisible( True );
                break;
            elif case(QgsComposerMapGrid.FrameAnnotationsOnly):
                self.mGridTypeComboBox.setCurrentIndex( self.mGridTypeComboBox.findText( QString( "Frame and annotations only" ) ) );
                self.mCrossWidthSpinBox.setVisible( False );
                self.mCrossWidthLabel.setVisible( False );
                self.mGridLineStyleButton.setVisible( False );
                self.mLineStyleLabel.setVisible( False );
                self.mGridMarkerStyleButton.setVisible( False );
                self.mMarkerStyleLabel.setVisible( False );
                self.mGridBlendComboBox.setVisible( False );
                self.mGridBlendLabel.setVisible( False );
                break;

        # //grid frame
        self.mFrameWidthSpinBox.setValue( grid.frameWidth() );
        gridFrameStyle = grid.frameStyle();
        for case in switch ( gridFrameStyle ):
            if case(QgsComposerMapGrid.Zebra):
                self.mFrameStyleComboBox.setCurrentIndex( 1 );
                self.toggleFrameControls( True, True, True );
                break;
            elif case(QgsComposerMapGrid.InteriorTicks):
                self.mFrameStyleComboBox.setCurrentIndex( 2 );
                self.toggleFrameControls( True, False, True );
                break;
            elif case(QgsComposerMapGrid.ExteriorTicks):
                self.mFrameStyleComboBox.setCurrentIndex( 3 );
                self.toggleFrameControls( True, False, True );
                break;
            elif case(QgsComposerMapGrid.InteriorExteriorTicks):
                self.mFrameStyleComboBox.setCurrentIndex( 4 );
                self.toggleFrameControls( True, False, True );
                break;
            elif case(QgsComposerMapGrid.LineBorder):
                self.mFrameStyleComboBox.setCurrentIndex( 5 );
                self.toggleFrameControls( True, False, False );
                break;
            else:
                self.mFrameStyleComboBox.setCurrentIndex( 0 );
                self.toggleFrameControls( False, False, False );
                break;

        self.mCheckGridLeftSide.setChecked( grid.testFrameSideFlag( QgsComposerMapGrid.FrameLeft ) );
        self.mCheckGridRightSide.setChecked( grid.testFrameSideFlag( QgsComposerMapGrid.FrameRight ) );
        self.mCheckGridTopSide.setChecked( grid.testFrameSideFlag( QgsComposerMapGrid.FrameTop ) );
        self.mCheckGridBottomSide.setChecked( grid.testFrameSideFlag( QgsComposerMapGrid.FrameBottom ) );

        self.initFrameDisplayBox( self.mFrameDivisionsLeftComboBox, grid.frameDivisions( QgsComposerMapGrid.Left ) );
        self.initFrameDisplayBox( self.mFrameDivisionsRightComboBox, grid.frameDivisions( QgsComposerMapGrid.Right ) );
        self.initFrameDisplayBox( self.mFrameDivisionsTopComboBox, grid.frameDivisions( QgsComposerMapGrid.Top ) );
        self.initFrameDisplayBox( self.mFrameDivisionsBottomComboBox, grid.frameDivisions( QgsComposerMapGrid.Bottom ) );

        # //line style
        self.updateGridLineSymbolMarker( grid );
        # //marker style
        self.updateGridMarkerSymbolMarker( grid );

        self.mGridBlendComboBox.setBlendMode( grid.blendMode() );

        self.mDrawAnnotationGroupBox.setChecked( grid.annotationEnabled() );
        self.initAnnotationDisplayBox( self.mAnnotationDisplayLeftComboBox, grid.annotationDisplay( QgsComposerMapGrid.Left ) );
        self.initAnnotationDisplayBox( self.mAnnotationDisplayRightComboBox, grid.annotationDisplay( QgsComposerMapGrid.Right ) );
        self.initAnnotationDisplayBox( self.mAnnotationDisplayTopComboBox, grid.annotationDisplay( QgsComposerMapGrid.Top ) );
        self.initAnnotationDisplayBox( self.mAnnotationDisplayBottomComboBox, grid.annotationDisplay( QgsComposerMapGrid.Bottom ) );

        self.initAnnotationPositionBox( self.mAnnotationPositionLeftComboBox, grid.annotationPosition( QgsComposerMapGrid.Left ) );
        self.initAnnotationPositionBox( self.mAnnotationPositionRightComboBox, grid.annotationPosition( QgsComposerMapGrid.Right ) );
        self.initAnnotationPositionBox( self.mAnnotationPositionTopComboBox, grid.annotationPosition( QgsComposerMapGrid.Top ) );
        self.initAnnotationPositionBox( self.mAnnotationPositionBottomComboBox, grid.annotationPosition( QgsComposerMapGrid.Bottom ) );

        self.initAnnotationDirectionBox( self.mAnnotationDirectionComboBoxLeft, grid.annotationDirection( QgsComposerMapGrid.Left ) );
        self.initAnnotationDirectionBox( self.mAnnotationDirectionComboBoxRight, grid.annotationDirection( QgsComposerMapGrid.Right ) );
        self.initAnnotationDirectionBox( self.mAnnotationDirectionComboBoxTop, grid.annotationDirection( QgsComposerMapGrid.Top ) );
        self.initAnnotationDirectionBox( self.mAnnotationDirectionComboBoxBottom, grid.annotationDirection( QgsComposerMapGrid.Bottom ) );

        self.mAnnotationFontColorButton.setColor( grid.annotationFontColor() );

        self.mAnnotationFormatComboBox.setCurrentIndex( self.mAnnotationFormatComboBox.findData( grid.annotationFormat() ) );
        self.mAnnotationFormatButton.setEnabled( grid.annotationFormat() == QgsComposerMapGrid.CustomFormat );
        self.mDistanceToMapFrameSpinBox.setValue( grid.annotationFrameDistance() );
        self.mCoordinatePrecisionSpinBox.setValue( grid.annotationPrecision() );

        # //Unit
        gridUnit = grid.units();
        if ( gridUnit == QgsComposerMapGrid.MapUnit ):
            self.mMapGridUnitComboBox.setCurrentIndex( self.mMapGridUnitComboBox.findText( QString( "Map unit" ) ) );
        elif ( gridUnit == QgsComposerMapGrid.MM ):
            self.mMapGridUnitComboBox.setCurrentIndex( self.mMapGridUnitComboBox.findText( QString( "Millimeter" ) ) );
        elif ( gridUnit == QgsComposerMapGrid.CM ):
            self.mMapGridUnitComboBox.setCurrentIndex( self.mMapGridUnitComboBox.findText( QString( "Centimeter" ) ) );

        # //CRS button
        gridCrs = grid.crs();
        crsButtonText = gridCrs.authid() if(gridCrs.isValid()) else QString( "change..." );
        self.mMapGridCRSButton.setText( crsButtonText );

        self.blockGridItemsSignals( False );

    def updateGridLineSymbolMarker( self, grid ):
        if ( grid ):
            nonConstSymbol = grid.lineSymbol() #); //bad
            icon = QgsSymbolLayerV2Utils.symbolPreviewIcon( nonConstSymbol, self.mGridLineStyleButton.iconSize() );
            self.mGridLineStyleButton.setIcon( icon );

    def updateGridMarkerSymbolMarker( self, grid ):
        if ( grid ):
            nonConstSymbol = grid.markerSymbol()# ); //bad
            icon = QgsSymbolLayerV2Utils.symbolPreviewIcon( nonConstSymbol, self.mGridMarkerStyleButton.iconSize() );
            self.mGridMarkerStyleButton.setIcon( icon );

    def on_mGridMarkerStyleButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        grid = self.currentGrid();
        if ( not grid ):
            return;

        newSymbol = grid.markerSymbol().clone()
        d = QgsSymbolV2SelectorDialog( newSymbol, QgsStyleV2.defaultStyle(), None, self);

        if ( d.exec_() == QDialog.Accepted ):

            self.mComposerMap.beginCommand( QString( "Grid markers style changed" ) );
            grid.setMarkerSymbol( newSymbol );
            self.updateGridMarkerSymbolMarker( grid );
            self.mComposerMap.endCommand();
            self.mComposerMap.update();
        self.timeStart = time.time()

    def on_mCheckGridLeftSide_toggled( self, checked ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( QString( "Frame left side changed" ) );
        grid.setFrameSideFlag( QgsComposerMapGrid.FrameLeft, checked );
        self.mComposerMap.updateBoundingRect();
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def on_mCheckGridRightSide_toggled( self, checked ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( QString( "Frame right side changed" ) );
        grid.setFrameSideFlag( QgsComposerMapGrid.FrameRight, checked );
        self.mComposerMap.updateBoundingRect();
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def on_mCheckGridTopSide_toggled( self, checked ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( QString( "Frame top side changed" ) );
        grid.setFrameSideFlag( QgsComposerMapGrid.FrameTop, checked );
        self.mComposerMap.updateBoundingRect();
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def on_mCheckGridBottomSide_toggled( self, checked ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( QString( "Frame bottom side changed" ) );
        grid.setFrameSideFlag( QgsComposerMapGrid.FrameBottom, checked );
        self.mComposerMap.updateBoundingRect();
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def on_mFrameDivisionsLeftComboBox_currentIndexChanged( self, index ):
        self.handleChangedFrameDisplay( QgsComposerMapGrid.Left, self.mFrameDivisionsLeftComboBox.itemData( self.mFrameDivisionsLeftComboBox.currentIndex() ).toInt()[0] );

    def on_mFrameDivisionsRightComboBox_currentIndexChanged( self, index ):
        self.handleChangedFrameDisplay( QgsComposerMapGrid.Right, self.mFrameDivisionsRightComboBox.itemData( self.mFrameDivisionsLeftComboBox.currentIndex() ).toInt()[0] );

    def on_mFrameDivisionsTopComboBox_currentIndexChanged( self, index ):
        self.handleChangedFrameDisplay( QgsComposerMapGrid.Top, self.mFrameDivisionsTopComboBox.itemData( self.mFrameDivisionsLeftComboBox.currentIndex() ).toInt()[0] );

    def on_mFrameDivisionsBottomComboBox_currentIndexChanged( self, index ):
        self.handleChangedFrameDisplay( QgsComposerMapGrid.Bottom, self.mFrameDivisionsBottomComboBox.itemData( self.mFrameDivisionsLeftComboBox.currentIndex() ).toInt()[0] );

    def on_mMapGridUnitComboBox_currentIndexChanged( self, text ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( QString( "Changed grid unit" ) );
        if ( text == QString( "Map unit" ) ):
            grid.setUnits( QgsComposerMapGrid.MapUnit );
        elif ( text == QString( "Millimeter" ) ):
            grid.setUnits( QgsComposerMapGrid.MM );
        elif ( text == QString( "Centimeter" ) ):
            grid.setUnits( QgsComposerMapGrid.CM );
        self.mComposerMap.updateBoundingRect();
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def on_mMapGridCRSButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        grid = self.currentGrid();
        if ( not grid or not self.mComposerMap ):
            return;

        crsDialog = QgsGenericProjectionSelector( self );
        crs = grid.crs();
        currentAuthId = crs.authid() if(crs.isValid()) else self.mComposerMap.composition().mapSettings().destinationCrs().authid()
        crsDialog.setSelectedAuthId( currentAuthId );

        if ( crsDialog.exec_() == QDialog.Accepted ):

            # self.mComposerMap.beginCommand( QString( "Grid CRS changed" ) );
            selectedAuthId = crsDialog.selectedAuthId();
            grid.setCrs( QgsCoordinateReferenceSystem( selectedAuthId ) );
            self.mComposerMap.updateBoundingRect();
            self.mMapGridCRSButton.setText( selectedAuthId );
            # self.mComposerMap.endCommand();
        self.timeStart = time.time()

    def on_mDrawAnnotationGroupBox_toggled( self, state ):
        grid = self.currentGrid();
        if ( not grid ):
            return;

        self.mComposerMap.beginCommand( QString( "Annotation toggled" ) );
        grid.setAnnotationEnabled( state );
        self.mComposerMap.updateBoundingRect();
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def on_mAnnotationFormatButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        grid = self.currentGrid();
        if ( not grid ):
            return;

        expressionContext = grid.createExpressionContext()

        exprDlg = QgsExpressionBuilderDialog( None, grid.annotationExpression(), self, "generic", expressionContext );
        exprDlg.setWindowTitle( QString( "Expression based annotation" ) );

        if ( exprDlg.exec_() == QDialog.Accepted ):

            expression =  exprDlg.expressionText();
            self.mComposerMap.beginCommand( QString( "Annotation format changed" ) );
            grid.setAnnotationExpression( expression );
            self.mComposerMap.updateBoundingRect();
            self.mComposerMap.update();
            self.mComposerMap.endCommand();
        self.timeStart = time.time()
    def on_mAnnotationDisplayLeftComboBox_currentIndexChanged( self, text ):
        self.handleChangedAnnotationDisplay( QgsComposerMapGrid.Left, text );

    def on_mAnnotationDisplayRightComboBox_currentIndexChanged( self, text ):
        self.handleChangedAnnotationDisplay( QgsComposerMapGrid.Right, text );

    def on_mAnnotationDisplayTopComboBox_currentIndexChanged( self, text ):
        self.handleChangedAnnotationDisplay( QgsComposerMapGrid.Top, text );

    def on_mAnnotationDisplayBottomComboBox_currentIndexChanged( self, text ):
        self.handleChangedAnnotationDisplay( QgsComposerMapGrid.Bottom, text );

    def addGridListItem( self, id, name ):
        item = QListWidgetItem( name, None);
        item.setData( Qt.UserRole, id );
        item.setFlags( Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable );
        self.mGridListWidget.insertItem( 0, item );
        return item;

    def loadGridEntries(self):
        # //save selection
        # QSet<QString> selectedIds;
        selectedIds = []
        itemSelection = self.mGridListWidget.selectedItems();
        # QList<QListWidgetItem*>.const_iterator sIt = itemSelection.constBegin();
        for sIt in itemSelection:
            selectedIds.append(sIt.data( Qt.UserRole ).toString()[0] );

        self.mGridListWidget.clear();
        if ( not self.mComposerMap ):
            return;

        # //load all composer grids into list widget
        grids = self.mComposerMap.grids().asList();
        # QList< QgsComposerMapGrid* >.const_iterator gridIt = grids.constBegin();
        for gridIt in grids:
            item = self.addGridListItem(gridIt.id(), gridIt.name() );
            if ( selectedIds.__contains__(gridIt.id() )):
                item.setSelected( True );
                self.mGridListWidget.setCurrentItem( item );

        if ( self.mGridListWidget.currentItem() ):
            self.on_mGridListWidget_currentItemChanged( self.mGridListWidget.currentItem(), None);
        else:
            self.on_mGridListWidget_currentItemChanged( None, None);

    def on_mAddOverviewPushButton_clicked(self):
        if ( not self.mComposerMap ):
            return;

        itemName = QString( "Overview %1" ).arg( self.mComposerMap.overviews().size() + 1 );
        overview = QgsComposerMapOverview( itemName, self.mComposerMap );
        self.mComposerMap.beginCommand( QString( "Add map overview" ) );
        self.mComposerMap.overviews().addOverview( overview );
        self.mComposerMap.endCommand();
        self.mComposerMap.update();

        self.addOverviewListItem( overview.id(), overview.name() );
        self.mOverviewListWidget.setCurrentRow( 0 );

    def on_mRemoveOverviewPushButton_clicked(self):
        item = self.mOverviewListWidget.currentItem();
        if ( not item ):
            return;

        self.mComposerMap.overviews().removeOverview( item.data( Qt.UserRole ).toString() );
        delItem = self.mOverviewListWidget.takeItem( self.mOverviewListWidget.row( item ) );
        # delete delItem;
        self.mComposerMap.update();

    def on_mOverviewUpButton_clicked(self):
        item = self.mOverviewListWidget.currentItem();
        if ( not item ):
            return;

        row = self.mOverviewListWidget.row( item );
        if ( row < 1 ):
            return;
        self.mOverviewListWidget.takeItem( row );
        self.mOverviewListWidget.insertItem( row - 1, item );
        self.mOverviewListWidget.setCurrentItem( item );
        self.mComposerMap.overviews().moveOverviewUp( item.data( Qt.UserRole ).toString() );
        self.mComposerMap.update();

    def on_mOverviewDownButton_clicked(self):
        item = self.mOverviewListWidget.currentItem();
        if ( not item ):
            return;

        row = self.mOverviewListWidget.row( item );
        if ( self.mOverviewListWidget.count() <= row ):
            return
        self.mOverviewListWidget.takeItem( row );
        self.mOverviewListWidget.insertItem( row + 1, item );
        self.mOverviewListWidget.setCurrentItem( item );
        self.mComposerMap.overviews().moveOverviewDown( item.data( Qt.UserRole ).toString() );
        self.mComposerMap.update();

    def currentOverview(self):
        if ( not self.mComposerMap ):
            return None

        item = self.mOverviewListWidget.currentItem();
        if ( not item ):
            return None

        return self.mComposerMap.overviews().overview( item.data( Qt.UserRole ).toString() );

    def on_mOverviewListWidget_currentItemChanged( self, current, previous ):
        if ( not current ):
            self.mOverviewCheckBox.setEnabled( False );
            return;

        self.mOverviewCheckBox.setEnabled( True );
        self.setOverviewItems( self.mComposerMap.overviews().constOverview( current.data( Qt.UserRole ).toString() ) );

    def on_mOverviewListWidget_itemChanged( self, item ):
        if ( not self.mComposerMap ):
            return

        overview = self.mComposerMap.overviews().overview( item.data( Qt.UserRole ).toString() );
        if ( not overview ):
            return;

        overview.setName( item.text() );
        if ( item.isSelected() ):
        # //update check box title if item is current item
            self.mOverviewCheckBox.setTitle( QString( QString( "Draw \"%1\" overview" ) ).arg( overview.name() ) );

    def setOverviewItemsEnabled( self, enabled ):
        self.mOverviewFrameMapLabel.setEnabled( enabled );
        self.mOverviewFrameMapComboBox.setEnabled( enabled );
        self.mOverviewFrameStyleLabel.setEnabled( enabled );
        self.mOverviewFrameStyleButton.setEnabled( enabled );
        self.mOverviewBlendModeLabel.setEnabled( enabled );
        self.mOverviewBlendModeComboBox.setEnabled( enabled );
        self.mOverviewInvertCheckbox.setEnabled( enabled );
        self.mOverviewCenterCheckbox.setEnabled( enabled );

    def blockOverviewItemsSignals( self, block ):
        # //grid
        self.mOverviewFrameMapComboBox.blockSignals( block );
        self.mOverviewFrameStyleButton.blockSignals( block );
        self.mOverviewBlendModeComboBox.blockSignals( block );
        self.mOverviewInvertCheckbox.blockSignals( block );
        self.mOverviewCenterCheckbox.blockSignals( block );

    def setOverviewItems( self, overview ):
        if ( not overview ):
            return;

        self.blockOverviewItemsSignals( True );

        self.mOverviewCheckBox.setTitle( QString( QString( "Draw \"%1\" overview" ) ).arg( overview.name() ) );
        self.mOverviewCheckBox.setChecked( overview.enabled() );

        # //overview frame
        self.refreshMapComboBox();
        overviewMapFrameId = overview.frameMapId();
        self.mOverviewFrameMapComboBox.setCurrentIndex( self.mOverviewFrameMapComboBox.findData( overviewMapFrameId ) );
        # //overview frame blending mode
        self.mOverviewBlendModeComboBox.setBlendMode( overview.blendMode() );
        # //overview inverted
        self.mOverviewInvertCheckbox.setChecked( overview.inverted() );
        # //center overview
        self.mOverviewCenterCheckbox.setChecked( overview.centered() );

        # //frame style
        self.updateOverviewFrameSymbolMarker( overview );

        self.blockOverviewItemsSignals( False );

    def updateOverviewFrameSymbolMarker( self, overview ):
        if ( overview ):
            nonConstSymbol = overview.frameSymbol()# ); //bad
            icon = QgsSymbolLayerV2Utils.symbolPreviewIcon( nonConstSymbol, self.mOverviewFrameStyleButton.iconSize() );
            self.mOverviewFrameStyleButton.setIcon( icon );

    def addOverviewListItem( self, id, name ):
        item = QListWidgetItem( name, None);
        item.setData( Qt.UserRole, id );
        item.setFlags( Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable );
        self.mOverviewListWidget.insertItem( 0, item );
        return item;

    def loadOverviewEntries(self):
        # //save selection
        # QSet<QString> selectedIds;
        selectedIds = []
        itemSelection = self.mOverviewListWidget.selectedItems();
        # QList<QListWidgetItem*>::const_iterator sIt = itemSelection.constBegin();
        for sIt in itemSelection:
            selectedIds.append(sIt.data( Qt.UserRole ).toString() );

        self.mOverviewListWidget.clear();
        if ( not self.mComposerMap ):
            return;

        # //load all composer overviews into list widget
        overviews = self.mComposerMap.overviews().asList();
        # QList< QgsComposerMapOverview* >::const_iterator overviewIt = overviews.constBegin();
        for overviewIt in overviews:
            item = self.addOverviewListItem(overviewIt.id(), overviewIt.name() );
            if ( selectedIds.__contains__(overviewIt.id() ) ):
                item.setSelected( True );
                self.mOverviewListWidget.setCurrentItem( item );

        if ( self.mOverviewListWidget.currentItem() ):
            self.on_mOverviewListWidget_currentItemChanged( self.mOverviewListWidget.currentItem(), None);
        else:
            self.on_mOverviewListWidget_currentItemChanged( None, None);

    def on_mOverviewCheckBox_toggled( self, state ):
        overview = self.currentOverview();
        if ( not overview ):
            return;

        self.mComposerMap.beginCommand( QString( "Overview checkbox toggled" ) );
        if ( state ):
            overview.setEnabled( True );
        else:
            overview.setEnabled( False );
        self.mComposerMap.update();
        self.mComposerMap.endCommand();

    def atlasComposition(self):
        if ( not self.mComposerMap ):
            return None;
        composition = self.mComposerMap.composition();

        if ( not composition ):
            return None;

        return composition.atlasComposition();
    def atlasCoverageLayer(self):
        atlasMap = self.atlasComposition();

        if ( atlasMap and atlasMap.enabled() ):
            return atlasMap.coverageLayer();

        return None;
    def updateDataDefinedProperty(self):
        #match data defined button to item's data defined property

        ddButton = self.sender()
        ddButton._class_ = QgsDataDefinedButton
        if ( not isinstance(ddButton, QgsDataDefinedButton) ):
            return;
        property = self.ddPropertyForWidget( ddButton );
        if ( property == QgsComposerObject.NoProperty ):
            return;

        #set the data defined property and refresh the item
        self.setDataDefinedProperty( ddButton, property );
        self.mComposerMap.refreshDataDefinedProperty( property );
    def setDataDefinedProperty( self, ddBtn, p ):
        if ( not self.mComposerObject ):
            return;

        map = ddBtn.definedProperty();
        self.mComposerMap.setDataDefinedProperty( p, map.value( "active" ).toInt(), map.value( "useexpr" ).toInt(), map.value( "expression" ), map.value( "field" ) );

