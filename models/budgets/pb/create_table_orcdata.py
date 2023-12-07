#!/usr/bin/env python3
"""
models/budgets/pb/create_table_orcdata.py

nt1 = nt_constr(
  n_jira='a', descr=None, n_orp=None, n_oport=None, date_ini=None,
  date_entr=None, date_exp_aprv=None, date_aprv=None, date_res_nect=None,
)

sql_create_table_cpis =
CREATE TABLE IF NOT EXISTS cpi_indices (
  seriesid varchar(12) NOT NULL,
  refdate date NOT NULL,
  baselineindex real NOT NULL,
  created_at datetime,
  modified_at datetime,
  PRIMARY KEY (seriesid, refdate)
)

"""
import datetime
import sqlite3
import models.budgets.pb.orc_datum_model as orcmdl
import settings as sett
tablename = 'orc_data'


def get_connection(p_filepath=None):
  filepath = p_filepath or sett.get_sqlite_appsdata_filepath()
  return sqlite3.connect(filepath)


def recup_field_sql_types():
  names_types_list = []
  for fieldname in orcmdl.orc_fieldtype_dict:
    vtype = orcmdl.orc_fieldtype_dict[fieldname]
    sqltype = 'TEXT'  # as a default for the IF's
    if vtype == str:
      sqltype = 'TEXT'
    elif vtype == int:
      sqltype = 'INTEGER'
    elif vtype == bool:
      sqltype = 'BOOLEAN'
    elif vtype == datetime.date:
      sqltype = 'DATE'
    tupl = (fieldname, sqltype)
    names_types_list.append(tupl)
  return names_types_list


def form_sqlcreatetable_str():
  names_types_list = []
  sql_createtable = f"CREATE TABLE IF NOT EXISTS {tablename} (\n"
  for fieldname in orcmdl.orc_fieldtype_dict:
    vtype = orcmdl.orc_fieldtype_dict[fieldname]
    is_null = True
    is_pk = False  # PRIMARY KEY
    sqltype = 'TEXT'  # as a default for the IF's
    if fieldname == 'n_jira':
      is_pk = True  # PRIMARY KEY
    if vtype == str:
      sqltype = 'TEXT'
    elif vtype == int:
      sqltype = 'INTEGER'
    elif vtype == bool:
      sqltype = 'BOOLEAN'
    elif vtype == datetime.date:
      sqltype = 'DATE'
    if is_pk:
      line = f"\t{fieldname} {sqltype} PRIMARY KEY,\n"
    elif not is_null:
      line = f"\t{fieldname} {sqltype} NOT NULL,\n"
    else:
      line = f"\t{fieldname} {sqltype},\n"
    sql_createtable += line
  sql_createtable = sql_createtable.rstrip(' ,\n')
  sql_createtable += '\n)'
  return sql_createtable


def create_table_if_not_exists():
  conn = get_connection()
  cursor = conn.cursor()
  sql = form_sqlcreatetable_str()
  print('create_table_if_not_exists')
  print(sql)
  retval = cursor.execute(sql)
  print('retval', retval)


def adhoctest():
  pass


def process():
  create_table_if_not_exists()


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
