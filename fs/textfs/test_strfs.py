#!/usr/bin/env python3
"""
fs/textfs/test_strfs.py
  unit-tests functions in module strfs.py which contains string related functions.
"""
import fs.textfs.strfs as sfs
import unittest


class TestStrFunctions(unittest.TestCase):

  def test_trans_str_or_number_to_tuple_commasepstrnumber_n_float(self):
    # t1 test a strnumber with 3 decimal places expecting 2 decimal places
    strnumber = "2.456,165"
    expected_strnumber = "2456,16"
    expected_float_n = 2456.165
    returned_strnumber, ret_float_n = sfs.trans_str_or_number_to_tuple_commasepstrnumber_n_float(strnumber, decimal_places=2)
    self.assertEqual(expected_strnumber, returned_strnumber)
    self.assertAlmostEquals(expected_float_n, ret_float_n)
    # t2 same as t1 but rounding decimal places 'down' instead of 'up'
    strnumber = "2.456,155"
    expected_strnumber = "2456,15"
    expected_float_n = 2456.155
    returned_strnumber, ret_float_n = sfs.trans_str_or_number_to_tuple_commasepstrnumber_n_float(strnumber, decimal_places=2)
    self.assertEqual(expected_strnumber, returned_strnumber)
    self.assertAlmostEquals(expected_float_n, ret_float_n)

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
