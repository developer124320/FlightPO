# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''


from Charting.ui_chartingBase import Ui_ChartingBase
from PyQt4.QtGui import QGraphicsRectItem
from PyQt4.QtCore import *
# import PyQt4
from PyQt4.QtGui import  QGraphicsProxyWidget, QDialog,QFontDialog, QColorDialog, QVBoxLayout,\
     QGridLayout, QSpinBox, QShortcut, QKeySequence, QWidget, QSpacerItem,\
    QGroupBox, QFrame, QWidget,QGraphicsRectItem, QLabel, QComboBox, QHBoxLayout,\
     QPushButton, QDialogButtonBox, QToolBar, QAction, QIcon,\
      QFont,QPlainTextEdit,QCheckBox, QPen, QBrush, QColor,QTableView, QStandardItemModel, QStandardItem
from qgis.core import QgsComposerMap, QgsComposition, QgsComposerLabel,QgsComposerItem,QgsComposerMergeCommand, QgsComposerShape, QgsComposerPicture
from qgis.gui import QgsComposerView, QgsComposerRuler,QgsPreviewEffect
from Charting.previewDlg import previewDlg
from Composer.ComposerDlg import ComposerDlg
from Charting.ComposerView import CompositiononWidget
from FlightPlanner.helpers import Unit, AngleGradientSlope

