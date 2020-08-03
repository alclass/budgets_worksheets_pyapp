#!/usr/bin/env python3
"""
  docstring
"""
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Time, TIMESTAMP
from sqlalchemy.sql.expression import asc
import config
import fs.datefs.datefunctions as dtfs
import models.conn_sa as con

Base = declarative_base()


class ExchangeRateDate(Base):

  EXCHANGE_RATE_DECIMAL_TO_INTEGER = 10000  # for keeping quotevalue as integer in db and packing/unpacking it here

  __tablename__ = 'daily_exchange_rates'

  id = Column(Integer, primary_key=True)
  numerator_curr3 = Column(String(3), default=config.CURR_BRL)
  denominator_curr3 = Column(String(3), default=config.CURR_USD)
  buyquote_as_int = Column(Integer, name='buyquote', nullable=True)  # DECIMAL(precision=4)
  sellquote_as_int = Column(Integer, name='sellquote', nullable=True)
  quotesdate = Column(Date, unique=True)
  quotesdaytime = Column(Time)
  infofrom = Column(String(10), default='BCB PTAX')

  created_at = Column(TIMESTAMP, default=datetime.datetime.now)  # utcnow() uses UTC (SaoPaulo timezone plus 3h)
  updated_at = Column(TIMESTAMP, nullable=True, onupdate=datetime.datetime.now)

  @property
  def quotesdatetime(self):
    if self.quotesdate is None:
      return None
    return datetime.datetime(
      self.quotesdate.year,
      self.quotesdate.month,
      self.quotesdate.day,
      self.quotesdaytime.hour,
      self.quotesdaytime.minute,
      self.quotesdaytime.second
    )

  @quotesdatetime.setter
  def quotesdatetime(self, pdatetime):
    if pdatetime is None:
      return
    pdate, ptime = dtfs.split_date_n_time_from_datetime(pdatetime)
    self.quotesdate = pdate
    self.quotesdaytime = ptime

  @property
  def buyquote(self):
    if self.buyquote_as_int is None:
      return None
    return self.buyquote_as_int / self.EXCHANGE_RATE_DECIMAL_TO_INTEGER

  @property
  def sellquote(self):
    if self.sellquote_as_int is None:
      return None
    return self.sellquote_as_int / self.EXCHANGE_RATE_DECIMAL_TO_INTEGER

  @buyquote.setter
  def buyquote(self, buyquote_as_decimal):
    """
    Notice in db it's an integer that keeps 4 decimal places
      so this setter will multiply it to become an integer. The get-property will divide it back to a decimal.
    :param buyquote_as_decimal:
    :return:
    """
    if buyquote_as_decimal is None:
      return
    try:
      buyquote_as_decimal = float(buyquote_as_decimal)
    except ValueError:
      return
    self.buyquote_as_int = int(buyquote_as_decimal * self.EXCHANGE_RATE_DECIMAL_TO_INTEGER)

  @sellquote.setter
  def sellquote(self, sellquote_as_decimal):
    if sellquote_as_decimal is None:
      return
    try:
      sellquote_as_decimal = float(sellquote_as_decimal)
    except ValueError:
      return
    self.sellquote_as_int = int(sellquote_as_decimal * self.EXCHANGE_RATE_DECIMAL_TO_INTEGER)

  def __repr__(self):
    outstr = '<ExRate %s/%s exchange rate q=%.4f on d=%s>' \
             % (self.numerator_curr3, self.denominator_curr3, self.buyquote, self.quotesdate)
    return outstr


def ahdoc_test_insert_etc():
  session = con.Session()
  quotesdate = dtfs.returns_date_or_today('2015-11-13')
  exrate = session.query(ExchangeRateDate).filter(ExchangeRateDate.quotesdate == quotesdate).first()
  if exrate is None:
    print(quotesdate, 'exists in db')
    exrate = ExchangeRateDate()
    exrate.quotevalue = 3.4375
    exrate.quotesdate = quotesdate
    session.add(exrate)
    session.commit()
  else:
    exrate.quotevalue = exrate.quotevalue * 0.1
    session.commit()
    print(quotesdate, 'exists in db')
  print(exrate)
  session.close()


def print_db():
  session = con.Session()
  print('print_db =>')
  exrates = session.query(ExchangeRateDate). \
      order_by(asc(ExchangeRateDate.quotesdate)).\
      all()
  for exrate in exrates:
    print(exrate)
  print('Total records =', len(exrates))


def adhoc_test():
  ahdoc_test_insert_etc()


def process():
  print_db()


if __name__ == "__main__":
  process()
