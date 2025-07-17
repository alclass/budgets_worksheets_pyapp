#!/usr/bin/env python3
"""
fs/numberfs/test_combinations.py
  Unit-tests for module fs/numberfs/combinations.py

"""
import unittest
import lib.numberfs.combinations as cmb  # .comb_n_2_by_2


class TestCombination(unittest.TestCase):

  def test_compare_sum_of_ns_w_comb_n_2_by_2(self):
    """
    This test-method tests all the following three functions (without their lower limits) in combinations.py, ie:
      a) fact()
      b) comb_n_2_by_2()
      c) sum_first_n_ints_non_negative()
    and, also, tests the comparison between the two latter ones.
    """
    # t1
    n, expected_comb = 5, 10
    returned_comb = cmb.comb_n_2_by_2(n)
    self.assertEqual(expected_comb, returned_comb)
    n, expected_sum_ns = n-1, expected_comb
    returned_sum_ns = cmb.sum_first_n_ints_non_negative(n)
    self.assertEqual(expected_sum_ns, returned_sum_ns)
    # t2 same as t1 with a different couple comb & sum_ns
    n, expected_comb = 12, 66
    returned_comb = cmb.comb_n_2_by_2(n)
    self.assertEqual(expected_comb, returned_comb)
    n, expected_sum_ns = n-1, expected_comb
    returned_sum_ns = cmb.sum_first_n_ints_non_negative(n)
    self.assertEqual(expected_sum_ns, returned_sum_ns)

  def test_lower_limits(self):
    """
    Complementing the test-method above, this test-method tests the three above referred functions
      with input values "close" to their "lower" limits:
      a) for fact(), test a negative number, 0 & 1
      b) for comb_n_2_by_2(), test a negative number, 0, 1 & 2
      c) sum_first_n_ints_non_negative(), test a negative number & then comparisons with its simmetrical function
    """
    # t1 factorial() close to 'limits'
    returned_fact = cmb.fact(-123)
    self.assertIsNone(returned_fact)
    returned_fact = cmb.fact(-1)
    self.assertIsNone(returned_fact)
    returned_fact = cmb.fact(0)
    self.assertEqual(1, returned_fact)
    returned_fact = cmb.fact(1)
    self.assertEqual(1, returned_fact)
    returned_fact = cmb.fact(2)
    self.assertEqual(2, returned_fact)
    # t2 combination() close to 'limits'
    returned_comb = cmb.comb_n_2_by_2(-1)
    self.assertIsNone(returned_comb)
    returned_comb = cmb.comb_n_2_by_2(1)
    self.assertIsNone(returned_comb)
    returned_comb = cmb.comb_n_2_by_2(2)
    self.assertEqual(1, returned_comb)
    # t3 sum_of_first_ns() close to 'limits' & compared to its simmetrical function
    returned_sum_ns = cmb.sum_first_n_ints_non_negative(-1)
    self.assertIsNone(returned_sum_ns)
    returned_sum_ns_negative = cmb.sum_first_n_ints_allow_negative(-1)
    self.assertEqual(returned_sum_ns_negative, -1)
    returned_sum_ns = cmb.sum_first_n_ints_non_negative(1)
    returned_sum_ns_negative = cmb.sum_first_n_ints_allow_negative(-1)
    self.assertEqual(returned_sum_ns_negative, -returned_sum_ns)
    returned_sum_ns_negative = cmb.sum_first_n_ints_allow_negative(0)
    self.assertEqual(returned_sum_ns_negative, 0)
    returned_sum_ns = cmb.sum_first_n_ints_non_negative(0)
    self.assertEqual(returned_sum_ns, 0)
    returned_sum_ns = cmb.sum_first_n_ints_non_negative(1234)
    returned_sum_ns_negative = cmb.sum_first_n_ints_allow_negative(-1234)
    self.assertEqual(returned_sum_ns_negative, -returned_sum_ns)
