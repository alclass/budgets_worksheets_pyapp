#!/usr/bin/env python3
"""
config.py
"""
import config as cfg

apps_root_abspath = cfg.get_apps_root_abspath()
print('1 apps_root_abspath', apps_root_abspath)
apps_data_abspath = cfg.get_apps_data_abspath()
print('2 apps_data_abspath', apps_data_abspath)

