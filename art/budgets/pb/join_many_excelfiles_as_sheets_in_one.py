#!/usr/bin/env python3
"""
models/budgets/pb/worksheet_batcher.py

import copy
"""
import os
import pandas as pd
import xlsxwriter
import art.budgets.pb.db_n_file_settings as dbs  # dbs.get_orcdados_batch_output_filepath_w_filename
folderpath = "/home/dados/Sw3/PrdPrjSw/BudgetsWorksheets_PrdPrjSw/dados/orçs_dados/batch_output"


class XlsxJoiner:

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

    For engine compatibility:
      https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html

    openpyxl supports newer Excel file formats.
    calamine supports Excel (.xls, .xlsx, .xlsm, .xlsb) and OpenDocument (.ods) file formats.
    odf supports OpenDocument file formats (.odf, .ods, .odt).
    pyxlsb supports Binary Excel files.
    xlrd supports old-style Excel files (.xls).

    # a different approach not using pandas
    # -------------------------------------
    with open(xlsx_file, 'r', encoding='utf-8') as f:
      reader = xlsxwriter.r.reader(f)
      for r, row in enumerate(reader):
        for c, cell in enumerate(row):
          worksheet.write(r, c, cell)
    """
    pd_fd = pd.ExcelWriter(self.joined_excel_filepath)
    seqs = list(range(1, 73))
    print('Processing n of files', self.size)
    for seq in seqs:
      xlsx_filename = f"{seq:02}.xlsx"
      print(seq, xlsx_filename)
      xlsx_file = os.path.join(folderpath, xlsx_filename)
      print(seq, xlsx_filename)
      df = pd.read_excel(xlsx_file,)  # openpyxl  engine="pyxlsb"
      seqstr = str(seq).zfill(2)
      aba_name = '_' + seqstr
      df.to_excel(pd_fd, sheet_name=aba_name)
    pd_fd.close()


def adhoctest():
  pass


def process():
  joiner = XlsxJoiner()
  joiner.process()


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
