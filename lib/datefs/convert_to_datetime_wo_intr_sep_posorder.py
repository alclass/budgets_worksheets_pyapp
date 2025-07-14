#!/usr/bin/env python3
"""
fs/datefs/convert_to_datetime_wo_intr_sep_posorder.py
  Has functions for converting str's or attr_obj's into datetime. datetime's

The difference from its datetime. date counterpart is that this has more attributes, ie,
  beyond year, month & day, there are hour, minute, second and microsecond

"""
import collections
import datetime
nt_dtymd_constr = collections.namedtuple('NTymd', field_names=['year', 'month', 'day'])
nt_dtym_refmo_constr = collections.namedtuple('NTrefmo', field_names=['year', 'month'])


def make_datetime_n_get_time_via_split_from_strdt(pdatetime):
  dt = make_datetime_w_formatfields_or_none(pdatetime)
  if dt is None:
    return None
  _, dtime = split_date_n_time_from_datetime(dt)
  return dtime


def split_date_n_time_from_datetime(pdatetime):
  if pdatetime is None:
    return None, None
  try:
    pdate = datetime.date(pdatetime.year, pdatetime.month, pdatetime.day)
  except AttributeError:
    return None, None
  try:
    daytime = datetime.time(
      hour=pdatetime.hour, minute=pdatetime.minute, second=pdatetime.second, microsecond=pdatetime.microsecond
    )
  except AttributeError:
    return pdate, None
  return pdate, daytime


def convert_date_to_datetime_or_none(pdate):
  try:
    o = pdate
    y, m, d = int(o.year), int(o.month), int(o.day)
    return datetime.datetime(year=y, month=m, day=d)
  except (AttributeError, TypeError, ValueError):
    pass
  return None


def convert_datetime_to_date_or_none(pdatetime):
  """
  :param pdatetime:
  :return:
  """
  if pdatetime is None:
    return None
  try:
    return datetime.date(pdatetime.year, pdatetime.month, pdatetime.day)
  except AttributeError:
    pass
  return None


def make_datetime_w_formatfields_or_none(wholestr):
  """
  formatstr = '%Y-%m-%d %H:%M:%S.%f'
  """
  if wholestr is None:
    return None
  format_list = ['%Y-%m-%d %H', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f']
  previous_dto = None
  dto = None
  for f_piece in format_list:
    try:
      dto = datetime.datetime.strptime(wholestr, f_piece)
      previous_dto = dto
    except ValueError:
      if previous_dto:
        return previous_dto
      continue
  # Notice that None may be returned
  return dto


def make_datetime_w_fields_or_none(y, m, d, h, mi, s, f):
  """
  The parameters are:
    y => year, m => month, d => day, h => hour, mi => minute, s => second, f => microsecond

  Obs:
    1) at least y, m, d & h must exist for a dto be instanted from datetime.datetime
      if the client called needs a datetime.datetime from a datetime. date,
        he or she must, at least, include the hour field next to y, m & d
    2) a rightmost field depends on that all its leftsize fields are non-None, examples:
      2-a y=1, m=1, d=1, h=1, mi=7, s=15, f => this will recup up to s (second)
      2-b y=1, m=1, d=1, h=1, mi=None, s=15, f => this will recup up to h (hour), s gets 'lost'
  """
  dto = None
  try:
    # 1st try: every parameter should be an int, it doesn't 'interfere' to the next 'try'
    y = int(y)
    m = int(m)
    d = int(d)
    h = int(h)
    mi = int(mi)
    s = int(s)
    f = int(f)
  except ValueError:
    pass
  try:
    # 2nd try: parses rightward checking non-None's and, if adequate, instantiate a datetime.datetime
    if y and m and d and h:
      if mi:
        if s:
          if f:
            dto = datetime.datetime(year=y, month=m, day=d, hour=h, minute=m, second=s, microsecond=f)
          else:
            dto = datetime.datetime(year=y, month=m, day=d, hour=h, minute=mi, second=s)
        else:
          dto = datetime.datetime(year=y, month=m, day=d, hour=h, minute=mi)
      else:
        dto = datetime.datetime(year=y, month=m, day=d, hour=h)
  except ValueError:
    pass
  # Notice that None may be returned
  return dto


def convert_str_or_attrsobj_to_datetime_or_none(str_or_attrsobj):
  """
  year-mm-dd hh:mm:ss.cccccc
  formatstr = '%Y-%m-%d %H:%M:%S.%f'
  """
  if str_or_attrsobj is None:
    return None
  if isinstance(str_or_attrsobj, datetime.datetime):
    return str_or_attrsobj
  if issubclass(datetime.datetime, type(str_or_attrsobj)):
    return str_or_attrsobj
  try:
    # 1st try: uses strptime() against the whole string
    wholestr = str(str_or_attrsobj)
    pp = wholestr.split(' ')
    if len(pp) >= 2:
      wholestr = ' '.join(pp[:2])
    else:
      if wholestr.find('T') < 0:
        # it should be like year-mm-dd hh:mm:ss.cccccc,
        # but it's also allowed to be like year-mm-ddThh:mm:ss
        # None is returned because either the " " was missing or the "T" was missing
        return None
    dto = make_datetime_w_formatfields_or_none(wholestr)
    if dto:
      return dto
  except ValueError:
    pass
  y, m, d, h, mi, s, f = None, None, None, None, None, None, None
  try:
    # 2nd try: tries to recup datetime by attribute names
    o = str_or_attrsobj
    y = int(o.year)
    m = int(o.month)
    d = int(o.day)
    h = int(o.hour)
    mi = int(o.minute)
    s = int(o.second)
    f = int(o.microsecond)
    dto = datetime.datetime(year=y, month=m, day=d, hour=h, minute=m, second=s, microsecond=f)
    return dto
  except ValueError:
    # the following function recups a datetime if at least it exists up to h (hour)
    dto = make_datetime_w_fields_or_none(y, m, d, h, mi, s, f)
    if dto:
      return dto
  return None


def adhoc_test():
  pass


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
