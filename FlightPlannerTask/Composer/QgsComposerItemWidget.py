
from PyQt4 import uic
from PyQt4.QtGui import QWidget, QButtonGroup, QDoubleValidator, QColorDialog
from PyQt4.QtCore import SIGNAL, SLOT, QString, Qt
from Composer.ui_qgscomposeritemwidget import Ui_QgsComposerItemWidgetBase
# s = QString("q")
# s.toDouble()

from qgis.core import QgsComposerMap, QgsExpressionContextScope, QgsExpressionContext, QgsComposerItem, QgsComposerMergeCommand, QgsExpressionContextUtils, QgsComposerObject
from qgis.gui import QgsDataDefinedButton
import define
# FORM_CLASS, _ = uic.loadUiType(define.appPath + "/UI/Composer/qgsComposerItemWidgetBase.ui")

class QgsComposerItemWidget(Ui_QgsComposerItemWidgetBase):
    def __init__(self, parent, item):
        Ui_QgsComposerItemWidgetBase.__init__(self, parent, item)
        
        # self.setupUi( self )

        self.mItem = item
        self.mFreezeXPosSpin = False
        self.mFreezeYPosSpin = False
        self.mFreezeWidthSpin = False
        self.mFreezeHeightSpin = False
        self.mFreezePageSpin = False
        #make button exclusive
        buttonGroup = QButtonGroup( self )
        buttonGroup.addButton( self.mUpperLeftCheckBox )
        buttonGroup.addButton( self.mUpperMiddleCheckBox )
        buttonGroup.addButton( self.mUpperRightCheckBox )
        buttonGroup.addButton( self.mMiddleLeftCheckBox )
        buttonGroup.addButton( self.mMiddleCheckBox )
        buttonGroup.addButton( self.mMiddleRightCheckBox )
        buttonGroup.addButton( self.mLowerLeftCheckBox )
        buttonGroup.addButton( self.mLowerMiddleCheckBox )
        buttonGroup.addButton( self.mLowerRightCheckBox )
        buttonGroup.setExclusive( True )
        
        # self.mXLineEdit.setValidator( QDoubleValidator( 0 ) )
        # self.mYLineEdit.setValidator( QDoubleValidator( 0 ) )
        # self.mWidthLineEdit.setValidator( QDoubleValidator( 0 ) )
        # self.mHeightLineEdit.setValidator( QDoubleValidator( 0 ) )
        
        self.setValuesForGuiElements()
        self.connect( self.mItem.composition(), SIGNAL( "paperSizeChanged()" ), self.setValuesForGuiPositionElements);
        self.connect( self.mItem, SIGNAL( "sizeChanged()" ), self.setValuesForGuiPositionElements )
        self.connect( self.mItem, SIGNAL( "itemChanged()" ), self.setValuesForGuiNonPositionElements);

        
        self.connect( self.mTransparencySlider, SIGNAL( "valueChanged( int )" ), self.mTransparencySpnBx, SLOT( "setValue( int )" ) )
        self.updateVariables();
        self.connect( self.mVariableEditor, SIGNAL( "scopeChanged()" ), self.variablesChanged);
        # listen out for variable edits
        # QgsApplication* app = qobject_cast<QgsApplication*>( QgsApplication.instance() );
        # if ( app )
        # {
        # self.connect( app, SIGNAL( settingsChanged() ), this, SLOT( updateVariables() ) );
        # }
        # self.connect( QgsProject.instance(), SIGNAL( variablesChanged() ), this, SLOT( updateVariables() ) );
        if ( self.mItem.composition() ):
            self.connect( self.mItem.composition(), SIGNAL( "variablesChanged()" ), self.updateVariables);
        
        #self.connect atlas signals to data defined buttons
        atlas = self.atlasComposition();
        if ( atlas ):
            #repopulate data defined buttons if atlas layer changes
            self.connect( atlas, SIGNAL( "coverageLayerChanged( QgsVectorLayer* )" ),
                 self.populateDataDefinedButtons);
            self.connect( atlas, SIGNAL( "toggled( bool )" ), self.populateDataDefinedButtons);
        
        #self.connect data defined buttons
        self.connect( self.mXPositionDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mXPositionDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);
        
        self.connect( self.mYPositionDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mYPositionDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);
        
        self.connect( self.mWidthDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mWidthDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);
        
        self.connect( self.mHeightDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mHeightDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);
        
        self.connect( self.mItemRotationDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mItemRotationDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);
        
        self.connect( self.mTransparencyDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mTransparencyDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);
        
        self.connect( self.mBlendModeDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mBlendModeDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);
        
        self.connect( self.mExcludePrintsDDBtn, SIGNAL( "dataDefinedChanged( const QString& )" ), self.updateDataDefinedProperty);
        self.connect( self.mExcludePrintsDDBtn, SIGNAL( "dataDefinedActivated( bool )" ), self.updateDataDefinedProperty);
       
        
        #content in QgsComposerItemWidget.h file
        self.mFrameColorButton.colorChanged.connect(self.on_mFrameColorButton_colorChanged)
        self.mBackgroundColorButton.clicked.connect(self.on_mBackgroundColorButton_clicked)
        self.mBackgroundColorButton.colorChanged.connect(self.on_mBackgroundColorButton_colorChanged)
        self.connect( self.mOutlineWidthSpinBox, SIGNAL( "valueChanged( double )" ), self.on_mOutlineWidthSpinBox_valueChanged);


        self.mFrameGroupBox.toggled.connect(self.on_mFrameGroupBox_toggled)
        self.mFrameJoinStyleCombo.currentIndexChanged.connect(self.on_mFrameJoinStyleCombo_currentIndexChanged)
        self.mBackgroundGroupBox.toggled.connect(self.on_mBackgroundGroupBox_toggled)

        self.mItemIdLineEdit.editingFinished.connect(self.on_mItemIdLineEdit_editingFinished)
        self.mPageSpinBox.valueChanged.connect(self.on_mPageSpinBox_valueChanged)
        self.mXPosSpin.valueChanged.connect(self.on_mXPosSpin_valueChanged)
        self.mYPosSpin.valueChanged.connect(self.on_mYPosSpin_valueChanged)
        self.mWidthSpin.valueChanged.connect(self.on_mWidthSpin_valueChanged)
        self.mHeightSpin.valueChanged.connect(self.on_mHeightSpin_valueChanged)

        self.mUpperLeftCheckBox.stateChanged.connect(self.on_mUpperLeftCheckBox_stateChanged)
        self.mUpperMiddleCheckBox.stateChanged.connect(self.on_mUpperMiddleCheckBox_stateChanged)
        self.mUpperRightCheckBox.stateChanged.connect(self.on_mUpperRightCheckBox_stateChanged)
        self.mMiddleLeftCheckBox.stateChanged.connect(self.on_mMiddleLeftCheckBox_stateChanged)
        self.mMiddleCheckBox.stateChanged.connect(self.on_mMiddleCheckBox_stateChanged)
        self.mMiddleRightCheckBox.stateChanged.connect(self.on_mMiddleRightCheckBox_stateChanged)
        self.mLowerLeftCheckBox.stateChanged.connect(self.on_mLowerLeftCheckBox_stateChanged)
        self.mLowerMiddleCheckBox.stateChanged.connect(self.on_mLowerMiddleCheckBox_stateChanged)
        self.mLowerRightCheckBox.stateChanged.connect(self.on_mLowerRightCheckBox_stateChanged)

        self.mBlendModeCombo.currentIndexChanged.connect(self.on_mBlendModeCombo_currentIndexChanged)
        self.mTransparencySpnBx.valueChanged.connect(self.on_mTransparencySpnBx_valueChanged)
        self.connect( self.mItemRotationSpinBox, SIGNAL( "valueChanged( double )" ), self.on_mItemRotationSpinBox_valueChanged);

        self.mExcludeFromPrintsCheckBox.toggled.connect(self.on_mExcludeFromPrintsCheckBox_toggled)
    def updateVariables(self):
        context = self.mItem.createExpressionContext();
        self.mVariableEditor.setContext( context );
        editableIndex = context.indexOfScope( QgsExpressionContextScope("Composer Item" ));
        if ( editableIndex >= 0 ):
            self.mVariableEditor.setEditableScopeIndex( editableIndex );
        # delete context;

    def showBackgroundGroup( self, showGroup ):
        self.mBackgroundGroupBox.setVisible( showGroup )

    def showFrameGroup( self, showGroup ):
        self.mFrameGroupBox.setVisible( showGroup )

