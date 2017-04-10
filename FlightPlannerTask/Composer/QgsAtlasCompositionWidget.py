

from qgis.core import *
from qgis.gui import QgsGenericProjectionSelector, QgsMapLayerProxyModel, QgsExpressionBuilderDialog, QgsFieldComboBox, QgsMapLayerComboBox
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QToolButton
from PyQt4.QtCore import pyqtSlot, QThreadPool, Qt, SIGNAL, SLOT, QString, QRegExp, QSettings
from PyQt4.QtGui import QMessageBox, QFileDialog
from FlightPlanner.QgisHelper import QgisHelper
from Qgsatlascompositionwidgetbase import QgsAtlasCompositionWidgetBase
import define, os

# print "FORM_CLASS"
# # print os.path.join(os.path.dirname(__file__), 'grid_zone_generator_dialog_base.ui')
# FORM_CLASS, _ = uic.loadUiType(define.appPath + "/UI/Composer/qgsatlascompositionwidgetbase.ui")

class QgsAtlasCompositionWidget(QgsAtlasCompositionWidgetBase):
    def __init__(self, parent, c):
        """Constructor."""
        QgsAtlasCompositionWidgetBase.__init__(self, parent)
        # super(QgsAtlasCompositionWidget, self).__init__(parent)
        # self.setupUi(self)
        self.setWindowTitle("Print Dialog")

        self.mComposition = c
        
        self.mAtlasCoverageLayerComboBox.setFilters( QgsMapLayerProxyModel.VectorLayer );

        self.connect( self.mAtlasCoverageLayerComboBox, SIGNAL( "layerChanged( QgsMapLayer* )" ), self.mAtlasSortFeatureKeyComboBox, SLOT( "setLayer( QgsMapLayer* )" ) );
        self.connect(self.mAtlasCoverageLayerComboBox, SIGNAL( "layerChanged( QgsMapLayer* )" ), self.mPageNameWidget, SLOT( "setLayer( QgsMapLayer* )" ) );
        self.connect( self.mAtlasCoverageLayerComboBox, SIGNAL( "layerChanged( QgsMapLayer* )" ), self, SLOT( "changeCoverageLayer( QgsMapLayer* )" ) );
        self.connect( self.mAtlasSortFeatureKeyComboBox, SIGNAL( "fieldChanged( QString )" ), self, SLOT( "changesSortFeatureField( QString )" ) );
        self.connect( self.mPageNameWidget, SIGNAL( "fieldChanged( QString, bool )" ), self, SLOT( "pageNameExpressionChanged( QString, bool )" ) );
        self.mUseAtlasCheckBox.stateChanged.connect(self.on_mUseAtlasCheckBox_stateChanged)
        self.mAtlasFeatureFilterCheckBox.stateChanged.connect(self.on_mAtlasFeatureFilterCheckBox_stateChanged)
        self.mAtlasSingleFileCheckBox.stateChanged.connect(self.on_mAtlasSingleFileCheckBox_stateChanged)
        self.mAtlasHideCoverageCheckBox.stateChanged.connect(self.on_mAtlasHideCoverageCheckBox_stateChanged)
        self.mAtlasFilenamePatternEdit.editingFinished.connect(self.on_mAtlasFilenamePatternEdit_editingFinished)
        self.mAtlasFeatureFilterEdit.editingFinished.connect(self.on_mAtlasFeatureFilterEdit_editingFinished)
        self.mAtlasFilenameExpressionButton.clicked.connect(self.on_mAtlasFilenameExpressionButton_clicked)
        self.mAtlasFeatureFilterButton.clicked.connect(self.on_mAtlasFeatureFilterButton_clicked)

        # // Sort direction
        self.mAtlasSortFeatureDirectionButton.setEnabled( False );
        self.mAtlasSortFeatureKeyComboBox.setEnabled( False );
        
        # // connect to updates
        self.connect( self.mComposition.atlasComposition(), SIGNAL( "parameterChanged()" ), self, SLOT( "updateGuiElements()" ) );
        
        # self.mPageNameWidget.registerGetExpressionContextCallback( self._getExpressionContext, self.mComposition );
        
        self.updateGuiElements();

    def changeCoverageLayer(self, layer):
        atlasMap = self.mComposition.atlasComposition();
        if ( not atlasMap ):
            return;

        vl = layer;

        if ( not vl ):
            atlasMap.setCoverageLayer( None);
        else:
            atlasMap.setCoverageLayer( vl );
            self.updateAtlasFeatures();

    def changesSortFeatureField(self, fieldName):
        atlasMap = self.mComposition.atlasComposition();
        if ( not atlasMap ):
            return;
        atlasMap.setSortKeyAttributeName( fieldName );
        self.updateAtlasFeatures();
    def pageNameExpressionChanged(self, expression, valid):
        atlasMap = self.mComposition.atlasComposition();
        if ( not atlasMap or ( not valid and not expression.isEmpty() ) ):
            return;
        atlasMap.setPageNameExpression( expression );
    def updateGuiElements(self):
        self.blockAllSignals( True );
        atlasMap = self.mComposition.atlasComposition();
        
        self.mUseAtlasCheckBox.setCheckState( Qt.Checked if(atlasMap.enabled()) else Qt.Unchecked );
        self.mConfigurationGroup.setEnabled( atlasMap.enabled() );
        self.mOutputGroup.setEnabled( atlasMap.enabled() );
        
        self.mAtlasCoverageLayerComboBox.setLayer( atlasMap.coverageLayer() );
        self.mPageNameWidget.setLayer( atlasMap.coverageLayer() );
        self.mPageNameWidget.setField( atlasMap.pageNameExpression() );
        
        self.mAtlasSortFeatureKeyComboBox.setLayer( atlasMap.coverageLayer() );
        self.mAtlasSortFeatureKeyComboBox.setField( atlasMap.sortKeyAttributeName() );
        
        self.mAtlasFilenamePatternEdit.setText( atlasMap.filenamePattern() );
        self.mAtlasHideCoverageCheckBox.setCheckState( Qt.Checked if(atlasMap.hideCoverage()) else Qt.Unchecked );
        
        self.mAtlasSingleFileCheckBox.setCheckState( Qt.Checked if(atlasMap.singleFile()) else Qt.Unchecked );
        self.mAtlasFilenamePatternEdit.setEnabled( not atlasMap.singleFile() );
        self.mAtlasFilenameExpressionButton.setEnabled( not atlasMap.singleFile() );
        
        self.mAtlasSortFeatureCheckBox.setCheckState( Qt.Checked if(atlasMap.sortFeatures()) else Qt.Unchecked );
        self.mAtlasSortFeatureDirectionButton.setEnabled( atlasMap.sortFeatures() );
        self.mAtlasSortFeatureKeyComboBox.setEnabled( atlasMap.sortFeatures() );
        
        self.mAtlasSortFeatureDirectionButton.setArrowType( Qt.UpArrow if(atlasMap.sortAscending()) else Qt.DownArrow );
        self.mAtlasFeatureFilterEdit.setText( atlasMap.featureFilter() );
        
        self.mAtlasFeatureFilterCheckBox.setCheckState( Qt.Checked if(atlasMap.filterFeatures()) else Qt.Unchecked );
        self.mAtlasFeatureFilterEdit.setEnabled( atlasMap.filterFeatures() );
        self.mAtlasFeatureFilterButton.setEnabled( atlasMap.filterFeatures() );
        
        self.blockAllSignals( False );
    def blockAllSignals( self, b ):
        self.mUseAtlasCheckBox.blockSignals( b );
        self.mConfigurationGroup.blockSignals( b );
        self.mOutputGroup.blockSignals( b );
        self.mAtlasCoverageLayerComboBox.blockSignals( b );
        self.mPageNameWidget.blockSignals( b );
        self.mAtlasSortFeatureKeyComboBox.blockSignals( b );
        self.mAtlasFilenamePatternEdit.blockSignals( b );
        self.mAtlasHideCoverageCheckBox.blockSignals( b );
        self.mAtlasSingleFileCheckBox.blockSignals( b );
        self.mAtlasSortFeatureCheckBox.blockSignals( b );
        self.mAtlasSortFeatureDirectionButton.blockSignals( b );
        self.mAtlasFeatureFilterEdit.blockSignals( b );
        self.mAtlasFeatureFilterCheckBox.blockSignals( b );
    def _getExpressionContext(self, context):
        pass
        # const QgsComposition* composition = ( const QgsComposition* ) context;
        # if ( !composition )
        # {
        #     return QgsExpressionContext();
        # }
        #
        # QScopedPointer< QgsExpressionContext > expContext( composition->createExpressionContext() );
        # return QgsExpressionContext( *expContext );
    def on_mUseAtlasCheckBox_stateChanged( self, state ):
        atlasMap = self.mComposition.atlasComposition();
        if ( state == Qt.Checked ):
            atlasMap.setEnabled( True);
            self.mConfigurationGroup.setEnabled( True);
            self.mOutputGroup.setEnabled( True);
        else:
            atlasMap.setEnabled( False );
            self.mConfigurationGroup.setEnabled( False );
            self.mOutputGroup.setEnabled( False );

    def on_mAtlasFilenamePatternEdit_editingFinished(self):
        atlasMap = self.mComposition.atlasComposition();
        if ( not atlasMap ):
            return;

        if ( not atlasMap.setFilenamePattern( self.mAtlasFilenamePatternEdit.text() ) ):
        # //expression could not be set
            QMessageBox.warning(self
                                  , "Could not evaluate filename pattern"
                                  , QString("Could not set filename pattern as '%1'.\nParser error:\n%2")
                                  .arg( self.mAtlasFilenamePatternEdit.text(),
                                        atlasMap.filenamePatternErrorString() ));
    
    def on_mAtlasFilenameExpressionButton_clicked(self):
        atlasMap = self.mComposition.atlasComposition();
        if ( not atlasMap or not atlasMap.coverageLayer() ):
            return;
        
        # QScopedPointer<QgsExpressionContext> context( mComposition.createExpressionContext() );
        exprDlg = QgsExpressionBuilderDialog( atlasMap.coverageLayer(), self.mAtlasFilenamePatternEdit.text(), self, "generic" );
        exprDlg.setWindowTitle( "Expression based filename" );
        
        if ( exprDlg.exec_() == QtGui.QDialog.Accepted ):
            expression =  exprDlg.expressionText();
            if ( not expression.isEmpty() ):
              # //set atlas filename expression
                self.mAtlasFilenamePatternEdit.setText( expression );
                if ( not atlasMap.setFilenamePattern( expression ) ):
                # //expression could not be set
                    QMessageBox.warning( self
                                          , "Could not evaluate filename pattern"
                                          , QString("Could not set filename pattern as '%1'.\nParser error:\n%2")
                                          .arg( expression,
                                                atlasMap.filenamePatternErrorString() ));

    def on_mAtlasHideCoverageCheckBox_stateChanged( self, state ):
        atlasMap = self.mComposition.atlasComposition();
        if ( not atlasMap ):
            return;
        atlasMap.setHideCoverage( state == Qt.Checked );

    def on_mAtlasSingleFileCheckBox_stateChanged( self, state ):
        atlasMap = self.mComposition.atlasComposition();
        if ( not atlasMap ):
            return;
        if ( state == Qt.Checked ):
            self.mAtlasFilenamePatternEdit.setEnabled( False );
            self.mAtlasFilenameExpressionButton.setEnabled( False );
        else:
            self.mAtlasFilenamePatternEdit.setEnabled( True );
            self.mAtlasFilenameExpressionButton.setEnabled( True );
        atlasMap.setSingleFile( state == Qt.Checked );

    def on_mAtlasSortFeatureCheckBox_stateChanged( self, state ):
        atlasMap = self.mComposition.atlasComposition();
        if ( not atlasMap ):
            return;

        if ( state == Qt.Checked ):
            self.mAtlasSortFeatureDirectionButton.setEnabled( True );
            self.mAtlasSortFeatureKeyComboBox.setEnabled( True );
        else:
            self.mAtlasSortFeatureDirectionButton.setEnabled( False );
            self.mAtlasSortFeatureKeyComboBox.setEnabled( False );
        atlasMap.setSortFeatures( state == Qt.Checked );
        self.updateAtlasFeatures();

    def updateAtlasFeatures(self):
        # //only do this if composer mode is preview
        if ( not ( self.mComposition.atlasMode() == QgsComposition.PreviewAtlas ) ):
            return;

        # //update atlas features
        atlasMap = self.mComposition.atlasComposition();
        if ( not atlasMap ):
            return;

        updated = atlasMap.updateFeatures();
        if ( not updated ):
            QMessageBox.warning( self, "Atlas preview",
                                  "No matching atlas features found!" ,
                                  QMessageBox.Ok,
                                  QMessageBox.Ok );

        # //Perhaps atlas preview should be disabled now? If so, it may get annoying if user is editing
        # //the filter expression and it keeps disabling itself.
            return;

    def on_mAtlasFeatureFilterCheckBox_stateChanged( self, state ):
        atlasMap = self.mComposition.atlasComposition();
        if ( not atlasMap ):
            return;

        if ( state == Qt.Checked ):
            self.mAtlasFeatureFilterEdit.setEnabled( True );
            self.mAtlasFeatureFilterButton.setEnabled( True );
        else:
            self.mAtlasFeatureFilterEdit.setEnabled( False );
            self.mAtlasFeatureFilterButton.setEnabled( False );
        atlasMap.setFilterFeatures( state == Qt.Checked );
        self.updateAtlasFeatures();
    def on_mAtlasFeatureFilterEdit_editingFinished(self):
        atlasMap = self.mComposition.atlasComposition();
        if ( not atlasMap ):
            return;
        atlasMap.setFeatureFilter( self.mAtlasFeatureFilterEdit.text() );
        self.updateAtlasFeatures();
    
    def on_mAtlasFeatureFilterButton_clicked(self):
        atlasMap = self.mComposition.atlasComposition();
        vl = self.mAtlasCoverageLayerComboBox.currentLayer()
        
        if ( not atlasMap or not vl ):
            return;
        
        # QScopedPointer<QgsExpressionContext> context( mComposition.createExpressionContext() );
        exprDlg = QgsExpressionBuilderDialog( vl, self.mAtlasFeatureFilterEdit.text(), self, "generic");
        exprDlg.setWindowTitle( "Expression based filter" );
        
        if ( exprDlg.exec_() == QtGui.QDialog.Accepted ):
            expression =  exprDlg.expressionText();
            if ( not expression.isEmpty() ):
                self.mAtlasFeatureFilterEdit.setText( expression );
                atlasMap.setFeatureFilter( self.mAtlasFeatureFilterEdit.text() );
                self.updateAtlasFeatures();
    
    def on_mAtlasSortFeatureDirectionButton_clicked(self):
        at = self.mAtlasSortFeatureDirectionButton.arrowType();
        at = Qt.DownArrow if( at == Qt.UpArrow ) else Qt.UpArrow;
        self.mAtlasSortFeatureDirectionButton.setArrowType( at );
        
        atlasMap = self.mComposition.atlasComposition();
        if ( not atlasMap ):
            return;
        
        atlasMap.setSortAscending( at == Qt.UpArrow );
        self.updateAtlasFeatures();
        
