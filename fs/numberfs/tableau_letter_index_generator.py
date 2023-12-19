#!/usr/bin/env python3
"""
fs/numberfs/tableau_letter_index_generator.py

"""
import string
import fs.numberfs.letterlist_inherited as llst  # .LetterList
import fs.numberfs.indexfunctions as idxfs  # .get_1basedindex_from_letterindex
import fs.numberfs.tableau_letter_index as tli  # .TableauLetterIndex
MAX_LOOP_CYCLES = 200
ASCII_26_UPPERCASE_LETTERS = string.ascii_uppercase


class TableauLetterIndexGenerator:

  def __init__(self):
    """
    The instance variable tbi is immutable, so it's reinstanciated after each operation
    """
    self.tab_let_idx = None

  def generate_first_n_letterindices(self, first_n=3):
    self.tab_let_idx = tli.TableauLetterIndex(letterindex='A')
    for i in range(first_n):
      yield self.tab_let_idx.letterindex
      self.tab_let_idx.add_one(inplace=True)

  def generate_letterindices_within_range_as_0baseidx_asc(self, start, end):
    while start <= end:
      yield self.tab_let_idx.letterlist.get_as_str_n_reversed()
      start += 1
      self.tab_let_idx.subtract_one(inplace=True)
      if self.tab_let_idx.is_zeroed():
        return

  def generate_letterindices_within_range_as_0baseidx_desc(self, start, end):
    while start >= end:
      if self.tab_let_idx.letterindex is None or len(self.tab_let_idx.letterindex) == 0:
        return
      yield self.tab_let_idx.letterindex
      start -= 1
      self.tab_let_idx.subtract_one(inplace=True)

  def generate_letterindices_within_range_as_0basedidx(self, start=0, end=100, decrescent=False):
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
      return self.generate_letterindices_within_range_as_0baseidx_asc(start, end)
    else:
      # swap start with end
      tmpvar = end
      end = start
      start = tmpvar
      # descending: initialize letteridx with 'start' after it swapped with 'end'
      self.tab_let_idx = tli.TableauLetterIndex(base0index=start)
      return self.generate_letterindices_within_range_as_0baseidx_desc(start, end)

  @staticmethod
  def generate_first_n_base1indices(first_n):
    for i in range(first_n):
      yield i+1

  def process(self):
    for i, idx_as_word in enumerate(self.generate_first_n_letterindices()):
      scrmsg = f"{i+1} letterindex {idx_as_word}"
      print(scrmsg)


def adhoctest1():
  """
  sg.process()
  ret = sg.set_1basedidx_transposing_from_letterindex('aa')
  sg.process()
  word = 'aa'
  print(word, 'set_1basedidx_transposing_from_letterindex', ret)

  b1idx = 53
  letteridx = sg.set_letterindex_transposing_from_1basedindex(b1idx)
  print('letteridx for b1idx', b1idx, letteridx)
  """
  sg = TableauLetterIndexGenerator()
  total_to_gen = 800
  letterindices = list(sg.generate_first_n_letterindices(total_to_gen))
  b1indices = list(sg.generate_first_n_base1indices(total_to_gen))
  for i in range(total_to_gen):
    letteridx = letterindices[i]
    b1idx = b1indices[i]
    returned_letteridx = sg.set_letterindex_transposing_from_1basedindex(b1idx)
    returned_b1idx = sg.set_1basedidx_transposing_from_letterindex(letteridx)
    print(b1idx, returned_b1idx)
    print(letteridx, returned_letteridx)


