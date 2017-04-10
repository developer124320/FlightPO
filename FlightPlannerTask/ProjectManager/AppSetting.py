

import os
from Type.String import String

class AppSetting:
    def __init__(self):
        self.StateInfoFile = "\\StateInfo.xml";
        # public string StateInfoFile
        # {
        #     get { return m_strStateInfoFile; }
        #     //set { m_strStateInfoFile = value; }
        # }
        self.AeroInfoFile = "\\AerodromeInfo.xml";
        # public string AeroInfoFile
        # {
        #     get { return m_strAeroInfoFile; }
        #     //set { m_strAeroInfoFile = value; }
        # }
        self.RunwayInfoFile = "\\RunwayInfo.xml";
        # public string RunwayInfoFile
        # {
        #     get { return m_strRunwayInfoFile; }
        #     //set { m_strRunwayInfoFile = value; }
        # }

        self.ProjectFolderPath = None
        # public string
        # {
        #     get { return m_strProjectFolderPath; }
        #     set { m_strProjectFolderPath = value; }
        # }
        self.DbaseConnected = False
        # public bool
        # {
        #     get { return m_dbaseConnected; }
        #     set { m_dbaseConnected = value; }
        # }
        self.SnappingEnabled = False
        # public bool SnappingEnabled
        # {
        #     get { return m_bSnappingEnabled; }
        #     set { m_bSnappingEnabled = value; }
        # }
        self.CurrentCoordSys = None
        # public BaseOP.cocaCoordSystem CurrentCoordSys
        # {
        #     get { return m_CurrentCoordSys; }
        #     set { m_CurrentCoordSys = value; }
        # }
        self.OldCoordSys = None
        # public BaseOP.cocaCoordSystem OldCoordSys
        # {
        #     get { return m_OldCoordSys; }
        #     set { m_OldCoordSys = value; }
        # }
        self.CurrentUnitSys = None
        # public BaseOP.cocaUnitSystem CurrentUnitSys
        # {
        #     get { return m_CurrentUnitSys; }
        #     set { m_CurrentUnitSys = value; }
        # }

        self.DBManager = None
        # public HelenaCS.DBManager DBManager
        # {
        #     get { return m_DBManager; }
        #     set { m_DBManager = value; }
        # }
    #endregion

    # public AppSetting()
    # {
        self.ProjectFolderPath = os.getcwdu()
        # self.CurrentCoordSys = BaseOP.cocaCoordSystem.coordMap;
        # m_CurrentUnitSys = BaseOP.cocaUnitSystem.sysNonsi;
        # m_dbaseConnected = false;
        # m_bSnappingEnabled = true;
        # m_DBManager = new DBManager();
    def WriteSettings(self):
        import _winreg as wr

        aReg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
        # aKey = None
        # try:
        targ = r'SOFTWARE\Microsoft\Windows\FlightPlannerLicense'
        print "*** Writing to", targ, "***"
        try:
            aKey = wr.OpenKey(aReg, targ, 0, wr.KEY_WRITE)
        except:
            aKey = wr.CreateKey(aReg, targ)
        try:
            try:
                wr.SetValueEx(aKey, "ProjectPath", 0, wr.REG_SZ, String.QString2Str(self.ProjectFolderPath))
            except Exception:
                print "Encountered problems writing into the Registry..."
        except:
            print "NO"
        finally:
            wr.CloseKey(aKey)
            wr.CloseKey(aReg)
        # except:
        #     print "no"
        # finally:
        #     try:
        #         wr.CloseKey(aReg)
        #         # self.accept()
        #     except:
        #         pass
    #     Microsoft.Win32.RegistryKey key;
    #     try
    #     {
    #         key = Microsoft.Win32.Registry.CurrentUser.CreateSubKey("KayDev");
    #         key.SetValue("ProjectPath", m_strProjectFolderPath);
    #         key.SetValue("DbaseConnected", m_dbaseConnected, Microsoft.Win32.RegistryValueKind.DWord);
    #         key.SetValue("CurrentCoordSys", m_CurrentCoordSys, Microsoft.Win32.RegistryValueKind.DWord);
    #         key.SetValue("CurrentUnitSys", m_CurrentUnitSys, Microsoft.Win32.RegistryValueKind.DWord);
    #         key.SetValue("SnappingEnabled", m_bSnappingEnabled, Microsoft.Win32.RegistryValueKind.DWord);
    #         if (!String.IsNullOrEmpty(m_DBManager.DBServer))
    #         {
    #             key.SetValue("DBServer", m_DBManager.DBServer);
    #         }
    #         if (!String.IsNullOrEmpty(m_DBManager.Database))
    #         {
    #             key.SetValue("DBaseName", m_DBManager.Database);
    #         }
    #         if (!String.IsNullOrEmpty(m_DBManager.DBUser))
    #         {
    #             key.SetValue("DBUser", m_DBManager.DBUser);
    #         }
    #         if (!String.IsNullOrEmpty(m_DBManager.Password))
    #         {
    #             key.SetValue("DBPass", m_DBManager.Password);
    #         }
    #         key.Close();
    #     }
    #     catch (System.Exception ex)
    #     {
    #         MessageBox.Show(ex.Message);
    #     }
    #     finally
    #     {
    #     }
    # }
    def ReadSettings(self):
        import _winreg as wr
        aReg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
        aKey = None
        try:
            targ = r'SOFTWARE\Microsoft\Windows\FlightPlannerLicense'
            print "*** Reading from", targ, "***"
            aKey = wr.OpenKey(aReg, targ)
            try:
                n, v, t = wr.EnumValue(aKey, 0)
                if n == "ProjectPath":
                    self.ProjectFolderPath = v
                    print self.ProjectFolderPath
                    return
            except:
                print "no ProjectPath"
            finally:
                try:
                    wr.CloseKey(aKey)
                except:
                    pass
        except:
            print "no ProjectPath trag"
        finally:
            try:
                wr.CloseKey(aReg)
            except:
                pass
    #     Microsoft.Win32.RegistryKey key;
    #     try
    #     {
    #         key = Microsoft.Win32.Registry.CurrentUser.OpenSubKey("KayDev");
    #         m_strProjectFolderPath = key.GetValue("ProjectPath") as string;
    #         m_dbaseConnected = (Int32)key.GetValue("DbaseConnected", Microsoft.Win32.RegistryValueKind.DWord) > 0;
    #         m_CurrentCoordSys = (BaseOP.cocaCoordSystem)key.GetValue("CurrentCoordSys", Microsoft.Win32.RegistryValueKind.DWord);
    #         m_CurrentUnitSys = (BaseOP.cocaUnitSystem)key.GetValue("CurrentUnitSys", Microsoft.Win32.RegistryValueKind.DWord);
    #         m_bSnappingEnabled = (Int32)key.GetValue("SnappingEnabled", Microsoft.Win32.RegistryValueKind.DWord) > 0;
    #         m_DBManager.DBServer = (string)key.GetValue("DBServer");
    #         m_DBManager.Database = (string)key.GetValue("DBaseName");
    #         m_DBManager.DBUser = (string)key.GetValue("DBUser");
    #         m_DBManager.Password = (string)key.GetValue("DBPass");
    #     }
    #     catch (System.Exception ex)
    #     {
    #         MessageBox.Show(ex.Message);
    #     }
    #     finally
    #     {
    #     }
    # }