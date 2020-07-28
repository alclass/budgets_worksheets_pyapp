#!/usr/bin/env python3
import math # for math.log(n, base)
import string # for ZERO_PLUS_UPPERCASE_ASCII_LETTERS

import fs.textfs.strfs as strfs

ZERO_PLUS_UPPERCASE_ASCII_LETTERS = '0' + string.ascii_uppercase
NSYSTEM27SIZE = len(ZERO_PLUS_UPPERCASE_ASCII_LETTERS)

def pick_up_letter_n_number_from_cellref(cellref):
  if cellref is None:
    return None
  cellref = cellref.upper()
  letters = ''
  strnumber = ''
  for c in cellref:
    if c in ZERO_PLUS_UPPERCASE_ASCII_LETTERS:
      letters += c
    elif c in string.digits:
      strnumber += c
  number = int(strnumber)
  return letters, number

def convert_columnletters_to_number_nonrecursively(cell_letters):
  '''
  Instead of "consuming and recursing", this routine calculates "number" as a series sumation.

  Example:
    'BCD' has the following number system equivalence:
      (2*26*26)+((3-1)*26)+(4-1) #
    Abstracting the summation, it is:
      n = (il[pN]*(26**N)) + ... + (il[p2]*(26**2))+(il[p1]*(26**1))+(il[p0]*(26**0)) # 'BCD'

    or, in the other direction:
      n = (il[p0]*(26**0)) + (il[p1]*(26**1)) + (il[p2]*(26**2)) + ... + (il[pN]*(26**N))

  :param cell_letters:
  :return: (int) number
  '''
  if cell_letters is None or cell_letters == '':
    return None
  cell_letters = cell_letters.upper()
  reversed_letters = reversed(list(cell_letters))
  number = 0
  for decimal_place, c in enumerate(reversed_letters):
    decimal_equiv = ZERO_PLUS_UPPERCASE_ASCII_LETTERS.index(c)
    parcel = decimal_equiv * (NSYSTEM27SIZE ** decimal_place)
    number += parcel
  return number

def convert_columnletters_to_number_recursively(cell_letters, to_number=0, pos_order=0):
  '''
  This function is PRIVATE, ie, it should only be called by:
    convert_columnletters_to_number_recursively_entrance(cell_letters):

  Explanation: the column letters are mapped to a 27-base number system where 0 is excluded.
  Examples:
    A is 1 (0 is not allowed)
    B is 2
    Z is 26
    AA is = (1*27**1)+1 ie it's 28
    B is  = (1*27**1)+2 ie it's 29
    Z is  = (1*27**1)+26 ie it's 53
  Generally:
    l(pN)...l(p2)l(p1)l(p0) is
    number = nlp0*(27**0) + nlp1*(27**1) + nlp2*(27**2) + ... + nlpN*(27**pN)

  :param cell_letters:
  :param to_number:
  :param pos_order:
  :return:
  '''
  cell_letters = cell_letters.upper()
  if len(cell_letters) > 0:
    pos_letter, cell_letters = strfs.pop_str(cell_letters) # simulates a str.pop() similar to list.pop()
    pos_number = ZERO_PLUS_UPPERCASE_ASCII_LETTERS.index(pos_letter)
    to_number += pos_number * (NSYSTEM27SIZE ** pos_order)
  if len(cell_letters) > 0:
    return convert_columnletters_to_number_recursively(cell_letters, to_number, pos_order + 1)
  return to_number

def convert_columnletters_to_number_recursively_entrance(cell_letters):
  if cell_letters is None or cell_letters == '':
    return None
  return convert_columnletters_to_number_recursively(cell_letters)

def convert_number_to_columnletters_nonrecursively(number):
  letters = ''
  if number == 0: # number cannot be 0, return None
    return None
  decimal_place = int(math.log(number, NSYSTEM27SIZE))
  remainder = number % NSYSTEM27SIZE
  if remainder == 0: # a shift happens in these cases, eg, Z+1 is A0, but A0 should be jumped over arriving at AA (this is a one-forward shift)
    return None # the move call is able to treat this
  left_to_right_letter = ZERO_PLUS_UPPERCASE_ASCII_LETTERS[remainder]
  letters = left_to_right_letter + letters
  while decimal_place > 0:
    number = number // NSYSTEM27SIZE
    decimal_place = int(math.log(number, NSYSTEM27SIZE))
    remainder = number % NSYSTEM27SIZE
    if remainder == 0:  # remainder cannot be 0, return None
      return None
    left_to_right_letter = ZERO_PLUS_UPPERCASE_ASCII_LETTERS[remainder]
    letters = left_to_right_letter + letters
    number = number - remainder
  return letters

