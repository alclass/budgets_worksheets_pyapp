#!/usr/bin/env python3
"""
commands/fetch/bcb_br/buffer_bcb_apifetch_to_prettyprint.py
  This script writes monthly prettyprint data files with
  exchange rate data from BCB


"""
import os.path
import re
re_patt_exchangerate_datafilename = r"^(?P<yearmonth>\d{4}\-\d{2})\s{1}(?P<currs_num_den_w_uline>[A-Z]{3}_[A-Z]{3}) exchange rates\.txt$"
re_cmpld_exchangerate_datafilename = re.compile(re_patt_exchangerate_datafilename)

class PrettyPrintMonthlyExchangeRatesWriter:
  """
  This class retrieves and writes monthly exchange rates for a pair of currencies

  Example:
    the text file that stores the daily exchange rates for BRL_USD in Jul 2020 is named:
      => '2020-07 BRL_USD exchange rates.txt'
    The lines of this file is organized as:

    seq | date | buyquote | sellquote | obs-if-any

    The buyquote and sellquote are the main ones for the day
      (i.e., they are not the open-quote or close-quote,
      but the PTAC quote as it's defined and published by BCB)
  """

  txtdatafilename = "{yearmonth} {currs_num_den_w_uline} exchange rates.txt"

  def __init__(self, exchratedate, curr_3letter_pair, datafolder=None):
    self.datafolder = datafolder
    self.exchratedate = exchratedate
    self.folderpath = None
    self.curr_num = curr_3letter_pair[0]
    self.curr_den = curr_3letter_pair[1]
    self.filename = None
    self.dailydate_n_quoterec_dict = None

  @property
  def year(self):
    return self.exchratedate.year

  @property
  def yearmonth_datafolder(self):
    # add year
    midpath = os.path.join(self.datafolder, str(year))
    _ympath = os.path.join(midpath, str(month).zfill(2))
    return _ympath

  @property
  def datafilepath(self):
    try:
      return os.path.join(self.yearmonth_datafolder, self.textdata_filename)
    except AttributeError:
      pass
    return None

  @property
  def currs_num_den_w_uline(self):
    return f"{self.curr_num}_{self.curr_den}"

  @property
  def currency_pair(self) -> tuple:
    _curr_pair = (self.curr_num, self.curr_den)
    return _curr_pair

  @property
  def yearmonth(self) -> str | None:
    try:
      _ym = f"{self.exchratedate.year}-{self.exchratedate.month}"
    except AttributeError:
      pass
    return None

  @property
  def textdata_filename(self) -> str:
    return make_name_exchangerate_datafile()

  def get_quoterec_for_date(self, pdate):
    try:
      return self.dailydate_n_quoterec_dict[pdate]
    except KeyError:
      pass
    return None

  def receive_daily_quoterec(self, pdate, quoterec):
    try:
      self.dailydate_n_quoterec_dict[pdate] = quoterec
    except KeyError:
      pass

  @property
  def str_currencies_num_den(self):
    return f"{self.curr_num}/{self.curr_den}"

  def interpol_fileline(self, pdate, quoterec):
    line = f"{pdate} | {self.str_currencies_num_den} | {quoterec.buyprice} \t | {quoterec.buyprice}\n"
    return line

  def write_file_w_text(self, text):
    """
    TODO Recuperates file if it exists previously
    """
    fd = open(self.datafilepath, 'w')
    scrmsg = f"Writing file [{self.datafilepath}]"
    fd.write(text)
    fd.close()

  def finalize_writing_file(self, pdate, quoterec):
    textfile = ''
    try:
      for pdate in self.dailydate_n_quoterec_dict:
        quoterec = self.dailydate_n_quoterec_dict[pdate]
        line = self.interpol_fileline(quoterec)
        textfile += line
      return self.write_file_w_text(text)
    except KeyError:
      pass



    except KeyError:
      pass



  def __str__(self):
    return ''

def make_name_exchangerate_datafile(yearmonth, currency_pair):


def adhoctest1():
  print(re_patt_exchangerate_datafilename)
  yearmonth = '2020-07'
  curr_num = 'BRL'
  curr_den = 'USD'
  currency_pair = (curr_num, curr_den)
  fn = make_name_exchangerate_datafile(yearmonth, currency_pair)
  fn = '2020-07 BRL_USD exchange rates.txt'
  print(fn)
  match = re_cmpld_exchangerate_datafilename.match(fn)
  print(match)


def get_args():
  return None

def process():
  """
  """
  args = get_args()
  print('Dispatching', args)


if __name__ == "__main__":
  adhoctest1()
