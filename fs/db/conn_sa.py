#!/usr/bin/python3
"""
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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import settings


def get_sa_session():
  sqlite_filepath = config.get_exchange_rate_sqlite_filepath()
  engine_line = 'sqlite:///' + sqlite_filepath
  if engine_line.startswith('mysql'):
    engine_line = engine_line + '?charset=utf8mb4'
  sqlalchemy_engine = create_engine(engine_line)
  # print (engine_line)
  session = sessionmaker(bind=sqlalchemy_engine)
  return session


def adhoc_test():
  print('adhoc_test')
  session = get_sa_session()
  print('Session', session)


def process():
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
