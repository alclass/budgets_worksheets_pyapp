#!/usr/bin/env python3
"""
commands/fetch/cpi_us/read_cpis_from_prettyprintdb.py

The data the script extracts is like the following pretty-print text table:

+-------------+------+--------+---------+-----------+
|   seriesID  | year | period |  value  | footnotes |
+-------------+------+--------+---------+-----------+
| CUUR0000SA0 | 2025 |  M02   | 319.082 |           |
| CUUR0000SA0 | 2025 |  M01   | 317.671 |           |
+-------------+------+--------+---------+-----------+
"""
import datetime
# import datetime
import os
import re
# from fs.indices.bls_us.report_reqstatus_in_jsondatafiles_cls import DEFAULT_BLS_DATA_FOLDERNAME
# import fs.db.db_settings as dbs
# from models.budgets.pb.tmp1 import recomp
from art.bls_us.bls_clss import cpis_cls
import settings as sett
from commands.fetch.bls_us.read_cpis_from_db import DEFAULT_SERIESID
from commands.fetch.bls_us.read_cpis_from_db import KNOWN_SERIESID
import lib.datefs.refmonths_mod as rmd
tablename = 'idxind_monthly_indices'
prettyprint_file_pattern = r'^(\d{4}\s{1}[a-zA-Z0-9]+?\s{1}prettyprint\.txt)$'
cmpld_prettyprint_file_pattern = re.compile(prettyprint_file_pattern)
prettyprint_file_tointerpol = "{year} {seriesid} prettyprint.txt"


