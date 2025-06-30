#!/usr/bin/env python3
"""
commands/fetch/cpi/read_cpis_from_prettyprintdb.py

The data the script extracts is like the following pretty-print text table:

+-------------+------+--------+---------+-----------+
|   seriesID  | year | period |  value  | footnotes |
+-------------+------+--------+---------+-----------+
| CUUR0000SA0 | 2025 |  M02   | 319.082 |           |
| CUUR0000SA0 | 2025 |  M01   | 317.671 |           |
+-------------+------+--------+---------+-----------+
"""
import datetime
import fs.db.db_settings as dbs
import settings as sett
import fs.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_order
SERIESID_LIST = ['CUUR0000SA0', 'SUUR0000SA0']
tablename = 'idxind_monthly_indices'


class CPIDatum:

  def __init__(
      self,
      seriesid: str,
      year: str | int,
      refmonthdate: str | datetime.date,
      acc_index: float,
      footnootes=None
    ):
    self.seriesid = seriesid
    self.year = year
    self.refmonthdate = refmonthdate
    self.acc_index = acc_index
    self.footnotes = footnootes

  def treat_attribs(self):
    try:
      self.year = int(self.year)
    except ValueError:
      errmsg = f"year ({self.year}) was not passed as integer to class CPIDatum. Please, correct data and retry."
      raise ValueError(errmsg)
    if not isinstance(self.refmonthdate, datetime.datetime):
      self.refmonthdate = intr.make_refmonthdate_or_none(self.refmonthdate)
      if self.refmonthdate is None:
        errmsg = f"refmonthdate (None) was not passed to class CPIDatum. Please, correct data and retry."
        raise ValueError(errmsg)
    if self.seriesid is None or self.seriesid not in SERIESID_LIST:
      errmsg = (f"series {self.seriesid} was not passed to class CPIDatum"
                f" belonging to list {SERIESID_LIST}. Please, correct data and retry.")
      raise ValueError(errmsg)

  def __str__(self):
    outstr = """CPIDatum:
    self.seriesid = 
    self.year = 
    self.refmonthdate = 
    self.acc_index = 
    self.footnotes = 
    """
    return outstr


class CPIPrettyPrintReader:

  def __init__(self, cpidatum):
    self.cpidatum = cpidatum

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
      print('No cpi info to inserto to db.')
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
