
from epics import PV
from energy2bm import log
import time

TESTING = False

ShutterA_Open_Value = 1
ShutterA_Close_Value = 0
ShutterB_Open_Value = 1
ShutterB_Close_Value = 0

def init_energy_change_PVs():

    energy_change_PVs = {}

    # shutter pv's
    energy_change_PVs['ShutterA_Open'] = PV('2bma:A_shutter:open.VAL')
    energy_change_PVs['ShutterA_Close'] = PV('2bma:A_shutter:close.VAL')
    energy_change_PVs['ShutterA_Move_Status'] = PV('PA:02BM:STA_A_FES_OPEN_PL')
    energy_change_PVs['ShutterB_Open'] = PV('2bma:B_shutter:open.VAL')
    energy_change_PVs['ShutterB_Close'] = PV('2bma:B_shutter:close.VAL')
    energy_change_PVs['ShutterB_Move_Status'] = PV('PA:02BM:STA_B_SBS_OPEN_PL')


    energy_change_PVs['filter'] = PV('2bma:fltr1:select.VAL')
    energy_change_PVs['mirror_angle'] = PV('2bma:M1angl.VAL')
    energy_change_PVs['mirror_vertical_position'] = PV('2bma:M1avg.VAL')
    
    energy_change_PVs['dmm_usx'] = PV('2bma:m25.VAL')
    energy_change_PVs['dmm_dsx'] = PV('2bma:m28.VAL')
    energy_change_PVs['dmm_usy_ob'] = PV('2bma:m26.VAL')
    energy_change_PVs['dmm_usy_ib'] = PV('2bma:m27.VAL')
    energy_change_PVs['dmm_dsy'] = PV('2bma:m29.VAL')

    energy_change_PVs['dmm_us_arm'] = PV('2bma:m30.VAL')
    energy_change_PVs['dmm_ds_arm'] = PV('2bma:m31.VAL')
    energy_change_PVs['dmm_m2y'] = PV('2bma:m32.VAL')

    energy_change_PVs['xia_slits_y'] = PV('2bma:m7.VAL')
    energy_change_PVs['a_slits_h_center'] = PV('2bma:Slit1Hcenter.VAL')

    energy_change_PVs['Energy'] = PV('2bmS1:ExpInfo:Energy.VAL')
    energy_change_PVs['Energy_Mode'] = PV('2bmS1:ExpInfo:EnergyMode.VAL')
 
    return energy_change_PVs


def energy_pv(energy_change_PVs, params):

    energy_change_PVs['Energy_Mode'].put(params.mode, wait=True)
    energy_change_PVs['Energy'].put(params.energy_value, wait=True)


def move_filter(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving filters')

    if TESTING:
        log.warning('     *** testing mode:  set filter:  %s ' % params.filter)
    else:
        log.info('     *** Set filter:  %s ' % params.filter)
        energy_change_PVs['filter'].put(params.filter, wait=True)


def move_mirror(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving mirror')

    if TESTING:
        log.warning('     *** testing mode:  set mirror vertical position %s mm' % params.mirror_vertical_position)
        log.warning('     *** testing mode:  set mirror angle %s mrad' % params.mirror_angle)
    else:
        log.info('     *** mirror_vertical_position %s mm' % params.mirror_vertical_position)
        energy_change_PVs['mirror_vertical_position'].put(params.mirror_vertical_position, wait=True)
        time.sleep(1) 
        log.info('     *** mirror_angle %s mrad' % params.mirror_angle)
        energy_change_PVs['mirror_angle'].put(params.mirror_angle, wait=True)
        time.sleep(1) 


def move_DMM_Y(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving dmm y')

    if TESTING:
        log.warning('     *** testing mode:  set dmm usy ob %s mm' % params.dmm_usy_ob) 
        log.warning('     *** testing mode:  set dmm usy ib %s mm' % params.dmm_usy_ib)    
        log.warning('     *** testing mode:  set dmm dsy %s mm' % params.dmm_dsy)        
    else:
        log.info('     *** dmm usy ob %s mm' % params.dmm_usy_ob) 
        energy_change_PVs['dmm_usy_ob'].put(params.dmm_usy_ob, wait=False)
        log.info('     *** dmm usy ib %s mm' % params.dmm_usy_ib)    
        energy_change_PVs['dmm_usy_ib'].put(params.dmm_usy_ib, wait=False)
        log.info('     *** dmm_dsy %s mm' % params.dmm_dsy)        
        energy_change_PVs['dmm_dsy'].put(params.dmm_dsy, wait=True)
        time.sleep(3) 


def move_DMM_arms(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving dmm arms')

    if TESTING:
        log.warning('     *** testing mode:  set DMM dmm_us_arm %s mm' % params.dmm_us_arm) 
        log.warning('     *** testing mode:  set DMM dmm_ds_arm %s mm' % params.dmm_ds_arm) 
    else:    
        log.info('     *** moving dmm us arm %s mm' % params.dmm_us_arm) 
        energy_change_PVs['dmm_us_arm'].put(params.dmm_us_arm, wait=False, timeout=1000.0)
        log.info('     *** moving dmm ds arm %s mm' % params.dmm_ds_arm) 
        energy_change_PVs['dmm_ds_arm'].put(params.dmm_ds_arm, wait=True, timeout=1000.0)
        time.sleep(3)


def move_DMM_dmm_m2y(energy_change_PVs, params):    

    log.info(' ')
    log.info('     *** moving dmm m2y')

    if TESTING:
        log.warning('     *** testing mode:  set dmm m2y %s mm' % params.dmm_m2y) 
    else:
        log.info('     *** moving  dmm m2y %s mm' % params.dmm_m2y) 
        energy_change_PVs['dmm_m2y'].put(params.dmm_m2y, wait=True, timeout=1000.0)


def move_DMM_X(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving dmm x')

    if TESTING:
        log.warning('     *** testing mode:  set dmm usx %s mm' % params.dmm_usx)
        log.warning('     *** testing mode:  set dmm dsx %s mm' % params.dmm_dsx)
    else:
        log.info('     *** moving dmm usx %s mm' % params.dmm_usx)
        energy_change_PVs['dmm_usx'].put(params.dmm_usx, wait=False)
        log.info('     *** moving dmm dsx %s mm' % params.dmm_dsx)
        energy_change_PVs['dmm_dsx'].put(params.dmm_dsx, wait=True)
        time.sleep(3) 


def move_xia_slits(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving xia slits')

    if TESTING:
        log.warning('     *** testing mode:  set A slits h center  %s mm' % params.a_slits_h_center) 
        log.warning('     *** testing mode:  set xia slits y %s mm' % params.xia_slits_y) 
    else:
        log.info('     *** moving A slits h center  %s mm' % params.a_slits_h_center) 
        energy_change_PVs['a_slits_h_center'].put(params.a_slits_h_center, wait=True)
        log.info('     *** moving xia slits y %s mm' % params.xia_slits_y) 
        energy_change_PVs['xia_slits_y'].put(params.xia_slits_y, wait=True)


def close_shutters(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** close_shutters')
    if TESTING:
        log.warning('     *** testing mode - shutters are deactivated during the scans !!!!')
    else:
        energy_change_PVs['ShutterA_Close'].put(1, wait=True)
        # wait_pv(energy_change_PVs['ShutterA_Move_Status'], ShutterA_Close_Value)
        log.info('     *** close_shutter A: Done!')

        