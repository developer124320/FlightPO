
from PyQt4.QtGui import QWidget, QMenu, QDoubleValidator, QColorDialog,\
    QDialog, QFontDialog, QIcon, QPixmap, QAction, QComboBox, QListWidgetItem, QTextCursor
from PyQt4 import uic
from PyQt4.QtCore import SIGNAL, SLOT, QString, Qt, QStringList, QSettings
from Composer.QgsComposerItemWidget import QgsComposerItemWidget

from qgis.core import QgsComposition, QgsComposerMap, QgsComposerMergeCommand, QGis, QgsRectangle, QgsStyleV2,\
    QgsSymbolLayerV2Utils, QgsComposerMapGrid, QgsExpressionContext, QgsComposerObject, QgsProject, QgsCoordinateReferenceSystem,\
    QgsComposerMapOverview
from qgis.gui import QgsSymbolV2SelectorDialog, QgsDataDefinedButton, QgsGenericProjectionSelector, QgsExpressionBuilderDialog
import define
from Type.switch import switch

from Composer.ui_qgscomposerlegendwidget import Ui_QgsComposerLegendWidgetBase
from Composer.ui_qgscomposeritemwidget import Ui_QgsComposerItemWidgetBase
# FORM_CLASS, _ = uic.loadUiType(define.appPath + "/UI/Composer/qgsComposerMapWidgetBase.ui")

class QgsComposerLegendWidget(Ui_QgsComposerLegendWidgetBase):
    def __init__(self, parent, legend):
        Ui_QgsComposerLegendWidgetBase.__init__(self, parent)
        self.mLegend = legend

        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/images/themes/default/symbologyAdd.svg"), QIcon.Normal, QIcon.Off)
        self.mAddToolButton.setIcon( icon)

        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/images/themes/default/symbologyEdit.png"), QIcon.Normal, QIcon.Off)
        self.mEditPushButton.setIcon( icon )

        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/images/themes/default/symbologyRemove.svg"), QIcon.Normal, QIcon.Off)
        self.mRemoveToolButton.setIcon( icon )
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/images/themes/default/symbologyUp.svg"), QIcon.Normal, QIcon.Off)
        self.mMoveUpToolButton.setIcon( icon )
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/images/themes/default/symbologyDown.svg"), QIcon.Normal, QIcon.Off)
        self.mMoveDownToolButton.setIcon( icon )
        icon = QIcon()
        icon.addPixmap(QPixmap("Resource/images/themes/default/mActionSum.png"), QIcon.Normal, QIcon.Off)
        self.mCountToolButton.setIcon( icon )
        
        self.mFontColorButton.setColorDialogTitle( QString( "Select font color" ) )
        self.mFontColorButton.setContext( "composer" )
        
        self.mRasterBorderColorButton.setColorDialogTitle( QString( "Select border color" ) )
        self.mRasterBorderColorButton.setAllowAlpha( True )
        self.mRasterBorderColorButton.setContext( "composer " )
        
        #add widget for item properties
        itemPropertiesWidget = QgsComposerItemWidget( self, legend )
        self.mainLayout.addWidget( itemPropertiesWidget )
        
        self.mItemTreeView.setHeaderHidden( True )
        
        if ( legend ):
            self.mItemTreeView.setModel( legend.modelV2() )
            self.mItemTreeView.setMenuProvider( QgsComposerLegendMenuProvider( self.mItemTreeView, self ) )
            self.connect( legend, SIGNAL( "itemChanged()" ), self.setGuiElements)
            self.mWrapCharLineEdit.setText( legend.wrapChar() )

            # connect atlas state to the filter legend by atlas checkbox
            self.connect( legend.composition().atlasComposition(), SIGNAL( "toggled( bool )" ), self.updateFilterLegendByAtlasButton)
            self.connect( legend.composition().atlasComposition(), SIGNAL( "coverageLayerChanged( QgsVectorLayer* )" ), self.updateFilterLegendByAtlasButton)
        
        self.setGuiElements()
        
        self.connect( self.mItemTreeView.selectionModel(), SIGNAL( "currentChanged( const QModelIndex &, const QModelIndex & )" ),
               self.selectedChanged)


