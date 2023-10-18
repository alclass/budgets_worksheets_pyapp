#!/usr/bin/env python3
"""
calc_monet_corr.py
"""
import argparse
import datetime
import sqlite3
import fs.economicfs.preapis_finfunctions as fin
import commands.show.gen_composite_currency_updter as compo  # compo.get_cpi_baselineindex_in_month()
import models.CPIs as cpis
import settings as sett
import fs.datefs.dategenerators as gendt
# import fs.db.conn_sa as consa


def get_connection():
  return sqlite3.connect(sett.get_sqlite_appsdata_filepath())


def calc_monet_corr_between_dates(dateini, datefim):
  rateini = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(dateini)
  if rateini is None:
    print(dateini, 'did not find rate')
    return
  ratefim = fin.dbfetch_bcb_cotacao_compra_dolar_apifallback(datefim)
  if ratefim is None:
    print(datefim, 'did not find rate')
    return
  rate_var = (ratefim.venda - rateini.venda) / rateini.venda
  cpi_ini = compo.get_cpi_baselineindex_in_month(dateini)
  cpi_fim = compo.get_cpi_baselineindex_in_month(datefim)
  cpi_var = (cpi_fim - cpi_ini) / cpi_ini
  var_composite = (1 + rate_var) * (1 + cpi_var)
  return var_composite


def get_most_recent_cpi_date():
  sql = """
  SELECT * from cpi_indices
  ORDER BY refmonthdate DESC LIMIT 1;
  """
  conn = get_connection()
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  for row in rows:
    dictrow = dict(row)
    cpi = cpis.CPIDatum.instantiate_from_dict(dictrow)
    print(cpi)
  conn.close()
  return cpi


def calc_monet_corr_between_refmonthdates_n_mostrecent(refmonthdate):
  datefim = get_most_recent_cpi_date()
  for pdate in gendt.gen_daily_dates_for_refmonth(refmonthdate):
    dateini = pdate
    calc_monet_corr_between_dates(dateini, datefim)

def find_seriesid_by_serieschar(serieschar):
  if serieschar == 'C':
    return 'CUUR0000SA0'
  elif serieschar == 'S':
    return 'SUUR0000SA0'
  else:
    return DEFAULT_SERIESID


def read_yearrange_from_db(yearini, yearfim, serieschar=None):
  """
  session = consa.get_sa_session()
  rows = session.execute(sql, tuplevalues)
  session.close()
  """
  seriesid = find_seriesid_by_serieschar(serieschar)
  sql = """SELECT * from cpi_indices
    WHERE
      seriesid= ? and
      refmonthdate >= ? and
      refmonthdate <= ?
    ORDER BY refmonthdate;
  """
  dateini = datetime.date(year=yearini, month=1, day=1)
  datefim = datetime.date(year=yearfim, month=12, day=31)
  sqlitefile = sett.get_sqlite_appsdata_filepath()
  conn = sqlite3.connect(sqlitefile)
  tuplevalues = (seriesid, dateini, datefim)
  print(sql, tuplevalues)
  conn.row_factory = sqlite3.Row  # for returning rows as dict
  cursor = conn.cursor()
  fetchobj = cursor.execute(sql, tuplevalues)
  data = CPIData()
  for dictrow in fetchobj:
    cpi = CPIDatum.instantiate_from_dict(dictrow)
    data.append(cpi)
  print(data)


def adhoctest():
  yearini = 2020
  yearfim = 2022
  read_yearrange_from_db(yearini, yearfim)


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
    '-i', '--ini', metavar='date_ini', type=str, nargs=1,
    help="the beginning date in date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-f', '--fim', metavar='date_fim', type=str, nargs='?',
    help="the ending date in date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
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
    return calc_monet_corr_between_refmonthdates_n_mostrecent(refmonthdate)
  if args.year is not None:
    pass
  if args.yearrange is not None:
    yearini = args.yearrange[0]
    yearfim = args.yearrange[1]
    serieschar = args.serieschar
    return read_yearrange_from_db(yearini, yearfim, serieschar)
    # print(yearini, yearfim)


def process():
  get_args_via_argparse()


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()
