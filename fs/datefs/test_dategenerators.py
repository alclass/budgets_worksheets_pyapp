#!/usr/bin/env python3
"""
fs/datefs/test_dategenerators.py
  unit-tests to fs/datefs/dategenerators functions.

As of 2023-12-08 there are 7 tests and about 30 "subtests" (input/output hypotheses)
"""
import calendar
import collections
import datetime
from dateutil.relativedelta import relativedelta
import unittest
import fs.datefs.dategenerators as gendt
nt_dtymd_constr = collections.namedtuple('NTymd', field_names=['year', 'month', 'day'])
nt_dtym_refmo_constr = collections.namedtuple('NTrefmo', field_names=['year', 'month'])


class Test(unittest.TestCase):

  def setUp(self):
    self.today = datetime.date.today()

  def test_build_dates_n_refmonths_1(self):
    # t1 pass a ymd namedtuple and expect a datetime.date back
    y, m, d = 2023, 11, 11
    ntdate = nt_dtymd_constr(year=y, month=m, day=d)
    exp_date = datetime.date(year=y, month=m, day=d)
    ret_date = gendt.make_date_or_none(ntdate)
    self.assertEqual(exp_date, ret_date)
    # t2 variation of t1, ie the namedtuple is not the created datetime.date
    self.assertNotEqual(ntdate, ret_date)
    # t3 pass a non-dateable value and expect None
    ret_date = gendt.make_date_or_none('bla foo')
    self.assertIsNone(ret_date)
    # t4 pass a non-dateable value and expect 'today'
    ret_date = gendt.make_date_or_today('bla foo')
    self.assertEqual(self.today, ret_date)
    nt_refmo = nt_dtym_refmo_constr(year=y, month=m)
    exp_refmo = datetime.date(year=y, month=m, day=1)
    # t5 same as t1 but with refmonth which needs only year & month
    ret_refmo = gendt.make_refmonth_or_none(nt_refmo)
    self.assertEqual(exp_refmo, ret_refmo)
    # t6 sends in a non-refmonthable and expects None
    ret_refmo = gendt.make_refmonth_or_none('bla bar')
    self.assertIsNone(ret_refmo)
    # t7 sends in a non-refmonthable and expects current refmonth
    ret_refmo = gendt.make_refmonth_or_current('bla bar')
    exp_refmo = self.today
    if exp_refmo.day != 1:
      exp_refmo = datetime.date(year=exp_refmo.year, month=exp_refmo.month, day=1)
    self.assertEqual(exp_refmo, ret_refmo)

  def test_build_dates_n_refmonths_2(self):
    # t1 unit-testing make_date_or_none() & make_date_or_today()
    y, m, d = 2023, 11, 11
    anystrdate = f'{y}-{m}-{d}'
    expect_date = datetime.date(year=y, month=m, day=d)
    returned_date = gendt.make_date_from_str_or_none(anystrdate)
    self.assertEqual(returned_date, expect_date)
    returned_date = gendt.make_date_or_none(anystrdate)
    self.assertEqual(returned_date, expect_date)
    # t2 unit-testing make_refmonth_or_none() & make_refmonth_or_current()
    y, m = 2023, 11
    anystrdate = f'{y}-{m} bla bla'
    expect_date = datetime.date(year=y, month=m, day=1)
    returned_date = gendt.make_refmonth_or_none(anystrdate)
    self.assertEqual(returned_date, expect_date)
    returned_date = gendt.make_refmonth_or_current('bla foo')
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

  def test_gen_dateranges_weeks(self):
    # t1 gen_dailydates_for_lastweek_opt_order()
    # ie, generates one whole past week with its 7 days PLUS today as an 8th day
    sevendaysbefore = self.today - relativedelta(days=7)
    exp_datelist = []
    ret_datelist = []
    idate = sevendaysbefore
    for pdate in gendt.gen_dailydates_for_lastweek_opt_order():
      exp_datelist.append(idate)
      idate = idate + relativedelta(days=1)
      ret_datelist.append(pdate)
    self.assertEqual(exp_datelist, ret_datelist)
    self.assertEqual(sevendaysbefore, ret_datelist[0])
    self.assertEqual(self.today, ret_datelist[-1])
    # len is 7 + 1 for the interator range is inconclusive
    # ie, in "range(dateini, datefim)", datefim is inconcluded
    n_days = 8
    self.assertEqual(n_days, len(ret_datelist))
    # t2 get_gendailydates_for_lastweek_wo_today_opt_order()
    # ie, generates one whole past week with its 7 days NOT INCLUDING today as an 8th day
    ret2_datelist = gendt.get_gendailydates_for_lastweek_wo_today_opt_order()
    n_days = 7
    self.assertEqual(n_days, len(ret2_datelist))
    yesterday = self.today - relativedelta(days=1)
    self.assertEqual(yesterday, ret2_datelist[-1])
    self.assertEqual(sevendaysbefore, ret2_datelist[0])

  def test_gen_dateranges_upto_months_1(self):
    # t1 gen_dailydates_bw_ini_fim_opt_order() choosing one whole month range
    y, m, d = 2023, 10, 1
    ini_strdate = f'{y}-{m}-{d}'
    inidate = datetime.date(year=y, month=m, day=d)
    y, m, d = 2023, 10, 31
    fim_strdate = f'{y}-{m}-{d}'
    fimdate = datetime.date(year=y, month=m, day=d)
    exp_datelist, ret_datelist = [], []
    genfunc = gendt.gen_dailydates_bw_ini_fim_opt_order(ini_strdate, fim_strdate)
    for i, pdate in enumerate(genfunc):
      idate = inidate + relativedelta(days=i)
      exp_datelist.append(idate)
      ret_datelist.append(pdate)
    self.assertEqual(ret_datelist, exp_datelist)
    self.assertEqual(ret_datelist[-1], fimdate)
    self.assertEqual(ret_datelist[0], inidate)
    ret_asc_datelist = ret_datelist
    # t2 same as t1 but descending (ie decrescent=True)
    tmpdate = inidate
    inidate = fimdate
    fimdate = tmpdate
    exp_datelist, ret_datelist = [], []
    genfunc = gendt.gen_dailydates_bw_ini_fim_opt_order(ini_strdate, fim_strdate, decrescent=True)
    for i, pdate in enumerate(genfunc):
      idate = inidate - relativedelta(days=i)
      exp_datelist.append(idate)
      ret_datelist.append(pdate)
    self.assertEqual(ret_datelist, exp_datelist)
    self.assertEqual(ret_datelist[0], inidate)
    self.assertEqual(ret_datelist[-1], fimdate)
    # t3 get_gendailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut(str_refmonth)
    # previous tests spanned upon a whole month range,
    # now this one uses refmonth itself directly
    ret_desc_datelist = ret_datelist
    str_refmonth = f'{y}-{m}'
    ret_datelist = gendt.get_gendailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut(str_refmonth)
    self.assertEqual(ret_asc_datelist, ret_datelist)
    # t4 same as t3 but with desc ie decrescent=True
    ret_datelist = gendt.get_gendailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut(
      str_refmonth, decrescent=True
    )
    self.assertEqual(ret_desc_datelist, ret_datelist)
    # t5 same as t3 but with current refmonthdate and allowing "future"
    ret_datelist = gendt.get_gendailydates_for_current_refmonth_opt_order_cday_accfut(accfuture=True)
    curr_refmo = gendt.make_refmonth_or_current()
    _, n_days = calendar.monthrange(curr_refmo.year, curr_refmo.month)
    last_day_inmo = datetime.date(year=curr_refmo.year, month=curr_refmo.month, day=n_days)
    self.assertEqual(n_days, len(ret_datelist))
    self.assertEqual(curr_refmo, ret_datelist[0])
    self.assertEqual(last_day_inmo, ret_datelist[-1])
    # t6 same as t5 but decrescent and NOT allowing "future"
    ret_datelist = gendt.get_gendailydates_for_current_refmonth_opt_order_cday_accfut(decrescent=True, accfuture=False)
    self.assertEqual(self.today.day, len(ret_datelist))
    self.assertEqual(self.today, ret_datelist[0])
    self.assertEqual(curr_refmo, ret_datelist[-1])

  def test_gen_dateranges_upto_months_2(self):
    # t1 generates dates for last month passing its refmonthdate
    mo_m1_dt = self.today - relativedelta(months=1)
    firstdate = datetime.date(year=mo_m1_dt.year, month=mo_m1_dt.month, day=1)
    _, n_days_inmo = calendar.monthrange(mo_m1_dt.year, mo_m1_dt.month)
    lastdate = datetime.date(year=mo_m1_dt.year, month=mo_m1_dt.month, day=n_days_inmo)
    delta = lastdate - firstdate
    n_days_in_bw = delta.days + 1
    str_refmonth = f"{mo_m1_dt.year}-{mo_m1_dt.month}"
    datelist = gendt.get_gendailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut(str_refmonth)
    self.assertEqual(n_days_in_bw, n_days_inmo)
    self.assertEqual(n_days_in_bw, len(datelist))
    self.assertEqual(datelist[0], firstdate)
    self.assertEqual(datelist[-1], lastdate)
    # t2 same as t1 but letting it fall back to its default (still last month)
    str_refmonth = 'bla foo bar'  # sends in rubish to get lastmonth
    datelist = gendt.get_gendailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut(str_refmonth)
    self.assertEqual(n_days_in_bw, len(datelist))
    self.assertEqual(datelist[0], firstdate)
    self.assertEqual(datelist[-1], lastdate)
    # t3 same as t2 but desc ie with decrescent=True
    datelist = gendt.get_gendailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut(str_refmonth, decrescent=True)
    self.assertEqual(n_days_in_bw, len(datelist))
    self.assertEqual(datelist[0], lastdate)
    self.assertEqual(datelist[-1], firstdate)
    n_days = 15
    cutoff_date = datetime.date(year=mo_m1_dt.year, month=mo_m1_dt.month, day=n_days)
    # t4 same as t3 but with cutoff_day
    datelist = gendt.get_gendailydates_for_refmonth_or_lastmonth_opt_order_cday_accfut(str_refmonth, cutoff_day=n_days)
    self.assertEqual(n_days, len(datelist))
    self.assertEqual(datelist[0], firstdate)
    self.assertEqual(datelist[-1], cutoff_date)

  def test_gen_dateranges_upto_months_3(self):
    # t1 generates dates for lastweek
    seven_days_before = self.today - relativedelta(days=7)
    idate = seven_days_before
    exp_datelist, ret_datelist = [], []
    for i, pdate in enumerate(gendt.gen_dailydates_for_lastweek_opt_order()):
      exp_datelist.append(idate)
      idate = idate + relativedelta(days=1)
      ret_datelist.append(pdate)
    self.assertEqual(exp_datelist, ret_datelist)
    self.assertEqual(self.today, ret_datelist[-1])
    self.assertEqual(seven_days_before, ret_datelist[0])
    # t2 same as t1 but desc ie with decrescent=True
    ret2_datelist = gendt.get_gendailydates_for_lastweek_opt_order(decrescent=True)
    exp_datelist.reverse()
    self.assertEqual(exp_datelist, ret2_datelist)
    self.assertEqual(self.today, ret2_datelist[0])
    self.assertEqual(seven_days_before, ret2_datelist[-1])
    # t3 same as t2 but with 7 days (without 'today') instead of 8 and back to asc ie decrescent=False
    ret3_datelist = gendt.get_gendailydates_for_lastweek_wo_today_opt_order()
    # reverse it back
    exp_datelist.reverse()
    # remove the last element which should be 'today'
    exp_today = exp_datelist.pop()
    self.assertEqual(self.today, exp_today)
    self.assertEqual(exp_datelist, ret3_datelist)
    yesterday = self.today - relativedelta(days=1)
    self.assertEqual(yesterday, ret3_datelist[-1])
    self.assertEqual(seven_days_before, ret3_datelist[0])

  def test_gen_dateranges_beyond_months(self):
    # t1 gen_dailydates_f_yearini_t_today_or_empty_opt_order()
    y = 2022
    inidate = datetime.date(year=y, month=1, day=1)
    idate = inidate
    exp_datelist, ret_datelist = [], []
    for i, pdate in enumerate(gendt.gen_dailydates_f_yearini_t_today_or_empty_opt_order(y)):
      exp_datelist.append(idate)
      idate = idate + relativedelta(days=1)
      ret_datelist.append(pdate)
    # t2 gen_dailydates_for_yearrange_or_empty_opt_order_coff_accfut()
    y = 2023
    ret_fullyear_list = []
    # accept future
    for pdate in gendt.gen_dailydates_for_yearrange_or_empty_opt_order_coff_accfut(y, y, False, None, accfuture=True):
      ret_fullyear_list.append(pdate)
    self.assertEqual(365, len(ret_fullyear_list))
    # do not accept future
    # t3 same as t2 but with accfuture=True
    ret_year_no_future_allowed_datelist = []
    for pdate in gendt.gen_dailydates_for_yearrange_or_empty_opt_order_coff_accfut(y, y, False, None, accfuture=False):
      ret_year_no_future_allowed_datelist.append(pdate)
    exp_datelist = list(filter(lambda d: d <= self.today, ret_fullyear_list))
    self.assertEqual(ret_year_no_future_allowed_datelist, exp_datelist)
