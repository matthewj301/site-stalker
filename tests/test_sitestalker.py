#!/usr/bin/env python

from site_stalker.notify import Notifier
from pathlib import Path
import yaml

config_dir = Path('/mnt/gfs/container_configs/site_stalker').resolve()
config_file = config_dir.joinpath('config.yaml').resolve()
config = yaml.safe_load(config_file.open())




