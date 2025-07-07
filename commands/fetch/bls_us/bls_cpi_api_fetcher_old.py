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
import time
import commands.fetch.bls_us.cpi_rest_api_fetcher_fs as ftchfs  # .fetch_json_response_w_restapi_reqdictdata


class OldBLSAPISeriesDataFetcher:

  def fetch_rest_api_json_response(self):
    self.response_json_data = ftchfs.fetch_json_response_w_restapi_reqdictdata(self.restapi_reqdatadict)
    self.write_json_api_request_as_file()
    self.dump_n_save_res_per_series()

  @property
  def restapi_reqdatadict(self):
    return self.jsonreq.restapi_reqdatadict

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

  def process(self):
    start = time.time()
    self.fetch_rest_api_json_response()
    end = time.time()
    self.processing_duration = end - start


def process():
  pass


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()
