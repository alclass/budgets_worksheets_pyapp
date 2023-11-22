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
import argparse
import datetime
import os
import pandas
from prettytable import PrettyTable
import xlsxwriter
import fs.datefs.datefunctions as dtfs
import fs.datefs.dategenerators as gendt
import fs.economicfs.apis_finfunctions as apis
import fs.numberfs.tableaufunctions as tblfs
import fs.economicfs.bcb_cotacao_fetcher_from_db_or_api as bcbfetch  # bcbfetch.BCBCotacaoFetcher


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
      self.cotacao_namedtuplelist.append(namedtuple_cotacao)

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


class Dispatcher:

  def __init__(self, args):
    self.args = args
    self.n_rolls = 0
    self.today = datetime.date.today()
    self.dates = []

  def roll_dates(self, plist):
    """
    """
    for pdate in plist:
      if pdate > self.today:
        print('Cannot process pdate %s is greater than today %s' % (pdate, self.today))
        continue
      self.n_rolls += 1
      print(self.n_rolls, 'Rolling date', pdate)
      self.dates.append(pdate)
    return self.n_rolls

  def dispatch(self):
    if self.args.daterange:
      dateini = dtfs.make_date_or_none(self.args.daterange[0])
      datefim = dtfs.make_date_or_none(self.args.daterange[1])
      if dateini is None or datefim is None:
        print('dateini is None or datefim is None. Returning.')
        return 0
      if dateini > self.today:
        return 0
      if datefim > self.today:
        datefim = self.today
      plist = gendt.gen_daily_dates_for_daterange(dateini, datefim)
      return self.roll_dates(plist)
    if self.args.datelist:
      plist = self.args.datelist
      plist = map(lambda d: dtfs.make_date_or_none(d), plist)
      plist = filter(lambda d: d is not None, plist)
      plist = sorted(filter(lambda d: d <= self.today, plist))
      return self.roll_dates(plist)
    if self.args.refmonthdate:
      refmonthdate = self.args.refmonthdate[0]
      refmonthdate = dtfs.make_refmonthdate_or_none(refmonthdate)
      if refmonthdate is None:
        print("refmonthdate is None ie it's invalid. Returning.")
        return 0
      plist = gendt.gen_daily_dates_for_refmonth(refmonthdate)
      return self.roll_dates(plist)
    if self.args.date:
      pdate = self.args.date
      plist = [pdate]
      return self.roll_dates(plist)
    if self.args.today:
      plist = [self.today]
      return self.roll_dates(plist)


def get_args():
  """
  pdates = []
  for arg in sys.argv[1:]:
    pdate = arg
    pdates.append(pdate)
  return pdates

  """
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '-d', '--date', metavar='date', type=str, nargs=1,
    help="a date in format yyyy-mm-dd for input to the script",
  )
  parser.add_argument(
    '-t', '--today', action="store_true",
    help="a date in format yyyy-mm-dd for input to the script",
  )
  parser.add_argument(
    '-rmd', '--refmonthdate', metavar='refmonthdate', type=str, nargs=1,
    help="a refmonthdate in format yyyy-mm for input to the script",
  )
  parser.add_argument(
    '-dl', '--datelist', metavar='datelist', type=str, nargs='+',
    help="a datelist each one in format yyyy-mm-dd separated by a space (gap/blank) for input to the script",
  )
  parser.add_argument(
    '-dr', '--daterange', metavar='daterange', type=str, nargs=2,
    help="a daterange has two dates, each in format yyyy-mm-dd, "
         "and represents all days in-between dateini and datefim for input to the script",
  )
  args = parser.parse_args()
  print('args =>', args)
  return args


def process():
  """
  """
  args = get_args()
  print('Dispatching', args)
  dispatcher = Dispatcher(args)
  dispatcher.dispatch()
  lister = Lister(dispatcher.dates)
  lister.process()


if __name__ == "__main__":
  process()
