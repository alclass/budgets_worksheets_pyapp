#!/usr/bin/env python3
"""
commands/fetch/read_cpis_from_db.py
  fetches BLS CPI data from local db
Acronyms:
  BLS => Burreau of Labor Statistics (USA's)
  CPI => Consumer Price Index (US-measured)
# import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv
"""
import collections
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import settings as sett
import fs.datefs.refmonths_mod as rfm
import fs.db.db_settings as dbs
cur_seriesid = 'CUUR0000SA0'
sur_seriesid = 'SUUR0000SA0'
DEFAULT_SERIESID = 'CUUR0000SA0'
available_cpi_seriesid_list = [cur_seriesid, sur_seriesid]
NTCpiMonth = collections.namedtuple('NTCpiMonth', field_names=['cpi', 'refmonthdate'])


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
    refmonthdate = rfm.make_refmonthdate_or_none(refmonthdate)
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
    ntrow = NTCpiMonth(cpi=cpi, refmonthdate=refmonthdate)
    outrows.append(ntrow)
  return outrows


def get_cpi_baselineindex_for_refmonth_m2_in_db(refmonthdate, seriesid=None):
  """
  This function must be ENCAPSULATED in package-module fin
  The input pdate is transformed to an M-2 date ie month minus 2
  """
  refmonthdate = rfm.make_refmonthdate_or_none(refmonthdate)
  if isinstance(refmonthdate, datetime.date):
    # make M-2 (adjust day=1 already happens above with make_refmonthdate_or_none())
    m2_refmonthdate = refmonthdate + relativedelta(months=-2)
    baselineindex = get_cpi_baselineindex_for_refmonth_in_db(m2_refmonthdate, seriesid)
    return baselineindex, m2_refmonthdate
  return None, None


def get_cpi_baselineindex_for_refmonth_in_db(refmonthdate, p_seriesid=None):
  refmonthdate = rfm.make_refmonthdate_or_none(refmonthdate)
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
  It searches for index by the most recent refmonthdate
  returns both the index and the most recent refmonthdate
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
    nt = NTCpiMonth(cpi=cpi, refmonthdate=refmonthdate)
    output_ntlist.append(nt)
  return output_ntlist


def trans_cpis_refmonths_from_tuplelist_to_dictlist(tuplelist):
  ntlist = trans_cpis_refmonths_from_tuplelist_to_ntlist(tuplelist)
  return trans_cpis_refmonths_from_ntist_to_dictlist(ntlist)


def get_all_cpis_n_refmonths_as_ntlist_fromdb_by_series(p_seriesid=None):
  """
    pdict = {'cpi': cpi, 'refmonthdate': refmonthdate}
    outdictlist.append(pdict)

  """
  tuplelist = get_all_cpis_n_refmonths_as_tuplelist_fromdb_by_series(p_seriesid)
  return trans_cpis_refmonths_from_tuplelist_to_ntlist(tuplelist)


def get_all_cpis_n_refmonths_as_dictlist_fromdb_by_series(p_seriesid=None):
  """
  for cpi_n_refmonth in tuplelist:
    cpi, refmonthdate = cpi_n_refmonth
    pdict = {'cpi': cpi, 'refmonthdate': refmonthdate}
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
  year = 2021
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
  refmonthdate = '2023-10-01'
  res = get_cpi_baselineindex_for_refmonth_in_db(refmonthdate)
  scrmsg = f'get_cpi_baselineindex_for_refmonth_in_db({refmonthdate}) => {res}'
  print(scrmsg)


def process():
  pass


if __name__ == '__main__':
  """
  process()
  adhoctest2()
  adhoctest1()
  """
  adhoctest3()

