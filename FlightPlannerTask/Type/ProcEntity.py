from Type.String import String
from FlightPlanner.types import CodeTypeDesigPtAixm


class ProcEntityDirectionBase:
    def __init__(self):
        self.AhpCodeId = None
        pass
    # def get_AhpCodeId(self):
    #     return None
    # def set_AhpCodeId(self, value):
    #     pass
    # AhpCodeId = property(get_AhpCodeId, set_AhpCodeId, None, None)

class ProcEntityBase:
    def __init__(self):
        self.custom = False;
        self.modified = False;
        self.codeId = None;
        self.codeType = None;
        self.geoLat = None;
        self.geoLong = None;
        self.txtName = None;
        self.txtRmk = None;
        self.txtDesig = None;
    def get_CodeId(self):
        return self.codeId
    def set_CodeId(self, value):
        self.modified = value == self.codeId;
        self.codeId = value;
    CodeId = property(get_CodeId, set_CodeId, None, None)

    def get_CodeType(self):
        return self.codeType
    def set_CodeType(self, value):
        self.modified = value == self.codeType;
        self.codeType = value;
    CodeType = property(get_CodeType, set_CodeType, None, None)

    def get_Custom(self):
        return self.custom
    Custom = property(get_Custom, None, None, None)

    def get_GeoLat(self):
        return self.geoLat
    def set_GeoLat(self, value):
        self.modified = value == self.geoLat;
        self.geoLat = value;
    GeoLat = property(get_GeoLat, set_GeoLat, None, None)

    def get_GeoLong(self):
        return self.geoLong
    def set_GeoLong(self, value):
        self.modified = value == self.geoLong;
        self.geoLong = value;
    GeoLong = property(get_GeoLong, set_GeoLong, None, None)

    def get_TxtDesig(self):
        return self.txtDesig
    def set_TxtDesig(self, value):
        self.modified = value == self.txtDesig;
        self.txtDesig = value;
    TxtDesig = property(get_TxtDesig, set_TxtDesig, None, None)

    def get_TxtName(self):
        return self.txtName
    def set_TxtName(self, value):
        self.modified = value == self.txtName;
        self.txtName = value;
    TxtName = property(get_TxtName, set_TxtName, None, None)

    def get_TxtRmk(self):
        return self.txtRmk
    def set_TxtRmk(self, value):
        self.modified = value == self.txtRmk;
        self.txtRmk = value;
    TxtRmk = property(get_TxtRmk, set_TxtRmk, None, None)

    def get_Type(self):
        if isinstance(self, ProcEntityVOR):
            return "Vor";
        if isinstance(self, ProcEntityTCN):
            return "Tcn";
        if isinstance(self, ProcEntityDME):
            return "Dme";
        if isinstance(self, ProcEntityNDB):
            return "Ndb";
        if isinstance(self, ProcEntityMKR):
            return "Mkr";
        if isinstance(self, ProcEntitySNY):
            return "Sny";
        if isinstance(self, ProcEntityILS):
            return "Ils";
        if isinstance(self, ProcEntityMLS):
            return "Mls";
        if isinstance(self, ProcEntityDPN):
            return "Dpn";
        if isinstance(self, ProcEntityPCP):
            return "Pcp";
        if isinstance(self, ProcEntityRCP):
            return "Rcp";
        if isinstance(self, ProcEntityFCP):
            return "Fcp";
        if isinstance(self, ProcEntityTLA):
            return "Tla";
        if (not isinstance(self, ProcEntityAHP)):
            raise UserWarning, "ProcEntityBase type to string: Unsupported object type."
        return "Ahp";
    Type = property(get_Type, None, None, None)
    
    def ToString(self):
        strs = [];
        str0 = None;
        if isinstance(self, ProcEntityVOR):
            str0 = "VOR";
        elif isinstance(self, ProcEntityTCN):
            str0 = "TCN";
        elif isinstance(self, ProcEntityDME):
            str0 = "DME";
        elif isinstance(self, ProcEntityNDB):
            str0 = "NDB";
        elif isinstance(self, ProcEntityMKR):
            str0 = "MKR";
        elif isinstance(self, ProcEntitySNY):
            str0 = "SNY";
        elif isinstance(self, ProcEntityILS):
            str0 = "ILS";
        elif isinstance(self, ProcEntityMLS):
            str0 = "MLS";
        elif (not isinstance(self, ProcEntityDPN)):
            if (not isinstance(self, ProcEntityPCP)):
                str1 = self.GetType().ToString();
                return str1.Substring(str1.Length - 3);
            str0 = "PCP";
        else:
            str0 = "DPN";
        if isinstance(self, ProcEntityPCP):
            if (not String.IsNullOrEmpty(self.CodeId)):
                strs.append(self.CodeId);
            if (not String.IsNullOrEmpty(self.TxtDesig)):
                strs.append(self.TxtDesig);
            if (not String.IsNullOrEmpty(self.GeoLat)):
                strs.append(self.GeoLat);
            if (not String.IsNullOrEmpty(self.GeoLong)):
                strs.append(self.GeoLong);
        if isinstance(self, ProcEntityDPN):
            if (not String.IsNullOrEmpty(self.CodeId)):
                strs.append(self.CodeId);
            if (not String.IsNullOrEmpty(self.TxtDesig)):
                strs.append(self.TxtDesig);
            if (not String.IsNullOrEmpty(self.GeoLat)):
                strs.append(self.GeoLat);
            if (not String.IsNullOrEmpty(self.GeoLong)):
                strs.append(self.GeoLong);
        elif isinstance(self, ProcEntityMKR):
            strs.append(self.CodeId);
            if (not String.IsNullOrEmpty(self.GeoLat)):
                strs.append(self.GeoLat);
            if (not String.IsNullOrEmpty(self.GeoLong)):
                strs.append(self.GeoLong);
            if (not String.IsNullOrEmpty(self.TxtName)):
                strs.append(self.TxtName);
            elif (not String.IsNullOrEmpty(self.TxtRmk)):
                strs.append(self.TxtRmk);
        elif isinstance(self, ProcEntityILS or isinstance(ProcEntityMLS)):
            if (not String.IsNullOrEmpty(self.TxtName)):
                strs.append(self.TxtName);
        elif isinstance(self, ProcEntitySNY):
            if (not String.IsNullOrEmpty(self.CodeId)):
                strs.append(self.CodeId);
            if (not String.IsNullOrEmpty(self.CodeType)):
                strs.append(self.CodeType);
        elif (not isinstance(self, ProcEntityRCP) and not isinstance(self, ProcEntityFCP)):
            if (not String.IsNullOrEmpty(self.CodeId)):
                strs.append(self.CodeId);
        elif (not String.IsNullOrEmpty(self.TxtName)):
            strs.append(self.TxtName);
        newStrs = strs
        return "{0} {1}".format(str0, String.Join(", ", newStrs));

