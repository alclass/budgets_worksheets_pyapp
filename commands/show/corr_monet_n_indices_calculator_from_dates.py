#!/usr/bin/env python3
"""
commands/show/corr_monet_n_indices_calculator_from_dates.py

  => script on maintenance!

commands/show/corr_monet_n_indices_calculator_from_dates.py
  Script to fetch both exchange rates and CPI indices.

The purpose is to gen_first_n_letterindices an output with day to day
  composite money financial update indices, each day contrasted to the most-recent data, ie,
  today or the last day that has results

Usage:
  $corr_monet_n_indices_calculator_from_dates.py <text-file-with-dates>

Input parameter:
   <text-file-with-dates> is the filename of a data file with set of dates
  date1 date2 ... dateN

Output:
  A list with composite_index1, composite_index2, ..., composite_indexN
  will be output to stdout

Example:
  $corr_monet_n_indices_calculator_from_dates.py datafile.dat
In datafile.dat:
2020-10-15
2021-07-01
2022-03-03
EOF

The output will be the money correcting/updating indices
"""
from collections import namedtuple
import datetime
import settings as cfg
import sqlite3
import fs.db.db_settings as dbs
import fs.economicfs.bcb.bcb_cotacao_fetcher_from_db_or_api as bcbfetch  # bcbfetch.BCBCotacaoFetcher
import fs.datefs.introspect_dates as idt  # idt.for make_date_or_none()
import fs.datefs.refmonths_mod as rfm  # rfm.calc_refmonth_minus_n()
import fs.datefs.read_write_datelist_files as rwdt
import commands.fetch.cpi.read_cpis_from_db as ftcpi  # ftcpi.get_cpi_baselineindex_for_refmonth_m2_in_db
from prettytable import PrettyTable
DEFAULT_DATESFILENAME = 'datesfile.dat'
DEFAULT_CURRENCY_PAIR = ('BRL', 'USD')
nt_cpi_n_exr = namedtuple('nt_cpi_n_exr', 'cpi exr')


def get_dates_from_strdates_file():
  datefilepath = cfg.get_datafile_abspath_in_app(DEFAULT_DATESFILENAME)
  fd = open(datefilepath)
  text = fd.read()
  dates = text.split('\n')
  print(dates)
  dates = map(lambda s: s.lstrip(' \t').rstrip(' \t\r\n'), dates)
  pdates = rwdt.convert_strdatelist_to_datelist_wo_sep_n_posorder(dates)
  return pdates


