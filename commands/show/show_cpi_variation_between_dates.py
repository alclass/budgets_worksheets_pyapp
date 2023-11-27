#!/usr/bin/env python3
"""
show_table_with_variations_from_filedates_vs_mostrecent.py

This script reads a dateadhoctests data (text) file inside the app's data folder,
  fetches CPI index mapping to month-date and outputs a 2-column data text.

The output text contains:
This scripts fetches both exchange rates and CPI indices.
The purpose is to generate an output with day to day
  composite money financial update indices.
"""
import datetime
from dateutil.relativedelta import relativedelta
import commands.show.show_table_with_variations_from_filedates_vs_mostrecent as composite
import fs.datefs.datefunctions as dtfs
import sys


def show_variation_between_dates(ini_date, fim_date):
  """"
  previous version
    fim_cpi_baselineindex, lastdate = composite.get_last_available_cpi_baselineindex_in_db()
    lastdate = fim_date
  """
  ini_cpi_baselineindex = composite.get_cpi_baselineindex_for_refmonth(ini_date)
  print(ini_date, 'ini_cpi_baselineindex', ini_cpi_baselineindex)
  if fim_date is None:
    return None
  fim_cpi_baselineindex = composite.get_cpi_baselineindex_for_refmonth(fim_date)
  print(fim_date, 'fim_cpi_baselineindex', fim_cpi_baselineindex)
  cpi_variation = None
  try:
    cpi_variation = (fim_cpi_baselineindex - ini_cpi_baselineindex) / ini_cpi_baselineindex
    print('cpi_variation', cpi_variation)
  except TypeError:
    print('typeerror cpi_variation', cpi_variation)
  return cpi_variation


def get_dates_from_cli():
  dates = []
  if len(sys.argv) < 2:
    return []
  for arg in sys.argv[1:]:
    dates.append(arg)
  return dates


def fetch_dates_in_cli_if_any():
  idates = get_dates_from_cli()
  odates = []
  for strdate in idates:
    pdate = dtfs.returns_date_or_none(strdate)
    if pdate is not None:
      odates.append(pdate)
  return odates


def mount_variation_table():
  """
  pastdate = '2020-10-15'
  pydate = datetime.date(2020, 10, 15)
  """
  pydates = fetch_dates_in_cli_if_any()
  if len(pydates) == 0:
    pydates = composite.get_pydates_from_datafile()
  today = datetime.date.today()
  most_recent_date = today - relativedelta(days=-2)
  for pydate in pydates:
    show_variation_between_dates(pydate, most_recent_date)


def process():
  mount_variation_table()


if __name__ == '__main__':
  process()
