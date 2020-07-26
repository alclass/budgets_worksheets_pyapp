#!/usr/bin/env python3
import string

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

def adhoc_test():
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

def process():
  adhoc_test()

if __name__ == "__main__":
  process()
