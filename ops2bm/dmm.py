import os
import sys
import time
import shutil
from pathlib import Path
import numpy as np

from ops2bm import util
from ops2bm import epics_move
from ops2bm import log

def set_pink(params):

    print(params)
    log.info('changing pink')
    lookup={
    "1.500" : {"Mirr_YAvg": -0.1, "DMM_USY_OB": -10, "DMM_USY_IB": -10, "DMM_DSY": -10, "DMM_USX": 50, "DMM_DSX": 50, "XIASlitY":  8.75, "Slit1Hcenter": 4.85, "Filter": 0},
    "1.800" : {"Mirr_YAvg":  0.0, "DMM_USY_OB": -10, "DMM_USY_IB": -10, "DMM_DSY": -10, "DMM_USX": 50, "DMM_DSX": 50, "XIASlitY": 11.75, "Slit1Hcenter": 4.85, "Filter": 0},
    "2.000" : {"Mirr_YAvg":  0.0, "DMM_USY_OB": -10, "DMM_USY_IB": -10, "DMM_DSY": -10, "DMM_USX": 50, "DMM_DSX": 50, "XIASlitY": 13.75, "Slit1Hcenter":  7.5, "Filter": 0},
    "2.100" : {"Mirr_YAvg":  0.0, "DMM_USY_OB": -10, "DMM_USY_IB": -10, "DMM_DSY": -10, "DMM_USX": 50, "DMM_DSX": 50, "XIASlitY": 14.75, "Slit1Hcenter":  7.5, "Filter": 0},
    "2.657" : {"Mirr_YAvg":  0.0, "DMM_USY_OB": -10, "DMM_USY_IB": -10, "DMM_DSY": -10, "DMM_USX": 50, "DMM_DSX": 50, "XIASlitY": 18.75, "Slit1Hcenter":  7.2, "Filter": 0}
    }
    angles_str = np.array(list(lookup.keys())[:])
    angles_flt = [float(i) for i in  angles_str]

    angle_calibrated = find_nearest(angles_flt, params.Mirr_Ang)
    if float(params.Mirr_Ang) != float(angle_calibrated):
        log.warning('   *** Mirror angle requested is %s mrad, the closest calibrated angle is %s mrad' % (params.Mirr_Ang, angle_calibrated))
        log.info('   *** Options are %s mrad' % (angles_str))
    else:
        log.info('   *** Mirror angle is set at %s mrad' % params.Mirr_Ang)   

    log.info('   *** Move to %s mrad instead of %s?' % (angle_calibrated, params.Mirr_Ang))
    if util.yes_or_no('   *** Yes or No'):
        log.info(' ')
        log.info('   *** change to pink  *** ')

        params.Mirr_Ang = params.Mirr_Ang
        # set mirror and beamline motor positons
        params.Mirr_YAvg = lookup[angle_calibrated]["Mirr_YAvg"] 

        params.DMM_USY_OB = lookup[angle_calibrated]["DMM_USY_OB"] 
        params.DMM_USY_IB = lookup[angle_calibrated]["DMM_USY_IB"]
        params.DMM_DSY = lookup[angle_calibrated]["DMM_DSY"]
        params.DMM_USX = lookup[angle_calibrated]["DMM_USX"]
        params.DMM_DSX = lookup[angle_calibrated]["DMM_DSX"]

        params.XIA_Slits_Y = lookup[angle_calibrated]["XIASlitY"]          
        params.XIA_Slits_H_Center = lookup[angle_calibrated]["Slit1Hcenter"] 

        params.filter =  lookup[angle_calibrated]["Filter"]

        energy_change_PVs = epics_move.init_energy_change_PVs()
        
        # move mirror and beamline motor positons
        epics_move.close_shutters(energy_change_PVs, params)

        epics_move.move_filter(energy_change_PVs, params)
        epics_move.move_mirror(energy_change_PVs, params)
        epics_move.move_DMM_X(energy_change_PVs, params)
        epics_move.move_DMM_Y(energy_change_PVs, params)
        
        epics_move.move_xia_slits(energy_change_PVs, params)
            
        log.info(' ')
        log.info('   *** change to pink: Done!  *** ')
       

    else:
        log.info(' ')
        log.warning('   *** energy not changed')

