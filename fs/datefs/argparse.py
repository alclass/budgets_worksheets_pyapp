#!/usr/bin/env python3
"""
fs/datesetc/argparse_dates.py
  contains argparse functionality for scripts to import
"""
import argparse
import datetime
import fs.datefs.dategenerators as hilodt
import fs.datefs.datefunctions as dtfs
import fs.datefs.introspect_dates as intr  # intr.introspect_possible_month_position_in_date
import fs.datefs.read_write_datelist_files as rwdt  # .fetch_dates_from_textfile_w_filepath
DEFAULT_TXT_DATES_FILENAME = 'datesfile.txt'


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
    '-i', '--ini', metavar='date', type=str, nargs=1,
    help="dateini in format yyyy-mm-dd for input to the script",
  )
  parser.add_argument(
    '-f', '--fim', metavar='date', type=str, nargs=1,
    help="datefim in format yyyy-mm-dd for input to the script",
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
  parser.add_argument(
    '-fp', '--filepath', metavar='filepath', type=str, nargs=1,
    help="filepath to a dates file (that has dates line by line)",
  )
  parser.add_argument(
    '-fd', '--filedefault', action="store_true",
    help="the default filepath (configured) to a dates file (that has dates line by line)",
  )
  args = parser.parse_args()
  print('args =>', args)
  return args


class Dispatcher:

  def __init__(self, args, func=None):
    self.func = func
    self.args = args
    self.datelist = []
    self.n_rolls = 0
    self.n_funcapply = 0
    self.today = datetime.date.today()

  def treat_func(self):
    if self.func and not callable(self.func):
      error_msg = 'Func (%s) must be callable in Dispatcher' % str(self.func)
      raise RuntimeError(error_msg)
    elif self.func is None:
      self.func = self._roll_dates

  def apply(self):
    """
    error_msg = "Error: Paramenter function 'func' has been given to Dispatch."
    raise ValueError(error_msg)
    """
    # notice that dates may be string and in any one of three formats (ymd | dmy | mdy)
    # so the following function will 'normalize' them all to datetime.date's
    self.datelist = intr.introspect_n_convert_strdatelist_to_dates(self.datelist)
    self.n_funcapply += 1
    return self.func(self.datelist)

  def _roll_dates(self, plist):
    """
    """
    for pdate in plist:
      print('rolling date', pdate, 'Please, rerun with func parameter defined.')
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
      self.datelist = hilodt.gen_daily_dates_for_daterange(dateini, datefim)
      return self.apply()
    if self.args.datelist:
      plist = self.args.datelist
      plist = map(lambda d: dtfs.make_date_or_none(d), plist)
      plist = filter(lambda d: d is not None, plist)
      self.datelist = sorted(filter(lambda d: d <= self.today, plist))
      return self.apply()
    if self.args.refmonthdate:
      refmonthdate = self.args.refmonthdate[0]
      refmonthdate = dtfs.make_refmonthdate_or_none(refmonthdate)
      if refmonthdate is None:
        print("refmonthdate is None ie it's invalid. Returning.")
        return 0
      self.datelist = hilodt.gen_daily_dates_for_refmonth(refmonthdate)
      return self.apply()
    if self.args.date:
      self.datelist = self.args.date  # args.date is already a list
      return self.apply()
    if self.args.today:
      self.datelist = [self.today]  # today, differently from args.date, needs to be enclosed into a list
      return self.apply()
    if self.args.filepath:
      filepath = [self.args.filepath]
      self.datelist = rwdt.fetch_dates_from_strdates_intext_from_filepath_w_sep_n_posorder(filepath)
      return self.apply()
    if self.args.filedefault:
      filepath = rwdt.get_default_datesfilepath()
      self.datelist = rwdt.fetch_dates_from_strdates_intext_from_filepath_w_sep_n_posorder(filepath)
      return self.apply()


def adhoctest():
  filepath = rwdt.get_datesfilepath_from_datafolder_w_filename()
  plist = rwdt.fetch_dates_from_strdates_intext_from_filepath_w_sep_n_posorder(filepath)
  print(plist)


def process():
  """
  """
  args = get_args()
  print('Dispatching', args)
  dispatcher = Dispatcher(args)
  dispatcher.dispatch()


if __name__ == "__main__":
  """
  process()
  """
  adhoctest()
