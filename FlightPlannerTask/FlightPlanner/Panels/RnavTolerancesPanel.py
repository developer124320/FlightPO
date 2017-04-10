'''
Created on 23 Apr 2014

@author: Administrator
'''
from PyQt4.QtGui import QWidget, QFrame, QVBoxLayout, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QToolButton, QIcon, QPixmap, QMenu, QSpacerItem, QDialog
from PyQt4.QtCore import QSize,SIGNAL
from FlightPlanner.helpers import Distance
from FlightPlanner.types import  DistanceUnits, RnavSpecification, AircraftSpeedCategory, \
    RnavGnssFlightPhase
from FlightPlanner.Captions import Captions
from FlightPlanner.RnavTolerance0 import RnavGnssTolerance
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Holding.RnavVorDme.RnavVorDmeDlg import RnavVorDme
from FlightPlanner.Holding.RnavDmeDme.RnavDmeDmeDlg import RnavDmeDme
from FlightPlanner.Panels.Frame import Frame

class RnavTolerancesPanel(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("RnavTolerancesPanel" + str(len(parent.findChildren(RnavTolerancesPanel))))

        self.resize(380, 90)
        horizontalLayout = QHBoxLayout(self)
        horizontalLayout.setSpacing(0)
        horizontalLayout.setMargin(0)
        horizontalLayout.setObjectName(("horizontalLayout"))

        self.basicFrame = Frame(self, "HL")
        horizontalLayout.addWidget(self.basicFrame)

        frame_2 = QFrame(self.basicFrame)
        frame_2.setFrameShape(QFrame.StyledPanel)
        frame_2.setFrameShadow(QFrame.Raised)
        frame_2.setObjectName(("frame_2"))
        verticalLayout_3 = QVBoxLayout(frame_2)
        verticalLayout_3.setSpacing(3)
        verticalLayout_3.setMargin(0)
        verticalLayout_3.setObjectName(("verticalLayout_3"))
        self.frame_Att = QFrame(frame_2)
        self.frame_Att.setFrameShape(QFrame.NoFrame)
        self.frame_Att.setFrameShadow(QFrame.Raised)
        self.frame_Att.setObjectName(("self.frame_Att"))
        horizontalLayout_70 = QHBoxLayout(self.frame_Att)
        horizontalLayout_70.setSpacing(0)
        horizontalLayout_70.setMargin(0)
        horizontalLayout_70.setObjectName(("horizontalLayout_70"))
        self.label_78 = QLabel(self.frame_Att)
        self.label_78.setMinimumSize(QSize(100, 0))
        self.label_78.setMaximumSize(QSize(100, 2222222))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_78.setFont(font)
        self.label_78.setObjectName(("self.label_78"))
        horizontalLayout_70.addWidget(self.label_78)
        frame_APV_12 = QFrame(self.frame_Att)
        frame_APV_12.setFrameShape(QFrame.StyledPanel)
        frame_APV_12.setFrameShadow(QFrame.Raised)
        frame_APV_12.setObjectName(("frame_APV_12"))
        horizontalLayout_16 = QHBoxLayout(frame_APV_12)
        horizontalLayout_16.setSpacing(0)
        horizontalLayout_16.setMargin(0)
        horizontalLayout_16.setObjectName(("horizontalLayout_16"))
        self.txtAtt = QLineEdit(frame_APV_12)
        self.txtAtt.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtAtt.setFont(font)
        self.txtAtt.setObjectName("RnavTolerancesPaneAttLineEdit" + str(len(parent.findChildren(RnavTolerancesPanel))))
        # self.txtAtt.setObjectName(("self.txtAtt"))
        horizontalLayout_16.addWidget(self.txtAtt)
        horizontalLayout_70.addWidget(frame_APV_12)
        verticalLayout_3.addWidget(self.frame_Att)
        self.frame_Xtt = QFrame(frame_2)
        self.frame_Xtt.setFrameShape(QFrame.NoFrame)
        self.frame_Xtt.setFrameShadow(QFrame.Raised)
        self.frame_Xtt.setObjectName(("frame_Xtt"))
        horizontalLayout_72 = QHBoxLayout(self.frame_Xtt)
        horizontalLayout_72.setSpacing(0)
        horizontalLayout_72.setMargin(0)
        horizontalLayout_72.setObjectName(("horizontalLayout_72"))
        self.label_80 = QLabel(self.frame_Xtt)
        self.label_80.setMinimumSize(QSize(100, 0))
        self.label_80.setMaximumSize(QSize(100, 2222222))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_80.setFont(font)
        self.label_80.setObjectName(("label_80"))
        horizontalLayout_72.addWidget(self.label_80)
        frame_APV_14 = QFrame(self.frame_Xtt)
        frame_APV_14.setFrameShape(QFrame.StyledPanel)
        frame_APV_14.setFrameShadow(QFrame.Raised)
        frame_APV_14.setObjectName(("frame_APV_14"))
        horizontalLayout_18 = QHBoxLayout(frame_APV_14)
        horizontalLayout_18.setSpacing(0)
        horizontalLayout_18.setMargin(0)
        horizontalLayout_18.setObjectName(("horizontalLayout_18"))
        self.txtXtt = QLineEdit(frame_APV_14)
        self.txtXtt.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtXtt.setFont(font)
        self.txtXtt.setObjectName("RnavTolerancesPaneXttLineEdit" + str(len(parent.findChildren(RnavTolerancesPanel))))

        # self.txtXtt.setObjectName(("self.txtXtt"))
        horizontalLayout_18.addWidget(self.txtXtt)
        horizontalLayout_72.addWidget(frame_APV_14)
        verticalLayout_3.addWidget(self.frame_Xtt)
        self.frame_Asw = QFrame(frame_2)
        self.frame_Asw.setFrameShape(QFrame.NoFrame)
        self.frame_Asw.setFrameShadow(QFrame.Raised)
        self.frame_Asw.setObjectName(("frame_Asw"))
        horizontalLayout_71 = QHBoxLayout(self.frame_Asw)
        horizontalLayout_71.setSpacing(0)
        horizontalLayout_71.setMargin(0)
        horizontalLayout_71.setObjectName(("horizontalLayout_71"))
        self.label_79 = QLabel(self.frame_Asw)
        self.label_79.setMinimumSize(QSize(100, 0))
        self.label_79.setMaximumSize(QSize(100, 2222222))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_79.setFont(font)
        self.label_79.setObjectName(("label_79"))
        horizontalLayout_71.addWidget(self.label_79)
        frame_APV_13 = QFrame(self.frame_Asw)
        frame_APV_13.setFrameShape(QFrame.StyledPanel)
        frame_APV_13.setFrameShadow(QFrame.Raised)
        frame_APV_13.setObjectName(("frame_APV_13"))
        horizontalLayout_17 = QHBoxLayout(frame_APV_13)
        horizontalLayout_17.setSpacing(0)
        horizontalLayout_17.setMargin(0)
        horizontalLayout_17.setObjectName(("horizontalLayout_17"))
        self.txtAsw = QLineEdit(frame_APV_13)
        self.txtAsw.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtAsw.setFont(font)
        self.txtAsw.setObjectName("RnavTolerancesPaneAswLineEdit" + str(len(parent.findChildren(RnavTolerancesPanel))))

        # self.txtAsw.setObjectName(("self.txtAsw"))
        horizontalLayout_17.addWidget(self.txtAsw)
        horizontalLayout_71.addWidget(frame_APV_13)
        verticalLayout_3.addWidget(self.frame_Asw)
        self.basicFrame.Add = frame_2
        self.btnDropDown = QToolButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDropDown.sizePolicy().hasHeightForWidth())
        self.btnDropDown.setSizePolicy(sizePolicy)
        self.btnDropDown.setMinimumSize(QSize(0, 0))
        self.btnDropDown.setMaximumSize(QSize(16777215, 16777215))
        self.btnDropDown.setText((""))
        self.btnDropDown.setObjectName(("btnDropDown"))
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("Resource/sort2.png"), QIcon.Normal, QIcon.Off)
        self.btnDropDown.setIcon(icon1)
        self.basicFrame.Add = self.btnDropDown
        self.setLayout(horizontalLayout)

        spacerItem = QSpacerItem(10,10,QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontalLayout.addItem(spacerItem)
        
        self.label_78.setText("ATT (nm):")
#         .self.txtAtt.setText(_translate("Form", "180", None))
        self.label_80.setText( "XTT (nm):")
#         .self.txtXtt.setText(_translate("Form", "180", None))
        self.label_79.setText("1/2 A/W (nm):")
#         .self.txtAsw.setText(_translate("Form", "180", None))
        self.hasAtt = True
        self.hasXtt = True
        self.hasAsw = True
        
        self.vorDmeVisible = False
        self.dmeDmeVisible = False
        self.btnDropDown.clicked.connect(self.btnDropDown_Click)

        self.selectedActionText = ""
    
    def set_IsVorDmeVisble(self, bool_0):
        self.vorDmeVisible = bool_0
    def get_IsVorDmeVisble(self):
        return self.vorDmeVisible
    IsVorDmeVisble = property(get_IsVorDmeVisble, None, None, None) 
    
    def set_IsDmeDmeVisble(self, bool_0):
        self.dmeDmeVisible = bool_0
    def get_IsDmeDmeVisble(self):
        return self.dmeDmeVisible
    IsDmeDmeVisble = property(get_IsDmeDmeVisble, None, None, None)

    def set_LabelWidth(self, width):
        self.label_78.setMinimumSize(QSize(width, 0))
        self.label_78.setMaximumSize(QSize(width, 16777215))

        self.label_80.setMinimumSize(QSize(width, 0))
        self.label_80.setMaximumSize(QSize(width, 16777215))

        self.label_79.setMinimumSize(QSize(width, 0))
        self.label_79.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)
    
    # def set_HasASW(self, bool_0):
    #     self.hasAsw = bool_0
    #     self.frame_Asw.setVisible(bool_0)
    #     if not bool_0:
    #         h = self.height()- 22
    #         self.resize(self.width(),h)

    def set_HasASW(self, bool_0):
        self.hasAsw = bool_0
        self.frame_Asw.setVisible(bool_0)
        # if not bool_0:
        #     h = self.height()- 22
        #     self.resize(self.width(),h)
    def get_HasASW(self):
        return self.hasAsw
    HasASW = property(get_HasASW, set_HasASW, None, None)
    
    def set_HasATT(self, bool_0):
        self.hasAtt = bool_0
        self.frame_Att.setVisible(bool_0)
        # if not bool_0:
        #     h = self.height()- 22
        #     self.resize(self.width(),h)
    def get_HasATT(self):
        return self.hasAtt
    HasATT = property(get_HasATT, set_HasATT, None, None)
    
    def set_HasXTT(self, bool_0):
        self.hasXtt = bool_0
        self.frame_Xtt.setVisible(bool_0)
        # if not bool_0:
        #     h = self.height()- 22
        #     self.resize(self.width(),h)
    def get_HasXTT(self):
        return self.hasXtt
    HasXTT = property(get_HasXTT, set_HasXTT, None, None)
    
    def get_Asw(self):
        try:
            return Distance(float(self.txtAsw.text()), DistanceUnits.NM)
        except:
            return Distance.NaN()
    def set_Asw(self, distance_0):
        self.txtAsw.setText(str(distance_0.NauticalMiles))
    ASW = property(get_Asw, set_Asw, None, None)
    
    def get_Att(self):
        try:
            return Distance(float(self.txtAtt.text()), DistanceUnits.NM)
        except:
            return Distance.NaN()
    def set_Att(self, distance_0):
        self.txtAtt.setText(str(distance_0.NauticalMiles))
    ATT = property(get_Att, set_Att, None, None)
    
    def get_Xtt(self):
        try:
            return Distance(float(self.txtXtt.text()), DistanceUnits.NM)
        except:
            return Distance.NaN()
    def set_Xtt(self, distance_0):
        self.txtXtt.setText(str(distance_0.NauticalMiles))
