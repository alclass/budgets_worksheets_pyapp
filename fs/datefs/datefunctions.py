#!/usr/bin/env python3
import collections as coll
import datetime
import os
import fs.textfs.strfs as strfs
import config

def get_appsroot_abspath_for_filename_w_tstamp(filename):
  strdt = make_tstamp_for_filename()
  name, ext = os.path.splitext(filename)
  if name.find(' ') > -1:
    filename = name + ' ' + strdt + ext
    filename.replace('  ', ' ')
  else:
    filename = name + '_' + strdt + ext
  return config.get_appsroot_abspath_for_filename(filename)

def get_datafolder_abspath_for_filename_w_tstamp(filename):
  strdt = make_tstamp_for_filename()
  name, ext = os.path.splitext(filename)
  if name.find(' ') > -1:
    filename = name + ' ' + strdt + ext
    filename.replace('  ', ' ')
  else:
    filename = name + '_' + strdt + ext
  datafolder_abspath = config.get_datafolder_abspath()
  filepath = os.path.join(datafolder_abspath, filename)
  return filepath


def is_date_weekend(pdate):
  indate = convert_yyyymmdd_strdate_to_dtdate_or_None(pdate)
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

WEEKEND_PREVIOUS_DATE_MAX_RECURSE = 41 # go back up to 31 days (a month) plus 10
def get_date_or_previous_monday_to_friday(pdate, max_recurse=0):
  indate = convert_yyyymmdd_strdate_to_dtdate_or_None(pdate)
  if indate is None:
    return None
  if max_recurse > WEEKEND_PREVIOUS_DATE_MAX_RECURSE:
    return None
  if is_date_weekend(indate):
    previous_date = indate - datetime.timedelta(days=1)
    return get_date_or_previous_monday_to_friday(previous_date, max_recurse+1)
  return indate

def returns_date_or_None(pdate=None):
  return convert_yyyymmdd_strdate_to_dtdate_or_None(pdate)

def returns_date_or_today(pdate=None):
  indate = returns_date_or_None(pdate)
  if indate is None:
    indate = datetime.date.today()
  return indate

def prepare_datelist_uniq_n_in_desc_order(datelist):
  datelist = map(lambda x : returns_date_or_None(x), datelist)
  datelist = list(filter(lambda x: x is not None, datelist))
  # remove repeats
  od = coll.OrderedDict({})
  for d in datelist:
    od.update({d:1})
  datelist = list(od.keys())
  return sort_datelist_desc(datelist)

def sort_datelist_desc(daterange):
  if len(daterange) < 2:
    return daterange
  previous_date = daterange[0]; reorder= False
  for pdate in daterange[1:]:
    if previous_date < pdate:
      reorder= True
      break
    previous_date = pdate
  if not reorder:
    return daterange
  return list(reversed(sorted(daterange)))

def sort_datelist_asc(daterange):
  if len(daterange) < 2:
    return daterange
  previous_date = daterange[0]; reorder= False
  for pdate in daterange[1:]:
    if previous_date > pdate:
      reorder= True
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
    while ongoingdate < findate: # fimdate will also be included in daterange
      ongoingdate =  ongoingdate + datetime.timedelta(days=1)
      daterange.append(ongoingdate)
  elif inidate > findate:
    ongoingdate = inidate
    while ongoingdate > findate: # fimdate will also be included in daterange
      ongoingdate =  ongoingdate - datetime.timedelta(days=1)
      daterange.append(ongoingdate)
  return daterange

strdate_separators = ['-', '/', '.']
def convert_sep_or_datefields_position_for_ymdstrdate(pstrdate, tosep='-', sourceposorder='ymd', targetposorder='ymd'):
  '''
    The input pstrdate must be in the ymd order.
  :param pstrdate:
  :param tosep:
  :param posorder:
  :return:
  '''
  if pstrdate is None:
    return None
  strdate = str(pstrdate) # force it to be a str, only useful when, for example, a datetime.date is sent in, but not harmful otherwise
  sep_in_date = ''
  for sep in strdate_separators:
    if sep in strdate:
      sep_in_date = sep
      break
  strdate = strdate.replace(sep_in_date, tosep)
  strdate, pdate = return_strdate_in_fields_order_if_good_or_None(strdate, tosep, sourceposorder)
  if strdate is None:
    return None
  if sourceposorder == targetposorder:
    return strdate
  return put_date_fields_in_order(strdate, pdate, tosep, targetposorder)

def return_strdate_in_fields_order_if_good_or_None(strdate, sep, posorder):
  pp = strdate.split(sep)
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
  year = None; month = None; day = None
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

def put_date_fields_in_order(strdate, pdate, sep, targetposorder):
  '''
    Consider this function private, ie,
    strdate should already have been tested a good strdate,
    which is good in caller convert_sep_or_datefields_position_for_ymdstrdate()
  :param strdate:
  :param sep:
  :param posorder:
  :return:
  '''
  y = pdate.year; m = str(pdate.month).zfill(2); d = str(pdate.day).zfill(2)
  odict = {'y':y, 'm':m, 'd':d, 'sep':sep}
  if targetposorder == 'ymd':
    odate = '%(y)s%(sep)s%(m)s%(sep)s%(d)s' %odict
    return odate
  elif targetposorder == 'ydm':
    odate = '%(y)s%(sep)s%(d)s%(sep)s%(m)s' %odict
    return odate
  elif targetposorder == 'myd':
    odate = '%(m)s%(sep)s%(y)s%(sep)s%(d)s' %odict
    return odate
  elif targetposorder == 'mdy':
    odate = '%(m)s%(sep)s%(d)s%(sep)s%(y)s' %odict
    return odate
  elif targetposorder == 'dmy':
    odate = '%(d)s%(sep)s%(m)s%(sep)s%(y)s' %odict
    return odate
  elif targetposorder == 'dym':
    odate = '%(d)s%(sep)s%(y)s%(sep)s%(m)s' %odict
    return odate
  return None

