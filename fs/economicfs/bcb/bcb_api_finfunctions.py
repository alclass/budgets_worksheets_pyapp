#!/usr/bin/env python3
"""
The main function in this module is call_api_bcb_cotacao_dolar_on_date()
  See its docstring for info.
  
https://dadosabertos.bcb.gov.br/dataset/taxas-de-cambio-todos-os-boletins-diarios

Unidades de medida:

Moedas tipo A: Paridade (dólar): Quantidade da moeda por uma unidade de dólar americano (USD);
Cotação (unidade monetária corrente): Quantidade de moeda corrente por uma unidade da moeda

Moedas tipo B: Paridade (dólar): Quantidade de dólar americano (USD) por uma unidade da moeda;
Cotação (unidade monetária corrente): Quantidade de moeda corrente por uma unidade da moeda

Exemplo de cálculo da cotação das moedas tipo A em unidade monetária corrente,
  considerando o real (BRL) como unidade monetária corrente e o dólar canadense (CAD)
  como moeda estrangeira:

Cotação de Compra CADBRL = Cotação USDBRL de Compra ÷ Paridade USDCAD de Venda
Cotação de Venda CADBRL = Cotação USDBRL de Venda ÷ Paridade USDCAD de Compra

Exemplo de cálculo da cotação das moedas tipo B em unidade monetária corrente,
  considerando o real (BRL) como unidade monetária corrente e o euro (EUR)
  como moeda estrangeira:

Cotação de Compra EURBRL = Paridade EURUSD de Compra × Cotação USDBRL de Compra
Cotação de Venda EURBRL = Paridade EURUSD de Venda × Cotação USDBRL de Venda  

https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/documentacao

Para o Euro:
https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/aplicacao#!/recursos/CotacaoMoedaPeriodoFechamento

https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodoFechamento
  (codigoMoeda=@codigoMoeda,dataInicialCotacao=@dataInicialCotacao,dataFinalCotacao=@dataFinalCotacao)
  ?@codigoMoeda='EUR'&@dataInicialCotacao='07-09-2020'&@dataFinalCotacao='07-22-2020'&
  $top=100&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim

The API accepts a data in the format 'MM/DD/YYYY'. The returned dataHoraCotacao is "YYYY-MM-DD HH:MI:SS.MMM".
  The JsonToDict Result, for the URL above, is:
{
  '@odata.context': 'https://was-p.bcnet.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata$metadata#_CotacaoDolarDia',
  'value':[{'cotacaoCompra': 5.1641, 'cotacaoVenda': 5.1647, 'dataHoraCotacao': '2020-07-23 13:02:43.561'}]
}

When empty, it wraps up json within /* */:
https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia
/*{
  "codigo" : 400,
  "mensagem" : "The URI is malformed."
}*/
"""
import collections as coll
import datetime
import json
import os
import requests
import time
from prettytable import PrettyTable
import settings as sett
import fs.datefs.years_date_functions as dtfs
import fs.datefs.introspect_dates as dtconv  # .trans_strdate_from_one_format_to_another_w_sep_n_posorder

url_base = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/' \
           'versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)'
url_quer_interpol = "?@dataCotacao='%(mmddyyyy)s'&$top=100&$format=json"

API_CALL_COTACAO_MAX_PREVIOUS_DAY_TRIES = 8

namedtuple_bcb_api1 = coll.namedtuple(
  'BCBAPI1DataStr',
  'cotacao_compra cotacao_venda cotacao_datahora param_date error_msg gen_msg exchanger'
)
# 1) cotacao_compra is cotacaoCompra, 2) cotacao_venda is cotacaoVenda &  3) cotacao_datahora is dataHoraCotacao