import define, math
class DlgCharting(QDialog):
    def __init__(self, parent, data):
        QDialog.__init__(self, parent)
        self.ui = Ui_ChartingBase()
        self.ui.setupUi(self)


        self.setWindowTitle("Charting Tool 2")

        # self.ui.btnNext.clicked.connect(self.btnNext_clicked)
        self.ui.btnPrevious.clicked.connect(self.btnPrevious_clicked)
        self.ui.btnExit.clicked.connect(self.btnExit_clicked)

        self.ui.txtText1.textChanged.connect(self.txtText1_textChanged)
        self.ui.txtText2.textChanged.connect(self.txtText2_textChanged)
        self.ui.txtText3.textChanged.connect(self.txtText3_textChanged)
        self.ui.txtText4.textChanged.connect(self.txtText4_textChanged)
        self.ui.txtText5.textChanged.connect(self.txtText5_textChanged)
        self.ui.txtText6.textChanged.connect(self.txtText6_textChanged)
        self.ui.txtText7.textChanged.connect(self.txtText7_textChanged)
        self.ui.txtText8.textChanged.connect(self.txtText8_textChanged)
        self.ui.txtText9.textChanged.connect(self.txtText9_textChanged)
        self.ui.txtText10.textChanged.connect(self.txtText10_textChanged)
        self.ui.txtText11.textChanged.connect(self.txtText11_textChanged)
        self.ui.txtText12.textChanged.connect(self.txtText12_textChanged)
        self.ui.txtText13.textChanged.connect(self.txtText13_textChanged)







        # self.btnNextAndbtnPreviewSetEnabled()
        self.setDataDict = None
        self.parentDlg = parent
        self.pw = None
        self.stdModel = None
        self.data = data
        self.renderFlag = False
        self.changedComposerMap = None
        self.tableChangedValue = None
        self.straightCount = self.data["StraightCount"]
        self.catOfAcftCount = self.data["CatOfAcftCount"][0]

        self.rejected.connect(self.dlgRejected)

    def dlgRejected(self):
        self.parentDlg.show()
    def refreshData(self, data):
        self.data = data
    def txtText1_textChanged(self):
        self.txt1.setText(self.ui.txtText1.text())
    def txtText2_textChanged(self):
        self.txt2.setText(self.ui.txtText2.text())
    def txtText3_textChanged(self):
        self.txt3.setText(self.ui.txtText3.text())
    def txtText4_textChanged(self):
        self.txt4.setText(self.ui.txtText4.toPlainText())
    def txtText5_textChanged(self):
        self.txt5.setText(self.ui.txtText5.toPlainText())
    def txtText6_textChanged(self):
        self.txt6.setText(self.ui.txtText6.toPlainText())
    def txtText7_textChanged(self):
        try:
            self.txt7.setText(self.ui.txtText7.toPlainText())
        except:
            pass
    def txtText8_textChanged(self):
        self.txt8.setText(self.ui.txtText8.text())
    def txtText9_textChanged(self):
        self.txt9.setText(self.ui.txtText9.text())
    def txtText10_textChanged(self):
        self.txt10.setText(self.ui.txtText10.text())
    def txtText11_textChanged(self):
        self.txt11.setText(self.ui.txtText11.text())
    def txtText12_textChanged(self):
        self.txt12.setText(self.ui.txtText12.text())
    def txtText13_textChanged(self):
        self.txt13.setText(self.ui.txtText13.text())
    # def btnNextAndbtnPreviewSetEnabled(self):
    #     if self.ui.stackedWidget.currentIndex() == 0:
    #         self.ui.btnPrevious.setEnabled(False)
    #         self.ui.frame_2.setVisible(False)
    #         self.resize(100, 100)
    #
    #     else:
    #         self.ui.frame_2.setVisible(True)
    #         self.ui.btnPrevious.setEnabled(True)
    #     if self.ui.stackedWidget.currentIndex() == self.ui.stackedWidget.count() - 1:
    #         self.ui.btnNext.setEnabled(False)
    #     else:
    #         self.ui.btnNext.setEnabled(True)
    def btnExit_clicked(self):
        # comp = QgsComposer(self, define._canvas)
        # comp.show()
        self.setDataDict = dict()
        for key, val in self.data.iteritems():
            self.setDataDict.__setitem__(key, val)
        self.setDataDict.__setitem__("TextData",[self.ui.txtText1.text(), self.ui.txtText2.text(), self.ui.txtText3.text(),
                                         self.ui.txtText4.toPlainText(), self.ui.txtText5.toPlainText(), self.ui.txtText6.toPlainText(),
                                         self.ui.txtText7.toPlainText(), self.ui.txtText8.text(), self.ui.txtText9.text(),
                                         self.ui.txtText10.text(), self.ui.txtText11.text(), self.ui.txtText12.text(), self.ui.txtText13.text()])
        # self.setDataDict.__setitem__("StraightCount", self.straightCount)
        # self.setDataDict.__setitem__("CatOfAcftCount", self.catOfAcftCount)
        comp = None
        if self.pw == None or not isinstance(self.pw, ComposerDlg):
            comp = self.composer(self.setDataDict)
        else:
            comp = self.composer(self.setDataDict, False)
        pwFlag = False


        if self.pw == None or not isinstance(self.pw, ComposerDlg):
            self.pw = ComposerDlg(self, comp, self.stdModel, self.setDataDict)
            pwFlag = True
        if not self.renderFlag:
            self.pw.show()
        if not pwFlag:
            self.pw.rePresent(comp, self.stdModel, self.setDataDict)
        self.renderFlag = False
    def showDlg(self):
        self.pw.hide()
        self.show()
        self.ui.txtText1.setText(self.txt1.text())
        self.ui.txtText2.setText(self.txt2.text())
        self.ui.txtText3.setText(self.txt3.text())
        self.ui.txtText4.setText(self.txt4.text())
        self.ui.txtText5.setText(self.txt5.text())
        self.ui.txtText6.setText(self.txt6.text())
        self.ui.txtText7.setText(self.txt7.text())
        self.ui.txtText8.setText(self.txt8.text())
        self.ui.txtText9.setText(self.txt9.text())
        self.ui.txtText10.setText(self.txt10.text())
        self.ui.txtText11.setText(self.txt11.text())
        self.ui.txtText12.setText(self.txt12.text())
        self.ui.txtText13.setText(self.txt13.text())
    # def btnNext_clicked(self):
    #     if self.ui.stackedWidget.currentIndex() + 1 < self.ui.stackedWidget.count():
    #         self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex() + 1)
    #     self.btnNextAndbtnPreviewSetEnabled()
    def btnPrevious_clicked(self):
        self.setVisible(False)
        self.parent().show()
        # if self.ui.stackedWidget.currentIndex() > 0:
        #     self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex() - 1)
        # self.btnNextAndbtnPreviewSetEnabled()

    def composer(self, setData, flag = True):
        paperWidth = setData["Width"]
        paperHeight = setData["Height"]
        mapRenderer = define._canvas.mapRenderer()
