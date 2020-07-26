#!/usr/bin/env python3
import datetime

def is_date_weekend(pdate):
  indate = convert_yyyymmdd_strdate_to_dtdate(pdate)
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
  indate = convert_yyyymmdd_strdate_to_dtdate(pdate)
  if max_recurse > WEEKEND_PREVIOUS_DATE_MAX_RECURSE:
    return None
  if is_date_weekend(indate):
    previous_date = indate - datetime.timedelta(days=1)
    return get_date_or_previous_monday_to_friday(previous_date, max_recurse+1)
  return indate

def get_daterange(pinidate, pfimdate, accept_future=False):
  today = datetime.date.today()
  inidate = convert_yyyymmdd_strdate_to_dtdate(pinidate)
  if inidate is None:
    inidate = today
  fimdate = convert_yyyymmdd_strdate_to_dtdate(pfimdate)
  if fimdate is None:
    fimdate = today
  if inidate > today and not accept_future:
    inidate = today
  if fimdate > today and not accept_future:
    fimdate = today
  daterange = [inidate]
  if inidate == fimdate:
    pass
  elif inidate < fimdate:
    ongoingdate = inidate
    while ongoingdate < fimdate: # fimdate will also be included in daterange
      ongoingdate =  ongoingdate + datetime.timedelta(days=1)
      daterange.append(ongoingdate)
  elif inidate > fimdate:
    ongoingdate = inidate
    while ongoingdate > fimdate: # fimdate will also be included in daterange
      ongoingdate =  ongoingdate - datetime.timedelta(days=1)
      daterange.append(ongoingdate)
  return daterange

def pick_first_word(phrase):
  if phrase is None:
    return None
  if ' ' not in phrase:
    return phrase
  return phrase.split(' ')[0]

def convert_yyyymmdd_strdate_to_dtdate(strdate):
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
    strdd = pick_first_word(pp[2])
  try:
    yyyy = int(stryyyy)
    mm = int(strmm)
    dd = int(strdd)
  except ValueError:
    return None
  return datetime.date(yyyy, mm, dd)

def convert_date_to_mmddyyyy_str(pdate):
  if pdate is None:
    return None
  indate = pdate # copy.copy() not needed to protect side-effect against pdate
  if type(indate) == str:
    indate = convert_yyyymmdd_strdate_to_dtdate(indate)
    if indate is None:
      return None
  mm = str(indate.month).zfill(2)
  dd = str(indate.day).zfill(2)
  yyyy = str(indate.year)
  mmddyyyy = '%s-%s-%s' %(mm, dd, yyyy)
  return mmddyyyy

def adhoc_test():
  strdate = '2020-7-14'
  mmddyyyy = convert_date_to_mmddyyyy_str(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = '2020.7.14'
  mmddyyyy = convert_date_to_mmddyyyy_str(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = '2020/7/14'
  mmddyyyy = convert_date_to_mmddyyyy_str(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = '20200714'
  mmddyyyy = convert_date_to_mmddyyyy_str(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = 'bla'
  mmddyyyy = convert_date_to_mmddyyyy_str(strdate)
  print(strdate, '=>', mmddyyyy)
  strdate = '2020714'
  mmddyyyy = convert_date_to_mmddyyyy_str(strdate)
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
  pdate = convert_yyyymmdd_strdate_to_dtdate(strdt)
  print('pdate', pdate)

def process():
  adhoc_test()

if __name__ == "__main__":
  process()
