#!/usr/bin/env python3
"""
fs/indices/bcb_br/bcb_fetchfunctions.py

import fs.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_posorder
"""
import copy
import datetime
import logging
import os
from dateutil.relativedelta import relativedelta
import settings as sett
import lib.indices.bcb_br.bcb_remote_api_fin_cls as apicls
import lib.db.db_settings as dbs
import lib.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import lib.datefs.convert_to_datetime_wo_intr_sep_posorder as cvdt
import art.bcb_br.exrate.currency_exchange_rate_model as exmod
import lib.textfs.logfunctions as logfs  # logfs.log_error_namedtuple
import lib.indices.bcb_br.bcb_api_db_or_txt_fetch_sqlalch_fs as fetchfs  # .find_db_cotacao_w_date_currnum_currden_session
_, modlevelogfn = os.path.split(__file__)
modlevelogfn = str(datetime.date.today()) + '_' + modlevelogfn[:-3] + '.log'
modlevelogfp = os.path.join(sett.get_datafolder_abspath(), modlevelogfn)
logging.basicConfig(filename=str(modlevelogfp), filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # DEBUG means it and all others levels will be logged


def add_exchanger_to_res_bcb_api_namedtuple(exchanger, p_namedtuple):
  """
  Transposes the db_exchanger_record to a namedtuple
  """
  return apicls.namedtuple_bcb_api1(
    curr_num=p_namedtuple.curr_num,
    curr_den=p_namedtuple.curr_den,
    cotacao_compra=p_namedtuple.cotacao_compra,
    cotacao_venda=p_namedtuple.cotacao_venda,
    cotacao_datahora=p_namedtuple.cotacao_datahora,
    param_date=p_namedtuple.param_date,
    error_msg=p_namedtuple.error_msg,
    gen_msg=p_namedtuple.gen_msg,
    exchanger=exchanger
  )


class CascadeApiDbFileBcbCotacaoDiaFetcher:
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

  def __init__(
      self,
      pdate: datetime.date | None = None,
      curr_num: str | None = None,
      curr_den: str | None = None,
    ):
    self.daysdate = pdate
    # if a fetch is successful, datahoracotacao will get the 'datahoracotacao' in json
    self.datahoracotacao = datetime.datetime.now()
    self.curr_num = curr_num
    self.curr_den = curr_den
    self.buyprice = None
    self.sellprice = None

  def treat_attrs(self):
    pass

  def try_find_cotacaodia_in_txt(self):
    pass

  def try_fetch_cotacaodia_in_db(self):

    fetchfs.find_db_cotacao_w_date_currnum_currden_session(self.daysdate, self.curr_num, self.curr_den)
    pass

  def process(self):
    """
    1 - first it looks up DB
    2 - if it's not found, it looks up the data text files
    3 - if it's not found either, it tries to access the remote API
    """
    self.try_fetch_cotacaodia_in_db()


class BatchApiDbFileBcbCotacaoDiaFetcher:


  def __init__(self):
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
      indate = cnv.make_date_or_none(pdate)
      if indate is None:
        continue
      verified_dates.append(indate)
    self._currency_dates = verified_dates

  def verify_dates_fr_to(self):
    if self.dates_fr_to is None:
      return
    date_fr, date_to = self.dates_fr_to
    date_fr = cnv.make_date_or_none(date_fr)
    date_to = cnv.make_date_or_none(date_to)
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
      tuplevalues = (self.currency_dates,)
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


def dbfetch_nt_bcb_exrate_or_none_w_date_n_currencypair(pdate, currency_pair=None):
  indate = cnv.make_date_or_none(pdate)
  if indate is None:
    return None
  curr_num, curr_den = dbs.DEFAUT_CURRENCY_PAIR
  if currency_pair is not None:
    curr_num, curr_den = currency_pair
  res_bcb_api1 = None
  session = exmod.consa.get_sa_session()
  db_found_exch = session.query(exmod.ExchangeRateDate). \
      filter(exmod.ExchangeRateDate.refdate == indate). \
      filter(exmod.ExchangeRateDate.curr_num == curr_num). \
      filter(exmod.ExchangeRateDate.curr_den == curr_den). \
      first()
  if db_found_exch:
    log_msg = 'Quote was in db. Returning it: %s' % str(db_found_exch)
    logger.info(log_msg)
    # print(log_msg)
    res_bcb_api1 = apicls.namedtuple_bcb_api1(
      curr_num=sett.CURR_BRL, curr_den=sett.CURR_USD,
      cotacao_compra=db_found_exch.buyprice_as_int, cotacao_venda=db_found_exch.sellprice_as_int,
      cotacao_datahora=db_found_exch.quote_as_datetime,
      param_date=db_found_exch.refdate, error_msg=None, gen_msg='Fetched from db',
      exchanger=db_found_exch
    )
  session.close()
  return res_bcb_api1


def fetch_cotacao_via_the_api_for_date_n_dbsaveit(pdate):
  """
  Consider this method 'private' for the api call should only be issued
  after verifying data is not 'cached' (or buffered) in the local db
  """
  caller = apicls.BcbCotacaoDiaApiCaller(pdate)
  namedtuple_res_bcb_api1 = caller.recurs_call_api_bcb_cotacao_dolar_on_daysdate()
  # 'put' returns the namedtuple_res_bcb_api1 itself
  return put_cotacao_into_db_n_return_namedtuple(namedtuple_res_bcb_api1, pdate)


def dbfetch_bcb_cotdolar_recursive_or_apifallback(pdate, recurse_pass=0):
  """
  First look up local sqlite-db, if not found, fallback to its corresponding API call
  """
  if recurse_pass > 5:
    print('recurse_pass > 5 |', recurse_pass)
    return None
  indate = cnv.make_date_or_none(pdate)
  if indate is None:
    return None
  today = datetime.date.today()
  if indate >= today:
    # log_msg = 'Date ' + str(indate) + ' is today (the rundate). Recursing without adding 1 to limit of 5 ' \
    #         + str(recurse_pass)
    # logger.info(log_msg)
    # print(log_msg)
    # indate = indate - datetime.timedelta(days=1)
    # return dbfetch_bcb_cotacao_dolar_or_apifallback(indate, recurse_pass)
    print('Date in the future. Please, reenter dateadhoctests up to the moment.')
    return None
  if cnv.is_date_weekend(indate):
    log_msg = 'Date ' + str(indate) + ' is weekend. Recursing (limit to 5) ' + str(recurse_pass + 1)
    logger.info(log_msg)
    print(log_msg)
    indate = indate - datetime.timedelta(days=1)
    # recurse one day back right away, today's quotes should be available after market
    # (TO-DO: write a dedicated function for this)
    return dbfetch_bcb_cotdolar_recursive_or_apifallback(indate, recurse_pass+1)
  return old_retrieve_cotacao_from_db_or_move_on_to_call_the_api(indate, recurse_pass)


def old_retrieve_cotacao_from_db_or_move_on_to_call_the_api(pdate, recurse_pass):
  """
  indate = pdate
  session = exmod.consa.get_sa_session()
  db_found_exch = session.query(exmod.ExchangeRateDate). \
      filter(exmod.ExchangeRateDate.quotesdate == indate). \
      first()
  if db_found_exch:
    log_msg = 'Quote was in db. Returning it: %s' % str(db_found_exch)
    logger.info(log_msg)
    # print(log_msg)
    res_bcb_api1 = apis.namedtuple_bcb_api1(
      cotacao_compra=db_found_exch.buyprice, cotacao_venda=db_found_exch.sellprice,
      cotacao_datahora=db_found_exch.quote_as_datetime,
      param_date=db_found_exch.quotesdate, error_msg=None, gen_msg='Fetched from db',
      exchanger=db_found_exch
    )
    session.close()
    if db_found_exch.buyprice is None and db_found_exch.sellprice is None:
      indate = indate - datetime.timedelta(days=1)
      return dbfetch_bcb_cotdolar_recursive_or_apifallback(indate, recurse_pass+1)
    return res_bcb_api1

  res_bcb_api1 = dbfetch_nt_bcb_exrate_or_none_w_date_n_currencypair(pdate)
  if res_bcb_api1:
    return res_bcb_api1
  # at this point, cotacao is not in db & it's not a weekend
  return fetch_cotacao_thru_the_api_for_its_not_in_db(indate)
  """
  _, _ = pdate, recurse_pass


def fetch_cotacao_thru_the_api_for_its_not_in_db(indate):
  """
  session = exmod.consa.get_sa_session()
  session.close()
  """
  caller = apicls.BcbCotacaoDiaApiCaller(indate)
  res_bcb_api1 = caller.recurs_call_api_bcb_cotacao_dolar_on_daysdate()
  log_msg = str(res_bcb_api1)
  logger.info(log_msg)
  print(log_msg)
  if res_bcb_api1 and res_bcb_api1.error_msg is not None:
    # 'next' function will return an 'error' namedtuple
    return logfs.log_error_namedtuple(res_bcb_api1)
  # at this point, the API call has something
  return put_cotacao_into_db_n_return_namedtuple(res_bcb_api1, indate)


def find_db_cotacao_w_date_currnum_currden_session(pdate, curr_num, curr_den, session):
  db_rec = session.query(exmod.ExchangeRateDate). \
      filter(exmod.ExchangeRateDate.refdate == pdate). \
      filter(exmod.ExchangeRateDate.curr_num == curr_num). \
      filter(exmod.ExchangeRateDate.curr_den == curr_den). \
      first()
  if db_rec:
    scrmsg = f"rec date {pdate} has been found {db_rec}"
    print(scrmsg)
    return db_rec
  return None


def update_db(namedtuple_res_bcb_api1, db_rec, session):
  db_rec.curr_num = namedtuple_res_bcb_api1.curr_num
  db_rec.curr_den = namedtuple_res_bcb_api1.curr_den
  db_rec.buyprice = namedtuple_res_bcb_api1.cotacao_compra
  db_rec.sellprice = namedtuple_res_bcb_api1.cotacao_venda
  db_rec.refdate = namedtuple_res_bcb_api1.param_date
  db_rec.quotestime = namedtuple_res_bcb_api1.cotacao_datahora
  # db_rec.update()
  print('dbupdating ', db_rec)
  session.commit()
  session.close()
  return namedtuple_res_bcb_api1


def put_cotacao_into_db_n_return_namedtuple(namedtuple_res_bcb_api1, pdate):
  param_date = cnv.make_date_or_none(namedtuple_res_bcb_api1.param_date)
  if pdate != param_date:
    errmsg = f"param_date {param_date} is different than pdate {pdate}"
    raise ValueError(errmsg)
  curr_num = namedtuple_res_bcb_api1.curr_num
  curr_den = namedtuple_res_bcb_api1.curr_den
  # indate = param_date  # pdate
  session = exmod.consa.get_sa_session()
  db_rec = find_db_cotacao_w_date_currnum_currden_session(pdate, curr_num, curr_den, session)
  if db_rec:
    return update_db(namedtuple_res_bcb_api1, db_rec, session)
  db_found_exch = exmod.ExchangeRateDate()
  session.add(db_found_exch)
  db_found_exch.curr_num = curr_num
  db_found_exch.curr_den = curr_den
  db_found_exch.buyprice = namedtuple_res_bcb_api1.cotacao_compra
  db_found_exch.sellprice = namedtuple_res_bcb_api1.cotacao_venda
  # strdate = namedtuple_res_bcb_api1.cotacao_datahora
  # pdate = intr.convert_strdate_to_date_or_none_w_sep_n_posorder(strdate, '/', 'mdy')
  db_found_exch.refdate = namedtuple_res_bcb_api1.param_date
  cot_hora = cvdt.make_datetime_n_get_time_via_split_from_strdt(namedtuple_res_bcb_api1.cotacao_datahora)
  db_found_exch.quotestime = cot_hora
  session.commit()
  log_msg = 'After session.commit() ' + str(db_found_exch)
  logger.info(log_msg)
  # print(log_msg)
  # now it's time to set db_found_exch, ie it's been instantiated, in the namedtuple var
  namedtuple_res_bcb_api1 = add_exchanger_to_res_bcb_api_namedtuple(db_found_exch, namedtuple_res_bcb_api1)
  session.close()
  return namedtuple_res_bcb_api1


def adhoctest_issue_date_by_date(daterangetuple):
  dateini, datefim = daterangetuple
  dateini = cnv.make_date_or_none(dateini)
  datefim = cnv.make_date_or_none(datefim)
  if dateini > datefim:
    # swap them
    tmpdate = datefim
    datefim = dateini
    dateini = tmpdate
  pdate = copy.copy(dateini)
  while pdate <= datefim:
    fetcher = CascadeApiDbFileBcbCotacaoDiaFetcher(pdate=pdate)
    fetcher.process()
    dts = fetcher.currency_dates
    print('dates', dts)
    for dt in fetcher.gen_dates_iter():
      print(dt)
    pdate += relativedelta(days=1)


def adhoc_test():
  # ==================
  print("# test 1")
  date_fr = '2025-03-15'
  date_to = '2025-03-25'
  daterangetuple = (date_fr, date_to)
  adhoctest_issue_date_by_date(daterangetuple)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