class ProcEntityVOR(ProcEntityBase):
    def __init__(self, xmlNode_0 = None, string_0 = None, string_1 = None, string_2 = None):
        ProcEntityBase.__init__(self)

        if string_0 != None:
            self.codeId = string_0;
            self.geoLat = string_1;
            self.geoLong = string_2;
        elif xmlNode_0 != None:
            self.codeId = xmlNode_0.namedItem("codeId").toElement().text()#.SelectSingleNode("codeId").InnerText;
            self.geoLat = xmlNode_0.namedItem("geoLat").toElement().text()#.SelectSingleNode("geoLat").InnerText;
            self.geoLong = xmlNode_0.namedItem("geoLong").toElement().text()#.SelectSingleNode("geoLong").InnerText;

class ProcEntityTCN(ProcEntityBase):
    def __init__(self, xmlNode_0 = None, string_0 = None, string_1 = None, string_2 = None):
        ProcEntityBase.__init__(self)

        if string_0 != None:
            self.codeId = string_0;
            self.geoLat = string_1;
            self.geoLong = string_2;
        elif xmlNode_0 != None:
            self.codeId = xmlNode_0.namedItem("codeId").toElement().text()#.SelectSingleNode("codeId").InnerText;
            self.geoLat = xmlNode_0.namedItem("geoLat").toElement().text()#.SelectSingleNode("geoLat").InnerText;
            self.geoLong = xmlNode_0.namedItem("geoLong").toElement().text()#.SelectSingleNode("geoLong").InnerText;

