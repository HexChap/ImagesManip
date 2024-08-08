import copy
import logging
import os
import pathlib
import sys

from tufup.repo import DEFAULT_KEY_MAP, DEFAULT_KEYS_DIR_NAME, DEFAULT_REPO_DIR_NAME, Repository

from src import APP_NAME, __version__

logger = logging.getLogger(__name__)

# Path to directory containing current module
MODULE_DIR = pathlib.Path(__file__).resolve().parent

# For development
DEV_DIR = MODULE_DIR / 'temp_images_manip'
PYINSTALLER_DIST_DIR_NAME = 'dist'
DIST_DIR = DEV_DIR / PYINSTALLER_DIST_DIR_NAME

# Local repo path and keys path (would normally be offline)
KEYS_DIR = DEV_DIR / DEFAULT_KEYS_DIR_NAME
REPO_DIR = DEV_DIR / DEFAULT_REPO_DIR_NAME

# Key settings
# KEY_NAME = 'my_key'
# PRIVATE_KEY_PATH = KEYS_DIR / KEY_NAME
KEY_MAP = copy.deepcopy(DEFAULT_KEY_MAP)
ENCRYPTED_KEYS = []
THRESHOLDS = dict(root=1, targets=1, snapshot=1, timestamp=1)
EXPIRATION_DAYS = dict(root=365, targets=7, snapshot=7, timestamp=1)

logging.basicConfig(level=logging.INFO)


def init():
    repo = Repository(
        app_name=APP_NAME,
        app_version_attr='src.__version__',
        repo_dir=REPO_DIR,
        keys_dir=KEYS_DIR,
        key_map=KEY_MAP,
        expiration_days=EXPIRATION_DAYS,
        encrypted_keys=ENCRYPTED_KEYS,
        thresholds=THRESHOLDS,
    )

    # Save configuration (JSON file)
    repo.save_config()

    # Initialize repository (creates keys and root metadata, if necessary)
    repo.initialize()


def add_bundle(new_version: str = None):
    try:
        bundle_dirs = [path for path in DIST_DIR.iterdir() if path.is_dir()]
    except FileNotFoundError:
        sys.exit(f'Directory not found: {DIST_DIR}\nDid you run pyinstaller?')
    else:
        if len(bundle_dirs) != 1:
            sys.exit(f'Expected one bundle, found {len(bundle_dirs)}.')
    bundle_dir = bundle_dirs[0]
    print(f'Adding bundle: {bundle_dir}')

    # Create repository instance from config file (assuming the repository
    # has already been initialized)
    repo = Repository.from_config()

    # Add new app bundle to repository (automatically reads myapp.__version__)
    repo.add_bundle(
        new_bundle_dir=bundle_dir,
        new_version=__version__ if not new_version else new_version,
        # [optional] custom metadata can be any dict (default is None)
        custom_metadata={'changes': ['new feature x added', 'bug y fixed']},
    )
    repo.publish_changes(private_key_dirs=[KEYS_DIR])

    print('Done.')


if __name__ == '__main__':
    # init()
    add_bundle()