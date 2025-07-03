#!/usr/bin/env python3
"""
commands/fetch/verify_n_update_local_cpi_db.py
  verifies if a new month has already been elapsed for a new CPI_US API-fetch
  and, if so, executes the script that fetches the new data remotely and record them locally.
"""
import datetime
from dateutil.relativedelta import relativedelta
import fs.datefs.years_date_functions as dtfs
import fs.datefs.refmonths_mod as rmfs
import commands.fetch.cpi_us.read_cpis_from_db as cpi  # .get_last_available_cpi_n_refmonth_fromdb_by_series
import commands.fetch.cpi_us.bls_cpi_api_fetcher_fs as cftch  # .CPIFetcher
MIN_REFMONTHS_ELAPSED_FOR_A_NEW_REMOTE_FETCH = 1


class Verifier:

  def __init__(self):
    self._current_refmonthdate = None
    self.today = datetime.date.today()
    self.mostrecent_refmonthdate_in_db = None
    self.baselineindex = None
    self.n_months_elapsed = None
    self.api_has_been_fetch = False

  @property
  def is_time_for_apifetch(self):
    if self.n_months_elapsed is None:
      return False
    return self.n_months_elapsed >= MIN_REFMONTHS_ELAPSED_FOR_A_NEW_REMOTE_FETCH

  @property
  def current_refmonthdate(self):
    if self._current_refmonthdate is None:
      self._current_refmonthdate = rmfs.make_refmonthdate_or_none(self.today)
      if self._current_refmonthdate is None:
        error_msg = 'Error: current refmonthdate was not derived from %s' % str(self.today)
        raise ValueError(error_msg)
    return self._current_refmonthdate

  def dbfetch_mostrecent(self):
    self.baselineindex, self.mostrecent_refmonthdate_in_db = cpi.get_last_available_cpi_n_refmonth_fromdb_by_series()
    if self.mostrecent_refmonthdate_in_db is None:
      self.mostrecent_refmonthdate_in_db = dtfs.get_first_date_in_decade_year_tenmultiplebased_from_or_current()
      scr_msg = (f'most recent refmonth is None, defaulting to beginning of decade,'
                 f' ie {self.mostrecent_refmonthdate_in_db}')
      print(scr_msg)
    else:
      self.mostrecent_refmonthdate_in_db = rmfs.make_refmonthdate_or_none(self.mostrecent_refmonthdate_in_db)

  def verify_more_than_one_refmonth(self):
    current_refmonthdate = rmfs.make_refmonthdate_or_current(self.today)
    reladelt = relativedelta(current_refmonthdate, self.mostrecent_refmonthdate_in_db)
    self.n_months_elapsed = 12 * reladelt.years + reladelt.months

  def process(self):
    self.dbfetch_mostrecent()
    self.verify_more_than_one_refmonth()
    if self.is_time_for_apifetch:
      apifetcher = cftch.CPIFetcher(from_year=None, to_year=self.today.year)
      apifetcher.process()
      self.api_has_been_fetch = True

  def __str__(self):
    min_n_refmonths = MIN_REFMONTHS_ELAPSED_FOR_A_NEW_REMOTE_FETCH
    outstr = f"""Verifier:
    today = {self.today}
    current refmonth = {self.current_refmonthdate}
    last API-fetch on = {self.mostrecent_refmonthdate_in_db}
    CPI index then = {self.baselineindex}
    n of months elapsed since = {self.n_months_elapsed} | for a new fetch {min_n_refmonths} refmonths should elapse
    is it time for API-fetch = {self.is_time_for_apifetch} (ie more than one month passed relative to last index in db)
    api_has_been_fetch = {self.api_has_been_fetch}
    """
    return outstr


def process():
  verifier = Verifier()
  verifier.process()
  print('Stats', verifier)


if __name__ == '__main__':
  process()
