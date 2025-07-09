#!/usr/bin/env python3
"""
fs/indices/bcb_br/bcb_exchrate_cls.py
"""
import fs.datefs.convert_to_date_wo_intr_sep_posorder as dtfs
import datetime
import collections as coll


namedtuple_exchangerate = coll.namedtuple(
  'ExchangeRateNT',
  'exchratedate curr_num curr_den buyquote sellquote'
)


class ExchangeRate:
  """
    self.exchratedate = pdate
    self.curr_num = curr_num
    self.curr_den = curr_den
    self.buyprice = buyprice
    self.sellprice = sellprice
  """

  def __init__(
      self,
      pdate: datetime.date,
      curr_num: str,
      curr_den: str,
      buyprice: float,
      sellprice: float
    ):
    self.exchratedate = pdate
    self.curr_num = curr_num
    self.curr_den = curr_den
    self.buyprice = buyprice
    self.sellprice = sellprice

  def to_named_tuple(self):
    return namedtuple_exchangerate(
      exchratedate=self.exchratedate,
      curr_num=self.curr_num,
      curr_den=self.curr_den,
      buyquote=self.buyprice,
      sellquote=self.sellprice,
    )

  @property
  def currnum_currden(self):
    return f"{self.curr_num}/{self.curr_den}"

  def tell_buyquote_str(self):
    return f"{self.buyprice:5.3f} {self.currnum_currden} on {self.exchratedate}"

  def __str__(self):
    outstr = f"""
    exchratedate = {self.exchratedate}
    curr_num = {self.curr_num}
    curr_den = {self.curr_den}
    buyquote = {self.buyprice}
    sellquote = {self.buyprice}
    """
    return outstr


def adhoctest1():
  pdate = dtfs.make_date_or_today()
  curr_num = 'BRL'
  curr_den = 'USD'

  exrate = ExchangeRate(
    pdate=pdate,
    curr_num=curr_num,
    curr_den=curr_den,
    buyquote=5.23,
    sellquote=5.23,
  )
  print(exrate)
  print(exrate.to_named_tuple())
  print(exrate.tell_buyquote_str())


def process():
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoctest1()
