#!/usr/bin/env python3
"""
fs/numberfs/tableau_letter_index_generator.py

import fs.numberfs.indexfunctions as idxfs  # .get_1basedindex_from_letterindex
"""
import string
import fs.numberfs.letterlist_inherited as llst  # .LetterList
import fs.numberfs.tableau_letter_index as tli  # .TableauLetterIndex
MAX_LOOP_CYCLES = 200
ASCII_26_UPPERCASE_LETTERS = string.ascii_uppercase
DEFAULT_FIRST_N_INDICES = 5


class TableauLetterIndexGenerator:

  def __init__(self):
    """
    The instance variable tbi is immutable, so it's reinstanciated after each operation
    """
    self.tab_let_idx = None

  def gen_first_n_letterindices_desc(self, first_n=3):
    self.tab_let_idx = tli.TableauLetterIndex(base1index=first_n)
    for i in range(first_n):
      yield self.tab_let_idx.letterindex
      self.tab_let_idx.subtract_one(inplace=True)

  def gen_first_n_letterindices_asc(self, first_n=3):
    self.tab_let_idx = tli.TableauLetterIndex(letterindex='A')
    for i in range(first_n):
      yield self.tab_let_idx.letterindex
      self.tab_let_idx.add_one(inplace=True)

  def gen_first_n_letterindices(self, first_n=3, decrescent=False):
    if not decrescent:
      return self.gen_first_n_letterindices_asc(first_n)
    return self.gen_first_n_letterindices_desc(first_n)

  def get_genfirst_n_letterindices(self, first_n=3):
    return list(self.gen_first_n_letterindices(first_n))

  def gen_letterindices_within_range_as_0baseidx_asc(self, start, end):
    while start <= end:
      yield self.tab_let_idx.letterlist.get_as_str_n_reversed()
      start += 1
      self.tab_let_idx.add_one(inplace=True)
      if self.tab_let_idx.is_zeroed():
        return

  def gen_letterindices_within_range_as_0baseidx_desc(self, start, end):
    while start >= end:
      if self.tab_let_idx.letterindex is None or len(self.tab_let_idx.letterindex) == 0:
        return
      yield self.tab_let_idx.letterindex
      start -= 1
      self.tab_let_idx.subtract_one(inplace=True)

  def gen_letterindices_within_range_as_0basedidx(self, start=0, end=100, decrescent=False):
    """
    Generates, as iterator, elements ranging from start to end as 0basedidex.
    This generator can produce both ascendent and descendent iterations.
    Notice that if start > end and it's ascendent, empty will result.
    Likewise, if end < start, and it's descendent, empty will also result.
    """
    if start > end:
      return []
    start = start if start >= 0 else 0
    if not decrescent:
      # ascending: initialize letteridx with 'start'
      self.tab_let_idx = tli.TableauLetterIndex(base0index=start)
      return self.gen_letterindices_within_range_as_0baseidx_asc(start, end)
    else:
      # swap start with end
      tmpvar = end
      end = start
      start = tmpvar
      # descending: initialize letteridx with 'start' after it swapped with 'end'
      self.tab_let_idx = tli.TableauLetterIndex(base0index=start)
      return self.gen_letterindices_within_range_as_0baseidx_desc(start, end)

  def get_genletterindices_within_range_as_0basedidx(self, start=0, end=100, decrescent=False):
    return list(self.gen_letterindices_within_range_as_0basedidx(start, end, decrescent))

  def gen_first_n_base1indices(self, first_n=DEFAULT_FIRST_N_INDICES):
    for i in range(first_n):
      yield i+1
    return

  def get_genfirst_n_base1indices(self, first_n=DEFAULT_FIRST_N_INDICES):
    return list(self.gen_first_n_base1indices(first_n))

  def process(self):
    for i, idx_as_word in enumerate(self.gen_first_n_letterindices()):
      scrmsg = f"{i+1} letterindex {idx_as_word}"
      print(scrmsg)


def adhoctest4():
  ll = llst.LetterList(['a', 'b'])
  print(len(ll), ll)
  ll.insert(0, 'ddd')
  print("insert(0, 'ddd')", ll)
  ll.append('h')
  print("append('h')", ll)
  ll.remove('d')
  print("remove('d')", ll)
  del ll[-1]
  print('delete last dell ll[-1]', len(ll), ll)


def adhoctest6():
  """
  letterindex = 'ab'
  tli = TableauLetterIndex(letteridx)
  print('letteridx', letteridx, 'tli', tli)
  b1idx = 29
  tli = TableauLetterIndex(base1index=b1idx)
  print('letteridx', letteridx, 'tli', tli)
  letterlist = ['D', 'A']
  tli = TableauLetterIndex(letterlist=letterlist)
  print('letteridx', letteridx, 'tli', tli)
  base0index = 31
   letterindex = 'ab'
  tlig = TableauLetterIndexGenerator()
  print('letteridx', letterindex, 'tlig', tlig)
  for ww in tlig.gen_first_n_letterindices():
    print(ww)
  """
  print('decrescent')
  tlig = TableauLetterIndexGenerator()
  for i, letterindex in enumerate(
        tlig.gen_letterindices_within_range_as_0basedidx(
          start=-5, end=27, decrescent=True
        )
    ):
    print(27-i+1, letterindex)
  print('crescent')
  tlig = TableauLetterIndexGenerator()
  for i, letterindex in enumerate(
        tlig.gen_letterindices_within_range_as_0basedidx(
          start=-5, end=27, decrescent=False
        )
    ):
    print(i+1, letterindex)
  print('with range above 100 & crescent')
  tlig = TableauLetterIndexGenerator()
  for i, letterindex in enumerate(
        tlig.gen_letterindices_within_range_as_0basedidx(
          start=100, end=110, decrescent=False
        )
    ):
    tlio = tli.TableauLetterIndex(letterindex=letterindex)
    print(100+i+1, letterindex, tlio)
    return_letterindices = tlig.get_genfirst_n_letterindices(3)
    print('return_letterindices = tlig.get_genfirst_n_letterindices(3)', return_letterindices)



# self.assertEqual(tli3.letteridx, ll3.get_as_str_n_reversed())


def process():
  """
  adhoc_for_groupby()
  adhoctest1()
  adhoctest3()
  adhoctest5()
  """
  adhoctest6()


if __name__ == "__main__":
  process()
