#!/usr/bin/env python3
"""
lib/indices/bcb_br/bcbparams.py

"""
import collections as coll
import re

url_base = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/' \
           'versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)'
url_query_interpol = "?@dataCotacao='%(mmddyyyy)s'&$top=100&$format=json"
MAX_BCB_COTACAODIA_API_MAX_PREVIOUSDAY_CALLS = 8
MAX_BCB_COTACAODIA_API_CONN_TRIES = 10
namedtuple_bcb_api1 = coll.namedtuple(
  'BCBAPI1DataStr',
  'curr_num curr_den cotacao_compra cotacao_venda cotacao_datahora param_date error_msg gen_msg exchanger'
)
TABLENAME = 'currencies_exchangerates'
DEFAULT_DATEFILENAME = 'datesfile.txt'
bcb_exchrates_midpath = 'bcb financial data/bcb financial data'
year_bcb_exchrates_foldername_interpol = "{year} bcb exchange rates"
yearmonth_currs_datafilename_interpol = "{yeardashmonth} {currnum_uline_currden} exchange rates.txt"
yearmonth_currs_datafilename_repatt = (r"^(?P<yeardmonth>\d{4}\-\d{2}) (?P<currnum_ul_currden>[A-Z]{3}_[A-Z]{3})"
                                       r" exchange rates\.txt$")
yearmonth_currs_datafilename_recmpl = re.compile(yearmonth_currs_datafilename_repatt)
CURR_USD = 'USD'
DEFAULT_CURRENCY_FROM = CURR_USD
CURR_BRL = 'BRL'
DEFAULT_CURRENCY_TO = CURR_BRL
CURR_EUR = 'EUR'
REGISTERED_CURRENCIES_3LETTER = [CURR_BRL, CURR_USD, CURR_EUR]


def adhoctest():
  fn = "2025-07 BRL_USD exchange rates.txt"
  match = yearmonth_currs_datafilename_recmpl.match(fn)
  scrmsg = f"fn = [{fn}] -> match = {match}"
  print(scrmsg)
  yeardashmonth = match.group('yeardmonth')
  currnum_uline_currden = match.group('currnum_ul_currden')
  scrmsg = f"yeardashmonth = {yeardashmonth} | currnum_uline_currden = {currnum_uline_currden}"
  print(scrmsg)


def process():
  pass


if __name__ == '__main__':
  """
  adhoctest()
  process()
  """
  adhoctest()
