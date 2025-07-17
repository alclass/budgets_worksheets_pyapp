#!/usr/bin/env python3
"""
fs/numberfs/test_tableau_letter_index.py
  Unit Tests for tableau_letter_index.py
"""
import unittest
import lib.numberfs.tableau_letter_index as tli  # .TableauLetterIndexGenerator
import lib.numberfs.letterlist_inherited as llst  # .LetterList


class TestCaseTableauLetterIndex(unittest.TestCase):

  def setUp(self):
    self.letterindex = 'a'
    self.tlio = tli.TableauLetterIndex(letterindex=self.letterindex)

  def test_first_elements(self):
    expected_letterindex, expected_b0idx, expected_b1idx = self.letterindex.upper(), 0, 1
    expected_letterlist = list(expected_letterindex)
    # t1 instantiate tlio with letterindex 'A' & test all 4 attributes letterindex, letterlist, base0_index, base1_index
    self.assertEqual(expected_letterindex, self.tlio.letterindex)
    self.assertEqual(expected_letterlist, self.tlio.letterlist)
    self.assertEqual(expected_b0idx, self.tlio.base0index)
    self.assertEqual(expected_b1idx, self.tlio.base1index)
    # t2 test at 0 (zero or 'ground'), ie letterindex is '' (empty str) and letterlist is [] (empty list)
    tlio = tli.TableauLetterIndex(letterlist=[])
    self.assertEqual('', tlio.letterindex)
    self.assertEqual([], tlio.letterlist)
    self.assertEqual(-1, tlio.base0index)
    self.assertEqual(0, tlio.base1index)
    self.assertTrue(tlio.is_ground)
    # t3 test at 0 (zero) again via letterindex instead of letterlist
    tlio = tli.TableauLetterIndex(letterindex='')
    self.assertEqual('', tlio.letterindex)
    self.assertEqual([], tlio.letterlist)
    self.assertEqual(-1, tlio.base0index)
    self.assertEqual(0, tlio.base1index)
    self.assertTrue(tlio.is_ground)
    # t4 test at 0 (zero) again via base1_index=0
    tlio = tli.TableauLetterIndex(base1index=0)
    self.assertEqual('', tlio.letterindex)
    self.assertEqual([], tlio.letterlist)
    self.assertEqual(-1, tlio.base0index)
    self.assertEqual(0, tlio.base1index)
    self.assertTrue(tlio.is_ground)
    # t5 test at 0 (zero) again via base0_index=-1
    tlio = tli.TableauLetterIndex(base0index=-1)
    self.assertEqual('', tlio.letterindex)
    self.assertEqual([], tlio.letterlist)
    self.assertEqual(-1, tlio.base0index)
    self.assertEqual(0, tlio.base1index)
    self.assertTrue(tlio.is_ground)
    # t6 now test ValueError raised via base1_index=-1 (notice that base1_index as 0 is 'ground or zero', as 1 it's 'A')
    base1index = -1
    pdict = {'base1index': base1index}
    self.assertRaises(ValueError, tli.TableauLetterIndex, **pdict)

  def test_bad_input_parameters_combination(self):
    # t1 raises ValueError when nothing is passed in as parameter
    self.assertRaises(ValueError, tli.TableauLetterIndex)
    # t2 raises ValueError when more than one argument, though consistent among them, is passed in as parameter
    pdict = {'letterindex': 'A', 'letterlist': ['A']}
    self.assertRaises(ValueError, tli.TableauLetterIndex, **pdict)
    # t3 raises ValueError when more than one argument is passed in as parameter, this time no consistency
    # in fact, consistency among them is not checked, but the fact that there are more than 1 parameter passed in
    pdict = {'letterindex': 'A', 'letterlist': ['bla'], 'base0index': 7, 'base1index': 5}
    self.assertRaises(ValueError, tli.TableauLetterIndex, **pdict)
    # t4 the next combination does not raise ValueError internally, but TypeError,
    # which, though uncaught in code, should be raised because there is an 'unknown' parameter 'leaking in'
    pdict = {'blah': 'A', 'letterlist': ['bla'], 'base0index': 7, 'base1index': 5}
    self.assertRaises(TypeError, tli.TableauLetterIndex, **pdict)

  def test_first_adds_n_substracts(self):
    # t1 add one to object created at t1  # A + 1 is B
    self.tlio.add_one(inplace=True)
    expected_letterindex = 'B'
    expected_letterlist = list(expected_letterindex)
    expected_b0idx, expected_b1idx = 1, 2
    self.assertEqual(expected_letterindex, self.tlio.letterindex)
    self.assertEqual(expected_letterlist, self.tlio.letterlist)
    self.assertEqual(expected_b0idx, self.tlio.base0index)
    self.assertEqual(expected_b1idx, self.tlio.base1index)
    # t2 subtract one from object created at t1  # B - 1 is A
    self.tlio.subtract_one(inplace=True)
    expected_letterindex = 'A'
    expected_b0idx, expected_b1idx = 0, 1
    expected_letterlist = list(expected_letterindex)
    self.assertEqual(expected_letterindex, self.tlio.letterindex)
    self.assertEqual(expected_letterlist, self.tlio.letterlist)
    self.assertEqual(expected_b0idx, self.tlio.base0index)
    self.assertEqual(expected_b1idx, self.tlio.base1index)

  def test_add_n_subtract_w_2digits_letterindices(self):
    # t1 test add_one() & subtract_one()
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

  def test_more_arithmetic(self):
    """
    Notice that to add letters is the same as adding their base1_indices
    Example:
      B=2 + C=3 = E=5, ie B+C=E in the same way as 2+3=5
    """
    # t1 test B+C=E
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
    # t2 test 'BFWX' + 'KKKK'
    # though the result is not placed here as 'written',
    # calculation is done & compared via two different ways:
    # one way is adding them to tli3 and comparing its tli3.letterindex
    # another is adding base1_index, which is a direct sum (@see also docstring above)
    letterindex = 'BFWX'
    tli1 = tli.TableauLetterIndex(letterindex=letterindex)
    n1 = tli1.base1index
    letterindex = 'KKKK'
    tli2 = tli.TableauLetterIndex(letterindex=letterindex)
    n2 = tli2.base1index
    tli3 = tli1 + tli2
    # t3 is a kind of negative test, the second param is a concatenation, not an index summing
    # list sum is in fact a concatenation not an arithmetic
    self.assertNotEqual(list(tli3.letterindex), list(tli1.letterindex) + list(tli2.letterindex))
    n3 = n1 + n2
    direct_n3 = tli3.base1index
    self.assertEqual(n3, direct_n3)
    ll1 = llst.LetterList(tli1.letterindex)  # 'BFWX'
    ll2 = llst.LetterList(tli2.letterindex)  # 'KKKK'
    ll3 = ll1 + ll2
    # notice that tli is a TableauLetterIndex and ll3 is a LetterList
    # both were "constructed" from different variables summing up
    # t4 "completes" t2
    self.assertTrue(tli3.letterindex, ll3.get_as_str_n_reversed())
