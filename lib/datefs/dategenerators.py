#!/usr/bin/env python3
"""
dategenerators.py
  contains generator functions for dateadhoctests.

Example of one such functions:
  => gen_dailydates_for_last_month_opt_order_cday_accfut()
  A generator function that returns all daily dates of last month
    (relative to the system's current date)

import fs.datefs.introspect_dates as intr
"""
import calendar
import copy
import datetime
from dateutil.relativedelta import relativedelta
import lib.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import lib.datefs.refmonths_mod as rfm


def convert_strdatelist_to_datelist(strdatelist):
  datelist = []
  for strdate in strdatelist:
    if isinstance(strdate, datetime.date):
      datelist.append(strdate)
      continue
    pdate = cnv.make_date_or_none(strdate)
    if pdate is None:
      continue
    datelist.append(pdate)
  return datelist


def gen_dailydates_bw_ini_fim_asc(startpoint, finishpoint, accfuture=True):
  """
  accfuture is boolean for "accept the future?"
  """
  if startpoint > finishpoint:
    return
  today = datetime.date.today()
  if not accfuture and startpoint > today:
    return
  current_date = copy.copy(startpoint)
  while current_date <= finishpoint:
    if not accfuture:
      if current_date > today:
        return
    yield current_date
    current_date = current_date + relativedelta(days=1)  # it's crescent
  return


def gen_dailydates_bw_ini_fim_desc(startpoint, finishpoint, accfuture=True):
  """
  accfuture is boolean for "accept the future?"
  """
  if startpoint < finishpoint:
    return
  today = datetime.date.today()
  if not accfuture:
    if finishpoint > today:
      return
    if startpoint > today:
      startpoint = today
  current_date = copy.copy(startpoint)
  while current_date >= finishpoint:
    yield current_date
    current_date = current_date - relativedelta(days=1)  # it's decrescent
  return


def gen_dailydates_or_empty_bw_ini_fim_opt_order(date_ini, date_fim, decrescent=False):
  date_ini = cnv.make_date_or_none(date_ini)
  if date_ini is None:
    return
  date_fim = cnv.make_date_or_none(date_fim)
  if date_fim is None:
    return
  if decrescent:
    startpoint = date_fim
    finishpoint = date_ini
    return gen_dailydates_bw_ini_fim_desc(startpoint, finishpoint)
  startpoint = date_ini
  finishpoint = date_fim
  return gen_dailydates_bw_ini_fim_asc(startpoint, finishpoint)


def gen_dailydates_for_weekdate_opt_order(date_ini, decrescent=False, cutoff_idx=None, accfuture=False):
  dateini = cnv.make_date_or_today(date_ini)
  if dateini is None:
    return []
  today = datetime.date.today()
  n_days_in_a_week = 7
  n_days_a_first_for_adding = n_days_in_a_week - 1
  datefim = dateini + relativedelta(days=n_days_a_first_for_adding)
  try:
    cutoff_idx = int(cutoff_idx)
  except (TypeError, ValueError):
    cutoff_idx = None
  if cutoff_idx:
    if cutoff_idx > n_days_a_first_for_adding:
      return []
    datefim = dateini + relativedelta(days=cutoff_idx)
  if not accfuture:
    # relative future (ie relative to 'today') is not allowed when accfuture=False
    if dateini > today:
      return []
    if dateini <= today < datefim:
      datefim = today
  return gen_dailydates_or_empty_bw_ini_fim_opt_order(date_ini=dateini, date_fim=datefim, decrescent=decrescent)


def get_gendailydates_for_weekdate_opt_order(date_ini, decrescent=False, cutoff_idx=None, accfuture=False):
  return list(gen_dailydates_for_weekdate_opt_order(date_ini, decrescent, cutoff_idx, accfuture))


