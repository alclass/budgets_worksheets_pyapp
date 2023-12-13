#!/usr/bin/env python3
"""

fs/numberfs/test_tableau_idx_gen.py
  Unit Tests for tableaufunctions.py
import fs.numberfs.tableaufunctions as tblfs
"""
import unittest
import fs.numberfs.tableau_idx_gen as ligen  # .TableauLetterIndexGenerator


class TestCaseTableuFunctions(unittest.TestCase):

  def setUp(self):
    self.idxgen = ligen.TableauLetterIndex()

  def test_generate_some(self):
    expected_letter = 'a'.upper()
    b1idx_param = 1
    returned_letteridx = self.idxgen.get_letteridx_from_a_1basedidx(b1idx_param)
    # t1 starting by b1_idx 1 which maps to letteridx 'A'
    self.assertEqual(expected_letter, returned_letteridx)
    letteridx_param = expected_letter
    returned_b1idx = self.idxgen.get_1based_idx_for_letter_idx(letteridx_param)
    expected_b1idx = b1idx_param
    # t2 does the t1 comeback comparison
    self.assertEqual(expected_b1idx, returned_b1idx)

  def test_comparing_the_800_first_gen_indices(self):
    """
    Obs: the generator, specially for letterindices, generates sequencially started at 0-based index 0.
    If an arbitrary "high" index is wanted, it may be gotten from the functions tested above.
    """
    # t1 same as t1 in the method-test above
    # but comparing the 800 first b1_indices with their corresponding letterindices
    total_to_gen = 800
    letterindices = list(self.idxgen.generate_first_n_letterindices(total_to_gen))
    b1indices = list(self.idxgen.generate_first_n_base1indices(total_to_gen))
    for i in range(total_to_gen):
      letteridx = letterindices[i]
      b1idx = b1indices[i]
      returned_letteridx = self.idxgen.get_letteridx_from_a_1basedidx(b1idx)
      returned_b1idx = self.idxgen.get_1based_idx_for_letter_idx(letteridx)
      self.assertEqual(b1idx, returned_b1idx)
      self.assertEqual(letteridx, returned_letteridx)

  def test_above_800_first_indices(self):
    # t1 same as the method-tests above, but using a numberindex 'well' greater than 800
    b1idx_param = 10000
    returned_letteridx = self.idxgen.get_letteridx_from_a_1basedidx(b1idx_param)
    expected_letteridx = 'NTP'
    self.assertEqual(expected_letteridx, returned_letteridx)
    letteridx_param = 'PTN'
    returned_b1idx = self.idxgen.get_1based_idx_for_letter_idx(letteridx_param)
    expected_b1idx = 11350
    self.assertEqual(expected_b1idx, returned_b1idx)
    self.assertGreater(expected_b1idx, b1idx_param)
    self.assertGreater(letteridx_param, expected_letteridx)

  def test_an_even_greater_letterindex(self):
    # t1 same as the previous method-test above,
    # using a still greater letterindex but only indirectly testing the b1_idx
    letteridx_param = 'XZTGK'  # numberidx will be gotten and compared back
    returned_b1idx = self.idxgen.get_1based_idx_for_letter_idx(letteridx_param)
    returned_letteridx = self.idxgen.get_letteridx_from_a_1basedidx(returned_b1idx)
    self.assertEqual(letteridx_param, returned_letteridx)
    gottenback_b1idx = self.idxgen.get_1based_idx_for_letter_idx(returned_letteridx)
    self.assertEqual(gottenback_b1idx, returned_b1idx)
