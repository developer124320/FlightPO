

from qgis.core import QgsComposition
from qgis.gui import QgsComposerView
from PyQt4.QtGui import QGraphicsScene
from PyQt4.QtCore import SIGNAL
class CompositiononWidget(QgsComposition):
    def __init__(self, mapRenderer):
        QgsComposition.__init__(self, mapRenderer)

        self.drawShapeType = "Line"
        self.setPlotStyle(QgsComposition.Print)
    def mouseReleaseEvent(self, mouseEvent):
        self.emit(SIGNAL("mouseReleaseEvent()"))

    def mousePressEvent(self, mouseEvent):
        self.emit(SIGNAL("mousePressEvent()"))