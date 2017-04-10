# -*- encoding=utf-8 -*-

from distutils.core import setup
import ctypes
import os, datetime

# Build tree of files given a dir (for appending to py2exe data_files)
# Taken from http://osdir.com/ml/python.py2exe/2006-02/msg00085.html
def tree(src):
    list = [(root, map(lambda f: os.path.join(root, f), files)) for (root, dirs, files) in os.walk(os.path.normpath(src))]
    new_list = []
    for (root, files) in list:
        if len(files) > 0 and root.count('.svn') == 0:
            new_list.append((root, files))
    return new_list

################################################################
class InnoScript:
    def __init__(self,
                 name,
                 lib_dir,
                 dist_dir,
                 windows_exe_files = [],
                 lib_files = [],
                 version = "1.0"):
        self.lib_dir = lib_dir
        self.dist_dir = dist_dir
        if not self.dist_dir[-1] in "\\/":
            self.dist_dir += "\\"
        self.name = name
        self.version = version
        self.windows_exe_files = [self.chop(p) for p in windows_exe_files]
        self.lib_files = [self.chop(p) for p in lib_files]

    def chop(self, pathname):
        assert pathname.startswith(self.dist_dir)
        return pathname[len(self.dist_dir):]

    def create(self, pathname="dist\\CATSSetupScript.iss"):
        self.pathname = pathname
        ofi = self.file = open(pathname, "w")
        print >> ofi, "; WARNING: This script has been created by py2exe. Changes to this script"
        print >> ofi, "; will be overwritten the next time py2exe is run!"
        print >> ofi, r"[Setup]"
        print >> ofi, r"AppName=%s %s" % (self.name, self.version)
        print >> ofi, r"AppVerName=%s %s" % (self.name, self.version)
        print >> ofi, r"DefaultDirName={pf}\%s" % self.name
        print >> ofi, r"DefaultGroupName=%s" % self.name
        print >> ofi, r"VersionInfoVersion=%s" % self.version
        print >> ofi, r"VersionInfoCompany=GeoCoder"
        print >> ofi, r"VersionInfoDescription=GeoCoder"
        print >> ofi, r"VersionInfoCopyright=GeoCoder"
        print >> ofi, r"AppCopyright=GeoCoder - 2014"
        print >> ofi, r"AppSupportURL= "
        print >> ofi, r"OutputBaseFilename=FlightPlanner%d_%d_installer" % (datetime.datetime.today().month , datetime.datetime.today().day)
        print >> ofi, r"LicenseFile=licencia.txt"
        print >> ofi, r"WizardImageBackColor=clBlack"
        print >> ofi

        print >> ofi, r"[Tasks]"
        print >> ofi, r'Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"'
        print >> ofi, r'Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"'
        print >> ofi

        print >> ofi, r"[Files]"
        for path in self.windows_exe_files + self.lib_files:
            print >> ofi, r'Source: "%s"; DestDir: "{app}\%s"; Flags: ignoreversion' % (path, os.path.dirname(path))
#         print >> ofi, r'Source: lib\gdal16.dll; DestDir: {app}\lib; Flags: ignoreversion'
#         print >> ofi, r'Source: lib\QtSvg4.dll; DestDir: {app}\lib; Flags: ignoreversion'
#         print >> ofi, r'Source: lib\proj.dll; DestDir: {app}\lib; Flags: ignoreversion'
#         print >> ofi, r'Source: "vcredist_2005_x86.exe"; DestDir: "{app}\"'
#         print >> ofi, r'Source: "vcredist_2008_x86.exe"; DestDir: "{app}\"'
#         print >> ofi, r'Source: "vcredist_2010_x86.exe"; DestDir: "{app}\"'
#         print >> ofi, r'[Run]'
#         print >> ofi, r'Filename: "{app}\vcredist_2005_x86.exe"'
#         print >> ofi, r'Filename: "{app}\vcredist_2008_x86.exe"'
#         print >> ofi, r'Filename: "{app}\vcredist_2010_x86.exe"'
        
        print >> ofi, r"[Icons]"
        print >> ofi, r'Name: "{group}\{cm:ProgramOnTheWeb,%s}"; Filename: "flightPlanner.ico"' % \
              self.name

        for path in self.windows_exe_files:
            print >> ofi, r'Name: "{group}\%s"; Filename: "{app}\%s"; WorkingDir: {app}; IconFilename: "{app}\flightPlanner.ico"' % \
                  (self.name, path)

        print >> ofi, 'Name: "{group}\Uninstall %s"; Filename: "{uninstallexe}"' % self.name
        print >> ofi, 'Name: "{commondesktop}\%s"; Filename: "{app}\%s"; Tasks: desktopicon; WorkingDir: "{app}"; IconFilename: "{app}\flightPlanner.ico"' % \
              (self.name, path)
        print >> ofi, 'Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\%s"; Filename: "{app}\%s"; Tasks: quicklaunchicon; WorkingDir: "{app}"' % \
              (self.name, path)
        
    def compile(self):
        try:
            import ctypes2
        except ImportError:
            try:
                import win32api
            except ImportError:
                import os
                os.startfile(self.pathname)
            else:
                print "Ok, using win32api."
                win32api.ShellExecute(0, "compile",
                                               self.pathname,
                                               None,
                                               None,
                                               0)
        else:
            print "Cool, you have ctypes installed."
            res = ctypes.windll.shell32.ShellExecuteA(0, "compile",
                                                     self.pathname,
                                                     None,
                                                     None,
                                                     0)
            if res < 32:
                raise RuntimeError, "ShellExecute failed, error %d" % res


################################################################

from py2exe.build_exe import py2exe

class build_installer(py2exe):
    # This class first builds the exe file(s), then creates a Windows installer.
    # You need InnoSetup for it.
    def run(self):
        # First, let py2exe do it's work.
        py2exe.run(self)
    
        lib_dir = self.lib_dir
        dist_dir = self.dist_dir
    
        # create the Installer, using the files py2exe has created.
        script = InnoScript("FlightPlanner",
                            lib_dir,
                            dist_dir,
                            self.windows_exe_files,
                            self.lib_files)
        print "*** creating the inno setup script***"
        script.create()
        print "*** compiling the inno setup script***"
        script.compile()
        # Note: By default the final setup.exe will be in an Output subdirectory.

######################## py2exe setup options ########################################

zipfile = r"lib\shardlib"

options = {
   "py2exe": {
       "compressed": 1,
       "optimize": 2,
       "includes": ['sip'],
       "excludes": ['backend_gtkagg', 'backend_wxagg', 'tcl', 'tcl.tcl8.4', 'Tkinter' ],
       "dll_excludes": ['libgdk_pixbuf-2.0-0.dll', 'libgobject-2.0-0.dll', 'libiomp5md.dll', 'libgdk-win32-2.0-0.dll', 'phonon4.dll', 'QtScriptTools4.dll', 'tcl84.dll', 'tk84.dll' ],
       "packages": ["qgis", "PyQt4"],
       "dist_dir": "dist",
   }
}


data_files = tree('plugins') + tree('resources') + tree('Resource') + [ ( ".", [ "msvcp71.dll", "licencia.txt", "flightPlanner.ico"] ) ]

setup(
   options = options,
   # The lib directory contains everything except the executables and the python dll.
   zipfile = zipfile,
   windows=[{"script": "flightPlannerMain.py"}],
   # use out build_installer class as extended py2exe build command
   cmdclass = {"py2exe": build_installer},
   data_files = data_files
)