class ProcEntityDME(ProcEntityBase):
    def __init__(self, xmlNode_0 = None, string_0 = None, string_1 = None, string_2 = None):
        ProcEntityBase.__init__(self)

        if string_0 != None:
            self.codeId = string_0;
            self.geoLat = string_1;
            self.geoLong = string_2;
        elif xmlNode_0 != None:
            self.codeId = xmlNode_0.namedItem("codeId").toElement().text()#.SelectSingleNode("codeId").InnerText;
            self.geoLat = xmlNode_0.namedItem("geoLat").toElement().text()#.SelectSingleNode("geoLat").InnerText;
            self.geoLong = xmlNode_0.namedItem("geoLong").toElement().text()#.SelectSingleNode("geoLong").InnerText;

class ProcEntityNDB(ProcEntityBase):
    def __init__(self, xmlNode_0 = None, string_0 = None, string_1 = None, string_2 = None):
        ProcEntityBase.__init__(self)

        if string_0 != None:
            self.codeId = string_0;
            self.geoLat = string_1;
            self.geoLong = string_2;
        elif xmlNode_0 != None:
            self.codeId = xmlNode_0.namedItem("codeId").toElement().text()#.SelectSingleNode("codeId").InnerText;
            self.geoLat = xmlNode_0.namedItem("geoLat").toElement().text()#.SelectSingleNode("geoLat").InnerText;
            self.geoLong = xmlNode_0.namedItem("geoLong").toElement().text()#.SelectSingleNode("geoLong").InnerText;

class ProcEntityMKR(ProcEntityBase):
    def __init__(self, xmlNode_0 = None, string_0 = None, string_1 = None, string_2 = None, string_3 = None, string_4 = None):
        ProcEntityBase.__init__(self)

        if string_0 != None:
            if string_3 != None:
                self.txtName = string_0;
                self.codeId = string_1;
                self.geoLat = string_2;
                self.geoLong = string_3;
                self.txtRmk = string_4;
            else:
                self.codeId = string_0;
                self.geoLat = string_1;
                self.geoLong = string_2;
        elif xmlNode_0 != None:
            self.codeId = xmlNode_0.namedItem("codeId").toElement().text()#.SelectSingleNode("codeId").InnerText;
            self.geoLat = xmlNode_0.namedItem("geoLat").toElement().text()#.SelectSingleNode("geoLat").InnerText;
            self.geoLong = xmlNode_0.namedItem("geoLong").toElement().text()#.SelectSingleNode("geoLong").InnerText;

class ProcEntitySNY(ProcEntityBase):
    def __init__(self, xmlNode_0 = None, string_0 = None, string_1 = None, string_2 = None, string_3 = None):
        ProcEntityBase.__init__(self)

        if string_0 != None:
            if string_2 != None:
                self.txtName = string_0;
                self.codeId = string_1;
                self.codeType = string_2;
                self.txtRmk = string_3;
            else:
                self.codeId = string_0;
                self.codeType = string_1;
        elif xmlNode_0 != None:
            self.codeId = xmlNode_0.namedItem("codeId").toElement().text()#.SelectSingleNode("codeId").InnerText;
            self.codeType = xmlNode_0.namedItem("codeType").toElement().text()#.SelectSingleNode("geoLat").InnerText;

