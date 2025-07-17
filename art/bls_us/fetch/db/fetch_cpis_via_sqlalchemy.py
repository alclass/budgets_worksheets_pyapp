#!/usr/bin/env python3
"""
lib/db/sqlite/db_sqlite_manager.py

# create an in-memory SQLite database
engine = create_engine('sqlite:///:memory:', echo=True)

# create the users table
Base.metadata.create_all(engine)

# create a session to manage the connection to the database
Session = sessionmaker(bind=engine)
session = Session()
"""
import lib.db.sqlalchemy_connection_clsmod as sqlalch  # sqlalch.SqlAlchemyConnector
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
Base = sqlalchemy.orm.declarative_base()


class SqlAlchExchRateReader(Base):
  """
  def __init__(self):
    self.sqlalch_o = sqlalch.SqlAlchemyConnector()
  """

  __tablename__ = 'currencies_exchangerates'
  id = Column(Integer, primary_key=True)
  refdate = Column(DateTime)
  curr_num = Column(String)
  curr_den = Column(String)
  buypriceint = Column(Integer)
  sellpriceint = Column(Integer)
  buysell_decplaces = 4

  @property
  def currnum_slash_currden(self):
    _currnum_slash_currden = f"{self.curr_num}/{self.curr_den}"
    return _currnum_slash_currden

  @property
  def buyprice(self):
    try:
      decval = self.buypriceint / (10 ** self.buysell_decplaces)
      return decval
    except TypeError:
      pass
    return None

  @property
  def sellprice(self):
    try:
      decval = self.sellpriceint / (10 ** self.buysell_decplaces)
      return decval
    except TypeError:
      pass
    return None

  @property
  def strbuyprice(self):
    if self.buyprice is not None:
      sbuyprice = f"{self.buyprice:5.03f}"
      return sbuyprice
    return None

  @property
  def strsellprice(self):
    if self.sellprice is not None:
      ssellprice = f"{self.sellprice:5.03f}"
      return ssellprice
    return None

  def __repr__(self):
    buyp = f"{self.buyprice:5.03f}" if self.buyprice is not None else 's/inf'
    sellp = f"{self.sellprice:5.03f}" if self.sellprice is not None else 's/inf'
    sdate = f"{self.refdate.year}-{self.refdate.month}-{self.refdate.day}"
    return (f"<ExRate({self.currnum_slash_currden}, date={sdate}, "
            f" buy={buyp}, sell={sellp}>")


sqlalch_o = sqlalch.SqlAlchemyConnector()
session = sqlalch_o.get_sa_session()
# add a new user to the database
# user = SqlAlchExchRateReader()
# session.add(user)
# session.commit()

# query the users table
exchrates = session.query(SqlAlchExchRateReader).all()
for i, exrate in enumerate(exchrates):
  line = f"{exrate.refdate} | {exrate.strbuyprice}"
  seq = i + 1
  print(seq, line)
