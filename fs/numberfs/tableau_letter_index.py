#!/usr/bin/env python3
"""
fs/numberfs/tableau_letter_index.py
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
import copy
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

  def __init__(self, letterindex=None, base1index=None, letterlist=None, base0index=None):
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
    self.letterlist = None
    self.base1index = None
    # letterindex is derived from letterlist
    self._letterindex = None
    # base0index is derived from base1index (aka b1idx)
    self._base0index = None  # derived from
    if letterindex:
      self.init_letterlist_via_letterindex(letterindex)
    elif letterlist:
      self.letterlist = letterlist
      self.init_via_letterlist()
    if base1index:
      self.base1index = int(base1index)
      self.init_via_base1idx()
    elif base0index:
      self.base1index = int(base0index) + 1
      self.init_via_base1idx()
    if self.letterlist is None:
      error_msg = f"""
      Cannot instantiate TableauLetterIndex without either:
        letterindex (={letterindex}), letterlist (={letterindex}) 
        based0 (={base1index}), based1 ({base1index}) indices"""
      raise ValueError(error_msg)

  @property
  def base0index(self):
    if self.base1index:
      return self.base1index - 1
    return None

  @property
  def letterindex(self):
    if self.letterlist:
      return self.letterlist.get_as_str_n_reversed()
    return None

  def init_via_letterlist(self):
    self.letterlist = self.letterlist or []
    plist = list(self.letterlist)
    self.letterlist = llst.LetterList(plist)  # instantiated from a child class of UserList
    if self.base1index is None:
      self.base1index = idxfs.get_1basedindex_from_letterindex(self.letterindex)

  def init_letterlist_via_letterindex(self, letterindex):
    letterindex = letterindex or ''
    self.make_letterlist_from_letterindex(letterindex)
    self.init_via_letterlist()

  def init_via_base1idx(self):
    self.set_letterindex_transposing_from_1basedindex()

  def make_letterlist_from_letterindex(self, letterindex):
    # notice that letteridx is reversed in relation to letterlist
    reversed_letteridx_list = ''
    try:
      reversed_letteridx_list = list(reversed(list(str(letterindex).upper())))
    except TypeError:
      self.letterlist = []
      self.base1index = 0
    self.letterlist = llst.LetterList(reversed_letteridx_list)
    ret_letteridx = self.letterlist.get_as_str_n_reversed()
    if self.letterindex != ret_letteridx:
      # this is also unit-tested, so this happening is virtually imposible
      error_msg = f"Programming error: self._letteridx ={letterindex} != ret_letteridx ={ret_letteridx}"
      raise ValueError(error_msg)

  def set_letterindex_transposing_from_1basedindex(self):
    if self.letterlist is None:
      letterindex = idxfs.get_letterindex_from_1basedindex(self.base1index)
      self.make_letterlist_from_letterindex(letterindex)

  def set_1basedidx_transposing_from_letterindex(self):
    if self.base1index is None:
      self.base1index = idxfs.get_1basedindex_from_letterindex(self.letterindex)

  def add_one(self, inplace=True):
    if inplace:
      idxfs.add_one_to_letterlist_recursive_left_to_right(self.letterlist)
      self.base1index += 1
      return
    # from here, object is not mutated, inplace=False, another instance is returned
    letterlist = copy.copy(self.letterlist)
    idxfs.add_one_to_letterlist_recursive_left_to_right(letterlist)
    return __class__(letterlist=letterlist, base1index=self.base1index+1)

  def subtract_one(self, inplace=True):
    """
    reversed_letterlist = idxfs.subtract_one_from_letterindex_nonrecursive(self.tab_let_idx.letterlist)
    """
    if inplace:
      idxfs.subtract_one_from_reversed_letterlist_nonrecursive(self.letterlist)
      self.base1index -= 1
      return
    # from here, object is not mutated, inplace=False, another instance is returned
    letterlist = copy.copy(self.letterlist)
    idxfs.subtract_one_from_reversed_letterlist_nonrecursive(letterlist)
    return __class__(letterlist=letterlist, base1index=self.base1index-1)

  def is_zeroed(self):
    if len(self.letterlist) == 0:
      return True
    return False

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


def adhoctest():
  """
  """
  to = TableauLetterIndex(letterindex='a')
  print(to)
  to = TableauLetterIndex(letterlist=['a'])
  print(to)
  to = TableauLetterIndex(letterlist=['b', 'a'])
  print(to)
  to.add_one(inplace=True)
  print('to.add_one(inplace=True)', to)
  to2 = to.add_one(inplace=False)
  print('to.add_one(inplace=False)', to, to2)
  to2 = to.subtract_one(inplace=False)
  print('to.add_one(inplace=False)', to, to2)


def process():
  """
  adhoc_for_groupby()
  adhoctest3()
  adhoctest5()
  """
  adhoctest()


if __name__ == "__main__":
  process()
