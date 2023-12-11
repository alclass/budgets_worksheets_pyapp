#!/usr/bin/env python3
"""
fs/datefs/refmonths_mod.py
  Contains monthly and refmonthly date functions.

import fs.datefs.introspect_dates as intr
"""
import datetime
from dateutil.relativedelta import relativedelta
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv


class ClassWithYearMonthDay:
  def __init__(self, year=None, month=None, day=None):
    self.year = year
    self.month = month
    self.day = day

  def as_date(self):
    try:
      y, m, d = int(self.year), int(self.month), int(self.day)
      dt = datetime.date(year=y, month=m, day=d)
      return dt
    except (TypeError, ValueError):
      pass
    return None

  def as_refmonthdate(self):
    try:
      y, m = int(self.year), int(self.month)
      dt = datetime.date(year=y, month=m, day=1)
      return dt
    except (TypeError, ValueError):
      pass
    return None


def calc_refmonth_plus_n(pdate, n):
  pdate = cnv.make_date_or_none(pdate)
  if pdate is None:
    return None
  try:
    n = int(n)
  except (TypeError, ValueError):
    return pdate
  if pdate.day != 1:
    pdate = datetime.date(year=pdate.year, month=pdate.month, day=1)
  return pdate + relativedelta(months=n)


def calc_refmonth_minus_n(pdate, n):
  try:
    n = int(n)
  except (TypeError, ValueError):
    return pdate
  n = -n
  return calc_refmonth_plus_n(pdate, n)


def make_refmonthdate_or_current(refmonthdate=None):
  refmonthdate = make_refmonthdate_or_none(refmonthdate)
  if isinstance(refmonthdate, datetime.date):
    return refmonthdate
  today = datetime.date.today()
  current_refmonthdate = datetime.date(year=today.year, month=today.month, day=1)
  return current_refmonthdate


def make_refmonth_or_none(refmonth):
  """
  Notice: differently from make_date_or_none(), this function does not include the 'day' field in a date,
    though it returns a date with day=1
  """
  if refmonth is None:
    return None
  try:
    y = int(refmonth.year)
    m = int(refmonth.month)
    return datetime.date(year=y, month=m, day=1)
  except (AttributeError, TypeError, ValueError):
    # pass on for a new try below
    pass
  try:
    ppp = str(refmonth).split(' ')
    pp = ppp[0].split('-')
    year = int(pp[0])
    month = int(pp[1])
    return datetime.date(year=year, month=month, day=1)
  except (IndexError, ValueError):
    pass
  return None


def make_refmonth_or_current(str_or_date_refmonth=None):
  refmonthdate = make_refmonth_or_none(str_or_date_refmonth)
  if refmonthdate is not None:
    return refmonthdate
  today = datetime.date.today()
  return datetime.date(year=today.year, month=today.month, day=1)


def get_monthslastday_date_via_addition(pdate):
  indate = cnv.make_date_or_none(pdate)
  if indate is None:
    return None
  if indate.day > 1:
    date_set_on_first_day_of_month = datetime.date(indate.year, indate.month, 1)
  else:
    date_set_on_first_day_of_month = indate
  date_on_first_day_of_next_month = date_set_on_first_day_of_month + relativedelta(months=1)
  monthslastday_date = date_on_first_day_of_next_month - relativedelta(days=1)
  return monthslastday_date


def make_refmonthdate_or_none(refmonthdate=None):
  if refmonthdate is None:
    return None
  if isinstance(refmonthdate, datetime.date):
    if refmonthdate.day == 1:
      return refmonthdate
    return datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=1)
  try:
    refmonthdate = str(refmonthdate).strip(' \t\r\n')
    ppp = refmonthdate.split(' ')
    pp = ppp[0].split('-')
    year = int(pp[0])
    month = int(pp[1])
    return datetime.date(year=year, month=month, day=1)
  except (AttributeError, TypeError, ValueError):
    pass
  return None


def adhoc_test():
  """
  """
  y, m, d = 2012, 2, 3
  attrs_obj = ClassWithYearMonthDay(year=y, month=m, day=d)
  expected_refmonthdate = attrs_obj.as_refmonthdate()
  pdate = datetime.date(year=y, month=m, day=d)
  returned_refmonthdate = make_refmonth_or_none(pdate)
  print('expected_refmonthdate (done with ClassWithYearMonthDay)', expected_refmonthdate)
  print('returned_refmonthdate', returned_refmonthdate)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
