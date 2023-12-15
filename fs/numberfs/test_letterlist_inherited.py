#!/usr/bin/env python3
"""

"""
import string
import unittest
import fs.numberfs.letterlist_inherited as llst  # .LetterList
MAX_LOOP_CYCLES = 200
ASCII_26_UPPERCASE_LETTERS = string.ascii_uppercase


class LetterListUnitTest(unittest.TestCase):

  def setUp(self):
    self.letterlist = llst.LetterList()

  def test_instantiate(self):
    letterlist1 = llst.LetterList()
    self.assertEqual(0, len(letterlist1))
    self.assertEqual([], letterlist1)
    self.assertRaises(ValueError, letterlist1.append, 4)
    for c in ASCII_26_UPPERCASE_LETTERS:
      letterlist1.append(c)
    self.assertEqual(letterlist1, ASCII_26_UPPERCASE_LETTERS)
    letter_a = 'a'
    letterlist1.insert(0, 'a')
    should_be = letter_a.upper() + ASCII_26_UPPERCASE_LETTERS
    self.assertEqual(letterlist1, should_be)

  def test_instantiate2(self):
    list1 = ['a', 'b', 'c']
    letterlist1 = llst.LetterList(list1)
    word1 = 'cba'
    self.assertEqual(letterlist1.get_as_str_n_reversed(), word1.upper())

  def test_instantiate3(self):
    word1 = 'abcd'
    list1 = list(word1)
    letterlist1 = llst.LetterList(word1)
    letterlist2 = llst.LetterList(list1)
    self.assertEqual(letterlist1, letterlist2)
    letterlist1.reset()
    self.assertEqual(letterlist1, [])
    letterlist1.reset(word1)
    self.assertEqual(letterlist1, list1)
    letterlist1.reset(word1+word1)
    self.assertEqual(letterlist1, list1+list1)

    # letterlist1 = letterlist1.append('boo')
    # self.assertEqual(letterlist1.get_as_str_n_reversed(), word1.upper())


def adhoctest():
  pass


def process():
  """
  adhoc_for_groupby()
  adhoctest1()
  """
  adhoctest()


if __name__ == "__main__":
  process()
