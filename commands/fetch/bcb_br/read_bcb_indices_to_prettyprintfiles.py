#!/usr/bin/env python3
"""
commands/fetch/bcb_br/buffer_bcb_apifetch_to_prettyprint.py
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
import fs.datefs.convert_to_date_wo_intr_sep_posorder as dtfs
import fs.indices.bcb_br.bcb_exchrate_cls as ercls  # for class ercls.ExchangeRate
import commands.fetch.bcb_br.base_rw_bcb_indices_to_prettyprintfiles as baserw
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


class PrettyPrintMonthlyExchangeRatesReader(baserw.PrettyPrintMonthlyExchangeRatesRWBase):
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

  def read_file_into_dict(self):
    filepath = self.datafilepath
    fd = open(filepath, 'r')
    for line in fd.readlines():
      try:
        pp = line.split('|')
        # seq = pp[0]
        strdate = dtfs.make_date_or_none(pp[1])
        buyprice = float(pp[2])
        sellprice = float(pp[3])
        exrate_obj = ercls.ExchangeRate(
          pdate=strdate,
          curr_num=self.curr_num,
          curr_den=self.curr_den,
          buyprice=buyprice,
          sellprice=sellprice,
        )
        self.dates_quotes_dict.update({exrate_obj.exchratedate: exrate_obj})
      except AttributeError:
        pass

  @property
  def str_currencies_num_den(self):
    return f"{self.curr_num}/{self.curr_den}"

  def form_prettyprint_line_w_fields(self, exchrate: ercls.ExchangeRate):
    """
      Saves a "series" pretty-print dump formed in function
        dump_n_save_json_response_per_each_series_inside_data() above

    The pretty-print is like so:
    +-------------+------+--------+---------+-----------+
    |   seriesID  | year | period |  value  | footnotes |
    +-------------+------+--------+---------+-----------+
    | SUUR0000SA0 | 2020 |  M12   | 146.408 |           |
    | SUUR0000SA0 | 2020 |  M11   | 146.242 |           |
    (...)
    self.output.write(pprint_dump.get_string())

    """
    linevalues_list = [self.lineseq, exchrate.exchratedate, exchrate.buyprice, exchrate.buyprice]
    self.pp_seq_dt_buyp_sellp_str.add_row(linevalues_list)

  def write_file_w_prettyprintdump(self):
    """
    TODO Recuperates file if it exists previously
    """
    fd = open(self.datafilepath, 'w')
    scrmsg = f"Writing file [{self.datafilepath}]"
    print(scrmsg)
    fd.write(self.prettyprint_dump)
    fd.close()

  def finalize_writing_file(self):
    """
    Loops through all data putting line by line in the PrettyPrint object
    """
    try:
      for i, pdate in enumerate(self.dates_quotes_dict):
        self.lineseq = i + 1
        exrate_obj = self.dates_quotes_dict[pdate]
        self.form_prettyprint_line_w_fields(exrate_obj)
      return self.write_file_w_prettyprintdump()
    except KeyError:
      pass

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
  writer = PrettyPrintMonthlyExchangeRatesReader(
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