class CPIPrettyPrintReader:

  # "{year_fr}-{year_to} {seriesid}.prettyprint.dat"
  prettyprint_file_pattern = prettyprint_file_pattern
  cmpld_prettyprint_file_pattern = cmpld_prettyprint_file_pattern
  prettyprint_file_tointerpol = prettyprint_file_tointerpol
  bls_foldername = 'bls_cpi_data'

  def __init__(self, seriesid=None, p_datafolder_abspath=None):
    self.found_datafilenames = []
    self.seriesid = seriesid
    self.datafolder_abspath = p_datafolder_abspath  # this is the root data folder, the BLS one is a dynamic attribute
    self.treat_attrs()
    self.refmonths_n_cpis_dict = {}  # this is a 2-D dict, one for seriesid, the other for refmonth
    self._refmonths = None
    # dynamic (property) attributes without an "invisible" (underline prefixed) variable
    # self.total_cpi_indices
    # self.total_cpi_years
    # self.start_year
    # self.end_year
    # self.first_refm_n_cpi_in_db
    # self.last_refm_n_cpi_in_db

    self.process()

  def treat_attrs(self):
    if self.seriesid is None or self.seriesid not in KNOWN_SERIESID:
      self.seriesid = DEFAULT_SERIESID
    if self.datafolder_abspath is None:
      self.datafolder_abspath = sett.get_datafolder_abspath()
    if self.datafolder_abspath is None or not os.path.isdir(self.datafolder_abspath):
      errmsg = f"datafolder_abspath {self.datafolder_abspath} does not exist. Please, verify data and retry."
      raise OSError(errmsg)

  @property
  def cpis(self):
    return self.refmonths_n_cpis_dict.values()

  @property
  def bls_folderpath(self):
    return os.path.join(self.datafolder_abspath, self.bls_foldername)

  def get_prettyprintfilepath_fr_filename(self, filename: str) -> os.path:
    return os.path.join(self.bls_folderpath, filename)

  def get_prettyprintpfilepath_by_year(self, year):
    filename = prettyprint_file_pattern.format(year=year)
    return self.get_prettyprintfilepath_fr_filename(filename)

  def read_line_into_cpidatum(self, line: str) -> None:
    """
    if not isinstance(self.cpidatum, cpis_cls.CPIDatum):
      errmsg = f cpidatum must have come up as type CPIDatum, please verify data and retry.
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
        refmonthdate = rmd.get_refmonthdate_fr_mmonth_n_year_or_none(mmonth, year)
        if refmonthdate is None:
          return
        cpi_index = pp[3]
        footnotes = pp[4]
        cpidatum = cpis_cls.CPIDatum(
          seriesid=seriesid,
          year=year,
          refmonthdate=refmonthdate,
          acc_index=cpi_index,
          footnootes=footnotes
        )
        # scrmsg = f"Reading line cpidatum = {cpidatum}"
        # print(scrmsg)
        self.refmonths_n_cpis_dict.update({refmonthdate: cpidatum})
      except (IndexError, ValueError):
        pass

  def read_text_datafilepath(self, pp_filepath: os.path) -> None:
    """
    """
    if not os.path.isfile(pp_filepath):
      return None
    fd = open(pp_filepath, "r")
    line = fd.readline()
    while line:
      line = line.strip(' \t\r\n')
      self.read_line_into_cpidatum(line)
      line = fd.readline()
    return None

  def read_text_datafilename(self, prettyprint_filename):
    prettyprint_filepath = self.get_prettyprintfilepath_fr_filename(prettyprint_filename)
    return self.read_text_datafilepath(prettyprint_filepath)

  def read_text_datafile_by_year(self, year):
    filename = self.prettyprint_file_tointerpol.format(seriesid=self.seriesid, year=year)
    return self.read_text_datafilename(filename)

  def get_cpis_dict(self, year) -> dict[datetime.datetime: cpis_cls.CPIDatum]:
    self.read_text_datafile_by_year(year)
    return self.refmonths_n_cpis_dict

  def read_prettyprint_files(self):
    for i, prettyprint_filename in enumerate(self.found_datafilenames):
      # seq = i + 1
      # scrmsg = f"{seq} -> reading prettyprint file {prettyprint_filename}"
      # print(scrmsg)
      self.read_text_datafilename(prettyprint_filename)

  def find_prettyprint_files(self):
    filenames = os.listdir(self.bls_folderpath)
    # print('filenames:', filenames)
    self.found_datafilenames = []
    for filename in filenames:
      match = self.cmpld_prettyprint_file_pattern.search(filename)
      data_filename = None if match is None else match.group(1)
      if data_filename:
        filepath = self.get_prettyprintfilepath_fr_filename(data_filename)
        if os.path.isfile(filepath):
          self.found_datafilenames.append(data_filename)

  def gen_cpidatum_monthly_asc(self):
    for refmonthdate in self.refmonths:
      cpidatum = self.refmonths_n_cpis_dict[refmonthdate]
      yield cpidatum

  def process(self):
    scrmsg = 'Step 1 find_prettyprint_files()'
    print(scrmsg)
    self.find_prettyprint_files()
    print(self.found_datafilenames)
    scrmsg = 'Step 2 read_prettyprint_files()'
    print(scrmsg)
    self.read_prettyprint_files()
    scrmsg = 'Step 3 show_cpis_found()'
    print(scrmsg)
    scrmsg = 'Step 5 print_cpis()'
    print(scrmsg)
    self.print_cpis()
    scrmsg = '='*40
    print(scrmsg)
    print(self)

  def convert_stored_dict_to_a_spreadsheet(self):
    pass

  @property
  def refmonths(self) -> list:
    if self._refmonths is None:
      self._refmonths = self.refmonths_n_cpis_dict.keys()
      self._refmonths = sorted(self._refmonths)
    return self._refmonths

  @property
  def total_cpi_indices(self) -> int:
    return len(self.refmonths_n_cpis_dict.items())

  @property
  def total_cpi_years(self) -> int:
    """
    Gets total CPI years (an integer) in the database
    """
    return len(self.years)

  @property
  def years(self) -> list:
    """
    Gets all CPI years (a list) in the database
    """
    refmonths = self.refmonths_n_cpis_dict.keys()
    years = map(lambda d: d.year, refmonths)
    years = list(set(years))
    return years

  @property
  def first_cpi_year_in_db(self) -> int:
    """
    Gets first CPI year in the database
    """
    return min(self.years)

  @property
  def last_cpi_year_in_db(self) -> int:
    """
    Gets last CPI year in the database
    """
    return max(self.years)

  @property
  def first_cpi_refmonth_in_db(self) -> datetime.date:
    """
    Gets first CPI refmonth in the database
    """
    refmonths = self.refmonths_n_cpis_dict.keys()
    return min(refmonths)

  @property
  def last_cpi_refmonth_in_db(self) -> datetime.date:
    """
    Gets last CPI refmonth in the database
    """
    refmonths = self.refmonths_n_cpis_dict.keys()
    return max(refmonths)

  @property
  def first_refm_n_cpi_in_db(self) -> tuple[datetime.date, float]:
    """
    Gets tuple (first_refmonth, first_acc_index)
    """
    first_cpi_datum = self.refmonths_n_cpis_dict[self.first_cpi_refmonth_in_db]
    first_acc_index = first_cpi_datum.acc_index
    first_refmonth = first_cpi_datum.refmonthdate
    _first_refm_n_cpi_in_db = (first_refmonth, first_acc_index)
    return _first_refm_n_cpi_in_db

  @property
  def last_refm_n_cpi_in_db(self) -> tuple[datetime.date, float]:
    """
    Gets tuple (last_refmonth, last_acc_index)
    """
    last_cpi_datum = self.refmonths_n_cpis_dict[self.last_cpi_refmonth_in_db]
    last_acc_index = last_cpi_datum.acc_index
    last_refmonth = last_cpi_datum.refmonthdate
    _last_refm_n_cpi_in_db = (last_refmonth, last_acc_index)
    return _last_refm_n_cpi_in_db

  def print_cpis(self):
    """
    For cpi_us display, the 2-D dict is sorted (to a tmp-dict) on the "two dimensions" each at a time
    """
    count = 0
    # cpis_dict = sorted(self.refmonths_n_cpis_dict)
    for refmonthdate in self.refmonths:
      count += 1
      scrmsg = f"{count} seriesid {self.seriesid} | refmonthdate {refmonthdate}"
      print(scrmsg)
      cpidatum = self.refmonths_n_cpis_dict[refmonthdate]
      print(cpidatum)

  def __str__(self):
    outstr = f"""
    nº of years = {self.total_cpi_indices}
    nº of years = {self.total_cpi_years}
    start year =  {self.first_cpi_year_in_db}
    end year =  {self.last_cpi_year_in_db}
    first cpi/refmonth in db = {self.first_refm_n_cpi_in_db}
    last cpi/refmonth in db = {self.last_refm_n_cpi_in_db}
    """
    return outstr


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
  fn = '2024 CUUR0000SA0 prettyprint.txt'
  match = cmpld_prettyprint_file_pattern.search(fn)
  res = None if match is None else match.group(1)
  scrmsg = f"from [{fn}] match => [{res}]"
  print(scrmsg)


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
