#!/usr/bin/env python3
"""
fs/textfs/test_strfs.py
  unit-tests functions in module strfs.py which contains string related functions.
"""
import fs.textfs.strfs as sfs
import unittest


class TestStrFunctions(unittest.TestCase):

  def test_trans_str_or_number_to_tuple_commasepstrnumber_n_float(self):
    """
    This test takes into consideration the behavior of the round(n, dp)

    Python's round() adopts "rounding half to even strategy"
    which is the default rounding rule in the IEEE-754 standard



    """
    # t1 test a strnumber with 3 decimal places expecting 2 decimal places
    strnumber = "2456.165"
    expected_strnumber = "2456,16"  # ie, last but 1 is even,
    expected_float_n = 2456.165
    returned_strnumber, ret_float_n = sfs.trans_pointsep_str_or_number_to_tuple_commasep_str_n_float(
      strnumber, decimal_places=2
    )
    self.assertEqual(expected_strnumber, returned_strnumber)
    self.assertAlmostEqual(expected_float_n, ret_float_n)
    # t2 same as t1 but rounding decimal places 'down' instead of 'up'
    strnumber = "2456.155"
    expected_strnumber = "2456,16"  # notice that this is expected from round(n, 2)
    expected_float_n = 2456.155
    returned_strnumber, ret_float_n = sfs.trans_pointsep_str_or_number_to_tuple_commasep_str_n_float(
      strnumber, decimal_places=2
    )
    self.assertEqual(expected_strnumber, returned_strnumber)
    self.assertAlmostEqual(expected_float_n, ret_float_n)

  def test_validate_formedness_returning_brazils_cep_as_str_or_none(self):
    # t1 test an "arbitrary" cep
    p_cep = '20.550-045'
    expected_cep = '20550045'
    returned_cep = sfs.validate_formedness_returning_brazils_cep_as_str_or_none(p_cep)
    self.assertEqual(expected_cep, returned_cep)
    # t2 like t1 test another "arbitrary" cep
    p_cep = '25.123-123'
    expected_cep = p_cep.replace('.', '').replace('-', '')
    returned_cep = sfs.validate_formedness_returning_brazils_cep_as_str_or_none(p_cep)
    self.assertEqual(expected_cep, returned_cep)
    # t3 p_cep without dot or dash
    p_cep = '25123124'
    expected_cep = p_cep
    returned_cep = sfs.validate_formedness_returning_brazils_cep_as_str_or_none(p_cep)
    self.assertEqual(expected_cep, returned_cep)
    # t4 test None
    p_cep = 'blah bla foo bar'
    returned_cep = sfs.validate_formedness_returning_brazils_cep_as_str_or_none(p_cep)
    self.assertIsNone(returned_cep)
    # t5 as t3 with a different non-CEP
    p_cep = '123456789'  # has 9 digits, it should not have more than 8
    returned_cep = sfs.validate_formedness_returning_brazils_cep_as_str_or_none(p_cep)
    self.assertIsNone(returned_cep)

  def test_round_last_digit_from_integer_get_as_str(self):
    # t1 expecting round-down, ie given 125 get 120
    anumber = '125'
    expected_rounded_strnumber = '120'
    returned_rounded_strnumber = sfs.round_last_digit_from_integer_get_as_str(anumber)
    self.assertEqual(expected_rounded_strnumber, returned_rounded_strnumber)
    # t2 same as t1 expecting round-up, ie given 135 get 130
    anumber = '135'
    expected_rounded_strnumber = '130'
    returned_rounded_strnumber = sfs.round_last_digit_from_integer_get_as_str(anumber)
    self.assertEqual(expected_rounded_strnumber, returned_rounded_strnumber)

  def test_graft_thousands_pointsep_from_a_commasep_strnumber(self):
    """
    strnumbers = ['12345677,326', '12345677,335', '12345676,325']
    for strnumber in strnumbers:
      re_strnumber = sfs.graft_thousands_pointsep_from_a_commasep_strnumber(strnumber)
      scrmsg = f"strnumber {strnumber} | re_strnumber = {re_strnumber}"
      print(scrmsg)
    """
    p_strnumber = '12345677,325'
    expected_strnumber = '12.345.677,32'
    returned_strnumber = sfs.graft_thousands_pointsep_from_a_commasep_strnumber(p_strnumber)
    self.assertEqual(expected_strnumber, returned_strnumber)
    p_strnumber = '12345677,336'
    expected_strnumber = '12.345.677,34'
    returned_strnumber = sfs.graft_thousands_pointsep_from_a_commasep_strnumber(p_strnumber)
    self.assertEqual(expected_strnumber, returned_strnumber)

  def test_decimal_places_rounding_n_also_trans(self):
    """
    Python's round() adopts "rounding half to even strategy"
    which is the default rounding rule in the IEEE-754 standard
    """
    # abbreviating a long name to a short one
    trans = sfs.trans_pointsep_str_or_number_to_tuple_commasep_str_n_float
    # dplaces = 0
    prm_f, exp_f, dplaces = 3.5, 4.0, 0
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    prm_f, exp_f, dplaces = 4.5, 4.0, 0
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    prm_f, exp_f, dplaces = 5.5, 6.0, 0
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    prm_f, exp_f, dplaces = 6.5, 6.0, 0
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    # dplaces = 1
    prm_f, exp_f, dplaces = 3.25, 3.2, 1
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    # another
    prm_f, exp_f, dplaces = 3.35, 3.4, 1
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    # another
    prm_f, exp_f, dplaces = 3.45, 3.5, 1  # exception?
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    prm_f, exp_f, dplaces = 3.55, 3.5, 1  # exception?
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    # another
    prm_f, exp_f, dplaces = 3.65, 3.6, 1
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    # another
    prm_f, exp_f, dplaces = 3.75, 3.8, 1
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    # another
    # dplaces = 2
    prm_f, exp_f, dplaces = 1.155, 1.16, 2
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    # another
    prm_f, exp_f = 1.255, 1.25
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)  # exception?
    # another
    prm_f, exp_f = 1.355, 1.35
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)  # exception?
    # another
    prm_f, exp_f = 1.455, 1.46
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    # another
    prm_f, exp_f = 1.555, 1.55
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)  # exception?
    # another
    prm_f, exp_f = 1.655, 1.66
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    # another
    prm_f, exp_f = 1.755, 1.75
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)  # exception?
    # another
    prm_f, exp_f = 1.855, 1.85
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)  # exception?
    # another
    prm_f, exp_f = 1.955, 1.96
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    prm_f, exp_f = 2.055, 2.06
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    # another
    prm_f, exp_f = 2.155, 2.15
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces+1)  # exception?
    # another
    prm_f, exp_f = 2.255, 2.25
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces+1)  # exception?
    # another
    prm_f, exp_f = 2.355, 2.35
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    self.assertEqual(exp_sn, ret_sn)
    self.assertEqual(ret_f, prm_f)
    ret_f = round(prm_f, dplaces)
    self.assertAlmostEqual(exp_f, ret_f, dplaces+1)  # exception?