def gen_dailydates_for_lastweek_incl_today_opt_order(decrescent=False):
  """
    Generates daily dates for one whole past week with its 7 days INCLUDING 'today'
    @see also gen_dailydates_for_lastweek_wo_today_opt_order() which ends up on 'yesterday'
  """
  today = datetime.date.today()
  n_days_in_a_week = 7
  n_days_to_add_a_first_day_in_a_week = n_days_in_a_week - 1
  seven_days_before = today - relativedelta(days=n_days_to_add_a_first_day_in_a_week)
  return gen_dailydates_or_empty_bw_ini_fim_opt_order(seven_days_before, today, decrescent)


def get_gendailydates_for_lastweek_incl_today_opt_order(decrescent=False):
  """
  datelist = []
  for pdate in gen_dailydates_for_last7days_opt_order(decrescent):
    datelist.append(pdate)
  return datelist
  """
  return list(gen_dailydates_for_lastweek_incl_today_opt_order(decrescent))


def gen_dailydates_for_lastweek_wo_today_opt_order(decrescent=False):
  """
    Generates daily dates for one whole past week with its 7 days NOT INCLUDING today as an 8th day
    the "wo" in the function's name means "without"
  """
  today = datetime.date.today()
  n_days_in_a_week = 7
  first_date = today - relativedelta(days=n_days_in_a_week)  # it's 7 not 6 because today is not included
  yield first_date
  for pdate in gen_dailydates_for_lastweek_incl_today_opt_order(decrescent):
    if pdate < today:
      yield pdate
  return


def get_gendailydates_for_lastweek_wo_today_opt_order(decrescent=False):
  return list(gen_dailydates_for_lastweek_wo_today_opt_order(decrescent))


def gen_dailydates_for_last_month_opt_order_cday_accfut(decrescent=False, cutoff_day=None, accfuture=False):
  today = datetime.date.today()
  refmonthdate = today - relativedelta(months=1)
  if refmonthdate.day != 1:
    refmonthdate = datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=1)
  return gen_dailydates_for_refmonth_or_empty_opt_order_coff_accfut(refmonthdate, decrescent, cutoff_day, accfuture)


def get_gendailydates_for_last_month_opt_order_cday_accfut(decrescent=False):
  """

  """
  return list(gen_dailydates_for_last_month_opt_order_cday_accfut(decrescent))


def gen_dailydates_for_current_refmonth_opt_order_cday_accfut(
    decrescent=False, cutoff_day=None, accfuture=False
):
  refmonthdate = rfm.make_refmonth_or_current()
  return gen_dailydates_for_refmonth_or_empty_opt_order_coff_accfut(refmonthdate, decrescent, cutoff_day, accfuture)


def get_gendailydates_for_current_refmonth_opt_order_cday_accfut(
    decrescent=False, cutoff_day=None, accfuture=False
):
  return list(gen_dailydates_for_current_refmonth_opt_order_cday_accfut(decrescent, cutoff_day, accfuture))


def gen_dailydates_for_refmonth_or_current_opt_order_cday_accfut(
    refmonthdate=None, decrescent=False, cutoff_day=None, accfuture=False
):
  refmonthdate = rfm.make_refmonth_or_none(refmonthdate)
  if refmonthdate is None:
    return gen_dailydates_for_current_refmonth_opt_order_cday_accfut(decrescent, cutoff_day, accfuture)
  return gen_dailydates_for_refmonth_or_empty_opt_order_coff_accfut(refmonthdate, decrescent, cutoff_day, accfuture)


def get_gendailydates_for_refmonth_or_current_opt_order_cday_accfut(
    refmonthdate=None, decrescent=False, cutoff_day=None, accfuture=False
):
  return list(
    gen_dailydates_for_refmonth_or_current_opt_order_cday_accfut(
      refmonthdate, decrescent, cutoff_day, accfuture
    )
  )


def gen_dailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut(
    refmonthdate=None, decrescent=False, cutoff_day=None, accfuture=False
):
  refmonthdate = rfm.make_refmonth_or_none(refmonthdate)
  if refmonthdate is None:
    return gen_dailydates_for_last_month_opt_order_cday_accfut(decrescent, cutoff_day, accfuture)
  return gen_dailydates_for_refmonth_or_empty_opt_order_coff_accfut(refmonthdate, decrescent, cutoff_day, accfuture)


