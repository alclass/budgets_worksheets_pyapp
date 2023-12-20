#!/usr/bin/env python3
"""
fs/numberfs/tableau_letter_index.py
  contains functions that computes with a tableau (ie an x-y matrix or worksheet).

These are useful to constructing a worksheet when column parameter is a letter-index.

The two main functionalities are:
  a) gen_first_n_letterindices a letterindex from a numberindex, and
  a) gen_first_n_letterindices a numberindex from a letterindex

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
    This class models a data-object that represents a "letterindex" as a kind of letter-number-system item.
    To see it as an example, consider the following series:
      "ground", A, B, C, ..., X, Y, Z, AA, AB, AC ...
    Where:
      "ground" symbolizes a kind of zero or empty item,
      A is mapped to the first integer, ie 1
      B is mapped to the second integer, ie 2
      C is mapped to the third integer, ie 3
      (...)
      Z is mapped to the 26th integer, ie 26
      AA is mapped to the 27th integer, ie 27
      and so on theorically ad infinitum

    So, in a nutshell, each item in the series above may be represented by an instance of this class.

    Further to the two main attributes (letterindex & base_1index),
      two others are derived from the former two ones, they are:
    a) letterlist => derived from letterindex, but, in this implementation, it's the other way around;
    b) base_0index => derived from base_1index;

    At the time of this writing, two methods are available, ie:
      add_one()
      subtract_one()

    Taking into consideration the methods above, this class can be used either mutably or immutably.
    a) Example of an immutable use:
      suppose an instanciated object "tli_o"
        tli_o.add_one(inplace=False) will return another object with its "number" added to one,
        the object acted upon keeps its letterindex intact;
    b) Example of a mutable use:
      suppose an instanciated object "tli_o"
        tli_o.add_one(inplace=True) will not return another object, but will have with its own "number" added to one.

    More examples:
      letter A, as the first letter, has a 0-based index value 0 and a 1-based index as 1
      letter B, as the second letter, has a 0-based index value 1 and a 1-based index as 2
      (...)
      letter Z, as the last letter, has a 0-based index value 25 and a 1-based index as 26
    After Z, the next letterindex is AA having base_0index=26 & b1_idx=27
      Then AB, AC, AD, ..., AY, AZ, BB, BA and so on.


  Info on instance variable letterlist:
    1) it belongs to class that inherits from UserList (class LetterList);
    2) it represents the letterindex as a reversed list,
      e.g. if letterindex = 'BACE', letterlist should be = ['E', 'C', 'A', 'B'] (order reversed)
    """
    # it's sort of an implement choice to have letterindex derived from letterlist, it could be the other way around
    self.base1index = None
    self.letterlist = None
    # base_0index is derived from base_1index (aka b1_idx), it could be the other way around, but seemed more logical so
    self.raise_value_error_if_all_are_none(letterindex, base1index, letterlist, base0index)
    isground = self.init_conditions_for_ground(letterindex, base1index, letterlist, base0index)
    if isground:
      return
    self.treat_the_two_attributes(letterindex, base1index, letterlist, base0index)

  @property
  def is_ground(self):
    if len(self.letterindex) == 0:
      return True

  @staticmethod
  def raise_value_error_if_all_are_none(
      letterindex=None, base1index=None, letterlist=None, base0index=None
  ):
    if letterindex is None:
      if letterlist is None:
        if base0index is None:
          if base1index is None:
            error_msg = f"""Cannot instantiate TableauLetterIndex with all four init attributes as None:
              letterindex (={letterindex}), letterlist (={letterindex}) 
              based0 (={base0index}), based1 ({base1index}) indices"""
            raise ValueError(error_msg)

  def treat_the_two_attributes(
      self, letterindex=None, base1index=None, letterlist=None, base0index=None
  ):
    """
    The precedence order is:
      1st self.letterindex: if it's good, no other parameter is verified;
      2nd self.letterlist: idem;
      3rd self.base1index: idem;
      4th self.base0index;
    """
    if letterindex is not None:
      self.init_letterlist_via_letterindex(letterindex)
      return
    if base1index is not None:
      self.init_via_base1idx(base1index)
      return
    if letterlist is not None:
      self.init_via_letterlist(letterlist)
      return
    if base0index is not None:
      base1index = int(base0index) + 1
      self.init_via_base1idx(base1index)

  def init_conditions_for_ground(
      self, letterindex=None, base1index=None, letterlist=None, base0index=None
  ):
    # conditions for ground/zero
    if letterindex is not None and letterindex == '':
      self.letterlist = llst.LetterList([])
      self.base1index = 0
      return True
    if letterlist is not None and len(letterlist) == 0:
      self.letterlist = llst.LetterList([])
      self.base1index = 0
      return True
    # notice that 0 and None both returns False for boolean-conditions
    # because of that "if x is not None" is required instead of the simpler "if x"
    if base1index is not None and base1index == 0:
      self.letterlist = llst.LetterList([])
      self.base1index = 0
      return True
    if base0index is not None and base0index == -1:
      self.letterlist = llst.LetterList([])
      self.base1index = 0
      return True
    return False

  @property
  def base0index(self):
    """
    Notice that just "if base1_index:", here, is not correct,
      for when an int is 0, it resolves as a boolean False
    Because of that, a try-block returns a correct b0_idx when b1_idx is 0
    """
    try:
      i = int(self.base1index)
      return i - 1
    except (TypeError, ValueError):
      pass
    return None

  @property
  def letterindex(self):
    letterindex = None
    if isinstance(self.letterlist, llst.LetterList):
      letterindex = self.letterlist.get_as_str_n_reversed()
    if self.letterlist is None or len(self.letterlist) == 0:
      self.letterlist = llst.LetterList([])
      letterindex = ''
    return letterindex

  def init_via_letterlist(self):
    self.letterlist = self.letterlist or []
    plist = list(self.letterlist)
    self.letterlist = llst.LetterList(plist)  # instantiated from a child class of UserList
    if self.base1index is None:
      self.base1index = idxfs.get_1basedindex_from_letterlist_left_to_right(self.letterindex)

  def init_letterlist_via_letterindex(self, letterindex):
    letterindex = letterindex or ''
    if letterindex == '':
      self.letterlist = llst.LetterList([])
      self.base1index = 0
      return
    self.make_letterlist_from_letterindex(letterindex)
    self.init_via_letterlist()

  def init_via_base1idx(self, base1index):
    self.base1index = int(base1index)
    if self.base1index < 0:
      error_msg = f"base1index (={self.base1index}) cannot be less than 0 (zero)"
      raise ValueError(error_msg)
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
      self.base1index = idxfs.get_1basedindex_from_letterlist_left_to_right(self.letterindex)

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
      idxfs.subtract_one_from_letterlist_nonrecursive_bysideeffect(self.letterlist, input_reversed=True)
      self.base1index -= 1
      return
    # from here, object is not mutated, inplace=False, another instance is returned
    letterlist = copy.copy(self.letterlist)
    idxfs.subtract_one_from_letterlist_nonrecursive_bysideeffect(letterlist, input_reversed=True)
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
    b1idx_summed = b1idx_a + b1idx_b
    tbi = TableauLetterIndex(base1index=b1idx_summed)
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
    outstr = f"letterindex='{self.letterindex}', base1index={self.base1index}, letterlist={self.letterlist}"
    return outstr


def adhoctest():
  """
  letterindex = 'a'
  to = TableauLetterIndex(letterindex=letterindex)
  print(letterindex, '=>', to)
  letterlist = ['a']
  to = TableauLetterIndex(letterlist=letterlist)
  print(letterlist, '=>', to)
  to.add_one(inplace=True)
  print('to.add_one(inplace=True)', to)
  to2 = to.add_one(inplace=False)
  print('to.add_one(inplace=False)', 'to', to, 'to2', to2)
  letterlist = ['b', 'a']
  to = TableauLetterIndex(letterlist=letterlist)
  print('letterlist', letterlist, 'to =', to)
  letterlist = ['a', 'b']
  to = TableauLetterIndex(letterlist=letterlist)
  print('letterlist', letterlist, 'to =', to)
  to2 = to.subtract_one(inplace=False)
  print('to2 is to.subtract_one(inplace=False)', 'to2', to2)
  to = TableauLetterIndex(letterlist=[])
  print(to)
  """
  to = TableauLetterIndex(base0index=27)
  print(to)


def process():
  """
  adhoc_for_groupby()
  adhoctest3()
  adhoctest5()
  """
  adhoctest()


if __name__ == "__main__":
  process()
