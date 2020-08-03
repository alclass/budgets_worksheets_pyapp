#!/usr/bin/env python3
"""
  docstring

  bcb_api1_nt = coll.namedtuple('BCBAPI1DataStr', 'cotacao_compra cotacao_venda cotacao_datahora param_date error_msg')
  # 'value': [{'cotacaoCompra': 5.1641, 'cotacaoVenda': 5.1647, 'dataHoraCotacao': '2020-07-23 13:02:43.561'}]

class BRLUSDDailyQuotes:

  def __init__(self, pdate):
    self.pdate = pdate

  def fetch(self):
    if dtfs.is_date_weekend():
      return False

"""
import datetime
import time
from prettytable import PrettyTable
import fs.datefs.datefunctions as dtfs
import fs.economicfs.apis_finfunctions as apis
import models.exchange_rate_modelmod as exmod
from fs.textfs import strfs
import config


def treat_error(named_tuple):
  print('Error')
  print('named_tuple', named_tuple)
  try:
    print(named_tuple.error_msg)
  except AttributeError:
    pass
  return named_tuple


def dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate, recurse_pass=0):
  """
  First look up local sqlite-db, if not found, fallback to its corresponding API call
  """
  if recurse_pass > 5:
    print('recurse_pass > 5 |', recurse_pass)
    return None
  indate = dtfs.returns_date_or_none(pdate)
  if indate is None:
    return None
  if dtfs.is_date_weekend(indate):
    print('Date', indate, 'is weekend. Recursing (limit to 5)', recurse_pass+1)
    indate = indate - datetime.timedelta(days=1)
    return dbfetch_bcb_cotacao_compra_dolar_apifallback(indate, recurse_pass+1)
  session = exmod.con.Session()
  exchanger = session.query(exmod.ExchangeRateDate).\
      filter(exmod.ExchangeRateDate.quotesdate == indate).\
      first()
  if exchanger:
    print('Quote was in db. Returning it: %s' % str(exchanger))
    res_bcb_api1 = apis.bcb_api1_nt(
      cotacao_compra=exchanger.buyquote, cotacao_venda=exchanger.sellquote, cotacao_datahora=exchanger.quotesdatetime,
      param_date=exchanger.quotesdate, error_msg=None, gen_msg='Fetched from db',
    )
    session.close()
    return res_bcb_api1
  res_bcb_api1 = apis.call_api_bcb_cotacao_dolar_on_date(indate)
  if res_bcb_api1 and res_bcb_api1.error_msg is not None:
    session.close()
    return treat_error(res_bcb_api1)
  exchanger = exmod.ExchangeRateDate()
  session.add(exchanger)
  exchanger.numerator_curr3 = config.CURR_BRL
  exchanger.denominator_curr3 = config.CURR_USD
  buyquote = res_bcb_api1.cotacao_compra
  if buyquote is not None:
    exchanger.buyquote = buyquote
  sellquote = res_bcb_api1.cotacao_venda
  if sellquote is not None:
    exchanger.sellquote = sellquote
  cotacao_dt = res_bcb_api1.cotacao_datahora
  if cotacao_dt is None:
    cotacao_dt = dtfs.convert_date_to_datetime_or_none(indate)
  exchanger.quotesdatetime = cotacao_dt
  session.commit()
  session.close()
  '''
  if res_bcb_api1.cotacao_compra is None and res_bcb_api1.cotacao_venda is None:
    # recurse to one previous day
    indate = indate - datetime.timedelta(days=1)
    print('recurse_pass (limit 5) to', recurse_pass+1, indate)
    return dbfetch_bcb_cotacao_compra_dolar_apifallback(indate, recurse_pass+1)
  '''
  return res_bcb_api1


def adhoc_test1():
  dates = []
  strdate = '22/9/2015'  # '2020-01-07'
  strdate = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(strdate, tosep='-', sourceposorder='dmy')
  pdate = dtfs.returns_date_or_today(strdate)
  dates.append(pdate)
  strdate = '12/5/2016'  # '2020-01-07'
  strdate = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(strdate, tosep='-', sourceposorder='dmy')
  pdate = dtfs.returns_date_or_today(strdate)
  dates.append(pdate)

  ptab = PrettyTable()
  ptab.field_names = ['seq', 'data dmy', 'compra', 'venda', 'data ymd']
  for i, pdate in enumerate(dates):
    seq = i + 1
    res_bcb_api1 = dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)
    quotesdate = dtfs.convert_datetime_to_date_or_none(res_bcb_api1.cotacao_datahora)
    dmypdate = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(
      quotesdate, tosep='/', targetposorder='dmy'
    )
    cotacao_compra_with_comma = strfs.replace_point_to_comma(res_bcb_api1.cotacao_compra, decimal_places=4)
    cotacao_venda_with_comma = strfs.replace_point_to_comma(res_bcb_api1.cotacao_venda, decimal_places=4)
    ptab.add_row([seq, dmypdate, cotacao_compra_with_comma, cotacao_venda_with_comma, res_bcb_api1.param_date])
  print(ptab)
  text = ptab.get_html_string()
  filename = 'exchange_rate_on_dates.html'
  filepath = dtfs.get_datafolder_abspath_for_filename_w_tstamp(filename)
  fp = open(filepath, 'w', encoding='utf8')
  fp.write(text)
  fp.close()


def batch_fetch_brl_usd_cotacoes():
  inidate = '2020-1-1'
  findate = '2020-2-1'
  res_bcb_api1_list = []
  for pdate in dtfs.generate_daterange(inidate, findate):
    print(pdate, '-'*30)
    res_bcb_api1 = dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)
    if type(res_bcb_api1) == apis.bcb_api1_nt:
      res_bcb_api1_list.append(res_bcb_api1)
    print('res_bcb_api1', res_bcb_api1)
    print('=== wait 1 sec ===')
    time.sleep(1)
  apis.pretry_print_api_list(res_bcb_api1_list)


def adhoc_test2():
  pass


def process():
  # adhoc_test_ptab()
  batch_fetch_brl_usd_cotacoes()


if __name__ == "__main__":
  process()
