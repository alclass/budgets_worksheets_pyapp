#!/usr/bin/env python3
"""
gen_composite_currency_updter.py
Script to fetch both exchange rates and CPI indices.
The purpose is to generate an output with day to day
  composite money financial update indices.
"""
import datetime
import commands.gen_composite_currency_updter as composite
import fs.datefs.datefunctions as dtfs


def show_variation_between_dates(ini_date, fim_date=None):
  ini_cpi_baselineindex = composite.get_cpi_baselineindex_in_month(ini_date)
  print(ini_date, 'ini_cpi_baselineindex', ini_cpi_baselineindex)
  fim_cpi_baselineindex, lastdate = composite.get_last_available_cpi_baselineindex()
  print(lastdate, 'fim_cpi_baselineindex', fim_cpi_baselineindex)
  cpi_variation = (fim_cpi_baselineindex - ini_cpi_baselineindex) / ini_cpi_baselineindex
  print('cpi_variation', cpi_variation)
  return cpi_variation


def process():
  """
  pastdate = '2020-10-15'
  pydate = datetime.date(2020, 10, 15)

  """
  ini_strdate = '2020-6-1'
  ini_date = dtfs.convert_yyyymmdd_strdate_to_dtdate_or_none(ini_strdate)
  show_variation_between_dates(ini_date)


if __name__ == '__main__':
  process()
