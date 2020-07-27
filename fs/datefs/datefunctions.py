#!/usr/bin/env python3
import collections as coll
import datetime
import fs.textfs.strfs as strfs

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

def returns_date_or_None(pdate):
  return convert_yyyymmdd_strdate_to_dtdate_or_None(pdate)

def returns_date_or_today(pdate):
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

def convert_yyyymmdd_strdate_to_dtdate_or_today(strdate):
  pdate = convert_yyyymmdd_strdate_to_dtdate_or_None(strdate)
  if pdate is None:
    pdate = datetime.date.today()
  return pdate

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
