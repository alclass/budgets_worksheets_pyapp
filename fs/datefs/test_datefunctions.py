#!/usr/bin/env python3
"""
"""
import datetime
from dateutil.relativedelta import relativedelta
import unittest
import fs.datefs.years_date_functions as dtfs


class TestCaseDateFunctions(unittest.TestCase):

  def setUp(self):
    self.today = datetime.date.today()

  def test_decades(self):
    # t1 subtest the default decade year (passing in None) for decade
    current_year = self.today.year
    expected_dec_year = current_year // 10 * 10
    returned_dec_year = dtfs.get_decade_year_tenmultiplebased_from_or_current()
    self.assertEqual(expected_dec_year, returned_dec_year)
    expected_dec_date = datetime.date(year=expected_dec_year, month=1, day=1)
    returned_dec_date = dtfs.get_first_date_in_decade_year_tenmultiplebased_from_or_current()
    # t2 same as t1 but with decade date instead of decade year
    self.assertEqual(expected_dec_date, returned_dec_date)
    # t3 same as t2 but passing in 'rubish' then expecting None
    returned_dec_date = dtfs.get_first_date_in_decade_year_tenmultiplebased_from_or_none()
    self.assertIsNone(returned_dec_date)


  def ztest_convert_strdatetime_to_datetime_or_none(self):
    strdatetime = '2012-12-12 12:12:12.123'
    expected_datetime = datetime.datetime(
      2012, 12, 12, 12, 12, 12,  123000
    )
    returned_datetime = dtfs.convert_str_or_attrsobj_to_datetime_or_none(strdatetime)
    self.assertEqual(expected_datetime, returned_datetime)
    strdatetime = '2012-12-12 12:12:12'
    expected_datetime = datetime.datetime(
      2012, 12, 12, 12, 12, 12
    )
    returned_datetime = dtfs.convert_str_or_attrsobj_to_datetime_or_none(strdatetime)
    self.assertEqual(expected_datetime, returned_datetime)
    strdatetime = None
    returned_datetime = dtfs.convert_str_or_attrsobj_to_datetime_or_none(strdatetime)
    self.assertIsNone(returned_datetime)
    strdatetime = 'bla'
    returned_datetime = dtfs.convert_str_or_attrsobj_to_datetime_or_none(strdatetime)
    self.assertIsNone(returned_datetime)
    strdatetime = '2012-13-12 12:12:12'
    returned_datetime = dtfs.convert_str_or_attrsobj_to_datetime_or_none(strdatetime)
    self.assertIsNone(returned_datetime)
    strdatetime = '2222-12-12 12:12:12'
    expected_datetime = datetime.datetime(
      2222, 12, 12, 12, 12, 12)
    returned_datetime = dtfs.convert_str_or_attrsobj_to_datetime_or_none(strdatetime)
    self.assertEqual(expected_datetime, returned_datetime)
