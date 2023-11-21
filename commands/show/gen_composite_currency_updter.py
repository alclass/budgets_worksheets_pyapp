#!/usr/bin/env python3
"""
gen_composite_currency_updter.py
Script to fetch both exchange rates and CPI indices.
The purpose is to generate an output with day to day
  composite money financial update indices.

Usage:
  $gen_composite_currency_updter.py <text file with dateadhoctests>

Input parameter:
  <text file with dateadhoctests> is the filename of a data file with set of dateadhoctests
  date1, date2, ..., dateN

Output:
  A list with composite_index1, composite_index2, ..., composite_indexN
  will be output to stdout

Example:
  $gen_composite_currency_updter.py datafile.dat
In datafile.dat:
2020-10-15
2021-07-01
2022-03-03
EOF

The output will be the money correcting/updating indices
"""
import datetime
from dateutil.relativedelta import relativedelta
import settings as cfg
import fs.economicfs.bcb_cotacao_fetcher_from_db_or_api as fin
from prettytable import PrettyTable
DEFAULT_DATESFILENAME = 'datesfile.dat'


def transform_strdates_to_pydates(dates):
  """
  This function probably exists in package-module dtfs
  (if so, refactor this)
  """
  pydates = []
  for eachdate in dates:
    if eachdate.find('-') > -1:
      pp = eachdate.split('-')
      dateorder = 'ymd'
    elif eachdate.find('/') > -1:
      pp = eachdate.split('/')
      dateorder = 'dmy'
    else:
      continue
    try:
      if dateorder == 'ymd':
        year = int(pp[0])
        month = int(pp[1])
        day = int(pp[2])
      else:
        day = int(pp[0])
        month = int(pp[1])
        year = int(pp[2])
      pydate = datetime.date(year, month, day)
      pydates.append(pydate)
    except (ValueError, IndexError) as _:
      continue
  return pydates


def get_variation_exchange_rate_from(pydate):
  """
  This function exists in package-module fin
  (if so, refactor this)

  """
  today = datetime.date.today()
  variation = None
  exrate_before = None
  exrate_after = None
  sql = 'SELECT exchangerate FROM exchangerates WHERE date=? and date=?;'
  tuplevalues = (pydate, today)
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


def get_cpi_baselineindex_in_month(pdate):
  """
  This function must be ENCAPSULATED in package-module fin
  The input pdate is transformed to a M-2 date ie month minus 2
  """
  if pdate is None:
    return None
  conn = cfg.get_connection()
  cursor = conn.cursor()
  seriesid = 'CUUR0000SA0'
  # make M-2
  refmonthdate = pdate + relativedelta(months=-2)
  # adjust day=1
  refmonthdate = datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=1)
  tuplevalues = (seriesid, refmonthdate)
  sql = """
    SELECT baselineindex FROM cpi_indices
      WHERE
        seriesid = ? and refmonthdate = ?;
  """
  cursor.execute(sql, tuplevalues)
  try:
    baselineindex = cursor.fetchone()[0]
  except TypeError:
    baselineindex = None
  # print('first_baselineindex', first_baselineindex)
  conn.close()
  # None may be returned
  return baselineindex


def get_last_available_cpi_baselineindex():
  """
  It searches for index by the most recent refmonthdate
  returns both the index and the most recent refmonthdate
  """
  conn = cfg.get_connection()
  cursor = conn.cursor()
  seriesid = 'CUUR0000SA0'
  sql = """
    SELECT baselineindex, refmonthdate FROM cpi_indices
      WHERE
        seriesid = ? 
      ORDER BY
        refmonthdate DESC
      LIMIT 1;
  """
  cursor.execute(sql, (seriesid, ))
  retval = cursor.fetchone()
  baselineindex = retval[0]
  mostrecent_refmonthdate = retval[1]
  conn.close()
  return baselineindex, mostrecent_refmonthdate


def get_cpi_variation_from(pydate):
  ini_cpi_baselineindex = get_cpi_baselineindex_in_month(pydate)
  if ini_cpi_baselineindex is None:
    return None, None, None, None
  fim_cpi_baselineindex, refdate = get_last_available_cpi_baselineindex()  # second return is refdate
  cpi_variation = (fim_cpi_baselineindex - ini_cpi_baselineindex) / ini_cpi_baselineindex
  return cpi_variation, ini_cpi_baselineindex, fim_cpi_baselineindex, refdate


def calc_composite_money_indices(pydates):
  correction_indices = []
  for pydate in pydates:
    exchange_variation = get_variation_exchange_rate_from(pydate)
    cpi_variation, ini_cpi_baselineindex, fim_cpi_baselineindex, refdate = get_cpi_variation_from(pydate)
    correction_indice = exchange_variation * cpi_variation
    correction_indices.append(correction_indice)
  return correction_indices


def get_exchangerate_variation_from(pydate):
  """
    namedtuple_res_bcb_api1 = apis.namedtuple_bcb_api1(
      cotacao_compra=exchanger.buyquote,
      cotacao_venda=exchanger.sellquote,
      cotacao_datahora=exchanger.quotesdatetime,
      param_date=exchanger.quotesdate, error_msg=None, gen_msg='Fetched from db', exchanger=exchanger
    )
  """
  res_bcb_api1 = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(pydate)
  first_exchangerate = res_bcb_api1.cotacao_venda
  today = datetime.date.today()
  yesterday = today - relativedelta(days=1)
  res_bcb_api1 = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(yesterday)
  exchangerate_variation = None
  last_exchangerate = None
  if res_bcb_api1:
    last_exchangerate = res_bcb_api1.cotacao_venda
    exchangerate_variation = (last_exchangerate - first_exchangerate) / first_exchangerate
  return exchangerate_variation, first_exchangerate, last_exchangerate


def get_pydates_from_datafile():
  datefilepath = cfg.get_datafile_abspath_in_app(DEFAULT_DATESFILENAME)
  fd = open(datefilepath)
  text = fd.read()
  dates = text.split('\n')
  print(dates)
  dates = map(lambda s: s.lstrip(' \t').rstrip(' \t\r\n'), dates)
  pydates = transform_strdates_to_pydates(dates)
  return pydates


def process_datesfile():
  pydates = get_pydates_from_datafile()
  output_list = []
  ptab = PrettyTable()
  ptab.field_names = [
    'seq', 'date', 'cpi_ini', 'cpi_fim', 'cpi_var',
    'exchange_ini', 'exchange_fim', 'exchange_var', 'multiplier',
  ]
  for i, pydate in enumerate(pydates):
    seq = i + 1
    cpi_variation, cpi_ini, cpi_fim, _ = get_cpi_variation_from(pydate)
    exchangerate_variation, exchange_ini, exchange_fim = get_exchangerate_variation_from(pydate)
    multiplier = (1 + cpi_variation) * (1 + exchangerate_variation)
    output_tuple = (
      seq, pydate, cpi_ini, cpi_fim, cpi_variation,
      exchange_ini, exchange_fim, exchangerate_variation, multiplier
    )
    output_list.append(output_tuple)
    ptab.add_row(list(output_tuple))
  print(ptab)
  return


def process():
  """
  pastdate = '2020-10-15'
  pydate = datetime.date(2020, 10, 15)

  """
  process_datesfile()


if __name__ == '__main__':
  process()
