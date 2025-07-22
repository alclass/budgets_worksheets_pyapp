#!/usr/bin/env python3
"""
art/bcb_br/fetch/db/dbfetch_exrates_buysell_wi_dates_cls.py
  Fetches BCB's Exchange Rate buy/sell prices by daily-dates from local db

from typing import Any, AnyStr
import collections
import pandas as pd
import settings as sett
import lib.datefs.refmonths_mod as rmd
import lib.db.db_settings as dbs
"""
import argparse
import datetime
import json
import math
import sqlite3
from dateutil.relativedelta import relativedelta
import art.inflmeas.bcb_br.classes.modelbase_currency_exchrate as exrt  # exrt.CurrencyPairExchangeRateOnDate
import lib.datefs.convert_to_date_wo_intr_sep_posorder as dtfs
import lib.datefs.refmonths_mod as rmd
import lib.db.sqlite.db_sqlite_manager as sqlim  # sqlim.SqliteHandler

sqlite3.register_adapter(dict, lambda d: json.dumps(d).encode())
# argparse CLI arguments
parser = argparse.ArgumentParser(description="Obtain Arguments")
parser.add_argument(
  '-i', '--dateini', metavar='dateini', type=str,
  help="the beginning date in date range for finding daily exchange rate quotes",
)
parser.add_argument(
  '-f', '--datefim', metavar='datefim', type=str,
  help="the ending date in date range for finding daily exchange rate quotes",
)
parser.add_argument(
  '-mr', '--monthrange',  metavar='monthrange', type=str, nargs=2,
  help="month range (ini, fim) as the date range for finding daily exchange rate quotes",
)
parser.add_argument(
  '-y', '--year', type=int, nargs=1,
  help="year as the date range for finding daily exchange rate quotes",
)
parser.add_argument(
  '-cy', '--currentyear', action='store_true',
  help="days since the beginning of the current year as the date range for finding daily exchange rate quotes",
)
parser.add_argument(
  '-rdf', '--readdatefile', action='store_true',
  help="marker/signal for inputting the dateadhoctests from the conventioned datefile located in the app's data folder",
)
args = parser.parse_args()


