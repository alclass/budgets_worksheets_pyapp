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
Because of this, an M-2 or M-1 strategy is used. For example:

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
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import fs.datefs.introspect_dates as intr
import fs.datefs.read_write_datelist_files_fs as rwdl
import fs.datefs.argparse as ap  # ap.get_args
import commands.calc.multiplication_factor_calc as mfcalc
import commands.calc.cpi.adhoctests.datamass_for_multfactortable as prices_dmass  # .get_date_n_price_tuplelist


def create_df_w_prices():
  # row 1
  dictlist = []
  price_dict = {'dt_i': '2013-01-01', 'price': '24.55'}
  dictlist.append(price_dict)
  price_dict = {'dt_i': '2013-12-31', 'price': '41.31'}
  dictlist.append(price_dict)
  price_dict = {'dt_i': '2023-11-13', 'price': '19.17'}
  dictlist.append(price_dict)
  columns = list(price_dict.keys())
  dfprices = pd.DataFrame(dictlist, columns=columns)
  print(dfprices.to_string())
  return dfprices


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
  def __init__(self, refdate=None, datelist=None, date_n_price_ntlist=None):
    self.refdate = cnv.make_date_or_today(refdate)
    self.datelist = datelist
    self._date_n_price_ntlist = date_n_price_ntlist
    self._df = None
    self.dictlist = None
    # self.df_dates_n_prices = None
    self.trans_dates_into_df()

  @property
  def date_n_price_ntlist(self):
    return self._date_n_price_ntlist

  @property
  def df(self):
    if self._df is None:
      if self.datelist is not None:
        self.trans_dates_into_df()
    return self._df

  @date_n_price_ntlist.setter
  def date_n_price_ntlist(self, ntlist):
    if ntlist is None:
      self._date_n_price_ntlist = prices_dmass.get_date_n_price_ntlist()
    else:
      self._date_n_price_ntlist = ntlist

  def trans_dates_into_df(self):
    if self.datelist is None:
      return
    self._df = pd.DataFrame(columns=mfcalc.DATAFRAME_COLUMNS)
    for i, pdate in enumerate(self.datelist):
      mcc = mfcalc.MonetCorrCalculator(pdate, self.refdate, i)
      self._df.loc[i] = mcc.df.loc[i]

  def put_prices_from_date_price_ntlist_into_df(self, dates_n_prices_ntlist):
    """
    NT is NTDatesNPrices, fields=['date', 'price']
    """
    self._df.rename({'dt_i': 'date'}, inplace=True)
    self._df.set_index('date', inplace=True)
    local_columns = ['date', 'price']
    dfaux = pd.DataFrame(columns=local_columns)
    if dates_n_prices_ntlist is None or not iter(dates_n_prices_ntlist):
      return
    if len(dates_n_prices_ntlist) == 0:
      return
    for i, nt in enumerate(dates_n_prices_ntlist):
      try:
        dfrow = pd.DataFrame(nt, index=[0], columns=local_columns)
        dfaux[i] = dfrow[0]
      except (AttributeError, TypeError):
        return
    dfaux.set_index('date', inplace=True)
    pd.merge(self._df, dfaux, left_index=True, right_index=True)
    print(self._df.to_string())

  def integrate_prices_into_dates_dataframe(self, ntlist):
    """
    for i, pdate in enumerate(self.datelist):
      calcor = mfcalc.MonetCorrCalculator(pdate, self.refdate, rowindexfordf=i)
      self.df.loc[i] = calcor.df.loc[i]
    self.df[['dt_i', 'price']] = dfprices[['dt_i', 'price']]
    print('@ integrate_prices_into_dates_dataframe')
    print(self.df.to_string())
    """
    dfprices = pd.DataFrame(ntlist)
    dfprices.rename({'date': 'dt_i'}, axis=1, inplace=True)
    print('df', self.df.to_string())
    df = self.df
    dfprices = dfprices.set_index('dt_i')  # , inplace=True
    df = df.set_index('dt_i')  # , inplace=True
    print(df.to_string())
    print('dfprices', dfprices.to_string())
    dfres = pd.merge(df, dfprices, left_index=True, right_index=True)
    dfres['newprice'] = dfres['price'] * dfres['mul1']
    print('Result')
    print(dfres.to_string())

  def calc_monetcorr_w_datelist_n_refdate(self, strdatelist):
    """

    """
    # datelist = gendt.convert_strdatelist_to_datelist(strdatelist)
    datelist = intr.introspect_n_convert_sdlist_to_dates_w_or_wo_sep_n_posorder(strdatelist)
    if datelist is None:
      error_msg = f"""datelist was introspected as None
      strdatelist is {strdatelist}"""
      raise ValueError(error_msg)
    self._df = pd.DataFrame(columns=mfcalc.DATAFRAME_COLUMNS)
    for i, pdate in enumerate(datelist):
      # self.calc_monetcorr_bw_ref_n_a_comparedate(pdate)
      _ = i
      pass
    self._df = pd.DataFrame(self.dictlist, columns=mfcalc.DATAFRAME_COLUMNS)
    print(self.df.to_string())

  def update_prices(self):
    """
    self.calc_monetcorr_w_datelist_n_refdate()
    self.integrate_prices_into_dates_dataframe()
    """
    print(self.df.to_string())

  def __str__(self):
    outstr = """
    """
    return outstr


def create_adhoctest_calculator():
  dates = rwdl.fetch_dates_from_strdates_in_text_wo_sep_but_of_oneform_from_filepath()
  print('len =', len(dates), dates)
  today = datetime.date.today()
  yesterday = today - relativedelta(days=1)
  lcalcor = DatePriceRecordsMonetCorrCalculator(yesterday, dates)
  print(lcalcor.df.to_string())
  return lcalcor


def adhoctest():
  lcalcor = create_adhoctest_calculator()
  print(lcalcor)


def adhoctest2():
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
    dateini = cnv.make_date_or_none(args.ini[0])
    datefim = cnv.make_date_or_none(args.fim[0])
    print('i', dateini, 'f', datefim)
    mcc = mfcalc.MonetCorrCalculator(dateini, datefim)
    print(mcc.multiplication_factor)
    series = mcc.form_rowdict_with_explainparcels()
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
  adhoctest()
