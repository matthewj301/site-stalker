#!/usr/bin/env python
import sys
import time
from pathlib import Path

import yaml
from loguru import logger

from site_stalker.notify import Notifier
from site_stalker.stalk import SiteStalker
from site_stalker.vaccine_spot import VaccineSpotter

root_dir = Path('/').resolve()
config_dir = root_dir.joinpath('etc')
config_file = config_dir.joinpath('config.yaml')

if not config_file.exists():
    logger.error(f'no configuration file found in {config_dir}, exiting...')
    sys.exit()

config = yaml.safe_load(config_file.open())
general_config_dict = {k: v for (k, v) in config['general'].items()}

if 'log_level' in general_config_dict:
    log_level = general_config_dict['log_level'].upper()
else:
    log_level = 'INFO'

logger.remove()
logger.add(sys.stderr, level=log_level)

check_interval = config['general']['check_interval']

s_notifier = Notifier(config)
s_stalker = SiteStalker(config)
v_finder = VaccineSpotter(config)

logger.info('audit=site_stalker action=starting_up event=successfully_loaded_classes')
s_notifier.send_text_msg('Site Comparison/Vaccine Finder Service has started, linked to this number')
logger.info(f'audit=site_stalker action=notify_user_of_service_start event=text_msg_sent')

while True:
    if config['site_watch']['enable'] is True:
        logger.info(f'audit=site_stalker event=site_stalking started action=beginning_processing '
                    f'monitoring_list="{s_stalker.monitor_dict}" ')
        for _site in s_stalker.compare_websites():
            if _site['changed'] is True:
                s_notifier.notify_user_of_site_change(_site['site_alias'])
    if config['vaccine_watch']['enable'] is True:
        logger.info(f'audit=site_stalker event=vaccine_search_started action=beginning_search '
                    f'state={v_finder.state} '
                    f'zip_code={v_finder.zip_code} '
                    f'mile_radius={v_finder.acceptable_distance_from_user}')
        v_finder.find_vaccine_appointments()
        if v_finder.available_appointments:
            s_notifier.notify_user_of_vaccine(v_finder.available_appointments)
    logger.info(f'audit=site_stalker action=waiting event=still_waiting duration="{check_interval} seconds"')
    time.sleep(check_interval)
