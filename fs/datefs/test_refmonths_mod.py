#!/usr/bin/env python3
"""


import fs.datefs.datefunctions as dtfs
from dateutil.relativedelta import relativedelta
"""
import datetime
import unittest
import fs.datefs.convert_to_date_wo_intr_sep_posorder as mkdt
import fs.datefs.refmonths_mod as rfm  # .calc_refmonth_plus_n
import fs.datefs.read_write_datelist_files_fs as rwdt  # .calc_refmonth_plus_n


class TestCaseDateFunctions(unittest.TestCase):

  def setUp(self):
    self.today = datetime.date.today()

  def test_build_refmonths(self):
    y, m = 2023, 11
    strdate = f'{y}-{m} bla blah'
    expect_date = datetime.date(year=y, month=m, day=1)
    returned_date = rfm.make_refmonth_or_none(strdate)
    # t1 unit-testing make_refmonth_or_none()
    self.assertEqual(returned_date, expect_date)
    returned_date = rfm.make_refmonth_or_current('bla foo')
    current_refmonthdate = self.today
    if current_refmonthdate.day != 1:
      current_refmonthdate = datetime.date(year=self.today.year, month=self.today.month, day=1)
    # t2 same as t1 but with make_refmonth_or_current()
    self.assertEqual(returned_date, current_refmonthdate)
    # reminding that strdate is not complete (notice the bla blah above) for the next subtest
    returned_date = mkdt.make_date_or_none(strdate)
    # t3 same as t2 but with common dates (not refmonthdates)
    self.assertIsNone(returned_date)
    returned_date = mkdt.make_date_or_today(strdate)
    today = datetime.date.today()
    # t4 same as t3 with today
    self.assertEqual(returned_date, today)

  def test_strdatelist_conversion_to_datelist(self):
    # t1, t2 & t3 test convert_strdatelist_to_datelist() (though this function belongs the 'read_write' module)
    expect_datelist, strdatelist = [], []
    y, m, d = 2023, 11, 11
    strdate = f'{y}-{m}-{d}'
    # append first strdate to strdatelist
    strdatelist.append(strdate)
    pdate = datetime.date(year=y, month=m, day=d)
    expect_datelist.append(pdate)
    # t1 subtest pdate has y, m & d
    self.assertEqual((y, m, d), (pdate.year, pdate.month, pdate.day))
    y, m, d = 2022, 12, 13
    strdate = f'{y}-{m}-{d}'
    # append second strdate to strdatelist
    strdatelist.append(strdate)
    pdate = datetime.date(year=y, month=m, day=d)
    expect_datelist.append(pdate)
    # t2 subtest with a different strdate
    self.assertEqual((y, m, d), (pdate.year, pdate.month, pdate.day))
    sep, posorder = '-', 'ymd'
    returned_datelist = rwdt.convert_strdatelist_to_datelist_w_sep_n_posorder(strdatelist, sep=sep, posorder=posorder)
    # t3 subtest checking equality of expect_datelist (made here) & returned_datelist (api-processed)
    self.assertEqual(expect_datelist, returned_datelist)

  def test_refmonths_with_attrs_obj(self):
    y, m, d = 2012, 2, 3
    attrs_obj = rfm.ClassWithYearMonthDay(year=y, month=m, day=d)
    expected_refmonthdate = attrs_obj.as_refmonthdate()
    pdate = datetime.date(year=y, month=m, day=d)
    returned_refmonthdate = rfm.make_refmonth_or_none(pdate)
    # t1 subtest refmonthdate also using ClassWithYearMonthDay.as_refmonthdate()
    self.assertEqual(expected_refmonthdate, returned_refmonthdate)
    returned_refmonthdate = rfm.make_refmonth_or_none(pdate)
    # t2 subtest make_refmonth_or_none() passing None expecting None
    returned_refmonthdate = rfm.make_refmonth_or_none(None)
    self.assertIsNone(returned_refmonthdate)
    # t3 same as t1 but sending in 'rubish' then expecting None
    returned_refmonthdate = rfm.make_refmonth_or_none('rubish')
    self.assertIsNone(returned_refmonthdate)
    # t3 same as t1 but sending in 'rubish' then expecting None
    returned_refmonthdate = rfm.make_refmonth_or_none('rubish')
    y, m, d = 2012, 2, 'rubish'
    attrs_obj = rfm.ClassWithYearMonthDay(year=y, month=m, day=d)
    expected_refmonthdate = attrs_obj.as_refmonthdate()
    pdate = datetime.date(year=y, month=m, day=1)
    returned_refmonthdate = rfm.make_refmonth_or_none(pdate)
    # t4 having 'rubish' on day via ClassWithYearMonthDay then expecting refmonthdate which depends on year & month
    self.assertEqual(expected_refmonthdate, returned_refmonthdate)
    strdate = f"{y}-{m} blah bla foo bar"
    returned_refmonthdate = rfm.make_refmonth_or_none(strdate)
    # t5 a variation of t4 but using make_refmonth_or_none(strdate) directly
    self.assertEqual(expected_refmonthdate, returned_refmonthdate)
    strdate = f"{y}-{m}blah bla foo bar"
    returned_refmonthdate = rfm.make_refmonth_or_none(strdate)
    # t6 a variation of t5 with a "sutle" difference in not having a space (gap) after month
    self.assertIsNone(returned_refmonthdate)
