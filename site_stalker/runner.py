from site_stalker.stalk import SiteStalker
from site_stalker.notify import UserNotify
from loguru import logger
from pathlib import Path
import sys

root_dir = Path(__file__).resolve().parent.parent
config_dir = root_dir.joinpath('etc')
config_file = config_dir.joinpath('config.yaml')
if not config_file.exists():
    logger.error(f'no configuration file found in {config_dir}, exiting...')
    sys.exit()

s_stalker = SiteStalker(config_file)
s_notifier = UserNotify(config_file)
logger.info('audit=site_stalker action=starting_up event=successfully_loaded_classes')

for _site in s_stalker.compare_websites():
    if _site is True:
        s_notifier.notify_parties(_site)
