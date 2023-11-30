#!/usr/bin/env python3
"""
fs/datefs/from_to_convert_date_formats.py
"""
import datetime

import fs.datefs.introspect_dates as intr
import fs.datefs.datefunctions as dtfs


def trans_from_date_to_strdate_w_sep_n_posorder(pdate, sep='-', posorder='ymd'):
  try:
    y = f"{pdate.year}"
    m = f"{pdate.month:02}"
    d = f"{pdate.day:02}"
    if sep not in intr.STRDATE_SEPARATORS:
      return None
    if posorder == 'ymd':
     return y + sep + m + sep + d
    elif posorder == 'ydm':
      return y + sep + d + sep + m
    elif posorder == 'dmy':
      return d + sep + m + sep + y
    elif posorder == 'mdy':
      return m + sep + d + sep + y
  except (AttributeError, TypeError, ValueError):
    pass
  # fallback to returning None means that posorder is not one of the four available
  # [ymd, ydm,,dmy, mdy] or an except was caught due to pdate not implementing year, month, and day as int
  return None


def convert_yyyymmdd_dashsep_strdatelist_to_datelist(strdatelist):
  """
  This is the conventioned yyyy-mm-dd that is also the str repr from datetime.date
  Because of that, dtfs.make_date_or_none() is used directly instead of introspecting or converting via sep & posorder
  """
  datelist = map(lambda d: dtfs.make_date_or_none(d), strdatelist)
  return sorted(filter(lambda d: d is not None, datelist))


def convert_strdate_to_date_or_none_w_sep_n_fieldorder(strdate, sep, posorder):
  try:
    pp = strdate.split(sep)
    if posorder == 'ymd':
      y = int(pp[0])
      m = int(pp[1])
      d = int(pp[2])
    elif posorder == 'ydm':
      y = int(pp[0])
      d = int(pp[1])
      m = int(pp[2])
    elif posorder == 'dmy':
      d = int(pp[0])
      m = int(pp[1])
      y = int(pp[2])
    elif posorder == 'mdy':
      m = int(pp[0])
      d = int(pp[1])
      y = int(pp[2])
    else:
      return None
    return datetime.date(year=y, month=m, day=d)
  except (IndexError, TypeError, ValueError):
    pass
  return None


def trans_strdate_from_one_format_to_another_w_sep_n_posorder(
    pstrdate, fromsep='-', tosep='/', sourceposorder='ymd', targetposorder='mdy'
):
  """
    The input pstrdate must be in the ymd order.

  :param pstrdate:
  :param fromsep:
  :param tosep:
  :param sourceposorder:
  :param targetposorder:
  :return: datetime.date | None
  """
  if pstrdate is None:
    return None
  if isinstance(pstrdate, datetime.date):
    # if it's type is datetime.date, fromsep is ignored
    return trans_from_date_to_strdate_w_sep_n_posorder(pstrdate, tosep, targetposorder)
  # before go to str, try attributes
  pdate = convert_strdate_to_date_or_none_w_sep_n_fieldorder(pstrdate, fromsep, sourceposorder)
  if pdate is None:
    return None
  return trans_from_date_to_strdate_w_sep_n_posorder(pstrdate, tosep, targetposorder)


def adhoc_test():
  strdate = '2021-10-21'
  pdate = dtfs.make_date_or_none(strdate)
  odate = trans_strdate_from_one_format_to_another_w_sep_n_posorder(
    pstrdate=pdate, fromsep=None, tosep='/', sourceposorder=None, targetposorder='mdy' )
  print(odate)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
