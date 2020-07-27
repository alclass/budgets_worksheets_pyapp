#!/usr/bin/env python3

def pop_str(word):
  if word is None:
    return '', None
  if len(word) == '':
    return '', ''
  last_char = word[-1]
  word = word[ : -1]
  return last_char, word

def pick_first_word(phrase):
  if phrase is None:
    return None
  if ' ' not in phrase:
    return phrase
  return phrase.split(' ')[0]

def process():
  stri = 'sadfadfx'
  c, newstr = pop_str(stri)
  print(stri, 'pop() =>', c, ',', newstr)

if __name__ == "__main__":
  process()

