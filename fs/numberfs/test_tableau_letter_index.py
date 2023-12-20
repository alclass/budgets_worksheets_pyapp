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
