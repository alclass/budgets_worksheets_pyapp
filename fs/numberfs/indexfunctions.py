#!/usr/bin/env python3
"""
fs/numberfs/indexfunctions.py

  From the time of this writing, two main converting functions are present:

   => one of the two, converts letterindex to based1index
   => the other does the opposite, ie converts based1index to letterindex

  There are also 0-based_idx transforming, but the 0-based_idx is just the 1-based_idx minus 1.
"""
import string
import fs.numberfs.letterlist_inherited as llst  # .LetterList
MAX_LOOP_CYCLES = 200
ASCII_26_UPPERCASE_LETTERS = string.ascii_uppercase


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


def add_one_to_letterlist_recursive_left_to_right(letterlist, pos=0):
  """
  letterlist will be changed "in place" (mutably), ie no need to return it
  """
  if pos == len(letterlist):
    # a new digit is "opened"
    letterlist.insert(0, 'A')
    return letterlist
  letter = letterlist[pos]
  changed_letter, vai_um = add_one_to_single_letter(letter)
  letterlist[pos] = changed_letter
  if vai_um:
    return add_one_to_letterlist_recursive_left_to_right(letterlist, pos + 1)
  # letterlist is changed by "side effect"
  return  # letterlist


def get_0basedindex_from_1basedindex(b1idx):
  return b1idx - 1


def get_1basedindex_from_0basedindex(b0idx):
  return b0idx + 1


def get_letterindex_from_0basedindex(b0idx):
  return get_letterindex_from_1basedindex(get_1basedindex_from_0basedindex(b0idx))


def get_letterindex_from_1basedindex(b1idx):
  letterlist = get_letterlist_from_1basedindex(b1idx)
  return letterlist.get_as_str_n_reversed()


def get_letterlist_from_0basedindex(b0idx, letterlist=None):
  return get_letterlist_from_1basedindex(get_1basedindex_from_0basedindex(b0idx))


def get_letterlist_from_1basedindex(b1idx, letterlist=None):
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
  if letterlist is None:
    letterlist = llst.LetterList()
  digit_idx = b1idx % 26
  letter = ASCII_26_UPPERCASE_LETTERS[digit_idx - 1]
  letterlist.append(letter)
  # this is necessary to adjust the "vai_um", ie after Z it's AA, after AZ, it's BA and so on
  # without the adjusting "minus 1", the Z above would be AZ and AZ would be BZ...
  b1idx -= 1
  number_divided_by_base = b1idx // 26
  if number_divided_by_base > 0:
    # recurse while number_divided_by_base > 0
    return get_letterlist_from_1basedindex(number_divided_by_base, letterlist)
  return letterlist


def get_1basedindex_from_letterindex(letterindex):
  if letterindex is None:
    error_msg = f"Cannot find the 1-based index without letterindex existing."
    raise ValueError(error_msg)
  # verify_or_raise_letterindices_word()
  wordlist = list(str(letterindex).upper())
  reversed_wordlist = list(reversed(wordlist))
  letterlist = llst.LetterList(reversed_wordlist)
  return get_1basedindex_from_letterlist_left_to_right(letterlist)


def get_1basedindex_from_letterlist_right_to_left(letterlist):
  """
  This conversion/transform follows the summation:
    idx_as_soma = SumOf (idx(c[i])+1) * 26 ** pwr
  where c[i] represents the characters in word & idx(c[i]) is the index of character from 0 (A) to 25 (Z).

  Example (seen in the last method's docstring):
    b1_idx 53 => letteridx BA
    B alone is b1_index 2 (1+1), A alone is b1_index 1 (0+1); doing the summation S it gets:
    S = 2*26**1 + 1*26**0 = 52 + 1 = 53


  Notice that is other of the letters is important:
    In the left_to_right calculation, 'AB' is 28 (1based)
    In the right_to_left calculation, 'AB' is the reverse of 'BA' which is 53 (1based)
  """
  if letterlist is None or len(letterlist) == 0:
    return 0
  idx_as_soma, pwr = 0, 0
  for pwr, letter in enumerate(letterlist):
    idx = ASCII_26_UPPERCASE_LETTERS.index(letter)
    idx_as_soma += (idx + 1) * 26 ** pwr
  # if it got here, process has finished calculus of 1based_idx
  b1idx = idx_as_soma
  return b1idx


def get_1basedindex_from_letterlist_left_to_right(letterlist):
  """
  @see above docstring for get_1basedindex_from_letterlist_right_to_left()

  Notice that is other of the letters, then the two functions, is important:
    In the left_to_right calculation, 'AB' is 28 (1based)
    In the right_to_left calculation, 'AB' is the reverse of 'BA' which is 53 (1based)
  """
  if letterlist is None or len(letterlist) == 0:
    return 0
  idx_as_soma, pwr = 0, 0
  reversed_letterlist = list(reversed(letterlist))
  return get_1basedindex_from_letterlist_right_to_left(reversed_letterlist)


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

