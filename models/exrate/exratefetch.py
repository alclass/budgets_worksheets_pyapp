#!/usr/bin/env python3
"""
exratefetch.py

"""
import sqlite3
import settings as sett
EXRATE_TABLENAME = 'daily_exchange_rates'
DATE_COLUMN = 'quotesdate'


def get_connection():
  return sqlite3.connect(sett.get_sqlite_appsdata_filepath())


def find_most_recent_exrate_date():
  conn = get_connection()
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  sql = 'SELECT * from {exrate_tablename} ORDER by {date_column} DESC LIMIT 1;'.format(
    exrate_tablename=EXRATE_TABLENAME,
    date_column=DATE_COLUMN,
  )
  fetcho = cursor.execute(sql)
  if fetcho:
    row = fetcho.fetchone()
    pdate = row[DATE_COLUMN]
    return pdate


def adhoctest():
  pdate = find_most_recent_exrate_date()
  print(' adhoctest find_most_recent_exrate_date()', pdate)


def process():
  """
  """
  pass


if __name__ == '__main__':
  """
  process()
  """
  adhoctest()
