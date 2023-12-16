#!/usr/bin/env python3
"""

"""
import string
from collections import UserList
MAX_LOOP_CYCLES = 200
ASCII_26_UPPERCASE_LETTERS = string.ascii_uppercase


class LetterList(UserList):
  """
  def __init__(self):
    super().__init__()
    self.e = None

  """
  element = None
  position = None

  def __init__(self, plist=None):
    super().__init__([])
    try:
      _ = iter(plist)
    except TypeError:
      plist = []
    try:
      plist = list(plist)
      plist = filter(lambda e: e is not None, plist)
      plist = map(lambda e: str(e).upper(), plist)
      plist = filter(lambda e: e in ASCII_26_UPPERCASE_LETTERS, plist)
      self.extend(plist)
      # _ = [self.exappend(e) for e in plist]
    except (TypeError, ValueError):
      pass

  def __setitem__(self, position, element):
    self.element = element
    self.check_element_or_raise()
    self.position = position
    super().__setitem__(self.position, element)

  def check_element_or_raise(self):
    self.element = str(self.element).upper()
    if self.element not in ASCII_26_UPPERCASE_LETTERS:
      error_msg = f'attempt to append/insert element {self.element} not belonging to {ASCII_26_UPPERCASE_LETTERS}'
      raise ValueError(error_msg)

  def check_position_or_raise(self):
    self.position = self.position or 0
    pos = int(self.position)
    if abs(pos) > len(self):
      error_msg = (f'attempt to append/insert/replace element {self.element} '
                   f'at position {self.position} when size = {len(self)}')
      raise ValueError(error_msg)

  def append_element(self, element):
    self.element = element
    self.check_element_or_raise()
    super().append(self.element)

  def append(self, element):
    if isinstance(element, str):
      if len(element) == 1:
        return self.append_element(element)
      revlist = list(element)
      for e in revlist:
        self.append_element(e)
      return
    try:
      _ = iter(element)
      for e in element:
        self.append_element(e)
      return
    except TypeError:
      pass
    # if it's neither str nor iter, it falls down here for raising an exception
    error_msg = f'element {element} failed to be appended to letterlist'
    raise ValueError(error_msg)

  def reset(self, e_or_l=None):
    self.clear()
    e_or_l = e_or_l or []
    self.append(e_or_l)

  def reset_w_letteridx(self, letteridx):
    kept_letteridx = letteridx
    try:
      reversed_list = reversed(list(str(letteridx)))
      return self.reset(reversed_list)
    except TypeError:
      error_msg = f"can't reset letterlist with letteridx = {kept_letteridx}"
      raise ValueError(error_msg)

  def remove(self, e):
    try:
      if isinstance(e, str):
        if len(e) == 1:
          e = e.upper()
          return super().remove(e)
      le = list(e)
      for e in le:
        self.remove(e)
      return
    except TypeError:
      pass

  def insert_element(self, position, element):
    self.element = element
    self.position = position
    self.check_element_or_raise()
    self.check_position_or_raise()
    super().insert(position, self.element)

  def insert(self, position, element):
    if isinstance(element, str):
      revlist = reversed(list(element))
      for e in revlist:
        self.insert_element(position, e)
    else:
      self.insert_element(position, element)

  def __eq__(self, o):
    try:
      _ = iter(o)
    except TypeError:
      return False
    if len(self) == 0 and len(o) == 0:
      return True
    try:
      boolist = [self[i] == o[i] for i in range(len(self))]
      if boolist:
        return True
    except IndexError:
      pass
    return False

  def get_as_str_n_reversed(self):
    revlist = reversed(list(self))
    return ''.join(revlist)


def adhoctest():
  ll = LetterList(['a', 'c', 'b'])
  print('type(ll)', type(ll), ll)
  ll.insert(0, 'dfxx')
  # ll.remove('x')
  # del ll[-1]
  print(len(ll), type(ll), ll)
  ll.append('blah')
  print(len(ll), type(ll), ll)
  word = 'reset'
  ll.reset(word)
  print(len(ll), word, ll)

  # word = ll.get_as_str_n_reversed()
  # print('get_as_str_n_reversed', word)


def process():
  """
  adhoc_for_groupby()
  adhoctest1()
  """
  adhoctest()


if __name__ == "__main__":
  process()
