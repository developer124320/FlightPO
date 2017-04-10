
from PyQt4.QtCore import QString
from Type.String import String, StringBuilder
from FlightPlanner.types import SymbolType


SymbolTypeList = [ "Default",
              "Civil land",
               "Civil water",
               "Military land",
               "Military water",
               "Civil/Military land",
               "Civil/Military water",
               "Emergency aerodrome",
               "Sheltered anchorage",
               "Aerodrome",
               "Heliport",
               "Aerodrome reference point",
               "Arrow",
               "Elliptical radio marker beacon",
               "Bone shape radio marker beacon",
               "Navigational aid box 1",
               "Navigational aid box 2",
               "Navigational aid box 3",
               "Navigational aid box 4",
               "Bearing and distance",
               "Bearing and distance (one way)",
               "Church",
               "DME",
               "DME",
               "Localizer",
               "Final approach fix (FAF)",
               "Fly-By WPT",
               "Fly-Over WPT",
               "Glider activity",
               "Basic radio navigation aid",
               "Helicopter activity",
               "ILS",
               "3D Obstacle",
               "Insertion 1",
               "Insertion 2",
               "Insertion 3",
               "Insertion 4",
               "Locator beacon",
               "ATS/MET compulsory reporting point",
               "ATS/MET on request reporting point",
               "MSA box",
               "MSA arrow",
               "Compass rose",
               "NDB",
               "NDB",
               "Unlighted obstacle",
               "Lighted obstacle",
               "Unlighted group obstacles",
               "Lighted group obstacles",
               "Unlighted exceptionally high obstacle",
               "Lighted exceptionally high obstacle",
               "Parachute activity",
               "RDH box",
               "Compulsory reporting point",
               "On request reporting point",
               "VFR reporting point",
               "Runway visual range (RVR) observation site",
               "Scale - enroute",
               "Scale - approach",
               "Scale - aerodrome",
               "TACAN",
               "Transitional altitude box",
               "Tree or shrub",
               "Variation east",
               "Variation west",
               "VOR ",
               "VOR/DME",
               "VOR/TACAN",
               "VOR/TACAN",
               "Spotheight (m)",
               "Spotheight (ft)",
               "No Symbol"]

