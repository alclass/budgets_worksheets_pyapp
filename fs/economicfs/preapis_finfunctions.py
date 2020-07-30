#!/usr/bin/env python3
'''
'''
import datetime, json, requests
from prettytable import PrettyTable
import xlsxwriter
import fs.datefs.datefunctions as dtfs
import fs.economicfs.apis_finfunctions as apis
# import sqlalchemy
import models.exchange_rate_modelmod as exmod
import models.conn_sa as con
from fs.textfs import strfs
import config

def dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate, recurse_pass=0):
  '''
  First look up local sqlite-db, if not found, fallback to an API call
  '''
  indate = dtfs.returns_date_or_None(pdate)
  session = exmod.con.Session()
  exchanger = session.query(exmod.ExchangeRateDate).\
    filter(exmod.ExchangeRateDate.quotesdate==indate).\
    first()
  if exchanger and exchanger.buyquote!=None:
    print('Quote was in db. Returning it: %s' %str(exchanger))
    return indate, exchanger.buyquote, exchanger.quotesdate
  indate, cotacaoCompra, dataCotacao = apis.call_api_bcb_cotacao_dolar_on_date(indate, recurse_pass)
  print(indate, cotacaoCompra, dataCotacao)
  if exchanger is None:
    print('Creating exchange rate quote for db.')
    exchanger = exmod.ExchangeRateDate()
    session.add(exchanger)
  print('Updating exchange rate quote for db.')
  cotacaoCompra = float(cotacaoCompra)
  exchanger.buyquote = cotacaoCompra
  api_quotesdate = dtfs.returns_date_or_None(dataCotacao)
  if api_quotesdate is None:
    api_quotesdate = indate
  exchanger.quotesdate = api_quotesdate
  exchanger.numerator_curr3 = config.CURR_BRL
  exchanger.denominator_curr3 = config.CURR_USD
  session.commit()
  session.close()
  print ('Session closed.')
  return indate, cotacaoCompra, dataCotacao

def adhoc_test():
  dates = []
  strdate = '22/9/2015' # '2020-01-07'
  strdate = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(strdate,tosep='-', sourceposorder='dmy')
  pdate = dtfs.returns_date_or_today(strdate)
  dates.append(pdate)
  strdate = '12/5/2016' # '2020-01-07'
  strdate = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(strdate, tosep='-', sourceposorder='dmy')
  pdate = dtfs.returns_date_or_today(strdate)
  dates.append(pdate)

  ptab = PrettyTable()
  ptab.field_names = ['Seq', 'Data', 'valor câmbio', 'data câmbio']
  for i, pdate in enumerate(dates):
    seq = i + 1
    pdate, cotacaoCompra, dataCotacao = dbfetch_bcb_cotacao_compra_dolar_apifallback(pdate)
    dmypdate = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(pdate, tosep='/', targetposorder='dmy')
    dmydataCotacao = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(dataCotacao, tosep='/', targetposorder='dmy')
    cotacaoCompra_with_comma = strfs.replace_point_to_comma(cotacaoCompra, decimal_places=4)
    ptab.add_row([seq, dmypdate, cotacaoCompra_with_comma, dmydataCotacao])
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
