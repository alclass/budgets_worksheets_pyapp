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
  Contains:
   => two transforming functions, one from letteridx to 1-based_idx and another as its reserve;
   => some arithmetic functions (adding, subtracting, multiplying letterindices)

  There are also 0-based_idx transforming, but the 0-based_idx is just the 1-based_idx minus 1.
  """

  def __init__(self, plist=None):
    """
    The instance variable here (ongo_letter_list) is transient, for what it means
      that it is a sort of working variable, valid during processing;
      ie it's used for the transformation under action and is not useful
      before or after the transforming.

More on ongo_letter_list:
  1) it belongs to class that inherits from UserList;
  2) it represents the letterindex as a reversed list,
    e.g. if letterindex = 'BACE', ongo_letter_list should be = ['E', 'C', 'A', 'B']
  3) along processes, it's not reconstructed/reinstantiated,
     it uses method clear(), though implemented reset(), to clean up for restarting;
    """
    plist = plist or []
    plist = list(plist)
    self.ongo_letter_list = llst.LetterList(plist)  # instantiated from a child class of UserList

  @property
  def letteridx(self):
    return self.ongo_letter_list.get_as_str_n_reversed()

  def transpose_to_letteridx_from_a_given_1basedidx(self, b1idx, recursed=False):
    """
    Returns the letteridx associated with the base1_index input.
    It follows an algorithm that does:
      1st -> extracts mod 26, ie the remainder of division by 26 (the quantity of letters)
      2nd -> integer-divides by 26, diminish one digit for next iteration
             (notice that the dividend is "rolling number" minus 1 [@see algorithm below])

    Examples:
      b1_idx 1 => letteridx A
      b1_idx 2 => letteridx B
      b1_idx 3 => letteridx C
      (...)
      b1_idx 26 => letteridx Z
      b1_idx 27 => letteridx AA
      (...)
      b1_idx 52 => letteridx AZ
      b1_idx 53 => letteridx BA
      (...)
    """
    if not recursed:
      self.ongo_letter_list.reset()
    digit_idx = b1idx % 26
    letter = ASCII_26_UPPERCASE_LETTERS[digit_idx-1]
    self.ongo_letter_list.append(letter)
    # this is necessary to adjust the "vai_um", ie after Z it's AA, after AZ, it's BA and so on
    # without the adjusting "minus 1", the Z above would be AZ and AZ would be BZ...
    b1idx -= 1
    number_divided_by_base = b1idx // 26
    if number_divided_by_base > 0:
      return self.transpose_to_letteridx_from_a_given_1basedidx(number_divided_by_base, True)
    return self.letteridx

  @property
  def base1idx(self):
    return self.transpose_to_1basedidx_from_a_given_letteridx(self.letteridx)

  def transpose_to_1basedidx_from_a_given_letteridx(self, word):
    """
    This conversion/transform follows the summation:
      idx_as_soma = SumOf (idx(c[i])+1) * 26 ** pwr
    where c[i] represents the characters in word & idx(c[i]) is the index of character from 0 (A) to 25 (Z).

    Example (seen in the last method's docstring):
      b1_idx 53 => letteridx BA
      B alone is b1_index 2 (1+1), A alone is b1_index 1 (0+1); doing the summation S it gets:
      S = 2*26**1 + 1*26**0 = 52 + 1 = 53
    """
    verify_or_raise_letterindices_word(word)
    wordlist = list(str(word).upper())
    reversed_wordlist = reversed(wordlist)
    idx_as_soma, pwr = 0, 0
    for pwr, letter in enumerate(reversed_wordlist):
      idx = ASCII_26_UPPERCASE_LETTERS.index(letter)
      idx_as_soma += (idx+1) * 26 ** pwr
    # if it got here, process has finished calculus of 1based_idx
    self.ongo_letter_list.reset_w_letteridx(word)
    return idx_as_soma

  def transpose_to_letteridx_from_0basedidx(self, b0idx):
    return self.transpose_to_letteridx_from_a_given_1basedidx(b0idx + 1)

  def transpose_to_0basedidx_from_letteridx(self, word):
    return self.transpose_to_1basedidx_from_a_given_letteridx(word)

  def __eq__(self, o):
    try:
      if self.letteridx == o.letteridx:
        return True
    except (AttributeError, TypeError):
      pass
    return False

  def __add__(self, o):
    b1idx_a = self.base1idx
    b1idx_b = o.base1idx
    toachieve = b1idx_a + b1idx_b - 1
    tbi = TableauLetterIndex()
    tbi.transpose_to_letteridx_from_0basedidx(toachieve)
    return tbi

  def __sub__(self, o):
    b1idx_a = self.base1idx
    b1idx_b = o.base1idx
    toachieve = b1idx_a - b1idx_b - 1
    if toachieve < 0:
      return None
    tbi = TableauLetterIndex()
    tbi.transpose_to_letteridx_from_0basedidx(toachieve)
    return tbi

  def __str__(self):
    outstr = f"letteridx={self.letteridx}, based1idx={self.base1idx}"
    return outstr


class TableauLetterIndexGenerator(TableauLetterIndex):

  def __init__(self, plist=None):
    super().__init__(plist)

  @staticmethod
  def add_one_to_single_letter(letter: str):
    letter = letter.upper()
    vai_um = False
    if letter == 'Z':
      changed_letter = 'A'
      vai_um = True
    else:
      idx = ASCII_26_UPPERCASE_LETTERS.index(letter)
      changed_letter = ASCII_26_UPPERCASE_LETTERS[idx + 1]
    return changed_letter, vai_um

  @staticmethod
  def subtract_one_to_single_letter(letter: str):
    """
    propagate_to_the_right is signaled if letter is returned as 'Z'
    """
    letter = letter.upper()
    if letter == 'A':
      changed_letter = 'Z'
    else:
      idx = ASCII_26_UPPERCASE_LETTERS.index(letter)
      changed_letter = ASCII_26_UPPERCASE_LETTERS[idx - 1]
    return changed_letter

  def add_one_to_letter_index_recursive_left_to_right_letter(self, pos=0):
    """
    """
    if pos == len(self.ongo_letter_list):
      # because ongoing_letter_digits is private,
      # insert must be indirect
      self.ongo_letter_list.insert(0, 'A')
      return
    letter = self.ongo_letter_list[pos]
    changed_letter, vai_um = self.add_one_to_single_letter(letter)
    self.ongo_letter_list[pos] = changed_letter
    if vai_um:
      return self.add_one_to_letter_index_recursive_left_to_right_letter(pos + 1)

  def letteridx_plus_1(self):
    return self.add_one_to_letter_index_recursive_left_to_right_letter()

  def subtract_one_to_letter_index_recursive_left_to_right_letter(self, pos=0):
    letter = self.ongo_letter_list[pos]
    changed_letter = self.subtract_one_to_single_letter(letter)
    self.ongo_letter_list[pos] = changed_letter
    if changed_letter == 'Z':
      if pos == len(self.ongo_letter_list) - 1:
        before = self.letteridx
        self.ongo_letter_list.pop()
        print(before, 'last step ->', self.letteridx, 'must be empty')
        return
      return self.subtract_one_to_letter_index_recursive_left_to_right_letter(pos+1)

  def letteridx_minus_1(self):
    return self.subtract_one_to_letter_index_recursive_left_to_right_letter()

  def generate_first_n_letterindices(self, first_n=3):
    self.ongo_letter_list.reset()
    for i in range(first_n):
      self.add_one_to_letter_index_recursive_left_to_right_letter()
      yield self.letteridx

  def generate_letterindices_within_range_as_0baseidx_asc(self, start, end):
    while start <= end:
      yield self.letteridx
      start += 1
      self.letteridx_plus_1()

  def generate_letterindices_within_range_as_0baseidx_desc(self, start, end):
    while start >= end:
      yield self.letteridx
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
    self.ongo_letter_list.reset()
    self.transpose_to_letteridx_from_0basedidx(start)
    if not decrescent:
      # ascending: initialize letteridx with 'start'
      self.transpose_to_letteridx_from_0basedidx(start)
      return self.generate_letterindices_within_range_as_0baseidx_asc(start, end)
    else:
      # swap start with end
      tmpvar = end
      end = start
      start = tmpvar
      # descending: initialize letteridx with 'start' after it swapped with 'end'
      self.transpose_to_letteridx_from_0basedidx(start)
      return self.generate_letterindices_within_range_as_0baseidx_desc(start, end)

  @staticmethod
  def generate_first_n_base1indices(first_n):
    for i in range(first_n):
      yield i+1

  def process(self):
    for i, idx_as_word in enumerate(self.generate_first_n_letterindices()):
      comp_idx = self.transpose_to_1basedidx_from_a_given_letteridx(idx_as_word)
      print(i, i+1, idx_as_word, comp_idx)


def adhoctest1():
  """
  sg.process()
  ret = sg.transpose_to_1basedidx_from_a_given_letteridx('aa')
  sg.process()
  word = 'aa'
  print(word, 'transpose_to_1basedidx_from_a_given_letteridx', ret)

  b1idx = 53
  letteridx = sg.transpose_to_letteridx_from_a_given_1basedidx(b1idx)
  print('letteridx for b1idx', b1idx, letteridx)
  """
  sg = TableauLetterIndexGenerator()
  total_to_gen = 800
  letterindices = list(sg.generate_first_n_letterindices(total_to_gen))
  b1indices = list(sg.generate_first_n_base1indices(total_to_gen))
  for i in range(total_to_gen):
    letteridx = letterindices[i]
    b1idx = b1indices[i]
    returned_letteridx = sg.transpose_to_letteridx_from_a_given_1basedidx(b1idx)
    returned_b1idx = sg.transpose_to_1basedidx_from_a_given_letteridx(letteridx)
    print(b1idx, returned_b1idx)
    print(letteridx, returned_letteridx)


def adhoctest2():
  """
  li = list(sg.generate_first_n_letterindices(53))
  print(li)
  for i in range(25, 54):
    returned_letteridx = sg.transpose_to_letteridx_from_a_given_1basedidx(i)
    print(i, returned_letteridx)

  b1idx = 10000
  returned_letteridx = sg.transpose_to_letteridx_from_a_given_1basedidx(b1idx)
  print(b1idx, 'returned_letteridx', returned_letteridx)
  letteridx_param = 'PTN'
  returned_b1idx2 = sg.transpose_to_1basedidx_from_a_given_letteridx(returned_letteridx)
  print('returned_b1idx2', returned_b1idx2, returned_letteridx)
  returned_b1idx = sg.transpose_to_1basedidx_from_a_given_letteridx(letteridx_param)
  print(letteridx_param, returned_b1idx)
  returned_letteridx2 = sg.transpose_to_letteridx_from_a_given_1basedidx(returned_b1idx)
  print(returned_b1idx, 'returned_letteridx2', returned_letteridx2)
  sg.ongoing_letter_digits = ['B']
  sg.subtract_one_to_letter_index_recursive_left_to_right_letter()
  print('B minus 1', sg.letteridx, sg.ongoing_letter_digits)
  sg.ongoing_letter_digits = ['a']
  sg.subtract_one_to_letter_index_recursive_left_to_right_letter()
  print('a minus 1', sg.letteridx, sg.ongoing_letter_digits)
  letteridx = 'AA'
  sg.set_ongo_letter_list_from_letteridx(letteridx)
  sg.subtract_one_to_letter_index_recursive_left_to_right_letter()
  print(letteridx, 'minus 1', sg.letteridx, sg.ongoing_letter_digits)

  """
  sg = TableauLetterIndexGenerator()
  letteridx = 'AAB'
  sg.ongo_letter_list.reset_w_letteridx(letteridx)
  print(letteridx, sg.letteridx, sg.ongo_letter_list, 'minus 1')
  sg.letteridx_minus_1()
  print(letteridx, 'minus 1', sg.letteridx, sg.ongo_letter_list)
  letteridx = 'AAA'
  sg.ongo_letter_list.reset_w_letteridx(letteridx)
  sg.letteridx_minus_1()
  print(letteridx, 'last one, minus 1', sg.letteridx, sg.ongo_letter_list)
  letteridx = sg.letteridx
  sg.letteridx_plus_1()
  print(letteridx, 'last one, plus 1', sg.letteridx, sg.ongo_letter_list)
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
    returned_letteridx = idxgen.transpose_to_letteridx_from_a_given_1basedidx(b1idx)
    returned_b1idx = idxgen.transpose_to_1basedidx_from_a_given_letteridx(letteridx)
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
  tli1.transpose_to_letteridx_from_0basedidx(2)
  tli2.transpose_to_letteridx_from_0basedidx(3)
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
  ll1 = llst.LetterList(tli1.letteridx)
  ll2 = llst.LetterList(tli2.letteridx)
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


# self.assertEqual(tli3.letteridx, ll3.get_as_str_n_reversed())


def process():
  """
  adhoc_for_groupby()
  adhoctest1()
  """
  adhoctest3()
  adhoctest5()


if __name__ == "__main__":
  process()
