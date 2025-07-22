#!/usr/bin/env python3
"""
lib/indices/bcb_br/bcb_api_db_or_txt_fetch_sqlalch_fs.py
  Contains functions for fetching exchange rates from DB

import fs.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_posorder
"""
# from sympy.codegen.ast import continue_
import datetime
import logging
import os
import settings as sett
import lib.indices.bcb_br.bcb_remote_api_fin_cls as apicls
import art.inflmeas.bcb_br.classes.modelbase_currency_exchrate as exrt  # .BaseCurrExchRate
import lib.db.sqlalchemy_connection_clsmod as sqlconn # .SqlAlchemyConnector
import art.inflmeas.bcb_br.classes.daycurrexchrate_sqlal as exrtmod  # .ExchangeRateDate
# import fs.db.db_settings as dbs
# import fs.datefs.convert_to_datetime_wo_intr_sep_posorder as cvdt
# import models.exrate.currency_exchange_rate_model as exmod
import lib.textfs.logfunctions as logfs  # logfs.log_error_namedtuple
datetyp = datetime.date
_, modlevelogfn = os.path.split(__file__)
modlevelogfn = str(datetime.date.today()) + '_' + modlevelogfn[:-3] + '.log'
modlevelogfp = os.path.join(sett.get_datafolder_abspath(), modlevelogfn)
logging.basicConfig(filename=str(modlevelogfp), filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # DEBUG means it and all others levels will be logged


class DbOrTxtExchangeRateFetcher(exrt.DayCurrExchRate):

  def __init__(self, date_fr, date_to, datelist, currency_pair):
    super(self, date_fr, date_to, datelist, currency_pair)
    self.date_fr, self.date_to = date_fr, date_to
    self.datelist = datelist
    self.currency_pair = currency_pair
    sqlal = sqlconn.SqlAlchemyConnector()
    self.session = sqlal.get_sa_session()

  def find_db_cotacao_w_date_currnum_currden_session(self, pdate):
    o = find_db_cotacao_w_date_currnum_currden_session(pdate, self.curr_num, self.curr_den, self.session)
    print(o)

  def run_fetch_thru_dates(self):
    actual_datelist = []
    if self.datelist:
      actual_datelist = self.datelist
    else:
      actual_datelist = self.gen_datelist_fr_to
    for pdate in actual_datelist:
      self.find_db_cotacao_w_date_currnum_currden_session()


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
  """
  Correct the SqlAlchemy class
    at this moment apicls.BcbCotacaoDiaApiCallerExchangeRateDate
      is not a SqlAlchemy class

    look up where is the other one: exmod.ExchangeRateDate
  """
  db_rec = session.query(exrtmod.SADayCurrExchRate). \
      filter(exrtmod.SADayCurrExchRate.refdate == pdate). \
      filter(exrtmod.SADayCurrExchRate.curr_num == curr_num). \
      filter(exrtmod.SADayCurrExchRate.curr_den == curr_den). \
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
  db_found_exch = exmod.DayCurrExchRate()
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
  pdate = '2020-10-15'
  curr_num, curr_den = 'BRL', 'USD'
  sqlal = sqlconn.SqlAlchemyConnector()
  session = sqlal.get_sa_session()
  o = find_db_cotacao_w_date_currnum_currden_session(pdate, curr_num, curr_den, session)
  print(o)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  """
  adhoc_test()
  process()
