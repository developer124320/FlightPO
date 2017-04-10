'''
Created on Feb 6, 2015

@author: KangKuk
'''

from PyQt4.QtCore import QModelIndex, SIGNAL

from qgis.gui import QgsLayerTreeView

class MyLayerTreeView(QgsLayerTreeView):
    def __init__(self, parent = None):
        QgsLayerTreeView.__init__(self, parent)

    def contextMenuEvent(self, event):
        if ( self.menuProvider() is None ):
            return
        idx = self.indexAt( event.pos() )
        if not idx.isValid() :
            self.setCurrentIndex( QModelIndex() )
        menu = self.menuProvider().createContextMenu()
        actions = menu.actions()
        if menu != None and len(actions) != 0:
            menu.exec_( self.mapToGlobal( event.pos() ) )
    # def mouseReleaseEvent(self, e):
    #     self.emit(SIGNAL("mouseReleaseEvent()"))
        
        
    