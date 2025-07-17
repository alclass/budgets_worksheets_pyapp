#!/usr/bin/python3
"""
fs/db/conn_sa.py
  This config module organizes the Sqlalchemy session object for
    the sql-DB (at this moment under sqlite) for exchange rates and index indicators.

On the same theme, at the time of this writing, CEP "geodata" is placed
  in a different sqlite file configured by another Python module.

Some notes concerning mysql work with sqlalchemy:
------------------------------------------------
In order to make mysql work with sqlalchemy, two things were to be done:
  1) Ubuntu's package python3-dev and libmysqlclient-dev were installed;
  2) after that, mysqlclient was installed via pip.

this_db = config.THIS_DATABASE;
user         = config.DATABASE_DICT[this_db]['USER']
password     = config.DATABASE_DICT[this_db]['PASSWORD']
address      = config.DATABASE_DICT[this_db]['ADDRESS']
port         = config.DATABASE_DICT[this_db]['PORT']
databasename = config.DATABASE_DICT[this_db]['DATABASENAME']

engine_line = this_db + '://' + user + ':' + password + '@' + address + '/' + databasename
"""
import os.path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import settings as sett


class SqlAlchemyConnector:

  def __init__(self, datafilepath=None):
    self.sqlitedatafilepath = datafilepath
    self.treat_attrs()

  def treat_attrs(self):
    if self.sqlitedatafilepath is None or not os.path.isfile(self.sqlitedatafilepath):
      self.sqlitedatafilepath = sett.get_exchange_rate_sqlite_filepath()

  def get_sa_engine(self):
    engine_line = 'sqlite:///' + self.sqlitedatafilepath
    if engine_line.startswith('mysql'):
      engine_line = engine_line + '?charset=utf8mb4'
    sqlalchemy_engine = create_engine(engine_line)
    return sqlalchemy_engine

  def get_sa_session_handler(self):
    session = sessionmaker(bind=self.get_sa_engine())
    return session

  def get_sa_session(self):
    sessionhandler = self.get_sa_session_handler()
    session = sessionhandler()
    return session


def adhoc_test():
  conn_o = SqlAlchemyConnector()
  print('adhoctest3')
  session = conn_o.get_sa_session_handler()
  print('Session', session)


def process():
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
