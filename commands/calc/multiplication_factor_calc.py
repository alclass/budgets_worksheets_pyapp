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

import fs.datefs.introspect_dates as intr  # for make_refmonth_date_from_str
"""
import copy
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import fs.indices.bcb_br.bcb_cotacao_fetcher_from_db_or_api as ftchr  # ftchr.BCBCotacaoFetcher
import commands.fetch.bls_us.read_cpis_from_db as cpi  # cpi_us.get_cpi_baselineindex_for_refmonth_in_db
DATAFRAME_COLUMNS = ['dt_i', 'cpi_i', 'exr_i', 'dt_f', 'cpi_f', 'exr_f', 'mult', 'mul1']
DECIMAL_PLACES_FOR_EQ = 4


class MonetCorrCalculator:
  def __init__(self, dateini, datefim, rowindexfordf=0, cpi_ini=None, cpi_fim=None, exrate_ini=None, exrate_fim=None):
    self.rowindexfordf = rowindexfordf
    self.dateini = dateini
    self.datefim = datefim
    self.treat_dates()
    self._cpi_ini = cpi_ini
    self._cpi_fim = cpi_fim
    self._cpi_var_ratio = None
    self._exrate_ini = exrate_ini
    self._exrate_fim = exrate_fim
    self._exrate_var_ratio = None
    self._multiplication_factor = None
    self._df = None
    self.df_dates_n_prices = None
    # make multiplication factor calculation
    _ = self.multiplication_factor

  def are_cpi_values_available(self):
    if self.cpi_ini and self.cpi_fim:
      return True
    return False

  def are_exrate_values_available(self):
    if self.exrate_ini and self.exrate_fim:
      return True
    return False

  def are_both_cpi_n_exrate_available(self):
    if self.are_cpi_values_available and self.are_exrate_values_available():
      return True
    return False

  def treat_dates(self):
    """
    Info on how to treat both dateini & datefim
    a) dateini cannot be None, if it is, a ValueError exception will be raised

    b) datafim can come in (ie be passed in) as None and, in this case,
      it's interpreted as "getting the default to it"
    However, if it's not originally None and returns None after make_date_or_none(),
      a ValueError exception will be raised, meaning an invalid date (or a non-conformant)
      came in.

    Notice the suttle difference in treatment for datefim, the default should
      not be applied if date is None after make_date_or_none(), only before it.
    """
    self.dateini = cnv.make_date_or_none(self.dateini)
    if self.dateini is None:
      error_msg = 'Error: dateini is None.'
      raise ValueError(error_msg)
    if self.datefim is None:
      # the default for datefim is today's date
      self.datefim = datetime.date.today()
      return
    orig_datefim = copy.copy(self.datefim)
    self.datefim = cnv.make_date_or_none(self.datefim)
    if self.datefim is None:  # at this point, datefim was not originally None
      error_msg = f'In the multiplication factor, datefim {orig_datefim} is not valid.'
      raise ValueError(error_msg)
    if self.dateini > self.datefim:
      scrmsg = f"dateini {self.dateini} is greater than datefim {self.datefim}"
      raise ValueError(scrmsg)

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
  def n_days(self):
    try:
      deltadays = self.datefim - self.dateini
      return deltadays.days
    except TypeError:
      pass
    return -1

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
    """
    if self._exrate_ini is not None:
      return self._exrate_ini
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
    """
    if self._exrate_fim is not None:
      return self._exrate_fim
    bcb = ftchr.BCBCotacaoFetcher(pdate=self.datefim)
    if bcb is None or bcb.namedtuple_cotacao is None:
      return None
    if bcb.namedtuple_cotacao.cotacao_venda is None:
      return None
    self._exrate_fim = bcb.namedtuple_cotacao.cotacao_venda
    return self._exrate_fim

  @property
  def cpi_var_ratio(self):
    """
    Calculates the ratio of how cpi_fim increases (or decreases) in relation to cpi_ini
    self._cpi_var_ratio = (self.cpi_fim - self.cpi_ini) / self.cpi_ini
    """
    if self._cpi_var_ratio is not None:
      return self._cpi_var_ratio
    if not self.are_cpi_values_available():
      return None
    self._cpi_var_ratio = (self.cpi_fim - self.cpi_ini) / self.cpi_ini
    return self._cpi_var_ratio

  def get_cpi_var_factor(self):
    """
    Calculates the "cpi_us-composite" for the multiplication factor in here
    This factor-component is: 1 + cpi_var_ratio
    """
    if self.are_both_cpi_n_exrate_available():
      cpi_ratio = self.cpi_var_ratio
      if cpi_ratio:
        return 1 + cpi_ratio
    return 1

  @property
  def exrate_var_ratio(self):
    """
    Calculates the ratio of how exrate_fim increases (or decreases) in relation to exrate_ini
    self._exrate_var_ratio = (self.exrate_fim - self.exrate_ini) / self.exrate_ini
    """
    if self._exrate_var_ratio is not None:
      return self._exrate_var_ratio
    if not self.are_exrate_values_available():
      return None
    self._exrate_var_ratio = (self.exrate_fim - self.exrate_ini) / self.exrate_ini
    return self._exrate_var_ratio

  def get_exrate_var_factor(self):
    """
    Calculates the "exrate-composite" for the multiplication factor in here
    This factor-component is: 1 + cpi_var_ratio
    """
    if self.are_exrate_values_available():
      return 1 + self.exrate_var_ratio
    return None

  @property
  def multiplication_factor_nolessthan1(self):
    """
    Cuts off the multiplication factor at 1 if it is less than 1
      (a king of 'floor value')
    Obs:
      Though inflation is the norm in the "world today",
        deflation sometimes happens.
      For conceptual cases where deflation becames significant,
        some new formulation may be devised here in the future.
      One possible cenario is to have an attenuation function,
        ie, a function that allows deflation in an attenuated way.
      E.g.: suppose it do it in ranges:
        range 1: from 0.95 to 1.0 considers 1 (the cut-off value already in-here)
        range 2: from 0.85 to 0.95 considers half the interval
          (ie, if multiplication_factor is 0.9, output midway to 1.0, ie 0.95)
          (ie, if multiplication_factor is 0.86, output midway to 1.0, ie 0.93)
        and so on

      Another cenario is to make an on/off control variable that, if it's on,
        will use the scheme devised above, and, if it's off,
        will use the whole multiplication factor without attenuation.
    """
    if self.are_both_cpi_n_exrate_available():
      return self.multiplication_factor if self.multiplication_factor >= 1 else 1.0
    return None

  @property
  def multiplication_factor(self):
    if self._multiplication_factor is not None:
      return self._multiplication_factor
    if not self.are_both_cpi_n_exrate_available():
      return None
    self._multiplication_factor = self.get_cpi_var_factor() * self.get_exrate_var_factor()
    return self._multiplication_factor

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

  def __eq__(self, o):
    dpeq = DECIMAL_PLACES_FOR_EQ
    try:
      if self.dateini == o.date_ini and self.datefim == o.datefim and self.rowindexfordf == o.rowindexfordf:
        if round(self.cpi_ini, dpeq) == round(o.cpi_ini, dpeq):
          if round(self.cpi_fim, dpeq) == round(o.cpi_fim, dpeq):
            if round(self.exrate_ini, dpeq) == round(o.exrate_ini, dpeq):
              if round(self.exrate_fim, dpeq) == round(o.exrate_fim, dpeq):
                return True
    except (AttributeError, TypeError):
      pass
    return False

  def form_rowdict_with_explainparcels(self):
    parcel1 = f"({self.cpi_fim:.4f}-{self.cpi_ini:.4f})/{self.cpi_ini:.4f}"
    parcel2 = f"({self.exrate_fim:.4f}-{self.exrate_ini:.4f})/{self.exrate_ini:.4f}"
    formula = f"=(1+{parcel1})*(1+{parcel2})"
    outdict = copy.copy(self.dfdict)
    outdict.update({
      'parcel1': parcel1,
      'parcel2': parcel2,
      'formula': formula,
    })
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
    on {self.dateini} => cpi_us {self.cpi_ini:04f} | on {self.datefim} => cpi_us {self.cpi_fim:04f}
    cpi_us ratio = {self.cpi_var_ratio:04f} | cpi_us factor = {self.get_cpi_var_factor():04f}
    exrate ratio = {self.exrate_var_ratio:04f} | cpi_us factor = {self.get_exrate_var_factor():04f}
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
