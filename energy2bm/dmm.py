import os
import sys
import json
import time
import shutil
import numpy as np

from pathlib import Path

from energy2bm import util
from energy2bm import epics_move
from energy2bm import log

data_path = Path(__file__).parent / 'data'


def set_default_config(params):
    log.info('set default motor values')
    # Load DMM lookup table from the JSON file
    with open(os.path.join(data_path, 'dmm.json')) as json_file:
        lookup = json.load(json_file)
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

    if(params.mode=="Mono"):
        params.dmm_us_arm = lookup[params.mode][energy_calibrated]["dmm_us_arm"]                
        params.dmm_ds_arm = lookup[params.mode][energy_calibrated]["dmm_ds_arm"]
        params.dmm_m2y = lookup[params.mode][energy_calibrated]["dmm_m2y"]

    params.dmm_usx = lookup[params.mode][energy_calibrated]["dmm_usx"]
    params.dmm_dsx = lookup[params.mode][energy_calibrated]["dmm_dsx"]
    params.filter = lookup[params.mode][energy_calibrated]["filter"]   
    params.table_y = lookup[params.mode][energy_calibrated]["table_y"]   
    params.flag = lookup[params.mode][energy_calibrated]["flag"]   
    return 0

def move(params):

    if not util.yes_or_no('   *** Yes or No'):                
        log.info(' ')
        log.warning('   *** Energy not changed')
        return False

    log.info('move motors')
    energy_change_PVs = epics_move.init_energy_change_PVs(params)
    
    epics_move.close_shutters(energy_change_PVs, params)
    epics_move.move_filter(energy_change_PVs, params)
    epics_move.move_mirror(energy_change_PVs, params)

    if(params.mode=="Mono"):
        epics_move.move_DMM_Y(energy_change_PVs, params)
        epics_move.move_DMM_arms(energy_change_PVs, params)
        epics_move.move_DMM_dmm_m2y(energy_change_PVs, params)
        epics_move.move_DMM_X(energy_change_PVs, params)
    elif(params.mode=="Pink" or params.mode=="White"):            
        epics_move.move_DMM_X(energy_change_PVs, params)
        epics_move.move_DMM_Y(energy_change_PVs, params)        

    epics_move.move_table(energy_change_PVs, params)
    epics_move.move_flag(energy_change_PVs, params)

    epics_move.energy_pv(energy_change_PVs, params)

    log.info(' ')
    log.info('   *** Change Energy: Done!  *** ')
    return True