def subtract_one_from_letterlist_reversed(letterlist):
  """
  Consider this function private, ie, only to be called from
    subtract_one_from_letterlist_nonrecursive_bysideeffect()
  """
  pos = 0
  while pos < len(letterlist):
    letter = letterlist[pos]
    changed_letter = subtract_one_to_single_letter(letter)
    letterlist[pos] = changed_letter
    if changed_letter == 'Z':
      if pos < len(letterlist) - 1:
        pos += 1  # simétrico do "vai um"
        continue
      else:
        del letterlist[pos]
    break
  return letterlist  # the list here was mutated, it's the same object as the input parameter

def subtract_one_from_letterlist_nonreversed(letterlist):
  """
  Consider this function private, ie, only to be called from
    subtract_one_from_letterlist_nonrecursive_bysideeffect()
  """
  pos = len(letterlist) - 1
  while pos > -1:
    letter = letterlist[pos]
    changed_letter = subtract_one_to_single_letter(letter)
    letterlist[pos] = changed_letter
    if changed_letter == 'Z':
      if pos == len(letterlist) - 2:
        del letterlist[-1]
      else:
        pos += 1
    break
  return letterlist  # the list here was mutated, it's the same object as the input parameter


def subtract_one_from_letterlist_nonrecursive_bysideeffect(letterlist: list, input_reversed=False):
  """
  letterlist may or may not be reversed here
    a) when it's not reversed, it represents letterindex "as it is"
      Example:
        letterlist = ['A', 'B'] is letterindex 'AB' not 'BA'
    b) when it's reversed, it represents letterindex "reversed"
      Example:
        letterlist = ['A', 'B'] is letterindex 'BA' not 'AB'

  boolean parameter "input_reversed" controls whether it's one case or the other.
  The difference is the way the while-loop goes (see below), ie
    the non-reversed =>  while pos > -1:
    the reversed =>  while pos < len(letterlist):

  Obs:
    Another "side effect" is that if any lowercase letter exists, it will be uppercased.
  """
  # condition that returns [] rightaway
  if letterlist is None or len(letterlist) == 0:
    return []
  # upper() all letters to guarantee "all caps"
  # do not use the map() function here or list comprehension for they will create a new list
  # the aim here is to change the list mutably, ie by "side effect"
  for i, c in enumerate(letterlist):
    if c != c.upper():
      letterlist[i] = c.upper()
  if len(letterlist) == 1 and letterlist[0] == 'A':
    return llst.LetterList([])
  if not input_reversed:
    return subtract_one_from_letterlist_nonreversed(letterlist)
  return subtract_one_from_letterlist_reversed(letterlist)


def adhoctest():
  """
  letterindex = list('abc')
  letterlist = llst.trans_letterindex_as_reversed_letterlist(letterindex)
  ll = llst.LetterList(inputlist=letterlist)
  res = subtract_one_from_letterlist_nonrecursive_bysideeffect(ll)
  print('letterindex', letterindex, 'translist', ll, 'subtract_one', res)
  letterindex = list('aa')
  letterlist = llst.trans_letterindex_as_reversed_letterlist(letterindex)
  ll = llst.LetterList(inputlist=letterlist)
  res = subtract_one_from_letterlist_nonrecursive_bysideeffect(ll)
  print('letterindex', letterindex, 'translist', ll, 'subtract_one', res)

  """
  ll = ['a', 'b']
  print('ll', ll, 'next subtract one')
  l2 = subtract_one_from_letterlist_nonrecursive_bysideeffect(ll)
  print('ll', ll, 'subtract one', 'l2', l2)
  print('subtracting reversed')
  ll = ['a', 'b']
  print('ll', ll, 'next subtract one')
  l2 = subtract_one_from_letterlist_nonrecursive_bysideeffect(ll, input_reversed=True)
  print('ll', ll, 'subtract one', 'l2', l2)


def adhoctest2():
  letteridx = 'ab'
  b1idx = get_1basedindex_from_letterlist_left_to_right(letteridx)
  scrmsg = f"letteridx={letteridx}, b1idx={b1idx}"
  print(scrmsg)
  ret_letteridx = get_letterlist_from_1basedindex(b1idx)
  scrmsg = f"ret_letteridx={ret_letteridx}, b1idx={b1idx}"
  print(scrmsg)
  ret_letteridx = get_letterindex_from_1basedindex(b1idx)
  scrmsg = f"ret_letteridx={ret_letteridx}, b1idx={b1idx}"
  print(scrmsg)


def process():
  """
  adhoc_for_groupby()
  adhoctest1()
  """
  pass


if __name__ == "__main__":
  process()
  adhoctest()
