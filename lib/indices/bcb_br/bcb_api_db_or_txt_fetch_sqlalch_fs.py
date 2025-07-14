#!/usr/bin/env python3
"""
fs/indices/bcb_br/bcb_api_db_or_txt_fetch_cls.py

import fs.datefs.introspect_dates as intr  # .convert_strdate_to_date_or_none_w_sep_n_posorder
"""
# from sympy.codegen.ast import continue_
import copy
import datetime
import logging
import os
from dateutil.relativedelta import relativedelta
import settings as sett
import lib.indices.bcb_br.bcb_remote_api_fin_fs as apis
import lib.datefs.convert_to_date_wo_intr_sep_posorder as dtfs
# import fs.db.db_settings as dbs
# import fs.datefs.convert_to_datetime_wo_intr_sep_posorder as cvdt
# import models.exrate.currency_exchange_rate_model as exmod
# import fs.textfs.logfunctions as logfs  # logfs.log_error_namedtuple
datetyp = datetime.date
_, modlevelogfn = os.path.split(__file__)
modlevelogfn = str(datetime.date.today()) + '_' + modlevelogfn[:-3] + '.log'
modlevelogfp = os.path.join(sett.get_datafolder_abspath(), modlevelogfn)
logging.basicConfig(filename=str(modlevelogfp), filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # DEBUG means it and all others levels will be logged


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


def adhoc_test():
  pass


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  """
  adhoc_test()
  process()
