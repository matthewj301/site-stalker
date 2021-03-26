#!/usr/bin/env python
import sys
import time
from pathlib import Path

import yaml
from loguru import logger

from site_stalker.notify import Notifier
from site_stalker.stalk import SiteStalker
from site_stalker.vaccine_spot import VaccineSpotter

root_dir = Path(__file__).resolve().parent.parent
config_dir = root_dir.joinpath('etc')
config_file = config_dir.joinpath('config.yaml')

if not config_file.exists():
    logger.error(f'no configuration file found in {config_dir}, exiting...')
    sys.exit()

config = yaml.safe_load(config_file.open())
general_config_dict = {k: v for (k, v) in config['general'].items()}

log_level = 'INFO'
log_file = root_dir.joinpath('site_stalker.log')

if 'log_level' in general_config_dict:
    log_level = general_config_dict['log_level'].upper()
if 'log_dir' in general_config_dict:
    log_file = Path(general_config_dict['log_dir']).joinpath('site_stalker.log')

logger.remove()
logger.add(log_file, level=log_level, rotation='100 MB', retention='1 week', backtrace=True)


check_interval = config['general']['check_interval']

s_notifier = Notifier(config)

logger.info('audit=site_stalker action=starting_up event=successfully_loaded_classes')

while True:
    if config['site_watch']['enable'] is True:
        s_stalker = SiteStalker(config)
        for _site in s_stalker.compare_websites():
            if _site['changed'] is True:
                s_notifier.notify_user_of_site_change(_site['site_alias'])
    if config['vaccine_watch']['enable'] is True:
        v_finder = VaccineSpotter(config)
        v_finder.find_vaccine_appointments()
        if v_finder.available_appointments:
            s_notifier.notify_user_of_vaccine(v_finder.available_appointments)
    logger.info(f'audit=site_stalker action=waiting event=still_waiting duration="{check_interval} seconds"')
    time.sleep(check_interval)
