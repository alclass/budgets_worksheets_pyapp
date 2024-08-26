#!/usr/bin/env python3
"""
commands/fetch/bcb/batch_exchange_rate_fetcher_mod.py
  calls bcbfetch.BCBCotacaoFetcher (to search for daily BRL/USD BCD cotações)
  for each date entered as input.

Input is available as:
 => a sole date
 => a date range (days in between two dates)
 => the days in a month (using a refmonthdate as parameter)
 => etc.

import config
import sys
"""
import argparse
import collections
import datetime
from dateutil.relativedelta import relativedelta
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import fs.datefs.refmonths_mod as rfm
import fs.datefs.dategenerators as gendt
import fs.economicfs.bcb.bcb_cotacao_fetcher_from_db_or_api as bcbf  # bcbfetch.BCBCotacaoFetcher


def convert_dates(pdates):
  odates = []
  for pdate in pdates:
    odate = cnv.make_date_or_none(pdate)
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
  """
  field_names = [date, today, refmonthdate, datelist, daterange]
  * today is boolean, all others are list
  args = Namespace(date=None, today=False, refmonthdate=None, datelist=None, daterange=None)

  Obs:
    None is equivalent to False (and vice versa)
  """

  arg_fieldnames = ['date', 'today', 'refmonthdate', 'datelist', 'daterange']
  nt_args_fallback = collections.namedtuple(
    'NTArgs', field_names=arg_fieldnames
  )

  def __init__(self, args=None):
    self.func = None
    self.args = args
    self.n_rolls = 0
    self.n_funcapply = 0
    self.today = datetime.date.today()

  def are_args_empty(self):
    """
    asdict = self.args._asdict()
    """
    if self.args is None:
      return False
    for fieldname in self.arg_fieldnames:
      arg = eval('self.args.'+fieldname)
      if arg is None:
        return True
    return False

  def apply(self, plist):
    """
    error_msg = "Error: Paramenter function 'func' has been given to Dispatch."
    raise ValueError(error_msg)
    """
    self.n_funcapply += 1
    if self.func is not None:
      return self.func(plist)
    # default
    func = self._roll_dates
    return func(plist)

  def _roll_dates(self, plist):
    """
    """
    for pdate in plist:
      if pdate > self.today:
        print('Cannot process pdate %s is greater than today %s' % (pdate, self.today))
        continue
      self.n_rolls += 1
      print(self.n_rolls, 'Rolling date', pdate)
      fetcher = bcbf.BCBCotacaoFetcher(pdate)
      print(fetcher)
    return self.n_rolls

  def dispatch(self):
    if self.args.daterange:
      dateini = cnv.make_date_or_none(self.args.daterange[0])
      datefim = cnv.make_date_or_none(self.args.daterange[1])
      if dateini is None or datefim is None:
        print('dateini is None or datefim is None. Returning.')
        return 0
      if dateini > self.today:
        return 0
      if datefim > self.today:
        datefim = self.today
      plist = gendt.gen_dailydates_or_empty_bw_ini_fim_opt_order(dateini, datefim)
      return self.apply(plist)
    if self.args.datelist:
      plist = self.args.datelist
      plist = map(lambda d: cnv.make_date_or_none(d), plist)
      plist = filter(lambda d: d is not None, plist)
      plist = sorted(filter(lambda d: d <= self.today, plist))
      return self.apply(plist)
    if self.args.refmonthdate:
      refmonthdate = self.args.refmonthdate[0]
      refmonthdate = rfm.make_refmonthdate_or_none(refmonthdate)
      if refmonthdate is None:
        print("refmonthdate is None ie it's invalid. Returning.")
        return 0
      plist = gendt.gen_dailydates_for_refmonth_or_empty_opt_order_coff_accfut(refmonthdate)
      return self.apply(plist)
    if self.args.date:
      pdate = self.args.date
      plist = [pdate]
      return self.apply(plist)
    if self.args.topdate:
      plist = [self.today]
      return self.apply(plist)


def process():
  """
  limit_hour = datetime.datetime(now.year, now. month, now. day, 16)
  if now > limit_hour:

  """
  args = get_args()
  print('Dispatching', args)
  dispatcher = Dispatcher(args)
  if dispatcher.are_args_empty():
    today = datetime.date.today()
    yesterday = datetime.date.today() - relativedelta(days=1)
    date_1wb_yesterday = yesterday - relativedelta(days=7)
    daterange = [date_1wb_yesterday, today]
    # daterange = gendt.get_gendailydates_for_lastweek_incl_today_opt_order()
    scrmsg = f"""
    CLI args were empty.
    Adding to args daterange [with dates thru lastweek] = f{daterange}"""
    print(scrmsg)
    dispatcher.args.daterange = daterange
  dispatcher.dispatch()
  print('daterange', dispatcher.args.daterange)


if __name__ == "__main__":
  process()
