#!/usr/bin/env python3
"""
fs/datefs/datefunctions.py
  contains date-related functions
"""
import calendar
import collections as coll
import datetime
from dateutil.relativedelta import relativedelta
import os
import fs.textfs.strfs as strfs
import settings
WEEKEND_PREVIOUS_DATE_MAX_RECURSE = 41  # go back up to 31 days (a month) plus 10
WEEKDAYS3LETTER = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
ALL_MONTHS_ENG_CAP_FIRST_LIST = list(map(lambda e: calendar.month_name[e], range(1, 13)))


def make_allmonths_englishlower3letter_list():
  return list(map(lambda e: e[:3].lower(), ALL_MONTHS_ENG_CAP_FIRST_LIST))


def is_date_valid(pdate):
  if isinstance(pdate, datetime.date):
    return True
  # next try includes more possibilities than datetime.date,
  # including all str repr's like yyyy-mm-dd (which in turn includes, e.g., datetime.datetime)
  pdate = make_date_or_none(pdate)
  if pdate is not None:
    return True
  return False


def adjust_date_if_str(pdate):
  if isinstance(pdate, datetime.date):
    return pdate
  return convert_strdate_to_date_or_none(pdate)


def transform_strdatelist_to_datelist(strdatelist):
  outlist = []
  for strdate in strdatelist:
    pdate = adjust_date_if_str(strdate)
    if pdate is not None:
      outlist.append(pdate)
  return outlist


def transform_strdates_sep_by_blank_to_datelist(strdatelist):
  datelist = strdatelist.split(' ')
  outlist = []
  for strdate in datelist:
    pdate = adjust_date_if_str(strdate)
    if pdate is not None:
      outlist.append(pdate)
  return outlist


def make_refmonthdate_or_none(refmonthdate=None):
  if refmonthdate is None:
    return None
  if isinstance(refmonthdate, datetime.date):
    if refmonthdate.day == 1:
      return refmonthdate
    return datetime.date(year=refmonthdate.year, month=refmonthdate.month, day=1)
  try:
    refmonthdate = str(refmonthdate).strip(' \t\r\n')
    ppp = refmonthdate.split(' ')
    pp = ppp[0].split('-')
    year = int(pp[0])
    month = int(pp[1])
    return datetime.date(year=year, month=month, day=1)
  except (AttributeError, TypeError, ValueError):
    pass
  return None


def make_refmonthdate_or_current(refmonthdate=None):
  refmonthdate = make_refmonthdate_or_none(refmonthdate)
  if isinstance(refmonthdate, datetime.date):
    return refmonthdate
  today = datetime.date.today()
  current_refmonthdate = datetime.date(year=today.year, month=today.month, day=1)
  return current_refmonthdate


def adjust_datelist_if_str(datelist):
  if datelist is None:
    return None
  try:
    tmpdatelist = list(datelist)
    if len(tmpdatelist[0]) == 1:
      # if datelist was a string, the list function will generate of list of "chars"
      raise TypeError
    return transform_strdatelist_to_datelist(tmpdatelist)
  except TypeError:
    pass
  # at this point, datelist is not subscriptable, ie list(datelist) raised TypeError
  # however, if it's a string, dateadhoctests in there should be separated by blank (sort of convention, not by another char)
  return transform_strdates_sep_by_blank_to_datelist(datelist)


def get_appsroot_abspath_for_filename_w_tstamp(filename):
  strdt = make_tstamp_for_filename()
  name, ext = os.path.splitext(filename)
  if name.find(' ') > -1:
    filename = name + ' ' + strdt + ext
    filename.replace('  ', ' ')
  else:
    filename = name + '_' + strdt + ext
  return settings.get_appsroot_abspath_for_filename(filename)


def get_decade_year_tenmultiplebased_from_or_current(pdate=None):
  """
  Examples:
    input: 2023-mm-dd, output: 2020
    input: None, output: 2020 (notice that at the time of this writing, year = 2023)
    input: 2010-mm-dd, output: 2010
  """
  if pdate is None:
    pdate = datetime.date.today()
  if not isinstance(pdate, datetime.date):
    pdate = make_date_or_today(pdate)
  year = pdate.year
  decade_year = year // 10 * 10
  return decade_year


