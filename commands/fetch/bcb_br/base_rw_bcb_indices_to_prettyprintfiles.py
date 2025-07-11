#!/usr/bin/env python3
"""
commands/fetch/bcb_br/base_rw_bcb_indices_to_prettyprintfiles.py
  This script writes monthly prettyprint data files with
  exchange rate data from BCB

"""
import argparse
import datetime
import os.path
import prettytable
import re
import settings as sett
import fs.datefs.refmonths_mod as rmd
# import fs.datefs.convert_to_date_wo_intr_sep_posorder as dtfs
import fs.indices.bcb_br.bcb_exchrate_cls as ercls  # for class ercls.ExchangeRate
import commands.db.bcb_br.retrieve_bcbexchangerates_fr_db as bcbretr  # bcbretr.BCBExchangeRatesRetriever
re_patt_exchangerate_datafilename =\
  r"^(?P<yearmonth>\d{4}\-\d{2})\s{1}(?P<currs_num_den_w_uline>[A-Z]{3}_[A-Z]{3}) exchange rates\.txt$"
re_cmpld_exchangerate_datafilename = re.compile(re_patt_exchangerate_datafilename)
tointerpol_exchangerate_datafilename = \
  '{yearmonth} {currnum_currden} exchange rates.txt'
parser = argparse.ArgumentParser(description="Download BLS CPI indices.")
parser.add_argument("--yeardashmonth", type=str, default=datetime.datetime.today(),
                    help="Data Directory")
parser.add_argument("--currnum", type=str, default="BRL",
                    help="currency to")
parser.add_argument("--currden", type=str, default="USD",
                    help="currency from")
args = parser.parse_args()


def make_yearmonth_currnum_currden_exchrate_filename(yearmonthstr, currnum_currden):
  yearmonth_currs_filename = tointerpol_exchangerate_datafilename.format(
    yearmonth=yearmonthstr, currnum_currden=currnum_currden
  )
  return yearmonth_currs_filename


def make_yearmonth_n_currs_exchrate_filename_w_refmonth_n_currpair(refmonthdate, currency_pair):
  year = refmonthdate.year
  month = refmonthdate.month
  yearmonthstr = f"{year:04}-{month:02}"
  currnum, currden = currency_pair
  currnum_currden = f"{currnum}_{currden}"
  return make_yearmonth_currnum_currden_exchrate_filename(yearmonthstr, currnum_currden)


