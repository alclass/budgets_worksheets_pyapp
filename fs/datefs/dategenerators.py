#!/usr/bin/env python3
"""
dategenerators.py
  contains generator functions for dates.
Example of one such functions:
  => gen_dates_for_last_month()
  A generator function that returns all day-dates for last month
    (relative to the system's current date)

import os
import fs.textfs.strfs as strfs
import settings
import collections as coll
"""
import calendar
import copy
import datetime
from dateutil.relativedelta import relativedelta


def make_date_from_str(strdate):
  if strdate is None:
    return None
  try:
    strdate = str(strdate)
    pp = strdate.split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = int(pp[2])
    refmonthdate = datetime.date(year=year, month=month, day=day)
    return refmonthdate
  except (IndexError, ValueError):
    pass
  return None

def make_refmonth_from_str(strdate):
  if strdate is None:
    return None
  try:
    strdate = str(strdate)
    pp = strdate.split('-')
    year = int(pp[0])
    month = int(pp[1])
    refmonthdate = datetime.date(year=year, month=month, day=1)
    return refmonthdate
  except (IndexError, ValueError):
    pass
  return None


def gen_decrescent_daily_dates_within(startpoint, finishpoint):
  current_date = copy.copy(startpoint)
  while current_date >= finishpoint:
    yield current_date
    current_date = current_date - relativedelta(days=1)  # it's decrescent
  return


def gen_crescent_daily_dates_within(startpoint, finishpoint):
  current_date = copy.copy(startpoint)
  while current_date <= finishpoint:
    yield current_date
    current_date = current_date + relativedelta(days=1)  # it's crescent
  return


def gen_daily_dates_for_daterange(date_ini, date_fim, decrescent=False):
  if decrescent:
    startpoint = date_fim
    finishpoint = date_ini
    return gen_decrescent_daily_dates_within(startpoint, finishpoint)
  startpoint = date_ini
  finishpoint = date_fim
  return gen_crescent_daily_dates_within(startpoint, finishpoint)


def gen_daily_dates_for_last_month(decrescent=False):
  today = datetime.date.today()
  t_a_month_ago = today - relativedelta(months=1)
  _, months_last_day = calendar.monthrange(t_a_month_ago.year, t_a_month_ago.month)  # _ is weekday
  firstdateinmonth = datetime.date(year=t_a_month_ago.year, month=t_a_month_ago.month, day=1)
  lastdateinmonth = datetime.date(year=t_a_month_ago.year, month=t_a_month_ago.month, day=months_last_day)
  if decrescent:
    startpoint = lastdateinmonth
    finishpoint = firstdateinmonth
    return gen_decrescent_daily_dates_within(startpoint, finishpoint)
  startpoint = firstdateinmonth
  finishpoint = lastdateinmonth
  return gen_crescent_daily_dates_within(startpoint, finishpoint)


def gen_daily_dates_for_refmonth_or_lastmonth(refmonthdate, decrescent=False):
  if refmonthdate is None:
    return gen_daily_dates_for_last_month(decrescent)
  return gen_daily_dates_for_refmonth(refmonthdate, decrescent)


def make_refmonth_from_str_or_none(str_or_date_refmonth):
  if isinstance(str_or_date_refmonth, datetime.date):
    return str_or_date_refmonth
  try:
    # None will be "caught" here
    refmonth = str(str_or_date_refmonth)
    pp = refmonth.split('-')
    year = int(pp[0])
    month = int(pp[1])
    pdate = datetime.date(year=year, month=month, day=1)
    return pdate
  except (IndexError, NameError, ValueError):
    pass
  return None


def gen_daily_dates_for_refmonth(refmonthdate, decrescent=False):
  bakrefmonth = copy.copy(refmonthdate)
  if type(refmonthdate) != datetime.date:
    refmonthdate = make_refmonth_from_str_or_none(refmonthdate)
  if refmonthdate is None:
    error_msg = 'Error: refmonth is None or not a refmonth (%s) in gen_daily_dates_for_refmonth()' % str(bakrefmonth)
    raise ValueError(error_msg)
  year = refmonthdate.year
  month = refmonthdate.month
  _, lastday = calendar.monthrange(year, month)  # the _ is weekday
  firstdateinmonth = datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=1)
  lastdateinmonth = datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=lastday)
  if decrescent:
    startpoint = lastdateinmonth
    finishpoint = firstdateinmonth
    return gen_decrescent_daily_dates_within(startpoint, finishpoint)
  startpoint = firstdateinmonth
  finishpoint = lastdateinmonth
  return gen_crescent_daily_dates_within(startpoint, finishpoint)


def gen_daily_dates_for_year(pyear, decrescent=False):
  firstdayinyear = datetime.date(year=pyear, month=1, day=1)
  lastdayinyear = datetime.date(year=pyear, month=12, day=31)
  if decrescent:
    startpoint = lastdayinyear
    finishpoint = firstdayinyear
    return gen_decrescent_daily_dates_within(startpoint, finishpoint)
  startpoint = firstdayinyear
  finishpoint = lastdayinyear
  return gen_crescent_daily_dates_within(startpoint, finishpoint)


def gen_daily_dates_for_current_year(decrescent=False):
  today = datetime.date.today()
  firstdayinyear = datetime.date(year=today.year, month=1, day=1)
  if decrescent:
    startpoint = today
    finishpoint = firstdayinyear
    return gen_decrescent_daily_dates_within(startpoint, finishpoint)
  startpoint = firstdayinyear
  finishpoint = today
  return gen_crescent_daily_dates_within(startpoint, finishpoint)


def adhoc_test():
  """
  for i, pdate in enumerate(gen_daily_dates_for_last_month()):
    print(i+1, pdate)
  for i, pdate in enumerate(gen_daily_dates_for_last_month(decrescent=True)):
    print(i+1, pdate)
  refmonth = make_refmonth_from_str_or_none('2023-5')
  for i, pdate in enumerate(gen_daily_dates_for_refmonth(refmonth)):
    print(i+1, pdate)
  """
  for i, pdate in enumerate(gen_daily_dates_for_current_year()):
    print(i+1, pdate)


def process():
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
