'''
    Auto center for 2-BM

'''
import sys
import json
import time
from epics import PV
import h5py
import shutil
import os
# import imp
import traceback
import numpy as np
from datetime import datetime
import pathlib
import signal

import libs.aps2bm_lib as aps2bm_lib
import libs.log_lib as log_lib

import matplotlib.pylab as pl
import matplotlib.widgets as wdg


from skimage import filters
from skimage.color import rgb2gray  # only needed for incorrectly saved images
from skimage.measure import regionprops
from skimage.feature import register_translation
import numexpr as ne

global variableDict

variableDict = {
        'SampleXIn': 0, 
        'SampleXOut': 4,
        'SampleRotStart': 0.0,
        'SampleRotEnd': 180.0,
        'center': 0.0,
        'roll': 0.0,
        # ####################### DO NOT MODIFY THE PARAMETERS BELOW ###################################
        'CCD_Readout': 0.006,              # options: 1. 8bit: 0.006, 2. 16-bit: 0.01
        # 'CCD_Readout': 0.01,             # options: 1. 8bit: 0.006, 2. 16-bit: 0.01
        'Station': '2-BM-A',
        'ExposureTime': 0.1,                # to use this as default value comment the variableDict['ExposureTime'] = global_PVs['Cam1_AcquireTime'].get() line
        'IOC_Prefix': '2bmbSP1:',           # options: 1. PointGrey: '2bmbPG3:', 2. Gbe '2bmbSP1:' 
        'detector_resolution': 1.0
        }

global_PVs = {}

DetectorIdle = 0
DetectorAcquire = 1

class plot():
    def __init__(self, data): #, axis):
        self.data = data

        ax = pl.subplot(111)
        pl.subplots_adjust(left=0.25, bottom=0.25)

        self.frame = 0
        self.l = pl.imshow(self.data, cmap='gist_gray') 
        # self.l = pl.imshow(self.data[self.frame,:,:], cmap='gist_gray') 

        axcolor = 'lightgoldenrodyellow'
        axframe = pl.axes([0.25, 0.1, 0.65, 0.03])
        self.sframe = wdg.Slider(axframe, 'Frame', 0, self.data.shape[0]-1, valfmt='%0.0f')
        # self.sframe.on_changed(self.update)

        pl.show()



def getVariableDict():
    global variableDict
    return variableDict

def as_dtype(arr, dtype, copy=False):
    if not arr.dtype == dtype:
        arr = np.array(arr, dtype=dtype, copy=copy)
    return arr

def as_ndarray(arr, dtype=None, copy=False):
    if not isinstance(arr, np.ndarray):
        arr = np.array(arr, dtype=dtype, copy=copy)
    return arr

def as_float32(arr):
    arr = as_ndarray(arr, np.float32)
    return as_dtype(arr, np.float32)


def get_resolution(global_PVs, variableDict):

    def cleanup(signal, frame):
        aps2bm_lib.stop_scan(global_PVs, variableDict)
        sys.exit(0)
    signal.signal(signal.SIGINT, cleanup)

    if 'StopTheScan' in variableDict:
        aps2bm_lib.stop_scan(global_PVs, variableDict)
        return

    sampple_x = 0.1
    aps2bm_lib.pgInit(global_PVs, variableDict)
    aps2bm_lib.pgSet(global_PVs, variableDict) 

    aps2bm_lib.close_shutters(global_PVs, variableDict)
    dark_field = acquire_dark(global_PVs, variableDict)
    # plot(dark_field)

    aps2bm_lib.open_shutters(global_PVs, variableDict)
    white_field = acquire_flat(global_PVs, variableDict)
    # plot(white_field)

    log_lib.info('  *** moving X stage  to 0 mm position')
    global_PVs["Motor_SampleX"].put(0, wait=True, timeout=600.0)
    
    log_lib.info('  *** acquire first image')
    sphere_0 = normalize(acquire_image(global_PVs, variableDict), white_field, dark_field)
 
    log_lib.info('  *** moving X stage to %f mm position' % sampple_x)
    global_PVs["Motor_SampleX"].put(sampple_x, wait=True, timeout=600.0)
    sphere_1 = normalize(acquire_image(global_PVs, variableDict), white_field, dark_field)

    shift = register_translation(sphere_0, sphere_1, 1000, return_error=False)
    log_lib.info('  *** shift %f' % shift[1])

    resolution =  sampple_x / np.abs(shift[1]) * 1000.0
    log_lib.info('  *** resolution %f μm/pixel' % resolution)


    log_lib.info('  *** moving X stage back to 0 mm position')
    global_PVs["Motor_SampleX"].put(0, wait=True, timeout=600.0)

    return resolution


