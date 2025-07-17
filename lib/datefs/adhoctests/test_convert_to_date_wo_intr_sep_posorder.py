#!/usr/bin/env python3
"""
fs/datefs/test_convert_to_date_wo_intr_sep_posorder.py
  Unit Tests for convert_to_date_wo_intr_sep_posorder.py

Obs/reminders:
  a) "wo" is abbreviation for "without"
  b) the target module converts strings such as yyyymmdd or yyyy-mm-dd or
     objs that implement year, month & day into datetime. date's
  c) there is another module that converts to date using sep & posorder

import fs.datefs.datefunctions as dtfs
"""
import datetime
from dateutil.relativedelta import relativedelta
import unittest
import lib.datefs.convert_to_date_wo_intr_sep_posorder as mkdt


class ClassWithYearMonthDay:
  def __init__(self, y, m, d):
    self.year = y or None
    self.month = m or None
    self.day = d or None

  def as_date(self):
    try:
      dt = datetime.date(self.year, self.month, self.day)
      return dt
    except (TypeError, ValueError):
      pass
    return None


class TestCaseDateFunctions(unittest.TestCase):

  def setUp(self):
    self.today = datetime.date.today()

  def test_returns_date_or_today_or_none(self):
    # t1 date exists, ie it's makeable
    y, m, d = 2020, 7, 3
    strdate = f"{y}-{m}-{d}"
    returned_date = mkdt.make_date_or_none(strdate)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(expected_date, returned_date)
    # t2 same as t1 but expecting None
    y, m, d = 2020, 7, 32
    strdate = f"{y}-{m}-{d}"
    returned_date = mkdt.make_date_or_none(strdate)
    self.assertIsNone(returned_date)
    # t3 same as t1 but expecting 'today'
    returned_date = mkdt.make_date_or_today(strdate)
    self.assertEqual(self.today, returned_date)
    # t4 sends in 'rubish' to make_date, expect None
    returned_date = mkdt.make_date_or_none('foo bar')
    self.assertIsNone(returned_date)
    # t5 sends in 'rubish' to make_date, expect today
    returned_date = mkdt.make_date_or_today('foo bar')
    self.assertEqual(self.today, returned_date)
    # t6 sends in a strdate with separators ie yyyymmdd instead of yyyy-mm-dd (dd & mm must be 2-digit)
    y, m, d = 2017, 5, 1
    strdate = f"{y}{m:02}{d:02}"
    returned_date = mkdt.make_date_or_none(strdate)
    expected_date = datetime.date(year=y, month=m, day=d)
    self.assertEqual(expected_date, returned_date)
    # t7 same as t6 now expecting None returned back
    y, m, d = 2017, 5, 41
    strdate = f"{y}{m:02}{d:02}"
    returned_date = mkdt.make_date_or_none(strdate)
    self.assertIsNone(returned_date)
    # t8 same as t6 (which has a valid date) but without zfill=2 for mm (which makes it invalid)
    # (ie zfill=2 means adding the leftzero, if needed, for 2-digit dd & mm)
    y, m, d = 2017, 5, 1
    strdate = f"{y}{m}{d}"
    returned_date = mkdt.make_date_or_none(strdate)
    self.assertIsNone(returned_date)

  def test_returns_date_from_attrobjs(self):
    # t1 date exists within an object that implements year, month & day
    y, m, d = 2020, 7, 3
    expected_date = datetime.date(year=y, month=m, day=d)
    attrs_obj = ClassWithYearMonthDay(y, m, d)
    returned_date = mkdt.make_date_or_none(attrs_obj)
    self.assertEqual(expected_date, returned_date)
    # t2 same as t1 testing with object's method as_date()
    self.assertEqual(attrs_obj.as_date(), returned_date)
    # t3 same as t1 but sending in a non-existent date
    y, m, d = 2020, 7, None
    attrs_obj = ClassWithYearMonthDay(y, m, d)
    returned_date = mkdt.make_date_or_none(attrs_obj)
    self.assertIsNone(returned_date)
    # t4 same as t3 testing with object's method as_date()
    self.assertIsNone(attrs_obj.as_date())
    # t5 using a datetime.datetime as input
    y, m, d = 1111, 1, 1  # this is a valid date!
    dtdt = datetime.datetime(y, m, d)
    expected_date = datetime.date(year=y, month=m, day=d)
    returned_date = mkdt.make_date_or_none(dtdt)
    self.assertEqual(expected_date, returned_date)

  def test_with_today(self):
    # t1 stringifying 'today'
    strdate = str(self.today)
    returned_date = mkdt.make_date_or_none(strdate)
    self.assertEqual(self.today, returned_date)
    # t2 same as t1 but objectifying 'today' via ClassWithYearMonthDay
    y, m, d = self.today.year, self.today.month, self.today.day
    attrs_obj = ClassWithYearMonthDay(y, m, d)
    returned_date = mkdt.make_date_or_none(attrs_obj)
    self.assertEqual(self.today, returned_date)
    # t3 is a negative test, ie yesterday is not today
    yesterday = self.today - relativedelta(days=1)
    self.assertNotEqual(yesterday, returned_date)

  def test_build_dates_n_refmonths_1(self):
    # t1 pass a ymd namedtuple and expect a datetime.date back
    y, m, d = 2023, 11, 11
    ntdate = mkdt.nt_dtymd_constr(year=y, month=m, day=d)
    exp_date = datetime.date(year=y, month=m, day=d)
    ret_date = mkdt.make_date_or_none(ntdate)
    self.assertEqual(exp_date, ret_date)
    # t2 variation of t1, ie the namedtuple is not the created datetime.date
    self.assertNotEqual(ntdate, ret_date)
    # t3 pass a non-dateable value and expect None
    ret_date = mkdt.make_date_or_none('bla foo')
    self.assertIsNone(ret_date)
    # t4 pass a non-dateable value and expect 'today'
    ret_date = mkdt.make_date_or_today('bla foo')
    self.assertEqual(self.today, ret_date)
    nt_refmo = mkdt.nt_dtym_refmo_constr(year=y, month=m)
    exp_refmo = mkdt.datetime.date(year=y, month=m, day=1)
    # t5 same as t1 but with refmonth which needs only year & month
    ret_refmo = mkdt.make_refmonth_or_none(nt_refmo)
    self.assertEqual(exp_refmo, ret_refmo)
    # t6 sends in a non-refmonthable and expects None
    ret_refmo = mkdt.make_refmonth_or_none('bla bar')
    self.assertIsNone(ret_refmo)
    # t7 sends in a non-refmonthable and expects current refmonth
    ret_refmo = mkdt.make_refmonth_or_current('bla bar')
    exp_refmo = self.today
    if exp_refmo.day != 1:
      exp_refmo = datetime.date(year=exp_refmo.year, month=exp_refmo.month, day=1)
    self.assertEqual(exp_refmo, ret_refmo)
    # t1 unit-testing make_date_or_none() & make_date_or_today()
    y, m, d = 2023, 11, 11
    anystrdate = f'{y}-{m}-{d}'
    expect_date = datetime.date(year=y, month=m, day=d)
    returned_date = mkdt.make_date_from_str_or_none(anystrdate)
    self.assertEqual(returned_date, expect_date)
    returned_date = mkdt.make_date_or_none(anystrdate)
    self.assertEqual(returned_date, expect_date)

  def test_build_dates_n_refmonths_2(self):
    # t2 unit-testing make_refmonth_or_none() & make_refmonth_or_current()
    y, m = 2023, 11
    anystrdate = f'{y}-{m} bla bla'
    expect_date = datetime.date(year=y, month=m, day=1)
    returned_date = mkdt.make_refmonth_or_none(anystrdate)
    self.assertEqual(returned_date, expect_date)
    returned_date = mkdt.make_refmonth_or_current('bla foo')
    current_refmonthdate = self.today
    if current_refmonthdate.day != 1:
      current_refmonthdate = datetime.date(year=self.today.year, month=self.today.month, day=1)
    self.assertEqual(returned_date, current_refmonthdate)
    # reminding that anystrdate is not complete
    # t3 same as t1 but with the str that was used for refmonth with day
    returned_date = gendt.make_date_or_none(anystrdate)
    self.assertIsNone(returned_date)
    returned_date = gendt.make_date_or_today(anystrdate)
    today = datetime.date.today()
    self.assertEqual(returned_date, today)
    # t4 test convert_strdatelist_to_datelist()
    expect_datelist, strdatelist = [], []
    y, m, d = 2023, 11, 11
    anystrdate = f'{y}-{m}-{d}'
    strdatelist.append(anystrdate)
    pdate = datetime.date(year=y, month=m, day=d)
    expect_datelist.append(pdate)
    y, m, d = 2022, 12, 13
    anystrdate = f'{y}-{m}-{d}'
    strdatelist.append(anystrdate)
    pdate = datetime.date(year=y, month=m, day=d)
    expect_datelist.append(pdate)
    returned_datelist = gendt.convert_strdatelist_to_datelist(strdatelist)
    self.assertEqual(returned_datelist, expect_datelist)
