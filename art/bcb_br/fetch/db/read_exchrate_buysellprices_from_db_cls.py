#!/usr/bin/env python3
"""
art/bcb_br/fetch/db/read_exchrate_buysellprices_from_db_cls.py
  Fetches BCB's Exchange Rate buy/sell prices by daily-dates from local db

"""
# from typing import Any, AnyStr
import argparse
import collections
import datetime
import json
import math
import pandas as pd
import sqlite3
import settings as sett
from dateutil.relativedelta import relativedelta
import lib.datefs.refmonths_mod as rmd
import lib.datefs.convert_to_date_wo_intr_sep_posorder as dtfs
import lib.db.sqlite.db_sqlite_manager as sqlim  # sqlim.SqliteHandler
import lib.db.db_settings as dbs
cur_seriesid = 'CUUR0000SA0'
sur_seriesid = 'SUUR0000SA0'
DEFAULT_SERIESID = 'CUUR0000SA0'
KNOWN_SERIESID = ['CUUR0000SA0', 'SUUR0000SA0']
available_cpi_seriesid_list = [cur_seriesid, sur_seriesid]
NTCpiMonth = collections.namedtuple('NTCpiMonth', field_names=['cpi_us', 'refmonthdate'])
sqlite3.register_adapter(dict, lambda d: json.dumps(d).encode())
# argparse CLI arguments
parser = argparse.ArgumentParser(description="Obtain Arguments")
parser.add_argument(
  '-i', '--date_ini', metavar='date_ini', type=str,
  help="the beginning date in date range for finding daily exchange rate quotes",
)
parser.add_argument(
  '-f', '--date_fim', metavar='date_fim', type=str,
  help="the ending date in date range for finding daily exchange rate quotes",
)
parser.add_argument(
  '-mr', '--monthrange', type=int, nargs=2,
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
parser.add_argument(
  '-s', '--serieschar', choices=["C", "S"], default="C",
  help="marker/signal for inputting the dateadhoctests from the conventioned datefile located in the app's data folder",
)
args = parser.parse_args()


class BCBExchangeRateDbReader:

  tablename = 'currencies_exchangerates'

  def __init__(self, dailydate_fr=None, dailydate_to=None):
    self._dailydate_fr = dailydate_fr
    self._dailydate_to = dailydate_to
    self.n_monthly_indices = 0
    self.first_acc_index = None
    self.last_acc_index = None
    self.sqlhld = sqlim.SqliteHandler()
    self.treat_attrs()

  def treat_attrs(self):
    """
    refmonth_fr and refmonth_to are treated in their 'property/setter' attribute-methods
    """
    pass

  @property
  def total_days_inbetween(self):
    return dtfs.calc_n_completedays_between_dates(self.dailydate_to, self.dailydate_fr)

  @property
  def total_monthly_indices(self):
    return self.n_monthly_indices

  @property
  def dailydate_fr(self):
    if self._dailydate_fr is None:
      self._dailydate_fr = self.dailydate_to - relativedelta(days=10)
    return self._dailydate_fr

  @dailydate_fr.setter
  def dailydate_fr(self, p_dailydate=None):
    p_dailydate = rmd.make_refmonth_or_none(p_dailydate)
    if p_dailydate is None:
      self._dailydate_fr = self.dailydate_to - relativedelta(days=10)
    else:
      self._dailydate_fr = p_dailydate

  @property
  def dailydate_to(self):
    if self._dailydate_to is None:
      self._dailydate_to = dtfs.make_date_or_today()
    return self._dailydate_to

  @dailydate_to.setter
  def dailydate_to(self, p_refmonth=None):
    self._dailydate_to = dtfs.make_date_or_today(p_refmonth)

  @property
  def str_n_tuplevalues_select_bw_refmonths(self):
    sql = f"""SELECT * FROM {self.tablename}
    WHERE 
     refmonthdate >= ? and  
     refmonthdate <= ? ;  
    """
    tuplevalues = (self.refmonth_fr, self.refmonth_to)
    sql_n_tuplevalues = sql, tuplevalues
    return sql_n_tuplevalues

  @property
  def multiplier_within_period_after_1st_month(self):
    """
    This variatioin counts after the first given month
    """
    if self.last_acc_index is not None and self.first_acc_index is not None:
      mult = self.last_acc_index/self.first_acc_index
      return mult
    return None

  def get_months_n_refmonths_as_dict_bt_refmonths(self):
    """
    pdict = self.sqlhld.fetch_as_dict(sql, tuplevalues)
    for row in pdict:
      print(row.acc_index)

    """
    sql, tuplevalues = self.str_n_tuplevalues_select_bw_refmonths
    cursor = self.sqlhld.execute(sql, tuplevalues)
    pdict = {}
    acc_index = None
    for i, row in enumerate(cursor.fetchall()):
      refmonthdate = row['refmonthdate']
      acc_index = row['acc_index']
      self.n_monthly_indices += 1
      if i == 0:
        self.first_acc_index = acc_index
      pdict.update({refmonthdate: acc_index})
    self.last_acc_index = acc_index
    return pdict

  def print_months_n_refmonths_bt_refmonths(self):
    pdict = self.get_months_n_refmonths_as_dict_bt_refmonths()
    n_months = len(pdict)
    n_places = 0
    if n_months != 0:
      n_places = math.floor(math.log10(n_months)) + 1
    for i, refmonthdate in enumerate(pdict):
      seq = i + 1
      acc_index = pdict[refmonthdate]
      seqstr = str(seq).zfill(n_places)
      scrmsg = f"{seqstr} | {refmonthdate} | {acc_index}"
      print(scrmsg)

  def __str__(self):
    outstr = f"""{self.__class__.__name__}
    refmonth_fr = {self.refmonth_fr} 
    refmonth_to = {self.refmonth_to} 
    total_months = {self.total_months}
    total_monthly_indices = {self.total_monthly_indices}
    first_acc_index = {self.first_acc_index}
    last_acc_index = {self.last_acc_index}
    multiplier after 1st month = {self.multiplier_within_period_after_1st_month:6.5f} 
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


def get_min_or_max_available_refmonthdate_in_cpi_db(lowest=True, p_seriesid=None):
  conn = sett.get_sqlite_connection()
  cursor = conn.cursor()
  seriesid = p_seriesid or DEFAULT_SERIESID
  tuplevalues = (seriesid, )
  asc_or_desc = 'ASC' if lowest else 'DESC'
  sql = f"""
    SELECT refmonthdate FROM {dbs.IDXIND_TABLENAME}
      WHERE
        seriesid = ?
      ORDER BY
        refmonthdate {asc_or_desc}
      LIMIT 1;  """
  cursor.execute(sql, tuplevalues)
  try:
    refmonthdate = cursor.fetchone()[0]
    refmonthdate = rmd.make_refmonthdate_or_none(refmonthdate)
  except TypeError:
    refmonthdate = None
  # print('first_baselineindex', first_baselineindex)
  conn.close()
  # None may be returned
  return refmonthdate


def get_older_available_refmonthdate_in_cpi_db(seriesid=None):
  return get_min_or_max_available_refmonthdate_in_cpi_db(True, seriesid)


def get_newer_available_refmonthdate_in_cpi_db(seriesid=None):
  return get_min_or_max_available_refmonthdate_in_cpi_db(False, seriesid)


def get_older_available_year_in_cpi_db(seriesid=None):
  refmonthdate = get_older_available_refmonthdate_in_cpi_db(seriesid)
  try:
    return refmonthdate.year
  except (AttributeError, TypeError):
    pass
  return None


def get_newer_available_year_in_cpi_db(seriesid=None):
  refmonthdate = get_newer_available_refmonthdate_in_cpi_db(seriesid)
  try:
    return refmonthdate.year
  except (AttributeError, TypeError):
    pass
  return None


def convert_cpi_month_tuplerows_to_namedtuplerows(allrows):
  outrows = []
  for rowtuple in allrows:
    cpi, refmonthdate = rowtuple
    ntrow = NTCpiMonth(cpi_us=cpi, refmonthdate=refmonthdate)
    outrows.append(ntrow)
  return outrows


def get_cpi_baselineindex_for_refmonth_m2_in_db(refmonthdate, seriesid=None):
  """
  This function must be ENCAPSULATED in package-module fin
  The input pdate is transformed to an M-2 date ie month minus 2
  """
  refmonthdate = rmd.make_refmonthdate_or_none(refmonthdate)
  if isinstance(refmonthdate, datetime.date):
    # make M-2 (adjust day=1 already happens above with make_refmonthdate_or_none())
    m2_refmonthdate = refmonthdate + relativedelta(months=-2)
    baselineindex = get_cpi_baselineindex_for_refmonth_in_db(m2_refmonthdate, seriesid)
    return baselineindex, m2_refmonthdate
  return None, None


def get_cpi_baselineindex_for_refmonth_in_db(refmonthdate, p_seriesid=None):
  refmonthdate = rmd.make_refmonthdate_or_none(refmonthdate)
  if not isinstance(refmonthdate, datetime.date):
    return None
  conn = sett.get_sqlite_connection()
  cursor = conn.cursor()
  seriesid = p_seriesid or DEFAULT_SERIESID
  tuplevalues = (seriesid, refmonthdate)
  sql = f"""
    SELECT baselineindex FROM {dbs.IDXIND_TABLENAME}
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


def get_last_available_cpi_n_refmonth_fromdb_by_series(p_seriesid=None):
  """
  searches for the cpi_us on the most recent refmonthdate
  returns both the index and its corresponding most recent refmonthdate
  """
  conn = sett.get_sqlite_connection()
  cursor = conn.cursor()
  seriesid = p_seriesid or DEFAULT_SERIESID
  sql = f"""
    SELECT baselineindex, refmonthdate FROM {dbs.IDXIND_TABLENAME}
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


def trans_cpis_refmonths_from_ntist_to_dictlist(ntlist):
  return list(map(lambda e: e.as_dict(), ntlist))


def trans_cpis_refmonths_from_tuplelist_to_ntlist(tuplelist):
  output_ntlist = []
  for cpi_n_refmonth in tuplelist:
    cpi, refmonthdate = cpi_n_refmonth
    nt = NTCpiMonth(cpi_us=cpi, refmonthdate=refmonthdate)
    output_ntlist.append(nt)
  return output_ntlist


def trans_cpis_refmonths_from_tuplelist_to_dictlist(tuplelist):
  ntlist = trans_cpis_refmonths_from_tuplelist_to_ntlist(tuplelist)
  return trans_cpis_refmonths_from_ntist_to_dictlist(ntlist)


def get_all_cpis_n_refmonths_as_ntlist_fromdb_by_series(p_seriesid=None):
  """
    pdict = {'cpi_us': cpi_us, 'refmonthdate': refmonthdate}
    outdictlist.append(pdict)

  """
  tuplelist = get_all_cpis_n_refmonths_as_tuplelist_fromdb_by_series(p_seriesid)
  return trans_cpis_refmonths_from_tuplelist_to_ntlist(tuplelist)


def get_all_cpis_n_refmonths_as_dictlist_fromdb_by_series(p_seriesid=None):
  """
  for cpi_n_refmonth in tuplelist:
    cpi_us, refmonthdate = cpi_n_refmonth
    pdict = {'cpi_us': cpi_us, 'refmonthdate': refmonthdate}
    outdictlist.append(pdict)
  """
  ntlist = get_all_cpis_n_refmonths_as_ntlist_fromdb_by_series(p_seriesid)
  return trans_cpis_refmonths_from_ntist_to_dictlist(ntlist)


def get_all_cpis_n_refmonths_as_tuplelist_fromdb_by_series(p_seriesid=None):
  """
  Selects all available indices.
  """
  conn = sett.get_sqlite_connection()
  cursor = conn.cursor()
  seriesid = p_seriesid or DEFAULT_SERIESID
  sql = f"""
    SELECT baselineindex, refmonthdate FROM {dbs.IDXIND_TABLENAME}
      WHERE
        seriesid = ? 
      ORDER BY
        refmonthdate ASC;
  """
  cursor.execute(sql, (seriesid,))
  rows = cursor.fetchall()
  allrows = []
  for row in rows:
    baselineindex = row[0]
    refmonthdate = row[1]
    rowtuple = (baselineindex, refmonthdate)
    allrows.append(rowtuple)
  conn.close()
  return allrows


def get_cpis_n_refmonths_as_dictlist_fromdb_by_year_n_series(year, p_seriesid=None):
  tuplelist = get_cpis_n_refmonths_as_tuplelist_fromdb_by_year_n_series(year, p_seriesid)
  return trans_cpis_refmonths_from_tuplelist_to_dictlist(tuplelist)


def get_cpis_n_refmonths_as_ntlist_fromdb_by_year_n_series(year, p_seriesid=None):
  tuplelist = get_cpis_n_refmonths_as_tuplelist_fromdb_by_year_n_series(year, p_seriesid)
  return trans_cpis_refmonths_from_tuplelist_to_ntlist(tuplelist)


def get_cpis_n_refmonths_as_tuplelist_fromdb_by_year_n_series(year, p_seriesid=None):
  """
  Selects all available indices.
  """
  str_year = str(year)
  conn = sett.get_sqlite_connection()
  cursor = conn.cursor()
  seriesid = p_seriesid or DEFAULT_SERIESID
  sql = f"""
    SELECT baselineindex, refmonthdate FROM {dbs.IDXIND_TABLENAME}
      WHERE
        seriesid = ? and
        substr(refmonthdate, 1, 4) = ?
      ORDER BY
        refmonthdate ASC;
  """
  cursor.execute(sql, (seriesid, str_year))
  rows = cursor.fetchall()
  allrows = []
  for row in rows:
    baselineindex = row[0]
    refmonthdate = row[1]
    rowtuple = (baselineindex, refmonthdate)
    allrows.append(rowtuple)
  conn.close()
  return allrows


def get_all_cpis_n_refmonths_from_db_as_dataframe(p_seriesid=None):
  ntlist = get_all_cpis_n_refmonths_as_ntlist_fromdb_by_series(p_seriesid)
  df = pd.DataFrame(ntlist)
  return df


def adhoctest1():
  for seriesid in available_cpi_seriesid_list:
    print('seriesid', seriesid)
    baselineindex, refmonthdate = get_last_available_cpi_n_refmonth_fromdb_by_series(seriesid)
    scr_msg = f"\t refmonth={refmonthdate} => idx={baselineindex:.4f} (last available)"
    print(scr_msg)
    baselineindex, refmonthdate = get_cpi_baselineindex_for_refmonth_m2_in_db(refmonthdate, seriesid)
    scr_msg = f"\t refmonth={refmonthdate} => idx={baselineindex:.4f} (M2 ie Month-minus-2)"
    print(scr_msg)


def adhoctest2():
  """
  df = get_all_cpis_n_refmonths_from_db_as_dataframe()
  print(df.head())
  print(df.info())
  """
  year = 2025
  ret = get_cpis_n_refmonths_as_tuplelist_fromdb_by_year_n_series(year=year)
  print(year, 'get_cpis_n_refmonths_as_tuplelist_fromdb_by_year_n_series')
  print(ret)
  older_refmonth = get_older_available_refmonthdate_in_cpi_db()
  print('older_refmonth', older_refmonth)
  newer_refmonth = get_newer_available_refmonthdate_in_cpi_db()
  print('newer_refmonth', newer_refmonth)
  older_year = get_older_available_year_in_cpi_db()
  print('older_year', older_year)
  newer_year = get_newer_available_year_in_cpi_db()
  print('newer_year', newer_year)
  df = get_all_cpis_n_refmonths_from_db_as_dataframe()
  print(df.to_string())
  print('n rows', df.shape[0])


def adhoctest3():
  """
  refmonthdate = '2024-12-01'
  """
  refmonthdate = '2024-01-01'
  res = get_cpi_baselineindex_for_refmonth_in_db(refmonthdate)
  scrmsg = f'get_cpi_baselineindex_for_refmonth_in_db({refmonthdate}) => {res}'
  print(scrmsg)
  today = datetime.date.today()
  refmonthdate = datetime.date(year=today.year, month=today.month, day=1)
  res = get_cpi_baselineindex_for_refmonth_m2_in_db(refmonthdate)
  scrmsg = f'get_cpi_baselineindex_for_refmonth_in_db({refmonthdate}) => {res}'
  print(scrmsg)


def find_refmonth_ini_n_fim_lookingup_cliargs():
  print(args)
  try:
    refmonth_ini = args.refmonth_ini
    refmonth_fim = args.refmonth_fim
    if refmonth_ini:
      refmonth_ini = rmd.make_refmonth_or_none(refmonth_ini)
      refmonth_fim = rmd.make_refmonth_or_none(refmonth_fim)
      return refmonth_ini, refmonth_fim
  except AttributeError:
    pass
  try:
    year = int(args.year)
    refmonth_ini, refmonth_fim = rmd.make_refmonth_ini_n_fim_w_year_forbid_future(year)
    return refmonth_ini, refmonth_fim
  except (AttributeError, TypeError):
    pass
  try:
    if args.currentyear:
      refmonth_ini, refmonth_fim = rmd.make_refmonth_ini_n_fim_w_year_forbid_future()
      return refmonth_ini, refmonth_fim
  except AttributeError:
    pass
  try:
    if args.yearrange:
      pp = args.yearrange.split(',')
      year_ini = int(pp[0])
      year_fim = int(pp[1])
      refmonth_ini, refmonth_fim = rmd.make_refmonth_ini_n_fim_w_yearrange_forbid_future(year_ini, year_fim)
      return refmonth_ini, refmonth_fim
  except (AttributeError, IndexError, TypeError):
    pass
  # try:
  # bool_readdatefile = args.readdatefile
  return None, None


def process():
  refmonth_ini, refmonth_fim = find_refmonth_ini_n_fim_lookingup_cliargs()
  scrmsg = f"refmonth_ini={refmonth_ini} | refmonth_fim={refmonth_fim}"
  print(scrmsg)
  cpi_r = BCBExchangeRateDbReader(refmonth_ini, refmonth_fim)
  cpi_r.print_months_n_refmonths_bt_refmonths()
  print(cpi_r)


if __name__ == '__main__':
  """
  process()
  adhoctest1()
  adhoctest2()
  adhoctest3()
  """
  process()
