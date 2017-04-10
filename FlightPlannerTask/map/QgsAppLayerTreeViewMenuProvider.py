'''
Created on 3 Feb 2015

@author: Administrator
'''

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMenu
from qgis.gui import QgsLayerTreeViewMenuProvider
from qgis.core import QgsLayerTree, QgsMapLayerRegistry, QgsRectangle, QgsMapLayer, QGis\
                , QgsLayerTreeGroup, QgsVectorLayer, QgsRasterLayer

from FlightPlanner.QgisHelper import QgisHelper
from map.QgsAttributeTableDialog import QgsAttributeTableDialog
from map.layerSaveAsDlg import layerSaveAsDlg
from map.vectorLayerPropertyDlg import vectorLayerPropertyDlg
from map.rasterLayerPropertyDlg import rasterLayerPropertyDlg
import define

class QgsAppLayerTreeViewMenuProvider(QgsLayerTreeViewMenuProvider):
    '''
    classdocs
    '''

    def __init__(self, view):
        '''
        Constructor
        '''
        QgsLayerTreeViewMenuProvider.__init__(self)
        self.mView = view
        self.overviewLayerset =[]
    def openAttriTable(self):        
        mDialog = QgsAttributeTableDialog(self.mView,self.mView.currentLayer() )
#         mDialog.setWindowFlags(Qt.Widget)
        mDialog.show()

    def uniqueGroupName( self, parentGroup ):
        if parentGroup == self.mView.layerTreeModel().rootGroup():
            prefix =  "group" 
        else:
            prefix = "sub-group"
        newName = prefix + "1"
        i = 2
        groupNumber = parentGroup.findGroup( newName )
        while i < groupNumber:
            newName = prefix + str( i )
            i += 1
        return newName
    
    def addGroup(self):
        group = self.mView.currentGroupNode()
        if group:
            group = self.mView.layerTreeModel().rootGroup()
        
        newGroup = group.addGroup( self.uniqueGroupName( group ) )
        self.mView.edit( self.mView.layerTreeModel().node2index( newGroup ) ) 
        
    def zoomToGroup(self):
        groupNode = self.mView.currentGroupNode();
        if groupNode == None:
            return

        layers = []
        for layerId in groupNode.findLayerIds():
            layers.append(QgsMapLayerRegistry.instance().mapLayer( layerId ))
        
        QgisHelper.zoomToLayers(layers)
  
        
    def zoomToLayer(self):
        QgisHelper.zoomToLayers([self.mView.currentLayer()])
    
    def rename(self):
        self.mView.edit( self.mView.currentIndex() )
        
    def removeLayer(self):
        isSelectedUsersLayerGroup = False
        for node in self.mView.selectedNodes( True ) :
            # could be more efficient if working directly with ranges instead of individual nodes
            if isinstance(node, QgsLayerTreeGroup) and (node.name() == "Users layer" or node.name() == "Lines"):
                isSelectedUsersLayerGroup = True
            else:
                item = node.parent()
                item._class_ = QgsLayerTreeGroup
                if isinstance(item, QgsLayerTreeGroup):
                    if item.name() == "Users layer" or item.name() == "Lines":
                        isSelectedUsersLayerGroup = True

            node.parent().removeChildNode( node )
        if isSelectedUsersLayerGroup:
            define._userLayers = None
         
    def groupSelected(self):
        nodes = self.mView.selectedNodes( True )
        if len(nodes) < 2 or not QgsLayerTree.isGroup( nodes[0].parent() ):
            return
        
        parentGroup = nodes[0].parent()
        insertIdx = parentGroup.children().index( nodes[0] )
        
        newGroup = QgsLayerTreeGroup( self.uniqueGroupName( parentGroup ) )
        for node in nodes:
            newGroup.addChildNode( node.clone() )
            
        parentGroup.insertChildNode( insertIdx, newGroup )
  
        for node in nodes:
            group = node.parent()
            if  group != None:
                group.removeChildNode( node )
        self.mView.setCurrentIndex( self.mView.layerTreeModel().node2index( newGroup ) )
    def saveAs(self):
        saveDld = layerSaveAsDlg(self.mView, self.mView.currentLayer())
        saveDld.exec_()
    def layerProperty(self):
        dlg = None
        if isinstance(self.mView.currentLayer(), QgsVectorLayer):
            dlg = vectorLayerPropertyDlg(self.mView, self.mView.currentLayer())
        elif isinstance(self.mView.currentLayer(), QgsRasterLayer):
            dlg = rasterLayerPropertyDlg(self.mView, self.mView.currentLayer())
        if dlg != None:
            dlg.exec_()
    def showOverview(self):
