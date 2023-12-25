#!/usr/bin/env python3
"""
commands/db/bcb/insert_exchangerates_into_db.py

from dateutil. relativedelta import relativedelta
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import settings as sett
"""
import argparse
import datetime
import fs.economicfs.bcb.bcb_cotacao_fetcher_from_db_or_api as fin
import fs.datefs.dategenerators as gendt
import fs.datefs.read_write_datelist_files as rwdt


def fetch_exchangerate_thru_api(pdate):
  bcb = fin.BCBCotacaoFetcher(pdate)
  bcb_api_nt = bcb.pop_dates_n_try_find_cotacao()
  return bcb_api_nt


def get_args_via_argparse():
  """
  https://realpython.com/command-line-interfaces-python-argparse/
  One Example:
    parser.add_argument("--veggies", nargs="+")
    parser.add_argument("--fruits", nargs="*")
      $ python cooking.py --veggies pepper tomato --fruits apple banana
    parser.add_argument("--size", choices=["S", "M", "L", "XL"], default="M")
    my_parser.add_argument("--weekday", type=int, choices=range(1, 8))
  """
  parser = argparse.ArgumentParser(description="Obtain Arguments")
  parser.add_argument(
    '-y', '--year', metavar='year', type=int, nargs=1,
    help="the year for getting its daily exchange rate quotes",
  )
  parser.add_argument(
    '-m', '--month', metavar='yearmonth', type=str, nargs=1,
    help="the year dash month for getting its daily exchange rate quotes",
  )
  parser.add_argument(
    '-d', '--day', metavar='yearmonthday', type=str, nargs=1,
    help="the date for finding its daily exchange rate quotes",
  )
  parser.add_argument(
    '-dl', '--datelist', metavar='datelist', type=str, nargs='+',
    help="datelist for finding daily exchange rate quotes one by one",
  )
  parser.add_argument(
    '-cy', '--current-year', action='store_true',
    help="current year for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-yr', '--yearrange', type=int, nargs=2,
    help="year range (ini, fim) as the date range for finding daily exchange rate quotes",
  )
  parser.add_argument(
    '-rdf', '--readdatefile', action='store_true',
    help="marker/signal for inputting the dateadhoctests from "
         "the conventioned datefile located in the app's data folder",
  )
  parser.add_argument(
    '-cp', '--currencypair', type=str, nargs=1, default='brl/usd',
    help="for specifying the currency pair ratio that corresponds to the output quotes (default 'brl/usd')",
  )
  args = parser.parse_args()
  return args


class ArgDispatcher:
  def __init__(self, argnamedtuple=None, func=None):
    self.today = datetime.date.today()
    self.func = func or fetch_exchangerate_thru_api
    self.seq = 0
    self.bcbs = []
    self.year = None
    self.month = None
    self.day = None
    self.datelist = None
    self.current_year = False
    self.yearrange = None
    self.readdatefile = False
    self.currencypair = 'brl/usd'
    self.treat_attrs(argnamedtuple)

  @property
  def attrs(self):
    _attrs = [
      fie_n_val for fie_n_val in self.__dict__.items()
      if not callable(fie_n_val[0])
    ]
    return _attrs

  def treat_attrs(self, argnamedtuple):
    """
      self.year = argnamedtuple.year
      self.month = argnamedtuple.month
      self.day = argnamedtuple.day
      self.datelist = None
      self.current_year = False
      self.yearrange = None
      self.readdatefile = False
      self.currencypair = 'brl/usd'
      self.treat_attrs(argnamedtuple)
    """
    _ = argnamedtuple  # just for the IDE for it's used inside the exec() function below
    for attr in self.attrs:
      field, _ = attr
      _ = field
      try:
        pyline = 'self.{field} = argnamedtuple.{field}'.format(field=field)
        exec(pyline)
      except AttributeError:
        pass

  def dispatch(self):
    self.seq += 1
    an_option_actioned = False
    if self.day:
      an_option_actioned = True
      y, m, d = self.today.year, self.today.month, int(self.day)
      pdate = datetime.date(year=y, month=m, day=d)
      bcb = self.func(pdate)
      print(self.seq, bcb)
      self.bcbs.append(bcb)
    if self.month:
      an_option_actioned = True
      y, m = self.today.year, int(self.month)
      refmonthdate = datetime.date(year=y, month=m, day=1)
      for pdate in gendt.gen_dailydates_for_refmonth_or_empty_opt_order_coff_accfut(refmonthdate):
        bcb = self.func(pdate)
        print(self.seq, bcb)
        self.bcbs.append(bcb)
    self.datelist = rwdt.convert_strdatelist_to_datelist_wo_sep_n_posorder(self.datelist)
    if self.datelist:
      for pdate in self.datelist:
        bcb = self.func(pdate)
        print(self.seq, bcb)
        self.bcbs.append(bcb)
    if self.current_year:
      an_option_actioned = True
      for pdate in gendt.gen_dailydates_for_current_year_opt_order_coff_accfut():
        bcb = self.func(pdate)
        print(self.seq, bcb)
        self.bcbs.append(bcb)
    if self.yearrange and isinstance(self.yearrange, list):
      yearini, yearfim = tuple(self.yearrange)
      for pdate in gendt.gen_dailydates_f_yearini_t_today_or_empty_opt_order(yearini, yearfim):
        an_option_actioned = True
        bcb = self.func(pdate)
        print(self.seq, bcb)
        self.bcbs.append(bcb)
    if an_option_actioned:
      return True
    # default fallback
    today = datetime.date.today()
    print('default fallback', today)
    bcb = self.func(today)
    print(self.seq, bcb)
    self.bcbs.append(bcb)
    return True

  def adhoctest(self):
    print('In adhoctest() yearrange =', self.yearrange)
    if self.yearrange and isinstance(self.yearrange, list):
      yearini, yearfim = tuple(self.yearrange)
      for pdate in gendt.gen_dailydates_f_yearini_t_today_or_empty_opt_order(yearini, yearfim):
          print(pdate)

  def __str__(self):
    outstr = '<ArgDispatcher\n'
    for fie_n_val in self.attrs:
      field, value = fie_n_val
      line = '\t{field} = "{value}"\n'.format(field=field, value=value)
      outstr += line
    outstr += '/>\n'
    return outstr


def adhoctest():
  """
  pastdate = '2020-10-15'
  pdate = datetime.date.today()
  pdate = pdate - relativedelta(days=1)
  # pydate = datetime.date(2020, 10, 15)
  """
  pdate = datetime.date(2023, 10, 14)
  bcb_api_nt = fetch_exchangerate_thru_api(pdate)
  print(pdate, bcb_api_nt)
  if bcb_api_nt is not None:
    print(bcb_api_nt.cotacao_venda)


def adhoctest2():
  """
  args = get_args_via_argparse()
  print(args)
  o.current_year = True
  o.dispatch()
  for year in range(2022, 2023+1):
    print(year)

  yearini, yearfim = args.yearrange
  print('yearini, yearfim = ', yearini, yearfim
  """
  args = get_args_via_argparse()
  print(args)
  o = ArgDispatcher(args)
  o.dispatch()


def process():
  pass


if __name__ == '__main__':
  """
  process()
  """
  adhoctest2()
