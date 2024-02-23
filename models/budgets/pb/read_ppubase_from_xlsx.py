#!/usr/bin/env python3
"""
models/budgets/pb/read_ppubase_from_xlsx.py
"""
import os.path
import sqlite3
import time
import pandas as pd
import models.budgets.pb.create_tables_ppubase_n_pricebank as ct  # ct.get_orcdados_folderpath
ppubase_filename = 'PPU base.xlsx'
PPUBASE_TABLENAME = ct.PPUBASE_TABLENAME
PRICEBANK_TABLENAME = ct.PRICEBANK_TABLENAME


def get_xlsx_ppubase_filepath():
  folderpath = ct.get_orcdados_folderpath()
  xlsx_filepath = os.path.join(folderpath, ppubase_filename)
  return xlsx_filepath


def get_df_from_xlsx_ppubase():
  ppubase_filepath = get_xlsx_ppubase_filepath()
  df = pd.read_excel(ppubase_filepath)
  return df


class Insertor:

  ppubase_tablename = PPUBASE_TABLENAME
  pricebank_tablename = PRICEBANK_TABLENAME
  columnnames = [
    'seq', 'ncmcode', 'ipi', 'familycode', 'nmcode', 'partnumber',
    'manufacturer_sname', 'textobreve', 'description', 'qty', 'meas_unit'
  ]  # 11 fieldnames

  def __init__(self):
    self.conn = None
    self.cursor = None
    self.n_inserted = 0
    self.seq = 0
    self.df = get_df_from_xlsx_ppubase()
    self.reset_column_names()

  @property
  def size(self):
    if self.df:
      return self.df.shape[1]
    return 0

  def open_db_connection(self):
    ct.create_tables_if_not_exists()
    filepath = ct.get_orcdados_sqlitefilepath()
    print(f'Opening db connection @ [{filepath}]')
    self.conn = sqlite3.connect(filepath)
    self.conn.row_factory = sqlite3.Row
    self.cursor = self.conn.cursor()

  def close_db_connection(self):
    print('Closing db connection.')
    self.cursor.close()
    self.conn.close()

  def reset_column_names(self):
    """
    Seq	NCM	%IPI	 família 	NM	part-number	fabricante
      Texto Breve	  Descrição	qtd	tipo-unidade
    """
    self.df.columns = self.columnnames

  def make_row_dict(self, series):
    rowdict = {}
    for col in self.columnnames:
      rowdict[col] = eval(f'series["{col}"]')
    return rowdict

  def mount_fieldnames_part_of_sqlinsert(self, series):
    fieldnames_sql = '('
    for col in self.columnnames:
      fieldnames_sql += f'`{col}`, '
    # add created_at field at the end
    fieldnames_sql += '`created_at`)'
    return fieldnames_sql

  def mount_questionmark_part_of_sqlinsert(self):
    n_questionmarks = len(self.columnnames)
    # add created_at field at the end
    n_questionmarks += 1
    questionmarks_part = '?, ' * n_questionmarks
    questionmarks_part = questionmarks_part.rstrip(', ')
    questionmarks_part = f"({questionmarks_part})"
    return questionmarks_part

  def mount_sqlinsert(self, series):
    fieldnames_sql = self.mount_fieldnames_part_of_sqlinsert(series)
    questionmarks_part = self.mount_questionmark_part_of_sqlinsert()
    sql = f"""INSERT OR IGNORE into `{self.ppubase_tablename}`
        {fieldnames_sql} VALUES {questionmarks_part};"""
    return sql

  def get_tuple_from_series(self, series):
    alist = []
    for col in self.columnnames:
      value = eval(f'series["{col}"]')
      alist.append(value)
    dtime = time.time()
    alist.append(dtime)
    return tuple(alist)

  def db_row_insert(self, series):
    tuplevalues = self.get_tuple_from_series(series)
    sql = self.mount_sqlinsert(series)
    self.seq += 1
    print(sql)
    retval = self.cursor.execute(sql, tuplevalues)
    if retval:
      self.n_inserted += 1
      print('Inserted', self.n_inserted)

  def insert_rows_from_df_into_db(self):
    self.open_db_connection()
    for row in self.df.iterrows():
      series = row[1]
      self.db_row_insert(series)
    if self.n_inserted > 0:
      print(f'Committing db with {self.n_inserted} inserted rows.')
      self.conn.commit()
    self.close_db_connection()

  def process(self):
    self.insert_rows_from_df_into_db()


def adhoctest():
  pass


def process():
  inso = Insertor()
  inso.process()


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
