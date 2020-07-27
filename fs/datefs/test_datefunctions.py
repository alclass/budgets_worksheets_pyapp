#!/usr/bin/env python3
'''
Unit Tests for datefunctions.py
'''
import datetime, unittest
import fs.datefs.datefunctions as dtfs

class TestCaseDateFunctions(unittest.TestCase):

  def test_returns_date_or_today(self):
    # 1 date exists
    stryear = '2020'; strmonth = '7'; strday = '3';
    strdate = '%s-%s-%s' %(stryear, strmonth, strday)
    expected_date = datetime.date(int(stryear), int(strmonth), int(strday))
    returned_date = dtfs.returns_date_or_today(strdate)
    self.assertEqual(expected_date, returned_date)
    # 2 date does not exist, datetime.date.today() should return
    stryear = '2020'; strmonth = '13'; strday = '3';
    strdate = '%s-%s-%s' %(stryear, strmonth, strday)
    expected_date = datetime.date.today()
    returned_date = dtfs.returns_date_or_today(strdate)
    self.assertEqual(expected_date, returned_date)

  def test_returns_date_or_None(self):
    # 1 date exists
    stryear = '2020'; strmonth = '7'; strday = '3';
    strdate = '%s-%s-%s' %(stryear, strmonth, strday)
    expected_date = datetime.date(int(stryear), int(strmonth), int(strday))
    returned_date = dtfs.returns_date_or_None(strdate)
    self.assertEqual(expected_date, returned_date)
    # 2 date does not exist, None should return
    stryear = '2020'; strmonth = '13'; strday = '3';
    strdate = '%s-%s-%s' %(stryear, strmonth, strday)
    returned_date = dtfs.returns_date_or_None(strdate)
    self.assertIsNone(returned_date)
    # 3 date does not exist, None should return
    strdate = 'bla blah'
    returned_date = dtfs.returns_date_or_None(strdate)
    self.assertIsNone(returned_date)

  def test_get_daterange_asc_or_desc(self):
    # 1 makes a descendent range
    ini_date = '2020-07-03'
    ini_date = dtfs.returns_date_or_today(ini_date)
    mid_date = '2020-07-04'
    mid_date = dtfs.returns_date_or_today(mid_date)
    fin_date = '2020-07-05'
    fin_date = dtfs.returns_date_or_today(fin_date)
    expected_daterange = [fin_date, mid_date, ini_date]
    returned_daterange = dtfs.get_daterange_asc_or_desc(ini_date, fin_date, makes_desc=True)
    self.assertEqual(expected_daterange, returned_daterange)
    # 2 makes an ascendent range
    expected_daterange = [ini_date, mid_date, fin_date]
    returned_daterange = dtfs.get_daterange_asc_or_desc(ini_date, fin_date, makes_desc=False)
    self.assertEqual(expected_daterange, returned_daterange)

  def test_get_daterange_in_the_future(self):
    # 1 makes a daterange not in the future and flag not set
    ini_date = '2020-07-03'
    ini_date = dtfs.returns_date_or_today(ini_date)
    mid_date = '2020-07-04'
    mid_date = dtfs.returns_date_or_today(mid_date)
    fin_date = '2020-07-05'
    fin_date = dtfs.returns_date_or_today(fin_date)
    expected_daterange = [fin_date, mid_date, ini_date]
    returned_daterange = dtfs.get_daterange(fin_date, ini_date)
    self.assertEqual(expected_daterange, returned_daterange)
    # 2 makes a daterange not in the future and flag set
    returned_daterange = dtfs.get_daterange(fin_date, ini_date, accept_future=True)
    self.assertEqual(expected_daterange, returned_daterange)
    # 3 makes a daterange in the future (with help of datetime.timedelta())
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    dayaftertomorrow = today + datetime.timedelta(days=2)
    expected_daterange = [tomorrow, dayaftertomorrow]
    returned_daterange = dtfs.get_daterange(tomorrow, dayaftertomorrow, accept_future=True)
    self.assertEqual(expected_daterange, returned_daterange)
    # 4 tries to make a daterange in the future not setting its parameter flag, [today] should return
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    dayaftertomorrow = today + datetime.timedelta(days=2)
    expected_daterange = [tomorrow, dayaftertomorrow] # notice NotEqual below
    returned_daterange = dtfs.get_daterange(tomorrow, dayaftertomorrow, accept_future=False)
    self.assertNotEqual(expected_daterange, returned_daterange)
    # 5 former tries expected_daterange should be [today]
    self.assertEqual([today], returned_daterange)

  def test_convert_date_to_mmddyyyy_str_or_None(self):
    # 1 use a date that exists
    pdate = '2020-07-03'
    pdate = dtfs.returns_date_or_today(pdate)
    expected_strdate = '07-03-2020'
    returned_strdate = dtfs.convert_date_to_mmddyyyy_str_or_None(pdate)
    self.assertEqual(expected_strdate, returned_strdate)
    # 2 use a date that exists on former century
    pdate = '1997-1-31'
    pdate = dtfs.returns_date_or_today(pdate)
    expected_strdate = '01-31-1997'
    returned_strdate = dtfs.convert_date_to_mmddyyyy_str_or_None(pdate)
    self.assertEqual(expected_strdate, returned_strdate)
    # 3 use a date that does not exist
    pdate = '1997-1-32'
    pdate = dtfs.returns_date_or_None(pdate)
    returned_strdate = dtfs.convert_date_to_mmddyyyy_str_or_None(pdate)
    self.assertIsNone(returned_strdate)

  def test_sort_asc_or_desc_datelist(self):
    unordered = []
    d1 = datetime.date(2020, 4, 15)
    unordered.append(d1)
    d2 = datetime.date(2020, 2, 4)
    unordered.append(d2)
    d3 = datetime.date(2020, 3, 11)
    unordered.append(d3)
    d4 = datetime.date(2019, 1, 1)
    unordered.append(d4)
    expected_asc_ordered = [d4, d2, d3, d1]
    returned_asc_ordered = dtfs.sort_datelist_asc(unordered)
    self.assertEqual(expected_asc_ordered, returned_asc_ordered)
    expected_desc_ordered = [d1, d3, d2, d4]
    returned_desc_ordered = dtfs.sort_datelist_desc(unordered)
    self.assertEqual(expected_desc_ordered, returned_desc_ordered)

  def prepare_datelist_uniq_n_in_desc_order(self):
    datelist = []
    d = 'blah bla'
    datelist.append(d)
    d1 = datetime.date(2020, 3, 11)
    datelist.append(d1)
    d3 = '2020-5-2'
    d3conv = datetime.date(2020, 5, 2)
    datelist.append(d3)
    datelist.append(d3)
    d2 = datetime.date(2020, 4, 15)
    datelist.append(d2)
    datelist.append(d2)
    datelist.append(d2)
    expected_prepdatelist = [d3conv, d2, d1]
    returned_prepdatelist = dtfs.prepare_datelist_uniq_n_in_desc_order(datelist)
    self.assertEqual(expected_prepdatelist, returned_prepdatelist)
