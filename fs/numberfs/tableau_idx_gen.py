#!/usr/bin/env python3
"""
fs/numberfs/numfunctions.py
  contains various numbers functions.

"""
import string


class SeriesGen:

  MAX_LOOP_CYCLES = 200
  allletters = string.ascii_uppercase

  def __init__(self):
    self.element = None
    self.left_digits = []
    self.right_most_digit = None
    self.right_most_idx = -1

  def zero_or_restart(self):
    self.left_digits = []
    self.right_most_digit = None
    self.right_most_idx = -1

  def vai_um(self, pos=0):
    self.right_most_idx = 0
    if pos + 1 > len(self.left_digits):
      self.left_digits.insert(0, 'A')
      return
    digit = self.left_digits[pos]
    idx = self.allletters.index(digit)
    # foresee the next one (ie the incremented one)
    if idx + 1 > len(self.allletters) - 1:
      self.left_digits[pos] = 'A'
      return self.vai_um(pos+1)
    # there is space, increment it
    incr_idx = idx + 1
    self.left_digits[pos] = self.allletters[incr_idx]
    return

  def mount_element(self):
    left_digits_str = ''.join(self.left_digits)
    self.element = left_digits_str + self.right_most_digit

  def add_one(self):
    self.right_most_idx += 1
    if self.right_most_idx > len(self.allletters) - 1:
      self.vai_um()
    self.right_most_digit = self.allletters[self.right_most_idx]
    self.mount_element()

  def generate(self):
    for i in range(800):
      self.add_one()
      yield self.element

  def get_0based_idx_for_letter_idx(self, word):
    word = word.upper()
    wordlist = list(word)
    rev_wl = reversed(wordlist)
    idx_as_soma, pwr = 0, 0
    for pwr, c in enumerate(rev_wl):
      idx = self.allletters.index(c)
      idx_as_soma += (idx+1) * 26 ** pwr
    return idx_as_soma

  def process(self):
    for i, idx_as_word in enumerate(self.generate()):
      comp_idx = self.get_0based_idx_for_letter_idx(idx_as_word)
      print(i, i+1, idx_as_word, comp_idx)


def adhoctest1():
  """
  sg.process()

  """
  sg = SeriesGen()
  ret = sg.get_0based_idx_for_letter_idx('aa')
  sg.process()
  word = 'aa'
  print(word, 'get_0based_idx_for_letter_idx', ret)


def process():
  """
  adhoc_for_groupby()
  """
  adhoctest1()


if __name__ == "__main__":
  process()
