#!/usr/bin/env python3
"""
commands/fetch/bls_cpis_from_file_to_db.py
  Script to fetch BLS CPI (Consumer Price Index) data

Based on:
  www.bls.gov/developers/api_python.html
"""
import datetime
from dateutil.relativedelta import relativedelta
import settings as cfg
import requests
import json
import prettytable
import fs.datefs.datefunctions as dtfs
BLS_URL = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
m_headers = {'Content-type': 'application/json'}
DICTKEY_SERIESID_K = 'seriesID'


def get_cpi_baselineindex_for_refmonth_m2(refmonthdate):
  """
  This function must be ENCAPSULATED in package-module fin
  The input pdate is transformed to an M-2 date ie month minus 2
  """
  refmonthdate = dtfs.make_refmonthdate_or_none(refmonthdate)
  if isinstance(refmonthdate, datetime.date):
    # make M-2 (adjust day=1 already happens above with make_refmonthdate_or_none())
    refmonthdate = refmonthdate + relativedelta(months=-2)
    return get_cpi_baselineindex_for_refmonth(refmonthdate)
  return None


def get_cpi_baselineindex_for_refmonth(refmonthdate):
  refmonthdate = dtfs.make_refmonthdate_or_none(refmonthdate)
  if not isinstance(refmonthdate, datetime.date):
    return None
  conn = cfg.get_connection()
  cursor = conn.cursor()
  seriesid = 'CUUR0000SA0'
  tuplevalues = (seriesid, refmonthdate)
  sql = """
    SELECT baselineindex FROM cpi_indices
      WHERE
        seriesid = ? and refmonthdate = ?;
  """
  cursor.execute(sql, tuplevalues)
  try:
    baselineindex = cursor.fetchone()[0]
  except TypeError:
    baselineindex = None
  # print('first_baselineindex', first_baselineindex)
  conn.close()
  # None may be returned
  return baselineindex


def get_last_available_cpi_baselineindex():
  """
  It searches for index by the most recent refmonthdate
  returns both the index and the most recent refmonthdate
  """
  conn = cfg.get_connection()
  cursor = conn.cursor()
  seriesid = 'CUUR0000SA0'
  sql = """
    SELECT baselineindex, refmonthdate FROM cpi_indices
      WHERE
        seriesid = ? 
      ORDER BY
        refmonthdate DESC
      LIMIT 1;
  """
  cursor.execute(sql, (seriesid,))
  retval = cursor.fetchone()
  baselineindex = retval[0]
  mostrecent_refmonthdate = retval[1]
  conn.close()
  return baselineindex, mostrecent_refmonthdate


def db_schema():
  sql = '''
  create table econ_indices (
    id int
    idxcode string
    refdate
    baselineindex
  )
  '''
  _ = sql


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


def api_remote_fetch(p_data, p_headers):
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


def adhoctest_api_fetch():
  m_data = json.dumps(
    {
      'seriesid': ['CUUR0000SA0', 'SUUR0000SA0'],
      'startyear': '2021',
      'endyear': '2023'
    }
  )
  api_remote_fetch(m_data, m_headers)


def adhoctest():
  adhoctest_api_fetch()


def process():
  pass


if __name__ == '__main__':
  """
  process()
  
  """
  adhoctest()
