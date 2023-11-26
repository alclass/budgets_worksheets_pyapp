#!/usr/bin/env python3
"""
commands/fetch/bls_cpi_api_fetcher.py
  fetches BLS CPI (Consumer Price Index) monthly index data for the known series available
    ie ['CUUR0000SA0', 'SUUR0000SA0']

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
import copy
import datetime
import time
import settings as cfg
import requests
import json
import prettytable
BLS_URL = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
m_headers = {'Content-type': 'application/json'}
DICTKEY_SERIESID_K = 'seriesID'


def save_series_pprint_as_file(pprint_filename, pprint_dump):
  pprint_outfile = cfg.get_datafile_abspath_in_app(pprint_filename)
  output = open(pprint_outfile, 'w')
  print('Closing output file for series', pprint_filename)
  print(pprint_outfile)
  output.write(pprint_dump.get_string())
  output.close()


class CPIFetcher:

  DEFAULT_JSON_OUTFILENAME = 'bls_cpi.json'
  cpi_api_modeldatadict = {
    'seriesid': ['CUUR0000SA0', 'SUUR0000SA0'],
    'startyear': '2021',
    'endyear': '2024'
  }

  def __init__(self, uptoyear=None):
    self.response_json_data = None
    self.series_files_save = []
    self.runduration = None
    self.today = datetime.date.today()
    self.year = uptoyear
    self.treat_year()
    self.api_datadict = copy.copy(self.cpi_api_modeldatadict)
    self.api_datadict['endyear'] = str(self.year)

  def treat_year(self):
    if self.year is None:
      self.year = self.today.year
      return
    # if year is not int-liked-typed a ValueError exception will be raised
    self.year = int(self.year)

  @property
  def json_outfile(self):
    _json_outfile = cfg.get_datafile_abspath_in_app(self.DEFAULT_JSON_OUTFILENAME)
    return _json_outfile

  @staticmethod
  def get_pprint_dump_filename(seriesid):
    return seriesid + '.dat'

  def dump_n_save_res_per_series(self):
    for series in self.response_json_data['Results']['series']:
      pprint_dump = prettytable.PrettyTable(
        [DICTKEY_SERIESID_K, 'year', 'period', 'value', 'footnotes']
      )
      seriesid = series[DICTKEY_SERIESID_K]
      pprint_dump_filename = self.get_pprint_dump_filename(seriesid)
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
      self.series_files_save.append(pprint_dump_filename)
      save_series_pprint_as_file(pprint_dump_filename, pprint_dump)

  def write_json_api_request_as_file(self):
    print('Writing json file [', self.DEFAULT_JSON_OUTFILENAME, "] inside app's data folder")
    print(self.json_outfile)
    with open(self.json_outfile, 'w') as f:
      json.dump(self.response_json_data, f)

  def cpi_remote_api_fetch(self, request_json_data, p_headers):
    p = requests.post(BLS_URL, data=request_json_data, headers=p_headers)
    self.response_json_data = json.loads(p.text)
    self.write_json_api_request_as_file()
    self.dump_n_save_res_per_series()

  def fetch_cpis_upto_currentyear(self):
    json_cpi_api_m_data = json.dumps(self.api_datadict)
    self.cpi_remote_api_fetch(json_cpi_api_m_data, m_headers)

  def process(self):
    start = time.time()
    self.fetch_cpis_upto_currentyear()
    end = time.time()
    self.runduration = end - start

  def __str__(self):
    outstr = f"""CPIFetcher:
    today = {self.today}
    run duration = {self.runduration}
    uptoyear = {self.year}
    json_outfilename = {self.DEFAULT_JSON_OUTFILENAME}
    json_outfile = {self.json_outfile}
    {self.series_files_save}
    """
    return outstr


def process():
  cpifetcher = CPIFetcher()
  cpifetcher.process()
  print('Stats', cpifetcher)


if __name__ == '__main__':
  process()
