#!/usr/bin/env python3
"""
dategenerators.py
  contains generator functions for dateadhoctests.

Example of one such functions:
  => gen_dailydates_for_last_month_opt_order()
  A generator function that returns all daily dates of last month
    (relative to the system's current date)
"""
import calendar
import copy
import datetime
from dateutil.relativedelta import relativedelta


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


def make_refmonth_or_current(str_or_date_refmonth):
  refmonthdate = make_refmonth_or_none(str_or_date_refmonth)
  if refmonthdate is not None:
    return refmonthdate
  today = datetime.date.today()
  return datetime.date(year=today.year, month=today.month, day=1)


def convert_strdatelist_to_datelist(strdatelist):
  datelist = []
  for strdate in strdatelist:
    if isinstance(strdate, datetime.date):
      datelist.append(strdate)
      continue
    pdate = make_date_from_str_or_none(strdate)
    if pdate is None:
      continue
    datelist.append(pdate)
  return datelist


def make_date_or_none(pdate):
  """
  The input is tested for 'date' in 3 subsequent conversion-tests, ie:
    1 if it's a datetime.date itself or a subclass of it (which is returned rightaway) or
    2 if it's an object that contains, as properties, the int attributes year, month & day
    2 if it's an object whose str-repr has the prefix form "yyyy-mm-dd" ie, at_least_1digit_year-1or2digit_month-1or2digit_day
  param: pdate object | string | None
  output: datetime.date | None

  if issubclass(pdate, datetime.date):
    return pdate

  """
  if isinstance(pdate, datetime.date):
    return pdate
  try:
    y = int(pdate.year)
    m = int(pdate.month)
    d = int(pdate.day)
    return datetime.date(year=y, month=m, day=d)
  except (AttributeError, TypeError, ValueError):
    # pass on for a new try below
    pass
  try:
    pdate = str(pdate)
    ppp = pdate.split(' ')
    pp = ppp[0].split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = int(pp[2])
    return datetime.date(year=year, month=month, day=day)
  except (IndexError, TypeError, ValueError):
    pass
  return None


def make_date_or_today(pdate):
  pdate = make_date_or_none(pdate)
  if pdate is None:
    return datetime.date.today()
  return pdate


def make_date_from_str_or_none(strdate):
  return make_date_or_none(strdate)



def gen_dailydates_bw_ini_fim_asc(startpoint, finishpoint, cutoff_date=None, accfuture=True):
  today = datetime.date.today()
  current_date = copy.copy(startpoint)
  while current_date <= finishpoint:
    if not accfuture:
      if current_date > today:
        return
    if cutoff_date and current_date > cutoff_date:
      return
    yield current_date
    current_date = current_date + relativedelta(days=1)  # it's crescent
  return


def gen_dailydates_bw_ini_fim_desc(startpoint, finishpoint, cutoff_date=None, accfuture=True):
  today = datetime.date.today()
  current_date = copy.copy(startpoint)
  while current_date >= finishpoint:
    if not accfuture:
      if current_date > today:
        return
    if cutoff_date and current_date > cutoff_date:
      return
    yield current_date
    current_date = current_date - relativedelta(days=1)  # it's decrescent
  return


def gen_dailydates_bw_ini_fim_opt_order(date_ini, date_fim, decrescent=False):
  try:
    date_ini = make_date_from_str_or_none(date_ini)
    date_fim = make_date_from_str_or_none(date_fim)
  except TypeError:
    return []
  if decrescent:
    startpoint = date_fim
    finishpoint = date_ini
    return gen_dailydates_bw_ini_fim_desc(startpoint, finishpoint)
  startpoint = date_ini
  finishpoint = date_fim
  return gen_dailydates_bw_ini_fim_asc(startpoint, finishpoint)


def gen_dailydates_for_lastweek_opt_order(decrescent=False):
  today = datetime.date.today()
  seven_days_before = today - relativedelta(days=7)
  return gen_dailydates_bw_ini_fim_opt_order(seven_days_before, today, decrescent)


def get_gendailydates_for_lastweek_opt_order(decrescent=False):
  """
  datelist = []
  for pdate in gen_dailydates_for_last7days_opt_order(decrescent):
    datelist.append(pdate)
  return datelist
  """
  return list(gen_dailydates_for_lastweek_opt_order(decrescent))


