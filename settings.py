#!/usr/bin/env python3
"""
settings.py

# As of 2023-11, the first var in local_settings.py is:
  DATA_FOLDERPATH = None  # the one in settings.py will be used
This setting may be used if the user wants to configure a different directory for data.

Notice that script 'local_settings.py' is not included in the git repo of this app,
  but for mounting (or recreating) it, it suffices look up the importing variables here.
"""
import os
import sqlite3
import local_settings as ls
CEPABERTO_API_TOKEN = ls.CEPABERTO_API_TOKEN
# the conditional assignment below is to avoid TypeError from abspath() in case
# ls.DATA_FOLDERPATH is None; however, if it does not exist there (in local_settings.py)
# AttributeError comes up anyway (so, because local_settings is not in repo, please add it during install)
NONDEFAULT_DATA_FOLDERPATH = os.path.abspath(ls.DATA_FOLDERPATH) if ls.DATA_FOLDERPATH else None
CURR_USD = 'USD'
CURR_BRL = 'BRL'
DATESDATA_FILENAME_DEFAULT = 'datesfile.dat'
DATA_FOLDERNAME = 'dados'  # may be overridden by its counterpart in local_settings.py
SQLITE_FILENAME_DEFAULT = 'exchange_n_indices.sqlite'


def get_sqlite_connection(sqlitefilename: str | None = None):
  """"
  For the sqlite data filepath:
    get_sqlite_appsdata_filepath()
  """
  if sqlitefilename is None:
    sqlitefilename = SQLITE_FILENAME_DEFAULT
  filepath = get_datafile_abspath_in_app(sqlitefilename)
  return sqlite3.connect(filepath)


def get_apps_root_abspath():
  if NONDEFAULT_DATA_FOLDERPATH is not None:
    return NONDEFAULT_DATA_FOLDERPATH
  thisfile_abspath = __file__
  apps_root_abspath, _ = os.path.split(thisfile_abspath)
  if apps_root_abspath == '.':
    apps_root_abspath = os.path.abspath(apps_root_abspath)
  return apps_root_abspath


def get_appsroot_abspath_for_filename(filename):
  return os.path.join(get_apps_root_abspath(), filename)


def get_apps_data_abspath():
  if NONDEFAULT_DATA_FOLDERPATH is not None:
    return NONDEFAULT_DATA_FOLDERPATH
  apps_root_abspath = get_apps_root_abspath()
  return os.path.join(apps_root_abspath, DATA_FOLDERNAME)


def get_datafolder_abspath():
  return get_apps_data_abspath()


def get_exchange_rate_sqlite_filepath():
  """
  DEPRECATED (@see the one below)
  """
  return os.path.join(get_apps_data_abspath(), SQLITE_FILENAME_DEFAULT)


def get_sqlite_appsdata_filepath():
  return os.path.join(get_apps_data_abspath(), SQLITE_FILENAME_DEFAULT)


def get_datafile_abspath_in_app(data_filename=None):
  if data_filename is None:
    return SQLITE_FILENAME_DEFAULT
  return os.path.join(get_apps_data_abspath(), data_filename)


def get_dates_datafile_abspath_in_app(data_filename=None):
  if data_filename is None:
    data_filename = DATESDATA_FILENAME_DEFAULT
  return os.path.join(get_apps_data_abspath(), data_filename)


def adhoctest():
  apps_root_abspath = get_apps_root_abspath()
  print('apps_root_abspath [', apps_root_abspath, ']')
  data_abspath = get_dates_datafile_abspath_in_app()
  print('data_abspath [', data_abspath, ']')
  print('exchange_rate_sqlite_filepath [', get_exchange_rate_sqlite_filepath(), ']')
  print('dates_datafile_abspath_in_app [', get_dates_datafile_abspath_in_app(), ']')
  print('CEPABERTO_API_TOKEN [', CEPABERTO_API_TOKEN, ']')


def process():
  pass


if __name__ == '__main__':
  """
  process()
  """
  adhoctest()
