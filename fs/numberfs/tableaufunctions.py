#!/usr/bin/env python3
import math # for math.log(n, base)
import string # for string.ascii_uppercase

import fs.textfs.strfs as strfs

def pick_up_letter_n_number_from_cellref(cellref):
  if cellref is None:
    return None
  cellref = cellref.upper()
  letters = ''
  strnumber = ''
  for c in cellref:
    if c in string.ascii_uppercase:
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
  if cell_letters is None:
    return None
  cell_letters = cell_letters.upper()
  reversed_letters = reversed(list(cell_letters))
  number = 0
  for i, c in enumerate(reversed_letters):
    d = string.ascii_uppercase.index(c)
    if i > 0:
      d += 1
    parcel = d * (26**i)
    number += parcel
  return number

def convert_columnletters_to_number_recursively(cell_letters, to_number=0, pos_order=0):
  '''
    Example:
     AA is 26**1 + 0
  :param cell_letters:
  :param to_number:
  :param pos_order:
  :return:
  '''
  if cell_letters is None:
    return None
  cell_letters = cell_letters.upper()
  if len(cell_letters) > 0:
    pos_letter, cell_letters = strfs.pop_str(cell_letters) # simulates a str.pop() similar to list.pop()
    pos_number = string.ascii_uppercase.index(pos_letter)
    if pos_order > 0:
      pos_number += 1
    to_number += pos_number * (26 ** pos_order)
  if len(cell_letters) > 0:
    return convert_columnletters_to_number_recursively(cell_letters, to_number, pos_order + 1)
  return to_number

def convert_number_to_columnletters_nonrecursively(number):
  letters = ''
  if number > 0:
    decimal_place = int(math.log(number, 26))
  else:
    decimal_place = 0
  remainder = number % 26
  left_to_right_letter = string.ascii_uppercase[remainder]
  letters = left_to_right_letter + letters
  while decimal_place > 0:
    number = number // 26
    decimal_place = int(math.log(number, 26))
    remainder = number % 26
    left_to_right_letter = string.ascii_uppercase[remainder-1]
    letters = left_to_right_letter + letters
    number = number - remainder
  # the combination below should be treated
  if letters.startswith('AZ'):
    letters = letters.lstrip('A')
  return letters

def convert_number_to_columnletters_recursively(number, letters=''):
  '''

  :param cell_letters:
  :param to_number:
  :param pos_order:
  :return:
  '''
  multiple  = number // 26
  remainder = number % 26
  if len(letters) == 0:
    leftwards_digit = string.ascii_uppercase[remainder]
  else:
    leftwards_digit = string.ascii_uppercase[remainder-1]
  letters = leftwards_digit + letters
  if multiple == 0:
    # special case to treat, when letters starts with 'AZ'
    if letters.startswith('AZ'):
      letters = letters.lstrip('A')
    return letters
  else:
    number = (number - remainder) // 26
    return convert_number_to_columnletters_recursively(number, letters)

def move_columns_by(cell_letters, ncolumns):
  '''

  For the time being it works only within A to Z, ie, it doesn't go beyong Z to AA
  And
  :param cell_letters:
  :param ncolumns:
  :return:
  '''
  cell_letters = cell_letters.upper()
  # i = string.ascii_uppercase.index(cell_letters)
  fromcolumn = convert_columnletters_to_number_nonrecursively(cell_letters)
  next_column = fromcolumn + ncolumns # % len(string.ascii_uppercase)
  if next_column < 0:
    error_msg = 'Moved column outside the tableu (negative columns %d)' %next_column
    raise IndexError(error_msg)
  next_cell_letters = convert_number_to_columnletters_nonrecursively(next_column)
  return next_cell_letters

def move_rows_by(number, nrows):
  next_number = number + nrows
  if next_number < 0:
    error_msg = 'Moved row outside the tableu (negative nrows %d)' %next_number
    raise IndexError(error_msg)
  return next_number


def move_cell_along_columns(cellref, ncolumns):
  if cellref is None:
    return None
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
  next_cellref = move_cell_along_rows(cellref, nrows)
  next_cellref = move_cell_along_columns(next_cellref, ncolumns)
  return next_cellref

def adhoc_test1():
  cell_letters = 'zead'
  rec_number = convert_columnletters_to_number_recursively(cell_letters)
  print(cell_letters, '(recurse) =>',  rec_number)
  nonrec_number = convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse) =>',  nonrec_number)
  expected_number = 26*26**3 + 5*26**2 + 1*26**1+ 3
  returned_letters = convert_number_to_columnletters_recursively(nonrec_number)
  print(nonrec_number, '(recurse) =>',  returned_letters, 'expected', expected_number)
  returned_letters = convert_number_to_columnletters_nonrecursively(nonrec_number)
  print(nonrec_number, '(nonrecurse) =>',  returned_letters, 'expected', expected_number)