def convert_number_to_columnletters_recursively(number, letters=''):
  '''

  :param cell_letters:
  :param to_number:
  :param pos_order:
  :return:
  '''
  multiple  = number // NSYSTEM27SIZE
  remainder = number % NSYSTEM27SIZE
  leftwards_digit = ZERO_PLUS_UPPERCASE_ASCII_LETTERS[remainder]
  letters = leftwards_digit + letters
  if multiple == 0:
    return letters
  else:
    number = (number - remainder) // NSYSTEM27SIZE
    return convert_number_to_columnletters_recursively(number, letters)

def move_columns_by(cell_letters, ncolumns, with_recursive=False):
  '''

  IMPORTANT:
    There's a limitation in the algorithms here so that addition results are,
      in some cases, not unique. Let's see why:

    The letters-number system is implements under a number system conversion scheme without zero.
    In comparison to the decimal number system, this is like have holes in the integers, as illustrated below:
      1,2,3..., 9, 11, 12, 13, ..., 19, 21, 22, ..., 99, 111, 112, 113, and so on.

    Because of that, 111 can be the result of 99+1 and,
      compoundedly, some operations may not be commutative.

    What to do?
    1) one option is to find out a new algorithm;
    2) another option is to allow only additions of less than 27 (base size)
       and then allow only one possible jump (1-shift).
       ie, moves across the tableau should be below 27 places (cells).

  :param cell_letters:
  :param ncolumns:
  :return:
  '''
  if cell_letters is None:
    return None
  cell_letters = cell_letters.upper()
  # i = ZERO_PLUS_UPPERCASE_ASCII_LETTERS.index(cell_letters)
  if with_recursive:
    fromcolumn = convert_columnletters_to_number_recursively(cell_letters)
  else:
    fromcolumn = convert_columnletters_to_number_nonrecursively(cell_letters)
  next_column = fromcolumn + ncolumns
  if next_column <= 0:
    error_msg = 'Moved column outside the tableu (negative columns %d)' %next_column
    raise IndexError(error_msg)
  if with_recursive:
    next_cell_letters = convert_number_to_columnletters_recursively(next_column)
  else:
    next_cell_letters = convert_number_to_columnletters_nonrecursively(next_column)
  while next_cell_letters is None:
    if ncolumns < 0:
      # at this point, ncolumns is, at least, in the operation AA-1 which needs to jump from A0 (not valid) to Z (=26)
      ncolumns -= 1
      next_column = fromcolumn + ncolumns
      if with_recursive:
        next_cell_letters = convert_number_to_columnletters_recursively(next_column)
      else:
        next_cell_letters = convert_number_to_columnletters_nonrecursively(next_column)
    else:
      ncolumns += 1
      next_column = fromcolumn + ncolumns
      if with_recursive:
        next_cell_letters = convert_number_to_columnletters_recursively(next_column)
      else:
        next_cell_letters = convert_number_to_columnletters_nonrecursively(next_column)

  return next_cell_letters

def move_rows_by(number, nrows):
  if nrows == 0:
    return number
  next_number = number + nrows
  if next_number < 0:
    error_msg = 'Moved row outside the tableu (negative nrows %d)' %next_number
    raise IndexError(error_msg)
  return next_number

def move_cell_along_columns(cellref, ncolumns):
  if cellref is None:
    return cellref
  if cellref == '':
    return cellref
  if ncolumns == 0:
    return cellref
  cellref = cellref.upper()
  cell_letters, row_number = pick_up_letter_n_number_from_cellref(cellref)
  next_letters = move_columns_by(cell_letters, ncolumns)
  next_cellref = next_letters + str(row_number)
  return next_cellref

def move_cell_along_rows(cellref, nrows):
  if cellref is None:
    return None
  cellref = cellref.upper()
  cell_letters, number = pick_up_letter_n_number_from_cellref(cellref)
  number = move_rows_by(number, nrows)
  next_cellref = '%s%d' %(cell_letters, number)
  return next_cellref

def move_cell_along_tableau(cellref, ncolumns, nrows):
  if cellref is None:
    return None
  cellref = cellref.upper()
  if nrows == 0 and ncolumns == 0:
    # no moving happens here
    return cellref
  next_cellref = None
  if nrows != 0:
    next_cellref = move_cell_along_rows(cellref, nrows)
  if ncolumns != 0:
    next_cellref = move_cell_along_columns(next_cellref, ncolumns)
  return next_cellref

def adhoc_test():
  '''
    See adhoc tests as a module in the same folder as this file's one.
  :return:
  '''
  pass

def process():
  adhoc_test()

if __name__ == "__main__":
  process()

