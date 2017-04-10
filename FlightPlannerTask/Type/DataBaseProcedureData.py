from FlightPlanner.types import ProcEntityListType, DegreesType, ProcEntityParseNodeType, \
    DataBaseProcedureExportType, CodeRefOchAixm, CodePhaseProcAixm, CodeTypeCourseAixm, \
    CodeDirTurnAixm, CodeTypeFlyByAixm, CodeDescrDistVerAixm, CodeDistVerAixm, CodeSpeedRefAixm, \
    CodeRepAtcAixm, CodeIapFixAixm, CodeLegTypeAixm, CodePathTypeAixm, CodeCatIlsAixm, CodeTypeDesigPtAixm
from FlightPlanner.helpers import EnumHelper
from Type.ProcEntity import ProcEntityPCP, ProcEntityTCN, ProcEntityVOR, ProcEntityDPN, \
                            ProcEntityNDB, ProcEntityDME, ProcEntityMKR, ProcEntityRCP,\
                            ProcEntitySNY, ProcEntityILS, ProcEntityMLS, ProcEntityAHP,\
                            ProcEntityFCP, ProcEntityTLA, ProcEntityRDN, ProcEntityFDN

from Type.Degrees import Degrees
from Type.Extensions import XmlNode
from Type.String import String
import math

from PyQt4.QtCore import QString

