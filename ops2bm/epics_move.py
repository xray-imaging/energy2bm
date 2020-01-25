
from epics import PV
from ops2bm import log

TESTING = True

def init_energy_change_PVs():
# def init_energy_change_PVs():

    energy_change_PVs = {}

    # shutter pv's
    energy_change_PVs['ShutterA_Open'] = PV('2bma:A_shutter:open.VAL')
    energy_change_PVs['ShutterA_Close'] = PV('2bma:A_shutter:close.VAL')
    energy_change_PVs['ShutterA_Move_Status'] = PV('PA:02BM:STA_A_FES_OPEN_PL')
    energy_change_PVs['ShutterB_Open'] = PV('2bma:B_shutter:open.VAL')
    energy_change_PVs['ShutterB_Close'] = PV('2bma:B_shutter:close.VAL')
    energy_change_PVs['ShutterB_Move_Status'] = PV('PA:02BM:STA_B_SBS_OPEN_PL')


    energy_change_PVs['Filter_Select'] = PV('2bma:fltr1:select.VAL')
    energy_change_PVs['Mirr_Ang'] = PV('2bma:M1angl.VAL')
    energy_change_PVs['Mirr_YAvg'] = PV('2bma:M1avg.VAL')
    
    energy_change_PVs['DMM_USX'] = PV('2bma:m25.VAL')
    energy_change_PVs['DMM_DSX'] = PV('2bma:m28.VAL')
    energy_change_PVs['DMM_USY_OB'] = PV('2bma:m26.VAL')
    energy_change_PVs['DMM_USY_IB'] = PV('2bma:m27.VAL')
    energy_change_PVs['DMM_DSY'] = PV('2bma:m29.VAL')

    energy_change_PVs['USArm'] = PV('2bma:m30.VAL')
    energy_change_PVs['DSArm'] = PV('2bma:m31.VAL')
    energy_change_PVs['M2Y'] = PV('2bma:m32.VAL')
                                 
    energy_change_PVs['XIASlitY'] = PV('2bma:m7.VAL')
    energy_change_PVs['Slit1Hcenter'] = PV('2bma:Slit1Hcenter.VAL')
 
    return energy_change_PVs

def move_filter(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving filters')

    if TESTING:
        log.warning('     *** testing mode. Set filter:  %s ' % params.filter)
    else:
        log.info('     *** Set filter:  %s ' % params.filter)
        # energy_change_PVs['Filter_Select'].put(params.filter, wait=True)


def move_mirror(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving mirror')

    if TESTING:
        log.warning('     *** testing mode. Mirr_YAvg %s mm' % params.Mirr_YAvg)
        log.warning('     *** testing mode. Mirr_Ang %s rad' % params.Mirr_Ang)
    else:
        log.info('Mirr_YAvg %s mm' % params.Mirr_YAvg)
        # energy_change_PVs['Mirr_YAvg'].put(params.Mirr_YAvg, wait=True)
        time.sleep(1) 
        log.info('Mirr_Ang %s rad' % params.Mirr_Ang)
        # energy_change_PVs['Mirr_Ang'].put(params.Mirr_Ang, wait=True)
        time.sleep(1) 


def move_DMM_Y(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving DMM_Y')

    if TESTING:
        log.warning('     *** testing mode. DMM_USY_OB %s mm' % params.DMM_USY_OB) 
        log.warning('     *** testing mode. DMM_USY_IB %s mm' % params.DMM_USY_IB)    
        log.warning('     *** testing mode. DMM_DSY %s mm' % params.DMM_DSY)        
    else:
        log.info('     *** DMM_USY_OB %s mm' % params.DMM_USY_OB) 
        # energy_change_PVs['DMM_USY_OB'].put(params.DMM_USY_OB, wait=False)
        log.info('     *** DMM_USY_IB %s mm' % params.DMM_USY_IB)    
        # energy_change_PVs['DMM_USY_IB'].put(params.DMM_USY_IB, wait=False)
        log.info('     *** DMM_DSY %s mm' % params.DMM_DSY)        
        # energy_change_PVs['DMM_DSY'].put(params.DMM_DSY, wait=True)
        time.sleep(3) 


def move_DMM_arms(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving DMM_arms')

    if TESTING:
        log.warning('     *** testing mode. Moving DMM USArm %s mm' % params.US_Arm) 
        log.warning('     *** testing mode. Moving DMM DSArm %s mm' % params.DS_Arm) 
    else:    
        log.info('     *** Moving DMM USArm %s mm' % params.USArm) 
        # energy_change_PVs['USArm'].put(params.USArm, wait=False, timeout=1000.0)
        log.info('     *** Moving DMM DSArm %s mm' % params.DSArm) 
        # energy_change_PVs['DSArm'].put(params.DSArm, wait=True, timeout=1000.0)
        time.sleep(3)


def move_DMM_M2Y(energy_change_PVs, params):    

    log.info(' ')
    log.info('     *** moving DMM_M2Y')

    if TESTING:
        log.warning('     *** testing mode. Moving DMM_M2Y %s mm' % params.M2Y) 
    else:
        log.info('     *** Moving DMM_M2Y %s mm' % params.M2Y) 
        # energy_change_PVs['M2Y'].put(params.M2Y, wait=True, timeout=1000.0)


def move_DMM_X(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving DMM_X')

    if TESTING:
        log.warning('     *** testing mode. DMM_USX %s mm' % params.DMM_USX)
        log.warning('     *** testing mode. DMM_DSX %s mm' % params.DMM_DSX)
    else:
        log.info('     *** DMM_USX %s mm' % params.DMM_USX)
        # energy_change_PVs['DMM_USX'].put(params.DMM_USX, wait=False)
        log.info('     *** DMM_DSX %s mm' % params.DMM_DSX)
        # energy_change_PVs['DMM_DSX'].put(params.DMM_DSX, wait=True)
        time.sleep(3) 


def move_xia_slits(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving XIA Slits')

    if TESTING:
        log.warning('     *** testing mode. Moving XIA Slits H Center  %s mm' % params.XIA_Slits_H_Center) 
        log.warning('     *** testing mode. Moving XIA Slits Y %s mm' % params.XIA_Slits_Y) 
    else:
        log.info('     *** Moving XIA Slits H Center  %s mm' % params.XIA_Slits_H_Center) 
        # energy_change_PVs['Slit1Hcenter'].put(params.XIA_Slits_H_Center, wait=True)
        log.info('     *** Moving XIA Slits Y %s mm' % params.XIA_Slits_Y) 
        # energy_change_PVs['XIASlitY'].put(params.XIASlitY, wait=True)


def close_shutters(energy_change_PVs, params):
# def close_shutters(energy_change_PVs):
    log.info(' ')
    log.info('     *** close_shutters')
    if TESTING:
        log.warning('     *** testing mode - shutters are deactivated during the scans !!!!')
    else:
        # energy_change_PVs['ShutterA_Close'].put(1, wait=True)
        # wait_pv(energy_change_PVs['ShutterA_Move_Status'], ShutterA_Close_Value)
        log.info('     *** close_shutter A: Done!')

        