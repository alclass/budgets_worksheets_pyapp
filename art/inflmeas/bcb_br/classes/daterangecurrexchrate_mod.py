#!/usr/bin/env python3
"""
models/exrate/currency_exchange_rate_model.py
  models the sql-table `currencies_exchangerates` via SqlAlchemy

At the time of this writing, a sqlite file maintains the table.

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, Time, String, TIMESTAMP
from sqlalchemy.sql.expression import asc
import settings as sett
import lib.datefs.convert_to_datetime_wo_intr_sep_posorder as cvdt
"""
import copy
from dateutil.relativedelta import relativedelta
import art.inflmeas.bcb_br.classes as pkg  # pkg
import lib.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import art.inflmeas.bcb_br.classes.daycurrexchrate_mod as dayexrtmod  # dayexrtmod.DayCurrExchRate
EXCHRATE_DBTABLENAME = pkg.EXCHRATE_DBTABLENAME
BRL, EUR, USD = pkg.BRL, pkg.EUR, pkg.USD
DEFAULT_CURR_NUM = pkg.DEFAULT_CURR_NUM
DEFAULT_CURR_DEN = pkg.DEFAULT_CURR_DEN
REGISTERED_3LETTER_CURRENCIES = pkg.REGISTERED_3LETTER_CURRENCIES


