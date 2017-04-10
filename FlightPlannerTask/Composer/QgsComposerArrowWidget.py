
from PyQt4.QtGui import QWidget, QMenu, QDoubleValidator, QColorDialog,\
    QDialog, QFontDialog, QIcon, QPixmap, QAction, QComboBox, QListWidgetItem, QFileDialog, QButtonGroup
from PyQt4 import uic
from PyQt4.QtCore import SIGNAL, SLOT, QString, Qt, QStringList, QSettings, QFileInfo, QDir
from Composer.QgsComposerItemWidget import QgsComposerItemWidget

from qgis.core import QgsComposition, QgsComposerMap, QgsComposerMergeCommand, QGis, QgsRectangle, QgsStyleV2,\
    QgsSymbolLayerV2Utils, QgsComposerMapGrid, QgsExpressionContext, QgsComposerObject, QgsProject, QgsCoordinateReferenceSystem,\
    QgsComposerMapOverview, QgsComposerArrow
from qgis.gui import QgsSymbolV2SelectorDialog, QgsDataDefinedButton, QgsGenericProjectionSelector, QgsExpressionBuilderDialog
import define, time
from Type.switch import switch

from Composer.ui_qgscomposerarrowwidget import Ui_QgsComposerArrowWidgetBase
from Composer.ui_qgscomposeritemwidget import Ui_QgsComposerItemWidgetBase
# FORM_CLASS, _ = uic.loadUiType(define.appPath + "/UI/Composer/qgsComposerMapWidgetBase.ui")

