# -*- coding: UTF-8 -*-
'''
Money
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QScrollArea, QDialogButtonBox, QWidget
from PyQt4.QtCore import  SIGNAL
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.CheckedListBox import CheckedListBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.AngleGradientBoxPanel import AngleGradientBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.types import AerodromeSurfacesBalkedLandingFrom, AerodromeSurfacesInnerHorizontalLocation, AerodromeSurfacesTakeOffFrom,\
    AerodromeSurfacesCriteriaType
from FlightPlanner.helpers import AngleGradientSlope, AngleGradientSlopeUnits, Altitude, AltitudeUnits, MathHelper
from Type.String import String
from FlightPlanner.Captions import Captions
from Type.SurfaceCriteria import ApproachSurfaceCriteria, BalkedLandingSurfaceCriteria, ConicalSurfaceCriteria,\
    InnerApproachSurfaceCriteria, InnerHorizontalSurfaceCriteria, InnerTransitionalSurfaceCriteria, NavigationalAidSurfaceCriteria,\
    OuterHorizontalSurfaceCriteria, StripSurfaceCriteria, TakeOffSurfaceCriteria, TransitionalSurfaceCriteria


class DlgAerodromeSurfacesCriteria(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        self.resize(400, 500)
        self.setWindowTitle("Aerodrome Surfaces Criteria")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"))

        scrollArea = QScrollArea(self);
        scrollArea.setObjectName("scrollArea")
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget(scrollArea)
        scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        # scrollAreaWidgetContents.setGeometry(QRect(0, 0, 380, 280))
        vLayoutScrollArea = QVBoxLayout(scrollAreaWidgetContents)
        vLayoutScrollArea.setObjectName("vLayoutScrollArea")
        scrollArea.setWidget(scrollAreaWidgetContents)
        verticalLayoutDlg.addWidget(scrollArea)

        self.groupBox = GroupBox(self)
        self.groupBox.Caption = ""
        vLayoutScrollArea.addWidget(self.groupBox)

        self.panel = Frame(self.groupBox)
        self.groupBox.Add = self.panel

        self.pnlName = TextBoxPanel(self.panel)
        self.pnlName.LabelWidth = 0
        self.panel.Add = self.pnlName

        self.gbApproach = GroupBox(self.panel)
        self.gbApproach.Caption = "Approach"
        self.panel.Add = self.gbApproach

        self.pnlAPP_InnerEdge = DistanceBoxPanel(self.gbApproach, DistanceUnits.M)
        self.pnlAPP_InnerEdge.Caption = "Inner Edge"
        self.pnlAPP_InnerEdge.Button = None
        self.gbApproach.Add = self.pnlAPP_InnerEdge

        self.pnlAPP_DistFromTHR = DistanceBoxPanel(self.gbApproach, DistanceUnits.M)
        self.pnlAPP_DistFromTHR.Caption = "Distance From Threshold"
        self.pnlAPP_DistFromTHR.Button = None
        self.gbApproach.Add = self.pnlAPP_DistFromTHR

        self.pnlAPP_Divergence = AngleGradientBoxPanel(self.gbApproach)
        self.pnlAPP_Divergence.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlAPP_Divergence.Caption = "Divergence (each side)"
        self.gbApproach.Add = self.pnlAPP_Divergence

        self.gbApproach1 = GroupBox(self.gbApproach)
        self.gbApproach1.Caption = "First Section"
        self.gbApproach.Add = self.gbApproach1

        self.pnlAPP_Length1 = DistanceBoxPanel(self.gbApproach1, DistanceUnits.M)
        self.pnlAPP_Length1.Caption = "Length"
        self.pnlAPP_Length1.Button = None
        self.gbApproach1.Add = self.pnlAPP_Length1

        self.pnlAPP_Slope1 = AngleGradientBoxPanel(self.gbApproach1)
        self.pnlAPP_Slope1.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlAPP_Slope1.Caption = "Slope"
        self.gbApproach1.Add = self.pnlAPP_Slope1

        self.gbApproach2 = GroupBox(self.gbApproach)
        self.gbApproach2.Caption = "Second Section"
        self.gbApproach.Add = self.gbApproach2

        self.pnlAPP_Length2 = DistanceBoxPanel(self.gbApproach2, DistanceUnits.M)
        self.pnlAPP_Length2.Caption = "Length"
        self.pnlAPP_Length2.Button = None
        self.gbApproach2.Add = self.pnlAPP_Length2

        self.pnlAPP_Slope2 = AngleGradientBoxPanel(self.gbApproach2)
        self.pnlAPP_Slope2.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlAPP_Slope2.Caption = "Slope"
        self.gbApproach2.Add = self.pnlAPP_Slope2

        self.gbApproach3 = GroupBox(self.gbApproach)
        self.gbApproach3.Caption = "Horizontal Section"
        self.gbApproach.Add = self.gbApproach3

        self.pnlAPP_Length3 = DistanceBoxPanel(self.gbApproach3, DistanceUnits.M)
        self.pnlAPP_Length3.Caption = "Length"
        self.pnlAPP_Length3.Button = None
        self.gbApproach3.Add = self.pnlAPP_Length3

        self.pnlAPP_TotalLength = DistanceBoxPanel(self.gbApproach3, DistanceUnits.M)
        self.pnlAPP_TotalLength.Caption = "Total Length"
        self.pnlAPP_TotalLength.Button = None
        self.gbApproach3.Add = self.pnlAPP_TotalLength

        self.gbBalkedLanding = GroupBox(self.panel)
        self.gbBalkedLanding.Caption = "Balked Landing"
        self.panel.Add = self.gbBalkedLanding

        self.pnlBL_InnerEdge = DistanceBoxPanel(self.gbBalkedLanding, DistanceUnits.M)
        self.pnlBL_InnerEdge.Caption = "Length of Inner Edge"
        self.pnlBL_InnerEdge.Button = None
        self.gbBalkedLanding.Add = self.pnlBL_InnerEdge

        self.pnlBL_DistFromTHR = Frame(self.gbBalkedLanding, "HL")
        self.gbBalkedLanding.Add = self.pnlBL_DistFromTHR

        self.cmbBL_DistFromTHR = ComboBoxPanel(self.pnlBL_DistFromTHR)
        self.cmbBL_DistFromTHR.CaptionUnits = "m"
        self.cmbBL_DistFromTHR.Caption = "Distance From Threshold"
        self.pnlBL_DistFromTHR.Add = self.cmbBL_DistFromTHR

        self.txtBL_DistFromTHR = DistanceBoxPanel(self.pnlBL_DistFromTHR, DistanceUnits.M)
        self.txtBL_DistFromTHR.LabelWidth = 0
        self.txtBL_DistFromTHR.Button = None
        self.pnlBL_DistFromTHR.Add = self.txtBL_DistFromTHR

        self.pnlBL_Divergence = AngleGradientBoxPanel(self.gbBalkedLanding)
        self.pnlBL_Divergence.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlBL_Divergence.Caption = "Divergence (each side)"
        self.gbBalkedLanding.Add = self.pnlBL_Divergence

        self.pnlBL_Slope = AngleGradientBoxPanel(self.gbBalkedLanding)
        self.pnlBL_Slope.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlBL_Slope.Caption = "Slope"
        self.gbBalkedLanding.Add = self.pnlBL_Slope

        self.gbConical = GroupBox(self.panel)
        self.gbConical.Caption = "Conical"
        self.panel.Add = self.gbConical

        self.pnlCON_Slope = AngleGradientBoxPanel(self.gbConical)
        self.pnlCON_Slope.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlCON_Slope.Caption = "Slope"
        self.gbConical.Add = self.pnlCON_Slope

        self.pnlCON_Height = AltitudeBoxPanel(self.gbConical)
        self.pnlCON_Height.CaptionUnits = "m"
        self.pnlCON_Height.Caption = "Height"
        self.gbConical.Add = self.pnlCON_Height

        self.gbInnerApproach = GroupBox(self.panel)
        self.gbInnerApproach.Caption = "Inner Approach"
        self.panel.Add = self.gbInnerApproach

        self.pnlIA_Width = DistanceBoxPanel(self.gbInnerApproach, DistanceUnits.M)
        self.pnlIA_Width.Caption = "Width"
        self.pnlIA_Width.Button = None
        self.gbInnerApproach.Add = self.pnlIA_Width

        self.pnlIA_DistFromTHR = DistanceBoxPanel(self.gbInnerApproach, DistanceUnits.M)
        self.pnlIA_DistFromTHR.Caption = "Distance From Threshold"
        self.pnlIA_DistFromTHR.Button = None
        self.gbInnerApproach.Add = self.pnlIA_DistFromTHR

        self.pnlIA_Length = DistanceBoxPanel(self.gbInnerApproach, DistanceUnits.M)
        self.pnlIA_Length.Caption = "Length"
        self.pnlIA_Length.Button = None
        self.gbInnerApproach.Add = self.pnlIA_Length

        self.pnlIA_Slope = AngleGradientBoxPanel(self.gbInnerApproach)
        self.pnlIA_Slope.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlIA_Slope.Caption = "Slope"
        self.gbInnerApproach.Add = self.pnlIA_Slope

        self.gbInnerHorizontal = GroupBox(self.panel)
        self.gbInnerHorizontal.Caption = "Inner Horizontal"
        self.panel.Add = self.gbInnerHorizontal

        self.pnlIH_Location = ComboBoxPanel(self.gbInnerHorizontal)
        self.pnlIH_Location.Caption = "Location"
        self.gbInnerHorizontal.Add = self.pnlIH_Location

        self.pnlIH_Height = AltitudeBoxPanel(self.gbInnerHorizontal)
        self.pnlIH_Height.CaptionUnits = "m"
        self.pnlIH_Height.Caption = "Height"
        self.gbInnerHorizontal.Add = self.pnlIH_Height

        self.pnlIH_Radius = DistanceBoxPanel(self.gbInnerHorizontal, DistanceUnits.M)
        self.pnlIH_Radius.Caption = "Radius"
        self.pnlIH_Radius.Button = None
        self.gbInnerHorizontal.Add = self.pnlIH_Radius

        self.gbInnerTransitional = GroupBox(self.panel)
        self.gbInnerTransitional.Caption = "Inner Transitional"
        self.panel.Add = self.gbInnerTransitional

        self.pnlIT_Slope = AngleGradientBoxPanel(self.gbInnerTransitional)
        self.pnlIT_Slope.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlIT_Slope.Caption = "Slope"
        self.gbInnerTransitional.Add = self.pnlIT_Slope

        self.gbNavAid = GroupBox(self.panel)
        self.gbNavAid.Caption = "1:10 Navigational Aid"
        self.panel.Add = self.gbNavAid

        self.pnlNA_Slope = AngleGradientBoxPanel(self.gbNavAid)
        self.pnlNA_Slope.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlNA_Slope.Caption = "Slope"
        self.gbNavAid.Add = self.pnlNA_Slope

        self.gbOuterHorizontal = GroupBox(self.panel)
        self.gbOuterHorizontal.Caption = "Outer Horizontal"
        self.panel.Add = self.gbOuterHorizontal

        self.pnlOH_Height = AltitudeBoxPanel(self.gbOuterHorizontal)
        self.pnlOH_Height.CaptionUnits = "m"
        self.pnlOH_Height.Caption = "Height"
        self.gbOuterHorizontal.Add = self.pnlOH_Height

        self.pnlOH_Radius = DistanceBoxPanel(self.gbOuterHorizontal, DistanceUnits.M)
        self.pnlOH_Radius.Caption = "Radius"
        self.pnlOH_Radius.Button = None
        self.gbOuterHorizontal.Add = self.pnlOH_Radius

        self.gbStrip = GroupBox(self.panel)
        self.gbStrip.Caption = "Strip"
        self.panel.Add = self.gbStrip

        self.pnlS_Width = DistanceBoxPanel(self.gbStrip, DistanceUnits.M)
        self.pnlS_Width.Caption = "Width"
        self.pnlS_Width.Button = None
        self.gbStrip.Add = self.pnlS_Width

        self.pnlS_Length = DistanceBoxPanel(self.gbStrip, DistanceUnits.M)
        self.pnlS_Length.Caption = "Length"
        self.pnlS_Length.Button = None
        self.gbStrip.Add = self.pnlS_Length

        self.gbTakeOff = GroupBox(self.panel)
        self.gbTakeOff.Caption = "Take-off "
        self.panel.Add = self.gbTakeOff

        self.pnlTO_InnerEdge = DistanceBoxPanel(self.gbTakeOff, DistanceUnits.M)
        self.pnlTO_InnerEdge.Caption = "Length of Inner Edge"
        self.pnlTO_InnerEdge.Button = None
        self.gbTakeOff.Add = self.pnlTO_InnerEdge

        self.pnlTO_DistFromEND = Frame(self.gbTakeOff, "HL")
        self.gbTakeOff.Add = self.pnlTO_DistFromEND

        self.cmbTO_DistFromEND = ComboBoxPanel(self.pnlTO_DistFromEND)
        self.cmbTO_DistFromEND.CaptionUnits = "m"
        self.cmbTO_DistFromEND.Caption = "Distance From Runway End"
        self.pnlTO_DistFromEND.Add = self.cmbTO_DistFromEND

        self.txtTO_DistFromEND = DistanceBoxPanel(self.pnlTO_DistFromEND, DistanceUnits.M)
        self.txtTO_DistFromEND.LabelWidth = 0
        self.txtTO_DistFromEND.Button = None
        self.pnlTO_DistFromEND.Add = self.txtTO_DistFromEND

        self.pnlTO_Divergence = AngleGradientBoxPanel(self.gbTakeOff)
        self.pnlTO_Divergence.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlTO_Divergence.Caption = "Divergence (each side)"
        self.gbTakeOff.Add = self.pnlTO_Divergence

        self.pnlTO_FinalWidth = DistanceBoxPanel(self.gbTakeOff, DistanceUnits.M)
        self.pnlTO_FinalWidth.Caption = "Final Width"
        self.pnlTO_FinalWidth.Button = None
        self.gbTakeOff.Add = self.pnlTO_FinalWidth

        self.pnlTO_Length = DistanceBoxPanel(self.gbTakeOff, DistanceUnits.M)
        self.pnlTO_Length.Caption = "Length"
        self.pnlTO_Length.Button = None
        self.gbTakeOff.Add = self.pnlTO_Length

        self.pnlTO_Slope = AngleGradientBoxPanel(self.gbTakeOff)
        self.pnlTO_Slope.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlTO_Slope.Caption = "Slope"
        self.gbTakeOff.Add = self.pnlTO_Slope

        self.gbTransitional = GroupBox(self.panel)
        self.gbTransitional.Caption = "Transitional"
        self.panel.Add = self.gbTransitional

        self.pnlT_Slope = AngleGradientBoxPanel(self.gbTransitional)
        self.pnlT_Slope.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlT_Slope.Caption = "Slope"
        self.gbTransitional.Add = self.pnlT_Slope

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"))
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.btnSave = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)
        self.btnSave.setText("Save")

        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        vLayoutScrollArea.addWidget(self.btnBoxOkCancel)

        self.cmbBL_DistFromTHR.Items = AerodromeSurfacesBalkedLandingFrom.Items
        self.pnlIH_Location.Items = AerodromeSurfacesInnerHorizontalLocation.Items
        self.cmbTO_DistFromEND.Items = AerodromeSurfacesTakeOffFrom.Items


        self.connect(self.pnlT_Slope, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlTO_Slope, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlTO_Length, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlTO_FinalWidth, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlTO_Divergence, SIGNAL("Event_0"), self.method_6)
        self.connect(self.txtTO_DistFromEND, SIGNAL("Event_0"), self.method_6)
        self.connect(self.cmbTO_DistFromEND, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlTO_InnerEdge, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlS_Length, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlS_Width, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlOH_Radius, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlOH_Height, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlNA_Slope, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlIT_Slope, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlIH_Radius, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlIH_Height, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlIH_Location, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlIA_Slope, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlIA_Length, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlIA_DistFromTHR, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlIA_Width, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlCON_Height, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlCON_Slope, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlBL_Slope, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlBL_Divergence, SIGNAL("Event_0"), self.method_6)

        self.connect(self.txtBL_DistFromTHR, SIGNAL("Event_0"), self.method_6)
        self.connect(self.cmbBL_DistFromTHR, SIGNAL("Event_0"), self.cmbBL_DistFromTHR_currentIndexChanged)
        self.connect(self.pnlBL_InnerEdge, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlAPP_TotalLength, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlAPP_Length3, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlAPP_Slope2, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlAPP_Length2, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlAPP_Slope1, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlAPP_Length1, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlAPP_Divergence, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlAPP_DistFromTHR, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlAPP_InnerEdge, SIGNAL("Event_0"), self.method_6)
        self.connect(self.pnlName, SIGNAL("Event_0"), self.method_6)

        self.modified = False
        self.criteria = None

    def acceptDlg(self):
        self.accept()

    def method_5(self):
        self.txtBL_DistFromTHR.Enabled = self.cmbBL_DistFromTHR.SelectedIndex > 0
    def method_6(self):
        if (not self.modified):
            self.setWindowTitle(Captions.CRITERIA_MODIFIED)
            self.btnSave.setEnabled(True)
            self.modified = True

    def cmbBL_DistFromTHR_currentIndexChanged(self):
        self.method_5()
        if (not self.modified):
            self.setWindowTitle(Captions.CRITERIA_MODIFIED)
            self.btnSave.setEnabled(True)
            self.modified = True

    @staticmethod
    def smethod_0(parent, aerodromeSurfacesCriteria_0):
        flag = False
        dlgAerodromeSurfacesCriterium = DlgAerodromeSurfacesCriteria()
        dlgAerodromeSurfacesCriterium.Criteria = aerodromeSurfacesCriteria_0
        resultDlg = dlgAerodromeSurfacesCriterium.exec_()
        if (not resultDlg == 1):
            flag = False
        else:
            aerodromeSurfacesCriteria_0 = dlgAerodromeSurfacesCriterium.Criteria
            flag = True
        return flag, aerodromeSurfacesCriteria_0

    def get_Criteria(self):
        num = None
        self.criteria.Criteria = AerodromeSurfacesCriteriaType.Custom
        self.criteria.Name = self.pnlName.Value
        approachSurfaceCriterium = self.criteria
        metres = self.pnlAPP_InnerEdge.Value.Metres
        metres1 = self.pnlAPP_DistFromTHR.Value.Metres
        percent = self.pnlAPP_Divergence.Value.Percent
        num1 = self.pnlAPP_Length1.Value.Metres
        percent1 = self.pnlAPP_Slope1.Value.Percent
        metres2 = self.pnlAPP_Length2.Value.Metres
        percent2 = self.pnlAPP_Slope2.Value.Percent
        num2 = self.pnlAPP_Length3.Value.Metres
        value = self.pnlAPP_TotalLength.Value
        approachSurfaceCriterium.Approach = ApproachSurfaceCriteria(metres, metres1, percent, num1, percent1, metres2, percent2, num2, value.Metres)
        balkedLandingSurfaceCriterium = self.criteria
        metres3 = self.pnlBL_InnerEdge.Value.Metres
        num = (self.cmbBL_DistFromTHR.SelectedIndex > 0) and self.txtBL_DistFromTHR.Value.Metres or None
        percent3 = self.pnlBL_Divergence.Value.Percent
        angleGradientSlope = self.pnlBL_Slope.Value
        balkedLandingSurfaceCriterium.BalkedLanding = BalkedLandingSurfaceCriteria(metres3, num, self.cmbBL_DistFromTHR.SelectedIndex == 2, percent3, angleGradientSlope.Percent)
        conicalSurfaceCriterium = self.criteria
        num3 = self.pnlCON_Slope.Value.Percent
        altitude = self.pnlCON_Height.Value
        conicalSurfaceCriterium.Conical = ConicalSurfaceCriteria(num3, altitude.Metres)
        innerApproachSurfaceCriterium = self.criteria
        metres4 = self.pnlIA_Width.Value.Metres
        num4 = self.pnlIA_DistFromTHR.Value.Metres
        metres5 = self.pnlIA_Length.Value.Metres
        value1 = self.pnlIA_Slope.Value
        innerApproachSurfaceCriterium.InnerApproach = InnerApproachSurfaceCriteria(metres4, num4, metres5, value1.Percent)
        innerHorizontalSurfaceCriterium = self.criteria
        selectedItem = self.pnlIH_Location.SelectedItem
        num5 = self.pnlIH_Height.Value.Metres
        distance = self.pnlIH_Radius.Value
        innerHorizontalSurfaceCriterium.InnerHorizontal = InnerHorizontalSurfaceCriteria(selectedItem, num5, distance.Metres)
        self.criteria.InnerTransitional =  InnerTransitionalSurfaceCriteria(self.pnlIT_Slope.Value.Percent)
        self.criteria.NavigationalAid = NavigationalAidSurfaceCriteria(self.pnlNA_Slope.Value.Percent)
        outerHorizontalSurfaceCriterium = self.criteria
        metres6 = self.pnlOH_Height.Value.Metres
        distance1 = self.pnlOH_Radius.Value
        outerHorizontalSurfaceCriterium.OuterHorizontal = OuterHorizontalSurfaceCriteria(metres6, distance1.Metres)
        stripSurfaceCriterium = self.criteria
        num6 = self.pnlS_Length.Value.Metres
        value2 = self.pnlS_Width.Value
        stripSurfaceCriterium.Strip = StripSurfaceCriteria(num6, value2.Metres)
        takeOffSurfaceCriterium = self.criteria
        metres7 = self.pnlTO_InnerEdge.Value.Metres
        num7 = self.txtTO_DistFromEND.Value.Metres
        percent4 = self.pnlTO_Divergence.Value.Percent
        metres8 = self.pnlTO_FinalWidth.Value.Metres
        num8 = self.pnlTO_Length.Value.Metres
        angleGradientSlope1 = self.pnlTO_Slope.Value
        takeOffSurfaceCriterium.TakeOff = TakeOffSurfaceCriteria(metres7, num7, self.cmbTO_DistFromEND.SelectedIndex == 1, percent4, metres8, num8, angleGradientSlope1.Percent)
        self.criteria.Transitional = TransitionalSurfaceCriteria(self.pnlT_Slope.Value.Percent)
        return self.criteria
    def set_Criteria(self, value):
        if value == None:
            return
        self.criteria = value
        self.pnlName.Value = self.criteria.Name
        if (self.criteria.Approach.Enabled):
            self.pnlAPP_InnerEdge.Value = Distance(self.criteria.Approach.InnerEdge)
            self.pnlAPP_DistFromTHR.Value = Distance(self.criteria.Approach.DistFromTHR)
            self.pnlAPP_Divergence.Value = AngleGradientSlope(self.criteria.Approach.Divergence, AngleGradientSlopeUnits.Percent)
            self.pnlAPP_Length1.Value = Distance(self.criteria.Approach.Length1)
            self.pnlAPP_Slope1.Value = AngleGradientSlope(self.criteria.Approach.Slope1, AngleGradientSlopeUnits.Percent)
            if (self.criteria.Approach.HasSection2):
                self.pnlAPP_Length2.Value = Distance(self.criteria.Approach.Length2)
                self.pnlAPP_Slope2.Value = AngleGradientSlope(self.criteria.Approach.Slope2, AngleGradientSlopeUnits.Percent)
                self.pnlAPP_Length3.Value = Distance(self.criteria.Approach.Length3)
                self.pnlAPP_TotalLength.Value = Distance(self.criteria.Approach.TotalLength)
        self.cmbBL_DistFromTHR.SelectedIndex = 0
        if (self.criteria.BalkedLanding.Enabled):
            self.pnlBL_InnerEdge.Value = Distance(self.criteria.BalkedLanding.InnerEdge)
            if (not MathHelper.smethod_97(self.criteria.BalkedLanding.DistFromTHR, 0)):
                self.txtBL_DistFromTHR.Value = Distance(self.criteria.BalkedLanding.DistFromTHR)
                if (not self.criteria.BalkedLanding.DistFromTHRFixed):
                    self.cmbBL_DistFromTHR.SelectedIndex = 1
                else:
                    self.cmbBL_DistFromTHR.SelectedIndex = 2
            else:
                self.cmbBL_DistFromTHR.SelectedIndex = 0
            self.pnlBL_Divergence.Value = AngleGradientSlope(self.criteria.BalkedLanding.Divergence, AngleGradientSlopeUnits.Percent)
            self.pnlBL_Slope.Value = AngleGradientSlope(self.criteria.BalkedLanding.Slope, AngleGradientSlopeUnits.Percent)
        if (self.criteria.Conical.Enabled):
            self.pnlCON_Slope.Value = AngleGradientSlope(self.criteria.Conical.Slope, AngleGradientSlopeUnits.Percent)
            self.pnlCON_Height.Value = Altitude(self.criteria.Conical.Height)
        if (self.criteria.InnerApproach.Enabled):
            self.pnlIA_Width.Value = Distance(self.criteria.InnerApproach.Width)
            self.pnlIA_DistFromTHR.Value = Distance(self.criteria.InnerApproach.DistFromTHR)
            self.pnlIA_Length.Value = Distance(self.criteria.InnerApproach.Length)
            self.pnlIA_Slope.Value = AngleGradientSlope(self.criteria.InnerApproach.Slope, AngleGradientSlopeUnits.Percent)
        self.pnlIH_Location.SelectedItem = self.criteria.InnerHorizontal.Location
        self.pnlIH_Height.Value = Altitude(self.criteria.InnerHorizontal.Height)
        self.pnlIH_Radius.Value = Distance(self.criteria.InnerHorizontal.Radius)
        if (self.criteria.InnerTransitional.Enabled):
            self.pnlIT_Slope.Value = AngleGradientSlope(self.criteria.InnerTransitional.Slope, AngleGradientSlopeUnits.Percent)
        if (self.criteria.NavigationalAid.Enabled):
            self.pnlNA_Slope.Value = AngleGradientSlope(self.criteria.NavigationalAid.Slope, AngleGradientSlopeUnits.Percent)
        if (self.criteria.OuterHorizontal.Enabled):
            self.pnlOH_Height.Value = Altitude(self.criteria.OuterHorizontal.Height)
            self.pnlOH_Radius.Value = Distance(self.criteria.OuterHorizontal.Radius)
        self.pnlS_Width.Value = Distance(self.criteria.Strip.Width)
        self.pnlS_Length.Value = Distance(self.criteria.Strip.Length)
        if (not self.criteria.TakeOff.DistFromENDFixed):
            self.cmbTO_DistFromEND.SelectedIndex = 0
        else:
            self.cmbTO_DistFromEND.SelectedIndex = 1
        if (self.criteria.TakeOff.Enabled):
            self.pnlTO_InnerEdge.Value = Distance(self.criteria.TakeOff.InnerEdge)
            self.txtTO_DistFromEND.Value = Distance(self.criteria.TakeOff.DistFromEND)
            self.pnlTO_Divergence.Value = AngleGradientSlope(self.criteria.TakeOff.Divergence, AngleGradientSlopeUnits.Percent)
            self.pnlTO_FinalWidth.Value = Distance(self.criteria.TakeOff.FinalWidth)
            self.pnlTO_Length.Value = Distance(self.criteria.TakeOff.Length)
            self.pnlTO_Slope.Value = AngleGradientSlope(self.criteria.TakeOff.Slope, AngleGradientSlopeUnits.Percent)
        if (self.criteria.Transitional.Enabled):
            self.pnlT_Slope.Value = AngleGradientSlope(self.criteria.Transitional.Slope, AngleGradientSlopeUnits.Percent)
    Criteria = property(get_Criteria, set_Criteria)
