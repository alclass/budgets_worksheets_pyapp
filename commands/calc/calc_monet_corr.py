#!/usr/bin/env python3
"""
commands/calc/calc_monet_corr.py

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
  more than one month period for a certain month's index
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

The Calculation Formula
-----------------------

Obs: [TO-DO] In the future, this system may allow
  configuring the composition of the terms for the calculation.

The CPI variation ratio is given by the following 2 terms
  (called below variations):

 variation_1 = ( CPI(2023-03) - CPI(2022-08) ) / CPI(2022-08)

The first variation, as informed above,
  is related to inflation, ie the loss of monetary power
  against itself through time.

The second variation, also as informed above,
  is related to the exchange rate of currencies. Notice
  that the premisse here is that the price under consideration
  is somehow influenced by the foreign currency.
  (This may or may not be the case, as said above,
  configuration may be implemented here to give more control to
  opting in or out of some terms or components in the calculation.)

Let's consider the BRL/USD exchange ratio variation
 for the two dates above:

 variation_2 = BRL_USD(2023-05-15) - BRL_USD(2022-10-25) / BRL_USD(2022-10-25)

In the second variation, there's no M-2 or M-1 convention.
  The "indices" are taken as the available exchange rates
  on the "day" dates themselves.

The two variations (1 & 2) altogether compose
  the "multiplier factor" that represents
  the monetary correction to be applied.

In a nutshell, this final multiplier
  (the monetary corrected factor) is given by
  the composition of the two variations above, as such:

monet_corr_multiplier = (1 + variation_1) * (1 + variation_2)
--------------
As commented above, other variations/combinations may be
  implemented in this system in the future.
"""
import datetime
import pandas as pd
import fs.datefs.datefunctions as dtfs
import fs.datefs.dategenerators as gendt  # for make_refmonth_date_from_str
from dateutil.relativedelta import relativedelta
import fs.economicfs.bcb.bcb_cotacao_fetcher_from_db_or_api as ftchr  # ftchr.BCBCotacaoFetcher
import fs.datefs.argparse as ap  # ap.get_args
import commands.fetch.cpi.read_cpis_from_db as cpi  # cpi.get_cpi_baselineindex_for_refmonth_in_db
# for compo.get_cpi_baselineindex_for_refmonth_in_db()
# import commands.show.show_table_with_variations_from_filedates_vs_mostrecent as compo


