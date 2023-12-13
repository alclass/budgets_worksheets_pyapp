#!/usr/bin/env python3
"""
fs/numberfs/tableau_idx_gen.py
  contains functions that computes with a tableau (ie an x-y matrix or worksheet).

These are useful to constructing a worksheet when column parameter is a letter-index.

The two main functionalities are:
  a) generate_first_n_letterindices a letterindex from a numberindex, and
  a) generate_first_n_letterindices a numberindex from a letterindex

The letterindices are those characteristically seen in a spreadsheet software,
  ie, A, B, C, ..., X, Y, Z, AA, AB, AC, ..., AX, AY, AZ, BA, BB, BC,etc.

The number indices may be 0-based or 1-based, ie:
  0-based: 0, 1, 2, ...
  1-based: 1, 2, 3, ...

The mapping one-to-one among them are:
  0-base to letter: 0: A, 1: B, 2: C, ...
  1-base to letter: 1: A, 2: B, 3: C, ...

More examples:
  (...) 727 728 AAZ; 728 729 ABA; 729 730 ABB; 730 731 ABC; 733 734 ABF (...)
  (...) 750 751 ABW; 751 752 ABX; 752 753 ABY; 753 754 ABZ; 754 755 ACA (...)

@see also unit-tests for perceiving that there are "assert-equal's" one to the other.
"""
import string


class TableauLetterIndexGenerator:

  MAX_LOOP_CYCLES = 200
  ASCII_26_UPPERCASE_LETTERS = string.ascii_uppercase

  def __init__(self):
    self.ongoing_letter_digits = []

  @property
  def rolling_letter_index(self):
    if len(self.ongoing_letter_digits) == 0:
      return ''
    letter_list = reversed(self.ongoing_letter_digits)
    return ''.join(letter_list)

  def add_one_to_single_letter(self, letter: str):
    letter = letter.upper()
    vai_um = False
    if letter == 'Z':
      changed_letter = 'A'
      vai_um = True
    else:
      idx = self.ASCII_26_UPPERCASE_LETTERS.index(letter)
      changed_letter = self.ASCII_26_UPPERCASE_LETTERS[idx + 1]
    return changed_letter, vai_um

  def add_one_to_letter_index_recursive_left_to_right_letter(self, pos=0):
    """
    """
    if pos == len(self.ongoing_letter_digits):
      self.ongoing_letter_digits.insert(0, 'A')
      return
    letter = self.ongoing_letter_digits[pos]
    changed_letter, vai_um = self.add_one_to_single_letter(letter)
    self.ongoing_letter_digits[pos] = changed_letter
    if vai_um:
      return self.add_one_to_letter_index_recursive_left_to_right_letter(pos + 1)

  def generate_first_n_letterindices(self, first_n=53):
    self.ongoing_letter_digits = []
    for i in range(first_n):
      self.add_one_to_letter_index_recursive_left_to_right_letter()
      yield self.rolling_letter_index

  def get_letteridx_from_a_1basedidx(self, b1idx, recursed=False):
    if not recursed:
      self.ongoing_letter_digits = []
    digit_idx = b1idx % 26
    letter = self.ASCII_26_UPPERCASE_LETTERS[digit_idx-1]
    self.ongoing_letter_digits.append(letter)
    # this is necessary to adjust the "vai_um", ie after Z it's AA, after AZ, it's BA and so on
    # without the adjusting "minus 1", the Z above would be AZ and AZ would be BZ...
    b1idx -= 1
    number_divided_by_base = b1idx // 26
    if number_divided_by_base > 0:
      return self.get_letteridx_from_a_1basedidx(number_divided_by_base, True)
    return self.rolling_letter_index

  @staticmethod
  def generate_first_n_base1indices(first_n):
    for i in range(first_n):
      yield i+1

  def get_letteridx_from_a_0basedidx(self, b0idx):
    return self.get_letteridx_from_a_1basedidx(b0idx+1)

  def get_1based_idx_for_letter_idx(self, word):
    word = word.upper()
    wordlist = list(word)
    rev_wl = reversed(wordlist)
    idx_as_soma, pwr = 0, 0
    for pwr, c in enumerate(rev_wl):
      idx = self.ASCII_26_UPPERCASE_LETTERS.index(c)
      idx_as_soma += (idx+1) * 26 ** pwr
    return idx_as_soma

  def get_0based_idx_for_letter_idx(self, word):
    return self.get_1based_idx_for_letter_idx(word)

  def process(self):
    for i, idx_as_word in enumerate(self.generate_first_n_letterindices()):
      comp_idx = self.get_1based_idx_for_letter_idx(idx_as_word)
      print(i, i+1, idx_as_word, comp_idx)


def adhoctest1():
  """
  sg.process()
  ret = sg.get_1based_idx_for_letter_idx('aa')
  sg.process()
  word = 'aa'
  print(word, 'get_1based_idx_for_letter_idx', ret)

  b1idx = 53
  letteridx = sg.get_letteridx_from_a_1basedidx(b1idx)
  print('letteridx for b1idx', b1idx, letteridx)
  """
  sg = TableauLetterIndexGenerator()
  total_to_gen = 800
  letterindices = list(sg.generate_first_n_letterindices(total_to_gen))
  b1indices = list(sg.generate_first_n_base1indices(total_to_gen))
  for i in range(total_to_gen):
    letteridx = letterindices[i]
    b1idx = b1indices[i]
    returned_letteridx = sg.get_letteridx_from_a_1basedidx(b1idx)
    returned_b1idx = sg.get_1based_idx_for_letter_idx(letteridx)
    print(b1idx, returned_b1idx)
    print(letteridx, returned_letteridx)


def adhoctest2():
  sg = TableauLetterIndexGenerator()
  li = list(sg.generate_first_n_letterindices(53))
  print(li)
  for i in range(25, 54):
    returned_letteridx = sg.get_letteridx_from_a_1basedidx(i)
    print(i, returned_letteridx)
  b1idx = 10000
  returned_letteridx = sg.get_letteridx_from_a_1basedidx(b1idx)
  print(b1idx, returned_letteridx)
  letteridx_param = 'PTN'
  returned_b1idx = sg.get_1based_idx_for_letter_idx(letteridx_param)
  print(letteridx_param, returned_b1idx)


def process():
  """
  adhoc_for_groupby()
  """
  adhoctest2()


if __name__ == "__main__":
  process()