class BCBExchangeRateNonSAFetcher:

  tablename = 'currencies_exchangerates'
  days_difference_when_one_of_the_dates_misses = 10

  def __init__(self, dailydate_fr=None, dailydate_to=None, datelist=None, curr_pair=None):
    self._dailydate_fr = dailydate_fr
    self._dailydate_to = dailydate_to
    self.datelist = datelist
    self.curr_pair = curr_pair
    self.n_daily_exrates = 0
    self.first_acc_index = None
    self.last_acc_index = None
    self.sqlhld = sqlim.SqliteHandler()
    self.days_n_exrts_dict = {}
    self.treat_attrs()
    self.process()

  def treat_attrs(self):
    """
    refmonth_fr and refmonth_to are treated in their 'property/setter' attribute-methods
    """
    self.treat_dates()
    self.treat_currpair()

  def treat_dates(self):
    """
    Out of the 3 dates sources (date_fr, date_to, datelist), only datelist is treated here.

    In this class, the two dates (from [date_fr] and to [date_to]) are dynamic properties,
      so they don't need to be treated at __init__() time,
      they are 'lazily' treated on their 'property' methods

    The two dates treatment is the following:

      1) if the two dates are given, those they are
      2) if date_from is given, date_to is that plus a conventioned number of days
      3) if date_from is not given, and date_to is, that is this minus a conventioned number of days
      4) if neither is given, date_to defaults to 'today' and rule 3 above is applied
    Examples:
      eg1
        dailydate_fr = 2020-10-15
        dailydate_to = None
          apply rule 2 above, resulting
        dailydate_fr = 2020-10-15
        dailydate_to = 2020-10-25
      eg2
        dailydate_fr = None
        dailydate_to = 2020-10-15
          apply rule 3 above, resulting
        dailydate_fr = 2020-10-15
        dailydate_to = 2020-10-25
      eg3
        dailydate_fr = None
        dailydate_to = None
          apply rule 3 above, resulting
        dailydate_fr = today - ndays
        dailydate_to = today
    """
    self.datelist = dtfs.trans_convertabledates_to_datelist(self.datelist)
    self.datelist.sort()

  def treat_currpair(self):
    """
      exrt.DEFAULT_CURR_NUM
      exrt.DEFAULT_CURR_DEN
      exrt.REGISTERED_3LETTER_CURRENCIES
    """
    if self.curr_pair is None or self.curr_pair == (None, None):
      self.curr_pair = exrt.DEFAULT_CURR_NUM, exrt.DEFAULT_CURR_DEN
      return
    try:
      curr_num, curr_den = self.curr_pair
      errmsg = ''
      if curr_num not in exrt.REGISTERED_3LETTER_CURRENCIES:
        errmsg = f"curr_num {curr_num} not in registered {exrt.REGISTERED_3LETTER_CURRENCIES}\n"
      if curr_den not in exrt.REGISTERED_3LETTER_CURRENCIES:
        errmsg = f"curr_den {curr_den} not in registered {exrt.REGISTERED_3LETTER_CURRENCIES}\n"
      if errmsg != '':
        raise ValueError(errmsg)
    except TypeError:
      self.curr_pair = exrt.DEFAULT_CURR_NUM, exrt.DEFAULT_CURR_DEN

  @property
  def curr_num(self):
    return self.curr_pair[0]

  @property
  def curr_den(self):
    return self.curr_pair[1]

  @property
  def total_days_inbetween(self):
    return dtfs.calc_n_completedays_between_dates(self.dailydate_to, self.dailydate_fr)

  @property
  def dailydate_fr(self):
    if self.datelist:
      return self.datelist[0]
    # step 1: if it's datetime.date, return it rightaway
    if isinstance(self._dailydate_fr, datetime.date):
      return self._dailydate_fr
    # step 2: if it's convertible to datetime.date, return it
    self._dailydate_fr = dtfs.make_date_or_none(self._dailydate_fr)
    if self._dailydate_fr is not None:
      return self._dailydate_fr
    # at this point, _dailydate_fr is None, it has to be derived from dailydate_to
    # step 3: derive it from dailydate_to under the hypotheses below
    ndays = self.days_difference_when_one_of_the_dates_misses
    if isinstance(self._dailydate_to, datetime.date):
      # step 3a: dailydate_to is datetime.date, subtract it of 'diff' and return result
      self._dailydate_fr = self._dailydate_to - relativedelta(days=ndays)
      return self._dailydate_fr
    # at this point, _dailydate_to may be either None or an object not datetime.date
    # find out if it's convertible to datetime.date, or it's indeed None
    self._dailydate_to = dtfs.make_date_or_none(self._dailydate_to)
    if self._dailydate_to is None:
      # step 3b: dailydate_to was not convertible to datetime.date, so it defaults to 'today',
      self._dailydate_to = datetime.date.today()
    # step 3c: at this point, dailydate_to exists (whether today or some other date),
    #   apply the conventioned diff to dailydate_fr and return it
    self._dailydate_fr = self._dailydate_to - relativedelta(days=ndays)
    return self._dailydate_fr

  def append_to_datelist(self, p_dailydate):
    p_dailydate = dtfs.make_date_or_none(p_dailydate)
    if p_dailydate:
      self.datelist.append(p_dailydate)

  @dailydate_fr.setter
  def dailydate_fr(self, p_dailydate=None):
    if self.datelist:
      self.append_to_datelist(p_dailydate)
      return
    p_dailydate = dtfs.make_date_or_none(p_dailydate)
    if p_dailydate is None:
      if not isinstance(self._dailydate_to, datetime.date):
        self._dailydate_to = dtfs.make_date_or_today(self._dailydate_to)
      self._dailydate_fr = self._dailydate_to - relativedelta(days=10)
    else:
      self._dailydate_fr = p_dailydate

  @property
  def dailydate_to(self):
    if self.datelist:
      return self.datelist[0]
    if isinstance(self._dailydate_to, datetime.date):
      return self._dailydate_to
    self._dailydate_to = dtfs.make_date_or_none(self._dailydate_to)
    if self._dailydate_to is not None:
      return self._dailydate_to
    # at this point, _dailydate_to is None
    if isinstance(self._dailydate_fr, datetime.date):
      self._dailydate_to = self._dailydate_fr + relativedelta(days=10)
      return self._dailydate_to
    self._dailydate_fr = dtfs.make_date_or_none(self._dailydate_fr)
    if self._dailydate_fr is not None:
      self._dailydate_to = self._dailydate_fr + relativedelta(days=10)
    # at this point, the only resort is to make dailydate_to equals today
    # and dailydate_fr equals today minus 10 (or its conventioned antecedence)
    self._dailydate_to = datetime.date.today()
    self._dailydate_fr = self._dailydate_to - relativedelta(days=10)
    return self._dailydate_to

  @dailydate_to.setter
  def dailydate_to(self, p_dailydate=None):
    if self.datelist:
      self.append_to_datelist(p_dailydate)
      return
    self._dailydate_to = dtfs.make_date_or_today(p_dailydate)

  @property
  def sqlselect_wi_datelist_str(self):
    sql = f"""SELECT * FROM {self.tablename}
    WHERE
      curr_num = ? and
      curr_den = ? and
      refdate IN ? ;  
    """
    return sql

  @property
  def sqlselect_bw_ini_n_fim_dates_str(self):
    sql = f"""SELECT * FROM {self.tablename}
    WHERE
      curr_num = ? and
      curr_den = ? and
      refdate >= ? and  
      refdate <= ? ;  
    """
    return sql

  @property
  def sqlselect_bw_ini_n_fim_dates_str_n_its_tuplevalues(self):
    tuplevalues = (
      self.curr_num, self.curr_den, self.dailydate_fr, self.dailydate_to
    )
    sql_n_tuplevalues = self.sqlselect_bw_ini_n_fim_dates_str, tuplevalues
    return sql_n_tuplevalues

  @property
  def sqlselect_wi_datelist_str_n_its_tuplevalues(self):
    strdatelist = dtfs.trans_datelist_to_strdatelist(self.datelist)
    tuplevalues = (
      self.curr_num, self.curr_den, strdatelist
    )
    sql_n_tuplevalues = self.sqlselect_wi_datelist_str, tuplevalues
    return sql_n_tuplevalues

  @property
  def min_buyprice_in_interval(self):
    if len(self.days_n_exrts_dict) > 0:
      buyprices = map(lambda o: o.buyprice, self.days_n_exrts_dict.values())
      buyprices = filter(lambda buyprice: buyprice is not None, buyprices)
      minbuyprice = min(buyprices)
      return minbuyprice
    return None

  @property
  def max_buyprice_in_interval(self):
    if len(self.days_n_exrts_dict) > 0:
      buyprices = map(lambda o: o.buyprice, self.days_n_exrts_dict.values())
      buyprices = filter(lambda buyprice: buyprice is not None, buyprices)
      maxbuyprice = max(buyprices)
      return maxbuyprice
    return None

  @property
  def buyprice_amplitude_var_wi_interval(self):
    """
    This variatioin counts after the first given month
    """
    if self.max_buyprice_in_interval is None or self.min_buyprice_in_interval is None:
      return 0.0
    variation = self.max_buyprice_in_interval - self.min_buyprice_in_interval
    return variation

  @property
  def buyprice_pct_amplitude_var_wi_interval(self):
    """
    This variatioin counts after the first given month
    """
    return 100 * self.buyprice_amplitude_var_wi_interval / self.min_buyprice_in_interval

  def dbfetch_days_n_buysell_as_dict_bt_dates(self):
    """
    pdict = self.sqlhld.fetch_as_dict(sql, tuplevalues)
    for row in pdict:
      print(row.acc_index)

    """
    if not self.datelist:
      sql, tuplevalues = self.sqlselect_bw_ini_n_fim_dates_str_n_its_tuplevalues
    else:
      sql, tuplevalues = self.sqlselect_wi_datelist_str_n_its_tuplevalues
    cursor = self.sqlhld.execute(sql, tuplevalues)
    self.days_n_exrts_dict = {}
    for i, row in enumerate(cursor.fetchall()):
      refdate = dtfs.make_date_or_none(row['refdate'])
      if refdate is None:
        continue
      exrt_o = exrt.DayCurrExchRate(refdate)
      exrt_o.buypriceint = row['buypriceint']
      exrt_o.sellpriceint = row['sellpriceint']
      self.n_daily_exrates += 1
      self.days_n_exrts_dict.update({refdate: exrt_o})

  def process(self):
    self.dbfetch_days_n_buysell_as_dict_bt_dates()

  def prettyprint_exrates_bt_dates(self):
    pdict = self.days_n_exrts_dict
    n_days = len(pdict)
    n_decplaces = 0
    if n_days != 0:
      n_decplaces = math.floor(math.log10(n_days)) + 1
    for i, dailydate in enumerate(pdict):
      seq = i + 1
      buyprice = pdict[dailydate]
      seqstr = str(seq).zfill(n_decplaces)
      scrmsg = f"{seqstr} | {dailydate} | {buyprice}"
      print(scrmsg)

  def show_result_table(self):
    for i, dailydate in enumerate(self.days_n_exrts_dict):
      exrt_o = self.days_n_exrts_dict[dailydate]
      seq = i + 1
      scrmsg = f"{seq} | {exrt_o}"
      print(scrmsg)

  def make_floatstrs_for_selfstr(self):
    # 1 min_buyprice_in_interval
    min_buyprice = self.min_buyprice_in_interval
    minbuyprice_str = f"{min_buyprice:6.5f}" if min_buyprice is not None else 's/inf'
    # 2 max_buyprice_in_interval
    max_buyprice = self.max_buyprice_in_interval
    maxbuyprice_str = f"{max_buyprice:6.5f}" if max_buyprice is not None else 's/inf'
    # 3 buyprice_amplitude_var_wi_interval
    buyprice_ampvar = self.buyprice_amplitude_var_wi_interval
    buyprice_ampvar_str = f"{buyprice_ampvar:6.5f}" if buyprice_ampvar is not None else 's/inf'
    # 4 buyprice_pct_amplitude_var_wi_interval
    buyprice_pctampvar = self.buyprice_pct_amplitude_var_wi_interval
    buyprice_pctampvar_str = f"{buyprice_pctampvar:6.3f}%" if buyprice_pctampvar is not None else 's/inf'
    return minbuyprice_str, maxbuyprice_str, buyprice_ampvar_str, buyprice_pctampvar_str

  def __str__(self):
    minbuyprice_str, maxbuyprice_str, buyprice_ampvar_str, pctbuyamp_str = self.make_floatstrs_for_selfstr()
    outstr = f"""{self.__class__.__name__}
    Date range: from = {self.dailydate_fr} | to = {self.dailydate_to} 
    total exrt days = {len(self.days_n_exrts_dict.items())} | total days in-between = {self.total_days_inbetween}
    min buyprice within interval = {minbuyprice_str} {self.curr_num}/{self.curr_den}
    max buyprice within interval = {maxbuyprice_str} {self.curr_num}/{self.curr_den}
    buyprice min-max amplitude within interval = {self.buyprice_amplitude_var_wi_interval:6.5f} 
    buyprice min-max pct ampl var within interval = {pctbuyamp_str} (it's amplitude divided by min in period) 
    db_path = {self.sqlhld.db_path}
    """
    return outstr