def gen_dailydates_for_lastweek_wo_today_opt_order(decrescent=False):
  today = datetime.date.today()
  for pdate in gen_dailydates_for_lastweek_opt_order(decrescent):
    if pdate < today:
      yield pdate
  return

def get_gendailydates_for_lastweek_wo_today_opt_order(decrescent=False):
  return list(gen_dailydates_for_lastweek_wo_today_opt_order(decrescent))


def gen_dailydates_for_last_month_opt_order(decrescent=False, cutoff_date=None):
  today = datetime.date.today()
  refmonthdate = today - relativedelta(months=1)
  if refmonthdate.day != 1:
    refmonthdate = datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=1)
  return gen_dailydates_for_refmonth_or_empty_opt_order(refmonthdate, decrescent, cutoff_date)


def get_gendailydates_for_last_month_opt_order(decrescent=False):
  """

  """
  return list(gen_dailydates_for_last_month_opt_order(decrescent))


def gen_dailydates_for_refmonth_or_lastmonth_opt_order(refmonthdate=None, decrescent=False, cutoff_date=None):
  refmonthdate = make_refmonth_or_none(refmonthdate)
  if refmonthdate is None:
    return gen_dailydates_for_last_month_opt_order(decrescent, cutoff_date)
  return gen_dailydates_for_refmonth_or_empty_opt_order(refmonthdate, decrescent, cutoff_date)

def get_gendailydates_for_refmonth_or_lastmonth_opt_order(refmonthdate=None, decrescent=False):
  return list(gen_dailydates_for_refmonth_or_lastmonth_opt_order(refmonthdate, decrescent))


def get_gendailydates_for_refmonth_or_lastmonth_opt_order(refmonthdate=None, decrescent=False, cutoff_date=None):
  return list(gen_dailydates_for_refmonth_or_lastmonth_opt_order(refmonthdate, decrescent, cutoff_date))


def gen_dailydates_for_refmonth_or_empty_opt_order(refmonthdate, decrescent=False, cutoffdate=None):
  refmonthdate = make_refmonth_or_none(refmonthdate)
  if refmonthdate is None:
    return []
  year = refmonthdate.year
  month = refmonthdate.month
  _, lastday = calendar.monthrange(year, month)  # the _ is weekday
  firstdateinmonth = datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=1)
  lastdateinmonth = datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=lastday)
  if decrescent:
    startpoint = lastdateinmonth
    finishpoint = firstdateinmonth
    return gen_dailydates_bw_ini_fim_desc(startpoint, finishpoint, cutoffdate)
  startpoint = firstdateinmonth
  finishpoint = lastdateinmonth
  return gen_dailydates_bw_ini_fim_asc(startpoint, finishpoint, cutoffdate)


def get_gendailydates_for_refmonth_or_empty_opt_order(refmonthdate, decrescent=False):
  return list(gen_dailydates_for_refmonth_or_empty_opt_order(refmonthdate, decrescent))


def gen_dailydates_or_empty_for_year_opt_order(pyear, decrescent=False, cutoff_date=None):
  if pyear is None:
    return []
  try:
    pyear = int(pyear)
  except ValueError:
    return []
  firstdayinyear = datetime.date(year=pyear, month=1, day=1)
  lastdayinyear = datetime.date(year=pyear, month=12, day=31)
  if decrescent:
    startpoint = lastdayinyear
    finishpoint = firstdayinyear
    return gen_dailydates_bw_ini_fim_desc(startpoint, finishpoint, cutoff_date)
  startpoint = firstdayinyear
  finishpoint = lastdayinyear
  return gen_dailydates_bw_ini_fim_desc(startpoint, finishpoint, cutoff_date)


def get_gendailydates_or_empty_for_year_opt_order(pyear, decrescent=False, cutoff_date=None):
  return list(gen_dailydates_or_empty_for_year_opt_order(pyear, decrescent, cutoff_date))


def gen_dailydates_for_current_year_opt_order(decrescent=False):
  today = datetime.date.today()
  firstdayinyear = datetime.date(year=today.year, month=1, day=1)
  if decrescent:
    startpoint = today
    finishpoint = firstdayinyear
    return gen_dailydates_bw_ini_fim_desc(startpoint, finishpoint)
  startpoint = firstdayinyear
  finishpoint = today
  return gen_dailydates_bw_ini_fim_asc(startpoint, finishpoint)


