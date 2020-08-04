#!/usr/bin/env python3
import collections as coll

namedtuple_constr = coll.namedtuple('NTest', 'field1 field2 field3 msg')


def reinstantiate_named_tuple_replacing_one_field(replacefield, value, p_namedtuple, namedtuple_constr_ref):
  """
    This function allows to reinstantiate a named tuple when there is a need to change one field.
    The namedtuple is immutable, so the trick here is:
      1) to convert it to an OrderedDict,
      2) then to a dict,
      3) include the (replacefield, value) pair and
      4) then convert it back to the namedtuple.

  :param p_namedtuple:
  :param replacefield:
  :return:
  """
  try:
    pdict = p_namedtuple._asdict()  # returns an OrderedDict
    pdict = dict(pdict)  # returns a dict
    pdict[replacefield] = value  # add the replacefield and value
    new_namedtuple = namedtuple_constr_ref(**pdict)
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
  print(p_namedtuple)


if __name__ == "__main__":
  process()
