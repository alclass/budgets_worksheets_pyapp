#!/usr/bin/env python3
"""
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


class Dispatcher:

  def __init__(self, args):
    self.args = args
    self.n_rolls = 0
    self.today = datetime.date.today()

  def roll_dates(self, plist):
    """
    """
    for pdate in plist:
      if pdate > self.today:
        print('Cannot process pdate %s is greater than today %s' % (pdate, self.today))
        continue
      self.n_rolls += 1
      print(self.n_rolls, 'Rolling date', pdate)
      fetcher = bcbfetch.BCBCotacaoFetcher(pdate)
      print(fetcher)
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


def process():
  """
  """
  args = get_args()
  print('Dispatching', args)
  dispatcher = Dispatcher(args)
  dispatcher.dispatch()


if __name__ == "__main__":
  process()
