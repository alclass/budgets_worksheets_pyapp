#!/usr/bin/env python3
"""
  docstring

  bcb_api1_nt = coll.namedtuple('BCBAPI1DataStr', 'cotacao_compra cotacao_venda cotacao_datahora param_date error_msg')
  # 'value': [{'cotacaoCompra': 5.1641, 'cotacaoVenda': 5.1647, 'dataHoraCotacao': '2020-07-23 13:02:43.561'}]
"""
from prettytable import PrettyTable
import fs.datefs.datefunctions as dtfs
import fs.economicfs.apis_finfunctions as apis
import models.exchange_rate_modelmod as exmod
from fs.textfs import strfs
import config


class BRLUSDDailyQuotes:

  def __init__(self, pdate):
    self.pdate = pdate

  def fetch(self):
    if dtfs.is_date_weekend():
      return False


def dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate, recurse_pass=0):
  """
  First look up local sqlite-db, if not found, fallback to an API call
  """
  indate = dtfs.returns_date_or_none(pdate)
  session = exmod.con.Session()
  exchanger = session.query(exmod.ExchangeRateDate).\
      filter(exmod.ExchangeRateDate.quotesdate == indate).\
      first()
  if exchanger and exchanger.buyquote is not None:
    print('Quote was in db. Returning it: %s' % str(exchanger))
    res_bcb_api1 = apis.bcb_api1_nt(
      cotacao_compra=exchanger.buyquote, cotacao_venda=exchanger.sellquote, cotacao_datahora=exchanger.quotesdatetime,
      param_date=exchanger.quotesdate, error_msg=None
    )
    return res_bcb_api1
  res_bcb_api1 = apis.call_api_bcb_cotacao_dolar_on_date(indate, recurse_pass)
  if res_bcb_api1.error_msg is not None:
    return res_bcb_api1
  print('res_bcb_api1', res_bcb_api1)
  if exchanger is None:
    print('Creating exchange rate quote for db.')
    exchanger = exmod.ExchangeRateDate()
    session.add(exchanger)
  print('Updating exchange rate quote for db.')
  cotacao_compra = float(res_bcb_api1.cotacao_compra)
  exchanger.buyquote = cotacao_compra
  cotacao_venda = float(res_bcb_api1.cotacao_venda)
  exchanger.sellquote = cotacao_venda
  api_quotesdatetime = dtfs.returns_date_or_none(res_bcb_api1.cotacao_datahora)
  api_quotesdate, api_quotesdaytime = dtfs.split_date_n_time_from_datetime(api_quotesdatetime)
  exchanger.quotesdate = api_quotesdate
  exchanger.quotesdaytime = api_quotesdaytime
  exchanger.numerator_curr3 = config.CURR_BRL
  exchanger.denominator_curr3 = config.CURR_USD
  session.commit()
  session.close()
  print('Session closed.')
  return res_bcb_api1


def adhoc_test():
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


def process():
  # adhoc_test_ptab()
  adhoc_test()


if __name__ == "__main__":
  process()
