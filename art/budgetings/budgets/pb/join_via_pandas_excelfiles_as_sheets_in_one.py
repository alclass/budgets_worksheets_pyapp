#!/usr/bin/env python3
"""
models/budgets/pb/worksheet_batcher.py

import copy
"""
import os.path

import xlsxwriter
import pandas as pd
import art.budgetings.budgets.pb.db_n_file_settings as dbs  # dbs.get_orcdados_batch_output_filepath_w_filename
folderpath = "/home/dados/Sw3/PrdPrjSw/BudgetsWorksheets_PrdPrjSw/dados/orçs_dados/batch_output"


class XlsxJoinerViaPandas:

  def __init__(self):
    self.workbook = xlsxwriter.Workbook('joined_workbook.xlsx')
    self.input_excel_files = dbs.get_xlsxfilepaths_from_batch_output_folder()
    filename = 'z-joined.xlsx'
    self.joined_excel_filepath = dbs.get_orcdados_batch_output_filepath_w_filename(filename)
    self.workbook = xlsxwriter.Workbook(self.joined_excel_filepath)

  @property
  def size(self):
    return len(self.input_excel_files)

  def process(self):
    """
    worksheet = workbook.add_worksheet(sh)
    worksheet.write(1,1,"abcd")
    workbook.close()

      with open(sh, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
          for c, col in enumerate(row):
            self.worksheet.write(r, c, col)
    """
    seqs = list(range(1, 73))
    print('Processing n of files', self.size)
    for seq in seqs:
      txt_filename = f"{seq:02}.txt"
      print(seq, txt_filename)
      txt_file = os.path.join(folderpath, txt_filename)
      xlsx_filename = f"{seq:02}.xlsx"
      xlsx_file = os.path.join(folderpath, xlsx_filename)
      if not os.path.isfile(txt_file):
        print('Filename', txt_filename, 'does not exist. Continuing')
        continue
      if os.path.isfile(xlsx_file):
        print('Filename', xlsx_filename, 'already exists. Continuing')
        continue
      pd_rw_o = pd.read_csv(txt_file, sep=';')
      print('Saving from', txt_filename, 'to', xlsx_file)
      pd_rw_o.to_excel(xlsx_file)


def adhoctest():
  pass


def process():
  joiner = XlsxJoinerViaPandas()
  joiner.process()


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
