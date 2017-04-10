# -*- coding: utf-8 -*-

from PyQt4.QtGui import QTableView, QMenu
from PyQt4.QtCore import Qt, SIGNAL

class TableViewObstacle(QTableView):
    def __init__(self, parent):
        QTableView.__init__(self, parent)
        self.pressed.connect(self.pressedEvent)
    def pressedEvent(self, modelIndex):
        self.emit(SIGNAL("pressedEvent"), modelIndex)
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.RightButton:
            self.emit(SIGNAL("tableViewObstacleMouseReleaseEvent_rightButton"), e)