class ProcEntityILS(ProcEntityBase):
    def __init__(self, xmlNode_0 = None, procEntityDirectionBase_0 = None, string_0 = None, string_1 = None):
        ProcEntityBase.__init__(self)

        self.uidBase = None

        if xmlNode_0 != None:
            xmlNodes = xmlNode_0.namedItem("RdnUid");
            xmlNodes1 = xmlNode_0.namedItem("FdnUid");
            if (xmlNodes != None):
                xmlNodes2 = xmlNodes.namedItem("RwyUid");
                xmlNodes3 = xmlNodes2.namedItem("AhpUid");
                self.uidBase = ProcEntityRDN(None, xmlNodes3.namedItem("codeId").toElement().text(), \
                                             xmlNodes2.namedItem("txtDesig").toElement().text(), \
                                             xmlNodes.namedItem("txtDesig").toElement().text());
            elif (xmlNodes1 != None):
                xmlNodes4 = xmlNodes.namedItem("FtoUid");
                xmlNodes5 = xmlNodes4.namedItem("AhpUid");
                self.uidBase = ProcEntityFDN(None, xmlNodes5.namedItem("codeId").toElement().text(), \
                                             xmlNodes4.namedItem("txtDesig").toElement().text(), \
                                             xmlNodes1.namedItem("txtDesig").toElement().text());

            self.txtName = self.uidBase.ToString();
        else:
            self.uidBase = procEntityDirectionBase_0;
            self.txtName = procEntityDirectionBase_0.ToString();
            if (not String.IsNullOrEmpty(string_0)):
                self.txtDesig = string_0;
            if (not String.IsNullOrEmpty(string_1)):
                self.txtRmk = string_1;

    def get_UidBase(self):
        return self.uidBase
    UidBase = property(get_UidBase, None, None, None)

class ProcEntityMLS(ProcEntityBase):
    def __init__(self, xmlNode_0 = None, procEntityDirectionBase_0 = None, string_0 = None, string_1 = None):
        ProcEntityBase.__init__(self)

        self.uidBase = None

        if xmlNode_0 != None:
            xmlNodes = xmlNode_0.namedItem("RdnUid");
            xmlNodes1 = xmlNode_0.namedItem("FdnUid");
            if (xmlNodes != None):
                xmlNodes2 = xmlNodes.namedItem("RwyUid");
                xmlNodes3 = xmlNodes2.namedItem("AhpUid");
                self.uidBase = ProcEntityRDN(None, xmlNodes3.namedItem("codeId").toElement().text(), \
                                             xmlNodes2.namedItem("txtDesig").toElement().text(), \
                                             xmlNodes.namedItem("txtDesig").toElement().text());
            elif (xmlNodes1 != None):
                xmlNodes4 = xmlNodes.namedItem("FtoUid");
                xmlNodes5 = xmlNodes4.namedItem("AhpUid");
                self.uidBase = ProcEntityFDN(None, xmlNodes5.namedItem("codeId").toElement().text(), \
                                             xmlNodes4.namedItem("txtDesig").toElement().text(), \
                                             xmlNodes1.namedItem("txtDesig").toElement().text());

            self.txtName = self.uidBase.ToString();
        else:
            self.uidBase = procEntityDirectionBase_0;
            self.txtName = procEntityDirectionBase_0.ToString();
            if (not String.IsNullOrEmpty(string_0)):
                self.txtDesig = string_0;
            if (not String.IsNullOrEmpty(string_1)):
                self.txtRmk = string_1;

    def get_UidBase(self):
        return self.uidBase
    UidBase = property(get_UidBase, None, None, None)

class ProcEntityDPN(ProcEntityBase):
    def __init__(self, string_0, string_1, string_2, procEntityAHP_0 = None, procEntityBase_0 = None, codeTypeDesigPtAixm_0 = None, string_3 = None, string_4 = None, bool_0 = None):
        ProcEntityBase.__init__(self)

        self.codeTypeDpn = None;
        self.associated = None;
        self.location = None;

        if procEntityAHP_0 == None:
            self.custom = False;
            self.modified = False;
            self.codeId = string_0;
            self.geoLat = string_1;
            self.geoLong = string_2;
            self.associated = None;
            self.location = None;
            self.codeTypeDpn = CodeTypeDesigPtAixm.OTHER;
            self.txtName = None;
            self.txtRmk = None;
        else:
            self.custom = bool_0;
            self.modified = False;
            self.codeId = string_0;
            self.geoLat = string_1;
            self.geoLong = string_2;
            self.associated = procEntityAHP_0;
            self.location = procEntityBase_0;
            self.codeTypeDpn = codeTypeDesigPtAixm_0;
            self.txtName = string_3;
            self.txtRmk = string_4;
    def get_Associated(self):
        return self.associated
    def set_Associated(self, value):
        self.modified = True;
        self.associated = value;
    Associated = property(get_Associated, set_Associated, None, None)

    def get_CodeTypeDpn(self):
        return self.codeTypeDpn
    def set_CodeTypeDpn(self, value):
        self.modified = True;
        self.codeTypeDpn = value;
    CodeTypeDpn = property(get_CodeTypeDpn, set_CodeTypeDpn, None, None)

    def get_Location(self):
        return self.location
    def set_Location(self, value):
        self.modified = True;
        self.location = value;
    Location = property(get_Location, set_Location, None, None)

