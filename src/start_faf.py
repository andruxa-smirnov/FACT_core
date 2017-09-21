#! /usr/bin/env python3
'''
This script starts all installed FACT components
'''

import logging
import os
import signal
import sys
from subprocess import Popen, TimeoutExpired
from time import sleep

from faf_init import _setup_argparser, _setup_logging, _load_config
from helperFunctions.config import get_src_dir

PROGRAM_NAME = 'FACT Starter'
PROGRAM_DESCRIPTION = 'This script starts all installed FACT components'


def _evaluate_optional_args(args):
    optional_args = ''
    if args.debug:
        optional_args += ' -d'
    if args.silent:
        optional_args += ' -s'
    return optional_args


def _start_component(component, args):
    script_path = os.path.join(get_src_dir(), '../start_fact_{}'.format(component))
    if os.path.exists(script_path):
        logging.info('starting {}'.format(component))
        optional_args = _evaluate_optional_args(args)
        p = Popen('{} -l {} -L {} -C {} {}'.format(script_path, config['Logging']['logFile'], config['Logging']['logLevel'], args.config_file, optional_args), shell=True)
        return p
    else:
        logging.debug('{} not installed'.format(component))
        return None


def _terminate_process(process):
    if process is not None:
        process.terminate()
        try:
            process.wait(timeout=60)
        except TimeoutExpired:
            logging.error('component did not stop in time -> kill')
            process.kill()


def shutdown(signum, frame):
    global run
    logging.info('shutting down...')
    run = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

if __name__ == '__main__':
    process_list = []
    run = True
    args = _setup_argparser(name=PROGRAM_NAME, description=PROGRAM_DESCRIPTION)
    config = _load_config(args)
    _setup_logging(config, args)

    db_process = _start_component('db', args)
    sleep(2)
    frontend_process = _start_component('frontend', args)
    backend_process = _start_component('backend', args)

    while run:
        sleep(5)

    logging.debug('shutdown backend')
    _terminate_process(backend_process)
    logging.debug('shutdown frontend')
    _terminate_process(frontend_process)
    logging.debug('wait for childprocesses to stop...')
    sleep(60)
    logging.debug('shutdown db')
    _terminate_process(db_process)

    sys.exit()