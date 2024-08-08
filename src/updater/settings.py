import logging
import os
import pathlib
import sys

from tufup.utils.platform_specific import ON_MAC, ON_WINDOWS

from src import APP_NAME

logger = logging.getLogger(__name__)

MODULE_DIR = pathlib.Path(__file__).resolve().parent.parent

# Are we running in a PyInstaller bundle?
FROZEN = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

# For development
DEV_DIR = MODULE_DIR.parent.parent / f'temp_{APP_NAME}'

# App directories
if ON_WINDOWS:
    # Windows per-user paths
    PER_USER_DATA_DIR = pathlib.Path(os.getenv('LOCALAPPDATA'))
    PER_USER_PROGRAMS_DIR = PER_USER_DATA_DIR / 'Programs'
elif ON_MAC:
    # macOS per-user paths
    PER_USER_DATA_DIR = pathlib.Path.home() / 'Library'
    PER_USER_PROGRAMS_DIR = pathlib.Path.home() / 'Applications'
else:
    raise NotImplementedError('Unsupported platform')

PROGRAMS_DIR = PER_USER_PROGRAMS_DIR if FROZEN else DEV_DIR
DATA_DIR = PER_USER_DATA_DIR if FROZEN else DEV_DIR

INSTALL_DIR = PROGRAMS_DIR / APP_NAME
UPDATE_CACHE_DIR = DATA_DIR / APP_NAME / 'update_cache'
METADATA_DIR = UPDATE_CACHE_DIR / 'metadata'
TARGET_DIR = UPDATE_CACHE_DIR / 'targets'

# Update-server urls
METADATA_BASE_URL = 'http://localhost:8000/metadata/'
TARGET_BASE_URL = 'http://localhost:8000/targets/'

# Location of trusted root metadata file
TRUSTED_ROOT_SRC = MODULE_DIR.parent / 'root.json'
TRUSTED_ROOT_DST = METADATA_DIR / 'root.json'
