#!/usr/bin/env python3
"""
commands/db/bcb_br/retrieve_bcbexchangerates_fr_db.py
  Retrieves BCB exchange rates stores in the local Sqlite-DB

import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import settings as sett
"""
import argparse
import datetime
from dateutil.relativedelta import relativedelta
# import fs.indices.bcb_br.bcb_cotacao_fetcher_from_db_or_api as fin
import lib.datefs.convert_to_date_wo_intr_sep_posorder as dtfs
import os
import settings as sett
import lib.indices.bcb_br.bcbparams as bcbparams
# import fs.datefs.convert_to_datetime_wo_intr_sep_posorder as cvdt
url_base = bcbparams.url_base
url_query_interpol = bcbparams.url_query_interpol
MAX_BCB_COTACAODIA_API_MAX_PREVIOUSDAY_CALLS = bcbparams.MAX_BCB_COTACAODIA_API_MAX_PREVIOUSDAY_CALLS
MAX_BCB_COTACAODIA_API_CONN_TRIES = bcbparams.MAX_BCB_COTACAODIA_API_CONN_TRIES
namedtuple_bcb_api1 = bcbparams.namedtuple_bcb_api1
yearmonth_currs_datafilename_interpol = bcbparams.yearmonth_currs_datafilename_interpol
bcb_exchrates_midpath = bcbparams.bcb_exchrates_midpath
year_bcb_exchrates_foldername_interpol = bcbparams.year_bcb_exchrates_foldername_interpol
TABLENAME = bcbparams.TABLENAME
DEFAULT_DATEFILENAME = bcbparams.DEFAULT_DATEFILENAME
DEFAULT_CURRENCY_FROM = bcbparams.DEFAULT_CURRENCY_FROM
DEFAULT_CURRENCY_TO = bcbparams.DEFAULT_CURRENCY_TO
REGISTERED_CURRENCIES_3LETTER = bcbparams.REGISTERED_CURRENCIES_3LETTER
# import fs.datefs.dategenerators as gendt
# import fs.datefs.read_write_datelist_files_fs as rwdt