#         m = QMenu()
#         m.setG
    XTT = property(get_Xtt, set_Xtt, None, None)
    
    def btnDropDown_Click(self):
        
#         {
#             ToolStripMenuItem toolStripMenuItem = null;
#             self.mnuDropDown.Items.Clear();
        menu1 = QMenu(Captions.GNSS) 
        if (RnavVorDme.Result1 != None or RnavVorDme.Result2 != None):
            toolStripMenuItem00 = QMenu(Captions.VOR_DME) 
            menu1.addMenu(toolStripMenuItem00)
#             toolStripMenuItem = self.mnuDropDown.Items.Add(Captions.VOR_DME) as ToolStripMenuItem;
            if (RnavVorDme.Result1 != None):
                if (RnavVorDme.Result2 == None):
                    toolStripMenuItem00.addAction(self.method_6(Captions.WAYPOINT, RnavVorDme.Result1))
#                     toolStripMenuItem.DropDownItems.Add(self.method_6(Captions.WAYPOINT, RnavVorDme.Result1));
                else:
                    toolStripMenuItem00.addAction(self.method_6(Captions.WAYPOINT_1, RnavVorDme.Result1))
#                     toolStripMenuItem.DropDownItems.Add(self.method_6(Captions.WAYPOINT_1, RnavVorDme.Result1));
            if (RnavVorDme.Result2 != None):
                if (RnavVorDme.Result1 == None):
                    toolStripMenuItem00.addAction(self.method_6(Captions.WAYPOINT, RnavVorDme.Result2))
