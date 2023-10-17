#!/usr/bin/env python3
"""
collfunctions.py
  This script contains functions related to collections.
  At this moment:
  1) function remake_namedtuple_with_dict()
     reconstructs a named-tuple replacing some of its fields.
  2) remake_namedtuple_with_a_pair_namevalue()
     an envelope to the first function above
"""
import collections as coll
# noinspection PyProtectedMember


def remake_namedtuple_with_dict(
    replacingdict, p_namedtuple, namedtuple_constr_ref
):
  """
    This function allows to reinstantiate a named tuple (an immutable type)
      when there is some need to change one or more of its fields.
    Here follows the procedure for this "virtual modfication"
      (in fact, the construction of a new one with the changes):

      1) convert it to an OrderedDict (with method _asdict() on namedtuple);
      2) then to a dict;
      3) include the (replacefield, value) pair and
      4) then convert it back to the namedtuple.
  """
  try:
    ntdict = p_namedtuple._asdict()  # returns an OrderedDict
    ntdict.update(replacingdict)
    new_namedtuple = namedtuple_constr_ref(**ntdict)  # convert it back to a new namedtuple
    return new_namedtuple
  except AttributeError:
    pass
  return None


def remake_namedtuple_with_a_pair_namevalue(
    fieldname, value, p_namedtuple, namedtuple_constr_ref
):
  try:
    replacingdict = {fieldname: value}
  except (NameError,  ValueError):
    # either NameError or ValueError was raised, return None
    return None
  return remake_namedtuple_with_dict(
    replacingdict, p_namedtuple, namedtuple_constr_ref
  )


def adhoctest2():
  """
  adhoctest2()
  """
  namedtuple_constr_test = coll.namedtuple(
    'NTest2', 'name descr qtd date'
  )
  original_namedtuple = namedtuple_constr_test(
    name='a name', descr='a descr', qtd=3, date='any date'
  )
  fieldname = 'date'
  value = '2023-10-17'
  changed_namedtuple = remake_namedtuple_with_a_pair_namevalue(
    fieldname, value, original_namedtuple, namedtuple_constr_test
  )
  print('2 === Adhoctest =========')
  print('2-1 changing pair (the one that will modify namedtuple => date =', value)
  print('2-2 original_namedtuple =>', original_namedtuple)
  print('2-3 After remake_namedtuple_with_dict()')
  print('2-4 changed_namedtuple =>', changed_namedtuple)


def adhoctest():
  """
  In this adhoctest, one wants to change field named msg from a namedtuple.
  As we know, a namedtuple is immutable, so a new one is created from
    an updated dict.
  """
  namedtuple_constr_test = coll.namedtuple(
    'NTest', 'field1 field2 field3 msg'
  )
  original_namedtuple = namedtuple_constr_test(
    field1='bla', field2='blah', field3='hi hi', msg=None
  )
  replacingdict = {'msg': 'a replacing message'}
  changed_namedtuple = remake_namedtuple_with_dict(
    replacingdict, original_namedtuple, namedtuple_constr_test
  )
  print('1 === Adhoctest =========')
  print('1-1 changingdict (the one that will modify namedtuple =>', replacingdict)
  print('1-2 original_namedtuple =>', original_namedtuple)
  print('1-3 After remake_namedtuple_with_dict()')
  print('1-4 changed_namedtuple =>', changed_namedtuple)


def process():
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoctest()
  adhoctest2()