#         comp = None
        comp = QgsComposition(mapRenderer)
        comp.setPlotStyle(QgsComposition.Print)

        comp.setPaperSize(paperWidth, paperHeight)
        # rectangleAll = QgsComposerShape(comp)
        # rectangleAll.setItemPosition(3, 3, paperWidth - 3, paperHeight - 3)
        # rectangleAll.setShapeType(1)
        # comp.addItem(rectangleAll)

        self.txt1 = QgsComposerLabel(comp)
        self.txt1.setItemPosition(20, 20)
        self.txt1.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt1.setFont(font)
        self.txt1.setText(setData["TextData"][0])
        self.txt1.adjustSizeToText()
        comp.addItem(self.txt1)
        
        self.txt2 = QgsComposerLabel(comp)
        self.txt2.setItemPosition(int(paperWidth / 2) + 10, 20)
        self.txt2.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt2.setFont(font)
        self.txt2.setText(setData["TextData"][1])
        self.txt2.adjustSizeToText()
        comp.addItem(self.txt2)
        
        self.txt3 = QgsComposerLabel(comp)
        self.txt3.setItemPosition(paperWidth - 40, 20)
        self.txt3.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt3.setFont(font)
        self.txt3.setText(setData["TextData"][2])
        self.txt3.adjustSizeToText()
        comp.addItem(self.txt3)

        w = int((paperWidth - 40) / 4)

        self.txt4 = QgsComposerLabel(comp)
        self.txt4.setItemPosition(20, 35)
        self.txt4.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt4.setFont(font)
        self.txt4.setText(setData["TextData"][3])
        self.txt4.adjustSizeToText()
        comp.addItem(self.txt4)

        self.txt5 = QgsComposerLabel(comp)
        self.txt5.setItemPosition(20 + w, 35)
        self.txt5.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt5.setFont(font)
        self.txt5.setText(setData["TextData"][4])
        self.txt5.adjustSizeToText()
        comp.addItem(self.txt5)

        self.txt6 = QgsComposerLabel(comp)
        self.txt6.setItemPosition(20 + w * 2, 35)
        self.txt6.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt6.setFont(font)
        self.txt6.setText(setData["TextData"][5])
        self.txt6.adjustSizeToText()
        comp.addItem(self.txt6)

        self.txt7 = QgsComposerLabel(comp)
        self.txt7.setItemPosition(20 + w * 3, 35)
        self.txt7.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt7.setFont(font)
        self.txt7.setText(setData["TextData"][6])
        self.txt7.adjustSizeToText()
        comp.addItem(self.txt7)



        # if flag:
        x, y = 20, 45
        composerMap = QgsComposerMap(comp, x, y, paperWidth - 40, 150)
#         composerMap.setPreviewMode(QgsComposerMap.Render)
#         composerMap.setGridEnabled(False)

        #rect = composerMap.currentMapExtent ()
        renderer = composerMap.mapRenderer()
        newExtent = renderer.extent()

        #Make sure the width/height ratio is the same as in current composer map extent.
        #This is to keep the map item frame and the page layout fixed
        currentMapExtent = composerMap.currentMapExtent()
        currentWidthHeightRatio = currentMapExtent.width() / currentMapExtent.height()
        newWidthHeightRatio = newExtent.width() / newExtent.height()

        if currentWidthHeightRatio < newWidthHeightRatio :
            #enlarge height of new extent, ensuring the map center stays the same
            newHeight = newExtent.width() / currentWidthHeightRatio
            deltaHeight = newHeight - newExtent.height()
            newExtent.setYMinimum( newExtent.yMinimum() - deltaHeight / 2 )
            newExtent.setYMaximum( newExtent.yMaximum() + deltaHeight / 2 )

        else:
            #enlarge width of new extent, ensuring the map center stays the same
            newWidth = currentWidthHeightRatio * newExtent.height()
            deltaWidth = newWidth - newExtent.width()
            newExtent.setXMinimum( newExtent.xMinimum() - deltaWidth / 2 )
            newExtent.setXMaximum( newExtent.xMaximum() + deltaWidth / 2 )

        composerMap.beginCommand( "Map extent changed")
        composerMap.setNewExtent( newExtent )
        composerMap.endCommand()
        # composerMap.setNewScale(3500)

        composerMap.setFrameEnabled(True)
        composerMap.setFrameOutlineWidth(1.0)
        composerMap.setPreviewMode(QgsComposerMap.Render)
        composerMap.updateCachedImage()

        composerMap.setGridEnabled(True)
        composerMap.setGridPenColor(QColor(255,255,255,0))
        composerMap.setGridPenWidth(0.0)
        #composerMap.setGridStyle(QgsComposerMap.FrameAnnotationsOnly)
        composerMap.setGridIntervalX(1.0)
        composerMap.setGridIntervalY(1.0)
