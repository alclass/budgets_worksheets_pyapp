#!/usr/bin/env python3
"""
fs/economicfs/bcb_cotacao_fetcher_from_db_or_api.py

  This module contains class:
    => fs.economicfs.preapis_finfunctions.BCBCotacaoFetcher
  which models the cotacao fetching that uses a date-scheme
    that helps 'navigate' through weekend days and hollidays together with
    finding cotacao at its target date.
  Obs: the target date is the input date itself
       or a previous one that has cotacao data.
  Example:
    if a day is Sunday and Friday is not a holliday, target_date will
    be input date minus 2 (Friday is 2 days less than Sunday).
"""
import datetime
from dateutil.relativedelta import relativedelta
import calendar
import logging
import os
import random
import fs.datefs.datefunctions as dtfs
import fs.datefs.dategenerators as gendt
import fs.economicfs.bcb.bcb_api_finfunctions as apis
import fs.economicfs.bcb.bcb_fetchfunctions as fetchfs  # fetchfs.add_exchanger_to_res_bcb_api_namedtuple()
import settings as sett
_, modlevelogfn = os.path.split(__file__)
modlevelogfn = str(datetime.date.today()) + '_' + modlevelogfn[:-3] + '.log'
modlevelogfp = os.path.join(sett.get_datafolder_abspath(), modlevelogfn)
logging.basicConfig(filename=modlevelogfp, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # DEBUG means it and all others levels will be logged
DATES_STACK_SIZE = 5


def is_date_a_weekend_day(pdate):
  week_n = calendar.weekday(pdate.year, pdate.month, pdate.day)
  if week_n in [5, 6]:
    return True
  return False


def is_cotacao_in_holliday(namedtuple_cotacao):
  """
  The hypothesis for a cotacao on holliday is it
    having None as an exchange rate value inside it
    (field cotacao_compra or cotacao_venda)
  Notice also that the database table does not contain info for weekend-day rows
    and contains rows with None (ie null, for rate values) on hollidays.

  The structure below is that of the namedtuple that models the cotacao-datum:
  (please refer to the apis.py module for its exact formulation)
  apis.namedtuple_bcb_api1(
    'BCBAPI1DataStr',
    [cotacao_compra, cotacao_venda, cotacao_datahora,
     param_date, error_msg, gen_msg, exchanger]
  )
  """
  # an exception (TypeError if None, AttributeError if attribute inexists) may be raised from here
  if not isinstance(namedtuple_cotacao, apis.namedtuple_bcb_api1):
    error_msg = 'Object namedtuple_cotacao [%s] is not type namedtuple_bcb_api1' % str(namedtuple_cotacao)
    raise TypeError(error_msg)
  if namedtuple_cotacao.cotacao_compra is None:
    return True
  else:
    return False


def create_dates_stack_for_n_last_days(pdate, dates_stack_size=None):
  """
  The 'stack' is a list.
  """
  pdate = dtfs.make_date_or_none(pdate)
  if dates_stack_size is None:
    dates_stack_size = DATES_STACK_SIZE
  dates_stack = [pdate]
  for i in range(dates_stack_size):
    pdate = pdate - datetime.timedelta(days=1)
    dates_stack.append(pdate)
  dates_stack.reverse()  # the reverse() is because pop() takes out the last
  return dates_stack


def get_random_wait_seconds():
  return random.randint(1, 8)


class BCBCotacaoFetcher:
  """
  This class models fetching a date's cotacao info either from local db or from its API call.
  The 'buffering' is local, ie depends on the computer when this program is running and
    is devised to help diminish API calls altogether,
    ie once a date is request, it gets copied locally and,
    if needed again, retrieved without the API call.
  This class is able to handle weekend days (known programatically) and hollidays
    (when values return None (or null) from the API).

  The strategy on the day-date handling is the following:
    => exchange quotes exist during week days except hollidays.
    => exchange quotes do not exist on weekend days (Saturday & Sunday).
  So the system has to identify both weekends (which is easy with dateutils & calendar)
    and hollidays, which need a strategy proper.

  As a weekend is 'easily' identified, no API call needs to happen for these dates.
  However, when the API calls info for a holliday and the 'web payload' returns 'well' formed,
   it's expected that the exchangerate fields comes as None (or null)
   So it's safe to infer that that date as a holliday without,
     for example, keeping a separate table for hollidays.

  Considering the above, this class will do the following:
    => it receives a date as parameter
    => it builds a stack with at most 5 days (or a config number)
    => it will pop out dates from the date stack, one by one,
       until a date returns a cotacao record
      -> as said, there are up to 5 (or a config amount) tries for finding a date cotacao info
      -> the datetime connected to the cotacao info also belongs to the received datum
    => if all 5 days (or a config one) do not return a cotacao record, an exception is raised
    TO-DO: the 5 days, at this version, is hardcoded, it may become a config parameter in the future.
  """

  def __init__(self, pdate):
    self.date = pdate
    self.treat_date()
    self.weekend_day_hits = 0
    self.holliday_hits = 0
    self.dates_stack_size = DATES_STACK_SIZE
    self.dates_stack = create_dates_stack_for_n_last_days(self.date, self.dates_stack_size)
    self.target_date = None
    self._target_datetime = None
    self.namedtuple_cotacao = None
    self.process()

  @property
  def target_datetime(self):
    """
    This attribute is the same as self.namedtuple_cotacao.cotacao_datahora
    """
    if self.namedtuple_cotacao is None:
      return None
    if self._target_datetime is None:
      self._target_datetime = self.namedtuple_cotacao.cotacao_datahora
    return self._target_datetime

  def treat_date(self):
    pdate = self.date
    self.date = dtfs.make_date_or_none(pdate)
    if self.date is None:
      error_msg = 'Data error: Date entered [%s] is not valid.' % pdate
      raise ValueError(error_msg)
    today = datetime.date.today()
    if self.date > today:
      error_msg = (
          'Inconsistent error: Date entered [%s] is greater than today [%s] ' %
          (self.date, today)
      )
      raise ValueError(error_msg)

  def verify_date_n_try_find_its_corresponding_cotacao(self):
    # 1st: look if it's in weekend
    if is_date_a_weekend_day(self.target_date):
      self.weekend_day_hits += 1
      return None
    # 2nd: look up local database
    namedtuple_cotacao = fetchfs.fetch_cotacao_in_db_for_date_or_none(self.target_date)
    if namedtuple_cotacao is not None:
      # Holliday hypothesis
      if is_cotacao_in_holliday(namedtuple_cotacao):
        self.holliday_hits += 1
        return None  # upon returning, it will pop out another date or terminate
      return namedtuple_cotacao
    # cotacao is None from db, move on
    namedtuple_cotacao = fetchfs.fetch_cotacao_via_the_api_for_date_n_dbsaveit(self.target_date)
    if namedtuple_cotacao is not None:
      # test Holliday hypothesis
      if is_cotacao_in_holliday(namedtuple_cotacao):
        self.holliday_hits += 1
        return None  # upon returning, it will pop out another date or terminate
      return namedtuple_cotacao
    # connection error
    error_msg = 'Nothing returned from the API call after looking up back %s days.\n' % self.dates_stack_size
    error_msg += 'Either connection is broken or remote server is down.\n'
    error_msg += 'Start date is [%s]' % self.date
    raise ConnectionError(error_msg)

  def pop_dates_n_try_find_cotacao(self):
    if len(self.dates_stack) > 0:
      self.target_date = self.dates_stack.pop()
      print('Popped date', self.target_date)
      namedtuple_cotacao = self.verify_date_n_try_find_its_corresponding_cotacao()
      if namedtuple_cotacao is None:
        return self.pop_dates_n_try_find_cotacao()  # recurse until at most dates_stack gets empty
      return namedtuple_cotacao
    print('All 5 dates were popped out and no cotacao data found.')

  def process(self):
    self.namedtuple_cotacao = self.pop_dates_n_try_find_cotacao()

  def __str__(self):
    outstr = f"""BCBCotacaoFetcher:
    Upper date: {self.date}
    target date: {self.target_date}
    target datetime: {self.target_datetime}
    weekend_day_hits: {self.weekend_day_hits}
    holliday_hits: {self.holliday_hits}
    Found entry date if any: {self.target_date}
    dates stack size:  {self.dates_stack_size}
    Found cotacao if any: {self.namedtuple_cotacao}
    """
    return outstr


def adhoctest():
  pdate = datetime.date.today()
  dates_stack = create_dates_stack_for_n_last_days(pdate)
  popped_date = dates_stack.pop()
  print('Popped', popped_date)
  print(dates_stack)


def process():
  """
  # adhoc_test_ptab()
  pdate = '2022-03-03'
  bcb_api_nt = dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)
  print(bcb_api_nt)
  pass
  pdate = '2023-10-29'
  """
  today = datetime.date.today()
  before20days = today - relativedelta(days=31)
  for pdate in gendt.gen_dailydates_bw_ini_fim_opt_order(before20days, today):
    prefetcher = BCBCotacaoFetcher(pdate)
    print(prefetcher)


if __name__ == "__main__":
  """
  adhoctest()
  """
  process()