def get_decade_year_tenmultiplebased_from_or_none(pdate=None):
  """
  Examples:
    input: 2023-mm-dd, output: 2020
    input: None, output: None (see also variation of this method which has a default)
    input: 2010-mm-dd, output: 2010
  """
  if pdate is None:
    return None
  pdate = make_date_or_today(pdate)
  if not isinstance(pdate, datetime.date):
    return None
  return get_decade_year_tenmultiplebased_from_or_current(pdate)


def get_first_date_in_decade_year_tenmultiplebased_from_or_current(pdate=None):
  """
  Examples:
    input: 2023-mm-dd, output: 2020-01-01
    input: None, output: 2020-01-01 (notice that at the time of this writing, year = 2023)
    input: 2010-mm-dd, output: 2010-01-01
  """
  year = get_decade_year_tenmultiplebased_from_or_current(pdate)
  # the above function either returns an int (datetime.date.year) or raises an exception there
  # ie year is "never" None here
  return datetime.date(year=year, month=1, day=1)


def get_first_date_in_decade_year_tenmultiplebased_from_or_none(pdate=None):
  """
  Examples:
    input: 2023-mm-dd, output: 2020-01-01
    input: None, output: None (see also variation of this method which has a default)
    input: 2010-mm-dd, output: 2010-01-01
  """
  year = get_decade_year_tenmultiplebased_from_or_none(pdate)
  if year is None:
    return None
  return datetime.date(year=year, month=1, day=1)


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
  if pdate is None:
    return None
  return datetime.datetime(pdate.year, pdate.month, pdate.day)


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


def convert_strdate_to_date_or_none(strdate):
  if strdate is None:
    return None
  if isinstance(strdate, datetime.date):
    return strdate
  try:
    strdate = str(strdate)
    ppp = strdate.split(' ')
    pp = ppp[0].split('-')
    year = int(pp[0])
    month = int(pp[1])
    day = int(pp[2])
    return datetime.date(year=year, month=month, day=day)
  except (IndexError, ValueError):
    pass
  return None


def convert_strdatetime_to_datetime_or_none(strdatetime):
  if strdatetime is None:
    return None
  if isinstance(strdatetime, datetime.datetime):
    return strdatetime
  strdatetime = str(strdatetime)
  pp = strdatetime.split(' ')
  strdate = pp[0]
  pdate = returns_date_or_none(strdate)
  if pdate is None:
    return None
  try:
    strtime = pp[1]
  except IndexError:
    return convert_date_to_datetime_or_none(pdate)
  ppp = strtime.split(':')
  strhh = ppp[0]
  hh = 0
  strmi = ppp[1]
  mi = 0
  pppp = ppp[-1].split('.')
  strss = pppp[0]
  ss = 0
  strmmm = '0'
  mmm = 0
  try:
    strmmm = pppp[1]
  except IndexError:
    pass
  try:
    hh = int(strhh)
    mi = int(strmi)
    ss = int(strss)
    mmm = 1000 * int(strmmm)
  except ValueError:
    pass
  pdatetime = datetime.datetime(
    year=pdate.year,
    month=pdate.month,
    day=pdate.day,
    hour=hh,
    minute=mi,
    second=ss,
    microsecond=mmm,
  )
  return pdatetime


def get_datafolder_abspath_for_filename_w_tstamp(filename):
  strdt = make_tstamp_for_filename()
  name, ext = os.path.splitext(filename)
  if name.find(' ') > -1:
    filename = name + ' ' + strdt + ext
    filename.replace('  ', ' ')
  else:
    filename = name + '_' + strdt + ext
  datafolder_abspath = settings.get_datafolder_abspath()
  filepath = os.path.join(datafolder_abspath, filename)
  return filepath


def is_date_weekend(pdate):
  indate = convert_generic_yyyymmdd_strdate_to_dtdate_or_none(pdate)
  if indate is None:
    return None
  try:
    weekdaynumber = indate.weekday()
    if weekdaynumber in [5, 6]:
      return True
    return False
  except AttributeError:
    pass
  return None


def get_weekday3letter_from_date(pdate):
  """
  # previously:
  # weekday = calendar.weekday(year=indate.year, month=indate.month, day=indate.day)  # _ is days in month
  # currently:
  # weekday can be obtained directly from date (instead of calling calendar.weekday(date)
  """
  indate = returns_date_or_none(pdate)
  if indate is None:
    return None
  weekday = indate.weekday()
  return WEEKDAYS3LETTER[weekday]


