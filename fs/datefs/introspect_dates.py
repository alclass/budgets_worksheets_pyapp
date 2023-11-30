#!/usr/bin/env python3
"""
fs/datefs/introspect_dates.py
  contains introspecting functions to convert string dates, under up to 9 different formats, into datetime. date's

Formats may be (with separator "-"):
  => ymd meaning year month day eg "2021-1-17"
  => ydm meaning day month day eg "2021-17-1"
  => dmy meaning day month day eg "17-1-2021"
  => mdy meaning day month day eg "1-17-2021"
With separator "/":     With separator ".":
  => ymd "2021/1/17"     => ymd "2021.1.17"
  => ydm "2021/17/1"     => ydm "2021.17.1"
  => dmy "17/1/2021"     => dmy "17.1.2021"
  => mdy "1/17/2021"     => mdy "1.17.2021"
Altogether there are 12 options (4 positionings times 3 separators)
Notice year (y) is never in the middle.
"""
import datetime
import fs.datefs.datefunctions as dtfs
STRDATE_SEPARATORS = ['-', '/', '.']
ORDERPOS_TOKENS_AVAILABLE = ['ymd', 'ydm', 'dmy', 'mdy']


def convert_strdate_to_date_or_none_w_sep_n_order(strdate, sep='-', order='ymd'):
  try:
    ppp = strdate.split(' ')
    pp = ppp[0].split(sep)
    year = None
    month = None
    day = None
    if order == 'ymd':
      year = int(pp[0])
      month = int(pp[1])
      day = int(pp[2])
    elif order == 'dmy':
      year = int(pp[2])
      month = int(pp[1])
      day = int(pp[0])
    elif order == 'mdy':
      year = int(pp[2])
      month = int(pp[0])
      day = int(pp[1])
    return datetime.date(year=year, month=month, day=day)
  except (IndexError, TypeError, ValueError):
    pass
  return None


def convert_strdate_w_or_wo_sep_to_dtdate_or_none(strdate):
  if strdate is None:
    return None
  if isinstance(strdate, datetime.date):
    return strdate
  if isinstance(strdate, datetime.datetime):
    return strdate
  try:
    if hasattr(strdate, 'year') and hasattr(strdate, 'month') and hasattr(strdate, 'day'):
      _ = int(strdate.year)
      _ = int(strdate.month)
      _ = int(strdate.day)
      return strdate  # its type is neither datetime.date nor datetime.datetime, but it has the 3 int attributes
  except (AttributeError, TypeError, ValueError):
    pass
  try:
    strdate = str(strdate)
    strdate = strdate.split(' ')[0]
    sep = ''
    if strdate.find('-') > -1:
      sep = '-'
    elif strdate.find('.') > -1:
      sep = '.'
    elif strdate.find('/') > -1:
      sep = '/'
    if sep == '':
      # if no separator is present, it must be ymd (no other combination allowed in this case)
      # however, if slicing below is errand, an exception will raise, caught and None returned at the end
      year = int(strdate[:4])
      month = int(strdate[4:6])
      day = int(strdate[6:8])
      return datetime.date(year, month, day)
    # at this point, sep is either -, / or .
    pp = strdate.split(sep)
    n0 = int(pp[0])
    n1 = int(pp[1])
    n2 = int(pp[2])
    year, month, day = None, None, None
    if n0 > 31:
      year = n0
      if n2 > 12:
        # hypothesis 1 ymd where d is > 12
        day = n2
        month = n1
      # hypothesis 2 ydm where d is > 12
      if n1 > 12:
        day = n1
        month = n2
    if n2 > 31:
      year = n2
      if n0 > 12:
        # hypothesis 3 dmy where d is > 12
        day = n0
        month = n1
      # hypothesis 4 mdy where d is > 12
      if n1 > 12:
        day = n1
        month = n0
    if year and month and day:
      return datetime.date(year, month, day)
  except (IndexError, ValueError):
    pass
  # falling back here means either a inconsistent positioning
  # or an ambiguity (or inconclusiveness) having both day and month < 13
  return None


def convert_date_to_mmddyyyy_str_or_today(pdate):
  pdate = convert_date_to_mmddyyyy_str_or_none(pdate)
  if pdate is None:
    pdate = datetime.date.today()
  return pdate


