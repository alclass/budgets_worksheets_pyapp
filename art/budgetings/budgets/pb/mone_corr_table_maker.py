#!/usr/bin/env python3
"""
models/budgets/pb/mone_corr_table_maker.py

import copy
import fs.datefs.introspect_dates as idt  # idt.for make_date_or_none()
"""
import datetime
import art.budgetings.budgets.pb.price_data_as_dict as pdd  # pdd.gather_data
import commands.bcb_br.report.corr_monet_n_indices_calculator_from_dates as cmc  # cmc.CorrMonetWithinDatesCalculator


def dates_from_prices():
  dates = []
  prices = pdd.gather_data()
  for nm in prices.nn_n_priceitemlist_dict:
    priceitems = prices.nn_n_priceitemlist_dict[nm]
    for pi in priceitems:
      dates.append(pi.date)
  dates = sorted(set(dates))
  # print(len(dates))
  return dates


class MoneCorrTableMaker:

  def __init__(self, topdate=None):
    self.topdate = topdate
    self.dates = dates_from_prices()
    self.process()

  def process(self):
    cmo = cmc.CorrMonetWithinDatesCalculator(self.topdate)
    for pdate in self.dates:
      cmo.add_cpi_n_exr_on_date(pdate)
    cmo.process()


def adhoctest():
  dates = dates_from_prices()
  # dates = sorted(set(dates))
  print('size', len(dates))
  for pdate in dates:
    print(pdate)
  topdate = datetime.date(year=2024, month=2, day=1)
  mk_o = MoneCorrTableMaker(topdate)


def process():
  pass


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
