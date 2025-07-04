#!/usr/bin/env python3
"""
commands/fetch/bls_cpi_api_fetcher_fs.py
  fetches BLS CPI (Consumer Price Index) monthly index data
    for the known series available
    i.e., ['CUUR0000SA0', 'SUUR0000SA0']

This script uses version 1 of the public API:
https://www.bls.gov/developers/api_signature.htm#years

HTTP Type: 	POST
URL: 	https://api.bls.gov/publicAPI/v1/timeseries/data/

The JSON Payload is filled as:
  {"seriesid":["Series1",..., "SeriesN"],
   "startyear":"yearX",
   "endyear":"yearY"
}


"""
import copy
import datetime
import os.path
import time
import settings as cfg
import commands.fetch.bls_us.cpi_rest_api_fetcher_fs as ftchfs  # .fetch_json_response_w_restapi_reqdictdata


class USBLS_API_SeriesDataFetcher:
  """
  This class uses the API option for multiple series,
    but with only one (if more are needed, the client user
    should call one by one each time)
  """

  year_fr = 2020
  year_to = 2023
  default_seriesidlist = ['CUUR0000SA0', 'SUUR0000SA0']
  datafileform = "{year} {seriesid} prettyprint.txt"

  def __init__(self, year_fr=None, year_to=None, seriesid=None):
    self.year_fr = year_fr
    self.year_to = year_to
    self.today = datetime.date.today()
    self.treat_years()
    self.seriesid = seriesid  # conditional TO-DO: improve this attribute when new info about it is found
    self._restapi_reqdatadict = None

  def treat_years(self):
    if self.year_to is None:
      self.year_to = self.today.year
    # if year is not int-liked-typed a ValueError exception will be raised
    self.year_to = int(self.year_to)
    if self.year_fr is None:
      # (formerly) self.from_year = dtfs.get_decade_year_tenmultiplebased_from_or_current()
      # if from_year is missing, probable cenario is to search for a newly added monthly index
      self.year_fr = self.year_to
    self.year_fr = int(self.year_fr)
    if self.year_to > self.today.year:
      self.year_to = self.today.year
    if self.year_fr > self.year_to:
      error_msg = (f"Error: from-year {self.year_fr} is greater than to-year {self.year_to}"
                   f" or currentyear {self.today.year} in class CPIFetcher.")
      raise ValueError(error_msg)

  @property
  def payload_as_json(self):
    """
    The JSON Payload is filled as:
      {
        "seriesid":["Series1",..., "SeriesN"],
         "startyear":"yearX",
         "endyear":"yearY"
      }
    """

  @property
  def seriesid_in_a_list(self):
    return [self.seriesid]

  @property
  def payload_as_dict(self):
    cpi_restapi_datadict_payload = {
      'seriesid': self.default_seriesidlist,
      'startyear': str(self.year_fr),
      'endyear': str(self.year_to)
    }
    return cpi_restapi_datadict_payload

  @property
  def restapi_reqdatadict(self):
    if self._restapi_reqdatadict is not None:
      return self._restapi_reqdatadict
    self._restapi_reqdatadict = copy.copy(self.cpi_restapi_datadict_modelparam)
    self._restapi_reqdatadict['startyear'] = str(self.year_fr)
    self._restapi_reqdatadict['endyear'] = str(self.year_to)
    # there is already a default seriesid list in the restapi_reqdatadict
    # only change it if it's been given from __init__()
    if self.seriesidlist is not None:
      self.seriesidlist = list(self.seriesidlist)
      self._restapi_reqdatadict['seriesid'] = self.seriesidlist
    return self._restapi_reqdatadict

  def __str__(self):
    seriesidlist = self.seriesidlist or self.default_seriesidlist
    outstr = f"""RestApiJsonRequestParamMaker:
    today = {self.today}
    from year = {self.year_fr}
    to year = {self.year_to}
    series id list = {seriesidlist}
    """
    return outstr


class CPIFetcher:

  DEFAULT_JSON_OUTFILENAME = 'bls_cpi.json'

  def __init__(self, from_year=None, to_year=None, seriesidlist=None):
    self.jsonreq = USBLS_API_SeriesDataFetcher(from_year, to_year, seriesidlist)
    self.processing_duration = None
    self.response_json_data = None
    self.seriesidlist = seriesidlist
    self.series_jsondumpfiles_saved = []
    self._json_outfilename = None

  @property
  def from_year(self):
    return self.jsonreq.year_fr

  @property
  def to_year(self):
    return self.jsonreq.year_to

  @property
  def today(self):
    return self.jsonreq.today

  @property
  def restapi_reqdatadict(self):
    return self.jsonreq.restapi_reqdatadict

  @property
  def json_outfilename(self):
    if self._json_outfilename is None:
      self._json_outfilename = self.DEFAULT_JSON_OUTFILENAME
    return self._json_outfilename

  @json_outfilename.setter
  def json_outfilename(self, filename):
    self._json_outfilename = filename

  @property
  def json_outfilepath(self):
    _json_outfilepath = cfg.get_datafile_abspath_in_app(self.json_outfilename)
    return _json_outfilepath

  def dump_n_save_res_per_series(self):
    self.series_jsondumpfiles_saved = ftchfs.dump_n_save_json_response_per_each_series_inside_data(
      self.response_json_data, folderpath=None, year_fr=self.from_year, year_to=self.to_year
    )

  def write_json_api_request_as_file(self):
    json_output_filepath = ftchfs.write_json_as_file_w_its_path(self.response_json_data, self.json_outfilepath)
    # property filepath cannot be changed, for it's derived from filename
    if json_output_filepath == self.json_outfilepath:
      # okay, no need to be changed
      return self.json_outfilepath
    # property was changed, let's change it via 'private' json_outfilename
    self.json_outfilename = os.path.split(json_output_filepath)[-1]

  def fetch_rest_api_json_response(self):
    self.response_json_data = ftchfs.fetch_json_response_w_restapi_reqdictdata(self.restapi_reqdatadict)
    self.write_json_api_request_as_file()
    self.dump_n_save_res_per_series()

  def process(self):
    start = time.time()
    self.fetch_rest_api_json_response()
    end = time.time()
    self.processing_duration = end - start

  def __str__(self):
    outstr = f"""CPIFetcher:
    today = {self.today}
    run duration = {self.processing_duration}
    from year = {self.from_year}
    to year = {self.to_year}
    json_outfilename = {self.json_outfilename}
    json_outfilepath = {self.json_outfilepath}
    series id files save = {self.series_jsondumpfiles_saved}
    """
    return outstr


def adhoctest():
  pass


def process():
  cpifetcher = CPIFetcher()
  cpifetcher.process()
  print('Stats', cpifetcher)


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()
