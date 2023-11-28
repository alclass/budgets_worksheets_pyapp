#!/usr/bin/env python3
"""
commands/calc/tabulate_cpi_from_db_to_df.py
  reads all db rows with cpi & refmonthdate into a pandas df (Data Frame) and reorganizes them
    into a year line month column table.

The tabulation chosen is the following
 ys/ ms | jan | feb | mar  (...)
--------|-----|-----|----
year y1 |     |     |
--------|-----|-----|----
year y2 |     |     |
--------|-----|-----|----
  (...)
"""
import argparse
import datetime
from dateutil.relativedelta import relativedelta
import os.path
import fs.datefs.datefunctions as dtfs
import pandas as pd
import commands.fetch.cpi.read_cpis_from_db as dbr  # get_as_df_all_available_cpi_baselineindices_in_db
import settings as sett
import commands.fetch.cpi.read_cpis_from_db as rcpi


class Tabulator:

  def __init__(self, startyear=None, endyear=None, seriesid=None):
    self.startyear = startyear
    self.endyear = endyear
    self.startrefmonth = None
    self.endrefmonth = None
    self.seriesid = seriesid or rcpi.DEFAULT_SERIESID
    self._month3letter_colindices = None
    self._year_rowindices = None
    self.namedtuplerows = None
    self.cpisdictlist_prep_for_df = None
    self.df = None
    self.been_processed = False
    self.scripts_start_time = None  # set on method "process" (ie process_create_df())
    self.savefile_report_msg = None
    self.runduration = None
    self.treat_years()

  def treat_years(self):
    try:
      self.startyear = int(self.startyear)
    except (TypeError, ValueError):
      self.startyear = dbr.get_older_available_year_in_cpi_db(self.seriesid)
    try:
      self.endyear = int(self.endyear)
    except (TypeError, ValueError):
      self.endyear = dbr.get_newer_available_year_in_cpi_db(self.seriesid)
    self.startrefmonth = dbr.get_older_available_refmonthdate_in_cpi_db(self.seriesid)
    self.endrefmonth = dbr.get_newer_available_refmonthdate_in_cpi_db(self.seriesid)
    if self.startrefmonth.year != self.startyear:
      error_msg = f'startrefmonth.year {self.startrefmonth.year} != startyear {self.startyear}'
      raise ValueError(error_msg)
    if self.endrefmonth.year != self.endyear:
      error_msg = f'endrefmonth.year {self.endrefmonth.year} != endyear {self.endyear}'
      raise ValueError(error_msg)

  @property
  def n_years(self):
    try:
      return self.endyear - self.startyear + 1
    except (AttributeError, ValueError):
      pass
    return None

  @property
  def n_months(self):
    try:
      reladelt = relativedelta(self.endrefmonth, self.startrefmonth)
      n_months_inbetween_dates = reladelt.years * 12 + reladelt.months + 1
      return n_months_inbetween_dates
    except (AttributeError, ValueError):
      pass
    return None

  @property
  def output_excel_folderpath(self):
    folderpath = sett.get_datafolder_abspath()
    if not os.path.exists(folderpath):
      os.mkdir(folderpath)
    return folderpath

  @property
  def output_excel_filename(self):
    inirefmonth_str = f'{self.startrefmonth.year}-{self.startrefmonth.month:02}'
    fimrefmonth_str = f'{self.endrefmonth.year}-{self.endrefmonth.month:02}'
    return f"CPIs {inirefmonth_str} {fimrefmonth_str} {self.seriesid}.xlsx"

  @property
  def output_excel_filepath(self):
    return os.path.join(self.output_excel_folderpath, self.output_excel_filename)

  @property
  def month3letter_colindices(self):
    """
    Represents the column indices ['jan', 'feb', 'mar', etc.]
      It will be created (lazily) upon first access.
    """
    if self._month3letter_colindices is None:
      self._month3letter_colindices = dtfs.make_allmonths_englishlower3letter_list()
    return self._month3letter_colindices

  @property
  def year_rowindices(self):
    """
    Represents the row indices:example [2011, 2012, 2013, etc.]
      In fact, its integer range is range(startyear, endyear+1)
      It will be created (lazily) upon first access.
    """
    if self._year_rowindices is None:
      self._year_rowindices = [year for year in range(self.startyear, self.endyear+1)]
    return self._year_rowindices

  def accumulate_all_years_ntlist_for_df(self):
    """
    Accumulates all monthly cpis year by year, within startyear and endyear
    """
    self.namedtuplerows = []
    for year in range(self.startyear, self.endyear+1):
      ntlist = dbr.get_cpis_n_refmonths_as_ntlist_fromdb_by_year_n_series(year, self.seriesid)
      self.namedtuplerows.append(ntlist)

  def mount_all_years_dictlist_to_prep_for_df(self):
    """
    Once all data structures above are ready, df (DataFrame) may be instantiated from
      an "on-the-fly" dict montage that will create an NxN matrix for df
    The result will be similar to:
      The tabulation chosen is the following
       ys/ ms | jan | feb | mar  (...)
      --------|-----|-----|----
      year y1 |     |     |
      --------|-----|-----|----
      year y2 |     |     |
      --------|-----|-----|----
        (...)
    """
    self.cpisdictlist_prep_for_df = []
    for i, year in enumerate(range(self.startyear, self.endyear + 1)):
      cpis = [nt.cpi for nt in self.namedtuplerows[i]]  # list came ordered ASC from db
      # print('year', year, 'cpis', cpis)
      cpi_arr_size = len(cpis)
      cpisdict = {self.month3letter_colindices[i]: cpis[i] for i in range(0, cpi_arr_size)}
      # print('cpisdict', cpisdict)
      self.cpisdictlist_prep_for_df.append(cpisdict)

  def create_df_from_prepared_dictlist(self):
    """
    Instantiates the instance's DataFrame object.
      It needs the preparation from the method mount_all_years_dictlist_to_prep_for_df() above
    """
    self.df = pd.DataFrame(
      self.cpisdictlist_prep_for_df,
      columns=self.month3letter_colindices,
      index=self.year_rowindices,
    )
    # print(self.df.to_string())

  def save_df_to_excel(self):
    if os.path.exists(self.output_excel_filepath):
      self.savefile_report_msg = 'file not saved due to it already existing in folder'
      scrmsg = f"""Not saving [{self.output_excel_filename}],
      Folder: [{self.output_excel_folderpath}]
      for there is an os-entry with same name. In case it's necessary to recreate the output Excel file,
      please delete/remove the above mentioned file in the folder and rerun this program."""
      print(scrmsg)
    else:
      self.savefile_report_msg = f'file saved {datetime.datetime.now()}'
      self.df.to_excel(self.output_excel_filepath)
      scrmsg = f"""Saved [{self.output_excel_filename}],
      Folder: [{self.output_excel_folderpath}]"""
      print(scrmsg)

  def process_create_df(self):
    self.scripts_start_time = datetime.datetime.now()
    self.accumulate_all_years_ntlist_for_df()
    self.mount_all_years_dictlist_to_prep_for_df()
    self.create_df_from_prepared_dictlist()
    self.save_df_to_excel()
    self.been_processed = True
    scripts_end_time = datetime.datetime.now()
    self.runduration = scripts_end_time - self.scripts_start_time
    self.report()

  def report(self):
    print(self)

  def __str__(self):
    outstr = f"""Tabulator:
    From {self.startrefmonth} to {self.endrefmonth} | seriesid {self.seriesid}
    Number of years {self.n_years} | number of months (data points) {self.n_months}
    been processed = {self.been_processed} | duration = {self.runduration}
    Output Excel Filename: [{self.output_excel_filename}] | {self.savefile_report_msg}
    Folder in which output Excel file is located: [{self.output_excel_folderpath}] 
    """
    return outstr


def adhoctest():
  """
  df = get_df_of_all_db_cpis_n_refmonths()
  print(df.to_string())
  tab = DfYearMonthTabulator(df)
  tab.slice_year(2001)
  """
  tab = Tabulator()
  tab.process_create_df()
  print(tab.df.to_string())


def get_seriesid_from_cli():
  """
  The argument expected is either of the two below:
    cur_seriesid = 'CUUR0000SA0'
    sur_seriesid = 'SUUR0000SA0'
  iF none is given, the first one above is DEFAULT.
  """
  parser = argparse.ArgumentParser()
  helpstr = f"the CPI seriesid, it's either {rcpi.available_cpi_seriesid_list}"
  parser.add_argument(
    '-s', '--seriesid', metavar='seriesid', type=str, nargs=1,
    help=helpstr,
  )
  args = parser.parse_args()
  seriesid = args.seriesid
  if isinstance(seriesid, list) and len(seriesid) > 0:
    seriesid = seriesid[0] if seriesid[0] else rcpi.available_cpi_seriesid_list or None
    return seriesid
  return None


def process():
  seriesid = get_seriesid_from_cli() or rcpi.DEFAULT_SERIESID
  tab = Tabulator(None, None, seriesid)
  tab.process_create_df()


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()
