#!/usr/bin/env python3
"""
commands/calc/adhoctest_multfact_w_prices.py

"""
import collections
import datetime
from dateutil.relativedelta import relativedelta
import commands.calc.cpi.adhoctests.datamass_for_multfactortable as prices_dmass  # .get_date_n_price_tuplelist
import commands.calc.calc_monet_corr as cmc  # .DatePriceRecordsMonetCorrCalculator
import fs.datefs.read_write_datelist_files_fs as rwdt
nt_dateprice_constr = collections.namedtuple('NTDeP', field_names=['date', 'price'])


def perform_step1(pdate):
  dates = rwdt.fetch_dates_from_strdates_in_text_wo_sep_but_of_oneform_from_filepath()
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
