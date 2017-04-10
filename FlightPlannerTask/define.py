# -*- coding: UTF-8 -*-
'''
Created on Jan 23, 2015

@author: 
'''
from PyQt4.QtCore import QDate, QString

_canvas = None
_mLayerTreeView =None
_qgsDistanceArea = None
_obstacleLayers = None
_surfaceLayers = None
_units = None
_trees = 0.0
_treesDEM = 0.0
_tolerance = 0.0
_toleranceDEM = 0.0
_snapping = True
_messagBar = None
_mapCrs = None
_selectedLayerName = None
_messageLabel = None
_crsLabel = None
_newGeometryList = []
_userLayers = None
_xyCrs = None
_latLonCrs = None
_shownDlgList = []
_degreeStr = QString(unicode("°", "utf-8"))
_numberSavingObstacles = 30
appPath = None
_deletedFeatures = []

smtpServer = "mail.ferventsoft.co.uk"
smtpPort = 587
email = "test@ferventsoft.co.uk"
password = "Fco123"
FromEmail = "infor@flightplanner.se"
FromName = "infor"
MailSubject = "Request Activation Code"
ToEmail = "munna@ferventsoft.com"


obstaclePath = None
xmlPath = None
_appWidth = 0
_appHeight = 0
projectDir = None