class DataBaseProcedureData:
    def __init__(self):
        self.FORMAT_DIST_VER = "0.0###";
        self.FORMAT_DIST_HORZ = "0.0###";
        self.FORMAT_ANGLE_BRG = "000.0###";
        self.FORMAT_ANGLE = "0.0###";
        self.FORMAT_DUR = "0.0#";
        self.FORMAT_SPEED = "0.0#";
        self.points = [];
        self.directions = [];
        self.aerodromes = [];
        self.mgps = [];
    def method_0(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityVOR = ProcEntityVOR((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("VorUid") or xmlNode_0);
        procEntityVOR1 = self.method_2(procEntityVOR);
        if (procEntityVOR1 != None):
            return procEntityVOR1;
        self.points.append(procEntityVOR);
        return procEntityVOR;
    def method_1(self, string_0, string_1, string_2):
        for procEntityBase_0 in self.points:
            if not isinstance(procEntityBase_0, ProcEntityVOR) or not (procEntityBase_0.CodeId == string_0) or not (procEntityBase_0.GeoLat == string_1):
                continue
            if procEntityBase_0.GeoLong == string_2:
                return procEntityBase_0
        return None
    def method_2(self, procEntityVOR_0):
        return self.method_1(procEntityVOR_0.CodeId, procEntityVOR_0.GeoLat, procEntityVOR_0.GeoLong);
    def method_3(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityTCN = ProcEntityTCN((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("TcnUid") or xmlNode_0);
        procEntityTCN1 = self.method_5(procEntityTCN);
        if (procEntityTCN1 != None):
            return procEntityTCN1;
        self.points.append(procEntityTCN);
        return procEntityTCN;
    def method_4(self, string_0, string_1, string_2):
        for procEntityBase_0 in self.points:
            if not isinstance(procEntityBase_0, ProcEntityTCN) or not (procEntityBase_0.CodeId == string_0) or not (procEntityBase_0.GeoLat == string_1):
                continue
            if procEntityBase_0.GeoLong == string_2:
                return procEntityBase_0
        return None
    def method_5(self, procEntityTCN_0):
        return self.method_4(procEntityTCN_0.CodeId, procEntityTCN_0.GeoLat, procEntityTCN_0.GeoLong);
    def method_6(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityDME = ProcEntityDME((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("DmeUid") or xmlNode_0);
        procEntityDME1 = self.method_8(procEntityDME);
        if (procEntityDME1 != None):
            return procEntityDME1;
        self.points.append(procEntityDME);
        return procEntityDME;
    def method_7(self, string_0, string_1, string_2):
        for procEntityBase_0 in self.points:
            if not isinstance(procEntityBase_0, ProcEntityDME) or not (procEntityBase_0.CodeId == string_0) or not (procEntityBase_0.GeoLat == string_1):
                continue
            if procEntityBase_0.GeoLong == string_2:
                return procEntityBase_0
        return None
    def method_8(self, procEntityDME_0):
        return self.method_7(procEntityDME_0.CodeId, procEntityDME_0.GeoLat, procEntityDME_0.GeoLong);
    def method_9(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityNDB = ProcEntityNDB((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("NdbUid") or xmlNode_0);
        procEntityNDB1 = self.method_11(procEntityNDB);
        if (procEntityNDB1 != None):
            return procEntityNDB1;
        self.points.append(procEntityNDB);
        return procEntityNDB;
    def method_10(self, string_0, string_1, string_2):
        for procEntityBase_0 in self.points:
            if not isinstance(procEntityBase_0, ProcEntityNDB) or not (procEntityBase_0.CodeId == string_0) or not (procEntityBase_0.GeoLat == string_1):
                continue
            if procEntityBase_0.GeoLong == string_2:
                return procEntityBase_0
        return None
    def method_11(self, procEntityNDB_0):
        return self.method_10(procEntityNDB_0.CodeId, procEntityNDB_0.GeoLat, procEntityNDB_0.GeoLong);
    def method_12(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityMKR = ProcEntityMKR((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("MkrUid") or xmlNode_0);
        if (procEntityParseNodeType_0 == ProcEntityParseNodeType.Node):
            xmlNodes = xmlNode_0.namedItem("txtName");
            if (not xmlNodes.isNull()):
                procEntityMKR.TxtName = xmlNodes.toElement().text();
            xmlNodes = xmlNode_0.namedItem("txtRmk");
            if (not xmlNodes.isNull()):
                procEntityMKR.TxtRmk = xmlNodes.toElement().text();
        procEntityMKR1 = self.method_14(procEntityMKR);
        if (procEntityMKR1 != None):
            return procEntityMKR1;
        self.points.append(procEntityMKR);
        return procEntityMKR;
    def method_13(self, string_0, string_1, string_2):
        for procEntityBase_0 in self.points:
            if not isinstance(procEntityBase_0, ProcEntityMKR) or not (procEntityBase_0.CodeId == string_0) or not (procEntityBase_0.GeoLat == string_1):
                continue
            if procEntityBase_0.GeoLong == string_2:
                return procEntityBase_0
        return None
    def method_14(self, procEntityMKR_0):
        return self.method_13(procEntityMKR_0.CodeId, procEntityMKR_0.GeoLat, procEntityMKR_0.GeoLong);
    def method_15(self, xmlNode_0, procEntityParseNodeType_0):
        xmlNodes = (procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("SnyUid") or xmlNode_0;
        procEntitySNY = ProcEntitySNY(xmlNodes.namedItem("codeId").toElement().text(), xmlNodes.namedItem("codeType").toElement().text());
        if (procEntityParseNodeType_0 == ProcEntityParseNodeType.Node):
            xmlNodes1 = xmlNode_0.namedItem("txtName");
            if (not xmlNodes1.isNull()):
                procEntitySNY.TxtName = xmlNodes1.toElement().text();
            xmlNodes1 = xmlNode_0.namedItem("txtRmk");
            if (not xmlNodes1.isNull()):
                procEntitySNY.TxtRmk = xmlNodes1.toElement().text();
        procEntitySNY1 = self.method_17(procEntitySNY);
        if (procEntitySNY1 != None):
            return procEntitySNY1;
        self.points.append(procEntitySNY);
        return procEntitySNY;
    def method_16(self, string_0, string_1):
        for procEntityBase_0 in self.points:
            if not isinstance(procEntityBase_0, ProcEntitySNY) or not (procEntityBase_0.CodeId == string_0):
                continue
            if procEntityBase_0.CodeType == string_1:
                return procEntityBase_0
        return None
    def method_17(self, procEntitySNY_0):
        return self.method_16(procEntitySNY_0.CodeId, procEntitySNY_0.CodeType);
    def method_18(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityRCP = ProcEntityRCP((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("RcpUid") or xmlNode_0);
        procEntityRCP1 = self.method_20(procEntityRCP);
        if (procEntityRCP1 != None):
            return procEntityRCP1;
        self.points.append(procEntityRCP);
        return procEntityRCP;

    def method_19(self, string_0, string_1, string_2, string_3):
        for procEntityBase_0 in self.points:
            if (not (isinstance(procEntityBase_0, ProcEntityRCP)) or not (procEntityBase_0.CodeId == string_0) or not (procEntityBase_0.TxtDesig == string_1) or not (procEntityBase_0.GeoLat == string_2)):
                continue
            if procEntityBase_0.GeoLong == string_3:
                return procEntityBase_0
        return None

    def method_20(self, procEntityRCP_0):
        return self.method_19(procEntityRCP_0.CodeId, procEntityRCP_0.TxtDesig, procEntityRCP_0.GeoLat, procEntityRCP_0.GeoLong);

    def method_21(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityFCP = ProcEntityFCP((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("FcpUid") or xmlNode_0);
        procEntityFCP1 = self.method_23(procEntityFCP);
        if (procEntityFCP1 != None):
            return procEntityFCP1;
        self.points.append(procEntityFCP);
        return procEntityFCP;

    def method_22(self, string_0, string_1, string_2, string_3):
        for procEntityBase_0 in self.points:
            if (not isinstance(procEntityBase_0, ProcEntityFCP) or not (procEntityBase_0.CodeId == string_0) or not (procEntityBase_0.TxtDesig == string_1) or not (procEntityBase_0.GeoLat == string_2)):
                continue
            if procEntityBase_0.GeoLong == string_3:
                return procEntityBase_0
        return None

    def method_23(self, procEntityFCP_0):
        return self.method_22(procEntityFCP_0.CodeId, procEntityFCP_0.TxtDesig, procEntityFCP_0.GeoLat, procEntityFCP_0.GeoLong);

    def method_24(self, procEntityPCP_0):
        self.points.append(procEntityPCP_0);

    def method_25(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityPCP = ProcEntityPCP((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("PcpUid") or xmlNode_0);
        if (procEntityParseNodeType_0 == ProcEntityParseNodeType.Node):
            xmlNodes = xmlNode_0.namedItem("codeType");
            if (not xmlNodes.isNull()):
                procEntityPCP.TxtName = xmlNodes.toElement().text();
            xmlNodes = xmlNode_0.namedItem("txtRmk");
            if (not xmlNodes.isNull()):
                procEntityPCP.TxtRmk = xmlNodes.toElement().text();
        procEntityPCP1 = self.method_28(procEntityPCP);
        if (procEntityPCP1 != None):
            return procEntityPCP1;
        self.points.append(procEntityPCP);
        return procEntityPCP;
    

    def method_26(self, string_0, degrees_0, degrees_1):
        for procEntityBase_0 in self.points:
            if not isinstance(procEntityBase_0, ProcEntityPCP):
                continue
            degree = Degrees.smethod_15(procEntityBase_0.GeoLat, DegreesType.Latitude);
            degree1 = Degrees.smethod_15(procEntityBase_0.GeoLong, DegreesType.Longitude);
            if (not (procEntityBase_0.TxtDesig == string_0) or not degree.method_3(degrees_0)):
                continue;
            if degree1.method_3(degrees_1):
                return procEntityBase_0
        return None
    
    def method_27(self, string_0, string_1, string_2):
        for procEntityBase_0 in self.points:
            if (not isinstance(procEntityBase_0, ProcEntityPCP) or not (procEntityBase_0.TxtDesig == string_0) or not (procEntityBase_0.GeoLat == string_1)):
                continue
            if procEntityBase_0.GeoLong == string_2:
                return procEntityBase_0
        return None

    def method_28(self, procEntityPCP_0):
        return self.method_27(procEntityPCP_0.TxtDesig, procEntityPCP_0.GeoLat, procEntityPCP_0.GeoLong);

    def method_29(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityRDN = ProcEntityRDN((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("RdnUid") or xmlNode_0);
        procEntityRDN1 = self.method_31(procEntityRDN);
        if (procEntityRDN1 != None):
            return procEntityRDN1;
        self.directions.append(procEntityRDN);
        return procEntityRDN;

    def method_30(self, string_0, string_1, string_2):
        for procEntityDirectionBase0 in self.directions:
            if not isinstance(procEntityDirectionBase0, ProcEntityRDN):
                continue
            if (not (procEntityDirectionBase0.AhpCodeId == string_0) or not (procEntityDirectionBase0.RdnDesig == string_2)):
                continue
            if procEntityDirectionBase0.RwyDesig == string_1:
                return procEntityDirectionBase0
        return None

    def method_31(self, procEntityRDN_0):
        return self.method_30(procEntityRDN_0.AhpCodeId, procEntityRDN_0.RwyDesig, procEntityRDN_0.RdnDesig);

    def method_32(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityFDN = ProcEntityFDN((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("FdnUid") or xmlNode_0)
        procEntityFDN1 = self.method_34(procEntityFDN);
        if (procEntityFDN1 != None):
            return procEntityFDN1;
        self.directions.append(procEntityFDN);
        return procEntityFDN;

    def method_33(self, string_0, string_1, string_2):
        for procEntityDirectionBase0 in self.directions:
            if not isinstance(procEntityDirectionBase0, ProcEntityRDN):
                continue
            if (not (procEntityDirectionBase0.AhpCodeId == string_0) or not (procEntityDirectionBase0.FdnDesig == string_2)):
                continue
            if procEntityDirectionBase0.FtoDesig == string_1:
                return procEntityDirectionBase0
        return None

    def method_34(self, procEntityFDN_0):
        return self.method_33(procEntityFDN_0.AhpCodeId, procEntityFDN_0.FtoDesig, procEntityFDN_0.FdnDesig);

    def method_35(self, ilist_0, procEntityAHP_0):
        ######------------  ilist_0 : ComboBoxPanel ------------#############
        ilist_0.Clear();
        for direction in self.directions:
            if (direction.AhpCodeId != procEntityAHP_0.AhpCodeId):
                continue;
            ilist_0.Add(direction);
            
    def method_36(self, xmlNode_0, procEntityParseNodeType_0):
        xmlNodes = None;
        procEntityIL = ProcEntityILS((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("IlsUid") or xmlNode_0);
        if (procEntityParseNodeType_0 == ProcEntityParseNodeType.Node):
            xmlNodes = xmlNode_0.namedItem("codeCat");
            if (not xmlNodes.isNull()):
                procEntityIL.TxtDesig = EnumHelper.Parse(CodeCatIlsAixm, xmlNodes.toElement().text())
            xmlNodes = xmlNode_0.namedItem("txtRmk");
            if (not xmlNodes.isNull()):
                procEntityIL.TxtRmk = xmlNodes.toElement().text();
        procEntityIL1 = self.method_38(procEntityIL);
        if (procEntityIL1 != None):
            return procEntityIL1;
        self.points.append(procEntityIL);
        return procEntityIL;

    def method_37(self, procEntityDirectionBase_0):
        for procEntityBase0 in self.points:
            if isinstance(procEntityBase0, ProcEntityILS):
                if isinstance(procEntityBase0.UidBase, ProcEntityRDN) and isinstance(procEntityDirectionBase_0, ProcEntityRDN):
                    uidBase = procEntityBase0.UidBase
                    procEntityRDN = procEntityDirectionBase_0
                    if (not (uidBase.AhpCodeId == procEntityRDN.AhpCodeId) or not (uidBase.RdnDesig == procEntityRDN.RdnDesig)):
                        continue
                    if uidBase.RwyDesig == procEntityRDN.RwyDesig:
                        return procEntityBase0
                if isinstance(procEntityBase0.UidBase, ProcEntityFDN) and isinstance(procEntityDirectionBase_0, ProcEntityFDN):
                    procEntityFDN = procEntityBase0.UidBase;
                    procEntityFDN1 = procEntityDirectionBase_0;
                    if (not (procEntityFDN.AhpCodeId == procEntityFDN1.AhpCodeId) or not (procEntityFDN.FdnDesig == procEntityFDN1.FdnDesig)):
                        continue
                    if procEntityFDN.FtoDesig == procEntityFDN1.FtoDesig:
                        return procEntityBase0

        return None

    def method_38(self, procEntityILS_0):
        return self.method_37(procEntityILS_0.UidBase);

    def method_39(self, xmlNode_0, procEntityParseNodeType_0):
        xmlNodes = None;
        procEntityML = ProcEntityMLS((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("MlsUid") or xmlNode_0);
        if (procEntityParseNodeType_0 == ProcEntityParseNodeType.Node):
            xmlNodes = xmlNode_0.namedItem("codeCat");
            if (not xmlNodes.isNull()):
                procEntityML.TxtDesig = EnumHelper.Parse(CodeCatIlsAixm, xmlNodes.toElement().text())
            xmlNodes = xmlNode_0.namedItem("txtRmk");
            if (not xmlNodes.isNull()):
                procEntityML.TxtRmk = xmlNodes.toElement().text();
        procEntityML1 = self.method_41(procEntityML);
        if (procEntityML1 != None):
            return procEntityML1;
        self.points.append(procEntityML);
        return procEntityML;

    def method_40(self, procEntityDirectionBase_0):
        for procEntityBase0 in self.points:
            if isinstance(procEntityBase0, ProcEntityMLS):
                if isinstance(procEntityBase0.UidBase, ProcEntityRDN) and isinstance(procEntityDirectionBase_0, ProcEntityRDN):
                    uidBase = procEntityBase0.UidBase
                    procEntityRDN = procEntityDirectionBase_0
                    if (not (uidBase.AhpCodeId == procEntityRDN.AhpCodeId) or not (uidBase.RdnDesig == procEntityRDN.RdnDesig)):
                        continue
                    if uidBase.RwyDesig == procEntityRDN.RwyDesig:
                        return procEntityBase0
                if isinstance(procEntityBase0.UidBase, ProcEntityFDN) and isinstance(procEntityDirectionBase_0, ProcEntityFDN):
                    procEntityFDN = procEntityBase0.UidBase;
                    procEntityFDN1 = procEntityDirectionBase_0;
                    if (not (procEntityFDN.AhpCodeId == procEntityFDN1.AhpCodeId) or not (procEntityFDN.FdnDesig == procEntityFDN1.FdnDesig)):
                        continue
                    if procEntityFDN.FtoDesig == procEntityFDN1.FtoDesig:
                        return procEntityBase0
        return None

    def method_41(self, procEntityMLS_0):
        return self.method_40(procEntityMLS_0.UidBase);

    def method_42(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityTLA = ProcEntityTLA((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("TlaUid") or xmlNode_0)
        procEntityTLA1 = self.method_44(procEntityTLA);
        if (procEntityTLA1 != None):
            return procEntityTLA1;
        self.points.append(procEntityTLA);
        return procEntityTLA;

    def method_43(self, string_0, string_1):
        for procEntityBase_0 in self.points:
            if (not isinstance(procEntityBase_0, ProcEntityTLA) or not (procEntityBase_0.CodeId == string_0)):
                continue
            if procEntityBase_0.TxtDesig == string_1:
                return procEntityBase_0
        return None

    def method_44(self, procEntityTLA_0):
        return self.method_43(procEntityTLA_0.CodeId, procEntityTLA_0.TxtDesig);

    def method_45(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityBase = None;
        xmlNodes = ((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("MgpUid") or xmlNode_0).namedItem("TcnUid");
        if (not xmlNodes.isNull()):
            procEntityBase = self.method_3(xmlNodes, ProcEntityParseNodeType.UidNode);
        if (procEntityBase == None):
            xmlNodes = xmlNode_0.namedItem("VorUid");
            if (not xmlNodes.isNull()):
                procEntityBase = self.method_0(xmlNodes, ProcEntityParseNodeType.UidNode);
        if (procEntityBase == None):
            xmlNodes = xmlNode_0.namedItem("DpnUid");
            if (not xmlNodes.isNull()):
                procEntityBase = self.method_53(xmlNodes, ProcEntityParseNodeType.UidNode);
        if (procEntityBase == None):
            xmlNodes = xmlNode_0.namedItem("NdbUid");
            if (not xmlNodes.isNull()):
                procEntityBase = self.method_9(xmlNodes, ProcEntityParseNodeType.UidNode);
        if (procEntityBase == None):
            xmlNodes = xmlNode_0.namedItem("DmeUid");
            if (not xmlNodes.isNull()):
                procEntityBase = self.method_6(xmlNodes, ProcEntityParseNodeType.UidNode);
        if (procEntityBase == None):
            xmlNodes = xmlNode_0.namedItem("MkrUid");
            if (not xmlNodes.isNull()):
                procEntityBase = self.method_12(xmlNodes, ProcEntityParseNodeType.UidNode);
        if (procEntityBase == None):
            return None;
        procEntityBase1 = self.method_46(procEntityBase);
        if (procEntityBase1 != None):
            return procEntityBase1;
        self.mgps.append(procEntityBase);
        return procEntityBase;

    def method_46(self, procEntityBase_0):
        for argument0 in self.mgps:
            if (not (argument0.__class__ == procEntityBase_0.__class__) or not (argument0.GeoLat == procEntityBase_0.GeoLat)):
                continue
            if argument0.GeoLong == procEntityBase_0.GeoLong:
                return argument0
        return None
    def method_47(self, ilist_0):
        ######------------  ilist_0 : ComboBoxPanel ------------#############
        ilist_0.Clear();
        ilist_0.Items = self.mgps

    def method_48(self, xmlNode_0, procEntityParseNodeType_0):
        procEntityAHP = ProcEntityAHP((procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("AhpUid") or xmlNode_0);
        if (procEntityParseNodeType_0 == ProcEntityParseNodeType.Node):
            xmlNodes = xmlNode_0.namedItem("txtName");
            if (not xmlNodes.isNull()):
                procEntityAHP.TxtName = xmlNodes.toElement().text();
            xmlNodes = xmlNode_0.namedItem("valMagVar");
            if (not xmlNodes.isNull()):
                procEntityAHP.ValMagVar = float(xmlNodes.toElement().text())
        procEntityAHP1 = self.method_50(procEntityAHP);
        if (procEntityAHP1 != None):
            return procEntityAHP1;
        self.aerodromes.append(procEntityAHP);
        return procEntityAHP;

    def method_49(self, string_0):
        for procEntityAHP_0 in self.aerodromes:
            if procEntityAHP_0.AhpCodeId == string_0:
                return procEntityAHP_0
        return None

    def method_50(self, procEntityAHP_0):
        return self.method_49(procEntityAHP_0.AhpCodeId);

    def method_51(self, ilist_0):
        ######------------  ilist_0 : ComboBoxPanel ------------#############
        ilist_0.Clear();
        ilist_0.Items = self.aerodromes

    def method_52(self, procEntityDPN_0):
        self.points.append(procEntityDPN_0);

    def method_53(self, xmlNode_0, procEntityParseNodeType_0):
        xmlNodes = (procEntityParseNodeType_0 == ProcEntityParseNodeType.Node) and xmlNode_0.namedItem("DpnUid") or xmlNode_0;
        procEntityDPN = ProcEntityDPN(xmlNodes.namedItem("codeId").toElement().text(), xmlNodes.namedItem("geoLat").toElement().text(), xmlNodes.namedItem("geoLong").toElement().text());
        if (procEntityParseNodeType_0 == ProcEntityParseNodeType.Node):
            xmlNodes1 = xmlNode_0.namedItem("TlaUid");
            if (not xmlNodes1.isNull()):
                procEntityDPN.Location = self.method_44(ProcEntityTLA(xmlNodes1));
            xmlNodes1 = xmlNode_0.namedItem("AhpUid");
            if (not xmlNodes1.isNull()):
                procEntityDPN.Location = self.method_50(ProcEntityAHP(xmlNodes1));
            xmlNodes1 = xmlNode_0.namedItem("AhpUidAssoc");
            if (not xmlNodes1.isNull()):
                procEntityDPN.Associated = self.method_50(ProcEntityAHP(xmlNodes1));
            xmlNodes1 = xmlNode_0.namedItem("RcpUid");
            if (not xmlNodes1.isNull()):
                procEntityDPN.Location = self.method_20(ProcEntityRCP(xmlNodes1));
            xmlNodes1 = xmlNode_0.namedItem("FcpUid");
            if (not xmlNodes1.isNull()):
                procEntityDPN.Location = self.method_23(ProcEntityFCP(xmlNodes1));
            xmlNodes1 = xmlNode_0.namedItem("codeType");
            procEntityDPN.CodeTypeDpn = EnumHelper.Parse(CodeTypeDesigPtAixm, xmlNodes1.toElement().text())
            xmlNodes1 = xmlNode_0.namedItem("txtName");
            if (not xmlNodes1.isNull()):
                procEntityDPN.TxtName = xmlNodes1.toElement().text();
            xmlNodes1 = xmlNode_0.namedItem("txtRmk");
            if (not xmlNodes1.isNull()):
                procEntityDPN.TxtRmk = xmlNodes1.toElement().text();
        procEntityDPN1 = self.method_58(procEntityDPN);
        if (procEntityDPN1 != None):
            return procEntityDPN1;
        self.points.append(procEntityDPN);
        return procEntityDPN;

    def method_54(self, string_0):
        resultList = []
        for procEntityBase_0 in self.points:
            if (not (procEntityBase_0.__class__ == ProcEntityDPN)):
                continue
            if procEntityBase_0.CodeId == string_0:
                resultList.append(procEntityBase_0)
        return resultList

    def method_55(self, string_0, procEntityAHP_0):
        resultList = []
        for procEntityBase_0 in self.points:
            if (not (procEntityBase_0.__class__ == ProcEntityDPN)):
                continue
            associated = procEntityBase_0.Associated;
            strS = (associated == None) and None or associated.AhpCodeId;
            if (procEntityBase_0.CodeId != string_0):
                continue
            if strS == procEntityAHP_0.AhpCodeId:
                resultList.append(procEntityBase_0)
        return resultList

    def method_56(self, string_0, string_1, string_2):
        for procEntityBase_0 in self.points:
            if (not (procEntityBase_0.__class__ == ProcEntityDPN) or not (procEntityBase_0.CodeId == string_0) or not (procEntityBase_0.GeoLat == string_1)):
                continue
            if procEntityBase_0.GeoLong == string_2:
                return procEntityBase_0
        return None

    def method_57(self, string_0, degrees_0, degrees_1):
        for procEntityBase_0 in self.points:
            if not isinstance(procEntityBase_0, ProcEntityDPN):
                continue
            degree = Degrees.smethod_15(procEntityBase_0.GeoLat, DegreesType.Latitude);
            degree1 = Degrees.smethod_15(procEntityBase_0.GeoLong, DegreesType.Longitude);
            if (not (procEntityBase_0.CodeId == string_0) or not degree.method_3(degrees_0)):
                continue;
            if degree1.method_3(degrees_1):
                return procEntityBase_0
        return None
    def method_58(self, procEntityDPN_0):
        return self.method_56(procEntityDPN_0.CodeId, procEntityDPN_0.GeoLat, procEntityDPN_0.GeoLong);
    def method_59(self, ilist_0, procEntityListType_0):
        ilist_0.Clear();
        if procEntityListType_0 == ProcEntityListType.Holding or procEntityListType_0 == ProcEntityListType.Fixes or procEntityListType_0 == ProcEntityListType.Centers:
            for point in self.points:
                if (not (isinstance(point, ProcEntityTCN)) and 
                        not (isinstance(point, ProcEntityVOR)) and 
                        not (isinstance(point, ProcEntityDPN)) and 
                        not (isinstance(point, ProcEntityNDB)) and 
                        not (isinstance(point, ProcEntityDME)) and 
                        not (isinstance(point, ProcEntityMKR))):
                    continue;
                ilist_0.Add(point);
            if (procEntityListType_0 != ProcEntityListType.Centers):
                return ;
            # ilist_0.Add("");
            return;
        elif procEntityListType_0 == ProcEntityListType.FixesEx or procEntityListType_0 == ProcEntityListType.CentersEx:
            for procEntityBase in self.points:
                if (not (isinstance(procEntityBase, ProcEntityVOR)) and 
                        not (isinstance(procEntityBase, ProcEntityTCN)) and 
                        not (isinstance(procEntityBase, ProcEntityNDB)) and 
                        not (isinstance(procEntityBase, ProcEntityDME)) and 
                        not (isinstance(procEntityBase, ProcEntityMKR)) and 
                        not (isinstance(procEntityBase, ProcEntityDPN)) and 
                        not (isinstance(procEntityBase, ProcEntityPCP)) and 
                        not (isinstance(procEntityBase, ProcEntityRCP))):
                    continue;
                ilist_0.Add(procEntityBase);
            if (procEntityListType_0 != ProcEntityListType.CentersEx):
                return;
            # ilist_0.Add("");
            return;
        elif procEntityListType_0 == ProcEntityListType.RecommendedNavAids:
            for point1 in self.points:
                if (not (isinstance(point1, ProcEntitySNY)) and 
                        not (isinstance(point1, ProcEntityILS)) and 
                        not (isinstance(point1, ProcEntityMLS)) and 
                        not (isinstance(point1, ProcEntityDME)) and 
                        not (isinstance(point1, ProcEntityNDB)) and 
                        not (isinstance(point1, ProcEntityVOR)) and 
                        not (isinstance(point1, ProcEntityTCN))):
                    continue;
                ilist_0.Add(point1);
            # ilist_0.Add("");
            return;
        elif procEntityListType_0 == ProcEntityListType.VORs:
            for procEntityBase1 in self.points:
                if not (isinstance(procEntityBase1, ProcEntityVOR)):
                    continue;
                ilist_0.Add(procEntityBase1);
            # ilist_0.Add("");
            return;
        elif procEntityListType_0 == ProcEntityListType.DMEs:
            for point2 in self.points:
                if not (isinstance(point2, ProcEntityDME)):
                    continue;
                ilist_0.Add(point2);
            # ilist_0.Add("");
            return;
        elif procEntityListType_0 == ProcEntityListType.AHPs:
            for aerodrome in self.aerodromes:
                if not (isinstance(aerodrome, ProcEntityAHP)):
                    continue;
                ilist_0.Add(aerodrome);
            # ilist_0.Add("");
            return;
        elif procEntityListType_0 == ProcEntityListType.LocationsDPN:
            for procEntityBase2 in self.points:
                if (not (isinstance(procEntityBase2, ProcEntityTLA)) and
                        not (isinstance(procEntityBase2, ProcEntityRCP)) and
                        not (isinstance(procEntityBase2, ProcEntityFCP))):
                    continue;
                ilist_0.Add(procEntityBase2);
            for procEntityAHP in self.aerodromes:
                ilist_0.Add(procEntityAHP);
            # ilist_0.Add("");
            return ;
        
    def method_60(self, list_0, procEntityListType_0, string_0, string_1):
        # string_0 = "581342.0N"
        # string_1 = "0223055.3E"

        if procEntityListType_0 == ProcEntityListType.Holding or procEntityListType_0 == ProcEntityListType.Fixes or procEntityListType_0 == ProcEntityListType.Centers:
            for current in self.points:
                if (not (current.__class__ == ProcEntityTCN) and not (current.__class__ == ProcEntityVOR) and not (current.__class__ == ProcEntityDPN) and not (current.__class__ == ProcEntityNDB) and not (current.__class__ == ProcEntityDME) and not (current.__class__ == ProcEntityMKR) or not (current.GeoLat == string_0) or not (current.GeoLong == string_1)):
                    continue;
                list_0.append(current);
        elif procEntityListType_0 == ProcEntityListType.FixesEx or procEntityListType_0 == ProcEntityListType.CentersEx:
            for procEntityBase in self.points:
                if (not (procEntityBase.__class__ == ProcEntityVOR) and not (procEntityBase.__class__ == ProcEntityTCN) and not (procEntityBase.__class__ == ProcEntityNDB) and not (procEntityBase.__class__ == ProcEntityDME) and not (procEntityBase.__class__ == ProcEntityMKR) and not (procEntityBase.__class__ == ProcEntityDPN) and not (procEntityBase.__class__ == ProcEntityPCP) and not (procEntityBase.__class__ == ProcEntityRCP) or not (procEntityBase.GeoLat == string_0) or not (procEntityBase.GeoLong == string_1)):
                    continue;
                list_0.append(procEntityBase);
        elif procEntityListType_0 == ProcEntityListType.RecommendedNavAids:
            for current1 in self.points:
                if (not (current1.__class__ == ProcEntitySNY) and not (current1.__class__ == ProcEntityILS) and not (current1.__class__ == ProcEntityMLS) and not (current1.__class__ == ProcEntityDME) and not (current1.__class__ == ProcEntityNDB) and not (current1.__class__ == ProcEntityVOR) and not (current1.__class__ == ProcEntityTCN) or not (current1.GeoLat == string_0) or not (current1.GeoLong == string_1)):
                    continue;
                list_0.append(current1);
        elif procEntityListType_0 == ProcEntityListType.VORs:
            for procEntityBase1 in self.points:
                if (not (procEntityBase1.__class__ == ProcEntityVOR) or not (procEntityBase1.GeoLat == string_0) or not (procEntityBase1.GeoLong == string_1)):
                    continue;
                list_0.append(procEntityBase1);
        elif procEntityListType_0 == ProcEntityListType.DMEs:
            for current2 in self.points:
                if (not (current2.__class__ == ProcEntityDME) or not (current2.GeoLat == string_0) or not (current2.GeoLong == string_1)):
                    continue;
                list_0.append(current2);
        elif procEntityListType_0 == ProcEntityListType.AHPs:
            for procEntityBase2 in self.points:
                if (not (procEntityBase2.__class__ == ProcEntityAHP) or not (procEntityBase2.GeoLat == string_0) or not (procEntityBase2.GeoLong == string_1)):
                    continue;
                list_0.append(procEntityBase2);
        elif procEntityListType_0 == ProcEntityListType.LocationsDPN:
            for point in self.points:
                if (not (point.__class__ == ProcEntityTLA) and not (point.__class__ == ProcEntityAHP) and not (point.__class__ == ProcEntityRCP) and not (point.__class__ == ProcEntityFCP) or not (point.GeoLat == string_0) or not (point.GeoLong == string_1)):
                    continue;
                list_0.append(point);
            for procEntityAHP in self.aerodromes:
                if (not (procEntityAHP.GeoLat == string_0) or not (procEntityAHP.GeoLong == string_1)):
                    continue;
                list_0.append(procEntityAHP);
        else:
            return;

    def method_61(self, xmlNode_0, list_0):
        if (list_0 == None or len(list_0) == 0):
            return;
        for list0 in list_0:
            xmlNodes = XmlNode.smethod_29(xmlNode_0, "New");
            if (not (list0.__class__ == ProcEntityDPN)):
                if (not (list0.__class__ == ProcEntityPCP)):
                    continue;
                list0.__class__ = ProcEntityPCP;
                procEntityPCP = list0
                xmlNodes1 = XmlNode.smethod_29(xmlNodes, "Pcp");
                xmlNodes2 = XmlNode.smethod_29(xmlNodes1, "PcpUid");
                if (not String.IsNullOrEmpty(procEntityPCP.TxtDesig)):
                    XmlNode.smethod_30(xmlNodes2, "txtDesig", procEntityPCP.TxtDesig);
                XmlNode.smethod_30(xmlNodes2, "geoLat", procEntityPCP.GeoLat);
                XmlNode.smethod_30(xmlNodes2, "geoLong", procEntityPCP.GeoLong);
                if (not String.IsNullOrEmpty(procEntityPCP.CodeType)):
                    XmlNode.smethod_30(xmlNodes1, "codeType", procEntityPCP.CodeType);
                if (String.IsNullOrEmpty(procEntityPCP.TxtRmk)):
                    continue;
                XmlNode.smethod_30(xmlNodes1, "txtRmk", procEntityPCP.TxtRmk);
            else:
                list0.__class__ = ProcEntityDPN
                procEntityDPN = list0
                xmlNodes3 = XmlNode.smethod_29(xmlNodes, "Dpn");
                xmlNodes4 = XmlNode.smethod_29(xmlNodes3, "DpnUid");
                XmlNode.smethod_30(xmlNodes4, "codeId", procEntityDPN.CodeId);
                XmlNode.smethod_30(xmlNodes4, "geoLat", procEntityDPN.GeoLat);
                XmlNode.smethod_30(xmlNodes4, "geoLong", procEntityDPN.GeoLong);
                if (procEntityDPN.Location != None):
                    self.method_69(xmlNodes3, "Uid", procEntityDPN.Location);
                elif (procEntityDPN.Associated != None):
                    self.method_69(xmlNodes3, "UidAssoc", procEntityDPN.Associated);
                XmlNode.smethod_30(xmlNodes3, "codeDatum", "WGE");
                XmlNode.smethod_30(xmlNodes3, "codeType", procEntityDPN.CodeTypeDpn);
                if (not String.IsNullOrEmpty(procEntityDPN.TxtName)):
                    XmlNode.smethod_30(xmlNodes3, "txtName", procEntityDPN.CodeType);
                if (String.IsNullOrEmpty(procEntityDPN.TxtRmk)):
                    continue;
                XmlNode.smethod_30(xmlNodes3, "txtRmk", procEntityDPN.TxtRmk);

    def method_62(self, xmlNode_0, dataRow_0, dataBaseProcedureExportType_0):
        if (dataRow_0 == None or len(dataRow_0) == 0):
            return;
        dataRow0 = dataRow_0;
        for i in range(len(dataRow0)):
            dataRow = dataRow0[i];
            xmlNodes = None;
            if (dataBaseProcedureExportType_0 != DataBaseProcedureExportType.Deleted):
                if (dataBaseProcedureExportType_0 != DataBaseProcedureExportType.Updated):
                    xmlNodes = XmlNode.smethod_29(xmlNode_0, "New");
                else:
                    xmlNodes = XmlNode.smethod_29(xmlNode_0, "Changed");
                    num = 0;
                    while (num < 4):
                        strN = None
                        strN4 = None
                        if dataRow[dataRow.nameList[num]].__class__ == str or dataRow[dataRow.nameList[num]].__class__ == QString:
                            strN = dataRow[dataRow.nameList[num]]
                        elif dataRow[dataRow.nameList[num]].__class__ == int or dataRow[dataRow.nameList[num]].__class__ == float:
                            strN = str(dataRow[dataRow.nameList[num]])
                        else:
                            strN = dataRow[dataRow.nameList[num]].ToString()
                        if dataRow[dataRow.nameList[num + 4]].__class__ == str or dataRow[dataRow.nameList[num + 4]].__class__ == QString:
                            strN4 = dataRow[dataRow.nameList[num + 4]]
                        elif dataRow[dataRow.nameList[num + 4]].__class__ == int or dataRow[dataRow.nameList[num + 4]].__class__ == float:
                            strN4 = str(dataRow[dataRow.nameList[num + 4]])
                        else:
                            strN4 = dataRow[dataRow.nameList[num + 4]].ToString()    
                            
                        if (strN != strN4):
                            xmlNodes1 = XmlNode.smethod_29(xmlNodes, "SidUid");
                            self.method_66(xmlNodes1, dataRow["oldAhpEnt"]);
                            XmlNode.smethod_30(xmlNodes1, "txtDesig", dataRow["oldTxtDesig"]);
                            if (dataRow["oldCodeCatAcft"] != None):
                                XmlNode.smethod_30(xmlNodes1, "codeCatAcft", dataRow["oldCodeCatAcft"]);
                            if (dataRow["oldCodeTransId"] == None):
                                break
                            XmlNode.smethod_30(xmlNodes1, "codeTransId", dataRow["oldCodeTransId"]);
                            break
                        else:
                            num += 1;
                xmlNodes2 = XmlNode.smethod_29(xmlNodes, "Sid");
                xmlNodes3 = XmlNode.smethod_29(xmlNodes2, "SidUid");
                self.method_66(xmlNodes3, dataRow["ahpEnt"]);
                XmlNode.smethod_30(xmlNodes3, "txtDesig", dataRow["txtDesig"]);
                if (dataRow["codeCatAcft"] != None):
                    XmlNode.smethod_30(xmlNodes3, "codeCatAcft", dataRow["codeCatAcft"]);
                if (dataRow["codeTransId"] != None):
                    XmlNode.smethod_30(xmlNodes3, "codeTransId", dataRow["codeTransId"]);
                if (dataRow["rdnEnt"] != None):
                    self.method_67(xmlNodes2, dataRow["rdnEnt"]);
                if (dataRow["mgpEnt"] != None):
                    self.method_68(xmlNodes2, dataRow["mgpEnt"]);
                if (dataRow["codeRnp"] != None):
                    try:
                        num1 = float(dataRow["codeRnp"]);
                    except:
                        num1 = 0
                    XmlNode.smethod_30(xmlNodes2, "codeRnp", str(num1));
                if (dataRow["txtDescrComFail"] != None):
                    XmlNode.smethod_30(xmlNodes2, "txtDescrComFail", dataRow["txtDescrComFail"]);
                if (dataRow["codeTypeRte"] != None):
                    XmlNode.smethod_30(xmlNodes2, "codeTypeRte", dataRow["codeTypeRte"]);
                if (dataRow["txtDescr"] != None):
                    XmlNode.smethod_30(xmlNodes2, "txtDescr", dataRow["txtDescr"]);
                if (dataRow["txtRmk"] != None):
                    XmlNode.smethod_30(xmlNodes2, "txtRmk", dataRow["txtRmk"]);
                if (dataRow["procLegs"] != None):
                    self.method_71(xmlNodes2, dataRow["procLegs"]);
                if (dataRow["procLegsEx"] != None):
                    self.method_72(xmlNodes2, dataRow["procLegsEx"]);
            else:
                xmlNodes = XmlNode.smethod_29(xmlNode_0, "Withdrawn");
                xmlNodes4 = XmlNode.smethod_29(xmlNodes, "SidUid");
                self.method_66(xmlNodes4, dataRow["oldAhpEnt"]);
                XmlNode.smethod_30(xmlNodes4, "txtDesig", dataRow["oldTxtDesig"]);
                if (dataRow["oldCodeCatAcft"] != None):
                    XmlNode.smethod_30(xmlNodes4, "codeCatAcft", dataRow["oldCodeCatAcft"]);
                if (dataRow["oldCodeTransId"] != None):
                    XmlNode.smethod_30(xmlNodes4, "codeTransId", dataRow["oldCodeTransId"]);
                    
    def method_63(self, xmlNode_0, dataRow_0, dataBaseProcedureExportType_0):
        if (dataRow_0 == None or len(dataRow_0) == 0):
            return;
        dataRow0 = dataRow_0;
        for i in range(len(dataRow0)):
            dataRow = dataRow0[i];
            xmlNodes = None;
            if (dataBaseProcedureExportType_0 != DataBaseProcedureExportType.Deleted):
                if (dataBaseProcedureExportType_0 != DataBaseProcedureExportType.Updated):
                    xmlNodes = XmlNode.smethod_29(xmlNode_0, "New");
                else:
                    xmlNodes = XmlNode.smethod_29(xmlNode_0, "Changed");
                    num = 0;
                    while (num < 4):
                        strN = None
                        strN4 = None
                        if dataRow[dataRow.nameList[num]].__class__ == str or dataRow[dataRow.nameList[num]].__class__ == QString:
                            strN = dataRow[dataRow.nameList[num]]
                        elif dataRow[dataRow.nameList[num]].__class__ == int or dataRow[dataRow.nameList[num]].__class__ == float:
                            strN = str(dataRow[dataRow.nameList[num]])
                        else:
                            strN = dataRow[dataRow.nameList[num]].ToString()
                        if dataRow[dataRow.nameList[num + 4]].__class__ == str or dataRow[dataRow.nameList[num + 4]].__class__ == QString:
                            strN4 = dataRow[dataRow.nameList[num + 4]]
                        elif dataRow[dataRow.nameList[num + 4]].__class__ == int or dataRow[dataRow.nameList[num + 4]].__class__ == float:
                            strN4 = str(dataRow[dataRow.nameList[num + 4]])
                        else:
                            strN4 = dataRow[dataRow.nameList[num + 4]].ToString()   
                        if (strN != strN4):
                            xmlNodes1 = XmlNode.smethod_29(xmlNodes, "SiaUid");
                            self.method_66(xmlNodes1, dataRow["oldAhpEnt"]);
                            XmlNode.smethod_30(xmlNodes1, "txtDesig", dataRow["oldTxtDesig"]);
                            if (dataRow["oldCodeCatAcft"] != None):
                                XmlNode.smethod_30(xmlNodes1, "codeCatAcft", dataRow["oldCodeCatAcft"]);
                            if (dataRow["oldCodeTransId"] == None):
                                break
                            XmlNode.smethod_30(xmlNodes1, "codeTransId", dataRow["oldCodeTransId"]);
                            break
                        else:
                            num += 1;
            # Label0:
                xmlNodes2 = XmlNode.smethod_29(xmlNodes, "Sia");
                xmlNodes3 = XmlNode.smethod_29(xmlNodes2, "SiaUid");
                self.method_66(xmlNodes3, dataRow["ahpEnt"]);
                XmlNode.smethod_30(xmlNodes3, "txtDesig", dataRow["txtDesig"]);
                if (dataRow["codeCatAcft"] != None):
                    XmlNode.smethod_30(xmlNodes3, "codeCatAcft", dataRow["codeCatAcft"]);
                if (dataRow["codeTransId"] != None):
                    XmlNode.smethod_30(xmlNodes3, "codeTransId", dataRow["codeTransId"]);
                if (dataRow["mgpEnt"] != None):
                    self.method_68(xmlNodes2, dataRow["mgpEnt"]);
                if (dataRow["codeRnp"] != None):
                    num1 = float(dataRow["codeRnp"]);
                    XmlNode.smethod_30(xmlNodes2, "codeRnp", str(num1));
                if (dataRow["txtDescrComFail"] != None):
                    XmlNode.smethod_30(xmlNodes2, "txtDescrComFail", dataRow["txtDescrComFail"]);
                if (dataRow["codeTypeRte"] != None):
                    XmlNode.smethod_30(xmlNodes2, "codeTypeRte", dataRow["codeTypeRte"]);
                if (dataRow["txtDescr"] != None):
                    XmlNode.smethod_30(xmlNodes2, "txtDescr", dataRow["txtDescr"]);
                if (dataRow["txtRmk"] != None):
                    XmlNode.smethod_30(xmlNodes2, "txtRmk", dataRow["txtRmk"]);
                if (dataRow["procLegs"] != None):
                    self.method_71(xmlNodes2, dataRow["procLegs"]);
                if (dataRow["procLegsEx"] != None):
                    self.method_72(xmlNodes2, dataRow["procLegsEx"]);
            else:
                xmlNodes = XmlNode.smethod_29(xmlNode_0, "Withdrawn");
                xmlNodes4 = XmlNode.smethod_29(xmlNodes, "SiaUid");
                self.method_66(xmlNodes4, dataRow["oldAhpEnt"]);
                XmlNode.smethod_30(xmlNodes4, "txtDesig", dataRow["oldTxtDesig"]);
                if (dataRow["oldCodeCatAcft"] != None):
                    XmlNode.smethod_30(xmlNodes4, "codeCatAcft", dataRow["oldCodeCatAcft"]);
                if (dataRow["oldCodeTransId"] != None):
                    XmlNode.smethod_30(xmlNodes4, "codeTransId", dataRow["oldCodeTransId"]);
                    
    def method_64(self, xmlNode_0, dataRow_0, dataBaseProcedureExportType_0):
        if (dataRow_0 == None or len(dataRow_0) == 0):
            return;
        dataRow0 = dataRow_0;
        for i in range(len(dataRow0)):
            dataRow = dataRow0[i];
            xmlNodes = None;
            if (dataBaseProcedureExportType_0 != DataBaseProcedureExportType.Deleted):
                if (dataBaseProcedureExportType_0 != DataBaseProcedureExportType.Updated):
                    xmlNodes = XmlNode.smethod_29(xmlNode_0, "New");
                else:
                    xmlNodes = XmlNode.smethod_29(xmlNode_0, "Changed");
                    num = 0;
                    while (num < 4):
                        strN = None
                        strN4 = None
                        if dataRow[dataRow.nameList[num]].__class__ == str or dataRow[dataRow.nameList[num]].__class__ == QString:
                            strN = dataRow[dataRow.nameList[num]]
                        elif dataRow[dataRow.nameList[num]].__class__ == int or dataRow[dataRow.nameList[num]].__class__ == float:
                            strN = str(dataRow[dataRow.nameList[num]])
                        else:
                            strN = dataRow[dataRow.nameList[num]].ToString()
                        if dataRow[dataRow.nameList[num + 4]].__class__ == str or dataRow[dataRow.nameList[num + 4]].__class__ == QString:
                            strN4 = dataRow[dataRow.nameList[num + 4]]
                        elif dataRow[dataRow.nameList[num + 4]].__class__ == int or dataRow[dataRow.nameList[num + 4]].__class__ == float:
                            strN4 = str(dataRow[dataRow.nameList[num + 4]])
                        else:
                            strN4 = dataRow[dataRow.nameList[num + 4]].ToString()
                        if (strN != strN4):
                            xmlNodes1 = XmlNode.smethod_29(xmlNodes, "IapUid");
                            self.method_66(xmlNodes1, dataRow["oldAhpEnt"]);
                            XmlNode.smethod_30(xmlNodes1, "txtDesig", dataRow["oldTxtDesig"]);
                            if (dataRow["oldCodeCatAcft"] != None):
                                XmlNode.smethod_30(xmlNodes1, "codeCatAcft", dataRow["oldCodeCatAcft"]);
                            if (dataRow["oldCodeTransId"] == None):
                                break
                            XmlNode.smethod_30(xmlNodes1, "codeTransId", dataRow["oldCodeTransId"]);
                            break
                        else:
                            num += 1;
            # Label0:
                xmlNodes2 = XmlNode.smethod_29(xmlNodes, "Iap");
                xmlNodes3 = XmlNode.smethod_29(xmlNodes2, "IapUid");
                self.method_66(xmlNodes3, dataRow["ahpEnt"]);
                XmlNode.smethod_30(xmlNodes3, "txtDesig", dataRow["txtDesig"]);
                if (dataRow["codeCatAcft"] != None):
                    XmlNode.smethod_30(xmlNodes3, "codeCatAcft", dataRow["codeCatAcft"]);
                if (dataRow["codeTransId"] != None):
                    XmlNode.smethod_30(xmlNodes3, "codeTransId", dataRow["codeTransId"]);
                if (dataRow["rdnEnt"] != None):
                    self.method_67(xmlNodes2, dataRow["rdnEnt"]);
                if (dataRow["mgpEnt"] != None):
                    self.method_68(xmlNodes2, dataRow["mgpEnt"]);
                if (dataRow["codeRnp"] != None):
                    num1 = float(dataRow["codeRnp"]);
                    XmlNode.smethod_30(xmlNodes2, "codeRnp", str(num1));
                if (dataRow["txtDescrComFail"] != None):
                    XmlNode.smethod_30(xmlNodes2, "txtDescrComFail", dataRow["txtDescrComFail"]);
                if (dataRow["codeTypeRte"] != None):
                    XmlNode.smethod_30(xmlNodes2, "codeTypeRte", dataRow["codeTypeRte"]);
                if (dataRow["txtDescrMiss"] != None):
                    XmlNode.smethod_30(xmlNodes2, "txtDescrMiss", dataRow["txtDescrMiss"]);
                if (dataRow["txtRmk"] != None):
                    XmlNode.smethod_30(xmlNodes2, "txtRmk", dataRow["txtRmk"]);
                if (dataRow["ocah"] != None):
                    self.method_70(xmlNodes2, dataRow["ocah"]);
                if (dataRow["procLegs"] != None):
                    self.method_71(xmlNodes2, dataRow["procLegs"]);
                if (dataRow["procLegsEx"] != None):
                    self.method_72(xmlNodes2, dataRow["procLegsEx"]);
            else:
                xmlNodes = XmlNode.smethod_29(xmlNode_0, "Withdrawn");
                xmlNodes4 = XmlNode.smethod_29(xmlNodes, "IapUid");
                self.method_66(xmlNodes4, dataRow["oldAhpEnt"]);
                XmlNode.smethod_30(xmlNodes4, "txtDesig", dataRow["oldTxtDesig"]);
                if (dataRow["oldCodeCatAcft"] != None):
                    XmlNode.smethod_30(xmlNodes4, "codeCatAcft", dataRow["oldCodeCatAcft"]);
                if (dataRow["oldCodeTransId"] != None):
                    XmlNode.smethod_30(xmlNodes4, "codeTransId", dataRow["oldCodeTransId"]);
                    
    def method_65(self, xmlNode_0, dataRow_0, dataBaseProcedureExportType_0):
        if (dataRow_0 == None or len(dataRow_0) == 0):
            return;
        dataRow0 = dataRow_0;
        for i in range(len(dataRow0)):
            dataRow = dataRow0[i];
            xmlNodes = None;
            if (dataBaseProcedureExportType_0 != DataBaseProcedureExportType.Deleted):
                if (dataBaseProcedureExportType_0 != DataBaseProcedureExportType.Updated):
                    xmlNodes = XmlNode.smethod_29(xmlNode_0, "New");
                else:
                    xmlNodes = XmlNode.smethod_29(xmlNode_0, "Changed");
                    num = 0;
                    while (num < 2):
                        strN = None
                        strN2 = None
                        if dataRow[dataRow.nameList[num]].__class__ == str or dataRow[dataRow.nameList[num]].__class__ == QString:
                            strN = dataRow[dataRow.nameList[num]]
                        elif dataRow[dataRow.nameList[num]].__class__ == int or dataRow[dataRow.nameList[num]].__class__ == float:
                            strN = str(dataRow[dataRow.nameList[num]])
                        else:
                            strN = dataRow[dataRow.nameList[num]].ToString()
                        if dataRow[dataRow.nameList[num + 2]].__class__ == str or dataRow[dataRow.nameList[num + 2]].__class__ == QString:
                            strN2 = dataRow[dataRow.nameList[num + 2]]
                        elif dataRow[dataRow.nameList[num + 2]].__class__ == int or dataRow[dataRow.nameList[num + 2]].__class__ == float:
                            strN2 = str(dataRow[dataRow.nameList[num + 2]])
                        else:
                            strN2 = dataRow[dataRow.nameList[num + 2]].ToString()
                        if (strN != strN2):
                            xmlNodes1 = XmlNode.smethod_29(xmlNodes, "HpeUid");
                            self.method_69(xmlNodes1, "UidSpn", dataRow["oldBasedOnEnt"]);
                            XmlNode.smethod_30(xmlNodes1, "codeType", dataRow["oldCodeType"]);
                            break
                        else:
                            num += 1;
            # Label0:
                xmlNodes2 = XmlNode.smethod_29(xmlNodes, "Hpe");
                xmlNodes3 = XmlNode.smethod_29(xmlNodes2, "HpeUid");
                self.method_69(xmlNodes3, "UidSpn", dataRow["basedOnEnt"]);
                XmlNode.smethod_30(xmlNodes3, "codeType", dataRow["codeType"]);
                if (dataRow["txtDescr"] != None):
                    XmlNode.smethod_30(xmlNodes2, "txtDescr", dataRow["txtDescr"]);
                if (dataRow["txtRmk"] != None):
                    XmlNode.smethod_30(xmlNodes2, "txtRmk", dataRow["txtRmk"]);
                if (dataRow["procLegs"] != None):
                    self.method_71(xmlNodes2, dataRow["procLegs"]);
                if (dataRow["procLegsEx"] != None):
                    self.method_72(xmlNodes2, dataRow["procLegsEx"]);
            else:
                xmlNodes = XmlNode.smethod_29(xmlNode_0, "Withdrawn");
                xmlNodes4 = xmlNodes.smethod_29("HpeUid");
                self.method_69(xmlNodes4, "UidSpn", dataRow["oldBasedOnEnt"]);
                XmlNode.smethod_30(xmlNodes4, "codeType", dataRow["oldCodeType"]);
                
    def method_66(self, xmlNode_0, procEntityAHP_0):
        xmlNodes = XmlNode.smethod_29(xmlNode_0, "AhpUid");
        XmlNode.smethod_30(xmlNodes, "codeId", procEntityAHP_0.AhpCodeId);
        
    def method_67(self, xmlNode_0, procEntityDirectionBase_0):
        if (procEntityDirectionBase_0.__class__ == ProcEntityRDN):
            procEntityDirectionBase0 = procEntityDirectionBase_0;
            xmlNodes = XmlNode.smethod_29(xmlNode_0, "RdnUid");
            xmlNodes1 = XmlNode.smethod_29(xmlNodes, "RwyUid");
            xmlNodes2 = XmlNode.smethod_29(xmlNodes1, "AhpUid");
            XmlNode.smethod_30(xmlNodes2, "codeId", procEntityDirectionBase0.AhpCodeId);
            XmlNode.smethod_30(xmlNodes1, "txtDesig", procEntityDirectionBase0.RwyDesig);
            XmlNode.smethod_30(xmlNodes, "txtDesig", procEntityDirectionBase0.RdnDesig);
            return;
        procEntityFDN = procEntityDirectionBase_0;
        xmlNodes3 = XmlNode.smethod_29(xmlNode_0, "FdnUid");
        xmlNodes4 = XmlNode.smethod_29(xmlNodes3, "FtoUid");
        xmlNodes5 = XmlNode.smethod_29(xmlNodes4, "AhpUid");
        XmlNode.smethod_30(xmlNodes5, "codeId", procEntityFDN.AhpCodeId);
        XmlNode.smethod_30(xmlNodes4, "txtDesig", procEntityFDN.FtoDesig);
        XmlNode.smethod_30(xmlNodes3, "txtDesig", procEntityFDN.FdnDesig);
        
    def method_68(self, xmlNode_0, procEntityBase_0):
        self.method_69(XmlNode.smethod_29(xmlNode_0, "MgpUid"), "Uid", procEntityBase_0);
        
    def method_69(self, xmlNode_0, string_0, procEntityBase_0):
        strS = String.Concat([procEntityBase_0.Type, string_0]);
        xmlNodes = XmlNode.smethod_29(xmlNode_0, strS);
        if (procEntityBase_0.__class__ == ProcEntityPCP):
            if (not String.IsNullOrEmpty(procEntityBase_0.TxtDesig)):
                XmlNode.smethod_30(xmlNodes, "txtDesig", procEntityBase_0.TxtDesig);
            XmlNode.smethod_30(xmlNodes, "geoLat", procEntityBase_0.GeoLat);
            XmlNode.smethod_30(xmlNodes, "geoLong", procEntityBase_0.GeoLong);
            return;
        if (procEntityBase_0.__class__ == ProcEntityRCP):
            xmlNodes1 = XmlNode.smethod_29(xmlNodes, "RwyUid");
            xmlNodes2 = XmlNode.smethod_29(xmlNodes1, "AhpUid");
            XmlNode.smethod_30(xmlNodes2, "codeId", procEntityBase_0.CodeId);
            XmlNode.smethod_30(xmlNodes1, "txtDesig", procEntityBase_0.TxtDesig);
            XmlNode.smethod_30(xmlNodes, "geoLat", procEntityBase_0.GeoLat);
            XmlNode.smethod_30(xmlNodes, "geoLong", procEntityBase_0.GeoLong);
            return;
        if (procEntityBase_0.__class__ == ProcEntityFCP):
            xmlNodes3 = XmlNode.smethod_29(xmlNodes, "FtoUid");
            xmlNodes4 = XmlNode.smethod_29(xmlNodes3, "AhpUid");
            XmlNode.smethod_30(xmlNodes4, "codeId", procEntityBase_0.CodeId);
            XmlNode.smethod_30(xmlNodes3, "txtDesig", procEntityBase_0.TxtDesig);
            XmlNode.smethod_30(xmlNodes, "geoLat", procEntityBase_0.GeoLat);
            XmlNode.smethod_30(xmlNodes, "geoLong", procEntityBase_0.GeoLong);
            return;
        if (procEntityBase_0.__class__ == ProcEntitySNY):
            XmlNode.smethod_30(xmlNodes, "codeType", procEntityBase_0.CodeType);
            XmlNode.smethod_30(xmlNodes, "codeId", procEntityBase_0.CodeId);
            return;
        if (procEntityBase_0.__class__ == ProcEntityILS):
            procEntityBase0 = procEntityBase_0;
            if (procEntityBase0.UidBase.__class__ == ProcEntityRDN):
                uidBase = procEntityBase0.UidBase;
                xmlNodes5 = XmlNode.smethod_29(xmlNodes, "RdnUid");
                xmlNodes6 = XmlNode.smethod_29(xmlNodes5, "RwyUid");
                xmlNodes7 = XmlNode.smethod_29(xmlNodes6, "AhpUid");
                XmlNode.smethod_30(xmlNodes7, "codeId", uidBase.AhpCodeId);
                XmlNode.smethod_30(xmlNodes6, "txtDesig", uidBase.RwyDesig);
                XmlNode.smethod_30(xmlNodes5, "txtDesig", uidBase.RdnDesig);
                return;
            procEntityFDN = procEntityBase0.UidBase;
            xmlNodes8 = XmlNode.smethod_29(xmlNodes, "FdnUid");
            xmlNodes9 = XmlNode.smethod_29(xmlNodes8, "FtoUid");
            xmlNodes10 = XmlNode.smethod_29(xmlNodes9, "AhpUid");
            XmlNode.smethod_30(xmlNodes10, "codeId", procEntityFDN.AhpCodeId);
            XmlNode.smethod_30(xmlNodes9, "txtDesig", procEntityFDN.FtoDesig);
            XmlNode.smethod_30(xmlNodes8, "txtDesig", procEntityFDN.FdnDesig);
            return;
        if (not (procEntityBase_0.__class__ == ProcEntityMLS)):
            if (not String.IsNullOrEmpty(procEntityBase_0.CodeId)):
                XmlNode.smethod_30(xmlNodes, "codeId", procEntityBase_0.CodeId);
            XmlNode.smethod_30(xmlNodes, "geoLat", procEntityBase_0.GeoLat);
            XmlNode.smethod_30(xmlNodes, "geoLong", procEntityBase_0.GeoLong);
            return;
        procEntityML = procEntityBase_0;
        if (procEntityML.UidBase.__class__ == ProcEntityRDN):
            procEntityRDN = procEntityML.UidBase;
            xmlNodes11 = XmlNode.smethod_29(xmlNodes, "RdnUid");
            xmlNodes12 = XmlNode.smethod_29(xmlNodes11, "RwyUid");
            xmlNodes13 = XmlNode.smethod_29(xmlNodes12, "AhpUid");
            XmlNode.smethod_30(xmlNodes13, "codeId", procEntityRDN.AhpCodeId);
            XmlNode.smethod_30(xmlNodes12, "txtDesig", procEntityRDN.RwyDesig);
            XmlNode.smethod_30(xmlNodes11, "txtDesig", procEntityRDN.RdnDesig);
            return;
        uidBase1 = procEntityML.UidBase;
        xmlNodes14 = XmlNode.smethod_29(xmlNodes, "FdnUid");
        xmlNodes15 = XmlNode.smethod_29(xmlNodes14, "FtoUid");
        xmlNodes16 = XmlNode.smethod_29(xmlNodes15, "AhpUid");
        XmlNode.smethod_30(xmlNodes16, "codeId", uidBase1.AhpCodeId);
        XmlNode.smethod_30(xmlNodes15, "txtDesig", uidBase1.FtoDesig);
        XmlNode.smethod_30(xmlNodes14, "txtDesig", uidBase1.FdnDesig);


    def method_70(self, xmlNode_0, dataBaseIapOcaOchs_0):
        for dataBaseIapOcaOchs0 in dataBaseIapOcaOchs_0:
            strS = None;
            xmlNodes = XmlNode.smethod_29(xmlNode_0, "Ooh");
            XmlNode.smethod_30(xmlNodes, "codeCatAcft", dataBaseIapOcaOchs0.CodeCatAcft.ToString());
            XmlNode.smethod_30(xmlNodes, "codeTypeApch", dataBaseIapOcaOchs0.CodeTypeApch.ToString());
            if (dataBaseIapOcaOchs0.ValOca.IsValid()):
                valOca = dataBaseIapOcaOchs0.ValOca;
                XmlNode.smethod_30(xmlNodes, "valOca", valOca.ToString("0.0###"));
                strS = dataBaseIapOcaOchs0.ValOca.OriginalUnits_ToString();
            if (dataBaseIapOcaOchs0.ValOch.IsValid()):
                valOch = dataBaseIapOcaOchs0.ValOch;
                XmlNode.smethod_30(xmlNodes, "valOch", valOch.ToString("0.0###"));
                if (String.IsNullOrEmpty(strS)):
                    strS = dataBaseIapOcaOchs0.ValOca.OriginalUnits_ToString();
            if (dataBaseIapOcaOchs0.CodeRefOch != CodeRefOchAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codeRefOch", dataBaseIapOcaOchs0.CodeRefOch);
            if (not String.IsNullOrEmpty(strS)):
                XmlNode.smethod_30(xmlNodes, "uomDistVer", strS);
            if (String.IsNullOrEmpty(dataBaseIapOcaOchs0.TxtRmk)):
                continue;
            XmlNode.smethod_30(xmlNodes, "txtRmk", dataBaseIapOcaOchs0.TxtRmk);
            
    def method_71(self, xmlNode_0, dataBaseProcedureLegs_0):
        for dataBaseProcedureLegs0 in dataBaseProcedureLegs_0:
            strS = None;
            xmlNodes = XmlNode.smethod_29(xmlNode_0, "Plg");
            if (dataBaseProcedureLegs0.RecommendedEnt != None):
                self.method_69(xmlNodes, "Uid", dataBaseProcedureLegs0.RecommendedEnt);
            if (dataBaseProcedureLegs0.PointEnt != None):
                self.method_69(xmlNodes, "UidFix", dataBaseProcedureLegs0.PointEnt);
            if (dataBaseProcedureLegs0.CenterEnt != None):
                self.method_69(xmlNodes, "UidCen", dataBaseProcedureLegs0.CenterEnt);
            if (dataBaseProcedureLegs0.CodePhase != CodePhaseProcAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codePhase", dataBaseProcedureLegs0.CodePhase);
            XmlNode.smethod_30(xmlNodes, "codeType", dataBaseProcedureLegs0.CodeType);
            if (not math.isinf(dataBaseProcedureLegs0.ValCourse) and not math.isnan(dataBaseProcedureLegs0.ValCourse)):
                valCourse = dataBaseProcedureLegs0.ValCourse;
                XmlNode.smethod_30(xmlNodes, "valCourse", str(valCourse));
            if (dataBaseProcedureLegs0.CodeTypeCourse != CodeTypeCourseAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codeTypeCourse", dataBaseProcedureLegs0.CodeTypeCourse);
            if (dataBaseProcedureLegs0.CodeDirTurn != CodeDirTurnAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codeDirTurn", dataBaseProcedureLegs0.CodeDirTurn);
            if (dataBaseProcedureLegs0.CodeTurnValid != CodeTypeFlyByAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codeTurnValid", dataBaseProcedureLegs0.CodeTurnValid);
            if (dataBaseProcedureLegs0.CodeDescrDistVer != CodeDescrDistVerAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codeDescrDistVer", dataBaseProcedureLegs0.CodeDescrDistVer);
            if (dataBaseProcedureLegs0.CodeDistVerUpper != CodeDistVerAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codeDistVerUpper", dataBaseProcedureLegs0.CodeDistVerUpper)
            if (dataBaseProcedureLegs0.ValDistVerUpper.IsValid()):
                valDistVerUpper = dataBaseProcedureLegs0.ValDistVerUpper;
                XmlNode.smethod_30(xmlNodes, "valDistVerUpper", valDistVerUpper.ToString("0.0###"));
                altitude = dataBaseProcedureLegs0.ValDistVerUpper;
                XmlNode.smethod_30(xmlNodes, "uomDistVerUpper", altitude.OriginalUnits_ToString());
            if (dataBaseProcedureLegs0.CodeDistVerLower != CodeDistVerAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codeDistVerLower", dataBaseProcedureLegs0.CodeDistVerLower);
            if (dataBaseProcedureLegs0.ValDistVerLower.IsValid()):
                valDistVerLower = dataBaseProcedureLegs0.ValDistVerLower;
                XmlNode.smethod_30(xmlNodes, "valDistVerLower", valDistVerLower.ToString("0.0###"));
                valDistVerLower1 = dataBaseProcedureLegs0.ValDistVerLower;
                XmlNode.smethod_30(xmlNodes, "uomDistVerLower", valDistVerLower1.OriginalUnits_ToString());
            if (dataBaseProcedureLegs0.ValVerAngle != None):
                degrees = Degrees(dataBaseProcedureLegs0.ValVerAngle);
                XmlNode.smethod_30(xmlNodes, "valVerAngle", degrees.ToString("0.0###"));
            if (dataBaseProcedureLegs0.ValSpeedLimit.IsValid()):
                valSpeedLimit = dataBaseProcedureLegs0.ValSpeedLimit;
                XmlNode.smethod_30(xmlNodes, "valSpeedLimit", valSpeedLimit.ToString("0.0#"));
                speed = dataBaseProcedureLegs0.ValSpeedLimit;
                XmlNode.smethod_30(xmlNodes, "uomSpeed", speed.OriginalUnits_ToString());
            if (dataBaseProcedureLegs0.CodeSpeedRef != CodeSpeedRefAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codeSpeedRef", dataBaseProcedureLegs0.CodeSpeedRef);
            if (dataBaseProcedureLegs0.ValDist.IsValid()):
                valDist = dataBaseProcedureLegs0.ValDist;
                XmlNode.smethod_30(xmlNodes, "valDist", valDist.ToString("0.0###"));
                strS = dataBaseProcedureLegs0.ValDist.OriginalUnits_ToString();
            if (dataBaseProcedureLegs0.ValDur.IsValid()):
                valDur = dataBaseProcedureLegs0.ValDur;
                XmlNode.smethod_30(xmlNodes, "valDur", valDur.ToString("0.0#"));
                duration = dataBaseProcedureLegs0.ValDur;
                XmlNode.smethod_30(xmlNodes, "uomDur", duration.OriginalUnits_ToString());
            if (not math.isnan(dataBaseProcedureLegs0.ValTheta) and not math.isinf(dataBaseProcedureLegs0.ValTheta)):
                valTheta = dataBaseProcedureLegs0.ValTheta;
                XmlNode.smethod_30(xmlNodes, "valTheta", str(valTheta));
            if (dataBaseProcedureLegs0.ValRho.IsValid()):
                valRho = dataBaseProcedureLegs0.ValRho;
                XmlNode.smethod_30(xmlNodes, "valRho", valRho.ToString("0.0###"));
                if (String.IsNoneOrEmpty(strS)):
                    strS = dataBaseProcedureLegs0.ValDist.OriginalUnits_ToString();
            if (not String.IsNoneOrEmpty(strS)):
                XmlNode.smethod_30(xmlNodes, "uomDistHorz", strS);
            if (not math.isinf(dataBaseProcedureLegs0.ValBankAngle) and not math.isnan(dataBaseProcedureLegs0.ValBankAngle)):
                valBankAngle = dataBaseProcedureLegs0.ValBankAngle;
                XmlNode.smethod_30(xmlNodes, "valBankAngle", str(valBankAngle));
            if (dataBaseProcedureLegs0.CodeRepAtc != CodeRepAtcAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codeRepAtc", dataBaseProcedureLegs0.CodeRepAtc);
            if (dataBaseProcedureLegs0.CodeRoleFix != CodeIapFixAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codeRoleFix", dataBaseProcedureLegs0.CodeRoleFix);
            if (String.IsNoneOrEmpty(dataBaseProcedureLegs0.TxtRmk)):
                continue;
            XmlNode.smethod_30(xmlNodes, "txtRmk", dataBaseProcedureLegs0.TxtRmk);

    def method_72(self, xmlNode_0, dataBaseProcedureLegsEx_0):
        i = 0
        for dataBaseProcedureLegsEx0 in dataBaseProcedureLegsEx_0:
            xmlNodes = XmlNode.smethod_29(xmlNode_0, "Pcl");
            num = i + 1
            # num = dataBaseProcedureLegsEx_0.IndexOf(dataBaseProcedureLegsEx0) + 1;
            XmlNode.smethod_30(xmlNodes, "noSeq", str(num));
            if (dataBaseProcedureLegsEx0.PointEnt != None):
                self.method_69(xmlNodes, "UidPnt", dataBaseProcedureLegsEx0.PointEnt);
            if (dataBaseProcedureLegsEx0.CenterEnt != None):
                self.method_69(xmlNodes, "UidCen", dataBaseProcedureLegsEx0.CenterEnt);
            if (dataBaseProcedureLegsEx0.CodeLegType != CodeLegTypeAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codeLegType", dataBaseProcedureLegsEx0.CodeLegType);
            if (dataBaseProcedureLegsEx0.CodePathType != CodePathTypeAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codePathType", dataBaseProcedureLegsEx0.CodePathType);
            if (dataBaseProcedureLegsEx0.ValMinAlt.IsValid()):
                valMinAlt = dataBaseProcedureLegsEx0.ValMinAlt;
                XmlNode.smethod_30(xmlNodes, "valMinAlt", valMinAlt.ToString("0.0###"));
                altitude = dataBaseProcedureLegsEx0.ValMinAlt;
                XmlNode.smethod_30(xmlNodes, "uomMinAlt", altitude.OriginalUnits_ToString());
            if (dataBaseProcedureLegsEx0.ValDist.IsValid()):
                valDist = dataBaseProcedureLegsEx0.ValDist;
                XmlNode.smethod_30(xmlNodes, "valDist", valDist.ToString("0.0###"));
                distance = dataBaseProcedureLegsEx0.ValDist;
                XmlNode.smethod_30(xmlNodes, "uomDist", distance.OriginalUnits_ToString());
            if (dataBaseProcedureLegsEx0.ValCourse != None and not math.isnan(dataBaseProcedureLegsEx0.ValCourse) and not math.isinf(dataBaseProcedureLegsEx0.ValCourse)):
                valCourse = dataBaseProcedureLegsEx0.ValCourse;
                XmlNode.smethod_30(xmlNodes, "valCourse", str(valCourse));
            if dataBaseProcedureLegsEx0.ValLegRadial != None and not math.isnan(dataBaseProcedureLegsEx0.ValLegRadial) and not math.isinf(dataBaseProcedureLegsEx0.ValLegRadial):
                valLegRadial = dataBaseProcedureLegsEx0.ValLegRadial;
                XmlNode.smethod_30(xmlNodes, "valLegRadial", str(valLegRadial));
            if (dataBaseProcedureLegsEx0.VorUidLeg != None):
                self.method_69(xmlNodes, "UidLeg", dataBaseProcedureLegsEx0.VorUidLeg);
            if (not String.IsNoneOrEmpty(dataBaseProcedureLegsEx0.CodePointType)):
                XmlNode.smethod_30(xmlNodes, "codePointType", dataBaseProcedureLegsEx0.CodePointType);
            if (dataBaseProcedureLegsEx0.CodeRepAtc != CodeRepAtcAixm.Nothing):
                XmlNode.smethod_30(xmlNodes, "codeRepAtc", dataBaseProcedureLegsEx0.CodeRepAtc);
            if (dataBaseProcedureLegsEx0.ValPointRadial != None and not math.isnan(dataBaseProcedureLegsEx0.ValPointRadial) and not math.isinf(dataBaseProcedureLegsEx0.ValPointRadial)):
                valPointRadial = dataBaseProcedureLegsEx0.ValPointRadial;
                XmlNode.smethod_30(xmlNodes, "valPointRadial", str(valPointRadial));
            if (dataBaseProcedureLegsEx0.VorUidPoint != None):
                self.method_69(xmlNodes, "UidPoint", dataBaseProcedureLegsEx0.VorUidPoint);
            if (dataBaseProcedureLegsEx0.ValLegRadialBack != None and not math.isnan(dataBaseProcedureLegsEx0.ValLegRadialBack) and not math.isinf(dataBaseProcedureLegsEx0.ValLegRadialBack)):
                valLegRadialBack = dataBaseProcedureLegsEx0.ValLegRadialBack;
                XmlNode.smethod_30(xmlNodes, "valLegRadialBack", str(valLegRadialBack));
            if (dataBaseProcedureLegsEx0.VorUidLegBack != None):
                self.method_69(xmlNodes, "UidLegBack", dataBaseProcedureLegsEx0.VorUidLegBack);
            if (dataBaseProcedureLegsEx0.ValPointDist1.IsValid()):
                valPointDist1 = dataBaseProcedureLegsEx0.ValPointDist1;
                XmlNode.smethod_30(xmlNodes, "valPointDist1", valPointDist1.ToString("0.0###"));
                valPointDist11 = dataBaseProcedureLegsEx0.ValPointDist1;
                XmlNode.smethod_30(xmlNodes, "uomPointDist1", valPointDist11.OriginalUnits_ToString());
            if (dataBaseProcedureLegsEx0.UidPointDist1 != None):
                self.method_69(xmlNodes, "Uid1", dataBaseProcedureLegsEx0.UidPointDist1);
            if (dataBaseProcedureLegsEx0.ValPointDist2.IsValid()):
                valPointDist2 = dataBaseProcedureLegsEx0.ValPointDist2;
                XmlNode.smethod_30(xmlNodes, "valPointDist2", valPointDist2.ToString("0.0###"));
                valPointDist21 = dataBaseProcedureLegsEx0.ValPointDist2;
                XmlNode.smethod_30(xmlNodes, "uomPointDist2", valPointDist21.OriginalUnits_ToString());
            if (dataBaseProcedureLegsEx0.UidPointDist2 != None):
                self.method_69(xmlNodes, "Uid2", dataBaseProcedureLegsEx0.UidPointDist2);
            if (not String.IsNoneOrEmpty(dataBaseProcedureLegsEx0.ValDur)):
                XmlNode.smethod_30(xmlNodes, "valDur", dataBaseProcedureLegsEx0.ValDur);
            if (not String.IsNoneOrEmpty(dataBaseProcedureLegsEx0.TxtRmk)):
                XmlNode.smethod_30(xmlNodes, "txtRmk", dataBaseProcedureLegsEx0.TxtRmk);
            if (dataBaseProcedureLegsEx0.CodeFlyBy == CodeTypeFlyByAixm.Nothing):
                continue;
            XmlNode.smethod_30(xmlNodes, "codeFlyBy", dataBaseProcedureLegsEx0.CodeFlyBy);
            i += 1

    def get_HasPCPs(self):
        flag = False;
        if len(self.points) == 0:
            return False
        for current in self.points:
            if (not isinstance(current, ProcEntityPCP)):
                continue;
            flag = True;
            return flag;
        return flag
    HasPCPs = property(get_HasPCPs, None, None, None)