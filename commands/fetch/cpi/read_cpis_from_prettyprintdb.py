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
import os
import re
import fs.db.db_settings as dbs
from models.budgets.pb.tmp1 import recomp
from models.finindices.cpis import cpis_cls
import settings as sett
# import fs.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_order
tablename = 'idxind_monthly_indices'
prettyprint_file_pattern = r'^(\d[4]\-\d[4]\s[1].+?[\.prettyprint\.dat]$)'
cmpld_prettyprint_file_pattern = re.compile(prettyprint_file_pattern)


class CPIPrettyPrintReader:

  # "{year_fr}-{year_to} {seriesid}.prettyprint.dat"
  prettyprint_file_pattern = prettyprint_file_pattern
  cmpld_prettyprint_file_pattern = cmpld_prettyprint_file_pattern

  def __init__(self, p_datafolder_abspath=None):
    self.datafolder_abspath = p_datafolder_abspath
    self.data_filename = None

  def treat_attrs(self):
    if self.datafolder_abspath is None or not os.path.isdir(self.datafolder_abspath):
      errmsg = f"datafolder_abspath {self.datafolder_abspath} does not exist. Please, verify data and retry."
      raise OSError(errmsg)

  def read_line_into_cpidatum(self):
    """
    if not isinstance(self.cpidatum, cpis_cls.CPIDatum):
      errmsg = f"cpidatum must have come up as type CPIDatum. Please, verify data and retry."
      raise ValueError(errmsg)
    """
    pass

  @property
  def data_filepath(self) -> os.path or None:
    if self.data_filename is None:
      return None
    return os.path.join(self.datafolder_abspath, self.data_filename)

  def read_text_datafile(self):
    """
    """
    for line in open(self.data_filepath, 'r').readline():
      pp = line.split('|')
      if len(pp) > 3:
        seriesid = pp[0]
        year = pp[1]
        month = pp[2]
        cpi_index = pp[3]
        footnotes = pp[4]
        cpidatum = cpis_cls.CPIDatum(
          seriesid,
          year,
          month,
          cpi_index,
          footnotes,
        )
        scrmsg = f"cpidatum = {cpidatum}"
        print(scrmsg)

  def datafile_by_pattern_name(self):
    filenames = os.listdir(self.datafolder_abspath)
    data_filename = None
    for filename in filenames:
      match = self.cmpld_prettyprint_file_pattern.search(filename)
      data_filename = None if match is None else match.group(1)
      if data_filename:
        break
    if data_filename is not None:
      self.data_filename = data_filename

  def read_thru_datafolder(self, p_datafolder_abspath=None):
    pass


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
  """
  https://www.kaggle.com/code/albeffe/regex-exercises-solutions
  https://www.w3resource.com/python-exercises/re/
  https://learnbyexample.github.io/py_regular_expressions/Exercise_solutions.html
  https://pythonistaplanet.com/python-regex-exercises/
  https://realpython.com/regex-python/
  https://www.rexegg.com/regex-boundaries.php

  """
  pass


if __name__ == '__main__':
  """
  process()
  """
  adhoctest()
