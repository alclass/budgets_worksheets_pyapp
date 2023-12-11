#!/usr/bin/env python3
"""
fs/datefs/years_date_functions.py
  contains date-related functions

import collections as coll
import os
import settings
# import fs.datefs.introspect_dates as intr
"""
import calendar
import datetime
from dateutil.relativedelta import relativedelta
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv  # .convert_str_or_attrsobj_to_date_or_none
WEEKEND_PREVIOUS_DATE_MAX_RECURSE = 41  # go back up to 31 days (a month) plus 10
WEEKDAYS3LETTER = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
ALL_MONTHS_ENG_CAP_FIRST_LIST = list(map(lambda e: calendar.month_name[e], range(1, 13)))


def make_allmonths_englishlower3letter_list():
  return list(map(lambda e: e[:3].lower(), ALL_MONTHS_ENG_CAP_FIRST_LIST))


def is_date_valid(pdate):
  pdate = cnv.make_date_or_none(pdate)
  if pdate is not None:
    return True
  return False



def get_decade_year_tenmultiplebased_from_or_current(pdate=None):
  """
  Examples:
    input: 2023-mm-dd, output: 2020
    input: None, output: 2020 (notice that at the time of this writing, year = 2023)
    input: 2010-mm-dd, output: 2010
  """
  pdate = cnv.make_date_or_today(pdate)
  year = pdate.year
  decade_year = year // 10 * 10
  return decade_year


def get_decade_year_tenmultiplebased_from_or_none(pdate=None):
  """
  Examples:
    input: 2023-mm-dd, output: 2020
    input: None, output: None (see also variation of this method which has a default)
    input: 2010-mm-dd, output: 2010
  """
  if pdate is None:
    return None
  pdate = cnv.make_date_or_today(pdate)
  if not isinstance(pdate, datetime.date):
    return None
  return get_decade_year_tenmultiplebased_from_or_current(pdate)


def get_first_date_in_decade_year_tenmultiplebased_from_or_current(pdate=None):
  """
  Examples:
    input: 2023-mm-dd, output: 2020-01-01
    input: None, output: 2020-01-01 (notice that at the time of this writing, year = 2023)
    input: 2010-mm-dd, output: 2010-01-01
  """
  year = get_decade_year_tenmultiplebased_from_or_current(pdate)
  # the above function either returns an int (datetime.date.year) or raises an exception there
  # ie year is "never" None here
  return datetime.date(year=year, month=1, day=1)


def get_first_date_in_decade_year_tenmultiplebased_from_or_none(pdate=None):
  """
  Examples:
    input: 2023-mm-dd, output: 2020-01-01
    input: None, output: None (see also variation of this method which has a default)
    input: 2010-mm-dd, output: 2010-01-01
  """
  year = get_decade_year_tenmultiplebased_from_or_none(pdate)
  if year is None:
    return None
  return datetime.date(year=year, month=1, day=1)



def is_date_weekend(pdate):
  """
  DEPRECATED | OBSOLETE
    for built-in Python modules do it
  e.g. calendar and datetime itself
  e.g. ?pdate.weekend()?

  """
  pdate = cnv.make_date_or_none(pdate)
  if pdate is None:
    return None
  try:
    weekdaynumber = pdate.weekday()
    if weekdaynumber in [5, 6]:
      return True
    return False
  except AttributeError:
    pass
  return None


def get_weekday3letter_from_date(pdate):
  """
  # previously:
  # weekday = calendar.weekday(year=indate.year, month=indate.month, day=indate.day)  # _ is days in month
  # currently:
  # weekday can be obtained directly from date (instead of calling calendar.weekday(date)
  """
  indate = cnv.make_date_or_none(pdate)
  if indate is None:
    return None
  weekday = indate.weekday()
  return WEEKDAYS3LETTER[weekday]


def get_date_or_previous_monday_to_friday(pdate, max_recurse=0):
  indate = cnv.make_date_or_none(pdate)
  if indate is None:
    return None
  if max_recurse > WEEKEND_PREVIOUS_DATE_MAX_RECURSE:
    return None
  if is_date_weekend(indate):
    previous_date = indate - datetime.timedelta(days=1)
    return get_date_or_previous_monday_to_friday(previous_date, max_recurse + 1)
  return indate


def get_monthslastday_date_via_calendar(pdate):
  indate = cnv.make_date_or_none(pdate)
  if indate is None:
    return None
  _, n_days_in_month = calendar.monthrange(year=indate.year, month=indate.month)  # _ is the first weekday in month
  return datetime.date(year=indate.year, month=indate.month, day=n_days_in_month)




def trans_datelist_uniq_n_desc(datelist):
  """
  # remove repeats
  od = coll.OrderedDict({})
  for d in datelist:
    od.update({d: 1})
  datelist = list(od.keys())
  return sort_datelist_desc(datelist)
  """
  if datelist is None or len(datelist) == 0:
    return []
  datelist = map(lambda x: cnv.make_date_or_none(x), datelist)
  datelist = sorted(set(filter(lambda x: x is not None, datelist)))  # remove repeats and make it asc
  return reversed(datelist)  # make it desc and return


def adhoc_test3():
  today = datetime.date.today()
  weekday = today.weekday()
  print(today, 'weekday =>', weekday, get_weekday3letter_from_date(today))
  # adjust_datelist_if_str(datelist)
  datelist = "2023-01-11 2022-10-1"
  print('input datelist', datelist)


def adhoc_test():
  """
  pdate = get_monthslastday_date_via_calendar('2020-7-3')
  print("get_monthslastday_date_via_calendar('2020-7-3')", pdate)
  print(make_allmonths_englishlower3letter_list())
  """
  dtstr = "2023-12-09 14:28:15.400870"
  print(dtstr)
  dto = cnv.make_date_or_none(dtstr)
  print(dto)
  y, m, d = 2020, 7, 3
  # strdate = f"{y}-{m}-{d}"
  strdate = f"{y}{m:02}{d:02}"
  returned_date = cnv.make_date_or_none(strdate)
  print(strdate, 'returned_date', returned_date)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
