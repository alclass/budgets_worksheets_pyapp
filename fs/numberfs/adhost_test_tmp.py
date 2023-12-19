#!/usr/bin/env python3
'''
  Adhoc Tests to tableaufunctions.py
  See also the unit tests in folder under its conventioned filename.
'''
import fs.numberfs.tableaufunctions as tblfs


class Tes:

  def __init__(self, a=1):
    self.a = a

  def add_one(self, inplace=True):
    if inplace:
      self.a += 1
      return
    return __class__(self.a+1)

  def __str__(self):
    outstr = f"<class Tes a={self.a}>"
    return outstr


def adhoctest():
  t = Tes()
  print(t)
  ret = t.add_one()
  print('add one inplace', t, 'ret', ret)
  ret = t.add_one(inplace=False)
  print('add one inplace', t, 'ret', ret)


def process():
  pass


if __name__ == "__main__":
  process()
  adhoctest()

