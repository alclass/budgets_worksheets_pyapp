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
prettyprint_file_pattern = r'^(\d{4}\-\d{4}\s{1}.+?\.prettyprint\.dat)$'
cmpld_prettyprint_file_pattern = re.compile(prettyprint_file_pattern)


class CPIPrettyPrintReader:

  # "{year_fr}-{year_to} {seriesid}.prettyprint.dat"
  prettyprint_file_pattern = prettyprint_file_pattern
  cmpld_prettyprint_file_pattern = cmpld_prettyprint_file_pattern

  def __init__(self, p_datafolder_abspath=None):
    self.found_datafilenames = []
    self.datafolder_abspath = p_datafolder_abspath
    if self.datafolder_abspath is None:
      self.datafolder_abspath = sett.get_datafolder_abspath()
    self.cpis = []
    self.cpis_dict = {}  # this is a 2-D dict, one for seriesid, the other for refmonth
    self.process()

  def treat_attrs(self):
    if self.datafolder_abspath is None or not os.path.isdir(self.datafolder_abspath):
      errmsg = f"datafolder_abspath {self.datafolder_abspath} does not exist. Please, verify data and retry."
      raise OSError(errmsg)

  def get_filepath_from_filename(self, filename):
    return os.path.join(self.datafolder_abspath, filename)

  def show_cpis_found(self):
    for cpi in self.cpis:
      scrmsg = f"cpidatum = {cpi}"
      print(scrmsg)

  def read_line_into_cpidatum(self, line):
    """
    if not isinstance(self.cpidatum, cpis_cls.CPIDatum):
      errmsg = f"cpidatum must have come up as type CPIDatum. Please, verify data and retry."
      raise ValueError(errmsg)
    """
    pp = line.split('|')
    pp = filter(lambda c: c != '', pp)
    pp = list(map(lambda c: c.lstrip('\t ').rstrip(' '), pp))
    # print('Introspecting line ->', pp)
    if len(pp) > 3:
      try:
        seriesid = pp[0]
        year = int(pp[1])
        mmonth = pp[2]
        cpi_index = pp[3]
        footnotes = pp[4]
        cpidatum = cpis_cls.CPIDatum(
          seriesid=seriesid,
          year=year,
          refmonthdate=mmonth,
          acc_index=cpi_index,
          footnootes=footnotes
        )
        # scrmsg = f"Reading line cpidatum = {cpidatum}"
        # print(scrmsg)
        self.cpis.append(cpidatum)
        if seriesid in self.cpis_dict:
          refmonthdate_2nd_dim = self.cpis_dict[seriesid]
          if cpidatum.refmonthdate in refmonthdate_2nd_dim:
            # it has already been stored
            return
          refmonthdate_2nd_dim[cpidatum.refmonthdate] = cpidatum
          # added in the 2th level: refmonthdate
          return
        else:
          refmonthdate_2nd_dim = {cpidatum.refmonthdate: cpidatum}
          self.cpis_dict[seriesid] = refmonthdate_2nd_dim
          return
      except (IndexError, ValueError):
        pass

  def read_text_datafile(self, prettyprint_filename):
    """
    """
    prettyprint_filepath = self.get_filepath_from_filename(prettyprint_filename)
    fd = open(prettyprint_filepath, 'r')
    for line in fd.readlines():
      line = line.strip(' \t\r\n')
      self.read_line_into_cpidatum(line)

  def read_prettyprint_files(self):
    for i, prettyprint_filename in enumerate(self.found_datafilenames):
      seq = i + 1
      # scrmsg = f"{seq} -> reading prettyprint file {prettyprint_filename}"
      # print(scrmsg)
      self.read_text_datafile(prettyprint_filename)

  def find_prettyprint_files(self):
    filenames = os.listdir(self.datafolder_abspath)
    # print('filenames:', filenames)
    self.found_datafilenames = []
    for filename in filenames:
      match = self.cmpld_prettyprint_file_pattern.search(filename)
      data_filename = None if match is None else match.group(1)
      if data_filename:
        filepath = self.get_filepath_from_filename(data_filename)
        if os.path.isfile(filepath):
          self.found_datafilenames.append(data_filename)

  def convert_stored_dict_to_a_spreadsheet(self):
    pass

  def print_cpis(self):
    """
    For cpi display, the 2-D dict is sorted (to a tmp-dict) on the "two dimensions" each at a time
    """
    count = 0
    cpis_dict = dict(sorted(self.cpis_dict.items()))
    for seriesid in cpis_dict:
      refmonthdate_2nd_dim = self.cpis_dict[seriesid]
      refmonthdate_2d = dict(sorted(refmonthdate_2nd_dim.items()))
      for refmonthdate in refmonthdate_2d:
        count += 1
        scrmsg = f"{count} seriesid {seriesid} | refmonthdate {refmonthdate}"
        print(scrmsg)
        cpidatum = refmonthdate_2nd_dim[refmonthdate]
        print(cpidatum)

  def process(self):
    self.find_prettyprint_files()
    self.read_prettyprint_files()
    # self.show_cpis_found()
    self.print_cpis()


def process():
  CPIPrettyPrintReader()


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
  adhoctest()
  """
  process()