#         if self.actionShowOverview.isChecked():
        node = self.mView.currentNode()
        value = node.customProperty("overview",  0).toInt()
        if value[0] ==0:
            node.setCustomProperty("overview", 1)
        else:
            node.setCustomProperty("overview", 0)
            
    def createContextMenu(self):
        menu = QMenu()
        actionAddGroup = QgisHelper.createAction(menu, "&Add GroupLayer", self.addGroup)
        actionZoomToGroup = QgisHelper.createAction(menu, "&Zoom To Group", self.zoomToGroup)
        actionRenameGroupOrLayer = QgisHelper.createAction(menu, "&Rename", self.rename)
        actionRemoveLayer = QgisHelper.createAction(menu, "&Remove", self.removeLayer)
        actionGroupSelected = QgisHelper.createAction(menu, "&Group Selected", self.groupSelected)
        actionZoomToLayer = QgisHelper.createAction(menu, "&Zoom To Layer", self.zoomToLayer)
        actionOpenAttributetable = QgisHelper.createAction(menu, "&Open Attribute Table", self.openAttriTable)
        actionSaveAs = QgisHelper.createAction(menu, "&Save as...", self.saveAs)
        actionLayerProperty = QgisHelper.createAction(menu, "&Property", self.layerProperty)
        self.actionShowOverview = QgisHelper.createAction(menu, "&Show in overview...", self.showOverview, None, None, None, True)
        
        idx = self.mView.currentIndex()
        node = self.mView.layerTreeModel().index2node( idx )
        if  not idx.isValid() :
            #global menu
            menu.addAction( actionAddGroup )
#             menu.addAction( QgsApplication.getThemeIcon( "/mActionExpandTree.png" ),  "&Expand All" , self.mView,  "expandAll()"  )
#             menu.addAction( QgsApplication.getThemeIcon( "/mActionCollapseTree.png" ), "&Collapse All" , self.mView,  "collapseAll()"  )
        elif ( node != None ):
            if ( QgsLayerTree.isGroup( node ) ):                
                menu.addAction(actionZoomToGroup)
                menu.addAction(actionRemoveLayer)
#       menu.addAction( QgsApplication.getThemeIcon( "/mActionSetCRS.png" ),
#                        tr( "&Set Group CRS" ), QgisApp.instance(), SLOT( legendGroupSetCRS() ) );
                menu.addAction(actionRenameGroupOrLayer)

                if ( str(self.mView.selectedNodes( True )) >= 2 ):
                    menu.addAction(actionGroupSelected)
                menu.addAction(actionAddGroup)
    
            elif ( QgsLayerTree.isLayer( node ) ):
                menu.addAction(actionZoomToLayer)
                menu.addAction(actionRemoveLayer)
                menu.addAction(self.actionShowOverview)
                if self.mView.currentLayer().type() == QgsMapLayer.VectorLayer:
                    menu.addAction(actionOpenAttributetable)
                menu.addAction(actionLayerProperty)
                menu.addAction(actionSaveAs)
#                 menu.addAction( actions.actionShowInOverview( menu ) )            
#                 if layer.type() == QgsMapLayer.RasterLayer :
#                     menu.addAction(  "&Zoom to Best Scale (100%)" , QgisApp.instance(), " legendLayerZoomNative() " )            
#                     rasterLayer =  qobject_cast<QgsRasterLayer *>( layer );
#                     if ( rasterLayer && rasterLayer.rastertype() != QgsRasterLayer.Palette )
#                       menu.addAction( tr( "&Stretch Using Current Extent" ), QgisApp.instance(), SLOT( legendLayerStretchUsingCurrentExtent() ) );
#                   }

#                 menu.addAction( QgsApplication.getThemeIcon( "/mActionRemoveLayer.svg" ), tr( "&Remove" ), QgisApp.instance(), " removeLayer() ");

