#!/usr/bin/env python3
"""
models/budgets/pb/cellformat_workbook_exper.py

https://xlsxwriter.readthedocs.io/format.html
https://www.easyxls.com/manual/tutorials/python/format-excel-cells.html
"""
import xlsxwriter as xw
import os
import lib.db.db_settings as dbs
import settings as sett


class CellFormatExperimenter:

  excelfilename = 'workbook_cellformat_experiment.xlsx'

  def __init__(self):
    self._excelfilepath = None
    self.wrkbk = xw.Workbook(self.excelfilepath)

  @property
  def excelfilepath(self):
    if self._excelfilepath is None:
      datafolderpath = sett.get_datafolder_abspath()
      self._excelfilepath = os.path.join(datafolderpath, self.excelfilename)
    return self._excelfilepath

  def do_cellformat(self):
    print('@do_cellformat()')
    props = {'bold': True, 'font_color': 'red'}
    print('props', props)
    cell_format_o = self.wrkbk.add_format(props)  # Set properties at creation.
    wrksh = self.wrkbk.add_worksheet()
    wrksh.write(0, 0, 'Foo', cell_format_o)
    wrksh.write(1, 0, 'Bar', cell_format_o)
    wrksh.write(2, 0, 3, cell_format_o)
    wrksh.write(3, 0, '', cell_format_o)
    wrksh.set_row(0, 18, cell_format_o)
    wrksh.set_column('A:D', 20, cell_format_o)
    cell_format_o.set_font_color('blue')
    wrksh.write('B1', 'Cell B1', cell_format_o)
    wrkbk2 = xw.Workbook('currency_format.xlsx')
    wrksh = wrkbk2.add_worksheet()
    currency_format = self.wrkbk.add_format({'num_format': '$#,##0.00'})
    wrksh.write('A1', 1234.56, currency_format)
    wrkbk2.close()

  def save_workbook_to_file(self):
    print('Closing', self.excelfilepath)
    self.wrkbk.close()

  def process(self):
    self.do_cellformat()
    self.save_workbook_to_file()


def adhoctest():
  c_o = CellFormatExperimenter()
  c_o.process()


def process():
  pass


if __name__ == '__main__':
  """
  """
  adhoctest()
  process()
