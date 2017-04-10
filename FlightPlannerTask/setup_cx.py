import sys, os
from cx_Freeze import setup, Executable
from PyQt4.QtCore import QDateTime

# Build tree of files given a dir (for appending to py2exe data_files)
# Taken from http://osdir.com/ml/python.py2exe/2006-02/msg00085.html

includes = ['sys', 'PyQt4', 'sip']
excludes = ['Tkinter']
packages = ["qgis", "PyQt4"]
path = []
build_exe_options = {
    'icon'    : "flightPlanner.ico",
    'includes': includes,
    'excludes': excludes,
    'packages': packages,
    'path'    : path,
    'include_msvcr': True,
    'include_files': [("licencia.txt", "licencia.txt"), ("UI", "UI"), ("Resource", "Resource"), ("resources", "resources"), ("plugins", "plugins"), ("msvcp71.dll", "msvcp71.dll"), ("Python.Runtime.dll", "Python.Runtime.dll"), ("SKGL.dll", "SKGL.dll"), ("grid_zone_generator_dialog_base.ui", "grid_zone_generator_dialog_base.ui")],
}

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "FlightPlanner",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]flightPlannerMain.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

dateTime = QDateTime.currentDateTime()
currentDate = dateTime.date()
setup(
    name="flightPlannerMainSetup",
    version = str(currentDate.year()) + "." + str(currentDate.month()) + "." + str(currentDate.day()),
    description="",
    options={'build_exe': build_exe_options, 'bdist_msi': bdist_msi_options},
    executables=[Executable("flightPlannerMain.py", base=base, appendScriptToLibrary=False, copyDependentFiles=True)]
)