def convert_yyyymmdd_strdate_to_dtdate_or_today(strdate):
  pdate = convert_yyyymmdd_strdate_to_dtdate_or_None(strdate)
  if pdate is None:
    pdate = datetime.date.today()
  return pdate

def make_tstamp_for_filename(dtime=None):
  if dtime is None or type(dtime) != datetime.datetime:
    dtime = datetime.datetime.now()
  strdt = str(dtime)
  strdt = strdt.split('.')[0]
  strdt = strdt.replace(':', '')
  strdt = strdt.replace('-', '')
  strdt = strdt.replace(' ', 'T')
  return strdt

def convert_yyyymmdd_strdate_to_dtdate_or_None(strdate):
  if strdate is None:
    return None
  if type(strdate) != str:
    try:
      _, _, _ = strdate.year, strdate.month, strdate.day
      return strdate # though it's not a str, it has the three attributes year, month and day
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
  pdate = convert_date_to_mmddyyyy_str_or_None(pdate)
  if pdate is None:
    pdate = datetime.date.today()
  return pdate

def convert_date_to_mmddyyyy_str_or_None(pdate):
  if pdate is None:
    return None
  indate = pdate # copy.copy() not needed to protect side-effect against pdate
  if type(indate) == str:
    indate = convert_yyyymmdd_strdate_to_dtdate_or_None(indate)
    if indate is None:
      return None
  mm = str(indate.month).zfill(2)
  dd = str(indate.day).zfill(2)
  yyyy = str(indate.year)
  mmddyyyy = '%s-%s-%s' %(mm, dd, yyyy)
  return mmddyyyy

def adhoc_test1():
  strdate = '2020-7-14'
  mmddyyyy = convert_date_to_mmddyyyy_str_or_None(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = '2020.7.14'
  mmddyyyy = convert_date_to_mmddyyyy_str_or_None(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = '2020/7/14'
  mmddyyyy = convert_date_to_mmddyyyy_str_or_None(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = '20200714'
  mmddyyyy = convert_date_to_mmddyyyy_str_or_None(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = 'bla'
  mmddyyyy = convert_date_to_mmddyyyy_str_or_None(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = '2020714'
  mmddyyyy = convert_date_to_mmddyyyy_str_or_None(strdate)
  print(strdate, '=>', mmddyyyy)
  inistrdate = '20200717'
  fimstrdate = '20200720'
  daterange = get_daterange(inistrdate, fimstrdate)
  for pdate in daterange:
    print ('date', pdate, 'weekday', is_date_weekend(pdate))
  departdate = '20200719'
  pdate = get_date_or_previous_monday_to_friday(departdate)
  print('departdate', departdate, ' =>', pdate)
  strdt = '2020-07-23 13:02:43.561'
  pdate = convert_yyyymmdd_strdate_to_dtdate_or_None(strdt)
  print('pdate', pdate)

def adhoc_test2():
  '''

  :return:
  '''
  stryear = '2020';   strmonth = '7';   strday = '3';
  strdate = '%s-%s-%s' % (stryear, strmonth, strday)
  expected_date = datetime.date(int(stryear), int(strmonth), int(strday))
  returned_date = returns_date_or_today(strdate)
  print ('expected_date', expected_date, 'returned_date', returned_date)
  stryear = '2020';   strmonth = '13';   strday = '3';
  strdate = '%s-%s-%s' % (stryear, strmonth, strday)
  expected_date = None
  returned_date = returns_date_or_today(strdate)
  print ('expected_date', expected_date, 'returned_date', returned_date)

def adhoc_test3():
  unordered = []
  d1 = datetime.date(2020, 4, 15)
  unordered.append(d1)
  d2 = datetime.date(2020, 2, 4)
  unordered.append(d2)
  d3 = datetime.date(2020, 3, 11)
  unordered.append(d3)
  asc_ordered = sort_datelist_asc(unordered)
  desc_ordered = sort_datelist_desc(unordered)
  print('unordered', unordered)
  print('asc_ordered', asc_ordered)
  print('desc_ordered', desc_ordered)

def adhoc_test4():
  datelist = []
  d = 'blah bla'
  datelist.append(d)
  d = datetime.date(2020, 3, 11)
  datelist.append(d)
  d = '2020-5-2'
  datelist.append(d)
  datelist.append(d)
  d = datetime.date(2020, 4, 15)
  datelist.append(d)
  datelist.append(d)
  datelist.append(d)
  prepdatelist = prepare_datelist_uniq_n_in_desc_order(datelist)
  print (datelist)
  print (prepdatelist)

def process():
  # adhoc_test1()
  adhoc_test4()

if __name__ == "__main__":
  process()
