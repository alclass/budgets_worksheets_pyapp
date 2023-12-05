"""
fs/datefs/introspect_dates_datamass.py
"""

import datetime
import fs.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_order


def get_testtuple_12strdatelist_n_corresp_date_datamass(zfill=0):
  """
  Forms a datamass with all (12) combinations of strdates
  """
  zfill = intr.normalize_zfill_to_0_1_or_2(zfill)
  y, m, d = 2023, 5, 15
  pdate = datetime.date(year=y, month=m, day=d)
  outstrdatelist = []
  for posorder in intr.ORDERPOS_TOKENS_AVAILABLE:
    for sep in intr.STRDATE_SEPARATORS:
      strdate = intr.form_strdate_w_date_sep_posorder_opt_zfill(pdate, sep, posorder, zfill)
      outstrdatelist.append(strdate)
  return outstrdatelist, pdate


def get_testtuple_strdatelist_n_datelist_for_extraction_wo_sep_n_posorder():
  strdatelist = ['1965-5-15', '2023/12/13', '2023.5.6', '20211121']
  y, m, d = 1965, 5, 15
  dt1 = datetime.date(year=y, month=m, day=d)
  y, m, d = 2023, 12, 13
  dt2 = datetime.date(year=y, month=m, day=d)
  # this next one is unconclusive # y, m, d = 2023, 5, 6 # ie, day & month are ambiguous
  dt3 = None
  y, m, d = 2021, 11, 21
  dt4 = datetime.date(year=y, month=m, day=d)
  datelist = [dt1, dt2, dt3, dt4]
  return strdatelist, datelist


def get_unconclusive_strdatelist_f_extr_wo_sep_n_posorder():
  """
  All strdates in-here are "unconclusive", ie either day and month are ambiguous
    or year itself is ambiguous with day
  """
  strdatelist = ['1965-5-1', '30/12/13', '2023.5.6', '2021121']
  return strdatelist


def get_testtuple_coinc_day_month_sdlist_n_dlist_f_extr_wo_sep_n_posorder():
  """
  The first one is the only that produces a date, the others produce None
  """
  strdatelist = ['1965-5-5', '32/12/12', '2023.6.6', '20190131']
  y, m, d = 1965, 5, 5
  dt1 = datetime.date(year=y, month=m, day=d)
  y, m, d = 32, 12, 12
  dt2 = datetime.date(year=y, month=m, day=d)
  y, m, d = 2023, 6, 6
  dt3 = datetime.date(year=y, month=m, day=d)
  y, m, d = 2019, 1, 31
  dt4 = datetime.date(year=y, month=m, day=d)
  datelist = [dt1, dt2, dt3, dt4]
  return strdatelist, datelist


def adhoc_test2():
  strdate = '2021121'
  y = strdate[:4]
  m = strdate[4:6]
  d = strdate[6:18]  # the to-index is not raising IndexError if > len-1
  print(strdate, len(strdate), y, m, d)
  strdate = '20211213'
  y = strdate[:4]
  m = strdate[4:6]
  d = strdate[6:8]
  print(strdate, len(strdate), y, m, d)


def adhoc_test():
  strdatelist, pdate = get_testtuple_12strdatelist_n_corresp_date_datamass()
  print(strdatelist)
  print(pdate)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test2()