def get_date_or_previous_monday_to_friday(pdate, max_recurse=0):
  indate = convert_generic_yyyymmdd_strdate_to_dtdate_or_none(pdate)
  if indate is None:
    return None
  if max_recurse > WEEKEND_PREVIOUS_DATE_MAX_RECURSE:
    return None
  if is_date_weekend(indate):
    previous_date = indate - datetime.timedelta(days=1)
    return get_date_or_previous_monday_to_friday(previous_date, max_recurse + 1)
  return indate


def get_monthslastday_date_via_calendar(pdate):
  indate = returns_date_or_none(pdate)
  if indate is None:
    return None
  _, n_days_in_month = calendar.monthrange(year=indate.year, month=indate.month)  # _ is the first weekday in month
  return datetime.date(year=indate.year, month=indate.month, day=n_days_in_month)


def get_monthslastday_date_via_addition(pdate):
  indate = returns_date_or_none(pdate)
  if indate is None:
    return None
  if indate.day > 1:
    date_set_on_first_day_of_month = datetime.date(indate.year, indate.month, 1)
  else:
    date_set_on_first_day_of_month = indate
  date_on_first_day_of_next_month = date_set_on_first_day_of_month + relativedelta(months=1)
  monthslastday_date = date_on_first_day_of_next_month - relativedelta(days=1)
  return monthslastday_date


def returns_date_or_none(pdate=None):
  return convert_generic_yyyymmdd_strdate_to_dtdate_or_none(pdate)


def returns_date_or_today(pdate=None):
  indate = returns_date_or_none(pdate)
  if indate is None:
    indate = datetime.date.today()
  return indate


def prepare_datelist_uniq_n_in_desc_order(datelist):
  datelist = map(lambda x: returns_date_or_none(x), datelist)
  datelist = list(filter(lambda x: x is not None, datelist))
  # remove repeats
  od = coll.OrderedDict({})
  for d in datelist:
    od.update({d: 1})
  datelist = list(od.keys())
  return sort_datelist_desc(datelist)


def make_date_or_none(pdate):
  return convert_strdate_to_date_or_none(pdate)


def make_date_or_today(pdate=None):
  pdate = convert_strdate_to_date_or_none(pdate)
  if pdate is None:
    return datetime.date.today()
  return pdate


def sort_datelist_desc(daterange):
  if len(daterange) < 2:
    return daterange
  previous_date = daterange[0]
  reorder = False
  for pdate in daterange[1:]:
    if previous_date < pdate:
      reorder = True
      break
    previous_date = pdate
  if not reorder:
    return daterange
  return list(reversed(sorted(daterange)))


def sort_datelist_asc(daterange):
  if len(daterange) < 2:
    return daterange
  previous_date = daterange[0]
  reorder = False
  for pdate in daterange[1:]:
    if previous_date > pdate:
      reorder = True
      break
    previous_date = pdate
  if not reorder:
    return daterange
  return list(sorted(daterange))


def get_daterange_asc_or_desc(pinidate, pfindate, makes_desc=False, accept_future=False):
  inidate = returns_date_or_today(pinidate)
  findate = returns_date_or_today(pfindate)
  if inidate < findate and makes_desc:
    return get_daterange(findate, inidate, accept_future)
  if inidate > findate and not makes_desc:
    return get_daterange(findate, inidate, accept_future)
  return get_daterange(inidate, findate, accept_future)


def generate_daterange(pinidate, pfindate, accept_future=False):
  inidate = returns_date_or_today(pinidate)
  findate = returns_date_or_today(pfindate)
  today = datetime.date.today()
  if not accept_future:
    if inidate > today >= findate:
      inidate = today
    elif findate > today >= inidate:
      findate = today
    elif inidate > today and findate > today:
      return None
  if inidate == findate:
    yield inidate
    return
  elif inidate < findate:
    ongoingdate = inidate
    while ongoingdate <= findate:  # fimdate will also be included in daterange
      yield ongoingdate
      ongoingdate = ongoingdate + datetime.timedelta(days=1)
  elif inidate > findate:
    ongoingdate = inidate
    while ongoingdate >= findate:  # fimdate will also be included in daterange
      yield ongoingdate
      ongoingdate = ongoingdate - datetime.timedelta(days=1)
  return


