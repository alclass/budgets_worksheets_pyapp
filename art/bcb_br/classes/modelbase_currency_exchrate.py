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
import lib.db.db_settings as dbs
import lib.datefs.convert_to_date_wo_intr_sep_posorder as cnv
EXRATE_TABLENAME = dbs.EXRATE_TABLENAME
BRL, EUR, USD = 'BRL', 'EUR', 'USD'
DEFAULT_CURR_NUM = BRL
DEFAULT_CURR_DEN = USD
REGISTERED_3LETTER_CURRENCIES = [BRL, USD, EUR]


class CurrencyPairExchangeRateOnDate:

  n_decplaces_for_div_intprices = 4  # this means intprices should be divided by 10 ** n_decplaces_for_div_intprices

  def __init__(self, dailydate, curr_num=None, curr_den=None):
    self.dailydate = dailydate
    self.curr_num, self.curr_den = curr_num, curr_den
    self._buypriceint = None
    self._sellpriceint = None
    self.treat_attrs()

  def treat_attrs(self):
    self.treat_dailydate()
    self.treat_currency_pair()

  def treat_dailydate(self):
    self.dailydate = cnv.make_date_or_none(self.dailydate)
    if self.dailydate is None:
      errmsg = f"Data Error: dailydate is None when instantiating ExchangeRateDate. Halting."
      raise ValueError(errmsg)

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

  @property
  def divider_for_intprices(self):
    return 10 ** self.n_decplaces_for_div_intprices

  @property
  def buyprice(self):
    try:
      return self.buypriceint/self.divider_for_intprices
    except (TypeError, ValueError):
      pass
    return None

  @property
  def sellprice(self):
    try:
      return self.sellpriceint/self.divider_for_intprices
    except (TypeError, ValueError):
      pass
    return None

  @property
  def buypriceint(self):
    return self._buypriceint

  @buypriceint.setter
  def buypriceint(self, p_buypriceint):
    try:
      self._buypriceint = int(p_buypriceint)
    except (TypeError, ValueError):
      pass

  @property
  def sellpriceint(self):
    return self._sellpriceint

  @sellpriceint.setter
  def sellpriceint(self, p_sellpriceint):
    try:
      self._sellpriceint = int(p_sellpriceint)
    except (TypeError, ValueError):
      pass

  def make_n_get_exrtobj_with_inverted_currency_pairs(self):
    o_inv = CurrencyPairExchangeRateOnDate(self.dailydate, curr_num=self.curr_den, curr_den=self.curr_num)
    inv_sellprice = 1 / self.buyprice
    o_inv.buypriceint = inv_sellprice * self.divider_for_intprices
    inv_sellprice = 1 / self.sellprice
    o_inv.sellpriceint = inv_sellprice * self.divider_for_intprices
    return o_inv

  def report_invert_curr_pair(self):
    o_inv = self.make_n_get_exrtobj_with_inverted_currency_pairs()
    scrmsg = f"Inverted exchange rate is: {o_inv}"
    print(scrmsg)

  def __str__(self):
    buystr = 's/inf' if self.buyprice is None else f"{self.buyprice:5.04f}"
    sellstr = 's/inf' if self.sellprice is None else f"{self.sellprice:5.04f}"
    outstr = f"""{self.__class__.__name__}
    dailydate = {self.dailydate}
    curr_pair = {self.curr_num}/{self.curr_den}
    buyprice = {buystr}
    sellprice = {sellstr}
    """
    return outstr


def adhoc_test():
  dailydate = '2024-12-13'
  exrt_o = CurrencyPairExchangeRateOnDate(dailydate=dailydate)
  exrt_o.buypriceint = 54321
  exrt_o.sellpriceint = 54422
  print(exrt_o)
  exrt_o.report_invert_curr_pair()


def process():
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
