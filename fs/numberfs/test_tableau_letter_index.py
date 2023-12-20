#!/usr/bin/env python3
"""
fs/numberfs/test_tableau_letter_index.py
  Unit Tests for tableau_letter_index.py
"""
import unittest
import fs.numberfs.tableau_letter_index as tli  # .TableauLetterIndexGenerator
import fs.numberfs.letterlist_inherited as llst  # .LetterList


class TestCaseTableauLetterIndex(unittest.TestCase):

  def setUp(self):
    self.letterindex = 'a'
    self.tlio = tli.TableauLetterIndex(letterindex=self.letterindex)

  def test_first_elements(self):
    expected_letterindex, expected_b0idx, expected_b1idx = self.letterindex.upper(), 0, 1
    expected_letterlist = list(expected_letterindex)
    # t1 instance tlio with letterindex 'A'
    self.assertEqual(expected_letterindex, self.tlio.letterindex)
    self.assertEqual(expected_letterlist, self.tlio.letterlist)
    self.assertEqual(expected_b0idx, self.tlio.base0index)
    self.assertEqual(expected_b1idx, self.tlio.base1index)
    # test when 0 (zero), ie letterindex is None and letterlist is empty
    tlio = tli.TableauLetterIndex(letterlist=[])
    self.assertEqual('', tlio.letterindex)
    self.assertEqual([], tlio.letterlist)
    self.assertEqual(-1, tlio.base0index)
    self.assertEqual(0, tlio.base1index)
    self.assertTrue(tlio.is_ground)
    # test 0 (zero) again via letterindex instead of letterlist
    tlio = tli.TableauLetterIndex(letterindex='')
    self.assertEqual('', tlio.letterindex)
    self.assertEqual([], tlio.letterlist)
    self.assertEqual(-1, tlio.base0index)
    self.assertEqual(0, tlio.base1index)
    self.assertTrue(tlio.is_ground)
    tlio = tli.TableauLetterIndex(base1index=0)
    self.assertEqual('', tlio.letterindex)
    self.assertEqual([], tlio.letterlist)
    self.assertEqual(-1, tlio.base0index)
    self.assertEqual(0, tlio.base1index)
    self.assertTrue(tlio.is_ground)

  def test_first_adds_n_substracts(self):
    # t2 add one to object created at t1  # A + 1 is B
    self.tlio.add_one(inplace=True)
    expected_letterindex = 'B'
    expected_letterlist = list(expected_letterindex)
    expected_b0idx, expected_b1idx = 1, 2
    self.assertEqual(expected_letterindex, self.tlio.letterindex)
    self.assertEqual(expected_letterlist, self.tlio.letterlist)
    self.assertEqual(expected_b0idx, self.tlio.base0index)
    self.assertEqual(expected_b1idx, self.tlio.base1index)
    # t3 subtract one from object created at t1  # B - 1 is A
    self.tlio.subtract_one(inplace=True)
    expected_letterindex = 'A'
    expected_b0idx, expected_b1idx = 0, 1
    expected_letterlist = list(expected_letterindex)
    self.assertEqual(expected_letterindex, self.tlio.letterindex)
    self.assertEqual(expected_letterlist, self.tlio.letterlist)
    self.assertEqual(expected_b0idx, self.tlio.base0index)
    self.assertEqual(expected_b1idx, self.tlio.base1index)

  def test_add_n_subtract_w_2digits_letterindices(self):
    letterindex = 'ab'
    tlio = tli.TableauLetterIndex(letterindex=letterindex)
    expected_letterindex, expected_b1idx = 'AA', 27
    tlio.subtract_one(inplace=True)
    self.assertEqual(expected_letterindex, tlio.letterindex)
    self.assertEqual(expected_b1idx, tlio.base1index)
    expected_letterindex, expected_b1idx = 'Z', 26
    tlio.subtract_one(inplace=True)
    self.assertEqual(expected_letterindex, tlio.letterindex)
    self.assertEqual(expected_b1idx, tlio.base1index)
    expected_letterindex, expected_b1idx = 'AA', 27
    tlio.add_one(inplace=True)
    self.assertEqual(expected_letterindex, tlio.letterindex)
    self.assertEqual(expected_b1idx, tlio.base1index)
    expected_letterindex, expected_b1idx = 'AB', 28
    tlio.add_one(inplace=True)
    self.assertEqual(expected_letterindex, tlio.letterindex)
    self.assertEqual(expected_b1idx, tlio.base1index)
    letterindex = 'ba'
    tlio = tli.TableauLetterIndex(letterindex=letterindex)
    expected_letterindex, expected_b1idx = 'AZ', 52
    tlio.subtract_one(inplace=True)
    self.assertEqual(expected_letterindex, tlio.letterindex)
    self.assertEqual(expected_b1idx, tlio.base1index)

  def test_arithmetic(self):
    """
    tli1.set_letterindex_transposing_from_0basedidx(2)
    tli2.set_letterindex_transposing_from_0basedidx(3)
    tli3 = tli1 + tli2
    print('tli1 + tli2 = tli3', tli1, tli2, tli3)
    tli3 = tli2 - tli1
    print('tli2 - tli1 = tli3', tli2, tli1, tli3)
    tli3 = tli1 - tli2
    print('tli1 - tli2 = tli3', tli1, tli2, tli3)
    """
    letterindex, base1index = 'B', 2
    tli1 = tli.TableauLetterIndex(letterindex=letterindex)
    self.assertEqual(tli1.letterindex, letterindex)
    self.assertEqual(tli1.base1index, base1index)
    soma = base1index + 0
    letterindex, base1index = 'C', 3
    tli2 = tli.TableauLetterIndex(letterindex=letterindex)
    self.assertEqual(tli2.letterindex, letterindex)
    self.assertEqual(tli2.base1index, base1index)
    tli3 = tli1 + tli2
    soma += base1index
    expected_letter = 'E'  # ie, b1idx B=2 + C=3 => E=5
    self.assertEqual(tli3.letterindex, expected_letter)
    self.assertEqual(tli3.base1index, soma)
    # ==================
    letterindex = 'BFWX'
    tli1 = tli.TableauLetterIndex(letterindex=letterindex)
    n1 = tli1.base1index
    letterindex = 'KKKK'
    tli2 = tli.TableauLetterIndex(letterindex=letterindex)
    n2 = tli2.base1index
    tli3 = tli1 + tli2
    # the second param is a concatenation, not an index summing
    self.assertNotEqual(list(tli3.letterindex), list(tli1.letterindex) + list(tli2.letterindex))
    n3 = n1 + n2
    direct_n3 = tli3.base1index
    self.assertEqual(n3, direct_n3)
    ll1 = llst.LetterList(tli1.letterindex)  # 'BFWX'
    ll2 = llst.LetterList(tli2.letterindex)  # 'KKKK'
    ll3 = ll1 + ll2
    # notice that tli is a TableauLetterIndex and ll3 is a LetterList
    # both were "constructed" from different variables summing up
    self.assertTrue(tli3.letterindex, ll3.get_as_str_n_reversed())
    # list sum is in fact a concatenation not an arithmetic