def call_api_bcb_cotacao_dolar_on_date(pdate, connection_error_raised=0):
  """
  This function calls an endpoint API from the Banco Central do Brasil web services.
  Consider it a PRIVATE function in the sense that it should not be called directly.

  The call should be done to:
    preapis_finfunctions.dbfetch_bcb_cotacao_dolar_or_apifallback()

  This is necessary for the following reasons:
    1) the entrance function (in preapis) filters out weekend days (that do not have quotes);
    2) the entrance function checks a local 'buffer' database for the asked info;
    3) the entrance function envelops this so that it records an API response.

* The guide page for it is https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/aplicacao#!/recursos/CotacaoDolarDia
* An example follows:

  https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)
    ?@dataCotacao='07-23-2020'&$top=100&$format=json
  The JsonToDict Result, for the URL above, is:
  '{'
    '@odata.context': 'https://was-p.bcnet.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata$metadata#_CotacaoDolarDia',
    'value':[{'cotacaoCompra': 5.1641, 'cotacaoVenda': 5.1647, 'dataHoraCotacao': '2020-07-23 13:02:43.561'}]
  }

* Notice:
  when there's no currency exchange quote data, server answers 'value' as [], ie, the empty list,
    if, on the other hand, there is data, we're interested in the element-0
    which is a dict (in Python terms).

* Time backword recursion:
  On weekdays or holidays, there is no exchange info.
    Because of that, the functions looks up
    to see if value is [] (ie, the empty list) and tries again one day before.
  However, constant API_CALL_COTACAO_MAX_PREVIOUS_DAY_TRIES
    defines the maximum number of retries.
  Because of that attempt, the dataCotacao will also be return so that
    incoming (input) pdate and dataCotacao may be compared.

  The caller can also check where a date is a weekend day or a holiday in Brasil and
    in that case the max tries constant can very well be 0, ie, no retries.
  (This constant can be placed in settings.py at the app's root folder,
    so that it can be changed from there.)

  :param pdate:
  :param connection_error_raised:
  :return:
  """
  if connection_error_raised > 10:
    error_msg = 'connection_error_raised > 10 (%d)' % connection_error_raised
    raise requests.exceptions.ConnectionError(error_msg)
  refdate = dtfs.returns_date_or_none(pdate)
  if refdate is None:
    pdatetime = datetime.datetime.now()
    error_msg = 'Given date (%s) is None' % str(pdate)
    res_bcb_api = namedtuple_bcb_api1(
      cotacao_compra=None, cotacao_venda=None, cotacao_datahora=pdatetime,
      param_date=pdate,
      error_msg=error_msg, gen_msg=None,
      exchanger=None
    )
    return res_bcb_api
  # the API accepts a data in the format 'MM/DD/YYYY', so it needs to convert pdate to it
  mmddyyyy = dtconv.trans_strdate_from_one_format_to_another_w_sep_n_posorder(
    refdate, fromsep=None, tosep='/', sourceposorder=None, targetposorder='mdy')
  if mmddyyyy is None:
    error_msg = f"""An error occurred when trying to convert date {refdate} to a mdy sep / format,
    ie "mm/dd/yyyy" date format (got None).  This convertion is necessary to call the
      BCB REST API for fetching BRL/USD exchange rate date."""
    raise ValueError(error_msg)
  url = url_base + url_quer_interpol % {'mmddyyyy': mmddyyyy}
  print('calling', url)
  try:
    res = requests.get(url)
  except requests.exceptions.ConnectionError:
    wait_in_sec = 3 + connection_error_raised
    recurse_msg = '[Error for recurse] connection_error_raised ntimes=%d :: wait %d seconds' \
                  % (connection_error_raised+1, wait_in_sec)
    print(recurse_msg)
    time.sleep(wait_in_sec)
    return call_api_bcb_cotacao_dolar_on_date(pdate, connection_error_raised+1)
  if res.status_code != 200:
    error_msg = 'Error: HTTP Connection status received is not 200: res.status_code %d from the server; pdate = %s' \
                % (res.status_code, str(refdate))
    pdatetime = datetime.datetime.now()
    print(error_msg, pdatetime)
    res_bcb_api = namedtuple_bcb_api1(
      cotacao_compra=None, cotacao_venda=None, cotacao_datahora=pdatetime,
      param_date=refdate,
      error_msg=error_msg, gen_msg=None,
      exchanger=None
    )
    return res_bcb_api
  resdict = json.loads(res.text)
  try:
    valuedict = resdict['value'][0]
  except IndexError:
    # in general, this case means that the date does not have quotes as happens for holidays and weekend days
    # but the important fact is that the response came with a 200 OK status code
    datatime_cotacao = dtfs.convert_date_to_datetime_or_none(refdate)
    gen_msg = 'BCB API day with no quotes'
    print(gen_msg, refdate, datatime_cotacao)
    res_bcb_api = namedtuple_bcb_api1(
      cotacao_compra=None, cotacao_venda=None, cotacao_datahora=datatime_cotacao,
      param_date=refdate,
      error_msg=None, gen_msg=gen_msg,
      exchanger=None
    )
    return res_bcb_api
  if len(valuedict) == 0:
    # maybe this case never happens, and it's the above case when holidays or weekend days happen
    datatime_cotacao = dtfs.convert_date_to_datetime_or_none(refdate)
    res_bcb_api = namedtuple_bcb_api1(
      cotacao_compra=None, cotacao_venda=None, cotacao_datahora=datatime_cotacao,
      param_date=refdate,
      error_msg=None, gen_msg='BCB API len(valuedict) = 0',
      exchanger=None
    )
    return res_bcb_api
  print('result', resdict)
  cotacao_compra = valuedict['cotacaoCompra']
  cotacao_venda = valuedict['cotacaoVenda']
  data_hora_cotacao = valuedict['dataHoraCotacao']
  datatime_cotacao = dtfs.convert_str_or_attrsobj_to_datetime_or_none(data_hora_cotacao)
  res_bcb_api = namedtuple_bcb_api1(
    cotacao_compra=cotacao_compra, cotacao_venda=cotacao_venda, cotacao_datahora=datatime_cotacao,
    param_date=refdate,
    error_msg=None, gen_msg='BCB API',
    exchanger=None
  )
  return res_bcb_api