#                     toolStripMenuItem.DropDownItems.Add(self.method_6(Captions.WAYPOINT, RnavVorDme.Result2));
                else:
                    toolStripMenuItem00.addAction(self.method_6(Captions.WAYPOINT_2, RnavVorDme.Result2))
#                     toolStripMenuItem.DropDownItems.Add(self.method_6(Captions.WAYPOINT_2, RnavVorDme.Result2));
        if (RnavDmeDme.Result1 != None or RnavDmeDme.Result2 != None):
#                 toolStripMenuItem = self.mnuDropDown.Items.Add(Captions.DME_DME) as ToolStripMenuItem;
            toolStripMenuItem01 = QMenu(Captions.DME_DME) 
            menu1.addMenu(toolStripMenuItem01)
            if (RnavDmeDme.Result1 != None):
                if (RnavDmeDme.Result2 == None):
                    toolStripMenuItem01.addAction(self.method_7(Captions.WAYPOINT, RnavDmeDme.Result1))
#                     toolStripMenuItem.DropDownItems.Add(self.method_7(Captions.WAYPOINT, RnavDmeDme.Result1));
                else:
                    toolStripMenuItem01.addAction(self.method_7(Captions.WAYPOINT_1, RnavDmeDme.Result1))
#                     toolStripMenuItem.DropDownItems.Add(self.method_7(Captions.WAYPOINT_1, RnavDmeDme.Result1));
            if (RnavDmeDme.Result2 != None):
                if (RnavDmeDme.Result1 == None):
                    toolStripMenuItem01.addAction(self.method_7(Captions.WAYPOINT, RnavDmeDme.Result2))
