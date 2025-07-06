#!/usr/bin/env python3
"""
commands/fetch/bls_us/cpi_apifetcher_to_prettyprint_cls.py
  contains class Fetcher which is a client of the functions in cpi_apifetcher_to_prettyprint_fs.py

Acronyms:
  BLS => Burreau of Labor Statistics (USA's)
  CPI => Consumer Price Index (US-measured)

This class fetches BLS indices using the API's version 1 3rd option
This is chosen because:
  1 - version 2 needs authentication, version 1 is open
  2 - options 1 & 2 downloads the whole time period
        option 1 downloads a seriesid
        option 2 downloads a list of seriesid's
  3 - option 3, chosen, offers fetching by year


(*) At the of writting, the two known series are: ['CUUR0000SA0', 'SUUR0000SA0']
  More seriesid will later on be added and probably moved to a configfile

Running for fetching "many" year from bash-CLI:
===============================================
The script cpi_apifetcher_to_prettyprint_cls.py
  in commands/fetch/cpi_us
  may process various year with the help of bash's for-loop,
    as in the example below:
---------------------
Fetching CPI for various years:
  for i in {2010..2018}; do commands/fetch/bls_us/cpi_apifetcher_to_prettyprint_cls.py --year $i; done
---------------------

Based on:
  www.bls.gov/developers/api_python.html
  Example:
    https://data.bls.gov/timeseries/CUUR0000SA0
      shows a year-month table with the CPI_US indices
"""
# from tkinter.messagebox import RETRY
# import commands.fetch.cpi_us.bls_cpi_api_fetcher_fs as ftchfs
import argparse
import datetime
import json
import os
# import sys
import commands.fetch.bls_us.cpi_rest_api_fetcher_fs as ftchfs
import fs.indices.bls_us.jsonfile_reqstatus_extractor_cls as statusex
import fs.os.sufix_incrementor as osfs
import settings as sett
BLS_URL = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
DEFAULT_HTTP_HEADERS = {'Content-type': 'application/json'}
DICTKEY_SERIESID_K = 'seriesID'
# Parse command-line arguments
parser = argparse.ArgumentParser(description="Download BLS CPI indices.")
parser.add_argument("--datadir", type=str, default="datadir/",
                    help="Data Directory")
parser.add_argument("--seriesid", type=str, default="CUUR0000SA0",
                    help="Series Id")
parser.add_argument("--year", type=int, default=datetime.date.today().year,
                    help="Series Id")
args = parser.parse_args()


def is_valid_json(json_to_test):
    """
    Checks if a given string is a valid JSON format.
    """
    if isinstance(json_to_test, dict):
      # it's already a dict, so json is valid
      # (an iteratable json is in fact a dict)
      return True
    if type(json_to_test) not in [str, bytes, bytearray]:
      # to go ahead for method loads() it must be either str, bytes or bytearray
      return False
    try:
        json.loads(json_to_test)
        # at this point, json-encoding happened
        return True
    except json.JSONDecodeError:
        return False


