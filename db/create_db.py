#!/usr/bin/env python3
"""
create_db.py
"""
import config as cfg

sql_create_table_cpis = """
CREATE TABLE IF NOT EXISTS cpi_indices (
  seriesid varchar(12) NOT NULL,
  refdate date NOT NULL,
  baselineindex real NOT NULL,
  created_at datetime,
  modified_at datetime,
  PRIMARY KEY (seriesid, refdate)
)
"""
sql_create_table_exchange = """
CREATE TABLE IF NOT EXISTS exchangerates (
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
  conn = cfg.get_connection()
  cur = conn.cursor()
  print('create_table_cpis')
  print('=================')
  print(sql_create_table_cpis)
  cur.execute(sql_create_table_cpis)
  print('Finished')


def create_table_exchangerates():
  conn = cfg.get_connection()
  cur = conn.cursor()
  print('create_table_exchangerates')
  print('==========================')
  print(sql_create_table_exchange)
  cur.execute(sql_create_table_exchange)
  print('Finished')


def process():
  create_table_cpis()
  create_table_exchangerates()


if __name__ == '__main__':
  process()
