import os
import sys
import shutil
import pathlib
import argparse
import configparser
import h5py
import numpy as np

from collections import OrderedDict

from ops2bm import log
from ops2bm import __version__

LOGS_HOME = os.path.join(str(pathlib.Path.home()), 'logs')
CONFIG_FILE_NAME = os.path.join(str(pathlib.Path.home()), 'cli.conf')

SECTIONS = OrderedDict()


SECTIONS['general'] = {
    'config': {
        'default': CONFIG_FILE_NAME,
        'type': str,
        'help': "File name of configuration file",
        'metavar': 'FILE'},
    'logs-home': {
        'default': LOGS_HOME,
        'type': str,
        'help': "Log file directory",
        'metavar': 'FILE'},
    'verbose': {
        'default': False,
        'help': 'Verbose output',
        'action': 'store_true'}
        }

SECTIONS['energy'] = {
    'copy-log': {
        'default': False,
        'help': 'Verbose output',
        'action': 'store_true'},
    'set': {
        'default': 24.9,
        'type': float,
        'help': "Desired double crystal multilayer (DMM) monochromator energy"},
      }

SECTIONS['dmm-motor-positions'] = {
    'Mirr-Ang': {
        'default':  2.657,
        'type': float,
        'help': " "},
    'Mirr-YAvg': {
        'default':  -0.2,
        'type': float,
        'help': " "}, 
    'DMM-USY-OB': {
        'default':  -0.1,
        'type': float,
        'help': " "}, 
    'DMM-USY-IB': {
        'default':  -0.1,
        'type': float,
        'help': " "}, 
    'DMM-DSY': {
        'default':  -0.2,
        'type': float,
        'help': " "}, 
    'US-Arm': {
        'default':  1.20,
        'type': float,
        'help': " "}, 
    'DS-Arm': {
        'default':  1.2235,
        'type': float,
        'help': " "}, 
    'M2Y': {
        'default':  14.37,
        'type': float,
        'help': " "}, 
    'DMM-USX':  {
        'default': 82.5,
        'type': float,
        'help': " "}, 
    'DMM-DSX':  {
        'default': 82.5,
        'type': float,
        'help': " "}, 
    'XIA-Slit-Y':  {
        'default': 30.35,
        'type': float,
        'help': " "},           
      }


GENERAL_PARAMS = ('energy', 'dmm-motor-positions')
SPECIFIC_PARAMS = ('energy', 'dmm-motor-positions')

NICE_NAMES = ('General', 'DMM Energy', 'DMM Motor Positions')

def get_config_name():
    """Get the command line --config option."""
    name = CONFIG_FILE_NAME
    for i, arg in enumerate(sys.argv):
        if arg.startswith('--config'):
            if arg == '--config':
                return sys.argv[i + 1]
            else:
                name = sys.argv[i].split('--config')[1]
                if name[0] == '=':
                    name = name[1:]
                return name
    return name


def parse_known_args(parser, subparser=False):
    """
    Parse arguments from file and then override by the ones specified on the
    command line. Use *parser* for parsing and is *subparser* is True take into
    account that there is a value on the command line specifying the subparser.
    """
    if len(sys.argv) > 1:
        subparser_value = [sys.argv[1]] if subparser else []
        config_values = config_to_list(config_name=get_config_name())
        values = subparser_value + config_values + sys.argv[1:]
        #print(subparser_value, config_values, values)
    else:
        values = ""

    return parser.parse_known_args(values)[0]


def config_to_list(config_name=CONFIG_FILE_NAME):
    """
    Read arguments from config file and convert them to a list of keys and
    values as sys.argv does when they are specified on the command line.
    *config_name* is the file name of the config file.
    """
    result = []
    config = configparser.ConfigParser()

    if not config.read([config_name]):
        return []

    for section in SECTIONS:
        for name, opts in ((n, o) for n, o in SECTIONS[section].items() if config.has_option(section, n)):
            value = config.get(section, name)

            if value is not '' and value != 'None':
                action = opts.get('action', None)

                if action == 'store_true' and value == 'True':
                    # Only the key is on the command line for this action
                    result.append('--{}'.format(name))

                if not action == 'store_true':
                    if opts.get('nargs', None) == '+':
                        result.append('--{}'.format(name))
                        result.extend((v.strip() for v in value.split(',')))
                    else:
                        result.append('--{}={}'.format(name, value))

    return result
  

class Params(object):
    def __init__(self, sections=()):
        self.sections = sections + ('general', )

    def add_parser_args(self, parser):
        for section in self.sections:
            for name in sorted(SECTIONS[section]):
                opts = SECTIONS[section][name]
                parser.add_argument('--{}'.format(name), **opts)

    def add_arguments(self, parser):
        self.add_parser_args(parser)
        return parser

    def get_defaults(self):
        parser = argparse.ArgumentParser()
        self.add_arguments(parser)

        return parser.parse_args('')


def write(config_file, args=None, sections=None):
    """
    Write *config_file* with values from *args* if they are specified,
    otherwise use the defaults. If *sections* are specified, write values from
    *args* only to those sections, use the defaults on the remaining ones.
    """
    config = configparser.ConfigParser()
    for section in SECTIONS:
        config.add_section(section)
        for name, opts in SECTIONS[section].items():
            if args and sections and section in sections and hasattr(args, name.replace('-', '_')):
                value = getattr(args, name.replace('-', '_'))
                if isinstance(value, list):
                    # print(type(value), value)
                    value = ', '.join(value)
            else:
                value = opts['default'] if opts['default'] is not None else ''

            prefix = '# ' if value is '' else ''

            if name != 'config':
                config.set(section, prefix + name, str(value))


    with open(config_file, 'w') as f:
        config.write(f)


def log_values(args):
    """Log all values set in the args namespace.

    Arguments are grouped according to their section and logged alphabetically
    using the DEBUG log level thus --verbose is required.
    """
    args = args.__dict__

    log.warning('tomopy-cli status start')
    for section, name in zip(SECTIONS, NICE_NAMES):
        entries = sorted((k for k in args.keys() if k.replace('_', '-') in SECTIONS[section]))

        # print('log_values', section, name, entries)
        if entries:
            log.info(name)

            for entry in entries:
                value = args[entry] if args[entry] is not None else "-"
                if (value == 'none'):
                    log.warning("  {:<16} {}".format(entry, value))
                elif (value is not False):
                    log.info("  {:<16} {}".format(entry, value))
                elif (value is False):
                    log.warning("  {:<16} {}".format(entry, value))

    log.warning('tomopy-cli status end')


def update_log(args):
       # update tomopy.conf
        sections = GENERAL_PARAMS
        write(args.config, args=args, sections=sections)
        if (args.copy_log):
            head, tail = os.path.split(args.file_name)
            log_fname = head + os.sep + "test" + os.path.split(args.config)[1]
            try:
                shutil.copyfile(args.config, log_fname)
                log.info('  *** copied %s to %s ' % (args.config, log_fname))
            except:
                log.error('  *** attempt to copy %s to %s failed' % (args.config, log_fname))
                pass
            log.warning(' *** command to repeat the reconstruction: tomopy recon --config {:s}'.format(log_fname))