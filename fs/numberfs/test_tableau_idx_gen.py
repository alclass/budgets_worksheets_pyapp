#!/usr/bin/env python3
"""
fs/numberfs/test_tableau_idx_gen.py
  Unit Tests for tableaufunctions.py
"""
import unittest
import fs.numberfs.tableau_idx_gen as ligen  # .TableauLetterIndexGenerator
import fs.numberfs.letterlist_inherited as llst  # .LetterList


class TestCaseTableuFunctions(unittest.TestCase):

  def setUp(self):
    self.idxgen = ligen.TableauLetterIndexGenerator()

  def test_generate_some(self):
    expected_letter = 'a'.upper()
    b1idx_param = 1
    returned_letteridx = self.idxgen.transpose_to_letteridx_from_a_given_1basedidx(b1idx_param)
    # t1 starting by b1_idx 1 which maps to letteridx 'A'
    self.assertEqual(expected_letter, returned_letteridx)
    letteridx_param = expected_letter
    returned_b1idx = self.idxgen.transpose_to_1basedidx_from_a_given_letteridx(letteridx_param)
    expected_b1idx = b1idx_param
    # t2 does the t1 comeback comparison
    self.assertEqual(expected_b1idx, returned_b1idx)

  def test_comparing_the_80_first_gen_indices(self):
    """
    Obs: the generator, specially for letterindices, generates sequencially started at 0-based index 0.
    If an arbitrary "high" index is wanted, it may be gotten from the functions tested above.
    """
    # t1 same as t1 in the method-test above
    # but comparing the 800 first b1_indices with their corresponding letterindices
    total_to_gen = 80
    letterindices = list(self.idxgen.generate_first_n_letterindices(total_to_gen))
    b1indices = list(self.idxgen.generate_first_n_base1indices(total_to_gen))
    for i in range(total_to_gen):
      letteridx = letterindices[i]
      b1idx = b1indices[i]
      returned_letteridx = self.idxgen.transpose_to_letteridx_from_a_given_1basedidx(b1idx)
      returned_b1idx = self.idxgen.transpose_to_1basedidx_from_a_given_letteridx(letteridx)
      self.assertEqual(b1idx, returned_b1idx)
      self.assertEqual(letteridx, returned_letteridx)

  def test_above_800_first_indices(self):
    # t1 same as the method-tests above, but using a numberindex 'well' greater than 800
    b1idx_param = 10000
    returned_letteridx = self.idxgen.transpose_to_letteridx_from_a_given_1basedidx(b1idx_param)
    expected_letteridx = 'NTP'
    self.assertEqual(expected_letteridx, returned_letteridx)
    letteridx_param = 'PTN'
    returned_b1idx = self.idxgen.transpose_to_1basedidx_from_a_given_letteridx(letteridx_param)
    expected_b1idx = 11350
    self.assertEqual(expected_b1idx, returned_b1idx)
    self.assertGreater(expected_b1idx, b1idx_param)
    self.assertGreater(letteridx_param, expected_letteridx)

  def test_an_even_greater_letterindex(self):
    # t1 same as the previous method-test above,
    # using a still greater letterindex but only indirectly testing the b1_idx
    letteridx_param = 'XZTGK'  # numberidx will be gotten and compared back
    returned_b1idx = self.idxgen.transpose_to_1basedidx_from_a_given_letteridx(letteridx_param)
    returned_letteridx = self.idxgen.transpose_to_letteridx_from_a_given_1basedidx(returned_b1idx)
    self.assertEqual(letteridx_param, returned_letteridx)
    gottenback_b1idx = self.idxgen.transpose_to_1basedidx_from_a_given_letteridx(returned_letteridx)
    self.assertEqual(gottenback_b1idx, returned_b1idx)

  def test_range_generation(self):
    expected_gen_list = list('DEFGH')
    return_gen_list = []
    counted = 0
    # notice that, differently from range(start, end), 'end' here is included
    for lindices in self.idxgen.generate_letterindices_within_range_as_0basedidx(start=3, end=7, decrescent=False):
      return_gen_list.append(lindices)
      counted += 1
    self.assertEqual(expected_gen_list, return_gen_list)
    self.assertEqual(len(expected_gen_list), counted)
    return_gen_list = []
    counted = 0
    for lindices in self.idxgen.generate_letterindices_within_range_as_0basedidx(start=3, end=7, decrescent=True):
      return_gen_list.append(lindices)
      counted += 1
    expected_gen_list = list(reversed(expected_gen_list))  # list('DEFGH') reverse => list('HGFED')
    # t3 same as t1 but now in descending order (where former list will equal the latter as reversed)
    self.assertEqual(expected_gen_list, return_gen_list)

  def test_arithmetic(self):
    """
    tli1.transpose_to_letteridx_from_0basedidx(2)
    tli2.transpose_to_letteridx_from_0basedidx(3)
    tli3 = tli1 + tli2
    print('tli1 + tli2 = tli3', tli1, tli2, tli3)
    tli3 = tli2 - tli1
    print('tli2 - tli1 = tli3', tli2, tli1, tli3)
    tli3 = tli1 - tli2
    print('tli1 - tli2 = tli3', tli1, tli2, tli3)

    """
    letter, number = 'B', 2
    tli1 = ligen.TableauLetterIndex(letter)
    self.assertEqual(tli1.letteridx, letter)
    self.assertEqual(tli1.base1idx, number)
    soma = number
    letter, number = 'C', 3
    tli2 = ligen.TableauLetterIndex(letter)
    self.assertEqual(tli2.letteridx, letter)
    self.assertEqual(tli2.base1idx, number)
    tli3 = tli1 + tli2
    soma += number
    expected_letter = 'E'  # ie, B=2 + C=3 = E=5
    self.assertEqual(tli3.letteridx, expected_letter)
    self.assertEqual(tli3.base1idx, soma)
    letter = 'BFWX'
    tli1 = ligen.TableauLetterIndex(letter)
    n1 = tli1.base1idx
    letter = 'KKKK'
    tli2 = ligen.TableauLetterIndex(letter)
    n2 = tli2.base1idx
    tli3 = tli1 + tli2
    # the second param is a concatenation, not an index summing
    self.assertNotEqual(list(tli3.letteridx), list(tli1.letteridx) + list(tli2.letteridx))
    n3 = n1 + n2
    direct_n3 = tli3.base1idx
    self.assertEqual(n3, direct_n3)
    ll1 = llst.LetterList(tli1.letteridx)  # 'BFWX'
    ll2 = llst.LetterList(tli2.letteridx)  # 'KKKK'
    ll3 = ll1 + ll2
    # notice that tli is a TableauLetterIndex and ll3 is a LetterList
    # both were "constructed" from different variables summing up
    self.assertTrue(tli3.letteridx, ll3.get_as_str_n_reversed())
    # list sum is in fact a concatenation not an arithmetic
