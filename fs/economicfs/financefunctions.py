#!/usr/bin/env python3
import datetime, json, requests
import fs.datefs.datefunctions as dtfs
import collections as coll
'''
The main function in this module is call_api_bcb_cotacao_dolar_on_date()
  See its docstring for info. 
'''

MonetCorrNT = coll.namedtuple('MonetCorrNamedTuple',
                'ini_montant, fin_montant, '
                'ini_rate, fin_rate, '
                'corr_fraction, '
                'ini_date, fin_date, '
                'ret_ini_date, ret_fin_date'
              )

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
  when there's no currency exchange quote, 'value' is [], ie, the empty list,
    if, on the other hand, there is data, we're interested in the element-0 which is a dict (in Python terms).

* Time backword recursion:
  On weekdays or holidays, there is no exchange info. Because of that, the functions looks up
    to see if value is [] (ie, the empty list) and tries again one day before.
    However, constant API_CALL_COTACAO_MAX_PREVIOUS_DAY_TRIES defines the maximum number of retries.

  The caller can also check where a date is a weekend day or a holiday in Brasil and
    in that case the max tries constant can very well be 0, ie, no retries.
  (This constant can be placed in config.py at the app's root folder, so that it can be changed from there.)

  :param pdate:
  :param recurse_pass:
  :return:
  '''
  if recurse_pass > API_CALL_COTACAO_MAX_PREVIOUS_DAY_TRIES:
    return None, pdate
  refdate = dtfs.get_date_or_previous_monday_to_friday(pdate)
  mmddyyyy = dtfs.convert_date_to_mmddyyyy_str(refdate)
  if mmddyyyy is None:
    return None, pdate
  url = url_base + url_quer_interpol %{'mmddyyyy': mmddyyyy}
  print ('calling', url)
  res = requests.get(url)
  if res.status_code != 200:
    print('res.status_code', res.status_code)
    return None, pdate
  resdict = json.loads(res.text)
  valuedict = resdict['value'][0]
  if valuedict == []:
    previous_date = refdate - datetime.timedelta(days=1)
    return call_api_bcb_cotacao_dolar_on_date(previous_date, recurse_pass + 1)
  print('result', resdict)
  cotacaoCompra = valuedict['cotacaoCompra']
  dataHoraCotacao = valuedict['dataHoraCotacao']
  dataCotacao = dtfs.convert_yyyymmdd_strdate_to_dtdate(dataHoraCotacao)
  return cotacaoCompra, dataCotacao

CURR_BRL = 'BRL'
CURR_EUR = 'EUR'
CURR_USD = 'USD'
CURRENCIES = [CURR_BRL, CURR_USD, CURR_EUR]
DEFAULT_CURRENCY = CURR_BRL

def calculate_monet_corr_value_from_past_brl_indexed_by_usd(ini_montant, ini_date, fin_date):
  '''
  '''
  fin_rate, ret_fin_date = call_api_bcb_cotacao_dolar_on_date(fin_date)
  if fin_rate is None:
    print  ('On fin_date', fin_date)
    monet_corr_nt = MonetCorrNT(
      ini_montant = ini_montant, fin_montant = None,
      ini_rate = None, fin_rate = None,
      corr_fraction = 0,
      ini_date = ini_date, fin_date = fin_date,
      ret_ini_date = None, ret_fin_date = ret_fin_date
    )
    return monet_corr_nt
  if ret_fin_date > ini_date:
    ini_rate, ret_ini_date  = call_api_bcb_cotacao_dolar_on_date(ini_date)
    if ini_rate is None:
      print('On ini_rate', ini_rate)
      monet_corr_nt = MonetCorrNT(
        ini_montant=ini_montant, fin_montant=ini_montant, # notice that ini_date cannot be greater than fin_date here
        ini_rate=None, fin_rate=fin_rate,
        corr_fraction=0,
        ini_date=ini_date, fin_date=fin_date,
        ret_ini_date=ret_ini_date, ret_fin_date=ret_fin_date
      )
      return monet_corr_nt
    corr_fraction = abs(ini_rate - fin_rate) / ini_rate
  else:
    ret_ini_date = ret_fin_date
    ini_rate = fin_rate
    corr_fraction = 0
  fin_montant = ini_montant * (1 + corr_fraction)
  print ('On fin_date =', fin_date, '| fin_rate =', fin_rate, '| ret_fin_date =', ret_fin_date)
  print ('On ini_date', ini_date, '| ini_rate', ini_rate, '| ret_ini_date =', ret_ini_date)
  print('BRL ini_montant =', ini_montant, '| fin_montant =', fin_montant)
  monet_corr_nt = MonetCorrNT(
    ini_montant=ini_montant, fin_montant=fin_montant,  # notice that ini_date cannot be greater than fin_date here
    ini_rate=ini_rate, fin_rate=fin_rate,
    corr_fraction=corr_fraction,
    ini_date=ini_date, fin_date=fin_date,
    ret_ini_date=ret_ini_date, ret_fin_date=ret_fin_date
  )
  return monet_corr_nt

def monetarily_correct_by_exchange_rate(ini_montant, ini_date, fin_date=None, curr=CURR_BRL, indexed_by_curr=CURR_USD):
  '''

  :param ini_montant:
  :param ini_date:
  :param fin_date:
  :param curr:
  :param indexed_by_curr:
  :return: MonetCorrNamedTuple
  '''
  if fin_date is None:
    fin_date = datetime.date.today()
  else:
    fin_date = dtfs.get_date_or_previous_monday_to_friday(fin_date)
  if fin_date == datetime.date.today():
    fin_date = fin_date - datetime.timedelta(days=1)
  ini_date = dtfs.get_date_or_previous_monday_to_friday(ini_date)
  deltatime = fin_date - ini_date
  if abs(deltatime.days) < 4:
    # in this case, no conversion is necessary, to-value is equal to from-value
    monet_corr_nt = MonetCorrNT(
      ini_montant=ini_montant, fin_montant=ini_montant,  # notice that ini_date cannot be greater than fin_date here
      ini_rate=None, fin_rate=None,
      corr_fraction=0,
      ini_date=ini_date, fin_date=fin_date,
      ret_ini_date=None, ret_fin_date=None
    )
    return monet_corr_nt
  if indexed_by_curr == CURR_USD and curr == CURR_BRL:
    # the 9-field NameTuple above described will be returned
    return calculate_monet_corr_value_from_past_brl_indexed_by_usd(ini_montant, ini_date, fin_date)
  elif indexed_by_curr == CURR_EUR and curr == CURR_BRL:
    pass
  monet_corr_nt = MonetCorrNT(
    ini_montant=ini_montant, fin_montant=None,  # notice that ini_date cannot be greater than fin_date here
    ini_rate=None, fin_rate=None,
    corr_fraction=None,
    ini_date=ini_date, fin_date=fin_date,
    ret_ini_date=None, ret_fin_date=None
  )
  return monet_corr_nt

def adhoc_test2():
  # converted_money = convert_fromto_currency(10, CURR_USD, CURR_BRL)
  daterange = dtfs.get_daterange('20200720', '20200717')
  exchangedate = None
  for refdate in daterange:
    if dtfs.is_date_weekend(refdate):
      print('refdate is weekend', refdate)
      continue
    if exchangedate is not None:
      if refdate >= exchangedate: # notice daterange is reversed, ie, it loops day by day to the past
        print('refdate has already been taken', refdate)
        continue
    exchangeratio, exchangedate = call_api_bcb_cotacao_dolar_on_date(refdate)
    print(refdate, 'exchangeratio =', exchangeratio, 'exchangedate =', exchangedate)

def adhoc_test3():
  ini_montant = 273.45; ini_date = '2011-11-12'
  print ('ini_montant =', ini_montant, ' ini_date = ', ini_date)
  print ('Processing:')
  monet_corr_nt = monetarily_correct_by_exchange_rate(ini_montant, ini_date, fin_date=None, curr=CURR_BRL, indexed_by_curr=CURR_USD)
  print ('monet_corr_nt =', monet_corr_nt)

def adhoc_test():
  '''
  'final_montant, corr_fraction, ini_rate, fin_rate, ret_ini_date, ret_fin_date'
  :return:
  '''
  ini_montant = 123
  corr_fraction = 0.12
  ini_rate = 3.54
  fin_rate = 4.21
  corr_fraction = abs(ini_rate - fin_rate) / ini_rate
  fin_montant = ini_montant * (1 + corr_fraction)
  ini_date = '2018-6-11'
  fin_date = '2019-10-11'
  monet_corr_nt=MonetCorrNT(
    ini_montant=ini_montant, fin_montant=fin_montant,  # notice that ini_date cannot be greater than fin_date here
    ini_rate=ini_rate, fin_rate=fin_rate,
    corr_fraction=corr_fraction,
    ini_date=ini_date, fin_date=fin_date,
    ret_ini_date=ini_date, ret_fin_date=fin_date
    )
  print (monet_corr_nt)

def process():
  adhoc_test()
  adhoc_test3()

if __name__ == "__main__":
  process()