#       // duplicate layer
#       QAction* duplicateLayersAction = menu.addAction( QgsApplication.getThemeIcon( "/mActionDuplicateLayer.svg" ), tr( "&Duplicate" ), QgisApp.instance(), SLOT( duplicateLayers() ) );
# 
#       // set layer scale visibility
#       menu.addAction( tr( "&Set Layer Scale Visibility" ), QgisApp.instance(), SLOT( setLayerScaleVisibility() ) );
# 
#       // set layer crs
#       menu.addAction( QgsApplication.getThemeIcon( "/mActionSetCRS.png" ), tr( "&Set Layer CRS" ), QgisApp.instance(), SLOT( setLayerCRS() ) );
# 
#       // assign layer crs to project
#       menu.addAction( QgsApplication.getThemeIcon( "/mActionSetProjectCRS.png" ), tr( "Set &Project CRS from Layer" ), QgisApp.instance(), SLOT( setProjectCRSFromLayer() ) );
# 
#       menu.addSeparator();
# 
#       if ( layer && layer.type() == QgsMapLayer.VectorLayer )
#       {
#         QgsVectorLayer* vlayer = qobject_cast<QgsVectorLayer *>( layer );
# 
#         QAction *toggleEditingAction = QgisApp.instance().actionToggleEditing();
#         QAction *saveLayerEditsAction = QgisApp.instance().actionSaveActiveLayerEdits();
#         QAction *allEditsAction = QgisApp.instance().actionAllEdits();
# 
#         // attribute table
#         menu.addAction( QgsApplication.getThemeIcon( "/mActionOpenTable.png" ), tr( "&Open Attribute Table" ),
#                          QgisApp.instance(), SLOT( attributeTable() ) );
# 
#         // allow editing
#         int cap = vlayer.dataProvider().capabilities();
#         if ( cap & QgsVectorDataProvider.EditingCapabilities )
#         {
#           if ( toggleEditingAction )
#           {
#             menu.addAction( toggleEditingAction );
#             toggleEditingAction.setChecked( vlayer.isEditable() );
#           }
#           if ( saveLayerEditsAction && vlayer.isModified() )
#           {
#             menu.addAction( saveLayerEditsAction );
#           }
#         }
# 
#         if ( allEditsAction.isEnabled() )
#           menu.addAction( allEditsAction );
# 
#         // disable duplication of memory layers
#         if ( vlayer.storageType() == "Memory storage" && self.mView.selectedLayerNodes().count() == 1 )
#           duplicateLayersAction.setEnabled( false );
# 
#         // save as vector file
#         menu.addAction( tr( "Save As..." ), QgisApp.instance(), SLOT( saveAsFile() ) );
#         menu.addAction( tr( "Save As Layer Definition File..." ), QgisApp.instance(), SLOT( saveAsLayerDefinition() ) );
# 
#         if ( !vlayer.isEditable() && vlayer.dataProvider().supportsSubsetString() && vlayer.vectorJoins().isEmpty() )
#           menu.addAction( tr( "&Filter..." ), QgisApp.instance(), SLOT( layerSubsetString() ) );
# 
#         menu.addAction( actions.actionShowFeatureCount( menu ) );
# 
#         menu.addSeparator();
#       }
#       else if ( layer && layer.type() == QgsMapLayer.RasterLayer )
#       {
#         menu.addAction( tr( "Save As..." ), QgisApp.instance(), SLOT( saveAsRasterFile() ) );
#         menu.addAction( tr( "Save As Layer Definition File..." ), QgisApp.instance(), SLOT( saveAsLayerDefinition() ) );
#       }
#       else if ( layer && layer.type() == QgsMapLayer.PluginLayer && self.mView.selectedLayerNodes().count() == 1 )
#       {
#         // disable duplication of plugin layers
#         duplicateLayersAction.setEnabled( false );
#       }

#                 addCustomLayerActions( menu, layer );
# 
#       if ( layer && QgsProject.instance().layerIsEmbedded( layer.id() ).isEmpty() )
#         menu.addAction( tr( "&Properties" ), QgisApp.instance(), SLOT( layerProperties() ) );

#             if ( node.parent() != self.mView.layerTreeModel().rootGroup() ):
#                 menu.addAction( actions.actionMakeTopLevel( menu ) )
            menu.addAction(actionRenameGroupOrLayer)
    
            if ( len(self.mView.selectedNodes( True )) >= 2 ):
                menu.addAction(actionGroupSelected)

#       if ( self.mView.selectedLayerNodes().count() == 1 )
#       {
#         QgisApp* app = QgisApp.instance();
#         menu.addAction( tr( "Copy Style" ), app, SLOT( copyStyle() ) );
#         if ( app.clipboard().hasFormat( QGSCLIPBOARD_STYLE_MIME ) )
#         {
#           menu.addAction( tr( "Paste Style" ), app, SLOT( pasteStyle() ) );
#         }
#       }

        return menu
