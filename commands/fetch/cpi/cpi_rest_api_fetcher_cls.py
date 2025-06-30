#!/usr/bin/env python3
"""
commands/fetch/cpi/cpi_rest_api_fetcher_cls.py
  contains class Fetcher which is a client of the functions in
    commands/fetch/cpi/cpi_rest_api_fetcher_cls.py

The latter calls the public REST API that returns CPI month by month indices for known series (*)
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
import commands.fetch.cpi.cpi_rest_api_fetcher_cls as cpifs
BLS_URL = 'https://api.bls.gov/publicAPI/v1/timeseries/data/'
DEFAULT_HTTP_HEADERS = {'Content-type': 'application/json'}
DICTKEY_SERIESID_K = 'seriesID'


class Fetcher:

  def __init__(self, pdate):
    self.pdate = pdate

  def read_cpi_for_refmonth(self, pdate):
    pass


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