#                     toolStripMenuItem.DropDownItems.Add(self.method_7(Captions.WAYPOINT, RnavDmeDme.Result2));
                else:
                    toolStripMenuItem01.addAction(self.method_7(Captions.WAYPOINT_2, RnavDmeDme.Result2))
#                     toolStripMenuItem.DropDownItems.Add(self.method_7(Captions.WAYPOINT_2, RnavDmeDme.Result2));
       
          
        if self.vorDmeVisible:
            toolStripMenuItem00 = QMenu(Captions.VOR_DME) 
            menu1.addMenu(toolStripMenuItem00)
            itemAction = QgisHelper.createAction(self, "WayPoint 1,XTT = 2.56nm,ATT = 2.01nm ", self.setValues, None, None, None)
            toolStripMenuItem00.addAction(itemAction)
            itemAction = QgisHelper.createAction(self, "WayPoint 2,XTT = 3.2nm,ATT = 2.07nm ", self.setValues, None, None, None)
            toolStripMenuItem00.addAction(itemAction)
        if self.dmeDmeVisible:
            toolStripMenuItem01 = QMenu(Captions.DME_DME) 
            menu1.addMenu(toolStripMenuItem01)
        toolStripMenuItem1 = QMenu(Captions.GNSS) 
        self.toolStripMenuItem2 = QMenu(Captions.CAT_A_B_C_D_E)
        self.toolStripMenuItem3 = QMenu(Captions.CAT_H)
        toolStripMenuItem1.addMenu(self.toolStripMenuItem2)
        toolStripMenuItem1.addMenu(self.toolStripMenuItem3)
        '''menu1 init'''
        menu1_RNAV5 = QMenu("RNAV 5")
        self.method_8(menu1_RNAV5, RnavSpecification.Rnav5, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_RNAV5)
        menu1_RNAV2 = QMenu("RNAV 2")
        self.method_8(menu1_RNAV2, RnavSpecification.Rnav2, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_RNAV2)
        menu1_RNAV1 = QMenu("RNAV 1")
        self.method_8(menu1_RNAV1, RnavSpecification.Rnav1, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_RNAV1)
        menu1_RNP4 = QMenu("RNP 4")
        self.method_8(menu1_RNP4, RnavSpecification.Rnp4, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_RNP4)
        menu1_RNP2 = QMenu("RNP 2")
        self.method_8(menu1_RNP2, RnavSpecification.Rnp2, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_RNP2)
        menu1_RNP1 = QMenu("RNP 1")
        self.method_8(menu1_RNP1, RnavSpecification.Rnp1, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_RNP1)
        menu1_ARNP2 = QMenu("Advanced RNP 2")
        self.method_8(menu1_ARNP2, RnavSpecification.ARnp2, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_ARNP2)
        menu1_ARNP1 = QMenu("Advanced RNP 1")
        self.method_8(menu1_ARNP1, RnavSpecification.ARnp1, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_ARNP1)
        menu1_ARNP09 = QMenu("Advanced RNP 0.9")
        self.method_8(menu1_ARNP09, RnavSpecification.ARnp09, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_ARNP09)
        menu1_ARNP08 = QMenu("Advanced RNP 0.8")
        self.method_8(menu1_ARNP08, RnavSpecification.ARnp08, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_ARNP08)
        menu1_ARNP07 = QMenu("Advanced RNP 0.7")
        self.method_8(menu1_ARNP07, RnavSpecification.ARnp07, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_ARNP07)
        menu1_ARNP06 = QMenu("Advanced RNP 0.6")
        self.method_8(menu1_ARNP06, RnavSpecification.ARnp06, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_ARNP06)
        menu1_ARNP05 = QMenu("Advanced RNP 0.5")
        self.method_8(menu1_ARNP05, RnavSpecification.ARnp05, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_ARNP05)
        menu1_ARNP04 = QMenu("Advanced RNP 0.4")
        self.method_8(menu1_ARNP04, RnavSpecification.ARnp04, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_ARNP04)
        menu1_ARNP03 = QMenu("Advanced RNP 0.3")
        self.method_8(menu1_ARNP03, RnavSpecification.ARnp03, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_ARNP03)
        menu1_RNPAPCH = QMenu("RNP APCH")
        self.method_8(menu1_RNPAPCH, RnavSpecification.RnpApch, AircraftSpeedCategory.C)
        self.toolStripMenuItem2.addMenu(menu1_RNPAPCH)
        '''menu2 init'''
        menu2_RNAV5 = QMenu("RNAV 5")
        self.method_8(menu2_RNAV5, RnavSpecification.Rnav5, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_RNAV5)
        menu2_RNAV2 = QMenu("RNAV 2")
        self.method_8(menu2_RNAV2, RnavSpecification.Rnav2, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_RNAV2)
        menu2_RNAV1 = QMenu("RNAV 1")
        self.method_8(menu2_RNAV1, RnavSpecification.Rnav1, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_RNAV1)
        menu2_RNP4 = QMenu("RNP 4")
        self.method_8(menu2_RNP4, RnavSpecification.Rnp4, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_RNP4)
        menu2_RNP2 = QMenu("RNP 2")
        self.method_8(menu2_RNP2, RnavSpecification.Rnp2, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_RNP2)
        menu2_RNP1 = QMenu("RNP 1")
        self.method_8(menu2_RNP1, RnavSpecification.Rnp1, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_RNP1)
        menu2_ARNP2 = QMenu("Advanced RNP 2")
        self.method_8(menu2_ARNP2, RnavSpecification.ARnp2, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_ARNP2)
        menu2_ARNP1 = QMenu("Advanced RNP 1")
        self.method_8(menu2_ARNP1, RnavSpecification.ARnp1, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_ARNP1)
        menu2_ARNP09 = QMenu("Advanced RNP 0.9")
        self.method_8(menu2_ARNP09, RnavSpecification.ARnp09, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_ARNP09)
        menu2_ARNP08 = QMenu("Advanced RNP 0.8")
        self.method_8(menu2_ARNP08, RnavSpecification.ARnp08, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_ARNP08)
        menu2_ARNP07 = QMenu("Advanced RNP 0.7")
        self.method_8(menu2_ARNP07, RnavSpecification.ARnp07, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_ARNP07)
        menu2_ARNP06 = QMenu("Advanced RNP 0.6")
        self.method_8(menu2_ARNP06, RnavSpecification.ARnp06, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_ARNP06)
        menu2_ARNP05 = QMenu("Advanced RNP 0.5")
        self.method_8(menu2_ARNP05, RnavSpecification.ARnp05, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_ARNP05)
        menu2_ARNP04 = QMenu("Advanced RNP 0.4")
        self.method_8(menu2_ARNP04, RnavSpecification.ARnp04, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_ARNP04)
        menu2_ARNP03 = QMenu("Advanced RNP 0.3")
        self.method_8(menu2_ARNP03, RnavSpecification.ARnp03, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_ARNP03)
        menu2_RNPAPCH = QMenu("RNP APCH")
        self.method_8(menu2_RNPAPCH, RnavSpecification.RnpApch, AircraftSpeedCategory.H)
        self.toolStripMenuItem3.addMenu(menu2_RNPAPCH)
        
        rcRect = self.btnDropDown.geometry()
        ptPoint = rcRect.bottomLeft()
        menu1.addMenu(toolStripMenuItem1)
        menu1.exec_( self.mapToGlobal(ptPoint) )
    def method_3(self, string_0):
        stringBuilder = "";
        if (self.hasAtt):
            if (stringBuilder != ""):
                stringBuilder += "\n";
            stringBuilder += string_0 + "ATT: " + self.txtAtt.text() + " nm";
        if (self.hasXtt):
            if (stringBuilder !=  ""):
                stringBuilder += "\n"
            stringBuilder += string_0 + "XTT: " + self.txtXtt.text() + " nm";
            # stringBuilder.Append(self.pnlXtt.method_6(string_0));
        if (self.hasAsw):
            if (stringBuilder != ""):
                stringBuilder += "\n";
            stringBuilder += string_0 + "ASW: " + self.txtAsw.text() + " nm";
            # stringBuilder.Append(self.pnlAsw.method_6(string_0));
        return stringBuilder;
    def method_6(self, string_0, rnavVorDmeTolerance_0):
