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

"""
import datetime
import os.path
import sqlite3
import models.budgets.pb.orc_datum_model as orcmdl
import settings as sett
PPUBASE_TABLENAME = 'ppubase_orc'
PRICEBANK_TABLENAME = 'pricebank_orc'
ORCDADOS_FOLDERNAME = 'orçs_dados'
ORCDADOS_SQLFILENAME = 'orçs_db.sqlite'


def get_orcdados_folderpath():
  datafolderpath = sett.get_datafolder_abspath()
  orcsdados_folderpath = os.path.join(datafolderpath, ORCDADOS_FOLDERNAME)
  return orcsdados_folderpath


def get_orcdados_sqlitefilepath():
  orcsdados_folderpath = get_orcdados_folderpath()
  orcsdados_sqlitefilepath = os.path.join(orcsdados_folderpath, ORCDADOS_SQLFILENAME)
  return orcsdados_sqlitefilepath


def get_connection(p_filepath=None):
  filepath = p_filepath or get_orcdados_sqlitefilepath()
  return sqlite3.connect(filepath)


def ppubase_sqlcreatetable_str(tablename=None):
  tablename = PPUBASE_TABLENAME if tablename is None else tablename
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
  tablename = PRICEBANK_TABLENAME if tablename is None else tablename
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
  conn = get_connection()
  cursor = conn.cursor()
  sqls, tablenames = [], []
  tablenames.append(PPUBASE_TABLENAME)
  sql = ppubase_sqlcreatetable_str()
  sqls.append(sql)
  tablenames.append(PRICEBANK_TABLENAME)
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