#     def setGuiElements(self):
#         if ( !mLegend )
#         {
#         return
#         }
#
#         int alignment = mLegend.titleAlignment() == Qt.AlignLeft ? 0 : mLegend.titleAlignment() == Qt.AlignHCenter ? 1 : 2
#
#         blockAllSignals( True )
#         mTitleLineEdit.setText( mLegend.title() )
#         mTitleAlignCombo.setCurrentIndex( alignment )
#         mFilterByMapToolButton.setChecked( mLegend.legendFilterByMapEnabled() )
#         mColumnCountSpinBox.setValue( mLegend.columnCount() )
#         mSplitLayerCheckBox.setChecked( mLegend.splitLayer() )
#         mEqualColumnWidthCheckBox.setChecked( mLegend.equalColumnWidth() )
#         mSymbolWidthSpinBox.setValue( mLegend.symbolWidth() )
#         mSymbolHeightSpinBox.setValue( mLegend.symbolHeight() )
#         mWmsLegendWidthSpinBox.setValue( mLegend.wmsLegendWidth() )
#         mWmsLegendHeightSpinBox.setValue( mLegend.wmsLegendHeight() )
#         mTitleSpaceBottomSpinBox.setValue( mLegend.style( QgsComposerLegendStyle.Title ).margin( QgsComposerLegendStyle.Bottom ) )
#         mGroupSpaceSpinBox.setValue( mLegend.style( QgsComposerLegendStyle.Group ).margin( QgsComposerLegendStyle.Top ) )
#         mLayerSpaceSpinBox.setValue( mLegend.style( QgsComposerLegendStyle.Subgroup ).margin( QgsComposerLegendStyle.Top ) )
#         # We keep Symbol and SymbolLabel Top in sync for now
#         mSymbolSpaceSpinBox.setValue( mLegend.style( QgsComposerLegendStyle.Symbol ).margin( QgsComposerLegendStyle.Top ) )
#         mIconLabelSpaceSpinBox.setValue( mLegend.style( QgsComposerLegendStyle.SymbolLabel ).margin( QgsComposerLegendStyle.Left ) )
#         mBoxSpaceSpinBox.setValue( mLegend.boxSpace() )
#         mColumnSpaceSpinBox.setValue( mLegend.columnSpace() )
#
#         mRasterBorderGroupBox.setChecked( mLegend.drawRasterBorder() )
#         mRasterBorderWidthSpinBox.setValue( mLegend.rasterBorderWidth() )
#         mRasterBorderColorButton.setColor( mLegend.rasterBorderColor() )
#
#         mCheckBoxAutoUpdate.setChecked( mLegend.autoUpdateModel() )
#         refreshMapComboBox()
#
#         mCheckboxResizeContents.setChecked( mLegend.resizeToContents() )
#
#         const QgsComposerMap* map = mLegend.composerMap()
#         if ( map )
#         {
#         mMapComboBox.setCurrentIndex( mMapComboBox.findData( map.id() ) )
#         }
#         else
#         {
#         mMapComboBox.setCurrentIndex( mMapComboBox.findData( -1 ) )
#         }
#         mFontColorButton.setColor( mLegend.fontColor() )
#         blockAllSignals( False )
#
#         on_mCheckBoxAutoUpdate_stateChanged( mLegend.autoUpdateModel() ? Qt.Checked : Qt.Unchecked )
#     }
#
# def on_mWrapCharLineEdit_textChanged( const QString &text )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Item wrapping changed" ) )
#     mLegend.setWrapChar( text )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mTitleLineEdit_textChanged( const QString& text )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend title changed" ), QgsComposerMergeCommand.ComposerLegendText )
#     mLegend.setTitle( text )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mTitleAlignCombo_currentIndexChanged( int index )
# {
#   if ( mLegend )
#   {
#     Qt.AlignmentFlag alignment = index == 0 ? Qt.AlignLeft : index == 1 ? Qt.AlignHCenter : Qt.AlignRight
#     mLegend.beginCommand( QString( "Legend title alignment changed" ) )
#     mLegend.setTitleAlignment( alignment )
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mColumnCountSpinBox_valueChanged( int c )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend column count" ), QgsComposerMergeCommand.LegendColumnCount )
#     mLegend.setColumnCount( c )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
#   mSplitLayerCheckBox.setEnabled( c > 1 )
#   mEqualColumnWidthCheckBox.setEnabled( c > 1 )
# }
#
# def on_mSplitLayerCheckBox_toggled( bool checked )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend split layers" ), QgsComposerMergeCommand.LegendSplitLayer )
#     mLegend.setSplitLayer( checked )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mEqualColumnWidthCheckBox_toggled( bool checked )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend equal column width" ), QgsComposerMergeCommand.LegendEqualColumnWidth )
#     mLegend.setEqualColumnWidth( checked )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mSymbolWidthSpinBox_valueChanged( double d )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend symbol width" ), QgsComposerMergeCommand.LegendSymbolWidth )
#     mLegend.setSymbolWidth( d )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mSymbolHeightSpinBox_valueChanged( double d )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend symbol height" ), QgsComposerMergeCommand.LegendSymbolHeight )
#     mLegend.setSymbolHeight( d )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mWmsLegendWidthSpinBox_valueChanged( double d )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Wms Legend width" ), QgsComposerMergeCommand.LegendWmsLegendWidth )
#     mLegend.setWmsLegendWidth( d )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mWmsLegendHeightSpinBox_valueChanged( double d )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Wms Legend height" ), QgsComposerMergeCommand.LegendWmsLegendHeight )
#     mLegend.setWmsLegendHeight( d )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mTitleSpaceBottomSpinBox_valueChanged( double d )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend title space bottom" ), QgsComposerMergeCommand.LegendTitleSpaceBottom )
#     mLegend.rstyle( QgsComposerLegendStyle.Title ).setMargin( QgsComposerLegendStyle.Bottom, d )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mGroupSpaceSpinBox_valueChanged( double d )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend group space" ), QgsComposerMergeCommand.LegendGroupSpace )
#     mLegend.rstyle( QgsComposerLegendStyle.Group ).setMargin( QgsComposerLegendStyle.Top, d )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mLayerSpaceSpinBox_valueChanged( double d )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend layer space" ), QgsComposerMergeCommand.LegendLayerSpace )
#     mLegend.rstyle( QgsComposerLegendStyle.Subgroup ).setMargin( QgsComposerLegendStyle.Top, d )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mSymbolSpaceSpinBox_valueChanged( double d )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend symbol space" ), QgsComposerMergeCommand.LegendSymbolSpace )
#     # We keep Symbol and SymbolLabel Top in sync for now
#     mLegend.rstyle( QgsComposerLegendStyle.Symbol ).setMargin( QgsComposerLegendStyle.Top, d )
#     mLegend.rstyle( QgsComposerLegendStyle.SymbolLabel ).setMargin( QgsComposerLegendStyle.Top, d )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mIconLabelSpaceSpinBox_valueChanged( double d )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend icon label space" ), QgsComposerMergeCommand.LegendIconSymbolSpace )
#     mLegend.rstyle( QgsComposerLegendStyle.SymbolLabel ).setMargin( QgsComposerLegendStyle.Left, d )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mTitleFontButton_clicked()
# {
#   if ( mLegend )
#   {
#     bool ok
#     QFont newFont = QgisGui.getFont( ok, mLegend.style( QgsComposerLegendStyle.Title ).font() )
#     if ( ok )
#     {
#       mLegend.beginCommand( QString( "Title font changed" ) )
#       mLegend.setStyleFont( QgsComposerLegendStyle.Title, newFont )
#       mLegend.adjustBoxSize()
#       mLegend.update()
#       mLegend.endCommand()
#     }
#   }
# }
#
# def on_mGroupFontButton_clicked()
# {
#   if ( mLegend )
#   {
#     bool ok
#     QFont newFont = QgisGui.getFont( ok, mLegend.style( QgsComposerLegendStyle.Group ).font() )
#     if ( ok )
#     {
#       mLegend.beginCommand( QString( "Legend group font changed" ) )
#       mLegend.setStyleFont( QgsComposerLegendStyle.Group, newFont )
#       mLegend.adjustBoxSize()
#       mLegend.update()
#       mLegend.endCommand()
#     }
#   }
# }
#
# def on_mLayerFontButton_clicked()
# {
#   if ( mLegend )
#   {
#     bool ok
#     QFont newFont = QgisGui.getFont( ok, mLegend.style( QgsComposerLegendStyle.Subgroup ).font() )
#     if ( ok )
#     {
#       mLegend.beginCommand( QString( "Legend layer font changed" ) )
#       mLegend.setStyleFont( QgsComposerLegendStyle.Subgroup, newFont )
#       mLegend.adjustBoxSize()
#       mLegend.update()
#       mLegend.endCommand()
#     }
#   }
# }
#
# def on_mItemFontButton_clicked()
# {
#   if ( mLegend )
#   {
#     bool ok
#     QFont newFont = QgisGui.getFont( ok, mLegend.style( QgsComposerLegendStyle.SymbolLabel ).font() )
#     if ( ok )
#     {
#       mLegend.beginCommand( QString( "Legend item font changed" ) )
#       mLegend.setStyleFont( QgsComposerLegendStyle.SymbolLabel, newFont )
#       mLegend.adjustBoxSize()
#       mLegend.update()
#       mLegend.endCommand()
#     }
#   }
# }
#
# def on_mFontColorButton_colorChanged( const QColor& newFontColor )
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   mLegend.beginCommand( QString( "Legend font color changed" ) )
#   mLegend.setFontColor( newFontColor )
#   mLegend.update()
#   mLegend.endCommand()
# }
#
# def on_mBoxSpaceSpinBox_valueChanged( double d )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend box space" ), QgsComposerMergeCommand.LegendBoxSpace )
#     mLegend.setBoxSpace( d )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
# def on_mColumnSpaceSpinBox_valueChanged( double d )
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend box space" ), QgsComposerMergeCommand.LegendColumnSpace )
#     mLegend.setColumnSpace( d )
#     mLegend.adjustBoxSize()
#     mLegend.update()
#     mLegend.endCommand()
#   }
# }
#
#
# static void _moveLegendNode( QgsLayerTreeLayer* nodeLayer, int legendNodeIndex, int offset )
# {
#   QList<int> order = QgsMapLayerLegendUtils.legendNodeOrder( nodeLayer )
#
#   if ( legendNodeIndex < 0 || legendNodeIndex >= order.count() )
#     return
#   if ( legendNodeIndex + offset < 0 || legendNodeIndex + offset >= order.count() )
#     return
#
#   int id = order.takeAt( legendNodeIndex )
#   order.insert( legendNodeIndex + offset, id )
#
#   QgsMapLayerLegendUtils.setLegendNodeOrder( nodeLayer, order )
# }
#
#
# def on_mMoveDownToolButton_clicked()
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   QModelIndex index = mItemTreeView.selectionModel().currentIndex()
#   QModelIndex parentIndex = index.parent()
#   if ( !index.isValid() || index.row() == mItemTreeView.model().rowCount( parentIndex ) - 1 )
#     return
#
#   QgsLayerTreeNode* node = mItemTreeView.layerTreeModel().index2node( index )
#   QgsLayerTreeModelLegendNode* legendNode = mItemTreeView.layerTreeModel().index2legendNode( index )
#   if ( !node && !legendNode )
#     return
#
#   mLegend.beginCommand( "Moved legend item down" )
#
#   if ( node )
#   {
#     QgsLayerTreeGroup* parentGroup = QgsLayerTree.toGroup( node.parent() )
#     parentGroup.insertChildNode( index.row() + 2, node.clone() )
#     parentGroup.removeChildNode( node )
#   }
#   else # legend node
#   {
#     _moveLegendNode( legendNode.layerNode(), index.row(), 1 )
#     mItemTreeView.layerTreeModel().refreshLayerLegend( legendNode.layerNode() )
#   }
#
#   mItemTreeView.setCurrentIndex( mItemTreeView.layerTreeModel().index( index.row() + 1, 0, parentIndex ) )
#
#   mLegend.update()
#   mLegend.endCommand()
# }
#
# def on_mMoveUpToolButton_clicked()
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   QModelIndex index = mItemTreeView.selectionModel().currentIndex()
#   QModelIndex parentIndex = index.parent()
#   if ( !index.isValid() || index.row() == 0 )
#     return
#
#   QgsLayerTreeNode* node = mItemTreeView.layerTreeModel().index2node( index )
#   QgsLayerTreeModelLegendNode* legendNode = mItemTreeView.layerTreeModel().index2legendNode( index )
#   if ( !node && !legendNode )
#     return
#
#   mLegend.beginCommand( "Moved legend item up" )
#
#   if ( node )
#   {
#     QgsLayerTreeGroup* parentGroup = QgsLayerTree.toGroup( node.parent() )
#     parentGroup.insertChildNode( index.row() - 1, node.clone() )
#     parentGroup.removeChildNode( node )
#   }
#   else # legend node
#   {
#     _moveLegendNode( legendNode.layerNode(), index.row(), -1 )
#     mItemTreeView.layerTreeModel().refreshLayerLegend( legendNode.layerNode() )
#   }
#
#   mItemTreeView.setCurrentIndex( mItemTreeView.layerTreeModel().index( index.row() - 1, 0, parentIndex ) )
#
#   mLegend.update()
#   mLegend.endCommand()
# }
#
# def on_mCheckBoxAutoUpdate_stateChanged( int state )
# {
#   mLegend.beginCommand( "Auto update changed" )
#
#   mLegend.setAutoUpdateModel( state == Qt.Checked )
#
#   mLegend.updateItem()
#   mLegend.endCommand()
#
#   # do not allow editing of model if auto update is on - we would modify project's layer tree
#   QList<QWidget*> widgets
#   widgets << mMoveDownToolButton << mMoveUpToolButton << mRemoveToolButton << mAddToolButton
#   << mEditPushButton << mCountToolButton << mUpdateAllPushButton << mAddGroupToolButton
#   << mExpressionFilterButton
#   Q_FOREACH ( QWidget* w, widgets )
#     w.setEnabled( state != Qt.Checked )
#
#   if ( state == Qt.Unchecked )
#   {
#     # update widgets state based on current selection
#     selectedChanged( QModelIndex(), QModelIndex() )
#   }
# }
#
# def on_mMapComboBox_currentIndexChanged( int index )
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   QVariant itemData = mMapComboBox.itemData( index )
#   if ( itemData.type() == QVariant.Invalid )
#   {
#     return
#   }
#
#   const QgsComposition* comp = mLegend.composition()
#   if ( !comp )
#   {
#     return
#   }
#
#   int mapNr = itemData.toInt()
#   if ( mapNr < 0 )
#   {
#     mLegend.setComposerMap( nullptr )
#   }
#   else
#   {
#     const QgsComposerMap* map = comp.getComposerMapById( mapNr )
#     if ( map )
#     {
#       mLegend.beginCommand( QString( "Legend map changed" ) )
#       mLegend.setComposerMap( map )
#       mLegend.updateItem()
#       mLegend.endCommand()
#     }
#   }
# }
#
# def on_mCheckboxResizeContents_toggled( bool checked )
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   mLegend.beginCommand( QString( "Legend resize to contents" ) )
#   mLegend.setResizeToContents( checked )
#   if ( checked )
#     mLegend.adjustBoxSize()
#   mLegend.updateItem()
#   mLegend.endCommand()
# }
#
# def on_mRasterBorderGroupBox_toggled( bool state )
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   mLegend.beginCommand( QString( "Legend raster borders" ) )
#   mLegend.setDrawRasterBorder( state )
#   mLegend.adjustBoxSize()
#   mLegend.update()
#   mLegend.endCommand()
# }
#
# def on_mRasterBorderWidthSpinBox_valueChanged( double d )
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   mLegend.beginCommand( QString( "Legend raster border width" ), QgsComposerMergeCommand.LegendRasterBorderWidth )
#   mLegend.setRasterBorderWidth( d )
#   mLegend.adjustBoxSize()
#   mLegend.update()
#   mLegend.endCommand()
# }
#
# def on_mRasterBorderColorButton_colorChanged( const QColor& newColor )
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   mLegend.beginCommand( QString( "Legend raster border color" ) )
#   mLegend.setRasterBorderColor( newColor )
#   mLegend.update()
#   mLegend.endCommand()
# }
#
# def on_mAddToolButton_clicked()
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   QgisApp* app = QgisApp.instance()
#   if ( !app )
#   {
#     return
#   }
#
#   QgsMapCanvas* canvas = app.mapCanvas()
#   if ( canvas )
#   {
#     QList<QgsMapLayer*> layers = canvas.layers()
#
#     QgsComposerLegendLayersDialog addDialog( layers, self )
#     if ( addDialog.exec() == QDialog.Accepted )
#     {
#       QgsMapLayer* layer = addDialog.selectedLayer()
#       if ( layer )
#       {
#         mLegend.beginCommand( "Legend item added" )
#         mLegend.modelV2().rootGroup().addLayer( layer )
#         mLegend.endCommand()
#       }
#     }
#   }
# }
#
# def on_mRemoveToolButton_clicked()
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   QItemSelectionModel* selectionModel = mItemTreeView.selectionModel()
#   if ( !selectionModel )
#   {
#     return
#   }
#
#   mLegend.beginCommand( "Legend item removed" )
#
#   QList<QPersistentModelIndex> indexes
#   Q_FOREACH ( const QModelIndex &index, selectionModel.selectedIndexes() )
#     indexes << index
#
#   # first try to remove legend nodes
#   QHash<QgsLayerTreeLayer*, QList<int> > nodesWithRemoval
#   Q_FOREACH ( const QPersistentModelIndex& index, indexes )
#   {
#     if ( QgsLayerTreeModelLegendNode* legendNode = mItemTreeView.layerTreeModel().index2legendNode( index ) )
#     {
#       QgsLayerTreeLayer* nodeLayer = legendNode.layerNode()
#       nodesWithRemoval[nodeLayer].append( index.row() )
#     }
#   }
#   Q_FOREACH ( QgsLayerTreeLayer* nodeLayer, nodesWithRemoval.keys() )
#   {
#     QList<int> toDelete = nodesWithRemoval[nodeLayer]
#     qSort( toDelete.begin(), toDelete.end(), qGreater<int>() )
#     QList<int> order = QgsMapLayerLegendUtils.legendNodeOrder( nodeLayer )
#
#     Q_FOREACH ( int i, toDelete )
#     {
#       if ( i >= 0 && i < order.count() )
#         order.removeAt( i )
#     }
#
#     QgsMapLayerLegendUtils.setLegendNodeOrder( nodeLayer, order )
#     mItemTreeView.layerTreeModel().refreshLayerLegend( nodeLayer )
#   }
#
#   # then remove layer tree nodes
#   Q_FOREACH ( const QPersistentModelIndex& index, indexes )
#   {
#     if ( index.isValid() && mItemTreeView.layerTreeModel().index2node( index ) )
#       mLegend.modelV2().removeRow( index.row(), index.parent() )
#   }
#
#   mLegend.adjustBoxSize()
#   mLegend.updateItem()
#   mLegend.endCommand()
# }
#
# def on_mEditPushButton_clicked()
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   QModelIndex idx = mItemTreeView.selectionModel().currentIndex()
#   on_mItemTreeView_doubleClicked( idx )
# }
#
# def resetLayerNodeToDefaults()
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   #get current item
#   QModelIndex currentIndex = mItemTreeView.currentIndex()
#   if ( !currentIndex.isValid() )
#   {
#     return
#   }
#
#   QgsLayerTreeLayer* nodeLayer = nullptr
#   if ( QgsLayerTreeNode* node = mItemTreeView.layerTreeModel().index2node( currentIndex ) )
#   {
#     if ( QgsLayerTree.isLayer( node ) )
#       nodeLayer = QgsLayerTree.toLayer( node )
#   }
#   if ( QgsLayerTreeModelLegendNode* legendNode = mItemTreeView.layerTreeModel().index2legendNode( currentIndex ) )
#   {
#     nodeLayer = legendNode.layerNode()
#   }
#
#   if ( !nodeLayer )
#     return
#
#   mLegend.beginCommand( QString( "Legend updated" ) )
#
#   Q_FOREACH ( const QString& key, nodeLayer.customProperties() )
#   {
#     if ( key.startsWith( "legend/" ) )
#       nodeLayer.removeCustomProperty( key )
#   }
#
#   mItemTreeView.layerTreeModel().refreshLayerLegend( nodeLayer )
#
#   mLegend.updateItem()
#   mLegend.adjustBoxSize()
#   mLegend.endCommand()
# }
#
# def on_mCountToolButton_clicked( bool checked )
# {
#   QgsDebugMsg( "Entered." )
#   if ( !mLegend )
#   {
#     return
#   }
#
#   #get current item
#   QModelIndex currentIndex = mItemTreeView.currentIndex()
#   if ( !currentIndex.isValid() )
#   {
#     return
#   }
#
#   QgsLayerTreeNode* currentNode = mItemTreeView.currentNode()
#   if ( !QgsLayerTree.isLayer( currentNode ) )
#     return
#
#   mLegend.beginCommand( QString( "Legend updated" ) )
#   currentNode.setCustomProperty( "showFeatureCount", checked ? 1 : 0 )
#   mLegend.updateItem()
#   mLegend.adjustBoxSize()
#   mLegend.endCommand()
# }
#
# def on_mFilterByMapToolButton_toggled( bool checked )
# {
#   mLegend.beginCommand( QString( "Legend updated" ) )
#   mLegend.setLegendFilterByMapEnabled( checked )
#   mLegend.adjustBoxSize()
#   mLegend.endCommand()
# }
#
# def on_mExpressionFilterButton_toggled( bool checked )
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   #get current item
#   QModelIndex currentIndex = mItemTreeView.currentIndex()
#   if ( !currentIndex.isValid() )
#   {
#     return
#   }
#
#   QgsLayerTreeNode* currentNode = mItemTreeView.currentNode()
#   if ( !QgsLayerTree.isLayer( currentNode ) )
#     return
#
#   QgsLayerTreeUtils.setLegendFilterByExpression( *qobject_cast<QgsLayerTreeLayer*>( currentNode ),
#       mExpressionFilterButton.expressionText(),
#       checked )
#
#   mLegend.beginCommand( QString( "Legend updated" ) )
#   mLegend.updateItem()
#   mLegend.adjustBoxSize()
#   mLegend.endCommand()
# }
#
# def on_mUpdateAllPushButton_clicked()
# {
#   updateLegend()
# }
#
# def on_mAddGroupToolButton_clicked()
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend group added" ) )
#     mLegend.modelV2().rootGroup().addGroup( QString( "Group" ) )
#     mLegend.updateItem()
#     mLegend.endCommand()
#   }
# }
#
# def on_mFilterLegendByAtlasCheckBox_toggled( bool toggled )
# {
#   if ( mLegend )
#   {
#     mLegend.setLegendFilterOutAtlas( toggled )
#     # force update of legend when in preview mode
#     if ( mLegend.composition().atlasMode() == QgsComposition.PreviewAtlas )
#     {
#       mLegend.composition().atlasComposition().refreshFeature()
#     }
#   }
# }
#
# def updateLegend()
# {
#   if ( mLegend )
#   {
#     mLegend.beginCommand( QString( "Legend updated" ) )
#
#     # self will reset the model completely, loosing any changes
#     mLegend.setAutoUpdateModel( True )
#     mLegend.setAutoUpdateModel( False )
#     mLegend.updateItem()
#     mLegend.endCommand()
#   }
# }
#
# def blockAllSignals( bool b )
# {
#   mTitleLineEdit.blockSignals( b )
#   mTitleAlignCombo.blockSignals( b )
#   mItemTreeView.blockSignals( b )
#   mCheckBoxAutoUpdate.blockSignals( b )
#   mMapComboBox.blockSignals( b )
#   mFilterByMapToolButton.blockSignals( b )
#   mColumnCountSpinBox.blockSignals( b )
#   mSplitLayerCheckBox.blockSignals( b )
#   mEqualColumnWidthCheckBox.blockSignals( b )
#   mSymbolWidthSpinBox.blockSignals( b )
#   mSymbolHeightSpinBox.blockSignals( b )
#   mGroupSpaceSpinBox.blockSignals( b )
#   mLayerSpaceSpinBox.blockSignals( b )
#   mSymbolSpaceSpinBox.blockSignals( b )
#   mIconLabelSpaceSpinBox.blockSignals( b )
#   mBoxSpaceSpinBox.blockSignals( b )
#   mColumnSpaceSpinBox.blockSignals( b )
#   mFontColorButton.blockSignals( b )
#   mRasterBorderGroupBox.blockSignals( b )
#   mRasterBorderColorButton.blockSignals( b )
#   mRasterBorderWidthSpinBox.blockSignals( b )
#   mWmsLegendWidthSpinBox.blockSignals( b )
#   mWmsLegendHeightSpinBox.blockSignals( b )
#   mCheckboxResizeContents.blockSignals( b )
#   mTitleSpaceBottomSpinBox.blockSignals( b )
# }
#
# def refreshMapComboBox()
# {
#   if ( !mLegend )
#   {
#     return
#   }
#
#   const QgsComposition* composition = mLegend.composition()
#   if ( !composition )
#   {
#     return
#   }
#
#   #save current entry
#   int currentMapId = mMapComboBox.itemData( mMapComboBox.currentIndex() ).toInt()
#   mMapComboBox.clear()
#
#   QList<const QgsComposerMap*> availableMaps = composition.composerMapItems()
#   QList<const QgsComposerMap*>.const_iterator mapItemIt = availableMaps.constBegin()
#   for (  mapItemIt != availableMaps.constEnd() ++mapItemIt )
#   {
#     mMapComboBox.addItem( QString( "Map %1" ).arg(( *mapItemIt ).id() ), ( *mapItemIt ).id() )
#   }
#   mMapComboBox.addItem( QString( "None" ), -1 )
#
#   #the former entry is not there anymore
#   int entry = mMapComboBox.findData( currentMapId )
#   if ( entry == -1 )
#   {
#   }
#   else
#   {
#     mMapComboBox.setCurrentIndex( entry )
#   }
# }
#
# def showEvent( QShowEvent * event )
# {
#   refreshMapComboBox()
#   QWidget.showEvent( event )
# }
#
# def selectedChanged( const QModelIndex & current, const QModelIndex & previous )
# {
#   Q_UNUSED( current )
#   Q_UNUSED( previous )
#   QgsDebugMsg( "Entered" )
#
#   if ( mLegend && mLegend.autoUpdateModel() )
#     return
#
#   mCountToolButton.setChecked( False )
#   mCountToolButton.setEnabled( False )
#
#   mExpressionFilterButton.blockSignals( True )
#   mExpressionFilterButton.setChecked( False )
#   mExpressionFilterButton.setEnabled( False )
#   mExpressionFilterButton.blockSignals( False )
#
#   QgsLayerTreeNode* currentNode = mItemTreeView.currentNode()
#   if ( !QgsLayerTree.isLayer( currentNode ) )
#     return
#
#   QgsLayerTreeLayer* currentLayerNode = QgsLayerTree.toLayer( currentNode )
#   QgsVectorLayer* vl = qobject_cast<QgsVectorLayer*>( currentLayerNode.layer() )
#   if ( !vl )
#     return
#
#   mCountToolButton.setChecked( currentNode.customProperty( "showFeatureCount", 0 ).toInt() )
#   mCountToolButton.setEnabled( True )
#
#   bool exprEnabled
#   QString expr = QgsLayerTreeUtils.legendFilterByExpression( *qobject_cast<QgsLayerTreeLayer*>( currentNode ), &exprEnabled )
#   mExpressionFilterButton.blockSignals( True )
#   mExpressionFilterButton.setExpressionText( expr )
#   mExpressionFilterButton.setVectorLayer( vl )
#   mExpressionFilterButton.setEnabled( True )
#   mExpressionFilterButton.setChecked( exprEnabled )
#   mExpressionFilterButton.blockSignals( False )
# }
#
# def setCurrentNodeStyleFromAction()
# {
#   QAction* a = qobject_cast<QAction*>( sender() )
#   if ( !a || !mItemTreeView.currentNode() )
#     return
#
#   QgsLegendRenderer.setNodeLegendStyle( mItemTreeView.currentNode(), ( QgsComposerLegendStyle.Style ) a.data().toInt() )
#   mLegend.updateItem()
# }
#
# def updateFilterLegendByAtlasButton()
# {
#   const QgsAtlasComposition& atlas = mLegend.composition().atlasComposition()
#   mFilterLegendByAtlasCheckBox.setEnabled( atlas.enabled() && atlas.coverageLayer() && atlas.coverageLayer().geometryType() == QGis.Polygon )
# }
#
# def on_mItemTreeView_doubleClicked( const QModelIndex &idx )
# {
#   if ( !mLegend || !idx.isValid() )
#   {
#     return
#   }
#
#   QgsLayerTreeModel* model = mItemTreeView.layerTreeModel()
#   QgsLayerTreeNode* currentNode = model.index2node( idx )
#   QgsLayerTreeModelLegendNode* legendNode = model.index2legendNode( idx )
#   QString currentText
#
#   if ( QgsLayerTree.isGroup( currentNode ) )
#   {
#     currentText = QgsLayerTree.toGroup( currentNode ).name()
#   }
#   else if ( QgsLayerTree.isLayer( currentNode ) )
#   {
#     currentText = QgsLayerTree.toLayer( currentNode ).layerName()
#     QVariant v = currentNode.customProperty( "legend/title-label" )
#     if ( !v.isNull() )
#       currentText = v.toString()
#   }
#   else if ( legendNode )
#   {
#     currentText = legendNode.data( Qt.EditRole ).toString()
#   }
#
#   bool ok
#   QString newText = QInputDialog.getText( self, QString( "Legend item properties" ), QString( "Item text" ),
#                     QLineEdit.Normal, currentText, &ok )
#   if ( !ok || newText == currentText )
#     return
#
#   mLegend.beginCommand( QString( "Legend item edited" ) )
#
#   if ( QgsLayerTree.isGroup( currentNode ) )
#   {
#     QgsLayerTree.toGroup( currentNode ).setName( newText )
#   }
#   else if ( QgsLayerTree.isLayer( currentNode ) )
#   {
#     currentNode.setCustomProperty( "legend/title-label", newText )
#
#     # force update of label of the legend node with embedded icon (a bit clumsy i know)
#     QList<QgsLayerTreeModelLegendNode*> nodes = model.layerLegendNodes( QgsLayerTree.toLayer( currentNode ) )
#     if ( nodes.count() == 1 && nodes[0].isEmbeddedInParent() )
#       nodes[0].setUserLabel( QString() )
#   }
#   else if ( legendNode )
#   {
#     QList<int> order = QgsMapLayerLegendUtils.legendNodeOrder( legendNode.layerNode() )
#     #find unfiltered row number
#     QList<QgsLayerTreeModelLegendNode*> layerLegendNodes = model.layerOriginalLegendNodes( legendNode.layerNode() )
#     int unfilteredRowIndex = layerLegendNodes.indexOf( legendNode )
#     int originalIndex = ( unfilteredRowIndex >= 0 && unfilteredRowIndex < order.count() ? order[unfilteredRowIndex] : -1 )
#     QgsMapLayerLegendUtils.setLegendNodeUserLabel( legendNode.layerNode(), originalIndex, newText )
#     model.refreshLayerLegend( legendNode.layerNode() )
#   }
#
#   mLegend.adjustBoxSize()
#   mLegend.updateItem()
#   mLegend.endCommand()
# }
#
#
# #
# # QgsComposerLegendMenuProvider
# #
#
# QgsComposerLegendMenuProvider.QgsComposerLegendMenuProvider( QgsLayerTreeView* view, QgsComposerLegendWidget* w )
#     : mView( view )
#     , mWidget( w )
# {}
#
# QMenu*QgsComposerLegendMenuProvider.createContextMenu()
# {
#   if ( !mView.currentNode() )
#     return nullptr
#
#   if ( mWidget.legend().autoUpdateModel() )
#     return nullptr # no editing allowed
#
#   QMenu* menu = new QMenu()
#
#   if ( QgsLayerTree.isLayer( mView.currentNode() ) )
#   {
#     menu.addAction( QString( "Reset to defaults" ), mWidget, SLOT( resetLayerNodeToDefaults() ) )
#     menu.addSeparator()
#   }
#
#   QgsComposerLegendStyle.Style currentStyle = QgsLegendRenderer.nodeLegendStyle( mView.currentNode(), mView.layerTreeModel() )
#
#   QList<QgsComposerLegendStyle.Style> lst
#   lst << QgsComposerLegendStyle.Hidden << QgsComposerLegendStyle.Group << QgsComposerLegendStyle.Subgroup
#   Q_FOREACH ( QgsComposerLegendStyle.Style style, lst )
#   {
#     QAction* action = menu.addAction( QgsComposerLegendStyle.styleLabel( style ), mWidget, SLOT( setCurrentNodeStyleFromAction() ) )
#     action.setCheckable( True )
#     action.setChecked( currentStyle == style )
#     action.setData(( int ) style )
#   }
#
#   return menu
# }
#
