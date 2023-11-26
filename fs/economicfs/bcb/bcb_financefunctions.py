#!/usr/bin/env python3
"""
  budgets worksheets pyapp
  This module is intended to contain (mostly) financial (def) functions.

  One of the important functions here is a gateway to fetching exchange rate quotes
    either via an API or from a sqlite db.
  Exchange rate quotes, when fetched online, are kept in a sqlite file, so it's somehow like a history buffer.

  @date 2020-07-29 
  @author Luiz Lewis
"""
import collections as coll
import datetime
import fs.datefs.datefunctions as dtfs
import fs.economicfs.bcb_api_finfunctions as apis

MonetCorrNT = coll.namedtuple(
  'MonetCorrNamedTuple',
  'ini_montant, fin_montant, '
  'ini_rate, fin_rate, '
  'corr_fraction, '
  'ini_date, fin_date, '
  'ret_ini_date, ret_fin_date'
)

CURR_BRL = 'BRL'
CURR_EUR = 'EUR'
CURR_USD = 'USD'
CURRENCIES = [CURR_BRL, CURR_USD, CURR_EUR]
DEFAULT_CURRENCY = CURR_BRL


def fetch_cotacao_brl_per_usd_for_datelist(datelist):
  # datelist = dtfs.prepare_datelist_uniq_n_in_desc_order(datelist)
  quote_n_date_resultlist = []
  for pdate in datelist:
    mdy = dtfs.convert_sep_or_datefields_position_for_ymdstrdate(
      pdate, tosep='-', sourceposorder='ymd', targetposorder='mdy'
    )
    print('mdy', mdy)
    cotacao_compra, data_cotacao = apis.call_api_bcb_cotacao_dolar_on_date(mdy)
    quote_n_date_resultlist.append((cotacao_compra, data_cotacao))
    print('For', pdate, 'api returned =>', cotacao_compra, data_cotacao)
  return quote_n_date_resultlist


def fetch_cotacao_brl_per_usd_within_inidate_n_findate(inidate, findate):
  daterange = dtfs.get_daterange_asc_or_desc(inidate, findate, makes_desc=True)
  return fetch_cotacao_brl_per_usd_for_datelist(daterange)


def calculate_monet_corr_value_from_past_brl_indexed_by_usd(ini_montant, ini_date, fin_date):
  """
  """
  fin_rate, ret_fin_date = apis.call_api_bcb_cotacao_dolar_on_date(fin_date)
  if fin_rate is None:
    print('On fin_date', fin_date)
    monet_corr_nt = MonetCorrNT(
      ini_montant=ini_montant, fin_montant=None,
      ini_rate=None, fin_rate=None,
      corr_fraction=0,
      ini_date=ini_date, fin_date=fin_date,
      ret_ini_date=None, ret_fin_date=ret_fin_date
    )
    return monet_corr_nt
  if ret_fin_date > ini_date:
    ini_rate, ret_ini_date = apis.call_api_bcb_cotacao_dolar_on_date(ini_date)
    if ini_rate is None:
      print('On ini_rate', ini_rate)
      monet_corr_nt = MonetCorrNT(
        ini_montant=ini_montant, fin_montant=ini_montant,  # notice that ini_date cannot be greater than fin_date here
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
  print('On fin_date =', fin_date, '| fin_rate =', fin_rate, '| ret_fin_date =', ret_fin_date)
  print('On ini_date', ini_date, '| ini_rate', ini_rate, '| ret_ini_date =', ret_ini_date)
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
  """

  :param ini_montant:
  :param ini_date:
  :param fin_date:
  :param curr:
  :param indexed_by_curr:
  :return: MonetCorrNamedTuple
  """
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
      if refdate >= exchangedate:  # notice daterange is reversed, ie, it loops day by day to the past
        print('refdate has already been taken', refdate)
        continue
    exchangeratio, exchangedate = apis.call_api_bcb_cotacao_dolar_on_date(refdate)
    print(refdate, 'exchangeratio =', exchangeratio, 'exchangedate =', exchangedate)


def adhoc_test3():
  ini_montant = 273.45
  ini_date = '2011-11-12'
  print('ini_montant =', ini_montant, ' ini_date = ', ini_date)
  print('Processing:')
  monet_corr_nt = monetarily_correct_by_exchange_rate(
    ini_montant, ini_date, fin_date=None, curr=CURR_BRL, indexed_by_curr=CURR_USD
  )
  print('monet_corr_nt =', monet_corr_nt)


def adhoc_test():
  """
  'final_montant, corr_fraction, ini_rate, fin_rate, ret_ini_date, ret_fin_date'
  :return:
  """
  ini_montant = 123
  ini_rate = 3.54
  fin_rate = 4.21
  corr_fraction = abs(ini_rate - fin_rate) / ini_rate
  fin_montant = ini_montant * (1 + corr_fraction)
  ini_date = '2018-6-11'
  fin_date = '2019-10-11'
  monet_corr_nt = MonetCorrNT(
    ini_montant=ini_montant, fin_montant=fin_montant,  # notice that ini_date cannot be greater than fin_date here
    ini_rate=ini_rate, fin_rate=fin_rate,
    corr_fraction=corr_fraction,
    ini_date=ini_date, fin_date=fin_date,
    ret_ini_date=ini_date, ret_fin_date=fin_date
    )
  print(monet_corr_nt)


def process():
  pass


if __name__ == "__main__":
  process()
