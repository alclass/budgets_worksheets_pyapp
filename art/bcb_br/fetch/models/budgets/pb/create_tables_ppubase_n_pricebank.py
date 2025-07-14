#!/usr/bin/env python3
"""
models/budgets/pb/create_tables_ppubase_n_pricebank.py

SELECT * FROM table2
INNER JOIN table1
on

nt1 = nt_constr(
  n_jira='a', descr=None, n_orp=None, n_oport=None, date_ini=None,
  date_entr=None, date_exp_aprv=None, date_aprv=None, date_res_nect=None,
)

sql_create_table_cpis =
CREATE TABLE IF NOT EXISTS cpi_indices (
  x varchar(12) NOT NULL,
  x date NOT NULL,
  x real NOT NULL,
  created_at datetime,
  modified_at datetime,
  PRIMARY KEY (seriesid, refdate)
)

import datetime
import models.budgets.pb.orc_datum_model as orcmdl
import os.path
import sqlite3
import settings as sett
"""
import art.bcb_br.fetch.models.budgets.pb.db_n_file_settings as dbs  # for dbs.get_orcdados_folderpath


def ppubase_sqlcreatetable_str(tablename=None):
  tablename = dbs.PPUBASE_TABLENAME if tablename is None else tablename
  sql = f"""CREATE TABLE IF NOT EXISTS `{tablename}` (
    `seq` INT PRIMARY KEY,
    `ncmcode` INT,
    `ipi` FLOAT,
    `familycode` INT,
    `nmcode` INT,
    `partnumber` VARCHAR(40),
    `manufacturer_sname` VARCHAR(30),
    `textobreve` TEXT,
    `description` TEXT,
    `qty` INT,
    `meas_unit` VARCHAR(10),
    `n_prices` INT,
    `prices_dict_asstr` TEXT,
    `created_at` DATETIME,
    `modified_at` DATETIME,
    UNIQUE(NMCODE)
  );"""
  return sql


def pricebank_sqlcreatetable_str(tablename=None):
  tablename = dbs.PRICEBANK_TABLENAME if tablename is None else tablename
  sql = f"""CREATE TABLE IF NOT EXISTS `{tablename}` (
    `seq` INT PRIMARY KEY,
    `nmcode` INT,
    `orig_price` INT,
    `date` DATE,
    `multfact` INT,
    `updt_price` INT,
    `sourcename` INT,
    `pedido` INT,
    `contrato` INT,
    `url` INT,
    `created_at` DATETIME,
    `modified_at` DATETIME
  );"""
  return sql


def create_tables_if_not_exists():
  """
  Order is: (first) PPUBASE_TABLENAME, (second) PRICEBANK_TABLENAME
  """
  conn = dbs.get_connection()
  cursor = conn.cursor()
  sqls, tablenames = [], []
  tablenames.append(dbs.PPUBASE_TABLENAME)
  sql = ppubase_sqlcreatetable_str()
  sqls.append(sql)
  tablenames.append(dbs.PRICEBANK_TABLENAME)
  sql = pricebank_sqlcreatetable_str()
  sqls.append(sql)
  for i, tablename in enumerate(tablenames):
    seq = i + 1
    print(seq, 'create_table', tablename, 'if_not_exists')
    sql = sqls[i]
    print(sql)
    retval = cursor.execute(sql)
    print('retval', retval)
    if retval:
      print('Committing connexion => retval', retval)
      conn.commit()
  conn.close()


def adhoctest():
  pass


def process():
  create_tables_if_not_exists()


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
