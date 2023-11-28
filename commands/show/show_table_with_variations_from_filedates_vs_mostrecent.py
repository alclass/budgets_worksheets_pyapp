#!/usr/bin/env python3
"""
  => script on maintenance!

commands/show/show_table_with_variations_from_filedates_vs_mostrecent.py
  Script to fetch both exchange rates and CPI indices.

The purpose is to generate an output with day to day
  composite money financial update indices, each day contrasted to the most-recent data, ie,
  today or the last day that has results

Usage:
  $show_table_with_variations_from_filedates_vs_mostrecent.py <text-file-with-dates>

Input parameter:
   <text-file-with-dates> is the filename of a data file with set of dates
  date1 date2 ... dateN

Output:
  A list with composite_index1, composite_index2, ..., composite_indexN
  will be output to stdout

Example:
  $show_table_with_variations_from_filedates_vs_mostrecent.py datafile.dat
In datafile.dat:
2020-10-15
2021-07-01
2022-03-03
EOF

The output will be the money correcting/updating indices
"""
import datetime
import settings as cfg
import fs.economicfs.bcb.bcb_cotacao_fetcher_from_db_or_api as bcbfetch  # bcbfetch.BCBCotacaoFetcher
import commands.fetch.cpi.read_cpis_from_db as ftcpi  # ftcpi.get_cpi_baselineindex_for_refmonth_m2_in_db
import fs.datefs.datefunctions as dtfs
from prettytable import PrettyTable
DEFAULT_DATESFILENAME = 'datesfile.dat'


def get_pydates_from_datafile():
  datefilepath = cfg.get_datafile_abspath_in_app(DEFAULT_DATESFILENAME)
  fd = open(datefilepath)
  text = fd.read()
  dates = text.split('\n')
  print(dates)
  dates = map(lambda s: s.lstrip(' \t').rstrip(' \t\r\n'), dates)
  pdates = dtfs.transform_strdates_to_pydates(dates)
  return pdates


class Comparator:
  def __init__(self):
    self.today = datetime.date.today()
    self.mostrecentdate = None
    self._most_recent_cpi = None
    self.m2refmonthdate = None
    self.find_mostrecent()

  def find_mostrecent(self):
    """
    The strategy here is to try 'today'; if it's not availabole, try 'yesterday'
    In any case, namedtuple_cotacao.param_date will point to the most recent date with exchange rate info
    """
    fetcher = bcbfetch.BCBCotacaoFetcher(self.today)
    self.mostrecentdate = fetcher.namedtuple_cotacao.param_date

  def get_variation_exchange_rate_from(self, pdate):
    """
    This function exists in package-module fin
    (if so, refactor this)

    """
    today = self.today
    variation = None
    exrate_before = None
    exrate_after = None
    sql = 'SELECT exchangerate FROM exchangerates WHERE date=? and date=?;'
    tuplevalues = (pdate, today)
    conn = cfg.get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(sql, tuplevalues)
    if rows:
      try:
        exrate_before = rows[0][0]
        exrate_after = rows[0][1]
        variation = (exrate_after - exrate_before) / exrate_before
      except IndexError:
        pass
    conn.close()
    return variation, exrate_before, exrate_after

  @property
  def most_recent_cpi_m2(self):
    if self._most_recent_cpi is None:
      self._most_recent_cpi, self.m2refmonthdate = ftcpi.get_cpi_baselineindex_for_refmonth_m2_in_db(self.mostrecentdate)
    return self._most_recent_cpi, self.m2refmonthdate

  def get_cpi_variation_from(self, pdate):
    ini_cpi_baselineindex = ftcpi.get_cpi_baselineindex_for_refmonth_in_db(pdate)
    if ini_cpi_baselineindex is None:
      return None, None, None, None
    fim_cpi_baselineindex, refdate = self.most_recent_cpi_m2
    cpi_variation = (fim_cpi_baselineindex - ini_cpi_baselineindex) / ini_cpi_baselineindex
    return cpi_variation, ini_cpi_baselineindex, fim_cpi_baselineindex, refdate

  def calc_composite_money_indices(self, pdates):
    correction_indices = []
    for pdate in pdates:
      exchange_variation = self.get_variation_exchange_rate_from(pdate)
      cpi_variation, ini_cpi_baselineindex, fim_cpi_baselineindex, refdate = self.get_cpi_variation_from(pdate)
      correction_indice = exchange_variation * cpi_variation
      correction_indices.append(correction_indice)
    return correction_indices

  def get_exchangerate_variation_from(self, pdate):
    """
      namedtuple_res_bcb_api1 = apis.namedtuple_bcb_api1(
        cotacao_compra=exchanger.buyquote,
        cotacao_venda=exchanger.sellquote,
        cotacao_datahora=exchanger.quotesdatetime,
        param_date=exchanger.quotesdate, error_msg=None, gen_msg='Fetched from db', exchanger=exchanger
      )
    res_bcb_api1 = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)

    """
    try:
      fetcher = bcbfetch.BCBCotacaoFetcher(pdate)
      first_exchangerate = fetcher.namedtuple_cotacao.cotacao_venda
      fetcher = bcbfetch.BCBCotacaoFetcher(self.mostrecentdate)
      last_exchangerate = fetcher.namedtuple_cotacao.cotacao_venda
      exchangerate_variation = (last_exchangerate - first_exchangerate) / first_exchangerate
      return exchangerate_variation, first_exchangerate, last_exchangerate
    except (AttributeError, TypeError):
      pass
    return None, None, None

  def process_datesfile(self):
    pdates = get_pydates_from_datafile()
    output_list = []
    ptab = PrettyTable()
    ptab.field_names = [
      'seq', 'date', 'cpi_ini', 'cpi_fim', 'cpi_var',
      'exchange_ini', 'exchange_fim', 'exchange_var', 'multiplier',
    ]
    for i, pdate in enumerate(pdates):
      seq = i + 1
      cpi_variation, cpi_ini, cpi_fim, _ = self.get_cpi_variation_from(pdate)
      exchangerate_variation, exchange_ini, exchange_fim = self.get_exchangerate_variation_from(pdate)
      multiplier = (1 + cpi_variation) * (1 + exchangerate_variation)
      output_tuple = (
        seq, pdate, cpi_ini, cpi_fim, cpi_variation,
        exchange_ini, exchange_fim, exchangerate_variation, multiplier
      )
      output_list.append(output_tuple)
      ptab.add_row(list(output_tuple))
    print(ptab)


def process():
  """
  pastdate = '2020-10-15'
  pydate = datetime.date(2020, 10, 15)

  """
  comparator = Comparator()
  comparator.process_datesfile()


if __name__ == '__main__':
  process()
