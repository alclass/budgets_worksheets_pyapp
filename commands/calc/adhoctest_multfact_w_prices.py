#!/usr/bin/env python3
"""
commands/calc/adhoctest_multfact_w_prices.py

"""
import collections
import datetime
from dateutil.relativedelta import relativedelta
import commands.calc.datamass_for_multfactortable as prices_dmass  #.get_date_n_price_tuplelist
import fs.datefs.datefunctions as dtfs
import commands.calc.calc_monet_corr as cmc  # .DatePriceRecordsMonetCorrCalculator
# intr.introspect_n_convert_sdlist_to_dates_w_or_wo_sep_n_posorder(strdatelist)
import fs.datefs.introspect_dates as intr
import fs.datefs.read_write_datelist_files as rwdt
nt_dateprice_constr = collections.namedtuple('NTDeP', field_names=['date', 'price'])


def perform_step1(pdate):
  dates = rwdt.fetch_dates_from_strdates_in_text_wo_sep_but_of_oneform_from_filepath()
  # dates = intr.introspect_n_convert_sdlist_to_dates_w_or_wo_sep_n_posorder(strdatelist)
  print('step 1 dates', dates)
  recs = cmc.DatePriceRecordsMonetCorrCalculator(refdate=pdate)
  recs.datelist = dates
  print(recs)
  ntlist = prices_dmass.get_date_n_price_ntlist()
  print(ntlist)
  recs.integrate_prices_into_dates_dataframe(ntlist)


def perform_step2():
  pass


def adhoctest():
  """
  """
  today = datetime.date.today()
  yesterday = today - relativedelta(days=1)
  perform_step1(yesterday)


def process():
  pass


if __name__ == '__main__':
  """
  """
  process()
  adhoctest()
