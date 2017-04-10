'''
Created on 28 Apr 2014

@author: Administrator
'''
from PyQt4.QtGui import QWidget, QFontComboBox,  QDialog, QDialogButtonBox, QPushButton, QColorDialog, \
    QStackedWidget, QFont, QCursor, QSpinBox, QSpacerItem, QGridLayout, QHBoxLayout
from PyQt4.QtCore import QSizeF, Qt, QObject, SIGNAL, QPointF
from qgis.gui import QgsTextAnnotationItem, QgsAnnotationItem, QgsMapTool
from qgis.core import QgsSymbolLayerV2Utils
# from qgis.core import QgsAnnotationItem
from map.AnnotaionTool.QgsTextAnnotationDialog import QgsTextAnnotationDialog

class QgsMapToolAnnotation(QgsMapTool):
    def __init__(self, canvas):
        self.mCanvas = canvas
        QgsMapTool.__init__(self, self.mCanvas)
        self.mCurrentMoveAction = QgsAnnotationItem.NoAction 
        self.mLastMousePosition = QPointF( 0, 0 )
        self.mCursor = QCursor( Qt.ArrowCursor )
    def createItem(self, e ):
        return None
    def createItemEditor(self, item ):
        if ( item == None ):
            return None
        item._class_ = QgsTextAnnotationItem
        if isinstance(item, QgsTextAnnotationItem):
            return QgsTextAnnotationDialog( item )
        return None
    
    def canvasReleaseEvent( self, e ):
        self.mCurrentMoveAction = QgsAnnotationItem.NoAction
        self.mCanvas.setCursor( self.mCursor )
        
    def canvasPressEvent( self, e ):
        sItem = self.selectedItem()
        if ( sItem != None):
            self.mCurrentMoveAction = sItem.moveActionForPosition( e.posF() )
            if ( self.mCurrentMoveAction != QgsAnnotationItem.NoAction ):
                return
        if ( sItem == None or self.mCurrentMoveAction == QgsAnnotationItem.NoAction ):
            self.mCanvas.scene().clearSelection()
            existingItem = self.itemAtPos( e.posF() )
            if ( existingItem != None):
                existingItem.setSelected( True )
            else:
                self.createItem( e )
    def keyPressEvent(self, e ):
        if ( e.key() == Qt.Key_T and e.modifiers() == Qt.ControlModifier ):
            self.toggleTextItemVisibilities()
        sItem = self.selectedItem()
        if ( sItem != None ):
            if ( e.key() == Qt.Key_Backspace or e.key() == Qt.Key_Delete ):
                neutralCursor = QCursor( sItem.cursorShapeForAction( QgsAnnotationItem.NoAction ) )
                self.mCanvas.scene().removeItem( sItem )
                self.mCanvas.setCursor( neutralCursor )
                
                #// Override default shortcut management in MapCanvas
                e.ignore()
    
    def canvasMoveEvent( self, e ):
        sItem = self.selectedItem()
        if ( sItem != None and ( e.buttons() & Qt.LeftButton ) ):
            if ( self.mCurrentMoveAction == QgsAnnotationItem.MoveMapPosition ):
                sItem.setMapPosition( self.toMapCoordinates( e.pos() ) )
                sItem.update()
            elif ( self.mCurrentMoveAction == QgsAnnotationItem.MoveFramePosition ):
                if ( sItem.mapPositionFixed() ):
                    sItem.setOffsetFromReferencePoint( sItem.offsetFromReferencePoint() + ( e.posF() - self.mLastMousePosition ) )
                else:
                    newCanvasPos = sItem.pos() + ( e.posF() - self.mLastMousePosition )
                    sItem.setMapPosition( self.toMapCoordinates( newCanvasPos.toPoint() ) )
                sItem.update()
            elif ( self.mCurrentMoveAction != QgsAnnotationItem.NoAction ):
                size = sItem.frameSize()
                xmin = sItem.offsetFromReferencePoint().x()
                ymin = sItem.offsetFromReferencePoint().y()
                xmax = xmin + size.width()
                ymax = ymin + size.height()
                
                if ( self.mCurrentMoveAction == QgsAnnotationItem.ResizeFrameRight or
                   self.mCurrentMoveAction == QgsAnnotationItem.ResizeFrameRightDown or
                   self.mCurrentMoveAction == QgsAnnotationItem.ResizeFrameRightUp ):
                    xmax += e.posF().x() - self.mLastMousePosition.x()
                if ( self.mCurrentMoveAction == QgsAnnotationItem.ResizeFrameLeft or
                   self.mCurrentMoveAction == QgsAnnotationItem.ResizeFrameLeftDown or
                   self.mCurrentMoveAction == QgsAnnotationItem.ResizeFrameLeftUp ):
                    xmin += e.posF().x() - self.mLastMousePosition.x()
                if ( self.mCurrentMoveAction == QgsAnnotationItem.ResizeFrameUp or
                   self.mCurrentMoveAction == QgsAnnotationItem.ResizeFrameLeftUp or
                   self.mCurrentMoveAction == QgsAnnotationItem.ResizeFrameRightUp ):
                    ymin += e.posF().y() - self.mLastMousePosition.y()
                if ( self.mCurrentMoveAction == QgsAnnotationItem.ResizeFrameDown or
                   self.mCurrentMoveAction == QgsAnnotationItem.ResizeFrameLeftDown or
                   self.mCurrentMoveAction == QgsAnnotationItem.ResizeFrameRightDown ):
                    ymax += e.posF().y() - self.mLastMousePosition.y()
                
                #//switch min / max if necessary
                tmp = 0.0
                if ( xmax < xmin ):
                    tmp = xmax
                    xmax = xmin 
                    xmin = tmp
                if ( ymax < ymin ):
                    tmp = ymax 
                    ymax = ymin 
                    ymin = tmp
                sItem.setOffsetFromReferencePoint( QPointF( xmin, ymin ) )
                sItem.setFrameSize( QSizeF( xmax - xmin, ymax - ymin ) )
                sItem.update()
        elif ( sItem != None):
            moveAction = sItem.moveActionForPosition( e.posF() )
            self.mCanvas.setCursor( QCursor( sItem.cursorShapeForAction( moveAction ) ) )
        self.mLastMousePosition = e.posF()
        
    def canvasDoubleClickEvent( self, e ):
        item = self.itemAtPos( e.posF() )
        if ( item == None ):
            return
        itemEditor = self.createItemEditor( item )
        if ( itemEditor != None ):
            itemEditor.exec_()
    def itemAtPos( self, pos ):
        graphicItems = self.mCanvas.items( pos.toPoint() )
        for annotationItem in graphicItems:
            annotationItem._class_ = QgsAnnotationItem
            if ( isinstance(annotationItem, QgsAnnotationItem) ):
                return annotationItem
        return None
    def selectedItem(self):
        gItemList = self.mCanvas.scene().selectedItems()
        for aItem in gItemList:
            aItem._class_ = QgsAnnotationItem
            if (isinstance(aItem, QgsAnnotationItem) ):
                return aItem
        return None
    def annotationItems(self):
        annotationItemList = []
        itemList = self.mCanvas.scene().items()
        for aItem in itemList:
            aItem._class_ = QgsAnnotationItem
            if ( isinstance(aItem, QgsAnnotationItem)):
                self.annotationItemList.append( aItem )
        return annotationItemList
    def toggleTextItemVisibilities(self):
        itemList = self.annotationItems()
        for textItem in itemList:
            textItem._class_ = QgsTextAnnotationItem
            if ( isinstance(textItem, QgsTextAnnotationItem) ):
                textItem.setVisible( not textItem.isVisible() )
                