class PrettyPrintMonthlyExchangeRatesRWBase:
  """
  This class retrieves and writes monthly exchange rates for a pair of currencies

  Example:
    the text file that stores the daily exchange rates for BRL_USD in Jul 2020 is named:
      => '2020-07 BRL_USD exchange rates.txt'
    The lines of this file is organized as:

    seq | date | buyquote | sellquote | obs-if-any
      Obs:
        1 - obs-if-any is not yet implemented
        2 - curr_num and curr_den are implicit in the filename (as metadata)

    The buyquote and sellquote are the main ones for the day
      (i.e., they are not the open-quote or close-quote,
      but the PTAC quote as it's defined and published by BCB)
  """

  txtdatafilename = "{yearmonth} {currs_num_den_w_uline} exchange rates.txt"
  DEFAULT_DATA_FOLDERNAME = 'bcb_indices'

  def __init__(
      self,
      curr_3letter_pair: tuple[str, str],
      refmonthdate: datetime.date | str = None,
      dates_quotes_dict: dict[datetime.date: ercls.ExchangeRate] = None,
      datafolderpath: os.path = None,
    ):
    self.is_refmonth_set = False
    self.lineseq = 0
    self.refmonthdate = refmonthdate
    self.datafolderpath = datafolderpath
    self.prettyprint_dump = ''
    self.pp_seq_dt_buyp_sellp_str = prettytable.PrettyTable(
        ['seq', 'date', 'buyprice', 'sellprice']
      )
    self.curr_num = curr_3letter_pair[0]
    self.curr_den = curr_3letter_pair[1]
    self.filename = None
    self.dates_quotes_dict = dates_quotes_dict
    self.treat_attrs()

  def treat_attrs(self):
    if self.datafolderpath is None or not os.path.isdir(self.datafolderpath):
      data_root_folderpath = sett.get_datafolder_abspath()
      self.datafolderpath = os.path.join(data_root_folderpath, self.DEFAULT_DATA_FOLDERNAME)
    return self.treat_dates_quotes_dict()

  def treat_dates_quotes_dict(self):
    if self.dates_quotes_dict is None:
      self.dates_quotes_dict = {}
    try:
      self.dates_quotes_dict = dict(self.dates_quotes_dict)
    except ValueError:
      self.dates_quotes_dict = {}
    self.verify_refmonth_uniformity()

  def set_refmonth(self, pdate):
    if self.is_refmonth_set:
      # refmonth set happens only at the beginning (an init setting)
      return
    self.refmonthdate = rmd.make_refmonth_or_none(pdate)
    if self.refmonthdate is None:
      errmsg = f"Error: refmonthdate is None from date = {pdate}."
      raise ValueError(errmsg)
    self.is_refmonth_set = True
    return

  def verify_refmonth_uniformity(self):
    for pdate in self.dates_quotes_dict:
      if not self.is_refmonth_set:
        self.set_refmonth(pdate)
      if not rmd.is_date_in_refmonth(pdate, self.refmonthdate):
        errmsg = f"""Error: date outside month
        date {pdate} in the exchange rate data is not belonging
          to the expected month {self.refmonthdate}."""
        raise ValueError(errmsg)

  @property
  def year(self):
    return self.refmonthdate.year

  def month(self):
    return self.refmonthdate.month

  @property
  def yearfolderpath(self):
    yearfoldername = f"{self.year} exchange rates"
    yearfolderpath = os.path.join(self.datafolderpath, yearfoldername)
    os.makedirs(yearfolderpath, exist_ok=True)
    return yearfolderpath

  @property
  def datafilepath(self):
    try:
      return os.path.join(self.yearfolderpath, self.yearmonth_textdata_filename)
    except AttributeError:
      pass
    return None

  @property
  def currs_num_den_w_uline(self):
    return f"{self.curr_num}_{self.curr_den}"

  @property
  def curr_num_slash_curr_den(self):
    return f"{self.curr_num}_{self.curr_den}"

  @property
  def currency_pair(self) -> tuple:
    _curr_pair = (self.curr_num, self.curr_den)
    return _curr_pair

  @property
  def yearmonth(self) -> str | None:
    try:
      _ym = f"{self.year}-{self.month}"
    except AttributeError:
      pass
    return None

  @property
  def yearmonth_textdata_filename(self) -> str:
    return make_yearmonth_n_currs_exchrate_filename_w_refmonth_n_currpair(self.refmonthdate, self.currency_pair)

  def get_quoterec_for_date(self, pdate):
    try:
      return self.dates_quotes_dict[pdate]
    except KeyError:
      pass
    return None

  def add_daysprice_to_month(self, exrate: ercls.ExchangeRate):
    try:
      self.dates_quotes_dict.update({exrate.exchratedate: exrate})
    except AttributeError:
      pass

  def receive_daily_quoterec(self, pdate, quoterec):
    try:
      self.dates_quotes_dict[pdate] = quoterec
    except KeyError:
      pass

  def input_w_dict_dates_n_tuple_buy_n_sell(self, pdict):
    for pdate in pdict:
      tuplebuysell = pdict[pdate]
      buyprice, sellprice = tuplebuysell
      exchrate = ercls.ExchangeRate(
        pdate=pdate, curr_num=self.curr_num, curr_den=self.curr_den, buyprice=buyprice, sellprice=sellprice)
      self.dates_quotes_dict.update({pdate: exchrate})

  @property
  def str_currencies_num_den(self):
    return f"{self.curr_num}/{self.curr_den}"

  def process(self):
    self.finalize_writing_file()

  def __str__(self):
    outstr = f"""{self.__class__.__name__}
    {self.curr_num_slash_curr_den}
    """
    return outstr


def adhoctest1():
  print(re_patt_exchangerate_datafilename)
  # yearmonth = '2020-07'
  curr_num = 'BRL'
  curr_den = 'USD'
  refmonthdate = rmd.make_current_refmonthdate()
  currency_pair = (curr_num, curr_den)
  fn = make_yearmonth_n_currs_exchrate_filename_w_refmonth_n_currpair(refmonthdate, currency_pair)
  scrmsg = f"make filename: {refmonthdate} & {currency_pair} => {fn}"
  print(scrmsg)
  match = re_cmpld_exchangerate_datafilename.match(fn)
  result = f"match = {match}"
  print(result)


def get_args():
  yeardashmonth = args.yeardashmonth
  refmonthdate = rmd.make_refmonth_or_none(yeardashmonth)
  currnum = args.currnum
  currden = args.currden
  curr_3letter_pair = (currnum, currden)
  return refmonthdate, curr_3letter_pair


def process():
  """
  """
  refmonthdate, curr_3letter_pair = get_args()
  writer = PrettyPrintMonthlyExchangeRatesRWBase(
    curr_3letter_pair=curr_3letter_pair,
    refmonthdate=refmonthdate
  )
  writer.process()
  retriever = bcbretr.BCBExchangeRatesRetriever(
    date_fr='2023-01-01',
    date_to='2025-01-01',
  )
  pdict = retriever.get_date_n_tupleprices_dict_between_daterange()
  writer.input_w_dict_dates_n_tuple_buy_n_sell(pdict)
  print(writer)


if __name__ == "__main__":
  adhoctest1()
  process()
