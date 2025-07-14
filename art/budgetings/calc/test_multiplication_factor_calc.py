#!/usr/bin/env python3
"""
commands/calc/test_multiplication_factor_calc.py
  Unit-tests for module multiplication_factor_calc.py
@see also that module's docstring for info on it.
"""
import datetime
import pandas as pd
import unittest
from dateutil.relativedelta import relativedelta
import commands.calc.multiplication_factor_calc as mfc  # .MonetCorrCalculator
import lib.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import lib.datefs.refmonths_mod as rfm


class TestCase(unittest.TestCase):

  def setUp(self):
    pass

  def test_monet_corr_calc(self):
    # this hypothesis puts all properties into the mcc object, ie the fetchable data
    # and the calculations are given ready
    # the next subtest (hypothesis) allows a 'live' fetching and then calculation
    strdateini = '2023-04-28'
    strdatefim = '2023-12-05'
    cpi_ini = 300.84
    cpi_fim = 307.671
    exrate_ini = 5.0007
    exrate_fim = 4.9522
    multiplication_factor = 1.012788
    multiplication_factor_nolessthan1 = multiplication_factor if multiplication_factor > 1 else 1.0
    mcc = mfc.MonetCorrCalculator(
      strdateini, strdatefim, rowindexfordf=0,
      cpi_ini=cpi_ini, cpi_fim=cpi_fim, exrate_ini=exrate_ini, exrate_fim=exrate_fim
    )
    # t1 multiplication_factor calculated here & in mcc
    self.assertAlmostEqual(mcc.multiplication_factor, multiplication_factor, 6)
    # t2 multiplication_factor "no less than 1" calculated here & in mcc
    self.assertAlmostEqual(mcc.multiplication_factor_nolessthan1, multiplication_factor_nolessthan1, 6)
    dateini = cnv.make_date_or_none(strdateini)
    exp_dateini_m2 = rfm.calc_refmonth_minus_n(dateini, 2)  # dateini - relativedelta(months=2)
    self.assertEqual(mcc.dateini_m2, exp_dateini_m2)
    datefim = cnv.make_date_or_none(strdatefim)
    exp_datefim_m2 = rfm.calc_refmonth_minus_n(datefim, 2)  # datefim - relativedelta(months=2)
    print('exp_datefim_m2', exp_datefim_m2, 'datefim', datefim, dateini)
    self.assertEqual(mcc.datefim_m2, exp_datefim_m2)
    pdict = {
      'dt_i': dateini,
      'cpi_i': mcc.cpi_ini,
      'exr_i': mcc.exrate_ini,
      'dt_f': datefim,
      'cpi_f': mcc.cpi_fim,
      'exr_f': mcc.exrate_fim,
      'mult': mcc.multiplication_factor,
      'mul1': mcc.multiplication_factor_nolessthan1,
    }
    # due to differences in decimal places, pdict above became mixed,
    # ie, the two dates (ini & fim) came from the 'expected'
    # and the six float numbers came from the 'returned' (if floats differ, df.equals() returns False)
    # this subtest, one might say, has at least an organization value
    df = pd.DataFrame(pdict, index=[0], columns=mfc.DATAFRAME_COLUMNS)
    # t3 DataFrame here compare to mcc's
    self.assertTrue(mcc.df.equals(df))
    # ----------------------------------------------------------------
    # This next subtest is the same as t1 but this new one lets it fetch data from db or the REST API
    # the subtest may not work 'live', ie if local db is empty or the REST API
    # is not retrieving data at the moment of this unit-testing
    previous_mcc = mcc
    mcc = mfc.MonetCorrCalculator(
      strdateini, strdatefim
    )
    # t4 comparing all fields in mcc
    self.assertEqual(mcc.dateini, dateini)
    self.assertEqual(mcc.datefim, datefim)
    self.assertEqual(mcc.dateini_m2, exp_dateini_m2)
    self.assertEqual(mcc.datefim_m2, exp_datefim_m2)
    self.assertAlmostEqual(mcc.cpi_ini, cpi_ini, 4)
    self.assertAlmostEqual(mcc.cpi_fim, cpi_fim, 4)
    self.assertAlmostEqual(mcc.exrate_ini, exrate_ini, 4)
    self.assertAlmostEqual(mcc.exrate_fim, exrate_fim, 4)
    self.assertAlmostEqual(mcc.multiplication_factor, multiplication_factor, 6)
    self.assertAlmostEqual(mcc.multiplication_factor_nolessthan1, multiplication_factor_nolessthan1, 6)
    # the df was built up in a subtest above
    self.assertTrue(mcc.df.equals(df))
    # reminding that both mcc's (the previous one and this) should be the same
    # mcc.__eq__ uses round(f, DECIMALPLACES) where DECIMALPLACES has been configured with 4
    self.assertEqual(mcc, previous_mcc)

  def test_passing_invalid_n_valid_dates_at_construction(self):
    # this hypothesis sends in 'bad' strdates and expect a ValueError raised
    strdateini, strdatefim = 'foo', 'bar'
    # t1 expects ValueError raised
    self.assertRaises(
      ValueError,
      mfc.MonetCorrCalculator,
      dateini=strdateini, datefim=strdatefim,
    )
    # in this, dateini is good but datefim is rubish, again ValueError is expected
    # (remind that datefim as None means default, but a Non-None that is not date-makeable doesn't go to default)
    strdateini, strdatefim = '2023-12-12', 'bar'
    # t2 also expects ValueError raised
    self.assertRaises(
      ValueError,
      mfc.MonetCorrCalculator,
      dateini=strdateini, datefim=strdatefim,
    )
    # in this, dateini is yesterday and datefim is today
    today = datetime.date.today()
    yesterday = today - relativedelta(days=1)
    mcc = mfc.MonetCorrCalculator(yesterday, today)
    # t3 comparing dateini & datefim
    self.assertEqual(mcc.dateini, yesterday)
    self.assertEqual(mcc.datefim, today)
    n_days = today - yesterday  # result is datetime.timedelta(days=n)
    self.assertEqual(n_days.days, 1)
    # in this, dateini & datefim are date-makeable and in the past
    strdateini, strdatefim = '2023-10-12', '2023-11-12'
    mcc = mfc.MonetCorrCalculator(strdateini, strdatefim)
    dateini, datefim = cnv.make_date_or_none(strdateini), cnv.make_date_or_none(strdatefim)
    # t4 compares previous mcc with a directly instantiated one
    self.assertEqual(
      mcc,
      mfc.MonetCorrCalculator(dateini=dateini, datefim=datefim)
    )
    # dates cannot be in the future, if so ValueError is raised
    tomorrow = today + relativedelta(days=1)
    # t5 expected ValueError raised because of date in the future (tomorrow)
    self.assertRaises(
      ValueError,
      mfc.MonetCorrCalculator,
      dateini=yesterday, datefim=tomorrow,
    )