def adapt_date_iso(val: datetime.date):
  """Adapt datetime.date to ISO 8601 date."""
  return val.isoformat()


def adapt_datetime_iso(val: datetime.datetime):
  """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
  return val.isoformat()


def adapt_datetime_epoch(val: datetime.datetime):
  """Adapt datetime.datetime to Unix timestamp.
  The datetime.datetime object in Python's standard datetime module
    has the timestamp() method. This method returns the time elapsed
    since the Unix epoch (January 1, 1970, 00:00:00 UTC)
    as a floating-point number, typically representing seconds.
  """
  return int(val.timestamp())


def convert_date(val):
  """
  previously
  return bytes(datetime.date.fromisoformat(val))
  """
  return datetime.date.fromisoformat(val.decode())


# https://docs.python.org/3/library/sqlite3.html
# (with examples) https://github.com/python/cpython/issues/99392
sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_converter("datetime.date", convert_date)


def adhoctest1():
  date_fr = '2020-10-15'
  # date_to = "2020-10-25"
  date_to = datetime.date.today()
  print('adhoctest1 Looking up exchange rate for date range: =', date_fr, '|', date_to)
  fetcher = BCBExchangeRateNonSAFetcher(
    dailydate_fr=date_fr,
    dailydate_to=date_to
  )
  fetcher.show_result_table()
  print(fetcher)


def adhoctest2():
  """
  """
  pass


def adhoctest3():
  """
  """
  pass


def adhoctest4():
  """
  """
  pass


def get_args():
  dateini = args.dateini
  datefim = args.datefim
  if not dateini and not datefim:
    if args.monthrange:
      dateini, datefim = rmd.trans_monthrange_into_dailydaterange_or_none(args.monthrange)
  if not dateini and not datefim:
    if args.year:
      dateini, datefim = rmd.trans_year_into_dailydaterange(args.year)
  if not dateini and not datefim:
    if args.currentyear:
      dateini, datefim = rmd.trans_year_into_dailydaterange()
  return dateini, datefim


def process():
  dateini, datefim = get_args()
  datelist = dtfs.make_random_dates(5, '2025-05-09', '2025-07-09')
  fetcher = BCBExchangeRateNonSAFetcher(
    dailydate_fr=dateini,
    dailydate_to=datefim,
    datelist=datelist
  )
  fetcher.show_result_table()
  print(fetcher)
  scrmsg = f"dateini = {dateini} | datefim = {datefim}"
  print(scrmsg)
  print(args)


if __name__ == '__main__':
  """
  process()
  adhoctest1()
  adhoctest2()
  adhoctest3()
  """
  process()
