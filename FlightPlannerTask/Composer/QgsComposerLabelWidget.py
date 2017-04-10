
from PyQt4.QtGui import QWidget, QMenu, QDoubleValidator, QColorDialog,\
    QDialog, QFontDialog, QIcon, QPixmap, QAction, QComboBox, QListWidgetItem, QTextCursor
from PyQt4 import uic
from PyQt4.QtCore import SIGNAL, SLOT, QString, Qt, QStringList, QSettings
from Composer.QgsComposerItemWidget import QgsComposerItemWidget

from qgis.core import QgsComposition, QgsComposerMap, QgsComposerMergeCommand, QGis, QgsRectangle, QgsStyleV2,\
    QgsSymbolLayerV2Utils, QgsComposerMapGrid, QgsExpressionContext, QgsComposerObject, QgsProject, QgsCoordinateReferenceSystem,\
    QgsComposerMapOverview
from qgis.gui import QgsSymbolV2SelectorDialog, QgsDataDefinedButton, QgsGenericProjectionSelector, QgsExpressionBuilderDialog
import define, time
from Type.switch import switch

from Composer.ui_qgscomposerlabelwidget import Ui_QgsComposerLabelWidgetBase
from Composer.ui_qgscomposeritemwidget import Ui_QgsComposerItemWidgetBase
# FORM_CLASS, _ = uic.loadUiType(define.appPath + "/UI/Composer/qgsComposerMapWidgetBase.ui")

