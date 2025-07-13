#!/usr/bin/env python3
"""
fs/indices/bcb_br/bcb_api_db_or_txt_fetch_cls.py

import fs.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_posorder
"""
import copy
import datetime
import logging
import os
from dateutil.relativedelta import relativedelta
from sympy.codegen.ast import continue_
import settings as sett
import fs.indices.bcb_br.bcb_api_finfunctions as apis
import fs.db.db_settings as dbs
import fs.datefs.convert_to_date_wo_intr_sep_posorder as dtfs
import fs.datefs.convert_to_datetime_wo_intr_sep_posorder as cvdt
import models.exrate.currency_exchange_rate_model as exmod
import fs.textfs.logfunctions as logfs  # logfs.log_error_namedtuple
datetyp = datetime.date
_, modlevelogfn = os.path.split(__file__)
modlevelogfn = str(datetime.date.today()) + '_' + modlevelogfn[:-3] + '.log'
modlevelogfp = os.path.join(sett.get_datafolder_abspath(), modlevelogfn)
logging.basicConfig(filename=str(modlevelogfp), filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # DEBUG means it and all others levels will be logged


class BCBApiDbOrTxtExchangeRateFetcher:
  """
  This class organizes fetching currency exchange rates by dates.

  This data set can be retrieved either:

    a) from its open API at BCB
    b) or from DB (cached data in the local computer previously gotten via the API above)
    c) or data text files (also cached in the computer idem)

  This also means that the other scripts that API-fetches data
     should also cache it to b) and c) mentioned above.

  The precedence order for looking up exchange rates is the following:
    1 - first it looks up DB
    2 - if it's not found, it looks up the data text files
    3 - if it's not found either, it tries to access the remote API
  """

  def __init__(self, currency_dates: list[datetyp] = None, dates_fr_to: tuple[datetyp, datetyp] = None):
    self._currency_dates = currency_dates
    self.dates_fr_to = dates_fr_to
    self.treat_attrs()

  def treat_attrs(self):
    self.treat_dates()

  def treat_dates(self):
    """
    Either currency_dates is set or dates_fr_to is, if both are then raise a ValueError exception
    """
    if self._currency_dates and self.dates_fr_to:
      # oh, oh, it's an error
      errmsg = f"""Error: both parameters: 
        a) currency_dates (a list of dates) and
        b) dates_fr_to (coordinates date-from date-to)
      were given, only one can. Please, change input parameters and retry.
      
      currency_dates=[{self._currency_dates}]  | dates_fr_to={self.dates_fr_to}
      ------------------------------------------------------------------------- 
      """
      raise ValueError(errmsg)
    if self._currency_dates is None and self.dates_fr_to is None:
      # oh, oh, it's also an error
      errmsg = f"""Error: both parameters: 
        a) currency_dates (a list of dates) and
        b) dates_fr_to (coordinates date-from date-to)
      were NOT given. Please, input parameter one parameter or the other.
            
      currency_dates=[{self._currency_dates}]  | dates_fr_to={self.dates_fr_to}
      ------------------------------------------------------------------------- 
      """
      raise ValueError(errmsg)
    self.verify_dates_list()
    self.verify_dates_fr_to()

  def verify_dates_list(self):
    if self._currency_dates is None or len(self._currency_dates) == 0:
      return
    types_fine = list(map(lambda e: isinstance(e, datetime.date), self._currency_dates))
    if False not in types_fine:
      return
    verified_dates = []
    for pdate in self._currency_dates:
      indate = dtfs.make_date_or_none(pdate)
      if indate is None:
        continue
      verified_dates.append(indate)
    self._currency_dates = verified_dates

  def verify_dates_fr_to(self):
    if self.dates_fr_to is None:
      return
    date_fr, date_to = self.dates_fr_to
    date_fr = dtfs.make_date_or_none(date_fr)
    date_to = dtfs.make_date_or_none(date_to)
    if date_to < date_fr:
      # swap positions
      tmpdate = date_fr
      date_fr = date_to
      date_to = tmpdate
    self.dates_fr_to = (date_fr, date_to)

  @property
  def currency_dates(self):
    if self._currency_dates:
      return self._currency_dates
    tmpdatelist = list(self.gen_dates_iter())
    return tmpdatelist

  def gen_dates_iter(self):
    if self._currency_dates:
      for pdate in self._currency_dates:
        yield pdate
      return
    date_fr = self.dates_fr_to[0]
    date_to = self.dates_fr_to[1]
    pdate = copy.copy(date_fr)
    while pdate <= date_to:
      yield pdate
      pdate = pdate + relativedelta(days=1)
    return

  def try_find_exchrates_in_db(self):
    tablename = 'abc'
    conn = sett.get_sqlite_connection()
    if self._currency_dates:
      sql = f"""SELECT curr_num, curr_den FROM {tablename}
      WHERE currdate IN ? ;
      """
      tuplevalues = (self.currency_dates, )
    else:
      sql = f"""SELECT curr_num, curr_den, currdate FROM {tablename}
      WHERE currdate >= ? and currdate <= ?;
      """
      date_fr, date_to = self.dates_fr_to
      tuplevalues = (date_fr, date_to)
    cursor = conn.cursor()
    cursor.execute()
    rows = cursor.fetchall()
    for row in rows:
      # instantiate an ExRate object
      pass

  def try_find_exchrates_in_txt(self):
    for pdate in self.gen_dates_iter():
      pass


  def process(self):
    """
    1 - first it looks up DB
    2 - if it's not found, it looks up the data text files
    3 - if it's not found either, it tries to access the remote API
    """
    pass


def adhoc_test():
  # ==================
  print("# test 1")
  date_fr = '2025-03-15'
  date_to = '2025-03-25'
  dates_fr_to = (date_fr, date_to)
  fetcher = BCBApiDbOrTxtExchangeRateFetcher(dates_fr_to=dates_fr_to)
  fetcher.process()
  dts = fetcher.currency_dates
  print('dates', dts)
  for dt in fetcher.gen_dates_iter():
    print(dt)
  # ==================
  print("# test 2")
  dates = ['2025-03-15', '2025-03-20', '2025-03-25']
  fetcher = BCBApiDbOrTxtExchangeRateFetcher(currency_dates=dates)
  fetcher.process()
  dts = fetcher.currency_dates
  print('dates', dts)
  for dt in fetcher.gen_dates_iter():
    print(dt)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  """
  adhoc_test()
  process()