def normalize(arr, flat, dark, cutoff=None, out=None):
    """
    Normalize raw projection data using the flat and dark field projections.

    Parameters
    ----------
    arr : ndarray
        2D of projections.
    flat : ndarray
        2D flat field data.
    dark : ndarray
        2D dark field data.
    cutoff : float, optional
        Permitted maximum vaue for the normalized data.
    out : ndarray, optional
        Output array for result. If same as arr,
        process will be done in-place.

    Returns
    -------
    ndarray
        Normalized 2D tomographic data.
    """
    arr = as_float32(arr)
    l = np.float32(1e-5)
    log_lib.info(flat.shape)
    # flat = np.mean(flat, axis=0, dtype=np.float32)
    # dark = np.mean(dark, axis=0, dtype=np.float32)
    flat = flat.astype('float32')
    dark = dark.astype('float32')

    denom = ne.evaluate('flat')
    # denom = ne.evaluate('flat-dark')
    ne.evaluate('where(denom<l,l,denom)', out=denom)
    out = ne.evaluate('arr', out=out)
    # out = ne.evaluate('arr-dark', out=out)
    ne.evaluate('out/denom', out=out, truediv=True)
    if cutoff is not None:
        cutoff = np.float32(cutoff)
        ne.evaluate('where(out>cutoff,cutoff,out)', out=out)
    return out


def acquire_image(global_PVs, variableDict):
    nRow = global_PVs['Cam1_SizeY_RBV'].get()
    nCol = global_PVs['Cam1_SizeX_RBV'].get()

    image_size = nRow * nCol

    global_PVs['Cam1_NumImages'].put(1, wait=True)
    global_PVs['Cam1_TriggerMode'].put('Off', wait=True)
    wait_time_sec = int(variableDict['ExposureTime']) + 5

    global_PVs['Cam1_Acquire'].put(DetectorAcquire, wait=True, timeout=1000.0)
    time.sleep(0.1)
    if aps2bm_lib.wait_pv(global_PVs['Cam1_Acquire'], DetectorIdle, wait_time_sec) == False: # adjust wait time
        global_PVs['Cam1_Acquire'].put(DetectorIdle)
    
    # Get the image loaded in memory
    img_vect = global_PVs['Cam1_Image'].get(count=image_size)
    img = np.reshape(img_vect,[nRow, nCol])

    return img

def acquire_flat(global_PVs, variableDict):
    log_lib.info('  *** move sample out of the field of view')
    global_PVs['Motor_SampleX'].put(str(variableDict['SampleXOut']), wait=True, timeout=1000.0)
    log_lib.info('  *** acquire white')
    return acquire_image(global_PVs, variableDict)

def acquire_dark(global_PVs, variableDict):
    log_lib.info('  *** acquire dark')
    return acquire_image(global_PVs, variableDict)

def acquire_sphere(global_PVs, variableDict):
    log_lib.info('  *** move sphere in the field of view')
    global_PVs['Motor_SampleX'].put(str(variableDict['SampleXIn']), wait=True, timeout=1000.0)
    log_lib.info('  *** acquire sphere')
    return acquire_image(global_PVs, variableDict)

def center_of_mass(image):
    threshold_value = filters.threshold_otsu(image)
    log_lib.info("threshold_value: %f" % (threshold_value))
    labeled_foreground = (image < threshold_value).astype(int)
    properties = regionprops(labeled_foreground, image)
    return properties[0].weighted_centroid
    # return properties[0].centroid

def find_rotation_axis(global_PVs, variableDict):

    sphere_0, sphere_180 = get_0_180(global_PVs, variableDict)

    cmass_0 = center_of_mass(sphere_0)
    cmass_180 = center_of_mass(sphere_180)

    center = (cmass_180[1] + cmass_0[1]) / 2.0
    log_lib.info('  *** difference vertical center of mass %f' % (cmass_180[0] - cmass_0[0]))
    log_lib.info('  *** difference horizontal center of mass %f' % (cmass_180[1] - cmass_0[1]))
    log_lib.info('  *** ratio %f' % ((cmass_180[0] - cmass_0[0]) / (cmass_180[1] - cmass_0[1])))

    roll = np.rad2deg(np.arctan((cmass_180[0] - cmass_0[0]) / (cmass_180[1] - cmass_0[1])))
    log_lib.info("roll:%f" % (roll))
    # plot(sphere_0)
    # plot(sphere_180)
    # plot(sphere_180[:,::-1])
    
    shift = register_translation(sphere_0, sphere_180[:,::-1], 1000, return_error=False)
    log_lib.info("shift: [%f, %f]" % (shift[0],shift[1]))
    log_lib.info("Rotation axis location: %f" % (sphere_0.shape[1]/2.0 +(shift[1]/2)))
    log_lib.info("Rotation axis offset: %f" % (shift[1]/2))
    center = (sphere_0.shape[1]/2.0 +(shift[1]/2))
    roll = np.rad2deg(np.arctan(shift[0]/shift[1]))
    log_lib.info("new roll:%f" % (roll))
    # shift = register_translation(sphere_0, sphere_180, 1000, return_error=False)
    # roll = np.rad2deg(np.arctan(shift[0]/shift[1]))
    # log_lib.info("new roll2:%f" % (roll))


    return center, roll


