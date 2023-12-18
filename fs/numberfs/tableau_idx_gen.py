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
import fs.numberfs.letterlist_inherited as llst  # .LetterList
import fs.numberfs.indexfunctions as idxfs  # .get_1basedindex_from_letterindex
MAX_LOOP_CYCLES = 200
ASCII_26_UPPERCASE_LETTERS = string.ascii_uppercase


def verify_or_raise_letterindices_word(word):
  word = str(word)
  boolist = list(map(lambda c: c in ASCII_26_UPPERCASE_LETTERS, word))
  if False in boolist:
    error_msg = (f"word {word} is not a full valid letterindex one,"
                 f" ie it has characters outside of {ASCII_26_UPPERCASE_LETTERS}")
    raise ValueError(error_msg)


class TableauLetterIndex:
  """

  """

  def __init__(self, letterindex=None, base0index=None, base1index=None, letterlist=None):
    """
    This class is to be considered an instantiator of immutable objects.
    The object instantiated is composed of a letterindex and another three equivalent values.
    The four attributes are: letterindex, based0index, based1index, letterlist
      which is an auxiliary variable and represents letterindex as an inverted list.

    For example:
      letter A, as the first letter, has a 0-based index value 0 and a 1-based index as 1
      letter B, as the second letter, has a 0-based index value 1 and a 1-based index as 2
      (...)
      letter Z, as the last letter, has a 0-based index value 25 and a 1-based index as 26
    After Z, the next letterindex is AA having base0index=26 & b1idx=27
      Then AB, AC, AD, ..., AY, AZ, BB, BA and so on.


Info on instance variable ongo_letter_list:
  1) it belongs to class that inherits from UserList;
  2) it represents the letterindex as a reversed list,
    e.g. if letterindex = 'BACE', ongo_letter_list should be = ['E', 'C', 'A', 'B']
  3) along processes, it's not reconstructed/reinstantiated,
     it uses method clear(), though implemented reset(), to clean up for restarting;
    """
    self.letterindex = None
    self.letterlist = None
    self._base0index = None  # derived from b1idx
    self.base1index = None
    if letterindex:
      self.letterindex = str(letterindex).upper()
      self.init_via_letterindex()
    elif letterlist:
      self.letterlist = letterlist
      self.init_via_letterlist()
    elif base1index:
      self.base1index = int(base1index)
      self.init_via_base1idx()
    elif base0index:
      self.base1index = int(base0index) + 1
      self.init_via_base1idx()
    else:
      error_msg = f"""
      Cannot instantiate TableauLetterIndex without either:
        letterindex (={letterindex}, based0 (={base1index}), based1 ({base1index}) indices or
        letterlist (={letterindex}"""
      raise ValueError(error_msg)

  @property
  def base0index(self):
    if self.base1index:
      return self.base1index - 1
    return None

  def init_via_letterlist(self):
    self.letterlist = self.letterlist or []
    plist = list(self.letterlist)
    self.letterlist = llst.LetterList(plist)  # instantiated from a child class of UserList
    self.letterindex = self.letterlist.get_as_str_n_reversed()
    self.base1index = idxfs.get_1basedindex_from_letterindex(self.letterindex)

  def init_via_letterindex(self):
    self.letterindex = self.letterindex or ''
    self.make_letterlist_from_letterindex()
    self.init_via_letterlist()

  def init_via_base1idx(self):
    self.set_letterindex_transposing_from_1basedindex()

  def make_letterlist_from_letterindex(self):
    # notice that letteridx is reversed in relation to letterlist
    reversed_letteridx_list = list(reversed(list(self.letterindex)))
    self.letterlist = llst.LetterList(reversed_letteridx_list)
    ret_letteridx = self.letterlist.get_as_str_n_reversed()
    if self.letterindex != ret_letteridx:
      # this is also unit-tested, so this happening is virtually imposible
      error_msg = f"Programming error: self._letteridx ={self.letterindex} != ret_letteridx ={ret_letteridx}"
      raise ValueError(error_msg)

  def set_letterindex_transposing_from_1basedindex(self):
    self.letterindex = idxfs.get_letterindex_from_1basedindex(self.base1index)
    self.make_letterlist_from_letterindex()

  def set_1basedidx_transposing_from_letterindex(self):
    self_b1idx = idxfs.get_1basedindex_from_letterindex(self.letterindex)

  def __eq__(self, o):
    try:
      if self.letterindex == o.letterindex:
        return True
    except (AttributeError, TypeError):
      pass
    return False

  def __add__(self, o):
    b1idx_a = self.base1index
    b1idx_b = o.base1index
    toachieve = b1idx_a + b1idx_b - 1
    tbi = TableauLetterIndex(base1index=toachieve)
    return tbi

  def __sub__(self, o):
    b1idx_a = self.base1index
    b1idx_b = o.base1index
    toachieve = b1idx_a - b1idx_b - 1
    if toachieve < 0:
      return None
    tbi = TableauLetterIndex(base1index=toachieve)
    return tbi

  def __str__(self):
    outstr = f"letteridx={self.letterindex}, based1idx={self.base1index}, letterlist={self.letterlist}"
    return outstr


