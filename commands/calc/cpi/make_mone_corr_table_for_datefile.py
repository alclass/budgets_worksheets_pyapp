#!/usr/bin/env python3
"""
commands/calc/cpi/make_mone_corr_table_for_datefile.py

import copy
import datetime
import fs.datefs.introspect_dates as intd
import fs.datefs.introspect_dates as idt  # idt.for make_date_or_none()
import models.budgets.pb.price_data_as_dict as pdd  # pdd.gather_data
"""
import os
import settings as sett
import commands.show.corr_monet_n_indices_calculator_from_dates as cmc  # cmc.CorrMonetWithinDatesCalculator
import fs.datefs.read_write_datelist_files as rwdf
import fs.datefs.introspect_dates as idt  # idt.for make_date_or_none()


def get_datedata_filepath():
  filename = 'datesfile.txt'
  datafolder_abspath = sett.get_datafolder_abspath()
  filepath = os.path.join(datafolder_abspath, filename)
  return filepath


def read_dates_from_datefiles():
  """
  """
  filepath = get_datedata_filepath()
  dates = rwdf.fetch_dates_from_strdates_in_text_wo_sep_but_of_oneform_from_filepath(filepath)
  return dates


class MoneCorrTableMaker:

  def __init__(self, topdate=None, fallback_to_cpi_m2date=False):
    self.fallback_to_cpi_m2date = fallback_to_cpi_m2date
    # self.topdate = topdate
    self.topdate = idt.make_date_or_none(topdate)
    self.dates = read_dates_from_datefiles()
    self.process()

  def process(self):
    cmo = cmc.CorrMonetWithinDatesCalculator(self.topdate, self.fallback_to_cpi_m2date)
    cmo.set_workdates(self.dates)
    # for pdate in self.dates:
    #   cmo.add_cpi_n_exr_on_date(pdate)
    cmo.process()
    print(cmo)


def adhoctest():
  dates = read_dates_from_datefiles()
  # dates = sorted(set(dates))
  print('size', len(dates))
  for pdate in dates:
    print(pdate)
  # topdate = datetime.date(year=2024, month=2, day=1)
  # topdate = datetime.date(year=2024, month=2, day=29)
  mk_o = MoneCorrTableMaker(topdate=None, fallback_to_cpi_m2date=True)


def process():
  pass


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
