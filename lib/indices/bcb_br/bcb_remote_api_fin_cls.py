#!/usr/bin/env python3
"""
fs/indices/bcb_br/bcb_remote_api_fin_cls.py

  Contains class BcbCotacaoDiaApiCaller class which in turn, contains method
    recurs_call_api_bcb_cotacao_dolar_on_daysdate()

@See also its docstring for info.
  
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
import datetime
import json
import os
from prettytable import PrettyTable
import requests
import settings as sett
import time
import lib.datefs.convert_to_date_wo_intr_sep_posorder as cnv
import lib.datefs.introspect_dates as intr
from art.inflmeas.bcb_br.fetch.prettyprint.fetch_exchrate_fr_dates_in_textfile import REGISTERED_CURRENCIES_3LETTER
import lib.indices.bcb_br.bcbparams as bcbparams
# import fs.datefs.convert_to_datetime_wo_intr_sep_posorder as cvdt
url_base = bcbparams.url_base
url_query_interpol = bcbparams.url_query_interpol
MAX_BCB_COTACAODIA_API_MAX_PREVIOUSDAY_CALLS = bcbparams.MAX_BCB_COTACAODIA_API_MAX_PREVIOUSDAY_CALLS
MAX_BCB_COTACAODIA_API_CONN_TRIES = bcbparams.MAX_BCB_COTACAODIA_API_CONN_TRIES
namedtuple_bcb_api1 = bcbparams.namedtuple_bcb_api1
# 1) cotacao_compra is cotacaoCompra, 2) cotacao_venda is cotacaoVenda &  3) cotacao_datahora is dataHoraCotacao


class BcbCotacaoDiaApiCaller:

  MAX_BCB_COTACAODIA_API_CONN_TRIES = MAX_BCB_COTACAODIA_API_CONN_TRIES

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
    self.exchanger = None
    self.error_msg = None
    self.gen_msg = None
    self.n_of_connection_errors_raised = 0
    self.n_method_calls = 0
    self.n_api_being_called = 0
    self.treat_attrs()

  def treat_attrs(self):
    self.daysdate = cnv.make_date_or_none(self.daysdate)
    if self.curr_num is None or self.curr_num not in REGISTERED_CURRENCIES_3LETTER:
      self.curr_num = sett.CURR_BRL
    if self.curr_den is None or self.curr_den not in REGISTERED_CURRENCIES_3LETTER:
      self.curr_den = sett.CURR_BRL

  @property
  def nt_bcb_api_result(self) -> namedtuple_bcb_api1:
    _res_bcb_api = namedtuple_bcb_api1(
      curr_num=self.curr_num, curr_den=self.curr_den,
      cotacao_compra=self.buyprice, cotacao_venda=self.buyprice, cotacao_datahora=self.datahoracotacao,
      param_date=self.daysdate,
      error_msg=self.error_msg, gen_msg=self.gen_msg,
      exchanger=self.exchanger
    )
    return _res_bcb_api

  def if_conn_max_tries_is_reached_fillin_attrs_n_return_true(self, givendate) -> bool:
    """
    """
    if self.n_of_connection_errors_raised > self.MAX_BCB_COTACAODIA_API_CONN_TRIES:
      self.error_msg = (
          'Finishing connection attempts: connection_error_raised > 10 (n_conn_errs=%d)'
          % self.n_of_connection_errors_raised
      )
      # raise requests.exceptions.ConnectionError(self.error_msg)
      self.error_msg = 'Given date [%s] is None' % str(givendate)
      return True
    return False

  @property
  def days_mmddyyyy_date(self) -> str:
    """
    # the API accepts a data in the format 'MM/DD/YYYY', so it needs to convert pdate to it

    """
    mmddyyyy = intr.trans_strdate_from_one_format_to_another_w_sep_n_posorder(
      self.daysdate, fromsep=None, tosep='/', sourceposorder=None, targetposorder='mdy')
    if mmddyyyy is None:
      error_msg = f"""An error occurred when trying to convert date {self.daysdate} to a mdy sep-/-format,
      (i.e., "mm/dd/yyyy" date format), it got None.  This convertion is necessary to call the
        BCB REST API for fetching BRL/USD exchange rate date."""
      raise ValueError(error_msg)
    return mmddyyyy

  def recurs_call_api_bcb_cotacao_dolar_on_daysdate(self) -> namedtuple_bcb_api1:
    """
    pdate, curr_num=None, curr_den=None, connection_error_raised=0

    This function calls an endpoint API from the Banco Central do Brasil (BCB) web services.
    Consider it a PRIVATE function in the sense that it should not be called from 'general clients'.

    Instead, these (general) clients should call:
      preapis_finfunctions.dbfetch_bcb_cotacao_dolar_or_apifallback()

    This is necessary for the following reasons:
      1) the entrance function (in preapis above) filters out weekend days (that do not have quotes);
      2) the entrance function checks a local 'buffer' database for the asked info;
      3) the entrance function envelops this so that it may chace the API response to DB and/or file.

  * The guide page for it is:
      https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/aplicacao#!/recursos/CotacaoDolarDia

  * An example follows:
    https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)
      ?@dataCotacao='07-23-2020'&$top=100&$format=json
    The JsonToDict Result, for the URL above, is:
    '{'
      '@odata.context': 'https://was-p.bcnet.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata$metadata#_CotacaoDolarDia',
      'value':[{'cotacaoCompra': 5.1641, 'cotacaoVenda': 5.1647, 'dataHoraCotacao': '2020-07-23 13:02:43.561'}]
    }

  * Notice:
    when there's no currency exchange quote data, server answers 'value' as [],
      i.e., the empty list, if, on the other hand, there is data,
      we're interested in the element-0 which is a dict (in Python terms).

  * Time backward recursion:
    On weekdays or holidays, there is no exchange info.
      Because of that, the functions looks up
      to see if value is [] (ie, the empty list) and tries again one day before.
    However, constant API_CALL_COTACAO_MAX_PREVIOUS_DAY_TRIES
      defines the maximum number of retries.
    Because of that attempt, the dataCotacao will also be returned so that
      incoming (input) pdate and dataCotacao may be compared.

    The caller can also check where a date is a weekend day or a holiday in Brazil and
      in that case the max-tries constant can very well be 0, ie, no retries.
    (This constant can be placed in settings.py at the app's root folder,
      so that it can be changed from there.)

    """
    self.n_method_calls += 1
    # this is the max-limit of tries condition to end of the recursion
    if self.if_conn_max_tries_is_reached_fillin_attrs_n_return_true:
      return self.nt_bcb_api_result
    scrmsg = "-"*40
    print(scrmsg)
    url = url_base + url_query_interpol % {'mmddyyyy': self.days_mmddyyyy_date}
    self.n_api_being_called += 1
    scrmsg = f"{self.n_api_being_called}/{self.n_method_calls} => Issuing: [{url}]"
    print(scrmsg)
    scrmsg = "-"*40
    print(scrmsg)
    try:
      res = requests.get(url)
    except requests.exceptions.ConnectionError:
      self.n_of_connection_errors_raised += 1
      wait_in_sec = 3 + self.n_of_connection_errors_raised
      scrmsg = "-+-" * 10
      print(scrmsg)
      recurse_msg = f'api_n={self.n_api_being_called}/meth_n={self.n_method_calls} | '
      recurse_msg += '[ConnectionError raised on recurse] acc times=%d :: wait %d seconds' \
                     % (self.n_of_connection_errors_raised + 1, wait_in_sec)
      print(recurse_msg)
      scrmsg = "-+-" * 10
      print(scrmsg)
      time.sleep(wait_in_sec)
      # recurse on for a new try
      return self.recurs_call_api_bcb_cotacao_dolar_on_daysdate()
    # check if status code received is not "200 OK"
    if res.status_code != 200:
      scrmsg = "-+-" * 10
      print(scrmsg)
      error_msg = (
        'Error: HTTP Connection status received is not "200 OK":'
        ' res.status_code %d from the server; pdate = %s'
        % (res.status_code, str(self.daysdate))
      )
      self.datahoracotacao = datetime.datetime.now()
      error_msg = f"{self.datahoracotacao}: {error_msg}"
      print(error_msg)
      scrmsg = "-+-" * 10
      print(scrmsg)
      # returning and finishing recursion
      return self.nt_bcb_api_result
    # at this point, status code received is "200 OK"
    scrmsg = ' => API call returned with status code received "200 OK"'
    print(scrmsg)
    scrmsg = "-"*40
    print(scrmsg)
    resdict = json.loads(res.text)
    try:
      valuedict = resdict['value'][0]
    except IndexError:
      # in general, this case means that the date does not have quotes as happens for holidays and weekend days
      # but the important fact is that the response came with a 200 OK status code
      self.gen_msg = f'BCB API returned day {self.daysdate} with no quotes'
      errmsg = f"Error: missing first dict element value in the received json payload: [{self.gen_msg}]"
      print(errmsg)
      return self.nt_bcb_api_result
    if len(valuedict) == 0:
      # maybe this case never happens, and it's the same as above case when holidays or weekend days happen
      # returning and finishing recursion
      return self.nt_bcb_api_result
    # the json payload is expected to have values
    # notice a try/except block is not enclosing this attribute extraction part: should it?
    scrmsg = f"Result {resdict}"
    print(scrmsg)
    self.buyprice = valuedict['cotacaoCompra']
    self.sellprice = valuedict['cotacaoVenda']
    self.datahoracotacao = valuedict['dataHoraCotacao']
    self.error_msg = None
    self.gen_msg = 'BCB API'
    self.exchanger = None
    # returning and finishing recursion
    return self.nt_bcb_api_result


def get_pretryprint_txtrepresentation_from_bcb_api1_list(res_bcb_api1_list):
  """
  namedtuple_bcb_api1 =
    coll.namedtuple('BCBAPI1DataStr', 'cotacao_compra cotacao_venda cotacao_datahora param_date error_msg')

  :param res_bcb_api1_list:
  :return:
  """
  ptab = PrettyTable()
  ptab.field_names = [
    'Seq', 'curr_num', 'curr_den',
    'cotacao_compra', 'cotacao_venda', 'cotacao_datahora',
    'param_date', 'error_msg', 'gen_msg'
  ]
  for i, res_api1_nt in enumerate(res_bcb_api1_list):
    seq = i + 1
    ptab.add_row([
      seq,
      res_api1_nt.curr_num,
      res_api1_nt.curr_den,
      res_api1_nt.cotacao_compra,
      res_api1_nt.cotacao_venda,
      res_api1_nt.cotacao_datahora,
      res_api1_nt.param_date,
      res_api1_nt.error_msg,
      res_api1_nt.gen_msg
    ])
  return str(ptab)


def write_txtdata_file(
    textdata: str,
    pdate: datetime.date | None = None,
    datafilename: str | None = None,
  ):
  pdate = cnv.make_date_or_none(pdate)
  datafolder_abspath = sett.get_datafolder_abspath()
  if datafilename is None:
    datafilename = f'exchange_rate_monthly_quotes_date={pdate}.log'
  datafile_abspath = os.path.join(datafolder_abspath, datafilename)
  fp = open(datafile_abspath, 'w', encoding='utf8')
  scrmsg = f'Writing datafile_abspath: [{datafile_abspath}]'
  print(scrmsg)
  fp.write(textdata)
  fp.close()


def adhoc_test():
  dates = []
  strdate = '2020-07-30'
  pdate = cnv.make_date_or_none(strdate)
  dates.append(pdate)
  # pdate = dtfs.returns_date_or_today()
  strdate = '2020-07-31'
  pdate = cnv.make_date_or_none(strdate)
  dates.append(pdate)
  res_bcb_api1_list = []
  for pdate in dates:
    caller = BcbCotacaoDiaApiCaller(pdate=pdate)
    res_api1_nt = caller.recurs_call_api_bcb_cotacao_dolar_on_daysdate()
    res_bcb_api1_list.append(res_api1_nt)
  datatext = get_pretryprint_txtrepresentation_from_bcb_api1_list(res_bcb_api1_list)
  write_txtdata_file(datatext)


def adhoctest2():
  pdate = '2023-12-18'
  pdate = cnv.make_date_or_none(pdate)
  print('Calling bcb_br api for date', pdate)
  caller = BcbCotacaoDiaApiCaller(pdate=pdate)
  res_api1_nt = caller.recurs_call_api_bcb_cotacao_dolar_on_daysdate()
  print(res_api1_nt)
  get_pretryprint_txtrepresentation_from_bcb_api1_list([res_api1_nt])
  datatext = get_pretryprint_txtrepresentation_from_bcb_api1_list(res_api1_nt)
  write_txtdata_file(datatext)


def process():
  # adhoc_test_ptab()
  adhoc_test()


if __name__ == "__main__":
  """
  process()
  """
  adhoctest2()