def convert_date_to_mmddyyyy_str_or_none(pdate):
  if pdate is None:
    return None
  indate = pdate  # copy.copy() not needed to protect side effect against pdate
  if str == type(indate):
    indate = convert_generic_yyyymmdd_strdate_to_dtdate_or_none(indate)
    if indate is None:
      return None
  mm = str(indate.month).zfill(2)
  dd = str(indate.day).zfill(2)
  yyyy = str(indate.year)
  mmddyyyy = '%s-%s-%s' % (mm, dd, yyyy)
  return mmddyyyy


def introspect_n_convert_strdate_to_date_or_none(strdate, sep=None, positionstr=None):
  """

  """
  if sep is None:
    sep = introspect_sep_char_in_strdate(strdate)
    if sep is None:
      return None
  if positionstr is None:
    positionstr = introspect_year_month_day_field_order_in_date(strdate, sep)
  return convert_strdate_to_date_or_none_w_sep_n_order(strdate, sep, positionstr)


def introspect_n_convert_strdate_to_date_or_today(strdate, sep=None, fieldsorder=None):
  pdate = introspect_n_convert_strdate_to_date_or_none(strdate, sep, fieldsorder)
  if pdate is None:
    return datetime.date.today()
  return pdate


def find_sep_n_posorder_from_a_strdatelist(p_datelist):
  """
  private function: only to be called from below introspect_n_convert_strdatelist_to_dates(p_datelist)
  """
  if p_datelist is None or len(p_datelist) == 0:
    return None, None
  firstdate = p_datelist[0]
  firstdate = str(firstdate)
  sep = introspect_sep_char_in_strdate(firstdate)
  if sep is None:
    # sep was not found, raise ValueError
    error_msg = 'Separator character in dates were not found'
    raise ValueError(error_msg)
  for strdate in p_datelist:
    positionstr = introspect_year_month_day_field_order_in_date(strdate, sep)
    if positionstr:
      return sep, positionstr
  # positionstr was not found, raise ValueError
  error_msg = 'Field order (ymd | dmy | mdy) in dates were not found'
  raise ValueError(error_msg)


def introspect_n_convert_strdatelist_to_dates(p_datelist):
  if p_datelist is None or len(p_datelist) == 0:
    return []
  outdatelist = []
  firstdate = p_datelist[0]
  if isinstance(firstdate, datetime.date):
    # all elements are supposed to be of the same type
    return p_datelist
  if isinstance(firstdate, datetime.datetime):
    # all elements are supposed to be of the same type
    return p_datelist
  sep, positionstr = find_sep_n_posorder_from_a_strdatelist(p_datelist)
  for strdate in p_datelist:
    pdate = introspect_n_convert_strdate_to_date_or_none(strdate, sep, positionstr)
    outdatelist.append(pdate)
  return outdatelist


def introspect_possible_month_position_in_date(strdate, sep, positions):
  """
  This function is not inclusive when both day and month are less than 13
  This function should be used, issued from an 'upstream function',  with a set that has
    at least one day (in the dates) greater than 12.
  private function that should be called from
    introspect_possible_year_position_in_date(strdate, sep='-'
  """
  try:
    year_pos = positions['y']
  except (IndexError, TypeError):
    return None
  month_testable_pos_indices = [0, 1, 2]  # ie ymd (year month day), dmy, mdy (y is never in the middle)
  del month_testable_pos_indices[year_pos]
  first_test_pos = month_testable_pos_indices.pop()
  try:
    pp = strdate.split(sep)
    month = int(pp[first_test_pos])
    if month > 12:
      # this is day! (for month cannot be greater than 12)
      last_pos = month_testable_pos_indices.pop()
      positions.update({'d': first_test_pos, 'm': last_pos})  # year was already set
      return positions
    last_test_pos = month_testable_pos_indices.pop()
    month = int(pp[last_test_pos])
    if month > 12:
      # this is day! (for month cannot be greater than 12)
      positions.update({'d': last_test_pos, 'm': first_test_pos})
      return positions  # year was already set
  except (IndexError, ValueError):
    pass
  # at this point, day and month are both < 13 and that's inconclusive to where they are in datum
  positions.update({'d': None, 'm': None})
  return positions


def introspect_possible_year_position_in_date(strdate, sep):
  """
  It's inconclusive when the variable is in the first 31 years in A.D. (Annum Domini - After Christ)
  """
  positions = None  # {'y': None, 'm': None, 'd': None}
  try:
    pp = strdate.split(sep)
    pos0 = int(pp[0])
    pos2 = int(pp[2])
    year_pos0 = False
    year_pos2 = False
    if pos0 > 31:
      positions = {'y': 0}
      year_pos0 = True
    # year is never in the middle, look up pos2
    if pos2 > 31:
      positions = {'y': 2}
      year_pos2 = True
    if year_pos0 and year_pos2:
      error_msg = 'Inconsistent date having two fields (first & last) greater than 31'
      raise ValueError(error_msg)
    elif year_pos0 or year_pos2:
      return positions
  except (AttributeError, IndexError, ValueError):
    pass
  # falling back to returning None down here means it's inconclusive (or, also possible, year is mistaken in pos1)
  return None


