#!/usr/bin/env python3
"""
fs/numberfs/numfunctions.py
  contains various numbers functions.


INDEX_LETTERS = 'Z' + string.ascii_uppercase[:-1]
"""
# import math # for math.log(n, base)
import itertools
import random
import string # for string.ascii_uppercase
INDEX_LETTERS = '*' + string.ascii_uppercase
ALPH_SIZE = len(INDEX_LETTERS)


def idx_to_letter_notation_nonrecursive(n: int):
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


def trans_word_to_int_dropping_decplaces_if_any(word):
  if word is None:
    return None
  if isinstance(word, int):
    return word
  numberstr = ''
  word = word.strip(' \t\r\n')
  entered = False
  for c in word:
    if c in string.digits:
      numberstr += c
      entered = True
    elif not entered:
      continue
    else:
      break
  if numberstr == '':
    return None
  intnumber = int(numberstr)
  return intnumber


def adhoc_test1():
  """
  Inputs and outputs below
  i = '234,4 blah'; o = 234
  i = '234.5 blah'; o = 234
  i = 'a234.5 blah'; o = 234
  i = ' \t 23foo4.5 blah'; o = 23
  """
  word = '234,4 blah'
  leftnumber = trans_word_to_int_dropping_decplaces_if_any(word)
  print(word , '=>', leftnumber)
  word = '234.5 blah'
  leftnumber = trans_word_to_int_dropping_decplaces_if_any(word)
  print(word , '=>', leftnumber)
  word = 'a234.5 blah'
  leftnumber = trans_word_to_int_dropping_decplaces_if_any(word)
  print(word , '=>', leftnumber)
  word = ' \t 23foo4.5 blah'
  leftnumber = trans_word_to_int_dropping_decplaces_if_any(word)
  print(word , '=>', leftnumber)


def adhoc_test2():
  """
    letters = idx_to_letter_notation_nonrecursive(n)
    print(n, n+1, letters,)
    for j in itertools.groupby(range(4)):
  """
  for n in range(26*3):
    letters = idx_to_letter_notation_nonrecursive(n)
    scrmsg = f"{n} {n+1}-{letters}"
    print(scrmsg)
  print('ALPH_SIZE with *', ALPH_SIZE)


def adhoc_test3():
  for n in [3, 4, 6*2, 26]:
    letters = idx_to_letter_notation_nonrecursive(n)
    scrmsg = f"base0index={n} base0index={n+1} letterindex={letters}"
    print(scrmsg)
  print('ALPH_SIZE with *', ALPH_SIZE, INDEX_LETTERS)


def callable1():
  for i in range(10):
    yield random.randint(1, 10)


def adhoc_for_groupby():
  """
  Reminding: it's not in fact groupby(), but printing by 'chunks'
  (Laravel & possibly Django have 'chunk' functions for outputting)
  The solution for prints is possibly viable via a
    customized 'divide_chunks()' function
  A chunk loop is something like:
  for chunk_function in iterator_function:
    for element in chunk_function:
      process(element)
  """
  r10 = range(10)
  for k, g in itertools.groupby(r10):  # , callable1
    print(k, dir(g))


def process():
  """
  adhoc_for_groupby()
  """
  adhoc_test3()
  adhoc_test1()


if __name__ == "__main__":
  process()
