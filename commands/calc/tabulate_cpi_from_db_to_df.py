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
import os.path
import time

import pandas
import fs.datefs.datefunctions as dtfs
import pandas as pd
import commands.fetch.cpi.read_cpis_from_db as dbr  # get_as_df_all_available_cpi_baselineindices_in_db
import settings as sett


class Tabulator:

  def __init__(self, startyear=None, endyear=None):
    self._month3letter_colindices = None
    self._year_rowindices = None
    self.namedtuplerows = None
    self.cpisdictlist_prep_for_df = None
    self.df = None
    self.startyear = startyear
    self.endyear = endyear
    self.treat_years()

  def treat_years(self):
    try:
      self.startyear = int(self.startyear)
    except (TypeError, ValueError):
      self.startyear = dbr.get_older_available_year_in_cpi_db()
    try:
      self.endyear = int(self.endyear)
    except (TypeError, ValueError):
      self.endyear = dbr.get_newer_available_year_in_cpi_db()

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
      ntlist = dbr.get_cpis_n_refmonths_as_ntlist_fromdb_by_year_n_series(year)
      self.namedtuplerows.append(ntlist)

  def mount_all_years_dictlist_to_prep_for_df(self):
    """
    Once all data structures above are ready, df (DataFrame) may be instantiated from
      a "on-the-fly" dict montage that will create an NxN matrix for df
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
      print('year', year, 'cpis', cpis)
      cpi_arr_size = len(cpis)
      cpisdict = {self.month3letter_colindices[i]: cpis[i] for i in range(0, cpi_arr_size)}
      print('cpisdict', cpisdict)
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
    print('save_df_to_excel')
    time.sleep(3)
    excel_filename = 'CPIs year by year.xlsx'
    folderpath = sett.get_datafolder_abspath()
    excel_filepath = os.path.join(folderpath, excel_filename)
    print('About to file', excel_filename)
    if os.path.exists(excel_filepath):
      print('Not saving, for there is an os-entry with same name. Please remove it and try again.')
    else:
      self.df.to_excel(excel_filepath)
      print('Saved file', excel_filename)

  def process_create_df(self):
    self.accumulate_all_years_ntlist_for_df()
    self.mount_all_years_dictlist_to_prep_for_df()
    self.create_df_from_prepared_dictlist()
    self.save_df_to_excel()


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


def process():
  pass


if __name__ == '__main__':
  """
  process()
  """
  adhoctest()