#         mySymbol1 = composerMap.gridLineSymbol ()
#         mySymbol1.setAlpha(0)
        #composerMap.setGridLineSymbol(mySymbol1)
        composerMap.setShowGridAnnotation(True)
        composerMap.setGridAnnotationFormat(1)
        composerMap.setGridAnnotationPrecision (0)
        composerMap.setGridAnnotationDirection(1,0)
        composerMap.setGridAnnotationDirection(1,1)

        comp.addItem(composerMap)


        w = int((paperWidth - 40) / 3)

        self.txt8 = QgsComposerLabel(comp)
        self.txt8.setItemPosition(20, 225)
        self.txt8.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt8.setFont(font)
        self.txt8.setText(setData["TextData"][7])
        self.txt8.adjustSizeToText()
        comp.addItem(self.txt8)

        self.txt9 = QgsComposerLabel(comp)
        self.txt9.setItemPosition(20 + w, 225)
        self.txt9.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt9.setFont(font)
        self.txt9.setText(setData["TextData"][8])
        self.txt9.adjustSizeToText()
        comp.addItem(self.txt9)

        self.txt10 = QgsComposerLabel(comp)
        self.txt10.setItemPosition(20 + w * 2, 225)
        self.txt10.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt10.setFont(font)
        self.txt10.setText(setData["TextData"][9])
        self.txt10.adjustSizeToText()
        comp.addItem(self.txt10)

        # profileRect = QgsComposerPicture(comp)
        # profileRect.setItemPosition(20, 200, paperWidth - 40, 50)
        # comp.addItem(profileRect)

        self.txt11 = QgsComposerLabel(comp)
        self.txt11.setItemPosition(20, paperHeight - 30)
        self.txt11.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt11.setFont(font)
        self.txt11.setText(setData["TextData"][10])
        self.txt11.adjustSizeToText()
        comp.addItem(self.txt11)

        self.txt12 = QgsComposerLabel(comp)
        self.txt12.setItemPosition(20 + w, paperHeight - 30)
        self.txt12.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt12.setFont(font)
        self.txt12.setText(setData["TextData"][11])
        self.txt12.adjustSizeToText()
        comp.addItem(self.txt12)

        self.txt13 = QgsComposerLabel(comp)
        self.txt13.setItemPosition(20 + w * 2, paperHeight - 30)
        self.txt13.setFrameEnabled(False)
        font = QFont("Arial", 10)
        self.txt13.setFont(font)
        self.txt13.setText(setData["TextData"][12])
        self.txt13.adjustSizeToText()
        comp.addItem(self.txt13)

        # gpw = QGraphicsProxyWidget()
        self.tblView = QTableView()
        tableHeight = None
        tableWidth = None
        if self.tableChangedValue == None:
            self.tblView.setFixedWidth(paperWidth - 40)
            tableHeight = 50
            tableWidth = paperWidth - 40
            self.tblView.setFixedHeight(tableHeight)
        else:
            self.tblView.setFixedWidth(self.tableChangedValue["Width"])
            self.tblView.setFixedHeight(self.tableChangedValue["Height"])
            tableHeight = self.tableChangedValue["Height"]
            tableWidth = self.tableChangedValue["Width"]
        self.tblView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tblView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        hHeder = self.tblView.horizontalHeader()
        hHeder.setVisible(False)
        vHeder = self.tblView.verticalHeader()
        vHeder.setVisible(False)

        # if flag:
        self.stdModel = QStandardItemModel()
        self.data.__setitem__("TableWidth", tableWidth)
        self.data.__setitem__("TableHeight", tableHeight)
        self.setTableView(self.tblView, self.stdModel, self.data)
        
        self.calcALT()
        self.calcTimeRate()

        self.gpw = 	QGraphicsProxyWidget()
        self.gpw.setWidget(self.tblView)
        # gpw.setWidget(tblView)
        if self.tableChangedValue == None:
            self.gpw.setPos(20, 210)
            font = QFont()
            font.setPixelSize(2)
            self.gpw.setFont(font)
        else:
            self.gpw.setPos(self.tableChangedValue["X"], self.tableChangedValue["Y"])
            font = QFont()
            font.setPixelSize(self.tableChangedValue["FontSize"])
            self.gpw.setFont(font)

        # tblView.setFrameRect(QRect(20, 210, paperWidth - 40, 50))
        comp.addItem(self.gpw)

        self.connect(self.stdModel, SIGNAL("itemChanged(QStandardItem *)"), self.stdModel_itemChanged)
        return comp
    def setTableView(self, tblView, stdModel, data):
        for i in range(7):
            for j in range(12 + data["CatOfAcftCount"][0]):
                item = QStandardItem("")
                item.setEditable(True)
                item.setTextAlignment(Qt.AlignCenter)
                stdModel.setItem(i, j, item)
        item = QStandardItem("O C A ( H )")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(0, 0, item)

        item = QStandardItem("C a t  of  A C F T")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(1, 0, item)

        item = QStandardItem("S t r a i g h t-I n  A p p r o a c h")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(2, 0, item)

        if data["Template"][0] >= 0 and data["Template"][0] <= 4:
            item = QStandardItem("C i r c l i n g")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(4, 0, item)

            item = QStandardItem("F i n a l  A p p r o a c h  L O C  D i s t a n c e  F A F-M A P t")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(0, data["CatOfAcftCount"][0] + 3, item)
        else:
            item = QStandardItem("F i n a l  A p p r o a c h  F A F-M A P t")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(0, data["CatOfAcftCount"][0] + 3, item)
        if data["Template"][0] == 5:
            item = QStandardItem("LPV")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(2, 0, item)

            item = QStandardItem("LNAV / VNAV")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(3, 0, item)

            item = QStandardItem("LNAV")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(4, 0, item)

            item = QStandardItem("C i r c l i n g")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(5, 0, item)
        elif data["Template"][0] == 6:
            item = QStandardItem("LNAV / VNAV")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(2, 0, item)

            item = QStandardItem("LNAV")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(3, 0, item)

            item = QStandardItem("C i r c l i n g")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(4, 0, item)
        elif data["Template"][0] == 7:
            item = QStandardItem("LPV")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(2, 0, item)

            item = QStandardItem("LNAV")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(3, 0, item)

            item = QStandardItem("C i r c l i n g")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(4, 0, item)
        elif data["Template"][0] == 8:
            item = QStandardItem("LNAV")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(2, 0, item)

            item = QStandardItem("C i r c l i n g")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(3, 0, item)
        elif data["Template"][0] == 9:
            item = QStandardItem("RNP 0.3")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(2, 0, item)

            item = QStandardItem("C i r c l i n g")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(3, 0, item)

        if data["CatOfAcftCount"][0] == 1:
            item = QStandardItem("A")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 3, item)
        elif data["CatOfAcftCount"][0] == 2:
            item = QStandardItem("A")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 3, item)

            item = QStandardItem("B")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 4, item)
        elif data["CatOfAcftCount"][0] == 3:
            item = QStandardItem("A")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 3, item)

            item = QStandardItem("B")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 4, item)

            item = QStandardItem("C")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 5, item)
        elif data["CatOfAcftCount"][0] == 4:
            item = QStandardItem("A")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 3, item)

            item = QStandardItem("B")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 4, item)

            item = QStandardItem("C")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 5, item)

            item = QStandardItem("D")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 6, item)
        elif data["CatOfAcftCount"][0] == 5:
            if data["CatOfAcftCount"][1] == 4:
                item = QStandardItem("A")
                item.setTextAlignment(Qt.AlignCenter)
                stdModel.setItem(1, 3, item)

                item = QStandardItem("B")
                item.setTextAlignment(Qt.AlignCenter)
                stdModel.setItem(1, 4, item)

                item = QStandardItem("C")
                item.setTextAlignment(Qt.AlignCenter)
                stdModel.setItem(1, 5, item)

                item = QStandardItem("D")
                item.setTextAlignment(Qt.AlignCenter)
                stdModel.setItem(1, 6, item)

                item = QStandardItem("DL")
                item.setTextAlignment(Qt.AlignCenter)
                stdModel.setItem(1, 7, item)
            else:
                item = QStandardItem("A")
                item.setTextAlignment(Qt.AlignCenter)
                stdModel.setItem(1, 3, item)

                item = QStandardItem("B")
                item.setTextAlignment(Qt.AlignCenter)
                stdModel.setItem(1, 4, item)

                item = QStandardItem("C")
                item.setTextAlignment(Qt.AlignCenter)
                stdModel.setItem(1, 5, item)

                item = QStandardItem("D")
                item.setTextAlignment(Qt.AlignCenter)
                stdModel.setItem(1, 6, item)

                item = QStandardItem("E")
                item.setTextAlignment(Qt.AlignCenter)
                stdModel.setItem(1, 7, item)
        elif data["CatOfAcftCount"][0] == 6:
            item = QStandardItem("A")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 3, item)

            item = QStandardItem("B")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 4, item)

            item = QStandardItem("C")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 5, item)

            item = QStandardItem("D")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 6, item)

            item = QStandardItem("DL")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 7, item)

            item = QStandardItem("E")
            item.setTextAlignment(Qt.AlignCenter)
            stdModel.setItem(1, 8, item)



        # item = QStandardItem("DME MX NM")
        # item.setTextAlignment(Qt.AlignCenter)
        # stdModel.setItem(1, 6, item)

        item = QStandardItem("DME SSA")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(1, data["CatOfAcftCount"][0] + 3, item)

        item = QStandardItem("6")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(1, data["CatOfAcftCount"][0] + 5, item)

        item = QStandardItem("5")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(1, data["CatOfAcftCount"][0] + 6, item)

        item = QStandardItem("4")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(1, data["CatOfAcftCount"][0] + 7, item)

        item = QStandardItem("3")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(1, data["CatOfAcftCount"][0] + 8, item)

        item = QStandardItem("2")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(1, data["CatOfAcftCount"][0] + 9, item)

        item = QStandardItem("1")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(1, data["CatOfAcftCount"][0] + 10, item)


        item = QStandardItem("A L T(HGT)")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(2, data["CatOfAcftCount"][0] + 3, item)

        item = QStandardItem("G S")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(3, data["CatOfAcftCount"][0] + 3, item)

        item = QStandardItem("kt")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(3, data["CatOfAcftCount"][0] + 5, item)

        item = QStandardItem("80")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(3, data["CatOfAcftCount"][0] + 6, item)

        item = QStandardItem("100")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(3, data["CatOfAcftCount"][0] + 7, item)

        item = QStandardItem("120")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(3, data["CatOfAcftCount"][0] + 8, item)

        item = QStandardItem("140")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(3, data["CatOfAcftCount"][0] + 9, item)

        item = QStandardItem("160")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(3, data["CatOfAcftCount"][0] + 10, item)

        item = QStandardItem("180")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(3, data["CatOfAcftCount"][0] + 11, item)

        item = QStandardItem("T i me")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(4, data["CatOfAcftCount"][0] + 3, item)

        item = QStandardItem("mi n:s")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(4, data["CatOfAcftCount"][0] + 5, item)

        item = QStandardItem("Rate  Of  D e s c e n t")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(5, data["CatOfAcftCount"][0] + 3, item)

        item = QStandardItem("ft/mi n")
        item.setTextAlignment(Qt.AlignCenter)
        stdModel.setItem(5, data["CatOfAcftCount"][0] + 5, item)

        tblView.setModel(stdModel)
        for i in range(7):
            tblView.setRowHeight(i, int(data["TableHeight"] / 7))
        for j in range(12 + data["CatOfAcftCount"][0]):
            tblView.setColumnWidth(j, int(data["TableWidth"] / float(12 + data["CatOfAcftCount"][0])))
        # tblView.setColumnWidth(0, 25)
        # tblView.setColumnWidth(6, 20)
        tblView.setSpan(0, 0, 1, data["CatOfAcftCount"][0] + 3)
        tblView.setSpan(1, 0, 1, 3)
        if data["Template"][0] >= 0 and data["Template"][0] <= 4:
            tblView.setSpan(2, 0, 1, 3)
            tblView.setSpan(2, 3, 1, data["CatOfAcftCount"][0])
            tblView.setSpan(3, 0, 1, data["CatOfAcftCount"][0] + 3)
            tblView.setSpan(4, 0, 1, 3)
            tblView.setSpan(5, 0, 1, 3)
            tblView.setSpan(6, 0, 1, 3)
        else:
            tblView.setSpan(2, 0, 1, 3)
            tblView.setSpan(3, 0, 1, 3)
            tblView.setSpan(4, 0, 1, 3)
            tblView.setSpan(5, 0, 1, 3)
            tblView.setSpan(6, 0, 1, 3)

        # tblView.setSpan(data["StraightCount"] + 2, 0, 1, 3)

        tblView.setSpan(0, data["CatOfAcftCount"][0] + 3, 1, 9)
        # tblView.setSpan(1, data["CatOfAcftCount"][0] + 4, 1, 5)
        # tblView.setSpan(1, data["CatOfAcftCount"][0] + 9, 1, 3)
        # tblView.setSpan(2, data["CatOfAcftCount"][0] + 5, 1, 4)
        # tblView.setSpan(2, data["CatOfAcftCount"][0] + 9, 1, 3)

        tblView.setSpan(1, data["CatOfAcftCount"][0] + 3, 1, 2)
        tblView.setSpan(2, data["CatOfAcftCount"][0] + 3, 1, 2)
        tblView.setSpan(3, data["CatOfAcftCount"][0] + 3, 1, 2)
        tblView.setSpan(4, data["CatOfAcftCount"][0] + 3, 1, 2)
        tblView.setSpan(5, data["CatOfAcftCount"][0] + 3, 1, 2)
        tblView.setSpan(6, data["CatOfAcftCount"][0] + 3, 1, 2)
    def stdModel_itemChanged(self, item):
        if item.row() != 1 and item.row() != 3:
            return
        self.calcTimeRate()
        self.calcALT()
    def calcALT(self):
        thrAlt = Unit.ConvertFeetToMeter(self.data["ThrAltitude"])
        rdhAlt = Unit.ConvertFeetToMeter(self.data["RDHAltitude"])
        gradient = self.data["DescentGradient"]
        dx = self.data["dX"]

        for i in range(7):
            item = self.stdModel.item(1, self.data["CatOfAcftCount"][0] + 5 + i)
            val = 0.0
            try:
                val = float(item.text())
            except:
                continue
            dist = val * 1852
            valueHgt = Unit.ConvertFeetToMeter((dist - dx) * math.tan(Unit.ConvertDegToRad(gradient)))
            valueAlt = valueHgt + thrAlt + rdhAlt
            if valueAlt > int(valueAlt):
                valueAlt = int(valueAlt) + 1
            if valueHgt > int(valueHgt):
                valueHgt = int(valueHgt) + 1

            itemTemp = QStandardItem(str(valueAlt) + "\n(" + str(valueHgt) + ")")
            itemTemp.setTextAlignment(Qt.AlignCenter)
            self.stdModel.setItem(2, self.data["CatOfAcftCount"][0] + 5 + i, itemTemp)

    def calcTimeRate(self):
        for i in range(6):
            item = self.stdModel.item(3, self.data["CatOfAcftCount"][0] + 6 + i)
            val = 0.0
            try:
                val = float(item.text())
            except:
                continue
            time = (3600 * self.data["Distance"]) / val
            minute = int(time / 60)
            second = int(time % 60)

            timeStr = str(minute) + " : " + str(second)
            if second == 0:
                timeStr = str(minute) + " : " + "00"
            elif second < 10:
                timeStr = str(minute) + " : 0" + str(second)
            itemTemp = QStandardItem(timeStr)
            itemTemp.setTextAlignment(Qt.AlignCenter)
            self.stdModel.setItem(4, self.data["CatOfAcftCount"][0] + 6 + i, itemTemp)


            rate = int((val * 6076.1 * (AngleGradientSlope(self.data["DescentGradient"]).Percent / float(100))) / float(60))
            itemTemp = QStandardItem(str(rate))
            itemTemp.setTextAlignment(Qt.AlignCenter)
            self.stdModel.setItem(5, self.data["CatOfAcftCount"][0] + 6 + i, itemTemp)



