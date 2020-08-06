#!/usr/bin/env python3
"""
  docstring
"""
import os
import xlsxwriter
from prettytable import PrettyTable
import fs.datefs.datefunctions as dtfs
import fs.economicfs.apis_finfunctions as apis
import fs.numberfs.tableaufunctions as tblfs


def xlsxwrite_exchangerate_results(dt_exrt_n_dc_exchangerates):
  fpath = dtfs.get_appsroot_abspath_for_filename_w_tstamp('exchange_rates_test.xlsx')
  workbook = xlsxwriter.Workbook(fpath)
  worksheet = workbook.add_worksheet()
  cellref = 'B4'
  worksheet.write(cellref, 'Seq')
  cellref = tblfs.move_cell_along_columns(cellref, 1)
  worksheet.write(cellref, 'Data')
  cellref = tblfs.move_cell_along_columns(cellref, 1)
  worksheet.write(cellref, 'valor câmbio')
  cellref = tblfs.move_cell_along_columns(cellref, 1)
  worksheet.write(cellref, 'data câmbio')
  cellref = tblfs.move_cell_along_tableau(cellref, -3, 1)
  for i, dt_exrt_n_dc in enumerate(dt_exrt_n_dc_exchangerates):
    pdate, exchange_rate, data_cotacao = dt_exrt_n_dc
    seq = i + 1
    worksheet.write(cellref, seq)
    cellref = tblfs.move_cell_along_columns(cellref, 1)
    worksheet.write(cellref, pdate)
    cellref = tblfs.move_cell_along_columns(cellref, 1)
    worksheet.write(cellref, exchange_rate)
    cellref = tblfs.move_cell_along_columns(cellref, 1)
    worksheet.write(cellref, data_cotacao)
    cellref = tblfs.move_cell_along_tableau(cellref, -3, 1)
  workbook.close()


def pretty_table_print_exchangerate_results(dt_exrt_n_dc_exchangerates):
  ptab = PrettyTable()
  ptab.field_names = ['Seq', 'Data', 'valor câmbio', 'data câmbio']
  for i, dt_exrt_n_dc in enumerate(dt_exrt_n_dc_exchangerates):
    pdate, exchange_rate, data_cotacao = dt_exrt_n_dc
    seq = i + 1
    ptab.add_row([seq, pdate, exchange_rate, data_cotacao])
  print(ptab)
  htmlfilename = 'exchange_rates_test.html'
  fpath = dtfs.get_appsroot_abspath_for_filename_w_tstamp(htmlfilename)
  _, htmlfilename = os.path.split(fpath)
  print('Writing ', htmlfilename)
  text = ptab.get_html_string()
  fp = open(fpath, 'w', encoding='utf8')
  fp.write(text)
  fp.close()


def process_some_dates():
  dates = []
  results = []
  strdate = '2016-12-12'
  pdate = dtfs.returns_date_or_today(strdate)
  dates.append(pdate)
  pdate = dtfs.returns_date_or_today()
  dates.append(pdate)
  for pdate in dates:
    dt_exrt_n_dc = apis.call_api_bcb_cotacao_dolar_on_date(pdate)
    results.append(dt_exrt_n_dc)
  pretty_table_print_exchangerate_results(results)
  xlsxwrite_exchangerate_results(results)


def process():
  process_some_dates()


if __name__ == "__main__":
  process()