def pretry_print_api_list(res_bcb_api1_list):
  """
  namedtuple_bcb_api1 =
    coll.namedtuple('BCBAPI1DataStr', 'cotacao_compra cotacao_venda cotacao_datahora param_date error_msg')

  :param res_bcb_api1_list:
  :return:
  """
  ptab = PrettyTable()
  ptab.field_names = ['Seq', 'cotacao_compra', 'cotacao_venda', 'cotacao_datahora',
                      'param_date', 'error_msg', 'gen_msg']
  last_str_date = ''
  for i, res_api1_nt in enumerate(res_bcb_api1_list):
    seq = i + 1
    ptab.add_row([
      seq,
      res_api1_nt.cotacao_compra,
      res_api1_nt.cotacao_venda,
      res_api1_nt.cotacao_datahora,
      res_api1_nt.param_date,
      res_api1_nt.error_msg,
      res_api1_nt.gen_msg
    ])
    last_str_date = str(res_api1_nt.param_date)
  print(ptab)
  datafolder_abspath = sett.get_datafolder_abspath()
  filename = 'exchange_rate_monthly_quotes_' + last_str_date + '.log'
  datafile_abspath = os.path.join(datafolder_abspath, filename)
  fp = open(datafile_abspath, 'w', encoding='utf8')
  print('Writing datafile_abspath', datafile_abspath)
  fp.write(str(ptab))
  fp.close()


def adhoc_test():
  dates = []
  strdate = '2020-07-30'
  pdate = dtfs.returns_date_or_today(strdate)
  dates.append(pdate)
  # pdate = dtfs.returns_date_or_today()
  strdate = '2020-07-31'
  pdate = dtfs.returns_date_or_today(strdate)
  dates.append(pdate)
  res_bcb_api1_list = []
  for pdate in dates:
    res_api1_nt = call_api_bcb_cotacao_dolar_on_date(pdate)
    res_bcb_api1_list.append(res_api1_nt)
  pretry_print_api_list(res_bcb_api1_list)


def process():
  # adhoc_test_ptab()
  adhoc_test()


if __name__ == "__main__":
  process()
