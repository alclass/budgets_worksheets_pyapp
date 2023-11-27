#!/usr/bin/env python3
"""
insert_cpis_from_textfiles.py
  inserts CPI data from textfiles to a database.

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
import glob
import os
import sqlite3
import settings as sett
import fs.os.osfunctions as osfs
curseriesid = 'CUUR0000SA0'
surseriesid = 'SUUR0000SA0'
seriesfile_dotext = '.dat'
cur_ending = f'{curseriesid}.prettyprint{seriesfile_dotext}'
sur_ending = f'{surseriesid}.prettyprint{seriesfile_dotext}'


def get_conn():
  return sqlite3.connect(sett.get_sqlite_appsdata_filepath())


def create_table_if_not_exists():
  """
  """
  sql = """
  CREATE TABLE IF NOT EXISTS cpi_indices (
    seriesid varchar(12) NOT NULL,
    refmonthdate date NOT NULL,
    baselineindex real NOT NULL,
    created_at datetime,
    modified_at datetime,
    PRIMARY KEY (seriesid, refdate)
  )"""
  conn = get_conn()
  retval = conn.execute(sql)
  if retval:
    conn.commit()
  conn.close()


class Insertor:

  TABLENAME = 'cpi_indices'

  def __init__(self, seriesid, year, month, baselineindex):
    self.seriesid = seriesid.lstrip(' ').rstrip(' ')
    self.year = int(year)
    self.month = int(month)
    self.baselineindex = float(baselineindex)
    self.created_at = datetime.datetime.now()
    self.n_inserted = 0

  @property
  def refdate(self):
    return datetime.date(year=self.year, month=self.month, day=1)

  @property
  def refmonthdate(self):
    return self.refdate

  @property
  def modified_at(self):
    return self.created_at

  @property
  def fields_with_parentheses(self):
    return '(seriesid, refmonthdate, baselineindex, created_at, modified_at)'

  @property
  def questionmarks(self):
    qm = '?,' * 5
    qm = '(' + qm[:-1] + ')'
    return qm

  @property
  def tuplevalues(self):
    return self.seriesid, self.refdate, self.baselineindex, self.created_at, self.modified_at

  def insert(self):
    create_table_if_not_exists()
    sql = """INSERT OR IGNORE into {tablename}
      {fields_with_parentheses} 
      VALUES {questionmarks};""".format(
      tablename=self.TABLENAME,
      fields_with_parentheses=self.fields_with_parentheses,
      questionmarks=self.questionmarks
    )
    conn = get_conn()
    cursor = conn.cursor()
    retval = cursor.execute(sql, self.tuplevalues)
    if retval.rowcount == 1:
      self.n_inserted += 1
      print(self.n_inserted, 'inserted & committing')
      conn.commit()
    conn.close()

  def __str__(self):
    bool_ins = self.n_inserted > 0
    outstr = f"Sqlite inserted={bool_ins} {self.year}/{self.month:02} => cpi="
    outstr += f"{self.baselineindex} @ {self.seriesid}"
    return outstr


def insert_cpis_from_file(filepath):
  lines = open(filepath).readlines()
  seq = 0
  total_insert = 0
  last_seriesid = None
  for line in lines:
    # print(line)
    values = line.split('|')
    values = filter(lambda e: e not in ['', '\n'], values)
    values = list(filter(lambda e: not e.startswith('   '), values))
    try:
      seriesid = values[0]
      yearstr = values[1]
      yearstr = yearstr.strip(' ')
      year = int(yearstr)
      monthstr = values[2]
      if monthstr.find('value') > -1:
        continue
      monthstr = monthstr.lstrip(' M').rstrip(' ')
      month = int(monthstr)
      bindex = values[3]
      # print('month, year, bindex, seriesid', seriesid, year, month, bindex)
      seq += 1
      ins = Insertor(seriesid, year, month, bindex)
      ins.insert()
      print(seq, ins)
      total_insert += ins.n_inserted
      last_seriesid = seriesid
    except (IndexError, ValueError):
      pass
  print('Total inserted', total_insert, 'seriesid', last_seriesid)


def get_prettyprint_cpi_series_data_filepaths_in_folder():
  datafolderpath = sett.get_apps_data_abspath()
  ospaths = glob.glob(datafolderpath + '/*' + seriesfile_dotext)
  # sorted() is required because map/filter/etc consume the iterable making it empty for another time
  fileentries = sorted(filter(lambda e: os.path.isfile(e), ospaths))
  curfilepaths = sorted(filter(lambda e: e.endswith(cur_ending), fileentries))
  surfilepaths = sorted(filter(lambda e: e.endswith(sur_ending), fileentries))
  filepaths = curfilepaths + surfilepaths
  osfs.print_filenames_from_filepaths(filepaths, datafolderpath)
  return filepaths


def adhoctest():
  pass


def process():
  filepaths = get_prettyprint_cpi_series_data_filepaths_in_folder()
  for filepath in filepaths:
    insert_cpis_from_file(filepath)


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()