class ProcEntityPCP(ProcEntityBase):
    def __init__(self, xmlNode_0 = None, string_0 = None, string_1 = None, string_2 = None, string_3 = None, string_4 = None, bool_0 = None):
        ProcEntityBase.__init__(self)

        if xmlNode_0 != None:
            innerText = None;
            xmlNodes = xmlNode_0.namedItem("txtDesig");
            if (xmlNodes == None):
                innerText = None;
            else:
                innerText = xmlNodes.toElement().text();
            self.txtDesig = innerText;
            self.geoLat = xmlNode_0.namedItem("geoLat").toElement().text();
            self.geoLong = xmlNode_0.namedItem("geoLong").toElement().text();
            self.custom = False;

        elif string_3 == None:
            self.txtDesig = string_0;
            self.geoLat = string_1;
            self.geoLong = string_2;
            self.custom = False;
        else:
            self.txtDesig = string_0;
            self.geoLat = string_1;
            self.geoLong = string_2;
            self.codeType = string_3;
            self.txtRmk = string_4;
            self.custom = bool_0;

class ProcEntityRCP(ProcEntityBase):
    def __init__(self, xmlNode_0 = None, string_0 = None, string_1 = None, string_2 = None, string_3 = None):
        ProcEntityBase.__init__(self)

        if xmlNode_0 != None:
            xmlNodes = xmlNode_0.namedItem("RwyUid");
            xmlNodes1 = xmlNodes.namedItem("AhpUid");
            self.codeId = xmlNodes1.namedItem("codeId").toElement().text();
            self.txtDesig = xmlNodes.namedItem("txtDesig").toElement().text();
            self.geoLat = xmlNode_0.namedItem("geoLat").toElement().text();
            self.geoLong = xmlNode_0.namedItem("geoLong").toElement().text();
            self.txtName = "{0} RWY {1}".format(self.codeId, self.txtDesig);
        else:
            self.codeId = string_0;
            self.txtDesig = string_1;
            self.geoLat = string_2;
            self.geoLong = string_3;
            self.txtName = "{0} RWY {1}".format(string_0, string_1);

    def ToString(self):
        return "RCP {0}, {1}, {2}".format(self.txtName, self.geoLat, self.geoLong);

class ProcEntityFCP(ProcEntityBase):
    def __init__(self, xmlNode_0 = None, string_0 = None, string_1 = None, string_2 = None, string_3 = None):
        ProcEntityBase.__init__(self)

        if xmlNode_0 != None:
            xmlNodes = xmlNode_0.namedItem("FtoUid");
            xmlNodes1 = xmlNodes.namedItem("AhpUid");
            self.codeId = xmlNodes1.namedItem("codeId").toElement().text();
            self.txtDesig = xmlNodes.namedItem("txtDesig").toElement().text();
            self.geoLat = xmlNode_0.namedItem("geoLat").toElement().text();
            self.geoLong = xmlNode_0.namedItem("geoLong").toElement().text();
            self.txtName = "{0}".format(self.codeId, self.txtDesig);
            if (self.codeId != self.txtDesig):
                procEntityFCP = self;
                self.txtName = String.Concat([procEntityFCP.txtName, " {0}".format(self.txtDesig)]);
        else:
            self.codeId = string_0;
            self.txtDesig = string_1;
            self.geoLat = string_2;
            self.geoLong = string_3;
            self.txtName = "{0} {1}".format(string_0, string_1);
    def ToString(self):
        return "FCP {0}, {1}, {2}".format(self.txtName, self.geoLat, self.geoLong);