class QgsComposerLabelWidget(Ui_QgsComposerLabelWidgetBase):
    def __init__(self, parent, composerLabel):
        Ui_QgsComposerLabelWidgetBase.__init__(self, parent, composerLabel)

        self.mComposerLabel = composerLabel
        
        itemPropertiesWidget = QgsComposerItemWidget( self, self.mComposerLabel )
        self.mainLayout.addWidget( itemPropertiesWidget )
        
        self.mFontColorButton.setColorDialogTitle( "Select font color" )
        self.mFontColorButton.setContext( "composer" )
        
        self.mMarginXDoubleSpinBox.setClearValue( 0.0 )
        self.mMarginYDoubleSpinBox.setClearValue( 0.0 )
        
        if ( self.mComposerLabel ):
            self.setGuiElementValues()
            self.connect( self.mComposerLabel, SIGNAL( "itemChanged()" ), self.setGuiElementValues)

        self.timeStart = 0
        self.timeEnd = 0
    def on_mHtmlCheckBox_stateChanged( self, state ):
        if ( self.mComposerLabel ):
            if ( state ):
                self.mFontButton.setEnabled( False )
                self.mFontColorButton.setEnabled( False )
                self.mAppearanceGroup.setEnabled( False )
            else:
                self.mFontButton.setEnabled( True )
                self.mFontColorButton.setEnabled( True )
                self.mAppearanceGroup.setEnabled( True )

            self.mComposerLabel.beginCommand( QString( "Label text HTML state changed" ), QgsComposerMergeCommand.ComposerLabelSetText )
            self.mComposerLabel.blockSignals( True )
            self.mComposerLabel.setHtmlState( state )
            self.mComposerLabel.setText( self.mTextEdit.toPlainText() )
            self.mComposerLabel.update()
            self.mComposerLabel.blockSignals( False )
            self.mComposerLabel.endCommand()
    def on_mTextEdit_textChanged(self):
        if ( self.mComposerLabel ):
            self.mComposerLabel.beginCommand( QString( "Label text changed" ), QgsComposerMergeCommand.ComposerLabelSetText )
            self.mComposerLabel.blockSignals( True )
            self.mComposerLabel.setText( self.mTextEdit.toPlainText() )
            self.mComposerLabel.update()
            self.mComposerLabel.blockSignals( False )
            self.mComposerLabel.endCommand()

    def on_mFontButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        if ( self.mComposerLabel ):
            # bool ok
            newFont, ok = QFontDialog.getFont( self.mComposerLabel.font() )
            if ( ok ):

                self.mComposerLabel.beginCommand( QString( "Label font changed" ) )
                self.mComposerLabel.setFont( newFont )
                self.mComposerLabel.update()
                self.mComposerLabel.endCommand()
        self.timeStart = time.time()

    def on_mMarginXDoubleSpinBox_valueChanged( self, d ):
        if ( self.mComposerLabel ):
            self.mComposerLabel.beginCommand( QString( "Label margin changed" ) )
            self.mComposerLabel.setMarginX( self.mMarginXDoubleSpinBox.value() )
            self.mComposerLabel.update()
            self.mComposerLabel.endCommand()

    def on_mMarginYDoubleSpinBox_valueChanged( self, d ):
        if ( self.mComposerLabel ):
            self.mComposerLabel.beginCommand( QString( "Label margin changed" ) )
            self.mComposerLabel.setMarginY( self.mMarginYDoubleSpinBox.value() )
            self.mComposerLabel.update()
            self.mComposerLabel.endCommand()

    def on_mFontColorButton_colorChanged( self, newLabelColor ):
        if ( not self.mComposerLabel ):
            return

        self.mComposerLabel.beginCommand( QString( "Label color changed" ) )
        self.mComposerLabel.setFontColor( newLabelColor )
        self.mComposerLabel.update()
        self.mComposerLabel.endCommand()

    def on_mInsertExpressionButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        if ( not self.mComposerLabel ):
            return

        selText = self.mTextEdit.textCursor().selectedText()

        #edit the selected expression if there's one
        if ( selText.startsWith( "[%" ) and selText.endsWith( "%]" ) ):
            selText = selText.mid( 2, selText.size() - 4 )

        #use the atlas coverage layer, if any
        coverageLayer = self.atlasCoverageLayer()
        context = self.mComposerLabel.createExpressionContext()
        exprDlg = QgsExpressionBuilderDialog( coverageLayer, selText, self, "generic", context )

        exprDlg.setWindowTitle( QString( "Insert expression" ) )
        if ( exprDlg.exec_() == QDialog.Accepted ):

            expression =  exprDlg.expressionText()
            if ( not expression.isEmpty() ):
                self.mComposerLabel.beginCommand( QString( "Insert expression" ) )
                self.mTextEdit.insertPlainText( "[%" + expression + "%]" )
                self.mComposerLabel.endCommand()
        self.timeStart = time.time()

    def on_mCenterRadioButton_clicked(self):
        if ( self.mComposerLabel ):
            self.mComposerLabel.beginCommand( QString( "Label alignment changed" ) )
            self.mComposerLabel.setHAlign( Qt.AlignHCenter )
            self.mComposerLabel.update()
            self.mComposerLabel.endCommand()

    def on_mRightRadioButton_clicked(self):
        if ( self.mComposerLabel ):
            self.mComposerLabel.beginCommand( QString( "Label alignment changed" ) )
            self.mComposerLabel.setHAlign( Qt.AlignRight )
            self.mComposerLabel.update()
            self.mComposerLabel.endCommand()

    def on_mLeftRadioButton_clicked(self):
        if ( self.mComposerLabel ):
            self.mComposerLabel.beginCommand( QString( "Label alignment changed" ) )
            self.mComposerLabel.setHAlign( Qt.AlignLeft )
            self.mComposerLabel.update()
            self.mComposerLabel.endCommand()

    def on_mTopRadioButton_clicked(self):
        if ( self.mComposerLabel ):
            self.mComposerLabel.beginCommand( QString( "Label alignment changed" ) )
            self.mComposerLabel.setVAlign( Qt.AlignTop )
            self.mComposerLabel.update()
            self.mComposerLabel.endCommand()

    def on_mBottomRadioButton_clicked(self):
        if ( self.mComposerLabel ):
            self.mComposerLabel.beginCommand( QString( "Label alignment changed" ) )
            self.mComposerLabel.setVAlign( Qt.AlignBottom )
            self.mComposerLabel.update()
            self.mComposerLabel.endCommand()

    def on_mMiddleRadioButton_clicked(self):
        if ( self.mComposerLabel ):
            self.mComposerLabel.beginCommand( QString( "Label alignment changed" ) )
            self.mComposerLabel.setVAlign( Qt.AlignVCenter )
            self.mComposerLabel.update()
            self.mComposerLabel.endCommand()

    def setGuiElementValues(self):
        self.blockAllSignals( True )
        self.mTextEdit.setPlainText( self.mComposerLabel.text() )
        self.mTextEdit.moveCursor( QTextCursor.End, QTextCursor.MoveAnchor )
        self.mMarginXDoubleSpinBox.setValue( self.mComposerLabel.marginX() )
        self.mMarginYDoubleSpinBox.setValue( self.mComposerLabel.marginY() )
        self.mHtmlCheckBox.setChecked( self.mComposerLabel.htmlState() )
        self.mTopRadioButton.setChecked( self.mComposerLabel.vAlign() == Qt.AlignTop )
        self.mMiddleRadioButton.setChecked( self.mComposerLabel.vAlign() == Qt.AlignVCenter )
        self.mBottomRadioButton.setChecked( self.mComposerLabel.vAlign() == Qt.AlignBottom )
        self.mLeftRadioButton.setChecked( self.mComposerLabel.hAlign() == Qt.AlignLeft )
        self.mCenterRadioButton.setChecked( self.mComposerLabel.hAlign() == Qt.AlignHCenter )
        self.mRightRadioButton.setChecked( self.mComposerLabel.hAlign() == Qt.AlignRight )
        self.mFontColorButton.setColor( self.mComposerLabel.fontColor() )
        self.blockAllSignals( False )

    def blockAllSignals( self, block ):
        self.blockSignals( block )
        self.mHtmlCheckBox.blockSignals( block )
        self.mMarginXDoubleSpinBox.blockSignals( block )
        self.mMarginYDoubleSpinBox.blockSignals( block )
        self.mTopRadioButton.blockSignals( block )
        self.mMiddleRadioButton.blockSignals( block )
        self.mBottomRadioButton.blockSignals( block )
        self.mLeftRadioButton.blockSignals( block )
        self.mCenterRadioButton.blockSignals( block )
        self.mRightRadioButton.blockSignals( block )
        self.mFontColorButton.blockSignals( block )

    def atlasComposition(self):
        if ( not self.mComposerLabel ):
            return None
        composition = self.mComposerLabel.composition()

        if ( not composition ):
            return None

        return composition.atlasComposition()
    def atlasCoverageLayer(self):
        atlasMap = self.atlasComposition()

        if ( atlasMap and atlasMap.enabled() ):
            return atlasMap.coverageLayer()

        return None