class Symbol:
    def __init__(self, symbolType_0, bool_0 = None, double_0 = None):
        self.type = symbolType_0;
        self.masked = bool_0;
        self.rotationAngle = double_0
        pass

    def get_DbCode(self):
        str0 = None;
        if self.type == SymbolType.Ad1:
            str0 = "ad1";
        elif self.type == SymbolType.Ad2:
            str0 = "ad2";
        elif self.type == SymbolType.Ad3:
            str0 = "ad3";
        elif self.type == SymbolType.Ad4:
            str0 = "ad4";
        elif self.type == SymbolType.Ad5:
            str0 = "ad5";
        elif self.type == SymbolType.Ad6:
            str0 = "ad6";
        elif self.type == SymbolType.Ad7:
            str0 = "ad7";
        elif self.type == SymbolType.Ad8:
            str0 = "ad8";
        elif self.type == SymbolType.Ad9:
            str0 = "ad9";
        elif self.type == SymbolType.Ad10:
            str0 = "ad10";
        elif self.type == SymbolType.Arp:
            str0 = "arp";
        elif self.type == SymbolType.Arr or \
            self.type == SymbolType.Box1 or \
            self.type == SymbolType.Box2 or \
            self.type == SymbolType.Box3 or \
            self.type == SymbolType.Box4 or \
            self.type == SymbolType.Brg or \
            self.type == SymbolType.Brg1 or \
            self.type == SymbolType.Dme_P or \
            self.type == SymbolType.Ils or \
            self.type == SymbolType.Imp0 or \
            self.type == SymbolType.Imp1 or \
            self.type == SymbolType.Imp2 or \
            self.type == SymbolType.Imp3 or \
            self.type == SymbolType.Imp4 or \
            self.type == SymbolType.Msab or \
            self.type == SymbolType.Msaa or \
            self.type == SymbolType.Ndb_P or \
            self.type == SymbolType.Rdh_P or \
            self.type == SymbolType.Sca1 or \
            self.type == SymbolType.Sca2 or \
            self.type == SymbolType.Sca3 or \
            self.type == SymbolType.TAlt_P or \
            self.type == SymbolType.Vare or \
            self.type == SymbolType.Varw or \
            self.type == SymbolType.Vortac_P:
            return "*";
        elif self.type == SymbolType.Be1:
            str0 = "be1";
        elif self.type == SymbolType.Be2:
            str0 = "be2";
        elif self.type == SymbolType.Church:
            str0 = "church";
        elif self.type == SymbolType.Dme:
            str0 = "dme";
        elif self.type == SymbolType.Loc:
            str0 = "loc";
        elif self.type == SymbolType.Faf:
            str0 = "faf";
        elif self.type == SymbolType.Flyb:
            str0 = "wpfb";
        elif self.type == SymbolType.Flyo:
            str0 = "wpfo";
        elif self.type == SymbolType.Gld:
            str0 = "gld";
        elif self.type == SymbolType.Gp:
            str0 = "gp";
        elif self.type == SymbolType.Hel:
            str0 = "hel";
        elif self.type == SymbolType.Lmm:
            str0 = "lmm";
        elif self.type == SymbolType.Mrp1:
            str0 = "mrpc";
        elif self.type == SymbolType.Mrp2:
            str0 = "mrpnc";
        elif self.type == SymbolType.Nav:
            str0 = "nav";
        elif self.type == SymbolType.Ndb:
            str0 = "ndb";
        elif self.type == SymbolType.Obst1:
            str0 = "obst1";
        elif self.type == SymbolType.Obst2:
            str0 = "obst2";
        elif self.type == SymbolType.Obst3:
            str0 = "obst3";
        elif self.type == SymbolType.Obst4:
            str0 = "obst4";
        elif self.type == SymbolType.Obst5:
            str0 = "obst5";
        elif self.type == SymbolType.Obst6:
            str0 = "obst6";
        elif self.type == SymbolType.Par:
            str0 = "par";
        elif self.type == SymbolType.Repc:
            str0 = "repc";
        elif self.type == SymbolType.Repnc:
            str0 = "repnc";
        elif self.type == SymbolType.Repv:
            str0 = "repv";
        elif self.type == SymbolType.Rvr:
            str0 = "rvr";
        elif self.type == SymbolType.Tacan:
            str0 = "tacan";
        elif self.type == SymbolType.Tree:
            str0 = "tree";
        elif self.type == SymbolType.Vor:
            str0 = "vor";
        elif self.type == SymbolType.Vord:
            str0 = "vord";
        elif self.type == SymbolType.Vortac:
            str0 = "vortac";
        elif self.type == SymbolType.Spot:
            str0 = "spot";
        elif self.type == SymbolType.SpotFt:
            str0 = "spotft";
        else:
            return "*";
        if (self.masked == None and not self.masked):
            return str0;
        str1 = String.Concat([str0, "m"]);
        str0 = str1;
        return str1;
    DbCode = property(get_DbCode, None, None, None)

    def get_IsDataBox(self):
        if (self.type == SymbolType.Box1 or self.type == SymbolType.Box2 or self.type == SymbolType.Box3):
            return True;
        return self.type == SymbolType.Box4;
    IsDataBox = property(get_IsDataBox, None, None, None)

    @staticmethod
    def smethod_4(string_0):
        symbol = None;
        flag = False;
        if isinstance(string_0, QString):
            string_0 = String.QString2Str(string_0)
        if ((string_0[len(string_0) - 1:] == 'm' or string_0[len(string_0) - 1:] == 'M') and not string_0 == "phxlmm"):
            string_0 = string_0[:len(string_0) - 1];
            flag = True;

        for current in SymbolTypeList:
            if current != string_0:
            # if (!string_0.StartsWith(string.Concat("PHX", current.ToString().ToLower()), StringComparison.InvariantCultureIgnoreCase))
            # {
                continue;
            symbol = Symbol(current, flag);
            return symbol;
        return None;
    def ToString(self):
        return self.type

    def __eq__(self, other):
        if other == None:
            return 0
        return self.ToString() == other.ToString()


class SymbolAttributes(list):
    def __init__(self, stringList = None):
        self = []
        if stringList != None:
            self = stringList
            return
        for i in range(8):
            self.append(None)
            
    def get_attributes(self):
        return self
    Array = property(get_attributes, None, None, None)   
    
    def get_Remarks(self):
        if len(self) == 0:
            return
        strBuild = ""
        for i in range(3, len(self)):
            str0 = self[i]
            if str0 != None and str0 != "":
                if strBuild != "":
                    strBuild += ", "
                strBuild += str0  
        return strBuild
    Remarks = property(get_Remarks, None, None, None)

    def get_Count(self):
        if (self == None):
            return -1;
        return len(self);
    Count = property(get_Count, None, None, None)

    
    def method_0(self):
        attrs = self
        return SymbolAttributes(attrs);
    
    def ToString(self):
        if (self == None):
            return "";
        stringBuilder = StringBuilder();
        strArrays = self;
        for i in range(len(strArrays)):
            strS = strArrays[i];
            if (not String.IsNullOrEmpty(strS)):
                if (stringBuilder.Length > 0):
                    stringBuilder.Append(", ");
                stringBuilder.Append(strS);
        return stringBuilder.ToString();

    def __eq__(self, other):
        if other == None:
            return 0
        return self.ToString() == other.ToString()