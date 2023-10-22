#!/usr/bin/env python3
"""
insert_cpis_from_textfiles.py

+-------------+------+--------+---------+-----------+
|   seriesID  | year | period |  value  | footnotes |
+-------------+------+--------+---------+-----------+
| CUUR0000SA0 | 2023 |  M09   | 307.789 |           |
| CUUR0000SA0 | 2023 |  M08   | 307.026 |           |
| CUUR0000SA0 | 2023 |  M07   | 305.691 |           |
"""
import datetime
import os
import sqlite3
import settings as sett
cuur_ending = 'CUUR0000SA0.dat'
suur_ending = 'SUUR0000SA0.dat'


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
    self.n_inserted += 1
    print(self.n_inserted+1, retval, '=>', sql)
    if retval.rowcount == 1:
      self.n_inserted += 1
      print(self.n_inserted, 'inserted & committing')
      conn.commit()
    conn.close()


def insert_cpis_from_file(filepath):
  lines = open(filepath).readlines()
  for line in lines:
    print(line)
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
      ins = Insertor(seriesid, year, month, bindex)
      ins.insert()
    except (IndexError, ValueError):
      pass


def get_files_in_folder():
  datafolderpath = sett.get_apps_data_abspath()
  entries = os.listdir(datafolderpath)
  # TO-DO verify only files fileentries = filter(lambda e: os.path.isfile(e)))
  print(datafolderpath)
  currfiles = sorted(filter(lambda e: e.endswith(cuur_ending), entries))
  surrfiles = sorted(filter(lambda e: e.endswith(suur_ending), entries))
  print(currfiles)
  print(surrfiles)
  allfilenames = currfiles + surrfiles
  filepaths = sorted(map(lambda e: os.path.join(datafolderpath, e), allfilenames))
  return filepaths


def process():
  filepaths = get_files_in_folder()
  for filepath in filepaths:
    insert_cpis_from_file(filepath)


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()
