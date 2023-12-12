#!/usr/bin/env python3
"""
fs/numberfs/numfunctions.py
  contains various numbers functions.

"""
# import math # for math.log(n, base)
import itertools
import random
import string # for string.ascii_uppercase
INDEX_LETTERS = 'Z' + string.ascii_uppercase[:-1]
INDEX_LETTERS = '*' + string.ascii_uppercase
ALPH_SIZE = len(INDEX_LETTERS)


def idx_to_letter_notation(n: int):
  orig = n
  letters_list = []
  if n == 0:
    letter = INDEX_LETTERS[0+1]
    letters_list.append(letter)
  while n > 0:
    remainder = n % 26
    if remainder == 0:
      letter = INDEX_LETTERS[0+1]  # ie 'A'
      letters_list.append(letter)
      n = n // 26 # // is integer division as new to Python3 (in Py2 it was /)
    if n > 26:
      letter = INDEX_LETTERS[remainder+1]
      letters_list.append(letter)
      n = n // 26  # // is integer division as new to Python3 (in Py2 it was /)
    else:
      if n == 0:
        letter = INDEX_LETTERS[remainder+1]
      else:
        letter = INDEX_LETTERS[remainder+1]
      letters_list.append(letter)
      break
    # print(n, letter, remainder)
  letters = ''.join(reversed(letters_list))
  # letters = ''.join(letters_list)
  return letters




def consume_left_side_int_number_w_optional_having_comma_or_point(word):
  if word is None:
    return None
  if type(word) == int: # or type(word) == float:
    return word
  numberstr = ''
  word = word.lstrip(' \t')
  for c in word:
    if c in string.digits:
      numberstr += c
    #elif c in [',','.']:
      #continue
    else:
      break
  if numberstr == '':
    return None
  intnumber = int(numberstr)
  return intnumber



def adhoc_test1():
  word = '234,4 blah'
  leftnumber = consume_left_side_int_number_w_optional_having_comma_or_point(word)
  print(word , '=>', leftnumber)
  word = '234.5 blah'
  leftnumber = consume_left_side_int_number_w_optional_having_comma_or_point(word)
  print(word , '=>', leftnumber)
  word = 'a234.5 blah'
  leftnumber = consume_left_side_int_number_w_optional_having_comma_or_point(word)
  print(word , '=>', leftnumber)
  word = ' \t 234.5 blah'
  leftnumber = consume_left_side_int_number_w_optional_having_comma_or_point(word)
  print(word , '=>', leftnumber)



def adhoc_test3():
  for n in [30, 31, 26*2, 26*2+1]:
    letters = idx_to_letter_notation(n)
    scrmsg = f"{n} {n + 1}-{letters}"
    print(scrmsg)
  print('ALPH_SIZE with *', ALPH_SIZE, INDEX_LETTERS)


def adhoc_test2():
  """
    letters = idx_to_letter_notation(n)
    print(n, n+1, letters,)
    for j in itertools.groupby(range(4)):
  """
  for n in range(26*3):
    letters = idx_to_letter_notation(n)
    scrmsg = f"{n} {n+1}-{letters}"
    print(scrmsg)
  print('ALPH_SIZE with *', ALPH_SIZE)


def callable1():
  for i in range(10):
    yield random.randint(1, 10)


def adhoc_for_groupby():
  """
  Reminding: it's not groupby(), it's printing by chunks
  (Laravel & possibly Django have a chunk functions for outputting)
  The solution for prints is possible a customized 'divide_chunks()' function
  """
  r10 = range(10)
  for k, g in itertools.groupby(r10):  # , callable1
    print(k, dir(g))


def process():
  """
  adhoc_for_groupby()
  """
  adhoc_test3()
  for tt in gen_letter_indices():
    print(tt)
  pass

if __name__ == "__main__":
  process()
