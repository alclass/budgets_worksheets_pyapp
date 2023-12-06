#!/usr/bin/env python3
"""
commands/calc/multiplication_factor_calc.py
  contains the class (MonetCorrCalculator)
  that computes a multiplication factor that
  represents one particular way (among other ones possible)
  to quantify an increase or decrease in monetary correction between two dates.

Up to the time of this writing, the composition available here
  takes account of two varying public economic indices,
  one is the CPI_US and the other is the exchange rate
   between two determined currencies.

@see docstring in commands/calc/calc_monet_corr.py
  for more info.

The Calculation Formula
-----------------------

Obs: [TO-DO] In the future, this system may allow
  configuring the composition of the terms for the calculation,
  allowing other combinations of indices, currencies, exchange-rates sources etc.

The multiplication factor is given by the following 2 terms
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
  configuration may be implemented on this system to give more control,
  e.g. to opt in or out of some terms or components in the calculation.)

Let's consider the BRL/USD exchange ratio variation, curated by BCB,
  for the two dates above:

 variation_2 = BRL_USD(2023-05-15) - BRL_USD(2022-10-25) / BRL_USD(2022-10-25)

In the second variation, there's no M-2 or M-1 convention.
  The "indices" are taken as the available exchange rates
  on the "day" dates themselves, no "date-shifting".

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
import fs.datefs.introspect_dates as intr  # for make_refmonth_date_from_str
from dateutil.relativedelta import relativedelta
import fs.economicfs.bcb.bcb_cotacao_fetcher_from_db_or_api as ftchr  # ftchr.BCBCotacaoFetcher
import commands.fetch.cpi.read_cpis_from_db as cpi  # cpi.get_cpi_baselineindex_for_refmonth_in_db
DATAFRAME_COLUMNS = ['dt_i', 'cpi_i', 'exr_i', 'dt_f', 'cpi_f', 'exr_f', 'mult', 'mul1']


class MonetCorrCalculator:
  def __init__(self, dateini, datefim, rowindexfordf=0):
    self.rowindexfordf = rowindexfordf
    self.dateini = dateini
    self.datefim = datefim
    self.treat_dates()
    self._cpi_ini = None
    self._cpi_fim = None
    self._exrate_ini = None
    self._exrate_fim = None
    self._multiplication_factor = None
    self._multiplication_factor_nolessthan1 = None
    self._df = None
    self.df_dates_n_prices = None
    self.calc_monet_corr_multiplier_between_dates()

  def are_four_values_available(self):
    if self.cpi_ini and self.cpi_fim and self.exrate_ini and self.exrate_fim:
      return True
    return False

  def treat_dates(self):
    self.dateini = intr.introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(self.dateini)
    if self.dateini is None:
      error_msg = 'Error: dateini is None.'
      raise ValueError(error_msg)
    self.datefim = intr.introspect_n_convert_strdate_to_date_or_today_w_or_wo_sep_n_posorder(self.datefim)
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
  def cpi_variation_ratio(self):
    return (self.cpi_fim - self.cpi_ini) / self.cpi_ini

  @property
  def cpi_variation_factor(self):
    return 1 + (self.cpi_fim - self.cpi_ini) / self.cpi_ini

  @property
  def exrates_variation_ratio(self):
    return (self.exrate_fim - self.exrate_ini) / self.exrate_ini

  @property
  def exrates_variation_factor(self):
    return 1 + (self.exrate_fim - self.exrate_ini) / self.exrate_ini

  @property
  def multiplication_factor_nolessthan1(self):
    if self._multiplication_factor_nolessthan1 is not None:
      return self._multiplication_factor_nolessthan1
    mfactor = self.multiplication_factor
    self._multiplication_factor_nolessthan1 = mfactor if mfactor >= 1 else 1.0
    return self._multiplication_factor_nolessthan1

  @property
  def multiplication_factor(self):
    if self._multiplication_factor is not None:
      return self._multiplication_factor
    if not self.are_four_values_available():
      return None
    self.calc_monet_corr_multiplier_between_dates()
    return self._multiplication_factor

  def calc_monet_corr_multiplier_between_dates(self):
    """
    """
    self._multiplication_factor = self.cpi_variation_factor * self.exrates_variation_factor

  @property
  def dfdict(self):
    pdict = {
      'dt_i': self.dateini,
      'cpi_i': self.cpi_ini,
      'exr_i': self.exrate_ini,
      'dt_f': self.datefim,
      'cpi_f': self.cpi_fim,
      'exr_f': self.exrate_fim,
      'mult': self.multiplication_factor,
      'mul1': self.multiplication_factor_nolessthan1,
    }
    return pdict

  @property
  def df(self):
    """
    columns = ['dt_i',  'cpi_i', 'exr_i', 'dt_f', 'cpi_f', 'exr_f', 'mult', 'mul1']
    """
    columns = list(self.dfdict.keys())
    if columns != DATAFRAME_COLUMNS:
      error_msg = f"""Program inconsistency that needs correction.
      The two lists below need to be the same:
      a) instantiated columns = {columns}
      b) is different than the module-exportable one = {DATAFRAME_COLUMNS}.
      The simpler correction is to rewrite the second one above."""
      raise ValueError(error_msg)
    idxlist = [self.rowindexfordf]
    if self._df is None:
      self._df = pd.DataFrame(self.dfdict, index=idxlist, columns=columns)
    return self._df

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
      'mult': self.multiplication_factor,
    }
    return outdict

  def get_tuplelist(self):
    return [(attr, value) for attr, value in self.__dict__.items() if not callable(attr)]

  def show_properties_from_get_tuplelist(self):
    outstr = 'Calc Monet Corr\n'
    tuplelist = self.get_tuplelist()
    for tupl in tuplelist:
      outstr += '{fieldname} = {value}\n'.format(fieldname=tupl[0], value=tupl[1])
    return outstr

  def __str__(self):
    outstr = f"""Monetary Correction Calculator:
    on {self.dateini} => cpi {self.cpi_ini:04f} | on {self.datefim} => cpi {self.cpi_fim:04f}
    cpi ratio = {self.cpi_variation_ratio:04f} | cpi factor = {self.cpi_variation_factor:04f}
    exrate ratio = {self.exrates_variation_ratio:04f} | cpi factor = {self.exrates_variation_factor:04f}
    multiplication factor = {self.multiplication_factor}
    """
    return outstr


def adhoctest():
  """
  """
  dateini = '2023-01-01'
  datefim = '2023-10-11'
  calc = MonetCorrCalculator(dateini, datefim)
  print(calc)
  print(calc.df.to_string())


def process():
  pass


if __name__ == '__main__':
  """
  """
  process()
  adhoctest()
