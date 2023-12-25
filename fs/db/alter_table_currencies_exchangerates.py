#!/usr/bin/env python3
"""
fs/db/alter_table_currencies_exchangerates.py

"""
import settings as sett


def alter_table():
  """
    Originally:
  CREATE TABLE "currencies_exchangerates" (
    "id"	INTEGER NOT NULL,
    "curr_num"	char(3),
    "curr_den"	char(3),
    "buypriceint"	INTEGER,
    "sellpriceint"	INTEGER COLLATE BINARY,
    "refdate"	DATE COLLATE BINARY,
    "quotestime"	TIME COLLATE BINARY,
    "created_at"	timestamp COLLATE BINARY,
    "updated_at"	timestamp,
    UNIQUE("refdate"),
    PRIMARY KEY("id")
  )

    Updating the UNIQUE constraint:
  CREATE UNIQUE INDEX unq_currnum_currden_refdate ON currencies_exchangerates(curr_num, curr_den, refdate);

    This form below does not work for sqlite:
  ALTER TABLE currencies_exchangerates
    ADD CONSTRAINT unq_currnum_currden_refdate UNIQUE(curr_num, curr_den, refdate);

  CREATE TABLE "currencies_exchangerates" (
    "id"	INTEGER NOT NULL,
    "curr_num"	char(3),
    "curr_den"	char(3),
    "buypriceint"	INTEGER,
    "sellpriceint"	INTEGER COLLATE BINARY,
    "refdate"	DATE COLLATE BINARY,
    "quotestime"	TIME COLLATE BINARY,
    "created_at"	timestamp COLLATE BINARY,
    "updated_at"	timestamp,
    UNIQUE("refdate"),
    PRIMARY KEY("id")
)
  """
  sql = """
  CREATE UNIQUE INDEX unq_currnum_currden_refdate ON currencies_exchangerates(curr_num, curr_den, refdate);
  """
  print(sql)
  conn = sett.get_sqlite_connection()
  cursor = conn.cursor()
  retval = cursor.execute(sql)
  print(retval)
  conn.commit()
  conn.close()


alter_table()