def get_args_via_argparse():
  """
  https://realpython.com/command-line-interfaces-python-argparse/
  One Example:
    parser.add_argument("--veggies", nargs="+")
    parser.add_argument("--fruits", nargs="*")
      $ python cooking.py --veggies pepper tomato --fruits apple banana
    parser.add_argument("--size", choices=["S", "M", "L", "XL"], default="M")
    my_parser.add_argument("--weekday", type=int, choices=range(1, 8))

  def fetch_exchangerate_thru_api(pdate):
    bcb = fin.BCBCotacaoFetcher(pdate)
    bcb_api_nt = bcb.pop_dates_n_try_find_cotacao()
    return bcb_api_nt

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


class BCBExchangeRatesRetriever:

  TABLENAME = TABLENAME
  DEFAULT_DATEFILENAME = DEFAULT_DATEFILENAME

  def __init__(
      self,
      curr_fr=None, curr_to=None,
      date_fr=None, date_to=None,
      datafolderpath=None, datafilename=None, p_datafilepath=None
    ):
    self.curr_fr, self.curr_to = curr_fr, curr_to
    self.date_fr, self.date_to = date_fr, date_to
    self.datafolderpath, self.datafilename, self.p_datafilepath = datafolderpath, datafilename, p_datafilepath
    self.datesreader = None
    self.treat_attrs()
    self.today = datetime.date.today()
    self.seq = 0
    self.bcbs = []
    self.year = None
    self.month = None
    self.day = None
    self.datelist = None
    self.current_year = False
    self.yearrange = None
    self.has_read_datefile = False
    self.conn = None
    self.date_n_tupleprices_dict = {}
    self.treat_attrs()

  def treat_attrs(self):
    self.treat_currs()
    self.treat_dates()
    self.treat_attr_paths()

  def treat_currs(self):
    if self.curr_fr is None or self.curr_fr not in REGISTERED_CURRENCIES_3LETTER:
      self.curr_fr = DEFAULT_CURRENCY_FROM
    if self.curr_to is None or self.curr_to not in REGISTERED_CURRENCIES_3LETTER:
      self.curr_to = DEFAULT_CURRENCY_TO

  def treat_dates(self):
    if self.date_fr is None and self.date_to is None:
      self.date_to = dtfs.make_date_or_today(self.date_to)
      self.date_fr = self.date_to - relativedelta(days=7)
      return
    self.date_to = dtfs.make_date_or_today_forbid_future(self.date_to)
    self.date_fr = dtfs.make_date_or_none(self.date_fr)
    if self.date_fr is None:
      self.date_fr = self.date_to - relativedelta(days=7)
    self.date_fr, self.date_to = dtfs.swap_dates_if_first_is_greater_than_second(self.date_fr, self.date_to)

  def treat_attr_paths(self):
    """
    For the time being, datefilepath will be set as a convention (TODO recuperate its setting code)
    """
    # accept the double default (folderpath plus filename equals filepath)
    self.datafolderpath = sett.get_datafolder_abspath()
    self.datafilename = DEFAULT_DATEFILENAME

  @property
  def datesfilepath(self):
    return os.path.join(self.datafolderpath, self.datafilename)

  def get_year_bcb_exchrate_datafolder(self, year):
    fullmidpath = os.path.join(self.datafolderpath, bcb_exchrates_midpath)
    yearfoldername = year_bcb_exchrates_foldername_interpol.format(year=year)
    return os.path.join(fullmidpath, yearfoldername)

  def get_bcb_exchrates_yearmonth_pp_filepath(self, year, month):
    year_dash_month = f"{year}-{month:02}"
    currnum_uline_currden = self.currnum_uline_currden
    year_bcb_exchrates_pp_datafilename = yearmonth_currs_datafilename_interpol.format(
      year_dash_month=year_dash_month, currnum_uline_currden=currnum_uline_currden
    )
    return os.path.join(self.get_year_bcb_exchrate_datafolder(year), year_bcb_exchrates_pp_datafilename)

  @property
  def dates_in_run(self):
    return self.date_n_tupleprices_dict.keys()

  @property
  def first_date_in_run(self):
    return min(self.dates_in_run)

  @property
  def last_date_in_run(self):
    return max(self.dates_in_run)

  @property
  def datefilefolderpath(self):
    rootfolderpath = sett.get_datafolder_abspath()
    return rootfolderpath

  @property
  def datefilename(self):
    return self.DEFAULT_DATEFILENAME

  @property
  def datefilepath(self):
    return os.path.join(self.datefilefolderpath, self.datefilename)

  @property
  def attrs(self):
    _attrs = [
      fie_n_val for fie_n_val in self.__dict__.items()
      if not callable(fie_n_val[0])
    ]
    return _attrs

  def get_conn(self):
    self.conn = sett.get_sqlite_connection()
    return self.conn

  @property
  def curr_num(self):
    """
    curr_num means the currency on the numerator in a fraction (num/den), this is curr_to
    Example:
      5,55 BRL/USD means the exchange of BRL (the curr_to) to USD (the curr_fr [fr=from]) is 5,55
      The USD/BRL is just its inverse (i.e., 1/(BRL/USD))
    """
    return self.curr_to

  @property
  def curr_den(self):
    """
    curr_den means the currency on the denominator in a fraction (num/den), this is curr_fr [fr=from]
    Example:
      0,18 USD/BRL means the exchange of USD (the curr_to) to BRL (the curr_fr [fr=from]) is 0,18
      The BRL/USD is just its inverse (i.e., 1/(BRL/USD))
    """
    return self.curr_fr

  @property
  def currency_pair(self) -> tuple[str, str]:
    return self.curr_num, self.curr_to

  @property
  def currnum_slash_currden(self):
    return f"{self.curr_to}/{self.curr_fr}"

  @property
  def currnum_uline_currden(self):
    return f"{self.curr_to}_{self.curr_fr}"

  def make_sql_select(self) -> str:
    sql = f"""
    SELECT buypriceint, sellpriceint, refdate from {self.TABLENAME}
      WHERE
        curr_num = ? and curr_den = ? and
        refdate >= ? and refdate <= ?
      ORDER BY
        refdate; 
    """
    return sql

  def do_select(self):
    """
    Obs: the db-storing of the currency pair (from, to) is done by alphabetical precedence,
      i.e., the currency 3-letter code that comes alphabetically before is stored in the curr_num
      and then the curr_den
    Because of that, the method should check if the inverse division (1/n) should take place
    """
    conn = self.get_conn()
    cursor = conn.cursor()
    sql = self.make_sql_select()
    print(sql)
    from_to_inverted_position = False
    if self.curr_num < self.curr_to:
      from_to_inverted_position = True  # the inverse division (1/n) should happen at the end
      curr1 = self.curr_fr
      curr2 = self.curr_to
    else:
      # invert position and flag it
      curr1 = self.curr_to
      curr2 = self.curr_fr
    tuplevalues = (curr1, curr2, self.date_fr, self.date_to)
    cursor.execute(sql, tuplevalues)
    rows = cursor.fetchall()
    for record in rows:
      try:
        buyprice = float(record[0])/10000
        sellprice = float(record[1])/10000
        refdate = dtfs.make_date_or_none(record[2])
        if from_to_inverted_position:
          buyprice = 1/buyprice
          sellprice = 1/sellprice
        self.date_n_tupleprices_dict.update({refdate: (buyprice, sellprice)})
      except (TypeError, ValueError):
        pass

  def get_buyprice_n_sellprice_tuple_on_date(self, pdate) -> tuple:
    if pdate in self.date_n_tupleprices_dict.keys():
      pricetuple = self.date_n_tupleprices_dict[pdate]
      return pricetuple
    return None, None

  def get_date_n_tupleprices_dict_between_daterange(self, p_daterange: tuple = None):
    """
    From https://realpython.com/sort-python-dictionary/
      # Sort by key
      dict(sorted(people.items()))
        {1: 'Jill', 2: 'Jack', 3: 'Jim', 4: 'Jane'}

      # Sort by value
      dict(sorted(people.items(), key=lambda item: item[1]))
        {2: 'Jack', 4: 'Jane', 1: 'Jill', 3: 'Jim'}

    pdict = {k: pdict[k] for k in pdict if inidate <= k <= fimdate else None}
    """
    if p_daterange is None or len(p_daterange) == 0:
      daterange = self.date_fr, self.date_to
    else:
      daterange = p_daterange
    inidate, fimdate = daterange
    inidate = dtfs.make_date_or_none(inidate)
    if inidate is None:
      inidate = self.first_date_in_run
    fimdate = dtfs.make_date_or_none(fimdate)
    if fimdate is None:
      fimdate = self.last_date_in_run
    # remind that date_tupleprices_dict.items() has elements with
    # k[0] (the key) the date and k[1] (the value) the tuple (buyprice, sellprice)
    pdict = filter(lambda k: inidate <= k[0] <= fimdate, self.date_n_tupleprices_dict.items())
    pdict = dict(pdict)
    pdict = dict(sorted(pdict.items()))
    return pdict

  def process(self):
    self.do_select()
    print(self)

  def from_to_daterange(self):
    pdate = self.date_fr
    while pdate <= self.date_to:
      yield pdate
      pdate = pdate + relativedelta(days=1)

  @property
  def n_found_recs(self) -> int:
    try:
      return len(self.date_n_tupleprices_dict.keys())
    except AttributeError:
      pass
    return 0

  def buy_sell_prices_quote_wholedaterange_str(self):
    outstr = "Buy | Sell price quotes:\n"
    for pdate in self.from_to_daterange():
      buy, sell = self.get_buyprice_n_sellprice_tuple_on_date(pdate)
      outstr += f"{pdate} -> buy={buy} | sell={sell}\n"
    return outstr

  def buy_sell_prices_quote_str(self):
    outstr = f"seq |    Date    |    Buy     |  Sell {self.currnum_slash_currden}\n"
    for i, pdate in enumerate(self.date_n_tupleprices_dict.keys()):
      buy, sell = self.get_buyprice_n_sellprice_tuple_on_date(pdate)
      seq = i + 1
      outstr += f"\t{seq}   | {pdate} | buy={buy} | sell={sell}\n"
    outstr = outstr.rstrip('\n')
    return outstr

  def __str__(self):
    outstr = f"""Fetcher:
    curr_fr = {self.curr_fr}
    curr_to = {self.curr_to}
    date_fr = {self.date_fr}
    date_to = {self.date_to}
    -----------------
    {self.buy_sell_prices_quote_str()}
    -----------------
    total exchrates found = {self.n_found_recs}
    """
    return outstr


def adhoctest():
  pass


def process():
  """
    580   | 2023-12-04 | buy=4.9085 | sell=4.909
    581   | 2023-12-05 | buy=4.9516 | sell=4.9522
    582   | 2023-12-06 | buy=4.9025 | sell=4.9031
    583   | 2023-12-07 | buy=4.8943 | sell=4.8949
  """
  retriever = BCBExchangeRatesRetriever(
    date_fr='2017-10-1',
    date_to='2024-10-31'
  )
  retriever.process()
  inidate, fimdate = '2023-12-04', '2023-12-07'
  daterange = inidate, fimdate
  print(daterange)
  res = retriever.get_date_n_tupleprices_dict_between_daterange(daterange)
  for it in res:
    print(it, res[it])


if __name__ == '__main__':
  """
  adhoctest2()
  """
  process()
