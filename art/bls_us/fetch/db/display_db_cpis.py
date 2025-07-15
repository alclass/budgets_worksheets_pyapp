#!/usr/bin/env python3
"""
show_cpis.py
"""
import argparse
import datetime
import sqlite3
# import fs.db.conn_sa as consa
import settings as sett

DEFAULT_SERIESID = bls_us.DEFAULT_SERIESID


def read_yearrange_from_db(yearini, yearfim, serieschar=None):
  """
  session = consa.get_sa_session()
  rows = session.execute(sql, tuplevalues)
  session.close()
  """
  seriesid = bls_us.find_seriesid_by_serieschar(serieschar)
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
  data = bls_us.CPIData()
  for dictrow in fetchobj:
    cpi = bls_us.CPIDatum.instantiate_from_dict(dictrow)
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
    '-rm', '--refmonth', type=str, nargs='?',
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
    help="marker/signal for inputting the dateadhoctests from the conventioned datefile located in the app's data folder",
  )
  parser.add_argument(
    '-s', '--serieschar', choices=["C", "S"], default="C",
    help="marker/signal for inputting the dateadhoctests from the conventioned datefile located in the app's data folder",
  )
  parser.add_argument(
    '-cp', '--currencypair', type=str, nargs=1, default='brl/usd',
    help="for specifying the currency pair ratio that corresponds to the output quotes (default 'brl/usd')",
  )
  args = parser.parse_args()
  print('args =>', args)
  if args.refmonth is not None:
    pass
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
  adhoctest1()
  """
  process()