def get_daterange(pinidate, pfindate, accept_future=False):
  inidate = returns_date_or_today(pinidate)
  findate = returns_date_or_today(pfindate)
  today = datetime.date.today()
  if inidate > today and not accept_future:
    inidate = today
  if findate > today and not accept_future:
    findate = today
  daterange = [inidate]
  if inidate == findate:
    pass
  elif inidate < findate:
    ongoingdate = inidate
    while ongoingdate < findate:  # fimdate will also be included in daterange
      ongoingdate = ongoingdate + datetime.timedelta(days=1)
      daterange.append(ongoingdate)
  elif inidate > findate:
    ongoingdate = inidate
    while ongoingdate > findate:  # fimdate will also be included in daterange
      ongoingdate = ongoingdate - datetime.timedelta(days=1)
      daterange.append(ongoingdate)
  return daterange


strdate_separators = ['-', '/', '.']


def convert_sep_or_datefields_position_for_ymdstrdate(pstrdate, tosep='-', sourceposorder='ymd', targetposorder='ymd'):
  """
    The input pstrdate must be in the ymd order.

  :param pstrdate:
  :param tosep:
  :param sourceposorder:
  :param targetposorder:
  :return:
  """
  if pstrdate is None:
    return None
  # force it to be a str, only useful when, for example, a datetime.date is sent in, but not harmful otherwise
  strdate = str(pstrdate)
  sep_in_date = ''
  for sep in strdate_separators:
    if sep in strdate:
      sep_in_date = sep
      break
  strdate = strdate.replace(sep_in_date, tosep)
  strdate, pdate = return_strdate_in_fields_order_if_good_or_none(strdate, tosep, sourceposorder)
  if strdate is None:
    return None
  if sourceposorder == targetposorder:
    return strdate
  return transform_date_to_other_order_fields_n_sep(pdate, tosep, targetposorder)


def return_strdate_in_fields_order_if_good_or_none(strdate, sep, posorder):
  pp = strdate.split(sep)
  y = None
  m = None
  d = None
  try:
    if posorder == 'ymd':
      y = int(pp[0])
      m = int(pp[1])
      d = int(pp[2])
    elif posorder == 'ydm':
      y = int(pp[0])
      m = int(pp[2])
      d = int(pp[1])
    elif posorder == 'myd':
      y = int(pp[1])
      m = int(pp[0])
      d = int(pp[2])
    elif posorder == 'mdy':
      y = int(pp[2])
      m = int(pp[0])
      d = int(pp[1])
    elif posorder == 'dmy':
      y = int(pp[2])
      m = int(pp[1])
      d = int(pp[0])
    elif posorder == 'dym':
      y = int(pp[1])
      m = int(pp[2])
      d = int(pp[0])
  except ValueError:
    return None, None
  except IndexError:
    return None, None
  _ = y
  _ = m
  _ = d
  year = None
  month = None
  day = None
  try:
    for c in posorder:
      if c == 'y':
        year = eval(c)
      elif c == 'm':
        month = eval(c)
      elif c == 'd':
        day = eval(c)
      else:
        return None
  except TypeError:
    return None, None
  try:
    pdate = datetime.date(int(year), int(month), int(day))
    return strdate, pdate
  except ValueError:
    pass
  return None, None


def transform_date_to_other_order_fields_n_sep_or_none(pdate, tosep='/', targetposorder='dmy'):
  if pdate is None:
    return None
  if isinstance(pdate, datetime.date):
    return transform_date_to_other_order_fields_n_sep(pdate, tosep, targetposorder)
  pdate = convert_strdate_to_date_or_none(pdate)
  if isinstance(pdate, datetime.date):
    return transform_date_to_other_order_fields_n_sep(pdate, tosep, targetposorder)
  return None


def transform_date_to_other_order_fields_n_sep(pdate, tosep, targetposorder):
  """
    Consider this function private, ie,
    strdate should already have been tested a good strdate,
    which is good in caller convert_sep_or_datefields_position_for_ymdstrdate()

  :param pdate:
  :param tosep:
  :param targetposorder:
  :return:
  """
  '''
  :param strdate:
  :param sep:
  :param posorder:
  :return:
  '''
  y = pdate.year
  m = str(pdate.month).zfill(2)
  d = str(pdate.day).zfill(2)
  odict = {'y': y, 'm': m, 'd': d, 'sep': tosep}
  if targetposorder == 'ymd':
    odate = '%(y)s%(sep)s%(m)s%(sep)s%(d)s' % odict
    return odate
  elif targetposorder == 'ydm':
    odate = '%(y)s%(sep)s%(d)s%(sep)s%(m)s' % odict
    return odate
  elif targetposorder == 'myd':
    odate = '%(m)s%(sep)s%(y)s%(sep)s%(d)s' % odict
    return odate
  elif targetposorder == 'mdy':
    odate = '%(m)s%(sep)s%(d)s%(sep)s%(y)s' % odict
    return odate
  elif targetposorder == 'dmy':
    odate = '%(d)s%(sep)s%(m)s%(sep)s%(y)s' % odict
    return odate
  elif targetposorder == 'dym':
    odate = '%(d)s%(sep)s%(y)s%(sep)s%(m)s' % odict
    return odate
  return None