class ProcEntityTLA(ProcEntityBase):
    def __init__(self, xmlNode_0 = None, string_0 = None, string_1 = None):
        ProcEntityBase.__init__(self)

        if xmlNode_0 != None:
            xmlNodes = xmlNode_0.namedItem("AhpUid");
            self.codeId = xmlNodes.namedItem("codeId").toElement().text();
            self.txtDesig = xmlNode_0.namedItem("txtDesig").toElement().text();
        else:
            self.codeId = string_0;
            self.txtDesig = string_1;
    def ToString(self):
        return "TLA {0} {1}".format(self.codeId, self.txtDesig);

class ProcEntityAHP(ProcEntityBase):
    def __init__(self, xmlNode_0):
        ProcEntityBase.__init__(self)

        self.AhpCodeId = xmlNode_0.namedItem("codeId").toElement().text();
        self.TxtName = None;
        self.ValMagVar = None;
    def ToString(self):
        if (String.IsNullOrEmpty(self.txtName)):
            return self.AhpCodeId;
        return "{0} ({1})".Format(self.AhpCodeId, self.txtName);

    # def get_AhpCodeId(self):
    #     return None
    # def set_AhpCodeId(self):
    #     pass
    # AhpCodeId = property(get_AhpCodeId, set_AhpCodeId, None, None)
    #
    # def get_ValMagVar(self):
    #     return None
    # def set_ValMagVar(self):
    #     pass
    # ValMagVar = property(get_ValMagVar, set_ValMagVar, None, None)

class ProcEntityRDN(ProcEntityDirectionBase):
    def __init__(self, xmlNode_0 = None, string_0 = None, string_1 = None, string_2 = None):
        ProcEntityDirectionBase.__init__(self)

        if xmlNode_0 != None:
            xmlNodes = xmlNode_0.namedItem("RwyUid");
            xmlNodes1 = xmlNodes.namedItem("AhpUid");
            self.AhpCodeId = xmlNodes1.namedItem("codeId").toElement().text();
            self.RwyDesig = xmlNodes.namedItem("txtDesig").toElement().text();
            self.RdnDesig = xmlNode_0.namedItem("txtDesig").toElement().text();
        else:
            self.AhpCodeId = string_0;
            self.RwyDesig = string_1;
            self.RdnDesig = string_2;

    # def get_RdnDesig(self):
    #     return None
    # def set_RdnDesig(self):
    #     pass
    # RdnDesig = property(get_RdnDesig, set_RdnDesig, None, None)
    #
    # def get_RwyDesig(self):
    #     return None
    # def set_RwyDesig(self):
    #     pass
    # RwyDesig = property(get_RwyDesig, set_RwyDesig, None, None)

    def ToString(self):
        return "{0} RWY {1}".format(self.AhpCodeId, self.RdnDesig);

class ProcEntityFDN(ProcEntityDirectionBase):
    def __init__(self, xmlNode_0 = None, string_0 = None, string_1 = None, string_2 = None):
        ProcEntityDirectionBase.__init__(self)

        if xmlNode_0 != None:
            xmlNodes = xmlNode_0.namedItem("FtoUid");
            xmlNodes1 = xmlNodes.namedItem("AhpUid");
            self.AhpCodeId = xmlNodes1.namedItem("codeId").toElement().text();
            self.FtoDesig = xmlNodes.namedItem("txtDesig").toElement().text();
            self.FdnDesig = xmlNode_0.namedItem("txtDesig").toElement().text();
        else:
            self.AhpCodeId = string_0;
            self.FtoDesig = string_1;
            self.FdnDesig = string_2;
    def ToString(self):
        return "{0} {1}".format(self.AhpCodeId, self.FdnDesig);




