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
    # notice that one has avoided a float number ending with 5 (@see also the last test method)
    strnumber = "2456.166"
    expected_strnumber = "2456,17"  # ie, last but 1 is even,
    expected_float_n = 2456.166
    returned_strnumber, ret_float_n = sfs.trans_pointsep_str_or_number_to_tuple_commasep_str_n_float(
      strnumber, decimal_places=2
    )
    self.assertEqual(expected_strnumber, returned_strnumber)
    self.assertAlmostEqual(expected_float_n, ret_float_n)
    # t2 same as t1 but rounding decimal places 'down' instead of 'up'
    strnumber = "2456.144"
    expected_strnumber = "2456,14"  # notice that this is expected from round(n, 2)
    expected_float_n = 2456.144
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
    """
    "rounding" is not a simple issue in computing, because it needs to undergo a trade-off of "bias".
    (@see also the last test method)
    The target-function in-here does not use the built-in round() function, but a home-made one.
    However, the 'transpose' function to be tested in the sequence does use Python's built-in round() function
      and, because of that, rounding results may differ
      (crossed tests [ie, the built-in round() with the one homemade here]
      are not attempted due to possible differences when the last decimal place digit is 5).
    """
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
    # t1
    p_strnumber = '12345677,325'
    expected_strnumber = '12.345.677,32'
    returned_strnumber = sfs.graft_thousands_pointsep_from_a_commasep_strnumber(p_strnumber)
    self.assertEqual(expected_strnumber, returned_strnumber)
    # t2
    p_strnumber = '12345677,336'
    expected_strnumber = '12.345.677,34'
    returned_strnumber = sfs.graft_thousands_pointsep_from_a_commasep_strnumber(p_strnumber)
    self.assertEqual(expected_strnumber, returned_strnumber)
    # t3
    # p_strnumber = '-12345677,336'
    # expected_strnumber = '-12.345.677,34'
    # returned_strnumber = sfs.graft_thousands_pointsep_from_a_commasep_strnumber(p_strnumber)
    # self.assertEqual(expected_strnumber, returned_strnumber)

  def test_decimal_places_rounding_n_also_trans(self):
    """
    Python's round() adopts "rounding half to even strategy"
    which is the default rounding rule in the IEEE-754 standard.
      However, not really all instances are rounded that way.

    It's import to reflect that we're not testing the built-in round() function itself, but using it to
      'produce' the 'expected values', ie those that are to be compared to the 'returned values'.
      This is because the target-function itself uses round() internally.

    Obs: tests that FAIL logically considering the target function's job are under the following condition:
       => a float ending with a right zero in the decimal side, represented as str, e.g.: "1.230"
       On one side, these numbers are redundant, ie 1.23 is simpler than 1.230
       (notice that the float test pass, it's just that the string test ends up as "1,23" != "1,230")
       On another side, the very code in the test methods use rstrip(',0') for making up the "expected values".
       (Of course, one might treat the issue on the "expected side", but it might also add some
       complexity to a situation that the simpler value ("1,23") is preferable (than "1,230")
    Advice on the "Obs": avoid adding a subtest with a right zero in the decimal side of its str representation!

    Explanation of the adding of line:
      exp_sn = '0' if exp_sn == '' else exp_sn
    It's because, when producing:
      exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    exp_sn becomes empty (ie '') when exp_f is zero (0 or 0.0 became 0,0).
    Because of that, the if-expression above assigns '0' to it if it's empty.
      Notice it's not related to the target-function, but to producing the "expected value" to be
      compared to the "returned value".
    """
    # abbreviating a long name to a short one
    trans = sfs.trans_pointsep_str_or_number_to_tuple_commasep_str_n_float
    # t1
    prm_f, dplaces = 3.45, 0
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_f = round(prm_f, dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    exp_sn = '0' if exp_sn == '' else exp_sn
    self.assertEqual(exp_sn, ret_sn)
    self.assertAlmostEqual(prm_f, ret_f)
    # t2
    prm_f, dplaces = 1111.1111, 0
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_f = round(prm_f, dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    exp_sn = '0' if exp_sn == '' else exp_sn
    self.assertEqual(exp_sn, ret_sn)
    self.assertAlmostEqual(prm_f, ret_f)
    self.assertAlmostEqual(exp_f, ret_f, dplaces)
    # t3
    prm_f, dplaces = 83234.556, 0
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_f = round(prm_f, dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    exp_sn = '0' if exp_sn == '' else exp_sn
    self.assertEqual(exp_sn, ret_sn)
    self.assertAlmostEqual(prm_f, ret_f)
    # t4
    prm_f, dplaces = 3.75, 1
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_f = round(prm_f, dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    exp_sn = '0' if exp_sn == '' else exp_sn
    self.assertEqual(exp_sn, ret_sn)
    self.assertAlmostEqual(prm_f, ret_f)
    # t5
    prm_f, dplaces = 1.155, 2
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_f = round(prm_f, dplaces)
    exp_sn = str(exp_f).replace('.', ',')  # .rstrip(',0')
    exp_sn = '0' if exp_sn == '' else exp_sn
    self.assertEqual(exp_sn, ret_sn)
    self.assertAlmostEqual(prm_f, ret_f)
    # t6
    prm_f, dplaces = 1.255678, 4
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_f = round(prm_f, dplaces)
    exp_sn = str(exp_f).replace('.', ',')  # .rstrip(',0')
    exp_sn = '0' if exp_sn == '' else exp_sn
    self.assertEqual(exp_sn, ret_sn)
    self.assertAlmostEqual(prm_f, ret_f)
    # t7
    prm_f, dplaces = 1.355, 1
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_f = round(prm_f, dplaces)
    exp_sn = str(exp_f).replace('.', ',')  # .rstrip(',0')
    exp_sn = '0' if exp_sn == '' else exp_sn
    self.assertEqual(exp_sn, ret_sn)
    self.assertAlmostEqual(prm_f, ret_f)
    # t8
    prm_f, dplaces = 0.7556, 1
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_f = round(prm_f, dplaces)
    exp_sn = str(exp_f).replace('.', ',')  # .rstrip(',0')
    exp_sn = '0' if exp_sn == '' else exp_sn
    self.assertEqual(exp_sn, ret_sn)
    self.assertAlmostEqual(prm_f, ret_f)
    # t9
    prm_f, dplaces = -1.8556, 2
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_f = round(prm_f, dplaces)
    exp_sn = str(exp_f).replace('.', ',')  # .rstrip(',0')
    exp_sn = '0' if exp_sn == '' else exp_sn
    self.assertEqual(exp_sn, ret_sn)
    self.assertAlmostEqual(prm_f, ret_f)
    # t10
    prm_f, dplaces = 0.355, 0
    ret_sn, ret_f = trans(str(prm_f), decimal_places=dplaces)
    exp_f = round(prm_f, dplaces)
    exp_sn = str(exp_f).replace('.', ',').rstrip(',0')
    exp_sn = '0' if exp_sn == '' else exp_sn
    self.assertEqual(exp_sn, ret_sn)
    self.assertAlmostEqual(prm_f, ret_f)
