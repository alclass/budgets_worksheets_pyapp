#!/usr/bin/env python3
"""
art/inflmeas/bcb_br/classes/daycurrexchrate_sqlal.py
  models the sql-table `currencies_exchangerates` via SqlAlchemy

At the time of this writing, a sqlite file maintains the configured dbtable.
"""
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, Time, String, TIMESTAMP
from sqlalchemy.sql.expression import asc
import settings as sett
import lib.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import lib.datefs.convert_to_datetime_wo_intr_sep_posorder as cvdt
import art.inflmeas.bcb_br.classes as pkg
import lib.db.sqlalch.sqlalchemy_connection_clsmod as consa
Base = declarative_base()
EXCHRATE_DBTABLENAME = pkg.EXCHRATE_DBTABLENAME


class SADayCurrExchRate(Base):

  EXCHANGE_RATE_DECIMAL_TO_INTEGER = 10000  # for keeping quotevalue as integer in db and packing/unpacking it here

  __tablename__ = EXCHRATE_DBTABLENAME

  id = Column(Integer, primary_key=True)
  curr_num = Column(String(3), default=sett.CURR_BRL)
  curr_den = Column(String(3), default=sett.CURR_USD)
  buyprice_as_int = Column(Integer, name='buypriceint', nullable=True)  # DECIMAL(precision=4)
  sellprice_as_int = Column(Integer, name='sellpriceint', nullable=True)
  refdate = Column(Date, unique=True)
  quotestime = Column(Time, nullable=True)
  # infofrom = Column(String(10), default='BCB PTAX')
  created_at = Column(TIMESTAMP, default=datetime.datetime.now)  # utcnow() uses UTC (SaoPaulo timezone plus 3h)
  updated_at = Column(TIMESTAMP, nullable=True, onupdate=datetime.datetime.now)
  infofrom = 'BCB PTAX'

  @property
  def quote_as_datetime(self):
    if self.refdate is None:
      return None
    dt = datetime.datetime(
      self.refdate.year,
      self.refdate.month,
      self.refdate.day
    )
    if self.quotestime:
      dt = datetime.datetime(
        self.refdate.year,
        self.refdate.month,
        self.refdate.day,
        self.quotestime.hour,
        self.quotestime.minute,
        self.quotestime.second,
        self.quotestime.microsecond,
      )
    return dt

  @quote_as_datetime.setter
  def quote_as_datetime(self, pdatetime):
    if pdatetime is None:
      return
    _, ptime = cvdt.split_date_n_time_from_datetime(pdatetime)  # pdate, _
    # self.refdate = pdate
    self.quotestime = ptime

  @property
  def buyprice(self):
    if self.buyprice_as_int is None:
      return None
    return self.buyprice_as_int / self.EXCHANGE_RATE_DECIMAL_TO_INTEGER

  @property
  def sellprice(self):
    if self.sellprice_as_int is None:
      return None
    return self.sellprice_as_int / self.EXCHANGE_RATE_DECIMAL_TO_INTEGER

  @buyprice.setter
  def buyprice(self, buyquote_as_decimal):
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
    self.buyprice_as_int = int(buyquote_as_decimal * self.EXCHANGE_RATE_DECIMAL_TO_INTEGER)

  @sellprice.setter
  def sellprice(self, sellquote_as_decimal):
    if sellquote_as_decimal is None:
      return
    try:
      sellquote_as_decimal = float(sellquote_as_decimal)
    except ValueError:
      return
    self.sellprice_as_int = int(sellquote_as_decimal * self.EXCHANGE_RATE_DECIMAL_TO_INTEGER)

  def __repr__(self):
    buypricefloat = 'w/i'
    sellpricefloat = 'w/i'
    if self.buyprice is not None:
      buypricefloat = '%.4f' % self.buyprice
    if self.sellprice is not None:
      sellpricefloat = '%.4f' % self.sellprice
    outstr = '<ExRate %s/%s buy=%s sell=%s on d=%s t=%s>' \
             % (self.curr_num, self.curr_den, buypricefloat, sellpricefloat, self.refdate, self.quotestime)
    return outstr


def ahdoc_test_insert_etc():
  session = consa.get_sa_session()
  quotesdate = cnv.make_date_or_today('2019-12-31')
  exrate = session.query(SADayCurrExchRate).filter(SADayCurrExchRate.refdate == quotesdate).first()
  if exrate is None:
    print(quotesdate, 'does not exist in db')
  else:
    print(quotesdate, 'exists in db')
  print(exrate)
  session.close()


def print_db():
  sqlal_o = consa.SqlAlchemyConnector()
  session = sqlal_o.get_sa_session()
  exrates = session.query(SADayCurrExchRate). \
      order_by(asc(SADayCurrExchRate.refdate)).\
      all()
  scrmsg = f"""ExchangeRateDate: 1) create table | 2) read table 
  tablename = {SADayCurrExchRate.__tablename__} | Base.metadata.create_all(con.sqlalchemy_engine
  """
  print(scrmsg)
  for i, exrate in enumerate(exrates):
    print(i+1, exrate)
  print('Total records =', len(exrates))


def adhoc_test():
  ahdoc_test_insert_etc()


def process():
  print_db()


if __name__ == "__main__":
  process()