def convert_yyyymmdd_strdate_to_dtdate_or_today(strdate):
  pdate = convert_generic_yyyymmdd_strdate_to_dtdate_or_none(strdate)
  if pdate is None:
    pdate = datetime.date.today()
  return pdate


def make_tstamp_for_filename(dtime=None):
  if dtime is None or isinstance(dtime, datetime.datetime):
    dtime = datetime.datetime.now()
  strdt = str(dtime)
  strdt = strdt.split('.')[0]
  strdt = strdt.replace(':', '')
  strdt = strdt.replace('-', '')
  strdt = strdt.replace(' ', 'T')
  return strdt


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
  except (IndexError, TypeError,ValueError):
    pass
  return None

def convert_generic_yyyymmdd_strdate_to_dtdate_or_none(strdate):
  if strdate is None:
    return None
  if isinstance(strdate, datetime.date):
    return strdate
  if isinstance(strdate, datetime.datetime):
    return strdate
  try:
    _, _, _ = strdate.year, strdate.month, strdate.day
    return strdate  # though it's not a str, it has the three attributes year, month and day
  except (AttributeError, TypeError):
    pass
  strdate = str(strdate)
  if len(strdate) < 8:
    return None
  sep = ''
  if strdate.find('-') > -1:
    sep = '-'
  elif strdate.find('.') > -1:
    sep = '.'
  elif strdate.find('/') > -1:
    sep = '/'
  if sep == '':
    stryyyy = strdate[:4]
    strmm = strdate[4:6]
    strdd = strdate[6:8]
  else:
    pp = strdate.split(sep)
    stryyyy = pp[0]
    strmm = pp[1]
    strdd = strfs.pick_first_word(pp[2])
  try:
    yyyy = int(stryyyy)
    mm = int(strmm)
    dd = int(strdd)
    return datetime.date(yyyy, mm, dd)
  except ValueError:
    pass
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


def add_or_subtract_to_month(pdate, delta):
  """
  DEPRECATED: use instead relativedelta from dateutils.relativedelta

  Ref https://stackoverflow.com/questions/3424899/whats-the-simplest-way-to-subtract-a-month-from-a-date-in-python

  d = min(date.day, calendar.monthrange(y, m)[1])
      or
  d = min(date.day, [31,
                     29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])

  :param pdate:
  :param delta:
  :return:
  """
  m, y = (pdate.month + delta) % 12, pdate.year + (pdate.month + delta - 1) // 12
  if not m:
    m = 12
  d = min(pdate.day, calendar.monthrange(y, m)[1])
  return pdate.replace(day=d, month=m, year=y)


def introspect_possible_month_position_in_date(strdate, sep, positions):
  """
  This function is not inclusive when both day and month are less than 13
  This function should be used, issued from an 'upstream function',  with a set that has
    at least one day (in the dates) greater than 12.
  private function that should be called from
    introspect_possible_year_position_in_date(strdate, sep='-')
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
      # this is day!
      last_pos =  month_testable_pos_indices.pop()
      positions.update({'d': first_test_pos, 'm': last_pos})  # year was already set
      return positions
    last_test_pos = month_testable_pos_indices.pop()
    month = int(pp[last_test_pos])
    if month > 12:
      # this is day!
      positions.update({'d': last_test_pos, 'm': first_test_pos})
      return positions  # year was already set
  except (IndexError, ValueError):
    pass
  # at this point, day and month are both < 13 and that's inconclusive to where they are in datum
  positions.update({'d': None, 'm': None})
  return positions


def introspect_possible_year_position_in_date(strdate, sep):
  """
  It's inconclusive when years are in the first 31 in A.D. (Annum Domini - After Christ)
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
  return None


