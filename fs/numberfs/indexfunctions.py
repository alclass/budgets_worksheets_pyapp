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


def get_1basedindex_from_letterindex(letteridx):
  """
  This conversion/transform follows the summation:
    idx_as_soma = SumOf (idx(c[i])+1) * 26 ** pwr
  where c[i] represents the characters in word & idx(c[i]) is the index of character from 0 (A) to 25 (Z).

  Example (seen in the last method's docstring):
    b1_idx 53 => letteridx BA
    B alone is b1_index 2 (1+1), A alone is b1_index 1 (0+1); doing the summation S it gets:
    S = 2*26**1 + 1*26**0 = 52 + 1 = 53
  """
  if letteridx is None:
    error_msg = f"Cannot find the 1-based index without letterindex existing."
    raise ValueError(error_msg)
  # verify_or_raise_letterindices_word()
  wordlist = list(str(letteridx).upper())
  reversed_wordlist = list(reversed(wordlist))
  letterlist = llst.LetterList(reversed_wordlist)
  idx_as_soma, pwr = 0, 0
  for pwr, letter in enumerate(letterlist):
    idx = ASCII_26_UPPERCASE_LETTERS.index(letter)
    idx_as_soma += (idx + 1) * 26 ** pwr
  # if it got here, process has finished calculus of 1based_idx
  b1idx = idx_as_soma
  return b1idx


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


def add_one_to_letter_index_recursive_left_to_right_letter(letterlist, pos=0):
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
    return add_one_to_letter_index_recursive_left_to_right_letter(letterlist, pos+1)
  return letterlist


def adhoctest():
  letteridx = 'ab'
  b1idx = get_1basedindex_from_letterindex(letteridx)
  scrmsg = f"letteridx={letteridx}, b1idx={b1idx}"
  print(scrmsg)
  ret_letteridx = get_letterlist_from_1basedindex(b1idx)
  scrmsg = f"ret_letteridx={ret_letteridx}, b1idx={b1idx}"
  print(scrmsg)
  ret_letteridx = get_letterindex_from_1basedindex(b1idx)
  scrmsg = f"ret_letteridx={ret_letteridx}, b1idx={b1idx}"
  print(scrmsg)


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


def subtract_one_from_reversed_letterlist_nonrecursive(letterlist: list, pos=0):
  """
  letterlist is not reversed here, ie it represents letterindex directy
  Example:
    letterlist = ['A', 'B'] is letterindex 'AB' not 'BA'
  """
  # condition that returns [] rightaway
  if letterlist is None or len(letterlist) == 0:
    return []
  # upper() all letters to guarantee "all caps"
  letterlist = map(lambda c: c.upper(), letterlist)
  # only A to Z allowed
  letterlist = list(filter(lambda c: c in ASCII_26_UPPERCASE_LETTERS, letterlist))
  # condition that intends to diminish 1 from A, which should be [] (empty list)
  if len(letterlist) == 1 and letterlist[0] == 'A':
    return []
  pos = 0
  vai_um = False
  while pos < len(letterlist):
    letter = letterlist[pos]
    changed_letter = subtract_one_to_single_letter(letter)
    letterlist[pos] = changed_letter
    if changed_letter == 'Z':
      if pos == len(letterlist) - 2:
        del letterlist[-1]
      else:
        pos += 1
    break
  return letterlist


def subtract_one_from_letterindex_nonrecursive(letterindex):
  """
  Example:
    B minus 1 is A
    Z minus 1 is Y
    A minus 1, as a one-digit, is None (a sort of "end of line")
    AA minus 1 is Z
    etc
  """
  # letterlist is not reversed here
  letterlist = list(letterindex)
  letterlist = subtract_one_from_reversed_letterlist_nonrecursive(letterlist)
  if len(letterlist) == 0:
    return None
  letterindex = ''.join(reversed(letterlist))
  return letterindex


def adhoctest():
  letterindex = list('abc')
  letterlist = llst.trans_letterindex_as_reversed_letterlist(letterindex)
  ll = llst.LetterList(inputlist=letterlist)
  res = subtract_one_from_reversed_letterlist_nonrecursive(ll)
  print('letterindex', letterindex, 'translist', ll, 'subtract_one', res)
  letterindex = list('aa')
  letterlist = llst.trans_letterindex_as_reversed_letterlist(letterindex)
  ll = llst.LetterList(inputlist=letterlist)
  res = subtract_one_from_reversed_letterlist_nonrecursive(ll)
  print('letterindex', letterindex, 'translist', ll, 'subtract_one', res)


def process():
  """
  adhoc_for_groupby()
  adhoctest1()
  """
  pass


if __name__ == "__main__":
  process()
  adhoctest()
