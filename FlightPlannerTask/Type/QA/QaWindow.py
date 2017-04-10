# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_self.ui'
#
# Created: Thu Jun 23 17:00:03 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.StandardItemModel import StandardItemModelQA
from FlightPlanner.Panels.TreeView import TreeView, TreeNode
from FlightPlanner.types import QARecordType, QAExportType, QAColorCode, QADefaultView, QASessionType,\
    QASnapshotFormat
from FlightPlanner.messages import Messages
from FlightPlanner.Captions import Captions
from FlightPlanner.Confirmations import Confirmations
from Type.String import String
from Type.Path import Path
from Type.switch import switch
from Type.Extensions import Extensions
from QADocument import QADocument
from QAComment import QAComment
from QASession import QARecord, QASession
from QAAttached import QAAttached
from QAReportEntry import QAReportEntry
from QASnapshot import QASnapshot
from QA0 import QA0
import os, sys
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class QaWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.parent = parent
        self.currentDir = os.getcwdu()
        self.setObjectName(_fromUtf8("QaWindow"))
        self.resize(456, 447)
        self.setAcceptDrops(True)
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tabControl = QtGui.QTabWidget(self.frame)
        self.tabControl.setMaximumSize(QtCore.QSize(200, 16777215))
        self.tabControl.setObjectName(_fromUtf8("tabControl"))
        self.tabQA = QtGui.QWidget()
        self.tabQA.setWhatsThis(_fromUtf8(""))
        self.tabQA.setObjectName(_fromUtf8("tabQA"))
        self.vlTabQA = QtGui.QVBoxLayout(self.tabQA)
        self.vlTabQA.setContentsMargins(-1, -1, -1, 6)
        self.vlTabQA.setObjectName(_fromUtf8("vlTabQA"))


        self.treeView = TreeView(self.tabQA)
        # self.treeView.setObjectName(_fromUtf8("treeView"))
        self.vlTabQA.addWidget(self.treeView)
        self.tabControl.addTab(self.tabQA, _fromUtf8(""))
        self.tabReport = QtGui.QWidget()
        self.tabReport.setObjectName(_fromUtf8("tabReport"))

        # self.treeViewModel = StandardItemModelQA()
        # self.treeView.setModel(self.treeViewModel)

        self.hlTabReport = QtGui.QHBoxLayout(self.tabReport)
        self.hlTabReport.setContentsMargins(-1, -1, -1, 6)
        self.hlTabReport.setObjectName(_fromUtf8("hlTabReport"))
        self.treeViewReport = TreeView(self.tabReport)
        # self.treeViewReport.setObjectName(_fromUtf8("treeViewReport"))

        # self.treeViewReportModel = StandardItemModelQA()
        # self.treeViewReport.setModel(self.treeViewReportModel)

        self.hlTabReport.addWidget(self.treeViewReport)
        self.tabControl.addTab(self.tabReport, _fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.tabControl)
        self.pnlEntry = QtGui.QFrame(self.frame)
        self.pnlEntry.setFrameShape(QtGui.QFrame.StyledPanel)
        self.pnlEntry.setFrameShadow(QtGui.QFrame.Raised)
        self.pnlEntry.setObjectName(_fromUtf8("pnlEntry"))
        self.vlPnlEntry = QtGui.QVBoxLayout(self.pnlEntry)
        self.vlPnlEntry.setContentsMargins(-1, 0, -1, -1)
        self.vlPnlEntry.setObjectName(_fromUtf8("vlPnlEntry"))
        self.lblDateTime = QtGui.QLabel(self.pnlEntry)
        self.lblDateTime.setObjectName(_fromUtf8("lblDateTime"))
        self.vlPnlEntry.addWidget(self.lblDateTime)
        self.pnlSnapshot = QtGui.QFrame(self.pnlEntry)
        self.pnlSnapshot.setMinimumSize(QtCore.QSize(0, 0))
        self.pnlSnapshot.setFrameShape(QtGui.QFrame.StyledPanel)
        self.pnlSnapshot.setFrameShadow(QtGui.QFrame.Raised)
        self.pnlSnapshot.setObjectName(_fromUtf8("pnlSnapshot"))
        self.hlPnlSnapshot = QtGui.QHBoxLayout(self.pnlSnapshot)
        self.hlPnlSnapshot.setMargin(0)
        self.hlPnlSnapshot.setObjectName(_fromUtf8("hlPnlSnapshot"))
        self.picSnapshot = QtGui.QGraphicsView(self.pnlSnapshot)
        self.picSnapshot.setObjectName(_fromUtf8("picSnapshot"))
        self.hlPnlSnapshot.addWidget(self.picSnapshot)
        self.vlPnlEntry.addWidget(self.pnlSnapshot)
        self.richBox = QtGui.QTextEdit(self.pnlEntry)
        self.richBox.setObjectName(_fromUtf8("richBox"))
        self.vlPnlEntry.addWidget(self.richBox)
        self.horizontalLayout_2.addWidget(self.pnlEntry)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frame_3 = QtGui.QFrame(self.frame_2)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(9)
        self.horizontalLayout_3.setContentsMargins(9, 0, 9, 0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lblHeading = QtGui.QLabel(self.frame_3)
        self.lblHeading.setMinimumSize(QtCore.QSize(50, 0))
        self.lblHeading.setObjectName(_fromUtf8("lblHeading"))
        self.horizontalLayout_3.addWidget(self.lblHeading)
        self.txtHeading = QtGui.QLineEdit(self.frame_3)
        self.txtHeading.setObjectName(_fromUtf8("txtHeading"))
        self.horizontalLayout_3.addWidget(self.txtHeading)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.frame_4 = QtGui.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setSpacing(9)
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.txtComment = QtGui.QLineEdit(self.frame_4)
        self.txtComment.setObjectName(_fromUtf8("txtComment"))
        self.horizontalLayout_4.addWidget(self.txtComment)
        self.btnSubmit = QtGui.QPushButton(self.frame_4)
        self.btnSubmit.setMinimumSize(QtCore.QSize(100, 0))
        self.btnSubmit.setObjectName(_fromUtf8("btnSubmit"))
        self.horizontalLayout_4.addWidget(self.btnSubmit)
        self.verticalLayout_2.addWidget(self.frame_4)
        self.verticalLayout.addWidget(self.frame_2)
        self.setCentralWidget(self.centralwidget)
        self.menuStrip = QtGui.QMenuBar(self)
        self.menuStrip.setGeometry(QtCore.QRect(0, 0, 456, 21))
        self.menuStrip.setObjectName(_fromUtf8("menuStrip"))
        self.mniFile = QtGui.QMenu(self.menuStrip)
        self.mniFile.setObjectName(_fromUtf8("mniFile"))
        self.mniEdit = QtGui.QMenu(self.menuStrip)
        self.mniEdit.setObjectName(_fromUtf8("mniEdit"))
        self.setMenuBar(self.menuStrip)
        self.statusStrip = QtGui.QStatusBar(self)
        self.statusStrip.setObjectName(_fromUtf8("statusStrip"))
        self.setStatusBar(self.statusStrip)
        self.toolStrip = QtGui.QToolBar(self)
        self.toolStrip.setMinimumSize(QtCore.QSize(0, 23))
        self.toolStrip.setObjectName(_fromUtf8("toolStrip"))
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolStrip)
        self.insertToolBarBreak(self.toolStrip)
        self.mniFileExportQA = QtGui.QAction(self)
        self.mniFileExportQA.setObjectName(_fromUtf8("mniFileExportQA"))
        self.mniFileExportReport = QtGui.QAction(self)
        self.mniFileExportReport.setObjectName(_fromUtf8("mniFileExportReport"))
        self.mniFileClose = QtGui.QAction(self)
        self.mniFileClose.setObjectName(_fromUtf8("mniFileClose"))
        self.mniEditCopy = QtGui.QAction(self)
        self.mniEditCopy.setObjectName(_fromUtf8("mniEditCopy"))
        self.mniEditDelete = QtGui.QAction(self)
        self.mniEditDelete.setObjectName(_fromUtf8("mniEditDelete"))
        self.mniEditExportWord = QtGui.QAction(self)
        self.mniEditExportWord.setObjectName(_fromUtf8("mniEditExportWord"))
        self.mniEditComment = QtGui.QAction(self)
        self.mniEditComment.setObjectName(_fromUtf8("mniEditComment"))
        self.mniEditExportSST = QtGui.QAction(self)
        self.mniEditExportSST.setObjectName(_fromUtf8("mniEditExportSST"))
        self.mniEditRestoreView = QtGui.QAction(self)
        self.mniEditRestoreView.setObjectName(_fromUtf8("mniEditRestoreView"))
        self.mniFile.addAction(self.mniFileExportQA)
        self.mniFile.addAction(self.mniFileExportReport)
        self.mniFile.addSeparator()
        self.mniFile.addAction(self.mniFileClose)
        self.mniEdit.addAction(self.mniEditCopy)
        self.mniEdit.addAction(self.mniEditDelete)
        self.mniEdit.addSeparator()
        self.mniEdit.addAction(self.mniEditExportWord)
        self.mniEdit.addAction(self.mniEditComment)
        self.mniEdit.addAction(self.mniEditExportSST)
        self.mniEdit.addAction(self.mniEditRestoreView)
        self.menuStrip.addAction(self.mniFile.menuAction())
        self.menuStrip.addAction(self.mniEdit.menuAction())

        self.lblFile = QtGui.QLabel(self.statusStrip)
        self.statusStrip.addWidget(self.lblFile)

        self.retranslateUi()
        self.tabControl.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.toolBarCreate()
        self.createContextMenuOfTreeView()
        self.signalSlotConnect()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.timeOutEvent)
        self.timer.start()

        #init Variables
        self.NO_INDEX = -1999
        self.activeDocument = QADocument()
        self.size = None
        self.location = None
        self.splitterDistance = 0
        self.previousState = self.windowState()
        self.boundsSpecified = None
        self.loaded = True
        self.shown = False
        self.boldFont = None
        self.labelEditInProgress = False
        self.dragNodeNewIndex = -1
        self.dragTargetParentNode = None
        self.ImageList = dict()

        self.clipboard = QtGui.QApplication.clipboard()
    def resizeEvent(self, *args, **kwargs):
        if (self.loaded and self.windowState() != QtCore.Qt.WindowMinimized):
            self.previousState = self.windowState()
    def timeOutEvent(self):
        self.method_0()
        self.timer.stop()
        self.timer.start()
    
    def retranslateUi(self):
        self.setWindowTitle(_translate("self", "Quality Assurance Assistant", None))
        self.tabQA.setToolTip(_translate("self", "QA", None))
        self.tabControl.setTabText(self.tabControl.indexOf(self.tabQA), _translate("self", "QA", None))
        self.tabReport.setToolTip(_translate("self", "Report", None))
        self.tabControl.setTabText(self.tabControl.indexOf(self.tabReport), _translate("self", "Report", None))
        self.lblDateTime.setText(_translate("self", "TextLabel", None))
        self.lblHeading.setText(_translate("self", "Title:", None))
        self.btnSubmit.setText(_translate("self", "Submit", None))
        self.mniFile.setTitle(_translate("self", "File", None))
        self.mniEdit.setTitle(_translate("self", "Edit", None))
        self.toolStrip.setWindowTitle(_translate("self", "toolBar", None))
        self.mniFileExportQA.setText(_translate("self", "Export as QA Document", None))
        self.mniFileExportReport.setText(_translate("self", "Export as Report Document ", None))
        self.mniFileClose.setText(_translate("self", "Close", None))
        self.mniEditCopy.setText(_translate("self", "Copy", None))
        self.mniEditDelete.setText(_translate("self", "Delete", None))
        self.mniEditExportWord.setText(_translate("self", "Export to MS Word", None))
        self.mniEditComment.setText(_translate("self", "Edit Comment...", None))
        self.mniEditExportSST.setText(_translate("self", "Export to File...", None))
    def createContextMenuOfTreeView(self):
        self.mnuEntries = QtGui.QMenu(self.treeView)
        self.mniFlags = self.mnuEntries.addMenu("Flag")
        self.mniFlagNone = self.mniFlags.addAction("None")
        self.mniFlagRed = self.mniFlags.addAction("Red")
        self.mniFlagBlue = self.mniFlags.addAction("Blue")
        self.mniFlagMagenta = self.mniFlags.addAction("Magenta")
        self.mniFlagGreen = self.mniFlags.addAction("Green")
        self.mniFlagCyan = self.mniFlags.addAction("Cyan")
        self.mniFlagYellow = self.mniFlags.addAction("Yellow")
        self.mniQaSep1 = self.mnuEntries.addSeparator()
        self.mniQaCopy = self.mnuEntries.addAction("Copy")
        self.mniQaDelete = self.mnuEntries.addAction("Delete")
        self.mniQaSep2 = self.mnuEntries.addSeparator()
        self.mniQaExportWord = self.mnuEntries.addAction("Export to MS Word")
        self.mniQaComment = self.mnuEntries.addAction("Edit Comment...")
        self.mniQaExportSST = self.mnuEntries.addAction("Export to File...")
        self.mniQaRestoreView = self.mnuEntries.addAction("Restore View")
        self.mniQaSep3 = self.mnuEntries.addSeparator()
        self.mniCopyToReport = self.mnuEntries.addAction("Copy entry into the report view")

        self.mnuFolders = QtGui.QMenu(self.treeView)
        self.mniNewFolder = self.mnuFolders.addAction("New Folder")

        self.mnuRichText = QtGui.QMenu(self.richBox)
        self.mniRichTextCopy = self.mnuRichText.addAction("&Copy")

        self.mniFlagNone.triggered.connect(self.mniFlagNone_Click)
        self.mniFlagRed.triggered.connect(self.mniFlagRed_Click)
        self.mniFlagBlue.triggered.connect(self.mniFlagBlue_Click)
        self.mniFlagMagenta.triggered.connect(self.mniFlagMagenta_Click)
        self.mniFlagYellow.triggered.connect(self.mniFlagYellow0_Click)
        self.mniFlagCyan.triggered.connect(self.mniFlagCyan_Click)
        self.mniFlagGreen.triggered.connect(self.mniFlagGreen_Click)

        self.mniQaCopy.triggered.connect(self.mniQaCopy_Click)
        self.mniQaDelete.triggered.connect(self.mniQaDelete_Click)

        self.mniQaExportWord.triggered.connect(self.mniQaExportWord_Click)
        self.mniQaExportSST.triggered.connect(self.mniQaExportSST_Click)
        self.mniQaComment.triggered.connect(self.mniQaComment_Click)
        self.mniQaRestoreView.triggered.connect(self.mniQaRestoreView_Click)

        self.mniCopyToReport.triggered.connect(self.mniCopyToReport_Click)

        self.mniNewFolder.triggered.connect(self.mniNewFolder_Click)
        self.mnuRichText.aboutToShow.connect(self.mnuRichText_Opening)
        self.mnuEntries.aboutToShow.connect(self.mnuEntries_Opening)
        self.mniRichTextCopy.triggered.connect(self.mniRichTextCopy_Click)
    def mnuEntries_Opening(self):
        flag = False;
        flag1 = False;
        self.mniFlags.setVisible(self.isFlagAvailable);
        self.mniQaCopy.setVisible(self.isCopyAvailable);
        self.mniQaDelete.setVisible(self.isDeleteAvailable);
        self.mniQaExportWord.setVisible(self.isExportToWordAvailable);
        self.mniQaComment.setVisible(self.isEditCommentAvailable);
        self.mniQaExportSST.setVisible(self.isSnapshotActionAvailable);
        self.mniQaRestoreView.setVisible(self.isSnapshotActionAvailable);
        self.mniCopyToReport.setVisible(self.isCopyEntryToReportAvailable);
        flag2 = self.isFlagAvailable;
        flag3 = True if(self.isCopyAvailable) else self.isDeleteAvailable;
        flag4 = True if(self.isExportToWordAvailable or self.isEditCommentAvailable) else self.isSnapshotActionAvailable;
        flag5 = self.isCopyEntryToReportAvailable;
        toolStripSeparator = self.mniQaSep1;
        if (not flag2):
            flag = False;
        else:
            flag = True if(flag3 or flag4) else flag5
        toolStripSeparator.setVisible(flag);
        toolStripSeparator1 = self.mniQaSep2;
        if (not flag3):
            flag1 = False;
        else:
            flag1 = True if(flag4) else flag5;
        toolStripSeparator1.setVisible(flag1);
        self.mniQaSep3.setVisible(False if(not flag4) else flag5);
    def mniFlagYellow0_Click(self):
        self.mniFlagYellow_Click()
    def mniFlagBlue_Click(self):
        self.mniFlagYellow_Click(self.mniFlagBlue)
    def mniFlagNone_Click(self):
        self.mniFlagYellow_Click(self.mniFlagNone)
    def mniFlagRed_Click(self):
        self.mniFlagYellow_Click(self.mniFlagRed)
    def mniFlagMagenta_Click(self):
        self.mniFlagYellow_Click(self.mniFlagMagenta)
    def mniFlagCyan_Click(self):
        self.mniFlagYellow_Click(self.mniFlagCyan)
    def mniFlagGreen_Click(self):
        self.mniFlagYellow_Click(self.mniFlagGreen)
    def signalSlotConnect(self):
        self.btnSubmit.clicked.connect(self.btnSubmit_Click)

        self.mniFileExportQA.triggered.connect(self.btnExportQA_Click)
        self.mniFileExportReport.triggered.connect(self.btnExportReport_Click)
        self.mniFileClose.triggered.connect(self.mniFileClose_Click)
        self.mniEditCopy.triggered.connect(self.mniQaCopy_Click)
        self.mniEditDelete.triggered.connect(self.mniQaDelete_Click)
        self.mniEditExportWord.triggered.connect(self.mniQaExportWord_Click)
        self.mniEditComment.triggered.connect(self.mniQaComment_Click)
        self.mniEditExportSST.triggered.connect(self.mniQaExportSST_Click)
        self.mniEditRestoreView.triggered.connect(self.mniQaRestoreView_Click)

        self.btnExportQA.triggered.connect(self.btnExportQA_Click)
        self.btnExportReport.triggered.connect(self.btnExportReport_Click)
        self.btnCopy.triggered.connect(self.mniQaCopy_Click)
        self.btnDelete.triggered.connect(self.mniQaDelete_Click)
        self.btnExportWord.triggered.connect(self.mniQaExportWord_Click)
        self.btnEditComment.triggered.connect(self.mniQaComment_Click)
        self.btnExportSST.triggered.connect(self.mniQaExportSST_Click)
        self.btnRestoreView.triggered.connect(self.mniQaRestoreView_Click)

        self.tabControl.currentChanged.connect(self.tabControl_SelectedIndexChanged)
        # self.treeView.clicked.connect(self.treeView_NodeMouseClick)
        # self.connect( self.treeViewReport, QtCore.SIGNAL( "mousePressEvent( QMouseEvent )" ), self, QtCore.SLOT( "treeViewReport_MousePressEvent(QMouseEvent)" ) )
        # self.connect( self.treeViewReport, QtCore.SIGNAL( "mouseReleaseEvent( QMouseEvent )" ), self, QtCore.SLOT( "treeViewReport_MouseReleaseEvent(QMouseEvent)" ) )
        # self.connect( self.treeView, QtCore.SIGNAL( "mousePressEvent( QMouseEvent )" ), self, QtCore.SLOT( "treeView_MousePressEvent(QMouseEvent)" ) )

        self.treeViewReport.clicked.connect(self.treeViewReport_NodeMouseClick)
    def treeView_MousePressEvent(self, e):
        if ( e.buttons() != QtCore.Qt.RightButton ):
            # self.treeView.SelectedNode = e.Node
            self.mnuEntries.exec_( self.treeView.treeView.mapToGlobal(e.pos() ))
    def treeViewReport_MouseReleaseEvent(self, e):
        if (len(self.treeView.Nodes) > 0 and e.buttons() != QtCore.Qt.RightButton and self.treeViewReport.HitTest(e.Location).Node == None):
            self.mnuFolders.exec_( self.treeViewReport.mapToGlobal(e.pos() ))
    def treeViewReport_MousePressEvent(self, e):
        if ( e.buttons() != QtCore.Qt.RightButton ):
            # self.treeView.SelectedNode = e.Node
            self.mnuEntries.exec_( self.treeViewReport.mapToGlobal(e.pos() ))
    def btnSubmit_Click(self):
        self.timer.stop()
        if (self.activeDocument == None):
            return
        if (self.lastSessionNode == None):
            return
        qAComment = QAComment()
        qAComment.Heading = self.txtHeading.text()
        qAComment.Text = self.txtComment.text()
        self.method_25(qAComment)
        self.txtHeading.setText("")
        self.txtComment.setText("")
        self.timer.start()
    def mniRichTextCopy_Click(self):
        self.timer.stop()
        self.richBox.copy()
        self.timer.start()
    def mnuRichText_Opening(self):
        self.timer.stop()
        flag = False
        flag1 = False
        self.mniFlags.setVisible(self.isFlagAvailable)
        self.mniQaCopy.setVisible(self.isCopyAvailable)
        self.mniQaDelete.setVisible(self.isDeleteAvailable)
        self.mniQaExportWord.setVisible(self.isExportToWordAvailable)
        self.mniQaComment.setVisible(self.isEditCommentAvailable)
        self.mniQaExportSST.setVisible(self.isSnapshotActionAvailable)
        self.mniQaRestoreView.setVisible(self.isSnapshotActionAvailable)
        self.mniCopyToReport.setVisible(self.isCopyEntryToReportAvailable)
        flag2 = self.isFlagAvailable
        flag3 = True if(self.isCopyAvailable) else self.isDeleteAvailable
        flag4 = True if(self.isExportToWordAvailable or self.isEditCommentAvailable) else self.isSnapshotActionAvailable
        flag5 = self.isCopyEntryToReportAvailable
        toolStripSeparator = self.mniQaSep1
        if (not flag2):
            flag = False
        else:
            flag = True if(flag3 or flag4) else flag5
        toolStripSeparator.setVisible(flag)
        toolStripSeparator1 = self.mniQaSep2
        if (not flag3):
            flag1 = False
        else:
            flag1 = True if(flag4) else flag5
        toolStripSeparator1.setVisible(flag1)
        self.mniQaSep3.setVisible(False if(not flag4) else flag5)
        self.timer.start()
    def mniNewFolder_Click(self):
        self.timer.stop()
        qAReportEntry = QAReportEntry()
        self.activeDocument.ReportEntries.append(qAReportEntry)
        self.method_5(None, qAReportEntry)
        self.treeViewReport.SelectedNode = self.treeViewReport.Nodes[self.treeViewReport.Nodes.Count - 1]
        self.treeViewReport.SelectedNode.BeginEdit()
        self.activeDocument.method_2(self)
        self.timer.start()
    def mniCopyToReport_Click(self):
        self.timer.stop()
        selectedNode = self.treeView.SelectedNode
        if (selectedNode == None):
            return
        tag = selectedNode.Tag# as QARecord
        tag._class_ = QARecord
        if (tag == None):
            return
        treeNode = self.method_13(tag)
        if (treeNode != None):
            self.treeViewReport.SelectedNode = treeNode
            return
        treeNode1 = None
        qAReportEntry = QAReportEntry()
        qAReportEntry.Value = tag
        self.activeDocument.ReportEntries.append(qAReportEntry)
        self.method_5(treeNode1, qAReportEntry)
        self.treeViewReport.SelectedNode = self.treeViewReport.Nodes[len(self.treeViewReport.Nodes) - 1]
        self.activeDocument.method_2(self)
        self.timer.start()
    def mniFlagYellow_Click(self, sender):
        self.timer.stop()
        selectedNode = self.treeViewReport.SelectedNode
        if (selectedNode == None):
            return
        qAColorCode = QAColorCode.None
        if (sender == self.mniFlagBlue):
            qAColorCode = QAColorCode.Blue
        elif (sender == self.mniFlagRed):
            qAColorCode = QAColorCode.Red
        elif (sender == self.mniFlagGreen):
            qAColorCode = QAColorCode.Green
        elif (sender == self.mniFlagMagenta):
            qAColorCode = QAColorCode.Magenta
        elif (sender == self.mniFlagCyan):
            qAColorCode = QAColorCode.Cyan
        elif (sender == self.mniFlagYellow):
            qAColorCode = QAColorCode.Yellow
        tag = selectedNode.Tag #as QAReportEntry
        tag._class_ = QAReportEntry
        if (tag == None):
            return
        value = tag.Value
        if (value == None):
            return
        tag.ColorCode = qAColorCode
        str0 = self.method_18(value.Type, qAColorCode)
        selectedNode.ImageKey = str0
        # selectedNode.SelectedImageKey = str0
        for node in selectedNode.Nodes:
            node.ImageKey = str0
            # node.SelectedImageKey = str0
        self.method_19()
        self.activeDocument.method_2(self)
        self.timer.start()
    def treeViewReport_NodeMouseClick(self, index):
        self.treeViewReportModel.selectedIndex = index
        self.timer.stop()
        self.timer.start()
    def treeView_NodeMouseClick(self, index):
        self.treeViewModel.selectedIndex = index
        self.timer.stop()
        self.timer.start()
    def tabControl_SelectedIndexChanged(self):
        self.timer.stop()
        if (len(self.treeView.Nodes) > 0):
            self.method_7()
            return
        self.method_22(None, True)
        self.timer.start()
    def mniQaRestoreView_Click(self):
        self.timer.stop()
        treeNode = self.treeView.SelectedNode if(self.tabControl.currentIndex() == 0) else self.treeViewReport.SelectedNode
        if (treeNode == None):
            return
        tag = treeNode.Tag# as QASnapshot
        if (tag == None):
            qAReportEntry = treeNode.Tag# as QAReportEntry
            if (qAReportEntry == None):
                return
            tag = qAReportEntry.Value# as QASnapshot
            if (tag == None):
                return
        QA0.smethod_5(self, tag)
        self.timer.start()
    def mniQaExportSST_Click(self):
        self.timer.stop()
        treeNode = self.treeView.SelectedNode if(self.tabControl.currentIndex() == 0) else self.treeViewReport.SelectedNode
        if (treeNode == None):
            return;
        tag = treeNode.Tag# as QASnapshot;
        tag._class_ = QASnapshot
        if (tag == None):
            qAReportEntry = treeNode.Tag# as QAReportEntry;
            qAReportEntry._class_ = QAReportEntry
            if (qAReportEntry == None):
                return;
            tag = qAReportEntry.Value# as QASnapshot;
            tag._class_ = QASnapshot
            if (tag == None):
                return;
        filePathDir = ""
        # self.sfd.Filter = FileDialogFilters.SAVE_SNAPSHOT;
        if (tag.ImageFormatType == QASnapshotFormat.Gif):
            filePathDir = QtGui.QFileDialog.getSaveFileName(self, "Save Data",QtCore.QCoreApplication.applicationDirPath (),"GIF Image File (*.gif)")
            if filePathDir == "":
                return
            # self.sfd.DefaultExt = "png";
            # self.sfd.FilterIndex = 0;
        elif (tag.ImageFormatType == QASnapshotFormat.Png):
            filePathDir = QtGui.QFileDialog.getSaveFileName(self, "Save Data",QtCore.QCoreApplication.applicationDirPath (),"Portable Network Graphics (*.png)")
            if filePathDir == "":
                return
            # self.sfd.DefaultExt = "png";
            # self.sfd.FilterIndex = 1;
        elif (tag.ImageFormatType == QASnapshotFormat.Jpeg):
            filePathDir = QtGui.QFileDialog.getSaveFileName(self, "Save Data",QtCore.QCoreApplication.applicationDirPath (),"JPEG Image File (*.jpg, *.jpeg)|*.jpg;*.jpeg")
            if filePathDir == "":
                return
            # self.sfd.DefaultExt = "jpg";
            # self.sfd.FilterIndex = 2;
        # self.sfd.FileName = "";
        try:
            # if (self.sfd.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            # {
            #     using (Image image = tag.Image)
            #     {
            image = tag.Image
            filePathDir = String.Str2QString(filePathDir)
            image.save(filePathDir)
            # if (filePathDir.right(4) == ".gif"):
            #     image.Save(filePathDir, ImageFormat.Gif);
            # elif (filePathDir.right(4) == ".png"):
            #     image.Save(self.sfd.FileName, ImageFormat.Png);
            # elif (filePathDir.right(4) == ".jpg" or filePathDir.right(5) == ".jpeg"):
            #     image.Save(self.sfd.FileName, ImageHelper.smethod_2(ImageFormat.Jpeg), ImageHelper.smethod_3(QA.JpegQuality));
            # elif (filePathDir.right(4) == ".bmp"):
            #     image.Save(self.sfd.FileName, ImageFormat.Bmp);
        finally:
            pass
        self.timer.start()
    def mniQaComment_Click(self):
        self.timer.stop()
        treeNode = self.treeView.SelectedNode if(self.tabControl.currentIndex() == 0) else self.treeViewReport.SelectedNode
        if (treeNode == None):
            return
        tag = treeNode.Tag# as QAComment
        tag._class_ = QAComment
        if (tag == None):
            qAReportEntry = treeNode.Tag# as QAReportEntry
            qAReportEntry._class_ = QAReportEntry
            if (qAReportEntry == None):
                return
            tag = qAReportEntry.Value# as QAComment
            tag._class_ = QAComment
            if (tag == None):
                return
        text = tag.Text
        result, text = QA0.smethod_4(self, text)
        if (result):
            tag.Text = text
            self.activeDocument.method_2(self)
            self.method_7()
        self.timer.start()
    def mniQaExportWord_Click(self):
        self.timer.stop()
        treeNode = self.treeView.SelectedNode if(self.tabControl.currentIndex() == 0) else self.treeViewReport.SelectedNode
        if (treeNode == None):
            return;
        tag = treeNode.Tag# as QARecord;
        tag._class_ = QARecord
        if (tag == None):
            qAReportEntry = treeNode.Tag# as QAReportEntry;
            qAReportEntry._class_ = QAReportEntry
            if (qAReportEntry == None):
                return;
            tag = qAReportEntry.Value;
            if (tag == None):
                return;
        QA0.smethod_3(self, tag);
        self.timer.start()
    def mniQaDelete_Click(self):
        self.timer.stop()
        if (self.activeDocument == None):
            return
        if (self.lastSessionNode == None):
            return
        if (self.tabControl.currentIndex() != 0):
            selectedNode = self.treeViewReport.SelectedNode
            if (selectedNode == None):
                return
            tag = selectedNode.Tag# as QAReportEntry
            tag._class_ = QAReportEntry
            if (tag == None):
                return
            if (selectedNode.Parent != None):
                selectedNode.Parent.Tag.Children.remove(tag)
            else:
                self.activeDocument.ReportEntries.remove(tag)
            if (selectedNode.NextNode != None):
                self.treeView.SelectedNode = selectedNode.NextNode
            elif (selectedNode.PrevNode == None):
                self.treeView.SelectedNode = selectedNode.Parent
            else:
                self.treeView.SelectedNode = selectedNode.PrevNode
            if selectedNode.Parent == None:
                self.treeViewReport.RemoveNode(selectedNode.nodeIndex)
            else:
                selectedNode.Parent.RemoveChild(selectedNode.nodeIndex)
            self.method_19()
            self.activeDocument.method_2(self)
        else:
            treeNode = self.treeView.SelectedNode
            if (treeNode == None):
                return
            if (treeNode.ParentLevel == 0):
                return
            if (treeNode.ParentLevel > 1):
                treeNode = self.method_10(treeNode, 1)
            if (self.method_10(treeNode, 0) != self.lastSessionNode):
                return
            qARecord = treeNode.Tag
            if (qARecord == None):
                return
            qASession = self.lastSessionNode.Tag
            if (qASession == None):
                return
            if (QtGui.QMessageBox.warning(self, "Warning", Confirmations.DELETE_SELECTED_ENTRY, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes):
                if (treeNode.NextNode != None):
                    self.treeView.SelectedNode = treeNode.NextNode
                elif (treeNode.PrevNode == None):
                    self.treeView.SelectedNode = treeNode.Parent
                else:
                    self.treeView.SelectedNode = treeNode.PrevNode
                if treeNode.Parent == None:
                    self.treeView.RemoveNode(treeNode.nodeIndex)
                else:
                    treeNode.Parent.RemoveChild(treeNode.nodeIndex)
                # treeNode.Remove()
                qASession.Children.remove(qARecord)
                treeNode = self.method_13(qARecord)
                if (treeNode != None):
                    qAReportEntry = treeNode.Tag# as QAReportEntry
                    if (qAReportEntry == None):
                        return
                    if (treeNode.Parent != None):
                        treeNode.Parent.Tag.Children.remove(qAReportEntry)
                    else:
                        self.activeDocument.ReportEntries.remove(qAReportEntry)
                    if treeNode.Parent == None:
                        self.treeViewReport.RemoveNode(treeNode.nodeIndex)
                    else:
                        treeNode.Parent.RemoveChild(treeNode.nodeIndex)
                    # treeNode.Remove()
                self.activeDocument.method_2(self)
                return
        self.timer.start()
    def mniQaCopy_Click(self):
        self.timer.stop()
        treeNode = self.treeView.SelectedNode if(self.tabControl.currentIndex() == 0) else self.treeViewReport.SelectedNode
        if (treeNode == None):
            return
        tag = treeNode.Tag# as QARecord
        tag._class_ = QARecord
        if (tag == None):
            qAReportEntry = treeNode.Tag# as QAReportEntry
            qAReportEntry._class_ = QAReportEntry
            if (qAReportEntry == None):
                return
            tag = qAReportEntry.Value
            if (tag == None):
                return
        tag.method_11()
        self.timer.start()
    def btnExportQA_Click(self):
        self.timer.stop()
        try:
            filePathDir = QtGui.QFileDialog.getSaveFileName(self, "Save Data",QtCore.QCoreApplication.applicationDirPath (),"Web Page (*.htm *.html)|*.htm*.html")
            if filePathDir == "":
                return
            self.activeDocument.method_5(filePathDir, QAExportType.QA)
        except:
            QtGui.QMessageBox.warning(self, "Error", Messages.ERR_FAILED_TO_EXPORT_QA_DOCUMENT + sys.exc_info()[0])
        self.timer.start()
    def btnExportReport_Click(self):
        self.timer.stop()
        try:
            filePathDir = QtGui.QFileDialog.getSaveFileName(self, "Save Data",QtCore.QCoreApplication.applicationDirPath (),"Web Page (*.htm *.html)|*.htm*.html")
            if filePathDir == "":
                return
            self.activeDocument.method_6(filePathDir, self.treeViewModel.Nodes)
        except:
            QtGui.QMessageBox.warning(self, "Error", Messages.ERR_FAILED_TO_EXPORT_QA_DOCUMENT + sys.exc_info()[0])
        self.timer.start()
    def mniFileClose_Click(self):
        self.close()
        self.timer.stop()
    def toolBarCreate(self):
        self.btnExportQA = QtGui.QAction(self)
        self.btnExportQA.setIcon(QtGui.QIcon(self.currentDir + "/Resource/btnImage/btnExportQA.png"))
        self.btnExportQA.setToolTip("Export as QA document")
        self.toolStrip.addAction(self.btnExportQA)

        self.btnExportReport = QtGui.QAction(self)
        self.btnExportReport.setIcon(QtGui.QIcon(self.currentDir + "/Resource/btnImage/btnExportReport.png"))
        self.btnExportReport.setToolTip("Export as QA report")
        self.toolStrip.addAction(self.btnExportReport)

        self.toolStrip.addSeparator()

        self.btnCopy = QtGui.QAction(self)
        self.btnCopy.setIcon(QtGui.QIcon(self.currentDir + "/Resource/btnImage/btnCopy.png"))
        self.btnCopy.setToolTip("Copy the selected entry to the clipboard")
        self.toolStrip.addAction(self.btnCopy)

        self.btnDelete = QtGui.QAction(self)
        self.btnDelete.setIcon(QtGui.QIcon(self.currentDir + "/Resource/btnImage/btnDelete.png"))
        self.btnDelete.setToolTip("Delete the selected entry")
        self.toolStrip.addAction(self.btnDelete)

        self.toolStrip.addSeparator()

        self.btnExportWord = QtGui.QAction(self)
        self.btnExportWord.setIcon(QtGui.QIcon(self.currentDir + "/Resource/btnImage/btnExportWord.png"))
        self.btnExportWord.setToolTip("Export the selected entry to the active MS Word document")
        self.toolStrip.addAction(self.btnExportWord)

        self.btnEditComment = QtGui.QAction(self)
        self.btnEditComment.setIcon(QtGui.QIcon(self.currentDir + "/Resource/btnImage/btnEditComment.png"))
        self.btnEditComment.setToolTip("Edit the selected comment")
        self.toolStrip.addAction(self.btnEditComment)

        self.btnExportSST = QtGui.QAction(self)
        self.btnExportSST.setIcon(QtGui.QIcon(self.currentDir + "/Resource/btnImage/btnExportSST.png"))
        self.btnExportSST.setToolTip("Export the selected snapshot to a file")
        self.toolStrip.addAction(self.btnExportSST)

        self.btnRestoreView = QtGui.QAction(self)
        self.btnRestoreView.setIcon(QtGui.QIcon(self.currentDir + "/Resource/btnImage/btnRestoreView.png"))
        self.btnRestoreView.setToolTip("Restore view of the selected snapshot")
        self.toolStrip.addAction(self.btnRestoreView)
    def method_0(self):
        self.method_20()
    def method_2(self):
        self.treeView.Clear()
        if (self.activeDocument == None):
            return
        count = len(self.activeDocument.Sessions)
        for i in range(count):
            item = self.activeDocument.Sessions[i]
            treeNode = TreeNode()
            if (item.SessionType != QASessionType.Started):
                treeNode.Text = Captions.QA_OPENED
            else:
                treeNode.Text = Captions.QA_STARTED
            if (i == count - 1):
                treeNode1 = treeNode
                treeNode1.Text = String.Concat([treeNode1.Text, " ({0})".format(Captions.CURRENT)])
            treeNode.setIcon(QtGui.QIcon("Resource/btnImage/Session.png"))
            # treeNode.SelectedImageKey = treeNode.ImageKey
            treeNode.Tag = item
            self.treeView.Add(treeNode)
            for child in item.Children:
                self.method_4(treeNode, child)
    def method_3(self):
        self.treeViewReport.Clear()
        if (self.activeDocument == None):
            return
        for reportEntry in self.activeDocument.ReportEntries:
            self.method_5(None, reportEntry)
        self.method_19()
    def method_4(self, treeNode_0, qarecord_0):
        treeNode = TreeNode(qarecord_0.Heading)
        for case in switch (qarecord_0.Type):
            if case(QARecordType.Unknown) or case(QARecordType.Table):
                treeNode.setIcon(QtGui.QIcon("Resource/btnImage/Program.png"))
                break
            elif case(QARecordType.Attached):
                treeNode.setIcon(QtGui.QIcon("Resource/btnImage/Attachment.png"))
                break
            elif case(QARecordType.Comment):
                treeNode.setIcon(QtGui.QIcon("Resource/btnImage/Comment.png"))
                break
            elif case(QARecordType.Snapshot):
                treeNode.setIcon(QtGui.QIcon("Resource/btnImage/Snapshot.png"))
                break
            elif case(QARecordType.Session):
                treeNode.setIcon(QtGui.QIcon("Resource/btnImage/Session.png"))
                break
        # treeNode.SelectedImageKey = treeNode.ImageKey
        treeNode.Tag = qarecord_0
        treeNode_0.Add(treeNode)
        for child in qarecord_0.Children:
            self.method_4(treeNode, child)
    def method_5(self, treeNode_0, qareportEntry_0):
        treeNode = TreeNode(qareportEntry_0.Title)
        str0 = "Session_None.png"
        if (qareportEntry_0.Value != None):
            for case in switch (qareportEntry_0.Value.Type):
                if case(QARecordType.Unknown) or case(QARecordType.Table):
                    str0 = "Program_{0}.png".format(qareportEntry_0.ColorCode)
                    break
                elif case(QARecordType.Attached):
                    str0 = "Attachment_{0}.png".format(qareportEntry_0.ColorCode)
                    break
                elif case(QARecordType.Comment):
                    str0 = "Comment_{0}.png".format(qareportEntry_0.ColorCode)
                    break
                elif case(QARecordType.Snapshot):
                    str0 = "Snapshot_{0}.png".format(qareportEntry_0.ColorCode)
                    break
        treeNode.ImageKey = str0
        # treeNode.SelectedImageKey = str0
        treeNode.Tag = qareportEntry_0
        if (treeNode_0 != None):
            treeNode_0.Add(treeNode)
        else:
            self.treeViewReport.Add(treeNode)
        if (len(qareportEntry_0.Children) != 0 or qareportEntry_0.Value == None):
            for child in qareportEntry_0.Children:
                self.method_5(treeNode, child)
        else:
            for qARecord in qareportEntry_0.Value.Children:
                self.method_6(treeNode, qARecord, str0)
    def method_6(self, treeNode_0, qarecord_0, string_0):
        treeNode = TreeNode(qarecord_0.Heading)
        treeNode.ImageKey = string_0,
        # SelectedImageKey = string_0,
        treeNode.Tag = qarecord_0
        treeNode_0.Add(treeNode)
        for child in qarecord_0.Children:
            self.method_6(treeNode, child, string_0)
    def method_7(self):
        image = None
        treeNode = self.treeView.SelectedNode if(self.tabControl.currentIndex() == 0) else self.treeViewReport.SelectedNode
        if (treeNode == None):
            return
        tag = treeNode.Tag# as QARecord
        tag._class_ = QARecord
        if (tag != None):
            self.lblDateTime.setText(Extensions.smethod_19(tag.Stamp))
        else:
            qAReportEntry = treeNode.Tag# as QAReportEntry
            qAReportEntry._class_ = QAReportEntry
            if (qAReportEntry == None):
                return
            self.lblDateTime.setText(Extensions.smethod_19(qAReportEntry.Stamp))
            tag = qAReportEntry.Value
            if (tag == None):
                self.method_22(None, True)
                return
        if (tag.Type != QARecordType.Snapshot):
            self.method_22(tag.method_7(), True)
            self.method_23(None, False)
        else:
            qASnapshot = tag# as QASnapshot
            qASnapshot._class_ = QASnapshot
            if (qASnapshot != None):
                image = qASnapshot.Image
            else:
                image = None
            self.method_23(image, True)
            self.method_22(None, False)
        self.method_20()
    def method_8(self, qarecord_0):
        treeNode = None
        for node in self.treeView.Nodes:
            if (node.Tag != qarecord_0):
                continue
            treeNode = node
            return treeNode
        treeNode1 = None
        for current in self.treeView.Nodes:
            treeNode1 = self.method_9(current, qarecord_0)
            if (treeNode1 == None):
                continue
            treeNode = treeNode1
            return treeNode
        return treeNode
    def method_9(self, treeNode_0, qarecord_0):
        treeNode = None
        if (treeNode_0.Tag == qarecord_0):
            return treeNode_0
        treeNode1 = None
        for current in treeNode_0.Nodes:
            treeNode1 = self.method_9(current, qarecord_0)
            if (treeNode1 == None):
                continue
            treeNode = treeNode1
            return treeNode
        return treeNode
    def method_10(self, treeNode_0, int_0):
        if (treeNode_0 == None):
            return None
        if (treeNode_0.Parent == None):
            return None
        if (treeNode_0.ParentLevel == int_0):
            return treeNode_0.Parent
        return self.method_10(treeNode_0.Parent, int_0)
    def method_11(self, treeNode_0):
        if (treeNode_0 == None):
            return None
        tag = treeNode_0.Tag# as QAReportEntry
        tag._class_ = QAReportEntry
        if (tag != None):
            return tag
        return self.method_11(treeNode_0.Parent)
    def method_12(self, qareportEntry_0):
        treeNode = None
        if (qareportEntry_0 != None):
            for current in self.treeViewReport.Nodes:
                tag = current.Tag
                tag._class_ = QAReportEntry
                if (tag != qareportEntry_0):
                    for current1 in current.Nodes:
                        tag1 = current1.Tag
                        tag1._class_ = QAReportEntry
                        if (tag1 != qareportEntry_0):
                            continue
                        treeNode = current1
                        return treeNode
                else:
                    treeNode = current
                    return treeNode

            return treeNode
        return None
    def method_13(self, qarecord_0):
        treeNode = None
        for current in self.treeViewReport.Nodes:
            tag = current.Tag# as QAReportEntry
            tag._class_ = QAReportEntry
            if (tag == None or tag.Value != qarecord_0):
                for current1 in current.Nodes:
                    tag1 = current1.Tag# as QAReportEntry
                    tag1._class_ = QAReportEntry
                    if (tag1 == None or tag1.Value != qarecord_0):
                        continue
                    treeNode = current1
                    return treeNode
            else:
                treeNode = current
                return treeNode
        return treeNode
    def method_14(self, treeNode_0, bool_0):
        if (treeNode_0 != None):
            text = treeNode_0.Text
            treeNode_0.Text = " "
            if (not bool_0):
                font = treeNode_0.font()
                font.setBold(False)
                treeNode_0.NodeFont = font
            else:
                font = treeNode_0.font()
                font.setBold(True)
                treeNode_0.NodeFont = font
            treeNode_0.Text = text
    def method_15(self, treeNode_0, qarecordType_0):
        if (treeNode_0 == None):
            return False
        tag = treeNode_0.Tag# as QARecord
        tag._class_ = QARecord
        if (tag == None):
            qAReportEntry = treeNode_0.Tag# as QAReportEntry
            qAReportEntry._class_ = QAReportEntry
            if (qAReportEntry == None):
                return False
            tag = qAReportEntry.Value
            if (tag == None):
                return False
        return tag.Type == qarecordType_0
    def method_16(self):
        if (self.lastSessionNode == None or self.treeView.SelectedNode == None):
            return False
        return self.method_10(self.treeView.SelectedNode, 0) == self.lastSessionNode
    def method_17(self, treeNode_0):
        if (self.lastSessionNode != None):
            if (treeNode_0 == None):
                return False
            tag = treeNode_0.Tag# as QARecord
            tag._class_ = QARecord
            if (tag != None):
                return self.method_10(treeNode_0, 0) == self.lastSessionNode
            qAReportEntry = treeNode_0.Tag# as QAReportEntry
            qAReportEntry._class_ = QAReportEntry
            if (qAReportEntry == None):
                return False
            tag = qAReportEntry.Value
            if (tag == None):
                return False
            if (treeNode_0.Parent == None):
                return self.activeDocument.Sessions[len(self.activeDocument.Sessions) - 1].Children.__contains__(tag)
            tag1 = treeNode_0.Parent.Tag# as QAReportEntry
            tag1._class_ = QAReportEntry
            if (tag1 != None and tag1.Value == None):
                return self.activeDocument.Sessions[len(self.activeDocument.Sessions) - 1].Children.__contains__(tag)
        return False
    def method_18(self, qarecordType_0, qacolorCode_0):
        for case in switch (qarecordType_0):
            if case(QARecordType.Attached):
                return "attachment_{0}.png".format(qacolorCode_0)
            elif case(QARecordType.Table):
                return "program_{0}.png".format(qacolorCode_0)
            elif case(QARecordType.Comment):
                return "comment_{0}.png".format(qacolorCode_0)
            elif case(QARecordType.Snapshot):
                return "snapshot_{0}.png".format(qacolorCode_0)
            else:
                return "session_{0}.png".format(qacolorCode_0)
    def method_19(self):
        for node in self.treeViewReport.Nodes:
            tag = node.Tag #as QAReportEntry
            tag._class_ = QAReportEntry
            if (tag == None or tag.Value != None):
                continue
            str0 = self.method_18(QARecordType.Session, QAColorCode.None)
            for current in tag.Children:
                if (current.ColorCode != QAColorCode.None):
                    str0 = self.method_18(QARecordType.Session, current.ColorCode)
                    break
            node.ImageKey = str0
            # node.SelectedImageKey = str0
    def method_20(self):
        flag = self.isExportQaAvailable
        self.btnExportQA.setVisible(flag)
        self.mniFileExportQA.setVisible(flag)
        flag = self.isExportReportAvailable
        self.btnExportReport.setVisible(flag)
        self.mniFileExportReport.setVisible(flag)
        flag = self.isCopyAvailable
        self.mniEditCopy.Enabled = flag
        self.btnCopy.Enabled = flag
        flag = self.isDeleteAvailable
        self.mniEditDelete.setVisible(flag)
        self.btnDelete.setVisible(flag)
        flag = self.isExportToWordAvailable
        self.mniEditExportWord.setVisible(flag)
        self.btnExportWord.setVisible(flag)
        flag = self.isEditCommentAvailable
        self.mniEditComment.setVisible(flag)
        self.btnEditComment.setVisible(flag)
        flag = self.isSnapshotActionAvailable
        self.mniEditExportSST.setVisible(flag)
        self.mniEditRestoreView.setVisible(flag)
        self.btnExportSST.setVisible(flag)
        self.btnRestoreView.setVisible(flag)
        self.btnSubmit.ssetEnabled(False if(self.txtHeading.setText().trimmed() == "") else self.txtComment.setText().trimmed() != "")

    def method_21(self):
        self.treeView.Clear()
        self.lblDateTime.setText("")
        self.txtHeading.setText("")
        self.txtComment.setText("")
        if (self.activeDocument != None):
            self.method_28()
            self.lblFile.setText(self.activeDocument.FileNameQA)
            self.mniFileExportQA.setEnabled(True)
            self.mniFileExportReport.setEnabled(True)
            self.btnExportQA.setEnabled(True)
            self.btnExportReport.setEnabled(True)
            self.toolStrip.setEnabled(True)
            self.splitContainer.setEnabled(True)
            self.tblComment.setEnabled(True)
        else:
            self.setWindowTitle(Captions.QUALITY_ASSURANCE_ASSISTENT)
            self.lblFile.setText("")
            self.mniFileExportQA.setEnabled(False)
            self.mniFileExportReport.setEnabled(False)
            self.btnExportQA.setEnabled(False)
            self.btnExportReport.setEnabled(False)
            self.toolStrip.setEnabled(False)
            self.splitContainer.setEnabled(False)
            self.tblComment.setEnabled(False)
        self.method_23(None, False)
        self.method_22(None, True)
        self.method_20()
    def method_22(self, string_0, bool_0):
        self.richBox.setText("")
        if (not String.IsNullOrEmpty(string_0)):
            self.richBox.setText(string_0)
        if (self.richBox.isVisible() != bool_0):
            self.richBox.setVisible(bool_0)
    def method_23(self, image_0, bool_0):
        self.picSnapshot.setFixedSize(QtCore.QSize(100, 100))
        self.picSnapshot.Image = image_0
        if (self.pnlSnapshot.isVisible() != bool_0):
            self.pnlSnapshot.setVisible(bool_0)
    def method_24(self):
        if (not self.isVisible()):
            self.setVisible(True)
        if (self.windowState() == QtCore.Qt.WindowMinimized):
            self.setWindowState(self.previousState)
        self.activateWindow()
    def method_25(self, qarecord_0):
        if (qarecord_0 == None):
            return
        if (self.activeDocument == None):
            return
        if (self.lastSessionNode == None):
            return
        tag = self.lastSessionNode.Tag#(QASession)this.lastSessionNode.Tag
        tag._class_ = QASession
        if (tag == None):
            return
        tag.Children.append(qarecord_0)
        self.method_4(self.lastSessionNode, qarecord_0)
        self.treeView.SelectedNode = self.lastSessionNode.LastNode
        if (QA0.AutoReportEntry and not (isinstance(qarecord_0, QASession) and not (isinstance(qarecord_0, QAAttached) and self.tabControl.count() == 2))):
            treeNode = None
            qAReportEntry = QAReportEntry()
            qAReportEntry.Value = qarecord_0
            self.activeDocument.ReportEntries.Add(qAReportEntry)
            self.method_5(treeNode, qAReportEntry)
            self.treeViewReport.SelectedNode = self.treeViewReport.Nodes[len(self.treeViewReport.Nodes) - 1]
        self.activeDocument.method_2(self)
    def method_26(self, string_0, string_1):
        str0 = Path.ChangeExtension(string_0, string_1)
        qAAttached = QAAttached()
        qAAttached.Heading = Captions.QA_ATTACHED,
        qAAttached.Text = Captions.QA_CONTINUING_WITH.format(str0)
        self.method_25(qAAttached)
        self.ActiveDocument.FileNameQA = str0
        qAAttached.Text = Captions.QA_ATTACHED_TO.format(string_0)
        self.method_27()
        self.ActiveDocument.method_2(self)
    def method_27(self):
        self.method_7()
    def method_28(self):
        self.windowTitle("{0} ({1})".format(Captions.QUALITY_ASSURANCE_ASSISTENT, Path.GetFileNameWithoutExtension(self.activeDocument.FileNameQA)))
    def method_29(self, treeNode_0):
        if (treeNode_0.ImageKey == None or self.ImageList == None or not self.ImageList.has_key(treeNode_0.ImageKey)):
            return 8
        size = self.ImageList.__getitem__(treeNode_0.ImageKey).size()
        return size.width() + 8
    # def method_30(self, treeNode_0):
    #     prevNode = None
    #     if treeNode_0.PrevNode != None:
    #         prevNode = treeNode_0.PrevNode
    #     elif treeNode_0.Parent != None:
    #         prevNode = treeNode_0.Parent
    #     else:
    #         prevNode = treeNode_0
    #     return self.method_32(prevNode)
    # def method_31(self, treeNode_0):
    #     nextNode = None
    #     if treeNode_0.PrevNode != None:
    #         nextNode = treeNode_0.NextNode
    #     else:
    #         nextNode = treeNode_0.Parent
    #     if (nextNode != None):
    #         nextNode = nextNode.NextNode
    #     if (nextNode == None):
    #         nextNode = treeNode_0
    #     return self.method_32(nextNode)
    def method_32(self, treeNode_0):
        #TODO: UnCompleted
        return False
        # bounds = treeNode_0.Bounds
        # clientRectangle = treeNode_0.TreeView.ClientRectangle
        # if (bounds.Top >= clientRectangle.Top && bounds.Bottom <= clientRectangle.Bottom):
        #     return True
        # }
        # treeNode_0.EnsureVisible()
        # return false
    def getIsExportQaAvailable(self):
        return self.tabControl.currentIndex() == 0
    isExportQaAvailable = property(getIsExportQaAvailable, None, None, None)

    def getIsExportReportAvailable(self):
        return self.tabControl.currentIndex() == 1
    isExportReportAvailable = property(getIsExportReportAvailable, None, None, None)

    def getIsCopyAvailable(self):
        #TODO: UnCompleted
        pass
        return False
        # treeNodeIndex = self.treeView.currentIndex() if(self.tabControl.currentIndex() == 0) else self.treeViewReport.currentIndex()
        # flag = treeNodeIndex.isValid()
        # flag1 = flag
        # # if (flag and self.tabControl.currentIndex() == 1):
        # #     tag = treeNode.Tag as QAReportEntry
        # #     if (tag != null && tag.Value == null)
        # #     {
        # #         flag1 = false
        # #     }
        # # }
        # return flag1
    isCopyAvailable = property(getIsCopyAvailable, None, None, None)

    def getIsCopyEntryToReportAvailable(self):
        if (self.tabControl.currentIndex() != 0):
            return False
        if (self.tabControl.count() != 2):
            return False
        selectedNodeIndex = self.treeView.currentIndex()
        if (not selectedNodeIndex.isValid()):
            return False
        if (not selectedNodeIndex.parent().isValid()):
            return False
        if (not selectedNodeIndex.parent().parent().isValid()):
            return False
        return True
    isCopyEntryToReportAvailable = property(getIsCopyEntryToReportAvailable, None, None, None)

    def getIsDeleteAvailable(self):
        #TODO: UnCompleted
        if (self.tabControl.currentIndex() == 0):
            return self.method_16()
        selectedNode = self.treeViewReport.currentIndex()
        if (not selectedNode.isValid()):
            return False
        return selectedNode.Tag# is QAReportEntry
    isDeleteAvailable = property(getIsDeleteAvailable, None, None, None)

    def getIsEditCommentAvailable(self):
        treeNodeIndex = self.treeView.currentIndex() if(self.tabControl.currentIndex() == 0) else self.treeViewReport.currentIndex()
        flag = False
        flag = self.method_17(treeNodeIndex) if(self.tabControl.currentIndex() != 0) else self.method_16()
        if (self.method_15(treeNodeIndex, QARecordType.Comment)):
            return flag
        return False
    isEditCommentAvailable = property(getIsEditCommentAvailable, None, None, None)

    def getIsExportToWordAvailable(self):
        #TODO:UnCompleted
        flag = False
        treeNodeIndex = self.treeView.currentIndex () if(self.tabControl.currentIndex() == 0) else self.treeViewReport.currentIndex()
        flag = False if(not treeNodeIndex.isValid()) else not self.method_15(treeNodeIndex, QARecordType.Session)
        flag1 = flag
        if (flag and self.tabControl.currentIndex() == 1):
            tag = treeNodeIndex.Tag# as QAReportEntry
            if (tag != None and tag.Value == None):
                flag1 = False
        return flag1
    isExportToWordAvailable = property(getIsExportToWordAvailable, None, None, None)

    def getIsFlagAvailable(self):
        #TODO:UnCompleted
        if (self.tabControl.currentIndex() != 1):
            return False
        selectedNodeIndex = self.treeViewReport.currentIndex()
        if (not selectedNodeIndex.isValid()):
            return False
        tag = selectedNodeIndex.Tag# as QAReportEntry
        if (tag == None):
            return False
        if (tag.Value == None):
            return False
        return True
    isFlagAvailable = property(getIsFlagAvailable, None, None, None)

    def getIsSnapshotActionAvailable(self):
        return self.method_15(self.treeView.currentIndex() if(self.tabControl.currentIndex() == 0) else self.treeViewReport.currentIndex(), QARecordType.Snapshot)
    isSnapshotActionAvailable = property(getIsSnapshotActionAvailable, None, None, None)

    


    def getActiveDocument(self):
        return self.activeDocument
    def setActiveDocument(self, val):
        self.activeDocument = val
        self.method_21()
        if (self.activeDocument != None):
            if (self.activeDocument.ReportEntriesSupported):
                if (self.tabControl.count() == 1):
                    self.tabControl.addTab(self.tabReport)
            elif (self.tabControl.count() == 2):
                self.tabControl.removeTab(1)
            self.method_2()
            if (self.tabControl.count() == 2):
                self.method_3()
            self.treeView.SelectedNode = self.method_8(self.activeDocument.SelectedRecord)
            if (self.treeView.SelectedNode == None):
                self.treeView.SelectedNode = self.lastSessionNode
            self.treeViewReport.SelectedNode = self.method_12(self.activeDocument.SelectedReportEntry)
            if (not self.isVisible()):
                self.setVisible(True)
        self.method_20()
    ActiveDocument = property(getActiveDocument, setActiveDocument, None, None)

    def get_lastSessionNode(self):
        if (len(self.treeView.Nodes) < 1):
            return None
        return self.treeView.Nodes[len(self.treeView.Nodes) - 1]
    lastSessionNode = property(get_lastSessionNode, None, None, None)