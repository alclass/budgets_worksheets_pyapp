#!/usr/bin/env python3
"""
art/bls_us/store/insert_cpis_from_textfiles.py
  Inserts CPI data from textfiles to a database.

At the time of this writing, database is Sqlite.

The pretty-print input CPI data file is like so:
+-------------+------+--------+---------+-----------+
|   seriesID  | year | period |  value  | footnotes |
+-------------+------+--------+---------+-----------+
| CUUR0000SA0 | 2023 |  M09   | 307.789 |           |
| CUUR0000SA0 | 2023 |  M08   | 307.026 |           |
(...)

Notes on the table fragment above and the overall CPI data fetching strategy:

Notes on the table:

 => The 'period' column means the month in year, ie, for examples:
  M09 above is month 9 or September,
  M08 above is month 8 or August;
 => the 'value' column contains the accumulated CPI itself;

Notes on the overall CPI data fetching strategy:

 => the pretty-print is file-written by the REST API fetcher at
    commands.fetch.bls_cpi_api_fetcher.CPIFetcher;
 => indirectly, commands.fetch.verify_n_update_local_cpi_db.Verifier
    checks if more than one refmonth has elapsed so that CPIFetcher may be called
    aiming to find newly added monthy CPI indices.
"""
import datetime
import sqlite3
import settings as sett
import lib.datefs.refmonths_mod as rmd
from art.bls_us.bls_clss.cpis_cls import SERIESID_LIST
from art.bls_us..bls_clss.cpis_cls import DEFAULT_SERIESID
import commands.fetch.bls_us.read_cpis_from_prettyprintdb as ppdb
BLS_CPI_TABLENAME = 'bls_us_indices'


def get_conn():
  return sqlite3.connect(sett.get_sqlite_appsdata_filepath())


def create_table_if_not_exists():
  """
  Creates dbtable, if it does not yet exist, in the db-file whose filepath is given by settings.py
  """
  sql = f"""
  CREATE TABLE IF NOT EXISTS {BLS_CPI_TABLENAME} (
    seriesid varchar(12) NOT NULL,
    refmonthdate date NOT NULL,
    acc_index real NOT NULL,
    created_at datetime,
    modified_at datetime,
    PRIMARY KEY (seriesid, refmonthdate)
  )"""
  conn = get_conn()
  retval = conn.execute(sql)
  if retval:
    conn.commit()
  conn.close()


class Insertor:

  TABLENAME = BLS_CPI_TABLENAME

  def __init__(self, seriesid, refmonthdate, acc_index):
    self.seriesid = seriesid  # seriesid.lstrip(' ').rstrip(' ')
    self.refmonthdate = refmonthdate
    self.acc_index = acc_index
    self.created_at = datetime.datetime.now()
    self.dbfields_within_parentheses_str = '(seriesid, refmonthdate, acc_index, created_at, modified_at)'
    self.bool_inserted = None

  @property
  def treat_attrs(self):
    """
    Treats the instantiated input parameters
    """
    # treat seriesid
    if self.seriesid is None or self.seriesid not in SERIESID_LIST:
      self.seriesid = DEFAULT_SERIESID
    # treat refmonthdate
    self.refmonthdate = rmd.make_refmonth_or_m_minus_2(self.refmonthdate)
    if issubclass(self.acc_index, float):
      return
    # treat acc_index
    try:
      self.acc_index = float(self.acc_index)
    except ValueError as e:
      errmsg = (f"acc_index {self.acc_index} is not a valid float."
                f" Please, correct datum and retry.\n\t => {e}")
      raise ValueError(errmsg)

  @property
  def year(self):
    return self.refmonthdate.year

  @property
  def month(self):
    return self.refmonthdate.month

  @property
  def modified_at(self):
    """
    At this version, both created_at and modified_at are the same
    """
    return self.created_at

  @property
  def questionmarks(self):
    qm = '?,' * self.n_fields
    qm = '(' + qm[:-1] + ')'
    return qm

  @property
  def tuplevalues(self):
    return self.seriesid, self.refmonthdate, self.acc_index, self.created_at, self.modified_at

  @property
  def n_fields(self):
    return len(self.tuplevalues)

  def insert(self, conn):
    create_table_if_not_exists()
    sql = """INSERT OR IGNORE into {tablename}
      {fields_with_parentheses} 
      VALUES {questionmarks};""".format(
      tablename=self.TABLENAME,
      fields_with_parentheses=self.dbfields_within_parentheses_str,
      questionmarks=self.questionmarks
    )
    # conn = get_conn()
    cursor = conn.cursor()
    retval = cursor.execute(sql, self.tuplevalues)
    if retval.rowcount == 1:
      self.bool_inserted = True
      scrmsg = f"bool_inserted={self.bool_inserted} @insert"
      print(scrmsg)
      # conn.commit()  # commit will occur at the list's end by calling object
    else:
      self.bool_inserted = False
      scrmsg = f'retval.rowcount={retval.rowcount} not inserting'
      print(scrmsg)
    cursor.close()

  def __str__(self):
    outstr = f"Sqlite inserted={self.bool_inserted} {self.year}/{self.month:02} => cpi_us="
    outstr += f"accidx={self.acc_index} @ {self.seriesid}"
    return outstr


class BatchInsertor:

  def __init__(self):
    self.ppreader = ppdb.CPIPrettyPrintReader()
    self.n_eff_inserted = 0
    print(self.ppreader)
    self.conn = get_conn()
    self.n_eff_inserted = 0

  def insert_cpi_data_fr_prettyprintfiles(self):
    for i, cpidatum in enumerate(self.ppreader.gen_cpidatum_monthly_asc()):
      n_to_insert = i + 1
      ins = Insertor(
        seriesid=cpidatum.seriesid, refmonthdate=cpidatum.refmonthdate, acc_index=cpidatum.acc_index
      )
      scrmsg = f"Going to db-insert {n_to_insert}/{self.n_eff_inserted} {cpidatum}"
      print(scrmsg)
      scrmsg = "-"*40
      print(scrmsg)
      ins.insert(self.conn)
      if ins.bool_inserted:
        self.n_eff_inserted += 1

  def commit_at_the_end(self):
    scrmsg = "commit_at_the_end"
    print(scrmsg)
    self.conn.commit()
    self.conn.close()

  def process(self):
    self.insert_cpi_data_fr_prettyprintfiles()
    self.commit_at_the_end()


def adhoctest():
  pass


def process():
  bi = BatchInsertor()
  bi.process()


if __name__ == '__main__':
  """
  adhoctest1()
  """
  process()
