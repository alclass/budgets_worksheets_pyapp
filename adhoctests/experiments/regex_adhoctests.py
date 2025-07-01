#!/usr/bin/env python3
"""

"""
import re


def adhoctest2():
  # repattern = r'^(\d[4]\-\d[4]\s[1].+?[\.prettyprint\.dat]$)'
  fn = '2025-2025 CUUR0000SA0.prettyprint.dat'
  # repattern = r'(^\d{4}\-\d{4}).*'
  repattern = r'^(\d{4}\-\d{4}\s{1}.+?\.prettyprint\.dat)$'
  print('fn', fn)
  print('repattern', repattern)
  match = re.search(repattern, fn)
  found = None if match is None else match.group(1)
  scrmsg = f"match = {found}"
  print(scrmsg)
  repattern = r'^(\.\w+)'
  recomp = re.compile(repattern)
  strtest = '.filename'
  match = re.search(repattern, strtest)
  print(match)
  matchcomp = recomp.search(strtest)
  print('matchcomp', matchcomp)
  repattern = r'(^\w+)'
  strtest = 'filename'
  match = re.search(repattern, strtest)
  print(match)
  repattern = r'(^begin\s\w+\send$)'
  strtest = 'begin adldfjaçlkfj end'
  match = re.search(repattern, strtest)
  print(match)


def adhoctest1():
  """
  https://www.kaggle.com/code/albeffe/regex-exercises-solutions
  https://www.w3resource.com/python-exercises/re/
  https://learnbyexample.github.io/py_regular_expressions/Exercise_solutions.html
  https://pythonistaplanet.com/python-regex-exercises/
  https://realpython.com/regex-python/
  https://www.rexegg.com/regex-boundaries.php

  """
  fn = '2025-2025 CUUR0000SA0.prettyprint.dat'
  scrmsg = f"filename = {fn}"
  print(scrmsg)


if __name__ == '__main__':
  """
  process()
  """
  adhoctest2()
