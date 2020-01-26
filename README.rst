=======
ops-cli
=======

**ops-cli** is commad-line-interface to operate `beamline 2bm <https://2bm-docs.readthedocs.io>`_ of the 
`APS <https://aps.anl.gov/>`_.


Installation
============

::

    $ git clone https://github.com/xray-imaging/2bm-ops.git
    $ cd 2bm-ops
    $ python setup.py install

in a prepared virtualenv or as root for system-wide installation.

.. warning:: If your python installation is in a location different from #!/usr/bin/env python please edit the first line of the bin/tomopy file to match yours.


Usage
=====

Set energy
-----------

To set the beamline energy to 20 keV::

    $ ops set_mono --energy-value 20 

to list of all available options::

    $ ops -h
  usage: ops [-h] [--config FILE] [--version]  ...

  optional arguments:
    -h, --help     show this help message and exit
    --config FILE  File name of configuration file
    --version      show program's version number and exit

  Commands:
    
      init         Create configuration file
      set_mono     Set energy
      save_mono    Save current beamline position to an energy value
      set_white    Set white
      set_pink     Set pink
      status       Show status

Configuration File
------------------

The beamline status is stored in **ops.conf**. You can create a template with::

    $ ops init

**osp2bm.conf** is constantly updated to keep track of the last stored parameters, as initalized by **init** or modified by setting a new option value. For example to set the beamline to the last energy configuration ::

    $ ops set_mono

If the beamline has been manually optimized after setting a preset energy configuration, you can save the current beamline status in the default config file **osp2bm.conf** with::  

    $ ops save_mono --energy-value 12

or you can save it in **osp2bm_12.0.conf** with::

    $ ops save_mono --energy-value 12 --copy-log

In this way you be able to restore the beamline in the optimize energy configuration with::

    $ ops set_mono --config ops2bm_12.0.conf
