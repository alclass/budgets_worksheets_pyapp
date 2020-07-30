#!/usr/bin/env python3
'''
The main function in this module is call_api_bcb_cotacao_dolar_on_date()
  See its docstring for info.
  
https://dadosabertos.bcb.gov.br/dataset/taxas-de-cambio-todos-os-boletins-diarios

Unidades de medida:

Moedas tipo A: Paridade (dólar): Quantidade da moeda por uma unidade de dólar americano (USD);
Cotação (unidade monetária corrente): Quantidade de moeda corrente por uma unidade da moeda

Moedas tipo B: Paridade (dólar): Quantidade de dólar americano (USD) por uma unidade da moeda;
Cotação (unidade monetária corrente): Quantidade de moeda corrente por uma unidade da moeda

Exemplo de cálculo da cotação das moedas tipo A em unidade monetária corrente, considerando o real (BRL) como unidade monetária corrente e o dólar canadense (CAD) como moeda estrangeira:

Cotação de Compra CADBRL = Cotação USDBRL de Compra ÷ Paridade USDCAD de Venda
Cotação de Venda CADBRL = Cotação USDBRL de Venda ÷ Paridade USDCAD de Compra

Exemplo de cálculo da cotação das moedas tipo B em unidade monetária corrente, considerando o real (BRL) como unidade monetária corrente e o euro (EUR) como moeda estrangeira:

Cotação de Compra EURBRL = Paridade EURUSD de Compra × Cotação USDBRL de Compra
Cotação de Venda EURBRL = Paridade EURUSD de Venda × Cotação USDBRL de Venda  

https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/documentacao

Para o Euro:
https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/aplicacao#!/recursos/CotacaoMoedaPeriodoFechamento

https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodoFechamento
  (codigoMoeda=@codigoMoeda,dataInicialCotacao=@dataInicialCotacao,dataFinalCotacao=@dataFinalCotacao)
  ?@codigoMoeda='EUR'&@dataInicialCotacao='07-09-2020'&@dataFinalCotacao='07-22-2020'&
  $top=100&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim
  
(Copy here the json result)
'''
import datetime, json, requests
from prettytable import PrettyTable
import xlsxwriter
import fs.datefs.datefunctions as dtfs

url_base = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)'
url_quer_interpol = "?@dataCotacao='%(mmddyyyy)s'&$top=100&$format=json"

API_CALL_COTACAO_MAX_PREVIOUS_DAY_TRIES = 8
def call_api_bcb_cotacao_dolar_on_date(pdate, recurse_pass=0):
  '''
  This function calls an endpoint API from the Banco Central site.

* The guide page for it is https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/aplicacao#!/recursos/CotacaoDolarDia
* An example follows:

  https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='07-23-2020'&$top=100&$format=json
  The JsonToDict Result, for the URL above, is:
{
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
  (This constant can be placed in config.py at the app's root folder,
    so that it can be changed from there.)

  :param pdate:
  :param recurse_pass:
  :return:
  '''
  if dtfs.returns_date_or_None(pdate) is None:
    return pdate, None, None
  if recurse_pass > API_CALL_COTACAO_MAX_PREVIOUS_DAY_TRIES:
    error_msg = 'Error: could not find an available exchange rate quote from the open BCB API within 10 days backwards from given date (%s)' %str(pdate)
    return pdate, error_msg, None
  refdate = dtfs.get_date_or_previous_monday_to_friday(pdate)
  # the API accepts a data in the format 'MM/DD/YYYY', so it needs to convert pdate to it
  mmddyyyy = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(pdate, targetposorder='mdy') # tosep='-',
  url = url_base + url_quer_interpol %{'mmddyyyy': mmddyyyy}
  print ('calling', url)
  res = requests.get(url)
  if res.status_code != 200:
    error_msg = 'Error: HTTP Connection status received is not 200: res.status_code %d from the server; pdate = %s' %(res.status_code, str(pdate))
    print(error_msg)
    return pdate, error_msg, None
  resdict = json.loads(res.text)
  try:
    valuedict = resdict['value'][0]
  except IndexError:
    error_msg = "Error: HTTP status received was 200 OK, but valuedict = resdict['value'][0] failed :: resdict = ||%s||" %(str(resdict))
    print(error_msg)
    return pdate, error_msg, None
  if valuedict == []:
    previous_date = refdate - datetime.timedelta(days=1)
    # recurse from here trying the previous day
    return call_api_bcb_cotacao_dolar_on_date(previous_date, recurse_pass + 1)
  print('result', resdict)
  cotacaoCompra = valuedict['cotacaoCompra']
  dataHoraCotacao = valuedict['dataHoraCotacao']
  dataCotacao = dtfs.convert_yyyymmdd_strdate_to_dtdate_or_None(dataHoraCotacao)
  return pdate, cotacaoCompra, dataCotacao

def adhoc_test():
  dates = []
  strdate = '2020-01-07'
  pdate = dtfs.returns_date_or_today(strdate)
  dates.append(pdate)
  pdate = dtfs.returns_date_or_today()
  dates.append(pdate)
  ptab = PrettyTable()
  ptab.field_names = ['Seq', 'Data', 'valor câmbio', 'data câmbio']
  for i, pdate in enumerate(dates):
    seq = i + 1
    cotacaoCompra, dataCotacao = call_api_bcb_cotacao_dolar_on_date(pdate)
    ptab.add_row([seq, pdate, cotacaoCompra, dataCotacao])
  print(ptab)

def process():
  # adhoc_test_ptab()
  adhoc_test()

if __name__ == "__main__":
  process()
