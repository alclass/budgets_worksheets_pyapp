#!/usr/bin/env python3
"""
batch_exchange_rate_fetcher_mod.py
  docstring
"""
import datetime
# import config
import os
import sys
import xlsxwriter
from prettytable import PrettyTable
import fs.datefs.datefunctions as dtfs
import fs.datefs.dategenerators as gendt
import fs.economicfs.apis_finfunctions as apis
import fs.numberfs.tableaufunctions as tblfs
import fs.economicfs.bcb_cotacao_fetcher_from_db_or_api as bcbfetch  #.BCBCotacaoFetcher


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
  """
  apis.namedtuple_bcb_api1(
    'BCBAPI1DataStr',
    [cotacao_compra, cotacao_venda, cotacao_datahora,
     param_date, error_msg, gen_msg, exchanger]
  )
  """
  ptab = PrettyTable()
  ptab.field_names = [
    'cotacao_compra', 'cotacao_venda', 'cotacao_datahora',
     'param_date', 'error_msg', 'gen_msg', 'exchanger'
  ]
  for i, dt_exrt_n_dc in enumerate(dt_exrt_n_dc_exchangerates):
    nt = dt_exrt_n_dc
    if not isinstance(nt, apis.namedtuple_bcb_api1):
      continue
    seq = i + 1
    ptab.add_row([
      nt.cotacao_compra, nt.cotacao_venda, nt.cotacao_datahora,
       nt.param_date, nt.error_msg, nt.gen_msg, nt.exchanger
    ])
  print(ptab)
  htmlfilename = 'exchange_rates_test.html'
  fpath = dtfs.get_appsroot_abspath_for_filename_w_tstamp(htmlfilename)
  _, htmlfilename = os.path.split(fpath)
  print('Writing ', htmlfilename)
  text = ptab.get_html_string()
  fp = open(fpath, 'w', encoding='utf8')
  fp.write(text)
  fp.close()


def process_some_dates(pdates):
  results = []
  # strdate = '2016-12-12'
  # pdate = dtfs.returns_date_or_today(strdate)
  # dateadhoctests.append(pdate)
  # dateadhoctests.append(pdate)
  today = datetime.date.today()
  for pdate in pdates:
    idate = dtfs.make_date_or_none(pdate)
    if idate is None:
      print('date is None', str(pdate))
      continue
    if idate > today:
      print('date', idate, 'is greater than today ', today)
      continue
    fetcher = bcbfetch.BCBCotacaoFetcher(idate)
    namedtuple_cotacao = fetcher.namedtuple_cotacao
    if not isinstance(namedtuple_cotacao, apis.namedtuple_bcb_api1):
      print('namedtuple_cotacao is not type apis.namedtuple_bcb_api1')
      print(fetcher)
      continue
    # dt_exrt_n_dc = apis.call_api_bcb_cotacao_dolar_on_date(pdate)
    results.append(namedtuple_cotacao)
  # pretty_table_print_exchangerate_results(results)
  # xlsxwrite_exchangerate_results(results)
  return results


def get_args():
  pdates = []
  for arg in sys.argv[1:]:
    pdate = arg
    pdates.append(pdate)
  return pdates


def convert_dates(pdates):
  odates = []
  for pdate in pdates:
    odate = dtfs.returns_date_or_none(pdate)
    odates.append(odate)
  return odates


def process():
  clidates = get_args()
  if len(clidates) == 0:
    refmonthdate = '2023-10-01'
    pdates = gendt.get_list_gen_daily_dates_for_refmonth(refmonthdate)
  else:
    pdates = convert_dates(clidates)
  print(pdates)
  results = process_some_dates(pdates)
  pretty_table_print_exchangerate_results(results)


if __name__ == "__main__":
  process()