class DateRangeCurrExchRate:

  # db-field-intprices should be divided by 10 ** n_decplaces_for_div_intprices
  n_decplaces_for_div_intprices = pkg.n_decplaces_for_div_intprices

  def __init__(self, date_fr=None, date_to=None, datelist=None, curr_num=None, curr_den=None):
    self.date_fr = date_fr
    self.date_to = date_to
    self.datelist = datelist
    self.curr_num, self.curr_den = curr_num, curr_den
    self.dates_n_exchrates_dict = {}
    self.treat_attrs()

  def treat_attrs(self):
    self.treat_dates()
    self.treat_currency_pair()

  def treat_dates(self):
    if self.datelist is not None:
      if isinstance(self.datelist, list):
        orig_list = copy.copy(self.datelist)
        self.datelist = cnv.trans_convertabledates_to_datelist(self.datelist)
        if len(orig_list) != len(self.datelist):
          errmsg = f"""Error: given datelist has non-date data. 
          entered = [{orig_list}]
          datelist = [{self.datelist}]
            Please, retry reentering dates."""
          raise TypeError(errmsg)
        # at this point, datelist is set, sort it and return
        self.datelist.sort()  # sort is required in this class, i.e., first date is least, last is greatest
        return
    self.datelist = None
    self.date_fr = cnv.make_date_or_none(self.date_fr)
    self.date_to = cnv.make_date_or_none(self.date_to)
    if self.date_fr is None:
      if self.date_to is None:
        self.date_to = cnv.make_date_or_today(self.date_to)
      self.date_fr = self.date_to - relativedelta(days=10)
    if self.date_to is None:
      self.date_to = self.date_fr + relativedelta(days=10)
    # swap if 'datefrom' is greater than 'dateto'
    if self.date_fr > self.date_to:
      tmpdate = self.date_fr
      self.date_fr = self.date_to
      self.date_to = tmpdate

  def treat_currency_pair(self):
    if self.curr_num is None:
      self.curr_num = DEFAULT_CURR_NUM
    if self.curr_num not in REGISTERED_3LETTER_CURRENCIES:
      errmsg = (f"Data Error: curr_num [{self.curr_num}] not in registered currencies {REGISTERED_3LETTER_CURRENCIES}."
                f" Halting.")
      raise ValueError(errmsg)
    if self.curr_den is None:
      self.curr_den = DEFAULT_CURR_DEN
    if self.curr_den not in REGISTERED_3LETTER_CURRENCIES:
      errmsg = (f"Data Error: curr_den [{self.curr_den}] not in registered currencies {REGISTERED_3LETTER_CURRENCIES}."
                f" Halting.")
      raise ValueError(errmsg)

  def add_or_update_dates_n_exchrates_dict(self, daycurrexchrate_o: dayexrtmod.DayCurrExchRate):
    if isinstance(daycurrexchrate_o, dayexrtmod.DayCurrExchRate):
      pdate = daycurrexchrate_o.dailydate
      if self.datelist:
        leastdate = self.datelist[0]
        greaterdate = self.datelist[-1]
      else:
        leastdate = self.date_fr
        greaterdate = self.date_to
      if pdate < leastdate or pdate > greaterdate:
        errmsg = f"Error: date {pdate} in exrt_obj is out of given range: {leastdate}, {greaterdate}"
        raise ValueError(errmsg)
      self.dates_n_exchrates_dict.update({pdate: daycurrexchrate_o})

  def gen_dates(self):
    """
    Generator for dates whether when date_fr and date_to are given or when datelist is
    """
    if self.datelist:
      for pdate in self.datelist:
        yield pdate
      return
    pdate = copy.copy(self.date_fr)
    while pdate <= self.date_to:
      yield pdate
      pdate = pdate + relativedelta(days=1)
    return

  @property
  def total_dates(self):
    if self.datelist:
      return len(self.datelist)
    # at this point, treat_dates() has guaranted that date_fr and date_to are datetime.date's
    diff = self.date_to - self.date_fr
    return diff.days + 1

  @property
  def len_dates(self):
    if self.datelist:
      return len(self.datelist)
    return len(list(self.gen_dates()))

  @staticmethod
  def make_line_w_sample_dates(datelist):
    outstr = ''
    if len(datelist) == 0:
      return ''
    if len(datelist) <= 3:
      outstr += '|'.join(datelist)
      return outstr
    outstr += f"{datelist[0]}|"
    outstr += f"{datelist[1]}|...|"
    outstr += f"{datelist[-1]}"
    return outstr

  def sample_datelist_if_any(self):
    if self.datelist:
      return self.make_line_w_sample_dates(self.datelist)
    datelist = list(self.gen_dates())
    return self.make_line_w_sample_dates(datelist)

  def print_exrate_data(self):
    scrmsg = 'Exchange Rate Date Data'
    print(scrmsg)
    for i, pdate in enumerate(self.dates_n_exchrates_dict):
      exrt_o = self.dates_n_exchrates_dict[pdate]
      seq = i + 1
      scrmsg = f"{seq} {exrt_o}"
      print(scrmsg)

  def __str__(self):
    outstr = f"""{self.__class__.__name__}
    curr_num = {self.curr_num} | curr_den = {self.curr_den}
    nº of exch-rates in obj = {len(self.dates_n_exchrates_dict)}
    nº of dates = {self.total_dates} | len dates = {self.len_dates}
    date_fr = {self.date_fr} | date_to = {self.date_to}
    datelist = {self.sample_datelist_if_any()}
    nº of exch-rates = {len(self.dates_n_exchrates_dict)}
    """
    return outstr


def adhoc_test():
  dailydate = '2024-12-13'
  exrt_o = dayexrtmod.DayCurrExchRate(dailydate=dailydate)
  exrt_o.buypriceint = 54321
  exrt_o.sellpriceint = 54422
  print(exrt_o)
  exrt_o.report_invert_curr_pair()
  # =============================
  dtrange = DateRangeCurrExchRate(date_fr=dailydate)
  dtrange.add_or_update_dates_n_exchrates_dict(exrt_o)
  # =============================
  dailydate = '2024-12-23'
  exrt_o = dayexrtmod.DayCurrExchRate(dailydate=dailydate)
  exrt_o.buypriceint = 45312
  exrt_o.sellpriceint = 45411
  dtrange.add_or_update_dates_n_exchrates_dict(exrt_o)
  print(dtrange)
  dtrange.print_exrate_data()


def process():
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