class Fetcher:

  DEFAULT_BLS_CPI_FOLDERNAME = 'bls_cpi_data'
  default_prettyprint_fn_to_interpol = "{year} {seriesid} prettyprint.txt"

  def __init__(self, seriesid=None, year=None, root_datafolder=None):
    self.seriesid = seriesid
    self.year = year
    self.today = datetime.date.today()
    self.root_datafolder = root_datafolder
    self.treat_attrs()
    self.bool_json_w_request_succeeded_for_year = False
    self.bool_prettyprintfile_is_already_present_in_folder = False  # to prove otherwise
    self.bool_jsonfile_is_already_present_in_folder = False
    self._prettyprintfilename = None
    self.response_json = None
    self.pprint_saved_filepath = None

  def treat_attrs(self):
    try:
      self.year = int(self.year)
      # adjust 'year' if in the future
      if self.year > self.today.year:
        self.year = self.today.year
    except ValueError:
      self.year = self.today.year
    if self.root_datafolder is None or not os.path.isdir(self.root_datafolder):
      self.root_datafolder = sett.get_datafolder_abspath()
      if not os.path.isdir(self.root_datafolder):
        errmsg = f"datafolder {self.root_datafolder} does not exist. Please, verify input or configfile."
        raise OSError(errmsg)

  @property
  def year_fr(self):
    """
      year from or start year
      notice that in this class year_fr or year_to is 'year'
      this named attribute is add to help fill in the API payload
    """
    return self.year

  @property
  def year_to(self):
    """
      year from or start year
      notice that in this class year_fr or year_to is 'year'
      this named attribute is add to help fill in the API payload
    """
    return self.year

  @property
  def bls_cpi_datafolder(self):
    _bls_cpi_datafolder = os.path.join(self.root_datafolder, self.DEFAULT_BLS_CPI_FOLDERNAME)
    if not os.path.isdir(_bls_cpi_datafolder):
      os.makedirs(_bls_cpi_datafolder, exist_ok=True)
    return _bls_cpi_datafolder

  @property
  def prettyprintfilename(self):
    if self._prettyprintfilename is None:
      self._prettyprintfilename = self.default_prettyprint_fn_to_interpol.format(seriesid=self.seriesid, year=self.year)
      if self._prettyprintfilename is None:
        errmsg = f"Error: datafilename could not be found or formed."
        raise OSError(errmsg)
    return self._prettyprintfilename

  @property
  def json_filename(self):
    name, dot_ext = os.path.splitext(self.prettyprintfilename)
    json_dot_ext = '.json'
    json_filename = f"{name}{json_dot_ext}"
    return json_filename

  @property
  def json_filepath(self):
    return os.path.join(self.bls_cpi_datafolder, self.json_filename)

  @property
  def prettyprintfilepath(self):
    return os.path.join(self.bls_cpi_datafolder, self.prettyprintfilename)

  @property
  def seriesid_in_a_list(self):
    """
    The enclosing here is just within square brackets [] (i.e., put an element inside a list)
    The "within quotes" part is done by json.loads() later on
    This is to comply with the API's wellformedness rule
      (@see the specific docstr or take a look at an example json file already downloaded to the data folder)
    """
    _seriesid_in_a_list = [self.seriesid]
    return _seriesid_in_a_list

  @property
  def payload_dict(self):
    """
    The JSON Payload is filled as:
      {
        "seriesid":["Series1",..., "SeriesN"],
        "startyear":"yearX",
        "endyear":"yearY"
       }
    """
    v1_payload_dict = {
      'seriesid': self.seriesid_in_a_list,
      'startyear': f'{self.year_fr}',
      'endyear': f'{self.year_to}',
    }
    return v1_payload_dict

  @property
  def payload_json(self):
    return json.dumps(self.payload_dict)

  def save_json_response(self):
    if os.path.isfile(self.json_filepath):
      scrmsg = f"""json file [{self.json_filename}] already exists in [{self.bls_cpi_datafolder}]
      => Overwrite it? [Y/y, n] [ENTER] means Yes """
      ans = input(scrmsg)
      if ans.lower not in ['y', 'n', '']:
        return
    json_str = self.response_json
    if type(json_str) not in [str, bytes, bytearray]:
      # from dict to str (loads returns a str which is text-file-writeable!)
      scrmsg = f"Converting json type {type(json_str)} to {[str, bytes, bytearray]}"
      print(scrmsg)
      json_str = json.dumps(json_str)
    fd = open(self.json_filepath, 'w')
    fd.write(json_str)
    scrmsg = f"Save json file [{self.json_filename}]."
    print(scrmsg)
    fd.close()

  def fetch_json_response_w_restapi_reqjsondata(self):
    self.response_json = ftchfs.fetch_json_response_w_restapi_reqjsondata(self.payload_json)
    bool_json_valid = is_valid_json(self.response_json)
    print('bool_json_valid =', bool_json_valid)
    print('type response_json =', type(self.response_json))
    self.save_json_response()

  def save_series_pprint_as_file(self):
    """
    # self.response_json = json.loads(self.response_json)
    if isinstance(self.response_json, dict):
      print('type is json')
      print('type =', type(self.response_json))
    else:
      print('type is NOT json. Halting for it will crash the for-loop ahead.')
      print('type =', type(self.response_json))
    """
    try:
      json_as_dict = json.loads(self.response_json)
    except TypeError:
      # if caught, response_json is probably already a dict
      json_as_dict = self.response_json
    print('save_series_pprint_as_file | type var json_as_dict =', type(json_as_dict))
    # sys.exit(0)
    prettyprint_str = ftchfs.convert_json_response_to_pretyprint(json_as_dict)
    self.pprint_saved_filepath = ftchfs.save_series_pprint_as_file(
      pprint_filename=self.prettyprintfilename,
      pprint_dump=prettyprint_str,
      folderpath=self.bls_cpi_datafolder,
    )
    print('Saved prettyprint to', self.pprint_saved_filepath)

  def verify_if_jsonfile_is_already_present_in_folder(self):
    self.bool_jsonfile_is_already_present_in_folder = False
    scrmsg = f" Exists {self.json_filepath} ?"
    print(scrmsg)
    if os.path.isfile(self.json_filepath):
      self.bool_jsonfile_is_already_present_in_folder = True

  def is_there_a_json_w_request_succeeded_for_year(self):
    self.bool_json_w_request_succeeded_for_year = False
    stat = statusex.JsonRequestStatusesReader()
    if stat.has_request_succeeded(self.json_filename):
      scrmsg = f"request_succeeded {self.json_filename}"
      print(scrmsg)
      self.bool_json_w_request_succeeded_for_year = True
      return

  def verify_if_prettyprintfile_is_already_present_in_folder(self):
    self.bool_prettyprintfile_is_already_present_in_folder = False
    if os.path.isfile(self.prettyprintfilepath):
      self.bool_prettyprintfile_is_already_present_in_folder = True

  def read_json_from_json_stored_file(self):
    text = open(self.json_filepath).read()
    self.response_json = json.loads(text)

  def process_old(self):
    n_step = 1
    action_str = 'verify if refmonth data file has already been download, if so, nothing to do'
    scrmsg = f'Step {n_step} - {action_str}.'
    print(scrmsg)
    self.verify_if_prettyprintfile_is_already_present_in_folder()
    if self.bool_prettyprintfile_is_already_present_in_folder:
      scrmsg = f"""File [{self.prettyprintfilename}] is already present in data folder.
       BLS CPI datafolder is [{self.bls_cpi_datafolder}] 
       * If a refresh (redownload) is wanted, please delete above mentioned file and retry."""
      print(scrmsg)
      return
    n_step += 1
    action_str = 'verify if jsonfile is already present in folder'
    scrmsg = f'Step {n_step} - {action_str}.'
    print(scrmsg)
    self.verify_if_jsonfile_is_already_present_in_folder()
    if self.bool_jsonfile_is_already_present_in_folder:
      print(scrmsg)
      n_step += 1
      action_str = 'json stored file exists, read it.'
      scrmsg = f'Step {n_step} - {action_str}.'
      print(scrmsg)
      self.read_json_from_json_stored_file()

  def process(self):
    """
    For an API fetch to happen, the system checks whether its json response been downloaded
      and contains the REQUEST_SUCCEEDED statuscode at the beginning
    If there isn't this, a download will be tried
    """
    print(self.payload_dict)
    n_step = 1
    action_str = "check if the year's json file exists and has the request succeeded status code."
    scrmsg = f'Step {n_step} - {action_str}'
    print(scrmsg)
    self.is_there_a_json_w_request_succeeded_for_year()
    bool_succeeded = self.bool_json_w_request_succeeded_for_year
    if bool_succeeded:
      scrmsg = f""" => answer -> json request succeeded for year {self.year}: {bool_succeeded}
      no need to (re)download it. 
      If its prettyprint is missing, regenerate it with generate_cpi_prettyprint_from_json.py"""
      print(scrmsg)
      return
    n_step += 1
    action_str = 'fetch CPI data from the BLS API'
    scrmsg = f'Step {n_step} - {action_str}.'
    print(scrmsg)
    self.fetch_json_response_w_restapi_reqjsondata()
    n_step += 1
    action_str = 'save fetched json or json-read to its prettyprint datafile'
    scrmsg = f'Step {n_step} - {action_str}.'
    print(scrmsg)
    # has to check request status code again
    n_step += 1
    self.is_there_a_json_w_request_succeeded_for_year()
    if self.bool_json_w_request_succeeded_for_year:
      scrmsg = f" => Step {n_step} -> json request succeeded for year {self.bool_json_w_request_succeeded_for_year}"
      print(scrmsg)
      n_step += 1
      self.save_series_pprint_as_file()

  def __str__(self):
    outstr = f"""BLS CPI API-Fetcher: 
    seriesid = {self.seriesid}
    year = {self.year}
    datafolder = [{self.bls_cpi_datafolder}]
    json_filename = [{self.json_filename}]
    prettyprint_filename = [{self.prettyprintfilename}]
    json_w_request_succeeded = {self.bool_json_w_request_succeeded_for_year}
    """
    return outstr


def adhoctest():
  filename = 'SUUR0000SA0-015.dat'
  filepath = sett.get_datafile_abspath_in_app(filename)
  print('filepath', filepath)
  newfilepath = osfs.get_filepath_if_available_or_increment_numbersufix(filepath)
  print('newfilepath', newfilepath)


def get_args():
  seriesid = args.seriesid
  year = args.year
  return seriesid, year


def process():
  seriesid, year = get_args()
  fetcher = Fetcher(seriesid, year)
  fetcher.process()
  print(fetcher)


def adhoctest2():
  txt = '{"seriesID":{"seriesid": ["CUUR0000SA0"], "startyear": "2024", "endyear": "2024"},"data":[]}'
  pdict = eval(txt)
  print(pdict)
  j = json.dumps(txt)
  print(j)
  json_list_string = '[{"id": 1}, {"id": 2}]'
  data_list = json.loads(json_list_string)
  for item in data_list:
    print(item['id'])


if __name__ == '__main__':
  """
  adhoctest()
  adhoctest2()
  """
  process()
