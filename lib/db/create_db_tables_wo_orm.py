#!/usr/bin/env python3
"""
fs/db/create_db_tables_wo_orm.py

"""
import settings as cfg
import lib.db.db_settings as dbs
EXRATE_TABLENAME = dbs.EXRATE_TABLENAME
IDXIND_TABLENAME = dbs.IDXIND_TABLENAME


sql_create_table_idxind = f"""
CREATE TABLE IF NOT EXISTS {IDXIND_TABLENAME} (
  seriesid varchar(12) NOT NULL,
  refmonthdate date NOT NULL,
  baselineindex real NOT NULL,
  created_at datetime,
  modified_at datetime,
  PRIMARY KEY (seriesid, refmonthdate)
)
"""
sql_create_table_exchange = f"""
CREATE TABLE IF NOT EXISTS {EXRATE_TABLENAME} (
  numerator_curr character(3) NOT NULL,
  denominator_curr character(3) NOT NULL,
  refdate date NOT NULL,
  buyexchangerate real,
  sellexchangerate real NOT NULL,
  created_at datetime,
  modified_at datetime,
  PRIMARY KEY (numerator_curr, numerator_curr, refdate)
)
"""


def create_table_cpis():
  conn = cfg.get_sqlite_connection()
  cur = conn.cursor()
  print('Creating table [', IDXIND_TABLENAME, '] if not exists')
  print('='*50)
  print(sql_create_table_idxind)
  cur.execute(sql_create_table_idxind)
  print('Finished (see results above).')


def create_table_exchangerates():
  conn = cfg.get_sqlite_connection()
  cur = conn.cursor()
  print('Creating table [', EXRATE_TABLENAME, '] if not exists')
  print('='*50)
  print('==========================')
  print(sql_create_table_exchange)
  cur.execute(sql_create_table_exchange)
  print('Finished (see results above).')


def process():
  create_table_cpis()
  create_table_exchangerates()


if __name__ == '__main__':
  process()
