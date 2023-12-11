#!/usr/bin/env python3
"""
fs/datefs/test_dategenerators.py
  unit-tests to fs/datefs/dategenerators functions.

As of 2023-12-08 there are 7 tests and about 30 "subtests" (input/output hypotheses)

import collections
"""
import calendar
import datetime
from dateutil.relativedelta import relativedelta
import unittest
import fs.datefs.dategenerators as gendt
import fs.datefs.refmonths_mod as rfm


class Test(unittest.TestCase):

  def setUp(self):
    self.today = datetime.date.today()

  def test_gen_dateranges_weeks(self):
    # t1 gen_dailydates_for_lastweek_incl_today_opt_order()
    # ie, generates one whole past week with its 7 but today is included as its last day
    # @see below function version that ends on yesterday
    n_days_in_a_week = 7
    sevendaysbefore = self.today - relativedelta(days=n_days_in_a_week-1)
    exp_datelist = []
    ret_datelist = []
    idate = sevendaysbefore
    for pdate in gendt.gen_dailydates_for_lastweek_incl_today_opt_order():
      exp_datelist.append(idate)
      idate = idate + relativedelta(days=1)
      ret_datelist.append(pdate)
    self.assertEqual(n_days_in_a_week, len(ret_datelist))
    self.assertEqual(exp_datelist, ret_datelist)
    self.assertEqual(sevendaysbefore, ret_datelist[0])
    self.assertEqual(self.today, ret_datelist[-1])
    self.assertEqual(n_days_in_a_week, len(ret_datelist))
    # t2 same as t1 but without 'today', ie get_gendailydates_for_lastweek_wo_today_opt_order()
    # ie, generates one whole past week with its 7 days having 'yesterday' as its last day
    ret2_datelist = gendt.get_gendailydates_for_lastweek_wo_today_opt_order()
    self.assertEqual(n_days_in_a_week, len(ret2_datelist))
    yesterday = self.today - relativedelta(days=1)
    self.assertEqual(yesterday, ret2_datelist[-1])
    # "_b_" means "before"
    sixdays_b_yesterdar = yesterday - relativedelta(days=n_days_in_a_week-1)
    self.assertEqual(sixdays_b_yesterdar, ret2_datelist[0])
    yesterday = self.today - relativedelta(days=1)
    # t3 gen_dailydates_for_weekdate_opt_order() with accfuture=True ie "accept future"
    returned_datelist = gendt.get_gendailydates_for_weekdate_opt_order(
      yesterday, decrescent=False, cutoff_idx=None, accfuture=True
    )
    self.assertEqual(n_days_in_a_week, len(returned_datelist))
    self.assertEqual(yesterday, returned_datelist[0])
    # "_a_" means "after"
    sixdays_a_yesterdar = yesterday + relativedelta(days=n_days_in_a_week-1)
    self.assertEqual(sixdays_a_yesterdar, returned_datelist[-1])
    # t4 same as t3 with accfuture=False
    returned_datelist = gendt.get_gendailydates_for_weekdate_opt_order(
      yesterday, decrescent=False, cutoff_idx=None, accfuture=False
    )
    # there should be only yesterday and today in returned_datelist, so 2 elements (the others are in future)
    n_days_not_in_future_yet = 2
    self.assertEqual(n_days_not_in_future_yet, len(returned_datelist))
    self.assertEqual(yesterday, returned_datelist[0])
    self.assertEqual(self.today, returned_datelist[-1])
    # t5 same as t4 with cutoff_idx=0 (meaning it's picking up only one day from the list of the subtest above)
    cutoff_idx = 0
    returned_datelist = gendt.get_gendailydates_for_weekdate_opt_order(
      yesterday, decrescent=False, cutoff_idx=cutoff_idx, accfuture=False
    )
    self.assertEqual(n_days_not_in_future_yet, len(returned_datelist))
    self.assertEqual(yesterday, returned_datelist[0])
    # t5 subtesting parameter decrescent=True along side with list.reverse()
    ret_datelist_asc = gendt.get_gendailydates_for_weekdate_opt_order(
      self.today, decrescent=False, cutoff_idx=None, accfuture=True
    )
    # notice that date_ini (today in this case) is the same, only the element order gets changed (reversed)
    ret_datelist_desc = gendt.get_gendailydates_for_weekdate_opt_order(
      self.today, decrescent=True, cutoff_idx=None, accfuture=True
    )
    self.assertEqual(ret_datelist_asc[0], ret_datelist_desc[-1])
    self.assertEqual(ret_datelist_asc[-1], ret_datelist_desc[0])
    ret_datelist_asc.reverse()
    self.assertEqual(ret_datelist_asc, ret_datelist_desc)

  def test_gen_dateranges_upto_months_1(self):
    # t1 gen_dailydates_or_empty_bw_ini_fim_opt_order() choosing one whole month range
    y, m, d = 2023, 10, 1
    ini_strdate = f'{y}-{m}-{d}'
    inidate = datetime.date(year=y, month=m, day=d)
    y, m, d = 2023, 10, 31
    fim_strdate = f'{y}-{m}-{d}'
    fimdate = datetime.date(year=y, month=m, day=d)
    exp_datelist, ret_datelist = [], []
    genfunc = gendt.gen_dailydates_or_empty_bw_ini_fim_opt_order(ini_strdate, fim_strdate)
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
    genfunc = gendt.gen_dailydates_or_empty_bw_ini_fim_opt_order(ini_strdate, fim_strdate, decrescent=True)
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
    curr_refmo = rfm.make_refmonth_or_current()
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
    # t2 same as t1 but letting it fall back to its default (still last month's)
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
    seven_days_before = self.today - relativedelta(days=6)
    idate = seven_days_before
    exp_datelist, ret_datelist = [], []
    for i, pdate in enumerate(gendt.gen_dailydates_for_lastweek_incl_today_opt_order()):
      exp_datelist.append(idate)
      idate = idate + relativedelta(days=1)
      ret_datelist.append(pdate)
    self.assertEqual(exp_datelist, ret_datelist)
    self.assertEqual(self.today, ret_datelist[-1])
    self.assertEqual(seven_days_before, ret_datelist[0])
    # t2 same as t1 but desc ie with decrescent=True
    ret2_datelist = gendt.get_gendailydates_for_lastweek_incl_today_opt_order(decrescent=True)
    exp_datelist.reverse()
    self.assertEqual(exp_datelist, ret2_datelist)
    self.assertEqual(self.today, ret2_datelist[0])
    self.assertEqual(seven_days_before, ret2_datelist[-1])
    # unreverse it because of the decrescent=True
    exp_datelist.reverse()
    # t3 same as t2 but with 7 days (without 'today') instead of 8 and back to asc ie decrescent=False
    ret3_datelist = gendt.get_gendailydates_for_lastweek_wo_today_opt_order()
    # remove the last element which should be 'today' and included a new one at the beginning
    # ie shift it one day before
    exp_today = exp_datelist[-1]
    exp_datelist = exp_datelist[:-1]
    first_elem = exp_datelist[0]
    new_first = first_elem - relativedelta(days=1)
    exp_datelist.insert(0, new_first)
    self.assertEqual(self.today, exp_today)
    self.assertEqual(exp_datelist, ret3_datelist)
    yesterday = self.today - relativedelta(days=1)
    self.assertEqual(yesterday, ret3_datelist[-1])
    self.assertEqual(new_first, ret3_datelist[0])

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
    # t4 subtest empty lists returned (ask a year in the future, but do not allow "accept future" (ie, accfuture=False)
    y = self.today.year + 1
    returned_datelist = gendt.get_gendailydates_for_yearrange_or_empty_opt_order_coff_accfut(
      y, y, False, None, accfuture=False
    )
    self.assertEqual([], returned_datelist)
