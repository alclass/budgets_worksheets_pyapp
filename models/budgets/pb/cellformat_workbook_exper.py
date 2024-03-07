#!/usr/bin/env python3
"""
models/budgets/pb/cellformat_workbook_exper.py

https://xlsxwriter.readthedocs.io/format.html
https://www.easyxls.com/manual/tutorials/python/format-excel-cells.html
"""
import xlsxwriter as xw
import os
import fs.db.db_settings as dbs
import settings as sett


class CellFormatExperimenter:

  def __init__(self):
    self.wrkbk = xw.Workbook()

  def do_cellformat(self):
    print('@do_cellformat()')
    props = {'bold': True, 'font_color': 'red'}
    cell_format_o = self.wrkbk.add_format(props)  # Set properties at creation.
    wrksh = self.wrkbk.add_worksheet()
    wrksh.write(0, 0, 'Foo', cell_format_o)
    wrksh.write(1, 0, 'Bar', cell_format_o)
    wrksh.write(2, 0, 3, cell_format_o)
    wrksh.write(3, 0, '', cell_format_o)
    wrksh.set_row(0, 18, cell_format_o)
    wrksh.set_column('A:D', 20, cell_format_o)
    cell_format_o.set_font_color('green')
    wrksh.write('B1', 'Cell B1', cell_format_o)
    wrkbk2 = xw.Workbook('currency_format.xlsx')
    wrksh = wrkbk2.add_worksheet()
    currency_format = self.wrkbk.add_format({'num_format': '$#,##0.00'})
    wrksh.write('A1', 1234.56, currency_format)
    wrkbk2.close()

  def save_workbook_to_file(self):
    filename = 'workbook_cellformat_experiment.xlsx'
    datafolderpath = sett.get_datafolder_abspath()
    filepath = os.path.join(datafolderpath, filename)
    self.wrkbk.w


def adhoctest():
  do_cellformat()


def process():
  pass


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
