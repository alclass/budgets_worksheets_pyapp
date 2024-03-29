#!/usr/bin/env python3
"""
"""
import datetime
import os
import pandas as pd
import sqlite3
import settings as sett
PPUBASE_TABLENAME = 'ppubase_orc'
PRICEBANK_TABLENAME = 'pricebank_orc'
ORCDADOS_FOLDERNAME = 'orçs_dados'
ORCDADOS_SQLFILENAME = 'orçs_db.sqlite'
PPUBASE_FILENAME = 'PPU base.xlsx'
PPUBASE_COLUMNNAMES = [
  'seq', 'ncmcode', 'ipi', 'familycode', 'nmcode', 'partnumber',
  'manufacturer_sname', 'textobreve', 'description', 'qty', 'meas_unit'
]  # 11 fieldnames


def get_orcdados_folderpath():
  datafolderpath = sett.get_datafolder_abspath()
  orcsdados_folderpath = os.path.join(datafolderpath, ORCDADOS_FOLDERNAME)
  return orcsdados_folderpath


def get_orcdados_batch_output_folderpath():
  batch_output_foldername = 'batch_output'
  base_folderpath = get_orcdados_folderpath()
  batch_output_folderpath = os.path.join(base_folderpath, batch_output_foldername)
  if not os.path.isdir(batch_output_folderpath):
    os.makedirs(batch_output_folderpath)
  return batch_output_folderpath


def get_xlsxfilepaths_from_batch_output_folder(dotext='.xlsx'):
  dotext = '.xlsx' if dotext is None else dotext
  dotext = '.' + dotext if not dotext.startswith('.') else dotext
  orcsdados_folderpath = get_orcdados_batch_output_folderpath()
  filenames = os.listdir(orcsdados_folderpath)
  filenames = filter(lambda e: e.endswith(dotext), filenames)
  filepaths = map(lambda e: os.path.join(orcsdados_folderpath, e), filenames)
  filepaths = sorted(filter(lambda e: os.path.isfile(e), filepaths))
  return filepaths


def get_orcdados_batch_output_filepath_w_filename(filename):
  batch_output_folderpath = get_orcdados_batch_output_folderpath()
  batch_output_filepath = os.path.join(batch_output_folderpath, filename)
  return batch_output_filepath


def get_orcdados_sqlitefilepath():
  orcsdados_folderpath = get_orcdados_folderpath()
  orcsdados_sqlitefilepath = os.path.join(orcsdados_folderpath, ORCDADOS_SQLFILENAME)
  return orcsdados_sqlitefilepath


def get_connection(p_filepath=None):
  filepath = p_filepath or get_orcdados_sqlitefilepath()
  return sqlite3.connect(filepath)


def get_xlsx_ppubase_filepath():
  folderpath = get_orcdados_folderpath()
  xlsx_filepath = os.path.join(folderpath, PPUBASE_FILENAME)
  return xlsx_filepath


def get_xlsx_ppubase_output_filepath(filename=None):
  if filename is None:
    filename = 'PPU ' + str(datetime.datetime.now()) + '.xlsx'
  folderpath = get_orcdados_folderpath()
  xlsx_filepath = os.path.join(folderpath, filename)
  return xlsx_filepath


def save_xlsx_ppubase_from_dataframe(df, filename=None):
  filepath = get_xlsx_ppubase_output_filepath(filename)
  print('Saving xlsx ppubase from pandas DataFrame:', filepath)
  df.to_excel(filepath)
  print('Saved')


def get_df_from_xlsx_ppubase():
  ppubase_filepath = get_xlsx_ppubase_filepath()
  df = pd.read_excel(ppubase_filepath)
  return df


def adhoctest():
  pass


def process():
  pass


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