def introspect_sep_char_in_strdate(strdate):
  """
  Only three separate characters are allowed conventionally in-here, they are:
    => "-" dash, "/" (forward slash) and "." (dot)
  """
  if strdate is None:
    return None
  strdate = strdate.strip(' \t\r\n')
  if strdate.find('-') > -1:
    if strdate.find('/') < 0 and strdate.find('.') < 0:
      sep = '-'
      return sep
  if strdate.find('/') > -1:
    if strdate.find('-') < 0 and strdate.find('.') < 0:
      sep = '/'
      return sep
  if strdate.find('.') > -1:
    if strdate.find('-') < 0 and strdate.find('/') < 0:
      sep = '/'
      return sep
  # strdate either is not a str-date or it's inconsistent
  return None


def convert_positiondict_to_strpositions(positiondict):
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


def introspect_n_convert_strdate_to_date_or_today(strdate, sep=None, fieldsorder=None):
  pdate = introspect_n_convert_strdate_to_date_or_none(strdate, sep, fieldsorder)
  if pdate is None:
    return datetime.date.today()
  return pdate

def introspect_year_month_day_field_order_in_date(strdate, sep):
  positiondict = introspect_possible_year_position_in_date(strdate, sep)
  positiondict = introspect_possible_month_position_in_date(strdate, sep, positiondict)
  positionstr = convert_positiondict_to_strpositions(positiondict)
  return positionstr


def introspect_n_convert_strdate_to_date_or_none(strdate, sep=None, fieldsorder=None):
  """

  """
  if sep is None:
    sep = introspect_sep_char_in_strdate(strdate)
    if sep is None:
      return None
  positionstr = introspect_year_month_day_field_order_in_date(strdate, sep)
  return convert_strdate_to_date_or_none_w_sep_n_order(strdate, sep, positionstr)


def introspect_n_convert_strdatelist_to_dates(p_datelist):
  outdatelist = []
  firstdate = p_datelist[0]
  if isinstance(firstdate, datetime.date):
    # all elements are supposed to be of the same type
    return p_datelist
  if isinstance(firstdate, datetime.datetime):
    # all elements are supposed to be of the same type
    return p_datelist
  firstdate = str(firstdate)
  sep = introspect_sep_char_in_strdate(firstdate)
  if sep is None:
    error_msg = 'Separator character in dates were not found'
    raise ValueError(error_msg)
  positionstr = None
  for strdate in p_datelist:
    positionstr = introspect_year_month_day_field_order_in_date(strdate, sep)
    if positionstr:
      break
  if positionstr is None:
    error_msg = 'Field order (ymd | dmy | mdy) in dates were not found'
    raise ValueError(error_msg)
  for strdate in p_datelist:
    pdate = introspect_n_convert_strdate_to_date_or_none(strdate, sep, positionstr)
    outdatelist.append(pdate)
  return outdatelist


def adhoc_test3():
  today = datetime.date.today()
  weekday = today.weekday()
  print(today, 'weekday =>', weekday, get_weekday3letter_from_date(today))
  strdate = transform_date_to_other_order_fields_n_sep_or_none(today)
  print(strdate)
  # adjust_datelist_if_str(datelist)
  datelist = "2023-01-11 2022-10-1"
  print('input datelist', datelist)
  datelist = adjust_datelist_if_str(datelist)
  print('output datelist', datelist)


def adhoc_test2():
  inidate = '2020-1-1'
  findate = '2020-1-5'
  print('Generate', findate, inidate)
  for pdate in generate_daterange(findate, inidate):
    print(pdate)
  print('-' * 30)
  print('Get', inidate, findate)
  for pdate in get_daterange(inidate, findate):
    print(pdate)
  print('-' * 30)
  inidate = '2021-1-1'
  findate = '2021-1-5'
  print('Generate', findate, inidate)
  for pdate in generate_daterange(findate, inidate):
    print(pdate)
  print('Finished')


def extract_year_from_date_or_none(pdate):
  pdate = make_date_or_none(pdate)
  if pdate is None:
    return None
  return pdate.year


def adhoc_test():

  pdate = get_monthslastday_date_via_calendar('2020-7-3')
  print("get_monthslastday_date_via_calendar('2020-7-3')", pdate)
  print(make_allmonths_englishlower3letter_list())
  strdate = '2021-10-21'
  print(strdate, 'introspect_transform_strdate_to_date')
  pdate = introspect_n_convert_strdate_to_date_or_none(strdate, sep=None, fieldsorder=None)
  print('introspected/transformed', pdate)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
