import logging
import shutil
import time

from tufup.client import Client

import src
from . import settings

logger = logging.getLogger(__name__)


def progress_hook(bytes_downloaded: int, bytes_expected: int):
    progress_percent = bytes_downloaded / bytes_expected * 100
    print(f'\r{progress_percent:.1f}%', end='')

    if progress_percent >= 100:
        print('')


def update(pre: str, skip_confirmation: bool = False):
    client = Client(
        app_name=settings.APP_NAME,
        app_install_dir=settings.INSTALL_DIR,
        current_version=src.__version__,
        metadata_dir=settings.METADATA_DIR,
        metadata_base_url=settings.METADATA_BASE_URL,
        target_dir=settings.TARGET_DIR,
        target_base_url=settings.TARGET_BASE_URL,
        refresh_required=False,
    )
    new_update = client.check_for_updates(pre=pre)
    if new_update:
        # [optional] use custom metadata, if available
        if new_update.custom:
            print('changes in this update:')
            for item in new_update.custom.get('changes', []):
                print(f'\t- {item}')

        client.download_and_apply_update(
            skip_confirmation=skip_confirmation,
            progress_hook=progress_hook,
            purge_dst_dir=False,
            exclude_from_purge=None,
            log_file_name='install.log',
        )


def do_update():
    # The app must ensure dirs exist
    for dir_path in [settings.INSTALL_DIR, settings.METADATA_DIR, settings.TARGET_DIR]:
        dir_path.mkdir(exist_ok=True, parents=True)

    if not settings.TRUSTED_ROOT_DST.exists():
        shutil.copy(src=settings.TRUSTED_ROOT_SRC, dst=settings.TRUSTED_ROOT_DST)
        logger.info('Trusted root metadata copied to cache.')

    # Download and apply any available updates
    update(pre="rc", skip_confirmation=False)
