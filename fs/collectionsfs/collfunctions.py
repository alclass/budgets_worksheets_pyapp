#!/usr/bin/env python3
import collections as coll

namedtuple_constr = coll.namedtuple('NTest', 'field1 field2 field3 msg')


# noinspection PyProtectedMember
def reinstantiate_named_tuple_replacing_one_field(replacefield, value, p_namedtuple, namedtuple_constr_ref):
  """
    This function allows to reinstantiate a named tuple when there is a need to change one field.
    The namedtuple is immutable, so the trick here is:
      1) to convert it to an OrderedDict;
      obs: the use of method _asdict() on the namedtuple for getting an OrderedDict is complained by the IDE,
           but the underline (_) (meaning private method) was planned to avoid mixing with names not to be a private;
      2) then to a dict;
      3) include the (replacefield, value) pair and
      4) then convert it back to the namedtuple.

  :param replacefield:
  :param value:
  :param p_namedtuple:
  :param namedtuple_constr_ref:
  :return:
  """
  try:
    pdict = p_namedtuple._asdict()  # returns an OrderedDict
    pdict[replacefield] = value  # add the replacefield and value to the OrderedDict
    new_namedtuple = namedtuple_constr_ref(**pdict)  # convert it back to a new namedtuple
    return new_namedtuple
  except AttributeError:
    pass
  return None


def process():
  replacefield = 'msg'
  value = 'a message'
  p_namedtuple = namedtuple_constr(field1='bla', field2='blah', field3='hi hi', msg=None)
  print(p_namedtuple)
  p_namedtuple = reinstantiate_named_tuple_replacing_one_field(replacefield, value, p_namedtuple, namedtuple_constr)
  print('replacefield is [', replacefield, '] | value is [', value, ']')
  print('After reinstantiate_named_tuple_replacing_one_field()')
  print(p_namedtuple)


if __name__ == "__main__":
  process()