class QgsComposerArrowWidget(Ui_QgsComposerArrowWidgetBase):
    def __init__(self, parent, arrow):
        Ui_QgsComposerArrowWidgetBase.__init__(self, parent)

        self.mArrow = arrow
        self.mRadioButtonGroup = QButtonGroup( self );
        self.mRadioButtonGroup.addButton( self.mDefaultMarkerRadioButton );
        self.mRadioButtonGroup.addButton( self.mNoMarkerRadioButton );
        self.mRadioButtonGroup.addButton( self.mSvgMarkerRadioButton );
        self.mRadioButtonGroup.setExclusive( True );
        
        # //disable the svg related gui elements by default
        self.on_mSvgMarkerRadioButton_toggled( False );
        
        # //add widget for general composer item properties
        itemPropertiesWidget = QgsComposerItemWidget( self, self.mArrow );
        self.mainLayout.addWidget( itemPropertiesWidget );
        
        self.mArrowHeadOutlineColorButton.setColorDialogTitle( QString( "Select arrow head outline color" ) );
        self.mArrowHeadOutlineColorButton.setAllowAlpha( True );
        self.mArrowHeadOutlineColorButton.setContext( "composer" );
        self.mArrowHeadOutlineColorButton.setNoColorString( QString( "Transparent outline" ) );
        self.mArrowHeadOutlineColorButton.setShowNoColor( True );
        self.mArrowHeadFillColorButton.setColorDialogTitle( QString( "Select arrow head fill color" ) );
        self.mArrowHeadFillColorButton.setAllowAlpha( True );
        self.mArrowHeadFillColorButton.setContext( "composer" );
        self.mArrowHeadFillColorButton.setNoColorString( QString( "Transparent fill" ) );
        self.mArrowHeadFillColorButton.setShowNoColor( True );
        
        self.setGuiElementValues();
        
        if ( arrow ):
            self.connect( arrow, SIGNAL( "itemChanged()" ), self.setGuiElementValues)
        self.connect(self.mArrowHeadWidthSpinBox, SIGNAL("valueChanged(double)"), self.on_mArrowHeadWidthSpinBox_valueChanged)
            
        self.timeEnd = 0
        self.timeStart = 0
    def on_mOutlineWidthSpinBox_valueChanged( self, d ):
        if ( not self.mArrow ):
            return;

        self.mArrow.beginCommand( QString( "Arrow head outline width" ), QgsComposerMergeCommand.ArrowOutlineWidth );
        self.mArrow.setArrowHeadOutlineWidth( self.mOutlineWidthSpinBox.value() );
        self.mArrow.update();
        self.mArrow.endCommand();

    def on_mArrowHeadWidthSpinBox_valueChanged( self, d ):
        if ( not self.mArrow ):
            return;

        self.mArrow.beginCommand( QString( "Arrowhead width" ), QgsComposerMergeCommand.ArrowHeadWidth );
        self.mArrow.setArrowHeadWidth( self.mArrowHeadWidthSpinBox.value() );
        self.mArrow.update();
        self.mArrow.endCommand();

    def on_mArrowHeadFillColorButton_colorChanged( self, newColor ):
        if ( not self.mArrow ):
            return;

        self.mArrow.beginCommand( QString( "Arrow head fill color" ) );
        self.mArrow.setArrowHeadFillColor( newColor );
        self.mArrow.update();
        self.mArrow.endCommand();

    def on_mArrowHeadOutlineColorButton_colorChanged( self, newColor ):
        if ( not self.mArrow ):
            return;

        self.mArrow.beginCommand( QString( "Arrow head outline color" ) );
        self.mArrow.setArrowHeadOutlineColor( newColor );
        self.mArrow.update();
        self.mArrow.endCommand();

    def blockAllSignals( self, block ):
        self.mLineStyleButton.blockSignals( block );
        self.mArrowHeadFillColorButton.blockSignals( block );
        self.mArrowHeadOutlineColorButton.blockSignals( block );
        self.mOutlineWidthSpinBox.blockSignals( block );
        self.mArrowHeadWidthSpinBox.blockSignals( block );
        self.mDefaultMarkerRadioButton.blockSignals( block );
        self.mNoMarkerRadioButton.blockSignals( block );
        self.mSvgMarkerRadioButton.blockSignals( block );
        self.mStartMarkerLineEdit.blockSignals( block );
        self.mStartMarkerToolButton.blockSignals( block );
        self.mEndMarkerLineEdit.blockSignals( block );
        self.mEndMarkerToolButton.blockSignals( block );

    def setGuiElementValues(self):
        if ( not self.mArrow ):
            return;

        self.blockAllSignals( True );
        self.mArrowHeadFillColorButton.setColor( self.mArrow.arrowHeadFillColor() );
        self.mArrowHeadOutlineColorButton.setColor( self.mArrow.arrowHeadOutlineColor() );
        self.mOutlineWidthSpinBox.setValue( self.mArrow.arrowHeadOutlineWidth() );
        self.mArrowHeadWidthSpinBox.setValue( self.mArrow.arrowHeadWidth() );

        mode = self.mArrow.markerMode();
        if ( mode == QgsComposerArrow.DefaultMarker ):
            self.mDefaultMarkerRadioButton.setChecked( True );
        elif ( mode == QgsComposerArrow.NoMarker ):
            self.mNoMarkerRadioButton.setChecked( True )
        else:# //svg marker:
            self.mSvgMarkerRadioButton.setChecked( True );
            self.enableSvgInputElements( True );
        self.mStartMarkerLineEdit.setText( self.mArrow.startMarker() );
        self.mEndMarkerLineEdit.setText( self.mArrow.endMarker() );

        self.updateLineSymbolMarker();

        self.blockAllSignals( False );

    def enableSvgInputElements( self,  enable ):
        self.mStartMarkerLineEdit.setEnabled( enable );
        self.mStartMarkerToolButton.setEnabled( enable );
        self.mEndMarkerLineEdit.setEnabled( enable );
        self.mEndMarkerToolButton.setEnabled( enable );

    def on_mDefaultMarkerRadioButton_toggled( self, toggled ):
        if ( self.mArrow and toggled ):
            self.mArrow.beginCommand( QString( "Arrow marker changed" ) );
            self.mArrow.setMarkerMode( QgsComposerArrow.DefaultMarker );
            self.mArrow.update();
            self.mArrow.endCommand();

    def on_mNoMarkerRadioButton_toggled( self, toggled ):
        if ( self.mArrow and toggled ):
            self.mArrow.beginCommand( QString( "Arrow marker changed" ) );
            self.mArrow.setMarkerMode( QgsComposerArrow.NoMarker );
            self.mArrow.update();
            self.mArrow.endCommand();

    def on_mSvgMarkerRadioButton_toggled( self, toggled ):
        self.enableSvgInputElements( toggled );
        if ( self.mArrow and toggled ):
            self.mArrow.beginCommand( QString( "Arrow marker changed" ) );
            self.mArrow.setMarkerMode( QgsComposerArrow.SVGMarker );
            self.mArrow.update();
            self.mArrow.endCommand();

    def on_mStartMarkerLineEdit_textChanged( self, text ):
        if ( self.mArrow ):
            self.mArrow.beginCommand( QString( "Arrow start marker" ) );
            fi = QFileInfo( text );
            if ( fi.exists() and fi.isFile() ):
                self.mArrow.setStartMarker( text );
            else:
                self.mArrow.setStartMarker( "" );
            self.mArrow.update();
            self.mArrow.endCommand();

    def on_mEndMarkerLineEdit_textChanged( self, text ):
        if ( self.mArrow ):
            self.mArrow.beginCommand( QString( "Arrow end marker" ) );
            fi = QFileInfo( text );
            if ( fi.exists() and fi.isFile() ):
                self.mArrow.setEndMarker( text );
            else:
                self.mArrow.setEndMarker( "" );
            self.mArrow.update();
            self.mArrow.endCommand();

    def on_mStartMarkerToolButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        s = QSettings();
        openDir = QString()
        if ( not self.mStartMarkerLineEdit.text().isEmpty() ):
            fi = QFileInfo( self.mStartMarkerLineEdit.text() );
            openDir = fi.dir().absolutePath();

        if ( openDir.isEmpty() ):
            openDir = s.value( "/UI/lastComposerMarkerDir", QDir.homePath() ).toString();

        svgFileName = QFileDialog.getOpenFileName( self, QString( "Start marker svg file" ), openDir );
        if ( not svgFileName.isNull() ):
            fileInfo = QFileInfo( svgFileName );
            s.setValue( "/UI/lastComposerMarkerDir", fileInfo.absolutePath() );
            self.mArrow.beginCommand( QString( "Arrow start marker" ) );
            self.mStartMarkerLineEdit.setText( svgFileName );
            self.mArrow.endCommand();
        self.timeStart = time.time()

    def on_mEndMarkerToolButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        s = QSettings();
        openDir = QString();

        if ( not self.mEndMarkerLineEdit.text().isEmpty() ):
            fi = QFileInfo( self.mEndMarkerLineEdit.text() );
            openDir = fi.dir().absolutePath();

        if ( openDir.isEmpty() ):
            openDir = s.value( "/UI/lastComposerMarkerDir", QDir.homePath() ).toString();

        svgFileName = QFileDialog.getOpenFileName( self, QString( "End marker svg file" ), openDir );
        if ( not svgFileName.isNull() ):
            fileInfo = QFileInfo( svgFileName );
            s.setValue( "/UI/lastComposerMarkerDir", fileInfo.absolutePath() );
            self.mArrow.beginCommand( QString( "Arrow end marker" ) );
            self.mEndMarkerLineEdit.setText( svgFileName );
            self.mArrow.endCommand();
        self.timeStart = time.time()

    def on_mLineStyleButton_clicked(self):
        if self.timeStart != 0:
            self.timeEnd = time.time()
            print self.timeEnd
            if self.timeEnd - self.timeStart <= 2:
                self.timeStart = 0
                return
        if ( not self.mArrow ):
            return;

        newSymbol = self.mArrow.lineSymbol().clone();
        d = QgsSymbolV2SelectorDialog( newSymbol, QgsStyleV2.defaultStyle(), None, self);
        d.setExpressionContext( self.mArrow.createExpressionContext() );

        if ( d.exec_() == QDialog.Accepted ):

            self.mArrow.beginCommand( QString( "Arrow line style changed" ) );
            self.mArrow.setLineSymbol( newSymbol );
            self.updateLineSymbolMarker();
            self.mArrow.endCommand();
            self.mArrow.update();
        else:
            pass
            # delete newSymbol;
        self.timeStart = time.time()

    def updateLineSymbolMarker(self):
        if ( not self.mArrow ):
            return;

        icon = QgsSymbolLayerV2Utils.symbolPreviewIcon( self.mArrow.lineSymbol(), self.mLineStyleButton.iconSize() );
        self.mLineStyleButton.setIcon( icon );