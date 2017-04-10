# -*- coding: UTF-8 -*-



import os
import sys, define

mapinfo = None
appdatadir = None
path = None
if getattr(sys, 'frozen', False):
    path = os.path.dirname(sys.executable)
    path = path.replace("\\", "/")
    appdatadir = os.environ['LOCALAPPDATA']
    sys.stdout = open(appdatadir + '/my_stdout.log', 'w')
    sys.stderr = open(appdatadir + '/my_stderr.log', 'w')
elif __file__:
    path = os.path.dirname(__file__)
    path = path.replace("\\", "/")
    appdatadir = os.environ['LOCALAPPDATA']
    sys.__stdout__ = open(appdatadir + '/my_stdout.log', 'w')
    sys.__stderr__ = open(appdatadir + '/my_stderr.log', 'w')

define.appPath = path
from subprocess import call
call("runas " + define.appPath + "/Resource/dlls/gacutil.exe /i \"SKGL.dll\"")


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Type.String import String
from AircraftOperation import AirCraftOperation
from qgis.core import QgsApplication
print "Before MyWnd"
from map.mainWindow import MyWnd
print "Before DlgLicensing"
from Licensing.DlgLicensing import DlgLicensing




print "Before clr"
try:
    import clr
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
except SystemError as e1:
    print e1.message
except:
    print "Unexpected error:", sys.exc_info()[0]

print "Before SKGL"
try:
    mydll = clr.AddReference('SKGL')
    from SKGL import Validate, Generate
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
except SystemError as e1:
    print e1.message
except:
    print "Unexpected error:", sys.exc_info()[0]

print "Import End"

l = QStyleFactory.keys()
print l.count()
for ll in l:
    print ll
    i = 1
pass


def main(argv):

    import _winreg as wr
    licenseKey = None
    aReg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
    aKey = None
    try:
        targ = r'SOFTWARE\Microsoft\Windows\FlightPlannerLicense'
        print "*** Reading from", targ, "***"
        aKey = wr.OpenKey(aReg, targ)
        try:
            n, v, t = wr.EnumValue(aKey, 0)
            if n == "License":
                licenseKey = v
                print licenseKey
        except:
            print "no license"
        finally:
            try:
                wr.CloseKey(aKey)
            except:
                pass
    except:
        print "no License trag"
    finally:
        try:
            wr.CloseKey(aReg)
        except:
            pass
        app = QApplication(argv)
        QgsApplication.setPrefixPath(".", True)
        a = QgsApplication.initQgis()

        # f = file("D:/ccc.txt", "w")
        # ss = ["sfdffdsf", "233424324", "sdfsdfs"]
        # f.write("start")
        # f.writelines(ss)
        # f.close()

        print "File print End"
        licenceFlag = False
        if licenseKey != None:

            print "Compare Start"
            objValidate = Validate();
            print "aerodrome$pw3s$Pa$$W0rd"
            objValidate.secretPhase = "aerodrome$pw3s$Pa$$W0rd";
            # GlobalSettings objSetting = GlobalSettings.Load(Constants.globaleSettingsPath);
            objValidate.Key = String.QString2Str(QString(licenseKey)).replace("-", "");
            print objValidate.Key
            # objValidate.Key = "IVAII-UTDIE-HGIEG-WMVOG"
            try:
                if (objValidate.IsValid and objValidate.IsOnRightMachine and objValidate.SetTime >= objValidate.DaysLeft):# and objValidate.IsExpired == False ):
                    licenceFlag = True
            except:
                pass
        print licenceFlag
        # if not licenceFlag:
        #     dlgLicensing = DlgLicensing()
        #     licenceFlag = dlgLicensing.exec_()
        # if licenceFlag:
        #     print "Start  MyWnd"
        define._appWidth = QApplication.desktop().screenGeometry().width()
        define._appHeight = QApplication.desktop().screenGeometry().height()






        window = MyWnd()
        window.setWindowState(Qt.WindowMaximized)
        window.show()
        retval = app.exec_()

        AirCraftOperation.g_AppSetting.WriteSettings()
        if retval:
            pass
        QgsApplication.exitQgis()
        sys.exit(retval)




if __name__ == "__main__":
    # Si el modulo es importado __name__= VisorGeografico  ,
    #    si es ejecutado: __name__ = __main__
    main(sys.argv) # Crear la aplicacion Qt


