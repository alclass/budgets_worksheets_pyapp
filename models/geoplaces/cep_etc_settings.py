#!/usr/bin/env python3
"""
models/geoplaces/cep_etc_settings.py

"""
import os
import sqlite3
import settings as sett
GEOPLACES_DATAFOLDER_ROOTDIRNAME = 'geoplaces'
CEPABERTO_BASEDIRNAME = 'cepaberto_data'
# CEP_DATAFOLDER_MIDDLEPATH = f"{GEOPLACES_DATAFOLDER_ROOTDIRNAME}/cep"
CEP_DATA_DIRNAME = "cep"
SQLITE_DB_FILEPATH = 'brazil_cep.sqlite'


def get_geoplaces_datafolderpath():
  datafolderpath = sett.get_datafolder_abspath()
  geoplaces_datafolderpath = os.path.join(datafolderpath, GEOPLACES_DATAFOLDER_ROOTDIRNAME)
  if not os.path.isdir(geoplaces_datafolderpath):
    os.makedirs(geoplaces_datafolderpath)
  return geoplaces_datafolderpath


def get_cep_datafolderpath():
  cep_datafolderpath = os.path.join(get_geoplaces_datafolderpath(), CEP_DATA_DIRNAME)
  if not os.path.isdir(cep_datafolderpath):
    os.makedirs(cep_datafolderpath)
  return cep_datafolderpath


def get_cepaberto_basefolderpath():
  cepaberto_basefolderpath = os.path.join(get_cep_datafolderpath(), CEPABERTO_BASEDIRNAME)
  if not os.path.isdir(cepaberto_basefolderpath):
    os.makedirs(cepaberto_basefolderpath)
  return cepaberto_basefolderpath


def get_cep_sqlite_filepath():
  return os.path.join(get_cep_datafolderpath(), SQLITE_DB_FILEPATH)


def get_cep_sqlite_connection():
  return sqlite3.connect(get_cep_sqlite_filepath())


def adhoc_test():
  """
  conn = get_cep_sqlite_connection()
  """
  print("geoplace's data folder", get_geoplaces_datafolderpath())
  print("cep data folder", get_cep_datafolderpath())
  print('cep sqlite filepath', get_cep_sqlite_filepath())
  print('cepaberto_basefolderpath', get_cepaberto_basefolderpath())


def process():
  pass


if __name__ == "__main__":
  process()
  adhoc_test()
