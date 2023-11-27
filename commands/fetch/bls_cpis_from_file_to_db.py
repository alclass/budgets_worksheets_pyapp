#!/usr/bin/env python3
"""
commands/fetch/bls_cpis_from_file_to_db.py
  fetches BLS CPI data from local db
Acronyms:
  BLS => Burreau of Labor Statistics (USA's)
  CPI => Consumer Price Index (US-measured)

Based on:
  www.bls.gov/developers/api_python.html
"""
import datetime
from dateutil.relativedelta import relativedelta
import settings as cfg
import fs.datefs.datefunctions as dtfs
cur_seriesid = 'CUUR0000SA0'
sur_seriesid = 'SUUR0000SA0'
DEFAULT_SERIESID = 'CUUR0000SA0'
seriesidlist = [cur_seriesid, sur_seriesid]


def get_cpi_baselineindex_for_refmonth_m2_in_db(refmonthdate, seriesid=None):
  """
  This function must be ENCAPSULATED in package-module fin
  The input pdate is transformed to an M-2 date ie month minus 2
  """
  refmonthdate = dtfs.make_refmonthdate_or_none(refmonthdate)
  if isinstance(refmonthdate, datetime.date):
    # make M-2 (adjust day=1 already happens above with make_refmonthdate_or_none())
    m2_refmonthdate = refmonthdate + relativedelta(months=-2)
    baselineindex = get_cpi_baselineindex_for_refmonth_in_db(m2_refmonthdate, seriesid)
    return baselineindex, m2_refmonthdate
  return None, None


def get_cpi_baselineindex_for_refmonth_in_db(refmonthdate, p_seriesid=None):
  refmonthdate = dtfs.make_refmonthdate_or_none(refmonthdate)
  if not isinstance(refmonthdate, datetime.date):
    return None
  conn = cfg.get_connection()
  cursor = conn.cursor()
  seriesid = p_seriesid or DEFAULT_SERIESID
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


def get_last_available_cpi_baselineindex_in_db(p_seriesid=None):
  """
  It searches for index by the most recent refmonthdate
  returns both the index and the most recent refmonthdate
  """
  conn = cfg.get_connection()
  cursor = conn.cursor()
  seriesid = p_seriesid or DEFAULT_SERIESID
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


def adhoctest():
  for seriesid in seriesidlist:
    print('seriesid', seriesid)
    baselineindex, refmonthdate = get_last_available_cpi_baselineindex_in_db(seriesid)
    scr_msg = f"\t{refmonthdate} => {baselineindex:.4f}"
    print(scr_msg)
    baselineindex, refmonthdate = get_cpi_baselineindex_for_refmonth_m2_in_db(refmonthdate, seriesid)
    scr_msg = f"\t{refmonthdate} => {baselineindex:.4f}"
    print(scr_msg)


def process():
  pass


if __name__ == '__main__':
  """
  process()
  """
  adhoctest()
