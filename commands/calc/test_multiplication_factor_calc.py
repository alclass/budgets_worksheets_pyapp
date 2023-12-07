#!/usr/bin/env python3
"""

"""
import pandas as pd
import unittest
import commands.calc.multiplication_factor_calc as mfc  # .MonetCorrCalculator
import fs.datefs.datefunctions as dtfs  # for make_refmonth_date_from_str


class TestCase(unittest.TestCase):

  def setUp(self):
    pass

  def test_monet_corr_calc(self):
    # t1
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
    self.assertAlmostEqual(mcc.multiplication_factor, multiplication_factor, 6)
    self.assertAlmostEqual(mcc.multiplication_factor_nolessthan1, multiplication_factor_nolessthan1, 6)
    dateini = dtfs.make_date_or_none(strdateini)
    exp_dateini_m2 = dtfs.calc_refmonth_minus_n(dateini, 2)
    self.assertEqual(mcc.dateini_m2, exp_dateini_m2)
    datefim = dtfs.make_date_or_none(strdatefim)
    exp_datefim_m2 = dtfs.calc_refmonth_minus_n(datefim, 2)
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
    # this subtest, one might say, has at least was an organization value
    df = pd.DataFrame(pdict, index=[0], columns=mfc.DATAFRAME_COLUMNS)
    self.assertTrue(mcc.df.equals(df))
    # ----------------------------------------------------------------
    # t2 is the same as t1 but the former let it fetch data from db or the REST API
    # this subtest may not work 'live', ie if local db is empty or the REST API
    # is not retrieving data at the moment of this unit-testing
    previous_mcc = mcc
    mcc = mfc.MonetCorrCalculator(
      strdateini, strdatefim
    )
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
    # the df was built up in the t1 subtest above
    self.assertTrue(mcc.df.equals(df))
    # reminding that both mcc's (the previous one at t1 and this at t2) should be the same
    # mcc.__eq__ uses round(f, DECIMALPLACES) where DECIMALPLACES has been configured with 4
    self.assertEqual(mcc, previous_mcc)
