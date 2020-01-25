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

    log.info('changing pink')

def set_white(params):

    log.info('changing white')

def set_energy(params):

    log.info('changing energy')

    lookup={
    "55.00" : {"Mirr_Ang": 1.200, "Mirr_YAvg":  0.2, "DMM_USY_OB": -5.1, "DMM_USY_IB": -5.1, "DMM_DSY": -5.1, "USArm": 0.95, "DSArm": 0.973 , "M2Y": 11.63, "DMM_USX":27.5, "DMM_DSX": 27.5, "XIASlitY": 21.45, "filter": 0},           
    "50.00" : {"Mirr_Ang": 1.500, "Mirr_YAvg": -0.2, "DMM_USY_OB": -5.1, "DMM_USY_IB": -5.1, "DMM_DSY": -5.1, "USArm": 1.00, "DSArm": 1.022 , "M2Y": 12.58, "DMM_USX":27.5, "DMM_DSX": 27.5, "XIASlitY": 24.05, "filter": 0},           
    "45.00" : {"Mirr_Ang": 1.500, "Mirr_YAvg": -0.2, "DMM_USY_OB": -5.1, "DMM_USY_IB": -5.1, "DMM_DSY": -5.1, "USArm": 1.05, "DSArm": 1.072 , "M2Y": 13.38, "DMM_USX":27.5, "DMM_DSX": 27.5, "XIASlitY": 25.05, "filter": 0},           
    "40.00" : {"Mirr_Ang": 1.500, "Mirr_YAvg": -0.2, "DMM_USY_OB": -5.1, "DMM_USY_IB": -5.1, "DMM_DSY": -5.1, "USArm": 1.10, "DSArm": 1.124 , "M2Y": 13.93, "DMM_USX":27.5, "DMM_DSX": 27.5, "XIASlitY": 23.35, "filter": 0},           
    "35.00" : {"Mirr_Ang": 2.000, "Mirr_YAvg": -0.2, "DMM_USY_OB": -3.8, "DMM_USY_IB": -3.8, "DMM_DSY": -3.7, "USArm": 1.25, "DSArm": 1.2745, "M2Y": 15.57, "DMM_USX":27.5, "DMM_DSX": 27.5, "XIASlitY": 26.35, "filter": 0},           
    "31.00" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.10, "DSArm": 1.121 , "M2Y": 12.07, "DMM_USX":82.5, "DMM_DSX": 82.5, "XIASlitY": 28.35, "filter": 0},           
    "27.40" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.15, "DSArm": 1.169 , "M2Y": 13.71, "DMM_USX":82.5, "DMM_DSX": 82.5, "XIASlitY": 29.35, "filter": 0},           
    "24.90" : {"Mirr_Ang": 2.657, "Mirr_YAvg": -0.2, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.2, "USArm": 1.20, "DSArm": 1.2235, "M2Y": 14.37, "DMM_USX":82.5, "DMM_DSX": 82.5, "XIASlitY": 30.35, "filter": 0},           
    "22.70" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.25, "DSArm": 1.271 , "M2Y": 15.57, "DMM_USX":82.5, "DMM_DSX": 82.5, "XIASlitY": 31.35, "filter": 0},           
    "21.10" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.30, "DSArm": 1.3225, "M2Y": 15.67, "DMM_USX":82.5, "DMM_DSX": 82.5, "XIASlitY": 32.35, "filter": 0},           
    "20.20" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.35, "DSArm": 1.373 , "M2Y": 17.04, "DMM_USX":82.5, "DMM_DSX": 82.5, "XIASlitY": 33.35, "filter": 0},           
    "18.90" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.40, "DSArm": 1.4165, "M2Y": 17.67, "DMM_USX":82.5, "DMM_DSX": 82.5, "XIASlitY": 34.35, "filter": 0},           
    "17.60" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.45, "DSArm": 1.472 , "M2Y": 18.89, "DMM_USX":82.5, "DMM_DSX": 82.5, "XIASlitY": 34.35, "filter": 4},           
    "16.80" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.50, "DSArm": 1.5165, "M2Y": 19.47, "DMM_USX":82.5, "DMM_DSX": 82.5, "XIASlitY": 52.35, "filter": 4},           
    "16.00" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.55, "DSArm": 1.568 , "M2Y": 20.57, "DMM_USX":82.5, "DMM_DSX": 82.5, "XIASlitY": 53.35, "filter": 4},           
    "15.00" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.60, "DSArm": 1.6195, "M2Y": 21.27, "DMM_USX":82.5, "DMM_DSX": 82.5, "XIASlitY": 54.35, "filter": 4},           
    "14.40" : {"Mirr_Ang": 2.657, "Mirr_YAvg":  0.0, "DMM_USY_OB": -0.1, "DMM_USY_IB": -0.1, "DMM_DSY": -0.1, "USArm": 1.65, "DSArm": 1.67  , "M2Y": 22.27, "DMM_USX":82.5, "DMM_DSX": 82.5, "XIASlitY": 51.35, "filter": 4}            
    }

    energies_str = np.array(list(lookup.keys())[:])
    energies_flt = [float(i) for i in  energies_str]

    energy_calibrated = find_nearest(energies_flt, params.set)
    if float(params.set) != float(energy_calibrated):
        log.warning('   *** Energy requested is %s keV, the closest calibrated energy is %s' % (params.set, energy_calibrated))
        log.info('   *** Options are %s keV' % (energies_str))
    else:
        log.info('   *** Energy is set at %s keV' % params.set)   

    log.info('   *** Move to %s keV instead of %s?' % (energy_calibrated, params.set))  
    if util.yes_or_no('Yes or No'):
        log.info(' ')
        log.info('   *** Change Energy  *** ')

        # set dmm motor positons
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
        params.XIA_Slit_Y = lookup[energy_calibrated]["XIASlitY"]   
        params.filter = lookup[energy_calibrated]["filter"]   

        energy_change_PVs = epics_move.init_energy_change_PVs()
        # move ddm to set motor positions
        epics_move.move_filter(energy_change_PVs, params)
        epics_move.move_mirror(energy_change_PVs, params)
        epics_move.move_DMM_Y(energy_change_PVs, params)
        epics_move.move_DMM_arms(energy_change_PVs, params)
        epics_move.move_DMM_M2Y(energy_change_PVs, params)
        epics_move.move_DMM_X(energy_change_PVs, params)
        epics_move.move_xia_slits_Y(energy_change_PVs, params)
            
        log.info(' ')
        log.info('   *** Change Energy: Done!  *** ')

        return energy_calibrated
    else:
        log.info(' ')
        log.warning('   *** Energy not changed')

    log.info(lookup[energy_calibrated]["Mirr_Ang"])

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
    params.XIA_Slit_Y = lookup[energy_calibrated]["XIASlitY"]   
    params.filter = lookup[energy_calibrated]["filter"]   



def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    value = "{0:4.2f}".format(array[idx])
    return value