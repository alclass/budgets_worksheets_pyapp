#!/usr/bin/env python3
"""
  docstring
"""
import calendar
from dateutil.relativedelta import relativedelta
import collections as coll
import datetime
import os
import fs.textfs.strfs as strfs
import settings
WEEKEND_PREVIOUS_DATE_MAX_RECURSE = 41  # go back up to 31 days (a month) plus 10
WEEKDAYS3LETTER = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def is_date_valid(pdate):
  if isinstance(pdate, datetime.date):
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
  indate = convert_yyyymmdd_strdate_to_dtdate_or_none(pdate)
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
  indate = convert_yyyymmdd_strdate_to_dtdate_or_none(pdate)
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
  return convert_yyyymmdd_strdate_to_dtdate_or_none(pdate)


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
  pdate = convert_strdate_to_date_or_none()
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
  pdate = convert_yyyymmdd_strdate_to_dtdate_or_none(strdate)
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


def convert_yyyymmdd_strdate_to_dtdate_or_none(strdate):
  if strdate is None:
    return None
  if str != type(strdate):
    try:
      _, _, _ = strdate.year, strdate.month, strdate.day
      return strdate  # though it's not a str, it has the three attributes year, month and day
    except AttributeError:
      return None
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
    indate = convert_yyyymmdd_strdate_to_dtdate_or_none(indate)
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


def adhoc_test2():
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


def adhoc_test():
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
  pdate = get_monthslastday_date_via_calendar('2020-7-3')
  print("get_monthslastday_date_via_calendar('2020-7-3')", pdate)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test2()
