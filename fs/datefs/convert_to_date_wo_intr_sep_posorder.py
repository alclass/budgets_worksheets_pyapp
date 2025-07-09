#!/usr/bin/env python3
"""
fs/datefs/convert_to_date_wo_intr_sep_posorder.py
  Has functions for converting str's or attr_obj's into datetime. date's

Differently from the introspect_dates.py modules, it does not use parameters used by the latter, ie:

  a) sep (separator) => STRDATE_SEPARATORS = ['-', '/', '.'] or
  b) posorder => ORDERPOS_TOKENS_AVAILABLE = ['ymd', 'ydm', 'dmy', 'mdy']

Because of that, only the two following formats are acceptable here:
  a) either yyyy-mm-dd (mm & dd don't need to have a leftzero if less than 10) or
    e.g. 2023-1-1
  b) yyyymmdd in which case mm & dd need to have a leftzero if less than 10
    e.g. 20230101

Also:
  the convertion here accepts an object that implements the three integer attributes: year, month & day.
    e.g. an object such as collection.namedtuple('Name', fields=['year', 'month', day']
      of course, in the case above, the final consistency check will be taken
      through datetime. date's constructor.
"""
import datetime


def convert_str_or_attrsobj_to_date_or_none(str_or_obj):
  """
    Tries to tranform/convert parameter pdate into a datetime. date value, or else returns None.

  The input is tested for 'date' in 5 subsequent conversion-tests, ie:
    1 if it's a datetime. date itself or a subclass of it (which is returned rightaway) or
    2 if it's an object that contains, as properties, the int attributes year, month & day
    3 if it's an object whose str-repr has the prefix form "yyyy-mm-dd" ie,
    at_least_1digit_year-1or2digit_month-1or2digit_day
    4 if all above failed, it tries to find a date in a string of the form "yyyymmdd" without the "-" separator
  param: pdate object | string | None
  output: datetime. date | None

  if issubclass(datetime.date, type(str_or_obj)):
    return str_or_obj
  """
  if str_or_obj is None:
    return None
  if isinstance(str_or_obj, datetime.date):
    # notice that a datetime.datetime object may also "enter" here,
    # so, also because of unit-test equality necessity, a datetime.date must be reconstructed for the output
    o = str_or_obj
    return datetime.date(year=o.year, month=o.month, day=o.day)
  try:
    # in this first try, aim is to find an object that contains the 3 integer attrs named: year, month & day
    o = str_or_obj
    year = int(o.year)
    month = int(o.month)
    day = int(o.day)
    return datetime.date(year=year, month=month, day=day)
  except (AttributeError, TypeError, ValueError):
    # AttributeError catches the lack of the attribute
    # ValueError catches in case int(n) fails
    # TypeError is necessary because an object's inner attribute may be None
    pass
  try:
    str_or_obj = str(str_or_obj)[:10]
    pp = str_or_obj.split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = int(pp[2])
    return datetime.date(year=year, month=month, day=day)
  except (IndexError, ValueError):
    # IndexError catches whether the indexed element (ie e[i]) does not exist
    # ValueError catches in case int(n) fails
    # * TypeError is not necessary for is-None has already been checked above
    pass
  # last try with a strdate without separators (ie yyyymmdd instead of yyyy-mm-dd)
  return make_date_or_none_wo_separators(str_or_obj)


def is_date_weekend(pdate):
  try:
    weekidx = pdate.weekday()
    # 5 is Saturday, 6 is Sunday
    if weekidx in [5, 6]:
      return True
    return False
  except TypeError:
    pass
  return False


def find_most_recent_name_n_its_prefix_date_in_strlist(strlist):
  if strlist is None or len(strlist) == 0:
    return None, None
  tuplelist = [(e, make_date_or_none(e[:10])) for e in strlist if len(e)>9]
  tuplelist = sorted([te for te in tuplelist if te[1] is not None])
  if len(tuplelist) == 0:
    return None, None
  most_recent_name, pdate = tuplelist[0]
  return most_recent_name, pdate


def make_date_or_none_wo_separators(pdate):
  """
  Transforms/converts an 8-char string under the form yyyymmdd (without '-') into datetime. date
    Notice
      a) strdate is this case must have 8-char and all of them must be integer
      b) the datetime. date constructor itself does the validation/consistency of the date
  """
  if pdate is None:
    return None
  try:
    strdate = str(pdate)
    year = int(strdate[:4])
    month = int(strdate[4:6])
    day = int(strdate[6:8])
    return datetime.date(year=year, month=month, day=day)
  except (IndexError, ValueError):
    pass
  return None


def make_date_or_none(pdate):
  """
  Just an alias to the main function
  """
  return convert_str_or_attrsobj_to_date_or_none(pdate)


def make_date_or_today(pdate: str | datetime.date | None = None) -> datetime.date | None:
  """
    Calls the main function for converting to a date.
    If receives a None, returns 'today'.

  Reminder that:
    b) this function uses make_date_or_none() (which is itself an alias of the main function)
    a) both forms: yyyy-mm-dd & yyyymmdd are tried from here
  """
  pdate = make_date_or_none(pdate)
  if pdate is None:
    return datetime.date.today()
  return pdate


def make_date_from_str_or_none(strdate):
  """
  Just an alias to the main function
  """
  return convert_str_or_attrsobj_to_date_or_none(strdate)


def adhoc_test():
  class C1:
    def __init__(self, year=None, month=None, day=None):
      self.year = year
      self.month = month
      self.day = day

  y, m, d = 2020, 7, 3
  expected_date = datetime.date(year=y, month=m, day=d)
  attrs_obj = C1(y, m, d)
  returned_date = make_date_or_none(attrs_obj)
  print('attrs_obj', attrs_obj.year)
  print(expected_date, returned_date)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
