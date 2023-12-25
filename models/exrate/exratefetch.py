#!/usr/bin/env python3
"""
exratefetch.py

"""
import sqlite3
import settings as sett
import fs.db.db_settings as dbs
EXRATE_TABLENAME = dbs.EXRATE_TABLENAME
DATE_COLUMN = 'refdate'


def get_connection():
  return sqlite3.connect(sett.get_sqlite_appsdata_filepath())


def find_most_recent_exrate_date_for_currpair_or_any(currency_pair=None):
  conn = get_connection()
  try:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = f"SELECT * from {EXRATE_TABLENAME} ORDER by {DATE_COLUMN} DESC LIMIT 1;"
    fetcho = cursor.execute(sql)
    if currency_pair is not None:
      sql = f"""
      SELECT * from {EXRATE_TABLENAME}
        WHERE
          curr_num=? and
          curr_den=?
        ORDER by {DATE_COLUMN} DESC LIMIT 1;"""
      curr_num, curr_den = currency_pair
      tuplevalues = (curr_num, curr_den)
      fetcho = cursor.execute(sql, tuplevalues)
    if fetcho:
      row = fetcho.fetchone()
      pdate = row[DATE_COLUMN]
      return pdate
  except (IndexError, sqlite3.SQLITE_ERROR):
    pass
  finally:
    conn.close()
  return None


def adhoctest():
  pdate = find_most_recent_exrate_date_for_currpair_or_any()
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