#         StringBuilder stringBuilder = new StringBuilder();
#         stringBuilder.Append(string_0);
        resultStr = string_0
        if (self.hasXtt):
            xTT = Captions.XTT;
            distance = rnavVorDmeTolerance_0.XTT;
            resultStr = resultStr + ", " + xTT + " = " + str(distance.NauticalMiles) + "nm"
#             stringBuilder.Append(string.Format(", {0} = {1}", xTT, distance.method_0(":u")));
        if (self.hasAtt):
            aTT = Captions.ATT;
            aTT1 = rnavVorDmeTolerance_0.ATT;
            resultStr = resultStr + ", " + aTT + " = " + str(aTT1.NauticalMiles) + "nm"
#             stringBuilder.Append(string.Format(", {0} = {1}", aTT, aTT1.method_0(":u")));
        if (self.hasAsw):
            aSW = Captions.ASW;
            aSW1 = rnavVorDmeTolerance_0.ASW;
            resultStr = resultStr + ", " + aSW + " = " + str(aSW1.NauticalMiles) + "nm"
#             stringBuilder.Append(string.Format(", {0} = {1}", aSW, aSW1.method_0(":u")));
#         ToolStripMenuItem toolStripMenuItem = new ToolStripMenuItem(stringBuilder.ToString(), null, new EventHandler(self.method_9));
        
        itemAction = QgisHelper.createAction(self, resultStr, self.setValues, None, None, None)
