#!/usr/bin/env python3
"""
  docstring
"""
from lib.datefs.years_date_functions import *


def adhoc_test1():
  strdate = '2020-7-14'
  mmddyyyy = convert_date_to_mmddyyyy_str_or_none(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = '2020.7.14'
  mmddyyyy = convert_date_to_mmddyyyy_str_or_none(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = '2020/7/14'
  mmddyyyy = convert_date_to_mmddyyyy_str_or_none(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = '20200714'
  mmddyyyy = convert_date_to_mmddyyyy_str_or_none(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = 'bla'
  mmddyyyy = convert_date_to_mmddyyyy_str_or_none(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = '2020714'
  mmddyyyy = convert_date_to_mmddyyyy_str_or_none(strdate)
  print(strdate, '=>', mmddyyyy)
  inistrdate = '20200717'
  fimstrdate = '20200720'
  daterange = get_daterange(inistrdate, fimstrdate)
  for pdate in daterange:
    print('date', pdate, 'weekday', is_date_weekend(pdate))
  departdate = '20200719'
  pdate = get_date_or_previous_monday_to_friday(departdate)
  print('departdate', departdate, ' =>', pdate)
  strdt = '2020-07-23 13:02:43.561'
  pdate = convert_generic_yyyymmdd_strdate_to_dtdate_or_none(strdt)
  print('pdate', pdate)


def adhoc_test2():
  """

  :return:
  """
  stryear = '2020'
  strmonth = '7'
  strday = '3'
  strdate = '%s-%s-%s' % (stryear, strmonth, strday)
  expected_date = datetime.date(int(stryear), int(strmonth), int(strday))
  returned_date = returns_date_or_today(strdate)
  print('expected_date', expected_date, 'returned_date', returned_date)
  stryear = '2020'
  strmonth = '13'
  strday = '3'
  strdate = '%s-%s-%s' % (stryear, strmonth, strday)
  expected_date = None
  returned_date = returns_date_or_today(strdate)
  print('expected_date', expected_date, 'returned_date', returned_date)


def adhoc_test3():
  unordered = []
  d1 = datetime.date(2020, 4, 15)
  unordered.append(d1)
  d2 = datetime.date(2020, 2, 4)
  unordered.append(d2)
  d3 = datetime.date(2020, 3, 11)
  unordered.append(d3)
  asc_ordered = sort_datelist_asc(unordered)
  desc_ordered = sort_datelist_desc(unordered)
  print('unordered', unordered)
  print('asc_ordered', asc_ordered)
  print('desc_ordered', desc_ordered)


def adhoc_test4():
  datelist = []
  d = 'blah bla'
  datelist.append(d)
  d = datetime.date(2020, 3, 11)
  datelist.append(d)
  d = '2020-5-2'
  datelist.append(d)
  datelist.append(d)
  d = datetime.date(2020, 4, 15)
  datelist.append(d)
  datelist.append(d)
  datelist.append(d)
  prepdatelist = trans_datelist_uniq_n_desc(datelist)
  print(datelist)
  print(prepdatelist)


def adhoc_test5():
  strdatetime = '2012-12-12 12:12:12.123'
  pdatetime = convert_str_or_attrsobj_to_datetime_or_none(strdatetime)
  print('strdatetime', strdatetime, '=>', 'pdatetime', pdatetime)


def process():
  fname_to_interpol = 'adhoctest3%d()'
  for i in range(1, 6):
    fname = fname_to_interpol %i
    print('-'*40)
    print ('Function: ', fname)
    print('-'*40)
    eval(fname)


if __name__ == "__main__":
  process()
