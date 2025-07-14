#!/usr/bin/env python3
"""
models/budgets/pb/recreate_xls_from_df_from_db.py
  Reads data from db, translate them to a pandas DataFrame, writes them to a xls file.
"""
import sqlite3
import pandas as pd
import art.bcb_br.fetch.models.budgets.pb.db_n_file_settings as dbs  # for dbs.get_orcdados_folderpath


class PPUBaseXlsWriter:

  columnnames = dbs.PPUBASE_COLUMNNAMES

  def __init__(self):
    self.n_rows = 0
    self.seq_n_record_tabledict = {}
    self.df = None
    self.tablename = dbs.PPUBASE_TABLENAME
    self.process()

  @property
  def size(self):
    return len(self.seq_n_record_tabledict)

  def extract_field_n_value_dict_from_row(self, row):
    field_n_value_rowdict = {}
    for fieldname in self.columnnames:
      value = row[fieldname]
      field_n_value_rowdict[fieldname] = value
    seq = field_n_value_rowdict['seq']
    self.seq_n_record_tabledict[seq] = field_n_value_rowdict

  def dbfetch(self):
    self.n_rows = 0
    sql = f"""SELECT * FROM {self.tablename} ORDER BY seq;"""
    conn = dbs.get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    fetch_o = cursor.execute(sql)
    if fetch_o:
      for row in fetch_o.fetchall():
        self.extract_field_n_value_dict_from_row(row)

  def transpose_db_to_df(self):
    """
    Transposes the instance's data dict to pandas DataFrame

    self.df = pd.DataFrame(self.seq_n_record_tabledict, columns=)
    for seq in self.seq_n_record_tabledict:
      rowdict = self.seq_n_record_tabledict[seq]
      self.df += f"{rowdict}\n"
    """
    self.df = pd.DataFrame.from_dict(
      self.seq_n_record_tabledict, orient='index', dtype=None, columns=self.columnnames
    )
    self.df = self.df.dropna()

  def save_df_to_excel(self):
    dbs.save_xlsx_ppubase_from_dataframe(self.df)

  def process(self):
    self.dbfetch()
    self.transpose_db_to_df()
    self.save_df_to_excel()
    print(self)

  def print_asdict(self):
    outstr = f"{self.__class__.__name__} size={self.size}\n"
    for seq in self.seq_n_record_tabledict:
      rowdict = self.seq_n_record_tabledict[seq]
      outstr += f"{rowdict}\n"
    return outstr

  def __str__(self):
    return self.df.to_string()


def adhoctest():
  pass


def process():
  PPUBaseXlsWriter()


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