#         toolStripMenuItem = QMenu(resultStr)
        distanceArray = [rnavVorDmeTolerance_0.ATT, rnavVorDmeTolerance_0.XTT, rnavVorDmeTolerance_0.ASW]
#         toolStripMenuItem.Tag = distanceArray;
        return itemAction;
    
    def method_7(self, string_0, rnavDmeDmeTolerance_0):
#         StringBuilder stringBuilder = new StringBuilder();
#         stringBuilder.Append(string_0);
        resultStr = string_0
        if (self.hasXtt):
            xTT = Captions.XTT;
            distance = rnavDmeDmeTolerance_0.XTT;
            resultStr = resultStr + ", " + xTT + " = " + str(distance.NauticalMiles) + "nm"
#             stringBuilder.Append(string.Format(", {0} = {1}", xTT, distance.method_0(":u")));
        if (self.hasAtt):
            aTT = Captions.ATT;
            aTT1 = rnavDmeDmeTolerance_0.ATT;
            resultStr = resultStr + ", " + aTT + " = " + str(aTT1.NauticalMiles) + "nm"
#             stringBuilder.Append(string.Format(", {0} = {1}", aTT, aTT1.method_0(":u")));
        if (self.hasAsw):
            aSW = Captions.ASW;
            aSW1 = rnavDmeDmeTolerance_0.ASW;
            resultStr = resultStr + ", " + aSW + " = " + str(aSW1.NauticalMiles) + "nm"
