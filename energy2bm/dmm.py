import os
import sys
import time
import shutil
from pathlib import Path
import numpy as np

from energy2bm import util
from energy2bm import epics_move
from energy2bm import log

def set_default_config(params):
    
    log.info('set default motor values')
    lookup = {"Mono":{
    "50.000" : {"mirror_angle": 1.200, "mirror_vertical_position":  0.2, "dmm_usy_ob": -5.1, "dmm_usy_ib": -5.1, "dmm_dsy": -5.1, "dmm_us_arm": 0.95, "dmm_ds_arm": 0.973 , "dmm_m2y": 11.63, "dmm_usx": 27.5, "dmm_dsx": 27.5, "a_slits_h_center": 7.2,  "xia_slits_y": 19.65, "filter": 0,  "table_y": 0.00, "camera_y": -8.9, "foil": 'None'  },
    "45.000" : {"mirror_angle": 1.500, "mirror_vertical_position": -0.2, "dmm_usy_ob": -5.1, "dmm_usy_ib": -5.1, "dmm_dsy": -5.1, "dmm_us_arm": 1.00, "dmm_ds_arm": 1.022 , "dmm_m2y": 12.58, "dmm_usx": 27.5, "dmm_dsx": 27.5, "a_slits_h_center": 7.2,  "xia_slits_y": 23.20, "filter": 0,  "table_y": 0.00, "camera_y": -6.3, "foil": 'None'  },
    "40.000" : {"mirror_angle": 1.500, "mirror_vertical_position": -0.2, "dmm_usy_ob": -5.1, "dmm_usy_ib": -5.1, "dmm_dsy": -5.1, "dmm_us_arm": 1.05, "dmm_ds_arm": 1.072 , "dmm_m2y": 13.38, "dmm_usx": 27.5, "dmm_dsx": 27.5, "a_slits_h_center": 7.2,  "xia_slits_y": 24.20, "filter": 0,  "table_y": 0.00, "camera_y": -5.3, "foil": 'None'  },
    # "35.500" : {"mirror_angle": 1.500, "mirror_vertical_position": -0.2, "dmm_usy_ob": -5.1, "dmm_usy_ib": -5.1, "dmm_dsy": -5.1, "dmm_us_arm": 1.10, "dmm_ds_arm": 1.124 , "dmm_m2y": 13.93, "dmm_usx": 27.5, "dmm_dsx": 27.5, "a_slits_h_center": 7.2,  "xia_slits_y": 24.50, "filter": 0},
    # "32.000" : {"mirror_angle": 2.000, "mirror_vertical_position": -0.2, "dmm_usy_ob": -3.8, "dmm_usy_ib": -3.8, "dmm_dsy": -3.7, "dmm_us_arm": 1.25, "dmm_ds_arm": 1.2745, "dmm_m2y": 15.57, "dmm_usx": 27.5, "dmm_dsx": 27.5, "a_slits_h_center": 7.2,  "xia_slits_y": 28.70, "filter": 0},
    # "31.000" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.10, "dmm_ds_arm": 1.121 , "dmm_m2y": 12.07, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 29.35, "filter": 0},
    # "27.400" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.15, "dmm_ds_arm": 1.169 , "dmm_m2y": 13.71, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 29.95, "filter": 0},
    # "24.900" : {"mirror_angle": 2.657, "mirror_vertical_position": -0.2, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.2, "dmm_us_arm": 1.20, "dmm_ds_arm": 1.2235, "dmm_m2y": 14.37, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 30.15, "filter": 0},
    # "22.700" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.25, "dmm_ds_arm": 1.271 , "dmm_m2y": 15.57, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 32.25, "filter": 0},
    # "21.100" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.30, "dmm_ds_arm": 1.3225, "dmm_m2y": 15.67, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 33.15, "filter": 0},
    # "20.200" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.35, "dmm_ds_arm": 1.373 , "dmm_m2y": 17.04, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 33.95, "filter": 0},           
    # "18.900" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.40, "dmm_ds_arm": 1.4165, "dmm_m2y": 17.67, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 34.95, "filter": 0},           
    # "17.600" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.45, "dmm_ds_arm": 1.472 , "dmm_m2y": 18.89, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 35.95, "filter": 4},           
    # "16.800" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.50, "dmm_ds_arm": 1.5165, "dmm_m2y": 19.47, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 36.85, "filter": 4},           
    # "16.000" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.55, "dmm_ds_arm": 1.568 , "dmm_m2y": 20.57, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 37.85, "filter": 4},           
    # "15.000" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.60, "dmm_ds_arm": 1.6195, "dmm_m2y": 21.27, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 38.85, "filter": 4},           
    # "14.400" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.65, "dmm_ds_arm": 1.67  , "dmm_m2y": 22.27, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 39.85, "filter": 4},
    "09.660" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 2.10, "dmm_ds_arm": 2.143, "dmm_m2y": 32.72, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 48.75, "filter": 4,  "table_y": 0.00, "camera_y": 21.20, "foil": 'Zn'  },
    "17.040" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.38, "dmm_ds_arm": 1.418, "dmm_m2y": 17.97, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 34.45, "filter": 4,  "table_y": 0.00, "camera_y":  6.30, "foil": 'Y'   },
    "18.000" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.33, "dmm_ds_arm": 1.370, "dmm_m2y": 17.15, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 33.65, "filter": 4,  "table_y": 0.00, "camera_y":  5.40, "foil": 'Zr'  },
    "18.990" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.28, "dmm_ds_arm": 1.325, "dmm_m2y": 16.06, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 32.85, "filter": 4,  "table_y": 0.00, "camera_y":  4.60, "foil": 'Nb'  },
    "20.000" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.24, "dmm_ds_arm": 1.280, "dmm_m2y": 15.13, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 32.15, "filter": 4,  "table_y": 0.00, "camera_y":  3.80, "foil": 'Mo'  },
    "23.220" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.13, "dmm_ds_arm": 1.172, "dmm_m2y": 13.00, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 29.85, "filter": 4,  "table_y": 0.00, "camera_y":  1.50, "foil": 'Rh'  },
    "24.350" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.11, "dmm_ds_arm": 1.150, "dmm_m2y": 12.60, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 29.45, "filter": 4,  "table_y": 0.00, "camera_y":  1.00, "foil": 'Pd'  },
    "25.510" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -0.1, "dmm_usy_ib": -0.1, "dmm_dsy": -0.1, "dmm_us_arm": 1.07, "dmm_ds_arm": 1.103, "dmm_m2y": 11.58, "dmm_usx": 82.5, "dmm_dsx": 82.5, "a_slits_h_center": 7.2,  "xia_slits_y": 28.55, "filter": 4,  "table_y": 0.00, "camera_y":  0.10, "foil": 'Ag'  }},
    "Pink": {
    # "55.000" : {"mirror_angle": 1.500, "mirror_vertical_position": -0.1, "dmm_usy_ob": -10,  "dmm_usy_ib": -10,  "dmm_dsy": -10,                                                              "dmm_usx": 50,   "dmm_dsx": 50,   "a_slits_h_center": 4.85, "xia_slits_y":  8.75, "filter": 0},
    # "50.000" : {"mirror_angle": 1.800, "mirror_vertical_position":  0.0, "dmm_usy_ob": -10,  "dmm_usy_ib": -10,  "dmm_dsy": -10,                                                              "dmm_usx": 50,   "dmm_dsx": 50,   "a_slits_h_center": 4.85, "xia_slits_y": 11.75, "filter": 0},
    # "45.000" : {"mirror_angle": 2.000, "mirror_vertical_position":  0.0, "dmm_usy_ob": -10,  "dmm_usy_ib": -10,  "dmm_dsy": -10,                                                              "dmm_usx": 50,   "dmm_dsx": 50,   "a_slits_h_center": 7.5,  "xia_slits_y": 13.75, "filter": 0},
    # "40.000" : {"mirror_angle": 2.100, "mirror_vertical_position":  0.0, "dmm_usy_ob": -10,  "dmm_usy_ib": -10,  "dmm_dsy": -10,                                                              "dmm_usx": 50,   "dmm_dsx": 50,   "a_slits_h_center": 7.5,  "xia_slits_y": 14.75, "filter": 0},
    "30.000" : {"mirror_angle": 2.657, "mirror_vertical_position":  0.0, "dmm_usy_ob": -10,  "dmm_usy_ib": -10,  "dmm_dsy": -10,                                                              "dmm_usx": 50,   "dmm_dsx": 50,   "a_slits_h_center": 7.2,  "xia_slits_y": 18.75, "filter": 0}},
    "White": {
    "100.000": {"mirror_angle": 0,     "mirror_vertical_position":  -4,  "dmm_usy_ob": -16,  "dmm_usy_ib": -16,  "dmm_dsy": -16,                                                              "dmm_usx": 50,   "dmm_dsx": 50,   "a_slits_h_center": 7.2,  "xia_slits_y": -1.65, "filter": 0}}}

    energies_str = np.array(list(lookup[params.mode].keys())[:])
    energies_flt = [float(i) for i in  energies_str]
    energy_calibrated = util.find_nearest(energies_flt, params.energy_value)
    if float(params.energy_value) != float(energy_calibrated):
        log.warning('   *** Energy requested is %s keV, the closest calibrated energy is %s' % (params.energy_value, energy_calibrated))
        log.info('   *** Options are %s keV' % (energies_str))
        log.info('   *** Energy is set at %s keV' % params.energy_value)   
        log.info('   *** Move to %s keV instead of %s?' % (energy_calibrated, params.energy_value))  
    log.info('   *** Change Energy for %s as %s *** ' % (params.mode, energy_calibrated) )

    params.energy_value = energy_calibrated

    # set dmm motor and beamline positons
    params.mirror_angle = lookup[params.mode][energy_calibrated]["mirror_angle"]
    params.mirror_vertical_position = lookup[params.mode][energy_calibrated]["mirror_vertical_position"]
    params.dmm_usy_ob = lookup[params.mode][energy_calibrated]["dmm_usy_ob"] 
    params.dmm_usy_ib = lookup[params.mode][energy_calibrated]["dmm_usy_ib"]
    params.dmm_dsy = lookup[params.mode][energy_calibrated]["dmm_dsy"]

    if(params.mode=="mono"):
        params.dmm_us_arm = lookup[params.mode][energy_calibrated]["dmm_us_arm"]                
        params.dmm_ds_arm = lookup[params.mode][energy_calibrated]["dmm_ds_arm"]
        params.dmm_m2y = lookup[params.mode][energy_calibrated]["dmm_m2y"]

    params.dmm_usx = lookup[params.mode][energy_calibrated]["dmm_usx"]
    params.dmm_dsx = lookup[params.mode][energy_calibrated]["dmm_dsx"]
    params.a_slits_h_center = lookup[params.mode][energy_calibrated]["a_slits_h_center"]  
    params.xia_slits_y = lookup[params.mode][energy_calibrated]["xia_slits_y"]   
    params.filter = lookup[params.mode][energy_calibrated]["filter"]   
    return 0

def move(params):

    if not util.yes_or_no('   *** Yes or No'):                
        log.info(' ')
        log.warning('   *** Energy not changed')
        return False

    log.info('move motors')
    energy_change_PVs = epics_move.init_energy_change_PVs()
    
    epics_move.close_shutters(energy_change_PVs, params)
    epics_move.move_filter(energy_change_PVs, params)
    epics_move.move_mirror(energy_change_PVs, params)

    if(params.mode=="mono"):
        epics_move.move_DMM_Y(energy_change_PVs, params)
        epics_move.move_DMM_arms(energy_change_PVs, params)
        epics_move.move_DMM_dmm_m2y(energy_change_PVs, params)
        epics_move.move_DMM_X(energy_change_PVs, params)
    elif(params.mode=="pink" or params.mode=="white"):            
        epics_move.move_DMM_X(energy_change_PVs, params)
        epics_move.move_DMM_Y(energy_change_PVs, params)        

    epics_move.move_xia_slits(energy_change_PVs, params)

    epics_move.energy_pv(energy_change_PVs, params)

    log.info(' ')
    log.info('   *** Change Energy: Done!  *** ')
    return True
