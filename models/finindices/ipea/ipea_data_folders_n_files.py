#!/usr/bin/env python3
"""
models/finindices/ipea/ipea_data_folders_n_files.py

"""
import collections
import datetime
import os
import pandas as pd
import settings as sett
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import fs.os.os_complement as osc  # fetch_only_filepaths_from_folderpath
today = datetime.date.today()
IPEA_MIDDLE_FOLDERNAME = 'findata/ipea'
IPCA_DATAFRAME_FILENAME = str(today) + '_ipca_dataframe_001.xlsx'
SQL_TABLENAME = 'cpi_indices'
indidx_namedtuple = collections.namedtuple('NTIndIdx', field_names=['date', 'accindex'])
IPCA12_SERIESID_STR = 'PRECOS12_IPCA12'

def get_connection():
  return sett.get_connection()

def get_ipea_folderpath():
  datafolderpath = sett.get_datafolder_abspath()
  ipea_datafolderpath = os.path.join(datafolderpath, IPEA_MIDDLE_FOLDERNAME)
  if not os.path.isdir(ipea_datafolderpath):
    os.makedirs(ipea_datafolderpath)
  return ipea_datafolderpath


def find_if_any_most_recent_ipca12_filepath_n_its_date():
  folderpath = get_ipea_folderpath()
  filenames = osc.fetch_only_filenames_from_folderpath(folderpath)
  most_recent_ipca12_filename, pdate = cnv.find_most_recent_name_n_its_prefix_date_in_strlist(filenames)
  most_recent_ipca12_filepath = os.path.join(folderpath, most_recent_ipca12_filename)
  return most_recent_ipca12_filepath, pdate


class IndicadorFileToDBTransposer:

  def __init__(self):
    self.df = None
    self.tablename = SQL_TABLENAME
    self.indicator_filepath, self.date = find_if_any_most_recent_ipca12_filepath_n_its_date()
    self.ntrows = []

  def read_file_into_pandas_df(self):
    """
    print(self.df.columns)
    print(self.df.describe())
    """
    self.df = pd.read_excel(self.indicator_filepath)
    # print(self.df.to_string())

  def roll_rows(self):
    """
    The row objects from a DataFrame are 'Series'
    The Series object in turn is a 2-tuple with a sequencial and a dict
    In the case here, the dict contains the fields needed to be extracted:
      nseq, pdict = row_as_a_series_obj
      seriesid = pdict['SERCODIGO']
      pdate = pdict['VALDATA']
      indicator_index = pdict['VALVALOR']
      scrmsg = f"{nseq} {seriesid} {pdate} {indicator_index}"
      print(scrmsg)

    """
    for row_as_a_series_obj in self.df.iterrows():
      nseq, pdict = row_as_a_series_obj
      seriesid = pdict['SERCODIGO']
      if seriesid != IPCA12_SERIESID_STR:
        continue
      vdate = pdict['VALDATA']
      pdate = cnv.make_date_or_none(vdate)
      if pdate is None:
        continue
      accindex = pdict['VALVALOR']
      ntrow = indidx_namedtuple(date=pdate, accindex=accindex)
      self.ntrows.append(ntrow)

  def insert_rows_into_db(self):
    print('insert_rows_into_db size =', len(self.ntrows))
    conn = sett.get_connection()
    cursor = conn.cursor()
    has_inserted = False
    for i, ro in enumerate(self.ntrows):
      # scrmsg = f"seq={i+1} sid={ro.seriesid} dat={ro.date} idx={ro.accindex}"
      scrmsg = f"Trying to db-insert seq={i+1} | date={ro.date} | idx={ro.accindex}"
      print(scrmsg)
      sql = f"""INSERT OR IGNORE INTO {self.tablename}
      (seriesid, baselineindex, refmonthdate) VALUES (?, ?, ?);"""
      tuplevalues = (IPCA12_SERIESID_STR, ro.accindex, ro.date)
      retval = cursor.execute(sql, tuplevalues)
      if retval.rowcount > 0:
        has_inserted = True
        print('has been inserted')
      else:
        print('has NOT been inserted')
    if has_inserted:
      conn.commit()
    conn.close()

  def transpose(self):
    self.read_file_into_pandas_df()
    self.roll_rows()
    self.insert_rows_into_db()

  def __str__(self):
    outstr = f"""Transposer date={self.date}
    n of rows = {self.df.shape[0]}
    """
    return outstr


def adhoctest():
  """
  scrmsg = f"output_filepath = '{output_filepath}'"
  print(scrmsg)
  """
  ifdb = IndicadorFileToDBTransposer()
  ifdb.transpose()
  print(ifdb)



def process():
  pass


if __name__ == '__main__':
  """
  """
  process()
  adhoctest()
