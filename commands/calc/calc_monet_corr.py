#!/usr/bin/env python3
"""
calc_monet_corr.py

The underlying system or app, up til now, has used one particular form of monetary correction.
Let us call this "particular form" the "protocol for monet corr".

This protocol consists of multiplying two variations, ie:
  1 the variation of one correction index (here the one used is CPI_US)
  2 the variation of currency exchange rate (here the one used is BRL/USD)
  Other forms may be devised for this system in the future.

Let's see an example: suppose one want to find the monet corr between 2023-05-15 and 2022-10-25.

The CPI used here is a monthly index, and it takes more than one month, in relation to a month, to be known.
So the system searches the following indices:

for 2022-10-25, it fetches the CPI(2022-08), this is called "M-2", ie, two months before
for 2023-05-15, it fetches the CPI(2023-03), idem, M-2

The CPI, with rare exception, is a growing series. The increase is given by:

 variation_1 = ( CPI(2023-03) - CPI(2022-08) ) / CPI(2022-08)

The second variation, as informed above, is related to the exchange rate of currencies.
  So the same dates as above, we have:

 variation_2 = BRL_USD(2023-05-15) - BRL_USD(2022-10-25) / BRL_USD(2022-10-25)

The final multiplier (to find the monetary corrected value) is given by
  the composition of the two variations above, ie:

monet_corr_multiplier = (1 + variation_1) * (1 + variation_2)

--------------

As commented above, other variations/combinations may be implemented here in the future.

"""
import argparse
import datetime
import fs.economicfs.preapis_finfunctions as fin
import commands.show.gen_composite_currency_updter as compo  # for compo.get_cpi_baselineindex_in_month()
# import models.finindices.cpis as cps
import models.exrate.exratefetch as exrf  # for exr.find_most_recent_exrate()
import fs.datefs.dategenerators as gendt  # for make_refmonth_date_from_str
from dateutil.relativedelta import relativedelta


class MonetCorrCalculator:
  def __init__(self, dateini, datefim):
    self.calculation_not_possible = False
    self.dateini = dateini
    self.datefim = datefim
    self.treat_dates()
    self._cpi_ini = None
    self._cpi_fim = None
    self._exrate_ini = None
    self._exrate_fim = None
    self._monetcorr_multiplier = None
    self.calc_monet_corr_multiplier_between_dates()

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
    if self.calculation_not_possible:
      return None
    if self._cpi_ini is None:
      self._cpi_ini = compo.get_cpi_baselineindex_in_month(self.dateini_m2)
      if self._cpi_ini is None:
        self.calculation_not_possible = True
        return None
    return self._cpi_ini

  @property
  def cpi_fim(self):
    if self.calculation_not_possible:
      return None
    if self._cpi_fim is None:
      self._cpi_fim = compo.get_cpi_baselineindex_in_month(self.datefim_m2)
      if self._cpi_fim is None:
        self.calculation_not_possible = True
        return None
    return self._cpi_fim

  @property
  def exrate_ini(self):
    if self.calculation_not_possible:
      return None
    if self._exrate_ini is None:
      bcb = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(self.dateini)
      if bcb is None or bcb.cotacao_venda is None:
        self.calculation_not_possible = True
        return None
      self._exrate_ini = bcb.cotacao_venda
    return self._exrate_ini

  @property
  def exrate_fim(self):
    if self.calculation_not_possible:
      return None
    if self._exrate_fim is None:
      bcb = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(self.datefim)
      if bcb is None or bcb.cotacao_venda is None:
        self.calculation_not_possible = True
        return None
      self._exrate_fim = bcb.cotacao_venda
    return self._exrate_ini

  @property
  def monetcorr_multiplier(self):
    if self.calculation_not_possible:
      return None
    if self._monetcorr_multiplier is None:
      try:
        variation_1 = (self.cpi_fim - self.cpi_ini) / self.cpi_ini
        variation_2 = (self.exrate_fim - self.exrate_ini) / self.exrate_ini
        self._monetcorr_multiplier = (1 + variation_1) * (1 + variation_2)
      except (NameError, ValueError, TypeError):
        self.calculation_not_possible = True
    return self._monetcorr_multiplier

  def calc_monet_corr_multiplier_between_dates(self):
    """
    Calling property monetcorr_multiplier will start all attribute vars setting
    """
    _ = self.monetcorr_multiplier

  def get_tuplelist(self):
    return [(attr, value) for attr, value in self.__dict__.items() if not callable(attr)]

  def __str__(self):
    outstr = 'Calc Monet Corr\n'
    tuplelist = self.get_tuplelist()
    for tupl in tuplelist:
      outstr += '{fieldname} = {value}\n'.format(fieldname=tupl[0], value=tupl[1])
    return outstr


