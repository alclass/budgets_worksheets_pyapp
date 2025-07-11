#!/usr/bin/env python3
"""
commands/fetch/bcb_br/bcb_rw_clss/base_rw_bcb_indices_to_prettyprintfiles.py
  This script contains 'base' class:
    PrettyPrintMonthlyExchangeRatesRWBase
  that forms a basis for
    a) a data prettyprint file reader subclass and
    b) its counterpart writer subclass

Because this base class has common functionality for both the reader and writer subclasses,
  let's take a look at 'Some info on the data file contents'

Some info on the data file contents
===================================

Theses prettyprint data files have the following information:

  a) in the filename (as metadata):
     {year_dash_month} and {the_currency_pair_backslashed_str}
  b) through the line contents:
     daysdate, buyprice, sellprice
     (field 'seqnumber' is virtual, an ordinal sequence 1, 2, 3... derived dynamicly)

So, all fields for a refmonth day's exchange rate data set are:
  1 - an ordinal sequence number (virtual or dynamicly generated)
  2 - day's date (each file is monthly, i.e., their quotes belong to a refmonthdate {year and month})
      currencies (a pair: numerator is 'to', denominator is 'from')
  3 - curr_fr (or curr_den)
  4 - curr_to (or curr_num)
      at least a buy price and a sell price
  5 - buyprice
  6 - sellprice
    (these are BCB's PTAC which is a kind of mean price during the day, not the open or close values)
    (currency-unit of measure for prices are determined by curr_to which is also curr_num (numerator))
    (at the time of writing, price are str-represention of floats)

An Alternative (not used here) for the float-typed prices:
    a second strategy would be to have them as integer with a second field telling the 10-raised-to-n divider
    For example of a price with 2 fields:
    a)
      integer field: 54321
      divisor field: 10^4 (or 10000)
        which results 54321/10000=5.4321
    b)
      integer field: 5432174
      divisor field: 10^6 (or 1000000)
        which results 5432174/1000000=5.432174

@see also how this data set is stored in SqliteDB (or any other RDBMS if available)
"""
import argparse
import datetime
import os.path
import prettytable
import re
import settings as sett
import fs.datefs.refmonths_mod as rmd
import fs.datefs.convert_to_date_wo_intr_sep_posorder as dtfs
# import fs.datefs.convert_to_date_wo_intr_sep_posorder as dtfs
import fs.indices.bcb_br.bcb_exchrate_cls as ercls  # for class ercls.ExchangeRate
import commands.db.bcb_br.retrieve_bcbexchangerates_fr_db as bcbretr  # bcbretr.BCBExchangeRatesRetriever
re_patt_exchangerate_datafilename =\
  r"^(?P<yearmonth>\d{4}\-\d{2})\s{1}(?P<currs_num_den_w_uline>[A-Z]{3}_[A-Z]{3}) exchange rates\.txt$"
re_cmpld_exchangerate_datafilename = re.compile(re_patt_exchangerate_datafilename)
tointerpol_exchangerate_datafilename = \
  '{yearmonth} {currnum_currden} exchange rates.txt'
year_foldername_patt = "{year} bcb exchange rates"
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


def make_yeardashmonth_n_currs_dailyexchrates_pp_datafilename(refmonthdate, currency_pair):
  year = refmonthdate.year
  month = refmonthdate.month
  yearmonthstr = f"{year:04}-{month:02}"
  currnum, currden = currency_pair
  currnum_currden = f"{currnum}_{currden}"
  return make_yearmonth_currnum_currden_exchrate_filename(yearmonthstr, currnum_currden)