def get_gendailydates_for_current_year_opt_order(decrescent=False):
  return list(gen_dailydates_for_current_year_opt_order(decrescent))


def gen_dailydates_for_yearrange_or_empty_opt_order(yearini, yearfim=None, decrescent=False, cutoff_date=None):
  """
  generates a list of years in-between yearini and yearfim
  obs:
    1 this method version applies a default for yearfim
    2 this method version works "for the future", ie for dateadhoctests above today
  """
  if yearini is None:
    return []
  try:
    yearini = int(yearini)
  except ValueError:
    return []
  today = datetime.date.today()
  try:
    yearfim = int(yearfim)
  except (TypeError, ValueError):
    yearfim = today.year
  if yearini > yearfim:
    return []
  for year in range(yearini, yearfim+1):
    for pdate in gen_dailydates_or_empty_for_year_opt_order(year, decrescent):
      if cutoff_date and pdate > cutoff_date:
        return
      yield pdate


def get_gendailydates_for_yearrange_or_empty_opt_order(yearini, yearfim=None, decrescent=False, cutoff_date=None):
  return list(gen_dailydates_for_yearrange_or_empty_opt_order(yearini, yearfim, decrescent, cutoff_date))


def gen_dailydates_for_yearrange_or_empty_opt_order_n_future(yearini, yearfim=None, decrescent=False, accept_future=False, cutoff_date=None):
  today = datetime.date.today()
  yearfim = yearfim or today.year
  try:
    yearini = int(yearini)
    yearfim = int(yearfim)
  except ValueError:
    return []
  if yearfim < today.year:
    return gen_dailydates_for_yearrange_or_empty_opt_order(yearini, yearfim, decrescent, cutoff_date)
  first_day = datetime.date(year=yearini, month=1, day=1)
  if not accept_future:
    last_day = today
  else:
    last_day = datetime.date(year=yearfim, month=12, day=31)
  if cutoff_date and cutoff_date > last_day:
    last_day = cutoff_date
  if last_day < first_day:
    return []
  return gen_dailydates_bw_ini_fim_opt_order(first_day, last_day, decrescent)


def gen_dailydates_f_yearini_t_today_or_empty_opt_order(yearini, decrescent=False):
  """
  generates a list of years in-between yearini and yearfim
  obs:
    1 this method version does not apply a default for yearfim
    2 this method version does not work "for the future", ie for dateadhoctests above today
  """
  try:
    yearini = int(yearini)
  except (TypeError, ValueError):
    return []
  today = datetime.date.today()
  yearfim = today.year
  if yearini > yearfim:
    return []
  return gen_dailydates_for_yearrange_or_empty_opt_order(yearini, yearfim, decrescent, today)


def get_gendailydates_f_yearini_t_today_or_empty_opt_order(yearini, decrescent=False):
  datelist = []
  for pdate in gen_dailydates_f_yearini_t_today_or_empty_opt_order(yearini, decrescent):
    datelist.append(pdate)
  return datelist


def adhoc_test():
  """
  for i, pdate in enumerate(gen_daily_dates_for_last_month()):
    print(i+1, pdate)
  for i, pdate in enumerate(gen_daily_dates_for_last_month(decrescent=True)):
    print(i+1, pdate)
  refmonth = make_refmonth_from_str_or_none('2023-5')
  for i, pdate in enumerate(gen_daily_dates_for_refmonth(refmonth)):
    print(i+1, pdate)
  for i, pdate in enumerate(gen_daily_dates_for_current_year()):
    print(i+1, pdate)
  """
  strdatelist = ["2023-05-20", "2023-06-21"]
  print(strdatelist)
  datelist = convert_strdatelist_to_datelist(strdatelist)
  print('convert_strdatelist_to_datelist(strdatelist)')
  print(datelist)
  datelist = get_gendailydates_for_refmonth_or_lastmonth_opt_order('foo bar')
  print(len(datelist), datelist)
  datelist = get_gendailydates_for_refmonth_or_lastmonth_opt_order('2023-2')
  print(len(datelist), datelist)
  today = datetime.date.today()
  mo_m1_dt = today - relativedelta(months=1)
  print('mo_m1_dt', mo_m1_dt)


def process():
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