def get_gendailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut(
    refmonthdate=None, decrescent=False, cutoff_day=None, accfuture=False
):
  return list(
    gen_dailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut(
      refmonthdate, decrescent, cutoff_day, accfuture
    )
  )


def gen_dailydates_for_refmonth_or_empty_opt_order_coff_accfut(
    refmonthdate, decrescent=False, cutoff_day=None, accfuture=False
):
  refmonthdate = rfm.make_refmonth_or_none(refmonthdate)
  if refmonthdate is None:
    return []
  year = refmonthdate.year
  month = refmonthdate.month
  _, lastday = calendar.monthrange(year, month)  # the _ is weekday
  firstdateinmonth = datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=1)
  lastdateinmonth = datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=lastday)
  try:
    cutoff_day = int(cutoff_day)
  except (TypeError, ValueError):
    cutoff_day = None
  if cutoff_day and cutoff_day < lastday:
    lastdateinmonth = datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=cutoff_day)
  if decrescent:
    startpoint = lastdateinmonth
    finishpoint = firstdateinmonth
    return gen_dailydates_bw_ini_fim_desc(startpoint, finishpoint, accfuture)
  startpoint = firstdateinmonth
  finishpoint = lastdateinmonth
  return gen_dailydates_bw_ini_fim_asc(startpoint, finishpoint, accfuture)


def get_gendailydates_for_refmonth_or_empty_opt_order(refmonthdate, decrescent=False, accfuture=False):
  return list(gen_dailydates_for_refmonth_or_empty_opt_order_coff_accfut(refmonthdate, decrescent, accfuture))


def gen_dailydates_or_empty_for_year_opt_order_coff_accfut(pyear, decrescent=False, cutoff_date=None, accfuture=False):
  if pyear is None:
    return []
  try:
    pyear = int(pyear)
  except ValueError:
    return []
  firstdayinyear = datetime.date(year=pyear, month=1, day=1)
  lastday_in_range = datetime.date(year=pyear, month=12, day=31)
  cutoff_date = cnv.make_date_or_none(cutoff_date)
  if cutoff_date and cutoff_date < lastday_in_range:
    if cutoff_date >= firstdayinyear:
      lastday_in_range = cutoff_date
  if decrescent:
    startpoint = lastday_in_range
    finishpoint = firstdayinyear
    return gen_dailydates_bw_ini_fim_desc(startpoint, finishpoint, accfuture)
  startpoint = firstdayinyear
  finishpoint = lastday_in_range
  return gen_dailydates_bw_ini_fim_desc(startpoint, finishpoint, accfuture)


def get_gendailydates_or_empty_for_year_opt_order_coff_accfut(
    pyear, decrescent=False, cutoff_date=None, accfuture=False
):
  return list(gen_dailydates_or_empty_for_year_opt_order_coff_accfut(pyear, decrescent, cutoff_date, accfuture))


def gen_dailydates_for_current_year_opt_order_coff_accfut(decrescent=False, cutoff_date=None, accfuture=False):
  today = datetime.date.today()
  return gen_dailydates_or_empty_for_year_opt_order_coff_accfut(today.year, decrescent, cutoff_date, accfuture)


def get_gendailydates_for_current_year_opt_order_coff_accfut(decrescent=False, cutoff_date=None, accfuture=False):
  return list(gen_dailydates_for_current_year_opt_order_coff_accfut(decrescent, cutoff_date, accfuture))