class PrettyPrintMonthlyExchangeRatesRWBase:
  """
  This class is a base for a file reader class and a file writer

  The files involved are monthly exchange rates for a pair of currencies

  @see also the module's docstr above for more info

  Example:
    the text file that stores the daily exchange rates for BRL_USD in Jul 2020 is named:
      => '2020-07 BRL_USD exchange rates.txt'
    The lines of this file are organized as:

    seq | date | buyquote | sellquote | obs-if-any
      Obs:
        1 - seq is virtual, not recorded on the text file
        2 - obs-if-any is not yet implemented
        3 - curr_num and curr_den are implicit in the filename (as metadata)
        4 - the refmonth is also implicit in the filename (as metadata),
            though derived by any one date along the content

    The buyquote and sellquote are the main ones for the day
      (i.e., they are not the open-quote or close-quote,
      but the PTAC quote as it's defined and published by BCB)
  """

  txtdatafilename = "{yearmonth} {currs_num_den_w_uline} exchange rates.txt"
  DEFAULT_DATA_FOLDERNAME = 'bcb_indices'
  year_foldername_patt = year_foldername_patt

  def __init__(
      self,
      curr_3letter_pair: tuple[str, str],
      refmonthdate: datetime.date | str = None,
      dates_quotes_dict: dict[datetime.date: ercls.ExchangeRate] = None,
      rootdatafolderpath: os.path = None,
    ):
    self.lineseq = 0
    self.refmonthdate = refmonthdate
    self.rootdatafolderpath = rootdatafolderpath
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
    if self.rootdatafolderpath is None or not os.path.isdir(self.rootdatafolderpath):
      data_root_folderpath = sett.get_datafolder_abspath()
      self.rootdatafolderpath = os.path.join(data_root_folderpath, self.DEFAULT_DATA_FOLDERNAME)
    return self.treat_dates_quotes_dict()

  def convert_strdates_to_dates_in_quotesdict_if_needed(self):
    for pdate in self.dates_quotes_dict:
      strdate = pdate
      pdate = dtfs.make_date_or_none(strdate)
      if pdate == strdate:
        continue
      # has to swap it (datetime.date value replaces str value)
      exchrate = self.dates_quotes_dict[strdate]
      self.dates_quotes_dict.update({pdate: exchrate})
      del self.dates_quotes_dict[strdate]

  def treat_dates_quotes_dict(self):
    if self.dates_quotes_dict is None:
      self.dates_quotes_dict = {}
    try:
      self.dates_quotes_dict = dict(self.dates_quotes_dict)
    except ValueError:
      self.dates_quotes_dict = {}
    self.convert_strdates_to_dates_in_quotesdict_if_needed()
    self.verify_refmonth_against_dates_quotes_dict()

  def verify_refmonth_against_dates_quotes_dict(self):
    """
    This verification is because every exchrate date should belong to the month's object
    """
    self.convert_strdates_to_dates_in_quotesdict_if_needed()
    if self.refmonthdate is None:
      # okay, take anyone in dict and set it
      try:
        pdate, _ = self.dates_quotes_dict.items()[0]
        self.refmonthdate = rmd.make_refmonthdate_or_none(pdate)
      except IndexError as e:
        errmsg = f"Error: refmonth was not given and quotes dict is empty. Halting.\n{e}"
        raise ValueError(errmsg)
    for pdate in self.dates_quotes_dict:
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
  def yearfoldername(self):
    _yearfoldername = self.year_foldername_patt.format(year=self.year)
    return _yearfoldername

  @property
  def yearfolderpath(self):
    yearfolderpath = os.path.join(self.rootdatafolderpath, self.yearfoldername)
    os.makedirs(yearfolderpath, exist_ok=True)
    return yearfolderpath

  @property
  def yeardashmonth_pp_datafilepath(self) -> os.path | bytes | None:
    try:
      return os.path.join(self.yearfolderpath, self.yeardashmonth_pp_datafilename)
    except AttributeError:
      pass
    return None

  @property
  def currnum_uline_currden(self) -> str:
    return f"{self.curr_num}_{self.curr_den}"

  @property
  def currnum_slash_currden(self) -> str:
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
  def yeardashmonth_pp_datafilename(self) -> str:
    return make_yeardashmonth_n_currs_dailyexchrates_pp_datafilename(self.refmonthdate, self.currency_pair)

  def get_exchrate_for_date(self, pdate):
    try:
      return self.dates_quotes_dict[pdate]
    except KeyError:
      pass
    return None

  def add_or_upt_exchrate_to_month(self, exrate: ercls.ExchangeRate):
    try:
      self.dates_quotes_dict.update({exrate.exchratedate: exrate})
    except AttributeError:
      pass

  def batch_add_or_upt_daysprices_w_tuplelist(self, plist: list):
    for tupl in plist:
      pdate = tupl[0]
      buyprice = tupl[1]
      sellprice = tupl[2]
      exchrate = ercls.ExchangeRate(
        pdate=pdate, curr_num=self.curr_num, curr_den=self.curr_den, buyprice=buyprice, sellprice=sellprice
      )
      self.add_or_upt_exchrate_to_month(exchrate)

  def batch_add_or_upt_daysprices_w_exchratelist(self, plist: list[ercls.ExchangeRate]):
    for exchrate in plist:
      self.add_or_upt_exchrate_to_month(exchrate)

  def batch_add_or_upt_daysprices_w_list(self, plist: list):
    """
    @see docstr below
    """
    # introspect the first element to see whether it's a tuple or an ExchangeRate
    elem = plist[0]
    if isinstance(elem, tuple):
      return self.batch_add_or_upt_daysprices_w_tuplelist(plist)
    if not isinstance(elem, ercls.ExchangeRate):
      errmsg = f"TypeError: object {elem} is not an instance of ercls.ExchangeRate"
      raise TypeError(errmsg)
    return self.batch_add_or_upt_daysprices_w_exchratelist(plist)

  def batch_add_or_upt_daysprices_w_dict(self, pdict: dict[str | datetime.date: ercls.ExchangeRate]):
    """
    @see docstr below
    """
    for exchrate in pdict:
      self.add_or_upt_exchrate_to_month(exchrate)

  def batch_add_or_upt_daysprices_w_dict_or_list(self, pdict_or_list):
    """
    This method receives either a dict or a list with either tuples or ExchRates objects
      and batch-feeds their items to dates_quotes_dict
    """
    if isinstance(pdict_or_list, list):
      plist = pdict_or_list
      return self.batch_add_or_upt_daysprices_w_list(plist)
    pdict = pdict_or_list
    return self.batch_add_or_upt_daysprices_w_dict(pdict)

  @property
  def str_currencies_num_den(self):
    return f"{self.curr_num}/{self.curr_den}"

  def process(self):
    pass

  def __str__(self):
    outstr = f"""{self.__class__.__name__}
    {self.currnum_slash_currden}
    """
    return outstr


def adhoctest1():
  print(re_patt_exchangerate_datafilename)
  # yearmonth = '2020-07'
  curr_num = 'BRL'
  curr_den = 'USD'
  refmonthdate = rmd.make_current_refmonthdate()
  currency_pair = (curr_num, curr_den)
  fn = make_yeardashmonth_n_currs_dailyexchrates_pp_datafilename(refmonthdate, currency_pair)
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
  writer.batch_add_or_upt_daysprices_w_dict_or_list(pdict)
  print(writer)


if __name__ == "__main__":
  adhoctest1()
  process()