#slots
    def on_mFrameColorButton_clicked(self):
        if ( not self.mItem ):
            return

    def on_mFrameColorButton_colorChanged( self, newFrameColor ):
        if ( not self.mItem ):
            return
        self.mItem.beginCommand( "Frame color changed" )
        self.mItem.setFrameOutlineColor( newFrameColor )
        self.mItem.update()
        self.mItem.endCommand()

    def on_mBackgroundColorButton_clicked(self):
        if ( not self.mItem ):
            return

    def on_mBackgroundColorButton_colorChanged( self, newBackgroundColor ):
        if ( not self.mItem ):
            return
        self.mItem.beginCommand( "Background color changed" )
        self.mItem.setBackgroundColor( newBackgroundColor )
        
        #if the item is a composer map, we need to regenerate the map image
        #because it usually is cached
        a = ""
        self.mItem._class_ = QgsComposerMap
        cm = self.mItem
        if ( isinstance(cm, QgsComposerMap) ):
            cm.cache()
        self.mItem.update()
        self.mItem.endCommand()

    def changeItemPosition(self):
        self.mItem.beginCommand( "Item position changed" )
        
        x = self.mXPosSpin.value();
        y = self.mYPosSpin.value();
        width = self.mWidthSpin.value();
        height = self.mHeightSpin.value();

        self.mItem.setItemPosition( x, y, width, height, self.positionMode(), False, self.mPageSpinBox.value() )
        
        self.mItem.update()
        self.mItem.endCommand()
    def variablesChanged(self):
        QgsExpressionContextUtils.setComposerItemVariables( self.mItem, self.mVariableEditor.variablesInActiveScope() );
    def positionMode(self):
        if ( self.mUpperLeftCheckBox.checkState() == Qt.Checked ):
            return QgsComposerItem.UpperLeft
        elif ( self.mUpperMiddleCheckBox.checkState() == Qt.Checked ):
            return QgsComposerItem.UpperMiddle
        elif ( self.mUpperRightCheckBox.checkState() == Qt.Checked ):
            return QgsComposerItem.UpperRight
        elif ( self.mMiddleLeftCheckBox.checkState() == Qt.Checked ):
            return QgsComposerItem.MiddleLeft
        elif ( self.mMiddleCheckBox.checkState() == Qt.Checked ):
            return QgsComposerItem.Middle
        elif ( self.mMiddleRightCheckBox.checkState() == Qt.Checked ):
            return QgsComposerItem.MiddleRight
        elif ( self.mLowerLeftCheckBox.checkState() == Qt.Checked ):
            return QgsComposerItem.LowerLeft
        elif ( self.mLowerMiddleCheckBox.checkState() == Qt.Checked ):
            return QgsComposerItem.LowerMiddle
        elif ( self.mLowerRightCheckBox.checkState() == Qt.Checked ):
            return QgsComposerItem.LowerRight
        return QgsComposerItem.UpperLeft

    def on_mOutlineWidthSpinBox_valueChanged( self, d ):
        if ( not self.mItem ):
            return
        
        self.mItem.beginCommand( "Item outline width" , QgsComposerMergeCommand.ItemOutlineWidth )
        self.mItem.setFrameOutlineWidth( self.mOutlineWidthSpinBox.value() )
        self.mItem.endCommand()
    def on_mFrameJoinStyleCombo_currentIndexChanged( self, index ):
        # Q_UNUSED( index );
        if ( not self.mItem ):
            return;

        self.mItem.beginCommand( "Item frame join style" )
        self.mItem.setFrameJoinStyle( self.mFrameJoinStyleCombo.penJoinStyle() );
        self.mItem.endCommand();
    def on_mFrameGroupBox_toggled( self, state ):
        if ( not self.mItem ):
            return
        
        self.mItem.beginCommand( "Item frame toggled" )
        self.mItem.setFrameEnabled( state )
        self.mItem.update()
        self.mItem.endCommand()

    def on_mBackgroundGroupBox_toggled( self, state ):
        if ( not self.mItem ):
            return
        
        self.mItem.beginCommand( "Item background toggled" )
        self.mItem.setBackgroundEnabled( state )
        
        #if the item is a composer map, we need to regenerate the map image
        #because it usually is cached
        self.mItem._class_ = QgsComposerMap
        cm = self.mItem
        if ( isinstance(cm, QgsComposerMap )):
            cm.cache()
        
        self.mItem.update()
        self.mItem.endCommand()

    def setValuesForGuiPositionElements(self):
        if ( not self.mItem ):
            return
        
        self.mXPosSpin.blockSignals( True );
        self.mYPosSpin.blockSignals( True );
        self.mWidthSpin.blockSignals( True );
        self.mHeightSpin.blockSignals( True );
        self.mUpperLeftCheckBox.blockSignals( True );
        self.mUpperMiddleCheckBox.blockSignals( True );
        self.mUpperRightCheckBox.blockSignals( True );
        self.mMiddleLeftCheckBox.blockSignals( True );
        self.mMiddleCheckBox.blockSignals( True );
        self.mMiddleRightCheckBox.blockSignals( True );
        self.mLowerLeftCheckBox.blockSignals( True );
        self.mLowerMiddleCheckBox.blockSignals( True );
        self.mLowerRightCheckBox.blockSignals( True );
        self.mPageSpinBox.blockSignals( True );
        
        pos = self.mItem.pagePos();
        
        if ( self.mItem.lastUsedPositionMode() == QgsComposerItem.UpperLeft ):
            self.mUpperLeftCheckBox.setChecked( True );
            if ( not self.mFreezeXPosSpin ):
                self.mXPosSpin.setValue( pos.x() );
            if ( not self.mFreezeYPosSpin ):
                self.mYPosSpin.setValue( pos.y() );
        
        if ( self.mItem.lastUsedPositionMode() == QgsComposerItem.UpperMiddle ):
            self.mUpperMiddleCheckBox.setChecked( True );
            if ( not self.mFreezeXPosSpin ):
                self.mXPosSpin.setValue( pos.x() + self.mItem.rect().width() / 2.0 );
            if ( not self.mFreezeYPosSpin ):
                self.mYPosSpin.setValue( pos.y() );
        
        if ( self.mItem.lastUsedPositionMode() == QgsComposerItem.UpperRight ):
            self.mUpperRightCheckBox.setChecked( True );
            if ( not self.mFreezeXPosSpin ):
                self.mXPosSpin.setValue( pos.x() + self.mItem.rect().width() );
            if ( not self.mFreezeYPosSpin ):
                self.mYPosSpin.setValue( pos.y() );
        
        if ( self.mItem.lastUsedPositionMode() == QgsComposerItem.MiddleLeft ):
            self.mMiddleLeftCheckBox.setChecked( True );
            if ( not self.mFreezeXPosSpin ):
                self.mXPosSpin.setValue( pos.x() );
            if ( not self.mFreezeYPosSpin ):
                self.mYPosSpin.setValue( pos.y() + self.mItem.rect().height() / 2.0 );
        
        if ( self.mItem.lastUsedPositionMode() == QgsComposerItem.Middle ):
            self.mMiddleCheckBox.setChecked( True );
            if ( not self.mFreezeXPosSpin ):
                self.mXPosSpin.setValue( pos.x() + self.mItem.rect().width() / 2.0 );
            if ( not self.mFreezeYPosSpin ):
                self.mYPosSpin.setValue( pos.y() + self.mItem.rect().height() / 2.0 );
        
        if ( self.mItem.lastUsedPositionMode() == QgsComposerItem.MiddleRight ):
            self.mMiddleRightCheckBox.setChecked( True );
            if ( not self.mFreezeXPosSpin ):
                self.mXPosSpin.setValue( pos.x() + self.mItem.rect().width() );
            if ( not self.mFreezeYPosSpin ):
                self.mYPosSpin.setValue( pos.y() + self.mItem.rect().height() / 2.0 );
        
        if ( self.mItem.lastUsedPositionMode() == QgsComposerItem.LowerLeft ):
            self.mLowerLeftCheckBox.setChecked( True );
            if ( not self.mFreezeXPosSpin ):
                self.mXPosSpin.setValue( pos.x() );
            if ( not self.mFreezeYPosSpin ):
                self.mYPosSpin.setValue( pos.y() + self.mItem.rect().height() );
        
        if ( self.mItem.lastUsedPositionMode() == QgsComposerItem.LowerMiddle ):
            self.mLowerMiddleCheckBox.setChecked( True );
            if ( not self.mFreezeXPosSpin ):
                self.mXPosSpin.setValue( pos.x() + self.mItem.rect().width() / 2.0 );
            if ( not self.mFreezeYPosSpin ):
                self.mYPosSpin.setValue( pos.y() + self.mItem.rect().height() );
        
        if ( self.mItem.lastUsedPositionMode() == QgsComposerItem.LowerRight ):
            self.mLowerRightCheckBox.setChecked( True );
            if ( not self.mFreezeXPosSpin ):
                self.mXPosSpin.setValue( pos.x() + self.mItem.rect().width() );
            if ( not self.mFreezeYPosSpin ):
                self.mYPosSpin.setValue( pos.y() + self.mItem.rect().height() );
        
        if ( not self.mFreezeWidthSpin ):
            self.mWidthSpin.setValue( self.mItem.rect().width() );
        if ( not self.mFreezeHeightSpin ):
            self.mHeightSpin.setValue( self.mItem.rect().height() );
        if ( not self.mFreezePageSpin ):
            self.mPageSpinBox.setValue( self.mItem.page() );
        
        self.mXPosSpin.blockSignals( False );
        self.mYPosSpin.blockSignals( False );
        self.mWidthSpin.blockSignals( False );
        self.mHeightSpin.blockSignals( False );
        self.mUpperLeftCheckBox.blockSignals( False );
        self.mUpperMiddleCheckBox.blockSignals( False );
        self.mUpperRightCheckBox.blockSignals( False );
        self.mMiddleLeftCheckBox.blockSignals( False );
        self.mMiddleCheckBox.blockSignals( False );
        self.mMiddleRightCheckBox.blockSignals( False );
        self.mLowerLeftCheckBox.blockSignals( False );
        self.mLowerMiddleCheckBox.blockSignals( False );
        self.mLowerRightCheckBox.blockSignals( False );
        self.mPageSpinBox.blockSignals( False );
    def setValuesForGuiNonPositionElements(self):
        if ( not self.mItem ):
            return;
        
        self.mOutlineWidthSpinBox.blockSignals( True );
        self.mFrameGroupBox.blockSignals( True );
        self.mBackgroundGroupBox.blockSignals( True );
        self.mItemIdLineEdit.blockSignals( True );
        self.mBlendModeCombo.blockSignals( True );
        self.mTransparencySlider.blockSignals( True );
        self.mTransparencySpnBx.blockSignals( True );
        self.mFrameColorButton.blockSignals( True );
        self.mFrameJoinStyleCombo.blockSignals( True );
        self.mBackgroundColorButton.blockSignals( True );
        self.mItemRotationSpinBox.blockSignals( True );
        self.mExcludeFromPrintsCheckBox.blockSignals( True );
        
        self.mBackgroundColorButton.setColor( self.mItem.backgroundColor() );
        self.mFrameColorButton.setColor( self.mItem.frameOutlineColor() );
        self.mOutlineWidthSpinBox.setValue( self.mItem.frameOutlineWidth() );
        self.mFrameJoinStyleCombo.setPenJoinStyle( self.mItem.frameJoinStyle() );
        self.mItemIdLineEdit.setText( str(self.mItem.id()) );
        self.mFrameGroupBox.setChecked( self.mItem.hasFrame() );
        self.mBackgroundGroupBox.setChecked( self.mItem.hasBackground() );
        self.mBlendModeCombo.setBlendMode( self.mItem.blendMode() );
        self.mTransparencySlider.setValue( self.mItem.transparency() );
        self.mTransparencySpnBx.setValue( self.mItem.transparency() );
        self.mItemRotationSpinBox.setValue( self.mItem.itemRotation( QgsComposerObject.OriginalValue ) );
        self.mExcludeFromPrintsCheckBox.setChecked( self.mItem.excludeFromExports( QgsComposerObject.OriginalValue ) );
        
        self.mBackgroundColorButton.blockSignals( False );
        self.mFrameColorButton.blockSignals( False );
        self.mFrameJoinStyleCombo.blockSignals( False );
        self.mOutlineWidthSpinBox.blockSignals( False );
        self.mFrameGroupBox.blockSignals( False );
        self.mBackgroundGroupBox.blockSignals( False );
        self.mItemIdLineEdit.blockSignals( False );
        self.mBlendModeCombo.blockSignals( False );
        self.mTransparencySlider.blockSignals( False );
        self.mTransparencySpnBx.blockSignals( False );
        self.mItemRotationSpinBox.blockSignals( False );
        self.mExcludeFromPrintsCheckBox.blockSignals( False );
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
            # button.registerGetExpressionContextCallback( _getExpressionContext, mItem );
        
        #initialise buttons to use atlas coverage layer
        self.mXPositionDDBtn.init( vl, self.mItem.dataDefinedProperty( QgsComposerObject.PositionX ),
                             QgsDataDefinedButton.AnyType, QgsDataDefinedButton.doubleDesc() );
        self.mYPositionDDBtn.init( vl, self.mItem.dataDefinedProperty( QgsComposerObject.PositionY ),
                             QgsDataDefinedButton.AnyType, QgsDataDefinedButton.doubleDesc() );
        self.mWidthDDBtn.init( vl, self.mItem.dataDefinedProperty( QgsComposerObject.ItemWidth ),
                         QgsDataDefinedButton.AnyType, QgsDataDefinedButton.doubleDesc() );
        self.mHeightDDBtn.init( vl, self.mItem.dataDefinedProperty( QgsComposerObject.ItemHeight ),
                          QgsDataDefinedButton.AnyType, QgsDataDefinedButton.doubleDesc() );
        self.mItemRotationDDBtn.init( vl, self.mItem.dataDefinedProperty( QgsComposerObject.ItemRotation ),
                                QgsDataDefinedButton.AnyType, QgsDataDefinedButton.double180RotDesc() );
        self.mTransparencyDDBtn.init( vl, self.mItem.dataDefinedProperty( QgsComposerObject.Transparency ),
                                QgsDataDefinedButton.AnyType, QgsDataDefinedButton.intTranspDesc() );
        self.mBlendModeDDBtn.init( vl, self.mItem.dataDefinedProperty( QgsComposerObject.BlendMode ),
                             QgsDataDefinedButton.String, QgsDataDefinedButton.blendModesDesc() );
        self.mExcludePrintsDDBtn.init( vl, self.mItem.dataDefinedProperty( QgsComposerObject.ExcludeFromExports ),
                                 QgsDataDefinedButton.String, QgsDataDefinedButton.boolDesc() );
        
        #unblock signals from data defined buttons
        for button in self.findChildren(QgsDataDefinedButton):
            button.blockSignals( False );

    def ddPropertyForWidget( self, widget ):
        if ( widget == self.mXPositionDDBtn ):
            return QgsComposerObject.PositionX;
        elif ( widget == self.mYPositionDDBtn ):
            return QgsComposerObject.PositionY
        elif ( widget == self.mWidthDDBtn ):
            return QgsComposerObject.ItemWidth
        elif ( widget == self.mHeightDDBtn ):
            return QgsComposerObject.ItemHeight
        elif ( widget == self.mItemRotationDDBtn ):
            return QgsComposerObject.ItemRotation
        elif ( widget == self.mTransparencyDDBtn ):
            return QgsComposerObject.Transparency
        elif ( widget == self.mBlendModeDDBtn ):
            return QgsComposerObject.BlendMode
        elif ( widget == self.mExcludePrintsDDBtn ):
            return QgsComposerObject.ExcludeFromExports
        
        return QgsComposerObject.NoProperty;




    def setValuesForGuiElements(self):
        if ( not self.mItem ):
            return
        self.mBackgroundColorButton.setColorDialogTitle( "Select background color" );
        self.mBackgroundColorButton.setAllowAlpha( True );
        self.mBackgroundColorButton.setContext( "composer" );
        self.mFrameColorButton.setColorDialogTitle( "Select frame color" );
        self.mFrameColorButton.setAllowAlpha( True );
        self.mFrameColorButton.setContext( "composer" );
        
        self.setValuesForGuiPositionElements();
        self.setValuesForGuiNonPositionElements();
        self.populateDataDefinedButtons();
        # self.setValuesForGuiPositionElements()
        # 
        # self.mOutlineWidthSpinBox.blockSignals( True )
        # self.mFrameGroupBox.blockSignals( True )
        # self.mBackgroundGroupBox.blockSignals( True )
        # self.mItemIdLineEdit.blockSignals( True )
        # self.mBlendModeCombo.blockSignals( True )
        # self.mTransparencySlider.blockSignals( True )
        # self.mTransparencySpnBx.blockSignals( True )
        # self.mFrameColorButton.blockSignals( True )
        # self.mBackgroundColorButton.blockSignals( True )
        # self.mItemRotationSpinBox.blockSignals( True )
        # 
        # self.mBackgroundColorButton.setColor( self.mItem.brush().color() )
        # self.mBackgroundColorButton.setColorDialogTitle( "Select background color" )
        # self.mBackgroundColorButton.setColorDialogOptions( QColorDialog.ShowAlphaChannel )
        # self.mFrameColorButton.setColor( self.mItem.pen().color() )
        # self.mFrameColorButton.setColorDialogTitle( "Select frame color" )
        # self.mFrameColorButton.setColorDialogOptions( QColorDialog.ShowAlphaChannel )
        # self.mOutlineWidthSpinBox.setValue( self.mItem.pen().widthF() )
        # self.mItemIdLineEdit.setText( self.mItem.id() )
        # self.mFrameGroupBox.setChecked( self.mItem.hasFrame() )
        # self.mBackgroundGroupBox.setChecked( self.mItem.hasBackground() )
        # self.mBlendModeCombo.setBlendMode( self.mItem.blendMode() )
        # self.mTransparencySlider.setValue( self.mItem.transparency() )
        # self.mTransparencySpnBx.setValue( self.mItem.transparency() )
        # self.mItemRotationSpinBox.setValue( self.mItem.itemRotation() )
        # 
        # self.mBackgroundColorButton.blockSignals( False )
        # self.mFrameColorButton.blockSignals( False )
        # self.mOutlineWidthSpinBox.blockSignals( False )
        # self.mFrameGroupBox.blockSignals( False )
        # self.mBackgroundGroupBox.blockSignals( False )
        # self.mItemIdLineEdit.blockSignals( False )
        # self.mBlendModeCombo.blockSignals( False )
        # self.mTransparencySlider.blockSignals( False )
        # self.mTransparencySpnBx.blockSignals( False )
        # self.mItemRotationSpinBox.blockSignals( False )

    def on_mBlendModeCombo_currentIndexChanged( self, index ):
        # Q_UNUSED( index )
        if ( self.mItem ):
            self.mItem.setBlendMode( self.mBlendModeCombo.blendMode() )
    def on_mTransparencySpnBx_valueChanged( self, value ):
        self.mTransparencySlider.blockSignals( True );
        self.mTransparencySlider.setValue( value );
        self.mTransparencySlider.blockSignals( False );
        if ( self.mItem ):
            self.mItem.beginCommand( "Item transparency changed" , QgsComposerMergeCommand.ItemTransparency );
            self.mItem.setTransparency( value );
            self.mItem.endCommand();
    # def on_mTransparencySlider_valueChanged( self, value ):
    #     if ( self.mItem ):
    #         self.mItem.setTransparency( int(value) )

    def on_mPageSpinBox_valueChanged( self ):
        self.mFreezePageSpin = True;
        self.changeItemPosition();
        self.mFreezePageSpin = False;
        
    def on_mXPosSpin_valueChanged( self ):
        self.mFreezeXPosSpin = True;
        self.changeItemPosition();
        self.mFreezeXPosSpin = False;

    def on_mYPosSpin_valueChanged( self):
        self.mFreezeYPosSpin = True;
        self.changeItemPosition();
        self.mFreezeYPosSpin = False;

    def on_mWidthSpin_valueChanged( self):
        self.mFreezeWidthSpin = True;
        self.changeItemPosition();
        self.mFreezeWidthSpin = False;

    def on_mHeightSpin_valueChanged( self):
        self.mFreezeHeightSpin = True;
        self.changeItemPosition();
        self.mFreezeHeightSpin = False;

    def on_mItemIdLineEdit_editingFinished(self):
        if ( self.mItem ):
            self.mItem.beginCommand( "Item id changed", QgsComposerMergeCommand.ComposerLabelSetId )
            self.mItem.setId( self.mItemIdLineEdit.text() )
            self.mItemIdLineEdit.setText( self.mItem.id() )
            self.mItem.endCommand()

    def on_mUpperLeftCheckBox_stateChanged( self, state ):
        if ( state != Qt.Checked ):
            return
        if ( self.mItem ):
            self.mItem.setItemPosition( self.mItem.pos().x(), self.mItem.pos().y(), QgsComposerItem.UpperLeft )
        self.setValuesForGuiPositionElements()

    def on_mUpperMiddleCheckBox_stateChanged( self, state ):
        if ( state != Qt.Checked ):
            return
        if ( self.mItem ):
            self.mItem.setItemPosition( self.mItem.pos().x() + self.mItem.rect().width() / 2.0,
                                        self.mItem.pos().y(), QgsComposerItem.UpperMiddle )
        self.setValuesForGuiPositionElements()

    def on_mUpperRightCheckBox_stateChanged( self, state ):
        if ( state != Qt.Checked ):
            return
        if ( self.mItem ):
            self.mItem.setItemPosition( self.mItem.pos().x() + self.mItem.rect().width(),
                                        self.mItem.pos().y(), QgsComposerItem.UpperRight )
        self.setValuesForGuiPositionElements()

    def on_mMiddleLeftCheckBox_stateChanged( self, state ):
        if ( state != Qt.Checked ):
            return
        if ( self.mItem ):
            self.mItem.setItemPosition( self.mItem.pos().x(),
                                        self.mItem.pos().y() + self.mItem.rect().height() / 2.0,
                                        QgsComposerItem.MiddleLeft )
        self.setValuesForGuiPositionElements()

    def on_mMiddleCheckBox_stateChanged( self, state ):
        if ( state != Qt.Checked ):
            return
        if ( self.mItem ):
            self.mItem.setItemPosition( self.mItem.pos().x() + self.mItem.rect().width() / 2.0,
                                        self.mItem.pos().y() + self.mItem.rect().height() / 2.0, QgsComposerItem.Middle )
        self.setValuesForGuiPositionElements()

    def on_mMiddleRightCheckBox_stateChanged( self, state ):
        if ( state != Qt.Checked ):
            return
        if ( self.mItem ):
            self.mItem.setItemPosition( self.mItem.pos().x() + self.mItem.rect().width(),
                                        self.mItem.pos().y() + self.mItem.rect().height() / 2.0, QgsComposerItem.MiddleRight )
        self.setValuesForGuiPositionElements()

    def on_mLowerLeftCheckBox_stateChanged( self, state ):
        if ( state != Qt.Checked ):
            return
        if ( self.mItem ):
            self.mItem.setItemPosition( self.mItem.pos().x(),
                                        self.mItem.pos().y() + self.mItem.rect().height(), QgsComposerItem.LowerLeft )
        self.setValuesForGuiPositionElements()

    def on_mLowerMiddleCheckBox_stateChanged( self, state ):
        if ( state != Qt.Checked ):
            return
        if ( self.mItem ):
            self.mItem.setItemPosition( self.mItem.pos().x() + self.mItem.rect().width() / 2.0,
                                    self.mItem.pos().y() + self.mItem.rect().height(), QgsComposerItem.LowerMiddle )
        self.setValuesForGuiPositionElements()

    def on_mLowerRightCheckBox_stateChanged( self, state ):
        if ( state != Qt.Checked ):
            return
        if ( self.mItem ):
            self.mItem.setItemPosition( self.mItem.pos().x() + self.mItem.rect().width(),
                                    self.mItem.pos().y() + self.mItem.rect().height(), QgsComposerItem.LowerRight )
        self.setValuesForGuiPositionElements()

    def on_mItemRotationSpinBox_valueChanged( self, val ):
        if ( self.mItem ):
            self.mItem.beginCommand( "Item rotation changed", QgsComposerMergeCommand.ItemRotation )
            self.mItem.setItemRotation( self.mItemRotationSpinBox.value(), True)#QString(val).mid(0, QString(val).length() - 1).toDouble()[0], True )
            self.mItem.update()
            self.mItem.endCommand()
    
    def on_mExcludeFromPrintsCheckBox_toggled( self, checked ):
        if ( self.mItem ):
            self.mItem.beginCommand( "Exclude from exports changed" )
            self.mItem.setExcludeFromExports( checked );
            self.mItem.endCommand();