def introspect_sep_char_in_strdate(strdate):
  """
  Only three separate characters are allowed conventionally in-here, they are:
    => "-" dash, "/" (forward slash) and "." (dot)
  """
  caught_inconsistent_separators = False
  if strdate is None:
    return None
  strdate = strdate.strip(' \t\r\n')
  if strdate.find('-') > -1:
    if strdate.find('/') < 0 and strdate.find('.') < 0:
      sep = '-'
      return sep
    else:
      caught_inconsistent_separators = True
  if strdate.find('/') > -1:
    if strdate.find('-') < 0 and strdate.find('.') < 0:
      sep = '/'
      return sep
    else:
      caught_inconsistent_separators = True
  if strdate.find('.') > -1:
    if strdate.find('-') < 0 and strdate.find('/') < 0:
      sep = '/'
      return sep
  else:
    caught_inconsistent_separators = True
  if caught_inconsistent_separators:
    error_msg = f"""When trying to find the date separator character, 
    it caught more than one in it.  Only one is allowed.
    str date before convertion = {strdate}
    possible separator characters = {STRDATE_SEPARATORS}
    """
    raise ValueError(error_msg)
  # strdate either is not a str-date or it's inconsistent to the 9-combination convention
  return None


def introspect_year_month_day_field_order_in_date(strdate, sep):
  positiondict = introspect_possible_year_position_in_date(strdate, sep)
  positiondict = introspect_possible_month_position_in_date(strdate, sep, positiondict)
  positionstr = trans_positiondict_to_strpositions(positiondict)
  return positionstr


def find_with_a_strdatelist_the_year_month_day_positioning(strdatelist):
  first_strdate = strdatelist[0]
  sep = introspect_sep_char_in_strdate(first_strdate)
  for strdate in strdatelist:
    positionstr = introspect_year_month_day_field_order_in_date(strdate)
    if positionstr is not None:
      return positionstr
    # loop on next expecting to find it at some moment at least until last element
  error_msg = f"""  Failed to find the order of year, month, and day in datelist.
  The conventioned combinations are: y-m-d, y-d-m, d-m-y and m-d-y
  The conventioned separators are: -, / and .
  Altogether, there are 12 possible strdate combinations.
  The non-resolved input string date list is:
  {strdatelist} 
  """
  raise ValueError(error_msg)


def trans_positiondict_to_strpositions(positiondict):
  """
  input: positiondict = {'y': idxY,'m': idxM,'d': idxD}
  output expected: 'ymd' | 'dmy' |  'mdy'
  """
  output_expected = ['ymd', 'dmy', 'mdy']
  try:
    poslist = [None, None, None]
    posy = positiondict['y']
    poslist[posy] = 'y'
    posm = positiondict['m']
    poslist[posm] = 'm'
    posd = positiondict['d']
    poslist[posd] = 'd'
    position_str = ''.join(poslist)
    if position_str in output_expected:
      return position_str
  except (IndexError, TypeError):
    pass
  return None


def adhoc_test():
  strdate = '2021-10-21'
  print(strdate, type(strdate), 'introspect_transform_strdate_to_date')
  pdate = introspect_n_convert_strdate_to_date_or_none(strdate, sep=None, positionstr=None)
  print('introspected/transformed', pdate, type(pdate))
  pdate = convert_strdate_w_or_wo_sep_to_dtdate_or_none(strdate)
  print('convert_strdate_w_or_wo_sep_to_dtdate_or_none', pdate, type(pdate))
  strdate = '20211021'
  pdate = convert_strdate_w_or_wo_sep_to_dtdate_or_none(strdate)
  print(strdate, 'convert_strdate_w_or_wo_sep_to_dtdate_or_none', pdate, type(pdate))
  strdate = '2021-1-1'  # this is ambiguos / inconclusive for day and month are both < 13
  pdate = convert_strdate_w_or_wo_sep_to_dtdate_or_none(strdate)
  print(strdate, 'convert_strdate_w_or_wo_sep_to_dtdate_or_none', pdate, type(pdate))


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
