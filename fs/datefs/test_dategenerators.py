#!/usr/bin/env python3
"""
fs/datefs/test_dategenerators.py
  unit-tests to fs/datefs/dategenerators functions.
fferent in sep & posorder (sep='/', posorder='mdy'
"""
import calendar
import collections
import datetime
from dateutil.relativedelta import relativedelta
import unittest
import fs.datefs.dategenerators as gendt
nt_dtymd_constr = collections.namedtuple('NTymd', field_names=['year', 'month', 'day'])
nt_dtym_refmo_constr = collections.namedtuple('NTymd', field_names=['year', 'month'])


class Test(unittest.TestCase):

  def setUp(self):
    self.today = datetime.date.today()

  def test_build_dates_n_refmonths_1(self):
    # t1
    y, m, d = 2023, 11, 11
    ntdate = nt_dtymd_constr(year=y, month=m, day=d)
    exp_date = datetime.date(year=y, month=m, day=d)
    ret_date = gendt.make_date_or_none(ntdate)
    self.assertEqual(exp_date, ret_date)
    self.assertNotEqual(ntdate, ret_date)
    # t2
    ret_date = gendt.make_date_or_none('bla foo')
    self.assertIsNone(ret_date)
    # t3
    ret_date = gendt.make_date_or_today('bla foo')
    self.assertEqual(self.today, ret_date)
    # t4
    nt_refmo = nt_dtym_refmo_constr(year=y, month=m)
    exp_refmo = datetime.date(year=y, month=m, day=1)
    ret_refmo = gendt.make_refmonth_or_none(nt_refmo)
    self.assertEqual(exp_refmo, ret_refmo)
    # t4
    ret_refmo = gendt.make_refmonth_or_none('bla bar')
    self.assertIsNone(ret_refmo)

  def test_build_dates_n_refmonths_2(self):
    # t1 test make_date_from_str() & make_date_or_none()
    y, m, d = 2023, 11, 11
    anystrdate = f'{y}-{m}-{d}'
    expect_date = datetime.date(year=y, month=m, day=d)
    returned_date = gendt.make_date_from_str_or_none(anystrdate)
    self.assertEqual(returned_date, expect_date)
    returned_date = gendt.make_date_or_none(anystrdate)
    self.assertEqual(returned_date, expect_date)
    # t2 test make_refdate_from_str() & make_date_or_none() & make_date_or_today()
    y, m = 2023, 11
    anystrdate = f'{y}-{m} bla bla'
    expect_date = datetime.date(year=y, month=m, day=1)
    returned_date = gendt.make_refmonth_or_none(anystrdate)
    self.assertEqual(returned_date, expect_date)
    returned_date = gendt.make_date_or_none(anystrdate)
    self.assertIsNone(returned_date)
    # reminding that anystrdate is not complete
    returned_date = gendt.make_date_or_today(anystrdate)
    today = datetime.date.today()
    self.assertEqual(returned_date, today)
    # t3 test convert_strdatelist_to_datelist()
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
    # t2 the same as t1 but descending (ie decrescent=True)
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
    # t3 get_gendailydates_for_refmonth_or_lastmonth_opt_order(str_refmonth)
    # previous tests spanned upon a whole month range,
    # now this one uses refmonth itself directly
    ret_desc_datelist = ret_datelist
    str_refmonth = f'{y}-{m}'
    ret_datelist = gendt.get_gendailydates_for_refmonth_or_lastmonth_opt_order(str_refmonth)
    self.assertEqual(ret_asc_datelist, ret_datelist)
    # t4 same as t3 but with desc ie decrescent=True
    ret_datelist = gendt.get_gendailydates_for_refmonth_or_lastmonth_opt_order(str_refmonth, decrescent=True)
    self.assertEqual(ret_desc_datelist, ret_datelist)

  def test_gen_dateranges_upto_months_2(self):
    mo_m1_dt = self.today - relativedelta(months=1)
    firstdate = datetime.date(year=mo_m1_dt.year, month=mo_m1_dt.month, day=1)
    _, n_days_inmo = calendar.monthrange(mo_m1_dt.year, mo_m1_dt.month)
    lastdate = datetime.date(year=mo_m1_dt.year, month=mo_m1_dt.month, day=n_days_inmo)
    delta = lastdate - firstdate
    n_days_in_bw = delta.days + 1
    str_refmonth = f"{mo_m1_dt.year}-{mo_m1_dt.month}"
    datelist = gendt.get_gendailydates_for_refmonth_or_lastmonth_opt_order(str_refmonth)
    self.assertEqual(n_days_in_bw, n_days_inmo)
    self.assertEqual(n_days_in_bw, len(datelist))
    self.assertEqual(datelist[0], firstdate)
    self.assertEqual(datelist[-1], lastdate)
    str_refmonth = 'bla foo bar'  # sends in rubish to get lastmonth
    datelist = gendt.get_gendailydates_for_refmonth_or_lastmonth_opt_order(str_refmonth)
    self.assertEqual(n_days_in_bw, len(datelist))
    self.assertEqual(datelist[0], firstdate)
    self.assertEqual(datelist[-1], lastdate)
    # desc ie decrescent=True
    datelist = gendt.get_gendailydates_for_refmonth_or_lastmonth_opt_order(str_refmonth, decrescent=True)
    self.assertEqual(n_days_in_bw, len(datelist))
    self.assertEqual(datelist[0], lastdate)
    self.assertEqual(datelist[-1], firstdate)
    n_days = 15
    cutoff_date = datetime.date(year=mo_m1_dt.year, month=mo_m1_dt.month, day=n_days)
    datelist = gendt.get_gendailydates_for_refmonth_or_lastmonth_opt_order(str_refmonth, cutoff_date=cutoff_date)
    self.assertEqual(n_days, len(datelist))
    self.assertEqual(datelist[0], firstdate)
    self.assertEqual(datelist[-1], cutoff_date)

  def test_gen_dateranges_upto_months_3(self):
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
    ret2_datelist = gendt.get_gendailydates_for_lastweek_opt_order(decrescent=True)
    exp_datelist.reverse()
    self.assertEqual(exp_datelist, ret2_datelist)
    self.assertEqual(self.today, ret2_datelist[0])
    self.assertEqual(seven_days_before, ret2_datelist[-1])

  def test_gen_dateranges_beyond_months(self):
    y = 2022
    inidate = datetime.date(year=y, month=1, day=1)
    idate = inidate
    exp_datelist, ret_datelist = [], []
    for i, pdate in enumerate(gendt.gen_dailydates_f_yearini_t_today_or_empty_opt_order(y)):
      exp_datelist.append(idate)
      idate = idate + relativedelta(days=1)
      ret_datelist.append(pdate)
    """
    today = datetime.date.today()
    self.assertEqual(exp_datelist, ret_datelist)
    self.assertEqual(inidate, ret_datelist[0])
    self.assertEqual(today, ret_datelist[-1])
    """
    y = 2023
    ret_fullyear_list = []
    # accept future
    for pdate in gendt.gen_dailydates_for_yearrange_or_empty_opt_order_n_future(y, y, False, True):
      ret_fullyear_list.append(pdate)
    self.assertEqual(365, len(ret_fullyear_list))
    # do not accept future
    ret_year_condicional_cutoff_list = []
    for pdate in gendt.gen_dailydates_for_yearrange_or_empty_opt_order_n_future(y, y, False, False):
      ret_year_condicional_cutoff_list.append(pdate)
    exp_datelist = list(filter(lambda d: d <= self.today, ret_fullyear_list))
    # print('len ret_year_condicional_cutoff_list', len(ret_year_condicional_cutoff_list))
    self.assertEqual(ret_year_condicional_cutoff_list, exp_datelist)
