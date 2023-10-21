#!/usr/bin/env python3
"""
dbfetchcpis.py
  contains helper function for fetching CPI data from db
"""
import datetime
import sqlite3
import settings as sett
import models.finindices.cpis as cps


def get_connection():
  return sqlite3.connect(sett.get_sqlite_appsdata_filepath())


def dbfetch_most_recent_refmonthdate_in_cpi(self):
  sql = """
  SELECT * from cpi_indices
  ORDER BY refmonthdate DESC LIMIT 1;
  """
  conn = get_connection()
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  cpi = None
  for row in rows:
    dictrow = dict(row)
    cpi = cps.CPIDatum.instantiate_from_dict(dictrow)
    print(cpi)
  conn.close()
  return cpi


def dbfetch_cpi_by_refmonthdate(self, refmonthdate):
  """

  """
  sql = """
  SELECT * from cpi_indices
  ORDER BY refmonthdate DESC LIMIT 1;
  """
  conn = get_connection()
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  cpi = None
  for row in rows:
    dictrow = dict(row)
    cpi = cps.CPIDatum.instantiate_from_dict(dictrow)
    print(cpi)
  conn.close()
  return cpi


def read_yearrange_from_db(yearini, yearfim, serieschar=None):
  """
  session = consa.get_sa_session()
  rows = session.execute(sql, tuplevalues)
  session.close()
  """
  seriesid = cps.find_seriesid_by_serieschar(serieschar)
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
  data = cps.CPIData()
  for dictrow in fetchobj:
    cpi = cps.CPIDatum.instantiate_from_dict(dictrow)
    data.append(cpi)
  print(data)


def process():
  pass


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()
