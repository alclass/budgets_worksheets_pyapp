#!/usr/bin/env python3
"""
commands/calc/calc_monet_corr.py
  contains class DatePriceRecordsMonetCorrCalculator

The underlying system or app, up til now, has used
  one particular form of monetary correction. Let us
  call this "particular form" the "protocol for monet corr".

This protocol consists of multiplying two variations, ie:
  1 the variation of one monetary correction index
    (here the one used is CPI_US series "cur")
  2 the variation in currency exchange rate
    (here the one used is BRL/USD)

  Other forms may be devised for this system in the future.

Let's see an example:
  suppose one wants to find the monet corr between
  dates 2022-10-25 (initial) & 2023-05-15 (final).

The M-2 (month minus 2) or M-1 Strategy
---------------------------------------

The CPI indices publication is a monthly, and it takes
  more than one-month (the IDE spelling corrector forced the hyphen...)
  period for a certain month's index
  to be published in relation to itself.
Because of this, a M-2 or M-1 strategy is used. For example:

Consider a price monetary correction in-between the following
  two dates: 2022-10-25 (initial) & 2023-05-15 (final).

 => for the inital date 2022-10-25, program fetches
    the CPI for month 2022-08; this is called "M-2" (month minus 2),
    ie, because the CPI is published later than the month itself,
  the convention M-2 retards both dates in 2 months.

 => similarly, for date 2023-05-15, program fetches
    the CPI month 2023-03, idem, that's under the M-2 convention.

Inflation versus Deflation
--------------------------

The CPI, with rare exceptions of deflation, is a growing series,
  ie inflation tends to be the norm, for more or for less.

This fact is import if one considers not using a negative
  factor that will diminish, excepting if deflation becames
  more common and with "more impact" in prices.

@see commands/calc/multiplication_factor_calc.py
  for the calculation formula.
"""
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import fs.datefs.datefunctions as dtfs
import fs.datefs.introspect_dates as intr
import fs.datefs.read_write_datelist_files as rwdl
import fs.datefs.argparse as ap  # ap.get_args
import commands.calc.multiplication_factor_calc as mfcalc


class DatePriceRecordsMonetCorrCalculator:
  """
  => First Step
  The computation strategy here, in its first step,
    is to calculate a multiplication factor table
    with all dates that will be necessary later on to the second step.

  Thus, the first step is dependent on dates, their corresponding indices,
    and not on prices. This first step keeps its results in a pandas DataFrame.

  => Second Step
  Once the DataFrame mentioned above is available, a prices-on-dates second table,
    may be monetarily corrected looking up the multiplication factors
    on the first DataFrame on their dates.
  """
  def __init__(self, refdate=None, datelist=[]):
    self.refdate = dtfs.make_date_or_today(refdate)
    self.dictlist = []
    self.datelist = datelist
    self.df = None
    # self.df_dates_n_prices = None
    self.df = pd.DataFrame(columns=mfcalc.DATAFRAME_COLUMNS)

  def set_dates_n_prices_ntlist(self, dates_n_prices_ntlist):
    """
    NT is NTDatesNPrices, fields=['date', 'price']
    """
    _ = self.dictlist
    if dates_n_prices_ntlist is None or not iter(dates_n_prices_ntlist):
      return
    if len(dates_n_prices_ntlist) == 0:
      return
    for nt in dates_n_prices_ntlist:
      try:
        _ = nt.date
        _ = nt.price
      except (AttributeError, TypeError):
        return

  def integrate_date_price_into_df(self):
    self.df[['date', 'price']] = self.df_dates_n_prices

  def calc_monetcorr_bw_date_n_ref(self, otherdate):
    """

    """
    date1 = otherdate
    date2 = self.refdate
    mcc = MonetCorrCalculator(dateini=date1, datefim=date2)
    nrows = self.df.shape[0]
    print(date1, date2, 'nrows', nrows, 'multiplication_factor', mcc.multiplication_factor)
    pdict = mcc.gen_rowdict()
    self.dictlist.append(pdict)

  def calc_monetcorr_w_datelist_n_refdate(self, strdatelist):
    """

    """
    # datelist = gendt.convert_strdatelist_to_datelist(strdatelist)
    datelist = intr.introspect_n_convert_sdlist_to_dates_w_or_wo_sep_n_posorder(strdatelist)
    for pdate in datelist:
      self.calc_monetcorr_bw_date_n_ref(pdate)
    self.df = pd.DataFrame(self.dictlist)
    print(self.df.to_string())

  def integrate_dates_df(self):
    for i, pdate in enumerate(self.datelist):
      calcor = mfcalc.MonetCorrCalculator(pdate, self.refdate, rowindexfordf=i)
      self.df.loc[i] = calcor.df.loc[i]

  def update_prices(self):
    self.calc_monetcorr_w_datelist_n_refdate()
    self.integrate_date_price_into_df()
    print(self.df.to_string())


def adhoctest2():
  dates = rwdl.fetch_dates_from_strdates_in_text_wo_sep_but_of_oneform_from_filepath()
  print('len =', len(dates), dates)
  today = datetime.date.today()
  yesterday = today - relativedelta(days=1)
  lcalcor = DatePriceRecordsMonetCorrCalculator(yesterday, dates)
  lcalcor.integrate_dates_df()
  print(lcalcor.df.to_string())


def adhoctest():
  """
  -dl "2023-05-20" "2023-06-21"
  calc_monet_corr_between_datelist_n_mostrecent(args.datelist)
  yearini = 2020
  yearfim = 2022
  # read_yearrange_from_db(yearini, yearfim)
  calc_monet_corr_between_datelist_n_mostrecent(args.datelist)
  """
  args = ap.get_args()
  print(args)
  try:
    dateini = dtfs.make_date_or_none(args.ini[0])
    datefim = dtfs.make_date_or_none(args.fim[0])
    print('i', dateini, 'f', datefim)
    mcc = mfcalc.MonetCorrCalculator(dateini, datefim)
    mcc.calc_monet_corr_multiplier_between_dates()
    print(mcc.multiplication_factor)
    series = mcc.gen_rowdict()
    print(series)
  # twodates = args.calc_monet_corr
  except (AttributeError, IndexError, TypeError):
    print('No argument processed.')


def process():
  """
  dateini = args.ini
  datefim = args.fim
  calc = MonetCorrCalculator(dateini, datefim)
  print(calc)
  args = get_args_via_argparse()
  calc_monet_corr_between_datelist_n_mostrecent(args.datelist)
  """
  args = ap.get_args()
  print(args)
  double = DatePriceRecordsMonetCorrCalculator()
  dispatcher = ap.Dispatcher(args)
  dispatcher.func = double.calc_monetcorr_w_datelist_n_refdate
  dispatcher.dispatch()


if __name__ == '__main__':
  """
  adhoctest()
  process()
  """
  adhoctest2()