#             stringBuilder.Append(string.Format(", {0} = {1}", aSW, aSW1.method_0(":u")));
#         ToolStripMenuItem toolStripMenuItem = new ToolStripMenuItem(stringBuilder.ToString(), null, new EventHandler(self.method_9));
        
        itemAction = QgisHelper.createAction(self, resultStr, self.setValues, None, None, None)
#         toolStripMenuItem = QMenu(resultStr)
        distanceArray = [rnavDmeDmeTolerance_0.ATT, rnavDmeDmeTolerance_0.XTT, rnavDmeDmeTolerance_0.ASW]
#         toolStripMenuItem.Tag = distanceArray;
        return itemAction;
    
    def method_8(self, itemMenu, rnavSpecification_0, aircraftSpeedCategory_0):
#         itemMenu = QMenu(menuName)
        strrnavGnssFlightPhaseList = RnavGnssTolerance.smethod_0(rnavSpecification_0)
        rnavGnssFlightPhaseList = []
        for strRnavGnssFlightPhase in strrnavGnssFlightPhaseList:
            if strRnavGnssFlightPhase == "Enroute":
                rnavGnssFlightPhaseList.append(RnavGnssFlightPhase.Enroute)
            elif strRnavGnssFlightPhase == "StarSid":
                rnavGnssFlightPhaseList.append(RnavGnssFlightPhase.StarSid)
            elif strRnavGnssFlightPhase == "Star30Sid30IfIafMa30":
                rnavGnssFlightPhaseList.append(RnavGnssFlightPhase.Star30Sid30IfIafMa30)
            elif strRnavGnssFlightPhase == "Sid15":
                rnavGnssFlightPhaseList.append(RnavGnssFlightPhase.Sid15)
            elif strRnavGnssFlightPhase == "Ma15":
                rnavGnssFlightPhaseList.append(RnavGnssFlightPhase.Ma15)
            elif strRnavGnssFlightPhase == "Mapt":
                rnavGnssFlightPhaseList.append(RnavGnssFlightPhase.Mapt)
            elif strRnavGnssFlightPhase == "Faf":
                rnavGnssFlightPhaseList.append(RnavGnssFlightPhase.Faf)
            
        for rnavGnssFlightPhase in rnavGnssFlightPhaseList:
            rnavGnssTolerance = RnavGnssTolerance(rnavSpecification_0, rnavGnssFlightPhase, aircraftSpeedCategory_0)
            rnavGnssFlightPhaseTxt = RnavGnssTolerance.translateParameter(rnavGnssFlightPhase)
            stringBuilder = rnavGnssFlightPhaseTxt
            if (self.hasXtt):
                xTT = Captions.XTT
                distance = rnavGnssTolerance.xtt
                stringBuilder = stringBuilder + ", %s = %.2f nm"%(xTT, round(distance,2))
            if (self.hasAtt):
                aTT = Captions.ATT;
                aTT1 = rnavGnssTolerance.att
                stringBuilder = stringBuilder + ", %s = %.2f nm"%(aTT, round(aTT1,2))
            if (self.hasAsw):
                aSW = Captions.ASW
                aSW1 = round(rnavGnssTolerance.asw,2)
                stringBuilder = stringBuilder + ", %s = %.2f nm"%(aSW, aSW1)
            itemAction = QgisHelper.createAction(self, stringBuilder, self.setValues, None, None, None)
            itemMenu.addAction(itemAction)
#         return itemAction
    def setValues(self):
        action = self.sender()
        strTotal = action.text()
        strTotal.replace("nm", "")
        strTotal.replace(" ", "")
        strList = strTotal.split(",")
        flag = False
        for strItem in strList:
            if "=" in strItem:
                valueList = strItem.split("=")
                xz = valueList[0]
                if Captions.XTT == valueList[0]:
                    self.txtXtt.setText(valueList[1])
                    flag = True
                elif Captions.ATT == valueList[0]:
                    self.txtAtt.setText(valueList[1])
                    flag = True
                elif Captions.ASW == valueList[0]:
                    self.txtAsw.setText(valueList[1])
                    flag = True
        if flag:
            self.selectedActionText = action.text()
            self.emit(SIGNAL("valueChanged()"), self)
                
            
            