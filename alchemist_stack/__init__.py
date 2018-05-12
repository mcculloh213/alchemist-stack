# System Imports
import logging
from os import environ

# Third-Party Imports

# Local Source Imports

__author__ = 'H.D. "Chip" McCullough IV'

__version__ = '0.1.0.dev1'
VERSION = __version__

logging.basicConfig(level=environ.get('LOGLEVEL', 'INFO'))
root_logger = logging.getLogger('Alchemist Stack')
root_logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    root_logger.debug('This is a debug message')
    root_logger.info('This is some info')
    root_logger.warning('This is a warning')
    root_logger.error('This is an error')
    root_logger.critical('HOLY GOD, WE HAVE A CRITICAL FAILURE')