def calc_monet_corr_between_2_dates(date1, date2):
  """

  """
  mcc = MonetCorrCalculator(dateini=date1, datefim=date2)
  print(date1, date2, 'monetcorr_multiplier', mcc.monetcorr_multiplier)


def calc_monet_corr_between_datelist_n_mostrecent(datelist):
  """

  """
  datelist = gendt.convert_strdatelist_to_datelist(datelist)
  most_recent_date = exrf.find_most_recent_exrate_date()
  for pdate in datelist:
    calc_monet_corr_between_2_dates(pdate, most_recent_date)


def get_args_via_argparse():
  """
  https://realpython.com/command-line-interfaces-python-argparse/
  One Example:
    parser.add_argument("--veggies", nargs="+")
    parser.add_argument("--fruits", nargs="*")
      $ python cooking.py --veggies pepper tomato --fruits apple banana
    parser.add_argument("--size", choices=["S", "M", "L", "XL"], default="M")
    my_parser.add_argument("--weekday", type=int, choices=range(1, 8))
  """
  parser = argparse.ArgumentParser(description="Obtain Arguments")
  parser.add_argument(
    '-i', '--ini', metavar='date_ini', type=str, nargs='?',
    help="the beginning date in date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-f', '--fim', metavar='date_fim', type=str, nargs='?',
    help="the ending date in date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-cmc', '--calc-monet-corr', metavar='twodates', type=str, nargs=2,
    help="the ending date in date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-dl', '--datelist', metavar='datelist', type=str, nargs='+',
    help="datelist for finding daily exchange rate quotes one by one",
  )
  parser.add_argument(
    # example -rm "2023-04"
    '-rm', '--refmonth', type=str, nargs=1,
    help="the month as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-cy', '--current-year', action='store_true',
    help="days since the beginning of the current year as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-y', '--year', type=int, nargs=1,
    help="year as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-yr', '--yearrange', type=int, nargs=2,
    help="year range (ini, fim) as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-rdf', '--readdatefile', action='store_true',
    help="marker/signal for inputting the dates from the conventioned datefile located in the app's data folder",
  )
  parser.add_argument(
    '-s', '--serieschar', choices=["C", "S"], default="C",
    help="marker/signal for inputting the dates from the conventioned datefile located in the app's data folder",
  )
  parser.add_argument(
    '-cp', '--currencypair', type=str, nargs=1, default='brl/usd',
    help="for specifying the currency pair ratio that corresponds to the output quotes (default 'brl/usd')",
  )
  args = parser.parse_args()
  print('args =>', args)
  if args.refmonth is not None:
    # return calc_monet_corr_between_dates(args.refmonth)
    refmonthdate = args.refmonth[0]
    print('argparse refmonthdate', refmonthdate)
    return calc_monet_corr_between_datelist_n_mostrecent(refmonthdate)
  if args.year is not None:
    pass
  return args


def adhoctest():
  """
  -dl "2023-05-20" "2023-06-21"
  calc_monet_corr_between_datelist_n_mostrecent(args.datelist)
  yearini = 2020
  yearfim = 2022
  # read_yearrange_from_db(yearini, yearfim)
  calc_monet_corr_between_datelist_n_mostrecent(args.datelist)
  """
  args = get_args_via_argparse()
  twodates = args.calc_monet_corr
  try:
    return calc_monet_corr_between_2_dates(twodates[0], twodates[1])
  except (IndexError, TypeError):
    # if twodates is None or not subscriptable; TypeError is raised
    # if twodates, subscriptable, doesn't have at least 2 elements; IndexError is raised
    scrmsg = (
        'Missing argument: twodates must contain two dates from the command line parameter.'
        ' It cames as [%s]' % str(twodates)
    )
    print(scrmsg)


def process():
  """
  dateini = args.ini
  datefim = args.fim
  calc = MonetCorrCalculator(dateini, datefim)
  print(calc)
  args = get_args_via_argparse()
  calc_monet_corr_between_datelist_n_mostrecent(args.datelist)
  """


if __name__ == '__main__':
  """
  process()
  """
  adhoctest()
