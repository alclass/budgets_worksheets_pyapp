#!/usr/bin/env python3
"""
fs/indices/bls_us/jsonfile_reqstatus_extractor_cls.py
This module contains class JsonRequestStatusesReader that aims to find the "request status phrase"
  at the beginning (a kind of header) of data json files from BLS (US's Bureau of Labor Statistics)

  Known statuses from BLS version 1 API are:
    REQUEST_SUCCEEDED
    REQUEST_NOT_PROCESSED

---------------------

"""
import argparse
import os
import json
import re
import settings as sett
from commands.fetch.bls_us.read_cpis_from_db_fs import DEFAULT_SERIESID
from commands.fetch.bls_us.read_cpis_from_db_fs import KNOWN_SERIESID
DEFAULT_BLS_DATA_FOLDERNAME = 'bls_cpi_data'
parser = argparse.ArgumentParser(description="Download BLS CPI indices.")
parser.add_argument("--seriesid", type=str, default="CUUR0000SA0",
                    help="Series Id")
args = parser.parse_args()


class JsonRequestStatusesReader:

  prettyprint_filename_tointerpol = r"{year} {seriesid} prettyprint.json"
  prettyprint_filename_repattern = r"^(\d{4}) ([A-Z0-9]+?) prettyprint.json"
  prettyprint_filename_recmpld = re.compile(prettyprint_filename_repattern)
  REQUEST_SUCCEEDED = 'REQUEST_SUCCEEDED'

  def __init__(self, seriesid=None):
    self.n_files = 0
    self.seriesid = seriesid
    self.years = []
    self.treat_attrs()

  def treat_attrs(self):
    if self.seriesid is None:
      self.seriesid = DEFAULT_SERIESID
    if self.seriesid not in KNOWN_SERIESID:
      self.seriesid = DEFAULT_SERIESID

  @property
  def bls_datafolderpath(self):
    folderpath = sett.get_datafolder_abspath()
    bls_folderpath = os.path.join(folderpath, DEFAULT_BLS_DATA_FOLDERNAME)
    return bls_folderpath

  def get_jsonfilename_for_year(self, year):
    """
    Example
      "2011 CUUR0000SA0 prettyprint.json"
    """
    json_fn_for_year = self.prettyprint_filename_tointerpol.format(year=year, seriesid=self.seriesid)
    return json_fn_for_year

  def get_jsonfilepath_on_year(self, year):
    fn = self.get_jsonfilename_for_year(year)
    return os.path.join(self.bls_datafolderpath, fn)

  def get_contents_fr_jsonfile_on_year(self, year):
    fipath = self.get_jsonfilepath_on_year(year)
    if not os.path.isfile(fipath):
      return None
    jsontext = open(fipath).read()
    return jsontext

  def get_dict_fr_jsonfile_on_year(self, year):
    jsontext = self.get_contents_fr_jsonfile_on_year(year)
    if jsontext is None:
      return {}
    pdict = json.loads(jsontext)
    return pdict

  def extract_statuscode_from_json_by_year(self, year):
    pdict = self.get_dict_fr_jsonfile_on_year(year)
    try:
      status = pdict['status']
      return status
    except KeyError:
      return None

  def has_request_succeeded(self, filename):
    match = self.prettyprint_filename_recmpld.search(filename)
    year = None if match is None else match.group(1)
    if year is None:
      return False
    year = int(year)
    reqstatus = self.extract_statuscode_from_json_by_year(year)
    if reqstatus == self.REQUEST_SUCCEEDED:
      return True
    return False

  def show_statuscode_from_json_by_year(self, year):
    statuscode = self.extract_statuscode_from_json_by_year(year)\
      if year in self.years else f'data for year {year} is missing'
    if statuscode is not None:
      self.n_files += 1
      scrmsg = f"{self.n_files} | {year} => statuscode {statuscode}"
      print(scrmsg)
    else:
      scrmsg = f"{year} => do not have a statuscode"
      print(scrmsg)
      fipath = self.get_jsonfilepath_on_year(year)
      bool_exists = os.path.isfile(fipath)
      scrmsg = f"\texists = {bool_exists} | file = [{fipath}]"
      print(scrmsg)

  def get_all_years_for_the_seriesid_in_datafolder(self) -> list:
    filenames = os.listdir(self.bls_datafolderpath)
    self.years = []
    for fn in filenames:
      match = self.prettyprint_filename_recmpld.search(fn)
      year = None if match is None else match.group(1)
      seriesid = None if match is None else match.group(2)
      if seriesid is None or seriesid != self.seriesid:
        continue
      try:
        int_year = int(year)
        self.years.append(int_year)
      except ValueError:
        continue
    self.years.sort()
    return self.years

  def verify_statuscode_in_bls_datafolder(self):
    _ = self.get_all_years_for_the_seriesid_in_datafolder()
    scrmsg = f"""verify_statuscode_in_bls_datafolder()
    Number of year-data-files in datafolder: {len(self.years)}"""
    print(scrmsg)
    if len(self.years) == 0:
      scrmsg = f'Database for seriesid {self.seriesid} is empty (nº of years = {len(self.years)}). Returning'
      print(scrmsg)
      return
    try:
      minyear = min(self.years)
      maxyear = max(self.years)
      for year in range(minyear, maxyear+1):
        self.show_statuscode_from_json_by_year(year)
    except ValueError:
      scrmsg = 'Database may be empty.'
      print(scrmsg)

  def process(self):
    self.verify_statuscode_in_bls_datafolder()


def process():
  """
  Known seriesid are CUUR0000SA0 & SUUR0000SA0
    (but there are others)
  """
  statex = JsonRequestStatusesReader(args.seriesid)
  statex.process()


if __name__ == '__main__':
  """
  adhoctest()
  adhoctest2()
  """
  process()