class MonetCorrCalculator:
  def __init__(self, dateini, datefim):
    self.dateini = dateini
    self.datefim = datefim
    self.treat_dates()
    self._cpi_ini = None
    self._cpi_fim = None
    self._exrate_ini = None
    self._exrate_fim = None
    self._monetcorr_multiplier = None
    self.df = None
    self.df_dates_n_prices = None
    self.calc_monet_corr_multiplier_between_dates()

  def are_four_values_available(self):
    if self.cpi_ini and self.cpi_fim and self.exrate_ini and self.exrate_fim:
      return True
    return False

  def treat_dates(self):
    if self.dateini is None:
      error_msg = 'Error: dateini is None.'
      raise ValueError(error_msg)
    if not isinstance(self.dateini, datetime.date):
      self.dateini = gendt.make_date_from_str(self.dateini)
      if self.dateini is None:
        error_msg = 'Error: dateini (%s) is not valid.' % self.dateini
        raise ValueError(error_msg)
    if self.datefim is None:
      error_msg = 'Error: datefim is None.'
      raise ValueError(error_msg)
    if not isinstance(self.datefim, datetime.date):
      self.datefim = gendt.make_date_from_str(self.datefim)
      if self.datefim is None:
        error_msg = 'Error: datefim (%s) is not valid.' % self.datefim
        raise ValueError(error_msg)
    if self.dateini > self.datefim:
      # swap positions
      tmpdate = self.dateini
      self.dateini = self.datefim
      self.datefim = tmpdate

  @property
  def refmonthini(self):
    """
    refmonth is a date for year & month whose day is conventioned as 1
    """
    return datetime.date(self.dateini.year, self.dateini.month, 1)

  @property
  def refmonthfim(self):
    """
    refmonth is a date for year & month whose day is conventioned as 1
    """
    return datetime.date(self.datefim.year, self.datefim.month, 1)

  @property
  def dateini_m2(self):
    """
    Minus 2 months from refmonthini
    """
    return self.refmonthini + relativedelta(months=-2)

  @property
  def datefim_m2(self):
    """
    Minus 2 months from refmonthfim
    """
    return self.refmonthfim + relativedelta(months=-2)

  @property
  def cpi_ini(self):
    if self._cpi_ini is None:
      self._cpi_ini = cpi.get_cpi_baselineindex_for_refmonth_in_db(self.dateini_m2)
      if self._cpi_ini is None:
        return None
    return self._cpi_ini

  @property
  def cpi_fim(self):
    if self._cpi_fim is None:
      self._cpi_fim = cpi.get_cpi_baselineindex_for_refmonth_in_db(self.datefim_m2)
      if self._cpi_fim is None:
        return None
    return self._cpi_fim

  @property
  def exrate_ini(self):
    """
      bcb = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(self.dateini)
    """
    if self._exrate_ini is None:
      bcb = ftchr.BCBCotacaoFetcher(pdate=self.dateini)
      if bcb is None or bcb.namedtuple_cotacao is None:
        return None
      if bcb.namedtuple_cotacao.cotacao_venda is None:
        return None
      self._exrate_ini = bcb.namedtuple_cotacao.cotacao_venda
    return self._exrate_ini

  @property
  def exrate_fim(self):
    """
      bcb = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(self.datefim)
    """
    if self._exrate_fim is None:
      bcb = ftchr.BCBCotacaoFetcher(pdate=self.datefim)
      if bcb is None or bcb.namedtuple_cotacao is None:
        return None
      if bcb.namedtuple_cotacao.cotacao_venda is None:
        return None
      self._exrate_fim = bcb.namedtuple_cotacao.cotacao_venda
    return self._exrate_fim

  @property
  def monetcorr_multiplier(self):
    if self._monetcorr_multiplier is not None:
      return self._monetcorr_multiplier
    if not self.are_four_values_available():
      return None
    self._monetcorr_multiplier = self.calc_monet_corr_multiplier_between_dates()
    return self._monetcorr_multiplier

  def calc_monet_corr_multiplier_between_dates(self):
    """
    """
    variation_1 = (self.cpi_fim - self.cpi_ini) / self.cpi_ini
    variation_2 = (self.exrate_fim - self.exrate_ini) / self.exrate_ini
    multiplier = (1 + variation_1) * (1 + variation_2)
    return multiplier

  def gen_rowdict(self):
    parcel1 = f"({self.cpi_fim:.4f}-{self.cpi_ini:.4f})/{self.cpi_ini:.4f}"
    parcel2 = f"({self.exrate_fim:.4f}-{self.exrate_ini:.4f})/{self.exrate_ini:.4f}"
    formula = f"=(1+{parcel1})*(1+{parcel2})"
    _ = formula
    outdict = {
      'dt_i': self.dateini,
      'cpi_i': self.cpi_ini,
      'exr_i': self.exrate_ini,
      'dt_f': self.datefim,
      'cpi_f': self.cpi_fim,
      'exr_f': self.exrate_fim,
      'mult': self.monetcorr_multiplier,
    }
    return outdict

  def get_tuplelist(self):
    return [(attr, value) for attr, value in self.__dict__.items() if not callable(attr)]

  def __str__(self):
    outstr = 'Calc Monet Corr\n'
    tuplelist = self.get_tuplelist()
    for tupl in tuplelist:
      outstr += '{fieldname} = {value}\n'.format(fieldname=tupl[0], value=tupl[1])
    return outstr


class DatePriceRecordsMonetCorrCalculator:
  def __init__(self, refdate=None):
    self.refdate = dtfs.make_date_or_today(refdate)
    self.dictlist = []
    self.df = None
    self.df_dates_n_prices = None
    self.df = pd.DataFrame(columns=['dt_i',  'cpi_i', 'exr_i', 'dt_f', 'cpi_f', 'exr_f', 'mult'])

  def set_dates_n_prices_ntlist(self, dates_n_prices_ntlist):
    """
    NT is NTDatesNPrices, fields=['date', 'price']
    """
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
    self.df_dates_n_prices = pd.DataFrame(dates_n_prices_ntlist)

  def integrate_date_price_into_df(self):
    self.df[['date', 'price']] = self.df_dates_n_prices

  def calc_monetcorr_bw_date_n_ref(self, otherdate):
    """

    """
    date1 = otherdate
    date2 = self.refdate
    mcc = MonetCorrCalculator(dateini=date1, datefim=date2)
    nrows = self.df.shape[0]
    print(date1, date2, 'nrows', nrows, 'monetcorr_multiplier', mcc.monetcorr_multiplier)
    pdict = mcc.gen_rowdict()
    self.dictlist.append(pdict)

  def calc_monetcorr_w_datelist_n_refdate(self, strdatelist):
    """

    """
    datelist = gendt.convert_strdatelist_to_datelist(strdatelist)
    for pdate in datelist:
      self.calc_monetcorr_bw_date_n_ref(pdate)
    self.df = pd.DataFrame(self.dictlist)
    print(self.df.to_string())

  def update_prices(self):
    self.calc_monetcorr_w_datelist_n_refdate()
    self.integrate_date_price_into_df()
    print(self.df.to_string())


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
    mcc = MonetCorrCalculator(dateini, datefim)
    mcc.calc_monet_corr_multiplier_between_dates()
    print(mcc.monetcorr_multiplier)
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
  """
  process()
