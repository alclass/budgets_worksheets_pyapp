#!/usr/bin/env python3
"""
fs/datefs/introspect_dates.py
  contains introspecting & converting functions to transform string dates,
  under up to 12 different formats, to datetime. date's

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
STRDATE_SEPARATORS = ['-', '/', '.']
DEFAULT_DATE_SEPARATOR = '-'
ORDERPOS_TOKENS_AVAILABLE = ['ymd', 'ydm', 'dmy', 'mdy']


def convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(pdate, sep='/', zfill=None):
  target_posorder = 'mdy'
  # strdate
  return form_strdate_w_date_sep_posorder_opt_zfill(pdate, sep, target_posorder, zfill)


def convert_date_to_strmmddyyyy_or_itsreprtoday_opt_sep_zfill(pdate, sep='/', zfill=0):
  strdate = convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(pdate, sep, zfill)
  if strdate is not None:
    return strdate
  today = datetime.date.today()
  return convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(today, sep, zfill)


def convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(pdate, sep='/', zfill=None):
  target_posorder = 'mdy'
  # strdate
  return form_strdate_w_date_sep_posorder_opt_zfill(pdate, sep, target_posorder, zfill)


def convert_date_to_strmmddyyyy_or_itsreprtoday_opt_sep_zfill(pdate, sep='/', zfill=0):
  strdate = convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(pdate, sep, zfill)
  if strdate is not None:
    return strdate
  today = datetime.date.today()
  return convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(today, sep, zfill)


def convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, sep='-', orderpos='ymd'):
  try:
    ppp = strdate.split(' ')
    pp = ppp[0].split(sep)
    year = None
    month = None
    day = None
    if orderpos == 'ymd':
      year = int(pp[0])
      month = int(pp[1])
      day = int(pp[2])
    elif orderpos == 'ydm':
      year = int(pp[0])
      month = int(pp[2])
      day = int(pp[1])
    elif orderpos == 'dmy':
      year = int(pp[2])
      month = int(pp[1])
      day = int(pp[0])
    elif orderpos == 'mdy':
      year = int(pp[2])
      month = int(pp[0])
      day = int(pp[1])
    return datetime.date(year=year, month=month, day=day)
  except (IndexError, TypeError, ValueError):
    pass
  return None


def convert_strdate_to_date_or_none_wo_sep_n_fieldorder(strdate):
  return introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)


def convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, sep='-', orderpos='ymd'):
  try:
    ppp = strdate.split(' ')
    pp = ppp[0].split(sep)
    year = None
    month = None
    day = None
    if orderpos == 'ymd':
      year = int(pp[0])
      month = int(pp[1])
      day = int(pp[2])
    elif orderpos == 'ydm':
      year = int(pp[0])
      month = int(pp[2])
      day = int(pp[1])
    elif orderpos == 'dmy':
      year = int(pp[2])
      month = int(pp[1])
      day = int(pp[0])
    elif orderpos == 'mdy':
      year = int(pp[2])
      month = int(pp[0])
      day = int(pp[1])
    return datetime.date(year=year, month=month, day=day)
  except (AttributeError, IndexError, TypeError, ValueError):
    pass
  return None


def trans_from_date_to_strdate_w_sep_posorder_n_zfill(pdate, sep='-', posorder='ymd', zfill=0):
  zfill = normalize_zfill_to_0_1_or_2(zfill)
  try:
    y = f"{pdate.year}"
    m = f"{pdate.month}"
    d = f"{pdate.day}"
    if zfill == 2:
      m = str(pdate.month).zfill(zfill)
      d = str(pdate.day).zfill(zfill)
    if sep not in STRDATE_SEPARATORS:
      return None
    if posorder == 'ymd':
     return y + sep + m + sep + d
    elif posorder == 'ydm':
      return y + sep + d + sep + m
    elif posorder == 'dmy':
      return d + sep + m + sep + y
    elif posorder == 'mdy':
      return m + sep + d + sep + y
  except (AttributeError, TypeError, ValueError):
    pass
  # fallback to returning None means that posorder is not one of the four available
  # [ymd, ydm,dmy, mdy] or an except was caught due to pdate not implementing year, month, and day as int
  return None


def trans_strdate_from_one_format_to_another_w_sep_n_posorder(
   strdate: any,
   fromsep='-', sourceposorder='ymd',
   tosep='/', targetposorder='mdy', zfill=0
):
  """
    The incoming strdate is transformed into date and then 'formatted'
      to the output specified.

  :param strdate:
  :param fromsep:
  :param tosep:
  :param sourceposorder:
  :param targetposorder:
  :param zfill:
  :return: str | None
  """
  if strdate is None:
    return None
  if isinstance(strdate, datetime.date):
    # if it's type is datetime.date, fromsep is ignored
    return trans_from_date_to_strdate_w_sep_posorder_n_zfill(strdate, tosep, targetposorder, zfill)
  # before go to str, try attributes
  pdate = convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, fromsep, sourceposorder)
  if pdate is None:
    return None
  return trans_from_date_to_strdate_w_sep_posorder_n_zfill(pdate, tosep, targetposorder, zfill)


def extract_datelist_from_strdatelist_considering_any_sep_n_posorder(p_strdatelist):
  outdatelist = []
  for strdate in p_strdatelist:
    pdate = introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
    if pdate is None:
      continue
    outdatelist.append(pdate)
  return outdatelist


def extract_datelist_from_strdatelist_w_sep_n_posorder(strdatelist, sep, posorder):
  outdatelist = []
  for strdate in strdatelist:
    pdate = convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, sep, posorder)
    if pdate is None:
      continue
    outdatelist.append(pdate)
  return outdatelist


def extract_datelist_from_strdatelist_sep_n_posorder_consistent(strdatelist):
  sep, posorder = find_sep_n_posorder_from_a_strdatelist(strdatelist)
  return extract_datelist_from_strdatelist_w_sep_n_posorder(strdatelist, sep, posorder)


def check_n_raise_if_strdatelist_has_any_nonconformant_sep_n_posorder(p_strdatelist):
  datelist = extract_datelist_from_strdatelist_sep_n_posorder_consistent(p_strdatelist)
  n_datelist, n_strdatelist = len(datelist), len(p_strdatelist)
  if n_datelist != n_strdatelist:
    error_msg = f"""Input data has one or more invalid strdates.
    original date words = {n_strdatelist}
    converted dates = {n_datelist}"""
    raise ValueError(error_msg)


def form_strdate_w_date_sep_posorder_opt_zfill(pdate, sep='/', posorder='dmy', zfill=None):
  try:
    _, _, _ = int(pdate.year), int(pdate.month), int(pdate.day)
  except (AttributeError, TypeError, ValueError):
    return None
  if posorder not in ORDERPOS_TOKENS_AVAILABLE:
    return None
  zfill = normalize_zfill_to_0_1_or_2(zfill)
  mstr = f"{pdate.month}"
  dstr = f"{pdate.day}"
  if zfill > 0:
    mstr = str(pdate.month).zfill(zfill)
    dstr = str(pdate.day).zfill(zfill)
  try:
    if posorder == 'ymd':
      strdate = f"{pdate.year}{sep}{mstr}{sep}{dstr}"
    elif posorder == 'ydm':
      strdate = f"{pdate.year}{sep}{dstr}{sep}{mstr}"
    elif posorder == 'dmy':
      strdate = f"{dstr}{sep}{mstr}{sep}{pdate.year}"
    elif posorder == 'mdy':
      strdate = f"{mstr}{sep}{dstr}{sep}{pdate.year}"
    else:
      # this error should never occur if ORDERPOS_TOKENS_AVAILABLE contains the four combinations above
      error_msg = f"Logical Error in program: posorder {posorder} should be in set {ORDERPOS_TOKENS_AVAILABLE}"
      raise ValueError(error_msg)
    return strdate
  except (AttributeError, TypeError):
    pass
  return None


def introspect_n_convert_to_date_or_none_w_strdate_opt_sep_posorder(strdate, sep=None, posorder=None):
  """
  This function tries to convert a strdate to a date.
  If the strdate does not have one of the allowed separators ['-', '/', '.'], it returns None.
  @see function above that can treat the no-separator case.
  """
  if sep is None:
    sep = introspect_sep_char_in_strdate(strdate)
    if sep is None:
      return None
  if posorder is None:
    posorder = introspect_year_month_day_field_order_in_date(strdate, sep)
  return convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, sep, posorder)


def introspect_n_convert_strdate_to_date_or_today(strdate, sep=None, posorder=None):
  try:
    pdate = introspect_n_convert_to_date_or_none_w_strdate_opt_sep_posorder(strdate, sep, posorder)
    return pdate
  except (TypeError, ValueError):
    pass
  return datetime.date.today()


def introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate):
  if strdate is None:
    return None
  if isinstance(strdate, datetime.date):
    # a datetime.datetime may have come in, reinstantiate to datetime.date
    o = strdate
    return datetime.date(year=o.year, month=o.month, day=o.day)
  try:
    if hasattr(strdate, 'year') and hasattr(strdate, 'month') and hasattr(strdate, 'day'):
      y = int(strdate.year)
      m = int(strdate.month)
      d = int(strdate.day)
      pdate = datetime.date(year=y, month=m, day=d)
      return pdate
  except (AttributeError, TypeError, ValueError):
    pass
  try:
    strdate = str(strdate).strip(' \t\r\n').split(' ')[0]
    sep = ''
    if strdate.find('-') > -1:
      sep = '-'
    elif strdate.find('.') > -1:
      sep = '.'
    elif strdate.find('/') > -1:
      sep = '/'
    if sep == '':
      # either of the 3 separators is not present, so algorithm presupposes format 'ymd'
      # (no other combination than 'ymd' is allowed in this case)
      # however, if slicing below is errand, an exception will be raised/caught and None returned at the end
      # IMPORTANT: the to-index in slicing is not raising IndexError,
      #   so len(strdate) must be used right at the beginning here
      if len(strdate) != 8:
        # though the following msg, the IndexError exception below is caught at the end of this segment,
        # making function returns None and not crashing the run
        error_msg = f'strdate [{strdate}] without a separator is only acceptable with 8 digits'
        raise IndexError(error_msg)
      # strdates without a separator are only acceptable with 8 digits
      year = int(strdate[:4])
      month = int(strdate[4:6])
      day = int(strdate[6:8])
      pdate = datetime.date(year, month, day)
      return pdate
    # at this point, sep is either '-', '/' or '.'
    pp = strdate.split(sep)
    n0 = int(pp[0])
    n1 = int(pp[1])
    n2 = int(pp[2])
    n0 = n0 if n0 > -1 else -1 * n0
    n1 = n1 if n1 > -1 else -1 * n1
    n2 = n2 if n2 > -1 else -1 * n2
    year, month, day = None, None, None
    if n0 > 31:
      year = n0
      if n2 > 12:  # this if is not to date-validate but just to disambiguate month from day
        # hypothesis 1: ymd where d is > 12
        day = n2
        month = n1
      elif n1 == n2:  # at this point (elif), only if month==day a datetime.date is consistent
        day = n1
        month = n1
      # hypothesis 2: ydm where d is > 12
      if n1 > 12:  # this if is not to date-validate but just to disambiguate month from day
        day = n1
        month = n2
      elif n1 == n2:  # at this point (elif), only if month==day a datetime.date is consistent
        day = n1
        month = n1
    if n2 > 31:
      year = n2
      if n0 > 12:  # this if is not to date-validate but just to disambiguate month from day
        # hypothesis 3 dmy where d is > 12 & m < 13 or d=m
        day = n0
        month = n1
      elif n0 == n1:  # at this point (elif), only if month==day a datetime.date is consistent
        day = n0
        month = n0
      # hypothesis 4 mdy where d is > 12
      if n1 > 12:  # this if is not to date-validate but just to disambiguate month from day
        day = n1
        month = n0
      if n0 == n1:  # at this point (elif), only if month==day a datetime.date is consistent
        # because they are the same, it's indifferent day or month
        day = n0
        month = n0
    if year and month and day:
      return datetime.date(year, month, day)
  except (IndexError, ValueError):
    pass
  # falling back here means either an inconsistent positioning happened
  # or an ambiguity (or inconclusiveness) of day to month happened
  return None


def introspect_n_convert_strdate_to_date_or_today_w_or_wo_sep_n_posorder(strdate):
  pdate = introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
  if pdate is None:
    return datetime.date.today()
  return pdate


def introspect_n_convert_sdlist_to_dates_w_or_wo_sep_n_posorder(strdatelist):
  if strdatelist is None or len(strdatelist) == 0:
    return []
  outdatelist = []
  firstdate = strdatelist[0]
  if isinstance(firstdate, datetime.date):
    # all elements are supposed to be of the same type
    return strdatelist
  if isinstance(firstdate, datetime.datetime):
    # all elements are supposed to be of the same type
    return strdatelist
  sep, posorder = find_sep_n_posorder_from_a_strdatelist(strdatelist)
  for strdate in strdatelist:
    if sep and posorder:
      pdate = convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, sep, posorder)
    else:
      pdate = introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
    if pdate:
      outdatelist.append(pdate)
  return outdatelist


def introspect_n_convert_strdatelist_to_dates(strdatelist):
  if strdatelist is None or len(strdatelist) == 0:
    return []
  outdatelist = []
  firstdate = strdatelist[0]
  if isinstance(firstdate, datetime.date):
    # all elements are supposed to be of the same type
    return strdatelist
  if isinstance(firstdate, datetime.datetime):
    # all elements are supposed to be of the same type
    return strdatelist
  sep, positionstr = find_sep_n_posorder_from_a_strdatelist(strdatelist)
  for strdate in strdatelist:
    pdate = introspect_n_convert_to_date_or_none_w_strdate_opt_sep_posorder(strdate, sep, positionstr)
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
  sep_dash, sep_slash, sep_dot = ('-', '/', '.')
  if strdate is None:
    return None
  strdate = strdate.strip(' \t\r\n')
  if strdate.find(sep_dash) > -1:
    if strdate.find(sep_slash) < 0 and strdate.find(sep_dot) < 0:
      return sep_dash  # dash -
    else:
      caught_inconsistent_separators = True
  elif strdate.find(sep_slash) > -1:
    if strdate.find(sep_dash) < 0 and strdate.find(sep_dot) < 0:
      return sep_slash  # slash /
    else:
      caught_inconsistent_separators = True
  elif strdate.find(sep_dot) > -1:
    if strdate.find(sep_dash) < 0 and strdate.find(sep_slash) < 0:
      return sep_dot  # dot .
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


def find_sep_n_posorder_from_a_strdatelist(p_datelist):
  """
  private function: only to be called from below introspect_n_convert_strdatelist_to_dates(p_datelist)
  """
  if p_datelist is None or len(p_datelist) == 0:
    return None, None
  first_str_date = p_datelist[0]
  firstdate = str(first_str_date)
  sep = introspect_sep_char_in_strdate(firstdate)
  n_of_strdates = len(p_datelist)
  if sep is None:
    # sep was not found, raise ValueError
    error_msg = f"""At this point, the date separator character was not found in
    function find_sep_n_orderpos_from_a_strdatelist() [confirm it in stack trace]
    first_str_date = {first_str_date} in {n_of_strdates} strdates"""
    raise ValueError(error_msg)
  last_str_date = None
  for strdate in p_datelist:
    positionstr = introspect_year_month_day_field_order_in_date(strdate, sep)
    if positionstr:
      return sep, positionstr
    last_str_date = strdate
  # positionstr was not found, raise ValueError
  error_msg = f"""Field order in dates were not found. Separator found is "{sep}"
  Field order can be either ymd, dmy or mdy; 
     where: y is year, m is month, d is day
  Example of ymd is: "2023{sep}12{sep}03"
  first_str_date = {first_str_date}
  last_str_date = {last_str_date}"""
  raise ValueError(error_msg)


def find_with_a_strdatelist_the_year_month_day_positioning(strdatelist):
  first_strdate = strdatelist[0]
  sep = introspect_sep_char_in_strdate(first_strdate)
  for strdate in strdatelist:
    positionstr = introspect_year_month_day_field_order_in_date(strdate, sep)
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


def remove_strdates_not_conforming_to_sep_n_posorder(strdatelist, sep, posorder):
  if sep is None or posorder is None:
    return strdatelist
  outstrdatelist = []
  for strdate in strdatelist:
    pdate = convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, sep, posorder)
    if pdate is None:
      continue
    outstrdatelist.append(strdate)
  return outstrdatelist


def normalize_zfill_to_0_1_or_2(zfill=0):
  """
  zfill may be either 0, 1 or 2 for it is applied to str month and day
    0 and 1 have the same effect in strdates ie yyyy-m-d e.g. 2023-5-5
    2 fills in a left-zero if needed ie yyyy-mm-dd e.g. 2023-05-05
  """
  if isinstance(zfill, int):
    # if it's negative, take its reciprocal (or simetrical, ie -1*n)
    zfill = zfill if zfill > -1 else -1 * zfill
    # any integer greater than 2 becomes 2 (its ceiling)
    zfill = zfill if zfill < 3 else 2
  else:  # if some variable not int came in
    try:
      zfill = int(zfill)
      # if zfill was cast into int and an exception was not raised, call itself (recursion) 'returning'
      return normalize_zfill_to_0_1_or_2(zfill)
    except (TypeError, ValueError):
      zfill = 0
  return zfill


def trans_positiondict_to_strpositions(positiondict):
  """
  input: positiondict = {'y': idxY,'m': idxM,'d': idxD}
  output expected: 'ymd' | 'dmy' |  'mdy'
  """
  output_expected = ORDERPOS_TOKENS_AVAILABLE  # ['ymd', 'ymd', 'dmy', 'mdy']
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
  pdate = introspect_n_convert_to_date_or_none_w_strdate_opt_sep_posorder(strdate, sep=None, posorder=None)
  print('introspected/transformed', pdate, type(pdate))
  pdate = introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
  print('convert_strdate_w_or_wo_sep_to_date_or_none', pdate, type(pdate))
  strdate = '20211021'
  pdate = introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
  print(strdate, 'convert_strdate_w_or_wo_sep_to_date_or_none', pdate, type(pdate))
  strdate = '2021-1-1'  # this is ambiguos / inconclusive for day and month are both < 13
  pdate = introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
  print(strdate, 'convert_strdate_w_or_wo_sep_to_date_or_none', pdate, type(pdate))


def adhoc_test2():
  sd1, sd2, sd3 = ('2023.14.05', '2023/03-04', 'bla foo bar')
  strdatelist = [sd1, sd2, sd3]
  print(strdatelist)
  # expected_sep = '.'
  # expected_posorder = 'ydm'
  sep, posorder = find_sep_n_posorder_from_a_strdatelist(strdatelist)
  scrmsg = f'sep => {sep} :: posorder => {posorder}'
  print(scrmsg)
  filtered_list = remove_strdates_not_conforming_to_sep_n_posorder(strdatelist, sep, posorder)
  print('filtered_strlist (conformant with sep and posorder)', filtered_list)
  datelist = extract_datelist_from_strdatelist_sep_n_posorder_consistent(strdatelist)
  print('extract_datelist_from_strdatelist_sep_n_posorder_consistent =>', datelist)
  today = datetime.date.today()
  sep, posorder = '/', 'dmy'
  strdate = form_strdate_w_date_sep_posorder_opt_zfill(today, sep, posorder)
  print(today, 'sep', sep, 'posorder', posorder, 'no-zfill, form_strdate...', strdate)
  sep, posorder, zfill = '.', 'mdy', 2
  strdate = form_strdate_w_date_sep_posorder_opt_zfill(today, sep, posorder, zfill)
  print(today, 'sep', sep, 'posorder', posorder, 'zfill', zfill, 'form_strdate...', strdate)


def adhoc_test4():
  strdate = '2023-04-28'
  pdate = introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
  scrmsg = f"{strdate} type {type(strdate)}=> {pdate} type {type(pdate)}"
  print(scrmsg)


def adhoc_test3():
  strdate = '2013/12/1'
  pdate = introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
  scrmsg = f"strdate={strdate}, date={pdate}"
  print(scrmsg)
  strdate = '2013.12.13'
  pdate = introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
  scrmsg = f"strdate={strdate}, date={pdate}"
  print(scrmsg)
  strdate = '20211121'
  pdate = introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
  scrmsg = f"strdate={strdate}, date={pdate}"
  print(scrmsg)
  strdate = '2021121'
  pdate = introspect_n_convert_strdate_to_date_or_none_w_or_wo_sep_n_posorder(strdate)
  scrmsg = f"strdate={strdate}, date={pdate}"
  print(scrmsg)
  today = datetime.date.today()
  sep, zfill = '/', -77
  strdate = convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(today, sep=sep, zfill=zfill)
  scrmsg = f"sep={sep}, zfill={zfill}, mmddyyyy date={today}, strdate={strdate} "
  print(scrmsg)
  zfill = -1
  strdate = convert_date_to_strmmddyyyy_or_none_opt_sep_zfill(today, sep=sep, zfill=zfill)
  scrmsg = f"sep={sep}, zfill={zfill}, mmddyyyy date={today}, strdate={strdate} "
  print(scrmsg)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test4()
