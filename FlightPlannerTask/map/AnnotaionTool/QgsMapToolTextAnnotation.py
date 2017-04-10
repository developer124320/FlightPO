'''
Created on 3 May 2014

@author: Administrator
'''
from qgis.gui import QgsTextAnnotationItem
from map.AnnotaionTool.QgsMapToolAnnotation import QgsMapToolAnnotation
from PyQt4.QtCore import QSizeF

class QgsMapToolTextAnnotation(QgsMapToolAnnotation):
    def __init__(self, canvas):
        self.mCanvas = canvas
        QgsMapToolAnnotation.__init__(self, self.mCanvas)
    def createItem( self, e ):
        mapCoord = self.toMapCoordinates( e.pos() )
        textItem = QgsTextAnnotationItem( self.mCanvas )
        textItem.setMapPosition( self.toMapCoordinates( e.pos() ) )
        textItem.setFrameSize( QSizeF( 200, 100 ) )
        textItem.setSelected( True )
        return textItem
