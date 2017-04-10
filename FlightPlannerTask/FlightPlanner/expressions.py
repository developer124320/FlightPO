'''
Created on Mar 26, 2015

@author: Administrator
'''
class Expressions:
    GNSS_WPT_EXPRESION = "CASE WHEN  \"Category\" = 'MAHF'  THEN 1 " + \
        "WHEN \"Category\" = 'MAPt' THEN 1 " + \
        "WHEN \"Category\" = 'FAF' THEN 0 " +\
        "WHEN \"Category\" = 'IAFR' THEN 0 " +\
        "WHEN \"Category\" = 'IF' THEN 0 " +\
        "WHEN \"Category\" = 'IAFC' THEN 0 " +\
        "WHEN \"Category\" = 'IAFL' THEN 0 " +\
        "WHEN \"Category\" = 'ARP' THEN 0 " +\
        "END"
        
    BARO_WPT_EXPRESION = "CASE WHEN  \"Category\" = 'FAWP'  THEN 0 " + \
        "WHEN \"Category\" = 'MAHWP' THEN 1 " + \
        "WHEN \"Category\" = 'FAF' THEN 0 " + \
        "WHEN \"Category\" = 'MAPT' THEN 1 " + \
        "END"
    
    COMMON_WPT_EXPRESION = "CASE WHEN  \"Category\" = 'FAWP'  THEN 0 " + \
        "WHEN \"Category\" = 'FlyBy' THEN 0 " + \
        "WHEN \"Category\" = 'FlyOver' THEN 1 " + \
        "WHEN \"Category\" = 'FAP' THEN 0 " + \
        "END"
    
    MSA_ARROW_EXPRESION = "CASE WHEN  \"Category\" = 'ARROW'  THEN 0 " + \
    "WHEN \"Category\" = 'NO_ARROW' THEN 1 " + \
        "END"

    VORDME_WPT_EXPRESION = "CASE WHEN  \"Category\" = 'Waypoint1'  THEN 0 " + \
        "WHEN \"Category\" = 'Waypoint2' THEN 0 " + \
        "END"

    WPT_EXPRESION = "CASE WHEN  \"Category\" = 'Waypoint1'  THEN 1 " + \
        "WHEN \"Category\" = 'Waypoint2' THEN 0 " + \
        "END"
    WPT_EXPRESION_FLY = "CASE WHEN  \"Category\" = 'Fly-Over'  THEN 1 " + \
        "WHEN \"Category\" = 'Fly-By' THEN 0 " + \
        "END"
    RNAVNOMINAL_EXPRESION = "CASE WHEN  \"Category\" = 'FlyOver'  THEN 1 " + \
        "WHEN \"Category\" = 'FlyBy' THEN 0 " + \
        "END"