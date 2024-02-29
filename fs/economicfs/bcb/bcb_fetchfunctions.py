#!/usr/bin/env python3
"""
fs/economicfs/bcb_fetchfunctions.py

import fs.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_posorder
"""
import datetime
import logging
import os
import settings as sett
import fs.economicfs.bcb.bcb_api_finfunctions as apis
import fs.db.db_settings as dbs
import fs.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import fs.datefs.convert_to_datetime_wo_intr_sep_posorder as cvdt
import models.exrate.currency_exchange_rate_model as exmod
import fs.textfs.logfunctions as logfs  # logfs.log_error_namedtuple
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
  return apis.namedtuple_bcb_api1(
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
    res_bcb_api1 = apis.namedtuple_bcb_api1(
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
  namedtuple_res_bcb_api1 = apis.call_api_bcb_cotacao_dolar_on_date(pdate)
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
  return retrieve_cotacao_from_db_or_move_on_to_call_the_api(indate, recurse_pass)


def retrieve_cotacao_from_db_or_move_on_to_call_the_api(pdate, recurse_pass):
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
  res_bcb_api1 = apis.call_api_bcb_cotacao_dolar_on_date(indate)
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


def adhoc_test():
  pass


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  adhoc_test()