class CorrMonetWithinDatesCalculator:
  def __init__(self, topdate=None):
    self.topdate = idt.make_date_or_none(topdate)
    self.topdate = datetime.date.today() if self.topdate is None else self.topdate
    self.mostrecentdate = None
    self._most_recent_cpi = None
    self.m2refmonthdate = None
    self.find_mostrecent()
    self.cpi_exr_per_date_dict = {}  # type nt_cpi_n_exr

  @property
  def dates(self):
    return sorted(self.cpi_exr_per_date_dict.keys())

  def find_mostrecent(self):
    """
    The strategy here is to try 'today'; if it's not availabole, try 'yesterday'
    In any case, namedtuple_cotacao.param_date will point to the most recent date with exchange rate info
    """
    fetcher = bcbfetch.BCBCotacaoFetcher(self.topdate)
    self.mostrecentdate = fetcher.namedtuple_cotacao.param_date

  def get_sellquotesvariation_to_today_w_date_n_currencypair(self, pdate, currency_pair=None):
    """
        variation = (exrate_after - exrate_before) / exrate_before
    """
    t1_sellprice = self.get_exrate_sellquote_w_date_n_currencypair(pdate, currency_pair)
    if t1_sellprice is None:
      return None
    t2_sellprice = self.get_exrate_sellquote_w_date_n_currencypair(self.topdate, currency_pair)
    ratio = (t2_sellprice - t1_sellprice) / t1_sellprice
    return ratio

  @staticmethod
  def get_exrate_sellquote_w_date_n_currencypair(pdate, currency_pair=None):
    """
    This function exists in package-module fin
    (if so, refactor this)

    """
    if currency_pair is None:
      curr_numerator = DEFAULT_CURRENCY_PAIR[0]
      curr_denominator = DEFAULT_CURRENCY_PAIR[1]
    else:
      curr_numerator = currency_pair[0]
      curr_denominator = currency_pair[1]
    sql = f"""
      SELECT sellprice FROM {dbs.EXRATE_TABLENAME}
      WHERE
        refdate=? and
        curr_num=? and
        curr_num=?;"""
    tuplevalues = (pdate, curr_numerator, curr_denominator)
    conn = cfg.get_sqlite_connection()
    try:
      cursor = conn.cursor()
      retval = cursor.execute(sql, tuplevalues)
      if retval:
        row = retval.fetchone()
        sellprice = row[0]
        sellprice = sellprice / dbs.EXRATE_INTEGER_TO_FLOAT_DIVISOR
        return sellprice
    except (IndexError, sqlite3.OperationalError):  # sqlite3.SQLITE_ERROR
      pass
    # finally:
    #   conn.close()
    return None

  @property
  def most_recent_cpi_m2(self):
    """
    TO-DO: use this method with the purpose of verifying that cpi is close to topdate,
           otherwise, raise an exception for, a supposition, the cpi index is not yet available
    """
    if self._most_recent_cpi is None:
      self._most_recent_cpi, self.m2refmonthdate = ftcpi.get_cpi_baselineindex_for_refmonth_m2_in_db(
        self.mostrecentdate
      )
    return self._most_recent_cpi, self.m2refmonthdate

  def get_n_store_exrate_on_date(self, pdate):
    self.add_cpi_n_exr_on_date(pdate)
    nt_cpi_n_exr_o = self.cpi_exr_per_date_dict[pdate]
    return nt_cpi_n_exr_o.exr

  def get_n_store_cpi_for_m1_refmonth(self, pdate):
    pdate = idt.make_date_or_none(pdate)
    m1date = rfm.calc_refmonth_minus_n(pdate, 1)
    self.add_cpi_n_exr_on_date(m1date)
    nt_cpi_n_exr_o = self.cpi_exr_per_date_dict[m1date]
    return nt_cpi_n_exr_o.cpi

  def add_cpi_n_exr_on_date(self, pdate):
    pdate = idt.make_date_or_none(pdate)
    if pdate is None:
      errmsg = 'pdate is not a valid date (None) is add_cpi_n_exr_on_date()'
      raise ValueError(errmsg)
    cpi = ftcpi.get_cpi_baselineindex_for_refmonth_in_db(pdate)
    # exr = self.get_exrate_sellquote_w_date_n_currencypair(pdate)
    exr = self.get_exchangerate_on(pdate)
    exr = 0.0 if exr is None else exr
    nt_cpi_n_exr_o = nt_cpi_n_exr(cpi=cpi, exr=exr)
    self.cpi_exr_per_date_dict[pdate] = nt_cpi_n_exr_o

  def get_triple_cpivar_cpiini_cpifim_on_date(self, pdate):
    cpi_i = self.get_n_store_cpi_for_m1_refmonth(pdate)
    cpi_f = self.get_n_store_cpi_for_m1_refmonth(self.topdate)
    if cpi_i is None or cpi_f is None:
      return None, None, None,
    try:
      cpi_var = (cpi_f - cpi_i) / cpi_i
    except (TypeError, ZeroDivisionError):
      cpi_var = 0.0
    return cpi_var, cpi_i, cpi_f

  def get_triple_exrvar_exrini_exrfim_on_date(self, pdate):
    exr_i = self.get_n_store_exrate_on_date(pdate)
    exr_f = self.get_n_store_exrate_on_date(self.topdate)
    if exr_i is None or exr_i is None:
      return None, None, None,
    try:
      exr_var = (exr_f - exr_i) / exr_i
    except (TypeError, ZeroDivisionError):
      exr_var = 0.0
    return exr_var, exr_i, exr_f

  def get_not_storing_quad_cpivar_cpiini_cpifim_topdate_on_date(self, pdate):
    """
    This method fetches cpi value not storing it and calculate its variation
      relative to 'topdate'
    """
    if pdate in self.cpi_exr_per_date_dict:
      nt_cpi_n_exr_o = self.cpi_exr_per_date_dict[pdate]
      ini_cpi_baselineindex = nt_cpi_n_exr_o.cpi
    else:
      ini_cpi_baselineindex = ftcpi.get_cpi_baselineindex_for_refmonth_in_db(pdate)
    fim_cpi_baselineindex = self.get_n_store_cpi_for_m1_refmonth(self.topdate)
    if ini_cpi_baselineindex is None:
      return None, None, None, None
    try:
      cpi_variation = (fim_cpi_baselineindex - ini_cpi_baselineindex) / ini_cpi_baselineindex
    except TypeError:
      cpi_variation = 0
    return cpi_variation, ini_cpi_baselineindex, fim_cpi_baselineindex, self.topdate

  def calc_composite_corr_mone_from_date(self, pdate):
    exr_i = self.get_n_store_exrate_on_date(pdate)
    exr_f = self.get_n_store_exrate_on_date(self.topdate)
    cpi_i = self.get_n_store_cpi_for_m1_refmonth(pdate)
    cpi_f = self.get_n_store_cpi_for_m1_refmonth(self.topdate)
    if cpi_i is None:
      return 0.0
    try:
      cpi_var = (cpi_f - cpi_i) / cpi_i
      exr_var = (exr_f - exr_i) / exr_i
    except TypeError:
      cpi_var = 0.0
      exr_var = 0.0
    mone_corr_mult_fact = (1 + cpi_var) * (1 + exr_var)
    return mone_corr_mult_fact

  def calc_composite_money_indices(self, pdates):
    correction_indices = []
    for pdate in pdates:
      correction_indice = self.calc_composite_corr_mone_from_date(pdate)
      correction_indices.append(correction_indice)
    return correction_indices

  def get_exchangerate_on(self, pdate):
    try:
      fetcher = bcbfetch.BCBCotacaoFetcher(pdate)
      exr = fetcher.cotacao_venda
      # exr = exr10k / dbs.EXRATE_INTEGER_TO_FLOAT_DIVISOR
      return exr
    except (AttributeError, TypeError):
      pass
    return None

  def get_exchangerate_variation_from(self, pdate):
    """
      namedtuple_res_bcb_api1 = apis.namedtuple_bcb_api1(
        cotacao_compra=exchanger.buyprice,
        cotacao_venda=exchanger.sellprice,
        cotacao_datahora=exchanger.quote_as_datetime,
        param_date=exchanger.quotesdate, error_msg=None, gen_msg='Fetched from db', exchanger=exchanger
      )
    res_bcb_api1 = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)

    """
    try:
      fetcher = bcbfetch.BCBCotacaoFetcher(pdate)
      first_exchangerate = fetcher.namedtuple_cotacao.cotacao_venda
      fetcher = bcbfetch.BCBCotacaoFetcher(self.topdate)
      last_exchangerate = fetcher.namedtuple_cotacao.cotacao_venda
      exchangerate_variation = (last_exchangerate - first_exchangerate) / first_exchangerate
      return exchangerate_variation, first_exchangerate, last_exchangerate
    except (AttributeError, TypeError):
      pass
    return None, None, None

  def process_datesfile(self):
    dates = get_dates_from_strdates_file()
    for pdate in dates:
      self.add_cpi_n_exr_on_date(pdate)
    self.process()

  def process(self):
    output_list = []
    ptab = PrettyTable()
    ptab.field_names = [
      'seq', 'date', 'cpi_ini', 'cpi_fim', 'cpi_var',
      'exchange_ini', 'exchange_fim', 'exchange_var', 'multiplier',
    ]
    for i, pdate in enumerate(self.dates):
      seq = i + 1
      cpi_var, cpi_i, cpi_f = self.get_triple_cpivar_cpiini_cpifim_on_date(pdate)
      # cpi_var = 0 if cpi_var is None else cpi_var
      # exr_var, exr_i, exr_f = self.get_exchangerate_variation_from(pdate)
      exr_var, exr_i, exr_f = self.get_triple_exrvar_exrini_exrfim_on_date(pdate)
      exr_var = 0 if exr_var is None else exr_var
      multiplier = (1 + cpi_var) * (1 + exr_var)
      output_tuple = (
        seq, pdate, cpi_i, cpi_f, cpi_var,
        exr_i, exr_f, exr_var, multiplier
      )
      output_list.append(output_tuple)
      ptab.add_row(list(output_tuple))
    print(ptab)


def process():
  """
  pastdate = '2020-10-15'
  pydate = datetime.date(2020, 10, 15)

  """
  comparator = CorrMonetWithinDatesCalculator()
  comparator.process_datesfile()


if __name__ == '__main__':
  process()