def set_white(params):

    log.info('   *** changing white?')
    if util.yes_or_no('   *** Yes or No'):
        log.info(' ')
        log.info('   *** changing to white  *** ')

        # set dmm and beamline motor positons
        params.filter = 0
        params.Mirr_YAvg = -4
        params.Mirr_Ang = 0
        params.DMM_USX = 50
        params.DMM_DSX = 50
        params.DMM_USY_OB = -16
        params.DMM_USY_IB = -16
        params.DMM_DSY = -16
        params.XIA_Slits_H_Center = 7.2
        params.XIA_Slits_Y = -1.65

        energy_change_PVs = epics_move.init_energy_change_PVs()
        # move dmm and beamline motor positons
        epics_move.close_shutters(energy_change_PVs, params)
        epics_move.move_filter(energy_change_PVs, params)
        epics_move.move_mirror(energy_change_PVs, params)
        epics_move.move_DMM_X(energy_change_PVs, params)
        epics_move.move_DMM_Y(energy_change_PVs, params)
        epics_move.move_xia_slits(energy_change_PVs, params)

    else:
        log.info(' ')
        log.warning('   *** energy not changed')


def set_energy(params):

    log.info('changing energy')

    lookup={
    "55.000" : {"Mirr_Ang": 1.200, "Mirr_YAvg":  0.2, "DMM_USY_OB": -5.1, "DMM_USY_IB": -5.1, "DMM_DSY": -5.1, "USArm": 0.95, "DSArm": 0.973 , "M2Y": 11.63, "DMM_USX":27.5, "DMM_DSX": 27.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 21.45, "filter": 0},           
    "50.000" : {"Mirr_Ang": 1.500, "Mirr_YAvg": -0.2, "DMM_USY_OB": -5.1, "DMM_USY_IB": -5.1, "DMM_DSY": -5.1, "USArm": 1.00, "DSArm": 1.022 , "M2Y": 12.58, "DMM_USX":27.5, "DMM_DSX": 27.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 24.05, "filter": 0},           
    "45.000" : {"Mirr_Ang": 1.500, "Mirr_YAvg": -0.2, "DMM_USY_OB": -5.1, "DMM_USY_IB": -5.1, "DMM_DSY": -5.1, "USArm": 1.05, "DSArm": 1.072 , "M2Y": 13.38, "DMM_USX":27.5, "DMM_DSX": 27.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 25.05, "filter": 0},           
    "40.000" : {"Mirr_Ang": 1.500, "Mirr_YAvg": -0.2, "DMM_USY_OB": -5.1, "DMM_USY_IB": -5.1, "DMM_DSY": -5.1, "USArm": 1.10, "DSArm": 1.124 , "M2Y": 13.93, "DMM_USX":27.5, "DMM_DSX": 27.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 23.35, "filter": 0},           
    "35.000" : {"Mirr_Ang": 2.000, "Mirr_YAvg": -0.2, "DMM_USY_OB": -3.8, "DMM_USY_IB": -3.8, "DMM_DSY": -3.7, "USArm": 1.25, "DSArm": 1.2745, "M2Y": 15.57, "DMM_USX":27.5, "DMM_DSX": 27.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 26.35, "filter": 0},           
    "31.000" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.10, "DSArm": 1.121 , "M2Y": 12.07, "DMM_USX":82.5, "DMM_DSX": 82.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 28.35, "filter": 0},           
    "27.400" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.15, "DSArm": 1.169 , "M2Y": 13.71, "DMM_USX":82.5, "DMM_DSX": 82.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 29.35, "filter": 0},           
    "24.900" : {"Mirr_Ang": 2.657, "Mirr_YAvg": -0.2, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.2, "USArm": 1.20, "DSArm": 1.2235, "M2Y": 14.37, "DMM_USX":82.5, "DMM_DSX": 82.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 30.35, "filter": 0},           
    "22.700" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.25, "DSArm": 1.271 , "M2Y": 15.57, "DMM_USX":82.5, "DMM_DSX": 82.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 31.35, "filter": 0},           
    "21.100" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.30, "DSArm": 1.3225, "M2Y": 15.67, "DMM_USX":82.5, "DMM_DSX": 82.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 32.35, "filter": 0},           
    "20.200" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.35, "DSArm": 1.373 , "M2Y": 17.04, "DMM_USX":82.5, "DMM_DSX": 82.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 33.35, "filter": 0},           
    "18.900" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.40, "DSArm": 1.4165, "M2Y": 17.67, "DMM_USX":82.5, "DMM_DSX": 82.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 34.35, "filter": 0},           
    "17.600" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.45, "DSArm": 1.472 , "M2Y": 18.89, "DMM_USX":82.5, "DMM_DSX": 82.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 34.35, "filter": 4},           
    "16.800" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.50, "DSArm": 1.5165, "M2Y": 19.47, "DMM_USX":82.5, "DMM_DSX": 82.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 52.35, "filter": 4},           
    "16.000" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.55, "DSArm": 1.568 , "M2Y": 20.57, "DMM_USX":82.5, "DMM_DSX": 82.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 53.35, "filter": 4},           
    "15.000" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.60, "DSArm": 1.6195, "M2Y": 21.27, "DMM_USX":82.5, "DMM_DSX": 82.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 54.35, "filter": 4},           
    "14.400" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.65, "DSArm": 1.67  , "M2Y": 22.27, "DMM_USX":82.5, "DMM_DSX": 82.5, "Slit1Hcenter": 7.2 ,"XIASlitsY": 51.35, "filter": 4}            
    }

    energies_str = np.array(list(lookup.keys())[:])
    energies_flt = [float(i) for i in  energies_str]

    energy_calibrated = find_nearest(energies_flt, params.energy_value)
    if float(params.energy_value) != float(energy_calibrated):
        log.warning('   *** Energy requested is %s keV, the closest calibrated energy is %s' % (params.energy_value, energy_calibrated))
        log.info('   *** Options are %s keV' % (energies_str))
    else:
        log.info('   *** Energy is set at %s keV' % params.energy_value)   

    log.info('   *** Move to %s keV instead of %s?' % (energy_calibrated, params.energy_value))  
    if util.yes_or_no('   *** Yes or No'):
        log.info(' ')
        log.info('   *** Change Energy  *** ')

        params.energy_value = energy_calibrated
        # set dmm motor and beamline positons
        params.Mirr_Ang = lookup[energy_calibrated]["Mirr_Ang"]
        params.Mirr_YAvg = lookup[energy_calibrated]["Mirr_YAvg"]

        params.DMM_USY_OB = lookup[energy_calibrated]["DMM_USY_OB"] 
        params.DMM_USY_IB = lookup[energy_calibrated]["DMM_USY_IB"]
        params.DMM_DSY = lookup[energy_calibrated]["DMM_DSY"]

        params.US_Arm = lookup[energy_calibrated]["USArm"]                
        params.DS_Arm = lookup[energy_calibrated]["DSArm"]

        params.M2Y = lookup[energy_calibrated]["M2Y"]
        params.DMM_USX = lookup[energy_calibrated]["DMM_USX"]
        params.DMM_DSX = lookup[energy_calibrated]["DMM_DSX"]

        params.XIA_Slits_H_Center = lookup[energy_calibrated]["Slit1Hcenter"]  
        params.XIA_Slits_Y = lookup[energy_calibrated]["XIASlitsY"]   

        params.filter = lookup[energy_calibrated]["filter"]   

        energy_change_PVs = epics_move.init_energy_change_PVs()
        # move ddm to set motor positions
        epics_move.close_shutters(energy_change_PVs, params)
        epics_move.move_filter(energy_change_PVs, params)
        epics_move.move_mirror(energy_change_PVs, params)
        epics_move.move_DMM_Y(energy_change_PVs, params)
        epics_move.move_DMM_arms(energy_change_PVs, params)
        epics_move.move_DMM_M2Y(energy_change_PVs, params)
        epics_move.move_DMM_X(energy_change_PVs, params)
        epics_move.move_xia_slits(energy_change_PVs, params)
            
        log.info(' ')
        log.info('   *** Change Energy: Done!  *** ')

        return energy_calibrated
    else:
        log.info(' ')
        log.warning('   *** Energy not changed')

    # log.info(lookup[energy_calibrated]["Mirr_Ang"])

    # params.Mirr_Ang = lookup[energy_calibrated]["Mirr_Ang"]
    # params.Mirr_YAvg = lookup[energy_calibrated]["Mirr_YAvg"]

    # params.DMM_USY_OB = lookup[energy_calibrated]["DMM_USY_OB"] 
    # params.DMM_USY_IB = lookup[energy_calibrated]["DMM_USY_IB"]
    # params.DMM_DSY = lookup[energy_calibrated]["DMM_DSY"]

    # params.US_Arm = lookup[energy_calibrated]["USArm"]                
    # params.DS_Arm = lookup[energy_calibrated]["DSArm"]

    # params.M2Y = lookup[energy_calibrated]["M2Y"]
    # params.DMM_USX = lookup[energy_calibrated]["DMM_USX"]
    # params.DMM_DSX = lookup[energy_calibrated]["DMM_DSX"]
    # params.XIA_Slits_Y = lookup[energy_calibrated]["XIASlitsY"]   
    # params.filter = lookup[energy_calibrated]["filter"]   


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    value = "{0:4.3f}".format(array[idx])
    return value