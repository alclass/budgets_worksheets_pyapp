#!/usr/bin/env python3
"""
bls_cpi_api_fetcher.py
Script to fetch BLS CPI (Consumer Price Index) data
Based on:
  www.bls.gov/developers/api_python.html
  webpage:
  https://data.bls.gov/timeseries/CUUR0000SA0
  shows a year-month table with the CPI_US indices
"""
import settings as cfg
import requests
import json
import prettytable
BLS_URL = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
m_headers = {'Content-type': 'application/json'}
DICTKEY_SERIESID_K = 'seriesID'


def write_series_pprint_as_file(pprint_filename, pprint_dump):
  pprint_outfile = cfg.get_datafile_abspath_in_app(pprint_filename)
  output = open(pprint_outfile, 'w')
  print('Closing output file for series', pprint_filename)
  print(pprint_outfile)
  output.write(pprint_dump.get_string())
  output.close()  # ends series looping


def write_json_api_request_as_file(json_data):
  json_outfilename = 'bls_cpi.json'
  json_outfile = cfg.get_datafile_abspath_in_app(json_outfilename)
  print('Writing json file [', json_outfilename, "] inside app's data folder")
  print(json_outfile)
  with open(json_outfile, 'w') as f:
    json.dump(json_data, f)


def fetch(p_data, p_headers):
  p = requests.post(BLS_URL, data=p_data, headers=p_headers)
  json_data = json.loads(p.text)
  write_json_api_request_as_file(json_data)
  for series in json_data['Results']['series']:
    pprint_dump = prettytable.PrettyTable(
      [DICTKEY_SERIESID_K, 'year', 'period', 'value', 'footnotes']
    )
    seriesid = series[DICTKEY_SERIESID_K]
    pprint_dump_filename = seriesid + '.dat'
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
    write_series_pprint_as_file(pprint_dump_filename, pprint_dump)


m_data = json.dumps(
  {
    'seriesid': ['CUUR0000SA0', 'SUUR0000SA0'],
    'startyear': '2021',
    'endyear': '2024'
  }
)


def process():
  fetch(m_data, m_headers)


if __name__ == '__main__':
  process()
