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
import os
import json
import re

import settings as sett


class JsonRequestStatusesReader:

  prettyprint_filename_tointerpol = r"{year} CUUR0000SA0 prettyprint.json"
  prettyprint_filename_repattern = r"^(\d{4}) CUUR0000SA0 prettyprint.json"
  prettyprint_filename_recmpld = re.compile(prettyprint_filename_repattern)
  REQUEST_SUCCEEDED = 'REQUEST_SUCCEEDED'

  def __init__(self):
    self.n_file = 0
    # self.process()

  @property
  def bls_datafolderpath(self):
    folderpath = sett.get_datafolder_abspath()
    foldername = 'bls_cpi_data'
    bls_folderpath = os.path.join(folderpath, foldername)
    return bls_folderpath

  def get_jsonfilename_for_year(self, year):
    """
    Example
    2011 CUUR0000SA0 prettyprint.json
    """
    json_fn_for_year = self.prettyprint_filename_tointerpol.format(year=year)
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
    statuscode = self.extract_statuscode_from_json_by_year(year)
    if statuscode is not None:
      self.n_file += 1
      scrmsg = f"{self.n_file} | {year} => statuscode {statuscode}"
      print(scrmsg)
    else:
      scrmsg = f"{year} => do not have a statuscode"
      print(scrmsg)
      fipath = self.get_jsonfilepath_on_year(year)
      bool_exists = os.path.isfile(fipath)
      scrmsg = f"\texists = {bool_exists} | file = [{fipath}]"
      print(scrmsg)

  def get_all_years_in_bls_datafolder(self):
    filenames = os.listdir(self.bls_datafolderpath)
    years = []
    for fn in filenames:
      match = self.prettyprint_filename_recmpld.search(fn)
      year = None if match is None else match.group(1)
      try:
        if year:
          years.append(int(year))
      except ValueError:
        continue
    years.sort()
    return years

  def verify_statuscode_in_bls_datafolder(self):
    years = self.get_all_years_in_bls_datafolder()
    scrmsg = f"""verify_statuscode_in_bls_datafolder()
    Number of year-data-files in datafolder: {len(years)}"""
    print(scrmsg)
    for year in years:
      self.show_statuscode_from_json_by_year(year)

  def process(self):
    self.verify_statuscode_in_bls_datafolder()


if __name__ == '__main__':
  """
  adhoctest()
  adhoctest2()
  """
  statex = JsonRequestStatusesReader()
  statex.process()

