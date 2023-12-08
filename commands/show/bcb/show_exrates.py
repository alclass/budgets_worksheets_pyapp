#!/usr/bin/env python3
"""
calc_monet_corr.py
SELECT * FROM daily_exchange_rates WHERE quotesdate = "2022-04-01";
"""
import datetime
from dateutil.relativedelta import relativedelta
import models.exrate.exchange_rate_modelmod as exrt  # exrt.ExchangeRateDate()
import fs.datefs.dategenerators as gendt
import fs.datefs.datefunctions as dtfs
import pandas as pd
# when just needing weekday from date, it can be called directly: adate.weekday() instead of calendar.weekday(adate)
# import calendar


def show_exrates_on_date(pdate):
  """
  Curiosity: In:
    weekday, days_in_month = calendar.monthrange(indate.year, indate. month)
  weekday (0 Monday to 6 Sunday) means the weekday of the first day of the given year/month
  Examples:
     weekday, _ = calendar.monthrange(2023, 3)
     answer is weekday = 1 Tuesday ie day 2022-03-01 falls on Tuesday
     weekday, _ = calendar.monthrange(2023, 4)
     answer is weekday = 4 Friday ie day 2022-04-01 falls on Friday
     weekday, _ = calendar.monthrange(2023, 5)
     answer is weekday = 6 Sunday ie day 2022-05-01 falls on Sunday
  """
  # exrate = exrt.ExchangeRateDate()
  indate = gendt.make_date_from_str_or_none(pdate)
  # weekdays range from 0 to 6 where 0 is Monday 6 is Sunday
  weekday3letter = dtfs.get_weekday3letter_from_date(indate)
  session = exrt.consa.get_sa_session()
  exchanger = session.query(exrt.ExchangeRateDate). \
      filter(exrt.ExchangeRateDate.quotesdate == indate). \
      first()
  strdate = dtfs.transform_date_to_other_order_fields_n_sep_or_none(indate)
  if exchanger:
    print('weekday', weekday3letter, strdate, exchanger)
  else:
    print('weekday', weekday3letter, ' | ', strdate, 'was not found in db.')
  return exchanger


def show_exrates_up_to(lastdate):
  before20days = lastdate - relativedelta(days=31)
  scrmsg = f"before20days {before20days} | lastdate {lastdate}"
  print(scrmsg)
  for pdate in gendt.gen_dailydates_bw_ini_fim_opt_order(lastdate, before20days, decrescent=True):
    show_exrates_on_date(pdate)
  exrate_dictlist = []
  for pdate in gendt.gen_dailydates_bw_ini_fim_opt_order(before20days, lastdate):
    exchanger = show_exrates_on_date(pdate)
    if exchanger:
      try:
        # sellquote_as_int is null (None) on holidays
        ratevalue = exchanger.sellquote_as_int / 10000
      except TypeError:
        continue
      pdict = {'date': exchanger.quotesdate, 'rate': ratevalue}
      exrate_dictlist.append(pdict)
  df = pd.DataFrame(exrate_dictlist)
  print(df.to_string())
  print(df.describe())


def show_last_exrates():
  """
  -cmc "2022-10-04" "2022-04-03"
  indate = "2022-04-01"
  show_exrates_on_date(indate)
  datelist = ["2022-04-03", "2022-10-04", "2022-10-05"]
  for pdate in datelist:
    show_exrates_on_date(pdate)
  mrange = ["2022-10-04", "2022-04-03"]
  dateini, datefim = "2022-03-27", "2022-05-13"
  """
  today = datetime.date.today()
  show_exrates_up_to(today)



def process():
  """
  """
  show_last_exrates()


if __name__ == '__main__':
  """
  process()
  """
  process()
