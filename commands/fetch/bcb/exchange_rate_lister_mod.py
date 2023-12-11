#!/usr/bin/env python3
"""
commands/fetch/exchange_rate_lister_mod.py
commands/fetch/batch_exchange_rate_fetcher_mod.py
  calls bcbfetch.BCBCotacaoFetcher (to search for daily BRL/USD BCD cotações) for each date entered as input.

Input is available as:
 => a sole date
 => a date range (days in between two dates)
 => the days in a month (using a refmonthdate as parameter)
 => etc.

import config
import sys
"""
import datetime
import os
import pandas
from prettytable import PrettyTable
import xlsxwriter
import fs.datefs.years_date_functions as dtfs
import fs.datefs.argparse as ap
import fs.economicfs.bcb.bcb_api_finfunctions as apis
import fs.numberfs.tableaufunctions as tblfs
import fs.economicfs.bcb.bcb_cotacao_fetcher_from_db_or_api as bcbfetch  # bcbfetch.BCBCotacaoFetcher


def convert_dates(pdates):
  odates = []
  for pdate in pdates:
    odate = dtfs.returns_date_or_none(pdate)
    odates.append(odate)
  return odates


class Lister:

  excelfilename = 'exchange_rates_test.xlsx'

  def __init__(self, dates):
    self.df = None
    self.ptab = None
    self.dates = dates
    self.cotacao_namedtuplelist = []
    self.process_dates()

  def xlsxwrite_exchangerate_results(self):
    fpath = dtfs.get_appsroot_abspath_for_filename_w_tstamp(self.excelfilename)
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
    for i, dt_exrt_n_dc in enumerate(self.cotacao_namedtuplelist):
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

  def pretty_table_print_exchangerate_results(self):
    """
    apis.namedtuple_bcb_api1(
      'BCBAPI1DataStr',
      [cotacao_compra, cotacao_venda, cotacao_datahora,
       param_date, error_msg, gen_msg, exchanger]
    )
    """
    self.ptab = PrettyTable()
    self.ptab.field_names = [
       'seq', 'cotacao_compra', 'cotacao_venda', 'cotacao_datahora',
       'param_date', 'error_msg', 'gen_msg', 'exchanger'
    ]
    for i, namedtuplelist_cotacao in enumerate(self.cotacao_namedtuplelist):
      nt = namedtuplelist_cotacao
      if not isinstance(nt, apis.namedtuple_bcb_api1):
        continue
      seq = i + 1
      self.ptab.add_row([
         seq, nt.cotacao_compra, nt.cotacao_venda, nt.cotacao_datahora,
         nt.param_date, nt.error_msg, nt.gen_msg, nt.exchanger
      ])
    print(self.ptab)

  def save_html_file(self):
    htmlfilename = 'exchange_rates_test.html'
    fpath = dtfs.get_appsroot_abspath_for_filename_w_tstamp(htmlfilename)
    _, htmlfilename = os.path.split(fpath)
    print('Writing ', htmlfilename)
    text = self.ptab.get_html_string()
    fp = open(fpath, 'w', encoding='utf8')
    fp.write(text)
    fp.close()

  def process_dates(self):
    self.cotacao_namedtuplelist = []
    today = datetime.date.today()
    for pdate in self.dates:
      self.cotacao_namedtuplelist.append(self.cotacao_namedtuplelist)

  def create_df(self):
    tripledictlist = [
      {'compra': nt.cotacao_compra, 'venda': nt.cotacao_venda, 'date': nt.param_date}
      for nt in self.cotacao_namedtuplelist
    ]
    self.df = pandas.DataFrame(tripledictlist)

  def as_df_to_string(self):
    if self.df is None:
      self.create_df()
    print('Cotações:')
    print(self.df.to_string())

  def process(self):
    self.process_dates()
    self.as_df_to_string()
    # self.pretty_table_print_exchangerate_results()


def process_date_n_return_bcbnamedtuple(pdate):
  today = datetime.date.today()
  idate = dtfs.make_date_or_none(pdate)
  if idate is None:
    print('date is None', str(pdate))
    return None
  if idate > today:
    print('date', idate, 'is greater than today ', today)
    print('date', idate, 'is greater than today ', today)
    return None
  print('Instantiating bcbfetch with', pdate)
  fetcher = bcbfetch.BCBCotacaoFetcher(idate)
  namedtuple_cotacao = fetcher.namedtuple_cotacao
  try:
    print(pdate, 'cotação venda =',  namedtuple_cotacao.cotacao_venda, 'ref', namedtuple_cotacao.param_date)
  except AttributeError:
    print('cotacao not found in object.')
  # this is API direct, ie doesn't look up db => bcbnamedtuple = apis.call_api_bcb_cotacao_dolar_on_date(pdate)
  return namedtuple_cotacao


def process_dates(datelist):
  for pdate in datelist:
    process_date_n_return_bcbnamedtuple(pdate)


def process():
  """
  lister = Lister(dispatcher.dates)
  lister.process()
  """
  args = ap.get_args()
  print('Dispatching', args)
  dispatcher = ap.Dispatcher(args)
  dispatcher.func = process_dates
  dispatcher.dispatch()
  datelist = dispatcher.datelist
  print('datelist', datelist)


if __name__ == "__main__":
  process()
