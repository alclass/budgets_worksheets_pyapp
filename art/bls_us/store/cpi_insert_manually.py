#!/usr/bin/env python3
"""
commands/fetch/cpi_us/cpi_insert_manually.py

The webpages for both CUUR0000SA0 & SUUR0000SA0 have both a table and a linear-graphic; their URL's are:
  https://data.bls.gov/timeseries/CUUR0000SA0
  https://data.bls.gov/timeseries/SUUR0000SA0
"""
import datetime
import lib.db.db_settings as dbs
import settings as sett
tablename = 'idxind_monthly_indices'


def get_triplelist_for_dbinserting():
  seriesid = 'CUUR0000SA0'
  triples_list = []
  refmonthdate, rm_idx = '2023-11-01', 307.051
  triple = (seriesid, refmonthdate, rm_idx)
  triples_list.append(triple)
  refmonthdate, rm_idx = '2023-12-01', 306.746
  triple = (seriesid, refmonthdate, rm_idx)
  triples_list.append(triple)
  refmonthdate, rm_idx = '2024-01-01', 308.417
  triple = (seriesid, refmonthdate, rm_idx)
  triples_list.append(triple)
  seriesid = 'SUUR0000SA0'
  refmonthdate, rm_idx = '2023-11-01', 171.219
  triple = (seriesid, refmonthdate, rm_idx)
  triples_list.append(triple)
  refmonthdate, rm_idx = '2023-12-01', 171.015
  triple = (seriesid, refmonthdate, rm_idx)
  triples_list.append(triple)
  refmonthdate, rm_idx = '2024-01-01', 171.910
  triple = (seriesid, refmonthdate, rm_idx)
  triples_list.append(triple)
  return triples_list


class ManInsertor:

  tablename = dbs.IDXIND_TABLENAME

  def __init__(self):
    self.conn = None
    self.cursor = None
    self.n_inserted = 0
    self.triples_list = get_triplelist_for_dbinserting()
    self.process()

  def open_connection(self):
    self.conn = sett.get_sqlite_connection()

  def close_connection(self):
    self.conn.close()

  def db_insert_row_into_cpis(self, sql, tuplevalues):
    cursor = self.conn.cursor()
    db_o = cursor.execute(sql, tuplevalues)
    print(self.n_inserted+1, 'Inserting', tuplevalues)
    if db_o:
      self.n_inserted += 1
    cursor.close()

  def db_insert_triples_list_into_cpis(self):
    if len(self.triples_list) < 1:
      print('No cpi_us info to inserto to db.')
      return
    self.open_connection()
    sql = f"""INSERT OR IGNORE INTO `{self.tablename}`
      (`seriesid`, `refmonthdate`, `baselineindex`, `created_at`) VALUES (?, ?, ?, ?);"""
    for triple in self.triples_list:
      seriesid, refmonthdate, rm_idx = triple
      created_at = datetime.datetime.now()
      tuplevalues = (seriesid, refmonthdate, rm_idx, created_at)
      self.db_insert_row_into_cpis(sql, tuplevalues)
    if self.n_inserted > 0:
      print('DB Committing', self.n_inserted)
      self.conn.commit()
    self.close_connection()

  def process(self):
    self.db_insert_triples_list_into_cpis()


def process():
  ManInsertor()


def adhoctest():
  pass


if __name__ == '__main__':
  """
  process()
  """
  adhoctest()
  process()