def get_0_180(global_PVs, variableDict):

    def cleanup(signal, frame):
        aps2bm_lib.stop_scan(global_PVs, variableDict)
        sys.exit(0)
    signal.signal(signal.SIGINT, cleanup)

    if 'StopTheScan' in variableDict:
        aps2bm_lib.stop_scan(global_PVs, variableDict)
        return

    aps2bm_lib.pgInit(global_PVs, variableDict)
    aps2bm_lib.pgSet(global_PVs, variableDict) 

    aps2bm_lib.close_shutters(global_PVs, variableDict)
    dark_field = acquire_dark(global_PVs, variableDict)
    # plot(dark_field)

    aps2bm_lib.open_shutters(global_PVs, variableDict)
    white_field = acquire_flat(global_PVs, variableDict)
    # plot(white_field)

    log_lib.info('  *** moving rotary stage to 0 deg position')
    global_PVs["Motor_SampleRot"].put(0, wait=True, timeout=600.0)
    
    log_lib.info('  *** acquire sphere at 0 deg')
    sphere_0 = normalize(acquire_sphere(global_PVs, variableDict), white_field, dark_field)
 
    log_lib.info('  *** moving rotary stage to 180 deg')
    global_PVs["Motor_SampleRot"].put(180, wait=True, timeout=600.0)
    
    log_lib.info('  *** acquire sphere at 180')
    sphere_180 = normalize(acquire_sphere(global_PVs, variableDict), white_field, dark_field)

    return sphere_0, sphere_180


def center_rotation_axis(global_PVs, variableDict):

    nCol = global_PVs['Cam1_SizeX_RBV'].get()
    
    log_lib.info(' ')
    log_lib.info('  *** centering rotation axis')

    current_axis_position = global_PVs["Motor_SampleX"].get()
    log_lib.info('  *** current axis position: %f' % current_axis_position)
    time.sleep(.5)
    correction = (((nCol / 2.0) - variableDict['center']) * variableDict['detector_resolution'] / 1000.0) + current_axis_position
    log_lib.info('  *** correction: %f' % correction)

    log_lib.info('  *** moving to: %f (mm)' % correction)
    global_PVs["Motor_SampleX"].put(correction, wait=True, timeout=600.0)

    log_lib.info('  *** re-setting position from %f (mm) to 0 (mm)' % correction)
    global_PVs["Motor_SampleX_SET"].put(1, wait=True, timeout=5.0)
    time.sleep(.5)
    global_PVs["Motor_SampleX"].put(0, wait=True, timeout=5.0)
    time.sleep(.5)
    global_PVs["Motor_SampleX_SET"].put(0, wait=True, timeout=5.0)


def main():
    home = os.path.expanduser("~")
    logs_home = home + '/logs/'
    # make sure logs directory exists
    if not os.path.exists(logs_home):
        os.makedirs(logs_home)

    lfname = logs_home + 'center.log'
    # lfname = logs_home + datetime.strftime(datetime.now(), "%Y-%m-%d_%H:%M:%S") + '.log'
    log_lib.setup_logger(lfname)

    aps2bm_lib.update_variable_dict(variableDict)
    aps2bm_lib.init_general_PVs(global_PVs, variableDict)
    try:
        detector_sn = global_PVs['Cam1_SerialNumber'].get()
        if ((detector_sn == None) or (detector_sn == 'Unknown')):
            Logger("log").error('*** The Point Grey Camera with EPICS IOC prefix %s is down' % variableDict['IOC_Prefix'])
            Logger("log").error('  *** Failed!')
        else:
            log_lib.info('*** The Point Grey Camera with EPICS IOC prefix %s and serial number %s is on' \
                % (variableDict['IOC_Prefix'], detector_sn))
            variableDict['center'], variableDict['roll'] = find_rotation_axis(global_PVs, variableDict)
            variableDict['detector_resolution'] = get_resolution(global_PVs, variableDict)
            center_rotation_axis(global_PVs, variableDict) 
            # # log_lib.info('  *** rotary roll angle %f deg' % variableDict['roll'])
        
        log_lib.info('  *** moving rotary stage to 0 deg position')
        global_PVs["Motor_SampleRot"].put(0, wait=True, timeout=600.0)
        log_lib.info('  *** Done!')

    except  KeyError:
        Logger("log").error('  *** Some PV assignment failed!')
        pass


if __name__ == '__main__':
    main()
