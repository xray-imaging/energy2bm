import os
import sys
import shutil
from pathlib import Path
from multiprocessing import cpu_count
import threading
import numpy as np
import tomopy
import dxchange

from ops2bm import log

def change_energy(params):
    log.info('... changing energy')