def adhoctest2():
  """
  li = list(sg.generate_first_n_letterindices(53))
  print(li)
  for i in range(25, 54):
    returned_letteridx = sg.set_letterindex_transposing_from_1basedindex(i)
    print(i, returned_letteridx)

  b1idx = 10000
  returned_letteridx = sg.set_letterindex_transposing_from_1basedindex(b1idx)
  print(b1idx, 'returned_letteridx', returned_letteridx)
  letteridx_param = 'PTN'
  returned_b1idx2 = sg.set_1basedidx_transposing_from_letterindex(returned_letteridx)
  print('returned_b1idx2', returned_b1idx2, returned_letteridx)
  returned_b1idx = sg.set_1basedidx_transposing_from_letterindex(letteridx_param)
  print(letteridx_param, returned_b1idx)
  returned_letteridx2 = sg.set_letterindex_transposing_from_1basedindex(returned_b1idx)
  print(returned_b1idx, 'returned_letteridx2', returned_letteridx2)
  sg.ongoing_letter_digits = ['B']
  sg.subtract_one_from_letterindex_nonrecursive()
  print('B minus 1', sg.letteridx, sg.ongoing_letter_digits)
  sg.ongoing_letter_digits = ['a']
  sg.subtract_one_from_letterindex_nonrecursive()
  print('a minus 1', sg.letteridx, sg.ongoing_letter_digits)
  letteridx = 'AA'
  sg.set_ongo_letter_list_from_letteridx(letteridx)
  sg.subtract_one_from_letterindex_nonrecursive()
  print(letteridx, 'minus 1', sg.letteridx, sg.ongoing_letter_digits)

  """
  sg = TableauLetterIndexGenerator()
  letteridx = 'AAB'
  sg.letterlist.reset_w_letteridx(letteridx)
  print(letteridx, sg.letteridx, sg.letterlist, 'minus 1')
  sg.letteridx_minus_1()
  print(letteridx, 'minus 1', sg.letteridx, sg.letterlist)
  letteridx = 'AAA'
  sg.letterlist.reset_w_letteridx(letteridx)
  sg.letteridx_minus_1()
  print(letteridx, 'last one, minus 1', sg.letteridx, sg.letterlist)
  letteridx = sg.letteridx
  sg.letteridx_plus_1()
  print(letteridx, 'last one, plus 1', sg.letteridx, sg.letterlist)
  ongo, end = 3, 53
  print('adhoctest crescent ongo, end', ongo, end)
  for idx in sg.generate_letterindices_within_range_as_0basedidx(start=ongo, end=end):
    print('idx', idx, ongo+1)
    ongo += 1
  ongo, end = 28, 2
  print('adhoctest decrescent ongo, end', ongo, end)
  for idx in sg.generate_letterindices_within_range_as_0basedidx(start=ongo, end=end, decrescent=True):
    print('idx', idx, ongo+1)
    ongo -= 1


def adhoctest3():
  """
  Obs: the generator, specially for letterindices, generates sequencially started at 0-based index 0.
  If an arbitrary "high" index is wanted, it may be gotten from the functions tested above.
  # t1 same as t1 in the method-test above
  # but comparing the 800 first b1_indices with their corresponding letterindices
  """
  total_to_gen = 8
  idxgen = TableauLetterIndexGenerator()
  letterindices = list(idxgen.generate_first_n_letterindices(total_to_gen))
  b1indices = list(idxgen.generate_first_n_base1indices(total_to_gen))
  for i in range(4, total_to_gen):
    letteridx = letterindices[i]
    b1idx = b1indices[i]
    returned_letteridx = idxgen.set_letterindex_transposing_from_1basedindex(b1idx)
    returned_b1idx = idxgen.set_1basedidx_transposing_from_letterindex(letteridx)
    print('b1idx', b1idx, 'returned_b1idx', returned_b1idx, 'returned_letteridx',
          returned_letteridx, 'letteridx [', letteridx, ']')


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
  """
  letterindex = 'ab'
  tlig = TableauLetterIndexGenerator()
  print('letteridx', letterindex, 'tlig', tlig)
  for ww in tlig.generate_first_n_letterindices():
    print(ww)
  tlig = TableauLetterIndexGenerator()
  for i, letterindex in enumerate(
        tlig.generate_letterindices_within_range_as_0basedidx(
          start=-5, end=27, decrescent=True
        )
    ):
    print(27-i+1, letterindex)


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