class TableauLetterIndexGenerator:

  def __init__(self):
    """
    The instance variable tbi is immutable, so it's reinstanciated after each operation
    """
    self.tab_let_idx = None

  def letteridx_plus_1(self):
    """
    self.tbi is immutable, so the result one is created
    """
    letterlist = idxfs.add_one_to_letter_index_recursive_left_to_right_letter(self.tab_let_idx.letterlist)
    self.tab_let_idx = TableauLetterIndex(letterlist=letterlist)

  def letteridx_minus_1(self):
    reversed_letterlist = idxfs.subtract_one_from_letterindex_nonrecursive(self.tab_let_idx.letterlist)
    if reversed_letterlist is None:
      return
    letterlist = list(reversed(reversed_letterlist))
    self.tab_let_idx = TableauLetterIndex(letterlist=letterlist)

  def generate_first_n_letterindices(self, first_n=3):
    letterlist = llst.LetterList([])
    for i in range(first_n):
      letterlist = idxfs.add_one_to_letter_index_recursive_left_to_right_letter(letterlist)
      self.tab_let_idx = TableauLetterIndex(letterlist=letterlist)
      letterlist = self.tab_let_idx.letterlist
      yield self.tab_let_idx.letterindex

  def generate_letterindices_within_range_as_0baseidx_asc(self, start, end):
    while start <= end:
      yield self.tab_let_idx.letterlist.get_as_str_n_reversed()
      start += 1
      self.letteridx_plus_1()

  def generate_letterindices_within_range_as_0baseidx_desc(self, start, end):
    while start >= end:
      letterindex = self.tab_let_idx.letterlist.get_as_str_n_reversed()
      if letterindex is None:
        return
      yield letterindex
      start -= 1
      self.letteridx_minus_1()

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
      self.tab_let_idx = TableauLetterIndex(base0index=start)
      return self.generate_letterindices_within_range_as_0baseidx_asc(start, end)
    else:
      # swap start with end
      tmpvar = end
      end = start
      start = tmpvar
      # descending: initialize letteridx with 'start' after it swapped with 'end'
      self.tab_let_idx = TableauLetterIndex(base0index=start)
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


def adhoctest5():
  tli1 = TableauLetterIndex()
  tli2 = TableauLetterIndex()
  tli1.set_letterindex_transposing_from_0basedidx(2)
  tli2.set_letterindex_transposing_from_0basedidx(3)
  tli3 = tli1 + tli2
  print('tli1 + tli2 = tli3', tli1, tli2, tli3)
  tli3 = tli2 - tli1
  print('tli2 - tli1 = tli3', tli2, tli1, tli3)
  tli3 = tli1 - tli2
  print('tli1 - tli2 = tli3', tli1, tli2, tli3)
  letter = 'B'
  tli1 = TableauLetterIndex(letter)
  # n1 = tli1.base1idx
  letter = 'D'
  tli2 = TableauLetterIndex(letter)
  # n2 = tli2.base1idx
  tli3 = tli1 + tli2
  print('tli1', tli1, 'tli2', tli2, 'tli3', tli3)
  # n3 = n1 + n2
  direct_n3 = tli3.base1idx
  print('direct_n3 tli3.base1idx', direct_n3)
  ll1 = llst.LetterList(tli1.letterindex)
  ll2 = llst.LetterList(tli2.letterindex)
  # list sum is in fact a concatenation, not an arithmetic
  ll3 = ll1 + ll2
  print('ll1 ll2 ll3', ll1, ll2, ll3)
  tlg1 = TableauLetterIndexGenerator()
  outlist = []
  for li in tlg1.generate_letterindices_within_range_as_0basedidx(start=3, end=7, decrescent=True):
    outlist.append(li)
  print('generate_letterindices_within_range_as_0basedidx', outlist)
  outlist = []
  for li in tlg1.generate_letterindices_within_range_as_0basedidx(start=3, end=7, decrescent=False):
    outlist.append(li)
  print('generate_letterindices_within_range_as_0basedidx', outlist)


def adhoctest6():
  """
  letteridx = 'ab'
  tli = TableauLetterIndex(letteridx)
  print('letteridx', letteridx, 'tli', tli)
  b1idx = 29
  tli = TableauLetterIndex(base1index=b1idx)
  print('letteridx', letteridx, 'tli', tli)
  letterlist = ['D', 'A']
  tli = TableauLetterIndex(letterlist=letterlist)
  print('letteridx', letteridx, 'tli', tli)
  base0index = 31
  tli = TableauLetterIndex(base0index=base0index)
  print('letteridx', letteridx, 'tli', tli)
  for ww in tlig.generate_first_n_letterindices():
    print(ww)
  """
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
