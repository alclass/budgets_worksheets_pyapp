#!/usr/bin/env python3
"""
commands/fetch/bls_cpi_api_fetcher.py
  contains functions for calling the public REST API that returns CPI month by month indices for known series (*)
  contains functions to fetch CPI data from BLS's public REST API

Acronyms:
  BLS => Burreau of Labor Statistics (USA's)
  CPI => Consumer Price Index (US-measured)

(*) The known series are: ['CUUR0000SA0', 'SUUR0000SA0']
  They are organized in another script for aggregating/mounting the json request data for the remote request
    that happens from here.

The API available here is an open one, ie it's not necessary to authenticate into it.
Another script in this system reads the data files recorded and insert the data into a sqlite db.
In a nutshell, this system (this script and the ones accompanying) fetches API data
  and buffers (or caches) them locally.

Based on:
  www.bls.gov/developers/api_python.html
  Example:
    https://data.bls.gov/timeseries/CUUR0000SA0
      shows a year-month table with the CPI_US indices
"""
import json
import os
import prettytable
import requests
import settings as sett
import fs.os.sufix_incrementor as osfs
BLS_URL = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
DEFAULT_HTTP_HEADERS = {'Content-type': 'application/json'}
DICTKEY_SERIESID_K = 'seriesID'


def form_pprint_dump_filename(seriesid, startyear=None, endyear=None):
  prefix_year_range = ''
  if startyear is not None and endyear is not None:
    prefix_year_range = f"{startyear}-{endyear} "
  pprint_dump_filename = f"{prefix_year_range}{seriesid}.prettyprint.dat"
  return pprint_dump_filename


def dump_n_save_json_response_per_each_series_inside_data(
    response_json_data, folderpath=None, startyear=None, endyear=None
):
  """
    Saves a pretty-print representation of the response json data for each series id available
    ie more than one file may be written
  Returns: pprint_dump_filenames => list with the saved/written filenames
  """
  pprint_dump_filenames = []
  try:
    for series in response_json_data['Results']['series']:
      pprint_dump = prettytable.PrettyTable(
        [DICTKEY_SERIESID_K, 'year', 'period', 'value', 'footnotes']
      )
      seriesid = series[DICTKEY_SERIESID_K]

      for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        footnotes = ''
        for footnote in item['footnotes']:
          if footnote:
            footnotes = footnotes + footnote['text'] + ','
        if 'M01' <= period <= 'M12':
          pprint_dump.add_row(
            [seriesid, year, period, value, footnotes[0:-1]]
          )    # ends items (in each series) looping
      pprint_dump_filename = form_pprint_dump_filename(seriesid, startyear, endyear)
      filepath = save_series_pprint_as_file(pprint_dump_filename, pprint_dump, folderpath)
      if filepath:
        # filename may be the one above or a changed one if it was needed
        # to form a number sufix name due to unavailability of the former
        pprint_dump_filename = os.path.split(filepath)[-1]
        pprint_dump_filenames.append(pprint_dump_filename)
  except (IndexError, TypeError):
    n_files = len(pprint_dump_filenames)
    scrmsg = f"series files saving incomplete: {n_files} saved. Continuing."
    print(scrmsg)
  return pprint_dump_filenames


def fetch_json_response_w_restapi_reqdictdata(rest_api_req_m_dictdata, p_headers=None):
  """
    Envelopes the dictdata into a jsondata and calls the REST API jsondata caller function (@see below)
  """
  rest_api_req_m_jsondata = json.dumps(rest_api_req_m_dictdata)
  return fetch_json_response_w_restapi_reqjsondata(rest_api_req_m_jsondata, p_headers)


def fetch_json_response_w_restapi_reqjsondata(rest_api_req_m_jsondata, p_headers=None):
  """
    Calls the REST API with a request json data parameter

  testdict = {'testkey': 'testvalue'}
  response_json_data = json.dumps(testdict)

  """
  if p_headers is None:
    p_headers = DEFAULT_HTTP_HEADERS
  print('Issuing REST API request to', BLS_URL)
  print('Json REST API Request:', rest_api_req_m_jsondata)
  # the call below may raise requests.exceptions.ConnectionError
  p = requests.post(BLS_URL, data=rest_api_req_m_jsondata, headers=p_headers)
  response_json_data = json.loads(p.text)
  return response_json_data


def save_series_pprint_as_file(pprint_filename, pprint_dump, folderpath=None):
  """
    Saves a "series" pretty-print dump formed in function dump_n_save_json_response_per_each_series_inside_data() above

  The pretty-print is like so:
  +-------------+------+--------+---------+-----------+
  |   seriesID  | year | period |  value  | footnotes |
  +-------------+------+--------+---------+-----------+
  | SUUR0000SA0 | 2020 |  M12   | 146.408 |           |
  | SUUR0000SA0 | 2020 |  M11   | 146.242 |           |
  (...)
  """
  if folderpath is not None and os.path.isdir(folderpath):
    pprint_outfilepath = os.path.join(folderpath, pprint_filename)
  else:
    pprint_outfilepath = sett.get_datafile_abspath_in_app(pprint_filename)
  scrmsg = f'Preparing to write json output file for series [{pprint_filename}]'
  print(scrmsg)
  print('\t path = ', pprint_outfilepath)
  pprint_outfilepath = osfs.get_filepath_if_available_or_increment_numbersufix(pprint_outfilepath)
  if os.path.isfile(pprint_outfilepath):
    error_msg = (f" => File f{pprint_outfilepath} already exists."
                 f" Logical error in get_filepath_if_available_or_increment_numbersufix()")
    raise OSError(error_msg)
  output = open(pprint_outfilepath, 'w')
  output.write(pprint_dump.get_string())
  output.close()
  scrmsg = 'File written.'
  print(scrmsg)
  # filepath may have been changed (the number sufix case)
  return pprint_outfilepath


def write_json_as_file_w_its_path(response_json_data, json_output_filepath):
  """
    Saves a response_json_data as a file
  """
  json_output_filepath = osfs.get_filepath_if_available_or_increment_numbersufix(json_output_filepath)
  json_output_filename = os.path.split(json_output_filepath)
  scrmsg = f"Preparing to write json file [f{json_output_filename}]."
  print(scrmsg)
  print('\tsytem path:', json_output_filepath)
  if os.path.isfile(json_output_filepath):
    error_msg = (f" => File f{json_output_filepath} already exists."
                 f" Logical error in get_filepath_if_available_or_increment_numbersufix()")
    raise OSError(error_msg)
  with open(json_output_filepath, 'w') as fd:
    json.dump(response_json_data, fd)
    scrmsg = 'File written.'
    print(scrmsg)
  # filepath may have been changed (the number sufix case)
  return json_output_filepath


def adhoctest():
  filename = 'SUUR0000SA0-015.dat'
  filepath = sett.get_datafile_abspath_in_app(filename)
  print('filepath', filepath)
  newfilepath = osfs.get_filepath_if_available_or_increment_numbersufix(filepath)
  print('newfilepath', newfilepath)


def process():
  pass


if __name__ == '__main__':
  """
  process()
  """
  adhoctest()
