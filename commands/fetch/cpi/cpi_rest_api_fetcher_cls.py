#!/usr/bin/env python3
"""
commands/fetch/cpi/cpi_rest_api_fetcher_cls.py
  contains class Fetcher which is a client of the functions in
    commands/fetch/cpi/cpi_rest_api_fetcher_cls.py

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

Based on:
  www.bls.gov/developers/api_python.html
  Example:
    https://data.bls.gov/timeseries/CUUR0000SA0
      shows a year-month table with the CPI_US indices
"""
import datetime
import json
import os
import sys
# import commands.fetch.cpi.bls_cpi_api_fetcher_fs as ftchfs
import commands.fetch.cpi.cpi_rest_api_fetcher_fs as ftchfs
import fs.os.sufix_incrementor as osfs
import settings as sett
BLS_URL = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
DEFAULT_HTTP_HEADERS = {'Content-type': 'application/json'}
DICTKEY_SERIESID_K = 'seriesID'


import json


def is_valid_json(json_string):
    """
    Checks if a given string is a valid JSON format.
    """
    try:
        json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False


class Fetcher:

  datafileform = "{year} {seriesid} prettyprint.txt"

  def __init__(self, seriesid=None, year=None, datafolder=None):
    self.seriesid = seriesid
    self.year = year
    self.today = datetime.date.today()
    self.datafolder = datafolder
    self.treat_attrs()
    self._datafilename = None
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
    if self.datafolder is None or not os.path.isdir(self.datafolder):
      self.datafolder = sett.get_datafolder_abspath()
      if not os.path.isdir(self.datafolder):
        errmsg = f"datafolder {self.datafolder} does not exist. Please, verify input or configfile."
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
  def datafilename(self):
    if self._datafilename is None:
      self.datafileform.format(year=self.year)
      if self._datafilename is None:
        errmsg = f"Error: datafilename could not be found or formed."
        raise OSError(errmsg)
    return self._datafilename

  @property
  def seriesid_in_a_list(self):
    """
    within_quotes = f'{self.seriesid}'
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

  def fetch_json_response_w_restapi_reqjsondata(self):
    # self.response_json = ftchfs.fetch_json_response_w_restapi_reqjsondata(self.payload_json)
    self.response_json = json.dumps('{"Results":{"series":[{"seriesID":"CUUR0000SA0","data":[{"year":"2024","period":"M12","periodName":"December","value":"315.605","footnotes":[{}]},{"year":"2024","period":"M11","periodName":"November","value":"315.493","footnotes":[{}]},{"year":"2024","period":"M10","periodName":"October","value":"315.664","footnotes":[{}]},{"year":"2024","period":"M09","periodName":"September","value":"315.301","footnotes":[{}]},{"year":"2024","period":"M08","periodName":"August","value":"314.796","footnotes":[{}]},{"year":"2024","period":"M07","periodName":"July","value":"314.540","footnotes":[{}]},{"year":"2024","period":"M06","periodName":"June","value":"314.175","footnotes":[{}]},{"year":"2024","period":"M05","periodName":"May","value":"314.069","footnotes":[{}]},{"year":"2024","period":"M04","periodName":"April","value":"313.548","footnotes":[{}]},{"year":"2024","period":"M03","periodName":"March","value":"312.332","footnotes":[{}]},{"year":"2024","period":"M02","periodName":"February","value":"310.326","footnotes":[{}]},{"year":"2024","period":"M01","periodName":"January","value":"308.417","footnotes":[{}]}]}]}}')
    print('before')
    print('type response_json =', type(self.response_json))
    bool_json_valid = is_valid_json(self.response_json)
    print('bool_json_valid =', bool_json_valid)
    print(self.response_json)
    self.response_json = json.loads(self.response_json)
    if isinstance(self.response_json, dict):
      print('type is json')
      print('type =', type(self.response_json))
    else:
      print('type is NOT json')
      print('type =', type(self.response_json))
    # sys.exit(0)

  def save_series_pprint_as_file(self):
    json_as_dict = json.loads(self.response_json)
    print('type var json_as_dict =', type(json_as_dict))
    # sys.exit(0)
    prettyprint_str = ftchfs.convert_json_response_to_pretyprint(json_as_dict)
    self.pprint_saved_filepath = ftchfs.save_series_pprint_as_file(
      pprint_filename=self.datafilename,
      pprint_dump=prettyprint_str,
      folderpath=self.datafolder,
    )
    print('Saved prettyprint to', self.pprint_saved_filepath)

  def process(self):
    print(self.payload_dict)
    # return
    print('Step 1 - fetching')
    self.fetch_json_response_w_restapi_reqjsondata()
    print('Step 2 - saving to prettyprint file')
    self.save_series_pprint_as_file()

  def __str__(self):
    outstr = f"""
    seriesid = {self.seriesid}
    year = {self.year}
    json responde =>
    {self.response_json}
    """
    return outstr


def adhoctest():
  filename = 'SUUR0000SA0-015.dat'
  filepath = sett.get_datafile_abspath_in_app(filename)
  print('filepath', filepath)
  newfilepath = osfs.get_filepath_if_available_or_increment_numbersufix(filepath)
  print('newfilepath', newfilepath)


def process():
  seriesid = 'CUUR0000SA0'
  fetcher = Fetcher(seriesid, 2024)
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
  """
  adhoctest2()
  process()