def gen_dailydates_for_yearrange_or_empty_opt_order_coff_accfut(
    yearini, yearfim=None, decrescent=False, cutoff_date=None, accfuture=False
):
  """
  generates an iterator of daily dates for the years in-between yearini & yearfim
  Obs:
    1 this method uses for yearfim, if it is None, current year
    2 yearini cannot be a "non-date", if so, returns [] (the empty list)
    3 it accepts a cutoff_date which, if valid, overrides the last day date in yearfim
    4 it can work "for the future" if flag accept_future is True
    5 it does not swap yearini with yearfim if yearini > yearfim, if it is, empty [] is returned
      5-1 the notice above is because some functions in the module do the swapping, this does not
      5-2 the corresponding/accompanying unit-test should test this 'feature' of not-swapping
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
  first_date = datetime.date(year=yearini, month=1, day=1)
  last_date = datetime.date(year=yearfim, month=12, day=31)
  cutoff_date = cnv.make_date_or_none(cutoff_date)
  if cutoff_date:
    if first_date <= cutoff_date <= last_date:
      # cutoff_date is in between first & last dates, set it to last_date_in_yearfim
      last_date = cutoff_date
    elif cutoff_date <= first_date:
      # cutoff_date is below first_date_in_yearini, return [] (the empty list)
      return []
  if not accfuture:
    if first_date > today:
      return []
    if last_date > today:
      last_date = today
  if decrescent:
    gen_dailydates_bw_ini_fim_desc(first_date, last_date, accfuture)
  return gen_dailydates_bw_ini_fim_asc(first_date, last_date, accfuture)


def get_gendailydates_for_yearrange_or_empty_opt_order_coff_accfut(
    yearini, yearfim=None, decrescent=False, cutoff_date=None, accfuture=False
):
  return list(
    gen_dailydates_for_yearrange_or_empty_opt_order_coff_accfut(
      yearini, yearfim, decrescent, cutoff_date, accfuture
    )
  )


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
  return gen_dailydates_for_yearrange_or_empty_opt_order_coff_accfut(yearini, yearfim, decrescent, today)


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
  datelist = get_gendailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut('foo bar')
  print(len(datelist), datelist)
  datelist = get_gendailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut('2023-2')
  print(len(datelist), datelist)
  today = datetime.date.today()
  mo_m1_dt = today - relativedelta(months=1)
  print('mo_m1_dt', mo_m1_dt)
  datelist = get_gendailydates_for_yearrange_or_empty_opt_order_coff_accfut(
    2023, yearfim=None, decrescent=False, cutoff_date=None, accfuture=True
  )
  print(len(datelist), 'datelist', datelist)


def adhoc_test2():
  str_refmonth = 'bla foo'
  datelist = get_gendailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut(str_refmonth, decrescent=True)
  print(len(datelist), 'datelist', datelist)


def adhoc_test3():
  """
  returned_datelist = get_gendailydates_for_weekdate_opt_order(yesterday, decrescent=False, accfuture=True)
  print(n_days_in_a_week, len(returned_datelist))
  print(yesterday, returned_datelist[0])
  print(sixdays_a_yesterdar, returned_datelist[-1])

  """
  # t3 test week with cutoff & future
  today = datetime.date.today()
  yesterday = today - relativedelta(days=1)
  # n_days_in_a_week = 7
  # sixdays_a_yesterdar = yesterday + relativedelta(days=n_days_in_a_week - 1)
  # t3 gen_dailydates_for_weekdate_opt_order() with accfuture=True
  # t4 as t3 with accfuture=False
  returned_datelist = get_gendailydates_for_weekdate_opt_order(yesterday, decrescent=False, accfuture=False)
  # there should be only yesterday and today in returned_datelist, so 2 elements
  n_days_not_in_future_yet = 2
  print(n_days_not_in_future_yet, len(returned_datelist))
  print(yesterday, returned_datelist[0])
  print(today, returned_datelist[-1])
  datelist = get_gendailydates_for_lastweek_wo_today_opt_order()
  print(len(datelist), 'datelist', datelist)
  datelist = get_gendailydates_for_weekdate_opt_order(today, accfuture=True)
  print(len(datelist), 'asc datelist', datelist)
  datelist = get_gendailydates_for_weekdate_opt_order(today, decrescent=True, accfuture=True)
  print(len(datelist), 'desc datelist', datelist)


def process():
  pass


if __name__ == "__main__":
  """
  adhoctest3()
  process()
  """
  adhoc_test3()
