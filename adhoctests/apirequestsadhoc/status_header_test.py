#!/usr/bin/env python3
"""
adhoctests/apirequestsadhoc/status_header_test.py

Known statuses from BLS version 1 API:
  REQUEST_SUCCEEDED
  REQUEST_NOT_PROCESSED

---------------------
The script cpi_apifetcher_to_prettyprint_cls.py
  in commands/fetch/cpi
  may process various year with the help of bash's for-loop,
    as in the example below:
---------------------
Fetching CPI for various years:
  for i in {2010..2018}; do commands/fetch/cpi/cpi_apifetcher_to_prettyprint_cls.py --year $i; done

"""
import os
import json
import settings as sett


class JsonStatusesAdhocTest:

  prettyprint_filename_tointerpol = "{year} CUUR0000SA0 prettyprint.json"

  def __init__(self):
    self.process()
    # self.year = year

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

  def show_status_code(self, year):
    pdict = self.get_dict_fr_jsonfile_on_year(year)
    try:
      status = pdict['status']
      scrmsg = f"{year} => status {status}"
      print(scrmsg)
    except KeyError:
      scrmsg = f"{year} => do not have a status code"
      print(scrmsg)
      fipath = self.get_jsonfilepath_on_year(year)
      bool_exists = os.path.isfile(fipath)
      scrmsg = f"\texists = {bool_exists} | file = [{fipath}]"
      print(scrmsg)

  def process(self):
    for year in range(2005, 2026):
      self.show_status_code(year)


if __name__ == '__main__':
  """
  adhoctest()
  adhoctest2()
  """
  JsonStatusesAdhocTest()