def adhoc_test2():
  cellref = 'A3'; ncolumns = 4
  next_cellref = move_cell_along_columns(cellref, ncolumns)
  print ('cellref', cellref, 'move', ncolumns, 'results in', next_cellref)
  cellref = next_cellref; ncolumns = -4
  next_cellref = move_cell_along_columns(cellref, ncolumns)
  print ('cellref', cellref, 'move', ncolumns, 'results in', next_cellref)
  ncolumns = 7; nrows = 3
  next_cellref = move_cell_along_tableau(cellref, ncolumns, nrows)
  print ('cellref', cellref, 'move ncolumns', ncolumns, 'move nrows', nrows, 'results in', next_cellref)
  cellref = next_cellref
  ncolumns = -7; nrows = -3
  next_cellref = move_cell_along_tableau(cellref, ncolumns, nrows)
  print ('cellref', cellref, 'move ncolumns', ncolumns, 'move nrows', nrows, 'results in', next_cellref)
  # cellref = next_cellref; ncolumns = 34
  # next_cellref = move_cell_along_columns(cellref, ncolumns)
  cellref = 'A3'; ncolumns = 26+4
  next_cellref = move_cell_along_columns(cellref, ncolumns)
  print ('cellref', cellref, 'move', ncolumns, 'results in', next_cellref)
  cellref = 'A3'; ncolumns = 26*26+26+4
  next_cellref = move_cell_along_columns(cellref, ncolumns)
  print ('cellref', cellref, 'move', ncolumns, 'results in', next_cellref)
  cell_letters = 'D'
  n = convert_columnletters_to_number_recursively(cell_letters)
  cell_letters = 'AA'
  n = convert_columnletters_to_number_recursively(cell_letters)
  print (cell_letters, '=>', n)
  cell_letters = convert_number_to_columnletters_recursively(n)
  print (n, '=>', cell_letters)
  cell_letters = 'CB'
  n = convert_columnletters_to_number_recursively(cell_letters)
  print (cell_letters, '=>', n)
  cell_letters = convert_number_to_columnletters_recursively(n)
  print (n, '=>', cell_letters)
  '''
  cellref = next_cellref; ncolumns = -(26*26+26+4)
  next_cellref = move_cell_along_columns(cellref, ncolumns)
  print ('cellref', cellref, 'move', ncolumns, 'results in', next_cellref)
  '''

def adhoc_test3():
  column_as_number = 0 # 'A'
  letters = convert_number_to_columnletters_recursively(column_as_number)
  print(column_as_number, '=>', letters)
  column_as_number = (1*26)+0 # 'AA'
  letters = convert_number_to_columnletters_recursively(column_as_number)
  print(column_as_number, '=>', letters)
  column_as_number = (1*26)+1 # 'AB'
  letters = convert_number_to_columnletters_recursively(column_as_number)
  print(column_as_number, '=>', letters)
  column_as_number = (2*26*26)+((3-1)*26)+(4-1) # 'BCD'
  letters = convert_number_to_columnletters_recursively(column_as_number)
  print(column_as_number, '=>', letters)
  column_as_number = (2*26*26)+(0*26)+3 # 'BAD'
  letters = convert_number_to_columnletters_recursively(column_as_number)
  print(column_as_number, '=>', letters)
  cell_letters = 'AC'
  n = convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse =>', n)
  cell_letters = convert_number_to_columnletters_nonrecursively(n)
  print(n, '(nonrecurse) =>',  cell_letters)
  n = convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse =>', n)
  cell_letters = convert_number_to_columnletters_nonrecursively(n)
  print(n, '(nonrecurse) =>',  cell_letters)
  cell_letters = 'DBC'
  n = convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse =>', n)
  cell_letters = convert_number_to_columnletters_nonrecursively(n)
  print(n, '(nonrecurse) =>',  cell_letters)

def adhoc_test4():
  '''
  cell_letters = 'zeaD'
  returned_number = convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse) =>',  returned_number)
  expected_number = 26 * 26 ** 3 + 5 * 26 ** 2 + 1 * 26 ** 1 + 3
  returned_letters = convert_number_to_columnletters_nonrecursively(returned_number)
  print(returned_number, '(nonrecurse) =>',  returned_letters)

  :return:
  '''
  # 4 forward
  cell_letters = 'zz'
  returned_number = convert_columnletters_to_number_nonrecursively(cell_letters)
  print(cell_letters, '(nonrecurse) =>',  returned_number)
  expected_number = 26*26 + 25
  returned_letters = convert_number_to_columnletters_nonrecursively(returned_number)
  print(returned_number, '(nonrecurse) =>',  returned_letters)


def process():
  # adhoc_test()
  adhoc_test1()

if __name__ == "__main__":
  process()

